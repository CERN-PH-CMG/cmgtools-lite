import PhysicsTools.HeppyCore.framework.config as cfg
from PhysicsTools.HeppyCore.framework.config import printComps

from PhysicsTools.Heppy.analyzers.core.SkimAnalyzerCount import SkimAnalyzerCount
from CMGTools.H2TauTau.proto.analyzers.TauFRTreeProducer import TauFRTreeProducer
from CMGTools.H2TauTau.proto.analyzers.TauGenTreeProducer import TauGenTreeProducer
from CMGTools.H2TauTau.proto.analyzers.JetAnalyzer import JetAnalyzer
from CMGTools.H2TauTau.proto.analyzers.TauJetMuAnalyzer import TauJetMuAnalyzer
from CMGTools.H2TauTau.proto.analyzers.LeptonWeighter import LeptonWeighter

from CMGTools.RootTools.utils.splitFactor import splitFactor
from CMGTools.H2TauTau.proto.samples.fall15.htt_common import backgrounds_mu, sm_signals, mssm_signals, data_single_muon, sync_list, WJetsHT
from CMGTools.H2TauTau.proto.samples.fall15.triggers_tauMu import mc_triggers, mc_triggerfilters
from CMGTools.H2TauTau.proto.samples.fall15.triggers_tauMu import data_triggers, data_triggerfilters

from CMGTools.H2TauTau.htt_ntuple_base_cff import genAna, vertexAna, puFileData, puFileMC, eventSelector, jsonAna, triggerAna, pileUpAna, httGenAna, NJetsAna


# Get all heppy options; set via "-o production" or "-o production=True"

# production = True run on batch, production = False (or unset) run locally

production = True

skimAna = cfg.Analyzer(
    SkimAnalyzerCount,
    name='SkimAnalyzerCount'
)

tauJetMuAna = cfg.Analyzer(
    TauJetMuAnalyzer,
    name='TauJetMuAnalyzer',
    pt1=20.,
    eta1=2.1,
    iso1=0.1,
    looseiso1=0.1,
    pt2=13., # looser cut because of subsequente jet re-calibration - 7 GeV difference to 20 should be fine
    eta2=2.3,
    iso2=None,
    looseiso2=None,
    m_min=10,
    m_max=99999,
    dR_min=0.5,
    from_single_objects=True,
    verbose=False
)

treeProducer = cfg.Analyzer(
    TauFRTreeProducer,
    name='TauFRTreeProducer'
)

genTreeProducer = cfg.Analyzer(
    TauGenTreeProducer,
    name='TauGenTreeProducer'
)

jetAna = cfg.Analyzer(
    JetAnalyzer,
    name='JetAnalyzer',
    jetCol='slimmedJets',  # <- These are CHS jets
    jetPt=20.,
    jetEta=2.3,
    relaxJetId=False,
    relaxPuJetId=True,
    jerCorr=False,
    ptUncTolerance=True, # require pt > 20 for either central JEC or up/down
    leptonCollections={'slimmedMuons':'std::vector<pat::Muon>', 'slimmedElectrons':'std::vector<pat::Electron>'},
    recalibrateJets=True,
    puJetIDDisc='pileupJetId:fullDiscriminant',
)

muonWeighter = cfg.Analyzer(
    LeptonWeighter,
    name='LeptonWeighter_mu',
    scaleFactorFiles={
        'trigger':'$CMSSW_BASE/src/CMGTools/H2TauTau/data/Muon_IsoMu18_fall15.root',
        'idiso':'$CMSSW_BASE/src/CMGTools/H2TauTau/data/Muon_IdIso0p1_fall15.root',
    },
    lepton='leg1',
    disable=False
)


# Minimal list of samples
samples = backgrounds_mu +WJetsHT#+ sm_signals#+ sync_list + mssm_signals


split_factor = 5e3
split_factor = 5e5

for sample in samples:
    sample.triggers = mc_triggers
    sample.triggerobjects = mc_triggerfilters
    sample.splitFactor = splitFactor(sample, split_factor)

data_list = data_single_muon

for sample in data_list:
    sample.triggers = data_triggers
    sample.triggerobjects = data_triggerfilters
    sample.splitFactor = splitFactor(sample, split_factor)
    sample.json = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/Cert_246908-260627_13TeV_PromptReco_Collisions15_25ns_JSON_v2.txt'
    sample.lumi = 2300.

selectedComponents = samples + data_list

selectedComponents = [s for s in selectedComponents if not ('DY' in s.name and 'Jets' in s.name and not 'DYJets' in s.name)]
selectedComponents = [s for s in selectedComponents if not ('W' in s.name and 'Jets' in s.name and not 'WJets' in s.name)]
# selectedComponents = [s for s in selectedComponents if s in WJetsHT]

###################################################
###             SET COMPONENTS BY HAND          ###
###################################################

sequence = cfg.Sequence([
    jsonAna,
    skimAna,
    genAna,
    vertexAna,
    triggerAna,
    tauJetMuAna,
    httGenAna,
    jetAna,
    muonWeighter,
    pileUpAna,
    NJetsAna,
    treeProducer
])


if not production:
    cache = True
    comp = selectedComponents[1]
    selectedComponents = [comp]
    comp.splitFactor = 1
    comp.fineSplitFactor = 1
    # comp.files = comp.files[:1]




# the following is declared in case this cfg is used in input to the
# heppy.py script
from PhysicsTools.HeppyCore.framework.eventsfwlite import Events
config = cfg.Config(components=selectedComponents,
                    sequence=sequence,
                    services=[],
                    events_class=Events,
                    )

printComps(config.components, True)

