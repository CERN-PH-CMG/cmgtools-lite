import FWCore.ParameterSet.Config as cms

from CMGTools.H2TauTau.objects.cmgMuEle_cfi import cmgMuEle
from CMGTools.H2TauTau.skims.cmgMuEleSel_cfi import cmgMuEleSel

from CMGTools.H2TauTau.objects.cmgMuEleCor_cfi import cmgMuEleCor 
from CMGTools.H2TauTau.objects.muEleSVFit_cfi import muEleSVFit 

from CMGTools.H2TauTau.objects.muCuts_cff import muonPreSelection
from CMGTools.H2TauTau.objects.eleCuts_cff import electronPreSelection

from CMGTools.H2TauTau.skims.skim_cff import muEleFullSelSkimSequence, muEleFullSelCount

# lepton pre-selection
muonPreSelectionMuEle = muonPreSelection.clone()
electronPreSelectionMuEle = electronPreSelection.clone()

muonPreSelectionMuEle.cut = cms.string('pt > 9 && abs(eta) < 2.5')
electronPreSelectionMuEle.cut = cms.string('pt > 12 && abs(eta) < 2.6')

# # Correct tau pt (after MVA MET according to current baseline)
#cmgMuEleCor = cmgMuEleCor.clone()

# This selector goes after the tau pt correction
cmgMuEleTauPtSel = cms.EDFilter(
    "PATCompositeCandidateSelector",
    src = cms.InputTag("cmgMuEle"),
    cut = cms.string("daughter(0).pt()>9.")
    )

cmgMuEleTauPtSel = cmgMuEleTauPtSel.clone()

# SVFit
cmgMuEleCorSVFitPreSel = muEleSVFit.clone()

# If you want to apply some extra selection after SVFit, do it here
cmgMuEleCorSVFitFullSel = cmgMuEleSel.clone(src = 'cmgMuEleCorSVFitPreSel',
                                              cut = ''
                                              ) 

muEleMuCounter = cms.EDFilter(
    "CandViewCountFilter",
    src = cms.InputTag("muonPreSelectionMuEle"),
    minNumber = cms.uint32(1),
    )

muEleEleCounter = cms.EDFilter(
    "CandViewCountFilter",
    src = cms.InputTag("electronPreSelectionMuEle"),
    minNumber = cms.uint32(1),
    )

muEleSequence = cms.Sequence( #
    muonPreSelectionMuEle +   
    muEleMuCounter + 
    electronPreSelectionMuEle +   
    muEleEleCounter +
    cmgMuEle +
    # cmgMuEleCor+ # Correction only applies to taus, not needed for mu-ele
    cmgMuEleTauPtSel +
    cmgMuEleCorSVFitPreSel +
    cmgMuEleCorSVFitFullSel
    )


muElePath = cms.Path(
    # metRegressionSequence + 
    muEleSequence *
    muEleFullSelSkimSequence
    )
