import ROOT
import os
import numpy as np
ROOT.PyConfig.IgnoreCommandLineOptions = True

from CMGTools.MonoXAnalysis.postprocessing.framework.datamodel import Collection 
from CMGTools.MonoXAnalysis.postprocessing.framework.eventloop import Module
from math import *

class SimpleVBoson:
    def __init__(self,legs):
        self.legs = legs
        if len(legs)<2:
            print "ERROR: making a VBoson w/ < 2 legs!"
        self.pt1 = legs[0].Pt()
        self.pt2 = legs[1].Pt()
        self.dphi = self.legs[0].Phi()-self.legs[1].Phi()
        self.deta = self.legs[0].Eta()-self.legs[1].Eta()
        self.px1 = legs[0].Px(); self.py1 = legs[0].Py();
        self.px2 = legs[1].Px(); self.py2 = legs[1].Py();
    def pt(self):
        return (self.legs[0]+self.legs[1]).Pt()
    def y(self):
        return (self.legs[0]+self.legs[1]).Rapidity()
    def mt(self):
        return sqrt(2*self.pt1*self.pt2*(1-cos(self.dphi)))
    def ux(self):
        return (-self.px1-self.px2)
    def uy(self):
        return (-self.py1-self.py2)    
    def mll(self):
        return sqrt(2*self.pt1*self.pt2*(cosh(self.deta)-cos(self.dphi)))

class KinematicVars:
    def __init__(self,beamE=7000):
        self.beamE = beamE
    def CSFrame(self,dilepton):
        pMass = 0.938272
        sign = np.sign(dilepton.Z())
        proton1 = ROOT.TLorentzVector(0.,0.,sign*self.beamE,hypot(self.beamE,pMass));  proton2 = ROOT.TLorentzVector(0.,0.,-sign*self.beamE,hypot(self.beamE,pMass))
        proton1.Boost(-dilepton.BoostVector()); proton2.Boost(-dilepton.BoostVector())
        CSAxis = (proton1.Vect().Unit()-proton2.Vect().Unit()).Unit()
        yAxis = (proton1.Vect().Unit()).Cross((proton2.Vect().Unit()));
        yAxis = yAxis.Unit();
        xAxis = yAxis.Cross(CSAxis);
        xAxis = xAxis.Unit();
        return (xAxis,yAxis,CSAxis)
    def cosThetaCS(self,lplus,lminus):
        dilep = lplus + lminus
        boostedLep = ROOT.TLorentzVector(lminus)
        boostedLep.Boost(-dilep.BoostVector())
        csframe = self.CSFrame(dilep)
        return cos(boostedLep.Angle(csframe[2]))
    def phiCS(self,lplus,lminus):
        dilep = lplus + lminus
        boostedLep = ROOT.TLorentzVector(lminus)
        boostedLep.Boost(-dilep.BoostVector())
        csframe = self.CSFrame(dilep)
        phi = atan2((boostedLep.Vect()*csframe[1]),(boostedLep.Vect()*csframe[0]))
        if(phi<0): return phi + 2*ROOT.TMath.Pi()
        else: return phi

