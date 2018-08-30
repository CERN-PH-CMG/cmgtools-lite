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
#include <TMath.h>
TH2 * helicityFractions_0 = 0;
TH2 * helicityFractions_L = 0;
TH2 * helicityFractions_R = 0;

TH2 * FR_mu = 0;
TH2 * FR_el = 0;
TH2 * FRi_mu[30], *FRi_el[30];
TH2 *PR_mu=0;
TH2 *PR_el = 0;
// TH2 * FRcorrectionForPFMET = 0;
// TH2 * FRcorrectionForPFMET_i[5];

bool loadFRHisto(const std::string &histoName, const char *file, const char *name) {
  TH2 **histo = 0, **hptr2 = 0;
  TH2 * FR_temp = 0;
    if (histoName == "FR_mu")  { histo = & FR_mu;  hptr2 = & FRi_mu[0]; }
    else if (histoName == "FR_mu_qcdmc")  { histo = & FR_mu;  hptr2 = & FRi_mu[0]; }
    else if (histoName == "FR_el")  { histo = & FR_el;  hptr2 = & FRi_el[0]; }
    else if (histoName == "PR_mu")  { histo = & PR_mu;  }
    else if (histoName == "PR_el")  { histo = & PR_el;  }
    else if (histoName == "FR_el_qcdmc")  { histo = & FR_el;  hptr2 = & FRi_el[0]; }
    // else if (histoName == "FR_correction")  { histo = & FRcorrectionForPFMET; hptr2 = & FRcorrectionForPFMET_i[0]; }
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

// float puw2017_herwigg[80] = {0,0,0,2.27008,3.74564,2.25339,2.82139,2.97948,2.47187,2.77325,2.53951,2.33365,2.03668,1.88443,1.77833,1.67443,1.56289,1.3917,1.25253,1.06277,0.976758,0.870936,0.790535,0.713799,0.643822,0.551428,0.516994,0.465398,0.38879,0.349138,0.327546,0.30658,0.240941,0.251968,0.200709,0.181512,0.183967,0.157223,0.151671,0.106266,0.104634,0.0948796,0.0902638,0.0717555,0.0832775,0.0625131,0.0606511,0.0446805,0.036115,0.0295584,0.0344268,0.0403625,0.0211761,0.0270248,0.00522258,0.0136205,0.0214609,0.0390496,0.0286949,0.0197972,0.0425641,0,0.0236467,0.0257964,0,0,0,0.0405372,0,0,0,0,0,0,0,0,0,0,0,0};
// float puw2017_CP5[80] = {0,0,0,0.0720495,0.396272,0.368435,1.04472,1.10326,1.26087,2.03283,2.41803,1.9437,1.61881,1.51869,1.59003,1.60409,1.48697,1.55307,1.42429,1.04643,0.977148,0.925688,0.89919,0.696008,0.652616,0.619487,0.529287,0.476657,0.363019,0.380386,0.38475,0.295426,0.227875,0.243373,0.189566,0.184144,0.194828,0.150433,0.177622,0.0854195,0.0947405,0.109906,0.0900619,0.104282,0.0827099,0.0577756,0.068155,0.0438763,0.0360248,0.0237005,0.0300206,0.0309588,0.0250172,0.0200138,0.00428866,0.0180124,0.0150103,0.0204686,0.0142203,0.0225155,0.0600413,0,0.0150103,0.0300206,0,0,0,0.0900619,0,0,0,0,0,0,0,0,0,0,0,0};
// 
// float puw_2017( int nVert, bool herwMC){
//   if(herwMC == true) return puw2017_herwigg[nVert];
//   else if (nVert > 80) return 0;
//   else if(herwMC == false) return puw2017_CP5[nVert];
//   else return 0;
// }

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

/////////////////////////////////////////////////

float fakeRateWeight_2lssMVA_smoothed_FR(float l1pt, float l1eta, int l1pdgId, float l1mva,
                         float l2pt, float l2eta, int l2pdgId, float l2mva, float WP)
{
    int nfail = (l1mva < WP)+(l2mva < WP);
    switch (nfail) {
        case 1: {
            double fpt,feta; int fid;
            if (l1mva < l2mva) { fpt = l1pt; feta = std::abs(l1eta); fid = abs(l1pdgId); }
            else               { fpt = l2pt; feta = std::abs(l2eta); fid = abs(l2pdgId); }
            TH2 *hist = (fid == 11 ? FR_el : FR_mu);
	    int etabin = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(feta)));
	    float p0 = hist->GetBinContent(etabin, 1);
	    float p1 = hist->GetBinContent(etabin, 2);
	    
	    float fr = (fpt < 60.0 ? p0 + p1*fpt : p0 + p1*60);
	    //	    if(l1pt > 25 && l2pt > 20) cout<<"FT/TF "<<"\t eta \t"<<feta<<"\t pt \t"<<fpt<<" \t p0 \t"<<p0<<" \t p1 \t"<<p1<<"\t FR \t"<<(fr/(1-fr))<<endl;
            return fr/(1-fr);

        }
        case 2: {
            TH2 *hist1 = (abs(l1pdgId) == 11 ? FR_el : FR_mu);
            int etabin1 = std::max(1, std::min(hist1->GetNbinsY(), hist1->GetYaxis()->FindBin(std::abs(l1eta))));
	    float p0_1 = hist1->GetBinContent(etabin1, 1);
            float p1_1 = hist1->GetBinContent(etabin1, 2);
            float fr1 = (l1pt < 60.0 ? p0_1 + p1_1*l1pt :  p0_1 + p1_1*60);
            TH2 *hist2 = (abs(l2pdgId) == 11 ? FR_el : FR_mu);
            int etabin2 = std::max(1, std::min(hist2->GetNbinsY(), hist2->GetYaxis()->FindBin(std::abs(l2eta))));
	    float p0_2 = hist2->GetBinContent(etabin2, 1);
            float p1_2 = hist2->GetBinContent(etabin2, 2);
            float fr2 = (l1pt < 60.0 ? p0_2 + p1_2*l2pt :  p0_2 + p1_2*60);
	    // if(l1pt > 25 && l2pt > 20)cout<<"FF"<<"\t pt l1 \t"<<l1pt<<"\t eta l1 \t"<<abs(l1eta)<<"\t pt l2 \t"<<l2pt<<"\t eta l2 \t"<<abs(l2eta)<<" \t p0_1 \t"<<p0_1<<" \t p1_1 \t"<<p1_1<<" \t p0_2 \t"<<p0_2<<" \t p1_2 \t"<<p1_2<<"\t FR \t"<<(-fr1*fr2/((1-fr1)*(1-fr2)))<<endl;
         return -fr1*fr2/((1-fr1)*(1-fr2));
        }
        default: return 0;
    }
}


