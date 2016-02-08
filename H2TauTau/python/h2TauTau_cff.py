import FWCore.ParameterSet.Config as cms

from CMGTools.H2TauTau.objects.tauMuObjectsMVAMET_cff import tauMuSequence
from CMGTools.H2TauTau.objects.tauEleObjectsMVAMET_cff import tauEleSequence
from CMGTools.H2TauTau.objects.diTauObjectsMVAMET_cff import diTauSequence
from CMGTools.H2TauTau.objects.diMuObjectsMVAMET_cff import diMuSequence
from CMGTools.H2TauTau.objects.muEleObjectsMVAMET_cff import muEleSequence

from CMGTools.H2TauTau.skims.skim_cff import tauMuFullSelSkimSequence, tauEleFullSelSkimSequence, diTauFullSelSkimSequence, muEleFullSelSkimSequence, diMuFullSelSkimSequence


# Need to explicitly import all modules in all sequences for cms.load(..)
# to work properly in the top-level config

from CMGTools.H2TauTau.objects.mvaMetInputs_cff import mvaMetInputSequence, calibratedAK4PFJetsForPFMVAMEt, puJetIdForPFMVAMEt, ak4PFL1FastL2L3Corrector, ak4PFL1FastjetCorrector, ak4PFL2RelativeCorrector, ak4PFL3AbsoluteCorrector

from CMGTools.H2TauTau.objects.tauMuObjectsMVAMET_cff import mvaMETTauMu, cmgTauMu, cmgTauMuCor, cmgTauMuTauPtSel, cmgTauMuCorSVFitPreSel, cmgTauMuCorSVFitFullSel, tauMuMVAMetSequence, tauPreSelectionTauMu, muonPreSelectionTauMu, tauMuTauCounter, tauMuMuonCounter

from CMGTools.H2TauTau.objects.tauEleObjectsMVAMET_cff import mvaMETTauEle, cmgTauEle, cmgTauEleCor, cmgTauEleTauPtSel, cmgTauEleCorSVFitPreSel, cmgTauEleCorSVFitFullSel, tauEleMVAMetSequence, tauPreSelectionTauEle, electronPreSelectionTauEle, tauEleTauCounter, tauEleEleCounter

from CMGTools.H2TauTau.objects.diTauObjectsMVAMET_cff import mvaMETDiTau, cmgDiTau, cmgDiTauCor, cmgDiTauTauPtSel, cmgDiTauCorSVFitPreSel, cmgDiTauCorSVFitFullSel, diTauMVAMetSequence, tauPreSelectionDiTau, diTauTauCounter

from CMGTools.H2TauTau.objects.muEleObjectsMVAMET_cff import mvaMETMuEle, cmgMuEle, cmgMuEleCor, cmgMuEleTauPtSel, cmgMuEleCorSVFitPreSel, cmgMuEleCorSVFitFullSel, muEleMVAMetSequence, muonPreSelectionMuEle, electronPreSelectionMuEle, muEleMuCounter, muEleEleCounter

from CMGTools.H2TauTau.objects.diMuObjectsMVAMET_cff import mvaMETDiMu, cmgDiMu, cmgDiMuCor, cmgDiMuTauPtSel, cmgDiMuCorSVFitPreSel, cmgDiMuCorSVFitFullSel, diMuMVAMetSequence, muonPreSelectionDiMu, diMuMuCounter

from CMGTools.H2TauTau.skims.skim_cff import tauMuFullSelCount, tauEleFullSelCount, diTauFullSelCount, muEleFullSelCount, diMuFullSelCount

# MVA MET Inputs
# mvaMetInputPath = cms.Path(
    # mvaMetInputSequence
    # )

# tau-mu ---
tauMuPath = cms.Path(
    # metRegressionSequence + 
    tauMuSequence + 
    tauMuFullSelSkimSequence
    )

tauMuSequence.insert(tauMuSequence.index(tauMuMVAMetSequence), mvaMetInputSequence)

# tau-ele ---
tauElePath = cms.Path(
    # metRegressionSequence + 
    tauEleSequence + 
    tauEleFullSelSkimSequence     
    )

tauEleSequence.insert(tauEleSequence.index(tauEleMVAMetSequence), mvaMetInputSequence)

# tau-tau ---
diTauPath = cms.Path(
    # metRegressionSequence + 
    diTauSequence +
    diTauFullSelSkimSequence     
    )

diTauSequence.insert(diTauSequence.index(diTauMVAMetSequence), mvaMetInputSequence)

# tau-tau ---
diMuPath = cms.Path(
    # metRegressionSequence + 
    diMuSequence +
    diMuFullSelSkimSequence     
    )

diMuSequence.insert(diMuSequence.index(diMuMVAMetSequence), mvaMetInputSequence)

# mu-ele ---
muElePath = cms.Path(
    muEleSequence +
    muEleFullSelSkimSequence     
    )

muEleSequence.insert(muEleSequence.index(muEleMVAMetSequence), mvaMetInputSequence)

