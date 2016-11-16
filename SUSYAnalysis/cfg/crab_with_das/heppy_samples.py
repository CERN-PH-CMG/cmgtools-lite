#-------- SAMPLES AND TRIGGERS -----------
##from CMGTools.TTHAnalysis.samples.samples_13TeV_PHYS14 import *
#from CMGTools.RootTools.samples.samples_13TeV_74X import *
#from CMGTools.RootTools.samples.samples_13TeV_DATA2015 import *
#from CMGTools.RootTools.samples.triggers_13TeV_Spring15 import *
#from CMGTools.RootTools.samples.triggers_13TeV_Spring15_1l import *
##from CMGTools.RootTools.samples.samples_13TeV_80X_signals import *
#from CMGTools.RootTools.samples.samples_13TeV_DATA2016 import *
from CMGTools.RootTools.samples.samples_13TeV_Moriond2017 import *
from CMGTools.RootTools.samples.samples_13TeV_RunIISpring16MiniAODv2 import *

###applying the correct json files to PrompReco and July17 samples
#for sample in dataSamples_Run2015B:
##  sample.json = "$CMSSW_BASE/src/CMGTools/TTHAnalysis/data/json/Cert_246908-251883_13TeV_PromptReco_Collisio#ns15_JSON_v2_Non17Jul2015.txt"
#  sample.json = "$CMSSW_BASE/src/CMGTools/TTHAnalysis/data/json/Cert_246908-251883_13TeV_PromptReco_Collision#s15_JSON_v2.txt"
#for sample in dataSamples_17Jul:
##  sample.json = "$CMSSW_BASE/src/CMGTools/TTHAnalysis/data/json/Cert_246908-251883_13TeV_PromptReco_Collisio#ns15_JSON_v2_17Jul2015.txt"
#  sample.json = "$CMSSW_BASE/src/CMGTools/TTHAnalysis/data/json/Cert_246908-251883_13TeV_PromptReco_Collision#s15_JSON_v2.txt"
#for sample in dataSamples_Run2015D:
#  sample.json = "$CMSSW_BASE/src/CMGTools/TTHAnalysis/data/json/Cert_246908-257599_13TeV_PromptReco_Collisions15_25ns_JSON.json"

for sample in dataSamples_Moriond2017: 
  #sample.json = "$CMSSW_BASE/src/CMGTools/SUSYAnalysis/data/Cert_271036-273730_13TeV_PromptReco_Collisions16_JSON.txt"
  #sample.json = "$CMSSW_BASE/src/CMGTools/SUSYAnalysis/data/Cert_271036-274443_13TeV_PromptReco_Collisions16_JSON.txt"
  #sample.json = "$CMSSW_BASE/src/CMGTools/SUSYAnalysis/data/Cert_271036-276097_13TeV_PromptReco_Collisions16_JSON_NoL1T_v2.txt"
  sample.json = "$CMSSW_BASE/src/CMGTools/SUSYAnalysis/data/Cert_271036-284044_13TeV_PromptReco_Collisions16_JSON_NoL1T.txt"
