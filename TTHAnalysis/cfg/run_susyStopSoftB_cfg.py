##########################################################
##       CONFIGURATION FOR SUSY STOP SOFT B TREES       ##
##########################################################
import PhysicsTools.HeppyCore.framework.config as cfg
import re

#-------- LOAD ALL ANALYZERS -----------
from CMGTools.TTHAnalysis.analyzers.susyCore_modules_cff import *
from PhysicsTools.HeppyCore.framework.heppy_loop import getHeppyOption
from CMGTools.HToZZ4L.tools.configTools import * 


#-------- DEFINE CONFIGURATION -----------

# Pre-skim
from CMGTools.TTHAnalysis.analyzers.ttHFastMETSkimmer import ttHFastMETSkimmer
ttHFastMETSkim = cfg.Analyzer(
   ttHFastMETSkimmer, name='ttHFastMETSkimmer',
   met      = "slimmedMETs", # jet collection to use
   metCut    =  150,  # MET cut
   )
susyCoreSequence.insert(susyCoreSequence.index(skimAnalyzer)+1, ttHFastMETSkim)

# Leptons
lepAna.doMiniIsolation = True
lepAna.inclusive_muon_dxy = 999
lepAna.inclusive_muon_dz  = 999
lepAna.loose_muon_dxy = 0.2
lepAna.loose_muon_dz  = 0.5
lepAna.loose_muon_isoCut = lambda muon : muon.miniRelIso < 0.2
lepAna.inclusive_electron_dxy = 999
lepAna.inclusive_electron_dz  = 999
lepAna.inclusive_electron_lostHits  = 9999
lepAna.loose_electron_dxy = 0.5
lepAna.loose_electron_dz  = 1.0
lepAna.loose_electron_pt = 5
lepAna.loose_electron_id = "POG_Cuts_ID_SPRING15_25ns_v1_ConvVetoDxyDz_Veto"
lepAna.loose_electron_isoCut = lambda elec : elec.miniRelIso < 0.1
lepAna.loose_electron_lostHits  = 9999
lepAna.vertexChoice = "vertices" # FIXME

# Photons (may need updates) 
photonAna.do_mc_match = False

# Taus (will need updates)
tauAna.inclusive_dzMax  = 999 # FIXME
tauAna.loose_decayModeID = "decayModeFindingNewDMs"
tauAna.loose_ptMin = 20
tauAna.loose_etaMax = 999 # FIXME
tauAna.loose_dzMax  = 999 # FIXME
tauAna.loose_vetoLeptons = False
tauAna.loose_decayModeID = "decayModeFindingNewDMs" 
tauAna.loose_tauID = "byVLooseIsolationMVArun2v1DBnewDMwLT"
tauAna.vertexChoice = "vertices" #FIXME

# Jets
jetAna.jetPt = 20
jetAna.mcGT   = "Spring16_25nsV1_MC"
jetAna.dataGT = "Spring16_25nsV1_MC"
jetAna.calculateType1METCorrection = True
jetAna.jetLepDR = 0.0
jetAna.minLepPt = 1e9
jetAna.cleanSelectedLeptons = False
#jetAna.recalibrateJets = False
#jetAna.relaxJetId = True

# MET
#metAna.recalibrate = "type1"
metAna.recalibrate = False

# MET Filters 
from CMGTools.TTHAnalysis.analyzers.hbheAnalyzer import hbheAnalyzer
hbheAna = cfg.Analyzer( hbheAnalyzer, name="hbheAnalyzer", IgnoreTS4TS5ifJetInLowBVRegion=False)

# IVF
ttHSVAna.associatedJetsByRef = False
ttHSVAna.vertexChoice = "vertices" #FIXME
ttHSVAna.jets = 'cleanJets'

# Event (common)
ttHCoreEventAna.jetPt = 20

