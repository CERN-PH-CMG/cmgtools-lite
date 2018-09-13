from PhysicsTools.Heppy.analyzers.core.AutoFillTreeProducer  import * 

leptonTypeHZZ = NTupleObjectType("leptonHZZ", baseObjectTypes = [ leptonTypeExtra ], variables = [
    NTupleVariable("looseId",     lambda x : x.looseIdSusy, int, help="Loose HZZ ID"),
    NTupleVariable("mvaIdSpring15",   lambda lepton : lepton.mvaRun2("NonTrigSpring15MiniAOD") if abs(lepton.pdgId()) == 11 else 1, help="EGamma POG MVA ID for non-triggering electrons, Spring15 re-training; 1 for muons"),
    NTupleVariable("mvaIdSpring16",   lambda lepton : lepton.mvaRun2("Spring16HZZ") if abs(lepton.pdgId()) == 11 else 1, help="EGamma POG MVA ID, Spring16 training; 1 for muons"),
    # ----------------------
    # Extra isolation variables
    NTupleVariable("relIsoAfterFSR",    lambda x : x.relIsoAfterFSR,   help="RelIso after FSR"),
    NTupleVariable("chargedHadIso04",   lambda x : x.chargedHadronIso(0.4),   help="PF Abs Iso, R=0.4, charged hadrons only"),
    NTupleVariable("neutralHadIso04",   lambda x : x.neutralHadronIso(0.4),   help="PF Abs Iso, R=0.4, neutral hadrons only"),
    NTupleVariable("photonIso04",       lambda x : x.photonIso(0.4),          help="PF Abs Iso, R=0.4, photons only"),
    NTupleVariable("puChargedHadIso04", lambda x : x.puChargedHadronIso(0.4), help="PF Abs Iso, R=0.4, pileup charged hadrons only"),
    NTupleVariable("rho",               lambda x : x.rho,                             help="rho for isolation"),
    NTupleVariable("EffectiveArea04",   lambda x : x.EffectiveArea04,                 help="EA for isolation"),
    NTupleVariable("chargedHadIso03",   lambda x : x.chargedHadronIso(0.3),   help="PF Abs Iso, R=0.3, charged hadrons only"),
    NTupleVariable("neutralHadIso03",   lambda x : x.neutralHadronIso(0.3),   help="PF Abs Iso, R=0.3, neutral hadrons only"),
    NTupleVariable("photonIso03",       lambda x : x.photonIso(0.3),          help="PF Abs Iso, R=0.3, photons only"),
    NTupleVariable("puChargedHadIso03", lambda x : x.puChargedHadronIso(0.3), help="PF Abs Iso, R=0.3, pileup charged hadrons only"),
    NTupleVariable("EffectiveArea03",   lambda x : x.EffectiveArea03,                 help="EA for isolation"),
    # ----------------------
    NTupleVariable("hasFSR",     lambda x : len(x.fsrPhotons), int),
    NTupleVariable("hasOwnFSR",  lambda x : len(x.ownFsrPhotons), int),
    NTupleVariable("pho_pt",  lambda x : (x.ownFsrPhotons[0].pt()  if x.ownFsrPhotons else -99.0) ),
    NTupleVariable("pho_eta", lambda x : (x.ownFsrPhotons[0].eta() if x.ownFsrPhotons else -99.0) ),
    NTupleVariable("pho_phi", lambda x : (x.ownFsrPhotons[0].phi() if x.ownFsrPhotons else -99.0) ),
    NTupleSubObject("p4WithFSR", lambda x : x.p4WithFSR(), fourVectorType),
    # ----------------------
    NTupleVariable("ptErr",   lambda x : x.ptErr(), help="Lepton p_{T} error"),
    # ----------------------
    NTupleVariable("r9",   lambda x : x.r9() if abs(x.pdgId())==11 else 1.0, help="electron r9"),
    NTupleVariable("fbrem",   lambda x : x.fbrem() if abs(x.pdgId())==11 else 0.0, help="electron fbrem"),
    NTupleVariable("eleClass",   lambda x : x.classification() if abs(x.pdgId())==11 else -1, int, help="electron classification"),
    # ----------------------
    NTupleVariable("muIdLoose", lambda x : x.muonID("POG_ID_Loose") if abs(x.pdgId())==13 else 1, help="Mu Loose ID"),
    NTupleVariable("muIdTrkHighPt", lambda x : x.muonID("HZZ_ID_TkHighPt") if abs(x.pdgId())==13 else 1, help="Mu Loose ID"),
    # ----------------------
    NTupleVariable("mcPrompt",    lambda x : x.mcMatchAny_gp.isPromptFinalState() if getattr(x,"mcMatchAny_gp",None) else 0, int, mcOnly=True, help="isPromptFinalState"),
    NTupleVariable("mcPromptTau", lambda x : x.mcMatchAny_gp.isDirectPromptTauDecayProductFinalState() if getattr(x,"mcMatchAny_gp",None) else 0, int, mcOnly=True, help="isDirectPromptTauDecayProductFinalState"),
    NTupleVariable("mcPromptGamma", lambda x : x.mcPho.isPromptFinalState() if getattr(x,"mcPho",None) else 0, int, mcOnly=True, help="Photon isPromptFinalState"),
    NTupleVariable("mcGamma", lambda x : getattr(x,"mcPho",None) != None, int, mcOnly=True, help="Matched to a photon"),
    # ----------------------
    NTupleVariable("hlt1L", lambda x : getattr(x,'matchedTrgObj1El',None) != None or  getattr(x,'matchedTrgObj1Mu',None) != None, int, help="Matched to single lepton trigger"),
])

