################## 
## Triggers for HLT_MC_SPRING15 and Run II
## Based on HLT_MC_SPRING15 and /frozen/2015/25ns14e33/v2.1/HLT/V1 and /frozen/2015/50ns_5e33/v2.1/HLT/V5
## Names with _50ns are unprescaled at 50ns but prescaled at 25ns
## Names with _run1 are for comparing Spring15 MC to 8 TeV data: they're the closest thing I could find to run1 triggers, they're prescaled or even excluded in data but should appear in MC.

triggers_mumu_run1   = ["HLT_Mu17_Mu8_v*","HLT_Mu17_TkMu8_DZ_v*"]
triggers_mumu_iso    = [ "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v*", "HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_v*","HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_v*", "HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_v*" ]
triggers_mumu_noniso_50ns = [ "HLT_Mu27_TkMu8_v*" ]
triggers_mumu_noniso = [ "HLT_Mu30_TkMu11_v*" ]
triggers_mumu_ss = [ "HLT_Mu17_Mu8_SameSign_v*", "HLT_Mu17_Mu8_SameSign_DZ_v*" ]
triggers_mumu = triggers_mumu_iso

triggers_ee_run1   = ["HLT_Ele17_Ele12_CaloIdL_TrackIdL_IsoVL*" ]
triggers_ee = [ "HLT_Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v*", "HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v*" ]
# warning: ee trigger without DZ is prescaled
triggers_ee_nodz = [ "HLT_Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_v*" ]

triggers_mue_run1   = [ "HLT_Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v*", 
                        "HLT_Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVL_v*" ]
triggers_mue   = [ "HLT_Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v*", 
                   "HLT_Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVL_v*",
                   "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v*", 
                   "HLT_Mu23_TrkIsoVVL_Ele8_CaloIdL_TrackIdL_IsoVL_v*", 
                   "HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_v*" ]

triggers_mumu_ht =  [ "HLT_DoubleMu8_Mass8_PFHT300_v*" ]
triggers_ee_ht =  [ "HLT_DoubleEle8_CaloIdM_TrackIdM_Mass8_PFHT300_v*" ]
triggers_mue_ht = [ "HLT_Mu8_Ele8_CaloIdM_TrackIdM_Mass8_PFHT300_v*" ]

triggers_leptau = ["HLT_IsoMu19_eta2p1_LooseIsoPFTau20_v*", "HLT_Ele22_eta2p1_WPLoose_GSF_LooseIsoPFtau20_SingleL1_v*", "HLT_DoubleMediumIsoPFTau32_Trk1_eta2p1_Reg_v"] 

triggers_3e = [ "HLT_Ele16_Ele12_Ele8_CaloIdL_TrackIdL_v*" ]
triggers_3mu = [ "HLT_TripleMu_12_10_5_v*", "HLT_TripleMu_5_3_3_v*" ]
triggers_3mu_alt = [ "HLT_TrkMu15_DoubleTrkMu5NoFiltersNoVtx_v*" ]
triggers_2mu1e = [ "HLT_DiMu9_Ele9_CaloIdL_TrackIdL_v*" ]
triggers_2e1mu = [ "HLT_Mu8_DiEle12_CaloIdL_TrackIdL_v*" ]

triggers_1mu_iso_r  = [ 'HLT_IsoMu24_eta2p1_v*', 'HLT_IsoTkMu24_eta2p1_v*' ]
triggers_1mu_iso_w  = [ 'HLT_IsoMu18_v*', 'HLT_IsoMu20_v*', 'HLT_IsoTkMu20_v*',
                        "HLT_IsoTkMu22_v*", "HLT_IsoMu22_v*", 'HLT_IsoMu27_v*',
                        'HLT_IsoTkMu27_v*'  ]
triggers_1mu_iso_r_50ns = [ 'HLT_IsoMu17_eta2p1_v*', 'HLT_IsoTkMu17_eta2p1_v*'  ]
triggers_1mu_iso_w_50ns = [ 'HLT_IsoMu20_v*', 'HLT_IsoTkMu20_v*'  ]
triggers_1mu_noniso = [ 'HLT_Mu45_eta2p1_v*', 'HLT_Mu50_v*' ]
triggers_1mu_iso_50ns = triggers_1mu_iso_r_50ns + triggers_1mu_iso_w_50ns
triggers_1mu_iso      = triggers_1mu_iso_r + triggers_1mu_iso_w

