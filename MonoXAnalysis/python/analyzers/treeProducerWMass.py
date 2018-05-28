from PhysicsTools.Heppy.analyzers.core.AutoFillTreeProducer  import * 

from CMGTools.TTHAnalysis.analyzers.ntupleTypes import *
from CMGTools.MonoXAnalysis.analyzers.ntupleTypes import *

wmass_globalVariables = [

            NTupleVariable("Flag_badMuonMoriond2017",  lambda ev: ev.badMuonMoriond2017, int, help="bad muon found in event (Moriond 2017 filter)?"),
            NTupleVariable("Flag_badCloneMuonMoriond2017",  lambda ev: ev.badCloneMuonMoriond2017, int, help="clone muon found in event (Moriond 2017 filter)?"),
            NTupleVariable("badCloneMuonMoriond2017_maxPt",  lambda ev: max(mu.pt() for mu in ev.badCloneMuonMoriond2017_badMuons) if not ev.badCloneMuonMoriond2017 else 0, help="max pt of any clone muon found in event (Moriond 2017 filter)"),
            NTupleVariable("badNotCloneMuonMoriond2017_maxPt",  lambda ev: max((mu.pt() if mu not in ev.badCloneMuonMoriond2017_badMuons else 0) for mu in ev.badMuonMoriond2017_badMuons) if not ev.badMuonMoriond2017 else 0, help="max pt of any bad non-clone muon found in event (Moriond 2017 filter)"),


            NTupleVariable("rho",  lambda ev: ev.rho, float, help="kt6PFJets rho"),
            NTupleVariable("rhoCN",  lambda ev: ev.rhoCN, float, help="fixed grid rho central neutral"),
            NTupleVariable("nVert",  lambda ev: len(ev.goodVertices), int, help="Number of good vertices"), 
            ## NTupleVariable("nTrueInt",  lambda ev: ev.nTrueInteractions, mcOnly=True, int, help="Number of true interaction from MC"), 

            ## ------- lheHT, needed for merging HT binned samples 
            NTupleVariable("lheHT", lambda ev : getattr(ev,"lheHT",-999), mcOnly=True, help="H_{T} computed from quarks and gluons in Heppy LHEAnalyzer"),
            NTupleVariable("lheHTIncoming", lambda ev : getattr(ev,"lheHTIncoming",-999), mcOnly=True, help="H_{T} computed from quarks and gluons in Heppy LHEAnalyzer (only LHE status<0 as mothers)"),

            ##--------------------------------------------------            
            NTupleVariable("mZ1", lambda ev : ev.bestZ1[0], help="Best m(ll) SF/OS"),

            ##--------------------------------------------------
            NTupleVariable("puppimet_sumEt",       lambda ev : getattr(ev,'met_sumetpuppi'),       help="Puppi Sum E_{T}"),
            NTupleVariable("met_sumEt",            lambda ev : getattr(ev,'met_sumet'),            help="Puppi Sum E_{T}"),
            NTupleVariable("tkGenMet_sumEt",       lambda ev : getattr(ev,'tkGenMet').sumEt,  mcOnly=True,       help="Gen charged Sum E_{T} eta<2.4"),   
            NTupleVariable("tkGenMetInc_sumEt",    lambda ev : getattr(ev,'tkGenMetInc').sumEt,  mcOnly=True, help="Gen charged Sum E_{T} eta<5"),   
            NTupleVariable("tkMetPVchs_sumEt",     lambda ev : getattr(ev,'tkMetPVchs').sumEt,     help="Sum E_{T} from charged candidates with chs"),
            NTupleVariable("tkMetPVLoose_sumEt",   lambda ev : getattr(ev,'tkMetPVLoose').sumEt,   help="Sum E_{T} from charged candidates with Loose chs"),
            NTupleVariable("tkMetPUPVLoose_sumEt", lambda ev : getattr(ev,'tkMetPUPVLoose').sumEt, help="Sum E_{T} from PU charged candidates with Loose chs"),
            NTupleVariable("tkMetPVTight_sumEt",   lambda ev : getattr(ev,'tkMetPVTight').sumEt,   help="Sum E_{T} from charged candidates with Tight chs"),            
            NTupleVariable("ntMet_sumEt",          lambda ev : getattr(ev,'ntMet').sumEt,          help="Sum E_{T} from neutral PF candidates"),
            NTupleVariable("ntCentralMet_sumEt",   lambda ev : getattr(ev,'ntCentralMet').sumEt,   help="Sum E_{T} from neutral PF candidates with eta<2.4"),            

            NTupleVariable("tkMetPVchs_Count",     lambda ev : getattr(ev,'tkMetPVchs_Count'),     help="Count of charged candidates with chs"),
            NTupleVariable("tkMetPVLoose_Count",   lambda ev : getattr(ev,'tkMetPVLoose_Count'),   help="Count of from charged candidates with Loose chs"),
            NTupleVariable("tkMetPUPVLoose_Count", lambda ev : getattr(ev,'tkMetPUPVLoose_Count'), help="Count of from PU charged candidates with Loose chs"),
            NTupleVariable("tkMetPVTight_Count",   lambda ev : getattr(ev,'tkMetPVTight_Count'),   help="Count of from charged candidates with Tight chs"),            
            NTupleVariable("ntMet_Count",          lambda ev : getattr(ev,'ntMet_Count'),          help="Count of from neutral PF candidates"),
            NTupleVariable("ntCentralMet_Count",   lambda ev : getattr(ev,'ntCentralMet_Count'),   help="Count of from neutral PF candidates with eta<2.4"),            
]

