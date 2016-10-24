from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from CMGTools.VVResonances.tools.Pair import Pair
from PhysicsTools.HeppyCore.utils.deltar import *
from CMGTools.VVResonances.tools.VectorBosonToolBox import VectorBosonToolBox
from CMGTools.VVResonances.tools.BTagEventWeights import *
import itertools
import ROOT
import os
import math

class Substructure(object):
    def __init__(self):
        pass


class VVBuilder(Analyzer):
    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(VVBuilder,self).__init__(cfg_ana, cfg_comp, looperName)
        self.vbTool = VectorBosonToolBox()
        self.smearing=ROOT.TRandom(10101982)
        if hasattr(self.cfg_ana,"doPUPPI") and self.cfg_ana.doPUPPI:
            self.doPUPPI=True
            puppiJecCorrWeightFile = os.path.expandvars(self.cfg_ana.puppiJecCorrFile)
            self.puppiJecCorr = ROOT.TFile.Open(puppiJecCorrWeightFile)
            self.puppisd_corrGEN = self.puppiJecCorr.Get("puppiJECcorr_gen")
            self.puppisd_corrRECO_cen = self.puppiJecCorr.Get("puppiJECcorr_reco_0eta1v3")
            self.puppisd_corrRECO_for = self.puppiJecCorr.Get("puppiJECcorr_reco_1v3eta2v5")

        else:
            self.doPUPPI=False


        #btag reweighting
        self.btagSF = BTagEventWeights('btagsf',os.path.expandvars(self.cfg_ana.btagCSVFile))

    def declareHandles(self):
        super(VVBuilder, self).declareHandles()
        self.handles['packed'] = AutoHandle( 'packedPFCandidates', 'std::vector<pat::PackedCandidate>' )

    def copyLV(self,LV):
        out=[]
        for i in LV:
            out.append(ROOT.math.XYZTLorentzVector(i.px(),i.py(),i.pz(),i.energy()))
        return out

    def substructure(self,jet,event):
        #if we already filled it exit
        if hasattr(jet,'substructure'):
            return

        constituents=[]
        LVs = ROOT.std.vector("math::XYZTLorentzVector")()

        #we take LVs around the jets and recluster
        for LV in event.LVs:
            if deltaR(LV.eta(),LV.phi(),jet.eta(),jet.phi())<1.2:
                LVs.push_back(LV)

        interface = ROOT.cmg.FastJetInterface(LVs,-1.0,0.8,1,0.01,5.0,4.4)
        #make jets
        interface.makeInclusiveJets(150.0)

        outputJets = interface.get(True)
        if len(outputJets)==0:
            return

        #For the pruned sub jets +PUPPIcalculate the correction
        #without L1
        corrNoL1 = jet.corr/jet.CorrFactor_L1

        #if PUPPI reset the jet four vector
        if self.doPUPPI:
            jet.setP4(outputJets[0]*jet.corr)

        jet.substructure=Substructure()
        #OK!Now save the area
        jet.substructure.area=interface.getArea(1,0)



        #Get pruned lorentzVector and subjets
        interface.prune(True,0,0.1,0.5)


        jet.substructure.prunedJet = self.copyLV(interface.get(False))[0]*corrNoL1
        jet.substructure.prunedJetUp = 1.05*jet.substructure.prunedJet.mass()
        jet.substructure.prunedJetDown = 0.95*jet.substructure.prunedJet.mass()
        jet.substructure.prunedJetSmear = jet.substructure.prunedJet.mass()*self.smearing.Gaus(1.0,1.1)


        interface.makeSubJets(False,0,2)
        jet.substructure.prunedSubjets = self.copyLV(interface.get(False))

        #getv the btag of the pruned subjets
        jet.subJetTags=[-1.0,-1.0]
        jet.subJetCTagL=[-1.0,-1.0]
        jet.subJetCTagB=[-1.0,-1.0]
        jet.subJet_hadronFlavour=[0,0]
        jet.subJet_partonFlavour=[0,0]

        for i,s in enumerate(jet.substructure.prunedSubjets):
            for o in jet.subjets("SoftDrop"):
                dr=deltaR(s.eta(),s.phi(),o.eta(),o.phi())
                if dr<0.1:
                    found=True
                    jet.subJetTags[i] = o.bDiscriminator(self.cfg_ana.bDiscriminator)
                    jet.subJetCTagL[i] = o.bDiscriminator(self.cfg_ana.cDiscriminatorL)
                    jet.subJetCTagB[i] = o.bDiscriminator(self.cfg_ana.cDiscriminatorB)
                    jet.subJet_partonFlavour[i] = o.partonFlavour()
                    jet.subJet_hadronFlavour[i] = o.hadronFlavour()
                    break;


        #Get soft Drop lorentzVector and subjets


        interface.softDrop(True,0,0.0,0.1,0.8)
        jet.substructure.softDropJet = self.copyLV(interface.get(False))[0]*corrNoL1
        jet.substructure.softDropJetUp = 1.05*jet.substructure.softDropJet.mass()
        jet.substructure.softDropJetDown = 0.95*jet.substructure.softDropJet.mass()
        jet.substructure.softDropJetSmear = jet.substructure.softDropJet.mass()*self.smearing.Gaus(1.0,0.1)
        if self.doPUPPI:
            softDropJetUnCorr = self.copyLV(interface.get(False))[0]
            jet.substructure.softDropJetMassCor = self.getPUPPIMassWeight(softDropJetUnCorr)
            jet.substructure.softDropJetMassBare = softDropJetUnCorr.mass()

        interface.makeSubJets(False,0,2)
        jet.substructure.softDropSubjets = self.copyLV(interface.get(False))

        #get NTau
        jet.substructure.ntau = interface.nSubJettiness(0,4,0,6,1.0,0.8,999.0,999.0,999)
        # calculate DDT tau21 (currently without softDropJetMassCor, but the L2L3 corrections)
        jet.substructure.tau21_DDT = 0
        if (jet.substructure.softDropJet.mass() > 0):
            jet.substructure.tau21_DDT = jet.substructure.ntau[1]/jet.substructure.ntau[0] + ( 0.063 * math.log( (jet.substructure.softDropJet.mass()*jet.substructure.softDropJet.mass())/jet.substructure.softDropJet.pt()))

        #recluster with CA and do massdrop

        interface = ROOT.cmg.FastJetInterface(LVs,0.0,1.5,1,0.01,5.0,4.4)
        interface.makeInclusiveJets(150.0)

        mu= ROOT.Double(0.667)
        y= ROOT.Double(0.08)
        jet.substructure.massDropTag = interface.massDropTag(0,mu,y)
        jet.substructure.massDrop = (mu,y)


    def cleanOverlap(self,collection,toRemove):
        after=list(set(collection)-set(toRemove))
        return after


    def topology(self,VV,jets,leptons):
        VV.otherLeptons=leptons
        VV.satteliteJets=jets
        #VBF Tag
        if len(jets)>1:
            VV.vbfDEta = abs(jets[0].eta()-jets[1].eta())
            VV.vbfMass = (jets[0].p4()+jets[1].p4()).M()
        else:
            VV.vbfDEta = -999
            VV.vbfMass = -999

        # Btags
        jetsCentral = filter(lambda x: abs(x.eta())<2.4,jets)


        VV.satteliteCentralJets=jetsCentral
        # cuts are taken from https://twiki.cern.ch/twiki/bin/view/CMS/BtagRecommendation80X (20.06.2016)
        VV.nLooseBTags = len(filter(lambda x: x.bDiscriminator(self.cfg_ana.bDiscriminator)>0.460,jetsCentral))
        VV.nMediumBTags = len(filter(lambda x: x.bDiscriminator(self.cfg_ana.bDiscriminator)>0.800,jetsCentral))
        VV.nTightBTags = len(filter(lambda x: x.bDiscriminator(self.cfg_ana.bDiscriminator)>0.935,jetsCentral))
        VV.nOtherLeptons = len(leptons)

        maxbtag=-100.0

        VV.btagWeight=1.0
        for  j in jetsCentral:
            btag=j.bDiscriminator(self.cfg_ana.bDiscriminator)
            flavor = j.hadronFlavour()

            #btag event weight
            if self.cfg_comp.isMC:
                VV.btagWeight*= self.btagSF.getSF(j.pt(),j.eta(),flavor,btag)
            #and systematics
            if btag>maxbtag:
                maxbtag=btag
        VV.highestEventBTag = maxbtag



    def selectJets(self,jets,func,otherObjects,DR,otherObjects2=None,DR2=0.0):
        output=[]
        for j in jets:
            if not func(j):
                continue
            overlap=False
            for o in otherObjects:
                dr=deltaR(j.eta(),j.phi(),o.eta(),o.phi())
                if dr<DR:
                    overlap=True
                    break;
            if otherObjects2 !=None:
                for o in otherObjects2:
                    dr=deltaR(j.eta(),j.phi(),o.eta(),o.phi())
                    if dr<DR2:
                        overlap=True
                        break;
            if not overlap:
                output.append(j)
        return output


    def makeWV(self,event):
        output=[]

        #loop on the leptons
        looseLeptonsForW = filter(lambda x: (abs(x.pdgId())==11 and x.heepID) or (abs(x.pdgId())==13 and x.highPtIDIso ),event.selectedLeptons)
        tightLeptonsForW = filter(lambda x: (abs(x.pdgId())==11 and x.heepID and x.pt()>120) or (abs(x.pdgId())==13 and x.highPtIDIso and x.pt()>53 and abs(x.eta())<2.1),event.selectedLeptons)



        if len(tightLeptonsForW)==0:
            return output

        #make leptonic W
        W = self.vbTool.makeW(tightLeptonsForW,event.met)
        if len(W)==0:
            return output


        bestW = max(W,key = lambda x: x.leg1.pt())
        #now the jets
        fatJets=self.selectJets(event.jetsAK8,lambda x: x.pt()>200.0 and abs(x.eta())<2.4 and x.jetID('POG_PFID_Loose')  ,tightLeptonsForW,1.0)
        if len(fatJets)==0:
            return output
        bestJet = max(fatJets,key=lambda x: x.pt())

        VV=Pair(bestW,bestJet)
        if deltaR(bestW.leg1.eta(),bestW.leg1.phi(),bestJet.eta(),bestJet.phi())<ROOT.TMath.Pi()/2.0:
            return output
        if VV.deltaPhi()<2.0:
            return output
        if abs(deltaPhi(bestW.leg2.phi(),bestJet.phi()))<2.0:
            return output

        #substructure
        self.substructure(VV.leg2,event)
        if not hasattr(VV.leg2,'substructure'):
            return output

        #check if there are subjets

