#!/bin/env python
from math import *
from PhysicsTools.Heppy.analyzers.core.autovars import NTupleObjectType  
from PhysicsTools.Heppy.analyzers.objects.autophobj import  *
from PhysicsTools.HeppyCore.utils.deltar import deltaR

from CMGTools.TTHAnalysis.signedSip import *
from CMGTools.TTHAnalysis.tools.functionsTTH import _ttH_idEmu_cuts_E2_obj,_soft_MuonId_2016ICHEP,_medium_MuonId_2016ICHEP
from CMGTools.TTHAnalysis.tools.functionsRAX import _susy2lss_idEmu_cuts_obj,_susy2lss_idIsoEmu_cuts_obj
#from CMGTools.TTHAnalysis.tools.leptonChoiceRA5 import _susy2lss_idEmu_cuts_obj,_susy2lss_idIsoEmu_cuts_obj

##------------------------------------------  
## LEPTON
##------------------------------------------  

leptonTypeSusy = NTupleObjectType("leptonSusy", baseObjectTypes = [ leptonType ], variables = [
    NTupleVariable("mvaIdSpring15",   lambda lepton : lepton.mvaRun2("NonTrigSpring15MiniAOD") if abs(lepton.pdgId()) == 11 else 1, help="EGamma POG MVA ID for non-triggering electrons, Spring15 re-training; 1 for muons"),
    # Lepton MVA-id related variables
    NTupleVariable("mvaTTH",    lambda lepton : getattr(lepton, 'mvaValueTTH', -1), help="Lepton MVA (TTH version)"),
    NTupleVariable("mvaSUSY",    lambda lepton : getattr(lepton, 'mvaValueSUSY', -1), help="Lepton MVA (SUSY version)"),
    NTupleVariable("jetPtRatiov1", lambda lepton : lepton.pt()/lepton.jet.pt() if hasattr(lepton,'jet') else -1, help="pt(lepton)/pt(nearest jet)"),
    NTupleVariable("jetPtRelv1", lambda lepton : ptRelv1(lepton.p4(),lepton.jet.p4()) if hasattr(lepton,'jet') else -1, help="pt of the lepton transverse to the jet axis (subtracting the lepton)"),
    NTupleVariable("jetPtRatiov2", lambda lepton: lepton.pt()/jetLepAwareJEC(lepton).Pt() if hasattr(lepton,'jet') else -1, help="pt(lepton)/[rawpt(jet-PU-lep)*L2L3Res+pt(lepton)]"),
    NTupleVariable("jetPtRelv2", lambda lepton : ptRelv2(lepton) if hasattr(lepton,'jet') else -1, help="pt of the lepton transverse to the jet axis (subtracting the lepton) - v2"),
    NTupleVariable("jetBTagCSV", lambda lepton : lepton.jet.btag('pfCombinedInclusiveSecondaryVertexV2BJetTags') if hasattr(lepton,'jet') and hasattr(lepton.jet, 'btag') else -99, help="CSV btag of nearest jet"),
    NTupleVariable("jetBTagCMVA", lambda lepton : lepton.jet.btag('pfCombinedMVABJetTags') if hasattr(lepton,'jet') and hasattr(lepton.jet, 'btag') else -99, help="CMA btag of nearest jet"),
    NTupleVariable("jetBTagDeepCSV", lambda lepton : (lambda x: -99 if isnan(x) else x)(lepton.jet.btag('pfDeepCSVJetTags:probb')+lepton.jet.btag('pfDeepCSVJetTags:probbb') if hasattr(lepton,'jet') and hasattr(lepton.jet, 'btag') else -99), help="DeepCSV btag of nearest jet, BvsAll = b+bb"),
    NTupleVariable("jetBTagDeepCSVCvsB", lambda lepton : (lambda x: -99 if isnan(x) else x)((lepton.jet.btag('pfDeepCSVJetTags:probc')/(lepton.jet.btag('pfDeepCSVJetTags:probc')+lepton.jet.btag('pfDeepCSVJetTags:probb')+lepton.jet.btag('pfDeepCSVJetTags:probbb'))) if hasattr(lepton,'jet') and hasattr(lepton.jet, 'btag') else -99), help="DeepCSV btag of nearest jet, CvsB = c/(c+b+bb)"),
    NTupleVariable("jetBTagDeepCSVCvsL", lambda lepton : (lambda x: -99 if isnan(x) else x)((lepton.jet.btag('pfDeepCSVJetTags:probc')/(lepton.jet.btag('pfDeepCSVJetTags:probc')+lepton.jet.btag('pfDeepCSVJetTags:probudsg'))) if hasattr(lepton,'jet') and hasattr(lepton.jet, 'btag') else -99), help="DeepCSV btag of nearest jet, CvsL = c/(c+udsg)"),
    NTupleVariable("jetDR",      lambda lepton : deltaR(lepton.eta(),lepton.phi(),lepton.jet.eta(),lepton.jet.phi()) if hasattr(lepton,'jet') else -1, help="deltaR(lepton, nearest jet)"),
    NTupleVariable("r9",      lambda lepton : lepton.full5x5_r9() if abs(lepton.pdgId()) == 11 else -99, help="SuperCluster 5x5 r9 variable, only for electrons; -99 for muons"),
    #2016 muon Id
    NTupleVariable("softMuonId2016", lambda lepton: _soft_MuonId_2016ICHEP(lepton), help="Soft muon ID retuned for ICHEP 2016"),
    NTupleVariable("mediumMuonID2016", lambda lepton: _medium_MuonId_2016ICHEP(lepton), help="Medium muon ID retuned for ICHEP 2016"),
    # More
    NTupleVariable("tightChargeFix",  lambda lepton : ( lepton.isGsfCtfScPixChargeConsistent() + lepton.isGsfScPixChargeConsistent() ) if abs(lepton.pdgId()) == 11 else 2*(lepton.muonBestTrack().ptError()/lepton.muonBestTrack().pt() < 0.2), int, help="Tight charge criteria: for electrons, 2 if isGsfCtfScPixChargeConsistent, 1 if only isGsfScPixChargeConsistent, 0 otherwise; for muons, 2 if ptError/pt < 0.20, 0 otherwise (using the muon best track)"),
    NTupleVariable("muonTrackType",  lambda lepton : 1 if abs(lepton.pdgId()) == 11 else lepton.muonBestTrackType(), int, help="Muon best track type"),
    NTupleVariable("chargeConsistency",  lambda lepton : ( lepton.isGsfCtfScPixChargeConsistent() + lepton.isGsfScPixChargeConsistent() ) if abs(lepton.pdgId()) == 11 else abs(lepton.muonBestTrack().charge() + lepton.innerTrack().charge() + lepton.tunePMuonBestTrack().charge() + ( lepton.globalTrack().charge() + lepton.outerTrack().charge() if lepton.isGlobalMuon() else 0) ), int, help="Tight charge criteria: for electrons, 2 if isGsfCtfScPixChargeConsistent, 1 if only isGsfScPixChargeConsistent, 0 otherwise; for muons, absolute value of the sum of all the charges (5 for global-muons, 3 for global muons)"),
    NTupleVariable("ptErrTk",  lambda lepton : ( lepton.gsfTrack().ptError() ) if abs(lepton.pdgId()) == 11 else (lepton.muonBestTrack().ptError()), help="pt error, for the gsf track or muon best track"),
])


