#include <cmath>
#include <vector>
#include <algorithm>
#include <TTreeReaderValue.h>
#include <TTreeReaderArray.h>
#include <TLorentzVector.h>

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
  typedef TTreeReaderValue<int>   rint;
  typedef TTreeReaderArray<float> rfloats;
  typedef TTreeReaderArray<int> rints;
  
  fastCombinedObjectRecleanerMassVetoCalculator(bool doVetoZ = true, bool doVetoLMf = true, bool doVetoLMt = true) : doVetoZ_(doVetoZ), doVetoLMf_(doVetoLMf), doVetoLMt_(doVetoLMt){}
  
  void setLeptons(rint *nLep, rfloats *lepPt, rfloats *lepEta, rfloats *lepPhi, rfloats *lepMass, rints *lepPdgId) {
    nLep_ = nLep; Lep_pt_ = lepPt; Lep_eta_ = lepEta; Lep_phi_ = lepPhi; Lep_mass_ = lepMass; Lep_pdgid_ = lepPdgId;
  }

  float Mass(int i, int j){
    TLorentzVector p1, p2;
    p1.SetPtEtaPhiM((*Lep_pt_)[i],(*Lep_eta_)[i],(*Lep_phi_)[i],(*Lep_mass_)[i]);
    p2.SetPtEtaPhiM((*Lep_pt_)[j],(*Lep_eta_)[j],(*Lep_phi_)[j],(*Lep_mass_)[j]);
    return (p1+p2).M();
  }

  MassVetoCalculatorOutput GetPairMasses(){
    MassVetoCalculatorOutput output;
    output.mZ1 = -1;
    output.minMllAFAS = -1;
    output.minMllAFOS = -1;
    output.minMllAFSS = -1;
    output.minMllSFOS = -1;
    for (auto p : pairs){
      if ((output.mZ1<0 || fabs(p.m-91.2)<fabs(output.mZ1-91.2)) && p.isOS && p.isSF) output.mZ1 = p.m;
      if (output.minMllAFAS<0 || p.m<output.minMllAFAS) output.minMllAFAS = p.m;
      if ((output.minMllAFOS<0 || p.m<output.minMllAFOS) && p.isOS) output.minMllAFOS = p.m;
      if ((output.minMllAFSS<0 || p.m<output.minMllAFSS) && !(p.isOS)) output.minMllAFSS = p.m;
      if ((output.minMllSFOS<0 || p.m<output.minMllSFOS) && p.isOS && p.isSF) output.minMllSFOS = p.m;
    }
    return output;
  }

  void run() {

    int nLep = **nLep_;
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
      if ((doVetoZ_ && 76.2<p.m && p.m<106.2 && p.isOS && p.isSF) || (doVetoLMf_ && 0<p.m && p.m<12 && p.isOS && p.isSF)) {veto_FO.insert(p.i); veto_FO.insert(p.j);}
      if ((doVetoZ_ && 76.2<p.m && p.m<106.2 && p.isOS && p.isSF) || (doVetoLMt_ && 0<p.m && p.m<12 && p.isOS && p.isSF)) {veto_tight.insert(p.i); veto_tight.insert(p.j);}
    }
    for (auto i: veto_FO) leps_fo.erase(i);
    for (auto i: veto_tight) leps_tight.erase(i);

  }

  std::vector<int> getVetoedFO() {std::vector<int> _l; for (auto x: leps_fo) _l.push_back(x); return _l;}
  std::vector<int> getVetoedTight() {std::vector<int> _l; for (auto x: leps_tight) _l.push_back(x); return _l;}

  void clear(){
    nLep = **nLep_;
    pairs.clear();
    leps_loose.reset(new bool[nLep]);
    std::fill_n(leps_loose.get(),nLep,false);
    leps_fo.clear();
    leps_tight.clear();
  }

  void setLeptonFlagLoose(int i){
    leps_loose[i] = true;
  }
  void setLeptonFlagFO(int i){
    assert(leps_loose[i]);
    leps_fo.insert(i);
  }
  void setLeptonFlagTight(int i){
    assert(leps_loose[i]);
    leps_tight.insert(i);
  }

private:
  rint *nLep_;
  rfloats *Lep_pt_, *Lep_eta_, *Lep_phi_, *Lep_mass_;
  rints *Lep_pdgid_;
  std::vector<LeptonPairInfo> pairs;
  Int_t nLep;
  std::unique_ptr<bool[]> leps_loose;
  std::set<int> leps_fo, leps_tight;
  bool doVetoZ_;
  bool doVetoLMf_;
  bool doVetoLMt_;
};
