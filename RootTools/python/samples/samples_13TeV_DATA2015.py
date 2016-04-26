import PhysicsTools.HeppyCore.framework.config as cfg
import os

#####COMPONENT CREATOR

from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()

### ----------------------------- Zero Tesla run  ----------------------------------------

dataDir = "$CMSSW_BASE/src/CMGTools/TTHAnalysis/data"  # use environmental variable, useful for instance to run on CRAB
json=dataDir+'/json/Cert_246908-256869_13TeV_PromptReco_Collisions15_25ns_JSON.txt'
#https://hypernews.cern.ch/HyperNews/CMS/get/physics-validation/2496.html
#golden JSON 166.37/pb 


#jetHT_0T = cfg.DataComponent(
#    name = 'jetHT_0T',
#    files = kreator.getFilesFromEOS('jetHT_0T',
#                                    'firstData_JetHT_v2',
#                                    '/store/user/pandolf/MINIAOD/%s'),
#    intLumi = 4.0,
#    triggers = [],
#    json = None #json
#    )


# PromptReco-v1 for run > 251561
run_range = (251643, 251883)
label = "_runs%s_%s"%(run_range[0], run_range[1])

JetHT_Run2015B_PromptReco          = kreator.makeDataComponent("JetHT_Run2015B_PromptReco"         , "/JetHT/Run2015B-PromptReco-v1/MINIAOD"         , "CMS", ".*root", json, run_range)
HTMHT_Run2015B_PromptReco          = kreator.makeDataComponent("HTMHT_Run2015B_PromptReco"         , "/HTMHT/Run2015B-PromptReco-v1/MINIAOD"         , "CMS", ".*root", json, run_range)
MET_Run2015B_PromptReco            = kreator.makeDataComponent("MET_Run2015B_PromptReco"           , "/MET/Run2015B-PromptReco-v1/MINIAOD"           , "CMS", ".*root", json, run_range)
SingleElectron_Run2015B_PromptReco = kreator.makeDataComponent("SingleElectron_Run2015B_PromptReco", "/SingleElectron/Run2015B-PromptReco-v1/MINIAOD", "CMS", ".*root", json, run_range)
SingleMuon_Run2015B_PromptReco     = kreator.makeDataComponent("SingleMuon_Run2015B_PromptReco"    , "/SingleMuon/Run2015B-PromptReco-v1/MINIAOD"    , "CMS", ".*root", json, run_range)
SinglePhoton_Run2015B_PromptReco   = kreator.makeDataComponent("SinglePhoton_Run2015B_PromptReco"  , "/SinglePhoton/Run2015B-PromptReco-v1/MINIAOD"  , "CMS", ".*root", json, run_range)
DoubleEG_Run2015B_PromptReco       = kreator.makeDataComponent("DoubleEG_Run2015B_PromptReco"      , "/DoubleEG/Run2015B-PromptReco-v1/MINIAOD"      , "CMS", ".*root", json, run_range)
MuonEG_Run2015B_PromptReco         = kreator.makeDataComponent("MuonEG_Run2015B_PromptReco"        , "/MuonEG/Run2015B-PromptReco-v1/MINIAOD"        , "CMS", ".*root", json, run_range)
DoubleMuon_Run2015B_PromptReco     = kreator.makeDataComponent("DoubleMuon_Run2015B_PromptReco"    , "/DoubleMuon/Run2015B-PromptReco-v1/MINIAOD"    , "CMS", ".*root", json, run_range)

#minBias_Run2015B  = kreator.makeDataComponent("minBias_Run2015B" , "/MinimumBias/Run2015B-PromptReco-v1/MINIAOD", "CMS", ".*root", json)
#zeroBias_Run2015B = kreator.makeDataComponent("zeroBias_Run2015B", "/ZeroBias/Run2015B-PromptReco-v1/MINIAOD"   , "CMS", ".*root", json)

dataSamples_Run2015B = [JetHT_Run2015B_PromptReco, HTMHT_Run2015B_PromptReco, MET_Run2015B_PromptReco, SingleElectron_Run2015B_PromptReco, SingleMuon_Run2015B_PromptReco, SinglePhoton_Run2015B_PromptReco, DoubleEG_Run2015B_PromptReco, MuonEG_Run2015B_PromptReco, DoubleMuon_Run2015B_PromptReco]

### ----------------------------- 17July re-reco ----------------------------------------
# https://twiki.cern.ch/twiki/bin/view/CMS/PdmVDataReprocessing747reMiniAod2015B

