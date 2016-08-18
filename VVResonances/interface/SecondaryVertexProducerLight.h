#ifndef CMGTools_VVResonances_SecondaryVertexProducerLight
#define CMGTools_VVResonances_SecondaryVertexProducerLight

#include <functional>
#include <algorithm>
#include <iterator>
#include <cstddef>
#include <string>
#include <vector>
#include <map>
#include <set>

#include <boost/iterator/transform_iterator.hpp>

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

#include "MagneticField/ParametrizedEngine/src/OAEParametrizedMagneticField.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"


#include "fastjet/JetDefinition.hh"
#include "fastjet/ClusterSequence.hh"
#include "fastjet/PseudoJet.hh"

//
// constants, enums and typedefs
//
typedef boost::shared_ptr<fastjet::ClusterSequence>  ClusterSequencePtr;
typedef boost::shared_ptr<fastjet::JetDefinition>    JetDefPtr;


namespace cmg {

	class VertexInfo : public fastjet::PseudoJet::UserInfoBase{
	  public:
	    VertexInfo(const int vertexIndex) :
	      m_vertexIndex(vertexIndex) { }

	    inline const int vertexIndex() const { return m_vertexIndex; }

	  protected:
	    int m_vertexIndex;
	};

	template<typename T>
	struct RefToBaseLess : public std::binary_function<edm::RefToBase<T>,
							   edm::RefToBase<T>,
							   bool> {
		inline bool operator()(const edm::RefToBase<T> &r1,
				       const edm::RefToBase<T> &r2) const
		{
			return r1.id() < r2.id() ||
			       (r1.id() == r2.id() && r1.key() < r2.key());
		}
	};


    class SecondaryVertexProducerLight {
        public:
    	explicit SecondaryVertexProducerLight(
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
		/*const edm::ParameterSet &params*/);
    	~SecondaryVertexProducerLight();
    	// static void fillDescriptions(edm::ConfigurationDescriptions & descriptions);
    	// typedef std::vector<TemplatedSecondaryVertexTagInfo<CandIPTagInfo,reco::VertexCompositePtrCandidate> > Product;
    	typedef reco::TemplatedSecondaryVertex<reco::VertexCompositePtrCandidate> SecondaryVertex;
    	typedef typename reco::CandIPTagInfo::input_container input_container;
    	typedef typename reco::CandIPTagInfo::input_container::value_type input_item;
    	typedef typename std::vector<reco::btag::IndexedTrackData> TrackDataVector;
    	std::vector<reco::CandSecondaryVertexTagInfo> produce(const std::vector<pat::Jet>& jets, const std::vector<reco::CandIPTagInfo> trackIPTagInfos,
			const std::vector<pat::PackedCandidate> &cands, const std::vector<reco::VertexCompositePtrCandidate> &extSecVertex,
			const reco::BeamSpot& beamSpot); //override
		reco::TransientTrack getTransientTrack(const reco::CandidatePtr& trackRef) const;

        private:
            // template<class CONTAINER>
    	// void matchReclusteredJets(const std::vector<pat::Jet>& jets,
    	// 			  const std::vector<fastjet::PseudoJet>& matchedJets,
    	// 			  std::vector<int>& matchedIndices,
    	// 			  const std::string& jetType="");
    	// void matchGroomedJets(const edm::Handle<edm::View<reco::Jet> >& jets,
    	// 		      const edm::Handle<edm::View<reco::Jet> >& matchedJets,
    	// 		      std::vector<int>& matchedIndices);
    	// void matchSubjets(const std::vector<int>& groomedIndices,
    	// 		  const edm::Handle<edm::View<reco::Jet> >& groomedJets,
    	// 		  const edm::Handle<std::vector<CandIPTagInfo> >& subjets,
    	// 		  std::vector<std::vector<int> >& matchedIndices);
    	// void matchSubjets(const edm::Handle<edm::View<reco::Jet> >& fatJets,
    	// 		  const edm::Handle<std::vector<CandIPTagInfo> >& subjets,
    	// 		  std::vector<std::vector<int> >& matchedIndices);

