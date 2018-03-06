#include <memory>
#include <vector>
#include <string>
#include <utility>
#include "DataFormats/Math/interface/LorentzVector.h"
#include <DataFormats/Math/interface/deltaR.h>
#include "TMVA/Reader.h"
#include <iostream>

typedef math::PtEtaPhiMLorentzVectorD BDT_rTT_ptvec;

class BDT_rTT_Jet : public BDT_rTT_ptvec{
 public:
  BDT_rTT_Jet() : BDT_rTT_ptvec(0,0,0,0){};
  BDT_rTT_Jet(float pt,float eta, float phi, float mass, float csv, float cvsl, float ptD, float axis1, int mult) // pass axis1 = -log(sqrt(...))
    : BDT_rTT_ptvec(pt,eta,phi,mass), _csv(csv), _cvsl(cvsl), _ptD(ptD), _axis1(axis1), _mult(mult){};
  float _csv = 0;
  float _cvsl = 0;
  float _ptD = 0;
  float _axis1 = 0;
  int _mult = 0;
  float csv() const {return _csv;}
  float cvsl() const {return _cvsl;}
  float ptD() const {return _ptD;}
  float axis1() const {return _axis1;}
  float mult() const {return _mult;}
};

class BDT_rTT_top {
public:
  BDT_rTT_top(){};
  BDT_rTT_top(std::shared_ptr<BDT_rTT_Jet> _j1, std::shared_ptr<BDT_rTT_Jet> _j2, std::shared_ptr<BDT_rTT_Jet> _j3){
    j1 = _j1; j2 = _j2; j3 = _j3;
    *p4w = *(dynamic_cast<BDT_rTT_ptvec*>(j2.get()))+*(dynamic_cast<BDT_rTT_ptvec*>(j3.get()));
    *p4 = (j1!=NULL) ? *p4w+*(dynamic_cast<BDT_rTT_ptvec*>(j1.get())) : *p4w;
  }
  std::shared_ptr<BDT_rTT_ptvec> p4 = std::make_shared<BDT_rTT_ptvec>(0,0,0,0);
  std::shared_ptr<BDT_rTT_ptvec> p4w = std::make_shared<BDT_rTT_ptvec>(0,0,0,0);
  std::shared_ptr<BDT_rTT_Jet> j1 = nullptr;
  std::shared_ptr<BDT_rTT_Jet> j2 = nullptr;
  std::shared_ptr<BDT_rTT_Jet> j3 = nullptr;
  float score = -99;
  int j1idx = -99;
  int j2idx = -99;
  int j3idx = -99;
};

class BDT_resolvedTopTagger {
public:
  BDT_resolvedTopTagger(std::string weight_file_name){
    Init(weight_file_name);
  };
  ~BDT_resolvedTopTagger(){
    clear();
  };
  void addJet(float pt,float eta, float phi, float mass, float csv, float cvsl, float ptD, float axis1, int mult){
    jets.push_back(std::make_shared<BDT_rTT_Jet>(pt,eta,phi,mass,csv,cvsl,ptD,axis1,mult));
  };
  void clear();
  void Init(std::string weight_file_name);
  std::vector<float> EvalMVA();
  void setDebug(bool val){debug = val;};

private:

  float EvalScore(const std::shared_ptr<BDT_rTT_top>);

  std::vector<std::shared_ptr<BDT_rTT_Jet>> jets;

  std::shared_ptr<TMVA::Reader> TMVAReader_ = nullptr;

  float var_b_mass = -99;
  float var_b_csv = -99;
  float var_j2_csv = -99;
  float var_j2_cvsl = -99;
  float var_j2_ptD = -99;
  float var_j2_axis1 = -99;
  float var_j3_csv = -99;
  float var_j3_cvsl = -99;
  float var_j3_ptD = -99;
  float var_j3_axis1 = -99;
  float var_topcand_mass = -99;
  float var_topcand_ptDR = -99;
  float var_wcand_mass = -99;
  float var_wcand_ptDR = -99;
  float var_b_j2_mass = -99;
  float var_b_j3_mass = -99;
  float var_sd_n2 = -99;
  float var_j2_mult = -99;
  float var_j3_mult = -99;

  bool debug = false;

};

