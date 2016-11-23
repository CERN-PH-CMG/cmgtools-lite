#!/usr/bin/env python
from CMGTools.TTHAnalysis.treeReAnalyzer import *
from array import array
from glob import glob
import os.path

import ROOT

class MVAVar:
    def __init__(self,name,func,corrfunc=None):
        self.name = name
        self.var  = array('f',[0.])
        self.func = func
        self.corrfunc = corrfunc
    def set(self,lep,ncorr): ## apply correction ncorr times
        self.var[0] = self.func(lep)
        if self.corrfunc:
            for i in range(ncorr):
                self.var[0] = self.corrfunc(self.var[0], lep.pdgId,lep.pt,lep.eta,lep.mcMatchId,lep.mcMatchAny)

from CMGTools.TTHAnalysis.leptonMVA import MVATool, CategorizedMVA

_CommonSpect = {
    'forMoriond16': [],
    'forMoriond16NoJetChDau': [],
    'mvaMultiIso' : [],
    'SoftALaMoriond16': [
        MVAVar("LepGood_mcMatchAny",lambda x: x.mcMatchAny),
        ],
    'SoftJetLess': [
        MVAVar("LepGood_mcMatchAny",lambda x: x.mcMatchAny),
        ],
    'SoftJetLessIVF': [
        MVAVar("LepGood_mcMatchAny",lambda x: x.mcMatchAny),
        ],
    'SoftJetLessIVFSVSafe': [
        MVAVar("LepGood_mcMatchAny",lambda x: x.mcMatchAny),
        ],
    'SoftJetLessNOBTAG': [
        MVAVar("LepGood_mcMatchAny",lambda x: x.mcMatchAny),
        ],
    'SoftJetLessNO04ISO': [
        MVAVar("LepGood_mcMatchAny",lambda x: x.mcMatchAny),
        ],
    'SoftJetLessMuCBID': [
        MVAVar("LepGood_mcMatchAny",lambda x: x.mcMatchAny),
        ],
    'SoftJetLessMuMVAID': [
        MVAVar("LepGood_mcMatchAny",lambda x: x.mcMatchAny),
        ],
    'SoftJetLessIVFMuMVAID': [
        MVAVar("LepGood_mcMatchAny",lambda x: x.mcMatchAny),
        ],
}
_CommonVars = {
'mvaMultiIso' : [ 
    MVAVar("LepGood_miniRelIso",lambda x: x.miniRelIso),
    MVAVar("LepGood_jetPtRelv2",lambda x: x.jetPtRelv2),
    MVAVar("LepGood_jetPtRatiov2 := min(LepGood_jetPtRatiov2,1.5)", lambda x : min(x.jetPtRatiov2,1.5)),
],
'forMoriond16': [
    MVAVar("LepGood_pt",lambda x: x.pt),
    MVAVar("LepGood_eta",lambda x: x.eta),
    MVAVar("LepGood_jetNDauChargedMVASel",lambda x: x.jetNDauChargedMVASel),
    MVAVar("LepGood_miniRelIsoCharged",lambda x: x.miniRelIsoCharged),
    MVAVar("LepGood_miniRelIsoNeutral",lambda x: x.miniRelIsoNeutral),
    MVAVar("LepGood_jetPtRelv2",lambda x: x.jetPtRelv2),
    MVAVar("LepGood_jetPtRatio := min(LepGood_jetPtRatiov2,1.5)", lambda x : min(x.jetPtRatiov2,1.5)),
    MVAVar("LepGood_jetBTagCSV := max(LepGood_jetBTagCSV,0)", lambda x : max(x.jetBTagCSV,0.)),
    MVAVar("LepGood_sip3d",lambda x: x.sip3d),
    MVAVar("LepGood_dxy := log(abs(LepGood_dxy))",lambda x: log(abs(x.dxy))),
    MVAVar("LepGood_dz  := log(abs(LepGood_dz))", lambda x: log(abs(x.dz))),
],
'forMoriond16NoJetChDau': [
    MVAVar("LepGood_pt",lambda x: x.pt),
    MVAVar("LepGood_eta",lambda x: x.eta),
    #MVAVar("LepGood_jetNDauChargedMVASel",lambda x: x.jetNDauChargedMVASel),
    MVAVar("LepGood_miniRelIsoCharged",lambda x: x.miniRelIsoCharged),
    MVAVar("LepGood_miniRelIsoNeutral",lambda x: x.miniRelIsoNeutral),
    MVAVar("LepGood_jetPtRelv2",lambda x: x.jetPtRelv2),
    MVAVar("LepGood_jetPtRatio := min(LepGood_jetPtRatiov2,1.5)", lambda x : min(x.jetPtRatiov2,1.5)),
    MVAVar("LepGood_jetBTagCSV := max(LepGood_jetBTagCSV,0)", lambda x : max(x.jetBTagCSV,0.)),
    MVAVar("LepGood_sip3d",lambda x: x.sip3d),
    MVAVar("LepGood_dxy := log(abs(LepGood_dxy))",lambda x: log(abs(x.dxy))),
    MVAVar("LepGood_dz  := log(abs(LepGood_dz))", lambda x: log(abs(x.dz))),
],
'SoftALaMoriond16': [
    MVAVar("LepGood_pt",lambda x: x.pt),
    MVAVar("LepGood_eta",lambda x: x.eta),
    MVAVar("LepGood_jetNDauChargedMVASel",lambda x: x.jetNDauChargedMVASel),
    MVAVar("LepGood_miniRelIsoCharged",lambda x: x.miniRelIsoCharged),
    MVAVar("LepGood_miniRelIsoNeutral",lambda x: x.miniRelIsoNeutral),
    MVAVar("LepGood_jetPtRelv2",lambda x: x.jetPtRelv2),
    MVAVar("LepGood_jetPtRatio := min(LepGood_jetPtRatiov2,1.5)", lambda x : min(x.jetPtRatiov2,1.5)),
    MVAVar("LepGood_jetBTagCSV := max(LepGood_jetBTagCSV,0)", lambda x : max(x.jetBTagCSV,0.)),
    MVAVar("LepGood_sip3d",lambda x: x.sip3d),
    MVAVar("LepGood_dxy := log(abs(LepGood_dxy))",lambda x: log(abs(x.dxy))),
    MVAVar("LepGood_dz  := log(abs(LepGood_dz))", lambda x: log(abs(x.dz))),
],
'SoftJetLess': [
    MVAVar("LepGood_pt",lambda x: x.pt),
    MVAVar("LepGood_eta",lambda x: x.eta),
    MVAVar("LepGood_miniRelIsoCharged := min(LepGood_miniRelIsoCharged,4)",lambda x: x.miniRelIsoCharged),
    MVAVar("LepGood_miniRelIsoNeutral := min(LepGood_miniRelIsoNeutral,4)",lambda x: x.miniRelIsoNeutral),
    MVAVar("LepGood_isoRelH04",lambda x: x.isoRelH04),
    MVAVar("LepGood_RelIsoChargedFix04 := min(LepGood_RelIsoChargedFix04,4)",lambda x: x.RelIsoMIVCharged04),
    MVAVar("LepGood_RelIsoNeutralFix04 := min(LepGood_RelIsoNeutralFix04,4)",lambda x: x.RelIsoMIVNeutral04),
    MVAVar("LepGood_jetBTagCSV := max(LepGood_jetBTagCSV,0)", lambda x : max(x.jetBTagCSV,0.)),
    MVAVar("LepGood_sip3d",lambda x: x.sip3d),
    MVAVar("LepGood_dxy := log(abs(LepGood_dxy))",lambda x: log(abs(x.dxy))),
    MVAVar("LepGood_dz  := log(abs(LepGood_dz))", lambda x: log(abs(x.dz))),
],
'SoftJetLessIVF': [
    MVAVar("LepGood_pt",lambda x: x.pt),
    MVAVar("LepGood_eta",lambda x: x.eta),
    MVAVar("LepGood_miniRelIsoCharged := min(LepGood_miniRelIsoCharged,4)",lambda x: x.miniRelIsoCharged),
    MVAVar("LepGood_miniRelIsoNeutral := min(LepGood_miniRelIsoNeutral,4)",lambda x: x.miniRelIsoNeutral),
    MVAVar("LepGood_isoRelH04",lambda x: x.isoRelH04),
    MVAVar("LepGood_RelIsoChargedFix04 := min(LepGood_RelIsoChargedFix04,4)",lambda x: x.RelIsoMIVCharged04),
    MVAVar("LepGood_RelIsoNeutralFix04 := min(LepGood_RelIsoNeutralFix04,4)",lambda x: x.RelIsoMIVNeutral04),
    MVAVar("LepGood_hasSV", lambda x: x.hasSV),
    MVAVar("LepGood_svSip3d := max(LepGood_svSip3d,0)", lambda x: max(x.svSip3d,0)),
    MVAVar("LepGood_svRedPt := max(LepGood_svRedPt,0)", lambda x: max(x.svRedPt,0)),
    MVAVar("LepGood_svMass := max(LepGood_svMass,0)", lambda x: max(x.svMass,0)),
    MVAVar("LepGood_svNTracks := max(LepGood_svNTracks,0)", lambda x: max(x.svNTracks,0)),
    MVAVar("LepGood_sip3d",lambda x: x.sip3d),
    MVAVar("LepGood_dxy := log(abs(LepGood_dxy))",lambda x: log(abs(x.dxy))),
    MVAVar("LepGood_dz  := log(abs(LepGood_dz))", lambda x: log(abs(x.dz))),
],
'SoftJetLessIVFSVSafe': [
    MVAVar("LepGood_pt",lambda x: x.pt),
    MVAVar("LepGood_eta",lambda x: x.eta),
    MVAVar("LepGood_miniRelIsoCharged := min(LepGood_miniRelIsoCharged,4)",lambda x: x.miniRelIsoCharged),
    MVAVar("LepGood_miniRelIsoNeutral := min(LepGood_miniRelIsoNeutral,4)",lambda x: x.miniRelIsoNeutral),
    MVAVar("LepGood_isoRelH04",lambda x: x.isoRelH04),
    MVAVar("LepGood_RelIsoChargedFix04 := min(LepGood_RelIsoChargedFix04,4)",lambda x: x.RelIsoMIVCharged04),
    MVAVar("LepGood_RelIsoNeutralFix04 := min(LepGood_RelIsoNeutralFix04,4)",lambda x: x.RelIsoMIVNeutral04),
    MVAVar("LepGood_hasSV := (LepGood_hasSV>1)*(LepGood_hasSV)", lambda x: (x.hasSV>1)*(x.hasSV)),
    MVAVar("LepGood_svSip3d := (LepGood_hasSV>1)*(max(LepGood_svSip3d,0))", lambda x: (x.hasSV>1)*(max(x.svSip3d,0))),
    MVAVar("LepGood_svRedPt := (LepGood_hasSV>1)*(max(LepGood_svRedPt,0))", lambda x: (x.hasSV>1)*(max(x.svRedPt,0))),
    MVAVar("LepGood_svMass := (LepGood_hasSV>1)*(max(LepGood_svMass,0))", lambda x: (x.hasSV>1)*(max(x.svMass,0))),
    MVAVar("LepGood_svNTracks := (LepGood_hasSV>1)*(max(LepGood_svNTracks,0))", lambda x: (x.hasSV>1)*(max(x.svNTracks,0))),
    MVAVar("LepGood_sip3d",lambda x: x.sip3d),
    MVAVar("LepGood_dxy := log(abs(LepGood_dxy))",lambda x: log(abs(x.dxy))),
    MVAVar("LepGood_dz  := log(abs(LepGood_dz))", lambda x: log(abs(x.dz))),
],
'SoftJetLessNOBTAG': [
    MVAVar("LepGood_pt",lambda x: x.pt),
    MVAVar("LepGood_eta",lambda x: x.eta),
    MVAVar("LepGood_miniRelIsoCharged := min(LepGood_miniRelIsoCharged,4)",lambda x: x.miniRelIsoCharged),
    MVAVar("LepGood_miniRelIsoNeutral := min(LepGood_miniRelIsoNeutral,4)",lambda x: x.miniRelIsoNeutral),
    MVAVar("LepGood_isoRelH04",lambda x: x.isoRelH04),
    MVAVar("LepGood_RelIsoChargedFix04 := min(LepGood_RelIsoChargedFix04,4)",lambda x: x.RelIsoMIVCharged04),
    MVAVar("LepGood_RelIsoNeutralFix04 := min(LepGood_RelIsoNeutralFix04,4)",lambda x: x.RelIsoMIVNeutral04),
    MVAVar("LepGood_sip3d",lambda x: x.sip3d),
    MVAVar("LepGood_dxy := log(abs(LepGood_dxy))",lambda x: log(abs(x.dxy))),
    MVAVar("LepGood_dz  := log(abs(LepGood_dz))", lambda x: log(abs(x.dz))),
],
'SoftJetLessNO04ISO': [
    MVAVar("LepGood_pt",lambda x: x.pt),
    MVAVar("LepGood_eta",lambda x: x.eta),
    MVAVar("LepGood_miniRelIsoCharged := min(LepGood_miniRelIsoCharged,4)",lambda x: x.miniRelIsoCharged),
    MVAVar("LepGood_miniRelIsoNeutral := min(LepGood_miniRelIsoNeutral,4)",lambda x: x.miniRelIsoNeutral),
    MVAVar("LepGood_jetBTagCSV := max(LepGood_jetBTagCSV,0)", lambda x : max(x.jetBTagCSV,0.)),
    MVAVar("LepGood_sip3d",lambda x: x.sip3d),
    MVAVar("LepGood_dxy := log(abs(LepGood_dxy))",lambda x: log(abs(x.dxy))),
    MVAVar("LepGood_dz  := log(abs(LepGood_dz))", lambda x: log(abs(x.dz))),
],
'SoftJetLessMuCBID': [
    MVAVar("LepGood_pt",lambda x: x.pt),
    MVAVar("LepGood_eta",lambda x: x.eta),
    MVAVar("LepGood_miniRelIsoCharged := min(LepGood_miniRelIsoCharged,4)",lambda x: x.miniRelIsoCharged),
    MVAVar("LepGood_miniRelIsoNeutral := min(LepGood_miniRelIsoNeutral,4)",lambda x: x.miniRelIsoNeutral),
    MVAVar("LepGood_isoRelH04",lambda x: x.isoRelH04),
    MVAVar("LepGood_RelIsoChargedFix04 := min(LepGood_RelIsoChargedFix04,4)",lambda x: x.RelIsoMIVCharged04),
    MVAVar("LepGood_RelIsoNeutralFix04 := min(LepGood_RelIsoNeutralFix04,4)",lambda x: x.RelIsoMIVNeutral04),
    MVAVar("LepGood_jetBTagCSV := max(LepGood_jetBTagCSV,0)", lambda x : max(x.jetBTagCSV,0.)),
    MVAVar("LepGood_sip3d",lambda x: x.sip3d),
    MVAVar("LepGood_dxy := log(abs(LepGood_dxy))",lambda x: log(abs(x.dxy))),
    MVAVar("LepGood_dz  := log(abs(LepGood_dz))", lambda x: log(abs(x.dz))),
],
'SoftJetLessMuMVAID': [
    MVAVar("LepGood_pt",lambda x: x.pt),
    MVAVar("LepGood_eta",lambda x: x.eta),
    MVAVar("LepGood_miniRelIsoCharged := min(LepGood_miniRelIsoCharged,4)",lambda x: x.miniRelIsoCharged),
    MVAVar("LepGood_miniRelIsoNeutral := min(LepGood_miniRelIsoNeutral,4)",lambda x: x.miniRelIsoNeutral),
    MVAVar("LepGood_isoRelH04",lambda x: x.isoRelH04),
    MVAVar("LepGood_RelIsoChargedFix04 := min(LepGood_RelIsoChargedFix04,4)",lambda x: x.RelIsoMIVCharged04),
    MVAVar("LepGood_RelIsoNeutralFix04 := min(LepGood_RelIsoNeutralFix04,4)",lambda x: x.RelIsoMIVNeutral04),
    MVAVar("LepGood_jetBTagCSV := max(LepGood_jetBTagCSV,0)", lambda x : max(x.jetBTagCSV,0.)),
    MVAVar("LepGood_sip3d",lambda x: x.sip3d),
    MVAVar("LepGood_dxy := log(abs(LepGood_dxy))",lambda x: log(abs(x.dxy))),
    MVAVar("LepGood_dz  := log(abs(LepGood_dz))", lambda x: log(abs(x.dz))),
],
'SoftJetLessIVFMuMVAID': [
    MVAVar("LepGood_pt",lambda x: x.pt),
    MVAVar("LepGood_eta",lambda x: x.eta),
    MVAVar("LepGood_miniRelIsoCharged := min(LepGood_miniRelIsoCharged,4)",lambda x: x.miniRelIsoCharged),
    MVAVar("LepGood_miniRelIsoNeutral := min(LepGood_miniRelIsoNeutral,4)",lambda x: x.miniRelIsoNeutral),
    MVAVar("LepGood_isoRelH04",lambda x: x.isoRelH04),
    MVAVar("LepGood_RelIsoChargedFix04 := min(LepGood_RelIsoChargedFix04,4)",lambda x: x.RelIsoMIVCharged04),
    MVAVar("LepGood_RelIsoNeutralFix04 := min(LepGood_RelIsoNeutralFix04,4)",lambda x: x.RelIsoMIVNeutral04),
    MVAVar("LepGood_hasSV", lambda x: x.hasSV),
    MVAVar("LepGood_svSip3d := max(LepGood_svSip3d,0)", lambda x: max(x.svSip3d,0)),
    MVAVar("LepGood_svRedPt := max(LepGood_svRedPt,0)", lambda x: max(x.svRedPt,0)),
    MVAVar("LepGood_svMass := max(LepGood_svMass,0)", lambda x: max(x.svMass,0)),
    MVAVar("LepGood_svNTracks := max(LepGood_svNTracks,0)", lambda x: max(x.svNTracks,0)),
    MVAVar("LepGood_sip3d",lambda x: x.sip3d),
    MVAVar("LepGood_dxy := log(abs(LepGood_dxy))",lambda x: log(abs(x.dxy))),
    MVAVar("LepGood_dz  := log(abs(LepGood_dz))", lambda x: log(abs(x.dz))),
],

}

