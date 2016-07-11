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

TFile *_file_recoToLoose_leptonSF_mu_sos_barrel_highpt = NULL;
TGraphAsymmErrors *_histo_recoToLoose_leptonSF_mu_sos_barrel_highpt = NULL;
TFile *_file_recoToLoose_leptonSF_mu_sos_endcap_highpt = NULL;
TGraphAsymmErrors *_histo_recoToLoose_leptonSF_mu_sos_endcap_highpt = NULL;


float _get_recoToLoose_leptonSF_SOS(int pdgid, float _pt, float eta, float var){

  float pt = std::min(float(119.9),_pt);

  if (var!=0) assert(0); // NOT IMPLEMENTED

  if (abs(pdgid)!=13) return 1.0;

  if (!_histo_recoToLoose_leptonSF_mu_sos_barrel) {
    _file_recoToLoose_leptonSF_mu_sos_barrel = new TFile("../../data/sos_lepton_SF/mu_Loose_barrel.root","read");
    _histo_recoToLoose_leptonSF_mu_sos_barrel = ( TGraphAsymmErrors*)(_file_recoToLoose_leptonSF_mu_sos_barrel->Get("ratio"));
  }
  
  if (!_histo_recoToLoose_leptonSF_mu_sos_endcap) {
    _file_recoToLoose_leptonSF_mu_sos_endcap = new TFile("../../data/sos_lepton_SF/mu_Loose_endcap.root","read");
    _histo_recoToLoose_leptonSF_mu_sos_endcap = ( TGraphAsymmErrors*)(_file_recoToLoose_leptonSF_mu_sos_endcap->Get("ratio"));
  }

  if (!_histo_recoToLoose_leptonSF_mu_sos_barrel_highpt) {
    _file_recoToLoose_leptonSF_mu_sos_barrel_highpt = new TFile("../../data/sos_lepton_SF/mu_LooseIdOnly_barrel.root","read");
    _histo_recoToLoose_leptonSF_mu_sos_barrel_highpt = ( TGraphAsymmErrors*)(_file_recoToLoose_leptonSF_mu_sos_barrel_highpt->Get("ratio"));
  }
  
  if (!_histo_recoToLoose_leptonSF_mu_sos_endcap_highpt) {
    _file_recoToLoose_leptonSF_mu_sos_endcap_highpt = new TFile("../../data/sos_lepton_SF/mu_LooseIdOnly_endcap.root","read");
    _histo_recoToLoose_leptonSF_mu_sos_endcap_highpt = ( TGraphAsymmErrors*)(_file_recoToLoose_leptonSF_mu_sos_endcap_highpt->Get("ratio"));
  }


  TGraphAsymmErrors *hist_barrel = _histo_recoToLoose_leptonSF_mu_sos_barrel;
  TGraphAsymmErrors *hist_endcap = _histo_recoToLoose_leptonSF_mu_sos_endcap;
  TGraphAsymmErrors *hist_barrel_highpt = _histo_recoToLoose_leptonSF_mu_sos_barrel_highpt;
  TGraphAsymmErrors *hist_endcap_highpt = _histo_recoToLoose_leptonSF_mu_sos_endcap_highpt;

  if (pt<25){
    if(abs(eta)<1.2){
      return  hist_barrel->Eval(pt);
    }
    else {     
      return hist_endcap->Eval(pt);
    }
  }
  else{
    if(abs(eta)<1.2){
      return  hist_barrel_highpt->Eval(pt);
    }
    else {     
      return hist_endcap_highpt->Eval(pt);
    }  
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

  float pt = std::min(float(79.9),_pt);

  if (var!=0) assert(0); // NOT IMPLEMENTED
  
  if (!_histo_looseToTight_leptonSF_mu_sos_barrel) {
    _file_looseToTight_leptonSF_mu_sos_barrel = new TFile("../../data/sos_lepton_SF/mu_SOS_barrel.root","read");
    _histo_looseToTight_leptonSF_mu_sos_barrel = (TGraphAsymmErrors*)(_file_looseToTight_leptonSF_mu_sos_barrel->Get("ratio"));
  }
  if (!_histo_looseToTight_leptonSF_mu_sos_endcap) {
    _file_looseToTight_leptonSF_mu_sos_endcap = new TFile("../../data/sos_lepton_SF/mu_SOS_endcap.root","read");
    _histo_looseToTight_leptonSF_mu_sos_endcap = (TGraphAsymmErrors*)(_file_looseToTight_leptonSF_mu_sos_endcap->Get("ratio"));
  }
  
  if (!_histo_looseToTight_leptonSF_el_sos_barrel) {
    _file_looseToTight_leptonSF_el_sos_barrel = new TFile("../../data/sos_lepton_SF/el_SOS_barrel.root","read");
    _histo_looseToTight_leptonSF_el_sos_barrel = (TGraphAsymmErrors*)(_file_looseToTight_leptonSF_el_sos_barrel->Get("ratio"));
  }
  if (!_histo_looseToTight_leptonSF_el_sos_endcap) {
    _file_looseToTight_leptonSF_el_sos_endcap = new TFile("../../data/sos_lepton_SF/el_SOS_endcap.root","read");
    _histo_looseToTight_leptonSF_el_sos_endcap = (TGraphAsymmErrors*)(_file_looseToTight_leptonSF_el_sos_endcap->Get("ratio"));
  }

  if (abs(pdgid)==13){
    TGraphAsymmErrors *hist_mu_barrel = _histo_looseToTight_leptonSF_mu_sos_barrel;
    TGraphAsymmErrors *hist_mu_endcap = _histo_looseToTight_leptonSF_mu_sos_endcap;
    
    if(abs(eta)<1.2){
      return  hist_mu_barrel->Eval(pt);
    }
    if(abs(eta)>1.2){
      return hist_mu_endcap->Eval(pt);
    }
  }
 
  if(abs(pdgid)==11){
    TGraphAsymmErrors *hist_el_barrel = _histo_looseToTight_leptonSF_el_sos_barrel;
    TGraphAsymmErrors *hist_el_endcap = _histo_looseToTight_leptonSF_el_sos_endcap;
    
    if(abs(eta)<1.479){
      return  hist_el_barrel->Eval(pt);
    }
    if(abs(eta)>1.479){
      return hist_el_endcap->Eval(pt);
    }
  }
  
  assert(0);
  return -999;
}

// ----  With loose IP, for DY CR only --------------------------

TFile *_file_looseToTight_leptonSF_mu_sos_looseIP_barrel = NULL;
TGraphAsymmErrors *_histo_looseToTight_leptonSF_mu_sos_looseIP_barrel = NULL;
TFile *_file_looseToTight_leptonSF_mu_sos_looseIP_endcap = NULL;
TGraphAsymmErrors *_histo_looseToTight_leptonSF_mu_sos_looseIP_endcap = NULL;

TFile *_file_looseToTight_leptonSF_el_sos_looseIP_barrel = NULL;
TGraphAsymmErrors *_histo_looseToTight_leptonSF_el_sos_looseIP_barrel = NULL;
TFile *_file_looseToTight_leptonSF_el_sos_looseIP_endcap = NULL;
TGraphAsymmErrors *_histo_looseToTight_leptonSF_el_sos_looseIP_endcap = NULL;


float _get_looseToTight_leptonSF_looseIP_SOS(int pdgid, float _pt, float eta, float var){

  float pt = std::min(float(79.9),_pt);

  if (var!=0) assert(0); // NOT IMPLEMENTED
  
  if (!_histo_looseToTight_leptonSF_mu_sos_looseIP_barrel) {
    _file_looseToTight_leptonSF_mu_sos_looseIP_barrel = new TFile("../../data/sos_lepton_SF/mu_SOS_003_barrel.root","read"); /// TO BE CHANGED once available from Giovanni
    _histo_looseToTight_leptonSF_mu_sos_looseIP_barrel = (TGraphAsymmErrors*)(_file_looseToTight_leptonSF_mu_sos_looseIP_barrel->Get("ratio"));
  }
  if (!_histo_looseToTight_leptonSF_mu_sos_looseIP_endcap) {
    _file_looseToTight_leptonSF_mu_sos_looseIP_endcap = new TFile("../../data/sos_lepton_SF/mu_SOS_003_endcap.root","read"); /// TO BE CHANGED once available from Giovanni
    _histo_looseToTight_leptonSF_mu_sos_looseIP_endcap = (TGraphAsymmErrors*)(_file_looseToTight_leptonSF_mu_sos_looseIP_endcap->Get("ratio"));
  }
  
  if (!_histo_looseToTight_leptonSF_el_sos_looseIP_barrel) {
    _file_looseToTight_leptonSF_el_sos_looseIP_barrel = new TFile("../../data/sos_lepton_SF/el_SOS_003_barrel.root","read"); 
    _histo_looseToTight_leptonSF_el_sos_looseIP_barrel = (TGraphAsymmErrors*)(_file_looseToTight_leptonSF_el_sos_looseIP_barrel->Get("ratio"));
  }
  if (!_histo_looseToTight_leptonSF_el_sos_looseIP_endcap) {
    _file_looseToTight_leptonSF_el_sos_looseIP_endcap = new TFile("../../data/sos_lepton_SF/el_SOS_003_endcap.root","read");
    _histo_looseToTight_leptonSF_el_sos_looseIP_endcap = (TGraphAsymmErrors*)(_file_looseToTight_leptonSF_el_sos_looseIP_endcap->Get("ratio"));
  }

  if (abs(pdgid)==13){
    TGraphAsymmErrors *hist_mu_barrel = _histo_looseToTight_leptonSF_mu_sos_looseIP_barrel;
    TGraphAsymmErrors *hist_mu_endcap = _histo_looseToTight_leptonSF_mu_sos_looseIP_endcap;
    
    if(abs(eta)<1.2){
      return  hist_mu_barrel->Eval(pt);
    }
    if(abs(eta)>1.2){
      return hist_mu_endcap->Eval(pt);
    }
  }
 
  if(abs(pdgid)==11){
    TGraphAsymmErrors *hist_el_barrel = _histo_looseToTight_leptonSF_el_sos_looseIP_barrel;
    TGraphAsymmErrors *hist_el_endcap = _histo_looseToTight_leptonSF_el_sos_looseIP_endcap;
    
    if(abs(eta)<1.479){
      return  hist_el_barrel->Eval(pt);
    }
    if(abs(eta)>1.479){
      return hist_el_endcap->Eval(pt);
    }
  }
  
  assert(0);
  return -999;
}

// ------------------------------------------

float leptonSF_SOS(int pdgid, float _pt, float eta, float var=0){

  float recoToLoose = _get_recoToLoose_leptonSF_SOS(pdgid,_pt,eta,var);
  float looseToTight = _get_looseToTight_leptonSF_SOS(pdgid,_pt,eta,var);
  float res = recoToLoose*looseToTight;
  assert (res>0);
  return res;
}

// --- For DY only -----------------------------

float leptonSF_DY_SOS(int pdgid, float _pt, float eta, float var=0){

  float recoToLoose = _get_recoToLoose_leptonSF_SOS(pdgid,_pt,eta,var);
  float looseToTight = _get_looseToTight_leptonSF_looseIP_SOS(pdgid,_pt,eta,var);
  float res = recoToLoose*looseToTight;
  assert (res>0);
  return res;
}

// Trigger: hard coded (so far) ---------------------------

float triggerSF_SOS(float met, float met_corr, float var_ee=0){
 
  if (var_ee!=0) assert(0); // NOT IMPLEMENTED
 
  if(met>200 && met_corr>200){ 
    return 1.0;
  }
  else if(met>=125 && met<=150 && met_corr>=125 && met_corr<=150 ){
    return 0.94*0.94*0.93*0.90;
  }
  //-----------------
  else if(met>=125 && met<=150 && met_corr>150 && met_corr<=200 ){
    return 0.94*0.94*0.93*0.93;
  }
  // ----------------
  else if(met>150 && met<=200 && met_corr>=125 && met_corr<=150 ){
    return 0.94*0.94*0.93*0.96;
  }
  else { return 1.0;}
  
}

void lepton_trigger_SF() {}
