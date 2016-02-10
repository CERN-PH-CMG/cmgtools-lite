import PhysicsTools.HeppyCore.framework.config as cfg

from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator

creator = ComponentCreator()

DYJetsToLL_M50_ext1 = creator.makeMCComponent('DYJetsToLL_M50_ext1', '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/MINIAODSIM', 'CMS', '.*root', 6025.2 )
DYJetsToLL_M50      = creator.makeMCComponent('DYJetsToLL_M50'     , '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'      , 'CMS', '.*root', 6025.2 )
DY1JetsToLL_M50     = creator.makeMCComponent('DY1JetsToLL_M50'    , '/DY1JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'     , 'CMS', '.*root', 1016   )
DY2JetsToLL_M50     = creator.makeMCComponent('DY2JetsToLL_M50'    , '/DY2JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'     , 'CMS', '.*root',  331.4 )
DY3JetsToLL_M50     = creator.makeMCComponent('DY3JetsToLL_M50'    , '/DY3JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'     , 'CMS', '.*root',   96.36)
DY4JetsToLL_M50     = creator.makeMCComponent('DY4JetsToLL_M50'    , '/DY4JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'     , 'CMS', '.*root',   51.4 )

DYJetsToLL_M50_HT_100to200 = creator.makeMCComponent('DYJetsToLL_M50_HT_100to200', '/DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM', 'CMS', '.*root', 147.4  )
DYJetsToLL_M50_HT_200to400 = creator.makeMCComponent('DYJetsToLL_M50_HT_200to400', '/DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM', 'CMS', '.*root',  40.99 )
DYJetsToLL_M50_HT_400to600 = creator.makeMCComponent('DYJetsToLL_M50_HT_400to600', '/DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM', 'CMS', '.*root',   5.678)
DYJetsToLL_M50_HT_600toInf = creator.makeMCComponent('DYJetsToLL_M50_HT_600toInf', '/DYJetsToLL_M-50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM', 'CMS', '.*root',   2.198)

DYJetsToLL_M10to50  = creator.makeMCComponent('DYJetsToLL_M10to50' , '/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM' , 'CMS', '.*root', 18610  )
DY1JetsToLL_M10to50 = creator.makeMCComponent('DY1JetsToLL_M10to50', '/DY1JetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM', 'CMS', '.*root',   421.5)
DY2JetsToLL_M10to50 = creator.makeMCComponent('DY2JetsToLL_M10to50', '/DY2JetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM', 'CMS', '.*root',   184.3)

dy_inclusive = [
    DYJetsToLL_M50_ext1,
    DYJetsToLL_M50      
]

dy_jet_bins = [
    DY1JetsToLL_M50,    
    DY2JetsToLL_M50,    
    DY3JetsToLL_M50,    
    DY4JetsToLL_M50,    
]

dy_ht_bins = [
    DYJetsToLL_M50_HT_100to200,
    DYJetsToLL_M50_HT_200to400,
    DYJetsToLL_M50_HT_400to600,
    DYJetsToLL_M50_HT_600toInf,
]

dy_low_mass = [
    DYJetsToLL_M10to50 ,
    DY1JetsToLL_M10to50,
    DY2JetsToLL_M10to50,
]

dy_all = dy_inclusive + dy_jet_bins + dy_ht_bins + dy_low_mass

WJetsToLNu             = creator.makeMCComponent('WJetsToLNu'            , '/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'           , 'CMS', '.*root', 61526.2 )
WJetsToLNu_HT_100to200 = creator.makeMCComponent('WJetsToLNu_HT_100to200', '/WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM', 'CMS', '.*root',  1345   )
WJetsToLNu_HT_200to400 = creator.makeMCComponent('WJetsToLNu_HT_200to400', '/WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM', 'CMS', '.*root',   359.7 )
WJetsToLNu_HT_400to600 = creator.makeMCComponent('WJetsToLNu_HT_400to600', '/WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM', 'CMS', '.*root',    48.91)
WJetsToLNu_HT_600toInf = creator.makeMCComponent('WJetsToLNu_HT_600toInf', '/WJetsToLNu_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM', 'CMS', '.*root',    18.77)

wjets_inclusive = [
    WJetsToLNu,
]

wjets_ht_bins = [
    WJetsToLNu_HT_100to200,
    WJetsToLNu_HT_200to400,
    WJetsToLNu_HT_400to600,
    WJetsToLNu_HT_600toInf,
]












