import PhysicsTools.HeppyCore.framework.config as cfg
import os

#####COMPONENT CREATOR

from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()

### NB: Commented lines refer to samples available in RunIIFall15MiniAODv2 but not yet in RunIISpring16MiniAODv1

### ----------------------------- 25 ns ----------------------------------------

# TTbar cross section: NNLO, https://twiki.cern.ch/twiki/bin/view/LHCPhysics/TtbarNNLO (172.5)
TTJets = kreator.makeMCComponent("TTJets", "/TTJets_TuneCUETP8M2T4_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv2-PUMoriond17_backup_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root", 831.76)
# NOTAVAILYET # TTJets_reHLT = kreator.makeMCComponent("TTJets_reHLT", "/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM", "CMS", ".*root", 831.76)

#TTJets_ext = kreator.makeMCComponent("TTJets_ext", "/TTJets_13TeV-amcatnloFXFX-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/MINIAODSIM", "CMS", ".*root", 831.76)
#TTJets_LO = kreator.makeMCComponent("TTJets_LO", "/TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM", "CMS", ".*root", 831.76)
TT_pow = kreator.makeMCComponent("TT_pow", "/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root", 831.762)
TT_pow_ext3 = kreator.makeMCComponent("TT_pow_ext3", "/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/RunIISummer16MiniAODv2-PUMoriond17_backup_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root", 831.76)
# NOTAVAILYET # TT_pow_ext4 = kreator.makeMCComponent("TT_pow_ext4", "/TT_TuneCUETP8M1_13TeV-powheg-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext4-v1/MINIAODSIM", "CMS", ".*root", 831.76)

TTJets_SingleLeptonFromTbar     = kreator.makeMCComponent("TTJets_SingleLeptonFromTbar"    , "/TTJets_SingleLeptFromTbar_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root", 831.76*(3*0.108)*(1-3*0.108) )
TTJets_SingleLeptonFromTbar_ext = kreator.makeMCComponent("TTJets_SingleLeptonFromTbar_ext", "/TTJets_SingleLeptFromTbar_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM", "CMS", ".*root", 831.76*(3*0.108)*(1-3*0.108) )
TTJets_SingleLeptonFromT        = kreator.makeMCComponent("TTJets_SingleLeptonFromT"       , "/TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root", 831.76*(3*0.108)*(1-3*0.108))
TTJets_SingleLeptonFromT_ext    = kreator.makeMCComponent("TTJets_SingleLeptonFromT_ext"   , "/TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM", "CMS", ".*root", 831.76*(3*0.108)*(1-3*0.108))
TTJets_DiLepton                 = kreator.makeMCComponent("TTJets_DiLepton"                , "/TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM"     , "CMS", ".*root", 831.76*((3*0.108)**2) )
TTJets_DiLepton_ext             = kreator.makeMCComponent("TTJets_DiLepton_ext"            , "/TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM", "CMS", ".*root", 831.76*((3*0.108)**2) )

TTLep_pow = kreator.makeMCComponent("TTLep_pow", "/TTTo2L2Nu_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root", 831.76*((3*0.108)**2) )
# NOTAVAILYET # TTLep_pow_ext = kreator.makeMCComponent("TTLep_pow_ext", "/TTTo2L2Nu_13TeV-powheg/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1/MINIAODSIM", "CMS", ".*root", 831.76*((3*0.108)**2) )
TTSemiLep_pow = kreator.makeMCComponent("TTSemiLep_pow", "/TTToSemilepton_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root", 2*831.76*(3*0.108)*(1-3*0.108) )

#
# NOTAVAILYET # TTJets_LO_HT600to800       = kreator.makeMCComponent("TTJets_LO_HT600to800", "/TTJets_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM", "CMS", ".*root", 1.610*831.76/502.2)
TTJets_LO_HT600to800_ext   = kreator.makeMCComponent("TTJets_LO_HT600to800_ext", "/TTJets_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM", "CMS", ".*root", 1.610*831.76/502.2)
# NOTAVAILYET # TTJets_LO_HT800to1200      = kreator.makeMCComponent("TTJets_LO_HT800to1200", "/TTJets_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM", "CMS", ".*root", 0.663*831.76/502.2)
TTJets_LO_HT800to1200_ext  = kreator.makeMCComponent("TTJets_LO_HT800to1200_ext", "/TTJets_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM",  "CMS", ".*root", 0.663*831.76/502.2)
# NOTAVAILYET # TTJets_LO_HT1200to2500     = kreator.makeMCComponent("TTJets_LO_HT1200to2500", "/TTJets_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM", "CMS", ".*root", 0.12*831.76/502.2)
TTJets_LO_HT1200to2500_ext = kreator.makeMCComponent("TTJets_LO_HT1200to2500_ext", "/TTJets_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM", "CMS", ".*root", 0.12*831.76/502.2)
# NOTAVAILYET # TTJets_LO_HT2500toInf      = kreator.makeMCComponent("TTJets_LO_HT2500toInf", "/TTJets_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM", "CMS", ".*root", 0.001430*831.76/502.2)
TTJets_LO_HT2500toInf_ext  = kreator.makeMCComponent("TTJets_LO_HT2500toInf_ext", "/TTJets_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM",  "CMS", ".*root", 0.001430*831.76/502.2)


TTs = [
TTJets,
# NOTAVAILYET # TTJets_reHLT,
#TTJets_ext,
#TTJets_LO,
TT_pow_ext3,
# NOTAVAILYET # TT_pow_ext4,
TT_pow,
TTJets_SingleLeptonFromTbar,
TTJets_SingleLeptonFromTbar_ext,
TTJets_SingleLeptonFromT,
TTJets_SingleLeptonFromT_ext,
TTJets_DiLepton,
TTJets_DiLepton_ext,
TTLep_pow,
# NOTAVAILYET # TTLep_pow_ext,
TTSemiLep_pow,
# NOTAVAILYET # TTJets_LO_HT600to800,
TTJets_LO_HT600to800_ext,
# NOTAVAILYET # TTJets_LO_HT800to1200,
TTJets_LO_HT800to1200_ext,
# NOTAVAILYET # TTJets_LO_HT1200to2500,
TTJets_LO_HT1200to2500_ext,
# NOTAVAILYET # TTJets_LO_HT2500toInf
TTJets_LO_HT2500toInf_ext
]



# Higgs
# TTH cross section from LHC Higgs XS WG: https://twiki.cern.ch/twiki/bin/view/LHCPhysics/CERNYellowReportPageAt1314TeV?rev=15
#TTHnobb     = kreator.makeMCComponent("TTHnobb", "/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM", "CMS", ".*root",0.5085*(1-0.577))
# NOTAVAILYET # TTHnobb_ext = kreator.makeMCComponent("TTHnobb_ext", "/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v2/MINIAODSIM", "CMS", ".*root",0.5085*(1-0.577))
TTHnobb_pow = kreator.makeMCComponent("TTHnobb_pow", "/ttHToNonbb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root",0.5085*(1-0.577))
TTHnobb_mWCutfix_ext = kreator.makeMCComponent("TTHnobb_mWCutfix_ext", "/ttHJetToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8_mWCutfix/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM", "CMS", ".*root", 0.5085*(1-0.577))


# GGH cross section from LHC Higgs XS WG: https://twiki.cern.ch/twiki/bin/view/LHCPhysics/CERNYellowReportPageAt1314TeV?rev=15
GGHZZ4L = kreator.makeMCComponent("GGHZZ4L", "/GluGluHToZZTo4L_M125_13TeV_powheg2_JHUgenV6_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root", 0.01212) #43.92*2.76E-04)
# NOTAVAILYET # GGHZZ4L = kreator.makeMCComponent("GGHZZ4L", "/GluGluHToZZTo4L_M125_13TeV_powheg2_JHUgenV6_pythia8/RunIISpring16MiniAODv1-PUSpring16RAWAODSIM_80X_mcRun2_asymptotic_2016_v3-v1/MINIAODSIM", "CMS", ".*root", 0.01212)
#QQHZZ4L = kreator.makeMCComponent("QQHZZ4L", "/VBF_HToZZTo4L_M125_13TeV_powheg2_JHUgenV6_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM", "CMS", ".*root", 0.001034)# 3.748*2.76E-04)
# split in assing W+/(W+ + W-) = 0.6385 as at 8 TeV, to be updated
#WpHZZ4L = kreator.makeMCComponent("WpHZZ4L", "/WplusH_HToZZTo4L_M125_13TeV_powheg2-minlo-HWJ_JHUgenV6_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM", "CMS", ".*root", 0.0002339) # 1.38*0.6385*2.76E-04)
#WmHZZ4L = kreator.makeMCComponent("WmHZZ4L", "/WminusH_HToZZTo4L_M125_13TeV_powheg2-minlo-HWJ_JHUgenV6_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM", "CMS", ".*root", 0.0001471) # 1.38*(1-0.6385)*2.76E-04)
#ZHZZ4LF = kreator.makeMCComponent("ZHZZ4LF", "/ZH_HToZZ_4LFilter_M125_13TeV_powheg2-minlo-HZJ_JHUgenV6_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM", "CMS", ".*root", 0.000652) #0.8696*(3.70E-03+2.34E-02+2.76E-04)*0.15038)
#TTHZZ4LF = kreator.makeMCComponent("TTHZZ4LF", "/ttH_HToZZ_4LFilter_M125_13TeV_powheg2_JHUgenV6_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM", "CMS", ".*root", 0.000337 )