_ElectronVars = [
    MVAVar("LepGood_mvaIdSpring15",lambda x: x.mvaIdSpring15)
]

_MuonVars = {
    'mvaMultiIso': [],
    'forMoriond16': [
        MVAVar("LepGood_segmentCompatibility",lambda x: x.segmentCompatibility)
        ],
    'forMoriond16NoJetChDau': [
        MVAVar("LepGood_segmentCompatibility",lambda x: x.segmentCompatibility)
        ],
    'SoftJetLess': [
        MVAVar("LepGood_segmentCompatibility",lambda x: x.segmentCompatibility)
        ],
    'SoftJetLessIVF': [
        MVAVar("LepGood_segmentCompatibility",lambda x: x.segmentCompatibility)
        ],
    'SoftJetLessIVFSVSafe': [
        MVAVar("LepGood_segmentCompatibility",lambda x: x.segmentCompatibility)
        ],
    'SoftJetLessNOBTAG': [
        MVAVar("LepGood_segmentCompatibility",lambda x: x.segmentCompatibility)
        ],
    'SoftJetLessNO04ISO': [
        MVAVar("LepGood_segmentCompatibility",lambda x: x.segmentCompatibility)
        ],
    'SoftJetLessMuCBID': [
        MVAVar("LepGood_mediumMuonId",lambda x: x.mediumMuonId),
        MVAVar("LepGood_segmentCompatibility",lambda x: x.segmentCompatibility),
        ],
    'SoftJetLessMuMVAID': [
        MVAVar("LepGood_trackerLayers",lambda x: x.trackerLayers),
        MVAVar("LepGood_pixelLayers",lambda x: x.pixelLayers),
        MVAVar("LepGood_innerTrackValidHitFraction",lambda x: x.innerTrackValidHitFraction),
        MVAVar("LepGood_trkKink := min(LepGood_trkKink,400)",lambda x: min(x.trkKink,400)),
        MVAVar("LepGood_chi2LocalPosition",lambda x: x.chi2LocalPosition),
        MVAVar("LepGood_segmentCompatibility",lambda x: x.segmentCompatibility),
        ],
    'SoftJetLessIVFMuMVAID': [
        MVAVar("LepGood_trackerLayers",lambda x: x.trackerLayers),
        MVAVar("LepGood_pixelLayers",lambda x: x.pixelLayers),
        MVAVar("LepGood_innerTrackValidHitFraction",lambda x: x.innerTrackValidHitFraction),
        MVAVar("LepGood_trkKink := min(LepGood_trkKink,400)",lambda x: min(x.trkKink,400)),
        MVAVar("LepGood_chi2LocalPosition",lambda x: x.chi2LocalPosition),
        MVAVar("LepGood_segmentCompatibility",lambda x: x.segmentCompatibility),
        ],
    'SoftALaMoriond16': [
        MVAVar("LepGood_segmentCompatibility",lambda x: x.segmentCompatibility)
        ],
    }

