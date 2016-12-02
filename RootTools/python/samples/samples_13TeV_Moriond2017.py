import PhysicsTools.HeppyCore.framework.config as cfg
import os

#####COMPONENT CREATOR

from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()

dataDir = "$CMSSW_BASE/src/CMGTools/TTHAnalysis/data"  # use environmental variable, useful for instance to run on CRAB
json=dataDir+'/json/Cert_271036-283685_13TeV_PromptReco_Collisions16_JSON_NoL1T.txt'

json_F=dataDir+'/json/json_DCSONLY_2016_08_10_F.txt' #only RunF
#https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions16/13TeV/
#https://hypernews.cern.ch/HyperNews/CMS/get/physics-validation/2657.html
#with recorded luminosity: 804.2/pb

json =dataDir+'/json/Cert_271036-284044_13TeV_PromptReco_Collisions16_JSON_NoL1T.txt' # Golden Json

#jetHT_0T = cfg.DataComponent(
#    name = 'jetHT_0T',
#    files = kreator.getFilesFromEOS('jetHT_0T',
#                                    'firstData_JetHT_v2',
#                                    '/store/user/pandolf/MINIAOD/%s'),
#    intLumi = 4.0,
#    triggers = [],
#    json = None #json
#    )


#run_range = (271036, 284044)
#label = "_runs%s_%s"%(run_range[0], run_range[1])

###Need to be check for run ranges

#### ----------------------------- Run2016B 23Sep2016 additionals ----------------------------------------

JetHT_Run2016B_23Sep2016_v1          = kreator.makeDataComponent("JetHT_Run2016B_23Sep2016_v1"         , "/JetHT/Run2016B-23Sep2016-v1/MINIAOD"         , "CMS", ".*root", json)
HTMHT_Run2016B_23Sep2016_v1          = kreator.makeDataComponent("HTMHT_Run2016B_23Sep2016_v1"         , "/HTMHT/Run2016B-23Sep2016-v1/MINIAOD"         , "CMS", ".*root", json)
MET_Run2016B_23Sep2016_v2            = kreator.makeDataComponent("MET_Run2016B_23Sep2016_v2"           , "/MET/Run2016B-23Sep2016-v2/MINIAOD"           , "CMS", ".*root", json)
SingleElectron_Run2016B_23Sep2016_v2 = kreator.makeDataComponent("SingleElectron_Run2016B_23Sep2016_v2", "/SingleElectron/Run2016B-23Sep2016-v2/MINIAOD", "CMS", ".*root", json)
SingleMuon_Run2016B_23Sep2016_v1     = kreator.makeDataComponent("SingleMuon_Run2016B_23Sep2016_v1"    , "/SingleMuon/Run2016B-23Sep2016-v1/MINIAOD"    , "CMS", ".*root", json)
SinglePhoton_Run2016B_23Sep2016_v1   = kreator.makeDataComponent("SinglePhoton_Run2016B_23Sep2016_v1"  , "/SinglePhoton/Run2016B-23Sep2016-v1/MINIAOD"  , "CMS", ".*root", json)
DoubleEG_Run2016B_23Sep2016_v2       = kreator.makeDataComponent("DoubleEG_Run2016B_23Sep2016_v2"      , "/DoubleEG/Run2016B-23Sep2016-v2/MINIAOD"      , "CMS", ".*root", json)
MuonEG_Run2016B_23Sep2016_v2        = kreator.makeDataComponent("MuonEG_Run2016B_23Sep2016_v2"        , "/MuonEG/Run2016B-23Sep2016-v2/MINIAOD"        , "CMS", ".*root", json)
DoubleMuon_Run2016B_23Sep2016_v1     = kreator.makeDataComponent("DoubleMuon_Run2016B_23Sep2016_v1"    , "/DoubleMuon/Run2016B-23Sep2016-v1/MINIAOD"    , "CMS", ".*root", json)
Tau_Run2016B_23Sep2016_v1     = kreator.makeDataComponent("Tau_Run2016B_23Sep2016_v1"    , "/Tau/Run2016B-23Sep2016-v1/MINIAOD"    , "CMS", ".*root", json)

dataSamples_Run2016B_add = [JetHT_Run2016B_23Sep2016_v1, HTMHT_Run2016B_23Sep2016_v1, MET_Run2016B_23Sep2016_v2, SingleElectron_Run2016B_23Sep2016_v2,\
 SingleMuon_Run2016B_23Sep2016_v1, SinglePhoton_Run2016B_23Sep2016_v1, DoubleEG_Run2016B_23Sep2016_v2, MuonEG_Run2016B_23Sep2016_v2,\
 DoubleMuon_Run2016B_23Sep2016_v1, Tau_Run2016B_23Sep2016_v1]

