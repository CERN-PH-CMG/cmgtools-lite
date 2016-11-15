import PhysicsTools.HeppyCore.framework.config as cfg
import os

#####COMPONENT CREATOR

from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()

### ----------------------------- 25 ns ----------------------------------------
# TTbar cross section: NNLO, https://twiki.cern.ch/twiki/bin/view/LHCPhysics/TtbarNNLO (172.5)
TTJets_LO_25ns = kreator.makeMCComponentFromDESY("TTJets_LO_25ns", "/TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/MINIAODSIM", "CMS", ".*root", 831.76)
# single/di-lepton
TTJets_SingleLeptonFromT = kreator.makeMCComponentFromDESY("TTJets_SingleLeptonFromT", "/TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM", "CMS", ".*root", 831.76*(3*0.108)*(1-3*0.108))
TTJets_SingleLeptonFromT_ext1 = kreator.makeMCComponentFromDESY("TTJets_SingleLeptonFromT_ext1", "/TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9_ext1-v1/MINIAODSIM", "CMS", ".*root", 831.76*(3*0.108)*(1-3*0.108))
TTJets_SingleLeptonFromTbar = kreator.makeMCComponentFromDESY("TTJets_SingleLeptonFromTbar", "/TTJets_SingleLeptFromTbar_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/MINIAODSIM", "CMS", ".*root", 831.76*(3*0.108)*(1-3*0.108))
TTJets_SingleLeptonFromTbar_ext1 = kreator.makeMCComponentFromDESY("TTJets_SingleLeptonFromTbar_ext1", "/TTJets_SingleLeptFromTbar_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9_ext1-v1/MINIAODSIM", "CMS", ".*root", 831.76*(3*0.108)*(1-3*0.108))
TTJets_DiLepton = kreator.makeMCComponentFromDESY("TTJets_DiLepton", "/TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/MINIAODSIM", "CMS", ".*root", 831.76*((3*0.108)**2))
TTJets_DiLepton_ext1 = kreator.makeMCComponentFromDESY("TTJets_DiLepton_ext1", "/TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9_ext1-v1/MINIAODSIM", "CMS", ".*root", 831.76*((3*0.108)**2))

##HT binned samples
TTJets_HT600to800 = kreator.makeMCComponentFromDESY("TTJets_HT600to800", "/TTJets_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM", "CMS", ".*root", 1.61*1.655)
TTJets_HT800to1200 = kreator.makeMCComponentFromDESY("TTJets_HT800to1200", "/TTJets_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM", "CMS", ".*root", 0.663*1.655)
TTJets_HT1200to2500 = kreator.makeMCComponentFromDESY("TTJets_HT1200to2500", "/TTJets_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM", "CMS", ".*root", 0.12*1.655)
TTJets_HT2500toInf = kreator.makeMCComponentFromDESY("TTJets_HT2500toInf", "/TTJets_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM", "CMS", ".*root", 0.00143*1.655)

TTs = [ TTJets_LO_25ns , TTJets_SingleLeptonFromT, TTJets_SingleLeptonFromT_ext1, TTJets_SingleLeptonFromTbar, TTJets_SingleLeptonFromTbar_ext1, TTJets_DiLepton, TTJets_DiLepton_ext1, TTJets_HT600to800 , TTJets_HT800to1200, TTJets_HT1200to2500, TTJets_HT2500toInf]

### V+jets inclusive (from https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat13TeV)
WJetsToLNu = kreator.makeMCComponentFromDESY("WJetsToLNu","/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM", "CMS", ".*root", 3* 20508.9)
DYJetsToLL_M50 = kreator.makeMCComponentFromDESY("DYJetsToLL_M50", "/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v3/MINIAODSIM", "CMS", ".*root", 2008.*3)

# Single top cross sections: https://twiki.cern.ch/twiki/bin/viewauth/CMS/SingleTopSigma
TToLeptons_tch = kreator.makeMCComponentFromDESY("TToLeptons_tch", "/ST_t-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM", "CMS", ".*root", (136.05+80.97)*0.108*3)
TToLeptons_sch = kreator.makeMCComponentFromDESY("TToLeptons_sch", "/ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM", "CMS", ".*root", (7.20+4.16)*0.108*3)
TBar_tWch = kreator.makeMCComponentFromDESY("TBar_tWch", "/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM", "CMS", ".*root",35.6)
T_tWch = kreator.makeMCComponentFromDESY("T_tWch", "/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM", "CMS", ".*root",35.6)

SingleTop = [
    TToLeptons_tch, TToLeptons_sch, TBar_tWch, T_tWch
]

