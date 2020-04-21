#include <TH2.h>
#include <TFile.h>
#include <cmath>
#include <iostream>
#include <string>
#include <map>

TH2 * FR_mu = 0;
TH2 * FR2_mu = 0;
TH2 * FR3_mu = 0;
TH2 * FR4_mu = 0;
TH2 * FR5_mu = 0;
TH2 * FR_el = 0;
TH2 * FR2_el = 0;
TH2 * FR3_el = 0;
TH2 * FR4_el = 0;
TH2 * FR5_el = 0;
TH2 * QF_el = 0;
TH2 * FRi_mu[99], *FRi_el[99], *FRi_tau[6];
TH2 * QFi_el[99];
TH2 * FR_tau = 0;
TH2 * FR2_tau = 0;
TH2 * FR3_tau = 0;

TH2 * FR_mu_FO1_QCD    = 0;
TH2 * FR_mu_FO1_insitu = 0;
TH2 * FR_mu_FO2_QCD    = 0;
TH2 * FR_mu_FO2_insitu = 0;
TH2 * FR_mu_FO3_QCD    = 0;
TH2 * FR_mu_FO3_insitu = 0;
TH2 * FR_mu_FO4_QCD    = 0;
TH2 * FR_mu_FO4_insitu = 0;
TH2 * FR_el_FO1_QCD    = 0;
TH2 * FR_el_FO1_insitu = 0;
TH2 * FR_el_FO2_QCD    = 0;
TH2 * FR_el_FO2_insitu = 0;
TH2 * FR_el_FO3_QCD    = 0;
TH2 * FR_el_FO3_insitu = 0;
TH2 * FR_el_FO4_QCD    = 0;
TH2 * FR_el_FO4_insitu = 0;
TH2 * FRi_FO_mu[8];
TH2 * FRi_FO_el[8];

TH2 * FR_mu_QCD_iso = 0;
TH2 * FR_mu_QCD_noniso = 0;
TH2 * FR_el_QCD_iso = 0;
TH2 * FR_el_QCD_noniso = 0;
TH2 * FRi_fHT_FO_mu[2];
TH2 * FRi_fHT_FO_el[2];

TH2 * BTAG  = 0;
TH2 * ELSF1 = 0;
TH2 * ELSF2 = 0;
TH2 * ELSF3 = 0;
TH2 * MUSF1 = 0;
TH2 * MUSF2 = 0;
TH2 * MUSF3 = 0;


