#include "TH2.h"
#include "TROOT.h"
#include "TFile.h"

const float x_1 = -0.5;
const float x_2 = 0.4;
const float x_3 = 0.7;
const float y_1 = -0.5;
const float y_2 = 0.4;
const float y_3 = 0.7;

const float a_1 = -0.3;
const float a_2 = 0.3; 
const float a_3 = 0.7; 
const float b_1 = -0.3;
const float b_2 = 0.2; 
const float b_3 = 0.6; 

const float u_1 = -0.5;
const float u_2 = 0.4;
const float u_3 = 0.7;
const float v_1 = -0.4;
const float v_2 = 0.4;
const float v_3 = 0.7;

const float r_1 = -0.5;
const float r_2 = 0.3; //0.4
const float r_3 = 0.7;
const float s_1 = -0.3; //-0.4
const float s_2 = 0.3; //0.4

const float p_1 = -0.4;
const float p_2 = 0.4;
const float p_3 = 0.6;
const float q_1 = -0.4;
const float q_2 = 0.3;
const float q_3 = 0.5;

const float w_1 = -0.4;
const float w_2 = 0.4;
const float w_3 = 0.7;
const float z_1 = -0.5;
const float z_2 = 0.2;

float tHq_MVAto1D_3l_16(float mva_tt, float mva_ttv){
/*
These are sorted roughly in increasing signal yield.
 1 ---------------------
   |  6 |  8 | 13 | 16 |
   |----|----|----|----|
   |  4 | 11 | 15 | 14 |
 0 |----|----|----|----|
   |  2 | 10 | 12 |  9 |
   |----|----|----|----|
   |  1 |  3 |  5 |  7 |
-1 |----|----|----|----|
  -1         0         1
*/
    if( mva_tt  > x_3  && mva_ttv  >  y_3 ) return 16;
    if( mva_tt  > x_2  && mva_ttv  >  y_3 ) return 13;
    if( mva_tt  > x_1  && mva_ttv  >  y_3 ) return 8;
    if( mva_tt >= -1.0 && mva_ttv  >  y_3 ) return 6;

    if( mva_tt  > x_3  && mva_ttv  >  y_2 ) return 14;
    if( mva_tt  > x_2  && mva_ttv  >  y_2 ) return 15;
    if( mva_tt  > x_1  && mva_ttv  >  y_2 ) return 11;
    if( mva_tt >= -1.0 && mva_ttv  >  y_2 ) return 4;

    if( mva_tt  > x_3  && mva_ttv  >  y_1 ) return 9;
    if( mva_tt  > x_2  && mva_ttv  >  y_1 ) return 12;
    if( mva_tt  > x_1  && mva_ttv  >  y_1 ) return 10;
    if( mva_tt >= -1.0 && mva_ttv  >  y_1 ) return 2;

    if( mva_tt  > x_3  && mva_ttv >= -1.0 ) return 7;
    if( mva_tt  > x_2  && mva_ttv >= -1.0 ) return 5;
    if( mva_tt  > x_1  && mva_ttv >= -1.0 ) return 3;
    if( mva_tt >= -1.0 && mva_ttv >= -1.0 ) return 1;

    return 0;
}

float tHq_MVAto1D_3l_12(float mva_tt, float mva_ttv){
/*
Same as above but with merged bins:
   8 + 11
   6 + 4 + 2
   7 + 5
New bins are:
 1 ---------------------
   |    |    |  9 | 12 |
   |    |  8 |----|----|
   |  2 |    | 11 | 10 |
 0 |    |----|----|----|
   |    |  7 |  6 |  5 | 
   |----|----|----|----|
   |  1 |  3 |    4    |
-1 |----|----|----|----|
  -1         0         1
*/
    if( mva_tt  > x_3  && mva_ttv  >  y_3 ) return 12;
    if( mva_tt  > x_2  && mva_ttv  >  y_3 ) return 9;
    if( mva_tt  > x_1  && mva_ttv  >  y_3 ) return 8;
    if( mva_tt >= -1.0 && mva_ttv  >  y_3 ) return 2;

    if( mva_tt  > x_3  && mva_ttv  >  y_2 ) return 10;
    if( mva_tt  > x_2  && mva_ttv  >  y_2 ) return 11;
    if( mva_tt  > x_1  && mva_ttv  >  y_2 ) return 8;
    if( mva_tt >= -1.0 && mva_ttv  >  y_2 ) return 2;

    if( mva_tt  > x_3  && mva_ttv  >  y_1 ) return 5;
    if( mva_tt  > x_2  && mva_ttv  >  y_1 ) return 6;
    if( mva_tt  > x_1  && mva_ttv  >  y_1 ) return 7;
    if( mva_tt >= -1.0 && mva_ttv  >  y_1 ) return 2;

    if( mva_tt  > x_3  && mva_ttv >= -1.0 ) return 4;
    if( mva_tt  > x_2  && mva_ttv >= -1.0 ) return 4;
    if( mva_tt  > x_1  && mva_ttv >= -1.0 ) return 3;
    if( mva_tt >= -1.0 && mva_ttv >= -1.0 ) return 1;

    return 0;
}

