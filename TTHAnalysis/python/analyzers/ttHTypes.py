#!/bin/env python
from math import *
from PhysicsTools.Heppy.analyzers.core.autovars import NTupleObjectType  
from PhysicsTools.Heppy.analyzers.objects.autophobj import  *
from PhysicsTools.HeppyCore.utils.deltar import deltaR

from CMGTools.TTHAnalysis.signedSip import *
from CMGTools.TTHAnalysis.tools.functionsTTH import _ttH_idEmu_cuts_E2_obj,_soft_MuonId_2016ICHEP,_medium_MuonId_2016ICHEP

##------------------------------------------  
## LEPTON
##------------------------------------------  

leptonTypeSusy = NTupleObjectType("leptonSusy", baseObjectTypes = [ leptonType ], variables = [
    # Lepton MVA-id related variables
    NTupleVariable("mvaTTH",    lambda lepton : getattr(lepton, 'mvaValueTTH', -1), help="Lepton MVA (TTH version)"),
    NTupleVariable("mvaSUSY",    lambda lepton : getattr(lepton, 'mvaValueSUSY', -1), help="Lepton MVA (SUSY version)"),
    NTupleVariable("jetPtRatiov2", lambda lepton: lepton.pt()/jetLepAwareJEC(lepton).Pt() if hasattr(lepton,'jet') else -1, help="pt(lepton)/[rawpt(jet-PU-lep)*L2L3Res+pt(lepton)]"),
    NTupleVariable("jetPtRelv2", lambda lepton : ptRelv2(lepton) if hasattr(lepton,'jet') else -1, help="pt of the lepton transverse to the jet axis (subtracting the lepton) - v2"),
    NTupleVariable("jetBTagCSV", lambda lepton : lepton.jet.btag('pfCombinedInclusiveSecondaryVertexV2BJetTags') if hasattr(lepton,'jet') and hasattr(lepton.jet, 'btag') else -99, help="CSV btag of nearest jet"),
    NTupleVariable("jetBTagDeepCSV", lambda lepton : (lambda x: -99 if isnan(x) else x)(lepton.jet.btag('pfDeepCSVJetTags:probb')+lepton.jet.btag('pfDeepCSVJetTags:probbb') if hasattr(lepton,'jet') and hasattr(lepton.jet, 'btag') else -99), help="DeepCSV btag of nearest jet, BvsAll = b+bb"),
    NTupleVariable("jetBTagDeepCSVCvsB", lambda lepton : (lambda x: -99 if isnan(x) else x)((lepton.jet.btag('pfDeepCSVJetTags:probc')/(lepton.jet.btag('pfDeepCSVJetTags:probc')+lepton.jet.btag('pfDeepCSVJetTags:probb')+lepton.jet.btag('pfDeepCSVJetTags:probbb'))) if hasattr(lepton,'jet') and hasattr(lepton.jet, 'btag') else -99), help="DeepCSV btag of nearest jet, CvsB = c/(c+b+bb)"),
    NTupleVariable("jetBTagDeepCSVCvsL", lambda lepton : (lambda x: -99 if isnan(x) else x)((lepton.jet.btag('pfDeepCSVJetTags:probc')/(lepton.jet.btag('pfDeepCSVJetTags:probc')+lepton.jet.btag('pfDeepCSVJetTags:probudsg'))) if hasattr(lepton,'jet') and hasattr(lepton.jet, 'btag') else -99), help="DeepCSV btag of nearest jet, CvsL = c/(c+udsg)"),
    NTupleVariable("miniRelIsoCharged",   lambda x : getattr(x,'miniAbsIsoCharged',-99)/x.pt()),
    NTupleVariable("miniRelIsoNeutral",   lambda x : getattr(x,'miniAbsIsoNeutral',-99)/x.pt()),
    NTupleVariable("jetNDauChargedMVASel",    lambda lepton : sum((deltaR(x.eta(),x.phi(),lepton.eta(),lepton.phi())<=0.4 and x.charge()!=0 and x.fromPV()>1 and x.hasTrackDetails() and qualityTrk(x.pseudoTrack(),lepton.associatedVertex)) for x in lepton.jet.daughterPtrVector()) if hasattr(lepton,'jet') and lepton.jet != lepton else 0, help="n charged daughters (with selection for ttH lepMVA) of nearest jet"),
    # More ID
    NTupleVariable("chargedHadRelIso04",  lambda x : x.chargedHadronIso(0.4)/x.pt(), help="PF Rel Iso, R=0.4, charged hadrons only"),
    NTupleVariable("trackerLayers", lambda x : (x.track() if abs(x.pdgId())==13 else x.gsfTrack()).hitPattern().trackerLayersWithMeasurement(), int, help="Tracker Layers"),
    NTupleVariable("pixelLayers", lambda x : (x.track() if abs(x.pdgId())==13 else x.gsfTrack()).hitPattern().pixelLayersWithMeasurement(), int, help="Pixel Layers"),
    NTupleVariable("chargeConsistency",  lambda lepton : ( lepton.isGsfCtfScPixChargeConsistent() + lepton.isGsfScPixChargeConsistent() ) if abs(lepton.pdgId()) == 11 else abs(lepton.muonBestTrack().charge() + lepton.innerTrack().charge() + lepton.tunePMuonBestTrack().charge() + ( lepton.globalTrack().charge() + lepton.outerTrack().charge() if lepton.isGlobalMuon() else 0) ), int, help="Tight charge criteria: for electrons, 2 if isGsfCtfScPixChargeConsistent, 1 if only isGsfScPixChargeConsistent, 0 otherwise; for muons, absolute value of the sum of all the charges (5 for global-muons, 3 for global muons)"),
    NTupleVariable("ptErrTk",  lambda lepton : ( lepton.gsfTrack().ptError() ) if abs(lepton.pdgId()) == 11 else (lepton.muonBestTrack().ptError()), help="pt error, for the gsf track or muon best track"),
    # More ID: muons
    NTupleVariable("nStations",    lambda lepton : lepton.numberOfMatchedStations() if abs(lepton.pdgId()) == 13 else 4, help="Number of matched muons stations (4 for electrons)"),
    NTupleVariable("segmentCompatibility", lambda lepton : lepton.segmentCompatibility() if abs(lepton.pdgId()) == 13 else 0, help="Segment-based compatibility"), 
    NTupleVariable("softMuonId", lambda x : x.muonID("POG_ID_Soft") if abs(x.pdgId())==13 else 1, int, help="Muon POG Soft id"),
    NTupleVariable("softMuonId2016", lambda lepton: _soft_MuonId_2016ICHEP(lepton), help="Soft muon ID retuned for ICHEP 2016"),
    NTupleVariable("mediumMuonID2016", lambda lepton: _medium_MuonId_2016ICHEP(lepton), help="Medium muon ID retuned for ICHEP 2016"),
    NTupleVariable("muonTrackType",  lambda lepton : 1 if abs(lepton.pdgId()) == 11 else lepton.muonBestTrackType(), int, help="Muon best track type"),
    # More ID: electrons
    NTupleVariable("mvaIdSpring16HZZ",   lambda lepton : lepton.mvaRun2("Spring16HZZ") if abs(lepton.pdgId()) == 11 else 1, help="EGamma POG MVA ID, Spring16, HZZ; 1 for muons"),
    NTupleVariable("mvaIdSpring16GP",   lambda lepton : lepton.mvaRun2("Spring16GP") if abs(lepton.pdgId()) == 11 else 1, help="EGamma POG MVA ID, Spring16, GeneralPurpose; 1 for muons"),
    NTupleVariable("mvaIdFall17noIso",   lambda lepton : lepton.mvaRun2("Fall17noIso") if abs(lepton.pdgId()) == 11 else 1, help="EGamma POG MVA ID, Fall17 training, without isolation; 1 for muons"),
    NTupleVariable("mvaIdFall17Iso",   lambda lepton : lepton.mvaRun2("Fall17Iso") if abs(lepton.pdgId()) == 11 else 1, help="EGamma POG MVA ID, Fall17 training, with isolation; 1 for muons"),
    NTupleVariable("r9",      lambda lepton : lepton.full5x5_r9() if abs(lepton.pdgId()) == 11 else -99, help="SuperCluster 5x5 r9 variable, only for electrons; -99 for muons"),
    NTupleVariable("sigmaIEtaIEta",  lambda x : x.full5x5_sigmaIetaIeta() if abs(x.pdgId())==11 else 0, help="Electron sigma(ieta ieta), with full5x5 cluster shapes"),
    NTupleVariable("dEtaScTrkIn",    lambda x : x.deltaEtaSuperClusterTrackAtVtx() if abs(x.pdgId())==11 else 0, help="Electron deltaEtaSuperClusterTrackAtVtx (without absolute value!)"),
    NTupleVariable("dPhiScTrkIn",    lambda x : x.deltaPhiSuperClusterTrackAtVtx() if abs(x.pdgId())==11 else 0, help="Electron deltaPhiSuperClusterTrackAtVtx (without absolute value!)"),
    NTupleVariable("hadronicOverEm", lambda x : x.hadronicOverEm() if abs(x.pdgId())==11 else 0, help="Electron hadronicOverEm"),
    NTupleVariable("eInvMinusPInv",  lambda x : ((1.0/x.ecalEnergy() - x.eSuperClusterOverP()/x.ecalEnergy()) if x.ecalEnergy()>0. else 9e9) if abs(x.pdgId())==11 else 0, help="Electron 1/E - 1/p  (without absolute value!)"),
    NTupleVariable("eInvMinusPInv_tkMom", lambda x: ((1.0/x.ecalEnergy()) - (1.0 / x.trackMomentumAtVtx().R() ) if (x.ecalEnergy()>0. and x.trackMomentumAtVtx().R()>0.) else 9e9) if abs(x.pdgId())==11 else 0, help="Electron 1/E - 1/p_tk_vtx  (without absolute value!)"),
    NTupleVariable("ecalPFClusterIso", lambda lepton :  lepton.ecalPFClusterIso() if abs(lepton.pdgId())==11 else -999, help="Electron ecalPFClusterIso"),
    NTupleVariable("hcalPFClusterIso", lambda lepton :  lepton.hcalPFClusterIso() if abs(lepton.pdgId())==11 else -999, help="Electron hcalPFClusterIso"),
    NTupleVariable("dr03TkSumPt", lambda lepton: lepton.dr03TkSumPt() if abs(lepton.pdgId())==11 else -999, help="Electron dr03TkSumPt isolation"),
    NTupleVariable("trackIso", lambda lepton :  lepton.trackIso() if abs(lepton.pdgId())==11 else -999, help="Electron trackIso (in cone of 0.4)"),
    NTupleVariable("etaSc", lambda x : x.superCluster().eta() if abs(x.pdgId())==11 else -100, help="Electron supercluster pseudorapidity"),
    NTupleVariable("energySc", lambda x : x.superCluster().energy() if abs(x.pdgId())==11 else -100, help="Electron supercluster pseudorapidity"),
    NTupleVariable("idEmuTTH", lambda lepton: _ttH_idEmu_cuts_E2_obj(lepton), help="Electron pass trigger ID emulation cuts (TTH, E2)"),
    # More: MC
    NTupleVariable("mcMatchPdgId",  lambda x : x.mcLep.pdgId() if getattr(x,'mcLep',None)!=None else -99, int, mcOnly=True, help="Match to source from hard scatter (pdgId of heaviest particle in chain, 25 for H, 6 for t, 23/24 for W/Z): pdgId of the matched gen-level lepton, zero if non-prompt or fake"),
    NTupleVariable("mcPrompt",    lambda x : x.mcMatchAny_gp.isPromptFinalState() if getattr(x,"mcMatchAny_gp",None) else 0, int, mcOnly=True, help="isPromptFinalState"),
    NTupleVariable("mcPromptTau", lambda x : x.mcMatchAny_gp.isDirectPromptTauDecayProductFinalState() if getattr(x,"mcMatchAny_gp",None) else 0, int, mcOnly=True, help="isDirectPromptTauDecayProductFinalState"),
    NTupleVariable("mcPromptGamma", lambda x : x.mcPho.isPromptFinalState() if getattr(x,"mcPho",None) else 0, int, mcOnly=True, help="Photon isPromptFinalState"),
    NTupleVariable("mcGamma", lambda x : getattr(x,"mcPho",None) != None, int, mcOnly=True, help="Matched to a photon"),
])
leptonTypeSusy.removeVariable("relIsoAn04")
leptonTypeSusy.removeVariable("eleCutIdSpring15_25ns_v1")
leptonTypeSusy.removeVariable("ICHEPsoftMuonId")
leptonTypeSusy.removeVariable("ICHEPmediumMuonId")