### ----------------------------- Run2016B 23Sep2016 v3 ----------------------------------------

JetHT_Run2016B_23Sep2016          = kreator.makeDataComponent("JetHT_Run2016B_23Sep2016"         , "/JetHT/Run2016B-23Sep2016-v3/MINIAOD"         , "CMS", ".*root", json)
HTMHT_Run2016B_23Sep2016          = kreator.makeDataComponent("HTMHT_Run2016B_23Sep2016"         , "/HTMHT/Run2016B-23Sep2016-v3/MINIAOD"         , "CMS", ".*root", json)
MET_Run2016B_23Sep2016            = kreator.makeDataComponent("MET_Run2016B_23Sep2016"           , "/MET/Run2016B-23Sep2016-v3/MINIAOD"           , "CMS", ".*root", json)
SingleElectron_Run2016B_23Sep2016 = kreator.makeDataComponent("SingleElectron_Run2016B_23Sep2016", "/SingleElectron/Run2016B-23Sep2016-v3/MINIAOD", "CMS", ".*root", json)
SingleMuon_Run2016B_23Sep2016     = kreator.makeDataComponent("SingleMuon_Run2016B_23Sep2016"    , "/SingleMuon/Run2016B-23Sep2016-v3/MINIAOD"    , "CMS", ".*root", json)
SinglePhoton_Run2016B_23Sep2016   = kreator.makeDataComponent("SinglePhoton_Run2016B_23Sep2016"  , "/SinglePhoton/Run2016B-23Sep2016-v3/MINIAOD"  , "CMS", ".*root", json)
DoubleEG_Run2016B_23Sep2016       = kreator.makeDataComponent("DoubleEG_Run2016B_23Sep2016"      , "/DoubleEG/Run2016B-23Sep2016-v3/MINIAOD"      , "CMS", ".*root", json)
MuonEG_Run2016B_23Sep2016         = kreator.makeDataComponent("MuonEG_Run2016B_23Sep2016"       , "/MuonEG/Run2016B-23Sep2016-v3/MINIAOD"        , "CMS", ".*root", json)
DoubleMuon_Run2016B_23Sep2016     = kreator.makeDataComponent("DoubleMuon_Run2016B_23Sep2016"    , "/DoubleMuon/Run2016B-23Sep2016-v3/MINIAOD"    , "CMS", ".*root", json)
Tau_Run2016B_23Sep2016     = kreator.makeDataComponent("Tau_Run2016B_23Sep2016"    , "/Tau/Run2016B-23Sep2016-v3/MINIAOD"    , "CMS", ".*root", json)

dataSamples_Run2016B_v3 = [JetHT_Run2016B_23Sep2016, HTMHT_Run2016B_23Sep2016, MET_Run2016B_23Sep2016, SingleElectron_Run2016B_23Sep2016, SingleMuon_Run2016B_23Sep2016, SinglePhoton_Run2016B_23Sep2016, DoubleEG_Run2016B_23Sep2016, MuonEG_Run2016B_23Sep2016, DoubleMuon_Run2016B_23Sep2016, Tau_Run2016B_23Sep2016]

### ----------------------------- Run2016C 23Sep2016 v1 ----------------------------------------

JetHT_Run2016C_23Sep2016_v1          = kreator.makeDataComponent("JetHT_Run2016C_23Sep2016_v1"         , "/JetHT/Run2016C-23Sep2016-v1/MINIAOD"         , "CMS", ".*root", json)
HTMHT_Run2016C_23Sep2016_v1          = kreator.makeDataComponent("HTMHT_Run2016C_23Sep2016_v1"         , "/HTMHT/Run2016C-23Sep2016-v1/MINIAOD"         , "CMS", ".*root", json)
MET_Run2016C_23Sep2016_v1            = kreator.makeDataComponent("MET_Run2016C_23Sep2016_v1"           , "/MET/Run2016C-23Sep2016-v1/MINIAOD"           , "CMS", ".*root", json)
SingleElectron_Run2016C_23Sep2016_v1 = kreator.makeDataComponent("SingleElectron_Run2016C_23Sep2016_v1", "/SingleElectron/Run2016C-23Sep2016-v1/MINIAOD", "CMS", ".*root", json)
SingleMuon_Run2016C_23Sep2016_v1     = kreator.makeDataComponent("SingleMuon_Run2016C_23Sep2016_v1"    , "/SingleMuon/Run2016C-23Sep2016-v1/MINIAOD"    , "CMS", ".*root", json)
SinglePhoton_Run2016C_23Sep2016_v1   = kreator.makeDataComponent("SinglePhoton_Run2016C_23Sep2016_v1"  , "/SinglePhoton/Run2016C-23Sep2016-v1/MINIAOD"  , "CMS", ".*root", json)
DoubleEG_Run2016C_23Sep2016_v1       = kreator.makeDataComponent("DoubleEG_Run2016C_23Sep2016_v1"      , "/DoubleEG/Run2016C-23Sep2016-v1/MINIAOD"      , "CMS", ".*root", json)
MuonEG_Run2016C_23Sep2016_v1         = kreator.makeDataComponent("MuonEG_Run2016C_23Sep2016_v1"        , "/MuonEG/Run2016C-23Sep2016-v1/MINIAOD"        , "CMS", ".*root", json)
DoubleMuon_Run2016C_23Sep2016_v1     = kreator.makeDataComponent("DoubleMuon_Run2016C_23Sep2016_v1"    , "/DoubleMuon/Run2016C-23Sep2016-v1/MINIAOD"    , "CMS", ".*root", json)
Tau_Run2016C_23Sep2016_v1            = kreator.makeDataComponent("Tau_Run2016C_23Sep2016_v1"           , "/Tau/Run2016C-23Sep2016-v1/MINIAOD"           , "CMS", ".*root", json)

