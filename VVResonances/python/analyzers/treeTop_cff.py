from PhysicsTools.Heppy.analyzers.core.AutoFillTreeProducer  import *
from CMGTools.VVResonances.analyzers.vvTypes  import *
from CMGTools.VVResonances.analyzers.Skimmer  import *
import PhysicsTools.HeppyCore.framework.config as cfg

ttSkimmer = cfg.Analyzer(
    Skimmer,
    name='ttSkimmer',
    required = ['TT','WbT','WbWb']
)

ttTreeProducer = cfg.Analyzer(
     AutoFillTreeProducer, name='vvTreeProducer',
     vectorTree = True,
     saveTLorentzVectors = False,  # can set to True to get also the TLorentzVectors, but trees will be bigger
     defaultFloatType = 'F', # use Float_t for floating point
#     PDFWeights = PDFWeights,
     globalVariables = [
        NTupleVariable("rho",  lambda ev: ev.rho, float, help="kt6PFJets rho"),
        NTupleVariable("rhoCN",  lambda ev: ev.rhoCN, float, help="fixed grid rho central neutral"),
        NTupleVariable("nVert",  lambda ev: len(ev.goodVertices), int, help="Number of good vertices"),
        NTupleVariable("Flag_badChargedHadronFilter", lambda ev: ev.badChargedHadron, help="bad charged hadron filter decision"),
        NTupleVariable("Flag_badMuonFilter", lambda ev: ev.badMuon, help="bad muon filter decision"),
     ],
     globalObjects =  {
            "met" : NTupleObject("met", metType, help="PF E_{T}^{miss}, after type 1 corrections"),
     },

     collections = {
        "TT" : NTupleCollection("tt",JJType ,5, help="TT candidate with two fat jets"),
        "WbT" : NTupleCollection("WbT",WbJJType ,5, help="VV candidate with a top decaying to W jet and separate b jet and a top merged jet"),
        "WbWb" : NTupleCollection("WbWb",WbWbType ,5, help="VV candidate with  two unmerged tops but ,merged W")
     }
)



