#include "../interface/utility.h"

using namespace std;

// the core of this macro is makeFakeRateGraphPlotsAndSmoothing(), which is at the bottom of this code and calls all the rest

// the idea is to get the files with the fake rate graphs and plot them together (plots produced with the fake rate script suck ;-) )
// you need to pass:
// inputFilePath: path to root file with fake rate graphs ( /path/to/some/where/, which contains the file(s) for the different eta bins)
// isMuon: a boolean flag to decide if you have muons, or electrons (but now there are some hardcoded pieces that suppose you use electrons :( )
// etaBinBoundariesList: a string with eta bin boundaries separated by commas (no space), e.g.: "0.0,1.479,2.1,2.5" (please always use at least one decimal, like 1.0)
// saveToFile: boolean flag to decide whether to save smoothed FR fit parameters in file (you might just want to do plots to see how they look)
// inputLuminosity: luminosity to be shown in the plot (a negative value doens't print any number, just '13 TeV' in the canvas)
// inputFilePathForQCD_tmp: if empty, take QCD from same file as data, otherwise use this path (the reason is that you might want to use a different pt
//   binning for QCD because you have much less statistics and in this case the graphs are in another path)


//=======================================================================

// following part is for the plotting the fake rate

//=====================================================================


void doFakeRateGraphPlots(const string& outputDIR_tmp = "./", 
			  const string& inputFileName_tmp = "wmass_varhists.root", 
			  const Bool_t isMuon = false, 
			  const Bool_t isEB = true,
			  const Double_t inputLuminosity = -1,
			  const string& plotPostFix = "",
			  const string& inputFileNameForQCD = ""
			  ) 
{
  
  string outputDIR = outputDIR_tmp + "FR_graphs/";
  string inputFileName = inputFileName_tmp;

  createPlotDirAndCopyPhp(outputDIR);

  gROOT->SetBatch(kTRUE);
  TH1::SetDefaultSumw2(); //all the following histograms will automatically call TH1::Sumw2()                  
  cout << endl;

  TFile* inputFile = new TFile(inputFileName.c_str(),"READ");
  if (!inputFile || inputFile->IsZombie()) {
    cout << "Error: file not opened. Exit" << endl;
    exit(EXIT_FAILURE);
  }

  inputFile->cd();

  TFile* inputFileForQCD = NULL;
  if (inputFileNameForQCD != "") {
    inputFileForQCD = new TFile(inputFileNameForQCD.c_str(),"READ");
    if (!inputFileForQCD || inputFileForQCD->IsZombie()) {
      cout << "Error: file not opened. Exit" << endl;
      exit(EXIT_FAILURE);
    }
    
  }

  TGraphAsymmErrors* fr_data_subEWKpromptRate = NULL; // FR obtained computing it in 2 mT regions to remove prompt lepton rate
  TGraphAsymmErrors* fr_data_orig = NULL;  // FR before EWK subraction
  TGraphAsymmErrors* fr_data_subEWKMC = NULL;  // FR from data after subtracting EWK from MC
  TGraphAsymmErrors* fr_qcdmc = NULL;  // FR from QCD MC

  // tmp plot to be removed to adjust settings in CMS_lumi
  TH1D* htmp1 = new TH1D("htmp1","",1,0,1);
  TH1D* htmp2 = new TH1D("htmp2","",1,0,1);
  htmp1->Fill(0.5);
  htmp2->Fill(0.5);
  vector<TH1*> htmpVec; htmpVec.push_back(htmp2);
  drawTH1dataMCstack(htmp1, htmpVec, "variable", "Events", "tmpToBeRemoved", outputDIR);
  system(("rm " + outputDIR + "*tmpToBeRemoved*").c_str());

  string detId = isEB ? "EB" : "EE";

  vector<TGraph*> graphList;  // first element is the one on top of the stack
  vector<string> graphLegend;
  vector <Double_t> legCoord = {0.12,0.65,0.60,0.9};

  string graphPrefix = isEB ? "FullSel_looseID_vs_pt_granular" : "FullSel_mediumID_vs_pt_granular";
  string graphPrefixQCD = "";
  if (inputFileNameForQCD == "") graphPrefixQCD = graphPrefix;
  else graphPrefixQCD = isEB ? "FullSel_looseID_vs_pt_coarse" : "FullSel_mediumID_vs_pt_coarse";

  fr_data_subEWKMC         = (TGraphAsymmErrors*) getGraphCloneFromFile(inputFile, graphPrefix + "_data_2d_prefit_sub_graph", "", inputFileName);
  fr_data_orig             = (TGraphAsymmErrors*) getGraphCloneFromFile(inputFile, graphPrefix + "_trkmtfix_data_prefit", "", inputFileName);
  if (inputFileNameForQCD == "") 
    fr_qcdmc               = (TGraphAsymmErrors*) getGraphCloneFromFile(inputFile, graphPrefix + "_trkmtfix_QCD_prefit", "", inputFileName);
  else { 
    inputFileForQCD->cd();
    fr_qcdmc               = (TGraphAsymmErrors*) getGraphCloneFromFile(inputFileForQCD, graphPrefixQCD + "_trkmtfix_QCD_prefit", "", inputFileNameForQCD);
  }
  // fr_data_subEWKpromptRate = (TGraphAsymmErrors*) getGraphCloneFromFile(inputFile, graphPrefix + "_trkmtfix_data_fqcd", "", inputFileName);
  
  checkNotNullPtr(fr_data_subEWKMC,"fr_data_subEWKMC");
  checkNotNullPtr(fr_data_orig,"fr_data_orig");
  checkNotNullPtr(fr_qcdmc,"fr_qcdmc");
  // checkNotNullPtr(fr_data_subEWKpromptRate,"fr_data_subEWKpromptRate");
  
  graphList.push_back(fr_data_orig);
  graphList.push_back(fr_data_subEWKMC);
  graphList.push_back(fr_qcdmc);
  // graphList.push_back(fr_data_subEWKpromptRate);

  graphLegend.push_back("data");
  graphLegend.push_back("data subtr. EWK MC");
  graphLegend.push_back("QCD MC");
  // graphLegend.push_back("data subtr. prompt rate");

  string yrange = isEB ? "0.2,1.3" : "0,0.8";

  drawGraphCMS(graphList,"electron p_{T} [GeV]",Form("Fake Rate::%s",yrange.c_str()),Form("fakerateComparison_%s_%s",detId.c_str(),plotPostFix.c_str()),outputDIR,graphLegend,legCoord,inputLuminosity);

}


