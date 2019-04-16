#ifndef CMGTools_VVResonances_CandidateBoostedDoubleSecondaryVertexComputerLight_h
#define CMGTools_VVResonances_CandidateBoostedDoubleSecondaryVertexComputerLight_h

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "CommonTools/MVAUtils/interface/TMVAEvaluator.h"
#include "DataFormats/JetReco/interface/JetCollection.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/Candidate/interface/VertexCompositePtrCandidate.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "RecoBTag/SecondaryVertex/interface/V0Filter.h"
#include "RecoBTag/SecondaryVertex/interface/TrackSelector.h"
#include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"
#include "MagneticField/ParametrizedEngine/src/OAEParametrizedMagneticField.h"
#include "DataFormats/BTauReco/interface/CandIPTagInfo.h"

#include "fastjet/PseudoJet.hh"

namespace cmg{

    class CandidateBoostedDoubleSecondaryVertexComputerLight {

      public:
        CandidateBoostedDoubleSecondaryVertexComputerLight(
            double beta, double R0, double maxSVDeltaRToJet, std::string gbrForestLabel,
            std::string weightFile, bool useGBRForest, bool useAdaBoost, double k0sMassWindow,
            unsigned int totalHitsMin, double jetDeltaRMax, std::string qualityClass, unsigned int pixelHitsMin,
            double maxDistToAxis, double maxDecayLen, double sip3dSigMin, double sip3dSigMax,
            double sip2dValMax, double ptMin, double sip2dSigMax, double sip2dSigMin,
            double sip3dValMax, double sip3dValMin, double sip2dValMin, double normChi2Max
        );
        // typedef std::vector<reco::IPTagInfo<std::vector<reco::CandidatePtr>,reco::JetTagInfo> > IPProduct;

        void  initialize();
        float discriminator(const pat::Jet& jet, const reco::CandIPTagInfo ipTagInfo, const reco::CandSecondaryVertexTagInfo svTagInfo) const;
        reco::TransientTrack getTransientTrack(const reco::CandidatePtr& trackRef) const;

      private:
        // void calcNsubjettiness(const reco::JetBaseRef & jet, float & tau1, float & tau2, std::vector<fastjet::PseudoJet> & currentAxes) const;
        void calcNsubjettiness(const pat::Jet& jet, float & tau1, float & tau2, std::vector<fastjet::PseudoJet> & currentAxes) const;
        void setTracksPVBase(const reco::TrackRef & trackRef, const reco::VertexRef & vertexRef, float & PVweight) const;
        void setTracksPV(const reco::CandidatePtr & trackRef, const reco::VertexRef & vertexRef, float & PVweight) const;
        void etaRelToTauAxis(const reco::VertexCompositePtrCandidate & vertex, fastjet::PseudoJet & tauAxis, std::vector<float> & tau_trackEtaRel) const;

        reco::V0Filter *trackPairV0Filter;
        reco::TrackSelector *trackSelector;
        OAEParametrizedMagneticField *paramField;

        const double beta_;
        const double R0_;

        const double maxSVDeltaRToJet_;
        const std::string gbrForestLabel_;
        const edm::FileInPath weightFile_;
        const bool useGBRForest_;
        const bool useAdaBoost_;
        const double maxDistToAxis_;
        const double maxDecayLen_;

        edm::ESHandle<TransientTrackBuilder> trackBuilder;
        std::unique_ptr<TMVAEvaluator> mvaID;

        // static variables
        static constexpr float dummyZ_ratio             = -3.0f;
        static constexpr float dummyTrackSip3dSig       = -50.0f;
        static constexpr float dummyTrackSip2dSigAbove  = -19.0f;
        static constexpr float dummyTrackEtaRel         = -1.0f;
        static constexpr float dummyVertexMass          = -1.0f;
        static constexpr float dummyVertexEnergyRatio   = -1.0f;
        static constexpr float dummyVertexDeltaR        = -1.0f;
        static constexpr float dummyFlightDistance2dSig = -1.0f;

        static constexpr float charmThreshold  = 1.5f;
        static constexpr float bottomThreshold = 5.2f;

    };

} // end namespace cmg

#endif // CMGTools_VVResonances_CandidateBoostedDoubleSecondaryVertexComputerLight_h