# Event (susyStopSoftB)
from CMGTools.TTHAnalysis.analyzers.susyStopSoftBEventAnalyzer import susyStopSoftBEventAnalyzer
stopSoftBAna = cfg.Analyzer(
   susyStopSoftBEventAnalyzer, name='stopSoftBAna',
)

# Event selection
from CMGTools.TTHAnalysis.analyzers.ttHJetMETSkimmer import ttHJetMETSkimmer
ttHJetMETSkim = cfg.Analyzer(
   ttHJetMETSkimmer, name='ttHJetMETSkimmer',
   jets      = "cleanJets", # jet collection to use
   jetPtCuts = [],  # e.g. [60,40,30,20] to require at least four jets with pt > 60,40,30,20
   jetVetoPt =  0,  # if non-zero, veto additional jets with pt > veto beyond the ones in jetPtCuts
   metCut    =  200,  # MET cut
   htCut     = ('htJetXj', 0), # cut on HT defined with only jets and pt cut 40, at zero; i.e. no cut
                                # see ttHCoreEventAnalyzer for alternative definitions
   mhtCut    = ('mhtJetX', 0), # cut on MHT defined with all leptons, and jets with pt > 40.
   nBJet     = ('CSVv2IVFM', 0, "jet.pt() > 30"),     # require at least 0 jets passing CSV medium and pt > 30
   )
susyCoreSequence.insert(susyCoreSequence.index(metAna)+1, ttHJetMETSkim)

## Tree Producer
from CMGTools.TTHAnalysis.analyzers.treeProducerSusyStopSoftB import * 
treeProducer = cfg.Analyzer(
     AutoFillTreeProducer, name='treeProducerStopSoftB',
     vectorTree = True, saveTLorentzVectors = False,  defaultFloatType = 'F', PDFWeights = [],
     globalVariables = susyStopSoftB_globalVariables,
     globalObjects = susyStopSoftB_globalObjects,
     collections = susyStopSoftB_collections,
)


## For non-signal
if True:
    susyCoreSequence.remove(lheWeightAna)
    del treeProducer.collections["LHE_weights"]

#-------- SAMPLES AND TRIGGERS -----------
from CMGTools.RootTools.samples.triggers_13TeV_Spring15 import *
triggerFlagsAna.triggerBits = {
    'MET90MHT90' : triggers_met90_mht90,
}
triggerFlagsAna.unrollbits = True

from CMGTools.RootTools.samples.samples_13TeV_RunIISpring16MiniAODv1 import *
from CMGTools.RootTools.samples.samples_13TeV_signals import *
from CMGTools.RootTools.samples.samples_13TeV_80X_susySignalsPriv import *

selectedComponents = [ZJetsToNuNu_HT200to400_ext]

#-------- SEQUENCE -----------
sequence = cfg.Sequence(susyCoreSequence+[
        ttHFatJetAna,
        ttHSVAna, 
        ttHHeavyFlavourHadronAna,
        stopSoftBAna,
        hbheAna,
        treeProducer,
    ])

#-------- HOW TO RUN -----------
test = getHeppyOption('test')
if test == "1":
    selectedComponents = doTest1(T2ttDeg_mStop425_mChi405_4bodydec, sequence=sequence, cache=False )
elif test == "1Z":
    print ZJetsToNuNu_HT200to400_ext.files[2]
    selectedComponents = doTest1(ZJetsToNuNu_HT200to400_ext, sequence=sequence, cache=True )
elif test == "sync":
    T2ttDeg_mStop425_mChi405_4bodydec.files = T2ttDeg_mStop425_mChi405_4bodydec.files[:5]
    selectedComponents = [ T2ttDeg_mStop425_mChi405_4bodydec ]
    if getHeppyOption('events'): 
        selectedComponents[0].splitFactor = 1
        insertEventSelector(sequence)
elif test in ('2','3','5s'):
    doTestN(test,selectedComponents)

config = autoConfig(selectedComponents, sequence)

