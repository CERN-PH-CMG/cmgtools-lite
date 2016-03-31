import PhysicsTools.HeppyCore.framework.config as cfg

from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator

creator = ComponentCreator()


DYJetsToLL_M50_NLO           = creator.makeMCComponent('DYJetsToLL_M50_NLO'           , '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'                  , 'CMS', '.*root',      6025.2  ) #  MG5_aMCNLO     28751199         6025.2   (NNLO)     
DYJetsToLL_M50_NLO_ext4      = creator.makeMCComponent('DYJetsToLL_M50_NLO_ext4'      , '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext4-v1/MINIAODSIM'             , 'CMS', '.*root',      6025.2  ) #  MG5_aMCNLO     28751199         6025.2   (NNLO)     
DYJetsToLL_M50_LO            = creator.makeMCComponent('DYJetsToLL_M50_LO'            , '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'                   , 'CMS', '.*root',      6025.2  ) #  LO_MG5          9004328         6025.2   (NNLO)     
DYJetsToLL_M50_LO_ext1       = creator.makeMCComponent('DYJetsToLL_M50_LO_ext1'       , '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/MINIAODSIM'              , 'CMS', '.*root',      6025.2  ) #  LO_MG5        247512446         6025.2   (NNLO)     

DY1JetsToLL_M50_LO           = creator.makeMCComponent('DY1JetsToLL_M50_LO'           , '/DY1JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'                  , 'CMS', '.*root',      1012.5  ) #  LO_MG5         65314144         1012.5   (from McM)     
DY2JetsToLL_M50_LO           = creator.makeMCComponent('DY2JetsToLL_M50_LO'           , '/DY2JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'                  , 'CMS', '.*root',       332.8  ) #  LO_MG5         20019059          332.8   (from McM)     
DY3JetsToLL_M50_LO           = creator.makeMCComponent('DY3JetsToLL_M50_LO'           , '/DY3JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'                  , 'CMS', '.*root',       101.8  ) #  LO_MG5          5701878          101.8   (from McM)     
DY4JetsToLL_M50_LO           = creator.makeMCComponent('DY4JetsToLL_M50_LO'           , '/DY4JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'                  , 'CMS', '.*root',        54.8  ) #  LO_MG5          4189017           54.8   (from McM)     

DYJetsToLL_M150_LO           = creator.makeMCComponent('DYJetsToLL_M150_LO'           , '/DYJetsToLL_M-150_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'                  , 'CMS', '.*root',         6.657) #  LO_MG5          6079415            6.657 (from McM)     

DYJetsToLL_M50_LO_HT100to200 = creator.makeMCComponent('DYJetsToLL_M50_LO_HT100to200' , '/DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'       , 'CMS', '.*root',       147.4  ) #  LO_MG5          2655294          147.4   (LO)    k-factor : 1.23
DYJetsToLL_M50_LO_HT200to400 = creator.makeMCComponent('DYJetsToLL_M50_LO_HT200to400' , '/DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'       , 'CMS', '.*root',        40.99 ) #  LO MG5           962195           40.99  (LO)    k-factor : 1.23
DYJetsToLL_M50_LO_HT400to600 = creator.makeMCComponent('DYJetsToLL_M50_LO_HT400to600' , '/DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'       , 'CMS', '.*root',         5.678) #  LO MG5          1069003            5.678 (LO)    k-factor : 1.23
DYJetsToLL_M50_LO_HT600toInf = creator.makeMCComponent('DYJetsToLL_M50_LO_HT600toInf' , '/DYJetsToLL_M-50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'       , 'CMS', '.*root',         2.198) #  LO MG5          1031103            2.198 (LO)    k-factor : 1.23

DYJetsToLL_M10to50_NLO       = creator.makeMCComponent('DYJetsToLL_M10to50_NLO'       , '/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'              , 'CMS', '.*root',     18610    ) #  MG5_aMCNLO     30899063        18610     (from McM)     
DYJetsToLL_M10to50_NLO_ext1  = creator.makeMCComponent('DYJetsToLL_M10to50_NLO_ext1'  , '/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/MINIAODSIM'         , 'CMS', '.*root',     18610    ) #  MG5_aMCNLO     62135699        18610     (from McM)     
DY1JetsToLL_M10to50_NLO      = creator.makeMCComponent('DY1JetsToLL_M10to50_NLO'      , '/DY1JetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'             , 'CMS', '.*root',       421.5  ) #  MG5_aMCNLO     15615590          421.5   (from McM)     
DY2JetsToLL_M10to50_NLO      = creator.makeMCComponent('DY2JetsToLL_M10to50_NLO'      , '/DY2JetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'             , 'CMS', '.*root',       184.3  ) #  MG5_aMCNLO     40473762          184.3   (from McM)     

DYJetsToTT_M50_NLO           = creator.makeMCComponent('DYJetsToTT_M50_NLO'           , '/DYJetsToTauTau_ForcedMuDecay_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM', 'CMS', '.*root',      1967    ) #  MG5_aMCNLO      1749048         1967     (from McM)     

dy_inclusive = [
    DYJetsToLL_M50_NLO,
    DYJetsToLL_M50_NLO_ext4,
    DYJetsToLL_M50_LO,
    DYJetsToLL_M50_LO_ext1,
]

dy_jet_bins = [
    DY1JetsToLL_M50_LO,    
    DY2JetsToLL_M50_LO,    
    DY3JetsToLL_M50_LO,    
    DY4JetsToLL_M50_LO,    
]

