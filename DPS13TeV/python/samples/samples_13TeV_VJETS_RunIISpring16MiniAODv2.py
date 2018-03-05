import PhysicsTools.HeppyCore.framework.config as cfg
import os

### common MC samples
from CMGTools.RootTools.samples.samples_13TeV_RunIISpring16MiniAODv2 import *

from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()

ZGamma_Signal_1000TeV = kreator.makeMCComponent("ZGamma_Signal_1000TeV","/GluGluSpin0ToZGamma_ZToQQ_W_0-p-014_M_1000_TuneCUEP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM", "CMS", ".*root", 1.)

VGamma_signal=[
ZGamma_Signal_1000TeV
]

GJets = GJetsDR04HT
VV_VGamma = VJetsQQHT

