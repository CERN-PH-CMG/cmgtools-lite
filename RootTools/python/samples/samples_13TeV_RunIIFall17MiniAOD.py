# COMPONENT CREATOR
from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()

# QCD_Pt_Flat
QCD_Pt_15to7000_TuneCP5_Flat2017 = kreator.makeMCComponent("QCD_Pt_15to7000_TuneCP5_Flat2017", "/QCD_Pt-15to7000_TuneCP5_Flat2017_13TeV_pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1/MINIAODSIM", "CMS", ".*root", 1)
QCD_Pt_15to7000_TuneCP5_Flat2017_FlatPU0to70 = kreator.makeMCComponent("QCD_Pt_15to7000_TuneCP5_Flat2017_FlatPU0to70", "/QCD_Pt-15to7000_TuneCP5_Flat2017_13TeV_pythia8/RunIIFall17MiniAOD-FlatPU0to70_94X_mc2017_realistic_v10-v1/MINIAODSIM", "CMS", ".*root", 1)
QCD_Pt_15to7000_TuneCP5_Flat2017_NoPU = kreator.makeMCComponent("QCD_Pt_15to7000_TuneCP5_Flat2017_NoPU", "/QCD_Pt-15to7000_TuneCP5_Flat2017_13TeV_pythia8/RunIIFall17MiniAOD-NoPU_94X_mc2017_realistic_v10-v2/MINIAODSIM", "CMS", ".*root", 1)
QCD_Pt_15to7000_TuneCP5_Flat = kreator.makeMCComponent("QCD_Pt_15to7000_TuneCP5_Flat", "/QCD_Pt-15to7000_TuneCP5_Flat_13TeV_pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1/MINIAODSIM", "CMS", ".*root", 1)
QCD_Pt_15to7000_TuneCP5_Flat_FlatPU0to70 = kreator.makeMCComponent("QCD_Pt_15to7000_TuneCP5_Flat_FlatPU0to70", "/QCD_Pt-15to7000_TuneCP5_Flat_13TeV_pythia8/RunIIFall17MiniAOD-FlatPU0to70_94X_mc2017_realistic_v10-v1/MINIAODSIM", "CMS", ".*root", 1)
QCD_Pt_15to7000_TuneCP5_Flat_NoPU = kreator.makeMCComponent("QCD_Pt_15to7000_TuneCP5_Flat_NoPU", "/QCD_Pt-15to7000_TuneCP5_Flat_13TeV_pythia8/RunIIFall17MiniAOD-NoPU_94X_mc2017_realistic_v10-v2/MINIAODSIM", "CMS", ".*root", 1)
QCD_Pt_15to7000_TuneCUETP8M1_Flat_FlatPU0to70 = kreator.makeMCComponent("QCD_Pt_15to7000_TuneCUETP8M1_Flat_FlatPU0to70", "/QCD_Pt-15to7000_TuneCUETP8M1_Flat_13TeV_pythia8/RunIIFall17MiniAOD-FlatPU0to70_94X_mc2017_realistic_v10-v1/MINIAODSIM", "CMS", ".*root", 1)
QCD_Pt_15to7000_TuneCUETP8M1_Flat_NoPU = kreator.makeMCComponent("QCD_Pt_15to7000_TuneCUETP8M1_Flat_NoPU", "/QCD_Pt-15to7000_TuneCUETP8M1_Flat_13TeV_pythia8/RunIIFall17MiniAOD-NoPU_94X_mc2017_realistic_v10-v3/MINIAODSIM", "CMS", ".*root", 1)
QCD_Pt_15to7000_TuneCUETP8M1_Flat_NoPU_pilot = kreator.makeMCComponent("QCD_Pt_15to7000_TuneCUETP8M1_Flat_NoPU_pilot", "/QCD_Pt-15to7000_TuneCUETP8M1_Flat_13TeV_pythia8/RunIIFall17MiniAOD-NoPU_pilot_94X_mc2017_realistic_v10-v1/MINIAODSIM", "CMS", ".*root", 1)
QCD_Pt_15to7000_TuneCUETHS1_Flat = kreator.makeMCComponent("QCD_Pt_15to7000_TuneCUETHS1_Flat", "/QCD_Pt-15to7000_TuneCUETHS1_Flat_13TeV_herwigpp/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1/MINIAODSIM", "CMS", ".*root", 1)
QCD_Pt_15to7000_TuneCUETHS1_Flat_NoPU = kreator.makeMCComponent("QCD_Pt_15to7000_TuneCUETHS1_Flat_NoPU", "/QCD_Pt-15to7000_TuneCUETHS1_Flat_13TeV_herwigpp/RunIIFall17MiniAOD-NoPU_94X_mc2017_realistic_v10-v1/MINIAODSIM", "CMS", ".*root", 1)

