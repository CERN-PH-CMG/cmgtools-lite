import PhysicsTools.HeppyCore.framework.config as cfg
import os

#####COMPONENT CREATOR

from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()

### OFFICIAL SMS SIGNALS
T1tttt_mGo_1000_mLSP_1to700 = kreator.makeMCComponent("T1tttt_mGo_1000_mLSP_1to700","/SMS-T1tttt_mGluino-1000_mLSP-1to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-FastAsympt25ns_74X_mcRun2_asymptotic_v2-v1/MINIAODSIM","CMS",".*root")
T1tttt_mGo_1000to1050_mLSP_1to800 = kreator.makeMCComponent("T1tttt_mGo_1000to1050_mLSP_1to800","/SMS-T1tttt_mGluino-1000to1050_mLSP-1to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-FastAsympt25ns_74X_mcRun2_asymptotic_v2-v1/MINIAODSIM","CMS",".*root", useAAA = True)
T1tttt_mGo_1050_mLSP_50to775 = kreator.makeMCComponent("T1tttt_mGo_1050_mLSP_50to775","/SMS-T1tttt_mGluino-1050_mLSP-50to775_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-FastAsympt25ns_74X_mcRun2_asymptotic_v2-v1/MINIAODSIM","CMS",".*root")
T1tttt_mGo_1050to1075_mLSP_650to850 = kreator.makeMCComponent("T1tttt_mGo_1050to1075_mLSP_650to850","/SMS-T1tttt_mGluino-1050to1075_mLSP-650to850_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-FastAsympt25ns_74X_mcRun2_asymptotic_v2-v1/MINIAODSIM","CMS",".*root")
T1tttt_mGo_1100_mLSP_1to775 = kreator.makeMCComponent("T1tttt_mGo_1100_mLSP_1to775","/SMS-T1tttt_mGluino-1100_mLSP-1to775_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-FastAsympt25ns_74X_mcRun2_asymptotic_v2-v1/MINIAODSIM","CMS",".*root")
T1tttt_mGo_1100to1125_mLSP_700to900 = kreator.makeMCComponent("T1tttt_mGo_1100to1125_mLSP_700to900","/SMS-T1tttt_mGluino-1100to1125_mLSP-700to900_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-FastAsympt25ns_74X_mcRun2_asymptotic_v2-v1/MINIAODSIM","CMS",".*root")
T1tttt_mGo_1150_mLSP_1to800 = kreator.makeMCComponent("T1tttt_mGo_1150_mLSP_1to800","/SMS-T1tttt_mGluino-1150_mLSP-1to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-FastAsympt25ns_74X_mcRun2_asymptotic_v2-v1/MINIAODSIM","CMS",".*root")
T1tttt_mGo_1150to1175_mLSP_750to925 = kreator.makeMCComponent("T1tttt_mGo_1150to1175_mLSP_750to925","/SMS-T1tttt_mGluino-1150to1175_mLSP-750to925_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-FastAsympt25ns_74X_mcRun2_asymptotic_v2-v1/MINIAODSIM","CMS",".*root")
T1tttt_mGo_1175_mLSP_950 = kreator.makeMCComponent("T1tttt_mGo_1175_mLSP_950","/SMS-T1tttt_mGluino-1175_mLSP-950_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-FastAsympt25ns_74X_mcRun2_asymptotic_v2-v1/MINIAODSIM","CMS",".*root")
T1tttt_mGo_1200_mLSP_1to825 = kreator.makeMCComponent("T1tttt_mGo_1200_mLSP_1to825","/SMS-T1tttt_mGluino-1200_mLSP-1to825_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-FastAsympt25ns_74X_mcRun2_asymptotic_v2-v1/MINIAODSIM","CMS",".*root")
T1tttt_mGo_1200to1225_mLSP_800to1000 = kreator.makeMCComponent("T1tttt_mGo_1200to1225_mLSP_800to1000","/SMS-T1tttt_mGluino-1200to1225_mLSP-800to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-FastAsympt25ns_74X_mcRun2_asymptotic_v2-v1/MINIAODSIM","CMS",".*root")
T1tttt_mGo_1225to1250_mLSP_1to1025 = kreator.makeMCComponent("T1tttt_mGo_1225to1250_mLSP_1to1025","/SMS-T1tttt_mGluino-1225to1250_mLSP-1to1025_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-FastAsympt25ns_74X_mcRun2_asymptotic_v2-v1/MINIAODSIM","CMS",".*root", useAAA = True)
T1tttt_mGo_1250to1275_mLSP_700to1050 = kreator.makeMCComponent("T1tttt_mGo_1250to1275_mLSP_700to1050","/SMS-T1tttt_mGluino-1250to1275_mLSP-700to1050_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-FastAsympt25ns_74X_mcRun2_asymptotic_v2-v1/MINIAODSIM","CMS",".*root")
T1tttt_mGo_1275_mLSP_900to975 = kreator.makeMCComponent("T1tttt_mGo_1275_mLSP_900to975","/SMS-T1tttt_mGluino-1275_mLSP-900to975_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-FastAsympt25ns_74X_mcRun2_asymptotic_v2-v1/MINIAODSIM","CMS",".*root")
T1tttt_mGo_1300_mLSP_1to1075 = kreator.makeMCComponent("T1tttt_mGo_1300_mLSP_1to1075","/SMS-T1tttt_mGluino-1300_mLSP-1to1075_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-FastAsympt25ns_74X_mcRun2_asymptotic_v2-v1/MINIAODSIM","CMS",".*root")
T1tttt_mGo_1300to1325_mLSP_700to1100 = kreator.makeMCComponent("T1tttt_mGo_1300to1325_mLSP_700to1100","/SMS-T1tttt_mGluino-1300to1325_mLSP-700to1100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-FastAsympt25ns_74X_mcRun2_asymptotic_v2-v1/MINIAODSIM","CMS",".*root")
T1tttt_mGo_1325to1350_mLSP_1to1125 = kreator.makeMCComponent("T1tttt_mGo_1325to1350_mLSP_1to1125","/SMS-T1tttt_mGluino-1325to1350_mLSP-1to1125_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-FastAsympt25ns_74X_mcRun2_asymptotic_v2-v1/MINIAODSIM","CMS",".*root", useAAA = True)
T1tttt_mGo_1350to1375_mLSP_50to1025 = kreator.makeMCComponent("T1tttt_mGo_1350to1375_mLSP_50to1025","/SMS-T1tttt_mGluino-1350to1375_mLSP-50to1025_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-FastAsympt25ns_74X_mcRun2_asymptotic_v2-v1/MINIAODSIM","CMS",".*root")
T1tttt_mGo_1375_mLSP_950to1150 = kreator.makeMCComponent("T1tttt_mGo_1375_mLSP_950to1150","/SMS-T1tttt_mGluino-1375_mLSP-950to1150_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-FastAsympt25ns_74X_mcRun2_asymptotic_v2-v1/MINIAODSIM","CMS",".*root")
T1tttt_mGo_1400_mLSP_1to1175 = kreator.makeMCComponent("T1tttt_mGo_1400_mLSP_1to1175","/SMS-T1tttt_mGluino-1400_mLSP-1to1175_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-FastAsympt25ns_74X_mcRun2_asymptotic_v2-v1/MINIAODSIM","CMS",".*root")
T1tttt_mGo_1400to1425_mLSP_50to1100 = kreator.makeMCComponent("T1tttt_mGo_1400to1425_mLSP_50to1100","/SMS-T1tttt_mGluino-1400to1425_mLSP-50to1100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-FastAsympt25ns_74X_mcRun2_asymptotic_v2-v1/MINIAODSIM","CMS",".*root")
T1tttt_mGo_1425to1450_mLSP_1to1200 = kreator.makeMCComponent("T1tttt_mGo_1425to1450_mLSP_1to1200","/SMS-T1tttt_mGluino-1425to1450_mLSP-1to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-FastAsympt25ns_74X_mcRun2_asymptotic_v2-v1/MINIAODSIM","CMS",".*root")
T1tttt_mGo_1450to1475_mLSP_50to1075 = kreator.makeMCComponent("T1tttt_mGo_1450to1475_mLSP_50to1075","/SMS-T1tttt_mGluino-1450to1475_mLSP-50to1075_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-FastAsympt25ns_74X_mcRun2_asymptotic_v2-v1/MINIAODSIM","CMS",".*root")
T1tttt_mGo_1475to1500_mLSP_1to1250 = kreator.makeMCComponent("T1tttt_mGo_1475to1500_mLSP_1to1250","/SMS-T1tttt_mGluino-1475to1500_mLSP-1to1250_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-FastAsympt25ns_74X_mcRun2_asymptotic_v2-v1/MINIAODSIM","CMS",".*root")
T1tttt_mGo_1500to1525_mLSP_50to1125 = kreator.makeMCComponent("T1tttt_mGo_1500to1525_mLSP_50to1125","/SMS-T1tttt_mGluino-1500to1525_mLSP-50to1125_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-FastAsympt25ns_74X_mcRun2_asymptotic_v2-v1/MINIAODSIM","CMS",".*root")
T1tttt_mGo_1525to1550_mLSP_1to1300 = kreator.makeMCComponent("T1tttt_mGo_1525to1550_mLSP_1to1300","/SMS-T1tttt_mGluino-1525to1550_mLSP-1to1300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-FastAsympt25ns_74X_mcRun2_asymptotic_v2-v1/MINIAODSIM","CMS",".*root")
T1tttt_mGo_1550to1575_mLSP_500to1175 = kreator.makeMCComponent("T1tttt_mGo_1550to1575_mLSP_500to1175","/SMS-T1tttt_mGluino-1550to1575_mLSP-500to1175_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-FastAsympt25ns_74X_mcRun2_asymptotic_v2-v1/MINIAODSIM","CMS",".*root")
T1tttt_mGo_1600to1650_mLSP_1to1350 = kreator.makeMCComponent("T1tttt_mGo_1600to1650_mLSP_1to1350","/SMS-T1tttt_mGluino-1600to1650_mLSP-1to1350_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-FastAsympt25ns_74X_mcRun2_asymptotic_v2-v1/MINIAODSIM","CMS",".*root")
T1tttt_mGo_1650to1700_mLSP_1to1400 = kreator.makeMCComponent("T1tttt_mGo_1650to1700_mLSP_1to1400","/SMS-T1tttt_mGluino-1650to1700_mLSP-1to1400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-FastAsympt25ns_74X_mcRun2_asymptotic_v2-v1/MINIAODSIM","CMS",".*root")
T1tttt_mGo_1700to1750_mLSP_1to1450 = kreator.makeMCComponent("T1tttt_mGo_1700to1750_mLSP_1to1450","/SMS-T1tttt_mGluino-1700to1750_mLSP-1to1450_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-FastAsympt25ns_74X_mcRun2_asymptotic_v2-v1/MINIAODSIM","CMS",".*root")
T1tttt_mGo_1750_mLSP_50to1450 = kreator.makeMCComponent("T1tttt_mGo_1750_mLSP_50to1450","/SMS-T1tttt_mGluino-1750_mLSP-50to1450_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-FastAsympt25ns_74X_mcRun2_asymptotic_v2-v1/MINIAODSIM","CMS",".*root")
T1tttt_mGo_1800to1850_mLSP_1to1450 = kreator.makeMCComponent("T1tttt_mGo_1800to1850_mLSP_1to1450","/SMS-T1tttt_mGluino-1800to1850_mLSP-1to1450_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-FastAsympt25ns_74X_mcRun2_asymptotic_v2-v1/MINIAODSIM","CMS",".*root")
T1tttt_mGo_1850to1900_mLSP_1to1450 = kreator.makeMCComponent("T1tttt_mGo_1850to1900_mLSP_1to1450","/SMS-T1tttt_mGluino-1850to1900_mLSP-1to1450_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-FastAsympt25ns_74X_mcRun2_asymptotic_v2-v1/MINIAODSIM","CMS",".*root")
T1tttt_mGo_1900to1950_mLSP_0to1450 = kreator.makeMCComponent("T1tttt_mGo_1900to1950_mLSP_0to1450","/SMS-T1tttt_mGluino-1900to1950_mLSP-0to1450_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-FastAsympt25ns_74X_mcRun2_asymptotic_v2-v1/MINIAODSIM","CMS",".*root")
T1tttt_mGo_1950_mLSP_700to950 = kreator.makeMCComponent("T1tttt_mGo_1950_mLSP_700to950","/SMS-T1tttt_mGluino-1950_mLSP-700to950_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-FastAsympt25ns_74X_mcRun2_asymptotic_v2-v1/MINIAODSIM","CMS",".*root")
T1tttt_mGo_600_mLSP_1to225 = kreator.makeMCComponent("T1tttt_mGo_600_mLSP_1to225","/SMS-T1tttt_mGluino-600_mLSP-1to225_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-FastAsympt25ns_74X_mcRun2_asymptotic_v2-v1/MINIAODSIM","CMS",".*root")
T1tttt_mGo_600_mLSP_250to325 = kreator.makeMCComponent("T1tttt_mGo_600_mLSP_250to325","/SMS-T1tttt_mGluino-600_mLSP-250to325_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-FastAsympt25ns_74X_mcRun2_asymptotic_v2-v1/MINIAODSIM","CMS",".*root")
T1tttt_mGo_600to625_mLSP_250to375 = kreator.makeMCComponent("T1tttt_mGo_600to625_mLSP_250to375","/SMS-T1tttt_mGluino-600to625_mLSP-250to375_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-FastAsympt25ns_74X_mcRun2_asymptotic_v2-v1/MINIAODSIM","CMS",".*root", useAAA = True)
T1tttt_mGo_625_mLSP_275to375 = kreator.makeMCComponent("T1tttt_mGo_625_mLSP_275to375","/SMS-T1tttt_mGluino-625_mLSP-275to375_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-FastAsympt25ns_74X_mcRun2_asymptotic_v2-v1/MINIAODSIM","CMS",".*root")
T1tttt_mGo_625to650_mLSP_200to400 = kreator.makeMCComponent("T1tttt_mGo_625to650_mLSP_200to400","/SMS-T1tttt_mGluino-625to650_mLSP-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-FastAsympt25ns_74X_mcRun2_asymptotic_v2-v1/MINIAODSIM","CMS",".*root")
T1tttt_mGo_650to675_mLSP_250to425 = kreator.makeMCComponent("T1tttt_mGo_650to675_mLSP_250to425","/SMS-T1tttt_mGluino-650to675_mLSP-250to425_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-FastAsympt25ns_74X_mcRun2_asymptotic_v2-v1/MINIAODSIM","CMS",".*root")
T1tttt_mGo_675_mLSP_325to450 = kreator.makeMCComponent("T1tttt_mGo_675_mLSP_325to450","/SMS-T1tttt_mGluino-675_mLSP-325to450_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-FastAsympt25ns_74X_mcRun2_asymptotic_v2-v1/MINIAODSIM","CMS",".*root")
T1tttt_mGo_700_mLSP_1to450 = kreator.makeMCComponent("T1tttt_mGo_700_mLSP_1to450","/SMS-T1tttt_mGluino-700_mLSP-1to450_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-FastAsympt25ns_74X_mcRun2_asymptotic_v2-v1/MINIAODSIM","CMS",".*root")
T1tttt_mGo_700to750_mLSP_200to500 = kreator.makeMCComponent("T1tttt_mGo_700to750_mLSP_200to500","/SMS-T1tttt_mGluino-700to750_mLSP-200to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-FastAsympt25ns_74X_mcRun2_asymptotic_v2-v1/MINIAODSIM","CMS",".*root")
T1tttt_mGo_750to775_mLSP_350to525 = kreator.makeMCComponent("T1tttt_mGo_750to775_mLSP_350to525","/SMS-T1tttt_mGluino-750to775_mLSP-350to525_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-FastAsympt25ns_74X_mcRun2_asymptotic_v2-v1/MINIAODSIM","CMS",".*root")
T1tttt_mGo_775_mLSP_475to550 = kreator.makeMCComponent("T1tttt_mGo_775_mLSP_475to550","/SMS-T1tttt_mGluino-775_mLSP-475to550_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-FastAsympt25ns_74X_mcRun2_asymptotic_v2-v1/MINIAODSIM","CMS",".*root")
T1tttt_mGo_800to825_mLSP_1to575 = kreator.makeMCComponent("T1tttt_mGo_800to825_mLSP_1to575","/SMS-T1tttt_mGluino-800to825_mLSP-1to575_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-FastAsympt25ns_74X_mcRun2_asymptotic_v2-v1/MINIAODSIM","CMS",".*root")
T1tttt_mGo_825to850_mLSP_200to600 = kreator.makeMCComponent("T1tttt_mGo_825to850_mLSP_200to600","/SMS-T1tttt_mGluino-825to850_mLSP-200to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-FastAsympt25ns_74X_mcRun2_asymptotic_v2-v1/MINIAODSIM","CMS",".*root")
T1tttt_mGo_850to875_mLSP_450to625 = kreator.makeMCComponent("T1tttt_mGo_850to875_mLSP_450to625","/SMS-T1tttt_mGluino-850to875_mLSP-450to625_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-FastAsympt25ns_74X_mcRun2_asymptotic_v2-v1/MINIAODSIM","CMS",".*root")
T1tttt_mGo_875to900_mLSP_1to650 = kreator.makeMCComponent("T1tttt_mGo_875to900_mLSP_1to650","/SMS-T1tttt_mGluino-875to900_mLSP-1to650_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-FastAsympt25ns_74X_mcRun2_asymptotic_v2-v1/MINIAODSIM","CMS",".*root")
T1tttt_mGo_900to950_mLSP_200to700 = kreator.makeMCComponent("T1tttt_mGo_900to950_mLSP_200to700","/SMS-T1tttt_mGluino-900to950_mLSP-200to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-FastAsympt25ns_74X_mcRun2_asymptotic_v2-v1/MINIAODSIM","CMS",".*root")
T1tttt_mGo_950to975_mLSP_350to725 = kreator.makeMCComponent("T1tttt_mGo_950to975_mLSP_350to725","/SMS-T1tttt_mGluino-950to975_mLSP-350to725_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-FastAsympt25ns_74X_mcRun2_asymptotic_v2-v1/MINIAODSIM","CMS",".*root")
T1tttt_mGo_975_mLSP_600to750 = kreator.makeMCComponent("T1tttt_mGo_975_mLSP_600to750","/SMS-T1tttt_mGluino-975_mLSP-600to750_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-FastAsympt25ns_74X_mcRun2_asymptotic_v2-v1/MINIAODSIM","CMS",".*root")


