#include "TFile.h"
#include "TH2.h"
#include "TH2Poly.h"
#include "TGraphAsymmErrors.h"
#include "TRandom3.h"

#include <iostream>
#include <vector>
#include <algorithm>
#include <numeric>
#include <map>

float ttH_MVAto1D_6_2lss_Marco (float kinMVA_2lss_ttbar, float kinMVA_2lss_ttV){

  return 2*((kinMVA_2lss_ttbar>=-0.2)+(kinMVA_2lss_ttbar>=0.3))+(kinMVA_2lss_ttV>=-0.1)+1;

}
float ttH_MVAto1D_3_3l_Marco (float kinMVA_3l_ttbar, float kinMVA_3l_ttV){

  if (kinMVA_3l_ttbar<0.3 && kinMVA_3l_ttV<-0.1) return 1;
  else if (kinMVA_3l_ttbar>=0.3 && kinMVA_3l_ttV>=-0.1) return 3;
  else return 2;

}

#include "binning_2d_thresholds.h"
float ttH_MVAto1D_7_2lss_Marco (float kinMVA_2lss_ttbar, float kinMVA_2lss_ttV){

//________________
//|   |   |   | 7 |
//|   |   | 4 |___|
//| 1 | 2 |___| 6 |
//|   |   |   |___|
//|   |   | 3 | 5 |
//|___|___|___|___|
//

  if (kinMVA_2lss_ttbar<cuts_2lss_ttbar0) return 1;
  else if (kinMVA_2lss_ttbar<cuts_2lss_ttbar1) return 2;
  else if (kinMVA_2lss_ttbar<cuts_2lss_ttbar2) return 3+(kinMVA_2lss_ttV>=cuts_2lss_ttV0);
  else return 5+(kinMVA_2lss_ttV>=cuts_2lss_ttV1)+(kinMVA_2lss_ttV>=cuts_2lss_ttV2);

}
float ttH_MVAto1D_5_3l_Marco (float kinMVA_3l_ttbar, float kinMVA_3l_ttV){

  int reg = 2*((kinMVA_3l_ttbar>=cuts_3l_ttbar1)+(kinMVA_3l_ttbar>=cuts_3l_ttbar2))+(kinMVA_3l_ttV>=cuts_3l_ttV1)+1;
  if (reg==2) reg=1;
  if (reg>2) reg = reg-1;
  return reg;

}


float newBinning(float x, float y){
  float r =  4*((y>-0.16)+(y>0.28))+(x>-0.22)+(x>0.09)+(x>0.42)+1;
  if (r==9) r-=4;
  if (r>9) r-=1;
  return r;
}

#include "GetBinning.C"


float ttH_MVAto1D_6_flex (float kinMVA_2lss_ttbar, float kinMVA_2lss_ttV, int pdg1, int pdg2, float ttVcut, float ttcut1, float ttcut2){

  return 2*((kinMVA_2lss_ttbar>=ttcut1)+(kinMVA_2lss_ttbar>=ttcut2)) + (kinMVA_2lss_ttV>=ttVcut)+1;

}

float returnInputX(float x, float y) {return x;}

float mvaCat(float ttH, float rest, float ttW, float thq){
  float ret = 0; 
  if (ttH > rest && ttH > ttW && ttH > thq){
    ret =  ttH;
  }
  if (ttW > ttH && ttW > rest && ttW > thq){
    ret= ttW+1;
  }
  if (thq > ttH && thq > ttW && thq > rest){
    ret= thq+2;
  }
  if (rest > ttH && rest > thq && rest > ttW){
    ret= rest+3;
  }
  return ret;

}

int ttH_catIndex_2lss(int LepGood1_pdgId, int LepGood2_pdgId, float tth, float ttw, float thq, float rest)
{

//2lss_ee_ttH
//2lss_ee_rest
//2lss_ee_ttw
//2lss_ee_thq
//2lss_em_ttH
//2lss_em_rest
//2lss_em_ttw
//2lss_em_thq
//2lss_mm_ttH
//2lss_mm_rest
//2lss_mm_ttw
//2lss_mm_thq  
  int flch = 0;
  int procch = 0;

  if (abs(LepGood1_pdgId)+abs(LepGood2_pdgId) == 22)
    flch = 0;
  else if (abs(LepGood1_pdgId)+abs(LepGood2_pdgId) == 24)
    flch = 1;
  else if (abs(LepGood1_pdgId)+abs(LepGood2_pdgId) == 26)
    flch = 2;
  else
    cout << "[2lss]: It shouldnt be here. pdgids are " << abs(LepGood1_pdgId) << " " << abs(LepGood2_pdgId)  << endl;

  if (tth >= ttw && tth >= thq && tth >= rest)
    procch = 0;
  else if (rest >= tth && rest >= ttw && rest >= thq)
    procch = 1;
  else if (ttw >= tth && ttw >= rest && ttw >= thq)
    procch = 2;
  else if (thq >= tth && thq >= rest && thq >= ttw)
    procch = 3;
  else 
    cout << "[2lss]: It shouldnt be here. DNN scores are " << tth << " " << rest << " " << ttw << " " << thq << endl;
      
  return flch*4+procch+1;

}

std::map<TString,int> bins2lss = {{"ee_ttHnode",5},{"ee_Restnode",8},{"ee_ttWnode",6},{"ee_tHQnode",4},
				  {"em_ttHnode",13},{"em_Restnode",8},{"em_ttWnode",19},{"em_tHQnode",11},
				  {"mm_ttHnode",13},{"mm_Restnode",11},{"mm_ttWnode",15},{"mm_tHQnode",7}};
std::vector<TString> bin2lsslabels = {
  "ee_ttHnode","ee_Restnode","ee_ttWnode","ee_tHQnode",
  "em_ttHnode","em_Restnode","em_ttWnode","em_tHQnode",
  "mm_ttHnode","mm_Restnode","mm_ttWnode","mm_tHQnode"
};

std::map<TString, TH1F*> binHistos2lss;
std::map<TString, int> bins2lsscumul;
TFile* f2lssBins;


