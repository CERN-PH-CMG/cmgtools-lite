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
TH2 * FRi_mu[30], *FRi_el[30], *FRi_tau[6];
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
  TH2 * FR_temp = 0;
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
    return histo != 0;
}

float fakeRateWeight_2lssMVA(float l1pt, float l1eta, int l1pdgId, float l1mva,
                         float l2pt, float l2eta, int l2pdgId, float l2mva, float WP) 
{
    int nfail = (l1mva < WP)+(l2mva < WP);
    switch (nfail) {
        case 1: {
            double fpt,feta; int fid;
            if (l1mva < l2mva) { fpt = l1pt; feta = std::abs(l1eta); fid = abs(l1pdgId); }
            else               { fpt = l2pt; feta = std::abs(l2eta); fid = abs(l2pdgId); }
            TH2 *hist = (fid == 11 ? FR_el : FR_mu);
            int ptbin  = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(fpt)));
            int etabin = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(feta)));
            double fr = hist->GetBinContent(ptbin,etabin);
            return fr/(1-fr);
        }
        case 2: {
            TH2 *hist1 = (abs(l1pdgId) == 11 ? FR_el : FR_mu);
            int ptbin1  = std::max(1, std::min(hist1->GetNbinsX(), hist1->GetXaxis()->FindBin(l1pt)));
            int etabin1 = std::max(1, std::min(hist1->GetNbinsY(), hist1->GetYaxis()->FindBin(std::abs(l1eta))));
            double fr1 = hist1->GetBinContent(ptbin1,etabin1);
            TH2 *hist2 = (abs(l2pdgId) == 11 ? FR_el : FR_mu);
            int ptbin2  = std::max(1, std::min(hist2->GetNbinsX(), hist2->GetXaxis()->FindBin(l2pt)));
            int etabin2 = std::max(1, std::min(hist2->GetNbinsY(), hist2->GetYaxis()->FindBin(std::abs(l2eta))));
            double fr2 = hist2->GetBinContent(ptbin2,etabin2);
            return -fr1*fr2/((1-fr1)*(1-fr2));
        }
        default: return 0;
    }
}



float fakeRateWeight_2lssCB_i(float l1pt, float l1eta, int l1pdgId, float l1relIso,
                            float l2pt, float l2eta, int l2pdgId, float l2relIso, float WP, int iFR) 
{
    int nfail = (l1relIso > WP)+(l2relIso > WP);
    switch (nfail) {
        case 1: {
            double fpt,feta; int fid;
            if (l1relIso > l2relIso) { fpt = l1pt; feta = std::abs(l1eta); fid = abs(l1pdgId); }
            else                     { fpt = l2pt; feta = std::abs(l2eta); fid = abs(l2pdgId); }
            TH2 *hist = (fid == 11 ? FRi_el[iFR] : FRi_mu[iFR]);
            if (hist == 0) { std::cerr << "ERROR, missing FR for pdgId " << fid << ", iFR " << iFR << std::endl; std::abort(); }
            int ptbin  = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(fpt)));
            int etabin = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(feta)));
            double fr = hist->GetBinContent(ptbin,etabin);
            if (fr < 0)  { std::cerr << "WARNING, FR is " << fr << " for " << hist->GetName() << ", pt " << fpt << " eta " << feta << std::endl; if (fr<0) std::abort(); }
            return fr/(1-fr);
        }
        case 2: {
            TH2 *hist1 = (abs(l1pdgId) == 11 ? FRi_el[iFR] : FRi_mu[iFR]);
            if (hist1 == 0) { std::cerr << "ERROR, missing FR for pdgId " << l1pdgId << ", iFR " << iFR << std::endl; std::abort(); }
            int ptbin1  = std::max(1, std::min(hist1->GetNbinsX(), hist1->GetXaxis()->FindBin(l1pt)));
            int etabin1 = std::max(1, std::min(hist1->GetNbinsY(), hist1->GetYaxis()->FindBin(std::abs(l1eta))));
            double fr1 = hist1->GetBinContent(ptbin1,etabin1);
            if (fr1 < 0)  { std::cerr << "WARNING, FR is " << fr1 << " for " << hist1->GetName() << ", pt " << l1pt << " eta " << l1eta << std::endl; if (fr1<0) std::abort(); }
            TH2 *hist2 = (abs(l2pdgId) == 11 ? FRi_el[iFR] : FRi_mu[iFR]);
            if (hist2 == 0) { std::cerr << "ERROR, missing FR for pdgId " << l2pdgId << ", iFR " << iFR << std::endl; std::abort(); }
            int ptbin2  = std::max(1, std::min(hist2->GetNbinsX(), hist2->GetXaxis()->FindBin(l2pt)));
            int etabin2 = std::max(1, std::min(hist2->GetNbinsY(), hist2->GetYaxis()->FindBin(std::abs(l2eta))));
            double fr2 = hist2->GetBinContent(ptbin2,etabin2);
            if (fr2 < 0)  { std::cerr << "WARNING, FR is " << fr2 << " for " << hist2->GetName() << ", pt " << l2pt << " eta " << l2eta << std::endl; if (fr2<0) std::abort(); }
            return -fr1*fr2/((1-fr1)*(1-fr2));
        }
        default: return 0;
    }
}

