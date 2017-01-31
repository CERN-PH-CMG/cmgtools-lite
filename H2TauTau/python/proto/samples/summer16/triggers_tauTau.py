data_triggers = [
    'HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg_v2', # up to run 274733
    'HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg_v3', # up to run 276837
    'HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg_v4', # up to run 278240
    'HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg_v5', # up to run 280960
    'HLT_DoubleMediumCombinedIsoPFTau35_Trk1_eta2p1_Reg_v2', # up to run 282544
    'HLT_DoubleMediumCombinedIsoPFTau35_Trk1_eta2p1_Reg_v3', # up to run 284044

    'HLT_VLooseIsoPFTau140_Trk50_eta2p1_v1', # runs 274748-276244
    'HLT_VLooseIsoPFTau140_Trk50_eta2p1_v2', # runs 276271-278240
    'HLT_VLooseIsoPFTau140_Trk50_eta2p1_v3', # runs 278270-280960
    'HLT_VLooseIsoPFTau140_Trk50_eta2p1_v5', # runs 281010-284044
    ]

data_triggerfilters = [
    'hltDoublePFTau35TrackPt1MediumIsolationDz02Reg', # same trigger filter for all
    'hltDoublePFTau35TrackPt1MediumCombinedIsolationDz02Reg',
    'hltPFTau140TrackPt50LooseAbsOrRelVLooseIso'
]

mc_triggers = [
    'HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg_v5',
    'HLT_DoubleMediumCombinedIsoPFTau35_Trk1_eta2p1_Reg_v2',
    # 'HLT_DoubleMediumCombinedIsoPFTau40_Trk1_eta2p1_Reg_v1', # higher threshold
    'HLT_VLooseIsoPFTau140_Trk50_eta2p1_v5',
    'HLT_VLooseIsoPFTau120_Trk50_eta2p1_v5',
    # 'HLT_PFTau140_eta2p1_v5' # prescaled
    
    ]

mc_triggerfilters = [
    'hltDoublePFTau35TrackPt1MediumIsolationDz02Reg', # 
    'hltDoublePFTau35TrackPt1MediumCombinedIsolationDz02Reg',
    # 'hltDoublePFTau35TrackPt1MediumCombinedIsolationL1HLTMatchedReg',
    'hltPFTau140TrackPt50LooseAbsOrRelVLooseIso',
    'hltPFTau120TrackPt50LooseAbsOrRelVLooseIso',
]

embed_triggers = [
    ]
