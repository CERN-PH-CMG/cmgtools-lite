##########################################################
##          MONOX COMMON MODULES ARE DEFINED HERE       ##
## skimming modules are configured to not cut anything  ##
##########################################################

import PhysicsTools.HeppyCore.framework.config as cfg
from PhysicsTools.Heppy.analyzers.core.all import *
from PhysicsTools.Heppy.analyzers.objects.all import *
from PhysicsTools.Heppy.analyzers.gen.all import *
import os

from CMGTools.TTHAnalysis.analyzers.ttHhistoCounterAnalyzer import ttHhistoCounterAnalyzer
histoCounter = cfg.Analyzer(
    ttHhistoCounterAnalyzer, name="ttHhistoCounterAnalyzer",
    )

PDFWeights = []
#PDFWeights = [ ("CT10",53), ("MSTW2008lo68cl",41), ("NNPDF21_100",101) ]

# Find the initial events before the skim
skimAnalyzer = cfg.Analyzer(
    SkimAnalyzerCount, name='skimAnalyzerCount',
    useLumiBlocks = False,
    )

# Pick individual events (normally not in the path)
eventSelector = cfg.Analyzer(
    EventSelector,name="EventSelector",
    toSelect = []  # here put the event numbers (actual event numbers from CMSSW)
    )

# Apply json file (if the dataset has one)
jsonAna = cfg.Analyzer(
    JSONAnalyzer, name="JSONAnalyzer",
    )

# Filter using the 'triggers' and 'vetoTriggers' specified in the dataset
triggerAna = cfg.Analyzer(
    TriggerBitFilter, name="TriggerBitFilter",
    )

# Create flags for trigger bits
triggerFlagsAna = cfg.Analyzer(
    TriggerBitAnalyzer, name="TriggerFlags",
    processName = 'HLT',
    fallbackProcessName = 'HLT2',
    prescaleProcessName = 'PAT',
    prescaleFallbackProcessName = 'RECO',
    unrollbits = False,
    saveIsUnprescaled = False,
    checkL1prescale = False,
    triggerBits = {
        # "<name>" : [ 'HLT_<Something>_v*', 'HLT_<SomethingElse>_v*' ] 
    }
    )

# Create flags for MET filter bits
eventFlagsAna = cfg.Analyzer(
    TriggerBitAnalyzer, name="EventFlags",
    processName = 'PAT',
    fallbackProcessName = 'RECO',
    outprefix   = 'Flag',
    triggerBits = {
        "HBHENoiseFilter" : [ "Flag_HBHENoiseFilter" ],
        "HBHENoiseIsoFilter" : [ "Flag_HBHENoiseIsoFilter" ],
        "globalTightHalo2016Filter" : [ "Flag_globalTightHalo2016Filter" ],
        "CSCTightHalo2015Filter" : [ "Flag_CSCTightHalo2015Filter" ],
        "CSCTightHaloFilter" : [ "Flag_CSCTightHaloFilter" ],
        "CSCTightHalo2016Filter" : [ "Flag_globalTightHalo2016Filter" ],
        "hcalLaserEventFilter" : [ "Flag_hcalLaserEventFilter" ],
        "EcalDeadCellTriggerPrimitiveFilter" : [ "Flag_EcalDeadCellTriggerPrimitiveFilter" ],
        "goodVertices" : [ "Flag_goodVertices" ],
        "trackingFailureFilter" : [ "Flag_trackingFailureFilter" ],
        "eeBadScFilter" : [ "Flag_eeBadScFilter" ],
        "ecalLaserCorrFilter" : [ "Flag_ecalLaserCorrFilter" ],
        "trkPOGFilters" : [ "Flag_trkPOGFilters" ],
        "trkPOG_manystripclus53X" : [ "Flag_trkPOG_manystripclus53X" ],
        "trkPOG_toomanystripclus53X" : [ "Flag_trkPOG_toomanystripclus53X" ],
        "trkPOG_logErrorTooManyClusters" : [ "Flag_trkPOG_logErrorTooManyClusters" ],
        "MuFlag_good" : [ "Flag_noBadMuons" ],
        "MuFlag_bad" : [ "Flag_badMuons" ],
        "MuFlag_dup" : [ "Flag_duplicateMuons" ],
    }
    )

