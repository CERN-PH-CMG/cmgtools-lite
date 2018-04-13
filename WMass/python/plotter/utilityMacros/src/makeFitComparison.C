#include "../interface/utility.h"

using namespace std;

// this macro compares relative errors of fits made with different condition.
// It was originally conceived to compare fit errors on W rapidity distributions obtained with different selections
// 
// Pass input directory where the files are and the comma separated list of file names (it is suggested to co
//
// needs bin edges for rapidity: x values of graphs obtained from central values between consecutive edges
// FIXME: read it from file

void makeFitComparison(const string& inputFilePath_tmp = "./fitComparison/",
		       const TString& fileNameList = "multidimfit_plus_nominal_NLO_HLT27.root,multidimfit_plus_pfmt40_NLO_HLT27.root",
		       const TString& legendList = "no PF M_{T},PF M_{T} > 40",
		       const vector<Double_t> binning = {0.0,0.25,0.5,0.75,1.0,1.25,1.5,1.75,2.0,2.25,2.5,2.75,3.25,6.0},  
		       const string& outDir_tmp = "www/wmass/13TeV/test/rapidityW/fitComparison/" 
		       ) 
{

  gROOT->SetBatch(kTRUE);
  TH1::SetDefaultSumw2(); //all the following histograms will automatically call TH1::Sumw2()                  
  cout << endl;
  
  string outDir = ((outDir_tmp == "SAME") ? inputFilePath_tmp : (outDir_tmp));
  createPlotDirAndCopyPhp(outDir);
  adjustSettings_CMS_lumi(outDir);

  vector<string> fileNames;
  cout << "Input files: " << endl;
  getVectorCStringFromTStringList(fileNames, fileNameList, ",", true);

  vector<TGraph*> gr_rapidityR;
  vector<TGraph*> gr_rapidityL;
  vector<string> legEntries;
  cout << "Legend entries: " << endl;
  getVectorCStringFromTStringList(legEntries,  legendList, ",", true);

  // loop on files
  TGraphAsymmErrors* gr_tmp = nullptr;

  for (UInt_t ifile = 0; ifile < fileNames.size(); ++ifile) {

    string inputFileName = inputFilePath_tmp + fileNames[ifile];
  
    TFile* inputFile = new TFile(inputFileName.c_str(),"READ");
    if (!inputFile || inputFile->IsZombie()) {
      cout << "Error: file not opened. Exit" << endl;
      exit(EXIT_FAILURE);
    }
    
    inputFile->cd();

    RooFitResult* fitresult = (RooFitResult*) inputFile->Get("fit_mdf");
    RooArgList parPostfit = fitresult->floatParsFinal();
    RooArgList parConst = fitresult->constPars();
    RooArgList parAll = RooArgList(parPostfit); parAll.add(parConst);
    RooArgList parRapidityLeft = RooArgList("rapidityBinsL");
    RooArgList parRapidityRight = RooArgList("rapidityBinsR");

    vector<string> rapidityRight_parNames;
    vector<string> rapidityLeft_parNames;
    Double_t totalrate = 0.0;

    cout << "###################################" << endl;
    cout << "File: " << inputFileName << endl;
    cout << "Getting following parameters " << endl;
    cout << "-----------------------------------" << endl;

    // string extension = ".root";
    // string gr_name = fileNames[ifile].substr(0, fileNames[ifile].size() - extension.size()); // assign to graph the name of the root file without the extension
    // cout << "graph name: " << gr_name << endl;

    gr_rapidityR.push_back(new TGraphAsymmErrors());
    gr_rapidityL.push_back(new TGraphAsymmErrors());
    
    for (Int_t ipf = 0; ipf < parAll.getSize(); ++ipf) {

      TString objName = parAll.at(ipf)->GetName();

      if (objName.BeginsWith("norm_W") and objName.Contains("_Ybin_")) {

	if (objName.Contains("right")) {

	  rapidityRight_parNames.push_back(objName.Data());
	  cout << rapidityRight_parNames.back() << endl;
	  parRapidityRight.add(*parAll.at(ipf));
	  totalrate += ((RooRealVar*) parAll.at(ipf))->getVal();

	} else if (objName.Contains("left"))  {

	  rapidityLeft_parNames.push_back(objName.Data());
	  cout << rapidityLeft_parNames.back() << endl;
	  parRapidityLeft.add(*parAll.at(ipf));
	  totalrate += ((RooRealVar*) parAll.at(ipf))->getVal();

	}

      }

    }

    cout << "Total rate left+right = " << totalrate << endl;

    // edges are Nbins+1
    if (binning.size() <= (UInt_t) parRapidityLeft.getSize()) {
      cout << Form("Warning: I have %d parameters for Y_WL, but you passed %lu bins! Please check. Exit.",parRapidityLeft.getSize(), binning.size()-1) << endl;
      exit(EXIT_FAILURE);
    }

    for (Int_t iL = 0; iL < parRapidityLeft.getSize(); ++iL) {

      string objName = string(parRapidityLeft.at(iL)->GetName());
      string match = "Ybin_";
      size_t pos = objName.find(match);
      Int_t bin = stoi(objName.substr(pos+match.size()));
      Double_t binWidth = (binning[bin+1] - binning[bin]);
      Double_t normFactor = totalrate * binWidth;

      Double_t xval = 0.5 * (binning[bin] + binning[bin+1]);
      Double_t yval = ((RooRealVar*) parRapidityLeft.at(iL))->getVal()/normFactor;
      Double_t xerr = 0.5 * binWidth;
      Double_t yerrhi = fabs( ((RooRealVar*) parRapidityLeft.at(iL))->getAsymErrorHi() ) / normFactor;
      Double_t yerrlo = fabs( ((RooRealVar*) parRapidityLeft.at(iL))->getAsymErrorLo() ) / normFactor;
      if (abs(yerrlo) < 0.0000001) yerrlo = yerrhi;

      gr_rapidityL.back()->SetPoint(bin, xval, yval);      
      ((TGraphAsymmErrors*) gr_rapidityL.back())->SetPointError(bin, xerr, xerr, yerrlo, yerrhi);      

    }

    // edges are Nbins+1
    if (binning.size() <= (UInt_t) parRapidityRight.getSize()) {
      cout << Form("Warning: I have %d parameters for Y_WR, but you passed %lu bins! Please check. Exit.",parRapidityRight.getSize(), binning.size()-1) << endl;
      exit(EXIT_FAILURE);
    }

    for (Int_t iR = 0; iR < parRapidityRight.getSize(); ++iR) {

      string objName = string(parRapidityRight.at(iR)->GetName());
      string match = "Ybin_";
      size_t pos = objName.find(match);
      Int_t bin = stoi(objName.substr(pos+match.size()));
      Double_t binWidth = (binning[bin+1] - binning[bin]);
      Double_t normFactor = totalrate * binWidth;

      Double_t xval = 0.5 * (binning[bin] + binning[bin+1]);
      Double_t yval = ((RooRealVar*) parRapidityRight.at(iR))->getVal()/normFactor;
      Double_t xerr = 0.5 * binWidth;
      Double_t yerrhi = fabs( ((RooRealVar*) parRapidityRight.at(iR))->getAsymErrorHi() ) / normFactor;
      Double_t yerrlo = fabs( ((RooRealVar*) parRapidityRight.at(iR))->getAsymErrorLo() ) / normFactor;
      if (abs(yerrlo) < 0.0000001) yerrlo = yerrhi;

      gr_rapidityR.back()->SetPoint(bin, xval, yval);      
      ((TGraphAsymmErrors*) gr_rapidityR.back())->SetPointError(bin, xerr, xerr, yerrlo, yerrhi);      

    }

    cout << "-----------------------------------" << endl;
    cout << "Rapidity values for WL" << endl;
    gr_rapidityL.back()->Print();
    cout << "-----------------------------------" << endl;
    cout << "Rapidity values for WR" << endl;
    gr_rapidityR.back()->Print();
    cout << "-----------------------------------" << endl;

    cout << "###################################" << endl;

    inputFile->Close();

  }

  cout << "Now drawing graphs and ratios" << endl;  
  drawRapidityGraph(gr_rapidityL,"Y_{W} left", "a.u.", "rapidity_Wleft",outDir_tmp, legEntries, {0.6,0.7,0.9,0.9}, -1.0, true,"X/first::0.95,1.05");
  drawRapidityGraph(gr_rapidityR,"Y_{W} right", "a.u.", "rapidity_Wright",outDir_tmp, legEntries, {0.6,0.7,0.9,0.9}, -1.0, true,"X/first::0.95,1.05");

  for (UInt_t i = 0; i < gr_rapidityL.size(); ++i) {
    delete gr_rapidityL[i];
    delete gr_rapidityR[i];
  }

  cout << endl;

}
