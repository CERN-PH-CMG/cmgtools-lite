# COMPONENT CREATOR
from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()

# ----------------------------- 2017 pp run  ----------------------------------------

json = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/ReReco/Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON_v1.txt'

run_range = (294927, 306462)
label = "_runs%s_%s" % (run_range[0], run_range[1])

# ----------------------------- Run2017B 17Nov2017 ----------------------------------------

JetHT_Run2017B_17Nov2017 = kreator.makeDataComponent("JetHT_Run2017B_17Nov2017", "/JetHT/Run2017B-17Nov2017-v1/MINIAOD", "CMS", ".*root", json)
HTMHT_Run2017B_17Nov2017 = kreator.makeDataComponent("HTMHT_Run2017B_17Nov2017", "/HTMHT/Run2017B-17Nov2017-v1/MINIAOD", "CMS", ".*root", json)
MET_Run2017B_17Nov2017 = kreator.makeDataComponent("MET_Run2017B_17Nov2017", "/MET/Run2017B-17Nov2017-v1/MINIAOD", "CMS", ".*root", json)
SingleElectron_Run2017B_17Nov2017 = kreator.makeDataComponent("SingleElectron_Run2017B_17Nov2017", "/SingleElectron/Run2017B-17Nov2017-v1/MINIAOD", "CMS", ".*root", json)
SingleMuon_Run2017B_17Nov2017 = kreator.makeDataComponent("SingleMuon_Run2017B_17Nov2017", "/SingleMuon/Run2017B-17Nov2017-v1/MINIAOD", "CMS", ".*root", json)
SinglePhoton_Run2017B_17Nov2017 = kreator.makeDataComponent("SinglePhoton_Run2017B_17Nov2017", "/SinglePhoton/Run2017B-17Nov2017-v1/MINIAOD", "CMS", ".*root", json)
DoubleEG_Run2017B_17Nov2017 = kreator.makeDataComponent("DoubleEG_Run2017B_17Nov2017", "/DoubleEG/Run2017B-17Nov2017-v1/MINIAOD", "CMS", ".*root", json)
MuonEG_Run2017B_17Nov2017 = kreator.makeDataComponent("MuonEG_Run2017B_17Nov2017", "/MuonEG/Run2017B-17Nov2017-v1/MINIAOD", "CMS", ".*root", json)
DoubleMuon_Run2017B_17Nov2017 = kreator.makeDataComponent("DoubleMuon_Run2017B_17Nov2017", "/DoubleMuon/Run2017B-17Nov2017-v1/MINIAOD", "CMS", ".*root", json)
Tau_Run2017B_17Nov2017 = kreator.makeDataComponent("Tau_Run2017B_17Nov2017", "/Tau/Run2017B-17Nov2017-v1/MINIAOD", "CMS", ".*root", json)

dataSamples_Run2017B_17Nov2017 = [JetHT_Run2017B_17Nov2017, HTMHT_Run2017B_17Nov2017, MET_Run2017B_17Nov2017, SingleElectron_Run2017B_17Nov2017, SingleMuon_Run2017B_17Nov2017, SinglePhoton_Run2017B_17Nov2017, DoubleEG_Run2017B_17Nov2017, MuonEG_Run2017B_17Nov2017, DoubleMuon_Run2017B_17Nov2017, Tau_Run2017B_17Nov2017]

# ----------------------------- Run2017C 17Nov2017 ----------------------------------------