dataSamples_Run2016C_v1 = [JetHT_Run2016C_23Sep2016_v1, HTMHT_Run2016C_23Sep2016_v1, MET_Run2016C_23Sep2016_v1, SingleElectron_Run2016C_23Sep2016_v1, SingleMuon_Run2016C_23Sep2016_v1, SinglePhoton_Run2016C_23Sep2016_v1, DoubleEG_Run2016C_23Sep2016_v1, MuonEG_Run2016C_23Sep2016_v1, DoubleMuon_Run2016C_23Sep2016_v1, Tau_Run2016C_23Sep2016_v1]


### ----------------------------- Run2016D 23Sep2016 v1 ----------------------------------------

JetHT_Run2016D_23Sep2016_v1          = kreator.makeDataComponent("JetHT_Run2016D_23Sep2016_v1"         , "/JetHT/Run2016D-23Sep2016-v1/MINIAOD"         , "CMS", ".*root", json)
HTMHT_Run2016D_23Sep2016_v1          = kreator.makeDataComponent("HTMHT_Run2016D_23Sep2016_v1"         , "/HTMHT/Run2016D-23Sep2016-v1/MINIAOD"         , "CMS", ".*root", json)
MET_Run2016D_23Sep2016_v1            = kreator.makeDataComponent("MET_Run2016D_23Sep2016_v1"           , "/MET/Run2016D-23Sep2016-v1/MINIAOD"           , "CMS", ".*root", json)
SingleElectron_Run2016D_23Sep2016_v1 = kreator.makeDataComponent("SingleElectron_Run2016D_23Sep2016_v1", "/SingleElectron/Run2016D-23Sep2016-v1/MINIAOD", "CMS", ".*root", json)
SingleMuon_Run2016D_23Sep2016_v1     = kreator.makeDataComponent("SingleMuon_Run2016D_23Sep2016_v1"    , "/SingleMuon/Run2016D-23Sep2016-v1/MINIAOD"    , "CMS", ".*root", json)
SinglePhoton_Run2016D_23Sep2016_v1   = kreator.makeDataComponent("SinglePhoton_Run2016D_23Sep2016_v1"  , "/SinglePhoton/Run2016D-23Sep2016-v1/MINIAOD"  , "CMS", ".*root", json)
DoubleEG_Run2016D_23Sep2016_v1       = kreator.makeDataComponent("DoubleEG_Run2016D_23Sep2016_v1"      , "/DoubleEG/Run2016D-23Sep2016-v1/MINIAOD"      , "CMS", ".*root", json)
MuonEG_Run2016D_23Sep2016_v1         = kreator.makeDataComponent("MuonEG_Run2016D_23Sep2016_v1"        , "/MuonEG/Run2016D-23Sep2016-v1/MINIAOD"        , "CMS", ".*root", json)
DoubleMuon_Run2016D_23Sep2016_v1     = kreator.makeDataComponent("DoubleMuon_Run2016D_23Sep2016_v1"    , "/DoubleMuon/Run2016D-23Sep2016-v1/MINIAOD"    , "CMS", ".*root", json)
Tau_Run2016D_23Sep2016_v1            = kreator.makeDataComponent("Tau_Run2016D_23Sep2016_v1"           , "/Tau/Run2016D-23Sep2016-v1/MINIAOD"           , "CMS", ".*root", json)

