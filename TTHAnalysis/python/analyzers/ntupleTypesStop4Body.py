from CMGTools.TTHAnalysis.analyzers.ntupleTypes import *

##------------------------------------------
## GENJET
##------------------------------------------

genJetType = NTupleObjectType("genJets",  baseObjectTypes = [ fourVectorType ], mcOnly=True, variables = [
    NTupleVariable("nConstituents", lambda x : x.nConstituents(), help="Number of Constituents"),
])

##------------------------------------------
## GENPARTICLE
##------------------------------------------

genParticleWithMotherIndex = NTupleObjectType("genParticleWithMotherIndex", baseObjectTypes = [ genParticleWithMotherId ], mcOnly=True, variables = [
    NTupleVariable("nDaughters",     lambda x : x.numberOfDaughters(),                                                               int, help="index of the daughters in the genParticles"),
    NTupleVariable("nMothers",       lambda x : x.numberOfMothers(),                                                                 int, help="index of the mother in the genParticles"),
    NTupleVariable("motherIndex1",   lambda x : x.motherRef(0).index() if x.numberOfMothers() > 0 else -1,                           int, help="index of the first mother in the genParticles"),
    NTupleVariable("daughterIndex1", lambda x : x.daughterRef(0).index() if x.numberOfDaughters() >0 else -1,                        int, help="index of the first mother in the genParticles"),
    NTupleVariable("motherIndex2",   lambda x : x.motherRef(x.numberOfMothers()-1).index() if x.numberOfMothers() > 1 else -1,       int, help="index of the last mother in the genParticles"),
    NTupleVariable("daughterIndex2", lambda x : x.daughterRef(x.numberOfDaughters()-1).index() if x.numberOfDaughters() > 1 else -1, int, help="index of the last mother in the genParticles"),
])

##------------------------------------------
## LEPTON
##------------------------------------------

