#########################################################
##       CONFIGURATION FOR HZZ4L TREES                  ##
##########################################################
import PhysicsTools.HeppyCore.framework.config as cfg
import re

#Load all analyzers
from CMGTools.HToZZ4L.analyzers.hzz4lCore_modules_cff import * 
from CMGTools.HToZZ4L.analyzers.hzz4lExtra_modules_cff import * 
from CMGTools.HToZZ4L.tools.configTools import * 
from CMGTools.RootTools.samples.autoAAAconfig import *

#-------- SEQUENCE
fsrRecovery.enable = False
hzz4lObjSequence.remove(jetAna)
hzz4lObjSequence.remove(metAna)
sequence = cfg.Sequence(hzz4lPreSequence +  [ fastSkim2Mu3 ] + hzz4lObjSequence + [
    twoLeptonAnalyzerOnia, 
    twoLeptonEventSkimmerOnia, 
    twoLeptonTreeProducerOnia 
])


#-------- SAMPLES AND TRIGGERS -----------
from CMGTools.HToZZ4L.samples.samples_13TeV_2016 import *
dataSamples = [ d for d in dataSamples_onia if "Charm" in d.name ]
for d in dataSamples:
    d.triggers = triggers_jpsi2mu if 'Charmonium' in d.name else triggers_upsilon2mu
    d.vetoTriggers = []
    d.splitFactor = len(d.files)/3
    
mcSamples = [ JpsiToMuMuPt8 ] #, UpsToMuMuPt6 ]
#UpsToMuMuPt6.files = UpsToMuMuPt6.files[:len(UpsToMuMuPt6.files)/2+1]
for d in mcSamples:
    d.triggers = [] # triggers_jpsi2mu + triggers_upsilon2mu
    d.vetoTriggers = []
    d.splitFactor = len(d.files)/4

selectedComponents = dataSamples + mcSamples 
configureSplittingFromTime(selectedComponents, 3, 1)

if True:
    lepAna.inclusive_muon_pt = 3
    lepAna.loose_muon_pt = 3
    #selectedComponents = [ UpsToMuMuPt6 ] #JpsiToMuMuPt8 ]

if not getHeppyOption("test"):
    printSummary(selectedComponents)
    #autoAAA(selectedComponents)
 

from PhysicsTools.HeppyCore.framework.heppy_loop import getHeppyOption
test = getHeppyOption('test')
if test == "1":
    Charmonium_Run2016B_PromptV2.files = [ "root://eoscms//eos/cms/store/data/Run2016B/Charmonium/MINIAOD/PromptReco-v2/000/274/335/00000/D20107C3-EA2A-E611-A9FD-02163E01339F.root" ]
    selectedComponents = doTest1( Charmonium_Run2016B_PromptV2,
                                  sequence = sequence, cache = True)
elif test == "1M":
    selectedComponents = doTest1( JpsiToMuMuPt8, sequence=sequence )
elif test in ('2','3','5'):
    doTestN(test,selectedComponents)

config = autoConfig(selectedComponents, sequence)
