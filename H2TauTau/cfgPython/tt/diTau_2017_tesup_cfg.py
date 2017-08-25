import os
import PhysicsTools.HeppyCore.framework.config as cfg
from PhysicsTools.HeppyCore.framework.config import printComps
from PhysicsTools.HeppyCore.framework.heppy_loop import getHeppyOption as _getHeppyOption
from PhysicsTools.Heppy.utils.cmsswPreprocessor import CmsswPreprocessor

# Tau-tau analyzers
from CMGTools.H2TauTau.proto.analyzers.FileCleaner import FileCleaner
from CMGTools.H2TauTau.proto.analyzers.TauTauAnalyzer import TauTauAnalyzer
from CMGTools.H2TauTau.proto.analyzers.H2TauTauTreeProducerTauTau import H2TauTauTreeProducerTauTau
from CMGTools.H2TauTau.proto.analyzers.TauDecayModeWeighter import TauDecayModeWeighter
from CMGTools.H2TauTau.proto.analyzers.LeptonWeighter import LeptonWeighter
from CMGTools.H2TauTau.proto.analyzers.TauP4Scaler import TauP4Scaler
from CMGTools.H2TauTau.proto.analyzers.SVfitProducer import SVfitProducer
from CMGTools.H2TauTau.proto.analyzers.L1TriggerAnalyzer import L1TriggerAnalyzer
from CMGTools.H2TauTau.proto.analyzers.MT2Analyzer import MT2Analyzer
from CMGTools.H2TauTau.proto.analyzers.METFilter import METFilter

# common configuration and sequence
from CMGTools.H2TauTau.htt_ntuple_base_cff import commonSequence, httGenAna, puFileData, puFileMC, eventSelector, susyCounter, susyScanAna, jetAna, recoilCorr, mcWeighter, triggerAna, lheWeightAna

def getHeppyOption(option, default):
    opt = _getHeppyOption(option, default)
    if opt in ['False', 'false']:
        opt = False
    return opt


# Get all heppy options; set via '-o production' or '-o production=True'

# production = True run on batch, production = False (or unset) run locally
production = getHeppyOption('production', True)
pick_events = getHeppyOption('pick_events', False)
syncntuple = getHeppyOption('syncntuple', True)
cmssw = getHeppyOption('cmssw', True)
doSUSY = getHeppyOption('susy', True)
computeSVfit = getHeppyOption('computeSVfit', False)
data = getHeppyOption('data', False)
tes_string = getHeppyOption('tes_string', '') # '_tesup' '_tesdown'
reapplyJEC = getHeppyOption('reapplyJEC', False)
calibrateTaus = getHeppyOption('calibrateTaus', False)
scaleTaus = getHeppyOption('scaleTaus', False)
correct_recoil = getHeppyOption('correct_recoil', True)

if doSUSY:
    cmssw = False

scaleTaus = True
tes_scale = 1.03

# Just to be sure
if production:
    syncntuple = False
    pick_events = False

if reapplyJEC:
    if cmssw:
        jetAna.jetCol = 'patJetsReapplyJEC'
        httGenAna.jetCol = 'patJetsReapplyJEC'
    else:
        jetAna.recalibrateJets = True
        jetAna.mcGT = 'Summer16_23Sep2016V3_MC'
        jetAna.dataGT = 'Summer16_23Sep2016HV3_DATA'
        # Summer16_23Sep2016EFV3_DATA
        # Summer16_23Sep2016GV3_DATA

if not data:
    triggerAna.requireTrigger = False

if correct_recoil:
    recoilCorr.apply = True

# Define tau-tau specific modules

tauP4Scaler = cfg.Analyzer(
    class_object=TauP4Scaler,
    name='TauP4Scaler',
)