class GenQEDJetProducer(Module):
    def __init__(self,deltaR,beamEn=7000.):
        self.beamEn=beamEn
        self.deltaR = deltaR
        self.vars = ("pt","eta","phi","mass","pdgId")
        self.genwvars = ("charge","pt","eta","phi","mass","y","costcs","phics")
        if "genQEDJetHelper_cc.so" not in ROOT.gSystem.GetLibraries():
            print "Load C++ Worker"
            ROOT.gROOT.ProcessLine(".L %s/src/CMGTools/MonoXAnalysis/python/postprocessing/helpers/genQEDJetHelper.cc+" % os.environ['CMSSW_BASE'])
        self._worker = ROOT.GenQEDJetHelper(deltaR)
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.initReaders(inputTree) # initReaders must be called in beginFile
        self.out = wrappedOutputTree
        self.out.branch("nGenLepDressed", "I")
        self.out.branch("nGenPromptNu", "I")
        for V in self.vars:
            self.out.branch("GenLepDressed_"+V, "F", lenVar="nGenLepDressed")
            self.out.branch("GenPromptNu_"+V, "F", lenVar="nGenPromptNu")
        for V in self.genwvars:
            self.out.branch("genw_"+V, "F")
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def initReaders(self,tree): # this function gets the pointers to Value and ArrayReaders and sets them in the C++ worker class
        try:
            self.nGenPart = tree.valueReader("nGenPart")
            for B in ("pt","eta","phi","mass","pdgId","isPromptHard") : setattr(self,"GenPart_"+B, tree.arrayReader("GenPart_"+B))
            self._worker.setGenParticles(self.nGenPart,self.GenPart_pt,self.GenPart_eta,self.GenPart_phi,self.GenPart_mass,self.GenPart_pdgId,self.GenPart_isPromptHard)
        except:
            print '[genFriendProducer][Warning] Unable to attach to generator-level particles (data only?). No info will be produced'
        self._ttreereaderversion = tree._ttreereaderversion # self._ttreereaderversion must be set AFTER all calls to tree.valueReader or tree.arrayReader

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        if event._tree._ttreereaderversion > self._ttreereaderversion: # do this check at every event, as other modules might have read further branches
            self.initReaders(event._tree)

        #nothing to do if this is data
        if event.isData: return

        # do NOT access other branches in python between the check/call to initReaders and the call to C++ worker code
        ## Algo
        self._worker.run()
        dressedLeptons = self._worker.dressedLeptons()
        neutrinos = self._worker.promptNeutrinos()
        lepPdgIds = self._worker.dressedLeptonsPdgId()
        nuPdgIds = self._worker.promptNeutrinosPdgId()
        
        retL={}
        retL["pt"] = [dl.Pt() for dl in dressedLeptons]
        retL["eta"] = [dl.Eta() for dl in dressedLeptons]
        retL["phi"] = [dl.Phi() for dl in dressedLeptons]
        retL["mass"] = [dl.M() for dl in dressedLeptons]
        retL["pdgId"] = [pdgId for pdgId in lepPdgIds]
        self.out.fillBranch("nGenLepDressed", len(dressedLeptons))
        for V in self.vars:
            self.out.fillBranch("GenLepDressed_"+V, retL[V])
        self.out.fillBranch("GenLepDressed_pdgId", [pdgId for pdgId in lepPdgIds])

        retN={}
        retN["pt"] = [nu.Pt() for nu in neutrinos]
        retN["eta"] = [nu.Eta() for nu in neutrinos]
        retN["phi"] = [nu.Phi() for nu in neutrinos]
        retN["mass"] = [nu.M() for nu in neutrinos]
        retN["pdgId"] = [pdgId for pdgId in lepPdgIds]
        self.out.fillBranch("nGenPromptNu", len(neutrinos))
        for V in self.vars:
            self.out.fillBranch("GenPromptNu_"+V, retN[V])
        self.out.fillBranch("GenPromptNu_pdgId", [pdgId for pdgId in nuPdgIds])

        if len(dressedLeptons) and len(neutrinos):
            genw = dressedLeptons[0] + neutrinos[0]
            self.out.fillBranch("genw_charge",float(-1*np.sign(lepPdgIds[0])))
            self.out.fillBranch("genw_pt",genw.Pt())
            self.out.fillBranch("genw_eta",genw.Eta())
            self.out.fillBranch("genw_phi",genw.Phi())
            self.out.fillBranch("genw_y",genw.Rapidity())
            self.out.fillBranch("genw_mass",genw.M())
            kv = KinematicVars(self.beamEn)
            # convention for phiCS: use l- direction for W-, use neutrino for W+
            (lplus,lminus) = (neutrinos[0],dressedLeptons[0]) if lepPdgIds[0]<0 else (dressedLeptons[0],neutrinos[0])
            self.out.fillBranch("genw_costcs",kv.cosThetaCS(lplus,lminus))
            self.out.fillBranch("genw_phics",kv.phiCS(lplus,lminus))
        else:
            for V in self.genwvars:
                self.out.fillBranch("genw_"+V, -999)

        return True

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

genQEDJets = lambda : GenQEDJetProducer(deltaR=0.1,beamEn=7000.)
genQEDJets13TeV = lambda : GenQEDJetProducer(deltaR=0.1,beamEn=13000.)

