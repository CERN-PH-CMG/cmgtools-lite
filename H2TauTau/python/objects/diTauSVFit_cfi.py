import FWCore.ParameterSet.Config as cms

diTauSVFit = cms.EDProducer(
    "TauTauWithSVFitProducer",
    diTauSrc = cms.InputTag("cmgDiTauTauPtSel"),
    SVFitVersion =  cms.int32(2), # 1 for 2011 version, 2 for new 2012 (slow) version
    fitAlgo = cms.string('MC'),
    verbose = cms.untracked.bool(False),
    p4TransferFunctionFile = cms.untracked.string('CMGTools/SVfitStandalone/data/svFitVisMassAndPtResolutionPDF.root'),
    integrateOverP4 = cms.untracked.bool(False),
    )