float fakeRateWeight_2lssCB(float l1pt, float l1eta, int l1pdgId, float l1relIso,
                            float l2pt, float l2eta, int l2pdgId, float l2relIso, float WP) 
{
    return fakeRateWeight_2lssCB_i(l1pt, l1eta, l1pdgId, l1relIso,
                            l2pt, l2eta, l2pdgId, l2relIso, WP, 0);
}

float fakeRateWeight_2lss(float l1pt, float l1eta, int l1pdgId, float l1pass,
                            float l2pt, float l2eta, int l2pdgId, float l2pass) 
{
    return fakeRateWeight_2lssCB_i(l1pt, l1eta, l1pdgId, -l1pass,
                            l2pt, l2eta, l2pdgId, -l2pass, -0.5, 0);
}
float fakeRateWeight_2lss_2(float l1pt, float l1eta, int l1pdgId, float l1pass,
                            float l2pt, float l2eta, int l2pdgId, float l2pass) 
{
    return fakeRateWeight_2lssCB_i(l1pt, l1eta, l1pdgId, -l1pass,
                            l2pt, l2eta, l2pdgId, -l2pass, -0.5, 2);
}
float fakeRateWeight_2lss_i(float l1pt, float l1eta, int l1pdgId, float l1pass,
                            float l2pt, float l2eta, int l2pdgId, float l2pass, int iFR) 
{
    return fakeRateWeight_2lssCB_i(l1pt, l1eta, l1pdgId, -l1pass,
                            l2pt, l2eta, l2pdgId, -l2pass, -0.5, iFR);
}

float fakeRateWeight_2lss_up(float l1pt, float l1eta, int l1pdgId, float l1pass,
                            float l2pt, float l2eta, int l2pdgId, float l2pass) 
{
    return fakeRateWeight_2lssCB_i(l1pt, l1eta, l1pdgId, -l1pass,
                            l2pt, l2eta, l2pdgId, -l2pass, -0.5, 3);
}

float fakeRateWeight_2lss_down(float l1pt, float l1eta, int l1pdgId, float l1pass,
			       float l2pt, float l2eta, int l2pdgId, float l2pass) 
{
    return fakeRateWeight_2lssCB_i(l1pt, l1eta, l1pdgId, -l1pass,
                            l2pt, l2eta, l2pdgId, -l2pass, -0.5, 4);
}


float fakeRateWeight_2lssSyst(float l1pt, float l1eta, int l1pdgId, float l1mva,
                         float l2pt, float l2eta, int l2pdgId, float l2mva, float WP, 
                         float mu_barrel_lowpt, float mu_barrel_highpt, float mu_endcap_lowpt, float mu_endcap_highpt,
                         float el_cb_lowpt, float el_cb_highpt, float el_fb_lowpt, float el_fb_highpt, float el_endcap_lowpt, float el_endcap_highpt)
{
    /// 2 pass: weight  0
    /// 1 fail: weight +f/(1-f)
    /// 2 fail: weight -f*f/(1-f)(1-f)
    //  so, just multiply up factors of -f/(1-f) for each failure
    float mvas[]={l1mva, l2mva};
    float pts[]={l1pt, l2pt};
    float etas[]={fabs(l1eta), fabs(l2eta)};
    int pdgids[]={l1pdgId, l2pdgId};
    float ret = -1.0f;
    for (unsigned int i = 0; i < 2 ; ++i) {
        if (mvas[i] < WP) {
	    TH2 *hist = (abs(pdgids[i]) == 11 ? FR_el : FR_mu);
            int ptbin  = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(pts[i])));
            int etabin = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(etas[i])));
            double fr = hist->GetBinContent(ptbin,etabin);
            if (abs(pdgids[i]) == 11) fr *= ( std::abs(etas[i]) < 0.8 ? (pts[i] < 30 ? el_cb_lowpt : el_cb_highpt) :
                                             (std::abs(etas[i]) < 1.5 ? (pts[i] < 30 ? el_fb_lowpt : el_fb_highpt) :
                                                                        (pts[i] < 30 ? el_endcap_lowpt : el_endcap_highpt) ));
            else /*==13*/             fr *= (std::abs(etas[i]) < 1.5 ?  (pts[i] < 30 ? mu_barrel_lowpt : mu_barrel_highpt) :
                                                                        (pts[i] < 30 ? mu_endcap_lowpt : mu_endcap_highpt) );
            ret *= -fr/(1.0f-fr);
        }
    }
    if (ret == -1.0f) ret = 0.0f;
    return ret;

}
float fakeRateWeight_2lssBCat(float l1pt, float l1eta, int l1pdgId, float l1mva,
                         float l2pt, float l2eta, int l2pdgId, float l2mva, float WP, 
                         int nBJetMedium25, float scaleMuBL, float scaleMuBT, float scaleElBL, float scaleElBT)
{
    /// 2 pass: weight  0
    /// 1 fail: weight +f/(1-f)
    /// 2 fail: weight -f*f/(1-f)(1-f)
    //  so, just multiply up factors of -f/(1-f) for each failure
    float mvas[]={l1mva, l2mva};
    float pts[]={l1pt, l2pt};
    float etas[]={fabs(l1eta), fabs(l2eta)};
    int pdgids[]={l1pdgId, l2pdgId};
    float ret = -1.0f;
    for (unsigned int i = 0; i < 2 ; ++i) {
        if (mvas[i] < WP) {
	    TH2 *hist = (abs(pdgids[i]) == 11 ? (nBJetMedium25 > 1 ? FR2_el : FR_el):
                                                (nBJetMedium25 > 1 ? FR2_mu : FR_mu));
            int ptbin  = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(pts[i])));
            int etabin = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(etas[i])));
            double fr = hist->GetBinContent(ptbin,etabin);
            fr *= (nBJetMedium25 > 1 ? (abs(pdgids[i]) == 11 ? scaleElBT : scaleMuBT) : 
                                       (abs(pdgids[i]) == 11 ? scaleElBL : scaleMuBL) );
            ret *= -fr/(1.0f-fr);
        }
    }
    if (ret == -1.0f) ret = 0.0f;
    return ret;
}

