#include <cmath>
#include <assert.h>
#include "Math/GenVector/LorentzVector.h"
#include "Math/GenVector/PtEtaPhiM4D.h"
#include "Math/GenVector/PxPyPzM4D.h"
#include "Math/GenVector/Boost.h"
#include "TLorentzVector.h"
#include "TGraphAsymmErrors.h"
#include "TH2F.h"
#include "TFile.h"

TFile *_file_recoToLoose_leptonSF_mu_sos_barrel = NULL;
TGraphAsymmErrors *_histo_recoToLoose_leptonSF_mu_sos_barrel = NULL;
TFile *_file_recoToLoose_leptonSF_mu_sos_endcap = NULL;
TGraphAsymmErrors *_histo_recoToLoose_leptonSF_mu_sos_endcap = NULL;

TFile *_file_recoToLoose_leptonSF_mu_sos_all_highpt = NULL;
//TGraphAsymmErrors *_histo_recoToLoose_leptonSF_mu_sos_barrel_highpt = NULL;
TH1F *_histo_recoToLoose_leptonSF_mu_sos_all_highpt = NULL;

TFile *_file_recoToLoose_leptonSF_mu_sos_endcap_highpt = NULL;
//TGraphAsymmErrors *_histo_recoToLoose_leptonSF_mu_sos_endcap_highpt = NULL;


int get_bin_recoToLoose(float pt){
  if(pt> 3.0 && pt<=3.5) return 0;
  else if(pt>3.5  && pt<=4.0) return 1;
  else if(pt>4.0  && pt<=4.5) return 2;
  else if(pt>4.5  && pt<=5.0) return 3;
  else if(pt>5.0  && pt<=6.0) return 4;
  else if(pt>6.0  && pt<=7.0) return 5;
  else if(pt>7.0  && pt<=8.0) return 6;
  else if(pt> 8.0 && pt<=10.0) return 7;
  else if(pt> 10.0 && pt<=12.0) return 8;
  else if(pt> 12.0 && pt<=18.0) return 9;
  else if(pt>18.) return 10;
  else assert(0);
}

int get_bin_looseToTight_mu(float pt){
  if(pt> 3.5 && pt<=7.5) return 0;
  else if(pt>7.5  && pt<=10.0) return 1;
  else if(pt>10.0  && pt<=15.0) return 2;
  else if(pt>15.0  && pt<=20.0) return 3;
  else if(pt>20.0  && pt<=30.0) return 4;
  else if(pt>30.0  && pt<=45.0) return 5;
  else if(pt>45.0  && pt<=70.0) return 6;
  else if(pt> 70.0 ) return 7;
  else assert(0);
}

int get_bin_looseToTight_el(float pt){
  if(pt> 5.0 && pt<=12.5) return 0;
  else if(pt>12.5  && pt<=20.0) return 1;
  else if(pt>20.0  && pt<=25.0) return 2;
  else if(pt>25.0  && pt<=40.0) return 3;
  else if(pt>40.0  && pt<=70.0) return 4;
  else if(pt> 70.0 ) return 5;
  else assert(0);
}