VHToNonbb = kreator.makeMCComponent("VHToNonbb", "/VHToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root", 0.9561)

Higgs = [
#TTHnobb,
# NOTAVAILYET # TTHnobb_ext,
TTHnobb_pow,
TTHnobb_mWCutfix_ext,
GGHZZ4L,
#QQHZZ4L,
#WpHZZ4L,
#WmHZZ4L,
#ZHZZ4LF,
#TTHZZ4LF,
VHToNonbb,
]

#TTHbb       = kreator.makeMCComponent("TTHbb",      "/ttHJetTobb_M125_13TeV_amcatnloFXFX_madspin_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext3-v2/MINIAODSIM", "CMS", ".*root", 0.5085*(0.577))
#TTHbb_ext1   = kreator.makeMCComponent("TTHbb_ext1",  "/ttHJetTobb_M125_13TeV_amcatnloFXFX_madspin_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/MINIAODSIM", "CMS", ".*root",  0.5085*(0.577))
#TTHbb_ext2   = kreator.makeMCComponent("TTHbb_ext2",  "/ttHJetTobb_M125_13TeV_amcatnloFXFX_madspin_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext2-v1/MINIAODSIM", "CMS", ".*root",  0.5085*(0.577))
# NOTAVAILYET # TTHbb_ext3   = kreator.makeMCComponent("TTHbb_ext3",      "/ttHJetTobb_M125_13TeV_amcatnloFXFX_madspin_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext3-v2/MINIAODSIM", "CMS", ".*root", 0.5085*(0.577))

Higgs += [
#TTHbb,
#TTHbb_ext1,
#TTHbb_ext2,
# NOTAVAILYET # TTHbb_ext3,
]

# These are the SM cross sections, i.e. cf = cv = 1.0 (see https://twiki.cern.ch/twiki/bin/viewauth/CMS/SingleTopHiggsGeneration13TeV)
THQ = kreator.makeMCComponent("THQ", "/THQ_Hincl_13TeV-madgraph-pythia8_TuneCUETP8M1/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root",  0.7927)
THW = kreator.makeMCComponent("THW", "/THW_Hincl_13TeV-madgraph-pythia8_TuneCUETP8M1/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root",  0.1472)

Higgs += [
THQ,
THW,
]

# Single top cross sections: https://twiki.cern.ch/twiki/bin/viewauth/CMS/SingleTopSigma
# NOTAVAILYET # TToLeptons_tch_amcatnlo = kreator.makeMCComponent("TToLeptons_tch_amcatnlo", "/ST_t-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1/RunIISpring16MiniAODv2-premix_withHLT_80X_mcRun2_asymptotic_v14_ext1-v1/MINIAODSIM", "CMS", ".*root", (136.05+80.97)*0.108*3)
#TToLeptons_tch_amcatnlo_ext = kreator.makeMCComponent("TToLeptons_tch_amcatnlo_ext", "/ST_t-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/MINIAODSIM", "CMS", ".*root", (136.05+80.97)*0.108*3) 
# NOTAVAILYET # TToLeptons_tch_powheg = kreator.makeMCComponent("TToLeptons_tch_powheg", "/ST_t-channel_top_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM", "CMS", ".*root", (136.02)*0.108*3)
# NOTAVAILYET # TBarToLeptons_tch_powheg = kreator.makeMCComponent("TBarToLeptons_tch_powheg", "/ST_t-channel_antitop_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM", "CMS", ".*root", 80.95*0.108*3)

TToLeptons_sch_amcatnlo = kreator.makeMCComponent("TToLeptons_sch_amcatnlo", "/ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root", (7.20+4.16)*0.108*3)
T_sch_amcatnlo = kreator.makeMCComponent("T_sch_amcatnlo", "/ST_s-channel_4f_InclusiveDecays_13TeV-amcatnlo-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root", (7.20+4.16))

T_tch_powheg = kreator.makeMCComponent("T_tch_powheg", "/ST_t-channel_top_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root", 136.02) # inclusive sample
TBar_tch_powheg = kreator.makeMCComponent("TBar_tch_powheg", "/ST_t-channel_antitop_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root", 80.95) # inclusive sample

TBar_tWch_noFullyHad_ext = kreator.makeMCComponent("TBar_tWch_noFullyHad_ext", "/ST_tW_antitop_5f_NoFullyHadronicDecays_13TeV-powheg_TuneCUETP8M1/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM", "CMS", ".*root",19.55)
TBar_tWch_noFullyHad      = kreator.makeMCComponent("TBar_tWch_noFullyHad"     , "/ST_tW_antitop_5f_NoFullyHadronicDecays_13TeV-powheg_TuneCUETP8M1/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root",19.55)
TBar_tWch_ext = kreator.makeMCComponent("TBar_tWch_ext", "/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM", "CMS", ".*root",35.6)

T_tWch_noFullyHad_ext = kreator.makeMCComponent("T_tWch_noFullyHad_ext", "/ST_tW_top_5f_NoFullyHadronicDecays_13TeV-powheg_TuneCUETP8M1/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM", "CMS", ".*root",19.55)
T_tWch_noFullyHad      = kreator.makeMCComponent("T_tWch_noFullyHad"     , "/ST_tW_top_5f_NoFullyHadronicDecays_13TeV-powheg_TuneCUETP8M1/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root",19.55)
T_tWch_ext= kreator.makeMCComponent("T_tWch_ext", "/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM", "CMS", ".*root",35.6)

TGJets = kreator.makeMCComponent("TGJets", "/TGJets_TuneCUETP8M1_13TeV_amcatnlo_madspin_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root", 2.967)
TGJets_ext = kreator.makeMCComponent("TGJets_ext", "/TGJets_TuneCUETP8M1_13TeV_amcatnlo_madspin_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM", "CMS", ".*root", 2.967)
tZq_ll_ext = kreator.makeMCComponent("tZq_ll_ext", "/tZq_ll_4f_13TeV-amcatnlo-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM", "CMS", ".*root", 0.0758 )
#tZq_nunu = kreator.makeMCComponent("tZq_nunu", "/tZq_nunu_4f_13TeV-amcatnlo-pythia8_TuneCUETP8M1/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM", "CMS", ".*root", 0.1379 )
tWll = kreator.makeMCComponent("tWll", "/ST_tWll_5f_LO_13TeV-MadGraph-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root", 0.01123)
tWnunu = kreator.makeMCComponent("tWnunu", "/ST_tWnunu_5f_LO_13TeV-MadGraph-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root", 0.01123*1.9822 )

SingleTop = [
# NOTAVAILYET # TToLeptons_tch_amcatnlo,
#TBarToLeptons_tch_amcatnlo,
#TToLeptons_tch_amcatnlo_ext,
# NOTAVAILYET # TToLeptons_tch_powheg,
# NOTAVAILYET # TBarToLeptons_tch_powheg,
TToLeptons_sch_amcatnlo,
T_sch_amcatnlo,
TBar_tWch_noFullyHad_ext,
TBar_tWch_noFullyHad,
T_tWch_noFullyHad_ext,
T_tWch_noFullyHad,
T_tch_powheg,
TBar_tch_powheg,
TBar_tWch_ext,
T_tWch_ext,
TGJets,
TGJets_ext,
tZq_ll_ext,
#tZq_nunu,
tWll,
tWnunu
]

### V+jets inclusive (from https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat13TeV)
WJetsToLNu = kreator.makeMCComponent("WJetsToLNu","/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root", 3* 20508.9)
WJetsToLNu_LO = kreator.makeMCComponent("WJetsToLNu_LO","/WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root", 3* 20508.9)
WJetsToLNu_LO_ext =  kreator.makeMCComponent("WJetsToLNu_LO_ext", "/WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v1/MINIAODSIM", "CMS", ".*root", 61526.7)
# NOTAVAILYET # WJetsToLNu_reHLT = kreator.makeMCComponent("WJetsToLNu_reHLT","/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14_ext1-v1/MINIAODSIM", "CMS", ".*root", 3* 20508.9)
# NOTAVAILYET # WJetsToLNu_LO_reHLT = kreator.makeMCComponent("WJetsToLNu_LO_reHLT","/WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14_ext1-v1/MINIAODSIM", "CMS", ".*root", 3* 20508.9)

