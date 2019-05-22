import PhysicsTools.HeppyCore.framework.config as cfg
import os

#####COMPONENT CREATOR

from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()

### ----------------------------- Zero Tesla run  ----------------------------------------

dataDir = "$CMSSW_BASE/src/CMGTools/TTHAnalysis/data"  # use environmental variable, useful for instance to run on CRAB
json='/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/ReReco/Final/Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt'

run_range = (273158, 284044)
label = "_runs%s_%s"%(run_range[0], run_range[1])

### ----------------------------- Run2016 PromptReco v1 ----------------------------------------

## Commenting out, since it doesn't contain any run in the golden JSON so it's not useful

#JetHT_Run2016B_PromptReco          = kreator.makeDataComponent("JetHT_Run2016B_PromptReco"         , "/JetHT/Run2016B-PromptReco-v1/MINIAOD"         , "CMS", ".*root", json)
#HTMHT_Run2016B_PromptReco          = kreator.makeDataComponent("HTMHT_Run2016B_PromptReco"         , "/HTMHT/Run2016B-PromptReco-v1/MINIAOD"         , "CMS", ".*root", json)
#MET_Run2016B_PromptReco            = kreator.makeDataComponent("MET_Run2016B_PromptReco"           , "/MET/Run2016B-PromptReco-v1/MINIAOD"           , "CMS", ".*root", json)
#SingleElectron_Run2016B_PromptReco = kreator.makeDataComponent("SingleElectron_Run2016B_PromptReco", "/SingleElectron/Run2016B-PromptReco-v1/MINIAOD", "CMS", ".*root", json)
#SingleMuon_Run2016B_PromptReco     = kreator.makeDataComponent("SingleMuon_Run2016B_PromptReco"    , "/SingleMuon/Run2016B-PromptReco-v1/MINIAOD"    , "CMS", ".*root", json)
#SinglePhoton_Run2016B_PromptReco   = kreator.makeDataComponent("SinglePhoton_Run2016B_PromptReco"  , "/SinglePhoton/Run2016B-PromptReco-v1/MINIAOD"  , "CMS", ".*root", json)
#DoubleEG_Run2016B_PromptReco       = kreator.makeDataComponent("DoubleEG_Run2016B_PromptReco"      , "/DoubleEG/Run2016B-PromptReco-v1/MINIAOD"      , "CMS", ".*root", json)
#MuonEG_Run2016B_PromptReco         = kreator.makeDataComponent("MuonEG_Run2016B_PromptReco"       , "/MuonEG/Run2016B-PromptReco-v1/MINIAOD"        , "CMS", ".*root", json)
#DoubleMuon_Run2016B_PromptReco     = kreator.makeDataComponent("DoubleMuon_Run2016B_PromptReco"    , "/DoubleMuon/Run2016B-PromptReco-v1/MINIAOD"    , "CMS", ".*root", json)
#Tau_Run2016B_PromptReco     = kreator.makeDataComponent("Tau_Run2016B_PromptReco"    , "/Tau/Run2016B-PromptReco-v2/MINIAOD"    , "CMS", ".*root", json)
#
#dataSamples_Run2016_v1 = [JetHT_Run2016B_PromptReco, HTMHT_Run2016B_PromptReco, MET_Run2016B_PromptReco, SingleElectron_Run2016B_PromptReco, SingleMuon_Run2016B_PromptReco, SinglePhoton_Run2016B_PromptReco, DoubleEG_Run2016B_PromptReco, MuonEG_Run2016B_PromptReco, DoubleMuon_Run2016B_PromptReco, Tau_Run2016B_PromptReco]
dataSamples_Run2016_v1 = []

### ----------------------------- Run2016B PromptReco v2 ----------------------------------------

JetHT_Run2016B_PromptReco_v2          = kreator.makeDataComponent("JetHT_Run2016B_PromptReco_v2"         , "/JetHT/Run2016B-PromptReco-v2/MINIAOD"         , "CMS", ".*root", json)
HTMHT_Run2016B_PromptReco_v2          = kreator.makeDataComponent("HTMHT_Run2016B_PromptReco_v2"         , "/HTMHT/Run2016B-PromptReco-v2/MINIAOD"         , "CMS", ".*root", json)
MET_Run2016B_PromptReco_v2            = kreator.makeDataComponent("MET_Run2016B_PromptReco_v2"           , "/MET/Run2016B-PromptReco-v2/MINIAOD"           , "CMS", ".*root", json)
SingleElectron_Run2016B_PromptReco_v2 = kreator.makeDataComponent("SingleElectron_Run2016B_PromptReco_v2", "/SingleElectron/Run2016B-PromptReco-v2/MINIAOD", "CMS", ".*root", json)
SingleMuon_Run2016B_PromptReco_v2     = kreator.makeDataComponent("SingleMuon_Run2016B_PromptReco_v2"    , "/SingleMuon/Run2016B-PromptReco-v2/MINIAOD"    , "CMS", ".*root", json)
SinglePhoton_Run2016B_PromptReco_v2   = kreator.makeDataComponent("SinglePhoton_Run2016B_PromptReco_v2"  , "/SinglePhoton/Run2016B-PromptReco-v2/MINIAOD"  , "CMS", ".*root", json)
DoubleEG_Run2016B_PromptReco_v2       = kreator.makeDataComponent("DoubleEG_Run2016B_PromptReco_v2"      , "/DoubleEG/Run2016B-PromptReco-v2/MINIAOD"      , "CMS", ".*root", json)
MuonEG_Run2016B_PromptReco_v2        = kreator.makeDataComponent("MuonEG_Run2016B_PromptReco_v2"        , "/MuonEG/Run2016B-PromptReco-v2/MINIAOD"        , "CMS", ".*root", json)
DoubleMuon_Run2016B_PromptReco_v2     = kreator.makeDataComponent("DoubleMuon_Run2016B_PromptReco_v2"    , "/DoubleMuon/Run2016B-PromptReco-v2/MINIAOD"    , "CMS", ".*root", json)
Tau_Run2016B_PromptReco_v2     = kreator.makeDataComponent("Tau_Run2016B_PromptReco_v2"    , "/Tau/Run2016B-PromptReco-v2/MINIAOD"    , "CMS", ".*root", json)

dataSamples_Run2016B_v2 = [JetHT_Run2016B_PromptReco_v2, HTMHT_Run2016B_PromptReco_v2, MET_Run2016B_PromptReco_v2, SingleElectron_Run2016B_PromptReco_v2, SingleMuon_Run2016B_PromptReco_v2, SinglePhoton_Run2016B_PromptReco_v2, DoubleEG_Run2016B_PromptReco_v2, MuonEG_Run2016B_PromptReco_v2, DoubleMuon_Run2016B_PromptReco_v2, Tau_Run2016B_PromptReco_v2]

### ----------------------------- Run2016C PromptReco v2 ----------------------------------------

JetHT_Run2016C_PromptReco_v2          = kreator.makeDataComponent("JetHT_Run2016C_PromptReco_v2"         , "/JetHT/Run2016C-PromptReco-v2/MINIAOD"         , "CMS", ".*root", json)
HTMHT_Run2016C_PromptReco_v2          = kreator.makeDataComponent("HTMHT_Run2016C_PromptReco_v2"         , "/HTMHT/Run2016C-PromptReco-v2/MINIAOD"         , "CMS", ".*root", json)
MET_Run2016C_PromptReco_v2            = kreator.makeDataComponent("MET_Run2016C_PromptReco_v2"           , "/MET/Run2016C-PromptReco-v2/MINIAOD"           , "CMS", ".*root", json)
SingleElectron_Run2016C_PromptReco_v2 = kreator.makeDataComponent("SingleElectron_Run2016C_PromptReco_v2", "/SingleElectron/Run2016C-PromptReco-v2/MINIAOD", "CMS", ".*root", json)
SingleMuon_Run2016C_PromptReco_v2     = kreator.makeDataComponent("SingleMuon_Run2016C_PromptReco_v2"    , "/SingleMuon/Run2016C-PromptReco-v2/MINIAOD"    , "CMS", ".*root", json)
SinglePhoton_Run2016C_PromptReco_v2   = kreator.makeDataComponent("SinglePhoton_Run2016C_PromptReco_v2"  , "/SinglePhoton/Run2016C-PromptReco-v2/MINIAOD"  , "CMS", ".*root", json)
DoubleEG_Run2016C_PromptReco_v2       = kreator.makeDataComponent("DoubleEG_Run2016C_PromptReco_v2"      , "/DoubleEG/Run2016C-PromptReco-v2/MINIAOD"      , "CMS", ".*root", json)
MuonEG_Run2016C_PromptReco_v2         = kreator.makeDataComponent("MuonEG_Run2016C_PromptReco_v2"        , "/MuonEG/Run2016C-PromptReco-v2/MINIAOD"        , "CMS", ".*root", json)
DoubleMuon_Run2016C_PromptReco_v2     = kreator.makeDataComponent("DoubleMuon_Run2016C_PromptReco_v2"    , "/DoubleMuon/Run2016C-PromptReco-v2/MINIAOD"    , "CMS", ".*root", json)
Tau_Run2016C_PromptReco_v2            = kreator.makeDataComponent("Tau_Run2016C_PromptReco_v2"           , "/Tau/Run2016C-PromptReco-v2/MINIAOD"           , "CMS", ".*root", json)

dataSamples_Run2016C_v2 = [JetHT_Run2016C_PromptReco_v2, HTMHT_Run2016C_PromptReco_v2, MET_Run2016C_PromptReco_v2, SingleElectron_Run2016C_PromptReco_v2, SingleMuon_Run2016C_PromptReco_v2, SinglePhoton_Run2016C_PromptReco_v2, DoubleEG_Run2016C_PromptReco_v2, MuonEG_Run2016C_PromptReco_v2, DoubleMuon_Run2016C_PromptReco_v2, Tau_Run2016C_PromptReco_v2]


### ----------------------------- Run2016D PromptReco v2 ----------------------------------------

JetHT_Run2016D_PromptReco_v2          = kreator.makeDataComponent("JetHT_Run2016D_PromptReco_v2"         , "/JetHT/Run2016D-PromptReco-v2/MINIAOD"         , "CMS", ".*root", json)
HTMHT_Run2016D_PromptReco_v2          = kreator.makeDataComponent("HTMHT_Run2016D_PromptReco_v2"         , "/HTMHT/Run2016D-PromptReco-v2/MINIAOD"         , "CMS", ".*root", json)
MET_Run2016D_PromptReco_v2            = kreator.makeDataComponent("MET_Run2016D_PromptReco_v2"           , "/MET/Run2016D-PromptReco-v2/MINIAOD"           , "CMS", ".*root", json)
SingleElectron_Run2016D_PromptReco_v2 = kreator.makeDataComponent("SingleElectron_Run2016D_PromptReco_v2", "/SingleElectron/Run2016D-PromptReco-v2/MINIAOD", "CMS", ".*root", json)
SingleMuon_Run2016D_PromptReco_v2     = kreator.makeDataComponent("SingleMuon_Run2016D_PromptReco_v2"    , "/SingleMuon/Run2016D-PromptReco-v2/MINIAOD"    , "CMS", ".*root", json)
SinglePhoton_Run2016D_PromptReco_v2   = kreator.makeDataComponent("SinglePhoton_Run2016D_PromptReco_v2"  , "/SinglePhoton/Run2016D-PromptReco-v2/MINIAOD"  , "CMS", ".*root", json)
DoubleEG_Run2016D_PromptReco_v2       = kreator.makeDataComponent("DoubleEG_Run2016D_PromptReco_v2"      , "/DoubleEG/Run2016D-PromptReco-v2/MINIAOD"      , "CMS", ".*root", json)
MuonEG_Run2016D_PromptReco_v2         = kreator.makeDataComponent("MuonEG_Run2016D_PromptReco_v2"        , "/MuonEG/Run2016D-PromptReco-v2/MINIAOD"        , "CMS", ".*root", json)
DoubleMuon_Run2016D_PromptReco_v2     = kreator.makeDataComponent("DoubleMuon_Run2016D_PromptReco_v2"    , "/DoubleMuon/Run2016D-PromptReco-v2/MINIAOD"    , "CMS", ".*root", json)
Tau_Run2016D_PromptReco_v2            = kreator.makeDataComponent("Tau_Run2016D_PromptReco_v2"           , "/Tau/Run2016D-PromptReco-v2/MINIAOD"           , "CMS", ".*root", json)

