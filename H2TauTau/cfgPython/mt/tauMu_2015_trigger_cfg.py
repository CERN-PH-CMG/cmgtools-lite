import PhysicsTools.HeppyCore.framework.config as cfg

from CMGTools.H2TauTau.tauMu_2015_base_cfg import sequence, treeProducer

from PhysicsTools.HeppyCore.framework.config import printComps
from PhysicsTools.HeppyCore.framework.heppy_loop import getHeppyOption
from PhysicsTools.Heppy.utils.cmsswPreprocessor import CmsswPreprocessor

from CMGTools.H2TauTau.proto.analyzers.FileCleaner import FileCleaner
from CMGTools.H2TauTau.proto.analyzers.L1TriggerAnalyzer import L1TriggerAnalyzer
from CMGTools.H2TauTau.proto.analyzers.TauIsolationCalculator import TauIsolationCalculator
from CMGTools.H2TauTau.proto.analyzers.MuonIsolationCalculator import MuonIsolationCalculator

from CMGTools.RootTools.utils.splitFactor import splitFactor
# from CMGTools.H2TauTau.proto.samples.spring15.htt_common import backgrounds_mu, sm_signals, mssm_signals, data_single_muon, sync_list
# from CMGTools.H2TauTau.proto.samples.spring15.triggers_tauMu import mc_triggers, mc_triggerfilters
from CMGTools.H2TauTau.proto.samples.data15.data import data_single_muon
from CMGTools.H2TauTau.proto.samples.fall15.triggers_tauMu import data_triggers, data_triggerfilters
from CMGTools.H2TauTau.proto.samples.fall15.higgs import HiggsGGH125, HiggsGGH130, HiggsVBF120, HiggsVBF125, HiggsVBF130
from CMGTools.H2TauTau.proto.samples.fall15.ewk import dy_inclusive, dy_jet_bins, dy_ht_bins
from CMGTools.H2TauTau.htt_ntuple_base_cff import puFileData, puFileMC, eventSelector

# Get all heppy options; set via "-o production" or "-o production=True"

# production = True run on batch, production = False (or unset) run locally
production = getHeppyOption('production')
production    = True
pick_events   = False
syncntuple    = False
cmssw         = False
singleObjects = True
computeSVfit  = False

# Define extra modules
tauIsoCalc = cfg.Analyzer(
    TauIsolationCalculator,
    name   = 'TauIsolationCalculator',
    getter = lambda event: [event.leg2]
)

muonIsoCalc = cfg.Analyzer(
    MuonIsolationCalculator,
    name   = 'MuonIsolationCalculator',
    getter = lambda event: [event.leg1]
)

fileCleaner = cfg.Analyzer(
    FileCleaner,
    name = 'FileCleaner'
)

sequence.insert(sequence.index(treeProducer), muonIsoCalc)
sequence.insert(sequence.index(treeProducer), tauIsoCalc)

treeProducer.addIsoInfo = True

# samples = dy_inclusive + dy_jet_bins + dy_ht_bins + [HiggsGGH125, HiggsGGH130, HiggsVBF120, HiggsVBF125, HiggsVBF130]
# samples = dy_inclusive + [HiggsGGH125, HiggsGGH130, HiggsVBF120, HiggsVBF125, HiggsVBF130]
samples = dy_jet_bins + dy_ht_bins

split_factor = 1e5

for sample in samples:
#     sample.triggers = mc_triggers # RIC: override if necessary with the trigger used for Tagging the event, e.g. sample.triggers = ['HLT_IsoMu17_eta2p1_v1', 'HLT_IsoMu17_eta2p1_v2']
    sample.triggers  = ['HLT_IsoMu17_eta2p1_v%d' %i for i in range(1, 6)]
    sample.triggers += ['HLT_IsoMu18_v%d'        %i for i in range(1, 6)]
    sample.triggerobjects = [
        'hltL3crIsoL1sMu16L1f0L2f10QL3f18QL3trkIsoFiltered0p09',
        'hltL3crIsoL1sSingleMu16erL1f0L2f10QL3f17QL3trkIsoFiltered0p09'
    ]
    sample.splitFactor = splitFactor(sample, split_factor)

data_list = data_single_muon