//============================================

// following part is for the smoothing of the fake rate

//============================================

TFitResultPtr fitGraph(TGraph* gr = NULL, 
		       const Bool_t isEB = true,
		       const string& xAxisNameTmp = "xAxis", 
		       const string& yAxisNameTmp = "yAxis", 
		       const string& canvasName = "default",
		       const string& outputDIR = "./",
		       const string& legEntry = "",
		       const vector<Double_t>& legCoord = {0.5,0.15,0.9,0.35},
		       const Double_t lumi = -1.0,
		       const Bool_t isData = true
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

  // see fit options here: https://root.cern.ch/doc/master/classTGraph.html#aa978c8ee0162e661eae795f6f3a35589
  TF1 * f1 = new TF1("f1","pol1",25,60);
  TF1 * f2 = new TF1("f2","pol1",30,46);
  // TF1 * f1 = new TF1("f1","[0] * (x - 25.) + [1]",25,60);
  // TF1 * f2 = new TF1("f2","[0] * (x - 25.) + [1]",30,46);
  if (isEB) {
    f1->SetParameters(0.8,0.0);
    f1->SetParLimits(0,0.65,0.9);
    f1->SetParLimits(1,-0.02,0.02);
    f2->SetParameters(0.8,0.0);
    f2->SetParLimits(0,0.5,0.9);
    f2->SetParLimits(1,-0.02,0.02);
  } else {
    f1->SetParameters(0.3,0.0);	
    f1->SetParLimits(0,0.15,0.4);
    f1->SetParLimits(1,-0.005,0.005);
    f2->SetParameters(0.3,0.0);	
    f2->SetParLimits(0,0.15,0.4);
    f2->SetParLimits(1,-0.005,0.005);
  }

  TFitResultPtr fitres = gr->Fit("f1","EMFRS+"); // fit with straigth line
  TFitResultPtr fitres2 = gr->Fit("f2","EMFRS+"); // fit with straigth line
  TF1 *linefit = gr->GetFunction("f1");
  linefit->SetLineWidth(3);
  Double_t xminfit = 0.0;
  Double_t xmaxfit = 0.0;
  linefit->GetRange(xminfit,xmaxfit);

  TF1 * linefit_p0up = new TF1("linefit_p0up","pol1",xminfit,xmaxfit);
  linefit_p0up->SetNpx(10000);
  linefit_p0up->SetParameter(0, linefit->GetParameter(0)+2*linefit->GetParError(0));
  linefit_p0up->SetParameter(1, linefit->GetParameter(1));
  TF1 * linefit_p0dn = new TF1("linefit_p0dn","pol1",xminfit,xmaxfit);
  linefit_p0dn->SetNpx(10000);
  linefit_p0dn->SetParameter(0, linefit->GetParameter(0)-2*linefit->GetParError(0));
  linefit_p0dn->SetParameter(1, linefit->GetParameter(1));

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
  TF1 * linefit2_p0up = new TF1("linefit2_p0up","pol1",xminfit2,xmaxfit2);
  linefit2_p0up->SetNpx(10000);
  linefit2_p0up->SetParameter(0, linefit2->GetParameter(0)+2*linefit2->GetParError(0));
  linefit2_p0up->SetParameter(1, linefit2->GetParameter(1));
  TF1 * linefit2_p0dn = new TF1("linefit2_p0dn","pol1",xminfit2,xmaxfit2);
  linefit2_p0dn->SetNpx(10000);
  linefit2_p0dn->SetParameter(0, linefit2->GetParameter(0)-2*linefit2->GetParError(0));
  linefit2_p0dn->SetParameter(1, linefit2->GetParameter(1));

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
  leg.AddEntry(linefit,"fit: p_{0} + p_{1}#upointx","L");
  leg.AddEntry(linefit_p0dn,"p_{0} up/down (2#sigma)","L");
  leg.AddEntry(linefit2,"fit narrow range","L");
  leg.AddEntry(linefit2_p0dn,"p_{0} up/down (2#sigma)","L");
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

  canvas->SaveAs((outputDIR+canvasName+".png").c_str());
  canvas->SaveAs((outputDIR+canvasName+".pdf").c_str());

  if (isData) return fitres2;  // return fit in shorter range
  else return fitres; // for QCD, it makes much more sense to use graph in full range, because we don't have to worry about prompt lepton rate at high pt
  // also, for QCD the binning is tipically much less granular, so the fit in the narrow range would have just 4 points

}