dataSamples_Run2016D_v2 = [JetHT_Run2016D_PromptReco_v2, HTMHT_Run2016D_PromptReco_v2, MET_Run2016D_PromptReco_v2, SingleElectron_Run2016D_PromptReco_v2, SingleMuon_Run2016D_PromptReco_v2, SinglePhoton_Run2016D_PromptReco_v2, DoubleEG_Run2016D_PromptReco_v2, MuonEG_Run2016D_PromptReco_v2, DoubleMuon_Run2016D_PromptReco_v2, Tau_Run2016D_PromptReco_v2]

### ----------------------------- Run2016E PromptReco v2 ----------------------------------------

JetHT_Run2016E_PromptReco_v2          = kreator.makeDataComponent("JetHT_Run2016E_PromptReco_v2"         , "/JetHT/Run2016E-PromptReco-v2/MINIAOD"         , "CMS", ".*root", json)
HTMHT_Run2016E_PromptReco_v2          = kreator.makeDataComponent("HTMHT_Run2016E_PromptReco_v2"         , "/HTMHT/Run2016E-PromptReco-v2/MINIAOD"         , "CMS", ".*root", json)
MET_Run2016E_PromptReco_v2            = kreator.makeDataComponent("MET_Run2016E_PromptReco_v2"           , "/MET/Run2016E-PromptReco-v2/MINIAOD"           , "CMS", ".*root", json)
SingleElectron_Run2016E_PromptReco_v2 = kreator.makeDataComponent("SingleElectron_Run2016E_PromptReco_v2", "/SingleElectron/Run2016E-PromptReco-v2/MINIAOD", "CMS", ".*root", json)
SingleMuon_Run2016E_PromptReco_v2     = kreator.makeDataComponent("SingleMuon_Run2016E_PromptReco_v2"    , "/SingleMuon/Run2016E-PromptReco-v2/MINIAOD"    , "CMS", ".*root", json)
SinglePhoton_Run2016E_PromptReco_v2   = kreator.makeDataComponent("SinglePhoton_Run2016E_PromptReco_v2"  , "/SinglePhoton/Run2016E-PromptReco-v2/MINIAOD"  , "CMS", ".*root", json)
DoubleEG_Run2016E_PromptReco_v2       = kreator.makeDataComponent("DoubleEG_Run2016E_PromptReco_v2"      , "/DoubleEG/Run2016E-PromptReco-v2/MINIAOD"      , "CMS", ".*root", json)
MuonEG_Run2016E_PromptReco_v2         = kreator.makeDataComponent("MuonEG_Run2016E_PromptReco_v2"        , "/MuonEG/Run2016E-PromptReco-v2/MINIAOD"        , "CMS", ".*root", json)
DoubleMuon_Run2016E_PromptReco_v2     = kreator.makeDataComponent("DoubleMuon_Run2016E_PromptReco_v2"    , "/DoubleMuon/Run2016E-PromptReco-v2/MINIAOD"    , "CMS", ".*root", json)
Tau_Run2016E_PromptReco_v2            = kreator.makeDataComponent("Tau_Run2016E_PromptReco_v2"           , "/Tau/Run2016E-PromptReco-v2/MINIAOD"           , "CMS", ".*root", json)

dataSamples_Run2016E_v2 = [JetHT_Run2016E_PromptReco_v2, HTMHT_Run2016E_PromptReco_v2, MET_Run2016E_PromptReco_v2, SingleElectron_Run2016E_PromptReco_v2, SingleMuon_Run2016E_PromptReco_v2, SinglePhoton_Run2016E_PromptReco_v2, DoubleEG_Run2016E_PromptReco_v2, MuonEG_Run2016E_PromptReco_v2, DoubleMuon_Run2016E_PromptReco_v2, Tau_Run2016E_PromptReco_v2]


### ----------------------------- Run2016F PromptReco v1 ----------------------------------------

JetHT_Run2016F_PromptReco_v1          = kreator.makeDataComponent("JetHT_Run2016F_PromptReco_v1"         , "/JetHT/Run2016F-PromptReco-v1/MINIAOD"         , "CMS", ".*root", json)
HTMHT_Run2016F_PromptReco_v1          = kreator.makeDataComponent("HTMHT_Run2016F_PromptReco_v1"         , "/HTMHT/Run2016F-PromptReco-v1/MINIAOD"         , "CMS", ".*root", json)
MET_Run2016F_PromptReco_v1            = kreator.makeDataComponent("MET_Run2016F_PromptReco_v1"           , "/MET/Run2016F-PromptReco-v1/MINIAOD"           , "CMS", ".*root", json)
SingleElectron_Run2016F_PromptReco_v1 = kreator.makeDataComponent("SingleElectron_Run2016F_PromptReco_v1", "/SingleElectron/Run2016F-PromptReco-v1/MINIAOD", "CMS", ".*root", json)
SingleMuon_Run2016F_PromptReco_v1     = kreator.makeDataComponent("SingleMuon_Run2016F_PromptReco_v1"    , "/SingleMuon/Run2016F-PromptReco-v1/MINIAOD"    , "CMS", ".*root", json)
SinglePhoton_Run2016F_PromptReco_v1   = kreator.makeDataComponent("SinglePhoton_Run2016F_PromptReco_v1"  , "/SinglePhoton/Run2016F-PromptReco-v1/MINIAOD"  , "CMS", ".*root", json)
DoubleEG_Run2016F_PromptReco_v1       = kreator.makeDataComponent("DoubleEG_Run2016F_PromptReco_v1"      , "/DoubleEG/Run2016F-PromptReco-v1/MINIAOD"      , "CMS", ".*root", json)
MuonEG_Run2016F_PromptReco_v1         = kreator.makeDataComponent("MuonEG_Run2016F_PromptReco_v1"        , "/MuonEG/Run2016F-PromptReco-v1/MINIAOD"        , "CMS", ".*root", json)
DoubleMuon_Run2016F_PromptReco_v1     = kreator.makeDataComponent("DoubleMuon_Run2016F_PromptReco_v1"    , "/DoubleMuon/Run2016F-PromptReco-v1/MINIAOD"    , "CMS", ".*root", json)
Tau_Run2016F_PromptReco_v1            = kreator.makeDataComponent("Tau_Run2016F_PromptReco_v1"           , "/Tau/Run2016F-PromptReco-v1/MINIAOD"           , "CMS", ".*root", json)

dataSamples_Run2016F_v1 = [JetHT_Run2016F_PromptReco_v1, HTMHT_Run2016F_PromptReco_v1, MET_Run2016F_PromptReco_v1, SingleElectron_Run2016F_PromptReco_v1, SingleMuon_Run2016F_PromptReco_v1, SinglePhoton_Run2016F_PromptReco_v1, DoubleEG_Run2016F_PromptReco_v1, MuonEG_Run2016F_PromptReco_v1, DoubleMuon_Run2016F_PromptReco_v1, Tau_Run2016F_PromptReco_v1]

### ----------------------------- Run2016G PromptReco v1 ----------------------------------------

JetHT_Run2016G_PromptReco_v1          = kreator.makeDataComponent("JetHT_Run2016G_PromptReco_v1"         , "/JetHT/Run2016G-PromptReco-v1/MINIAOD"         , "CMS", ".*root", json)
HTMHT_Run2016G_PromptReco_v1          = kreator.makeDataComponent("HTMHT_Run2016G_PromptReco_v1"         , "/HTMHT/Run2016G-PromptReco-v1/MINIAOD"         , "CMS", ".*root", json)
MET_Run2016G_PromptReco_v1            = kreator.makeDataComponent("MET_Run2016G_PromptReco_v1"           , "/MET/Run2016G-PromptReco-v1/MINIAOD"           , "CMS", ".*root", json)
SingleElectron_Run2016G_PromptReco_v1 = kreator.makeDataComponent("SingleElectron_Run2016G_PromptReco_v1", "/SingleElectron/Run2016G-PromptReco-v1/MINIAOD", "CMS", ".*root", json)
SingleMuon_Run2016G_PromptReco_v1     = kreator.makeDataComponent("SingleMuon_Run2016G_PromptReco_v1"    , "/SingleMuon/Run2016G-PromptReco-v1/MINIAOD"    , "CMS", ".*root", json)
SinglePhoton_Run2016G_PromptReco_v1   = kreator.makeDataComponent("SinglePhoton_Run2016G_PromptReco_v1"  , "/SinglePhoton/Run2016G-PromptReco-v1/MINIAOD"  , "CMS", ".*root", json)
DoubleEG_Run2016G_PromptReco_v1       = kreator.makeDataComponent("DoubleEG_Run2016G_PromptReco_v1"      , "/DoubleEG/Run2016G-PromptReco-v1/MINIAOD"      , "CMS", ".*root", json)
MuonEG_Run2016G_PromptReco_v1        = kreator.makeDataComponent("MuonEG_Run2016G_PromptReco_v1"        , "/MuonEG/Run2016G-PromptReco-v1/MINIAOD"        , "CMS", ".*root", json)
DoubleMuon_Run2016G_PromptReco_v1     = kreator.makeDataComponent("DoubleMuon_Run2016G_PromptReco_v1"    , "/DoubleMuon/Run2016G-PromptReco-v1/MINIAOD"    , "CMS", ".*root", json)
Tau_Run2016G_PromptReco_v1     = kreator.makeDataComponent("Tau_Run2016G_PromptReco_v1"    , "/Tau/Run2016G-PromptReco-v1/MINIAOD"    , "CMS", ".*root", json)

dataSamples_Run2016G_v1 = [JetHT_Run2016G_PromptReco_v1, HTMHT_Run2016G_PromptReco_v1, MET_Run2016G_PromptReco_v1, SingleElectron_Run2016G_PromptReco_v1, SingleMuon_Run2016G_PromptReco_v1, SinglePhoton_Run2016G_PromptReco_v1, DoubleEG_Run2016G_PromptReco_v1, MuonEG_Run2016G_PromptReco_v1, DoubleMuon_Run2016G_PromptReco_v1, Tau_Run2016G_PromptReco_v1]

