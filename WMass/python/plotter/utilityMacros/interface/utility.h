#ifndef utility_h
#define utility_h

#include "./CMS_lumi.h"
#include "./centerOfMassEnergy.h"


#include <stdio.h>
#include <stdlib.h>
#include <cstdlib> //as stdlib.h
#include <cstdio>
#include <cmath>
#include <iostream>
#include <fstream>
#include <sstream>      // std::istringstream ; to read array of numbers from a line in a file
#include <string>
#include <vector>
#include <map>
#include <iomanip> //for input/output manipulators

#include <algorithm>  // to use the "reverse" function to reverse the order in the array
#include <Rtypes.h> // to use kColor

//ROOT header files
#include <TROOT.h>
#include <TAttFill.h>
#include <TAxis.h>
#include <TCanvas.h>
#include <TChain.h>
#include <TColor.h>
#include <TF1.h>
#include <TFile.h>
#include <TFitResult.h>
#include <TGraph2D.h>
#include <TGraphErrors.h>
#include <TGraphAsymmErrors.h>
#include <THStack.h>
#include <TH1.h>
#include <TH1D.h>
#include <TH1F.h>
#include <TH2.h>
#include <TKey.h>
#include <TLatex.h>
#include <TLegend.h>
#include <TLegendEntry.h>
#include <TLorentzVector.h>
#include <TMath.h>
#include <TMatrixDSym.h>
#include <TMultiGraph.h>
#include <TPad.h>
#include <TPaletteAxis.h>
#include <TPaveStats.h>
#include <TPaveText.h>
#include <TProfile.h>
#include <TTreeIndex.h>
#include <TTreeReader.h>
#include <TTreeReaderArray.h>
#include <TTreeReaderValue.h>
#include <TStyle.h>
#include <TString.h>
#include <TVector3.h>
#include <TVirtualFitter.h>

#include <RooStats/RooStatsUtils.h>
#include <RooStats/HLFactory.h>
#include <RooRealVar.h>
#include <RooArgSet.h>
#include <RooDataHist.h>
#include <RooFitResult.h>
#include <RooWorkspace.h>
#include <RooPlot.h>
#include <RooHistPdf.h>
#include <RooAddPdf.h>
#include <RooAbsPdf.h>
#include <RooRandom.h>
#include <RooBinning.h>
#include <RooMinimizer.h>

using namespace std;

//static string treeLocation = "/store/group/phys_smp/Wmass/perrozzi/ntuples/ntuples_2014_05_23_53X/";
//static string treeLocation = "/u2/emanuele/MCTrees_1LEP_80X_V1/";
static string PhpToCopy = "/afs/cern.ch/user/m/mciprian/www/index.php";

// define sample
enum class Sample {
  data_doubleEG, data_singleEG, data_doubleMu, data_singleMu, 
    wjets, wenujets, wmunujets, wtaunujets, zjets,
    wjets_LO, wenujets_LO, wmunujets_LO, wtaunujets_LO, zjets_LO,
    qcd_mu, qcd_ele, qcd_ele_fake, qcd_mu_fake, 
    top, diboson
    };

enum LepFlavour {electron = 11, muon = 13, tau = 15};

// moved to centerOfMassEnergy.h
//static Double_t intLumi = 36.4;
//static Double_t intLumi = 19.7;
//static Bool_t use8TeVSample = true;
/* static Bool_t useTrackMet = true; */
/* static Bool_t useAbsIso = false;  // rel iso or abs iso to cut (abs iso is rel iso times lepton pT) */
/* static bool useFakeRateForElectron = false; */
/* static bool useFakeRateForMuon = false; */

// electron ID variable
class electronID {
  
public:
 electronID(const Double_t & dEtaIn,  
	    const Double_t & dPhiIn, 
	    const Double_t & sigmaIetaIeta,  // Sigma ieta-ieta
	    const Double_t & HoE,
	    const Double_t & dxy, 
	    const Double_t & dz, 
	    const Double_t & invE_minus_invP,
	    const Int_t    & vertexFitProb,
	    const Int_t    & missingHits     
	    ) :
  dEtaIn(dEtaIn),
    dPhiIn(dPhiIn),
    sigmaIetaIeta(sigmaIetaIeta),
    HoE(HoE),
    dxy(dxy),
    dz(dz),
    invE_minus_invP(invE_minus_invP),
    vertexFitProb(vertexFitProb),
    missingHits(missingHits){
    };
  ~electronID(){};
  
  Double_t dEtaIn;
  Double_t dPhiIn;
  Double_t sigmaIetaIeta;
  Double_t HoE;
  Double_t dxy;
  Double_t dz;
  Double_t invE_minus_invP;
  Int_t vertexFitProb;
  Int_t missingHits;

};

class electronTriggeringMVAID {
  
public:
 electronTriggeringMVAID(const Double_t & mva,
			 const Double_t & relPFiso,
			 const Int_t    & convVeto,
			 const Int_t    & maxMissingHits     
			 ) :
  mva(mva),
    relPFiso(relPFiso),
    convVeto(convVeto),
    maxMissingHits(maxMissingHits) {};
  ~electronTriggeringMVAID(){};
  
  Double_t mva;
  Double_t relPFiso;
  Int_t convVeto;
  Int_t maxMissingHits;

};

class electronCutThreshold {
  
public:
 electronCutThreshold(const Double_t & deta,
		      const Double_t & dphi
		      ) :
  deta(deta),
    dphi(dphi)
    {};
  ~electronCutThreshold(){};
  
  Double_t deta;
  Double_t dphi;

};

//=======================================


class eleIdWorkingPoint {

public:
 eleIdWorkingPoint(const Double_t & dxy,
		   const Double_t & dz,
		   const Double_t & relIso04,
		   const Int_t    & convVeto,
		   const Int_t    & maxMissingHits,
		   const Int_t    & cutBasedId
		   ) 
   {
     dxy_ = dxy;
     dz_ = dz;
     relIso04_ = relIso04;
     convVeto_ = convVeto;
     maxMissingHits_ = maxMissingHits;
     cutBasedId_ = cutBasedId;
   }
 
  ~eleIdWorkingPoint(){};
  
  void setDxy(           const Double_t dxy)         { dxy_ = dxy;                       };
  void setDz(            const Double_t dz)          { dz_ = dz;                         };
  void setRelIso04(      const Double_t relIso04)    { relIso04_ = relIso04;             };
  void setConvVeto(      const Int_t convVeto)       { convVeto_ = convVeto;             };
  void setMaxMissingHits(const Int_t maxMissingHits) { maxMissingHits_ = maxMissingHits; };
  void setCutBasedId(    const Int_t cutBasedId)     { cutBasedId_ = cutBasedId;         };

  Double_t dxy()            const { return dxy_;            };
  Double_t dz()             const { return dz_;             };
  Double_t relIso04()       const { return relIso04_;       };
  Int_t    convVeto()       const { return convVeto_;       };
  Int_t    maxMissingHits() const { return maxMissingHits_; };
  Int_t    cutBasedId()     const { return cutBasedId_;     };


private:
  Double_t dxy_;
  Double_t dz_;
  Double_t relIso04_;
  Int_t    convVeto_;
  Int_t    maxMissingHits_;
  Int_t    cutBasedId_;

};

//=============================================


class plotManager {

public:
  plotManager(const string & histName,
	      const string & xAxisName,
	      const string & canvasName,
	      const int    & rebinFactor,
	      const int    & logy = 0 // 0 for both, 1 for no log, 2 for only log
	      ) 
  {
    histName_    = histName;
    xAxisName_   = xAxisName;
    canvasName_  = canvasName;
    rebinFactor_ = rebinFactor;    
    logy_        = logy;
  };

  ~plotManager() {};

  string getHistName()    const { return histName_;    };
  string getXaxisName()   const { return xAxisName_;   };
  string getCanvasName()  const { return canvasName_;  };
  int    getRebinFactor() const { return rebinFactor_; };
  int    getLogy()        const { return logy_; };

  void setHistName   (const string & histName  )  { histName_    = histName;    };
  void setXaxisName  (const string & xAxisName )  { xAxisName_   = xAxisName;   };
  void setCanvasName (const string & canvasName)  { canvasName_  = canvasName;  };  
  void setRebinFactor(const int    & rebinFactor) { rebinFactor_ = rebinFactor; };
  void setLogy       (const int    & logy)        { logy_        = logy; };

private:

  string histName_;
  string xAxisName_;
  string canvasName_;    
  int    rebinFactor_;
  int    logy_;

};


//======================================================

string getTexLabel(const string& sampleDir = "wjets") {

  string label = "";
  if (sampleDir == "qcd_ele") label = "QCD";
  else if (sampleDir == "qcd_mu") label = "QCD";
  else if (sampleDir == "wjets") label = "W(l#nu)+jets (aMC@NLO)";
  else if (sampleDir == "wenujets") label = "W(e#nu)+jets (aMC@NLO)";
  else if (sampleDir == "wmunujets") label = "W(#mu#nu)+jets (aMC@NLO)";
  else if (sampleDir == "wtaunujets") label = "W(#tau#nu)+jets (aMC@NLO)";
  else if (sampleDir == "wjets_LO") label = "W(l#nu)+jets (MadGraph)";
  else if (sampleDir == "wenujets_LO") label = "W(e#nu)+jets (MadGraph)";
  else if (sampleDir == "wmunujets_LO") label = "W(#mu#nu)+jets (MadGraph)";
  else if (sampleDir == "wtaunujets_LO") label = "W(#tau#nu)+jets (MadGraph)"; 
  else if (sampleDir == "zjets") label = "Z(ll)+jets (aMC@NLO)";
  else if (sampleDir == "zjets_LO") label = "Z(ll)+jets (MadGraph)";
  else if (sampleDir == "top") label = "t#bar{t}, single top";
  else if (sampleDir == "diboson") label = "WW, WZ";
  else if (sampleDir == "data_doubleEG") label = "data DoubleEG";
  else if (sampleDir == "data_singleEG") label = "data singleEG";
  else if (sampleDir == "data_doubleMu") label = "data DoubleMu";
  else if (sampleDir == "data_singleMu") label = "data singleMu";
  else if (sampleDir == "qcd_ele_fake") label = "QCD (fake rate)";
  else if (sampleDir == "qcd_mu_fake") label = "QCD (fake rate)";
  else {
    cout << "Error in getTexLabel(): directory name " << sampleDir << " unknown, please check. Exit" << endl;
    exit(EXIT_FAILURE);
  }
  
  return label;

}


//======================================================


void addOverflowInLastBin(TH1D *h) {

  // to avoid problems regarding memory leak for not deleting htemp in previous function, I sum directly the content of overflow bin in last bin

  Int_t lastBinNumber = h->GetNbinsX();
  Int_t overflowBinNumber = 1 + lastBinNumber;
  Double_t lastBinContent = h->GetBinContent(lastBinNumber);
  Double_t overflowBinContent = h->GetBinContent(overflowBinNumber);
  Double_t lastBinError = h->GetBinError(lastBinNumber);
  Double_t overflowBinError = h->GetBinError(overflowBinNumber);

  // add content of overflow bin in last bin and set error as square root of sum of error squares (with the assumption that they are uncorrelated)
  h->SetBinContent(lastBinNumber, lastBinContent + overflowBinContent);
  h->SetBinError(lastBinNumber, sqrt(lastBinError * lastBinError + overflowBinError * overflowBinError));
  // deleting content of overflow bin (safer, since I might be using that bin to add it again somewhere and I want it to be empty)                   
  h->SetBinContent(overflowBinNumber,0.0);
  h->SetBinError(overflowBinNumber,0.0);


}


//======================================================

void addUnderflowInFirstBin(TH1D *h) {

  // to avoid problems regarding memory leak for not deleting htemp in previous function, I sum directly the content of overflow bin in last bin

  // Int_t underflowBinNumber = 0;
  Double_t firstBinContent = h->GetBinContent(1);
  Double_t underflowBinContent = h->GetBinContent(0);
  Double_t firstBinError = h->GetBinError(1);
  Double_t underflowBinError = h->GetBinError(0);

  // add content of underflow bin in first bin and set error as square root of sum of error squares (with the assumption that they are uncorrelated)
  h->SetBinContent(1, firstBinContent + underflowBinContent);
  h->SetBinError(1, sqrt(firstBinError * firstBinError + underflowBinError * underflowBinError));
  // deleting content of underflow bin (safer, since I might be using that bin to add it again somewhere and I want it to be empty)                   
  h->SetBinContent(0,0.0);
  h->SetBinError(0,0.0);

}


//======================================================

void addOutliersInHistoRange(TH1D* h) {

  addOverflowInLastBin(h);
  addUnderflowInFirstBin(h);

}

//======================================================

void checkPoint(const Int_t& nCheck = 1, const Int_t& checkEveryN = 100000, const Int_t& nEvents = -1) {

  if(nEvents % checkEveryN == 0) {
    cout << "check "<< nCheck << ": nEvents = " << nEvents << endl;
    cout << endl;
  }

}

//======================================================

void checkPoint(const string& message = "", const Int_t& checkEveryN = 100000, const Int_t& nEvents = -1) {

  if(nEvents % checkEveryN == 0) {
    cout << "check "<< message << ": nEvents = " << nEvents << endl;
    cout << endl;
  }

}

//=====================================================================

Double_t my2sideCrystalBall(double* x, double* par) {

  //a priori we allow for different shape of right and left tail, thus two values of alpha and n 

  Double_t xcur = x[0];
  Double_t alphaL = par[0];
  Double_t nL = par[1];
  Double_t mu = par[2];
  Double_t sigma = par[3];
  Double_t N = par[4];
  Double_t alphaR = par[5];
  Double_t nR = par[6];
  Double_t t = (xcur-mu)/sigma;
  Double_t absAlphaL = fabs((Double_t)alphaL);
  Double_t invAbsAlphaL = 1./absAlphaL;
  Double_t absAlphaR = fabs((Double_t)alphaR);
  Double_t invAbsAlphaR = 1./absAlphaR;

  
  if ( t<-absAlphaL ) {
    //cout<<"checkpoint dscb left"<<endl;
    Double_t AL = TMath::Power(nL*invAbsAlphaL,nL)*exp(-0.5*absAlphaL*absAlphaL);
    Double_t BL = nL*invAbsAlphaL - absAlphaL;
    return N*AL*TMath::Power(BL-t,-nL);
  } else if ( t <= absAlphaR )  {
    //cout<<"checkpoint dscb gaussian"<<endl;
    return N*exp(-0.5*t*t);
  } else {
    //cout<<"checkpoint dscb right"<<endl;
    Double_t AR = TMath::Power(nR*invAbsAlphaR,nR)*exp(-0.5*absAlphaR*absAlphaR);
    Double_t BR = nR*invAbsAlphaR - absAlphaR;
    return N*AR*TMath::Power(BR+t,-nR);
  }

}


//======================================================

void createPlotDirAndCopyPhp(const string& outputDIR) {

  if (outputDIR != "./") {
    system(("mkdir -p " + outputDIR).c_str());
    system(("cp "+ PhpToCopy + " " + outputDIR).c_str());
  }

}


//======================================================

string getStringFromEnumSample(const Sample& sample = Sample::zjets) {

  if (sample == Sample::data_doubleEG)
    return "data_doubleEG";
  else if (sample == Sample::data_singleEG)
    return "data_singleEG";
  if (sample == Sample::data_doubleMu)
    return "data_doubleMu";
  else if (sample == Sample::data_singleMu)
    return "data_singleMu";
  else if (sample == Sample::zjets)
    return "zjets";
  else if (sample == Sample::zjets_LO)
    return "zjets_LO";
  else if (sample == Sample::wjets)
    return "wjets";
  else if (sample == Sample::wenujets)
    return "wenujets";
  else if (sample == Sample::wmunujets)
    return "wmunujets";
  else if (sample == Sample::wtaunujets)
    return "wtaunujets";
  else if (sample == Sample::wjets_LO)
    return "wjets_LO";
  else if (sample == Sample::wenujets_LO)
    return "wenujets_LO";
  else if (sample == Sample::wmunujets_LO)
    return "wmunujets_LO";
  else if (sample == Sample::wtaunujets_LO)
    return "wtaunujets_LO";
  else if (sample == Sample::qcd_mu)
    return "qcd_mu";
  else if (sample == Sample::qcd_ele)
    return "qcd_ele";
  else if (sample == Sample::top)
    return "top";
  else if (sample == Sample::diboson)
    return "diboson";
  else if (sample == Sample::qcd_ele_fake)
    return "qcd_ele_fake";
  else if (sample == Sample::qcd_mu_fake)
    return "qcd_mu_fake";
  else {
    cout << "Error in getStringFromEnumSample(): unknown sample, please check. Exit" << endl;
    exit(EXIT_FAILURE);    
  }

}

// ============================================

void quantiles(TGraph*gr = NULL, TH1* h = NULL) {

  const Int_t nq = gr->GetN(); // 20 bins

  Double_t xq[nq];  // position where to compute the quantiles in [0,1]                                                                  
  Double_t yq[nq];  // array to contain the quantiles                                                                             

  for (Int_t i=0 ; i<nq ; i++) 
    xq[i] = Float_t(i)/(nq-1);

  h->GetQuantiles(nq,yq,xq);

  for (Int_t i=0 ; i<nq ; i++) 
    gr->SetPoint(i,yq[i],xq[i]); // put efficiency on y axis
  

}

//=============================================

Double_t doSoverB(TGraph* gsob = NULL, TH1* hwjets = NULL, TH1* hqcd = NULL) {

  const UInt_t npoints = gsob->GetN(); 

  Double_t max = 0.0;
  Double_t xin = hwjets->GetBinCenter(1);
  Double_t step = (hwjets->GetBinCenter(hwjets->GetNbinsX()) - xin)/npoints;
  Double_t sob = 0.0;
  Double_t x_i = 0.0;
  Double_t s = 0.0; 
  Double_t b = 0.0;

  for (UInt_t i = 0; i <npoints; i++ ) {
    x_i = xin + ((Double_t)i) * step;
    s = hwjets->Integral(0, hwjets->FindFixBin(x_i));
    b = hqcd->Integral(0, hqcd->FindFixBin(x_i)); 
    sob = s / b;
    //cout << "x: " << x_i << "    s: " << s << "    b: " << b << "    s/b: " << sob << endl;
    gsob->SetPoint(i,x_i, sob);
    if (max < sob) max = sob;
  }

  return max;

}

//=============================================

void doEfficiencyFromTH2(TH2* h2 = NULL, const TH2* h2orig = NULL) {

  for (Int_t ix = 1; ix <= h2->GetNbinsX(); ix++) {

    // include underflow and overflow in the integral
    Double_t yIntegralFixedX = h2orig->Integral(ix, ix, 0, 1 + h2orig->GetNbinsY());

    for (Int_t iy = 1; iy <= h2->GetNbinsY(); iy++) {

      h2->SetBinContent(ix,iy, h2orig->Integral(ix, ix, 0, iy)/yIntegralFixedX);

    }

  }
  
}

//=============================================

void makeROC(TGraph* gr = NULL, const TH1* hsTmp = NULL, const TH1* hbTmp = NULL) {

  // clone original histogram
  // this is only needed if the histogram passed as argument is declared const in this function
  // because in this case cannot use methods like TH1::FindBin which is not declared const
  TH1* hs = (TH1*) hsTmp->Clone(); 
  TH1* hb = (TH1*) hbTmp->Clone(); 

  const Int_t nq = gr->GetN(); 
  Double_t xq[nq];  // position where to compute the quantiles in [0,1]                                                                  
  Double_t yq[nq];  // array to contain the quantiles                                                                             

  for (Int_t i=0 ; i<nq ; i++) 
    xq[i] = Float_t(i)/(nq-1);

  hs->GetQuantiles(nq,yq,xq);

  Double_t integralB = hb->Integral(0, hb->GetNbinsX()+1);

  for (Int_t ipoint = 0; ipoint < nq; ipoint++) {

    Double_t effB = hb->Integral(0, hb->FindFixBin(yq[ipoint])) / integralB;
    gr->SetPoint(ipoint, effB, xq[ipoint]);

  }

}

//======================================================

