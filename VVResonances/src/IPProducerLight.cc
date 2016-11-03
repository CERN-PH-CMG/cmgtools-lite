// system include files
#include <cmath>
#include <memory>
#include <iostream>
#include <algorithm>

#include "boost/bind.hpp"

#include "CMGTools/VVResonances/interface/IPProducerLight.h"

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "DataFormats/Common/interface/View.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ParameterSet/interface/ConfigurationDescriptions.h"
#include "FWCore/ParameterSet/interface/ParameterSetDescription.h"

#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/JetReco/interface/JetTracksAssociation.h"
#include "DataFormats/BTauReco/interface/JetTag.h"
#include "DataFormats/BTauReco/interface/TrackIPTagInfo.h"
#include "DataFormats/Candidate/interface/Candidate.h"

#include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"
#include "TrackingTools/IPTools/interface/IPTools.h"
#include "TrackingTools/Records/interface/TransientTrackRecord.h"

#include "RecoVertex/VertexPrimitives/interface/VertexState.h"
#include "RecoVertex/VertexPrimitives/interface/ConvertError.h"
#include "RecoVertex/VertexPrimitives/interface/ConvertToFromReco.h"
#include "RecoVertex/VertexTools/interface/VertexDistance3D.h"
#include "RecoVertex/GhostTrackFitter/interface/GhostTrack.h"
// #include "RecoVertex/GhostTrackFitter/interface/GhostTrackState.h"
// #include "RecoVertex/GhostTrackFitter/interface/GhostTrackPrediction.h"
// #include "RecoVertex/GhostTrackFitter/interface/GhostTrackFitter.h"

#include "RecoBTag/TrackProbability/interface/HistogramProbabilityEstimator.h"
#include "DataFormats/BTauReco/interface/JTATagInfo.h"
#include "DataFormats/BTauReco/interface/JetTagInfo.h"

// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "FWCore/Framework/interface/ConsumesCollector.h"

class HistogramProbabilityEstimator;
using boost::bind;