### ----------------------------- Run2016H PromptReco v1 ----------------------------------------

### Skipping this datasets since there were no stable beam collisions

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


### ----------------------------- summary of prompt reco ----------------------------------------
dataSamples_PromptReco = dataSamples_Run2016_v1 + dataSamples_Run2016B_v2 + dataSamples_Run2016C_v2 + dataSamples_Run2016D_v2 + dataSamples_Run2016E_v2 + dataSamples_Run2016F_v1 + dataSamples_Run2016G_v1 + dataSamples_Run2016H_v2 + dataSamples_Run2016H_v3


### ----------------------------- Run2016B 23Sep2016 ----------------------------------------

JetHT_Run2016B_23Sep2016          = kreator.makeDataComponent("JetHT_Run2016B_23Sep2016"         , "/JetHT/Run2016B-23Sep2016-v3/MINIAOD"         , "CMS", ".*root", json)
HTMHT_Run2016B_23Sep2016          = kreator.makeDataComponent("HTMHT_Run2016B_23Sep2016"         , "/HTMHT/Run2016B-23Sep2016-v3/MINIAOD"         , "CMS", ".*root", json)
MET_Run2016B_23Sep2016            = kreator.makeDataComponent("MET_Run2016B_23Sep2016"           , "/MET/Run2016B-23Sep2016-v3/MINIAOD"           , "CMS", ".*root", json)
SingleElectron_Run2016B_23Sep2016 = kreator.makeDataComponent("SingleElectron_Run2016B_23Sep2016", "/SingleElectron/Run2016B-23Sep2016-v3/MINIAOD", "CMS", ".*root", json)
SingleMuon_Run2016B_23Sep2016     = kreator.makeDataComponent("SingleMuon_Run2016B_23Sep2016"    , "/SingleMuon/Run2016B-23Sep2016-v3/MINIAOD"    , "CMS", ".*root", json)
SinglePhoton_Run2016B_23Sep2016   = kreator.makeDataComponent("SinglePhoton_Run2016B_23Sep2016"  , "/SinglePhoton/Run2016B-23Sep2016-v3/MINIAOD"  , "CMS", ".*root", json)
DoubleEG_Run2016B_23Sep2016       = kreator.makeDataComponent("DoubleEG_Run2016B_23Sep2016"      , "/DoubleEG/Run2016B-23Sep2016-v3/MINIAOD"      , "CMS", ".*root", json)
MuonEG_Run2016B_23Sep2016        = kreator.makeDataComponent("MuonEG_Run2016B_23Sep2016"        , "/MuonEG/Run2016B-23Sep2016-v3/MINIAOD"        , "CMS", ".*root", json)
DoubleMuon_Run2016B_23Sep2016     = kreator.makeDataComponent("DoubleMuon_Run2016B_23Sep2016"    , "/DoubleMuon/Run2016B-23Sep2016-v3/MINIAOD"    , "CMS", ".*root", json)
Tau_Run2016B_23Sep2016     = kreator.makeDataComponent("Tau_Run2016B_23Sep2016"    , "/Tau/Run2016B-23Sep2016-v3/MINIAOD"    , "CMS", ".*root", json)

dataSamples_Run2016B_23Sep2016 = [JetHT_Run2016B_23Sep2016, HTMHT_Run2016B_23Sep2016, MET_Run2016B_23Sep2016, SingleElectron_Run2016B_23Sep2016, SingleMuon_Run2016B_23Sep2016, SinglePhoton_Run2016B_23Sep2016, DoubleEG_Run2016B_23Sep2016, MuonEG_Run2016B_23Sep2016, DoubleMuon_Run2016B_23Sep2016, Tau_Run2016B_23Sep2016]

### ----------------------------- Run2016C 23Sep2016 ----------------------------------------

JetHT_Run2016C_23Sep2016          = kreator.makeDataComponent("JetHT_Run2016C_23Sep2016"         , "/JetHT/Run2016C-23Sep2016-v1/MINIAOD"         , "CMS", ".*root", json)
HTMHT_Run2016C_23Sep2016          = kreator.makeDataComponent("HTMHT_Run2016C_23Sep2016"         , "/HTMHT/Run2016C-23Sep2016-v1/MINIAOD"         , "CMS", ".*root", json)
MET_Run2016C_23Sep2016            = kreator.makeDataComponent("MET_Run2016C_23Sep2016"           , "/MET/Run2016C-23Sep2016-v1/MINIAOD"           , "CMS", ".*root", json)
SingleElectron_Run2016C_23Sep2016 = kreator.makeDataComponent("SingleElectron_Run2016C_23Sep2016", "/SingleElectron/Run2016C-23Sep2016-v1/MINIAOD", "CMS", ".*root", json)
SingleMuon_Run2016C_23Sep2016     = kreator.makeDataComponent("SingleMuon_Run2016C_23Sep2016"    , "/SingleMuon/Run2016C-23Sep2016-v1/MINIAOD"    , "CMS", ".*root", json)
SinglePhoton_Run2016C_23Sep2016   = kreator.makeDataComponent("SinglePhoton_Run2016C_23Sep2016"  , "/SinglePhoton/Run2016C-23Sep2016-v1/MINIAOD"  , "CMS", ".*root", json)
DoubleEG_Run2016C_23Sep2016       = kreator.makeDataComponent("DoubleEG_Run2016C_23Sep2016"      , "/DoubleEG/Run2016C-23Sep2016-v1/MINIAOD"      , "CMS", ".*root", json)
MuonEG_Run2016C_23Sep2016         = kreator.makeDataComponent("MuonEG_Run2016C_23Sep2016"        , "/MuonEG/Run2016C-23Sep2016-v1/MINIAOD"        , "CMS", ".*root", json)
DoubleMuon_Run2016C_23Sep2016     = kreator.makeDataComponent("DoubleMuon_Run2016C_23Sep2016"    , "/DoubleMuon/Run2016C-23Sep2016-v1/MINIAOD"    , "CMS", ".*root", json)
Tau_Run2016C_23Sep2016            = kreator.makeDataComponent("Tau_Run2016C_23Sep2016"           , "/Tau/Run2016C-23Sep2016-v1/MINIAOD"           , "CMS", ".*root", json)

dataSamples_Run2016C_23Sep2016 = [JetHT_Run2016C_23Sep2016, HTMHT_Run2016C_23Sep2016, MET_Run2016C_23Sep2016, SingleElectron_Run2016C_23Sep2016, SingleMuon_Run2016C_23Sep2016, SinglePhoton_Run2016C_23Sep2016, DoubleEG_Run2016C_23Sep2016, MuonEG_Run2016C_23Sep2016, DoubleMuon_Run2016C_23Sep2016, Tau_Run2016C_23Sep2016]


### ----------------------------- Run2016D 23Sep2016 v2 ----------------------------------------

JetHT_Run2016D_23Sep2016          = kreator.makeDataComponent("JetHT_Run2016D_23Sep2016"         , "/JetHT/Run2016D-23Sep2016-v1/MINIAOD"         , "CMS", ".*root", json)
HTMHT_Run2016D_23Sep2016          = kreator.makeDataComponent("HTMHT_Run2016D_23Sep2016"         , "/HTMHT/Run2016D-23Sep2016-v1/MINIAOD"         , "CMS", ".*root", json)
MET_Run2016D_23Sep2016            = kreator.makeDataComponent("MET_Run2016D_23Sep2016"           , "/MET/Run2016D-23Sep2016-v1/MINIAOD"           , "CMS", ".*root", json)
SingleElectron_Run2016D_23Sep2016 = kreator.makeDataComponent("SingleElectron_Run2016D_23Sep2016", "/SingleElectron/Run2016D-23Sep2016-v1/MINIAOD", "CMS", ".*root", json)
SingleMuon_Run2016D_23Sep2016     = kreator.makeDataComponent("SingleMuon_Run2016D_23Sep2016"    , "/SingleMuon/Run2016D-23Sep2016-v1/MINIAOD"    , "CMS", ".*root", json)
SinglePhoton_Run2016D_23Sep2016   = kreator.makeDataComponent("SinglePhoton_Run2016D_23Sep2016"  , "/SinglePhoton/Run2016D-23Sep2016-v1/MINIAOD"  , "CMS", ".*root", json)
DoubleEG_Run2016D_23Sep2016       = kreator.makeDataComponent("DoubleEG_Run2016D_23Sep2016"      , "/DoubleEG/Run2016D-23Sep2016-v1/MINIAOD"      , "CMS", ".*root", json)
MuonEG_Run2016D_23Sep2016         = kreator.makeDataComponent("MuonEG_Run2016D_23Sep2016"        , "/MuonEG/Run2016D-23Sep2016-v1/MINIAOD"        , "CMS", ".*root", json)
DoubleMuon_Run2016D_23Sep2016     = kreator.makeDataComponent("DoubleMuon_Run2016D_23Sep2016"    , "/DoubleMuon/Run2016D-23Sep2016-v1/MINIAOD"    , "CMS", ".*root", json)
Tau_Run2016D_23Sep2016            = kreator.makeDataComponent("Tau_Run2016D_23Sep2016"           , "/Tau/Run2016D-23Sep2016-v1/MINIAOD"           , "CMS", ".*root", json)

dataSamples_Run2016D_23Sep2016 = [JetHT_Run2016D_23Sep2016, HTMHT_Run2016D_23Sep2016, MET_Run2016D_23Sep2016, SingleElectron_Run2016D_23Sep2016, SingleMuon_Run2016D_23Sep2016, SinglePhoton_Run2016D_23Sep2016, DoubleEG_Run2016D_23Sep2016, MuonEG_Run2016D_23Sep2016, DoubleMuon_Run2016D_23Sep2016, Tau_Run2016D_23Sep2016]

### ----------------------------- Run2016E 23Sep2016 v2 ----------------------------------------

JetHT_Run2016E_23Sep2016          = kreator.makeDataComponent("JetHT_Run2016E_23Sep2016"         , "/JetHT/Run2016E-23Sep2016-v1/MINIAOD"         , "CMS", ".*root", json)
HTMHT_Run2016E_23Sep2016          = kreator.makeDataComponent("HTMHT_Run2016E_23Sep2016"         , "/HTMHT/Run2016E-23Sep2016-v1/MINIAOD"         , "CMS", ".*root", json)
MET_Run2016E_23Sep2016            = kreator.makeDataComponent("MET_Run2016E_23Sep2016"           , "/MET/Run2016E-23Sep2016-v1/MINIAOD"           , "CMS", ".*root", json)
SingleElectron_Run2016E_23Sep2016 = kreator.makeDataComponent("SingleElectron_Run2016E_23Sep2016", "/SingleElectron/Run2016E-23Sep2016-v1/MINIAOD", "CMS", ".*root", json)
SingleMuon_Run2016E_23Sep2016     = kreator.makeDataComponent("SingleMuon_Run2016E_23Sep2016"    , "/SingleMuon/Run2016E-23Sep2016-v1/MINIAOD"    , "CMS", ".*root", json)
SinglePhoton_Run2016E_23Sep2016   = kreator.makeDataComponent("SinglePhoton_Run2016E_23Sep2016"  , "/SinglePhoton/Run2016E-23Sep2016-v1/MINIAOD"  , "CMS", ".*root", json)
DoubleEG_Run2016E_23Sep2016       = kreator.makeDataComponent("DoubleEG_Run2016E_23Sep2016"      , "/DoubleEG/Run2016E-23Sep2016-v1/MINIAOD"      , "CMS", ".*root", json)
MuonEG_Run2016E_23Sep2016         = kreator.makeDataComponent("MuonEG_Run2016E_23Sep2016"        , "/MuonEG/Run2016E-23Sep2016-v1/MINIAOD"        , "CMS", ".*root", json)
DoubleMuon_Run2016E_23Sep2016     = kreator.makeDataComponent("DoubleMuon_Run2016E_23Sep2016"    , "/DoubleMuon/Run2016E-23Sep2016-v1/MINIAOD"    , "CMS", ".*root", json)
Tau_Run2016E_23Sep2016            = kreator.makeDataComponent("Tau_Run2016E_23Sep2016"           , "/Tau/Run2016E-23Sep2016-v1/MINIAOD"           , "CMS", ".*root", json)

