#ifndef CMGTools_WMassTools_JetReCleanerHelper_h
#define CMGTools_WMassTools_JetReCleanerHelper_h

#include <iostream>
#include <vector>
#include <TTreeReaderValue.h>
#include <TTreeReaderArray.h>
#include <DataFormats/Math/interface/deltaR.h>

class JetReCleanerHelper {
 public:
  typedef TTreeReaderValue<int>   rint;
  typedef TTreeReaderArray<float> rfloats;
  typedef TTreeReaderArray<int> rints;

  JetReCleanerHelper(float dR=0.4) { deltaR_=dR; }
  ~JetReCleanerHelper() {}
  
  void setLeptons(rint *nLep, rfloats *lepEta, rfloats *lepPhi) {
    nLep_ = nLep; Lep_eta_ = lepEta; Lep_phi_ = lepPhi;
  }
  void setJets(rint *nJet, rfloats *jetEta, rfloats *jetPhi, rfloats *jetPt) {
    nJet_ = nJet; Jet_eta_ = jetEta; Jet_phi_ = jetPhi;  Jet_pt_ = jetPt;

  }
  const std::vector<int> & run() {
    ret_.clear();
    int n = (*nJet_).Get()[0];
    for (int iJ = 0, nJ = **nJet_; iJ < nJ; ++iJ) {
      if((*Jet_pt_)[iJ] < 25.00 || abs((*Jet_eta_)[iJ]) > 2.4) continue;
      //      if((*Jet_pt_)[iJ] < 25.00 || abs((*Jet_eta_)[iJ]) > 2.4)cout<<"here"<<(*Jet_pt_)[iJ]<<"\t"<<abs((*Jet_eta_)[iJ])<<endl;
      bool ok = true;
      for (int iL = 0, nL = **nLep_; iL < nL; ++iL) {
        if (deltaR2((*Lep_eta_)[iL], (*Lep_phi_)[iL], (*Jet_eta_)[iJ], (*Jet_phi_)[iJ]) < deltaR_*deltaR_) {
          ok = false;
          break;
        }
      }
      if (ok) {
        ret_.push_back(iJ);
      }
    }
    return ret_;
  }

private:
  std::vector<int> ret_;
  float deltaR_;
  rint *nLep_ = nullptr;
  rint *nJet_ = nullptr;
  rfloats *Lep_eta_ = nullptr;
  rfloats *Lep_phi_ = nullptr;
  rfloats *Jet_phi_ = nullptr;
  rfloats *Jet_eta_ = nullptr;
  rfloats *Jet_pt_ = nullptr;
};

#endif

