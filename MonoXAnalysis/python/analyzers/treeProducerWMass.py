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

            ## ------- lheHT, needed for merging HT binned samples 
            NTupleVariable("lheHT", lambda ev : getattr(ev,"lheHT",-999), mcOnly=True, help="H_{T} computed from quarks and gluons in Heppy LHEAnalyzer"),
            NTupleVariable("lheHTIncoming", lambda ev : getattr(ev,"lheHTIncoming",-999), mcOnly=True, help="H_{T} computed from quarks and gluons in Heppy LHEAnalyzer (only LHE status<0 as mothers)"),

            ##--------------------------------------------------            
            NTupleVariable("mZ1", lambda ev : ev.bestZ1[0], help="Best m(ll) SF/OS"),
]

wmass_globalObjects = {
            "met"   : NTupleObject("met", metType, help="PF E_{T}^{miss}, after type 1 corrections"),
            "tkMet" : NTupleObject("tkMet", fourVectorType, help="PF E_{T}^{miss} from charged candidates with dz<0.1"),
            "tkMetPVchs" : NTupleObject("tkMetPVchs", fourVectorType, help="PF E_{T}^{miss} from charged candidates with chs"),
            "tkMetPVLoose" : NTupleObject("tkMetPVLoose", fourVectorType, help="PF E_{T}^{miss} from charged candidates with Loose chs"),
            "tkMetPVTight" : NTupleObject("tkMetPVTight", fourVectorType, help="PF E_{T}^{miss} from charged candidates with Tight chs"),
}

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
            "LHE_weights"    : NTupleCollection("LHEweight",  weightsInfoType, 1000, mcOnly=True, help="LHE weight info"),
            ##------------------------------------------------
            #"genleps"         : NTupleCollection("genLep",     genParticleWithLinksType, 10, help="Generated leptons (e/mu) from W/Z decays"),                                                                                                
            #"gentauleps"      : NTupleCollection("genLepFromTau", genParticleWithLinksType, 10, help="Generated leptons (e/mu) from decays of taus from W/Z/h decays"),                                                                       
            #"gentaus"         : NTupleCollection("genTau",     genParticleWithLinksType, 10, help="Generated leptons (tau) from W/Z decays"),                            
            "generatorSummary" : NTupleCollection("GenPart", genParticleWithLinksType, 20 , help="Hard scattering particles, with ancestry and links"),
}