from CMGTools.TTHAnalysis.analyzers.badChargedHadronAnalyzer import badChargedHadronAnalyzer
badChargedHadronAna = cfg.Analyzer(
    badChargedHadronAnalyzer, name = 'badChargedHadronAna',
    muons='slimmedMuons',
    packedCandidates = 'packedPFCandidates',
)

from CMGTools.TTHAnalysis.analyzers.badMuonAnalyzer import badMuonAnalyzer
badMuonAna = cfg.Analyzer(
    badMuonAnalyzer, name = 'badMuonAna',
    muons='slimmedMuons',
    packedCandidates = 'packedPFCandidates',
)

from CMGTools.TTHAnalysis.analyzers.badMuonAnalyzerMoriond2017 import badMuonAnalyzerMoriond2017
badCloneMuonAnaMoriond2017 = cfg.Analyzer(
    badMuonAnalyzerMoriond2017, name = 'badCloneMuonMoriond2017',
    muons = 'slimmedMuons',
    vertices         = 'offlineSlimmedPrimaryVertices',
    minMuPt = 20,
    selectClones = True,
    postFix = '',
)

badMuonAnaMoriond2017 = cfg.Analyzer(
    badMuonAnalyzerMoriond2017, name = 'badMuonMoriond2017',
    muons = 'slimmedMuons',
    vertices         = 'offlineSlimmedPrimaryVertices',
    minMuPt = 20,
    selectClones = False,
    postFix = '',
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


## Gen Info Analyzer (generic, but should be revised)
genAna = cfg.Analyzer(
    GeneratorAnalyzer, name="GeneratorAnalyzer",
    # BSM particles that can appear with status <= 2 and should be kept
    stableBSMParticleIds = [ 1000022 ],
    # Particles of which we want to save the pre-FSR momentum (a la status 3).
    # Note that for quarks and gluons the post-FSR doesn't make sense,
    # so those should always be in the list
    savePreFSRParticleIds = [ 1,2,3,4,5, 11,12,13,14,15,16, 21,22 ],
    # Make also the list of all genParticles, for other analyzers to handle
    makeAllGenParticles = True,
    # save all the genParticles in the generatorSummary object of the event
    saveAllGenParticles = False,
    # Make also the splitted lists
    makeSplittedGenLists = True,
    allGenTaus = False,
    saveIncomingPartons = True,
    # Print out debug information
    verbose = False,
    )

genHiggsAna = cfg.Analyzer(
    HiggsDecayModeAnalyzer, name="HiggsDecayModeAnalyzer",
    filterHiggsDecays = False,
)
genHFAna = cfg.Analyzer(
    GenHeavyFlavourAnalyzer, name="GenHeavyFlavourAnalyzer",
    status2Only = False,
    bquarkPtCut = 15.0,
)

lheWeightAna = cfg.Analyzer(
    LHEWeightAnalyzer, name="LHEWeightAnalyzer",
    useLumiInfo=False
)

pdfwAna = cfg.Analyzer(
    PDFWeightsAnalyzer, name="PDFWeightsAnalyzer",
    PDFWeights = [ pdf for pdf,num in PDFWeights ],
    doPDFVars = True,
    )

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
    inclusive_muon_id  = "POG_ID_Loose",
    inclusive_muon_pt  = 7,
    inclusive_muon_eta = 2.4,
    inclusive_muon_dxy = 1000,
    inclusive_muon_dz  = 1000,
    muon_dxydz_track = "innerTrack",
    # veto muon selection
    loose_muon_id     = "POG_ID_Loose",
    loose_muon_pt     = 10,
    loose_muon_eta    = 2.4,
    loose_muon_dxy    = 1000,
    loose_muon_dz     = 1000,
    loose_muon_relIso = 1000,
    # inclusive very loose electron selection
    inclusive_electron_id  = "",
    inclusive_electron_pt  = 5,
    inclusive_electron_eta = 2.5,
    inclusive_electron_dxy = 0.5,
    inclusive_electron_dz  = 1.0,
    inclusive_electron_lostHits = 5.0,
    # veto electron selection
    loose_electron_id     = "POG_Cuts_ID_SPRING16_25ns_v1_ConvVetoDxyDz_Veto",
    loose_electron_pt     = 10,
    loose_electron_eta    = 2.5,
    loose_electron_dxy    = 0.5,
    loose_electron_dz     = 1.0,
    loose_electron_relIso = 1.0,
    loose_electron_lostHits = 5.0,
    # muon isolation correction method (can be "rhoArea" or "deltaBeta")
    mu_isoCorr = "deltaBeta" ,
    mu_effectiveAreas = "Spring15_25ns_v1", #(can be 'Data2012' or 'Phys14_25ns_v1' or 'Spring15_25ns_v1')
    # electron isolation correction method (can be "rhoArea" or "deltaBeta")
    ele_isoCorr = "rhoArea" ,
    ele_effectiveAreas = "Spring16_25ns_v1" , #(can be 'Data2012' or 'Phys14_25ns_v1' or 'Spring15_25ns_v1' or 'Spring15_50ns_v1')
    ele_tightId = "Cuts_SPRING16_25ns_v1_ConvVetoDxyDz" ,
    # Mini-isolation, with pT dependent cone: will fill in the miniRelIso, miniRelIsoCharged, miniRelIsoNeutral variables of the leptons (see https://indico.cern.ch/event/368826/ )
    doMiniIsolation = False, # off by default since it requires access to all PFCandidates 
    packedCandidates = 'packedPFCandidates',
    miniIsolationPUCorr = 'rhoArea', # Allowed options: 'rhoArea' (EAs for 03 cone scaled by R^2), 'deltaBeta', 'raw' (uncorrected), 'weights' (delta beta weights; not validated)
    miniIsolationVetoLeptons = None, # use 'inclusive' to veto inclusive leptons and their footprint in all isolation cones
    # minimum deltaR between a loose electron and a loose muon (on overlaps, discard the electron)
    min_dr_electron_muon = 0.05,
    # do MC matching 
    do_mc_match = True, # note: it will in any case try it only on MC, not on data
    do_mc_match_photons = "all",
    match_inclusiveLeptons = False, # match to all inclusive leptons
    )

