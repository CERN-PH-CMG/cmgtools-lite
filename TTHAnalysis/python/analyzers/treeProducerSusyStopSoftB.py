from CMGTools.TTHAnalysis.analyzers.treeProducerSusyCore import *
from CMGTools.TTHAnalysis.analyzers.ntupleTypes import *

susyStopSoftB_globalVariables = susyCore_globalVariables + [
    ##-------- custom jets ------------------------------------------
    NTupleVariable("htJet20j", lambda ev : ev.htJetXj, help="H_{T} computed from leptons and jets (with |eta|<2.4, pt > 20 GeV)"),
    NTupleVariable("mhtJet20", lambda ev : ev.mhtJetX, help="H_{T}^{miss} computed from leptons and jets (with |eta|<2.4, pt > 20 GeV)"),
    NTupleVariable("htJet25j", lambda ev : ev.htJet25j, help="H_{T} computed from leptons and jets (with |eta|<2.4, pt > 25 GeV)"),
    NTupleVariable("mhtJet25", lambda ev : ev.mhtJet25, help="H_{T}^{miss} computed from leptons and jets (with |eta|<2.4, pt > 25 GeV)"),
    NTupleVariable("htJet40j", lambda ev : ev.htJet40j, help="H_{T} computed from only jets (with |eta|<2.4, pt > 40 GeV)"),
    NTupleVariable("mhtJet40", lambda ev : ev.mhtJet40, help="H_{T}^{miss} computed from leptons and jets (with |eta|<2.4, pt > 40 GeV)"),
    ## -------------------------------------------------------------
    NTupleVariable("nBJetsLoose20",  lambda ev : sum([j.pt()>20 and j.btagWP("CSVv2IVFL") for j in ev.cleanJets]), int, help="N(b-jets, pt > 20, CSVv2IVFL"),
    NTupleVariable("nBJetsMedium20", lambda ev : sum([j.pt()>20 and j.btagWP("CSVv2IVFM") for j in ev.cleanJets]), int, help="N(b-jets, pt > 20, CSVv2IVFM"),
    NTupleVariable("nBJetsTight20",  lambda ev : sum([j.pt()>20 and j.btagWP("CSVv2IVFT") for j in ev.cleanJets]), int, help="N(b-jets, pt > 20, CSVv2IVFT"),
    NTupleVariable("nBJetsLoose40",  lambda ev : sum([j.pt()>40 and j.btagWP("CSVv2IVFL") for j in ev.cleanJets]), int, help="N(b-jets, pt > 40, CSVv2IVFL"),
    NTupleVariable("nBJetsMedium40", lambda ev : sum([j.pt()>40 and j.btagWP("CSVv2IVFM") for j in ev.cleanJets]), int, help="N(b-jets, pt > 40, CSVv2IVFM"),
    NTupleVariable("nBJetsTight40",  lambda ev : sum([j.pt()>40 and j.btagWP("CSVv2IVFT") for j in ev.cleanJets]), int, help="N(b-jets, pt > 40, CSVv2IVFT"),
    ## -------------------------------------------------------------
    NTupleVariable("mtB1", lambda ev: ev.mtB1, help="M_{T}(b1, MET), where b_1 is the first  highest-CSVv2-tagged jet; -99 if missing"),
    NTupleVariable("mtB2", lambda ev: ev.mtB2, help="M_{T}(b2, MET), where b_2 is the second highest-CSVv2-tagged jet; -99 if missing"),
    NTupleVariable("dphiJet1Met", lambda ev: ev.dphiJet1Met, help="deltaPhi(j1, MET), where j1 is the leading jet by pT; -99 if missing"),
    NTupleVariable("dphiJet2Met", lambda ev: ev.dphiJet2Met, help="deltaPhi(j2, MET), where j2 is the leading jet by pT; -99 if missing"),
    NTupleVariable("dphiJet3Met", lambda ev: ev.dphiJet3Met, help="deltaPhi(j3, MET), where j3 is the leading jet by pT; -99 if missing"),
    NTupleVariable("dphiJet4Met", lambda ev: ev.dphiJet4Met, help="deltaPhi(j4, MET), where j4 is the leading jet by pT; -99 if missing"),
    ## -------------------------------------------------------------
    NTupleVariable("hbheFilterNew", lambda ev: ev.hbheFilterNew25ns, int, help="new HBHE filter for 25 ns"),
    NTupleVariable("hbheFilterIso", lambda ev: ev.hbheFilterIso, int, help="HBHE iso-based noise filter"),
    NTupleVariable("firstPVIsGood", lambda ev: (ev.vertices[0].ndof() == ev.goodVertices[0].ndof()) if len(ev.goodVertices) > 0 else 0, int, help="first PV is good"),
    NTupleVariable("Flag_badChargedHadronFilter", lambda ev: ev.badChargedHadron, help="bad charged hadron filter decision"),
    NTupleVariable("Flag_badMuonFilter", lambda ev: ev.badMuon, help="bad muon filter decision"),
]

