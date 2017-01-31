# 2016 data
data_triggers = [
    'HLT_IsoMu24_v5',
    'HLT_IsoMu24_v4',
    'HLT_IsoMu24_v3',
    'HLT_IsoMu24_v2',
    'HLT_IsoMu24_v1',
    'HLT_IsoTkMu24_v5',
    'HLT_IsoTkMu24_v4',
    'HLT_IsoTkMu24_v3',
    'HLT_IsoTkMu24_v2',
    'HLT_IsoTkMu24_v1',
    'HLT_IsoMu19_eta2p1_LooseIsoPFTau20_v1',
    'HLT_IsoMu19_eta2p1_LooseIsoPFTau20_v2',
    'HLT_IsoMu19_eta2p1_LooseIsoPFTau20_v3',
    'HLT_IsoMu19_eta2p1_LooseIsoPFTau20_v4',
    'HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1_v1',
    'HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1_v2',
    'HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1_v3',
    'HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1_v4'
    ]

data_triggerfilters = [
    'hltL3crIsoL1sMu22L1f0L2f10QL3f24QL3trkIsoFiltered0p09', # IsoMu24
    'hltL3fL1sMu22L1f0Tkf24QL3trkIsoFiltered0p09', # IsoTkMu24
    'hltL3crIsoL1sMu18erTauJet20erL1f0L2f10QL3f19QL3trkIsoFiltered0p09', # IsoMu19_eta2p1_LooseIsoPFTau20
    'hltOverlapFilterIsoMu19LooseIsoPFTau20'# IsoMu19_eta2p1_LooseIsoPFTau20
]

mc_triggers = [
    'HLT_IsoMu24_v4',
    'HLT_IsoTkMu24_v4',
    'HLT_IsoMu19_eta2p1_LooseIsoPFTau20_v5',
    'HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1_v5',
    'HLT_IsoMu21_eta2p1_LooseIsoPFTau20_SingleL1_v5'
    ]

mc_triggerfilters = [
    # FIXME - to be checked
    'hltL3crIsoL1sMu22L1f0L2f10QL3f24QL3trkIsoFiltered0p09', #IsoMu24
    'hltL3fL1sMu22L1f0Tkf24QL3trkIsoFiltered0p09', # IsoTkMu24
    'hltOverlapFilterIsoMu19LooseIsoPFTau20',
    'hltPFTau20TrackLooseIsoAgainstMuon'
]

embed_triggers = [
    ]
