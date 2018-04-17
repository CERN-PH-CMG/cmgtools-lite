from CMGTools.TTHAnalysis.treeReAnalyzer import *
from CMGTools.TTHAnalysis.tools.mvaTool import *
import itertools
import copy
import math

class BDTv8_eventReco: # has to run on a recleaner with label _Recl
    def __init__(self, weightfile_bloose, weightfile_btight, weightfile_hj, weightfile_hjj, recllabel='Recl', selection = []):

        self.inputlabel = '_'+recllabel
        self.systsJEC = {0:"", 1:"_jecUp", -1:"_jecDown"}
        self.selection = selection

        if "/BDTv8_eventReco_C.so" not in ROOT.gSystem.GetLibraries():
            ROOT.gSystem.CompileMacro("%s/src/CMGTools/TTHAnalysis/macros/finalMVA/BDTv8_eventReco.C" % os.environ['CMSSW_BASE'],"kO");

        self.run = ROOT.BDTv8_eventReco(weightfile_bloose,weightfile_btight,weightfile_hj,weightfile_hjj)

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
            "Hj_score",
            "Hjj_score",
            "H_Wmass",
            "H_mass",
            ]

    def listBranches(self):
        return [ "BDTv8_eventReco_%s"%k+self.systsJEC[var] for k in self.branches for var in self.systsJEC ]

    def __call__(self,event):
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
            if (_var==0): jets = filter(lambda x : x.pt>jetptcut, jets)
            elif (_var==1): jets = filter(lambda x : x.pt*x.corr_JECUp/x.corr>jetptcut, jets)
            elif (_var==-1): jets = filter(lambda x : x.pt*x.corr_JECDown/x.corr>jetptcut, jets)

            if (_var==0): jetcorr = [1 for x in jets]
            elif (_var==1): jetcorr = [x.corr_JECUp/x.corr for x in jets]
            elif (_var==-1): jetcorr = [x.corr_JECDown/x.corr for x in jets]

            res = [-100]*len(self.branches)

            good = True
            for sel in self.selection:
                if not sel(leps,jets,event):
                    good = False
                    break

            if good:
                self.run.clear()
                for i,j in enumerate(jets): self.run.addJet(j.pt*jetcorr[i],j.eta,j.phi,j.mass,j.btagCSV,j.qgl)
                for l in leps: self.run.addLep(l.conePt,l.eta,l.phi,l.mass)
                res = self.run.EvalMVA()

            for i,x in enumerate(res): out["BDTv8_eventReco_%s"%self.branches[i]+self.systsJEC[var]] = res[i]

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
            self.sf = BDTv8_eventReco('../../data/kinMVA/tth/TMVAClassification_bloose_BDTG.weights.xml',
                                      '../../data/kinMVA/tth/TMVAClassification_btight_BDTG.weights.xml',
                                      '../../data/kinMVA/tth/Hj_csv_BDTG.weights.xml',
                                      '../../data/kinMVA/tth/Hjj_csv_BDTG.weights.xml',
                                      )
        def analyze(self,ev):
            print "\nrun %6d lumi %4d event %d: leps %d" % (ev.run, ev.lumi, ev.evt, ev.nLepGood)
            print self.sf(ev)
    el = EventLoop([ Tester("tester") ])
    el.loop([tree], maxEvents = 500)

