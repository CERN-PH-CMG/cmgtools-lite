import re, os, sys
from CMGTools.RootTools.samples.configTools import printSummary, mergeExtensions, doTestN
from CMGTools.RootTools.samples.autoAAAconfig import autoAAA
from PhysicsTools.HeppyCore.framework.heppy_loop import getHeppyOption

from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()
def byCompName(components, regexps):
    return [ c for c in components if any(re.match(r, c.name) for r in regexps) ]

year = int(getHeppyOption("year", "2018"))

DatasetsAndTriggers = []
if year == 2018:
    from CMGTools.RootTools.samples.samples_13TeV_RunIIAutumn18NanoAODv4 import samples as mcSamples_RunIIAutumn18_NanoAODv4 
    mcSamples = byCompName(mcSamples_RunIIAutumn18_NanoAODv4, [ 
        "DYJetsToLL_M50$", "TT(Lep|Semi)_pow" 
    ])
    from CMGTools.RootTools.samples.samples_13TeV_DATA2018_NanoAOD import samples as dataSamples_DATA2018_NanoAODv4 
    allData = dataSamples_DATA2018_NanoAODv4
    from CMGTools.RootTools.samples.triggers_13TeV_DATA2017 import all_triggers as triggers
    DatasetsAndTriggers.append( ("DoubleMuon", triggers["mumu_iso"] + triggers["3mu"]) )
    DatasetsAndTriggers.append( ("EGamma",     triggers["ee"] + triggers["3e"] + triggers["1e_iso"]) )
    DatasetsAndTriggers.append( ("MuonEG",     triggers["mue"] + triggers["2mu1e"] + triggers["2e1mu"]) )
    DatasetsAndTriggers.append( ("SingleMuon", triggers["1mu_iso"]) )
elif year == 2017:
    from CMGTools.RootTools.samples.samples_13TeV_RunIIFall17NanoAODv4 import samples as mcSamples_RunIIFall17_NanoAODv4 
    mcSamples = byCompName(mcSamples_RunIIFall17_NanoAODv4, [ 
        "DYJetsToLL_M50$", "TT(Lep|Semi)_pow" 
    ])
    from CMGTools.RootTools.samples.samples_13TeV_DATA2017_NanoAOD import samples as dataSamples_DATA2017_NanoAODv4 
    allData = dataSamples_DATA2017_NanoAODv4
    from CMGTools.RootTools.samples.triggers_13TeV_DATA2017 import all_triggers as triggers
    DatasetsAndTriggers.append( ("DoubleMuon", triggers["mumu_iso"] + triggers["3mu"]) )
    DatasetsAndTriggers.append( ("DoubleEG",   triggers["ee"] + triggers["3e"]) )
    DatasetsAndTriggers.append( ("MuonEG",     triggers["mue"] + triggers["2mu1e"] + triggers["2e1mu"]) )
    DatasetsAndTriggers.append( ("SingleMuon", triggers["1mu_iso"]) )
    DatasetsAndTriggers.append( ("SingleElectron", triggers["1e_iso"]) )
elif year == 2016:
    from CMGTools.RootTools.samples.samples_13TeV_RunIISummer16NanoAODv4 import samples as mcSamples_RunIISummer16_NanoAODv4 
    mcSamples = byCompName(mcSamples_RunIISummer16_NanoAODv4, [ 
        "DYJetsToLL_M50$", "TT(Lep|Semi)_pow" 
    ])
    from CMGTools.RootTools.samples.samples_13TeV_DATA2016_NanoAOD import samples as dataSamples_DATA2016_NanoAODv4 
    allData = dataSamples_DATA2016_NanoAODv4
    from CMGTools.RootTools.samples.triggers_13TeV_DATA2016 import all_triggers as triggers
    DatasetsAndTriggers.append( ("DoubleMuon", triggers["mumu_iso"] + triggers["3mu"]) )
    DatasetsAndTriggers.append( ("DoubleEG",   triggers["ee"] + triggers["3e"]) )
    DatasetsAndTriggers.append( ("MuonEG",     triggers["mue"] + triggers["2mu1e"] + triggers["2e1mu"]) )
    DatasetsAndTriggers.append( ("SingleMuon", triggers["1mu_iso"]) )
    DatasetsAndTriggers.append( ("SingleElectron", triggers["1e_iso"]) )
