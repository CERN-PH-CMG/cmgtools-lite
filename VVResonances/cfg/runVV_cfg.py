##########################################################
##       GENERIC SUSY TREE PRODUCTION CONFIG.           ##
## no skim is applied in this configuration, as it is   ##
## meant only to check that all common modules run ok   ##
##########################################################


#AAA
###
def autoAAA(selectedComponents,runOnlyRemoteSamples=False,forceAAA=False):
    newComp=[]
    import re
    from CMGTools.Production import changeComponentAccessMode
    from CMGTools.Production.localityChecker import LocalityChecker
    tier2Checker = LocalityChecker("T2_CH_CERN", datasets="/*/*/MINIAOD*")
    for comp in selectedComponents:
        if len(comp.files)==0:
            continue
        if not hasattr(comp,'dataset'): continue
        if not re.match("/[^/]+/[^/]+/MINIAOD(SIM)?", comp.dataset): continue
        if "/store/" not in comp.files[0]: continue
        if re.search("/store/(group|user|cmst3)/", comp.files[0]): continue
        if (not tier2Checker.available(comp.dataset)) or forceAAA:
            print "Dataset %s is not available, will use AAA" % comp.dataset
            changeComponentAccessMode.convertComponent(comp, "root://cms-xrd-global.cern.ch/%s")
            if 'X509_USER_PROXY' not in os.environ or "/afs/" not in os.environ['X509_USER_PROXY']:
                raise RuntimeError, "X509_USER_PROXY not defined or not pointing to /afs"
            newComp.append(comp)
    if runOnlyRemoteSamples:
        return newComp
    else:
        return selectedComponents

def autoConfig(selectedComponents,sequence,services=[],xrd_aggressive=2):
    import PhysicsTools.HeppyCore.framework.config as cfg
    from PhysicsTools.HeppyCore.framework.eventsfwlite import Events
    from CMGTools.TTHAnalysis.tools.EOSEventsWithDownload import EOSEventsWithDownload
    event_class = EOSEventsWithDownload
    EOSEventsWithDownload.aggressive = xrd_aggressive
    if getHeppyOption("nofetch") or getHeppyOption("isCrab"):
        event_class = Events
    return cfg.Config( components = selectedComponents,
                     sequence = sequence,
                     services = services,
                     events_class = event_class)


###



import CMGTools.RootTools.fwlite.Config as cfg
from CMGTools.RootTools.fwlite.Config import printComps
from CMGTools.RootTools.RootTools import *
from PhysicsTools.HeppyCore.framework.heppy_loop import getHeppyOption

#Load all common analyzers
from CMGTools.VVResonances.analyzers.core_cff import *

#PUPPI by default #uncomment for prunning
#doPruning()



#-------- SAMPLES AND TRIGGERS -----------
from CMGTools.VVResonances.samples.loadSamples import *

#selectedComponents = mcSamples+dataSamplesLNUJ
selectedComponents =mcSamples+dataSamplesLNUJ



#import pdb;pdb.set_trace()

#-------- Analyzer
from CMGTools.VVResonances.analyzers.tree_cff import *

#-------- SEQUENCE

sequence = cfg.Sequence(coreSequence+[vvAna,metWeightAna,vvSkimmer,vvTreeProducer])
from CMGTools.RootTools.samples.triggers_13TeV_DATA2016 import *


triggerFlagsAna.triggerBits ={
    "ISOMU":triggers_1mu_iso,
    "MU":triggers_1mu_noniso,
    "ISOELE":triggers_1e_iso,
    "ELE":triggers_1e_noniso,
    "MET120":triggers_metNoMu120_mhtNoMu120+triggers_met120_mht120
}


#-------- HOW TO RUN
test = 1
if test==1:
    # test a single component, using a single thread.
#    selectedComponents = [BulkGravToWWToWlepWhad_narrow_2000]
#    selectedComponents = [TTJets]
    selectedComponents = [WJetsToLNu_HT2500ToInf]
#    selectedComponents = [BulkGravToZZToZhadZinv_narrow_1400]
    for c in selectedComponents:
#        c.files = c.files[:1]
        c.files = ['file:/tmp/bachtis/file.root']
        c.splitFactor = 1

elif test==2:
    # test a single component, using a single thread.
    selectedComponents = [TTJets]
elif test==3:
    selectedComponents = [WJetsToLNu_HT2500toInf]
    for c in selectedComponents:
        c.files = c.files[:1]
        c.splitFactor = 1
else:
    # full scale production
    # split samples in a smarter way
    from CMGTools.RootTools.samples.configTools import configureSplittingFromTime, printSummary
    configureSplittingFromTime(selectedComponents, 10, 3)  # means 40 ms per event, job to last 3h
    # print summary of components to process
    printSummary(selectedComponents)

selectedComponents=autoAAA(selectedComponents)
config=autoConfig(selectedComponents,sequence)
