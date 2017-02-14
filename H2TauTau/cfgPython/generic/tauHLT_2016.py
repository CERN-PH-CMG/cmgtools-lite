import PhysicsTools.HeppyCore.framework.config as cfg
from PhysicsTools.HeppyCore.framework.config import printComps
from PhysicsTools.HeppyCore.framework.heppy_loop import getHeppyOption
from PhysicsTools.HeppyCore.framework.eventsfwlite import Events

from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator

from CMGTools.H2TauTau.proto.analyzers.TauHLTAnalyzer import TauHLTAnalyzer
from CMGTools.H2TauTau.proto.analyzers.HLTTauTreeProducer import HLTTauTreeProducer

production = getHeppyOption('production', True)

c = ComponentCreator()
# ggH135_0 = c.makeMCComponentFromEOS('ggH135_rawaod', 'ggH135_rawaod', '/store/group/phys_higgs/cmshtt/steggema/HPSatHLTv5/GluGluHToTauTau_M125_13TeV_powheg_pythia8/TauHPSatHLTFine/161117_103941/0000/')
# ggH135_1 = c.makeMCComponentFromEOS('ggH135_rawaod', 'ggH135_rawaod', '/store/group/phys_higgs/cmshtt/steggema/HPSatHLTv5/GluGluHToTauTau_M125_13TeV_powheg_pythia8/TauHPSatHLTFine/161117_103941/0001/')


ggH135_0 = c.makeMCComponentFromEOS('ggH135_rawaod', 'ggH135_rawaod', '/store/group/phys_tau/HLT2016/HPSatHLT/GluGluHToTauTau_M125_13TeV_powheg_pythia8/HPSatHLT/161206_134434/0000/')
ggH135_1 = c.makeMCComponentFromEOS('ggH135_rawaod_2', 'ggH135_rawaod', '/store/group/phys_tau/HLT2016/HPSatHLT/GluGluHToTauTau_M125_13TeV_powheg_pythia8/HPSatHLT/161206_134434/0001/')


selectedComponents = [ggH135_0, ggH135_1]


tauHLTAna = cfg.Analyzer(
    TauHLTAnalyzer,
    name='TauHLTAnalyzer',
    )

tauHLTTree = cfg.Analyzer(
    HLTTauTreeProducer,
    name='HLTTauTreeProducer'
)

sequence = cfg.Sequence([
    tauHLTAna,
    tauHLTTree
])


if not production:
    selectedComponents = selectedComponents[:1]
    for comp in selectedComponents:
        comp.splitFactor = 1
        comp.fineSplitFactor = 1
    # comp.files = comp.files[:1]
else:
    for comp in selectedComponents:
        comp.splitFactor = 200

config = cfg.Config(components=selectedComponents,
                    sequence=sequence,
                    services=[],
                    events_class=Events
                    )

printComps(config.components, True)