#        if len(VV.leg2.substructure.prunedSubjets)<2:
#            print 'No substructure',len(VV.leg2.substructure.prunedSubjets)
#            return output

        #topology
        satteliteJets = self.selectJets(event.jets,lambda x: x.pt()>30.0  and x.jetID('POG_PFID_Loose')  ,tightLeptonsForW,0.3,[bestJet],0.8)
        otherLeptons = self.cleanOverlap(looseLeptonsForW,[bestW.leg1])
        self.topology(VV,satteliteJets,otherLeptons)



        output.append(VV)
        return output



    def makeTOPCR(self,event):
        output=[]

        #loop on the leptons
        looseLeptonsForW = filter(lambda x: (abs(x.pdgId())==11 and x.heepID) or (abs(x.pdgId())==13 and x.highPtIDIso ),event.selectedLeptons)
        tightLeptonsForW = filter(lambda x: (abs(x.pdgId())==11 and x.heepID and x.pt()>120) or (abs(x.pdgId())==13 and x.highPtIDIso and x.pt()>53 and abs(x.eta())<2.1),event.selectedLeptons)


        if len(tightLeptonsForW)==0:
            return output

        #make leptonic W
        W = self.vbTool.makeW(tightLeptonsForW,event.met)
        if len(W)==0:
            return output


        bestW = max(W,key = lambda x: x.leg1.pt())
        #now the jets
        fatJets=self.selectJets(event.jetsAK8,lambda x: x.pt()>200.0 and abs(x.eta())<2.4 and x.jetID('POG_PFID_Loose')  ,tightLeptonsForW,1.0)
        fatJets=filter(lambda x: abs(deltaPhi(bestW.leg1.phi(),x.phi()))>ROOT.TMath.Pi()/2.0,fatJets)

        if len(fatJets)==0:
            return output

        bestJet = max(fatJets,key=lambda x: x.mass())

        VV=Pair(bestW,bestJet)
        if deltaR(bestW.leg1.eta(),bestW.leg1.phi(),bestJet.eta(),bestJet.phi())<ROOT.TMath.Pi()/2.0:
            return output
        if VV.deltaPhi()<2.0:
            return output
        if abs(deltaPhi(bestW.leg2.phi(),bestJet.phi()))<2.0:
            return output

        #substructure
        self.substructure(VV.leg2,event)

        if not hasattr(VV.leg2,"substructure"):
            return output

        #check if there are subjets