void myAddOverflowInLastBin(TH1 *h) { 

  Int_t lastBinNumber = h->GetNbinsX();
  Int_t overflowBinNumber = 1 + lastBinNumber;
  Double_t lastBinContent = h->GetBinContent(lastBinNumber);
  Double_t overflowBinContent = h->GetBinContent(overflowBinNumber);
  Double_t lastBinError = h->GetBinError(lastBinNumber);
  Double_t overflowBinError = h->GetBinError(overflowBinNumber);

  // add content of overflow bin in last bin and set error as square root of sum of error squares (with the assumption that they are uncorrelated)
  h->SetBinContent(lastBinNumber, lastBinContent + overflowBinContent);
  h->SetBinError(lastBinNumber, sqrt(lastBinError * lastBinError + overflowBinError * overflowBinError));
  // deleting content of last bin (safer, since I might be using that bin to add it again somewhere and I want it to be empty)
  h->SetBinContent(overflowBinNumber,0.0);
  h->SetBinError(overflowBinNumber,0.0);

}


//======================================================

void myRebinHisto(TH1 *h, const Int_t rebinFactor = 1) {

  if (rebinFactor != 1) {
    h->Rebin(rebinFactor);
    if ( (h->GetNbinsX() % rebinFactor) != 0) myAddOverflowInLastBin(h);
  }

}

//======================================================

TH1* getHistCloneFromFile(TFile* inputFile = NULL, const string& hvarName = "", const string& sampleDir = "") {

  // use sampleDir to select a directory, default is the first one
  // use sampleDir without "/" at the end

  TH1* hvar = NULL;

  if (!inputFile || inputFile == NULL || inputFile->IsZombie()) {
    cout << "Error in getHistCloneFromFile(): file not opened. Exit" << endl;
    exit(EXIT_FAILURE);
  }

  if (sampleDir == "") hvar = (TH1*) inputFile->Get((hvarName).c_str());
  else hvar = (TH1*) inputFile->Get((sampleDir + "/" + hvarName).c_str());
  if (!hvar || hvar == NULL) {
    cout << "Error in getHistCloneFromFile(): histogram '" << hvarName << "' not found in file (directory is " << sampleDir << "). End of programme." << endl;
    exit(EXIT_FAILURE);
  }

  return (TH1*) hvar->Clone(sampleDir.c_str());

}

//==================================================

TGraph* getGraphCloneFromFile(TFile* inputFile = NULL, const string& graphvarName = "", const string& sampleDir = "", const string &filename = "") {

  // use sampleDir to select a directory, default is the first one
  // use sampleDir without "/" at the end

  TGraph* graphvar = NULL;

  if (!inputFile || inputFile == NULL || inputFile->IsZombie()) {
    cout << "Error in getGraphCloneFromFile(): file not opened. Exit" << endl;
    exit(EXIT_FAILURE);
  }

  if (sampleDir == "") graphvar = (TGraph*) inputFile->Get((graphvarName).c_str());
  else graphvar = (TGraph*) inputFile->Get((sampleDir + "/" + graphvarName).c_str());
  if (!graphvar || graphvar == NULL) {
    cout << "Error in getGraphCloneFromFile(): graph '" << graphvarName << "' not found in file '" << filename << "' (directory is " << sampleDir << "). End of programme." << endl;
    exit(EXIT_FAILURE);
  }

  return (TGraph*) graphvar->Clone(sampleDir.c_str());

}


//======================================================

TH2* getHist2CloneFromFile(TFile* inputFile = NULL, const string& hvarName = "", const string& sampleDir = "") {

  // use sampleDir to select a directory, default is the first one
  // use sampleDir without "/" at the end

  TH2* hvar = NULL;

  if (!inputFile || inputFile == NULL || inputFile->IsZombie()) {
    cout << "Error in getHistCloneFromFile(): file not opened. Exit" << endl;
    exit(EXIT_FAILURE);
  }

  if (sampleDir == "") hvar = (TH2*) inputFile->Get((hvarName).c_str());
  else hvar = (TH2*) inputFile->Get((sampleDir + "/" + hvarName).c_str());
  if (!hvar || hvar == NULL) {
    cout << "Error in getHistCloneFromFile(): histogram '" << hvarName << "' not found in file (directory is " << sampleDir << "). End of programme." << endl;
    exit(EXIT_FAILURE);
  }

  return (TH2*) hvar->Clone(sampleDir.c_str());

}

//======================================================

void checkNotNullPtr(TH1* hptr, const string& ptrName = "hptr") {

  if ( hptr == NULL) {
    cout << "Error: pointer " << ptrName << " is NULL. Exit" << endl;
    exit(EXIT_FAILURE);
  }

}

//======================================================

void checkNotNullPtr(TGraph* graphptr, const string& ptrName = "graphptr") {

  if ( graphptr == NULL) {
    cout << "Error: pointer " << ptrName << " is NULL. Exit" << endl;
    exit(EXIT_FAILURE);
  }

}

//======================================================

void checkNotNullPtr(TObject* objptr, const string& ptrName = "graphptr") {

  if ( objptr == NULL) {
    cout << "Error: pointer " << ptrName << " is NULL. Exit" << endl;
    exit(EXIT_FAILURE);
  }

}

//======================================================

void checkNotNullPtr(TH2* hptr, const string& ptrName = "hptr") {

  if ( hptr == NULL) {
    cout << "Error: pointer " << ptrName << " is NULL. Exit" << endl;
    exit(EXIT_FAILURE);
  }

}


//======================================================

string getStringFromDouble(const Double_t& num = 1.0, const Double_t epsilon = 0.00001) {
  
  Int_t i = (Int_t) num;
  // stringstream ss;                                                                                      
  // ss<<i;                                                                                                                         
  // string numStr = ss.str();                                                                                         
  Int_t int_decim = (Int_t) (1000 * (num - (Double_t) i + epsilon));
  if      (int_decim%1000 == 0) return string(Form("%dp%d",i,int_decim/1000));
  else if (int_decim%100 == 0)  return string(Form("%dp%d",i,int_decim/100));
  else if (int_decim%10 == 0)   return string(Form("%dp%d",i,int_decim/10));
  else                          return string(Form("%dp%d",i,int_decim));

}

//======================================================                                                                


void fillTH1(TH1* histo, const Double_t val, const Double_t weight = 1.0, const Bool_t useOverflowBin = true) {

  // embed overflow if useOverflowBin = true (default)

  if(val < histo->GetXaxis()->GetBinLowEdge(histo->GetNbinsX()+1))
    histo->Fill(val,weight);
  else if ( useOverflowBin )
    histo->Fill(histo->GetXaxis()->GetBinCenter(histo->GetNbinsX()),weight);
  else 
    histo->Fill(val,weight);

}


//======================================================


void fillTH2(TH2* histo, const Double_t valx, const Double_t valy, const Double_t weight = 1.0){ // Embed- the overflow
  
  Double_t x = 0;
  if(valx < histo->GetXaxis()->GetBinLowEdge(histo->GetNbinsX()+1))
    x = valx;
  else
    x =histo->GetXaxis()->GetBinCenter(histo->GetNbinsX());
  double y = 0;
  if(valy < histo->GetYaxis()->GetBinLowEdge(histo->GetNbinsY()+1))
    y = valy;
  else
    y = histo->GetYaxis()->GetBinCenter(histo->GetNbinsY());

  histo->Fill(x,y,weight);
}

//======================================================

Double_t getDphi(Double_t phi1, Double_t phi2) {

  Double_t dphi = phi1 -phi2;

  if(dphi > TMath::Pi())
    dphi -= 2*TMath::Pi();

  if(dphi < -TMath::Pi())
    dphi += 2*TMath::Pi();

  return dphi;

}

//======================================================

Int_t findGenPartFromWLNu(const Int_t nGenParticles,
                          TTreeReaderArray<Int_t>& particleId,
                          TTreeReaderArray<Int_t>& particleMotherId,
			  const Int_t lepFlavour,
			  Int_t& genPartIndex2,
			  Int_t& genBosonIndex)
{

  // This function looks whether there are a lepton and a neutrino from a W in                                          
  //the array. It works when using Emanuele's tree. 
  // It also looks for the index of the mother in the list of particles, that is a W
  // The algorithm looks for a lepton and neutrino (or antineutrino) originating from mother in the list of generated particles.
  // The function returns 1 if the search is successful, and 0 otherwise                                                        

  genPartIndex2 = -1;
  genBosonIndex = -1;
  
  Int_t genPartIndex = -1;  // will become the index of the lepton from  W if search is successful. Otherwise it is a negative value 
  Int_t i = 0;      // index of the array                                                                                            
  Int_t Wid = 0;
  Int_t lepCharge = 0;
  Bool_t Wfound = false;
  Bool_t firstLepFound = false;
  Bool_t secondLepFound = false;
  
  //first look for a W (assuming there's only 1)                                                                           

  // PGD ID W+(W-)     = 24(-24)
  // PDG ID e-(e+)     = 11(-11)
  // PDG ID mu-(mu+)   = 13(-13)
  // PDG ID tau-(tau+) = 15(-15) 
  
  while ((not Wfound) && (i < nGenParticles)) {

    if (fabs(particleId[i]) == 24) {

      genBosonIndex = i;
      Wid = particleId[i];
      lepCharge =  (Wid > 0) ? -1 : 1;
      Wfound = true;
      //cout << "Found W" << endl;
  
    }
    i++;
  }

  i = 0;
  
  if (Wfound) {

    while ((not firstLepFound) && (i < nGenParticles)) {
      
      if ( (particleMotherId[i] == Wid) && (particleId[i] == (lepCharge * lepFlavour)) ) {
	genPartIndex = i;
  	firstLepFound = true;
      }
      i++;
  
    }

    i = 0; // to search for neutrino, reset i and start search from the beginning

    if (firstLepFound) {

      Int_t chargedLeptonPdgID = particleId[genPartIndex];
      Int_t neutrinoPdgID = 0;
      if (chargedLeptonPdgID == 11) neutrinoPdgID = -12;
      else if (chargedLeptonPdgID == -11) neutrinoPdgID = 12;
      else if (chargedLeptonPdgID == 13) neutrinoPdgID = -14;
      else if (chargedLeptonPdgID == -13) neutrinoPdgID = 14;

      while ( (not secondLepFound) && (i < nGenParticles)) {
	
	if ( (particleMotherId[i] == Wid) && (particleId[i] == neutrinoPdgID) ) {
	  genPartIndex2 = i;
	  secondLepFound = true;
	}
	i++;
	
      }

    }

   
  }
   
  //if (secondLepFound) cout << particleId[genBosonIndex] << " " << particleId[genPartIndex] << " " << particleId[genPartIndex2] << endl;

  if (firstLepFound && secondLepFound) return genPartIndex;  // return index of first particle
  else return -1;                           // if 2 leptons are not found, return -1 as if even the first one was not found

}


//======================================================

Int_t findGenPartFromZLL(const Int_t nGenParticles,
			 TTreeReaderArray<Int_t>& particleId,
			 TTreeReaderArray<Int_t>& particleMotherId,
			 const Int_t lepFlavour,
			 Int_t& genPartIndex2,
			 Int_t& genBosonIndex)
{

  // This function looks whether there are a lepton and a neutrino from a W in                                          
  //the array. It works when using Emanuele's tree. 
  // It also looks for the index of the mother in the list of particles, that is a W
  // The algorithm looks for a lepton and neutrino (or antineutrino) originating from mother in the list of generated particles.
  // The function returns 1 if the search is successful, and 0 otherwise                                                        

  Int_t genPartIndex = -1;  // will become the index of the lepton from  W if search is successful. Otherwise it is a negative value 
  Int_t i = 0;      // index of the array                                                                                            
  Int_t Zid = 23;
  Bool_t Zfound = false;
  Bool_t firstLepFound = false;
  Bool_t secondLepFound = false;

  genPartIndex2 = -1;
  genBosonIndex = -1;
  
  //first look for a Z (assuming there's only 1)                                                          
      
  // PGD ID Z          = 23
  // PDG ID e-(e+)     = 11(-11)
  // PDG ID mu-(mu+)   = 13(-13)
  // PDG ID tau-(tau+) = 15(-15) 
  
  while ((not Zfound) && (i < nGenParticles)) {

    if (fabs(particleId[i]) == Zid) {
      Zfound = true;
      genBosonIndex = i;
    }
    i++;

  }
  
  i = 0;

  if (Zfound) {
  
    // search first lepton from Z
    while ((not firstLepFound) && (i < nGenParticles)) {

      if ( (particleMotherId[i] == Zid) && (fabs(particleId[i]) == lepFlavour) ) {
	genPartIndex = i;
	firstLepFound = true;
      }
      i++;
  
    }

    // search for second lepton (start from current i)
    if (firstLepFound) {

      while ( (not secondLepFound) && (i < nGenParticles)) {
	
	if ( (particleMotherId[i] == Zid) && ( (particleId[i] + particleId[genPartIndex]) == 0) ) {
	  genPartIndex2 = i;
	  secondLepFound = true;
	}
	i++;
	
      }

    }

  }

  if (firstLepFound && secondLepFound) return genPartIndex;  // return index of first particle
  else return -1;                           // if 2 leptons are not found, return -1 as if even the first one was not found

}


//=============================================================                                                                      

Bool_t getAxisRangeFromUser(string& axisName, Double_t& min, Double_t& max, 
			    const string& axisNameTmp = "", 
			    const string& separator = "::", 
			    const string& rangeSeparator = ","
			    ) {
  
  Bool_t setXAxisRangeFromUser = false;
  size_t pos = axisNameTmp.find(separator);
    
  if (pos != string::npos) {
    string xrange = "";
    setXAxisRangeFromUser = true;
    axisName.assign(axisNameTmp, 0, pos);
    xrange.assign(axisNameTmp, pos + separator.size(), string::npos);
    pos = xrange.find(rangeSeparator);
    string numString = "";
    numString.assign(xrange,0,pos);
    min = std::stod(numString);
    numString.assign(xrange,pos + rangeSeparator.size(), string::npos);
    max = std::stod(numString);
  } else {
    axisName = axisNameTmp;
  }

  return setXAxisRangeFromUser;

}

//=============================================

void drawGraph(vector<TGraph*> gr_roc_S_B = {}, 
	       const string& xAxisNameTmp = "xAxis", 
	       const string& yAxisNameTmp = "yAxis", 
	       const string& canvasName = "default",
	       const string& outputDIR = "./",
	       const vector<string>& leg_roc = {""},
	       const vector<Double_t>& legCoord = {0.5,0.15,0.9,0.35}) 
{

  string xAxisName = "";
  Double_t xmin = 0;
  Double_t xmax = 0;
  Bool_t setXAxisRangeFromUser = getAxisRangeFromUser(xAxisName, xmin, xmax, xAxisNameTmp);

  string yAxisName = "";
  Double_t ymin = 0;
  Double_t ymax = 0;
  Bool_t setYAxisRangeFromUser = getAxisRangeFromUser(yAxisName, ymin, ymax, yAxisNameTmp);


  Int_t nGraphs = gr_roc_S_B.size();

  TCanvas* canvas = new TCanvas("canvas","",600,600);
  canvas->cd();
  canvas->SetFillColor(0);
  canvas->SetGrid();
  canvas->SetRightMargin(0.06);
  canvas->cd();

  //  TLegend leg (0.5,0.15,0.9,0.15+0.05*nGraphs);
  TLegend leg (legCoord[0],legCoord[1],legCoord[2],legCoord[3]);
  leg.SetFillColor(0);
  leg.SetFillStyle(0);
  leg.SetBorderSize(0);

  Int_t colorList[] = {kBlack, kBlue, kRed, kGreen+2, kOrange+1, kCyan+2, kGray+2};

  for (Int_t ig = 0; ig < nGraphs; ig++) {
    gr_roc_S_B[ig]->SetMarkerStyle(21);
    gr_roc_S_B[ig]->SetMarkerColor(colorList[ig]);
    gr_roc_S_B[ig]->SetLineColor(colorList[ig]);
    gr_roc_S_B[ig]->SetFillColor(colorList[ig]);
    if (ig == 0) gr_roc_S_B[ig]->Draw("alp");
    else gr_roc_S_B[ig]->Draw("lp same");
    leg.AddEntry(gr_roc_S_B[ig],leg_roc[ig].c_str(),"LF");
  }
  leg.Draw("same");

  gr_roc_S_B[0]->GetXaxis()->SetTitle(xAxisName.c_str());
  gr_roc_S_B[0]->GetYaxis()->SetTitle(yAxisName.c_str());
  if (setXAxisRangeFromUser) gr_roc_S_B[0]->GetXaxis()->SetRangeUser(xmin,xmax);
  if (setYAxisRangeFromUser) gr_roc_S_B[0]->GetYaxis()->SetRangeUser(ymin,ymax);

  canvas->RedrawAxis("sameaxis");

  canvas->SaveAs((outputDIR+canvasName+".png").c_str());
  canvas->SaveAs((outputDIR+canvasName+".pdf").c_str());

}

//=============================================

void drawGraphCMS(vector<TGraph*> grList = {}, 
		  const string& xAxisNameTmp = "xAxis", 
		  const string& yAxisNameTmp = "yAxis", 
		  const string& canvasName = "default",
		  const string& outputDIR = "./",
		  const vector<string>& leg_roc = {""},
		  const vector<Double_t>& legCoord = {0.5,0.15,0.9,0.35},
		  const Double_t lumi = -1.0 
		  ) 

{

  string xAxisName = "";
  Double_t xmin = 0;
  Double_t xmax = 0;
  Bool_t setXAxisRangeFromUser = getAxisRangeFromUser(xAxisName, xmin, xmax, xAxisNameTmp);

  string yAxisName = "";
  Double_t ymin = 0;
  Double_t ymax = 0;
  Bool_t setYAxisRangeFromUser = getAxisRangeFromUser(yAxisName, ymin, ymax, yAxisNameTmp);


  Int_t nGraphs = grList.size();

  TCanvas* canvas = new TCanvas("canvas","",600,600);
  canvas->cd();
  canvas->SetFillColor(0);
  canvas->SetGrid();
  canvas->SetRightMargin(0.06);
  canvas->cd();

  //  TLegend leg (0.5,0.15,0.9,0.15+0.05*nGraphs);
  TLegend leg (legCoord[0],legCoord[1],legCoord[2],legCoord[3]);
  leg.SetFillColor(0);
  leg.SetFillStyle(0);
  leg.SetBorderSize(0);

  Int_t colorList[] = {kBlack, kRed, kGreen+2, kBlue, kOrange+1, kCyan+2, kGray+2};

  for (Int_t ig = 0; ig < nGraphs; ig++) {
    grList[ig]->SetMarkerStyle(20);
    grList[ig]->SetMarkerColor(colorList[ig]);
    grList[ig]->SetLineColor(colorList[ig]);
    grList[ig]->SetLineWidth(2);
    grList[ig]->SetFillColor(colorList[ig]);
    if (ig == 0) grList[ig]->Draw("ap");
    else grList[ig]->Draw("p same");
    leg.AddEntry(grList[ig],leg_roc[ig].c_str(),"LF");
  }
  leg.Draw("same");

  grList[0]->GetXaxis()->SetTitleSize(0.05);
  grList[0]->GetXaxis()->SetLabelSize(0.04);
  grList[0]->GetYaxis()->SetTitleOffset(1.1);
  grList[0]->GetYaxis()->SetTitleSize(0.05);
  grList[0]->GetYaxis()->SetLabelSize(0.04);
  grList[0]->GetXaxis()->SetTitle(xAxisName.c_str());
  grList[0]->GetYaxis()->SetTitle(yAxisName.c_str());
  if (setXAxisRangeFromUser) grList[0]->GetXaxis()->SetRangeUser(xmin,xmax);
  if (setYAxisRangeFromUser) grList[0]->GetYaxis()->SetRangeUser(ymin,ymax);

  //  CMS_lumi(canvas,Form("%.1f",lumi));
  if (lumi < 0) CMS_lumi(canvas,"",true,false);
  else CMS_lumi(canvas,Form("%.1f",lumi),true,false);
  setTDRStyle();

  canvas->RedrawAxis("sameaxis");

  canvas->SaveAs((outputDIR+canvasName+".png").c_str());
  canvas->SaveAs((outputDIR+canvasName+".pdf").c_str());

}


//=============================================================