class LeptonMVA:
    def __init__(self,basepath,training="forMoriond16"):
        global _CommonVars, _CommonSpect, _ElectronVars, _MuonVars, _SVVars
        if type(basepath) == tuple: basepathmu, basepathel  = basepath
        else:                       basepathmu, basepathel  = basepath, basepath
        print "Booking %s %s" % (training, basepath)
        muVars = _CommonVars[training][:] + _MuonVars[training][:]
        elVars = _CommonVars[training][:] + _ElectronVars[:]
        if not muVars:
            self.mu = lambda mu, ncorr : -37.0;
        else:
            self.mu = CategorizedMVA([
                ( lambda x: True , MVATool("BDTG",basepathmu%"mu",_CommonSpect[training],muVars) ),
            ])
        if not elVars:
            self.el = lambda el, ncorr : -37.0;
        else:
            self.el = CategorizedMVA([
                ( lambda x: True, MVATool("BDTG",basepathel%"el",_CommonSpect[training],elVars) ),
            ])
    def __call__(self,lep,ncorr=0):
        if   abs(lep.pdgId) == 11: return self.el(lep,ncorr)
        elif abs(lep.pdgId) == 13: return self.mu(lep,ncorr)
        else: return -99

class LepMVAFriend:
    def __init__(self,path,training="forMoriond16",label="",fast=True):
        self.mva = LeptonMVA(path+"/%s_BDTG.weights.xml" if type(path) == str else path, training=training)
        self.fast = fast
        self.label = label
        print 'done init',training
    def listBranches(self):
        return [ ("nLepGood","I"), ("LepGood_mva"+self.label,"F",8,"nLepGood") ]
    def __call__(self,event):
        lep = Collection(event,"LepGood","nLepGood",8)
        ret = { 'nLepGood' : event.nLepGood }
        if event.run >= 1: # DATA
            ret['LepGood_mva'+self.label] = [ self.mva(l, ncorr=0) for l in lep ] 
        else:              # MC
            ret['LepGood_mva'+self.label] = [ self.mva(l, ncorr=0) for l in lep ] 
        return ret