Jet_Run2015B_17Jul            = kreator.makeDataComponent("Jet_Run2015B_17Jul"           , "/Jet/Run2015B-17Jul2015-v1/MINIAOD"           , "CMS", ".*root", json)
JetHT_Run2015B_17Jul          = kreator.makeDataComponent("JetHT_Run2015B_17Jul"         , "/JetHT/Run2015B-17Jul2015-v1/MINIAOD"         , "CMS", ".*root", json)
HTMHT_Run2015B_17Jul          = kreator.makeDataComponent("HTMHT_Run2015B_17Jul"         , "/HTMHT/Run2015B-17Jul2015-v1/MINIAOD"         , "CMS", ".*root", json)
MET_Run2015B_17Jul            = kreator.makeDataComponent("MET_Run2015B_17Jul"           , "/MET/Run2015B-17Jul2015-v1/MINIAOD"           , "CMS", ".*root", json)
SingleElectron_Run2015B_17Jul = kreator.makeDataComponent("SingleElectron_Run2015B_17Jul", "/SingleElectron/Run2015B-17Jul2015-v1/MINIAOD", "CMS", ".*root", json)
SingleMu_Run2015B_17Jul       = kreator.makeDataComponent("SingleMu_Run2015B_17Jul"      , "/SingleMu/Run2015B-17Jul2015-v1/MINIAOD"      , "CMS", ".*root", json)
SingleMuon_Run2015B_17Jul     = kreator.makeDataComponent("SingleMuon_Run2015B_17Jul"    , "/SingleMuon/Run2015B-17Jul2015-v1/MINIAOD"    , "CMS", ".*root", json)
SinglePhoton_Run2015B_17Jul   = kreator.makeDataComponent("SinglePhoton_Run2015B_17Jul"  , "/SinglePhoton/Run2015B-17Jul2015-v1/MINIAOD"  , "CMS", ".*root", json)
EGamma_Run2015B_17Jul         = kreator.makeDataComponent("EGamma_Run2015B_17Jul"        , "/EGamma/Run2015B-17Jul2015-v1/MINIAOD"        , "CMS", ".*root", json)
DoubleEG_Run2015B_17Jul       = kreator.makeDataComponent("DoubleEG_Run2015B_17Jul"      , "/DoubleEG/Run2015B-17Jul2015-v1/MINIAOD"      , "CMS", ".*root", json)
MuonEG_Run2015B_17Jul         = kreator.makeDataComponent("MuonEG_Run2015B_17Jul"        , "/MuonEG/Run2015B-17Jul2015-v1/MINIAOD"        , "CMS", ".*root", json)
DoubleMuon_Run2015B_17Jul     = kreator.makeDataComponent("DoubleMuon_Run2015B_17Jul"    , "/DoubleMuon/Run2015B-17Jul2015-v1/MINIAOD"    , "CMS", ".*root", json)

#minBias_Run2015B_17Jul  = kreator.makeDataComponent("minBias_Run2015B_17Jul" , "/MinimumBias/Run2015B-17Jul2015-v1/MINIAOD", "CMS", ".*root", json)
zeroBias_Run2015B_17Jul = kreator.makeDataComponent("zeroBias_Run2015B_17Jul", "/ZeroBias/Run2015B-17Jul2015-v1/MINIAOD"   , "CMS", ".*root", json)

dataSamples_17Jul = [Jet_Run2015B_17Jul, JetHT_Run2015B_17Jul, HTMHT_Run2015B_17Jul, MET_Run2015B_17Jul, SingleElectron_Run2015B_17Jul, SingleMu_Run2015B_17Jul, SingleMuon_Run2015B_17Jul, SinglePhoton_Run2015B_17Jul, EGamma_Run2015B_17Jul, DoubleEG_Run2015B_17Jul, MuonEG_Run2015B_17Jul, DoubleMuon_Run2015B_17Jul, zeroBias_Run2015B_17Jul]

### ----------------------------- Run2015C ----------------------------------------

#Jet_Run2015C            = kreator.makeDataComponent("Jet_Run2015C"           , "/Jet/Run2015C-PromptReco-v1/MINIAOD"           , "CMS", ".*root", json)
JetHT_Run2015C          = kreator.makeDataComponent("JetHT_Run2015C"         , "/JetHT/Run2015C-PromptReco-v1/MINIAOD"         , "CMS", ".*root", json)
HTMHT_Run2015C          = kreator.makeDataComponent("HTMHT_Run2015C"         , "/HTMHT/Run2015C-PromptReco-v1/MINIAOD"         , "CMS", ".*root", json)
MET_Run2015C            = kreator.makeDataComponent("MET_Run2015C"           , "/MET/Run2015C-PromptReco-v1/MINIAOD"           , "CMS", ".*root", json)
SingleElectron_Run2015C = kreator.makeDataComponent("SingleElectron_Run2015C", "/SingleElectron/Run2015C-PromptReco-v1/MINIAOD", "CMS", ".*root", json)
SingleMuon_Run2015C     = kreator.makeDataComponent("SingleMuon_Run2015C"    , "/SingleMuon/Run2015C-PromptReco-v1/MINIAOD"    , "CMS", ".*root", json)
SinglePhoton_Run2015C   = kreator.makeDataComponent("SinglePhoton_Run2015C"  , "/SinglePhoton/Run2015C-PromptReco-v1/MINIAOD"  , "CMS", ".*root", json)
#EGamma_Run2015C         = kreator.makeDataComponent("EGamma_Run2015C"        , "/EGamma/Run2015C-PromptReco-v1/MINIAOD"        , "CMS", ".*root", json)
DoubleEG_Run2015C       = kreator.makeDataComponent("DoubleEG_Run2015C"      , "/DoubleEG/Run2015C-PromptReco-v1/MINIAOD"      , "CMS", ".*root", json)
MuonEG_Run2015C         = kreator.makeDataComponent("MuonEG_Run2015C"        , "/MuonEG/Run2015C-PromptReco-v1/MINIAOD"        , "CMS", ".*root", json)
DoubleMuon_Run2015C     = kreator.makeDataComponent("DoubleMuon_Run2015C"    , "/DoubleMuon/Run2015C-PromptReco-v1/MINIAOD"    , "CMS", ".*root", json)