JetHT_Run2017C_17Nov2017 = kreator.makeDataComponent("JetHT_Run2017C_17Nov2017", "/JetHT/Run2017C-17Nov2017-v1/MINIAOD", "CMS", ".*root", json)
HTMHT_Run2017C_17Nov2017 = kreator.makeDataComponent("HTMHT_Run2017C_17Nov2017", "/HTMHT/Run2017C-17Nov2017-v1/MINIAOD", "CMS", ".*root", json)
MET_Run2017C_17Nov2017 = kreator.makeDataComponent("MET_Run2017C_17Nov2017", "/MET/Run2017C-17Nov2017-v1/MINIAOD", "CMS", ".*root", json)
SingleElectron_Run2017C_17Nov2017 = kreator.makeDataComponent("SingleElectron_Run2017C_17Nov2017", "/SingleElectron/Run2017C-17Nov2017-v1/MINIAOD", "CMS", ".*root", json)
SingleMuon_Run2017C_17Nov2017 = kreator.makeDataComponent("SingleMuon_Run2017C_17Nov2017", "/SingleMuon/Run2017C-17Nov2017-v1/MINIAOD", "CMS", ".*root", json)
SinglePhoton_Run2017C_17Nov2017 = kreator.makeDataComponent("SinglePhoton_Run2017C_17Nov2017", "/SinglePhoton/Run2017C-17Nov2017-v1/MINIAOD", "CMS", ".*root", json)
DoubleEG_Run2017C_17Nov2017 = kreator.makeDataComponent("DoubleEG_Run2017C_17Nov2017", "/DoubleEG/Run2017C-17Nov2017-v1/MINIAOD", "CMS", ".*root", json)
MuonEG_Run2017C_17Nov2017 = kreator.makeDataComponent("MuonEG_Run2017C_17Nov2017", "/MuonEG/Run2017C-17Nov2017-v1/MINIAOD", "CMS", ".*root", json)
DoubleMuon_Run2017C_17Nov2017 = kreator.makeDataComponent("DoubleMuon_Run2017C_17Nov2017", "/DoubleMuon/Run2017C-17Nov2017-v1/MINIAOD", "CMS", ".*root", json)
Tau_Run2017C_17Nov2017 = kreator.makeDataComponent("Tau_Run2017C_17Nov2017", "/Tau/Run2017C-17Nov2017-v1/MINIAOD", "CMS", ".*root", json)

dataSamples_Run2017C_17Nov2017 = [JetHT_Run2017C_17Nov2017, HTMHT_Run2017C_17Nov2017, MET_Run2017C_17Nov2017, SingleElectron_Run2017C_17Nov2017, SingleMuon_Run2017C_17Nov2017, SinglePhoton_Run2017C_17Nov2017, DoubleEG_Run2017C_17Nov2017, MuonEG_Run2017C_17Nov2017, DoubleMuon_Run2017C_17Nov2017, Tau_Run2017C_17Nov2017]


# ----------------------------- Run2017D 17Nov2017 ----------------------------------------

JetHT_Run2017D_17Nov2017 = kreator.makeDataComponent("JetHT_Run2017D_17Nov2017", "/JetHT/Run2017D-17Nov2017-v1/MINIAOD", "CMS", ".*root", json)
HTMHT_Run2017D_17Nov2017 = kreator.makeDataComponent("HTMHT_Run2017D_17Nov2017", "/HTMHT/Run2017D-17Nov2017-v1/MINIAOD", "CMS", ".*root", json)
MET_Run2017D_17Nov2017 = kreator.makeDataComponent("MET_Run2017D_17Nov2017", "/MET/Run2017D-17Nov2017-v1/MINIAOD", "CMS", ".*root", json)
SingleElectron_Run2017D_17Nov2017 = kreator.makeDataComponent("SingleElectron_Run2017D_17Nov2017", "/SingleElectron/Run2017D-17Nov2017-v1/MINIAOD", "CMS", ".*root", json)
SingleMuon_Run2017D_17Nov2017 = kreator.makeDataComponent("SingleMuon_Run2017D_17Nov2017", "/SingleMuon/Run2017D-17Nov2017-v1/MINIAOD", "CMS", ".*root", json)
SinglePhoton_Run2017D_17Nov2017 = kreator.makeDataComponent("SinglePhoton_Run2017D_17Nov2017", "/SinglePhoton/Run2017D-17Nov2017-v1/MINIAOD", "CMS", ".*root", json)
DoubleEG_Run2017D_17Nov2017 = kreator.makeDataComponent("DoubleEG_Run2017D_17Nov2017", "/DoubleEG/Run2017D-17Nov2017-v1/MINIAOD", "CMS", ".*root", json)
MuonEG_Run2017D_17Nov2017 = kreator.makeDataComponent("MuonEG_Run2017D_17Nov2017", "/MuonEG/Run2017D-17Nov2017-v1/MINIAOD", "CMS", ".*root", json)
DoubleMuon_Run2017D_17Nov2017 = kreator.makeDataComponent("DoubleMuon_Run2017D_17Nov2017", "/DoubleMuon/Run2017D-17Nov2017-v1/MINIAOD", "CMS", ".*root", json)
Tau_Run2017D_17Nov2017 = kreator.makeDataComponent("Tau_Run2017D_17Nov2017", "/Tau/Run2017D-17Nov2017-v1/MINIAOD", "CMS", ".*root", json)