leptonTypeSusyExtraLight = NTupleObjectType("leptonSusyExtraLight", baseObjectTypes = [ leptonTypeSusy, leptonTypeExtra ], variables = [
    NTupleVariable("miniRelIsoCharged",   lambda x : getattr(x,'miniAbsIsoCharged',-99)/x.pt()),
    NTupleVariable("miniRelIsoNeutral",   lambda x : getattr(x,'miniAbsIsoNeutral',-99)/x.pt()),
    NTupleVariable("jetNDauChargedMVASel",    lambda lepton : sum((deltaR(x.eta(),x.phi(),lepton.eta(),lepton.phi())<=0.4 and x.charge()!=0 and x.fromPV()>1 and x.hasTrackDetails() and qualityTrk(x.pseudoTrack(),lepton.associatedVertex)) for x in lepton.jet.daughterPtrVector()) if hasattr(lepton,'jet') and lepton.jet != lepton else 0, help="n charged daughters (with selection for ttH lepMVA) of nearest jet"),
    NTupleVariable("jetCorrFactor_L1", lambda x: x.jet.CorrFactor_L1 if hasattr(x.jet,'CorrFactor_L1') else 1, help="matched jet L1 correction factor"),
    NTupleVariable("jetCorrFactor_L1L2", lambda x: x.jet.CorrFactor_L1L2 if hasattr(x.jet,'CorrFactor_L1L2') else 1, help="matched jet L1L2 correction factor"),
    NTupleVariable("jetCorrFactor_L1L2L3", lambda x: x.jet.CorrFactor_L1L2L3 if hasattr(x.jet,'CorrFactor_L1L2L3') else 1, help="matched jet L1L2L3 correction factor"),
    NTupleVariable("jetCorrFactor_L1L2L3Res", lambda x: x.jet.CorrFactor_L1L2L3Res if hasattr(x.jet,'CorrFactor_L1L2L3Res') else 1, help="matched jet L1L2L3Res correction factor"),        
    # variables for isolated electron trigger matching cuts
    NTupleVariable("ecalPFClusterIso", lambda lepton :  lepton.ecalPFClusterIso() if abs(lepton.pdgId())==11 else -999, help="Electron ecalPFClusterIso"),
    NTupleVariable("hcalPFClusterIso", lambda lepton :  lepton.hcalPFClusterIso() if abs(lepton.pdgId())==11 else -999, help="Electron hcalPFClusterIso"),
    NTupleVariable("dr03TkSumPt", lambda lepton: lepton.dr03TkSumPt() if abs(lepton.pdgId())==11 else -999, help="Electron dr03TkSumPt isolation"),
    NTupleVariable("trackIso", lambda lepton :  lepton.trackIso() if abs(lepton.pdgId())==11 else -999, help="Electron trackIso (in cone of 0.4)"),
    NTupleVariable("idEmuTTH", lambda lepton: _ttH_idEmu_cuts_E2_obj(lepton), help="Electron pass trigger ID emulation cuts (TTH, E2)"),
    NTupleVariable("idEmuRA5", lambda lepton: _susy2lss_idEmu_cuts_obj(lepton), help="Electron pass trigger ID emulation cuts (RA5)"),
    NTupleVariable("idIsoEmuRA5", lambda lepton: _susy2lss_idIsoEmu_cuts_obj(lepton), help="Electron pass trigger ID+ISO emulation cuts (RA5)"),
    NTupleVariable("SOSTightID2017", lambda lepton: (lepton.electronID("MVA_ID_nonIso_Fall17_wp90") if lepton.pt()<10 else lepton.electronID("MVA_ID_nonIso_Fall17_SUSYTight")) if abs(lepton.pdgId())==11 else 0, int, help="SOS tight electron MVA noIso ID 2017 (WP: POG wp90 below 10 GeV, SUSYTight above)"),
    NTupleVariable("mcPrompt",    lambda x : x.mcMatchAny_gp.isPromptFinalState() if getattr(x,"mcMatchAny_gp",None) else 0, int, mcOnly=True, help="isPromptFinalState"),
    NTupleVariable("mcPromptTau", lambda x : x.mcMatchAny_gp.isDirectPromptTauDecayProductFinalState() if getattr(x,"mcMatchAny_gp",None) else 0, int, mcOnly=True, help="isDirectPromptTauDecayProductFinalState"),
    NTupleVariable("mcPromptGamma", lambda x : x.mcPho.isPromptFinalState() if getattr(x,"mcPho",None) else 0, int, mcOnly=True, help="Photon isPromptFinalState"),
    NTupleVariable("mcGamma", lambda x : getattr(x,"mcPho",None) != None, int, mcOnly=True, help="Matched to a photon"),
    NTupleVariable("RelIsoMIV03",   lambda x : getattr(x,'AbsIsoMIV03',-99)/x.pt()),
    NTupleVariable("RelIsoMIVCharged03",   lambda x : getattr(x,'AbsIsoMIVCharged03',-99)/x.pt()),
    NTupleVariable("RelIsoMIVNeutral03",   lambda x : getattr(x,'AbsIsoMIVNeutral03',-99)/x.pt()),
    NTupleVariable("RelIsoMIV04",   lambda x : getattr(x,'AbsIsoMIV04',-99)/x.pt()),
    NTupleVariable("RelIsoMIVCharged04",   lambda x : getattr(x,'AbsIsoMIVCharged04',-99)/x.pt()),
    NTupleVariable("RelIsoMIVNeutral04",   lambda x : getattr(x,'AbsIsoMIVNeutral04',-99)/x.pt()),
    NTupleVariable("jetPtRelHv2", lambda lepton : ptRelHv2(lepton) if hasattr(lepton,'jet') else -1, help="pt of the jet (subtracting the lepton) transverse to the lepton axis - v2"),
    NTupleVariable("isoRelH04", lambda lepton : isoRelH(lepton,'04') if hasattr(lepton,'isoSumRawP4Charged04') else -1, help="transverse relative isolation R=0.4 H"),
    NTupleVariable("jetBasedRelIsoCharged", lambda lepton : jetBasedRelIsoCharged(lepton) if hasattr(lepton,'jet') else -1, help="relative charged isolation from jet chH constituents"),
    # IVF variables
    NTupleVariable("hasSV",   lambda x : (2 if getattr(x,'ivfAssoc','') == "byref" else (0 if getattr(x,'ivf',None) == None else 1)), int, help="2 if lepton track is from a SV, 1 if loosely matched, 0 if no SV found."),
    NTupleVariable("svSip3d", lambda x : x.ivf.d3d.significance() if getattr(x,'ivf',None) != None else -99, help="S_{ip3d} of associated SV"),
    NTupleVariable("svRedPt", lambda x : getattr(x, 'ivfRedPt', 0), help="pT of associated SV, removing the lepton track"),
    NTupleVariable("svMass", lambda x : x.ivf.mass() if getattr(x,'ivf',None) != None else -99, help="mass of associated SV"),
    NTupleVariable("svNTracks", lambda x : x.ivf.numberOfDaughters() if getattr(x,'ivf',None) != None else -99, help="Number of tracks of associated SV"),

    # Extra electron kinematic variables used for charge flip studies
    ##NTupleVariable("etaSc", lambda x : x.superCluster().eta(), help="Photon supercluster pseudorapidity"), # already in leptonExtra
    NTupleVariable("energySc", lambda x : x.superCluster().energy() if abs(x.pdgId())==11 else -100, help="Electron supercluster pseudorapidity"),


])
leptonTypeSusyExtraLight.addSubObjects([
        NTupleSubObject("jetLepAwareJEC",lambda x: jetLepAwareJEC(x), tlorentzFourVectorType)
        ])