minBias_Run2015C  = kreator.makeDataComponent("minBias_Run2015C" , "/MinimumBias/Run2015C-PromptReco-v1/MINIAOD", "CMS", ".*root", json)
zeroBias_Run2015C = kreator.makeDataComponent("zeroBias_Run2015C", "/ZeroBias/Run2015C-PromptReco-v1/MINIAOD"   , "CMS", ".*root", json)

dataSamples_Run2015C = [JetHT_Run2015C, HTMHT_Run2015C, MET_Run2015C, SingleElectron_Run2015C, SingleMuon_Run2015C, SinglePhoton_Run2015C, DoubleEG_Run2015C, MuonEG_Run2015C, DoubleMuon_Run2015C, minBias_Run2015C, zeroBias_Run2015C]

### ----------------------------- Run2015D miniAODv1 ----------------------------------------

#Jet_Run2015D            = kreator.makeDataComponent("Jet_Run2015D"           , "/Jet/Run2015D-PromptReco-v3/MINIAOD"           , "CMS", ".*root", json)
JetHT_Run2015D          = kreator.makeDataComponent("JetHT_Run2015D"         , "/JetHT/Run2015D-PromptReco-v3/MINIAOD"         , "CMS", ".*root", json)
HTMHT_Run2015D          = kreator.makeDataComponent("HTMHT_Run2015D"         , "/HTMHT/Run2015D-PromptReco-v3/MINIAOD"         , "CMS", ".*root", json)
MET_Run2015D            = kreator.makeDataComponent("MET_Run2015D"           , "/MET/Run2015D-PromptReco-v3/MINIAOD"           , "CMS", ".*root", json)
SingleElectron_Run2015D = kreator.makeDataComponent("SingleElectron_Run2015D", "/SingleElectron/Run2015D-PromptReco-v3/MINIAOD", "CMS", ".*root", json)
SingleMuon_Run2015D     = kreator.makeDataComponent("SingleMuon_Run2015D"    , "/SingleMuon/Run2015D-PromptReco-v3/MINIAOD"    , "CMS", ".*root", json)
SinglePhoton_Run2015D   = kreator.makeDataComponent("SinglePhoton_Run2015D"  , "/SinglePhoton/Run2015D-PromptReco-v3/MINIAOD"  , "CMS", ".*root", json)
#EGamma_Run2015D         = kreator.makeDataComponent("EGamma_Run2015D"        , "/EGamma/Run2015D-PromptReco-v3/MINIAOD"        , "CMS", ".*root", json)
DoubleEG_Run2015D       = kreator.makeDataComponent("DoubleEG_Run2015D"      , "/DoubleEG/Run2015D-PromptReco-v3/MINIAOD"      , "CMS", ".*root", json)
MuonEG_Run2015D         = kreator.makeDataComponent("MuonEG_Run2015D"        , "/MuonEG/Run2015D-PromptReco-v3/MINIAOD"        , "CMS", ".*root", json)
DoubleMuon_Run2015D     = kreator.makeDataComponent("DoubleMuon_Run2015D"    , "/DoubleMuon/Run2015D-PromptReco-v3/MINIAOD"    , "CMS", ".*root", json)

#minBias_Run2015D  = kreator.makeDataComponent("minBias_Run2015D" , "/MinimumBias/Run2015D-PromptReco-v3/MINIAOD", "CMS", ".*root", json)
#zeroBias_Run2015D = kreator.makeDataComponent("zeroBias_Run2015D", "/ZeroBias/Run2015D-PromptReco-v3/MINIAOD"   , "CMS", ".*root", json)

#dataSamples_Run2015D = [Jet_Run2015D, JetHT_Run2015D, HTMHT_Run2015D, MET_Run2015D, SingleElectron_Run2015D, SingleMuon_Run2015D, SinglePhoton_Run2015D, EGamma_Run2015D, DoubleEG_Run2015D, MuonEG_Run2015D, DoubleMuon_Run2015D, minBias_Run2015D, zeroBias_Run2015D]
dataSamples_Run2015D = [JetHT_Run2015D, HTMHT_Run2015D, MET_Run2015D, SingleElectron_Run2015D, SingleMuon_Run2015D, SinglePhoton_Run2015D, DoubleEG_Run2015D, MuonEG_Run2015D, DoubleMuon_Run2015D]


### ----------------------------- Run2015D miniAODv2 ----------------------------------------

