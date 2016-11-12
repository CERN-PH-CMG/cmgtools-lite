#ifndef CMGTools_VVResonances_IPProducerLight
#define CMGTools_VVResonances_IPProducerLight

// system include files
#include <cmath>
#include <memory>
#include <iostream>
#include <algorithm>

#include "boost/bind.hpp"

// user include files
// #include "FWCore/Framework/interface/Frameworkfwd.h"
// #include "FWCore/Framework/interface/Event.h"
// #include "DataFormats/Common/interface/View.h"
// #include "FWCore/Framework/interface/MakerMacros.h"
// #include "FWCore/Framework/interface/EventSetup.h"
// #include "FWCore/Framework/interface/ESHandle.h"
// #include "FWCore/ParameterSet/interface/ParameterSet.h"
// #include "FWCore/ParameterSet/interface/ConfigurationDescriptions.h"
// #include "FWCore/ParameterSet/interface/ParameterSetDescription.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "MagneticField/ParametrizedEngine/src/OAEParametrizedMagneticField.h"

#include "DataFormats/TrackReco/interface/Track.h"
// #include "DataFormats/JetReco/interface/JetTracksAssociation.h"
// #include "DataFormats/BTauReco/interface/JetTag.h"
// #include "DataFormats/BTauReco/interface/TrackIPTagInfo.h"


#include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"
// #include "TrackingTools/IPTools/interface/IPTools.h"
// #include "TrackingTools/Records/interface/TransientTrackRecord.h"

// #include "RecoVertex/VertexPrimitives/interface/VertexState.h"
// #include "RecoVertex/VertexPrimitives/interface/ConvertError.h"
// #include "RecoVertex/VertexPrimitives/interface/ConvertToFromReco.h"
// #include "RecoVertex/VertexTools/interface/VertexDistance3D.h"

#include "RecoBTag/TrackProbability/interface/HistogramProbabilityEstimator.h"
// #include "DataFormats/BTauReco/interface/JTATagInfo.h"
#include "DataFormats/BTauReco/interface/JetTagInfo.h"
#include "DataFormats/BTauReco/interface/CandIPTagInfo.h"



class HistogramProbabilityEstimator;
using boost::bind;

namespace cmg {

namespace IPProducerLightHelpers {

      class FromJetAndCands{
              public:
              FromJetAndCands(double maxDeltaR, bool explicitJTA);

              const std::vector<reco::CandidatePtr> & tracks(const reco::JetTagInfo & it);
            //   const std::vector<int>& tracksIndex(const reco::JetTagInfo & it);
              std::vector<reco::JetTagInfo>  makeBaseVector(const std::vector<pat::Jet> &jets, const std::vector<pat::PackedCandidate> &cands);
		      std::vector<std::vector<reco::CandidatePtr> > m_map;
            //   std::vector<int> m_mapIndex;
		      double m_maxDeltaR;
		      bool   m_explicitJTA;
      };
}


class IPProducerLight {
   public:

    //   typedef std::vector<reco::IPTagInfo<std::vector<reco::CandidatePtr>,reco::JetTagInfo> > Product;

      explicit IPProducerLight(bool computeProbabilities, bool computeGhostTrack, double ghostTrackPriorDeltaR,
      int cutPixelHits, int cutTotalHits, double cutMaxTIP, double cutMinPt, double cutMaxChiSquared,
      double cutMaxLIP, bool directionWithTracks, bool directionWithGhostTrack, bool useTrackQuality,
      double maxDeltaR, bool explicitJTA);

      ~IPProducerLight();

    //   static void fillDescriptions(edm::ConfigurationDescriptions & descriptions);

      std::vector<reco::CandIPTagInfo> produce(const std::vector<pat::Jet> &jets, const std::vector<reco::Vertex> &primaryVertex, const std::vector<pat::PackedCandidate> &cands);
      reco::TransientTrack getTransientTrack(const reco::CandidatePtr& trackRef) const;

   private:
    // void  checkEventSetup(const edm::EventSetup & iSetup);

    // edm::EDGetTokenT<reco::VertexCollection> token_primaryVertex;
    OAEParametrizedMagneticField *paramField;

    bool m_computeProbabilities;
    bool m_computeGhostTrack;
    double m_ghostTrackPriorDeltaR;
    std::auto_ptr<HistogramProbabilityEstimator> m_probabilityEstimator;
    // unsigned long long  m_calibrationCacheId2D;
    // unsigned long long  m_calibrationCacheId3D;
    bool m_useDB;

    int  m_cutPixelHits;
    int  m_cutTotalHits;
    double  m_cutMaxTIP;
    double  m_cutMinPt;
    double  m_cutMaxChiSquared;
    double  m_cutMaxLIP;
    bool  m_directionWithTracks;
    bool  m_directionWithGhostTrack;
    bool  m_useTrackQuality;
    IPProducerLightHelpers::FromJetAndCands m_helper;
};

} //namespace cmg

#endif
