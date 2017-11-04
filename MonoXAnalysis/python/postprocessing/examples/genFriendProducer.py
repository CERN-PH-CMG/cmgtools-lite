import ROOT
import os
import numpy as np
ROOT.PyConfig.IgnoreCommandLineOptions = True

from CMGTools.MonoXAnalysis.postprocessing.framework.datamodel import Collection 
from CMGTools.MonoXAnalysis.postprocessing.framework.eventloop import Module

class GenQEDJetProducer(Module):
    def __init__(self,deltaR):
        self.deltaR = deltaR
        self.vars = ("pt","eta","phi","mass","pdgId")
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
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def initReaders(self,tree): # this function gets the pointers to Value and ArrayReaders and sets them in the C++ worker class
        self.nGenPart = tree.valueReader("nGenPart")
        for B in ("pt","eta","phi","mass","pdgId","isPromptHard") : setattr(self,"GenPart_"+B, tree.arrayReader("GenPart_"+B))
        self._worker.setGenParticles(self.nGenPart,self.GenPart_pt,self.GenPart_eta,self.GenPart_phi,self.GenPart_mass,self.GenPart_pdgId,self.GenPart_isPromptHard)
        self._ttreereaderversion = tree._ttreereaderversion # self._ttreereaderversion must be set AFTER all calls to tree.valueReader or tree.arrayReader

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        if event._tree._ttreereaderversion > self._ttreereaderversion: # do this check at every event, as other modules might have read further branches
            self.initReaders(event._tree)
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

        return True

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

genQEDJets = lambda : GenQEDJetProducer(deltaR=0.1)