#        if len(VV.leg2.substructure.prunedSubjets)<2:
#            print 'No substructure',len(VV.leg2.substructure.prunedSubjets)
#            return output

        #topology
        satteliteJets = self.selectJets(event.jets,lambda x: x.pt()>30.0  and x.jetID('POG_PFID_Loose')  ,tightLeptonsForW,0.3,[bestJet],0.8)
        otherLeptons = self.cleanOverlap(looseLeptonsForW,[bestW.leg1])
        self.topology(VV,satteliteJets,otherLeptons)



        output.append(VV)
        return output





    def makeZV(self,event):
        output=[]

        #loop on the leptons


        leptonsForZ = filter(lambda x: (abs(x.pdgId())==11 and x.heepIDNoIso) or (abs(x.pdgId())==13 and (x.highPtID or x.highPtTrackID)),event.selectedLeptons)



        if len(leptonsForZ)<2:
            return output

        #make leptonic Z
        Z = self.vbTool.makeZ(leptonsForZ)
        if len(Z)==0:
            return output
        bestZ = max(Z,key = lambda x: x.pt())


        #other higbn pt isolated letpons in the event
        otherGoodLeptons=self.cleanOverlap(leptonsForZ,[bestZ.leg1,bestZ.leg2])
        otherTightLeptons = filter(lambda x: (abs(x.pdgId())==11 and x.heepID) or (abs(x.pdgId())==13 and (x.highPtIDIso)),otherGoodLeptons)
        #now the jets
        fatJets=self.selectJets(event.jetsAK8,lambda x: x.pt()>200.0 and abs(x.eta())<2.4 and x.jetID('POG_PFID_Loose')  ,[bestZ.leg1,bestZ.leg2],1.0)
        if len(fatJets)==0:
            return output
        bestJet = max(fatJets,key=lambda x: x.pt())

        VV=Pair(bestZ,bestJet)

        #substructure
        self.substructure(VV.leg2,event)

        if not hasattr(VV.leg2,"substructure"):
            return output


        #check if there are subjets

 #       if len(VV.leg2.substructure.prunedSubjets)<2:
 #           print 'No substructure',len(VV.leg2.substructure.prunedSubjets)
 #           return output

        #topology
        satteliteJets = self.selectJets(event.jets,lambda x: x.pt()>30.0  and x.jetID('POG_PFID_Loose')  ,otherTightLeptons,0.3,[bestJet],0.8)
        self.topology(VV,satteliteJets,otherTightLeptons)
        output.append(VV)
        return output



    def makeJJ(self,event):
        output=[]

        #loop on the leptons
        leptons= filter(lambda x: (abs(x.pdgId())==11 and x.heepID) or (abs(x.pdgId())==13 and x.highPtIDIso ),event.selectedLeptons)
        fatJets=self.selectJets(event.jetsAK8,lambda x: x.pt()>200.0 and abs(x.eta())<2.4 and x.jetID('POG_PFID_Tight')  ,leptons,1.0)

        if len(fatJets)<2:
            return output

        VV=Pair(fatJets[0],fatJets[1])

        #kinematics
        if abs(VV.leg1.eta()-VV.leg2.eta())>1.3 or VV.mass()<1000:
            return output

        self.substructure(VV.leg1,event)
        self.substructure(VV.leg2,event)


        if not hasattr(VV.leg1,"substructure"):
            return output

        if not hasattr(VV.leg2,"substructure"):
            return output

        #check if there are subjets

  #      if len(VV.leg2.substructure.prunedSubjets)<2 or len(VV.leg1.substructure.prunedSubjets)<2:
  #          print 'No substructure'
  #          return output



        #topology
        satteliteJets = self.selectJets(event.jets,lambda x: x.pt()>30.0  and x.jetID('POG_PFID_Loose')  ,leptons,0.3,[VV.leg1,VV.leg2],0.8)
        self.topology(VV,satteliteJets,leptons)
        output.append(VV)
        return output


    def makeMETV(self,event):
        output=[]

        #loop on the leptons
        leptons= filter(lambda x: (abs(x.pdgId())==11 and x.heepID) or (abs(x.pdgId())==13 and x.highPtIDIso ),event.selectedLeptons)
        fatJets=self.selectJets(event.jetsAK8,lambda x: x.pt()>200.0 and abs(x.eta())<2.4 and x.jetID('POG_PFID_Loose')  ,leptons,1.0)

        if len(fatJets)<1:
            return output

        VV=Pair(event.met,fatJets[0])

        #kinematics
        if VV.deltaPhi()<2.0 or VV.leg1.pt()<200:
            return output

        self.substructure(VV.leg2,event)

        if not hasattr(VV.leg2,"substructure"):
            return output


        #check if there are subjets