void BDT_resolvedTopTagger::Init(std::string weight_file_name){

  TMVAReader_ = std::make_shared<TMVA::Reader>( "!Color:!Silent" );

  TMVAReader_->AddVariable("var_b_mass",&var_b_mass);
  TMVAReader_->AddVariable("var_b_csv",&var_b_csv);
  TMVAReader_->AddVariable("var_j2_csv",&var_j2_csv);
  TMVAReader_->AddVariable("var_j2_cvsl",&var_j2_cvsl);
  TMVAReader_->AddVariable("var_j2_ptD",&var_j2_ptD);
  TMVAReader_->AddVariable("var_j2_axis1",&var_j2_axis1);
  TMVAReader_->AddVariable("var_j3_csv",&var_j3_csv);
  TMVAReader_->AddVariable("var_j3_cvsl",&var_j3_cvsl);
  TMVAReader_->AddVariable("var_j3_ptD",&var_j3_ptD);
  TMVAReader_->AddVariable("var_j3_axis1",&var_j3_axis1);
  TMVAReader_->AddVariable("var_topcand_mass",&var_topcand_mass);
  TMVAReader_->AddVariable("var_topcand_ptDR",&var_topcand_ptDR);
  TMVAReader_->AddVariable("var_wcand_mass",&var_wcand_mass);
  TMVAReader_->AddVariable("var_wcand_ptDR",&var_wcand_ptDR);
  TMVAReader_->AddVariable("var_b_j2_mass",&var_b_j2_mass);
  TMVAReader_->AddVariable("var_b_j3_mass",&var_b_j3_mass);
  TMVAReader_->AddVariable("var_sd_n2",&var_sd_n2);
  TMVAReader_->AddVariable("var_j2_mult",&var_j2_mult);
  TMVAReader_->AddVariable("var_j3_mult",&var_j3_mult);

  TMVAReader_->BookMVA("BDT",weight_file_name);

};

void BDT_resolvedTopTagger::clear(){

  jets.clear();

  var_b_mass = -99;
  var_b_csv = -99;
  var_j2_csv = -99;
  var_j2_cvsl = -99;
  var_j2_ptD = -99;
  var_j2_axis1 = -99;
  var_j3_csv = -99;
  var_j3_cvsl = -99;
  var_j3_ptD = -99;
  var_j3_axis1 = -99;
  var_topcand_mass = -99;
  var_topcand_ptDR = -99;
  var_wcand_mass = -99;
  var_wcand_ptDR = -99;
  var_b_j2_mass = -99;
  var_b_j3_mass = -99;
  var_sd_n2 = -99;
  var_j2_mult = -99;
  var_j3_mult = -99;

}

std::vector<float> BDT_resolvedTopTagger::EvalMVA(){

  int njets = jets.size();
  std::sort(jets.begin(),jets.end(),[](const std::shared_ptr<BDT_rTT_Jet> &a, const std::shared_ptr<BDT_rTT_Jet> &b){return a->csv() > b->csv();});

  if (debug) std::cout << "njets " << njets << std::endl;

  std::vector<std::shared_ptr<BDT_rTT_top>> allcands;

  for (int i1=0; i1<2; i1++) {
    for (int i2=0; i2<int(njets-1); i2++){
      if (i2==i1) continue;
      for (int i3=i2+1; i3<int(njets); i3++){
	if (i3==i1) continue;
	auto topcand = std::make_shared<BDT_rTT_top>(jets.at(i1),jets.at(i2),jets.at(i3));
	if ((fabs(topcand->p4->mass()-175)>80) || (fabs(topcand->p4w->mass()-80)>40)) continue;
	topcand->score = EvalScore(topcand);
	topcand->j1idx = i1;
	topcand->j2idx = i2;
	topcand->j3idx = i3;
	allcands.push_back(topcand);
      }
    }
  }

  std::vector<float> output(16,-99);
  if (allcands.size()>0) {
    auto top = *std::min_element(allcands.begin(),allcands.end(),[](const std::shared_ptr<BDT_rTT_top> &a, const std::shared_ptr<BDT_rTT_top> &b){return a->score > b->score;});
    output.at(0) = top->score; // mvaValue
    output.at(1) = top->p4->pt(); // HadTop_pt
    output.at(2) = top->p4->eta(); // HadTop_eta
    output.at(3) = top->p4->phi(); // HadTop_phi
    output.at(4) = top->p4->mass(); // HadTop_mass
    output.at(5) = top->p4w->pt(); // W_fromHadTop_pt
    output.at(6) = top->p4w->eta(); // W_fromHadTop_eta
    output.at(7) = top->p4w->phi(); // W_fromHadTop_phi
    output.at(8) = top->p4w->mass(); // W_fromHadTop_mass
    output.at(9) = std::max(top->j2->csv(),top->j3->csv()); // W_fromHadTop_maxCSVjj
    output.at(10) = deltaR(top->j2->eta(),top->j2->phi(),top->j3->eta(),top->j3->phi()); // W_fromHadTop_dRjj
    output.at(11) = deltaR(top->j1->eta(),top->j1->phi(),top->p4w->eta(),top->p4w->phi()); // W_fromHadTop_dRb
    output.at(12) = top->j1->csv(); // b_fromHadTop_CSV
    output.at(13) = top->j1idx;
    output.at(14) = top->j2idx;
    output.at(15) = top->j3idx;
  }
  if (debug) std::cout << "returning " << output.at(0) << std::endl;
  return output;

};