float tHq_MVAto1D_3l_new(float mva_tt, float mva_ttv){
    if( mva_tt  > u_3  && mva_ttv  >  v_3 ) return 10;
    if( mva_tt  > u_2  && mva_ttv  >  v_3 ) return 9;
    if( mva_tt  > u_1  && mva_ttv  >  v_3 ) return 6;
    if( mva_tt >= -1.0 && mva_ttv  >  v_3 ) return 5;

    if( mva_tt  > u_3  && mva_ttv  >  v_2 ) return 8;
    if( mva_tt  > u_2  && mva_ttv  >  v_2 ) return 7;
    if( mva_tt  > u_1  && mva_ttv  >  v_2 ) return 6;
    if( mva_tt >= -1.0 && mva_ttv  >  v_2 ) return 5;

    if( mva_tt  > u_3  && mva_ttv  >  v_1 ) return 4;
    if( mva_tt  > u_2  && mva_ttv  >  v_1 ) return 4;
    if( mva_tt  > u_1  && mva_ttv  >  v_1 ) return 2;
    if( mva_tt >= -1.0 && mva_ttv  >  v_1 ) return 5;

    if( mva_tt  > u_3  && mva_ttv >= -1.0 ) return 3;
    if( mva_tt  > u_2  && mva_ttv >= -1.0 ) return 3;
    if( mva_tt  > u_1  && mva_ttv >= -1.0 ) return 3;
    if( mva_tt >= -1.0 && mva_ttv >= -1.0 ) return 1;

    return 0;
}

float tHq_MVAto1D_3l_8(float mva_tt, float mva_ttv){
    if( mva_tt  > r_3  && mva_ttv  >  s_2 ) return 8;
    if( mva_tt  > r_2  && mva_ttv  >  s_2 ) return 7;
    if( mva_tt  > r_1  && mva_ttv  >  s_2 ) return 6;
    if( mva_tt >= -1.0 && mva_ttv  >  s_2 ) return 4;

    if( mva_tt  > r_3  && mva_ttv  >  s_1 ) return 5;
    if( mva_tt  > r_2  && mva_ttv  >  s_1 ) return 5;
    if( mva_tt  > r_1  && mva_ttv  >  s_1 ) return 2;
    if( mva_tt >= -1.0 && mva_ttv  >  s_1 ) return 4;

    if( mva_tt  > r_3  && mva_ttv >= -1.0 ) return 3;
    if( mva_tt  > r_2  && mva_ttv >= -1.0 ) return 3;
    if( mva_tt  > r_1  && mva_ttv >= -1.0 ) return 3;
    if( mva_tt >= -1.0 && mva_ttv >= -1.0 ) return 1;

    return 0;
}


