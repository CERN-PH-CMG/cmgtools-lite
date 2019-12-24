from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection as NanoAODCollection
from CMGTools.TTHAnalysis.tools.nanoAOD.friendVariableProducerTools import declareOutput, writeOutput
from CMGTools.TTHAnalysis.treeReAnalyzer import Collection as CMGCollection
 
from CMGTools.TTHAnalysis.tools.mvaTool import *
import itertools
import copy
import math
import os

class BDT_eventReco(Module): # has to run on a recleaner with label _Recl
    def __init__(self, weightfile_bloose, weightfile_btight, weightfile_hj, weightfile_hjj, weightfile_rTT, weightfile_httTT, kinfitfile_httTT, algostring, csv_looseWP, csv_mediumWP, recllabel='Recl', selection = [], variations=[]):

        self.inputlabel = '_'+recllabel
        self.systsJEC = {0:"", 1:"_jesTotalCorrUp", -1:"_jesTotalCorrDown", 2:"_jesTotalUnCorrUp", -2:"_jesTotalUnCorrDown", 3 : '_jerUp', -3:'_jerDown'}
        if len(variations):
            self.systsJEC = {0:""}
            for i,var in enumerate(variations):
                self.systsJEC[i+1]   ="_%sUp"%var
                self.systsJEC[-(i+1)]="_%sDown"%var
        self.selection = selection

        if "/libCommonToolsMVAUtils.so" not in ROOT.gSystem.GetLibraries():
            ROOT.gSystem.Load("libCommonToolsMVAUtils")

        if "/BDT_eventReco_legacy_C.so" not in ROOT.gSystem.GetLibraries():
            if "/libCommonToolsMVAUtils.so" not in ROOT.gSystem.GetLibraries(): raise RuntimeError
            ROOT.gSystem.AddIncludePath(" -I/cvmfs/cms.cern.ch/slc7_amd64_gcc700/external/gsl/2.2.1-omkpbe2/include ")
            ROOT.gSystem.AddLinkedLibs(" -L//cvmfs/cms.cern.ch/slc7_amd64_gcc700/external/gsl/2.2.1-omkpbe2/lib -lgsl -lgslcblas -lm ");
            ROOT.gSystem.CompileMacro("%s/src/CMGTools/TTHAnalysis/macros/finalMVA/BDT_eventReco_legacy.C" % os.environ['CMSSW_BASE'],"kO");

        algo = getattr(ROOT,algostring)
        hj2017 = ("2017" in weightfile_hj)
        hjLegacy = ("legacy" in weightfile_hj)

        self.run = ROOT.BDT_EventReco(weightfile_bloose,weightfile_btight,weightfile_hj,hj2017,hjLegacy,weightfile_hjj,weightfile_rTT,weightfile_httTT,kinfitfile_httTT,algo,csv_looseWP,csv_mediumWP)
        self.run.setDebug(False)

        if algo==ROOT.k_BDTv8_Hj:
            self.branches = [
                "mvaValue",
                "bJet_fromLepTop_CSV",
                "bJet_fromHadTop_CSV",
                "HadTop_pT",
                "W_fromHadTop_mass",
                "HadTop_mass",
                "lep_ptRatio_fromTop_fromHig",
                "dR_lep_fromTop_bJet_fromLepTop",
                "dR_lep_fromTop_bJet_fromHadTop",
                "dR_lep_fromHig_bJet_fromLepTop",
                "LepTop_mass",
                "X_mass",
                "HadTop_eta",
                "HadTop_phi",
                "LepTop_pT",
                "LepTop_eta",
                "LepTop_phi",
                "X_pt",
                "X_eta",
                "X_phi",
                ]
            self.prefix = 'v8'
        elif algo==ROOT.k_rTT_Hj:
            self.branches = [
                "mvaValue",
                "HadTop_pt",
                "HadTop_eta",
                "HadTop_phi",
                "HadTop_mass",
                "W_fromHadTop_pt",
                "W_fromHadTop_eta",
                "W_fromHadTop_phi",
                "W_fromHadTop_mass",
                "W_fromHadTop_maxDeepCSVjj",
                "W_fromHadTop_dRjj",
                "W_fromHadTop_dRb",
                "b_fromHadTop_DeepCSV",
                "iJetSel1",
                "iJetSel2",
                "iJetSel3",
                ]
            self.prefix = 'rTT'
        elif algo==ROOT.k_httTT_Hj:
            self.branches = [
                "mvaValue",
                "HadTop_pt",
                "HadTop_mass",
                "iJetSel1",
                "iJetSel2",
                "iJetSel3",
                ]
            self.prefix='httTT'
        else:
            raise RuntimeError
        self.branches += [
            "Hj_score",
            "Hjj_score",
            "H_Wmass",
            "H_mass",
            ]
        self.outbranches = [ "BDT%s_eventReco_%s"%(self.prefix,k)+self.systsJEC[var] for k in self.branches for var in self.systsJEC ]

    # old interface
    def listBranches(self):
        return self.outbranches
    def __call__(self,event):
        return self.runIt(event, CMGCollection)
    
    # new interface
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        declareOutput(self,wrappedOutputTree, self.outbranches)

    def analyze(self, event):
        writeOutput(self, self.runIt(event, NanoAODCollection))
        return True

    # code
    def runIt(self,event, Collection):
        out = {}

        all_leps = [l for l in Collection(event,"LepGood","nLepGood")]
        nFO = getattr(event,"nLepFO"+self.inputlabel)
        chosen = getattr(event,"iLepFO"+self.inputlabel)
        leps = [all_leps[chosen[i]] for i in xrange(nFO)]
        for var in self.systsJEC:
            _var = var
            if not hasattr(event,"nJet25"+self.systsJEC[var]+self.inputlabel): _var = 0
            jets = [j for j in Collection(event,"JetSel"+self.inputlabel,"nJetSel"+self.inputlabel)]

            jetptcut = 25
            jets = filter(lambda x : getattr(x, 'pt%s'%self.systsJEC[_var]) > jetptcut, jets)

            res = [-100]*len(self.branches)

            good = True
            for sel in self.selection:
                if not sel(leps,jets,event):
                    good = False
                    break

            if good:
                self.run.clear()
                for i,j in enumerate(jets): self.run.addJet(getattr(j,'pt%s'%self.systsJEC[_var]),j.eta,j.phi,j.mass,0,j.btagDeepB, j.btagDeepFlavB,0,0,0,0,0,j.qgl)
                for l in leps: self.run.addLep(l.conePt,l.eta,l.phi,l.mass)
                res = self.run.EvalMVA()
            for i,x in enumerate(res): out["BDT%s_eventReco_%s"%(self.prefix,self.branches[i])+self.systsJEC[var]] = res[i]
        return out


