#!/usr/bin/env python
import os.path, types
from array import array
from math import log, exp

from CMGTools.TTHAnalysis.treeReAnalyzer import ROOT, EventLoop, Module, Collection
from BTagScaleFactors import BTagScaleFactors

class BTagEventWeightFriend:
    def __init__(self, csvfile,
                 algo='csv',
                 btag_branch='btagCSV',
                 flavor_branch='hadronFlavour',
                 label='eventBTagSF',
                 recllabel='Recl',
                 mcOnly=True):

        self.reader = BTagScaleFactors('btagsf', csvfile=csvfile, algo=algo, verbose=0)

        self.jec_systs = ["", "_jecUp", "_jecDown"]
        self.recllabel = recllabel
        self.label = label
        self.btag_branch = btag_branch
        self.flavor_branch = flavor_branch
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

        self.branches = self.listBranches()

    def listBranches(self):
        out = []
        for syst in self.btag_systs:
            label = "%s_%s" % (self.label, syst)
            if syst == 'central': label = self.label
            out.append(label)

        return out

    def getJetCollection(self, event, jec_syst):
        if not hasattr(event, "nJet"+jec_syst): jec_syst = ""
        jets      = [j for j in Collection(event, "Jet"    +jec_syst, "nJet"    +jec_syst)]
        jets_disc = [j for j in Collection(event, "DiscJet"+jec_syst, "nDiscJet"+jec_syst)]

        try:
            _ijets_list = getattr(event, "iJSel_%s%s" % (self.recllabel, jec_syst))
            return [(jets[ij] if ij>=0 else jets_disc[-ij-1]) for ij in _ijets_list]
        except AttributeError:
            return jets

    def __call__(self, event):
        ret = {k:1.0 for k in self.branches}
        if self.mcOnly and event.isData: return ret

        for syst in self.btag_systs:
            jets = self.getJetCollection(event, jec_syst=self.jec_syst_to_use[syst])

            label = "%s_%s" % (self.label, syst)
            if syst == 'central': label = self.label

            ret[label] = self.reader.get_event_SF(jets, syst=syst,
                                                  flavorAttr=self.flavor_branch,
                                                  btagAttr=self.btag_branch)

        return ret

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
            self.sf = BTagEventWeightFriend(btagsf_reader, recllabel="Recl")
            print "Adding these branches:", self.sf.listBranches()

        def analyze(self,ev):
            print "\nrun %6d lumi %4d event %d: jets %d, isdata=%d" % (ev.run, ev.lumi, ev.evt, ev.nJet25, int(ev.isData))
            ret = self.sf(ev)
            jets = Collection(ev,"Jet")
            # leps = Collection(ev,"LepGood")

            for i,j in enumerate(jets):
                print "\tjet %8.2f %+5.2f %1d %.3f" % (j.pt, j.eta, getattr(j, "hadronFlavour", -1), min(max(0, j.btagCSV), 1))

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
