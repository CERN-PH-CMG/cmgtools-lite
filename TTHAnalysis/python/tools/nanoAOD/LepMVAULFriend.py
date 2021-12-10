#!/usr/bin/env python
from array import array
from glob import glob
import os.path

import ROOT
import math 

from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection as Collection 
from CMGTools.TTHAnalysis.tools.mvaTool import *



elVars = [
     MVAVar("Electron_pt", func=lambda x: x.pt),
     MVAVar("Electron_eta", func=lambda x: x.eta),
     MVAVar("Electron_pfRelIso03_all", func=lambda x: x.pfRelIso03_all),
     MVAVar("Electron_miniPFRelIso_chg", func=lambda x: x.miniPFRelIso_chg),
     MVAVar("Electron_miniRelIsoNeutral := Electron_miniPFRelIso_all - Electron_miniPFRelIso_chg", func=lambda x: x.miniPFRelIso_all - x.miniPFRelIso_chg),
     MVAVar("Electron_jetNDauCharged", func=lambda x: x.jetNDauCharged),
     MVAVar("Electron_jetPtRelv2", func=lambda x: x.jetPtRelv2),
     MVAVar("Electron_jetPtRatio := min(1 / (1 + Electron_jetRelIso), 1.5)", func=lambda x: min(1 / (1 + x.jetRelIso), 1.5)),
     MVAVar("Electron_jetBTagDeepFlavB := Electron_jetIdx > -1 ? Jet_btagDeepFlavB[Electron_jetIdx] : 0", func=lambda x: x.jetBTagDeepFlav),
     MVAVar("Electron_sip3d", func=lambda x: x.sip3d),
     MVAVar("Electron_dxy := log(abs(Electron_dxy))",func=lambda x: math.log(abs(x.dxy))),
     MVAVar("Electron_dz  := log(abs(Electron_dz))", func=lambda x: math.log(abs(x.dz))),
     MVAVar("Electron_mvaFall17V2noIso", func=lambda x: x.mvaFall17V2noIso)
]

class LeptonMVA:
    def __init__(self,elpath):
        print "Booking %s" % (elpath)

        self.el = MVATool("BDTG", elpath,elVars)

    def __call__(self,lep, debug):
        if debug: print 'calling'
        if   abs(lep.pdgId) == 11: return self.el(lep, debug)
        elif abs(lep.pdgId) == 13: return lep.mvaTTH # for muons we keep the old training since we would lose performance by retraining on top of nano
        else: return -99

class LepMVAFriend(Module):
    def __init__(self, era, separateCollections):
        self.mva = LeptonMVA(os.environ['CMSSW_BASE']+'/src/CMGTools/TTHAnalysis/data/leptonMVA/tth/UL20_%s.xml'%era)
        self.collections = ['Electron', 'Muon'] if separateCollections else [ 'LepGood']

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.wrappedOutputTree = wrappedOutputTree
        for coll in self.collections:
            self.wrappedOutputTree.branch( '%s_mvaTTHUL'%coll, "F", lenVar="n%s"%coll)

    def analyze(self,event):
        debug = bool(event.event == 207226029)
        for coll in self.collections:
            lep = Collection(event,coll)
            self.wrappedOutputTree.fillBranch( '%s_mvaTTHUL'%coll,  [ self.mva(l, debug) for l in lep ])

        return True

lepMVA_16=lambda : LepMVAFriend('16', False)
lepMVA_16_preVFP=lambda : LepMVAFriend('16_preVFP', False)
lepMVA_17=lambda : LepMVAFriend('17', False)
lepMVA_18=lambda : LepMVAFriend('18', False)
