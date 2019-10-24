import PhysicsTools.HeppyCore.framework.config as cfg
import os

#####COMPONENT CREATOR

from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()

### NB: Commented lines refer to samples available in RunIIFall15MiniAODv2 but not yet in RunIISpring16MiniAODv1

### ----------------------------- 25 ns ----------------------------------------

# TTbar cross section: NNLO, https://twiki.cern.ch/twiki/bin/view/LHCPhysics/TtbarNNLO (172.5)
TTJets = kreator.makeMCComponent("TTJets", "/TTJets_TuneCUETP8M2T4_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root", 831.76, fracNegWeights=0.319)

TT_pow = kreator.makeMCComponent("TT_pow", "/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM", "CMS", ".*root", 831.762)

TTJets_SingleLeptonFromTbar     = kreator.makeMCComponent("TTJets_SingleLeptonFromTbar"    , "/TTJets_SingleLeptFromTbar_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root", 831.76*(3*0.108)*(1-3*0.108) )
TTJets_SingleLeptonFromTbar_ext = kreator.makeMCComponent("TTJets_SingleLeptonFromTbar_ext", "/TTJets_SingleLeptFromTbar_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM", "CMS", ".*root", 831.76*(3*0.108)*(1-3*0.108) )
TTJets_SingleLeptonFromT        = kreator.makeMCComponent("TTJets_SingleLeptonFromT"       , "/TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root", 831.76*(3*0.108)*(1-3*0.108))
TTJets_SingleLeptonFromT_ext    = kreator.makeMCComponent("TTJets_SingleLeptonFromT_ext"   , "/TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM", "CMS", ".*root", 831.76*(3*0.108)*(1-3*0.108))
TTJets_DiLepton                 = kreator.makeMCComponent("TTJets_DiLepton"                , "/TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM"     , "CMS", ".*root", 831.76*((3*0.108)**2) )
TTJets_DiLepton_ext             = kreator.makeMCComponent("TTJets_DiLepton_ext"            , "/TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM", "CMS", ".*root", 831.76*((3*0.108)**2) )

TTLep_pow = kreator.makeMCComponent("TTLep_pow", "/TTTo2L2Nu_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root", 831.76*((3*0.108)**2) )
TTSemi_pow = kreator.makeMCComponent("TTSemi_pow", "/TTToSemilepton_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root", 2*831.76*(3*0.108)*(1-3*0.108) )

#
TTJets_LO_HT600to800   = kreator.makeMCComponent("TTJets_LO_HT600to800", "/TTJets_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM", "CMS", ".*root", 1.610*831.76/502.2)
TTJets_LO_HT800to1200  = kreator.makeMCComponent("TTJets_LO_HT800to1200", "/TTJets_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM",  "CMS", ".*root", 0.663*831.76/502.2)
TTJets_LO_HT1200to2500 = kreator.makeMCComponent("TTJets_LO_HT1200to2500", "/TTJets_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM", "CMS", ".*root", 0.12*831.76/502.2)
TTJets_LO_HT2500toInf  = kreator.makeMCComponent("TTJets_LO_HT2500toInf", "/TTJets_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM",  "CMS", ".*root", 0.001430*831.76/502.2)


TTs = [
TTJets,
TT_pow,
TTJets_SingleLeptonFromTbar,
TTJets_SingleLeptonFromTbar_ext,
TTJets_SingleLeptonFromT,
TTJets_SingleLeptonFromT_ext,
TTJets_DiLepton,
TTJets_DiLepton_ext,
TTLep_pow,
TTSemi_pow,
TTJets_LO_HT600to800,
TTJets_LO_HT800to1200,
TTJets_LO_HT1200to2500,
TTJets_LO_HT2500toInf
]



# Higgs
# TTH cross section from LHC Higgs XS WG: https://twiki.cern.ch/twiki/bin/view/LHCPhysics/CERNYellowReportPageAt1314TeV?rev=15
TTHnobb_pow = kreator.makeMCComponent("TTHnobb_pow", "/ttHToNonbb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root",0.5085*(1-0.577))
TTHnobb_fxfx = kreator.makeMCComponent("TTHnobb_fxfx", "/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM", "CMS", ".*root", 0.5085*(1-0.577), fracNegWeights=0.35)
TTH_ctcvcp = kreator.makeMCComponent("TTH_ctcvcp", "/ttH_4f_ctcvcp_TuneCP5_13TeV_madgraph_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM", "CMS", ".*root", 0.5085)


# GGH cross section from LHC Higgs XS WG: https://twiki.cern.ch/twiki/bin/view/LHCPhysics/CERNYellowReportPageAt1314TeV?rev=15
GGHZZ4L = kreator.makeMCComponent("GGHZZ4L", "/GluGluHToZZTo4L_M125_13TeV_powheg2_JHUgenV6_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM", "CMS", ".*root", 0.01212) #43.92*2.76E-04)

VHToNonbb = kreator.makeMCComponent("VHToNonbb", "/VHToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root", 0.9561, fracNegWeights=0.26)
ZHTobb_ll = kreator.makeMCComponent("ZHTobb_ll", "/ZH_HToBB_ZToLL_M125_13TeV_powheg_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v1/MINIAODSIM", "CMS", ".*root", 0.05198)
ZHToTauTau = kreator.makeMCComponent("ZHToTauTau", "/ZHToTauTau_M125_13TeV_powheg_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root", 0.05544)

Higgs = [
TTHnobb_pow,
TTHnobb_fxfx,
TTH_ctcvcp,
GGHZZ4L,
VHToNonbb,
ZHTobb_ll,
ZHToTauTau,
]

Higgs += [
#TTHbb,
#TTHbb_ext1,
#TTHbb_ext2,
# NOTAVAILYET # TTHbb_ext3,
]

THQ_ctcvcp_noM125 = kreator.makeMCComponent("THQ_ctcvcp_noM125", "/THQ_ctcvcp_Hincl_13TeV-madgraph-pythia8_TuneCUETP8M1/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root",  0.7927)
THW_ctcvcp_noM125 = kreator.makeMCComponent("THW_ctcvcp_noM125", "/THW_ctcvcp_Hincl_13TeV-madgraph-pythia8_TuneCUETP8M1/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root",  0.1472)
THQ = kreator.makeMCComponent("THQ", "/THQ_Hincl_13TeV-madgraph-pythia8_TuneCUETP8M1/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root", 0.7927)
THW = kreator.makeMCComponent("THW", "/THW_Hincl_13TeV-madgraph-pythia8_TuneCUETP8M1/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root", 0.1472)
THQ_ctcvcp = kreator.makeMCComponent("THQ_ctcvcp", "/THQ_ctcvcp_HIncl_M125_TuneCP5_13TeV-madgraph-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM",  "CMS", ".*root", 0.7927)
THW_ctcvcp = kreator.makeMCComponent("THW_ctcvcp", "/THW_ctcvcp_HIncl_M125_TuneCP5_13TeV-madgraph-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM", "CMS", ".*root", 0.1472)

Higgs += [
THQ_ctcvcp_noM125,
THW_ctcvcp_noM125,
THQ,
THW,
THQ_ctcvcp,
THW_ctcvcp,
]

# Single top cross sections: https://twiki.cern.ch/twiki/bin/viewauth/CMS/SingleTopSigma
T_sch_lep = kreator.makeMCComponent("T_sch_lep", "/ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM", "CMS", ".*root", (7.20+4.16)*0.108*3, fracNegWeights=0.188)
T_sch_lep_PS = kreator.makeMCComponent("T_sch_lep_PS", "/ST_s-channel_4f_leptonDecays_13TeV_PSweights-amcatnlo-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM", "CMS", ".*root", (7.20+4.16)*0.108*3, fracNegWeights=0.188)
T_sch = kreator.makeMCComponent("T_sch", "/ST_s-channel_4f_InclusiveDecays_13TeV-amcatnlo-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM", "CMS", ".*root", (7.20+4.16), fracNegWeights=0.188)

T_tch = kreator.makeMCComponent("T_tch", "/ST_t-channel_top_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM", "CMS", ".*root", 136.02) # inclusive sample
TBar_tch = kreator.makeMCComponent("TBar_tch", "/ST_t-channel_antitop_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM", "CMS", ".*root", 80.95) # inclusive sample
TBar_tch_PS = kreator.makeMCComponent("TBar_tch_PS", "/ST_t-channel_antitop_4f_inclusiveDecays_13TeV_PSweights-powhegV2-madspin/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM", "CMS", ".*root", 80.95) # inclusive sample

