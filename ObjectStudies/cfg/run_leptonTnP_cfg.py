##########################################################
##       CONFIGURATION FOR HZZ4L TREES                  ##
##########################################################
import PhysicsTools.HeppyCore.framework.config as cfg


#-------- SAMPLES AND TRIGGERS -----------
from CMGTools.RootTools.samples.samples_13TeV_RunIISummer16MiniAODv2 import DYJetsToLL_M50_LO_ext as DYJetsToLL_M50_LO
DYJetsToLL_M50_LO.name = "DYJetsToLL_M50_LO"

from CMGTools.RootTools.samples.samples_13TeV_DATA2016 import *
from CMGTools.RootTools.samples.autoAAAconfig import *


#Load all analyzers
from CMGTools.ObjectStudies.analyzers.lepTnPModules_cff import * 
from CMGTools.RootTools.samples.configTools import *



#-------- SEQUENCE
sequence = tnpSequence
#run = "Both"
#run = "Mu" 
run = "El"

from CMGTools.RootTools.samples.triggers_13TeV_DATA2016 import *

#-------- SAMPLES AND TRIGGERS -----------
if   run == "Mu": dataSamples = [ d for d in dataSamples_23Sep2016PlusPrompt if "SingleM" in d.name ]
elif run == "El": dataSamples = [ d for d in dataSamples_23Sep2016PlusPrompt if "SingleE" in d.name ]
else            : dataSamples = [ d for d in dataSamples_23Sep2016PlusPrompt if ("SingleM" in d.name or "SingleE" in d.name) ]
for d in dataSamples[:]:
    d.triggers = triggers_1mu_iso if 'Muon' in d.name else triggers_1e
    d.vetoTriggers = []
    d.json='/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/ReReco/Final/Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt'
    if not d.files: dataSamples.remove(d)
configureSplittingFromTime(dataSamples, 5.0, 2)
    
mcSamples = [ DYJetsToLL_M50_LO ]
for d in mcSamples:
    d.triggers = [] # triggers_1mu + triggers_1e
    d.vetoTriggers = []
configureSplittingFromTime(mcSamples, 10.0, 2)

if False:
    prescaleComponents(mcSamples, 4)
    #redefineRunRange(dataSamples,[274315,274315])
    for d in dataSamples: d.splitFactor = 3

selectedComponents = mcSamples + dataSamples# + mcSamples
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
    SingleElectron_Run2016B_23Sep2016.files = [ SingleElectron_Run2016B_23Sep2016.files[3] ]
    SingleMuon_Run2016B_23Sep2016.files = [ SingleMuon_Run2016B_23Sep2016.files[3] ]
    component = { "1":DYJetsToLL_M50_LO, "1M":SingleMuon_Run2016B_23Sep2016, "1E":SingleElectron_Run2016B_23Sep2016 }[test]
    selectedComponents = doTest1( component, sequence=sequence, cache=True )
elif test in ('2','3'):
    doTestN(test,selectedComponents)

config = autoConfig(selectedComponents, sequence)#, xrd_aggressive=-1)