leptonTypeSusy.addSubObjects([
    NTupleSubObject("jetLepAwareJEC",lambda x: jetLepAwareJEC(x), tlorentzFourVectorType)
])


##------------------------------------------  
## TAU
##------------------------------------------  

tauTypeSusy = NTupleObjectType("tauSusy",  baseObjectTypes = [ tauType ], variables = [
     NTupleVariable("idMVAdR03", lambda x : x.idMVAdR03, int, help="1,2,3,4,5,6 if the tau passes the very loose to very very tight WP of the IsolationMVArun2v1DBdR03oldDMwLT discriminator"),
     NTupleVariable("mvaId2017", lambda x : getattr(x,'mvaId2017',-99), float, help="2017 tau ID MVA discriminator score"),
])
tauTypeSusy.removeVariable("idMVANewDM")
tauTypeSusy.removeVariable("idCI3hit")



jetTypeSusy = NTupleObjectType("jetSusy",  baseObjectTypes = [ jetTypeExtra ], variables = [
  # NTupleVariable("charge", lambda x : x.jetCharge(), float, help="Jet charge"), 
    NTupleVariable("btagDeepCSVCvsB", lambda x : (lambda y : -99 if isnan(y) else y)(x.btag('pfDeepCSVJetTags:probc')/(x.btag('pfDeepCSVJetTags:probc')+x.btag('pfDeepCSVJetTags:probb')+x.btag('pfDeepCSVJetTags:probbb'))), help="DeepCSV discriminator, CvsB = c/(c+b+bb)"),
    NTupleVariable("btagDeepCSVCvsL", lambda x : (lambda y : -99 if isnan(y) else y)(x.btag('pfDeepCSVJetTags:probc')/(x.btag('pfDeepCSVJetTags:probc')+x.btag('pfDeepCSVJetTags:probudsg'))), help="DeepCSV discriminator, CvsL = c/(c+udsg)"),
    NTupleVariable("ctagCsvL", lambda x : x.btag('pfCombinedCvsLJetTags'), float, help="CsvL discriminator"),
    NTupleVariable("chHEF", lambda x : x.chargedHadronEnergyFraction(), float, mcOnly = False, help="chargedHadronEnergyFraction (relative to uncorrected jet energy)"),
    NTupleVariable("neHEF", lambda x : x.neutralHadronEnergyFraction(), float, mcOnly = False,help="neutralHadronEnergyFraction (relative to uncorrected jet energy)"),
 #  NTupleVariable("CorrFactor_L1", lambda x: x.CorrFactor_L1 if hasattr(x,'CorrFactor_L1') else 0, help="L1 correction factor"),
 #  NTupleVariable("CorrFactor_L1L2", lambda x: x.CorrFactor_L1L2 if hasattr(x,'CorrFactor_L1L2') else 0, help="L1L2 correction factor"),
 #  NTupleVariable("CorrFactor_L1L2L3", lambda x: x.CorrFactor_L1L2L3 if hasattr(x,'CorrFactor_L1L2L3') else 0, help="L1L2L3 correction factor"),
 #  NTupleVariable("CorrFactor_L1L2L3Res", lambda x: x.CorrFactor_L1L2L3Res if hasattr(x,'CorrFactor_L1L2L3Res') else 0, help="L1L2L3Res correction factor"),
    NTupleVariable("mcMatchFlav",  lambda x : getattr(x,'mcMatchFlav',-99), int, mcOnly=True, help="Flavour of associated parton from hard scatter (if any)"),
])
jetTypeSusy.removeVariable("btagCMVA")
jetTypeSusy.removeVariable("nLeptons")

