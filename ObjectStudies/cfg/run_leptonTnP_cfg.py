##########################################################
##       CONFIGURATION FOR HZZ4L TREES                  ##
##########################################################
import PhysicsTools.HeppyCore.framework.config as cfg


#-------- SAMPLES AND TRIGGERS -----------
from CMGTools.RootTools.samples.samples_13TeV_RunIIFall15MiniAODv2 import DYJetsToLL_M50_LO
from CMGTools.RootTools.samples.samples_13TeV_DATA2015 import *
from CMGTools.RootTools.samples.autoAAAconfig import *


#Load all analyzers
from CMGTools.ObjectStudies.analyzers.lepTnPModules_cff import * 
from CMGTools.HToZZ4L.tools.configTools import * 


#-------- SEQUENCE
sequence = tnpSequence
#run = "Both"
#run = "Mu" 
run = "El"

triggers_1mu = [ 'HLT_IsoMu22_v*', 'HLT_IsoMu20_v*' ]
triggers_1e  = [ 'HLT_Ele23_WPLoose_Gsf_v*' ]

#-------- SAMPLES AND TRIGGERS -----------
if   run == "Mu": dataSamples = [ d for d in dataSamples_76X if "SingleM" in d.name ]
elif run == "El": dataSamples = [ d for d in dataSamples_76X if "SingleE" in d.name ]
else            : dataSamples = [ d for d in dataSamples_76X if ("SingleM" in d.name or "SingleE" in d.name) ]
for d in dataSamples:
    d.triggers = triggers_1mu if 'Muon' in d.name else triggers_1e
    d.vetoTriggers = []
    d.json = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/Cert_246908-260627_13TeV_PromptReco_Collisions15_25ns_JSON_v2.txt'
configureSplittingFromTime(dataSamples, 2.0, 2)
    
mcSamples = [ DYJetsToLL_M50_LO ]
for d in mcSamples:
    d.triggers = triggers_1mu + triggers_1e
    d.vetoTriggers = []
configureSplittingFromTime(mcSamples, 5.0, 2)

if True:
    prescaleComponents(mcSamples, 10)
    dataSamples = [ d for d in dataSamples if 'Run2015D' in d.name ]
    redefineRunRange(dataSamples,[258214,258214])
    for d in dataSamples: d.splitFactor = 3

selectedComponents = dataSamples + mcSamples
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
    component = { "1":DYJetsToLL_M50_LO, "1M":SingleMuon_Run2015D_16Dec, "1E":SingleElectron_Run2015D_16Dec }[test]
    if not component.isMC: redefineRunRange([component],[258214,258214])
    selectedComponents = doTest1( component, sequence=sequence )
elif test in ('2','3'):
    doTestN(test,selectedComponents)

config = autoConfig(selectedComponents, sequence)
