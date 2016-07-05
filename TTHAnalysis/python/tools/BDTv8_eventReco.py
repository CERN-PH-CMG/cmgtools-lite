from CMGTools.TTHAnalysis.treeReAnalyzer import *
from CMGTools.TTHAnalysis.tools.mvaTool import *
import itertools
import copy
import math

class BDTv8_eventReco: # has to run on a recleaner with label _Recl
    def __init__(self, weightfile, recllabel='Recl'):
        self._MVAs = {}
        self.inputlabel = '_'+recllabel
        self.systsJEC = {0:"", 1:"_jecUp", -1:"_jecDown"}

        self.vars = [
            MVAVar("bJet_fromLepTop_CSV", func = lambda ev : ev["bJet_fromLepTop_CSV"]),
            MVAVar("bJet_fromHadTop_CSV", func = lambda ev : ev["bJet_fromHadTop_CSV"]),
            MVAVar("qJet1_fromW_fromHadTop_CSV", func = lambda ev : ev["qJet1_fromW_fromHadTop_CSV"]),
            MVAVar("HadTop_pT", func = lambda ev : ev["HadTop_pT"]),
            MVAVar("W_fromHadTop_mass", func = lambda ev : ev["W_fromHadTop_mass"]),
            MVAVar("HadTop_mass", func = lambda ev : ev["HadTop_mass"]),
            MVAVar("W_fromHiggs_mass", func = lambda ev : ev["W_fromHiggs_mass"]),
            MVAVar("LepTop_HadTop_dR", func = lambda ev : ev["LepTop_HadTop_dR"]),
            ]

        self.MVA = MVATool("BDTv8_eventReco", weightfile, self.vars)
        self.branches = [x.name for x in self.vars] + ["mvaValue"]

    def listBranches(self):
        return [ "BDTv8_eventReco_%s"%k+self.systsJEC[var] for k in self.branches for var in self.systsJEC ]
    def getp4(self,obj):
        if not obj: return ROOT.TLorentzVector(0,0,0,0)
        return obj.p4()
    def getp4lep(self,obj):
        if not obj: return ROOT.TLorentzVector(0,0,0,0)
        p4 = ROOT.TLorentzVector()
        p4.SetPtEtaPhiM(obj.conePt,obj.eta,obj.phi,obj.mass)
        return p4
    def getbtag(self,obj):
        if not obj: return -0.2
        return max(-0.1,obj.btagCSV)

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

            max_mva_value = -99
            best_permutation = None

            _jets = range(len(jets))
            if len(jets)<8: _jets.extend([-1]*3)
            elif len(jets)==8: _jets.extend([-1]*2)
            else: _jets.extend([-1])
            _leps = range(len(leps))

            permutations_leps = [x for x in itertools.permutations(_leps,2)]
            permutations_jets = set()
            if len(permutations_leps)>0:
                for x in itertools.permutations(_jets,6):
                    permutations_jets.add(x)

            permutations_jets = set(permutations_jets) # remove duplicates from null jets
            _permutations_jets = set()
            for x in permutations_jets:
                _x = list(x); _x[2]=x[3]; _x[3]=x[2];
                _permutations_jets.add(tuple(_x))
            permutations_jets = _permutations_jets # remove duplicates from W hadTop assignment
            _permutations_jets = set()
            for x in permutations_jets:
                _x = list(x); _x[4]=x[5]; _x[5]=x[4]; # remove duplicates from W Higgs assignment
                _permutations_jets.add(tuple(_x))
            permutations_jets = _permutations_jets

            nperm = 0
            nperm_full = 0

            for permleps in permutations_leps:
                for permjets in permutations_jets:

                    nperm += 1

                    bjet_fromHadTop = jets[permjets[0]] if permjets[0]>=0 else None
                    bjet_fromLepTop = jets[permjets[1]] if permjets[1]>=0 else None
                    wjet1_fromHadTop = jets[permjets[2]] if permjets[2]>=0 else None # careful, unordered
                    wjet2_fromHadTop = jets[permjets[3]] if permjets[3]>=0 else None # careful, unordered

                    btags = (self.getbtag(bjet_fromHadTop),self.getbtag(bjet_fromLepTop))
                    if max(btags)<0.80 and min(btags)<0.46: continue

                    hadTop_W = self.getp4(wjet1_fromHadTop)+self.getp4(wjet2_fromHadTop)
                    hadTop = hadTop_W + self.getp4(bjet_fromHadTop)

                    if hadTop_W.M() > 120: continue
                    if hadTop.M() > 220: continue

                    wjet1_fromHiggs = jets[permjets[4]] if permjets[4]>=0 else None # careful, unordered
                    wjet2_fromHiggs = jets[permjets[5]] if permjets[5]>=0 else None # careful, unordered

                    higgs_W = self.getp4(wjet1_fromHiggs) + self.getp4(wjet2_fromHiggs)

                    lep_fromTop = leps[permleps[0]]
#                    lep_fromHiggs = leps[permleps[1]]

                    lepTop = self.getp4lep(lep_fromTop) + self.getp4(bjet_fromLepTop)
#                    higgs = higgs_W + self.getp4lep(lep_fromHiggs)

                    if lepTop.M() > 180: continue
#                    if higgs.M() > 130: continue

                    nperm_full += 1

                    my_inputs = {}
                    my_inputs["bJet_fromLepTop_CSV"] = self.getbtag(bjet_fromLepTop)
                    my_inputs["bJet_fromHadTop_CSV"] = self.getbtag(bjet_fromHadTop)
                    my_inputs["qJet1_fromW_fromHadTop_CSV"] = self.getbtag(wjet1_fromHadTop)
                    my_inputs["HadTop_pT"] = hadTop.Pt()
                    my_inputs["W_fromHadTop_mass"] = hadTop_W.M()
                    my_inputs["HadTop_mass"] = hadTop.M()
                    my_inputs["W_fromHiggs_mass"] = higgs_W.M()
                    my_inputs["LepTop_HadTop_dR"] = deltaR(lepTop.Eta(),lepTop.Phi(),hadTop.Eta(),hadTop.Phi()) if hadTop.Pt()>0 else -1
                    
                    mva_value = self.MVA(my_inputs)
                    if mva_value>max_mva_value:
                        max_mva_value = mva_value
                        best_permutation = copy.copy(my_inputs)

                    my_inputs["qJet1_fromW_fromHadTop_CSV"] = self.getbtag(wjet2_fromHadTop)
                    mva_value = self.MVA(my_inputs)
                    if mva_value>max_mva_value:
                        max_mva_value = mva_value
                        best_permutation = copy.copy(my_inputs)

            out["BDTv8_eventReco_mvaValue"+self.systsJEC[var]] = max_mva_value
            for k in self.branches:
                if k=='mvaValue': continue
                out["BDTv8_eventReco_%s"%k+self.systsJEC[var]] = best_permutation[k] if best_permutation else -99

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
    el.loop([tree], maxEvents = 5)