dataSamples_Run2016D_v1 = [JetHT_Run2016D_23Sep2016_v1, HTMHT_Run2016D_23Sep2016_v1, MET_Run2016D_23Sep2016_v1, SingleElectron_Run2016D_23Sep2016_v1, SingleMuon_Run2016D_23Sep2016_v1, SinglePhoton_Run2016D_23Sep2016_v1, DoubleEG_Run2016D_23Sep2016_v1, MuonEG_Run2016D_23Sep2016_v1, DoubleMuon_Run2016D_23Sep2016_v1, Tau_Run2016D_23Sep2016_v1]

### ----------------------------- Run2016E 23Sep2016 v1 ----------------------------------------

JetHT_Run2016E_23Sep2016_v1          = kreator.makeDataComponent("JetHT_Run2016E_23Sep2016_v1"         , "/JetHT/Run2016E-23Sep2016-v1/MINIAOD"         , "CMS", ".*root", json)
HTMHT_Run2016E_23Sep2016_v1          = kreator.makeDataComponent("HTMHT_Run2016E_23Sep2016_v1"         , "/HTMHT/Run2016E-23Sep2016-v1/MINIAOD"         , "CMS", ".*root", json)
MET_Run2016E_23Sep2016_v1            = kreator.makeDataComponent("MET_Run2016E_23Sep2016_v1"           , "/MET/Run2016E-23Sep2016-v1/MINIAOD"           , "CMS", ".*root", json)
SingleElectron_Run2016E_23Sep2016_v1 = kreator.makeDataComponent("SingleElectron_Run2016E_23Sep2016_v1", "/SingleElectron/Run2016E-23Sep2016-v1/MINIAOD", "CMS", ".*root", json)
SingleMuon_Run2016E_23Sep2016_v1     = kreator.makeDataComponent("SingleMuon_Run2016E_23Sep2016_v1"    , "/SingleMuon/Run2016E-23Sep2016-v1/MINIAOD"    , "CMS", ".*root", json)
SinglePhoton_Run2016E_23Sep2016_v1   = kreator.makeDataComponent("SinglePhoton_Run2016E_23Sep2016_v1"  , "/SinglePhoton/Run2016E-23Sep2016-v1/MINIAOD"  , "CMS", ".*root", json)
DoubleEG_Run2016E_23Sep2016_v1       = kreator.makeDataComponent("DoubleEG_Run2016E_23Sep2016_v1"      , "/DoubleEG/Run2016E-23Sep2016-v1/MINIAOD"      , "CMS", ".*root", json)
MuonEG_Run2016E_23Sep2016_v1         = kreator.makeDataComponent("MuonEG_Run2016E_23Sep2016_v1"        , "/MuonEG/Run2016E-23Sep2016-v1/MINIAOD"        , "CMS", ".*root", json)
DoubleMuon_Run2016E_23Sep2016_v1     = kreator.makeDataComponent("DoubleMuon_Run2016E_23Sep2016_v1"    , "/DoubleMuon/Run2016E-23Sep2016-v1/MINIAOD"    , "CMS", ".*root", json)
Tau_Run2016E_23Sep2016_v1            = kreator.makeDataComponent("Tau_Run2016E_23Sep2016_v1"           , "/Tau/Run2016E-23Sep2016-v1/MINIAOD"           , "CMS", ".*root", json)

dataSamples_Run2016E_v1 = [JetHT_Run2016E_23Sep2016_v1, HTMHT_Run2016E_23Sep2016_v1, MET_Run2016E_23Sep2016_v1, SingleElectron_Run2016E_23Sep2016_v1, SingleMuon_Run2016E_23Sep2016_v1, SinglePhoton_Run2016E_23Sep2016_v1, DoubleEG_Run2016E_23Sep2016_v1, MuonEG_Run2016E_23Sep2016_v1, DoubleMuon_Run2016E_23Sep2016_v1, Tau_Run2016E_23Sep2016_v1]


### ----------------------------- Run2016F 23Sep2016 v1 ----------------------------------------

