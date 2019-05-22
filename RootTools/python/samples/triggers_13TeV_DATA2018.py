# Triggers for 2018 DATA

#https://twiki.cern.ch/twiki/bin/view/CMS/EgHLTRunIISummary#2018_AN1
#https://twiki.cern.ch/twiki/bin/view/CMS/MuonHLT2018
#https://twiki.cern.ch/twiki/bin/view/CMS/HiggsZZ4lRunIILegacy#2018_AN1

triggers_mumu_iso    = [ "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8_v*" ]  
triggers_mumu_noniso = [ "HLT_Mu37_TkMu27_v*" ] # FIXME to be checked
triggers_mumu_ss = [ "HLT_Mu18_Mu9_SameSign_v*", # FIXME to be checked
                     "HLT_Mu18_Mu9_SameSign_DZ_v*", 
                     "HLT_Mu20_Mu10_SameSign_v*", 
                     "HLT_Mu20_Mu10_SameSign_DZ_v*" ]
triggers_mumu = triggers_mumu_iso

triggers_ee_iso = [ "HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_v*"  ] 
triggers_ee_noniso = ["HLT_DoubleEle25_CaloIdL_MW_v*"  ]
triggers_ee = triggers_ee_iso + triggers_ee_noniso

triggers_mue   = [ "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v*", 
                   "HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v*" ]

triggers_mumu_ht =  [ "HLT_DoubleMu8_Mass8_PFHT350_v*",
                      "HLT_DoubleMu4_Mass8_DZ_PFHT350_v*" ] # FIXME to be checked
triggers_ee_ht =  [ "HLT_DoubleEle8_CaloIdM_TrackIdM_Mass8_PFHT350_v*",  ]
triggers_mue_ht = [ "HLT_Mu8_Ele8_CaloIdM_TrackIdM_Mass8_PFHT350_DZ_v*" ]

triggers_3e = [ "HLT_Ele16_Ele12_Ele8_CaloIdL_TrackIdL_v*" ] # unprescaled for 54.7 out of 60 fb 
triggers_3mu = [ "HLT_TripleMu_10_5_5_DZ_v*",    
                 "HLT_TripleMu_12_10_5_v*", 
                 "HLT_TripleMu_5_3_3_Mass3p8_DCA_v*", # FIXME 5_3_3 to be checked
                 "HLT_TripleMu_5_3_3_Mass3p8_DZ_v*" ]
triggers_2mu1e = [ "HLT_DiMu9_Ele9_CaloIdL_TrackIdL_DZ_v*" ]
triggers_2e1mu = [ "HLT_Mu8_DiEle12_CaloIdL_TrackIdL_v*" ]

triggers_1mu_iso = [ 'HLT_IsoMu24_v*']  # Always unprescaled
triggers_1mu_noniso = [ 'HLT_Mu50_v*', 'HLT_OldMu100_v*', 'HLT_TkMu100_v' ] # POG recomm: OR with OldMu100 & TkMu100: recover the inefficiency on high pT (~O(100)GeV) muons due to global chi2/ndof cut in Mu50 trigger 

triggers_1e_iso = [ "HLT_Ele32_WPTight_Gsf_v*" ]
triggers_1e_noniso = [ "HLT_Ele115_CaloIdVT_GsfTrkIdT_v*"] 

# Prescaled lepton triggers
triggers_FR_1mu       = [ "HLT_Mu%d_TrkIsoVVL_v*" % pt for pt in (8,17,19) ] # DoubleMu PD
triggers_FR_1mu_noiso = [ "HLT_Mu%d_v*" % pt for pt in (8,17,19) ] # DoubleMu PD
triggers_FR_1mu_noiso_smpd = [ "HLT_Mu%d_v*" % pt for pt in (12,15,20,27) ] + ["HLT_Mu3_PFJet40_v*"] # SingleMu PD
triggers_FR_1mu_noiso_highpt = [ "HLT_Mu%d_v*" % pt for pt in (50,) ] # SingleMu PD
triggers_FR_1e_noiso = [ "HLT_Ele%d_CaloIdM_TrackIdM_PFJet30_v*" % pt for pt in (8,17,23) ] 
triggers_FR_1e_iso   = [ "HLT_Ele%d_CaloIdL_TrackIdL_IsoVL_PFJet30_v*" % pt for pt in (8,12,23) ] 


### Wrap all in a dictionary for easier importing of multiple years
all_triggers = dict((x.replace("triggers_",""),y) for (x,y) in locals().items() if x.startswith("triggers_") and isinstance(y,list))
