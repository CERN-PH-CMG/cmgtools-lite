import PhysicsTools.HeppyCore.framework.config as cfg
from PhysicsTools.HeppyCore.framework.config import printComps
from PhysicsTools.HeppyCore.framework.heppy_loop import getHeppyOption
from PhysicsTools.Heppy.utils.cmsswPreprocessor import CmsswPreprocessor


# Tau-tau analyzers
from CMGTools.H2TauTau.proto.analyzers.MuEleAnalyzer import MuEleAnalyzer
from CMGTools.H2TauTau.proto.analyzers.H2TauTauTreeProducerMuEle import H2TauTauTreeProducerMuEle
from CMGTools.H2TauTau.proto.analyzers.DiLeptonWeighter import DiLeptonWeighter
from CMGTools.H2TauTau.proto.analyzers.SVfitProducer import SVfitProducer
from CMGTools.H2TauTau.proto.analyzers.LeptonIsolationCalculator import LeptonIsolationCalculator
from CMGTools.H2TauTau.proto.analyzers.FileCleaner import FileCleaner

# common configuration and sequence
from CMGTools.H2TauTau.htt_ntuple_base_cff import commonSequence, dyJetsFakeAna, puFileData, puFileMC, eventSelector, jetAna

from CMGTools.RootTools.utils.splitFactor import splitFactor
from CMGTools.H2TauTau.proto.samples.spring16.triggers_muEle import mc_triggers, mc_triggerfilters, data_triggers, data_triggerfilters

from CMGTools.H2TauTau.proto.samples.spring16.htt_common import backgrounds_mu, sm_signals, mssm_signals, data_muon_electron, sync_list

# local switches
production = getHeppyOption('production', True)
pick_events = getHeppyOption('pick_events', False)
syncntuple = getHeppyOption('syncntuple', True)
cmssw = getHeppyOption('cmssw', True)
computeSVfit = getHeppyOption('computeSVfit', False)
data = getHeppyOption('data', False)
reapplyJEC = getHeppyOption('reapplyJEC', True)

addIsoInfo = False

# Just to be sure
if production:
    syncntuple = False
    pick_events = False

if reapplyJEC:
    if cmssw:
        jetAna.jetCol = 'patJetsReapplyJEC'
        dyJetsFakeAna.jetCol = 'patJetsReapplyJEC'
    else:
        jetAna.recalibrateJets = True

muonIsoCalc = cfg.Analyzer(
    LeptonIsolationCalculator,
    name='MuonIsolationCalculator',
    lepton='muon',
    getter=lambda event: [event.leg2]
)

electronIsoCalc = cfg.Analyzer(
    LeptonIsolationCalculator,
    name='ElectronIsolationCalculator',
    lepton='electron',
    getter=lambda event: [event.leg1]
)


dyJetsFakeAna.channel = 'em'

# Define mu-ele specific modules

muEleAna = cfg.Analyzer(
    MuEleAnalyzer,
    'MuEleAnalyzer',
    pt1=13.,
    pt1_leading=18.,
    eta1=2.5,
    iso1=0.15,
    looseiso1=9999.,
    pt2=10.,
    pt2_leading=18.,
    eta2=2.4,
    iso2=0.2,
    looseiso2=9999.,
    m_min=0.,
    m_max=99999,
    dR_min=0.3,
    from_single_objects=True,
    verbose=False,
)

leptonWeighter = cfg.Analyzer(
    DiLeptonWeighter,
    name='DiLeptonWeighter',
    scaleFactorFiles={
        'trigger_mu_low': '$CMSSW_BASE/src/CMGTools/H2TauTau/data/Muon_Mu8leg_eff.root',
        'trigger_mu_high': '$CMSSW_BASE/src/CMGTools/H2TauTau/data/Muon_Mu23leg_eff.root',
        'trigger_e_low': '$CMSSW_BASE/src/CMGTools/H2TauTau/data/Electron_Ele12leg_eff.root',
        'trigger_e_high': '$CMSSW_BASE/src/CMGTools/H2TauTau/data/Electron_Ele23leg_eff.root',
        'idiso_mu': '$CMSSW_BASE/src/CMGTools/H2TauTau/data/Muon_IdIso0p20_eff.root',
        'idiso_e': '$CMSSW_BASE/src/CMGTools/H2TauTau/data/Electron_IdIso0p15_eff.root',
    },
    lepton_e='leg1',
    lepton_mu='leg2',
    disable=False
)