float BDT_resolvedTopTagger::EvalScore(const std::shared_ptr<BDT_rTT_top> top){

  var_b_mass = top->j1->mass();
  var_b_csv = top->j1->csv();
  var_j2_csv = top->j2->csv();
  var_j2_cvsl = top->j2->cvsl();
  var_j2_ptD = top->j2->ptD();
  var_j2_axis1 = std::exp(-top->j2->axis1()); // training uses definition of axis1 without -log
  var_j3_csv = top->j3->csv();
  var_j3_cvsl = top->j3->cvsl();
  var_j3_ptD = top->j3->ptD();
  var_j3_axis1 = std::exp(-top->j3->axis1()); // training uses definition of axis1 without -log
  var_topcand_mass = top->p4->mass();
  var_topcand_ptDR = top->p4->pt()*deltaR(top->j1->eta(),top->j1->phi(),top->p4w->eta(),top->p4w->phi());
  var_wcand_mass = top->p4w->mass();
  auto var_wcand_deltaR = deltaR(top->j2->eta(),top->j2->phi(),top->j3->eta(),top->j3->phi());
  var_wcand_ptDR = top->p4w->pt()*var_wcand_deltaR;
  var_b_j2_mass = (*(dynamic_cast<BDT_rTT_ptvec*>(top->j1.get()))+*(dynamic_cast<BDT_rTT_ptvec*>(top->j2.get()))).mass();
  var_b_j3_mass = (*(dynamic_cast<BDT_rTT_ptvec*>(top->j1.get()))+*(dynamic_cast<BDT_rTT_ptvec*>(top->j3.get()))).mass();
  var_sd_n2 = top->j3->pt()/(top->j2->pt()+top->j3->pt())/std::pow(var_wcand_deltaR,-2);
  var_j2_mult = top->j2->mult();
  var_j3_mult = top->j3->mult();

  if (debug) {
    std::cout <<  var_b_mass << " " ;
    std::cout <<  var_b_csv << " " ;
    std::cout <<  var_j2_csv << " " ;
    std::cout <<  var_j2_cvsl << " " ;
    std::cout <<  var_j2_ptD << " " ;
    std::cout <<  var_j2_axis1 << " " ;
    std::cout <<  var_j3_csv << " " ;
    std::cout <<  var_j3_cvsl << " " ;
    std::cout <<  var_j3_ptD << " " ;
    std::cout <<  var_j3_axis1 << " " ;
    std::cout <<  var_topcand_mass << " " ;
    std::cout <<  var_topcand_ptDR << " " ;
    std::cout <<  var_wcand_mass << " " ;
    std::cout <<  var_wcand_ptDR << " " ;
    std::cout <<  var_b_j2_mass << " " ;
    std::cout <<  var_b_j3_mass << " " ;
    std::cout <<  var_sd_n2 << " " ;
    std::cout <<  var_j2_mult << " " ;
    std::cout <<  var_j3_mult << std::endl;
    std::cout << TMVAReader_->EvaluateMVA("BDT") << std::endl;
  }

  return TMVAReader_->EvaluateMVA("BDT");

};
