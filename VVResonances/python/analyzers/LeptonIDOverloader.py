import ROOT
import random
import math
from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
import PhysicsTools.HeppyCore.framework.config as cfg

class LeptonIDOverloader( Analyzer ):
    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(LeptonIDOverloader,self).__init__(cfg_ana, cfg_comp, looperName)

    def beginLoop(self, setup):
        super(LeptonIDOverloader,self).beginLoop(setup)


    def heepID(self,lepton):    
#        for leptonid in lepton.electronIDs():
#            print leptonid.first,leptonid.second
        return lepton.electronID("heepElectronID-HEEPV60")>0.0


    def heepIDNoIso(self,e):
        decisionBarrel = abs(e.superCluster().eta())<1.4442 and \
            e.ecalDriven() and abs(e.deltaEtaSeedClusterTrackAtVtx())<0.004 and \
            abs( e.deltaPhiSuperClusterTrackAtVtx())< 0.06 and (e.hadronicOverEm()<1.0/e.superCluster().energy()+0.05) and \
            (e.e2x5Max()/e.e5x5()>0.94 or e.e1x5()/e.e5x5()>0.83) and abs(e.dxy())<0.02


        decisionEndcap = abs(e.superCluster().eta())>1.566 and \
            e.ecalDriven() and abs(e.deltaEtaSeedClusterTrackAtVtx())<0.006 and \
            abs( e.deltaPhiSuperClusterTrackAtVtx())< 0.06 and (e.hadronicOverEm()<5.0/e.superCluster().energy()+0.05) and \
            abs(e.dxy())<0.05 and e.full5x5_sigmaIetaIeta()<0.03
        return decisionBarrel or decisionEndcap


    def muonIDTrackerHighPt(self,mu):    
        decision =  mu.isTrackerMuon() and mu.numberOfMatchedStations() > 1 and\
            mu.muonBestTrack().ptError()/mu.muonBestTrack().pt()<0.3 and mu.dB()< 0.2 and mu.innerTrack().hitPattern().numberOfValidPixelHits() > 0 and\
            mu.innerTrack().hitPattern().trackerLayersWithMeasurement()>5
        return decision


    def muonIDHighPt(self,mu):    
        return mu.isHighPtMuon(mu.associatedVertex)

    def muonIDHighPtIso(self,mu):    
        return mu.isHighPtMuon(mu.associatedVertex) and mu.isolationR03().sumPt/mu.pt()<0.05 # per discussion with Zuchetta go down to 0.05

    def muonIDTrackerHighPtIso(self,mu):    
        return self.muonIDTrackerHighPt(mu) and mu.isolationR03().sumPt/mu.pt()<0.05

        
    def process(self, event):
        self.readCollections( event.input )
#        for l in event.genleps:
#            if l.pt()>30:
#                print l.pdgId(),l.pt(),l.eta()

        for lepton in event.selectedLeptons:
            if abs(lepton.pdgId())==11:
                lepton.heepID = self.heepID(lepton)
                lepton.heepIDNoIso = self.heepIDNoIso(lepton)
            else:
                lepton.highPtID = self.muonIDHighPt(lepton)
                lepton.highPtTrackID = self.muonIDTrackerHighPt(lepton)
                lepton.highPtIDIso = self.muonIDHighPtIso(lepton)
                lepton.highPtTrackIDIso = self.muonIDTrackerHighPtIso(lepton)




        
            

        


                
                
