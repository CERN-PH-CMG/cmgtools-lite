#include <TH2.h>
#include <TH2D.h>
#include <TFile.h>
#include <TF1.h>
#include <cmath>
#include <iostream>
#include <string>
#include <map>
#include <cstdlib> //as stdlib.h         
#include <cstdio>

TH2 * helicityFractions_0 = 0;
TH2 * helicityFractions_L = 0;
TH2 * helicityFractions_R = 0;

TH2 * FR_mu = 0;
TH2 * FR_el = 0;
TH2 * FRi_mu[30], *FRi_el[30];
TH2 * FR_mu_smooth = 0;
TH2 * FR_el_smooth = 0;


bool loadFRHisto(const std::string &histoName, const char *file, const char *name) {
  TH2 **histo = 0, **hptr2 = 0;
  TH2 * FR_temp = 0;
    if (histoName == "FR_mu")  { histo = & FR_mu;  hptr2 = & FRi_mu[0]; }
    else if (histoName == "FR_mu_qcdmc")  { histo = & FR_mu;  hptr2 = & FRi_mu[0]; }
    else if (histoName == "FR_el")  { histo = & FR_el;  hptr2 = & FRi_el[0]; }
    else if (histoName == "FR_el_qcdmc")  { histo = & FR_el;  hptr2 = & FRi_el[0]; }
    else if (TString(histoName).BeginsWith("FR_mu_i")) {histo = & FR_temp; hptr2 = & FRi_mu[TString(histoName).ReplaceAll("FR_mu_i","").Atoi()];}
    else if (TString(histoName).BeginsWith("FR_el_i")) {histo = & FR_temp; hptr2 = & FRi_el[TString(histoName).ReplaceAll("FR_el_i","").Atoi()];}
    else if (TString(histoName).Contains("helicityFractions_0")) { histo = & helicityFractions_0; }
    else if (TString(histoName).Contains("helicityFractions_L")) { histo = & helicityFractions_L; }
    else if (TString(histoName).Contains("helicityFractions_R")) { histo = & helicityFractions_R; }
    if (histo == 0)  {
        std::cerr << "ERROR: histogram " << histoName << " is not defined in fakeRate.cc." << std::endl;
        return 0;
    }

    TFile *f = TFile::Open(file);
    if (*histo != 0) {
      if (std::string(name) != (*histo)->GetName()) {
        //std::cerr << "WARNING: overwriting histogram " << (*histo)->GetName() << std::endl;
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

float fakeRateWeight_1l_i(float lpt, float leta, int lpdgId, bool passWP, int iFR) {
  if (!passWP) {
    double fpt = lpt; double feta = std::abs(leta); int fid = abs(lpdgId);
    TH2 *hist = (fid == 11 ? FRi_el[iFR] : FRi_mu[iFR]);
    if (hist == 0) return 0;
    int ptbin  = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(fpt)));
    int etabin = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(feta)));
    double fr = hist->GetBinContent(ptbin,etabin);
    return fr/(1-fr);
  } else return 0;
}

float fakeRateWeight_1l(float lpt, float leta, int lpdgId, bool passWP)
{
  return fakeRateWeight_1l_i(lpt, leta, lpdgId, passWP, 0);
}

float fetchFR_i(float l1pt, float l1eta, int l1pdgId, int iFR) 
{
    TH2 *hist1 = (abs(l1pdgId) == 11 ? FRi_el[iFR] : FRi_mu[iFR]);
    if (hist1 == 0) { std::cerr << "ERROR, missing FR for pdgId " << l1pdgId << ", iFR " << iFR << std::endl; }
    int ptbin1  = std::max(1, std::min(hist1->GetNbinsX(), hist1->GetXaxis()->FindBin(l1pt)));
    int etabin1 = std::max(1, std::min(hist1->GetNbinsY(), hist1->GetYaxis()->FindBin(std::abs(l1eta))));
    double fr1 = hist1->GetBinContent(ptbin1,etabin1);
    if (fr1 <= 0)  { std::cerr << "WARNING, FR is " << fr1 << " for " << hist1->GetName() << ", pt " << l1pt << " eta " << l1eta << std::endl; }
    return fr1;
}


