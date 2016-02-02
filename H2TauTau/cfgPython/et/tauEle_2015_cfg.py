import PhysicsTools.HeppyCore.framework.config as cfg
from PhysicsTools.HeppyCore.framework.config import printComps
from PhysicsTools.Heppy.utils.cmsswPreprocessor import CmsswPreprocessor

# Tau-tau analyzers
from CMGTools.H2TauTau.proto.analyzers.TauEleAnalyzer import TauEleAnalyzer
from CMGTools.H2TauTau.proto.analyzers.H2TauTauTreeProducerTauEle import H2TauTauTreeProducerTauEle
from CMGTools.H2TauTau.proto.analyzers.DYLLReweighterTauEle import DYLLReweighterTauEle
from CMGTools.H2TauTau.proto.analyzers.TauDecayModeWeighter import TauDecayModeWeighter
from CMGTools.H2TauTau.proto.analyzers.TauFakeRateWeighter import TauFakeRateWeighter
from CMGTools.H2TauTau.proto.analyzers.LeptonWeighter import LeptonWeighter
from CMGTools.H2TauTau.proto.analyzers.SVfitProducer import SVfitProducer
from CMGTools.H2TauTau.proto.analyzers.FileCleaner import FileCleaner

# common configuration and sequence
from CMGTools.H2TauTau.htt_ntuple_base_cff import commonSequence, genAna, dyJetsFakeAna, puFileData, puFileMC, eventSelector

# e-tau specific configuration settings

# 'Nom', 'Up', 'Down', or None
shift = None
computeSVfit = False
production = False  # production = True run on batch, production = False run locally
syncntuple = True
cmssw = False


dyJetsFakeAna.channel = 'et'

# Define e-tau specific modules

tauEleAna = cfg.Analyzer(
    TauEleAnalyzer,
    name='TauEleAnalyzer',
    pt1=24,
    eta1=2.1,
    iso1=0.1,
    looseiso1=9999.,
    pt2=20,
    eta2=2.3,
    iso2=1.5,
    looseiso2=9999.,
    m_min=10,
    m_max=99999,
    dR_min=0.5,
    from_single_objects=True,
    verbose=False
)

dyLLReweighterTauEle = cfg.Analyzer(
    DYLLReweighterTauEle,
    name='DYLLReweighterTauEle',
    # 2012
    W1p0PB=1.,  # 1.37, # weight for 1 prong 0 Pi Barrel
    W1p0PE=1.,  # 1.11,
    W1p1PB=1.,  # 2.18,
    W1p1PE=1.,  # 0.47,
    verbose=False
)

tauDecayModeWeighter = cfg.Analyzer(
    TauDecayModeWeighter,
    name='TauDecayModeWeighter',
    legs=['leg2']
)

tauFakeRateWeighter = cfg.Analyzer(
    TauFakeRateWeighter,
    name='TauFakeRateWeighter'
)

tauWeighter = cfg.Analyzer(
    LeptonWeighter,
    name='LeptonWeighter_tau',
    scaleFactorFiles = {},
    lepton='leg2',
    disable=True,
)

eleWeighter = cfg.Analyzer(
    LeptonWeighter,
    name='LeptonWeighter_ele',
    scaleFactorFiles={
        'trigger':'$CMSSW_BASE/src/CMGTools/H2TauTau/data/Electron_SingleEle_eff.root',
        'idiso':'$CMSSW_BASE/src/CMGTools/H2TauTau/data/Electron_IdIso0p10_eff.root',
    },
    lepton='leg1',
    disable=False
)

treeProducer = cfg.Analyzer(
    H2TauTauTreeProducerTauEle,
    name='H2TauTauTreeProducerTauEle'
)

syncTreeProducer = cfg.Analyzer(
    H2TauTauTreeProducerTauEle,
    name='H2TauTauSyncTreeProducerTauEle',
    varStyle='sync',
    # skimFunction='event.isSignal'
)


svfitProducer = cfg.Analyzer(
    SVfitProducer,
    name='SVfitProducer',
    # integration='VEGAS',
    integration='MarkovChain',
    # verbose=True,
    # order='21', # muon first, tau second
    l1type='ele',
    l2type='tau'
)

fileCleaner = cfg.Analyzer(
    FileCleaner,
    name='FileCleaner'
)

###################################################
### CONNECT SAMPLES TO THEIR ALIASES AND FILES  ###
###################################################
# from CMGTools.H2TauTau.proto.samples.phys14.connector import httConnector
# my_connect = httConnector('htt_6mar15_manzoni_nom', 'htautau_group',
#                           '.*root', 'et', production=production)
# my_connect.connect()
# MC_list = my_connect.MC_list

from CMGTools.H2TauTau.proto.samples.fall15.htt_common import backgrounds_ele, sm_signals, mssm_signals, data_single_electron, sync_list

from CMGTools.H2TauTau.proto.samples.fall15.triggers_tauEle import mc_triggers, mc_triggerfilters
from CMGTools.H2TauTau.proto.samples.fall15.triggers_tauEle import data_triggers, data_triggerfilters

from CMGTools.RootTools.utils.splitFactor import splitFactor

# Get all heppy options; set via "-o production" or "-o production=True"

samples = backgrounds_ele + sm_signals + mssm_signals + sync_list

split_factor = 1e5

for sample in samples:
    sample.triggers = mc_triggers
    sample.triggerobjects = mc_triggerfilters
    sample.splitFactor = splitFactor(sample, split_factor)

data_list = data_single_electron

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
selectedComponents = samples + data_list

###################################################
###                  SEQUENCE                   ###
###################################################
sequence = commonSequence
sequence.insert(sequence.index(genAna), tauEleAna)
sequence.append(tauDecayModeWeighter)
sequence.append(tauFakeRateWeighter)
sequence.append(tauWeighter)
sequence.append(eleWeighter)
sequence.insert(sequence.index(dyJetsFakeAna) + 1, dyLLReweighterTauEle)
if computeSVfit:
    sequence.append(svfitProducer)
sequence.append(treeProducer)

if syncntuple:
    sequence.append(syncTreeProducer)

if not cmssw:
    module = [s for s in sequence if s.name == 'MCWeighter'][0]
    sequence.remove(module)

###################################################
###             CHERRY PICK EVENTS              ###
###################################################
# eventSelector.toSelect = [186583]
# sequence.insert(0, eventSelector)

###################################################
###            SET BATCH OR LOCAL               ###
###################################################
if not production:
    cache = True
    # comp = my_connect.mc_dict['HiggsGGH125']
    comp = sync_list[0]
    selectedComponents = [comp]
    comp.splitFactor = 5
    comp.fineSplitFactor = 1
#    comp.files = comp.files[:1]

preprocessor = None
if cmssw:
    sequence.append(fileCleaner)
    preprocessor = CmsswPreprocessor("$CMSSW_BASE/src/CMGTools/H2TauTau/prod/h2TauTauMiniAOD_etau_cfg.py", addOrigAsSecondary=False)

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
