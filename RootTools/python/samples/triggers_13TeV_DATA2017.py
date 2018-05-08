# Triggers for 2017 DATA

triggers_mumu_iso    = [ "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8_v*",
                         "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8_v*",
                         "HLT_Mu19_TrkIsoVVL_Mu9_TrkIsoVVL_DZ_Mass3p8_v*", 
                         "HLT_Mu19_TrkIsoVVL_Mu9_TrkIsoVVL_DZ_Mass8_v*", ] # Note: Mass3p8 and 19/9 missing in early data 
triggers_mumu_noniso = [ "HLT_Mu37_TkMu27_v*" ] # Only in late data
triggers_mumu_ss = [ "HLT_Mu18_Mu9_SameSign_v*", # Only in late data
                     "HLT_Mu18_Mu9_SameSign_DZ_v*", 
                     "HLT_Mu20_Mu10_SameSign_v*", 
                     "HLT_Mu20_Mu10_SameSign_DZ_v*" ]
triggers_mumu = triggers_mumu_iso

triggers_ee = [ "HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v*", # Note: no-dz version missing in 2017B
                "HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_v*", ] 
triggers_ee_noniso = ["HLT_DoubleEle25_CaloIdL_MW_v*", # 25 and 27 missing in early part of 2017
                      "HLT_DoubleEle27_CaloIdL_MW_v*", 
                      "HLT_DoubleEle33_CaloIdL_MW_v*" ]

triggers_mue   = [ "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v*",  # NoDZ version only from 2017C
                   "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v*", 
                   "HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v*" ] # Mu8/Ele23 w/o DZ is always prescaled

# note: all dilepton+HT are missing in the early part of the data taking (2017B)
triggers_mumu_ht =  [ "HLT_DoubleMu8_Mass8_PFHT350_v*",
                      "HLT_DoubleMu4_Mass8_DZ_PFHT350_v*" ]
triggers_ee_ht =  [ "HLT_DoubleEle8_CaloIdM_TrackIdM_Mass8_PFHT350_v*", 
                    "HLT_DoubleEle8_CaloIdM_TrackIdM_Mass8_DZ_PFHT350_v*", ]
triggers_mue_ht = [ "HLT_Mu8_Ele8_CaloIdM_TrackIdM_Mass8_PFHT350_DZ_v*" ]

triggers_3e = [ "HLT_Ele16_Ele12_Ele8_CaloIdL_TrackIdL_v*" ] 
triggers_3mu = [ "HLT_TripleMu_10_5_5_DZ_v*", 
                 "HLT_TripleMu_12_10_5_v*", 
                 "HLT_TripleMu_5_3_3_Mass3p8to60_DCA_v*", # 5_3_3 only in late part of the data (esp. DCA one)
                 "HLT_TripleMu_5_3_3_Mass3p8to60_DZ_v*" ]
triggers_2mu1e = [ "HLT_DiMu9_Ele9_CaloIdL_TrackIdL_DZ_v*" ]
triggers_2e1mu = [ "HLT_Mu8_DiEle12_CaloIdL_TrackIdL_v*" ,
                   "HLT_Mu8_DiEle12_CaloIdL_TrackIdL_DZ_v*" ]

triggers_1mu_iso = [ 'HLT_IsoMu24_v*', 'HLT_IsoMu24_eta2p1_v*', # Prescaled at high lumi
                     'HLT_IsoMu27_v*']                          # Always unprescaled
triggers_1mu_noniso = [ 'HLT_Mu50_v*', 'HLT_Mu55_v*' ] # 55 only in late part of the data

triggers_1e_iso = [ "HLT_Ele32_WPTight_Gsf_v*", # Ele32 missing in Run2017B
                    "HLT_Ele35_WPTight_Gsf_v*" ]
triggers_1e_noniso = [ "HLT_Ele115_CaloIdVT_GsfTrkIdT_v*"] # Not 2017B

# Prescaled lepton triggers
triggers_FR_1mu_noiso = [ "HLT_Mu%d_v*" % pt for pt in (8,17) ] # DoubleMu PD
triggers_FR_1mu_noiso_highpt = [ "HLT_Mu%d_v*" % pt for pt in (20,27,50) ] + ["HLT_Mu3_PFJet40_v*"] # SingleMu PD
triggers_FR_1e_noiso = [ "HLT_Ele%d_CaloIdM_TrackIdM_PFJet30_v*" % pt for pt in (8,17,23) ] # SingleElectron
triggers_FR_1e_iso   = [ "HLT_Ele%d_CaloIdL_TrackIdL_IsoVL_PFJet30_v*" % pt for pt in (8,12,23) ] # SingleElectron


# HT:
triggers_pfht1050 = ['HLT_PFHT1050_v*']

# AK8 HT: not in 2017B, lower thresholds are prescaled
triggers_ak8pfht_mass50 = ['HLT_AK8PFHT%d_TrimMass50_v*' % ht for ht in (750, 800)]

# PF Jet
triggers_ak8pfjet = ['HLT_AK8PFJet500_v*']

# AK8 PF Jet: not in 2017B, lower thresholds are prescaled
triggers_ak8pfjet_mass30 = ['HLT_AK8PFJet%d_TrimMass30_v*' % pt for pt in (360, 380, 400)]


# MET and muon+MET triggers for SOS
triggers_SOS_doublemulowMET = ["HLT_DoubleMu3_DZ_PFMET50_PFMHT60_v*"]
triggers_SOS_highMET = ["HLT_PFMETNoMu100_PFMHTNoMu100_IDTight_PFHT60","HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_PFHT60","HLT_PFMETNoMu120_PFMHTNoMu120_IDTight", "HLT_PFMETNoMu140_PFMHTNoMu140_IDTight"] #NoMu version
#triggers_SOS_highMET = ["HLT_PFMET100_PFMHT100_IDTight_PFHT60","HLT_PFMET120_PFMHT120_IDTight_PFHT60","HLT_PFMET120_PFMHT120_IDTight", "HLT_PFMET140_PFMHT140_IDTight"] 
triggers_SOS_tripleMu = ["HLT_TripleMu_5_3_3_Mass3p8to60_DZ_v*"]