#        if len(VV.leg2.substructure.prunedSubjets)<2:
#            print 'No substructure'
#            return output


        #topology
        satteliteJets = self.selectJets(event.jets,lambda x: x.pt()>30.0  and x.jetID('POG_PFID_Loose')  ,leptons,0.3,[VV.leg2],0.8)
        self.topology(VV,satteliteJets,leptons)
        output.append(VV)
        return output



    def getPUPPIMassWeight(self, puppijet):
        # mass correction for PUPPI following https://github.com/thaarres/PuppiSoftdropMassCorr

        genCorr = 1.
        recoCorr = 1.
        # corrections only valid up to |eta| < 2.5, use 1. beyond
        if (abs(puppijet.eta()) < 2.5):
            genCorr = self.puppisd_corrGEN.Eval(puppijet.pt())
            if (abs(puppijet.eta()) <= 1.3):
                recoCorr = self.puppisd_corrRECO_cen.Eval(puppijet.pt())
            else:
                recoCorr = self.puppisd_corrRECO_for.Eval(puppijet.pt())
        totalWeight = genCorr*recoCorr
        return totalWeight



    def process(self, event):
        self.readCollections( event.input )
        #first create a set of four vectors to recluster jets later
        event.LVs = ROOT.std.vector("math::XYZTLorentzVector")()
        #load packed candidatyes
        cands = self.handles['packed'].product()

