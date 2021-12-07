from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()

json='/work/sesanche/FRs/CMSSW_10_4_0/src/CMGTools/RootTools/python/samples/Cert_271036-284044_13TeV_ReReco_07Aug2017_Collisions16_JSON.txt'

### ----------------------------- UL16 Run2016Bv1 HIPM  ----------------------------------------

JetHT_Run2016Bv1_HIPM_UL16          = kreator.makeDataComponent("JetHT_Run2016Bv1_HIPM_UL16"         , "/JetHT/Run2016B-ver1_HIPM_UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD"         , "CMS", ".*root", json)
HTMHT_Run2016Bv1_HIPM_UL16          = kreator.makeDataComponent("HTMHT_Run2016Bv1_HIPM_UL16"         , "/HTMHT/Run2016B-ver1_HIPM_UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD"         , "CMS", ".*root", json)
MET_Run2016Bv1_HIPM_UL16            = kreator.makeDataComponent("MET_Run2016Bv1_HIPM_UL16"           , "/MET/Run2016B-ver1_HIPM_UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD"           , "CMS", ".*root", json)
SingleElectron_Run2016Bv1_HIPM_UL16 = kreator.makeDataComponent("SingleElectron_Run2016Bv1_HIPM_UL16", "/SingleElectron/Run2016B-ver1_HIPM_UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2016Bv1_HIPM_UL16     = kreator.makeDataComponent("SingleMuon_Run2016Bv1_HIPM_UL16"    , "/SingleMuon/Run2016B-ver1_HIPM_UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD"    , "CMS", ".*root", json)
SinglePhoton_Run2016Bv1_HIPM_UL16   = kreator.makeDataComponent("SinglePhoton_Run2016Bv1_HIPM_UL16"  , "/SinglePhoton/Run2016B-ver1_HIPM_UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD"  , "CMS", ".*root", json)
DoubleEG_Run2016Bv1_HIPM_UL16       = kreator.makeDataComponent("DoubleEG_Run2016Bv1_HIPM_UL16"      , "/DoubleEG/Run2016B-ver1_HIPM_UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD"      , "CMS", ".*root", json)
MuonEG_Run2016Bv1_HIPM_UL16         = kreator.makeDataComponent("MuonEG_Run2016Bv1_HIPM_UL16"        , "/MuonEG/Run2016B-ver1_HIPM_UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD"        , "CMS", ".*root", json)
DoubleMuon_Run2016Bv1_HIPM_UL16     = kreator.makeDataComponent("DoubleMuon_Run2016Bv1_HIPM_UL16"    , "/DoubleMuon/Run2016B-ver1_HIPM_UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD"    , "CMS", ".*root", json)
Tau_Run2016Bv1_HIPM_UL16            = kreator.makeDataComponent("Tau_Run2016Bv1_HIPM_UL16"           , "/Tau/Run2016B-ver1_HIPM_UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD"    , "CMS", ".*root", json)

dataSamples_Run2016Bv1_HIPM_UL16 = [JetHT_Run2016Bv1_HIPM_UL16,HTMHT_Run2016Bv1_HIPM_UL16,MET_Run2016Bv1_HIPM_UL16,SingleElectron_Run2016Bv1_HIPM_UL16,SingleMuon_Run2016Bv1_HIPM_UL16,SinglePhoton_Run2016Bv1_HIPM_UL16,DoubleEG_Run2016Bv1_HIPM_UL16,MuonEG_Run2016Bv1_HIPM_UL16,DoubleMuon_Run2016Bv1_HIPM_UL16,Tau_Run2016Bv1_HIPM_UL16]

### ----------------------------- UL16 Run2016Bv2 HIPM  ----------------------------------------

JetHT_Run2016Bv2_HIPM_UL16          = kreator.makeDataComponent("JetHT_Run2016Bv2_HIPM_UL16"         , "/JetHT/Run2016B-ver2_HIPM_UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD"         , "CMS", ".*root", json)
HTMHT_Run2016Bv2_HIPM_UL16          = kreator.makeDataComponent("HTMHT_Run2016Bv2_HIPM_UL16"         , "/HTMHT/Run2016B-ver2_HIPM_UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD"         , "CMS", ".*root", json)
MET_Run2016Bv2_HIPM_UL16            = kreator.makeDataComponent("MET_Run2016Bv2_HIPM_UL16"           , "/MET/Run2016B-ver2_HIPM_UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD"           , "CMS", ".*root", json)
SingleElectron_Run2016Bv2_HIPM_UL16 = kreator.makeDataComponent("SingleElectron_Run2016Bv2_HIPM_UL16", "/SingleElectron/Run2016B-ver2_HIPM_UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2016Bv2_HIPM_UL16     = kreator.makeDataComponent("SingleMuon_Run2016Bv2_HIPM_UL16"    , "/SingleMuon/Run2016B-ver2_HIPM_UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD"    , "CMS", ".*root", json)
SinglePhoton_Run2016Bv2_HIPM_UL16   = kreator.makeDataComponent("SinglePhoton_Run2016Bv2_HIPM_UL16"  , "/SinglePhoton/Run2016B-ver2_HIPM_UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD"  , "CMS", ".*root", json)
#DoubleEG_Run2016Bv2_HIPM_UL16       = kreator.makeDataComponent("DoubleEG_Run2016Bv2_HIPM_UL16"      , "/DoubleEG/Run2016B-ver2_HIPM_UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD"      , "CMS", ".*root", json)
MuonEG_Run2016Bv2_HIPM_UL16         = kreator.makeDataComponent("MuonEG_Run2016Bv2_HIPM_UL16"        , "/MuonEG/Run2016B-ver2_HIPM_UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD"        , "CMS", ".*root", json)
DoubleMuon_Run2016Bv2_HIPM_UL16     = kreator.makeDataComponent("DoubleMuon_Run2016Bv2_HIPM_UL16"    , "/DoubleMuon/Run2016B-ver2_HIPM_UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD"    , "CMS", ".*root", json)
Tau_Run2016Bv2_HIPM_UL16            = kreator.makeDataComponent("Tau_Run2016Bv2_HIPM_UL16"           , "/Tau/Run2016B-ver2_HIPM_UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD"    , "CMS", ".*root", json)

dataSamples_Run2016Bv2_HIPM_UL16 = [JetHT_Run2016Bv2_HIPM_UL16,HTMHT_Run2016Bv2_HIPM_UL16,MET_Run2016Bv2_HIPM_UL16,SingleElectron_Run2016Bv2_HIPM_UL16,SingleMuon_Run2016Bv2_HIPM_UL16,SinglePhoton_Run2016Bv2_HIPM_UL16,MuonEG_Run2016Bv2_HIPM_UL16,DoubleMuon_Run2016Bv2_HIPM_UL16,Tau_Run2016Bv2_HIPM_UL16] # ,DoubleEG_Run2016Bv2_HIPM_UL16

### ----------------------------- UL16 Run2016C HIPM  ----------------------------------------

JetHT_Run2016C_HIPM_UL16          = kreator.makeDataComponent("JetHT_Run2016C_HIPM_UL16"         , "/JetHT/Run2016C-HIPM_UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD"         , "CMS", ".*root", json)
HTMHT_Run2016C_HIPM_UL16          = kreator.makeDataComponent("HTMHT_Run2016C_HIPM_UL16"         , "/HTMHT/Run2016C-HIPM_UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD"         , "CMS", ".*root", json)
MET_Run2016C_HIPM_UL16            = kreator.makeDataComponent("MET_Run2016C_HIPM_UL16"           , "/MET/Run2016C-HIPM_UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD"           , "CMS", ".*root", json)
SingleElectron_Run2016C_HIPM_UL16 = kreator.makeDataComponent("SingleElectron_Run2016C_HIPM_UL16", "/SingleElectron/Run2016C-HIPM_UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2016C_HIPM_UL16     = kreator.makeDataComponent("SingleMuon_Run2016C_HIPM_UL16"    , "/SingleMuon/Run2016C-HIPM_UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD"    , "CMS", ".*root", json)
SinglePhoton_Run2016C_HIPM_UL16   = kreator.makeDataComponent("SinglePhoton_Run2016C_HIPM_UL16"  , "/SinglePhoton/Run2016C-HIPM_UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD"  , "CMS", ".*root", json)
DoubleEG_Run2016C_HIPM_UL16       = kreator.makeDataComponent("DoubleEG_Run2016C_HIPM_UL16"      , "/DoubleEG/Run2016C-HIPM_UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD"      , "CMS", ".*root", json)
MuonEG_Run2016C_HIPM_UL16         = kreator.makeDataComponent("MuonEG_Run2016C_HIPM_UL16"        , "/MuonEG/Run2016C-HIPM_UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD"        , "CMS", ".*root", json)
DoubleMuon_Run2016C_HIPM_UL16     = kreator.makeDataComponent("DoubleMuon_Run2016C_HIPM_UL16"    , "/DoubleMuon/Run2016C-HIPM_UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD"    , "CMS", ".*root", json)
Tau_Run2016C_HIPM_UL16            = kreator.makeDataComponent("Tau_Run2016C_HIPM_UL16"           , "/Tau/Run2016C-HIPM_UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD"    , "CMS", ".*root", json)

dataSamples_Run2016C_HIPM_UL16 = [JetHT_Run2016C_HIPM_UL16,HTMHT_Run2016C_HIPM_UL16,MET_Run2016C_HIPM_UL16,SingleElectron_Run2016C_HIPM_UL16,SingleMuon_Run2016C_HIPM_UL16,SinglePhoton_Run2016C_HIPM_UL16,DoubleEG_Run2016C_HIPM_UL16,MuonEG_Run2016C_HIPM_UL16,DoubleMuon_Run2016C_HIPM_UL16,Tau_Run2016C_HIPM_UL16]

### ----------------------------- UL16 Run2016D HIPM  ----------------------------------------

JetHT_Run2016D_HIPM_UL16          = kreator.makeDataComponent("JetHT_Run2016D_HIPM_UL16"         , "/JetHT/Run2016D-HIPM_UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD"         , "CMS", ".*root", json)
HTMHT_Run2016D_HIPM_UL16          = kreator.makeDataComponent("HTMHT_Run2016D_HIPM_UL16"         , "/HTMHT/Run2016D-HIPM_UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD"         , "CMS", ".*root", json)
MET_Run2016D_HIPM_UL16            = kreator.makeDataComponent("MET_Run2016D_HIPM_UL16"           , "/MET/Run2016D-HIPM_UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD"           , "CMS", ".*root", json)
SingleElectron_Run2016D_HIPM_UL16 = kreator.makeDataComponent("SingleElectron_Run2016D_HIPM_UL16", "/SingleElectron/Run2016D-HIPM_UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2016D_HIPM_UL16     = kreator.makeDataComponent("SingleMuon_Run2016D_HIPM_UL16"    , "/SingleMuon/Run2016D-HIPM_UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD"    , "CMS", ".*root", json)
SinglePhoton_Run2016D_HIPM_UL16   = kreator.makeDataComponent("SinglePhoton_Run2016D_HIPM_UL16"  , "/SinglePhoton/Run2016D-HIPM_UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD"  , "CMS", ".*root", json)
DoubleEG_Run2016D_HIPM_UL16       = kreator.makeDataComponent("DoubleEG_Run2016D_HIPM_UL16"      , "/DoubleEG/Run2016D-HIPM_UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD"      , "CMS", ".*root", json)
MuonEG_Run2016D_HIPM_UL16         = kreator.makeDataComponent("MuonEG_Run2016D_HIPM_UL16"        , "/MuonEG/Run2016D-HIPM_UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD"        , "CMS", ".*root", json)
DoubleMuon_Run2016D_HIPM_UL16     = kreator.makeDataComponent("DoubleMuon_Run2016D_HIPM_UL16"    , "/DoubleMuon/Run2016D-HIPM_UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD"    , "CMS", ".*root", json)
Tau_Run2016D_HIPM_UL16            = kreator.makeDataComponent("Tau_Run2016D_HIPM_UL16"           , "/Tau/Run2016D-HIPM_UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD"    , "CMS", ".*root", json)

dataSamples_Run2016D_HIPM_UL16 = [JetHT_Run2016D_HIPM_UL16,HTMHT_Run2016D_HIPM_UL16,MET_Run2016D_HIPM_UL16,SingleElectron_Run2016D_HIPM_UL16,SingleMuon_Run2016D_HIPM_UL16,SinglePhoton_Run2016D_HIPM_UL16,DoubleEG_Run2016D_HIPM_UL16,MuonEG_Run2016D_HIPM_UL16,DoubleMuon_Run2016D_HIPM_UL16,Tau_Run2016D_HIPM_UL16]

### ----------------------------- UL16 Run2016E HIPM  ----------------------------------------

JetHT_Run2016E_HIPM_UL16          = kreator.makeDataComponent("JetHT_Run2016E_HIPM_UL16"         , "/JetHT/Run2016E-HIPM_UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD"         , "CMS", ".*root", json)
HTMHT_Run2016E_HIPM_UL16          = kreator.makeDataComponent("HTMHT_Run2016E_HIPM_UL16"         , "/HTMHT/Run2016E-HIPM_UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD"         , "CMS", ".*root", json)
MET_Run2016E_HIPM_UL16            = kreator.makeDataComponent("MET_Run2016E_HIPM_UL16"           , "/MET/Run2016E-HIPM_UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD"           , "CMS", ".*root", json)
#SingleElectron_Run2016E_HIPM_UL16 = kreator.makeDataComponent("SingleElectron_Run2016E_HIPM_UL16", "/SingleElectron/Run2016E-HIPM_UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2016E_HIPM_UL16     = kreator.makeDataComponent("SingleMuon_Run2016E_HIPM_UL16"    , "/SingleMuon/Run2016E-HIPM_UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD"    , "CMS", ".*root", json)
SinglePhoton_Run2016E_HIPM_UL16   = kreator.makeDataComponent("SinglePhoton_Run2016E_HIPM_UL16"  , "/SinglePhoton/Run2016E-HIPM_UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD"  , "CMS", ".*root", json)
DoubleEG_Run2016E_HIPM_UL16       = kreator.makeDataComponent("DoubleEG_Run2016E_HIPM_UL16"      , "/DoubleEG/Run2016E-HIPM_UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD"      , "CMS", ".*root", json)
MuonEG_Run2016E_HIPM_UL16         = kreator.makeDataComponent("MuonEG_Run2016E_HIPM_UL16"        , "/MuonEG/Run2016E-HIPM_UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD"        , "CMS", ".*root", json)
DoubleMuon_Run2016E_HIPM_UL16     = kreator.makeDataComponent("DoubleMuon_Run2016E_HIPM_UL16"    , "/DoubleMuon/Run2016E-HIPM_UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD"    , "CMS", ".*root", json)
Tau_Run2016E_HIPM_UL16            = kreator.makeDataComponent("Tau_Run2016E_HIPM_UL16"           , "/Tau/Run2016E-HIPM_UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD"    , "CMS", ".*root", json)

dataSamples_Run2016E_HIPM_UL16 = [JetHT_Run2016E_HIPM_UL16,HTMHT_Run2016E_HIPM_UL16,MET_Run2016E_HIPM_UL16,SingleMuon_Run2016E_HIPM_UL16,SinglePhoton_Run2016E_HIPM_UL16,DoubleEG_Run2016E_HIPM_UL16,MuonEG_Run2016E_HIPM_UL16,DoubleMuon_Run2016E_HIPM_UL16,Tau_Run2016E_HIPM_UL16] # ,SingleElectron_Run2016E_HIPM_UL16


### ----------------------------- UL16 Run2016F HIPM  ----------------------------------------

JetHT_Run2016F_HIPM_UL16          = kreator.makeDataComponent("JetHT_Run2016F_HIPM_UL16"         , "/JetHT/Run2016F-HIPM_UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD"         , "CMS", ".*root", json)
HTMHT_Run2016F_HIPM_UL16          = kreator.makeDataComponent("HTMHT_Run2016F_HIPM_UL16"         , "/HTMHT/Run2016F-HIPM_UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD"         , "CMS", ".*root", json)
MET_Run2016F_HIPM_UL16            = kreator.makeDataComponent("MET_Run2016F_HIPM_UL16"           , "/MET/Run2016F-HIPM_UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD"           , "CMS", ".*root", json)
SingleElectron_Run2016F_HIPM_UL16 = kreator.makeDataComponent("SingleElectron_Run2016F_HIPM_UL16", "/SingleElectron/Run2016F-HIPM_UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2016F_HIPM_UL16     = kreator.makeDataComponent("SingleMuon_Run2016F_HIPM_UL16"    , "/SingleMuon/Run2016F-HIPM_UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD"    , "CMS", ".*root", json)
SinglePhoton_Run2016F_HIPM_UL16   = kreator.makeDataComponent("SinglePhoton_Run2016F_HIPM_UL16"  , "/SinglePhoton/Run2016F-HIPM_UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD"  , "CMS", ".*root", json)
DoubleEG_Run2016F_HIPM_UL16       = kreator.makeDataComponent("DoubleEG_Run2016F_HIPM_UL16"      , "/DoubleEG/Run2016F-HIPM_UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD"      , "CMS", ".*root", json)
MuonEG_Run2016F_HIPM_UL16         = kreator.makeDataComponent("MuonEG_Run2016F_HIPM_UL16"        , "/MuonEG/Run2016F-HIPM_UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD"        , "CMS", ".*root", json)
DoubleMuon_Run2016F_HIPM_UL16     = kreator.makeDataComponent("DoubleMuon_Run2016F_HIPM_UL16"    , "/DoubleMuon/Run2016F-HIPM_UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD"    , "CMS", ".*root", json)
Tau_Run2016F_HIPM_UL16            = kreator.makeDataComponent("Tau_Run2016F_HIPM_UL16"           , "/Tau/Run2016F-HIPM_UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD"    , "CMS", ".*root", json)

dataSamples_Run2016F_HIPM_UL16 = [JetHT_Run2016F_HIPM_UL16,HTMHT_Run2016F_HIPM_UL16,MET_Run2016F_HIPM_UL16,SingleElectron_Run2016F_HIPM_UL16,SingleMuon_Run2016F_HIPM_UL16,SinglePhoton_Run2016F_HIPM_UL16,DoubleEG_Run2016F_HIPM_UL16,MuonEG_Run2016F_HIPM_UL16,DoubleMuon_Run2016F_HIPM_UL16,Tau_Run2016F_HIPM_UL16]

dataSamples_UL16APV=dataSamples_Run2016Bv1_HIPM_UL16+dataSamples_Run2016Bv2_HIPM_UL16+dataSamples_Run2016C_HIPM_UL16+dataSamples_Run2016D_HIPM_UL16+dataSamples_Run2016E_HIPM_UL16+dataSamples_Run2016F_HIPM_UL16
