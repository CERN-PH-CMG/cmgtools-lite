import copy

common = [
    # 'drop *',
    'keep double_fixedGridRho*_*_*',
    'keep edmTriggerResults_TriggerResults_*_*',
    'keep patPackedTriggerPrescales_*_*_*',
    'keep patElectrons_slimmedElectrons_*_*',
    'keep patJets_slimmedJets_*_*',
    'keep patJets_patJetsReapplyJEC_*_*',
    'keep patMETs_slimmedMETs_*_*',
    'keep patMuons_slimmedMuons_*_*',
    # 'keep patPacked*_*_*_*',
    'keep patPackedCandidate*_*packedPFCandidates*_*_*', # RIC: agreed to keep it to: 1. tau vtx 2. possibly compute isolations at analysis level
    # 'keep patTaus_slimmedTaus_*_*',
    'keep patTaus_slimmedTausExtraIDs_*_*',
    'keep patTrigger*_*_*_*',
    'keep recoVertexs_*_*_*',
    'keep cmgMETSignificances_*_*_*',
    'keep patCompositeCandidates_cmg*CorSVFitFullSel_*_H2TAUTAU',
    'keep patJets_patJetsAK4PF_*_*',
    'keep PileupSummaryInfos_*_*_*',
    'keep recoGenParticles_prunedGenParticles_*_*',
    'keep patPackedGenParticles_packedGenParticles__*', # these are status 1
    'keep recoGsfElectronCores_*_*_*', # needed?
    'keep recoSuperClusters_*_*_*', # for electron MVA ID
    'keep recoGenJets_slimmedGenJets_*_*',
    'keep *_slimmedSecondaryVertices_*_*',
    'keep patPackedCandidates_packedPFCandidates__*',
    'keep *_puppi_*_*',
    'keep *_slimmedMETsPuppi_*_*',
    'keep *_generator_*_*',
    'keep *_genEvtWeightsCounter_*_H2TAUTAU',
    'keep *_offlineBeamSpot_*_*',
    'keep *_reducedEgamma_reducedConversions_*',
    'keep LHEEventProduct_*_*_*',
    'keep *_l1extraParticles_*_*',
    'keep patPATTauDiscriminator_*_*_H2TAUTAU',
    # 'keep *_mvaMETTauMu_*_H2TAUTAU'
    'keep *_BadPFMuonFilter_*_H2TAUTAU',
    'keep *_BadChargedCandidateFilter_*_H2TAUTAU'
    ]

commonDebug = copy.deepcopy(common) 
commonDebug.extend([
    'keep patCompositeCandidates_*_*_*', # keep all intermediate di-taus
    'keep patElectrons_*_*_*'
    ])
