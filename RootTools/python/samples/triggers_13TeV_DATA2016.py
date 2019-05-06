################## 
## Triggers for 2016 DATA 

triggers_mumu_iso    = [ "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_v*", 
                         "HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_v*",
                         "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v*",
                         "HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_v*",
                         "HLT_Mu23_TrkIsoVVL_Mu8_TrkIsoVVL_v*", 
                         "HLT_Mu23_TrkIsoVVL_TkMu8_TrkIsoVVL_v*",
                         "HLT_Mu23_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v*",
                         "HLT_Mu23_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_v*" ]
triggers_mumu_noniso = [ "HLT_Mu30_TkMu11_v*" ]
triggers_mumu_ss = [ "HLT_Mu17_Mu8_SameSign_v*",
                     "HLT_Mu17_Mu8_SameSign_DZ_v*", 
                     "HLT_Mu20_Mu10_SameSign_v*", 
                     "HLT_Mu20_Mu10_SameSign_DZ_v*" ]
triggers_mumu = triggers_mumu_iso

triggers_ee = [ "HLT_Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v*", 
                "HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v*" ] # 17/12 prescaled in column 0
triggers_ee_noniso = ["HLT_DoubleEle33_CaloIdL_v*", 
                      "HLT_DoubleEle37_Ele27_CaloIdL_GsfTrkIdVL_v*", 
                      "HLT_DoubleEle33_CaloIdL_GsfTrkIdVL_v" ]

# warning: ee trigger without DZ is prescaled
triggers_ee_nodz = [ "HLT_Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_v*" ]

triggers_mue_run1   = [ "HLT_Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v*", 
                        "HLT_Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVL_v*" ]
triggers_mue   = [ "HLT_Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v*", # warning, check prescales depending on run range 
                   "HLT_Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVL_v*",
                   "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v*", 
                   "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v*", 
                   "HLT_Mu23_TrkIsoVVL_Ele8_CaloIdL_TrackIdL_IsoVL_v*",
                   "HLT_Mu23_TrkIsoVVL_Ele8_CaloIdL_TrackIdL_IsoVL_DZ_v*",
                   "HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_v*",
                   "HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v*" ]

triggers_mumu_ht =  [ "HLT_DoubleMu8_Mass8_PFHT300_v*" ]
triggers_ee_ht =  [ "HLT_DoubleEle8_CaloIdM_TrackIdM_Mass8_PFHT300_v*" ]
triggers_mue_ht = [ "HLT_Mu8_Ele8_CaloIdM_TrackIdM_Mass8_PFHT300_v*" ]

triggers_leptau = ["HLT_IsoMu19_eta2p1_LooseIsoPFTau20_v*",
                   #"HLT_Ele22_eta2p1_WPLoose_GSF_LooseIsoPFtau20_SingleL1_v*",
                   "HLT_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau30_v*",
                   "HLT_Ele36_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_SingleL1_v*",
                   "HLT_DoubleMediumIsoPFTau32_Trk1_eta2p1_Reg_v"]

triggers_3e = [ "HLT_Ele16_Ele12_Ele8_CaloIdL_TrackIdL_v*" ]
triggers_3mu = [ "HLT_TripleMu_12_10_5_v*", 
                 "HLT_TripleMu_5_3_3_v*" ] # 533 only in part of the dataset
triggers_3mu_alt = [ "HLT_TrkMu15_DoubleTrkMu5NoFiltersNoVtx_v*" ]
triggers_2mu1e = [ "HLT_DiMu9_Ele9_CaloIdL_TrackIdL_v*" ]
triggers_2e1mu = [ "HLT_Mu8_DiEle12_CaloIdL_TrackIdL_v*" ]

triggers_1mu_iso = [ 'HLT_IsoMu20_v*', 
                     'HLT_IsoTkMu20_v*', 
                     'HLT_IsoMu22_v*', 
                     'HLT_IsoTkMu22_v*',
                     'HLT_IsoMu24_v*', # Mu20's prescaled in column 0
                     'HLT_IsoTkMu24_v*',
                     'HLT_IsoMu22_eta2p1_v',
                     'HLT_IsoTkMu22_eta2p1_v']
triggers_1mu_noniso = [ 'HLT_Mu45_eta2p1_v*', 
                        'HLT_Mu50_v*', 
                        'HLT_TkMu50_v*' ]

