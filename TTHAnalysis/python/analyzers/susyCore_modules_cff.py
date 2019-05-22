##########################################################
##          SUSY COMMON MODULES ARE DEFINED HERE        ##
## skimming modules are configured to not cut anything  ##
##########################################################

import PhysicsTools.HeppyCore.framework.config as cfg
from PhysicsTools.Heppy.analyzers.core.all import *
from PhysicsTools.Heppy.analyzers.objects.all import *
from PhysicsTools.Heppy.analyzers.gen.all import *
import os

from CMGTools.TTHAnalysis.analyzers.ttHhistoCounterAnalyzer import ttHhistoCounterAnalyzer
susyCounter = cfg.Analyzer(
    ttHhistoCounterAnalyzer, name="ttHhistoCounterAnalyzer",
    SMS_max_mass = 3000, # maximum mass allowed in the scan
    SMS_mass_1 = 'genSusyMScan1', # first scanned mass
    SMS_mass_2 = 'genSusyMScan2', # second scanned mass
    SMS_varying_masses = [], # other mass variables that are expected to change in the tree (e.g., in T1tttt it should be set to ['genSusyMGluino','genSusyMNeutralino'])
    SMS_regexp_evtGenMass = 'genSusyM.+',
    bypass_trackMass_check = True # bypass check that non-scanned masses are the same in all events
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
        "EcalDeadCellTriggerPrimitiveFilter" : [ "Flag_EcalDeadCellTriggerPrimitiveFilter" ],
        "goodVertices" : [ "Flag_goodVertices" ],
        "eeBadScFilter" : [ "Flag_eeBadScFilter" ],
        "ecalBadCalibFilter" : [ "Flag_ecalBadCalibFilter" ],
        "BadPFMuonFilter" : [ "Flag_BadPFMuonFilter" ],
        "BadChargedCandidateFilter" : [ "Flag_BadChargedCandidateFilter" ],
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
    makeHists=True
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
    # Make also the splitted lists
    makeSplittedGenLists = True,
    allGenTaus = False,
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
    PDFWeights = [ pdf for pdf,num in PDFWeights ]
    )

# Save SUSY masses
from CMGTools.TTHAnalysis.analyzers.susyParameterScanAnalyzer import susyParameterScanAnalyzer
susyScanAna = cfg.Analyzer(
    susyParameterScanAnalyzer, name="susyParameterScanAnalyzer",
    doLHE=True,
    useLumiInfo=True
    )