void drawTH1pair(TH1* h1, TH1* h2, 
		 const string& xAxisNameTmp = "", const string& yAxisName = "Events", const string& canvasName = "default", 
		 const string& outputDIR = "./", 
		 const string& legEntry1 = "data", const string& legEntry2 = "MC", const string& ratioPadYaxisName = "data/MC", 
		 const Double_t lumi = -1.0, 
		 const Int_t rebinFactor = 1, 
		 const Bool_t drawPlotLogY = true) 
{

  TH1::SetDefaultSumw2(); //all the following histograms will automatically call TH1::Sumw2() 

  string xAxisName = "";
  Double_t xmin = 0;
  Double_t xmax = 0;
  Bool_t setXAxisRangeFromUser = getAxisRangeFromUser(xAxisName, xmin, xmax, xAxisNameTmp);

  // cout << "xAxisName = " << xAxisName << "   xmin = " << xmin << "  xmax = " << xmax << endl;

  myRebinHisto(h1,rebinFactor);
  myRebinHisto(h2,rebinFactor);

  Double_t intNum, intDen, errNum, errDen;
  intNum = h1->IntegralAndError(1,h1->GetNbinsX(),errNum);
  intDen = h2->IntegralAndError(1,h2->GetNbinsX(),errDen);
  Double_t IntegralRatio = intNum/intDen;
  Double_t ratioError = IntegralRatio * sqrt(errNum*errNum/(intNum*intNum) + errDen*errDen/(intDen*intDen));

  if (yAxisName == "a.u.") {
    h1->Scale(1./h1->Integral());
    h2->Scale(1./h2->Integral());
  }

  h1->SetStats(0);
  h2->SetStats(0);

  TCanvas* canvas = new TCanvas("canvas","",600,700);
  canvas->cd();
  canvas->SetTickx(1);
  canvas->SetTicky(1);
  canvas->cd();
  canvas->SetBottomMargin(0.3);
  canvas->SetRightMargin(0.06);

  TPad *pad2 = new TPad("pad2","pad2",0,0.,1,0.9);
  pad2->SetTopMargin(0.7);
  pad2->SetRightMargin(0.06);
  pad2->SetFillColor(0);
  pad2->SetGridy(1);
  pad2->SetFillStyle(0);

  TH1* frame =  (TH1*) h1->Clone("frame");
  frame->GetXaxis()->SetLabelSize(0.04);
  frame->SetStats(0);

  h1->SetLineColor(kBlack);
  h1->SetMarkerColor(kBlack);
  h1->SetMarkerStyle(20);
  h1->SetMarkerSize(1);

  h1->GetXaxis()->SetLabelSize(0);
  h1->GetYaxis()->SetTitle(yAxisName.c_str());
  h1->GetYaxis()->SetTitleOffset(1.1);
  // h1->GetYaxis()->SetTitleOffset(0.8);  // was 1.03 without setting also the size
  h1->GetYaxis()->SetTitleSize(0.05);
  //h1->GetYaxis()->SetRangeUser(0.0, max(h1->GetMaximum(),h2->GetMaximum()) * 1.2);
  h1->GetYaxis()->SetRangeUser(0.0, max(h1->GetBinContent(h1->GetMaximumBin()),h2->GetBinContent(h2->GetMaximumBin())) * 1.2);
  if (setXAxisRangeFromUser) h1->GetXaxis()->SetRangeUser(xmin,xmax);
  h1->Draw("EP");

  h2->SetLineColor(kRed);
  h2->SetLineWidth(2);
  h2->Draw("hist same");

  TLegend leg (0.5,0.7,0.9,0.9);
  leg.SetFillColor(0);
  leg.SetFillStyle(0);
  leg.SetBorderSize(0);
  leg.AddEntry(h1,legEntry1.c_str(),"PLE");
  leg.AddEntry(h2,legEntry2.c_str(),"L");
  leg.Draw("same");
  canvas->RedrawAxis("sameaxis");

  TPaveText *pvtxt = NULL;
  if (yAxisName == "a.u.") {
    pvtxt = new TPaveText(0.5,0.6,0.90,0.7, "BR NDC");
    pvtxt->SetFillColor(0);
    pvtxt->SetFillStyle(0);
    pvtxt->SetBorderSize(0);
    pvtxt->AddText(Form("norm num/den = %.2f +/- %.2f",IntegralRatio,ratioError));
    pvtxt->Draw();
  }

  //  CMS_lumi(canvas,Form("%.1f",lumi));
  if (lumi < 0) CMS_lumi(canvas,"",false,false);
  else CMS_lumi(canvas,Form("%.1f",lumi),false,false);
  setTDRStyle();

  pad2->Draw();
  pad2->cd();

  frame->Reset("ICES");
  frame->GetYaxis()->SetRangeUser(0.5,1.5);
  frame->GetYaxis()->SetNdivisions(5);
  frame->GetYaxis()->SetTitle(ratioPadYaxisName.c_str());
  frame->GetYaxis()->SetTitleOffset(1.2);
  // frame->GetYaxis()->SetTitleSize(0.15);
  frame->GetYaxis()->CenterTitle();
  frame->GetXaxis()->SetTitle(xAxisName.c_str());
  if (setXAxisRangeFromUser) frame->GetXaxis()->SetRangeUser(xmin,xmax);
  // frame->GetXaxis()->SetTitleOffset(0.8);
  frame->GetXaxis()->SetTitleSize(0.05);

  TH1D* ratio = (TH1D*) h1->Clone("ratio");
  TH1D* den_noerr = (TH1D*) h2->Clone("den_noerr");
  TH1D* den = (TH1D*) h2->Clone("den");
  for(int iBin = 1; iBin < den->GetNbinsX()+1; iBin++)
    den_noerr->SetBinError(iBin,0.);

  ratio->Divide(den_noerr);
  den->Divide(den_noerr);
  den->SetFillColor(kGray);
  frame->Draw();
  ratio->SetMarkerSize(0.85);
  ratio->Draw("EPsame");
  den->Draw("E2same");

  TF1* line = new TF1("horiz_line","1",ratio->GetXaxis()->GetBinLowEdge(1),ratio->GetXaxis()->GetBinLowEdge(ratio->GetNbinsX()+1));
  line->SetLineColor(kRed);
  line->SetLineWidth(2);
  line->Draw("Lsame");
  ratio->Draw("EPsame");
  pad2->RedrawAxis("sameaxis");

  // Calculate chi2                                                                                        
  double chi2 = h1->Chi2Test(h2,"CHI2/NDF WW");
  TLegend leg2 (0.14,0.25,0.32,0.28,NULL,"brNDC");
  leg2.SetFillColor(0);
  leg2.SetFillStyle(1);
  leg2.SetBorderSize(0);
  leg2.SetLineColor(0);
  leg2.AddEntry((TObject*)0,Form("#chi^{2}/ndf = %.2f",chi2),"");
  leg2.Draw("same");

  canvas->SaveAs((outputDIR + canvasName + ".png").c_str());
  canvas->SaveAs((outputDIR + canvasName + ".pdf").c_str());

  if (drawPlotLogY) {

    if (yAxisName == "a.u.") h1->GetYaxis()->SetRangeUser(max(0.0001,min(h1->GetMinimum(),h2->GetMinimum())*0.8),max(h1->GetMaximum(),h2->GetMaximum())*100);
    else h1->GetYaxis()->SetRangeUser(max(0.001,min(h1->GetMinimum(),h2->GetMinimum())*0.8),max(h1->GetMaximum(),h2->GetMaximum())*100);
    canvas->SetLogy();
    /* if (lumi < 0) CMS_lumi(canvas,"",true,false); */
    /* else CMS_lumi(canvas,Form("%.1f",lumi),true,false); */
    canvas->SaveAs((outputDIR + canvasName + "_logY.png").c_str());
    canvas->SaveAs((outputDIR + canvasName + "_logY.pdf").c_str());
    canvas->SetLogy(0);

  }    

  delete canvas;

}


//=============================================================

void draw_nTH1(vector<TH1*> vecHist1d = {}, 
	       const string& xAxisNameTmp = "", 
	       const string& yAxisName = "Events", 
	       const string& canvasName = "default", 
	       const string& outputDIR = "./", 
	       const vector<string>& vecLegEntry = {""},
	       const string& ratioPadYaxisName = "var/nominal",
	       const Double_t lumi = -1.0, 
	       const Int_t rebinFactor = 1, 
	       const Bool_t drawPlotLogY = true,
	       const Bool_t drawRatioWithNominal = false  // to be implemented
	       ) 
{

  // assume the "nominal histogram is the first one

  TH1::SetDefaultSumw2(); //all the following histograms will automatically call TH1::Sumw2() 

  string xAxisName = "";
  Double_t xmin = 0;
  Double_t xmax = 0;
  Bool_t setXAxisRangeFromUser = getAxisRangeFromUser(xAxisName, xmin, xmax, xAxisNameTmp);

  // cout << "xAxisName = " << xAxisName << "   xmin = " << xmin << "  xmax = " << xmax << endl;

  for (UInt_t i = 0; i < vecHist1d.size(); i++) {
    myRebinHisto(vecHist1d[i],rebinFactor);
    if (yAxisName == "a.u.") vecHist1d[i]->Scale(1./vecHist1d[i]->Integral());
    vecHist1d[i]->SetStats(0);
  }


  TCanvas* canvas = new TCanvas("canvas","",600,700);
  canvas->cd();
  canvas->SetTickx(1);
  canvas->SetTicky(1);
  canvas->cd();
  if (drawRatioWithNominal) canvas->SetBottomMargin(0.3);
  canvas->SetRightMargin(0.06);

  TPad *pad2 = new TPad("pad2","pad2",0,0.,1,0.9);
  pad2->SetTopMargin(0.7);
  pad2->SetRightMargin(0.06);
  pad2->SetFillColor(0);
  pad2->SetGridy(1);
  pad2->SetFillStyle(0);

  TH1* frame =  (TH1*) vecHist1d[0]->Clone("frame");
  frame->GetXaxis()->SetLabelSize(0.04);
  frame->SetStats(0);

  Int_t colorList[] = {kBlack, kBlue, kRed, kGreen+2, kOrange+1, kCyan, kGreen, kCyan+2, kGray+1, kViolet, kYellow+2};
  vector<Int_t> histColor;
  for (UInt_t i = 0; i < vecHist1d.size(); i++) {   // now color are assigned in reverse order (the main contribution is the last object in the sample array)         
    vecHist1d[i]->SetLineColor(colorList[i]);
    vecHist1d[i]->SetLineWidth(2);
    vecHist1d[i]->SetFillColor(0);
  }

  if (drawRatioWithNominal) {
    vecHist1d[0]->GetXaxis()->SetLabelSize(0);
    vecHist1d[0]->GetXaxis()->SetTitle(0);
  } else {
    vecHist1d[0]->GetXaxis()->SetTitle(xAxisName.c_str());
    // vecHist1d[0]->GetXaxis()->SetTitleOffset(0.8);
    vecHist1d[0]->GetXaxis()->SetLabelSize(0.04);
    vecHist1d[0]->GetXaxis()->SetTitleSize(0.05);    
  }
  vecHist1d[0]->GetYaxis()->SetTitle(yAxisName.c_str());
  vecHist1d[0]->GetYaxis()->SetTitleOffset(1.1);
  // vecHist1d[0]->GetYaxis()->SetTitleOffset(0.8);  // was 1.03 without setting also the size
  vecHist1d[0]->GetYaxis()->SetTitleSize(0.05);
  //vecHist1d[0]->GetYaxis()->SetRangeUser(0.0, max(vecHist1d[0]->GetMaximum(),h2->GetMaximum()) * 1.2);

  //////////////////////////////
  // set X and Y axis range

  // search for maximum Y and for minimum > 0 (latter only if using log scale for Y axis
  Double_t maxY = -999.0;
  for (UInt_t i = 0; i < vecHist1d.size(); i++) {
    if ( vecHist1d[i]->GetBinContent(vecHist1d[i]->GetMaximumBin()) > maxY ) maxY = vecHist1d[i]->GetBinContent(vecHist1d[i]->GetMaximumBin());
  }

  Double_t minY = 1e34;

  if (drawPlotLogY) {

    // quick check if there are no empty bins
    for (UInt_t i = 0; i < vecHist1d.size(); i++) {
      if ( vecHist1d[i]->GetBinContent(vecHist1d[i]->GetMinimumBin()) < minY ) minY = vecHist1d[i]->GetBinContent(vecHist1d[i]->GetMinimumBin());
    }

    if (fabs(minY) < 0.00000001) {

      minY = 1e34;
      
      for (UInt_t ihist = 0; ihist < vecHist1d.size(); ihist++) {

	for (Int_t ibin = 0; ibin <= vecHist1d[ihist]->GetNbinsX(); ibin++ ) {
	  if (vecHist1d[ihist]->GetBinContent(ibin) > 0.0000001 && minY > vecHist1d[ihist]->GetBinContent(ibin)) minY = vecHist1d[ihist]->GetBinContent(ibin);
	}      
      
      }

    }

  }

  vecHist1d[0]->GetYaxis()->SetRangeUser(0.0, maxY * 1.2);

  if (setXAxisRangeFromUser) vecHist1d[0]->GetXaxis()->SetRangeUser(xmin,xmax);
  //////////////////////

  vecHist1d[0]->Draw("Hist");
  vecHist1d[0]->SetFillColor(0);
  vecHist1d[0]->SetMarkerStyle(0);
  for (UInt_t i = 1; i < vecHist1d.size(); i++) {
    vecHist1d[i]->Draw("hist same");
  }

  double legLowY = 0.75;
  if (vecHist1d.size() > 4) legLowY = max( 0.5, legLowY - 0.4 * (vecHist1d.size() - 4) );
  TLegend leg (0.58,0.70,0.95,0.9);
  leg.SetFillColor(0);
  leg.SetFillStyle(0);
  leg.SetBorderSize(0);
  for (UInt_t i = 0; i < vecHist1d.size(); i++) {
    leg.AddEntry(vecHist1d[i],vecLegEntry[i].c_str(),"L");
  }
  leg.Draw("same");
  canvas->RedrawAxis("sameaxis");

  //  CMS_lumi(canvas,Form("%.1f",lumi));
  bool cmsPreliminaryIsUp = false;
  if (yAxisName == "a.u.") cmsPreliminaryIsUp = true;
  if (canvasName.find("pi0mass_comparison_E") != string::npos) cmsPreliminaryIsUp = false;

  if (lumi < 0) CMS_lumi(canvas,"",cmsPreliminaryIsUp,false);
  else CMS_lumi(canvas,Form("%.1f",lumi),cmsPreliminaryIsUp,false);
  setTDRStyle();

  if (drawRatioWithNominal) {
    pad2->Draw();
    pad2->cd();
  
    frame->Reset("ICES");
    if (canvasName.find("comparisonMassVariation") != string::npos) {
      frame->GetYaxis()->SetRangeUser(0.99, 1.01);
      /* if      (outputDIR.find("/eta_0/") != string::npos) frame->GetYaxis()->SetRangeUser(0.99, 1.01); */
      /* else if (outputDIR.find("/eta_1/") != string::npos) frame->GetYaxis()->SetRangeUser(0.98, 1.02); */
      /* else if (outputDIR.find("/eta_2/") != string::npos) frame->GetYaxis()->SetRangeUser(0.98, 1.02); */
    } else if (canvasName.find("elescale") != string::npos) {
      frame->GetYaxis()->SetRangeUser(0.99,1.01);
    } else if (canvasName.find("elescale") != string::npos) {
      frame->GetYaxis()->SetRangeUser(0.99,1.01);
    } else frame->GetYaxis()->SetRangeUser(0.9,1.1);
    frame->GetYaxis()->SetNdivisions(5);
    frame->GetYaxis()->SetTitle(ratioPadYaxisName.c_str());
    frame->GetYaxis()->SetTitleOffset(1.2);
    // frame->GetYaxis()->SetTitleSize(0.15);
    frame->GetYaxis()->CenterTitle();
    frame->GetXaxis()->SetTitle(xAxisName.c_str());
    if (setXAxisRangeFromUser) frame->GetXaxis()->SetRangeUser(xmin,xmax);
    // frame->GetXaxis()->SetTitleOffset(0.8);
    frame->GetXaxis()->SetTitleSize(0.05);

    vector<TH1D*> ratio;
    for (UInt_t ivar = 1; ivar < vecHist1d.size(); ivar++) 
      ratio.push_back( (TH1D*) vecHist1d[ivar]->Clone(Form("ratio_%d",ivar)) );

    TH1D* den_noerr = (TH1D*) vecHist1d[0]->Clone("den_noerr");
    TH1D* den = (TH1D*) vecHist1d[0]->Clone("den");
    for(int iBin = 1; iBin < den->GetNbinsX()+1; iBin++)
      den_noerr->SetBinError(iBin,0.);

    den->Divide(den_noerr);
    den->SetFillColor(kGray);
    frame->Draw();
    den->Draw("E2same");
    for (UInt_t ir = 0; ir < ratio.size(); ir++) {
      ratio[ir]->Divide(den_noerr);
      // ratio[ir]->SetMarkerSize(0.65);
      // ratio[ir]->Draw("EPsame");
      ratio[ir]->SetMarkerStyle(0);
      ratio[ir]->SetLineWidth(2);
      ratio[ir]->Draw("Hist same");
    }
 

    TF1* line = new TF1("horiz_line","1",den->GetXaxis()->GetBinLowEdge(1),den->GetXaxis()->GetBinLowEdge(den->GetNbinsX()+1));
    line->SetLineColor(kBlack);
    line->SetLineWidth(2);
    line->Draw("Lsame");
    // for (UInt_t ir = 0; ir < ratio.size(); ir++)
    //   ratio[ir]->Draw("EPsame");
    pad2->RedrawAxis("sameaxis");

  }  // end of ratio plot settings

  if (canvasName.find("tmpToBeRemoved") == string::npos) { 
    canvas->SaveAs((outputDIR + canvasName + ".png").c_str());
    canvas->SaveAs((outputDIR + canvasName + ".pdf").c_str());
  }

  if (drawPlotLogY) {

    if (yAxisName == "a.u.") vecHist1d[0]->GetYaxis()->SetRangeUser(minY*0.05, maxY*100);
    else vecHist1d[0]->GetYaxis()->SetRangeUser(minY*0.05, maxY*100);
    canvas->SetLogy();
    /* if (lumi < 0) CMS_lumi(canvas,"",true,false); */
    /* else CMS_lumi(canvas,Form("%.1f",lumi),true,false); */
    if (canvasName.find("tmpToBeRemoved") == string::npos) { 
      canvas->SaveAs((outputDIR + canvasName + "_logY.png").c_str());
      canvas->SaveAs((outputDIR + canvasName + "_logY.pdf").c_str());
    }
    canvas->SetLogy(0);

  }    

  delete canvas;

}



//=============================================================

