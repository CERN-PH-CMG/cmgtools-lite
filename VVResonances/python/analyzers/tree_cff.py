from PhysicsTools.Heppy.analyzers.core.AutoFillTreeProducer  import *
from CMGTools.VVResonances.analyzers.vvTypes  import *
from CMGTools.VVResonances.analyzers.Skimmer  import *
import PhysicsTools.HeppyCore.framework.config as cfg

vvSkimmer = cfg.Analyzer(
    Skimmer,
    name='vvSkimmer',
    required = ['LNuJJ','JJ','LLJJ','JJNuNu']
)

vTauSkimmer = cfg.Analyzer(
    Skimmer,
    name='vTauSkimmer',
    required = ['TauTau','TauJet','TauTauLoose','TauJetLoose']
)

leptonSkimmer = cfg.Analyzer(
    Skimmer,
    name='leptonSkimmer',
    required = ['inclusiveLeptons']
)


vvTreeProducer = cfg.Analyzer(
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
#            "genleps"          : NTupleCollection("gen",     genParticleWithLinksType, 10, help="Generated leptons (e/mu) from W/Z decays"),
#            "inclusiveLeptons" : NTupleCollection("l",    leptonTypeExtra, 10, help="Inclusive Leptons"),
        "LNuJJ" : NTupleCollection("lnujj",LNuJJType ,5, help="VV candidate with a lepton neutrino and a fat jet"),
#        "TopCR" : NTupleCollection("topCR",LNuJJType ,5, help="Top control region candidate with a lepton neutrino and a fat jet"),
        "JJ" : NTupleCollection("jj",JJType ,5, help="VV candidate with two fat jets"),
        "LLJJ" : NTupleCollection("lljj",LLJJType ,5, help="VV candidate with two leptons and a fat jet"),
        "JJNuNu" : NTupleCollection("nunujj",NuNuJJType ,5, help="VV candidate with  fat jet and MET")
#        "leadJetConstituents" : NTupleCollection("jetConstituents",     particleType, 500, help="Constituents"),

#            "genVBosons" : NTupleCollection("genV",     genParticleWithLinksType, 10, help="Generated V bosons"),
     }
)



vTauTreeProducer = cfg.Analyzer(
     AutoFillTreeProducer, name='vTauTreeProducer',
     vectorTree = True,
     saveTLorentzVectors = False,  # can set to True to get also the TLorentzVectors, but trees will be bigger
     defaultFloatType = 'F', # use Float_t for floating point
#     PDFWeights = PDFWeights,
     globalVariables = [
        NTupleVariable("rho",  lambda ev: ev.rho, float, help="kt6PFJets rho"),
        NTupleVariable("rhoCN",  lambda ev: ev.rhoCN, float, help="fixed grid rho central neutral"),
        NTupleVariable("nVert",  lambda ev: len(ev.goodVertices), int, help="Number of good vertices"),
     ],
     globalObjects =  {
            "met" : NTupleObject("met", metType, help="PF E_{T}^{miss}, after type 1 corrections"),
     },

     collections = {
        "TauTau" : NTupleCollection("tautau",TauTauType ,5, help="4 taus"),
        "TauJet" : NTupleCollection("taujet",TauJetType ,5, help="2 taus and merged jet"),
        "TauTauLoose" : NTupleCollection("tautauLoose",TauTauType ,5, help="4 taus"),
        "TauJetLoose" : NTupleCollection("taujetLoose",TauJetType ,5, help="2 taus and merged jet"),

     }
)



leptonTreeProducer = cfg.Analyzer(
     AutoFillTreeProducer, name='leptonTreeProducer',
     vectorTree = True,
     saveTLorentzVectors = False,  # can set to True to get also the TLorentzVectors, but trees will be bigger
     defaultFloatType = 'F', # use Float_t for floating point
#     PDFWeights = PDFWeights,
#     globalVariables = susyMultilepton_globalVariables,
#     globalObjects = susyMultilepton_globalObjects,
     collections = {
            "genleps"          : NTupleCollection("gen",     genParticleWithLinksType, 10, help="Generated leptons (e/mu) from W/Z decays"),
            "inclusiveLeptons" : NTupleCollection("l",    leptonTypeExtra, 10, help="Inclusive Leptons"),
     }
)