wmass_globalObjects = {
    ##--------------------------------------------------
    "tkGenMet"     :   NTupleObject("tkGenMet",       fourVectorType,  mcOnly=True, help="Gen charged E_{T}^{miss} eta<2.4"),
    "tkGenMetInc"  :   NTupleObject("tkGenMetInc",    fourVectorType,  mcOnly=True, help="Gen charged E_{T}^{miss} eta<5"),
    "met"          :   NTupleObject("met",            fourVectorType, help="PF E_{T}^{miss}, after type 1 corrections"),
    "metpuppi"     :   NTupleObject("puppimet",       fourVectorType, help="Puppi E_{T}^{miss}"),
    "tkMetPVchs"   :   NTupleObject("tkMetPVchs",     fourVectorType, help="PF E_{T}^{miss} from charged candidates with chs"),
    "tkMetPVLoose" :   NTupleObject("tkMetPVLoose",   fourVectorType, help="PF E_{T}^{miss} from charged candidates with Loose chs"),
    "tkMetPUPVLoose" : NTupleObject("tkMetPUPVLoose", fourVectorType, help="PF E_{T}^{miss} from PU charged candidates with Loose chs"),
    "tkMetPVTight" :   NTupleObject("tkMetPVTight",   fourVectorType, help="PF E_{T}^{miss} from charged candidates with Tight chs"),
    "ntMet"        :   NTupleObject("ntMet",          fourVectorType, help="PF E_{T}^{miss} from neutral candidates"),
    "ntCentralMet" :   NTupleObject("ntCentralMet",   fourVectorType, help="PF E_{T}^{miss} from neutral eta<2.4 candidates"),
    "leadCharged"  :   NTupleObject("leadCharged",    fourVectorType, help="leading pT charged PF candidate"),
    "leadNeutral"  :   NTupleObject("leadNeutral",    fourVectorType, help="leading pT neutral PF candidate"),
}

##------------------------------------------  
## PDFs
##------------------------------------------  

pdfsVariables = [
        NTupleVariable("x1", lambda ev: ev.pdf_x1, mcOnly=True, help="fraction of proton momentum carried by the first parton"),
        NTupleVariable("x2", lambda ev: ev.pdf_x2, mcOnly=True, help="fraction of proton momentum carried by the second parton"),
        NTupleVariable("id1", lambda ev: ev.pdf_id1, int, mcOnly=True, help="id of the first parton in the proton"),
        NTupleVariable("id2", lambda ev: ev.pdf_id2, int, mcOnly=True, help="id of the second parton in the proton"),
        ]

wmass_collections = {
            "selectedLeptons" : NTupleCollection("LepGood",  leptonTypeWMass, 8, help="Leptons after the preselection"),
            #"otherLeptons"    : NTupleCollection("LepOther", leptonTypeSusy, 8, help="Leptons after the preselection"),
            ##------------------------------------------------
            "cleanJets"       : NTupleCollection("Jet",     jetTypeSusyExtraLight, 15, help="Cental jets after full selection and cleaning, sorted by pt"),
            #"cleanJetsFwd"    : NTupleCollection("JetFwd",  jetTypeSusy,  6, help="Forward jets after full selection and cleaning, sorted by pt"),            
            #"fatJets"         : NTupleCollection("FatJet",  fatJetType,  15, help="AK8 jets, sorted by pt"),
            ##------------------------------------------------
            #"ivf"       : NTupleCollection("SV",     svType, 20, help="SVs from IVF"),
            ##------------------------------------------------
            #"LHE_weights"    : NTupleCollection("LHEweight",  weightsInfoType, 1000, mcOnly=True, help="LHE weight info"),
            ##------------------------------------------------
            #"genleps"         : NTupleCollection("genLep",     genParticleWithLinksType, 10, help="Generated leptons (e/mu) from W/Z decays"),                                                                                                
            #"gentauleps"      : NTupleCollection("genLepFromTau", genParticleWithLinksType, 10, help="Generated leptons (e/mu) from decays of taus from W/Z/h decays"),                                                                       
            #"gentaus"         : NTupleCollection("genTau",     genParticleWithLinksType, 10, help="Generated leptons (tau) from W/Z decays"),                            
            "generatorSummary" : NTupleCollection("GenPart", genParticleWithLinksType, 50 , mcOnly=True, help="Hard scattering particles, with ancestry and links"),
}

