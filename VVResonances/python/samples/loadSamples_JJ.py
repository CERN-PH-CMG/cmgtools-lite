import PhysicsTools.HeppyCore.framework.config as cfg
import os

# Load backgrounds from common place
from CMGTools.RootTools.samples.samples_13TeV_RunIIFall17MiniAOD import *

####
####


# TTs = [TTJets, TT_pow_ext3, TT_pow_ext4]
background = QCDHT+VJetsQQHT+[QCD_Pt_15to7000_TuneCUETHS1_Flat]+[TTHad_pow]

# Load signal from here
from CMGTools.VVResonances.samples.signal_13TeV_94X_Fall17 import *
from CMGTools.VVResonances.samples.signal_13TeV_94X_Fall17_private import *


mcSamples = background+signalSamples+signalSamples_private
# load triggers
from CMGTools.RootTools.samples.triggers_13TeV_DATA2017 import *
# Load Data samples
from CMGTools.RootTools.samples.samples_13TeV_DATA2017 import *


# Load JSON
json = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/ReReco/Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON.txt'


JetHT = [JetHT_Run2017B_17Nov2017, JetHT_Run2017C_17Nov2017, JetHT_Run2017D_17Nov2017, JetHT_Run2017E_17Nov2017, JetHT_Run2017F_17Nov2017]


# Jet HT to be used for jj
for s in JetHT:
    s.triggers = triggers_pfht1050+triggers_ak8pfht_mass50+triggers_ak8pfjet+triggers_ak8pfjet_mass30
    s.vetoTriggers = []
    s.json = json


dataSamples = JetHT


from CMGTools.TTHAnalysis.setup.Efficiencies import *
dataDir = "$CMSSW_BASE/src/CMGTools/VVResonances/data"


# Define splitting

for comp in mcSamples:
    comp.isMC = True
    comp.isData = False
    comp.splitFactor = 300
    comp.puFileMC=dataDir+"/pileup_MC2017.root"
    comp.puFileData=dataDir+"/pileup_DATA2017.root"
    comp.efficiency = eff2012
    comp.triggers=[]
#    comp.globalTag = "Summer15_25nsV6_MC"

for comp in dataSamples:
    comp.splitFactor = 500
    comp.isMC = False
    comp.isData = True
#    comp.globalTag = "Summer15_25nsV6_DATA"
