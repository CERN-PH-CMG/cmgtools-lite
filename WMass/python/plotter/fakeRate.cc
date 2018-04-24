// #ifndef FAKERATE_H
// #define FAKERATE_H

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
TH2 * FRi_mu[30] = {0};
TH2 * FR_el = 0;
TH2 * FRi_el[30] = {0};

// FR for QCD MC, needed not to clash with that on data (above) in case they are used together
TH2 * FR_mu_qcdmc = 0;
TH2 * FRi_mu_qcdmc[30] = {0}; 
TH2 * FR_el_qcdmc = 0;
TH2 *FRi_el_qcdmc[30] = {0};

// prompt rate
TH2 * PR_mu = 0;
TH2 * PRi_mu[30] = {0};
TH2 * PR_el = 0;
TH2 * PRi_el[30] = {0};

// TH2 * FRcorrectionForPFMET = 0;
// TH2 * FRcorrectionForPFMET_i[5];

bool loadFRHisto(const std::string &histoName, const std::string file, const char *name) {

  TH2 **histo = 0, **hptr2 = 0;
  TH2 * FR_temp = 0;
  TH2 * PR_temp = 0;
  if (histoName == "FR_mu")  { histo = & FR_mu;  hptr2 = & FRi_mu[0]; }
  else if (histoName == "FR_mu_qcdmc")  { histo = & FR_mu_qcdmc;  hptr2 = & FRi_mu_qcdmc[0]; }
  else if (histoName == "FR_el")  { histo = & FR_el;  hptr2 = & FRi_el[0]; }
  else if (histoName == "FR_el_qcdmc")  { histo = & FR_elqcdmc;  hptr2 = & FRi_el_qcdmc[0]; }
  else if (histoName == "PR_el")  { histo = & PR_el;  hptr2 = & PRi_el[0]; }
  // else if (histoName == "FR_correction")  { histo = & FRcorrectionForPFMET; hptr2 = & FRcorrectionForPFMET_i[0]; }
  else if (TString(histoName).BeginsWith("FR_mu_i")) {histo = & FR_temp; hptr2 = & FRi_mu[TString(histoName).ReplaceAll("FR_mu_i","").Atoi()];}
  else if (TString(histoName).BeginsWith("FR_el_i")) {histo = & FR_temp; hptr2 = & FRi_el[TString(histoName).ReplaceAll("FR_el_i","").Atoi()];}
  else if (TString(histoName).Contains("helicityFractions_0")) { histo = & helicityFractions_0; }
  else if (TString(histoName).Contains("helicityFractions_L")) { histo = & helicityFractions_L; }
  else if (TString(histoName).Contains("helicityFractions_R")) { histo = & helicityFractions_R; }
  else if (TString(histoName).BeginsWith("PR_mu_i")) {histo = & PR_temp; hptr2 = & PRi_mu[TString(histoName).ReplaceAll("PR_mu_i","").Atoi()];}
  else if (TString(histoName).BeginsWith("PR_el_i")) {histo = & PR_temp; hptr2 = & PRi_el[TString(histoName).ReplaceAll("PR_el_i","").Atoi()];}
  if (histo == 0)  {
    std::cerr << "ERROR: histogram " << histoName << " is not defined in fakeRate.cc." << std::endl;
    return 0;
  }

  TFile *f = TFile::Open(file.c_str());
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

// float fakeRateWeight_1l_i_smoothed_FRcorr(float lpt, float leta, int lpdgId, bool passWP, int iFR, float pfmet) {
//   if (!passWP) {
//     double fpt = lpt; double feta = std::fabs(leta); int fid = abs(lpdgId);
//     TH2 *hist = (fid == 11 ? FRi_el[iFR] : FRi_mu[iFR]);
//     if (hist == 0) {
//       std::cout << "Error in fakeRateWeight_1l_i_smoothed_FRcorr: hist == 0. Returning 0" << std::endl;	
//       return 0;
//     }
//     int etabin = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(feta)));
//     float p0 = hist->GetBinContent(etabin, 1);
//     float p1 = hist->GetBinContent(etabin, 2);
//     if (iFR==1) p0 += hist->GetBinError(etabin, 1);
//     if (iFR==2) p0 -= hist->GetBinError(etabin, 1);
//     if (iFR==3) p1 += hist->GetBinError(etabin, 2);
//     if (iFR==4) p1 -= hist->GetBinError(etabin, 2);
//     float fr = p0 + p1*lpt;
//     /////////////
//     float FRcorrection = 1;
//     TH2 *hist_FRcorr = 0;
//     if (fid == 11 && pfmet >= 0) {
//       hist_FRcorr = FRcorrectionForPFMET_i[iFR];
//       if (hist_FRcorr == 0) {
// 	std::cout << "Error in fakeRateWeight_1l_i_smoothed_FRcorr: hist_FRcorr == 0. Returning 0" << std::endl;
// 	return 0;
//       } else {
// 	int pfmetbin = std::max(1, std::min(hist_FRcorr->GetNbinsX(), hist_FRcorr->GetXaxis()->FindBin(pfmet))); 
// 	etabin = std::max(1, std::min(hist_FRcorr->GetNbinsY(), hist_FRcorr->GetYaxis()->FindBin(leta))); 
// 	FRcorrection = hist_FRcorr->GetBinContent(pfmetbin,etabin); 
//       }
//     }
//     /////////////
//     return FRcorrection * fr/(1-fr);
//   } else return 0;
// }

// float fakeRateWeight_1l_i_smoothed(float lpt, float leta, int lpdgId, bool passWP, int iFR) {

//   // this function is used for backward compatibility, becasue I added a new argument with respect to original fakeRateWeight_1l_i_smoothed(...)
//   return fakeRateWeight_1l_i_smoothed_FRcorr(lpt, leta, lpdgId, passWP, iFR, -1);

// }

float fakeRateWeight_promptRateCorr_1l_i_smoothed(float lpt, float leta, int lpdgId, bool passWP, int iFR=0, int iPR=0) { //, int expected_pdgId=11) {

  // formula for fake rate including effect of prompt rate
  //
  // Let LNT denote the region passing loose but not tight selection, T the region passing the tight selection.
  // Let p and f denote the prompt and fake lepton rate respectively.
  // Then:
  // N(QCD in T) = f/(p-f) * (p*N(NLT) - (1-p)*N(T))
  // second term is negative by definition of p)
  // If p=1, then N(QCD in T) = f/(1-f) * N(NLT), which is the formula used in function fakeRateWeight_1l_i_smoothed()


  double fpt = lpt; double feta = std::fabs(leta); int fid = abs(lpdgId); 

  // int fAbsExpected_pdgId = abs(expected_pdgId);
  // if (fid != fAbsExpected_pdgId) {
  //   return 0;
  // }

  if (FRi_el[iFR] == 0 and FRi_mu[iFR] == 0) {
    // this is the case where the histogram was not loaded correctly (one is 0 because you use the other flavour)
    std::cout << "Error in fakeRateWeight_promptRateCorr_1l_i_smoothed: hist_fr == 0. Returning 0" << std::endl;	
    return 0;
  } 

  if (PRi_el[iPR] == 0 and PRi_mu[iPR] == 0) {
    // as above
    std::cout << "Error in fakeRateWeight_promptRateCorr_1l_i_smoothed: hist_pr == 0. Returning 0" << std::endl;	
    return 0;
  }


  TH2 *hist_fr = (fid == 11 ? FRi_el[iFR] : FRi_mu[iFR]);
  if (hist_fr == 0) {
    // this is the case where you expect electrons but get a muon, or viceversa
    // Indeed, selection is evaluated as 1 or 0 multiplying the event weight in TTree::Draw(...), so you potentially have all flavours here
    // do not issue warnign mewssages here, unless it is for testing
    //std::cout << "Error in fakeRateWeight_promptRateCorr_1l_i_smoothed: hist_fr == 0. It seems the flavour is not what you expect. Returning 0" << std::endl;	
    return 0;
  }

  TH2 *hist_pr = (fid == 11 ? PRi_el[iPR] : PRi_mu[iPR]);
  if (hist_pr == 0) {
    // as before
    //std::cout << "Error in fakeRateWeight_promptRateCorr_1l_i_smoothed: hist_pr == 0. Returning 0" << std::endl;	
    return 0;
  } 

  int etabin = std::max(1, std::min(hist_fr->GetNbinsX(), hist_fr->GetXaxis()->FindBin(feta)));
  // FR
  float p0 = hist_fr->GetBinContent(etabin, 1);
  float p1 = hist_fr->GetBinContent(etabin, 2);
  if (iFR==1) p0 += hist_fr->GetBinError(etabin, 1);
  if (iFR==2) p0 -= hist_fr->GetBinError(etabin, 1);
  if (iFR==3) p1 += hist_fr->GetBinError(etabin, 2);
  if (iFR==4) p1 -= hist_fr->GetBinError(etabin, 2);
  // now PR
  // eta bin is the same as for fake rate
  float p0_pr = hist_pr->GetBinContent(etabin, 1);
  float p1_pr = hist_pr->GetBinContent(etabin, 2);
  if (iPR==1) p0_pr += hist_pr->GetBinError(etabin, 1);
  if (iPR==2) p0_pr -= hist_pr->GetBinError(etabin, 1);
  if (iPR==3) p1_pr += hist_pr->GetBinError(etabin, 2);
  if (iPR==4) p1_pr -= hist_pr->GetBinError(etabin, 2);

  float fr = p0    + p1   *lpt;
  float pr = p0_pr + p1_pr*lpt;

  if (passWP) {
    // tight
    // returning a negative weight
    return fr*(pr-1)/(pr-fr); // pr=1 --> return 0
  } else {
    // not tight (but still loose)
    return fr*pr/(pr-fr);  // pr=1 --> return fr/(1-fr)
  }

}

//==============================

float fakeRateWeight_1l_i_smoothed(float lpt, float leta, int lpdgId, bool passWP, int iFR=0) { //, int expected_pdgId=11) {
  if (!passWP) {
    double fpt = lpt; double feta = std::fabs(leta); int fid = abs(lpdgId); 
    // int fAbsExpected_pdgId = abs(expected_pdgId);
    // if (fid != fAbsExpected_pdgId) {
    //   return 0;
    // }
    if (FRi_el[iFR] == 0 and FRi_mu[iFR] == 0) {
      // this is the case where the histogram was not loaded correctly (one is 0 because you use the other flavour)
      std::cout << "Error in fakeRateWeight_1l_i_smoothed: hist == 0. Returning 0" << std::endl;	
      return 0;
    } 
    TH2 *hist = (fid == 11 ? FRi_el[iFR] : FRi_mu[iFR]);
    if (hist == 0) {
      // this is the case where you expect electrons but get a muon, or viceversa
      // Indeed, selection is evaluated as 1 or 0 multiplying the event weight in TTree::Draw(...), so you potentially have all flavours here
      // do not issue warnign mewssages here, unless it is for testing
      //std::cout << "Error in fakeRateWeight_1l_i_smoothed: hist == 0. Returning 0" << std::endl;	
      //std::cout << "pdg ID = " << lpdgId << std::endl;
      return 0;
    }
    int etabin = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(feta)));
    float p0 = hist->GetBinContent(etabin, 1);
    float p1 = hist->GetBinContent(etabin, 2);
    if (iFR==1) p0 += hist->GetBinError(etabin, 1);
    if (iFR==2) p0 -= hist->GetBinError(etabin, 1);
    if (iFR==3) p1 += hist->GetBinError(etabin, 2);
    if (iFR==4) p1 -= hist->GetBinError(etabin, 2);
    float fr = p0 + p1*lpt;
    return fr/(1-fr);
  } else return 0;
}


float fakeRateWeight_1l_i(float lpt, float leta, int lpdgId, bool passWP, int iFR) {
  if (!passWP) {
    double fpt = lpt; double feta = std::fabs(leta); int fid = abs(lpdgId);
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

  float weight = 0.;
  float max_weight = 4.;

  if      (pol == 0) return std::min( f0*f0Term/(f0*f0Term+fL*fLTerm+fR*fRTerm), max_weight);
  else if (pol == 1) return std::min( fL*fLTerm/(f0*f0Term+fL*fLTerm+fR*fRTerm), max_weight);
  else if (pol == 2) return std::min( fR*fRTerm/(f0*f0Term+fL*fLTerm+fR*fRTerm), max_weight);
        
  std::cout << "something went wrong in the helicity reweighting" << std::endl;
  return -99999.;

}


//#endif
