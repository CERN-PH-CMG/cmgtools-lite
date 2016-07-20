import FWCore.ParameterSet.Config as cms

from CMGTools.H2TauTau.objects.cmgDiMu_cfi import cmgDiMu
from CMGTools.H2TauTau.skims.cmgDiMuSel_cfi import cmgDiMuSel

# from CMGTools.H2TauTau.objects.cmgDiMuCor_cfi import cmgDiMuCor
from CMGTools.H2TauTau.objects.diMuSVFit_cfi import diMuSVFit

from CMGTools.H2TauTau.objects.muCuts_cff import muonPreSelection

from CMGTools.H2TauTau.skims.skim_cff import diMuFullSelSkimSequence, diMuFullSelCount

# lepton pre-selection
muonPreSelectionDiMu = muonPreSelection.clone()

# # Correct tau pt (after MVA MET according to current baseline)
# cmgDiMuCor = cmgDiMuCor.clone()

# This selector goes after the tau pt correction
cmgDiMuTauPtSel = cms.EDFilter(
    "PATCompositeCandidateSelector",
    src=cms.InputTag("cmgDiMu"),
    cut=cms.string("daughter(0).pt()>18.")
)

cmgDiMuTauPtSel = cmgDiMuTauPtSel.clone()

# SVFit
cmgDiMuCorSVFitPreSel = diMuSVFit.clone()

# If you want to apply some extra selection after SVFit, do it here
cmgDiMuCorSVFitFullSel = cmgDiMuSel.clone(src='cmgDiMuCorSVFitPreSel',
                                          cut=''
                                          )


diMuMuCounter = cms.EDFilter(
    "CandViewCountFilter",
    src = cms.InputTag("muonPreSelectionDiMu"),
    minNumber = cms.uint32(1),
    )

diMuSequence = cms.Sequence(
    muonPreSelectionDiMu +
    diMuMuCounter + 
    cmgDiMu +
    # cmgDiMuCor + # Correction only applies to taus, not needed for di-mu
    cmgDiMuTauPtSel +
    cmgDiMuCorSVFitPreSel +
    cmgDiMuCorSVFitFullSel
)

diMuPath = cms.Path(
    diMuSequence *
    diMuFullSelSkimSequence
)