mcSamplesT1tttt = [T1tttt_mGo_1000_mLSP_1to700, T1tttt_mGo_1000to1050_mLSP_1to800, T1tttt_mGo_1050_mLSP_50to775, T1tttt_mGo_1050to1075_mLSP_650to850, T1tttt_mGo_1100_mLSP_1to775, T1tttt_mGo_1100to1125_mLSP_700to900, T1tttt_mGo_1150_mLSP_1to800, T1tttt_mGo_1150to1175_mLSP_750to925, T1tttt_mGo_1175_mLSP_950, T1tttt_mGo_1200_mLSP_1to825, T1tttt_mGo_1200to1225_mLSP_800to1000, T1tttt_mGo_1225to1250_mLSP_1to1025, T1tttt_mGo_1250to1275_mLSP_700to1050, T1tttt_mGo_1275_mLSP_900to975, T1tttt_mGo_1300_mLSP_1to1075, T1tttt_mGo_1300to1325_mLSP_700to1100, T1tttt_mGo_1325to1350_mLSP_1to1125, T1tttt_mGo_1350to1375_mLSP_50to1025, T1tttt_mGo_1375_mLSP_950to1150, T1tttt_mGo_1400_mLSP_1to1175, T1tttt_mGo_1400to1425_mLSP_50to1100, T1tttt_mGo_1425to1450_mLSP_1to1200, T1tttt_mGo_1450to1475_mLSP_50to1075, T1tttt_mGo_1475to1500_mLSP_1to1250, T1tttt_mGo_1500to1525_mLSP_50to1125, T1tttt_mGo_1525to1550_mLSP_1to1300, T1tttt_mGo_1550to1575_mLSP_500to1175, T1tttt_mGo_1600to1650_mLSP_1to1350, T1tttt_mGo_1650to1700_mLSP_1to1400, T1tttt_mGo_1700to1750_mLSP_1to1450, T1tttt_mGo_1750_mLSP_50to1450, T1tttt_mGo_1800to1850_mLSP_1to1450, T1tttt_mGo_1850to1900_mLSP_1to1450, T1tttt_mGo_1900to1950_mLSP_0to1450, T1tttt_mGo_1950_mLSP_700to950, T1tttt_mGo_600_mLSP_1to225, T1tttt_mGo_600_mLSP_250to325, T1tttt_mGo_600to625_mLSP_250to375, T1tttt_mGo_625_mLSP_275to375, T1tttt_mGo_625to650_mLSP_200to400, T1tttt_mGo_650to675_mLSP_250to425, T1tttt_mGo_675_mLSP_325to450, T1tttt_mGo_700_mLSP_1to450, T1tttt_mGo_700to750_mLSP_200to500, T1tttt_mGo_750to775_mLSP_350to525, T1tttt_mGo_775_mLSP_475to550, T1tttt_mGo_800to825_mLSP_1to575, T1tttt_mGo_825to850_mLSP_200to600, T1tttt_mGo_850to875_mLSP_450to625, T1tttt_mGo_875to900_mLSP_1to650, T1tttt_mGo_900to950_mLSP_200to700, T1tttt_mGo_950to975_mLSP_350to725, T1tttt_mGo_975_mLSP_600to750]

mcSamples = mcSamplesT1tttt

samples = mcSamples

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
