from array import array
from math import *
from CMGTools.TTHAnalysis.analyzers.ntupleTypes import ptRelv2, jetLepAwareJEC, isoRelH
from PhysicsTools.HeppyCore.utils.deltar import deltaR
from CMGTools.TTHAnalysis.signedSip import qualityTrk

import ROOT
#import os
#if "/smearer_cc.so" not in ROOT.gSystem.GetLibraries(): 
#    ROOT.gROOT.ProcessLine(".L %s/src/CMGTools/TTHAnalysis/python/plotter/smearer.cc+" % os.environ['CMSSW_BASE']);
#if "/mcCorrections_cc.so" not in ROOT.gSystem.GetLibraries(): 
#    ROOT.gROOT.ProcessLine(".L %s/src/CMGTools/TTHAnalysis/python/plotter/mcCorrections.cc+" % os.environ['CMSSW_BASE']);


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
                self.var[0] = self.corrfunc(self.var[0], lep.pdgId(),lep.pt(),lep.eta(),lep.mcMatchId,lep.mcMatchAny)
class MVATool:
    def __init__(self,name,xml,specs,vars):
        self.name = name
        self.reader = ROOT.TMVA.Reader("Silent")
        self.specs = specs
        self.vars  = vars
        for s in specs: self.reader.AddSpectator(s.name,s.var)
        for v in vars:  self.reader.AddVariable(v.name,v.var)
        #print "Would like to load %s from %s! " % (name,xml)
        self.reader.BookMVA(name,xml)
    def __call__(self,lep,ncorr): ## apply correction ncorr times
        for s in self.specs: s.set(lep,ncorr)
        for s in self.vars:  s.set(lep,ncorr)
        return self.reader.EvaluateMVA(self.name)   
class CategorizedMVA:
    def __init__(self,catMvaPairs):
        self.catMvaPairs = catMvaPairs
    def __call__(self,lep,ncorr):
        for c,m in self.catMvaPairs:
            if c(lep): return m(lep,ncorr)
        return -99.

_CommonSpect = {
 'forMoriond': [],
 'SoftJetLessNOBTAG': [
    MVAVar("LepGood_mcMatchAny",lambda x: getattr(x,'mcMatchAny',-999)),
  ],
}
_CommonSpect['forMoriond_eleOLD'] = _CommonSpect['forMoriond']
_CommonSpect['forMoriond_eleHZZ'] = _CommonSpect['forMoriond']
_CommonSpect['forMoriond_eleGP'] = _CommonSpect['forMoriond']
_CommonSpect['training2017'] = _CommonSpect['forMoriond']

