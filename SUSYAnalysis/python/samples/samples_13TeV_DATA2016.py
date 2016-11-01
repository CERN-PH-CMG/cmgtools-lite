import PhysicsTools.HeppyCore.framework.config as cfg
import os

#####COMPONENT CREATOR

from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()

### ----------------------------- Zero Tesla run  ----------------------------------------

dataDir = "$CMSSW_BASE/src/CMGTools/TTHAnalysis/data"  # use environmental variable, useful for instance to run on CRAB
#json=dataDir+'/json/Cert_271036-276097_13TeV_PromptReco_Collisions16_JSON_NoL1T_v2.txt'

## top up from 7.7/fb json to 12.9/fb
json=dataDir+'/json/Cert_271036-276811_13TeV_PromptReco_Collisions16_JSON_NoL1T.txt'

#https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions16/13TeV/
#https://hypernews.cern.ch/HyperNews/CMS/get/physics-validation/2657.html
#with recorded luminosity: 804.2/pb


#jetHT_0T = cfg.DataComponent(
#    name = 'jetHT_0T',
#    files = kreator.getFilesFromEOS('jetHT_0T',
#                                    'firstData_JetHT_v2',
#                                    '/store/user/pandolf/MINIAOD/%s'),
#    intLumi = 4.0,
#    triggers = [],
#    json = None #json
#    )


### ----------------------------- Run2016 PromptReco v1 ----------------------------------------

'''
HTMHT_Run2016B_PromptReco          = kreator.makeDataComponent("HTMHT_Run2016B_PromptReco"         , "/HTMHT/Run2016B-PromptReco-v1/MINIAOD"         , "CMS", ".*root", json)
MET_Run2016B_PromptReco            = kreator.makeDataComponent("MET_Run2016B_PromptReco"           , "/MET/Run2016B-PromptReco-v1/MINIAOD"           , "CMS", ".*root", json)
SinglePhoton_Run2016B_PromptReco   = kreator.makeDataComponent("SinglePhoton_Run2016B_PromptReco"  , "/SinglePhoton/Run2016B-PromptReco-v1/MINIAOD"  , "CMS", ".*root", json)
DoubleEG_Run2016B_PromptReco       = kreator.makeDataComponent("DoubleEG_Run2016B_PromptReco"      , "/DoubleEG/Run2016B-PromptReco-v1/MINIAOD"      , "CMS", ".*root", json)
MuonEG_Run2016B_PromptReco         = kreator.makeDataComponent("MuonEG_Run2016B_PromptReco"       , "/MuonEG/Run2016B-PromptReco-v1/MINIAOD"        , "CMS", ".*root", json)
DoubleMuon_Run2016B_PromptReco     = kreator.makeDataComponent("DoubleMuon_Run2016B_PromptReco"    , "/DoubleMuon/Run2016B-PromptReco-v1/MINIAOD"    , "CMS", ".*root", json)

JetHT_Run2016B_PromptReco          = kreator.makeDataComponent("JetHT_Run2016B_PromptReco"         , "/JetHT/Run2016B-PromptReco-v1/MINIAOD"         , "CMS", ".*root", json)
SingleElectron_Run2016B_PromptReco = kreator.makeDataComponent("SingleElectron_Run2016B_PromptReco", "/SingleElectron/Run2016B-PromptReco-v1/MINIAOD", "CMS", ".*root", json)
SingleMuon_Run2016B_PromptReco     = kreator.makeDataComponent("SingleMuon_Run2016B_PromptReco"    , "/SingleMuon/Run2016B-PromptReco-v1/MINIAOD"    , "CMS", ".*root", json)
'''
#dataSamples_Run2016_v1 = [JetHT_Run2016B_PromptReco, HTMHT_Run2016B_PromptReco, MET_Run2016B_PromptReco, SingleElectron_Run2016B_PromptReco, SingleMuon_Run2016B_PromptReco, SinglePhoton_Run2016B_PromptReco, DoubleEG_Run2016B_PromptReco, MuonEG_Run2016B_PromptReco, DoubleMuon_Run2016B_PromptReco]
#dataSamples_Run2016_v1 = [SingleElectron_Run2016B_PromptReco, SingleMuon_Run2016B_PromptReco]