# note: here the WP75 is th name in MC, WPLoose and WPTight should be in data
triggers_1e_50ns = [ "HLT_Ele27_eta2p1_WP75_Gsf_v*", "HLT_Ele27_eta2p1_WPLoose_Gsf_v*", "HLT_Ele27_eta2p1_WPTight_Gsf_v*" ]
triggers_1e      = [ "HLT_Ele22_WPLoose_Gsf_v*", "HLT_Ele22_CaloIdL_TrackIdL_IsoVL_v*", "HLT_Ele23_WPLoose_Gsf_v*", "HLT_Ele23_CaloIdL_TrackIdL_IsoVL_v*", "HLT_Ele27_WPLoose_Gsf_v*", "HLT_Ele27_eta2p1_WPLoose_Gsf_v*", "HLT_Ele27_WPTight_Gsf_v*", "HLT_Ele32_eta2p1_WPLoose_Gsf_v*", "HLT_Ele27_WP85_Gsf_v*", "HLT_Ele27_eta2p1_WP75_Gsf_v*", "HLT_Ele32_eta2p1_WP75_Gsf_v*" ]
triggers_1e_noniso      = [ "HLT_Ele105_CaloIdVT_GsfTrkIdT_v*","HLT_Ele115_CaloIdVT_GsfTrkIdT_v*"]

# Lepton fake rate triggers (prescaled)
triggers_FR_1mu_iso = [ "HLT_Mu%d_TrkIsoVVL_v*" % pt for pt in (8,17) ]
triggers_FR_1mu_noiso = [ "HLT_Mu%d_v*" % pt for pt in (8,17) ] + ["HLT_Mu3_PFJet40_v*"]
triggers_FR_1e_noiso = [ "HLT_Ele%d_CaloIdM_TrackIdM_PFJet30_v*" % pt for pt in (8,12,17,23,33) ]
triggers_FR_1e_iso   = [ "HLT_Ele%d_CaloIdL_TrackIdL_IsoVL_PFJet30_v*" % pt for pt in (12,17,23,33) ]
triggers_FR_1e_b2g = [ "HLT_Ele17_CaloIdL_TrkIdL_IsoVL_v*", "HLT_Ele12_CaloIdL_TrackIdL_IsoVL_v*" ]
triggers_FR_jetHT  = [ "HLT_PFHT200_v*", "HLT_PFHT250_v*", "HLT_PFHT350_v*" ]
triggers_FR_jet  =  [ "HLT_PFJet40_v*", "HLT_PFJet60_v*", "HLT_PFJet80_v*" ]
triggers_FR_muNoIso = [ "HLT_Mu%d_v*" % pt for pt in (20,27,) ] + [ "HLT_Mu%d_eta2p1_v*" % pt for pt in (45,) ] + [ "HLT_L2Mu%d_v*" % pt for pt in (10,) ]
triggers_FR_ZB      = [ "HLT_ZeroBias_v*" ] + [ "HLT_ZeroBias_part%d_v*" % i for i in xrange(1,9) ]

# tau triggers for EWKino
triggers_leptautau = ["HLT_IsoMu19_eta2p1_LooseIsoPFTau20_v*",
                      "HLT_Ele22_eta2p1_WPLoose_GSF_LooseIsoPFtau20_SingleL1_v*",
                      "HLT_DoubleMediumIsoPFTau32_Trk1_eta2p1_Reg_v"]

### GP: did not look at anything below this

triggers_SOS_doublemulowMET = ["HLT_DoubleMu3_PFMET50_v*"]
triggers_SOS_highMET = ["HLT_PFMET90_PFMHT90_IDTight_v*","HLT_PFMETNoMu90_PFMHTNoMu90_IDTight_v*","HLT_PFMET100_PFMHT100_IDTight_v*","HLT_PFMETNoMu100_PFMHTNoMu100_IDTight_v*", "HLT_PFMET110_PFMHT110_IDTight_v*", "HLT_PFMETNoMu110_PFMHTNoMu110_IDTight_v*", "HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_v*", "HLT_PFMET120_PFMHT120_IDTight_v*"]


### Mike ---> for the VV analysis 
triggers_dijet_fat=["HLT_PFHT650_WideJetMJJ900DEtaJJ1p5_v*","HLT_PFHT650_WideJetMJJ950DEtaJJ1p5_v*"]
### ----> for the MT2 analysis