_CommonVars = {
 'forMoriond':[ 
    MVAVar("LepGood_pt",lambda x: x.pt()),
    MVAVar("LepGood_eta",lambda x: x.eta()),
    MVAVar("LepGood_jetNDauChargedMVASel",lambda lepton: sum((deltaR(x.eta(),x.phi(),lepton.eta(),lepton.phi())<=0.4 and x.charge()!=0 and x.fromPV()>1 and x.hasTrackDetails() and qualityTrk(x.pseudoTrack(),lepton.associatedVertex)) for x in lepton.jet.daughterPtrVector()) if hasattr(lepton,'jet') and lepton.jet != lepton else 0),
    MVAVar("LepGood_miniRelIsoCharged",lambda x: getattr(x,'miniAbsIsoCharged',-99)/x.pt()), 
    MVAVar("LepGood_miniRelIsoNeutral",lambda x: getattr(x,'miniAbsIsoNeutral',-99)/x.pt()), 
    MVAVar("LepGood_jetPtRelv2", lambda x : ptRelv2(x) if hasattr(x,'jet') else -1),
    MVAVar("LepGood_jetPtRatio := min(LepGood_jetPtRatiov2,1.5)", lambda x : min((x.pt()/jetLepAwareJEC(x).Pt() if hasattr(x,'jet') else -1), 1.5)),
    MVAVar("LepGood_jetBTagCSV := max(LepGood_jetBTagCSV,0)", lambda x : max( (x.jet.btag('pfCombinedInclusiveSecondaryVertexV2BJetTags') if hasattr(x.jet, 'btag') else -99) ,0.)),
    MVAVar("LepGood_sip3d",lambda x: x.sip3D()),
    MVAVar("LepGood_dxy := log(abs(LepGood_dxy))",lambda x: log(abs(x.dxy()))),
    MVAVar("LepGood_dz  := log(abs(LepGood_dz))", lambda x: log(abs(x.dz()))),
 ],
 'SoftJetLessNOBTAG': [
    MVAVar("LepGood_pt",lambda x: x.pt()),
    MVAVar("LepGood_eta",lambda x: x.eta()),
    MVAVar("LepGood_miniRelIsoCharged := min(LepGood_miniRelIsoCharged,4)",lambda x: min(getattr(x,'miniAbsIsoCharged',-99)/x.pt(),4)),
    MVAVar("LepGood_miniRelIsoNeutral := min(LepGood_miniRelIsoNeutral,4)",lambda x: min(getattr(x,'miniAbsIsoNeutral',-99)/x.pt(),4)),
    MVAVar("LepGood_isoRelH04",lambda x: isoRelH(x,'04') if hasattr(x,'isoSumRawP4Charged04') else -1),
    MVAVar("LepGood_RelIsoChargedFix04 := min(LepGood_RelIsoChargedFix04,4)",lambda x: min(getattr(x,'AbsIsoMIVCharged04',-99)/x.pt(),4)),
    MVAVar("LepGood_RelIsoNeutralFix04 := min(LepGood_RelIsoNeutralFix04,4)",lambda x: min(getattr(x,'AbsIsoMIVNeutral04',-99)/x.pt(),4)),
    MVAVar("LepGood_sip3d",lambda x: x.sip3D()),
    MVAVar("LepGood_dxy := log(abs(LepGood_dxy))",lambda x: log(abs(x.dxy()))),
    MVAVar("LepGood_dz  := log(abs(LepGood_dz))", lambda x: log(abs(x.dz()))),
 ],
 'training2017':[
    MVAVar("LepGood_pt",lambda x: x.pt()),
    MVAVar("LepGood_eta",lambda x: x.eta()),
    MVAVar("LepGood_jetNDauChargedMVASel",lambda lepton: sum((deltaR(x.eta(),x.phi(),lepton.jet.eta(),lepton.jet.phi())<=0.4 and x.charge()!=0 and x.fromPV()>1 and x.hasTrackDetails() and qualityTrk(x.pseudoTrack(),lepton.associatedVertex)) for x in lepton.jet.daughterPtrVector()) if hasattr(lepton,'jet') and lepton.jet != lepton else 0),
    MVAVar("LepGood_miniRelIsoCharged",lambda x: getattr(x,'miniAbsIsoCharged',-99)/x.pt()),
    MVAVar("LepGood_miniRelIsoNeutral",lambda x: getattr(x,'miniAbsIsoNeutral',-99)/x.pt()),
    MVAVar("LepGood_jetPtRelv2", lambda x : ptRelv2(x) if hasattr(x,'jet') else -1),
    MVAVar("LepGood_jetBTagCSV := max(LepGood_jetBTagCSV,0)", lambda x : max( (x.jet.btag('pfCombinedInclusiveSecondaryVertexV2BJetTags') if hasattr(x.jet, 'btag') else -99) ,0.)),
    MVAVar("LepGood_jetPtRatiov2 := (LepGood_jetBTagCSV>-5)*min(LepGood_jetPtRatiov2,1.5)+(LepGood_jetBTagCSV<-5)/(1+LepGood_relIso04)", lambda x : min(x.pt()/jetLepAwareJEC(x).Pt(),1.5) if hasattr(x,'jet') else 1./(1.+x.relIso04)),
    MVAVar("LepGood_sip3d",lambda x: x.sip3D()),
    MVAVar("LepGood_dxy := log(abs(LepGood_dxy))",lambda x: log(abs(x.dxy()))),
    MVAVar("LepGood_dz  := log(abs(LepGood_dz))", lambda x: log(abs(x.dz()))),
 ],
}
_CommonVars['forMoriond_eleOLD'] = _CommonVars['forMoriond']
_CommonVars['forMoriond_eleHZZ'] = _CommonVars['forMoriond']
_CommonVars['forMoriond_eleGP'] = _CommonVars['forMoriond']