## DYjets
DYJetsToLL_M50_HT100to200 = kreator.makeMCComponent("DYJetsToLL_M50_HT100to200", "/DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/MINIAODSIM", "CMS", ".*root",139.4*1.27)
DYJetsToLL_M50_HT200to400 = kreator.makeMCComponent("DYJetsToLL_M50_HT200to400", "/DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/MINIAODSIM", "CMS", ".*root",42.75*1.27)
DYJetsToLL_M50_HT400to600 = kreator.makeMCComponent("DYJetsToLL_M50_HT400to600", "/DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/MINIAODSIM", "CMS", ".*root",5.497*1.27)
DYJetsToLL_M50_HT600toInf = kreator.makeMCComponent("DYJetsToLL_M50_HT600toInf", "/DYJetsToLL_M-50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/MINIAODSIM", "CMS", ".*root",2.21*1.27)
DYJetsM50HT = [
DYJetsToLL_M50_HT100to200,
DYJetsToLL_M50_HT200to400,
DYJetsToLL_M50_HT400to600,
DYJetsToLL_M50_HT600toInf,
]

VJets = [ WJetsToLNu, DYJetsToLL_M50 ]

## TT+V (W,Z,H)
TTZToLLNuNu_25ns = kreator.makeMCComponentFromDESY("TTZToLLNuNu_25ns","/TTZToLLNuNu_M-10_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM", "CMS", ".*root", 0.2529 )
TTZToQQ_25ns = kreator.makeMCComponentFromDESY("TTZToQQ_25ns","/TTZToQQ_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM", "CMS", ".*root", 0.5297 )
TTWJetsToLNu_25ns = kreator.makeMCComponentFromDESY("TTWJetsToLNu_25ns","/TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM", "CMS", ".*root", 0.2043 )
TTWJetsToQQ_25ns = kreator.makeMCComponentFromDESY("TTWJetsToQQ_25ns","/TTWJetsToQQ_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM", "CMS", ".*root", 0.4062 )

TTV = [ TTZToLLNuNu_25ns, TTZToQQ_25ns, TTWJetsToQQ_25ns, TTWJetsToLNu_25ns ]

### W+jets

### W+jets

WJetsToLNu_HT100to200 = kreator.makeMCComponentFromDESY("WJetsToLNu_HT100to200", "/WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM", "CMS", ".*root",1347*1.23)
WJetsToLNu_HT200to400 = kreator.makeMCComponentFromDESY("WJetsToLNu_HT200to400", "/WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM", "CMS", ".*root",360*1.23)
WJetsToLNu_HT400to600 = kreator.makeMCComponentFromDESY("WJetsToLNu_HT400to600", "/WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v3/MINIAODSIM", "CMS", ".*root",48.9*1.23)
WJetsToLNu_HT600toInf = kreator.makeMCComponentFromDESY("WJetsToLNu_HT600toInf", "/WJetsToLNu_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM", "CMS", ".*root",18.77*1.23)
WJetsToLNu_HT600to800 = kreator.makeMCComponentFromDESY("WJetsToLNu_HT600to800", "/WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/MINIAODSIM", "CMS", ".*root",12.8*1.23)
WJetsToLNu_HT800to1200 = kreator.makeMCComponentFromDESY("WJetsToLNu_HT800to1200", "/WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM", "CMS", ".*root",5.26*1.23)
WJetsToLNu_HT1200to2500 = kreator.makeMCComponentFromDESY("WJetsToLNu_HT1200to2500", "/WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM", "CMS", ".*root",1.33*1.23)
WJetsToLNu_HT2500toInf = kreator.makeMCComponentFromDESY("WJetsToLNu_HT2500toInf", "/WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/MINIAODSIM", "CMS", ".*root",0.03089*1.23)
WJetsToLNuHT = [
WJetsToLNu_HT100to200,
WJetsToLNu_HT200to400,
WJetsToLNu_HT400to600,
WJetsToLNu_HT600toInf,
WJetsToLNu_HT600to800,
WJetsToLNu_HT800to1200,
WJetsToLNu_HT1200to2500,
WJetsToLNu_HT2500toInf
]

## QCD multijets HT binned
QCD_HT100to200 = kreator.makeMCComponentFromDESY("QCD_HT100to200","/QCD_HT100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/MINIAODSIM","CMS",".*root",27540000)
QCD_HT200to300 = kreator.makeMCComponentFromDESY("QCD_HT200to300","/QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/MINIAODSIM","CMS",".*root",1735000)
QCD_HT300to500 = kreator.makeMCComponentFromDESY("QCD_HT300to500","/QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/MINIAODSIM","CMS",".*root",366800)
QCD_HT500to700 = kreator.makeMCComponentFromDESY("QCD_HT500to700","/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM","CMS",".*root",29370)
QCD_HT700to1000 = kreator.makeMCComponentFromDESY("QCD_HT700to1000","/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM","CMS",".*root",6524)
QCD_HT1000to1500 = kreator.makeMCComponentFromDESY("QCD_HT1000to1500","/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/MINIAODSIM","CMS",".*root",1064)
QCD_HT1500to2000 = kreator.makeMCComponentFromDESY("QCD_HT1500to2000","/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM","CMS",".*root",121.5)
QCD_HT2000toInf = kreator.makeMCComponentFromDESY("QCD_HT2000toInf","/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM","CMS",".*root",25.42)