bool loadFRHisto(const std::string &histoName, const char *file, const char *name) {
    TH2 **histo = 0, **hptr2 = 0;
    TH2 * FR_temp = 0; TH2* QF_el_temp =0 ;
    if      (histoName == "FR_tau") { histo = & FR_tau; hptr2 = & FRi_tau[0]; }
    else if (histoName == "FR_mu")  { histo = & FR_mu;  hptr2 = & FRi_mu[0]; }
    else if (histoName == "FR_el")  { histo = & FR_el;  hptr2 = & FRi_el[0]; }
    else if (histoName == "FR2_mu") { histo = & FR2_mu; hptr2 = & FRi_mu[2]; }
    else if (histoName == "FR2_el") { histo = & FR2_el; hptr2 = & FRi_el[2]; }
    else if (histoName == "FR2_tau"){ histo = & FR2_tau; hptr2 = & FRi_tau[2]; }
    else if (histoName == "FR3_mu") { histo = & FR3_mu; hptr2 = & FRi_mu[3]; }
    else if (histoName == "FR3_el") { histo = & FR3_el; hptr2 = & FRi_el[3]; }
    else if (histoName == "FR3_tau"){ histo = & FR3_tau; hptr2 = & FRi_tau[3]; }
    else if (histoName == "FR4_mu") { histo = & FR4_mu; hptr2 = & FRi_mu[4]; }
    else if (histoName == "FR4_el") { histo = & FR4_el; hptr2 = & FRi_el[4]; }
    else if (histoName == "FR5_mu") { histo = & FR5_mu; hptr2 = & FRi_mu[5]; }
    else if (histoName == "FR5_el") { histo = & FR5_el; hptr2 = & FRi_el[5]; }
    else if (TString(histoName).BeginsWith("FR_mu_i")) {histo = & FR_temp; hptr2 = & FRi_mu[TString(histoName).ReplaceAll("FR_mu_i","").Atoi()];}
    else if (TString(histoName).BeginsWith("FR_el_i")) {histo = & FR_temp; hptr2 = & FRi_el[TString(histoName).ReplaceAll("FR_el_i","").Atoi()];}
    else if (TString(histoName).BeginsWith("QF_el_"))  {histo = & QF_el_temp; hptr2 = & QFi_el[TString(histoName).ReplaceAll("QF_el_","").Atoi()];}
    else if (histoName == "QF_el") histo = & QF_el;
    else if (histoName == "FR_mu_FO1_QCD")  { histo = &FR_mu_FO1_QCD ;  hptr2 = & FRi_FO_mu[0]; }
    else if (histoName == "FR_mu_FO1_insitu")  { histo = &FR_mu_FO1_insitu ;  hptr2 = & FRi_FO_mu[1]; }
    else if (histoName == "FR_mu_FO2_QCD")  { histo = &FR_mu_FO2_QCD ;  hptr2 = & FRi_FO_mu[2]; }
    else if (histoName == "FR_mu_FO2_insitu")  { histo = &FR_mu_FO2_insitu ;  hptr2 = & FRi_FO_mu[3]; }
    else if (histoName == "FR_mu_FO3_QCD")  { histo = &FR_mu_FO3_QCD ;  hptr2 = & FRi_FO_mu[4]; }
    else if (histoName == "FR_mu_FO3_insitu")  { histo = &FR_mu_FO3_insitu ;  hptr2 = & FRi_FO_mu[5]; }
    else if (histoName == "FR_mu_FO4_QCD")  { histo = &FR_mu_FO4_QCD ;  hptr2 = & FRi_FO_mu[6]; }
    else if (histoName == "FR_mu_FO4_insitu")  { histo = &FR_mu_FO4_insitu ;  hptr2 = & FRi_FO_mu[7]; }
    else if (histoName == "FR_el_FO1_QCD")  { histo = &FR_el_FO1_QCD ;  hptr2 = & FRi_FO_el[0]; }
    else if (histoName == "FR_el_FO1_insitu")  { histo = &FR_el_FO1_insitu ;  hptr2 = & FRi_FO_el[1]; }
    else if (histoName == "FR_el_FO2_QCD")  { histo = &FR_el_FO2_QCD ;  hptr2 = & FRi_FO_el[2]; }
    else if (histoName == "FR_el_FO2_insitu")  { histo = &FR_el_FO2_insitu ;  hptr2 = & FRi_FO_el[3]; }
    else if (histoName == "FR_el_FO3_QCD")  { histo = &FR_el_FO3_QCD ;  hptr2 = & FRi_FO_el[4]; }
    else if (histoName == "FR_el_FO3_insitu")  { histo = &FR_el_FO3_insitu ;  hptr2 = & FRi_FO_el[5]; }
    else if (histoName == "FR_el_FO4_QCD")  { histo = &FR_el_FO4_QCD ;  hptr2 = & FRi_FO_el[6]; }
    else if (histoName == "FR_el_FO4_insitu")  { histo = &FR_el_FO4_insitu ;  hptr2 = & FRi_FO_el[7]; }
    else if (histoName == "FR_mu_QCD_iso")  { histo = &FR_mu_QCD_iso ;  hptr2 = & FRi_fHT_FO_mu[0]; }
    else if (histoName == "FR_mu_QCD_noniso")  { histo = &FR_mu_QCD_noniso ;  hptr2 = & FRi_fHT_FO_mu[1]; }
    else if (histoName == "FR_el_QCD_iso")  { histo = &FR_el_QCD_iso ;  hptr2 = & FRi_fHT_FO_el[0]; }
    else if (histoName == "FR_el_QCD_noniso")  { histo = &FR_el_QCD_noniso ;  hptr2 = & FRi_fHT_FO_el[1]; }
    else if (histoName == "BTAG"            )  { histo = &BTAG;  }
    else if (histoName == "ELSF1"           )  { histo = &ELSF1; }
    else if (histoName == "ELSF2"           )  { histo = &ELSF2; }
    else if (histoName == "ELSF3"           )  { histo = &ELSF3; }
    else if (histoName == "MUSF1"           )  { histo = &MUSF1; }
    else if (histoName == "MUSF2"           )  { histo = &MUSF2; }
    else if (histoName == "MUSF3"           )  { histo = &MUSF3; }
    if (histo == 0)  {
        std::cerr << "ERROR: histogram " << histoName << " is not defined in fakeRate.cc." << std::endl;
        return 0;
    }
    TDirectory *here = gDirectory;
    TFile *f = TFile::Open(file);
    if (*histo != 0) {
      if (std::string(name) != (*histo)->GetName()) {
          std::cerr << "WARNING: overwriting histogram " << (*histo)->GetName() << std::endl;
      } else {
          TH2* hnew = (TH2*) f->Get(name);
          if (hnew == 0 || hnew->GetNbinsX() != (*histo)->GetNbinsX() || hnew->GetNbinsY() != (*histo)->GetNbinsY()) {
              std::cerr << "WARNING: overwriting histogram " << (*histo)->GetName() << std::endl;
          } else {
              bool fail = false;
              for (int ix = 1; ix <= (*histo)->GetNbinsX(); ++ix) {
                  for (int iy = 1; iy <= (*histo)->GetNbinsX(); ++iy) {
                      if ((*histo)->GetBinContent(ix,iy) != hnew->GetBinContent(ix,iy)) {
                          fail = true; break;
                      }
                  }
              }
              if (fail) std::cerr << "WARNING: overwriting histogram " << (*histo)->GetName() << std::endl;
          }
      }
      delete *histo;
    }
    if (f->Get(name) == 0) {
        std::cerr << "ERROR: could not find " << name << " in " << file << std::endl;
        *histo = 0;
    } else {
        *histo = (TH2*) f->Get(name)->Clone(name);
        (*histo)->SetDirectory(0);
        if (hptr2) *hptr2 = *histo;
    }
    f->Close();
    here->cd();
    return histo != 0;
}

