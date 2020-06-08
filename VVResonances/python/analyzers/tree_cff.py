from PhysicsTools.Heppy.analyzers.core.AutoFillTreeProducer  import *
from CMGTools.VVResonances.analyzers.vvTypes  import *
from CMGTools.VVResonances.analyzers.Skimmer  import *
import PhysicsTools.HeppyCore.framework.config as cfg

vvSkimmer = cfg.Analyzer(
    Skimmer,
    name='vvSkimmer',
    required = ['LNuJJ']
)

vvTreeProducer = cfg.Analyzer(
     AutoFillTreeProducer, name='vvTreeProducer',
     vectorTree = True,
     saveTLorentzVectors = False,  # can set to True to get also the TLorentzVectors, but trees will be bigger
     defaultFloatType = 'F', # use Float_t for floating point
#     PDFWeights = PDFWeights,
     globalVariables = [
        NTupleVariable("year",  lambda ev: 2016, int, help="processing year"),
        NTupleVariable("rho",  lambda ev: ev.rho, float, help="kt6PFJets rho"),
        NTupleVariable("rhoCN",  lambda ev: ev.rhoCN, float, help="fixed grid rho central neutral"),
        NTupleVariable("nVert",  lambda ev: len(ev.goodVertices), int, help="Number of good vertices"),
        NTupleVariable("Flag_badChargedHadronFilter", lambda ev: ev.badChargedHadron, help="bad charged hadron filter decision"),
        NTupleVariable("Flag_BadMuonFilter", lambda ev: ev.badMuon, help="bad muon filter decision"),
        NTupleVariable("L1PrefireWeight", lambda ev: ev.prefiringWeight, help="prefiring weight"),
        NTupleVariable("L1PrefireWeightUp", lambda ev: ev.prefiringWeightUp, help="prefiring weight"),
        NTupleVariable("L1PrefireWeightDown", lambda ev: ev.prefiringWeightDown, help="prefiring weight"),
     ],
     globalObjects =  {
            "met" : NTupleObject("met", metType, help="PF E_{T}^{miss}, after type 1 corrections"),
     },

     collections = {
        "LNuJJ" : NTupleCollection("lnujj",LNuJJType ,5, help="VV candidate with a lepton neutrino and a fat jet"),
        "LLJJ" : NTupleCollection("lljj",LLJJType ,5, help="VV candidate with two leptons and a fat jet"),
#        "JJNuNu": NTupleCollection("nunujj", NuNuJJType, 5, help="VV candidate with  fat jet and MET"),
        "TruthType": NTupleCollection("truth", TruthType, 5, help="generator level information")
     }
)
