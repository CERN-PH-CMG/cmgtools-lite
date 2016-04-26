import os

import PhysicsTools.HeppyCore.framework.config as cfg

# Tau-tau analyzers
from CMGTools.H2TauTau.proto.analyzers.TauMuAnalyzer import TauMuAnalyzer
from CMGTools.H2TauTau.proto.analyzers.H2TauTauTreeProducerTauMu import H2TauTauTreeProducerTauMu
from CMGTools.H2TauTau.proto.analyzers.TauDecayModeWeighter import TauDecayModeWeighter
from CMGTools.H2TauTau.proto.analyzers.TauFakeRateWeighter import TauFakeRateWeighter
from CMGTools.H2TauTau.proto.analyzers.LeptonWeighter import LeptonWeighter
from CMGTools.H2TauTau.proto.analyzers.SVfitProducer import SVfitProducer

# from CMGTools.H2TauTau.proto.samples.spring15.connector import httConnector

# common configuration and sequence
from CMGTools.H2TauTau.htt_ntuple_base_cff import commonSequence, genAna, dyJetsFakeAna

# mu-tau specific configuration settings
syncntuple = True
computeSVfit = True

dyJetsFakeAna.channel = 'mt'

# Define mu-tau specific modules

tauMuAna = cfg.Analyzer(
    TauMuAnalyzer,
    name='TauMuAnalyzer',
    pt1=19,
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
    scaleFactorFiles={},
    lepton='leg2',
    disable=True,
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

treeProducer = cfg.Analyzer(
    H2TauTauTreeProducerTauMu,
    name='H2TauTauTreeProducerTauMu'
)

syncTreeProducer = cfg.Analyzer(
    H2TauTauTreeProducerTauMu,
    name='H2TauTauSyncTreeProducerTauMu',
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
    integrateOverVisPtResponse = True          ,
    visPtResponseFile = os.environ['CMSSW_BASE']+'/src/CMGTools/SVfitStandalone/data/svFitVisMassAndPtResolutionPDF.root', 
    l1type='muon',
    l2type='tau'
)

###################################################
###                  SEQUENCE                   ###
###################################################
sequence = commonSequence
sequence.insert(sequence.index(genAna), tauMuAna)
sequence.append(tauDecayModeWeighter)
sequence.append(tauFakeRateWeighter)
sequence.append(tauWeighter)
sequence.append(muonWeighter)
sequence.append(treeProducer)
if syncntuple:
    sequence.append(syncTreeProducer)

