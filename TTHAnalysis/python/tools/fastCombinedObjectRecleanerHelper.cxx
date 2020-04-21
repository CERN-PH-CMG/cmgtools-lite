#include <cmath>
#include <vector>
#include <algorithm>
#include <iostream>
#include <TTreeReaderValue.h>
#include <TTreeReaderArray.h>
#include <DataFormats/Math/interface/deltaR.h>
#include <CMGTools/TTHAnalysis/interface/CollectionSkimmer.h>
#include "CMGTools/TTHAnalysis/interface/CombinedObjectTags.h"
#include "DataFormats/Math/interface/LorentzVector.h"

struct JetSumCalculatorOutput {
  int thr;
  float htJetj;
  float mhtJet;
  int nBJetLoose;
  int nBJetMedium; 
  int nJet;
  int nFwdJet;
  float fwd1_pt;
  float fwd1_eta;
};

class fastCombinedObjectRecleanerHelper {
public:
  typedef TTreeReaderValue<unsigned>   ruint;
  typedef TTreeReaderValue<int>   rint;
  typedef TTreeReaderArray<float> rfloats;
  typedef TTreeReaderArray<int> rints;
  class rcount {
      public:
          rcount() : signed_(NULL), unsigned_(NULL) {}
          rcount(rint *src) : signed_(src), unsigned_(NULL) {}
          rcount(ruint *src) : signed_(NULL), unsigned_(src) {}
          rcount & operator=(rint *src) { signed_ = src; return *this; }  
          rcount & operator=(ruint *src) { unsigned_ = src; return *this; }  
          int operator*() const { return signed_ ? **signed_ : int(**unsigned_); }
      private:
          rint * signed_;
          ruint * unsigned_;
  };
  
  fastCombinedObjectRecleanerHelper(CollectionSkimmer &clean_taus, CollectionSkimmer &clean_jets, bool cleanJetsWithFOTaus, float bTagL, float bTagM, bool cleanWithRef=false) : clean_taus_(clean_taus), clean_jets_(clean_jets), deltaR2cut(0.16), cleanJetsWithFOTaus_(cleanJetsWithFOTaus), bTagL_(bTagL), bTagM_(bTagM), cleanWithRef_(cleanWithRef), deltaR2cut_taus(0.09) {
    _ct.reset(new std::vector<int>);
    _cj.reset(new std::vector<int>);
}
  
  void setLeptons(rint *nLep, rfloats* lepPt, rfloats *lepEta, rfloats *lepPhi) {
    nLep_ = nLep; Lep_pt_ = lepPt; Lep_eta_ = lepEta; Lep_phi_ = lepPhi;
    if (!nLep || !lepPt || !lepEta || !lepPhi) { std::cout << "ERROR: fastCombinedObjectRecleanerHelper initialized setLeptons with a null reader" << std::endl; }
  }
  void setLeptons(ruint *nLep, rfloats* lepPt, rfloats *lepEta, rfloats *lepPhi, rints *lepJet) {
    nLep_ = nLep; Lep_pt_ = lepPt; Lep_eta_ = lepEta; Lep_phi_ = lepPhi; Lep_jet_ = lepJet;
    if (!nLep || !lepPt || !lepEta || !lepPhi || !lepJet) { std::cout << "ERROR: fastCombinedObjectRecleanerHelper initialized setLeptons with a null reader" << std::endl; }
  }
  void setTaus(rint *nTau, rfloats *tauPt, rfloats *tauEta, rfloats *tauPhi) {
    nTau_ = nTau; Tau_pt_ = tauPt; Tau_eta_ = tauEta; Tau_phi_ = tauPhi;
    if (!nTau || !tauPt || !tauEta || !tauPhi) { std::cout << "ERROR: fastCombinedObjectRecleanerHelper initialized setTaus with a null reader" << std::endl; }
  }
  void setTaus(ruint *nTau, rfloats *tauPt, rfloats *tauEta, rfloats *tauPhi, rints *tauJet) {
    nTau_ = nTau; Tau_pt_ = tauPt; Tau_eta_ = tauEta; Tau_phi_ = tauPhi; Tau_jet_ = tauJet;
    if (!nTau || !tauPt || !tauEta || !tauPhi || !tauJet) { std::cout << "ERROR: fastCombinedObjectRecleanerHelper initialized setTaus with a null reader" << std::endl; }
  }
  void setJets(ruint *nJet, rfloats *jetPt, rfloats *jetEta, rfloats *jetPhi, rfloats *jetbtagCSV, vector<rfloats*> jetpt) {
    nJet_ = nJet; Jet_pt_ = jetPt; Jet_eta_ = jetEta; Jet_phi_ = jetPhi; Jet_btagCSV_ = jetbtagCSV; 
    Jet_corr_   = jetpt;
  }

