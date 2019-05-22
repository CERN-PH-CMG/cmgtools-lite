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
  
  fastCombinedObjectRecleanerHelper(CollectionSkimmer &clean_taus, CollectionSkimmer &clean_jets, bool cleanJetsWithFOTaus, float bTagL, float bTagM) : clean_taus_(clean_taus), clean_jets_(clean_jets), deltaR2cut(0.16), cleanJetsWithFOTaus_(cleanJetsWithFOTaus), bTagL_(bTagL), bTagM_(bTagM) {
    _ct.reset(new std::vector<int>);
    _cj.reset(new std::vector<int>);
}
  
  void setLeptons(rint *nLep, rfloats* lepPt, rfloats *lepEta, rfloats *lepPhi) {
    nLep_ = nLep; Lep_pt_ = lepPt; Lep_eta_ = lepEta; Lep_phi_ = lepPhi;
    if (!nLep || !lepPt || !lepEta || !lepPhi) { std::cout << "ERROR: fastCombinedObjectRecleanerHelper initialized setLeptons with a null reader" << std::endl; }
  }
  void setLeptons(ruint *nLep, rfloats* lepPt, rfloats *lepEta, rfloats *lepPhi) {
    nLep_ = nLep; Lep_pt_ = lepPt; Lep_eta_ = lepEta; Lep_phi_ = lepPhi;
    if (!nLep || !lepPt || !lepEta || !lepPhi) { std::cout << "ERROR: fastCombinedObjectRecleanerHelper initialized setLeptons with a null reader" << std::endl; }
  }
  void setTaus(rint *nTau, rfloats *tauPt, rfloats *tauEta, rfloats *tauPhi) {
    nTau_ = nTau; Tau_pt_ = tauPt; Tau_eta_ = tauEta; Tau_phi_ = tauPhi;
    if (!nTau || !tauPt || !tauEta || !tauPhi) { std::cout << "ERROR: fastCombinedObjectRecleanerHelper initialized setTaus with a null reader" << std::endl; }
  }
  void setTaus(ruint *nTau, rfloats *tauPt, rfloats *tauEta, rfloats *tauPhi) {
    nTau_ = nTau; Tau_pt_ = tauPt; Tau_eta_ = tauEta; Tau_phi_ = tauPhi;
    if (!nTau || !tauPt || !tauEta || !tauPhi) { std::cout << "ERROR: fastCombinedObjectRecleanerHelper initialized setTaus with a null reader" << std::endl; }
  }
  void setJets(rint *nJet, rfloats *jetPt, rfloats *jetEta, rfloats *jetPhi, rfloats *jetbtagCSV, rfloats *jetcorr, rfloats *jetcorr_JECUp, rfloats *jetcorr_JECDown) {
    nJet_ = nJet; Jet_pt_ = jetPt; Jet_eta_ = jetEta; Jet_phi_ = jetPhi; Jet_btagCSV_ = jetbtagCSV; Jet_corr_ = jetcorr; Jet_corr_JECUp_ = jetcorr_JECUp; Jet_corr_JECDown_ = jetcorr_JECDown;
    if (!nJet || !jetPt || !jetEta || !jetPhi || !jetbtagCSV) { std::cout << "ERROR: fastCombinedObjectRecleanerHelper initialized setJets with a null reader" << std::endl; }
  }
  void setJets(ruint *nJet, rfloats *jetPt, rfloats *jetEta, rfloats *jetPhi, rfloats *jetbtagCSV, rfloats *jetcorr = NULL, rfloats *jetcorr_JECUp = NULL, rfloats *jetcorr_JECDown = NULL) {
    nJet_ = nJet; Jet_pt_ = jetPt; Jet_eta_ = jetEta; Jet_phi_ = jetPhi; Jet_btagCSV_ = jetbtagCSV; Jet_corr_ = jetcorr; Jet_corr_JECUp_ = jetcorr_JECUp; Jet_corr_JECDown_ = jetcorr_JECDown;
    if (!nJet || !jetPt || !jetEta || !jetPhi || !jetbtagCSV) { std::cout << "ERROR: fastCombinedObjectRecleanerHelper initialized setJets with a null reader" << std::endl; }
  }

  void addJetPt(int pt){
    _jetptcuts.insert(pt);
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
      
      for (auto j : *_cj){
	float pt = (*Jet_pt_)[j];
	if (variation==1) pt *= (*Jet_corr_JECUp_)[j] / (*Jet_corr_)[j];
	if (variation==-1) pt *= (*Jet_corr_JECDown_)[j] / (*Jet_corr_)[j];
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

  void loadTags(CombinedObjectTags *tags, bool cleanTausWithLooseLeptons){
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
	if (deltaR2((*Lep_eta_)[iL], (*Lep_phi_)[iL], (*Tau_eta_)[iT], (*Tau_phi_)[iT]) < deltaR2cut) {
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
      for (int iL = 0, nL = *nLep_; iL < nL; ++iL) if (sel_leps[iL]) {vetos_eta.push_back((*Lep_eta_)[iL]); vetos_phi.push_back((*Lep_phi_)[iL]);}
      for (int iT = 0, nT = *nTau_; iT < nT; ++iT) if (sel_taus[iT]) {vetos_eta.push_back((*Tau_eta_)[iT]); vetos_phi.push_back((*Tau_phi_)[iT]);}
      std::unique_ptr<bool[]> good;
      good.reset(new bool[*nJet_]);
      std::fill_n(good.get(),*nJet_,true);
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
      for (int iJ = 0, nJ = *nJet_; iJ < nJ; ++iJ) {
	if (good[iJ] && sel_jets[iJ]) {
	  clean_jets_.push_back(iJ);
	  _cj->push_back(iJ);
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
  rfloats *Jet_pt_, *Jet_phi_, *Jet_eta_, *Jet_btagCSV_, *Jet_corr_, *Jet_corr_JECUp_, *Jet_corr_JECDown_;
  float deltaR2cut;
  std::set<int> _jetptcuts;
  std::unique_ptr<std::vector<int> > _ct;
  std::unique_ptr<std::vector<int> > _cj;
  bool cleanJetsWithFOTaus_;
  float bTagL_,bTagM_;
};
