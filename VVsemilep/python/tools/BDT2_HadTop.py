from CMGTools.TTHAnalysis.treeReAnalyzer import *
from CMGTools.TTHAnalysis.tools.mvaTool import *
import itertools

class BDT2_HadTop: # has to run on a recleaner with label _Recl
    def __init__(self, weightfile):
        self._MVAs = {}

        self.systsJEC = {0:"", 1:"_jecUp", -1:"_jecDown"}

        self.vars = [
            MVAVar("bJet_csv", func = lambda ev : ev["BDT2_bJet_csv"]),
            MVAVar("wJet1_csv", func = lambda ev : ev["BDT2_wJet1_csv"]),
            MVAVar("wJet2_csv", func = lambda ev : ev["BDT2_wJet2_csv"]),
            MVAVar("w_Mass", func = lambda ev : ev["BDT2_w_Mass"]),
            MVAVar("top_Mass", func = lambda ev : ev["BDT2_top_Mass"]),
            MVAVar("bJet_W_dR", func = lambda ev : ev["BDT2_bJet_W_dR"]),
            MVAVar("j_j_dR", func = lambda ev : ev["BDT2_j_j_dR"]),
            ]

        self.MVA = MVATool("BDT2", weightfile, self.vars)

    def listBranches(self):
        return [ "BDT2"+self.systsJEC[var] for var in self.systsJEC ]
    def __call__(self,event):
        out = {}

        for var in self.systsJEC:
            _var = var
            if not hasattr(event,"nJet"+self.systsJEC[var]): _var = 0
            jetsc = [j for j in Collection(event,"Jet"+self.systsJEC[_var],"nJet"+self.systsJEC[_var])]
            jetsd = [j for j in Collection(event,"DiscJet"+self.systsJEC[_var],"nDiscJet"+self.systsJEC[_var])]
            _ijets_list = getattr(event,"iJ"+self.systsJEC[_var]+"_Recl")
            _ijets = [ij for ij in _ijets_list]
            jets = [ (jetsc[ij] if ij>=0 else jetsd[-ij-1]) for ij in _ijets]

            max_mva_value = -99

            for j1,j2,j3 in itertools.permutations(jets,3):
                qq_vect = j2.p4()+j3.p4()
                t_vect = j1.p4()+qq_vect
                my_inputs = {}
                my_inputs["BDT2_bJet_csv"] = j1.btagCSV
                my_inputs["BDT2_wJet1_csv"] = j2.btagCSV
                my_inputs["BDT2_wJet2_csv"] = j3.btagCSV
                my_inputs["BDT2_w_Mass"] = qq_vect.M()
                my_inputs["BDT2_top_Mass"] = t_vect.M()
                my_inputs["BDT2_bJet_W_dR"] = qq_vect.DeltaR(j1.p4())
                my_inputs["BDT2_j_j_dR"] = j2.p4().DeltaR(j3.p4())
                max_mva_value = max(max_mva_value,self.MVA(my_inputs))

            out["BDT2"+self.systsJEC[var]] = max_mva_value

        return out


if __name__ == '__main__':
    from sys import argv
    file = ROOT.TFile(argv[1])
    tree = file.Get("treeProducerSusyMultilepton")
    file = ROOT.TFile(argv[1])
    tree = file.Get("tree")
    tree.vectorTree = True
    tree.AddFriend("sf/t",argv[2]) # recleaner
              
    class Tester(Module):
        def __init__(self, name):
            Module.__init__(self,name,None)
            self.sf = BDT2_HadTop(weightfile = '../../data/kinMVA/tth/TMVAClassification_BDTG.weights_BDT2.xml')
        def analyze(self,ev):
            print "\nrun %6d lumi %4d event %d: leps %d" % (ev.run, ev.lumi, ev.evt, ev.nLepGood)
            print self.sf(ev)
    el = EventLoop([ Tester("tester") ])
    el.loop([tree], maxEvents = 50)