T_tWch_noFullyHad      = kreator.makeMCComponent("T_tWch_noFullyHad", "/ST_tW_top_5f_NoFullyHadronicDecays_13TeV-powheg_TuneCUETP8M1/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM", "CMS", ".*root",19.55)
T_tWch_noFullyHad_ext  = kreator.makeMCComponent("T_tWch_noFullyHad_ext", "/ST_tW_top_5f_NoFullyHadronicDecays_13TeV-powheg_TuneCUETP8M1/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM", "CMS", ".*root",19.55)
T_tWch_noFullyHad_ext2 = kreator.makeMCComponent("T_tWch_noFullyHad_ext2", "/ST_tW_top_5f_NoFullyHadronicDecays_13TeV-powheg_TuneCUETP8M1/RunIISummer16MiniAODv3-94X_mcRun2_asymptotic_v3_ext2-v1/MINIAODSIM", "CMS", ".*root",19.55)

TBar_tWch_noFullyHad      = kreator.makeMCComponent("TBar_tWch_noFullyHad"     , "/ST_tW_antitop_5f_NoFullyHadronicDecays_13TeV-powheg_TuneCUETP8M1/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM", "CMS", ".*root",19.55)
TBar_tWch_noFullyHad_ext  = kreator.makeMCComponent("TBar_tWch_noFullyHad_ext" , "/ST_tW_antitop_5f_NoFullyHadronicDecays_13TeV-powheg_TuneCUETP8M1/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM", "CMS", ".*root",19.55)
TBar_tWch_noFullyHad_ext2 = kreator.makeMCComponent("TBar_tWch_noFullyHad_ext2", "/ST_tW_antitop_5f_NoFullyHadronicDecays_13TeV-powheg_TuneCUETP8M1/RunIISummer16MiniAODv3-94X_mcRun2_asymptotic_v3_ext2-v1/MINIAODSIM", "CMS", ".*root",19.55)

T_tWch    = kreator.makeMCComponent("T_tWch", "/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v1/MINIAODSIM", "CMS", ".*root",35.6)
TBar_tWch = kreator.makeMCComponent("TBar_tWch", "/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v1/MINIAODSIM", "CMS", ".*root",35.6)

TGJets_lep = kreator.makeMCComponent("TGJets_lep", "/TGJets_leptonDecays_13TeV_amcatnlo_madspin_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root", 1.018, fracNegWeights=0.411) # leptonic top decays only
TGJets = kreator.makeMCComponent("TGJets", "/TGJets_TuneCUETP8M1_13TeV_amcatnlo_madspin_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root", 2.967, fracNegWeights=0.411)
TZQToLL = kreator.makeMCComponent("TZQToLL", "/tZq_ll_4f_13TeV-amcatnlo-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v1/MINIAODSIM", "CMS", ".*root", 0.0758, fracNegWeights=0.367 )
TZQToLL_PS = kreator.makeMCComponent("TZQToLL_PS", "/tZq_ll_4f_PSweights_13TeV-amcatnlo-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM", "CMS", ".*root", 0.0758, fracNegWeights=0.367 )
tWll = kreator.makeMCComponent("tWll", "/ST_tWll_5f_LO_13TeV-MadGraph-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM", "CMS", ".*root", 0.01123)
tWnunu = kreator.makeMCComponent("tWnunu", "/ST_tWnunu_5f_LO_13TeV-MadGraph-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM", "CMS", ".*root", 0.01123*1.9822 )

SingleTop = [
T_sch_lep,
T_sch_lep_PS,
T_sch,

T_tch,
TBar_tch,
TBar_tch_PS,

T_tWch_noFullyHad,
T_tWch_noFullyHad_ext,
T_tWch_noFullyHad_ext2,
TBar_tWch_noFullyHad,
TBar_tWch_noFullyHad_ext,
TBar_tWch_noFullyHad_ext2,

T_tWch,
TBar_tWch,

TGJets_lep,
TGJets,
TZQToLL,
TZQToLL_PS,
tWll,
tWnunu
]

### V+jets inclusive (from https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat13TeV)
WJetsToLNu = kreator.makeMCComponent("WJetsToLNu","/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM", "CMS", ".*root", 3* 20508.9, fracNegWeights=0.16)
WJetsToLNu_ext = kreator.makeMCComponent("WJetsToLNu_ext","/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext2-v1/MINIAODSIM", "CMS", ".*root", 3* 20508.9, fracNegWeights=0.16)
WJetsToLNu_LO = kreator.makeMCComponent("WJetsToLNu_LO","/WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root", 3* 20508.9)
WJetsToLNu_LO_ext =  kreator.makeMCComponent("WJetsToLNu_LO_ext", "/WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext2-v2/MINIAODSIM", "CMS", ".*root", 61526.7)

DYJetsToLL_M10to50 = kreator.makeMCComponent("DYJetsToLL_M10to50", "/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root", 18610, fracNegWeights=0.135)
DYJetsToLL_M10to50_ext = kreator.makeMCComponent("DYJetsToLL_M10to50_ext", "/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM", "CMS", ".*root", 18610, fracNegWeights=0.135)
DYJetsToLL_M10to50_LO = kreator.makeMCComponent("DYJetsToLL_M10to50_LO", "/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root", 18610)
DYJetsToLL_M50 = kreator.makeMCComponent("DYJetsToLL_M50", "/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext2-v1/MINIAODSIM", "CMS", ".*root", 2008.*3, fracNegWeights=0.16)
DYJetsToLL_M50_LO =  kreator.makeMCComponent("DYJetsToLL_M50_LO", "/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM", "CMS", ".*root", 2008.*3)
DYJetsToLL_M50_LO_ext =  kreator.makeMCComponent("DYJetsToLL_M50_LO_ext", "/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext2-v2/MINIAODSIM", "CMS", ".*root", 2008.*3)


VJets = [
WJetsToLNu,
WJetsToLNu_ext,
WJetsToLNu_LO,
WJetsToLNu_LO_ext,
DYJetsToLL_M10to50,
DYJetsToLL_M10to50_ext,
DYJetsToLL_M10to50_LO,
DYJetsToLL_M50,
DYJetsToLL_M50_LO,
DYJetsToLL_M50_LO_ext,
]

# DY njet bins
DY1JetsToLL_M50_LO =  kreator.makeMCComponent("DY1JetsToLL_M50_LO", "/DY1JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM", "CMS", ".*root", 1012.5)
DY2JetsToLL_M50_LO =  kreator.makeMCComponent("DY2JetsToLL_M50_LO", "/DY2JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root", 332.8)
DY3JetsToLL_M50_LO =  kreator.makeMCComponent("DY3JetsToLL_M50_LO", "/DY3JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root", 101.8)
DY4JetsToLL_M50_LO =  kreator.makeMCComponent("DY4JetsToLL_M50_LO", "/DY4JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root", 54.8)

DYNJets = [ 
DY1JetsToLL_M50_LO,
DY2JetsToLL_M50_LO,
DY3JetsToLL_M50_LO,
DY4JetsToLL_M50_LO,
]

# W njet bins
W1JetsToLNu_LO =  kreator.makeMCComponent("W1JetsToLNu_LO", "/W1JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM", "CMS", ".*root", 9644.5)
W2JetsToLNu_LO =  kreator.makeMCComponent("W2JetsToLNu_LO", "/W2JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM", "CMS", ".*root", 3144.5)
W3JetsToLNu_LO =  kreator.makeMCComponent("W3JetsToLNu_LO", "/W3JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM", "CMS", ".*root", 954.8)
W4JetsToLNu_LO =  kreator.makeMCComponent("W4JetsToLNu_LO", "/W4JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root", 485.6)
W4JetsToLNu_LO_ext =  kreator.makeMCComponent("W4JetsToLNu_LO_ext", "/W4JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM", "CMS", ".*root", 485.6)
W4JetsToLNu_LO_ext2 =  kreator.makeMCComponent("W4JetsToLNu_LO_ext2", "/W4JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext2-v1/MINIAODSIM", "CMS", ".*root", 485.6)


WNJets = [
W1JetsToLNu_LO,
W2JetsToLNu_LO,
W3JetsToLNu_LO,
W4JetsToLNu_LO,
W4JetsToLNu_LO_ext,
W4JetsToLNu_LO_ext2
]

# DY HT bins:
#https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns#DY_Z