JetHT_Run2015D_Promptv4          = kreator.makeDataComponent("JetHT_Run2015D_v4"         , "/JetHT/Run2015D-PromptReco-v4/MINIAOD"         , "CMS", ".*root", json)
HTMHT_Run2015D_Promptv4          = kreator.makeDataComponent("HTMHT_Run2015D_v4"         , "/HTMHT/Run2015D-PromptReco-v4/MINIAOD"         , "CMS", ".*root", json)
MET_Run2015D_Promptv4            = kreator.makeDataComponent("MET_Run2015D_v4"           , "/MET/Run2015D-PromptReco-v4/MINIAOD"           , "CMS", ".*root", json)
SingleElectron_Run2015D_Promptv4 = kreator.makeDataComponent("SingleElectron_Run2015D_v4", "/SingleElectron/Run2015D-PromptReco-v4/MINIAOD", "CMS", ".*root", json)
SingleMuon_Run2015D_Promptv4     = kreator.makeDataComponent("SingleMuon_Run2015D_v4"    , "/SingleMuon/Run2015D-PromptReco-v4/MINIAOD"    , "CMS", ".*root", json)
SinglePhoton_Run2015D_Promptv4   = kreator.makeDataComponent("SinglePhoton_Run2015D_v4"  , "/SinglePhoton/Run2015D-PromptReco-v4/MINIAOD"  , "CMS", ".*root", json)
DoubleEG_Run2015D_Promptv4       = kreator.makeDataComponent("DoubleEG_Run2015D_v4"      , "/DoubleEG/Run2015D-PromptReco-v4/MINIAOD"      , "CMS", ".*root", json)
MuonEG_Run2015D_Promptv4         = kreator.makeDataComponent("MuonEG_Run2015D_v4"        , "/MuonEG/Run2015D-PromptReco-v4/MINIAOD"        , "CMS", ".*root", json)
DoubleMuon_Run2015D_Promptv4     = kreator.makeDataComponent("DoubleMuon_Run2015D_v4"    , "/DoubleMuon/Run2015D-PromptReco-v4/MINIAOD"    , "CMS", ".*root", json)
Tau_Run2015D_Promptv4            = kreator.makeDataComponent("Tau_Run2015D_v4"           , "/Tau/Run2015D-PromptReco-v4/MINIAOD"           , "CMS", ".*root", json)

dataSamples_Run2015D_v4 = [JetHT_Run2015D_Promptv4, HTMHT_Run2015D_Promptv4, MET_Run2015D_Promptv4, SingleElectron_Run2015D_Promptv4, SingleMuon_Run2015D_Promptv4, SinglePhoton_Run2015D_Promptv4, DoubleEG_Run2015D_Promptv4, MuonEG_Run2015D_Promptv4, DoubleMuon_Run2015D_Promptv4, Tau_Run2015D_Promptv4]



### --- 05Oct2015 --- miniAOD 74X v2

JetHT_Run2015B_05Oct          = kreator.makeDataComponent("JetHT_Run2015B_05Oct"         , "/JetHT/Run2015B-05Oct2015-v1/MINIAOD"         , "CMS", ".*root", json)
HTMHT_Run2015B_05Oct          = kreator.makeDataComponent("HTMHT_Run2015B_05Oct"         , "/HTMHT/Run2015B-05Oct2015-v1/MINIAOD"         , "CMS", ".*root", json)
MET_Run2015B_05Oct            = kreator.makeDataComponent("MET_Run2015B_05Oct"           , "/MET/Run2015B-05Oct2015-v1/MINIAOD"           , "CMS", ".*root", json)
SingleElectron_Run2015B_05Oct = kreator.makeDataComponent("SingleElectron_Run2015B_05Oct", "/SingleElectron/Run2015B-05Oct2015-v1/MINIAOD", "CMS", ".*root", json)
SingleMuon_Run2015B_05Oct     = kreator.makeDataComponent("SingleMuon_Run2015B_05Oct"    , "/SingleMuon/Run2015B-05Oct2015-v1/MINIAOD"    , "CMS", ".*root", json)
SinglePhoton_Run2015B_05Oct   = kreator.makeDataComponent("SinglePhoton_Run2015B_05Oct"  , "/SinglePhoton/Run2015B-05Oct2015-v1/MINIAOD"  , "CMS", ".*root", json)
DoubleEG_Run2015B_05Oct       = kreator.makeDataComponent("DoubleEG_Run2015B_05Oct"      , "/DoubleEG/Run2015B-05Oct2015-v1/MINIAOD"      , "CMS", ".*root", json)
MuonEG_Run2015B_05Oct         = kreator.makeDataComponent("MuonEG_Run2015B_05Oct"        , "/MuonEG/Run2015B-05Oct2015-v1/MINIAOD"        , "CMS", ".*root", json)
DoubleMuon_Run2015B_05Oct     = kreator.makeDataComponent("DoubleMuon_Run2015B_05Oct"    , "/DoubleMuon/Run2015B-05Oct2015-v1/MINIAOD"    , "CMS", ".*root", json)

JetHT_Run2015C_50ns_05Oct          = kreator.makeDataComponent("JetHT_Run2015C_50ns_05Oct"         , "/JetHT/Run2015C_50ns-05Oct2015-v1/MINIAOD"         , "CMS", ".*root", json)
HTMHT_Run2015C_50ns_05Oct          = kreator.makeDataComponent("HTMHT_Run2015C_50ns_05Oct"         , "/HTMHT/Run2015C_50ns-05Oct2015-v1/MINIAOD"         , "CMS", ".*root", json)
MET_Run2015C_50ns_05Oct            = kreator.makeDataComponent("MET_Run2015C_50ns_05Oct"           , "/MET/Run2015C_50ns-05Oct2015-v1/MINIAOD"           , "CMS", ".*root", json)
SingleElectron_Run2015C_50ns_05Oct = kreator.makeDataComponent("SingleElectron_Run2015C_50ns_05Oct", "/SingleElectron/Run2015C_50ns-05Oct2015-v1/MINIAOD", "CMS", ".*root", json)
SingleMuon_Run2015C_50ns_05Oct     = kreator.makeDataComponent("SingleMuon_Run2015C_50ns_05Oct"    , "/SingleMuon/Run2015C_50ns-05Oct2015-v1/MINIAOD"    , "CMS", ".*root", json)
SinglePhoton_Run2015C_50ns_05Oct   = kreator.makeDataComponent("SinglePhoton_Run2015C_50ns_05Oct"  , "/SinglePhoton/Run2015C_50ns-05Oct2015-v1/MINIAOD"  , "CMS", ".*root", json)
DoubleEG_Run2015C_50ns_05Oct       = kreator.makeDataComponent("DoubleEG_Run2015C_50ns_05Oct"      , "/DoubleEG/Run2015C_50ns-05Oct2015-v1/MINIAOD"      , "CMS", ".*root", json)
MuonEG_Run2015C_50ns_05Oct         = kreator.makeDataComponent("MuonEG_Run2015C_50ns_05Oct"        , "/MuonEG/Run2015C_50ns-05Oct2015-v1/MINIAOD"        , "CMS", ".*root", json)
DoubleMuon_Run2015C_50ns_05Oct     = kreator.makeDataComponent("DoubleMuon_Run2015C_50ns_05Oct"    , "/DoubleMuon/Run2015C_50ns-05Oct2015-v1/MINIAOD"    , "CMS", ".*root", json)
Tau_Run2015C_50ns_05Oct            = kreator.makeDataComponent("Tau_Run2015C_50ns_05Oct"           , "/Tau/Run2015C_50ns-05Oct2015-v1/MINIAOD"           , "CMS", ".*root", json)

