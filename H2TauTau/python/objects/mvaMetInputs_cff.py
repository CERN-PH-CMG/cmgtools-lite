import FWCore.ParameterSet.Config as cms

from RecoMET.METPUSubtraction.mvaPFMET_cff import puJetIdForPFMVAMEt, calibratedAK4PFJetsForPFMVAMEt
from JetMETCorrections.Configuration.JetCorrectors_cff import ak4PFL1FastL2L3Corrector, ak4PFL1FastjetCorrector, ak4PFL2RelativeCorrector, ak4PFL3AbsoluteCorrector

puJetIdForPFMVAMEt.jec =  cms.string('AK4PF')
#process.puJetIdForPFMVAMEt.jets = cms.InputTag("ak4PFJets")
puJetIdForPFMVAMEt.vertexes = cms.InputTag("offlineSlimmedPrimaryVertices")
puJetIdForPFMVAMEt.rho = cms.InputTag("fixedGridRhoFastjetAll")

mvaMetInputSequence = cms.Sequence(
    ak4PFL1FastjetCorrector *
    ak4PFL2RelativeCorrector *
    ak4PFL3AbsoluteCorrector *
    ak4PFL1FastL2L3Corrector *
    calibratedAK4PFJetsForPFMVAMEt *
    puJetIdForPFMVAMEt
  )
