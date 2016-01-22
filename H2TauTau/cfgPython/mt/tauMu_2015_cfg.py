import PhysicsTools.HeppyCore.framework.config as cfg

from CMGTools.H2TauTau.tauMu_2015_base_cfg import sequence, treeProducer, tauMuAna

from PhysicsTools.HeppyCore.framework.config import printComps
from PhysicsTools.HeppyCore.framework.heppy_loop import getHeppyOption
from PhysicsTools.Heppy.utils.cmsswPreprocessor import CmsswPreprocessor

from CMGTools.H2TauTau.proto.analyzers.FileCleaner import FileCleaner
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
if cmssw:
    tauMuAna.from_single_objects = False

# Minimal list of samples
samples = backgrounds_mu + sm_signals + mssm_signals + sync_list


split_factor = 2e4

for sample in samples:
    sample.triggers = mc_triggers
    sample.triggerobjects = mc_triggerfilters
    sample.splitFactor = splitFactor(sample, split_factor)
    sample.splitFactor = 50

data_list = data_single_muon

for sample in data_list:
    sample.triggers = data_triggers
    sample.triggerobjects = data_triggerfilters
    sample.splitFactor = splitFactor(sample, split_factor)
    sample.json = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/Cert_246908-260627_13TeV_PromptReco_Collisions15_25ns_JSON_v2.txt'
    sample.lumi = 2260.

###################################################
###              ASSIGN PU to MC                ###
###################################################
for mc in samples:
    mc.puFileData = puFileData
    mc.puFileMC = puFileMC

###################################################
###             SET COMPONENTS BY HAND          ###
###################################################
# selectedComponents = samples + data_list
# selectedComponents = data_list
# selectedComponents = samples
selectedComponents = [s for s in samples if s.name == 'DYJetsToLL_M50_LO']

###################################################
###             CHERRY PICK EVENTS              ###
###################################################

if pick_events:
    eventSelector.toSelect = [486113, 164284, 252066, 399795, 11269]
    sequence.insert(0, eventSelector)

if not syncntuple:
    module = [s for s in sequence if s.name == 'H2TauTauSyncTreeProducerTauMu'][0]
    sequence.remove(module)

if not cmssw:
    module = [s for s in sequence if s.name == 'MCWeighter'][0]
    sequence.remove(module)

###################################################
###            SET BATCH OR LOCAL               ###
###################################################
if not production:
    cache = True
    # comp = samples[0]
    # comp = sync_list[0]
    # selectedComponents = [comp]
    selectedComponents = [selectedComponents[0]]
    comp = selectedComponents[0]
    comp.splitFactor = 1
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