void drawTH1dataMCstack(TH1* h1 = NULL, vector<TH1*> vecMC = {}, 
			const string& xAxisNameTmp = "", const string& yAxisName = "Events", const string& canvasName = "default", 
			const string& outputDIR = "./", 
			const string& legEntry1 = "data", const vector<string>& vecLegEntryMC = {""}, 
			const string& ratioPadYaxisName = "data/MC", const Double_t lumi = -1.0, const Int_t rebinFactor = 1, 
			const Bool_t normalizeMCToData = false,
			const Int_t draw_both0_noLog1_onlyLog2 = 0
			)
{

  string xAxisName = "";
  Double_t xmin = 0;
  Double_t xmax = 0;
  Bool_t setXAxisRangeFromUser = getAxisRangeFromUser(xAxisName, xmin, xmax, xAxisNameTmp);

  // cout << "xAxisName = " << xAxisName << "   xmin = " << xmin << "  xmax = " << xmax << endl;

  TH1::SetDefaultSumw2(); //all the following histograms will automatically call TH1::Sumw2() 

  if (vecMC.size() != vecLegEntryMC.size()) {
    cout << "Error: legend has different number of entries than stack elements, please check. Exit" << endl;
    exit(EXIT_FAILURE);
  }

  for (UInt_t i = 0; i < vecMC.size(); i++) {
    vecMC[i]->SetStats(0);
  }
  
  Int_t colorList[] = {kCyan, kViolet, kBlue, kRed, kYellow, kGreen, kOrange+1, kCyan+2, kGreen+2, kGray}; 
  // the first color is for the main object. This array may contain more values than vecMC.size()
  vector<Int_t> histColor;
  for (UInt_t i = 0; i < vecMC.size(); i++) {   // now color are assigned in reverse order (the main contribution is the last object in the sample array)
    histColor.push_back(colorList[i]);
  }

  Double_t dataNorm = h1->Integral();
  Double_t stackNorm = 0.0; 

  if (normalizeMCToData) {
    for (UInt_t ibin = 0; ibin < vecMC.size(); ibin++) {
      stackNorm += vecMC[ibin]->Integral();
    }
  }

  THStack* hMCstack = new THStack("hMCstack","");
  for (UInt_t j = 0; j < vecMC.size(); j++) {
    vecMC[j]->SetFillColor(histColor[j]);
    vecMC[j]->SetFillStyle(3001);
    myRebinHisto(vecMC[j],rebinFactor);
    if (normalizeMCToData) vecMC[j]->Scale(dataNorm/stackNorm);
    hMCstack->Add(vecMC[(UInt_t) vecMC.size() - j -1]);  // add last element as the first one (last element added in stack goes on top)
  }
  TH1D* stackCopy = (TH1D*) hMCstack->GetStack()->Last(); // used to make ratioplot without affecting the plot and setting maximum

  if (h1 == NULL) h1 = (TH1D*) stackCopy->Clone("pseudoData");
  else myRebinHisto(h1,rebinFactor);

  h1->SetStats(0);

  TCanvas* canvas = new TCanvas("canvas","",600,700);
  canvas->cd();
  canvas->SetTickx(1);
  canvas->SetTicky(1);
  canvas->cd();
  canvas->SetBottomMargin(0.3);
  canvas->SetRightMargin(0.06);

  TPad *pad2 = new TPad("pad2","pad2",0,0.,1,0.9);
  pad2->SetTopMargin(0.7);
  pad2->SetRightMargin(0.06);
  pad2->SetFillColor(0);
  pad2->SetGridy(1);
  pad2->SetFillStyle(0);


  TH1* frame =  (TH1*) h1->Clone("frame");
  frame->GetXaxis()->SetLabelSize(0.04);
  frame->SetStats(0);

  h1->SetLineColor(kBlack);
  h1->SetMarkerColor(kBlack);
  h1->SetMarkerStyle(20);
  h1->SetMarkerSize(1);

  h1->GetXaxis()->SetLabelSize(0);
  h1->GetYaxis()->SetTitle(yAxisName.c_str());
  h1->GetYaxis()->SetTitleOffset(1.1);
  // h1->GetYaxis()->SetTitleOffset(0.8);  // was 1.03 without setting also the size
  h1->GetYaxis()->SetTitleSize(0.05);
  h1->GetYaxis()->SetRangeUser(0.0, max(h1->GetMaximum(),stackCopy->GetMaximum()) * 1.2);
  if (setXAxisRangeFromUser) h1->GetXaxis()->SetRangeUser(xmin,xmax);
  h1->Draw("EP");
  hMCstack->Draw("HIST SAME");
  h1->Draw("EP SAME");

  TLegend leg (0.6,0.7,0.9,0.9);
  leg.SetFillColor(0);
  leg.SetFillStyle(0);
  leg.SetBorderSize(0);
  leg.AddEntry(h1,legEntry1.c_str(),"PLE");
  for (UInt_t i = 0; i < vecMC.size(); i++) {
    leg.AddEntry(vecMC[i],vecLegEntryMC[i].c_str(),"LF");
  }
  leg.Draw("same");
  canvas->RedrawAxis("sameaxis");

  //  CMS_lumi(canvas,Form("%.1f",lumi));
  if (lumi < 0) CMS_lumi(canvas,"",false,false);
  else CMS_lumi(canvas,Form("%.1f",lumi),false,false);
  setTDRStyle();

  pad2->Draw();
  pad2->cd();

  frame->Reset("ICES");
  frame->GetYaxis()->SetRangeUser(0.5,1.5);
  frame->GetYaxis()->SetNdivisions(5);
  frame->GetYaxis()->SetTitle(ratioPadYaxisName.c_str());
  frame->GetYaxis()->SetTitleOffset(1.2);
  // frame->GetYaxis()->SetTitleSize(0.15);
  frame->GetYaxis()->CenterTitle();
  if (setXAxisRangeFromUser) frame->GetXaxis()->SetRangeUser(xmin,xmax);
  frame->GetXaxis()->SetTitle(xAxisName.c_str());
  // frame->GetXaxis()->SetTitleOffset(0.8);
  frame->GetXaxis()->SetTitleSize(0.05);

  TH1D* ratio = (TH1D*) h1->Clone("ratio");
  TH1D* den_noerr = (TH1D*) stackCopy->Clone("den_noerr");
  TH1D* den = (TH1D*) stackCopy->Clone("den");
  for(int iBin = 1; iBin < den->GetNbinsX()+1; iBin++)
    den_noerr->SetBinError(iBin,0.);

  ratio->Divide(den_noerr);
  den->Divide(den_noerr);
  den->SetFillColor(kGray);
  frame->Draw();
  ratio->SetMarkerSize(0.85);
  ratio->Draw("EPsame");
  den->Draw("E2same");

  TF1* line = new TF1("horiz_line","1",ratio->GetXaxis()->GetBinLowEdge(1),ratio->GetXaxis()->GetBinLowEdge(ratio->GetNbinsX()+1));
  line->SetLineColor(kRed);
  line->SetLineWidth(2);
  line->Draw("Lsame");
  ratio->Draw("EPsame");
  pad2->RedrawAxis("sameaxis");

  // Calculate chi2                                                                                        
  double chi2 = h1->Chi2Test(stackCopy,"CHI2/NDF WW");
  TLegend leg2 (0.14,0.25,0.32,0.28,NULL,"brNDC");
  leg2.SetFillColor(0);
  leg2.SetFillStyle(1);
  leg2.SetBorderSize(0);
  leg2.SetLineColor(0);
  leg2.AddEntry((TObject*)0,Form("#chi^{2}/ndf = %.2f",chi2),"");
  leg2.Draw("same");

  if (draw_both0_noLog1_onlyLog2 != 2) {
    canvas->SaveAs((outputDIR + canvasName + ".png").c_str());
    canvas->SaveAs((outputDIR + canvasName + ".pdf").c_str());
  }

  /* Double_t minY_log = max(0.001, min(h1->GetBinContent(h1->GetMinimumBin()),stackCopy->GetBinContent(stackCopy->GetMinimumBin())) ) * 0.01; */
  /* if ( fabs(minY_log) < 0.00001) minY_log = 0.001;  // avoid zero */
  /* h1->GetYaxis()->SetRangeUser(minY_log * 0.8, max(h1->GetMaximum(),stackCopy->GetMaximum())*100); */
  //Double_t minY_log = max(0.001,min(h1->GetMinimum(),stackCopy->GetMinimum())*0.8);
  //if (min(h1->GetBinContent(h1->GetMinimumBin()),stackCopy->GetBinContent(stackCopy->GetMinimumBin()) > 0) minY_log = 0.5;

  /* Double_t minY_log = -1.0; */
  /* TH1D* lowerStackObject = (TH1D*) hMCstack->GetStack()->First(); // */

  if (draw_both0_noLog1_onlyLog2 != 1) {

    Double_t minY_log = 1e20;
    TH1D* lowerStackObject = (TH1D*) hMCstack->GetStack()->First();
    /* if (lowerStackObject->GetBinContent(stackCopy->GetMinimumBin()) > 0.000001 ) { */
    /*   // if no empty bin in stack */
    /*   minY_log = 0.05 * lowerStackObject->GetBinContent(lowerStackObject->GetMinimumBin()); */
    /* } else { */
    /*   minY_log = 0.01 * stackCopy->GetBinContent(stackCopy->GetMinimumBin()); */
    /* } */

    for (Int_t ibin = 0; ibin <= lowerStackObject->GetNbinsX(); ibin++ ) {
      if (lowerStackObject->GetBinContent(ibin) > 0.0000001 && minY_log > lowerStackObject->GetBinContent(ibin)) minY_log = lowerStackObject->GetBinContent(ibin);
    }

    if (minY_log < 0.000001) minY_log = 0.1;
    minY_log = 0.05 * minY_log;

    h1->GetYaxis()->SetRangeUser(minY_log,max(h1->GetMaximum(),stackCopy->GetMaximum())*100);
    canvas->SetLogy();
    pad2->RedrawAxis("sameaxis");
    /* if (lumi < 0) CMS_lumi(canvas,"",true,false); */
    /* else CMS_lumi(canvas,Form("%.1f",lumi),true,false); */
    canvas->SaveAs((outputDIR + canvasName + "_logY.png").c_str());
    canvas->SaveAs((outputDIR + canvasName + "_logY.pdf").c_str());
    canvas->SetLogy(0);
  }

  delete canvas;

}


//=============================================================

/* // following function calls the previous one that is more general and takes a vector of TH1* as "data" */
/* // it would be used to have a stack and more than one not stacked histogram  */
/* // ratio is made using only first non stacked object, but the others are used for the ratio */
/* void drawTH1dataMCstack(TH1* h1 = NULL, vector<TH1*> vecMC = {},  */
/* 			const string& xAxisNameTmp = "", const string& yAxisName = "Events", const string& canvasName = "default",  */
/* 			const string& outputDIR = "./",  */
/* 			const string& legEntry1 = "data", const vector<string>& vecLegEntryMC = {""},  */
/* 			const string& ratioPadYaxisName = "data/MC", const Double_t lumi = -1.0, const Int_t rebinFactor = 1,  */
/* 			const Bool_t normalizeMCToData = false, */
/* 			const Int_t draw_both0_noLog1_onlyLog2 = 0 */
/* 			) */
/* { */

/*   vector<TH1*> vecNostack;  */
/*   vecNostack.push_back(h1); */

/*   vector<string> vecLegEntryNostack; */
/*   vecLegEntryNostack.push_back(legEntry1); */

/*   drawMoreTH1andMCstack(vecNostack, vecMC, xAxisNameTmp, yAxisName, canvasName, outputDIR, vecLegEntryNostack, vecLegEntryMC, ratioPadYaxisName, lumi, rebinFactor, normalizeMCToData, ) */

/* } */

// function to draw data and MC and other not stacked objects
void drawTH1dataMCstackAndNoStack(TH1* h1 = NULL, vector<TH1*> vecMC = {}, vector<TH1*> vecMCnostack = {},
				  const string& xAxisNameTmp = "", const string& yAxisName = "Events", const string& canvasName = "default", 
				  const string& outputDIR = "./", 
				  const string& legEntry1 = "data", const vector<string>& vecLegEntryMC = {""}, const vector<string>& vecLegEntryMCnostack = {""}, 
				  const string& ratioPadYaxisNameTmp = "data/MC", const Double_t lumi = -1.0, const Int_t rebinFactor = 1, 
				  const Bool_t normalizeMCToData = false, // normalize MC stack and non stacked object individually
				  const Int_t draw_both0_noLog1_onlyLog2 = 0,
				  const string& denForRatio = "stack" // stack, TH1nostack
				  )
{

  // select what to use as denominator in ratio plot
  // nostack use first TH1 not stacked

  string xAxisName = "";
  Double_t xmin = 0;
  Double_t xmax = 0;
  Bool_t setXAxisRangeFromUser = getAxisRangeFromUser(xAxisName, xmin, xmax, xAxisNameTmp);

  string ratioPadYaxisName = "";
  Double_t yminRatio = 0;
  Double_t ymaxRatio = 0;
  Bool_t setRatioYAxisRangeFromUser = getAxisRangeFromUser(ratioPadYaxisName, yminRatio, ymaxRatio, ratioPadYaxisNameTmp);

  // cout << "xAxisName = " << xAxisName << "   xmin = " << xmin << "  xmax = " << xmax << endl;

  TH1::SetDefaultSumw2(); //all the following histograms will automatically call TH1::Sumw2() 

  if (vecMC.size() != vecLegEntryMC.size()) {
    cout << "Error: stack legend has different number of entries than stack elements, please check. Exit" << endl;
    exit(EXIT_FAILURE);
  }
  if (vecMCnostack.size() != vecLegEntryMCnostack.size()) {
    cout << "Error: non-stack legend has different number of entries than non-stack elements, please check. Exit" << endl;
    exit(EXIT_FAILURE);
  }


  for (UInt_t i = 0; i < vecMC.size(); i++) {
    vecMC[i]->SetStats(0);
  }  
  for (UInt_t i = 0; i < vecMCnostack.size(); i++) {
    vecMCnostack[i]->SetStats(0);
  }

  Int_t colorList[] = {kCyan, kViolet, kBlue, kRed, kYellow, kGreen, kOrange+1, kCyan+2, kGreen+2, kGray}; 
  // the first color is for the main object. This array may contain more values than vecMC.size()
  vector<Int_t> histColor;
  for (UInt_t i = 0; i < vecMC.size(); i++) {   
    histColor.push_back(colorList[i]);
  }

  vector<Int_t> histColorNostack = { kRed+2, kBlue+2, kGreen+2, kGray+2, kMagenta+2, kCyan+1, kOrange+1};

  Double_t dataNorm = h1->Integral();
  Double_t stackNorm = 0.0; 

  if (normalizeMCToData) {
    for (UInt_t ibin = 0; ibin < vecMC.size(); ibin++) {
      stackNorm += vecMC[ibin]->Integral();
    }
    for (UInt_t ibin = 0; ibin < vecMCnostack.size(); ibin++) {
      vecMCnostack[ibin]->Scale(dataNorm/vecMCnostack[ibin]->Integral());
    }
  }

  THStack* hMCstack = new THStack("hMCstack","");
  for (UInt_t j = 0; j < vecMC.size(); j++) {
    vecMC[j]->SetFillColor(histColor[j]);
    vecMC[j]->SetFillStyle(3001);
    myRebinHisto(vecMC[j],rebinFactor);
    if (normalizeMCToData) vecMC[j]->Scale(dataNorm/stackNorm);
    hMCstack->Add(vecMC[(UInt_t) vecMC.size() - j -1]);  // add last element as the first one (last element added in stack goes on top)
    vecMC[j]->GetXaxis()->SetTitle("");

  }
  for (UInt_t j = 0; j < vecMCnostack.size(); j++) {
    vecMCnostack[j]->SetLineColor(histColorNostack[j]);
    vecMCnostack[j]->SetFillColor(0);
    vecMCnostack[j]->SetLineWidth(3);
    vecMCnostack[j]->SetMarkerStyle(0);
    myRebinHisto(vecMCnostack[j],rebinFactor);
  }

  TH1D* stackCopy = (TH1D*) hMCstack->GetStack()->Last(); // used to make ratioplot without affecting the plot and setting maximum

  if (h1 == NULL) h1 = (TH1D*) stackCopy->Clone("pseudoData");
  else myRebinHisto(h1,rebinFactor);

  h1->SetStats(0);

  TCanvas* canvas = new TCanvas("canvas","",600,700);
  canvas->cd();
  canvas->SetTickx(1);
  canvas->SetTicky(1);
  canvas->cd();
  canvas->SetBottomMargin(0.3);
  canvas->SetRightMargin(0.06);
  canvas->SetLeftMargin(0.13);

  TPad *pad2 = new TPad("pad2","pad2",0,0.,1,0.9);
  pad2->SetTopMargin(0.7);
  pad2->SetLeftMargin(0.13);
  pad2->SetRightMargin(0.06);
  pad2->SetFillColor(0);
  pad2->SetGridy(1);
  pad2->SetFillStyle(0);


  TH1* frame =  (TH1*) h1->Clone("frame");
  frame->GetXaxis()->SetLabelSize(0.04);
  frame->SetStats(0);

  h1->SetLineColor(kBlack);
  h1->SetMarkerColor(kBlack);
  h1->SetMarkerStyle(20);
  h1->SetMarkerSize(1);

  h1->GetXaxis()->SetLabelSize(0);
  h1->GetXaxis()->SetTitle(0);
  h1->GetYaxis()->SetTitle(yAxisName.c_str());
  h1->GetYaxis()->SetTitleOffset(1.3);
  // h1->GetYaxis()->SetTitleOffset(0.8);  // was 1.03 without setting also the size
  h1->GetYaxis()->SetTitleSize(0.05);  
  h1->GetYaxis()->SetLabelSize(0.04);
  h1->GetYaxis()->SetRangeUser(0.0, max(h1->GetMaximum(),stackCopy->GetMaximum()) * 1.2);
  if (setXAxisRangeFromUser) h1->GetXaxis()->SetRangeUser(xmin,xmax);
  h1->Draw("EP");
  hMCstack->Draw("HIST SAME");
  TH1D* noStackCopy = NULL;
  for (UInt_t j = 0; j < vecMCnostack.size(); j++) {
    /* TH1D* noStackCopy = (TH1D*) vecMCnostack[j]->DrawCopy("hist same"); */
    /* vecMCnostack[j]->SetFillColor(vecMCnostack[j]->GetLineColor()); */
    /* vecMCnostack[j]->SetFillStyle(3013); */
    /* vecMCnostack[j]->Draw("E2 SAME"); */
    if (vecMCnostack.size() == 1) {
      noStackCopy = (TH1D*) vecMCnostack[j]->Clone(Form("%s_clone",vecMCnostack[j]->GetName()));
      noStackCopy->SetFillColor(vecMCnostack[j]->GetLineColor());
      noStackCopy->SetFillStyle(3013);
      noStackCopy->Draw("E2 SAME");
    }
    vecMCnostack[j]->Draw("HIST SAME");
    vecMCnostack[j]->GetXaxis()->SetTitle("");
  }
  h1->Draw("EP SAME");

  Double_t legLowY = 0.7;
  if ((vecMC.size() + vecMCnostack.size()) > 5) legLowY = legLowY - 0.03 * (vecMC.size() + vecMCnostack.size() - 5); 
  TLegend leg (0.6,legLowY,0.9,0.9);
  leg.SetFillColor(0);
  leg.SetFillStyle(0);
  leg.SetBorderSize(0);
  leg.AddEntry(h1,legEntry1.c_str(),"PLE");
  for (UInt_t i = 0; i < vecMC.size(); i++) {
    leg.AddEntry(vecMC[i],vecLegEntryMC[i].c_str(),"LF");
  }
  for (UInt_t i = 0; i < vecMCnostack.size(); i++) {
    if (vecMCnostack.size() == 1) leg.AddEntry(noStackCopy,vecLegEntryMCnostack[i].c_str(),"LF");
    else leg.AddEntry(vecMCnostack[i],vecLegEntryMCnostack[i].c_str(),"L");
  }
  leg.Draw("same");
  canvas->RedrawAxis("sameaxis");

  //  CMS_lumi(canvas,Form("%.1f",lumi));
  if (lumi < 0) CMS_lumi(canvas,"",false,false);
  else CMS_lumi(canvas,Form("%.1f",lumi),false,false);
  setTDRStyle();

  pad2->Draw();
  pad2->cd();

  frame->Reset("ICES");
  if (setRatioYAxisRangeFromUser) frame->GetYaxis()->SetRangeUser(yminRatio,ymaxRatio);
  else frame->GetYaxis()->SetRangeUser(0.5,1.5);
  frame->GetYaxis()->SetNdivisions(5);
  frame->GetYaxis()->SetTitle(ratioPadYaxisName.c_str());
  frame->GetYaxis()->SetTitleOffset(1.2);
  frame->GetYaxis()->SetTitleSize(0.04); // needed when using histograms in file produced with mcPlots.py 
  frame->GetYaxis()->SetLabelSize(0.04); // needed when using histograms in file produced with mcPlots.py 
  frame->GetYaxis()->CenterTitle();
  if (setXAxisRangeFromUser) frame->GetXaxis()->SetRangeUser(xmin,xmax);
  frame->GetXaxis()->SetTitle(xAxisName.c_str());
  // frame->GetXaxis()->SetTitleOffset(0.8);
  frame->GetXaxis()->SetTitleSize(0.05); 

  TH1D* ratio = NULL;
  vector<TH1D*> ratio_noStack;
  TH1D* den_noerr = NULL;
  TH1D* den = NULL;
  if (denForRatio == "stack") {
    ratio = (TH1D*) h1->Clone("ratio");
    den_noerr = (TH1D*) stackCopy->Clone("den_noerr");
    den = (TH1D*) stackCopy->Clone("den");
  } else if (denForRatio == "nostack") {
    ratio = (TH1D*) h1->Clone("ratio");
    den_noerr = (TH1D*) vecMCnostack[0]->Clone("den_noerr");
    den = (TH1D*) vecMCnostack[0]->Clone("den");
  } else if (denForRatio == "data") {
    ratio = (TH1D*) stackCopy->Clone();
    for (UInt_t i = 0; i < vecMCnostack.size(); i++) 
      ratio_noStack.push_back( (TH1D*) vecMCnostack[i]->Clone());
    den_noerr = (TH1D*) h1->Clone("den_noerr");
    den = (TH1D*) h1->Clone("den");
  }

  for(int iBin = 1; iBin < den->GetNbinsX()+1; iBin++)
    den_noerr->SetBinError(iBin,0.);

  ratio->Divide(den_noerr);
  if (denForRatio == "data") {
    ratio->SetMarkerStyle(22); // triangle, use 22 for filled marker
    ratio->SetMarkerSize(1.1); // triangle, use 22 for filled marker
    ratio->SetMarkerColor(kBlue);
  } else {
    ratio->SetMarkerSize(0.85);
  }
  den->Divide(den_noerr);
  den->SetFillColor(kGray);
  frame->Draw();
  den->SetMarkerStyle(0);
  den->Draw("E2same");
  ratio->Draw("EPsame");
  for (UInt_t i = 0; i < ratio_noStack.size(); i++) {
    ratio_noStack[i]->Divide(den_noerr);
    ratio_noStack[i]->SetMarkerSize(0.85);
    //ratio_noStack[i]->SetMarkerColor();
    ratio_noStack[i]->Draw("EPsame");
  }

  TF1* line = new TF1("horiz_line","1",ratio->GetXaxis()->GetBinLowEdge(1),ratio->GetXaxis()->GetBinLowEdge(ratio->GetNbinsX()+1));
  line->SetLineColor(kRed);
  line->SetLineWidth(2);
  line->Draw("Lsame");
  ratio->Draw("EPsame");
  pad2->RedrawAxis("sameaxis");

  TLegend leg2 (0.14,0.24,0.32,0.29,NULL,"brNDC");
  leg2.SetFillColor(0);
  leg2.SetFillStyle(1);
  leg2.SetBorderSize(0);
  leg2.SetLineColor(0);
  if (denForRatio == "data") leg2.AddEntry(ratio,"stack","PLE");
  leg2.Draw("same");

  // Calculate chi2                                                                                        
  /* double chi2 = h1->Chi2Test(stackCopy,"CHI2/NDF WW"); */
  /* TLegend leg2 (0.14,0.25,0.32,0.28,NULL,"brNDC"); */
  /* leg2.SetFillColor(0); */
  /* leg2.SetFillStyle(1); */
  /* leg2.SetBorderSize(0); */
  /* leg2.SetLineColor(0); */
  /* leg2.AddEntry((TObject*)0,Form("#chi^{2}/ndf = %.2f",chi2),""); */
  /* leg2.Draw("same"); */

  if (draw_both0_noLog1_onlyLog2 != 2) {
    canvas->SaveAs((outputDIR + canvasName + ".png").c_str());
    canvas->SaveAs((outputDIR + canvasName + ".pdf").c_str());
  }

  /* Double_t minY_log = max(0.001, min(h1->GetBinContent(h1->GetMinimumBin()),stackCopy->GetBinContent(stackCopy->GetMinimumBin())) ) * 0.01; */
  /* if ( fabs(minY_log) < 0.00001) minY_log = 0.001;  // avoid zero */
  /* h1->GetYaxis()->SetRangeUser(minY_log * 0.8, max(h1->GetMaximum(),stackCopy->GetMaximum())*100); */
  //Double_t minY_log = max(0.001,min(h1->GetMinimum(),stackCopy->GetMinimum())*0.8);
  //if (min(h1->GetBinContent(h1->GetMinimumBin()),stackCopy->GetBinContent(stackCopy->GetMinimumBin()) > 0) minY_log = 0.5;

  /* Double_t minY_log = -1.0; */
  /* TH1D* lowerStackObject = (TH1D*) hMCstack->GetStack()->First(); // */

  if (draw_both0_noLog1_onlyLog2 != 1) {

    Double_t minY_log = 1e20;
    TH1D* lowerStackObject = (TH1D*) hMCstack->GetStack()->First();
    /* if (lowerStackObject->GetBinContent(stackCopy->GetMinimumBin()) > 0.000001 ) { */
    /*   // if no empty bin in stack */
    /*   minY_log = 0.05 * lowerStackObject->GetBinContent(lowerStackObject->GetMinimumBin()); */
    /* } else { */
    /*   minY_log = 0.01 * stackCopy->GetBinContent(stackCopy->GetMinimumBin()); */
    /* } */

    for (Int_t ibin = 0; ibin <= lowerStackObject->GetNbinsX(); ibin++ ) {
      if (lowerStackObject->GetBinContent(ibin) > 0.0000001 && minY_log > lowerStackObject->GetBinContent(ibin)) minY_log = lowerStackObject->GetBinContent(ibin);
    }

    if (minY_log < 0.000001) minY_log = 0.1;
    minY_log = 0.05 * minY_log;

    h1->GetYaxis()->SetRangeUser(minY_log,max(h1->GetMaximum(),stackCopy->GetMaximum())*100);
    canvas->SetLogy();
    pad2->RedrawAxis("sameaxis");
    /* if (lumi < 0) CMS_lumi(canvas,"",true,false); */
    /* else CMS_lumi(canvas,Form("%.1f",lumi),true,false); */
    canvas->SaveAs((outputDIR + canvasName + "_logY.png").c_str());
    canvas->SaveAs((outputDIR + canvasName + "_logY.pdf").c_str());
    canvas->SetLogy(0);
  }

  delete canvas;

}


