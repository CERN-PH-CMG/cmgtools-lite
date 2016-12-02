#include <cmath>
#include <vector>
#include <algorithm>
#include <TTreeReaderValue.h>
#include <TTreeReaderArray.h>
#include <TLorentzVector.h>
#include <DataFormats/Math/interface/deltaR.h>
#include <CMGTools/TTHAnalysis/interface/CollectionSkimmer.h>
#include "CMGTools/TTHAnalysis/interface/CombinedObjectTags.h"

struct JetSumCalculatorOutput {
  int thr;
  float htJetj;
  float mhtJet;
  int nBJetLoose;
  int nBJetMedium; 
};

class fastCombinedObjectRecleanerHelper {
public:
  typedef TTreeReaderValue<int>   rint;
  typedef TTreeReaderArray<float> rfloats;
  typedef TTreeReaderArray<int> rints;
  
  fastCombinedObjectRecleanerHelper(CollectionSkimmer &clean_taus, CollectionSkimmer &clean_jets, float bTagL, float bTagM) : clean_taus_(clean_taus), clean_jets_(clean_jets), deltaR2cut(0.16), bTagL_(bTagL), bTagM_(bTagM) {}
  
  void setLeptons(rint *nLep, rfloats* lepPt, rfloats *lepEta, rfloats *lepPhi) {
    nLep_ = nLep; Lep_pt_ = lepPt; Lep_eta_ = lepEta; Lep_phi_ = lepPhi;
  }
  void setTaus(rint *nTau, rfloats *tauPt, rfloats *tauEta, rfloats *tauPhi) {
    nTau_ = nTau; Tau_pt_ = tauPt; Tau_eta_ = tauEta; Tau_phi_ = tauPhi;
  }
  void setJets(rint *nJet, rfloats *jetPt, rfloats *jetEta, rfloats *jetPhi, rfloats *jetbtagCSV) {
    nJet_ = nJet; Jet_pt_ = jetPt; Jet_eta_ = jetEta; Jet_phi_ = jetPhi; Jet_btagCSV_ = jetbtagCSV;
  }

  void addJetPt(int pt){
    _jetptcuts.insert(pt);
  }

  std::vector<JetSumCalculatorOutput> GetJetSums(){

    std::vector<JetSumCalculatorOutput> output;

      for (auto thr : _jetptcuts){

	TLorentzVector mht(0,0,0,0);
	JetSumCalculatorOutput sums;
	sums.thr = float(thr);
	sums.htJetj = 0;
	sums.nBJetLoose = 0;
	sums.nBJetMedium = 0;

	for (int i=0; i<**nLep_; i++) {
	  if (!sel_leps[i]) continue;
	  TLorentzVector lep;
	  lep.SetPtEtaPhiM((*Lep_pt_)[i],0,(*Lep_phi_)[i],0);
	  mht = mht - lep;
	}
	for (auto i : _ct){
	  TLorentzVector tau;
	  tau.SetPtEtaPhiM((*Tau_pt_)[i],0,(*Tau_phi_)[i],0);
	  mht = mht - tau;
	}

	for (auto j : _cj){
	  float pt = (*Jet_pt_)[j];
	  if (pt<=thr) continue;
	  float phi = (*Jet_phi_)[j];
	  float csv = (*Jet_btagCSV_)[j];
	  sums.htJetj += pt;
	  TLorentzVector jp4;
	  jp4.SetPtEtaPhiM(pt,0,phi,0);
	  mht = mht - jp4;
	  if (csv>bTagL_) sums.nBJetLoose += 1;
	  if (csv>bTagM_) sums.nBJetMedium += 1;
	}

	sums.mhtJet = mht.Pt();
	output.push_back(sums);
      }
      return output;
  }
  
