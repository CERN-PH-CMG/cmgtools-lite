from CMGTools.TTHAnalysis.analyzers.ntupleTypes import *

leptonTypeStop4Body = NTupleObjectType("leptonStop4Body", baseObjectTypes= [ leptonTypeSusy ], variables = [
    NTupleVariable("cosPhiLepMet", lambda x : x.cosLMet,  help="Cos phi of the lepton and met  "),
    NTupleVariable("mt",           lambda x : x.mt,       help="Transverse Mass calculated for lepton"),
    NTupleVariable("Q80",          lambda x : x.Q80  ,    help="Q80 variable for the deconstrcuted transverse mass")
])

genJetType = NTupleObjectType("genJets",  baseObjectTypes = [ fourVectorType ], mcOnly=True, variables = [
    NTupleVariable("nConstituents", lambda x : x.nConstituents(), help="Number of Constituents"),
])