//=============================================================


TFitResultPtr drawTH1(TH1* h1 = NULL, 
		      const string& xAxisNameTmp = "", const string& yAxisName = "Events", const string& canvasName = "default", 
		      const string& outputDIR = "./", 
		      const string& legEntryTmp = "", 
		      const Double_t lumi = -1.0, 
		      const Int_t rebinFactor = 1,
		      const Bool_t noStatBox = false,
		      const Bool_t saveCanvas = true
		      )
{

  string xAxisName = "";
  Double_t xmin = 0;
  Double_t xmax = 0;
  Bool_t setXAxisRangeFromUser = getAxisRangeFromUser(xAxisName, xmin, xmax, xAxisNameTmp);

  string legEntry = "";
  string legHeader = "";
  Bool_t setLegendHeader = false;

  string separator = "::";
  size_t pos = legEntryTmp.find(separator);
  if (pos != string::npos) {
    setLegendHeader = true;
    legEntry.assign(legEntryTmp, 0, pos); 
    legHeader.assign(legEntryTmp, pos + separator.size(), string::npos);
  } else {
    legEntry = legEntryTmp;
  }


  // cout << "xAxisName = " << xAxisName << "   xmin = " << xmin << "  xmax = " << xmax << endl;

  TH1::SetDefaultSumw2(); //all the following histograms will automatically call TH1::Sumw2() 

  myRebinHisto(h1,rebinFactor);
  
  TCanvas* canvas = new TCanvas("canvas","",700,700);
  canvas->cd();
  canvas->SetTickx(1);
  canvas->SetTicky(1);
  canvas->cd();
  canvas->SetBottomMargin(0.12);
  canvas->SetRightMargin(0.06);

  h1->Draw("HE");
  //Double_t histNorm = h1->Integral(0, h1->GetNbinsX()+1);
  Double_t histNorm = h1->GetBinContent(h1->GetMaximumBin()); // cout << "histNorm = " << histNorm << endl;
  Double_t histMean = h1->GetMean();   //  cout << "histMean = " << histMean << endl;
  Double_t histStdDev = h1->GetStdDev(); //  cout << "histStdDev = " << histStdDev << endl;
  /* TF1 *gaussian = new TF1("gaussian","gaus",histMean-4*histStdDev, histMean+4*histStdDev); */
  /* gaussian->SetParLimits(0, 0.95 * histNorm, 1.05 * histNorm); */
  /* gaussian->SetParLimits(1, histMean - histStdDev, histMean + histStdDev); */
  /* gaussian->SetParLimits(2, 0.1 * histStdDev, 2.0 * histStdDev); */
  /* gaussian->SetParameter(0, histNorm); */
  /* gaussian->SetParameter(1, histMean); */
  /* gaussian->SetParameter(2, histStdDev); */
  /* gaussian->SetLineColor(kRed); */
  /* gaussian->SetLineWidth(2); */
  //gaussian->Draw("SAME");

  TF1*cb1 = new TF1("cb1",&my2sideCrystalBall,histMean-4*histStdDev, histMean+4*histStdDev,7);
  cb1->SetParNames("alphaL","nL","Mean(fit)","Sigma","Const","alphaR","nR");
  cb1->SetParLimits(cb1->GetParNumber("nL"),0.1,15);
  cb1->SetParLimits(cb1->GetParNumber("Mean(fit)"), histMean - histStdDev, histMean + histStdDev);
  cb1->SetParLimits(cb1->GetParNumber("Sigma"),0.1 * histStdDev, 1.1 * histStdDev);
  cb1->SetParLimits(cb1->GetParNumber("nR"),0.1,15);
  cb1->SetParLimits(cb1->GetParNumber("alphaL"),-5.0,-0.1);
  cb1->SetParLimits(cb1->GetParNumber("alphaR"),0.1,5.0);
  cb1->SetParLimits(cb1->GetParNumber("Const"),0.8*histNorm,1.2*histNorm);
  cb1->SetParameters(-1.4,5,histMean,histStdDev,histNorm,1.4,5);
  cb1->SetLineColor(kGreen+2);
  cb1->SetLineWidth(2);

  //TFitResultPtr frp1 = h1->Fit(gaussian,"E L I S Q B R","HE", histMean - 1.4 * histStdDev, histMean + 1.4 * histStdDev);
  /* TF1 *fitFunction = h1->GetFunction("gaussian"); */
  /* if (fitFunction) { */
  /*   fitFunction->SetLineColor(kRed); */
  /*   fitFunction->SetLineWidth(2); */
  /*   fitFunction->Draw("SAME"); */
  /* } */
  TFitResultPtr frp2 = h1->Fit(cb1,"E WL I S Q B R","HE SAMES", histMean - 3.0 * histStdDev, histMean + 3.0 * histStdDev);
  //cout << "checkpoint" << endl; return 0;
  if (frp2->Parameter(cb1->GetParNumber("Sigma")) < 0.0 ) {
    cout << "WARNING: CB sigma is negative!" << endl;
  }

  TF1 *gaussCore = new TF1(*(h1->GetFunction("cb1")));
  if (gaussCore) {
    Double_t gaussMean = frp2->Parameter(cb1->GetParNumber("Mean(fit)"));
    Double_t gaussSigma = frp2->Parameter(cb1->GetParNumber("Sigma"));
    Double_t alphaL = frp2->Parameter(cb1->GetParNumber("alphaL"));
    Double_t alphaR = frp2->Parameter(cb1->GetParNumber("alphaR"));
    gaussCore->DrawF1(gaussMean + fabs(gaussSigma) * -fabs(alphaL), gaussMean + fabs(gaussSigma) * fabs(alphaR),"SAME"); // alphaL < 0, alphaR > 0
    gaussCore->SetLineColor(kRed);
    gaussCore->SetLineWidth(2);
  }
  /* gaussian->SetParLimits(0, 0.95 * histNorm, 1.05 * histNorm); */
  /* gaussian->SetParLimits(1, histMean - histStdDev, histMean + histStdDev); */
  /* gaussian->SetParLimits(2, 0.1 * histStdDev, 2.0 * histStdDev); */
  /* gaussian->SetParameter(0, histNorm); */
  /* gaussian->SetParameter(1, histMean); */
  /* gaussian->SetParameter(2, histStdDev); */
  /* gaussian->SetLineColor(kRed); */
  /* gaussian->SetLineWidth(2); */
  //gaussian->Draw("SAME");


  canvas->Update();
  TPaveStats *statBox = (TPaveStats*)(h1->FindObject("stats"));
  if (statBox) {
    statBox->SetX1NDC(0.62);
    statBox->SetX2NDC(0.92);
    statBox->SetY1NDC(0.59);
    statBox->SetY2NDC(0.91);
    statBox->SetFillColor(0);
    statBox->SetFillStyle(0);
    statBox->SetBorderSize(0);
    statBox->Draw();
  }
  canvas->Update();

  if (setXAxisRangeFromUser) h1->GetXaxis()->SetRangeUser(xmin,xmax);
  h1->GetXaxis()->SetTitle(xAxisName.c_str());
  // h1->GetXaxis()->SetTitleOffset(0.8);
  h1->GetXaxis()->SetTitleSize(0.05);
  h1->GetYaxis()->SetTitle(yAxisName.c_str());
  h1->GetYaxis()->SetTitleOffset(1.1);
  // h1->GetYaxis()->SetTitleOffset(0.8);  // was 1.03 without setting also the size
  h1->GetYaxis()->SetTitleSize(0.05);
  h1->GetYaxis()->SetRangeUser(0.0, h1->GetMaximum() * 1.5);
  canvas->RedrawAxis("sameaxis");
  canvas->Update();

  TLegend leg (0.15,0.7,0.6,0.9);
  if (setLegendHeader) leg.SetHeader(legHeader.c_str());
  leg.SetFillColor(0);
  leg.SetFillStyle(0);
  leg.SetBorderSize(0);
  leg.AddEntry(h1,legEntry.c_str(),"L");
  //leg.AddEntry(gaussian,"gauss","l");
  if (gaussCore) leg.AddEntry(gaussCore,"gauss core","l");
  leg.AddEntry(cb1,"CB","l");
  leg.Draw("same");
  canvas->RedrawAxis("sameaxis");

  //  CMS_lumi(canvas,Form("%.1f",lumi));
  if (lumi < 0) CMS_lumi(canvas,"",true,false);
  else CMS_lumi(canvas,Form("%.1f",lumi),true,false);
  setTDRStyle();

  
  if (noStatBox) {
    h1->SetStats(0);
    //cout << "No Statistics box" << endl;
  } else {
    //canvas->Update();
    gPad->Update();
    gStyle->SetOptStat(1110);
    gStyle->SetOptFit(1102);
  }
  //h1->SetStats(0);

  if (saveCanvas) {
    canvas->SaveAs((outputDIR + canvasName + ".png").c_str());
    canvas->SaveAs((outputDIR + canvasName + ".pdf").c_str());
  }

  delete canvas;
  return frp2;

}


//=============================================================

void drawTH1MCstack(vector<TH1*> vecMC = {}, 
		    const string& xAxisNameTmp = "", const string& yAxisName = "Events", const string& canvasName = "default", 
		    const string& outputDIR = "./", 
		    const vector<string>& vecLegEntryMC = {""}, 
		    const Double_t lumi = -1.0, const Int_t rebinFactor = 1,
		    const Int_t draw_both0_noLog1_onlyLog2 = 0		    
		    )
{

  string xAxisName = "";
  Double_t xmin = 0;
  Double_t xmax = 0;
  Bool_t setXAxisRangeFromUser = getAxisRangeFromUser(xAxisName, xmin, xmax, xAxisNameTmp);

  // cout << "xAxisName = " << xAxisName << "   xmin = " << xmin << "  xmax = " << xmax << endl;

  TH1::SetDefaultSumw2(); //all the following histograms will automatically call TH1::Sumw2() 

  if (vecMC.size() != vecLegEntryMC.size()) {
    cout << "Error: legend has different number of entries than stack elements, please check. Exit" << endl;
    exit(EXIT_FAILURE);
  }

  for (UInt_t i = 0; i < vecMC.size(); i++) {
    vecMC[i]->SetStats(0);
  }
  
  Int_t colorList[] = {kCyan, kViolet, kBlue, kRed, kYellow, kGreen, kOrange+1, kCyan+2, kGreen+2, kGray}; 
  // the first color is for the main object. This array may contain more values than vecMC.size()
  vector<Int_t> histColor;
  for (UInt_t i = 0; i < vecMC.size(); i++) {  
    histColor.push_back(colorList[i]);
  }

  Double_t stackNorm = 0.0; 

  THStack* hMCstack = new THStack("hMCstack","");
  for (UInt_t j = 0; j < vecMC.size(); j++) {
    vecMC[j]->SetFillColor(histColor[j]);
    vecMC[j]->SetFillStyle(3001);
    myRebinHisto(vecMC[j],rebinFactor);
    hMCstack->Add(vecMC[(UInt_t) vecMC.size() - j -1]);  // add last element as the first one (last element added in stack goes on top)
  }
  TH1D* stackCopy = (TH1D*) hMCstack->GetStack()->Last(); // used to make ratioplot without affecting the plot and setting maximum

  TCanvas* canvas = new TCanvas("canvas","",700,700);
  canvas->cd();
  canvas->SetTickx(1);
  canvas->SetTicky(1);
  canvas->cd();
  canvas->SetBottomMargin(0.1);
  canvas->SetRightMargin(0.06);

  stackCopy->Draw("HIST");
  hMCstack->Draw("HIST SAME");

  //TH1* stackCopy = hMCstack->GetHistogram();

  if (setXAxisRangeFromUser) stackCopy->GetXaxis()->SetRangeUser(xmin,xmax);
  stackCopy->GetXaxis()->SetTitle(xAxisName.c_str());
  // stackCopy->GetXaxis()->SetTitleOffset(0.8);
  stackCopy->GetXaxis()->SetTitleSize(0.05);
  stackCopy->GetYaxis()->SetTitle(yAxisName.c_str());
  stackCopy->GetYaxis()->SetTitleOffset(1.1);
  // stackCopy->GetYaxis()->SetTitleOffset(0.8);  // was 1.03 without setting also the size
  stackCopy->GetYaxis()->SetTitleSize(0.05);
  stackCopy->GetYaxis()->SetRangeUser(0.0, stackCopy->GetMaximum() * 1.5);
  canvas->RedrawAxis("sameaxis");
  canvas->Update();

  TLegend leg (0.6,0.7,0.9,0.9);
  leg.SetFillColor(0);
  leg.SetFillStyle(0);
  leg.SetBorderSize(0);
  for (UInt_t i = 0; i < vecMC.size(); i++) {
    leg.AddEntry(vecMC[i],vecLegEntryMC[i].c_str(),"LF");
  }
  leg.Draw("same");
  canvas->RedrawAxis("sameaxis");

  //  CMS_lumi(canvas,Form("%.1f",lumi));
  if (lumi < 0) CMS_lumi(canvas,"",false,false);
  else CMS_lumi(canvas,Form("%.1f",lumi),false,false);
  setTDRStyle();

  if (draw_both0_noLog1_onlyLog2 != 2) {
    canvas->SaveAs((outputDIR + canvasName + ".png").c_str());
    canvas->SaveAs((outputDIR + canvasName + ".pdf").c_str());
  }

  if (draw_both0_noLog1_onlyLog2 != 1) {

    Double_t minY_log = 1e10;
    TH1D* lowerStackObject = (TH1D*) hMCstack->GetStack()->First();
    
    for (Int_t ibin = 0; ibin <= lowerStackObject->GetNbinsX(); ibin++ ) {
      if (lowerStackObject->GetBinContent(ibin) > 0.0000001 && minY_log > lowerStackObject->GetBinContent(ibin)) minY_log = lowerStackObject->GetBinContent(ibin);
    }
    
    if (minY_log < 0.000001) minY_log = 0.1;
    minY_log = 0.05 * minY_log;
    
    stackCopy->GetYaxis()->SetRangeUser(minY_log,stackCopy->GetMaximum()*100);
    canvas->SetLogy();
    canvas->RedrawAxis("sameaxis");
    canvas->SaveAs((outputDIR + canvasName + "_logY.png").c_str());
    //canvas->SaveAs((outputDIR + canvasName + "_logY.pdf").c_str());
    canvas->SetLogy(0);
  }

  delete canvas;

}


//=============================================================