DYJetsToLL_M50_HT70to100      =   kreator.makeMCComponent("DYJetsToLL_M50_HT70to100"    , '/DYJetsToLL_M-50_HT-70to100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM'        ,    "CMS", ".*root", 170.4 *1.23)
DYJetsToLL_M50_HT100to200     =   kreator.makeMCComponent("DYJetsToLL_M50_HT100to200", "/DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM"             , "CMS", ".*root", 147.4*1.23)
DYJetsToLL_M50_HT100to200_ext =   kreator.makeMCComponent("DYJetsToLL_M50_HT100to200_ext", "/DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM",     "CMS", ".*root", 147.4*1.23)
DYJetsToLL_M50_HT200to400     =   kreator.makeMCComponent("DYJetsToLL_M50_HT200to400", "/DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM"             , "CMS", ".*root",40.99*1.23)
DYJetsToLL_M50_HT200to400_ext =   kreator.makeMCComponent("DYJetsToLL_M50_HT200to400_ext", "/DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM"    , "CMS", ".*root",40.99*1.23)
DYJetsToLL_M50_HT400to600     =   kreator.makeMCComponent("DYJetsToLL_M50_HT400to600", "/DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM"             , "CMS", ".*root",5.678*1.23)
DYJetsToLL_M50_HT400to600_ext =   kreator.makeMCComponent("DYJetsToLL_M50_HT400to600_ext", "/DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM"    , "CMS", ".*root",5.678*1.23)
DYJetsToLL_M50_HT600to800     =   kreator.makeMCComponent("DYJetsToLL_M50_HT600to800"   , '/DYJetsToLL_M-50_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM',           "CMS", ".*root", 1.367*1.23 )
DYJetsToLL_M50_HT800to1200    =   kreator.makeMCComponent("DYJetsToLL_M50_HT800to1200"  , '/DYJetsToLL_M-50_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM',          "CMS", ".*root", 0.6304*1.23 )
DYJetsToLL_M50_HT1200to2500   =   kreator.makeMCComponent("DYJetsToLL_M50_HT1200to2500" , '/DYJetsToLL_M-50_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM',         "CMS", ".*root", 0.1514*1.23 )
DYJetsToLL_M50_HT2500toInf    =   kreator.makeMCComponent("DYJetsToLL_M50_HT2500toInf"  , '/DYJetsToLL_M-50_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM',          "CMS", ".*root", 0.003565*1.23 )


DYJetsM50HT = [
DYJetsToLL_M50_HT70to100   , 
DYJetsToLL_M50_HT100to200,
DYJetsToLL_M50_HT100to200_ext,
DYJetsToLL_M50_HT200to400,
DYJetsToLL_M50_HT200to400_ext,
DYJetsToLL_M50_HT400to600,
DYJetsToLL_M50_HT400to600_ext,
DYJetsToLL_M50_HT600to800  ,
DYJetsToLL_M50_HT800to1200 ,
DYJetsToLL_M50_HT1200to2500,
DYJetsToLL_M50_HT2500toInf ,

]



DYJetsToLL_M5to50_HT100to200     = kreator.makeMCComponent("DYJetsToLL_M5to50_HT100to200"    , "/DYJetsToLL_M-5to50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root", 224.2) #LO
DYJetsToLL_M5to50_HT100to200_ext = kreator.makeMCComponent("DYJetsToLL_M5to50_HT100to200_ext", "/DYJetsToLL_M-5to50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM", "CMS", ".*root", 224.2) #LO
DYJetsToLL_M5to50_HT200to400     = kreator.makeMCComponent("DYJetsToLL_M5to50_HT200to400"    , "/DYJetsToLL_M-5to50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root", 37.2) #LO
DYJetsToLL_M5to50_HT200to400_ext = kreator.makeMCComponent("DYJetsToLL_M5to50_HT200to400_ext", "/DYJetsToLL_M-5to50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM", "CMS", ".*root", 37.2) #LO
DYJetsToLL_M5to50_HT400to600     = kreator.makeMCComponent("DYJetsToLL_M5to50_HT400to600"    , "/DYJetsToLL_M-5to50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root", 3.581) #LO
DYJetsToLL_M5to50_HT400to600_ext = kreator.makeMCComponent("DYJetsToLL_M5to50_HT400to600_ext", "/DYJetsToLL_M-5to50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM", "CMS", ".*root", 3.581)
DYJetsToLL_M5to50_HT600toInf     = kreator.makeMCComponent("DYJetsToLL_M5to50_HT600toInf"    , "/DYJetsToLL_M-5to50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root", 1.124) #LO
DYJetsToLL_M5to50_HT600toInf_ext = kreator.makeMCComponent("DYJetsToLL_M5to50_HT600toInf_ext", "/DYJetsToLL_M-5to50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM", "CMS", ".*root", 1.124) #LO

DYJetsM5to50HT = [
DYJetsToLL_M5to50_HT100to200,
DYJetsToLL_M5to50_HT100to200_ext,
DYJetsToLL_M5to50_HT200to400,
DYJetsToLL_M5to50_HT200to400_ext,
DYJetsToLL_M5to50_HT400to600,
DYJetsToLL_M5to50_HT400to600_ext,
DYJetsToLL_M5to50_HT600toInf,
DYJetsToLL_M5to50_HT600toInf_ext
]

### W+jets
WJetsToLNu_HT70to100 = kreator.makeMCComponent("WJetsToLNu_HT70to100", "/WJetsToLNu_HT-70To100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root",1319*1.21)
WJetsToLNu_HT100to200 = kreator.makeMCComponent("WJetsToLNu_HT100to200", "/WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root",1345*1.21)
WJetsToLNu_HT100to200_ext = kreator.makeMCComponent("WJetsToLNu_HT100to200_ext", "/WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM", "CMS", ".*root",1345*1.21)
WJetsToLNu_HT100to200_ext2 = kreator.makeMCComponent("WJetsToLNu_HT100to200_ext2", "/WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext2-v2/MINIAODSIM", "CMS", ".*root",1345*1.21)
WJetsToLNu_HT200to400 = kreator.makeMCComponent("WJetsToLNu_HT200to400", "/WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root",359.7*1.21)
WJetsToLNu_HT200to400_ext = kreator.makeMCComponent("WJetsToLNu_HT200to400_ext", "/WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM", "CMS", ".*root",359.7*1.21)
WJetsToLNu_HT200to400_ext2 = kreator.makeMCComponent("WJetsToLNu_HT200to400_ext2", '/WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext2-v2/MINIAODSIM' , "CMS", ".*root",359.7*1.21)
WJetsToLNu_HT400to600      = kreator.makeMCComponent("WJetsToLNu_HT400to600", "/WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root",48.91*1.21)
WJetsToLNu_HT400to600_ext  = kreator.makeMCComponent("WJetsToLNu_HT400to600_ext", "/WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM", "CMS", ".*root",48.91*1.21)
WJetsToLNu_HT600to800      = kreator.makeMCComponent("WJetsToLNu_HT600to800",     "/WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root",12.05*1.21)
WJetsToLNu_HT600to800_ext  = kreator.makeMCComponent("WJetsToLNu_HT600to800_ext", '/WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM', "CMS", ".*root",12.05*1.21)
WJetsToLNu_HT800to1200     = kreator.makeMCComponent("WJetsToLNu_HT800to1200",    "/WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root",5.501*1.21)
WJetsToLNu_HT800to1200_ext = kreator.makeMCComponent("WJetsToLNu_HT800to1200_ext","/WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM", "CMS", ".*root",5.501*1.21)
WJetsToLNu_HT1200to2500    = kreator.makeMCComponent("WJetsToLNu_HT1200to2500",   "/WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root",1.329*1.21)
WJetsToLNu_HT1200to2500_ext = kreator.makeMCComponent("WJetsToLNu_HT1200to2500_ext", "/WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM", "CMS", ".*root",1.329*1.21)
WJetsToLNu_HT2500toInf = kreator.makeMCComponent("WJetsToLNu_HT2500toInf", "/WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root",0.03216*1.21)
WJetsToLNu_HT2500toInf_ext = kreator.makeMCComponent("WJetsToLNu_HT2500toInf_ext", "/WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM", "CMS", ".*root",0.03216*1.21)

WJetsToLNuHT = [
WJetsToLNu_HT70to100,
WJetsToLNu_HT100to200,
WJetsToLNu_HT100to200_ext,
WJetsToLNu_HT100to200_ext2,
WJetsToLNu_HT200to400,
WJetsToLNu_HT200to400_ext,
WJetsToLNu_HT200to400_ext2,
WJetsToLNu_HT400to600,
WJetsToLNu_HT400to600_ext,
WJetsToLNu_HT600to800,
WJetsToLNu_HT600to800_ext,
WJetsToLNu_HT800to1200,
WJetsToLNu_HT800to1200_ext,
WJetsToLNu_HT1200to2500,
WJetsToLNu_HT1200to2500_ext,
WJetsToLNu_HT2500toInf,
WJetsToLNu_HT2500toInf_ext
]

