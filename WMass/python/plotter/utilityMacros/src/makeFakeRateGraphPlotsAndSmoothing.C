#include "../interface/utility.h"

const static int smoothPolinDegree = 1; 
// when I search for a bin given the boundary, the lower boundary should belong to the bin, the upper not, but rounding could ruin this logic 
// so I add an epsilon
const static Double_t epsilon = 0.0001;  

using namespace std;

// rebin pt like this for W and Z or sum (should be a subsample of bin boundaries array before rebinning (taken directly from histograms)
// the higher the index, the less granular is the array
static const vector<Double_t> ptBinBoundariesQCD_1 = {30,34,38,42,46,50,55,60,65};
static const vector<Double_t> ptBinBoundariesQCD_2 = {30,35,40,45,50,55,60,65};
static const vector<Double_t> ptBinBoundariesEWK_1 = {30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,46,48,50,55,60,65};
static const vector<Double_t> ptBinBoundariesEWK_2 = {30,32,34,36,38,40,42,44,46,48,50,55,60,65};
static const vector<Double_t> ptBinBoundariesData_1 = {30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,46,48,50,55,60,65};
static const vector<Double_t> ptBinBoundariesData_2 = {30,32,34,36,38,40,42,44,46,48,50,55,60,65};

vector<Double_t> etaBoundariesGlobal;

TH2D* frSmoothParameter_data = nullptr;
TH2D* frSmoothParameter_data_fitNarrowRange = nullptr;
TH2D* frSmoothParameter_qcd = nullptr;
TH2D* frSmoothParameter_w = nullptr;
TH2D* frSmoothParameter_z = nullptr;
TH2D* frSmoothParameter_ewk = nullptr;

// the core of this macro is makeFakeRateGraphPlotsAndSmoothing(), which is at the bottom of this code and calls all the rest

//============================================

void plotFRparamRelUncertainty(TH2* h2 = nullptr, 
			       const string& outDir = "", 
			       const string& xAxisName = "",
			       const string& yAxisName = "",
			       const string& zAxisName = "", 
			       const string& canvasName = "") 
{

  TH2* h2relUnc = (TH2*) h2->Clone("relUnc");

  for (Int_t i = 1; i <= h2relUnc->GetNbinsX(); i++) {

    for (Int_t j = 1; j <= h2relUnc->GetNbinsX(); j++) {
      
      Double_t var = h2relUnc->GetBinContent(i,j);
      var = (var == 0) ? 0 : fabs(h2relUnc->GetBinError(i,j)/var);
      if (var > 1) var = 1;
      h2relUnc->SetBinContent(i,j,var);

    }

  }
    

  drawCorrelationPlot(h2relUnc, 
		      xAxisName,
		      yAxisName,
		      zAxisName,
		      canvasName,
		      "", outDir, 1,1, false,false,false,1);


}

//============================================

void fillTH2fromTH3zrange(TH2* h2 = nullptr, const TH3* h3 = nullptr, const Int_t zbinLow = 1, const Int_t zbinHigh = 1) {

  // assume TH2 is a slice of TH3 with same binning

  for (Int_t ix = 1; ix <= h2->GetNbinsX(); ++ix) {

    for (Int_t iy = 1; iy <= h2->GetNbinsY(); ++iy) {
      
      h2->SetBinContent(ix,iy,h3->Integral(ix,ix,iy,iy,zbinLow,zbinHigh));
      
    }
    
  }

}

//============================================

void fillFakeRateTH2(TH2* h2 = nullptr, const Int_t etaBin = 0, const TH1* hpass = nullptr, const TH1* hntot = nullptr) {

  // the TH1 passed to this function might have less xbins than TH2, becasue TH2 has the original bins of pt in the input root file
  // TH1 might have been rebinned, but since the new binning is a subset of the original, we can just fill two or more consecutive bins of TH2 with same values

  TH1* ratio = (TH1*) hpass->Clone("ratio");
  ratio->Divide(hntot);

  Double_t pt = 0.0;

  for (Int_t ipt = 1; ipt < h2->GetNbinsX(); ++ipt) {
    
    pt = h2->GetXaxis()->GetBinCenter(ipt);
    h2->SetBinContent(ipt,etaBin,ratio->GetBinContent(ratio->GetXaxis()->FindFixBin(pt)));

  }

}


//============================================


void fillFakeRateTH2smooth(TH2* h2 = nullptr, const TH2* h2fit = nullptr) {

  // the TH1 passed to this function might have less xbins than TH2, becasue TH2 has the original bins of pt in the input root file
  // TH1 might have been rebinned, but since the new binning is a subset of the original, we can just fill two or more consecutive bins of TH2 with same values

  Double_t offset = 0.0;
  Double_t slope  = 0.0;
  Double_t pt = 0.0;

  for (Int_t ipt = 1; ipt <= h2->GetNbinsX(); ++ipt) {

    for (Int_t ieta = 1; ieta <= h2->GetNbinsY(); ++ieta) {

      pt = h2->GetXaxis()->GetBinCenter(ipt);
      offset = h2fit->GetBinContent(ieta, 1);
      slope = h2fit->GetBinContent(ieta, 2);
      h2->SetBinContent(ipt,ieta, std::max(0.0, offset + slope * pt));
      
    }

  }

}

//============================================

// following part is for the smoothing of the fake rate

//============================================

