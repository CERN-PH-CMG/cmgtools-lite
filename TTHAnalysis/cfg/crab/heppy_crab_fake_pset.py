import FWCore.ParameterSet.Config as cms
process = cms.Process('FAKE')
process.source = cms.Source("EmptySource")
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))
process.output = cms.OutputModule("PoolOutputModule", fileName = cms.untracked.string('dummyOutput.root'))
process.out = cms.EndPath(process.output)