float tHq_MVAto1D_3l_10(float mva_tt, float mva_ttv){
/*
Same as above but with merged bins:
   3 + 4
   6 + 5
New bins are:
 1 ---------------------
   |    |    |  9 | 10 |
   |    |  6 |----|----|
   |  5 |    |  7 |  8 |
 0 |    |----|----|----|
   |    |  2 |    4    | 
   |----|----|----|----|
   |  1 |      3       |
-1 |----|----|----|----|
  -1         0         1
*/
    if( mva_tt  > x_3  && mva_ttv  >  y_3 ) return 10; 
    if( mva_tt  > x_2  && mva_ttv  >  y_3 ) return 9;  
    if( mva_tt  > x_1  && mva_ttv  >  y_3 ) return 6;  
    if( mva_tt >= -1.0 && mva_ttv  >  y_3 ) return 5;  

    if( mva_tt  > x_3  && mva_ttv  >  y_2 ) return 8;  
    if( mva_tt  > x_2  && mva_ttv  >  y_2 ) return 7;  
    if( mva_tt  > x_1  && mva_ttv  >  y_2 ) return 6;  
    if( mva_tt >= -1.0 && mva_ttv  >  y_2 ) return 5;  

    if( mva_tt  > x_3  && mva_ttv  >  y_1 ) return 4;  
    if( mva_tt  > x_2  && mva_ttv  >  y_1 ) return 4;  
    if( mva_tt  > x_1  && mva_ttv  >  y_1 ) return 2;  
    if( mva_tt >= -1.0 && mva_ttv  >  y_1 ) return 5;  

    if( mva_tt  > x_3  && mva_ttv >= -1.0 ) return 3;  
    if( mva_tt  > x_2  && mva_ttv >= -1.0 ) return 3;  
    if( mva_tt  > x_1  && mva_ttv >= -1.0 ) return 3;  
    if( mva_tt >= -1.0 && mva_ttv >= -1.0 ) return 1;  

    return 0;
}

float tHq_MVAto1D_2lss_new(float mva_tt, float mva_ttv){
    if( mva_tt  > p_3  && mva_ttv  >  q_3 ) return 9;
    if( mva_tt  > p_2  && mva_ttv  >  q_3 ) return 7;
    if( mva_tt  > p_1  && mva_ttv  >  q_3 ) return 5;
    if( mva_tt >= -1.0 && mva_ttv  >  q_3 ) return 4;

    if( mva_tt  > p_3  && mva_ttv  >  q_2 ) return 10;
    if( mva_tt  > p_2  && mva_ttv  >  q_2 ) return 6;
    if( mva_tt  > p_1  && mva_ttv  >  q_2 ) return 5;
    if( mva_tt >= -1.0 && mva_ttv  >  q_2 ) return 4;

    if( mva_tt  > p_3  && mva_ttv  >  q_1 ) return 8;
    if( mva_tt  > p_2  && mva_ttv  >  q_1 ) return 8;
    if( mva_tt  > p_1  && mva_ttv  >  q_1 ) return 3;
    if( mva_tt >= -1.0 && mva_ttv  >  q_1 ) return 4;

    if( mva_tt  > p_3  && mva_ttv >= -1.0 ) return 2;
    if( mva_tt  > p_2  && mva_ttv >= -1.0 ) return 2;
    if( mva_tt  > p_1  && mva_ttv >= -1.0 ) return 2;
    if( mva_tt >= -1.0 && mva_ttv >= -1.0 ) return 1;

    return 0;
}

float tHq_MVAto1D_2lss_8(float mva_tt, float mva_ttv){
    if( mva_tt  > w_3  && mva_ttv  >  z_2 ) return 8;
    if( mva_tt  > w_2  && mva_ttv  >  z_2 ) return 7;
    if( mva_tt  > w_1  && mva_ttv  >  z_2 ) return 6;
    if( mva_tt >= -1.0 && mva_ttv  >  z_2 ) return 4;

    if( mva_tt  > w_3  && mva_ttv  >  z_1 ) return 5;
    if( mva_tt  > w_2  && mva_ttv  >  z_1 ) return 5;
    if( mva_tt  > w_1  && mva_ttv  >  z_1 ) return 2;
    if( mva_tt >= -1.0 && mva_ttv  >  z_1 ) return 4;

    if( mva_tt  > w_3  && mva_ttv >= -1.0 ) return 3;
    if( mva_tt  > w_2  && mva_ttv >= -1.0 ) return 3;
    if( mva_tt  > w_1  && mva_ttv >= -1.0 ) return 3;
    if( mva_tt >= -1.0 && mva_ttv >= -1.0 ) return 1;

    return 0;
}

