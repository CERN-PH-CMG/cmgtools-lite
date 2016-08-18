#include <functional>
#include <algorithm>
#include <iterator>
#include <cstddef>
#include <string>
#include <vector>
#include <map>
#include <set>

#include <boost/iterator/transform_iterator.hpp>

#include "CMGTools/VVResonances/interface/SecondaryVertexProducerLight.h"

#include "FWCore/Framework/interface/stream/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ParameterSet/interface/ConfigurationDescriptions.h"
#include "FWCore/ParameterSet/interface/ParameterSetDescription.h"
#include "FWCore/ParameterSet/interface/IfExistsDescription.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/Utilities/interface/Exception.h"

#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"

#include "DataFormats/GeometryCommonDetAlgo/interface/Measurement1D.h"
#include "DataFormats/BTauReco/interface/TrackIPTagInfo.h"
#include "DataFormats/BTauReco/interface/CandIPTagInfo.h"
#include "DataFormats/BTauReco/interface/SecondaryVertexTagInfo.h"

#include "RecoVertex/VertexPrimitives/interface/VertexException.h"
#include "RecoVertex/VertexPrimitives/interface/ConvertToFromReco.h"
#include "RecoVertex/ConfigurableVertexReco/interface/ConfigurableVertexReconstructor.h"
#include "RecoVertex/GhostTrackFitter/interface/GhostTrackVertexFinder.h"
#include "RecoVertex/GhostTrackFitter/interface/GhostTrackPrediction.h"
#include "RecoVertex/GhostTrackFitter/interface/GhostTrackState.h"
#include "RecoVertex/GhostTrackFitter/interface/GhostTrack.h"

#include "TrackingTools/TransientTrack/interface/TransientTrack.h"
#include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"
#include "TrackingTools/TransientTrack/interface/CandidatePtrTransientTrack.h"
#include "TrackingTools/Records/interface/TransientTrackRecord.h"

#include "RecoBTag/SecondaryVertex/interface/TrackSelector.h"
#include "RecoBTag/SecondaryVertex/interface/TrackSorting.h"
#include "RecoBTag/SecondaryVertex/interface/SecondaryVertex.h"
#include "RecoBTag/SecondaryVertex/interface/VertexFilter.h"
#include "RecoBTag/SecondaryVertex/interface/VertexSorting.h"

#include "DataFormats/GeometryVector/interface/VectorUtil.h"

#include "fastjet/JetDefinition.hh"
#include "fastjet/ClusterSequence.hh"
#include "fastjet/PseudoJet.hh"

//
// constants, enums and typedefs
//
typedef boost::shared_ptr<fastjet::ClusterSequence>  ClusterSequencePtr;
typedef boost::shared_ptr<fastjet::JetDefinition>    JetDefPtr;


using namespace reco;