triggers_MT2_mumu = ["HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v*", "HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_v*"]
triggers_MT2_ee = ["HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v*","HLT_Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v*"]
triggers_MT2_emu = ["HLT_Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v*", "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v*"]
triggers_MT2_mue = ["HLT_Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVL_v*", "HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_v*"]

#triggers_MT2_mue = triggers_mue + ["HLT_Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v*", "HLT_Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVL_v*"]

triggers_MT2_mu = ["HLT_IsoMu17_eta2p1_v*","HLT_IsoMu20_eta2p1_v*", "HLT_IsoMu20_v*", "HLT_IsoTkMu20_v*"]
triggers_MT2_e = ["HLT_Ele23_WPLoose_Gsf_v*", "HLT_Ele22_eta2p1_WPLoose_Gsf_v*","HLT_Ele22_eta2p1_WP75_Gsf_v*", "HLT_Ele23_WP75_Gsf_v*"]

triggers_HT900 = ["HLT_PFHT900_v*"]
triggers_HT800 = ["HLT_PFHT800_v*","HLT_ECALHT800_v*"]
triggers_MET170 = ["HLT_PFMET170_NoiseCleaned_v*"]
#other paths added in data:
triggers_MET170_NotCleaned = ["HLT_PFMET170_v*"]
triggers_MET170_HBHECleaned = ["HLT_PFMET170_HBHECleaned_v*"]
triggers_MET170_JetIdCleaned = ["HLT_PFMET170_JetIdCleaned_v*"]
triggers_AllMET170 = triggers_MET170 + triggers_MET170_NotCleaned + triggers_MET170_HBHECleaned + triggers_MET170_JetIdCleaned

triggers_MET300 = ["HLT_PFMET300_NoiseCleaned_v*"]
triggers_MET300_NotCleaned = ["HLT_PFMET300_v*"]
triggers_MET300_JetIdCleaned = ["HLT_PFMET300_JetIdCleaned_v*"]
triggers_AllMET300 = triggers_MET300 + triggers_MET300_NotCleaned + triggers_MET300_JetIdCleaned

triggers_HT350_MET120 = ["HLT_PFHT350_PFMET120_NoiseCleaned_v*"]
#triggers_HTMET100 = ["HLT_PFHT350_PFMET100_NoiseCleaned_v*"]
triggers_HT350_MET100 = ["HLT_PFHT350_PFMET100_JetIdCleaned_v*","HLT_PFHT350_PFMET100_NoiseCleaned_v*","HLT_PFHT350_PFMET100_v"]

triggers_HT350 = ["HLT_PFHT350_v*"] # prescaled
triggers_HT475 = ["HLT_PFHT475_v*"] # prescaled
triggers_HT600 = ["HLT_PFHT600_v*"] # prescaled

triggers_dijet = ["HLT_DiPFJetAve40_v*", "HLT_DiPFJetAve60_v*"]

triggers_jet = ["HLT_PFJet40_v*", "HLT_PFJet60_v*", "HLT_PFJet80_v*", "HLT_PFJet140_v*", "HLT_PFJet200_v*", "HLT_PFJet260_v*", "HLT_PFJet320_v*", "HLT_PFJet400_v*", "HLT_PFJet450_v*", "HLT_PFJet500_v*"]

triggers_dijet70met120 = [ "HLT_dijet70met120" ]
triggers_dijet55met110 = [ "HLT_dijet55met110" ]

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


