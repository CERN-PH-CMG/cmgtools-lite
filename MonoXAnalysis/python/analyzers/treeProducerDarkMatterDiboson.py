from CMGTools.MonoXAnalysis.analyzers.treeProducerDarkMatterMonoJet import *
from CMGTools.TTHAnalysis.analyzers.ntupleTypes import *

puppiJetType = NTupleObjectType("puppiJet",  baseObjectTypes = [ jetTypeSusyExtra ], variables = [
        NTupleVariable("massCorrected",  lambda x : x.puppiMassCorrected,  float, help="puppi corrected mass"),
        ])
puppiFatJetType = NTupleObjectType("puppiFatJet",  baseObjectTypes = [ fourVectorType ], variables = [
        NTupleVariable("massCorrected",  lambda x : x.massCorrected,  float, help="puppi corrected mass for AK08"),
        ])

dmDiboson_globalVariables = dmMonoJet_globalVariables + [
        NTupleVariable("rhoCN", lambda ev: ev.rhoCN, float, help="fixed grid rho central neutral"),
        #NTupleVariable("nTrueInteractions", lambda ev: ev.nPU if ev.nPU!=None else -99, int, help="Total number of true interactions"),

]


dmDiboson_globalObjects = dmMonoJet_globalObjects.copy()
dmDiboson_globalObjects.update({
        # put more here
        "metPuppi" : NTupleObject("metPuppi", metType, help="PF E_{T}^{miss}, after type 1 corrections (Puppi)"),
         #"metPuppi_jecUp" : NTupleObject("metPuppi_jecUp", metType, help="PF E_{T}^{miss}, after type 1 corrections with JEC up variation (Puppi)"),
         #"metPuppi_jecDown" : NTupleObject("metPuppi_jecDown", metType, help="PF E_{T}^{miss}, after type 1 corrections with JEC down variation (Puppi)"),
})

dmDiboson_collections = dmMonoJet_collections.copy()
dmDiboson_collections.update({
            # put more here
            "puppiJets"       : NTupleCollection("PuppiJet",  puppiJetType,       20, help="Puppi jets, sorted by pt"),
            "subJetPuppi"     : NTupleCollection("PuppiSubJet",  fourVectorType,       20, help="Puppi ak08 subJets, sorted by pt"),
            "subJetSoftDrop"  : NTupleCollection("SoftDropSubJet",  fourVectorType,       20, help="SoftDrop ak08 subJets, sorted by pt"),
            "customPuppiAK8"  : NTupleCollection("customPuppiAK8",  puppiFatJetType,       20, help="Puppi ak08 Jets, sorted by pt"), 
})