int ttH_catIndex_2lss_MVA(int LepGood1_pdgId, int LepGood2_pdgId, float tth, float ttw, float thq, float rest)
{
  if (!f2lssBins){
    int offset = 0;
    f2lssBins = TFile::Open("../../data/kinMVA/DNNBin_v3_xmas.root");
    for (auto & la : bin2lsslabels){
      int bins = bins2lss[la];
      binHistos2lss[la] = (TH1F*) f2lssBins->Get(Form("%s_2018_Map_nBin%d", la.Data(), bins));
      bins2lsscumul[la] = offset;
      offset += bins;
    }
  }
  
  int idx = ttH_catIndex_2lss(LepGood1_pdgId, LepGood2_pdgId, tth,ttw, thq,rest); 
  TString binLabel = bin2lsslabels[idx-1];
  float mvavar = 0;
  if (tth >= ttw && tth >= thq && tth >= rest)
    mvavar = tth;
  else if (rest >= tth && rest >= ttw && rest >= thq)
    mvavar =rest;
  else if (ttw >= tth && ttw >= rest && ttw >= thq)
    mvavar = ttw;
  else if (thq >= tth && thq >= rest && thq >= ttw)
    mvavar = thq;
  else 
    cout << "It shouldnt be here" << endl;
  return binHistos2lss[binLabel]->FindBin( mvavar ) + bins2lsscumul[binLabel];

}


// for plots

int ttH_2lss_node( float tth, float ttw, float thq, float rest ){

  int procch = 0;
  if (tth >= ttw && tth >= thq && tth >= rest)
    procch = 0;
  else if (rest >= tth && rest >= ttw && rest >= thq)
    procch = 1;
  else if (ttw >= tth && ttw >= rest && ttw >= thq)
    procch = 2;
  else if (thq >= tth && thq >= rest && thq >= ttw)
    procch = 3;
  else 
    cout << "[2lss]: It shouldnt be here. DNN scores are " << tth << " " << rest << " " << ttw << " " << thq << endl;

  return procch;
}


std::vector<TString> bin2lsslabels_plots = {
  "ee_ttHnode" , "em_ttHnode" ,  "mm_ttHnode", 
  "ee_Restnode", "em_Restnode",  "mm_Restnode",
  "ee_ttWnode" , "em_ttWnode" ,  "mm_ttWnode",
  "ee_tHQnode" , "em_tHQnode" ,  "mm_tHQnode",

};

std::map<TString, TH1F*> binHistos2lss_plots;
TFile* f2lssBins_plots;


int ttH_catIndex_2lss_plots(int LepGood1_pdgId, int LepGood2_pdgId, float tth, float ttw, float thq, float rest)
{

  if (!f2lssBins_plots){
    f2lssBins_plots = TFile::Open("../../data/kinMVA/DNNBin_v3_xmas.root");
    for (auto & la : bin2lsslabels_plots){
      int bins = bins2lss[la];
      binHistos2lss_plots[la] = (TH1F*) f2lssBins_plots->Get(Form("%s_2018_Map_nBin%d", la.Data(), bins));
    }
  }

  int idx = ttH_catIndex_2lss(LepGood1_pdgId, LepGood2_pdgId, tth,ttw, thq,rest); 
  TString binLabel = bin2lsslabels[idx-1];
  int offset=0;
  int node = ttH_2lss_node(tth, ttw,thq, rest);
  if (abs(LepGood1_pdgId*LepGood2_pdgId) == 143){
    if (node == 0) offset = 5;
    else if (node == 1) offset = 8;
    else if (node == 2) offset = 6;
    else offset = 4;
  }
  if (abs(LepGood1_pdgId*LepGood2_pdgId) == 169){
    if (node == 0) offset = 5+13;
    else if (node == 1) offset = 8+8;
    else if (node == 2) offset = 6+19;
    else offset = 4+11;
  }

  float mvavar = 0;
  if (tth >= ttw && tth >= thq && tth >= rest)
    mvavar = tth;
  else if (rest >= tth && rest >= ttw && rest >= thq)
    mvavar =rest;
  else if (ttw >= tth && ttw >= rest && ttw >= thq)
    mvavar = ttw;
  else if (thq >= tth && thq >= rest && thq >= ttw)
    mvavar = thq;
  else 
    cout << "It shouldnt be here" << endl;


  return binHistos2lss_plots[binLabel]->FindBin( mvavar ) + offset;
    

}


int ttH_catIndex_2lss_nosign(int LepGood1_pdgId, int LepGood2_pdgId, int nBJetMedium25){

  if (abs(LepGood1_pdgId)==11 && abs(LepGood2_pdgId)==11) return 1;
  if ((abs(LepGood1_pdgId) != abs(LepGood2_pdgId)) && nBJetMedium25 < 2) return 2;
  if ((abs(LepGood1_pdgId) != abs(LepGood2_pdgId)) && nBJetMedium25 >= 2) return 3;
  if (abs(LepGood1_pdgId)==13 && abs(LepGood2_pdgId)==13 && nBJetMedium25 < 2) return 4;
  if (abs(LepGood1_pdgId)==13 && abs(LepGood2_pdgId)==13 && nBJetMedium25 >= 2) return 5;

 return -1;

}

int ttH_catIndex_2lss_SVA(int LepGood1_pdgId, int LepGood2_pdgId, int LepGood1_charge, int nJet25){

  int res = -2;

  if (abs(LepGood1_pdgId)==11 && abs(LepGood2_pdgId)==11) res = 1;
  if ((abs(LepGood1_pdgId) != abs(LepGood2_pdgId)) && LepGood1_charge<0) res = 3;
  if ((abs(LepGood1_pdgId) != abs(LepGood2_pdgId)) && LepGood1_charge>0) res = 5;
  if (abs(LepGood1_pdgId)==13 && abs(LepGood2_pdgId)==13 && LepGood1_charge<0) res = 7;
  if (abs(LepGood1_pdgId)==13 && abs(LepGood2_pdgId)==13 && LepGood1_charge>0) res = 9;
  if (nJet25>=6) res+=1;

  return res; // 1-10
}


