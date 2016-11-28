#include <cmath>
#include <vector>
#include <algorithm>
#include <TTreeReaderValue.h>
#include <TTreeReaderArray.h>
#include <DataFormats/Math/interface/deltaR.h>
#include <CMGTools/TTHAnalysis/interface/CollectionSkimmer.h>

class fastCombinedObjectRecleanerHelper {
public:
  typedef TTreeReaderValue<int>   rint;
  typedef TTreeReaderArray<float> rfloats;
  typedef TTreeReaderArray<int> rints;
  
  fastCombinedObjectRecleanerHelper(CollectionSkimmer &clean_taus, CollectionSkimmer &clean_jets) : clean_taus_(clean_taus), clean_jets_(clean_jets), deltaR2cut(0.16) {}
  
  void setLeptons(rint *nLep, rfloats *lepEta, rfloats *lepPhi) {
    nLep_ = nLep; Lep_eta_ = lepEta; Lep_phi_ = lepPhi;
  }
  void setTaus(rint *nTau, rfloats *tauEta, rfloats *tauPhi) {
    nTau_ = nTau; Tau_eta_ = tauEta; Tau_phi_ = tauPhi;
  }
  void setJets(rint *nJet, rfloats *jetEta, rfloats *jetPhi) {
    nJet_ = nJet; Jet_eta_ = jetEta; Jet_phi_ = jetPhi;
  }

  void clear() {
    sel_leps.reset(new bool[**nLep_]);
    sel_taus.reset(new bool[**nTau_]);
    sel_jets.reset(new bool[**nJet_]);
    for (int i=0; i<**nLep_; i++) sel_leps.get()[i]=false;
    for (int i=0; i<**nTau_; i++) sel_taus.get()[i]=false;
    for (int i=0; i<**nJet_; i++) sel_jets.get()[i]=false;
  }
  void selectLepton(uint i, bool what=true) {sel_leps.get()[i]=what;}
  void selectTau(uint i, bool what=true) {sel_taus.get()[i]=what;}
  void selectJet(uint i, bool what=true) {sel_jets.get()[i]=what;}

  void setDR(float f) {deltaR2cut = f*f;}

  std::pair<std::vector<int>, std::vector<int> > run() {

    clean_taus_.clear();
    clean_jets_.clear();

    std::vector<int> _ct;
    std::vector<int> _cj;

    for (int iT = 0, nT = **nTau_; iT < nT; ++iT) {
      bool ok = true;
      for (int iL = 0, nL = **nLep_; iL < nL; ++iL) {
	if (!sel_leps.get()[iL]) continue;
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
  std::unique_ptr<bool[]> sel_leps, sel_taus, sel_jets;
  CollectionSkimmer &clean_taus_, &clean_jets_;
  rint *nLep_, *nTau_, *nJet_;
  rfloats *Lep_eta_, *Lep_phi_;
  rfloats *Tau_eta_, *Tau_phi_;
  rfloats *Jet_phi_, *Jet_eta_;
  float deltaR2cut;
};