dataSamples_Run2016E_23Sep2016 = [JetHT_Run2016E_23Sep2016, HTMHT_Run2016E_23Sep2016, MET_Run2016E_23Sep2016, SingleElectron_Run2016E_23Sep2016, SingleMuon_Run2016E_23Sep2016, SinglePhoton_Run2016E_23Sep2016, DoubleEG_Run2016E_23Sep2016, MuonEG_Run2016E_23Sep2016, DoubleMuon_Run2016E_23Sep2016, Tau_Run2016E_23Sep2016]


### ----------------------------- Run2016F 23Sep2016 v1 ----------------------------------------

JetHT_Run2016F_23Sep2016          = kreator.makeDataComponent("JetHT_Run2016F_23Sep2016"         , "/JetHT/Run2016F-23Sep2016-v1/MINIAOD"         , "CMS", ".*root", json)
HTMHT_Run2016F_23Sep2016          = kreator.makeDataComponent("HTMHT_Run2016F_23Sep2016"         , "/HTMHT/Run2016F-23Sep2016-v1/MINIAOD"         , "CMS", ".*root", json)
MET_Run2016F_23Sep2016            = kreator.makeDataComponent("MET_Run2016F_23Sep2016"           , "/MET/Run2016F-23Sep2016-v1/MINIAOD"           , "CMS", ".*root", json)
SingleElectron_Run2016F_23Sep2016 = kreator.makeDataComponent("SingleElectron_Run2016F_23Sep2016", "/SingleElectron/Run2016F-23Sep2016-v1/MINIAOD", "CMS", ".*root", json)
SingleMuon_Run2016F_23Sep2016     = kreator.makeDataComponent("SingleMuon_Run2016F_23Sep2016"    , "/SingleMuon/Run2016F-23Sep2016-v1/MINIAOD"    , "CMS", ".*root", json)
SinglePhoton_Run2016F_23Sep2016   = kreator.makeDataComponent("SinglePhoton_Run2016F_23Sep2016"  , "/SinglePhoton/Run2016F-23Sep2016-v1/MINIAOD"  , "CMS", ".*root", json)
DoubleEG_Run2016F_23Sep2016       = kreator.makeDataComponent("DoubleEG_Run2016F_23Sep2016"      , "/DoubleEG/Run2016F-23Sep2016-v1/MINIAOD"      , "CMS", ".*root", json)
MuonEG_Run2016F_23Sep2016         = kreator.makeDataComponent("MuonEG_Run2016F_23Sep2016"        , "/MuonEG/Run2016F-23Sep2016-v1/MINIAOD"        , "CMS", ".*root", json)
DoubleMuon_Run2016F_23Sep2016     = kreator.makeDataComponent("DoubleMuon_Run2016F_23Sep2016"    , "/DoubleMuon/Run2016F-23Sep2016-v1/MINIAOD"    , "CMS", ".*root", json)
Tau_Run2016F_23Sep2016            = kreator.makeDataComponent("Tau_Run2016F_23Sep2016"           , "/Tau/Run2016F-23Sep2016-v1/MINIAOD"           , "CMS", ".*root", json)

dataSamples_Run2016F_23Sep2016 = [JetHT_Run2016F_23Sep2016, HTMHT_Run2016F_23Sep2016, MET_Run2016F_23Sep2016, SingleElectron_Run2016F_23Sep2016, SingleMuon_Run2016F_23Sep2016, SinglePhoton_Run2016F_23Sep2016, DoubleEG_Run2016F_23Sep2016, MuonEG_Run2016F_23Sep2016, DoubleMuon_Run2016F_23Sep2016, Tau_Run2016F_23Sep2016]

### ----------------------------- Run2016G 23Sep2016 v1 ----------------------------------------

JetHT_Run2016G_23Sep2016          = kreator.makeDataComponent("JetHT_Run2016G_23Sep2016"         , "/JetHT/Run2016G-23Sep2016-v1/MINIAOD"         , "CMS", ".*root", json)
HTMHT_Run2016G_23Sep2016          = kreator.makeDataComponent("HTMHT_Run2016G_23Sep2016"         , "/HTMHT/Run2016G-23Sep2016-v2/MINIAOD"         , "CMS", ".*root", json)
MET_Run2016G_23Sep2016            = kreator.makeDataComponent("MET_Run2016G_23Sep2016"           , "/MET/Run2016G-23Sep2016-v1/MINIAOD"           , "CMS", ".*root", json)
SingleElectron_Run2016G_23Sep2016 = kreator.makeDataComponent("SingleElectron_Run2016G_23Sep2016", "/SingleElectron/Run2016G-23Sep2016-v1/MINIAOD", "CMS", ".*root", json)
SingleMuon_Run2016G_23Sep2016     = kreator.makeDataComponent("SingleMuon_Run2016G_23Sep2016"    , "/SingleMuon/Run2016G-23Sep2016-v1/MINIAOD"    , "CMS", ".*root", json)
SinglePhoton_Run2016G_23Sep2016   = kreator.makeDataComponent("SinglePhoton_Run2016G_23Sep2016"  , "/SinglePhoton/Run2016G-23Sep2016-v1/MINIAOD"  , "CMS", ".*root", json)
DoubleEG_Run2016G_23Sep2016       = kreator.makeDataComponent("DoubleEG_Run2016G_23Sep2016"      , "/DoubleEG/Run2016G-23Sep2016-v1/MINIAOD"      , "CMS", ".*root", json)
MuonEG_Run2016G_23Sep2016        = kreator.makeDataComponent("MuonEG_Run2016G_23Sep2016"        , "/MuonEG/Run2016G-23Sep2016-v1/MINIAOD"        , "CMS", ".*root", json)
DoubleMuon_Run2016G_23Sep2016     = kreator.makeDataComponent("DoubleMuon_Run2016G_23Sep2016"    , "/DoubleMuon/Run2016G-23Sep2016-v1/MINIAOD"    , "CMS", ".*root", json)
Tau_Run2016G_23Sep2016     = kreator.makeDataComponent("Tau_Run2016G_23Sep2016"    , "/Tau/Run2016G-23Sep2016-v1/MINIAOD"    , "CMS", ".*root", json)

dataSamples_Run2016G_23Sep2016 = [JetHT_Run2016G_23Sep2016, HTMHT_Run2016G_23Sep2016, MET_Run2016G_23Sep2016, SingleElectron_Run2016G_23Sep2016, SingleMuon_Run2016G_23Sep2016, SinglePhoton_Run2016G_23Sep2016, DoubleEG_Run2016G_23Sep2016, MuonEG_Run2016G_23Sep2016, DoubleMuon_Run2016G_23Sep2016, Tau_Run2016G_23Sep2016]
samples = dataSamples_PromptReco

### Summary of prompt reco
dataSamples_23Sep2016 = dataSamples_Run2016B_23Sep2016 + dataSamples_Run2016C_23Sep2016 + dataSamples_Run2016D_23Sep2016 + dataSamples_Run2016E_23Sep2016 + dataSamples_Run2016F_23Sep2016 + dataSamples_Run2016G_23Sep2016

### Dataset corresponding to the full Run2016 with re-reco + prompt
dataSamples_23Sep2016PlusPrompt = dataSamples_23Sep2016 + dataSamples_Run2016H_v2 + dataSamples_Run2016H_v3

### ----------------------------- Run2016B v2 03Feb2017 ----------------------------------------

JetHT_Run2016B_03Feb2017_v2       = kreator.makeDataComponent("JetHT_Run2016B_03Feb2017_v2"      , "/JetHT/Run2016B-03Feb2017_ver2-v2/MINIAOD"         , "CMS", ".*root", json)
HTMHT_Run2016B_03Feb2017_v2       = kreator.makeDataComponent("HTMHT_Run2016B_03Feb2017_v2"      , "/HTMHT/Run2016B-03Feb2017_ver2-v2/MINIAOD"         , "CMS", ".*root", json)
MET_Run2016B_03Feb2017_v2         = kreator.makeDataComponent("MET_Run2016B_03Feb2017_v2"        , "/MET/Run2016B-03Feb2017_ver2-v2/MINIAOD"           , "CMS", ".*root", json)
SingleElectron_Run2016B_03Feb2017_v2 = kreator.makeDataComponent("SingleElectron_Run2016B_03Feb2017_v2", "/SingleElectron/Run2016B-03Feb2017_ver2-v2/MINIAOD", "CMS", ".*root", json)
SingleMuon_Run2016B_03Feb2017_v2  = kreator.makeDataComponent("SingleMuon_Run2016B_03Feb2017_v2" , "/SingleMuon/Run2016B-03Feb2017_ver2-v2/MINIAOD"    , "CMS", ".*root", json)
SinglePhoton_Run2016B_03Feb2017_v2= kreator.makeDataComponent("SinglePhoton_Run2016B_03Feb2017_v2"  , "/SinglePhoton/Run2016B-03Feb2017_ver2-v2/MINIAOD"  , "CMS", ".*root", json)
DoubleEG_Run2016B_03Feb2017_v2    = kreator.makeDataComponent("DoubleEG_Run2016B_03Feb2017_v2"   , "/DoubleEG/Run2016B-03Feb2017_ver2-v2/MINIAOD"      , "CMS", ".*root", json)
MuonEG_Run2016B_03Feb2017_v2     = kreator.makeDataComponent("MuonEG_Run2016B_03Feb2017_v2"     , "/MuonEG/Run2016B-03Feb2017_ver2-v2/MINIAOD"        , "CMS", ".*root", json)
DoubleMuon_Run2016B_03Feb2017_v2  = kreator.makeDataComponent("DoubleMuon_Run2016B_03Feb2017_v2" , "/DoubleMuon/Run2016B-03Feb2017_ver2-v2/MINIAOD"    , "CMS", ".*root", json)
Tau_Run2016B_03Feb2017_v2  = kreator.makeDataComponent("Tau_Run2016B_03Feb2017_v2" , "/Tau/Run2016B-03Feb2017_ver2-v2/MINIAOD"    , "CMS", ".*root", json)

