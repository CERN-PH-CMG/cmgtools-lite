import operator 
import itertools
import copy

from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.HeppyCore.statistics.counter import Counter, Counters
from PhysicsTools.HeppyCore.utils.deltar import *
import PhysicsTools.HeppyCore.framework.config as cfg

class badChargedHadronAnalyzer( Analyzer ):

    def __init__(self, cfg_ana, cfg_comp, looperName ):
        super(badChargedHadronAnalyzer,self).__init__(cfg_ana,cfg_comp,looperName)

    def declareHandles(self):
        super(badChargedHadronAnalyzer, self).declareHandles()
        self.handles['muons'] = AutoHandle(self.cfg_ana.muons,"std::vector<pat::Muon>")
        self.handles['packedCandidates'] = AutoHandle( self.cfg_ana.packedCandidates, 'std::vector<pat::PackedCandidate>')

    def beginLoop(self, setup):
        super(badChargedHadronAnalyzer,self).beginLoop( setup )

    def process(self, event):
        self.readCollections( event.input )
        
        maxDR = 0.001
        minMuonTrackRelErr = 0.5
        minPtDiffRel = -0.5
        minMuPt = 100
        flagged = False

        for muon in self.handles['muons'].product():
            if muon.pt()<minMuPt : continue
            if muon.innerTrack().isNonnull():
                it = muon.innerTrack()
                if it.quality(it.highPurity): continue
                # All events had a drastically high pt error on the inner muon track (fac. ~10). Require at least 0.5
                if it.ptError()/it.pt() < minMuonTrackRelErr: continue
                for c in self.handles['packedCandidates'].product():
                    if abs(c.pdgId()) == 211:
                        # Require very loose similarity in pt (one-sided). 
                        dPtRel =  ( c.pt() - it.pt() )/(0.5*(c.pt() + it.pt()))
                        # Flag the event bad if dR is tiny
                        if deltaR( it.eta(), it.phi(), c.eta(), c.phi() ) < maxDR and dPtRel > minPtDiffRel:
                            flagged = True
                            break
                if flagged: break
        event.badChargedHadron=(not flagged) 
        return True

setattr(badChargedHadronAnalyzer,"defaultConfig", cfg.Analyzer(
        class_object = badChargedHadronAnalyzer,
        muons='slimmedMuons',
        packedCandidates = 'packedPFCandidates',
        )
)