TFitResultPtr fitGraph(TGraph* gr = NULL, 
		       const Bool_t isEB = true,
		       const string& xAxisNameTmp = "xAxis", 
		       const string& yAxisNameTmp = "yAxis", 
		       const string& canvasName = "default",
		       const string& outDir = "./",
		       const string& legEntry = "",
		       const vector<Double_t>& legCoord = {0.5,0.15,0.9,0.35},
		       const Double_t lumi = -1.0,
		       const Bool_t isData = true,
		       const Bool_t isPromptRate = false,
		       const Double_t nSigmaVarInPlot = 1.0,
		       TFitResultPtr* fitPtr_fitNarrowRange = nullptr
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

  // override function above
  Int_t n = gr->GetN();
  Double_t* y = gr->GetY();
  Double_t* yerrup = gr->GetEYhigh();
  Double_t* yerrdn = gr->GetEYlow();
  Int_t loc = TMath::LocMax(n,y);
  Double_t tmax = y[loc]+yerrup[loc];
  loc = TMath::LocMin(n,y);
  Double_t tmin = y[loc]-yerrdn[loc];
  Double_t ydiff = tmax - tmin;

  ymin = std::max(0.0, tmin - 0.5 * ydiff);
  ymax = std::min(1.4, tmax + 1.0 * ydiff);

  string polN = string(Form("pol%d",smoothPolinDegree));
  // see fit options here: https://root.cern.ch/doc/master/classTGraph.html#aa978c8ee0162e661eae795f6f3a35589
  Double_t xMaxFit = isPromptRate ? 65 : 60;
  TF1 * f1 = new TF1("f1",polN.c_str(),30,xMaxFit);
  TF1 * f2 = new TF1("f2",polN.c_str(),30,50);
  // TF1 * f1 = new TF1("f1","[0] * (x - 25.) + [1]",25,60);
  // TF1 * f2 = new TF1("f2","[0] * (x - 25.) + [1]",30,46);

  Double_t maxslope = isData ? 0.0005 : 0.01;  

  if (isEB) {

    if (isPromptRate) {

      f1->SetParLimits(0,0.0,1.5);
      f1->SetParLimits(1,-0.02,maxslope);
      f2->SetParLimits(0,0.0,1.5);
      f2->SetParLimits(1,-0.02,maxslope);      
      if (smoothPolinDegree > 1) {
	f1->SetParameters(0.95,0.0,0.0);
	f2->SetParameters(0.95,0.0,0.0);
	f1->SetParLimits(2,-0.05,0.05);
	f2->SetParLimits(2,-0.05,0.05);
      } else {
	f1->SetParameters(0.95,0.0);
	f2->SetParameters(0.95,0.0);
      }

    } else {

      f1->SetParLimits(0,0.0,1.0);
      f1->SetParLimits(1,-0.03,maxslope);
      f2->SetParLimits(0,0.0,1.0);
      f2->SetParLimits(1,-0.03,maxslope);
      if (smoothPolinDegree > 1) {
	f1->SetParameters(0.8,0.0,0.0);
	f2->SetParameters(0.8,0.0,0.0);
	f1->SetParLimits(2,-0.05,0.05);
	f2->SetParLimits(2,-0.05,0.05);
      } else {
	f1->SetParameters(0.8,0.0);
	f2->SetParameters(0.8,0.0);
      }

    }

  } else {

    if (isPromptRate) {

      f1->SetParLimits(0,0.0,1.5);
      f1->SetParLimits(1,-0.02,maxslope);
      f2->SetParLimits(0,0.0,1.5);
      f2->SetParLimits(1,-0.02,maxslope);      

      if (smoothPolinDegree > 1) {
	f1->SetParameters(0.8,0.0,0.0);	
	f1->SetParLimits(2,-0.02,0.02);
	f2->SetParameters(0.8,0.0,0.0);	
	f2->SetParLimits(2,-0.02,0.02);
      } else {
	f1->SetParameters(0.8,0.0);
	f2->SetParameters(0.8,0.0); 
      }

    } else {
   
      f1->SetParLimits(0,0.0,1.5);
      f1->SetParLimits(1,-0.03,maxslope);
      f2->SetParLimits(0,0.0,1.5);
      f2->SetParLimits(1,-0.03,maxslope);      

      if (smoothPolinDegree > 1) {
	f1->SetParameters(0.3,0.0,0.0);	
	f1->SetParLimits(2,-0.02,0.02);
	f2->SetParameters(0.3,0.0,0.0);	
	f2->SetParLimits(2,-0.01,0.01);
      } else {
	f1->SetParameters(0.3,0.0);
	f2->SetParameters(0.3,0.0); 
      }

    }

  }

  TFitResultPtr fitres = gr->Fit("f1","EMFRS+"); // fit with straigth line
  TFitResultPtr fitres2 = gr->Fit("f2","EMFRS+"); // fit with straigth line
  TF1 *linefit = gr->GetFunction("f1");
  linefit->SetLineWidth(3);
  Double_t xminfit = 0.0;
  Double_t xmaxfit = 0.0;
  linefit->GetRange(xminfit,xmaxfit);

  TF1 * linefit_p0up = new TF1("linefit_p0up",polN.c_str(),xminfit,xmaxfit);
  linefit_p0up->SetNpx(10000);
  linefit_p0up->SetParameter(0, linefit->GetParameter(0)+nSigmaVarInPlot*linefit->GetParError(0));
  linefit_p0up->SetParameter(1, linefit->GetParameter(1));
  if (smoothPolinDegree > 1) linefit_p0up->SetParameter(2, linefit->GetParameter(2));
  TF1 * linefit_p0dn = new TF1("linefit_p0dn",polN.c_str(),xminfit,xmaxfit);
  linefit_p0dn->SetNpx(10000);
  linefit_p0dn->SetParameter(0, linefit->GetParameter(0)-nSigmaVarInPlot*linefit->GetParError(0));
  linefit_p0dn->SetParameter(1, linefit->GetParameter(1));
  if (smoothPolinDegree > 1) linefit_p0dn->SetParameter(2, linefit->GetParameter(2));

  linefit_p0up->SetLineColor(kGreen+1);
  linefit_p0dn->SetLineColor(kGreen+1);
  linefit_p0up->SetLineWidth(3);
  linefit_p0dn->SetLineWidth(3);

  TF1 *linefit2 = gr->GetFunction("f2");
  linefit2->SetLineWidth(3);
  linefit2->SetLineColor(kBlue);
  Double_t xminfit2 = 0.0;
  Double_t xmaxfit2 = 0.0;
  linefit2->GetRange(xminfit2,xmaxfit2);
  TF1 * linefit2_p0up = new TF1("linefit2_p0up",polN.c_str(),xminfit2,xmaxfit2);
  linefit2_p0up->SetNpx(10000);
  linefit2_p0up->SetParameter(0, linefit2->GetParameter(0)+nSigmaVarInPlot*linefit2->GetParError(0));
  linefit2_p0up->SetParameter(1, linefit2->GetParameter(1));
  if (smoothPolinDegree > 1) linefit2_p0up->SetParameter(2, linefit2->GetParameter(2));
  TF1 * linefit2_p0dn = new TF1("linefit2_p0dn",polN.c_str(),xminfit2,xmaxfit2);
  linefit2_p0dn->SetNpx(10000);
  linefit2_p0dn->SetParameter(0, linefit2->GetParameter(0)-nSigmaVarInPlot*linefit2->GetParError(0));
  linefit2_p0dn->SetParameter(1, linefit2->GetParameter(1));
  if (smoothPolinDegree > 1) linefit2_p0dn->SetParameter(2, linefit2->GetParameter(2));

  linefit2_p0up->SetLineColor(kOrange+2);
  linefit2_p0dn->SetLineColor(kOrange+2);
  linefit2_p0up->SetLineWidth(3);
  linefit2_p0dn->SetLineWidth(3);


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

  gr->SetMarkerStyle(20);
  gr->SetMarkerColor(kBlack);
  gr->SetLineColor(kBlack);
  gr->SetFillColor(kBlack);
  gr->SetLineWidth(2);
  gr->Draw("ap");
  leg.AddEntry(gr,legEntry.c_str(),"PLE");
  //leg.AddEntry(linefit,"fit: p_{0} + p_{1}#upointx","L");
  if (smoothPolinDegree > 1) leg.AddEntry(linefit,"fit: p_{0} + p_{1}#upointx + p_{2}#upointx^{2}","L");
  else leg.AddEntry(linefit,Form("fit: %.2g %s %.2g #upoint x",fitres->Parameter(0),((fitres->Parameter(1) > 0) ? "+":"-"), fabs(fitres->Parameter(1))),"L");
  leg.AddEntry(linefit_p0dn,"offset up/down (1#sigma)","L");
  leg.AddEntry(linefit2,Form("fit: %.2g %s %.2g #upoint x",fitres2->Parameter(0),((fitres2->Parameter(1) > 0) ? "+":"-"), fabs(fitres2->Parameter(1))),"L");
  leg.AddEntry(linefit2_p0dn,"offset up/down (1#sigma)","L");
  leg.Draw("same");
  // draw envelope
  linefit_p0up->Draw("Lsame");
  linefit_p0dn->Draw("Lsame");
  linefit2_p0up->Draw("Lsame");
  linefit2_p0dn->Draw("Lsame");
  // linefit_p0up->Print();
  // Double_t *params = linefit_p0up->GetParameters();
  // cout << "p0 = " << params[0] << "    p1 = " << params[1] << endl;
  // linefit_p0dn->Print();
  // params = linefit_p0dn->GetParameters();
  // cout << "p0 = " << params[0] << "    p1 = " << params[1] << endl;

  gr->GetXaxis()->SetTitleSize(0.05);
  gr->GetXaxis()->SetLabelSize(0.04);
  gr->GetYaxis()->SetTitleOffset(1.1);
  gr->GetYaxis()->SetTitleSize(0.05);
  gr->GetYaxis()->SetLabelSize(0.04);
  gr->GetXaxis()->SetTitle(xAxisName.c_str());
  gr->GetYaxis()->SetTitle(yAxisName.c_str());
  if (setXAxisRangeFromUser) gr->GetXaxis()->SetRangeUser(xmin,xmax);
  if (setYAxisRangeFromUser) gr->GetYaxis()->SetRangeUser(ymin,ymax);

  //  CMS_lumi(canvas,Form("%.1f",lumi));
  if (lumi < 0) CMS_lumi(canvas,"",true,false);
  else CMS_lumi(canvas,Form("%.1f",lumi),true,false);
  setTDRStyle();

  canvas->RedrawAxis("sameaxis");

  canvas->SaveAs((outDir+canvasName+".png").c_str());
  canvas->SaveAs((outDir+canvasName+".pdf").c_str());

  delete canvas;

  if (isData && fitPtr_fitNarrowRange != nullptr) *fitPtr_fitNarrowRange = fitres2;

  return fitres;
  // else return fitres; // for QCD or other MC, it makes much more sense to use graph in full range, because we don't have to worry about prompt lepton rate at high pt
  // also, for QCD the binning is tipically much less granular, so the fit in the narrow range would have just 4 points

}