JetHT_Run2015C_25ns_05Oct          = kreator.makeDataComponent("JetHT_Run2015C_25ns_05Oct"         , "/JetHT/Run2015C_25ns-05Oct2015-v1/MINIAOD"         , "CMS", ".*root", json)
HTMHT_Run2015C_25ns_05Oct          = kreator.makeDataComponent("HTMHT_Run2015C_25ns_05Oct"         , "/HTMHT/Run2015C_25ns-05Oct2015-v1/MINIAOD"         , "CMS", ".*root", json)
MET_Run2015C_25ns_05Oct            = kreator.makeDataComponent("MET_Run2015C_25ns_05Oct"           , "/MET/Run2015C_25ns-05Oct2015-v1/MINIAOD"           , "CMS", ".*root", json)
SingleElectron_Run2015C_25ns_05Oct = kreator.makeDataComponent("SingleElectron_Run2015C_25ns_05Oct", "/SingleElectron/Run2015C_25ns-05Oct2015-v1/MINIAOD", "CMS", ".*root", json)
SingleMuon_Run2015C_25ns_05Oct     = kreator.makeDataComponent("SingleMuon_Run2015C_25ns_05Oct"    , "/SingleMuon/Run2015C_25ns-05Oct2015-v1/MINIAOD"    , "CMS", ".*root", json)
SinglePhoton_Run2015C_25ns_05Oct   = kreator.makeDataComponent("SinglePhoton_Run2015C_25ns_05Oct"  , "/SinglePhoton/Run2015C_25ns-05Oct2015-v1/MINIAOD"  , "CMS", ".*root", json)
DoubleEG_Run2015C_25ns_05Oct       = kreator.makeDataComponent("DoubleEG_Run2015C_25ns_05Oct"      , "/DoubleEG/Run2015C_25ns-05Oct2015-v1/MINIAOD"      , "CMS", ".*root", json)
MuonEG_Run2015C_25ns_05Oct         = kreator.makeDataComponent("MuonEG_Run2015C_25ns_05Oct"        , "/MuonEG/Run2015C_25ns-05Oct2015-v1/MINIAOD"        , "CMS", ".*root", json)
DoubleMuon_Run2015C_25ns_05Oct     = kreator.makeDataComponent("DoubleMuon_Run2015C_25ns_05Oct"    , "/DoubleMuon/Run2015C_25ns-05Oct2015-v1/MINIAOD"    , "CMS", ".*root", json)
Tau_Run2015C_25ns_05Oct            = kreator.makeDataComponent("Tau_Run2015C_25ns_05Oct"           , "/Tau/Run2015C_25ns-05Oct2015-v1/MINIAOD"           , "CMS", ".*root", json)

JetHT_Run2015D_05Oct          = kreator.makeDataComponent("JetHT_Run2015D_05Oct"         , "/JetHT/Run2015D-05Oct2015-v1/MINIAOD"         , "CMS", ".*root", json)
HTMHT_Run2015D_05Oct          = kreator.makeDataComponent("HTMHT_Run2015D_05Oct"         , "/HTMHT/Run2015D-05Oct2015-v1/MINIAOD"         , "CMS", ".*root", json)
MET_Run2015D_05Oct            = kreator.makeDataComponent("MET_Run2015D_05Oct"           , "/MET/Run2015D-05Oct2015-v1/MINIAOD"           , "CMS", ".*root", json)
SingleElectron_Run2015D_05Oct = kreator.makeDataComponent("SingleElectron_Run2015D_05Oct", "/SingleElectron/Run2015D-05Oct2015-v1/MINIAOD", "CMS", ".*root", json)
SingleMuon_Run2015D_05Oct     = kreator.makeDataComponent("SingleMuon_Run2015D_05Oct"    , "/SingleMuon/Run2015D-05Oct2015-v1/MINIAOD"    , "CMS", ".*root", json)
SinglePhoton_Run2015D_05Oct   = kreator.makeDataComponent("SinglePhoton_Run2015D_05Oct"  , "/SinglePhoton/Run2015D-05Oct2015-v1/MINIAOD"  , "CMS", ".*root", json)
DoubleEG_Run2015D_05Oct       = kreator.makeDataComponent("DoubleEG_Run2015D_05Oct"      , "/DoubleEG/Run2015D-05Oct2015-v1/MINIAOD"      , "CMS", ".*root", json)
MuonEG_Run2015D_05Oct         = kreator.makeDataComponent("MuonEG_Run2015D_05Oct"        , "/MuonEG/Run2015D-05Oct2015-v2/MINIAOD"        , "CMS", ".*root", json)
DoubleMuon_Run2015D_05Oct     = kreator.makeDataComponent("DoubleMuon_Run2015D_05Oct"    , "/DoubleMuon/Run2015D-05Oct2015-v1/MINIAOD"    , "CMS", ".*root", json)
Tau_Run2015D_05Oct            = kreator.makeDataComponent("Tau_Run2015D_05Oct"           , "/Tau/Run2015D-05Oct2015-v1/MINIAOD"           , "CMS", ".*root", json)

