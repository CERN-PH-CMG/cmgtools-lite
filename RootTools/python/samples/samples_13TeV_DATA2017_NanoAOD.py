# COMPONENT CREATOR
from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()

# ----------------------------- 2017 pp run  ----------------------------------------

json = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/ReReco/Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON_v1.txt'

# ----------------------------- Run2017B 14Dec2018 ----------------------------------------

JetHT_Run2017B_14Dec2018 = kreator.makeDataComponent("JetHT_Run2017B_14Dec2018", "/JetHT/Run2017B-Nano14Dec2018-v1/NANOAOD", "CMS", ".*root", json)
HTMHT_Run2017B_14Dec2018 = kreator.makeDataComponent("HTMHT_Run2017B_14Dec2018", "/HTMHT/Run2017B-Nano14Dec2018-v1/NANOAOD", "CMS", ".*root", json)
MET_Run2017B_14Dec2018 = kreator.makeDataComponent("MET_Run2017B_14Dec2018", "/MET/Run2017B-Nano14Dec2018-v1/NANOAOD", "CMS", ".*root", json)
SingleElectron_Run2017B_14Dec2018 = kreator.makeDataComponent("SingleElectron_Run2017B_14Dec2018", "/SingleElectron/Run2017B-Nano14Dec2018-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2017B_14Dec2018 = kreator.makeDataComponent("SingleMuon_Run2017B_14Dec2018", "/SingleMuon/Run2017B-Nano14Dec2018-v1/NANOAOD", "CMS", ".*root", json)
SinglePhoton_Run2017B_14Dec2018 = kreator.makeDataComponent("SinglePhoton_Run2017B_14Dec2018", "/SinglePhoton/Run2017B-Nano14Dec2018-v1/NANOAOD", "CMS", ".*root", json)
DoubleEG_Run2017B_14Dec2018 = kreator.makeDataComponent("DoubleEG_Run2017B_14Dec2018", "/DoubleEG/Run2017B-Nano14Dec2018-v1/NANOAOD", "CMS", ".*root", json)
MuonEG_Run2017B_14Dec2018 = kreator.makeDataComponent("MuonEG_Run2017B_14Dec2018", "/MuonEG/Run2017B-Nano14Dec2018-v1/NANOAOD", "CMS", ".*root", json)
DoubleMuon_Run2017B_14Dec2018 = kreator.makeDataComponent("DoubleMuon_Run2017B_14Dec2018", "/DoubleMuon/Run2017B-Nano14Dec2018-v1/NANOAOD", "CMS", ".*root", json)
Tau_Run2017B_14Dec2018 = kreator.makeDataComponent("Tau_Run2017B_14Dec2018", "/Tau/Run2017B-Nano14Dec2018-v1/NANOAOD", "CMS", ".*root", json)

dataSamples_Run2017B_14Dec2018 = [JetHT_Run2017B_14Dec2018, HTMHT_Run2017B_14Dec2018, MET_Run2017B_14Dec2018, SingleElectron_Run2017B_14Dec2018, SingleMuon_Run2017B_14Dec2018, SinglePhoton_Run2017B_14Dec2018, DoubleEG_Run2017B_14Dec2018, MuonEG_Run2017B_14Dec2018, DoubleMuon_Run2017B_14Dec2018, Tau_Run2017B_14Dec2018]

# ----------------------------- Run2017C 14Dec2018 ----------------------------------------

JetHT_Run2017C_14Dec2018 = kreator.makeDataComponent("JetHT_Run2017C_14Dec2018", "/JetHT/Run2017C-Nano14Dec2018-v1/NANOAOD", "CMS", ".*root", json)
HTMHT_Run2017C_14Dec2018 = kreator.makeDataComponent("HTMHT_Run2017C_14Dec2018", "/HTMHT/Run2017C-Nano14Dec2018-v1/NANOAOD", "CMS", ".*root", json)
MET_Run2017C_14Dec2018 = kreator.makeDataComponent("MET_Run2017C_14Dec2018", "/MET/Run2017C-Nano14Dec2018-v1/NANOAOD", "CMS", ".*root", json)
SingleElectron_Run2017C_14Dec2018 = kreator.makeDataComponent("SingleElectron_Run2017C_14Dec2018", "/SingleElectron/Run2017C-Nano14Dec2018-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2017C_14Dec2018 = kreator.makeDataComponent("SingleMuon_Run2017C_14Dec2018", "/SingleMuon/Run2017C-Nano14Dec2018-v1/NANOAOD", "CMS", ".*root", json)
SinglePhoton_Run2017C_14Dec2018 = kreator.makeDataComponent("SinglePhoton_Run2017C_14Dec2018", "/SinglePhoton/Run2017C-Nano14Dec2018-v1/NANOAOD", "CMS", ".*root", json)
DoubleEG_Run2017C_14Dec2018 = kreator.makeDataComponent("DoubleEG_Run2017C_14Dec2018", "/DoubleEG/Run2017C-Nano14Dec2018-v1/NANOAOD", "CMS", ".*root", json)
MuonEG_Run2017C_14Dec2018 = kreator.makeDataComponent("MuonEG_Run2017C_14Dec2018", "/MuonEG/Run2017C-Nano14Dec2018-v1/NANOAOD", "CMS", ".*root", json)
DoubleMuon_Run2017C_14Dec2018 = kreator.makeDataComponent("DoubleMuon_Run2017C_14Dec2018", "/DoubleMuon/Run2017C-Nano14Dec2018-v1/NANOAOD", "CMS", ".*root", json)
Tau_Run2017C_14Dec2018 = kreator.makeDataComponent("Tau_Run2017C_14Dec2018", "/Tau/Run2017C-Nano14Dec2018-v1/NANOAOD", "CMS", ".*root", json)

dataSamples_Run2017C_14Dec2018 = [JetHT_Run2017C_14Dec2018, HTMHT_Run2017C_14Dec2018, MET_Run2017C_14Dec2018, SingleElectron_Run2017C_14Dec2018, SingleMuon_Run2017C_14Dec2018, SinglePhoton_Run2017C_14Dec2018, DoubleEG_Run2017C_14Dec2018, MuonEG_Run2017C_14Dec2018, DoubleMuon_Run2017C_14Dec2018, Tau_Run2017C_14Dec2018]


# ----------------------------- Run2017D 14Dec2018 ----------------------------------------

JetHT_Run2017D_14Dec2018 = kreator.makeDataComponent("JetHT_Run2017D_14Dec2018", "/JetHT/Run2017D-Nano14Dec2018-v1/NANOAOD", "CMS", ".*root", json)
HTMHT_Run2017D_14Dec2018 = kreator.makeDataComponent("HTMHT_Run2017D_14Dec2018", "/HTMHT/Run2017D-Nano14Dec2018-v1/NANOAOD", "CMS", ".*root", json)
MET_Run2017D_14Dec2018 = kreator.makeDataComponent("MET_Run2017D_14Dec2018", "/MET/Run2017D-Nano14Dec2018-v1/NANOAOD", "CMS", ".*root", json)
SingleElectron_Run2017D_14Dec2018 = kreator.makeDataComponent("SingleElectron_Run2017D_14Dec2018", "/SingleElectron/Run2017D-Nano14Dec2018-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2017D_14Dec2018 = kreator.makeDataComponent("SingleMuon_Run2017D_14Dec2018", "/SingleMuon/Run2017D-Nano14Dec2018-v1/NANOAOD", "CMS", ".*root", json)
SinglePhoton_Run2017D_14Dec2018 = kreator.makeDataComponent("SinglePhoton_Run2017D_14Dec2018", "/SinglePhoton/Run2017D-Nano14Dec2018-v1/NANOAOD", "CMS", ".*root", json)
DoubleEG_Run2017D_14Dec2018 = kreator.makeDataComponent("DoubleEG_Run2017D_14Dec2018", "/DoubleEG/Run2017D-Nano14Dec2018-v1/NANOAOD", "CMS", ".*root", json)
MuonEG_Run2017D_14Dec2018 = kreator.makeDataComponent("MuonEG_Run2017D_14Dec2018", "/MuonEG/Run2017D-Nano14Dec2018-v1/NANOAOD", "CMS", ".*root", json)
DoubleMuon_Run2017D_14Dec2018 = kreator.makeDataComponent("DoubleMuon_Run2017D_14Dec2018", "/DoubleMuon/Run2017D-Nano14Dec2018-v1/NANOAOD", "CMS", ".*root", json)
Tau_Run2017D_14Dec2018 = kreator.makeDataComponent("Tau_Run2017D_14Dec2018", "/Tau/Run2017D-Nano14Dec2018-v1/NANOAOD", "CMS", ".*root", json)

dataSamples_Run2017D_14Dec2018 = [JetHT_Run2017D_14Dec2018, HTMHT_Run2017D_14Dec2018, MET_Run2017D_14Dec2018, SingleElectron_Run2017D_14Dec2018, SingleMuon_Run2017D_14Dec2018, SinglePhoton_Run2017D_14Dec2018, DoubleEG_Run2017D_14Dec2018, MuonEG_Run2017D_14Dec2018, DoubleMuon_Run2017D_14Dec2018, Tau_Run2017D_14Dec2018]

# ----------------------------- Run2017E 14Dec2018 ----------------------------------------

JetHT_Run2017E_14Dec2018 = kreator.makeDataComponent("JetHT_Run2017E_14Dec2018", "/JetHT/Run2017E-Nano14Dec2018-v1/NANOAOD", "CMS", ".*root", json)
HTMHT_Run2017E_14Dec2018 = kreator.makeDataComponent("HTMHT_Run2017E_14Dec2018", "/HTMHT/Run2017E-Nano14Dec2018-v1/NANOAOD", "CMS", ".*root", json)
MET_Run2017E_14Dec2018 = kreator.makeDataComponent("MET_Run2017E_14Dec2018", "/MET/Run2017E-Nano14Dec2018-v1/NANOAOD", "CMS", ".*root", json)
SingleElectron_Run2017E_14Dec2018 = kreator.makeDataComponent("SingleElectron_Run2017E_14Dec2018", "/SingleElectron/Run2017E-Nano14Dec2018-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2017E_14Dec2018 = kreator.makeDataComponent("SingleMuon_Run2017E_14Dec2018", "/SingleMuon/Run2017E-Nano14Dec2018-v1/NANOAOD", "CMS", ".*root", json)
SinglePhoton_Run2017E_14Dec2018 = kreator.makeDataComponent("SinglePhoton_Run2017E_14Dec2018", "/SinglePhoton/Run2017E-Nano14Dec2018-v1/NANOAOD", "CMS", ".*root", json)
DoubleEG_Run2017E_14Dec2018 = kreator.makeDataComponent("DoubleEG_Run2017E_14Dec2018", "/DoubleEG/Run2017E-Nano14Dec2018-v1/NANOAOD", "CMS", ".*root", json)
MuonEG_Run2017E_14Dec2018 = kreator.makeDataComponent("MuonEG_Run2017E_14Dec2018", "/MuonEG/Run2017E-Nano14Dec2018-v1/NANOAOD", "CMS", ".*root", json)
DoubleMuon_Run2017E_14Dec2018 = kreator.makeDataComponent("DoubleMuon_Run2017E_14Dec2018", "/DoubleMuon/Run2017E-Nano14Dec2018-v1/NANOAOD", "CMS", ".*root", json)
Tau_Run2017E_14Dec2018 = kreator.makeDataComponent("Tau_Run2017E_14Dec2018", "/Tau/Run2017E-Nano14Dec2018-v1/NANOAOD", "CMS", ".*root", json)

dataSamples_Run2017E_14Dec2018 = [JetHT_Run2017E_14Dec2018, HTMHT_Run2017E_14Dec2018, MET_Run2017E_14Dec2018, SingleElectron_Run2017E_14Dec2018, SingleMuon_Run2017E_14Dec2018, SinglePhoton_Run2017E_14Dec2018, DoubleEG_Run2017E_14Dec2018, MuonEG_Run2017E_14Dec2018, DoubleMuon_Run2017E_14Dec2018, Tau_Run2017E_14Dec2018]


# ----------------------------- Run2017F 14Dec2018 ----------------------------------------

JetHT_Run2017F_14Dec2018 = kreator.makeDataComponent("JetHT_Run2017F_14Dec2018", "/JetHT/Run2017F-Nano14Dec2018-v1/NANOAOD", "CMS", ".*root", json)
HTMHT_Run2017F_14Dec2018 = kreator.makeDataComponent("HTMHT_Run2017F_14Dec2018", "/HTMHT/Run2017F-Nano14Dec2018-v1/NANOAOD", "CMS", ".*root", json)
MET_Run2017F_14Dec2018 = kreator.makeDataComponent("MET_Run2017F_14Dec2018", "/MET/Run2017F-Nano14Dec2018-v1/NANOAOD", "CMS", ".*root", json)
SingleElectron_Run2017F_14Dec2018 = kreator.makeDataComponent("SingleElectron_Run2017F_14Dec2018", "/SingleElectron/Run2017F-Nano14Dec2018-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2017F_14Dec2018 = kreator.makeDataComponent("SingleMuon_Run2017F_14Dec2018", "/SingleMuon/Run2017F-Nano14Dec2018-v1/NANOAOD", "CMS", ".*root", json)
SinglePhoton_Run2017F_14Dec2018 = kreator.makeDataComponent("SinglePhoton_Run2017F_14Dec2018", "/SinglePhoton/Run2017F-Nano14Dec2018-v1/NANOAOD", "CMS", ".*root", json)
DoubleEG_Run2017F_14Dec2018 = kreator.makeDataComponent("DoubleEG_Run2017F_14Dec2018", "/DoubleEG/Run2017F-Nano14Dec2018-v1/NANOAOD", "CMS", ".*root", json)
MuonEG_Run2017F_14Dec2018 = kreator.makeDataComponent("MuonEG_Run2017F_14Dec2018", "/MuonEG/Run2017F-Nano14Dec2018-v1/NANOAOD", "CMS", ".*root", json)
DoubleMuon_Run2017F_14Dec2018 = kreator.makeDataComponent("DoubleMuon_Run2017F_14Dec2018", "/DoubleMuon/Run2017F-Nano14Dec2018-v1/NANOAOD", "CMS", ".*root", json)
Tau_Run2017F_14Dec2018 = kreator.makeDataComponent("Tau_Run2017F_14Dec2018", "/Tau/Run2017F-Nano14Dec2018-v1/NANOAOD", "CMS", ".*root", json)

dataSamples_Run2017F_14Dec2018 = [JetHT_Run2017F_14Dec2018, HTMHT_Run2017F_14Dec2018, MET_Run2017F_14Dec2018, SingleElectron_Run2017F_14Dec2018, SingleMuon_Run2017F_14Dec2018, SinglePhoton_Run2017F_14Dec2018, DoubleEG_Run2017F_14Dec2018, MuonEG_Run2017F_14Dec2018, DoubleMuon_Run2017F_14Dec2018, Tau_Run2017F_14Dec2018]

# Summary of 14Dec2018
dataSamples_14Dec2018 = dataSamples_Run2017B_14Dec2018 + dataSamples_Run2017C_14Dec2018 + dataSamples_Run2017D_14Dec2018 + dataSamples_Run2017E_14Dec2018 + dataSamples_Run2017F_14Dec2018

# ----------------------------- Run2017B 1June2019 ----------------------------------------

JetHT_Run2017B_1June2019 = kreator.makeDataComponent("JetHT_Run2017B_1June2019", "/JetHT/Run2017B-Nano1June2019-v1/NANOAOD", "CMS", ".*root", json)
HTMHT_Run2017B_1June2019 = kreator.makeDataComponent("HTMHT_Run2017B_1June2019", "/HTMHT/Run2017B-Nano1June2019-v1/NANOAOD", "CMS", ".*root", json)
MET_Run2017B_1June2019 = kreator.makeDataComponent("MET_Run2017B_1June2019", "/MET/Run2017B-Nano1June2019-v1/NANOAOD", "CMS", ".*root", json)
SingleElectron_Run2017B_1June2019 = kreator.makeDataComponent("SingleElectron_Run2017B_1June2019", "/SingleElectron/Run2017B-Nano1June2019-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2017B_1June2019 = kreator.makeDataComponent("SingleMuon_Run2017B_1June2019", "/SingleMuon/Run2017B-Nano1June2019-v1/NANOAOD", "CMS", ".*root", json)
SinglePhoton_Run2017B_1June2019 = kreator.makeDataComponent("SinglePhoton_Run2017B_1June2019", "/SinglePhoton/Run2017B-Nano1June2019-v1/NANOAOD", "CMS", ".*root", json)
DoubleEG_Run2017B_1June2019 = kreator.makeDataComponent("DoubleEG_Run2017B_1June2019", "/DoubleEG/Run2017B-Nano1June2019-v1/NANOAOD", "CMS", ".*root", json)
MuonEG_Run2017B_1June2019 = kreator.makeDataComponent("MuonEG_Run2017B_1June2019", "/MuonEG/Run2017B-Nano1June2019-v1/NANOAOD", "CMS", ".*root", json)
DoubleMuon_Run2017B_1June2019 = kreator.makeDataComponent("DoubleMuon_Run2017B_1June2019", "/DoubleMuon/Run2017B-Nano1June2019-v1/NANOAOD", "CMS", ".*root", json)
Tau_Run2017B_1June2019 = kreator.makeDataComponent("Tau_Run2017B_1June2019", "/Tau/Run2017B-Nano1June2019-v1/NANOAOD", "CMS", ".*root", json)

dataSamples_Run2017B_1June2019 = [JetHT_Run2017B_1June2019, HTMHT_Run2017B_1June2019, MET_Run2017B_1June2019, SingleElectron_Run2017B_1June2019, SingleMuon_Run2017B_1June2019, SinglePhoton_Run2017B_1June2019, DoubleEG_Run2017B_1June2019, MuonEG_Run2017B_1June2019, DoubleMuon_Run2017B_1June2019, Tau_Run2017B_1June2019]

# ----------------------------- Run2017C 1June2019 ----------------------------------------

JetHT_Run2017C_1June2019 = kreator.makeDataComponent("JetHT_Run2017C_1June2019", "/JetHT/Run2017C-Nano1June2019-v1/NANOAOD", "CMS", ".*root", json)
HTMHT_Run2017C_1June2019 = kreator.makeDataComponent("HTMHT_Run2017C_1June2019", "/HTMHT/Run2017C-Nano1June2019-v1/NANOAOD", "CMS", ".*root", json)
MET_Run2017C_1June2019 = kreator.makeDataComponent("MET_Run2017C_1June2019", "/MET/Run2017C-Nano1June2019-v1/NANOAOD", "CMS", ".*root", json)
SingleElectron_Run2017C_1June2019 = kreator.makeDataComponent("SingleElectron_Run2017C_1June2019", "/SingleElectron/Run2017C-Nano1June2019-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2017C_1June2019 = kreator.makeDataComponent("SingleMuon_Run2017C_1June2019", "/SingleMuon/Run2017C-Nano1June2019-v1/NANOAOD", "CMS", ".*root", json)
SinglePhoton_Run2017C_1June2019 = kreator.makeDataComponent("SinglePhoton_Run2017C_1June2019", "/SinglePhoton/Run2017C-Nano1June2019-v1/NANOAOD", "CMS", ".*root", json)
DoubleEG_Run2017C_1June2019 = kreator.makeDataComponent("DoubleEG_Run2017C_1June2019", "/DoubleEG/Run2017C-Nano1June2019-v1/NANOAOD", "CMS", ".*root", json)
MuonEG_Run2017C_1June2019 = kreator.makeDataComponent("MuonEG_Run2017C_1June2019", "/MuonEG/Run2017C-Nano1June2019-v1/NANOAOD", "CMS", ".*root", json)
DoubleMuon_Run2017C_1June2019 = kreator.makeDataComponent("DoubleMuon_Run2017C_1June2019", "/DoubleMuon/Run2017C-Nano1June2019-v1/NANOAOD", "CMS", ".*root", json)
Tau_Run2017C_1June2019 = kreator.makeDataComponent("Tau_Run2017C_1June2019", "/Tau/Run2017C-Nano1June2019-v1/NANOAOD", "CMS", ".*root", json)

dataSamples_Run2017C_1June2019 = [JetHT_Run2017C_1June2019, HTMHT_Run2017C_1June2019, MET_Run2017C_1June2019, SingleElectron_Run2017C_1June2019, SingleMuon_Run2017C_1June2019, SinglePhoton_Run2017C_1June2019, DoubleEG_Run2017C_1June2019, MuonEG_Run2017C_1June2019, DoubleMuon_Run2017C_1June2019, Tau_Run2017C_1June2019]


# ----------------------------- Run2017D 1June2019 ----------------------------------------

JetHT_Run2017D_1June2019 = kreator.makeDataComponent("JetHT_Run2017D_1June2019", "/JetHT/Run2017D-Nano1June2019-v1/NANOAOD", "CMS", ".*root", json)
HTMHT_Run2017D_1June2019 = kreator.makeDataComponent("HTMHT_Run2017D_1June2019", "/HTMHT/Run2017D-Nano1June2019-v1/NANOAOD", "CMS", ".*root", json)
MET_Run2017D_1June2019 = kreator.makeDataComponent("MET_Run2017D_1June2019", "/MET/Run2017D-Nano1June2019-v1/NANOAOD", "CMS", ".*root", json)
SingleElectron_Run2017D_1June2019 = kreator.makeDataComponent("SingleElectron_Run2017D_1June2019", "/SingleElectron/Run2017D-Nano1June2019-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2017D_1June2019 = kreator.makeDataComponent("SingleMuon_Run2017D_1June2019", "/SingleMuon/Run2017D-Nano1June2019-v1/NANOAOD", "CMS", ".*root", json)
SinglePhoton_Run2017D_1June2019 = kreator.makeDataComponent("SinglePhoton_Run2017D_1June2019", "/SinglePhoton/Run2017D-Nano1June2019-v1/NANOAOD", "CMS", ".*root", json)
DoubleEG_Run2017D_1June2019 = kreator.makeDataComponent("DoubleEG_Run2017D_1June2019", "/DoubleEG/Run2017D-Nano1June2019-v1/NANOAOD", "CMS", ".*root", json)
MuonEG_Run2017D_1June2019 = kreator.makeDataComponent("MuonEG_Run2017D_1June2019", "/MuonEG/Run2017D-Nano1June2019-v1/NANOAOD", "CMS", ".*root", json)
DoubleMuon_Run2017D_1June2019 = kreator.makeDataComponent("DoubleMuon_Run2017D_1June2019", "/DoubleMuon/Run2017D-Nano1June2019-v1/NANOAOD", "CMS", ".*root", json)
Tau_Run2017D_1June2019 = kreator.makeDataComponent("Tau_Run2017D_1June2019", "/Tau/Run2017D-Nano1June2019-v1/NANOAOD", "CMS", ".*root", json)

dataSamples_Run2017D_1June2019 = [JetHT_Run2017D_1June2019, HTMHT_Run2017D_1June2019, MET_Run2017D_1June2019, SingleElectron_Run2017D_1June2019, SingleMuon_Run2017D_1June2019, SinglePhoton_Run2017D_1June2019, DoubleEG_Run2017D_1June2019, MuonEG_Run2017D_1June2019, DoubleMuon_Run2017D_1June2019, Tau_Run2017D_1June2019]

# ----------------------------- Run2017E 1June2019 ----------------------------------------

JetHT_Run2017E_1June2019 = kreator.makeDataComponent("JetHT_Run2017E_1June2019", "/JetHT/Run2017E-Nano1June2019-v1/NANOAOD", "CMS", ".*root", json)
#HTMHT_Run2017E_1June2019 = kreator.makeDataComponent("HTMHT_Run2017E_1June2019", "/HTMHT/Run2017E-Nano1June2019-v1/NANOAOD", "CMS", ".*root", json)
MET_Run2017E_1June2019 = kreator.makeDataComponent("MET_Run2017E_1June2019", "/MET/Run2017E-Nano1June2019-v1/NANOAOD", "CMS", ".*root", json)
SingleElectron_Run2017E_1June2019 = kreator.makeDataComponent("SingleElectron_Run2017E_1June2019", "/SingleElectron/Run2017E-Nano1June2019-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2017E_1June2019 = kreator.makeDataComponent("SingleMuon_Run2017E_1June2019", "/SingleMuon/Run2017E-Nano1June2019-v1/NANOAOD", "CMS", ".*root", json)
SinglePhoton_Run2017E_1June2019 = kreator.makeDataComponent("SinglePhoton_Run2017E_1June2019", "/SinglePhoton/Run2017E-Nano1June2019-v1/NANOAOD", "CMS", ".*root", json)
DoubleEG_Run2017E_1June2019 = kreator.makeDataComponent("DoubleEG_Run2017E_1June2019", "/DoubleEG/Run2017E-Nano1June2019-v1/NANOAOD", "CMS", ".*root", json)
MuonEG_Run2017E_1June2019 = kreator.makeDataComponent("MuonEG_Run2017E_1June2019", "/MuonEG/Run2017E-Nano1June2019-v1/NANOAOD", "CMS", ".*root", json)
DoubleMuon_Run2017E_1June2019 = kreator.makeDataComponent("DoubleMuon_Run2017E_1June2019", "/DoubleMuon/Run2017E-Nano1June2019-v1/NANOAOD", "CMS", ".*root", json)
Tau_Run2017E_1June2019 = kreator.makeDataComponent("Tau_Run2017E_1June2019", "/Tau/Run2017E-Nano1June2019-v1/NANOAOD", "CMS", ".*root", json)

dataSamples_Run2017E_1June2019 = [JetHT_Run2017E_1June2019,
# HTMHT_Run2017E_1June2019, 
MET_Run2017E_1June2019, SingleElectron_Run2017E_1June2019, SingleMuon_Run2017E_1June2019, SinglePhoton_Run2017E_1June2019, DoubleEG_Run2017E_1June2019, MuonEG_Run2017E_1June2019, DoubleMuon_Run2017E_1June2019, Tau_Run2017E_1June2019]


# ----------------------------- Run2017F 1June2019 ----------------------------------------

JetHT_Run2017F_1June2019 = kreator.makeDataComponent("JetHT_Run2017F_1June2019", "/JetHT/Run2017F-Nano1June2019-v1/NANOAOD", "CMS", ".*root", json)
HTMHT_Run2017F_1June2019 = kreator.makeDataComponent("HTMHT_Run2017F_1June2019", "/HTMHT/Run2017F-Nano1June2019-v1/NANOAOD", "CMS", ".*root", json)
MET_Run2017F_1June2019 = kreator.makeDataComponent("MET_Run2017F_1June2019", "/MET/Run2017F-Nano1June2019-v1/NANOAOD", "CMS", ".*root", json)
SingleElectron_Run2017F_1June2019 = kreator.makeDataComponent("SingleElectron_Run2017F_1June2019", "/SingleElectron/Run2017F-Nano1June2019-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2017F_1June2019 = kreator.makeDataComponent("SingleMuon_Run2017F_1June2019", "/SingleMuon/Run2017F-Nano1June2019-v1/NANOAOD", "CMS", ".*root", json)
SinglePhoton_Run2017F_1June2019 = kreator.makeDataComponent("SinglePhoton_Run2017F_1June2019", "/SinglePhoton/Run2017F-Nano1June2019-v1/NANOAOD", "CMS", ".*root", json)
DoubleEG_Run2017F_1June2019 = kreator.makeDataComponent("DoubleEG_Run2017F_1June2019", "/DoubleEG/Run2017F-Nano1June2019-v1/NANOAOD", "CMS", ".*root", json)
MuonEG_Run2017F_1June2019 = kreator.makeDataComponent("MuonEG_Run2017F_1June2019", "/MuonEG/Run2017F-Nano1June2019-v1/NANOAOD", "CMS", ".*root", json)
DoubleMuon_Run2017F_1June2019 = kreator.makeDataComponent("DoubleMuon_Run2017F_1June2019", "/DoubleMuon/Run2017F-Nano1June2019-v1/NANOAOD", "CMS", ".*root", json)
Tau_Run2017F_1June2019 = kreator.makeDataComponent("Tau_Run2017F_1June2019", "/Tau/Run2017F-Nano1June2019-v1/NANOAOD", "CMS", ".*root", json)

dataSamples_Run2017F_1June2019 = [JetHT_Run2017F_1June2019, HTMHT_Run2017F_1June2019, MET_Run2017F_1June2019, SingleElectron_Run2017F_1June2019, SingleMuon_Run2017F_1June2019, SinglePhoton_Run2017F_1June2019, DoubleEG_Run2017F_1June2019, MuonEG_Run2017F_1June2019, DoubleMuon_Run2017F_1June2019, Tau_Run2017F_1June2019]

# Summary of 1June2019
dataSamples_1June2019 = dataSamples_Run2017B_1June2019 + dataSamples_Run2017C_1June2019 + dataSamples_Run2017D_1June2019 + dataSamples_Run2017E_1June2019 + dataSamples_Run2017F_1June2019

# ----------------------------- Run2017B 25Oct2019 ----------------------------------------

JetHT_Run2017B_25Oct2019 = kreator.makeDataComponent("JetHT_Run2017B_25Oct2019", "/JetHT/Run2017B-Nano25Oct2019-v1/NANOAOD", "CMS", ".*root", json)
HTMHT_Run2017B_25Oct2019 = kreator.makeDataComponent("HTMHT_Run2017B_25Oct2019", "/HTMHT/Run2017B-Nano25Oct2019-v2/NANOAOD", "CMS", ".*root", json)
MET_Run2017B_25Oct2019 = kreator.makeDataComponent("MET_Run2017B_25Oct2019", "/MET/Run2017B-Nano25Oct2019-v1/NANOAOD", "CMS", ".*root", json)
SingleElectron_Run2017B_25Oct2019 = kreator.makeDataComponent("SingleElectron_Run2017B_25Oct2019", "/SingleElectron/Run2017B-Nano25Oct2019-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2017B_25Oct2019 = kreator.makeDataComponent("SingleMuon_Run2017B_25Oct2019", "/SingleMuon/Run2017B-Nano25Oct2019-v1/NANOAOD", "CMS", ".*root", json)
SinglePhoton_Run2017B_25Oct2019 = kreator.makeDataComponent("SinglePhoton_Run2017B_25Oct2019", "/SinglePhoton/Run2017B-Nano25Oct2019-v1/NANOAOD", "CMS", ".*root", json)
DoubleEG_Run2017B_25Oct2019 = kreator.makeDataComponent("DoubleEG_Run2017B_25Oct2019", "/DoubleEG/Run2017B-Nano25Oct2019-v1/NANOAOD", "CMS", ".*root", json)
MuonEG_Run2017B_25Oct2019 = kreator.makeDataComponent("MuonEG_Run2017B_25Oct2019", "/MuonEG/Run2017B-Nano25Oct2019-v1/NANOAOD", "CMS", ".*root", json)
DoubleMuon_Run2017B_25Oct2019 = kreator.makeDataComponent("DoubleMuon_Run2017B_25Oct2019", "/DoubleMuon/Run2017B-Nano25Oct2019-v1/NANOAOD", "CMS", ".*root", json)
Tau_Run2017B_25Oct2019 = kreator.makeDataComponent("Tau_Run2017B_25Oct2019", "/Tau/Run2017B-Nano25Oct2019-v1/NANOAOD", "CMS", ".*root", json)

dataSamples_Run2017B_25Oct2019 = [JetHT_Run2017B_25Oct2019, HTMHT_Run2017B_25Oct2019, MET_Run2017B_25Oct2019, SingleElectron_Run2017B_25Oct2019, SingleMuon_Run2017B_25Oct2019, SinglePhoton_Run2017B_25Oct2019, DoubleEG_Run2017B_25Oct2019, MuonEG_Run2017B_25Oct2019, DoubleMuon_Run2017B_25Oct2019, Tau_Run2017B_25Oct2019]

# ----------------------------- Run2017C 25Oct2019 ----------------------------------------

JetHT_Run2017C_25Oct2019 = kreator.makeDataComponent("JetHT_Run2017C_25Oct2019", "/JetHT/Run2017C-Nano25Oct2019-v1/NANOAOD", "CMS", ".*root", json)
HTMHT_Run2017C_25Oct2019 = kreator.makeDataComponent("HTMHT_Run2017C_25Oct2019", "/HTMHT/Run2017C-Nano25Oct2019-v1/NANOAOD", "CMS", ".*root", json)
MET_Run2017C_25Oct2019 = kreator.makeDataComponent("MET_Run2017C_25Oct2019", "/MET/Run2017C-Nano25Oct2019-v1/NANOAOD", "CMS", ".*root", json)
SingleElectron_Run2017C_25Oct2019 = kreator.makeDataComponent("SingleElectron_Run2017C_25Oct2019", "/SingleElectron/Run2017C-Nano25Oct2019-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2017C_25Oct2019 = kreator.makeDataComponent("SingleMuon_Run2017C_25Oct2019", "/SingleMuon/Run2017C-Nano25Oct2019-v1/NANOAOD", "CMS", ".*root", json)
SinglePhoton_Run2017C_25Oct2019 = kreator.makeDataComponent("SinglePhoton_Run2017C_25Oct2019", "/SinglePhoton/Run2017C-Nano25Oct2019-v1/NANOAOD", "CMS", ".*root", json)
DoubleEG_Run2017C_25Oct2019 = kreator.makeDataComponent("DoubleEG_Run2017C_25Oct2019", "/DoubleEG/Run2017C-Nano25Oct2019-v1/NANOAOD", "CMS", ".*root", json)
MuonEG_Run2017C_25Oct2019 = kreator.makeDataComponent("MuonEG_Run2017C_25Oct2019", "/MuonEG/Run2017C-Nano25Oct2019-v1/NANOAOD", "CMS", ".*root", json)
DoubleMuon_Run2017C_25Oct2019 = kreator.makeDataComponent("DoubleMuon_Run2017C_25Oct2019", "/DoubleMuon/Run2017C-Nano25Oct2019-v1/NANOAOD", "CMS", ".*root", json)
Tau_Run2017C_25Oct2019 = kreator.makeDataComponent("Tau_Run2017C_25Oct2019", "/Tau/Run2017C-Nano25Oct2019-v1/NANOAOD", "CMS", ".*root", json)

dataSamples_Run2017C_25Oct2019 = [JetHT_Run2017C_25Oct2019, HTMHT_Run2017C_25Oct2019, MET_Run2017C_25Oct2019, SingleElectron_Run2017C_25Oct2019, SingleMuon_Run2017C_25Oct2019, SinglePhoton_Run2017C_25Oct2019, DoubleEG_Run2017C_25Oct2019, MuonEG_Run2017C_25Oct2019, DoubleMuon_Run2017C_25Oct2019, Tau_Run2017C_25Oct2019]


# ----------------------------- Run2017D 25Oct2019 ----------------------------------------

JetHT_Run2017D_25Oct2019 = kreator.makeDataComponent("JetHT_Run2017D_25Oct2019", "/JetHT/Run2017D-Nano25Oct2019-v1/NANOAOD", "CMS", ".*root", json)
HTMHT_Run2017D_25Oct2019 = kreator.makeDataComponent("HTMHT_Run2017D_25Oct2019", "/HTMHT/Run2017D-Nano25Oct2019-v1/NANOAOD", "CMS", ".*root", json)
MET_Run2017D_25Oct2019 = kreator.makeDataComponent("MET_Run2017D_25Oct2019", "/MET/Run2017D-Nano25Oct2019-v1/NANOAOD", "CMS", ".*root", json)
SingleElectron_Run2017D_25Oct2019 = kreator.makeDataComponent("SingleElectron_Run2017D_25Oct2019", "/SingleElectron/Run2017D-Nano25Oct2019-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2017D_25Oct2019 = kreator.makeDataComponent("SingleMuon_Run2017D_25Oct2019", "/SingleMuon/Run2017D-Nano25Oct2019-v1/NANOAOD", "CMS", ".*root", json)
SinglePhoton_Run2017D_25Oct2019 = kreator.makeDataComponent("SinglePhoton_Run2017D_25Oct2019", "/SinglePhoton/Run2017D-Nano25Oct2019-v1/NANOAOD", "CMS", ".*root", json)
DoubleEG_Run2017D_25Oct2019 = kreator.makeDataComponent("DoubleEG_Run2017D_25Oct2019", "/DoubleEG/Run2017D-Nano25Oct2019-v1/NANOAOD", "CMS", ".*root", json)
MuonEG_Run2017D_25Oct2019 = kreator.makeDataComponent("MuonEG_Run2017D_25Oct2019", "/MuonEG/Run2017D-Nano25Oct2019-v1/NANOAOD", "CMS", ".*root", json)
DoubleMuon_Run2017D_25Oct2019 = kreator.makeDataComponent("DoubleMuon_Run2017D_25Oct2019", "/DoubleMuon/Run2017D-Nano25Oct2019-v1/NANOAOD", "CMS", ".*root", json)
Tau_Run2017D_25Oct2019 = kreator.makeDataComponent("Tau_Run2017D_25Oct2019", "/Tau/Run2017D-Nano25Oct2019-v1/NANOAOD", "CMS", ".*root", json)

dataSamples_Run2017D_25Oct2019 = [JetHT_Run2017D_25Oct2019, HTMHT_Run2017D_25Oct2019, MET_Run2017D_25Oct2019, SingleElectron_Run2017D_25Oct2019, SingleMuon_Run2017D_25Oct2019, SinglePhoton_Run2017D_25Oct2019, DoubleEG_Run2017D_25Oct2019, MuonEG_Run2017D_25Oct2019, DoubleMuon_Run2017D_25Oct2019, Tau_Run2017D_25Oct2019]

# ----------------------------- Run2017E 25Oct2019 ----------------------------------------

JetHT_Run2017E_25Oct2019 = kreator.makeDataComponent("JetHT_Run2017E_25Oct2019", "/JetHT/Run2017E-Nano25Oct2019-v1/NANOAOD", "CMS", ".*root", json)
#HTMHT_Run2017E_25Oct2019 = kreator.makeDataComponent("HTMHT_Run2017E_25Oct2019", "/HTMHT/Run2017E-Nano25Oct2019-v1/NANOAOD", "CMS", ".*root", json)
MET_Run2017E_25Oct2019 = kreator.makeDataComponent("MET_Run2017E_25Oct2019", "/MET/Run2017E-Nano25Oct2019-v1/NANOAOD", "CMS", ".*root", json)
SingleElectron_Run2017E_25Oct2019 = kreator.makeDataComponent("SingleElectron_Run2017E_25Oct2019", "/SingleElectron/Run2017E-Nano25Oct2019-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2017E_25Oct2019 = kreator.makeDataComponent("SingleMuon_Run2017E_25Oct2019", "/SingleMuon/Run2017E-Nano25Oct2019-v1/NANOAOD", "CMS", ".*root", json)
SinglePhoton_Run2017E_25Oct2019 = kreator.makeDataComponent("SinglePhoton_Run2017E_25Oct2019", "/SinglePhoton/Run2017E-Nano25Oct2019-v1/NANOAOD", "CMS", ".*root", json)
DoubleEG_Run2017E_25Oct2019 = kreator.makeDataComponent("DoubleEG_Run2017E_25Oct2019", "/DoubleEG/Run2017E-Nano25Oct2019-v1/NANOAOD", "CMS", ".*root", json)
MuonEG_Run2017E_25Oct2019 = kreator.makeDataComponent("MuonEG_Run2017E_25Oct2019", "/MuonEG/Run2017E-Nano25Oct2019-v1/NANOAOD", "CMS", ".*root", json)
DoubleMuon_Run2017E_25Oct2019 = kreator.makeDataComponent("DoubleMuon_Run2017E_25Oct2019", "/DoubleMuon/Run2017E-Nano25Oct2019-v1/NANOAOD", "CMS", ".*root", json)
Tau_Run2017E_25Oct2019 = kreator.makeDataComponent("Tau_Run2017E_25Oct2019", "/Tau/Run2017E-Nano25Oct2019-v1/NANOAOD", "CMS", ".*root", json)

dataSamples_Run2017E_25Oct2019 = [JetHT_Run2017E_25Oct2019,
# HTMHT_Run2017E_25Oct2019, 
MET_Run2017E_25Oct2019, SingleElectron_Run2017E_25Oct2019, SingleMuon_Run2017E_25Oct2019, SinglePhoton_Run2017E_25Oct2019, DoubleEG_Run2017E_25Oct2019, MuonEG_Run2017E_25Oct2019, DoubleMuon_Run2017E_25Oct2019, Tau_Run2017E_25Oct2019]


# ----------------------------- Run2017F 25Oct2019 ----------------------------------------

JetHT_Run2017F_25Oct2019 = kreator.makeDataComponent("JetHT_Run2017F_25Oct2019", "/JetHT/Run2017F-Nano25Oct2019-v1/NANOAOD", "CMS", ".*root", json)
HTMHT_Run2017F_25Oct2019 = kreator.makeDataComponent("HTMHT_Run2017F_25Oct2019", "/HTMHT/Run2017F-Nano25Oct2019-v1/NANOAOD", "CMS", ".*root", json)
MET_Run2017F_25Oct2019 = kreator.makeDataComponent("MET_Run2017F_25Oct2019", "/MET/Run2017F-Nano25Oct2019-v1/NANOAOD", "CMS", ".*root", json)
SingleElectron_Run2017F_25Oct2019 = kreator.makeDataComponent("SingleElectron_Run2017F_25Oct2019", "/SingleElectron/Run2017F-Nano25Oct2019-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2017F_25Oct2019 = kreator.makeDataComponent("SingleMuon_Run2017F_25Oct2019", "/SingleMuon/Run2017F-Nano25Oct2019-v1/NANOAOD", "CMS", ".*root", json)
SinglePhoton_Run2017F_25Oct2019 = kreator.makeDataComponent("SinglePhoton_Run2017F_25Oct2019", "/SinglePhoton/Run2017F-Nano25Oct2019-v1/NANOAOD", "CMS", ".*root", json)
DoubleEG_Run2017F_25Oct2019 = kreator.makeDataComponent("DoubleEG_Run2017F_25Oct2019", "/DoubleEG/Run2017F-Nano25Oct2019-v1/NANOAOD", "CMS", ".*root", json)
MuonEG_Run2017F_25Oct2019 = kreator.makeDataComponent("MuonEG_Run2017F_25Oct2019", "/MuonEG/Run2017F-Nano25Oct2019-v1/NANOAOD", "CMS", ".*root", json)
DoubleMuon_Run2017F_25Oct2019 = kreator.makeDataComponent("DoubleMuon_Run2017F_25Oct2019", "/DoubleMuon/Run2017F-Nano25Oct2019-v1/NANOAOD", "CMS", ".*root", json)
Tau_Run2017F_25Oct2019 = kreator.makeDataComponent("Tau_Run2017F_25Oct2019", "/Tau/Run2017F-Nano25Oct2019-v1/NANOAOD", "CMS", ".*root", json)

dataSamples_Run2017F_25Oct2019 = [JetHT_Run2017F_25Oct2019, HTMHT_Run2017F_25Oct2019, MET_Run2017F_25Oct2019, SingleElectron_Run2017F_25Oct2019, SingleMuon_Run2017F_25Oct2019, SinglePhoton_Run2017F_25Oct2019, DoubleEG_Run2017F_25Oct2019, MuonEG_Run2017F_25Oct2019, DoubleMuon_Run2017F_25Oct2019, Tau_Run2017F_25Oct2019]

dataSamples_25Oct2019 = dataSamples_Run2017B_25Oct2019 + dataSamples_Run2017C_25Oct2019 + dataSamples_Run2017D_25Oct2019 + dataSamples_Run2017E_25Oct2019 + dataSamples_Run2017F_25Oct2019

dataSamples = dataSamples_14Dec2018 + dataSamples_1June2019 + dataSamples_25Oct2019
samples = dataSamples

# ---------------------------------------------------------------------

if __name__ == "__main__":
    from CMGTools.RootTools.samples.tools import runMain
    runMain(samples, localobjs=locals())