float fetchFR_ii(float l1pt, float l1eta, int l1pdgId, int iFRmu, int iFRel) 
{
    TH2 *hist1 = (abs(l1pdgId) == 11 ? FRi_el[iFRel] : FRi_mu[iFRmu]);
    if (hist1 == 0) { std::cerr << "ERROR, missing FR for pdgId " << l1pdgId << ", iFR " << (abs(l1pdgId) == 11 ? iFRel : iFRmu) << std::endl; std::abort(); }
    int ptbin1  = std::max(1, std::min(hist1->GetNbinsX(), hist1->GetXaxis()->FindBin(l1pt)));
    int etabin1 = std::max(1, std::min(hist1->GetNbinsY(), hist1->GetYaxis()->FindBin(std::abs(l1eta))));
    double fr1 = hist1->GetBinContent(ptbin1,etabin1);
    if (fr1 < 0)  { std::cerr << "WARNING, FR is " << fr1 << " for " << hist1->GetName() << ", pt " << l1pt << " eta " << l1eta << std::endl; if (fr1<0) std::abort(); }
    return fr1;
}

float fetchFR_i(float l1pt, float l1eta, int l1pdgId, int iFR) 
{
    return fetchFR_ii(l1pt,l1eta,l1pdgId,iFR,iFR);
}

float fakeRateWeight_short_2lss_ii(float l1fr, int l1pass, float l2fr, int l2pass) {
    if (l1pass && l2pass) return 0;
    float ret = -1.0;
    if (!l1pass) { 
        ret *= -l1fr/(1.0f-l1fr);
    }
    if (!l2pass) {
        ret *= -l2fr/(1.0f-l2fr);
    }
    return ret;
}

float fakeRateWeight_2lss_ii(float l1pt, float l1eta, int l1pdgId, bool l1pass,
                             float l2pt, float l2eta, int l2pdgId, bool l2pass, int iFRmu, int iFRel) {
    if (l1pass && l2pass) return 0;
    float ret = -1.0;
    if (!l1pass) { 
        float l1fr = fetchFR_ii(l1pt,l1eta,l1pdgId,iFRmu,iFRel);
        ret *= -l1fr/(1.0f-l1fr);
    }
    if (!l2pass) {
        float l2fr = fetchFR_ii(l2pt,l2eta,l2pdgId,iFRmu,iFRel);
        ret *= -l2fr/(1.0f-l2fr);
    }
    return ret;
}


float fakeRateWeight_2lss_i(float l1pt, float l1eta, int l1pdgId, bool l1pass,
                            float l2pt, float l2eta, int l2pdgId, bool l2pass, int iFR) 
{
    return fakeRateWeight_2lss_ii(l1pt,l1eta,l1pdgId,l1pass, 
                                  l2pt,l2eta,l2pdgId,l2pass,
                                  iFR,iFR);
}

float fakeRateWeight_2lss(float l1pt, float l1eta, int l1pdgId, float l1pass,
                            float l2pt, float l2eta, int l2pdgId, float l2pass) 
{
    return fakeRateWeight_2lss_ii(l1pt,l1eta,l1pdgId,l1pass, 
                                  l2pt,l2eta,l2pdgId,l2pass,
                                  0,0);
}
float fakeRateWeight_2lss_2(float l1pt, float l1eta, int l1pdgId, float l1pass,
                            float l2pt, float l2eta, int l2pdgId, float l2pass) 
{
    return fakeRateWeight_2lss_ii(l1pt,l1eta,l1pdgId,l1pass, 
                                  l2pt,l2eta,l2pdgId,l2pass,
                                  2,2);
}


