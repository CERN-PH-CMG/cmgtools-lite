################## 
## Triggers for HLT_MC_SPRING15 and Run II
## Based on HLT_MC_SPRING15 and /frozen/2015/25ns14e33/v2.1/HLT/V1 and /frozen/2015/50ns_5e33/v2.1/HLT/V5


### ----> for the degStop





    
        
METTriggers = \
[\
 # CLEANUP # 'HLT_CaloMHTNoPU90_PFMET90_PFMHT90_IDTight_BTagCSV_p067_v*',
 # CLEANUP # 'HLT_CaloMHTNoPU90_PFMET90_PFMHT90_IDTight_v*',
 # CLEANUP # 'HLT_DiCentralPFJet55_PFMET110_v*',
 # CLEANUP # 'HLT_DoubleMu3_PFMET50_v*',

 # CLEANUP # 'HLT_MET200_v*',
 # CLEANUP # 'HLT_MET250_v*',
 # CLEANUP # 'HLT_MET300_v*',
 # CLEANUP # 'HLT_MET600_v*',
 # CLEANUP # 'HLT_MET60_IsoTrk35_Loose_v*',
 # CLEANUP # 'HLT_MET700_v*',
 # CLEANUP # 'HLT_MET75_IsoTrk50_v*',
 # CLEANUP # 'HLT_MET90_IsoTrk50_v*',
 # CLEANUP # 'HLT_Mu14er_PFMET100_v*',
 'HLT_Mu3er_PFHT140_PFMET125_v*',
 # CLEANUP # 'HLT_Mu6_PFHT200_PFMET100_v*',
 # CLEANUP # 'HLT_Mu6_PFHT200_PFMET80_BTagCSV_p067_v*',
 # CLEANUP # 'HLT_PFMET120_BTagCSV_p067_v*',
 'HLT_PFMET120_Mu5_v*',
 # CLEANUP # 'HLT_PFMET170_BeamHaloCleaned_v*',
 # CLEANUP # 'HLT_PFMET170_HBHECleaned_v*',
 # CLEANUP # 'HLT_PFMET170_JetIdCleaned_v*',
 'HLT_PFMET170_NoiseCleaned_v*',
 # CLEANUP # 'HLT_PFMET170_NotCleaned_v*',
 # CLEANUP # 'HLT_PFMET300_v*',
 # CLEANUP # 'HLT_PFMET400_v*',
 # CLEANUP # 'HLT_PFMET500_v*',
 # CLEANUP # 'HLT_PFMET600_v*',

 'HLT_PFMET100_PFMHT100_IDTight_v*',
 'HLT_PFMET110_PFMHT110_IDTight_v*',
 'HLT_PFMET120_PFMHT120_IDTight_v*',
 'HLT_PFMET90_PFMHT90_IDTight_v*',

 'HLT_MonoCentralPFJet80_PFMETNoMu100_PFMHTNoMu100_IDTight_v*',
 'HLT_MonoCentralPFJet80_PFMETNoMu110_PFMHTNoMu110_IDTight_v*',
 'HLT_MonoCentralPFJet80_PFMETNoMu120_PFMHTNoMu120_IDTight_v*',
 'HLT_MonoCentralPFJet80_PFMETNoMu90_PFMHTNoMu90_IDTight_v*',

 'HLT_PFMETNoMu100_PFMHTNoMu100_IDTight_v*',
 'HLT_PFMETNoMu110_PFMHTNoMu110_IDTight_v*',
 'HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_v*',
 'HLT_PFMETNoMu90_PFMHTNoMu90_IDTight_v*'
]