//=======================================================================

// following part is for the plotting the fake rate

//=====================================================================


void doFakeRateGraphPlots(const string& inputFileName = "", 
			  const string& outDir = "",
			  const string& histPrefix = "fakeRateNumerator_el_vs_pt_granular",
			  const vector<Int_t> ptBinIndexQCD = {1},  // should be a number for each eta bin (if only one is given, use it for all)
			  const vector<Int_t> ptBinIndexEWK = {1},  // should be a number for each eta bin (if only one is given, use it for all)
			  const vector<Int_t> ptBinIndexData = {1}, 
			  const Bool_t showMergedEWK = true,
			  const Double_t inputLuminosity = -1,
			  const Bool_t isEB = true,
			  const string& plotPostFix = "",
			  const Int_t etaBinNumber = 0,
			  const Bool_t scan_vs_eta = false,
			  const Double_t etaLow = 0.0, // used only if scan_vs_eta = true
			  const Double_t etaHigh = 2.5, // used only if scan_vs_eta = true
			  const Bool_t hasSignedEta = true,
			  const Bool_t noDrawQCD = false
			  ) 
{

  gROOT->SetBatch(kTRUE);
  TH1::SetDefaultSumw2(); //all the following histograms will automatically call TH1::Sumw2()                  
  cout << endl;

  Int_t etaBinTH1 = etaBinNumber+1;

  vector<Double_t> ptBinBoundariesData;
  if (ptBinIndexData.size() == 1) {
    if      (ptBinIndexData[0] == 1) ptBinBoundariesData = ptBinBoundariesData_1;
    else if (ptBinIndexData[0] == 2) ptBinBoundariesData = ptBinBoundariesData_2;
  } else {
    if      (ptBinIndexData[etaBinNumber] == 1) ptBinBoundariesData = ptBinBoundariesData_1;
    else if (ptBinIndexData[etaBinNumber] == 2) ptBinBoundariesData = ptBinBoundariesData_2;
  }

  vector<Double_t> ptBinBoundariesEWK;
  if (ptBinIndexEWK.size() == 1) {
    if      (ptBinIndexEWK[0] == 1) ptBinBoundariesEWK = ptBinBoundariesEWK_1;
    else if (ptBinIndexEWK[0] == 2) ptBinBoundariesEWK = ptBinBoundariesEWK_2;
  } else {
    if      (ptBinIndexEWK[etaBinNumber] == 1) ptBinBoundariesEWK = ptBinBoundariesEWK_1;
    else if (ptBinIndexEWK[etaBinNumber] == 2) ptBinBoundariesEWK = ptBinBoundariesEWK_2;
  }

  vector<Double_t> ptBinBoundariesQCD;
  if (ptBinIndexQCD.size() == 1) {
    if      (ptBinIndexQCD[0] == 1) ptBinBoundariesQCD = ptBinBoundariesQCD_1;
    else if (ptBinIndexQCD[0] == 2) ptBinBoundariesQCD = ptBinBoundariesQCD_2;
  } else {
    if      (ptBinIndexQCD[etaBinNumber] == 1) ptBinBoundariesQCD = ptBinBoundariesQCD_1;
    else if (ptBinIndexQCD[etaBinNumber] == 2) ptBinBoundariesQCD = ptBinBoundariesQCD_2;
  }


  TGraphAsymmErrors* fr_data = nullptr;
  TGraphAsymmErrors* fr_data_subEWKMC = nullptr;
  TGraphAsymmErrors* fr_w = nullptr;
  TGraphAsymmErrors* fr_z = nullptr;
  TGraphAsymmErrors* fr_qcd = nullptr;
  TGraphAsymmErrors* fr_ewk = nullptr;

  string detId = isEB ? "EB" : "EE";
  string yrange = isEB ? "0.25,1.4" : "0,1.4";  // range for plotting all graphs
  vector <Double_t> legCoord = {0.15,0.65,0.60,0.9};

  cout << "Will save plots in " << outDir << endl;
  createPlotDirAndCopyPhp(outDir);
  adjustSettings_CMS_lumi(outDir);

  vector<string> processes = {"data", "data_sub", "QCD", "W", "Z"};

  vector<TH1*> hpass;
  vector<TH1*> hntot;
  TH3* h3tmp = nullptr;
  vector<TGraph*> gr;

  TH1* hpass_ewk = nullptr;
  TH1* hntot_ewk = nullptr;

  ///////////////////////////////////////
  // open file with inputs
  //
  TFile* inputFile = new TFile(inputFileName.c_str(),"READ");
  if (!inputFile || inputFile->IsZombie()) {
    cout << "Error: file not opened. Exit" << endl;
    exit(EXIT_FAILURE);
  }
  inputFile->cd();

  UInt_t nBins = 0;
  UInt_t nBinsQCD = ptBinBoundariesQCD.size()-1;  
  UInt_t nBinsEWK = ptBinBoundariesEWK.size()-1;  
  UInt_t nBinsData = ptBinBoundariesData.size()-1;  
  Double_t ptMin = 0.0;
  Double_t ptMax = 0.0;


  for (UInt_t j = 0; j < processes.size(); ++j) {

    string h3Name = Form("%s_%s",histPrefix.c_str(), processes[j].c_str());

    h3tmp = (TH3*) getObjectCloneFromFile(inputFile,h3Name);
    checkNotNullPtr(h3tmp, h3Name);
    h3tmp->SetDirectory(0);

    nBins = h3tmp->GetNbinsX();
    Double_t* ptBins = (Double_t*) h3tmp->GetXaxis()->GetXbins()->GetArray();
    //Double_t* ptBins = ptBins_tmp;
    ptMin = ptBins[0];
    ptMax = ptBins[nBins];

    // do this only once
    if (etaBinNumber == 0 && scan_vs_eta) {

      if (processes[j] == "data_sub") {
      
	// pt vs eta
	TH2D* hpass2D = new TH2D(Form("hpass2D_%s",processes[j].c_str()),"",
				 nBins, ptBins, 
				 h3tmp->GetNbinsY(), (Double_t*) h3tmp->GetYaxis()->GetXbins()->GetArray());
	TH2D* hntot2D = new TH2D(Form("hntot2D_%s",processes[j].c_str()),"",
				 nBins, ptBins, 
				 h3tmp->GetNbinsY(), (Double_t*) h3tmp->GetYaxis()->GetXbins()->GetArray());
	  
	fillTH2fromTH3zrange(hntot2D,h3tmp,1,2);
	fillTH2fromTH3zrange(hpass2D,h3tmp,2,2);
	hpass2D->SetMinimum(0.0);
	hntot2D->SetMinimum(0.0);
	TH2D* hFR2D = (TH2D*) hpass2D->Clone(Form("hFR2D_%s",processes[j].c_str()));
	if (!hFR2D->Divide(hntot2D)) {	  
	  cout << "Error in doing hFR2D->Divide(hntot2D). Exiting" << endl;
	  exit(EXIT_FAILURE);
	}

	string etaYaxisName = hasSignedEta ? "electron #eta" : "electron |#eta|";
	string ptXaxisName = "electron p_{T} [GeV]";

	drawCorrelationPlot(hpass2D, 
			    ptXaxisName,
			    etaYaxisName,
			    "Events (fake-rate numerator)",
			    "events_FRnumerator_data",
			    "", outDir, 1, 1, false,false,false,1,0.12,0.24);
	drawCorrelationPlot(hntot2D, 
			    ptXaxisName,
			    etaYaxisName,
			    "Events (fake-rate denominator)",
			    "events_FRdenominator_data",
			    "", outDir, 1, 1, false,false,false,1,0.12,0.24);

	// hFR2D->SetMinimum(0.0);
	// hFR2D->SetMaximum(1.0);
	drawCorrelationPlot(hFR2D, 
			    ptXaxisName,
			    etaYaxisName,
			    "Fake-rate::0,1.0",
			    "fakeRate_pt_vs_eta_data",
			    "", outDir, 1, 1, false,false,false,1);

      }
      
    }

    // if binning is 0.1,0.2,0.3,... and I look for range 0.1->0.2, search bin with 0.1+epsilon, then bin with 0.2+epsilon and subtract 1 bin from the latter
    // epsilon is a security number to avoid that due to float precision, the edge is assigned to wrong bin (lower boundary should belong to it, upper should not)
    Int_t binYlow  = scan_vs_eta ?  h3tmp->GetYaxis()->FindBin(etaLow+epsilon)       : 0;
    Int_t binYhigh = scan_vs_eta ? (h3tmp->GetYaxis()->FindBin(etaHigh+epsilon) - 1) : (1 + h3tmp->GetNbinsY());  
    // In binYhigh, if scan_vs_eta is true we subtract -1 because the lower edge of a bin belong to that bin
    // Therefore, if we want FR from 0.0 to 0.3 and the histogram is binned like 0.0,0.1,0.2,0.3,0.4,...
    // h3tmp->GetYaxis()->FindBin(0.0) return bin=1, because 0.0 is the lower edge of bin=1 and belongs to it
    // h3tmp->GetYaxis()->FindBin(0.3) would return bin=4 for the same reason, but we just want to sum bins from bin=1 to bin=3 (included)
    // if scan_vs_eta = false, use the integral in all the Y axis range (including underflows and overflows), unless we specify differently

    hpass.push_back( new TH1D(Form("%s_pass",processes[j].c_str()),"", nBins, ptBins) );
    hntot.push_back( new TH1D(Form("%s_ntot",processes[j].c_str()),"", nBins, ptBins) );
    if (hpass_ewk == nullptr && hntot_ewk == nullptr) {
      hpass_ewk = new TH1D("ewk_pass","", nBinsEWK, ptBinBoundariesEWK.data());
      hntot_ewk = new TH1D("ewk_ntot","", nBinsEWK, ptBinBoundariesEWK.data());
    }

    Double_t error = 0.0;
    for (Int_t ix = 1; ix <= h3tmp->GetNbinsX(); ++ix) {
      hpass.back()->SetBinContent(ix,h3tmp->IntegralAndError(ix,ix,binYlow,binYhigh,2,2,error)); // bin 1 along Z for fail, 2 for pass (from 2 to 2 selects only bin 2)
      hpass.back()->SetBinError(ix,error);
      hntot.back()->SetBinContent(ix,h3tmp->IntegralAndError(ix,ix,binYlow,binYhigh,1,2,error)); // bin 1 along Z for fail, 2 for pass (from 1 to 2 selects both bins)
      hntot.back()->SetBinError(ix,error);
    }
    if (processes[j] == "QCD") {
      hpass.back() = hpass.back()->Rebin(nBinsQCD,"",ptBinBoundariesQCD.data());
      hntot.back() = hntot.back()->Rebin(nBinsQCD,"",ptBinBoundariesQCD.data());
    } else if (processes[j] == "W" || processes[j] == "Z") {
      hpass.back() = hpass.back()->Rebin(nBinsEWK,"",ptBinBoundariesEWK.data());
      hntot.back() = hntot.back()->Rebin(nBinsEWK,"",ptBinBoundariesEWK.data());
      hpass_ewk->Add(hpass.back());
      hntot_ewk->Add(hntot.back());
    } else if (processes[j] == "data" || processes[j] == "data_sub") {
      hpass.back() = hpass.back()->Rebin(nBinsData,"",ptBinBoundariesData.data());
      hntot.back() = hntot.back()->Rebin(nBinsData,"",ptBinBoundariesData.data());
    }


    if (processes[j] == "W") {

      fr_w = new TGraphAsymmErrors(hpass.back(), hntot.back(), "cl=0.683 b(1,1) mode");
      //fillFakeRateTH2(fr_pt_eta_w,etaBinTH1,hpass.back(),hntot.back());

    } else if (processes[j] == "Z") {

      fr_z = new TGraphAsymmErrors(hpass.back(), hntot.back(), "cl=0.683 b(1,1) mode");
      //fillFakeRateTH2(fr_pt_eta_z,etaBinTH1,hpass.back(),hntot.back());

    } else if (processes[j] == "data_sub") {
	fr_data_subEWKMC = new TGraphAsymmErrors(hpass.back(), hntot.back(), "cl=0.683 b(1,1) mode"); 
	//fillFakeRateTH2(fr_pt_eta_data,etaBinTH1,hpass.back(),hntot.back());
    } else if (processes[j] == "QCD") {
	fr_qcd           = new TGraphAsymmErrors(hpass.back(), hntot.back(), "cl=0.683 b(1,1) mode"); 
	//fillFakeRateTH2(fr_pt_eta_qcd,etaBinTH1,hpass.back(),hntot.back());
    } else if (processes[j] == "data") {
	fr_data = new TGraphAsymmErrors(hpass.back(), hntot.back(), "cl=0.683 b(1,1) mode");
    } 

  }

  vector<Int_t> colorList = {kBlack, kRed};
  vector<string> legendEntries = {"data", "datasubtr. EWK MC"};
  gr.push_back( fr_data );
  gr.push_back( fr_data_subEWKMC );

  if (not noDrawQCD) {
    gr.push_back( fr_qcd );
    colorList.push_back(kGreen+2);
    legendEntries.push_back("QCD MC");
  }

  fr_ewk = new TGraphAsymmErrors(hpass_ewk, hntot_ewk, "cl=0.683 b(1,1) mode");

  if (showMergedEWK) {
    gr.push_back(fr_ewk);
    colorList.push_back(kBlue);
    legendEntries.push_back("W,Z MC (prompt rate)");
  } else {
    gr.push_back(fr_w);
    gr.push_back(fr_z);
    colorList.push_back(kBlue);
    colorList.push_back(kAzure+2);    
    legendEntries.push_back("W MC (prompt rate)");
    legendEntries.push_back("Z MC (prompt rate)");
  }


  //fillFakeRateTH2(fr_pt_eta_ewk,etaBinTH1,hpass_ewk,hntot_ewk);

  drawGraphCMS(gr, 
	       Form("electron p_{T} [GeV]::%f,%f",ptMin,ptMax), 
	       Form("Fake Rate::%s",yrange.c_str()), 
	       Form("fakerateComparison_%s_%s",detId.c_str(),plotPostFix.c_str()), 
	       outDir, legendEntries, legCoord,inputLuminosity,false,"", colorList);
  
  //////////////////////////////////////////////////////////
  //////////////////////////////////////////////////////////

  // ranges for the fit plot
  // currently overriden inside the fucntion to plot the fit
  // keep for reference
  string yrange_data  = isEB ? "0.5,1.0" : "0.1,0.4";
  string yrange_qcdmc = isEB ? "0.0,1.2" : "0.0,0.8";
  string yrange_w     = isEB ? "0.8,1.2" : "0.4,1.2";
  string yrange_z     = isEB ? "0.8,1.2" : "0.4,1.2";
  string yrange_ewk   = isEB ? "0.8,1.2" : "0.4,1.2";
  vector <Double_t> legCoordFit = {0.12,0.7,0.60,0.9};

  TFitResultPtr ptr_data_fitNarrowRange = nullptr;
  TFitResultPtr ptr_data = fitGraph(fr_data_subEWKMC, isEB, Form("electron p_{T} [GeV]::%f,%f",ptMin,ptMax), Form("Fake Rate::%s",yrange_data.c_str()), Form("fr_data_subEWKMC_%s_%s",detId.c_str(),plotPostFix.c_str()), outDir, "data subtr. EWK MC", legCoordFit,inputLuminosity,true, false, 1.0, &ptr_data_fitNarrowRange);

  // fit is Y=a*X+b
  // bin n.1 is for b (first parameter of pol1), bin n.2 is for a 
  frSmoothParameter_data->SetBinContent(etaBinTH1,1,ptr_data->Parameter(0));
  frSmoothParameter_data->SetBinError(etaBinTH1,1,ptr_data->ParError(0));
  frSmoothParameter_data->SetBinContent(etaBinTH1,2,ptr_data->Parameter(1));
  frSmoothParameter_data->SetBinError(etaBinTH1,2,ptr_data->ParError(1));

  // fit is Y=a*X+b
  // bin n.1 is for b (first parameter of pol1), bin n.2 is for a 
  frSmoothParameter_data_fitNarrowRange->SetBinContent(etaBinTH1,1,ptr_data_fitNarrowRange->Parameter(0));
  frSmoothParameter_data_fitNarrowRange->SetBinError(etaBinTH1,1,ptr_data_fitNarrowRange->ParError(0));
  frSmoothParameter_data_fitNarrowRange->SetBinContent(etaBinTH1,2,ptr_data_fitNarrowRange->Parameter(1));
  frSmoothParameter_data_fitNarrowRange->SetBinError(etaBinTH1,2,ptr_data_fitNarrowRange->ParError(1));


  TFitResultPtr ptr_w = nullptr;
  TFitResultPtr ptr_z = nullptr;
  TFitResultPtr ptr_ewk = nullptr;

  if (showMergedEWK) {

    ptr_ewk = fitGraph(fr_ewk, isEB, Form("electron p_{T} [GeV]::%f,%f",ptMin,ptMax), Form("Prompt Rate::%s",yrange_ewk.c_str()), Form("fr_ewk_%s_%s",detId.c_str(),plotPostFix.c_str()), outDir, "W,Z MC (prompt rate)", legCoordFit,inputLuminosity,false, true);
    // fit is Y=a*X+b
  // bin n.1 is for b (first parameter of pol1), bin n.2 is for a 
    frSmoothParameter_ewk->SetBinContent(etaBinTH1,1,ptr_ewk->Parameter(0));
    frSmoothParameter_ewk->SetBinError(etaBinTH1,1,ptr_ewk->ParError(0));
    frSmoothParameter_ewk->SetBinContent(etaBinTH1,2,ptr_ewk->Parameter(1));
    frSmoothParameter_ewk->SetBinError(etaBinTH1,2,ptr_ewk->ParError(1));

  } else {

    ptr_w = fitGraph(fr_w, isEB, Form("electron p_{T} [GeV]::%f,%f",ptMin,ptMax), Form("Prompt Rate::%s",yrange_w.c_str()), Form("fr_w_%s_%s",detId.c_str(),plotPostFix.c_str()), outDir, "W MC (prompt rate)", legCoordFit,inputLuminosity,false, true);
    // fit is Y=a*X+b
    // bin n.1 is for b (first parameter of pol1), bin n.2 is for a 
    frSmoothParameter_w->SetBinContent(etaBinTH1,1,ptr_w->Parameter(0));
    frSmoothParameter_w->SetBinError(etaBinTH1,1,ptr_w->ParError(0));
    frSmoothParameter_w->SetBinContent(etaBinTH1,2,ptr_w->Parameter(1));
    frSmoothParameter_w->SetBinError(etaBinTH1,2,ptr_w->ParError(1));

    ptr_z = fitGraph(fr_z, isEB, Form("electron p_{T} [GeV]::%f,%f",ptMin,ptMax), Form("Prompt Rate::%s",yrange_z.c_str()), Form("fr_z_%s_%s",detId.c_str(),plotPostFix.c_str()), outDir, "Z MC (prompt rate)", legCoordFit,inputLuminosity,false, true);
    // fit is Y=a*X+b
    // bin n.1 is for b (first parameter of pol1), bin n.2 is for a 
    frSmoothParameter_z->SetBinContent(etaBinTH1,1,ptr_z->Parameter(0));
    frSmoothParameter_z->SetBinError(etaBinTH1,1,ptr_z->ParError(0));
    frSmoothParameter_z->SetBinContent(etaBinTH1,2,ptr_z->Parameter(1));
    frSmoothParameter_z->SetBinError(etaBinTH1,2,ptr_z->ParError(1));

  }

  TFitResultPtr ptr_qcd = nullptr;

  if (not noDrawQCD) {
    
    ptr_qcd = fitGraph(fr_qcd, isEB, Form("electron p_{T} [GeV]::%f,%f",ptMin,ptMax), Form("Fake Rate::%s",yrange_qcdmc.c_str()), Form("fr_qcd_%s_%s",detId.c_str(),plotPostFix.c_str()), outDir, "QCD MC            ", legCoordFit,inputLuminosity,false, false);

    frSmoothParameter_qcd->SetBinContent(etaBinTH1,1,ptr_qcd->Parameter(0));
    frSmoothParameter_qcd->SetBinError(etaBinTH1,1,ptr_qcd->ParError(0));
    frSmoothParameter_qcd->SetBinContent(etaBinTH1,2,ptr_qcd->Parameter(1));
    frSmoothParameter_qcd->SetBinError(etaBinTH1,2,ptr_qcd->ParError(1));

  }
  //////////////////////////////////////////////////////////
  //////////////////////////////////////////////////////////

  inputFile->Close();
  delete inputFile;

}