int ttH_catIndex_2lss_SVA_forPlots1(int LepGood1_pdgId, int LepGood2_pdgId, int nJet25){

  int res = -2;

  if (abs(LepGood1_pdgId)==11 && abs(LepGood2_pdgId)==11) res = 1;
  if ((abs(LepGood1_pdgId) != abs(LepGood2_pdgId))) res = 3;
  if (abs(LepGood1_pdgId)==13 && abs(LepGood2_pdgId)==13) res = 5;
  if (nJet25>=6) res+=1;

  return res; // 1-6
}

int ttH_catIndex_2lss_SVA_forPlots2(int nJet25){

  int res = 1;
  if (nJet25>=6) res+=1;
  return res; // 1-6
}

int ttH_catIndex_2lss_SVA_soft(int LepGood1_pdgId, int LepGood2_pdgId, int LepGood1_charge, int nJet25){

  int res = -2;

  if (abs(LepGood1_pdgId)==11 && abs(LepGood2_pdgId)==11) res = 1;
  if ((abs(LepGood1_pdgId) != abs(LepGood2_pdgId)) && LepGood1_charge<0) res = 3;
  if ((abs(LepGood1_pdgId) != abs(LepGood2_pdgId)) && LepGood1_charge>0) res = 5;
  if (abs(LepGood1_pdgId)==13 && abs(LepGood2_pdgId)==13 && LepGood1_charge<0) res = 7;
  if (abs(LepGood1_pdgId)==13 && abs(LepGood2_pdgId)==13 && LepGood1_charge>0) res = 9;
  if (nJet25>3) res+=1;

  return res; // 1-10
}


int ttH_catIndex_3l(float ttH, float tH, float rest, int lep1_pdgId, int lep2_pdgId, int lep3_pdgId, int nBMedium )
{

  int sumpdgId = abs(lep1_pdgId)+abs(lep2_pdgId)+abs(lep3_pdgId);
  
  if (ttH >= rest && ttH >= tH){
    if (nBMedium < 2)
      return 1; // ttH_bl
    else
      return 2; // ttH_bt
  }
  else if (tH >= ttH && tH >= rest){
    if (nBMedium < 2){
      return 3; // tH_bl
    }
    else{
      return 4; // tH_bt
    }
  }
  else if (rest >= ttH && rest >= tH){
    if ( sumpdgId == 33){ // rest_eee
      return 5;
    }
    else if (sumpdgId == 35){ 
      if (nBMedium < 2)
	return 6; // rest_eem_bl
      else
	return 7; // rest_eem_bt
    }
    else if (sumpdgId == 37){ // emm
      if (nBMedium < 2)
	return 8; // rest_emm_bl
      else
	return 9; // rest_emm_bt
    }
    else if (sumpdgId == 39){ // mmm
      if (nBMedium < 2)
	return 10; // rest_mmm_bl
      else
	return 11; // rest_mmm_bt
    }
  }

  
  cout << "[ttH_catIndex_3l]: It should not be here" << endl;
  return -1;

}


std::vector<TString> bin3llabels = {"ttH_bl",  "ttH_bt",  "tH_bl",  "tH_bt",  "rest_eee",  "rest_eem_bl",  "rest_eem_bt",  "rest_emm_bl",  "rest_emm_bt",  "rest_mmm_bl",  "rest_mmm_bt"};

std::map<TString, TH1F*> binHistos3l;
std::map<TString, int> bins3lcumul;
TFile* f3lBins;



int ttH_catIndex_3l_MVA(float ttH, float tH, float rest, int lep1_pdgId, int lep2_pdgId, int lep3_pdgId, int nBMedium )
{

  if (!f3lBins){
    f3lBins=TFile::Open("../../data/kinMVA/binning_3l.root");
    int count=0;
    for (auto label : bin3llabels){
      binHistos3l[label] = (TH1F*) f3lBins->Get(label);
      bins3lcumul[label] = count;
      count += binHistos3l[label]->GetNbinsX();
    }
  }
  TString binLabel = bin3llabels[ttH_catIndex_3l(ttH,tH,rest,lep1_pdgId,lep2_pdgId,lep3_pdgId,nBMedium)-1];
  float mvas[] = { ttH, tH, rest };
  float mvavar = *std::max_element( mvas, mvas+3 );
  return binHistos3l[binLabel]->FindBin( mvavar ) + bins3lcumul[binLabel];

  
  cout << "[ttH_catIndex_3l_MVA]: It should not be here "<< ttH << " " << tH << " " << rest << endl;
  return -1;

}

int ttH_catIndex_3l_node(float ttH, float tH, float rest){
  if (ttH >= tH && ttH >= rest){
    return 0;
  }
  else if (tH >= ttH && tH >= rest){
    return 1;
  }
  else if (rest >= ttH && rest >= tH){
    return 2;
  }
}


int ttH_catIndex_3l_plots(float ttH, float tH, float rest, int lep1_pdgId, int lep2_pdgId, int lep3_pdgId, int nBMedium )
{
  if (!f3lBins){
    f3lBins=TFile::Open("../../data/kinMVA/binning_3l.root");
    int count=0;
    for (auto label : bin3llabels){
      binHistos3l[label] = (TH1F*) f3lBins->Get(label);
      bins3lcumul[label] = count;
      count += binHistos3l[label]->GetNbinsX();
    }
  }

  int offset =0;
  int pdgSum = abs(lep1_pdgId) + abs(lep2_pdgId) + abs(lep3_pdgId);

  if (ttH_catIndex_3l_node(ttH,tH,rest) == 0){
    if (nBMedium >= 2) offset=5;
  }
  else if (ttH_catIndex_3l_node(ttH,tH,rest) == 1){
    if (nBMedium >= 2) offset=7;
  }
  else{
    if (nBMedium  < 2){
      if (pdgSum == 35) offset = 1;
      else if (pdgSum == 37) offset=1+4;
      else if (pdgSum == 39) offset=1+4+4;
    }
    else{
      if (pdgSum == 35) offset = 1+4+4+3;
      if (pdgSum == 37) offset = 1+4+4+3+1;
      if (pdgSum == 39) offset = 1+4+4+3+1+1;
    }
  }
  TString binLabel = bin3llabels[ttH_catIndex_3l(ttH,tH,rest,lep1_pdgId,lep2_pdgId,lep3_pdgId,nBMedium)-1];
  float mvas[] = { ttH, tH, rest };
  float mvavar = *std::max_element( mvas, mvas+3 );
  return binHistos3l[binLabel]->FindBin( mvavar ) + offset;

}

