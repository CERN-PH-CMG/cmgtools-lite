#include <vector>
#include <string>
#include <unordered_set>
#include <unordered_map>
#include <utility>
#include "TLorentzVector.h"
#include "TMVA/Reader.h"
#include <iostream>

class BDTv8_eventReco_Jet {
 public:
  BDTv8_eventReco_Jet(){
    p4.SetXYZT(0,0,0,0);
    csv = -0.2;
  };
  BDTv8_eventReco_Jet(float pt,float eta, float phi, float mass, float _csv){
    p4.SetPtEtaPhiM(pt,eta,phi,mass);
    csv = std::max(float(-0.1),_csv);
  };
  ~BDTv8_eventReco_Jet(){};
  TLorentzVector p4;
  float csv;
};

class BDTv8_eventReco_Lep {
 public:
  BDTv8_eventReco_Lep(){
    p4.SetXYZT(0,0,0,0);
  };
  BDTv8_eventReco_Lep(float pt,float eta, float phi, float mass){
    p4.SetPtEtaPhiM(pt,eta,phi,mass);
  };
  ~BDTv8_eventReco_Lep(){};
  TLorentzVector p4;
};

class BDTv8_eventReco {
 public: 
  BDTv8_eventReco(std::string weight_file_name){
    Init(weight_file_name);
  };
  ~BDTv8_eventReco(){
    clear();
    delete TMVAReader_;
    delete nulljet;
  };
  void addJet(float pt,float eta, float phi, float mass, float csv){
    jets.push_back(new BDTv8_eventReco_Jet(pt,eta,phi,mass,csv));
  };
  void addLep(float pt,float eta, float phi, float mass){
    leps.push_back(new BDTv8_eventReco_Lep(pt,eta,phi,mass));
  };
  void clear();
  void Init(std::string weight_file_name);
  std::vector<float> EvalMVA();

  std::vector<BDTv8_eventReco_Jet*> jets;
  std::vector<BDTv8_eventReco_Lep*> leps;
  BDTv8_eventReco_Jet* nulljet;

  std::pair<float,float> CalcJetComb(std::unordered_map<std::string,std::pair<float,float> > *done_jetcomb, int i1, int i2, int i3=-99);

  TMVA::Reader *TMVAReader_;

  float bJet_fromLepTop_CSV_var;
  float bJet_fromHadTop_CSV_var;
  float qJet1_fromW_fromHadTop_CSV_var;
  float HadTop_pT_var;
  float W_fromHadTop_mass_var;
  float HadTop_mass_var;
  float W_fromHiggs_mass_var;
  float LepTop_HadTop_dR_var;

};

void BDTv8_eventReco::Init(std::string weight_file_name){

  TMVAReader_ = new TMVA::Reader( "!Color:!Silent" );
  
  TMVAReader_->AddVariable( "bJet_fromLepTop_CSV", &bJet_fromLepTop_CSV_var );
  TMVAReader_->AddVariable( "bJet_fromHadTop_CSV", &bJet_fromHadTop_CSV_var );
  TMVAReader_->AddVariable( "qJet1_fromW_fromHadTop_CSV", &qJet1_fromW_fromHadTop_CSV_var );
  TMVAReader_->AddVariable( "HadTop_pT", &HadTop_pT_var );
  TMVAReader_->AddVariable( "W_fromHadTop_mass", &W_fromHadTop_mass_var );
  TMVAReader_->AddVariable( "HadTop_mass", &HadTop_mass_var );
  TMVAReader_->AddVariable( "W_fromHiggs_mass", &W_fromHiggs_mass_var );
  TMVAReader_->AddVariable( "LepTop_HadTop_dR", &LepTop_HadTop_dR_var );
  
  TMVAReader_->BookMVA("BDTG method", weight_file_name);

  clear();

  nulljet = new BDTv8_eventReco_Jet();

};

void BDTv8_eventReco::clear(){

  for (auto *p : jets) delete p;
  for (auto *p : leps) delete p;
  jets.clear();
  leps.clear();

  bJet_fromLepTop_CSV_var = -99;
  bJet_fromHadTop_CSV_var = -99;
  qJet1_fromW_fromHadTop_CSV_var = -99;
  HadTop_pT_var = -99;
  W_fromHadTop_mass_var = -99;
  HadTop_mass_var = -99;
  W_fromHiggs_mass_var = -99;
  LepTop_HadTop_dR_var = -99;

}

