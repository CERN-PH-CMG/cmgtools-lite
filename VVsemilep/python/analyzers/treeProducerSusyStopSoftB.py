from CMGTools.TTHAnalysis.analyzers.treeProducerSusyCore import *
from CMGTools.TTHAnalysis.analyzers.ntupleTypes import *

leptonTypeDigest = NTupleObjectType("leptonTypeDigest",  baseObjectTypes = [ particleType ], variables = [
    NTupleVariable("charge",   lambda x : x.charge(), int),
    NTupleVariable("tightId",     lambda x : x.tightId(), int, help="POG Tight ID (for electrons it's configured in the analyzer)"),
    NTupleVariable("dxy",   lambda x : x.dxy(), help="d_{xy} with respect to PV, in cm (with sign)"),
    NTupleVariable("dz",    lambda x : x.dz() , help="d_{z} with respect to PV, in cm (with sign)"),
    NTupleVariable("ip3d",  lambda x : x.ip3D() , help="d_{3d} with respect to PV, in cm (absolute value)"),
    NTupleVariable("sip3d",  lambda x : x.sip3D(), help="S_{ip3d} with respect to PV (significance)"),
    NTupleVariable("convVeto",    lambda x : x.passConversionVeto() if abs(x.pdgId())==11 else 1, int, help="Conversion veto (always true for muons)"),
    NTupleVariable("lostHits",    lambda x : (x.gsfTrack() if abs(x.pdgId())==11 else x.innerTrack()).hitPattern().numberOfLostHits(ROOT.reco.HitPattern.MISSING_INNER_HITS), int, help="Number of lost hits on inner track"),
    NTupleVariable("relIso03",  lambda x : x.relIso03, help="PF Rel Iso, R=0.3, pile-up corrected"),
    NTupleVariable("miniRelIso",  lambda x : x.miniRelIso if hasattr(x,'miniRelIso') else  -999, help="PF Rel miniRel, pile-up corrected"),
    NTupleVariable("mcMatchId",  lambda x : getattr(x, 'mcMatchId', -99), int, mcOnly=True, help="Match to source from hard scatter (pdgId of heaviest particle in chain, 25 for H, 6 for t, 23/24 for W/Z), zero if non-prompt or fake"),
    NTupleVariable("mcMatchAny", lambda x : getattr(x, 'mcMatchAny', -99), int, mcOnly=True, help="Match to any final state leptons: 0 if unmatched, 1 if light flavour (including prompt), 4 if charm, 5 if bottom"),
    NTupleVariable("ICHEPmediumMuonId",   lambda x : x.muonID("POG_ID_Medium_ICHEP") if abs(x.pdgId())==13 else 1, int, help="Muon POG Medium id with fix for ICHEP 2016"), 
    NTupleVariable("nStations",    lambda lepton : lepton.numberOfMatchedStations() if abs(lepton.pdgId()) == 13 else 4, help="Number of matched muons stations (4 for electrons)"),
    NTupleVariable("mvaTTH",    lambda lepton : getattr(lepton, 'mvaValueTTH', -1), help="Lepton MVA (TTH version)"),
    NTupleVariable("mvaIdSpring16HZZ",   lambda lepton : lepton.mvaRun2("Spring16HZZ") if abs(lepton.pdgId()) == 11 else 1, help="EGamma POG MVA ID, Spring16, HZZ; 1 for muons"),
    NTupleVariable("jetPtRatiov2", lambda lepton: lepton.pt()/jetLepAwareJEC(lepton).Pt() if hasattr(lepton,'jet') else -1, help="pt(lepton)/[rawpt(jet-PU-lep)*L2L3Res+pt(lepton)]"),
    NTupleVariable("jetPtRelv2", lambda lepton : ptRelv2(lepton) if hasattr(lepton,'jet') else -1, help="pt of the lepton transverse to the jet axis (subtracting the lepton) - v2"),
    NTupleVariable("jetBTagCSV", lambda lepton : lepton.jet.btag('pfCombinedInclusiveSecondaryVertexV2BJetTags') if hasattr(lepton,'jet') and hasattr(lepton.jet, 'btag') else -99, help="CSV btag of nearest jet"),
])

