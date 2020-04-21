# COMPONENT CREATOR
from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()

# ----------------------------- 2018 pp run  ----------------------------------------

json = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/13TeV/ReReco/Cert_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18_JSON.txt'

# ----------------------------- Run2018A 17Sep2018 ----------------------------------------
JetHT_Run2018A_14Dec2018 = kreator.makeDataComponent("JetHT_Run2018A_14Dec2018", "/JetHT/Run2018A-Nano14Dec2018-v1/NANOAOD", "CMS", ".*root", json)
MET_Run2018A_14Dec2018 = kreator.makeDataComponent("MET_Run2018A_14Dec2018", "/MET/Run2018A-Nano14Dec2018-v1/NANOAOD", "CMS", ".*root", json)
EGamma_Run2018A_14Dec2018 = kreator.makeDataComponent("EGamma_Run2018A_14Dec2018", "/EGamma/Run2018A-Nano14Dec2018-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2018A_14Dec2018 = kreator.makeDataComponent("SingleMuon_Run2018A_14Dec2018", "/SingleMuon/Run2018A-Nano14Dec2018-v1/NANOAOD", "CMS", ".*root", json)
DoubleMuon_Run2018A_14Dec2018 = kreator.makeDataComponent("DoubleMuon_Run2018A_14Dec2018", "/DoubleMuon/Run2018A-Nano14Dec2018-v1/NANOAOD", "CMS", ".*root", json)
MuonEG_Run2018A_14Dec2018 = kreator.makeDataComponent("MuonEG_Run2018A_14Dec2018", "/MuonEG/Run2018A-Nano14Dec2018-v1/NANOAOD", "CMS", ".*root", json)
Tau_Run2018A_14Dec2018 = kreator.makeDataComponent("Tau_Run2018A_14Dec2018", "/Tau/Run2018A-Nano14Dec2018-v1/NANOAOD", "CMS", ".*root", json)

dataSamples_Run2018A_14Dec2018 = [JetHT_Run2018A_14Dec2018, MET_Run2018A_14Dec2018, EGamma_Run2018A_14Dec2018, SingleMuon_Run2018A_14Dec2018, DoubleMuon_Run2018A_14Dec2018, MuonEG_Run2018A_14Dec2018, Tau_Run2018A_14Dec2018]

# ----------------------------- Run2018B 17Sep2018 ----------------------------------------
JetHT_Run2018B_14Dec2018 = kreator.makeDataComponent("JetHT_Run2018B_14Dec2018", "/JetHT/Run2018B-Nano14Dec2018-v1/NANOAOD", "CMS", ".*root", json)
MET_Run2018B_14Dec2018 = kreator.makeDataComponent("MET_Run2018B_14Dec2018", "/MET/Run2018B-Nano14Dec2018-v1/NANOAOD", "CMS", ".*root", json)
EGamma_Run2018B_14Dec2018 = kreator.makeDataComponent("EGamma_Run2018B_14Dec2018", "/EGamma/Run2018B-Nano14Dec2018-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2018B_14Dec2018 = kreator.makeDataComponent("SingleMuon_Run2018B_14Dec2018", "/SingleMuon/Run2018B-Nano14Dec2018-v1/NANOAOD", "CMS", ".*root", json)
DoubleMuon_Run2018B_14Dec2018 = kreator.makeDataComponent("DoubleMuon_Run2018B_14Dec2018", "/DoubleMuon/Run2018B-Nano14Dec2018-v1/NANOAOD", "CMS", ".*root", json)
MuonEG_Run2018B_14Dec2018 = kreator.makeDataComponent("MuonEG_Run2018B_14Dec2018", "/MuonEG/Run2018B-Nano14Dec2018-v1/NANOAOD", "CMS", ".*root", json)
Tau_Run2018B_14Dec2018 = kreator.makeDataComponent("Tau_Run2018B_14Dec2018", "/Tau/Run2018B-Nano14Dec2018-v1/NANOAOD", "CMS", ".*root", json)

dataSamples_Run2018B_14Dec2018 = [JetHT_Run2018B_14Dec2018, MET_Run2018B_14Dec2018, EGamma_Run2018B_14Dec2018, SingleMuon_Run2018B_14Dec2018, DoubleMuon_Run2018B_14Dec2018, MuonEG_Run2018B_14Dec2018, Tau_Run2018B_14Dec2018]

# ----------------------------- Run2018C 17Sep2018 ----------------------------------------
JetHT_Run2018C_14Dec2018 = kreator.makeDataComponent("JetHT_Run2018C_14Dec2018", "/JetHT/Run2018C-Nano14Dec2018-v1/NANOAOD", "CMS", ".*root", json)
MET_Run2018C_14Dec2018 = kreator.makeDataComponent("MET_Run2018C_14Dec2018", "/MET/Run2018C-Nano14Dec2018-v1/NANOAOD", "CMS", ".*root", json)
EGamma_Run2018C_14Dec2018 = kreator.makeDataComponent("EGamma_Run2018C_14Dec2018", "/EGamma/Run2018C-Nano14Dec2018-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2018C_14Dec2018 = kreator.makeDataComponent("SingleMuon_Run2018C_14Dec2018", "/SingleMuon/Run2018C-Nano14Dec2018-v1/NANOAOD", "CMS", ".*root", json)
DoubleMuon_Run2018C_14Dec2018 = kreator.makeDataComponent("DoubleMuon_Run2018C_14Dec2018", "/DoubleMuon/Run2018C-Nano14Dec2018-v1/NANOAOD", "CMS", ".*root", json)
MuonEG_Run2018C_14Dec2018 = kreator.makeDataComponent("MuonEG_Run2018C_14Dec2018", "/MuonEG/Run2018C-Nano14Dec2018-v1/NANOAOD", "CMS", ".*root", json)
Tau_Run2018C_14Dec2018 = kreator.makeDataComponent("Tau_Run2018C_14Dec2018", "/Tau/Run2018C-Nano14Dec2018-v1/NANOAOD", "CMS", ".*root", json)

dataSamples_Run2018C_14Dec2018 = [JetHT_Run2018C_14Dec2018, MET_Run2018C_14Dec2018, EGamma_Run2018C_14Dec2018, SingleMuon_Run2018C_14Dec2018, DoubleMuon_Run2018C_14Dec2018, MuonEG_Run2018C_14Dec2018, Tau_Run2018C_14Dec2018]

# ----------------------------- Run2018D PromptReco  ----------------------------------------
JetHT_Run2018D_14Dec2018 = kreator.makeDataComponent("JetHT_Run2018D_14Dec2018", "/JetHT/Run2018D-Nano14Dec2018_ver2-v1/NANOAOD", "CMS", ".*root", json)
MET_Run2018D_14Dec2018 = kreator.makeDataComponent("MET_Run2018D_14Dec2018", "/MET/Run2018D-Nano14Dec2018_ver2-v1/NANOAOD", "CMS", ".*root", json)
EGamma_Run2018D_14Dec2018 = kreator.makeDataComponent("EGamma_Run2018D_14Dec2018", "/EGamma/Run2018D-22Jan2019_Nano14Dec2018-v1/NANOAOD", "CMS", ".*root", json) # 22Jan2019 to recover lumi lost in /EGamma/Run2018D-Nano14Dec2018_ver2-v1/NANOAOD
SingleMuon_Run2018D_14Dec2018 = kreator.makeDataComponent("SingleMuon_Run2018D_14Dec2018", "/SingleMuon/Run2018D-22Jan2019_Nano14Dec2018-v1/NANOAOD", "CMS", ".*root", json) # 22Jan2019 to recover lumi lost in /SingleMuon/Run2018D-Nano14Dec2018_ver2-v1/NANOAOD
DoubleMuon_Run2018D_14Dec2018 = kreator.makeDataComponent("DoubleMuon_Run2018D_14Dec2018", "/DoubleMuon/Run2018D-Nano14Dec2018_ver2-v1/NANOAOD", "CMS", ".*root", json)
MuonEG_Run2018D_14Dec2018 = kreator.makeDataComponent("MuonEG_Run2018D_14Dec2018", "/MuonEG/Run2018D-Nano14Dec2018_ver2-v1/NANOAOD", "CMS", ".*root", json)
Tau_Run2018D_14Dec2018 = kreator.makeDataComponent("Tau_Run2018D_14Dec2018", "/Tau/Run2018D-Nano14Dec2018_ver2-v1/NANOAOD", "CMS", ".*root", json)

dataSamples_Run2018D_14Dec2018 = [JetHT_Run2018D_14Dec2018, MET_Run2018D_14Dec2018, EGamma_Run2018D_14Dec2018, SingleMuon_Run2018D_14Dec2018, DoubleMuon_Run2018D_14Dec2018, MuonEG_Run2018D_14Dec2018, Tau_Run2018D_14Dec2018]

dataSamples_14Dec2018 = dataSamples_Run2018A_14Dec2018 + dataSamples_Run2018B_14Dec2018 + dataSamples_Run2018C_14Dec2018 + dataSamples_Run2018D_14Dec2018

# ----------------------------- Run2018A 1June2019 ----------------------------------------
JetHT_Run2018A_1June2019 = kreator.makeDataComponent("JetHT_Run2018A_1June2019", "/JetHT/Run2018A-Nano1June2019-v2/NANOAOD", "CMS", ".*root", json)
MET_Run2018A_1June2019 = kreator.makeDataComponent("MET_Run2018A_1June2019", "/MET/Run2018A-Nano1June2019-v1/NANOAOD", "CMS", ".*root", json)
EGamma_Run2018A_1June2019 = kreator.makeDataComponent("EGamma_Run2018A_1June2019", "/EGamma/Run2018A-Nano1June2019-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2018A_1June2019 = kreator.makeDataComponent("SingleMuon_Run2018A_1June2019", "/SingleMuon/Run2018A-Nano1June2019-v1/NANOAOD", "CMS", ".*root", json)
DoubleMuon_Run2018A_1June2019 = kreator.makeDataComponent("DoubleMuon_Run2018A_1June2019", "/DoubleMuon/Run2018A-Nano1June2019-v1/NANOAOD", "CMS", ".*root", json)
MuonEG_Run2018A_1June2019 = kreator.makeDataComponent("MuonEG_Run2018A_1June2019", "/MuonEG/Run2018A-Nano1June2019-v1/NANOAOD", "CMS", ".*root", json)
Tau_Run2018A_1June2019 = kreator.makeDataComponent("Tau_Run2018A_1June2019", "/Tau/Run2018A-Nano1June2019-v1/NANOAOD", "CMS", ".*root", json)

dataSamples_Run2018A_1June2019 = [JetHT_Run2018A_1June2019, MET_Run2018A_1June2019, EGamma_Run2018A_1June2019, SingleMuon_Run2018A_1June2019, DoubleMuon_Run2018A_1June2019, MuonEG_Run2018A_1June2019, Tau_Run2018A_1June2019]

# ----------------------------- Run2018B 1June2019 ----------------------------------------
JetHT_Run2018B_1June2019 = kreator.makeDataComponent("JetHT_Run2018B_1June2019", "/JetHT/Run2018B-Nano1June2019-v2/NANOAOD", "CMS", ".*root", json)
MET_Run2018B_1June2019 = kreator.makeDataComponent("MET_Run2018B_1June2019", "/MET/Run2018B-Nano1June2019-v1/NANOAOD", "CMS", ".*root", json)
EGamma_Run2018B_1June2019 = kreator.makeDataComponent("EGamma_Run2018B_1June2019", "/EGamma/Run2018B-Nano1June2019-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2018B_1June2019 = kreator.makeDataComponent("SingleMuon_Run2018B_1June2019", "/SingleMuon/Run2018B-Nano1June2019-v1/NANOAOD", "CMS", ".*root", json)
DoubleMuon_Run2018B_1June2019 = kreator.makeDataComponent("DoubleMuon_Run2018B_1June2019", "/DoubleMuon/Run2018B-Nano1June2019-v1/NANOAOD", "CMS", ".*root", json)
MuonEG_Run2018B_1June2019 = kreator.makeDataComponent("MuonEG_Run2018B_1June2019", "/MuonEG/Run2018B-Nano1June2019-v1/NANOAOD", "CMS", ".*root", json)
Tau_Run2018B_1June2019 = kreator.makeDataComponent("Tau_Run2018B_1June2019", "/Tau/Run2018B-Nano1June2019-v1/NANOAOD", "CMS", ".*root", json)

dataSamples_Run2018B_1June2019 = [JetHT_Run2018B_1June2019, MET_Run2018B_1June2019, EGamma_Run2018B_1June2019, SingleMuon_Run2018B_1June2019, DoubleMuon_Run2018B_1June2019, MuonEG_Run2018B_1June2019, Tau_Run2018B_1June2019]

# ----------------------------- Run2018C 1June2019  ----------------------------------------
JetHT_Run2018C_1June2019 = kreator.makeDataComponent("JetHT_Run2018C_1June2019", "/JetHT/Run2018C-Nano1June2019-v1/NANOAOD", "CMS", ".*root", json)
MET_Run2018C_1June2019 = kreator.makeDataComponent("MET_Run2018C_1June2019", "/MET/Run2018C-Nano1June2019-v1/NANOAOD", "CMS", ".*root", json)
EGamma_Run2018C_1June2019 = kreator.makeDataComponent("EGamma_Run2018C_1June2019", "/EGamma/Run2018C-Nano1June2019-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2018C_1June2019 = kreator.makeDataComponent("SingleMuon_Run2018C_1June2019", "/SingleMuon/Run2018C-Nano1June2019-v1/NANOAOD", "CMS", ".*root", json)
DoubleMuon_Run2018C_1June2019 = kreator.makeDataComponent("DoubleMuon_Run2018C_1June2019", "/DoubleMuon/Run2018C-Nano1June2019-v1/NANOAOD", "CMS", ".*root", json)
MuonEG_Run2018C_1June2019 = kreator.makeDataComponent("MuonEG_Run2018C_1June2019", "/MuonEG/Run2018C-Nano1June2019-v1/NANOAOD", "CMS", ".*root", json)
Tau_Run2018C_1June2019 = kreator.makeDataComponent("Tau_Run2018C_1June2019", "/Tau/Run2018C-Nano1June2019-v1/NANOAOD", "CMS", ".*root", json)

dataSamples_Run2018C_1June2019 = [JetHT_Run2018C_1June2019, MET_Run2018C_1June2019, EGamma_Run2018C_1June2019, SingleMuon_Run2018C_1June2019, DoubleMuon_Run2018C_1June2019, MuonEG_Run2018C_1June2019, Tau_Run2018C_1June2019]

# ----------------------------- Run2018D PromptReco  ----------------------------------------
JetHT_Run2018D_1June2019 = kreator.makeDataComponent("JetHT_Run2018D_1June2019", "/JetHT/Run2018D-Nano1June2019_ver2-v1/NANOAOD", "CMS", ".*root", json)
MET_Run2018D_1June2019 = kreator.makeDataComponent("MET_Run2018D_1June2019", "/MET/Run2018D-Nano1June2019_ver2-v1/NANOAOD", "CMS", ".*root", json)
EGamma_Run2018D_1June2019 = kreator.makeDataComponent("EGamma_Run2018D_1June2019", "/EGamma/Run2018D-Nano1June2019-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2018D_1June2019 = kreator.makeDataComponent("SingleMuon_Run2018D_1June2019", "/SingleMuon/Run2018D-Nano1June2019-v1/NANOAOD", "CMS", ".*root", json)
DoubleMuon_Run2018D_1June2019 = kreator.makeDataComponent("DoubleMuon_Run2018D_1June2019", "/DoubleMuon/Run2018D-Nano1June2019_ver2-v1/NANOAOD", "CMS", ".*root", json)
MuonEG_Run2018D_1June2019 = kreator.makeDataComponent("MuonEG_Run2018D_1June2019", "/MuonEG/Run2018D-Nano1June2019_ver2-v1/NANOAOD", "CMS", ".*root", json)
Tau_Run2018D_1June2019 = kreator.makeDataComponent("Tau_Run2018D_1June2019", "/Tau/Run2018D-Nano1June2019_ver2-v1/NANOAOD", "CMS", ".*root", json)

dataSamples_Run2018D_1June2019 = [JetHT_Run2018D_1June2019, MET_Run2018D_1June2019, EGamma_Run2018D_1June2019, SingleMuon_Run2018D_1June2019, DoubleMuon_Run2018D_1June2019, MuonEG_Run2018D_1June2019, Tau_Run2018D_1June2019]

dataSamples_1June2019 = dataSamples_Run2018A_1June2019 + dataSamples_Run2018B_1June2019 + dataSamples_Run2018C_1June2019 + dataSamples_Run2018D_1June2019

# ----------------------------- Run2018A 25Oct2019 ----------------------------------------
JetHT_Run2018A_25Oct2019 = kreator.makeDataComponent("JetHT_Run2018A_25Oct2019", "/JetHT/Run2018A-Nano25Oct2019-v1/NANOAOD", "CMS", ".*root", json)
MET_Run2018A_25Oct2019 = kreator.makeDataComponent("MET_Run2018A_25Oct2019", "/MET/Run2018A-Nano25Oct2019-v1/NANOAOD", "CMS", ".*root", json)
EGamma_Run2018A_25Oct2019 = kreator.makeDataComponent("EGamma_Run2018A_25Oct2019", "/EGamma/Run2018A-Nano25Oct2019-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2018A_25Oct2019 = kreator.makeDataComponent("SingleMuon_Run2018A_25Oct2019", "/SingleMuon/Run2018A-Nano25Oct2019-v1/NANOAOD", "CMS", ".*root", json)
DoubleMuon_Run2018A_25Oct2019 = kreator.makeDataComponent("DoubleMuon_Run2018A_25Oct2019", "/DoubleMuon/Run2018A-Nano25Oct2019-v1/NANOAOD", "CMS", ".*root", json)
MuonEG_Run2018A_25Oct2019 = kreator.makeDataComponent("MuonEG_Run2018A_25Oct2019", "/MuonEG/Run2018A-Nano25Oct2019-v1/NANOAOD", "CMS", ".*root", json)
Tau_Run2018A_25Oct2019 = kreator.makeDataComponent("Tau_Run2018A_25Oct2019", "/Tau/Run2018A-Nano25Oct2019-v1/NANOAOD", "CMS", ".*root", json)

dataSamples_Run2018A_25Oct2019 = [JetHT_Run2018A_25Oct2019, MET_Run2018A_25Oct2019, EGamma_Run2018A_25Oct2019, SingleMuon_Run2018A_25Oct2019, DoubleMuon_Run2018A_25Oct2019, MuonEG_Run2018A_25Oct2019, Tau_Run2018A_25Oct2019]

# ----------------------------- Run2018B 25Oct2019 ----------------------------------------
JetHT_Run2018B_25Oct2019 = kreator.makeDataComponent("JetHT_Run2018B_25Oct2019", "/JetHT/Run2018B-Nano25Oct2019-v1/NANOAOD", "CMS", ".*root", json)
MET_Run2018B_25Oct2019 = kreator.makeDataComponent("MET_Run2018B_25Oct2019", "/MET/Run2018B-Nano25Oct2019-v1/NANOAOD", "CMS", ".*root", json)
EGamma_Run2018B_25Oct2019 = kreator.makeDataComponent("EGamma_Run2018B_25Oct2019", "/EGamma/Run2018B-Nano25Oct2019-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2018B_25Oct2019 = kreator.makeDataComponent("SingleMuon_Run2018B_25Oct2019", "/SingleMuon/Run2018B-Nano25Oct2019-v1/NANOAOD", "CMS", ".*root", json)
DoubleMuon_Run2018B_25Oct2019 = kreator.makeDataComponent("DoubleMuon_Run2018B_25Oct2019", "/DoubleMuon/Run2018B-Nano25Oct2019-v1/NANOAOD", "CMS", ".*root", json)
MuonEG_Run2018B_25Oct2019 = kreator.makeDataComponent("MuonEG_Run2018B_25Oct2019", "/MuonEG/Run2018B-Nano25Oct2019-v1/NANOAOD", "CMS", ".*root", json)
Tau_Run2018B_25Oct2019 = kreator.makeDataComponent("Tau_Run2018B_25Oct2019", "/Tau/Run2018B-Nano25Oct2019-v1/NANOAOD", "CMS", ".*root", json)

dataSamples_Run2018B_25Oct2019 = [JetHT_Run2018B_25Oct2019, MET_Run2018B_25Oct2019, EGamma_Run2018B_25Oct2019, SingleMuon_Run2018B_25Oct2019, DoubleMuon_Run2018B_25Oct2019, MuonEG_Run2018B_25Oct2019, Tau_Run2018B_25Oct2019]

# ----------------------------- Run2018C 25Oct2019  ----------------------------------------
JetHT_Run2018C_25Oct2019 = kreator.makeDataComponent("JetHT_Run2018C_25Oct2019", "/JetHT/Run2018C-Nano25Oct2019-v2/NANOAOD", "CMS", ".*root", json)
MET_Run2018C_25Oct2019 = kreator.makeDataComponent("MET_Run2018C_25Oct2019", "/MET/Run2018C-Nano25Oct2019-v1/NANOAOD", "CMS", ".*root", json)
EGamma_Run2018C_25Oct2019 = kreator.makeDataComponent("EGamma_Run2018C_25Oct2019", "/EGamma/Run2018C-Nano25Oct2019-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2018C_25Oct2019 = kreator.makeDataComponent("SingleMuon_Run2018C_25Oct2019", "/SingleMuon/Run2018C-Nano25Oct2019-v1/NANOAOD", "CMS", ".*root", json)
DoubleMuon_Run2018C_25Oct2019 = kreator.makeDataComponent("DoubleMuon_Run2018C_25Oct2019", "/DoubleMuon/Run2018C-Nano25Oct2019-v1/NANOAOD", "CMS", ".*root", json)
MuonEG_Run2018C_25Oct2019 = kreator.makeDataComponent("MuonEG_Run2018C_25Oct2019", "/MuonEG/Run2018C-Nano25Oct2019-v1/NANOAOD", "CMS", ".*root", json)
Tau_Run2018C_25Oct2019 = kreator.makeDataComponent("Tau_Run2018C_25Oct2019", "/Tau/Run2018C-Nano25Oct2019-v1/NANOAOD", "CMS", ".*root", json)

dataSamples_Run2018C_25Oct2019 = [JetHT_Run2018C_25Oct2019, MET_Run2018C_25Oct2019, EGamma_Run2018C_25Oct2019, SingleMuon_Run2018C_25Oct2019, DoubleMuon_Run2018C_25Oct2019, MuonEG_Run2018C_25Oct2019, Tau_Run2018C_25Oct2019]

# ----------------------------- Run2018D PromptReco  ----------------------------------------
JetHT_Run2018D_25Oct2019 = kreator.makeDataComponent("JetHT_Run2018D_25Oct2019", "/JetHT/Run2018D-Nano25Oct2019_ver2-v1/NANOAOD", "CMS", ".*root", json)
MET_Run2018D_25Oct2019 = kreator.makeDataComponent("MET_Run2018D_25Oct2019", "/MET/Run2018D-Nano25Oct2019_ver2-v1/NANOAOD", "CMS", ".*root", json)
EGamma_Run2018D_25Oct2019 = kreator.makeDataComponent("EGamma_Run2018D_25Oct2019", "/EGamma/Run2018D-Nano25Oct2019-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2018D_25Oct2019 = kreator.makeDataComponent("SingleMuon_Run2018D_25Oct2019", "/SingleMuon/Run2018D-Nano25Oct2019-v1/NANOAOD", "CMS", ".*root", json)
DoubleMuon_Run2018D_25Oct2019 = kreator.makeDataComponent("DoubleMuon_Run2018D_25Oct2019", "/DoubleMuon/Run2018D-Nano25Oct2019_ver2-v1/NANOAOD", "CMS", ".*root", json)
MuonEG_Run2018D_25Oct2019 = kreator.makeDataComponent("MuonEG_Run2018D_25Oct2019", "/MuonEG/Run2018D-Nano25Oct2019_ver2-v1/NANOAOD", "CMS", ".*root", json)
Tau_Run2018D_25Oct2019 = kreator.makeDataComponent("Tau_Run2018D_25Oct2019", "/Tau/Run2018D-Nano25Oct2019_ver2-v1/NANOAOD", "CMS", ".*root", json)

dataSamples_Run2018D_25Oct2019 = [JetHT_Run2018D_25Oct2019, MET_Run2018D_25Oct2019, EGamma_Run2018D_25Oct2019, SingleMuon_Run2018D_25Oct2019, DoubleMuon_Run2018D_25Oct2019, MuonEG_Run2018D_25Oct2019, Tau_Run2018D_25Oct2019]

dataSamples_25Oct2019 = dataSamples_Run2018A_25Oct2019 + dataSamples_Run2018B_25Oct2019 + dataSamples_Run2018C_25Oct2019 + dataSamples_Run2018D_25Oct2019

dataSamples = dataSamples_14Dec2018 + dataSamples_1June2019 + dataSamples_25Oct2019

samples = dataSamples

# ---------------------------------------------------------------------

if __name__ == "__main__":
    from CMGTools.RootTools.samples.tools import runMain
    runMain(samples, localobjs=locals())
