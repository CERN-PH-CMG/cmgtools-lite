##########################################################
##          T&P COMMON MODULES ARE DEFINED HERE         ##
##########################################################
import PhysicsTools.HeppyCore.framework.config as cfg

from PhysicsTools.Heppy.analyzers.core.all import *
from PhysicsTools.Heppy.analyzers.objects.all import *
from PhysicsTools.Heppy.analyzers.gen.all import *

##------------------------------------------
##  Core modules
##------------------------------------------

from CMGTools.ObjectStudies.analyzers.treeProducerLepTnP import treeProducerTnP
from CMGTools.ObjectStudies.analyzers.ZTagAndProbeAnalyzer import ZTagAndProbeAnalyzer
from CMGTools.TTHAnalysis.analyzers.ttHFastLepSkimmer import ttHFastLepSkimmer
from CMGTools.ObjectStudies.analyzers.leptonTriggerMatching_cff import LeptonTriggerMatchersSequence

skimAnalyzer = cfg.Analyzer(
    SkimAnalyzerCount, name='skimAnalyzerCount',
    useLumiBlocks = False,
    )

# Apply json file (if the dataset has one)
jsonAna = cfg.Analyzer(
    JSONAnalyzer, name="JSONAnalyzer",
    )

# Filter using the 'triggers' and 'vetoTriggers' specified in the dataset
triggerAna = cfg.Analyzer(
    TriggerBitFilter, name="TriggerBitFilter",
    )

# Fast skimming
fastSkim1LTag = cfg.Analyzer( ttHFastLepSkimmer, name="fastSkim1LTag",
        muons = 'slimmedMuons',         muCut  = lambda mu  : mu.pt()  > 25 and mu.isMediumMuon() and mu.pfIsolationR03().sumChargedHadronPt < 0.2*mu.pt(),
        electrons = 'slimmedElectrons', eleCut = lambda ele : ele.pt() > 25                       and ele.pfIsolationVariables().sumChargedHadronPt < 0.2*ele.pt(),
        minLeptons = 1,
)
fastSkim2L = cfg.Analyzer( ttHFastLepSkimmer, name="fastSkim2L",
        muons = 'slimmedMuons', muCut = lambda mu : mu.pt() > 3.5,
        electrons = 'slimmedElectrons', eleCut = lambda ele : ele.pt() > 5,
        minLeptons = 2,
)



# Create flags for trigger bits
triggerFlagsAna = cfg.Analyzer(
    TriggerBitAnalyzer, name="TriggerFlags",
    processName = 'HLT',
    triggerBits = {
        # "<name>" : [ 'HLT_<Something>_v*', 'HLT_<SomethingElse>_v*' ] 
    }
    )

# Select a list of good primary vertices (generic)
vertexAna = cfg.Analyzer(
    VertexAnalyzer, name="VertexAnalyzer",
    vertexWeight = None,
    fixedWeight = 1,
    verbose = False
    )


# This analyzer actually does the pile-up reweighting (generic)
pileUpAna = cfg.Analyzer(
    PileUpAnalyzer, name="PileUpAnalyzer",
    true = True,  # use number of true interactions for reweighting
    makeHists=False
    )

##------------------------------------------
##  gen
##------------------------------------------

## Gen Info Analyzer (generic, but should be revised)
genAna = cfg.Analyzer(
    GeneratorAnalyzer, name="GeneratorAnalyzer",
    # BSM particles that can appear with status <= 2 and should be kept
    stableBSMParticleIds = [ 1000022 ],
    # Particles of which we want to save the pre-FSR momentum (a la status 3).
    # Note that for quarks and gluons the post-FSR doesn't make sense,
    # so those should always be in the list
    savePreFSRParticleIds = [ 1,2,3,4,5, 11,12,13,14,15,16, 21 ],
    # Make also the list of all genParticles, for other analyzers to handle
    makeAllGenParticles = True,
    # Make also the splitted lists
    makeSplittedGenLists = True,
    allGenTaus = False,
    # Print out debug information
    verbose = False,
    )

##------------------------------------------
##  leptons 
##------------------------------------------