leptonTypeSusyExtra = NTupleObjectType("leptonSusyExtra", baseObjectTypes = [ leptonTypeSusyExtraLight ], variables = [
    # more directional isolations
    NTupleVariable("isoRelH02", lambda lepton : isoRelH(lepton,'02') if hasattr(lepton,'isoSumRawP4Charged02') else -1, help="transverse relative isolation R=0.2 H"),
    NTupleVariable("isoRelH03", lambda lepton : isoRelH(lepton,'03') if hasattr(lepton,'isoSumRawP4Charged03') else -1, help="transverse relative isolation R=0.3 H"),
    NTupleVariable("isoRelH05", lambda lepton : isoRelH(lepton,'05') if hasattr(lepton,'isoSumRawP4Charged05') else -1, help="transverse relative isolation R=0.5 H"),
    NTupleVariable("isoRelH06", lambda lepton : isoRelH(lepton,'06') if hasattr(lepton,'isoSumRawP4Charged06') else -1, help="transverse relative isolation R=0.6 H"),
    # IVF variables
    NTupleVariable("svRedM",  lambda x : getattr(x, 'ivfRedM', 0), help="mass of associated SV, removing the lepton track"),
    NTupleVariable("svLepSip3d", lambda x : getattr(x, 'ivfSip3d', 0), help="sip3d of lepton wrt SV"),
    NTupleVariable("svChi2n", lambda x : x.ivf.vertexChi2()/x.ivf.vertexNdof() if getattr(x,'ivf',None) != None else -99, help="Normalized chi2 of associated SV"),
    NTupleVariable("svDxy", lambda x : x.ivf.dxy.value() if getattr(x,'ivf',None) != None else -99, help="dxy of associated SV"),
    NTupleVariable("svPt", lambda x : x.ivf.pt() if getattr(x,'ivf',None) != None else -99, help="pt of associated SV"),
    NTupleVariable("svMCMatchFraction", lambda x : x.ivf.mcMatchFraction if getattr(x,'ivf',None) != None else -99, mcOnly=True, help="Fraction of mc-matched tracks from b/c matched to a single hadron (if >= 2 tracks found), for associated SV"),
    NTupleVariable("svMva", lambda x : x.ivf.mva if getattr(x,'ivf',None) != None else -99, help="mva value of associated SV"),
    # Additional jet-lepton related variables
    NTupleVariable("jetNDau",    lambda lepton : lepton.jet.numberOfDaughters() if hasattr(lepton,'jet') and lepton.jet != lepton else -1, help="n daughters of nearest jet"),
    NTupleVariable("jetNDauCharged",    lambda lepton : sum(x.charge()!=0 for x in lepton.jet.daughterPtrVector()) if hasattr(lepton,'jet') and lepton.jet != lepton else -1, help="n charged daughters of nearest jet"),
    NTupleVariable("jetNDauPV",    lambda lepton : sum(x.charge()!=0 and x.fromPV()==3 for x in lepton.jet.daughterPtrVector()) if hasattr(lepton,'jet') and lepton.jet != lepton else -1, help="n charged daughters from PV of nearest jet"),
    NTupleVariable("jetNDauNotPV",    lambda lepton : sum(x.charge()!=0 and x.fromPV()<=2 for x in lepton.jet.daughterPtrVector()) if hasattr(lepton,'jet') and lepton.jet != lepton else -1, help="n charged daughters from PV of nearest jet"),    
    NTupleVariable("jetmaxSignedSip3D",    lambda lepton :  maxSignedSip3Djettracks(lepton), help="max signed Sip3D among jet's tracks"),
    NTupleVariable("jetmaxSip3D",    lambda lepton :   maxSip3Djettracks(lepton), help="max Sip3D among jet's tracks"),
    NTupleVariable("jetmaxSignedSip2D",    lambda lepton  : maxSignedSip2Djettracks(lepton) , help="max signed Sip2D among jet's tracks"),
    NTupleVariable("jetmaxSip2D",    lambda lepton :   maxSip2Djettracks(lepton), help="max Sip2D among jet's tracks"),
    NTupleVariable("jetPtRelv0",   lambda lepton : ptRel(lepton.p4(),lepton.jet.p4()) if hasattr(lepton,'jet') else -1, help="pt of the lepton transverse to the jet axis (not subtracting the lepton)"),
    NTupleVariable("jetMass",      lambda lepton : lepton.jet.mass() if hasattr(lepton,'jet') else -1, help="Mass of associated jet"),
    NTupleVariable("jetPrunedMass",      lambda lepton : getattr(lepton.jet, 'prunedP4', lepton.jet.p4()).M() if hasattr(lepton,'jet') else -1, help="Pruned mass of associated jet"),
    NTupleVariable("jetDecDR",      lambda lepton : lepton.jetDecDR if hasattr(lepton,'jetDecDR') else -1, help="deltaR(lepton, nearest jet) after declustering"),
    NTupleVariable("jetDecPtRel", lambda lepton : lepton.jetDecPtRel if hasattr(lepton,'jetDecPtRel') else -1, help="pt of the lepton transverse to the jet axis (subtracting the lepton), after declustering"),
    NTupleVariable("jetDecPtRatio", lambda lepton :  lepton.jetDecPtRatio if hasattr(lepton,'jetDecPtRatio') else -1, help="pt(lepton)/pt(nearest jet) after declustering"),
    NTupleVariable("jetDecPrunedMass", lambda lepton :  lepton.jetDecPrunedMass if hasattr(lepton,'jetDecPrunedMass') else -1, help="pt(lepton)/pt(nearest jet) after declustering and pruning"),
    NTupleVariable("jetDecPrunedPtRatio", lambda lepton :  lepton.jetDecPrunedPtRatio if hasattr(lepton,'jetDecPrunedPtRatio') else -1, help="pt(lepton)/pt(nearest jet) after declustering and pruning"),
    NTupleVariable("jetDec02DR",      lambda lepton : lepton.jetDec02DR if hasattr(lepton,'jetDec02DR') else -1, help="deltaR(lepton, nearest jet) after declustering 02"),
    NTupleVariable("jetDec02PtRel", lambda lepton : lepton.jetDec02PtRel if hasattr(lepton,'jetDec02PtRel') else -1, help="pt of the lepton transverse to the jet axis (subtracting the lepton), after declustering 02"),
    NTupleVariable("jetDec02PtRatio", lambda lepton :  lepton.jetDec02PtRatio if hasattr(lepton,'jetDec02PtRatio') else -1, help="pt(lepton)/pt(nearest jet) after declustering 02"),
    NTupleVariable("jetDec02PrunedPtRatio", lambda lepton :  lepton.jetDec02PrunedPtRatio if hasattr(lepton,'jetDec02PrunedPtRatio') else -1, help="pt(lepton)/pt(nearest jet) after declustering 02 and pruning"),
    NTupleVariable("jetDec02PrunedMass", lambda lepton :  lepton.jetDec02PrunedMass if hasattr(lepton,'jetDec02PrunedMass') else -1, help="pt(lepton)/pt(nearest jet) after declustering 02 and pruning"),
    NTupleVariable("jetRawPt", lambda x: x.jet.pt() * x.jet.rawFactor() if x.jet!=x else x.pt(), help="matched jet raw pt"),
    NTupleVariable("jetPtRatio_Raw", lambda lepton : -1 if not hasattr(lepton,'jet') else lepton.pt()/lepton.jet.pt() if not hasattr(lepton.jet,'rawFactor') else lepton.pt()/(lepton.jet.pt()*lepton.jet.rawFactor()), help="pt(lepton)/rawpt(nearest jet)"),
])


