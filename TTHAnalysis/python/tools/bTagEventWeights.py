#!/usr/bin/env python
import os.path, types
from array import array
from math import log, exp

from CMGTools.TTHAnalysis.treeReAnalyzer import ROOT, EventLoop, Module, Collection
from BTagScaleFactors import BTagScaleFactors

class BTagEventWeightFriend:
    def __init__(self, reader,
                 jetlabel="Jet",
                 blabel="btagCSV",
                 label="eventBTagSF",
                 mcOnly=True):
        self.reader = reader

        self.jetlabel = jetlabel
        self.label = label
        self.blabel = blabel
        self.mcOnly = mcOnly

        # Automatically add the iterative systs from the reader
        self.systs = ["central"]
        self.systs += ["up_%s"  %s for s in self.reader.iterative_systs]
        self.systs += ["down_%s"%s for s in self.reader.iterative_systs]

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

            ret[label] = self.reader.get_event_SF(jets, syst=syst)

        return ret

# class BTagLeptonEventWeightFriend(BTagEventWeightFriend):
#     def __init__(self, reweight,
#                  jetlabel="LepGood",
#                  blabel="jetBTagCSV",
#                  label="jetBTagCSVWeight",
#                  rwtSyst="central"):
#         BTagEventWeightFriend.__init__(self, reader,
#                                       jetlabel=jetlabel,
#                                       blabel=blabel,
#                                       label=label,
#                                       mcOnly=True)



#     def reweight(self, event, lep):
#         if self.mcOnly and event.isData:
#             return -99.0
#         fl = abs(lep.mcMatchAny)
#         if fl not in (4,5): fl = 0
#         jetpt = lep.pt/lep.jetPtRatiov2
#         jetcsv = lep.jetBTagCSV

#         return self.reader.get_SF(jetpt, abs(lep.eta), fl, jetcsv, ## FIXME is if abs(eta) or eta?
#                                     getattr(lep, self.blabel),
#                                     self.rwtSyst, shapeCorr=True)

if __name__ == '__main__':
    from sys import argv
    file = ROOT.TFile.Open(argv[1])
    tree = file.Get("tree")
    tree.vectorTree = True

    print "... processing %s" % argv[1]

    btagsf_payload = os.path.join(os.environ['CMSSW_BASE'], "src/CMGTools/TTHAnalysis/data/btag/", "CSVv2_4invfb.csv")
    btagsf_reader = BTagScaleFactors('btagsf', btagsf_payload, algo='csv', verbose=3)

    class Tester(Module):
        def __init__(self, name):
            Module.__init__(self,name,None)
            self.sf = BTagEventWeightFriend(btagsf_reader)

        def analyze(self,ev):
            print "\nrun %6d lumi %4d event %d: jets %d" % (ev.run, ev.lumi, ev.evt, ev.nJet25)

            ret = self.sf(ev)
            jets = Collection(ev,"Jet")
            # leps = Collection(ev,"LepGood")

            for i,j in enumerate(jets):
                print "\tjet %8.2f %+5.2f %1d %.3f" % (j.pt, j.eta, j.hadronFlavour, min(max(0, j.btagCSV), 1))

            for syst in self.sf.systs[:10]:
                print "%8s"%syst[-8:],
            print ""

            for syst in self.sf.systs[:10]:
                label = self.sf.label
                if not syst == "central":
                    label = "%s_%s" % (label, syst)
                print "%8.3f" % ret[label],
            print ""


        def done(self):
            pass

    T = Tester("tester")
    el = EventLoop([ T ])
    el.loop([tree], maxEvents = 10)
    T.done()