DYJetsToLL_M10to50 = kreator.makeMCComponent("DYJetsToLL_M10to50", "/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root", 18610)
DYJetsToLL_M10to50_ext = kreator.makeMCComponent("DYJetsToLL_M10to50_ext", "/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM", "CMS", ".*root", 18610)
DYJetsToLL_M10to50_LO = kreator.makeMCComponent("DYJetsToLL_M10to50_LO", "/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root", 18610)
# NOTAVAILYET # DYJetsToLL_M5to50_LO = kreator.makeMCComponent("DYJetsToLL_M5to50_LO", "/DYJetsToLL_M-5to50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM", "CMS", ".*root", 7.1310*10**4)
DYJetsToLL_M50 = kreator.makeMCComponent("DYJetsToLL_M50", "/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv2-PUMoriond17_HCALDebug_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root", 2008.*3)
DYJetsToLL_M50_LO_ext =  kreator.makeMCComponent("DYJetsToLL_M50_LO_ext", "/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v2/MINIAODSIM", "CMS", ".*root", 2008.*3)
DYJetsToLL_M50_LO_ext2 =  kreator.makeMCComponent("DYJetsToLL_M50_LO_ext2", "/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v1/MINIAODSIM", "CMS", ".*root", 2008.*3)
# NOTAVAILYET # DYJetsToLL_M50_reHLT = kreator.makeMCComponent("DYJetsToLL_M50_reHLT", "/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM", "CMS", ".*root", 2008.*3)
# NOTAVAILYET # DYJetsToLL_M50_LO_reHLT =  kreator.makeMCComponent("DYJetsToLL_M50_LO_reHLT", "/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14_ext1-v1/MINIAODSIM", "CMS", ".*root", 2008.*3)



#DYJetsToNuNu_M50 = kreator.makeMCComponent("DYJetsToNuNu_M50", "/DYJetsToNuNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM", "CMS", ".*root", 2008.*3)

#DYJetsToLL_M50_flatPu = kreator.makeMCComponent("DYJetsToLL_M50_flatPu", "/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv1-PUFlat0to50_80X_mcRun2_asymptotic_2016_v3-v1/MINIAODSIM", "CMS", ".*root", 2008.*3)

VJets = [
WJetsToLNu,
WJetsToLNu_LO,
WJetsToLNu_LO_ext,
# NOTAVAILYET # WJetsToLNu_reHLT,
# NOTAVAILYET # WJetsToLNu_LO_reHLT,
DYJetsToLL_M10to50,
DYJetsToLL_M10to50_ext,
DYJetsToLL_M10to50_LO,
# NOTAVAILYET # DYJetsToLL_M5to50_LO,
DYJetsToLL_M50,
DYJetsToLL_M50_LO_ext,
DYJetsToLL_M50_LO_ext2,
# NOTAVAILYET # DYJetsToLL_M50_reHLT,
# NOTAVAILYET # DYJetsToLL_M50_LO_reHLT,
#DYJetsToNuNu_M50,
#DYJetsToLL_M50_flatPu,
]

# DY njet bins
DY1JetsToLL_M50_LO =  kreator.makeMCComponent("DY1JetsToLL_M50_LO", "/DY1JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root", 1012.5)
DY2JetsToLL_M50_LO =  kreator.makeMCComponent("DY2JetsToLL_M50_LO", "/DY2JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root", 332.8)
DY3JetsToLL_M50_LO =  kreator.makeMCComponent("DY3JetsToLL_M50_LO", "/DY3JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root", 101.8)
DY4JetsToLL_M50_LO =  kreator.makeMCComponent("DY4JetsToLL_M50_LO", "/DY4JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root", 54.8)

# NOTAVAILYET # DY1JetsToLL_M10to50 =  kreator.makeMCComponent("DY1JetsToLL_M10to50", "/DY1JetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM", "CMS", ".*root", 432.5) # from GenXSecAnalyzer
# NOTAVAILYET # DY2JetsToLL_M10to50 =  kreator.makeMCComponent("DY2JetsToLL_M10to50", "/DY2JetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM", "CMS", ".*root", 202.9) # from GenXSecAnalyzer

DYNJets = [ 
DY1JetsToLL_M50_LO,
DY2JetsToLL_M50_LO,
DY3JetsToLL_M50_LO,
DY4JetsToLL_M50_LO,
# NOTAVAILYET # DY1JetsToLL_M10to50,
# NOTAVAILYET # DY2JetsToLL_M10to50,
]

# W njet bins
W1JetsToLNu_LO =  kreator.makeMCComponent("W1JetsToLNu_LO", "/W1JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root", 9644.5)
W2JetsToLNu_LO =  kreator.makeMCComponent("W2JetsToLNu_LO", "/W2JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root", 3144.5)
W2JetsToLNu_LO_ext =  kreator.makeMCComponent("W2JetsToLNu_LO_ext", "/W2JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM", "CMS", ".*root", 3144.5)
W3JetsToLNu_LO =  kreator.makeMCComponent("W3JetsToLNu_LO", "/W3JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root", 954.8)
W3JetsToLNu_LO_ext =  kreator.makeMCComponent("W3JetsToLNu_LO_ext", "/W3JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM", "CMS", ".*root", 954.8)
W4JetsToLNu_LO =  kreator.makeMCComponent("W4JetsToLNu_LO", "/W4JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root", 485.6)
W4JetsToLNu_LO_ext =  kreator.makeMCComponent("W4JetsToLNu_LO_ext", "/W4JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM", "CMS", ".*root", 485.6)
W4JetsToLNu_LO_ext2 =  kreator.makeMCComponent("W4JetsToLNu_LO_ext2", "/W4JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v1/MINIAODSIM", "CMS", ".*root", 485.6)

WNJets = [
W1JetsToLNu_LO,
W2JetsToLNu_LO,
W2JetsToLNu_LO_ext,
W3JetsToLNu_LO,
W3JetsToLNu_LO_ext,
W4JetsToLNu_LO,
W4JetsToLNu_LO_ext,
W4JetsToLNu_LO_ext2
]

# DY HT bins:
#https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns#DY_Z

DYJetsToLL_M50_HT70to100      =   kreator.makeMCComponent("DYJetsToLL_M50_HT70to100"    , '/DYJetsToLL_M-50_HT-70to100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM'        ,    "CMS", ".*root", 170.4 *1.23)
DYJetsToLL_M50_HT100to200     =   kreator.makeMCComponent("DYJetsToLL_M50_HT100to200", "/DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM"             , "CMS", ".*root", 147.4*1.23)
DYJetsToLL_M50_HT100to200_ext =   kreator.makeMCComponent("DYJetsToLL_M50_HT100to200_ext", "/DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM",     "CMS", ".*root", 147.4*1.23)
DYJetsToLL_M50_HT200to400     =   kreator.makeMCComponent("DYJetsToLL_M50_HT200to400", "/DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM"             , "CMS", ".*root",40.99*1.23)
DYJetsToLL_M50_HT200to400_ext =   kreator.makeMCComponent("DYJetsToLL_M50_HT200to400_ext", "/DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM"    , "CMS", ".*root",40.99*1.23)
DYJetsToLL_M50_HT400to600     =   kreator.makeMCComponent("DYJetsToLL_M50_HT400to600", "/DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM"             , "CMS", ".*root",5.678*1.23)
DYJetsToLL_M50_HT400to600_ext =   kreator.makeMCComponent("DYJetsToLL_M50_HT400to600_ext", "/DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM"    , "CMS", ".*root",5.678*1.23)
# NOTAVAILYET # DYJetsToLL_M50_HT600toInf = kreator.makeMCComponent("DYJetsToLL_M50_HT600toInf", "/DYJetsToLL_M-50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM", "CMS", ".*root",2.198*1.23)
# NOTAVAILYET # DYJetsToLL_M50_HT600toInf_ext = kreator.makeMCComponent("DYJetsToLL_M50_HT600toInf_ext", "/DYJetsToLL_M-50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1/MINIAODSIM", "CMS", ".*root",2.198*1.23)
DYJetsToLL_M50_HT600to800     =   kreator.makeMCComponent("DYJetsToLL_M50_HT600to800"   , '/DYJetsToLL_M-50_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v2/MINIAODSIM',           "CMS", ".*root", 1.367*1.23 )
DYJetsToLL_M50_HT800to1200    =   kreator.makeMCComponent("DYJetsToLL_M50_HT800to1200"  , '/DYJetsToLL_M-50_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',          "CMS", ".*root", 0.6304*1.23 )
DYJetsToLL_M50_HT1200to2500   =   kreator.makeMCComponent("DYJetsToLL_M50_HT1200to2500" , '/DYJetsToLL_M-50_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',         "CMS", ".*root", 0.1514*1.23 )
DYJetsToLL_M50_HT2500toInf    =   kreator.makeMCComponent("DYJetsToLL_M50_HT2500toInf"  , '/DYJetsToLL_M-50_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',          "CMS", ".*root", 0.003565*1.23 )


