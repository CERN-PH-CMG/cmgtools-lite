#!/usr/bin/env python
import os.path, types
from array import array
from math import log, exp

from CMGTools.TTHAnalysis.treeReAnalyzer import ROOT, EventLoop, Module, Collection
from BTagScaleFactors import BTagScaleFactors

class BTagSFReweightFriend:
    def __init__(self, sfreader,
                 jetlabel="Jet",
                 blabel="btagCSV",
                 label="eventBTagSF",
                 systs=["central"],
                 mcOnly=True):
        self.sfreader = sfreader

        self.jetlabel = jetlabel
        self.label = label
        self.blabel = blabel
        self.mcOnly = mcOnly

        self.systs = systs

    def listBranches(self):
        out = []
        for syst in self.systs:
            label = self.label
            if not syst == "central":
                label = "%s_%s" % (label, syst)
            out.append(label)

        return out

    def __call__(self, event):
        ret = {}
        jets = Collection(event, self.jetlabel)
        for syst in self.systs:
            label = self.label
            if not syst == "central":
                label = "%s_%s" % (label, syst)

            ret[label] = self.sfreader.get_event_SF(jets, syst=syst)

        return ret

# class BTagLeptonReweightFriend(BTagSFReweightFriend):
#     def __init__(self, reweight,
#                  jetlabel="LepGood",
#                  blabel="jetBTagCSV",
#                  label="jetBTagCSVWeight",
#                  rwtSyst="central"):
#         BTagSFReweightFriend.__init__(self, sfreader,
#                                       jetlabel=jetlabel,
#                                       blabel=blabel,
#                                       label=label,
#                                       rwtKind=rwtKind,
#                                       rwtSyst=rwtSyst,
#                                       mcOnly=True)



#     def reweight(self, event, lep):
#         if self.mcOnly and event.isData:
#             return -99.0
#         fl = abs(lep.mcMatchAny)
#         if fl not in (4,5): fl = 0
#         jetpt = lep.pt/lep.jetPtRatiov2
#         jetcsv = lep.jetBTagCSV

#         return self.sfreader.get_SF(jetpt, abs(lep.eta), fl, jetcsv, ## FIXME is if abs(eta) or eta?
#                                     getattr(lep, self.blabel),
#                                     self.rwtSyst, shapeCorr=True)

if __name__ == '__main__':
    from sys import argv
    file = ROOT.TFile(argv[1])
    tree = file.Get("tree")
    tree.vectorTree = True

    bTagSFs = BTagScaleFactors('csv', os.path.join(os.environ['CMSSW_BASE'],
                                     "src/CMGTools/TTHAnalysis/data/btag/",
                                     "CSVv2_4invfb.csv"),
                                algo='csv')

    class Tester(Module):
        def __init__(self, name):
            Module.__init__(self,name,None)
            self.sf = BTagSFReweightFriend(bTagSFs)
            self.sl = BTagLeptonReweightFriend(bTagSFs)
            self._wps = [ 0.605, 0.89, 0.97 ] ## FIXME?
            self._pcountA = [0, 0]
            self._pcount0 = [0 for w in self._wps]
            self._pcount1 = [0 for w in self._wps]

        def analyze(self,ev):
            print "\nrun %6d lumi %4d event %d: jets %d" % (ev.run, ev.lumi, ev.evt, ev.nJet25)

            ret = self.sf(ev)["Jet_btagCSVWeight"]
            # lrt = self.sl(ev)["LepGood_jetBTagCSVWeight"]
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

            # for i,j in enumerate(leps):
            #     print "\tlep %8.2f %+5.2f %+3d %.3f -> %.3f " % (j.pt, j.eta, j.mcMatchAny, min(max(0, j.jetBTagCSV), 1), lrt[i])
            # print ""

        def done(self):
            for iw,w in enumerate(self._wps):
                print " for WP %.3f, eff(pre) = %.3f, eff(post) = %.3f, SF = %.3f " % (w,
                                       self._pcount0[iw]/self._pcountA[0],
                                       self._pcount1[iw]/self._pcountA[1],
                                       self._pcount1[iw]/self._pcount0[iw]/self._pcountA[1]*self._pcountA[0])
    T = Tester("tester")
    el = EventLoop([ T ])
    el.loop([tree], maxEvents = 50)
    T.done()