treeProducer = cfg.Analyzer(
    H2TauTauTreeProducerMuEle,
    name='H2TauTauTreeProducerMuEle'
)

syncTreeProducer = cfg.Analyzer(
    H2TauTauTreeProducerMuEle,
    name='H2TauTauSyncTreeProducerMuEle',
    varStyle='sync',
)

svfitProducer = cfg.Analyzer(
    SVfitProducer,
    name='SVfitProducer',
    # integration = 'VEGAS'        ,
    integration='MarkovChain',
    # verbose     = True           ,
    # order       = '21'           , # muon first, tau second
    l1type='muon',
    l2type='ele'
)

fileCleaner = cfg.Analyzer(
    FileCleaner,
    name='FileCleaner'
)


if cmssw:
    muEleAna.from_single_objects = False

samples = backgrounds_mu + sm_signals + mssm_signals + sync_list
#samples = backgrounds_mu + sm_signals

split_factor = 1e5

for sample in samples:
    sample.triggers = mc_triggers
    sample.triggerobjects = mc_triggerfilters
    sample.splitFactor = splitFactor(sample, split_factor)

data_list = data_muon_electron

for sample in data_list:
    sample.triggers = data_triggers
    sample.triggerobjects = data_triggerfilters
    sample.splitFactor = splitFactor(sample, split_factor)


###################################################
###              ASSIGN PU to MC                ###
###################################################
for mc in samples:
    mc.puFileData = puFileData
    mc.puFileMC = puFileMC

###################################################
###             SET COMPONENTS BY HAND          ###
###################################################
#selectedComponents = samples
selectedComponents = data_list if data else samples
#selectedComponents = data_list
#selectedComponents = samples


###################################################
###                  SEQUENCE                   ###
###################################################
sequence = commonSequence
sequence.insert(sequence.index(dyJetsFakeAna), muEleAna)
sequence.append(leptonWeighter)
if computeSVfit:
    sequence.append(svfitProducer)
sequence.append(treeProducer)
if syncntuple:
    sequence.append(syncTreeProducer)


if addIsoInfo:
    treeProducer.addIsoInfo = False
    sequence.insert(sequence.index(treeProducer), muonIsoCalc)
    sequence.insert(sequence.index(treeProducer), electronIsoCalc)



if not cmssw:
    module = [s for s in sequence if s.name == 'MCWeighter'][0]
    sequence.remove(module)


###################################################
###             CHERRY PICK EVENTS              ###
###################################################

if pick_events:
    eventSelector.toSelect = [329583, 28471, 348428, 319508]
    sequence.insert(0, eventSelector)

###################################################
###            SET BATCH OR LOCAL               ###
###################################################
if not production:
    cache = True
    comp = data_list[-1] if data else sync_list[0]
    selectedComponents = [comp]
    comp.splitFactor = 1 if pick_events else 4
    comp.fineSplitFactor = 1
#  comp.files           = comp.files[:1]

preprocessor = None
if cmssw:
    fname = "$CMSSW_BASE/src/CMGTools/H2TauTau/prod/h2TauTauMiniAOD_emu_data_cfg.py" if data else "$CMSSW_BASE/src/CMGTools/H2TauTau/prod/h2TauTauMiniAOD_emu_cfg.py"

    sequence.append(fileCleaner)
    preprocessor = CmsswPreprocessor(fname, addOrigAsSecondary=False)

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