## Lepton-based Skim (generic, but requirements depend on the final state)
from CMGTools.TTHAnalysis.analyzers.ttHLepSkimmer import ttHLepSkimmer
ttHLepSkim = cfg.Analyzer(
    ttHLepSkimmer, name='ttHLepSkimmer',
    minLeptons = 0,
    maxLeptons = 999,
    #idCut  = "lepton.relIso03 < 0.2" # can give a cut
    #ptCuts = [20,10],                # can give a set of pt cuts on the leptons
    requireSameSignPair = False,
    allowLepTauComb = False
)

## Photon Analyzer (generic)
photonAna = cfg.Analyzer(
    PhotonAnalyzer, name='photonAnalyzer',
    photons='slimmedPhotons',
    ptMin = 15,
    etaMax = 2.5,
    doPhotonScaleCorrections=False,
    gammaID = "POG_SPRING15_25ns_Loose",
    rhoPhoton = 'fixedGridRhoFastjetAll',
    gamma_isoCorr = 'rhoArea',
    doFootprintRemovedIsolation = True,
    packedCandidates = 'packedPFCandidates',
    footprintRemovedIsolationPUCorr = 'rhoArea',
    conversionSafe_eleVeto = True,
    do_mc_match = True,
    do_randomCone = False,
)

## Tau Analyzer (generic)
tauAna = cfg.Analyzer(
    TauAnalyzer, name="tauAnalyzer",
    # inclusive very loose hadronic tau selection
    inclusive_ptMin = 18,
    inclusive_etaMax = 9999,
    inclusive_dxyMax = 1000.,
    inclusive_dzMax = 1000,
    inclusive_vetoLeptons = False,
    inclusive_leptonVetoDR = 0.4,
    inclusive_decayModeID = "", # ignored if not set or ""
    inclusive_tauID = "decayModeFinding",
    inclusive_vetoLeptonsPOG = False, # If True, the following two IDs are required
    inclusive_tauAntiMuonID = "",
    inclusive_tauAntiElectronID = "",
    # loose hadronic tau selection
    loose_ptMin = 18,
    loose_etaMax = 9999,
    loose_dxyMax = 1000.,
    loose_dzMax = 1000,
    loose_vetoLeptons = False,
    loose_leptonVetoDR = 0.4,
    loose_decayModeID = "decayModeFinding", # ignored if not set or ""
    loose_tauID = "decayModeFinding",
    loose_vetoLeptonsPOG = False, # If True, the following two IDs are required
    loose_tauAntiMuonID = "againstMuonLoose3",
    loose_tauAntiElectronID = "againstElectronLooseMVA5",
    loose_tauLooseID = "decayModeFinding"
)

