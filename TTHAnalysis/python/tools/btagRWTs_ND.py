#!/usr/bin/env python
from CMGTools.TTHAnalysis.treeReAnalyzer import ROOT, EventLoop, Module, Collection
from PhysicsTools.Heppy.physicsutils.BTagWeightCalculator import BTagWeightCalculator
import os.path, types
from array import array
from math import log, exp 
            
BTagReweight74X = lambda : BTagWeightCalculator("$CMSSW_BASE/src/CMGTools/TTHAnalysis/data/btag/csv_rwt_fit_hf_2015_11_20.root",
                                                "$CMSSW_BASE/src/CMGTools/TTHAnalysis/data/btag/csv_rwt_fit_lf_2015_11_20.root")
class BTagReweightFriend:
    def __init__(self,reweight,jets=["Jet","DiscJet"],inlabel="btagCSV",outlabel="btagCSVWeight",rwtKind='final',rwtSyst='nominal',maxjets=20,mcOnly=True):
        self.jets = jets
        self.label = outlabel
        self.blabel = inlabel
        self.maxJets = maxjets
        self.mcOnly = mcOnly
        self._reweight = (reweight() if type(reweight) == types.FunctionType else reweight)
        self._reweight.btag = inlabel
        self.rwtKind = rwtKind
        self.rwtSyst = rwtSyst
    def listBranches(self):
        out = []
        for ob in self.jets: out.extend([("n"+ob,"I"), (ob+"_"+self.label,"F",self.maxJets,"n"+ob)])
        return out
    def __call__(self,event):
        ret = {}
        for ob in self.jets:
            jets = Collection(event,ob)
            ret['n%s'%ob] = len(jets)
            ret[ob+"_"+self.label] = [ self.reweight(event,j) for j in jets ] 
        return ret
    def reweight(self,event,jet):
        if self.mcOnly and event.isData: return -99.0
        return self._reweight.calcJetWeight(jet, self.rwtKind, self.rwtSyst)

class BTagLeptonReweightFriend(BTagReweightFriend):
    def __init__(self,reweight,jets=["LepGood"],inlabel="jetBTagCSV",outlabel="jetBTagCSVWeight",rwtKind='final',rwtSyst='nominal',maxjets=20):
        BTagReweightFriend.__init__(self,reweight,jets=jets,inlabel=inlabel,outlabel=outlabel,rwtKind=rwtKind,rwtSyst=rwtSyst,maxjets=maxjets,mcOnly=True)
    def reweight(self,event,lep):
        if self.mcOnly and event.isData: return -99.0
        fl = abs(lep.mcMatchAny)
        if fl not in (4,5): fl = 1
        jetpt = lep.pt/lep.jetPtRatiov2
        return self._reweight.calcJetWeightImpl(jetpt, abs(lep.eta), fl, getattr(lep,self.blabel), self.rwtKind, self.rwtSyst)
    
if __name__ == '__main__':
    from sys import argv
    file = ROOT.TFile(argv[1])
    tree = file.Get("tree")
    tree.vectorTree = True
    class Tester(Module):
        def __init__(self, name):
            Module.__init__(self,name,None)
            self.sf = BTagReweightFriend(BTagReweight74X)
            self.sl = BTagLeptonReweightFriend(BTagReweight74X)
            self._wps = [ 0.605, 0.89, 0.97 ]
            self._pcountA = [0,0]
            self._pcount0 = [0 for w in self._wps]
            self._pcount1 = [0 for w in self._wps]
        def analyze(self,ev):
            print "\nrun %6d lumi %4d event %d: jets %d" % (ev.run, ev.lumi, ev.evt, ev.nJet25)
            ret = self.sf(ev)["Jet_btagCSVWeight"]
            lrt = self.sl(ev)["LepGood_jetBTagCSVWeight"]
            jets = Collection(ev,"Jet")
            leps = Collection(ev,"LepGood")
            for i,j in enumerate(jets):
                print "\tjet %8.2f %+5.2f %+3d %.3f -> %.3f " % (j.pt, j.eta, j.mcFlavour, min(max(0, j.btagCSV), 1), ret[i])
                if j.pt > 30 and abs(j.eta) < 2.4 and abs(j.mcFlavour) == 5:
                    self._pcountA[0] += 1.
                    self._pcountA[1] += ret[i]
                    for iw,w in enumerate(self._wps):
                        if j.btagCSV > w: 
                            self._pcount0[iw] += 1
                            self._pcount1[iw] += ret[i]
            for i,j in enumerate(leps):
                print "\tlep %8.2f %+5.2f %+3d %.3f -> %.3f " % (j.pt, j.eta, j.mcMatchAny, min(max(0, j.jetBTagCSV), 1), lrt[i])
            print ""
        def done(self):
            for iw,w in enumerate(self._wps):
                print " for WP %.3f, eff(pre) = %.3f, eff(post) = %.3f, SF = %.3f " % (w, self._pcount0[iw]/self._pcountA[0], self._pcount1[iw]/self._pcountA[1], self._pcount1[iw]/self._pcount0[iw]/self._pcountA[1]*self._pcountA[0])
    T = Tester("tester")
    el = EventLoop([ T ])
    el.loop([tree], maxEvents = 50)  
    T.done()