float fakeRateWeight_2lssBCatSB(float l1pt, float l1eta, int l1pdgId, float l1mva,
                         float l2pt, float l2eta, int l2pdgId, float l2mva, float WP, float SBlow, float SBhigh,
                         int nBJetMedium25)
{
    float mvas[]={l1mva, l2mva};
    float pts[]={l1pt, l2pt};
    float etas[]={fabs(l1eta), fabs(l2eta)};
    int pdgids[]={l1pdgId, l2pdgId};
    float ret = -1.0f;
    for (unsigned int i = 0; i < 2 ; ++i) {
        if (mvas[i] > WP) {
            continue;
        } else if (SBlow < mvas[i] && mvas[i] < SBhigh) {
	    TH2 *hist = (abs(pdgids[i]) == 11 ? (nBJetMedium25 > 1 ? FR2_el : FR_el):
                                                (nBJetMedium25 > 1 ? FR2_mu : FR_mu));
            int ptbin  = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(pts[i])));
            int etabin = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(etas[i])));
            double fr = hist->GetBinContent(ptbin,etabin);
            ret *= -fr/max(1.0f-fr,0.5);
        } else {
            ret = 0.0f; break;
        }
    }
    if (ret == -1.0f) ret = 0.0f;
    return ret;
}
float fakeRateWeight_2lssBCatX(float l1pt, float l1eta, int l1pdgId, float l1mva,
                         float l2pt, float l2eta, int l2pdgId, float l2mva, float WPlow, float WPhigh,
                         int nBJetMedium25)
{
    float mvas[]={l1mva, l2mva};
    float pts[]={l1pt, l2pt};
    float etas[]={fabs(l1eta), fabs(l2eta)};
    int pdgids[]={l1pdgId, l2pdgId};
    float ret = -1.0f;
    int npass = 0;
    for (unsigned int i = 0; i < 2 ; ++i) {
        if (mvas[i] > WPhigh) {
            npass++; continue;
        } else if (mvas[i] > WPlow) {
            continue;
        } else  {
	    TH2 *hist = (abs(pdgids[i]) == 11 ? (nBJetMedium25 > 1 ? FR2_el : FR_el):
                                                (nBJetMedium25 > 1 ? FR2_mu : FR_mu));
            int ptbin  = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(pts[i])));
            int etabin = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(etas[i])));
            double fr = hist->GetBinContent(ptbin,etabin);
            ret *= -fr/std::max(1.0f-fr,0.5);
        }
    }
    if (ret == -1.0f) ret = 0.0f;
    return ret;
}




float fakeRateWeight_2lssMuIDCat(float l1pt, float l1eta, int l1pdgId, float l1mva, float l1tightId,
                         float l2pt, float l2eta, int l2pdgId, float l2mva, float l2tightId, float WP)
{
    /// 2 pass: weight  0
    /// 1 fail: weight +f/(1-f)
    /// 2 fail: weight -f*f/(1-f)(1-f)
    //  so, just multiply up factors of -f/(1-f) for each failure
    float mvas[]={l1mva, l2mva};
    float pts[]={l1pt, l2pt};
    float etas[]={fabs(l1eta), fabs(l2eta)};
    float tightIds[]={l1tightId, l2tightId};
    int pdgids[]={l1pdgId, l2pdgId};
    float ret = -1.0f;
    for (unsigned int i = 0; i < 2 ; ++i) {
        if (mvas[i] < WP) {
	    TH2 *hist = (abs(pdgids[i]) == 11 ? FR_el: (tightIds[i] > 0 ? FR_mu : FR2_mu));
            int ptbin  = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(pts[i])));
            int etabin = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(etas[i])));
            double fr = hist->GetBinContent(ptbin,etabin);
            ret *= -fr/(1.0f-fr);
        }
    }
    if (ret == -1.0f) ret = 0.0f;
    return ret;
}