float chargeFlipWeight_2lss(float l1pt, float l1eta, int l1pdgId, 
                             float l2pt, float l2eta, int l2pdgId) 
{
    if (l1pdgId * l2pdgId > 0) return 0.;
    double w = 0;
    if (abs(l1pdgId) == 11) {
        int ptbin  = std::max(1, std::min(QF_el->GetNbinsX(), QF_el->GetXaxis()->FindBin(l1pt)));
        int etabin = std::max(1, std::min(QF_el->GetNbinsY(), QF_el->GetYaxis()->FindBin(std::abs(l1eta))));
        w += QF_el->GetBinContent(ptbin,etabin);
    }
    if (abs(l2pdgId) == 11) {
        int ptbin  = std::max(1, std::min(QF_el->GetNbinsX(), QF_el->GetXaxis()->FindBin(l2pt)));
        int etabin = std::max(1, std::min(QF_el->GetNbinsY(), QF_el->GetYaxis()->FindBin(std::abs(l2eta))));
        w += QF_el->GetBinContent(ptbin,etabin);
    }
    return w;
}

float chargeFlipWeight_2lss_i(float l1pt, float l1eta, int l1pdgId, 
			      float l2pt, float l2eta, int l2pdgId, int year) 
{
    if (l1pdgId * l2pdgId > 0) return 0.;
    int indx = year-2015;
    double w = 0;
    if (abs(l1pdgId) == 11) {
        int ptbin  = std::max(1, std::min(QFi_el[indx]->GetNbinsX(), QFi_el[indx]->GetXaxis()->FindBin(l1pt)));
        int etabin = std::max(1, std::min(QFi_el[indx]->GetNbinsY(), QFi_el[indx]->GetYaxis()->FindBin(std::abs(l1eta))));
        w += QFi_el[indx]->GetBinContent(ptbin,etabin);
    }
    if (abs(l2pdgId) == 11) {
        int ptbin  = std::max(1, std::min(QFi_el[indx]->GetNbinsX(), QFi_el[indx]->GetXaxis()->FindBin(l2pt)));
        int etabin = std::max(1, std::min(QFi_el[indx]->GetNbinsY(), QFi_el[indx]->GetYaxis()->FindBin(std::abs(l2eta))));
        w += QFi_el[indx]->GetBinContent(ptbin,etabin);
    }
    return w;
}

float chargeFlipBin_2lss(float l1pt, float l1eta) {
    if (std::abs(l1eta) < 1.479) {
        return (l1pt < 20 ? 0 : (l1pt < 50 ? 1 : 2));
    } else {
        return (l1pt < 20 ? 3 : (l1pt < 50 ? 4 : 5));
    }
}

float fakeRateWeight_3l(float l1fr, int l1pass, float l2fr, int l2pass, float l3fr, int l3pass) 
{
    float ret = -1.0f;
    if (!l1pass) ret *=  -l1fr/(1.0f-l1fr);
    if (!l2pass) ret *=  -l2fr/(1.0f-l2fr);
    if (!l3pass) ret *=  -l3fr/(1.0f-l3fr);
    if (ret == -1.0f) ret = 0.0f;
    return ret;
}


float fakeRateWeight_4l_2wp(float l1pt, float l1eta, int l1pdgId, float l1mva,
                        float l2pt, float l2eta, int l2pdgId, float l2mva,
                        float l3pt, float l3eta, int l3pdgId, float l3mva,
                        float l4pt, float l4eta, int l4pdgId, float l4mva,
                        float WP, float WP2)
{
    /// 4 pass: weight  0
    /// 1 fail: weight +f/(1-f)
    /// 2 fail: weight -f*f/(1-f)(1-f)
    //  3 fail: weight +f*f*f/((1-f)(1-f)(1-f)
    //  so, just multiply up factors of -f/(1-f) for each failure
    //  hope it works also for 4l....
    float mvas[]={l1mva-WP, l2mva-WP, l3mva-WP2, l4mva-WP2};
    float pts[]={l1pt, l2pt, l3pt, l4pt};
    float etas[]={fabs(l1eta), fabs(l2eta), fabs(l3eta), fabs(l4eta)};
    int pdgids[]={l1pdgId, l2pdgId, l3pdgId, l4pdgId};
    float ret = -1.0f;
    int ifail = 0;
    for (unsigned int i = 0; i < 4 ; ++i) {
        if (mvas[i] < 0) {
            ifail++;
	    TH2 *hist = (i <= 1 ? (abs(pdgids[i]) == 11 ? FR_el : FR_mu) : (abs(pdgids[i]) == 11 ? FR2_el : FR2_mu));
            int ptbin  = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(pts[i])));
            int etabin = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(etas[i])));
            double fr = hist->GetBinContent(ptbin,etabin);
            ret *= -fr/(1.0f-fr);
        }
    }
    if (ifail > 2) return 0;
    if (ret == -1.0f) ret = 0.0f;
    return ret;
}

