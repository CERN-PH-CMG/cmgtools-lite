from CMGTools.TTHAnalysis.treeReAnalyzer import Collection
import ROOT, itertools

class BestHmm:
    def __init__(self,label="_Recl"):
        self.label = label
        self.branches = ["mH1mm",("mH1mmiLep1","I"),("mH1mmiLep2","I")]
    def listBranches(self):
        return self.branches
    def __call__(self,event):

        nleps = getattr(event,"nLepGood")
        nFO = getattr(event,"nLepFO"+self.label)
        ileps = getattr(event,"iLepFO"+self.label)
        leps = Collection(event,"LepGood","nLepGood")
        ilepsFO = [ileps[i] for i in xrange(nFO)]

        best_pair = None
        best_dm = 9e9
        best_m = -99

        for il1,il2 in itertools.combinations(ilepsFO,2):
            l1 = leps[il1]
            l2 = leps[il2]
            if l1.pdgId*l2.pdgId!=-169: continue
            m = (l1.p4()+l2.p4()).M()
            dm = abs(m-125)
            if dm < best_dm:
                best_dm = dm
                best_m = m
                best_pair = (il1,il2)

        ret = {}
        ret["mH1mm"] = best_m
        ret["mH1mmiLep1"] = best_pair[0] if best_pair else 0
        ret["mH1mmiLep2"] = best_pair[1] if best_pair else 0
        return ret