### ----------------------------- Run2016B PromptReco v2 ----------------------------------------

'''
JetHT_Run2016B_PromptReco_v2          = kreator.makeDataComponent("JetHT_Run2016B_PromptReco_v2"         , "/JetHT/Run2016B-PromptReco-v2/MINIAOD"         , "CMS", ".*root", json)
HTMHT_Run2016B_PromptReco_v2          = kreator.makeDataComponent("HTMHT_Run2016B_PromptReco_v2"         , "/HTMHT/Run2016B-PromptReco-v2/MINIAOD"         , "CMS", ".*root", json)
'''
MET_Run2016B_PromptReco_v2            = kreator.makeDataComponent("MET_Run2016B_PromptReco_v2"           , "/MET/Run2016B-PromptReco-v2/MINIAOD"           , "CMS", ".*root", json)
'''
SingleElectron_Run2016B_PromptReco_v2 = kreator.makeDataComponent("SingleElectron_Run2016B_PromptReco_v2", "/SingleElectron/Run2016B-PromptReco-v2/MINIAOD", "CMS", ".*root", json)
SingleMuon_Run2016B_PromptReco_v2     = kreator.makeDataComponent("SingleMuon_Run2016B_PromptReco_v2"    , "/SingleMuon/Run2016B-PromptReco-v2/MINIAOD"    , "CMS", ".*root", json)
SinglePhoton_Run2016B_PromptReco_v2   = kreator.makeDataComponent("SinglePhoton_Run2016B_PromptReco_v2"  , "/SinglePhoton/Run2016B-PromptReco-v2/MINIAOD"  , "CMS", ".*root", json)
DoubleEG_Run2016B_PromptReco_v2       = kreator.makeDataComponent("DoubleEG_Run2016B_PromptReco_v2"      , "/DoubleEG/Run2016B-PromptReco-v2/MINIAOD"      , "CMS", ".*root", json)
MuonEG_Run2016B_PromptReco_v2        = kreator.makeDataComponent("MuonEG_Run2016B_PromptReco_v2"        , "/MuonEG/Run2016B-PromptReco-v2/MINIAOD"        , "CMS", ".*root", json)
DoubleMuon_Run2016B_PromptReco_v2     = kreator.makeDataComponent("DoubleMuon_Run2016B_PromptReco_v2"    , "/DoubleMuon/Run2016B-PromptReco-v2/MINIAOD"    , "CMS", ".*root", json)
'''
SingleElectron_Run2016B_PromptReco_v2 = kreator.makeDataComponent("SingleElectron_Run2016B_PromptReco_v2", "/SingleElectron/Run2016B-PromptReco-v2/MINIAOD", "CMS", ".*root", json)
SingleMuon_Run2016B_PromptReco_v2     = kreator.makeDataComponent("SingleMuon_Run2016B_PromptReco_v2"    , "/SingleMuon/Run2016B-PromptReco-v2/MINIAOD"    , "CMS", ".*root", json)

#JetHT_Run2016B_PromptReco_v2_HT800Only     = kreator.makeDataComponent("JetHT_Run2016B_PromptReco_v2_HT800Only"         , "/JetHT/Run2016B-PromptReco-v2/MINIAOD"         , "CMS", ".*root", json, triggers=['HLT_PFHT800_v*','HLT_PFHT400_v*'])

#dataSamples_Run2016B_v2 = [JetHT_Run2016B_PromptReco_v2, HTMHT_Run2016B_PromptReco_v2, MET_Run2016B_PromptReco_v2, SingleElectron_Run2016B_PromptReco_v2, SingleMuon_Run2016B_PromptReco_v2, SinglePhoton_Run2016B_PromptReco_v2, DoubleEG_Run2016B_PromptReco_v2, MuonEG_Run2016B_PromptReco_v2, DoubleMuon_Run2016B_PromptReco_v2, JetHT_Run2016B_PromptReco_v2_HT800Only]

