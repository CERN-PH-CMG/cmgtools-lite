# RIC: this file is  temporary solution to access data until the problem with 
#      imports from TTH that occurs when running in batch is not cleared out.
#      Create component only for 2015D Oct5 and 2015Dv4

import PhysicsTools.HeppyCore.framework.config as cfg

#####COMPONENT CREATOR

from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()

json = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/Cert_246908-260627_13TeV_PromptReco_Collisions15_25ns_JSON_v2.txt'

### ----------------------------- Run2015D-05Oct2015 ----------------------------------------
## https://hypernews.cern.ch/HyperNews/CMS/get/datasets/4154.html

SingleElectron_Run2015D_05Oct = kreator.makeDataComponent('SingleElectron_Run2015D_05Oct', '/SingleElectron/Run2015D-05Oct2015-v1/MINIAOD', 'CMS', '.*root', json)
SingleMuon_Run2015D_05Oct     = kreator.makeDataComponent('SingleMuon_Run2015D_05Oct'    , '/SingleMuon/Run2015D-05Oct2015-v1/MINIAOD'    , 'CMS', '.*root', json)
DoubleEG_Run2015D_05Oct       = kreator.makeDataComponent('DoubleEG_Run2015D_05Oct'      , '/DoubleEG/Run2015D-05Oct2015-v1/MINIAOD'      , 'CMS', '.*root', json)
MuonEG_Run2015D_05Oct         = kreator.makeDataComponent('MuonEG_Run2015D_05Oct'        , '/MuonEG/Run2015D-05Oct2015-v2/MINIAOD'        , 'CMS', '.*root', json)
DoubleMuon_Run2015D_05Oct     = kreator.makeDataComponent('DoubleMuon_Run2015D_05Oct'    , '/DoubleMuon/Run2015D-05Oct2015-v1/MINIAOD'    , 'CMS', '.*root', json)
Tau_Run2015D_05Oct            = kreator.makeDataComponent('Tau_Run2015D_05Oct'           , '/Tau/Run2015D-05Oct2015-v1/MINIAOD'           , 'CMS', '.*root', json)

### ----------------------------- Run2015D miniAODv2 ----------------------------------------
###https://hypernews.cern.ch/HyperNews/CMS/get/physics-announcements/3561.html

SingleElectron_Run2015D_Promptv4 = kreator.makeDataComponent('SingleElectron_Run2015D_v4', '/SingleElectron/Run2015D-PromptReco-v4/MINIAOD', 'CMS', '.*root', json)
SingleMuon_Run2015D_Promptv4     = kreator.makeDataComponent('SingleMuon_Run2015D_v4'    , '/SingleMuon/Run2015D-PromptReco-v4/MINIAOD'    , 'CMS', '.*root', json)
DoubleEG_Run2015D_Promptv4       = kreator.makeDataComponent('DoubleEG_Run2015D_v4'      , '/DoubleEG/Run2015D-PromptReco-v4/MINIAOD'      , 'CMS', '.*root', json)
MuonEG_Run2015D_Promptv4         = kreator.makeDataComponent('MuonEG_Run2015D_v4'        , '/MuonEG/Run2015D-PromptReco-v4/MINIAOD'        , 'CMS', '.*root', json)
DoubleMuon_Run2015D_Promptv4     = kreator.makeDataComponent('DoubleMuon_Run2015D_v4'    , '/DoubleMuon/Run2015D-PromptReco-v4/MINIAOD'    , 'CMS', '.*root', json)
Tau_Run2015D_Promptv4            = kreator.makeDataComponent('Tau_Run2015D_v4'           , '/Tau/Run2015D-PromptReco-v4/MINIAOD'           , 'CMS', '.*root', json)

###

data_single_muon     = [SingleMuon_Run2015D_05Oct    , SingleMuon_Run2015D_Promptv4    ]
data_single_electron = [SingleElectron_Run2015D_05Oct, SingleElectron_Run2015D_Promptv4]
data_muon_electron   = [MuonEG_Run2015D_05Oct        , MuonEG_Run2015D_Promptv4        ]
data_tau             = [Tau_Run2015D_05Oct           , Tau_Run2015D_Promptv4           ]

all_data = data_single_muon + data_single_electron + data_muon_electron + data_tau

for comp in all_data:
    comp.splitFactor = 1000
    comp.isMC = False
    comp.isData = True