JetHT_Run2016F_23Sep2016_v1          = kreator.makeDataComponent("JetHT_Run2016F_23Sep2016_v1"         , "/JetHT/Run2016F-23Sep2016-v1/MINIAOD"         , "CMS", ".*root", json)
HTMHT_Run2016F_23Sep2016_v1          = kreator.makeDataComponent("HTMHT_Run2016F_23Sep2016_v1"         , "/HTMHT/Run2016F-23Sep2016-v1/MINIAOD"         , "CMS", ".*root", json)
MET_Run2016F_23Sep2016_v1            = kreator.makeDataComponent("MET_Run2016F_23Sep2016_v1"           , "/MET/Run2016F-23Sep2016-v1/MINIAOD"           , "CMS", ".*root", json)
SingleElectron_Run2016F_23Sep2016_v1 = kreator.makeDataComponent("SingleElectron_Run2016F_23Sep2016_v1", "/SingleElectron/Run2016F-23Sep2016-v1/MINIAOD", "CMS", ".*root", json)
SingleMuon_Run2016F_23Sep2016_v1     = kreator.makeDataComponent("SingleMuon_Run2016F_23Sep2016_v1"    , "/SingleMuon/Run2016F-23Sep2016-v1/MINIAOD"    , "CMS", ".*root", json)
SinglePhoton_Run2016F_23Sep2016_v1   = kreator.makeDataComponent("SinglePhoton_Run2016F_23Sep2016_v1"  , "/SinglePhoton/Run2016F-23Sep2016-v1/MINIAOD"  , "CMS", ".*root", json)
DoubleEG_Run2016F_23Sep2016_v1       = kreator.makeDataComponent("DoubleEG_Run2016F_23Sep2016_v1"      , "/DoubleEG/Run2016F-23Sep2016-v1/MINIAOD"      , "CMS", ".*root", json)
MuonEG_Run2016F_23Sep2016_v1         = kreator.makeDataComponent("MuonEG_Run2016F_23Sep2016_v1"        , "/MuonEG/Run2016F-23Sep2016-v1/MINIAOD"        , "CMS", ".*root", json)
DoubleMuon_Run2016F_23Sep2016_v1     = kreator.makeDataComponent("DoubleMuon_Run2016F_23Sep2016_v1"    , "/DoubleMuon/Run2016F-23Sep2016-v1/MINIAOD"    , "CMS", ".*root", json)
Tau_Run2016F_23Sep2016_v1            = kreator.makeDataComponent("Tau_Run2016F_23Sep2016_v1"           , "/Tau/Run2016F-23Sep2016-v1/MINIAOD"           , "CMS", ".*root", json)

dataSamples_Run2016F_v1 = [JetHT_Run2016F_23Sep2016_v1, HTMHT_Run2016F_23Sep2016_v1, MET_Run2016F_23Sep2016_v1, SingleElectron_Run2016F_23Sep2016_v1, SingleMuon_Run2016F_23Sep2016_v1, SinglePhoton_Run2016F_23Sep2016_v1, DoubleEG_Run2016F_23Sep2016_v1, MuonEG_Run2016F_23Sep2016_v1, DoubleMuon_Run2016F_23Sep2016_v1, Tau_Run2016F_23Sep2016_v1]


### ----------------------------- Run2016G 23Sep2016 ----------------------------------------

JetHT_Run2016G_23Sep2016_v1          = kreator.makeDataComponent("JetHT_Run2016G_23Sep2016_v1"         , "/JetHT/Run2016G-23Sep2016-v1/MINIAOD"         , "CMS", ".*root", json)
HTMHT_Run2016G_23Sep2016_v2          = kreator.makeDataComponent("HTMHT_Run2016G_23Sep2016_v2"         , "/HTMHT/Run2016G-23Sep2016-v2/MINIAOD"         , "CMS", ".*root", json)
MET_Run2016G_23Sep2016_v1            = kreator.makeDataComponent("MET_Run2016G_23Sep2016_v1"           , "/MET/Run2016G-23Sep2016-v1/MINIAOD"           , "CMS", ".*root", json)
SingleElectron_Run2016G_23Sep2016_v1 = kreator.makeDataComponent("SingleElectron_Run2016G_23Sep2016_v1", "/SingleElectron/Run2016G-23Sep2016-v1/MINIAOD", "CMS", ".*root", json)
SingleMuon_Run2016G_23Sep2016_v1     = kreator.makeDataComponent("SingleMuon_Run2016G_23Sep2016_v1"    , "/SingleMuon/Run2016G-23Sep2016-v1/MINIAOD"    , "CMS", ".*root", json)
SinglePhoton_Run2016G_23Sep2016_v1   = kreator.makeDataComponent("SinglePhoton_Run2016G_23Sep2016_v1"  , "/SinglePhoton/Run2016G-23Sep2016-v1/MINIAOD"  , "CMS", ".*root", json)
DoubleEG_Run2016G_23Sep2016_v1       = kreator.makeDataComponent("DoubleEG_Run2016G_23Sep2016_v1"      , "/DoubleEG/Run2016G-23Sep2016-v1/MINIAOD"      , "CMS", ".*root", json)
MuonEG_Run2016G_23Sep2016_v1        = kreator.makeDataComponent("MuonEG_Run2016G_23Sep2016_v1"        , "/MuonEG/Run2016G-23Sep2016-v1/MINIAOD"        , "CMS", ".*root", json)
DoubleMuon_Run2016G_23Sep2016_v1     = kreator.makeDataComponent("DoubleMuon_Run2016G_23Sep2016_v1"    , "/DoubleMuon/Run2016G-23Sep2016-v1/MINIAOD"    , "CMS", ".*root", json)
Tau_Run2016G_23Sep2016_v1     = kreator.makeDataComponent("Tau_Run2016G_23Sep2016_v1"    , "/Tau/Run2016G-23Sep2016-v1/MINIAOD"    , "CMS", ".*root", json)