## isolation for monojet tau veto
from CMGTools.MonoXAnalysis.analyzers.objects.MonoXTauAnalyzer import MonoXTauAnalyzer
monoxTauAna = cfg.Analyzer(
    MonoXTauAnalyzer, name='monoXTauAnalyzer',
    tauIsolation = "byCombinedIsolationDeltaBetaCorrRaw3Hits",
    isolationMax = 5.0 # GeV
)


##------------------------------------------
###  ISOLATED TRACK
###------------------------------------------                                                                                                                                                                
#
## those are the cuts for the nonEMu                                                                                                                                                                         
isoTrackAna = cfg.Analyzer(
    IsoTrackAnalyzer, name='isoTrackAnalyzer',
    setOff=False,
    #####
    candidates='packedPFCandidates',
    candidatesTypes='std::vector<pat::PackedCandidate>',
    ptMin = 5, # for pion 
    ptMinEMU = 5, # for EMU
    dzMax = 0.1,
    #####
    isoDR = 0.3,
    ptPartMin = 0,
    dzPartMax = 0.1,
    maxAbsIso = 8,
    #####
    doRelIsolation = False,
    MaxIsoSum = 0.1, ### unused if not rel iso
    MaxIsoSumEMU = 0.2, ### unused if not rel iso
    doSecondVeto = False,
    #####
    doPrune = True,
    do_mc_match = False # note: it will in any case try it only on MC, not on data
    )

## Jets Analyzer (generic)
jetAna = cfg.Analyzer(
    JetAnalyzer, name='jetAnalyzer',
    jetCol = 'slimmedJets',
    copyJetsByValue = False,      #Whether or not to copy the input jets or to work with references (should be 'True' if JetAnalyzer is run more than once)
    genJetCol = 'slimmedGenJets',
    rho = ('fixedGridRhoFastjetAll','',''),
    jetPt = 25.,
    jetEta = 4.7,
    jetEtaCentral = 2.5,
    cleanJetsFromLeptons = True,
    jetLepDR = 0.4,
    jetLepArbitration = (lambda jet,lepton : (jet,lepton)), # you can decide which to keep in case of overlaps; e.g. if the jet is b-tagged you might want to keep the jet
    cleanSelectedLeptons = False, #Whether to clean 'selectedLeptons' after disambiguation. Treat with care (= 'False') if running Jetanalyzer more than once
    minLepPt = 10,
    relaxJetId = False,  
    doPuId = True, # Not commissioned in 7.0.X, use the Run1 training for the time being
    recalibrateJets = True, # "MC", # True, False, 'MC', 'Data'
    applyL2L3Residual = True, # Switch to 'Data' when they will become available for Data
    recalibrationType = "AK4PFchs",
    mcGT     = "Spring16_25nsV6_MC",
    dataGT   = "Spring16_25nsV6_DATA",
    jecPath = "%s/src/CMGTools/RootTools/data/jec/" % os.environ['CMSSW_BASE'],
    shiftJEC = 0, # set to +1 or -1 to get +/-1 sigma shifts
    addJECShifts = False, # if true, add  "corr", "corrJECUp", and "corrJECDown" for each jet (requires uncertainties to be available!)
    smearJets = False,
    shiftJER = 0, # set to +1 or -1 to get +/-1 sigma shifts  
    alwaysCleanPhotons = False,
    cleanJetsFromFirstPhoton = False,
    cleanJetsFromTaus = False,
    cleanJetsFromIsoTracks = False,
    doQG = False,
    do_mc_match = True,
    cleanGenJetsFromPhoton = False,
    collectionPostFix = "",
    calculateSeparateCorrections = True, # should be True if recalibrateJets is True, otherwise L1s will be inconsistent
    calculateType1METCorrection  = False,
    type1METParams = { 'jetPtThreshold':15., 'skipEMfractionThreshold':0.9, 'skipMuons':True },
    storeLowPtJets = False,
    )

