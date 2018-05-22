##########################################################
##       CONFIGURATION FOR SUSY STOP SOFT B TREES       ##
##########################################################
import PhysicsTools.HeppyCore.framework.config as cfg
import re

#-------- LOAD ALL ANALYZERS -----------
from PhysicsTools.HeppyCore.framework.heppy_loop import getHeppyOption
from CMGTools.RootTools.samples.configTools import *
from CMGTools.RootTools.samples.autoAAAconfig import *

#-------- Standard susy setup (useful to get core modules)
from CMGTools.TTHAnalysis.analyzers.susyCore_modules_cff import *

lepAna.doMiniIsolation = "precomputed"
lepAna.mu_isoCorr = "deltaBeta"
lepAna.loose_muon_id     = "POG_ID_Loose"
lepAna.loose_electron_id = "MVA_ID_nonIso_Fall17_Loose"
lepAna.loose_muon_isoCut     = lambda muon : muon.miniRelIso < 0.4 and muon.sip3D() < 8
lepAna.loose_electron_isoCut = lambda elec : elec.miniRelIso < 0.4 and elec.sip3D() < 8

tauAna.loose_ptMin = 20
tauAna.loose_etaMax = 2.3
tauAna.loose_tauID = "decayModeFindingNewDMs"
tauAna.loose_vetoLeptons = False # no cleaning with leptons in production

photonAna.do_mc_match = False

jetAna.addJECShifts = True
jetAna.jetPtOrUpOrDnSelection = True

jetAna.copyJetsByValue = True # do not remove this
metAna.copyMETsByValue = True # do not remove this
jetAna.calculateType1METCorrection = True
metAna.recalibrate = "type1"
jetAnaScaleUp.calculateType1METCorrection = True
metAnaScaleUp.recalibrate = "type1"
jetAnaScaleDown.calculateType1METCorrection = True
metAnaScaleDown.recalibrate = "type1"

## early skimming with loose cuts (before jet-lepton cleaning, re-application of JECs, ...)
from CMGTools.TTHAnalysis.analyzers.ttHFastMETSkimmer import ttHFastMETSkimmer
fastMETSkim = cfg.Analyzer( ttHFastMETSkimmer, name='fastMETSkimmer',
    met      = "slimmedMETs", # met collection to use
    metCut    =  50,  # MET cut, looser because of non-final JECs
    )
from CMGTools.TTHAnalysis.analyzers.ttHFastJetSkimmer import ttHFastJetSkimmer
fastJetSkim = cfg.Analyzer(ttHFastJetSkimmer, name="fastJetSkimmer",
    jets = 'slimmedJets',
    jetCut = lambda j : j.pt() > 80 and abs(j.eta()) < 2.4, # looser pt because of non-final JECs
    minJets = 1,
    )
from CMGTools.TTHAnalysis.analyzers.isoTrackFastSkimmer import isoTrackFastSkimmer
isoTrackFastSkim = cfg.Analyzer(isoTrackFastSkimmer, name="isoTrackFastSkim",
    cut = lambda t : (t.pt() > 50 and 
                      abs(t.eta()) < 2.4 and 
                      t.isHighPurityTrack() and 
                      abs(t.dxy()) < 0.5 and abs(t.dz()) < 0.5 and
                      (t.miniPFIsolation().chargedHadronIso() < 1.0*t.pt() or t.pt() > 100))
)

## late skimming (after analyzers have been run)
ttHJetMETSkim.jetPtCuts = [ 90., ]  # looser than the analysis, to allow for JEC uncertainties
ttHJetMETSkim.metCut    =   80.

## Full DeDx analyzer
from CMGTools.TTHAnalysis.analyzers.isoTrackDeDxAnalyzer import isoTrackDeDxAnalyzer
isoTrackDeDxAna = cfg.Analyzer(isoTrackDeDxAnalyzer, name="isoTrackDeDxAna",
    doDeDx = "94XMiniAODv1-Hack", 
        # for 94X MiniAOD v2, just set it to True
        # for 94X MiniAOD v1, you have two options
        #  - set it to False, and have no DeDx
        #  - set it to "94XMiniAODv1-Hack" and follow step (1) of https://hypernews.cern.ch/HyperNews/CMS/get/physTools/3586/1/1/1/1.html 
    )

## Tree Producer
from CMGTools.TTHAnalysis.analyzers.treeProducerSusyDeDx import *

## Sample production and setup
### Trigger
from CMGTools.RootTools.samples.triggers_13TeV_DATA2017 import *
triggerFlagsAna.triggerBits = {
    'SingleMu' : triggers_1mu_iso,
}
triggerFlagsAna.unrollbits = True

### MC
from CMGTools.RootTools.samples.samples_13TeV_RunIIFall17MiniAOD import *
mcSamples = [ W3JetsToLNu_LO ]
autoAAA(mcSamples)
for c in mcSamples:
    c.triggers = triggers_1mu_iso

## Data
from CMGTools.RootTools.samples.samples_13TeV_DATA2017 import *
selectedComponents = mcSamples # + dataSamples

#-------- SEQUENCE -----------
sequence = cfg.Sequence( [
    lheWeightAna,
    pileUpAna,
    skimAnalyzer,
    jsonAna,
    triggerAna,

    isoTrackFastSkim,
    fastMETSkim,
    fastJetSkim, 

    genAna,
    genHFAna,
    #susyScanAna, # may be needed later

    vertexAna,
    lepAna,
    tauAna,
    photonAna,
    jetAna,
    jetAnaScaleUp,
    jetAnaScaleDown,
    metAna,
    metAnaScaleUp,
    metAnaScaleDown,
    ttHJetMETSkim,

    isoTrackDeDxAna,

    triggerFlagsAna,
    eventFlagsAna,

    treeProducer,
])

#-------- HOW TO RUN -----------
test = getHeppyOption('test')
if test == "1":
    print "The test wil use %s " % selectedComponents[0].name
    selectedComponents = doTest1(selectedComponents[0], sequence=sequence, cache=True )
    print "The test wil use file %s " % selectedComponents[0].files[0]
elif test == "1S":
    comp = selectedComponents[0]
    comp.name = "Signal"
    comp.files = [ '/afs/cern.ch/work/g/gpetrucc/SusyWithDeDx/CMSSW_9_4_6_patch1/src/MiniAODv2.root' ]
    selectedComponents = doTest1(comp, sequence=sequence, cache=False )
    print "The test wil use file %s " % comp.files[0]
    ttHJetMETSkim.jetPtCuts = [ ]  # looser than the analysis, to allow for JEC uncertainties
    ttHJetMETSkim.metCut    =   0.
    fastJetSkim.minJets = 0
    fastMETSkim.metCut = 0
    isoTrackDeDxAna.doDeDx = True
    comp.triggers = []
elif test in ('2','3','5s'):
    doTestN(test,selectedComponents)

printSummary(selectedComponents)

config = autoConfig(selectedComponents, sequence) #, xrd_aggressive=-1)
