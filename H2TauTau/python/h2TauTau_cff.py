import FWCore.ParameterSet.Config as cms

from CMGTools.H2TauTau.objects.tauMuObjectsMVAMET_cff import tauMuSequence
from CMGTools.H2TauTau.objects.tauEleObjectsMVAMET_cff import tauEleSequence
from CMGTools.H2TauTau.objects.diTauObjectsMVAMET_cff import diTauSequence
from CMGTools.H2TauTau.objects.diMuObjectsMVAMET_cff import diMuSequence
from CMGTools.H2TauTau.objects.muEleObjectsMVAMET_cff import muEleSequence

from CMGTools.H2TauTau.skims.skim_cff import tauMuFullSelSkimSequence, tauEleFullSelSkimSequence, diTauFullSelSkimSequence, muEleFullSelSkimSequence, diMuFullSelSkimSequence


# Need to explicitly import all modules in all sequences for cms.load(..)
# to work properly in the top-level config

from CMGTools.H2TauTau.objects.tauMuObjectsMVAMET_cff import cmgTauMu, cmgTauMuCor, cmgTauMuTauPtSel, cmgTauMuCorSVFitPreSel, cmgTauMuCorSVFitFullSel, tauPreSelectionTauMu, muonPreSelectionTauMu, tauMuTauCounter, tauMuMuonCounter

from CMGTools.H2TauTau.objects.tauEleObjectsMVAMET_cff import cmgTauEle, cmgTauEleCor, cmgTauEleTauPtSel, cmgTauEleCorSVFitPreSel, cmgTauEleCorSVFitFullSel, tauPreSelectionTauEle, electronPreSelectionTauEle, tauEleTauCounter, tauEleEleCounter

from CMGTools.H2TauTau.objects.diTauObjectsMVAMET_cff import cmgDiTau, cmgDiTauCor, cmgDiTauTauPtSel, cmgDiTauCorSVFitPreSel, cmgDiTauCorSVFitFullSel, tauPreSelectionDiTau, diTauTauCounter

from CMGTools.H2TauTau.objects.muEleObjectsMVAMET_cff import cmgMuEle, cmgMuEleCor, cmgMuEleTauPtSel, cmgMuEleCorSVFitPreSel, cmgMuEleCorSVFitFullSel, muonPreSelectionMuEle, electronPreSelectionMuEle, muEleMuCounter, muEleEleCounter

from CMGTools.H2TauTau.objects.diMuObjectsMVAMET_cff import cmgDiMu, cmgDiMuCor, cmgDiMuTauPtSel, cmgDiMuCorSVFitPreSel, cmgDiMuCorSVFitFullSel, muonPreSelectionDiMu, diMuMuCounter

from CMGTools.H2TauTau.skims.skim_cff import tauMuFullSelCount, tauEleFullSelCount, diTauFullSelCount, muEleFullSelCount, diMuFullSelCount


# tau-mu ---
tauMuPath = cms.Path(
    # metRegressionSequence + 
    tauMuSequence *
    tauMuFullSelSkimSequence
    )

# tau-ele ---
tauElePath = cms.Path(
    # metRegressionSequence + 
    # tauEleSequence + 
    tauEleFullSelSkimSequence     
    )

# tau-tau ---
diTauPath = cms.Path(
    # metRegressionSequence + 
    # diTauSequence +
    diTauFullSelSkimSequence     
    )

# tau-tau ---
diMuPath = cms.Path(
    # metRegressionSequence + 
    # diMuSequence +
    diMuFullSelSkimSequence     
    )

# mu-ele ---
muElePath = cms.Path(
    muEleSequence +
    muEleFullSelSkimSequence     
    )
