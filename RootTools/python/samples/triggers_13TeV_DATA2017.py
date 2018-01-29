# Triggers for 2017 DATA

triggers_mumu_iso    = [ "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8_v*",
                         "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8_v*",
                         "HLT_Mu19_TrkIsoVVL_Mu9_TrkIsoVVL_DZ_Mass3p8_v*",
                         "HLT_Mu19_TrkIsoVVL_Mu9_TrkIsoVVL_DZ_Mass8_v*", ]
triggers_mumu_noniso = [ "HLT_Mu37_TkMu27_v*" ]
triggers_mumu_ss = [ "HLT_Mu18_Mu9_SameSign_v*",
                     "HLT_Mu18_Mu9_SameSign_DZ_v*", 
                     "HLT_Mu20_Mu10_SameSign_v*", 
                     "HLT_Mu20_Mu10_SameSign_DZ_v*" ]
triggers_mumu = triggers_mumu_iso

triggers_ee = [ "HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v*", 
                "HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_v*", ] 
triggers_ee_noniso = ["HLT_DoubleEle25_CaloIdL_MW_v*", 
                      "HLT_DoubleEle27_CaloIdL_MW_v*", 
                      "HLT_DoubleEle33_CaloIdL_MW_v*" ]

triggers_mue   = [ "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v*", 
                   "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v*", 
                   "HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v*" ]

triggers_mumu_ht =  [ "HLT_DoubleMu8_Mass8_PFHT350_v*",
                      "HLT_DoubleMu4_Mass8_DZ_PFHT350_v*" ]
triggers_ee_ht =  [ "HLT_DoubleEle8_CaloIdM_TrackIdM_Mass8_PFHT350_v*", 
                    "HLT_DoubleEle8_CaloIdM_TrackIdM_Mass8_DZ_PFHT350_v*", ]
triggers_mue_ht = [ "HLT_Mu8_Ele8_CaloIdM_TrackIdM_Mass8_PFHT350_DZ_v*" ]

triggers_3e = [ "HLT_Ele16_Ele12_Ele8_CaloIdL_TrackIdL_v*" ]
triggers_3mu = [ "HLT_TripleMu_10_5_5_DZ_v*", 
                 "HLT_TripleMu_12_10_5_v*", 
                 "HLT_TripleMu_5_3_3_Mass3p8to60_DCA_v*",
                 "HLT_TripleMu_5_3_3_Mass3p8to60_DZ_v*" ]
triggers_2mu1e = [ "HLT_DiMu9_Ele9_CaloIdL_TrackIdL_DZ_v*" ]
triggers_2e1mu = [ "HLT_Mu8_DiEle12_CaloIdL_TrackIdL_v*" ,
                   "HLT_Mu8_DiEle12_CaloIdL_TrackIdL_DZ_v*" ]

triggers_1mu_iso = [ 'HLT_IsoMu24_v*', 'HLT_IsoMu24_eta2p1_v*', # Prescaled at high lumi
                     'HLT_IsoMu27_v*'] # always unprescaled
triggers_1mu_noniso = [ 'HLT_Mu50_v*', 'HLT_Mu55_v*' ]

triggers_1e_iso = [ "HLT_Ele32_WPTight_Gsf_v*",
                    "HLT_Ele35_WPTight_Gsf_v*" ]
triggers_1e_noniso = [ "HLT_Ele115_CaloIdVT_GsfTrkIdT_v*"]


# HT:
triggers_pfht1050 = ['HLT_PFHT1050_v*']

# AK8 HT:
triggers_pfht800_mass50 = ['HLT_AK8PFHT800_TrimMass50_v*']

# PF Jet
triggers_pfjet500 = ['HLT_AK8PFJet500_v*']

# AK8 PF Jet
triggers_pfjet400_mass30 = ['HLT_AK8PFJet400_TrimMass30_v*']
