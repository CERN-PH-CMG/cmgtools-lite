from CMGTools.TTHAnalysis.treeReAnalyzer2 import Object
from PhysicsTools.HeppyCore.utils.deltar import matchObjectCollection3
import ROOT, os

class MatchRecoToPartonsTTH_MyObjectProxy:
    def __init__(self,event,prefix,index=None):
        self.obj = Object(event,prefix,index)
    def __getitem__(self,attr):
        return self.__getattr__(attr)
    def __getattr__(self,name):
        if name=='eta': return self.eta_
        elif name=='phi': return self.phi_
        else: return getattr(self.obj,name)
    def eta_(self):
        return self.obj.eta
    def phi_(self):
        return self.obj.phi

class MatchRecoToPartonsTTH:
    def __init__(self,label="_Recl"):
        self.label = label
        self.branches = []
        self.branches +=  [ ("nLepGood", "I"), ("LepGood_matchedGenPart", "I", 20, "nLepGood") ]
        self.branches +=  [ ("nJetSel"+self.label, "I"), ("JetSel"+self.label+"_matchedGenPart", "I", 20, "nJetSel"+self.label) ]
        self.branches +=  [ ("nGenPart", "I"), ("GenPart_matchedLepGood", "I", 50, "nGenPart"), ("GenPart_matchedJetSel", "I", 50, "nGenPart") ]
    def listBranches(self):
        return self.branches
    def __call__(self,event):

        nleps = getattr(event,"nLepGood")
        nFO = getattr(event,"nLepFO"+self.label)
        chosen = getattr(event,"iLepFO"+self.label)
        leps = [MatchRecoToPartonsTTH_MyObjectProxy(event,"LepGood",i) for i in xrange(nleps)]
        lepsFO = [leps[chosen[i]] for i in xrange(nFO)]
        reco = [MatchRecoToPartonsTTH_MyObjectProxy(event,"JetSel"+self.label,i) for i in xrange(getattr(event,"nJetSel"+self.label))]
        gen = [MatchRecoToPartonsTTH_MyObjectProxy(event,"GenPart",i) for i in xrange(getattr(event,'nGenPart'))]
        ngenfinal = getattr(event,"nallFinalParton")
        igenfinal = getattr(event,"iallFinalParton")
        genfinal = [gen[igenfinal[i]] for i in xrange(ngenfinal)]

        pairs = matchObjectCollection3(lepsFO+reco,genfinal)

        mLeps = [-1]*len(leps)
        mReco = [-1]*len(reco)
        mPartLeps = [-1]*len(gen)
        mPart = [-1]*len(gen)
        for ij,j in enumerate(leps):
            if j not in lepsFO: continue
            mp = pairs[j]
            if mp:
                gind = gen.index(mp)
                mLeps[ij] = gind
                mPartLeps[gind] = ij
        for ij,j in enumerate(reco):
            mp = pairs[j]
            if mp:
                gind = gen.index(mp)
                mReco[ij] = gind
                mPart[gind] = ij
        ret = {}
        ret["nLepGood"] = len(leps)
        ret["nJetSel"+self.label] = len(reco)
        ret["nGenPart"] = len(gen)
        ret["LepGood_matchedGenPart"] = mLeps
        ret["JetSel"+self.label+"_matchedGenPart"] = mReco
        ret['GenPart_matchedLepGood'] = mPartLeps
        ret['GenPart_matchedJetSel'] = mPart
        return ret
