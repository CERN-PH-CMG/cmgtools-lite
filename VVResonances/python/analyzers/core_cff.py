import PhysicsTools.HeppyCore.framework.config as cfg
from PhysicsTools.Heppy.analyzers.core.all import *
from PhysicsTools.Heppy.analyzers.objects.all import *
from PhysicsTools.Heppy.analyzers.gen.all import *
from CMGTools.VVResonances.analyzers.LeptonIDOverloader import *
from CMGTools.VVResonances.analyzers.HbbTagComputer import *
from CMGTools.VVResonances.analyzers.VVBuilder import *
from CMGTools.VVResonances.analyzers.VTauBuilder import *
from CMGTools.VVResonances.analyzers.Skimmer import *
from CMGTools.VVResonances.analyzers.TopMergingAnalyzer import *
from CMGTools.VVResonances.analyzers.ObjectWeightAnalyzer import *

import os

# Pick individual events (normally not in the path)
eventSelector = cfg.Analyzer(
    EventSelector,name="EventSelector",
    toSelect = []  # here put the event numbers (actual event numbers from CMSSW)
    )

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

# Create flags for trigger bits
triggerFlagsAna = cfg.Analyzer(
    TriggerBitAnalyzer, name="TriggerFlags",

    processName = 'HLT2',
    fallbackProcessName = 'HLT',
    triggerBits = {
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
        "CSCTightHaloFilter" : [ "Flag_CSCTightHaloFilter" ],
        "globalTightHalo2016Filter" : [ "Flag_globalTightHalo2016Filter" ],
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
        "METFilters" : [ "Flag_METFilters" ],
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
    savePreFSRParticleIds = [ 1,2,3,4,5, 11,12,13,14,15,16, 21 ],
    # Make also the list of all genParticles, for other analyzers to handle
    makeAllGenParticles = True,
    # Make also the splitted lists
    makeSplittedGenLists = True,
    allGenTaus = False,
    # Save LHE weights from LHEEventProduct
    makeLHEweights = True,
    # Print out debug information
    verbose = False,
    )

#pdfwAna = cfg.Analyzer(
#    PDFWeightsAnalyzer, name="PDFWeightsAnalyzer",
#    PDFWeights = [ pdf for pdf,num in PDFWeights ]
#    )

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
    inclusive_muon_id  = "",
    inclusive_muon_pt  = 20.0,
    inclusive_muon_eta = 2.4,
    inclusive_muon_dxy = 0.3,
    inclusive_muon_dz  = 20,
    muon_dxydz_track = "innerTrack",
    # loose muon selection
    loose_muon_id     = "",
    loose_muon_pt     = 20.0,
    loose_muon_eta    = 2.4,
    loose_muon_dxy    = 0.3,
    loose_muon_dz     = 20.0,
    loose_muon_isoCut = lambda x:True,
    # inclusive very loose electron selection
    inclusive_electron_id  = "",
    inclusive_electron_pt  = 35.0,
    inclusive_electron_eta = 2.5,
    inclusive_electron_dxy = 0.2,
    inclusive_electron_dz  = 0.2,
    inclusive_electron_lostHits = 1.0,
    # loose electron selection
    loose_electron_id     = "",
    loose_electron_pt     = 35.0,
    loose_electron_eta    = 2.4,
    loose_electron_dxy    = 0.2,
    loose_electron_dz     = 0.2,
    loose_electron_lostHits = 1.0,
    loose_electron_isoCut = lambda x:True,

    # muon isolation correction method (can be "rhoArea" or "deltaBeta")
    mu_isoCorr = "deltaBeta",
    mu_effectiveAreas = "Spring15_25ns_v1", #(can be 'Data2012' or 'Phys14_25ns_v1')
    # electron isolation correction method (can be "rhoArea" or "deltaBeta")
    ele_isoCorr = "rhoArea" ,
    el_effectiveAreas = "Spring15_25ns_v1" , #(can be 'Data2012' or 'Phys14_25ns_v1')
    ele_tightId = "" ,
    # Mini-isolation, with pT dependent cone: will fill in the miniRelIso, miniRelIsoCharged, miniRelIsoNeutral variables of the leptons (see https://indico.cern.ch/event/368826/ )
    doMiniIsolation = False, # off by default since it requires access to all PFCandidates
    packedCandidates = 'packedPFCandidates',
    miniIsolationPUCorr = 'deltaBeta', # Allowed options: 'rhoArea' (EAs for 03 cone scaled by R^2), 'deltaBeta', 'raw' (uncorrected), 'weights' (delta beta weights; not validated)
    miniIsolationVetoLeptons = 'inclusive', # use 'inclusive' to veto inclusive leptons and their footprint in all isolation cones
    # minimum deltaR between a loose electron and a loose muon (on overlaps, discard the electron)
    min_dr_electron_muon = 0.0,
    # do MC matching
    do_mc_match = True, # note: it will in any case try it only on MC, not on data
    match_inclusiveLeptons = False, # match to all inclusive leptons
    )



