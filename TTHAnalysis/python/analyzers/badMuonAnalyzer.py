import operator 
import itertools
import copy

from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.HeppyCore.statistics.counter import Counter, Counters
from PhysicsTools.HeppyCore.utils.deltar import *
import PhysicsTools.HeppyCore.framework.config as cfg

class badMuonAnalyzer( Analyzer ):

    def __init__(self, cfg_ana, cfg_comp, looperName ):
        super(badMuonAnalyzer,self).__init__(cfg_ana,cfg_comp,looperName)

    def declareHandles(self):
        super(badMuonAnalyzer, self).declareHandles()
        self.handles['muons'] = AutoHandle(self.cfg_ana.muons,"std::vector<pat::Muon>")
        self.handles['packedCandidates'] = AutoHandle( self.cfg_ana.packedCandidates, 'std::vector<pat::PackedCandidate>')

    def beginLoop(self, setup):
        super(badMuonAnalyzer,self).beginLoop( setup )

    def process(self, event):
        self.readCollections( event.input )
        
        maxDR = 0.001
        minMuonTrackRelErr = 0.5
        suspiciousAlgo=14
        minMuPt = 100
        flagged = False

        event.crazyMuon = []

        for muon in self.handles['muons'].product():

            ##### check the muon inner and globaTrack
            foundBadTrack = False
            if muon.innerTrack().isNonnull():
                it = muon.innerTrack()
                if it.pt()<minMuPt : continue
                if it.quality(it.highPurity): continue
                if it.ptError()/it.pt() < minMuonTrackRelErr: continue
                if it.originalAlgo()==suspiciousAlgo and it.algo()==suspiciousAlgo:
                    foundBadTrack = True

            if foundBadTrack:
                #   print 'there is suspicious muon  '
                for c in self.handles['packedCandidates'].product():
                    if c.pt()<minMuPt : continue
                    if abs(c.pdgId()) == 13:
                        if deltaR( muon.eta(), muon.phi(), c.eta(), c.phi() ) < maxDR:
                            flagged = True
                            event.crazyMuon.append(muon)
                            break
            if flagged: break

        event.badMuon = (not flagged)
#        self.printInfo(event)
        return True

    def printInfo(self, event):
 
        if len(event.crazyMuon)>0:
#            print 'found muon: run=', event.run,' lumi=', event.lumi,' event',event.eventId
            print 'met=',event.met.pt(),' metphi=',event.met.phi()
            print 'number of muons: ',len(event.crazyMuon)
            print ' muon candidate pt: ',event.crazyMuon[0].pt(),' phi=',event.crazyMuon[0].phi()
            print ' muon candidate eta: ',event.crazyMuon[0].eta()
            print ' pdgId candidate : ',event.crazyMuon[0].pdgId()
            print ' trackHighPurity: ',event.crazyMuon[0].trackHighPurity()
            print ' dz: ',event.crazyMuon[0].dz()
            print ' fromPV: ',event.crazyMuon[0].fromPV()
            print ' ptError: ',event.crazyMuon[0].pseudoTrack().ptError(),';relativeError',event.crazyMuon[0].pseudoTrack().ptError()/event.crazyMuon[0].pseudoTrack().pt()
            print ' chi2: ',event.crazyMuon[0].pseudoTrack().normalizedChi2()
            print ' algo: ',event.crazyMuon[0].algo(),' originalAlgo',event.crazyMuon[0].originalAlgo()
            print '----------------'
            print '----------------'

setattr(badMuonAnalyzer,"defaultConfig", cfg.Analyzer(
        class_object = badMuonAnalyzer,
        packedCandidates = 'packedPFCandidates',
        )
)
