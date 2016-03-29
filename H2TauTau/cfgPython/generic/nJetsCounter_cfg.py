import PhysicsTools.HeppyCore.framework.config as cfg
from PhysicsTools.HeppyCore.framework.config import printComps

from CMGTools.H2TauTau.proto.analyzers.NJetsAnalyzer import NJetsAnalyzer

# from CMGTools.H2TauTau.proto.samples.phys14.connector import httConnector
from CMGTools.H2TauTau.proto.samples.fall15.htt_common import DYJetsToLL_M50_LO


njetAna = cfg.Analyzer(
    NJetsAnalyzer,
    name='NJetsAnalyzer',
    fillTree=True,
    verbose=False
)

###################################################
selectedComponents = [DYJetsToLL_M50_LO]
sequence = cfg.Sequence([
    njetAna
])

for comp in selectedComponents:
    comp.splitFactor = 4
    comp.fineSplitFactor = 1
    # comp.files = comp.files[:1]


# the following is declared in case this cfg is used in input to the
# heppy.py script
from PhysicsTools.HeppyCore.framework.eventsfwlite import Events
config = cfg.Config(components=selectedComponents,
                    sequence=sequence,
                    services=[],
                    events_class=Events
                    )

printComps(config.components, True)