dataSamples_Run2016G = [JetHT_Run2016G_23Sep2016_v1, HTMHT_Run2016G_23Sep2016_v2, MET_Run2016G_23Sep2016_v1, SingleElectron_Run2016G_23Sep2016_v1, SingleMuon_Run2016G_23Sep2016_v1, SinglePhoton_Run2016G_23Sep2016_v1, DoubleEG_Run2016G_23Sep2016_v1, MuonEG_Run2016G_23Sep2016_v1, DoubleMuon_Run2016G_23Sep2016_v1, Tau_Run2016G_23Sep2016_v1]


### ----------------------------- Run2016H PromptReco v1 ----------------------------------------

JetHT_Run2016H_PromptReco_v1          = kreator.makeDataComponent("JetHT_Run2016H_PromptReco_v1"         , "/JetHT/Run2016H-PromptReco-v1/MINIAOD"         , "CMS", ".*root", json)
HTMHT_Run2016H_PromptReco_v1          = kreator.makeDataComponent("HTMHT_Run2016H_PromptReco_v1"         , "/HTMHT/Run2016H-PromptReco-v1/MINIAOD"         , "CMS", ".*root", json)
MET_Run2016H_PromptReco_v1            = kreator.makeDataComponent("MET_Run2016H_PromptReco_v1"           , "/MET/Run2016H-PromptReco-v1/MINIAOD"           , "CMS", ".*root", json)
SingleElectron_Run2016H_PromptReco_v1 = kreator.makeDataComponent("SingleElectron_Run2016H_PromptReco_v1", "/SingleElectron/Run2016H-PromptReco-v1/MINIAOD", "CMS", ".*root", json)
SingleMuon_Run2016H_PromptReco_v1     = kreator.makeDataComponent("SingleMuon_Run2016H_PromptReco_v1"    , "/SingleMuon/Run2016H-PromptReco-v1/MINIAOD"    , "CMS", ".*root", json)
SinglePhoton_Run2016H_PromptReco_v1   = kreator.makeDataComponent("SinglePhoton_Run2016H_PromptReco_v1"  , "/SinglePhoton/Run2016H-PromptReco-v1/MINIAOD"  , "CMS", ".*root", json)
DoubleEG_Run2016H_PromptReco_v1       = kreator.makeDataComponent("DoubleEG_Run2016H_PromptReco_v1"      , "/DoubleEG/Run2016H-PromptReco-v1/MINIAOD"      , "CMS", ".*root", json)
MuonEG_Run2016H_PromptReco_v1        = kreator.makeDataComponent("MuonEG_Run2016H_PromptReco_v1"        , "/MuonEG/Run2016H-PromptReco-v1/MINIAOD"        , "CMS", ".*root", json)
DoubleMuon_Run2016H_PromptReco_v1     = kreator.makeDataComponent("DoubleMuon_Run2016H_PromptReco_v1"    , "/DoubleMuon/Run2016H-PromptReco-v1/MINIAOD"    , "CMS", ".*root", json)
Tau_Run2016H_PromptReco_v1     = kreator.makeDataComponent("Tau_Run2016H_PromptReco_v1"    , "/Tau/Run2016H-PromptReco-v1/MINIAOD"    , "CMS", ".*root", json)

dataSamples_Run2016H_v1 = [JetHT_Run2016H_PromptReco_v1, HTMHT_Run2016H_PromptReco_v1, MET_Run2016H_PromptReco_v1, SingleElectron_Run2016H_PromptReco_v1, SingleMuon_Run2016H_PromptReco_v1, SinglePhoton_Run2016H_PromptReco_v1, DoubleEG_Run2016H_PromptReco_v1, MuonEG_Run2016H_PromptReco_v1, DoubleMuon_Run2016H_PromptReco_v1, Tau_Run2016H_PromptReco_v1]

### ----------------------------- Run2016H PromptReco v2 ----------------------------------------