float _get_recoToLoose_leptonSF_SOS(int pdgid, float _pt, float eta, float var){

  float pt = std::min(float(199.9),_pt);

  //  if (var!=0) assert(0); // NOT IMPLEMENTED

  if (abs(pdgid)!=13) return 1.0;

  if (!_histo_recoToLoose_leptonSF_mu_sos_barrel) {
    _file_recoToLoose_leptonSF_mu_sos_barrel = new TFile("../../data/sos_lepton_SF/mu_JDGauss_bern3_Loose_barrel_7invfb.root","read");//RECOtoLOOSE -low pT
    _histo_recoToLoose_leptonSF_mu_sos_barrel = ( TGraphAsymmErrors*)(_file_recoToLoose_leptonSF_mu_sos_barrel->Get("mu_JDGauss_bern3_Loose_barrel_ratio"));
  }
  
  if (!_histo_recoToLoose_leptonSF_mu_sos_endcap) {
    _file_recoToLoose_leptonSF_mu_sos_endcap = new TFile("../../data/sos_lepton_SF/mu_JDGauss_bern3_Loose_endcap_7invfb.root","read");//RECOtoLOOSE -low pT
    _histo_recoToLoose_leptonSF_mu_sos_endcap = ( TGraphAsymmErrors*)(_file_recoToLoose_leptonSF_mu_sos_endcap->Get("mu_JDGauss_bern3_Loose_endcap_ratio"));
  }

  if (!_histo_recoToLoose_leptonSF_mu_sos_all_highpt) {
    _file_recoToLoose_leptonSF_mu_sos_all_highpt = new TFile("../../data/sos_lepton_SF/MuonID_Z_RunBCD_prompt80X_7p65.root","read");
    _histo_recoToLoose_leptonSF_mu_sos_all_highpt = ( TH1F*)(_file_recoToLoose_leptonSF_mu_sos_all_highpt->Get("MC_NUM_LooseID_DEN_genTracks_PAR_pt_alleta_bin1/pt_ratio"));
  }
 
  TGraphAsymmErrors *hist_barrel = _histo_recoToLoose_leptonSF_mu_sos_barrel;
  TGraphAsymmErrors *hist_endcap = _histo_recoToLoose_leptonSF_mu_sos_endcap;
  TH1F *hist_all_highpt = _histo_recoToLoose_leptonSF_mu_sos_all_highpt;

  if (pt<25){
    if(abs(eta)<1.2){
      if(var>0) return (hist_barrel->Eval(pt)+hist_barrel->GetErrorYhigh(get_bin_recoToLoose(pt)));
      if(var<0) return (hist_barrel->Eval(pt)-hist_barrel->GetErrorYlow(get_bin_recoToLoose(pt)));
      //cout << pt << "===" << get_bin_recoToLoose(pt) << endl; 
      return  hist_barrel->Eval(pt);
     
    }
    else {
      if(var>0) return (hist_endcap->Eval(pt)+hist_endcap->GetErrorYhigh(get_bin_recoToLoose(pt)));
      if(var<0) return (hist_endcap->Eval(pt)-hist_endcap->GetErrorYlow(get_bin_recoToLoose(pt)));
      return hist_endcap->Eval(pt);
    }
  }
  else{
    Int_t binx = (hist_all_highpt->GetXaxis())->FindBin(pt);
    if(var>0) return (hist_all_highpt->GetBinContent(binx) + 0.01);
    if(var<0) return (hist_all_highpt->GetBinContent(binx) - 0.01);
    return  hist_all_highpt->GetBinContent(binx);
  }

  assert(0);
  return -999;

}

TFile *_file_looseToTight_leptonSF_mu_sos_barrel = NULL;
TGraphAsymmErrors *_histo_looseToTight_leptonSF_mu_sos_barrel = NULL;
TFile *_file_looseToTight_leptonSF_mu_sos_endcap = NULL;
TGraphAsymmErrors *_histo_looseToTight_leptonSF_mu_sos_endcap = NULL;

TFile *_file_looseToTight_leptonSF_el_sos_barrel = NULL;
TGraphAsymmErrors *_histo_looseToTight_leptonSF_el_sos_barrel = NULL;
TFile *_file_looseToTight_leptonSF_el_sos_endcap = NULL;
TGraphAsymmErrors *_histo_looseToTight_leptonSF_el_sos_endcap = NULL;