dataSamples_Run2017D_17Nov2017 = [JetHT_Run2017D_17Nov2017, HTMHT_Run2017D_17Nov2017, MET_Run2017D_17Nov2017, SingleElectron_Run2017D_17Nov2017, SingleMuon_Run2017D_17Nov2017, SinglePhoton_Run2017D_17Nov2017, DoubleEG_Run2017D_17Nov2017, MuonEG_Run2017D_17Nov2017, DoubleMuon_Run2017D_17Nov2017, Tau_Run2017D_17Nov2017]

# ----------------------------- Run2017E 17Nov2017 ----------------------------------------

JetHT_Run2017E_17Nov2017 = kreator.makeDataComponent("JetHT_Run2017E_17Nov2017", "/JetHT/Run2017E-17Nov2017-v1/MINIAOD", "CMS", ".*root", json)
HTMHT_Run2017E_17Nov2017 = kreator.makeDataComponent("HTMHT_Run2017E_17Nov2017", "/HTMHT/Run2017E-17Nov2017-v1/MINIAOD", "CMS", ".*root", json)
MET_Run2017E_17Nov2017 = kreator.makeDataComponent("MET_Run2017E_17Nov2017", "/MET/Run2017E-17Nov2017-v1/MINIAOD", "CMS", ".*root", json)
SingleElectron_Run2017E_17Nov2017 = kreator.makeDataComponent("SingleElectron_Run2017E_17Nov2017", "/SingleElectron/Run2017E-17Nov2017-v1/MINIAOD", "CMS", ".*root", json)
SingleMuon_Run2017E_17Nov2017 = kreator.makeDataComponent("SingleMuon_Run2017E_17Nov2017", "/SingleMuon/Run2017E-17Nov2017-v1/MINIAOD", "CMS", ".*root", json)
SinglePhoton_Run2017E_17Nov2017 = kreator.makeDataComponent("SinglePhoton_Run2017E_17Nov2017", "/SinglePhoton/Run2017E-17Nov2017-v1/MINIAOD", "CMS", ".*root", json)
DoubleEG_Run2017E_17Nov2017 = kreator.makeDataComponent("DoubleEG_Run2017E_17Nov2017", "/DoubleEG/Run2017E-17Nov2017-v1/MINIAOD", "CMS", ".*root", json)
MuonEG_Run2017E_17Nov2017 = kreator.makeDataComponent("MuonEG_Run2017E_17Nov2017", "/MuonEG/Run2017E-17Nov2017-v1/MINIAOD", "CMS", ".*root", json)
DoubleMuon_Run2017E_17Nov2017 = kreator.makeDataComponent("DoubleMuon_Run2017E_17Nov2017", "/DoubleMuon/Run2017E-17Nov2017-v1/MINIAOD", "CMS", ".*root", json)
Tau_Run2017E_17Nov2017 = kreator.makeDataComponent("Tau_Run2017E_17Nov2017", "/Tau/Run2017E-17Nov2017-v1/MINIAOD", "CMS", ".*root", json)