##------------------------------------------  
## TAU
##------------------------------------------  

tauTypeSusy = NTupleObjectType("tauSusy",  baseObjectTypes = [ tauType ], variables = [
        NTupleVariable("idMVAdR03", lambda x : x.idMVAdR03, int, help="1,2,3,4,5,6 if the tau passes the very loose to very very tight WP of the IsolationMVArun2v1DBdR03oldDMwLT discriminator"),
])

##------------------------------------------  
##  ISOTRACK
##------------------------------------------  

isoTrackTypeSusy = NTupleObjectType("isoTrackSusy",  baseObjectTypes = [ isoTrackType ], variables = [
])


##------------------------------------------  
## PHOTON
##------------------------------------------  

photonTypeSusy = NTupleObjectType("gammaSusy", baseObjectTypes = [ photonType ], variables = [
    NTupleVariable("genIso04",  lambda x : getattr(x, 'genIso04', -1.0), float, mcOnly=True, help="sum pt of all status 1 particles within DeltaR = 0.4 of the photon"),
    NTupleVariable("genIso03",  lambda x : getattr(x, 'genIso03', -1.0), float, mcOnly=True, help="sum pt of all status 1 particles within DeltaR = 0.3 of the photon"),
    NTupleVariable("chHadIsoRC04",  lambda x : getattr(x, 'chHadIsoRC04', -1.0), float, mcOnly=False, help="charged iso 0.4 in a random cone 90 degrees in phi from photon"),
    NTupleVariable("chHadIsoRC",  lambda x : getattr(x, 'chHadIsoRC03', -1.0), float, mcOnly=False, help="charged iso 0.3 in a random cone 90 degrees in phi from photon"),
    NTupleVariable("drMinParton",  lambda x : getattr(x, 'drMinParton', -1.0), float, mcOnly=True, help="deltaR min between photon and parton"),
])