//////////////////////////////////////////////////////////


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

float fakeRateWeight_1l_i_smoothed(float lpt, float leta, int lpdgId, bool passWP, int iFR) {
  if (!passWP) {
    double fpt = lpt; double feta = std::fabs(leta); int fid = abs(lpdgId);
    TH2 *hist = (fid == 11 ? FRi_el[iFR] : FRi_mu[iFR]);
    if (hist == 0) {
      std::cout << "Error in fakeRateWeight_1l_i_smoothed: hist == 0. Returning 0" << std::endl;	
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

float weights_TT_and_TL(float iso1, float iso2, float cut, int category){
  int sum = (iso1 > cut) + (iso2 > cut);
  if      (sum == 2 && category == 0) return 1;
  else if (sum == 1 && category == 1) return 1;
  else if (sum == 0 && category == 2) return 1;
  else return 0;
}


float eps_smoothFR(float lpt, float leta, int lpdgId, int variation){
  TH2 *hist = (abs(lpdgId) == 11 ? FR_el : FR_mu);
  int etabin = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(abs(leta))));
  float p0 = hist->GetBinContent(etabin, 1);
  float p1 = hist->GetBinContent(etabin, 2);
  if(variation == 1){
    p0+=hist->GetBinError(etabin, 1);
    p1+=hist->GetBinError(etabin, 2);
  }
  else if (variation == 2){
    p0-=hist->GetBinError(etabin, 1);
    p1-=hist->GetBinError(etabin, 2);
  }
  else if (variation == 3){
    p1-=0.25*p1;
  }
  else if (variation == 4){
    p1+=0.25*p1;
  }
  
  else{
    p0+=0;
    p1+=0;

  }  
  float SFR = (lpt < 60.0 ? p0 + p1*lpt : p0 + p1*60);
  return(SFR/(1-SFR));
}

float eta_smoothPR(float lpt, float leta, int lpdgId, int variation){
  TH2 *hist = (abs(lpdgId) == 11 ? PR_el : PR_mu);
  int etabin = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(abs(leta))));
  
  float p0 = hist->GetBinContent(etabin,1);
  float p1 = hist->GetBinContent(etabin,2);
  float p2 = hist->GetBinContent(etabin,3);
  
  if(variation == 1){
    p0+=hist->GetBinError(etabin, 1);
    p1+=hist->GetBinError(etabin, 2);
    p2+=hist->GetBinError(etabin, 3);
  }
  else if (variation == 2){
    p0-=hist->GetBinError(etabin, 1);
    p1-=hist->GetBinError(etabin, 2);
    p2-=hist->GetBinError(etabin, 3);
  }
  else{
    p0+=0;
    p1+=0;
    p2+=0;

  }  

  float SPR = p0*TMath::Erf((lpt-p1)/p2);
  return((1-SPR)/SPR);
}