jetTypeDigest = NTupleObjectType("jetTypeDigest",  baseObjectTypes = [ fourVectorType  ], variables = [
    NTupleVariable("id",    lambda x : x.jetID("POG_PFID") , int, mcOnly=False,help="POG Loose jet ID"),
    NTupleVariable("btagCSV",   lambda x : x.btag('pfCombinedInclusiveSecondaryVertexV2BJetTags'), help="CSV-IVF v2 discriminator"),
    NTupleVariable("ctagCsvL", lambda x : x.btag('pfCombinedCvsLJetTags'), float, help="CsvL discriminator"),
    NTupleVariable("ctagCsvB", lambda x : x.btag('pfCombinedCvsBJetTags'), float, help="CsvB discriminator"),
    NTupleVariable("corr_JECUp",  lambda x : getattr(x, 'corrJECUp', -99), float,  help=""),
    NTupleVariable("corr_JECDown",  lambda x : getattr(x, 'corrJECDown', -99), float,help=""),
    NTupleVariable("corr",  lambda x : getattr(x, 'corr', -99), float, help=""),
    NTupleVariable("partonFlavour", lambda x : x.partonFlavour(), int,     mcOnly=True, help="purely parton-based flavour"),
    NTupleVariable("hadronFlavour", lambda x : x.hadronFlavour(), int,     mcOnly=True, help="hadron flavour (ghost matching to B/C hadrons)"),
])



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
    #"selectedTaus"    : NTupleCollection("TauGood",  tauTypeSusy, 8, help="Taus after the preselection"),
    "selectedLeptons" : NTupleCollection("LepGood",  leptonTypeDigest, 8, help="Leptons after the preselection"),
    "otherLeptons"    : NTupleCollection("LepOther", leptonTypeDigest, 8, help="Leptons failing the preselection"),
    #"otherTaus"       : NTupleCollection("TauOther", tauTypeSusy, 8, help="Taus failing the preselection"),
    ##------------------------------------------------
    "cleanJets"       : NTupleCollection("Jet",     jetTypeDigest, 15, help="Cental jets after full selection and cleaning, sorted by pt"),
    "cleanJetsFwd"    : NTupleCollection("JetFwd",  jetTypeDigest,  6, help="Forward jets after full selection and cleaning, sorted by pt"),            
    #"fatJets"         : NTupleCollection("FatJet",  fatJetType,  15, help="AK8 jets, sorted by pt"),
    #"iBs"             : NTupleCollection("iBJet",   objectInt, 15, help="index of b-jets (CSVv2 M, sorted by discriminator)"),
    ##------------------------------------------------
    #"discardedJets"    : NTupleCollection("DiscJet", jetTypeSusyExtraLight, 15, help="Jets discarted in the jet-lepton cleaning"),
    #"discardedLeptons" : NTupleCollection("DiscLep", leptonTypeSusy, 8, help="Leptons discarded in the jet-lepton cleaning"),
    #"recoveredJets"    : NTupleCollection("RecJet", jetTypeSusy, 15, help="Jets recovered declustering in the jet-lepton cleaning"),
    #"recoveredSplitJets" : NTupleCollection("RecSplitJet", jetTypeSusy, 15, help="Jets recovered declustering in the jet-lepton cleaning, split"),
    ##------------------------------------------------
    "ivf"       : NTupleCollection("SV",     svTypeExtra, 20, help="SVs from IVF"),
    #"genBHadrons"  : NTupleCollection("GenBHad", heavyFlavourHadronType, 20, mcOnly=True, help="Gen-level B hadrons"),
    #"genDHadrons"  : NTupleCollection("GenDHad", heavyFlavourHadronType, 20, mcOnly=True, help="Gen-level D hadrons"),
    ##------------------------------------------------
    "LHE_weights"    : NTupleCollection("LHEweight",  weightsInfoType, 1000, mcOnly=True, help="LHE weight info"),
})