tauTauAna = cfg.Analyzer(
    class_object=TauTauAnalyzer,
    name='TauTauAnalyzer',
    pt1=40.,
    eta1=2.1,
    iso1=1.,
    looseiso1=999999999.,
    pt2=40.,
    eta2=2.1,
    iso2=1.,
    looseiso2=999999999.,
    isolation='byIsolationMVArun2v1DBoldDMwLTraw',
    m_min=10,
    m_max=99999,
    dR_min=0.5,
    jetPt=30.,
    jetEta=4.7,
    relaxJetId=False,
    verbose=False,
    from_single_objects=False,
    ignoreTriggerMatch=True, 
    scaleTaus=calibrateTaus or scaleTaus,
    tes_scale=tes_scale
)

if not cmssw:
    tauTauAna.from_single_objects = True

tauTauMT2Ana = cfg.Analyzer(
    MT2Analyzer, name='MT2Analyzer',
    metCollection="slimmedMETs",
    doOnlyDefault=False,
    jetPt=40.,
    collectionPostFix="",
    verbose=True
)

# For the moment not needed in 2016

# l1Ana = cfg.Analyzer(
#     class_object=L1TriggerAnalyzer,
#     name='L1TriggerAnalyzer',
#     collections=['IsoTau'],
#     requireMatches=['leg1', 'leg2'],
#     dR=0.5
# )

fileCleaner = cfg.Analyzer(
    FileCleaner,
    name='FileCleaner'
)

# tau1Calibration = cfg.Analyzer(
#   TauP4Scaler       ,
#   'TauP4Scaler_tau1',
#   leg      = 'leg1' ,
#   method   = 'peak' ,
#   scaleMET = True   ,
#   verbose  = False  ,
#   )

# tau2Calibration = cfg.Analyzer(
#   TauP4Scaler       ,
#   'TauP4Scaler_tau2',
#   leg      = 'leg2' ,
#   method   = 'peak' ,
#   scaleMET = True   ,
#   verbose  = False  ,
#   )

tauDecayModeWeighter = cfg.Analyzer(
    TauDecayModeWeighter,
    name='TauDecayModeWeighter',
    legs=['leg1', 'leg2'],
)

tau1Weighter = cfg.Analyzer(
    LeptonWeighter,
    name='LeptonWeighter_tau1',
    scaleFactorFiles={
        'trigger': ('$CMSSW_BASE/src/CMGTools/H2TauTau/data/htt_scalefactors_v16_5.root', 't_genuine_TightIso_tt'),
        # 'trigger': '$CMSSW_BASE/src/CMGTools/H2TauTau/data/Tau_diTau35_summer16.py',  # include in the event's overall weight
    },

    otherScaleFactorFiles={
        #'trigger_up': '$CMSSW_BASE/src/CMGTools/H2TauTau/data/Tau_diTau35_spring16_up.py',  # DO NOT include in the event's overall weight
        #'trigger_down': '$CMSSW_BASE/src/CMGTools/H2TauTau/data/Tau_diTau35_spring16_down.py',  # DO NOT include in the event's overall weight
    },
    lepton='leg1',
    verbose=True,
    disable=False,
)

tau2Weighter = cfg.Analyzer(
    LeptonWeighter,
    name='LeptonWeighter_tau2',
    scaleFactorFiles={
        'trigger': ('$CMSSW_BASE/src/CMGTools/H2TauTau/data/htt_scalefactors_v16_5.root', 't_genuine_TightIso_tt'),
        # 'trigger': '$CMSSW_BASE/src/CMGTools/H2TauTau/data/Tau_diTau35_summer16.py',  # include in the event's overall weight
    },

    otherScaleFactorFiles={
        #'trigger_up': '$CMSSW_BASE/src/CMGTools/H2TauTau/data/Tau_diTau35_spring16_up.py',  # DO NOT include in the event's overall weight
    #'trigger_down': '$CMSSW_BASE/src/CMGTools/H2TauTau/data/Tau_diTau35_spring16_down.py',  # DO NOT include in the event's overall weight
    },
    lepton='leg2',
    verbose=True,
    disable=False,
)

