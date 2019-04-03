#include "CMGTools/VVResonances/interface/HEEPEleIDRecalculator.h"

using namespace cmg;
bool HEEPEleIDRecalculator::id(const pat::Electron& e) {
        if (fabs(e.superCluster()->eta()) < 1.4442)
                return e.ecalDriven() &&
                       fabs(e.deltaEtaSeedClusterTrackAtVtx()) < 0.004 &&
                       fabs( e.deltaPhiSuperClusterTrackAtVtx())< 0.06 &&
                       (e.hadronicOverEm()<1.0/e.superCluster()->energy()+0.05) &&
                       (e.e2x5Max()/e.e5x5() > 0.94 || e.e1x5()/e.e5x5() > 0.83) && fabs(e.dB()) < 0.02;

        if (fabs(e.superCluster()->eta()) > 1.566)
                return fabs(e.superCluster()->eta()) < 2.5 &&
                       e.ecalDriven() && fabs(e.deltaEtaSeedClusterTrackAtVtx()) < 0.006 &&
                       fabs(e.deltaPhiSuperClusterTrackAtVtx()) < 0.06 &&
                       (e.hadronicOverEm() < 5.0/e.superCluster()->energy()+0.05) &&
                       fabs(e.dB()) < 0.05 && e.full5x5_sigmaIetaIeta() < 0.03;

        return false;
}

bool HEEPEleIDRecalculator::iso(const pat::Electron& e,const double rho, const std::vector<pat::Electron>& eles,const pat::PackedCandidateCollection& cands,const pat::PackedCandidateCollection& lostTracks) {
        float trackIso = 0.0;
        trackIso+=calIsol(e.gsfTrack()->eta(),e.gsfTrack()->phi(),e.gsfTrack()->vz(),cands,eles).second;
        trackIso+=calIsol(e.gsfTrack()->eta(),e.gsfTrack()->phi(),e.gsfTrack()->vz(),lostTracks,eles).second;
        if (trackIso>=5.0)
                return false;

        float neutralIso = e.dr03EcalRecHitSumEt()+e.dr03HcalDepth1TowerSumEt();
        if (fabs(e.superCluster()->eta()) < 1.4442)
                return neutralIso<2.0+0.03*e.et()+0.28*rho;

        if (fabs(e.superCluster()->eta()) > 1.566) {
                if (e.et()<50.0)
                        return neutralIso<2.5+0.28*rho;
                else
                        return neutralIso<2.5+0.03*(e.et()-50.0)+0.28*rho;

        }

        return false;
}

bool HEEPEleIDRecalculator::passQual(const reco::TrackBase& trk,
                                     const std::vector<reco::TrackBase::TrackQuality>& quals)
{
        if(quals.empty()) return true;

        for(auto qual : quals) {
                if(trk.quality(qual)) return true;
        }

        return false;
}

bool HEEPEleIDRecalculator::
passAlgo(const reco::TrackBase& trk,
         const std::vector<reco::TrackBase::TrackAlgorithm>& algosToRej)
{
        return algosToRej.empty() || !std::binary_search(algosToRej.begin(),algosToRej.end(),trk.algo());
}

//so the working theory here is that the track we have is the electrons gsf track
//if so, lets get the pt of the gsf track before E/p combinations
//if no match found to a gsf ele with a gsftrack, return the pt of the input track
double HEEPEleIDRecalculator::
getTrkPt(const reco::TrackBase& trk,
         const std::vector<pat::Electron>& eles)
{
        //note, the trk.eta(),trk.phi() should be identical to the gsf track eta,phi
        //although this may not be the case due to roundings after packing
        auto match=[](const reco::TrackBase& trk,const pat::Electron& ele){
                            return std::abs(trk.eta()-ele.gsfTrack()->eta())<0.001 &&
                                   reco::deltaPhi(trk.phi(),ele.gsfTrack()->phi())<0.001;// &&
                    };
        for(auto& ele : eles) {
                if(ele.gsfTrack().isNonnull()) {
                        if(match(trk,ele)) {
                                return ele.gsfTrack()->pt();
                        }
                }
        }
        return trk.pt();
}




std::pair<int,double>
HEEPEleIDRecalculator::calIsol(const double eleEta,const double elePhi,
                               const double eleVZ,
                               const pat::PackedCandidateCollection& cands,
                               const std::vector<pat::Electron>& eles)
{

        double ptSum=0.;
        int nrTrks=0;

        const TrkCuts& cuts = std::abs(eleEta)<1.5 ? barrelCuts_ : endcapCuts_;

        for(auto& cand  : cands) {
	  if (cand.vertexRef().isNonnull())
                if(cand.charge()!=0 && cand.hasTrackDetails()) {
                        const reco::Track& trk = cand.pseudoTrack();
                        double trkPt = std::abs(cand.pdgId())!=11 ? trk.pt() : getTrkPt(trk,eles);
                        if(passTrkSel(trk,trkPt,cuts,eleEta,elePhi,eleVZ)) {
                                ptSum+=trkPt;
                                nrTrks++;
                        }
                }
        }
        return {nrTrks,ptSum};
}

bool HEEPEleIDRecalculator::passTrkSel(const reco::Track& trk,
                                       const double trkPt,const TrkCuts& cuts,
                                       const double eleEta,const double elePhi,
                                       const double eleVZ)
{
        const float dR2 = reco::deltaR2(eleEta,elePhi,trk.eta(),trk.phi());
        const float dEta = trk.eta()-eleEta;
        const float dZ = eleVZ - trk.vz();

        return dR2>=cuts.minDR2 && dR2<=cuts.maxDR2 &&
               std::abs(dEta)>=cuts.minDEta &&
               std::abs(dZ)<cuts.maxDZ &&
               trk.hitPattern().numberOfValidHits() >= cuts.minHits &&
               trk.hitPattern().numberOfValidPixelHits() >=cuts.minPixelHits &&
               (trk.ptError()/trkPt < cuts.maxDPtPt || cuts.maxDPtPt<0) &&
               passQual(trk,cuts.allowedQualities) &&
               passAlgo(trk,cuts.algosToReject) &&
               trkPt > cuts.minPt;
}