float fakeRateWeight_4l_2wp_nf(int nf, float l1pt, float l1eta, int l1pdgId, float l1mva,
                        float l2pt, float l2eta, int l2pdgId, float l2mva,
                        float l3pt, float l3eta, int l3pdgId, float l3mva,
                        float l4pt, float l4eta, int l4pdgId, float l4mva,
                        float WP, float WP2)
{
    /// 4 pass: weight  0
    /// 1 fail: weight +f/(1-f)
    /// 2 fail: weight -f*f/(1-f)(1-f)
    //  3 fail: weight +f*f*f/((1-f)(1-f)(1-f)
    //  so, just multiply up factors of -f/(1-f) for each failure
    //  hope it works also for 4l....
    float mvas[]={l1mva-WP, l2mva-WP, l3mva-WP2, l4mva-WP2};
    float pts[]={l1pt, l2pt, l3pt, l4pt};
    float etas[]={fabs(l1eta), fabs(l2eta), fabs(l3eta), fabs(l4eta)};
    int pdgids[]={l1pdgId, l2pdgId, l3pdgId, l4pdgId};
    float ret = (nf == 1 ? 0.5f : 1.0f);
    int ifail = 0;
    for (unsigned int i = 0; i < 4 ; ++i) {
        if (mvas[i] < 0) {
            ifail++;
	    TH2 *hist = (i <= 1 ? (abs(pdgids[i]) == 11 ? FR_el : FR_mu) : (abs(pdgids[i]) == 11 ? FR2_el : FR2_mu));
            int ptbin  = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(pts[i])));
            int etabin = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(etas[i])));
            double fr = hist->GetBinContent(ptbin,etabin);
            ret *= fr/(1.0f-fr);
        }
    }
    if (ifail != nf) return 0;
    return ret;
}


namespace WP {
    enum WPId { V=0, VL=0, VVL=-1, L=1, M=2, T=3, VT=4, HT=5 } ;
}

float multiIso_singleWP(float LepGood_miniRelIso, float LepGood_jetPtRatiov2, float LepGood_jetPtRelv2, WP::WPId wp) {
    switch (wp) {
        case WP::VT: return LepGood_miniRelIso < 0.09  && (LepGood_jetPtRatiov2>0.84  || LepGood_jetPtRelv2>7.2 );
        case WP::T:  return LepGood_miniRelIso < 0.12  && (LepGood_jetPtRatiov2>0.80  || LepGood_jetPtRelv2>7.2 );
        case WP::M:  return LepGood_miniRelIso < 0.16  && (LepGood_jetPtRatiov2>0.76  || LepGood_jetPtRelv2>7.2 );
        case WP::L:  return LepGood_miniRelIso < 0.20  && (LepGood_jetPtRatiov2>0.69  || LepGood_jetPtRelv2>6.0 );
        case WP::VL: return LepGood_miniRelIso < 0.25  && (LepGood_jetPtRatiov2>0.67  || LepGood_jetPtRelv2>4.4 );
        case WP::VVL: return LepGood_miniRelIso < 0.4;
        default:
            std::cerr << "Working point " << wp << " not implemented for multiIso_singleWP" << std::endl;
            abort();
    }
}

float multiIso_singleWP(float LepGood_miniRelIso, float LepGood_jetPtRatiov2, float LepGood_jetPtRelv2, int wp) {
     WP::WPId wpid = static_cast<WP::WPId>(wp);
     return multiIso_singleWP(LepGood_miniRelIso, LepGood_jetPtRatiov2, LepGood_jetPtRelv2, wpid);
}

