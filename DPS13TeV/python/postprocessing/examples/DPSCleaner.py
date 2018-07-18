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
        self.jetlabelL = "_Clean_against_LL"
        self.jetlabelT = "_Clean_against_TL"
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
        self.out.branch("nJet25"+self.label,"I")
        self.out.branch("nJet25"+self.jetlabelL,"I")
        self.out.branch("nJet25"+self.jetlabelT,"I")

        self.out.branch("nbJetCSVL25"+self.label,"I")
        self.out.branch("nbJetCSVL25"+self.jetlabelT,"I")
        self.out.branch("nbJetCSVL25"+self.jetlabelL,"I")

        self.out.branch("nbJetCSVM25"+self.label,"I")
        self.out.branch("nbJetCSVL30"+self.label,"I")
        self.out.branch("nbJetCSVM30"+self.label,"I")

        self.out.branch("nTauGoodHad"+self.label,"I")

        #store default jets with pT > 25
        for V in self.vars:
            #jet with pT > 25 cleaned against LepGood
            self.out.branch("Jet"+self.label+"_"+V, "F", lenVar="nJet25"+self.label)
            # jets pt > 25 cleaned against loose leptons
            self.out.branch("Jet"+self.jetlabelL+"_"+V, "F", lenVar="nJet25"+self.jetlabelL)
            # jets pt > 25 cleaned against tight leptons
            self.out.branch("Jet"+self.jetlabelT+"_"+V, "F", lenVar="nJet25"+self.jetlabelT)
            #bjet with pT > 25 cleaned against LepGood
            self.out.branch("bJetCSVL25"+self.label+"_"+V, "F", lenVar="nbJetCSVL25"+self.label)
            #bjet with pT > 25 cleaned against loose leptons
            self.out.branch("bJetCSVL25"+self.jetlabelL+"_"+V, "F", lenVar="nbJetCSVL25"+self.jetlabelL)
            # bjet with pT > 25 cleaned against tight leptons
            self.out.branch("bJetCSVL25"+self.jetlabelT+"_"+V, "F", lenVar="nbJetCSVL25"+self.jetlabelT)

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
    def jetsel(self,jet):
        return (jet.pt > 25.0 and abs(jet.eta) < 2.4)
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
 
        hadtaus = filter(self.hadtau,Collection(event,"TauGood"))
        leptight = filter(self.lepTight,Collection(event,"LepGood"))
        leploose = filter(self.lepF0,Collection(event,"LepGood"))
        lep=Collection(event,"LepGood")
        jets= filter(self.jetsel,Collection(event,"Jet")) # jets are selected with a cut on pT and eta

        mindelR=0.4

        goodJetindex=[]  
        goodLJetindex=[]
        goodTJetindex=[]
        goodbJetindex=[] 
        goodLbJetindex=[]
        goodTbJetindex=[] 
        goodHadTauindex=[]

        nbjets25M=0
        nbjets30L=0
        nbjets30M=0
        njets30=0

        ret={}
        retTH={}
        retT={}
        retL={}
        retb={}
        retbL={}
        retbT={}
        
 
        for V in self.vars:
            ret["Jet"+self.label+"_"+V] = [getattr(j,V) for j in jets]
            #        for V in self.vars:
            retT["Jet"+self.jetlabelT+"_"+V] = [getattr(j,V) for j in jets]
            retL["Jet"+self.jetlabelL+"_"+V] = [getattr(j,V) for j in jets]
            retb["bJetCSVL25"+self.label+"_"+V] = [getattr(j,V) for j in jets]
            retbT["bJetCSVL25"+self.jetlabelT+"_"+V] = [getattr(j,V) for j in jets]
            retbL["bJetCSVL25"+self.jetlabelL+"_"+V] = [getattr(j,V) for j in jets]
        for TV in self.tauvars:
            retTH["TauGoodHad"+self.label+"_"+TV] = [getattr(j,TV) for j in hadtaus]

        for index,iJet in enumerate(jets):
            goodJ = True
            goodJL = True
            goodJT =True


            for iLep in lep:
                if (deltaR(iLep.eta,iLep.phi,iJet.eta,iJet.phi) < mindelR):
                    goodJ=False
                    break
            for iLep in leploose:
                if (deltaR(iLep.eta,iLep.phi,iJet.eta,iJet.phi) < mindelR):
                    goodJL=False
                    break
            for iLep in leptight:
                if (deltaR(iLep.eta,iLep.phi,iJet.eta,iJet.phi) < mindelR):
                    goodJT=False
                    break

            if goodJ: 
                goodJetindex.append(index)
                if self.loose25btag(iJet):
                    goodbJetindex.append(index)
                if self.medium25btag(iJet):
                    nbjets25M+=1
                if iJet.pt > 30 :
                    njets30+=1
                    if self.medium30btag(iJet):
                        nbjets30M+=1
                    if self.loose30btag(iJet):    
                        nbjets30L+=1

            if goodJL:
                goodLJetindex.append(index)
                if self.loose25btag(iJet):
                    goodLbJetindex.append(index)
            if goodJT:
                goodTJetindex.append(index)
                if self.loose25btag(iJet):
                    goodTbJetindex.append(index)

        for iT,iTau in enumerate(hadtaus):
            goodHadTau=True
            for iLep in leploose:
                if (deltaR(iLep.eta,iLep.phi,iTau.eta,iTau.phi) < mindelR):
                    goodHadTau=False
                    break
            if goodHadTau: 
                goodHadTauindex.append(iT)
        #print 'good had tau index %i'%len(goodHadTauindex)
        #print goodHadTauindex
        #print 'good jet index %i'%len(goodJetindex)
        #print goodJetindex



        self.out.fillBranch('nTauGoodHad'+self.label,len(goodHadTauindex))

        self.out.fillBranch('nbJetCSVL30'+self.label,nbjets30L)
        self.out.fillBranch('nbJetCSVM25'+self.label,nbjets25M)
        self.out.fillBranch('nbJetCSVM30'+self.label,nbjets30M)


        self.out.fillBranch('nJet25'+self.label, len(goodJetindex))
        self.out.fillBranch("nJet25"+self.jetlabelL,len(goodLJetindex))
        self.out.fillBranch("nJet25"+self.jetlabelT,len(goodTJetindex))

        self.out.fillBranch("nbJetCSVL25"+self.label,len(goodbJetindex))
        self.out.fillBranch("nbJetCSVL25"+self.jetlabelT,len(goodTbJetindex))
        self.out.fillBranch("nbJetCSVL25"+self.jetlabelL,len(goodLbJetindex))


        for V in self.vars:
            #print [ ret["Jet"+self.label+"_"+V][j] for j in goodJetindex]
            self.out.fillBranch("Jet"+self.label+"_"+V, [ ret["Jet"+self.label+"_"+V][j] for j in goodJetindex])
            self.out.fillBranch("Jet"+self.jetlabelL+"_"+V, [ retL["Jet"+self.jetlabelL+"_"+V][j] for j in goodLJetindex])
            self.out.fillBranch("Jet"+self.jetlabelT+"_"+V, [ retT["Jet"+self.jetlabelT+"_"+V][j] for j in goodTJetindex])
            self.out.fillBranch("bJetCSVL25"+self.label+"_"+V, [ retb["bJetCSVL25"+self.label+"_"+V][j] for j in goodbJetindex])
            self.out.fillBranch("bJetCSVL25"+self.jetlabelL+"_"+V, [ retbL["bJetCSVL25"+self.jetlabelL+"_"+V][j] for j in goodLbJetindex])
            self.out.fillBranch("bJetCSVL25"+self.jetlabelT+"_"+V, [ retbT["bJetCSVL25"+self.jetlabelT+"_"+V][j] for j in goodTbJetindex])


        for TV in self.tauvars:
            self.out.fillBranch("TauGoodHad"+self.label+"_"+TV, [retTH["TauGoodHad"+self.label+"_"+TV][j] for j in goodHadTauindex ])
            #print [retTH["TauGoodHad"+self.label+"_"+TV][j] for j in goodHadTauindex ]
        return True
TauHadFlag = lambda : DPSCleaner(lambda j1 : j1.pt > 25 and j1.btagCSV > 0.5426,
                                 lambda j2 : j2.pt > 25 and j2.btagCSV > 0.8484,
                                 lambda j3 : j3.pt > 30 and j3.btagCSV > 0.5426,
                                 lambda j4 : j4.pt > 30 and j4.btagCSV > 0.8484)

#Disclaimer: Clean jets are stored with pT > 25 and abs(eta) < 2.4, which are either cleaned against LepGood or loose or tight leptons. For the btagged jets, same conditions and cleaning hold for the jets selected with loose WP of the btagger. For Medium WP of btagger, only the nbJets variables are stored for the jets with pT > 25 and 30!!