# Lepton Analyzer (generic)
lepAna = cfg.Analyzer(
    LeptonAnalyzer, name="leptonAnalyzer",
    # input collections
    muons='slimmedMuons',
    electrons='slimmedElectrons',
    rhoMuon= 'fixedGridRhoFastjetCentralNeutral',
    rhoElectron = 'fixedGridRhoFastjetCentralNeutral',
    # energy scale corrections and ghost muon suppression (off by default)
    doMuonScaleCorrections=False,
    doElectronScaleCorrections=False, # "embedded" in 5.18 for regression
    doSegmentBasedMuonCleaning=False,
    # inclusive very loose muon selection
    inclusive_muon_id  = "",
    inclusive_muon_pt  = 3.5,
    inclusive_muon_eta = 2.4,
    inclusive_muon_dxy = 999,
    inclusive_muon_dz  = 999,
    # loose muon selection
    loose_muon_id     = "",
    loose_muon_pt     = 3.5,
    loose_muon_eta    = 2.4,
    loose_muon_dxy    = 999,
    loose_muon_dz     = 999,
    loose_muon_isoCut = lambda mu : True,
    muon_dxydz_track = "innerTrack",
    # inclusive very loose electron selection
    inclusive_electron_id  = "",
    inclusive_electron_pt  = 5,
    inclusive_electron_eta = 2.5,
    inclusive_electron_dxy = 999,
    inclusive_electron_dz  = 999,
    inclusive_electron_lostHits = 9999,
    # loose electron selection
    loose_electron_id     = "",
    loose_electron_pt     = 5,
    loose_electron_eta    = 2.4,
    loose_electron_dxy    = 999,
    loose_electron_dz     = 999,
    loose_electron_isoCut = lambda el : True,
    loose_electron_lostHits = 9999,
    # muon isolation correction method (can be "rhoArea" or "deltaBeta")
    mu_isoCorr = "rhoArea" ,
    mu_effectiveAreas = "Spring15_25ns_v1", #(can be 'Data2012' or 'Phys14_25ns_v1')
    mu_tightId = "POG_ID_Medium",
    # electron isolation correction method (can be "rhoArea" or "deltaBeta")
    ele_isoCorr = "rhoArea" ,
    ele_effectiveAreas = "Spring15_25ns_v1" , #(can be 'Data2012' or 'Phys14_25ns_v1')
    ele_tightId = "MVA_ID_NonTrig_Spring15_HZZ" ,
    # Mini-isolation, with pT dependent cone: will fill in the miniRelIso, miniRelIsoCharged, miniRelIsoNeutral variables of the leptons (see https://indico.cern.ch/event/368826/ )
    doMiniIsolation  = False, # off by default since it requires access to all PFCandidates 
    packedCandidates = 'packedPFCandidates',
    miniIsolationPUCorr = 'deltaBeta', # Allowed options: 'rhoArea' (EAs for 03 cone scaled by R^2), 'deltaBeta', 'raw' (uncorrected), 'weights' (delta beta weights; not validated)
    miniIsolationVetoLeptons = None, # use 'inclusive' to veto inclusive leptons and their footprint in all isolation cones
    # minimum deltaR between a loose electron and a loose muon (on overlaps, discard the electron)
    min_dr_electron_muon = 0.02,
    # do MC matching 
    do_mc_match = True, # note: it will in any case try it only on MC, not on data
    match_inclusiveLeptons = False, # match to all inclusive leptons
    do_mc_match_photons    = False, # do not do MC matching of electrons to photons
    )

trigMatcher1Mu = cfg.Analyzer(
    TriggerMatchAnalyzer, name="trigMatcher1Mu",
    label='1Mu',
    processName = 'PAT',
    fallbackProcessName = 'RECO',
    unpackPathNames = True,
    trgObjSelectors = [ lambda t : t.path("HLT_IsoMu22_v*",1,0) or t.path("HLT_IsoMu24_v*",1,0) or t.path("HLT_IsoTkMu22_v*",1,0) or t.path("HLT_IsoTkMu24_v*",1,0)],
    collToMatch = 'selectedLeptons',
    collMatchSelectors = [ lambda l,t : abs(l.pdgId()) == 13 ],
    collMatchDRCut = 0.2,
    univoqueMatching = True,
    verbose = False,
)
trigMatcher1El = trigMatcher1Mu.clone(
    name="trigMatcher1El",
    label='1El',
    trgObjSelectors = [ lambda t : t.path("HLT_Ele27_eta2p1_WPLoose_Gsf_v*",1,0) or t.path("HLT_Ele27_WPTight_Gsf_v*",1,0) or t.path("HLT_Ele25_eta2p1_WPLoose_Gsf_v*",1,0) or t.path("HLT_Ele25_eta2p1_WPTight_Gsf_v*",1,0) ],
    collMatchSelectors = [ lambda l,t : abs(l.pdgId()) == 11 ],
)

