from PhysicsTools.Heppy.analyzers.core.AutoFillTreeProducer  import * 

dmCore_globalVariables = [
            NTupleVariable("rhoCN", lambda ev: ev.rhoCN, float, help="fixed grid rho central neutral"),
            NTupleVariable("rho",  lambda ev: ev.rho, float, help="kt6PFJets rho"),
            NTupleVariable("nVert",  lambda ev: len(ev.goodVertices), int, help="Number of good vertices"),

            #NTupleVariable("nTrueInters1", lambda ev: ev.nTrueInt, float, help="Total number of true interactions"),
            NTupleVariable("nTrueInters", lambda ev: len(ev.vertices), float, help="Total number of true interactions"),#ev.slimmedAddPileupInfo.getTrueNumInteractions, float, help="Total number of true interactions"),
            NTupleVariable("nTrueInteractions", lambda ev: ev.nPU if ev.nPU!=None else -99, int, help="Total number of true interactions"),

            NTupleVariable("nJet25", lambda ev: len(ev.cleanJets), int, help="Number of jets with pt > 25"),
            NTupleVariable("nBJetLoose25", lambda ev: len(ev.bjetsLoose), int, help="Number of jets with pt > 25 passing CSV loose"),
            NTupleVariable("nBJetMedium25", lambda ev: len(ev.bjetsMedium), int, help="Number of jets with pt > 25 passing CSV medium"),
            NTupleVariable("nBJetTight25", lambda ev: sum([j.btagWP("CSVv2IVFT") for j in ev.bjetsMedium]), int, help="Number of jets with pt > 25 passing CSV tight"),

            NTupleVariable("nJet30", lambda ev: sum([j.pt() > 30 for j in ev.cleanJets]), int, help="Number of jets with pt > 30, |eta|<2.4"),
            NTupleVariable("nJet30a", lambda ev: sum([j.pt() > 30 for j in ev.cleanJetsAll]), int, help="Number of jets with pt > 30, |eta|<4.7"),
            NTupleVariable("nBJetLoose30", lambda ev: sum([j.btagWP("CSVv2IVFL") for j in ev.cleanJets if j.pt() > 30]), int, help="Number of jets with pt > 30 passing CSV loose"),
            NTupleVariable("nBJetMedium30", lambda ev: sum([j.btagWP("CSVv2IVFM") for j in ev.bjetsMedium if j.pt() > 30]), int, help="Number of jets with pt > 30 passing CSV medium"),
            NTupleVariable("nBJetTight30", lambda ev: sum([j.btagWP("CSVv2IVFT") for j in ev.bjetsMedium if j.pt() > 30]), int, help="Number of jets with pt > 30 passing CSV tight"),

            NTupleVariable("nJet40", lambda ev: sum([j.pt() > 40 for j in ev.cleanJets]), int, help="Number of jets with pt > 40, |eta|<2.4"),
            NTupleVariable("nJet40a", lambda ev: sum([j.pt() > 40 for j in ev.cleanJetsAll]), int, help="Number of jets with pt > 40, |eta|<4.7"),
            NTupleVariable("nBJetLoose40", lambda ev: sum([j.btagWP("CSVv2IVFL") for j in ev.cleanJets if j.pt() > 40]), int, help="Number of jets with pt > 40 passing CSV loose"),
            NTupleVariable("nBJetMedium40", lambda ev: sum([j.btagWP("CSVv2IVFM") for j in ev.bjetsMedium if j.pt() > 40]), int, help="Number of jets with pt > 40 passing CSV medium"),
            NTupleVariable("nBJetTight40", lambda ev: sum([j.btagWP("CSVv2IVFT") for j in ev.bjetsMedium if j.pt() > 40]), int, help="Number of jets with pt > 40 passing CSV tight"),

            ##--------------------------------------------------
            NTupleVariable("nLepGood20", lambda ev: sum([l.pt() > 20 for l in ev.selectedLeptons]), int, help="Number of leptons with pt > 20"),
            NTupleVariable("nLepGood15", lambda ev: sum([l.pt() > 15 for l in ev.selectedLeptons]), int, help="Number of leptons with pt > 15"),
            NTupleVariable("nLepGood10", lambda ev: sum([l.pt() > 10 for l in ev.selectedLeptons]), int, help="Number of leptons with pt > 10"),
            ##--------------------------------------------------
            #NTupleVariable("GenHeaviestQCDFlavour", lambda ev : ev.heaviestQCDFlavour, int, mcOnly=True, help="pdgId of heaviest parton in the event (after shower)"),
            #NTupleVariable("LepEff_1lep", lambda ev : ev.LepEff_1lep, mcOnly=True, help="Lepton preselection SF (1 lep)"),
            #NTupleVariable("LepEff_2lep", lambda ev : ev.LepEff_2lep, mcOnly=True, help="Lepton preselection SF (2 lep)"),
            ##------------------------------------------------
]

dmCore_globalObjects = {
            "met" : NTupleObject("met", metType, help="PF E_{T}^{miss}, after type 1 corrections"),
            "metNoMu" : NTupleObject("metNoMu", metType, help="PF E_{T}^{miss}, with muon pt added back"),
            "metNoPU" : NTupleObject("metNoPU", fourVectorType, help="PF noPU E_{T}^{miss}"),
            "metPuppi" : NTupleObject("metPuppi", metType, help="PF E_{T}^{miss}, after type 1 corrections (Puppi)"),
            #"metPuppi_jecUp" : NTupleObject("metPuppi_jecUp", metType, help="PF E_{T}^{miss}, after type 1 corrections with JEC up variation (Puppi)"),
            #"metPuppi_jecDown" : NTupleObject("metPuppi_jecDown", metType, help="PF E_{T}^{miss}, after type 1 corrections with JEC down variation (Puppi)"),
}

dmCore_collections = {
            "genJets"          : NTupleCollection("genJet",  genParticleType, 10, help="Generated jets (not cleaned)"),
            "genleps"          : NTupleCollection("genLep",  genParticleWithLinksType, 10, help="Generated leptons (e/mu) from W/Z decays"),
            "generatorSummary" : NTupleCollection("GenPart", genParticleWithLinksType, 100 , help="Hard scattering particles, with ancestry and links"),
}
