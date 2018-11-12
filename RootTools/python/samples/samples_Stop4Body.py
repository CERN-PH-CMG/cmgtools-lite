import PhysicsTools.HeppyCore.framework.config as cfg
import os

#####COMPONENT CREATOR

from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()

SMS_T1bbbb_mGluino1500_mLSP100 = kreator.makeMCComponent("SMS_T1bbbb_mGluino1500_mLSP100", "/SMS-T1bbbb_mGluino-1500_mLSP-100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv1-PUSpring16_80X_mcRun2_asymptotic_2016_v3-v1/MINIAODSIM", "CMS", ".*root", 0.0141903)
SMS_T1tttt_mGluino1500_mLSP100 = kreator.makeMCComponent("SMS_T1tttt_mGluino1500_mLSP100", "/SMS-T1tttt_mGluino-1500_mLSP-100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv1-PUSpring16_80X_mcRun2_asymptotic_2016_v3-v1/MINIAODSIM", "CMS", ".*root", 0.0141903)


SMS_T2tt_dM_10to80_genHT_160_genMET_80                = kreator.makeMCComponent("SMS_T2tt_dM_10to80_genHT_160_genMET_80",               "/SMS-T2tt_dM-10to80_genHT-160_genMET-80_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16Fast_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM",  "CMS", ".*root" )
SMS_T2tt_dM_10to80_genHT_160_genMET_80_mWMin_0p1      = kreator.makeMCComponent("SMS_T2tt_dM_10to80_genHT_160_genMET_80_mWMin_0p1",    "/SMS-T2tt_dM-10to80_genHT-160_genMET-80_mWMin-0p1_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16Fast_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM" ,  "CMS", ".*root", useAAA = True)
SMS_T2bW_X05_dM_10to80_genHT_160_genMET_80_mWMin_0p1  = kreator.makeMCComponent("SMS_T2bW_X05_dM_10to80_genHT_160_genMET_80_mWMin_0p1", "/SMS-T2bW_X05_dM-10to80_genHT-160_genMET-80_mWMin-0p1_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16Fast_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM" ,  "CMS", ".*root", useAAA = True )



## FullSIM ###
SMS_T2tt_genHT_160_genMET_80_mStop_275_mLSP_205   =    kreator.makeMCComponent( "SMS_T2tt_genHT_160_genMET_80_mStop_275_mLSP_205"  ,  "/SMS-T2-4bd_genMET-80_mStop-275_mLSP-205_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root" , xSec=13.32)
SMS_T2tt_genHT_160_genMET_80_mStop_350_mLSP_330   =    kreator.makeMCComponent( "SMS_T2tt_genHT_160_genMET_80_mStop_350_mLSP_330"  ,  "/SMS-T2-4bd_genMET-80_mStop-350_mLSP-330_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root" , xSec=3.786)
SMS_T2tt_genHT_160_genMET_80_mStop_400_mLSP_350   =    kreator.makeMCComponent( "SMS_T2tt_genHT_160_genMET_80_mStop_400_mLSP_350"  ,  "/SMS-T2-4bd_genMET-80_mStop-400_mLSP-350_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root" , xSec=1.835)

signalFullSim= [
SMS_T1bbbb_mGluino1500_mLSP100,
SMS_T1tttt_mGluino1500_mLSP100,
SMS_T2tt_genHT_160_genMET_80_mStop_275_mLSP_205,
SMS_T2tt_genHT_160_genMET_80_mStop_350_mLSP_330,
SMS_T2tt_genHT_160_genMET_80_mStop_400_mLSP_350,
]


SMS_TChiWZ_ZToLL  = kreator.makeMCComponent("SMS_TChiWZ_ZToLL", "/SMS-TChiWZ_ZToLL_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16Fast_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v2/MINIAODSIM",  "CMS", ".*root", )
SMS_TChipmWW      = kreator.makeMCComponent("SMS_TChipmWW"    , "/SMS-TChipmWW_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16Fast_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM", "CMS", ".*root" )



SMS_T2tt_dM_10to80_2Lfilter  = kreator.makeMCComponent("SMS_T2tt_dM_10to80_2Lfilter", "/SMS-T2tt_dM-10to80_2Lfilter_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16Fast_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM" , "CMS", ".*root", )


SignalSUSY = [
SMS_T2tt_dM_10to80_genHT_160_genMET_80,
SMS_T2tt_dM_10to80_2Lfilter,
SMS_T2tt_dM_10to80_genHT_160_genMET_80_mWMin_0p1,
SMS_T2bW_X05_dM_10to80_genHT_160_genMET_80_mWMin_0p1,
]

### -----2017
## FullSIM ###
SMS_T2_4bd_genMET_80_mStop_500_mLSP_420 = kreator.makeMCComponent("SMS_T2_4bd_genMET_80_mStop_500_mLSP_420","/SMS-T2-4bd_genMET-80_mStop-500_mLSP-420_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM", "CMS", ".*root")
SMS_T2_4bd_genMET_80_mStop_500_mLSP_490 = kreator.makeMCComponent("SMS_T2_4bd_genMET_80_mStop_500_mLSP_490","/SMS-T2-4bd_genMET-80_mStop-500_mLSP-490_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM", "CMS", ".*root")

signalFullSim2017 = [
SMS_T2_4bd_genMET_80_mStop_500_mLSP_420,
SMS_T2_4bd_genMET_80_mStop_500_mLSP_490
]

### ----------------------------- summary ----------------------------------------

signalSamples = SignalSUSY
samples = signalSamples + signalFullSim + signalFullSim2017

### ---------------------------------------------------------------------

from CMGTools.TTHAnalysis.setup.Efficiencies import *
dataDir = "$CMSSW_BASE/src/CMGTools/TTHAnalysis/data"

#Define splitting
for comp in signalSamples:
    comp.isMC = True
    comp.isData = False
    comp.isFastSim = True
    comp.splitFactor = 250 #  if comp.name in [ "WJets", "DY3JetsM50", "DY4JetsM50","W1Jets","W2Jets","W3Jets","W4Jets","TTJetsHad" ] else 100

for comp in signalFullSim:
    comp.isMC = True
    comp.isData = False
    comp.isFastSim = False
    comp.splitFactor = 250 #  if comp.name in [ "WJets", "DY3JetsM50", "DY4JetsM50","W1Jets","W2Jets","W3Jets","W4Jets","TTJetsHad" ] else 100

for comp in signalFullSim2017:
    comp.isMC = True
    comp.isData = False
    comp.isFastSim = False

if __name__ == "__main__":
    from CMGTools.RootTools.samples.tools import runMain
    runMain(samples, localobjs=locals())
    import sys
    if "test" in sys.argv:
        from CMGTools.RootTools.samples.ComponentCreator import testSamples
        testSamples(samples)
