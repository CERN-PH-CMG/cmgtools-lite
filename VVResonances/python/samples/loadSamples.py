import PhysicsTools.HeppyCore.framework.config as cfg
import os

# Load backgrounds from common place
from CMGTools.RootTools.samples.samples_13TeV_RunIIFall17MiniAOD import *\

####
####


# TTs = [TTJets, TT_pow_ext3, TT_pow_ext4]

background = TTs+Ts+DYJetsToLLM50HT+WJetsToLNuHT+QCDHT+DiBosons+Ws

# Load signal from here
mcSamples = background
# load triggers
from CMGTools.RootTools.samples.triggers_13TeV_DATA2017 import *
# Load Data samples
from CMGTools.RootTools.samples.samples_13TeV_DATA2017 import *


SingleMuon = [SingleMuon_Run2017B_17Nov2017,SingleMuon_Run2017C_17Nov2017,SingleMuon_Run2017D_17Nov2017,SingleMuon_Run2017E_17Nov2017,SingleMuon_Run2017F_17Nov2017]
SingleElectron = [SingleElectron_Run2017B_17Nov2017,SingleElectron_Run2017C_17Nov2017,SingleElectron_Run2017D_17Nov2017,SingleElectron_Run2017E_17Nov2017,SingleElectron_Run2017F_17Nov2017]
JetHT = [JetHT_Run2017B_17Nov2017,JetHT_Run2017C_17Nov2017,JetHT_Run2017D_17Nov2017,JetHT_Run2017E_17Nov2017,JetHT_Run2017F_17Nov2017]
MET = [MET_Run2017B_17Nov2017,MET_Run2017C_17Nov2017,MET_Run2017D_17Nov2017,MET_Run2017E_17Nov2017,MET_Run2017F_17Nov2017]



# Single electron or muon to be used for lnu+J and ll+J (silver)
for s in SingleMuon:
    s.triggers = triggers_1mu_noniso+triggers_1mu_iso
    s.vetoTriggers = []

for s in SingleElectron:
    s.triggers = triggers_1e_noniso+triggers_1e
    s.vetoTriggers = triggers_1mu_noniso+triggers_1mu_iso
# MET to be used for jj +MET but also to recover trigger efficiency for leptons
for s in MET:
    s.triggers = triggers_met
    s.vetoTriggers = triggers_1mu_noniso+triggers_1mu_iso+triggers_1e_noniso+triggers_1e
# Jet HT to be used for jj (silver)
for s in JetHT:
    s.triggers = triggers_pfht1050+triggers_pfht800_mass50+triggers_pfjet500+triggers_pfjet400_mass30
    s.vetoTriggers = triggers_1mu_noniso+triggers_1mu_iso+triggers_1e_noniso+triggers_1e+triggers_met



dataSamples = SingleMuon+SingleElectron+JetHT+MET

dataSamplesLNUJ = SingleMuon+SingleElectron+MET

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


for comp in dataSamples:
    comp.splitFactor = 500
    comp.isMC = False
    comp.isData = True