float fakeRateWeight_2lssCB_ptRel2D(float l1pt, float l1eta, int l1pdgId, float l1relIso, float l1ptRel,
                                    float l2pt, float l2eta, int l2pdgId, float l2relIso, float l2ptRel, float WPIsoL, float WPIsoT, float WPPtRelL, float WPPtRelT) 
{
    float relIsos[]={l1relIso, l2relIso};
    float ptRels[]={l1ptRel, l2ptRel};
    float pts[]={l1pt, l2pt};
    float etas[]={fabs(l1eta), fabs(l2eta)};
    int pdgids[]={l1pdgId, l2pdgId};
    float ret = 0.f;
    int npass = 0;
    for (unsigned int i = 0; i < 2 ; ++i) {
        if (relIsos[i] < WPIsoT || ptRels[i] > WPPtRelT) { 
            npass++; continue; 
        }
        if (relIsos[i] < WPIsoL && ptRels[i] <= WPPtRelL) {
            // iso sideband
	    TH2 *hist = abs(pdgids[i]) == 11 ? FR2_el : FR2_mu;
            int ptbin  = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(pts[i])));
            int etabin = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(etas[i])));
            double fr = hist->GetBinContent(ptbin,etabin);
            ret += fr/(1.0f-fr);
        }
        if (ptRels[i] > WPPtRelL) {
            // ptrel sideband
	    TH2 *hist = abs(pdgids[i]) == 11 ? FR3_el : FR3_mu;
            int ptbin  = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(pts[i])));
            int etabin = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(etas[i])));
            double fr = hist->GetBinContent(ptbin,etabin);
            ret += fr/(1.0f-fr);
        }
    }
    if (npass != 1) ret = 0.0f;
    return ret;
}



float fakeRateWeight_3lMuIDCat(float l1pt, float l1eta, int l1pdgId, float l1mva, float l1tightId,
                        float l2pt, float l2eta, int l2pdgId, float l2mva, float l2tightId,
                        float l3pt, float l3eta, int l3pdgId, float l3mva, float l3tightId, float WP)
{
    float mvas[]={l1mva, l2mva, l3mva};
    float pts[]={l1pt, l2pt, l3pt};
    float etas[]={fabs(l1eta), fabs(l2eta), fabs(l3eta)};
    int pdgids[]={l1pdgId, l2pdgId, l3pdgId};
    float tightIds[]={l1tightId, l2tightId,l3tightId};
    float ret = -1.0f;
    for (unsigned int i = 0; i < 3 ; ++i) {
        if (mvas[i] < WP) {
	    TH2 *hist = (abs(pdgids[i]) == 11 ? FR_el: (tightIds[i] > 0 ? FR_mu : FR2_mu));
            int ptbin  = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(pts[i])));
            int etabin = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(etas[i])));
            double fr = hist->GetBinContent(ptbin,etabin);
            ret *= -fr/(1.0f-fr);
        }
    }
    if (ret == -1.0f) ret = 0.0f;
    return ret;
}

bool passND_LooseDen(float l1pt, float l1eta, int l1pdgId, float relIso, float dxy, float dz, float tightId) 
{
    if (fabs(l1pdgId) == 13) {
        return l1pt >= 10;
    } else {
        return l1pt >= 10 && (fabs(l1eta)<1.4442 || fabs(l1eta)>1.5660);
    }
}

bool passND_Loose(float l1pt, float l1eta, int l1pdgId, float relIso, float dxy, float dz, float tightId) 
{
    if (fabs(l1pdgId) == 13) {
        return l1pt >= 10 && 
               relIso < 0.2;
    } else {
        return l1pt >= 10 && (fabs(l1eta)<1.4442 || fabs(l1eta)>1.5660) &&
               tightId > 0.5 && relIso < 0.2 && fabs(dxy) < 0.04;
    }
}

bool passND_TightDen(float l1pt, float l1eta, int l1pdgId, float relIso, float dxy, float dz, float tightId) 
{
    if (fabs(l1pdgId) == 13) {
        return l1pt >= 20 && fabs(l1eta) <= 2.1;
    } else {
        return l1pt >= 20 && (fabs(l1eta)<1.4442 || fabs(l1eta)>1.5660);
    }
}