float tHq_MVAto1D_2lss_10(float mva_tt, float mva_ttv){
/*
Same as above but with merged bins:
   3 + 4
   6 + 5
New bins are:
 1 ---------------------
   |    |    |  7 |  9 |
   |    |  5 |----|----|
   |  4 |    |  6 | 10 |
 0 |    |----|----|----|
   |    |  3 |    8    | 
   |----|----|----|----|
   |  1 |      2       |
-1 |----|----|----|----|
  -1         0         1
*/
    if( mva_tt  > a_3  && mva_ttv  >  b_3 ) return 9;   
    if( mva_tt  > a_2  && mva_ttv  >  b_3 ) return 7;  
    if( mva_tt  > a_1  && mva_ttv  >  b_3 ) return 5;  
    if( mva_tt >= -1.0 && mva_ttv  >  b_3 ) return 4;  

    if( mva_tt  > a_3  && mva_ttv  >  b_2 ) return 10; 
    if( mva_tt  > a_2  && mva_ttv  >  b_2 ) return 6;  
    if( mva_tt  > a_1  && mva_ttv  >  b_2 ) return 5;  
    if( mva_tt >= -1.0 && mva_ttv  >  b_2 ) return 4;  

    if( mva_tt  > a_3  && mva_ttv  >  b_1 ) return 8;  
    if( mva_tt  > a_2  && mva_ttv  >  b_1 ) return 8;  
    if( mva_tt  > a_1  && mva_ttv  >  b_1 ) return 3;  
    if( mva_tt >= -1.0 && mva_ttv  >  b_1 ) return 4;  

    if( mva_tt  > a_3  && mva_ttv >= -1.0 ) return 2;  
    if( mva_tt  > a_2  && mva_ttv >= -1.0 ) return 2;  
    if( mva_tt  > a_1  && mva_ttv >= -1.0 ) return 2;  
    if( mva_tt >= -1.0 && mva_ttv >= -1.0 ) return 1;  

    return 0;
}

float tHq_MVAto1D_2lss_12(float mva_tt, float mva_ttv){
/*
Same as above but with merged bins:
   6 + 8
   2 + 4
   3 + 5
   7 + 9
New bins are:
 1 ---------------------
   |   10    | 11 | 12 |
   |----|----|----|----|
   |    |  7 |  9 |  8 |
 0 |  2 |----|----|----|
   |    |  6 |  5 |    | 
   |----|----|----|  4 |
   |  1 |    3    |    |
-1 |----|----|----|----|
  -1         0         1
*/
    if( mva_tt  > a_3  && mva_ttv  >  b_3 ) return 12;
    if( mva_tt  > a_2  && mva_ttv  >  b_3 ) return 11;
    if( mva_tt  > a_1  && mva_ttv  >  b_3 ) return 10;
    if( mva_tt >= -1.0 && mva_ttv  >  b_3 ) return 10;

    if( mva_tt  > a_3  && mva_ttv  >  b_2 ) return 9;
    if( mva_tt  > a_2  && mva_ttv  >  b_2 ) return 8;
    if( mva_tt  > a_1  && mva_ttv  >  b_2 ) return 7;
    if( mva_tt >= -1.0 && mva_ttv  >  b_2 ) return 2;

    if( mva_tt  > a_3  && mva_ttv  >  b_1 ) return 4;
    if( mva_tt  > a_2  && mva_ttv  >  b_1 ) return 5;
    if( mva_tt  > a_1  && mva_ttv  >  b_1 ) return 6;
    if( mva_tt >= -1.0 && mva_ttv  >  b_1 ) return 2;

    if( mva_tt  > a_3  && mva_ttv >= -1.0 ) return 4;
    if( mva_tt  > a_2  && mva_ttv >= -1.0 ) return 3;
    if( mva_tt  > a_1  && mva_ttv >= -1.0 ) return 3;
    if( mva_tt >= -1.0 && mva_ttv >= -1.0 ) return 1;
    return 0;
}

