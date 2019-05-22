#include <cmath>
#include <vector>
#include <algorithm>
#include <TTreeReaderValue.h>
#include <TTreeReaderArray.h>
#include "CMGTools/TTHAnalysis/interface/CollectionSkimmer.h"
#include "CMGTools/TTHAnalysis/interface/CombinedObjectTags.h"
#include "DataFormats/Math/interface/LorentzVector.h"

struct LeptonPairInfo {
  int i;
  int j;
  float m;
  int isOS;
  int isSF;
};

struct MassVetoCalculatorOutput {
  float mZ1;
  float minMllAFAS;
  float minMllAFOS;
  float minMllAFSS;
  float minMllSFOS;
};

class fastCombinedObjectRecleanerMassVetoCalculator {
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

  typedef math::PtEtaPhiMLorentzVectorD ptvec;
  typedef math::XYZTLorentzVectorD crvec;
  
  fastCombinedObjectRecleanerMassVetoCalculator(CollectionSkimmer &skim_lepsF, CollectionSkimmer &skim_lepsT, bool doVetoZ, bool doVetoLMf, bool doVetoLMt) : skim_lepsF_(skim_lepsF), skim_lepsT_(skim_lepsT), doVetoZ_(doVetoZ), doVetoLMf_(doVetoLMf), doVetoLMt_(doVetoLMt){}
  
  void setLeptons(rint *nLep, rfloats *lepPt, rfloats *lepEta, rfloats *lepPhi, rfloats *lepMass, rints *lepPdgId) {
    nLep_ = nLep; Lep_pt_ = lepPt; Lep_eta_ = lepEta; Lep_phi_ = lepPhi; Lep_mass_ = lepMass; Lep_pdgid_ = lepPdgId;
    if (!nLep || !lepPt || !lepEta || !lepPhi || !lepPdgId) { std::cout << "ERROR: fastCombinedObjectRecleanerMassVetoCalculator initialized setLeptons with a null reader" << std::endl; }
  }
  void setLeptons(ruint *nLep, rfloats *lepPt, rfloats *lepEta, rfloats *lepPhi, rfloats *lepMass, rints *lepPdgId) {
    nLep_ = nLep; Lep_pt_ = lepPt; Lep_eta_ = lepEta; Lep_phi_ = lepPhi; Lep_mass_ = lepMass; Lep_pdgid_ = lepPdgId;
    if (!nLep || !lepPt || !lepEta || !lepPhi || !lepPdgId) { std::cout << "ERROR: fastCombinedObjectRecleanerMassVetoCalculator initialized setLeptons with a null reader" << std::endl; }
  }

  float Mass(int i, int j){
    return (leps_p4[i]+leps_p4[j]).M();
  }

  MassVetoCalculatorOutput GetPairMasses(){
    MassVetoCalculatorOutput output;
    output.mZ1 = -1;
    output.minMllAFAS = -1;
    output.minMllAFOS = -1;
    output.minMllAFSS = -1;
    output.minMllSFOS = -1;
    for (auto p : pairs){
      if ((output.mZ1<0 || fabs(p.m-91)<fabs(output.mZ1-91)) && p.isOS && p.isSF) output.mZ1 = p.m;
      if (output.minMllAFAS<0 || p.m<output.minMllAFAS) output.minMllAFAS = p.m;
      if ((output.minMllAFOS<0 || p.m<output.minMllAFOS) && p.isOS) output.minMllAFOS = p.m;
      if ((output.minMllAFSS<0 || p.m<output.minMllAFSS) && !(p.isOS)) output.minMllAFSS = p.m;
      if ((output.minMllSFOS<0 || p.m<output.minMllSFOS) && p.isOS && p.isSF) output.minMllSFOS = p.m;
    }
    return output;
  }

  void run() {
    int nLep = *nLep_;
    for (int i=0; i<nLep; i++) if (leps_loose[i]) leps_p4[i] = ptvec((*Lep_pt_)[i],(*Lep_eta_)[i],(*Lep_phi_)[i],(*Lep_mass_)[i]);
    for (int i=0; i<nLep; i++){
      if (!leps_loose[i]) continue;
      for (int j=i+1; j<nLep; j++){
	if (!leps_loose[j]) continue;
	LeptonPairInfo pair;
	pair.i = i;
	pair.j = j;
	pair.m = Mass(i,j);
	pair.isOS = ((*Lep_pdgid_)[i]*(*Lep_pdgid_)[j]<0);
	pair.isSF = (abs((*Lep_pdgid_)[i])==abs((*Lep_pdgid_)[j]));
	pairs.push_back(pair);
      }
    }

    std::set<int> veto_FO;
    std::set<int> veto_tight;
    for (auto p: pairs){
      if ((doVetoZ_ && 76<p.m && p.m<106 && p.isOS && p.isSF) || (doVetoLMf_ && 0<p.m && p.m<12 && p.isOS && p.isSF)) {veto_FO.insert(p.i); veto_FO.insert(p.j);}
      if ((doVetoZ_ && 76<p.m && p.m<106 && p.isOS && p.isSF) || (doVetoLMt_ && 0<p.m && p.m<12 && p.isOS && p.isSF)) {veto_tight.insert(p.i); veto_tight.insert(p.j);}
    }
    for (auto i: veto_FO) leps_fo.erase(std::remove(leps_fo.begin(),leps_fo.end(),i),leps_fo.end());
    for (auto i: veto_tight) leps_tight.erase(std::remove(leps_tight.begin(),leps_tight.end(),i),leps_tight.end());

    for (auto i : leps_fo) skim_lepsF_.push_back(i);
    for (auto i : leps_tight) skim_lepsT_.push_back(i);

  }

  std::vector<int>* getVetoedFO() {return &leps_fo;}
  std::vector<int>* getVetoedTight() {return &leps_tight;}

  void clear(){
    nLep = *nLep_;
    pairs.clear();
    leps_loose.reset(new bool[nLep]);
    std::fill_n(leps_loose.get(),nLep,false);
    leps_fo.clear();
    leps_tight.clear();
    leps_p4.reset(new crvec[nLep]);
  }

  void loadTags(CombinedObjectTags *tags){
    std::copy(tags->lepsL.get(),tags->lepsL.get()+*nLep_,leps_loose.get());
    for (auto i : tags->getLepsF_byConePt()) leps_fo.push_back(i);
    for (int i=0; i<*nLep_; i++) if (tags->lepsT[i]) leps_tight.push_back(i);
  }

  void setLeptonFlagLoose(int i){
    leps_loose[i] = true;
  }
  void setLeptonFlagFO(int i){
    assert(leps_loose[i]);
    leps_fo.push_back(i);
  }
  void setLeptonFlagTight(int i){
    assert(leps_loose[i]);
    leps_tight.push_back(i);
  }

private:
  CollectionSkimmer &skim_lepsF_, &skim_lepsT_;
  rcount nLep_;
  rfloats *Lep_pt_, *Lep_eta_, *Lep_phi_, *Lep_mass_;
  rints *Lep_pdgid_;
  std::vector<LeptonPairInfo> pairs;
  Int_t nLep;
  std::unique_ptr<bool[]> leps_loose;
  std::vector<int> leps_fo, leps_tight;
  std::unique_ptr<crvec[]> leps_p4;
  bool doVetoZ_;
  bool doVetoLMf_;
  bool doVetoLMt_;
};