float ttH_mva_4l(float score)
{
  return 1. / (1. + std::sqrt((1. - score) / (1. + score)));

}

int ttH_catIndex_4l(float bdt, float cut=0.85)
{
  if (ttH_mva_4l(bdt) < cut) return 1;
  else return 2;
}

int ttH_catIndex_3l_SVA(int LepGood1_charge, int LepGood2_charge, int LepGood3_charge, int nJet25){

  if ((LepGood1_charge+LepGood2_charge+LepGood3_charge)<0 && nJet25 < 4) return 11;
  if ((LepGood1_charge+LepGood2_charge+LepGood3_charge)>0 && nJet25 < 4) return 12;
  if ((LepGood1_charge+LepGood2_charge+LepGood3_charge)<0 && nJet25 >= 4) return 13;
  if ((LepGood1_charge+LepGood2_charge+LepGood3_charge)>0 && nJet25 >= 4) return 14;

  return -1;

}

int ttH_catIndex_3l_SVAforPlots(int nJet25){

  if (nJet25 < 4) return 1;
  if (nJet25 >= 4) return 2;

  return -1;

}

int ttH_catIndex_3l_SVA_soft(int LepGood1_charge, int LepGood2_charge, int LepGood3_charge, int nJet25){

  if ((LepGood1_charge+LepGood2_charge+LepGood3_charge)<0 && nJet25 <= 3) return 11;
  if ((LepGood1_charge+LepGood2_charge+LepGood3_charge)>0 && nJet25 <= 3) return 12;
  if ((LepGood1_charge+LepGood2_charge+LepGood3_charge)<0 && nJet25 > 3) return 13;
  if ((LepGood1_charge+LepGood2_charge+LepGood3_charge)>0 && nJet25 > 3) return 14;

  return -1;

}

TFile *_file_recoToLoose_leptonSF_mu1_lt30 = NULL;
TFile *_file_recoToLoose_leptonSF_mu1_gt30 = NULL;
TFile *_file_recoToLoose_leptonSF_mu2 = NULL;
TFile *_file_recoToLoose_leptonSF_mu3 = NULL;
TFile *_file_recoToLoose_leptonSF_mu4_lt10 = NULL;
TFile *_file_recoToLoose_leptonSF_mu4_gt10 = NULL;
TH2F *_histo_recoToLoose_leptonSF_mu1_lt30 = NULL;
TH2F *_histo_recoToLoose_leptonSF_mu1_gt30 = NULL;
TH2F *_histo_recoToLoose_leptonSF_mu2 = NULL;
TH2F *_histo_recoToLoose_leptonSF_mu3 = NULL;
TGraphAsymmErrors *_histo_recoToLoose_leptonSF_mu4_lt10 = NULL;
TGraphAsymmErrors *_histo_recoToLoose_leptonSF_mu4_gt10 = NULL;
TFile *_file_recoToLoose_leptonSF_el = NULL;
TH2F *_histo_recoToLoose_leptonSF_el1 = NULL;
TH2F *_histo_recoToLoose_leptonSF_el2 = NULL;
TH2F *_histo_recoToLoose_leptonSF_el3 = NULL;
TFile *_file_recoToLoose_leptonSF_gsf_lt20 = NULL;
TH2F *_histo_recoToLoose_leptonSF_gsf_lt20 = NULL;
TFile *_file_recoToLoose_leptonSF_gsf_gt20 = NULL;
TH2F *_histo_recoToLoose_leptonSF_gsf_gt20 = NULL;

