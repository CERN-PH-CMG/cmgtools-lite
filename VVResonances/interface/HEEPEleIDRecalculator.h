#ifndef CMGTools_VVresonances_HEEPEleIdRecalculator_h
#define CMGTools_VVresonances_HEEPEleIdRecalculator_h


#include "DataFormats/TrackReco/interface/TrackBase.h"
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/EgammaCandidates/interface/GsfElectron.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/GsfTrackReco/interface/GsfTrack.h"


namespace cmg {
class HEEPEleIDRecalculator {
 private:
  struct TrkCuts {
    float minPt;
    float minDR2;
    float maxDR2;
    float minDEta;
    float maxDZ;
    float minHits;
    float minPixelHits;
    float maxDPtPt;
    std::vector<reco::TrackBase::TrackQuality> allowedQualities;
    std::vector<reco::TrackBase::TrackAlgorithm> algosToReject;
  };  



 public:
  HEEPEleIDRecalculator() {
    std::vector<std::string> empty;
    setIsoCuts(true,1.0,0.0,0.3,0.005,0.5,8,1,0.1,empty,empty);
    setIsoCuts(false,1.0,0.0,0.3,0.005,0.5,8,1,0.1,empty,empty);
  }

  ~HEEPEleIDRecalculator() {


  }

  bool id(const pat::Electron& e);
  bool iso(const pat::Electron& e,const double rho, const std::vector<pat::Electron>& eles,const pat::PackedCandidateCollection& cands,const pat::PackedCandidateCollection& lostTracks);

  void setIsoCuts(bool barrel,const double minPt,const double minDR,const double maxDR,const double minDEta,const double maxDZ,const int minHits,const int minPixelHits,const double maxDPtPt,const std::vector<std::string >& qualNames,const std::vector<std::string >& algoNames) {
    auto sq = [](double val){return val*val;};
    

    TrkCuts cuts;
    cuts.minDR2 = sq(minDR);
    cuts.maxDR2 = sq(maxDR);
    cuts.minDEta = minDEta;
    cuts.maxDZ = maxDZ;
    cuts.minHits = minHits;
    cuts.minPixelHits = minPixelHits;
    cuts.maxDPtPt = maxDPtPt;
    
    for(auto& qualName : qualNames){
      cuts.allowedQualities.push_back(reco::TrackBase::qualityByName(qualName));
    }
    for(auto& algoName : algoNames){
      cuts.algosToReject.push_back(reco::TrackBase::algoByName(algoName));
    }
    std::sort(cuts.algosToReject.begin(),cuts.algosToReject.end());
    if (barrel)
      barrelCuts_ = cuts;
    else
      endcapCuts_ = cuts;
  }


	       


 private:
  TrkCuts barrelCuts_,endcapCuts_;

  static bool passTrkSel(const reco::Track& trk,
			 const double trkPt,
			 const TrkCuts& cuts,
			 const double eleEta,const double elePhi,
			 const double eleVZ);

  static bool passQual(const reco::TrackBase& trk,
		       const std::vector<reco::TrackBase::TrackQuality>& quals);

  static bool passAlgo(const reco::TrackBase& trk,
		       const std::vector<reco::TrackBase::TrackAlgorithm>& algosToRej);

  double getTrkPt(const reco::TrackBase& trk,
		  const std::vector<pat::Electron>& eles);



  std::pair<int,double> calIsol(const double eleEta,const double elePhi,const double eleVZ,
				const pat::PackedCandidateCollection& cands,
				const std::vector<pat::Electron>& eles);


};
}
#endif