float _get_looseToTight_leptonSF_SOS(int pdgid, float _pt, float eta, float var){

  float pt = std::min(float(119.9),_pt);

  //if (var!=0) assert(0); // NOT IMPLEMENTED
  
  if (!_histo_looseToTight_leptonSF_mu_sos_barrel) {
    _file_looseToTight_leptonSF_mu_sos_barrel = new TFile("../../data/sos_lepton_SF/mu_SOS_barrel_12invfb.root","read");
    _histo_looseToTight_leptonSF_mu_sos_barrel = (TGraphAsymmErrors*)(_file_looseToTight_leptonSF_mu_sos_barrel->Get("ratio"));
  }
  if (!_histo_looseToTight_leptonSF_mu_sos_endcap) {
    _file_looseToTight_leptonSF_mu_sos_endcap = new TFile("../../data/sos_lepton_SF/mu_SOS_endcap_12invfb.root","read");
    _histo_looseToTight_leptonSF_mu_sos_endcap = (TGraphAsymmErrors*)(_file_looseToTight_leptonSF_mu_sos_endcap->Get("ratio"));
  }
  
  if (!_histo_looseToTight_leptonSF_el_sos_barrel) {
    _file_looseToTight_leptonSF_el_sos_barrel = new TFile("../../data/sos_lepton_SF/el_SOS_barrel_12invfb.root","read");
    _histo_looseToTight_leptonSF_el_sos_barrel = (TGraphAsymmErrors*)(_file_looseToTight_leptonSF_el_sos_barrel->Get("ratio"));
  }
  if (!_histo_looseToTight_leptonSF_el_sos_endcap) {
    _file_looseToTight_leptonSF_el_sos_endcap = new TFile("../../data/sos_lepton_SF/el_SOS_endcap_12invfb.root","read");
    _histo_looseToTight_leptonSF_el_sos_endcap = (TGraphAsymmErrors*)(_file_looseToTight_leptonSF_el_sos_endcap->Get("ratio"));
  }

  if (abs(pdgid)==13){
    TGraphAsymmErrors *hist_mu_barrel = _histo_looseToTight_leptonSF_mu_sos_barrel;
    TGraphAsymmErrors *hist_mu_endcap = _histo_looseToTight_leptonSF_mu_sos_endcap;
    
    if(abs(eta)<1.2){
      if(var>0) return (hist_mu_barrel->Eval(pt) + hist_mu_barrel->GetErrorYhigh(get_bin_looseToTight_mu(pt))) ;
      if(var<0) return (hist_mu_barrel->Eval(pt) - hist_mu_barrel->GetErrorYlow(get_bin_looseToTight_mu(pt))) ;
      return  hist_mu_barrel->Eval(pt);
    }
    if(abs(eta)>1.2){
      if(var>0) return (hist_mu_endcap->Eval(pt) + hist_mu_endcap->GetErrorYhigh(get_bin_looseToTight_mu(pt))) ;
      if(var<0) return (hist_mu_endcap->Eval(pt) - hist_mu_endcap->GetErrorYlow(get_bin_looseToTight_mu(pt))) ;
      return hist_mu_endcap->Eval(pt);
    }
  }
 
  if(abs(pdgid)==11){
    TGraphAsymmErrors *hist_el_barrel = _histo_looseToTight_leptonSF_el_sos_barrel;
    TGraphAsymmErrors *hist_el_endcap = _histo_looseToTight_leptonSF_el_sos_endcap;
    
    if(abs(eta)<1.479){
      if(var>0) return (hist_el_barrel->Eval(pt) + hist_el_barrel->GetErrorYhigh(get_bin_looseToTight_el(pt))) ;
      if(var<0) return (hist_el_barrel->Eval(pt) - hist_el_barrel->GetErrorYlow(get_bin_looseToTight_el(pt))) ;
      return  hist_el_barrel->Eval(pt);
    }
    if(abs(eta)>1.479){
      if(var>0) return (hist_el_endcap->Eval(pt) + hist_el_endcap->GetErrorYhigh(get_bin_looseToTight_el(pt))) ;
      if(var<0) return (hist_el_endcap->Eval(pt) - hist_el_endcap->GetErrorYlow(get_bin_looseToTight_el(pt))) ;
      return hist_el_endcap->Eval(pt);
    }
  }
  
  assert(0);
  return -999;
}

// ---- Tracking (hard-coded so far)  ---------------------------

