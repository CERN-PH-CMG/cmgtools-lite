import PhysicsTools.HeppyCore.framework.config as cfg
import os

### common MC samples
from CMGTools.RootTools.samples.samples_13TeV_RunIISpring16MiniAODv2 import *

from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()

GJets = GJetsDR04HT
VV_VGamma = VJetsQQHT

