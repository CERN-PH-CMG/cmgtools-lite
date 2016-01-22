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
from CMGTools.H2TauTau.proto.samples.spring15.htt_common import backgrounds_mu, sm_signals, mssm_signals, data_single_muon, sync_list
from CMGTools.H2TauTau.proto.samples.spring15.triggers_tauMu import mc_triggers, mc_triggerfilters
from CMGTools.H2TauTau.proto.samples.spring15.triggers_tauMu import data_triggers, data_triggerfilters

from CMGTools.H2TauTau.htt_ntuple_base_cff import puFileData, puFileMC, eventSelector

# Get all heppy options; set via "-o production" or "-o production=True"

# production = True run on batch, production = False (or unset) run locally
production = getHeppyOption('production')
production = False
pick_events = False
syncntuple = False
cmssw = False
singleObjects = True
computeSVfit = False

# Define extra modules
tauIsoCalc = cfg.Analyzer(
    TauIsolationCalculator,
    name='TauIsolationCalculator',
    getter=lambda event: [event.leg2]
)

muonIsoCalc = cfg.Analyzer(
    MuonIsolationCalculator,
    name='MuonIsolationCalculator',
    getter=lambda event: [event.leg1]
)

fileCleaner = cfg.Analyzer(
    FileCleaner,
    name='FileCleaner'
)

sequence.insert(sequence.index(treeProducer), muonIsoCalc)
sequence.insert(sequence.index(treeProducer), tauIsoCalc)

treeProducer.addIsoInfo = True

# Minimal list of samples
samples = backgrounds_mu + sm_signals + mssm_signals + sync_list


split_factor = 1e5

for sample in samples:
#     sample.triggers = mc_triggers # RIC: override if necessary with the trigger used for Tagging the event, e.g. sample.triggers = ['HLT_IsoMu17_eta2p1_v1', 'HLT_IsoMu17_eta2p1_v2']
    sample.triggers = ['HLT_IsoMu17_eta2p1_v1', 'HLT_IsoMu17_eta2p1_v2'] # RIC: override if necessary with the trigger used for Tagging the event, e.g. sample.triggers = ['HLT_IsoMu17_eta2p1_v1', 'HLT_IsoMu17_eta2p1_v2']
    sample.triggerobjects = mc_triggerfilters
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
    mc.puFileMC = puFileMC

###################################################
###             SET COMPONENTS BY HAND          ###
###################################################
selectedComponents = samples + data_list
# selectedComponents = data_list
# selectedComponents = samples

###################################################
###          AD HOC L1 TRIGGER ANALYZER         ###
###################################################
L1TriggerAnalyzer = cfg.Analyzer(
    L1TriggerAnalyzer,
    name='L1TriggerAnalyzer',
    collections=['IsoTau', 'Tau', 'Muon'],
    label='L1extraParticles', # RIC: 'hltL1extraPArticles' if L1 is rerun on MC
    dR=0.5
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

if not syncntuple:
    module = [s for s in sequence if s.name == 'H2TauTauSyncTreeProducerTauMu'][0]
    sequence.remove(module)

if not cmssw:
    module = [s for s in sequence if s.name == 'MCWeighter'][0]
    sequence.remove(module)

if not singleObjects:
    module = [s for s in sequence if s.name == 'MuTauAnalyzer'][0]
    module.from_single_objects = True

if not computeSVfit:
    module = [s for s in sequence if s.name == 'SVfitProducer'][0]
    sequence.remove(module)

module = [s for s in sequence if s.name == 'TriggerAnalyzer'][0]
module.requireTrigger = True
# RIC: HLT paths to Probe
module.extraTrig = [
    'HLT_IsoMu17_eta2p1_MediumIsoPFTau35_Trk1_eta2p1_Reg_v1', 
    'HLT_IsoMu17_eta2p1_MediumIsoPFTau35_Trk1_eta2p1_Reg_v2'
]
module.saveFlag = True
# RIC specify the collections to be used. 
# Useful if trigger is rerun with another process name.
# Defaults to PAT
module.triggerResultsHandle = ('TriggerResults', '', 'PAT')
module.triggerObjectsHandle = ('selectedPatTrigger', '', 'PAT')

module = [s for s in sequence if s.name == 'H2TauTauTreeProducerTauMu'][0]
module.addTnPInfo = True

module = [s for s in sequence if s.name == 'TauMuAnalyzer'][0]
# RIC: save the trigger objects with FILTERNAME
# that match to leg number LEG (1 or 2)
# module.filtersToMatch = (['FILTERNAME'], LEG)
# module.filtersToMatch = (['hltL2Tau30eta2p2'], 2)
module.triggerObjectsHandle = ('selectedPatTrigger', '', 'PAT')
sequence.insert(i+1, L1TriggerAnalyzer)
    
print sequence

###################################################
###            SET BATCH OR LOCAL               ###
###################################################
if not production:
    cache = True
    # comp = samples[0]
    comp = sync_list[0]
    selectedComponents = [comp]
    comp.splitFactor = 100
    comp.fineSplitFactor = 1
    # comp.files = comp.files[]

preprocessor = None
if cmssw:
    sequence.append(fileCleaner)
    preprocessor = CmsswPreprocessor("$CMSSW_BASE/src/CMGTools/H2TauTau/prod/h2TauTauMiniAOD_mutau_cfg.py", addOrigAsSecondary=False)

# the following is declared in case this cfg is used in input to the
# heppy.py script
from PhysicsTools.HeppyCore.framework.eventsfwlite import Events
config = cfg.Config(components=selectedComponents,
                    sequence=sequence,
                    services=[],
                    preprocessor=preprocessor,
                    events_class=Events
                    )

printComps(config.components, True)

def modCfgForPlot(config):
    config.components = []