  void clear() {
    sel_leps.reset(new bool[**nLep_]);
    sel_leps_extrafortau.reset(new bool[**nLep_]);
    sel_taus.reset(new bool[**nTau_]);
    sel_jets.reset(new bool[**nJet_]);
    std::fill_n(sel_leps.get(),**nLep_,false);
    std::fill_n(sel_leps_extrafortau.get(),**nLep_,false);
    std::fill_n(sel_taus.get(),**nTau_,false);
    std::fill_n(sel_jets.get(),**nJet_,false);
  }
  void selectLepton(uint i, bool what=true) {sel_leps.get()[i]=what;}
  void selectLeptonExtraForTau(uint i, bool what=true) {sel_leps_extrafortau.get()[i]=what;}
  void selectTau(uint i, bool what=true) {sel_taus.get()[i]=what;}
  void selectJet(uint i, bool what=true) {sel_jets.get()[i]=what;}

  void loadTags(CombinedObjectTags *tags, bool cleanTausWithLooseLeptons){
    std::copy(tags->lepsC.get(),tags->lepsC.get()+**nLep_,sel_leps.get());
    if (cleanTausWithLooseLeptons) std::copy(tags->lepsL.get(),tags->lepsL.get()+**nLep_,sel_leps_extrafortau.get());
    std::copy(tags->tausF.get(),tags->tausF.get()+**nTau_,sel_taus.get());
    std::copy(tags->jetsS.get(),tags->jetsS.get()+**nJet_,sel_jets.get());
  }

  void setDR(float f) {deltaR2cut = f*f;}

  std::pair<std::vector<int>, std::vector<int> > run() {

    clean_taus_.clear();
    clean_jets_.clear();

    _ct.clear();
    _cj.clear();

    for (int iT = 0, nT = **nTau_; iT < nT; ++iT) {
      if (!sel_taus[iT]) continue;
      bool ok = true;
      for (int iL = 0, nL = **nLep_; iL < nL; ++iL) {
	if (!(sel_leps.get()[iL] || sel_leps_extrafortau.get()[iL])) continue;
	if (deltaR2((*Lep_eta_)[iL], (*Lep_phi_)[iL], (*Tau_eta_)[iT], (*Tau_phi_)[iT]) < deltaR2cut) {
	  ok = false;
	  break;
	}
      }
      if (ok) {
	clean_taus_.push_back(iT);
	_ct.push_back(iT);
      } else {
	sel_taus.get()[iT]=false; // do not use unclean taus for cleaning jets, use lepton instead
      }
    }
    for (int iJ = 0, nJ = **nJet_; iJ < nJ; ++iJ) {
      if (!sel_jets[iJ]) continue;
      bool ok = true;
      for (int iL = 0, nL = **nLep_; iL < nL; ++iL) {
	if (!sel_leps.get()[iL]) continue;
	if (deltaR2((*Lep_eta_)[iL], (*Lep_phi_)[iL], (*Jet_eta_)[iJ], (*Jet_phi_)[iJ]) < deltaR2cut) {
	  ok = false;
	  break;
	}
      }
      for (int iT = 0, nT = **nTau_; iT < nT; ++iT) {
	if (!sel_taus.get()[iT]) continue;
	if (deltaR2((*Tau_eta_)[iT], (*Tau_phi_)[iT], (*Jet_eta_)[iJ], (*Jet_phi_)[iJ]) < deltaR2cut) {
	  ok = false;
	  break;
	}
      }
      if (ok) {
	clean_jets_.push_back(iJ);
	_cj.push_back(iJ);
      }
    }

    return std::make_pair(_ct,_cj);
  }

private:
  std::unique_ptr<bool[]> sel_leps, sel_leps_extrafortau, sel_taus, sel_jets;
  CollectionSkimmer &clean_taus_, &clean_jets_;
  rint *nLep_, *nTau_, *nJet_;
  rfloats *Lep_pt_, *Lep_eta_, *Lep_phi_;
  rfloats *Tau_pt_, *Tau_eta_, *Tau_phi_;
  rfloats *Jet_pt_, *Jet_phi_, *Jet_eta_, *Jet_btagCSV_;
  float deltaR2cut;
  std::set<int> _jetptcuts;
  std::vector<int> _ct;
  std::vector<int> _cj;
  float bTagL_,bTagM_;
};
