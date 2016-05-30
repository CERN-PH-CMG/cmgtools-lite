from CMGTools.TTHAnalysis.treeReAnalyzer import *
import ROOT

class EventBTagRWT:
    def __init__(self, label="", recllabel='Recl', suppressWarning=False):
        self.label = "" if (label in ["",None]) else ("_"+label)
        self.inputlabel = '_'+recllabel
        self.suppressWarning = suppressWarning
        self.systsJEC = {0:"", 1:"_jecUp", -1:"_jecDown"}
        self.systsBTAG = dict(enumerate(["", "_JESUp", "_JESDown", "_LFUp", "_LFDown", "_HFUp", "_HFDown", \
                                             "_HFStats1Up", "_HFStats1Down", "_HFStats2Up", "_HFStats2Down", \
                                             "_LFStats1Up", "_LFStats1Down", "_LFStats2Up", "_LFStats2Down", \
                                             "_cErr1Up", "_cErr1Down", "_cErr2Up", "_cErr2Down" ]))
    def listBranches(self):
        label = self.label
        biglist = []
        for key in self.systsJEC:
            for bkey in self.systsBTAG:
                thisvar = self.select_jec_btag_unc_combinations(key,bkey)
                if thisvar!=None:
                    biglist.extend([
                            ("eventBTagSF"+label+thisvar, "F")
                            ])
        return biglist


    def __call__(self,event):

        all_leps = [l for l in Collection(event,"LepGood","nLepGood")]
        nCleaning = getattr(event,"nLepCleaning"+self.inputlabel)
        chosen = getattr(event,"iC"+self.inputlabel)
        leps = [all_leps[chosen[i]] for i in xrange(nCleaning)]

        retwlabel = {};

        for var in self.systsJEC:
            _var = var
            if not hasattr(event,"nJet"+self.systsJEC[var]): _var = 0
            jetsc = [j for j in Collection(event,"Jet"+self.systsJEC[_var],"nJet"+self.systsJEC[_var])]
            jetsd = [j for j in Collection(event,"DiscJet"+self.systsJEC[_var],"nDiscJet"+self.systsJEC[_var])]
            _ijets_list = getattr(event,"iJ"+self.inputlabel+self.systsJEC[_var])
            _ijets = [ij for ij in _ijets_list]
            jets = [ (jetsc[ij] if ij>=0 else jetsd[-ij-1]) for ij in _ijets]
            for btagsyst in self.systsBTAG:
                thisvar = self.select_jec_btag_unc_combinations(var,btagsyst)
                if thisvar!=None:
                    retwlabel["eventBTagSF"+self.label+thisvar] = self.bTag_eventRWT_SF(event,leps,jets,self.systsBTAG[btagsyst])
                    if (not self.suppressWarning) and hasattr(event,"eventBTagSF"+self.inputlabel+thisvar):
                        if abs(retwlabel["eventBTagSF"+self.label+thisvar]-getattr(event,"eventBTagSF"+self.inputlabel+thisvar))>1e-4: print 'Difference from pre-calculated value:',retwlabel["eventBTagSF"+self.label+thisvar],getattr(event,"eventBTagSF"+self.inputlabel+thisvar)

        return retwlabel

    def bTag_eventRWT_SF(self,ev,leps,jets,systlabel):
        if ev.isData: return 1
        sf = 1
        for l in leps: sf = sf * getattr(l,"jetBTagCSVWeight"+systlabel)
        for j in jets: sf = sf * getattr(j,"btagCSVWeight"+systlabel)
        return sf
    def select_jec_btag_unc_combinations(self,jetunc,btagunc):
        if "JESUp" in self.systsBTAG[btagunc]: return "_jecUp" if self.systsJEC[jetunc]=="_jecUp" else None
        if "JESDown" in self.systsBTAG[btagunc]: return "_jecDown" if self.systsJEC[jetunc]=="_jecDown" else None
        return self.systsBTAG[btagunc]+self.systsJEC[jetunc] if self.systsJEC[jetunc]=="" else None

