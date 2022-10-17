#!/usr/bin/env python
import os.path, types
from array import array
from math import log, exp

from CMGTools.TTHAnalysis.treeReAnalyzer import ROOT, EventLoop, Module, Collection
from BTagCSVFullShape import BTagCSVFullShape

class BTagEventWeightFriend:
    def __init__(self,
                 csvfile,
                 label='eventBTagSF',
                 recllabel='_Recl',
                 mcOnly=True,
                 discrname='btagCSV'):

        self.reader = BTagCSVFullShape(csvfile=csvfile)

        self.systsJEC = {0:"", 1:"_jecUp", -1:"_jecDown"}
        self.recllabel = recllabel
        self.label = label
        self.mcOnly = mcOnly
        self.discrname = discrname

        # Automatically add the iterative systs from the reader
        self.btag_systs = ["central"]
        self.btag_systs += ["up_%s"  %s for s in self.reader.iterative_systs]
        self.btag_systs += ["down_%s"%s for s in self.reader.iterative_systs]

        # JEC to use for each syst:
        # Central one for all btag variations except up_jes and down_jes
        self.jec_syst_to_use = {}
        for btag_syst in self.btag_systs:
            self.jec_syst_to_use[btag_syst] = 0
        self.jec_syst_to_use["up_jes"] = 1
        self.jec_syst_to_use["down_jes"] = -1

        self.branches = self.listBranches()

    def listBranches(self):
        out = []
        for syst in self.btag_systs:
            label = "%s_%s" % (self.label, syst)
            if syst == 'central': label = self.label
            out.append(label)

        return out

    def __call__(self, event):
        ret = {k:1.0 for k in self.branches}
        if self.mcOnly and event.isData: return ret

        jetscoll = {}
        for _var in self.systsJEC:
            jets = [j for j in Collection(event,"JetSel"+self.recllabel,"nJetSel"+self.recllabel)]
            jetptcut = 25
            if (_var==0): jets = filter(lambda x : x.pt>jetptcut, jets)
            elif (_var==1): jets = filter(lambda x : x.pt*x.corr_JECUp/x.corr>jetptcut, jets)
            elif (_var==-1): jets = filter(lambda x : x.pt*x.corr_JECDown/x.corr>jetptcut, jets)
            if (_var==0): jetcorr = [1 for x in jets]
            elif (_var==1): jetcorr = [x.corr_JECUp/x.corr for x in jets]
            elif (_var==-1): jetcorr = [x.corr_JECDown/x.corr for x in jets]
            jetscoll[_var]=(jets,jetcorr)

        for syst in self.btag_systs:

            _var=self.jec_syst_to_use[syst]

            label = "%s_%s" % (self.label, syst)
            if syst == 'central': label = self.label

            weight = 1.0
            jets,jetcorr = jetscoll[_var]
            for i,jet in enumerate(jets):
                weight *= self.reader.get_SF(pt=jet.pt*jetcorr[i], eta=jet.eta,
                                      flavor=jet.hadronFlavour, val=getattr(jet,self.discrname),
                                      syst=syst)
            ret[label] = weight

        return ret