# W+Jets NLO in Pt bins, cross sections are determined from GenXSecAnalyzer running over 10 files each
WJetsToLNu_Pt_100To250 = kreator.makeMCComponent("WJetsToLNu_Pt_100To250", "/WJetsToLNu_Pt-100To250_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root", 625.6, fracNegWeights=0.31)
WJetsToLNu_Pt_100To250_ext1 = kreator.makeMCComponent("WJetsToLNu_Pt_100To250_ext1", "/WJetsToLNu_Pt-100To250_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM", "CMS", ".*root", 625.6, fracNegWeights=0.31)
WJetsToLNu_Pt_100To250_ext4 = kreator.makeMCComponent("WJetsToLNu_Pt_100To250_ext4", "/WJetsToLNu_Pt-100To250_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext4-v2/MINIAODSIM", "CMS", ".*root", 625.6, fracNegWeights=0.31)
WJetsToLNu_Pt_250To400 = kreator.makeMCComponent("WJetsToLNu_Pt_250To400", "/WJetsToLNu_Pt-250To400_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root", 21.82, fracNegWeights=0.31)
WJetsToLNu_Pt_250To400_ext1 = kreator.makeMCComponent("WJetsToLNu_Pt_250To400_ext1", "/WJetsToLNu_Pt-250To400_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v1/MINIAODSIM", "CMS", ".*root", 21.82, fracNegWeights=0.31)
WJetsToLNu_Pt_250To400_ext4 = kreator.makeMCComponent("WJetsToLNu_Pt_250To400_ext4", "/WJetsToLNu_Pt-250To400_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext4-v2/MINIAODSIM", "CMS", ".*root", 21.82, fracNegWeights=0.31)
WJetsToLNu_Pt_400To600 = kreator.makeMCComponent("WJetsToLNu_Pt_400To600", "/WJetsToLNu_Pt-400To600_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root", 2.640, fracNegWeights=0.31)
WJetsToLNu_Pt_400To600_ext1 = kreator.makeMCComponent("WJetsToLNu_Pt_400To600_ext1", "/WJetsToLNu_Pt-400To600_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM", "CMS", ".*root", 2.640, fracNegWeights=0.31)
WJetsToLNu_Pt_600ToInf = kreator.makeMCComponent("WJetsToLNu_Pt_600ToInf", "/WJetsToLNu_Pt-600ToInf_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root", 0.4118, fracNegWeights=0.31)
WJetsToLNu_Pt_600ToInf_ext1 = kreator.makeMCComponent("WJetsToLNu_Pt_600ToInf_ext1", "/WJetsToLNu_Pt-600ToInf_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM", "CMS", ".*root", 0.4118, fracNegWeights=0.31)

WJetsToLNuPT = [
WJetsToLNu_Pt_100To250,
WJetsToLNu_Pt_100To250_ext1,
WJetsToLNu_Pt_100To250_ext4,
WJetsToLNu_Pt_250To400,
WJetsToLNu_Pt_250To400_ext1,
WJetsToLNu_Pt_250To400_ext4,
WJetsToLNu_Pt_400To600,
WJetsToLNu_Pt_400To600_ext1,
WJetsToLNu_Pt_600ToInf,
WJetsToLNu_Pt_600ToInf_ext1
]

### GJets (cross sections from McM)
GJets_HT40to100      = kreator.makeMCComponent("GJets_HT40to100"    , "/GJets_HT-40To100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root",20730)
GJets_HT40to100_ext  = kreator.makeMCComponent("GJets_HT40to100_ext", "/GJets_HT-40To100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM",  "CMS", ".*root",20730)
GJets_HT100to200     = kreator.makeMCComponent("GJets_HT100to200",    "/GJets_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root",9226)
GJets_HT100to200_ext = kreator.makeMCComponent("GJets_HT100to200_ext","/GJets_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM", "CMS", ".*root",9226)
GJets_HT200to400     = kreator.makeMCComponent("GJets_HT200to400",    "/GJets_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root",2300)
GJets_HT200to400_ext = kreator.makeMCComponent("GJets_HT200to400_ext","/GJets_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM", "CMS", ".*root",2300)
GJets_HT400to600     = kreator.makeMCComponent("GJets_HT400to600"    , "/GJets_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root",274.4)
GJets_HT400to600_ext = kreator.makeMCComponent("GJets_HT400to600_ext", "/GJets_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM",  "CMS", ".*root",274.4)
GJets_HT600toInf     = kreator.makeMCComponent("GJets_HT600toInf"    , "/GJets_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root",93.38)
GJets_HT600toInf_ext = kreator.makeMCComponent("GJets_HT600toInf_ext", "/GJets_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM",  "CMS", ".*root",93.38)

GJetsHT = [
GJets_HT40to100,
GJets_HT40to100_ext,
GJets_HT100to200,
GJets_HT100to200_ext,
GJets_HT200to400,
GJets_HT200to400_ext,
GJets_HT400to600,
GJets_HT400to600_ext,
GJets_HT600toInf,
GJets_HT600toInf_ext,
]


VJetsQQHT=[
]

### Zinv
ZJetsToNuNu_HT100to200 = kreator.makeMCComponent("ZJetsToNuNu_HT100to200", "/ZJetsToNuNu_HT-100To200_13TeV-madgraph/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root",280.47*1.23)
ZJetsToNuNu_HT100to200_ext = kreator.makeMCComponent("ZJetsToNuNu_HT100to200_ext", "/ZJetsToNuNu_HT-100To200_13TeV-madgraph/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM", "CMS", ".*root",280.47*1.23)
ZJetsToNuNu_HT200to400 = kreator.makeMCComponent("ZJetsToNuNu_HT200to400", "/ZJetsToNuNu_HT-200To400_13TeV-madgraph/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root",78.36*1.23) 
ZJetsToNuNu_HT200to400_ext = kreator.makeMCComponent("ZJetsToNuNu_HT200to400_ext", "/ZJetsToNuNu_HT-200To400_13TeV-madgraph/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM", "CMS", ".*root",78.36*1.23)
ZJetsToNuNu_HT400to600 = kreator.makeMCComponent("ZJetsToNuNu_HT400to600", "/ZJetsToNuNu_HT-400To600_13TeV-madgraph/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root",10.94*1.23) 
ZJetsToNuNu_HT400to600_ext = kreator.makeMCComponent("ZJetsToNuNu_HT400to600_ext", "/ZJetsToNuNu_HT-400To600_13TeV-madgraph/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM", "CMS", ".*root",10.94*1.23)
ZJetsToNuNu_HT600to800 = kreator.makeMCComponent("ZJetsToNuNu_HT600to800", "/ZJetsToNuNu_HT-600To800_13TeV-madgraph/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM", "CMS", ".*root",3.221*1.23)
ZJetsToNuNu_HT800to1200 = kreator.makeMCComponent("ZJetsToNuNu_HT800to1200", "/ZJetsToNuNu_HT-800To1200_13TeV-madgraph/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM", "CMS", ".*root",1.474*1.23)   # FIXME
ZJetsToNuNu_HT1200to2500 = kreator.makeMCComponent("ZJetsToNuNu_HT1200to2500", "/ZJetsToNuNu_HT-1200To2500_13TeV-madgraph/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM", "CMS", ".*root",0.3586*1.23 )
ZJetsToNuNu_HT1200to2500_ext = kreator.makeMCComponent("ZJetsToNuNu_HT1200to2500_ext", "/ZJetsToNuNu_HT-1200To2500_13TeV-madgraph/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v1/MINIAODSIM", "CMS", ".*root",0.3586*1.23 )
ZJetsToNuNu_HT2500toInf = kreator.makeMCComponent("ZJetsToNuNu_HT2500toInf", "/ZJetsToNuNu_HT-2500ToInf_13TeV-madgraph/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root",0.008203*1.23)

ZJetsToNuNuHT = [
ZJetsToNuNu_HT100to200,
ZJetsToNuNu_HT100to200_ext,
ZJetsToNuNu_HT200to400,
ZJetsToNuNu_HT200to400_ext,
ZJetsToNuNu_HT400to600,
ZJetsToNuNu_HT400to600_ext,
ZJetsToNuNu_HT600to800,
ZJetsToNuNu_HT800to1200,
ZJetsToNuNu_HT1200to2500,
ZJetsToNuNu_HT1200to2500_ext,
ZJetsToNuNu_HT2500toInf,
]

### QCD