##------------------------------------------  
## JET
##------------------------------------------  

jetTypeSusy = NTupleObjectType("jetSusy",  baseObjectTypes = [ jetTypeExtra ], variables = [
    NTupleVariable("mcMatchFlav",  lambda x : getattr(x,'mcMatchFlav',-99), int, mcOnly=True, help="Flavour of associated parton from hard scatter (if any)"),
    NTupleVariable("charge", lambda x : x.jetCharge(), float, help="Jet charge"), 
    NTupleVariable("ctagCsvL", lambda x : x.btag('pfCombinedCvsLJetTags'), float, help="CsvL discriminator"),
    NTupleVariable("ctagCsvB", lambda x : x.btag('pfCombinedCvsBJetTags'), float, help="CsvB discriminator"),
    NTupleVariable("btagDeepCSVCvsB", lambda x : (lambda y : -99 if isnan(y) else y)(x.btag('pfDeepCSVJetTags:probc')/(x.btag('pfDeepCSVJetTags:probc')+x.btag('pfDeepCSVJetTags:probb')+x.btag('pfDeepCSVJetTags:probbb'))), help="DeepCSV discriminator, CvsB = c/(c+b+bb)"),
    NTupleVariable("btagDeepCSVCvsL", lambda x : (lambda y : -99 if isnan(y) else y)(x.btag('pfDeepCSVJetTags:probc')/(x.btag('pfDeepCSVJetTags:probc')+x.btag('pfDeepCSVJetTags:probudsg'))), help="DeepCSV discriminator, CvsL = c/(c+udsg)"),
])

jetTypeSusyExtraLight = NTupleObjectType("jetSusyExtraLight",  baseObjectTypes = [ jetTypeSusy ], variables = [
    NTupleVariable("CorrFactor_L1", lambda x: x.CorrFactor_L1 if hasattr(x,'CorrFactor_L1') else 0, help="L1 correction factor"),
    NTupleVariable("CorrFactor_L1L2", lambda x: x.CorrFactor_L1L2 if hasattr(x,'CorrFactor_L1L2') else 0, help="L1L2 correction factor"),
    NTupleVariable("CorrFactor_L1L2L3", lambda x: x.CorrFactor_L1L2L3 if hasattr(x,'CorrFactor_L1L2L3') else 0, help="L1L2L3 correction factor"),
    NTupleVariable("CorrFactor_L1L2L3Res", lambda x: x.CorrFactor_L1L2L3Res if hasattr(x,'CorrFactor_L1L2L3Res') else 0, help="L1L2L3Res correction factor"),
    NTupleVariable("chHEF", lambda x : x.chargedHadronEnergyFraction(), float, mcOnly = False, help="chargedHadronEnergyFraction (relative to uncorrected jet energy)"),
    NTupleVariable("neHEF", lambda x : x.neutralHadronEnergyFraction(), float, mcOnly = False,help="neutralHadronEnergyFraction (relative to uncorrected jet energy)"),
])

