from PhysicsTools.Heppy.analyzers.core.AutoFillTreeProducer  import *
from CMGTools.TTHAnalysis.analyzers.ttHTypes import *

ttH_globalVariables = [
            NTupleVariable("rho",  lambda ev: ev.rho, float, help="kt6PFJets rho"),
            NTupleVariable("rhoCN",  lambda ev: ev.rhoCN, float, help="fixed grid rho central neutral"),
            NTupleVariable("nVert",  lambda ev: len(ev.goodVertices), int, help="Number of good vertices"),
            NTupleVariable("PV_ndof",  lambda ev: (ev.goodVertices if ev.goodVertices else ev.vertices)[0].ndof(), float, help="Degrees of freedom of PV"),

            NTupleVariable("nJet25", lambda ev: sum([j.pt() > 25 for j in ev.cleanJets]), int, help="Number of jets with pt > 25, |eta|<2.4"),
            NTupleVariable("nJet25a", lambda ev: sum([j.pt() > 25 for j in ev.cleanJetsAll]), int, help="Number of jets with pt > 25, |eta|<4.7"),
            NTupleVariable("nBJetLoose25", lambda ev: sum([j.btagWP("DeepCSVL") for j in ev.cleanJets if j.pt() > 25]), int, help="Number of jets with pt > 25 passing DeepCSV loose"),
            NTupleVariable("nBJetMedium25", lambda ev: sum([j.btagWP("DeepCSVM") for j in ev.cleanJets if j.pt() > 25]), int, help="Number of jets with pt > 25 passing DeepCSV medium"),
            NTupleVariable("nBJetTight25", lambda ev: sum([j.btagWP("DeepCSVT") for j in ev.cleanJets if j.pt() > 25]), int, help="Number of jets with pt > 25 passing DeepCSV tight"),

            NTupleVariable("nJet30", lambda ev: sum([j.pt() > 30 for j in ev.cleanJets]), int, help="Number of jets with pt > 30, |eta|<2.4"),
            NTupleVariable("nJet30a", lambda ev: sum([j.pt() > 30 for j in ev.cleanJetsAll]), int, help="Number of jets with pt > 30, |eta|<4.7"),
            NTupleVariable("nBJetLoose30", lambda ev: sum([j.btagWP("DeepCSVL") for j in ev.cleanJets if j.pt() > 30]), int, help="Number of jets with pt > 30 passing DeepCSV loose"),
            NTupleVariable("nBJetMedium30", lambda ev: sum([j.btagWP("DeepCSVM") for j in ev.cleanJets if j.pt() > 30]), int, help="Number of jets with pt > 30 passing DeepCSV medium"),
            NTupleVariable("nBJetTight30", lambda ev: sum([j.btagWP("DeepCSVT") for j in ev.cleanJets if j.pt() > 30]), int, help="Number of jets with pt > 30 passing DeepCSV tight"),

            NTupleVariable("nJet40", lambda ev: sum([j.pt() > 40 for j in ev.cleanJets]), int, help="Number of jets with pt > 40, |eta|<2.4"),
            NTupleVariable("nJet40a", lambda ev: sum([j.pt() > 40 for j in ev.cleanJetsAll]), int, help="Number of jets with pt > 40, |eta|<4.7"),
            NTupleVariable("nBJetLoose40", lambda ev: sum([j.btagWP("DeepCSVL") for j in ev.cleanJets if j.pt() > 40]), int, help="Number of jets with pt > 40 passing DeepCSV loose"),
            NTupleVariable("nBJetMedium40", lambda ev: sum([j.btagWP("DeepCSVM") for j in ev.cleanJets if j.pt() > 40]), int, help="Number of jets with pt > 40 passing DeepCSV medium"),
            NTupleVariable("nBJetTight40", lambda ev: sum([j.btagWP("DeepCSVT") for j in ev.cleanJets if j.pt() > 40]), int, help="Number of jets with pt > 40 passing DeepCSV tight"),
            ## ------- lheHT, needed for merging HT binned samples
            NTupleVariable("lheHT", lambda ev : getattr(ev,"lheHT",-999), mcOnly=True, help="H_{T} computed from quarks and gluons in Heppy LHEAnalyzer"),
            NTupleVariable("lheHTIncoming", lambda ev : getattr(ev,"lheHTIncoming",-999), mcOnly=True, help="H_{T} computed from quarks and gluons in Heppy LHEAnalyzer (only LHE status<0 as mothers)"),

            ##-------- custom jets ------------------------------------------
            NTupleVariable("htJet25", lambda ev : ev.htJet25, help="H_{T} computed from leptons and jets (with |eta|<2.4, pt > 25 GeV)"),
            NTupleVariable("mhtJet25", lambda ev : ev.mhtJet25, help="H_{T}^{miss} computed from leptons and jets (with |eta|<2.4, pt > 25 GeV)"),
            NTupleVariable("htJet40j", lambda ev : ev.htJet40j, help="H_{T} computed from only jets (with |eta|<2.4, pt > 40 GeV)"),
            NTupleVariable("htJet40ja", lambda ev : ev.htJet40ja, help="H_{T} computed from only jets (with |eta|<4.7, pt > 40 GeV)"),
            NTupleVariable("htJet40", lambda ev : ev.htJet40, help="H_{T} computed from leptons and jets (with |eta|<2.4, pt > 40 GeV)"),
            NTupleVariable("htJet40a", lambda ev : ev.htJet40a, help="H_{T} computed from leptons and jets (with |eta|<4.7, pt > 40 GeV)"),
            NTupleVariable("mhtJet40", lambda ev : ev.mhtJet40, help="H_{T}^{miss} computed from leptons and jets (with |eta|<2.4, pt > 40 GeV)"),
            ##--------------------------------------------------
            NTupleVariable("mZ1", lambda ev : ev.bestZ1[0], help="Best m(ll) SF/OS"),
            NTupleVariable("mZ1SFSS", lambda ev : ev.bestZ1sfss[0], help="Best m(ll) SF/SS"),
            NTupleVariable("minMllSFOS", lambda ev: ev.minMllSFOS, help="min m(ll), SF/OS"),
            NTupleVariable("maxMllSFOS", lambda ev: ev.maxMllSFOS, help="max m(ll), SF/OS"),
            NTupleVariable("minMllAFOS", lambda ev: ev.minMllAFOS, help="min m(ll), AF/OS"),
            NTupleVariable("maxMllAFOS", lambda ev: ev.maxMllAFOS, help="max m(ll), AF/OS"),
            NTupleVariable("minMllAFSS", lambda ev: ev.minMllAFSS, help="min m(ll), AF/SS"),
            NTupleVariable("maxMllAFSS", lambda ev: ev.maxMllAFSS, help="max m(ll), AF/SS"),
            NTupleVariable("minMllAFAS", lambda ev: ev.minMllAFAS, help="min m(ll), AF/AS"),
            NTupleVariable("maxMllAFAS", lambda ev: ev.maxMllAFAS, help="max m(ll), AF/AS"),
            NTupleVariable("m2l", lambda ev: ev.m2l, help="m(ll)"),
            ##--------------------------------------------------
            NTupleVariable("minDrllAFSS", lambda ev: ev.minDrllAFSS, help="min Dr(ll), AF/SS"),
            NTupleVariable("maxDrllAFSS", lambda ev: ev.maxDrllAFSS, help="max Dr(ll), AF/SS"),
            NTupleVariable("minDrllAFOS", lambda ev: ev.minDrllAFOS, help="min Dr(ll), AF/OS"),
            NTupleVariable("maxDrllAFOS", lambda ev: ev.maxDrllAFOS, help="max Dr(ll), AF/OS"),
            ##--------------------------------------------------
            NTupleVariable("mZ2", lambda ev : ev.bestZ2[3], help="m(ll) of second SF/OS pair, for ZZ reco."),
            NTupleVariable("m3l", lambda ev: ev.m3l, help="m(3l)"),
            NTupleVariable("m4l", lambda ev: ev.m4l, help="m(4l)"),
            NTupleVariable("pt2l", lambda ev: ev.pt2l, help="p_{T}(ll)"),
            NTupleVariable("pt3l", lambda ev: ev.pt3l, help="p_{T}(3l)"),
            NTupleVariable("pt4l", lambda ev: ev.pt4l, help="p_{T}(4l)"),
            NTupleVariable("ht3l", lambda ev: ev.ht3l, help="H_{T}(3l)"),
            NTupleVariable("ht4l", lambda ev: ev.ht4l, help="H_{T}(4l)"),
            NTupleVariable("q3l", lambda ev: ev.q3l, int, help="q(3l)"),
            NTupleVariable("q4l", lambda ev: ev.q4l, int, help="q(4l)"),
            ##--------------------------------------------------
            NTupleVariable("GenHiggsDecayMode", lambda ev : ev.genHiggsDecayMode, int, mcOnly=True, help="H decay mode (15 = tau, 23/24 = W/Z)"),
            ##--------------------------------------------------
            NTupleVariable("nLepGood20", lambda ev: sum([l.pt() > 20 for l in ev.selectedLeptons]), int, help="Number of leptons with pt > 20"),
            NTupleVariable("nLepGood15", lambda ev: sum([l.pt() > 15 for l in ev.selectedLeptons]), int, help="Number of leptons with pt > 15"),
            NTupleVariable("nLepGood10", lambda ev: sum([l.pt() > 10 for l in ev.selectedLeptons]), int, help="Number of leptons with pt > 10"),
            ##--------------------------------------------------
            NTupleVariable("prescaleFromSkim", lambda ev : getattr(ev, "prescaleFromSkim", 1), help="event prescale from the skimming module"),
]