float fakeRateWeight_2lssMVA_usingPRs_smooth(float l1pt, float l1eta, int l1pdgId, float l1mva,
                                             float l2pt, float l2eta, int l2pdgId, float l2mva,int syst){

  //syst variation = 0 for nominal FRs/PRs, 1 for Up, 2 for Down variation within uncert of fit params.
  //for variation = 3 & 4 slope of FR fit is varried down & up resp. by 25%. 
  float WP=0.9;
  double  wSum =0.0;
  double  qSum =0.0;
  bool l1pass=l1mva > WP;
  bool l2pass=l2mva > WP;
  //  int syst = 0;
  float Eta_l1=eta_smoothPR(l1pt,l1eta,l1pdgId,syst);
  float Eta_l2=eta_smoothPR(l2pt,l2eta,l2pdgId,syst);
  float Eps_l1=eps_smoothFR(l1pt,l1eta,l1pdgId,syst);
  float Eps_l2=eps_smoothFR(l2pt,l2eta,l2pdgId,syst);
  
  double  norm  = 1./((1-Eps_l1*Eta_l1)*(1-Eps_l2*Eta_l2));

  if(l1pass && l2pass){
    wSum = - (Eps_l1*Eta_l1 + Eps_l2*Eta_l2);
    qSum =   Eps_l1*Eta_l1*Eps_l2*Eta_l2;
    //    cout<<"weight is TT \t"<<(wSum+qSum)/norm<<endl;
    return ((wSum+qSum)/norm);
  }
  else if (l1pass && !l2pass){
    wSum     = (Eps_l2 + Eps_l1*Eta_l1*Eps_l2);
    qSum     = -(Eps_l1*Eps_l2*Eta_l1);
    //    cout<<"weight is TL \t"<<(wSum+qSum)/norm<<endl;
    return ((wSum+qSum)/norm);
  }
  else if (!l1pass && l2pass){
    wSum  = (Eps_l1 + Eps_l2*Eta_l2*Eps_l1);
    qSum  = -(Eps_l1*Eps_l2*Eta_l2);
    //cout<<"weight is LT \t"<<(wSum+qSum)/norm<<endl;
    return ((wSum+qSum)/norm);
  }
  else if (!l1pass && !l2pass){
    wSum     = -2*Eps_l1*Eps_l2;
    qSum     = Eps_l1*Eps_l2;
    //cout<<"weight is LL \t"<<(wSum+qSum)/norm<<endl;
    return ((wSum+qSum)/norm);
  }
  else {
    
    cout<<"Unexpected 2l category, returning defaults"<<endl;
    //    cout<<"MVA values"<<l1mva<<"\t"<<l2mva<<endl;
    return 0;
  }
}  

  // for syst uncertainty on Fake ratios







//#endif