if __name__ == '__main__':
    from sys import argv
    file = ROOT.TFile(argv[1])
    tree = file.Get("tree")
    tree.vectorTree = True
    tree.AddFriend("sf/t",argv[2]) # recleaner
              
    class Tester(Module):
        def __init__(self, name):
            Module.__init__(self,name,None)
            self.sf = BDT_eventReco(weightfile_bloose = '../../data/kinMVA/tth/TMVAClassification_bloose_BDTG.weights.xml',
                                    weightfile_btight = '../../data/kinMVA/tth/TMVAClassification_btight_BDTG.weights.xml',
                                    weightfile_hj = '../../data/kinMVA/tth/Hj_2017_configA_dcsv_BDTG.weights.xml',
                                    weightfile_hjj = '../../data/kinMVA/tth/Hjj_csv_BDTG.weights.xml',
                                    weightfile_rTT = '../../data/kinMVA/tth/resTop_xgb_csv_order_deepCTag.xml.gz',
                                    weightfile_httTT = '../../data/kinMVA/tth/HadTopTagger_resolved_XGB_CSV_sort_withKinFit.xml',
                                    kinfitfile_httTT = '../../data/kinMVA/tth/TF_jets_kinfit_httTT.root',
                                    algostring = 'k_rTT_Hj',
                                    csv_looseWP = 0.5426,
                                    csv_mediumWP = 0.8484,
                                    selection = [ lambda leps,jets,event : len(leps)>=2 and len(jets)>=3,
                                                  lambda leps,jets,event : leps[0].conePt>20 and leps[1].conePt>10,],
                                    )
        def analyze(self,ev):
            print "\nrun %6d lumi %4d event %d: leps %d, jets %d" % (ev.run, ev.lumi, ev.evt, ev.nLepGood, getattr(ev,'nJetSel'+self.sf.inputlabel))
            print sorted(self.sf(ev).iteritems())
    el = EventLoop([ Tester("tester") ])
    el.loop([tree], maxEvents = 3)

