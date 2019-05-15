# COMPONENT CREATOR
from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()

# ----------------------------- 2017 pp run  ----------------------------------------

json = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/13TeV/ReReco/Cert_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18_JSON.txt'

# ----------------------------- Run2017A 17Sep2018 ----------------------------------------
JetHT_Run2018A_17Sep2018 = kreator.makeDataComponent("JetHT_Run2018A_17Sep2018", "/JetHT/Run2018A-17Sep2018-v1/MINIAOD", "CMS", ".*root", json)
MET_Run2018A_17Sep2018 = kreator.makeDataComponent("MET_Run2018A_17Sep2018", "/MET/Run2018A-17Sep2018-v1/MINIAOD", "CMS", ".*root", json)
EGamma_Run2018A_17Sep2018 = kreator.makeDataComponent("EGamma_Run2018A_17Sep2018", "/EGamma/Run2018A-17Sep2018-v2/MINIAOD", "CMS", ".*root", json)
SingleMuon_Run2018A_17Sep2018 = kreator.makeDataComponent("SingleMuon_Run2018A_17Sep2018", "/SingleMuon/Run2018A-17Sep2018-v2/MINIAOD", "CMS", ".*root", json)
DoubleMuon_Run2018A_17Sep2018 = kreator.makeDataComponent("DoubleMuon_Run2018A_17Sep2018", "/DoubleMuon/Run2018A-17Sep2018-v2/MINIAOD", "CMS", ".*root", json)
MuonEG_Run2018A_17Sep2018 = kreator.makeDataComponent("MuonEG_Run2018A_17Sep2018", "/MuonEG/Run2018A-17Sep2018-v1/MINIAOD", "CMS", ".*root", json)
Tau_Run2018A_17Sep2018 = kreator.makeDataComponent("Tau_Run2018A_17Sep2018", "/Tau/Run2018A-17Sep2018-v1/MINIAOD", "CMS", ".*root", json)

dataSamples_Run2018A_17Sep2018 = [JetHT_Run2018A_17Sep2018, MET_Run2018A_17Sep2018, EGamma_Run2018A_17Sep2018, SingleMuon_Run2018A_17Sep2018, DoubleMuon_Run2018A_17Sep2018, MuonEG_Run2018A_17Sep2018, Tau_Run2018A_17Sep2018]

# ----------------------------- Run2017B 17Sep2018 ----------------------------------------
JetHT_Run2018B_17Sep2018 = kreator.makeDataComponent("JetHT_Run2018B_17Sep2018", "/JetHT/Run2018B-17Sep2018-v1/MINIAOD", "CMS", ".*root", json)
MET_Run2018B_17Sep2018 = kreator.makeDataComponent("MET_Run2018B_17Sep2018", "/MET/Run2018B-17Sep2018-v1/MINIAOD", "CMS", ".*root", json)
EGamma_Run2018B_17Sep2018 = kreator.makeDataComponent("EGamma_Run2018B_17Sep2018", "/EGamma/Run2018B-17Sep2018-v1/MINIAOD", "CMS", ".*root", json)
SingleMuon_Run2018B_17Sep2018 = kreator.makeDataComponent("SingleMuon_Run2018B_17Sep2018", "/SingleMuon/Run2018B-17Sep2018-v1/MINIAOD", "CMS", ".*root", json)
DoubleMuon_Run2018B_17Sep2018 = kreator.makeDataComponent("DoubleMuon_Run2018B_17Sep2018", "/DoubleMuon/Run2018B-17Sep2018-v1/MINIAOD", "CMS", ".*root", json)
MuonEG_Run2018B_17Sep2018 = kreator.makeDataComponent("MuonEG_Run2018B_17Sep2018", "/MuonEG/Run2018B-17Sep2018-v1/MINIAOD", "CMS", ".*root", json)
Tau_Run2018B_17Sep2018 = kreator.makeDataComponent("Tau_Run2018B_17Sep2018", "/Tau/Run2018B-17Sep2018-v1/MINIAOD", "CMS", ".*root", json)

dataSamples_Run2018B_17Sep2018 = [JetHT_Run2018B_17Sep2018, MET_Run2018B_17Sep2018, EGamma_Run2018B_17Sep2018, SingleMuon_Run2018B_17Sep2018, DoubleMuon_Run2018B_17Sep2018, MuonEG_Run2018B_17Sep2018, Tau_Run2018B_17Sep2018]