  void addJetPt(int pt){
    _jetptcuts.insert(pt);
  }
  void setFwdPt(float fwdJetPt1, float fwdJetPt2){
    fwdJetPt1_= fwdJetPt1;
    fwdJetPt2_= fwdJetPt2;
  }


  typedef math::PtEtaPhiMLorentzVectorD ptvec;
  typedef math::XYZTLorentzVectorD crvec;

  std::vector<JetSumCalculatorOutput> GetJetSums(int variation = 0){

    std::vector<JetSumCalculatorOutput> output;
    
    crvec _mht(0,0,0,0);
    
    for (int i=0; i<*nLep_; i++) {
      if (!sel_leps[i]) continue;
      crvec lep(ptvec((*Lep_pt_)[i],0,(*Lep_phi_)[i],0));
      _mht = _mht - lep;
    }
    if (cleanJetsWithFOTaus_) {
      for (auto i : *_ct){
	crvec tau(ptvec((*Tau_pt_)[i],0,(*Tau_phi_)[i],0));
	_mht = _mht - tau;
      }
    }
    
    for (auto thr : _jetptcuts){
      auto mht = _mht;
      JetSumCalculatorOutput sums;
      sums.thr = float(thr);
      sums.htJetj = 0;
      sums.nBJetLoose = 0;
      sums.nBJetMedium = 0;
      sums.nJet = 0;
      sums.nFwdJet = 0;
      sums.fwd1_pt = 0;
      sums.fwd1_eta = 0;
      int var = -1;
      if (variation < 0)
	var = 2*abs(variation) - 1;
      else
	var = 2*variation-2;


      for (auto j : *_cj){
	float pt = (*Jet_pt_)[j];
	if (variation != 0) 
	  pt = (*(Jet_corr_.at(var)))[j];
	float abseta = fabs((*Jet_eta_)[j]) ;
	if (abseta > 2.7 && abseta < 3 ){
	  if (pt  > fwdJetPt2_){
	    sums.nFwdJet++;
	    if (pt > sums.fwd1_pt){
	      sums.fwd1_pt = pt; sums.fwd1_eta = (*Jet_eta_)[j];
	    }
	  }
	  continue;
	}
	else if (abseta > 2.4 && abseta < 5){
	  if (pt > fwdJetPt1_){
	    sums.nFwdJet++;
	    if (pt > sums.fwd1_pt){
	      sums.fwd1_pt = pt; sums.fwd1_eta = (*Jet_eta_)[j];
	    }
	  }
	  continue;
	}
	else if(abseta > 2.4) continue;
	if (pt<=thr) continue;
	float phi = (*Jet_phi_)[j];
	float csv = (*Jet_btagCSV_)[j];
	sums.htJetj += pt;
	crvec jp4(ptvec(pt,0,phi,0));
	mht = mht - jp4;
	if (csv>bTagL_) sums.nBJetLoose += 1;
	if (csv>bTagM_) sums.nBJetMedium += 1;
	sums.nJet += 1;
      }

      sums.mhtJet = mht.Pt();
      output.push_back(sums);
    }

    return output;
  }
  
  void clear() {
    sel_leps.reset(new bool[*nLep_]);
    sel_leps_extrafortau.reset(new bool[*nLep_]);
    sel_taus.reset(new bool[*nTau_]);
    sel_jets.reset(new bool[*nJet_]);
    std::fill_n(sel_leps.get(),*nLep_,false);
    std::fill_n(sel_leps_extrafortau.get(),*nLep_,false);
    std::fill_n(sel_taus.get(),*nTau_,false);
    std::fill_n(sel_jets.get(),*nJet_,false);
  }
  void selectLepton(uint i, bool what=true) {sel_leps.get()[i]=what;}
  void selectLeptonExtraForTau(uint i, bool what=true) {sel_leps_extrafortau.get()[i]=what;}
  void selectTau(uint i, bool what=true) {sel_taus.get()[i]=what;}
  void selectJet(uint i, bool what=true) {sel_jets.get()[i]=what;}
  void loadTags(CombinedObjectTags *tags, bool cleanTausWithLooseLeptons, float wPL=0, float wPM=0){
    bTagL_ = wPL; bTagM_ = wPM;
    std::copy(tags->lepsC.get(),tags->lepsC.get()+*nLep_,sel_leps.get());
    if (cleanTausWithLooseLeptons) std::copy(tags->lepsL.get(),tags->lepsL.get()+*nLep_,sel_leps_extrafortau.get());
    std::copy(tags->tausF.get(),tags->tausF.get()+*nTau_,sel_taus.get());
    std::copy(tags->jetsS.get(),tags->jetsS.get()+*nJet_,sel_jets.get());
  }

