#include "../interface/utility.h"

using namespace std;

// read TH2 from file and create efficiency
// if you have TH2 of varY vs varX, efficiency of selection of Y variable is defined, for fixed X, as integral of Y from first bin to Y' over integral on whole Y range
// this is done by doEfficiencyFromTH2 function: by passing option "revert = true" the efficiency is defined using integral from Y' to last bin
// overflow and underflow are considered in the integrals   

// use makeEffStudy(...) below
// need path of input root file, name of root file and name of output folder
// if output folder is passed as "SAME", it is considered as input folder
// input file is supposed to be in a folder named neg/ or pos/ (no need to explicitly pass that, you can just pass the folder before that)

void realMakeEffStudy(const string& outDir = "", 
		      const string& inputFileName = "",
		      const string& histName_prefix = "",
		      const TString& processesList = "",
		      const TString& ycutList = ""  // use integer
		      ) 
{

  createPlotDirAndCopyPhp(outDir);
  adjustSettings_CMS_lumi(outDir);

  Bool_t isPlusCharge = (outDir.find("/neg/") == string::npos) ? true : false;
  cout << "Charge --> " << (isPlusCharge ? "positive" : "negative") << endl;

  vector<TString> processes;
  cout << "Processes to plot: " << endl;
  getVectorTStringFromTStringList(processes,  processesList, ",", true);

  string varOnYaxis = histName_prefix.substr(0,histName_prefix.find("_"));
  cout << "variable on Y axis --> " << varOnYaxis << endl;
  vector<Int_t> ycuts;
  cout << "Selected cuts on " << varOnYaxis << ": " << endl;
  getVectorIntFromTStringList(ycuts, ycutList, ",", true);
 
  string xAxisName = "";


  gROOT->SetBatch(kTRUE);
  TH1::SetDefaultSumw2(); //all the following histograms will automatically call TH1::Sumw2()                  
  cout << endl;

  TFile* inputFile = new TFile(inputFileName.c_str(),"READ");
  if (!inputFile || inputFile->IsZombie()) {
    cout << "Error: file not opened. Exit" << endl;
    exit(EXIT_FAILURE);
  }

  inputFile->cd();

  TH2D* h2 = NULL;
      
  vector<TH1*> hWright;
  vector<TH1*> hWleft;
  vector<TH1*> hWlong;
  vector<TH1*> hQCD;
  vector<TH1*> hZ;

  for (UInt_t i = 0; i < processes.size(); ++i) {

    if (isPlusCharge) {
      if (processes[i].Contains("Wminus")) {
	cout << "Warning: charge is positive. Skipping process " << processes[i] << endl;
	continue;
      }
    } else {
      if (processes[i].Contains("Wplus")) {
	cout << "Warning: charge is negative. Skipping process " << processes[i] << endl;
	continue;
      }
    } 

    string histName = Form("%s_%s",histName_prefix.c_str(),processes[i].Data());
    h2 = (TH2D*) getHistCloneFromFile(inputFile, histName);
    checkNotNullPtr(h2, histName);
    h2->SetDirectory(0);
    drawCorrelationPlot(h2,
			h2->GetXaxis()->GetTitle(), h2->GetYaxis()->GetTitle(), "Events",
			h2->GetName(),"",outDir,1,1,false,false,false,1);    

    if (i == 0) xAxisName = h2->GetXaxis()->GetTitle();

    TH2D* h2_eff = new TH2D(*h2);
    h2_eff->SetDirectory(0);
    doEfficiencyFromTH2(h2_eff, h2, true);
    drawCorrelationPlot(h2_eff,
			h2->GetXaxis()->GetTitle(), h2->GetYaxis()->GetTitle(), "y axis cut efficiency",
			Form("%s_efficiency",h2->GetName()),"",outDir,1,1,false,false,false,1);    

    for (UInt_t j = 0; j < ycuts.size(); ++j) {

      if (processes[i].Contains("Z")) 
	hZ.push_back(h2_eff->ProjectionX(Form("Z_eff_%s%d",varOnYaxis.c_str(),ycuts[j]),
					 h2_eff->GetYaxis()->FindBin(ycuts[j]),
					 h2_eff->GetYaxis()->FindBin(ycuts[j]))
		     );
      else if ((processes[i].Contains("Wplus") and isPlusCharge) or (processes[i].Contains("Wminus") and not isPlusCharge)) {

	if (processes[i].Contains("_right")) {
	  hWright.push_back(h2_eff->ProjectionX(Form("Wright_eff_%s%d",varOnYaxis.c_str(),ycuts[j]),
	  					h2_eff->GetYaxis()->FindBin(ycuts[j]),
	  					h2_eff->GetYaxis()->FindBin(ycuts[j]))
	  		    );
	  // hWright.push_back(new TH1D(Form("Wright_eff_%s%d",varOnYaxis.c_str(),ycuts[j]),"",
	  // 			     h2_eff->GetNbinsX(), h2_eff->GetXaxis()->GetBinLowEdge(1), h2_eff->GetXaxis()->GetBinLowEdge(1+h2_eff->GetNbinsX()))
	  // 		    );
	  // for (Int_t bin = 1; bin <= hWright.back()->GetNbinsX(); ++bin) {
	  //   cout << "Xbin " << bin << "   Ybin " << ycuts[j] << "   content " << h2_eff->GetBinContent(bin, h2_eff->GetYaxis()->FindBin(ycuts[j])) << endl; 
	  //   hWright.back()->SetBinContent(bin, h2_eff->GetBinContent(bin, h2_eff->GetYaxis()->FindBin(ycuts[j])) );
	  // }

	}	
	else if (processes[i].Contains("_left")) 
	  hWleft.push_back(h2_eff->ProjectionX(Form("Wleft_eff_%s%d",varOnYaxis.c_str(),ycuts[j]),
					       h2_eff->GetYaxis()->FindBin(ycuts[j]),
					       h2_eff->GetYaxis()->FindBin(ycuts[j]))
			   );
	else if (processes[i].Contains("_long")) 
	  hWlong.push_back(h2_eff->ProjectionX(Form("Wlong_eff_%s%d",varOnYaxis.c_str(),ycuts[j]),
					       h2_eff->GetYaxis()->FindBin(ycuts[j]),
					       h2_eff->GetYaxis()->FindBin(ycuts[j]))
			   );
	
      }	else if (processes[i].Contains("data_fakes")) 
	hQCD.push_back(h2_eff->ProjectionX(Form("QCD_eff_%s%d",varOnYaxis.c_str(),ycuts[j]),
					   h2_eff->GetYaxis()->FindBin(ycuts[j]),
					   h2_eff->GetYaxis()->FindBin(ycuts[j]))
		       );
      

    }

    delete h2_eff;

  }

  // cout << "Sizes of vectors" << endl;
  // cout << "WR : " << hWright.size() << endl;
  // cout << "WL : " << hWleft.size() << endl;
  // cout << "W0 : " << hWlong.size() << endl;
  // cout << "Z  : " << hZ.size() << endl;
  // cout << "QCD: " << hQCD.size() << endl;

  // drawSingleTH1(hWright[0],"x","y","trashtest",outDir,"WR",-1.0,1,true,1);
  // return;

  for (UInt_t j = 0; j < ycuts.size(); ++j) {

    vector<TH1*> hist;
    hist.push_back(hWright[j]);
    hist.push_back(hWleft[j]);
    hist.push_back(hWlong[j]);
    hist.push_back(hZ[j]);
    hist.push_back(hQCD[j]);
    vector<string> legendEntry;
    legendEntry.push_back("W right");
    legendEntry.push_back("W left");
    legendEntry.push_back("W long");
    legendEntry.push_back("Z");
    legendEntry.push_back("QCD");

    draw_nTH1(hist, xAxisName, Form("efficiency for %s > %d::0,1.2",varOnYaxis.c_str(),ycuts[j]), Form("efficiency_%s%d",varOnYaxis.c_str(),ycuts[j]), 
  	      outDir, legendEntry, "", -1, 1, false, false);

  }

  inputFile->Close();

  cout << endl;

}


//========================================================

// note: processesList could contain both Wplus and Wminus components: a check is made on the charge and non-existing components are discarded

void makeEffStudy(const string& inputFilePath_tmp = "www/wmass/13TeV/efficiency_trkmt_vs_eta/",
		  const string& inputFileName = "tmp_plots.root", 
		  const string& outDir_tmp = "SAME", 
		  const string& histName_prefix = "trkmt_etal1",
		  const TString& processesList = "Z,TauDecaysW,DiBosons,WFlips,data_fakes,Top,Wminus_left,Wminus_right,Wminus_long,Wplus_left,Wplus_right,Wplus_long",
		  const TString& ycutList = "30,40,50"  // use integer
		  ) 
{

  vector<string> chargeDir;
  chargeDir.push_back("neg/");
  chargeDir.push_back("pos/");

  for (UInt_t i = 0; i < chargeDir.size(); ++i) {

    string inputFilePath = inputFilePath_tmp + chargeDir[i];
    string outDir = ((outDir_tmp == "SAME") ? inputFilePath : (outDir_tmp+chargeDir[i]));

    realMakeEffStudy(outDir, inputFilePath+inputFileName, histName_prefix, processesList, ycutList);     

  }

}