if doSUSY:
    for module in tau1Weighter, tau2Weighter:
        module.dataEffFiles = module.scaleFactorFiles
        module.scaleFactorFiles = {}
    lheWeightAna.useLumiInfo = True

treeProducer = cfg.Analyzer(
    H2TauTauTreeProducerTauTau,
    name='H2TauTauTreeProducerTauTau',
    isSUSY=doSUSY,
    skimFunction='event.leptonAccept and event.thirdLeptonVeto and event.otherLeptonVeto'
)

syncTreeProducer = cfg.Analyzer(
    H2TauTauTreeProducerTauTau,
    name='H2TauTauSyncTreeProducerTauTau',
    varStyle='sync',
    treename='sync_tree',
    skimFunction=' and '.join(['event.'+met_filter for met_filter in ['Flag_HBHENoiseFilter', 'Flag_HBHENoiseIsoFilter', 'Flag_EcalDeadCellTriggerPrimitiveFilter', 'Flag_goodVertices', 'Flag_eeBadScFilter', 'Flag_globalTightHalo2016Filter', 'passBadMuonFilter', 'passBadChargedHadronFilter']])
)

svfitProducer = cfg.Analyzer(
    SVfitProducer,
    name='SVfitProducer',
    integration='MarkovChain',  # 'VEGAS'
    integrateOverVisPtResponse=False,
    visPtResponseFile=os.environ['CMSSW_BASE']+'/src/CMGTools/SVfitStandalone/data/svFitVisMassAndPtResolutionPDF.root',  # Christian's for uncalibrated taus
    verbose=False,
    l1type='tau',
    l2type='tau'
)

metFilter = cfg.Analyzer(
    METFilter,
    name='METFilter',
    processName='AOD',
    triggers=[
        'Flag_HBHENoiseFilter', 
        'Flag_HBHENoiseIsoFilter', 
        'Flag_EcalDeadCellTriggerPrimitiveFilter',
        'Flag_goodVertices',
        'Flag_eeBadScFilter',
        'Flag_globalTightHalo2016Filter'
    ]
)

###################################################
### CONNECT SAMPLES TO THEIR ALIASES AND FILES  ###
###################################################
from CMGTools.RootTools.utils.splitFactor import splitFactor
from CMGTools.H2TauTau.proto.samples.summer16.htt_common import backgrounds, sm_signals, mssm_signals, data_tau, sync_list
from CMGTools.H2TauTau.proto.samples.summer16.sms import samples_susy
# from CMGTools.RootTools.samples.samples_13TeV_signals import SignalSUSY
from CMGTools.H2TauTau.proto.samples.summer16.triggers_tauTau import mc_triggers, mc_triggerfilters, data_triggers, data_triggerfilters

data_list = data_tau
samples = backgrounds + sm_signals + sync_list #+ mssm_signals 
if doSUSY:
    samples = samples_susy #+ SignalSUSY[:1]
split_factor = 1e5

for sample in data_list:
    sample.triggers = data_triggers
    sample.triggerobjects = data_triggerfilters
    sample.splitFactor = splitFactor(sample, split_factor)

for sample in samples:
    sample.triggers = mc_triggers
    sample.triggerobjects = mc_triggerfilters
    sample.splitFactor = splitFactor(sample, split_factor)

###################################################
###              ASSIGN PU to MC                ###
###################################################
for mc in samples:
    mc.puFileData = puFileData
    mc.puFileMC = puFileMC
    if 'PUSpring16' in mc.dataset:
        print 'Attaching Spring 16 pileup to sample', mc.dataset
        # mc.puFileData = '$CMSSW_BASE/src/CMGTools/H2TauTau/data/data_pu_25-07-2016_69p2mb_60.root'
        mc.puFileMC = '$CMSSW_BASE/src/CMGTools/H2TauTau/data/MC_Spring16_PU25_Startup_800.root'