DYJetsM50HT = [
DYJetsToLL_M50_HT70to100   , 
DYJetsToLL_M50_HT100to200,
DYJetsToLL_M50_HT100to200_ext,
DYJetsToLL_M50_HT200to400,
DYJetsToLL_M50_HT200to400_ext,
DYJetsToLL_M50_HT400to600,
DYJetsToLL_M50_HT400to600_ext,
# NOTAVAILYET # DYJetsToLL_M50_HT600toInf,
# NOTAVAILYET # DYJetsToLL_M50_HT600toInf_ext,
DYJetsToLL_M50_HT600to800  ,
DYJetsToLL_M50_HT800to1200 ,
DYJetsToLL_M50_HT1200to2500,
DYJetsToLL_M50_HT2500toInf ,

]



DYJetsToLL_M5to50_HT100to200     = kreator.makeMCComponent("DYJetsToLL_M5to50_HT100to200"    , "/DYJetsToLL_M-5to50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root", 224.2) #LO
DYJetsToLL_M5to50_HT100to200_ext = kreator.makeMCComponent("DYJetsToLL_M5to50_HT100to200_ext", "/DYJetsToLL_M-5to50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM", "CMS", ".*root", 224.2) #LO
DYJetsToLL_M5to50_HT200to400     = kreator.makeMCComponent("DYJetsToLL_M5to50_HT200to400"    , "/DYJetsToLL_M-5to50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root", 37.2) #LO
DYJetsToLL_M5to50_HT200to400_ext = kreator.makeMCComponent("DYJetsToLL_M5to50_HT200to400_ext", "/DYJetsToLL_M-5to50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM", "CMS", ".*root", 37.2) #LO
DYJetsToLL_M5to50_HT400to600     = kreator.makeMCComponent("DYJetsToLL_M5to50_HT400to600"    , "/DYJetsToLL_M-5to50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root", 3.581) #LO
DYJetsToLL_M5to50_HT400to600_ext = kreator.makeMCComponent("DYJetsToLL_M5to50_HT400to600_ext", "/DYJetsToLL_M-5to50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM", "CMS", ".*root", 3.581)
DYJetsToLL_M5to50_HT600toInf     = kreator.makeMCComponent("DYJetsToLL_M5to50_HT600toInf"    , "/DYJetsToLL_M-5to50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root", 1.124) #LO
DYJetsToLL_M5to50_HT600toInf_ext = kreator.makeMCComponent("DYJetsToLL_M5to50_HT600toInf_ext", "/DYJetsToLL_M-5to50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM", "CMS", ".*root", 1.124) #LO

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

# DYJets high mass
# Note: The following is really only tau tau
#DYJetsToTauTau_M150_LO = kreator.makeMCComponent("DYJetsToTauTau_M150_LO", "/DYJetsToLL_M-150_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM", "CMS", ".*root", 6.7)

### W+jets
WJetsToLNu_HT70to100 = kreator.makeMCComponent("WJetsToLNu_HT70to100", "/WJetsToLNu_HT-70To100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root",1319*1.21)
WJetsToLNu_HT100to200 = kreator.makeMCComponent("WJetsToLNu_HT100to200", "/WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root",1345*1.21)
WJetsToLNu_HT100to200_ext = kreator.makeMCComponent("WJetsToLNu_HT100to200_ext", "/WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM", "CMS", ".*root",1345*1.21)
WJetsToLNu_HT100to200_ext2 = kreator.makeMCComponent("WJetsToLNu_HT100to200_ext2", "/WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v1/MINIAODSIM", "CMS", ".*root",1345*1.21)
WJetsToLNu_HT200to400 = kreator.makeMCComponent("WJetsToLNu_HT200to400", "/WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root",359.7*1.21)
WJetsToLNu_HT200to400_ext = kreator.makeMCComponent("WJetsToLNu_HT200to400_ext", "/WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM", "CMS", ".*root",359.7*1.21)
WJetsToLNu_HT200to400_ext2 = kreator.makeMCComponent("WJetsToLNu_HT200to400_ext2", '/WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v1/MINIAODSIM' , "CMS", ".*root",359.7*1.21)
WJetsToLNu_HT400to600      = kreator.makeMCComponent("WJetsToLNu_HT400to600", "/WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root",48.91*1.21)
WJetsToLNu_HT400to600_ext  = kreator.makeMCComponent("WJetsToLNu_HT400to600_ext", "/WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM", "CMS", ".*root",48.91*1.21)
WJetsToLNu_HT600to800      = kreator.makeMCComponent("WJetsToLNu_HT600to800",     "/WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root",12.05*1.21)
WJetsToLNu_HT600to800_ext  = kreator.makeMCComponent("WJetsToLNu_HT600to800_ext", '/WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM', "CMS", ".*root",12.05*1.21)
WJetsToLNu_HT800to1200     = kreator.makeMCComponent("WJetsToLNu_HT800to1200",    "/WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root",5.501*1.21)
WJetsToLNu_HT800to1200_ext = kreator.makeMCComponent("WJetsToLNu_HT800to1200_ext","/WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM", "CMS", ".*root",5.501*1.21)
WJetsToLNu_HT1200to2500    = kreator.makeMCComponent("WJetsToLNu_HT1200to2500",   "/WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root",1.329*1.21)
WJetsToLNu_HT1200to2500_ext = kreator.makeMCComponent("WJetsToLNu_HT1200to2500_ext", "/WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM", "CMS", ".*root",1.329*1.21)
WJetsToLNu_HT2500toInf = kreator.makeMCComponent("WJetsToLNu_HT2500toInf", "/WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root",0.03216*1.21)
WJetsToLNu_HT2500toInf_ext = kreator.makeMCComponent("WJetsToLNu_HT2500toInf_ext", "/WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM", "CMS", ".*root",0.03216*1.21)

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
WJetsToLNu_Pt_100To250 = kreator.makeMCComponent("WJetsToLNu_Pt_100To250", "/WJetsToLNu_Pt-100To250_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root", 625.6)
WJetsToLNu_Pt_100To250_ext1 = kreator.makeMCComponent("WJetsToLNu_Pt_100To250_ext1", "/WJetsToLNu_Pt-100To250_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM", "CMS", ".*root", 625.6)
WJetsToLNu_Pt_100To250_ext4 = kreator.makeMCComponent("WJetsToLNu_Pt_100To250_ext4", "/WJetsToLNu_Pt-100To250_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext4-v1/MINIAODSIM", "CMS", ".*root", 625.6)
WJetsToLNu_Pt_250To400 = kreator.makeMCComponent("WJetsToLNu_Pt_250To400", "/WJetsToLNu_Pt-250To400_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root", 21.82)
WJetsToLNu_Pt_250To400_ext1 = kreator.makeMCComponent("WJetsToLNu_Pt_250To400_ext1", "/WJetsToLNu_Pt-250To400_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM", "CMS", ".*root", 21.82)
WJetsToLNu_Pt_250To400_ext4 = kreator.makeMCComponent("WJetsToLNu_Pt_250To400_ext4", "/WJetsToLNu_Pt-250To400_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext4-v1/MINIAODSIM", "CMS", ".*root", 21.82)
WJetsToLNu_Pt_400To600 = kreator.makeMCComponent("WJetsToLNu_Pt_400To600", "/WJetsToLNu_Pt-400To600_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root", 2.640)
WJetsToLNu_Pt_400To600_ext1 = kreator.makeMCComponent("WJetsToLNu_Pt_400To600_ext1", "/WJetsToLNu_Pt-400To600_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM", "CMS", ".*root", 2.640)
WJetsToLNu_Pt_600ToInf = kreator.makeMCComponent("WJetsToLNu_Pt_600ToInf", "/WJetsToLNu_Pt-600ToInf_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root", 0.4118)
WJetsToLNu_Pt_600ToInf_ext1 = kreator.makeMCComponent("WJetsToLNu_Pt_600ToInf_ext1", "/WJetsToLNu_Pt-600ToInf_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM", "CMS", ".*root", 0.4118)

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
GJets_HT40to100      = kreator.makeMCComponent("GJets_HT40to100"    , "/GJets_HT-40To100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root",20730)
GJets_HT40to100_ext  = kreator.makeMCComponent("GJets_HT40to100_ext", "/GJets_HT-40To100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM",  "CMS", ".*root",20730)
GJets_HT100to200     = kreator.makeMCComponent("GJets_HT100to200",    "/GJets_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root",9226)
GJets_HT100to200_ext = kreator.makeMCComponent("GJets_HT100to200_ext","/GJets_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM", "CMS", ".*root",9226)
GJets_HT200to400     = kreator.makeMCComponent("GJets_HT200to400",    "/GJets_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root",2300)
GJets_HT200to400_ext = kreator.makeMCComponent("GJets_HT200to400_ext","/GJets_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM", "CMS", ".*root",2300)
GJets_HT400to600     = kreator.makeMCComponent("GJets_HT400to600"    , "/GJets_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root",274.4)
GJets_HT400to600_ext = kreator.makeMCComponent("GJets_HT400to600_ext", "/GJets_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v2/MINIAODSIM",  "CMS", ".*root",274.4)
GJets_HT600toInf     = kreator.makeMCComponent("GJets_HT600toInf"    , "/GJets_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root",93.38)
GJets_HT600toInf_ext = kreator.makeMCComponent("GJets_HT600toInf_ext", "/GJets_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM",  "CMS", ".*root",93.38)

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