//============================================

void doFakeRateSmoothing(const string& outputDIR_tmp = "./", 
			 const string& inputFileName_tmp = "wmass_varhists.root", 
			 const Bool_t isMuon = false, 
			 const Bool_t isEB = true,
			 const Double_t inputLuminosity = -1,
			 const string& plotPostFix = "",
			 const string& inputFileNameForQCD = "",
			 TH2D* h2_fitParVsEta_data = NULL,
			 TH2D* h2_fitParVsEta_qcd = NULL,
			 const Int_t etaBinNumber = 1
			 ) 
{
  
  string outputDIR = outputDIR_tmp + "FR_graphs/";
  string inputFileName = inputFileName_tmp;

  createPlotDirAndCopyPhp(outputDIR);

  gROOT->SetBatch(kTRUE);
  TH1::SetDefaultSumw2(); //all the following histograms will automatically call TH1::Sumw2()                  
  cout << endl;

  TFile* inputFile = new TFile(inputFileName.c_str(),"READ");
  if (!inputFile || inputFile->IsZombie()) {
    cout << "Error: file not opened. Exit" << endl;
    exit(EXIT_FAILURE);
  }

  inputFile->cd();

  TFile* inputFileForQCD = NULL;
  if (inputFileNameForQCD != "") {
    inputFileForQCD = new TFile(inputFileNameForQCD.c_str(),"READ");
    if (!inputFileForQCD || inputFileForQCD->IsZombie()) {
      cout << "Error: file not opened. Exit" << endl;
      exit(EXIT_FAILURE);
    }
    
  }

  TGraphAsymmErrors* fr_data_subEWKpromptRate = NULL; // FR obtained computing it in 2 mT regions to remove prompt lepton rate
  TGraphAsymmErrors* fr_data_orig = NULL;  // FR before EWK subraction
  TGraphAsymmErrors* fr_data_subEWKMC = NULL;  // FR from data after subtracting EWK from MC
  TGraphAsymmErrors* fr_qcdmc = NULL;  // FR from QCD MC

  // tmp plot to be removed to adjust settings in CMS_lumi
  TH1D* htmp1 = new TH1D("htmp1","",1,0,1);
  TH1D* htmp2 = new TH1D("htmp2","",1,0,1);
  htmp1->Fill(0.5);
  htmp2->Fill(0.5);
  vector<TH1*> htmpVec; htmpVec.push_back(htmp2);
  drawTH1dataMCstack(htmp1, htmpVec, "variable", "Events", "tmpToBeRemoved", outputDIR);
  system(("rm " + outputDIR + "*tmpToBeRemoved*").c_str());

  string detId = isEB ? "EB" : "EE";

  // hardcoded name of Tgraphs inside file :(
  string graphPrefix = isEB ? "FullSel_looseID_vs_pt_granular" : "FullSel_mediumID_vs_pt_granular";
  string graphPrefixQCD = "";
  if (inputFileNameForQCD == "") graphPrefixQCD = graphPrefix;
  else graphPrefixQCD = isEB ? "FullSel_looseID_vs_pt_coarse" : "FullSel_mediumID_vs_pt_coarse";

  fr_data_subEWKMC           = (TGraphAsymmErrors*) getGraphCloneFromFile(inputFile, graphPrefix + "_data_2d_prefit_sub_graph", "", inputFileName);
  // fr_data_subEWKpromptRate   = (TGraphAsymmErrors*) getGraphCloneFromFile(inputFile, graphPrefix + "_trkmtfix_data_fqcd", "", inputFileName);
  // fr_data_orig               = (TGraphAsymmErrors*) getGraphCloneFromFile(inputFile, graphPrefix + "_trkmtfix_data_prefit", "", inputFileName);
  if (inputFileNameForQCD == "") 
    fr_qcdmc               = (TGraphAsymmErrors*) getGraphCloneFromFile(inputFile, graphPrefix + "_trkmtfix_QCD_prefit", "", inputFileName);
  else { 
    inputFileForQCD->cd();
    fr_qcdmc               = (TGraphAsymmErrors*) getGraphCloneFromFile(inputFileForQCD, graphPrefixQCD + "_trkmtfix_QCD_prefit", "", inputFileNameForQCD);
  }
      
  //checkNotNullPtr(fr_data_subEWKpromptRate,"fr_data_subEWKpromptRate");
  checkNotNullPtr(fr_data_subEWKMC,"fr_data_subEWKMC");
  // checkNotNullPtr(fr_data_orig,"fr_data_orig");
  checkNotNullPtr(fr_qcdmc,"fr_qcdmc");

  string yrange_data = isEB ? "0.5,1.0" : "0.2,0.4";
  string yrange_qcdmc = isEB ? "0.3,1.2" : "0.0,0.6";
  vector <Double_t> legCoord = {0.12,0.7,0.60,0.9};

  TFitResultPtr ptr_data = fitGraph(fr_data_subEWKMC, isEB, "electron p_{T} [GeV]", Form("Fake Rate::%s",yrange_data.c_str()), Form("fr_data_subEWKMC_%s_%s",detId.c_str(),plotPostFix.c_str()), outputDIR, "data subtr. EWK MC", legCoord,inputLuminosity,true);

  // fit is Y=a*X+b
  // bin n.1 is for b (first parameter of pol1), bin n.2 is for a 
  h2_fitParVsEta_data->SetBinContent(etaBinNumber,1,ptr_data->Parameter(0));
  h2_fitParVsEta_data->SetBinError(etaBinNumber,1,ptr_data->ParError(0));
  h2_fitParVsEta_data->SetBinContent(etaBinNumber,2,ptr_data->Parameter(1));
  h2_fitParVsEta_data->SetBinError(etaBinNumber,2,ptr_data->ParError(1));

  TFitResultPtr ptr_qcd = fitGraph(fr_qcdmc, isEB, "electron p_{T} [GeV]", Form("Fake Rate::%s",yrange_qcdmc.c_str()), Form("fr_qcdmc_%s_%s",detId.c_str(),plotPostFix.c_str()), outputDIR, "QCD MC            ", legCoord,inputLuminosity,false);

  h2_fitParVsEta_qcd->SetBinContent(etaBinNumber,1,ptr_qcd->Parameter(0));
  h2_fitParVsEta_qcd->SetBinError(etaBinNumber,1,ptr_qcd->ParError(0));
  h2_fitParVsEta_qcd->SetBinContent(etaBinNumber,2,ptr_qcd->Parameter(1));
  h2_fitParVsEta_qcd->SetBinError(etaBinNumber,2,ptr_qcd->ParError(1));

}