namespace cmg {

IPProducerLightHelpers::FromJetAndCands::FromJetAndCands(double maxDeltaR, bool explicitJTA):
m_maxDeltaR(maxDeltaR),
m_explicitJTA(explicitJTA)
{
}

const std::vector<reco::CandidatePtr>& IPProducerLightHelpers::FromJetAndCands::tracks(const reco::JetTagInfo & it)
{
    return m_map[it.jet().key()];
}

// const std::vector<int>& IPProducerLightHelpers::FromJetAndCands::tracksIndex(const reco::JetTagInfo & it)
// {
//     return m_mapIndex[it.jet().key()];
// }


std::vector<reco::JetTagInfo> IPProducerLightHelpers::FromJetAndCands::makeBaseVector(const std::vector<pat::Jet> &jets, const std::vector<pat::PackedCandidate> &cands){

    std::vector<reco::JetTagInfo> bases;

    m_map.clear();
    m_map.resize(jets.size());
    // m_mapIndex.clear();
    // m_mapIndex.resize(jets.size());
    double maxDeltaR2 = m_maxDeltaR*m_maxDeltaR;
    size_t i = 0;
    for(std::vector<pat::Jet>::const_iterator it = jets.begin(); it != jets.end(); it++, i++) {

        pat::Jet uncorrectedJet( *it );
        uncorrectedJet.setP4(uncorrectedJet.correctedP4(0));

        // std::cout << "makeBaseVector jet: " << i << " - " << it->pt() << " - " << uncorrectedJet.pt() << std::endl;
        // edm::Ref<pat::Jet> myRef(jets, i);
        // edm::RefToBase<pat::Jet> jRef(myRef);
        // edm::RefToBase<pat::Jet> jRef(edm::Ref<std::vector<pat::Jet>>(jets, i));
        // edm::Ref<pat::Jet>
        edm::Ref<std::vector<pat::Jet>> edmRef(&jets, i);
        const edm::RefToBase<reco::Jet> jRef(edmRef);

        reco::JetTagInfo jetTag(jRef);
        bases.push_back(jetTag);
        if( m_explicitJTA )
        {
            for(size_t j=0;j<it->numberOfDaughters();++j) {
                if( it->daughterPtr(j)->bestTrack()!=0 && it->daughterPtr(j)->charge() !=0 ){
                    m_map[i].push_back(it->daughterPtr(j));
                }
            }
        }
        else
        {
            for(size_t j=0;j<cands.size();++j) {
                if(cands[j].bestTrack()!=0 && cands[j].charge() !=0 && Geom::deltaR2(cands[j],uncorrectedJet) < maxDeltaR2  ){
                    // edm::Ref<std::vector<pat::PackedCandidate>> edmCandRef(&cands, j);
                    // const edm::RefToBase<reco::CandidatePtr> cRef(edmCandRef);
                    // const reco::CandidatePtr ptr = cands[j].get<reco::CandidatePtr>();
                    const edm::Ptr<reco::Candidate> ptr((const reco::Candidate*)&cands[j], j);
	                //    m_map[i].push_back(edmCandRef);
                    m_map[i].push_back(ptr);
                    // m_mapIndex[i].push_back(j);
                }
            }
        }
    }
    return bases;
}


//
// constructors and destructor
//
IPProducerLight::IPProducerLight(bool computeProbabilities, bool computeGhostTrack, double ghostTrackPriorDeltaR,
int cutPixelHits, int cutTotalHits, double cutMaxTIP, double cutMinPt, double cutMaxChiSquared,
double cutMaxLIP, bool directionWithTracks, bool directionWithGhostTrack, bool useTrackQuality,
double maxDeltaR, bool explicitJTA) :
    m_computeProbabilities(computeProbabilities),
    m_computeGhostTrack(computeGhostTrack),
    m_ghostTrackPriorDeltaR(ghostTrackPriorDeltaR),
    m_cutPixelHits(cutPixelHits),
    m_cutTotalHits(cutTotalHits),
    m_cutMaxTIP(cutMaxTIP),
    m_cutMinPt(cutMinPt),
    m_cutMaxChiSquared(cutMaxChiSquared),
    m_cutMaxLIP(cutMaxLIP),
    m_directionWithTracks(directionWithTracks),
    m_directionWithGhostTrack(directionWithGhostTrack),
    m_useTrackQuality(useTrackQuality),
    m_helper(maxDeltaR, explicitJTA)
{
    paramField = new OAEParametrizedMagneticField("3_8T");
  // m_calibrationCacheId3D = 0;
  // m_calibrationCacheId2D = 0;

  // token_primaryVertex       = consumes<reco::VertexCollection>(m_config.getParameter<edm::InputTag>("primaryVertex"));
  //
  // m_computeProbabilities    = m_config.getParameter<bool>("computeProbabilities");
  // m_computeGhostTrack       = m_config.getParameter<bool>("computeGhostTrack");
  // m_ghostTrackPriorDeltaR   = m_config.getParameter<double>("ghostTrackPriorDeltaR");
  // m_cutPixelHits            = m_config.getParameter<int>("minimumNumberOfPixelHits");
  // m_cutTotalHits            = m_config.getParameter<int>("minimumNumberOfHits");
  // m_cutMaxTIP               = m_config.getParameter<double>("maximumTransverseImpactParameter");
  // m_cutMinPt                = m_config.getParameter<double>("minimumTransverseMomentum");
  // m_cutMaxChiSquared        = m_config.getParameter<double>("maximumChiSquared");
  // m_cutMaxLIP               = m_config.getParameter<double>("maximumLongitudinalImpactParameter");
  // m_directionWithTracks     = m_config.getParameter<bool>("jetDirectionUsingTracks");
  // m_directionWithGhostTrack = m_config.getParameter<bool>("jetDirectionUsingGhostTrack");
  // m_useTrackQuality         = m_config.getParameter<bool>("useTrackQuality");
  //
  // if (m_computeGhostTrack)
  //   produces<reco::TrackCollection>("ghostTracks");
  // produces<Product>();
}

IPProducerLight::~IPProducerLight()
{
}

//
// member functions
//
// ------------ method called to produce the data  ------------
std::vector<reco::CandIPTagInfo> IPProducerLight::produce(const std::vector<pat::Jet> &jets, const std::vector<reco::Vertex> &primaryVertex, const std::vector<pat::PackedCandidate> &cands)
{
   // Update probability estimator if event setup is changed
   // if (m_computeProbabilities)
   //   checkEventSetup(iSetup);


   // edm::Handle<reco::VertexCollection> primaryVertex;
   // iEvent.getByToken(token_primaryVertex, primaryVertex);

   // edm::ESHandle<TransientTrackBuilder> builder;
   // iSetup.get<TransientTrackRecord>().get("TransientTrackBuilder", builder);

   // output collections
   // std::auto_ptr<Product> result(new Product);

   // std::auto_ptr<reco::TrackCollection> ghostTracks;
   // reco::TrackRefProd ghostTrackRefProd;
   // if (m_computeGhostTrack) {
   //   ghostTracks.reset(new reco::TrackCollection);
   //   ghostTrackRefProd = iEvent.getRefBeforePut<reco::TrackCollection>("ghostTracks");
   // }

   std::vector<reco::CandIPTagInfo> jetTagInfo;

   // use first pv of the collection
   reco::Vertex dummy;
   const reco::Vertex *pv = &dummy;
   edm::Ref<reco::VertexCollection> pvRef;
   if (primaryVertex.size() != 0) {
     pv = &primaryVertex[0];
     // we always use the first vertex (at the moment)
     pvRef = edm::Ref<reco::VertexCollection>(&primaryVertex, 0);
    //  std::cout << "found PV" << std::endl;
   } else { // create a dummy PV
     reco::Vertex::Error e;
     e(0, 0) = 0.0015 * 0.0015;
     e(1, 1) = 0.0015 * 0.0015;
     e(2, 2) = 15. * 15.;
     reco::Vertex::Point p(0, 0, 0);
     dummy = reco::Vertex(p, e, 0, 0, 0);
   }

   std::vector<reco::JetTagInfo> baseTagInfos = m_helper.makeBaseVector(jets, cands);
   int tagInfoIndex = 0;
   for(std::vector<reco::JetTagInfo>::const_iterator it = baseTagInfos.begin();  it != baseTagInfos.end(); it++, ++tagInfoIndex) {
     std::vector<reco::CandidatePtr> tracks = m_helper.tracks(*it);
     pat::Jet uncorrectedJet( jets[tagInfoIndex] );
     uncorrectedJet.setP4(uncorrectedJet.correctedP4(0));
    //  math::XYZVector jetMomentum = it->jet()->momentum();
     math::XYZVector jetMomentum = uncorrectedJet.momentum();

     if (m_directionWithTracks) {
       jetMomentum *= 0.5;
       for(std::vector<reco::CandidatePtr>::const_iterator itTrack = tracks.begin();
           itTrack != tracks.end(); ++itTrack)
           if (reco::btag::toTrack(*itTrack)->numberOfValidHits() >= m_cutTotalHits)           //minimal quality cuts
	           jetMomentum += (*itTrack)->momentum();
     }

     std::vector<reco::CandidatePtr> selectedTracks;
     std::vector<reco::TransientTrack> transientTracks;

     for(std::vector<reco::CandidatePtr>::const_iterator itTrack = tracks.begin();
         itTrack != tracks.end(); ++itTrack) {
       reco::TransientTrack transientTrack = getTransientTrack(*itTrack);
       const reco::Track & track = transientTrack.track(); //**itTrack;
    //    std::cout << " pt " <<  track.pt() <<
    //         " d0 " <<  fabs(track.d0()) <<
    //         " #hit " <<    track.hitPattern().numberOfValidHits()<<
    //         " ipZ " <<   fabs(track.dz()-pv->z())<<
    //         " chi2 " <<  track.normalizedChi2()<<
    //         " #pixel " <<    track.hitPattern().numberOfValidPixelHits()<< std::endl;

       if (track.pt() > m_cutMinPt &&
           track.hitPattern().numberOfValidHits() >= m_cutTotalHits &&         // min num tracker hits
           track.hitPattern().numberOfValidPixelHits() >= m_cutPixelHits &&
           track.normalizedChi2() < m_cutMaxChiSquared &&
           std::abs(track.dxy(pv->position())) < m_cutMaxTIP &&
           std::abs(track.dz(pv->position())) < m_cutMaxLIP) {
            //    std::cout << "selected" << std::endl;
         selectedTracks.push_back(*itTrack);
         transientTracks.push_back(transientTrack);
        //  std::cout << "found a track" << std::endl;
       }
     }

     GlobalVector direction(jetMomentum.x(), jetMomentum.y(), jetMomentum.z());
    //  std::cout << "jetMomentum.x(): "<< jetMomentum.x() << std::endl;

     std::auto_ptr<reco::GhostTrack> ghostTrack;
     reco::TrackRef ghostTrackRef;
    //  if (m_computeGhostTrack) {
    //    reco::GhostTrackFitter fitter;
    //    GlobalPoint origin = RecoVertex::convertPos(pv->position());
    //    GlobalError error = RecoVertex::convertError(pv->error());
    //    ghostTrack.reset(new reco::GhostTrack(fitter.fit(origin, error, direction,
    //                                               m_ghostTrackPriorDeltaR,
    //                                               transientTracks)));
     //
    //    ghostTrackRef = reco::TrackRef(ghostTrackRefProd, ghostTracks->size());
    //    ghostTracks->push_back(*ghostTrack);
     //
    //    if (m_directionWithGhostTrack) {
    //      const reco::GhostTrackPrediction &pred = ghostTrack->prediction();
    //      double lambda = pred.lambda(origin);
    //      dummy = reco::Vertex(RecoVertex::convertPos(pred.position(lambda)),
    //                     RecoVertex::convertError(pred.positionError(lambda)),
    //                     0, 0, 0);
    //      pv = &dummy;
    //      direction = pred.direction();
    //    }
    //  }

     std::vector<float> prob2D, prob3D;
     std::vector<reco::btag::TrackIPData> ipData;

     for(unsigned int ind = 0; ind < transientTracks.size(); ind++) {
        //  std::cout << "track loop: " << ind << std::endl;
       const reco::TransientTrack &transientTrack = transientTracks[ind];
    //    const reco::Track & track = transientTrack.track();

       reco::btag::TrackIPData trackIP;
       trackIP.ip3d = IPTools::signedImpactParameter3D(transientTrack, direction, *pv).second;
       trackIP.ip2d = IPTools::signedTransverseImpactParameter(transientTrack, direction, *pv).second;
    //    std::cout << "IPTools::signedTransverseImpactParameter(transientTrack, direction, *pv).second: "<< IPTools::signedTransverseImpactParameter(transientTrack, direction, *pv).second.value() << std::endl;

       TrajectoryStateOnSurface closest =
               IPTools::closestApproachToJet(transientTrack.impactPointState(),
                                             *pv, direction,
                                             transientTrack.field());
       if (closest.isValid())
         trackIP.closestToJetAxis = closest.globalPosition();

       // TODO: cross check if it is the same using other methods
       trackIP.distanceToJetAxis = IPTools::jetTrackDistance(transientTrack, direction, *pv).second;

       if (ghostTrack.get()) {
         const std::vector<reco::GhostTrackState> &states = ghostTrack->states();
         std::vector<reco::GhostTrackState>::const_iterator pos =
                std::find_if(states.begin(), states.end(),
                             bind(std::equal_to<reco::TransientTrack>(),
                                  bind(&reco::GhostTrackState::track, _1),
                                  transientTrack));

         if (pos != states.end() && pos->isValid()) {
           VertexDistance3D dist;
           const reco::GhostTrackPrediction &pred = ghostTrack->prediction();
           GlobalPoint p1 = pos->tsos().globalPosition();
           GlobalError e1 = pos->tsos().cartesianError().position();
           GlobalPoint p2 = pred.position(pos->lambda());
           GlobalError e2 = pred.positionError(pos->lambda());
           trackIP.closestToGhostTrack = p1;
           trackIP.distanceToGhostTrack = dist.distance(VertexState(p1, e1),
                                                        VertexState(p2, e2));
           trackIP.ghostTrackWeight = pos->weight();
         } else {
           trackIP.distanceToGhostTrack = Measurement1D(-1. -1.);
           trackIP.ghostTrackWeight = 0.;
         }
       } else {
         trackIP.distanceToGhostTrack = Measurement1D(-1. -1.);
         trackIP.ghostTrackWeight = 1.;
       }

       ipData.push_back(trackIP);

    //    if (m_computeProbabilities) {
    //      //probability with 3D ip
    //      std::pair<bool,double> probability = m_probabilityEstimator->probability(m_useTrackQuality, 0,ipData.back().ip3d.significance(),track,*(it->jet()),*pv);
    //      prob3D.push_back(probability.first ? probability.second : -1.);
       //
    //      //probability with 2D ip
    //      probability = m_probabilityEstimator->probability(m_useTrackQuality,1,ipData.back().ip2d.significance(),track,*(it->jet()),*pv);
    //      prob2D.push_back(probability.first ? probability.second : -1.);
    //    }
     }

    //  result->push_back(typename Product::value_type(ipData, prob2D, prob3D, selectedTracks,
    //                          *it, pvRef, direction, ghostTrackRef));
        // Product is
        // typedef std::vector<reco::IPTagInfo<Container,Base> > Product;
        // std::vector<reco::CandidatePtr>,reco::JetTagInfo
        reco::CandIPTagInfo jtInfo(ipData, prob2D, prob3D, selectedTracks,
                                 *it, pvRef, direction, ghostTrackRef);
        jetTagInfo.push_back(jtInfo);
        // jetTagInfo.push_back(typename Product::value_type(ipData, prob2D, prob3D, selectedTracks,
                                //  *it, pvRef, direction, ghostTrackRef));
   }

   // if (m_computeGhostTrack)
   //   iEvent.put(ghostTracks, "ghostTracks");
   // iEvent.put(result);
   return jetTagInfo;
}


// #include "CondFormats/BTauObjects/interface/TrackProbabilityCalibration.h"
// #include "CondFormats/DataRecord/interface/BTagTrackProbability2DRcd.h"
// #include "CondFormats/DataRecord/interface/BTagTrackProbability3DRcd.h"
// #include "FWCore/Framework/interface/EventSetupRecord.h"
// #include "FWCore/Framework/interface/EventSetupRecordImplementation.h"
// #include "FWCore/Framework/interface/EventSetupRecordKey.h"
//
// template <class Container, class Base, class Helper> void IPProducerLight<Container,Base,Helper>::checkEventSetup(const edm::EventSetup & iSetup)
//  {
//   using namespace edm;
//   using namespace edm::eventsetup;
//
//    const EventSetupRecord & re2D= iSetup.get<BTagTrackProbability2DRcd>();
//    const EventSetupRecord & re3D= iSetup.get<BTagTrackProbability3DRcd>();
//    unsigned long long cacheId2D= re2D.cacheIdentifier();
//    unsigned long long cacheId3D= re3D.cacheIdentifier();
//
//    if(cacheId2D!=m_calibrationCacheId2D || cacheId3D!=m_calibrationCacheId3D  )  //Calibration changed
//    {
//      //iSetup.get<BTagTrackProbabilityRcd>().get(calib);
//      edm::ESHandle<TrackProbabilityCalibration> calib2DHandle;
//      iSetup.get<BTagTrackProbability2DRcd>().get(calib2DHandle);
//      edm::ESHandle<TrackProbabilityCalibration> calib3DHandle;
//      iSetup.get<BTagTrackProbability3DRcd>().get(calib3DHandle);
//
//      const TrackProbabilityCalibration *  ca2D= calib2DHandle.product();
//      const TrackProbabilityCalibration *  ca3D= calib3DHandle.product();
//
//      m_probabilityEstimator.reset(new HistogramProbabilityEstimator(ca3D,ca2D));
//
//    }
//    m_calibrationCacheId3D=cacheId3D;
//    m_calibrationCacheId2D=cacheId2D;
// }


// void IPProducerLight<std::vector<reco::CandidatePtr>,reco::JetTagInfo,  IPProducerLightHelpers::FromJetAndCands>::fillDescriptions(edm::ConfigurationDescriptions & descriptions) {
//
//   edm::ParameterSetDescription desc;
//   desc.add<double>("maximumTransverseImpactParameter",0.2);
//   desc.add<int>("minimumNumberOfHits",8);
//   desc.add<double>("minimumTransverseMomentum",1.0);
//   desc.add<edm::InputTag>("primaryVertex",edm::InputTag("offlinePrimaryVertices"));
//   desc.add<double>("maximumLongitudinalImpactParameter",17.0);
//   desc.add<bool>("computeGhostTrack",true);
//   desc.add<double>("maxDeltaR",0.4);
//   desc.add<edm::InputTag>("candidates",edm::InputTag("particleFlow"));
//   desc.add<bool>("jetDirectionUsingGhostTrack",false);
//   desc.add<int>("minimumNumberOfPixelHits",2);
//   desc.add<bool>("jetDirectionUsingTracks",false);
//   desc.add<bool>("computeProbabilities",true);
//   desc.add<bool>("useTrackQuality",false);
//   desc.add<edm::InputTag>("jets",edm::InputTag("ak4PFJetsCHS"));
//   desc.add<double>("ghostTrackPriorDeltaR",0.03);
//   desc.add<double>("maximumChiSquared",5.0);
//   desc.addOptional<bool>("explicitJTA",false);
//   descriptions.addDefault(desc);
// }

reco::TransientTrack IPProducerLight::getTransientTrack(const reco::CandidatePtr& trackRef) const
{

        reco::TransientTrack transientTrack(trackRef, paramField);
        return transientTrack;

}

} // namespace cmg
