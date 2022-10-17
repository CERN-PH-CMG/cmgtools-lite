from CMGTools.TTHAnalysis.treeReAnalyzer import *
import os, math

class BDT_resolvedTopTagger: # has to run on a recleaner with label _Recl
    def __init__(self, weightfile, recllabel='Recl', selection = []):

        self.inputlabel = '_'+recllabel
        self.systsJEC = {0:"", 1:"_jecUp", -1:"_jecDown"}
        self.selection = selection

        if "/libCommonToolsUtils.so" not in ROOT.gSystem.GetLibraries():
            ROOT.gSystem.Load("libCommonToolsUtils")

        if "/BDT_resolvedTopTagger_C.so" not in ROOT.gSystem.GetLibraries():
            if "/libCommonToolsUtils.so" not in ROOT.gSystem.GetLibraries(): raise RuntimeError
            ROOT.gSystem.CompileMacro("%s/src/CMGTools/TTHAnalysis/macros/finalMVA/BDT_resolvedTopTagger.C" % os.environ['CMSSW_BASE'],"kO");

        self.run = ROOT.BDT_resolvedTopTagger(weightfile)

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
            "j1",
            "j2",
            "j3",
            ]

    def listBranches(self):
        return [ "BDT_resolvedTopTagger_%s"%k+self.systsJEC[var] for k in self.branches for var in self.systsJEC ]

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
                for i,j in enumerate(jets): self.run.addJet(j.pt*jetcorr[i],j.eta,j.phi,j.mass,j.btagDeepCSV,j.btagDeepCSVCvsL,j.btagDeepCSVCvsB,j.ptd,j.axis1,j.mult)
                res = self.run.EvalMVA()

            for i,x in enumerate(res): out["BDT_resolvedTopTagger_%s"%self.branches[i]+self.systsJEC[var]] = res[i]

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
            self.sf = BDT_resolvedTopTagger('/data/peruzzi/resTop_xgb_csv_order_deepCTag.xml',#'../../data/kinMVA/tth/resTop_xgb_csv_order_deepCTag.xml.gz',
                                            selection = [ lambda leps,jets,event : len(leps)>=2 and len(jets)>=3,
                                                  lambda leps,jets,event : leps[0].conePt>20 and leps[1].conePt>10,])
        def analyze(self,ev):
            print "\nrun %6d lumi %4d event %d: leps %d, jets %d" % (ev.run, ev.lumi, ev.evt, ev.nLepGood, getattr(ev,'nJetSel'+self.sf.inputlabel))
            print sorted(self.sf(ev).iteritems())
    el = EventLoop([ Tester("tester") ])
    el.loop([tree], maxEvents = 3)