//================================================================

void makeFakeRateGraphPlotsAndSmoothing(const string& inputFilePath = "www/wmass/13TeV/fake-rate/test/SRtrees_new/fakeRate_eta_pt_granular_mT40_json32fb_signedEta_pt65_fullWMC/el/comb/",
					//const string& outDir_tmp = "SAME", 
					const string& outDir_tmp = "www/wmass/13TeV/fake-rate/electron/FR_graphs/fakeRate_eta_pt_granular_mT40_json32fb_signedEta_pt65_fullWMC/", 
					const string& outfileTag = "mT40_json32fb_signedEta_pt65_fullWMC",
					const string& histPrefix = "fakeRateNumerator_el_vs_etal1_pt_granular",
					const Bool_t isMuon = false, 
					const Bool_t showMergedEWK = true,
					const Bool_t saveToFile = false,  // whether to save is WMass/data/fakerate/ (if false, save in current folder)
					//const TString& etaBinBoundariesList = "-2.5,-2.3,-2.1,-1.9,-1.7,-1.479,-1.2,-0.9,-0.6,-0.3,0.0,0.3,0.6,0.9,1.2,1.479,1.7,1.9,2.1,2.3,2.5",  // important to use dots also for 1.0
					//const TString& etaBinBoundariesList = "0.0,1.0,1.479,1.8,2.1,2.5",
					const TString& etaBinBoundariesList = "-2.5,-2.4,-2.3,-2.2,-2.1,-2.0,-1.9,-1.8,-1.7,-1.566,-1.4442,-1.3,-1.2,-1.1,-1.0,-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.1,1.2,1.3,1.4442,1.566,1.7,1.8,1.9,2.0,2.1,2.2,2.3,2.4,2.5",
					const vector<Int_t> ptBinIndexQCD = {2},  // should be a number for each eta bin (if only one is given, use it for all)
					const vector<Int_t> ptBinIndexEWK = {2},  // should be a number for each eta bin (if only one is given, use it for all)
					const vector<Int_t> ptBinIndexData = {2},  // should be a number for each eta bin (if only one is given, use it for all)
					const Double_t inputLuminosity = 32.2, // -1 in case luminosity should not be printed
					const Bool_t scan_vs_eta = true, // see below
					const Bool_t hasSignedEta = true, // see below
					const Bool_t noDrawQCD = true
			   ) 
{

  // if scan_vs_eta is true, it means there is just one root file (fr_sub_eta_0p0_2p5.root or fr_sub_eta_m2p5_2p5.root)
  // The TH3 inside are pt vs eta vs passID (instead of mt or whatever other variable), where eta has bins of 0.1 from 0 to 2.5
  // Therefore, one can produce FR in whatever binning of eta (given by etaBinBoundariesList)
  // hasSignedEta is used to decide whether the input file has 0p0_2p5 or m2p5_2p5 in its name

  if (isMuon) {
    cout << "Warning: at the moment this macro has hardcoded parts for electrons. Usage with muons must be implemented! Exit." << endl;
    exit(EXIT_FAILURE);
  }


  TObjArray* array = etaBinBoundariesList.Tokenize(",");
  vector<Double_t> etaBoundaries;
  vector<string> etaBoundariesString;

  for (Int_t j = 0; j < array->GetEntries(); j++) {
    TString str = ((TObjString *) array->At(j))->String();
    etaBoundariesString.push_back(string(str.Data()));
    etaBoundaries.push_back(stod(etaBoundariesString.back()));
    size_t pos_dot = etaBoundariesString.back().find(".");  // find position of dot
    size_t pos_sign = etaBoundariesString.back().find("-");  // find position of minus sign
    etaBoundariesString.back().replace(pos_dot,1,"p"); // replace dot with p
    if (pos_sign != string::npos) etaBoundariesString.back().replace(pos_sign,1,"m"); // replace dot with p
  }


  cout << "Eta bins boundaries: ";
  for (UInt_t i = 0; i < etaBoundaries.size(); i++) {
    cout << etaBoundaries[i] << " ";
  }
  cout << endl;
  cout << "Eta bins boundaries (string): ";
  for (UInt_t i = 0; i < etaBoundariesString.size(); i++) {
    cout << etaBoundariesString[i] << " ";
  }
  cout << endl;

  etaBoundariesGlobal = etaBoundaries;
  Int_t NetaBins = (Int_t) etaBoundaries.size() - 1;
  vector<Double_t> parNumberBoundaries = {-0.5,0.5,1.5}; // bin center is 0 or 1 for a 2 parameter fit (we used a straight line to fit FR, so we have 2 parameters)
  Int_t Nparam = (Int_t) parNumberBoundaries.size() - 1;

  frSmoothParameter_data = new TH2D("frSmoothParameter_data","straight line fit parameters (offset, slope) vs eta",NetaBins,etaBoundaries.data(),Nparam,parNumberBoundaries.data());
  frSmoothParameter_data_fitNarrowRange = new TH2D("frSmoothParameter_data_fitNarrowRange","straight line fit parameters (offset, slope) vs eta",NetaBins,etaBoundaries.data(),Nparam,parNumberBoundaries.data());
  frSmoothParameter_qcd = new TH2D("frSmoothParameter_qcd","straight line fit parameters (offset, slope) vs eta",NetaBins,etaBoundaries.data(),Nparam,parNumberBoundaries.data());
  frSmoothParameter_w = new TH2D("frSmoothParameter_w","straight line fit parameters (offset, slope) vs eta",NetaBins,etaBoundaries.data(),Nparam,parNumberBoundaries.data());
  frSmoothParameter_z = new TH2D("frSmoothParameter_z","straight line fit parameters (offset, slope) vs eta",NetaBins,etaBoundaries.data(),Nparam,parNumberBoundaries.data());
  frSmoothParameter_ewk = new TH2D("frSmoothParameter_ewk","straight line fit parameters (offset, slope) vs eta",NetaBins,etaBoundaries.data(),Nparam,parNumberBoundaries.data());

  string outDir = (outDir_tmp == "SAME") ? (inputFilePath + "FR_graphs/") : outDir_tmp;

  for (Int_t i = 0; i < NetaBins; i++) {

    string etabinPostFix = "eta_" + etaBoundariesString[i] + "_" + etaBoundariesString[i+1];
    //string fr_fQCD_file = "fr_sub_" + etabinPostFix + "_fQCD.root";

    string specialEtaBinPostFix = "";
    if (scan_vs_eta) {
      if (hasSignedEta) specialEtaBinPostFix = "eta_m2p5_2p5";
      else              specialEtaBinPostFix = "eta_0p0_2p5";
    }

    string fr_fQCD_file = "fr_sub_" + (scan_vs_eta ? specialEtaBinPostFix : etabinPostFix) + ".root";

    //Bool_t isEB = (etaBoundaries[i] < 1.479) ? true : false; 
    Bool_t isEB = false;
    if (etaBoundaries[i] < 1.479 && etaBoundaries[i] >= 0) isEB = true; 
    if (etaBoundaries[i] >= -1.479 && etaBoundaries[i] <= 0) isEB = true; 

    doFakeRateGraphPlots(inputFilePath + fr_fQCD_file,
			 outDir,
			 histPrefix,
			 ptBinIndexQCD,
			 ptBinIndexEWK,
			 ptBinIndexData,
			 showMergedEWK,
			 inputLuminosity,
			 isEB,
			 etabinPostFix,
			 i,
			 scan_vs_eta,etaBoundaries[i],etaBoundaries[i+1],hasSignedEta,
			 noDrawQCD); 

  }

  cout << "etaBoundariesGlobal.size()-1, etaBoundariesGlobal.data() " << etaBoundariesGlobal.size()-1 << "   " << etaBoundariesGlobal.data() << endl;

  // following works only if you are in the CMSSW_BASE area where you have CMGTools/WMass/...
  char* cmsswPath;
  cmsswPath = getenv ("CMSSW_BASE");
  if (cmsswPath == NULL) {
    cout << "Error in makeFakeRateSmoothing(): environment variable CMSSW_BASE not found. Exit" << endl;
    exit(EXIT_FAILURE);
  }
  char* currentPath_ptr;
  currentPath_ptr = getenv ("PWD");
  string currentPath = string(currentPath_ptr);

  string frSmoothFileName = "";

  if (saveToFile && currentPath.find("src/CMGTools/WMass") != string::npos) {
    frSmoothFileName += Form("%s/src/CMGTools/WMass/data/fakerate/",cmsswPath);
  } else {
    if (not saveToFile) {
      cout << endl;
      cout << endl;
      cout << "##############" << endl;
      cout << "### WARNING: " << endl;
      cout << "### Not saving smoothed FR fit parameters to file in CMGTools/WMass/data/fakerate/ because saveToFile option is false." << endl;
      cout << "### Output file will be produced in current directory." << endl;
      cout << "##############" << endl;
      cout << endl;
    } else {
      cout << "Warning: current working path doesn't match 'src/CMGTools/WMass'." << endl;
      cout << "Output file will be produced in current directory" << endl;
    }
  }

  frSmoothFileName += (isMuon ? "fakeRateSmoothed_mu" : "fakeRateSmoothed_el");
  if (outfileTag != "") frSmoothFileName = frSmoothFileName + "_" + outfileTag;
  frSmoothFileName = frSmoothFileName + ".root";

  TFile* frSmoothFile = new TFile(frSmoothFileName.c_str(),"RECREATE");
  if (!frSmoothFile || frSmoothFile->IsZombie()) {
    cout << "Error: file not opened. Exit" << endl;
    exit(EXIT_FAILURE);
  }

  frSmoothFile->cd();

  // fill TH2 (pt vs |eta|) with smoothed fake rate
  string etaYaxisName = hasSignedEta ? "electron #eta" : "electron |#eta|";
  
  TH2D* fr_pt_eta_data = new TH2D("fr_pt_eta_data",Form("fake rate for data;electron p_{T};%s",etaYaxisName.c_str()), 
				  70, 30, 65, NetaBins, etaBoundaries.data());
  TH2D* fr_pt_eta_data_fitNarrowRange = new TH2D("fr_pt_eta_data_fitNarrowRange",Form("fake rate for data;electron p_{T};%s",etaYaxisName.c_str()), 
				  70, 30, 65, NetaBins, etaBoundaries.data());
  TH2D* fr_pt_eta_qcd  = new TH2D("fr_pt_eta_qcd",Form("fake rate for QCD MC;electron p_{T};%s",etaYaxisName.c_str()), 
				  70, 30, 65, NetaBins, etaBoundaries.data());
  TH2D* fr_pt_eta_w    = new TH2D("fr_pt_eta_w",Form("prompt rate for W MC;electron p_{T};%s",etaYaxisName.c_str()), 
				  70, 30, 65, NetaBins, etaBoundaries.data());
  TH2D* fr_pt_eta_z    = new TH2D("fr_pt_eta_z",Form("prompt rate for Z MC;electron p_{T};%s",etaYaxisName.c_str()), 
				  70, 30, 65, NetaBins, etaBoundaries.data());
  TH2D* fr_pt_eta_ewk  = new TH2D("fr_pt_eta_ewk",Form("prompt rate for W,Z MC;electron p_{T};%s",etaYaxisName.c_str()), 
				  70, 30, 65, NetaBins, etaBoundaries.data());

  cout << "Creating TH2 fr_pt_eta_* with smoothed fake or prompt rate (pT vs |eta|)" << endl;
  cout << endl;
  fillFakeRateTH2smooth(fr_pt_eta_data, frSmoothParameter_data);
  fillFakeRateTH2smooth(fr_pt_eta_data_fitNarrowRange, frSmoothParameter_data_fitNarrowRange);
  if (not noDrawQCD) fillFakeRateTH2smooth(fr_pt_eta_qcd, frSmoothParameter_qcd);
  if (showMergedEWK) {
    fillFakeRateTH2smooth(fr_pt_eta_ewk, frSmoothParameter_ewk);
  } else {
    fillFakeRateTH2smooth(fr_pt_eta_w, frSmoothParameter_w);
    fillFakeRateTH2smooth(fr_pt_eta_z, frSmoothParameter_z);
  }

  // draw some TH2
  drawCorrelationPlot(fr_pt_eta_data, 
		      fr_pt_eta_data->GetXaxis()->GetTitle(),
		      fr_pt_eta_data->GetYaxis()->GetTitle(),
		      "fake rate",
		      "smoothed_fakeRate_pt_vs_eta_data",
		      "", outDir, 1,1, false,false,false,1);
  drawCorrelationPlot(fr_pt_eta_data, 
		      fr_pt_eta_data->GetXaxis()->GetTitle(),
		      fr_pt_eta_data->GetYaxis()->GetTitle(),
		      "fake rate::0,1.0",
		      "smoothed_fakeRate_pt_vs_eta_data_wideZaxis",
		      "", outDir, 1,1, false,false,false,1);
  drawCorrelationPlot(fr_pt_eta_data_fitNarrowRange, 
		      fr_pt_eta_data_fitNarrowRange->GetXaxis()->GetTitle(),
		      fr_pt_eta_data_fitNarrowRange->GetYaxis()->GetTitle(),
		      "fake rate::0,1.0",
		      "smoothed_fakeRate_pt_vs_eta_data_fitNarrowRange",
		      "", outDir, 1,1, false,false,false,1);
  if (showMergedEWK) {
    drawCorrelationPlot(fr_pt_eta_ewk, 
			fr_pt_eta_ewk->GetXaxis()->GetTitle(),
			fr_pt_eta_ewk->GetYaxis()->GetTitle(),
			"prompt rate",
			"smoothed_promptRate_pt_vs_eta_ewk",
			"", outDir, 1,1, false,false,false,1);
  } else {
    drawCorrelationPlot(fr_pt_eta_w, 
			fr_pt_eta_w->GetXaxis()->GetTitle(),
			fr_pt_eta_w->GetYaxis()->GetTitle(),
			"prompt rate",
			"smoothed_promptRate_pt_vs_eta_w",
			"", outDir, 1,1, false,false,false,1);
    drawCorrelationPlot(fr_pt_eta_z, 
			fr_pt_eta_z->GetXaxis()->GetTitle(),
			fr_pt_eta_z->GetYaxis()->GetTitle(),
			"prompt rate",
			"smoothed_promptRate_pt_vs_eta_z",
			"", outDir, 1,1, false,false,false,1);
  }
  if (not noDrawQCD) 
    drawCorrelationPlot(fr_pt_eta_qcd, 
			fr_pt_eta_qcd->GetXaxis()->GetTitle(),
			fr_pt_eta_qcd->GetYaxis()->GetTitle(),
			"fake rate",
			"smoothed_fakeRate_pt_vs_eta_qcd",
			"", outDir, 1,1, false,false,false,1);


  cout << endl;
  cout << "Plotting TH2 with relative uncertainty on FR parameters" << endl;
  plotFRparamRelUncertainty(frSmoothParameter_data,outDir,fr_pt_eta_data->GetYaxis()->GetTitle(),"0 offset : 1 slope","relative uncertainty", "smoothed_fakeRate_pt_vs_eta_data_relUnc");
  plotFRparamRelUncertainty(frSmoothParameter_data_fitNarrowRange,outDir,fr_pt_eta_data->GetYaxis()->GetTitle(),"0 offset : 1 slope","relative uncertainty", "smoothed_fakeRate_pt_vs_eta_data_fitNarrowRange_relUnc");

  // parameters of linear fit
  cout << endl;
  cout << "Writing TH2 frSmoothParameter_* with linear fit parameters in file" << endl;
  frSmoothParameter_data->Write();
  frSmoothParameter_data_fitNarrowRange->Write();
  if (not noDrawQCD) frSmoothParameter_qcd->Write();
  if (showMergedEWK) {
    frSmoothParameter_ewk->Write();
  } else{
    frSmoothParameter_w->Write();
    frSmoothParameter_z->Write();
  }
  // fake or prompt rate points (no errors)
  cout << "Writing TH2 fr_pt_eta_* with smoothed fake or prompt rate in file" << endl;
  fr_pt_eta_data->Write();
  fr_pt_eta_data_fitNarrowRange->Write();
  if (not noDrawQCD) fr_pt_eta_qcd->Write();
  if (showMergedEWK) {
    fr_pt_eta_ewk->Write();
  } else {
    fr_pt_eta_w->Write();
    fr_pt_eta_z->Write();
  }

  frSmoothFile->Close();


  cout << endl;
  cout << endl;
  cout << "Created file " << frSmoothFileName << endl;
  system(Form("cp %s %s",frSmoothFileName.c_str(),outDir.c_str()));
  cout << "File also copied in " << outDir << endl;
  cout << endl;


  delete frSmoothFile;

}