void drawCorrelationPlot(TH2* h2D, 
			 const string & labelXtmp = "xaxis", const string & labelYtmp = "yaxis", const string & labelZ = "zaxis",  
			 const string& canvasName = "default", const string& plotLabel = "", const string & outputDIR = "./", 
			 const Int_t rebinFactorY = 1,
			 const Int_t rebinFactorX = 1,
			 const bool smoothPlot = true,
			 const bool drawProfileX = true,
			 const bool scaleToUnitArea = true,
			 const Int_t draw_both0_noLog1_onlyLog2 = 0)
{

  if (rebinFactorY > 1) h2D->RebinY(rebinFactorY);
  if (rebinFactorX > 1) h2D->RebinX(rebinFactorX);

  string labelX = "";
  Double_t xmin = 0;
  Double_t xmax = 0;
  Bool_t setXAxisRangeFromUser = getAxisRangeFromUser(labelX, xmin, xmax, labelXtmp);
  
  string labelY = "";
  Double_t ymin = 0;
  Double_t ymax = 0;
  Bool_t setYAxisRangeFromUser = getAxisRangeFromUser(labelY, ymin, ymax, labelYtmp);

  TCanvas* canvas = new TCanvas("canvas","",700,625);
  canvas->SetLeftMargin(0.16);
  canvas->SetRightMargin(0.20);
  canvas->cd();

  system(("mkdir -p "+outputDIR).c_str());
  // normalize to 1
  if (scaleToUnitArea) h2D->Scale(1./h2D->Integral());

  TGraph2D* h2DGraph = NULL;

  TH2* h2DPlot = NULL;
  if (not smoothPlot) h2DPlot = h2D;
  else {
    h2DGraph = new TGraph2D();
    h2DGraph->SetNpx(300);
    h2DGraph->SetNpy(300);
    int nPoint = 0;
    for(int iBinX = 0; iBinX < h2D->GetNbinsX() ; iBinX++){
      for(int iBinY = 0; iBinY < h2D->GetNbinsY() ; iBinY++){
        h2DGraph->SetPoint(nPoint,h2D->GetXaxis()->GetBinCenter(iBinX+1),h2D->GetYaxis()->GetBinCenter(iBinY+1),h2D->GetBinContent(iBinX+1,iBinY+1));
        nPoint++;
      }
    }
    h2DPlot = h2DGraph->GetHistogram();
  }
  
  h2DPlot->GetXaxis()->SetTitle(labelX.c_str());
  h2DPlot->GetYaxis()->SetTitle(labelY.c_str());
  if (scaleToUnitArea) h2DPlot->GetZaxis()->SetTitle("a.u");   
  else h2DPlot->GetZaxis()->SetTitle(labelZ.c_str());
  h2DPlot->Draw("colz");
  if (setXAxisRangeFromUser) h2DPlot->GetXaxis()->SetRangeUser(xmin,xmax);
  if (setYAxisRangeFromUser) h2DPlot->GetYaxis()->SetRangeUser(ymin,ymax);

  TProfile* h2DProfile = NULL;
  if (drawProfileX) {
    h2DProfile = h2D->ProfileX(Form("%s_pfx",h2D->GetName()));
    h2DProfile->SetMarkerColor(kBlack);
    h2DProfile->SetMarkerStyle(20);
    h2DProfile->SetMarkerSize(1);
    h2DProfile->Draw("EPsame");
  }

  CMS_lumi(canvas,"",true,false);
  setTDRStyle();

  TLegend leg(0.39,0.75,0.89,0.95);
  leg.SetFillStyle(0);
  leg.SetFillColor(0);
  leg.SetBorderSize(0);
  leg.SetTextFont(62);
  if (plotLabel != "") leg.AddEntry((TObject*)0,plotLabel.c_str(),"");
  if (drawProfileX) leg.AddEntry((TObject*)0,Form("Correlation = %.2f",h2DPlot->GetCorrelationFactor()),"");
  leg.Draw("same");

  if (draw_both0_noLog1_onlyLog2 == 0 || draw_both0_noLog1_onlyLog2 == 1) {
    canvas->SaveAs((outputDIR + canvasName + ".png").c_str(),"png");
    canvas->SaveAs((outputDIR + canvasName + ".pdf").c_str(),"pdf");
  }
  if (draw_both0_noLog1_onlyLog2 == 0 || draw_both0_noLog1_onlyLog2 == 2) {
    canvas->SetLogz();
    canvas->SaveAs((outputDIR + canvasName + "_logZ.png").c_str(),"png");
    canvas->SaveAs((outputDIR + canvasName + "_logZ.pdf").c_str(),"pdf");
    canvas->SetLogz(0);
  }

  delete canvas;

}



//======================================================


/* void buildChain(TChain* chain,  TChain* chFriend, const string& treePath = "", const Sample& sample = Sample::data_doubleEG) { */
  
/*   cout << "Creating chain ..." << endl; */
  
/*   vector<string> subSampleNameVector; */

/*   if (sample == Sample::wjets) { */
/*     subSampleNameVector.push_back("WJetsToLNu_reHLT"); */
/*   } else if (sample == Sample::zjets) { */
/*     subSampleNameVector.push_back("DYJetsToLL_M50_reHLT"); */
/*   } else if (sample == Sample::data_doubleEG) { */
/*     subSampleNameVector.push_back("DoubleEG_Run2016B_23Sep2016_v3_runs_273150_275376"); */
/*     subSampleNameVector.push_back("DoubleEG_Run2016C_23Sep2016_v1_runs_271036_284044"); */
/*     subSampleNameVector.push_back("DoubleEG_Run2016D_23Sep2016_v1_runs_271036_284044"); */
/*     subSampleNameVector.push_back("DoubleEG_Run2016E_23Sep2016_v1_runs_271036_284044"); */
/*     subSampleNameVector.push_back("DoubleEG_Run2016F_23Sep2016_v1_runs_271036_284044"); */
/*     subSampleNameVector.push_back("DoubleEG_Run2016G_23Sep2016_v1_runs_271036_284044"); */
/*     subSampleNameVector.push_back("DoubleEG_Run2016H_PromptReco_v1_runs_281085_281201"); */
/*     subSampleNameVector.push_back("DoubleEG_Run2016H_PromptReco_v2_runs_281207_284035"); */
/*     subSampleNameVector.push_back("DoubleEG_Run2016H_PromptReco_v3_runs_284036_284044");  */
/*   } else if (sample == Sample::qcd_mu) { */
/*     subSampleNameVector.push_back("QCD_Pt120to170_Mu5"); */
/*     subSampleNameVector.push_back("QCD_Pt15to20_Mu5"); */
/*     subSampleNameVector.push_back("QCD_Pt1000toInf_Mu5"); */
/*     subSampleNameVector.push_back("QCD_Pt20to30_Mu5"); */
/*     subSampleNameVector.push_back("QCD_Pt300to470_Mu5"); */
/*     //subSampleNameVector.push_back("QCD_Pt300to470_Mu5_ext"); */
/*     subSampleNameVector.push_back("QCD_Pt30to50_Mu5"); */
/*     subSampleNameVector.push_back("QCD_Pt470to600_Mu5"); */
/*     //subSampleNameVector.push_back("QCD_Pt470to600_Mu5_ext"); */
/*     subSampleNameVector.push_back("QCD_Pt170to300_Mu5"); */
/*     subSampleNameVector.push_back("QCD_Pt50to80_Mu5"); */
/*     subSampleNameVector.push_back("QCD_Pt600to800_Mu5"); */
/*     //subSampleNameVector.push_back("QCD_Pt600to800_Mu5_ext"); */
/*     subSampleNameVector.push_back("QCD_Pt800to1000_Mu5"); */
/*     //subSampleNameVector.push_back("QCD_Pt800to1000_Mu5_ext"); */
/*     subSampleNameVector.push_back("QCD_Pt80to120_Mu5"); */
/*   } else if (sample == Sample::qcd_ele) { */
/*     subSampleNameVector.push_back("QCD_Pt20to30_EMEnriched"); */
/*     subSampleNameVector.push_back("QCD_Pt30to50_EMEnriched"); */
/*     subSampleNameVector.push_back("QCD_Pt50to80_EMEnriched"); */
/*     subSampleNameVector.push_back("QCD_Pt80to120_EMEnriched"); */
/*     subSampleNameVector.push_back("QCD_Pt120to170_EMEnriched"); */
/*     subSampleNameVector.push_back("QCD_Pt170to300_EMEnriched"); */
/*     subSampleNameVector.push_back("QCD_Pt300toInf_EMEnriched"); */
/*     subSampleNameVector.push_back("QCD_Pt_30to80_bcToE"); */
/*     subSampleNameVector.push_back("QCD_Pt_170to250_bcToE"); */
/*     subSampleNameVector.push_back("QCD_Pt_250toInf_bcToE"); */
/*   } else { */
/*     cout << "#### Error in buildChain() function: sample name not available, please check. Exit ..." << endl; */
/*     exit(EXIT_FAILURE); */
/*   } */

  
/*   for(UInt_t i = 0; i < subSampleNameVector.size(); i++) { */
  
/*     string treeRootFile = treePath + subSampleNameVector[i] + "/treeProducerDarkMatterMonoJet/tree.root"; */
/*     string friend_treeRootFile = treePath + "friends/evVarFriend_" + subSampleNameVector[i]+ ".root"; */
/*     chain->Add(TString(treeRootFile.c_str())); */
/*     chFriend->Add(TString(friend_treeRootFile.c_str())); */

/*   } */

/*   if(!chain ) { */
/*     cout << "#### Error in buildChain() function: chain not created. End of programme" << endl; */
/*     exit(EXIT_FAILURE); */
/*   } */

/*   if(!chFriend ) { */
/*     cout << "#### Error in buildChain() function: chFriend not created. End of programme" << endl; */
/*     exit(EXIT_FAILURE); */
/*   } */

/*   cout << "Adding friend to chain ..." << endl; */
/*   chain->AddFriend(chFriend);  //adding whole friend chain as friend                                                                                                         */

/*   cout << "entries in chain    = " << chain->   GetEntries() << endl; */
/*   cout << "entries in chFriend = " << chFriend->GetEntries() << endl; */

/*   if (chain->GetEntries() != chFriend->GetEntries()) { */
/*     cout << "#### Error in buildChain() function: chain and chFriend have different number of events. End of programme" << endl; */
/*     exit(EXIT_FAILURE); */
/*   } */

/* } */

//===========================================================

Double_t getXsecOverNgen(const string& sample) {
  
  // xsec in pb
  map<string, Double_t> events_ntot;
  map<string, Double_t> cross_section;

  ////////////////////
  // ZJets
  ////////////////////
  events_ntot["DYJetsM50"] = 30429578;
  cross_section["DYJetsM50"] = 3503.7;

  ////////////////////
  //WJets
  ////////////////////
  events_ntot["WJets"] = 57093619;
  cross_section["WJets"] = 37509.0;

  ////////////////////
  // top
  ////////////////////
  events_ntot["TTJets"] = 6923750;
  cross_section["TTJets"] = 245.59;

  events_ntot["Tsch"] = 259961;
  cross_section["Tsch"] = 3.79;

  events_ntot["Tbarsch"] = 139974;
  cross_section["Tbarsch"] = 1.76;

  events_ntot["Ttch"] = 3753227;
  cross_section["Ttch"] = 56.4;

  events_ntot["Tbartch"] = 1935072;
  cross_section["Tbartch"] = 30.7;

  events_ntot["TtW"] = 497658;
  cross_section["TtW"] = 11.73;

  events_ntot["TbartW"] = 493460;
  cross_section["TbartW"] = 11.73;

  ////////////////////
  // diboson
  ////////////////////
  events_ntot["WWJets"] = 1898738;
  cross_section["WWJets"] = 5.995;

  events_ntot["WZJets"] = 2007120;
  cross_section["WZJets"] = 1.057 * 1.10;

  ////////////////////
  //QCD mu enriched
  ////////////////////
  events_ntot["QCDMuPt15"] = 21328956;
  cross_section["QCDMuPt15"] = 134680; // 364000000 * 0.00037 * 0.6 // without 0.6 factor it is 134680, otherwise it is 80808
  // 0.00037 is the filter efficiency, error on efficiency is 0.000038
  // 0.6 is an hardcoded value that should make QCD MC normalization be consistent with data
 

 // return xsec in fb
  if (sample.find("data") != string::npos) return 1.0;
  else                                     return cross_section[sample] * 1000.0/ events_ntot[sample] ;

}

//=========================================================

Double_t getXsec8TeV(const string& sample) {
  
  // xsec in pb
  map<string, Double_t> cross_section;

  ////////////////////
  // ZJets
  ////////////////////
  cross_section["DYJetsM50"] = 3503.7;

  ////////////////////
  //WJets
  ////////////////////
  cross_section["WJets"] = 37509.0;

  ////////////////////
  // top
  ////////////////////
  cross_section["TTJets"] = 245.59;
  cross_section["Tsch"] = 3.79;
  cross_section["Tbarsch"] = 1.76;
  cross_section["Ttch"] = 56.4;
  cross_section["Tbartch"] = 30.7;
  cross_section["TtW"] = 11.73;
  cross_section["TbartW"] = 11.73;

  ////////////////////
  // diboson
  ////////////////////
  cross_section["WWJets"] = 5.81;
  cross_section["WZJets"] = 1.057 * 1.10;

  ////////////////////
  //QCD mu enriched
  ////////////////////
  cross_section["QCDMuPt15"] = 134680; // 364000000 * 0.00037 * 0.6 // without 0.6 factor it is 134680, otherwise it is 80808
  // 0.00037 is the filter efficiency, error on efficiency is 0.000038
  // 0.6 is an hardcoded value that should make QCD MC normalization be consistent with data
 

 // return xsec in fb
  if (sample.find("data") != string::npos || sample.find("fake") != string::npos)
    return 1.0;
  else
    return cross_section[sample] * 1000.0 ;  // return xsec in fb

}


//=========================================================

Double_t getXsec13TeV(const string& sample) {
  
  // xsec in pb
  map<string, Double_t> cross_section;

  ////////////////////
  // ZJets
  ////////////////////
  cross_section["DYJetsM50"] = 3.0 * 2008.0;

  ////////////////////
  //WJets
  ////////////////////
  cross_section["WJets"] = 3.0 * 20508.9;

  ////////////////////
  // top
  ////////////////////
  cross_section["TBar_tWch"] = 35.6;
  cross_section["TTJets_SingleLeptonFromT"] = 831.76*(3*0.108)*(1-3*0.108);
  cross_section["TTJets_SingleLeptonFromTbar"] = 831.76*(3*0.108)*(1-3*0.108);
  cross_section["TToLeptons_sch"] = (7.20+4.16)*0.108*3;
  cross_section["TToLeptons_tch_amcatnlo"] = (136.05+80.97)*0.108*3;
  cross_section["T_tWch"] = 35.6;

  ////////////////////
  // diboson5B
  ////////////////////
  cross_section["WWJets"] = 63.21 * 1.82;
  cross_section["WZJets"] = 47.13;
  cross_section["ZZJets"] = 16.523;

  ////////////////////
  //QCD mu enriched
  ////////////////////
  cross_section["QCD_Mu15"] = 720.65e6*0.00042;
  cross_section["QCD_Pt1000toInf_Mu5"] = 10.4305*0.15544;
  cross_section["QCD_Pt120to170_Mu5"] = 469797*0.05362;
  cross_section["QCD_Pt15to20_Mu5"] = 1273190000*0.003;
  cross_section["QCD_Pt170to300_Mu5"] = 117989*0.07335;
  cross_section["QCD_Pt20to30_Mu5"] = 558528000*0.0053;
  cross_section["QCD_Pt300to470_Mu5_ext"] = 7820.25*0.10196;
  cross_section["QCD_Pt300to470_Mu5"] = 7820.25*0.10196;
  cross_section["QCD_Pt30to50_Mu5"] = 139803000*0.01182;
  cross_section["QCD_Pt470to600_Mu5_ext"] = 645.528*0.12242;
  cross_section["QCD_Pt470to600_Mu5"] = 645.528*0.12242;
  cross_section["QCD_Pt50to80_Mu5"] = 19222500*0.02276;
  cross_section["QCD_Pt600to800_Mu5_ext"] = 187.109*0.13412;
  cross_section["QCD_Pt600to800_Mu5"] = 187.109*0.13412;
  cross_section["QCD_Pt800to1000_Mu5_ext"] = 32.3486*0.14552;
  cross_section["QCD_Pt800to1000_Mu5"] = 32.3486*0.14552;
  cross_section["QCD_Pt80to120_Mu5"] = 2758420*0.03844;

  ////////////////////
  //QCD ele enriched
  ////////////////////
  cross_section["QCD_Pt120to170_EMEnriched"] = 477000*0.132;
  cross_section["QCD_Pt170to300_EMEnriched"] = 114000*0.165;
  cross_section["QCD_Pt20to30_EMEnriched"] = 557600000*0.0096;
  cross_section["QCD_Pt300toInf_EMEnriched"] = 9000*0.15;
  cross_section["QCD_Pt30to50_EMEnriched"] = 136000000*0.073;
  cross_section["QCD_Pt50to80_EMEnriched"] = 19800000*0.146;
  cross_section["QCD_Pt80to120_EMEnriched"] = 2800000*0.125;
  cross_section["QCD_Pt_170to250_bcToE"] = 105771*0.02492;
  cross_section["QCD_Pt_250toInf_bcToE"] = 21094.1*0.03375;
  cross_section["QCD_Pt_30to80_bcToE"] = 159068000*0.00255;

 // return xsec in fb
  if (sample.find("data") != string::npos || sample.find("fake") != string::npos) 
    return 1.0;
  else
    return cross_section[sample] * 1000.0 ;  // return xsec in fb

}

//=========================================================