jetAna = cfg.Analyzer(
    JetAnalyzer, name='jetAnalyzer',
    jetCol = 'slimmedJets',
    copyJetsByValue = False,      #Whether or not to copy the input jets or to work with references (should be 'True' if JetAnalyzer is run more than once)
    genJetCol = 'slimmedGenJets',
    rho = ('fixedGridRhoFastjetAll','',''),
    jetPt = 25.,
    jetEta = 4.7,
    jetEtaCentral = 2.4,
    cleanJetsFromLeptons = True,
    jetLepDR = 0.4,
    jetLepArbitration = (lambda jet,lepton : lepton), # you can decide which to keep in case of overlaps; e.g. if the jet is b-tagged you might want to keep the jet
    cleanSelectedLeptons = True, #Whether to clean 'selectedLeptons' after disambiguation. Treat with care (= 'False') if running Jetanalyzer more than once
    minLepPt = 10,
    relaxJetId = False,
    doPuId = False, # Not commissioned in 7.0.X
    recalibrateJets = True, #'MC', # True, False, 'MC', 'Data'
    applyL2L3Residual = True, # Switch to 'Data' when they will become available for Data
    recalibrationType = "AK4PFchs",
    mcGT     = "Summer16_23Sep2016V3_MC",
    dataGT   = [(1,"Summer16_23Sep2016BCDV3_DATA"),(276831,"Summer16_23Sep2016EFV3_DATA"),(278802,"Summer16_23Sep2016GV3_DATA"),(280919,"Summer16_23Sep2016HV3_DATA")],
    jecPath = "${CMSSW_BASE}/src/CMGTools/RootTools/data/jec/",
    shiftJEC = 0, # set to +1 or -1 to apply +/-1 sigma shift to the nominal jet energies
    addJECShifts = False, # if true, add  "corr", "corrJECUp", and "corrJECDown" for each jet (requires uncertainties to be available!)
    smearJets = False,
    shiftJER = 0, # set to +1 or -1 to get +/-1 sigma shifts
    alwaysCleanPhotons = False,
    cleanGenJetsFromPhoton = False,
    cleanJetsFromFirstPhoton = False,
    cleanJetsFromTaus = False,
    cleanJetsFromIsoTracks = False,
    doQG = False,
    do_mc_match = False,
    calculateSeparateCorrections = True, # should be True if recalibrateJets is True, otherwise L1s will be inconsistent
    calculateType1METCorrection  = True,
    type1METParams = { 'jetPtThreshold':15., 'skipEMfractionThreshold':0.9, 'skipMuons':True },
    collectionPostFix = "",
    storeLowPtJets = False,
    )


metAna = cfg.Analyzer(
    METAnalyzer, name="metAnalyzer",
    metCollection     = "slimmedMETs",
    noPUMetCollection = "slimmedMETs",    
    copyMETsByValue = False,
    doTkMet = False,
    doPuppiMet = False,
    includeTkMetCHS = False,
    includeTkMetPVLoose = False,
    includeTkMetPVTight = False,
    doMetNoPU = False,
    doMetNoMu = False,
    doMetNoEle = False,
    doMetNoPhoton = False,
    recalibrate = "type1",
    applyJetSmearing = False, # does nothing unless the jet smearing is turned on in the jet analyzer
    old74XMiniAODs = False, # set to True to get the correct Raw MET when running on old 74X MiniAODs
    jetAnalyzerPostFix = "",
    candidates='packedPFCandidates',
    candidatesTypes='std::vector<pat::PackedCandidate>',
    dzMax = 0.1,
    collectionPostFix = "",
    )

analyzerTnP = cfg.Analyzer(
    ZTagAndProbeAnalyzer, name="analyzerTnP",
    probeCollection = "selectedLeptons", 
    probeSelection  = lambda lep : True,
    tagSelectionMC  = lambda lep : lep.pt() > 25 and lep.tightId() and lep.relIso03 < 0.2,
    tagSelectionData = lambda lep : lep.pt() > 25 and lep.tightId() and lep.relIso03 < 0.2 and (lep.matchedTrgObj1El if abs(lep.pdgId())==11 else lep.matchedTrgObj1Mu),
    massRange = (50,130),
    filter = True,
)



tnpSequence = [
    skimAnalyzer,
    jsonAna,
    triggerAna,
    fastSkim2L,
    fastSkim1LTag,
    triggerFlagsAna,
    pileUpAna,
    genAna,
    vertexAna,
    lepAna,
] + LeptonTriggerMatchersSequence + [
    trigMatcher1Mu,
    trigMatcher1El,
    analyzerTnP,
    jetAna,
    metAna,
    treeProducerTnP
]
