import PhysicsTools.HeppyCore.framework.config as cfg
import os

#####COMPONENT CREATOR
from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()

### Higgs invisible
# VBF production
VBF_HToInvisible_M110 = kreator.makeMCComponent("VBF_HToInvisible_M110","/VBF_HToInvisible_M110_13TeV_powheg_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM", "CMS", ".*root", 4.434)
VBF_HToInvisible_M125 = kreator.makeMCComponent("VBF_HToInvisible_M125","/VBF_HToInvisible_M125_13TeV_powheg_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM", "CMS", ".*root", 3.782)
VBF_HToInvisible_M150 = kreator.makeMCComponent("VBF_HToInvisible_M150","/VBF_HToInvisible_M150_13TeV_powheg_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM", "CMS", ".*root", 3.239)
VBF_HToInvisible_M200 = kreator.makeMCComponent("VBF_HToInvisible_M200","/VBF_HToInvisible_M200_13TeV_powheg_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM", "CMS", ".*root", 2.282)
VBF_HToInvisible_M300 = kreator.makeMCComponent("VBF_HToInvisible_M300","/VBF_HToInvisible_M300_13TeV_powheg_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM", "CMS", ".*root", 1.256)
VBF_HToInvisible_M400 = kreator.makeMCComponent("VBF_HToInvisible_M400","/VBF_HToInvisible_M400_13TeV_powheg_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM", "CMS", ".*root", 0.758)
VBF_HToInvisible_M500 = kreator.makeMCComponent("VBF_HToInvisible_M500","/VBF_HToInvisible_M500_13TeV_powheg_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM", "CMS", ".*root", 0.487)
VBF_HToInvisible_M600 = kreator.makeMCComponent("VBF_HToInvisible_M600","/VBF_HToInvisible_M600_13TeV_powheg_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM", "CMS", ".*root", 0.327)
VBF_HToInvisible_M800 = kreator.makeMCComponent("VBF_HToInvisible_M800","/VBF_HToInvisible_M800_13TeV_powheg_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM", "CMS", ".*root", 0.1622)

VBF_HToInvisible = [
VBF_HToInvisible_M110,
VBF_HToInvisible_M125,
VBF_HToInvisible_M150,
VBF_HToInvisible_M200,
VBF_HToInvisible_M300,
VBF_HToInvisible_M400,
VBF_HToInvisible_M500,
VBF_HToInvisible_M600,
VBF_HToInvisible_M800,
]


# Gluon Fusion
GluGlu_HToInvisible_M110 = kreator.makeMCComponent("GluGlu_HToInvisible_M110","/GluGlu_HToInvisible_M110_13TeV_powheg_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM", "CMS", ".*root", 55.07)
GluGlu_HToInvisible_M125 = kreator.makeMCComponent("GluGlu_HToInvisible_M125","/GluGlu_HToInvisible_M125_13TeV_powheg_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM", "CMS", ".*root", 44.14)
GluGlu_HToInvisible_M150 = kreator.makeMCComponent("GluGlu_HToInvisible_M150","/GluGlu_HToInvisible_M150_13TeV_powheg_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM", "CMS", ".*root", 32.10)
GluGlu_HToInvisible_M200 = kreator.makeMCComponent("GluGlu_HToInvisible_M200","/GluGlu_HToInvisible_M200_13TeV_powheg_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM", "CMS", ".*root", 18.12)
GluGlu_HToInvisible_M300 = kreator.makeMCComponent("GluGlu_HToInvisible_M300","/GluGlu_HToInvisible_M300_13TeV_powheg_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM", "CMS", ".*root", 9.823)
GluGlu_HToInvisible_M400 = kreator.makeMCComponent("GluGlu_HToInvisible_M400","/GluGlu_HToInvisible_M400_13TeV_powheg_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM", "CMS", ".*root", 9.516)
GluGlu_HToInvisible_M500 = kreator.makeMCComponent("GluGlu_HToInvisible_M500","/GluGlu_HToInvisible_M500_13TeV_powheg_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM", "CMS", ".*root", 4.538)
GluGlu_HToInvisible_M600 = kreator.makeMCComponent("GluGlu_HToInvisible_M600","/GluGlu_HToInvisible_M600_13TeV_powheg_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM", "CMS", ".*root", 2.005)
GluGlu_HToInvisible_M800 = kreator.makeMCComponent("GluGlu_HToInvisible_M800","/GluGlu_HToInvisible_M800_13TeV_powheg_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM", "CMS", ".*root", 0.4491)

GluGlu_HToInvisible = [
GluGlu_HToInvisible_M110,
GluGlu_HToInvisible_M125,
GluGlu_HToInvisible_M150,
GluGlu_HToInvisible_M200,
GluGlu_HToInvisible_M300,
GluGlu_HToInvisible_M400,
GluGlu_HToInvisible_M500,
GluGlu_HToInvisible_M600,
GluGlu_HToInvisible_M800,
]