Double_t getSumGenWeightFromSampleName(const string& sample) {
  
  // xsec in pb
  map<string, Double_t> map_sampleName_sumGenWgt;

  // map created with script getSumWeightPerSample.py
  map_sampleName_sumGenWgt["DYJetsToLL_M50_LO_ext2_part1"] = 142209392.0;
  map_sampleName_sumGenWgt["DYJetsToLL_M50_LO_ext2_part10"] = 142209392.0;
  map_sampleName_sumGenWgt["DYJetsToLL_M50_LO_ext2_part11"] = 142209392.0;
  map_sampleName_sumGenWgt["DYJetsToLL_M50_LO_ext2_part2"] = 142209392.0;
  map_sampleName_sumGenWgt["DYJetsToLL_M50_LO_ext2_part3"] = 142209392.0;
  map_sampleName_sumGenWgt["DYJetsToLL_M50_LO_ext2_part4"] = 142209392.0;
  map_sampleName_sumGenWgt["DYJetsToLL_M50_LO_ext2_part5"] = 142209392.0;
  map_sampleName_sumGenWgt["DYJetsToLL_M50_LO_ext2_part6"] = 142209392.0;
  map_sampleName_sumGenWgt["DYJetsToLL_M50_LO_ext2_part7"] = 142209392.0;
  map_sampleName_sumGenWgt["DYJetsToLL_M50_LO_ext2_part8"] = 142209392.0;
  map_sampleName_sumGenWgt["DYJetsToLL_M50_LO_ext2_part9"] = 142209392.0;
  map_sampleName_sumGenWgt["DYJetsToLL_M50_LO_ext_part1"] = 142209392.0;
  map_sampleName_sumGenWgt["DYJetsToLL_M50_LO_ext_part2"] = 142209392.0;
  map_sampleName_sumGenWgt["DYJetsToLL_M50_LO_ext_part3"] = 142209392.0;
  map_sampleName_sumGenWgt["DYJetsToLL_M50_LO_ext_part4"] = 142209392.0;
  map_sampleName_sumGenWgt["DYJetsToLL_M50_LO_ext_part5"] = 142209392.0;
  map_sampleName_sumGenWgt["DYJetsToLL_M50_LO_ext_part6"] = 142209392.0;
  map_sampleName_sumGenWgt["DYJetsToLL_M50_part1"] = 4.4113015039e+11;
  map_sampleName_sumGenWgt["DYJetsToLL_M50_part2"] = 4.4113015039e+11;
  map_sampleName_sumGenWgt["QCD_Mu15_part1"] = 12260254.0;
  map_sampleName_sumGenWgt["QCD_Mu15_part2"] = 12260254.0;
  map_sampleName_sumGenWgt["QCD_Pt1000toInf_Mu5"] = 126748460.747;
  map_sampleName_sumGenWgt["QCD_Pt120to170_Mu5"] = 126748460.747;
  map_sampleName_sumGenWgt["QCD_Pt15to20_Mu5"] = 126748460.747;
  map_sampleName_sumGenWgt["QCD_Pt170to300_Mu5"] = 126748460.747;
  map_sampleName_sumGenWgt["QCD_Pt170to300_Mu5_ext"] = 126748460.747;
  map_sampleName_sumGenWgt["QCD_Pt20to30_EMEnriched"] = 38966443.5421;
  map_sampleName_sumGenWgt["QCD_Pt20to30_Mu5"] = 126748460.747;
  map_sampleName_sumGenWgt["QCD_Pt300to470_Mu5"] = 126748460.747;
  map_sampleName_sumGenWgt["QCD_Pt300to470_Mu5_ext"] = 126748460.747;
  map_sampleName_sumGenWgt["QCD_Pt300to470_Mu5_ext2"] = 126748460.747;
  map_sampleName_sumGenWgt["QCD_Pt30to50_EMEnriched"] = 38966443.5421;
  map_sampleName_sumGenWgt["QCD_Pt30to50_EMEnriched_ext"] = 38966443.5421;
  map_sampleName_sumGenWgt["QCD_Pt30to50_Mu5"] = 126748460.747;
  map_sampleName_sumGenWgt["QCD_Pt470to600_Mu5_ext"] = 126748460.747;
  map_sampleName_sumGenWgt["QCD_Pt50to80_EMEnriched_ext"] = 38966443.5421;
  map_sampleName_sumGenWgt["QCD_Pt50to80_Mu5"] = 126748460.747;
  map_sampleName_sumGenWgt["QCD_Pt600to800_Mu5"] = 126748460.747;
  map_sampleName_sumGenWgt["QCD_Pt800to1000_Mu5_ext2"] = 126748460.747;
  map_sampleName_sumGenWgt["QCD_Pt80to120_EMEnriched_ext"] = 38966443.5421;
  map_sampleName_sumGenWgt["QCD_Pt80to120_Mu5"] = 126748460.747;
  map_sampleName_sumGenWgt["QCD_Pt80to120_Mu5_ext"] = 126748460.747;
  map_sampleName_sumGenWgt["QCD_Pt_170to250_bcToE"] = 57429713.852;
  map_sampleName_sumGenWgt["QCD_Pt_20to30_bcToE"] = 57429713.852;
  map_sampleName_sumGenWgt["QCD_Pt_250toInf_bcToE"] = 57429713.852;
  map_sampleName_sumGenWgt["QCD_Pt_30to80_bcToE"] = 57429713.852;
  map_sampleName_sumGenWgt["QCD_Pt_80to170_bcToE"] = 57429713.852;
  map_sampleName_sumGenWgt["TBar_tWch_ext"] = 6481480.0;
  map_sampleName_sumGenWgt["TBar_tch_powheg_part1"] = 37659712.0;
  map_sampleName_sumGenWgt["TBar_tch_powheg_part2"] = 37659712.0;
  map_sampleName_sumGenWgt["TBar_tch_powheg_part3"] = 37659712.0;
  map_sampleName_sumGenWgt["TTJets_SingleLeptonFromT_ext_part1"] = 54512878.0;
  map_sampleName_sumGenWgt["TTJets_SingleLeptonFromT_ext_part2"] = 54512878.0;
  map_sampleName_sumGenWgt["TTJets_SingleLeptonFromT_ext_part3"] = 54512878.0;
  map_sampleName_sumGenWgt["TTJets_SingleLeptonFromT_ext_part4"] = 54512878.0;
  map_sampleName_sumGenWgt["TTJets_SingleLeptonFromT_ext_part5"] = 54512878.0;
  map_sampleName_sumGenWgt["TTJets_SingleLeptonFromT_ext_part6"] = 54512878.0;
  map_sampleName_sumGenWgt["TTJets_SingleLeptonFromT_ext_part7"] = 54512878.0;
  map_sampleName_sumGenWgt["TTJets_SingleLeptonFromT_ext_part8"] = 54512878.0;
  map_sampleName_sumGenWgt["TTJets_SingleLeptonFromT_ext_part9"] = 54512878.0;
  map_sampleName_sumGenWgt["TTJets_SingleLeptonFromT_part1"] = 54512878.0;
  map_sampleName_sumGenWgt["TTJets_SingleLeptonFromT_part2"] = 54512878.0;
  map_sampleName_sumGenWgt["TTJets_SingleLeptonFromTbar_ext_part1"] = 52405916.0;
  map_sampleName_sumGenWgt["TTJets_SingleLeptonFromTbar_ext_part2"] = 52405916.0;
  map_sampleName_sumGenWgt["TTJets_SingleLeptonFromTbar_ext_part3"] = 52405916.0;
  map_sampleName_sumGenWgt["TTJets_SingleLeptonFromTbar_ext_part4"] = 52405916.0;
  map_sampleName_sumGenWgt["TTJets_SingleLeptonFromTbar_ext_part5"] = 52405916.0;
  map_sampleName_sumGenWgt["TTJets_SingleLeptonFromTbar_part1"] = 52405916.0;
  map_sampleName_sumGenWgt["TTJets_SingleLeptonFromTbar_part2"] = 52405916.0;
  map_sampleName_sumGenWgt["TToLeptons_sch_amcatnlo"] = 3370668.5184;
  map_sampleName_sumGenWgt["T_tWch_ext"] = 6332490.0;
  map_sampleName_sumGenWgt["T_tch_powheg_part1"] = 61947468.0;
  map_sampleName_sumGenWgt["T_tch_powheg_part2"] = 61947468.0;
  map_sampleName_sumGenWgt["WJetsToLNu_LO_ext_part1"] = 86099951.0;
  map_sampleName_sumGenWgt["WJetsToLNu_LO_ext_part10"] = 86099951.0;
  map_sampleName_sumGenWgt["WJetsToLNu_LO_ext_part2"] = 86099951.0;
  map_sampleName_sumGenWgt["WJetsToLNu_LO_ext_part3"] = 86099951.0;
  map_sampleName_sumGenWgt["WJetsToLNu_LO_ext_part4"] = 86099951.0;
  map_sampleName_sumGenWgt["WJetsToLNu_LO_ext_part5"] = 86099951.0;
  map_sampleName_sumGenWgt["WJetsToLNu_LO_ext_part6"] = 86099951.0;
  map_sampleName_sumGenWgt["WJetsToLNu_LO_ext_part7"] = 86099951.0;
  map_sampleName_sumGenWgt["WJetsToLNu_LO_ext_part8"] = 86099951.0;
  map_sampleName_sumGenWgt["WJetsToLNu_LO_ext_part9"] = 86099951.0;
  map_sampleName_sumGenWgt["WJetsToLNu_LO_part1"] = 86099951.0;
  map_sampleName_sumGenWgt["WJetsToLNu_LO_part2"] = 86099951.0;
  map_sampleName_sumGenWgt["WJetsToLNu_LO_part3"] = 86099951.0;
  map_sampleName_sumGenWgt["WJetsToLNu_LO_part4"] = 86099951.0;
  map_sampleName_sumGenWgt["WJetsToLNu_LO_part5"] = 86099951.0;
  map_sampleName_sumGenWgt["WJetsToLNu_LO_part6"] = 86099951.0;
  map_sampleName_sumGenWgt["WJetsToLNu_part1"] = 3.50627475345e+12;
  map_sampleName_sumGenWgt["WJetsToLNu_part2"] = 3.50627475345e+12;
  map_sampleName_sumGenWgt["WJetsToLNu_part3"] = 3.50627475345e+12;
  map_sampleName_sumGenWgt["WJetsToLNu_part4"] = 3.50627475345e+12;
  map_sampleName_sumGenWgt["WJetsToLNu_part5"] = 3.50627475345e+12;
  map_sampleName_sumGenWgt["WJetsToLNu_part6"] = 3.50627475345e+12;
  map_sampleName_sumGenWgt["WJetsToLNu_part7"] = 3.50627475345e+12;
  map_sampleName_sumGenWgt["WW"] = 6248191.83067;
  map_sampleName_sumGenWgt["WW_ext"] = 6248191.83067;
  map_sampleName_sumGenWgt["WZ"] = 3995828.0;
  map_sampleName_sumGenWgt["WZ_ext"] = 3995828.0;
  map_sampleName_sumGenWgt["ZZ"] = 1988098.0;
  map_sampleName_sumGenWgt["ZZ_ext"] = 1988098.0;

  if (sample.find("data") != string::npos || sample.find("fake") != string::npos) 
    return 1.0;
  else
    return map_sampleName_sumGenWgt[sample];

}

//=========================================================

