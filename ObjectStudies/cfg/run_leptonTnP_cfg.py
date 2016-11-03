##########################################################
##       CONFIGURATION FOR HZZ4L TREES                  ##
##########################################################
import PhysicsTools.HeppyCore.framework.config as cfg


#-------- SAMPLES AND TRIGGERS -----------
from CMGTools.RootTools.samples.samples_13TeV_RunIISpring16MiniAODv2 import DYJetsToLL_M50_LO, DYJetsToLL_M50_LO_2
from CMGTools.RootTools.samples.samples_13TeV_DATA2016 import *
from CMGTools.RootTools.samples.autoAAAconfig import *
from CMGTools.Production.promptRecoRunRangeFilter import filterComponent


#Load all analyzers
from CMGTools.ObjectStudies.analyzers.lepTnPModules_cff import * 
from CMGTools.HToZZ4L.tools.configTools import * 



#-------- SEQUENCE
sequence = tnpSequence
#run = "Both"
#run = "Mu" 
run = "El"

from CMGTools.RootTools.samples.triggers_13TeV_DATA2016 import *

#-------- SAMPLES AND TRIGGERS -----------
dataSamples_PromptReco = [ d for d in dataSamples_PromptReco if "PromptReco-v2" in d.dataset ]
if   run == "Mu": dataSamples = [ d for d in dataSamples_PromptReco if "SingleM" in d.name ]
elif run == "El": dataSamples = [ d for d in dataSamples_PromptReco if "SingleE" in d.name ]
else            : dataSamples = [ d for d in dataSamples_PromptReco if ("SingleM" in d.name or "SingleE" in d.name) ]
for d in dataSamples[:]:
    d.triggers = triggers_1mu_iso if 'Muon' in d.name else triggers_1e
    d.vetoTriggers = []
    d.json = os.environ['CMSSW_BASE']+'/src/CMGTools/TTHAnalysis/data/json/Cert_275784-276811_13TeV_PromptReco_Collisions16_JSON_NoL1T.txt' 
    filterComponent(d,1)
    if not d.files: dataSamples.remove(d)
configureSplittingFromTime(dataSamples, 10.0, 2)
    
mcSamples = [ DYJetsToLL_M50_LO_2 ]
for d in mcSamples:
    d.triggers = [] # triggers_1mu + triggers_1e
    d.vetoTriggers = []
configureSplittingFromTime(mcSamples, 10.0, 2)

if False:
    prescaleComponents(mcSamples, 4)
    #redefineRunRange(dataSamples,[274315,274315])
    for d in dataSamples: d.splitFactor = 3

selectedComponents = mcSamples # dataSamples# + mcSamples
if run == "Mu":
    fastSkim1LTag.eleCut = lambda ele : False
    fastSkim2L.eleCut = lambda ele : False
    lepAna.loose_electron_isoCut = lambda ele : False
elif run == "El":
    fastSkim1LTag.muCut = lambda mu : False
    fastSkim2L.muCut = lambda mu : False
    lepAna.loose_muon_isoCut = lambda mu : False

printSummary(selectedComponents)
if True: autoAAA(selectedComponents)

from PhysicsTools.HeppyCore.framework.heppy_loop import getHeppyOption
test = getHeppyOption('test')
lepAna.do_mc_match_photons = False
if test in ("1","1M","1E"):
    #trigMatcher1Mu.verbose = True
    #trigMatcher1El.verbose = True
    SingleElectron_Run2016B_PromptReco_v2.files = [ 'root://eoscms//eos/cms/store/data/Run2016B/SingleElectron/MINIAOD/PromptReco-v2/000/274/315/00000/284A33F7-D829-E611-BFBE-02163E0146C7.root' ]
    SingleMuon_Run2016B_PromptReco_v2.files = [ 'root://eoscms//eos/cms/store/data/Run2016B/SingleMuon/MINIAOD/PromptReco-v2/000/274/315/00000/DCD3798B-DE29-E611-B032-02163E0138B8.root' ]
    component = { "1":DYJetsToLL_M50_LO, "1M":SingleMuon_Run2016B_PromptReco_v2, "1E":SingleElectron_Run2016B_PromptReco_v2 }[test]
    selectedComponents = doTest1( component, sequence=sequence, cache=True )
elif test in ('2','3'):
    doTestN(test,selectedComponents)

config = autoConfig(selectedComponents, sequence)#, xrd_aggressive=-1)