### missing xsec 
QCD_Pt15to30          = kreator.makeMCComponent("QCD_Pt15to30"         , "/QCD_Pt_15to30_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM"     , "CMS" , ".*root" , 1837410000)
QCD_Pt30to50          = kreator.makeMCComponent("QCD_Pt30to50"         , "/QCD_Pt_30to50_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM"      , "CMS" , ".*root" , 140932000)
QCD_Pt50to80          = kreator.makeMCComponent("QCD_Pt50to80"         , "/QCD_Pt_50to80_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root", 19204300)
QCD_Pt80to120         = kreator.makeMCComponent("QCD_Pt80to120"        , "/QCD_Pt_80to120_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM", "CMS", ".*root", 2762530)
QCD_Pt80to120_ext     = kreator.makeMCComponent("QCD_Pt80to120_ext"    , "/QCD_Pt_80to120_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext2-v2/MINIAODSIM", "CMS", ".*root", 2762530)
QCD_Pt120to170        = kreator.makeMCComponent("QCD_Pt120to170"       , "/QCD_Pt_120to170_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM"   , "CMS" , ".*root" , 471100)
QCD_Pt120to170_ext    = kreator.makeMCComponent("QCD_Pt120to170_ext"   , "/QCD_Pt_120to170_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM",    "CMS" , ".*root" , 471100)
QCD_Pt170to300        = kreator.makeMCComponent("QCD_Pt170to300"       , "/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM"   , "CMS" , ".*root" , 117276)
QCD_Pt170to300_ext    = kreator.makeMCComponent("QCD_Pt170to300_ext"   , "/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM"   , "CMS" , ".*root" , 117276)
QCD_Pt300to470        = kreator.makeMCComponent("QCD_Pt300to470"       , "/QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root", 7823)
QCD_Pt300to470_ext    = kreator.makeMCComponent("QCD_Pt300to470_ext"   , "/QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM", "CMS", ".*root", 7823)
QCD_Pt470to600        = kreator.makeMCComponent("QCD_Pt470to600"       , "/QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root", 648.2)
QCD_Pt600to800        = kreator.makeMCComponent("QCD_Pt600to800"       , "/QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM"   , "CMS" , ".*root" , 186.9)
QCD_Pt600to800_ext    = kreator.makeMCComponent("QCD_Pt600to800_ext"   , "/QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM"   , "CMS" , ".*root" , 186.9)
QCD_Pt800to1000       = kreator.makeMCComponent("QCD_Pt800to1000"      , "/QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM"  , "CMS" , ".*root" , 32.293)
QCD_Pt800to1000_ext   = kreator.makeMCComponent("QCD_Pt800to1000_ext"  , "/QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM"  , "CMS" , ".*root" , 32.293)
QCD_Pt1000to1400      = kreator.makeMCComponent("QCD_Pt1000to1400"     , "/QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM" , "CMS" , ".*root" , 9.4183)
QCD_Pt1000to1400_ext  = kreator.makeMCComponent("QCD_Pt1000to1400_ext" , "/QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM" , "CMS" , ".*root" , 9.4183)
QCD_Pt1400to1800      = kreator.makeMCComponent("QCD_Pt1400to1800"     , "/QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM" , "CMS" , ".*root" , 0.84265)
QCD_Pt1400to1800_ext  = kreator.makeMCComponent("QCD_Pt1400to1800_ext" , "/QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM" , "CMS" , ".*root" , 0.84265)
QCD_Pt1800to2400      = kreator.makeMCComponent("QCD_Pt1800to2400"     , "/QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM" , "CMS" , ".*root" , 0.114943)
QCD_Pt1800to2400_ext  = kreator.makeMCComponent("QCD_Pt1800to2400_ext" , "/QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM" , "CMS" , ".*root" , 0.114943)
QCD_Pt2400to3200      = kreator.makeMCComponent("QCD_Pt2400to3200"     , "/QCD_Pt_2400to3200_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM" , "CMS" , ".*root" , 0.00682981)
QCD_Pt2400to3200_ext  = kreator.makeMCComponent("QCD_Pt2400to3200_ext" , "/QCD_Pt_2400to3200_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM" , "CMS" , ".*root" , 0.00682981)
QCD_Pt3200toInf       = kreator.makeMCComponent("QCD_Pt3200toInf"      , "/QCD_Pt_3200toInf_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM"  , "CMS" , ".*root" , 0.000165445)

QCDPt = [
QCD_Pt15to30,
QCD_Pt30to50,
QCD_Pt50to80,
QCD_Pt80to120, QCD_Pt80to120_ext,
QCD_Pt120to170, QCD_Pt120to170_ext,
QCD_Pt170to300, QCD_Pt170to300_ext,
QCD_Pt300to470, QCD_Pt300to470_ext,
QCD_Pt470to600,
QCD_Pt600to800, QCD_Pt600to800_ext,
QCD_Pt800to1000, QCD_Pt800to1000_ext,
QCD_Pt1000to1400, QCD_Pt1000to1400_ext,
QCD_Pt1400to1800, QCD_Pt1400to1800_ext,
QCD_Pt1800to2400, QCD_Pt1800to2400_ext,
QCD_Pt2400to3200, QCD_Pt2400to3200_ext,
QCD_Pt3200toInf
]



# qcd muenr
QCD_Mu15 = kreator.makeMCComponent("QCD_Mu15", "/QCD_Pt-20toInf_MuEnrichedPt15_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root", 720.65e6*0.00042)
QCD_Pt15to20_Mu5    = kreator.makeMCComponent("QCD_Pt15to20_Mu5"    , "/QCD_Pt-15to20_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM"       , "CMS" , ".*root" , 1273190000*0.003)
QCD_Pt20to30_Mu5    = kreator.makeMCComponent("QCD_Pt20to30_Mu5"    , "/QCD_Pt-20to30_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM"      , "CMS" , ".*root" , 558528000*0.0053)
QCD_Pt30to50_Mu5    = kreator.makeMCComponent("QCD_Pt30to50_Mu5", "/QCD_Pt-30to50_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root", 139803000*0.01182)
QCD_Pt50to80_Mu5    = kreator.makeMCComponent("QCD_Pt50to80_Mu5"    , "/QCD_Pt-50to80_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM" , "CMS" , ".*root" , 19222500*0.02276)
QCD_Pt80to120_Mu5   = kreator.makeMCComponent("QCD_Pt80to120_Mu5"   , "/QCD_Pt-80to120_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM"     , "CMS" , ".*root" , 2758420*0.03844)
QCD_Pt80to120_Mu5_ext   = kreator.makeMCComponent("QCD_Pt80to120_Mu5_ext"   , "/QCD_Pt-80to120_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM"     , "CMS" , ".*root" , 2758420*0.03844)
QCD_Pt120to170_Mu5  = kreator.makeMCComponent("QCD_Pt120to170_Mu5"  , "/QCD_Pt-120to170_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS" , ".*root" , 469797*0.05362)
QCD_Pt170to300_Mu5  = kreator.makeMCComponent("QCD_Pt170to300_Mu5", "/QCD_Pt-170to300_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM", "CMS", ".*root", 117989*0.07335)
QCD_Pt170to300_Mu5_ext  = kreator.makeMCComponent("QCD_Pt170to300_Mu5_ext", "/QCD_Pt-170to300_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM", "CMS", ".*root", 117989*0.07335)
QCD_Pt300to470_Mu5  = kreator.makeMCComponent("QCD_Pt300to470_Mu5"  , "/QCD_Pt-300to470_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM"    , "CMS" , ".*root" , 7820.25*0.10196)
QCD_Pt300to470_Mu5_ext  = kreator.makeMCComponent("QCD_Pt300to470_Mu5_ext"  , "/QCD_Pt-300to470_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v1/MINIAODSIM"    , "CMS" , ".*root" , 7820.25*0.10196)
QCD_Pt300to470_Mu5_ext2  = kreator.makeMCComponent("QCD_Pt300to470_Mu5_ext2"  , "/QCD_Pt-300to470_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext2-v2/MINIAODSIM"    , "CMS" , ".*root" , 7820.25*0.10196)
QCD_Pt470to600_Mu5  = kreator.makeMCComponent("QCD_Pt470to600_Mu5"  , "/QCD_Pt-470to600_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM"    , "CMS" , ".*root" , 645.528*0.12242)
QCD_Pt470to600_Mu5_ext  = kreator.makeMCComponent("QCD_Pt470to600_Mu5_ext"  , "/QCD_Pt-470to600_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM"    , "CMS" , ".*root" , 645.528*0.12242)
QCD_Pt470to600_Mu5_ext2  = kreator.makeMCComponent("QCD_Pt470to600_Mu5_ext2"  , "/QCD_Pt-470to600_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext2-v2/MINIAODSIM"    , "CMS" , ".*root" , 645.528*0.12242)
QCD_Pt600to800_Mu5  = kreator.makeMCComponent("QCD_Pt600to800_Mu5", "/QCD_Pt-600to800_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root", 187.109*0.13412)
QCD_Pt600to800_Mu5_ext  = kreator.makeMCComponent("QCD_Pt600to800_Mu5_ext", "/QCD_Pt-600to800_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM", "CMS", ".*root", 187.109*0.13412)
QCD_Pt800to1000_Mu5 = kreator.makeMCComponent("QCD_Pt800to1000_Mu5" , "/QCD_Pt-800to1000_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM"   , "CMS" , ".*root" , 32.3486*0.14552)
QCD_Pt800to1000_Mu5_ext = kreator.makeMCComponent("QCD_Pt800to1000_Mu5_ext" , "/QCD_Pt-800to1000_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM"   , "CMS" , ".*root" , 32.3486*0.14552)
QCD_Pt800to1000_Mu5_ext2 = kreator.makeMCComponent("QCD_Pt800to1000_Mu5_ext2" , "/QCD_Pt-800to1000_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext2-v2/MINIAODSIM"   , "CMS" , ".*root" , 32.3486*0.14552)
QCD_Pt1000toInf_Mu5 = kreator.makeMCComponent("QCD_Pt1000toInf_Mu5" , "/QCD_Pt-1000toInf_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM"   , "CMS" , ".*root" , 10.4305*0.15544)
QCD_Pt1000toInf_Mu5_ext = kreator.makeMCComponent("QCD_Pt1000toInf_Mu5_ext" , "/QCD_Pt-1000toInf_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM"   , "CMS" , ".*root" , 10.4305*0.15544)

