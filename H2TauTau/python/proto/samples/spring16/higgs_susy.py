import copy

from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator

creator = ComponentCreator()

HiggsSUSYGG80 = creator.makeMCComponent(
    "HiggsSUSYGG80", "/SUSYGluGluToHToTauTau_M-80_TuneCUETP8M1_13TeV-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM", "CMS", ".*root", 1.0)
HiggsSUSYGG90 = creator.makeMCComponent(
    "HiggsSUSYGG90", "/SUSYGluGluToHToTauTau_M-90_TuneCUETP8M1_13TeV-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM", "CMS", ".*root", 1.0)
HiggsSUSYGG100 = creator.makeMCComponent(
    "HiggsSUSYGG100", "/SUSYGluGluToHToTauTau_M-100_TuneCUETP8M1_13TeV-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM", "CMS", ".*root", 1.0)
HiggsSUSYGG110 = creator.makeMCComponent(
    "HiggsSUSYGG110", "/SUSYGluGluToHToTauTau_M-110_TuneCUETP8M1_13TeV-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM", "CMS", ".*root", 1.0)
HiggsSUSYGG120 = creator.makeMCComponent(
    "HiggsSUSYGG120", "/SUSYGluGluToHToTauTau_M-120_TuneCUETP8M1_13TeV-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM", "CMS", ".*root", 1.0)
HiggsSUSYGG130 = creator.makeMCComponent(
    "HiggsSUSYGG130", "/SUSYGluGluToHToTauTau_M-130_TuneCUETP8M1_13TeV-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM", "CMS", ".*root", 1.0)
HiggsSUSYGG140 = creator.makeMCComponent(
    "HiggsSUSYGG140", "/SUSYGluGluToHToTauTau_M-140_TuneCUETP8M1_13TeV-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM", "CMS", ".*root", 1.0)
HiggsSUSYGG160 = creator.makeMCComponent(
    "HiggsSUSYGG160", "/SUSYGluGluToHToTauTau_M-160_TuneCUETP8M1_13TeV-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM", "CMS", ".*root", 1.0)
HiggsSUSYGG180 = creator.makeMCComponent(
    "HiggsSUSYGG180", "/SUSYGluGluToHToTauTau_M-180_TuneCUETP8M1_13TeV-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM", "CMS", ".*root", 1.0)
HiggsSUSYGG200 = creator.makeMCComponent(
    "HiggsSUSYGG200", "/SUSYGluGluToHToTauTau_M-200_TuneCUETP8M1_13TeV-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM", "CMS", ".*root", 1.0)
HiggsSUSYGG250 = creator.makeMCComponent(
    "HiggsSUSYGG250", "/SUSYGluGluToHToTauTau_M-250_TuneCUETP8M1_13TeV-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v2/MINIAODSIM", "CMS", ".*root", 1.0)
HiggsSUSYGG300 = creator.makeMCComponent(
    "HiggsSUSYGG300", "/SUSYGluGluToHToTauTau_M-300_TuneCUETP8M1_13TeV-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v2/MINIAODSIM", "CMS", ".*root", 1.0)
HiggsSUSYGG350 = creator.makeMCComponent(
    "HiggsSUSYGG350", "/SUSYGluGluToHToTauTau_M-350_TuneCUETP8M1_13TeV-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM", "CMS", ".*root", 1.0)
HiggsSUSYGG400 = creator.makeMCComponent(
    "HiggsSUSYGG400", "/SUSYGluGluToHToTauTau_M-400_TuneCUETP8M1_13TeV-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v3/MINIAODSIM", "CMS", ".*root", 1.0)
HiggsSUSYGG450 = creator.makeMCComponent(
    "HiggsSUSYGG450", "/SUSYGluGluToHToTauTau_M-450_TuneCUETP8M1_13TeV-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM", "CMS", ".*root", 1.0)
HiggsSUSYGG500 = creator.makeMCComponent(
    "HiggsSUSYGG500", "/SUSYGluGluToHToTauTau_M-500_TuneCUETP8M1_13TeV-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM", "CMS", ".*root", 1.0)
HiggsSUSYGG600 = creator.makeMCComponent(
    "HiggsSUSYGG600", "/SUSYGluGluToHToTauTau_M-600_TuneCUETP8M1_13TeV-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM", "CMS", ".*root", 1.0)
HiggsSUSYGG700 = creator.makeMCComponent(
    "HiggsSUSYGG700", "/SUSYGluGluToHToTauTau_M-700_TuneCUETP8M1_13TeV-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM", "CMS", ".*root", 1.0)
