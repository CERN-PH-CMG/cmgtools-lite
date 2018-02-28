from CMGTools.TTHAnalysis.treeReAnalyzer import Collection
import ROOT, itertools

class HiggsRecoTTH:
    def __init__(self,label="_Recl",cut_BDT_rTT_score = 0.0, cuts_mW_had = (50.,110.), cuts_mH_vis = (90.,130.), btagDeepCSVveto = 0.4941):
        self.label = label
        self.branches = ["Hreco_%s"%x for x in ["minDRlj","visHmass","Wmass","lepIdx","j1Idx","j2Idx"]]
        self.cut_BDT_rTT_score = cut_BDT_rTT_score
        self.cuts_mW_had = cuts_mW_had
        self.cuts_mH_vis = cuts_mH_vis
        self.btagDeepCSVveto = btagDeepCSVveto
    def listBranches(self):
        return self.branches
    def __call__(self,event):

        score = getattr(event,"BDT_resolvedTopTagger_mvaValue")

        candidates=[]

        if score>self.cut_BDT_rTT_score:

            nleps = getattr(event,"nLepGood")
            nFO = getattr(event,"nLepFO"+self.label)
            ileps = getattr(event,"iLepFO"+self.label)
            leps = Collection(event,"LepGood","nLepGood")
            lepsFO = [leps[ileps[i]] for i in xrange(nFO)]

            jets = [x for x in Collection(event,"JetSel"+self.label,"nJetSel"+self.label)]
            j1top = getattr(event,"BDT_resolvedTopTagger_j1")
            j2top = getattr(event,"BDT_resolvedTopTagger_j2")
            j3top = getattr(event,"BDT_resolvedTopTagger_j3")
            jetsNoTopNoB = [j for i,j in enumerate(jets) if i not in [j1top,j2top,j3top] and j.btagDeepCSV<self.btagDeepCSVveto]

            for _lep,lep in [(ix,x.p4()) for ix,x in enumerate(lepsFO)]:
                for _j1,_j2,j1,j2 in [(jets.index(x1),jets.index(x2),x1.p4(),x2.p4()) for x1,x2 in itertools.combinations(jetsNoTopNoB,2)]:
                    W = j1+j2
                    mW = W.M()
                    if mW<self.cuts_mW_had[0] or mW>self.cuts_mW_had[1]: continue
                    Wconstr = ROOT.TLorentzVector()
                    Wconstr.SetPtEtaPhiM(W.Pt(),W.Eta(),W.Phi(),80.4)
                    Hvisconstr = lep+Wconstr
                    mHvisconstr = Hvisconstr.M()
                    if mHvisconstr<self.cuts_mH_vis[0] or mHvisconstr>self.cuts_mH_vis[1]: continue
                    mindR = min(lep.DeltaR(j1),lep.DeltaR(j2))
                    candidates.append((mindR,mHvisconstr,mW,_lep,_j1,_j2))

        best = min(candidates) if len(candidates) else None

        ret = {}
        ret["Hreco_minDRlj"] = best[0] if best else -99
        ret["Hreco_visHmass"] = best[1] if best else -99
        ret["Hreco_Wmass"] = best[2] if best else -99
        ret["Hreco_lepIdx"] = best[3] if best else -99
        ret["Hreco_j1Idx"] = best[4] if best else -99
        ret["Hreco_j2Idx"] = best[5] if best else -99
        return ret