dataSamples_Run2016B_v2 = [SingleElectron_Run2016B_PromptReco_v2, SingleMuon_Run2016B_PromptReco_v2, MET_Run2016B_PromptReco_v2]

### ----------------------------- Run2016C PromptReco v2 ----------------------------------------

'''
JetHT_Run2016C_PromptReco_v2          = kreator.makeDataComponent("JetHT_Run2016C_PromptReco_v2"         , "/JetHT/Run2016C-PromptReco-v2/MINIAOD"         , "CMS", ".*root", json)
HTMHT_Run2016C_PromptReco_v2          = kreator.makeDataComponent("HTMHT_Run2016C_PromptReco_v2"         , "/HTMHT/Run2016C-PromptReco-v2/MINIAOD"         , "CMS", ".*root", json)
'''
MET_Run2016C_PromptReco_v2            = kreator.makeDataComponent("MET_Run2016C_PromptReco_v2"           , "/MET/Run2016C-PromptReco-v2/MINIAOD"           , "CMS", ".*root", json)
'''
SingleElectron_Run2016C_PromptReco_v2 = kreator.makeDataComponent("SingleElectron_Run2016C_PromptReco_v2", "/SingleElectron/Run2016C-PromptReco-v2/MINIAOD", "CMS", ".*root", json)
SingleMuon_Run2016C_PromptReco_v2     = kreator.makeDataComponent("SingleMuon_Run2016C_PromptReco_v2"    , "/SingleMuon/Run2016C-PromptReco-v2/MINIAOD"    , "CMS", ".*root", json)
SinglePhoton_Run2016C_PromptReco_v2   = kreator.makeDataComponent("SinglePhoton_Run2016C_PromptReco_v2"  , "/SinglePhoton/Run2016C-PromptReco-v2/MINIAOD"  , "CMS", ".*root", json)
DoubleEG_Run2016C_PromptReco_v2       = kreator.makeDataComponent("DoubleEG_Run2016C_PromptReco_v2"      , "/DoubleEG/Run2016C-PromptReco-v2/MINIAOD"      , "CMS", ".*root", json)
MuonEG_Run2016C_PromptReco_v2        = kreator.makeDataComponent("MuonEG_Run2016C_PromptReco_v2"        , "/MuonEG/Run2016C-PromptReco-v2/MINIAOD"        , "CMS", ".*root", json)
DoubleMuon_Run2016C_PromptReco_v2     = kreator.makeDataComponent("DoubleMuon_Run2016C_PromptReco_v2"    , "/DoubleMuon/Run2016C-PromptReco-v2/MINIAOD"    , "CMS", ".*root", json)

JetHT_Run2016C_PromptReco_v2_HT800Only     = kreator.makeDataComponent("JetHT_Run2016C_PromptReco_v2_HT800Only"         , "/JetHT/Run2016C-PromptReco-v2/MINIAOD"         , "CMS", ".*root", json, useAAA=True, triggers=['HLT_PFHT800_v*','HLT_PFHT400_v*'])
'''
SingleElectron_Run2016C_PromptReco_v2 = kreator.makeDataComponent("SingleElectron_Run2016C_PromptReco_v2", "/SingleElectron/Run2016C-PromptReco-v2/MINIAOD", "CMS", ".*root", json)
SingleMuon_Run2016C_PromptReco_v2     = kreator.makeDataComponent("SingleMuon_Run2016C_PromptReco_v2"    , "/SingleMuon/Run2016C-PromptReco-v2/MINIAOD"    , "CMS", ".*root", json)

#dataSamples_Run2016C_v2 = [JetHT_Run2016C_PromptReco_v2, HTMHT_Run2016C_PromptReco_v2, MET_Run2016C_PromptReco_v2, SingleElectron_Run2016C_PromptReco_v2, SingleMuon_Run2016C_PromptReco_v2, SinglePhoton_Run2016C_PromptReco_v2, DoubleEG_Run2016C_PromptReco_v2, MuonEG_Run2016C_PromptReco_v2, DoubleMuon_Run2016C_PromptReco_v2, JetHT_Run2016C_PromptReco_v2_HT800Only]
dataSamples_Run2016C_v2 = [SingleElectron_Run2016C_PromptReco_v2, SingleMuon_Run2016C_PromptReco_v2, MET_Run2016C_PromptReco_v2]