leptonTypeHZZLite = NTupleObjectType("leptonHZZLite", baseObjectTypes = [ particleType ], variables = [
    NTupleVariable("charge",   lambda x : x.charge(), int),
    # ----------------------
    NTupleVariable("tightId",     lambda x : x.tightId(), int, help="POG Tight ID (for electrons it's configured in the analyzer)"),
    NTupleVariable("looseId",     lambda x : x.looseIdSusy, int, help="Loose HZZ ID"),
    # ----------------------
    NTupleVariable("dxy",   lambda x : x.dxy(), help="d_{xy} with respect to PV, in cm (with sign)"),
    NTupleVariable("dz",    lambda x : x.dz() , help="d_{z} with respect to PV, in cm (with sign)"),
    NTupleVariable("edxy",  lambda x : x.edB(), help="#sigma(d_{xy}) with respect to PV, in cm"),
    NTupleVariable("edz",   lambda x : x.edz(), help="#sigma(d_{z}) with respect to PV, in cm"),
    NTupleVariable("ip3d",  lambda x : x.ip3D() , help="d_{3d} with respect to PV, in cm (absolute value)"),
    NTupleVariable("sip3d",  lambda x : x.sip3D(), help="S_{ip3d} with respect to PV (significance)"),
    # ----------------------
    NTupleVariable("ptErr",   lambda x : x.ptErr(), help="Lepton p_{T} error"),
    NTupleVariable("lostHits",    lambda x : (x.gsfTrack() if abs(x.pdgId())==11 else x.innerTrack()).hitPattern().numberOfLostHits(ROOT.reco.HitPattern.MISSING_INNER_HITS), int, help="Number of lost hits on inner track"),
    NTupleVariable("trackerLayers", lambda x : (x.track() if abs(x.pdgId())==13 else x.gsfTrack()).hitPattern().trackerLayersWithMeasurement(), int, help="Tracker Layers"),
    NTupleVariable("pixelLayers", lambda x : (x.track() if abs(x.pdgId())==13 else x.gsfTrack()).hitPattern().pixelLayersWithMeasurement(), int, help="Pixel Layers"),
    NTupleVariable("etaSc", lambda x : x.superCluster().eta() if abs(x.pdgId())==11 else -100, help="Electron supercluster pseudorapidity"),
    NTupleVariable("isGap", lambda x : x.isGap() if abs(x.pdgId())==11 else False, int, help="is this a Gap electron"),
    NTupleVariable("r9",   lambda x : x.r9() if abs(x.pdgId())==11 else 1.0, help="electron r9"),
    NTupleVariable("convVeto",    lambda x : x.passConversionVeto() if abs(x.pdgId())==11 else 1, int, help="Conversion veto (always true for muons)"),
    NTupleVariable("mvaIdSpring15",   lambda lepton : lepton.mvaRun2("NonTrigSpring15MiniAOD") if abs(lepton.pdgId()) == 11 else 1, help="EGamma POG MVA ID for non-triggering electrons, Spring15 re-training; 1 for muons"),
    # ----------------------
    NTupleVariable("relIsoAfterFSR",    lambda x : x.relIsoAfterFSR,   help="RelIso after FSR"),
    NTupleVariable("chargedHadIso03",   lambda x : x.chargedHadronIso(0.3),   help="PF Abs Iso, R=0.3, charged hadrons only"),
    # ----------------------
    NTupleVariable("hasOwnFSR",  lambda x : len(x.ownFsrPhotons), int),
    NTupleSubObject("p4WithFSR", lambda x : x.p4WithFSR(), fourVectorType),
    # ----------------------
    NTupleVariable("mcMatchId",  lambda x : getattr(x, 'mcMatchId', -99), int, mcOnly=True, help="Match to source from hard scatter (pdgId of heaviest particle in chain, 25 for H, 6 for t, 23/24 for W/Z), zero if non-prompt or fake"),
    NTupleVariable("mcMatchAny", lambda x : getattr(x, 'mcMatchAny', -99), int, mcOnly=True, help="Match to any final state leptons: 0 if unmatched, 1 if light flavour (including prompt), 4 if charm, 5 if bottom"),
    NTupleVariable("mcPt",   lambda x : x.mcLep.pt() if getattr(x,"mcLep",None) else 0., mcOnly=True, help="p_{T} of associated gen lepton"),
    NTupleVariable("mcPt1",   lambda x : x.mcMatchAny_gp.pt() if getattr(x,"mcMatchAny_gp",None) else 0., mcOnly=True, help="p_{T} of associated gen lepton (status 1)"),
    # ----------------------
    NTupleVariable("hlt1L", lambda x : getattr(x,'matchedTrgObj1El',None) != None or  getattr(x,'matchedTrgObj1Mu',None) != None, int, help="Matched to single lepton trigger"),
])