//class GetTHQBinning
//{
//public:
//    GetTHQBinning(TString fileName2l="tHq-multilepton/signal_extraction/binning_2l.root",
//                  TString fileName3l="tHq-multilepton/signal_extraction/binning_3l.root",
//                  TString histname="hTargetBinning");
//    Int_t GetCluster2l(Double_t, Double_t);
//    Int_t GetCluster3l(Double_t, Double_t);
//protected:
//    TFile* file2l;
//    TFile* file3l;
//    TH2F* hBinning2l;
//    TH2F* hBinning3l;
//};
//
//GetTHQBinning::GetTHQBinning(TString fileName2l, TString fileName3l, TString histname){
//    file2l = (TFile*) gROOT->GetListOfFiles()->FindObject(fileName2l);
//    file3l = (TFile*) gROOT->GetListOfFiles()->FindObject(fileName3l);
//    if (!file2l || !file2l->IsOpen()) file2l = TFile::Open(fileName2l);
//    if (!file3l || !file3l->IsOpen()) file3l = TFile::Open(fileName3l);
//    hBinning2l = (TH2F*) file2l->Get(histname);
//    hBinning3l = (TH2F*) file3l->Get(histname);
//}
//
//Int_t GetTHQBinning::GetCluster2l( Double_t x, Double_t y){
//    return hBinning2l->GetBinContent( hBinning2l->FindBin(x,y) );
//}
//
//Int_t GetTHQBinning::GetCluster3l( Double_t x, Double_t y){
//    return hBinning3l->GetBinContent( hBinning3l->FindBin(x,y) );
//}
//
//GetTHQBinning SBRatioClustering;
//Int_t tHq_MVAto1D_2lss_sbratio(Double_t x, Double_t y){
//    return SBRatioClustering.GetCluster2l(x,y)+1;
//}
//
//Int_t tHq_MVAto1D_3l_sbratio(Double_t x, Double_t y){
//    return SBRatioClustering.GetCluster3l(x,y)+1;
//}
//
//GetTHQBinning KMeansBinning = GetTHQBinning(
//                            "tHq-multilepton/signal_extraction/binning_kmeans_2l.root",    // 10 bins
//                            "tHq-multilepton/signal_extraction/binning_kmeans_3l_5.root",  // 5 bins
//                            "hBinning");
//Int_t tHq_MVAto1D_2lss_kmeans(Double_t x, Double_t y){
//    return KMeansBinning.GetCluster2l(x,y)+1;
//}
//
//Int_t tHq_MVAto1D_3l_kmeans(Double_t x, Double_t y){
//    return KMeansBinning.GetCluster3l(x,y)+1;
//}


float fwdjet_eventWeight_25(float eta){
/*
Return an event weight based on the data/MC ratio of the maxJetEta25
distribution in OS emu events.
Forward jet pt cut of 25 GeV
*/
  eta = fabs(eta);
  if(eta < 0.278) return 1.0925;
  if(eta < 0.556) return 1.0920;
  if(eta < 0.833) return 1.0675;
  if(eta < 1.111) return 1.0888;
  if(eta < 1.389) return 1.0759;
  if(eta < 1.667) return 1.0109;
  if(eta < 1.944) return 1.0727;
  if(eta < 2.222) return 1.0715;
  if(eta < 2.500) return 1.0112;
  if(eta < 2.778) return 1.0387;
  if(eta < 3.056) return 0.9687;
  if(eta < 3.333) return 0.8137;
  if(eta < 3.611) return 0.9010;
  if(eta < 3.889) return 0.8685;
  if(eta < 4.167) return 0.9277;
  if(eta < 4.444) return 0.8111;
  if(eta < 4.722) return 0.6497;
  if(eta < 5.000) return 1.0000;
  return 1.0;
}

float fwdjet_eventWeight_30(float eta){
/*
Return an event weight based on the data/MC ratio of the maxJetEta25_30
distribution in OS emu events.
Forward jet pt cut of 30 GeV
*/
  eta = fabs(eta);
  if(eta < 0.278) return 1.0566;
  if(eta < 0.556) return 1.0617;
  if(eta < 0.833) return 1.0459;
  if(eta < 1.111) return 1.0593;
  if(eta < 1.389) return 1.0508;
  if(eta < 1.667) return 0.9847;
  if(eta < 1.944) return 1.0448;
  if(eta < 2.222) return 1.0457;
  if(eta < 2.500) return 0.9871;
  if(eta < 2.778) return 0.9942;
  if(eta < 3.056) return 0.9427;
  if(eta < 3.333) return 0.8695;
  if(eta < 3.611) return 0.9387;
  if(eta < 3.889) return 0.8887;
  if(eta < 4.167) return 0.9466;
  if(eta < 4.444) return 0.8278;
  if(eta < 4.722) return 0.6485;
  if(eta < 5.000) return 1.0000;
  return 1.0;
}

float fwdjet_eventWeight_40(float eta){
/*
Return an event weight based on the data/MC ratio of the maxJetEta25_40
distribution in OS emu events.
Forward jet pt cut of 40 GeV
*/
  eta = fabs(eta);
  if(eta < 0.278) return 1.0326;
  if(eta < 0.556) return 1.0407;
  if(eta < 0.833) return 1.0244;
  if(eta < 1.111) return 1.0340;
  if(eta < 1.389) return 1.0322;
  if(eta < 1.667) return 0.9661;
  if(eta < 1.944) return 1.0239;
  if(eta < 2.222) return 1.0169;
  if(eta < 2.500) return 0.9746;
  if(eta < 2.778) return 0.9816;
  if(eta < 3.056) return 0.9200;
  if(eta < 3.333) return 0.9092;
  if(eta < 3.611) return 0.9807;
  if(eta < 3.889) return 0.9213;
  if(eta < 4.167) return 1.0135;
  if(eta < 4.444) return 0.8637;
  if(eta < 4.722) return 0.6367;
  if(eta < 5.000) return 1.0000;
  return 1.0;
}