jetTypeSusyFwd = NTupleObjectType("jetFwd",  baseObjectTypes = [ jetType ], variables = [
    NTupleVariable("chHEF", lambda x : x.chargedHadronEnergyFraction(), float, mcOnly = False, help="chargedHadronEnergyFraction (relative to uncorrected jet energy)"),
    NTupleVariable("neHEF", lambda x : x.neutralHadronEnergyFraction(), float, mcOnly = False,help="neutralHadronEnergyFraction (relative to uncorrected jet energy)"),
    NTupleVariable("mcMatchFlav",  lambda x : getattr(x,'mcMatchFlav',-99), int, mcOnly=True, help="Flavour of associated parton from hard scatter (if any)"),
])
jetTypeSusy.removeVariable("btagCMVA")
jetTypeSusyFwd.removeVariable("nLeptons")

##------------------------------------------  
## MET
##------------------------------------------  
  
metTypeSusy = NTupleObjectType("metSusy", baseObjectTypes = [ metType ], variables = [
])

def ptRel(p4,axis):
    a = ROOT.TVector3(axis.Vect().X(),axis.Vect().Y(),axis.Vect().Z())
    o = ROOT.TLorentzVector(p4.Px(),p4.Py(),p4.Pz(),p4.E())
    return o.Perp(a)