HiggsSUSYGG800 = creator.makeMCComponent(
    "HiggsSUSYGG800", "/SUSYGluGluToHToTauTau_M-800_TuneCUETP8M1_13TeV-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM", "CMS", ".*root", 1.0)
HiggsSUSYGG900 = creator.makeMCComponent(
    "HiggsSUSYGG900", "/SUSYGluGluToHToTauTau_M-900_TuneCUETP8M1_13TeV-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM", "CMS", ".*root", 1.0)
HiggsSUSYGG1000 = creator.makeMCComponent(
    "HiggsSUSYGG1000", "/SUSYGluGluToHToTauTau_M-1000_TuneCUETP8M1_13TeV-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM", "CMS", ".*root", 1.0)
HiggsSUSYGG1200 = creator.makeMCComponent(
    "HiggsSUSYGG1200", "/SUSYGluGluToHToTauTau_M-1200_TuneCUETP8M1_13TeV-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM", "CMS", ".*root", 1.0)
HiggsSUSYGG1400 = creator.makeMCComponent(
    "HiggsSUSYGG1400", "/SUSYGluGluToHToTauTau_M-1400_TuneCUETP8M1_13TeV-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM", "CMS", ".*root", 1.0)
HiggsSUSYGG1500 = creator.makeMCComponent(
    "HiggsSUSYGG1500", "/SUSYGluGluToHToTauTau_M-1500_TuneCUETP8M1_13TeV-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM", "CMS", ".*root", 1.0)
HiggsSUSYGG1600 = creator.makeMCComponent(
    "HiggsSUSYGG1600", "/SUSYGluGluToHToTauTau_M-1600_TuneCUETP8M1_13TeV-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM", "CMS", ".*root", 1.0)
HiggsSUSYGG1800 = creator.makeMCComponent(
    "HiggsSUSYGG1800", "/SUSYGluGluToHToTauTau_M-1800_TuneCUETP8M1_13TeV-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM", "CMS", ".*root", 1.0)
HiggsSUSYGG2000 = creator.makeMCComponent(
    "HiggsSUSYGG2000", "/SUSYGluGluToHToTauTau_M-2000_TuneCUETP8M1_13TeV-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM", "CMS", ".*root", 1.0)
HiggsSUSYGG2300 = creator.makeMCComponent(
    "HiggsSUSYGG2300", "/SUSYGluGluToHToTauTau_M-2300_TuneCUETP8M1_13TeV-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM", "CMS", ".*root", 1.0)
HiggsSUSYGG2600 = creator.makeMCComponent(
    "HiggsSUSYGG2600", "/SUSYGluGluToHToTauTau_M-2600_TuneCUETP8M1_13TeV-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM", "CMS", ".*root", 1.0)
HiggsSUSYGG2900 = creator.makeMCComponent(
    "HiggsSUSYGG2900", "/SUSYGluGluToHToTauTau_M-2900_TuneCUETP8M1_13TeV-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM", "CMS", ".*root", 1.0)
HiggsSUSYGG3200 = creator.makeMCComponent(
    "HiggsSUSYGG3200", "/SUSYGluGluToHToTauTau_M-3200_TuneCUETP8M1_13TeV-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM", "CMS", ".*root", 1.0)


HiggsSUSYBB80 = creator.makeMCComponent(
    "HiggsSUSYBB80", "/SUSYGluGluToBBHToTauTau_M-80_TuneCUETP8M1_13TeV-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM", "CMS", ".*root", 1.0)
HiggsSUSYBB90 = creator.makeMCComponent(
    "HiggsSUSYBB90", "/SUSYGluGluToBBHToTauTau_M-90_TuneCUETP8M1_13TeV-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM", "CMS", ".*root", 1.0)
HiggsSUSYBB100 = creator.makeMCComponent(
    "HiggsSUSYBB100", "/SUSYGluGluToBBHToTauTau_M-100_TuneCUETP8M1_13TeV-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM", "CMS", ".*root", 1.0)
HiggsSUSYBB110 = creator.makeMCComponent(
    "HiggsSUSYBB110", "/SUSYGluGluToBBHToTauTau_M-110_TuneCUETP8M1_13TeV-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM", "CMS", ".*root", 1.0)
HiggsSUSYBB120 = creator.makeMCComponent(
    "HiggsSUSYBB120", "/SUSYGluGluToBBHToTauTau_M-120_TuneCUETP8M1_13TeV-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM", "CMS", ".*root", 1.0)