void buildChain(TChain* chain, vector<Double_t>& genwgtVec, const bool use8TeVSample = true, const string& treePath = "", const Sample& sample = Sample::data_doubleEG, 
		TChain* chFriend = NULL, 
		TChain* chSfFriend = NULL
		) {
  
  cout << "Creating chain ..." << endl;
  
  vector<string> subSampleNameVector;

  if (use8TeVSample) {
    if (sample == Sample::wjets || sample == Sample::wenujets || sample == Sample::wmunujets || sample == Sample::wtaunujets) {
      subSampleNameVector.push_back("WJets");
    } else if (sample == Sample::zjets) {
      subSampleNameVector.push_back("DYJetsM50");
    } else if (sample == Sample::data_doubleEG) {
      subSampleNameVector.push_back("DoubleElectronAB");
      subSampleNameVector.push_back("DoubleElectronC");
      subSampleNameVector.push_back("DoubleElectronD");
    } else if (sample == Sample::data_singleEG || sample == Sample::qcd_ele_fake) {
      subSampleNameVector.push_back("SingleElectronAB");
      subSampleNameVector.push_back("SingleElectronC");
      subSampleNameVector.push_back("SingleElectronD");
    } else if (sample == Sample::data_doubleMu) {
      subSampleNameVector.push_back("DoubleMuAB");
      subSampleNameVector.push_back("DoubleMuC");
      subSampleNameVector.push_back("DoubleMuD");
    } else if (sample == Sample::data_singleMu || sample == Sample::qcd_mu_fake) {
      subSampleNameVector.push_back("SingleMuAB");
      subSampleNameVector.push_back("SingleMuC");
      subSampleNameVector.push_back("SingleMuD");
    } else if (sample == Sample::top) {
      subSampleNameVector.push_back("TTJets");
      subSampleNameVector.push_back("Tbarsch");
      subSampleNameVector.push_back("TbartW");
      subSampleNameVector.push_back("Tbartch");
      subSampleNameVector.push_back("Tsch");
      subSampleNameVector.push_back("TtW");
      subSampleNameVector.push_back("Ttch");
    } else if (sample == Sample::diboson) {
      subSampleNameVector.push_back("WWJets");
      subSampleNameVector.push_back("WZJets");
    } else if (sample == Sample::qcd_mu) {
      subSampleNameVector.push_back("QCDMuPt15");
    } else if (sample == Sample::qcd_ele) {
      cout << "#### Error in buildChain() function: qcd_ele not available at the moment, please check. Exit ..." << endl;
      exit(EXIT_FAILURE);
      //subSampleNameVector.push_back("");
    } else {
      cout << "#### Error in buildChain() function: sample name not available, please check. Exit ..." << endl;
      exit(EXIT_FAILURE);
    }
  } else {

    if (sample == Sample::wjets || sample == Sample::wenujets || sample == Sample::wmunujets || sample == Sample::wtaunujets) {
      subSampleNameVector.push_back("WJetsToLNu_part1");
      subSampleNameVector.push_back("WJetsToLNu_part2");
      subSampleNameVector.push_back("WJetsToLNu_part3");
      subSampleNameVector.push_back("WJetsToLNu_part4");
      subSampleNameVector.push_back("WJetsToLNu_part5");
      subSampleNameVector.push_back("WJetsToLNu_part6");
      subSampleNameVector.push_back("WJetsToLNu_part7");
    } else if (sample == Sample::wjets_LO || sample == Sample::wenujets_LO || sample == Sample::wmunujets_LO || sample == Sample::wtaunujets_LO) { 
      subSampleNameVector.push_back("WJetsToLNu_LO_ext_part1");
      subSampleNameVector.push_back("WJetsToLNu_LO_ext_part10");
      subSampleNameVector.push_back("WJetsToLNu_LO_ext_part2");
      subSampleNameVector.push_back("WJetsToLNu_LO_ext_part3");
      subSampleNameVector.push_back("WJetsToLNu_LO_ext_part4");
      subSampleNameVector.push_back("WJetsToLNu_LO_ext_part5");
      subSampleNameVector.push_back("WJetsToLNu_LO_ext_part6");
      subSampleNameVector.push_back("WJetsToLNu_LO_ext_part7");
      subSampleNameVector.push_back("WJetsToLNu_LO_ext_part8");
      subSampleNameVector.push_back("WJetsToLNu_LO_ext_part9");
      subSampleNameVector.push_back("WJetsToLNu_LO_part1");
      subSampleNameVector.push_back("WJetsToLNu_LO_part2");
      subSampleNameVector.push_back("WJetsToLNu_LO_part3");
      subSampleNameVector.push_back("WJetsToLNu_LO_part4");
      subSampleNameVector.push_back("WJetsToLNu_LO_part5");
      subSampleNameVector.push_back("WJetsToLNu_LO_part6");
    } else if (sample == Sample::zjets) {
      subSampleNameVector.push_back("DYJetsToLL_M50_part1");
      subSampleNameVector.push_back("DYJetsToLL_M50_part2");
    } else if (sample == Sample::zjets_LO) {
      subSampleNameVector.push_back("DYJetsToLL_M50_LO_ext2_part1");
      subSampleNameVector.push_back("DYJetsToLL_M50_LO_ext2_part10");
      subSampleNameVector.push_back("DYJetsToLL_M50_LO_ext2_part11");
      subSampleNameVector.push_back("DYJetsToLL_M50_LO_ext2_part2");
      subSampleNameVector.push_back("DYJetsToLL_M50_LO_ext2_part3");
      subSampleNameVector.push_back("DYJetsToLL_M50_LO_ext2_part4");
      subSampleNameVector.push_back("DYJetsToLL_M50_LO_ext2_part5");
      subSampleNameVector.push_back("DYJetsToLL_M50_LO_ext2_part6");
      subSampleNameVector.push_back("DYJetsToLL_M50_LO_ext2_part7");
      subSampleNameVector.push_back("DYJetsToLL_M50_LO_ext2_part8");
      subSampleNameVector.push_back("DYJetsToLL_M50_LO_ext2_part9");
      subSampleNameVector.push_back("DYJetsToLL_M50_LO_ext_part1");
      subSampleNameVector.push_back("DYJetsToLL_M50_LO_ext_part2");
      subSampleNameVector.push_back("DYJetsToLL_M50_LO_ext_part3");
      subSampleNameVector.push_back("DYJetsToLL_M50_LO_ext_part4");
      subSampleNameVector.push_back("DYJetsToLL_M50_LO_ext_part5");
      subSampleNameVector.push_back("DYJetsToLL_M50_LO_ext_part6");
    /* } else if (sample == Sample::data_doubleEG) { */
    /* } else if (sample == Sample::data_doubleMu) { */
    } else if (sample == Sample::data_singleEG) {
      subSampleNameVector.push_back("SingleElectron_Run2016B_part1");
      subSampleNameVector.push_back("SingleElectron_Run2016B_part10");
      subSampleNameVector.push_back("SingleElectron_Run2016B_part11");
      subSampleNameVector.push_back("SingleElectron_Run2016B_part12");
      subSampleNameVector.push_back("SingleElectron_Run2016B_part2");
      subSampleNameVector.push_back("SingleElectron_Run2016B_part3");
      subSampleNameVector.push_back("SingleElectron_Run2016B_part4");
      subSampleNameVector.push_back("SingleElectron_Run2016B_part5");
      subSampleNameVector.push_back("SingleElectron_Run2016B_part6");
      subSampleNameVector.push_back("SingleElectron_Run2016B_part7");
      subSampleNameVector.push_back("SingleElectron_Run2016B_part8");
      subSampleNameVector.push_back("SingleElectron_Run2016B_part9");
      subSampleNameVector.push_back("SingleElectron_Run2016C_part1");
      subSampleNameVector.push_back("SingleElectron_Run2016C_part2");
      subSampleNameVector.push_back("SingleElectron_Run2016C_part3");
      subSampleNameVector.push_back("SingleElectron_Run2016C_part4");
      subSampleNameVector.push_back("SingleElectron_Run2016C_part5");
      subSampleNameVector.push_back("SingleElectron_Run2016C_part6");
      subSampleNameVector.push_back("SingleElectron_Run2016C_part7");
      subSampleNameVector.push_back("SingleElectron_Run2016D_part1");
      subSampleNameVector.push_back("SingleElectron_Run2016D_part10");
      subSampleNameVector.push_back("SingleElectron_Run2016D_part11");
      subSampleNameVector.push_back("SingleElectron_Run2016D_part2");
      subSampleNameVector.push_back("SingleElectron_Run2016D_part3");
      subSampleNameVector.push_back("SingleElectron_Run2016D_part4");
      subSampleNameVector.push_back("SingleElectron_Run2016D_part5");
      subSampleNameVector.push_back("SingleElectron_Run2016D_part6");
      subSampleNameVector.push_back("SingleElectron_Run2016D_part7");
      subSampleNameVector.push_back("SingleElectron_Run2016D_part8");
      subSampleNameVector.push_back("SingleElectron_Run2016D_part9");
      subSampleNameVector.push_back("SingleElectron_Run2016E_part1");
      subSampleNameVector.push_back("SingleElectron_Run2016E_part2");
      subSampleNameVector.push_back("SingleElectron_Run2016E_part3");
      subSampleNameVector.push_back("SingleElectron_Run2016E_part4");
      subSampleNameVector.push_back("SingleElectron_Run2016E_part5");
      subSampleNameVector.push_back("SingleElectron_Run2016E_part6");
      subSampleNameVector.push_back("SingleElectron_Run2016E_part7");
      subSampleNameVector.push_back("SingleElectron_Run2016E_part8");
      subSampleNameVector.push_back("SingleElectron_Run2016F_part1");
      subSampleNameVector.push_back("SingleElectron_Run2016F_part2");
      subSampleNameVector.push_back("SingleElectron_Run2016F_part3");
      subSampleNameVector.push_back("SingleElectron_Run2016F_part4");
      subSampleNameVector.push_back("SingleElectron_Run2016F_part5");
      subSampleNameVector.push_back("SingleElectron_Run2016F_part6");
      /* subSampleNameVector.push_back("SingleElectron_Run2016G_part1"); */
      /* subSampleNameVector.push_back("SingleElectron_Run2016G_part10"); */
      /* subSampleNameVector.push_back("SingleElectron_Run2016G_part11"); */
      /* subSampleNameVector.push_back("SingleElectron_Run2016G_part12"); */
      /* subSampleNameVector.push_back("SingleElectron_Run2016G_part13"); */
      /* subSampleNameVector.push_back("SingleElectron_Run2016G_part2"); */
      /* subSampleNameVector.push_back("SingleElectron_Run2016G_part3"); */
      /* subSampleNameVector.push_back("SingleElectron_Run2016G_part4"); */
      /* subSampleNameVector.push_back("SingleElectron_Run2016G_part5"); */
      /* subSampleNameVector.push_back("SingleElectron_Run2016G_part6"); */
      /* subSampleNameVector.push_back("SingleElectron_Run2016G_part7"); */
      /* subSampleNameVector.push_back("SingleElectron_Run2016G_part8"); */
      /* subSampleNameVector.push_back("SingleElectron_Run2016G_part9"); */
      /* subSampleNameVector.push_back("SingleElectron_Run2016H_part1"); */
      /* subSampleNameVector.push_back("SingleElectron_Run2016H_part10"); */
      /* subSampleNameVector.push_back("SingleElectron_Run2016H_part11"); */
      /* subSampleNameVector.push_back("SingleElectron_Run2016H_part12"); */
      /* subSampleNameVector.push_back("SingleElectron_Run2016H_part13"); */
      /* subSampleNameVector.push_back("SingleElectron_Run2016H_part14"); */
      /* subSampleNameVector.push_back("SingleElectron_Run2016H_part2"); */
      /* subSampleNameVector.push_back("SingleElectron_Run2016H_part3"); */
      /* subSampleNameVector.push_back("SingleElectron_Run2016H_part4"); */
      /* subSampleNameVector.push_back("SingleElectron_Run2016H_part5"); */
      /* subSampleNameVector.push_back("SingleElectron_Run2016H_part6"); */
      /* subSampleNameVector.push_back("SingleElectron_Run2016H_part7"); */
      /* subSampleNameVector.push_back("SingleElectron_Run2016H_part8"); */
      /* subSampleNameVector.push_back("SingleElectron_Run2016H_part9"); */
    } else if (sample == Sample::data_singleMu) { 
      subSampleNameVector.push_back("SingleMuon_Run2016B_part1");
      subSampleNameVector.push_back("SingleMuon_Run2016B_part10");
      subSampleNameVector.push_back("SingleMuon_Run2016B_part11");
      subSampleNameVector.push_back("SingleMuon_Run2016B_part12");
      subSampleNameVector.push_back("SingleMuon_Run2016B_part13");
      subSampleNameVector.push_back("SingleMuon_Run2016B_part14");
      subSampleNameVector.push_back("SingleMuon_Run2016B_part15");
      subSampleNameVector.push_back("SingleMuon_Run2016B_part16");
      subSampleNameVector.push_back("SingleMuon_Run2016B_part17");
      subSampleNameVector.push_back("SingleMuon_Run2016B_part18");
      subSampleNameVector.push_back("SingleMuon_Run2016B_part19");
      subSampleNameVector.push_back("SingleMuon_Run2016B_part2");
      subSampleNameVector.push_back("SingleMuon_Run2016B_part20");
      subSampleNameVector.push_back("SingleMuon_Run2016B_part21");
      subSampleNameVector.push_back("SingleMuon_Run2016B_part22");
      subSampleNameVector.push_back("SingleMuon_Run2016B_part23");
      subSampleNameVector.push_back("SingleMuon_Run2016B_part3");
      subSampleNameVector.push_back("SingleMuon_Run2016B_part4");
      subSampleNameVector.push_back("SingleMuon_Run2016B_part5");
      subSampleNameVector.push_back("SingleMuon_Run2016B_part6");
      subSampleNameVector.push_back("SingleMuon_Run2016B_part7");
      subSampleNameVector.push_back("SingleMuon_Run2016B_part8");
      subSampleNameVector.push_back("SingleMuon_Run2016B_part9");
      subSampleNameVector.push_back("SingleMuon_Run2016C_part1");
      subSampleNameVector.push_back("SingleMuon_Run2016C_part10");
      subSampleNameVector.push_back("SingleMuon_Run2016C_part2");
      subSampleNameVector.push_back("SingleMuon_Run2016C_part3");
      subSampleNameVector.push_back("SingleMuon_Run2016C_part4");
      subSampleNameVector.push_back("SingleMuon_Run2016C_part5");
      subSampleNameVector.push_back("SingleMuon_Run2016C_part6");
      subSampleNameVector.push_back("SingleMuon_Run2016C_part7");
      subSampleNameVector.push_back("SingleMuon_Run2016C_part8");
      subSampleNameVector.push_back("SingleMuon_Run2016C_part9");
      subSampleNameVector.push_back("SingleMuon_Run2016D_part1");
      subSampleNameVector.push_back("SingleMuon_Run2016D_part2");
      subSampleNameVector.push_back("SingleMuon_Run2016D_part3");
      subSampleNameVector.push_back("SingleMuon_Run2016D_part4");
      subSampleNameVector.push_back("SingleMuon_Run2016D_part5");
      subSampleNameVector.push_back("SingleMuon_Run2016D_part6");
      subSampleNameVector.push_back("SingleMuon_Run2016E_part1");
      subSampleNameVector.push_back("SingleMuon_Run2016E_part10");
      subSampleNameVector.push_back("SingleMuon_Run2016E_part11");
      subSampleNameVector.push_back("SingleMuon_Run2016E_part12");
      subSampleNameVector.push_back("SingleMuon_Run2016E_part13");
      subSampleNameVector.push_back("SingleMuon_Run2016E_part14");
      subSampleNameVector.push_back("SingleMuon_Run2016E_part2");
      subSampleNameVector.push_back("SingleMuon_Run2016E_part3");
      subSampleNameVector.push_back("SingleMuon_Run2016E_part4");
      subSampleNameVector.push_back("SingleMuon_Run2016E_part5");
      subSampleNameVector.push_back("SingleMuon_Run2016E_part6");
      subSampleNameVector.push_back("SingleMuon_Run2016E_part7");
      subSampleNameVector.push_back("SingleMuon_Run2016E_part8");
      subSampleNameVector.push_back("SingleMuon_Run2016E_part9");
      subSampleNameVector.push_back("SingleMuon_Run2016F_part1");
      subSampleNameVector.push_back("SingleMuon_Run2016F_part10");
      subSampleNameVector.push_back("SingleMuon_Run2016F_part11");
      subSampleNameVector.push_back("SingleMuon_Run2016F_part2");
      subSampleNameVector.push_back("SingleMuon_Run2016F_part3");
      subSampleNameVector.push_back("SingleMuon_Run2016F_part4");
      subSampleNameVector.push_back("SingleMuon_Run2016F_part5");
      subSampleNameVector.push_back("SingleMuon_Run2016F_part6");
      subSampleNameVector.push_back("SingleMuon_Run2016F_part7");
      subSampleNameVector.push_back("SingleMuon_Run2016F_part8");
      subSampleNameVector.push_back("SingleMuon_Run2016F_part9");
      subSampleNameVector.push_back("SingleMuon_Run2016G_part1");
      subSampleNameVector.push_back("SingleMuon_Run2016G_part10");
      subSampleNameVector.push_back("SingleMuon_Run2016G_part11");
      subSampleNameVector.push_back("SingleMuon_Run2016G_part12");
      subSampleNameVector.push_back("SingleMuon_Run2016G_part13");
      subSampleNameVector.push_back("SingleMuon_Run2016G_part14");
      subSampleNameVector.push_back("SingleMuon_Run2016G_part15");
      subSampleNameVector.push_back("SingleMuon_Run2016G_part16");
      subSampleNameVector.push_back("SingleMuon_Run2016G_part17");
      subSampleNameVector.push_back("SingleMuon_Run2016G_part18");
      subSampleNameVector.push_back("SingleMuon_Run2016G_part19");
      subSampleNameVector.push_back("SingleMuon_Run2016G_part2");
      subSampleNameVector.push_back("SingleMuon_Run2016G_part20");
      subSampleNameVector.push_back("SingleMuon_Run2016G_part21");
      subSampleNameVector.push_back("SingleMuon_Run2016G_part22");
      subSampleNameVector.push_back("SingleMuon_Run2016G_part23");
      subSampleNameVector.push_back("SingleMuon_Run2016G_part3");
      subSampleNameVector.push_back("SingleMuon_Run2016G_part4");
      subSampleNameVector.push_back("SingleMuon_Run2016G_part5");
      subSampleNameVector.push_back("SingleMuon_Run2016G_part6");
      subSampleNameVector.push_back("SingleMuon_Run2016G_part7");
      subSampleNameVector.push_back("SingleMuon_Run2016G_part8");
      subSampleNameVector.push_back("SingleMuon_Run2016G_part9");
      subSampleNameVector.push_back("SingleMuon_Run2016H_part1");
      subSampleNameVector.push_back("SingleMuon_Run2016H_part10");
      subSampleNameVector.push_back("SingleMuon_Run2016H_part11");
      subSampleNameVector.push_back("SingleMuon_Run2016H_part12");
      subSampleNameVector.push_back("SingleMuon_Run2016H_part13");
      subSampleNameVector.push_back("SingleMuon_Run2016H_part14");
      subSampleNameVector.push_back("SingleMuon_Run2016H_part15");
      subSampleNameVector.push_back("SingleMuon_Run2016H_part17");
      subSampleNameVector.push_back("SingleMuon_Run2016H_part18");
      subSampleNameVector.push_back("SingleMuon_Run2016H_part19");
      subSampleNameVector.push_back("SingleMuon_Run2016H_part2");
      subSampleNameVector.push_back("SingleMuon_Run2016H_part20");
      subSampleNameVector.push_back("SingleMuon_Run2016H_part21");
      subSampleNameVector.push_back("SingleMuon_Run2016H_part22");
      subSampleNameVector.push_back("SingleMuon_Run2016H_part23");
      subSampleNameVector.push_back("SingleMuon_Run2016H_part24");
      subSampleNameVector.push_back("SingleMuon_Run2016H_part25");
      subSampleNameVector.push_back("SingleMuon_Run2016H_part26");
      subSampleNameVector.push_back("SingleMuon_Run2016H_part27");
      subSampleNameVector.push_back("SingleMuon_Run2016H_part28");
      subSampleNameVector.push_back("SingleMuon_Run2016H_part29");
      subSampleNameVector.push_back("SingleMuon_Run2016H_part3");
      subSampleNameVector.push_back("SingleMuon_Run2016H_part30");
      subSampleNameVector.push_back("SingleMuon_Run2016H_part31");
      subSampleNameVector.push_back("SingleMuon_Run2016H_part32");
      subSampleNameVector.push_back("SingleMuon_Run2016H_part4");
      subSampleNameVector.push_back("SingleMuon_Run2016H_part5");
      subSampleNameVector.push_back("SingleMuon_Run2016H_part6");
      subSampleNameVector.push_back("SingleMuon_Run2016H_part7");
      subSampleNameVector.push_back("SingleMuon_Run2016H_part8");
      subSampleNameVector.push_back("SingleMuon_Run2016H_part9");
    } else if (sample == Sample::top) {
      subSampleNameVector.push_back("TBar_tWch_ext");
      subSampleNameVector.push_back("TBar_tch_powheg_part1");
      subSampleNameVector.push_back("TBar_tch_powheg_part2");
      subSampleNameVector.push_back("TBar_tch_powheg_part3");
      subSampleNameVector.push_back("TTJets_SingleLeptonFromT_ext_part1");
      subSampleNameVector.push_back("TTJets_SingleLeptonFromT_ext_part2");
      subSampleNameVector.push_back("TTJets_SingleLeptonFromT_ext_part3");
      subSampleNameVector.push_back("TTJets_SingleLeptonFromT_ext_part4");
      subSampleNameVector.push_back("TTJets_SingleLeptonFromT_ext_part5");
      subSampleNameVector.push_back("TTJets_SingleLeptonFromT_ext_part6");
      subSampleNameVector.push_back("TTJets_SingleLeptonFromT_ext_part7");
      subSampleNameVector.push_back("TTJets_SingleLeptonFromT_ext_part8");
      subSampleNameVector.push_back("TTJets_SingleLeptonFromT_ext_part9");
      subSampleNameVector.push_back("TTJets_SingleLeptonFromT_part1");
      subSampleNameVector.push_back("TTJets_SingleLeptonFromT_part2");
      subSampleNameVector.push_back("TTJets_SingleLeptonFromTbar_ext_part1");
      subSampleNameVector.push_back("TTJets_SingleLeptonFromTbar_ext_part2");
      subSampleNameVector.push_back("TTJets_SingleLeptonFromTbar_ext_part3");
      subSampleNameVector.push_back("TTJets_SingleLeptonFromTbar_ext_part4");
      subSampleNameVector.push_back("TTJets_SingleLeptonFromTbar_ext_part5");
      subSampleNameVector.push_back("TTJets_SingleLeptonFromTbar_part1");
      subSampleNameVector.push_back("TTJets_SingleLeptonFromTbar_part2");
      subSampleNameVector.push_back("TToLeptons_sch_amcatnlo");
      subSampleNameVector.push_back("T_tWch_ext");
      subSampleNameVector.push_back("T_tch_powheg_part1");
      subSampleNameVector.push_back("T_tch_powheg_part2");
    } else if (sample == Sample::diboson) {
      subSampleNameVector.push_back("WW");
      subSampleNameVector.push_back("WW_ext");
      subSampleNameVector.push_back("WZ");
      subSampleNameVector.push_back("WZ_ext");
      subSampleNameVector.push_back("ZZ");
      subSampleNameVector.push_back("ZZ_ext");
    } else if (sample == Sample::qcd_mu) {
      subSampleNameVector.push_back("QCD_Mu15_part1");
      subSampleNameVector.push_back("QCD_Mu15_part2");
      subSampleNameVector.push_back("QCD_Pt1000toInf_Mu5");
      subSampleNameVector.push_back("QCD_Pt120to170_Mu5");
      subSampleNameVector.push_back("QCD_Pt15to20_Mu5");
      subSampleNameVector.push_back("QCD_Pt170to300_Mu5");
      subSampleNameVector.push_back("QCD_Pt170to300_Mu5_ext");
      subSampleNameVector.push_back("QCD_Pt20to30_Mu5");
      subSampleNameVector.push_back("QCD_Pt300to470_Mu5");
      subSampleNameVector.push_back("QCD_Pt300to470_Mu5_ext");
      subSampleNameVector.push_back("QCD_Pt300to470_Mu5_ext2");
      subSampleNameVector.push_back("QCD_Pt30to50_Mu5");
      subSampleNameVector.push_back("QCD_Pt470to600_Mu5_ext");
      subSampleNameVector.push_back("QCD_Pt50to80_Mu5");
      subSampleNameVector.push_back("QCD_Pt600to800_Mu5");
      subSampleNameVector.push_back("QCD_Pt800to1000_Mu5_ext2");
      subSampleNameVector.push_back("QCD_Pt80to120_Mu5");
      subSampleNameVector.push_back("QCD_Pt80to120_Mu5_ext");
    } else if (sample == Sample::qcd_ele) {
      subSampleNameVector.push_back("QCD_Pt20to30_EMEnriched");
      subSampleNameVector.push_back("QCD_Pt30to50_EMEnriched");
      subSampleNameVector.push_back("QCD_Pt30to50_EMEnriched_ext");
      subSampleNameVector.push_back("QCD_Pt50to80_EMEnriched_ext");
      subSampleNameVector.push_back("QCD_Pt80to120_EMEnriched_ext");
      subSampleNameVector.push_back("QCD_Pt_170to250_bcToE");
      subSampleNameVector.push_back("QCD_Pt_20to30_bcToE");
      subSampleNameVector.push_back("QCD_Pt_250toInf_bcToE");
      subSampleNameVector.push_back("QCD_Pt_30to80_bcToE");
      subSampleNameVector.push_back("QCD_Pt_80to170_bcToE");
    } else {
      cout << "#### Error in buildChain() function: sample name not available, please check. Exit ..." << endl;
      exit(EXIT_FAILURE);
    }

  }
  
  for(UInt_t i = 0; i < subSampleNameVector.size(); i++) {
  
    string treeRootFile = "";
    if (use8TeVSample) {

      treeRootFile = treePath + subSampleNameVector[i] + "/treeProducerWMassEle/treeProducerWMassEle_tree.root";
      if (treePath.find("WSKIM_V") != string::npos || treePath.find("QCDSKIM_V") != string::npos || treePath.find("ZEESKIM_V") != string::npos) {
	treeRootFile = treePath + subSampleNameVector[i] + "/treeProducerWMassEle/tree.root";
      }

    } else {

      if (treePath.find("/eos/cms/") != string::npos) {
	treeRootFile = treePath + subSampleNameVector[i] + "/treeProducerWMass/tree.root";
      } else {
	cout << "13 TeV trees not available outside eos, or function to read them not implemented yet. Please check. Exit." << endl;
	exit(EXIT_FAILURE);
      }

    }

    cout << "Tree: " << treeRootFile << endl;

    chain->Add(TString(treeRootFile.c_str()));

    // in the following we need the total number of generated events to normalize MC
    // for 8 TeV there is a histogram in the same file with root tree, named Count
    // its integral (or number of entries, since it is an integer) gives the total number of generated events
    // at 13 TeV, depending on MC (LO or NLO) we have a gen weight different from 1, and it is not an integer number in general
    // we need the sum of gen weights
    // Moreover, if we have extensions for a MC sample (and in case both versions are used) each of them must be normalized to the sum of the two sum of weights
    // otherwise we are adding the same MC as a different process
    // since at 13 TeV, due to lack of space during MC ntuples production, we also have many chunks of the same process, I wrote a script to produce a map
    // that associates to a given sample its proper sumGenWeights value

    if (use8TeVSample) {

      string fileNameToGetTH1 = treeRootFile;
      // read number of generated events
      TFile* ftree = new TFile(fileNameToGetTH1.c_str(),"READ");
      if (!ftree || ftree->IsZombie()) {
	cout << "### Error in buildChain(): couldn't open file '" << treeRootFile << "'. Exit" << endl;
	exit(EXIT_FAILURE);
      }
      TH1F* hCount = (TH1F*) getHistCloneFromFile(ftree,"Count","");
      checkNotNullPtr(hCount,"hCount");
 
     genwgtVec.push_back(getXsec8TeV(subSampleNameVector[i])/hCount->GetEntries());    
 
      delete hCount;
      ftree->Close();
      delete ftree;

    } else {

      string sampleDir = getStringFromEnumSample(sample).c_str();
      if (sampleDir.find("data") == string::npos && sampleDir.find("fake") == string::npos) {
	genwgtVec.push_back(1./getSumGenWeightFromSampleName(subSampleNameVector[i]));    
      }

    }

  }

  if(!chain ) {
    cout << "#### Error in buildChain() function: chain not created. End of programme" << endl;
    exit(EXIT_FAILURE);
  }

  cout << "entries in chain    = " << chain->   GetEntries() << endl;

  // friend
  if (chFriend != NULL) {

    for(UInt_t i = 0; i < subSampleNameVector.size(); i++) {
  
      string friend_treeRootFile = "";
      if (use8TeVSample) friend_treeRootFile = treePath + "friends/evVarFriend_" + subSampleNameVector[i]+ ".root";
      else friend_treeRootFile = treePath + "friends/tree_Friend_" + subSampleNameVector[i]+ ".root";

      chFriend->Add(TString(friend_treeRootFile.c_str()));

    }

    if(!chFriend ) {
      cout << "#### Error in buildChain() function: chFriend not created. End of programme" << endl;
      exit(EXIT_FAILURE);
    }

    cout << "Adding friend to chain ..." << endl;
    chain->AddFriend(chFriend); //adding whole friend chain as friend   
    cout << "entries in chFriend = " << chFriend->GetEntries() << endl;
    
    if (chain->GetEntries() != chFriend->GetEntries()) {
      cout << "#### Error in buildChain() function: chain and chFriend have different number of events." << endl;      
      cout << "sample: " << getStringFromEnumSample(sample) << endl;
      cout << "chain: " << chain->GetEntries() << endl;
      cout << "chFriend: " << chFriend->GetEntries() << endl;
      cout << "#### End of programme" << endl;
      exit(EXIT_FAILURE);
    }

  }

  // SF friend
  if (chSfFriend != NULL) {

    for(UInt_t i = 0; i < subSampleNameVector.size(); i++) {
  
      string friend_treeRootFile = treePath + "friends/sfFriend_" + subSampleNameVector[i]+ ".root";
      chSfFriend->Add(TString(friend_treeRootFile.c_str()));

    }

    if(!chSfFriend ) {
      cout << "#### Error in buildChain() function: chSfFriend not created. End of programme" << endl;
      exit(EXIT_FAILURE);
    }

    cout << "Adding SF friend to chain ..." << endl;
    chain->AddFriend(chSfFriend); //adding whole friend chain as friend   
    cout << "entries in chSfFriend = " << chSfFriend->GetEntries() << endl;
    
    if (chain->GetEntries() != chSfFriend->GetEntries()) {
      cout << "#### Error in buildChain8TeV() function: chain and chSfFriend have different number of events." << endl;      
      cout << "sample: " << getStringFromEnumSample(sample) << endl;
      cout << "chain: " << chain->GetEntries() << endl;
      cout << "chSfFriend: " << chSfFriend->GetEntries() << endl;
      cout << "#### End of programme" << endl;
      exit(EXIT_FAILURE);
    }

  }


}



//=========================================================


Double_t myRayleigh(Double_t* x, Double_t* par) {

  Double_t xcur = x[0];
  Double_t sigma = par[0];
  Double_t Norm = par[1];
  Double_t t = xcur - par[2];
  Double_t invSigma2 = TMath::Power(sigma * sigma, -1);
  
  return Norm * xcur * invSigma2 * exp(-1. * xcur * xcur * invSigma2);
  //return xcur * invSigma2 * exp(-1. * xcur * xcur * invSigma2);

}


//============================================================

void makeFit(TH1* hist) {

  TCanvas* canvas = new TCanvas("canvas","",700,700);
  hist->Draw("HE");

  TF1* rayleigh = new TF1("rayleigh",&myRayleigh,20,135,3);
  //TF1* rayleigh = new TF1("rayleigh",&myRayleigh,20,135,1);
  rayleigh->SetParNames("sigma","norm","shift");
  rayleigh->SetParLimits(rayleigh->GetParNumber("sigma"),50,70);
  rayleigh->SetParLimits(rayleigh->GetParNumber("norm"),0.1,100);
  rayleigh->SetParLimits(rayleigh->GetParNumber("shift"),15,25);
  // mode of rayleigh is sigma
  rayleigh->SetParameters(hist->GetBinCenter(hist->GetMaximumBin()),hist->GetBinContent(hist->GetMaximumBin()),20);
  //rayleigh->SetParameter(rayleigh->GetParNumber("sigma"),hist->GetBinCenter(hist->GetMaximumBin()));
  rayleigh->SetLineColor(kRed);

  TFitResultPtr frp1 = hist->Fit(rayleigh,"E L I S Q B R","HE",20, 135);

  canvas->Update();
  // box for fit with Crystal Ball                                                                                                                     
  TPaveStats *stat = (TPaveStats*)(hist->FindObject("stats"));
  if(stat) {
    // stat->SetTextColor(kBlue);                                                                                                                      
    // stat1->SetTextColor(kGreen);                                                                                                                    
    Double_t width = stat->GetX2NDC() - stat->GetX1NDC();
    // make stat box bigger                                                                                                                            
    stat->SetX1NDC(stat->GetX1NDC() - 0.25 * width);
    stat->Draw();
  }


  canvas->SaveAs("/afs/cern.ch/user/m/mciprian/www/test_plot/rayleigh.png");

}




#endif