QCDPtFlat = [
    QCD_Pt_15to7000_TuneCP5_Flat2017,
    QCD_Pt_15to7000_TuneCP5_Flat2017_FlatPU0to70,
    QCD_Pt_15to7000_TuneCP5_Flat2017_NoPU,
    QCD_Pt_15to7000_TuneCP5_Flat,
    QCD_Pt_15to7000_TuneCP5_Flat_FlatPU0to70,
    QCD_Pt_15to7000_TuneCP5_Flat_NoPU,
    QCD_Pt_15to7000_TuneCUETP8M1_Flat_FlatPU0to70,
    QCD_Pt_15to7000_TuneCUETP8M1_Flat_NoPU,
    QCD_Pt_15to7000_TuneCUETP8M1_Flat_NoPU_pilot,
    QCD_Pt_15to7000_TuneCUETHS1_Flat,
    QCD_Pt_15to7000_TuneCUETHS1_Flat_NoPU
]

# QCD_Pt
QCD_Pt80to120 = kreator.makeMCComponent("QCD_Pt80to120", "/QCD_Pt_80to120_TuneCP5_13TeV_pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1/MINIAODSIM", "CMS", ".*root", 2762530)
QCD_Pt120to170 = kreator.makeMCComponent("QCD_Pt120to170", "/QCD_Pt_120to170_TuneCP5_13TeV_pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1/MINIAODSIM", "CMS", ".*root", 471100)
QCD_Pt170to300 = kreator.makeMCComponent("QCD_Pt170to300", "/QCD_Pt_170to300_TuneCP5_13TeV_pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1/MINIAODSIM", "CMS", ".*root", 117276)
QCD_Pt300to470 = kreator.makeMCComponent("QCD_Pt300to470",  "/QCD_Pt_300to470_TuneCP5_13TeV_pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1/MINIAODSIM", "CMS", ".*root", 7823)
QCD_Pt470to600 = kreator.makeMCComponent("QCD_Pt470to600",  "/QCD_Pt_470to600_TuneCP5_13TeV_pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1/MINIAODSIM", "CMS", ".*root", 648.2)
QCD_Pt600to800 = kreator.makeMCComponent("QCD_Pt600to800", "/QCD_Pt_600to800_TuneCP5_13TeV_pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1/MINIAODSIM", "CMS", ".*root", 186.9)
QCD_Pt800to1000 = kreator.makeMCComponent("QCD_Pt800to1000", "/QCD_Pt_800to1000_TuneCP5_13TeV_pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1/MINIAODSIM", "CMS", ".*root", 32.293)
QCD_Pt1000to1400 = kreator.makeMCComponent("QCD_Pt1000to1400", "/QCD_Pt_1000to1400_TuneCP5_13TeV_pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1/MINIAODSIM", "CMS", ".*root", 9.4183)
QCD_Pt1400to1800 = kreator.makeMCComponent("QCD_Pt1400to1800", "/QCD_Pt_1400to1800_TuneCP5_13TeV_pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1/MINIAODSIM", "CMS", ".*root", 0.84265)
QCD_Pt1800to2400 = kreator.makeMCComponent("QCD_Pt1800to2400", "/QCD_Pt_1800to2400_TuneCP5_13TeV_pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1/MINIAODSIM", "CMS", ".*root", 0.114943)
QCD_Pt2400to3200 = kreator.makeMCComponent("QCD_Pt2400to3200", "/QCD_Pt_2400to3200_TuneCP5_13TeV_pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1/MINIAODSIM", "CMS", ".*root", 0.00682981)
QCD_Pt3200toInf = kreator.makeMCComponent("QCD_Pt3200", "/QCD_Pt_3200toInf_TuneCP5_13TeV_pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1/MINIAODSIM", "CMS", ".*root", 0.000165445)