susyStopSoftB_globalObjects = susyCore_globalObjects.copy()
susyStopSoftB_globalObjects.update({
    "ISRJet" : NTupleObject("ISRJet", jetTypeSusyExtraLight, help="Lead non-b jet (may be missing)", nillable=True),
})

susyStopSoftB_collections = susyCore_collections.copy()
susyStopSoftB_collections.update({
    ##--------------------------------------------------
    "selectedTaus"    : NTupleCollection("TauGood",  tauTypeSusy, 8, help="Taus after the preselection"),
    "selectedLeptons" : NTupleCollection("LepGood",  leptonTypeSusyExtraLight, 8, help="Leptons after the preselection"),
    "otherLeptons"    : NTupleCollection("LepOther", leptonTypeSusyExtraLight, 8, help="Leptons failing the preselection"),
    "otherTaus"       : NTupleCollection("TauOther", tauTypeSusy, 8, help="Taus failing the preselection"),
    ##------------------------------------------------
    "cleanJets"       : NTupleCollection("Jet",     jetTypeSusyExtraLight, 15, help="Cental jets after full selection and cleaning, sorted by pt"),
    "cleanJetsFwd"    : NTupleCollection("JetFwd",  jetTypeSusyExtraLight,  6, help="Forward jets after full selection and cleaning, sorted by pt"),            
    "fatJets"         : NTupleCollection("FatJet",  fatJetType,  15, help="AK8 jets, sorted by pt"),
    "iBs"             : NTupleCollection("iBJet",   objectInt, 15, help="index of b-jets (CSVv2 M, sorted by discriminator)"),
    ##------------------------------------------------
    "discardedJets"    : NTupleCollection("DiscJet", jetTypeSusyExtraLight, 15, help="Jets discarted in the jet-lepton cleaning"),
    #"discardedLeptons" : NTupleCollection("DiscLep", leptonTypeSusy, 8, help="Leptons discarded in the jet-lepton cleaning"),
    #"recoveredJets"    : NTupleCollection("RecJet", jetTypeSusy, 15, help="Jets recovered declustering in the jet-lepton cleaning"),
    #"recoveredSplitJets" : NTupleCollection("RecSplitJet", jetTypeSusy, 15, help="Jets recovered declustering in the jet-lepton cleaning, split"),
    ##------------------------------------------------
    "ivf"       : NTupleCollection("SV",     svTypeExtra, 20, help="SVs from IVF"),
    "genBHadrons"  : NTupleCollection("GenBHad", heavyFlavourHadronType, 20, mcOnly=True, help="Gen-level B hadrons"),
    "genDHadrons"  : NTupleCollection("GenDHad", heavyFlavourHadronType, 20, mcOnly=True, help="Gen-level D hadrons"),
    ##------------------------------------------------
    "LHE_weights"    : NTupleCollection("LHEweight",  weightsInfoType, 1000, mcOnly=True, help="LHE weight info"),
})
