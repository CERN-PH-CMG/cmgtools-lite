#include "TFile.h"
#include "TH2.h"
#include "TH2Poly.h"
#include "TSpline.h"
#include "TCanvas.h"
#include "TGraphAsymmErrors.h"
#include "TLorentzVector.h"
#include "EgammaAnalysis/ElectronTools/interface/ElectronEnergyCalibratorRun2Standalone.h"
#include "EgammaAnalysis/ElectronTools/interface/SimpleElectronStandalone.h"

#include <iostream>
#include <stdlib.h>

TFile *_file_recoToMedium_leptonSF_el = NULL;
TH2F *_histo_recoToMedium_leptonSF_el = NULL;
TFile *_file_recoToLoose_leptonSF_el = NULL;
TH2F *_histo_recoToLoose_leptonSF_el = NULL;
TFile *_file_elereco_leptonSF_gsf = NULL;
TH2F *_histo_elereco_leptonSF_gsf = NULL;

float _get_electronSF_recoToCustomTight(int pdgid, float pt, float eta, float var) {

  if (!_histo_elereco_leptonSF_gsf) {
    _file_elereco_leptonSF_gsf = new TFile("../postprocessing/data/leptonSF/EGM2D_eleGSF.root","read");
    _histo_elereco_leptonSF_gsf = (TH2F*)(_file_elereco_leptonSF_gsf->Get("EGamma_SF2D"));
    _histo_elereco_leptonSF_gsf->Smooth(1,"k3a");
  }

  if (!_histo_recoToMedium_leptonSF_el) {
    _file_recoToMedium_leptonSF_el = new TFile("../postprocessing/data/leptonSF/EGM2D_eleCutBasedMediumWP.root","read");
    _histo_recoToMedium_leptonSF_el = (TH2F*)(_file_recoToMedium_leptonSF_el->Get("EGamma_SF2D"));
    _histo_recoToMedium_leptonSF_el->Smooth(1,"k3a");
  }

  if (!_histo_recoToLoose_leptonSF_el) {
    _file_recoToLoose_leptonSF_el = new TFile("../postprocessing/data/leptonSF/EGM2D_eleCutBasedLooseWP.root","read");
    _histo_recoToLoose_leptonSF_el = (TH2F*)(_file_recoToLoose_leptonSF_el->Get("EGamma_SF2D"));
    _histo_recoToLoose_leptonSF_el->Smooth(1,"k3a");
  }

  if(abs(pdgid)==11) {
    TH2F *histMedium = _histo_recoToMedium_leptonSF_el;
    TH2F *histLoose = _histo_recoToLoose_leptonSF_el;
    int etabin = std::max(1, std::min(histMedium->GetNbinsX(), histMedium->GetXaxis()->FindBin(eta)));
    int ptbin  = std::max(1, std::min(histMedium->GetNbinsY(), histMedium->GetYaxis()->FindBin(pt)));
    float out = 0;
    if(fabs(eta)<1.479) out = histLoose->GetBinContent(etabin,ptbin)+var*histLoose->GetBinError(etabin,ptbin);
    else out = histMedium->GetBinContent(etabin,ptbin)+var*histMedium->GetBinError(etabin,ptbin);

    TH2F *hist = _histo_elereco_leptonSF_gsf;
    etabin = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(eta)));
    ptbin  = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(pt)));
    out *= (hist->GetBinContent(etabin,ptbin)+var*(hist->GetBinError(etabin,ptbin) + 0.01*((pt<20) || (pt>80))));

    return out;
  }

  return 0;

}

TFile *_file_eltrg_leptonSF_2D = NULL;
TH2F *_histo_eltrg_leptonSF_2D = NULL;
TFile *_file_eltrg_leptonSF_1D = NULL;
TH1F *_histo_eltrg_leptonSF_1D = NULL;
std::vector<TSpline3*> _splines_trg;
bool _cache_splines = false;