#        print "GEN LEPTONS-----"
#        for l in event.genleps:
#            print l.pdgId(),l.pt(),l.mother().pdgId()
#        print "GEN TAUS-"
#        for l in event.gentaus:
#            print l.pdgId(),l.pt(),l.mother().pdgId()

        #if use PUPPI weigh them or lese just pass through
        if self.doPUPPI:
            for c in cands:
                if c.pt()>13000 or c.pt()==float('Inf'):
                    continue;
                if c.puppiWeight()>0:
                    event.LVs.push_back(c.p4()*c.puppiWeight())
        else:
           for c in cands:
                if c.pt()>13000 or c.pt()==float('Inf'):
                    continue;
                event.LVs.push_back(c.p4())




        LNuJJ=self.makeWV(event)
        LLJJ =self.makeZV(event)
        JJ=self.makeJJ(event)
        JJNuNu=self.makeMETV(event)
#        TopCR=self.makeTOPCR(event)

        setattr(event,'LNuJJ'+self.cfg_ana.suffix,LNuJJ)
        setattr(event,'JJ'+self.cfg_ana.suffix,JJ)
        setattr(event,'LLJJ'+self.cfg_ana.suffix,LLJJ)
        setattr(event,'JJNuNu'+self.cfg_ana.suffix,JJNuNu)
#        setattr(event,'TopCR'+self.cfg_ana.suffix,TopCR)