HiggsSUSYBB130 = creator.makeMCComponent(
    "HiggsSUSYBB130", "/SUSYGluGluToBBHToTauTau_M-130_TuneCUETP8M1_13TeV-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM", "CMS", ".*root", 1.0)
HiggsSUSYBB140 = creator.makeMCComponent(
    "HiggsSUSYBB140", "/SUSYGluGluToBBHToTauTau_M-140_TuneCUETP8M1_13TeV-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM", "CMS", ".*root", 1.0)
HiggsSUSYBB160 = creator.makeMCComponent(
    "HiggsSUSYBB160", "/SUSYGluGluToBBHToTauTau_M-160_TuneCUETP8M1_13TeV-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM", "CMS", ".*root", 1.0)
HiggsSUSYBB180 = creator.makeMCComponent(
    "HiggsSUSYBB180", "/SUSYGluGluToBBHToTauTau_M-180_TuneCUETP8M1_13TeV-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM", "CMS", ".*root", 1.0)
HiggsSUSYBB200 = creator.makeMCComponent(
    "HiggsSUSYBB200", "/SUSYGluGluToBBHToTauTau_M-200_TuneCUETP8M1_13TeV-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v4/MINIAODSIM", "CMS", ".*root", 1.0)
HiggsSUSYBB250 = creator.makeMCComponent(
    "HiggsSUSYBB250", "/SUSYGluGluToBBHToTauTau_M-250_TuneCUETP8M1_13TeV-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM", "CMS", ".*root", 1.0)
HiggsSUSYBB300 = creator.makeMCComponent(
    "HiggsSUSYBB300", "/SUSYGluGluToBBHToTauTau_M-300_TuneCUETP8M1_13TeV-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM", "CMS", ".*root", 1.0)
HiggsSUSYBB350 = creator.makeMCComponent(
    "HiggsSUSYBB350", "/SUSYGluGluToBBHToTauTau_M-350_TuneCUETP8M1_13TeV-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM", "CMS", ".*root", 1.0)
HiggsSUSYBB400 = creator.makeMCComponent(
    "HiggsSUSYBB400", "/SUSYGluGluToBBHToTauTau_M-400_TuneCUETP8M1_13TeV-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM", "CMS", ".*root", 1.0)
HiggsSUSYBB450 = creator.makeMCComponent(
    "HiggsSUSYBB450", "/SUSYGluGluToBBHToTauTau_M-450_TuneCUETP8M1_13TeV-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM", "CMS", ".*root", 1.0)
HiggsSUSYBB500 = creator.makeMCComponent(
    "HiggsSUSYBB500", "/SUSYGluGluToBBHToTauTau_M-500_TuneCUETP8M1_13TeV-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM", "CMS", ".*root", 1.0)
HiggsSUSYBB600 = creator.makeMCComponent(
    "HiggsSUSYBB600", "/SUSYGluGluToBBHToTauTau_M-600_TuneCUETP8M1_13TeV-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM", "CMS", ".*root", 1.0)
HiggsSUSYBB700 = creator.makeMCComponent(
    "HiggsSUSYBB700", "/SUSYGluGluToBBHToTauTau_M-700_TuneCUETP8M1_13TeV-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM", "CMS", ".*root", 1.0)
HiggsSUSYBB800 = creator.makeMCComponent(
    "HiggsSUSYBB800", "/SUSYGluGluToBBHToTauTau_M-800_TuneCUETP8M1_13TeV-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM", "CMS", ".*root", 1.0)
HiggsSUSYBB900 = creator.makeMCComponent(
    "HiggsSUSYBB900", "/SUSYGluGluToBBHToTauTau_M-900_TuneCUETP8M1_13TeV-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM", "CMS", ".*root", 1.0)
HiggsSUSYBB1000 = creator.makeMCComponent(
    "HiggsSUSYBB1000", "/SUSYGluGluToBBHToTauTau_M-1000_TuneCUETP8M1_13TeV-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM", "CMS", ".*root", 1.0)
HiggsSUSYBB1200 = creator.makeMCComponent(
    "HiggsSUSYBB1200", "/SUSYGluGluToBBHToTauTau_M-1200_TuneCUETP8M1_13TeV-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM", "CMS", ".*root", 1.0)
HiggsSUSYBB1400 = creator.makeMCComponent(
    "HiggsSUSYBB1400", "/SUSYGluGluToBBHToTauTau_M-1400_TuneCUETP8M1_13TeV-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM", "CMS", ".*root", 1.0)
