import PhysicsTools.HeppyCore.framework.config as cfg
import os

#####COMPONENT CREATOR
from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()

### common MC samples
from CMGTools.RootTools.samples.samples_13TeV_RunIISpring16MiniAODv2 import *
### --- mc ---

# --- 25 ns background samples ---
ZJetsToNuNu_MJ = ZJetsToNuNuHT
VJets_MJ       = WJetsToLNuHT + DYJetsM50HT
#Top_MJ          = [ TTJets, TToLeptons_tch_amcatnlo, TToLeptons_tch_amcatnlo_ext, TBar_tWch, T_tWch ]
Top_MJ         = [ TTJets, TToLeptons_sch_amcatnlo, TBar_tWch, T_tWch ]
DiBosons_MJ    = [ WW, WZ, ZZ ]

#diboson analysis samples
TTBar          = [ TT_pow_ext3 ]
WJetsToLNu_HT     = [ WJetsToLNu_HT100to200, WJetsToLNu_HT200to400, WJetsToLNu_HT400to600, WJetsToLNu_HT600to800, WJetsToLNu_HT800to1200_ext, WJetsToLNu_HT1200to2500, WJetsToLNu_HT2500toInf ]
SingleTop      = [ TToLeptons_sch_amcatnlo, TBar_tWch, T_tWch ]

#V+gamma samples
from CMGTools.MonoXAnalysis.samples.samples_13TeV_VJETS_RunIISpring16MiniAODv2 import *
TTBar_amcatnlo = [ TTJets ]
TTGammaJets    = [ TTGJets ]
WJetsToLNu_amcatnlo = [ WJetsToLNu ]
#QCD = QCDHT
GammaJets = GJets
VV_VBosonGamma = VV_VGamma

mcSamples_monojet_Asymptotic25ns = ZJetsToNuNu_MJ + VJets_MJ + Top_MJ + DiBosons_MJ + GJetsHT + EWKV2Jets
mcSamples_diboson_Asymptotic25ns = TTBar #SingleTop + WJetsToLNu_HT + DiBosons_MJ# + TTBar
mcSamples_zgamma_Asymptotic25ns = TTBar_amcatnlo + WJetsToLNu_amcatnlo + QCDHT + GJetsHT + VV_VBosonGamma + TTGammaJets
mcSamples_zgamma_Signal = VGamma_signal

### ----------------------------- summary ----------------------------------------     
mcSamples_monojet = mcSamples_monojet_Asymptotic25ns
mcSamples_diboson = mcSamples_diboson_Asymptotic25ns
mcSamples_zgamma = mcSamples_zgamma_Signal

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
# for comp in dataSamples:
#     comp.splitFactor = 1000
#     comp.isMC = False
#     comp.isData = True


if __name__ == "__main__":
   import sys
   if "test" in sys.argv:
       from CMGTools.RootTools.samples.ComponentCreator import testSamples
       testSamples(mcSamples)
