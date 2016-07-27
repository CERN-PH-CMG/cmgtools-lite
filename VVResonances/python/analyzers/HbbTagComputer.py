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
        gbrForestLabel = cms.string(""),
        weightFile = cms.FileInPath('CMGTools/VVResonances/data/BoostedDoubleSV_AK8_BDT_v3.weights.xml.gz'),
        useGBRForest = cms.bool(True),
        useAdaBoost = cms.bool(False),
        trackPairV0Filter = cms.PSet(k0sMassWindow = cms.double(0.03))
        )
        # deltaRMax = 0.8
        candidateBDSVAK8ComputerPSet.trackSelection.jetDeltaRMax = cms.double(0.8)
        hbbComputer = ROOT.cmg.CandidateBoostedDoubleSecondaryVertexComputerLight(
            candidateBDSVAK8ComputerPSet.beta.value(), candidateBDSVAK8ComputerPSet.R0.value(), candidateBDSVAK8ComputerPSet.maxSVDeltaRToJet.value(), candidateBDSVAK8ComputerPSet.gbrForestLabel.value(),
            candidateBDSVAK8ComputerPSet.weightFile.value(), candidateBDSVAK8ComputerPSet.useGBRForest.value(), candidateBDSVAK8ComputerPSet.useAdaBoost.value(), candidateBDSVAK8ComputerPSet.trackPairV0Filter.k0sMassWindow.value(),
            candidateBDSVAK8ComputerPSet.trackSelection.totalHitsMin.value(), candidateBDSVAK8ComputerPSet.trackSelection.jetDeltaRMax.value(), candidateBDSVAK8ComputerPSet.trackSelection.qualityClass.value(), candidateBDSVAK8ComputerPSet.trackSelection.pixelHitsMin.value(),
            candidateBDSVAK8ComputerPSet.trackSelection.maxDistToAxis.value(), candidateBDSVAK8ComputerPSet.trackSelection.maxDecayLen.value(), candidateBDSVAK8ComputerPSet.trackSelection.sip3dSigMin.value(), candidateBDSVAK8ComputerPSet.trackSelection.sip3dSigMax.value(),
            candidateBDSVAK8ComputerPSet.trackSelection.sip2dValMax.value(), candidateBDSVAK8ComputerPSet.trackSelection.ptMin.value(), candidateBDSVAK8ComputerPSet.trackSelection.sip2dSigMax.value(), candidateBDSVAK8ComputerPSet.trackSelection.sip2dSigMin.value(),
            candidateBDSVAK8ComputerPSet.trackSelection.sip3dValMax.value(), candidateBDSVAK8ComputerPSet.trackSelection.sip3dValMin.value(), candidateBDSVAK8ComputerPSet.trackSelection.sip2dValMin.value(), candidateBDSVAK8ComputerPSet.trackSelection.normChi2Max.value()
        )
        hbbComputer.initialize()

    def beginLoop(self, setup):
        super(HbbTagComputer,self).beginLoop(setup)


    def Hbbtag(self,jet):
        return hbbComputer.discriminator(jet.sourcePtr())

    def process(self, event):
        self.readCollections( event.input )
        for jet in event.selectedJets:
            jet.Hbbtag = self.Hbbtag(jet)