SingleElPDTriggers = \
[\
 # CLEANUP #  'HLT_Ele105_CaloIdVT_GsfTrkIdT_v*',
 # CLEANUP #  'HLT_Ele115_CaloIdVT_GsfTrkIdT_v*',
 # CLEANUP #  'HLT_Ele15_IsoVVVL_BTagCSV_p067_PFHT400_v*',
 # CLEANUP #  'HLT_Ele15_IsoVVVL_PFHT350_PFMET50_v*',
 # CLEANUP #  'HLT_Ele15_IsoVVVL_PFHT350_v*',
 # CLEANUP #  'HLT_Ele15_IsoVVVL_PFHT400_PFMET50_v*',
 # CLEANUP #  'HLT_Ele15_IsoVVVL_PFHT400_v*',
 # CLEANUP #  'HLT_Ele15_IsoVVVL_PFHT600_v*',
 # CLEANUP #  'HLT_Ele22_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_SingleL1_v*',
 'HLT_Ele22_eta2p1_WPLoose_Gsf_v*',
 # CLEANUP #  'HLT_Ele23_WPLoose_Gsf_WHbbBoost_v*',
 # CLEANUP #  'HLT_Ele23_WPLoose_Gsf_v*',
 # CLEANUP #  'HLT_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_SingleL1_v*',
 # CLEANUP #  'HLT_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_v*',
 'HLT_Ele24_eta2p1_WPLoose_Gsf_v*',
 # CLEANUP #  'HLT_Ele250_CaloIdVT_GsfTrkIdT_v*',
 'HLT_Ele25_WPTight_Gsf_v*',
 'HLT_Ele25_eta2p1_WPLoose_Gsf_v*',
 'HLT_Ele25_eta2p1_WPTight_Gsf_v*',
 # CLEANUP #  'HLT_Ele27_WPLoose_Gsf_WHbbBoost_v*',
 # CLEANUP #  'HLT_Ele27_WPLoose_Gsf_v*',
 # CLEANUP #  'HLT_Ele27_WPTight_Gsf_L1JetTauSeeded_v*',
 'HLT_Ele27_WPTight_Gsf_v*',
 # CLEANUP #  'HLT_Ele27_eta2p1_WPLoose_Gsf_DoubleMediumIsoPFTau32_Trk1_eta2p1_Reg_v*',
 # CLEANUP #  'HLT_Ele27_eta2p1_WPLoose_Gsf_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg_v*',
 # CLEANUP #  'HLT_Ele27_eta2p1_WPLoose_Gsf_DoubleMediumIsoPFTau40_Trk1_eta2p1_Reg_v*',
 'HLT_Ele27_eta2p1_WPLoose_Gsf_HT200_v*',
 # CLEANUP #  'HLT_Ele27_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_SingleL1_v*',
 # CLEANUP #  'HLT_Ele27_eta2p1_WPLoose_Gsf_v*',
 'HLT_Ele27_eta2p1_WPTight_Gsf_v*',
 # CLEANUP #  'HLT_Ele300_CaloIdVT_GsfTrkIdT_v*',
 # CLEANUP #  'HLT_Ele32_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_SingleL1_v*',
 'HLT_Ele32_eta2p1_WPTight_Gsf_v*',
 # CLEANUP #  'HLT_Ele35_CaloIdVT_GsfTrkIdT_PFJet150_PFJet50_v*',
 # CLEANUP #  'HLT_Ele35_WPLoose_Gsf_v*',
 # CLEANUP #  'HLT_Ele45_CaloIdVT_GsfTrkIdT_PFJet200_PFJet50_v*',
 # CLEANUP #  'HLT_Ele45_WPLoose_Gsf_L1JetTauSeeded_v*',
 # CLEANUP #  'HLT_Ele45_WPLoose_Gsf_v*',
 # CLEANUP #  'HLT_Ele50_CaloIdVT_GsfTrkIdT_PFJet140_v*',
 # CLEANUP #  'HLT_Ele50_CaloIdVT_GsfTrkIdT_PFJet165_v*',
 # CLEANUP #  'HLT_Ele50_IsoVVVL_PFHT400_v*'
]


SingleMuonPDTriggers=\
[\
   "HLT_IsoMu22_v*",
   "HLT_IsoMu22_eta2p1_v*",
   "HLT_IsoMu24_v*",
   "HLT_IsoMu27_v*",
   "HLT_IsoTkMu22_v*",
   "HLT_IsoTkMu22_eta2p1_v*",
   "HLT_IsoTkMu24_v*",
   "HLT_IsoTkMu27_v*",
   "HLT_Mu50_v*",
]

JetHTPDTriggers=\
[\
   #"HLT_PFHT125_v*",
   #"HLT_PFHT200_v*",
   #"HLT_PFHT250_v*", #prescaled
   #"HLT_PFHT300_v*", #prescaled
   #"HLT_PFHT350_v*", #prescaled
   #"HLT_PFHT400_v*", #prescaled
   #"HLT_PFHT475_v*", #prescaled
   #"HLT_PFHT600_v*", #prescaled
   #"HLT_PFHT650_v*", #prescaled
   "HLT_PFHT800_v*",
   "HLT_PFHT900_v*",
   "HLT_HT2000_v*",
   "HLT_HT2500_v*",
   #"HLT_AK8PFJet500_v*",
   #"HLT_DiPFJetAve100_HFJEC_v*",
   #"HLT_AK8PFHT700_TrimR0p1PT0p03Mass50_v*",
   "HLT_AK8PFJet450_v*",
   #"HLT_PFJet500_v*",
   #"HLT_DiPFJetAve60_HFJEC_v*",
   #"HLT_DiCentralPFJet430_v*",
   #"HLT_AK8DiPFJet280_200_TrimMass30_BTagCSV_p20_v*",
   #"HLT_PFHT400_SixJet30_DoubleBTagCSV_p056_v*",
   #"HLT_AK8PFJet360_TrimMass30_v*",
   #"HLT_CaloJet500_NoJetID_v*",
   #"HLT_PFHT750_4JetPt50_v*",
   #"HLT_DiPFJetAve300_HFJEC_v*",
   #"HLT_DiCentralPFJet330_CFMax0p5_v*",
   #"HLT_PFHT650_WideJetMJJ950DEtaJJ1p5_v*",
   "HLT_PFJet450_v*",
   #"HLT_PFHT450_SixJet40_BTagCSV_p056_v*",
   #"HLT_DiCentralPFJet170_v*",
   #"HLT_DiCentralPFJet220_CFMax0p3_v*",
   #"HLT_PFHT650_WideJetMJJ900DEtaJJ1p5_v*",
   #"HLT_DiCentralPFJet170_CFMax0p1_v*",
]
                                               
triggers = METTriggers + SingleMuonPDTriggers + SingleElPDTriggers + JetHTPDTriggers

for trigger in  triggers:
  trigger_name = "trigger_{trig}".format(trig=trigger.replace("_v*","") )
  exec("{trig_name}  =  [ '{trig}'] ".format(trig_name = trigger_name, trig=trigger))
                                           
                
        
                
            
                                    
    
                                    
                     
            
                                    
           
        
    
           
                            
    
                            
            
                 
        
           
                           
                                                  
                   
                    
                    
