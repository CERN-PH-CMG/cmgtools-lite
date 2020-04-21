#include "CommonTools/MVAUtils/interface/TMVAZipReader.h"
#include <tuple>
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
#include "TMath.h"
#include <algorithm>


enum BDT_EventReco_algoType {
  k_BDTv8_Hj = 0,
  k_rTT_Hj = 1,
  k_httTT_Hj = 2,
};

typedef math::PtEtaPhiMLorentzVectorD ptvec;
typedef ptvec BDT_EventReco_Obj;

//class BDT_EventReco_Obj : public ptvec {
// public:
//  BDT_EventReco_Obj() : ptvec(0,0,0,0){};
//  BDT_EventReco_Obj(ptvec x) : ptvec(x){};
//  BDT_EventReco_Obj(float pt,float eta, float phi, float mass) : ptvec(pt,eta,phi,mass){};
//  ptvec p4(){return *(dynamic_cast<ptvec*>(this));}
//};

typedef BDT_EventReco_Obj eObj;
typedef std::shared_ptr<BDT_EventReco_Obj> eObjP;

class BDT_EventReco_Jet : public eObj {
 public:
  BDT_EventReco_Jet() : eObj(0,0,0,0) {
    _csv = -0.2;
    _qgl = -0.2;
  };
  BDT_EventReco_Jet(float pt,float eta, float phi, float mass, float csv, float deepcsv, float deepjet, float cvsl, float cvsb, float ptD, float axis1, int mult, float qgl): eObj(pt,eta,phi,mass),
																					      _deepcsv(deepcsv), _deepjet(deepjet), _cvsl(cvsl), _cvsb(cvsb), _ptD(ptD), _axis1(std::exp(-axis1)), _mult(mult) {
  // pass axis1 = -log(sqrt(...)), training uses definition of axis1 without -log
    _csv = std::max(float(-0.1),csv);
    _qgl = std::max(float(-0.1),qgl);
  };
  ~BDT_EventReco_Jet(){};
  float csv() const {return _csv;}
  float deepcsv() const {return _deepcsv;}
  float deepjet() const {return _deepjet;}
  float cvsl() const {return _cvsl;}
  float cvsb() const {return _cvsb;}
  float ptD() const {return _ptD;}
  float axis1() const {return _axis1;}
  int mult() const {return _mult;}
  float qgl() const {return _qgl;}
  const ptvec* p4() const {return dynamic_cast<const ptvec*>(this);}
 private:
  float _csv;
  float _deepcsv = 0;
  float _deepjet = 0;
  float _cvsl = 0;
  float _cvsb = 0;
  float _ptD = 0;
  float _axis1 = 0;
  int _mult = 0;
  float _qgl;
};

typedef BDT_EventReco_Jet eJet;
typedef std::shared_ptr<BDT_EventReco_Jet> eJetP;

class BDT_EventReco_Top {
public:
  BDT_EventReco_Top(){};

  BDT_EventReco_Top(eObjP _p4w, eObjP _p4, eJetP _b, eJetP _j2, eJetP _j3, int _j1idx, int _j2idx, int _j3idx, bool _hasScore_rTT, float _score_rTT): p4w(_p4w), p4(_p4), b(_b), j2(_j2), j3(_j3), j1idx(_j1idx), j2idx(_j2idx), j3idx(_j3idx), hasScore_rTT(_hasScore_rTT), score_rTT(_score_rTT){};

  eObjP p4w = nullptr;
  eObjP p4 = nullptr;
  eJetP b = nullptr;
  eJetP j2 = nullptr;
  eJetP j3 = nullptr;
  int j1idx = -99;
  int j2idx = -99;
  int j3idx = -99;
  bool hasScore_rTT = false;
  float score_rTT = -99;
  bool hasScore_httTT = false;
  float score_httTT = -99;
  int jetIndxMask = (1 << j1idx) | (1<< j2idx) | (1 << j3idx); // only for events with up to 32 jets 
};

typedef BDT_EventReco_Top eTop;
typedef std::shared_ptr<BDT_EventReco_Top> eTopP;

class BDT_EventReco_EventP4Cache {
 public:
  BDT_EventReco_EventP4Cache(std::vector<eJetP > *_jets, eJetP *_nulljet):
    jets(_jets), nulljet(_nulljet){};

  eObjP getSum(int i1, int i2){
    char _xc[2] = {(char)i1,(char)i2};
    std::sort(_xc,_xc+2); // no ordering kept
    std::string _x(_xc,_xc+2);
    auto it = paircache.find(_x);
    if (it==paircache.end()){
      auto o = std::make_shared<eObj>(*(getJet(i1).get()->p4())+*(getJet(i2).get()->p4()));
      paircache[_x] = o;
      return o;
    }
    else return (*it).second;
  };

  eObjP getSum(int i1, int i2, int i3){
    char _xc[3] = {(char)i1,(char)i2,(char)i3};
    std::sort(_xc,_xc+3); // no ordering kept
    std::string _x(_xc,_xc+3);
    auto it = triplecache.find(_x);
    if (it==triplecache.end()){
      auto o = std::make_shared<eObj>(*(getJet(i1).get()->p4())+*(getSum(i2,i3).get()));
      triplecache[_x] = o;
      return o;
    }
    else return (*it).second;
  };

  eTopP getTop(int i1, int i2, int i3){
    char _xc[3] = {(char)i1,(char)i2,(char)i3};
    std::string _x(_xc,_xc+3); // ordering kept
    auto it = topcache.find(_x);
    if (it==topcache.end()){
      auto o = std::make_shared<eTop>(getSum(i2,i3),getSum(i1,i2,i3),getJet(i1),getJet(i2),getJet(i3),i1,i2,i3,false,-99);
      topcache[_x] = o;
      return o;
    }
    else return (*it).second;
  };

  void clear(){paircache.clear(); triplecache.clear(); topcache.clear();};

  eJetP getJet(int i){if (i<0) return *nulljet; else return jets->at(i);}

  int getPairSize(){return paircache.size();}
  int getTripleSize(){return triplecache.size();}
  int getTopSize(){return topcache.size();}


 private:
  std::unordered_map<std::string, eObjP > paircache;
  std::unordered_map<std::string, eObjP > triplecache;
  std::unordered_map<std::string, eTopP > topcache;
  std::vector<eJetP > *jets = nullptr;
  eJetP *nulljet = nullptr;
};