QCD_Mu5 = [
QCD_Pt15to20_Mu5,
QCD_Pt20to30_Mu5,
QCD_Pt30to50_Mu5,
QCD_Pt50to80_Mu5,
QCD_Pt80to120_Mu5,
QCD_Pt80to120_Mu5_ext,
QCD_Pt120to170_Mu5,
QCD_Pt170to300_Mu5,
QCD_Pt170to300_Mu5_ext,
QCD_Pt300to470_Mu5,
QCD_Pt300to470_Mu5_ext,
QCD_Pt300to470_Mu5_ext2,
QCD_Pt470to600_Mu5,
QCD_Pt470to600_Mu5_ext,
QCD_Pt470to600_Mu5_ext2,
QCD_Pt600to800_Mu5,
QCD_Pt600to800_Mu5_ext,
QCD_Pt800to1000_Mu5,
QCD_Pt800to1000_Mu5_ext,
QCD_Pt800to1000_Mu5_ext2,
QCD_Pt1000toInf_Mu5,
QCD_Pt1000toInf_Mu5_ext,
]



# qcd emenr
##QCD_Pt15to20_EMEnriched   = kreator.makeMCComponent("QCD_Pt15to20_EMEnriched"  ,"/QCD_Pt-15to20_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM"  , "CMS", ".*root", 1273000000*0.0002)
QCD_Pt20to30_EMEnriched   = kreator.makeMCComponent("QCD_Pt20to30_EMEnriched"  ,"/QCD_Pt-20to30_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM"  , "CMS", ".*root", 557600000*0.0096)
QCD_Pt30to50_EMEnriched     = kreator.makeMCComponent("QCD_Pt30to50_EMEnriched"  ,"/QCD_Pt-30to50_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM"  , "CMS", ".*root", 136000000*0.073)
QCD_Pt30to50_EMEnriched_ext = kreator.makeMCComponent("QCD_Pt30to50_EMEnriched_ext"  ,"/QCD_Pt-30to50_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM"  , "CMS", ".*root", 136000000*0.073)
QCD_Pt50to80_EMEnriched     = kreator.makeMCComponent("QCD_Pt50to80_EMEnriched", "/QCD_Pt-50to80_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root", 19800000*0.146)
QCD_Pt50to80_EMEnriched_ext = kreator.makeMCComponent("QCD_Pt50to80_EMEnriched_ext", "/QCD_Pt-50to80_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM", "CMS", ".*root", 19800000*0.146)
QCD_Pt80to120_EMEnriched     = kreator.makeMCComponent("QCD_Pt80to120_EMEnriched" ,"/QCD_Pt-80to120_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM" , "CMS", ".*root", 2800000*0.125)
QCD_Pt80to120_EMEnriched_ext = kreator.makeMCComponent("QCD_Pt80to120_EMEnriched_ext" ,"/QCD_Pt-80to120_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM" , "CMS", ".*root", 2800000*0.125)
QCD_Pt120to170_EMEnriched     = kreator.makeMCComponent("QCD_Pt120to170_EMEnriched","/QCD_Pt-120to170_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root", 477000*0.132)
QCD_Pt120to170_EMEnriched_ext = kreator.makeMCComponent("QCD_Pt120to170_EMEnriched_ext","/QCD_Pt-120to170_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM", "CMS", ".*root", 477000*0.132)
QCD_Pt170to300_EMEnriched = kreator.makeMCComponent("QCD_Pt170to300_EMEnriched","/QCD_Pt-170to300_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root", 114000*0.165)
QCD_Pt300toInf_EMEnriched = kreator.makeMCComponent("QCD_Pt300toInf_EMEnriched","/QCD_Pt-300toInf_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root", 9000*0.15)

QCDPtEMEnriched = [
#QCD_Pt15to20_EMEnriched,
QCD_Pt20to30_EMEnriched,
QCD_Pt30to50_EMEnriched, QCD_Pt30to50_EMEnriched_ext,
QCD_Pt50to80_EMEnriched, QCD_Pt50to80_EMEnriched_ext,
QCD_Pt80to120_EMEnriched, QCD_Pt80to120_EMEnriched_ext,
QCD_Pt120to170_EMEnriched, QCD_Pt120to170_EMEnriched_ext,
QCD_Pt170to300_EMEnriched,
QCD_Pt300toInf_EMEnriched
]

# qcd bctoe

QCD_Pt15to20_bcToE   = kreator.makeMCComponent("QCD_Pt15to20_bcToE"   , "/QCD_Pt_15to20_bcToE_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM"  , "CMS" , ".*root" , 1272980000*0.0002)
QCD_Pt20to30_bcToE   = kreator.makeMCComponent("QCD_Pt20to30_bcToE"   , "/QCD_Pt_20to30_bcToE_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM"  , "CMS" , ".*root" , 557627000*0.00059)
QCD_Pt30to80_bcToE   = kreator.makeMCComponent("QCD_Pt30to80_bcToE"   , "/QCD_Pt_30to80_bcToE_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM"  , "CMS" , ".*root" , 159068000*0.00255)
QCD_Pt80to170_bcToE  = kreator.makeMCComponent("QCD_Pt80to170_bcToE"  , "/QCD_Pt_80to170_bcToE_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv3-PUMoriond17_backup_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM" , "CMS" , ".*root" , 3221000*0.01183)
QCD_Pt170to250_bcToE = kreator.makeMCComponent("QCD_Pt170to250_bcToE" , "/QCD_Pt_170to250_bcToE_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root", 105771*0.02492)
QCD_Pt250toInf_bcToE = kreator.makeMCComponent("QCD_Pt250toInf_bcToE" , "/QCD_Pt_250toInf_bcToE_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS" , ".*root" , 21094.1*0.03375)

QCDPtbcToE = [
QCD_Pt15to20_bcToE,
QCD_Pt20to30_bcToE,
QCD_Pt30to80_bcToE,
QCD_Pt80to170_bcToE,
QCD_Pt170to250_bcToE,
QCD_Pt250toInf_bcToE
]

# QCD HT bins (cross sections from McM)
QCD_HT100to200 = kreator.makeMCComponent("QCD_HT100to200", "/QCD_HT100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM", "CMS", ".*root", 2.785*10**7)
QCD_HT200to300 = kreator.makeMCComponent("QCD_HT200to300", "/QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root",1717000)
QCD_HT200to300_ext = kreator.makeMCComponent("QCD_HT200to300_ext", "/QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM", "CMS", ".*root",1717000)
QCD_HT300to500 = kreator.makeMCComponent("QCD_HT300to500", "/QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root",351300)
QCD_HT300to500_ext = kreator.makeMCComponent("QCD_HT300to500_ext", "/QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM", "CMS", ".*root",351300)
QCD_HT500to700 = kreator.makeMCComponent("QCD_HT500to700", "/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root",31630)
QCD_HT500to700_ext = kreator.makeMCComponent("QCD_HT500to700_ext", "/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM", "CMS", ".*root",31630)
QCD_HT700to1000 = kreator.makeMCComponent("QCD_HT700to1000", "/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root",6802)
QCD_HT700to1000_ext = kreator.makeMCComponent("QCD_HT700to1000_ext", "/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM", "CMS", ".*root",6802)
QCD_HT1000to1500 = kreator.makeMCComponent("QCD_HT1000to1500", "/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root",1206)
QCD_HT1000to1500_ext = kreator.makeMCComponent("QCD_HT1000to1500_ext", "/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM", "CMS", ".*root",1206)
QCD_HT1500to2000 = kreator.makeMCComponent("QCD_HT1500to2000", "/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root",120.4)
QCD_HT1500to2000_ext = kreator.makeMCComponent("QCD_HT1500to2000_ext", "/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM", "CMS", ".*root",120.4)
QCD_HT2000toInf = kreator.makeMCComponent("QCD_HT2000toInf", "/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root",25.25)
QCD_HT2000toInf_ext = kreator.makeMCComponent("QCD_HT2000toInf_ext", "/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM", "CMS", ".*root",25.25)