fsrPhotonTypeHZZ = NTupleObjectType("fsrPhotonHZZ", baseObjectTypes = [ particleType ], variables = [
    NTupleVariable("chargedHadIso",   lambda x : getattr(x,'absIsoCH',-1.0),   help="PF Abs Iso, R=0.3, charged hadrons only"),
    NTupleVariable("photonIso",       lambda x : getattr(x,'absIsoPH',-1.0),   help="PF Abs Iso, R=0.3, photons only"),
    NTupleVariable("neutralHadIso",   lambda x : getattr(x,'absIsoNH',-1.0),   help="PF Abs Iso, R=0.3, neutral hadrons only"),
    NTupleVariable("puChargedHadIso", lambda x : getattr(x,'absIsoPU',-1.0),   help="PF Abs Iso, R=0.3, pileup charged hadrons only"),
    NTupleVariable("relIso",          lambda x : getattr(x,'relIso', -1.0),    help="PF Rel Iso, R=0.3, charged + netural had + pileup"),
    NTupleSubObject("closestLepton",  lambda x : x.globalClosestLepton, particleType),
    NTupleVariable("closestLeptonDR", lambda x : deltaR(x.eta(),x.phi(),x.globalClosestLepton.eta(),x.globalClosestLepton.phi())),
]) 

ZType = NTupleObjectType("ZType", baseObjectTypes=[fourVectorType], variables = [
    NTupleVariable("hasFSR",   lambda x : x.hasFSR(), int),
    NTupleSubObject("l1",  lambda x : x.leg1,leptonTypeHZZ),
    NTupleSubObject("l2",  lambda x : x.leg2,leptonTypeHZZ),
    NTupleVariable("mll",  lambda x : (x.leg1.p4() + x.leg2.p4()).M(), help="Dilepton mass, without FSR"),
])
ZTypeLite = NTupleObjectType("ZTypeLite", baseObjectTypes=[fourVectorType], variables = [
    NTupleVariable("hasFSR",   lambda x : x.hasFSR(), int),
    NTupleSubObject("l1",  lambda x : x.leg1,leptonTypeHZZLite),
    NTupleSubObject("l2",  lambda x : x.leg2,leptonTypeHZZLite),
    NTupleVariable("mll",  lambda x : (x.leg1.p4() + x.leg2.p4()).M(), help="Dilepton mass, without FSR"),
])



