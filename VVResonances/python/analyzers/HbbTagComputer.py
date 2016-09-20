import ROOT
from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
import PhysicsTools.HeppyCore.framework.config as cfg
import FWCore.ParameterSet.Config as cms
import os
# ROOT.gSystem.Load("libCMGToolsVVResonances")

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
        
        weightFile = cms.FileInPath(self.cfg_ana.path), 
#        weightFile = cms.FileInPath('CMGTools/VVResonances/data/BoostedDoubleSV_AK8_BDT_v3.weights.xml.gz'),
        # weightFile = cms.FileInPath('CMGTools/VVResonances/data/BoostedDoubleSV_AK8_BDT_v2.weights.xml.gz'),
        useGBRForest = cms.bool(True),
        useAdaBoost = cms.bool(False),
        trackPairV0Filter = cms.PSet(k0sMassWindow = cms.double(0.03))
        )
        # deltaRMax = 0.8
        candidateBDSVAK8ComputerPSet.trackSelection.jetDeltaRMax = cms.double(0.8)
        self.hbbComputer = ROOT.cmg.CandidateBoostedDoubleSecondaryVertexComputerLight(
            candidateBDSVAK8ComputerPSet.beta.value(), candidateBDSVAK8ComputerPSet.R0.value(), candidateBDSVAK8ComputerPSet.maxSVDeltaRToJet.value(), candidateBDSVAK8ComputerPSet.gbrForestLabel.value(),
            candidateBDSVAK8ComputerPSet.weightFile.value(), candidateBDSVAK8ComputerPSet.useGBRForest.value(), candidateBDSVAK8ComputerPSet.useAdaBoost.value(), candidateBDSVAK8ComputerPSet.trackPairV0Filter.k0sMassWindow.value(),
            candidateBDSVAK8ComputerPSet.trackSelection.totalHitsMin.value(), candidateBDSVAK8ComputerPSet.trackSelection.jetDeltaRMax.value(), candidateBDSVAK8ComputerPSet.trackSelection.qualityClass.value(), candidateBDSVAK8ComputerPSet.trackSelection.pixelHitsMin.value(),
            candidateBDSVAK8ComputerPSet.trackSelection.maxDistToAxis.value(), candidateBDSVAK8ComputerPSet.trackSelection.maxDecayLen.value(), candidateBDSVAK8ComputerPSet.trackSelection.sip3dSigMin.value(), candidateBDSVAK8ComputerPSet.trackSelection.sip3dSigMax.value(),
            candidateBDSVAK8ComputerPSet.trackSelection.sip2dValMax.value(), candidateBDSVAK8ComputerPSet.trackSelection.ptMin.value(), candidateBDSVAK8ComputerPSet.trackSelection.sip2dSigMax.value(), candidateBDSVAK8ComputerPSet.trackSelection.sip2dSigMin.value(),
            candidateBDSVAK8ComputerPSet.trackSelection.sip3dValMax.value(), candidateBDSVAK8ComputerPSet.trackSelection.sip3dValMin.value(), candidateBDSVAK8ComputerPSet.trackSelection.sip2dValMin.value(), candidateBDSVAK8ComputerPSet.trackSelection.normChi2Max.value()
        )
        self.hbbComputer.initialize()

        # instantiate IPProducerLight
        # https://github.com/cms-sw/cmssw/blob/CMSSW_8_0_X/RecoBTag/ImpactParameter/python/pfImpactParameterAK8TagInfos_cfi.py
        from RecoBTag.ImpactParameter.pfImpactParameterAK8TagInfos_cfi import pfImpactParameterAK8TagInfos
        pfImpactParameterAK8TagInfos.maxDeltaR = cms.double(0.8)
        pfImpactParameterAK8TagInfos.computeProbabilities = cms.bool(False)
        pfImpactParameterAK8TagInfos.computeGhostTrack = cms.bool(False)
        # CandIPProducer (https://github.com/cms-sw/cmssw/blob/CMSSW_8_0_X/RecoBTag/ImpactParameter/plugins/modules.cc#L21) uses FromJetAndCands
        # Therefore explicitJTA = False (https://github.com/cms-sw/cmssw/blob/CMSSW_8_0_X/RecoBTag/ImpactParameter/plugins/IPProducer.h#L503)
        explicitJTA = False

        self.ipProducerLight = ROOT.cmg.IPProducerLight(pfImpactParameterAK8TagInfos.computeProbabilities.value(), pfImpactParameterAK8TagInfos.computeGhostTrack.value(), pfImpactParameterAK8TagInfos.ghostTrackPriorDeltaR.value(),
        pfImpactParameterAK8TagInfos.minimumNumberOfPixelHits.value(), pfImpactParameterAK8TagInfos.minimumNumberOfHits.value(), pfImpactParameterAK8TagInfos.maximumTransverseImpactParameter.value(),
        pfImpactParameterAK8TagInfos.minimumTransverseMomentum.value(), pfImpactParameterAK8TagInfos.maximumChiSquared.value(), pfImpactParameterAK8TagInfos.maximumLongitudinalImpactParameter.value(),
        pfImpactParameterAK8TagInfos.jetDirectionUsingTracks.value(), pfImpactParameterAK8TagInfos.jetDirectionUsingGhostTrack.value(),
        pfImpactParameterAK8TagInfos.useTrackQuality.value(), pfImpactParameterAK8TagInfos.maxDeltaR.value(), explicitJTA)

        # instantiate SecondaryVertexProducerLight
        # https://github.com/cms-sw/cmssw/blob/CMSSW_8_0_X/RecoBTag/SecondaryVertex/python/pfInclusiveSecondaryVertexFinderAK8TagInfos_cfi.py
        from RecoBTag.SecondaryVertex.pfInclusiveSecondaryVertexFinderAK8TagInfos_cfi import pfInclusiveSecondaryVertexFinderAK8TagInfos
        # print pfInclusiveSecondaryVertexFinderAK8TagInfos.vertexCuts.trackPairV0Filter
        pfInclusiveSecondaryVertexFinderAK8TagInfos.trackSelection.jetDeltaRMax = cms.double(0.8) # plays no role since using IVF vertices
        pfInclusiveSecondaryVertexFinderAK8TagInfos.vertexCuts.maxDeltaRToJetAxis = cms.double(0.8)
        pfInclusiveSecondaryVertexFinderAK8TagInfos.k0sMassWindow = cms.double(0.05) # checked to be correct, see https://github.com/cms-sw/cmssw/blob/CMSSW_8_0_X/RecoBTag/SecondaryVertex/python/combinedSecondaryVertexCommon_cff.py
        self.secondaryVertexProducerLight = ROOT.cmg.SecondaryVertexProducerLight(pfInclusiveSecondaryVertexFinderAK8TagInfos.trackSelection.totalHitsMin.value() , pfInclusiveSecondaryVertexFinderAK8TagInfos.trackSelection.jetDeltaRMax.value(),
        pfInclusiveSecondaryVertexFinderAK8TagInfos.trackSelection.qualityClass.value(),
        pfInclusiveSecondaryVertexFinderAK8TagInfos.trackSelection.pixelHitsMin.value(), pfInclusiveSecondaryVertexFinderAK8TagInfos.trackSelection.maxDistToAxis.value(), pfInclusiveSecondaryVertexFinderAK8TagInfos.trackSelection.maxDecayLen.value(),
        pfInclusiveSecondaryVertexFinderAK8TagInfos.trackSelection.sip3dSigMin.value(), pfInclusiveSecondaryVertexFinderAK8TagInfos.trackSelection.sip3dSigMax.value(), pfInclusiveSecondaryVertexFinderAK8TagInfos.trackSelection.sip2dValMax.value(),
        pfInclusiveSecondaryVertexFinderAK8TagInfos.trackSelection.ptMin.value(), pfInclusiveSecondaryVertexFinderAK8TagInfos.trackSelection.sip2dSigMax.value(),
        pfInclusiveSecondaryVertexFinderAK8TagInfos.trackSelection.sip2dSigMin.value(), pfInclusiveSecondaryVertexFinderAK8TagInfos.trackSelection.sip3dValMax.value(),
        pfInclusiveSecondaryVertexFinderAK8TagInfos.trackSelection.sip3dValMin.value(), pfInclusiveSecondaryVertexFinderAK8TagInfos.trackSelection.sip2dValMin.value(),
        pfInclusiveSecondaryVertexFinderAK8TagInfos.trackSelection.normChi2Max.value(), pfInclusiveSecondaryVertexFinderAK8TagInfos.usePVError.value(),
        pfInclusiveSecondaryVertexFinderAK8TagInfos.minimumTrackWeight.value(), pfInclusiveSecondaryVertexFinderAK8TagInfos.trackSort.value(),
        pfInclusiveSecondaryVertexFinderAK8TagInfos.extSVDeltaRToJet.value(), pfInclusiveSecondaryVertexFinderAK8TagInfos.vertexSelection.sortCriterium.value(),
        pfInclusiveSecondaryVertexFinderAK8TagInfos.vertexCuts.distVal2dMin.value(), pfInclusiveSecondaryVertexFinderAK8TagInfos.vertexCuts.distVal2dMax.value(),
        pfInclusiveSecondaryVertexFinderAK8TagInfos.vertexCuts.distSig2dMin.value(), pfInclusiveSecondaryVertexFinderAK8TagInfos.vertexCuts.distSig2dMax.value(),
        pfInclusiveSecondaryVertexFinderAK8TagInfos.vertexCuts.distSig3dMin.value(), pfInclusiveSecondaryVertexFinderAK8TagInfos.vertexCuts.distSig3dMax.value(),
        pfInclusiveSecondaryVertexFinderAK8TagInfos.vertexCuts.distVal3dMin.value(), pfInclusiveSecondaryVertexFinderAK8TagInfos.vertexCuts.distVal3dMax.value(),
        pfInclusiveSecondaryVertexFinderAK8TagInfos.vertexCuts.fracPV.value(), pfInclusiveSecondaryVertexFinderAK8TagInfos.vertexCuts.useTrackWeights.value(), pfInclusiveSecondaryVertexFinderAK8TagInfos.vertexCuts.maxDeltaRToJetAxis.value(),
        pfInclusiveSecondaryVertexFinderAK8TagInfos.vertexCuts.multiplicityMin.value(), pfInclusiveSecondaryVertexFinderAK8TagInfos.vertexCuts.massMax.value(), pfInclusiveSecondaryVertexFinderAK8TagInfos.k0sMassWindow.value())



    def declareHandles(self):
        super(HbbTagComputer, self).declareHandles()
        self.handles['primaryVertices'] = AutoHandle('offlineSlimmedPrimaryVertices',"vector<reco::Vertex>")
        self.handles['secondaryVertices'] = AutoHandle('slimmedSecondaryVertices',"vector<reco::VertexCompositePtrCandidate>")
        self.handles['packedCandidates'] = AutoHandle( 'packedPFCandidates', 'std::vector<pat::PackedCandidate>')
        self.handles['beamSpot'] = AutoHandle( 'offlineBeamSpot', 'reco::BeamSpot')
        # self.handles['jetsAK8'] = AutoHandle( 'slimmedJetsAK8', 'vector<pat::Jet>') # for all jetsAK8


    def beginLoop(self, setup):
        super(HbbTagComputer,self).beginLoop(setup)


    def Hbbtag(self, jet, i):
        # print "IPTagInfo", self.IPTagInfo[i], len(self.IPTagInfo)
        # print "SVTagInfo", self.SVTagInfo[i], len(self.SVTagInfo)
        return self.hbbComputer.discriminator(jet.physObj, self.IPTagInfo[i], self.SVTagInfo[i])
        # return self.hbbComputer.discriminator(jet, self.IPTagInfo[i], self.SVTagInfo[i]) # for all jetsAK8

    def process(self, event):
        self.readCollections( event.input )
        pVertices = self.handles['primaryVertices'].product()
        pCandidates = self.handles['packedCandidates'].product()
        sVertices = self.handles['secondaryVertices'].product()
        beamSpot = self.handles['beamSpot'].product()
        # jets = self.handles['jetsAK8'].product() # for all jetsAK8
        jets  = ROOT.std.vector(ROOT.pat.Jet)()
        for jet in event.jetsAK8:
            jets.push_back(jet.physObj)
        self.IPTagInfo = self.ipProducerLight.produce(jets, pVertices, pCandidates)
        # print type(self.IPTagInfo)
        self.SVTagInfo = self.secondaryVertexProducerLight.produce(jets, self.IPTagInfo, pCandidates, sVertices, beamSpot)
        # print type(self.SVTagInfo)
        for i,jet in enumerate(event.jetsAK8):
        # for i,jet in enumerate(jets):  # for all jetsAK8
            jet.Hbbtag = self.Hbbtag(jet, i)
            # print jet.Hbbtag, jet.pt


setattr(HbbTagComputer,"defaultConfig", cfg.Analyzer(
    class_object=HbbTagComputer,
    primaryVertices='offlineSlimmedPrimaryVertices',
    secondaryVertices='slimmedSecondaryVertices',
    packedCandidates='packedPFCandidates',
    beamSpot='offlineBeamSpot'
    )
)