dataSamples_Run2015B_05Oct = [JetHT_Run2015B_05Oct, HTMHT_Run2015B_05Oct, MET_Run2015B_05Oct, SingleElectron_Run2015B_05Oct, SingleMuon_Run2015B_05Oct, SinglePhoton_Run2015B_05Oct, DoubleEG_Run2015B_05Oct, MuonEG_Run2015B_05Oct, DoubleMuon_Run2015B_05Oct]
dataSamples_Run2015C_25ns_05Oct = [JetHT_Run2015C_25ns_05Oct, HTMHT_Run2015C_25ns_05Oct, MET_Run2015C_25ns_05Oct, SingleElectron_Run2015C_25ns_05Oct, SingleMuon_Run2015C_25ns_05Oct, SinglePhoton_Run2015C_25ns_05Oct, DoubleEG_Run2015C_25ns_05Oct, MuonEG_Run2015C_25ns_05Oct, DoubleMuon_Run2015C_25ns_05Oct]
dataSamples_Run2015C_50ns_05Oct = [JetHT_Run2015C_50ns_05Oct, HTMHT_Run2015C_50ns_05Oct, MET_Run2015C_50ns_05Oct, SingleElectron_Run2015C_50ns_05Oct, SingleMuon_Run2015C_50ns_05Oct, SinglePhoton_Run2015C_50ns_05Oct, DoubleEG_Run2015C_50ns_05Oct, MuonEG_Run2015C_50ns_05Oct, DoubleMuon_Run2015C_50ns_05Oct]
dataSamples_Run2015D_05Oct = [JetHT_Run2015D_05Oct, HTMHT_Run2015D_05Oct, MET_Run2015D_05Oct, SingleElectron_Run2015D_05Oct, SingleMuon_Run2015D_05Oct, SinglePhoton_Run2015D_05Oct, DoubleEG_Run2015D_05Oct, MuonEG_Run2015D_05Oct, DoubleMuon_Run2015D_05Oct, Tau_Run2015D_05Oct]
dataSamples_Run2015_05Oct = dataSamples_Run2015B_05Oct + dataSamples_Run2015C_25ns_05Oct + dataSamples_Run2015C_50ns_05Oct + dataSamples_Run2015D_05Oct



### --- 16Dec2015 --- miniAOD 76X

#JetHT_Run2015B_16Dec          = kreator.makeDataComponent("JetHT_Run2015B_16Dec"         , "/JetHT/Run2015B-16Dec2015-v1/MINIAOD"         , "CMS", ".*root", json)
HTMHT_Run2015B_16Dec          = kreator.makeDataComponent("HTMHT_Run2015B_16Dec"         , "/HTMHT/Run2015B-16Dec2015-v1/MINIAOD"         , "CMS", ".*root", json)
MET_Run2015B_16Dec            = kreator.makeDataComponent("MET_Run2015B_16Dec"           , "/MET/Run2015B-16Dec2015-v1/MINIAOD"           , "CMS", ".*root", json)
SingleElectron_Run2015B_16Dec = kreator.makeDataComponent("SingleElectron_Run2015B_16Dec", "/SingleElectron/Run2015B-16Dec2015-v1/MINIAOD", "CMS", ".*root", json)
SingleMuon_Run2015B_16Dec     = kreator.makeDataComponent("SingleMuon_Run2015B_16Dec"    , "/SingleMuon/Run2015B-16Dec2015-v1/MINIAOD"    , "CMS", ".*root", json)
SinglePhoton_Run2015B_16Dec   = kreator.makeDataComponent("SinglePhoton_Run2015B_16Dec"  , "/SinglePhoton/Run2015B-16Dec2015-v1/MINIAOD"  , "CMS", ".*root", json)
DoubleEG_Run2015B_16Dec       = kreator.makeDataComponent("DoubleEG_Run2015B_16Dec"      , "/DoubleEG/Run2015B-16Dec2015-v1/MINIAOD"      , "CMS", ".*root", json)
MuonEG_Run2015B_16Dec         = kreator.makeDataComponent("MuonEG_Run2015B_16Dec"        , "/MuonEG/Run2015B-16Dec2015-v1/MINIAOD"        , "CMS", ".*root", json)
DoubleMuon_Run2015B_16Dec     = kreator.makeDataComponent("DoubleMuon_Run2015B_16Dec"    , "/DoubleMuon/Run2015B-16Dec2015-v1/MINIAOD"    , "CMS", ".*root", json)
Tau_Run2015B_16Dec            = kreator.makeDataComponent("Tau_Run2015B_16Dec"           , "/Tau/Run2015B-16Dec2015-v1/MINIAOD"           , "CMS", ".*root", json)

