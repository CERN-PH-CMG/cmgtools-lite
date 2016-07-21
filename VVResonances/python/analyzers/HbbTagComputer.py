import ROOT
import random
import math
from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
import PhysicsTools.HeppyCore.framework.config as cfg
import FWCore.ParameterSet.Config as cms

class HbbTagComputer( Analyzer ):
    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(HbbTagComputer,self).__init__(cfg_ana, cfg_comp, looperName)
        # instantiate CandidateBoostedDoubleSecondaryVertexComputerLight
        # values taken from https://github.com/cms-sw/cmssw/blob/CMSSW_8_0_X/RecoBTag/SecondaryVertex/python/candidateBoostedDoubleSecondaryVertexAK8Computer_cfi.py
        from RecoBTag.SecondaryVertex.trackSelection_cff import trackSelectionBlock
        candidateBDSVAK8ComputerPSet = cms.PSet(
        trackSelectionBlock,
        beta = cms.double(1.0),
        R0 = cms.double(0.8),
        maxSVDeltaRToJet = cms.double(0.7),
        useCondDB = cms.bool(False),
        weightFile = cms.FileInPath('CMGTools/VVResonances/data/BoostedDoubleSV_AK8_BDT_v3.weights.xml.gz'),
        useGBRForest = cms.bool(True),
        useAdaBoost = cms.bool(False),
        trackPairV0Filter = cms.PSet(k0sMassWindow = cms.double(0.03))
        )
        # deltaRMax = 0.8
        hbbComputer = ROOT.cmg.CandidateBoostedDoubleSecondaryVertexComputerLight(
            candidateBDSVAK8ComputerPSet.beta, candidateBDSVAK8ComputerPSet.R0, candidateBDSVAK8ComputerPSet.maxSVDeltaRToJet, candidateBDSVAK8ComputerPSet.gbrForestLabel,
            candidateBDSVAK8ComputerPSet.weightFile, candidateBDSVAK8ComputerPSet.useGBRForest, candidateBDSVAK8ComputerPSet.useAdaBoost, candidateBDSVAK8ComputerPSet.trackPairV0Filter.k0sMassWindow,
            candidateBDSVAK8ComputerPSet.trackSelectionBlock.totalHitsMin, candidateBDSVAK8ComputerPSet.trackSelectionBlock.jetDeltaRMax, candidateBDSVAK8ComputerPSet.trackSelectionBlock.qualityClass, candidateBDSVAK8ComputerPSet.trackSelectionBlock.pixelHitsMin,
            candidateBDSVAK8ComputerPSet.trackSelectionBlock.maxDistToAxis, candidateBDSVAK8ComputerPSet.trackSelectionBlock.maxDecayLen, candidateBDSVAK8ComputerPSet.trackSelectionBlock.sip3dSigMin, candidateBDSVAK8ComputerPSet.trackSelectionBlock.sip3dSigMax,
            candidateBDSVAK8ComputerPSet.trackSelectionBlock.sip2dValMax, candidateBDSVAK8ComputerPSet.trackSelectionBlock.ptMin, candidateBDSVAK8ComputerPSet.trackSelectionBlock.sip2dSigMax, candidateBDSVAK8ComputerPSet.trackSelectionBlock.sip2dSigMin,
            candidateBDSVAK8ComputerPSet.trackSelectionBlock.sip3dValMax, candidateBDSVAK8ComputerPSet.trackSelectionBlock.sip3dValMin, candidateBDSVAK8ComputerPSet.trackSelectionBlock.sip2dValMin, candidateBDSVAK8ComputerPSet.trackSelectionBlock.normChi2Max
        )

    def beginLoop(self, setup):
        super(HbbTagComputer,self).beginLoop(setup)


    def Hbbtag(self,jet):
#        for leptonid in lepton.electronIDs():
#            print leptonid.first,leptonid.second
        return jet

    def process(self, event):
        self.readCollections( event.input )

        # for lepton in event.selectedLeptons:
        #     if abs(lepton.pdgId())==11:
        #         lepton.heepID = self.heepID(lepton)
        #         lepton.heepIDNoIso = self.heepIDNoIso(lepton)
        #     else:
        #         lepton.highPtID = self.muonIDHighPt(lepton)
        #         lepton.highPtTrackID = self.muonIDTrackerHighPt(lepton)
        #         lepton.highPtIDIso = self.muonIDHighPtIso(lepton)
        #         lepton.highPtTrackIDIso = self.muonIDTrackerHighPtIso(lepton)