## Jets Analyzer (generic)
jetAnaScaleUp = jetAna.clone(name='jetAnalyzerScaleUp',
    copyJetsByValue = True,
    jetCol = 'slimmedJets',
    shiftJEC = +1, # set to +1 or -1 to apply +/-1 sigma shift to the nominal jet energies
    collectionPostFix = "_jecUp",
    calculateType1METCorrection  = True,
    cleanSelectedLeptons = False,
   )

## Jets Analyzer (generic)
jetAnaScaleDown = jetAna.clone(name='jetAnalyzerScaleDown',
    copyJetsByValue = True,
    jetCol = 'slimmedJets',
    shiftJEC = -1, # set to +1 or -1 to apply +/-1 sigma shift to the nominal jet energies
    collectionPostFix = "_jecDown",
    calculateType1METCorrection  = True,
    cleanSelectedLeptons = False,
    )


## Fat Jets Analyzer (generic)
from CMGTools.MonoXAnalysis.analyzers.monoXFatJetAnalyzer import monoXFatJetAnalyzer
monoXFatJetAna = cfg.Analyzer(
    monoXFatJetAnalyzer, name = 'monoXFatJetAnalyzer',
    jetCol = 'slimmedJetsAK8',
    jetPt = 100.,
    jetEta = 2.4,
    jetLepDR = 0.4,
    # v--- not implemented for AK8
    #jetLepDR = 0.4,
    #minLepPt = 10,
    relaxJetId = False,  
    # v--- not implemented for AK8
    #doPuId = False, # Not commissioned in 7.0.X
    recalibrateJets = True,
    applyL2L3Residual = True, # Switch to 'Data' when they will become available for Data
    recalibrationType = "AK8PFchs",
    mcGT     = "Spring16_25nsV6_MC",
    dataGT   = "Spring16_25nsV6_DATA", # update with the new one when available in 8.0.X
    jecPath = "%s/src/CMGTools/RootTools/data/jec/" % os.environ['CMSSW_BASE'],
    shiftJEC = 0, # set to +1 or -1 to get +/-1 sigma shifts
    addJECShifts = False, # if true, add  "corr", "corrJECUp", and "corrJECDown" for each jet (requires uncertainties to be available!)
    rho = ('fixedGridRhoFastjetAll','',''),
    )

# Secondary vertex analyzer
from CMGTools.TTHAnalysis.analyzers.ttHSVAnalyzer import ttHSVAnalyzer
ttHSVAna = cfg.Analyzer(
    ttHSVAnalyzer, name="ttHSVAnalyzer",
    do_mc_match = True,
)

# Secondary vertex analyzer
from CMGTools.TTHAnalysis.analyzers.ttHHeavyFlavourHadronAnalyzer import ttHHeavyFlavourHadronAnalyzer
ttHHeavyFlavourHadronAna = cfg.Analyzer(
    ttHHeavyFlavourHadronAnalyzer, name="ttHHeavyFlavourHadronAnalyzer",
)