# NOTAVAILYET # GJets_DR04_HT100to200 = kreator.makeMCComponent("GJets_DR04_HT100to200", "/GJets_DR-0p4_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM", "CMS", ".*root", 4863.)
# NOTAVAILYET # GJets_DR04_HT200to400 = kreator.makeMCComponent("GJets_DR04_HT200to400", "/GJets_DR-0p4_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM", "CMS",".*root",1074.)
# NOTAVAILYET # GJets_DR04_HT400to600 = kreator.makeMCComponent("GJets_DR04_HT400to600", "/GJets_DR-0p4_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM", "CMS",".*root",1281.)
# NOTAVAILYET # GJets_DR04_HT600toInf = kreator.makeMCComponent("GJets_DR04_HT600toInf", "/GJets_DR-0p4_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM", "CMS",".*root",42.9)

GJetsDR04HT = [
# NOTAVAILYET # GJets_DR04_HT100to200,
# NOTAVAILYET # GJets_DR04_HT200to400,
# NOTAVAILYET # GJets_DR04_HT400to600,
# NOTAVAILYET # GJets_DR04_HT600toInf
]

# NOTAVAILYET # WJetsToQQ_HT180 = kreator.makeMCComponent("WJetsToQQ_HT180", "/WJetsToQQ_HT180_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM", "CMS",".*root", 3098.)
# NOTAVAILYET # WJetsToQQ_HT600toInf = kreator.makeMCComponent("WJetsToQQ_HT600toInf", "/WJetsToQQ_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM", "CMS",".*root", 98.4)
# NOTAVAILYET # DYJetsToQQ_HT180 = kreator.makeMCComponent("DYJetsToQQ_HT180", "/DYJetsToQQ_HT180_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM", "CMS",".*root", 1232.)
# NOTAVAILYET # ZJetsToQQ_HT600toInf = kreator.makeMCComponent("ZJetsToQQ_HT600toInf", "/ZJetsToQQ_HT600toInf_13TeV-madgraph/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM", "CMS",".*root", 581.9)

VJetsQQHT=[
# NOTAVAILYET # WJetsToQQ_HT180,
# NOTAVAILYET # WJetsToQQ_HT600toInf,
# NOTAVAILYET # DYJetsToQQ_HT180,
# NOTAVAILYET # ZJetsToQQ_HT600toInf
]

### Zinv
ZJetsToNuNu_HT100to200 = kreator.makeMCComponent("ZJetsToNuNu_HT100to200", "/ZJetsToNuNu_HT-100To200_13TeV-madgraph/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root",280.47*1.23)
ZJetsToNuNu_HT100to200_ext = kreator.makeMCComponent("ZJetsToNuNu_HT100to200_ext", "/ZJetsToNuNu_HT-100To200_13TeV-madgraph/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM", "CMS", ".*root",280.47*1.23)
ZJetsToNuNu_HT200to400 = kreator.makeMCComponent("ZJetsToNuNu_HT200to400", "/ZJetsToNuNu_HT-200To400_13TeV-madgraph/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root",78.36*1.23) 
# NOTAVAILYET # ZJetsToNuNu_HT200to400_ext = kreator.makeMCComponent("ZJetsToNuNu_HT200to400_ext", "/ZJetsToNuNu_HT-200To400_13TeV-madgraph/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1/MINIAODSIM", "CMS", ".*root",78.36*1.23)
# NOTAVAILYET # ZJetsToNuNu_HT400to600 = kreator.makeMCComponent("ZJetsToNuNu_HT400to600", "/ZJetsToNuNu_HT-400To600_13TeV-madgraph/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM", "CMS", ".*root",10.94*1.23) 
ZJetsToNuNu_HT400to600_ext = kreator.makeMCComponent("ZJetsToNuNu_HT400to600_ext", "/ZJetsToNuNu_HT-400To600_13TeV-madgraph/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM", "CMS", ".*root",10.94*1.23)
ZJetsToNuNu_HT600to800 = kreator.makeMCComponent("ZJetsToNuNu_HT600to800", "/ZJetsToNuNu_HT-600To800_13TeV-madgraph/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root",3.221*1.23)
# NOTAVAILYET # ZJetsToNuNu_HT800to1200 = kreator.makeMCComponent("ZJetsToNuNu_HT800t1200", "/ZJetsToNuNu_HT-800To1200_13TeV-madgraph/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v3/MINIAODSIM", "CMS", ".*root",1.474*1.23)
ZJetsToNuNu_HT1200to2500 = kreator.makeMCComponent("ZJetsToNuNu_HT1200to2500", "/ZJetsToNuNu_HT-1200To2500_13TeV-madgraph/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root",0.3586*1.23 )
ZJetsToNuNu_HT1200to2500_ext = kreator.makeMCComponent("ZJetsToNuNu_HT1200to2500_ext", "/ZJetsToNuNu_HT-1200To2500_13TeV-madgraph/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM", "CMS", ".*root",0.3586*1.23 )
ZJetsToNuNu_HT2500toInf = kreator.makeMCComponent("ZJetsToNuNu_HT2500toInf", "/ZJetsToNuNu_HT-2500ToInf_13TeV-madgraph/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root",0.008203*1.23)

ZJetsToNuNuHT = [
ZJetsToNuNu_HT100to200,
ZJetsToNuNu_HT100to200_ext,
ZJetsToNuNu_HT200to400,
# NOTAVAILYET # ZJetsToNuNu_HT200to400_ext,
# NOTAVAILYET # ZJetsToNuNu_HT400to600,
ZJetsToNuNu_HT400to600_ext,
ZJetsToNuNu_HT600to800,
# NOTAVAILYET # ZJetsToNuNu_HT800to1200,
#ZJetsToNuNu_HT800to1200ext,
ZJetsToNuNu_HT1200to2500,
ZJetsToNuNu_HT1200to2500_ext,
ZJetsToNuNu_HT2500toInf,
#ZJetsToNuNu_HT2500toInf_ext,
]

### QCD

## missing xsec QCD_Pt5to10      = kreator.makeMCComponent("QCD_Pt5to10"      , "/QCD_Pt_5to10_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM"      , "CMS" , ".*root" , )
#QCD_Pt10to15     = kreator.makeMCComponent("QCD_Pt10to15"     , "/QCD_Pt_10to15_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM"     , "CMS" , ".*root" , 5887580000)
QCD_Pt15to30          = kreator.makeMCComponent("QCD_Pt15to30"     , "/QCD_Pt_15to30_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM"     , "CMS" , ".*root" , 1837410000)
QCD_Pt30to50          = kreator.makeMCComponent("QCD_Pt30to50"         , "/QCD_Pt_30to50_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM"      , "CMS" , ".*root" , 140932000)
QCD_Pt50to80          = kreator.makeMCComponent("QCD_Pt50to80"         , "/QCD_Pt_50to80_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root", 19204300)
QCD_Pt80to120         = kreator.makeMCComponent("QCD_Pt80to120"        , "/QCD_Pt_80to120_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root", 2762530)
QCD_Pt80to120_ext2    = kreator.makeMCComponent("QCD_Pt80to120_ext2"   , "/QCD_Pt_80to120_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v1/MINIAODSIM", "CMS", ".*root", 2762530)
QCD_Pt120to170        = kreator.makeMCComponent("QCD_Pt120to170"       , "/QCD_Pt_120to170_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM"   , "CMS" , ".*root" , 471100)
QCD_Pt120to170_ext    = kreator.makeMCComponent("QCD_Pt120to170_ext"   , "/QCD_Pt_120to170_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM",    "CMS" , ".*root" , 471100)
QCD_Pt170to300        = kreator.makeMCComponent("QCD_Pt170to300"       , "/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM"   , "CMS" , ".*root" , 117276)
QCD_Pt170to300_ext    = kreator.makeMCComponent("QCD_Pt170to300_ext"   , "/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM"   , "CMS" , ".*root" , 117276)

