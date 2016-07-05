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

    def listBranches(self):
        return [ "BDTv8_eventReco"+self.systsJEC[var] for var in self.systsJEC ]
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

            _jets = []
            for j in jets: _jets.append(j)
            if len(jets)<8: _jets.extend([None]*3)
            elif len(jets)==8: _jets.extend([None]*2)
            else: _jets.extend([None])
            _leps = [None]*2
            for i,l in enumerate(_leps[:2]): _leps[i]=l

            print len(_leps), len(_jets), math.factorial(len(_jets))*math.factorial(len(_leps))

            nperm = 0
            nperm_full = 0
            for permleps in itertools.permutations(_leps):
                for permjets in itertools.permutations(_jets):

                    if len(_jets)<6 or len(_leps)<2: break

                    nperm += 1
                    if nperm%100000==0: print 'testing permutation %d' % nperm

                    bjet_fromHadTop = permjets[0]
                    bjet_fromLepTop = permjets[1]
                    wjet1_fromHadTop = permjets[2]
                    wjet2_fromHadTop = permjets[3]

                    btags = (self.getbtag(bjet_fromHadTop),self.getbtag(bjet_fromLepTop))
                    if max(btags)<0.80 and min(btags)<0.46: continue

                    hadTop_W = self.getp4(wjet1_fromHadTop)+self.getp4(wjet2_fromHadTop)
                    hadTop = hadTop_W + self.getp4(bjet_fromHadTop)

                    if hadTop_W.M() > 120: continue
                    if hadTop.M() > 220: continue

                    wjet1_fromHiggs = permjets[4]
                    wjet2_fromHiggs = permjets[5]

                    higgs_W = self.getp4(wjet1_fromHiggs) + self.getp4(wjet2_fromHiggs)
                    if higgs_W.M() > 120: continue

                    lep_fromTop = permleps[0]
#                    lep_fromHiggs = permleps[1]

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
                        best_permutation = [permjets[:],permleps[:],copy.copy(my_inputs)]

            print 'perms',nperm,nperm_full
            out["BDTv8_eventReco"+self.systsJEC[var]] = max_mva_value

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
    el.loop([tree], maxEvents = 50)