bool passND_Tight(float l1pt, float l1eta, int l1pdgId, float relIso, float dxy, float dz, float tightId) 
{
    if (fabs(l1pdgId) == 13) {
        return l1pt >= 20 && fabs(l1eta) <= 2.1 && 
               tightId != 0 && relIso < 0.12 && fabs(dxy) < 0.2 && fabs(dz) < 0.5;
    } else {
        return l1pt >= 20 && (fabs(l1eta)<1.4442 || fabs(l1eta)>1.5660) &&
               tightId > 0.5 && relIso < 0.1 && fabs(dxy) < 0.02;
    }
}

bool passEgammaTightMVA(float pt, float eta, float tightid) {
    if (fabs(eta) > 0.8) {
        return (pt > 20 ? (tightid > 0.94) : (tightid > 0.00));
    } else if (fabs(eta) < 1.479) {
        return (pt > 20 ? (tightid > 0.85) : (tightid > 0.10));
    } else {
        return (pt > 20 ? (tightid > 0.92) : (tightid > 0.062));
    }
}

float fakeRateWeight_2lss_ND(float l1pt, float l1eta, int l1pdgId, float l1relIso, float l1dxy, float l1dz, float l1tightId,
                          float l2pt, float l2eta, int l2pdgId, float l2relIso, float l2dxy, float l2dz, float l2tightId, int WP) 
{
    switch (WP) {
        case 11: {// loose-loose
            bool l1L = passND_Loose(l1pt, l1eta, l1pdgId, l1relIso, l1dxy, l1dz, l1tightId);
            bool l2L = passND_Loose(l2pt, l2eta, l2pdgId, l2relIso, l2dxy, l2dz, l2tightId);
            TH2 *hist1 = (abs(l1pdgId) == 11 ? FR_el : FR_mu);
            int ptbin1  = std::max(1, std::min(hist1->GetNbinsX(), hist1->GetXaxis()->FindBin(l1pt)));
            int etabin1 = std::max(1, std::min(hist1->GetNbinsY(), hist1->GetYaxis()->FindBin(std::abs(l1eta))));
            double fr1 = hist1->GetBinContent(ptbin1,etabin1);
            TH2 *hist2 = (abs(l2pdgId) == 11 ? FR_el : FR_mu);
            int ptbin2  = std::max(1, std::min(hist2->GetNbinsX(), hist2->GetXaxis()->FindBin(l2pt)));
            int etabin2 = std::max(1, std::min(hist2->GetNbinsY(), hist2->GetYaxis()->FindBin(std::abs(l2eta))));
            double fr2 = hist2->GetBinContent(ptbin2,etabin2);
            if      ( l1L &&  l2L) return 0;
            else if ( l1L && !l2L) return fr2/(1-fr2);
            else if (!l1L &&  l2L) return fr1/(1-fr1);
            else if (!l1L && !l2L) return -fr1*fr2/((1-fr1)*(1-fr2));
        }; 
        case 22: {// tight-tight 
            bool l1T = passND_Tight(l1pt, l1eta, l1pdgId, l1relIso, l1dxy, l1dz, l1tightId);
            bool l2T = passND_Tight(l2pt, l2eta, l2pdgId, l2relIso, l2dxy, l2dz, l2tightId);
            TH2 *hist1 = (abs(l1pdgId) == 11 ? FR2_el : FR2_mu);
            int ptbin1  = std::max(1, std::min(hist1->GetNbinsX(), hist1->GetXaxis()->FindBin(l1pt)));
            int etabin1 = std::max(1, std::min(hist1->GetNbinsY(), hist1->GetYaxis()->FindBin(std::abs(l1eta))));
            double fr1 = hist1->GetBinContent(ptbin1,etabin1);
            TH2 *hist2 = (abs(l2pdgId) == 11 ? FR2_el : FR2_mu);
            int ptbin2  = std::max(1, std::min(hist2->GetNbinsX(), hist2->GetXaxis()->FindBin(l2pt)));
            int etabin2 = std::max(1, std::min(hist2->GetNbinsY(), hist2->GetYaxis()->FindBin(std::abs(l2eta))));
            double fr2 = hist2->GetBinContent(ptbin2,etabin2);
            if      ( l1T &&  l2T) return 0;
            else if ( l1T && !l2T) return fr2/(1-fr2);
            else if (!l1T &&  l2T) return fr1/(1-fr1);
            else if (!l1T && !l2T) return -fr1*fr2/((1-fr1)*(1-fr2));
        }; 
        default: {
            static int _once = 0;
            if (_once++ == 0) { std::cerr << "ERROR, unknown WP " << WP << std::endl; }
        }

    }
    return 0;
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

float chargeFlipBin_2lss(float l1pt, float l1eta) {
    if (std::abs(l1eta) < 1.479) {
        return (l1pt < 20 ? 0 : (l1pt < 50 ? 1 : 2));
    } else {
        return (l1pt < 20 ? 3 : (l1pt < 50 ? 4 : 5));
    }
}


float fakeRateWeight_3lSyst(float l1pt, float l1eta, int l1pdgId, float l1mva,
                        float l2pt, float l2eta, int l2pdgId, float l2mva,
                        float l3pt, float l3eta, int l3pdgId, float l3mva,
                        float WP,
                        float mu_barrel_lowpt, float mu_barrel_highpt, float mu_endcap_lowpt, float mu_endcap_highpt,
                        float el_cb_lowpt, float el_cb_highpt, float el_fb_lowpt, float el_fb_highpt, float el_endcap_lowpt, float el_endcap_highpt)
{
    /// 3 pass: weight  0
    /// 1 fail: weight +f/(1-f)
    /// 2 fail: weight -f*f/(1-f)(1-f)
    //  3 fail: weight +f*f*f/((1-f)(1-f)(1-f)
    //  so, just multiply up factors of -f/(1-f) for each failure
    float mvas[]={l1mva, l2mva, l3mva};
    float pts[]={l1pt, l2pt, l3pt};
    float etas[]={fabs(l1eta), fabs(l2eta), fabs(l3eta)};
    int pdgids[]={l1pdgId, l2pdgId, l3pdgId};
    float ret = -1.0f;
    for (unsigned int i = 0; i < 3 ; ++i) {
        if (mvas[i] < WP) {
	    TH2 *hist = (abs(pdgids[i]) == 11 ? FR_el : FR_mu);
            int ptbin  = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(pts[i])));
            int etabin = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(etas[i])));
            double fr = hist->GetBinContent(ptbin,etabin);
            if (abs(pdgids[i]) == 11) fr *= ( std::abs(etas[i]) < 0.8 ? (pts[i] < 20 ? el_cb_lowpt : el_cb_highpt) :
                                             (std::abs(etas[i]) < 1.5 ? (pts[i] < 20 ? el_fb_lowpt : el_fb_highpt) :
                                                                        (pts[i] < 20 ? el_endcap_lowpt : el_endcap_highpt) ));
            else /*==13*/             fr *= (std::abs(etas[i]) < 1.5 ?  (pts[i] < 20 ? mu_barrel_lowpt : mu_barrel_highpt) :
                                                                        (pts[i] < 20 ? mu_endcap_lowpt : mu_endcap_highpt) );
            ret *= -fr/(1.0f-fr);
        }
    }
    if (ret == -1.0f) ret = 0.0f;
    return ret;
}

