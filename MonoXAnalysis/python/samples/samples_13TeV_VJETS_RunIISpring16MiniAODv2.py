import PhysicsTools.HeppyCore.framework.config as cfg
import os

from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()


GJets_100_200 = kreator.makeMCComponent("GJets_100_200", "/GJets_DR-0p4_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM", "CMS", ".*root", 4863.)
GJets_200_400 = kreator.makeMCComponent("GJets_200_400", "/GJets_DR-0p4_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM", "CMS",".*root",1074.)
GJets_400_600 = kreator.makeMCComponent("GJets_400_600", "/GJets_DR-0p4_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM", "CMS",".*root",1281.)
GJets_600_Inf = kreator.makeMCComponent("GJets_600_Inf", "/GJets_DR-0p4_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM", "CMS",".*root",42.9)

WJetsToQQ_600_Inf = kreator.makeMCComponent("WJetsToQQ_600_Inf", "/WJetsToQQ_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM", "CMS",".*root", 98.4)
WJetsToQQ_180 = kreator.makeMCComponent("WJetsToQQ_180", "/WJetsToQQ_HT180_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM", "CMS",".*root", 3098.)
ZJetsToQQ_600_Inf = kreator.makeMCComponent("ZJetsToQQ_600_Inf", "/ZJetsToQQ_HT600toInf_13TeV-madgraph/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM", "CMS",".*root", 581.9)
DYJetsToQQ_180 = kreator.makeMCComponent("DYJetsToQQ_180", "/DYJetsToQQ_HT180_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM", "CMS",".*root", 1232.)

GJets=[
GJets_100_200,
GJets_200_400,
GJets_400_600,
GJets_600_Inf
]

VV_VGamma=[
WJetsToQQ_600_Inf,
WJetsToQQ_180,
ZJetsToQQ_600_Inf,
DYJetsToQQ_180
]