float fwdjet_eventWeight_50(float eta){
/*
Return an event weight based on the data/MC ratio of the maxJetEta25_50
distribution in OS emu events.
Forward jet pt cut of 50 GeV
*/
  eta = fabs(eta);
  if(eta < 0.278) return 1.0233;
  if(eta < 0.556) return 1.0288;
  if(eta < 0.833) return 1.0211;
  if(eta < 1.111) return 1.0265;
  if(eta < 1.389) return 1.0146;
  if(eta < 1.667) return 0.9701;
  if(eta < 1.944) return 1.0112;
  if(eta < 2.222) return 1.0077;
  if(eta < 2.500) return 0.9747;
  if(eta < 2.778) return 0.9808;
  if(eta < 3.056) return 0.9525;
  if(eta < 3.333) return 0.9095;
  if(eta < 3.611) return 1.0222;
  if(eta < 3.889) return 0.9123;
  if(eta < 4.167) return 1.0626;
  if(eta < 4.444) return 0.8832;
  if(eta < 4.722) return 0.5845;
  if(eta < 5.000) return 1.0000;
  return 1.0;
}

float fwdjet_eventWeight_2017_option0(float eta){
/*
Return an event weight based on the data/MC ratio of the maxJetEta25
distribution in OS emu events.
All jet cut at 25 GeV.
*/
  eta = fabs(eta);
  if(eta < 0.278) return 0.8876;
  if(eta < 0.556) return 0.8845;
  if(eta < 0.833) return 0.8854;
  if(eta < 1.111) return 0.8922;
  if(eta < 1.389) return 0.9186;
  if(eta < 1.667) return 0.9347;
  if(eta < 1.944) return 0.9189;
  if(eta < 2.222) return 0.9451;
  if(eta < 2.500) return 0.9260;
  if(eta < 2.778) return 1.0786;
  if(eta < 3.056) return 2.0302;
  if(eta < 3.333) return 0.9231;
  if(eta < 3.611) return 1.0778;
  if(eta < 3.889) return 1.0270;
  if(eta < 4.167) return 1.0097;
  if(eta < 4.444) return 0.8161;
  if(eta < 4.722) return 0.5824;
  if(eta < 5.000) return 1.0000;
  return 1.0;
}

float fwdjet_eventWeight_2017_option1(float eta){
/*
Return an event weight based on the data/MC ratio of the maxJetEta25_40
distribution in OS emu events.
Central jet pt cut 25 GeV, forward jet pt cut 40 GeV.
*/
  eta = fabs(eta);
  if(eta < 0.278) return 0.9504;
  if(eta < 0.556) return 0.9541;
  if(eta < 0.833) return 0.9482;
  if(eta < 1.111) return 0.9578;
  if(eta < 1.389) return 0.9906;
  if(eta < 1.667) return 1.0003;
  if(eta < 1.944) return 0.9896;
  if(eta < 2.222) return 1.0188;
  if(eta < 2.500) return 0.9843;
  if(eta < 2.778) return 1.0564;
  if(eta < 3.056) return 1.5379;
  if(eta < 3.333) return 0.9840;
  if(eta < 3.611) return 1.1136;
  if(eta < 3.889) return 1.0121;
  if(eta < 4.167) return 1.0243;
  if(eta < 4.444) return 0.8865;
  if(eta < 4.722) return 0.5877;
  if(eta < 5.000) return 1.0000;
  return 1.0;
}