#### ----------------------------- Run2016D PromptReco v2 ----------------------------------------
#
#JetHT_Run2016D_PromptReco_v2          = kreator.makeDataComponent("JetHT_Run2016D_PromptReco_v2"         , "/JetHT/Run2016D-PromptReco-v2/MINIAOD"         , "CMS", ".*root", json)
#HTMHT_Run2016D_PromptReco_v2          = kreator.makeDataComponent("HTMHT_Run2016D_PromptReco_v2"         , "/HTMHT/Run2016D-PromptReco-v2/MINIAOD"         , "CMS", ".*root", json)
MET_Run2016D_PromptReco_v2            = kreator.makeDataComponent("MET_Run2016D_PromptReco_v2"           , "/MET/Run2016D-PromptReco-v2/MINIAOD"           , "CMS", ".*root", json)
SingleElectron_Run2016D_PromptReco_v2 = kreator.makeDataComponent("SingleElectron_Run2016D_PromptReco_v2", "/SingleElectron/Run2016D-PromptReco-v2/MINIAOD", "CMS", ".*root", json)
SingleMuon_Run2016D_PromptReco_v2     = kreator.makeDataComponent("SingleMuon_Run2016D_PromptReco_v2"    , "/SingleMuon/Run2016D-PromptReco-v2/MINIAOD"    , "CMS", ".*root", json)
#SinglePhoton_Run2016D_PromptReco_v2   = kreator.makeDataComponent("SinglePhoton_Run2016D_PromptReco_v2"  , "/SinglePhoton/Run2016D-PromptReco-v2/MINIAOD"  , "CMS", ".*root", json)
#DoubleEG_Run2016D_PromptReco_v2       = kreator.makeDataComponent("DoubleEG_Run2016D_PromptReco_v2"      , "/DoubleEG/Run2016D-PromptReco-v2/MINIAOD"      , "CMS", ".*root", json)
#MuonEG_Run2016D_PromptReco_v2        = kreator.makeDataComponent("MuonEG_Run2016D_PromptReco_v2"        , "/MuonEG/Run2016D-PromptReco-v2/MINIAOD"        , "CMS", ".*root", json)
#DoubleMuon_Run2016D_PromptReco_v2     = kreator.makeDataComponent("DoubleMuon_Run2016D_PromptReco_v2"    , "/DoubleMuon/Run2016D-PromptReco-v2/MINIAOD"    , "CMS", ".*root", json)
#
#JetHT_Run2016D_PromptReco_v2_HT800Only     = kreator.makeDataComponent("JetHT_Run2016D_PromptReco_v2_HT800Only"         , "/JetHT/Run2016D-PromptReco-v2/MINIAOD"         , "CMS", ".*root", json, triggers=['HLT_PFHT800_v*','HLT_PFHT400_v*'])
#
#dataSamples_Run2016D_v2 = [JetHT_Run2016D_PromptReco_v2, HTMHT_Run2016D_PromptReco_v2, MET_Run2016D_PromptReco_v2, SingleElectron_Run2016D_PromptReco_v2, SingleMuon_Run2016D_PromptReco_v2, SinglePhoton_Run2016D_PromptReco_v2, DoubleEG_Run2016D_PromptReco_v2, MuonEG_Run2016D_PromptReco_v2, DoubleMuon_Run2016D_PromptReco_v2, JetHT_Run2016D_PromptReco_v2_HT800Only]

dataSamples_Run2016D_v2 = [MET_Run2016D_PromptReco_v2, SingleElectron_Run2016D_PromptReco_v2, SingleMuon_Run2016D_PromptReco_v2]
### ----------------------------- summary ----------------------------------------

dataSamples_PromptReco = dataSamples_Run2016B_v2 + dataSamples_Run2016C_v2 + dataSamples_Run2016D_v2
samples = dataSamples_PromptReco

MET_BCD = [MET_Run2016B_PromptReco_v2, MET_Run2016C_PromptReco_v2, MET_Run2016D_PromptReco_v2]

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
