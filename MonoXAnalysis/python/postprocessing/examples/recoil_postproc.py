#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from CMGTools.MonoXAnalysis.postprocessing.framework.postprocessor import PostProcessor

from genFriendProducer import *
from eventRecoilAnalyzer import *

p=PostProcessor(outputDir=".",
#                eventRange=xrange(1000),
                inputFiles=["../../../cfg/mytest/WJetsToLNu_LO/treeProducerWMass/tree.root"],
                cut=None,
                branchsel=None, #"keep_and_drop.txt",
                modules=[GenQEDJetProducer(deltaR=0.1,beamEn=13000.),
                         eventRecoilAnalyzer(tag='test')])
p.run()