ZZType = NTupleObjectType("ZZType", baseObjectTypes=[fourVectorType], variables = [
    NTupleVariable("hasFSR",   lambda x : x.hasFSR(), int),
    NTupleSubObject("z1",  lambda x : x.leg1, ZType),
    NTupleSubObject("z2",  lambda x : x.leg2, ZType),
    NTupleVariable("mll_12",   lambda x : (x.leg1.leg1.p4()+x.leg1.leg2.p4()).M()),
    NTupleVariable("mll_13",   lambda x : (x.leg1.leg1.p4()+x.leg2.leg1.p4()).M()),
    NTupleVariable("mll_14",   lambda x : (x.leg1.leg1.p4()+x.leg2.leg2.p4()).M()),
    NTupleVariable("mll_23",   lambda x : (x.leg1.leg2.p4()+x.leg2.leg1.p4()).M()),
    NTupleVariable("mll_24",   lambda x : (x.leg1.leg2.p4()+x.leg2.leg2.p4()).M()),
    NTupleVariable("mll_34",   lambda x : (x.leg2.leg1.p4()+x.leg2.leg2.p4()).M()),
    # -------
    NTupleVariable("nJet30", lambda x : len(x.cleanJets), int, help="Number of jets (after cleaning with tight leptons + leptons of the candidate, and their FSR photons)"),
    NTupleVariable("j1ptzs", lambda x : x.cleanJets[1-1].pt() if len(x.cleanJets) >= 1 else -1, help="Jet 1 pt, or -1 if not found"),
    NTupleVariable("j2ptzs", lambda x : x.cleanJets[2-1].pt() if len(x.cleanJets) >= 2 else -1, help="Jet 2 pt, or -1 if not found"),
    NTupleVariable("j1qglzs", lambda x : x.cleanJets[1-1].qgl() if len(x.cleanJets) >= 1 else -1, help="Jet 1 QGL, or -1 if not found"),
    NTupleVariable("j2qglzs", lambda x : x.cleanJets[2-1].qgl() if len(x.cleanJets) >= 2 else -1, help="Jet 2 QGL, or -1 if not found"),
    NTupleVariable("ij1",    lambda x : x.cleanJetIndices[1-1] if len(x.cleanJetIndices) >= 1 else -1, int, help="Index of 1st jet after cleaning"),
    NTupleVariable("ij2",    lambda x : x.cleanJetIndices[2-1] if len(x.cleanJetIndices) >= 2 else -1, int, help="Index of 2nd jet after cleaning"),
    NTupleVariable("ij3",    lambda x : x.cleanJetIndices[3-1] if len(x.cleanJetIndices) >= 3 else -1, int, help="Index of 3rd jet after cleaning"),
    NTupleVariable("ij4",    lambda x : x.cleanJetIndices[4-1] if len(x.cleanJetIndices) >= 4 else -1, int, help="Index of 4th jet after cleaning"),
    NTupleVariable("ij5",    lambda x : x.cleanJetIndices[5-1] if len(x.cleanJetIndices) >= 5 else -1, int, help="Index of 5th jet after cleaning"),
    NTupleVariable("ij6",    lambda x : x.cleanJetIndices[6-1] if len(x.cleanJetIndices) >= 6 else -1, int, help="Index of 6th jet after cleaning"),
    NTupleVariable("ij7",    lambda x : x.cleanJetIndices[7-1] if len(x.cleanJetIndices) >= 7 else -1, int, help="Index of 7th jet after cleaning"),
    NTupleVariable("ij8",    lambda x : x.cleanJetIndices[8-1] if len(x.cleanJetIndices) >= 8 else -1, int, help="Index of 8th jet after cleaning"),
    NTupleVariable("ij9",    lambda x : x.cleanJetIndices[9-1] if len(x.cleanJetIndices) >= 9 else -1, int, help="Index of 9th jet after cleaning"),
    NTupleVariable("ij10",    lambda x : x.cleanJetIndices[10-1] if len(x.cleanJetIndices) >= 10 else -1, int, help="Index of 10th jet after cleaning"),
    NTupleVariable("ij11",    lambda x : x.cleanJetIndices[11-1] if len(x.cleanJetIndices) >= 11 else -1, int, help="Index of 11th jet after cleaning"),
    NTupleVariable("ij12",    lambda x : x.cleanJetIndices[12-1] if len(x.cleanJetIndices) >= 12 else -1, int, help="Index of 12th jet after cleaning"),
    NTupleVariable("ij13",    lambda x : x.cleanJetIndices[13-1] if len(x.cleanJetIndices) >= 13 else -1, int, help="Index of 13th jet after cleaning"),
    NTupleVariable("ij14",    lambda x : x.cleanJetIndices[14-1] if len(x.cleanJetIndices) >= 14 else -1, int, help="Index of 14th jet after cleaning"),
    NTupleVariable("ij15",    lambda x : x.cleanJetIndices[15-1] if len(x.cleanJetIndices) >= 15 else -1, int, help="Index of 15th jet after cleaning"),
    # -------
    NTupleVariable("KD",   lambda x : getattr(x, 'KD', -1.0), help="MELA KD"),
    NTupleVariable("MELAcosthetastar", lambda x : x.melaAngles.costhetastar if hasattr(x,'melaAngles') else -99.0, help="MELA angle costhetastar"),
    NTupleVariable("MELAcostheta1", lambda x : x.melaAngles.costheta1 if hasattr(x,'melaAngles') else -99.0, help="MELA angle costheta1"),
    NTupleVariable("MELAcostheta2", lambda x : x.melaAngles.costheta2 if hasattr(x,'melaAngles') else -99.0, help="MELA angle costheta2"),
    NTupleVariable("MELAphi", lambda x : x.melaAngles.phi if hasattr(x,'melaAngles') else -99.0, help="MELA angle phi"),
    NTupleVariable("MELAphistar1", lambda x : x.melaAngles.phistar1 if hasattr(x,'melaAngles') else -99.0, help="MELA angle phistar1"),
    NTupleVariable("D_bkg_kin",   lambda x : x.KDs["D_bkg^kin"], help="MELA D_bkg^kin"),
    NTupleVariable("D_bkg",   lambda x : x.KDs["D_bkg"], help="MELA D_bkg"),
    NTupleVariable("D_gg",   lambda x : x.KDs["D_gg"], help="MELA D_gg"),
    NTupleVariable("D_0m",   lambda x : x.KDs["D_0-"], help="MELA D_0-"),
    NTupleVariable("Dkin_HJJ_VBF",   lambda x : x.KDs["D_HJJ^VBF"], help="MELA D_HJJ^VBF"),
    NTupleVariable("Dkin_HJJ_VBF_2", lambda x : x.KDs["D_HJJ^VBF"] if len(x.cleanJets) >= 2 else -1, help="MELA D_HJJ^VBF (2-jet version)"),
    NTupleVariable("Dkin_HJJ_VBF_1", lambda x : x.KDs["D_HJJ^VBF"] if len(x.cleanJets) == 1 else -1, help="MELA D_HJJ^VBF (1-jet version)"),
    NTupleVariable("Dkin_HJJ_WH",    lambda x : x.KDs["D_HJJ^WH"], help="MELA D_HJJ^WH"),
    NTupleVariable("Dkin_HJJ_ZH",    lambda x : x.KDs["D_HJJ^ZH"], help="MELA D_HJJ^ZH"),
    NTupleVariable("Dfull_HJJ_VBF_2", lambda x : x.KDs["D_VBF2J"] if len(x.cleanJets) >= 2 else -1, help="Full D_HJJ^VBF (2-jet version)"),
    NTupleVariable("Dfull_HJJ_VBF_1", lambda x : x.KDs["D_VBF1J"] if len(x.cleanJets) == 1 else -1, help="Full D_HJJ^VBF (1-jet version)"),
    NTupleVariable("Dfull_HJJ_WH",    lambda x : x.KDs["D_WHh"] if len(x.cleanJets) >= 2 else -1, help="Full D_HJJ^WH"),
    NTupleVariable("Dfull_HJJ_ZH",    lambda x : x.KDs["D_ZHh"] if len(x.cleanJets) >= 2 else -1, help="Full D_HJJ^ZH"),
])