jetTypeSusySuperLight = NTupleObjectType("jet",  baseObjectTypes = [ fourVectorType ], variables = [
        NTupleVariable("etaetaMoment", lambda x : x.etaetaMoment() if hasattr(x,'etaetaMoment') else -1, mcOnly=True, help="eta eta moment"),
        NTupleVariable("phiphiMoment", lambda x : x.phiphiMoment() if hasattr(x,'phiphiMoment') else -1, mcOnly=True, help="phi phi moment"),
        NTupleVariable("btagCSV",   lambda x : x.btag('pfCombinedInclusiveSecondaryVertexV2BJetTags'), help="CSV-IVF v2 discriminator"),
        NTupleVariable("btagDeepCSV",     lambda x : (lambda y : -99 if isnan(y) else y)(x.btag('pfDeepCSVJetTags:probb')+x.btag('pfDeepCSVJetTags:probbb')), help="DeepCSV discriminator, BvsAll = b+bb"),
        NTupleVariable("mcFlavour", lambda x : x.partonFlavour(), int,     mcOnly=True, help="parton flavour (physics definition, i.e. including b's from shower)"),
        NTupleVariable("partonFlavour", lambda x : x.partonFlavour(), int,     mcOnly=True, help="purely parton-based flavour"),
])

jetTypeSusyExtra = NTupleObjectType("jetSusyExtra",  baseObjectTypes = [ jetTypeSusyExtraLight ], variables = [
    NTupleVariable("prunedMass", lambda x : x.prunedP4.M() if hasattr(x,'prunedP4') else x.mass(), float, help="Pruned mass"),
    NTupleVariable("mcNumPartons", lambda x : getattr(x,'mcNumPartons',-1),int, mcOnly=True, help="Number of matched partons (quarks, photons)"),
    NTupleVariable("mcNumLeptons", lambda x : getattr(x,'mcNumLeptons',-1),int, mcOnly=True, help="Number of matched leptons"),
    NTupleVariable("mcNumTaus", lambda x : getattr(x,'mcNumTaus',-1),int, mcOnly=True, help="Number of matched taus"),
    NTupleVariable("mcAnyPartonMass", lambda x : getattr(x,"mcAnyPartonMass",-1),float, mcOnly=True, help="Mass of associated partons, leptons, taus"),
    NTupleVariable("nSubJets", lambda x : getattr(x, "nSubJets", 0), int, help="Number of subjets (kt, R=0.2)"), 
    NTupleVariable("nSubJets25", lambda x : getattr(x, "nSubJets25", 0), int, help="Number of subjets with pt > 25 (kt, R=0.2)"), 
    NTupleVariable("nSubJets30", lambda x : getattr(x, "nSubJets30", 0), int, help="Number of subjets with pt > 30 (kt, R=0.2)"), 
    NTupleVariable("nSubJets40", lambda x : getattr(x, "nSubJets40", 0), int, help="Number of subjets with pt > 40 (kt, R=0.2)"), 
    NTupleVariable("nSubJetsZ01", lambda x : getattr(x, "nSubJetsZ01", 0), int, help="Number of subjets with pt > 0.1 * pt(jet) (kt, R=0.2)"), 
    # --------------- 
    NTupleVariable("phEF", lambda x : x.photonEnergyFraction(), float, mcOnly = False,help="photonEnergyFraction (relative to corrected jet energy)"),
    NTupleVariable("eEF", lambda x : x.electronEnergyFraction(), float, mcOnly = False,help="electronEnergyFraction (relative to corrected jet energy)"),
    NTupleVariable("muEF", lambda x : x.muonEnergyFraction(), float, mcOnly = False,help="muonEnergyFraction (relative to corrected jet energy)"),
    NTupleVariable("HFHEF", lambda x : x.HFHadronEnergyFraction(), float, mcOnly = False,help="HFHadronEnergyFraction (relative to corrected jet energy)"),
    NTupleVariable("HFEMEF", lambda x : x.HFEMEnergyFraction(), float, mcOnly = False,help="HFEMEnergyFraction (relative to corrected jet energy)"),
    NTupleVariable("chHMult", lambda x : x.chargedHadronMultiplicity(), int, mcOnly = False,help="chargedHadronMultiplicity from PFJet.h"),
    NTupleVariable("neHMult", lambda x : x.neutralHadronMultiplicity(), int, mcOnly = False,help="neutralHadronMultiplicity from PFJet.h"),
    NTupleVariable("phMult", lambda x : x.photonMultiplicity(), int, mcOnly = False,help="photonMultiplicity from PFJet.h"),
    NTupleVariable("eMult", lambda x : x.electronMultiplicity(), int, mcOnly = False,help="electronMultiplicity from PFJet.h"),
    NTupleVariable("muMult", lambda x : x.muonMultiplicity(), int, mcOnly = False,help="muonMultiplicity from PFJet.h"),
    NTupleVariable("HFHMult", lambda x : x.HFHadronMultiplicity(), int, mcOnly = False,help="HFHadronMultiplicity from PFJet.h"),
    NTupleVariable("HFEMMult", lambda x : x.HFEMMultiplicity(), int, mcOnly = False,help="HFEMMultiplicity from PFJet.h"),
])

fatJetType = NTupleObjectType("fatJet",  baseObjectTypes = [ jetType ], variables = [
    NTupleVariable("prunedMass",  lambda x : x.userFloat("ak8PFJetsCHSPrunedMass"),  float, help="pruned mass"),
    NTupleVariable("softDropMass", lambda x : x.userFloat("ak8PFJetsCHSSoftDropMass"), float, help="trimmed mass"),
    NTupleVariable("tau1", lambda x : x.userFloat("NjettinessAK8:tau1"), float, help="1-subjettiness"),
    NTupleVariable("tau2", lambda x : x.userFloat("NjettinessAK8:tau2"), float, help="2-subjettiness"),
    NTupleVariable("tau3", lambda x : x.userFloat("NjettinessAK8:tau3"), float, help="3-subjettiness"),
    NTupleVariable("topMass", lambda x : (x.tagInfo("caTop").properties().topMass if x.tagInfo("caTop") else -99), float, help="CA8 jet topMass"),
    NTupleVariable("minMass", lambda x : (x.tagInfo("caTop").properties().minMass if x.tagInfo("caTop") else -99), float, help="CA8 jet minMass"),
    NTupleVariable("nSubJets", lambda x : (x.tagInfo("caTop").properties().nSubJets if x.tagInfo("caTop") else -99), float, help="CA8 jet nSubJets"),
])
      
