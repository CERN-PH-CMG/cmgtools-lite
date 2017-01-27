#define __BMEDIUM__WORKING__POINT__ 0.8484

#include <vector>
#include <string>
#include <unordered_set>
#include <unordered_map>
#include <utility>
#include "DataFormats/Math/interface/LorentzVector.h"
#include <DataFormats/Math/interface/deltaR.h>
#include "TMVA/Reader.h"
#include <iostream>
#include "TStopwatch.h"

typedef math::PtEtaPhiMLorentzVectorD ptvec;

class BDTv8_eventReco_Obj {
 public:
  BDTv8_eventReco_Obj(){
    p4 = ptvec(0,0,0,0);
  };
  BDTv8_eventReco_Obj(float pt,float eta, float phi, float mass){
    p4 = ptvec(pt,eta,phi,mass);
  };
  ~BDTv8_eventReco_Obj(){};
  ptvec p4;
  float eta() {return p4.eta();}
  float phi() {return p4.phi();}
};

class BDTv8_eventReco_Jet : public BDTv8_eventReco_Obj {
 public:
  BDTv8_eventReco_Jet(){
    p4 = ptvec(0,0,0,0);
    csv = -0.2;
    qgl = -0.2;
  };
  BDTv8_eventReco_Jet(float pt,float eta, float phi, float mass, float _csv, float _qgl){
    p4 = ptvec(pt,eta,phi,mass);
    csv = std::max(float(-0.1),_csv);
    qgl = std::max(float(-0.1),_qgl);
  };
  ~BDTv8_eventReco_Jet(){};
  float csv;
  float qgl;
};

class BDTv8_eventReco {
 public: 
  BDTv8_eventReco(std::string weight_file_name_bloose, std::string weight_file_name_btight, std::string weight_file_name_Hj, std::string weight_file_name_Hjj){
    Init(weight_file_name_bloose,weight_file_name_btight,weight_file_name_Hj,weight_file_name_Hjj);
  };
  ~BDTv8_eventReco(){
    clear();
    delete TMVAReader_[0];
    delete TMVAReader_[1];
    delete TMVAReader_Hj_;
    delete TMVAReader_Hjj_;
    delete nulljet;
  };
  void addJet(float pt,float eta, float phi, float mass, float csv, float qgl){
    jets.push_back(new BDTv8_eventReco_Jet(pt,eta,phi,mass,csv,qgl));
    if (csv>__BMEDIUM__WORKING__POINT__) nBMedium+=1;
  };
  void addLep(float pt,float eta, float phi, float mass){
    leps.push_back(new BDTv8_eventReco_Obj(pt,eta,phi,mass));
  };
  void clear();
  void Init(std::string weight_file_name_bloose, std::string weight_file_name_btight, std::string weight_file_name_Hj, std::string weight_file_name_Hjj);
  std::vector<float> EvalMVA();

  std::vector<BDTv8_eventReco_Jet*> jets;
  std::vector<BDTv8_eventReco_Obj*> leps;
  BDTv8_eventReco_Jet* nulljet;

  float dR(BDTv8_eventReco_Obj *x, BDTv8_eventReco_Obj *y){
    return deltaR(x->eta(),x->phi(),y->eta(),y->phi());
  }

  std::pair<float,float> CalcJetComb(std::unordered_map<std::string,std::pair<float,float> > *done_jetcomb, int i1, int i2, int i3=-99);

  TMVA::Reader *TMVAReader_[2];
  TMVA::Reader *TMVAReader_Hj_, *TMVAReader_Hjj_;

  float bJet_fromLepTop_CSV_var;
  float bJet_fromHadTop_CSV_var;
  float HadTop_pT_var;
  float W_fromHadTop_mass_var;
  float HadTop_mass_var;
  float lep_ptRatio_fromTop_fromHig_var;
  float dR_lep_fromTop_bJet_fromLepTop_var;
  float dR_lep_fromTop_bJet_fromHadTop_var;
  float dR_lep_fromHig_bJet_fromLepTop_var;

  float iv1_1;
  float iv1_2;
  float iv1_3;
  float iv1_4;
  float iv1_5;

  float iv2_1;
  float iv2_2;
  float iv2_3;
  float iv2_4;
  float iv2_5;
  float iv2_6;

  int nBMedium;

  TStopwatch stopWatch;

};