JetHT_Run2016H_PromptReco_v2          = kreator.makeDataComponent("JetHT_Run2016H_PromptReco_v2"         , "/JetHT/Run2016H-PromptReco-v2/MINIAOD"         , "CMS", ".*root", json)
HTMHT_Run2016H_PromptReco_v2          = kreator.makeDataComponent("HTMHT_Run2016H_PromptReco_v2"         , "/HTMHT/Run2016H-PromptReco-v2/MINIAOD"         , "CMS", ".*root", json)
MET_Run2016H_PromptReco_v2            = kreator.makeDataComponent("MET_Run2016H_PromptReco_v2"           , "/MET/Run2016H-PromptReco-v2/MINIAOD"           , "CMS", ".*root", json)
SingleElectron_Run2016H_PromptReco_v2 = kreator.makeDataComponent("SingleElectron_Run2016H_PromptReco_v2", "/SingleElectron/Run2016H-PromptReco-v2/MINIAOD", "CMS", ".*root", json)
SingleMuon_Run2016H_PromptReco_v2     = kreator.makeDataComponent("SingleMuon_Run2016H_PromptReco_v2"    , "/SingleMuon/Run2016H-PromptReco-v2/MINIAOD"    , "CMS", ".*root", json)
SinglePhoton_Run2016H_PromptReco_v2   = kreator.makeDataComponent("SinglePhoton_Run2016H_PromptReco_v2"  , "/SinglePhoton/Run2016H-PromptReco-v2/MINIAOD"  , "CMS", ".*root", json)
DoubleEG_Run2016H_PromptReco_v2       = kreator.makeDataComponent("DoubleEG_Run2016H_PromptReco_v2"      , "/DoubleEG/Run2016H-PromptReco-v2/MINIAOD"      , "CMS", ".*root", json)
MuonEG_Run2016H_PromptReco_v2        = kreator.makeDataComponent("MuonEG_Run2016H_PromptReco_v2"        , "/MuonEG/Run2016H-PromptReco-v2/MINIAOD"        , "CMS", ".*root", json)
DoubleMuon_Run2016H_PromptReco_v2     = kreator.makeDataComponent("DoubleMuon_Run2016H_PromptReco_v2"    , "/DoubleMuon/Run2016H-PromptReco-v2/MINIAOD"    , "CMS", ".*root", json)
Tau_Run2016H_PromptReco_v2     = kreator.makeDataComponent("Tau_Run2016H_PromptReco_v2"    , "/Tau/Run2016H-PromptReco-v2/MINIAOD"    , "CMS", ".*root", json)

dataSamples_Run2016H_v2 = [JetHT_Run2016H_PromptReco_v2, HTMHT_Run2016H_PromptReco_v2, MET_Run2016H_PromptReco_v2, SingleElectron_Run2016H_PromptReco_v2, SingleMuon_Run2016H_PromptReco_v2, SinglePhoton_Run2016H_PromptReco_v2, DoubleEG_Run2016H_PromptReco_v2, MuonEG_Run2016H_PromptReco_v2, DoubleMuon_Run2016H_PromptReco_v2, Tau_Run2016H_PromptReco_v2]

### ----------------------------- Run2016H PromptReco v3 ----------------------------------------

JetHT_Run2016H_PromptReco_v3          = kreator.makeDataComponent("JetHT_Run2016H_PromptReco_v3"         , "/JetHT/Run2016H-PromptReco-v3/MINIAOD"         , "CMS", ".*root", json)
HTMHT_Run2016H_PromptReco_v3          = kreator.makeDataComponent("HTMHT_Run2016H_PromptReco_v3"         , "/HTMHT/Run2016H-PromptReco-v3/MINIAOD"         , "CMS", ".*root", json)
MET_Run2016H_PromptReco_v3            = kreator.makeDataComponent("MET_Run2016H_PromptReco_v3"           , "/MET/Run2016H-PromptReco-v3/MINIAOD"           , "CMS", ".*root", json)
SingleElectron_Run2016H_PromptReco_v3 = kreator.makeDataComponent("SingleElectron_Run2016H_PromptReco_v3", "/SingleElectron/Run2016H-PromptReco-v3/MINIAOD", "CMS", ".*root", json)
SingleMuon_Run2016H_PromptReco_v3     = kreator.makeDataComponent("SingleMuon_Run2016H_PromptReco_v3"    , "/SingleMuon/Run2016H-PromptReco-v3/MINIAOD"    , "CMS", ".*root", json)
SinglePhoton_Run2016H_PromptReco_v3   = kreator.makeDataComponent("SinglePhoton_Run2016H_PromptReco_v3"  , "/SinglePhoton/Run2016H-PromptReco-v3/MINIAOD"  , "CMS", ".*root", json)
DoubleEG_Run2016H_PromptReco_v3       = kreator.makeDataComponent("DoubleEG_Run2016H_PromptReco_v3"      , "/DoubleEG/Run2016H-PromptReco-v3/MINIAOD"      , "CMS", ".*root", json)
MuonEG_Run2016H_PromptReco_v3        = kreator.makeDataComponent("MuonEG_Run2016H_PromptReco_v3"        , "/MuonEG/Run2016H-PromptReco-v3/MINIAOD"        , "CMS", ".*root", json)
DoubleMuon_Run2016H_PromptReco_v3     = kreator.makeDataComponent("DoubleMuon_Run2016H_PromptReco_v3"    , "/DoubleMuon/Run2016H-PromptReco-v3/MINIAOD"    , "CMS", ".*root", json)
Tau_Run2016H_PromptReco_v3     = kreator.makeDataComponent("Tau_Run2016H_PromptReco_v3"    , "/Tau/Run2016H-PromptReco-v3/MINIAOD"    , "CMS", ".*root", json)

