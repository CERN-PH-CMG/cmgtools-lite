from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection as NanoAODCollection
from CMGTools.TTHAnalysis.tools.nanoAOD.friendVariableProducerTools import declareOutput, writeOutput
from CMGTools.TTHAnalysis.treeReAnalyzer import Collection as CMGCollection


import ROOT, itertools

class HiggsRecoTTH(Module):
    def __init__(self,label="_Recl",cut_BDT_rTT_score = 0.0, cuts_mW_had = (50.,110.), cuts_mH_vis = (90.,130.), btagDeepCSVveto = 0.4941, doSystJEC=True):
        self.label = label
        self.branches = []
        self.systsJEC = {0:"", 1:"_jesTotalUp", -1:"_jesTotalDown"} if doSystJEC else {0:""}
        for var in self.systsJEC: self.branches.extend(["Hreco_%s%s"%(x,self.systsJEC[var]) for x in ["minDRlj","visHmass","Wmass","lepIdx","j1Idx","j2Idx"]])
        self.cut_BDT_rTT_score = cut_BDT_rTT_score
        self.cuts_mW_had = cuts_mW_had
        self.cuts_mH_vis = cuts_mH_vis
        self.btagDeepCSVveto = btagDeepCSVveto
    
    # old interface
    def listBranches(self):
        return self.branches
    def __call__(self,event):
        return self.run(event,CMGCollection)

    # new interface
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        declareOutput(self,wrappedOutputTree, self.branches)
    def analyze(self, event):
        writeOutput(self, self.run(event, NanoAODCollection))
        return True

    # code
    def run(self,event,Collection):
        
        nleps = getattr(event,"nLepGood")
        nFO = getattr(event,"nLepFO"+self.label)
        ileps = getattr(event,"iLepFO"+self.label)
        leps = Collection(event,"LepGood","nLepGood")
        lepsFO = [leps[ileps[i]] for i in xrange(nFO)]
        jets = [x for x in Collection(event,"JetSel"+self.label,"nJetSel"+self.label)]
        ret = {}        

        for var in self.systsJEC:
            score = getattr(event,"BDThttTT_eventReco_mvaValue%s"%self.systsJEC[var])
            
            candidates=[]
            
            if score>self.cut_BDT_rTT_score:

                j1top = getattr(event,"BDThttTT_eventReco_iJetSel1%s"%self.systsJEC[var])
                j2top = getattr(event,"BDThttTT_eventReco_iJetSel2%s"%self.systsJEC[var])
                j3top = getattr(event,"BDThttTT_eventReco_iJetSel3%s"%self.systsJEC[var])
                jetsNoTopNoB = [j for i,j in enumerate(jets) if i not in [j1top,j2top,j3top] and j.btagDeepB<self.btagDeepCSVveto]

                for _lep,lep in [(ix,x.p4()) for ix,x in enumerate(lepsFO)]:
                    for _j1,_j2,j1,j2 in [(jets.index(x1),jets.index(x2),x1.p4(),x2.p4()) for x1,x2 in itertools.combinations(jetsNoTopNoB,2)]:
                        j1.SetPtEtaPhiM(getattr(jets[jets.index(x1)],'pt%s'%self.systsJEC[var]),j1.Eta(), j1.Phi(), j1.M())
                        j2.SetPtEtaPhiM(getattr(jets[jets.index(x2)],'pt%s'%self.systsJEC[var]),j2.Eta(), j2.Phi(), j2.M())
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


            ret["Hreco_minDRlj%s" %self.systsJEC[var]] = best[0] if best else -99
            ret["Hreco_visHmass%s"%self.systsJEC[var]] = best[1] if best else -99
            ret["Hreco_Wmass%s"   %self.systsJEC[var]] = best[2] if best else -99
            ret["Hreco_lepIdx%s"  %self.systsJEC[var]] = best[3] if best else -99
            ret["Hreco_j1Idx%s"   %self.systsJEC[var]] = best[4] if best else -99
            ret["Hreco_j2Idx%s"   %self.systsJEC[var]] = best[5] if best else -99
        return ret