HiggsSUSYBB1500 = creator.makeMCComponent(
    "HiggsSUSYBB1500", "/SUSYGluGluToBBHToTauTau_M-1500_TuneCUETP8M1_13TeV-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM", "CMS", ".*root", 1.0)
HiggsSUSYBB1600 = creator.makeMCComponent(
    "HiggsSUSYBB1600", "/SUSYGluGluToBBHToTauTau_M-1600_TuneCUETP8M1_13TeV-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM", "CMS", ".*root", 1.0)
HiggsSUSYBB1800 = creator.makeMCComponent(
    "HiggsSUSYBB1800", "/SUSYGluGluToBBHToTauTau_M-1800_TuneCUETP8M1_13TeV-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM", "CMS", ".*root", 1.0)
HiggsSUSYBB2000 = creator.makeMCComponent(
    "HiggsSUSYBB2000", "/SUSYGluGluToBBHToTauTau_M-2000_TuneCUETP8M1_13TeV-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM", "CMS", ".*root", 1.0)
HiggsSUSYBB2300 = creator.makeMCComponent(
    "HiggsSUSYBB2300", "/SUSYGluGluToBBHToTauTau_M-2300_TuneCUETP8M1_13TeV-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v4/MINIAODSIM", "CMS", ".*root", 1.0)
HiggsSUSYBB2600 = creator.makeMCComponent(
    "HiggsSUSYBB2600", "/SUSYGluGluToBBHToTauTau_M-2600_TuneCUETP8M1_13TeV-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM", "CMS", ".*root", 1.0)
HiggsSUSYBB2900 = creator.makeMCComponent(
    "HiggsSUSYBB2900", "/SUSYGluGluToBBHToTauTau_M-2900_TuneCUETP8M1_13TeV-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM", "CMS", ".*root", 1.0)
HiggsSUSYBB3200 = creator.makeMCComponent(
    "HiggsSUSYBB3200", "/SUSYGluGluToBBHToTauTau_M-3200_TuneCUETP8M1_13TeV-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM", "CMS", ".*root", 1.0)


mc_higgs_susy_gg = [
    # HiggsSUSYGG80,
    # HiggsSUSYGG90,
    # HiggsSUSYGG100,
    # HiggsSUSYGG110,
    # HiggsSUSYGG120,
    # HiggsSUSYGG130,
    # HiggsSUSYGG140,
    HiggsSUSYGG160,
    # HiggsSUSYGG180,
    # HiggsSUSYGG200,
    # HiggsSUSYGG250,
    # HiggsSUSYGG300,
    # HiggsSUSYGG350,
    # HiggsSUSYGG400,
    # HiggsSUSYGG450,
    HiggsSUSYGG500,
    # HiggsSUSYGG600,
    # HiggsSUSYGG700,
    # HiggsSUSYGG800,
    # HiggsSUSYGG900,
    # HiggsSUSYGG1000,
    # HiggsSUSYGG1200,
    # HiggsSUSYGG1400,
    # HiggsSUSYGG1500,
    # HiggsSUSYGG1600,
    # HiggsSUSYGG1800,
    # HiggsSUSYGG2000,
    # HiggsSUSYGG2300,
    # HiggsSUSYGG2600,
    # HiggsSUSYGG2900,
    # HiggsSUSYGG3200
]

mc_higgs_susy_bb = [
    # HiggsSUSYBB80,
    # HiggsSUSYBB90,
    # HiggsSUSYBB100,
    # HiggsSUSYBB110,
    # HiggsSUSYBB120,
    # HiggsSUSYBB130,
    # HiggsSUSYBB140,
    HiggsSUSYBB160,
    # HiggsSUSYBB180,
    # HiggsSUSYBB200,
    # HiggsSUSYBB250,
    # HiggsSUSYBB300,
    # HiggsSUSYBB350,
    # HiggsSUSYBB400,
    # HiggsSUSYBB450,
    HiggsSUSYBB500,
    # HiggsSUSYBB600,
    # HiggsSUSYBB700,
    # HiggsSUSYBB800,
    # HiggsSUSYBB900,
    HiggsSUSYBB1000,
    # HiggsSUSYBB1200,
    # HiggsSUSYBB1400,
    # HiggsSUSYBB1500,
    # HiggsSUSYBB1600,
    # HiggsSUSYBB1800,
    # HiggsSUSYBB2000,
    # HiggsSUSYBB2300,
    # HiggsSUSYBB2600,
    # HiggsSUSYBB2900,
    # HiggsSUSYBB3200
]

mc_higgs_susy = copy.copy(mc_higgs_susy_gg)
mc_higgs_susy.extend(mc_higgs_susy_bb)
