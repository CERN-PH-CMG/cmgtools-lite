import PhysicsTools.HeppyCore.framework.config as cfg
import os

#####COMPONENT CREATOR

from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()
dataDir = "$CMSSW_BASE/src/CMGTools/TTHAnalysis/data"  # use environmental variable, useful for instance to run on CRAB
#json=dataDir+'/json/Cert_246908-257599_13TeV_PromptReco_Collisions15_25ns_JSON_v3_private.txt'
#https://hypernews.cern.ch/HyperNews/CMS/get/physics-validation/2503.html
#golden JSON 225.57/pb

# https://hypernews.cern.ch/HyperNews/CMS/get/physics-validation/2520.html -- 800/pb
#json="/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/Cert_246908-258714_13TeV_PromptReco_Collisions15_25ns_JSON.txt"
# https://hypernews.cern.ch/HyperNews/CMS/get/physics-validation/2522.html -- 1200/pb
#json="/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/Cert_246908-258750_13TeV_PromptReco_Collisions15_25ns_JSON.txt"
# 1.6/fb
#json="/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/Cert_246908-259891_13TeV_PromptReco_Collisions15_25ns_JSON.txt"
# 2.1/fb
#json="/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/Cert_246908-260627_13TeV_PromptReco_Collisions15_25ns_JSON.txt"
#json="/afs/desy.de/group/cms/pool/lobanov/SUSY/Run2/CMG/Development/CMSSW_7_4_14/src/CMGTools/SUSYAnalysis/data/json/myEle_JSON_diff.txt"
## FINAL GOLDEN JSON for Run2015
# 2.3/fb
json="/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/Cert_246908-260627_13TeV_PromptReco_Collisions15_25ns_JSON_v2.txt"
#json="/afs/desy.de/group/cms/pool/lobanov/SUSY/Run2/CMG/Development/CMSSW_7_4_14/src/CMGTools/SUSYAnalysis/python/samples/diffMu.json"


### ----------------------------- Run2015D miniAODv2 ----------------------------------------
###https://hypernews.cern.ch/HyperNews/CMS/get/physics-announcements/3561.html

JetHT_Run2015D_Promptv4          = kreator.makeDataComponentDESY("JetHT_Run2015D_v4"         , "/JetHT/Run2015D-PromptReco-v4/MINIAOD"         , "CMS", ".*root", json,jsonFilter=True)
SingleElectron_Run2015D_Promptv4 = kreator.makeDataComponentDESY("SingleElectron_Run2015D_v4", "/SingleElectron/Run2015D-PromptReco-v4/MINIAOD", "CMS", ".*root", json,jsonFilter=True)
SingleMuon_Run2015D_Promptv4     = kreator.makeDataComponentDESY("SingleMuon_Run2015D_v4"    , "/SingleMuon/Run2015D-PromptReco-v4/MINIAOD"    , "CMS", ".*root", json,jsonFilter=True)
#SingleMuon_Run2015D_Promptv4     = kreator.makeDataComponent("SingleMuon_Run2015D_v4"    , "/SingleMuon/Run2015D-PromptReco-v4/MINIAOD"    , "CMS", ".*root", json,jsonFilter=True)

dataSamples_Run2015D_v4 = [JetHT_Run2015D_Promptv4, SingleElectron_Run2015D_Promptv4, SingleMuon_Run2015D_Promptv4]

### ----------------------------- Run2015D-05Oct2015 ----------------------------------------
## https://hypernews.cern.ch/HyperNews/CMS/get/datasets/4154.html

JetHT_Run2015D_05Oct          = kreator.makeDataComponentDESY("JetHT_Run2015D_05Oct"         , "/JetHT/Run2015D-05Oct2015-v1/MINIAOD"         , "CMS", ".*root", json,jsonFilter=True)
SingleElectron_Run2015D_05Oct = kreator.makeDataComponentDESY("SingleElectron_Run2015D_05Oct", "/SingleElectron/Run2015D-05Oct2015-v1/MINIAOD", "CMS", ".*root", json,jsonFilter=True)
SingleMuon_Run2015D_05Oct     = kreator.makeDataComponentDESY("SingleMuon_Run2015D_05Oct"    , "/SingleMuon/Run2015D-05Oct2015-v1/MINIAOD"    , "CMS", ".*root", json,jsonFilter=True)

dataSamples_Run2015D_05Oct = [JetHT_Run2015D_05Oct, SingleElectron_Run2015D_05Oct, SingleMuon_Run2015D_05Oct]

### ----------------------------- summary ----------------------------------------

dataSamples = dataSamples_Run2015D_v4 + dataSamples_Run2015D_05Oct
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