float _get_recoToLoose_leptonSF_ttH(int pdgid, float pt, float eta, int nlep, float var){

  // nlep is ignored for the loose selection

  if (!_histo_recoToLoose_leptonSF_mu1_lt30) {
    _file_recoToLoose_leptonSF_mu1_lt30 = new TFile("../../data/leptonSF/mu_scaleFactors_ptLt30.root","read");
    _file_recoToLoose_leptonSF_mu1_gt30 = new TFile("../../data/leptonSF/mu_scaleFactors_ptGt30.root","read");
    _file_recoToLoose_leptonSF_mu2 = new TFile("../../data/leptonSF/scaleFactors_mu_DxyDzSip8mIso04_over_LooseID.root","read");
    //    _file_recoToLoose_leptonSF_mu3 = new TFile("../../data/leptonSF/TnP_NUM_TightIP2D_DENOM_MediumID_VAR_map_pt_eta.root","read");
    _file_recoToLoose_leptonSF_mu4_lt10 = new TFile("../../data/leptonSF/mu_scaleFactors_trkEff_ptLt10.root","read");
    _file_recoToLoose_leptonSF_mu4_gt10 = new TFile("../../data/leptonSF/mu_scaleFactors_trkEff_ptGt10.root","read");
    _histo_recoToLoose_leptonSF_mu1_lt30 = (TH2F*)(_file_recoToLoose_leptonSF_mu1_lt30->Get("NUM_LooseID_DEN_genTracks_pt_abseta"));
    _histo_recoToLoose_leptonSF_mu1_gt30 = (TH2F*)(_file_recoToLoose_leptonSF_mu1_gt30->Get("NUM_LooseID_DEN_genTracks_pt_abseta"));
    _histo_recoToLoose_leptonSF_mu2 = (TH2F*)(_file_recoToLoose_leptonSF_mu2->Get("NUM_ttHLoo_DEN_LooseID"));
    //    _histo_recoToLoose_leptonSF_mu3 = (TH2F*)(_file_recoToLoose_leptonSF_mu3->Get("SF"));
    _histo_recoToLoose_leptonSF_mu4_lt10 = (TGraphAsymmErrors*)(_file_recoToLoose_leptonSF_mu4_lt10->Get("ratio_eff_eta3_tk0_dr030e030_corr"));
    _histo_recoToLoose_leptonSF_mu4_gt10 = (TGraphAsymmErrors*)(_file_recoToLoose_leptonSF_mu4_gt10->Get("ratio_eff_eta3_dr030e030_corr"));
  }
  if (!_histo_recoToLoose_leptonSF_el1) {
    _file_recoToLoose_leptonSF_el = new TFile("../../data/leptonSF/egammaEffi.txt_EGM2D_looseTTH_2017.root","read");
    _histo_recoToLoose_leptonSF_el1 = (TH2F*)(_file_recoToLoose_leptonSF_el->Get("EGamma_SF2D"));
//    _histo_recoToLoose_leptonSF_el2 = (TH2F*)(_file_recoToLoose_leptonSF_el->Get("MVAVLooseElectronToMini4"));
//    _histo_recoToLoose_leptonSF_el3 = (TH2F*)(_file_recoToLoose_leptonSF_el->Get("MVAVLooseElectronToConvVetoIHit1"));
  }
  if (!_histo_recoToLoose_leptonSF_gsf_lt20) {
    _file_recoToLoose_leptonSF_gsf_lt20 = new TFile("../../data/leptonSF/el_scaleFactors_gsf_ptLt20.root","read");
    _histo_recoToLoose_leptonSF_gsf_lt20 = (TH2F*)(_file_recoToLoose_leptonSF_gsf_lt20->Get("EGamma_SF2D"));
    _file_recoToLoose_leptonSF_gsf_gt20 = new TFile("../../data/leptonSF/el_scaleFactors_gsf_ptGt20.root","read");
    _histo_recoToLoose_leptonSF_gsf_gt20 = (TH2F*)(_file_recoToLoose_leptonSF_gsf_gt20->Get("EGamma_SF2D"));
  }

  if (abs(pdgid)==13){

    float out = 1;

    TH2F *hist = (pt<30) ? _histo_recoToLoose_leptonSF_mu1_lt30 : _histo_recoToLoose_leptonSF_mu1_gt30;
    int ptbin  = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(pt)));
    int etabin = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(fabs(eta))));
    out *= (pt>=15 && pt<30 && fabs(eta)>=2.1 && fabs(eta)<2.4) ? 1 : hist->GetBinContent(ptbin,etabin)+var*hist->GetBinError(ptbin,etabin); // careful: workaround, SF was not measured there

    if (_histo_recoToLoose_leptonSF_mu2){
    hist = _histo_recoToLoose_leptonSF_mu2;
    ptbin  = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(pt)));
    etabin = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(fabs(eta))));
    out *= hist->GetBinContent(ptbin,etabin)+var*hist->GetBinError(ptbin,etabin);
    }

    if (_histo_recoToLoose_leptonSF_mu3){
    hist = _histo_recoToLoose_leptonSF_mu3;
    ptbin  = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(pt)));
    etabin = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(fabs(eta))));
    out *= hist->GetBinContent(ptbin,etabin)+var*hist->GetBinError(ptbin,etabin);
    }

    if (_histo_recoToLoose_leptonSF_mu4_lt10 || _histo_recoToLoose_leptonSF_mu4_gt10){
      TGraphAsymmErrors *hist1 = (pt<10) ? _histo_recoToLoose_leptonSF_mu4_lt10 : _histo_recoToLoose_leptonSF_mu4_gt10;
      float eta1 = std::max(float(hist1->GetXaxis()->GetXmin()+1e-5), std::min(float(hist1->GetXaxis()->GetXmax()-1e-5), eta));
      out *= hist1->Eval(eta1); // uncertainty ignored here
    }

    if (out<=0) std::cout << "ERROR in muon recoToLoose SF: " << out << std::endl;
    return out;

  }

  if (abs(pdgid)==11){
    TH2F *hist = NULL;
    float out = 1;
    int ptbin, etabin;
    if (_histo_recoToLoose_leptonSF_el1){
    hist = _histo_recoToLoose_leptonSF_el1;
    etabin = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(eta))); // careful, different convention
    ptbin  = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(pt)));
    out *= hist->GetBinContent(etabin,ptbin)+var*hist->GetBinError(etabin,ptbin);
    }
    if (_histo_recoToLoose_leptonSF_el2){
    hist = _histo_recoToLoose_leptonSF_el2;
    ptbin  = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(pt)));
    etabin = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(eta)));
    out *= hist->GetBinContent(ptbin,etabin)+var*hist->GetBinError(ptbin,etabin);
    }
    if (_histo_recoToLoose_leptonSF_el3){
    hist = _histo_recoToLoose_leptonSF_el3;
    ptbin  = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(pt)));
    etabin = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(eta)));
    out *= hist->GetBinContent(ptbin,etabin)+var*hist->GetBinError(ptbin,etabin);
    }
    if (_histo_recoToLoose_leptonSF_gsf_lt20 && pt<20){
    hist = _histo_recoToLoose_leptonSF_gsf_lt20;
    etabin = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(eta))); // careful, different convention
    ptbin  = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(pt)));
    out *= hist->GetBinContent(etabin,ptbin)+var*hist->GetBinError(etabin,ptbin);
    }
    if (_histo_recoToLoose_leptonSF_gsf_gt20 && pt>=20){
    hist = _histo_recoToLoose_leptonSF_gsf_gt20;
    etabin = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(eta))); // careful, different convention
    ptbin  = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(pt)));
    out *= hist->GetBinContent(etabin,ptbin)+var*hist->GetBinError(etabin,ptbin);
    }

    if (out<=0) std::cout << "ERROR in electron recoToLoose SF: " << out << std::endl;
    return out;
  }

  std::cout << "ERROR in recoToLoose SF" << std::endl;
  std::abort();
  return 1;

}

