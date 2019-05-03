from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()

json='/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/ReReco/Final/Cert_271036-284044_13TeV_14Dec2018ReReco_Collisions16_JSON.txt'

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

### Summary of prompt reco
dataSamples_14Dec2018 = dataSamples_Run2016B_14Dec2018 + dataSamples_Run2016C_14Dec2018 + dataSamples_Run2016D_14Dec2018 + dataSamples_Run2016E_14Dec2018 + dataSamples_Run2016F_14Dec2018 + dataSamples_Run2016G_14Dec2018

dataSamples = dataSamples_14Dec2018
samples = dataSamples

### ---------------------------------------------------------------------


if __name__ == "__main__":
    from CMGTools.RootTools.samples.tools import runMain
    runMain(samples, localobjs=locals())