float fakeRateWeight_3lMVA(float l1pt, float l1eta, int l1pdgId, float l1mva,
                        float l2pt, float l2eta, int l2pdgId, float l2mva,
                        float l3pt, float l3eta, int l3pdgId, float l3mva,
                        float WP)
{
    /// 3 pass: weight  0
    /// 1 fail: weight +f/(1-f)
    /// 2 fail: weight -f*f/(1-f)(1-f)
    //  3 fail: weight +f*f*f/((1-f)(1-f)(1-f)
    //  so, just multiply up factors of -f/(1-f) for each failure
    float mvas[]={l1mva, l2mva, l3mva};
    float pts[]={l1pt, l2pt, l3pt};
    float etas[]={fabs(l1eta), fabs(l2eta), fabs(l3eta)};
    int pdgids[]={l1pdgId, l2pdgId, l3pdgId};
    float ret = -1.0f;
    for (unsigned int i = 0; i < 3 ; ++i) {
        if (mvas[i] < WP) {
	    TH2 *hist = (abs(pdgids[i]) == 11 ? FR_el : FR_mu);
            int ptbin  = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(pts[i])));
            int etabin = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(etas[i])));
            double fr = hist->GetBinContent(ptbin,etabin);
            ret *= -fr/(1.0f-fr);
        }
    }
    if (ret == -1.0f) ret = 0.0f;
    return ret;
}

float fakeRateWeight_3lBCat(float l1pt, float l1eta, int l1pdgId, float l1mva,
                        float l2pt, float l2eta, int l2pdgId, float l2mva,
                        float l3pt, float l3eta, int l3pdgId, float l3mva,
                        float WP, int nBJetMedium25, float scaleMuBL, float scaleMuBT, float scaleElBL, float scaleElBT)
{
    /// 3 pass: weight  0
    /// 1 fail: weight +f/(1-f)
    /// 2 fail: weight -f*f/(1-f)(1-f)
    //  3 fail: weight +f*f*f/((1-f)(1-f)(1-f)
    //  so, just multiply up factors of -f/(1-f) for each failure
    float mvas[]={l1mva, l2mva, l3mva};
    float pts[]={l1pt, l2pt, l3pt};
    float etas[]={fabs(l1eta), fabs(l2eta), fabs(l3eta)};
    int pdgids[]={l1pdgId, l2pdgId, l3pdgId};
    float ret = -1.0f;
    for (unsigned int i = 0; i < 3 ; ++i) {
        if (mvas[i] < WP) {
	    TH2 *hist = (abs(pdgids[i]) == 11 ? (nBJetMedium25 > 1 ? FR2_el : FR_el):
                                                (nBJetMedium25 > 1 ? FR2_mu : FR_mu));
            int ptbin  = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(pts[i])));
            int etabin = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(etas[i])));
            double fr = hist->GetBinContent(ptbin,etabin);
            fr *= (nBJetMedium25 > 1 ? (abs(pdgids[i]) == 11 ? scaleElBT : scaleMuBT) : 
                                       (abs(pdgids[i]) == 11 ? scaleElBL : scaleMuBL) );
            ret *= -fr/(1.0f-fr);
        }
    }
    if (ret == -1.0f) ret = 0.0f;
    return ret;
}