###################################################
###             SET COMPONENTS BY HAND          ###
###################################################
selectedComponents = samples
# selectedComponents = samples_susy
if data:
    selectedComponents = data_list

###################################################
###                  SEQUENCE                   ###
###################################################
sequence = commonSequence
if calibrateTaus:
    sequence.insert(sequence.index(httGenAna), tauP4Scaler)
sequence.insert(sequence.index(httGenAna)+1, tauTauAna)
# sequence.insert(sequence.index(genAna), l1Ana)
# sequence.append(tau1Calibration)
# sequence.append(tau2Calibration)
sequence.append(tauDecayModeWeighter)
sequence.append(tau1Weighter)
sequence.append(tau2Weighter)
sequence.append(tauTauMT2Ana)
sequence.append(metFilter)
if doSUSY:
    sequence.insert(sequence.index(mcWeighter) + 1, susyScanAna)
    sequence.insert(sequence.index(susyScanAna) + 1, susyCounter)
if computeSVfit:
    sequence.append(svfitProducer)
sequence.append(treeProducer)
if syncntuple:
    sequence.append(syncTreeProducer)
if not cmssw:
    mcWeighter.activate = False

###################################################
###             CHERRY PICK EVENTS              ###
###################################################
if pick_events:
    evtsToPick = [7125, 7204, 19150, 19157, 30297, 67087, 74521, 87615, 93964, 13385, 19948, 21748, 22048, 68695, 68980, 90677, 4019, 5003, 5228, 33261, 48241, 40571, 17727, 42382, 42762, 52834, 52756, 76821, 70141, 4266, 26879, 36797, 92495, 401, 3451, 3526, 32430, 15065, 48579, 44338, 88971, 6115, 55642, 1616, 43645, 51727, 57548, 27953, 22307, 38311, 43239, 43257, 55067, 62198, 76475, 79555, 45228, 91707]

    eventSelector.toSelect = evtsToPick
    sequence.insert(0, eventSelector)

# # output histogram
outputService = []
if doSUSY:
    from PhysicsTools.HeppyCore.framework.services.tfile import TFileService
    output_service = cfg.Service(
        TFileService,
        'outputfile',
        name="outputfile",
        fname='H2TauTauTreeProducerTauTau/tree.root',
        option='recreate'
    )
    outputService.append(output_service)

###################################################
###            SET BATCH OR LOCAL               ###
###################################################
if not production:
    # comp = data_list[0] if data else sync_list[0]
    # comp = SMS
    # comp = samples_susy[1]
    selectedComponents = samples_susy if doSUSY else sync_list
    if data:
        selectedComponents = [data_list[0]]
    selectedComponents = selectedComponents[:1]
    for comp in selectedComponents:
        comp.splitFactor = 1
        comp.fineSplitFactor = 1
    # comp.files = comp.files[13:20]

# selectedComponents = selectedComponents[-1:]

if doSUSY:
    from CMGTools.RootTools.samples.autoAAAconfig import autoAAA
    autoAAA(selectedComponents)

preprocessor = None
if cmssw:
    sequence.append(fileCleaner)
    cfg_name = "$CMSSW_BASE/src/CMGTools/H2TauTau/prod/h2TauTauMiniAOD_ditau_data_cfg.py" if data else "$CMSSW_BASE/src/CMGTools/H2TauTau/prod/h2TauTauMiniAOD_ditau_cfg.py"
    preprocessor = CmsswPreprocessor(cfg_name, addOrigAsSecondary=False)

# the following is declared in case this cfg is used in input to the
# heppy.py script
from PhysicsTools.HeppyCore.framework.eventsfwlite import Events

config = cfg.Config(components=selectedComponents,
                    sequence=sequence,
                    services=outputService,
                    preprocessor=preprocessor,
                    events_class=Events
                    )

printComps(config.components, True)