dataSamples_Run2017E_17Nov2017 = [JetHT_Run2017E_17Nov2017, HTMHT_Run2017E_17Nov2017, MET_Run2017E_17Nov2017, SingleElectron_Run2017E_17Nov2017, SingleMuon_Run2017E_17Nov2017, SinglePhoton_Run2017E_17Nov2017, DoubleEG_Run2017E_17Nov2017, MuonEG_Run2017E_17Nov2017, DoubleMuon_Run2017E_17Nov2017, Tau_Run2017E_17Nov2017]


# ----------------------------- Run2017F 17Nov2017 ----------------------------------------

JetHT_Run2017F_17Nov2017 = kreator.makeDataComponent("JetHT_Run2017F_17Nov2017", "/JetHT/Run2017F-17Nov2017-v1/MINIAOD", "CMS", ".*root", json)
HTMHT_Run2017F_17Nov2017 = kreator.makeDataComponent("HTMHT_Run2017F_17Nov2017", "/HTMHT/Run2017F-17Nov2017-v1/MINIAOD", "CMS", ".*root", json)
MET_Run2017F_17Nov2017 = kreator.makeDataComponent("MET_Run2017F_17Nov2017", "/MET/Run2017F-17Nov2017-v1/MINIAOD", "CMS", ".*root", json)
SingleElectron_Run2017F_17Nov2017 = kreator.makeDataComponent("SingleElectron_Run2017F_17Nov2017", "/SingleElectron/Run2017F-17Nov2017-v1/MINIAOD", "CMS", ".*root", json)
SingleMuon_Run2017F_17Nov2017 = kreator.makeDataComponent("SingleMuon_Run2017F_17Nov2017", "/SingleMuon/Run2017F-17Nov2017-v1/MINIAOD", "CMS", ".*root", json)
SinglePhoton_Run2017F_17Nov2017 = kreator.makeDataComponent("SinglePhoton_Run2017F_17Nov2017", "/SinglePhoton/Run2017F-17Nov2017-v1/MINIAOD", "CMS", ".*root", json)
DoubleEG_Run2017F_17Nov2017 = kreator.makeDataComponent("DoubleEG_Run2017F_17Nov2017", "/DoubleEG/Run2017F-17Nov2017-v1/MINIAOD", "CMS", ".*root", json)
MuonEG_Run2017F_17Nov2017 = kreator.makeDataComponent("MuonEG_Run2017F_17Nov2017", "/MuonEG/Run2017F-17Nov2017-v1/MINIAOD", "CMS", ".*root", json)
DoubleMuon_Run2017F_17Nov2017 = kreator.makeDataComponent("DoubleMuon_Run2017F_17Nov2017", "/DoubleMuon/Run2017F-17Nov2017-v1/MINIAOD", "CMS", ".*root", json)
Tau_Run2017F_17Nov2017 = kreator.makeDataComponent("Tau_Run2017F_17Nov2017", "/Tau/Run2017F-17Nov2017-v1/MINIAOD", "CMS", ".*root", json)

dataSamples_Run2017F_17Nov2017 = [JetHT_Run2017F_17Nov2017, HTMHT_Run2017F_17Nov2017, MET_Run2017F_17Nov2017, SingleElectron_Run2017F_17Nov2017, SingleMuon_Run2017F_17Nov2017, SinglePhoton_Run2017F_17Nov2017, DoubleEG_Run2017F_17Nov2017, MuonEG_Run2017F_17Nov2017, DoubleMuon_Run2017F_17Nov2017, Tau_Run2017F_17Nov2017]

# Summary of 17Nov2017
dataSamples_17Nov2017 = dataSamples_Run2017B_17Nov2017 + dataSamples_Run2017C_17Nov2017 + dataSamples_Run2017D_17Nov2017 + dataSamples_Run2017E_17Nov2017 + dataSamples_Run2017F_17Nov2017



# ----------------------------- Run2017B 31Mar2018 ----------------------------------------