void BDTv8_eventReco::Init(std::string weight_file_name_bloose, std::string weight_file_name_btight, std::string weight_file_name_Hj, std::string weight_file_name_Hjj){

  for (int i = 0; i<2; i++) {
    TMVAReader_[i] = new TMVA::Reader( "!Color:!Silent" );
  
    TMVAReader_[i]->AddVariable( "b_from_leptop_bdt.csv", &bJet_fromLepTop_CSV_var );
    TMVAReader_[i]->AddVariable( "b_from_hadtop_bdt.csv", &bJet_fromHadTop_CSV_var );
    TMVAReader_[i]->AddVariable( "hadTop_tlv_bdt.Pt()", &HadTop_pT_var );
    TMVAReader_[i]->AddVariable( "w_from_hadtop_tlv_bdt.M()", &W_fromHadTop_mass_var );
    TMVAReader_[i]->AddVariable( "hadTop_tlv_bdt.M()", &HadTop_mass_var );
    TMVAReader_[i]->AddVariable( "lep_from_leptop_bdt.obj.pt()/lep_from_higgs_bdt.obj.pt()", &lep_ptRatio_fromTop_fromHig_var );
    TMVAReader_[i]->AddVariable( "dr_lepFromTop_bFromLepTop", &dR_lep_fromTop_bJet_fromLepTop_var );
    TMVAReader_[i]->AddVariable( "dr_lepFromTop_bFromHadTop", &dR_lep_fromTop_bJet_fromHadTop_var );
    TMVAReader_[i]->AddVariable( "dr_lepFromHiggs_bFromLepTop", &dR_lep_fromHig_bJet_fromLepTop_var );
    
    TMVAReader_[i]->BookMVA("BDTG method", (i==0) ? weight_file_name_bloose : weight_file_name_btight);
  }

  TMVAReader_Hj_ = new TMVA::Reader( "!Color:!Silent" );
  TMVAReader_Hj_->AddVariable( "Jet_lepdrmin", &iv1_1);
  TMVAReader_Hj_->AddVariable( "Jet_pfCombinedInclusiveSecondaryVertexV2BJetTags", &iv1_2);
  TMVAReader_Hj_->AddVariable( "Jet_qg", &iv1_3);
  TMVAReader_Hj_->AddVariable( "Jet_lepdrmax", &iv1_4);
  TMVAReader_Hj_->AddVariable( "Jet_pt", &iv1_5);
  TMVAReader_Hj_->BookMVA("BDTG method", weight_file_name_Hj);

  TMVAReader_Hjj_ = new TMVA::Reader( "!Color:!Silent" );
  TMVAReader_Hjj_->AddVariable( "bdtJetPair_minlepmass", &iv2_1);
  TMVAReader_Hjj_->AddVariable( "bdtJetPair_sumbdt", &iv2_2);
  TMVAReader_Hjj_->AddVariable( "bdtJetPair_dr", &iv2_3);
  TMVAReader_Hjj_->AddVariable( "bdtJetPair_minjdr", &iv2_4);
  TMVAReader_Hjj_->AddVariable( "bdtJetPair_mass", &iv2_5);
  TMVAReader_Hjj_->AddVariable( "bdtJetPair_minjOvermaxjdr", &iv2_6);
  TMVAReader_Hjj_->BookMVA("BDTG method", weight_file_name_Hjj);

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
  HadTop_pT_var = -99;
  W_fromHadTop_mass_var = -99;
  HadTop_mass_var = -99;
  lep_ptRatio_fromTop_fromHig_var = -99;
  dR_lep_fromTop_bJet_fromLepTop_var = -99;
  dR_lep_fromTop_bJet_fromHadTop_var = -99;
  dR_lep_fromHig_bJet_fromLepTop_var = -99;

  iv1_1 = -99;
  iv1_2 = -99;
  iv1_3 = -99;
  iv1_4 = -99;
  iv1_5 = -99;

  iv2_1 = -99;
  iv2_2 = -99;
  iv2_3 = -99;
  iv2_4 = -99;
  iv2_5 = -99;
  iv2_6 = -99;

  nBMedium = 0;

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
  auto comb = (i3<0) ? (j1->p4+j2->p4) : (j1->p4+j2->p4+j3->p4);
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

  if (warn) stopWatch.Start();

  std::sort(permlep.begin(),permlep.end());
  std::sort(permjet.begin(),permjet.end());

  char *_permlep = NULL;
  if (permlep.size()>=2){
    _permlep = new char[permlep.size()];
    for (int i=0; i<int(permlep.size()); i++) _permlep[i]=permlep[i]+max_n_jets+10; // plus something not to confuse with jets
  }
  char *_permjet = NULL;
  if (permjet.size()>=6){
    _permjet = new char[permjet.size()];
    for (int i=0; i<int(permjet.size()); i++) _permjet[i]=permjet[i];
  }

  uint nlep = _permlep ? permlep.size() : 0;
  uint njet = _permjet ? permjet.size() : 0;

  float max_mva_value = -99;
  float max_mva_value_Hjj = -99;
  float max_mva_value_Hj = -99;

  uint nOutputVariables = 12;

  float *best_permutation = new float[nOutputVariables];
  std::fill_n(best_permutation,nOutputVariables,-99);
  
  std::unordered_map<std::string,float> done_perms;
  std::unordered_map<std::string,std::pair<float,float> > done_perms_Hj;
  std::unordered_map<std::string,std::pair<float,float> > done_jetcomb;

  do {

    BDTv8_eventReco_Obj *lep_fromTop = leps[((int)(_permlep[0]))-max_n_jets-10];
    BDTv8_eventReco_Obj *lep_fromHig = leps[((int)(_permlep[1]))-max_n_jets-10];
    
    do {

      char _xc[6];
      for (int i=0; i<6; i++) _xc[i] = (int(_permjet[i])<0) ? -1 : _permjet[i];
      std::string _x(_xc,_xc+6);

      /*

	hadTop: b-jet [0] + wjet1 [2] + wjet2 [3]
	lepTop: lep [1] + b-jet [1]
	Higgs : lep [0] + wjet [4] + wjet [5]

	// does not test if just 2/3 or 4/5 are swapped

	// top part depends only on lep[01], jet[0123]
	// higgs part depends on everything

       */

      // calculate hadTop part

      char _this_hadTop[6]={_permlep[0],_permlep[1],_x[0],_x[1],std::max(_x[2],_x[3]),std::min(_x[2],_x[3])};
      std::string this_hadTop(_this_hadTop,_this_hadTop+6);
      float this_hadTop_value = -99;

      if (done_perms.find(this_hadTop) != done_perms.end()){
	this_hadTop_value = done_perms[this_hadTop];
      }
      else {

	BDTv8_eventReco_Jet *bjet_fromHadTop = ((int)(_x[0])>=0) ? jets[(int)(_x[0])] : nulljet;
	BDTv8_eventReco_Jet *bjet_fromLepTop = ((int)(_x[1])>=0) ? jets[(int)(_x[1])] : nulljet;
	//      BDTv8_eventReco_Jet *wjet1_fromHadTop = ((int)(_x[2])>=0) ? jets[(int)(_x[2])] : nulljet;
	//      BDTv8_eventReco_Jet *wjet2_fromHadTop = ((int)(_x[3])>=0) ? jets[(int)(_x[3])] : nulljet;
      
	if (bjet_fromHadTop==nulljet && bjet_fromLepTop==nulljet) continue;
	if (nBMedium>1 && std::min(bjet_fromHadTop->csv,bjet_fromLepTop->csv)<0.8) continue;
	if (bjet_fromHadTop->csv>0 && bjet_fromHadTop->csv<0.46) continue;
	if (bjet_fromLepTop->csv>0 && bjet_fromLepTop->csv<0.46) continue;
	if (std::max(bjet_fromHadTop->csv,bjet_fromLepTop->csv)<0.80 && std::min(bjet_fromHadTop->csv,bjet_fromLepTop->csv)<0.46) continue;

	auto hadTop_W = CalcJetComb(&done_jetcomb,_x[2],_x[3]);
	auto hadTop = CalcJetComb(&done_jetcomb,_x[2],_x[3],_x[0]);

	if (hadTop_W.second > 120) continue;
	if (hadTop.second > 220) continue;

	auto lepTop = lep_fromTop->p4 + bjet_fromLepTop->p4;
	if (lepTop.M() > 180) continue;

	bJet_fromLepTop_CSV_var = bjet_fromLepTop->csv;
	bJet_fromHadTop_CSV_var = bjet_fromHadTop->csv;
	HadTop_pT_var = hadTop.first;
	W_fromHadTop_mass_var = hadTop_W.second;
	HadTop_mass_var = hadTop.second;
	lep_ptRatio_fromTop_fromHig_var = lep_fromTop->p4.Pt()/lep_fromHig->p4.Pt();
	dR_lep_fromTop_bJet_fromLepTop_var = (bjet_fromLepTop != nulljet) ? dR(lep_fromTop,bjet_fromLepTop) : -1;
	dR_lep_fromTop_bJet_fromHadTop_var = (bjet_fromHadTop != nulljet) ? dR(lep_fromTop,bjet_fromHadTop) : -1;
	dR_lep_fromHig_bJet_fromLepTop_var = (bjet_fromLepTop != nulljet) ? dR(lep_fromHig,bjet_fromLepTop) : -1;

	this_hadTop_value = TMVAReader_[(nBMedium>1)]->EvaluateMVA( "BDTG method" );
      	done_perms[this_hadTop] = this_hadTop_value;

      }

      if (this_hadTop_value >= max_mva_value){

	max_mva_value = this_hadTop_value;

	best_permutation[0] = max_mva_value;
	best_permutation[1] = bJet_fromLepTop_CSV_var;
	best_permutation[2] = bJet_fromHadTop_CSV_var;
	best_permutation[3] = HadTop_pT_var;
	best_permutation[4] = W_fromHadTop_mass_var;
	best_permutation[5] = HadTop_mass_var;
	best_permutation[6] = lep_ptRatio_fromTop_fromHig_var;
	best_permutation[7] = dR_lep_fromTop_bJet_fromLepTop_var;
	best_permutation[8] = dR_lep_fromTop_bJet_fromHadTop_var;
	best_permutation[9] = dR_lep_fromHig_bJet_fromLepTop_var;
	

	char _this_Hj[4]={_permlep[0],_permlep[1],std::max(_x[4],_x[5]),std::min(_x[4],_x[5])};
	std::string this_Hj(_this_Hj,_this_Hj+4);
	std::pair<float,float> this_Hj_values =  std::pair<float,float>(-99,-99);

	if (done_perms_Hj.find(this_Hj) != done_perms_Hj.end()){
	  this_Hj_values = done_perms_Hj[this_Hj];
	}
	else {

	  /////////// Higgs tagger

	  BDTv8_eventReco_Jet *wjet1_fromHiggs = ((int)(_x[4])>=0) ? jets[(int)(_x[4])] : nulljet;
	  BDTv8_eventReco_Jet *wjet2_fromHiggs = ((int)(_x[5])>=0) ? jets[(int)(_x[5])] : nulljet;
	  auto higgs_W = CalcJetComb(&done_jetcomb,_x[4],_x[5]);

	  float Hj_value[2] = {-99,-99};
	  float Hjj_value = -99;
      
	  for (int i=0; i<2; i++){
	    auto jet_fromHiggs = (i==0) ? wjet1_fromHiggs : wjet2_fromHiggs;
	    if (jet_fromHiggs==nulljet) continue;
	
	    float dr_lep0 = dR(lep_fromTop,jet_fromHiggs);
	    float dr_lep1 = dR(lep_fromHig,jet_fromHiggs);
	
	    iv1_1 = std::min(dr_lep0,dr_lep1);
	    iv1_2 = jet_fromHiggs->csv;
	    iv1_3 = jet_fromHiggs->qgl;
	    iv1_4 = std::max(dr_lep0,dr_lep1);
	    iv1_5 = jet_fromHiggs->p4.Pt();
	
	    Hj_value[i] = TMVAReader_Hj_->EvaluateMVA("BDTG method");
	
	  }

	  if (wjet1_fromHiggs!=nulljet && wjet2_fromHiggs!=nulljet){
	    auto jj = (wjet1_fromHiggs->p4+wjet2_fromHiggs->p4);
	    iv2_1 = std::min((jj+lep_fromTop->p4).M(),(jj+lep_fromHig->p4).M());
	    iv2_2 = Hj_value[0]+Hj_value[1];
	    iv2_3 = dR(wjet1_fromHiggs,wjet2_fromHiggs);
	    std::vector<float> drs;
	    for (auto i : permjet) {
	      if (i<0) continue;
	      if (i==(int)(_x[4]) || i==(int)(_x[5])) continue;
	      drs.push_back(deltaR(jj.eta(),jj.phi(),jets[i]->eta(),jets[i]->phi()));
	    }
	    std::sort(drs.begin(),drs.end());
	    iv2_4 = drs.at(0);
	    iv2_5 = higgs_W.second;
	    iv2_6 = drs.at(0)/drs.at(drs.size()-1);
	
	    Hjj_value = TMVAReader_Hjj_->EvaluateMVA("BDTG method");
	  }

	  this_Hj_values =  std::pair<float,float>(std::max(Hj_value[0],Hj_value[1]),Hjj_value);
	  done_perms_Hj[this_Hj] = this_Hj_values;

	}

	max_mva_value_Hj = std::max(this_Hj_values.first,max_mva_value_Hj);
	max_mva_value_Hjj = std::max(this_Hj_values.second,max_mva_value_Hjj);

	best_permutation[10] = max_mva_value_Hj;
	best_permutation[11] = max_mva_value_Hjj;

      }
     
    } while (std::next_permutation(_permjet,_permjet+njet));
  } while (std::next_permutation(_permlep,_permlep+nlep));
  
  if (warn) std::cout << "done in " << stopWatch.RealTime() << " s" << std::endl;

  if (_permlep) delete[] _permlep;
  if (_permjet) delete[] _permjet;

  std::vector<float> output;
  output.assign(best_permutation,best_permutation+nOutputVariables);
  delete[] best_permutation;
  return output;

};