##------------------------------------------  
## MET
##------------------------------------------  
  
metTypeSusy = NTupleObjectType("metSusy", baseObjectTypes = [ metType ], variables = [
])

##------------------------------------------  
## GENPARTICLE
##------------------------------------------  


##------------------------------------------  
## SECONDARY VERTEX CANDIDATE
##------------------------------------------  
svType = NTupleObjectType("sv", baseObjectTypes = [ fourVectorType ], variables = [
    NTupleVariable("charge",   lambda x : x.charge(), int),
    NTupleVariable("ntracks", lambda x : x.numberOfDaughters(), int, help="Number of tracks (with weight > 0.5)"),
    NTupleVariable("chi2", lambda x : x.vertexChi2(), help="Chi2 of the vertex fit"),
    NTupleVariable("ndof", lambda x : x.vertexNdof(), help="Degrees of freedom of the fit, ndof = (2*ntracks - 3)" ),
    NTupleVariable("dxy",  lambda x : x.dxy.value(), help="Transverse distance from the PV [cm]"),
    NTupleVariable("edxy", lambda x : x.dxy.error(), help="Uncertainty on the transverse distance from the PV [cm]"),
    NTupleVariable("ip3d",  lambda x : x.d3d.value(), help="3D distance from the PV [cm]"),
    NTupleVariable("eip3d", lambda x : x.d3d.error(), help="Uncertainty on the 3D distance from the PV [cm]"),
    NTupleVariable("sip3d", lambda x : x.d3d.significance(), help="S_{ip3d} with respect to PV (absolute value)"),
    NTupleVariable("cosTheta", lambda x : x.cosTheta, help="Cosine of the angle between the 3D displacement and the momentum"),
    NTupleVariable("mva", lambda x : x.mva, help="MVA discriminator"),
    NTupleVariable("jetPt",  lambda x : x.jet.pt() if x.jet != None else 0, help="pT of associated jet"),
    NTupleVariable("jetEta",  lambda x : x.jet.eta() if x.jet != None else 0, help="eta of associated jet"),
    NTupleVariable("jetDR",  lambda x : deltaR(x.jet.eta(),x.jet.phi(),x.eta(),x.phi()) if x.jet != None else 0, help="deltaR to associated jet"),
    NTupleVariable("jetBTagCSV",   lambda x : x.jet.btag('pfCombinedInclusiveSecondaryVertexV2BJetTags') if x.jet != None else -99, help="CSV b-tag of associated jet"),
    NTupleVariable("jetBTagCMVA",  lambda x : x.jet.btag('pfCombinedMVABJetTags') if x.jet != None else -99, help="CMVA b-tag of associated jet"),
    NTupleVariable("jetBTagDeepCSV", lambda x : (lambda y: -99 if isnan(y) else y)(x.jet.btag('pfDeepCSVJetTags:probb')+x.jet.btag('pfDeepCSVJetTags:probbb') if x.jet != None else -99), help="DeepCSV b-tag of associated jet, BvsAll = b+bb"),
    NTupleVariable("mcMatchNTracks", lambda x : getattr(x, 'mcMatchNTracks', -1), int, mcOnly=True, help="Number of mc-matched tracks in SV"),
    NTupleVariable("mcMatchNTracksHF", lambda x : getattr(x, 'mcMatchNTracksHF', -1), int, mcOnly=True, help="Number of mc-matched tracks from b/c in SV"),
    NTupleVariable("mcMatchFraction", lambda x : getattr(x, 'mcMatchFraction', -1), mcOnly=True, help="Fraction of mc-matched tracks from b/c matched to a single hadron (or -1 if mcMatchNTracksHF < 2)"),
    NTupleVariable("mcFlavFirst", lambda x : getattr(x,'mcFlavFirst', -1), int, mcOnly=True, help="Flavour of last ancestor with maximum number of matched daughters"),
    NTupleVariable("mcFlavHeaviest", lambda x : getattr(x,'mcFlavHeaviest', -1), int, mcOnly=True, help="Flavour of heaviest hadron with maximum number of matched daughters"),
    NTupleVariable("maxDxyTracks", lambda x : x.maxDxyTracks, help="highest |dxy| of vertex tracks"),
    NTupleVariable("secDxyTracks", lambda x : x.secDxyTracks, help="second highest |dxy| of vertex tracks"),
    NTupleVariable("maxD3dTracks", lambda x : x.maxD3dTracks, help="highest |ip3D| of vertex tracks"),
    NTupleVariable("secD3dTracks", lambda x : x.secD3dTracks, help="second highest |ip3D| of vertex tracks"),
])
svTypeExtra = NTupleObjectType("svExtra", baseObjectTypes = [ svType ], variables = [
    NTupleVariable("tk1_pt",  lambda x : x.daughter(0).pt() if x.numberOfDaughters() > 0 else -999, help="pt of first track"),
    NTupleVariable("tk1_eta",  lambda x : x.daughter(0).eta() if x.numberOfDaughters() > 0 else -999, help="eta of first track"),
    NTupleVariable("tk1_phi",  lambda x : x.daughter(0).phi() if x.numberOfDaughters() > 0 else -999, help="phi of first track"),
    NTupleVariable("tk1_charge",  lambda x : x.daughter(0).charge() if x.numberOfDaughters() > 0 else -999, int, help="charge of first track"),
    NTupleVariable("tk2_pt",  lambda x : x.daughter(1).pt() if x.numberOfDaughters() > 1 else -999, help="pt of second track"),
    NTupleVariable("tk2_eta",  lambda x : x.daughter(1).eta() if x.numberOfDaughters() > 1 else -999, help="eta of second track"),
    NTupleVariable("tk2_phi",  lambda x : x.daughter(1).phi() if x.numberOfDaughters() > 1 else -999, help="phi of second track"),
    NTupleVariable("tk2_charge",  lambda x : x.daughter(1).charge() if x.numberOfDaughters() > 1 else -999, int, help="charge of second track"),
    NTupleVariable("tk3_pt",  lambda x : x.daughter(2).pt() if x.numberOfDaughters() > 2 else -999, help="pt of third track"),
    NTupleVariable("tk3_eta",  lambda x : x.daughter(2).eta() if x.numberOfDaughters() > 2 else -999, help="eta of third track"),
    NTupleVariable("tk3_phi",  lambda x : x.daughter(2).phi() if x.numberOfDaughters() > 2 else -999, help="phi of third track"),
    NTupleVariable("tk3_charge",  lambda x : x.daughter(2).charge() if x.numberOfDaughters() > 2 else -999, int, help="charge of third track"),
    NTupleVariable("tk4_pt",  lambda x : x.daughter(0).pt() if x.numberOfDaughters() > 0 else -999, help="pt of fourth track"),
    NTupleVariable("tk4_eta",  lambda x : x.daughter(3).eta() if x.numberOfDaughters() > 3 else -999, help="eta of fourth track"),
    NTupleVariable("tk4_phi",  lambda x : x.daughter(3).phi() if x.numberOfDaughters() > 3 else -999, help="phi of fourth track"),
    NTupleVariable("tk4_charge",  lambda x : x.daughter(3).charge() if x.numberOfDaughters() > 3 else -999, int, help="charge of fourth track"),
])