std::pair<float,float> BDTv8_eventReco::CalcJetComb(std::unordered_map<std::string,std::pair<float,float> > *done_jetcomb, int i1, int i2, int i3){
  BDTv8_eventReco_Jet *j1 = (i1<0) ? nulljet : jets.at(i1);
  BDTv8_eventReco_Jet *j2 = (i2<0) ? nulljet : jets.at(i2);
  BDTv8_eventReco_Jet *j3 = (i3<0) ? nulljet : jets.at(i3);
  char _xc[3] = {(char)i1,(char)i2,(char)i3};
  std::sort(_xc,_xc+3);
  std::string _x(_xc,_xc+3);
  auto it = done_jetcomb->find(_x);
  if (it!=done_jetcomb->end()) return (*it).second;
  TLorentzVector comb = (i3<0) ? (j1->p4+j2->p4) : (j1->p4+j2->p4+j3->p4);
  std::pair<float,float> res = std::pair<float,float>(comb.Pt(),comb.M());
  (*done_jetcomb)[_x] = res;
  return res;
}

std::vector<float> BDTv8_eventReco::EvalMVA(){

  std::vector<int> permlep;
  for (int i=0; i<int(leps.size()); i++) permlep.push_back(i);
  std::vector<int> permjet;
  for (int i=0; i<int(jets.size()); i++) permjet.push_back(i);
  if (permjet.size()<8) for (int i=0; i<3; i++) permjet.push_back(-1-i);
  else if (permjet.size()==8) for (int i=0; i<2; i++) permjet.push_back(-1-i);
  else permjet.push_back(-1);

  uint warn_n_jets = 10;
  uint max_n_jets = 11;
  bool warn = false;
  if (permjet.size()>=warn_n_jets && permlep.size()>=2) {
    std::cout << "Warning: large number of jets: " << permjet.size() << " (" << jets.size() << " non-null) ... " ;
    warn = true;
  }
  if (permjet.size()>max_n_jets && permlep.size()>=2){
    std::cout << "Warning: large number of jets, cropped to " << max_n_jets << " ... " ;
    permjet.resize(max_n_jets);
    warn = true;
  }

  std::sort(permlep.begin(),permlep.end());
  std::sort(permjet.begin(),permjet.end());

  char *_permjet = new char[permjet.size()];
  for (int i=0; i<int(permjet.size()); i++) _permjet[i]=permjet[i];
  uint n = permjet.size();

  float max_mva_value = -99;
  std::vector<float> best_permutation;
  
  std::unordered_set<std::string> done_perms;
  std::unordered_map<std::string,std::pair<float,float> > done_jetcomb;

  long nperm = 0;

  do {
    do {
      nperm++;

      if (nperm==1){
	if (n<6) break;
	if (permlep.size()<2) break;
      }

      char _xc[6];
      for (int i=0; i<6; i++) _xc[i] = (int(_permjet[i])<0) ? -1 : _permjet[i];
      std::string _x(_xc,_xc+6);

      {
	if (done_perms.find(_x) != done_perms.end()) continue;
	char _x2c[6];
	std::copy(_xc,_xc+6,_x2c);
	std::swap(*(_x2c+2),*(_x2c+3));
	std::string _x2(_x2c,_x2c+6);
	if (done_perms.find(_x2) != done_perms.end()) continue;
	char _x3c[6];
	std::copy(_xc,_xc+6,_x3c);
	std::swap(*(_x3c+4),*(_x3c+5));
	std::string _x3(_x3c,_x3c+6);
	if (done_perms.find(_x3) != done_perms.end()) continue;
      }

      done_perms.insert(_x);

      BDTv8_eventReco_Jet *bjet_fromHadTop = ((int)(_x[0])>=0) ? jets[(int)(_x[0])] : nulljet;
      BDTv8_eventReco_Jet *bjet_fromLepTop = ((int)(_x[1])>=0) ? jets[(int)(_x[1])] : nulljet;
      BDTv8_eventReco_Jet *wjet1_fromHadTop = ((int)(_x[2])>=0) ? jets[(int)(_x[2])] : nulljet;
      BDTv8_eventReco_Jet *wjet2_fromHadTop = ((int)(_x[3])>=0) ? jets[(int)(_x[3])] : nulljet;
      
      if (std::max(bjet_fromHadTop->csv,bjet_fromLepTop->csv)<0.80 && std::min(bjet_fromHadTop->csv,bjet_fromLepTop->csv)<0.46) continue;
      
      auto hadTop_W = CalcJetComb(&done_jetcomb,_x[2],_x[3]);
      auto hadTop = CalcJetComb(&done_jetcomb,_x[2],_x[3],_x[0]);

      if (hadTop_W.second > 120) continue;
      if (hadTop.second > 220) continue;
      
      BDTv8_eventReco_Jet *wjet1_fromHiggs = ((int)(_x[4])>=0) ? jets[(int)(_x[4])] : nulljet;
      BDTv8_eventReco_Jet *wjet2_fromHiggs = ((int)(_x[5])>=0) ? jets[(int)(_x[5])] : nulljet;
      
      auto higgs_W = CalcJetComb(&done_jetcomb,_x[4],_x[5]);

      BDTv8_eventReco_Lep *lep_fromTop = leps[permlep[0]];
      
      auto lepTop = lep_fromTop->p4 + bjet_fromLepTop->p4;
      
      if (lepTop.M() > 180) continue;
      
      bJet_fromLepTop_CSV_var = bjet_fromLepTop->csv;
      bJet_fromHadTop_CSV_var = bjet_fromHadTop->csv;
      qJet1_fromW_fromHadTop_CSV_var = wjet1_fromHadTop->csv;
      HadTop_pT_var = hadTop.first;
      W_fromHadTop_mass_var = hadTop_W.second;
      HadTop_mass_var = hadTop.second;
      W_fromHiggs_mass_var = higgs_W.second;
      LepTop_HadTop_dR_var = (hadTop.first!=0) ? lepTop.DeltaR(wjet1_fromHadTop->p4 + wjet2_fromHadTop->p4 + bjet_fromHadTop->p4) : -1;

      float mva_value = TMVAReader_->EvaluateMVA( "BDTG method" );
      if (mva_value > max_mva_value){
	max_mva_value = mva_value;
	best_permutation.clear();
	best_permutation.push_back(max_mva_value);
	best_permutation.push_back(bJet_fromLepTop_CSV_var);
	best_permutation.push_back(bJet_fromHadTop_CSV_var);
	best_permutation.push_back(qJet1_fromW_fromHadTop_CSV_var);
	best_permutation.push_back(HadTop_pT_var);
	best_permutation.push_back(W_fromHadTop_mass_var);
	best_permutation.push_back(HadTop_mass_var);
	best_permutation.push_back(W_fromHiggs_mass_var);
	best_permutation.push_back(LepTop_HadTop_dR_var);
      }
      
      qJet1_fromW_fromHadTop_CSV_var = wjet2_fromHadTop->csv;
      mva_value = TMVAReader_->EvaluateMVA( "BDTG method" );
      if (mva_value > max_mva_value){
	max_mva_value = mva_value;
	best_permutation.clear();
	best_permutation.push_back(max_mva_value);
	best_permutation.push_back(bJet_fromLepTop_CSV_var);
	best_permutation.push_back(bJet_fromHadTop_CSV_var);
	best_permutation.push_back(qJet1_fromW_fromHadTop_CSV_var);
	best_permutation.push_back(HadTop_pT_var);
	best_permutation.push_back(W_fromHadTop_mass_var);
	best_permutation.push_back(HadTop_mass_var);
	best_permutation.push_back(W_fromHiggs_mass_var);
	best_permutation.push_back(LepTop_HadTop_dR_var);
      }
      
    } while (std::next_permutation(_permjet,_permjet+n));
  } while (std::next_permutation(permlep.begin(),permlep.end()));

  //  std::cout << "done " << nperm << " permutation from sizes " << permjet.size() << " " << permlep.size() << std::endl;

  if (warn) std::cout << "done." << std::endl;

  delete[] _permjet;

  if (max_mva_value>-99) return best_permutation;
  else return std::vector<float>(9,-99);

};




