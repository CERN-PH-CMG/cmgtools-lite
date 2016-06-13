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
    mu_isoCorr = "deltaBeta" ,
    mu_effectiveAreas = "Spring15_25ns_v1", #(can be 'Data2012' or 'Phys14_25ns_v1')
    mu_tightId = "POG_ID_Medium",
    # electron isolation correction method (can be "rhoArea" or "deltaBeta")
    ele_isoCorr = "deltaBeta" ,
    ele_effectiveAreas = "Spring15_25ns_v1" , #(can be 'Data2012' or 'Phys14_25ns_v1')
    ele_tightId = "POG_Cuts_ID_SPRING15_25ns_v1_ConvVetoDxyDz_Tight_full5x5" ,
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
    trgObjSelectors = [ lambda t : t.path("HLT_IsoMu22_v*",1,0) or t.path("HLT_IsoMu20_v*",1,0) ],
    collToMatch = 'selectedLeptons',
    collMatchSelectors = [ lambda l,t : abs(l.pdgId()) == 13 ],
    collMatchDRCut = 0.3,
    univoqueMatching = True,
    verbose = False,
)
trigMatcher1El = trigMatcher1Mu.clone(
    name="trigMatcher1El",
    label='1El',
    trgObjSelectors = [ lambda t : t.path("HLT_Ele23_WPLoose_Gsf_v*",1,0) ],
    collMatchSelectors = [ lambda l,t : abs(l.pdgId()) == 11 ],
)

analyzerTnP = cfg.Analyzer(
    ZTagAndProbeAnalyzer, name="analyzerTnP",
    probeCollection = "selectedLeptons", 
    probeSelection  = lambda lep : True,
    tagSelection    = lambda lep : lep.pt() > 25 and lep.tightId() and lep.relIso03 < 0.2 and (lep.matchedTrgObj1El if abs(lep.pdgId())==11 else lep.matchedTrgObj1Mu),
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
    trigMatcher1Mu,
    trigMatcher1El,
    analyzerTnP,
    treeProducerTnP
]
