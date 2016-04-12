import FWCore.ParameterSet.Config as cms

from CMGTools.H2TauTau.objects.cmgTauMu_cfi import cmgTauMu
from CMGTools.H2TauTau.skims.cmgTauMuSel_cfi import cmgTauMuSel

from CMGTools.H2TauTau.objects.cmgTauMuCor_cfi import cmgTauMuCor 
from CMGTools.H2TauTau.objects.tauMuSVFit_cfi import tauMuSVFit 

from CMGTools.H2TauTau.objects.tauCuts_cff import tauPreSelection
from CMGTools.H2TauTau.objects.muCuts_cff import muonPreSelection

from CMGTools.H2TauTau.skims.skim_cff import tauMuFullSelSkimSequence, tauMuFullSelCount

# tau pre-selection
tauPreSelectionTauMu = tauPreSelection.clone()
muonPreSelectionTauMu = muonPreSelection.clone()

# Correct tau pt (after MVA MET according to current baseline)
cmgTauMuCor = cmgTauMuCor.clone()

# This selector goes after the tau pt correction
cmgTauMuTauPtSel = cms.EDFilter(
    "PATCompositeCandidateSelector",
    src = cms.InputTag("cmgTauMuCor"),
    cut = cms.string("daughter(0).pt()>18.")
    )

cmgTauMuTauPtSel = cmgTauMuTauPtSel.clone()

# SVFit
cmgTauMuCorSVFitPreSel = tauMuSVFit.clone()

# If you want to apply some extra selection after SVFit, do it here
cmgTauMuCorSVFitFullSel = cmgTauMuSel.clone(src = 'cmgTauMuCorSVFitPreSel',
                                            cut = ''
                                            ) 

tauMuTauCounter = cms.EDFilter(
    "CandViewCountFilter",
    src = cms.InputTag("tauPreSelectionTauMu"),
    minNumber = cms.uint32(1),
    )

tauMuMuonCounter = cms.EDFilter(
    "CandViewCountFilter",
    src = cms.InputTag("muonPreSelectionTauMu"),
    minNumber = cms.uint32(1),
    )

tauMuSequence = cms.Sequence(   
    tauPreSelectionTauMu + 
    tauMuTauCounter +  
    muonPreSelectionTauMu +   
    tauMuMuonCounter +
    cmgTauMu +
    cmgTauMuCor+
    cmgTauMuTauPtSel +
    cmgTauMuCorSVFitPreSel +
    cmgTauMuCorSVFitFullSel
  )

# tau-mu ---
tauMuPath = cms.Path(
    # metRegressionSequence + 
    tauMuSequence *
    tauMuFullSelSkimSequence
    )
