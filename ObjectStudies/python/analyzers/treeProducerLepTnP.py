from PhysicsTools.Heppy.analyzers.core.AutoFillTreeProducer  import * 
import PhysicsTools.HeppyCore.framework.config as cfg

leptonTypeTnP = NTupleObjectType("leptonTnP", baseObjectTypes = [ leptonType ], variables = [
    NTupleVariable("looseId",     lambda x : x.looseIdSusy, int, help="Loose ID (as per lepton analyzer)"),
    # ----------------------
    NTupleVariable("eleMVASpring15_VLooseIdEmu", lambda x : x.electronID("POG_MVA_ID_Spring15_NonTrig_VLooseIdEmu") if abs(x.pdgId())==11 else 1, int, help="VLoose MVA Ele ID (as per susy)"),
    NTupleVariable("eleMVASpring15_HZZ",         lambda x : x.electronID("MVA_ID_NonTrig_Spring15_HZZ")             if abs(x.pdgId())==11 else 1, int, help="MVA Ele ID (as per hzz)"),
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
     ], 
     globalObjects = {
        #"met" : NTupleObject("met", metType, help="PF E_{T}^{miss}, after type 1 corrections"),
     },
     collections = {
        "TnP" : NTupleCollection("TnP", tnpType, 20, help="Dilepton Candidates"),    
     },
     defaultFloatType = 'F',
)