ttH_globalObjects = {
            "met" : NTupleObject("met", metType, help="PF E_{T}^{miss}, after type 1 corrections"),
}

ttH_collections = {
            "genleps"         : NTupleCollection("genLep",     genParticleWithAncestryType, 10, help="Generated leptons (e/mu) from W/Z decays"),
            "gentauleps"      : NTupleCollection("genLepFromTau", genParticleWithAncestryType, 10, help="Generated leptons (e/mu) from decays of taus from W/Z/h decays"),
            "gentaus"         : NTupleCollection("genTau",     genParticleWithAncestryType, 10, help="Generated leptons (tau) from W/Z decays"),
            "gentopquarks"    : NTupleCollection("GenTop",     genParticleType, 2, help="Generated top quarks from hard scattering (needed separately for top pt reweighting)"),
            ##--------------------------------------------------
            "selectedTaus"    : NTupleCollection("TauGood",  tauTypeSusy, 8, help="Taus after the preselection"),
            "selectedLeptons" : NTupleCollection("LepGood",  leptonTypeSusy, 8, help="Leptons after the preselection"),
            ##------------------------------------------------
            "cleanJets"       : NTupleCollection("Jet",     jetTypeSusy, 15, help="Cental jets after full selection and cleaning, sorted by pt"),
            "cleanJetsFwd"    : NTupleCollection("JetFwd",  jetTypeSusyFwd,  6, help="Forward jets after full selection and cleaning, sorted by pt"),
            #"ivf"            : NTupleCollection("SV",     svType, 20, help="SVs from IVF"),
            ##------------------------------------------------
            "LHE_weights"     : NTupleCollection("LHEweight",  weightsInfoType, 2000, mcOnly=True, help="LHE weight info"),
}

def setLossyFloatCompression(precision=12,highPrecision=-1):
    for t in fourVectorType, leptonType, leptonTypeSusy:
        for v in t.ownVars(True):
            if v.type != float: continue
            if v.name in ("pt","eta","mvaTTH") or "mvaId" in v.name:
                v.setPrecision(highPrecision)
            else:
                v.setPrecision(precision)
    for v in tlorentzFourVectorType.ownVars(True):
        v.setPrecision(precision)
    for t in tauType, jetType, jetTypeExtra, metType: 
        for v in t.ownVars(True):
            if v.type != float: continue
            if v.name in ("pt","eta","btagCSV","btagDeepCSV"):
                v.setPrecision(highPrecision)
            else:
                v.setPrecision(precision)
    for v in ttH_globalVariables:
        if v.type != float: continue
        v.setPrecision(precision)