float _get_tracking_SF(int pdgid, float pt, float eta, float var){

 if (var!=0) assert(0); // NOT IMPLEMENTED

 if (abs(pdgid)!=13) return 1.0;

 if(pt>10){ 
   //---pT>10 GeV-------
   
   if(eta>-2.4 && eta<=-2.1 ){
     return 0.9824;
   } 
   else if(eta>-2.1 && eta<=-1.60 ){
     return 0.9917;
   } 
   else if(eta>-1.60 && eta<=-1.10 ){
     return 0.9959;
   } 
   else if(eta>-1.10 && eta<=-0.6 ){
     return 0.9934;
   } 
   else if(eta>-0.6 && eta<=0.0 ){
     return 0.9915;
   } 
   else if(eta>0.0 && eta<=0.60 ){
     return 0.9947;
   } 
   else if(eta>0.60 && eta<=1.10 ){
     return 0.9967;
   } 
   else if(eta>1.10 && eta<=1.60 ){
     return 0.9949;
   } 
   else if(eta>1.60 && eta<=2.10 ){
     return 0.9912;
   } 
   else if(eta>2.10 && eta<=2.4 ){
     return 0.9768;
   } 
   else{
     return 1.0;
   }
 }

 // --- pT<10 GeV ---
 
 else{

   //-----------------
   if(eta>-2.4 && eta<=-2.1 ){
     return 0.9544;
   } 
   else if(eta>-2.1 && eta<=-1.60 ){
     return 0.9714;
   } 
   else if(eta>-1.60 && eta<=-1.10 ){
     return 0.9691;
   } 
   else if(eta>-1.10 && eta<=-0.6 ){
     return 0.9622;
   } 
   else if(eta>-0.6 && eta<=0.0 ){
     return 0.9586;
   } 
   else if(eta>0.0 && eta<=0.60 ){
     return 0.9703;
   } 
   else if(eta>0.60 && eta<=1.10 ){
     return 0.9764;
   } 
   else if(eta>1.10 && eta<=1.60 ){
     return 0.9729;
   } 
   else if(eta>1.60 && eta<=2.10 ){
     return 0.9711;
   } 
   else if(eta>2.10 && eta<=2.4 ){
     return 0.9412;
   } 
   else{
     return 1.0; 
   }
 }
 
}

// ------------------------------------------

float leptonSF_SOS(int pdgid, float _pt, float eta, float var=0){

  float tracking = _get_tracking_SF(pdgid,_pt,eta,var);
  float recoToLoose = _get_recoToLoose_leptonSF_SOS(pdgid,_pt,eta,var);
  float looseToTight = _get_looseToTight_leptonSF_SOS(pdgid,_pt,eta,var);
  float res = tracking*recoToLoose*looseToTight; 
  assert (res>0);
  return res;
}


// Trigger efficiency ---------------------------

TFile *_file_triggerSF = NULL;
TH2F  *_histo_triggerSF = NULL;

float triggerSF_SOS(float _met, float _met_corr, float var=0){
 
  //  if (var_ee!=0) assert(0); // NOT IMPLEMENTED

  if (_met>=200.0 && _met_corr>=200.0)return 1.0;
  
  if (!_file_triggerSF) {
    _file_triggerSF  = new TFile("../../data/sos_lepton_SF/trigger_eff_12invfb.root","read");
    _histo_triggerSF = (TH2F*)(_file_triggerSF->Get("hnummet"));
  }
 
  float muon_leg_eff=0.95*0.95*0.93; // Mu3 leg * Mu3 leg * DZ
  float met = std::min(float(199.9),_met);
  float met_corr = std::min(float(199.9),_met_corr);

  Int_t binx = (_histo_triggerSF->GetXaxis())->FindBin(met);
  Int_t biny = (_histo_triggerSF->GetYaxis())->FindBin(met_corr);  

  if(var>0) return (muon_leg_eff*(_histo_triggerSF->GetBinContent(binx,biny)))+0.05 ;// +/-5%
  if(var<0) return (muon_leg_eff*(_histo_triggerSF->GetBinContent(binx,biny)))-0.05 ;
  return muon_leg_eff*(_histo_triggerSF->GetBinContent(binx,biny));  

}

void lepton_trigger_SF() {}