class BDT_EventReco {
 public: 
  BDT_EventReco(std::string weight_file_name_bloose, std::string weight_file_name_btight, std::string weight_file_name_Hj, bool hj2017, bool hjlegacy, std::string weight_file_name_Hjj, std::string weight_file_name_rTT, std::string weight_file_name_httTT, std::string kinfit_file_name_httTT, BDT_EventReco_algoType _algo, float csv_looseWP, float csv_mediumWP);
  ~BDT_EventReco(){
    clear();
  };
  void addJet(float pt,float eta, float phi, float mass, float csv, float deepcsv, float deepjet, float cvsl, float cvsb, float ptD, float axis1, int mult, float qgl){
    jets.push_back(std::make_shared<eJet>(pt,eta,phi,mass,csv,deepcsv, deepjet,cvsl,cvsb,ptD,axis1,mult,qgl));
    if (csv>csv_medium_working_point) nBMedium+=1;
  };
  void addLep(float pt,float eta, float phi, float mass){
    leps.push_back(std::make_shared<eObj>(pt,eta,phi,mass));
  };
  void clear();
  std::vector<float> EvalMVA();
  std::vector<float> CalcHadTopTagger(char* _permlep, char* _x);
  std::vector<float> CalcHjTagger(char* _permlep, char* _x, std::vector<int> &permjet);
  std::vector<float> CalcrTT(char* _x);
  float EvalScore(eTopP top);
  float EvalScore_httTT(eTopP top);
  // std::tuple<float,float> EvalKinFit(eTopP top);

  void setDebug(bool val){debug = val;};

  std::vector<eJetP > jets;
  std::vector<eObjP > leps;
  eJetP nulljet = std::make_shared<eJet>();
  std::shared_ptr<BDT_EventReco_EventP4Cache> cache = std::make_shared<BDT_EventReco_EventP4Cache>(&jets,&nulljet);


  float dR(const ptvec *x, const ptvec *y){
    return deltaR(x->eta(),x->phi(),y->eta(),y->phi());
  }

  std::shared_ptr<TMVA::Reader> TMVAReader_[2];
  std::shared_ptr<TMVA::Reader> TMVAReader_Hj_, TMVAReader_Hjj_;
  std::shared_ptr<TMVA::Reader> TMVAReader_rTT_ = nullptr;
  std::shared_ptr<TMVA::Reader> TMVAReader_httTT_ = nullptr;

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

  float var_b_pt = -99;
  float var_b_mass = -99;
  float var_b_ptD = -99;
  float var_b_axis1 = -99;
  float var_b_mult = -99;
  float var_b_csv = -99;
  float var_b_cvsb = -99;
  float var_b_cvsl = -99;

  float var_wj1_pt = -99;
  float var_wj1_mass = -99;
  float var_wj1_ptD = -99;
  float var_wj1_axis1 = -99;
  float var_wj1_mult = -99;
  float var_wj1_csv = -99;
  float var_wj1_cvsb = -99;
  float var_wj1_cvsl = -99;

  float var_wj2_pt = -99;
  float var_wj2_mass = -99;
  float var_wj2_ptD = -99;
  float var_wj2_axis1 = -99;
  float var_wj2_mult = -99;
  float var_wj2_csv = -99;
  float var_wj2_cvsb = -99;
  float var_wj2_cvsl = -99;

  float var_b_wj1_deltaR = -99;
  float var_b_wj1_mass = -99;
  float var_b_wj2_deltaR = -99;
  float var_b_wj2_mass = -99;
  float var_wcand_deltaR = -99;
  float var_wcand_mass = -99;
  float var_b_wcand_deltaR = -99;
  float var_topcand_mass = -99;

  float var_httTT_btagDisc_b             = -99;   
  float var_httTT_btagDisc_Wj1 		 = -99;
  float var_httTT_btagDisc_Wj2		 = -99;
  float var_httTT_qg_Wj1   		 = -99;
  float var_httTT_qg_Wj2        	 = -99;
  float var_httTT_m_bWj1Wj2   		 = -99;
  float var_httTT_m_Wj1Wj2_div_m_bWj1Wj2 = -99;
  float var_httTT_pT_Wj1Wj2		 = -99;
  float var_httTT_dR_Wj1Wj2		 = -99;
  float var_httTT_dR_bW			 = -99;
  float var_httTT_m_bWj1    		 = -99;
  float var_httTT_m_bWj2    		 = -99;
  float var_httTT_mass_Wj1		 = -99;
  float var_httTT_pT_Wj2	         = -99;
  float var_httTT_mass_Wj2		 = -99;
  float var_httTT_pT_b			 = -99;
  float var_httTT_mass_b                 = -99;   
 
  //HadTopKinFit *httTT_kinfitWorker = nullptr;
  ptvec httTT_kinfit_recBJet;
  ptvec httTT_kinfit_recWJet1;
  ptvec httTT_kinfit_recWJet2;

  int nBMedium;

  bool debug = false;
  TStopwatch stopWatch;

  std::unordered_map<std::string,float> done_perms;
  std::unordered_map<std::string,std::pair<float,float> > done_perms_Hj;

  BDT_EventReco_algoType algo;
  const uint warn_n_jets = 10;
  const uint max_n_jets = 11;
  const uint nOutputVariablesHadTop = 20;
  const uint nOutputVariablesHig = 4;
  const uint nOutputVariablesrTT = 16;
  const uint nOutputVariableshttTT = 6;
  uint expected_size = 0;

  float csv_loose_working_point = -1;
  float csv_medium_working_point = -1;
  bool hj2017training = false;
  bool hjLegacyTraining = false;
};