float fakeRateWeight_3lCB(float l1pt, float l1eta, int l1pdgId, float l1relIso,
                        float l2pt, float l2eta, int l2pdgId, float l2relIso,
                        float l3pt, float l3eta, int l3pdgId, float l3relIso,
                        float WP)
{
    float relIsos[]={l1relIso, l2relIso, l3relIso};
    float pts[]={l1pt, l2pt, l3pt};
    float etas[]={fabs(l1eta), fabs(l2eta), fabs(l3eta)};
    int pdgids[]={l1pdgId, l2pdgId, l3pdgId};
    float ret = -1.0f;
    for (unsigned int i = 0; i < 3 ; ++i) {
        if (relIsos[i] > WP) {
	    TH2 *hist = (abs(pdgids[i]) == 11 ? FR_el : FR_mu);
            int ptbin  = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(pts[i])));
            int etabin = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(etas[i])));
            double fr = hist->GetBinContent(ptbin,etabin);
            ret *= -fr/(1.0f-fr);
        }
    }
    if (ret == -1.0f) ret = 0.0f;
    return ret;
}

float fetchFR_i(float l1pt, float l1eta, int l1pdgId, int iFR) 
{
    TH2 *hist1 = (abs(l1pdgId) == 11 ? FRi_el[iFR] : FRi_mu[iFR]);
    if (hist1 == 0) { std::cerr << "ERROR, missing FR for pdgId " << l1pdgId << ", iFR " << iFR << std::endl; std::abort(); }
    int ptbin1  = std::max(1, std::min(hist1->GetNbinsX(), hist1->GetXaxis()->FindBin(l1pt)));
    int etabin1 = std::max(1, std::min(hist1->GetNbinsY(), hist1->GetYaxis()->FindBin(std::abs(l1eta))));
    double fr1 = hist1->GetBinContent(ptbin1,etabin1);
    if (fr1 < 0)  { std::cerr << "WARNING, FR is " << fr1 << " for " << hist1->GetName() << ", pt " << l1pt << " eta " << l1eta << std::endl; if (fr1<0) std::abort(); }
    return fr1;
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

float fakeRate_flavour_2l_19_lead(float l1pt, float l1eta, int l1pdgId, 
                                 float l2pt, float l2eta, int l2pdgId, int histo) 
{
    if (l1pdgId == -l2pdgId) return 0.;
    switch (histo) {
        case 0: return 1.;
        case 1:
        case 2:
             TH2 *num = (histo <= 1 ? (abs(l1pdgId) == 11 ? FR_el : FR_mu) : (abs(l1pdgId) == 11 ? FR2_el : FR2_mu));
             TH2 *den = (histo <= 1 ? (abs(l1pdgId) == 11 ? FR_mu : FR_el) : (abs(l1pdgId) == 11 ? FR2_mu : FR2_el));
             int ptnum  = std::max(1, std::min(num->GetNbinsX(), num->GetXaxis()->FindBin(l1pt)));
             int etanum = std::max(1, std::min(num->GetNbinsY(), num->GetYaxis()->FindBin(fabs(l1eta))));
             int ptden  = std::max(1, std::min(den->GetNbinsX(), den->GetXaxis()->FindBin(l1pt)));
             int etaden = std::max(1, std::min(den->GetNbinsY(), den->GetYaxis()->FindBin(fabs(l1eta))));
             if (den->GetBinContent(ptden,etaden) == 0) return 1.0;
             return num->GetBinContent(ptnum,etanum)/den->GetBinContent(ptden,etaden);
    }
    return 0.;
}


float fakeRateBin_Muons(float pt, float eta) { // 0 .. 49
    if (pt >= 50) pt = 49.9;
    eta = fabs(eta); if (eta >= 2.5) eta = 2.499;
    int ieta = floor(eta/0.5); // 0 .. 4;
    int ipt  = floor(pt/5.0); // 0 .. 9;
    if (ipt == 8) ipt = 7; // now merge the 40-45 into the 35-40;
    return ipt*5 + ieta + 0.5; // make sure we end in the bin center
}
float fakeRateBin_Muons_eta(float bin) {
    int ibin = floor(bin);
    return (ibin % 5)*0.5 + 0.25;
}
float fakeRateBin_Muons_pt(float bin) {
    int ibin = floor(bin);
    return (ibin/5)*5.0 + 2.5;
}


float fakeRateReader_2lss_FO(float l1eta, float l1pt, float l2eta, float l2pt, int l1pdgId, int l2pdgId, int pass1, int pass2, int fo123, int isinsitu)
{
  assert (fo123==1 || fo123==2 || fo123==3 || fo123==4);
  assert (isinsitu==0 || isinsitu==1);
  int ind = 2*(fo123-1)+isinsitu;
  int nfail = 2-pass1-pass2;
    switch (nfail) {
        case 1: {
            double fpt,feta; int fid;
            if (pass2)   { fpt = l1pt; feta = std::abs(l1eta); fid = abs(l1pdgId); }
            else         { fpt = l2pt; feta = std::abs(l2eta); fid = abs(l2pdgId); }
            TH2 *hist = (fid == 11 ? FRi_FO_el[ind] : FRi_FO_mu[ind]);
	    if (!hist){
	      std::cout << "Error: FR histo not filled " << fid << " " << ind << std::endl;
	      assert(false);
	    }
	    int ptbin  = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(fpt)));
	    int etabin = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(feta)));
	    double fr = hist->GetBinContent(ptbin,etabin);
            return fr/(1-fr);
        }
      case 2: {
            TH2 *hist1 = (abs(l1pdgId) == 11 ? FRi_FO_el[ind] : FRi_FO_mu[ind]);
	    int ptbin1  = std::max(1, std::min(hist1->GetNbinsX(), hist1->GetXaxis()->FindBin(l1pt)));
	    int etabin1 = std::max(1, std::min(hist1->GetNbinsY(), hist1->GetYaxis()->FindBin(std::abs(l1eta))));
	    double fr1 = hist1->GetBinContent(ptbin1,etabin1);
           TH2 *hist2 = (abs(l2pdgId) == 11 ? FRi_FO_el[ind] : FRi_FO_mu[ind]);
	   int ptbin2  = std::max(1, std::min(hist2->GetNbinsX(), hist2->GetXaxis()->FindBin(l2pt)));
	   int etabin2 = std::max(1, std::min(hist2->GetNbinsY(), hist2->GetYaxis()->FindBin(std::abs(l2eta))));
	   double fr2 = hist2->GetBinContent(ptbin2,etabin2);
            return -fr1*fr2/((1-fr1)*(1-fr2));
      }
        default: return 0;
    }
}

