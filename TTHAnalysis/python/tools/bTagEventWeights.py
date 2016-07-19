#!/usr/bin/env python
import os.path, types
from array import array
from math import log, exp

from CMGTools.TTHAnalysis.treeReAnalyzer import ROOT, EventLoop, Module, Collection
from BTagScaleFactors import BTagScaleFactors

class BTagEventWeightFriend:
    def __init__(self, reader,
                 blabel="btagCSV",
                 label="eventBTagSF",
                 recllabel='Recl',
                 mcOnly=True):
        self.reader = reader

        self.jec_systs = ["", "_jecUp", "_jecDown"]
        self.recllabel = recllabel
        self.label = label
        self.blabel = blabel
        self.mcOnly = mcOnly

        # Automatically add the iterative systs from the reader
        self.btag_systs = ["central"]
        self.btag_systs += ["up_%s"  %s for s in self.reader.iterative_systs]
        self.btag_systs += ["down_%s"%s for s in self.reader.iterative_systs]

        # JEC to use for each syst:
        # Central one for all btag variations except up_jes and down_jes
        self.jec_syst_to_use = {}
        for btag_syst in self.btag_systs:
            self.jec_syst_to_use[btag_syst] = ""
        self.jec_syst_to_use["up_jes"] = "_jecUp"
        self.jec_syst_to_use["down_jes"] = "_jecDown"

    def listBranches(self):
        out = []
        for syst in self.btag_systs:
            label = "%s_%s" % (self.label, syst)
            if syst == 'central': label = self.label
            out.append(label)

        return out

    def getJetCollection(self, event, jec_syst):
        if not hasattr(event, "nJet"+jec_syst): jec_syst = ""
        jets_cent = [j for j in Collection(event, "Jet"    +jec_syst, "nJet"+jec_syst)]
        jets_disc = [j for j in Collection(event, "DiscJet"+jec_syst, "nDiscJet"+jec_syst)]

        _ijets_list = getattr(event, "iJSel_%s%s" % (self.recllabel, jec_syst))
        return [(jets_cent[ij] if ij>=0 else jets_disc[-ij-1]) for ij in _ijets_list]

    def __call__(self, event):
        ret = {}

        for syst in self.btag_systs:
            jets = self.getJetCollection(event, jec_syst=self.jec_syst_to_use[syst])

            label = "%s_%s" % (self.label, syst)
            if syst == 'central': label = self.label

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
    treefile = ROOT.TFile.Open(argv[1])
    tree = treefile.Get("tree")
    tree.vectorTree = True
    print "... processing %s" % argv[1]

    friendfile = ROOT.TFile.Open(argv[2])
    friendtree = friendfile.Get("sf/t")
    tree.AddFriend(friendtree)
    print "... adding friend tree from %s" % argv[2]


    btagsf_payload = os.path.join(os.environ['CMSSW_BASE'], "src/CMGTools/TTHAnalysis/data/btag/", "CSVv2_4invfb.csv")
    btagsf_reader = BTagScaleFactors('btagsf', btagsf_payload, algo='csv', verbose=3)

    class Tester(Module):
        def __init__(self, name):
            Module.__init__(self,name,None)
            self.sf = BTagEventWeightFriend(btagsf_reader)
            print "Adding these branches:", self.sf.listBranches()

        def analyze(self,ev):
            print "\nrun %6d lumi %4d event %d: jets %d" % (ev.run, ev.lumi, ev.evt, ev.nJet25)

            ret = self.sf(ev)
            jets = Collection(ev,"Jet")
            # leps = Collection(ev,"LepGood")

            for i,j in enumerate(jets):
                print "\tjet %8.2f %+5.2f %1d %.3f" % (j.pt, j.eta, j.hadronFlavour, min(max(0, j.btagCSV), 1))

            for label in self.sf.listBranches()[:10]:
                print "%8s"%label[-8:],
            print ""

            for label in self.sf.listBranches()[:10]:
                print "%8.3f" % ret[label],
            print ""


        def done(self):
            pass

    T = Tester("tester")
    el = EventLoop([ T ])
    el.loop([tree], maxEvents = 10)
    T.done()