# Lepton Analyzer (generic)
lepAna = cfg.Analyzer(
    LeptonAnalyzer, name="leptonAnalyzer",
    # input collections
    muons='slimmedMuons',
    electrons='slimmedElectrons',
    rhoMuon= 'fixedGridRhoFastjetAll',
    rhoElectron = 'fixedGridRhoFastjetAll',
    # energy scale corrections and ghost muon suppression (off by default)
    doMuonScaleCorrections=False,
    doElectronScaleCorrections=False, # "embedded" in 5.18 for regression
    doSegmentBasedMuonCleaning=False,
    # inclusive very loose muon selection
    inclusive_muon_id  = "POG_ID_Loose",
    inclusive_muon_pt  = 3,
    inclusive_muon_eta = 2.4,
    inclusive_muon_dxy = 0.5,
    inclusive_muon_dz  = 1.0,
    muon_dxydz_track = "innerTrack",
    # loose muon selection
    loose_muon_id     = "POG_ID_Loose",
    loose_muon_pt     = 5,
    loose_muon_eta    = 2.4,
    loose_muon_dxy    = 0.05,
    loose_muon_dz     = 0.1,
    loose_muon_relIso = 0.5,
    # inclusive very loose electron selection
    inclusive_electron_id  = "",
    inclusive_electron_pt  = 5,
    inclusive_electron_eta = 2.5,
    inclusive_electron_dxy = 0.5,
    inclusive_electron_dz  = 1.0,
    inclusive_electron_lostHits = 1.0,
    # loose electron selection
    loose_electron_id     = "POG_Cuts_ID_2012_Veto_full5x5",
    loose_electron_pt     = 7,
    loose_electron_eta    = 2.5,
    loose_electron_dxy    = 0.05,
    loose_electron_dz     = 0.1,
    loose_electron_relIso = 0.5,
    loose_electron_lostHits = 1.0,
    # muon isolation correction method (can be "rhoArea" or "deltaBeta")
    mu_isoCorr = "rhoArea" ,
    mu_effectiveAreas = "Fall17", #(can be 'Data2012' or 'Phys14_25ns_v1' or 'Spring15_25ns_v1')
    # electron isolation correction method (can be "rhoArea" or "deltaBeta")
    ele_isoCorr = "rhoArea" ,
    ele_effectiveAreas = "Fall17" , #(can be 'Data2012' or 'Phys14_25ns_v1' or 'Spring15_25ns_v1')
    ele_tightId = "Cuts_SPRING15_25ns_v1_ConvVetoDxyDz" ,
    # Mini-isolation, with pT dependent cone: will fill in the miniRelIso, miniRelIsoCharged, miniRelIsoNeutral variables of the leptons (see https://indico.cern.ch/event/368826/ )
    doMiniIsolation = False, # off by default since it requires access to all PFCandidates 
    packedCandidates = 'packedPFCandidates',
    miniIsolationPUCorr = 'rhoArea', # Allowed options: 'rhoArea' (EAs for 03 cone scaled by R^2), 'deltaBeta', 'raw' (uncorrected), 'weights' (delta beta weights; not validated)
    miniIsolationVetoLeptons = None, # use 'inclusive' to veto inclusive leptons and their footprint in all isolation cones
    doDirectionalIsolation = [], # calculate directional isolation with leptons (works only with doMiniIsolation, pass list of cone sizes)
    doFixedConeIsoWithMiniIsoVeto = False, # calculate fixed cone isolations with the same vetoes used for miniIso,
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

## global event Skimmer
from CMGTools.TTHAnalysis.analyzers.globalEventSkimmer import globalEventSkimmer
globalSkim = cfg.Analyzer(
    globalEventSkimmer, name='globalEventSkimmer',
    collections={"lep":"selectedLeptons",
                 "tau":"selectedTaus"},
    selections=[]
    )

## Photon Analyzer (generic)
photonAna = cfg.Analyzer(
    PhotonAnalyzer, name='photonAnalyzer',
    photons='slimmedPhotons',
    doPhotonScaleCorrections=False, 
    ptMin = 15,
    etaMax = 2.5,
    gammaID = "POG_PHYS14_25ns_Loose",
    rhoPhoton = 'fixedGridRhoFastjetAll',
    gamma_isoCorr = 'rhoArea',
    conversionSafe_eleVeto = False,
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
    inclusive_dzMax = 0.4,
    inclusive_vetoLeptons = False,
    inclusive_leptonVetoDR = 0.4,
    inclusive_decayModeID = "decayModeFindingNewDMs", # ignored if not set or ""
    inclusive_tauID = "decayModeFindingNewDMs",
    inclusive_vetoLeptonsPOG = False, # If True, the following two IDs are required
    inclusive_tauAntiMuonID = "",
    inclusive_tauAntiElectronID = "",
    # loose hadronic tau selection
    loose_ptMin = 18,
    loose_etaMax = 9999,
    loose_dxyMax = 1000.,
    loose_dzMax = 0.2,
    loose_vetoLeptons = True,
    loose_leptonVetoDR = 0.4,
    loose_decayModeID = "decayModeFindingNewDMs", # ignored if not set or ""
    loose_tauID = "byLooseCombinedIsolationDeltaBetaCorr3Hits",
    loose_vetoLeptonsPOG = False, # If True, the following two IDs are required
    loose_tauAntiMuonID = "againstMuonLoose3",
    loose_tauAntiElectronID = "againstElectronLooseMVA5",

)

##------------------------------------------
###  ISOLATED TRACK
###------------------------------------------                                                                                                                                                                
#
## those are the cuts for the nonEMu                                                                                                                                                                         
isoTrackAna = cfg.Analyzer(
    IsoTrackAnalyzer, name='isoTrackAnalyzer',
    useLegacy2016=True,
    setOff=True,
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
    jetEtaCentral = 2.4,
    cleanJetsFromLeptons = True,
    jetLepDR = 0.4,
    jetLepArbitration = (lambda jet,lepton : lepton), # you can decide which to keep in case of overlaps; e.g. if the jet is b-tagged you might want to keep the jet
    cleanSelectedLeptons = True, #Whether to clean 'selectedLeptons' after disambiguation. Treat with care (= 'False') if running Jetanalyzer more than once
    minLepPt = 10,
    lepSelCut = lambda lep : True,
    relaxJetId = False,  
    doPuId = False, # Not commissioned in 7.0.X
    recalibrateJets = True, #'MC', # True, False, 'MC', 'Data'
    applyL2L3Residual = True, # Switch to 'Data' when they will become available for Data
    recalibrationType = "AK4PFchs",
    mcGT     = "Fall17_17Nov2017_V32_MC",
    dataGT   = [(1,"Fall17_17Nov2017B_V32_DATA"),(299337,"Fall17_17Nov2017C_V32_DATA"),(302030,"Fall17_17Nov2017DE_V32_DATA"),(304911,"Fall17_17Nov2017F_V32_DATA")],
    jecPath = "${CMSSW_BASE}/src/CMGTools/RootTools/data/jec/",
    shiftJEC = 0, # set to +1 or -1 to apply +/-1 sigma shift to the nominal jet energies
    addJECShifts = False, # if true, add  "corr", "corrJECUp", and "corrJECDown" for each jet (requires uncertainties to be available!)
    jetPtOrUpOrDnSelection = False, # if true, apply pt cut on the maximum among central, JECUp and JECDown values of corrected pt
    smearJets = False,
    shiftJER = 0, # set to +1 or -1 to get +/-1 sigma shifts  
    alwaysCleanPhotons = False,
    cleanGenJetsFromPhoton = False,
    cleanJetsFromFirstPhoton = False,
    cleanJetsFromTaus = False,
    cleanJetsFromIsoTracks = False,
    doQG = False,
    do_mc_match = True,
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

##PFcharged jets analyzer
#pfChargedCHSjetAna = cfg.Analyzer(
#    JetAnalyzer, name='pfChargedCHSJetAnalyzer',
#    jetCol = 'patJetsAK4ChargedPFCHS',
#    copyJetsByValue = False,      #Whether or not to copy the input jets or to work with references (should be 'True' if JetAnalyzer is run more than once)
#    genJetCol = 'slimmedGenJets',
#    rho = ('fixedGridRhoFastjetAll','',''),
#    jetPt = 25.,
#    jetEta = 4.7,
#    jetEtaCentral = 2.4,
#    jetLepDR = 0.4,
#    jetLepArbitration = (lambda jet,lepton : lepton), # you can decide which to keep in case of overlaps; e.g. if the jet is b-tagged you might want to keep the jet
#    cleanSelectedLeptons = True, #Whether to clean 'selectedLeptons' after disambiguation. Treat with care (= 'False') if running Jetanalyzer more than once
#    minLepPt = 10,
#    relaxJetId = False,  
#    doPuId = False, # Not commissioned in 7.0.X
#    recalibrateJets = False, #'MC', # True, False, 'MC', 'Data'
#    applyL2L3Residual = False, # Switch to 'Data' when they will become available for Data
#    recalibrationType = "AK4PFchs",
#    mcGT     = "Summer15_25nsV6_MC",
#    dataGT   = "Summer15_25nsV6_DATA",
#    jecPath = "${CMSSW_BASE}/src/CMGTools/RootTools/data/jec/",
#    shiftJEC = 0, # set to +1 or -1 to apply +/-1 sigma shift to the nominal jet energies
#    addJECShifts = False, # if true, add  "corr", "corrJECUp", and "corrJECDown" for each jet (requires uncertainties to be available!)
#    smearJets = False,
#    shiftJER = 0, # set to +1 or -1 to get +/-1 sigma shifts  
#    alwaysCleanPhotons = False,
#    cleanJetsFromFirstPhoton = False,
#    cleanJetsFromTaus = False,
#    cleanJetsFromIsoTracks = False,
#    doQG = False,
#    do_mc_match = True,
#    cleanGenJetsFromPhoton = False,
#    collectionPostFix = "PFChargedCHS",
#    calculateSeparateCorrections = False,
#    calculateType1METCorrection  = False,
#    )

## Fat Jets Analyzer (generic)
from CMGTools.TTHAnalysis.analyzers.ttHFatJetAnalyzer import ttHFatJetAnalyzer
ttHFatJetAna = cfg.Analyzer(
    ttHFatJetAnalyzer, name = 'ttHFatJetAnalyzer',
    jetCol = 'slimmedJetsAK8',
    jetPt = 170.,
    jetEta = 2.4,
    jetLepDR = 0.4,
    # v--- not implemented for AK8
    #jetLepDR = 0.4,
    #minLepPt = 10,
    relaxJetId = False,  
    # v--- not implemented for AK8
    #doPuId = False, # Not commissioned in 7.0.X
    #recalibrateJets = False,
    #shiftJEC = 0, # set to +1 or -1 to get +/-1 sigma shifts
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
    doTkMet = False,
    doPuppiMet = False,
    doMetNoPU = False,
    doMetNoMu = False,
    doMetNoEle = False,
    doMetNoPhoton = False,
    storePuppiExtra = False, # False for MC, True for re-MiniAOD
    recalibrate = False, # or "type1", or True
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
    jetForBiasedDPhi = "cleanJets",
    jetPt = 40.,
    doLeptonMVASoft = False,
    )

# Jet-MET based Skim (generic, but requirements depend on the final state)
from CMGTools.TTHAnalysis.analyzers.ttHJetMETSkimmer import ttHJetMETSkimmer
ttHJetMETSkim = cfg.Analyzer(
   ttHJetMETSkimmer, name='ttHJetMETSkimmer',
   jets      = "cleanJets", # jet collection to use
   jetPtCuts = [],  # e.g. [60,40,30,20] to require at least four jets with pt > 60,40,30,20
   jetVetoPt =  0,  # if non-zero, veto additional jets with pt > veto beyond the ones in jetPtCuts
   metCut    =  0,  # MET cut
   htCut     = ('htJet40j', 0), # cut on HT defined with only jets and pt cut 40, at zero; i.e. no cut
                                # see ttHCoreEventAnalyzer for alternative definitions
   mhtCut    = ('mhtJet40', 0), # cut on MHT defined with all leptons, and jets with pt > 40.
   nBJet     = ('CSVv2IVFM', 0, "jet.pt() > 30"),     # require at least 0 jets passing CSV medium and pt > 30
   )

# Tailored lepton MC matching for SUSY
from CMGTools.TTHAnalysis.analyzers.susyLeptonMatchAnalyzer import susyLeptonMatchAnalyzer
susyLeptonMatchAna = cfg.Analyzer(
    susyLeptonMatchAnalyzer, name="susyLeptonMatchAna",
    collection = "inclusiveLeptons",
    deltaR     = 0.2,
    statusOne  = True # put True if trying to match to genParticle with same pdgId and status 1, but False if only require same pdgId
    )

# same as above for taus
susyTauMatchAna = cfg.Analyzer(
    susyLeptonMatchAnalyzer, name="susyTauMatchAna",
    collection = "inclusiveTaus",
    deltaR     = 0.2,
    statusOne  = False # put True if trying to match to genParticle with same pdgId and status 1, but False if only require same pdgId
    )

from CMGTools.TTHAnalysis.analyzers.PrefiringAnalyzer import PrefiringAnalyzer
PrefiringAnalyzer = cfg.Analyzer(
  PrefiringAnalyzer, name='PrefiringAnalyzer',
  #class_object= PrefiringAnalyzer,
  L1Maps = '$CMSSW_BASE/src/CMGTools/RootTools/data/L1PrefiringMaps_new.root',
  DataEra = '2017BtoF',
  UseJetEMPt = False ,
  PrefiringRateSystematicUncty =  0.2 , 
  SkipWarnings= True,
  )
  


# Core sequence of all common modules
susyCoreSequence = [
    lheWeightAna,
    pileUpAna,
    skimAnalyzer,
   #eventSelector,
    jsonAna,
    triggerAna,
    genAna,
    genHiggsAna,
    genHFAna,
    pdfwAna,
    susyScanAna,
    vertexAna,
    lepAna,
    tauAna,
    ttHLepSkim,
    #ttHLepMCAna,
    photonAna,
    isoTrackAna,
    jetAna,
    #ttHFatJetAna,  # out of core sequence for now
    #ttHSVAna, # out of core sequence for now
    metAna,
    ttHCoreEventAna,
    # ttHJetMETSkim,
    # susyLeptonMatchAna,
    triggerFlagsAna,
    eventFlagsAna,
    badMuonAna,
    badMuonAnaMoriond2017,
    badCloneMuonAnaMoriond2017,
    badChargedHadronAna,
    PrefiringAnalyzer,
]
