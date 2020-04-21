from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()

json='/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/ReReco/Final/Cert_271036-284044_13TeV_ReReco_07Aug2017_Collisions16_JSON.txt'

### ----------------------------- Run2016B 14Dec2018 ----------------------------------------

JetHT_Run2016B_14Dec2018          = kreator.makeDataComponent("JetHT_Run2016B_14Dec2018"         , "/JetHT/Run2016B_ver2-Nano14Dec2018_ver2-v1/NANOAOD"         , "CMS", ".*root", json)
HTMHT_Run2016B_14Dec2018          = kreator.makeDataComponent("HTMHT_Run2016B_14Dec2018"         , "/HTMHT/Run2016B_ver2-Nano14Dec2018_ver2-v1/NANOAOD"         , "CMS", ".*root", json)
MET_Run2016B_14Dec2018            = kreator.makeDataComponent("MET_Run2016B_14Dec2018"           , "/MET/Run2016B_ver2-Nano14Dec2018_ver2-v1/NANOAOD"           , "CMS", ".*root", json)
SingleElectron_Run2016B_14Dec2018 = kreator.makeDataComponent("SingleElectron_Run2016B_14Dec2018", "/SingleElectron/Run2016B_ver2-Nano14Dec2018_ver2-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2016B_14Dec2018     = kreator.makeDataComponent("SingleMuon_Run2016B_14Dec2018"    , "/SingleMuon/Run2016B_ver2-Nano14Dec2018_ver2-v1/NANOAOD"    , "CMS", ".*root", json)
SinglePhoton_Run2016B_14Dec2018   = kreator.makeDataComponent("SinglePhoton_Run2016B_14Dec2018"  , "/SinglePhoton/Run2016B_ver2-Nano14Dec2018_ver2-v1/NANOAOD"  , "CMS", ".*root", json)
DoubleEG_Run2016B_14Dec2018       = kreator.makeDataComponent("DoubleEG_Run2016B_14Dec2018"      , "/DoubleEG/Run2016B_ver2-Nano14Dec2018_ver2-v1/NANOAOD"      , "CMS", ".*root", json)
MuonEG_Run2016B_14Dec2018        = kreator.makeDataComponent("MuonEG_Run2016B_14Dec2018"        , "/MuonEG/Run2016B_ver2-Nano14Dec2018_ver2-v1/NANOAOD"        , "CMS", ".*root", json)
DoubleMuon_Run2016B_14Dec2018     = kreator.makeDataComponent("DoubleMuon_Run2016B_14Dec2018"    , "/DoubleMuon/Run2016B_ver2-Nano14Dec2018_ver2-v1/NANOAOD"    , "CMS", ".*root", json)
Tau_Run2016B_14Dec2018     = kreator.makeDataComponent("Tau_Run2016B_14Dec2018"    , "/Tau/Run2016B_ver2-Nano14Dec2018_ver2-v1/NANOAOD"    , "CMS", ".*root", json)

dataSamples_Run2016B_14Dec2018 = [JetHT_Run2016B_14Dec2018, HTMHT_Run2016B_14Dec2018, MET_Run2016B_14Dec2018, SingleElectron_Run2016B_14Dec2018, SingleMuon_Run2016B_14Dec2018, SinglePhoton_Run2016B_14Dec2018, DoubleEG_Run2016B_14Dec2018, MuonEG_Run2016B_14Dec2018, DoubleMuon_Run2016B_14Dec2018, Tau_Run2016B_14Dec2018]

### ----------------------------- Run2016C 14Dec2018 ----------------------------------------

JetHT_Run2016C_14Dec2018          = kreator.makeDataComponent("JetHT_Run2016C_14Dec2018"         , "/JetHT/Run2016C-Nano14Dec2018-v1/NANOAOD"         , "CMS", ".*root", json)
HTMHT_Run2016C_14Dec2018          = kreator.makeDataComponent("HTMHT_Run2016C_14Dec2018"         , "/HTMHT/Run2016C-Nano14Dec2018-v1/NANOAOD"         , "CMS", ".*root", json)
MET_Run2016C_14Dec2018            = kreator.makeDataComponent("MET_Run2016C_14Dec2018"           , "/MET/Run2016C-Nano14Dec2018-v1/NANOAOD"           , "CMS", ".*root", json)
SingleElectron_Run2016C_14Dec2018 = kreator.makeDataComponent("SingleElectron_Run2016C_14Dec2018", "/SingleElectron/Run2016C-Nano14Dec2018-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2016C_14Dec2018     = kreator.makeDataComponent("SingleMuon_Run2016C_14Dec2018"    , "/SingleMuon/Run2016C-Nano14Dec2018-v1/NANOAOD"    , "CMS", ".*root", json)
SinglePhoton_Run2016C_14Dec2018   = kreator.makeDataComponent("SinglePhoton_Run2016C_14Dec2018"  , "/SinglePhoton/Run2016C-Nano14Dec2018-v1/NANOAOD"  , "CMS", ".*root", json)
DoubleEG_Run2016C_14Dec2018       = kreator.makeDataComponent("DoubleEG_Run2016C_14Dec2018"      , "/DoubleEG/Run2016C-Nano14Dec2018-v1/NANOAOD"      , "CMS", ".*root", json)
MuonEG_Run2016C_14Dec2018         = kreator.makeDataComponent("MuonEG_Run2016C_14Dec2018"        , "/MuonEG/Run2016C-Nano14Dec2018-v1/NANOAOD"        , "CMS", ".*root", json)
DoubleMuon_Run2016C_14Dec2018     = kreator.makeDataComponent("DoubleMuon_Run2016C_14Dec2018"    , "/DoubleMuon/Run2016C-Nano14Dec2018-v1/NANOAOD"    , "CMS", ".*root", json)
Tau_Run2016C_14Dec2018            = kreator.makeDataComponent("Tau_Run2016C_14Dec2018"           , "/Tau/Run2016C-Nano14Dec2018-v1/NANOAOD"           , "CMS", ".*root", json)

dataSamples_Run2016C_14Dec2018 = [JetHT_Run2016C_14Dec2018, HTMHT_Run2016C_14Dec2018, MET_Run2016C_14Dec2018, SingleElectron_Run2016C_14Dec2018, SingleMuon_Run2016C_14Dec2018, SinglePhoton_Run2016C_14Dec2018, DoubleEG_Run2016C_14Dec2018, MuonEG_Run2016C_14Dec2018, DoubleMuon_Run2016C_14Dec2018, Tau_Run2016C_14Dec2018]


### ----------------------------- Run2016D 14Dec2018 v2 ----------------------------------------

JetHT_Run2016D_14Dec2018          = kreator.makeDataComponent("JetHT_Run2016D_14Dec2018"         , "/JetHT/Run2016D-Nano14Dec2018-v1/NANOAOD"         , "CMS", ".*root", json)
HTMHT_Run2016D_14Dec2018          = kreator.makeDataComponent("HTMHT_Run2016D_14Dec2018"         , "/HTMHT/Run2016D-Nano14Dec2018-v1/NANOAOD"         , "CMS", ".*root", json)
MET_Run2016D_14Dec2018            = kreator.makeDataComponent("MET_Run2016D_14Dec2018"           , "/MET/Run2016D-Nano14Dec2018-v1/NANOAOD"           , "CMS", ".*root", json)
SingleElectron_Run2016D_14Dec2018 = kreator.makeDataComponent("SingleElectron_Run2016D_14Dec2018", "/SingleElectron/Run2016D-Nano14Dec2018-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2016D_14Dec2018     = kreator.makeDataComponent("SingleMuon_Run2016D_14Dec2018"    , "/SingleMuon/Run2016D-Nano14Dec2018-v1/NANOAOD"    , "CMS", ".*root", json)
SinglePhoton_Run2016D_14Dec2018   = kreator.makeDataComponent("SinglePhoton_Run2016D_14Dec2018"  , "/SinglePhoton/Run2016D-Nano14Dec2018-v1/NANOAOD"  , "CMS", ".*root", json)
DoubleEG_Run2016D_14Dec2018       = kreator.makeDataComponent("DoubleEG_Run2016D_14Dec2018"      , "/DoubleEG/Run2016D-Nano14Dec2018-v1/NANOAOD"      , "CMS", ".*root", json)
MuonEG_Run2016D_14Dec2018         = kreator.makeDataComponent("MuonEG_Run2016D_14Dec2018"        , "/MuonEG/Run2016D-Nano14Dec2018-v1/NANOAOD"        , "CMS", ".*root", json)
DoubleMuon_Run2016D_14Dec2018     = kreator.makeDataComponent("DoubleMuon_Run2016D_14Dec2018"    , "/DoubleMuon/Run2016D-Nano14Dec2018-v1/NANOAOD"    , "CMS", ".*root", json)
Tau_Run2016D_14Dec2018            = kreator.makeDataComponent("Tau_Run2016D_14Dec2018"           , "/Tau/Run2016D-Nano14Dec2018-v1/NANOAOD"           , "CMS", ".*root", json)

dataSamples_Run2016D_14Dec2018 = [JetHT_Run2016D_14Dec2018, HTMHT_Run2016D_14Dec2018, MET_Run2016D_14Dec2018, SingleElectron_Run2016D_14Dec2018, SingleMuon_Run2016D_14Dec2018, SinglePhoton_Run2016D_14Dec2018, DoubleEG_Run2016D_14Dec2018, MuonEG_Run2016D_14Dec2018, DoubleMuon_Run2016D_14Dec2018, Tau_Run2016D_14Dec2018]

### ----------------------------- Run2016E 14Dec2018 v2 ----------------------------------------

JetHT_Run2016E_14Dec2018          = kreator.makeDataComponent("JetHT_Run2016E_14Dec2018"         , "/JetHT/Run2016E-Nano14Dec2018-v1/NANOAOD"         , "CMS", ".*root", json)
HTMHT_Run2016E_14Dec2018          = kreator.makeDataComponent("HTMHT_Run2016E_14Dec2018"         , "/HTMHT/Run2016E-Nano14Dec2018-v1/NANOAOD"         , "CMS", ".*root", json)
MET_Run2016E_14Dec2018            = kreator.makeDataComponent("MET_Run2016E_14Dec2018"           , "/MET/Run2016E-Nano14Dec2018-v1/NANOAOD"           , "CMS", ".*root", json)
SingleElectron_Run2016E_14Dec2018 = kreator.makeDataComponent("SingleElectron_Run2016E_14Dec2018", "/SingleElectron/Run2016E-Nano14Dec2018-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2016E_14Dec2018     = kreator.makeDataComponent("SingleMuon_Run2016E_14Dec2018"    , "/SingleMuon/Run2016E-Nano14Dec2018-v1/NANOAOD"    , "CMS", ".*root", json)
SinglePhoton_Run2016E_14Dec2018   = kreator.makeDataComponent("SinglePhoton_Run2016E_14Dec2018"  , "/SinglePhoton/Run2016E-Nano14Dec2018-v1/NANOAOD"  , "CMS", ".*root", json)
DoubleEG_Run2016E_14Dec2018       = kreator.makeDataComponent("DoubleEG_Run2016E_14Dec2018"      , "/DoubleEG/Run2016E-Nano14Dec2018-v1/NANOAOD"      , "CMS", ".*root", json)
MuonEG_Run2016E_14Dec2018         = kreator.makeDataComponent("MuonEG_Run2016E_14Dec2018"        , "/MuonEG/Run2016E-Nano14Dec2018-v1/NANOAOD"        , "CMS", ".*root", json)
DoubleMuon_Run2016E_14Dec2018     = kreator.makeDataComponent("DoubleMuon_Run2016E_14Dec2018"    , "/DoubleMuon/Run2016E-Nano14Dec2018-v1/NANOAOD"    , "CMS", ".*root", json)
Tau_Run2016E_14Dec2018            = kreator.makeDataComponent("Tau_Run2016E_14Dec2018"           , "/Tau/Run2016E-Nano14Dec2018-v1/NANOAOD"           , "CMS", ".*root", json)

dataSamples_Run2016E_14Dec2018 = [JetHT_Run2016E_14Dec2018, HTMHT_Run2016E_14Dec2018, MET_Run2016E_14Dec2018, SingleElectron_Run2016E_14Dec2018, SingleMuon_Run2016E_14Dec2018, SinglePhoton_Run2016E_14Dec2018, DoubleEG_Run2016E_14Dec2018, MuonEG_Run2016E_14Dec2018, DoubleMuon_Run2016E_14Dec2018, Tau_Run2016E_14Dec2018]


### ----------------------------- Run2016F 14Dec2018 v1 ----------------------------------------

JetHT_Run2016F_14Dec2018          = kreator.makeDataComponent("JetHT_Run2016F_14Dec2018"         , "/JetHT/Run2016F-Nano14Dec2018-v1/NANOAOD"         , "CMS", ".*root", json)
HTMHT_Run2016F_14Dec2018          = kreator.makeDataComponent("HTMHT_Run2016F_14Dec2018"         , "/HTMHT/Run2016F-Nano14Dec2018-v1/NANOAOD"         , "CMS", ".*root", json)
MET_Run2016F_14Dec2018            = kreator.makeDataComponent("MET_Run2016F_14Dec2018"           , "/MET/Run2016F-Nano14Dec2018-v1/NANOAOD"           , "CMS", ".*root", json)
SingleElectron_Run2016F_14Dec2018 = kreator.makeDataComponent("SingleElectron_Run2016F_14Dec2018", "/SingleElectron/Run2016F-Nano14Dec2018-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2016F_14Dec2018     = kreator.makeDataComponent("SingleMuon_Run2016F_14Dec2018"    , "/SingleMuon/Run2016F-Nano14Dec2018-v1/NANOAOD"    , "CMS", ".*root", json)
SinglePhoton_Run2016F_14Dec2018   = kreator.makeDataComponent("SinglePhoton_Run2016F_14Dec2018"  , "/SinglePhoton/Run2016F-Nano14Dec2018-v1/NANOAOD"  , "CMS", ".*root", json)
DoubleEG_Run2016F_14Dec2018       = kreator.makeDataComponent("DoubleEG_Run2016F_14Dec2018"      , "/DoubleEG/Run2016F-Nano14Dec2018-v1/NANOAOD"      , "CMS", ".*root", json)
MuonEG_Run2016F_14Dec2018         = kreator.makeDataComponent("MuonEG_Run2016F_14Dec2018"        , "/MuonEG/Run2016F-Nano14Dec2018-v1/NANOAOD"        , "CMS", ".*root", json)
DoubleMuon_Run2016F_14Dec2018     = kreator.makeDataComponent("DoubleMuon_Run2016F_14Dec2018"    , "/DoubleMuon/Run2016F-Nano14Dec2018-v1/NANOAOD"    , "CMS", ".*root", json)
Tau_Run2016F_14Dec2018            = kreator.makeDataComponent("Tau_Run2016F_14Dec2018"           , "/Tau/Run2016F-Nano14Dec2018-v1/NANOAOD"           , "CMS", ".*root", json)

dataSamples_Run2016F_14Dec2018 = [JetHT_Run2016F_14Dec2018, HTMHT_Run2016F_14Dec2018, MET_Run2016F_14Dec2018, SingleElectron_Run2016F_14Dec2018, SingleMuon_Run2016F_14Dec2018, SinglePhoton_Run2016F_14Dec2018, DoubleEG_Run2016F_14Dec2018, MuonEG_Run2016F_14Dec2018, DoubleMuon_Run2016F_14Dec2018, Tau_Run2016F_14Dec2018]

### ----------------------------- Run2016G 14Dec2018 v1 ----------------------------------------

JetHT_Run2016G_14Dec2018          = kreator.makeDataComponent("JetHT_Run2016G_14Dec2018"         , "/JetHT/Run2016G-Nano14Dec2018-v1/NANOAOD"         , "CMS", ".*root", json)
HTMHT_Run2016G_14Dec2018          = kreator.makeDataComponent("HTMHT_Run2016G_14Dec2018"         , "/HTMHT/Run2016G-Nano14Dec2018-v1/NANOAOD"         , "CMS", ".*root", json)
MET_Run2016G_14Dec2018            = kreator.makeDataComponent("MET_Run2016G_14Dec2018"           , "/MET/Run2016G-Nano14Dec2018-v1/NANOAOD"           , "CMS", ".*root", json)
SingleElectron_Run2016G_14Dec2018 = kreator.makeDataComponent("SingleElectron_Run2016G_14Dec2018", "/SingleElectron/Run2016G-Nano14Dec2018-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2016G_14Dec2018     = kreator.makeDataComponent("SingleMuon_Run2016G_14Dec2018"    , "/SingleMuon/Run2016G-Nano14Dec2018-v1/NANOAOD"    , "CMS", ".*root", json)
SinglePhoton_Run2016G_14Dec2018   = kreator.makeDataComponent("SinglePhoton_Run2016G_14Dec2018"  , "/SinglePhoton/Run2016G-Nano14Dec2018-v1/NANOAOD"  , "CMS", ".*root", json)
DoubleEG_Run2016G_14Dec2018       = kreator.makeDataComponent("DoubleEG_Run2016G_14Dec2018"      , "/DoubleEG/Run2016G-Nano14Dec2018-v1/NANOAOD"      , "CMS", ".*root", json)
MuonEG_Run2016G_14Dec2018        = kreator.makeDataComponent("MuonEG_Run2016G_14Dec2018"        , "/MuonEG/Run2016G-Nano14Dec2018-v1/NANOAOD"        , "CMS", ".*root", json)
DoubleMuon_Run2016G_14Dec2018     = kreator.makeDataComponent("DoubleMuon_Run2016G_14Dec2018"    , "/DoubleMuon/Run2016G-Nano14Dec2018-v1/NANOAOD"    , "CMS", ".*root", json)
Tau_Run2016G_14Dec2018     = kreator.makeDataComponent("Tau_Run2016G_14Dec2018"    , "/Tau/Run2016G-Nano14Dec2018-v1/NANOAOD"    , "CMS", ".*root", json)

dataSamples_Run2016G_14Dec2018 = [JetHT_Run2016G_14Dec2018, HTMHT_Run2016G_14Dec2018, MET_Run2016G_14Dec2018, SingleElectron_Run2016G_14Dec2018, SingleMuon_Run2016G_14Dec2018, SinglePhoton_Run2016G_14Dec2018, DoubleEG_Run2016G_14Dec2018, MuonEG_Run2016G_14Dec2018, DoubleMuon_Run2016G_14Dec2018, Tau_Run2016G_14Dec2018]

### ----------------------------- Run2016H 14Dec2018 v1 ----------------------------------------

JetHT_Run2016H_14Dec2018          = kreator.makeDataComponent("JetHT_Run2016H_14Dec2018"         , "/JetHT/Run2016H-Nano14Dec2018-v1/NANOAOD"         , "CMS", ".*root", json)
HTMHT_Run2016H_14Dec2018          = kreator.makeDataComponent("HTMHT_Run2016H_14Dec2018"         , "/HTMHT/Run2016H-Nano14Dec2018-v1/NANOAOD"         , "CMS", ".*root", json)
MET_Run2016H_14Dec2018            = kreator.makeDataComponent("MET_Run2016H_14Dec2018"           , "/MET/Run2016H-Nano14Dec2018-v1/NANOAOD"           , "CMS", ".*root", json)
SingleElectron_Run2016H_14Dec2018 = kreator.makeDataComponent("SingleElectron_Run2016H_14Dec2018", "/SingleElectron/Run2016H-Nano14Dec2018-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2016H_14Dec2018     = kreator.makeDataComponent("SingleMuon_Run2016H_14Dec2018"    , "/SingleMuon/Run2016H-Nano14Dec2018-v1/NANOAOD"    , "CMS", ".*root", json)
SinglePhoton_Run2016H_14Dec2018   = kreator.makeDataComponent("SinglePhoton_Run2016H_14Dec2018"  , "/SinglePhoton/Run2016H-Nano14Dec2018-v1/NANOAOD"  , "CMS", ".*root", json)
DoubleEG_Run2016H_14Dec2018       = kreator.makeDataComponent("DoubleEG_Run2016H_14Dec2018"      , "/DoubleEG/Run2016H-Nano14Dec2018-v1/NANOAOD"      , "CMS", ".*root", json)
MuonEG_Run2016H_14Dec2018        = kreator.makeDataComponent("MuonEG_Run2016H_14Dec2018"        , "/MuonEG/Run2016H-Nano14Dec2018-v1/NANOAOD"        , "CMS", ".*root", json)
DoubleMuon_Run2016H_14Dec2018     = kreator.makeDataComponent("DoubleMuon_Run2016H_14Dec2018"    , "/DoubleMuon/Run2016H-Nano14Dec2018-v1/NANOAOD"    , "CMS", ".*root", json)
Tau_Run2016H_14Dec2018     = kreator.makeDataComponent("Tau_Run2016H_14Dec2018"    , "/Tau/Run2016H-Nano14Dec2018-v1/NANOAOD"    , "CMS", ".*root", json)

dataSamples_Run2016H_14Dec2018 = [JetHT_Run2016H_14Dec2018, HTMHT_Run2016H_14Dec2018, MET_Run2016H_14Dec2018, SingleElectron_Run2016H_14Dec2018, SingleMuon_Run2016H_14Dec2018, SinglePhoton_Run2016H_14Dec2018, DoubleEG_Run2016H_14Dec2018, MuonEG_Run2016H_14Dec2018, DoubleMuon_Run2016H_14Dec2018, Tau_Run2016H_14Dec2018]


### Summary of prompt reco
dataSamples_14Dec2018 = dataSamples_Run2016B_14Dec2018 + dataSamples_Run2016C_14Dec2018 + dataSamples_Run2016D_14Dec2018 + dataSamples_Run2016E_14Dec2018 + dataSamples_Run2016F_14Dec2018 + dataSamples_Run2016G_14Dec2018 + dataSamples_Run2016H_14Dec2018

### ----------------------------- Run2016B 1June2019 ----------------------------------------

JetHT_Run2016B_1June2019          = kreator.makeDataComponent("JetHT_Run2016B_1June2019"         , "/JetHT/Run2016B_ver2-Nano1June2019_ver2-v2/NANOAOD"         , "CMS", ".*root", json)
HTMHT_Run2016B_1June2019          = kreator.makeDataComponent("HTMHT_Run2016B_1June2019"         , "/HTMHT/Run2016B_ver2-Nano1June2019_ver2-v1/NANOAOD"         , "CMS", ".*root", json)
MET_Run2016B_1June2019            = kreator.makeDataComponent("MET_Run2016B_1June2019"           , "/MET/Run2016B_ver2-Nano1June2019_ver2-v1/NANOAOD"           , "CMS", ".*root", json)
SingleElectron_Run2016B_1June2019 = kreator.makeDataComponent("SingleElectron_Run2016B_1June2019", "/SingleElectron/Run2016B_ver2-Nano1June2019_ver2-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2016B_1June2019     = kreator.makeDataComponent("SingleMuon_Run2016B_1June2019"    , "/SingleMuon/Run2016B_ver2-Nano1June2019_ver2-v1/NANOAOD"    , "CMS", ".*root", json)
SinglePhoton_Run2016B_1June2019   = kreator.makeDataComponent("SinglePhoton_Run2016B_1June2019"  , "/SinglePhoton/Run2016B_ver2-Nano1June2019_ver2-v1/NANOAOD"  , "CMS", ".*root", json)
DoubleEG_Run2016B_1June2019       = kreator.makeDataComponent("DoubleEG_Run2016B_1June2019"      , "/DoubleEG/Run2016B_ver2-Nano1June2019_ver2-v1/NANOAOD"      , "CMS", ".*root", json)
MuonEG_Run2016B_1June2019        = kreator.makeDataComponent("MuonEG_Run2016B_1June2019"        , "/MuonEG/Run2016B_ver2-Nano1June2019_ver2-v1/NANOAOD"        , "CMS", ".*root", json)
DoubleMuon_Run2016B_1June2019     = kreator.makeDataComponent("DoubleMuon_Run2016B_1June2019"    , "/DoubleMuon/Run2016B_ver2-Nano1June2019_ver2-v1/NANOAOD"    , "CMS", ".*root", json)
Tau_Run2016B_1June2019     = kreator.makeDataComponent("Tau_Run2016B_1June2019"    , "/Tau/Run2016B_ver2-Nano1June2019_ver2-v1/NANOAOD"    , "CMS", ".*root", json)

dataSamples_Run2016B_1June2019 = [JetHT_Run2016B_1June2019, HTMHT_Run2016B_1June2019, MET_Run2016B_1June2019, SingleElectron_Run2016B_1June2019, SingleMuon_Run2016B_1June2019, SinglePhoton_Run2016B_1June2019, DoubleEG_Run2016B_1June2019, MuonEG_Run2016B_1June2019, DoubleMuon_Run2016B_1June2019, Tau_Run2016B_1June2019]

### ----------------------------- Run2016C 1June2019 ----------------------------------------

JetHT_Run2016C_1June2019          = kreator.makeDataComponent("JetHT_Run2016C_1June2019"         , "/JetHT/Run2016C-Nano1June2019-v1/NANOAOD"         , "CMS", ".*root", json)
HTMHT_Run2016C_1June2019          = kreator.makeDataComponent("HTMHT_Run2016C_1June2019"         , "/HTMHT/Run2016C-Nano1June2019-v1/NANOAOD"         , "CMS", ".*root", json)
MET_Run2016C_1June2019            = kreator.makeDataComponent("MET_Run2016C_1June2019"           , "/MET/Run2016C-Nano1June2019-v1/NANOAOD"           , "CMS", ".*root", json)
SingleElectron_Run2016C_1June2019 = kreator.makeDataComponent("SingleElectron_Run2016C_1June2019", "/SingleElectron/Run2016C-Nano1June2019-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2016C_1June2019     = kreator.makeDataComponent("SingleMuon_Run2016C_1June2019"    , "/SingleMuon/Run2016C-Nano1June2019-v1/NANOAOD"    , "CMS", ".*root", json)
SinglePhoton_Run2016C_1June2019   = kreator.makeDataComponent("SinglePhoton_Run2016C_1June2019"  , "/SinglePhoton/Run2016C-Nano1June2019-v1/NANOAOD"  , "CMS", ".*root", json)
DoubleEG_Run2016C_1June2019       = kreator.makeDataComponent("DoubleEG_Run2016C_1June2019"      , "/DoubleEG/Run2016C-Nano1June2019-v1/NANOAOD"      , "CMS", ".*root", json)
MuonEG_Run2016C_1June2019         = kreator.makeDataComponent("MuonEG_Run2016C_1June2019"        , "/MuonEG/Run2016C-Nano1June2019-v1/NANOAOD"        , "CMS", ".*root", json)
DoubleMuon_Run2016C_1June2019     = kreator.makeDataComponent("DoubleMuon_Run2016C_1June2019"    , "/DoubleMuon/Run2016C-Nano1June2019-v1/NANOAOD"    , "CMS", ".*root", json)
Tau_Run2016C_1June2019            = kreator.makeDataComponent("Tau_Run2016C_1June2019"           , "/Tau/Run2016C-Nano1June2019-v1/NANOAOD"           , "CMS", ".*root", json)

dataSamples_Run2016C_1June2019 = [JetHT_Run2016C_1June2019, HTMHT_Run2016C_1June2019, MET_Run2016C_1June2019, SingleElectron_Run2016C_1June2019, SingleMuon_Run2016C_1June2019, SinglePhoton_Run2016C_1June2019, DoubleEG_Run2016C_1June2019, MuonEG_Run2016C_1June2019, DoubleMuon_Run2016C_1June2019, Tau_Run2016C_1June2019]


### ----------------------------- Run2016D 1June2019 v2 ----------------------------------------

JetHT_Run2016D_1June2019          = kreator.makeDataComponent("JetHT_Run2016D_1June2019"         , "/JetHT/Run2016D-Nano1June2019-v1/NANOAOD"         , "CMS", ".*root", json)
HTMHT_Run2016D_1June2019          = kreator.makeDataComponent("HTMHT_Run2016D_1June2019"         , "/HTMHT/Run2016D-Nano1June2019-v1/NANOAOD"         , "CMS", ".*root", json)
MET_Run2016D_1June2019            = kreator.makeDataComponent("MET_Run2016D_1June2019"           , "/MET/Run2016D-Nano1June2019-v1/NANOAOD"           , "CMS", ".*root", json)
SingleElectron_Run2016D_1June2019 = kreator.makeDataComponent("SingleElectron_Run2016D_1June2019", "/SingleElectron/Run2016D-Nano1June2019-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2016D_1June2019     = kreator.makeDataComponent("SingleMuon_Run2016D_1June2019"    , "/SingleMuon/Run2016D-Nano1June2019-v1/NANOAOD"    , "CMS", ".*root", json)
SinglePhoton_Run2016D_1June2019   = kreator.makeDataComponent("SinglePhoton_Run2016D_1June2019"  , "/SinglePhoton/Run2016D-Nano1June2019-v1/NANOAOD"  , "CMS", ".*root", json)
DoubleEG_Run2016D_1June2019       = kreator.makeDataComponent("DoubleEG_Run2016D_1June2019"      , "/DoubleEG/Run2016D-Nano1June2019-v1/NANOAOD"      , "CMS", ".*root", json)
MuonEG_Run2016D_1June2019         = kreator.makeDataComponent("MuonEG_Run2016D_1June2019"        , "/MuonEG/Run2016D-Nano1June2019-v1/NANOAOD"        , "CMS", ".*root", json)
DoubleMuon_Run2016D_1June2019     = kreator.makeDataComponent("DoubleMuon_Run2016D_1June2019"    , "/DoubleMuon/Run2016D-Nano1June2019-v1/NANOAOD"    , "CMS", ".*root", json)
Tau_Run2016D_1June2019            = kreator.makeDataComponent("Tau_Run2016D_1June2019"           , "/Tau/Run2016D-Nano1June2019-v1/NANOAOD"           , "CMS", ".*root", json)

dataSamples_Run2016D_1June2019 = [JetHT_Run2016D_1June2019, HTMHT_Run2016D_1June2019, MET_Run2016D_1June2019, SingleElectron_Run2016D_1June2019, SingleMuon_Run2016D_1June2019, SinglePhoton_Run2016D_1June2019, DoubleEG_Run2016D_1June2019, MuonEG_Run2016D_1June2019, DoubleMuon_Run2016D_1June2019, Tau_Run2016D_1June2019]

### ----------------------------- Run2016E 1June2019 v2 ----------------------------------------

JetHT_Run2016E_1June2019          = kreator.makeDataComponent("JetHT_Run2016E_1June2019"         , "/JetHT/Run2016E-Nano1June2019-v1/NANOAOD"         , "CMS", ".*root", json)
HTMHT_Run2016E_1June2019          = kreator.makeDataComponent("HTMHT_Run2016E_1June2019"         , "/HTMHT/Run2016E-Nano1June2019-v1/NANOAOD"         , "CMS", ".*root", json)
MET_Run2016E_1June2019            = kreator.makeDataComponent("MET_Run2016E_1June2019"           , "/MET/Run2016E-Nano1June2019-v1/NANOAOD"           , "CMS", ".*root", json)
SingleElectron_Run2016E_1June2019 = kreator.makeDataComponent("SingleElectron_Run2016E_1June2019", "/SingleElectron/Run2016E-Nano1June2019-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2016E_1June2019     = kreator.makeDataComponent("SingleMuon_Run2016E_1June2019"    , "/SingleMuon/Run2016E-Nano1June2019-v1/NANOAOD"    , "CMS", ".*root", json)
SinglePhoton_Run2016E_1June2019   = kreator.makeDataComponent("SinglePhoton_Run2016E_1June2019"  , "/SinglePhoton/Run2016E-Nano1June2019-v1/NANOAOD"  , "CMS", ".*root", json)
DoubleEG_Run2016E_1June2019       = kreator.makeDataComponent("DoubleEG_Run2016E_1June2019"      , "/DoubleEG/Run2016E-Nano1June2019-v1/NANOAOD"      , "CMS", ".*root", json)
MuonEG_Run2016E_1June2019         = kreator.makeDataComponent("MuonEG_Run2016E_1June2019"        , "/MuonEG/Run2016E-Nano1June2019-v3/NANOAOD"        , "CMS", ".*root", json)
DoubleMuon_Run2016E_1June2019     = kreator.makeDataComponent("DoubleMuon_Run2016E_1June2019"    , "/DoubleMuon/Run2016E-Nano1June2019-v1/NANOAOD"    , "CMS", ".*root", json)
Tau_Run2016E_1June2019            = kreator.makeDataComponent("Tau_Run2016E_1June2019"           , "/Tau/Run2016E-Nano1June2019-v1/NANOAOD"           , "CMS", ".*root", json)

dataSamples_Run2016E_1June2019 = [JetHT_Run2016E_1June2019, HTMHT_Run2016E_1June2019, MET_Run2016E_1June2019, SingleElectron_Run2016E_1June2019, SingleMuon_Run2016E_1June2019, SinglePhoton_Run2016E_1June2019, DoubleEG_Run2016E_1June2019, MuonEG_Run2016E_1June2019, DoubleMuon_Run2016E_1June2019, Tau_Run2016E_1June2019]


### ----------------------------- Run2016F 1June2019 v1 ----------------------------------------

JetHT_Run2016F_1June2019          = kreator.makeDataComponent("JetHT_Run2016F_1June2019"         , "/JetHT/Run2016F-Nano1June2019-v1/NANOAOD"         , "CMS", ".*root", json)
HTMHT_Run2016F_1June2019          = kreator.makeDataComponent("HTMHT_Run2016F_1June2019"         , "/HTMHT/Run2016F-Nano1June2019-v1/NANOAOD"         , "CMS", ".*root", json)
MET_Run2016F_1June2019            = kreator.makeDataComponent("MET_Run2016F_1June2019"           , "/MET/Run2016F-Nano1June2019-v1/NANOAOD"           , "CMS", ".*root", json)
SingleElectron_Run2016F_1June2019 = kreator.makeDataComponent("SingleElectron_Run2016F_1June2019", "/SingleElectron/Run2016F-Nano1June2019-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2016F_1June2019     = kreator.makeDataComponent("SingleMuon_Run2016F_1June2019"    , "/SingleMuon/Run2016F-Nano1June2019-v1/NANOAOD"    , "CMS", ".*root", json)
SinglePhoton_Run2016F_1June2019   = kreator.makeDataComponent("SinglePhoton_Run2016F_1June2019"  , "/SinglePhoton/Run2016F-Nano1June2019-v1/NANOAOD"  , "CMS", ".*root", json)
DoubleEG_Run2016F_1June2019       = kreator.makeDataComponent("DoubleEG_Run2016F_1June2019"      , "/DoubleEG/Run2016F-Nano1June2019-v1/NANOAOD"      , "CMS", ".*root", json)
MuonEG_Run2016F_1June2019         = kreator.makeDataComponent("MuonEG_Run2016F_1June2019"        , "/MuonEG/Run2016F-Nano1June2019-v1/NANOAOD"        , "CMS", ".*root", json)
DoubleMuon_Run2016F_1June2019     = kreator.makeDataComponent("DoubleMuon_Run2016F_1June2019"    , "/DoubleMuon/Run2016F-Nano1June2019-v1/NANOAOD"    , "CMS", ".*root", json)
#Tau_Run2016F_1June2019            = kreator.makeDataComponent("Tau_Run2016F_1June2019"           , "/Tau/Run2016F-Nano1June2019-v1/NANOAOD"           , "CMS", ".*root", json)

dataSamples_Run2016F_1June2019 = [JetHT_Run2016F_1June2019, HTMHT_Run2016F_1June2019, MET_Run2016F_1June2019, SingleElectron_Run2016F_1June2019, SingleMuon_Run2016F_1June2019, SinglePhoton_Run2016F_1June2019, DoubleEG_Run2016F_1June2019, MuonEG_Run2016F_1June2019, DoubleMuon_Run2016F_1June2019,
# Tau_Run2016F_1June2019
]

### ----------------------------- Run2016G 1June2019 v1 ----------------------------------------

JetHT_Run2016G_1June2019          = kreator.makeDataComponent("JetHT_Run2016G_1June2019"         , "/JetHT/Run2016G-Nano1June2019-v1/NANOAOD"         , "CMS", ".*root", json)
HTMHT_Run2016G_1June2019          = kreator.makeDataComponent("HTMHT_Run2016G_1June2019"         , "/HTMHT/Run2016G-Nano1June2019-v1/NANOAOD"         , "CMS", ".*root", json)
MET_Run2016G_1June2019            = kreator.makeDataComponent("MET_Run2016G_1June2019"           , "/MET/Run2016G-Nano1June2019-v1/NANOAOD"           , "CMS", ".*root", json)
SingleElectron_Run2016G_1June2019 = kreator.makeDataComponent("SingleElectron_Run2016G_1June2019", "/SingleElectron/Run2016G-Nano1June2019-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2016G_1June2019     = kreator.makeDataComponent("SingleMuon_Run2016G_1June2019"    , "/SingleMuon/Run2016G-Nano1June2019-v1/NANOAOD"    , "CMS", ".*root", json)
SinglePhoton_Run2016G_1June2019   = kreator.makeDataComponent("SinglePhoton_Run2016G_1June2019"  , "/SinglePhoton/Run2016G-Nano1June2019-v1/NANOAOD"  , "CMS", ".*root", json)
DoubleEG_Run2016G_1June2019       = kreator.makeDataComponent("DoubleEG_Run2016G_1June2019"      , "/DoubleEG/Run2016G-Nano1June2019-v1/NANOAOD"      , "CMS", ".*root", json)
MuonEG_Run2016G_1June2019        = kreator.makeDataComponent("MuonEG_Run2016G_1June2019"        , "/MuonEG/Run2016G-Nano1June2019-v1/NANOAOD"        , "CMS", ".*root", json)
DoubleMuon_Run2016G_1June2019     = kreator.makeDataComponent("DoubleMuon_Run2016G_1June2019"    , "/DoubleMuon/Run2016G-Nano1June2019-v1/NANOAOD"    , "CMS", ".*root", json)
Tau_Run2016G_1June2019     = kreator.makeDataComponent("Tau_Run2016G_1June2019"    , "/Tau/Run2016G-Nano1June2019-v1/NANOAOD"    , "CMS", ".*root", json)

dataSamples_Run2016G_1June2019 = [JetHT_Run2016G_1June2019, HTMHT_Run2016G_1June2019, MET_Run2016G_1June2019, SingleElectron_Run2016G_1June2019, SingleMuon_Run2016G_1June2019, SinglePhoton_Run2016G_1June2019, DoubleEG_Run2016G_1June2019, MuonEG_Run2016G_1June2019, DoubleMuon_Run2016G_1June2019, Tau_Run2016G_1June2019]

### ----------------------------- Run2016H 1June2019 v1 ----------------------------------------

JetHT_Run2016H_1June2019          = kreator.makeDataComponent("JetHT_Run2016H_1June2019"         , "/JetHT/Run2016H-Nano1June2019-v1/NANOAOD"         , "CMS", ".*root", json)
HTMHT_Run2016H_1June2019          = kreator.makeDataComponent("HTMHT_Run2016H_1June2019"         , "/HTMHT/Run2016H-Nano1June2019-v1/NANOAOD"         , "CMS", ".*root", json)
MET_Run2016H_1June2019            = kreator.makeDataComponent("MET_Run2016H_1June2019"           , "/MET/Run2016H-Nano1June2019-v3/NANOAOD"           , "CMS", ".*root", json)
SingleElectron_Run2016H_1June2019 = kreator.makeDataComponent("SingleElectron_Run2016H_1June2019", "/SingleElectron/Run2016H-Nano1June2019-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2016H_1June2019     = kreator.makeDataComponent("SingleMuon_Run2016H_1June2019"    , "/SingleMuon/Run2016H-Nano1June2019-v1/NANOAOD"    , "CMS", ".*root", json)
SinglePhoton_Run2016H_1June2019   = kreator.makeDataComponent("SinglePhoton_Run2016H_1June2019"  , "/SinglePhoton/Run2016H-Nano1June2019-v1/NANOAOD"  , "CMS", ".*root", json)
DoubleEG_Run2016H_1June2019       = kreator.makeDataComponent("DoubleEG_Run2016H_1June2019"      , "/DoubleEG/Run2016H-Nano1June2019-v1/NANOAOD"      , "CMS", ".*root", json)
MuonEG_Run2016H_1June2019        = kreator.makeDataComponent("MuonEG_Run2016H_1June2019"        , "/MuonEG/Run2016H-Nano1June2019-v1/NANOAOD"        , "CMS", ".*root", json)
DoubleMuon_Run2016H_1June2019     = kreator.makeDataComponent("DoubleMuon_Run2016H_1June2019"    , "/DoubleMuon/Run2016H-Nano1June2019-v1/NANOAOD"    , "CMS", ".*root", json)
Tau_Run2016H_1June2019     = kreator.makeDataComponent("Tau_Run2016H_1June2019"    , "/Tau/Run2016H-Nano1June2019-v1/NANOAOD"    , "CMS", ".*root", json)

dataSamples_Run2016H_1June2019 = [JetHT_Run2016H_1June2019, HTMHT_Run2016H_1June2019, MET_Run2016H_1June2019, SingleElectron_Run2016H_1June2019, SingleMuon_Run2016H_1June2019, SinglePhoton_Run2016H_1June2019, DoubleEG_Run2016H_1June2019, MuonEG_Run2016H_1June2019, DoubleMuon_Run2016H_1June2019, Tau_Run2016H_1June2019]


### Summary of prompt reco
dataSamples_1June2019 = dataSamples_Run2016B_1June2019 + dataSamples_Run2016C_1June2019 + dataSamples_Run2016D_1June2019 + dataSamples_Run2016E_1June2019 + dataSamples_Run2016F_1June2019 + dataSamples_Run2016G_1June2019 + dataSamples_Run2016H_1June2019

### ----------------------------- Run2016B 25Oct2019 ----------------------------------------

JetHT_Run2016B_25Oct2019          = kreator.makeDataComponent("JetHT_Run2016B_25Oct2019"         , "/JetHT/Run2016B_ver2-Nano25Oct2019_ver2-v1/NANOAOD"         , "CMS", ".*root", json)
HTMHT_Run2016B_25Oct2019          = kreator.makeDataComponent("HTMHT_Run2016B_25Oct2019"         , "/HTMHT/Run2016B_ver2-Nano25Oct2019_ver2-v1/NANOAOD"         , "CMS", ".*root", json)
MET_Run2016B_25Oct2019            = kreator.makeDataComponent("MET_Run2016B_25Oct2019"           , "/MET/Run2016B_ver2-Nano25Oct2019_ver2-v1/NANOAOD"           , "CMS", ".*root", json)
SingleElectron_Run2016B_25Oct2019 = kreator.makeDataComponent("SingleElectron_Run2016B_25Oct2019", "/SingleElectron/Run2016B_ver2-Nano25Oct2019_ver2-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2016B_25Oct2019     = kreator.makeDataComponent("SingleMuon_Run2016B_25Oct2019"    , "/SingleMuon/Run2016B_ver2-Nano25Oct2019_ver2-v1/NANOAOD"    , "CMS", ".*root", json)
SinglePhoton_Run2016B_25Oct2019   = kreator.makeDataComponent("SinglePhoton_Run2016B_25Oct2019"  , "/SinglePhoton/Run2016B_ver2-Nano25Oct2019_ver2-v1/NANOAOD"  , "CMS", ".*root", json)
DoubleEG_Run2016B_25Oct2019       = kreator.makeDataComponent("DoubleEG_Run2016B_25Oct2019"      , "/DoubleEG/Run2016B_ver2-Nano25Oct2019_ver2-v1/NANOAOD"      , "CMS", ".*root", json)
MuonEG_Run2016B_25Oct2019        = kreator.makeDataComponent("MuonEG_Run2016B_25Oct2019"        , "/MuonEG/Run2016B_ver2-Nano25Oct2019_ver2-v1/NANOAOD"        , "CMS", ".*root", json)
DoubleMuon_Run2016B_25Oct2019     = kreator.makeDataComponent("DoubleMuon_Run2016B_25Oct2019"    , "/DoubleMuon/Run2016B_ver2-Nano25Oct2019_ver2-v1/NANOAOD"    , "CMS", ".*root", json)
Tau_Run2016B_25Oct2019     = kreator.makeDataComponent("Tau_Run2016B_25Oct2019"    , "/Tau/Run2016B_ver2-Nano25Oct2019_ver2-v1/NANOAOD"    , "CMS", ".*root", json)

dataSamples_Run2016B_25Oct2019 = [JetHT_Run2016B_25Oct2019, HTMHT_Run2016B_25Oct2019, MET_Run2016B_25Oct2019, SingleElectron_Run2016B_25Oct2019, SingleMuon_Run2016B_25Oct2019, SinglePhoton_Run2016B_25Oct2019, DoubleEG_Run2016B_25Oct2019, MuonEG_Run2016B_25Oct2019, DoubleMuon_Run2016B_25Oct2019, Tau_Run2016B_25Oct2019]

### ----------------------------- Run2016C 25Oct2019 ----------------------------------------

JetHT_Run2016C_25Oct2019          = kreator.makeDataComponent("JetHT_Run2016C_25Oct2019"         , "/JetHT/Run2016C-Nano25Oct2019-v1/NANOAOD"         , "CMS", ".*root", json)
HTMHT_Run2016C_25Oct2019          = kreator.makeDataComponent("HTMHT_Run2016C_25Oct2019"         , "/HTMHT/Run2016C-Nano25Oct2019-v1/NANOAOD"         , "CMS", ".*root", json)
MET_Run2016C_25Oct2019            = kreator.makeDataComponent("MET_Run2016C_25Oct2019"           , "/MET/Run2016C-Nano25Oct2019-v1/NANOAOD"           , "CMS", ".*root", json)
SingleElectron_Run2016C_25Oct2019 = kreator.makeDataComponent("SingleElectron_Run2016C_25Oct2019", "/SingleElectron/Run2016C-Nano25Oct2019-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2016C_25Oct2019     = kreator.makeDataComponent("SingleMuon_Run2016C_25Oct2019"    , "/SingleMuon/Run2016C-Nano25Oct2019-v1/NANOAOD"    , "CMS", ".*root", json)
SinglePhoton_Run2016C_25Oct2019   = kreator.makeDataComponent("SinglePhoton_Run2016C_25Oct2019"  , "/SinglePhoton/Run2016C-Nano25Oct2019-v1/NANOAOD"  , "CMS", ".*root", json)
DoubleEG_Run2016C_25Oct2019       = kreator.makeDataComponent("DoubleEG_Run2016C_25Oct2019"      , "/DoubleEG/Run2016C-Nano25Oct2019-v1/NANOAOD"      , "CMS", ".*root", json)
MuonEG_Run2016C_25Oct2019         = kreator.makeDataComponent("MuonEG_Run2016C_25Oct2019"        , "/MuonEG/Run2016C-Nano25Oct2019-v1/NANOAOD"        , "CMS", ".*root", json)
DoubleMuon_Run2016C_25Oct2019     = kreator.makeDataComponent("DoubleMuon_Run2016C_25Oct2019"    , "/DoubleMuon/Run2016C-Nano25Oct2019-v1/NANOAOD"    , "CMS", ".*root", json)
Tau_Run2016C_25Oct2019            = kreator.makeDataComponent("Tau_Run2016C_25Oct2019"           , "/Tau/Run2016C-Nano25Oct2019-v1/NANOAOD"           , "CMS", ".*root", json)

dataSamples_Run2016C_25Oct2019 = [JetHT_Run2016C_25Oct2019, HTMHT_Run2016C_25Oct2019, MET_Run2016C_25Oct2019, SingleElectron_Run2016C_25Oct2019, SingleMuon_Run2016C_25Oct2019, SinglePhoton_Run2016C_25Oct2019, DoubleEG_Run2016C_25Oct2019, MuonEG_Run2016C_25Oct2019, DoubleMuon_Run2016C_25Oct2019, Tau_Run2016C_25Oct2019]


### ----------------------------- Run2016D 25Oct2019 v2 ----------------------------------------

JetHT_Run2016D_25Oct2019          = kreator.makeDataComponent("JetHT_Run2016D_25Oct2019"         , "/JetHT/Run2016D-Nano25Oct2019-v1/NANOAOD"         , "CMS", ".*root", json)
HTMHT_Run2016D_25Oct2019          = kreator.makeDataComponent("HTMHT_Run2016D_25Oct2019"         , "/HTMHT/Run2016D-Nano25Oct2019-v1/NANOAOD"         , "CMS", ".*root", json)
MET_Run2016D_25Oct2019            = kreator.makeDataComponent("MET_Run2016D_25Oct2019"           , "/MET/Run2016D-Nano25Oct2019-v1/NANOAOD"           , "CMS", ".*root", json)
SingleElectron_Run2016D_25Oct2019 = kreator.makeDataComponent("SingleElectron_Run2016D_25Oct2019", "/SingleElectron/Run2016D-Nano25Oct2019-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2016D_25Oct2019     = kreator.makeDataComponent("SingleMuon_Run2016D_25Oct2019"    , "/SingleMuon/Run2016D-Nano25Oct2019-v1/NANOAOD"    , "CMS", ".*root", json)
SinglePhoton_Run2016D_25Oct2019   = kreator.makeDataComponent("SinglePhoton_Run2016D_25Oct2019"  , "/SinglePhoton/Run2016D-Nano25Oct2019-v1/NANOAOD"  , "CMS", ".*root", json)
DoubleEG_Run2016D_25Oct2019       = kreator.makeDataComponent("DoubleEG_Run2016D_25Oct2019"      , "/DoubleEG/Run2016D-Nano25Oct2019-v1/NANOAOD"      , "CMS", ".*root", json)
MuonEG_Run2016D_25Oct2019         = kreator.makeDataComponent("MuonEG_Run2016D_25Oct2019"        , "/MuonEG/Run2016D-Nano25Oct2019-v1/NANOAOD"        , "CMS", ".*root", json)
DoubleMuon_Run2016D_25Oct2019     = kreator.makeDataComponent("DoubleMuon_Run2016D_25Oct2019"    , "/DoubleMuon/Run2016D-Nano25Oct2019-v1/NANOAOD"    , "CMS", ".*root", json)
Tau_Run2016D_25Oct2019            = kreator.makeDataComponent("Tau_Run2016D_25Oct2019"           , "/Tau/Run2016D-Nano25Oct2019-v1/NANOAOD"           , "CMS", ".*root", json)

dataSamples_Run2016D_25Oct2019 = [JetHT_Run2016D_25Oct2019, HTMHT_Run2016D_25Oct2019, MET_Run2016D_25Oct2019, SingleElectron_Run2016D_25Oct2019, SingleMuon_Run2016D_25Oct2019, SinglePhoton_Run2016D_25Oct2019, DoubleEG_Run2016D_25Oct2019, MuonEG_Run2016D_25Oct2019, DoubleMuon_Run2016D_25Oct2019, Tau_Run2016D_25Oct2019]

### ----------------------------- Run2016E 25Oct2019 v2 ----------------------------------------

JetHT_Run2016E_25Oct2019          = kreator.makeDataComponent("JetHT_Run2016E_25Oct2019"         , "/JetHT/Run2016E-Nano25Oct2019-v1/NANOAOD"         , "CMS", ".*root", json)
HTMHT_Run2016E_25Oct2019          = kreator.makeDataComponent("HTMHT_Run2016E_25Oct2019"         , "/HTMHT/Run2016E-Nano25Oct2019-v1/NANOAOD"         , "CMS", ".*root", json)
MET_Run2016E_25Oct2019            = kreator.makeDataComponent("MET_Run2016E_25Oct2019"           , "/MET/Run2016E-Nano25Oct2019-v1/NANOAOD"           , "CMS", ".*root", json)
SingleElectron_Run2016E_25Oct2019 = kreator.makeDataComponent("SingleElectron_Run2016E_25Oct2019", "/SingleElectron/Run2016E-Nano25Oct2019-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2016E_25Oct2019     = kreator.makeDataComponent("SingleMuon_Run2016E_25Oct2019"    , "/SingleMuon/Run2016E-Nano25Oct2019-v1/NANOAOD"    , "CMS", ".*root", json)
SinglePhoton_Run2016E_25Oct2019   = kreator.makeDataComponent("SinglePhoton_Run2016E_25Oct2019"  , "/SinglePhoton/Run2016E-Nano25Oct2019-v1/NANOAOD"  , "CMS", ".*root", json)
DoubleEG_Run2016E_25Oct2019       = kreator.makeDataComponent("DoubleEG_Run2016E_25Oct2019"      , "/DoubleEG/Run2016E-Nano25Oct2019-v1/NANOAOD"      , "CMS", ".*root", json)
MuonEG_Run2016E_25Oct2019         = kreator.makeDataComponent("MuonEG_Run2016E_25Oct2019"        , "/MuonEG/Run2016E-Nano25Oct2019-v1/NANOAOD"        , "CMS", ".*root", json)
DoubleMuon_Run2016E_25Oct2019     = kreator.makeDataComponent("DoubleMuon_Run2016E_25Oct2019"    , "/DoubleMuon/Run2016E-Nano25Oct2019-v1/NANOAOD"    , "CMS", ".*root", json)
Tau_Run2016E_25Oct2019            = kreator.makeDataComponent("Tau_Run2016E_25Oct2019"           , "/Tau/Run2016E-Nano25Oct2019-v1/NANOAOD"           , "CMS", ".*root", json)

dataSamples_Run2016E_25Oct2019 = [JetHT_Run2016E_25Oct2019, HTMHT_Run2016E_25Oct2019, MET_Run2016E_25Oct2019, SingleElectron_Run2016E_25Oct2019, SingleMuon_Run2016E_25Oct2019, SinglePhoton_Run2016E_25Oct2019, DoubleEG_Run2016E_25Oct2019, MuonEG_Run2016E_25Oct2019, DoubleMuon_Run2016E_25Oct2019, Tau_Run2016E_25Oct2019]


### ----------------------------- Run2016F 25Oct2019 v1 ----------------------------------------

JetHT_Run2016F_25Oct2019          = kreator.makeDataComponent("JetHT_Run2016F_25Oct2019"         , "/JetHT/Run2016F-Nano25Oct2019-v1/NANOAOD"         , "CMS", ".*root", json)
HTMHT_Run2016F_25Oct2019          = kreator.makeDataComponent("HTMHT_Run2016F_25Oct2019"         , "/HTMHT/Run2016F-Nano25Oct2019-v1/NANOAOD"         , "CMS", ".*root", json)
MET_Run2016F_25Oct2019            = kreator.makeDataComponent("MET_Run2016F_25Oct2019"           , "/MET/Run2016F-Nano25Oct2019-v1/NANOAOD"           , "CMS", ".*root", json)
SingleElectron_Run2016F_25Oct2019 = kreator.makeDataComponent("SingleElectron_Run2016F_25Oct2019", "/SingleElectron/Run2016F-Nano25Oct2019-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2016F_25Oct2019     = kreator.makeDataComponent("SingleMuon_Run2016F_25Oct2019"    , "/SingleMuon/Run2016F-Nano25Oct2019-v1/NANOAOD"    , "CMS", ".*root", json)
SinglePhoton_Run2016F_25Oct2019   = kreator.makeDataComponent("SinglePhoton_Run2016F_25Oct2019"  , "/SinglePhoton/Run2016F-Nano25Oct2019-v1/NANOAOD"  , "CMS", ".*root", json)
DoubleEG_Run2016F_25Oct2019       = kreator.makeDataComponent("DoubleEG_Run2016F_25Oct2019"      , "/DoubleEG/Run2016F-Nano25Oct2019-v1/NANOAOD"      , "CMS", ".*root", json)
MuonEG_Run2016F_25Oct2019         = kreator.makeDataComponent("MuonEG_Run2016F_25Oct2019"        , "/MuonEG/Run2016F-Nano25Oct2019-v1/NANOAOD"        , "CMS", ".*root", json)
DoubleMuon_Run2016F_25Oct2019     = kreator.makeDataComponent("DoubleMuon_Run2016F_25Oct2019"    , "/DoubleMuon/Run2016F-Nano25Oct2019-v1/NANOAOD"    , "CMS", ".*root", json)
#Tau_Run2016F_25Oct2019            = kreator.makeDataComponent("Tau_Run2016F_25Oct2019"           , "/Tau/Run2016F-Nano25Oct2019-v1/NANOAOD"           , "CMS", ".*root", json)

dataSamples_Run2016F_25Oct2019 = [JetHT_Run2016F_25Oct2019, HTMHT_Run2016F_25Oct2019, MET_Run2016F_25Oct2019, SingleElectron_Run2016F_25Oct2019, SingleMuon_Run2016F_25Oct2019, SinglePhoton_Run2016F_25Oct2019, DoubleEG_Run2016F_25Oct2019, MuonEG_Run2016F_25Oct2019, DoubleMuon_Run2016F_25Oct2019,
# Tau_Run2016F_25Oct2019
]

### ----------------------------- Run2016G 25Oct2019 v1 ----------------------------------------

JetHT_Run2016G_25Oct2019          = kreator.makeDataComponent("JetHT_Run2016G_25Oct2019"         , "/JetHT/Run2016G-Nano25Oct2019-v1/NANOAOD"         , "CMS", ".*root", json)
HTMHT_Run2016G_25Oct2019          = kreator.makeDataComponent("HTMHT_Run2016G_25Oct2019"         , "/HTMHT/Run2016G-Nano25Oct2019-v1/NANOAOD"         , "CMS", ".*root", json)
MET_Run2016G_25Oct2019            = kreator.makeDataComponent("MET_Run2016G_25Oct2019"           , "/MET/Run2016G-Nano25Oct2019-v1/NANOAOD"           , "CMS", ".*root", json)
SingleElectron_Run2016G_25Oct2019 = kreator.makeDataComponent("SingleElectron_Run2016G_25Oct2019", "/SingleElectron/Run2016G-Nano25Oct2019-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2016G_25Oct2019     = kreator.makeDataComponent("SingleMuon_Run2016G_25Oct2019"    , "/SingleMuon/Run2016G-Nano25Oct2019-v1/NANOAOD"    , "CMS", ".*root", json)
SinglePhoton_Run2016G_25Oct2019   = kreator.makeDataComponent("SinglePhoton_Run2016G_25Oct2019"  , "/SinglePhoton/Run2016G-Nano25Oct2019-v1/NANOAOD"  , "CMS", ".*root", json)
DoubleEG_Run2016G_25Oct2019       = kreator.makeDataComponent("DoubleEG_Run2016G_25Oct2019"      , "/DoubleEG/Run2016G-Nano25Oct2019-v1/NANOAOD"      , "CMS", ".*root", json)
MuonEG_Run2016G_25Oct2019        = kreator.makeDataComponent("MuonEG_Run2016G_25Oct2019"        , "/MuonEG/Run2016G-Nano25Oct2019-v1/NANOAOD"        , "CMS", ".*root", json)
DoubleMuon_Run2016G_25Oct2019     = kreator.makeDataComponent("DoubleMuon_Run2016G_25Oct2019"    , "/DoubleMuon/Run2016G-Nano25Oct2019-v1/NANOAOD"    , "CMS", ".*root", json)
Tau_Run2016G_25Oct2019     = kreator.makeDataComponent("Tau_Run2016G_25Oct2019"    , "/Tau/Run2016G-Nano25Oct2019-v1/NANOAOD"    , "CMS", ".*root", json)

dataSamples_Run2016G_25Oct2019 = [JetHT_Run2016G_25Oct2019, HTMHT_Run2016G_25Oct2019, MET_Run2016G_25Oct2019, SingleElectron_Run2016G_25Oct2019, SingleMuon_Run2016G_25Oct2019, SinglePhoton_Run2016G_25Oct2019, DoubleEG_Run2016G_25Oct2019, MuonEG_Run2016G_25Oct2019, DoubleMuon_Run2016G_25Oct2019, Tau_Run2016G_25Oct2019]

### ----------------------------- Run2016H 25Oct2019 v1 ----------------------------------------

JetHT_Run2016H_25Oct2019          = kreator.makeDataComponent("JetHT_Run2016H_25Oct2019"         , "/JetHT/Run2016H-Nano25Oct2019-v1/NANOAOD"         , "CMS", ".*root", json)
HTMHT_Run2016H_25Oct2019          = kreator.makeDataComponent("HTMHT_Run2016H_25Oct2019"         , "/HTMHT/Run2016H-Nano25Oct2019-v1/NANOAOD"         , "CMS", ".*root", json)
MET_Run2016H_25Oct2019            = kreator.makeDataComponent("MET_Run2016H_25Oct2019"           , "/MET/Run2016H-Nano25Oct2019-v1/NANOAOD"           , "CMS", ".*root", json)
SingleElectron_Run2016H_25Oct2019 = kreator.makeDataComponent("SingleElectron_Run2016H_25Oct2019", "/SingleElectron/Run2016H-Nano25Oct2019-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2016H_25Oct2019     = kreator.makeDataComponent("SingleMuon_Run2016H_25Oct2019"    , "/SingleMuon/Run2016H-Nano25Oct2019-v1/NANOAOD"    , "CMS", ".*root", json)
SinglePhoton_Run2016H_25Oct2019   = kreator.makeDataComponent("SinglePhoton_Run2016H_25Oct2019"  , "/SinglePhoton/Run2016H-Nano25Oct2019-v1/NANOAOD"  , "CMS", ".*root", json)
DoubleEG_Run2016H_25Oct2019       = kreator.makeDataComponent("DoubleEG_Run2016H_25Oct2019"      , "/DoubleEG/Run2016H-Nano25Oct2019-v1/NANOAOD"      , "CMS", ".*root", json)
MuonEG_Run2016H_25Oct2019        = kreator.makeDataComponent("MuonEG_Run2016H_25Oct2019"        , "/MuonEG/Run2016H-Nano25Oct2019-v1/NANOAOD"        , "CMS", ".*root", json)
DoubleMuon_Run2016H_25Oct2019     = kreator.makeDataComponent("DoubleMuon_Run2016H_25Oct2019"    , "/DoubleMuon/Run2016H-Nano25Oct2019-v1/NANOAOD"    , "CMS", ".*root", json)
Tau_Run2016H_25Oct2019     = kreator.makeDataComponent("Tau_Run2016H_25Oct2019"    , "/Tau/Run2016H-Nano25Oct2019-v1/NANOAOD"    , "CMS", ".*root", json)

dataSamples_Run2016H_25Oct2019 = [JetHT_Run2016H_25Oct2019, HTMHT_Run2016H_25Oct2019, MET_Run2016H_25Oct2019, SingleElectron_Run2016H_25Oct2019, SingleMuon_Run2016H_25Oct2019, SinglePhoton_Run2016H_25Oct2019, DoubleEG_Run2016H_25Oct2019, MuonEG_Run2016H_25Oct2019, DoubleMuon_Run2016H_25Oct2019, Tau_Run2016H_25Oct2019]


### Summary of prompt reco
dataSamples_25Oct2019 = dataSamples_Run2016B_25Oct2019 + dataSamples_Run2016C_25Oct2019 + dataSamples_Run2016D_25Oct2019 + dataSamples_Run2016E_25Oct2019 + dataSamples_Run2016F_25Oct2019 + dataSamples_Run2016G_25Oct2019 + dataSamples_Run2016H_25Oct2019

dataSamples = dataSamples_14Dec2018 + dataSamples_1June2019 + dataSamples_25Oct2019
samples = dataSamples

### ---------------------------------------------------------------------


if __name__ == "__main__":
    from CMGTools.RootTools.samples.tools import runMain
    runMain(samples, localobjs=locals())