float multiIso_multiWP(int LepGood_pdgId, float LepGood_pt, float LepGood_eta, float LepGood_miniRelIso, float LepGood_jetPtRatiov2, float LepGood_jetPtRelv2, WP::WPId wp) {
    switch (wp) {
        case WP::VT: 
           return abs(LepGood_pdgId)==13 ? 
                    multiIso_singleWP(LepGood_miniRelIso,LepGood_jetPtRatiov2,LepGood_jetPtRelv2, WP::VT) :
                    multiIso_singleWP(LepGood_miniRelIso,LepGood_jetPtRatiov2,LepGood_jetPtRelv2, WP::HT) ;
        case WP::T:
           return abs(LepGood_pdgId)==13 ? 
                    multiIso_singleWP(LepGood_miniRelIso,LepGood_jetPtRatiov2,LepGood_jetPtRelv2, WP::T) :
                    multiIso_singleWP(LepGood_miniRelIso,LepGood_jetPtRatiov2,LepGood_jetPtRelv2, WP::VT) ;
        case WP::M:
           return abs(LepGood_pdgId)==13 ? 
                    multiIso_singleWP(LepGood_miniRelIso,LepGood_jetPtRatiov2,LepGood_jetPtRelv2, WP::M) :
                    multiIso_singleWP(LepGood_miniRelIso,LepGood_jetPtRatiov2,LepGood_jetPtRelv2, WP::T) ;
        case WP::L:
           return abs(LepGood_pdgId)==13 ? 
                    multiIso_singleWP(LepGood_miniRelIso,LepGood_jetPtRatiov2,LepGood_jetPtRelv2, WP::L) :
                    multiIso_singleWP(LepGood_miniRelIso,LepGood_jetPtRatiov2,LepGood_jetPtRelv2, WP::M) ;
        case WP::VVL: return LepGood_miniRelIso < 0.4;
        default:
            std::cerr << "Working point " << wp << " not implemented for multiIso_multiWP" << std::endl;
            abort();
    }
}
float multiIso_multiWP(int LepGood_pdgId, float LepGood_pt, float LepGood_eta, float LepGood_miniRelIso, float LepGood_jetPtRatiov2, float LepGood_jetPtRelv2, int wp) {
    return multiIso_multiWP(LepGood_pdgId,LepGood_pt,LepGood_eta,LepGood_miniRelIso,LepGood_jetPtRatiov2,LepGood_jetPtRelv2,WP::WPId(wp));
}


float conept_RA5(int LepGood_pdgId, float LepGood_pt, float LepGood_eta, float LepGood_miniRelIso, float LepGood_jetPtRatiov2, float LepGood_jetPtRelv2) {

  float A = (abs(LepGood_pdgId)==11) ? 0.12 : 0.16;
  float B = (abs(LepGood_pdgId)==11) ? 0.80 : 0.76;
  float C = (abs(LepGood_pdgId)==11) ? 7.2 : 7.2;
  
  if (LepGood_jetPtRelv2>C) return LepGood_pt*(1+std::max(float(LepGood_miniRelIso-A),float(0.)));
  else return std::max(float(LepGood_pt),float(LepGood_pt/LepGood_jetPtRatiov2*B));

}

float conept_RA7(int LepGood_pdgId, float LepGood_pt, float LepGood_eta, float LepGood_miniRelIso, float LepGood_jetPtRatiov2, float LepGood_jetPtRelv2) {

  float A = (abs(LepGood_pdgId)==11) ? 0.16 : 0.20;
  float B = (abs(LepGood_pdgId)==11) ? 0.76 : 0.69;
  float C = (abs(LepGood_pdgId)==11) ? 7.2 : 6.0;

  if (LepGood_jetPtRelv2>C) return LepGood_pt*(1+std::max(float(LepGood_miniRelIso-A),float(0.)));
  else return std::max(float(LepGood_pt),float(LepGood_pt/LepGood_jetPtRatiov2*B));

}

float multiIso_singleWP_relaxFO3(int LepGood_pdgId, float LepGood_pt, float LepGood_CorrConePt, float LepGood_eta, float LepGood_miniRelIso, float LepGood_jetPtRatiov2, float LepGood_jetPtRelv2, WP::WPId wp) {
  assert (wp==2);
  return multiIso_multiWP(LepGood_pdgId,LepGood_pt,LepGood_eta,(LepGood_miniRelIso>=0.4),LepGood_CorrConePt/LepGood_pt*LepGood_jetPtRatiov2,LepGood_jetPtRelv2,wp)>0;
}

