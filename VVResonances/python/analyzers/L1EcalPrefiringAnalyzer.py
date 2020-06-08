from math import *
from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle

from PhysicsTools.HeppyCore.framework.event import Event
from PhysicsTools.HeppyCore.utils.deltar import *
import os
import itertools
import ROOT

        
class L1EcalPrefiringAnalyzer( Analyzer ):
    def __init__(self, cfg_ana, cfg_comp, looperName ):
        super(L1EcalPrefiringAnalyzer,self).__init__(cfg_ana,cfg_comp,looperName)

        self.photonfile = ROOT.TFile(cfg_ana.PhotonMapFile)
        self.photonMap = self.photonfile.Get(cfg_ana.PhotonMapHisto)
        self.systematic = cfg_ana.preFiringSystematic
        
        self.jetfile = ROOT.TFile(cfg_ana.JetMapFile)
        self.jetMap = self.jetfile.Get(cfg_ana.JetMapHisto)


    def declareHandles(self):
        super(L1EcalPrefiringAnalyzer, self).declareHandles()
        self.handles['photons'] = AutoHandle(
            'slimmedPhotons', 'std::vector<pat::Photon>')



    def beginLoop(self, setup):
        super(L1EcalPrefiringAnalyzer,self).beginLoop(setup)

    def getPrefiringRate(self,h,pt,eta):
        maxpt = h.GetYaxis().GetBinLowEdge(h.GetNbinsY()+1)
        if pt>=maxpt:
            pt=maxpt-0.01
        bin = h.FindBin(eta,pt)
        prefiringRate = h.GetBinContent(bin)
        prefiringRateStatErr = h.GetBinError(bin)
        prefiringRateSystErr = prefiringRate*self.systematic
        prefiringRateUp = min(1.,prefiringRate+sqrt(prefiringRateStatErr*prefiringRateStatErr+prefiringRateSystErr*prefiringRateSystErr))
        prefiringRateDown = max(0.,prefiringRate-sqrt(prefiringRateStatErr*prefiringRateStatErr+prefiringRateSystErr*prefiringRateSystErr))
        return [prefiringRate,prefiringRateUp,prefiringRateDown]
        

    def process(self, event):
        self.readCollections( event.input )
        event.prefiringWeight=1
        event.prefiringWeightUp=1
        event.prefiringWeightDown=1

        if self.cfg_comp.isData:
            return True

        photons =  filter(lambda x: x.pt()>20 and abs(x.eta())>2 and abs(x.eta())<3.,self.handles['photons'].product())
        jets =  filter(lambda x: x.pt()>20 and abs(x.eta())>2 and abs(x.eta())<3.,event.jets)
        for g in photons:
            prefireResults = self.getPrefiringRate(self.photonMap,g.pt(),g.eta())
            event.prefiringWeight=event.prefiringWeight*(1-prefireResults[0])
            event.prefiringWeightUp=event.prefiringWeightUp*(1-prefireResults[1])
            event.prefiringWeightDown=event.prefiringWeightDown*(1-prefireResults[2])
        #now jet
        preFireJet=1
        preFireJetUp=1
        preFireJetDown=1
        preFireOverlapGamma=1
        preFireOverlapGammaUp=1
        preFireOverlapGammaDown=1
        for j in event.jets:
            for g in photons:
                if deltaR(g.eta(),g.phi(),j.eta(),j.phi())>0.4:
                    continue
                prefireResults = self.getPrefiringRate(self.photonMap,g.pt(),g.eta())

                preFireOverlapGamma=preFireOverlapGamma*(1-prefireResults[0])
                preFireOverlapGammaUp=preFireOverlapGammaUp*(1-prefireResults[1])
                preFireOverlapGammaDown=preFireOverlapGammaDown*(1-prefireResults[2])

            pt = j.pt()*(j.neutralEmEnergyFraction()+j.chargedEmEnergyFraction())    
            pjet=self.getPrefiringRate(self.jetMap,pt,j.eta())
            preFireJet   = 1-pjet[0]
            preFireJetUp = 1-pjet[1]
            preFireJetDown   = 1-pjet[2]

            
            if preFireOverlapGamma==1.0:
                event.prefiringWeight=event.prefiringWeight*preFireJet
                event.prefiringWeightUp=event.prefiringWeightUp*preFireJetUp
                event.prefiringWeightDown=event.prefiringWeightDown*preFireJetDown
            elif  preFireOverlapGamma>preFireJet:
                if preFireOverlapGamma!=0:
                    event.prefiringWeight=event.prefiringWeight*preFireJet/preFireOverlapGamma
                else:
                    event.prefiringWeight=0;

                    
        return True

