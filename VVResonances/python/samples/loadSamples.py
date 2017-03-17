import PhysicsTools.HeppyCore.framework.config as cfg
import os

# Load backgrounds from common place
from CMGTools.RootTools.samples.samples_13TeV_RunIISummer16MiniAODv2 import *

####
####


# TTs = [TTJets, TT_pow_ext3, TT_pow_ext4]
TTs = [TTJets, TT_pow, TT_pow_ext3]
background = TTs+SingleTop+DYJetsM50HT+WJetsToLNuHT+QCDHT+DiBosons+WJetsToLNuPT

# Load signal from here
from CMGTools.VVResonances.samples.signal_13TeV_80X_Summer16 import *
from CMGTools.VVResonances.samples.signal_13TeV_80X_ZPTT import *


mcSamples = background+signalSamples+zprimeSamples
# load triggers
from CMGTools.RootTools.samples.triggers_13TeV_DATA2016 import *
# Load Data samples
from CMGTools.RootTools.samples.samples_13TeV_DATA2016 import *


# Load JSON
json = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/ReReco/Final/Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt'


SingleMuon = [SingleMuon_Run2016B_03Feb2017_v2, SingleMuon_Run2016C_03Feb2017, SingleMuon_Run2016D_03Feb2017, SingleMuon_Run2016E_03Feb2017, SingleMuon_Run2016F_03Feb2017, SingleMuon_Run2016G_03Feb2017, SingleMuon_Run2016H_03Feb2017_v2, SingleMuon_Run2016H_03Feb2017_v3]
SingleElectron = [SingleElectron_Run2016B_03Feb2017_v2, SingleElectron_Run2016C_03Feb2017, SingleElectron_Run2016D_03Feb2017, SingleElectron_Run2016E_03Feb2017, SingleElectron_Run2016F_03Feb2017, SingleElectron_Run2016G_03Feb2017, SingleElectron_Run2016H_03Feb2017_v2, SingleElectron_Run2016H_03Feb2017_v3]
JetHT = [JetHT_Run2016B_03Feb2017_v2, JetHT_Run2016C_03Feb2017, JetHT_Run2016D_03Feb2017, JetHT_Run2016E_03Feb2017, JetHT_Run2016F_03Feb2017, JetHT_Run2016G_03Feb2017, JetHT_Run2016H_03Feb2017_v2, JetHT_Run2016H_03Feb2017_v3]
MET = [MET_Run2016B_03Feb2017_v2, MET_Run2016C_03Feb2017, MET_Run2016D_03Feb2017, MET_Run2016E_03Feb2017, MET_Run2016F_03Feb2017, MET_Run2016G_03Feb2017, MET_Run2016H_03Feb2017_v2, MET_Run2016H_03Feb2017_v3]


# Single electron or muon to be used for lnu+J and ll+J (silver)
for s in SingleMuon:
    s.triggers = triggers_1mu_noniso+triggers_1mu_iso
    s.vetoTriggers = []
    s.json = json
for s in SingleElectron:
    s.triggers = triggers_1e_noniso+triggers_1e
    s.vetoTriggers = triggers_1mu_noniso+triggers_1mu_iso
    s.json = json


# MET to be used for jj +MET but also to recover trigger efficiency for leptons
for s in MET:
    s.triggers = triggers_metNoMu120_mhtNoMu120
    s.vetoTriggers = triggers_1mu_noniso+triggers_1mu_iso+triggers_1e_noniso+triggers_1e
    s.json = json



# Jet HT to be used for jj (silver)
for s in JetHT:
    s.triggers = triggers_HT800+triggers_HT900+triggers_dijet_fat+triggers_jet_recoverHT
    s.vetoTriggers = triggers_1mu_noniso+triggers_1mu_iso+triggers_1e_noniso+triggers_1e+triggers_metNoMu120_mhtNoMu120
    s.json = json


dataSamples = SingleMuon+SingleElectron+JetHT+MET


from CMGTools.TTHAnalysis.setup.Efficiencies import *
dataDir = "$CMSSW_BASE/src/CMGTools/VVResonances/data"


# Define splitting

for comp in mcSamples:
    comp.isMC = True
    comp.isData = False
    comp.splitFactor = 300
    comp.puFileMC=dataDir+"/pileup_MC.root"
    comp.puFileData=dataDir+"/pileup_DATA.root"
    comp.efficiency = eff2012
    comp.triggers=[]
#    comp.globalTag = "Summer15_25nsV6_MC"

for comp in dataSamples:
    comp.splitFactor = 500
    comp.isMC = False
    comp.isData = True
#    comp.globalTag = "Summer15_25nsV6_DATA"