float multiIso_singleWP_relaxFO4(int LepGood_pdgId, float LepGood_pt, float LepGood_eta, float LepGood_miniRelIso, float LepGood_jetPtRatiov2, float LepGood_jetPtRelv2, WP::WPId wp) {
  assert (wp==2);
  if (abs(LepGood_pdgId)==13) return (LepGood_miniRelIso<0.4 && (1/LepGood_jetPtRatiov2 < (1/0.76 + LepGood_miniRelIso)));
  else if (abs(LepGood_pdgId)==11) return (LepGood_miniRelIso<0.4 && (1/LepGood_jetPtRatiov2 < (1/0.80 + LepGood_miniRelIso)));
  else assert(false);
  return -1; // make gcc happy
}


float mvaIdSpring15(int LepGood_pdgId, float LepGood_eta, float LepGood_mvaIdSpring15, int wp, int iso_emulation_applied){
  if (abs(LepGood_pdgId)!=11) return 1;

  float eta = fabs(LepGood_eta);

  switch (wp) {

  case WP::VL:
    if (iso_emulation_applied) {
      if (eta<0.8) return LepGood_mvaIdSpring15>-0.155;
      else if (eta<=1.479) return LepGood_mvaIdSpring15>-0.56;
      else return LepGood_mvaIdSpring15>-0.76;
    }
    else {
      if (eta<0.8) return LepGood_mvaIdSpring15>-0.70;
      else if (eta<=1.479) return LepGood_mvaIdSpring15>-0.83;
      else return LepGood_mvaIdSpring15>-0.92;
  }

  case WP::T:
    if (eta<0.8) return LepGood_mvaIdSpring15>0.87;
    else if (eta<=1.479) return LepGood_mvaIdSpring15>0.60;
    else return LepGood_mvaIdSpring15>0.17;

  default:
    std::cerr << "Working point " << wp << " not implemented for mvaIdSpring15" << std::endl;
    abort();
  }
}

float ttHl_ptFO(int LepGood_pdgId, float LepGood_pt, float LepGood_jetPtRatio, float LepGood_mva, float WP) {
    if (LepGood_mva > WP) return LepGood_pt;
    float corr = 1.0;
    if (std::abs(WP-0.65)<0.05) { 
        if (std::abs(LepGood_pdgId) == 11) {
            if (LepGood_pt > 20) corr = 0.85;
            else if (LepGood_pt < 10) corr = 1.0;
            else corr = 0.85+0.015*(20.-LepGood_pt); // interpolate
        } else {
            if (LepGood_pt > 20) corr = 0.76;
            else if (LepGood_pt < 10) corr = 1.0;
            else corr = 0.76+0.024*(20.-LepGood_pt); // interpolate up from 0.75 to 1.0
        }
    } else if (std::abs(WP-0.40)<0.05) { 
        if (std::abs(LepGood_pdgId) == 11) {
            if (LepGood_pt > 20) corr = 0.80;
            else corr = 0.80+0.20*(20.-LepGood_pt)/13.; // interpolate
        } else {
            if (LepGood_pt > 20) corr = 0.74;
            else if (LepGood_pt < 10) corr = 1.0;
            else corr = 0.74+0.026*(20.-LepGood_pt); // interpolate up from 0.74 to 1.0
        }

    } else {
        static int warn = 0; if (++warn < 2) std::cout << "Warning: ttHl_ptFO requested for unexpected WP " << WP << std::endl; 
    }
    return corr * LepGood_pt/LepGood_jetPtRatio;
}
float ttHl_ptFO_ab(int LepGood_pdgId, float LepGood_pt, float LepGood_jetPtRatio, float LepGood_mva, float WP, float a, float b) {
    if (LepGood_mva > WP) return LepGood_pt;
    return std::max(LepGood_pt, a*(LepGood_pt/LepGood_jetPtRatio - b));
}

float EWK3L_fakeRate(float pt, float eta, int pdgId, int var = 1) {
    TH2 *hist = FR_el;
    if(abs(pdgId)==13) hist=FR_mu;
    if(abs(pdgId)==15) hist=FR_tau;
    if(var == 2){
        hist = FR2_el;
        if(abs(pdgId)==13) hist=FR2_mu;
        if(abs(pdgId)==15) hist=FR2_tau;
    }
    if(var == 3){
        hist = FR3_el;
        if(abs(pdgId)==13) hist=FR3_mu;
        if(abs(pdgId)==15) hist=FR3_tau;
    }
    int ptbin  = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(pt)));
    int etabin = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(abs(eta))));
    double fr = hist->GetBinContent(ptbin,etabin);
    if (fr <= 0)  { std::cerr << "WARNING, FR is " << fr << " for " << hist->GetName() << ", pt " << pt << " eta " << eta << std::endl; if (fr<0) std::abort(); }
    return fr/(1-fr);
}