QCDHT = [
QCD_HT100to200,
QCD_HT200to300,
QCD_HT200to300_ext,
QCD_HT300to500,
QCD_HT300to500_ext,
QCD_HT500to700,
QCD_HT500to700_ext,
QCD_HT700to1000,
QCD_HT700to1000_ext,
QCD_HT1000to1500,
QCD_HT1000to1500_ext,
QCD_HT1500to2000,
QCD_HT1500to2000_ext,
QCD_HT2000toInf,
QCD_HT2000toInf_ext
]

### DiBosons

# cross section from https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns#Diboson

WWTo2L2Nu = kreator.makeMCComponent("WWTo2L2Nu", "/WWTo2L2Nu_13TeV-powheg/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root", 10.481 )
WWToLNuQQ = kreator.makeMCComponent("WWToLNuQQ", "/WWToLNuQQ_13TeV-powheg/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root", 43.53 )
WWToLNuQQ_ext = kreator.makeMCComponent("WWToLNuQQ_ext", "/WWToLNuQQ_13TeV-powheg/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM", "CMS", ".*root", 43.53 )
WWTo1L1Nu2Q = kreator.makeMCComponent("WWTo1L1Nu2Q", "/WWTo1L1Nu2Q_13TeV_amcatnloFXFX_madspin_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root", 45.35, fracNegWeights=0.189 ) # genXSecAna

ZZTo2L2Nu = kreator.makeMCComponent("ZZTo2L2Nu", "/ZZTo2L2Nu_13TeV_powheg_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root", 0.564)
ZZTo2L2Q = kreator.makeMCComponent("ZZTo2L2Q", "/ZZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM", "CMS", ".*root",  3.28, fracNegWeights=0.18)
ZZTo2Q2Nu = kreator.makeMCComponent("ZZTo2Q2Nu", "/ZZTo2Q2Nu_13TeV_amcatnloFXFX_madspin_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root",  4.04, fracNegWeights=0.19)
ZZTo4L = kreator.makeMCComponent("ZZTo4L", "/ZZTo4L_13TeV_powheg_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM", "CMS", ".*root", 1.256)

#ZZTo4L_amcatnlo = kreator.makeMCComponent("ZZTo4L_amcatnlo", "/ZZTo4L_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM", "CMS", ".*root", 1.212)

WZJToLLLNu =  kreator.makeMCComponent("WZJToLLLNu"  , "/WZJToLLLNu_TuneCUETP8M1_13TeV-amcnlo-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM"  , "CMS", ".*root", 4.708 )
WZTo1L3Nu   = kreator.makeMCComponent("WZTo1L3Nu"  , "/WZTo1L3Nu_13TeV_amcatnloFXFX_madspin_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM"  , "CMS", ".*root", (47.13)*(3*0.108)*(0.2), fracNegWeights=0.22 )
WZTo1L1Nu2Q = kreator.makeMCComponent("WZTo1L1Nu2Q", "/WZTo1L1Nu2Q_13TeV_amcatnloFXFX_madspin_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root",  10.71, fracNegWeights=0.21)
WZTo2L2Q    = kreator.makeMCComponent("WZTo2L2Q"   , "/WZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM"   , "CMS", ".*root",  5.60, fracNegWeights=0.2)
WZTo3LNu_pow    = kreator.makeMCComponent("WZTo3LNu_pow"   , "/WZTo3LNu_TuneCUETP8M1_13TeV-powheg-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM", "CMS", ".*root", 4.42965)
WZTo3LNu_pow_ext= kreator.makeMCComponent("WZTo3LNu_pow_ext", "/WZTo3LNu_TuneCUETP8M1_13TeV-powheg-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v1/MINIAODSIM", "CMS", ".*root", 4.42965)
WZTo3LNu_fxfx = kreator.makeMCComponent("WZTo3LNu_fxfx", "/WZTo3LNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root", 4.666, fracNegWeights=0.19)

VVTo2L2Nu = kreator.makeMCComponent("VVTo2L2Nu","/VVTo2L2Nu_13TeV_amcatnloFXFX_madspin_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root",  11.95, fracNegWeights=0.2)
VVTo2L2Nu_ext = kreator.makeMCComponent("VVTo2L2Nu_ext" ,"/VVTo2L2Nu_13TeV_amcatnloFXFX_madspin_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM", "CMS", ".*root",  11.95, fracNegWeights=0.2)

WGJets = kreator.makeMCComponent("WGJets", "/WGJets_MonoPhoton_PtG-130_TuneCUETP8M1_13TeV-madgraph/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM", "CMS", ".*root", 0.6637)
WGToLNuG = kreator.makeMCComponent("WGToLNuG", "/WGToLNuG_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM", "CMS", ".*root", 585.8)
WGToLNuG_amcatnlo      = kreator.makeMCComponent("WGToLNuG_amcatnlo",      "/WGToLNuG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v1/MINIAODSIM", "CMS", ".*root", 511.2, fracNegWeights=0.18) # genXSecAna
WGToLNuG_amcatnlo_ext  = kreator.makeMCComponent("WGToLNuG_amcatnlo_ext",  "/WGToLNuG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext2-v1/MINIAODSIM", "CMS", ".*root", 511.2, fracNegWeights=0.18) # genXSecAna
WGToLNuG_amcatnlo_ext2 = kreator.makeMCComponent("WGToLNuG_amcatnlo_ext2", "/WGToLNuG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext3-v1/MINIAODSIM", "CMS", ".*root", 511.2, fracNegWeights=0.18) # genXSecAna

ZNuNuGJets_40130 = kreator.makeMCComponent("ZNuNuGJets_40130", "/ZNuNuGJets_MonoPhoton_PtG-40to130_TuneCUETP8M1_13TeV-madgraph/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root",2.816)

ZGTo2NuG = kreator.makeMCComponent("ZGTo2NuG","/ZGTo2NuG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root",28.05, fracNegWeights=0.19)
ZGTo2LG = kreator.makeMCComponent("ZGTo2LG", "/ZGTo2LG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v1/MINIAODSIM", "CMS", ".*root", 131.3, fracNegWeights=0.16)

WWTo2L2Nu_DPS = kreator.makeMCComponent("WWTo2L2Nu_DPS", "/WWTo2L2Nu_DoubleScattering_13TeV-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root", 0.1729)
WpWpJJ = kreator.makeMCComponent("WpWpJJ", "/WpWpJJ_EWK-QCD_TuneCUETP8M1_13TeV-madgraph-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM", "CMS", ".*root", 0.03711)

WW = kreator.makeMCComponent("WW", "/WW_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root", 63.21 * 1.82)
WW_ext = kreator.makeMCComponent("WW_ext", "/WW_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root", 63.21 * 1.82)
WW_ext = kreator.makeMCComponent("WW_ext", "/WW_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM", "CMS", ".*root", 63.21 * 1.82)
WZ = kreator.makeMCComponent("WZ", "/WZ_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root", 47.13 )
WZ_ext = kreator.makeMCComponent("WZ_ext", "/WZ_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM", "CMS", ".*root", 47.13 )
ZZ = kreator.makeMCComponent("ZZ", "/ZZ_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root", 16.523 )
ZZ_ext = kreator.makeMCComponent("ZZ_ext", "/ZZ_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM", "CMS", ".*root", 16.523 )

DiBosons = [
WWTo2L2Nu,
WWToLNuQQ,
WWToLNuQQ_ext,
WWTo1L1Nu2Q,
ZZTo2L2Nu,
ZZTo2L2Q,
ZZTo2Q2Nu,
ZZTo4L,
#ZZTo4L_amcatnlo,
WZJToLLLNu,
WZTo1L3Nu,
WZTo1L1Nu2Q,
WZTo2L2Q,
WZTo3LNu_pow,
WZTo3LNu_pow_ext,
WZTo3LNu_fxfx,
VVTo2L2Nu,
VVTo2L2Nu_ext,
WGToLNuG,
WGToLNuG_amcatnlo,
WGToLNuG_amcatnlo_ext,
WGToLNuG_amcatnlo_ext2,
WGJets,
ZNuNuGJets_40130,
ZGTo2NuG,
ZGTo2LG,
WWTo2L2Nu_DPS,
WpWpJJ,
WW,
WW_ext,
WZ,
WZ_ext,
ZZ,
ZZ_ext
]