dataSamples_Run2016H_v3 = [JetHT_Run2016H_PromptReco_v3, HTMHT_Run2016H_PromptReco_v3, MET_Run2016H_PromptReco_v3, SingleElectron_Run2016H_PromptReco_v3, SingleMuon_Run2016H_PromptReco_v3, SinglePhoton_Run2016H_PromptReco_v3, DoubleEG_Run2016H_PromptReco_v3, MuonEG_Run2016H_PromptReco_v3, DoubleMuon_Run2016H_PromptReco_v3, Tau_Run2016H_PromptReco_v3]

### ----------------------------- summary ----------------------------------------
dataSamples_Moriond2017 = dataSamples_Run2016B_add + dataSamples_Run2016B_v3 + dataSamples_Run2016C_v1 + dataSamples_Run2016D_v1 + dataSamples_Run2016E_v1 + dataSamples_Run2016F_v1 + dataSamples_Run2016G + dataSamples_Run2016H_v1 +dataSamples_Run2016H_v2 + dataSamples_Run2016H_v3


samples = dataSamples_Moriond2017


### ---------------------------------------------------------------------

from CMGTools.TTHAnalysis.setup.Efficiencies import *
dataDir = "$CMSSW_BASE/src/CMGTools/TTHAnalysis/data"

for comp in samples:
    comp.splitFactor = 1000
    comp.isMC = False
    comp.isData = True

if __name__ == "__main__":
   import sys
   if "test" in sys.argv:
       from CMGTools.RootTools.samples.ComponentCreator import testSamples
       testSamples(samples)
   if "locality" in sys.argv:
       import re
       from CMGTools.Production.localityChecker import LocalityChecker
       tier2Checker = LocalityChecker("T2_CH_CERN", datasets="/*/*/MINIAOD*")
       for comp in samples:
           if len(comp.files) == 0: 
               print '\033[34mE: Empty component: '+comp.name+'\033[0m'
               continue
           if not hasattr(comp,'dataset'): continue
           if not re.match("/[^/]+/[^/]+/MINIAOD(SIM)?", comp.dataset): continue
           if "/store/" not in comp.files[0]: continue
           if re.search("/store/(group|user|cmst3)/", comp.files[0]): continue
           if not tier2Checker.available(comp.dataset):
               print "\033[1;31mN: Dataset %s (%s) is not available on T2_CH_CERN\033[0m" % (comp.name,comp.dataset)
           else: print "Y: Dataset %s (%s) is available on T2_CH_CERN" % (comp.name,comp.dataset)
   if "refresh" in sys.argv:
        from CMGTools.Production.cacheChecker import CacheChecker
        checker = CacheChecker()
        dataSamples = samples
        if len(sys.argv) > 2: 
            dataSamples = []
            for x in sys.argv[2:]:
                for s in samples:
                    if x in s.name and s not in dataSamples:
                        dataSamples.append(s)
            dataSamples.sort(key = lambda d : d.name)
        for d in dataSamples:
            print "Checking ",d.name," aka ",d.dataset
            checker.checkComp(d, verbose=True)
   if "list" in sys.argv:
        from CMGTools.HToZZ4L.tools.configTools import printSummary
        dataSamples = samples
        if len(sys.argv) > 2:
            dataSamples = []
            for x in sys.argv[2:]:
                for s in samples:
                    if x in s.name and s not in dataSamples:
                        dataSamples.append(s)
            dataSamples.sort(key = lambda d : d.name)
        printSummary(dataSamples)