TFile *_file_looseToTight_leptonSF_mu_2lss = NULL;
TH2F *_histo_looseToTight_leptonSF_mu_2lss = NULL;
TFile *_file_looseToTight_leptonSF_el_2lss = NULL;
TH2F *_histo_looseToTight_leptonSF_el_2lss = NULL;
TFile *_file_looseToTight_leptonSF_mu_3l = NULL;
TH2F *_histo_looseToTight_leptonSF_mu_3l = NULL;
TFile *_file_looseToTight_leptonSF_el_3l = NULL;
TH2F *_histo_looseToTight_leptonSF_el_3l = NULL;

float _get_looseToTight_leptonSF_ttH(int pdgid, float pt, float eta, int nlep){

  if (!_histo_looseToTight_leptonSF_mu_2lss) {
    _file_looseToTight_leptonSF_mu_2lss = new TFile("../../data/leptonSF/lepMVAEffSF_m_2lss.root","read");
    _histo_looseToTight_leptonSF_mu_2lss = (TH2F*)(_file_looseToTight_leptonSF_mu_2lss->Get("sf"));
  }
  if (!_histo_looseToTight_leptonSF_el_2lss) {
    _file_looseToTight_leptonSF_el_2lss = new TFile("../../data/leptonSF/lepMVAEffSF_e_2lss.root","read");
    _histo_looseToTight_leptonSF_el_2lss = (TH2F*)(_file_looseToTight_leptonSF_el_2lss->Get("sf"));
  }
  if (!_histo_looseToTight_leptonSF_mu_3l) {
    _file_looseToTight_leptonSF_mu_3l = new TFile("../../data/leptonSF/lepMVAEffSF_m_3l.root","read");
    _histo_looseToTight_leptonSF_mu_3l = (TH2F*)(_file_looseToTight_leptonSF_mu_3l->Get("sf"));
  }
  if (!_histo_looseToTight_leptonSF_el_3l) {
    _file_looseToTight_leptonSF_el_3l = new TFile("../../data/leptonSF/lepMVAEffSF_e_3l.root","read");
    _histo_looseToTight_leptonSF_el_3l = (TH2F*)(_file_looseToTight_leptonSF_el_3l->Get("sf"));
  }

  TH2F *hist = 0;
  if (abs(pdgid)==13) hist = (nlep>2) ? _histo_looseToTight_leptonSF_mu_3l : _histo_looseToTight_leptonSF_mu_2lss;
  else if (abs(pdgid)==11) hist = (nlep>2) ? _histo_looseToTight_leptonSF_el_3l : _histo_looseToTight_leptonSF_el_2lss;
  if (!hist) {std::cout << "ERROR in looseToTight SF" << std::endl; std::abort();}
  int ptbin  = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(pt)));
  int etabin = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(fabs(eta))));
  return hist->GetBinContent(ptbin,etabin);

}

float leptonSF_ttH(int pdgid, float pt, float eta, int nlep, float var=0){

  float recoToLoose = _get_recoToLoose_leptonSF_ttH(pdgid,pt,eta,nlep,var);
  float looseToTight = _get_looseToTight_leptonSF_ttH(pdgid,pt,eta,nlep); // var is ignored in all cases for the tight part (systematics handled as nuisance parameter)
  float res = recoToLoose*looseToTight;
  if (!(res>0)) {std::cout << "ERROR in leptonSF " << res << std::endl; std::abort();}
  return res;

}

float leptonSF_ttH_var(int pdgid, float pt, float eta, int nlep, float var_e, float var_m){

  if (abs(pdgid)==11) return (var_e==0) ? 1 : leptonSF_ttH(pdgid,pt,eta,nlep,var_e)/leptonSF_ttH(pdgid,pt,eta,nlep);
  if (abs(pdgid)==13) return (var_m==0) ? 1 : leptonSF_ttH(pdgid,pt,eta,nlep,var_m)/leptonSF_ttH(pdgid,pt,eta,nlep);

  return 1;

}

//TFile *file_triggerSF_ttH = NULL;
//TH2Poly* t2poly_triggerSF_ttH_mm = NULL;
//TH2Poly* t2poly_triggerSF_ttH_ee = NULL;
//TH2Poly* t2poly_triggerSF_ttH_em = NULL;
//TH2Poly* t2poly_triggerSF_ttH_3l = NULL;

// float triggerSF_ttH(int pdgid1, float pt1, int pdgid2, float pt2, int nlep, float shift = 0){

//   if (nlep>=3) return 1.0+shift*0.05;

//   int comb = abs(pdgid1)+abs(pdgid2);

//   if (comb==22) return (pt1<30) ? (0.937+shift*0.027) : (0.991+shift*0.002); // ee
//   else if (comb==24) { // em
//     if (pt1<35) return 0.952+shift*0.008;
//     else if (pt1<50) return 0.983+shift*0.003;
//     else return 1.0+shift*0.001;
//   }
//   else if (comb==26) return (pt1<35) ? (0.972+shift*0.006) : (0.994+shift*0.001); // mm

//   std::cout << "ERROR: triggerSF_ttH called with wrong input, returning 1" << std::endl;
//   return 1;

// }