### TriBosons
# cross section from https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns#Triboson
WWW = kreator.makeMCComponent("WWW", "/WWW_4F_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root", 0.2086, fracNegWeights=0.053)
WWW_ll = kreator.makeMCComponent("WWW_ll", "/WWW_4F_DiLeptonFilter_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v3/MINIAODSIM", "CMS", ".*root", 0.007201, fracNegWeights=0.063) # xs from genXSecAna (on Fall17)
WWZ = kreator.makeMCComponent("WWZ", "/WWZ_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root",  0.1651 , fracNegWeights=0.06)
WZZ = kreator.makeMCComponent("WZZ", "/WZZ_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root",  0.05565 , fracNegWeights=0.060)
ZZZ = kreator.makeMCComponent("ZZZ", "/ZZZ_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root",  0.01398 , fracNegWeights=0.060)
WZG = kreator.makeMCComponent("WZG", "/WZG_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM", "CMS", ".*root", 0.04123)

TriBosons = [
WWW,
WWW_ll,
WZZ,
WWZ,
ZZZ,
WZG,
]

### TTV
TTWToLNu_fxfx     = kreator.makeMCComponent("TTWToLNu_fxfx", "/TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM", "CMS", ".*root", 0.2043, fracNegWeights=0.227)
TTWToLNu_fxfx_ext = kreator.makeMCComponent("TTWToLNu_fxfx_ext", "/TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext2-v1/MINIAODSIM", "CMS", ".*root", 0.2043, fracNegWeights=0.227)
TTWToQQ = kreator.makeMCComponent("TTWToQQ", "/TTWJetsToQQ_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root", 0.40620, fracNegWeights=0.24)
TTW_LO = kreator.makeMCComponent("TTW_LO", "/ttWJets_13TeV_madgraphMLM/RunIISummer16MiniAODv3-94X_mcRun2_asymptotic_v3-v1/MINIAODSIM", "CMS", ".*root",  0.6105 )
TTZToQQ = kreator.makeMCComponent("TTZToQQ","/TTZToQQ_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root", 0.5297, fracNegWeights=0.264)
TTZToLLNuNu_amc       = kreator.makeMCComponent("TTZToLLNuNu_amc", "/TTZToLLNuNu_M-10_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM", "CMS", ".*root", 0.2529, fracNegWeights=0.264)
TTZToLLNuNu_amc_ext  = kreator.makeMCComponent("TTZToLLNuNu_amc_ext", "/TTZToLLNuNu_M-10_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext2-v1/MINIAODSIM", "CMS", ".*root", 0.2529, fracNegWeights=0.264)
TTZToLLNuNu_amc_ext2 = kreator.makeMCComponent("TTZToLLNuNu_amc_ext2", "/TTZToLLNuNu_M-10_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext3-v1/MINIAODSIM", "CMS", ".*root", 0.2529, fracNegWeights=0.264)
TTZToLLNuNu_m1to10  = kreator.makeMCComponent("TTZToLLNuNu_m1to10","/TTZToLL_M-1to10_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-94X_mcRun2_asymptotic_v3-v1/MINIAODSIM", "CMS", ".*root", 0.0493)
# https://twiki.cern.ch/twiki/bin/view/CMS/SameSignDilepton2016
TTZ_LO = kreator.makeMCComponent("TTZ_LO", "/ttZJets_13TeV_madgraphMLM/RunIISummer16MiniAODv3-94X_mcRun2_asymptotic_v3-v1/MINIAODSIM", "CMS", ".*root",  0.5297/0.692)
TTGJets     = kreator.makeMCComponent("TTGJets",    "/TTGJets_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root", 3.76, fracNegWeights=0.34)
TTGJets_ext = kreator.makeMCComponent("TTGJets_ext","/TTGJets_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM", "CMS", ".*root", 3.76, fracNegWeights=0.34)

TTV = [
TTWToLNu_fxfx,
TTWToLNu_fxfx_ext,
TTWToQQ,
TTW_LO,
TTZToQQ,
TTZToLLNuNu_amc,
TTZToLLNuNu_amc_ext,
TTZToLLNuNu_amc_ext2,
TTZToLLNuNu_m1to10,
TTZ_LO,
TTGJets,
TTGJets_ext
]

### Rares
TTTT = kreator.makeMCComponent("TTTT", "/TTTT_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root", 0.009103, fracNegWeights=0.311)
TTTT_P8M2T4 = kreator.makeMCComponent("TTTT_P8M2T4", "/TTTT_TuneCUETP8M2T4_13TeV-amcatnlo-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM", "CMS", ".*root", 0.009103, fracNegWeights=0.311)
TTWW = kreator.makeMCComponent("TTWW","/TTWW_TuneCUETP8M2T4_13TeV-madgraph-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v1/MINIAODSIM", "CMS",".*root", 0.007936) # XS from genXSAnalyzer
TTWH = kreator.makeMCComponent("TTWH", "/TTWH_TuneCUETP8M2T4_13TeV-madgraph-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v1/MINIAODSIM", "CMS", ".*root", 0.001141)
TTZH = kreator.makeMCComponent("TTZH", "/TTZH_TuneCUETP8M2T4_13TeV-madgraph-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v1/MINIAODSIM", "CMS", ".*root", 0.001243)

Rares = [
TTTT,
TTTT_P8M2T4,
TTWW,
TTWH,
TTZH,
]


### EWK V+jets 
EWKWMinus2Jets = kreator.makeMCComponent("EWKWMinus2Jets", "/EWKWMinus2Jets_WToLNu_M-50_13TeV-madgraph-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root", 20.2) # genXSecAna
EWKWMinus2Jets_ext = kreator.makeMCComponent("EWKWMinus2Jets_ext", "/EWKWMinus2Jets_WToLNu_M-50_13TeV-madgraph-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM", "CMS", ".*root", 20.2) # genXSecAna 
EWKWMinus2Jets_ext2 = kreator.makeMCComponent("EWKWMinus2Jets_ext2", "/EWKWMinus2Jets_WToLNu_M-50_13TeV-madgraph-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext2-v2/MINIAODSIM", "CMS", ".*root", 20.2) # genXSecAna 
EWKWPlus2Jets = kreator.makeMCComponent("EWKWPlus2Jets", "/EWKWPlus2Jets_WToLNu_M-50_13TeV-madgraph-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM", "CMS", ".*root", 25.82)
EWKWPlus2Jets_ext = kreator.makeMCComponent("EWKWPlus2Jets_ext", "/EWKWPlus2Jets_WToLNu_M-50_13TeV-madgraph-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext2-v2/MINIAODSIM", "CMS", ".*root", 25.82)
EWKZToLL2Jets = kreator.makeMCComponent("EWKZToLL2Jets", "/EWKZ2Jets_ZToLL_M-50_13TeV-madgraph-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM", "CMS", ".*root", 3.998)
EWKZToLL2Jets_ext = kreator.makeMCComponent("EWKZToLL2Jets_ext", "/EWKZ2Jets_ZToLL_M-50_13TeV-madgraph-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext2-v2/MINIAODSIM", "CMS", ".*root", 3.998)
EWKZToNuNu2Jets = kreator.makeMCComponent("EWKZToNuNu2Jets", "/EWKZ2Jets_ZToNuNu_13TeV-madgraph-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM", "CMS", ".*root", 10.14)
EWKZToNuNu2Jets_ext = kreator.makeMCComponent("EWKZToNuNu2Jets_ext", "/EWKZ2Jets_ZToNuNu_13TeV-madgraph-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext2-v2/MINIAODSIM", "CMS", ".*root", 10.14)

EWKV2Jets = [
EWKWMinus2Jets, EWKWMinus2Jets_ext, EWKWMinus2Jets_ext2,
EWKWPlus2Jets, EWKWPlus2Jets_ext,
EWKZToLL2Jets, EWKZToLL2Jets_ext,
EWKZToNuNu2Jets, EWKZToNuNu2Jets_ext,
]

### ----------------------------- summary ----------------------------------------

mcSamples = TTs + SingleTop + VJets + DYJetsM50HT + DYJetsM5to50HT + DYNJets + WJetsToLNuHT + WJetsToLNuPT + WNJets + GJetsHT + ZJetsToNuNuHT + QCDHT + QCDPtbcToE + QCDPt + QCDPtEMEnriched + [QCD_Mu15] + QCD_Mu5 +  DiBosons + TriBosons + TTV + Higgs + Rares + EWKV2Jets 

samples = mcSamples

if __name__ == "__main__":
    from CMGTools.RootTools.samples.tools import runMain
    runMain(samples,localobjs=locals())