if __name__ == '__main__':
    from sys import argv
    file = ROOT.TFile(argv[1])
    tree = file.Get("tree")
    if len(argv) > 2: tree.AddFriend("sf/t",argv[2])
    tree.vectorTree = True
    class Tester(Module):
        def __init__(self, name, trees="new"):
            Module.__init__(self,name,None)
            self.mvas = {
                'forMoriond16' : LepMVAFriend(("/afs/cern.ch/user/p/peruzzi/work/cmgtools/CMSSW_7_4_14/src/CMGTools/TTHAnalysis/macros/leptons/weights/forMoriond16%s_BDTG.weights.xml",
                                               "/afs/cern.ch/user/p/peruzzi/work/cmgtools/CMSSW_7_4_14/src/CMGTools/TTHAnalysis/macros/leptons/weights/forMoriond16%s_BDTG.weights.xml",),
                                              training="forMoriond16"),
            }
        def analyze(self,ev):
            print "\nrun %6d lumi %4d event %d: leps %d" % (ev.run, ev.lumi, ev.evt, ev.nLepGood)
            lep = Collection(ev,"LepGood","nLepGood",8)
            for l,m in self.mvas.iteritems():
                print "%-10s: %s %s" % (l, m(ev), [ x.mvaTTH for x in lep ] )
    el = EventLoop([ Tester("tester", "new") ])
    el.loop([tree], maxEvents = 50)

        
