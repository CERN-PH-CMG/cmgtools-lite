import PhysicsTools.HeppyCore.framework.config as cfg
from PhysicsTools.Heppy.analyzers.core.AutoFillTreeProducer  import * 
from CMGTools.ObjectStudies.analyzers.leptonTriggerMatching_cff import WithLeptonTriggerMatchType

leptonTypeTnP = NTupleObjectType("leptonTnP", baseObjectTypes = [ leptonType, WithLeptonTriggerMatchType ], variables = [
    NTupleVariable("looseId",     lambda x : x.looseIdSusy, int, help="Loose ID (as per lepton analyzer)"),
    NTupleVariable("mvaIdSpring15",   lambda lepton : lepton.mvaRun2("NonTrigSpring15MiniAOD") if abs(lepton.pdgId()) == 11 else 1, help="EGamma POG MVA ID for non-triggering electrons, Spring15 re-training; 1 for muons"),
    NTupleVariable("mvaIdSpring16",   lambda lepton : lepton.mvaRun2("Spring16HZZ") if abs(lepton.pdgId()) == 11 else 1, help="EGamma POG MVA ID, Spring16; 1 for muons"),
    # ----------------------
    NTupleVariable("eleMVASpring15_VLooseIdEmu", lambda x : x.electronID("POG_MVA_ID_Spring15_NonTrig_VLooseIdEmu") if abs(x.pdgId())==11 else 1, int, help="VLoose MVA Ele ID (as per susy)"),
    NTupleVariable("eleMVASpring15_HZZ",         lambda x : x.electronID("MVA_ID_NonTrig_Spring15_HZZ")             if abs(x.pdgId())==11 else 1, int, help="MVA Ele ID (as per hzz)"),
    NTupleVariable("SOSTightID2017",             lambda x : (x.electronID("MVA_ID_nonIso_Fall17_wp90") if x.pt()<10 else x.electronID("MVA_ID_nonIso_Fall17_SUSYTight")) if abs(x.pdgId())==11 else 0, int, help="SOS tight electron MVA noIso ID 2017 (WP: POG wp90 below 10 GeV, SUSYTight above)"),
    NTupleVariable("SUSYVLooseFOFall17",         lambda x : x.electronID("MVA_ID_nonIso_Fall17_SUSYVLooseFO")       if abs(x.pdgId())==11 and x.pt()> 5 else 1, int, help="SUSYVLooseFOFall17"),
    NTupleVariable("SUSYVLooseFall17",           lambda x : x.electronID("MVA_ID_nonIso_Fall17_SUSYVLoose")         if abs(x.pdgId())==11 and x.pt()> 5 else 1, int, help="SUSYVLooseFall17"),
    NTupleVariable("SUSYTightFall17",            lambda x : x.electronID("MVA_ID_nonIso_Fall17_SUSYTight")          if abs(x.pdgId())==11 and x.pt()>10 else 1, int, help="SUSYTightFall17"),

    # ----------------------
    NTupleVariable("etaSc", lambda x : x.superCluster().eta() if abs(x.pdgId())==11 else -100, help="Electron supercluster pseudorapidity"),
    NTupleVariable("isGap", lambda x : x.isGap() if abs(x.pdgId())==11 else False, int, help="is this a Gap electron"),
    NTupleVariable("r9",    lambda x : x.r9() if abs(x.pdgId())==11 else 1.0, help="electron r9"),
    # ----------------------
    NTupleVariable("trkIso03", lambda x : (x.dr03TkSumPt() if abs(x.pdgId())==11 else x.isolationR03().sumPt)/x.pt(), help="TrkIso R=0.3"),
    NTupleVariable("trkIso045", lambda x : (x.dr04TkSumPt() if abs(x.pdgId())==11 else x.isolationR05().sumPt)/x.pt(), help="TrkIso R=0.4 (e), 0.5 (mu)"),
])

tnpType = NTupleObjectType("tnpType", baseObjectTypes=[fourVectorType], variables = [
    NTupleSubObject("tag",   lambda x : x.tag,   leptonTypeTnP),
    NTupleSubObject("probe", lambda x : x.probe, leptonTypeTnP),
])

treeProducerTnP = cfg.Analyzer(
     AutoFillTreeProducer, name='treeProducerTnP',
     vectorTree = True,
     saveTLorentzVectors = False,  # can set to True to get also the TLorentzVectors, but trees will be bigger
     globalVariables = [
        NTupleVariable("nVert",  lambda ev: len(ev.goodVertices), int, help="Number of good vertices"),
        NTupleVariable("nJet20", lambda ev: sum([j.pt() > 20 for j in ev.cleanJets]), int, help="Number of jets with pt > 20"),
        NTupleVariable("nJet25", lambda ev: sum([j.pt() > 25 for j in ev.cleanJets]), int, help="Number of jets with pt > 25"),
        NTupleVariable("nJet30", lambda ev: sum([j.pt() > 30 for j in ev.cleanJets]), int, help="Number of jets with pt > 30"),
        NTupleVariable("nJet40", lambda ev: sum([j.pt() > 40 for j in ev.cleanJets]), int, help="Number of jets with pt > 40"),
     ], 
     globalObjects = {
        "met" : NTupleObject("met", metType, help="PF E_{T}^{miss}, after type 1 corrections"),
     },
     collections = {
        "TnP" : NTupleCollection("TnP", tnpType, 20, help="Dilepton Candidates"),    
     },
     defaultFloatType = 'F',
)