float _get_electronSF_trg_top(int pdgid, float pt, float eta, int ndim, float var) {

  if (!_histo_eltrg_leptonSF_2D) {
    _file_eltrg_leptonSF_2D = new TFile("../postprocessing/data/leptonSF/el_trg/HLT_Ele32_eta2p1_WPTight_Gsf_FullRunRange.root","read");
    _histo_eltrg_leptonSF_2D = (TH2F*)(_file_eltrg_leptonSF_2D->Get("SF"));
  }

  if(abs(pdgid)==11) {
    TH2F *hist = _histo_eltrg_leptonSF_2D;
    int etabin = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(eta)));
    int ptbin  = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(pt)));
    float out = hist->GetBinContent(etabin,ptbin)+var*hist->GetBinError(etabin,ptbin);
    return out;
  }

  return 0.;
  
}

void _smoothTrgSF(TH2F* hist) {
  if(_cache_splines) return;
  _splines_trg.clear();
  double *x=0, *y=0;
  //  TCanvas c1;
  for(int ptbin=0; ptbin<hist->GetNbinsX()+1; ++ptbin) {
    int nbinseta = hist->GetNbinsY();
    if(x) delete x;
    x = new double[nbinseta];
    if(y) delete y;
    y = new double[nbinseta];
    for(int etabin=1; etabin<hist->GetNbinsY()+1; ++etabin) {
      x[etabin-1] = hist->GetYaxis()->GetBinCenter(etabin);
      y[etabin-1] = hist->GetBinContent(ptbin,etabin);
    }
    char name[50];
    sprintf(name,"smooth_ptbin_%d",ptbin);
    TSpline3 *spline = new TSpline3(name,x,y,hist->GetNbinsY());
    // spline->Draw();
    // c1.SaveAs((std::string(name)+".png").c_str());
    _splines_trg.push_back(spline);
  }
  _cache_splines = true;
}

float _get_electronSF_trg(int pdgid, float pt, float eta, int ndim, float var, bool smooth=true) {

  if (!_histo_eltrg_leptonSF_2D) {
    _file_eltrg_leptonSF_2D = new TFile("../postprocessing/data/leptonSF/el_trg/v5/sf/passHLT/eff2D.root","read");
    _histo_eltrg_leptonSF_2D = (TH2F*)(_file_eltrg_leptonSF_2D->Get("s2c_eff"));
  }

  if (!_histo_eltrg_leptonSF_1D) {
    _file_eltrg_leptonSF_1D = new TFile("../postprocessing/data/leptonSF/el_trg/v5/eta/passHLT/eff1D.root","read");
    _histo_eltrg_leptonSF_1D = (TH1F*)(_file_eltrg_leptonSF_1D->Get("s1c_eff"));
  }

  if(abs(pdgid)==11) {
    float out=0;
    if(ndim==2) {
      TH2F *hist = _histo_eltrg_leptonSF_2D;
      int ptbin  = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(pt))); // different convention for axes
      int etabin = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(eta)));
      if (!smooth) out = hist->GetBinContent(ptbin,etabin)+var*hist->GetBinError(ptbin,etabin);
      else {
        if(!_cache_splines) _smoothTrgSF(hist);
        TSpline3 *spline = _splines_trg[ptbin];
        out = spline->Eval(eta)+var*hist->GetBinError(ptbin,etabin);
      }
      if (fabs(eta)>1.479) out = std::min(double(out),1.1); // crazy values in EE- 
      // correct way would do a weighted average of the run-dep SFs. Here something rough from slide 5 of HLT eff talk
      if (fabs(eta)>1.479) out *= 0.96;
      if (pt<40 && fabs(eta)<1.479) out *= (0.00887*pt + 0.637); // measured turn on on Z->ee after v6 SFs
      if (pt<35 && fabs(eta)>1.479) out *= (0.032*pt - 0.117); // measured turn on on Z->ee after v6 SFs
    } else {
      TH1F *hist = _histo_eltrg_leptonSF_1D;
      int etabin = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(eta)));
      out = hist->GetBinContent(etabin)+var*hist->GetBinError(etabin);
    }
    return out;
  }

  return 0;

}

TFile *_file_elofflineWP_1D = NULL;
TH2F *_histo_elofflineWP_1D = NULL;