# note: here the WP75 is th name in MC, WPLoose and WPTight should be in data
triggers_1e      = [ 
        #"HLT_Ele23_WPLoose_Gsf_v*", # only up to 5E33
        #"HLT_Ele27_WPLoose_Gsf_v*", # only up to 5E33
        "HLT_Ele25_WPTight_Gsf_v*",        # not in column 0
        "HLT_Ele25_eta2p1_WPLoose_Gsf_v*", # not in column 0 
        "HLT_Ele25_eta2p1_WPTight_Gsf_v*", 
        "HLT_Ele27_WPTight_Gsf_v*", 
        "HLT_Ele27_eta2p1_WPLoose_Gsf_v*",
        "HLT_Ele45_WPLoose_Gsf_v*" ]
triggers_1e_noniso      = [ "HLT_Ele105_CaloIdVT_GsfTrkIdT_v*","HLT_Ele115_CaloIdVT_GsfTrkIdT_v*"]

# Lepton fake rate triggers (prescaled)
triggers_FR_1mu_iso = [ "HLT_Mu%d_TrkIsoVVL_v*" % pt for pt in (8,17) ] # DoubleMu PD
triggers_FR_1mu_noiso = [ "HLT_Mu%d_v*" % pt for pt in (8,17) ] + ["HLT_Mu3_PFJet40_v*"] # DoubleMu PD
triggers_FR_1e_noiso = [ "HLT_Ele%d_CaloIdM_TrackIdM_PFJet30_v*" % pt for pt in (8,12,17,23,33) ] + [ "HLT_Ele10_CaloIdM_TrackIdM_CentralPFJet30_BTagCSV_p13_v*" ]# DoubleEG
triggers_FR_1e_iso   = [ "HLT_Ele%d_CaloIdL_TrackIdL_IsoVL_PFJet30_v*" % pt for pt in (8,12,17,23,33) ] # DoubleEG
triggers_FR_1e_b2g = [ "HLT_Ele17_CaloIdL_TrkIdL_IsoVL_v*", "HLT_Ele12_CaloIdL_TrackIdL_IsoVL_v*" ]
triggers_FR_jet  =  [ "HLT_PFJet40_v*", "HLT_PFJet60_v*", "HLT_PFJet80_v*" ]
triggers_FR_muNoIso = [ "HLT_Mu%d_v*" % pt for pt in (20,27,50) ] #+ [ "HLT_Mu%d_eta2p1_v*" % pt for pt in (24,45,) ] + [ "HLT_L2Mu%d_v*" % pt for pt in (10,) ] # SingleMu PD

### GP: did not look at anything below this

triggers_SOS_doublemulowMET = ["HLT_DoubleMu3_PFMET50_v*"]
triggers_SOS_highMET = ["HLT_PFMET90_PFMHT90_IDTight_v*","HLT_PFMETNoMu90_PFMHTNoMu90_IDTight_v*","HLT_PFMET100_PFMHT100_IDTight_v*","HLT_PFMETNoMu100_PFMHTNoMu100_IDTight_v*", "HLT_PFMET110_PFMHT110_IDTight_v*", "HLT_PFMETNoMu110_PFMHTNoMu110_IDTight_v*", "HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_v*", "HLT_PFMET120_PFMHT120_IDTight_v*"]
triggers_SOS_tripleMu = ["HLT_TripleMu_5_3_3","HLT_TripleMu_5_3_3_DZ_Mass3p8_v1"]


### Mike ---> for the VV analysis 
triggers_dijet_fat=["HLT_PFHT650_WideJetMJJ900DEtaJJ1p5_v*","HLT_PFHT650_WideJetMJJ950DEtaJJ1p5_v*"]
# triggers to recover HT trigger inefficiency in late 2016
triggers_jet_recoverHT=["HLT_PFJet450_v*", "HLT_PFJet500_v*", "HLT_AK8PFJet450_v*", "HLT_AK8PFJet500_v*", "HLT_CaloJet500_NoJetID_v*"]
### ----> for the MT2 analysis

triggers_MT2_mumu = ["HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v*", "HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_v*"]
triggers_MT2_ee = ["HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v*","HLT_Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v*"]
triggers_MT2_emu = ["HLT_Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v*", "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v*"]
triggers_MT2_mue = ["HLT_Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVL_v*", "HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_v*"]

#triggers_MT2_mue = triggers_mue + ["HLT_Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v*", "HLT_Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVL_v*"]