JetHT_Run2015C_50ns_16Dec          = kreator.makeDataComponent("JetHT_Run2015C_50ns_16Dec"         , "/JetHT/Run2015C_50ns-16Dec2015-v1/MINIAOD"         , "CMS", ".*root", json)
HTMHT_Run2015C_50ns_16Dec          = kreator.makeDataComponent("HTMHT_Run2015C_50ns_16Dec"         , "/HTMHT/Run2015C_50ns-16Dec2015-v1/MINIAOD"         , "CMS", ".*root", json)
MET_Run2015C_50ns_16Dec            = kreator.makeDataComponent("MET_Run2015C_50ns_16Dec"           , "/MET/Run2015C_50ns-16Dec2015-v1/MINIAOD"           , "CMS", ".*root", json)
SingleElectron_Run2015C_50ns_16Dec = kreator.makeDataComponent("SingleElectron_Run2015C_50ns_16Dec", "/SingleElectron/Run2015C_50ns-16Dec2015-v1/MINIAOD", "CMS", ".*root", json)
SingleMuon_Run2015C_50ns_16Dec     = kreator.makeDataComponent("SingleMuon_Run2015C_50ns_16Dec"    , "/SingleMuon/Run2015C_50ns-16Dec2015-v1/MINIAOD"    , "CMS", ".*root", json)
SinglePhoton_Run2015C_50ns_16Dec   = kreator.makeDataComponent("SinglePhoton_Run2015C_50ns_16Dec"  , "/SinglePhoton/Run2015C_50ns-16Dec2015-v1/MINIAOD"  , "CMS", ".*root", json)
DoubleEG_Run2015C_50ns_16Dec       = kreator.makeDataComponent("DoubleEG_Run2015C_50ns_16Dec"      , "/DoubleEG/Run2015C_50ns-16Dec2015-v1/MINIAOD"      , "CMS", ".*root", json)
MuonEG_Run2015C_50ns_16Dec         = kreator.makeDataComponent("MuonEG_Run2015C_50ns_16Dec"        , "/MuonEG/Run2015C_50ns-16Dec2015-v1/MINIAOD"        , "CMS", ".*root", json)
DoubleMuon_Run2015C_50ns_16Dec     = kreator.makeDataComponent("DoubleMuon_Run2015C_50ns_16Dec"    , "/DoubleMuon/Run2015C_50ns-16Dec2015-v1/MINIAOD"    , "CMS", ".*root", json)
Tau_Run2015C_50ns_16Dec            = kreator.makeDataComponent("Tau_Run2015C_50ns_16Dec"           , "/Tau/Run2015C_50ns-16Dec2015-v1/MINIAOD"           , "CMS", ".*root", json)

JetHT_Run2015C_25ns_16Dec          = kreator.makeDataComponent("JetHT_Run2015C_25ns_16Dec"         , "/JetHT/Run2015C_25ns-16Dec2015-v1/MINIAOD"         , "CMS", ".*root", json)
HTMHT_Run2015C_25ns_16Dec          = kreator.makeDataComponent("HTMHT_Run2015C_25ns_16Dec"         , "/HTMHT/Run2015C_25ns-16Dec2015-v1/MINIAOD"         , "CMS", ".*root", json)
MET_Run2015C_25ns_16Dec            = kreator.makeDataComponent("MET_Run2015C_25ns_16Dec"           , "/MET/Run2015C_25ns-16Dec2015-v1/MINIAOD"           , "CMS", ".*root", json)
SingleElectron_Run2015C_25ns_16Dec = kreator.makeDataComponent("SingleElectron_Run2015C_25ns_16Dec", "/SingleElectron/Run2015C_25ns-16Dec2015-v1/MINIAOD", "CMS", ".*root", json)
SingleMuon_Run2015C_25ns_16Dec     = kreator.makeDataComponent("SingleMuon_Run2015C_25ns_16Dec"    , "/SingleMuon/Run2015C_25ns-16Dec2015-v1/MINIAOD"    , "CMS", ".*root", json)
SinglePhoton_Run2015C_25ns_16Dec   = kreator.makeDataComponent("SinglePhoton_Run2015C_25ns_16Dec"  , "/SinglePhoton/Run2015C_25ns-16Dec2015-v1/MINIAOD"  , "CMS", ".*root", json)
DoubleEG_Run2015C_25ns_16Dec       = kreator.makeDataComponent("DoubleEG_Run2015C_25ns_16Dec"      , "/DoubleEG/Run2015C_25ns-16Dec2015-v1/MINIAOD"      , "CMS", ".*root", json)
MuonEG_Run2015C_25ns_16Dec         = kreator.makeDataComponent("MuonEG_Run2015C_25ns_16Dec"        , "/MuonEG/Run2015C_25ns-16Dec2015-v1/MINIAOD"        , "CMS", ".*root", json)
DoubleMuon_Run2015C_25ns_16Dec     = kreator.makeDataComponent("DoubleMuon_Run2015C_25ns_16Dec"    , "/DoubleMuon/Run2015C_25ns-16Dec2015-v1/MINIAOD"    , "CMS", ".*root", json)
Tau_Run2015C_25ns_16Dec            = kreator.makeDataComponent("Tau_Run2015C_25ns_16Dec"           , "/Tau/Run2015C_25ns-16Dec2015-v1/MINIAOD"           , "CMS", ".*root", json)

