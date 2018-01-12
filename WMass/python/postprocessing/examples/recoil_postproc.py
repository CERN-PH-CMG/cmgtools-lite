#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from CMGTools.WMass.postprocessing.framework.postprocessor import PostProcessor

from genFriendProducer import *
from eventRecoilAnalyzer import *

p=PostProcessor(outputDir=".",
                #eventRange=xrange(1000),
                inputFiles=["mytest/WJetsToLNu_LO/treeProducerWMass/tree.root"],
                cut=None,
                branchsel=None, #"recoil_keep_and_drop.txt",
                modules=[GenQEDJetProducer(deltaR=0.1,beamEn=13000.),
                         EventRecoilAnalyzer(tag='test')])
p.run()