//================================================================

void makeFakeRateGraphPlotsAndSmoothing(const string& inputFilePath = "www/wmass/13TeV/fake-rate/test/SRtrees_new/hltID_mediumWP_36fb_PUTrgSF_trkmtfix_0_50_50_120_EE_fineBinning/el/comb/", 
					const Bool_t isMuon = false, 
					const TString& etaBinBoundariesList = "0.0,1.479,2.1,2.5",  // important to use dots also for 1.0
					const Double_t inputLuminosity = -1,
					const Bool_t saveToFile = false,
					const string& inputFilePathForQCD_tmp = ""
			   ) 
{

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
    etaBoundariesString.back().replace(pos_dot,1,"p"); // replace dot with p
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


  Int_t NetaBins = (Int_t) etaBoundaries.size() - 1;
  vector<Double_t> parNumberBoundaries = {-0.5,0.5,1.5}; // bin center is 0 or 1 for a 2 parameter fit (we used a straight line to fit FR, so we have 2 parameters)
  Int_t Nparam = (Int_t) parNumberBoundaries.size() - 1;

  TH2D* frSmoothParameter_data = new TH2D("frSmoothParameter_data","straight line fit parameters (offset, slope) vs eta",NetaBins,etaBoundaries.data(),Nparam,parNumberBoundaries.data());
  TH2D* frSmoothParameter_qcd = new TH2D("frSmoothParameter_qcd","straight line fit parameters (offset, slope) vs eta",NetaBins,etaBoundaries.data(),Nparam,parNumberBoundaries.data());

  string outputDIR = inputFilePath;
  string inputFilePathForQCD = (inputFilePathForQCD_tmp == "") ? inputFilePath : inputFilePathForQCD_tmp;

  for (Int_t i = 0; i < NetaBins; i++) {

    string etabinPostFix = "eta_" + etaBoundariesString[i] + "_" + etaBoundariesString[i+1];
    string fr_fQCD_file = "fr_sub_" + etabinPostFix + "_fQCD.root";

    Bool_t isEB = (etaBoundaries[i] < 1.479) ? true : false; 
    doFakeRateGraphPlots(outputDIR,inputFilePath+fr_fQCD_file,isMuon,isEB,inputLuminosity,etabinPostFix,inputFilePathForQCD+fr_fQCD_file);

    doFakeRateSmoothing(outputDIR,inputFilePath+fr_fQCD_file,isMuon,isEB,inputLuminosity,etabinPostFix,inputFilePathForQCD+fr_fQCD_file,frSmoothParameter_data,frSmoothParameter_qcd,i+1);  // pass i+1 as bin number because TH2 binning numbering starts from 1

  }


  if (saveToFile) {

    // following works only if you are in the CMSSW_BASE area where you have CMGTools/MonoXAnalysis/...
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
    if (currentPath.find("src/CMGTools/MonoXAnalysis") != string::npos) {
      frSmoothFileName += Form("%s/src/CMGTools/MonoXAnalysis/data/fakerate/",cmsswPath);
    } else {
      cout << "Warning: current working path doesn't match 'src/CMGTools/MonoXAnalysis/data/fakerate/'." << endl;
      cout << "Output file will be produced in current directory" << endl;
    }
    frSmoothFileName += (isMuon ? "fakeRateSmoothed_mu.root" : "fakeRateSmoothed_el.root");
    cout << endl;
    cout << endl;
    cout << "Created file " << frSmoothFileName << endl;
    cout << endl;

    TFile* frSmoothFile = new TFile(frSmoothFileName.c_str(),"RECREATE");
    if (!frSmoothFile || frSmoothFile->IsZombie()) {
      cout << "Error: file not opened. Exit" << endl;
      exit(EXIT_FAILURE);
    }

    frSmoothFile->cd();
    frSmoothParameter_data->Write();
    frSmoothParameter_qcd->Write();
    frSmoothFile->Close();
    delete frSmoothFile;

  } else {
    cout << endl;
    cout << endl;
    cout << "##############" << endl;
    cout << "### WARNING: " << endl;
    cout << "### Not saving smoothed FR fit parameters to file because saveToFile option is false." << endl;
    cout << "##############" << endl;
    cout << endl;
  }

}