//float triggerSF_ttH(int pdgid1, float pt1, int pdgid2, float pt2, int nlep, float var=0){
//
//  if (!file_triggerSF_ttH) {
//    file_triggerSF_ttH = new TFile("../../data/triggerSF/trig_eff_map_v4.root");
//    t2poly_triggerSF_ttH_mm = (TH2Poly*)(file_triggerSF_ttH->Get("SSuu2DPt_effic"));
//    t2poly_triggerSF_ttH_ee = (TH2Poly*)(file_triggerSF_ttH->Get("SSee2DPt__effic"));
//    t2poly_triggerSF_ttH_em = (TH2Poly*)(file_triggerSF_ttH->Get("SSeu2DPt_effic"));
//    t2poly_triggerSF_ttH_3l = (TH2Poly*)(file_triggerSF_ttH->Get("__3l2DPt_effic"));
//    if (!(t2poly_triggerSF_ttH_mm && t2poly_triggerSF_ttH_ee && t2poly_triggerSF_ttH_em && t2poly_triggerSF_ttH_3l)) {
//	std::cout << "Impossible to load trigger scale factors!" << std::endl;
//	file_triggerSF_ttH->ls();
//	file_triggerSF_ttH = NULL;
//      }
//  }
//  TH2Poly* hist = NULL;
//  if (nlep==2){
//    if (abs(pdgid1)==13 && abs(pdgid2)==13) hist = t2poly_triggerSF_ttH_mm;
//    else if (abs(pdgid1)==11 && abs(pdgid2)==11) hist = t2poly_triggerSF_ttH_ee;
//    else hist = t2poly_triggerSF_ttH_em;
//  }
//  else if (nlep==3) hist = t2poly_triggerSF_ttH_3l;
//  else std::cout << "Wrong options to trigger scale factors" << std::endl;
//  pt1 = std::max(float(hist->GetXaxis()->GetXmin()+1e-5), std::min(float(hist->GetXaxis()->GetXmax()-1e-5), pt1));
//  pt2 = std::max(float(hist->GetYaxis()->GetXmin()+1e-5), std::min(float(hist->GetYaxis()->GetXmax()-1e-5), pt2));
//  int bin = hist->FindBin(pt1,pt2);
//  float eff = hist->GetBinContent(bin) + var * hist->GetBinError(bin);
//
//  if (nlep>2) return eff;
//  int cat = (abs(pdgid1)==11) + (abs(pdgid2)==11);
//  if (cat==2) return eff*1.02;
//  else if (cat==1) return eff*1.02;
//  else return eff*1.01;
//
//
//}


float ttH_2lss_ifflav(int LepGood1_pdgId, int LepGood2_pdgId, float ret_ee, float ret_em, float ret_mm){
  if (abs(LepGood1_pdgId)==11 && abs(LepGood2_pdgId)==11) return ret_ee;
  if ((abs(LepGood1_pdgId) != abs(LepGood2_pdgId)))       return ret_em;
  if (abs(LepGood1_pdgId)==13 && abs(LepGood2_pdgId)==13) return ret_mm;
  std::cerr << "ERROR: invalid input " << abs(LepGood1_pdgId) << ", " << abs(LepGood1_pdgId) << std::endl;
  assert(0);
  return 0; // avoid warning
}
float ttH_2lss_ifflavnb(int LepGood1_pdgId, int LepGood2_pdgId, int nBJetMedium25, float ret_ee, float ret_em_bl, float ret_em_bt, float ret_mm_bl, float ret_mm_bt){
  if (abs(LepGood1_pdgId)==11 && abs(LepGood2_pdgId)==11) return ret_ee;
  if ((abs(LepGood1_pdgId) != abs(LepGood2_pdgId)) && nBJetMedium25 < 2) return ret_em_bl;
  if ((abs(LepGood1_pdgId) != abs(LepGood2_pdgId)) && nBJetMedium25 >= 2) return ret_em_bt;
  if (abs(LepGood1_pdgId)==13 && abs(LepGood2_pdgId)==13 && nBJetMedium25 < 2) return ret_mm_bl;
  if (abs(LepGood1_pdgId)==13 && abs(LepGood2_pdgId)==13 && nBJetMedium25 >= 2) return ret_mm_bt;
  std::cerr << "ERROR: invalid input " << abs(LepGood1_pdgId) << ", " << abs(LepGood1_pdgId) <<  ", " << nBJetMedium25 << std::endl;
  assert(0);
  return 0; // avoid warning
}

float ttH_3l_ifflav(int LepGood1_pdgId, int LepGood2_pdgId, int LepGood3_pdgId){
  if (abs(LepGood1_pdgId)==11 && abs(LepGood2_pdgId)==11 && abs(LepGood3_pdgId)==11) return 1;
  if ((abs(LepGood1_pdgId) + abs(LepGood2_pdgId) + abs(LepGood3_pdgId)) == 35)       return 2;
  if ((abs(LepGood1_pdgId) + abs(LepGood2_pdgId) + abs(LepGood3_pdgId)) == 37)       return 3;
  if (abs(LepGood1_pdgId)==13 && abs(LepGood2_pdgId)==13 && abs(LepGood3_pdgId)==13) return 4;
  return -1;
}

std::vector<int> boundaries_runPeriod2016 = {272007,275657,276315,276831,277772,278820,280919};
std::vector<int> boundaries_runPeriod2017 = {297020,299337,302030,303435,304911};
std::vector<int> boundaries_runPeriod2018 = {315252,316998,319313,320394};

std::vector<double> lumis_runPeriod2016 = {5.75, 2.573, 4.242, 4.025, 3.105, 7.576, 8.651};
std::vector<double> lumis_runPeriod2017 = {4.802,9.629,4.235,9.268,13.433};
std::vector<double> lumis_runPeriod2018 = {13.978 , 7.064 , 6.899 , 31.748};

bool cumul_lumis_isInit = false;
std::vector<float> cumul_lumis_runPeriod2016;
std::vector<float> cumul_lumis_runPeriod2017;
std::vector<float> cumul_lumis_runPeriod2018;

int runPeriod(int run, int year){
  std::vector<int> boundaries;
  if (year == 2016)
    boundaries = boundaries_runPeriod2016;
  else if (year == 2017)
    boundaries = boundaries_runPeriod2017;
  else if (year == 2018)
    boundaries = boundaries_runPeriod2018;
  else{
    std::cout << "Wrong year " << year << std::endl;
    return -99;
  }
  auto period = std::find_if(boundaries.begin(),boundaries.end(),[run](const int &y){return y>run;});
  return std::distance(boundaries.begin(),period)-1 + ( (year == 2017) ? 7 : 0 ) + ( (year == 2018) ? 12 : 0 ) ;
}