lepIDAna = cfg.Analyzer(
    LeptonIDOverloader,
    name='lepIDOverloader'
)


lepWeightAna = cfg.Analyzer(
    ObjectWeightAnalyzer, name="leptonWeightAnalyzer",
    path='${CMSSW_BASE}/src/CMGTools/VVResonances/data',
    collection = "selectedLeptons",
    weights = [
        #Muons from histograms
        {'cut':lambda x: abs(x.pdgId())==13,'dimensions':2,'filename':'MuonID_Z_RunBCD_prompt80X_7p65.root','histoname':"MC_NUM_HighPtIDPt20andIPCut_DEN_genTracks_PAR_pt_spliteta_bin1/pair_ne_ratio",'x':lambda x:x.pt(),'y':lambda x: abs(x.eta()),'tag':'sfWV'},
        {'cut':lambda x: abs(x.pdgId())==13,'dimensions':2,'filename':'MuonIso_Z_RunBCD_prompt80X_7p65.root','histoname':"MC_NUM_TightRelIso_DEN_TightID_PAR_pt_spliteta_bin1/pt_abseta_ratio",'x':lambda x:x.pt(),'y':lambda x: abs(x.eta()),'tag':'sfWV'},
        {'cut':lambda x: abs(x.pdgId())==13,'dimensions':2,'filename':'SingleMuonTrigger_Z_RunBCD_prompt80X_7p65.root','histoname':"Mu50_OR_TkMu50_PtEtaBins_Run274954_to_276097/efficienciesDATA/pt_abseta_DATA",'x':lambda x:x.pt(),'y':lambda x: abs(x.eta()),'tag':'sfHLT'},
        #Electrons flat from Sam
        {'cut':lambda x: abs(x.pdgId())==11 and x.isEB(),'filename':'None','f':lambda x:0.961,'tag':'sfWV'},
        {'cut':lambda x: abs(x.pdgId())==11 and x.isEE(),'filename':'None','f':lambda x:0.965,'tag':'sfWV'},
        {'cut':lambda x: abs(x.pdgId())==11,'dimensions':2,'filename':'myTriggerScaleFactors.root','histoname':"EleTrigger",'x':lambda x:x.pt(),'y':lambda x: abs(x.eta()),'tag':'sfHLT'}
        ]
)








hbbTagComputer = cfg.Analyzer(
    HbbTagComputer,
    name='hbbTagComputer',
    path='RecoBTag/SecondaryVertex/data/BoostedDoubleSV_AK8_BDT_v3.weights.xml.gz'
)


metAna = cfg.Analyzer(
    METAnalyzer, name="metAnalyzer",
    metCollection     = "slimmedMETs",
    noPUMetCollection = "slimmedMETs",
    copyMETsByValue = False,
    doTkMet = False,
    doMetNoPU = True,
    doMetNoMu = False,
    doMetNoEle = False,
    doMetNoPhoton = False,
    recalibrate = False, # or "type1", or True
    applyJetSmearing = False, # does nothing unless the jet smearing is turned on in the jet analyzer
    old74XMiniAODs = False, # set to True to get the correct Raw MET when running on old 74X MiniAODs
    jetAnalyzerPostFix = "",
    candidates='packedPFCandidates',
    candidatesTypes='std::vector<pat::PackedCandidate>',
    dzMax = 0.1,
    collectionPostFix = "",
    )



jetAna = cfg.Analyzer(
    JetAnalyzer, name='jetAnalyzer',
    jetCol = 'slimmedJetsPuppi',
    copyJetsByValue = False,      #Whether or not to copy the input jets or to work with references (should be 'True' if JetAnalyzer is run more than once)
    genJetCol = 'slimmedGenJets',
    rho = ('fixedGridRhoFastjetAll','',''),
    jetPt = 25.,
    jetEta = 4.7,
    jetEtaCentral = 2.4,
    jetLepDR = 0.4,
    cleanSelectedLeptons = False, #Whether to clean 'selectedLeptons' after disambiguation. Treat with care (= 'False') if running Jetanalyzer more than once
    minLepPt = 10,
    relaxJetId = False,
    doPuId = False, # Not commissioned in 7.0.X
    recalibrateJets = True, #'MC', # True, False, 'MC', 'Data'
    applyL2L3Residual = 'Data', # Switch to 'Data' when they will become available for Data
    recalibrationType = "AK4PFPuppi",
    mcGT     = "Spring16_25nsV6_MC",
    dataGT   = "Spring16_25nsV6_DATA",
    jecPath = "${CMSSW_BASE}/src/CMGTools/RootTools/data/jec/",
    shiftJEC = 0, # set to +1 or -1 to apply +/-1 sigma shift to the nominal jet energies
    addJECShifts = True, # if true, add  "corr", "corrJECUp", and "corrJECDown" for each jet (requires uncertainties to be available!)
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
    )


