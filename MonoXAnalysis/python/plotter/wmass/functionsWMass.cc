#include "TFile.h"
#include "TH2.h"
#include "TH2Poly.h"
#include "TSpline.h"
#include "TCanvas.h"
#include "TGraphAsymmErrors.h"

#include <iostream>

TFile *_file_recoToTight_leptonSF_el = NULL;
TH2F *_histo_recoToTight_leptonSF_el = NULL;
TFile *_file_elereco_leptonSF_gsf = NULL;
TH2F *_histo_elereco_leptonSF_gsf = NULL;

float _get_electronSF_recoToCustomTight(int pdgid, float pt, float eta, float var) {

  if (!_histo_elereco_leptonSF_gsf) {
    _file_elereco_leptonSF_gsf = new TFile("../postprocessing/data/leptonSF/EGM2D_eleGSF.root","read");
    _histo_elereco_leptonSF_gsf = (TH2F*)(_file_elereco_leptonSF_gsf->Get("EGamma_SF2D"));
    _histo_elereco_leptonSF_gsf->Smooth(1,"k3a");
  }

  if (!_histo_recoToTight_leptonSF_el) {
    _file_recoToTight_leptonSF_el = new TFile("../postprocessing/data/leptonSF/EGM2D_eleCutBasedMediumWP.root","read");
    _histo_recoToTight_leptonSF_el = (TH2F*)(_file_recoToTight_leptonSF_el->Get("EGamma_SF2D"));
    _histo_recoToTight_leptonSF_el->Smooth(1,"k3a");
  }

  if(abs(pdgid)==11) {
    TH2F *hist = _histo_recoToTight_leptonSF_el;
    int etabin = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(eta)));
    int ptbin  = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(pt)));
    float out = hist->GetBinContent(etabin,ptbin)+var*hist->GetBinError(etabin,ptbin);

    hist = _histo_elereco_leptonSF_gsf;
    etabin = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(eta)));
    ptbin  = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(pt)));
    out *= (hist->GetBinContent(etabin,ptbin)+var*(hist->GetBinError(etabin,ptbin) + 0.01*((pt<20) || (pt>80))));

    return out;
  }

  std::cout << "ERROR ele offline SF" << std::endl;
  std::abort();
  return -999;

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

  std::cout << "ERROR Trg SF" << std::endl;
  std::abort();
  return -999;
  
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

  std::cout << "ERROR Trg SF" << std::endl;
  std::abort();
  return -999;

}

float leptonSF_We(int pdgid, float pt, float eta, float var=0) {

  float recoToTight = _get_electronSF_recoToCustomTight(pdgid,pt,eta,var);
  float res = recoToTight;
  if (res<0) {std::cout << "ERROR negative result" << std::endl; std::abort();}
  return res;

}

float trgSF_We(int pdgid, float pt, float eta, int ndim, float var=0) {

  float trg = _get_electronSF_trg(pdgid,pt,eta,ndim,var);
  float res = trg;
  if (res<0) {std::cout << "ERROR negative result" << std::endl; std::abort();}
  return res;

}