dy_high_mass = [
    DYJetsToLL_M150_LO,
]

dy_ht_bins = [
    DYJetsToLL_M50_LO_HT100to200,
    DYJetsToLL_M50_LO_HT200to400,
    DYJetsToLL_M50_LO_HT400to600,
    DYJetsToLL_M50_LO_HT600toInf,
]

dy_low_mass = [
    DYJetsToLL_M10to50_NLO     ,
    DYJetsToLL_M10to50_NLO_ext1,
    DY1JetsToLL_M10to50_NLO    ,
    DY2JetsToLL_M10to50_NLO    ,
]

dy_tt =[
    DYJetsToTT_M50_NLO,
]

dy_all = dy_inclusive + dy_jet_bins + dy_high_mass + dy_ht_bins + dy_low_mass + dy_tt

WJetsToLNu_LO                = creator.makeMCComponent('WJetsToLNu_LO'                , '/WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'                        , 'CMS', '.*root',     61526.7  ) #  LO MG5         47161328        61526.7   (NNLO)     
WJetsToLNu_NLO               = creator.makeMCComponent('WJetsToLNu_NLO'               , '/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'                       , 'CMS', '.*root',     61526.7  ) #  MG5_aMCNLO     24156124        61526.7   (NNLO)     

W1JetsToLNu_LO               = creator.makeMCComponent('W1JetsToLNu_LO'               , '/W1JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'                       , 'CMS', '.*root',      9493    ) #  LO MG5         45442170         9493     (McM)     
# W2JetsToLNu_LO               = creator.makeMCComponent('W2JetsToLNu_LO'               , '/W2JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'                       , 'CMS', '.*root',      ???    ) #  LO MG5         ???         ???     (McM)     
W3JetsToLNu_LO               = creator.makeMCComponent('W3JetsToLNu_LO'               , '/W3JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'                       , 'CMS', '.*root',       942.3  ) #  LO MG5         19141299          942.3   (McM)     
W4JetsToLNu_LO               = creator.makeMCComponent('W4JetsToLNu_LO'               , '/W4JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'                       , 'CMS', '.*root',       524.2  ) #  LO MG5          8995605          524.2   (McM)     

WJetsToLNu_LO_HT100to200     = creator.makeMCComponent('WJetsToLNu_LO_HT100to200'     , '/WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'            , 'CMS', '.*root',      1345    ) #  LO MG5         10205377         1345     (LO)     
WJetsToLNu_LO_HT200to400     = creator.makeMCComponent('WJetsToLNu_LO_HT200to400'     , '/WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'            , 'CMS', '.*root',       359.7  ) #  LO MG5          4949568          359.7   (LO)     
WJetsToLNu_LO_HT400to600     = creator.makeMCComponent('WJetsToLNu_LO_HT400to600'     , '/WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'            , 'CMS', '.*root',        48.91 ) #  LO MG5          1943664           48.91  (LO)     
WJetsToLNu_LO_HT600toInf     = creator.makeMCComponent('WJetsToLNu_LO_HT600toInf'     , '/WJetsToLNu_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'            , 'CMS', '.*root',        18.77 ) #  LO MG5          1041358           18.77  (LO)     

wjets_inclusive = [
    WJetsToLNu_LO,
    WJetsToLNu_NLO, 
]

wjets_jet_bins = [
    W1JetsToLNu_LO,
    # W2JetsToLNu_LO,
    W3JetsToLNu_LO,
    W4JetsToLNu_LO,
]

wjets_ht_bins = [
    WJetsToLNu_LO_HT100to200,
    WJetsToLNu_LO_HT200to400,
    WJetsToLNu_LO_HT400to600,
    WJetsToLNu_LO_HT600toInf,
]

wjets_all = wjets_inclusive + wjets_jet_bins + wjets_ht_bins

EWKWMinus2Jets_WToLNu        = creator.makeMCComponent('EWKWMinus2Jets_WToLNu'        , '/EWKWMinus2Jets_WToLNu_M-50_13TeV-madgraph-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'                        , 'CMS', '.*root',        20.25 ) #  LO_MG5           490005           20.25  (from McM)     
EWKWPlus2Jets_WToLNu         = creator.makeMCComponent('EWKWPlus2Jets_WToLNu'         , '/EWKWPlus2Jets_WToLNu_M-50_13TeV-madgraph-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'                         , 'CMS', '.*root',        25.62 ) #  LO_MG5           500000           25.62  (from McM)     
EWKZ2Jets_ZToLL_M50          = creator.makeMCComponent('EWKZ2Jets_ZToLL_M50'          , '/EWKZ2Jets_ZToLL_M-50_13TeV-madgraph-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'                              , 'CMS', '.*root',         3.987) #  LO_MG5           150000            3.987 (from McM)     
EWKZ2Jets_ZToNuNu            = creator.makeMCComponent('EWKZ2Jets_ZToNuNu'            , '/EWKZ2Jets_ZToNuNu_13TeV-madgraph-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v2/MINIAODSIM'                                 , 'CMS', '.*root',        10.01 ) #  LO_MG5           298400           10.01  (from McM)

ewk_others = [
    EWKWMinus2Jets_WToLNu,
    EWKWPlus2Jets_WToLNu,
    EWKZ2Jets_ZToLL_M50,
    EWKZ2Jets_ZToNuNu,
]



ewk_all = dy_all + wjets_all + ewk_others