leptonTypeStop4Body = NTupleObjectType("leptonStop4Body", baseObjectTypes = [ leptonTypeSusy ], variables = [
    # TO DO: Muon ID
    # ID variables
    # ----------------------
    # Has to be tested
    NTupleVariable("SOSTightID2017",             lambda x : (x.electronID("MVA_ID_nonIso_Fall17_wp90") if x.pt()<10 else x.electronID("MVA_ID_nonIso_Fall17_SUSYTight")) if abs(x.pdgId())==11 else 0, int, help="SOS tight electron MVA noIso ID 2017 (WP: POG wp90 below 10 GeV, SUSYTight above)"),
    NTupleVariable("SUSYVLooseFOFall17",         lambda x : x.electronID("MVA_ID_nonIso_Fall17_SUSYVLooseFO")       if abs(x.pdgId())==11 and x.pt()> 5 else 1, int, help="SUSYVLooseFOFall17"),
    NTupleVariable("SUSYVLooseFall17",           lambda x : x.electronID("MVA_ID_nonIso_Fall17_SUSYVLoose")         if abs(x.pdgId())==11 and x.pt()> 5 else 1, int, help="SUSYVLooseFall17"),
    NTupleVariable("SUSYTightFall17",            lambda x : x.electronID("MVA_ID_nonIso_Fall17_SUSYTight")          if abs(x.pdgId())==11 and x.pt()>10 else 1, int, help="SUSYTightFall17"),
    NTupleVariable("trkIso03", lambda x : (x.dr03TkSumPt() if abs(x.pdgId())==11 else x.isolationR03().sumPt)/x.pt(), help="TrkIso R=0.3"),
    NTupleVariable("trkIso045", lambda x : (x.dr04TkSumPt() if abs(x.pdgId())==11 else x.isolationR05().sumPt)/x.pt(), help="TrkIso R=0.4 (e), 0.5 (mu)"),
    
    #MUON ID
    NTupleVariable("softMuonId",   lambda x : x.muonID("POG_ID_Soft") if abs(x.pdgId())==13 else 1,  int, help="Muon POG Soft id"),
    NTupleVariable("looseMuonId",  lambda x : x.muonID("POG_ID_Loose") if abs(x.pdgId())==13 else 1, int, help="Muon POG Loose id"),
    #NTupleVariable("mediumMuonId",  lambda x : x.muonID("POG_ID_Medium") if abs(x.pdgId())==13 else 1, int, help="Muon POG Medium id"),
    NTupleVariable("tightMuonId",  lambda x : x.muonID("POG_ID_Tight") if abs(x.pdgId())==13 else 1, int, help="Muon POG Tight id"),

    #ELECTRON ID
    NTupleVariable("softElectronId",   lambda x : x.muonID("POG_ID_Soft") if abs(x.pdgId())==11 else 1,  int, help="Electron POG Soft id"),
    NTupleVariable("looseElectronId",  lambda x : x.muonID("POG_ID_Loose") if abs(x.pdgId())==11 else 1, int, help="Electron POG Loose id"),
    NTupleVariable("mediumElectronId",  lambda x : x.muonID("POG_ID_Medium") if abs(x.pdgId())==11 else 1, int, help="Electron POG Medium id"),
    NTupleVariable("tightElectronId",  lambda x : x.muonID("POG_ID_Tight") if abs(x.pdgId())==11 else 1, int, help="Electron POG Tight id"),

    #NTupleVariable("mvaIdSpring15",   lambda lepton : lepton.mvaRun2("NonTrigSpring15MiniAOD") if abs(lepton.pdgId()) == 11 else 1, help="EGamma POG MVA ID for non-triggering electrons, Spring15 re-training; 1 for muons"),

    #NTupleVariable("SPRING15_25ns_v1", lambda x : (1*x.electronID("POG_Cuts_ID_SPRING15_25ns_v1_ConvVetoDxyDz_Veto") + 1*x.electronID("POG_Cuts_ID_SPRING15_25ns_v1_ConvVetoDxyDz_Loose") + 1*x.electronID("POG_Cuts_ID_SPRING15_25ns_v1_ConvVetoDxyDz_Medium") + 1*x.electronID("POG_Cuts_ID_SPRING15_25ns_v1_ConvVetoDxyDz_Tight")) if abs(x.pdgId()) == 11 else -1, int, help="Electron cut-based id (POG_SPRING15_25ns_v1_ConvVetoDxyDy): 0=none, 1=veto, 2=loose, 3=medium, 4=tight"),

    #NTupleVariable("eleCBID_SPRING15_25ns_ConvVeto", lambda x : (1*x.electronID("POG_Cuts_ID_SPRING15_25ns_v1_ConvVeto_Veto") + 1*x.electronID("POG_Cuts_ID_SPRING15_25ns_v1_ConvVeto_Loose") + 1*x.electronID("POG_Cuts_ID_SPRING15_25ns_v1_ConvVeto_Medium") + 1*x.electronID("POG_Cuts_ID_SPRING15_25ns_v1_ConvVeto_Tight")) if abs(x.pdgId()) == 11 else -1, int, help="Electron cut-based id (POG_SPRING15_25ns_v1_ConvVeto): 0=none, 1=veto, 2=loose, 3=medium, 4=tight"),
    #NTupleVariable("eleCBID_SPRING15_25ns_ConvVetoDxyDz", lambda x : (1*x.electronID("POG_Cuts_ID_SPRING15_25ns_v1_ConvVetoDxyDz_Veto") + 1*x.electronID("POG_Cuts_ID_SPRING15_25ns_v1_ConvVetoDxyDz_Loose") + 1*x.electronID("POG_Cuts_ID_SPRING15_25ns_v1_ConvVetoDxyDz_Medium") + 1*x.electronID("POG_Cuts_ID_SPRING15_25ns_v1_ConvVetoDxyDz_Tight")) if abs(x.pdgId()) == 11 else -1, int, help="Electron cut-based id (POG_SPRING15_25ns_v1_ConvVetoDxyDy): 0=none, 1=veto, 2=loose, 3=medium, 4=tight"),
    #NTupleVariable("eleCBID_SPRING15_25ns",               lambda x : (1*x.electronID("POG_Cuts_ID_SPRING15_25ns_v1_Veto") + 1*x.electronID("POG_Cuts_ID_SPRING15_25ns_v1_Loose") + 1*x.electronID("POG_Cuts_ID_SPRING15_25ns_v1_Medium") + 1*x.electronID("POG_Cuts_ID_SPRING15_25ns_v1_Tight")) if abs(x.pdgId()) == 11 else -1,                                                         int, help="Electron cut-based id (POG_SPRING15_25ns_v1_ConvVetoDxyDy): 0=none, 1=veto, 2=loose, 3=medium, 4=tight"),

    # Low level vars -- duplicates of leptonSusyExtra
    NTupleVariable("hOverE",  lambda x : x.hadronicOverEm() if abs(x.pdgId())==11 else 0,                                                                           help="Electron hadronicOverEm"),
    NTupleVariable("ooEmooP", lambda x : ((1.0/x.ecalEnergy() - x.eSuperClusterOverP()/x.ecalEnergy()) if x.ecalEnergy()>0. else 9e9) if abs(x.pdgId())==11 else 0, help="Electron 1/E - 1/p  (without absolute value!)"),
    # Extra isolation variables
    #NTupleVariable("chargedHadRelIso03",  lambda x : x.chargedHadronIsoR(0.3)/x.pt(), help="PF Rel Iso, R=0.3, charged hadrons only"),
    #NTupleVariable("chargedHadRelIso04",  lambda x : x.chargedHadronIsoR(0.4)/x.pt(), help="PF Rel Iso, R=0.4, charged hadrons only"),
    # Extra muon ID working points
    #NTupleVariable("softMuonId",   lambda x : x.muonID("POG_ID_Soft") if abs(x.pdgId())==13 else 1,  int, help="Muon POG Soft id"),
    #
    NTupleVariable("absIso03",     lambda x : x.absIso03, help="PF Abs Iso, R=0.3, pile-up corrected"),
    NTupleVariable("absIso",       lambda x : x.absIso04, help="PF Rel Iso, R=0.4, pile-up corrected"),
    NTupleVariable("cosPhiLepMet", lambda x : x.cosLMet,  help="Cos phi of the lepton and met  "),
    NTupleVariable("mt",           lambda x : x.mt,       help="Transverse Mass calculated for lepton"),
    NTupleVariable("Q80",          lambda x : x.Q80  ,    help="Q80 variable for the deconstrcuted transverse mass"),
    #

    #NTupleVariable("eleCutId2012_full5x5",     lambda x : (1*x.electronID("POG_Cuts_ID_2012_full5x5_Veto") + 1*x.electronID("POG_Cuts_ID_2012_full5x5_Loose") + 1*x.electronID("POG_Cuts_ID_2012_full5x5_Medium") + 1*x.electronID("POG_Cuts_ID_2012_full5x5_Tight")) if abs(x.pdgId()) == 11 else -1, int, help="Electron cut-based id (POG 2012, full5x5 shapes): 0=none, 1=veto, 2=loose, 3=medium, 4=tight"),
    NTupleVariable("sigmaIEtaIEta",  lambda x : x.full5x5_sigmaIetaIeta() if abs(x.pdgId())==11 else 0,                                                                    help="Electron sigma(ieta ieta), with full5x5 cluster shapes"),
    NTupleVariable("dEtaScTrkIn",    lambda x : x.deltaEtaSuperClusterTrackAtVtx() if abs(x.pdgId())==11 else 0,                                                           help="Electron deltaEtaSuperClusterTrackAtVtx (without absolute value!)"),
    NTupleVariable("dPhiScTrkIn",    lambda x : x.deltaPhiSuperClusterTrackAtVtx() if abs(x.pdgId())==11 else 0,                                                           help="Electron deltaPhiSuperClusterTrackAtVtx (without absolute value!)"),
    NTupleVariable("hadronicOverEm", lambda x : x.hadronicOverEm() if abs(x.pdgId())==11 else 0,                                                                           help="Electron hadronicOverEm"),
    NTupleVariable("eInvMinusPInv",  lambda x : ((1.0/x.ecalEnergy() - x.eSuperClusterOverP()/x.ecalEnergy()) if x.ecalEnergy()>0. else 9e9) if abs(x.pdgId())==11 else 0, help="Electron 1/E - 1/p  (without absolute value!)"),

    #new version used by EGM in Spring15, 7_4_14:
    NTupleVariable("eInvMinusPInv_tkMom", lambda x: ((1.0/x.ecalEnergy()) - (1.0 / x.trackMomentumAtVtx().R() ) if (x.ecalEnergy()>0. and x.trackMomentumAtVtx().R()>0.) else 9e9) if abs(x.pdgId())==11 else 0, help="Electron 1/E - 1/p_tk_vtx  (without absolute value!)"),
    NTupleVariable("etaSc",               lambda x : x.superCluster().eta() if abs(x.pdgId())==11 else -100,                                                                                                     help="Electron supercluster pseudorapidity"),
])

##------------------------------------------
## JET
##------------------------------------------

jetTypeStop4Body = NTupleObjectType("jetStop4Body", baseObjectTypes = [ jetTypeSusy ], variables = [
])