dataSamples_Run2016B_03Feb2017_v2 = [JetHT_Run2016B_03Feb2017_v2, HTMHT_Run2016B_03Feb2017_v2, MET_Run2016B_03Feb2017_v2, SingleElectron_Run2016B_03Feb2017_v2, SingleMuon_Run2016B_03Feb2017_v2, SinglePhoton_Run2016B_03Feb2017_v2, DoubleEG_Run2016B_03Feb2017_v2, MuonEG_Run2016B_03Feb2017_v2, DoubleMuon_Run2016B_03Feb2017_v2, Tau_Run2016B_03Feb2017_v2]

### ----------------------------- Run2016C 03Feb2017 ----------------------------------------

JetHT_Run2016C_03Feb2017          = kreator.makeDataComponent("JetHT_Run2016C_03Feb2017"         , "/JetHT/Run2016C-03Feb2017-v1/MINIAOD"         , "CMS", ".*root", json)
HTMHT_Run2016C_03Feb2017          = kreator.makeDataComponent("HTMHT_Run2016C_03Feb2017"         , "/HTMHT/Run2016C-03Feb2017-v1/MINIAOD"         , "CMS", ".*root", json)
MET_Run2016C_03Feb2017            = kreator.makeDataComponent("MET_Run2016C_03Feb2017"           , "/MET/Run2016C-03Feb2017-v1/MINIAOD"           , "CMS", ".*root", json)
SingleElectron_Run2016C_03Feb2017 = kreator.makeDataComponent("SingleElectron_Run2016C_03Feb2017", "/SingleElectron/Run2016C-03Feb2017-v1/MINIAOD", "CMS", ".*root", json)
SingleMuon_Run2016C_03Feb2017     = kreator.makeDataComponent("SingleMuon_Run2016C_03Feb2017"    , "/SingleMuon/Run2016C-03Feb2017-v1/MINIAOD"    , "CMS", ".*root", json)
SinglePhoton_Run2016C_03Feb2017   = kreator.makeDataComponent("SinglePhoton_Run2016C_03Feb2017"  , "/SinglePhoton/Run2016C-03Feb2017-v1/MINIAOD"  , "CMS", ".*root", json)
DoubleEG_Run2016C_03Feb2017       = kreator.makeDataComponent("DoubleEG_Run2016C_03Feb2017"      , "/DoubleEG/Run2016C-03Feb2017-v1/MINIAOD"      , "CMS", ".*root", json)
MuonEG_Run2016C_03Feb2017         = kreator.makeDataComponent("MuonEG_Run2016C_03Feb2017"        , "/MuonEG/Run2016C-03Feb2017-v1/MINIAOD"        , "CMS", ".*root", json)
DoubleMuon_Run2016C_03Feb2017     = kreator.makeDataComponent("DoubleMuon_Run2016C_03Feb2017"    , "/DoubleMuon/Run2016C-03Feb2017-v1/MINIAOD"    , "CMS", ".*root", json)
Tau_Run2016C_03Feb2017            = kreator.makeDataComponent("Tau_Run2016C_03Feb2017"           , "/Tau/Run2016C-03Feb2017-v1/MINIAOD"           , "CMS", ".*root", json)

dataSamples_Run2016C_03Feb2017 = [JetHT_Run2016C_03Feb2017, HTMHT_Run2016C_03Feb2017, MET_Run2016C_03Feb2017, SingleElectron_Run2016C_03Feb2017, SingleMuon_Run2016C_03Feb2017, SinglePhoton_Run2016C_03Feb2017, DoubleEG_Run2016C_03Feb2017, MuonEG_Run2016C_03Feb2017, DoubleMuon_Run2016C_03Feb2017, Tau_Run2016C_03Feb2017]


### ----------------------------- Run2016D 03Feb2017 v2 ----------------------------------------

JetHT_Run2016D_03Feb2017          = kreator.makeDataComponent("JetHT_Run2016D_03Feb2017"         , "/JetHT/Run2016D-03Feb2017-v1/MINIAOD"         , "CMS", ".*root", json)
HTMHT_Run2016D_03Feb2017          = kreator.makeDataComponent("HTMHT_Run2016D_03Feb2017"         , "/HTMHT/Run2016D-03Feb2017-v1/MINIAOD"         , "CMS", ".*root", json)
MET_Run2016D_03Feb2017            = kreator.makeDataComponent("MET_Run2016D_03Feb2017"           , "/MET/Run2016D-03Feb2017-v1/MINIAOD"           , "CMS", ".*root", json)
SingleElectron_Run2016D_03Feb2017 = kreator.makeDataComponent("SingleElectron_Run2016D_03Feb2017", "/SingleElectron/Run2016D-03Feb2017-v1/MINIAOD", "CMS", ".*root", json)
SingleMuon_Run2016D_03Feb2017     = kreator.makeDataComponent("SingleMuon_Run2016D_03Feb2017"    , "/SingleMuon/Run2016D-03Feb2017-v1/MINIAOD"    , "CMS", ".*root", json)
SinglePhoton_Run2016D_03Feb2017   = kreator.makeDataComponent("SinglePhoton_Run2016D_03Feb2017"  , "/SinglePhoton/Run2016D-03Feb2017-v1/MINIAOD"  , "CMS", ".*root", json)
DoubleEG_Run2016D_03Feb2017       = kreator.makeDataComponent("DoubleEG_Run2016D_03Feb2017"      , "/DoubleEG/Run2016D-03Feb2017-v1/MINIAOD"      , "CMS", ".*root", json)
MuonEG_Run2016D_03Feb2017         = kreator.makeDataComponent("MuonEG_Run2016D_03Feb2017"        , "/MuonEG/Run2016D-03Feb2017-v1/MINIAOD"        , "CMS", ".*root", json)
DoubleMuon_Run2016D_03Feb2017     = kreator.makeDataComponent("DoubleMuon_Run2016D_03Feb2017"    , "/DoubleMuon/Run2016D-03Feb2017-v1/MINIAOD"    , "CMS", ".*root", json)
Tau_Run2016D_03Feb2017            = kreator.makeDataComponent("Tau_Run2016D_03Feb2017"           , "/Tau/Run2016D-03Feb2017-v1/MINIAOD"           , "CMS", ".*root", json)

dataSamples_Run2016D_03Feb2017 = [JetHT_Run2016D_03Feb2017, HTMHT_Run2016D_03Feb2017, MET_Run2016D_03Feb2017, SingleElectron_Run2016D_03Feb2017, SingleMuon_Run2016D_03Feb2017, SinglePhoton_Run2016D_03Feb2017, DoubleEG_Run2016D_03Feb2017, MuonEG_Run2016D_03Feb2017, DoubleMuon_Run2016D_03Feb2017, Tau_Run2016D_03Feb2017]

### ----------------------------- Run2016E 03Feb2017 v2 ----------------------------------------

JetHT_Run2016E_03Feb2017          = kreator.makeDataComponent("JetHT_Run2016E_03Feb2017"         , "/JetHT/Run2016E-03Feb2017-v1/MINIAOD"         , "CMS", ".*root", json)
HTMHT_Run2016E_03Feb2017          = kreator.makeDataComponent("HTMHT_Run2016E_03Feb2017"         , "/HTMHT/Run2016E-03Feb2017-v1/MINIAOD"         , "CMS", ".*root", json)
MET_Run2016E_03Feb2017            = kreator.makeDataComponent("MET_Run2016E_03Feb2017"           , "/MET/Run2016E-03Feb2017-v1/MINIAOD"           , "CMS", ".*root", json)
SingleElectron_Run2016E_03Feb2017 = kreator.makeDataComponent("SingleElectron_Run2016E_03Feb2017", "/SingleElectron/Run2016E-03Feb2017-v1/MINIAOD", "CMS", ".*root", json)
SingleMuon_Run2016E_03Feb2017     = kreator.makeDataComponent("SingleMuon_Run2016E_03Feb2017"    , "/SingleMuon/Run2016E-03Feb2017-v1/MINIAOD"    , "CMS", ".*root", json)
SinglePhoton_Run2016E_03Feb2017   = kreator.makeDataComponent("SinglePhoton_Run2016E_03Feb2017"  , "/SinglePhoton/Run2016E-03Feb2017-v1/MINIAOD"  , "CMS", ".*root", json)
DoubleEG_Run2016E_03Feb2017       = kreator.makeDataComponent("DoubleEG_Run2016E_03Feb2017"      , "/DoubleEG/Run2016E-03Feb2017-v1/MINIAOD"      , "CMS", ".*root", json)
MuonEG_Run2016E_03Feb2017         = kreator.makeDataComponent("MuonEG_Run2016E_03Feb2017"        , "/MuonEG/Run2016E-03Feb2017-v1/MINIAOD"        , "CMS", ".*root", json)
DoubleMuon_Run2016E_03Feb2017     = kreator.makeDataComponent("DoubleMuon_Run2016E_03Feb2017"    , "/DoubleMuon/Run2016E-03Feb2017-v1/MINIAOD"    , "CMS", ".*root", json)
Tau_Run2016E_03Feb2017            = kreator.makeDataComponent("Tau_Run2016E_03Feb2017"           , "/Tau/Run2016E-03Feb2017-v1/MINIAOD"           , "CMS", ".*root", json)

dataSamples_Run2016E_03Feb2017 = [JetHT_Run2016E_03Feb2017, HTMHT_Run2016E_03Feb2017, MET_Run2016E_03Feb2017, SingleElectron_Run2016E_03Feb2017, SingleMuon_Run2016E_03Feb2017, SinglePhoton_Run2016E_03Feb2017, DoubleEG_Run2016E_03Feb2017, MuonEG_Run2016E_03Feb2017, DoubleMuon_Run2016E_03Feb2017, Tau_Run2016E_03Feb2017]


### ----------------------------- Run2016F 03Feb2017 v1 ----------------------------------------

JetHT_Run2016F_03Feb2017          = kreator.makeDataComponent("JetHT_Run2016F_03Feb2017"         , "/JetHT/Run2016F-03Feb2017-v1/MINIAOD"         , "CMS", ".*root", json)
HTMHT_Run2016F_03Feb2017          = kreator.makeDataComponent("HTMHT_Run2016F_03Feb2017"         , "/HTMHT/Run2016F-03Feb2017-v1/MINIAOD"         , "CMS", ".*root", json)
MET_Run2016F_03Feb2017            = kreator.makeDataComponent("MET_Run2016F_03Feb2017"           , "/MET/Run2016F-03Feb2017-v1/MINIAOD"           , "CMS", ".*root", json)
SingleElectron_Run2016F_03Feb2017 = kreator.makeDataComponent("SingleElectron_Run2016F_03Feb2017", "/SingleElectron/Run2016F-03Feb2017-v1/MINIAOD", "CMS", ".*root", json)
SingleMuon_Run2016F_03Feb2017     = kreator.makeDataComponent("SingleMuon_Run2016F_03Feb2017"    , "/SingleMuon/Run2016F-03Feb2017-v1/MINIAOD"    , "CMS", ".*root", json)
SinglePhoton_Run2016F_03Feb2017   = kreator.makeDataComponent("SinglePhoton_Run2016F_03Feb2017"  , "/SinglePhoton/Run2016F-03Feb2017-v1/MINIAOD"  , "CMS", ".*root", json)
DoubleEG_Run2016F_03Feb2017       = kreator.makeDataComponent("DoubleEG_Run2016F_03Feb2017"      , "/DoubleEG/Run2016F-03Feb2017-v1/MINIAOD"      , "CMS", ".*root", json)
MuonEG_Run2016F_03Feb2017         = kreator.makeDataComponent("MuonEG_Run2016F_03Feb2017"        , "/MuonEG/Run2016F-03Feb2017-v1/MINIAOD"        , "CMS", ".*root", json)
DoubleMuon_Run2016F_03Feb2017     = kreator.makeDataComponent("DoubleMuon_Run2016F_03Feb2017"    , "/DoubleMuon/Run2016F-03Feb2017-v1/MINIAOD"    , "CMS", ".*root", json)
Tau_Run2016F_03Feb2017            = kreator.makeDataComponent("Tau_Run2016F_03Feb2017"           , "/Tau/Run2016F-03Feb2017-v1/MINIAOD"           , "CMS", ".*root", json)