float getSmoothedFakeRateWeight(float lpt, float leta, int lpdgId, bool passWP, bool isData = true) 
{

  // fake rate was fitted with a straight line
  //cout << "Just inside getSmoothedFakeRateWeight()" << endl;

  if (not passWP) {

    float coeff = 0.0;
    float slope = 0.0;

    if (abs(lpdgId) == 11) {
      
      if (FR_el_smooth == 0) {

	char* cmsswPath;                                                                                               
	cmsswPath = getenv ("CMSSW_BASE");                                                                             
	if (cmsswPath == NULL) {                                                                                       
	  cout << "Error in getSmoothedFakeRateWeight(): environment variable CMSSW_BASE not found. Exit" << endl;         
	  exit(EXIT_FAILURE);                                                                                          
	}                                                                                                              
	string frSmoothFileName = Form("%s/src/CMGTools/MonoXAnalysis/data/fakerate/fakeRateSmoothed_el.root",cmsswPath); 
	//cout << "This is the first time that file " << frSmoothFileName << " is opened. Now reading histogram" << endl;

	TFile* frSmoothFile = new TFile(frSmoothFileName.c_str(),"READ");
	if (!frSmoothFile || frSmoothFile->IsZombie()) {
	  cout << "Error in getSmoothedFakeRateWeight(): file " << frSmoothFileName << " not opened. Exit" << endl;
	  exit(EXIT_FAILURE);
	}

	if (isData) FR_el_smooth = new TH2D( *( (TH2D*) frSmoothFile->Get("frSmoothParameter_data")->Clone()));
	else FR_el_smooth = new TH2D( *( (TH2D*) frSmoothFile->Get("frSmoothParameter_qcd")->Clone() ));

	if ( FR_el_smooth == 0) {
	  cout << "Error in getSmoothedFakeRateWeight(): pointer FR_el_smooth is NULL. Exit" << endl;
	  exit(EXIT_FAILURE);
	} else {
	  FR_el_smooth->SetDirectory(0);
	}	
	frSmoothFile->Close();
	delete frSmoothFile;
	
      }

      // 2D histogram defined with offset and slope on y axis, eta on x axis
      // y axis defined between -0.5 and 1.5 (2 bins centered at 0 and 1)
      coeff = FR_el_smooth->GetBinContent(FR_el_smooth->FindFixBin(fabs(leta),0));
      slope = FR_el_smooth->GetBinContent(FR_el_smooth->FindFixBin(fabs(leta),1));

    } else {
      cout << "Need to implement getSmoothedFakeRateWeight() for muons! Returning fake rate weight = 0." << endl;
      return 0;

    }

    float fr = coeff + slope * lpt;
    //cout << "leta,lpt = " << leta << "," << lpt << "    coeff,slope = " <<  coeff << "," << slope << "    fr = " << fr << endl;
    return fr/(1-fr);

  } else return 0.0;

}
   
TF1 * helicityFraction_0 = new TF1("helicityFraction_0", "3./4*(TMath::Sqrt(1-x*x))^2", -1., 1.);
TF1 * helicityFraction_L = new TF1("helicityFraction_L", "3./8.*(1-x)^2"              , -1., 1.);
TF1 * helicityFraction_R = new TF1("helicityFraction_R", "3./8.*(1+x)^2"              , -1., 1.);

float helicityWeight(float yw, float ptw, float costheta, int pol)
{

  if (std::abs(costheta) > 1.) {
    //std::cout << " found an event with weird cosTheta = " << costheta << std::endl;
    //std::cout << " setting event weight to 0" << std::endl;
    return 0;
  }

  TH2 *hist_f0 = helicityFractions_0;
  TH2 *hist_fL = helicityFractions_L;
  TH2 *hist_fR = helicityFractions_R;

  // float yval  = std::abs(yw) > hist_f0->GetXaxis()->GetXmax() ? hist_f0->GetXaxis()->GetXmax() : yw;
  // float ptval = ptw > hist_f0->GetYaxis()->GetXmax() ? hist_f0->GetYaxis()->GetXmax() : ptw;

  int ywbin = std::max(1, std::min(hist_f0->GetNbinsX(), hist_f0->GetXaxis()->FindBin(yw )));
  int ptbin = std::max(1, std::min(hist_f0->GetNbinsY(), hist_f0->GetYaxis()->FindBin(ptw)));

  float f0 = hist_f0->GetBinContent(ywbin, ptbin);
  float fL = hist_fL->GetBinContent(ywbin, ptbin);
  float fR = hist_fR->GetBinContent(ywbin, ptbin);

  float f0Term = helicityFraction_0->Eval(costheta);
  float fLTerm = helicityFraction_L->Eval(costheta);
  float fRTerm = helicityFraction_R->Eval(costheta);

  if      (pol == 0) return f0*f0Term/(f0*f0Term+fL*fLTerm+fR*fRTerm);
  else if (pol == 1) return fL*fLTerm/(f0*f0Term+fL*fLTerm+fR*fRTerm);
  else if (pol == 2) return fR*fRTerm/(f0*f0Term+fL*fLTerm+fR*fRTerm);
        
  std::cout << "something went wrong in the helicity reweighting" << std::endl;
  return -99999.;

}