# make MC
mcTriggers = sum((trigs for (pd,trigs) in DatasetsAndTriggers), [])
for comp in mcSamples:
    comp.triggers = mcTriggers

# make data
dataSamples = []; vetoTriggers = []
for pd, triggers in DatasetsAndTriggers:
    for comp in byCompName(allData, pd):
        comp.triggers = triggers[:]
        comp.vetoTriggers = vetoTriggers[:]
        dataSamples.append(comp)
    vetoTriggers += triggers[:]

selectedComponents = mcSamples + dataSamples
if getHeppyOption('selectComponents'):
    selectedComponents = byCompName(selectedComponents, getHeppyOption('selectComponents').split(","))
autoAAA(selectedComponents, quiet=not(getHeppyOption("verboseAAA",False)))
selectedComponents, _ = mergeExtensions(selectedComponents)

# print summary of components to process
if getHeppyOption("justSummary"): 
    printSummary(selectedComponents)
    sys.exit(0)

from CMGTools.TTHAnalysis.tools.nanoAOD.ttH_modules import *

from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor

# in the cut string, keep only the main cuts to have it simpler
modules = ttH_sequence_step1

branchsel_in = None
branchsel_out = None
compression = "ZLIB:3" #"LZ4:4" #"LZMA:9"

POSTPROCESSOR = PostProcessor(None, [], modules = modules,
        cut = ttH_skim_cut, prefetch = True, longTermCache = True,
        branchsel = branchsel_in, outputbranchsel = branchsel_out, compression = compression)

test = getHeppyOption("test")
if test == "94X-MC":
    TTLep_pow = kreator.makeMCComponent("TTLep_pow", "/TTTo2L2Nu_mtop166p5_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1/MINIAODSIM", "CMS", ".*root", 831.76*((3*0.108)**2) )
    TTLep_pow.files = ["/afs/cern.ch/user/g/gpetrucc/NanoAOD_94X_TTLep.root"]
    lepSkim.requireSameSignPair = False
    lepSkim.minJets = 0
    lepSkim.minMET = 0
    lepSkim.prescaleFactor = 0
    selectedComponents = [TTLep_pow]
elif test == "94X-MC-miniAOD":
    TTLep_pow = kreator.makeMCComponent("TTLep_pow", "/TTTo2L2Nu_mtop166p5_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1/MINIAODSIM", "CMS", ".*root", 831.76*((3*0.108)**2) )
    TTLep_pow.files =A [ 'root://cms-xrd-global.cern.ch//store/mc/RunIIFall17MiniAOD/TTTo2L2Nu_mtop166p5_TuneCP5_PSweights_13TeV-powheg-pythia8/MINIAODSIM/94X_mc2017_realistic_v10-v1/70000/3CC234EB-44E0-E711-904F-FA163E0DF774.root' ]
    localfile = os.path.expandvars("/tmp/$USER/%s" % os.path.basename(TTLep_pow.files[0]))
    if os.path.exists(localfile): TTLep_pow.files = [ localfile ] 
    from CMGTools.Production.nanoAODPreprocessor import nanoAODPreprocessor
    TTLep_pow.preprocessor = nanoAODPreprocessor("/afs/cern.ch/work/g/gpetrucc/ttH/CMSSW_10_4_0/src/nanov4_NANO_cfg.py")
    selectedComponents = [TTLep_pow]
elif test == "102X-MC":
    TTLep_pow = kreator.makeMCComponent("TTLep_pow", "/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM", "CMS", ".*root", 831.76*((3*0.108)**2), useAAA=True )
    TTLep_pow.files = TTLep_pow.files[:1]
    selectedComponents = [TTLep_pow]
elif test in ('2','3'):
    doTestN(test, selectedComponents)