dataSamples_Run2016F_03Feb2017 = [JetHT_Run2016F_03Feb2017, HTMHT_Run2016F_03Feb2017, MET_Run2016F_03Feb2017, SingleElectron_Run2016F_03Feb2017, SingleMuon_Run2016F_03Feb2017, SinglePhoton_Run2016F_03Feb2017, DoubleEG_Run2016F_03Feb2017, MuonEG_Run2016F_03Feb2017, DoubleMuon_Run2016F_03Feb2017, Tau_Run2016F_03Feb2017]

### ----------------------------- Run2016G 03Feb2017 v1 ----------------------------------------

JetHT_Run2016G_03Feb2017          = kreator.makeDataComponent("JetHT_Run2016G_03Feb2017"         , "/JetHT/Run2016G-03Feb2017-v1/MINIAOD"         , "CMS", ".*root", json)
HTMHT_Run2016G_03Feb2017          = kreator.makeDataComponent("HTMHT_Run2016G_03Feb2017"         , "/HTMHT/Run2016G-03Feb2017-v1/MINIAOD"         , "CMS", ".*root", json)
MET_Run2016G_03Feb2017            = kreator.makeDataComponent("MET_Run2016G_03Feb2017"           , "/MET/Run2016G-03Feb2017-v1/MINIAOD"           , "CMS", ".*root", json)
SingleElectron_Run2016G_03Feb2017 = kreator.makeDataComponent("SingleElectron_Run2016G_03Feb2017", "/SingleElectron/Run2016G-03Feb2017-v1/MINIAOD", "CMS", ".*root", json)
SingleMuon_Run2016G_03Feb2017     = kreator.makeDataComponent("SingleMuon_Run2016G_03Feb2017"    , "/SingleMuon/Run2016G-03Feb2017-v1/MINIAOD"    , "CMS", ".*root", json)
SinglePhoton_Run2016G_03Feb2017   = kreator.makeDataComponent("SinglePhoton_Run2016G_03Feb2017"  , "/SinglePhoton/Run2016G-03Feb2017-v1/MINIAOD"  , "CMS", ".*root", json)
DoubleEG_Run2016G_03Feb2017       = kreator.makeDataComponent("DoubleEG_Run2016G_03Feb2017"      , "/DoubleEG/Run2016G-03Feb2017-v1/MINIAOD"      , "CMS", ".*root", json)
MuonEG_Run2016G_03Feb2017        = kreator.makeDataComponent("MuonEG_Run2016G_03Feb2017"        , "/MuonEG/Run2016G-03Feb2017-v1/MINIAOD"        , "CMS", ".*root", json)
DoubleMuon_Run2016G_03Feb2017     = kreator.makeDataComponent("DoubleMuon_Run2016G_03Feb2017"    , "/DoubleMuon/Run2016G-03Feb2017-v1/MINIAOD"    , "CMS", ".*root", json)
Tau_Run2016G_03Feb2017     = kreator.makeDataComponent("Tau_Run2016G_03Feb2017"    , "/Tau/Run2016G-03Feb2017-v1/MINIAOD"    , "CMS", ".*root", json)

dataSamples_Run2016G_03Feb2017 = [JetHT_Run2016G_03Feb2017, HTMHT_Run2016G_03Feb2017, MET_Run2016G_03Feb2017, SingleElectron_Run2016G_03Feb2017, SingleMuon_Run2016G_03Feb2017, SinglePhoton_Run2016G_03Feb2017, DoubleEG_Run2016G_03Feb2017, MuonEG_Run2016G_03Feb2017, DoubleMuon_Run2016G_03Feb2017, Tau_Run2016G_03Feb2017]

### ----------------------------- Run2016H 03Feb2017_ver2-v1 ----------------------------------------

JetHT_Run2016H_03Feb2017_v2          = kreator.makeDataComponent("JetHT_Run2016H_03Feb2017_v2"         , "/JetHT/Run2016H-03Feb2017_ver2-v1/MINIAOD"         , "CMS", ".*root", json)
HTMHT_Run2016H_03Feb2017_v2          = kreator.makeDataComponent("HTMHT_Run2016H_03Feb2017_v2"         , "/HTMHT/Run2016H-03Feb2017_ver2-v1/MINIAOD"         , "CMS", ".*root", json)
MET_Run2016H_03Feb2017_v2            = kreator.makeDataComponent("MET_Run2016H_03Feb2017_v2"           , "/MET/Run2016H-03Feb2017_ver2-v1/MINIAOD"           , "CMS", ".*root", json)
SingleElectron_Run2016H_03Feb2017_v2 = kreator.makeDataComponent("SingleElectron_Run2016H_03Feb2017_v2", "/SingleElectron/Run2016H-03Feb2017_ver2-v1/MINIAOD", "CMS", ".*root", json)
SingleMuon_Run2016H_03Feb2017_v2     = kreator.makeDataComponent("SingleMuon_Run2016H_03Feb2017_v2"    , "/SingleMuon/Run2016H-03Feb2017_ver2-v1/MINIAOD"    , "CMS", ".*root", json)
SinglePhoton_Run2016H_03Feb2017_v2   = kreator.makeDataComponent("SinglePhoton_Run2016H_03Feb2017_v2"  , "/SinglePhoton/Run2016H-03Feb2017_ver2-v1/MINIAOD"  , "CMS", ".*root", json)
DoubleEG_Run2016H_03Feb2017_v2       = kreator.makeDataComponent("DoubleEG_Run2016H_03Feb2017_v2"      , "/DoubleEG/Run2016H-03Feb2017_ver2-v1/MINIAOD"      , "CMS", ".*root", json)
MuonEG_Run2016H_03Feb2017_v2        = kreator.makeDataComponent("MuonEG_Run2016H_03Feb2017_v2"        , "/MuonEG/Run2016H-03Feb2017_ver2-v1/MINIAOD"        , "CMS", ".*root", json)
DoubleMuon_Run2016H_03Feb2017_v2     = kreator.makeDataComponent("DoubleMuon_Run2016H_03Feb2017_v2"    , "/DoubleMuon/Run2016H-03Feb2017_ver2-v1/MINIAOD"    , "CMS", ".*root", json)
Tau_Run2016H_03Feb2017_v2     = kreator.makeDataComponent("Tau_Run2016H_03Feb2017_v2"    , "/Tau/Run2016H-03Feb2017_ver2-v1/MINIAOD"    , "CMS", ".*root", json)

dataSamples_Run2016H_03Feb2017_v2 = [JetHT_Run2016H_03Feb2017_v2, HTMHT_Run2016H_03Feb2017_v2, MET_Run2016H_03Feb2017_v2, SingleElectron_Run2016H_03Feb2017_v2, SingleMuon_Run2016H_03Feb2017_v2, SinglePhoton_Run2016H_03Feb2017_v2, DoubleEG_Run2016H_03Feb2017_v2, MuonEG_Run2016H_03Feb2017_v2, DoubleMuon_Run2016H_03Feb2017_v2, Tau_Run2016H_03Feb2017_v2]

### ----------------------------- Run2016H 03Feb2017_ver3-v1 ----------------------------------------

JetHT_Run2016H_03Feb2017_v3          = kreator.makeDataComponent("JetHT_Run2016H_03Feb2017_v3"         , "/JetHT/Run2016H-03Feb2017_ver3-v1/MINIAOD"         , "CMS", ".*root", json)
HTMHT_Run2016H_03Feb2017_v3          = kreator.makeDataComponent("HTMHT_Run2016H_03Feb2017_v3"         , "/HTMHT/Run2016H-03Feb2017_ver3-v1/MINIAOD"         , "CMS", ".*root", json)
MET_Run2016H_03Feb2017_v3            = kreator.makeDataComponent("MET_Run2016H_03Feb2017_v3"           , "/MET/Run2016H-03Feb2017_ver3-v1/MINIAOD"           , "CMS", ".*root", json)
SingleElectron_Run2016H_03Feb2017_v3 = kreator.makeDataComponent("SingleElectron_Run2016H_03Feb2017_v3", "/SingleElectron/Run2016H-03Feb2017_ver3-v1/MINIAOD", "CMS", ".*root", json)
SingleMuon_Run2016H_03Feb2017_v3     = kreator.makeDataComponent("SingleMuon_Run2016H_03Feb2017_v3"    , "/SingleMuon/Run2016H-03Feb2017_ver3-v1/MINIAOD"    , "CMS", ".*root", json)
SinglePhoton_Run2016H_03Feb2017_v3   = kreator.makeDataComponent("SinglePhoton_Run2016H_03Feb2017_v3"  , "/SinglePhoton/Run2016H-03Feb2017_ver3-v1/MINIAOD"  , "CMS", ".*root", json)
DoubleEG_Run2016H_03Feb2017_v3       = kreator.makeDataComponent("DoubleEG_Run2016H_03Feb2017_v3"      , "/DoubleEG/Run2016H-03Feb2017_ver3-v1/MINIAOD"      , "CMS", ".*root", json)
MuonEG_Run2016H_03Feb2017_v3        = kreator.makeDataComponent("MuonEG_Run2016H_03Feb2017_v3"        , "/MuonEG/Run2016H-03Feb2017_ver3-v1/MINIAOD"        , "CMS", ".*root", json)
DoubleMuon_Run2016H_03Feb2017_v3     = kreator.makeDataComponent("DoubleMuon_Run2016H_03Feb2017_v3"    , "/DoubleMuon/Run2016H-03Feb2017_ver3-v1/MINIAOD"    , "CMS", ".*root", json)
Tau_Run2016H_03Feb2017_v3     = kreator.makeDataComponent("Tau_Run2016H_03Feb2017_v3"    , "/Tau/Run2016H-03Feb2017_ver3-v1/MINIAOD"    , "CMS", ".*root", json)

dataSamples_Run2016H_03Feb2017_v3 = [JetHT_Run2016H_03Feb2017_v3, HTMHT_Run2016H_03Feb2017_v3, MET_Run2016H_03Feb2017_v3, SingleElectron_Run2016H_03Feb2017_v3, SingleMuon_Run2016H_03Feb2017_v3, SinglePhoton_Run2016H_03Feb2017_v3, DoubleEG_Run2016H_03Feb2017_v3, MuonEG_Run2016H_03Feb2017_v3, DoubleMuon_Run2016H_03Feb2017_v3, Tau_Run2016H_03Feb2017_v3]

