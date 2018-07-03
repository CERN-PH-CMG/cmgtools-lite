import ROOT, os
ROOT.PyConfig.IgnoreCommandLineOptions = True
from math import *
from CMGTools.DPS13TeV.postprocessing.framework.datamodel import Collection
from CMGTools.DPS13TeV.postprocessing.framework.eventloop import Module
from PhysicsTools.HeppyCore.utils.deltar import deltaR

ROOT.gROOT.ProcessLine('.L %s/src/CMGTools/DPS13TeV/python/plotter/functions.cc+' % os.environ['CMSSW_BASE']);

class DPSCleaner(Module):
    def __init__(self,loose25btagsel,medium25btagsel,loose30btagsel,medium30btagsel):
        self.label = "_Clean" # "" if (label in ["",None]) else ("_"+label)
        self.vars = ("pt","eta","phi","mass","btagCSV")
        self.tauvars = ("pt","eta","phi","idMVAdR03","idDecayMode")
        self.loose25btag=loose25btagsel
        self.medium25btag=medium25btagsel
        self.loose30btag=loose30btagsel
        self.medium30btag=medium30btagsel
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("nJet"+self.label,"I")
        self.out.branch("nJet30"+self.label,"I")
        self.out.branch("nbJetCSVL25"+self.label,"I")
        self.out.branch("nbJetCSVM25"+self.label,"I")
        self.out.branch("nbJetCSVL30"+self.label,"I")
        self.out.branch("nbJetCSVM30"+self.label,"I")
        self.out.branch("nTauGoodHad"+self.label,"I")
        for V in self.vars:
            self.out.branch("Jet"+self.label+"_"+V, "F", lenVar="nJet"+self.label)
        for TV in self.tauvars:
            self.out.branch("TauGoodHad"+self.label+"_"+TV, "F", lenVar="nTauGoodHad"+self.label)

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def lepF0(self,lep):
        if (lep.pt > 20.0 and abs(lep.eta) < (2.5 if abs(lep.pdgId) == 11 else 2.4)):
            if abs(lep.pdgId)==11:
                return (lep.idEmuTTH and (abs(lep.eta) < 1.442 or abs(lep.eta) > 1.556))
            else: 
                return (lep.mediumMuonId > 0 and lep.mvaTTH > -1.0) #
        else:
            return False

    def lepTight(self,lep):
        if (lep.pt > 20.0 and lep.mvaTTH > 0.9 and abs(lep.eta) < (2.5 if abs(lep.pdgId) == 11 else 2.4)):
            if abs(lep.pdgId)==11:
                return (lep.idEmuTTH and (abs(lep.eta) < 1.442 or abs(lep.eta) > 1.556))
            else:
                return True
        else:
            return False
        
    def hadtau(self,tau):
        return (tau.pt > 20.0 and abs(tau.eta) < 2.3 and abs(tau.dxy) < 1000 and abs(tau.dz) < 0.2 and tau.idMVAdR03 >=2 and tau.idDecayMode)

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        mindelR=0.4
        goodJetindex=[] 
        goodHadTauindex=[]
        nbjets25L=0
        nbjets25M=0
        nbjets30L=0
        nbjets30M=0
        njets30=0
        ret={}
        retTH={}
        hadtaus = filter(self.hadtau,Collection(event,"TauGood"))
        leps = filter(self.lepTight, Collection(event,"LepGood"))
        lep=Collection(event,"LepGood")
        jets= Collection(event,"Jet")
        for V in self.vars:
            #           print V
            ret["Jet"+self.label+"_"+V] = [getattr(j,V) for j in jets]

        for TV in self.tauvars:
            retTH["TauGoodHad"+self.label+"_"+TV] = [getattr(j,TV) for j in hadtaus]

        for index,iJet in enumerate(jets):
            goodJ = True
            goodbJ =True
            if iJet.pt < 25:
                goodJ = False
            if iJet.pt < 30 and iJet.btagCSV < 0.5426:
                goodJ = False
            for iLep in lep:#here  
                if (deltaR(iLep.eta,iLep.phi,iJet.eta,iJet.phi) < mindelR):
                    #print 'deltaR b/w jet and lep %f'%deltaR(iLep.eta,iLep.phi,iJet.eta,iJet.phi)
                    goodJ=False
                break
            if goodJ: 
                goodJetindex.append(index)
                if iJet.pt > 30 :
                    njets30+=1
                    #print'iJet.pt %s'%iJet.pt
                if self.medium25btag(iJet):
                    nbjets25M+=1
                if self.loose25btag(iJet):    
                    nbjets25L+=1
                if self.medium30btag(iJet):
                    #print'medium30btagsel'
                    #print'iJet.pt %f'%iJet.pt
                    #print'iJet.btagCSV  %f'%iJet.btagCSV 
                    nbjets30M+=1
                if self.loose30btag(iJet):    
                    #print'loose30btagsel'
                    #print'iJet.pt %f'%iJet.pt
                    #print'iJet.btagCSV  %f'%iJet.btagCSV 
                    nbjets30L+=1

        for iT,iTau in enumerate(hadtaus):
            goodHadTau=True
            for iLep in leps:
                if (deltaR(iLep.eta,iLep.phi,iTau.eta,iTau.phi) < mindelR):
                    goodHadTau=False
                    break
            if goodHadTau: 
                goodHadTauindex.append(iT)
        #print 'good had tau index %i'%len(goodHadTauindex)
        #print goodHadTauindex
        #print 'good jet index %i'%len(goodJetindex)
        #print goodJetindex

        self.out.fillBranch('nJet'+self.label, len(goodJetindex))
        self.out.fillBranch('nJet30'+self.label, njets30)
        self.out.fillBranch('nTauGoodHad'+self.label,len(goodHadTauindex))
        self.out.fillBranch('nbJetCSVL25'+self.label,nbjets25L)
        self.out.fillBranch('nbJetCSVM25'+self.label,nbjets25M)
        self.out.fillBranch('nbJetCSVL30'+self.label,nbjets30L)
        self.out.fillBranch('nbJetCSVM30'+self.label,nbjets30M)

        for V in self.vars:
            #print [ ret["Jet"+self.label+"_"+V][j] for j in goodJetindex]
            self.out.fillBranch("Jet"+self.label+"_"+V, [ ret["Jet"+self.label+"_"+V][j] for j in goodJetindex])
        for TV in self.tauvars:
            self.out.fillBranch("TauGoodHad"+self.label+"_"+TV, [retTH["TauGoodHad"+self.label+"_"+TV][j] for j in goodHadTauindex ])
            #print [retTH["TauGoodHad"+self.label+"_"+TV][j] for j in goodHadTauindex ]
        return True
TauHadFlag = lambda : DPSCleaner(lambda j1 : j1.pt > 25 and j1.btagCSV > 0.5426,
                                 lambda j2 : j2.pt > 25 and j2.btagCSV > 0.8484,
                                 lambda j3 : j3.pt > 30 and j3.btagCSV > 0.5426,
                                 lambda j4 : j4.pt > 30 and j4.btagCSV > 0.8484)