QCDPt = [
    QCD_Pt80to120,
    QCD_Pt120to170,
    QCD_Pt170to300,
    QCD_Pt300to470,
    QCD_Pt470to600,
    QCD_Pt600to800,
    QCD_Pt800to1000,
    QCD_Pt1000to1400,
    QCD_Pt1400to1800,
    QCD_Pt1800to2400,
    QCD_Pt2400to3200,
    QCD_Pt3200toInf
]


# QCD HT bins (cross sections from McM)
QCD_HT100to200 = kreator.makeMCComponent("QCD_HT100to200", "/QCD_HT100to200_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1/MINIAODSIM", "CMS", ".*root", 2.785*10**7)
QCD_HT200to300 = kreator.makeMCComponent("QCD_HT200to300", "/QCD_HT200to300_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1/MINIAODSIM", "CMS", ".*root", 1717000)
QCD_HT300to500 = kreator.makeMCComponent("QCD_HT300to500", "/QCD_HT300to500_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1/MINIAODSIM", "CMS", ".*root", 351300)
QCD_HT500to700 = kreator.makeMCComponent("QCD_HT500to700", "/QCD_HT500to700_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1/MINIAODSIM", "CMS", ".*root", 31630)
QCD_HT700to1000 = kreator.makeMCComponent("QCD_HT700to1000", "/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1/MINIAODSIM", "CMS", ".*root", 6802)
QCD_HT1000to1500 = kreator.makeMCComponent("QCD_HT1000to1500", "/QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1/MINIAODSIM", "CMS", ".*root", 1206)
# QCD_HT1500to2000 = kreator.makeMCComponent("QCD_HT1500to2000", "/QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1/MINIAODSIM", "CMS", ".*root", 120.4)
# QCD_HT2000toInf = kreator.makeMCComponent("QCD_HT2000toInf", "/QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1/MINIAODSIM", "CMS", ".*root", 25.25)

QCDHT = [
    QCD_HT100to200,
    QCD_HT200to300,
    QCD_HT300to500,
    QCD_HT500to700,
    QCD_HT700to1000,
    QCD_HT1000to1500,
    # QCD_HT1500to2000,
    # QCD_HT2000toInf,
]

# DiBosons
# cross section from https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns#Diboson
WW = kreator.makeMCComponent("WW", "/WW_TuneCP5_13TeV-pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1/MINIAODSIM", "CMS", ".*root", 63.21 * 1.82)
WZ = kreator.makeMCComponent("WZ", "/WZ_TuneCP5_13TeV-pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1/MINIAODSIM", "CMS", ".*root", 47.13)
ZZ = kreator.makeMCComponent("ZZ", "/ZZ_TuneCP5_13TeV-pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1/MINIAODSIM", "CMS", ".*root", 16.523)

DiBosons = [
    WW,
    WZ,
    ZZ,
]

# ----------------------------- summary ----------------------------------------

mcSamples = QCDPtFlat + QCDPt + QCDHT + DiBosons

samples = mcSamples

# ---------------------------------------------------------------------

if __name__ == "__main__":
    from CMGTools.RootTools.samples.tools import runMain
    runMain(samples, localobjs=locals())