### Summary of 03Feb2017
dataSamples_03Feb2017 = dataSamples_Run2016B_03Feb2017_v2 + dataSamples_Run2016C_03Feb2017 + dataSamples_Run2016D_03Feb2017 + dataSamples_Run2016E_03Feb2017 + dataSamples_Run2016F_03Feb2017 + dataSamples_Run2016G_03Feb2017 + dataSamples_Run2016H_03Feb2017_v2 + dataSamples_Run2016H_03Feb2017_v3


### ----------------------------- Run2016B (raw v2) 17Jul2018 ----------------------------------------

JetHT_Run2016B_17Jul2018       = kreator.makeDataComponent("JetHT_Run2016B_17Jul2018"      , "/JetHT/Run2016B-17Jul2018_ver2-v2/MINIAOD"         , "CMS", ".*root", json)
HTMHT_Run2016B_17Jul2018       = kreator.makeDataComponent("HTMHT_Run2016B_17Jul2018"      , "/HTMHT/Run2016B-17Jul2018_ver2-v1/MINIAOD"         , "CMS", ".*root", json)
MET_Run2016B_17Jul2018         = kreator.makeDataComponent("MET_Run2016B_17Jul2018"        , "/MET/Run2016B-17Jul2018_ver2-v1/MINIAOD"           , "CMS", ".*root", json)
SingleElectron_Run2016B_17Jul2018 = kreator.makeDataComponent("SingleElectron_Run2016B_17Jul2018", "/SingleElectron/Run2016B-17Jul2018_ver2-v1/MINIAOD", "CMS", ".*root", json)
SingleMuon_Run2016B_17Jul2018  = kreator.makeDataComponent("SingleMuon_Run2016B_17Jul2018" , "/SingleMuon/Run2016B-17Jul2018_ver2-v1/MINIAOD"    , "CMS", ".*root", json)
SinglePhoton_Run2016B_17Jul2018= kreator.makeDataComponent("SinglePhoton_Run2016B_17Jul2018"  , "/SinglePhoton/Run2016B-17Jul2018_ver2-v1/MINIAOD"  , "CMS", ".*root", json)
DoubleEG_Run2016B_17Jul2018    = kreator.makeDataComponent("DoubleEG_Run2016B_17Jul2018"   , "/DoubleEG/Run2016B-17Jul2018_ver2-v1/MINIAOD"      , "CMS", ".*root", json)
MuonEG_Run2016B_17Jul2018     = kreator.makeDataComponent("MuonEG_Run2016B_17Jul2018"     , "/MuonEG/Run2016B-17Jul2018_ver2-v1/MINIAOD"        , "CMS", ".*root", json)
DoubleMuon_Run2016B_17Jul2018  = kreator.makeDataComponent("DoubleMuon_Run2016B_17Jul2018" , "/DoubleMuon/Run2016B-17Jul2018_ver2-v1/MINIAOD"    , "CMS", ".*root", json)
Tau_Run2016B_17Jul2018  = kreator.makeDataComponent("Tau_Run2016B_17Jul2018" , "/Tau/Run2016B-17Jul2018_ver2-v1/MINIAOD"    , "CMS", ".*root", json)

dataSamples_Run2016B_17Jul2018 = [JetHT_Run2016B_17Jul2018, HTMHT_Run2016B_17Jul2018, MET_Run2016B_17Jul2018, SingleElectron_Run2016B_17Jul2018, SingleMuon_Run2016B_17Jul2018, SinglePhoton_Run2016B_17Jul2018, DoubleEG_Run2016B_17Jul2018, MuonEG_Run2016B_17Jul2018, DoubleMuon_Run2016B_17Jul2018, Tau_Run2016B_17Jul2018]

### ----------------------------- Run2016C 17Jul2018 ----------------------------------------

JetHT_Run2016C_17Jul2018          = kreator.makeDataComponent("JetHT_Run2016C_17Jul2018"         , "/JetHT/Run2016C-17Jul2018-v1/MINIAOD"         , "CMS", ".*root", json)
HTMHT_Run2016C_17Jul2018          = kreator.makeDataComponent("HTMHT_Run2016C_17Jul2018"         , "/HTMHT/Run2016C-17Jul2018-v1/MINIAOD"         , "CMS", ".*root", json)
MET_Run2016C_17Jul2018            = kreator.makeDataComponent("MET_Run2016C_17Jul2018"           , "/MET/Run2016C-17Jul2018-v1/MINIAOD"           , "CMS", ".*root", json)
SingleElectron_Run2016C_17Jul2018 = kreator.makeDataComponent("SingleElectron_Run2016C_17Jul2018", "/SingleElectron/Run2016C-17Jul2018-v1/MINIAOD", "CMS", ".*root", json)
SingleMuon_Run2016C_17Jul2018     = kreator.makeDataComponent("SingleMuon_Run2016C_17Jul2018"    , "/SingleMuon/Run2016C-17Jul2018-v1/MINIAOD"    , "CMS", ".*root", json)
SinglePhoton_Run2016C_17Jul2018   = kreator.makeDataComponent("SinglePhoton_Run2016C_17Jul2018"  , "/SinglePhoton/Run2016C-17Jul2018-v1/MINIAOD"  , "CMS", ".*root", json)
DoubleEG_Run2016C_17Jul2018       = kreator.makeDataComponent("DoubleEG_Run2016C_17Jul2018"      , "/DoubleEG/Run2016C-17Jul2018-v1/MINIAOD"      , "CMS", ".*root", json)
MuonEG_Run2016C_17Jul2018         = kreator.makeDataComponent("MuonEG_Run2016C_17Jul2018"        , "/MuonEG/Run2016C-17Jul2018-v1/MINIAOD"        , "CMS", ".*root", json)
DoubleMuon_Run2016C_17Jul2018     = kreator.makeDataComponent("DoubleMuon_Run2016C_17Jul2018"    , "/DoubleMuon/Run2016C-17Jul2018-v1/MINIAOD"    , "CMS", ".*root", json)
Tau_Run2016C_17Jul2018            = kreator.makeDataComponent("Tau_Run2016C_17Jul2018"           , "/Tau/Run2016C-17Jul2018-v1/MINIAOD"           , "CMS", ".*root", json)

dataSamples_Run2016C_17Jul2018 = [JetHT_Run2016C_17Jul2018, HTMHT_Run2016C_17Jul2018, MET_Run2016C_17Jul2018, SingleElectron_Run2016C_17Jul2018, SingleMuon_Run2016C_17Jul2018, SinglePhoton_Run2016C_17Jul2018, DoubleEG_Run2016C_17Jul2018, MuonEG_Run2016C_17Jul2018, DoubleMuon_Run2016C_17Jul2018, Tau_Run2016C_17Jul2018]


### ----------------------------- Run2016D 17Jul2018 ----------------------------------------

JetHT_Run2016D_17Jul2018          = kreator.makeDataComponent("JetHT_Run2016D_17Jul2018"         , "/JetHT/Run2016D-17Jul2018-v1/MINIAOD"         , "CMS", ".*root", json)
HTMHT_Run2016D_17Jul2018          = kreator.makeDataComponent("HTMHT_Run2016D_17Jul2018"         , "/HTMHT/Run2016D-17Jul2018-v1/MINIAOD"         , "CMS", ".*root", json)
MET_Run2016D_17Jul2018            = kreator.makeDataComponent("MET_Run2016D_17Jul2018"           , "/MET/Run2016D-17Jul2018-v1/MINIAOD"           , "CMS", ".*root", json)
SingleElectron_Run2016D_17Jul2018 = kreator.makeDataComponent("SingleElectron_Run2016D_17Jul2018", "/SingleElectron/Run2016D-17Jul2018-v1/MINIAOD", "CMS", ".*root", json)
SingleMuon_Run2016D_17Jul2018     = kreator.makeDataComponent("SingleMuon_Run2016D_17Jul2018"    , "/SingleMuon/Run2016D-17Jul2018-v1/MINIAOD"    , "CMS", ".*root", json)
SinglePhoton_Run2016D_17Jul2018   = kreator.makeDataComponent("SinglePhoton_Run2016D_17Jul2018"  , "/SinglePhoton/Run2016D-17Jul2018-v1/MINIAOD"  , "CMS", ".*root", json)
DoubleEG_Run2016D_17Jul2018       = kreator.makeDataComponent("DoubleEG_Run2016D_17Jul2018"      , "/DoubleEG/Run2016D-17Jul2018-v1/MINIAOD"      , "CMS", ".*root", json)
MuonEG_Run2016D_17Jul2018         = kreator.makeDataComponent("MuonEG_Run2016D_17Jul2018"        , "/MuonEG/Run2016D-17Jul2018-v1/MINIAOD"        , "CMS", ".*root", json)
DoubleMuon_Run2016D_17Jul2018     = kreator.makeDataComponent("DoubleMuon_Run2016D_17Jul2018"    , "/DoubleMuon/Run2016D-17Jul2018-v1/MINIAOD"    , "CMS", ".*root", json)
Tau_Run2016D_17Jul2018            = kreator.makeDataComponent("Tau_Run2016D_17Jul2018"           , "/Tau/Run2016D-17Jul2018-v1/MINIAOD"           , "CMS", ".*root", json)

dataSamples_Run2016D_17Jul2018 = [JetHT_Run2016D_17Jul2018, HTMHT_Run2016D_17Jul2018, MET_Run2016D_17Jul2018, SingleElectron_Run2016D_17Jul2018, SingleMuon_Run2016D_17Jul2018, SinglePhoton_Run2016D_17Jul2018, DoubleEG_Run2016D_17Jul2018, MuonEG_Run2016D_17Jul2018, DoubleMuon_Run2016D_17Jul2018, Tau_Run2016D_17Jul2018]

### ----------------------------- Run2016E 17Jul2018 ----------------------------------------

JetHT_Run2016E_17Jul2018          = kreator.makeDataComponent("JetHT_Run2016E_17Jul2018"         , "/JetHT/Run2016E-17Jul2018-v1/MINIAOD"         , "CMS", ".*root", json)
HTMHT_Run2016E_17Jul2018          = kreator.makeDataComponent("HTMHT_Run2016E_17Jul2018"         , "/HTMHT/Run2016E-17Jul2018-v1/MINIAOD"         , "CMS", ".*root", json)
MET_Run2016E_17Jul2018            = kreator.makeDataComponent("MET_Run2016E_17Jul2018"           , "/MET/Run2016E-17Jul2018-v1/MINIAOD"           , "CMS", ".*root", json)
SingleElectron_Run2016E_17Jul2018 = kreator.makeDataComponent("SingleElectron_Run2016E_17Jul2018", "/SingleElectron/Run2016E-17Jul2018-v1/MINIAOD", "CMS", ".*root", json)
SingleMuon_Run2016E_17Jul2018     = kreator.makeDataComponent("SingleMuon_Run2016E_17Jul2018"    , "/SingleMuon/Run2016E-17Jul2018-v1/MINIAOD"    , "CMS", ".*root", json)
SinglePhoton_Run2016E_17Jul2018   = kreator.makeDataComponent("SinglePhoton_Run2016E_17Jul2018"  , "/SinglePhoton/Run2016E-17Jul2018-v1/MINIAOD"  , "CMS", ".*root", json)
DoubleEG_Run2016E_17Jul2018       = kreator.makeDataComponent("DoubleEG_Run2016E_17Jul2018"      , "/DoubleEG/Run2016E-17Jul2018-v1/MINIAOD"      , "CMS", ".*root", json)
MuonEG_Run2016E_17Jul2018         = kreator.makeDataComponent("MuonEG_Run2016E_17Jul2018"        , "/MuonEG/Run2016E-17Jul2018-v2/MINIAOD"        , "CMS", ".*root", json)
DoubleMuon_Run2016E_17Jul2018     = kreator.makeDataComponent("DoubleMuon_Run2016E_17Jul2018"    , "/DoubleMuon/Run2016E-17Jul2018-v1/MINIAOD"    , "CMS", ".*root", json)
Tau_Run2016E_17Jul2018            = kreator.makeDataComponent("Tau_Run2016E_17Jul2018"           , "/Tau/Run2016E-17Jul2018-v1/MINIAOD"           , "CMS", ".*root", json)