JetHT_Run2017B_31Mar2018 = kreator.makeDataComponent("JetHT_Run2017B_31Mar2018", "/JetHT/Run2017B-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
HTMHT_Run2017B_31Mar2018 = kreator.makeDataComponent("HTMHT_Run2017B_31Mar2018", "/HTMHT/Run2017B-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
MET_Run2017B_31Mar2018 = kreator.makeDataComponent("MET_Run2017B_31Mar2018", "/MET/Run2017B-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
SingleElectron_Run2017B_31Mar2018 = kreator.makeDataComponent("SingleElectron_Run2017B_31Mar2018", "/SingleElectron/Run2017B-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
SingleMuon_Run2017B_31Mar2018 = kreator.makeDataComponent("SingleMuon_Run2017B_31Mar2018", "/SingleMuon/Run2017B-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
SinglePhoton_Run2017B_31Mar2018 = kreator.makeDataComponent("SinglePhoton_Run2017B_31Mar2018", "/SinglePhoton/Run2017B-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
DoubleEG_Run2017B_31Mar2018 = kreator.makeDataComponent("DoubleEG_Run2017B_31Mar2018", "/DoubleEG/Run2017B-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
MuonEG_Run2017B_31Mar2018 = kreator.makeDataComponent("MuonEG_Run2017B_31Mar2018", "/MuonEG/Run2017B-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
DoubleMuon_Run2017B_31Mar2018 = kreator.makeDataComponent("DoubleMuon_Run2017B_31Mar2018", "/DoubleMuon/Run2017B-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
Tau_Run2017B_31Mar2018 = kreator.makeDataComponent("Tau_Run2017B_31Mar2018", "/Tau/Run2017B-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)

dataSamples_Run2017B_31Mar2018 = [JetHT_Run2017B_31Mar2018, HTMHT_Run2017B_31Mar2018, MET_Run2017B_31Mar2018, SingleElectron_Run2017B_31Mar2018, SingleMuon_Run2017B_31Mar2018, SinglePhoton_Run2017B_31Mar2018, DoubleEG_Run2017B_31Mar2018, MuonEG_Run2017B_31Mar2018, DoubleMuon_Run2017B_31Mar2018, Tau_Run2017B_31Mar2018]

# ----------------------------- Run2017C 31Mar2018 ----------------------------------------

JetHT_Run2017C_31Mar2018 = kreator.makeDataComponent("JetHT_Run2017C_31Mar2018", "/JetHT/Run2017C-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
HTMHT_Run2017C_31Mar2018 = kreator.makeDataComponent("HTMHT_Run2017C_31Mar2018", "/HTMHT/Run2017C-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
MET_Run2017C_31Mar2018 = kreator.makeDataComponent("MET_Run2017C_31Mar2018", "/MET/Run2017C-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
SingleElectron_Run2017C_31Mar2018 = kreator.makeDataComponent("SingleElectron_Run2017C_31Mar2018", "/SingleElectron/Run2017C-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
SingleMuon_Run2017C_31Mar2018 = kreator.makeDataComponent("SingleMuon_Run2017C_31Mar2018", "/SingleMuon/Run2017C-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
SinglePhoton_Run2017C_31Mar2018 = kreator.makeDataComponent("SinglePhoton_Run2017C_31Mar2018", "/SinglePhoton/Run2017C-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
DoubleEG_Run2017C_31Mar2018 = kreator.makeDataComponent("DoubleEG_Run2017C_31Mar2018", "/DoubleEG/Run2017C-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
MuonEG_Run2017C_31Mar2018 = kreator.makeDataComponent("MuonEG_Run2017C_31Mar2018", "/MuonEG/Run2017C-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
DoubleMuon_Run2017C_31Mar2018 = kreator.makeDataComponent("DoubleMuon_Run2017C_31Mar2018", "/DoubleMuon/Run2017C-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
Tau_Run2017C_31Mar2018 = kreator.makeDataComponent("Tau_Run2017C_31Mar2018", "/Tau/Run2017C-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)

dataSamples_Run2017C_31Mar2018 = [JetHT_Run2017C_31Mar2018, HTMHT_Run2017C_31Mar2018, MET_Run2017C_31Mar2018, SingleElectron_Run2017C_31Mar2018, SingleMuon_Run2017C_31Mar2018, SinglePhoton_Run2017C_31Mar2018, DoubleEG_Run2017C_31Mar2018, MuonEG_Run2017C_31Mar2018, DoubleMuon_Run2017C_31Mar2018, Tau_Run2017C_31Mar2018]


# ----------------------------- Run2017D 31Mar2018 ----------------------------------------

JetHT_Run2017D_31Mar2018 = kreator.makeDataComponent("JetHT_Run2017D_31Mar2018", "/JetHT/Run2017D-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
HTMHT_Run2017D_31Mar2018 = kreator.makeDataComponent("HTMHT_Run2017D_31Mar2018", "/HTMHT/Run2017D-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
MET_Run2017D_31Mar2018 = kreator.makeDataComponent("MET_Run2017D_31Mar2018", "/MET/Run2017D-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
SingleElectron_Run2017D_31Mar2018 = kreator.makeDataComponent("SingleElectron_Run2017D_31Mar2018", "/SingleElectron/Run2017D-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
SingleMuon_Run2017D_31Mar2018 = kreator.makeDataComponent("SingleMuon_Run2017D_31Mar2018", "/SingleMuon/Run2017D-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
SinglePhoton_Run2017D_31Mar2018 = kreator.makeDataComponent("SinglePhoton_Run2017D_31Mar2018", "/SinglePhoton/Run2017D-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
DoubleEG_Run2017D_31Mar2018 = kreator.makeDataComponent("DoubleEG_Run2017D_31Mar2018", "/DoubleEG/Run2017D-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
MuonEG_Run2017D_31Mar2018 = kreator.makeDataComponent("MuonEG_Run2017D_31Mar2018", "/MuonEG/Run2017D-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
DoubleMuon_Run2017D_31Mar2018 = kreator.makeDataComponent("DoubleMuon_Run2017D_31Mar2018", "/DoubleMuon/Run2017D-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
Tau_Run2017D_31Mar2018 = kreator.makeDataComponent("Tau_Run2017D_31Mar2018", "/Tau/Run2017D-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)

dataSamples_Run2017D_31Mar2018 = [JetHT_Run2017D_31Mar2018, HTMHT_Run2017D_31Mar2018, MET_Run2017D_31Mar2018, SingleElectron_Run2017D_31Mar2018, SingleMuon_Run2017D_31Mar2018, SinglePhoton_Run2017D_31Mar2018, DoubleEG_Run2017D_31Mar2018, MuonEG_Run2017D_31Mar2018, DoubleMuon_Run2017D_31Mar2018, Tau_Run2017D_31Mar2018]

# ----------------------------- Run2017E 31Mar2018 ----------------------------------------

JetHT_Run2017E_31Mar2018 = kreator.makeDataComponent("JetHT_Run2017E_31Mar2018", "/JetHT/Run2017E-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
HTMHT_Run2017E_31Mar2018 = kreator.makeDataComponent("HTMHT_Run2017E_31Mar2018", "/HTMHT/Run2017E-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
MET_Run2017E_31Mar2018 = kreator.makeDataComponent("MET_Run2017E_31Mar2018", "/MET/Run2017E-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
SingleElectron_Run2017E_31Mar2018 = kreator.makeDataComponent("SingleElectron_Run2017E_31Mar2018", "/SingleElectron/Run2017E-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
SingleMuon_Run2017E_31Mar2018 = kreator.makeDataComponent("SingleMuon_Run2017E_31Mar2018", "/SingleMuon/Run2017E-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
SinglePhoton_Run2017E_31Mar2018 = kreator.makeDataComponent("SinglePhoton_Run2017E_31Mar2018", "/SinglePhoton/Run2017E-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
DoubleEG_Run2017E_31Mar2018 = kreator.makeDataComponent("DoubleEG_Run2017E_31Mar2018", "/DoubleEG/Run2017E-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
MuonEG_Run2017E_31Mar2018 = kreator.makeDataComponent("MuonEG_Run2017E_31Mar2018", "/MuonEG/Run2017E-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
DoubleMuon_Run2017E_31Mar2018 = kreator.makeDataComponent("DoubleMuon_Run2017E_31Mar2018", "/DoubleMuon/Run2017E-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
Tau_Run2017E_31Mar2018 = kreator.makeDataComponent("Tau_Run2017E_31Mar2018", "/Tau/Run2017E-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)

dataSamples_Run2017E_31Mar2018 = [JetHT_Run2017E_31Mar2018, HTMHT_Run2017E_31Mar2018, MET_Run2017E_31Mar2018, SingleElectron_Run2017E_31Mar2018, SingleMuon_Run2017E_31Mar2018, SinglePhoton_Run2017E_31Mar2018, DoubleEG_Run2017E_31Mar2018, MuonEG_Run2017E_31Mar2018, DoubleMuon_Run2017E_31Mar2018, Tau_Run2017E_31Mar2018]


# ----------------------------- Run2017F 31Mar2018 ----------------------------------------

JetHT_Run2017F_31Mar2018 = kreator.makeDataComponent("JetHT_Run2017F_31Mar2018", "/JetHT/Run2017F-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
HTMHT_Run2017F_31Mar2018 = kreator.makeDataComponent("HTMHT_Run2017F_31Mar2018", "/HTMHT/Run2017F-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
MET_Run2017F_31Mar2018 = kreator.makeDataComponent("MET_Run2017F_31Mar2018", "/MET/Run2017F-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
SingleElectron_Run2017F_31Mar2018 = kreator.makeDataComponent("SingleElectron_Run2017F_31Mar2018", "/SingleElectron/Run2017F-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
SingleMuon_Run2017F_31Mar2018 = kreator.makeDataComponent("SingleMuon_Run2017F_31Mar2018", "/SingleMuon/Run2017F-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
SinglePhoton_Run2017F_31Mar2018 = kreator.makeDataComponent("SinglePhoton_Run2017F_31Mar2018", "/SinglePhoton/Run2017F-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
DoubleEG_Run2017F_31Mar2018 = kreator.makeDataComponent("DoubleEG_Run2017F_31Mar2018", "/DoubleEG/Run2017F-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
MuonEG_Run2017F_31Mar2018 = kreator.makeDataComponent("MuonEG_Run2017F_31Mar2018", "/MuonEG/Run2017F-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
DoubleMuon_Run2017F_31Mar2018 = kreator.makeDataComponent("DoubleMuon_Run2017F_31Mar2018", "/DoubleMuon/Run2017F-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
Tau_Run2017F_31Mar2018 = kreator.makeDataComponent("Tau_Run2017F_31Mar2018", "/Tau/Run2017F-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)

dataSamples_Run2017F_31Mar2018 = [JetHT_Run2017F_31Mar2018, HTMHT_Run2017F_31Mar2018, MET_Run2017F_31Mar2018, SingleElectron_Run2017F_31Mar2018, SingleMuon_Run2017F_31Mar2018, SinglePhoton_Run2017F_31Mar2018, DoubleEG_Run2017F_31Mar2018, MuonEG_Run2017F_31Mar2018, DoubleMuon_Run2017F_31Mar2018, Tau_Run2017F_31Mar2018]

# Summary of 31Mar2018
dataSamples_31Mar2018 = dataSamples_Run2017B_31Mar2018 + dataSamples_Run2017C_31Mar2018 + dataSamples_Run2017D_31Mar2018 + dataSamples_Run2017E_31Mar2018 + dataSamples_Run2017F_31Mar2018


dataSamples = dataSamples_17Nov2017 + dataSamples_31Mar2018
samples = dataSamples

# ---------------------------------------------------------------------

if __name__ == "__main__":
    from CMGTools.RootTools.samples.tools import runMain
    runMain(samples)