#QCD_Pt300to470   = kreator.makeMCComponent("QCD_Pt300to470",  "/QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM", "CMS", ".*root", 7823)
#QCD_Pt470to600   = kreator.makeMCComponent("QCD_Pt470to600",  "/QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM", "CMS", ".*root", 648.2)
#QCD_Pt600to800   = kreator.makeMCComponent("QCD_Pt600to800"   , "/QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM"   , "CMS" , ".*root" , 186.9)
#QCD_Pt800to1000  = kreator.makeMCComponent("QCD_Pt800to1000"  , "/QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM"  , "CMS" , ".*root" , 32.293)

#QCD_Pt1000to1400 = kreator.makeMCComponent("QCD_Pt1000to1400" , "/QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM" , "CMS" , ".*root" , 9.4183)
#QCD_Pt1400to1800 = kreator.makeMCComponent("QCD_Pt1400to1800" , "/QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM" , "CMS" , ".*root" , 0.84265)
#QCD_Pt1800to2400 = kreator.makeMCComponent("QCD_Pt1800to2400" , "/QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM" , "CMS" , ".*root" , 0.114943)
#QCD_Pt2400to3200 = kreator.makeMCComponent("QCD_Pt2400to3200" , "/QCD_Pt_2400to3200_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM" , "CMS" , ".*root" , 0.00682981)
#QCD_Pt3200toInf  = kreator.makeMCComponent("QCD_Pt3200"       , "/QCD_Pt_3200toInf_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM"  , "CMS" , ".*root" , 0.000165445)

QCDPt = [
#QCD_Pt10to15,
QCD_Pt15to30,
QCD_Pt30to50,
QCD_Pt50to80,
QCD_Pt80to120,
QCD_Pt80to120_ext2,
QCD_Pt120to170,
QCD_Pt120to170_ext,
QCD_Pt170to300,
QCD_Pt170to300_ext,
#QCD_Pt300to470,
#QCD_Pt470to600,
#QCD_Pt600to800,
#QCD_Pt800to1000,
#QCD_Pt1000to1400,
#QCD_Pt1400to1800,
#QCD_Pt1800to2400,
#QCD_Pt2400to3200,
#QCD_Pt3200toInf
]



# qcd muenr
QCD_Mu15 = kreator.makeMCComponent("QCD_Mu15", "/QCD_Pt-20toInf_MuEnrichedPt15_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root", 720.65e6*0.00042)
QCD_Pt15to20_Mu5    = kreator.makeMCComponent("QCD_Pt15to20_Mu5"    , "/QCD_Pt-15to20_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM"       , "CMS" , ".*root" , 1273190000*0.003)
QCD_Pt20to30_Mu5    = kreator.makeMCComponent("QCD_Pt20to30_Mu5"    , "/QCD_Pt-20to30_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM"      , "CMS" , ".*root" , 558528000*0.0053)
QCD_Pt30to50_Mu5    = kreator.makeMCComponent("QCD_Pt30to50_Mu5", "/QCD_Pt-30to50_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root", 139803000*0.01182)
QCD_Pt50to80_Mu5    = kreator.makeMCComponent("QCD_Pt50to80_Mu5"    , "/QCD_Pt-50to80_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM" , "CMS" , ".*root" , 19222500*0.02276)
QCD_Pt80to120_Mu5   = kreator.makeMCComponent("QCD_Pt80to120_Mu5"   , "/QCD_Pt-80to120_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM"     , "CMS" , ".*root" , 2758420*0.03844)
QCD_Pt80to120_Mu5_ext   = kreator.makeMCComponent("QCD_Pt80to120_Mu5_ext"   , "/QCD_Pt-80to120_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v3/MINIAODSIM"     , "CMS" , ".*root" , 2758420*0.03844)
QCD_Pt120to170_Mu5  = kreator.makeMCComponent("QCD_Pt120to170_Mu5"  , "/QCD_Pt-120to170_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS" , ".*root" , 469797*0.05362)
QCD_Pt170to300_Mu5  = kreator.makeMCComponent("QCD_Pt170to300_Mu5", "/QCD_Pt-170to300_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root", 117989*0.07335)
QCD_Pt170to300_Mu5_ext  = kreator.makeMCComponent("QCD_Pt170to300_Mu5_ext", "/QCD_Pt-170to300_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM", "CMS", ".*root", 117989*0.07335)
QCD_Pt300to470_Mu5  = kreator.makeMCComponent("QCD_Pt300to470_Mu5"  , "/QCD_Pt-300to470_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM"    , "CMS" , ".*root" , 7820.25*0.10196)
QCD_Pt300to470_Mu5_ext  = kreator.makeMCComponent("QCD_Pt300to470_Mu5_ext"  , "/QCD_Pt-300to470_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM"    , "CMS" , ".*root" , 7820.25*0.10196)
QCD_Pt300to470_Mu5_ext2  = kreator.makeMCComponent("QCD_Pt300to470_Mu5_ext2"  , "/QCD_Pt-300to470_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v1/MINIAODSIM"    , "CMS" , ".*root" , 7820.25*0.10196)
QCD_Pt470to600_Mu5  = kreator.makeMCComponent("QCD_Pt470to600_Mu5"  , "/QCD_Pt-470to600_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM"    , "CMS" , ".*root" , 645.528*0.12242)
QCD_Pt470to600_Mu5_ext  = kreator.makeMCComponent("QCD_Pt470to600_Mu5_ext"  , "/QCD_Pt-470to600_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM"    , "CMS" , ".*root" , 645.528*0.12242)
QCD_Pt470to600_Mu5_ext2  = kreator.makeMCComponent("QCD_Pt470to600_Mu5_ext2"  , "/QCD_Pt-470to600_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v1/MINIAODSIM"    , "CMS" , ".*root" , 645.528*0.12242)
QCD_Pt600to800_Mu5  = kreator.makeMCComponent("QCD_Pt600to800_Mu5", "/QCD_Pt-600to800_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root", 187.109*0.13412)
QCD_Pt600to800_Mu5_ext  = kreator.makeMCComponent("QCD_Pt600to800_Mu5_ext", "/QCD_Pt-600to800_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM", "CMS", ".*root", 187.109*0.13412)
QCD_Pt800to1000_Mu5 = kreator.makeMCComponent("QCD_Pt800to1000_Mu5" , "/QCD_Pt-800to1000_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM"   , "CMS" , ".*root" , 32.3486*0.14552)
QCD_Pt800to1000_Mu5_ext = kreator.makeMCComponent("QCD_Pt800to1000_Mu5_ext" , "/QCD_Pt-800to1000_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM"   , "CMS" , ".*root" , 32.3486*0.14552)
QCD_Pt800to1000_Mu5_ext2 = kreator.makeMCComponent("QCD_Pt800to1000_Mu5_ext2" , "/QCD_Pt-800to1000_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v1/MINIAODSIM"   , "CMS" , ".*root" , 32.3486*0.14552)
QCD_Pt1000toInf_Mu5 = kreator.makeMCComponent("QCD_Pt1000toInf_Mu5" , "/QCD_Pt-1000toInf_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM"   , "CMS" , ".*root" , 10.4305*0.15544)
QCD_Pt1000toInf_Mu5_ext = kreator.makeMCComponent("QCD_Pt1000toInf_Mu5_ext" , "/QCD_Pt-1000toInf_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v3/MINIAODSIM"   , "CMS" , ".*root" , 10.4305*0.15544)

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
#QCD_Pt15to20_EMEnriched   = kreator.makeMCComponent("QCD_Pt15to20_EMEnriched"  ,"/QCD_Pt-15to20_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM"  , "CMS", ".*root", 1273000000*0.0002)
QCD_Pt20to30_EMEnriched   = kreator.makeMCComponent("QCD_Pt20to30_EMEnriched"  ,"/QCD_Pt-20to30_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM"  , "CMS", ".*root", 557600000*0.0096)
QCD_Pt30to50_EMEnriched   = kreator.makeMCComponent("QCD_Pt30to50_EMEnriched"  ,"/QCD_Pt-30to50_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM"  , "CMS", ".*root", 136000000*0.073)
QCD_Pt30to50_EMEnriched_ext   = kreator.makeMCComponent("QCD_Pt30to50_EMEnriched_ext"  ,"/QCD_Pt-30to50_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM"  , "CMS", ".*root", 136000000*0.073)
QCD_Pt50to80_EMEnriched_ext   = kreator.makeMCComponent("QCD_Pt50to80_EMEnriched_ext", "/QCD_Pt-50to80_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM", "CMS", ".*root", 19800000*0.146)
QCD_Pt80to120_EMEnriched_ext  = kreator.makeMCComponent("QCD_Pt80to120_EMEnriched_ext" ,"/QCD_Pt-80to120_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM" , "CMS", ".*root", 2800000*0.125)
QCD_Pt120to170_EMEnriched = kreator.makeMCComponent("QCD_Pt120to170_EMEnriched","/QCD_Pt-120to170_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root", 477000*0.132)
QCD_Pt170to300_EMEnriched = kreator.makeMCComponent("QCD_Pt170to300_EMEnriched","/QCD_Pt-170to300_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root", 114000*0.165)
QCD_Pt300toInf_EMEnriched = kreator.makeMCComponent("QCD_Pt300toInf_EMEnriched","/QCD_Pt-300toInf_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root", 9000*0.15)

