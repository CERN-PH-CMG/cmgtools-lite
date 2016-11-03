#!/usr/bin/env python
import os.path, types
from array import array
from math import log, exp

from CMGTools.TTHAnalysis.treeReAnalyzer import ROOT, EventLoop, Module, Collection
from BTagScaleFactors import BTagScaleFactors

class BTagEventWeightFriend:
    def __init__(self,
                 csvfile,
                 csvfastsim=None,
                 eff_rootfile=None,
                 algo='csv',
                 btag_branch='btagCSV',
                 flavor_branch='hadronFlavour',
                 label='eventBTagSF',
                 recllabel='Recl',
                 mcOnly=True):

        self.reader = BTagScaleFactors('btagsf',
                                       csvfile=csvfile,
                                       csvfastsim=csvfastsim,
                                       eff_rootfile=eff_rootfile,
                                       algo=algo,
                                       verbose=0)

        self.jec_systs = ["", "_jecUp", "_jecDown"]
        self.recllabel = recllabel
        self.label = label
        self.btag_branch = btag_branch
        self.flavor_branch = flavor_branch
        self.mcOnly = mcOnly

        self.is_fastsim = (csvfastsim != None)

        # Automatically add the iterative systs from the reader
        self.btag_systs = ["central"]
        self.btag_systs += ["up_%s"  %s for s in self.reader.iterative_systs]
        self.btag_systs += ["down_%s"%s for s in self.reader.iterative_systs]

        # Take only central, up_correlated, and down_correlated for fastsim
        if self.is_fastsim:
            self.btag_systs = ["central", "up_correlated", "down_correlated"]


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
            if not hasattr(self,'_debugprinted'): print 'Recleaned jets not found, falling back to default cleaned collection'
            self._debugprinted = True
            return jets


    def event_weight_from_discr_shape(self, jets,
                                      syst="central",
                                      flavorAttr=None,
                                      btagAttr=None):
        syst = syst.lower()
        if not flavorAttr: flavorAttr=self.flavor_branch
        if not btagAttr:   btagAttr=self.btag_branch

        weight = 1.0
        for jet in jets:
            flavor  = getattr(jet, flavorAttr)
            btagval = getattr(jet, btagAttr)
            weight *= self.reader.get_SF(pt=jet.pt, eta=jet.eta,
                                  flavor=flavor, val=btagval,
                                  syst=syst, shape_corr=True)
        return weight

    def fastsim_event_weight(self, jets,
                             syst="central",
                             flavorAttr=None,
                             btagAttr=None,
                             wp='M'):
        """
        This would correspond to the event weight when for a selection
        of events with jets of the given WP.
        """
        syst = syst.lower()
        if not flavorAttr: flavorAttr=self.flavor_branch
        if not btagAttr:   btagAttr=self.btag_branch

        pmc = 1.0
        pdata = 1.0
        for jet in jets:
            flavor  = getattr(jet, flavorAttr)
            btagval = getattr(jet, btagAttr)
            tagged = (btagval >= self.reader.working_points[wp])

            fastsim_syst = syst
            if 'correlated' in syst:
                fastsim_syst = syst.split('_', 1)[0] # take 'down' or 'up' for fastsim
            sf_fastsim = self.reader.get_SF(pt=jet.pt, eta=jet.eta,
                                            flavor=flavor, val=btagval,
                                            syst=fastsim_syst, mtype='fastsim')

            efficiency = self.reader.get_tagging_efficiency(jet, wp)

            # Convert to fullsim efficiency using scale factors
            # Inverted, because fastsim SF are defined as eff_full / eff_fast
            #    and we are using fullsim efficiencies
            efficiency /= sf_fastsim

            if not tagged:
                efficiency = 1.0 - efficiency

            sf_fullsim = self.reader.get_SF(pt=jet.pt, eta=jet.eta,
                                            flavor=flavor, val=btagval,
                                            syst=syst, mtype='auto')

            pmc *= efficiency
            pdata *= sf_fullsim*efficiency

        try:
            return pmc/pdata
        except ZeroDivisionError:
            print "WARNING: scale factor of 0 found"
            return 1.0



    def __call__(self, event):
        ret = {k:1.0 for k in self.branches}
        if self.mcOnly and event.isData: return ret

        for syst in self.btag_systs:
            jets = self.getJetCollection(event, jec_syst=self.jec_syst_to_use[syst])

            label = "%s_%s" % (self.label, syst)
            if syst == 'central': label = self.label

            if not self.is_fastsim:
                ret[label] = self.event_weight_from_discr_shape(jets, syst=syst)
            else:
                ret[label] = self.fastsim_event_weight(jets, syst=syst, wp='L')
        return ret

if __name__ == '__main__':
    from sys import argv
    treefile = ROOT.TFile.Open(argv[1])
    tree = treefile.Get("tree")
    tree.vectorTree = True
    print "... processing %s" % argv[1]

    try:
        friendfile = ROOT.TFile.Open(argv[2])
        friendtree = friendfile.Get("sf/t")
        tree.AddFriend(friendtree)
        print "... adding friend tree from %s" % argv[2]
    except IndexError:
        pass


    btagsf_payload = os.path.join(os.environ['CMSSW_BASE'], "src/CMGTools/TTHAnalysis/data/btag/", "CSVv2_ichep.csv")

    class Tester(Module):
        def __init__(self, name):
            Module.__init__(self,name,None)
            self.sf = BTagEventWeightFriend(btagsf_payload, recllabel="Recl", algo='csv')
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

    btagsf_payload_fastsim = os.path.join(os.environ['CMSSW_BASE'], "src/CMGTools/TTHAnalysis/data/btag/", "CSV_13TEV_TTJets_11_7_2016.csv")
    btag_efficiency_file   = os.path.join(os.environ['CMSSW_BASE'], "src/CMGTools/TTHAnalysis/data/btag/", "bTagEffs.root")

    class TesterFastSim(Module):
        def __init__(self, name):
            Module.__init__(self,name,None)
            self.sf = BTagEventWeightFriend(csvfile=btagsf_payload,
                                            csvfastsim=btagsf_payload_fastsim,
                                            eff_rootfile=btag_efficiency_file,
                                            recllabel="Recl", algo='csv')
            print "Adding these branches:", self.sf.listBranches()

        def analyze(self,ev):
            # print "\nrun %6d lumi %4d event %d: jets %d, isdata=%d" % (ev.run, ev.lumi, ev.evt, ev.nJet25, int(ev.isData))
            ret = self.sf(ev)
            # jets = Collection(ev,"Jet")
            # leps = Collection(ev,"LepGood")

            # for i,j in enumerate(jets):
            #     print "\tjet %8.2f %+5.2f %1d %.3f" % (j.pt, j.eta, getattr(j, "hadronFlavour", -1), min(max(0, j.btagCSV), 1))

            # for label in self.sf.listBranches()[:10]:
            #     print "%8s"%label[-8:],
            # print ""

            for label in self.sf.listBranches()[:10]:
                print "%8.3f" % ret[label],
            print ""


        def done(self):
            pass

    T = TesterFastSim("tester")
    el = EventLoop([ T ])
    el.loop([tree], maxEvents = 100)
    T.done()