# ----------------------------- Run2017C 17Sep2018 ----------------------------------------
JetHT_Run2018C_17Sep2018 = kreator.makeDataComponent("JetHT_Run2018C_17Sep2018", "/JetHT/Run2018C-17Sep2018-v1/MINIAOD", "CMS", ".*root", json)
MET_Run2018C_17Sep2018 = kreator.makeDataComponent("MET_Run2018C_17Sep2018", "/MET/Run2018C-17Sep2018-v1/MINIAOD", "CMS", ".*root", json)
EGamma_Run2018C_17Sep2018 = kreator.makeDataComponent("EGamma_Run2018C_17Sep2018", "/EGamma/Run2018C-17Sep2018-v1/MINIAOD", "CMS", ".*root", json)
SingleMuon_Run2018C_17Sep2018 = kreator.makeDataComponent("SingleMuon_Run2018C_17Sep2018", "/SingleMuon/Run2018C-17Sep2018-v1/MINIAOD", "CMS", ".*root", json)
DoubleMuon_Run2018C_17Sep2018 = kreator.makeDataComponent("DoubleMuon_Run2018C_17Sep2018", "/DoubleMuon/Run2018C-17Sep2018-v1/MINIAOD", "CMS", ".*root", json)
MuonEG_Run2018C_17Sep2018 = kreator.makeDataComponent("MuonEG_Run2018C_17Sep2018", "/MuonEG/Run2018C-17Sep2018-v1/MINIAOD", "CMS", ".*root", json)
Tau_Run2018C_17Sep2018 = kreator.makeDataComponent("Tau_Run2018C_17Sep2018", "/Tau/Run2018C-17Sep2018-v1/MINIAOD", "CMS", ".*root", json)

dataSamples_Run2018C_17Sep2018 = [JetHT_Run2018C_17Sep2018, MET_Run2018C_17Sep2018, EGamma_Run2018C_17Sep2018, SingleMuon_Run2018C_17Sep2018, DoubleMuon_Run2018C_17Sep2018, MuonEG_Run2018C_17Sep2018, Tau_Run2018C_17Sep2018]

# ----------------------------- Run2017D PromptReco  ----------------------------------------
JetHT_Run2018D_PromptReco_v2 = kreator.makeDataComponent("JetHT_Run2018D_PromptReco_v2", "/JetHT/Run2018D-PromptReco-v2/MINIAOD", "CMS", ".*root", json)
MET_Run2018D_PromptReco_v2 = kreator.makeDataComponent("MET_Run2018D_PromptReco_v2", "/MET/Run2018D-PromptReco-v2/MINIAOD", "CMS", ".*root", json)
EGamma_Run2018D_PromptReco_v2 = kreator.makeDataComponent("EGamma_Run2018D_PromptReco_v2", "/EGamma/Run2018D-22Jan2019-v2/MINIAOD", "CMS", ".*root", json) # 22Jan2019 to recover lumi lost in /EGamma/Run2018D-22Jan2019-v2/MINIAOD
SingleMuon_Run2018D_PromptReco_v2 = kreator.makeDataComponent("SingleMuon_Run2018D_PromptReco_v2", "/SingleMuon/Run2018D-22Jan2019-v2/MINIAOD", "CMS", ".*root", json) # 22Jan2019 to recover lumi lost in /SingleMuon/Run2018D-PromptReco-v2/MINIAOD
DoubleMuon_Run2018D_PromptReco_v2 = kreator.makeDataComponent("DoubleMuon_Run2018D_PromptReco_v2", "/DoubleMuon/Run2018D-PromptReco-v2/MINIAOD", "CMS", ".*root", json)
MuonEG_Run2018D_PromptReco_v2 = kreator.makeDataComponent("MuonEG_Run2018D_PromptReco_v2", "/MuonEG/Run2018D-PromptReco-v2/MINIAOD", "CMS", ".*root", json)
Tau_Run2018D_PromptReco_v2 = kreator.makeDataComponent("Tau_Run2018D_PromptReco_v2", "/Tau/Run2018D-PromptReco-v2/MINIAOD", "CMS", ".*root", json)

dataSamples_Run2018D_PromptReco_v2 = [JetHT_Run2018D_PromptReco_v2, MET_Run2018D_PromptReco_v2, EGamma_Run2018D_PromptReco_v2, SingleMuon_Run2018D_PromptReco_v2, DoubleMuon_Run2018D_PromptReco_v2, MuonEG_Run2018D_PromptReco_v2, Tau_Run2018D_PromptReco_v2]

dataSamples_17Sep2018_plus_Prompt = dataSamples_Run2018A_17Sep2018 + dataSamples_Run2018B_17Sep2018 + dataSamples_Run2018C_17Sep2018 + dataSamples_Run2018D_PromptReco_v2

dataSamples = dataSamples_17Sep2018_plus_Prompt

samples = dataSamples

# ---------------------------------------------------------------------

if __name__ == "__main__":
    from CMGTools.RootTools.samples.tools import runMain
    runMain(samples, localobjs=locals())