metAna = cfg.Analyzer(
    METAnalyzer, name="metAnalyzer",
    metCollection     = "slimmedMETs",
    noPUMetCollection = "slimmedMETs",
    copyMETsByValue = False,
    doTkMet = True,
    includeTkMetCHS = True,
    includeTkMetPVLoose = True,
    includeTkMetPVTight = True,
    doMetNoPU = True,
    doMetNoMu = False,
    doMetNoEle = False,
    doMetNoPhoton = False,
    storePuppiExtra = False, # False for MC, True for re-MiniAOD
    recalibrate = False,  # or "type1", or True 
    applyJetSmearing = False, # does nothing unless the jet smearing is turned on in the jet analyzer
    old74XMiniAODs = False, # set to True to get the correct Raw MET when running on old 74X MiniAODs
    jetAnalyzerPostFix = "",
    candidates='packedPFCandidates',
    candidatesTypes='std::vector<pat::PackedCandidate>',
    dzMax = 0.1,
    collectionPostFix = "",
    )

metAnaScaleUp = metAna.clone(name="metAnalyzerScaleUp",
    copyMETsByValue = True,
    recalibrate = "type1", 
    jetAnalyzerPostFix = "_jecUp",
    collectionPostFix = "_jecUp",
    )

metAnaScaleDown = metAna.clone(name="metAnalyzerScaleDown",
    copyMETsByValue = True,
    recalibrate = "type1", 
    jetAnalyzerPostFix = "_jecDown",
    collectionPostFix = "_jecDown",
    )

# Core Event Analyzer (computes basic quantities like HT, dilepton masses)
from CMGTools.TTHAnalysis.analyzers.ttHCoreEventAnalyzer import ttHCoreEventAnalyzer
ttHCoreEventAna = cfg.Analyzer(
    ttHCoreEventAnalyzer, name='ttHCoreEventAnalyzer',
    maxLeps = 4, ## leptons to consider
    mhtForBiasedDPhi = "mhtJet40jvec",
    jetForBiasedDPhi = "cleanJetsAll",
    jetPt = 40.,
    )


# Electron and Photon calibrator (scale and smearings)
def doECalElectronCorrections(sync=False,era="25ns"):
    global lepAna, monoJetCtrlLepSkim
    lepAna.doElectronScaleCorrections = {
        'data' : 'EgammaAnalysis/ElectronTools/data/ScalesSmearings/Winter_2016_reReco_v1_ele',
        'GBRForest': ('$CMSSW_BASE/src/CMGTools/RootTools/data/egamma_epComb_GBRForest_76X.root',
                      'gedelectron_p4combination_'+era),
        'isSync': sync
    }
def doECalPhotonCorrections(sync=False):
    global photonAna, gammaJetCtrlSkimmer
    photonAna.doPhotonScaleCorrections = {
        'data' : 'EgammaAnalysis/ElectronTools/data/ScalesSmearings/80X_ichepV2_2016_pho',
        'isSync': sync
    }
def doKalmanMuonCorrections(sync=False,smear="basic"):
    global lepAna
    lepAna.doMuonScaleCorrections = ( 'Kalman', {
        'MC': 'MC_80X_13TeV',
        'Data': 'DATA_80X_13TeV',
        'isSync': sync,
        'smearMode':smear
    })


# Core sequence of all common modules
dmCoreSequence = [
    lheWeightAna,
    skimAnalyzer,
   #eventSelector,
    jsonAna,
    triggerAna,
    pileUpAna,
    genAna,
#    genHiggsAna,
#    genHFAna,
    pdfwAna,
    vertexAna,
    lepAna,
    jetAna,
    ttHLepSkim,
    metAna,
    photonAna,
#    tauAna,
#    monoxTauAna,
#    isoTrackAna,
    ttHCoreEventAna,
#    monoXFatJetAna,
#    monoJetCtrlFatJetSkim,
#    gammaJetCtrlSkim,
    triggerFlagsAna,
    eventFlagsAna,
    badMuonAna,
    badMuonAnaMoriond2017,
    badCloneMuonAnaMoriond2017,
    badChargedHadronAna,
]