triggers_MT2_mu = ["HLT_IsoMu17_eta2p1_v*","HLT_IsoMu20_eta2p1_v*", "HLT_IsoMu20_v*", "HLT_IsoTkMu20_v*"]
triggers_MT2_e = ["HLT_Ele23_WPLoose_Gsf_v*", "HLT_Ele22_eta2p1_WPLoose_Gsf_v*","HLT_Ele22_eta2p1_WP75_Gsf_v*", "HLT_Ele23_WP75_Gsf_v*"]

triggers_HT900 = ["HLT_PFHT900_v*"]
triggers_HT800 = ["HLT_PFHT800_v*"]
#triggers_MET170 = ["HLT_PFMET170_NoiseCleaned_v*"] #removed from menu
#other paths added in data:
triggers_MET170_NotCleaned = ["HLT_PFMET170_NotCleaned_v*"]
triggers_MET170_HBHECleaned = ["HLT_PFMET170_HBHECleaned_v*"]
triggers_MET170_BeamHaloCleaned = ["HLT_PFMET170_BeamHaloCleaned_v*"] # removed from the menu
triggers_AllMET170 = triggers_MET170_NotCleaned + triggers_MET170_HBHECleaned 

triggers_MET300 = ["HLT_PFMET300_v*"] #not in 2016 menu anymore
#triggers_MET300_NotCleaned = ["HLT_PFMET300_v*"]
#triggers_MET300_JetIdCleaned = ["HLT_PFMET300_JetIdCleaned_v*"] #not in 2016 menu anymore
triggers_AllMET300 = triggers_MET300 

#triggers_HT350_MET120 = ["HLT_PFHT350_PFMET120_NoiseCleaned_v*"] # not in 2016 menu anymore
#triggers_HTMET100 = ["HLT_PFHT350_PFMET100_NoiseCleaned_v*"]
triggers_HT350_MET100 = ["HLT_PFHT350_PFMET100_v"]

triggers_HT350 = ["HLT_PFHT350_v*"] # prescaled
triggers_HT475 = ["HLT_PFHT475_v*"] # prescaled
triggers_HT600 = ["HLT_PFHT600_v*"] # prescaled

triggers_dijet = ["HLT_DiPFJetAve40_v*", "HLT_DiPFJetAve60_v*"]

triggers_jet = ["HLT_PFJet40_v*", "HLT_PFJet60_v*", "HLT_PFJet80_v*", "HLT_PFJet140_v*", "HLT_PFJet200_v*", "HLT_PFJet260_v*", "HLT_PFJet320_v*", "HLT_PFJet400_v*", "HLT_PFJet450_v*", "HLT_PFJet500_v*"]

triggers_dijet70met120 = [ "HLT_DiCentralPFJet70_PFMET120_v*" ]
triggers_dijet55met110 = [ "HLT_DiCentralPFJet55_PFMET110_v*" ]

triggers_photon75ps = ["HLT_Photon75_v*"]
triggers_photon90ps = ["HLT_Photon90_v*"]
triggers_photon120ps = ["HLT_Photon120_v*"]
triggers_photon30 = ["HLT_Photon30_R9Id90_HE10_IsoM_v*"]
triggers_photon50 = ["HLT_Photon50_R9Id90_HE10_IsoM_v*"]
triggers_photon75 = ["HLT_Photon75_R9Id90_HE10_IsoM_v*"]
triggers_photon90 = ["HLT_Photon90_R9Id90_HE10_IsoM_v*"]
triggers_photon120 = ["HLT_Photon120_R9Id90_HE10_IsoM_v*"]
triggers_photon155 = ["HLT_Photon155_v*"]
triggers_photon175 = ["HLT_Photon175_v*"]
triggers_photon165_HE10 = ["HLT_Photon165_HE10_v*"]

