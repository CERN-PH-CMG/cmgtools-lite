#include <vector>
#include <string>
#include <unordered_set>
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

std::vector<float> BDTv8_eventReco::EvalMVA(){

  std::vector<int> permlep;
  for (int i=0; i<int(leps.size()); i++) permlep.push_back(i);
  std::sort(permlep.begin(),permlep.end());
  std::vector<int> permjet;
  for (int i=0; i<int(jets.size()); i++) permjet.push_back(i);
  if (permjet.size()<8) for (int i=0; i<3; i++) permjet.push_back(-1-i);
  else if (permjet.size()==8) for (int i=0; i<2; i++) permjet.push_back(-1-i);
  else permjet.push_back(-1);
  std::sort(permjet.begin(),permjet.end());

  float max_mva_value = -99;
  std::vector<float> best_permutation;
  
  std::unordered_set<std::string> done_perms;
  

  long long nperm = 0;

  do {
    do {
      if (permjet.size()<6) break;
      if (permlep.size()<2) break;
      std::string _x;
      for (auto k : permjet) {
	if (_x.size()==6) break;
	char _k = (k<0) ? -1 : k;
	_x.push_back(_k);
      }
      nperm++;
//      for (auto k : _x) std::cout << (int)k << " ";
//      std::cout << std::endl;
      if (done_perms.find(_x) != done_perms.end()) continue;
      std::string _x2; _x2.push_back((char)(permjet[3])); _x2.push_back((char)(permjet[2]));
      _x.replace(2,2,_x2);
      if (done_perms.find(_x) != done_perms.end()) continue;
      std::string _x3; _x2.push_back((char)(permjet[5])); _x2.push_back((char)(permjet[4]));
      _x.replace(4,2,_x3);
      if (done_perms.find(_x) != done_perms.end()) continue;
      done_perms.insert(_x);

      BDTv8_eventReco_Jet *bjet_fromHadTop = (permjet[0]>=0) ? jets[permjet[0]] : nulljet;
      BDTv8_eventReco_Jet *bjet_fromLepTop = (permjet[1]>=0) ? jets[permjet[1]] : nulljet;
      BDTv8_eventReco_Jet *wjet1_fromHadTop = (permjet[2]>=0) ? jets[permjet[2]] : nulljet;
      BDTv8_eventReco_Jet *wjet2_fromHadTop = (permjet[3]>=0) ? jets[permjet[3]] : nulljet;
      
      if (std::max(bjet_fromHadTop->csv,bjet_fromLepTop->csv)<0.80 && std::min(bjet_fromHadTop->csv,bjet_fromLepTop->csv)<0.46) continue;
      
      auto hadTop_W = wjet1_fromHadTop->p4 + wjet2_fromHadTop->p4;
      auto hadTop = hadTop_W + bjet_fromHadTop->p4;
      
      if (hadTop_W.M() > 120) continue;
      if (hadTop.M() > 220) continue;
      
      BDTv8_eventReco_Jet *wjet1_fromHiggs = (permjet[4]>=0) ? jets[permjet[4]] : nulljet;
      BDTv8_eventReco_Jet *wjet2_fromHiggs = (permjet[5]>=0) ? jets[permjet[5]] : nulljet;
      
      auto higgs_W = wjet1_fromHiggs->p4 + wjet2_fromHiggs->p4;
      
      BDTv8_eventReco_Lep *lep_fromTop = leps[permlep[0]];
      
      auto lepTop = lep_fromTop->p4 + bjet_fromLepTop->p4;
      
      if (lepTop.M() > 180) continue;
      
      bJet_fromLepTop_CSV_var = bjet_fromLepTop->csv;
      bJet_fromHadTop_CSV_var = bjet_fromHadTop->csv;
      qJet1_fromW_fromHadTop_CSV_var = wjet1_fromHadTop->csv;
      HadTop_pT_var = hadTop.Pt();
      W_fromHadTop_mass_var = hadTop_W.M();
      HadTop_mass_var = hadTop.M();
      W_fromHiggs_mass_var = higgs_W.M();
      LepTop_HadTop_dR_var = (hadTop.Pt()!=0) ? lepTop.DeltaR(hadTop) : -1;
      
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
      
    } while (std::next_permutation(permjet.begin(),permjet.end()));
  } while (std::next_permutation(permlep.begin(),permlep.end()));

  //  std::cout << "done " << nperm << " permutation from sizes " << permjet.size() << " " << permlep.size() << std::endl;

  if (max_mva_value>-99) return best_permutation;
  else return std::vector<float>(9,-99);

};