heavyFlavourHadronType = NTupleObjectType("heavyFlavourHadron", baseObjectTypes = [ genParticleType ], variables = [
    NTupleVariable("flav", lambda x : x.flav, int, mcOnly=True, help="Flavour"),
    NTupleVariable("sourceId", lambda x : x.sourceId, int, mcOnly=True, help="pdgId of heaviest mother particle (stopping at the first one heaviest than 175 GeV)"),
    NTupleVariable("svMass",   lambda x : x.sv.mass() if x.sv else 0, help="SV: mass"),
    NTupleVariable("svPt",   lambda x : x.sv.pt() if x.sv else 0, help="SV: pt"),
    NTupleVariable("svCharge",   lambda x : x.sv.charge() if x.sv else -99., int, help="SV: charge"),
    NTupleVariable("svNtracks", lambda x : x.sv.numberOfDaughters() if x.sv else 0, int, help="SV: Number of tracks (with weight > 0.5)"),
    NTupleVariable("svChi2", lambda x : x.sv.vertexChi2() if x.sv else -99., help="SV: Chi2 of the vertex fit"),
    NTupleVariable("svNdof", lambda x : x.sv.vertexNdof() if x.sv else -99., help="SV: Degrees of freedom of the fit, ndof = (2*ntracks - 3)" ),
    NTupleVariable("svDxy",  lambda x : x.sv.dxy.value() if x.sv else -99., help="SV: Transverse distance from the PV [cm]"),
    NTupleVariable("svEdxy", lambda x : x.sv.dxy.error() if x.sv else -99., help="SV: Uncertainty on the transverse distance from the PV [cm]"),
    NTupleVariable("svIp3d",  lambda x : x.sv.d3d.value() if x.sv else -99., help="SV: 3D distance from the PV [cm]"),
    NTupleVariable("svEip3d", lambda x : x.sv.d3d.error() if x.sv else -99., help="SV: Uncertainty on the 3D distance from the PV [cm]"),
    NTupleVariable("svSip3d", lambda x : x.sv.d3d.significance() if x.sv else -99., help="SV: S_{ip3d} with respect to PV (absolute value)"),
    NTupleVariable("svCosTheta", lambda x : x.sv.cosTheta if x.sv else -99., help="SV: Cosine of the angle between the 3D displacement and the momentum"),
    NTupleVariable("svMva", lambda x : x.sv.mva if x.sv else -99., help="SV: mva value"),
    NTupleVariable("jetPt",  lambda x : x.jet.pt() if x.jet != None else 0, help="Jet: pT"),
    NTupleVariable("jetBTagCSV",  lambda x : x.jet.btag('pfCombinedInclusiveSecondaryVertexV2BJetTags') if x.jet != None else -99, help="CSV b-tag of associated jet"),
    NTupleVariable("jetBTagCMVA",  lambda x : x.jet.btag('pfCombinedMVABJetTags') if x.jet != None else -99, help="CMVA b-tag of associated jet"),
    NTupleVariable("jetBTagDeepCSV", lambda x : (lambda y: -99 if isnan(y) else y)(x.jet.btag('pfDeepCSVJetTags:probb')+x.jet.btag('pfDeepCSVJetTags:probbb') if x.jet != None else -99), help="DeepCSV b-tag of associated jet, BvsAll = b+bb"),
    
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
