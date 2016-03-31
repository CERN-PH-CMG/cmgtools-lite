import PhysicsTools.HeppyCore.framework.config as cfg

from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator

creator = ComponentCreator()


VVTo2L2Nu   = creator.makeMCComponent('VVTo2L2Nu'  , '/VVTo2L2Nu_13TeV_amcatnloFXFX_madspin_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'  , 'CMS', '.*root', 11.95 ) #  MG5_aMCNLO      2855237           11.95  (NLO, up to 1jet in ME)     
ZZTo2L2Q    = creator.makeMCComponent('ZZTo2L2Q'   , '/ZZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'   , 'CMS', '.*root',  3.22 ) #  MG5_aMCNLO     15301695            3.22  (NLO, up to 1jet in ME)     
ZZTo4L      = creator.makeMCComponent('ZZTo4L'     , '/ZZTo4L_13TeV-amcatnloFXFX-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'             , 'CMS', '.*root',  1.212) #  MG5_aMCNLO     10746497            1.212 (NLO)     
WWTo1L1Nu2Q = creator.makeMCComponent('WWTo1L1Nu2Q', '/WWTo1L1Nu2Q_13TeV_amcatnloFXFX_madspin_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM', 'CMS', '.*root', 49.997) #  MG5_aMCNLO      5244258           49.997 (NNLO)     
WZTo2L2Q    = creator.makeMCComponent('WZTo2L2Q'   , '/WZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'   , 'CMS', '.*root',  5.595) #  MG5_aMCNLO     25850479            5.595 (NLO, up to 1jet in ME)     
WZJets      = creator.makeMCComponent('WZJets'     , '/WZJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM', 'CMS', '.*root',  5.26 ) #  MG5_aMCNLO     12542004            5.26  (NLO, up to 1jet in ME)    3LNu sample, use Mll > 30
WZTo1L3Nu   = creator.makeMCComponent('WZTo1L3Nu'  , '/WZTo1L3Nu_13TeV_amcatnloFXFX_madspin_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'  , 'CMS', '.*root',  3.05 ) #  MG5_aMCNLO      1703772            3.05  (NLO)     
WZTo1L1Nu2Q = creator.makeMCComponent('WZTo1L1Nu2Q', '/WZTo1L1Nu2Q_13TeV_amcatnloFXFX_madspin_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM', 'CMS', '.*root', 10.71 ) #  MG5_aMCNLO     19742520           10.71  (NLO, up to 1jet in ME)     

diboson = [
    VVTo2L2Nu, 
    ZZTo2L2Q, 
    ZZTo4L, 
    WWTo1L1Nu2Q, 
    WZTo2L2Q, 
    WZJets, 
    WZTo1L3Nu, 
    WZTo1L1Nu2Q, 
]

T_tbarW    = creator.makeMCComponent('T_tbarW'   , '/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'    , 'CMS', '.*root',        35.6  ) #  Powheg           999400           35.6   (approx. NNLO)     
T_tW       = creator.makeMCComponent('T_tW'      , '/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'        , 'CMS', '.*root',        35.6  ) #  Powheg          1000000           35.6   (approx. NNLO)     
T_tbar     = creator.makeMCComponent('T_tbar'    , '/ST_t-channel_antitop_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM', 'CMS', '.*root',        80.95 ) #  Powheg          1630900           80.95  (NLO)    lep BR 0.108*3
T_t        = creator.makeMCComponent('T_t'       , '/ST_t-channel_top_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'    , 'CMS', '.*root',       136.02 ) #  Powheg          3299200          136.02  (NLO)    lep BR 0.108*3
TTInc_ext3 = creator.makeMCComponent('TTInc_ext3', '/TT_TuneCUETP8M1_13TeV-powheg-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext3-v1/MINIAODSIM'                             , 'CMS', '.*root',       831.76 ) #  Powheg         97994442          831.76  (NNLO)     
TTInc_ext4 = creator.makeMCComponent('TTInc_ext4', '/TT_TuneCUETP8M1_13TeV-powheg-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext4-v1/MINIAODSIM'                             , 'CMS', '.*root',       831.76 ) #  Powheg        187626200          831.76  (NNLO)     

single_top = [
    T_tbarW,
    T_tW   ,
    T_tbar ,
    T_t    ,
]

ttbar = [
    TTInc_ext3,
    TTInc_ext4,
]