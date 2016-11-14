import PhysicsTools.HeppyCore.framework.config as cfg

# import all analysers:
# Heppy analyzers
from PhysicsTools.Heppy.analyzers.core.JSONAnalyzer import JSONAnalyzer
from PhysicsTools.Heppy.analyzers.core.SkimAnalyzerCount import SkimAnalyzerCount
from PhysicsTools.Heppy.analyzers.core.EventSelector import EventSelector
from PhysicsTools.Heppy.analyzers.objects.VertexAnalyzer import VertexAnalyzer
from PhysicsTools.Heppy.analyzers.core.PileUpAnalyzer import PileUpAnalyzer
from PhysicsTools.Heppy.analyzers.gen.GeneratorAnalyzer import GeneratorAnalyzer
from PhysicsTools.Heppy.analyzers.gen.LHEWeightAnalyzer import LHEWeightAnalyzer

# Tau-tau analyzers
from CMGTools.H2TauTau.proto.analyzers.MCWeighter import MCWeighter
from CMGTools.H2TauTau.proto.analyzers.TriggerAnalyzer import TriggerAnalyzer
from CMGTools.H2TauTau.proto.analyzers.JetAnalyzer import JetAnalyzer
from CMGTools.H2TauTau.proto.analyzers.EmbedWeighter import EmbedWeighter
from CMGTools.H2TauTau.proto.analyzers.DYJetsFakeAnalyzer import DYJetsFakeAnalyzer
from CMGTools.H2TauTau.proto.analyzers.NJetsAnalyzer import NJetsAnalyzer
from CMGTools.H2TauTau.proto.analyzers.HiggsPtWeighter import HiggsPtWeighter
from CMGTools.H2TauTau.proto.analyzers.VBFAnalyzer import VBFAnalyzer
from CMGTools.H2TauTau.proto.analyzers.RecoilCorrector import RecoilCorrector

puFileMC = '$CMSSW_BASE/src/CMGTools/H2TauTau/data/MC_Spring16_PU25_Startup.root'
puFileData = '$CMSSW_BASE/src/CMGTools/H2TauTau/data/data_pu_25-07-2016_69p2mb_60.root'

applyRecoil = False

from CMGTools.TTHAnalysis.analyzers.ttHhistoCounterAnalyzer import ttHhistoCounterAnalyzer
susyCounter = cfg.Analyzer(
    ttHhistoCounterAnalyzer, name="ttHhistoCounterAnalyzer",
    SMS_max_mass=3000,  # maximum mass allowed in the scan
    # SMS_mass_1='genSusyMScan1',  # first scanned mass
    # SMS_mass_2='genSusyMScan2',  # second scanned mass
    SMS_mass_1='genSusyMStau',  # first scanned mass
    SMS_mass_2='genSusyMNeutralino',  # second scanned mass
    SMS_varying_masses=[],  # other mass variables that are expected to change in the tree (e.g., in T1tttt it should be set to ['genSusyMGluino','genSusyMNeutralino'])
    SMS_regexp_evtGenMass='genSusyM.+',
    bypass_trackMass_check=True  # bypass check that non-scanned masses are the same in all events
)

eventSelector = cfg.Analyzer(
    EventSelector,
    name='EventSelector',
    toSelect=[]
)

lheWeightAna = cfg.Analyzer(
    LHEWeightAnalyzer, name="LHEWeightAnalyzer",
)

jsonAna = cfg.Analyzer(
    JSONAnalyzer,
    name='JSONAnalyzer',
)

skimAna = cfg.Analyzer(
    SkimAnalyzerCount,
    name='SkimAnalyzerCount'
)

mcWeighter = cfg.Analyzer(
    MCWeighter,
    name='MCWeighter'
)

triggerAna = cfg.Analyzer(
    TriggerAnalyzer,
    name='TriggerAnalyzer',
    addTriggerObjects=True,
    requireTrigger=True,
    usePrescaled=False
)

vertexAna = cfg.Analyzer(
    VertexAnalyzer,
    name='VertexAnalyzer',
    fixedWeight=1,
    verbose=False
)

pileUpAna = cfg.Analyzer(
    PileUpAnalyzer,
    name='PileUpAnalyzer',
    true=True
)

genAna = GeneratorAnalyzer.defaultConfig

genAna.savePreFSRParticleIds = [1, 2, 3, 4, 5, 21]

# Save SUSY masses
from CMGTools.TTHAnalysis.analyzers.susyParameterScanAnalyzer import susyParameterScanAnalyzer
susyScanAna = cfg.Analyzer(
    susyParameterScanAnalyzer, name="susyParameterScanAnalyzer",
    doLHE=True,
)

dyJetsFakeAna = cfg.Analyzer(
    DYJetsFakeAnalyzer,
    name='DYJetsFakeAnalyzer',
    jetCol='slimmedJets',
    channel='',
    genPtCut=8.
)

jetAna = cfg.Analyzer(
    JetAnalyzer,
    name='JetAnalyzer',
    jetCol='slimmedJets',
    jetPt=20.,
    jetEta=4.7,
    relaxJetId=False,
    relaxPuJetId=True,
    jerCorr=False,
    #jesCorr = 1.,
    puJetIDDisc='pileupJetId:fullDiscriminant',
)

vbfAna = cfg.Analyzer(
    VBFAnalyzer,
    name='VBFAnalyzer',
    cjvPtCut=20.,
    Mjj=500.,
    deltaEta=3.5
)

recoilCorr = cfg.Analyzer(
    RecoilCorrector,
    name='RecoilCorrector'
)

embedWeighter = cfg.Analyzer(
    EmbedWeighter,
    name='EmbedWeighter',
    isRecHit=False,
    verbose=False
)

NJetsAna = cfg.Analyzer(
    NJetsAnalyzer,
    name='NJetsAnalyzer',
    fillTree=True,
    verbose=False
)

higgsWeighter = cfg.Analyzer(
    HiggsPtWeighter,
    name='HiggsPtWeighter',
)


###################################################
###                  SEQUENCE                   ###
###################################################
commonSequence = cfg.Sequence([
    lheWeightAna,
    jsonAna,
    skimAna,
    mcWeighter,
    genAna,
    susyScanAna,
    triggerAna, # First analyser that applies selections
    vertexAna,
    dyJetsFakeAna,
    jetAna,
    vbfAna,
    pileUpAna,
    embedWeighter,
    NJetsAna,
    higgsWeighter
])

if applyRecoil:
    commonSequence.insert(commonSequence.index(pileUpAna), recoilCorr)