dataSamples_Run2016E_17Jul2018 = [JetHT_Run2016E_17Jul2018, HTMHT_Run2016E_17Jul2018, MET_Run2016E_17Jul2018, SingleElectron_Run2016E_17Jul2018, SingleMuon_Run2016E_17Jul2018, SinglePhoton_Run2016E_17Jul2018, DoubleEG_Run2016E_17Jul2018, MuonEG_Run2016E_17Jul2018, DoubleMuon_Run2016E_17Jul2018, Tau_Run2016E_17Jul2018]


### ----------------------------- Run2016F 17Jul2018 ----------------------------------------

JetHT_Run2016F_17Jul2018          = kreator.makeDataComponent("JetHT_Run2016F_17Jul2018"         , "/JetHT/Run2016F-17Jul2018-v1/MINIAOD"         , "CMS", ".*root", json)
HTMHT_Run2016F_17Jul2018          = kreator.makeDataComponent("HTMHT_Run2016F_17Jul2018"         , "/HTMHT/Run2016F-17Jul2018-v1/MINIAOD"         , "CMS", ".*root", json)
MET_Run2016F_17Jul2018            = kreator.makeDataComponent("MET_Run2016F_17Jul2018"           , "/MET/Run2016F-17Jul2018-v1/MINIAOD"           , "CMS", ".*root", json)
SingleElectron_Run2016F_17Jul2018 = kreator.makeDataComponent("SingleElectron_Run2016F_17Jul2018", "/SingleElectron/Run2016F-17Jul2018-v1/MINIAOD", "CMS", ".*root", json)
SingleMuon_Run2016F_17Jul2018     = kreator.makeDataComponent("SingleMuon_Run2016F_17Jul2018"    , "/SingleMuon/Run2016F-17Jul2018-v1/MINIAOD"    , "CMS", ".*root", json)
SinglePhoton_Run2016F_17Jul2018   = kreator.makeDataComponent("SinglePhoton_Run2016F_17Jul2018"  , "/SinglePhoton/Run2016F-17Jul2018-v1/MINIAOD"  , "CMS", ".*root", json)
DoubleEG_Run2016F_17Jul2018       = kreator.makeDataComponent("DoubleEG_Run2016F_17Jul2018"      , "/DoubleEG/Run2016F-17Jul2018-v1/MINIAOD"      , "CMS", ".*root", json)
MuonEG_Run2016F_17Jul2018         = kreator.makeDataComponent("MuonEG_Run2016F_17Jul2018"        , "/MuonEG/Run2016F-17Jul2018-v1/MINIAOD"        , "CMS", ".*root", json)
DoubleMuon_Run2016F_17Jul2018     = kreator.makeDataComponent("DoubleMuon_Run2016F_17Jul2018"    , "/DoubleMuon/Run2016F-17Jul2018-v1/MINIAOD"    , "CMS", ".*root", json)
Tau_Run2016F_17Jul2018            = kreator.makeDataComponent("Tau_Run2016F_17Jul2018"           , "/Tau/Run2016F-17Jul2018-v1/MINIAOD"           , "CMS", ".*root", json)

dataSamples_Run2016F_17Jul2018 = [JetHT_Run2016F_17Jul2018, HTMHT_Run2016F_17Jul2018, MET_Run2016F_17Jul2018, SingleElectron_Run2016F_17Jul2018, SingleMuon_Run2016F_17Jul2018, SinglePhoton_Run2016F_17Jul2018, DoubleEG_Run2016F_17Jul2018, MuonEG_Run2016F_17Jul2018, DoubleMuon_Run2016F_17Jul2018, Tau_Run2016F_17Jul2018]

### ----------------------------- Run2016G 17Jul2018 ----------------------------------------

JetHT_Run2016G_17Jul2018          = kreator.makeDataComponent("JetHT_Run2016G_17Jul2018"         , "/JetHT/Run2016G-17Jul2018-v1/MINIAOD"         , "CMS", ".*root", json)
HTMHT_Run2016G_17Jul2018          = kreator.makeDataComponent("HTMHT_Run2016G_17Jul2018"         , "/HTMHT/Run2016G-17Jul2018-v1/MINIAOD"         , "CMS", ".*root", json)
MET_Run2016G_17Jul2018            = kreator.makeDataComponent("MET_Run2016G_17Jul2018"           , "/MET/Run2016G-17Jul2018-v1/MINIAOD"           , "CMS", ".*root", json)
SingleElectron_Run2016G_17Jul2018 = kreator.makeDataComponent("SingleElectron_Run2016G_17Jul2018", "/SingleElectron/Run2016G-17Jul2018-v1/MINIAOD", "CMS", ".*root", json)
SingleMuon_Run2016G_17Jul2018     = kreator.makeDataComponent("SingleMuon_Run2016G_17Jul2018"    , "/SingleMuon/Run2016G-17Jul2018-v1/MINIAOD"    , "CMS", ".*root", json)
SinglePhoton_Run2016G_17Jul2018   = kreator.makeDataComponent("SinglePhoton_Run2016G_17Jul2018"  , "/SinglePhoton/Run2016G-17Jul2018-v1/MINIAOD"  , "CMS", ".*root", json)
DoubleEG_Run2016G_17Jul2018       = kreator.makeDataComponent("DoubleEG_Run2016G_17Jul2018"      , "/DoubleEG/Run2016G-17Jul2018-v1/MINIAOD"      , "CMS", ".*root", json)
MuonEG_Run2016G_17Jul2018        = kreator.makeDataComponent("MuonEG_Run2016G_17Jul2018"        , "/MuonEG/Run2016G-17Jul2018-v1/MINIAOD"        , "CMS", ".*root", json)
DoubleMuon_Run2016G_17Jul2018     = kreator.makeDataComponent("DoubleMuon_Run2016G_17Jul2018"    , "/DoubleMuon/Run2016G-17Jul2018-v1/MINIAOD"    , "CMS", ".*root", json)
Tau_Run2016G_17Jul2018     = kreator.makeDataComponent("Tau_Run2016G_17Jul2018"    , "/Tau/Run2016G-17Jul2018-v1/MINIAOD"    , "CMS", ".*root", json)

dataSamples_Run2016G_17Jul2018 = [JetHT_Run2016G_17Jul2018, HTMHT_Run2016G_17Jul2018, MET_Run2016G_17Jul2018, SingleElectron_Run2016G_17Jul2018, SingleMuon_Run2016G_17Jul2018, SinglePhoton_Run2016G_17Jul2018, DoubleEG_Run2016G_17Jul2018, MuonEG_Run2016G_17Jul2018, DoubleMuon_Run2016G_17Jul2018, Tau_Run2016G_17Jul2018]

### ----------------------------- Run2016H 17Jul2018 ----------------------------------------

JetHT_Run2016H_17Jul2018          = kreator.makeDataComponent("JetHT_Run2016H_17Jul2018"         , "/JetHT/Run2016H-17Jul2018-v1/MINIAOD"         , "CMS", ".*root", json)
HTMHT_Run2016H_17Jul2018          = kreator.makeDataComponent("HTMHT_Run2016H_17Jul2018"         , "/HTMHT/Run2016H-17Jul2018-v1/MINIAOD"         , "CMS", ".*root", json)
MET_Run2016H_17Jul2018            = kreator.makeDataComponent("MET_Run2016H_17Jul2018"           , "/MET/Run2016H-17Jul2018-v2/MINIAOD"           , "CMS", ".*root", json)
SingleElectron_Run2016H_17Jul2018 = kreator.makeDataComponent("SingleElectron_Run2016H_17Jul2018", "/SingleElectron/Run2016H-17Jul2018-v1/MINIAOD", "CMS", ".*root", json)
SingleMuon_Run2016H_17Jul2018     = kreator.makeDataComponent("SingleMuon_Run2016H_17Jul2018"    , "/SingleMuon/Run2016H-17Jul2018-v1/MINIAOD"    , "CMS", ".*root", json)
SinglePhoton_Run2016H_17Jul2018   = kreator.makeDataComponent("SinglePhoton_Run2016H_17Jul2018"  , "/SinglePhoton/Run2016H-17Jul2018-v1/MINIAOD"  , "CMS", ".*root", json)
DoubleEG_Run2016H_17Jul2018       = kreator.makeDataComponent("DoubleEG_Run2016H_17Jul2018"      , "/DoubleEG/Run2016H-17Jul2018-v1/MINIAOD"      , "CMS", ".*root", json)
MuonEG_Run2016H_17Jul2018        = kreator.makeDataComponent("MuonEG_Run2016H_17Jul2018"        , "/MuonEG/Run2016H-17Jul2018-v1/MINIAOD"        , "CMS", ".*root", json)
DoubleMuon_Run2016H_17Jul2018     = kreator.makeDataComponent("DoubleMuon_Run2016H_17Jul2018"    , "/DoubleMuon/Run2016H-17Jul2018-v1/MINIAOD"    , "CMS", ".*root", json)
Tau_Run2016H_17Jul2018     = kreator.makeDataComponent("Tau_Run2016H_17Jul2018"    , "/Tau/Run2016H-17Jul2018-v1/MINIAOD"    , "CMS", ".*root", json)

dataSamples_Run2016H_17Jul2018 = [JetHT_Run2016H_17Jul2018, HTMHT_Run2016H_17Jul2018, MET_Run2016H_17Jul2018, SingleElectron_Run2016H_17Jul2018, SingleMuon_Run2016H_17Jul2018, SinglePhoton_Run2016H_17Jul2018, DoubleEG_Run2016H_17Jul2018, MuonEG_Run2016H_17Jul2018, DoubleMuon_Run2016H_17Jul2018, Tau_Run2016H_17Jul2018]


### Summary of 17Jul2018
dataSamples_17Jul2018 = dataSamples_Run2016B_17Jul2018 + dataSamples_Run2016C_17Jul2018 + dataSamples_Run2016D_17Jul2018 + dataSamples_Run2016E_17Jul2018 + dataSamples_Run2016F_17Jul2018 + dataSamples_Run2016G_17Jul2018 + dataSamples_Run2016H_17Jul2018


dataSamples = dataSamples_PromptReco + dataSamples_23Sep2016 + dataSamples_03Feb2017 + dataSamples_17Jul2018
samples = dataSamples

### ---------------------------------------------------------------------
if __name__ == "__main__":
    from CMGTools.RootTools.samples.tools import runMain
    runMain(samples, localobjs=locals())
