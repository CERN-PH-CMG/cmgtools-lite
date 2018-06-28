import ROOT
import os
import numpy as np
ROOT.PyConfig.IgnoreCommandLineOptions = True

from CMGTools.DPS13TeV.postprocessing.framework.datamodel import Collection 
from CMGTools.DPS13TeV.postprocessing.framework.eventloop import Module

class lepSFProducer(Module):
    def __init__(self, muonSelectionTag, electronSelectionTag):
        if muonSelectionTag=="TightWP_2016":
            mu_f=["Mu_Trg.root","Mu_ID.root","Mu_Iso.root"]
            mu_h = ["IsoMu24_OR_IsoTkMu24_PtEtaBins/pt_abseta_ratio",
                    "MC_NUM_TightID_DEN_genTracks_PAR_pt_eta/pt_abseta_ratio",
                    "TightISO_TightID_pt_eta/pt_abseta_ratio"]
        elif muonSelectionTag=="TightMVAWP_2016":
            mu_f=["lepMVAEffSF_m_2lss.root"]
            mu_h = ["sf"]
        else:
            print "Not foreseen WP: ",muonSelectionTag
            mu_f  = []
            mu_h  = []
        if electronSelectionTag=="GPMVA90_2016":
            el_f = ["EGM2D_eleGSF.root","EGM2D_eleMVA90.root"]
            el_h = ["EGamma_SF2D", "EGamma_SF2D"]

        elif electronSelectionTag=="CutBasedTight_2016":
            el_f = ["EGM2D_eleGSF.root","EGM2D_eleCutBasedTightWP.root"]
            el_h = ["EGamma_SF2D", "EGamma_SF2D"]
                    
        elif electronSelectionTag=="CutBasedMedium_2016":
            el_f = ["EGM2D_eleGSF.root","EGM2D_eleCutBasedMediumWP.root"]
            el_h = ["EGamma_SF2D", "EGamma_SF2D"]
        
        elif electronSelectionTag=="TightMVAWP_2016":
            el_f = ["lepMVAEffSF_e_2lss.root"]
            el_h = ["sf"]
        else:
            print "Not foreseen WP: ",electronSelectionTag
            el_f = []
        #        el_h = ["EGamma_SF2D", "EGamma_SF2D"]
        mu_f = ["%s/src/CMGTools/DPS13TeV/python/postprocessing/data/leptonSF/" % os.environ['CMSSW_BASE'] + f for f in mu_f]
        el_f = ["%s/src/CMGTools/DPS13TeV/python/postprocessing/data/leptonSF/" % os.environ['CMSSW_BASE'] + f for f in el_f]

        self.mu_f = ROOT.std.vector(str)(len(mu_f))
        self.mu_h = ROOT.std.vector(str)(len(mu_f))
        for i in range(len(mu_f)): self.mu_f[i] = mu_f[i]; self.mu_h[i] = mu_h[i];
        self.el_f = ROOT.std.vector(str)(len(el_f))
        self.el_h = ROOT.std.vector(str)(len(el_f))
        for i in range(len(el_f)): self.el_f[i] = el_f[i]; self.el_h[i] = el_h[i];

        if "/LeptonEfficiencyCorrector_cc.so" not in ROOT.gSystem.GetLibraries():
            print "Load C++ Worker"
            ROOT.gROOT.ProcessLine(".L %s/src/CMGTools/DPS13TeV/python/postprocessing/helpers/LeptonEfficiencyCorrector.cc+" % os.environ['CMSSW_BASE'])
    def beginJob(self):
        self._worker_mu = ROOT.LeptonEfficiencyCorrector(self.mu_f,self.mu_h)
        self._worker_el = ROOT.LeptonEfficiencyCorrector(self.el_f,self.el_h)
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("LepGood_effSF", "F", lenVar="nLepGood")
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        leps = Collection(event, "LepGood")
        sf = []
        for l in leps:
            if event.isData:
                sf.append(1.)
            else:
                worker = self._worker_el if abs(l.pdgId)==11 else self._worker_mu
                sf.append(worker.getSF(l.pdgId,l.pt,l.eta))
                #print('check the leptons for {lep} with {PT}: {ETA}: is {SF}:'.format(lep=l.pdgId,PT=l.pt,ETA=l.eta,SF=sf))
        self.out.fillBranch("LepGood_effSF", sf)
        return True

class lepTrgSFProducer(Module):
    def __init__(self,dimensions=2,prefer1Dvar="eta",maxrun=278808):
        # from  https://indico.cern.ch/event/570616/contributions/2354285/attachments/1365274/2067939/tnpBuda_nov03_v1.pdf
        # should make the weighted average in the data chunk considered.
        # here take the last measurement, since similar
        self.versions = {(273158,274442): "v1",
                         (274954,275066): "v2",
                         (275067,275311): "v3",
                         (275319,276834): "v4",
                         (276870,278240): "v5",
                         (278273,280385): "v6",
                         (281639,283059): "v7"}
        self.maxrun = maxrun
        self.dim = dimensions
        self.var = prefer1Dvar
        if "/WeightCalculatorFromHistogram_cc.so" not in ROOT.gSystem.GetLibraries():
            print "Load C++ Worker"
            ROOT.gROOT.ProcessLine(".L %s/src/CMGTools/DPS13TeV/python/postprocessing/helpers/WeightCalculatorFromHistogram.cc+" % os.environ['CMSSW_BASE'])
    def beginJob(self):
        ver=None
        for k,v in self.versions.iteritems(): 
            if k[0] < self.maxrun < k[1]: ver = v
        if ver:
            f = "%s/src/CMGTools/DPS13TeV/python/postprocessing/data/leptonSF/el_trg/%s/%s/passHLT/eff1D.root" % (os.environ['CMSSW_BASE'],ver,self.var)
            h = "s1c_eff"
            if self.dim==2:
                f2D = "%s/src/CMGTools/DPS13TeV/python/postprocessing/data/leptonSF/el_trg/%s/sf/passHLT/eff2D.root" % (os.environ['CMSSW_BASE'],ver)
                if os.path.isfile(f2D):
                    f = f2D
                    h = "s2c_eff"
                else: self.dim = 1
        else: raise Exception('No suitable version of trigger scale factors found!')
        print "Reading trigger scale factors in %d dimensions from file %s..." % (self.dim,f)
        tf = ROOT.TFile.Open(f)
        th = tf.Get(h).Clone("sf_%s" % v)
        th.SetDirectory(None)
        self._worker = ROOT.WeightCalculatorFromHistogram(th)
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("LepGood_trgSF", "F", lenVar="nLepGood")
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        leps = Collection(event, "LepGood")
        sf = []
        for l in leps:
            if event.isData or abs(l.pdgId)!=11:
                sf.append(1.)
            else:
                if self.dim == 2:
                    wgt = self._worker.getWeight(l.pt,l.eta)
                    sf.append(wgt if wgt>0 else 1.)
                else:
                    sf.append(self._worker.getWeight(getattr(l,sef.var)))
        self.out.fillBranch("LepGood_trgSF", sf)
        return True

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

lepSF = lambda : lepSFProducer("TightMVAWP_2016","TightMVAWP_2016")
trgSF = lambda : lepTrgSFProducer()