float fwdjet_eventWeight_2017_option2(float eta){
/*
Return an event weight based on the data/MC ratio of the maxJetEta25
distribution in OS emu events.
All jet pt cut 25 GeV. Events where 2.7 < maxJetEta25 < 3.0 are rejected.
*/
  eta = fabs(eta);
  if(eta < 0.278) return 1.0057;
  if(eta < 0.556) return 1.00570.9447;
  if(eta < 0.833) return 1.00570.9457;
  if(eta < 1.111) return 1.00570.9528;
  if(eta < 1.389) return 1.00570.9811;
  if(eta < 1.667) return 1.00570.9982;
  if(eta < 1.944) return 1.00570.9814;
  if(eta < 2.222) return 1.00571.0093;
  if(eta < 2.500) return 1.00570.9889;
  if(eta < 2.778) return 1.00571.0259;
  if(eta < 3.056) return 1.00571.3785;
  if(eta < 3.333) return 1.00570.9859;
  if(eta < 3.611) return 1.00571.1512;
  if(eta < 3.889) return 1.00571.0969;
  if(eta < 4.167) return 1.00571.0784;
  if(eta < 4.444) return 1.00570.8716;
  if(eta < 4.722) return 1.00570.6220;
  if(eta < 5.000) return 1.0000;
  return 1.0;
}

float fwdjet_eventWeight_2017_option2_modified(float eta){
/*
Return an event weight based on the data/MC ratio of the maxJetEta25
distribution in OS emu events.
All jet pt cut 25 GeV. Events where any fwd jet abs(eta) is between 2.7 and 3.0 are rejected.
*/
  eta = fabs(eta);
  if(eta < 0.278) return 0.8773;
  if(eta < 0.556) return 0.8185;
  if(eta < 0.833) return 0.8447;
  if(eta < 1.111) return 0.8459;
  if(eta < 1.389) return 0.8408;
  if(eta < 1.667) return 0.8972;
  if(eta < 1.944) return 0.8670;
  if(eta < 2.222) return 0.8876;
  if(eta < 2.500) return 0.8941;
  if(eta < 2.778) return 1.0149;
  if(eta < 3.056) return 1.9081;
  if(eta < 3.333) return 0.9533;
  if(eta < 3.611) return 1.1167;
  if(eta < 3.889) return 1.0622;
  if(eta < 4.167) return 1.0601;
  if(eta < 4.444) return 0.8323;
  if(eta < 4.722) return 0.5956;
  if(eta < 5.000) return 1.0000;
  return 1.0;
}

float fwdjet_eventWeight_2017_option3(float eta){
/*
Return an event weight based on the data/MC ratio of the maxJetEta25
distribution in OS emu events.
All jet pt cut 25 GeV, except if 2.7 < maxJetEta25 < 3.0, fwdJetPt25 > 60.
*/
  eta = fabs(eta);
  if(eta < 0.278) return 0.9997; 
  if(eta < 0.556) return 0.9546;
  if(eta < 0.833) return 0.9551;
  if(eta < 1.111) return 0.9494;
  if(eta < 1.389) return 0.9818;
  if(eta < 1.667) return 0.9988;
  if(eta < 1.944) return 0.9741;
  if(eta < 2.222) return 1.0035;
  if(eta < 2.500) return 0.9832;
  if(eta < 2.778) return 1.0279;
  if(eta < 3.056) return 1.3393;
  if(eta < 3.333) return 0.9846;
  if(eta < 3.611) return 1.1491;
  if(eta < 3.889) return 1.0955;
  if(eta < 4.167) return 1.0754;
  if(eta < 4.444) return 0.8703;
  if(eta < 4.722) return 0.6205;
  if(eta < 5.000) return 1.0000;
  return 1.0;
}

float fwdjet_eventWeight_2017_option3_modified(float eta){
/*
Return an event weight based on the data/MC ratio of the maxJetEta25_60
distribution in OS emu events.
All jet pt cut 25 GeV, except if 2.7 < ans(eta) < 3.0, pt > 60.
*/
  eta = fabs(eta);
  if(eta < 0.278) return 0.9715;
  if(eta < 0.556) return 0.9639;
  if(eta < 0.833) return 0.9647;
  if(eta < 1.111) return 0.9721;
  if(eta < 1.389) return 1.0045;
  if(eta < 1.667) return 1.0176;
  if(eta < 1.944) return 1.0046;
  if(eta < 2.222) return 1.0235;
  if(eta < 2.500) return 1.0121;
  if(eta < 2.778) return 1.0744;
  if(eta < 3.056) return 1.2978;
  if(eta < 3.333) return 0.9398;
  if(eta < 3.611) return 1.0973;
  if(eta < 3.889) return 1.0456;
  if(eta < 4.167) return 1.0279;
  if(eta < 4.444) return 0.8308;
  if(eta < 4.722) return 0.5930;
  if(eta < 5.000) return 1.0000;
  return 1.0;
}
