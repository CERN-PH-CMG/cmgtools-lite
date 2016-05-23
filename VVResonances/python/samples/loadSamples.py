import PhysicsTools.HeppyCore.framework.config as cfg
import os

#Load backgrounds from common place
from CMGTools.RootTools.samples.samples_13TeV_RunIIFall15MiniAODv2 import *

####
####




TTs = [TTJets,TTJets_ext,TTJets_LO_HT600to800,TTJets_LO_HT600to800_ext,TTJets_LO_HT800to1200,TTJets_LO_HT800to1200_ext,TTJets_LO_HT1200to2500,TTJets_LO_HT1200to2500_ext,TTJets_LO_HT2500toInf]



WJets=[
WJetsToLNu_HT100to200,
WJetsToLNu_HT100to200_ext,
WJetsToLNu_HT200to400,
WJetsToLNu_HT200to400_ext,
WJetsToLNu_HT400to600,
WJetsToLNu_HT600to800,
WJetsToLNu_HT800to1200,
WJetsToLNu_HT1200to2500,
WJetsToLNu_HT2500toInf
]



background = TTs+WJets+ZJetsToNuNuHT+GJetsHT+QCDHT+DiBosons+DYJetsM5to50HT



#Load signal from here 
from CMGTools.VVResonances.samples.signal_13TeV_76X import *


#and the 750 GeV samples for the tau analysis
from CMGTools.VVResonances.samples.signal_750 import *


mcSamples = background+signalSamples
#load triggers
from CMGTools.RootTools.samples.triggers_13TeV_Spring15 import *

#Load Data samples
from CMGTools.RootTools.samples.samples_13TeV_DATA2015 import *




SingleMuon=[SingleMuon_Run2015D_16Dec,]
SingleElectron=[SingleElectron_Run2015D_16Dec]
JetHT=[JetHT_Run2015D_16Dec]
MET=[MET_Run2015D_16Dec]


#Load JSON
silverJSON='/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/Reprocessing/Cert_13TeV_16Dec2015ReReco_Collisions15_25ns_JSON_Silver_v2.txt'
goldenJSON='/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/Reprocessing/Cert_13TeV_16Dec2015ReReco_Collisions15_25ns_JSON_v2.txt'


#Single electron or muon to be used for lnu+J and ll+J (silver)
for s in SingleMuon:
    s.triggers = triggers_1mu_noniso+triggers_1mu_iso
    s.vetoTriggers = []
    s.json=silverJSON
for s in SingleElectron:
    s.triggers = triggers_1e_noniso+triggers_1e
    s.vetoTriggers = triggers_1mu_noniso+triggers_1mu_iso
    s.json=silverJSON


#Jet HT to be used for jj (silver)
for s in JetHT:
    s.triggers = triggers_HT800+triggers_HT900+triggers_dijet_fat
    s.vetoTriggers = []
    s.json=silverJSON

#MET to be used for jj +MET
for s in MET:
    s.triggers = triggers_met90_mht90+triggers_metNoMu90_mhtNoMu90+triggers_metNoMu120_mhtNoMu120
    s.vetoTriggers = []
    s.json=goldenJSON

dataSamples=SingleMuon+SingleElectron+JetHT+MET


from CMGTools.TTHAnalysis.setup.Efficiencies import *
dataDir = "$CMSSW_BASE/src/CMGTools/VVResonances/data"


#Define splitting

for comp in mcSamples:
    comp.isMC = True
    comp.isData = False
    comp.splitFactor = 250   
    comp.puFileMC=dataDir+"/pileup_MC.root"
    comp.puFileData=dataDir+"/pileup_DATA.root"
    comp.efficiency = eff2012
    comp.triggers=triggers_1mu_noniso+triggers_1mu_iso+triggers_1e+triggers_1e_noniso+triggers_HT800+triggers_HT900+triggers_dijet_fat+triggers_met90_mht90+triggers_metNoMu90_mhtNoMu90+triggers_metNoMu120_mhtNoMu120
#    comp.globalTag = "Summer15_25nsV6_MC"

for comp in dataSamples:
    comp.splitFactor = 250
    comp.isMC = False
    comp.isData = True
#    comp.globalTag = "Summer15_25nsV6_DATA"