def ptRelv1(p4,axis):
    axis = axis - p4
    a = ROOT.TVector3(axis.Vect().X(),axis.Vect().Y(),axis.Vect().Z())
    o = ROOT.TLorentzVector(p4.Px(),p4.Py(),p4.Pz(),p4.E())
    return o.Perp(a)
def jetLepAwareJEC(lep): # use only if jetAna.calculateSeparateCorrections==True
    p4l = lep.p4()
    l = ROOT.TLorentzVector(p4l.Px(),p4l.Py(),p4l.Pz(),p4l.E())
    if not hasattr(lep.jet,'rawFactor'): return l # if lep==jet (matched to lepton object itself)
    p4j = lep.jet.p4()
    j = ROOT.TLorentzVector(p4j.Px(),p4j.Py(),p4j.Pz(),p4j.E())
    if ((j*lep.jet.rawFactor()-l).Rho()<1e-4): return l # matched to jet containing only the lepton
    j = (j*lep.jet.rawFactor()-l*(1.0/lep.jet.l1corrFactor()))*lep.jet.corrFactor()+l
    return j
def ptRelv2(lep): # use only if jetAna.calculateSeparateCorrections==True
    m = jetLepAwareJEC(lep)
    p4l = lep.p4()
    l = ROOT.TLorentzVector(p4l.Px(),p4l.Py(),p4l.Pz(),p4l.E())
    if ((m-l).Rho()<1e-4): return 0 # lep.jet==lep (no match) or jet containing only the lepton
    return l.Perp((m-l).Vect())
def ptRelHv2(lep): # use only if jetAna.calculateSeparateCorrections==True
    m = jetLepAwareJEC(lep)
    p4l = lep.p4()
    l = ROOT.TLorentzVector(p4l.Px(),p4l.Py(),p4l.Pz(),p4l.E())
    return (m-l).Perp(l.Vect())
def isoRelH(lep,tag):
    iso = getattr(lep,'isoSumRawP4Charged'+tag)+getattr(lep,'isoSumRawP4Neutral'+tag)
    p4l = lep.p4()
    l = ROOT.TLorentzVector(p4l.Px(),p4l.Py(),p4l.Pz(),p4l.E())
    m = ROOT.TLorentzVector(iso.Px(),iso.Py(),iso.Pz(),iso.E())
    return m.Perp(l.Vect())
def jetBasedRelIsoCharged(lep):
    if not hasattr(lep.jet,'rawFactor'): return 0
    return lep.jet.pt()*lep.jet.rawFactor()*lep.jet.chargedHadronEnergyFraction()/lep.pt()
