#!/bin/env python
from math import *
from PhysicsTools.Heppy.analyzers.core.autovars import NTupleObjectType  
from PhysicsTools.Heppy.analyzers.objects.autophobj import  *
from PhysicsTools.HeppyCore.utils.deltar import deltaR

from CMGTools.TTHAnalysis.signedSip import *
from CMGTools.TTHAnalysis.tools.functionsTTH import _ttH_idEmu_cuts_E2_obj,_soft_MuonId_2016ICHEP,_medium_MuonId_2016ICHEP
from CMGTools.TTHAnalysis.tools.functionsRAX import _susy2lss_idEmu_cuts_obj,_susy2lss_idIsoEmu_cuts_obj

##------------------------------------------  
## LEPTON
##------------------------------------------  

leptonTypeWMass = NTupleObjectType("leptonWMass", baseObjectTypes = [ leptonType ], variables = [
    # Lepton MVA-id related variables
    NTupleVariable("mvaTTH",    lambda lepton : getattr(lepton, 'mvaValueTTH', -1), help="Lepton MVA (TTH version)"),
    NTupleVariable("mvaSUSY",    lambda lepton : getattr(lepton, 'mvaValueSUSY', -1), help="Lepton MVA (SUSY version)"),
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
    # variables for isolated electron trigger matching cuts
    NTupleVariable("ecalPFClusterIso", lambda lepton :  lepton.ecalPFClusterIso() if abs(lepton.pdgId())==11 else -999, help="Electron ecalPFClusterIso"),
    NTupleVariable("hcalPFClusterIso", lambda lepton :  lepton.hcalPFClusterIso() if abs(lepton.pdgId())==11 else -999, help="Electron hcalPFClusterIso"),
    NTupleVariable("dr03TkSumPt", lambda lepton: lepton.dr03TkSumPt() if abs(lepton.pdgId())==11 else -999, help="Electron dr03TkSumPt isolation"),
    NTupleVariable("trackIso", lambda lepton :  lepton.trackIso() if abs(lepton.pdgId())==11 else -999, help="Electron trackIso (in cone of 0.4)"),
    NTupleVariable("etaSc", lambda x : x.superCluster().eta() if abs(x.pdgId())==11 else -100, help="Electron supercluster pseudorapidity"),
    NTupleVariable("energySc", lambda x : x.superCluster().energy() if abs(x.pdgId())==11 else -100, help="Electron supercluster pseudorapidity"),
    NTupleVariable("e5x5", lambda x: x.full5x5_e5x5() if (abs(x.pdgId())==11 and hasattr(x,"full5x5_e5x5")) else -999, help="Electron full5x5_e5x5"),
    NTupleVariable("sigmaIetaIeta", lambda x: x.full5x5_sigmaIetaIeta() if (abs(x.pdgId())==11 and hasattr(x,"full5x5_sigmaIetaIeta")) else -999, help="Electron full5x5_sigmaIetaIeta"),
    NTupleVariable("hcalOverEcal", lambda x: x.full5x5_hcalOverEcal() if (abs(x.pdgId())==11 and hasattr(x,"full5x5_hcalOverEcal")) else -999, help="Electron full5x5_hcalOverEcal"),
    NTupleVariable("eSuperClusterOverP", lambda x: x.eSuperClusterOverP() if (abs(x.pdgId())==11 and hasattr(x,"eSuperClusterOverP")) else -999, help="Electron eSuperClusterOverP"),
])
