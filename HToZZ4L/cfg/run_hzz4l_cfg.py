##########################################################
##       CONFIGURATION FOR HZZ4L TREES                  ##
##########################################################
import PhysicsTools.HeppyCore.framework.config as cfg

#Load all analyzers
from CMGTools.HToZZ4L.analyzers.hzz4lCore_modules_cff import * 
from CMGTools.HToZZ4L.tools.configTools import * 
from CMGTools.RootTools.samples.autoAAAconfig import *

#-------- SAMPLES AND TRIGGERS -----------

#-------- SEQUENCE
from CMGTools.HToZZ4L.samples.samples_13TeV_2016 import *

selectedComponents = [ d for d in dataSamples if "SingleMu" not in d.name ]
#redefineRunRange(selectedComponents,[258158,258158])
#selectedComponents = [ DoubleMuon_Run2015D_16Dec2015_25ns, DoubleEG_Run2015D_16Dec2015_25ns, MuonEG_Run2015D_16Dec2015_25ns, SingleMuon_Run2015D_16Dec2015_25ns, SingleElectron_Run2015D_16Dec2015_25ns ]
#redefineRunRange(selectedComponents,[258214,258214])
#configureSplittingFromTime(selectedComponents, 2.0, 1)
#selectedComponents = H4L + [ ZZTo4L, ZZTo4L_aMC ] + GGZZTo4L + [DYJetsToLL_M10to50,DYJetsToLL_M50] + [ WZTo3LNu, TTLep ] + SingleTop
#selectedComponents = H4L + GGZZTo4L + [DYJetsToLL_M10to50,DYJetsToLL_M50] + [ WZTo3LNu, TTLep ] + SingleTop
#cropToLumi( [DYJetsToLL_M10to50,DYJetsToLL_M50,TTLep]+SingleTop, 100.0 )
#cropToLumi( [ZZTo4L, ZZTo4L_aMC]+GGZZTo4L, 500.0 )
#cropToLumi( H4L, 10000.0 )
#configureSplittingFromTime(DYJets+SingleTop+[WZTo3LNu,TTLep,GGZZTo4tau], 10.0, 1)
#configureSplittingFromTime([DYJetsToLL_M10to50], 5.0, 1)
#configureSplittingFromTime([ ZZTo4L, ZZTo4L_aMC, GGZZTo2mu2tau, GGZZTo2e2tau ], 25.0, 1)
#configureSplittingFromTime( H4L + [ GGZZTo4mu, GGZZTo4e, GGZZTo2e2mu], 100.0, 1)
#selectedComponents = [ DYJetsToLL_M50, DYJetsToLL_LO_M50 ] + DYJetsM50HT

sequence = cfg.Sequence(hzz4lCoreSequence)

#switchOffMEs(sequence)

for comp in mcSamples:
    comp.triggers = []
    comp.vetoTriggers = []


#doECalCorrections(era="25ns")
#doKalmanMuonCorrections(smear="basic")

if not getHeppyOption("test"):
    printSummary(selectedComponents)
#autoAAA(selectedComponents)


from PhysicsTools.HeppyCore.framework.heppy_loop import getHeppyOption
test = getHeppyOption('test')
if test == "1":
    selectedComponents = doTest1( GGHZZ4L, sequence=sequence, cache=True )
elif test == "1ZZ":
    selectedComponents = doTest1( ZZTo4L, sequence=sequence, cache=True )
elif test == "1F":
    selectedComponents = doTest1( DYJetsToLL_M50, sequence=sequence, cache=False )
elif test in ('2','3','5'):
    doTestN(test,selectedComponents)
elif test == "data":
    redefineRunRange([DoubleMuon_Run2016B_PromptV2],[273158,273158])
    selectedComponents = doTest1( DoubleMuon_Run2016B_PromptV2, sequence=sequence )
elif test=="sync":
    comp = ZZTo4L
    comp.name = 'HZZ4L'
    comp.files = [ 'root://eoscms.cern.ch//eos/cms'+X for X in (
    #comp.files = [ 'root://cms-xrd-global.cern.ch//'+X for X in (
'/store/mc/RunIISpring16MiniAODv1/VBF_HToZZTo4L_M190_13TeV_powheg2_JHUgenV6_pythia8/MINIAODSIM/PUSpring16RAWAODSIM_80X_mcRun2_asymptotic_2016_v3-v1/00000/28ADE6D5-021F-E611-B1A4-00145E5521B9.root',
'/store/mc/RunIISpring16MiniAODv1/WminusH_HToZZTo4L_M150_13TeV_powheg2-minlo-HWJ_JHUgenV6_pythia8/MINIAODSIM/PUSpring16RAWAODSIM_80X_mcRun2_asymptotic_2016_v3-v1/00000/C6DF34D4-CF20-E611-A8EE-782BCB27B958.root',
    )]
    if os.path.exists('/data1/g/gpetrucc/HZZ/28ADE6D5-021F-E611-B1A4-00145E5521B9.root') and os.path.exists('/data1/g/gpetrucc/HZZ/C6DF34D4-CF20-E611-A8EE-782BCB27B958.root'):
        comp.files = [ '/data1/g/gpetrucc/HZZ/28ADE6D5-021F-E611-B1A4-00145E5521B9.root', '/data1/g/gpetrucc/HZZ/C6DF34D4-CF20-E611-A8EE-782BCB27B958.root' ]
    if getHeppyOption('turbo'):
        comp.fineSplitFactor = int(getHeppyOption('turbo'))
        comp.splitFactor = 1
    else:
        comp.fineSplitFactor = 1
        comp.splitFactor = 1 if getHeppyOption('single') else 5
    selectedComponents = [ comp ]
    if getHeppyOption('events'): 
        insertEventSelector(sequence)
        selectedComponents[0].splitFactor = 1
        fourLeptonAnalyzerSignal.debug = True
        fourLeptonAnalyzerSignal.maxCand = 999
    #doECalCorrections(sync=True)
    #doKalmanMuonCorrections(sync=True)
elif test=="sync76X":
    comp = ZZTo4L
    comp.name = 'HZZ4L'
    #comp.files = [ 'root://eoscms.cern.ch//eos/cms'+X for X in (
    comp.files = [ 'root://cms-xrd-global.cern.ch//'+X for X in (
    '/store/mc/RunIIFall15MiniAODv1/VBF_HToZZTo4L_M125_13TeV_powheg2_JHUgenV6_pythia8/MINIAODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/00000/E2490ECF-CBA7-E511-9B19-001E67398458.root', 
    '/store/mc/RunIIFall15MiniAODv1/WminusH_HToZZTo4L_M125_13TeV_powheg2-minlo-HWJ_JHUgenV6_pythia8/MINIAODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/50000/282C35FB-68A3-E511-A0C4-0CC47A4C8E5E.root',
    '/store/mc/RunIIFall15MiniAODv1/WplusH_HToZZTo4L_M125_13TeV_powheg2-minlo-HWJ_JHUgenV6_pythia8/MINIAODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/20000/E2DA5AA7-C5AC-E511-97E0-0CC47A4C8E98.root', 
    )]
    if getHeppyOption('turbo'):
        comp.fineSplitFactor = int(getHeppyOption('turbo'))
        comp.splitFactor = 1
    else:
        comp.fineSplitFactor = 1
        comp.splitFactor = 1 if getHeppyOption('single') else 5
    selectedComponents = [ comp ]
    if getHeppyOption('events'): insertEventSelector(sequence)
    doECalCorrections(sync=True)
    doKalmanMuonCorrections(sync=True)



config = autoConfig(selectedComponents, sequence)