QCDPtEMEnriched = [
#QCD_Pt15to20_EMEnriched,
QCD_Pt20to30_EMEnriched,
QCD_Pt30to50_EMEnriched,
QCD_Pt30to50_EMEnriched_ext,
QCD_Pt50to80_EMEnriched_ext,
QCD_Pt80to120_EMEnriched_ext,
QCD_Pt120to170_EMEnriched,
QCD_Pt170to300_EMEnriched,
QCD_Pt300toInf_EMEnriched
]

# qcd bctoe

##QCD_Pt_15to20_bcToE   = kreator.makeMCComponent("QCD_Pt_15to20_bcToE"   , "/QCD_Pt_15to20_bcToE_TuneCUETP8M1_13TeV_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM"  , "CMS" , ".*root" , 1272980000*0.0002)
QCD_Pt_20to30_bcToE   = kreator.makeMCComponent("QCD_Pt_20to30_bcToE"   , "/QCD_Pt_20to30_bcToE_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM"  , "CMS" , ".*root" , 557627000*0.00059)
QCD_Pt_30to80_bcToE   = kreator.makeMCComponent("QCD_Pt_30to80_bcToE"   , "/QCD_Pt_30to80_bcToE_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM"  , "CMS" , ".*root" , 159068000*0.00255)
QCD_Pt_80to170_bcToE  = kreator.makeMCComponent("QCD_Pt_80to170_bcToE"  , "/QCD_Pt_80to170_bcToE_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_backup_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM" , "CMS" , ".*root" , 3221000*0.01183)
QCD_Pt_170to250_bcToE = kreator.makeMCComponent("QCD_Pt_170to250_bcToE" , "/QCD_Pt_170to250_bcToE_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root", 105771*0.02492)
QCD_Pt_250toInf_bcToE = kreator.makeMCComponent("QCD_Pt_250toInf_bcToE" , "/QCD_Pt_250toInf_bcToE_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS" , ".*root" , 21094.1*0.03375)

QCDPtbcToE = [
##QCD_Pt_15to20_bcToE,
QCD_Pt_20to30_bcToE,
QCD_Pt_30to80_bcToE,
QCD_Pt_80to170_bcToE,
QCD_Pt_170to250_bcToE,
QCD_Pt_250toInf_bcToE
]

# QCD HT bins (cross sections from McM)
QCD_HT100to200 = kreator.makeMCComponent("QCD_HT100to200", "/QCD_HT100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root", 2.785*10**7)
QCD_HT200to300 = kreator.makeMCComponent("QCD_HT200to300", "/QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root",1717000)
QCD_HT200to300_ext = kreator.makeMCComponent("QCD_HT200to300_ext", "/QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM", "CMS", ".*root",1717000)
QCD_HT300to500 = kreator.makeMCComponent("QCD_HT300to500", "/QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root",351300)
QCD_HT300to500_ext = kreator.makeMCComponent("QCD_HT300to500_ext", "/QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM", "CMS", ".*root",351300)
QCD_HT500to700 = kreator.makeMCComponent("QCD_HT500to700", "/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root",31630)
QCD_HT500to700_ext = kreator.makeMCComponent("QCD_HT500to700_ext", "/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v2/MINIAODSIM", "CMS", ".*root",31630)
QCD_HT700to1000 = kreator.makeMCComponent("QCD_HT700to1000", "/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root",6802)
QCD_HT700to1000_ext = kreator.makeMCComponent("QCD_HT700to1000_ext", "/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM", "CMS", ".*root",6802)
QCD_HT1000to1500 = kreator.makeMCComponent("QCD_HT1000to1500", "/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root",1206)
QCD_HT1000to1500_ext = kreator.makeMCComponent("QCD_HT1000to1500_ext", "/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM", "CMS", ".*root",1206)
QCD_HT1500to2000 = kreator.makeMCComponent("QCD_HT1500to2000", "/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root",120.4)
QCD_HT1500to2000_ext = kreator.makeMCComponent("QCD_HT1500to2000_ext", "/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM", "CMS", ".*root",120.4)
QCD_HT2000toInf = kreator.makeMCComponent("QCD_HT2000toInf", "/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root",25.25)
QCD_HT2000toInf_ext = kreator.makeMCComponent("QCD_HT2000toInf_ext", "/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM", "CMS", ".*root",25.25)


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

WWTo2L2Nu = kreator.makeMCComponent("WWTo2L2Nu", "/WWTo2L2Nu_13TeV-powheg/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root", 10.481 )
WWToLNuQQ = kreator.makeMCComponent("WWToLNuQQ", "/WWToLNuQQ_13TeV-powheg/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root", 43.53 )
WWToLNuQQ_ext = kreator.makeMCComponent("WWToLNuQQ_ext", "/WWToLNuQQ_13TeV-powheg/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM", "CMS", ".*root", 43.53 )
WWTo1L1Nu2Q = kreator.makeMCComponent("WWTo1L1Nu2Q", "/WWTo1L1Nu2Q_13TeV_amcatnloFXFX_madspin_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root", 49.997 )

ZZTo2L2Nu = kreator.makeMCComponent("ZZTo2L2Nu", "/ZZTo2L2Nu_13TeV_powheg_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root", 0.564)
ZZTo2L2Q = kreator.makeMCComponent("ZZTo2L2Q", "/ZZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root",  3.28)
ZZTo2Q2Nu = kreator.makeMCComponent("ZZTo2Q2Nu", "/ZZTo2Q2Nu_13TeV_amcatnloFXFX_madspin_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root",  4.04)
ZZTo4L = kreator.makeMCComponent("ZZTo4L", "/ZZTo4L_13TeV_powheg_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root", 1.256)

#ZZTo4L_amcatnlo = kreator.makeMCComponent("ZZTo4L_amcatnlo", "/ZZTo4L_13TeV-amcatnloFXFX-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM", "CMS", ".*root", 1.212)

WZJToLLLNu =  kreator.makeMCComponent("WZJToLLLNu"  , "/WZJToLLLNu_TuneCUETP8M1_13TeV-amcnlo-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM"  , "CMS", ".*root", 4.708 )
WZTo1L3Nu   = kreator.makeMCComponent("WZTo1L3Nu"  , "/WZTo1L3Nu_13TeV_amcatnloFXFX_madspin_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM"  , "CMS", ".*root", (47.13)*(3*0.108)*(0.2) )
WZTo1L1Nu2Q = kreator.makeMCComponent("WZTo1L1Nu2Q", "/WZTo1L1Nu2Q_13TeV_amcatnloFXFX_madspin_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v3/MINIAODSIM", "CMS", ".*root",  10.71)
WZTo2L2Q    = kreator.makeMCComponent("WZTo2L2Q"   , "/WZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM"   , "CMS", ".*root",  5.60)
WZTo3LNu    = kreator.makeMCComponent("WZTo3LNu"   , "/WZTo3LNu_TuneCUETP8M1_13TeV-powheg-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root", 4.42965)
WZTo3LNu_amcatnlo = kreator.makeMCComponent("WZTo3LNu_amcatnlo", "/WZTo3LNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root", 4.666)

VVTo2L2Nu = kreator.makeMCComponent("VVTo2L2Nu","/VVTo2L2Nu_13TeV_amcatnloFXFX_madspin_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root",  11.95)
VVTo2L2Nu_ext = kreator.makeMCComponent("VVTo2L2Nu_ext" ,"/VVTo2L2Nu_13TeV_amcatnloFXFX_madspin_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM", "CMS", ".*root",  11.95)

WGJets = kreator.makeMCComponent("WGJets", "/WGJets_MonoPhoton_PtG-130_TuneCUETP8M1_13TeV-madgraph/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root", 0.6637)
WGToLNuG = kreator.makeMCComponent("WGToLNuG", "/WGToLNuG_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root", 585.8)
WGToLNuG_amcatnlo_ext = kreator.makeMCComponent("WGToLNuG_amcatnlo_ext", "/WGToLNuG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM", "CMS", ".*root", 585.8) # cross section copied from MLM sample above, to be checked
WGToLNuG_amcatnlo_ext2 = kreator.makeMCComponent("WGToLNuG_amcatnlo_ext2", "/WGToLNuG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v1/MINIAODSIM", "CMS", ".*root", 585.8) # cross section copied from MLM sample above, to be checked