JetHT_Run2015D_16Dec          = kreator.makeDataComponent("JetHT_Run2015D_16Dec"         , "/JetHT/Run2015D-16Dec2015-v1/MINIAOD"         , "CMS", ".*root", json)
HTMHT_Run2015D_16Dec          = kreator.makeDataComponent("HTMHT_Run2015D_16Dec"         , "/HTMHT/Run2015D-16Dec2015-v1/MINIAOD"         , "CMS", ".*root", json)
MET_Run2015D_16Dec            = kreator.makeDataComponent("MET_Run2015D_16Dec"           , "/MET/Run2015D-16Dec2015-v1/MINIAOD"           , "CMS", ".*root", json)
SingleElectron_Run2015D_16Dec = kreator.makeDataComponent("SingleElectron_Run2015D_16Dec", "/SingleElectron/Run2015D-16Dec2015-v1/MINIAOD", "CMS", ".*root", json)
SingleMuon_Run2015D_16Dec     = kreator.makeDataComponent("SingleMuon_Run2015D_16Dec"    , "/SingleMuon/Run2015D-16Dec2015-v1/MINIAOD"    , "CMS", ".*root", json)
SinglePhoton_Run2015D_16Dec   = kreator.makeDataComponent("SinglePhoton_Run2015D_16Dec"  , "/SinglePhoton/Run2015D-16Dec2015-v1/MINIAOD"  , "CMS", ".*root", json)
DoubleEG_Run2015D_16Dec       = kreator.makeDataComponent("DoubleEG_Run2015D_16Dec"      , "/DoubleEG/Run2015D-16Dec2015-v2/MINIAOD"      , "CMS", ".*root", json)
MuonEG_Run2015D_16Dec         = kreator.makeDataComponent("MuonEG_Run2015D_16Dec"        , "/MuonEG/Run2015D-16Dec2015-v1/MINIAOD"        , "CMS", ".*root", json)
DoubleMuon_Run2015D_16Dec     = kreator.makeDataComponent("DoubleMuon_Run2015D_16Dec"    , "/DoubleMuon/Run2015D-16Dec2015-v1/MINIAOD"    , "CMS", ".*root", json)
Tau_Run2015D_16Dec            = kreator.makeDataComponent("Tau_Run2015D_16Dec"           , "/Tau/Run2015D-16Dec2015-v1/MINIAOD"           , "CMS", ".*root", json)

dataSamples_Run2015B_16Dec = [HTMHT_Run2015B_16Dec, MET_Run2015B_16Dec, SingleElectron_Run2015B_16Dec, SingleMuon_Run2015B_16Dec, SinglePhoton_Run2015B_16Dec, DoubleEG_Run2015B_16Dec, MuonEG_Run2015B_16Dec, DoubleMuon_Run2015B_16Dec, Tau_Run2015B_16Dec]
dataSamples_Run2015C_50ns_16Dec = [JetHT_Run2015C_50ns_16Dec, HTMHT_Run2015C_50ns_16Dec, MET_Run2015C_50ns_16Dec, SingleElectron_Run2015C_50ns_16Dec, SingleMuon_Run2015C_50ns_16Dec, SinglePhoton_Run2015C_50ns_16Dec, DoubleEG_Run2015C_50ns_16Dec, MuonEG_Run2015C_50ns_16Dec, DoubleMuon_Run2015C_50ns_16Dec, Tau_Run2015C_50ns_16Dec]
dataSamples_Run2015C_25ns_16Dec = [JetHT_Run2015C_25ns_16Dec, HTMHT_Run2015C_25ns_16Dec, MET_Run2015C_25ns_16Dec, SingleElectron_Run2015C_25ns_16Dec, SingleMuon_Run2015C_25ns_16Dec, SinglePhoton_Run2015C_25ns_16Dec, DoubleEG_Run2015C_25ns_16Dec, MuonEG_Run2015C_25ns_16Dec, DoubleMuon_Run2015C_25ns_16Dec, Tau_Run2015C_25ns_16Dec]
dataSamples_Run2015D_16Dec = [JetHT_Run2015D_16Dec, HTMHT_Run2015D_16Dec, MET_Run2015D_16Dec, SingleElectron_Run2015D_16Dec, SingleMuon_Run2015D_16Dec, SinglePhoton_Run2015D_16Dec, DoubleEG_Run2015D_16Dec, MuonEG_Run2015D_16Dec, DoubleMuon_Run2015D_16Dec, Tau_Run2015D_16Dec]
dataSamples_Run2015_16Dec = dataSamples_Run2015B_16Dec + dataSamples_Run2015C_50ns_16Dec + dataSamples_Run2015C_25ns_16Dec + dataSamples_Run2015D_16Dec



### ----------------------------- summary ----------------------------------------

dataSamples_74Xv1 = dataSamples_Run2015B + dataSamples_Run2015C + dataSamples_Run2015D + dataSamples_17Jul
dataSamples_74Xv2 = dataSamples_Run2015_05Oct + dataSamples_Run2015D_v4
dataSamples_76X = dataSamples_Run2015_16Dec
dataSamples = dataSamples_74Xv1 + dataSamples_74Xv2 + dataSamples_76X
samples = dataSamples

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