TRandom3 rand_generator_RunDependentMC(0);
int hashBasedRunPeriod2017(int isData, int run, int lumi, int event, int year){
  if (isData) return runPeriod(run,year);
  if (!cumul_lumis_isInit){
    cumul_lumis_runPeriod2016.push_back(0);
    cumul_lumis_runPeriod2017.push_back(0);
    cumul_lumis_runPeriod2018.push_back(0);
    float tot_lumi_2016 = std::accumulate(lumis_runPeriod2016.begin(),lumis_runPeriod2016.end(),float(0.0));
    float tot_lumi_2017 = std::accumulate(lumis_runPeriod2017.begin(),lumis_runPeriod2017.end(),float(0.0));
    float tot_lumi_2018 = std::accumulate(lumis_runPeriod2018.begin(),lumis_runPeriod2018.end(),float(0.0));

    for (uint i=0; i<lumis_runPeriod2016.size(); i++) cumul_lumis_runPeriod2016.push_back(cumul_lumis_runPeriod2016.back()+lumis_runPeriod2016[i]/tot_lumi_2016);
    for (uint i=0; i<lumis_runPeriod2017.size(); i++) cumul_lumis_runPeriod2017.push_back(cumul_lumis_runPeriod2017.back()+lumis_runPeriod2017[i]/tot_lumi_2017);
    for (uint i=0; i<lumis_runPeriod2018.size(); i++) cumul_lumis_runPeriod2018.push_back(cumul_lumis_runPeriod2018.back()+lumis_runPeriod2018[i]/tot_lumi_2018);
    cumul_lumis_isInit = true;
  }
  Int_t x = 161248*run+2136324*lumi+12781432*event;
  unsigned int hash = TString::Hash(&x,sizeof(Int_t));
  rand_generator_RunDependentMC.SetSeed(hash);
  float val = rand_generator_RunDependentMC.Uniform();
  
  vector<float> cumul;
  if (year == 2016) cumul = cumul_lumis_runPeriod2016;
  else if (year == 2017) cumul = cumul_lumis_runPeriod2017;
  else if (year == 2018) cumul = cumul_lumis_runPeriod2018;
  else{
    std::cout << "Wrong year " << year << std::endl;
    return -99;
  }
  auto period = std::find_if(cumul.begin(),cumul.end(),[val](const float &y){return y>val;});
  return std::distance(cumul.begin(),period)-1 + ( (year == 2017) ? 7 : 0 ) + ( (year == 2018) ? 12 : 0 );
}

float smoothBFlav(float jetpt, float ptmin, float ptmax, int year, float scale_loose=1.0) {
    float wploose[3]  = { 0.0614, 0.0521, 0.0494 };
    float wpmedium[3] = { 0.3093, 0.3033, 0.2770 };
    float x = std::min(std::max(0.f, jetpt - ptmin)/(ptmax-ptmin), 1.f); 
    return x*wploose[year-2016]*scale_loose + (1-x)*wpmedium[year-2016];
}

float ttH_4l_clasifier(float nJet25,float nBJetMedium25,float mZ2){
 
  if ( abs(mZ2 -91.2)<10) return 1;
  if ((abs(mZ2-91.2) > 10) && nJet25==0) return 2;
  if ( (abs(mZ2-91.2) > 10) && nJet25>=0 && nBJetMedium25==1) return 3;
  if ( (abs(mZ2-91.2) > 10) && nJet25>=1 && nBJetMedium25>1) return 4;

  else return -1;
}

float ttH_3l_clasifier(float nJet25,float nBJetMedium25){

  if ((nJet25 == 1)*(nBJetMedium25 == 0)) return 1;
  if ((nJet25 == 2)*(nBJetMedium25 == 0)) return 2;
  if ((nJet25 == 3)*(nBJetMedium25 == 0)) return 3;
  if ((nJet25>3)*(nBJetMedium25 == 0))    return 4;
  if ((nJet25 == 2)*(nBJetMedium25 == 1)) return 5;
  if ((nJet25 == 3)*(nBJetMedium25 == 1)) return 6;
  if ((nJet25 == 4)*(nBJetMedium25 == 1)) return 7;
  if ((nJet25>4)*(nBJetMedium25 == 1))    return 8;
  if ((nJet25 == 2)*(nBJetMedium25>1))    return 9;
  if ((nJet25 == 3)*(nBJetMedium25>1))    return 10;
  if ((nJet25 == 4)*(nBJetMedium25>1))    return 11;
  if ((nJet25>4)*(nBJetMedium25>1))       return 12;
  else return -1;
}


float triggerSF_ttH(int pdgid1, float pt1, int pdgid2, float pt2, int nlep, int year, int var=0){
  if (nlep == 2){
    if (abs(pdgid1*pdgid2) == 121){
      if (year == 2016){
	if (pt2 < 25){
	  return 0.98*(1 + var*0.02);
	}
      else return 1.*(1 + var*0.02);
      }
      if (year == 2017){
	if (pt2<40) return 0.98*(1 + var*0.01);
	else return 1*(1 + var*0.01);
      }
      if (year == 2018){
	if (pt2<25){
	return 0.98*(1 + var*0.01);
	}
	else return 1.*(1 + var*0.01);
      }
    }
    
    else if ( abs(pdgid1*pdgid2) == 143){
      if (year == 2016) return 1.*(1 + var*0.01);
      if (year == 2017){
	if (pt2<40) return 0.98*(1 + var*0.01);
	else return 0.99*(1 + var*0.01);
      }
      if (year == 2018){
	if (pt2<25) return 0.98*(1 + var*0.01);
	else        return 1*(1 + var*0.01);
      }
    }
    else{
      if (year == 2016) return 0.99*(1 + var*0.01);
      if (year == 2017){
	if (pt2 < 40) return 0.97*(1 + var*0.02);
	else if (pt2 < 55 && pt2>40) return 0.995*(1 + var*0.02);
	else if (pt2 < 70 && pt2>55) return 0.96*(1 + var*0.02);
	else                         return 0.94*(1 + var*0.02);
      }
      if (year == 2018){
	if (pt1 < 40) return 1.01*(1 + var*0.01);
	if (pt1 < 70) return 0.995*(1 + var*0.01);
	else return 0.98*(1 + var*0.01);
      }
    }
    
  }
  else return 1.;
}