namespace cmg {

GlobalVector flightDirection(const reco::Vertex & pv, const reco::Vertex & sv) {
return  GlobalVector(sv.x() - pv.x(), sv.y() - pv.y(),sv.z() - pv.z());
}
GlobalVector flightDirection(const reco::Vertex & pv, const reco::VertexCompositePtrCandidate & sv) {
return  GlobalVector(sv.vertex().x() - pv.x(), sv.vertex().y() - pv.y(),sv.vertex().z() - pv.z());
}
const math::XYZPoint & position(const reco::Vertex & sv)
{return sv.position();}
const math::XYZPoint & position(const reco::VertexCompositePtrCandidate & sv)
{return sv.vertex();}



// template <class CandIPTagInfo,class reco::VertexCompositePtrCandidate>
// typename SecondaryVertexProducerLight<CandIPTagInfo,reco::VertexCompositePtrCandidate>::ConstraintType
// SecondaryVertexProducerLight<CandIPTagInfo,reco::VertexCompositePtrCandidate>::getConstraintType(const std::string &name)
// {
// 	if (name == "None")
// 		return CONSTRAINT_NONE;
// 	else if (name == "BeamSpot")
// 		return CONSTRAINT_BEAMSPOT;
// 	else if (name == "BeamSpot+PVPosition")
// 		return CONSTRAINT_PV_BEAMSPOT_SIZE;
// 	else if (name == "BeamSpotZ+PVErrorScaledXY")
// 		return CONSTRAINT_PV_BS_Z_ERRORS_SCALED;
// 	else if (name == "PVErrorScaled")
// 		return CONSTRAINT_PV_ERROR_SCALED;
// 	else if (name == "BeamSpot+PVTracksInFit")
// 		return CONSTRAINT_PV_PRIMARIES_IN_FIT;
// 	else
// 		throw cms::Exception("InvalidArgument")
// 			<< "SecondaryVertexProducerLight: ``constraint'' parameter "
// 			   "value \"" << name << "\" not understood."
// 			<< std::endl;
// }

// static GhostTrackVertexFinder::FitType
// getGhostTrackFitType(const std::string &name)
// {
// 	if (name == "AlwaysWithGhostTrack")
// 		return GhostTrackVertexFinder::kAlwaysWithGhostTrack;
// 	else if (name == "SingleTracksWithGhostTrack")
// 		return GhostTrackVertexFinder::kSingleTracksWithGhostTrack;
// 	else if (name == "RefitGhostTrackWithVertices")
// 		return GhostTrackVertexFinder::kRefitGhostTrackWithVertices;
// 	else
// 		throw cms::Exception("InvalidArgument")
// 			<< "SecondaryVertexProducerLight: ``fitType'' "
// 			   "parameter value \"" << name << "\" for "
// 			   "GhostTrackVertexFinder settings not "
// 			   "understood." << std::endl;
// }

SecondaryVertexProducerLight::SecondaryVertexProducerLight(
	unsigned int totalHitsMin, double jetDeltaRMax, std::string qualityClass, unsigned int pixelHitsMin,
	double maxDistToAxis, double maxDecayLen, double sip3dSigMin, double sip3dSigMax,
	double sip2dValMax, double ptMin, double sip2dSigMax, double sip2dSigMin,
	double sip3dValMax, double sip3dValMin, double sip2dValMin, double normChi2Max,
	bool usePVError, double minimumTrackWeight, std::string trackSort,
	double extSVDeltaRToJet, std::string sortCriterium,
	double distVal2dMin, double distVal2dMax,
	double distSig2dMin, double distSig2dMax,
	double distSig3dMin, double distSig3dMax,
	double distVal3dMin, double distVal3dMax,
	double fracPV, bool useTrackWeights, double maxDeltaRToJetAxis,
	int multiplicityMin, double massMax, double k0sMassWindow
/*const edm::ParameterSet &params*/
/*
trackSort

minimumTrackWeight
useExternalSV
extSVDeltaRToJet
*/

) :
	m_sortCriterium(TrackSorting::getCriterium(trackSort)), // sip3dSig
	// trackSelector(params.getParameter<edm::ParameterSet>("trackSelection")),
	// constraint(getConstraintType(params.getParameter<std::string>("constraint"))),
	// constraintScaling(1.0),
	// vtxRecoPSet(params.getParameter<edm::ParameterSet>("vertexReco")),
	// useGhostTrack(vtxRecoPSet.getParameter<std::string>("finder") == "gtvr"),
	m_withPVError(usePVError),
	m_minTrackWeight(minimumTrackWeight),
	m_extSVDeltaRToJet(extSVDeltaRToJet)
	// vertexFilter(params.getParameter<edm::ParameterSet>("vertexCuts")),
	// vertexSorting(params.getParameter<edm::ParameterSet>("vertexSelection"))
{
	edm::ParameterSet trackSelectionPSet;
	trackSelectionPSet.addParameter<unsigned int>("totalHitsMin", totalHitsMin);
	trackSelectionPSet.addParameter<double>("jetDeltaRMax", jetDeltaRMax);
	trackSelectionPSet.addParameter<std::string>("qualityClass", qualityClass);
	trackSelectionPSet.addParameter<unsigned int>("pixelHitsMin", pixelHitsMin);
	trackSelectionPSet.addParameter<double>("maxDistToAxis", maxDistToAxis);
	trackSelectionPSet.addParameter<double>("maxDecayLen", maxDecayLen);
	trackSelectionPSet.addParameter<double>("sip3dSigMin", sip3dSigMin);
	trackSelectionPSet.addParameter<double>("sip3dSigMax", sip3dSigMax);
	trackSelectionPSet.addParameter<double>("sip2dValMax", sip2dValMax);
	trackSelectionPSet.addParameter<double>("ptMin", ptMin);
	trackSelectionPSet.addParameter<double>("sip2dSigMax", sip2dSigMax);
	trackSelectionPSet.addParameter<double>("sip2dSigMin", sip2dSigMin);
	trackSelectionPSet.addParameter<double>("sip3dValMax", sip3dValMax);
	trackSelectionPSet.addParameter<double>("sip3dValMin", sip3dValMin);
	trackSelectionPSet.addParameter<double>("sip2dValMin", sip2dValMin);
	trackSelectionPSet.addParameter<double>("normChi2Max", normChi2Max);
	trackSelectionPSet.addParameter<double>("useVariableJTA", false);
	m_trackSelector = new reco::TrackSelector(trackSelectionPSet);

	edm::ParameterSet vertexFilterPSet;
    vertexFilterPSet.addParameter<double>("distSig3dMax",distSig3dMax);
    vertexFilterPSet.addParameter<double>("fracPV",fracPV);
    vertexFilterPSet.addParameter<double>("distVal2dMax",distVal2dMax);
    vertexFilterPSet.addParameter<bool>("useTrackWeights",useTrackWeights);
    vertexFilterPSet.addParameter<double>("maxDeltaRToJetAxis",maxDeltaRToJetAxis);
	edm::ParameterSet v0Filter;
	v0Filter.addParameter<double>("k0sMassWindow",k0sMassWindow);
	vertexFilterPSet.addParameter<edm::ParameterSet>("v0Filter",v0Filter);
    vertexFilterPSet.addParameter<double>("distSig2dMin",distSig2dMin);
    vertexFilterPSet.addParameter<unsigned int>("multiplicityMin",multiplicityMin);
    vertexFilterPSet.addParameter<double>("distVal2dMin",distVal2dMin);
    vertexFilterPSet.addParameter<double>("distSig2dMax",distSig2dMax);
    vertexFilterPSet.addParameter<double>("distVal3dMax",distVal3dMax);
    vertexFilterPSet.addParameter<double>("minimumTrackWeight",minimumTrackWeight);
    vertexFilterPSet.addParameter<double>("distVal3dMin",distVal3dMin);
    vertexFilterPSet.addParameter<double>("massMax",massMax);
    vertexFilterPSet.addParameter<double>("distSig3dMin",distSig3dMin);
	m_vertexFilter = new reco::VertexFilter(vertexFilterPSet);

	edm::ParameterSet vertexSelectionPSet;
	vertexSelectionPSet.addParameter<std::string>("sortCriterium",sortCriterium);
	m_vertexSorting = new reco::VertexSorting<SecondaryVertex>(vertexSelectionPSet);

	// token_trackIPTagInfo =  consumes<std::vector<CandIPTagInfo> >(params.getParameter<edm::InputTag>("trackIPTagInfos"));
	// if (constraint == CONSTRAINT_PV_ERROR_SCALED ||
	//     constraint == CONSTRAINT_PV_BS_Z_ERRORS_SCALED)
	// 	constraintScaling = params.getParameter<double>("pvErrorScaling");

	// if (constraint == CONSTRAINT_PV_BEAMSPOT_SIZE ||
	//     constraint == CONSTRAINT_PV_BS_Z_ERRORS_SCALED ||
	//     constraint == CONSTRAINT_BEAMSPOT ||
	//     constraint == CONSTRAINT_PV_PRIMARIES_IN_FIT )
	// token_BeamSpot = consumes<reco::BeamSpot>(params.getParameter<edm::InputTag>("beamSpotTag"));
	// useExternalSV = false;
	// if(params.existsAs<bool>("useExternalSV")) useExternalSV = params.getParameter<bool> ("useExternalSV");
	// if(useExternalSV) {
	//    token_extSVCollection =  consumes<edm::View<reco::VertexCompositePtrCandidate> >(params.getParameter<edm::InputTag>("extSVCollection"));
	//    extSVDeltaRToJet = params.getParameter<double>("extSVDeltaRToJet");
	// }
	// useSVClustering = ( params.existsAs<bool>("useSVClustering") ? params.getParameter<bool>("useSVClustering") : false );
	// useSVMomentum = ( params.existsAs<bool>("useSVMomentum") ? params.getParameter<bool>("useSVMomentum") : false );
	// useFatJets = ( useExternalSV && params.exists("fatJets") );
	// useGroomedFatJets = ( useExternalSV && params.exists("groomedFatJets") );
	// if( useSVClustering )
	// {
	//   jetAlgorithm = params.getParameter<std::string>("jetAlgorithm");
	//   rParam = params.getParameter<double>("rParam");
	//   jetPtMin = 0.; // hardcoded to 0. since we simply want to recluster all input jets which already had some PtMin applied
	//   ghostRescaling = ( params.existsAs<double>("ghostRescaling") ? params.getParameter<double>("ghostRescaling") : 1e-18 );
	//   relPtTolerance = ( params.existsAs<double>("relPtTolerance") ? params.getParameter<double>("relPtTolerance") : 1e-03); // 0.1% relative difference in Pt should be sufficient to detect possible misconfigurations
	//
	//   // set jet algorithm
	//   if (jetAlgorithm=="Kt")
	//     fjJetDefinition = JetDefPtr( new fastjet::JetDefinition(fastjet::kt_algorithm, rParam) );
	//   else if (jetAlgorithm=="CambridgeAachen")
	//     fjJetDefinition = JetDefPtr( new fastjet::JetDefinition(fastjet::cambridge_algorithm, rParam) );
	//   else if (jetAlgorithm=="AntiKt")
	//     fjJetDefinition = JetDefPtr( new fastjet::JetDefinition(fastjet::antikt_algorithm, rParam) );
	//   else
	//     throw cms::Exception("InvalidJetAlgorithm") << "Jet clustering algorithm is invalid: " << jetAlgorithm << ", use CambridgeAachen | Kt | AntiKt" << std::endl;
	// }
	// if( useFatJets )
	//   token_fatJets = consumes<edm::View<reco::Jet> >(params.getParameter<edm::InputTag>("fatJets"));
	// if( useGroomedFatJets )
	//   token_groomedFatJets = consumes<edm::View<reco::Jet> >(params.getParameter<edm::InputTag>("groomedFatJets"));
	// if( useFatJets && !useSVClustering )
	//   rParam = params.getParameter<double>("rParam"); // will be used later as a dR cut

	// produces<Product>();
	m_paramField = new OAEParametrizedMagneticField("3_8T");
}


SecondaryVertexProducerLight::~SecondaryVertexProducerLight()
{
}

std::vector<reco::CandSecondaryVertexTagInfo> SecondaryVertexProducerLight::produce(const std::vector<pat::Jet>& jets, const std::vector<reco::CandIPTagInfo> trackIPTagInfos,
	const std::vector<pat::PackedCandidate> &cands, const std::vector<reco::VertexCompositePtrCandidate> &extSecVertex,
	const reco::BeamSpot& beamSpot)
{
//	typedef std::map<TrackBaseRef, TransientTrack,
//	                 RefToBaseLess<Track> > TransientTrackMap;
	//How about good old pointers?
	typedef std::map<const Track *, TransientTrack> TransientTrackMap;


	// edm::ESHandle<TransientTrackBuilder> trackBuilder;
	// es.get<TransientTrackRecord>().get("TransientTrackBuilder",
	//                                    trackBuilder);

	// edm::Handle<std::vector<CandIPTagInfo> > trackIPTagInfos;
	// event.getByToken(token_trackIPTagInfo, trackIPTagInfos);

        // External Sec Vertex collection (e.g. for IVF usage)
        // edm::Handle<edm::View<reco::VertexCompositePtrCandidate> > extSecVertex;
        // if(useExternalSV) event.getByToken(token_extSVCollection,extSecVertex);

	// edm::Handle<edm::View<reco::Jet> > fatJetsHandle;
	// edm::Handle<edm::View<reco::Jet> > groomedFatJetsHandle;
	// if( useFatJets )
	// {
	//   event.getByToken(token_fatJets, fatJetsHandle);
	//
	//   if( useGroomedFatJets )
	//   {
	//     event.getByToken(token_groomedFatJets, groomedFatJetsHandle);
	//
	//     if( groomedFatJetsHandle->size() > fatJetsHandle->size() )
	//       edm::LogError("TooManyGroomedJets") << "There are more groomed (" << groomedFatJetsHandle->size() << ") than original fat jets (" << fatJetsHandle->size() << "). Please check that the two jet collections belong to each other.";
	//   }
	// }

	// edm::Handle<BeamSpot> beamSpot;
	// unsigned int bsCovSrc[7] = { 0, };
	// double sigmaZ = 0.0, beamWidth = 0.0;
	// switch(constraint) {
	//     case CONSTRAINT_PV_BEAMSPOT_SIZE:
	// 	event.getByToken(token_BeamSpot,beamSpot);
	// 	bsCovSrc[3] = bsCovSrc[4] = bsCovSrc[5] = bsCovSrc[6] = 1;
	// 	sigmaZ = beamSpot->sigmaZ();
	// 	beamWidth = beamSpot->BeamWidthX();
	// 	break;
	//
	//     case CONSTRAINT_PV_BS_Z_ERRORS_SCALED:
	// 	event.getByToken(token_BeamSpot,beamSpot);
	// 	bsCovSrc[0] = bsCovSrc[1] = 2;
	// 	bsCovSrc[3] = bsCovSrc[4] = bsCovSrc[5] = 1;
	// 	sigmaZ = beamSpot->sigmaZ();
	// 	break;
	//
	//     case CONSTRAINT_PV_ERROR_SCALED:
	// 	bsCovSrc[0] = bsCovSrc[1] = bsCovSrc[2] = 2;
	// 	break;
	//
	//     case CONSTRAINT_BEAMSPOT:
	//     case CONSTRAINT_PV_PRIMARIES_IN_FIT:
	// 	event.getByToken(token_BeamSpot,beamSpot);
	// 	break;
	//
	//     default:
	// 	/* nothing */;
	// }

	// ------------------------------------ SV clustering START --------------------------------------------
	// std::vector<std::vector<int> > clusteredSVs(trackIPTagInfos.size(),std::vector<int>());
	// if( useExternalSV && useSVClustering && trackIPTagInfos.size()>0 )
	// {
	//   // vector of constituents for reclustering jets and "ghost" SVs
	//   std::vector<fastjet::PseudoJet> fjInputs;
	//   // loop over all input jets and collect all their constituents
	// //   if( useFatJets )
	// //   {
	// //     for(edm::View<reco::Jet>::const_iterator it = fatJetsHandle->begin(); it != fatJetsHandle->end(); ++it)
	// //     {
	// //       std::vector<edm::Ptr<reco::Candidate> > constituents = it->getJetConstituents();
	// //       std::vector<edm::Ptr<reco::Candidate> >::const_iterator m;
	// //       for( m = constituents.begin(); m != constituents.end(); ++m )
	// //       {
	// // 	 reco::CandidatePtr constit = *m;
	// // 	 if(constit->pt() == 0)
	// // 	 {
	// // 	   edm::LogWarning("NullTransverseMomentum") << "dropping input candidate with pt=0";
	// // 	   continue;
	// // 	 }
	// // 	 fjInputs.push_back(fastjet::PseudoJet(constit->px(),constit->py(),constit->pz(),constit->energy()));
	// //       }
	// //     }
	// //   }
	// //   else
	// //   {
	//     for(typename std::vector<CandIPTagInfo>::const_iterator it = trackIPTagInfos.begin(); it != trackIPTagInfos.end(); ++it)
	//     {
	//       std::vector<edm::Ptr<reco::Candidate> > constituents = it->jet()->getJetConstituents();
	//       std::vector<edm::Ptr<reco::Candidate> >::const_iterator m;
	//       for( m = constituents.begin(); m != constituents.end(); ++m )
	//       {
	// 	 reco::CandidatePtr constit = *m;
	// 	 if(constit->pt() == 0)
	// 	 {
	// 	   edm::LogWarning("NullTransverseMomentum") << "dropping input candidate with pt=0";
	// 	   continue;
	// 	 }
	// 	 fjInputs.push_back(fastjet::PseudoJet(constit->px(),constit->py(),constit->pz(),constit->energy()));
	//       }
	//     }
	// //   }
	//   // insert "ghost" SVs in the vector of constituents
	//   for(typename edm::View<reco::VertexCompositePtrCandidate>::const_iterator it = extSecVertex->begin(); it != extSecVertex->end(); ++it)
	//   {
	//     const reco::Vertex &pv = *(trackIPTagInfos.front().primaryVertex());
	//     GlobalVector dir = flightDirection(pv, *it);
	//     dir = dir.unit();
	//     fastjet::PseudoJet p(dir.x(),dir.y(),dir.z(),dir.mag()); // using SV flight direction so treating SV as massless
	//     if( useSVMomentum )
	//       p = fastjet::PseudoJet(it->p4().px(),it->p4().py(),it->p4().pz(),it->p4().energy());
	//     p*=ghostRescaling; // rescale SV direction/momentum
	//     p.set_user_info(new VertexInfo( it - extSecVertex->begin() ));
	//     fjInputs.push_back(p);
	//   }
	//
	//   // define jet clustering sequence
	//   fjClusterSeq = ClusterSequencePtr( new fastjet::ClusterSequence( fjInputs, *fjJetDefinition ) );
	//   // recluster jet constituents and inserted "ghosts"
	//   std::vector<fastjet::PseudoJet> inclusiveJets = fastjet::sorted_by_pt( fjClusterSeq->inclusive_jets(jetPtMin) );
	//
	// //   if( useFatJets )
	// //   {
	// //     if( inclusiveJets.size() < fatJetsHandle->size() )
	// //       edm::LogError("TooFewReclusteredJets") << "There are fewer reclustered (" << inclusiveJets.size() << ") than original fat jets (" << fatJetsHandle->size() << "). Please check that the jet algorithm and jet size match those used for the original jet collection.";
	//   //
	// //     // match reclustered and original fat jets
	// //     std::vector<int> reclusteredIndices;
	// //     matchReclusteredJets<edm::View<reco::Jet> >(fatJetsHandle,inclusiveJets,reclusteredIndices,"fat");
	//   //
	// //     // match groomed and original fat jets
	// //     std::vector<int> groomedIndices;
	// //     if( useGroomedFatJets )
	// //       matchGroomedJets(fatJetsHandle,groomedFatJetsHandle,groomedIndices);
	//   //
	// //     // match subjets and original fat jets
	// //     std::vector<std::vector<int> > subjetIndices;
	// //     if( useGroomedFatJets )
	// //       matchSubjets(groomedIndices,groomedFatJetsHandle,trackIPTagInfos,subjetIndices);
	// //     else
	// //       matchSubjets(fatJetsHandle,trackIPTagInfos,subjetIndices);
	//   //
	// //     // collect clustered SVs
	// //     for(size_t i=0; i<fatJetsHandle->size(); ++i)
	// //     {
	// //       if( reclusteredIndices.at(i) < 0 ) continue; // continue if matching reclustered to original jets failed
	//   //
	// //       if( fatJetsHandle->at(i).pt() == 0 ) // continue if the original jet has Pt=0
	// //       {
	// //         edm::LogWarning("NullTransverseMomentum") << "The original fat jet " << i << " has Pt=0. This is not expected so the jet will be skipped.";
	// //         continue;
	// //       }
	//   //
	// //       if( subjetIndices.at(i).size()==0 ) continue; // continue if the original jet does not have subjets assigned
	//   //
	// //       // since the "ghosts" are extremely soft, the configuration and ordering of the reclustered and original fat jets should in principle stay the same
	// //       if( ( std::abs( inclusiveJets.at(reclusteredIndices.at(i)).pt() - fatJetsHandle->at(i).pt() ) / fatJetsHandle->at(i).pt() ) > relPtTolerance )
	// //       {
	// // 	 if( fatJetsHandle->at(i).pt() < 10. )  // special handling for low-Pt jets (Pt<10 GeV)
	// // 	   edm::LogWarning("JetPtMismatchAtLowPt") << "The reclustered and original fat jet " << i << " have different Pt's (" << inclusiveJets.at(reclusteredIndices.at(i)).pt() << " vs " << fatJetsHandle->at(i).pt() << " GeV, respectively).\n"
	// // 						   << "Please check that the jet algorithm and jet size match those used for the original fat jet collection and also make sure the original fat jets are uncorrected. In addition, make sure you are not using CaloJets which are presently not supported.\n"
	// // 						   << "Since the mismatch is at low Pt, it is ignored and only a warning is issued.\n"
	// // 						   << "\nIn extremely rare instances the mismatch could be caused by a difference in the machine precision in which case make sure the original jet collection is produced and reclustering is performed in the same job.";
	// // 	 else
	// // 	   edm::LogError("JetPtMismatch") << "The reclustered and original fat jet " << i << " have different Pt's (" << inclusiveJets.at(reclusteredIndices.at(i)).pt() << " vs " << fatJetsHandle->at(i).pt() << " GeV, respectively).\n"
	// // 					  << "Please check that the jet algorithm and jet size match those used for the original fat jet collection and also make sure the original fat jets are uncorrected. In addition, make sure you are not using CaloJets which are presently not supported.\n"
	// // 					  << "\nIn extremely rare instances the mismatch could be caused by a difference in the machine precision in which case make sure the original jet collection is produced and reclustering is performed in the same job.";
	// //       }
	//   //
	// //       // get jet constituents
	// //       std::vector<fastjet::PseudoJet> constituents = inclusiveJets.at(reclusteredIndices.at(i)).constituents();
	//   //
	// //       std::vector<int> svIndices;
	// //       // loop over jet constituents and try to find "ghosts"
	// //       for(std::vector<fastjet::PseudoJet>::const_iterator it = constituents.begin(); it != constituents.end(); ++it)
	// //       {
	// // 	 if( !it->has_user_info() ) continue; // skip if not a "ghost"
	//   //
	// // 	 svIndices.push_back( it->user_info<VertexInfo>().vertexIndex() );
	// //       }
	//   //
	// //       // loop over clustered SVs and assign them to different subjets based on smallest dR
	// //       for(size_t sv=0; sv<svIndices.size(); ++sv)
	// //       {
	// // 	const reco::Vertex &pv = *(trackIPTagInfos.front().primaryVertex());
	// // 	const reco::VertexCompositePtrCandidate &extSV = (*extSecVertex)[ svIndices.at(sv) ];
	// // 	GlobalVector dir = flightDirection(pv, extSV);
	// // 	dir = dir.unit();
	// // 	fastjet::PseudoJet p(dir.x(),dir.y(),dir.z(),dir.mag()); // using SV flight direction so treating SV as massless
	// // 	if( useSVMomentum )
	// // 	  p = fastjet::PseudoJet(extSV.p4().px(),extSV.p4().py(),extSV.p4().pz(),extSV.p4().energy());
	//   //
	// // 	std::vector<double> dR2toSubjets;
	//   //
	// // 	for(size_t sj=0; sj<subjetIndices.at(i).size(); ++sj)
	// // 	  dR2toSubjets.push_back( Geom::deltaR2( p.rapidity(), p.phi_std(), trackIPTagInfos.at(subjetIndices.at(i).at(sj)).jet()->rapidity(), trackIPTagInfos.at(subjetIndices.at(i).at(sj)).jet()->phi() ) );
	//   //
	// // 	// find the closest subjet
	// // 	int closestSubjetIdx = std::distance( dR2toSubjets.begin(), std::min_element(dR2toSubjets.begin(), dR2toSubjets.end()) );
	//   //
	// // 	clusteredSVs.at(subjetIndices.at(i).at(closestSubjetIdx)).push_back( svIndices.at(sv) );
	// //       }
	// //     }
	// //   }
	// //   else
	// //   {
	//     if( inclusiveJets.size() < trackIPTagInfos.size() )
	//       edm::LogError("TooFewReclusteredJets") << "There are fewer reclustered (" << inclusiveJets.size() << ") than original jets (" << trackIPTagInfos.size() << "). Please check that the jet algorithm and jet size match those used for the original jet collection.";
	//
	//     // match reclustered and original jets
	//     std::vector<int> reclusteredIndices;
	//     matchReclusteredJets<std::vector<CandIPTagInfo> >(trackIPTagInfos,inclusiveJets,reclusteredIndices);
	//
	//     // collect clustered SVs
	//     for(size_t i=0; i<trackIPTagInfos.size(); ++i)
	//     {
	//       if( reclusteredIndices.at(i) < 0 ) continue; // continue if matching reclustered to original jets failed
	//
	//       if( trackIPTagInfos.at(i).jet()->pt() == 0 ) // continue if the original jet has Pt=0
	//       {
	//         edm::LogWarning("NullTransverseMomentum") << "The original jet " << i << " has Pt=0. This is not expected so the jet will be skipped.";
	//         continue;
	//       }
	//
	//       // since the "ghosts" are extremely soft, the configuration and ordering of the reclustered and original jets should in principle stay the same
	//       if( ( std::abs( inclusiveJets.at(reclusteredIndices.at(i)).pt() - trackIPTagInfos.at(i).jet()->pt() ) / trackIPTagInfos.at(i).jet()->pt() ) > relPtTolerance )
	//       {
	// 	 if( trackIPTagInfos.at(i).jet()->pt() < 10. )  // special handling for low-Pt jets (Pt<10 GeV)
	// 	   edm::LogWarning("JetPtMismatchAtLowPt") << "The reclustered and original jet " << i << " have different Pt's (" << inclusiveJets.at(reclusteredIndices.at(i)).pt() << " vs " << trackIPTagInfos.at(i).jet()->pt() << " GeV, respectively).\n"
	// 						   << "Please check that the jet algorithm and jet size match those used for the original jet collection and also make sure the original jets are uncorrected. In addition, make sure you are not using CaloJets which are presently not supported.\n"
	// 						   << "Since the mismatch is at low Pt, it is ignored and only a warning is issued.\n"
	// 						   << "\nIn extremely rare instances the mismatch could be caused by a difference in the machine precision in which case make sure the original jet collection is produced and reclustering is performed in the same job.";
	// 	 else
	// 	   edm::LogError("JetPtMismatch") << "The reclustered and original jet " << i << " have different Pt's (" << inclusiveJets.at(reclusteredIndices.at(i)).pt() << " vs " << trackIPTagInfos.at(i).jet()->pt() << " GeV, respectively).\n"
	// 					  << "Please check that the jet algorithm and jet size match those used for the original jet collection and also make sure the original jets are uncorrected. In addition, make sure you are not using CaloJets which are presently not supported.\n"
	// 					  << "\nIn extremely rare instances the mismatch could be caused by a difference in the machine precision in which case make sure the original jet collection is produced and reclustering is performed in the same job.";
	//       }
	//
	//       // get jet constituents
	//       std::vector<fastjet::PseudoJet> constituents = inclusiveJets.at(reclusteredIndices.at(i)).constituents();
	//
	//       // loop over jet constituents and try to find "ghosts"
	//       for(std::vector<fastjet::PseudoJet>::const_iterator it = constituents.begin(); it != constituents.end(); ++it)
	//       {
	// 	 if( !it->has_user_info() ) continue; // skip if not a "ghost"
	// 	 // push back clustered SV indices
	// 	 clusteredSVs.at(i).push_back( it->user_info<VertexInfo>().vertexIndex() );
	//       }
	//     }
	// //   }
	// }
	// case where fat jets are used to associate SVs to subjets but no SV clustering is performed
	// else if( useExternalSV && !useSVClustering && trackIPTagInfos.size()>0 && useFatJets )
	// {
	//   // match groomed and original fat jets
	//   std::vector<int> groomedIndices;
	//   if( useGroomedFatJets )
	//     matchGroomedJets(fatJetsHandle,groomedFatJetsHandle,groomedIndices);
	//
	//   // match subjets and original fat jets
	//   std::vector<std::vector<int> > subjetIndices;
	//   if( useGroomedFatJets )
	//     matchSubjets(groomedIndices,groomedFatJetsHandle,trackIPTagInfos,subjetIndices);
	//   else
	//     matchSubjets(fatJetsHandle,trackIPTagInfos,subjetIndices);
	//
	//   // loop over fat jets
	//   for(size_t i=0; i<fatJetsHandle->size(); ++i)
	//   {
	//     if( fatJetsHandle->at(i).pt() == 0 ) // continue if the original jet has Pt=0
	//     {
	//       edm::LogWarning("NullTransverseMomentum") << "The original fat jet " << i << " has Pt=0. This is not expected so the jet will be skipped.";
	//       continue;
	//     }
	//
	//     if( subjetIndices.at(i).size()==0 ) continue; // continue if the original jet does not have subjets assigned
	//
	//     // loop over SVs, associate them to fat jets based on dR cone and
	//     // then assign them to the closets subjet in dR
	//     for(typename edm::View<reco::VertexCompositePtrCandidate>::const_iterator it = extSecVertex->begin(); it != extSecVertex->end(); ++it)
	//     {
	//       size_t sv = ( it - extSecVertex->begin() );
	//
	//       const reco::Vertex &pv = *(trackIPTagInfos.front().primaryVertex());
	//       const reco::VertexCompositePtrCandidate &extSV = (*extSecVertex)[sv];
	//       GlobalVector dir = flightDirection(pv, extSV);
	//       GlobalVector jetDir(fatJetsHandle->at(i).px(),
	// 			  fatJetsHandle->at(i).py(),
	// 			  fatJetsHandle->at(i).pz());
	//       // skip SVs outside the dR cone
    //           if( Geom::deltaR2( dir, jetDir ) > rParam*rParam ) // here using the jet clustering rParam as a dR cut
	//         continue;
	//
	//       dir = dir.unit();
	//       fastjet::PseudoJet p(dir.x(),dir.y(),dir.z(),dir.mag()); // using SV flight direction so treating SV as massless
	//       if( useSVMomentum )
	// 	p = fastjet::PseudoJet(extSV.p4().px(),extSV.p4().py(),extSV.p4().pz(),extSV.p4().energy());
	//
	//       std::vector<double> dR2toSubjets;
	//
	//       for(size_t sj=0; sj<subjetIndices.at(i).size(); ++sj)
	// 	dR2toSubjets.push_back( Geom::deltaR2( p.rapidity(), p.phi_std(), trackIPTagInfos.at(subjetIndices.at(i).at(sj)).jet()->rapidity(), trackIPTagInfos.at(subjetIndices.at(i).at(sj)).jet()->phi() ) );
	//
	//       // find the closest subjet
	//       int closestSubjetIdx = std::distance( dR2toSubjets.begin(), std::min_element(dR2toSubjets.begin(), dR2toSubjets.end()) );
	//
	//       clusteredSVs.at(subjetIndices.at(i).at(closestSubjetIdx)).push_back(sv);
	//     }
	//   }
	// }
	// ------------------------------------ SV clustering END ----------------------------------------------

	// std::auto_ptr<ConfigurableVertexReconstructor> vertexReco;
	// std::auto_ptr<GhostTrackVertexFinder> vertexRecoGT;
	// if (useGhostTrack)
	// 	vertexRecoGT.reset(new GhostTrackVertexFinder(
	// 		vtxRecoPSet.getParameter<double>("maxFitChi2"),
	// 		vtxRecoPSet.getParameter<double>("mergeThreshold"),
	// 		vtxRecoPSet.getParameter<double>("primcut"),
	// 		vtxRecoPSet.getParameter<double>("seccut"),
	// 		getGhostTrackFitType(vtxRecoPSet.getParameter<std::string>("fitType"))));
	// else
		// vertexReco.reset(
		// 	new ConfigurableVertexReconstructor(vtxRecoPSet));

	TransientTrackMap primariesMap;

	// result secondary vertices

	// std::auto_ptr<Product> tagInfos(new Product);
	std::vector<reco::CandSecondaryVertexTagInfo> tagInfos;

	for(std::vector<reco::CandIPTagInfo>::const_iterator iterJets =
		trackIPTagInfos.begin(); iterJets != trackIPTagInfos.end();
		++iterJets) {
		TrackDataVector trackData;
//		      std::cout << "Jet " << iterJets-trackIPTagInfos.begin() << std::endl;

		const Vertex &pv = *iterJets->primaryVertex();

		std::set<TransientTrack> primaries;
		// if (constraint == CONSTRAINT_PV_PRIMARIES_IN_FIT) {
		// 	for(Vertex::trackRef_iterator iter = pv.tracks_begin();
		// 	    iter != pv.tracks_end(); ++iter) {
		// 		TransientTrackMap::iterator pos =
		// 			primariesMap.lower_bound(iter->get());
		//
		// 		if (pos != primariesMap.end() &&
		// 		    pos->first == iter->get())
		// 			primaries.insert(pos->second);
		// 		else {
		// 			TransientTrack track =
		// 				trackBuilder->build(
		// 					iter->castTo<TrackRef>());
		// 			primariesMap.insert(pos,
		// 				std::make_pair(iter->get(), track));
		// 			primaries.insert(track);
		// 		}
		// 	}
		// }

		edm::RefToBase<Jet> jetRef = iterJets->jet();

		GlobalVector jetDir(jetRef->momentum().x(),
		                    jetRef->momentum().y(),
		                    jetRef->momentum().z());

		std::vector<std::size_t> indices =
				iterJets->sortedIndexes(m_sortCriterium);

		const std::vector<reco::CandidatePtr> trackRefs = iterJets->sortedTracks(indices); // was input_container

		const std::vector<reco::btag::TrackIPData> &ipData =
					iterJets->impactParameterData();

		// build transient tracks used for vertex reconstruction

		// std::vector<TransientTrack> fitTracks;
		// std::vector<GhostTrackState> gtStates;
		// std::auto_ptr<GhostTrackPrediction> gtPred;
		// if (useGhostTrack)
		// 	gtPred.reset(new GhostTrackPrediction(
		// 				*iterJets->ghostTrack()));

		for(unsigned int i = 0; i < indices.size(); i++) {
			typedef TemplatedSecondaryVertexTagInfo<CandIPTagInfo,reco::VertexCompositePtrCandidate>::IndexedTrackData IndexedTrackData;

			const input_item &trackRef = trackRefs[i];

			trackData.push_back(IndexedTrackData());
			trackData.back().first = indices[i];

			// select tracks for SV finder

			if (!((*m_trackSelector)(*reco::btag::toTrack(trackRef), ipData[indices[i]], *jetRef,
			                   RecoVertex::convertPos(
			                   		pv.position())))) {
				trackData.back().second.svStatus =
					  TemplatedSecondaryVertexTagInfo<CandIPTagInfo,reco::VertexCompositePtrCandidate>::TrackData::trackSelected;
				continue;
			}

			TransientTrackMap::const_iterator pos =
					primariesMap.find(reco::btag::toTrack((trackRef)));
			TransientTrack fitTrack;
			if (pos != primariesMap.end()) {
				primaries.erase(pos->second);
				fitTrack = pos->second;
			} else
				fitTrack = getTransientTrack(trackRef); // trackBuilder->build(trackRef);
			// fitTracks.push_back(fitTrack);

			trackData.back().second.svStatus =
				  TemplatedSecondaryVertexTagInfo<CandIPTagInfo,reco::VertexCompositePtrCandidate>::TrackData::trackUsedForVertexFit;

			// if (useGhostTrack) {
			// 	GhostTrackState gtState(fitTrack);
			// 	GlobalPoint pos =
			// 		ipData[indices[i]].closestToGhostTrack;
			// 	gtState.linearize(*gtPred, true,
			// 	                  gtPred->lambda(pos));
			// 	gtState.setWeight(ipData[indices[i]].ghostTrackWeight);
			// 	gtStates.push_back(gtState);
			// }
		}

		// std::auto_ptr<GhostTrack> ghostTrack;
		// if (useGhostTrack)
		// 	ghostTrack.reset(new GhostTrack(
		// 		GhostTrackPrediction(
		// 			RecoVertex::convertPos(pv.position()),
		// 			RecoVertex::convertError(pv.error()),
		// 			GlobalVector(
		// 				iterJets->ghostTrack()->px(),
		// 				iterJets->ghostTrack()->py(),
		// 				iterJets->ghostTrack()->pz()),
		// 			0.05),
		// 		*gtPred, gtStates,
		// 		iterJets->ghostTrack()->chi2(),
		// 		iterJets->ghostTrack()->ndof()));

		// perform actual vertex finding


	 	std::vector<reco::VertexCompositePtrCandidate>       extAssoCollection;
		// std::vector<TransientVertex> fittedSVs;
		std::vector<SecondaryVertex> SVs;
		// if(!useExternalSV){
    	// 	  switch(constraint)   {
		//     case CONSTRAINT_NONE:
		// 	if (useGhostTrack)
		// 		fittedSVs = vertexRecoGT->vertices(
		// 				pv, *ghostTrack);
		// 	else
		// 		fittedSVs = vertexReco->vertices(fitTracks);
		// 	break;
		//
		//     case CONSTRAINT_BEAMSPOT:
		// 	if (useGhostTrack)
		// 		fittedSVs = vertexRecoGT->vertices(
		// 				pv, *beamSpot, *ghostTrack);
		// 	else
		// 		fittedSVs = vertexReco->vertices(fitTracks,
		// 		                                 *beamSpot);
		// 	break;
		//
		//     case CONSTRAINT_PV_BEAMSPOT_SIZE:
		//     case CONSTRAINT_PV_BS_Z_ERRORS_SCALED:
		//     case CONSTRAINT_PV_ERROR_SCALED: {
		// 	BeamSpot::CovarianceMatrix cov;
		// 	for(unsigned int i = 0; i < 7; i++) {
		// 		unsigned int covSrc = bsCovSrc[i];
		// 		for(unsigned int j = 0; j < 7; j++) {
		// 			double v=0.0;
		// 			if (!covSrc || bsCovSrc[j] != covSrc)
		// 				v = 0.0;
		// 			else if (covSrc == 1)
		// 				v = beamSpot->covariance(i, j);
		// 			else if (j<3 && i<3)
		// 				v = pv.covariance(i, j) *
		// 				    constraintScaling;
		// 			cov(i, j) = v;
		// 		}
		// 	}
		//
		// 	BeamSpot bs(pv.position(), sigmaZ,
		// 	            beamSpot.isValid() ? beamSpot->dxdz() : 0.,
		// 	            beamSpot.isValid() ? beamSpot->dydz() : 0.,
		// 	            beamWidth, cov, BeamSpot::Unknown);
		//
		// 	if (useGhostTrack)
		// 		fittedSVs = vertexRecoGT->vertices(
		// 				pv, bs, *ghostTrack);
		// 	else
		// 		fittedSVs = vertexReco->vertices(fitTracks, bs);
		//     }	break;
		//
		//     case CONSTRAINT_PV_PRIMARIES_IN_FIT: {
		// 	std::vector<TransientTrack> primaries_(
		// 			primaries.begin(), primaries.end());
		// 	if (useGhostTrack)
		// 		fittedSVs = vertexRecoGT->vertices(
		// 				pv, *beamSpot, primaries_,
		// 				*ghostTrack);
		// 	else
		// 		fittedSVs = vertexReco->vertices(
		// 				primaries_, fitTracks,
		// 				*beamSpot);
		//     }	break;
		//   }
		//   // build combined SV information and filter
		//   SVBuilder svBuilder(pv, jetDir, withPVError, minTrackWeight);
		//   std::remove_copy_if(boost::make_transform_iterator(
		// 			  fittedSVs.begin(), svBuilder),
		// 		      boost::make_transform_iterator(
		// 			  fittedSVs.end(), svBuilder),
		// 		      std::back_inserter(SVs),
		// 		      SVFilter(vertexFilter, pv, jetDir));
		//
		// }else{
		//   if( useSVClustering || useFatJets ) {
		//       size_t jetIdx = ( iterJets - trackIPTagInfos.begin() );
		  //
		//       for(size_t iExtSv = 0; iExtSv < clusteredSVs.at(jetIdx).size(); iExtSv++){
		// 	 const reco::VertexCompositePtrCandidate & extVertex = (*extSecVertex)[ clusteredSVs.at(jetIdx).at(iExtSv) ];
		// 	 if( extVertex.p4().M() < 0.3 )
		// 	   continue;
		// 	 extAssoCollection.push_back( extVertex );
		//       }
		//   }
		//   else {
		      for(size_t iExtSv = 0; iExtSv < extSecVertex.size(); iExtSv++){
			 const reco::VertexCompositePtrCandidate & extVertex = (extSecVertex)[iExtSv];
			 if( Geom::deltaR2( ( position(extVertex) - pv.position() ), jetDir ) > m_extSVDeltaRToJet*m_extSVDeltaRToJet || extVertex.p4().M() < 0.3 )
			   continue;
			 extAssoCollection.push_back( extVertex );
		      }
		//   }
		  // build combined SV information and filter
		  SVBuilder svBuilder(pv, jetDir, m_withPVError, m_minTrackWeight);
		  std::remove_copy_if(boost::make_transform_iterator( extAssoCollection.begin(), svBuilder),
				    boost::make_transform_iterator(extAssoCollection.end(), svBuilder),
				    std::back_inserter(SVs),
				    SVFilter(*m_vertexFilter, pv, jetDir));
                // }
		// clean up now unneeded collections
		// gtPred.reset();
		// ghostTrack.reset();
		// gtStates.clear();
		// fitTracks.clear();
		// fittedSVs.clear();
		extAssoCollection.clear();

		// sort SVs by importance

		std::vector<unsigned int> vtxIndices = ((*m_vertexSorting)(SVs));

		std::vector<TemplatedSecondaryVertexTagInfo<CandIPTagInfo,reco::VertexCompositePtrCandidate>::VertexData> svData;

		svData.resize(vtxIndices.size());
		for(unsigned int idx = 0; idx < vtxIndices.size(); idx++) {
			const SecondaryVertex &sv = SVs[vtxIndices[idx]];

			svData[idx].vertex = sv;
			svData[idx].dist2d = sv.dist2d();
			svData[idx].dist3d = sv.dist3d();
			svData[idx].direction = flightDirection(pv,sv);
			// mark tracks successfully used in vertex fit
			markUsedTracks(trackData,trackRefs,sv,idx);
		}

		// fill result into tag infos

		// tagInfos->push_back(
		// 	TemplatedSecondaryVertexTagInfo<CandIPTagInfo,reco::VertexCompositePtrCandidate>(
		// 		trackData, svData, SVs.size(),
		// 		edm::Ref<std::vector<CandIPTagInfo> >(trackIPTagInfos,
		// 			iterJets - trackIPTagInfos.begin())));
		// edm::Ref<std::vector<CandIPTagInfo> > jetTagRef = edm::Ref<std::vector<CandIPTagInfo> >(&trackIPTagInfos,
		// 	iterJets - trackIPTagInfos.begin());
		// reco::CandSecondaryVertexTagInfo tagInfo = reco::CandSecondaryVertexTagInfo(
		// 	trackData, svData, SVs.size(),
		// 	jetTagRef);

		tagInfos.push_back(
			reco::CandSecondaryVertexTagInfo(
				trackData, svData, SVs.size(),
				edm::Ref<std::vector<CandIPTagInfo> >(&trackIPTagInfos,
					iterJets - trackIPTagInfos.begin())));
	}

	// event.put(tagInfos);
	return tagInfos;
}

//Need specialized template because reco::Vertex iterators are TrackBase and it is a mess to make general
// void  SecondaryVertexProducerLight::markUsedTracks(TrackDataVector & trackData, const std::vector<reco::CandidatePtr> & trackRefs, const SecondaryVertex & sv,size_t idx)
// {
// 	for(Vertex::trackRef_iterator iter = sv.tracks_begin();	iter != sv.tracks_end(); ++iter) {
// 		if (sv.trackWeight(*iter) < minTrackWeight)
// 			continue;
//
// 		std::vector<reco::CandidatePtr>::const_iterator pos =
// 			std::find(trackRefs.begin(), trackRefs.end(),
// 					iter->castTo<input_item>());
//
// 		if (pos == trackRefs.end() ) {
// 			if(!useExternalSV)
// 				throw cms::Exception("TrackNotFound")
// 					<< "Could not find track from secondary "
// 					"vertex in original tracks."
// 					<< std::endl;
// 		} else {
// 			unsigned int index = pos - trackRefs.begin();
// 			trackData[index].second.svStatus =
// 				(btag::TrackData::Status)
// 				((unsigned int)btag::TrackData::trackAssociatedToVertex + idx);
// 		}
// 	}
// }


void  SecondaryVertexProducerLight::markUsedTracks(TrackDataVector & trackData, const std::vector<reco::CandidatePtr> & trackRefs, const reco::VertexCompositePtrCandidate & sv,size_t idx)
{
	for(std::vector<reco::CandidatePtr>::const_iterator iter = sv.daughterPtrVector().begin(); iter != sv.daughterPtrVector().end(); ++iter)
	{
		std::vector<reco::CandidatePtr>::const_iterator pos =
			std::find(trackRefs.begin(), trackRefs.end(), *iter);

		if (pos != trackRefs.end() )
		{
			unsigned int index = pos - trackRefs.begin();
			trackData[index].second.svStatus =
				(btag::TrackData::Status)
				((unsigned int)btag::TrackData::trackAssociatedToVertex + idx);
		}
	}
}


SecondaryVertexProducerLight::SecondaryVertex
SecondaryVertexProducerLight::SVBuilder::operator () (const TransientVertex &sv) const
{
	if(sv.originalTracks().size()>0 && sv.originalTracks()[0].trackBaseRef().isNonnull())
		return SecondaryVertex(pv, sv, direction, m_withPVError_);
	else
	{
		edm::LogError("UnexpectedInputs") << "Building from Candidates, should not happen!";
		return SecondaryVertex(pv, sv, direction, m_withPVError_);
	}
}

// reco::SecondaryVertex
// SecondaryVertexProducerLight::SVBuilder::operator () (const TransientVertex &sv) const
// {
// 	if(sv.originalTracks().size()>0 && sv.originalTracks()[0].trackBaseRef().isNonnull())
// 	{
// 		edm::LogError("UnexpectedInputs") << "Building from Tracks, should not happen!";
// 		VertexCompositePtrCandidate vtxCompPtrCand;
//
// 		vtxCompPtrCand.setCovariance(sv.vertexState().error().matrix_new());
// 		vtxCompPtrCand.setChi2AndNdof(sv.totalChiSquared(), sv.degreesOfFreedom());
// 		vtxCompPtrCand.setVertex(Candidate::Point(sv.position().x(),sv.position().y(),sv.position().z()));
//
// 		return SecondaryVertex(pv, vtxCompPtrCand, direction, withPVError);
// 	}
// 	else
// 	{
// 		VertexCompositePtrCandidate vtxCompPtrCand;
//
// 		vtxCompPtrCand.setCovariance(sv.vertexState().error().matrix_new());
// 		vtxCompPtrCand.setChi2AndNdof(sv.totalChiSquared(), sv.degreesOfFreedom());
// 		vtxCompPtrCand.setVertex(Candidate::Point(sv.position().x(),sv.position().y(),sv.position().z()));
//
// 		Candidate::LorentzVector p4;
// 		for(std::vector<reco::TransientTrack>::const_iterator tt = sv.originalTracks().begin(); tt != sv.originalTracks().end(); ++tt)
// 		{
// 			if (sv.trackWeight(*tt) < minTrackWeight)
// 				continue;
//
// 			const CandidatePtrTransientTrack* cptt = dynamic_cast<const CandidatePtrTransientTrack*>(tt->basicTransientTrack());
// 			if ( cptt==0 )
// 				edm::LogError("DynamicCastingFailed") << "Casting of TransientTrack to CandidatePtrTransientTrack failed!";
// 			else
// 			{
// 				p4 += cptt->candidate()->p4();
// 				vtxCompPtrCand.addDaughter(cptt->candidate());
// 			}
// 		}
// 		vtxCompPtrCand.setP4(p4);
//
// 		return SecondaryVertex(pv, vtxCompPtrCand, direction, withPVError);
// 	}
// }

// ------------ method that matches reclustered and original jets based on minimum dR ------------
// template<class CandIPTagInfo,class reco::VertexCompositePtrCandidate>
// template<class CONTAINER>
// void SecondaryVertexProducerLight::matchReclusteredJets(const std::vector<pat::Jet>& jets,
//                                                                       const std::vector<fastjet::PseudoJet>& reclusteredJets,
//                                                                       std::vector<int>& matchedIndices,
//                                                                       const std::string& jetType)
// {
//    std::string type = ( jetType!="" ? jetType + " " : jetType );
//
//    std::vector<bool> matchedLocks(reclusteredJets.size(),false);
//
//    for(size_t j=0; j<jets.size(); ++j)
//    {
//      double matchedDR2 = 1e9;
//      int matchedIdx = -1;
//
//      for(size_t rj=0; rj<reclusteredJets.size(); ++rj)
//      {
//        if( matchedLocks.at(rj) ) continue; // skip jets that have already been matched
//
//        double tempDR2 = Geom::deltaR2( toJet(jets.at(j))->rapidity(), toJet(jets.at(j))->phi(), reclusteredJets.at(rj).rapidity(), reclusteredJets.at(rj).phi_std() );
//        if( tempDR2 < matchedDR2 )
//        {
//          matchedDR2 = tempDR2;
//          matchedIdx = rj;
//        }
//      }
//
//      if( matchedIdx>=0 )
//      {
//        if ( matchedDR2 > rParam*rParam )
//        {
//          edm::LogError("JetMatchingFailed") << "Matched reclustered jet " << matchedIdx << " and original " << type << "jet " << j <<" are separated by dR=" << sqrt(matchedDR2) << " which is greater than the jet size R=" << rParam << ".\n"
//                                             << "This is not expected so please check that the jet algorithm and jet size match those used for the original " << type << "jet collection.";
//        }
//        else
//          matchedLocks.at(matchedIdx) = true;
//      }
//      else
//        edm::LogError("JetMatchingFailed") << "Matching reclustered to original " << type << "jets failed. Please check that the jet algorithm and jet size match those used for the original " << type << "jet collection.";
//
//      matchedIndices.push_back(matchedIdx);
//    }
// }

// ------------ method that matches groomed and original jets based on minimum dR ------------
// template<class CandIPTagInfo,class reco::VertexCompositePtrCandidate>
// void SecondaryVertexProducerLight<CandIPTagInfo,reco::VertexCompositePtrCandidate>::matchGroomedJets(const edm::Handle<edm::View<reco::Jet> >& jets,
//                                                                   const edm::Handle<edm::View<reco::Jet> >& groomedJets,
//                                                                   std::vector<int>& matchedIndices)
// {
//    std::vector<bool> jetLocks(jets.size(),false);
//    std::vector<int>  jetIndices;
//
//    for(size_t gj=0; gj<groomedJets->size(); ++gj)
//    {
//      double matchedDR2 = 1e9;
//      int matchedIdx = -1;
//
//      if( groomedJets->at(gj).pt()>0. ) // skip pathological cases of groomed jets with Pt=0
//      {
//        for(size_t j=0; j<jets.size(); ++j)
//        {
//          if( jetLocks.at(j) ) continue; // skip jets that have already been matched
//
//          double tempDR2 = Geom::deltaR2( jets.at(j).rapidity(), jets.at(j).phi(), groomedJets->at(gj).rapidity(), groomedJets->at(gj).phi() );
//          if( tempDR2 < matchedDR2 )
//          {
//            matchedDR2 = tempDR2;
//            matchedIdx = j;
//          }
//        }
//      }
//
//      if( matchedIdx>=0 )
//      {
//        if ( matchedDR2 > rParam*rParam )
//        {
//          edm::LogWarning("MatchedJetsFarApart") << "Matched groomed jet " << gj << " and original jet " << matchedIdx <<" are separated by dR=" << sqrt(matchedDR2) << " which is greater than the jet size R=" << rParam << ".\n"
//                                                 << "This is not expected so the matching of these two jets has been discarded. Please check that the two jet collections belong to each other.";
//          matchedIdx = -1;
//        }
//        else
//          jetLocks.at(matchedIdx) = true;
//      }
//      jetIndices.push_back(matchedIdx);
//    }
//
//    for(size_t j=0; j<jets.size(); ++j)
//    {
//      std::vector<int>::iterator matchedIndex = std::find( jetIndices.begin(), jetIndices.end(), j );
//
//      matchedIndices.push_back( matchedIndex != jetIndices.end() ? std::distance(jetIndices.begin(),matchedIndex) : -1 );
//    }
// }

// ------------ method that matches subjets and original fat jets ------------
// template<class CandIPTagInfo,class reco::VertexCompositePtrCandidate>
// void SecondaryVertexProducerLight<CandIPTagInfo,reco::VertexCompositePtrCandidate>::matchSubjets(const std::vector<int>& groomedIndices,
//                                                               const edm::Handle<edm::View<reco::Jet> >& groomedJets,
//                                                               const edm::Handle<std::vector<CandIPTagInfo> >& subjets,
//                                                               std::vector<std::vector<int> >& matchedIndices)
// {
//    for(size_t g=0; g<groomedIndices.size(); ++g)
//    {
//      std::vector<int> subjetIndices;
//
//      if( groomedIndices.at(g)>=0 )
//      {
//        for(size_t s=0; s<groomedJets->at(groomedIndices.at(g)).numberOfDaughters(); ++s)
//        {
//          const edm::Ptr<reco::Candidate> & subjet = groomedJets->at(groomedIndices.at(g)).daughterPtr(s);
//
//          for(size_t sj=0; sj<subjets.size(); ++sj)
//          {
//            const edm::RefToBase<reco::Jet> &subjetRef = subjets.at(sj).jet();
//            if( subjet == edm::Ptr<reco::Candidate>( subjetRef.id(), subjetRef.get(), subjetRef.key() ) )
//            {
//              subjetIndices.push_back(sj);
//              break;
//            }
//          }
//        }
//
//        if( subjetIndices.size() == 0 )
//          edm::LogError("SubjetMatchingFailed") << "Matching subjets to original fat jets failed. Please check that the groomed fat jet and subjet collections belong to each other.";
//
//        matchedIndices.push_back(subjetIndices);
//      }
//      else
//        matchedIndices.push_back(subjetIndices);
//    }
// }

// ------------ method that matches subjets and original fat jets ------------
// template<class CandIPTagInfo,class reco::VertexCompositePtrCandidate>
// void SecondaryVertexProducerLight<CandIPTagInfo,reco::VertexCompositePtrCandidate>::matchSubjets(const edm::Handle<edm::View<reco::Jet> >& fatJets,
//                                                               const edm::Handle<std::vector<CandIPTagInfo> >& subjets,
//                                                               std::vector<std::vector<int> >& matchedIndices)
// {
//    for(size_t fj=0; fj<fatJets->size(); ++fj)
//    {
//      std::vector<int> subjetIndices;
//      size_t nSubjetCollections = 0;
//      size_t nSubjets = 0;
//
//      const pat::Jet * fatJet = dynamic_cast<const pat::Jet *>( fatJets->ptrAt(fj).get() );
//
//      if( !fatJet )
//      {
//        if( fj==0 ) edm::LogError("WrongJetType") << "Wrong jet type for input fat jets. Please check that the input fat jets are of the pat::Jet type.";
//
//        matchedIndices.push_back(subjetIndices);
//        continue;
//      }
//      else
//      {
//        nSubjetCollections = fatJet->subjetCollectionNames().size();
//
//        if( nSubjetCollections>0 )
//        {
//          for(size_t coll=0; coll<nSubjetCollections; ++coll)
//          {
//            const pat::JetPtrCollection & fatJetSubjets = fatJet->subjets(coll);
//
//            for(size_t fjsj=0; fjsj<fatJetSubjets.size(); ++fjsj)
//            {
//              ++nSubjets;
//
//              for(size_t sj=0; sj<subjets.size(); ++sj)
//              {
//                const pat::Jet * subJet = dynamic_cast<const pat::Jet *>( subjets.at(sj).jet().get() );
//
//                if( !subJet )
//                {
//                  if( fj==0 && coll==0 && fjsj==0 && sj==0 ) edm::LogError("WrongJetType") << "Wrong jet type for input subjets. Please check that the input subjets are of the pat::Jet type.";
//
//                  break;
//                }
//                else
//                {
//                  if( subJet->originalObjectRef() == fatJetSubjets.at(fjsj)->originalObjectRef() )
//                  {
//                    subjetIndices.push_back(sj);
//                    break;
//                  }
//                }
//              }
//            }
//          }
//
//          if( subjetIndices.size() == 0 && nSubjets > 0)
//            edm::LogError("SubjetMatchingFailed") << "Matching subjets to fat jets failed. Please check that the fat jet and subjet collections belong to each other.";
//
//          matchedIndices.push_back(subjetIndices);
//        }
//        else
//          matchedIndices.push_back(subjetIndices);
//      }
//    }
// }

// ------------ method fills 'descriptions' with the allowed parameters for the module ------------
// template<class CandIPTagInfo,class reco::VertexCompositePtrCandidate>
// void SecondaryVertexProducerLight<CandIPTagInfo,reco::VertexCompositePtrCandidate>::fillDescriptions(edm::ConfigurationDescriptions & descriptions) {
//
//   edm::ParameterSetDescription desc;
//   desc.add<double>("extSVDeltaRToJet",0.3);
//   desc.add<edm::InputTag>("beamSpotTag",edm::InputTag("offlineBeamSpot"));
//   {
//     edm::ParameterSetDescription vertexReco;
//     vertexReco.add<double>("primcut",1.8);
//     vertexReco.add<double>("seccut",6.0);
//     vertexReco.add<std::string>("finder","avr");
//     vertexReco.addOptionalNode( edm::ParameterDescription<double>("minweight",0.5, true) and
//                                 edm::ParameterDescription<double>("weightthreshold",0.001, true) and
//                                 edm::ParameterDescription<bool>("smoothing",false, true), true );
//     vertexReco.addOptionalNode( edm::ParameterDescription<double>("maxFitChi2",10.0, true) and
//                                 edm::ParameterDescription<double>("mergeThreshold",3.0, true) and
//                                 edm::ParameterDescription<std::string>("fitType","RefitGhostTrackWithVertices", true), true );
//     desc.add<edm::ParameterSetDescription>("vertexReco",vertexReco);
//   }
//   {
//     edm::ParameterSetDescription vertexSelection;
//     vertexSelection.add<std::string>("sortCriterium","dist3dError");
//     desc.add<edm::ParameterSetDescription>("vertexSelection",vertexSelection);
//   }
//   desc.add<std::string>("constraint","BeamSpot");
//   desc.add<edm::InputTag>("trackIPTagInfos",edm::InputTag("impactParameterTagInfos"));
//   {
//     edm::ParameterSetDescription vertexCuts;
//     vertexCuts.add<double>("distSig3dMax",99999.9);
//     vertexCuts.add<double>("fracPV",0.65);
//     vertexCuts.add<double>("distVal2dMax",2.5);
//     vertexCuts.add<bool>("useTrackWeights",true);
//     vertexCuts.add<double>("maxDeltaRToJetAxis",0.4);
//     {
//       edm::ParameterSetDescription v0Filter;
//       v0Filter.add<double>("k0sMassWindow",0.05);
//       vertexCuts.add<edm::ParameterSetDescription>("v0Filter",v0Filter);
//     }
//     vertexCuts.add<double>("distSig2dMin",3.0);
//     vertexCuts.add<unsigned int>("multiplicityMin",2);
//     vertexCuts.add<double>("distVal2dMin",0.01);
//     vertexCuts.add<double>("distSig2dMax",99999.9);
//     vertexCuts.add<double>("distVal3dMax",99999.9);
//     vertexCuts.add<double>("minimumTrackWeight",0.5);
//     vertexCuts.add<double>("distVal3dMin",-99999.9);
//     vertexCuts.add<double>("massMax",6.5);
//     vertexCuts.add<double>("distSig3dMin",-99999.9);
//     desc.add<edm::ParameterSetDescription>("vertexCuts",vertexCuts);
//   }
//   desc.add<bool>("useExternalSV",false);
//   desc.add<double>("minimumTrackWeight",0.5);
//   desc.add<bool>("usePVError",true);
//   {
//     edm::ParameterSetDescription trackSelection;
//     trackSelection.add<double>("b_pT",0.3684);
//     trackSelection.add<double>("max_pT",500);
//     trackSelection.add<bool>("useVariableJTA",false);
//     trackSelection.add<double>("maxDecayLen",99999.9);
//     trackSelection.add<double>("sip3dValMin",-99999.9);
//     trackSelection.add<double>("max_pT_dRcut",0.1);
//     trackSelection.add<double>("a_pT",0.005263);
//     trackSelection.add<unsigned int>("totalHitsMin",8);
//     trackSelection.add<double>("jetDeltaRMax",0.3);
//     trackSelection.add<double>("a_dR",-0.001053);
//     trackSelection.add<double>("maxDistToAxis",0.2);
//     trackSelection.add<double>("ptMin",1.0);
//     trackSelection.add<std::string>("qualityClass","any");
//     trackSelection.add<unsigned int>("pixelHitsMin",2);
//     trackSelection.add<double>("sip2dValMax",99999.9);
//     trackSelection.add<double>("max_pT_trackPTcut",3);
//     trackSelection.add<double>("sip2dValMin",-99999.9);
//     trackSelection.add<double>("normChi2Max",99999.9);
//     trackSelection.add<double>("sip3dValMax",99999.9);
//     trackSelection.add<double>("sip3dSigMin",-99999.9);
//     trackSelection.add<double>("min_pT",120);
//     trackSelection.add<double>("min_pT_dRcut",0.5);
//     trackSelection.add<double>("sip2dSigMax",99999.9);
//     trackSelection.add<double>("sip3dSigMax",99999.9);
//     trackSelection.add<double>("sip2dSigMin",-99999.9);
//     trackSelection.add<double>("b_dR",0.6263);
//     desc.add<edm::ParameterSetDescription>("trackSelection",trackSelection);
//   }
//   desc.add<std::string>("trackSort","sip3dSig");
//   desc.add<edm::InputTag>("extSVCollection",edm::InputTag("secondaryVertices"));
//   desc.addOptionalNode( edm::ParameterDescription<bool>("useSVClustering",false, true) and
//                         edm::ParameterDescription<std::string>("jetAlgorithm", true) and
//                         edm::ParameterDescription<double>("rParam", true), true );
//   desc.addOptional<bool>("useSVMomentum",false);
//   desc.addOptional<double>("ghostRescaling",1e-18);
//   desc.addOptional<double>("relPtTolerance",1e-03);
//   desc.addOptional<edm::InputTag>("fatJets");
//   desc.addOptional<edm::InputTag>("groomedFatJets");
//   descriptions.addDefault(desc);
// }

//define this as a plug-in
// typedef SecondaryVertexProducerLight<TrackIPTagInfo,reco::Vertex> SecondaryVertexProducer;
// typedef SecondaryVertexProducerLight<CandIPTagInfo,reco::VertexCompositePtrCandidate> CandSecondaryVertexProducer;

// DEFINE_FWK_MODULE(SecondaryVertexProducer);
// DEFINE_FWK_MODULE(CandSecondaryVertexProducer);

reco::TransientTrack SecondaryVertexProducerLight::getTransientTrack(const reco::CandidatePtr& trackRef) const
{

        reco::TransientTrack transientTrack(trackRef, m_paramField);
        return transientTrack;

}

} //namespace cmg