WZType = NTupleObjectType("WZType", baseObjectTypes=[fourVectorType], variables = [
    NTupleVariable("hasFSR",   lambda x : x.hasFSR(), int),
    NTupleSubObject("z",  lambda x : x.z, ZType),
    NTupleSubObject("lep3",  lambda x : x.lep3, leptonTypeHZZ),
    NTupleVariable("mll_12",   lambda x : (x.z.leg1.p4()+x.z.leg2.p4()).M()),
    NTupleVariable("mll_13",   lambda x : (x.z.leg1.p4()+x.lep3.p4()).M()),
    NTupleVariable("mll_23",   lambda x : (x.z.leg2.p4()+x.lep3.p4()).M()),
   ## -------
   #NTupleVariable("nJet30", lambda x : len(x.cleanJets), int, help="Number of jets (after cleaning with tight leptons + leptons of the candidate, and their FSR photons)"),
   #NTupleVariable("ij1",    lambda x : x.cleanJetIndices[1-1] if len(x.cleanJetIndices) >= 1 else -1, int, help="Index of 1st jet after cleaning"),
   #NTupleVariable("ij2",    lambda x : x.cleanJetIndices[2-1] if len(x.cleanJetIndices) >= 2 else -1, int, help="Index of 2nd jet after cleaning"),
   #NTupleVariable("ij3",    lambda x : x.cleanJetIndices[3-1] if len(x.cleanJetIndices) >= 3 else -1, int, help="Index of 3rd jet after cleaning"),
   #NTupleVariable("ij4",    lambda x : x.cleanJetIndices[4-1] if len(x.cleanJetIndices) >= 4 else -1, int, help="Index of 4th jet after cleaning"),
   #NTupleVariable("ij5",    lambda x : x.cleanJetIndices[5-1] if len(x.cleanJetIndices) >= 5 else -1, int, help="Index of 5th jet after cleaning"),
   #NTupleVariable("ij6",    lambda x : x.cleanJetIndices[6-1] if len(x.cleanJetIndices) >= 6 else -1, int, help="Index of 6th jet after cleaning"),
   #NTupleVariable("ij7",    lambda x : x.cleanJetIndices[7-1] if len(x.cleanJetIndices) >= 7 else -1, int, help="Index of 7th jet after cleaning"),
   #NTupleVariable("ij8",    lambda x : x.cleanJetIndices[8-1] if len(x.cleanJetIndices) >= 8 else -1, int, help="Index of 8th jet after cleaning"),
   #NTupleVariable("ij9",    lambda x : x.cleanJetIndices[9-1] if len(x.cleanJetIndices) >= 9 else -1, int, help="Index of 9th jet after cleaning"),
   #NTupleVariable("ij10",    lambda x : x.cleanJetIndices[10-1] if len(x.cleanJetIndices) >= 10 else -1, int, help="Index of 10th jet after cleaning"),
   #NTupleVariable("ij11",    lambda x : x.cleanJetIndices[11-1] if len(x.cleanJetIndices) >= 11 else -1, int, help="Index of 11th jet after cleaning"),
   #NTupleVariable("ij12",    lambda x : x.cleanJetIndices[12-1] if len(x.cleanJetIndices) >= 12 else -1, int, help="Index of 12th jet after cleaning"),
   #NTupleVariable("ij13",    lambda x : x.cleanJetIndices[13-1] if len(x.cleanJetIndices) >= 13 else -1, int, help="Index of 13th jet after cleaning"),
   #NTupleVariable("ij14",    lambda x : x.cleanJetIndices[14-1] if len(x.cleanJetIndices) >= 14 else -1, int, help="Index of 14th jet after cleaning"),
   #NTupleVariable("ij15",    lambda x : x.cleanJetIndices[15-1] if len(x.cleanJetIndices) >= 15 else -1, int, help="Index of 15th jet after cleaning"),
])



