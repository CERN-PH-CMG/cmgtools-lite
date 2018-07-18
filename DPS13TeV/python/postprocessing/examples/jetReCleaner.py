import ROOT
import os
import numpy as np
ROOT.PyConfig.IgnoreCommandLineOptions = True

from CMGTools.DPS13TeV.postprocessing.framework.datamodel import Collection
from CMGTools.DPS13TeV.postprocessing.framework.eventloop import Module
import ROOT, os

class JetReCleaner(Module):
    def __init__(self,label): 
        self.label = "" if (label in ["",None]) else ("_"+label)
        self.vars = ("pt","eta","phi","mass","btagCSV")
        if "jetReCleanerHelper.cc_cc.so" not in ROOT.gSystem.GetLibraries():
            print "Load C++ Worker"
            ROOT.gROOT.ProcessLine(".L %s/src/CMGTools/DPS13TeV/python/postprocessing/helpers/jetReCleanerHelper.cc+" % os.environ['CMSSW_BASE'])
        self._worker = ROOT.JetReCleanerHelper(0.4)
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.initReaders(inputTree) # initReaders must be called in beginFile
        self.out = wrappedOutputTree
        self.out.branch("nJet"+self.label, "I")
        for V in self.vars:
            self.out.branch("Jet"+self.label+"_"+V, "F", lenVar="nJet"+self.label)
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def initReaders(self,tree): # this function gets the pointers to Value and ArrayReaders and sets them in the C++ worker class
        for B in "nLepGood", "nJet": setattr(self, B, tree.valueReader(B))
        for B in "eta", "phi" : setattr(self,"LepGood_"+B, tree.arrayReader("LepGood_"+B))
        for B in "eta", "phi" , "pt": setattr(self,"Jet_"+B, tree.arrayReader("Jet_"+B))
        self._worker.setLeptons(self.nLepGood,self.LepGood_eta,self.LepGood_phi)
        self._worker.setJets(self.nJet,self.Jet_eta,self.Jet_phi,self.Jet_pt)
        for v in self.vars:
            if not hasattr(self,"Jet_"+v): setattr(self,"Jet_"+v, tree.arrayReader("Jet_"+v))
        self._ttreereaderversion = tree._ttreereaderversion # self._ttreereaderversion must be set AFTER all calls to tree.valueReader or tree.arrayReader

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        ret={}
        jets = Collection(event,"Jet")
        #jets = filter(self.jetSel, Collection(event, "Jet"))
        
        for V in self.vars:
            branch = getattr(self, "Jet_"+V)
            ret["Jet"+self.label+"_"+V] = [getattr(j,V) for j in jets]
        if event._tree._ttreereaderversion > self._ttreereaderversion: # do this check at every event, as other modules might have read further branches
            self.initReaders(event._tree)
        # do NOT access other branches in python between the check/call to initReaders and the call to C++ worker code
        ## Algo
        cleanJets = self._worker.run()
        ## Output
        self.out.fillBranch('nJet'+self.label, len(cleanJets))
        for V in self.vars:
            self.out.fillBranch("Jet"+self.label+"_"+V, [ ret["Jet"+self.label+"_"+V][j] for j in cleanJets ])
        return True

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

jetReCleaner = lambda : JetReCleaner(label="Clean")