ZGJets = kreator.makeMCComponent("ZGJets", "/ZNuNuGJets_MonoPhoton_PtG-130_TuneCUETP8M1_13TeV-madgraph/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root", 0.1903)
ZNuNuGJets_40130 = kreator.makeMCComponent("ZNuNuGJets_40130", "/ZNuNuGJets_MonoPhoton_PtG-40to130_TuneCUETP8M1_13TeV-madgraph/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root",2.816)

ZGTo2NuG = kreator.makeMCComponent("ZGTo2NuG","/ZGTo2NuG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root",28.05)
ZGTo2LG_ext = kreator.makeMCComponent("ZGTo2LG_ext", "/ZGTo2LG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM", "CMS", ".*root", 131.3)

#ZLLGJets_pt130 = kreator.makeMCComponent("ZLLGJets", "/ZLLGJets_MonoPhoton_PtG-130_TuneCUETP8M1_13TeV-madgraph/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM", "CMS", ".*root", ?????)

WWDoubleTo2L = kreator.makeMCComponent("WWDoubleTo2L", "/WWTo2L2Nu_DoubleScattering_13TeV-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root", 0.1729)
WpWpJJ = kreator.makeMCComponent("WpWpJJ", "/WpWpJJ_EWK-QCD_TuneCUETP8M1_13TeV-madgraph-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root", 0.03711)

WW = kreator.makeMCComponent("WW", "/WW_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root", 63.21 * 1.82)
WW_ext = kreator.makeMCComponent("WW_ext", "/WW_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM", "CMS", ".*root", 63.21 * 1.82)
WZ = kreator.makeMCComponent("WZ", "/WZ_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root", 47.13 )
WZ_ext = kreator.makeMCComponent("WZ_ext", "/WZ_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM", "CMS", ".*root", 47.13 )
ZZ = kreator.makeMCComponent("ZZ", "/ZZ_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root", 16.523 )
ZZ_ext = kreator.makeMCComponent("ZZ_ext", "/ZZ_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM", "CMS", ".*root", 16.523 )

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
WZTo1L3Nu,
WZTo1L1Nu2Q,
WZTo2L2Q,
WZTo3LNu,
WZTo3LNu_amcatnlo,
VVTo2L2Nu,
VVTo2L2Nu_ext,
WGToLNuG,
WGToLNuG_amcatnlo_ext,
WGToLNuG_amcatnlo_ext2,
WGJets,
ZGJets,
ZNuNuGJets_40130,
ZGTo2NuG,
ZGTo2LG_ext,
#ZLLGJets_pt130,
WWDoubleTo2L,
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
WWW = kreator.makeMCComponent("WWW", "/WWW_4F_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root", 0.2086)
WWZ = kreator.makeMCComponent("WWZ", "/WWZ_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root",  0.1651 )
WZZ = kreator.makeMCComponent("WZZ", "/WZZ_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root",  0.05565 )
ZZZ = kreator.makeMCComponent("ZZZ", "/ZZZ_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root",  0.01398 )

TriBosons = [
WWW,
WZZ,
WWZ,
ZZZ,
]

### TTV
TTWToLNu_ext = kreator.makeMCComponent("TTWToLNu_ext", "/TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v3/MINIAODSIM", "CMS", ".*root", 0.2043)
TTWToLNu_ext2 = kreator.makeMCComponent("TTWToLNu_ext2", "/TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v1/MINIAODSIM", "CMS", ".*root", 0.2043)
TTWToQQ = kreator.makeMCComponent("TTWToQQ", "/TTWJetsToQQ_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root", 0.40620)
TTW_LO = kreator.makeMCComponent("TTW_LO", "/ttWJets_13TeV_madgraphMLM/RunIISummer16MiniAODv2-80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root",  0.6105 )
TTZToQQ = kreator.makeMCComponent("TTZToQQ","/TTZToQQ_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root", 0.5297)
TTZToLLNuNu_ext     = kreator.makeMCComponent("TTZToLLNuNu_ext", "/TTZToLLNuNu_M-10_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM", "CMS", ".*root", 0.2529)
TTZToLLNuNu_m1to10  = kreator.makeMCComponent("TTZToLLNuNu_m1to10","/TTZToLL_M-1to10_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root", 0.0493)
# https://twiki.cern.ch/twiki/bin/view/CMS/SameSignDilepton2016
TTZ_LO = kreator.makeMCComponent("TTZ_LO", "/ttZJets_13TeV_madgraphMLM/RunIISummer16MiniAODv2-80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root",  0.5297/0.692)
TTGJets     = kreator.makeMCComponent("TTGJets",    "/TTGJets_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root", 3.697)
TTGJets_ext = kreator.makeMCComponent("TTGJets_ext","/TTGJets_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM", "CMS", ".*root", 3.697)

TTV = [
TTWToLNu_ext,
TTWToLNu_ext2,
TTWToQQ,
TTW_LO,
TTZToQQ,
TTZToLLNuNu_ext,
TTZToLLNuNu_m1to10,
TTZ_LO,
TTGJets,
TTGJets_ext
]

### Rares
TTTT = kreator.makeMCComponent("TTTT", "/TTTT_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root", 0.009103)
# NOTAVAILYET # TTTT_ext = kreator.makeMCComponent("TTTT_ext", "/TTTT_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1/MINIAODSIM", "CMS", ".*root", 0.009103)
TTWWTo2LSS2Nu_LO = kreator.makeMCComponentFromEOS("TTWWTo2LSS2Nu_LO","/ttWW_lo/","/store/cmst3/group/tthlep/gpetrucc/prod/%s/MINIAODSIM",".*root",0.011500*0.2002)

Rares = [
TTTT,
# NOTAVAILYET # TTTT_ext,
TTWWTo2LSS2Nu_LO,
]

# NOTAVAILYET # TChiSlepSnu=kreator.makeMCComponent("TChiSlepSnu","/SMS-TChiSlepSnu_x0p5_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16Fast_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM","CMS",".*root",1)
# NOTAVAILYET # T1tttt_2016     =kreator.makeMCComponent("T1tttt_2016", "/SMS-T1tttt_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16Fast_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM","CMS",".*root",1)
# NOTAVAILYET # T5qqqqVV_2016=kreator.makeMCComponent("T5qqqqVV_2016", "/SMS-T5qqqqVV_dM20_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16Fast_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM","CMS",".*root",1)

### EWK V+jets 
# NOTAVAILYET # EWKWMinus2Jets = kreator.makeMCComponent("EWKWMinus2Jets", "/EWKWMinus2Jets_WToLNu_M-50_13TeV-madgraph-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v2/MINIAODSIM", "CMS", ".*root", 20.36)
EWKWPlus2Jets = kreator.makeMCComponent("EWKWPlus2Jets", "/EWKWPlus2Jets_WToLNu_M-50_13TeV-madgraph-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root", 25.82)
EWKZToLL2Jets = kreator.makeMCComponent("EWKZToLL2Jets", "/EWKZ2Jets_ZToLL_M-50_13TeV-madgraph-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root", 3.998)
EWKZToNuNu2Jets = kreator.makeMCComponent("EWKZToNuNu2Jets", "/EWKZ2Jets_ZToNuNu_13TeV-madgraph-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root", 10.14)

EWKV2Jets = [
# NOTAVAILYET # EWKWMinus2Jets,
EWKWPlus2Jets,
EWKZToLL2Jets,
EWKZToNuNu2Jets,
]

### ----------------------------- summary ----------------------------------------

mcSamples = TTs + SingleTop + VJets + DYJetsM50HT + DYJetsM5to50HT + DYNJets + WJetsToLNuHT + WJetsToLNuPT + WNJets + GJetsHT + ZJetsToNuNuHT + QCDHT + QCDPtbcToE + QCDPt + QCDPtEMEnriched + [QCD_Mu15] + QCD_Mu5 +  DiBosons + TriBosons + TTV + Higgs + Rares + EWKV2Jets # + [TChiSlepSnu,T1tttt_2016,T5qqqqVV_2016]

samples = mcSamples

### ---------------------------------------------------------------------

from CMGTools.TTHAnalysis.setup.Efficiencies import *
dataDir = "$CMSSW_BASE/src/CMGTools/TTHAnalysis/data"

#Define splitting
for comp in mcSamples:
    comp.isMC = True
    comp.isData = False
    comp.splitFactor = 250 #  if comp.name in [ "WJets", "DY3JetsM50", "DY4JetsM50","W1Jets","W2Jets","W3Jets","W4Jets","TTJetsHad" ] else 100
    comp.puFileMC=dataDir+"/puProfile_Summer12_53X.root"
    comp.puFileData=dataDir+"/puProfile_Data12.root"
    comp.efficiency = eff2012

if __name__ == "__main__":
    from CMGTools.RootTools.samples.tools import runMain
    runMain(samples,localobjs=locals())