float _get_electronSF_offlineWP_residual(float eta) {

  if (!_histo_elofflineWP_1D) {
    _file_elofflineWP_1D = new TFile("../postprocessing/data/leptonSF/el_eta_offlineWP_SF.root");
    _histo_elofflineWP_1D = (TH2F*)(_file_elofflineWP_1D->Get("etal2_data"));
  }
  TH2F *hist = _histo_elofflineWP_1D;
  int etabin = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(eta)));
  float out = sqrt(hist->GetBinContent(etabin));
  return out;

}

float leptonSF_We(int pdgid, float pt, float eta, float var=0) {

  float recoToStdWP = _get_electronSF_recoToCustomTight(pdgid,pt,eta,var);
  float stdWPToAnaWP = _get_electronSF_offlineWP_residual(eta);
  float res = std::max(0.,double(recoToStdWP*stdWPToAnaWP));
  return res;

}

float trgSF_We(int pdgid, float pt, float eta, int ndim, float var=0) {

  double trg = _get_electronSF_trg(pdgid,pt,eta,ndim,var);
  float res = std::max(0.,trg);
  return res;

}

#include "TRandom.h"
TRandom3 *rng = NULL;
ElectronEnergyCalibratorRun2Standalone *calibratorData = NULL;
ElectronEnergyCalibratorRun2Standalone *calibratorMC = NULL;

float ptCorr(float pt, float eta, float phi, float r9, int run, int isData) {
  if(!calibratorData && isData ) calibratorData = new ElectronEnergyCalibratorRun2Standalone(false,false,"CMGTools/MonoXAnalysis/python/postprocessing/data/leptonScale/el/Run2016_legacyrereco");
  if(!calibratorMC && !isData ) calibratorMC = new ElectronEnergyCalibratorRun2Standalone(true,false,"CMGTools/MonoXAnalysis/python/postprocessing/data/leptonScale/el/Run2016_legacyrereco");
  ElectronEnergyCalibratorRun2Standalone *calibrator = isData ? calibratorData : calibratorMC;

  if(!isData) {
    if(!rng) rng = new TRandom3();
    rng->SetSeed(0); // make it really random across different jobs
    calibrator->initPrivateRng(rng);
  }

  TLorentzVector oldMomentum;
  oldMomentum.SetPtEtaPhiM(pt,eta,phi,0.51e-3);
  float p = oldMomentum.E();
  SimpleElectron electron(run,-1,r9,p,0,p,0,p,0,p,0,eta,fabs(eta)<1.479,!isData,1,0);
  calibrator->calibrate(electron);
  float scale = electron.getNewEnergy()/p;
  // std::cout << "isData = " << isData << " run = " << run 
  //           << "pt,eta,phi,r9 = " << pt << " " << eta << " " << phi << " " << r9 
  //           << "  SCALE = " << scale << std::endl;
  return pt * scale;
}

TFile *_file_residualcorr_scale = NULL;
TH2D *_histo_residualcorr_scale = NULL;

float residualScale(float pt, float eta, int isData) {
  if(!isData) return 1.;

  if(!_histo_residualcorr_scale) {
    _file_residualcorr_scale = new TFile("../postprocessing/data/leptonScale/el/plot_dm_diff.root");
    _histo_residualcorr_scale = (TH2D*)(_file_residualcorr_scale->Get("plot_dm_diff"));
  }
  
  TH2D *hist = _histo_residualcorr_scale;
  int etabin  = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(fabs(eta))));
  int ptbin = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(pt)));
  
  const float MZ0 = 91.1876;
  float scale = 1. - hist->GetBinContent(etabin,ptbin)/MZ0/sqrt(2.);
  return scale;
}

float ptElFull(float pt, float eta, float phi, float r9, int run, int isData, int nSigma=0) {
  float relSyst=0.;
  if(fabs(eta)<1.0) relSyst = 0.0015;  
  else if(fabs(eta)<1.479) relSyst = 0.005;  
  else relSyst = 0.01; 
  return (1.+nSigma*relSyst) * ptCorr(pt,eta,phi,r9,run,isData) * residualScale(pt,eta,isData);
}

float ptElFullUp(float pt, float eta, float phi, float r9, int run, int isData) {
  return ptElFull(pt,eta,phi,r9,run,isData,1);
}

float ptElFullDn(float pt, float eta, float phi, float r9, int run, int isData) {
  return ptElFull(pt,eta,phi,r9,run,isData,-1);
}