QCD_HT = [
    QCD_HT100to200,
    QCD_HT200to300,
    QCD_HT300to500,
    QCD_HT500to700,
    QCD_HT700to1000,
    QCD_HT1000to1500,
    QCD_HT1500to2000,
    QCD_HT2000toInf
]

### ----------------------------- 50 ns ----------------------------------------
#TTJets_50ns = kreator.makeMCComponentFromDESY("TTJets_50ns", "/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM", "CMS", ".*root", 831.76,)
TTJets_LO_50ns = kreator.makeMCComponentFromDESY("TTJets_LO_50ns", "/TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM", "CMS", ".*root", 831.76)

### V+jets inclusive
DYJetsToLL_M50_50ns = kreator.makeMCComponentFromDESY("DYJetsToLL_M50_50ns","/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2/MINIAODSIM", "CMS", ".*root", 2008.*3)
WJetsToLNu_50ns = kreator.makeMCComponentFromDESY("WJetsToLNu_50ns","/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM", "CMS", ".*root", 20508.9*3)

TToLeptons_tch_50ns = kreator.makeMCComponent("TToLeptons_tch_50ns", "/ST_t-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM", "CMS", ".*root", (136.05+80.97)*0.108*3)
TBar_tWch_50ns = kreator.makeMCComponent("TBar_tWch_50ns", "/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2/MINIAODSIM", "CMS", ".*root",35.6)
T_tWch_50ns = kreator.makeMCComponent("T_tWch_50ns", "/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM", "CMS", ".*root",35.6)

SingleTop_50ns = [
    TToLeptons_tch_50ns, TBar_tWch_50ns, T_tWch_50ns
]

### OFFICIAL SMS SIGNALS
T1tttt_mGo_1500to1525_mLSP_50to1125 = kreator.makeMCComponent("T1tttt_mGo_1500to1525_mLSP_50to1125", "/SMS-T1tttt_mGluino-1500to1525_mLSP-50to1125_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15FSPremix-MCRUN2_74_V9-v1/MINIAODSIM", "CMS", ".*root")


### ----------  Reprocessed PHYS14 SIGNAL samples ------------
# location: /nfs/dust/cms/group/susy-desy/Run2/MC/MiniAOD/RunIISpring15DR74/FromGiovanni
T1tttt_mGo1500_mChi100 = kreator.makePrivateMCComponentFromDir('T1tttt_mGo1500_mChi100', '/T1tttt_mGo1500_mChi100/', '/nfs/dust/cms/group/susy-desy/Run2/MC/MiniAOD/RunIISpring15DR74/FromGiovanni/', '*.root', 0.0141903)
T1tttt_mGo1200_mChi800 = kreator.makePrivateMCComponentFromDir('T1tttt_mGo1200_mChi800', '/T1tttt_mGo1200_mChi800/', '/nfs/dust/cms/group/susy-desy/Run2/MC/MiniAOD/RunIISpring15DR74/FromGiovanni/', '*.root', 0.0856418)
T1tttt_priv = [ T1tttt_mGo1500_mChi100, T1tttt_mGo1200_mChi800 ]

### ----------------------------- summary ----------------------------------------

mcSamples_Asymptotic25ns = TTs + VJets + WJetsToLNuHT + QCD_HT + TTV + DYJetsM50HT + SingleTop

mcSamples_Asymptotic50ns = [ TTJets_LO_50ns, WJetsToLNu_50ns, DYJetsToLL_M50_50ns ] + SingleTop_50ns

mcSamples = mcSamples_Asymptotic25ns + mcSamples_Asymptotic50ns

mcSamplesSignal = [ T1tttt_mGo_1500to1525_mLSP_50to1125 ]

mcSamplesPriv = T1tttt_priv

samples = mcSamplesSignal + mcSamples + mcSamplesPriv

dataSamples = []

### ---------------------------------------------------------------------

from CMGTools.TTHAnalysis.setup.Efficiencies import *
dataDir = "$CMSSW_BASE/src/CMGTools/TTHAnalysis/data"

#Define splitting
for comp in mcSamples:
    comp.isMC = True
    comp.isData = False
    comp.splitFactor = 250 #  if comp.name in [ "WJets", "DY3JetsM50", "DY4JetsM50","W1Jets","W2Jets","W3Jets","W4Jets","TTJetsHad" ] else 100
    comp.puFileMC=dataDir+"/puProfile_Summer15_74X.root"
    comp.puFileData=dataDir+"/puProfile_Data15_70mb.root"
    comp.efficiency = eff2012

for comp in dataSamples:
    comp.splitFactor = 1000
    comp.isMC = False
    comp.isData = True

if __name__ == "__main__":
   import sys
   if "test" in sys.argv:
       from CMGTools.RootTools.samples.ComponentCreator import testSamples
       testSamples(samples)
