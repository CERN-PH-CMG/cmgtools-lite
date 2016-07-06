from CMGTools.TTHAnalysis.treeReAnalyzer import *
from CMGTools.TTHAnalysis.tools.mvaTool import *
import itertools
import copy
import math

class BDTv8_eventReco: # has to run on a recleaner with label _Recl
    def __init__(self, weightfile, recllabel='Recl', selection = []):

        self.inputlabel = '_'+recllabel
        self.systsJEC = {0:"", 1:"_jecUp", -1:"_jecDown"}
        self.selection = selection

        if "/BDTv8_eventReco_C.so" not in ROOT.gSystem.GetLibraries():
            ROOT.gSystem.CompileMacro("%s/src/CMGTools/TTHAnalysis/macros/leptons/BDTv8_eventReco.C" % os.environ['CMSSW_BASE'],"kO");

        self.run = ROOT.BDTv8_eventReco(weightfile)

        self.branches = [
            "mvaValue",
            "bJet_fromLepTop_CSV",
            "bJet_fromHadTop_CSV",
            "qJet1_fromW_fromHadTop_CSV",
            "HadTop_pT",
            "W_fromHadTop_mass",
            "HadTop_mass",
            "W_fromHiggs_mass",
            "LepTop_HadTop_dR",
            ]

    def listBranches(self):
        return [ "BDTv8_eventReco_%s"%k+self.systsJEC[var] for k in self.branches for var in self.systsJEC ]

    def __call__(self,event):
        out = {}

        all_leps = [l for l in Collection(event,"LepGood","nLepGood")]
        nFO = getattr(event,"nLepFO"+self.inputlabel)
        chosen = getattr(event,"iF"+self.inputlabel)
        leps = [all_leps[chosen[i]] for i in xrange(nFO)]

        for var in self.systsJEC:
            _var = var
            if not hasattr(event,"nJet"+self.systsJEC[var]): _var = 0
            jetsc = [j for j in Collection(event,"Jet"+self.systsJEC[_var],"nJet"+self.systsJEC[_var])]
            jetsd = [j for j in Collection(event,"DiscJet"+self.systsJEC[_var],"nDiscJet"+self.systsJEC[_var])]
            _ijets_list = getattr(event,"iJSel"+self.inputlabel+self.systsJEC[_var])
            _ijets = [ij for ij in _ijets_list]
            jets = [ (jetsc[ij] if ij>=0 else jetsd[-ij-1]) for ij in _ijets]


            res = [-100]*len(self.branches)

            good = True
            for sel in self.selection:
                if not sel(leps,jets,event):
                    good = False
                    break

            if good:
                self.run.clear()
                for j in jets: self.run.addJet(j.pt,j.eta,j.phi,j.mass,j.btagCSV)
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
            self.sf = BDTv8_eventReco(weightfile = '../../data/kinMVA/tth/TMVAClassification_BDTG_slimmed_v8.weights.xml')
        def analyze(self,ev):
            print "\nrun %6d lumi %4d event %d: leps %d" % (ev.run, ev.lumi, ev.evt, ev.nLepGood)
            print self.sf(ev)
    el = EventLoop([ Tester("tester") ])
    el.loop([tree], maxEvents = 500)