BDT_EventReco::BDT_EventReco(std::string weight_file_name_bloose, std::string weight_file_name_btight, std::string weight_file_name_Hj, bool hj2017, bool hjlegacy, std::string weight_file_name_Hjj, std::string weight_file_name_rTT, std::string weight_file_name_httTT, std::string kinfit_file_name_httTT, BDT_EventReco_algoType _algo, float csv_looseWP, float csv_mediumWP){

  algo = _algo;
  csv_loose_working_point = csv_looseWP;
  csv_medium_working_point = csv_mediumWP;
  hj2017training = hj2017;
  hjLegacyTraining = hjlegacy;

  if (algo==k_BDTv8_Hj) {

  for (int i = 0; i<2; i++) {
    TMVAReader_[i] = std::make_shared<TMVA::Reader>( "!Color:!Silent" );
  
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

  }

  TMVAReader_Hj_ = std::make_shared<TMVA::Reader>( "!Color:!Silent" );
  if (hjLegacyTraining) {
      TMVAReader_Hj_->AddVariable( "Jet25_bDiscriminator", &iv1_2);
      TMVAReader_Hj_->AddVariable( "Jet25_pt", &iv1_5);
      TMVAReader_Hj_->AddVariable( "Jet25_lepdrmin", &iv1_1);
      TMVAReader_Hj_->AddVariable( "Jet25_lepdrmax", &iv1_4);
      TMVAReader_Hj_->AddVariable( "Jet25_qg", &iv1_3);
  }
  else if (hj2017training) {
      TMVAReader_Hj_->AddVariable( "Jet25_lepdrmin", &iv1_1);
      TMVAReader_Hj_->AddVariable( "max(Jet25_bDiscriminator,0.)", &iv1_2);
      TMVAReader_Hj_->AddVariable( "max(Jet25_qg,0.)", &iv1_3);
      TMVAReader_Hj_->AddVariable( "Jet25_lepdrmax", &iv1_4);
      TMVAReader_Hj_->AddVariable( "Jet25_pt", &iv1_5);
  } else {
      TMVAReader_Hj_->AddVariable( "Jet_lepdrmin", &iv1_1);
      TMVAReader_Hj_->AddVariable( "max(Jet_pfCombinedInclusiveSecondaryVertexV2BJetTags,0.)", &iv1_2);
      TMVAReader_Hj_->AddVariable( "max(Jet_qg,0.)", &iv1_3);
      TMVAReader_Hj_->AddVariable( "Jet_lepdrmax", &iv1_4);
      TMVAReader_Hj_->AddVariable( "Jet_pt", &iv1_5);
  }
  TMVAReader_Hj_->BookMVA("BDTG method", weight_file_name_Hj);

  TMVAReader_Hjj_ = std::make_shared<TMVA::Reader>( "!Color:!Silent" );
  TMVAReader_Hjj_->AddVariable( "bdtJetPair_minlepmass", &iv2_1);
  TMVAReader_Hjj_->AddVariable( "bdtJetPair_sumbdt", &iv2_2);
  TMVAReader_Hjj_->AddVariable( "bdtJetPair_dr", &iv2_3);
  TMVAReader_Hjj_->AddVariable( "bdtJetPair_minjdr", &iv2_4);
  TMVAReader_Hjj_->AddVariable( "bdtJetPair_mass", &iv2_5);
  TMVAReader_Hjj_->AddVariable( "bdtJetPair_minjOvermaxjdr", &iv2_6);
  TMVAReader_Hjj_->BookMVA("BDTG method", weight_file_name_Hjj);

  if (algo==k_rTT_Hj) {

  TMVAReader_rTT_ = std::make_shared<TMVA::Reader>( "!Color:!Silent" );

  TMVAReader_rTT_->AddVariable("var_b_pt",&var_b_pt);
  TMVAReader_rTT_->AddVariable("var_b_mass",&var_b_mass);
  TMVAReader_rTT_->AddVariable("var_b_ptD",&var_b_ptD);
  TMVAReader_rTT_->AddVariable("var_b_axis1",&var_b_axis1);
  TMVAReader_rTT_->AddVariable("var_b_mult",&var_b_mult);
  TMVAReader_rTT_->AddVariable("var_b_deepcsv_bvsall",&var_b_csv);
  TMVAReader_rTT_->AddVariable("var_b_deepcsv_cvsb",&var_b_cvsb);
  TMVAReader_rTT_->AddVariable("var_b_deepcsv_cvsl",&var_b_cvsl);

  TMVAReader_rTT_->AddVariable("var_wj1_pt",&var_wj1_pt);
  TMVAReader_rTT_->AddVariable("var_wj1_mass",&var_wj1_mass);
  TMVAReader_rTT_->AddVariable("var_wj1_ptD",&var_wj1_ptD);
  TMVAReader_rTT_->AddVariable("var_wj1_axis1",&var_wj1_axis1);
  TMVAReader_rTT_->AddVariable("var_wj1_mult",&var_wj1_mult);
  TMVAReader_rTT_->AddVariable("var_wj1_deepcsv_bvsall",&var_wj1_csv);
  TMVAReader_rTT_->AddVariable("var_wj1_deepcsv_cvsb",&var_wj1_cvsb);
  TMVAReader_rTT_->AddVariable("var_wj1_deepcsv_cvsl",&var_wj1_cvsl);

  TMVAReader_rTT_->AddVariable("var_wj2_pt",&var_wj2_pt);
  TMVAReader_rTT_->AddVariable("var_wj2_mass",&var_wj2_mass);
  TMVAReader_rTT_->AddVariable("var_wj2_ptD",&var_wj2_ptD);
  TMVAReader_rTT_->AddVariable("var_wj2_axis1",&var_wj2_axis1);
  TMVAReader_rTT_->AddVariable("var_wj2_mult",&var_wj2_mult);
  TMVAReader_rTT_->AddVariable("var_wj2_deepcsv_bvsall",&var_wj2_csv);
  TMVAReader_rTT_->AddVariable("var_wj2_deepcsv_cvsb",&var_wj2_cvsb);
  TMVAReader_rTT_->AddVariable("var_wj2_deepcsv_cvsl",&var_wj2_cvsl);

  TMVAReader_rTT_->AddVariable("var_b_wj1_deltaR",&var_b_wj1_deltaR);
  TMVAReader_rTT_->AddVariable("var_b_wj1_mass",&var_b_wj1_mass);
  TMVAReader_rTT_->AddVariable("var_b_wj2_deltaR",&var_b_wj2_deltaR);
  TMVAReader_rTT_->AddVariable("var_b_wj2_mass",&var_b_wj2_mass);
  TMVAReader_rTT_->AddVariable("var_wcand_deltaR",&var_wcand_deltaR);
  TMVAReader_rTT_->AddVariable("var_wcand_mass",&var_wcand_mass);
  TMVAReader_rTT_->AddVariable("var_b_wcand_deltaR",&var_b_wcand_deltaR);
  TMVAReader_rTT_->AddVariable("var_topcand_mass",&var_topcand_mass);

  reco::details::loadTMVAWeights(TMVAReader_rTT_.get(),"BDT",weight_file_name_rTT);

  }

  if (algo==k_httTT_Hj) {

    TMVAReader_httTT_ = std::make_shared<TMVA::Reader>( "!Color:!Silent" );

    TMVAReader_httTT_->AddVariable("btagDisc_b",            &var_httTT_btagDisc_b            );	
    TMVAReader_httTT_->AddVariable("btagDisc_Wj1",	  &var_httTT_btagDisc_Wj1 	   );	
    TMVAReader_httTT_->AddVariable("btagDisc_Wj2",	  &var_httTT_btagDisc_Wj2	   );	
    TMVAReader_httTT_->AddVariable("qg_Wj1",		  &var_httTT_qg_Wj1   		   );
    TMVAReader_httTT_->AddVariable("qg_Wj2",		  &var_httTT_qg_Wj2        	   );
    TMVAReader_httTT_->AddVariable("m_Wj1Wj2_div_m_bWj1Wj2", &var_httTT_m_Wj1Wj2_div_m_bWj1Wj2);
    TMVAReader_httTT_->AddVariable("pT_Wj1Wj2",		  &var_httTT_pT_Wj1Wj2		   );
    TMVAReader_httTT_->AddVariable("dR_Wj1Wj2",		  &var_httTT_dR_Wj1Wj2		   );
    TMVAReader_httTT_->AddVariable("m_bWj1Wj2",		  &var_httTT_m_bWj1Wj2   	   );	
    TMVAReader_httTT_->AddVariable("dR_bW",		  &var_httTT_dR_bW		   );	
    TMVAReader_httTT_->AddVariable("m_bWj1",		  &var_httTT_m_bWj1    		   );
    TMVAReader_httTT_->AddVariable("m_bWj2",		  &var_httTT_m_bWj2    		   );
    TMVAReader_httTT_->AddVariable("mass_Wj1",		  &var_httTT_mass_Wj1		   );
    TMVAReader_httTT_->AddVariable("pT_Wj2",		  &var_httTT_pT_Wj2	           );
    TMVAReader_httTT_->AddVariable("mass_Wj2",		  &var_httTT_mass_Wj2		   );
    TMVAReader_httTT_->AddVariable("pT_b",		  &var_httTT_pT_b		   );	
    TMVAReader_httTT_->AddVariable("mass_b",		  &var_httTT_mass_b                );

  
    reco::details::loadTMVAWeights(TMVAReader_httTT_.get(),"BDT",weight_file_name_httTT);

    // httTT_kinfitWorker = new HadTopKinFit(1,kinfit_file_name_httTT);

  }

  clear();

  expected_size = (algo==k_BDTv8_Hj)*nOutputVariablesHadTop+(algo==k_rTT_Hj)*nOutputVariablesrTT+(algo==k_httTT_Hj)*nOutputVariableshttTT+nOutputVariablesHig;

};

void BDT_EventReco::clear(){

  jets.clear();
  leps.clear();
  cache->clear();

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

  var_b_pt = -99;
  var_b_mass = -99;
  var_b_ptD = -99;
  var_b_axis1 = -99;
  var_b_mult = -99;
  var_b_csv = -99;
  var_b_cvsb = -99;
  var_b_cvsl = -99;

  var_wj1_pt = -99;
  var_wj1_mass = -99;
  var_wj1_ptD = -99;
  var_wj1_axis1 = -99;
  var_wj1_mult = -99;
  var_wj1_csv = -99;
  var_wj1_cvsb = -99;
  var_wj1_cvsl = -99;

  var_wj2_pt = -99;
  var_wj2_mass = -99;
  var_wj2_ptD = -99;
  var_wj2_axis1 = -99;
  var_wj2_mult = -99;
  var_wj2_csv = -99;
  var_wj2_cvsb = -99;
  var_wj2_cvsl = -99;

  var_b_wj1_deltaR = -99;
  var_b_wj1_mass = -99;
  var_b_wj2_deltaR = -99;
  var_b_wj2_mass = -99;
  var_wcand_deltaR = -99;
  var_wcand_mass = -99;
  var_b_wcand_deltaR = -99;
  var_topcand_mass = -99;

  var_httTT_btagDisc_b             = -99;   
  var_httTT_btagDisc_Wj1 	   = -99;	  
  var_httTT_btagDisc_Wj2	   = -99;	  
  var_httTT_qg_Wj1   		   = -99;	  
  var_httTT_qg_Wj2                 = -99;	  
  var_httTT_m_bWj1Wj2   	   = -99;	  
  var_httTT_m_Wj1Wj2_div_m_bWj1Wj2 = -99;	  
  var_httTT_pT_Wj1Wj2		   = -99;	  
  var_httTT_dR_Wj1Wj2		   = -99;	  
  var_httTT_dR_bW		   = -99;	  
  var_httTT_m_bWj1    		   = -99;	  
  var_httTT_m_bWj2    		   = -99;	  
  var_httTT_mass_Wj1		   = -99;	  
  var_httTT_pT_Wj2	           = -99;	  
  var_httTT_mass_Wj2		   = -99;	  
  var_httTT_pT_b		   = -99;	  
  var_httTT_mass_b                 = -99;   

  nBMedium = 0;

  done_perms.clear();
  done_perms_Hj.clear();

}

std::vector<float> BDT_EventReco::EvalMVA(){

  std::vector<int> permlep;
  for (int i=0; i<int(leps.size()); i++) permlep.push_back(i);
  std::vector<int> permjet;
  for (int i=0; i<int(jets.size()); i++) permjet.push_back(i);

  bool warn = false;

  if (algo==k_BDTv8_Hj) {
    
    if (permjet.size()<8) for (int i=0; i<3; i++) permjet.push_back(-1-i);
    else if (permjet.size()==8) for (int i=0; i<2; i++) permjet.push_back(-1-i);
    else permjet.push_back(-1);
    
    if (permjet.size()>=warn_n_jets && permlep.size()>=2) {
      std::cout << "Warning: large number of jets: " << permjet.size() << " (" << jets.size() << " non-null) ... " ;
      warn = true;
    }
    if (permjet.size()>max_n_jets && permlep.size()>=2){
      std::cout << "Warning: large number of jets, cropped to " << max_n_jets << " ... " ;
      permjet.resize(max_n_jets);
      warn = true;
    }

  }
  else if (algo==k_rTT_Hj || algo==k_httTT_Hj) {
    while (permjet.size()<6) permjet.push_back(-1-(permjet.size()-jets.size()));
    if (jets.size()>8) warn = true;
    if (permjet.size()>max_n_jets-1) { // allow 1 jet less in this case (careful max_n_jets is also used for coding elsewhere!)
      std::cout << "Warning: large number of jets, cropped to " << max_n_jets-1 << " ... " ;
      permjet.resize(max_n_jets-1);
      warn = true;
    }
    else if (warn) std::cout << "Processing event with " << jets.size() << " jets ... ";
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

  std::vector<float> best_permutation_hadTop(nOutputVariablesHadTop,-99);
  std::vector<float> best_permutation_Hj(nOutputVariablesHig,-99);
  std::vector<float> best_permutation_Hjj(nOutputVariablesHig,-99);
  eTopP best_permutation_rTT = nullptr;
  eTopP best_permutation_httTT = nullptr;

  uint n_tested_permutations = 0;

  bool go = true;
  float top_tag = -99;

  do {
    
    char _x[6];
    for (int i=0; i<6; i++) _x[i] = (int(_permjet[i])<0) ? -1 : _permjet[i];

    /*
      
      hadTop: b-jet [0] + wjet1 [2] + wjet2 [3]
      lepTop: lep [1] + b-jet [1]
      Higgs : lep [0] + wjet [4] + wjet [5]
      
      // does not test if just 2/3 or 4/5 are swapped
      
      // top part depends only on lep[0], lep[1], jet[0], jet[1], jet[23]
      // higgs part depends on lep[0], lep[1], jet[45]
      
      */
    
    
    
    if ((int)(_x[0])<0 || (int)(_x[2])<0 || (int)(_x[3])<0) continue;
        
    n_tested_permutations++;
    
    auto topcand = cache->getTop(_x[0],_x[2],_x[3]);
    float score = EvalScore_httTT(topcand);
    if (!best_permutation_httTT || (score > best_permutation_httTT->score_httTT)) {
      best_permutation_httTT = topcand;
      top_tag = score;
    }
      
  } while (go && std::next_permutation(_permjet,_permjet+njet));

  // cleanup
  if (_permjet) delete[] _permjet;

  // now go into Hj tagger
  _permjet = NULL;
  if (permjet.size()>=6){
    _permjet = new char[permjet.size()];
    for (int i=0; i<int(permjet.size()); i++) _permjet[i]=permjet[i];
  }
  
  do { 
    do {

      char _x[6];
      for (int i=0; i<6; i++) _x[i] = (int(_permjet[i])<0) ? -1 : _permjet[i];
      if (top_tag >= 0 && !( (best_permutation_httTT->jetIndxMask & (1 << _x[0])) && (best_permutation_httTT->jetIndxMask & (1 << _x[1])) && (best_permutation_httTT->jetIndxMask & (1 << _x[2]))))
	continue; // skip if the HTT has been computed and the three jets of the best top are not the three first in this permutation 
      std::vector<float> Hj = CalcHjTagger(_permlep,_x,permjet);
      if (Hj[0]>best_permutation_Hj[0]){
	assert(Hj.size()>1);
	best_permutation_Hj = Hj;
      }
      if (Hj[1]>best_permutation_Hjj[1]){
	assert(Hj.size()>1);
	best_permutation_Hjj = Hj;
      }
    } while (go && std::next_permutation(_permjet,_permjet+njet));
  } while (go && std::next_permutation(_permlep,_permlep+nlep));



  if (warn) std::cout << "tested " << n_tested_permutations << " permutations, done in " << stopWatch.RealTime() << " s" << std::endl;

  if (_permlep) delete[] _permlep;

  std::vector<float> output;

  if (algo==k_BDTv8_Hj) output = best_permutation_hadTop;
  else if (algo==k_rTT_Hj) {
    output.resize(nOutputVariablesrTT,-99);
    if (best_permutation_rTT) {
      auto top = best_permutation_rTT;
      output.at(0) = top->score_rTT; // mvaValue
      output.at(1) = top->p4->pt(); // HadTop_pt
      output.at(2) = top->p4->eta(); // HadTop_eta
      output.at(3) = top->p4->phi(); // HadTop_phi
      output.at(4) = top->p4->mass(); // HadTop_mass
      output.at(5) = top->p4w->pt(); // W_fromHadTop_pt
      output.at(6) = top->p4w->eta(); // W_fromHadTop_eta
      output.at(7) = top->p4w->phi(); // W_fromHadTop_phi
      output.at(8) = top->p4w->mass(); // W_fromHadTop_mass
      output.at(9) = std::max(top->j2->deepcsv(),top->j3->deepcsv()); // W_fromHadTop_maxCSVjj
      output.at(10) = dR(top->j2.get(),top->j3.get()); // W_fromHadTop_dRjj
      output.at(11) = dR(top->b.get(),top->p4w.get()); // W_fromHadTop_dRb
      output.at(12) = top->b->deepcsv(); // b_fromHadTop_CSV
      output.at(13) = top->j1idx;
      output.at(14) = top->j2idx;
      output.at(15) = top->j3idx;
    }
  }
  else if (algo==k_httTT_Hj) {
    output.resize(nOutputVariableshttTT,-99);
    if (best_permutation_httTT) {
      auto top = best_permutation_httTT;
      output.at(0) = top->score_httTT; // mvaValue
      output.at(1) = top->p4->pt(); // HadTop_pt
      output.at(2) = top->p4->mass(); // HadTop_mass
      output.at(3) = top->j1idx;
      output.at(4) = top->j2idx;
      output.at(5) = top->j3idx;
    }
  }
  output.push_back(best_permutation_Hj[0]);
  output.insert(output.end(),best_permutation_Hjj.begin()+1,best_permutation_Hjj.end());
  if (output.size()!=expected_size) std::cout << "ERROR: mismatch in output vector size: " << output.size() << " " << expected_size << std::endl;
  return output;

};

float BDT_EventReco::EvalScore(eTopP top){

  if (top->hasScore_rTT) return top->score_rTT;

  var_b_pt = top->b->pt();
  var_b_mass = top->b->mass();
  var_b_ptD = top->b->ptD();
  var_b_axis1 = top->b->axis1();
  var_b_mult = top->b->mult();
  var_b_csv = top->b->deepcsv();
  var_b_cvsb = top->b->cvsb();
  var_b_cvsl = top->b->cvsl();

  var_wj1_pt = top->j2->pt();
  var_wj1_mass = top->j2->mass();
  var_wj1_ptD = top->j2->ptD();
  var_wj1_axis1 = top->j2->axis1();
  var_wj1_mult = top->j2->mult();
  var_wj1_csv = top->j2->deepcsv();
  var_wj1_cvsb = top->j2->cvsb();
  var_wj1_cvsl = top->j2->cvsl();

  var_wj2_pt = top->j3->pt();
  var_wj2_mass = top->j3->mass();
  var_wj2_ptD = top->j3->ptD();
  var_wj2_axis1 = top->j3->axis1();
  var_wj2_mult = top->j3->mult();
  var_wj2_csv = top->j3->deepcsv();
  var_wj2_cvsb = top->j3->cvsb();
  var_wj2_cvsl = top->j3->cvsl();

  var_b_wj1_deltaR = dR(top->b->p4(),top->j2->p4());
  var_b_wj1_mass = (*(top->b->p4())+*(top->j2->p4())).mass();
  var_b_wj2_deltaR = dR(top->b->p4(),top->j3->p4());
  var_b_wj2_mass = (*(top->b->p4())+*(top->j3->p4())).mass();
  var_wcand_deltaR = dR(top->j2->p4(),top->j3->p4());
  var_wcand_mass = top->p4w->mass();
  var_b_wcand_deltaR = dR(top->b->p4(),top->p4w.get());
  var_topcand_mass = top->p4->mass();

  float score = TMVAReader_rTT_->EvaluateMVA("BDT");

  if (debug) {
    std::cout << "rTT tagger on jets " << top->j1idx << " " << top->j2idx << " " << top->j3idx << std::endl;

    std::cout <<  var_b_pt << " " ;
    std::cout <<  var_b_mass << " " ;
    std::cout <<  var_b_ptD << " " ;
    std::cout <<  var_b_axis1 << " " ;
    std::cout <<  var_b_mult << " " ;
    std::cout <<  var_b_csv << " " ;
    std::cout <<  var_b_cvsb << " " ;
    std::cout <<  var_b_cvsl << " " << std::endl;

    std::cout <<  var_wj1_pt << " " ;
    std::cout <<  var_wj1_mass << " " ;
    std::cout <<  var_wj1_ptD << " " ;
    std::cout <<  var_wj1_axis1 << " " ;
    std::cout <<  var_wj1_mult << " " ;
    std::cout <<  var_wj1_csv << " " ;
    std::cout <<  var_wj1_cvsb << " " ;
    std::cout <<  var_wj1_cvsl << " " << std::endl ;

    std::cout <<  var_wj2_pt << " " ;
    std::cout <<  var_wj2_mass << " " ;
    std::cout <<  var_wj2_ptD << " " ;
    std::cout <<  var_wj2_axis1 << " " ;
    std::cout <<  var_wj2_mult << " " ;
    std::cout <<  var_wj2_csv << " " ;
    std::cout <<  var_wj2_cvsb << " " ;
    std::cout <<  var_wj2_cvsl << " " << std::endl ;

    std::cout <<  var_b_wj1_deltaR << " " ;
    std::cout <<  var_b_wj1_mass << " " ;
    std::cout <<  var_b_wj2_deltaR << " " ;
    std::cout <<  var_b_wj2_mass << " " ;
    std::cout <<  var_wcand_deltaR << " " ;
    std::cout <<  var_wcand_mass << " " ;
    std::cout <<  var_b_wcand_deltaR << " " ;
    std::cout <<  var_topcand_mass << " " << std::endl;

    std::cout << score << std::endl;
  }

  top->hasScore_rTT = true;
  top->score_rTT = score;
  return score;

};

float BDT_EventReco::EvalScore_httTT(eTopP top){

  if (top->hasScore_httTT) return top->score_httTT;
  var_httTT_btagDisc_b = top->b->deepcsv();
  var_httTT_btagDisc_Wj1 = top->j2->deepcsv();
  var_httTT_btagDisc_Wj2 = top->j3->deepcsv();
  var_httTT_qg_Wj1  = top->j2->qgl();   		 
  var_httTT_qg_Wj2  = top->j3->qgl();       	 
  var_httTT_m_bWj1Wj2 = (*(top->b->p4())+*(top->j2->p4())+*(top->j3->p4())).mass();
  var_httTT_m_Wj1Wj2_div_m_bWj1Wj2  = (*(top->j2->p4())+*(top->j3->p4())).mass()/var_httTT_m_bWj1Wj2;
  var_httTT_pT_Wj1Wj2 = (*(top->j2->p4())+*(top->j3->p4())).pt();		 
  var_httTT_dR_Wj1Wj2 = dR(top->j2.get(),top->j3.get());
  auto sum =  *(top->j2->p4())+ *(top->j3->p4());
  var_httTT_dR_bW     = dR(top->b.get(),&sum);
  var_httTT_m_bWj1 = (*(top->b->p4())+*(top->j2->p4())).mass();     		 
  var_httTT_m_bWj2 = (*(top->b->p4())+*(top->j3->p4())).mass();     		     		 
  var_httTT_mass_Wj1 = top->j2->mass();
  var_httTT_pT_Wj2   = top->j3->pt();
  var_httTT_mass_Wj2 = top->j3->mass();
  var_httTT_pT_b     = top->b->pt();		 
  var_httTT_mass_b   = top->b->mass();		                 



  float score = TMVAReader_httTT_->EvaluateMVA("BDT");
  score = 1. / (1. + std::sqrt((1. - score) / (1. + score)));
  if (debug) {
    std::cout << "httTT tagger on jets " << top->j1idx << " " << top->j2idx << " " << top->j3idx << std::endl;

    std::cout << "var_httTT_btagDisc_b            :" << var_httTT_btagDisc_b               << std::endl;    
    std::cout << "var_httTT_btagDisc_Wj1 	  :" << var_httTT_btagDisc_Wj1   	  << std::endl;
    std::cout << "var_httTT_btagDisc_Wj2	  :" << var_httTT_btagDisc_Wj2	          << std::endl;
    std::cout << "var_httTT_qg_Wj1   		  :" << var_httTT_qg_Wj1   	          << std::endl;
    std::cout << "var_httTT_qg_Wj2                :" << var_httTT_qg_Wj2                   << std::endl;
    std::cout << "var_httTT_m_bWj1Wj2   	  :" << var_httTT_m_bWj1Wj2   	          << std::endl;
    std::cout << "var_httTT_m_Wj1Wj2_div_m_bWj1Wj2:" << var_httTT_m_Wj1Wj2_div_m_bWj1Wj2   << std::endl;
    std::cout << "var_httTT_pT_Wj1Wj2		  :" << var_httTT_pT_Wj1Wj2		  << std::endl;
    std::cout << "var_httTT_dR_Wj1Wj2		  :" << var_httTT_dR_Wj1Wj2		  << std::endl;
    std::cout << "var_httTT_dR_bW		  :" << var_httTT_dR_bW  		  << std::endl;
    std::cout << "var_httTT_m_bWj1    		  :" << var_httTT_m_bWj1    		  << std::endl;
    std::cout << "var_httTT_m_bWj2    		  :" << var_httTT_m_bWj2    		  << std::endl;
    std::cout << "var_httTT_mass_Wj1		  :" << var_httTT_mass_Wj1		  << std::endl;
    std::cout << "var_httTT_pT_Wj2	          :" << var_httTT_pT_Wj2	                  << std::endl;
    std::cout << "var_httTT_mass_Wj2		  :" << var_httTT_mass_Wj2		  << std::endl;
    std::cout << "var_httTT_pT_b		  :" << var_httTT_pT_b		          << std::endl;
    std::cout << "var_httTT_mass_b                :" << var_httTT_mass_b                   << std::endl;
    std::cout << "score: " << score << std::endl;

  }

  top->hasScore_httTT = true;
  top->score_httTT = score;
  return score;

};

// std::tuple<float,float> BDT_EventReco::EvalKinFit(eTopP top){
//   httTT_kinfit_recBJet = *(top->b);
//   httTT_kinfit_recWJet1 = *(top->j2);
//   httTT_kinfit_recWJet2 = *(top->j3);
//   //httTT_kinfitWorker->fit(httTT_kinfit_recBJet,httTT_kinfit_recWJet1,httTT_kinfit_recWJet2);
//   return std::make_tuple(float(httTT_kinfitWorker->nll()),float(httTT_kinfitWorker->fittedBJet().Pt()));
// };


std::vector<float> BDT_EventReco::CalcHadTopTagger(char* _permlep, char* _x){

      char _this_hadTop[6]={_permlep[0],_permlep[1],_x[0],_x[1],std::max(_x[2],_x[3]),std::min(_x[2],_x[3])};
      std::string this_hadTop(_this_hadTop,_this_hadTop+6);
      float this_hadTop_value = -99;

      if (done_perms.find(this_hadTop) != done_perms.end()){
	this_hadTop_value = done_perms[this_hadTop];
	auto output = std::vector<float>(1,this_hadTop_value);
	output.resize(nOutputVariablesHadTop,-99);
	return output;
      }
      else {

	auto lep_fromTop = leps[((int)(_permlep[0]))-max_n_jets-10];
	auto lep_fromHig = leps[((int)(_permlep[1]))-max_n_jets-10];
	auto bjet_fromHadTop = ((int)(_x[0])>=0) ? jets[(int)(_x[0])] : nulljet;
	auto bjet_fromLepTop = ((int)(_x[1])>=0) ? jets[(int)(_x[1])] : nulljet;
	//      eJet *wjet1_fromHadTop = ((int)(_x[2])>=0) ? jets[(int)(_x[2])] : nulljet;
	//      eJet *wjet2_fromHadTop = ((int)(_x[3])>=0) ? jets[(int)(_x[3])] : nulljet;
      
	if (bjet_fromHadTop==nulljet && bjet_fromLepTop==nulljet) return std::vector<float>(1,this_hadTop_value);
	if (nBMedium>1 && std::min(bjet_fromHadTop->csv(),bjet_fromLepTop->csv())<csv_medium_working_point) return std::vector<float>(1,this_hadTop_value);
	if (bjet_fromHadTop->csv()>0 && bjet_fromHadTop->csv()<csv_loose_working_point) return std::vector<float>(1,this_hadTop_value);
	if (bjet_fromLepTop->csv()>0 && bjet_fromLepTop->csv()<csv_loose_working_point) return std::vector<float>(1,this_hadTop_value);
	if (std::max(bjet_fromHadTop->csv(),bjet_fromLepTop->csv())<csv_medium_working_point && std::min(bjet_fromHadTop->csv(),bjet_fromLepTop->csv())<csv_loose_working_point) return std::vector<float>(1,this_hadTop_value);

	auto hadTop_W = cache->getSum(_x[2],_x[3]);
	auto hadTop = cache->getSum(_x[0],_x[2],_x[3]);

	float comb_pt = hadTop->pt();
	float comb_M = hadTop->mass();
	float comb_eta = hadTop->eta();
	float comb_phi = hadTop->phi();

	if (hadTop_W->mass() > 120) return std::vector<float>(1,this_hadTop_value);
	if (comb_M > 220) return std::vector<float>(1,this_hadTop_value);

	auto lepTop = (*lep_fromTop) + *(bjet_fromLepTop->p4());
	float leptop_pt = lepTop.Pt();
	float leptop_eta = lepTop.Eta();
	float leptop_phi = lepTop.Phi();

	if (lepTop.M() > 180) return std::vector<float>(1,this_hadTop_value);

	bJet_fromLepTop_CSV_var = bjet_fromLepTop->csv();
	bJet_fromHadTop_CSV_var = bjet_fromHadTop->csv();
	HadTop_pT_var = comb_pt;
	W_fromHadTop_mass_var = hadTop_W->mass();
	HadTop_mass_var = comb_M;
	auto X_info = lepTop + (*hadTop);
	auto X_invariant_mass = X_info.M(); 
	auto X_pt = X_info.Pt();
	auto X_eta = X_info.Eta();
	auto X_phi = X_info.Phi();

	lep_ptRatio_fromTop_fromHig_var = lep_fromTop->Pt()/lep_fromHig->Pt();
	dR_lep_fromTop_bJet_fromLepTop_var = (bjet_fromLepTop != nulljet) ? dR(lep_fromTop.get(),bjet_fromLepTop->p4()) : -1;
	dR_lep_fromTop_bJet_fromHadTop_var = (bjet_fromHadTop != nulljet) ? dR(lep_fromTop.get(),bjet_fromHadTop->p4()) : -1;
	dR_lep_fromHig_bJet_fromLepTop_var = (bjet_fromLepTop != nulljet) ? dR(lep_fromHig.get(),bjet_fromLepTop->p4()) : -1;

	this_hadTop_value = TMVAReader_[(nBMedium>1)]->EvaluateMVA( "BDTG method" );
      	done_perms[this_hadTop] = this_hadTop_value;

	std::vector<float> output;
	output.push_back(this_hadTop_value);
	output.push_back(bJet_fromLepTop_CSV_var);
	output.push_back(bJet_fromHadTop_CSV_var);
	output.push_back(HadTop_pT_var);
	output.push_back(W_fromHadTop_mass_var);
	output.push_back(HadTop_mass_var);
	output.push_back(lep_ptRatio_fromTop_fromHig_var);
	output.push_back(dR_lep_fromTop_bJet_fromLepTop_var);
	output.push_back(dR_lep_fromTop_bJet_fromHadTop_var);
	output.push_back(dR_lep_fromHig_bJet_fromLepTop_var);
	output.push_back(lepTop.M());
	output.push_back(X_invariant_mass);
	output.push_back(comb_eta);
	output.push_back(comb_phi);
	output.push_back(leptop_pt);
	output.push_back(leptop_eta);
	output.push_back(leptop_phi);
	output.push_back(X_pt);
	output.push_back(X_eta);
	output.push_back(X_phi);
	return output;

      }

}


std::vector<float> BDT_EventReco::CalcHjTagger(char* _permlep, char* _x, std::vector<int> &permjet){
  auto lep_fromTop = leps[((int)(_permlep[0]))-max_n_jets-10];
  auto lep_fromHig = leps[((int)(_permlep[1]))-max_n_jets-10];

  char _this_Hj[4]={_permlep[0],_permlep[1],std::max(_x[4],_x[5]),std::min(_x[4],_x[5])};
  std::string this_Hj(_this_Hj,_this_Hj+4);
  std::pair<float,float> this_Hj_values =  std::pair<float,float>(-99,-99);

  std::vector<float> output;

  if (done_perms_Hj.find(this_Hj) != done_perms_Hj.end()){
    this_Hj_values = done_perms_Hj[this_Hj];
    output.push_back(this_Hj_values.first);
    output.push_back(this_Hj_values.second);
    output.resize(nOutputVariablesHig,-99);
  }
  else {

    /////////// Higgs tagger

    auto wjet1_fromHiggs = ((int)(_x[4])>=0) ? jets[(int)(_x[4])] : nulljet;
    auto wjet2_fromHiggs = ((int)(_x[5])>=0) ? jets[(int)(_x[5])] : nulljet;
    auto higgs_W = cache->getSum(_x[4],_x[5]);

    float Hj_value[2] = {-99,-99};
    float Hjj_value = -99;
    float H_Wmass = -99;
    float H_mass = -99;
      
    for (int i=0; i<2; i++){
      auto jet_fromHiggs = (i==0) ? wjet1_fromHiggs : wjet2_fromHiggs;
      if (jet_fromHiggs==nulljet) continue;
	
      float dr_lep0 = dR(lep_fromTop.get(),jet_fromHiggs->p4());
      float dr_lep1 = dR(lep_fromHig.get(),jet_fromHiggs->p4());

      iv1_1 = std::min(dr_lep0,dr_lep1);
      iv1_2 = std::max(hjLegacyTraining ? jet_fromHiggs->deepjet() : (hj2017training ? jet_fromHiggs->deepcsv() : jet_fromHiggs->csv()) ,float(0));
      iv1_3 = std::max(jet_fromHiggs->qgl(),float(0));
      iv1_4 = std::max(dr_lep0,dr_lep1);
      iv1_5 = jet_fromHiggs->Pt();
	
      Hj_value[i] = TMVAReader_Hj_->EvaluateMVA("BDTG method");
      Hj_value[i] = 1. / (1. + std::sqrt((1. - Hj_value[i]) / (1. + Hj_value[i])));
	
    }

    // if (wjet1_fromHiggs!=nulljet && wjet2_fromHiggs!=nulljet){
    //   auto jj = (*(wjet1_fromHiggs->p4())+*(wjet2_fromHiggs->p4()));
    //   H_Wmass = jj.M();
    //   H_mass = (jj+*lep_fromHig).M();
    //   iv2_1 = std::min(float((jj+*lep_fromTop).M()),H_mass);
    //   iv2_2 = Hj_value[0]+Hj_value[1];
    //   iv2_3 = dR(wjet1_fromHiggs.get(),wjet2_fromHiggs.get());
    //   std::vector<float> drs;
    //   for (auto i : permjet) {
    // 	if (i<0) continue;
    // 	if (i==(int)(_x[4]) || i==(int)(_x[5])) continue;
    // 	drs.push_back(deltaR(jj.eta(),jj.phi(),jets[i]->eta(),jets[i]->phi()));
    //   }
    //   std::sort(drs.begin(),drs.end());
    //   iv2_4 = drs.at(0);
    //   iv2_5 = higgs_W->mass();
    //   iv2_6 = drs.at(0)/drs.at(drs.size()-1);

    //   Hjj_value = TMVAReader_Hjj_->EvaluateMVA("BDTG method");
    // }

    this_Hj_values =  std::pair<float,float>(std::max(Hj_value[0],Hj_value[1]),Hjj_value);
    done_perms_Hj[this_Hj] = this_Hj_values;

    output.push_back(std::max(Hj_value[0],Hj_value[1]));
    output.push_back(Hjj_value);
    output.push_back(H_Wmass);
    output.push_back(H_mass);

  }

  return output;

}
