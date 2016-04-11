##########################################################
##       GENERIC SUSY TREE PRODUCTION CONFIG.           ##
## no skim is applied in this configuration, as it is   ##
## meant only to check that all common modules run ok   ##
##########################################################


#AAA
###
def autoAAA(selectedComponents,onlyRemote=False,forceAAA=False):
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
            newComp.append(comp)
    if onlyRemote:
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

#-------- SAMPLES AND TRIGGERS -----------
from CMGTools.VVResonances.samples.loadSamples import *

selectedComponents =background+SingleMuon+SingleElectron



#import pdb;pdb.set_trace()

#-------- Analyzer
from CMGTools.VVResonances.analyzers.tree_cff import * 

#-------- SEQUENCE

sequence = cfg.Sequence(coreSequence+[vTauAna,vTauSkimmer,vTauTreeProducer])


from CMGTools.RootTools.samples.triggers_13TeV_Spring15 import *


triggerFlagsAna.triggerBits ={
    "ISOMU":triggers_1mu_iso,
    "MU":triggers_1mu_noniso,
    "ISOELE":triggers_1e,
    "ELE":triggers_1e_noniso,
    "HT800":triggers_HT800,
    "HT900":triggers_HT900,
    "JJ":triggers_dijet_fat,  
    "MET90":triggers_met90_mht90+triggers_metNoMu90_mhtNoMu90,
    "MET120":triggers_metNoMu120_mhtNoMu120
}


#-------- HOW TO RUN
test = 0
if test==1:
    # test a single component, using a single thread.
    selectedComponents = [VBF_RadionToZZ_narrow_4500]
    for c in selectedComponents:
        c.files = c.files[:1]
        c.splitFactor = 1
elif test==2:    
    # test all components (1 thread per component).
    selectedComponents = [testSample]
    for comp in selectedComponents:
        comp.splitFactor = 1
#        comp.files = comp.files[:1]
elif test==3:    
    # test all components (1 thread per component).
    selectedComponents = [DYJetsToLL_M50_HT600toInf]
    for comp in selectedComponents:
        comp.splitFactor = 1

elif test==4:    
    # test all components (1 thread per component).
    selectedComponents = [RSGravToWWToLNQQ_kMpl01_4500]
    for comp in selectedComponents:
        comp.splitFactor = 1
elif test==5:    
    selectedComponents = [WJetsToLNu_HT2500toInf,VBF_RadionToZZ_narrow_4500,RSGravToWWToLNQQ_kMpl01_4500]



selectedComponents=[SingleElectron_Run2015D_05Oct]
selectedComponents=autoAAA(selectedComponents,False,True)
config=autoConfig(selectedComponents,sequence)