float EWK3L_fakeTransfer(unsigned int nLep, float l1fr    , int l1isFake,
                                            float l2fr    , int l2isFake,
                                            float l3fr    , int l3isFake,
                                            float l4fr = 0, int l4isFake = 0) {

    int nfail = l1isFake + l2isFake + l3isFake + l4isFake;
    if(nLep == 3) nfail = l1isFake + l2isFake + l3isFake;

    if(nfail == 0) return 0;

    float weight = 1;
    if(l1isFake           ) weight *= -1*l1fr;
    if(l2isFake           ) weight *= -1*l2fr;
    if(l3isFake           ) weight *= -1*l3fr;
    if(l4isFake && nLep==4) weight *= -1*l4fr;

    return -1*weight;
}


void fakeRate() {}



float fakeRatePromptRateWeight_2l_ij(float l1pt, float l1eta, int l1pdgId, bool l1pass,
                            float l2pt, float l2eta, int l2pdgId, bool l2pass, int iFR, int iPR, int selhyp=-1, int selfs=11)
{
    // selhyp: -1 = all with at least one fake; 00 = double-fakes; 01 = l1 is fake, 10 = l2 is fake
    // selfs : 11 = pass-pass, 00 = fail-fail, 10 = pass-fail, 01 = fail-pass
    // The math is:
    // 1) 1/(p - f)   for each lepton
    // 2) to predict the yield before selection in a given configuration of prompt and fake, get a factor
    //         pass -> prompt :  ( 1 - f )
    //         pass -> fake   : -( 1 - p )
    //         fail -> prompt : -    f
    //         fail -> fake   :      p
    //  3) then add the various p, (1-p), f, (1-f) depending on what you want to predict
    float pt[2] = { l1pt, l2pt };
    float eta[2] = { std::abs(l1eta), std::abs(l2eta) };
    int id[2]  = { std::abs(l1pdgId), std::abs(l2pdgId) };
    bool pass[2] = { l1pass, l2pass };
    float p[2], f[2];
    for (int i = 0; i < 2; ++i) {
        TH2 *hist = (id[i] == 11 ? FRi_el[iFR] : FRi_mu[iFR]);
        int ptbin  = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(pt[i])));
        int etabin = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(eta[i])));
        double fr = hist->GetBinContent(ptbin,etabin);
        if (fr <= 0)  { std::cerr << "WARNING, FR is " << fr << " for " << hist->GetName() << ", pt " << pt[i] << " eta " << eta[i] << " id " << id[i] << std::endl; if (fr<0) std::abort(); }
        f[i] = fr;
        hist = (id[i] == 11 ? FRi_el[iPR] : FRi_mu[iPR]);
        ptbin  = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(pt[i])));
        etabin = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(eta[i])));
        fr = hist->GetBinContent(ptbin,etabin);
        if (fr <= 0)  { std::cerr << "WARNING, PR is " << fr << " for " << hist->GetName() << ", pt " << pt[i] << " eta " << eta[i] << " id " << id[i] << std::endl; if (fr<0) std::abort(); }
        p[i] = fr;
    }
    int hypots[4] = { 0, 1, 10, 11 };
    double weight = 0;
    for (int h : hypots) {
        if (!(selhyp == h || (selhyp == -1 && h != 11))) continue;
        double myw = 1.0;
        for (int i = 0; i < 2; ++i) {
            int target = (i == 1 ? h % 10 : h / 10); // 1 if prompt, 0 if fake
            // (1)
            myw *= 1.0/(p[i]-f[i]);
            // (2)
            if (pass[i]) myw *= (target ? (1-f[i]) : -(1-p[i]) );
            else         myw *= (target ?   -f[i]  :   p[i]    );
            // (3)
            int shouldpass = (i == 1 ? selfs % 10 : selfs / 10); // 1 if I'm predicting a passing, 0 if I'm predicting a failing
            if (shouldpass) myw *= (target ?    p[i]    :     f[i]   );
            else            myw *= (target ? (1 - p[i]) : (1 - f[i]) );
        }
        weight += myw;
    }
    return weight;
}


float fakeRatePromptRateWeight_2l_23(float l1pt, float l1eta, int l1pdgId, float l1pass,
                            float l2pt, float l2eta, int l2pdgId, float l2pass)
{
    return fakeRatePromptRateWeight_2l_ij(l1pt, l1eta, l1pdgId, l1pass,
                            l2pt, l2eta, l2pdgId, l2pass, 2, 3);
}