_MuonVars = {
 'forMoriond': [
    MVAVar("LepGood_segmentCompatibility",lambda x: x.segmentCompatibility()), 
 ],
 'SoftJetLessNOBTAG': [
    MVAVar("LepGood_segmentCompatibility",lambda x: x.segmentCompatibility()), 
 ],
}
_MuonVars['forMoriond_eleOLD'] = _MuonVars['forMoriond']
_MuonVars['forMoriond_eleHZZ'] = _MuonVars['forMoriond']
_MuonVars['forMoriond_eleGP'] = _MuonVars['forMoriond']
_MuonVars['training2017'] = _MuonVars['forMoriond']


_ElectronVars = {
 'forMoriond_eleOLD': [
    MVAVar("LepGood_mvaIdSpring15",lambda x: x.mvaRun2("NonTrigSpring15MiniAOD")),
 ],
 'forMoriond_eleHZZ': [
    MVAVar("LepGood_mvaIdSpring16HZZ",lambda x: x.mvaRun2("Spring16HZZ")),
 ],
 'forMoriond_eleGP': [
    MVAVar("LepGood_mvaIdSpring16GP",lambda x: x.mvaRun2("Spring16GP")),
 ],
 'SoftJetLessNOBTAG': [
    MVAVar("LepGood_mvaIdSpring15",lambda x: x.mvaRun2("NonTrigSpring15MiniAOD")),
 ],
 'training2017': [
    MVAVar("LepGood_mvaIdFall17noIso",lambda x: x.mvaRun2("Fall17noIso")),
 ],
}


class LeptonMVA:
    def __init__(self, kind, basepath, isMC):
        global _CommonVars, _CommonSpect, _ElectronVars
        #print "Creating LeptonMVA of kind %s, base path %s" % (kind, basepath)
        self._isMC = isMC
        self._kind = kind
        muVars = _CommonVars[kind] + _MuonVars[kind]
        elVars = _CommonVars[kind] + _ElectronVars[kind]
        if ('forMoriond' in self._kind) or ('SoftJetLessNOBTAG' in self._kind) or ('training2017' in self._kind):
            self.mu = CategorizedMVA([
                    ( lambda x: True, MVATool("BDTG",basepath%"mu",_CommonSpect[kind],muVars) ),
                    ])
            self.el = CategorizedMVA([
                    ( lambda x: True, MVATool("BDTG",basepath%"el",_CommonSpect[kind],elVars) ),
                    ])            
        else:
            self.mu = CategorizedMVA([
                    ( lambda x: abs(x.eta()) <  1.5, MVATool("BDTG",basepath%"mu_eta_b",_CommonSpect[kind],muVars) ),
                    ( lambda x: abs(x.eta()) >= 1.5, MVATool("BDTG",basepath%"mu_eta_e",_CommonSpect[kind],muVars) ),
                    ])
            self.el = CategorizedMVA([
                    ( lambda x: abs(x.eta()) <  0.8                          , MVATool("BDTG",basepath%"el_eta_cb",_CommonSpect[kind],elVars) ),
                    ( lambda x: abs(x.eta()) >= 0.8 and abs(x.eta()) <  1.479, MVATool("BDTG",basepath%"el_eta_fb",_CommonSpect[kind],elVars) ),
                    ( lambda x: abs(x.eta()) >= 1.479                        , MVATool("BDTG",basepath%"el_eta_ec",_CommonSpect[kind],elVars) ),
                    ])
    def __call__(self,lep,ncorr="auto"):
        if ncorr == "auto": ncorr = 0 # (1 if self._isMC else 0)
        if   abs(lep.pdgId()) == 11: return self.el(lep,ncorr)
        elif abs(lep.pdgId()) == 13: return self.mu(lep,ncorr)
        else: return -99