  void setDR(float f) {deltaR2cut = f*f;}

  std::pair<std::vector<int>*, std::vector<int>* > run() {
    clean_taus_.clear();
    clean_jets_.clear();

    _ct->clear();
    _cj->clear();

    for (int iT = 0, nT = *nTau_; iT < nT; ++iT) {
      if (!sel_taus[iT]) continue;
      bool ok = true;
      for (int iL = 0, nL = *nLep_; iL < nL; ++iL) {
	if (!(sel_leps.get()[iL] || sel_leps_extrafortau.get()[iL])) continue;
	if (deltaR2((*Lep_eta_)[iL], (*Lep_phi_)[iL], (*Tau_eta_)[iT], (*Tau_phi_)[iT]) < deltaR2cut_taus) {
	  ok = false;
	  break;
	}
      }
      if (ok) {
	clean_taus_.push_back(iT);
	_ct->push_back(iT);
      } else {
	sel_taus.get()[iT]=false; // do not use unclean taus for cleaning jets, use lepton instead
      }
    }

    { // jet cleaning (clean closest jet - one at most - for each lepton or tau, then apply jet selection)
      std::vector<float> vetos_eta;
      std::vector<float> vetos_phi;
      std::vector<int>   vetos_indices;
      for (int iL = 0, nL = *nLep_; iL < nL; ++iL) if (sel_leps[iL]) {vetos_eta.push_back((*Lep_eta_)[iL]); vetos_phi.push_back((*Lep_phi_)[iL]); if (Lep_jet_) vetos_indices.push_back((*Lep_jet_)[iL]);}
      for (int iT = 0, nT = *nTau_; iT < nT; ++iT) if (sel_taus[iT]) {vetos_eta.push_back((*Tau_eta_)[iT]); vetos_phi.push_back((*Tau_phi_)[iT]); if (Tau_jet_) vetos_indices.push_back((*Tau_jet_)[iT]);}
      std::unique_ptr<bool[]> good;
      good.reset(new bool[*nJet_]);
      std::fill_n(good.get(),*nJet_,true);
      if (cleanWithRef_){
	for (uint iV=0; iV<vetos_indices.size(); iV++) {
	  if (vetos_indices[iV] > -1) good[vetos_indices[iV]] = false;
	}
      }
      else{
	for (uint iV=0; iV<vetos_eta.size(); iV++) {
	  float mindr2 = -1; int best = -1;
	  for (int iJ = 0, nJ = *nJet_; iJ < nJ; ++iJ) {
	    float dr2 = deltaR2(vetos_eta[iV],vetos_phi[iV],(*Jet_eta_)[iJ], (*Jet_phi_)[iJ]);
	    if (mindr2<0 || dr2<mindr2) {mindr2=dr2; best=iJ;}
	  }
	  if (best>-1 && mindr2<deltaR2cut) {
	    good[best] = false;
	  }
	}
      }
      for (int iJ = 0, nJ = *nJet_; iJ < nJ; ++iJ) {
	if (good[iJ] && sel_jets[iJ]) {
	  _cj->push_back(iJ);
	  if(fabs((*Jet_eta_)[iJ]) < 2.4)
	    clean_jets_.push_back(iJ); // only to count fwd jets
	}
      }
    }

    return std::make_pair(_ct.get(),_cj.get());
  }

private:
  std::unique_ptr<bool[]> sel_leps, sel_leps_extrafortau, sel_taus, sel_jets;
  CollectionSkimmer &clean_taus_, &clean_jets_;
  rcount nLep_, nTau_, nJet_;
  rfloats *Lep_pt_, *Lep_eta_, *Lep_phi_;
  rfloats *Tau_pt_, *Tau_eta_, *Tau_phi_;
  rfloats *Jet_pt_, *Jet_phi_, *Jet_eta_, *Jet_btagCSV_;
  vector<rfloats*> Jet_corr_;
  rints    *Lep_jet_, *Tau_jet_;
  float deltaR2cut;
  float deltaR2cut_taus;
  std::set<int> _jetptcuts;
  std::unique_ptr<std::vector<int> > _ct;
  std::unique_ptr<std::vector<int> > _cj;
  bool cleanJetsWithFOTaus_;
  float bTagL_,bTagM_;
  bool cleanWithRef_;
  float fwdJetPt1_, fwdJetPt2_;
};