jetAnaAK8 = cfg.Analyzer(
    JetAnalyzer, name='jetAnalyzerAK8',
    jetCol = 'slimmedJetsAK8',
    copyJetsByValue = False,      #Whether or not to copy the input jets or to work with references (should be 'True' if JetAnalyzer is run more than once)
    genJetCol = 'slimmedGenJetsAK8',
    rho = ('fixedGridRhoFastjetAll','',''),
    jetPt = 150.,
    jetEta = 2.4,
    jetEtaCentral = 2.4,
    jetLepDR = 0.4,
    cleanSelectedLeptons = False, #Whether to clean 'selectedLeptons' after disambiguation. Treat with care (= 'False') if running Jetanalyzer more than once
    minLepPt = 10,
    relaxJetId = False,
    doPuId = False, # Not commissioned in 7.0.X
    recalibrateJets = True, #'MC', # True, False, 'MC', 'Data'
    applyL2L3Residual = 'Data', # Switch to 'Data' when they will become available for Data
    recalibrationType = "AK8PFPuppi",
    mcGT     = "Spring16_25nsV6_MC",
    dataGT   = "Spring16_25nsV6_DATA",
    jecPath = "${CMSSW_BASE}/src/CMGTools/RootTools/data/jec/",
    shiftJEC = 0, # set to +1 or -1 to apply +/-1 sigma shift to the nominal jet energies
    addJECShifts = True, # if true, add  "corr", "corrJECUp", and "corrJECDown" for each jet (requires uncertainties to be available!)
    smearJets = False,
    shiftJER = 0, # set to +1 or -1 to get +/-1 sigma shifts
    alwaysCleanPhotons = False,
    cleanGenJetsFromPhoton = False,
    cleanJetsFromFirstPhoton = False,
    cleanJetsFromTaus = False,
    cleanJetsFromIsoTracks = False,
    doQG = False,
    do_mc_match = False,
    collectionPostFix = "AK8",
    calculateSeparateCorrections = True, # should be True if recalibrateJets is True, otherwise L1s will be inconsistent
    calculateType1METCorrection  = False,
    type1METParams = { 'jetPtThreshold':15., 'skipEMfractionThreshold':0.9, 'skipMuons':True },
    )




mergedTruthAna = cfg.Analyzer(TopMergingAnalyzer,name='mergeTruthAna')



vvAna = cfg.Analyzer(
    VVBuilder,name='vvAna',
    suffix = '',
    doPUPPI=True,
    bDiscriminator = "pfCombinedInclusiveSecondaryVertexV2BJetTags",
#    boostedBdiscriminator = "pfBoostedDoubleSecondaryVertexAK8BJetTags",
    cDiscriminatorL = "pfCombinedCvsLJetTags",
    cDiscriminatorB = "pfCombinedCvsBJetTags",
    btagCSVFile = "${CMSSW_BASE}/src/CMGTools/VVResonances/data/btag.csv",
    puppiJecCorrFile = "${CMSSW_BASE}/src/CMGTools/VVResonances/data/puppiCorr.root"

)




metWeightAna = cfg.Analyzer(
    ObjectWeightAnalyzer, name="metWeightAnalyzer",
    path='${CMSSW_BASE}/src/CMGTools/VVResonances/data',
    collection = "LNuJJ",
    weights = [
        #Trigger privately calculated different for electrons and muons
        {'cut':lambda x: abs(x.leg1.leg1.pdgId())==13,'dimensions':1,'filename':'myTriggerScaleFactors.root','histoname':"METMu",'x':lambda x:x.leg1.leg2.pt(),'tag':'sfHLTMET'},
        {'cut':lambda x: abs(x.leg1.leg1.pdgId())==11,'dimensions':1,'filename':'myTriggerScaleFactors.root','histoname':"METEle",'x':lambda x:x.leg1.leg2.pt(),'tag':'sfHLTMET'},
        ]
)



vTauAna = cfg.Analyzer(
    VTauBuilder,name='vTauAna',
    suffix = ''
)






def doPruning():
    print "Switching to pruning"
    jetAna.jetCol = 'slimmedJets'
#    jetAna.mcGT     = "76X_mcRun2_asymptotic_v12"
#    jetAna.dataGT   = "76X_dataRun2_v15_Run2015D_25ns"
    jetAna.recalibrationType = "AK4PFchs"

#    jetAnaAK8.mcGT     = "Fall15_25nsV2_MC"

#    jetAnaAK8.mcGT     = "76X_mcRun2_asymptotic_v12"
#    jetAnaAK8.dataGT   = "76X_dataRun2_v15_Run2015D_25ns"
    jetAnaAK8.recalibrationType = "AK8PFchs"
    vvAna.doPUPPI=False




coreSequence = [
   #eventSelector,
    skimAnalyzer,
    jsonAna,
    triggerAna,
    pileUpAna,
    genAna,
    vertexAna,
    lepAna,
    lepIDAna,
    lepWeightAna,
    jetAna,
    jetAnaAK8,
    hbbTagComputer,
    metAna,
    eventFlagsAna,
    triggerFlagsAna,
    mergedTruthAna,
    badMuonAna,
    badChargedHadronAna,
    vvAna,
    metWeightAna
]