float fakeRateReader_2lss_fHT_FO(float l1eta, float l1pt, float l2eta, float l2pt, int l1pdgId, int l2pdgId, int pass1, int pass2, int isiso)
{
  int ind = isiso ? 0 : 1;
  int nfail = 2-pass1-pass2;
    switch (nfail) {
        case 1: {
            double fpt,feta; int fid;
            if (pass2)   { fpt = l1pt; feta = std::abs(l1eta); fid = abs(l1pdgId); }
            else         { fpt = l2pt; feta = std::abs(l2eta); fid = abs(l2pdgId); }
            TH2 *hist = (fid == 11 ? FRi_fHT_FO_el[ind] : FRi_fHT_FO_mu[ind]);
	    if (!hist){
	      std::cout << "Error: FR histo not filled " << fid << " " << ind << std::endl;
	      assert(false);
	    }
	    int ptbin  = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(fpt)));
	    int etabin = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(feta)));
	    double fr = hist->GetBinContent(ptbin,etabin);
	    //	    std::cout << "returning " << fr/(1-fr) << std::endl;
            return fr/(1-fr);
        }
      case 2: {
            TH2 *hist1 = (abs(l1pdgId) == 11 ? FRi_fHT_FO_el[ind] : FRi_fHT_FO_mu[ind]);
	    int ptbin1  = std::max(1, std::min(hist1->GetNbinsX(), hist1->GetXaxis()->FindBin(l1pt)));
	    int etabin1 = std::max(1, std::min(hist1->GetNbinsY(), hist1->GetYaxis()->FindBin(std::abs(l1eta))));
	    double fr1 = hist1->GetBinContent(ptbin1,etabin1);
           TH2 *hist2 = (abs(l2pdgId) == 11 ? FRi_fHT_FO_el[ind] : FRi_fHT_FO_mu[ind]);
	   int ptbin2  = std::max(1, std::min(hist2->GetNbinsX(), hist2->GetXaxis()->FindBin(l2pt)));
	   int etabin2 = std::max(1, std::min(hist2->GetNbinsY(), hist2->GetYaxis()->FindBin(std::abs(l2eta))));
	   double fr2 = hist2->GetBinContent(ptbin2,etabin2);
	   //	   std::cout << "returning " << -fr1*fr2/((1-fr1)*(1-fr2)) << std::endl;
            return -fr1*fr2/((1-fr1)*(1-fr2));
      }
        default: return 0;
    }
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