# there is no jetId or Noise Cleaned path in 2016 menu  all met, met cross paths by defult have HBHE cleaning applied
# monojets triggers
triggers_met90_mht90 = ["HLT_PFMET90_PFMHT90_IDTight_v*","HLT_PFMET90_PFMHT90_IDLoose_v*"]
triggers_met100_mht100 = ["HLT_PFMET100_PFMHT100_IDTight_v*","HLT_PFMET100_PFMHT100_IDLoose_v*"]
triggers_met120_mht120 = ["HLT_PFMET120_PFMHT120_IDTight_v*"]
#triggers_metNoMu90_mhtNoMu90 = ["HLT_PFMETNoMu90_NoiseCleaned_PFMHTNoMu90_IDTight_v*","HLT_PFMETNoMu90_JetIdCleaned_PFMHTNoMu90_IDTight_v*","HLT_PFMETNoMu90_PFMHTNoMu90_IDTight_v*"]
triggers_metNoMu90_mhtNoMu90 = ["HLT_PFMETNoMu90_PFMHTNoMu90_IDTight_v*"]
triggers_metNoMu120_mhtNoMu120 = ["HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_v*"]
triggers_Jet80MET90 = ["HLT_MonoCentralPFJet80_PFMETNoMu90_PFMHTNoMu90_IDTight_v*"]
triggers_Jet80MET120 = ["HLT_MonoCentralPFJet80_PFMETNoMu120_PFMHTNoMu120_IDTight_v*"]
triggers_MET120Mu5 = ["HLT_PFMET120_Mu5_v*"]

### ----> for the edgeZ analysis. 
### we want them separately for detailed trigger efficiency studies
###---- Muons
# Isolated triggers:
triggers_mu17mu8_dz      = ['HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v*']
triggers_mu17tkmu8       = ['HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_v*']
triggers_mu17tkmu8_dz    = ['HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_v*']
# Non-Isolated triggers:
triggers_mu27tkmu8       = ['HLT_Mu27_TkMu8_v*']
triggers_mu30tkmu11      = ['HLT_Mu30_TkMu11_v*']
###---- Electrons
# Isolated triggers:
triggers_el23el12_dz     = ['HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v*']
# Non-Isolated triggers:
triggers_doubleele33     = ['HLT_DoubleEle33_CaloIdL_GsfTrkIdVL_v*']
triggers_doubleele33_MW  = ['HLT_DoubleEle33_CaloIdL_GsfTrkIdVL_MW_v*']
###---- Electron-Muon
triggers_mu23el12        = ['HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v*']
triggers_mu8el23         = ['HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_v*']
# Non-Isolated triggers:
triggers_mu30ele30       = ['HLT_Mu30_Ele30_CaloIdL_GsfTrkIdVL_v*']
###---- HT:
triggers_pfht200      = ['HLT_PFHT200_v*']
triggers_pfht250      = ['HLT_PFHT250_v*']
triggers_pfht300      = ['HLT_PFHT300_v*']
triggers_pfht350      = ['HLT_PFHT350_v*']
triggers_pfht400      = ['HLT_PFHT400_v*']
triggers_pfht475      = ['HLT_PFHT475_v*']
triggers_pfht600      = ['HLT_PFHT600_v*']
triggers_pfht650      = ['HLT_PFHT650_v*']
triggers_pfht800      = ['HLT_PFHT800_v*']
triggers_pfht900      = ['HLT_PFHT900_v*']
triggers_at57         = ['HLT_PFHT200_DiPFJet90_PFAlphaT0p57_v*']
triggers_at55         = ['HLT_PFHT250_DiPFJet90_PFAlphaT0p55_v*']
triggers_at53         = ['HLT_PFHT300_DiPFJet90_PFAlphaT0p53_v*']
triggers_at52         = ['HLT_PFHT350_DiPFJet90_PFAlphaT0p52_v*']
triggers_at51         = ['HLT_PFHT400_DiPFJet90_PFAlphaT0p51_v*']
triggers_htmet        = ['HLT_PFHT350_PFMET120_NoiseCleaned_v*']
triggers_htjet        = ['HLT_PFHT550_4Jet_v*', 'HLT_PFHT650_4Jet_v*', 'HLT_PFHT750_4Jet_v*']
triggers_mu30ele30    = ['HLT_Mu30_Ele30_CaloIdL_GsfTrkIdVL_v*']
triggers_doubleele33  = ['HLT_DoubleEle33_CaloIdL_GsfTrkIdVL_v*']
triggers_pfht = triggers_pfht200 + triggers_pfht250 + triggers_pfht300 + triggers_pfht350 + triggers_pfht400 + triggers_pfht475 + triggers_pfht600 + triggers_pfht650 + triggers_pfht800
###---- MET:
triggers_htmet = ['HLT_PFHT300_PFMET110_v*']

all_triggers = dict((x.replace("triggers_",""),y) for (x,y) in locals().items() if x.startswith("triggers_") and isinstance(y,list))
