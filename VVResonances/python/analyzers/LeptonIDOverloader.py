import ROOT
import random
import math
from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
import PhysicsTools.HeppyCore.framework.config as cfg

class LeptonIDOverloader( Analyzer ):
    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(LeptonIDOverloader,self).__init__(cfg_ana, cfg_comp, looperName)
        self.heepIDCalculator = ROOT.cmg.HEEPEleIDRecalculator()
    def beginLoop(self, setup):
        super(LeptonIDOverloader,self).beginLoop(setup)

    def heepID(self,lepton,electrons,tracks,packed):
        passId = self.heepIDNoIso(lepton)
        if not passId:
            return passId
        passIso = False
#        if (self.handles['electrons'].isValid() and self.handles['lostTracks'].isValid() and self.handles['packed'].isValid()): ##Michalis -> For some reason this does not work in 94X
        passIso = self.heepIDCalculator.iso(lepton.physObj, lepton.rho, electrons, tracks,packed)
        return (passId and passIso)

    def declareHandles(self):
        super(LeptonIDOverloader, self).declareHandles()
        self.handles['packed'] = AutoHandle( 'packedPFCandidates', 'std::vector<pat::PackedCandidate>' )
        self.handles['lostTracks'] = AutoHandle( 'lostTracks', 'std::vector<pat::PackedCandidate>' )
        self.handles['electrons'] = AutoHandle( 'slimmedElectrons', 'std::vector<pat::Electron>' )


    def heepIDNoIso(self,e):
        return self.heepIDCalculator.id(e.physObj)


    def muonIDTrackerHighPt(self,mu):
        decision =  mu.isTrackerMuon() and mu.numberOfMatchedStations() > 1 and\
            mu.muonBestTrack().ptError()/mu.muonBestTrack().pt()<0.3 and mu.dB()< 0.2 and mu.innerTrack().hitPattern().numberOfValidPixelHits() > 0 and\
            mu.innerTrack().hitPattern().trackerLayersWithMeasurement()>5
        return decision


    def muonIDHighPt(self,mu):
        return mu.isHighPtMuon(mu.associatedVertex)

    def muonIDHighPtIso(self,mu):
        return mu.isHighPtMuon(mu.associatedVertex) and mu.relIso04 < 0.05

    def muonIDTrackerHighPtIso(self,mu):
        return self.muonIDTrackerHighPt(mu) and mu.relIso04 < 0.05


    def process(self, event):
        self.readCollections( event.input )
        electrons = self.handles['electrons'].product()
        lostTracks = self.handles['lostTracks'].product()
        packed = self.handles['packed'].product()
        for lepton in event.selectedLeptons:
            if abs(lepton.pdgId())==11:
                lepton.heepID = self.heepID(lepton,electrons,lostTracks,packed)
                lepton.heepIDNoIso = self.heepIDNoIso(lepton)
            else:
                lepton.highPtID = self.muonIDHighPt(lepton)
                lepton.highPtTrackID = self.muonIDTrackerHighPt(lepton)
                lepton.highPtIDIso = self.muonIDHighPtIso(lepton)
                lepton.highPtTrackIDIso = self.muonIDTrackerHighPtIso(lepton)