# monojets triggers
#MC is NoiseCleaned but data will be JetIdCleaned
triggers_met90_mht90 = ["HLT_PFMET90_PFMHT90_IDTight_v*","HLT_PFMET90_PFMHT90_IDLoose_v*"]
triggers_met100_mht100 = ["HLT_PFMET100_PFMHT100_IDTight_v*","HLT_PFMET100_PFMHT100_IDLoose_v*"]
triggers_met120_mht120 = ["HLT_PFMET120_PFMHT120_IDTight_v*"]
triggers_metNoMu90_mhtNoMu90 = ["HLT_PFMETNoMu90_NoiseCleaned_PFMHTNoMu90_IDTight_v*","HLT_PFMETNoMu90_JetIdCleaned_PFMHTNoMu90_IDTight_v*","HLT_PFMETNoMu90_PFMHTNoMu90_IDTight_v*"]
triggers_metNoMu100_mhtNoMu100 = ["HLT_PFMETNoMu100_NoiseCleaned_PFMHTNoMu100_IDTight_v*","HLT_PFMETNoMu100_JetIdCleaned_PFMHTNoMu100_IDTight_v*","HLT_PFMETNoMu100_PFMHTNoMu100_IDTight_v*"]
triggers_metNoMu110_mhtNoMu110 = ["HLT_PFMETNoMu110_NoiseCleaned_PFMHTNoMu110_IDTight_v*","HLT_PFMETNoMu110_JetIdCleaned_PFMHTNoMu110_IDTight_v*","HLT_PFMETNoMu110_PFMHTNoMu110_IDTight_v*"]
triggers_metNoMu120_mhtNoMu120 = ["HLT_PFMETNoMu120_NoiseCleaned_PFMHTNoMu120_IDTight_v*","HLT_PFMETNoMu120_JetIdCleaned_PFMHTNoMu120_IDTight_v*","HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_v*"]
triggers_Jet80MET90 = ["HLT_MonoCentralPFJet80_PFMETNoMu90_NoiseCleaned_PFMHTNoMu90_IDTight_v*","HLT_MonoCentralPFJet80_PFMETNoMu90_JetIdCleaned_PFMHTNoMu90_IDTight_v*","HLT_MonoCentralPFJet80_PFMETNoMu90_PFMHTNoMu90_IDTight_v*"]
triggers_Jet80MET120 = ["HLT_MonoCentralPFJet80_PFMETNoMu120_NoiseCleaned_PFMHTNoMu120_IDTight_v*","HLT_MonoCentralPFJet80_PFMETNoMu90_JetIdCleaned_PFMHTNoMu120_IDTight_v*","HLT_MonoCentralPFJet80_PFMETNoMu120_PFMHTNoMu120_IDTight_v*"]
triggers_MET120Mu5 = ["HLT_PFMET120_NoiseCleaned_Mu5_v*"]

### ----> for the edgeZ analysis. 
## mumu
triggers_mu17mu8      = ['HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_v*']
triggers_mu17mu8_dz   = ['HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v*']
triggers_mu17tkmu8_dz = ['HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_v*']
##  emu
triggers_mu17el12     = ['HLT_Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v*']
triggers_mu8el17      = ['HLT_Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVL_v*']
triggers_mu8el23      = ['HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_v*']
## ee
triggers_el17el12_dz  = ['HLT_Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v*']
triggers_el23el12_dz  = ['HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v*']
#non isolated
triggers_mu30tkmu11   = ['HLT_Mu30_TkMu11_v*']
triggers_mu30ele30    = ['HLT_Mu30_Ele30_CaloIdL_GsfTrkIdVL_v*']
triggers_doubleele33  = ['HLT_DoubleEle33_CaloIdL_GsfTrkIdVL_v*']
#ht all exist
triggers_pfht200      = ['HLT_PFHT200_v*']
triggers_pfht250      = ['HLT_PFHT250_v*']
triggers_pfht300      = ['HLT_PFHT300_v*']
triggers_pfht350      = ['HLT_PFHT350_v*']
triggers_pfht400      = ['HLT_PFHT400_v*']
triggers_pfht475      = ['HLT_PFHT475_v*']
triggers_pfht600      = ['HLT_PFHT600_v*']
triggers_pfht650      = ['HLT_PFHT650_v*']
triggers_pfht800      = ['HLT_PFHT800_v*']
#change names of alphattriggers
triggers_at51         = ['HLT_PFHT400_DiPFJetAve90_PFAlphaT0p51_v*']
triggers_at52         = ['HLT_PFHT350_DiPFJetAve90_PFAlphaT0p52_v*']
triggers_at53         = ['HLT_PFHT300_DiPFJetAve90_PFAlphaT0p53_v*']
triggers_at54         = ['HLT_PFHT300_DiPFJetAve90_PFAlphaT0p54_v*']
triggers_at55         = ['HLT_PFHT250_DiPFJetAve90_PFAlphaT0p55_v*']
triggers_at57         = ['HLT_PFHT200_DiPFJetAve90_PFAlphaT0p57_v*']
triggers_at63         = ['HLT_PFHT200_DiPFJetAve90_PFAlphaT0p63_v*']
# still the same
triggers_htmet        = ['HLT_PFHT300_PFMET110_v*']