    	// const reco::Jet * toJet(const reco::Jet & j) { return &j; }
    	// const reco::Jet * toJet(const reco::CandIPTagInfo & j) { return &(*(j.jet())); }

		OAEParametrizedMagneticField *m_paramField;

    	// enum ConstraintType {
    	// 	CONSTRAINT_NONE	= 0,
    	// 	CONSTRAINT_BEAMSPOT,
    	// 	CONSTRAINT_PV_BEAMSPOT_SIZE,
    	// 	CONSTRAINT_PV_BS_Z_ERRORS_SCALED,
    	// 	CONSTRAINT_PV_ERROR_SCALED,
    	// 	CONSTRAINT_PV_PRIMARIES_IN_FIT
    	// };
    	// static ConstraintType getConstraintType(const std::string &name);

            // edm::EDGetTokenT<reco::BeamSpot> token_BeamSpot;
            // edm::EDGetTokenT<std::vector<CandIPTagInfo> > token_trackIPTagInfo;
    	reco::btag::SortCriteria	m_sortCriterium;
    	reco::TrackSelector			*m_trackSelector;
    	// ConstraintType			constraint;
    	// double				constraintScaling;
    	// edm::ParameterSet		vtxRecoPSet;
    	// bool				useGhostTrack;
    	bool				m_withPVError;
    	double				m_minTrackWeight;
    	reco::VertexFilter			*m_vertexFilter;
    	reco::VertexSorting<SecondaryVertex>	*m_vertexSorting;
            // bool                            useExternalSV;
            double                          m_extSVDeltaRToJet;
            // edm::EDGetTokenT<edm::View<reco::VertexCompositePtrCandidate> > token_extSVCollection;
    	// bool				useSVClustering;
    	// bool				useSVMomentum;
    	// std::string			jetAlgorithm;
    	// double				rParam;
    	// double				jetPtMin;
    	// double				ghostRescaling;
    	// double				relPtTolerance;
    	// bool				useFatJets;
    	// bool				useGroomedFatJets;
    	// edm::EDGetTokenT<edm::View<reco::Jet> > token_fatJets;
    	// edm::EDGetTokenT<edm::View<reco::Jet> > token_groomedFatJets;

    	// ClusterSequencePtr		fjClusterSeq;
    	// JetDefPtr			fjJetDefinition;

    	void markUsedTracks(TrackDataVector & trackData, const std::vector<reco::CandidatePtr> & trackRefs, const reco::VertexCompositePtrCandidate & sv,size_t idx);

    	struct SVBuilder :
    		public std::unary_function<const reco::VertexCompositePtrCandidate&, SecondaryVertex> {

    		SVBuilder(const reco::Vertex &pv,
    		          const GlobalVector &direction,
    		          const bool withPVError,
    			  double minTrackWeight) :
    			pv(pv), direction(direction),
    			m_withPVError_(withPVError),
    			m_minTrackWeight_(minTrackWeight) {}
    		SecondaryVertex operator () (const TransientVertex &sv) const;

    		SecondaryVertex operator () ( const reco::VertexCompositePtrCandidate &sv) const
    		{ return SecondaryVertex(pv, sv, direction, m_withPVError_); }


    		const reco::Vertex		&pv;
    		const GlobalVector	&direction;
    		bool			m_withPVError_;
    		double 			m_minTrackWeight_;
    	};

    	struct SVFilter :
    		public std::unary_function<const SecondaryVertex&, bool> {

    		SVFilter(const reco::VertexFilter &filter, const reco::Vertex &pv,
    		         const GlobalVector &direction) :
    			filter(filter), pv(pv), direction(direction) {}

    		inline bool operator () (const SecondaryVertex &sv) const
    		{ return !filter(pv, sv, direction); }

    		const reco::VertexFilter	&filter;
    		const reco::Vertex		&pv;
    		const GlobalVector	&direction;
    	};
    };


} // end namespace cmg

#endif