for sample in data_list:
    sample.triggers = data_triggers # RIC: override if necessary with the trigger used for Tagging the event, e.g. sample.triggers = ['HLT_IsoMu17_eta2p1_v1', 'HLT_IsoMu17_eta2p1_v2']
    sample.triggerobjects = data_triggerfilters
    sample.splitFactor = splitFactor(sample, split_factor)
    sample.json = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/Cert_246908-260627_13TeV_PromptReco_Collisions15_25ns_JSON.txt'
    sample.lumi = 2110.

###################################################
###              ASSIGN PU to MC                ###
###################################################
for mc in samples:
    mc.puFileData = puFileData
    mc.puFileMC   = puFileMC

###################################################
###             SET COMPONENTS BY HAND          ###
###################################################
# selectedComponents = data_list
selectedComponents = samples

###################################################
###          AD HOC L1 TRIGGER ANALYZER         ###
###################################################
L1TriggerAnalyzer = cfg.Analyzer(
    L1TriggerAnalyzer,
    name        = 'L1TriggerAnalyzer',
    collections = ['IsoTau', 'Tau', 'Muon'],
    label       = 'l1extraParticles', # RIC: 'hltL1extraPArticles' if L1 is rerun on MC
    dR          = 0.5
)

###################################################
###             CHERRY PICK EVENTS              ###
###################################################

if pick_events:
    eventSelector.toSelect = [486113, 164284, 252066, 399795, 11269]
    sequence.insert(0, eventSelector)

###################################################
###                  SEQUENCE                   ###
###################################################

for i, module in enumerate(sequence):

    if module.name == 'TauMuAnalyzer': 
        module.from_single_objects = singleObjects
        # RIC: save the trigger objects with FILTERNAME
        # that match to leg number LEG (1 or 2)
        module.triggerObjectsHandle = ('selectedPatTrigger', '', 'PAT')
        sequence.insert(i+1, L1TriggerAnalyzer)

    if module.name == 'TriggerAnalyzer': 
        module.addTriggerObjects = True
        module.requireTrigger = True
        # RIC: HLT paths to Probe
#         module.extraTrig = [
#             'HLT_IsoMu17_eta2p1_LooseIsoPFTau20_SingleL1_v4', 
#         ]
        module.extraTrig = ['HLT_IsoMu17_eta2p1_MediumIsoPFTau35_Trk1_eta2p1_Reg_v%d' %i for i in range(1, 6)]
        module.saveFlag = True
        # RIC specify the collections to be used. 
        # Useful if trigger is rerun with another process name.
        # Defaults to PAT
        module.triggerResultsHandle = ('TriggerResults'    , '', 'HLT')
        module.triggerObjectsHandle = ('selectedPatTrigger', '', 'PAT')

    if module.name == 'H2TauTauTreeProducerTauMu': 
        module.addTnPInfo = True

if not syncntuple:
    module = [s for s in sequence if s.name == 'H2TauTauSyncTreeProducerTauMu'][0]
    sequence.remove(module)

if not computeSVfit and len([s for s in sequence if s.name == 'SVfitProducer']):
    module = [s for s in sequence if s.name == 'SVfitProducer'][0]
    sequence.remove(module)

if not cmssw and len([s for s in sequence if s.name == 'MCWeighter']):
    module = [s for s in sequence if s.name == 'MCWeighter'][0]
    sequence.remove(module)
    
print sequence

###################################################
###            SET BATCH OR LOCAL               ###
###################################################
if not production:
    comp                 = HiggsGGH125
    selectedComponents   = [comp]
    comp.splitFactor     = 1
    comp.fineSplitFactor = 1
    comp.files           = comp.files[:1]

preprocessor = None
if cmssw:
    sequence.append(fileCleaner)
    preprocessor = CmsswPreprocessor("$CMSSW_BASE/src/CMGTools/H2TauTau/prod/h2TauTauMiniAOD_mutau_cfg.py", addOrigAsSecondary=False)

# the following is declared in case this cfg is used in input to the
# heppy.py script
from PhysicsTools.HeppyCore.framework.eventsfwlite import Events
config = cfg.Config(
    components   = selectedComponents,
    sequence     = sequence,
    services     = [],
    preprocessor = preprocessor,
    events_class = Events
)

printComps(config.components, True)

def modCfgForPlot(config):
    config.components = []
