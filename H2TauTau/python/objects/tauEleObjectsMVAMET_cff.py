import FWCore.ParameterSet.Config as cms

from CMGTools.H2TauTau.objects.cmgTauEle_cfi import cmgTauEle
from CMGTools.H2TauTau.skims.cmgTauEleSel_cfi import cmgTauEleSel

from CMGTools.H2TauTau.objects.cmgTauEleCor_cfi import cmgTauEleCor 
from CMGTools.H2TauTau.objects.tauEleSVFit_cfi import tauEleSVFit 

from CMGTools.H2TauTau.objects.tauCuts_cff import tauPreSelection
from CMGTools.H2TauTau.objects.eleCuts_cff import electronPreSelection

from CMGTools.H2TauTau.skims.skim_cff import tauEleFullSelSkimSequence, tauEleFullSelCount

# tau pre-selection
tauPreSelectionTauEle = tauPreSelection.clone()
electronPreSelectionTauEle = electronPreSelection.clone()


# Correct tau pt (after MVA MET according to current baseline)
cmgTauEleCor = cmgTauEleCor.clone()

# This selector goes after the tau pt correction
cmgTauEleTauPtSel = cms.EDFilter(
    "PATCompositeCandidateSelector",
    src = cms.InputTag("cmgTauEleCor"),
    cut = cms.string("daughter(0).pt()>18.")
    )

cmgTauEleTauPtSel = cmgTauEleTauPtSel.clone()


# SVFit
cmgTauEleCorSVFitPreSel = tauEleSVFit.clone()

# If you want to apply some extra selection after SVFit, do it here
cmgTauEleCorSVFitFullSel = cmgTauEleSel.clone(src = 'cmgTauEleCorSVFitPreSel',
                                              cut = ''
                                              ) 


tauEleTauCounter = cms.EDFilter(
    "CandViewCountFilter",
    src = cms.InputTag("tauPreSelectionTauEle"),
    minNumber = cms.uint32(1),
    )

tauEleEleCounter = cms.EDFilter(
    "CandViewCountFilter",
    src = cms.InputTag("electronPreSelectionTauEle"),
    minNumber = cms.uint32(1),
    )

tauEleSequence = cms.Sequence( #
    tauPreSelectionTauEle + 
    tauEleTauCounter +  
    electronPreSelectionTauEle +   
    tauEleEleCounter + 
    cmgTauEle +
    cmgTauEleCor+
    cmgTauEleTauPtSel +
    cmgTauEleCorSVFitPreSel +
    cmgTauEleCorSVFitFullSel
    )

tauElePath = cms.Path(
    tauEleSequence *
    tauEleFullSelSkimSequence
    )
