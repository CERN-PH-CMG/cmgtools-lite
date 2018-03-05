import ROOT
import os
import numpy as np
ROOT.PyConfig.IgnoreCommandLineOptions = True

from CMGTools.WMass.postprocessing.framework.datamodel import Collection 
from CMGTools.WMass.postprocessing.framework.eventloop import Module

class puWeightProducer(Module):
    def __init__(self,myfile,targetfile,myhist="pu_mc",targethist="pileup",name="puWeight",norm=True,verbose=False,nvtx_var="nTrueInt"):
        self.myh = self.loadHisto(myfile,myhist)
        self.targeth = self.loadHisto(targetfile,targethist)
        self.name = name
        self.norm = norm
        self.verbose = verbose
        self.nvtxVar = nvtx_var
        self.fixLargeWeights = True
        if "/WeightCalculatorFromHistogram_cc.so" not in ROOT.gSystem.GetLibraries():
            print "Load C++ Worker"
            ROOT.gROOT.ProcessLine(".L %s/src/CMGTools/WMass/python/postprocessing/helpers/WeightCalculatorFromHistogram.cc+" % os.environ['CMSSW_BASE'])
    def loadHisto(self,filename,hname):
        tf = ROOT.TFile.Open(filename)
        tf.Print()
        hist = tf.Get(hname)
        hist.SetDirectory(None)
        tf.Close()
        return hist
    def beginJob(self):
        self._worker = ROOT.WeightCalculatorFromHistogram(self.myh,self.targeth,self.norm,self.fixLargeWeights,self.verbose)
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch(self.name, "F")
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        if hasattr(event,self.nvtxVar):
            nvtx = int(getattr(event,self.nvtxVar))
            weight = self._worker.getWeight(nvtx) if nvtx < self.myh.GetNbinsX() else 1
        else: weight = 1
        self.out.fillBranch(self.name,weight)
        return True

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

pufile_mc="%s/src/CMGTools/WMass/python/postprocessing/data/pileup/pileup_profile_Summer16.root" % os.environ['CMSSW_BASE']
pufile_data="%s/src/CMGTools/WMass/python/postprocessing/data/pileup/PileupData_GoldenJSON_Full2016.root" % os.environ['CMSSW_BASE']
pufile_data_2016BF="%s/src/CMGTools/WMass/python/postprocessing/data/pileup/PileupData_GoldenJSON_2016BF.root" % os.environ['CMSSW_BASE']
pufile_data_mc_2016G="%s/src/CMGTools/WMass/python/postprocessing/data/pileup/Pileup_Data2016G_MCSummer16MC.root" % os.environ['CMSSW_BASE']
puWeight = lambda : puWeightProducer(pufile_mc,pufile_data,"pu_mc","pileup",name="puw",verbose=True)
puWeight2016BF = lambda : puWeightProducer(pufile_mc,pufile_data_2016BF,"pu_mc","pileup",name="puwBF",verbose=True)
puWeight2016G =lambda : puWeightProducer(pufile_data_mc_2016G,pufile_data_mc_2016G,"pu_mc","pileup",name="puwG",verbose=True)
