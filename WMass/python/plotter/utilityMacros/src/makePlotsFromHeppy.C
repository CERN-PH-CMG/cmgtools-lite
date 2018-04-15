#include "../interface/utility.h"

#include <TDirectory.h>
#include <TKey.h>
#include <TList.h>

using namespace std;

// this macro makes plots of 1D distributions from root files created by mcPlots.py 


//======================================================================

void makePlotsFromHeppy(const string& inputFilePath = "www/wmass/13TeV/distribution/TREES_1LEP_80X_V3_WENUSKIM_V5_TINY/FR_application_region/full2016data_14_04_2018_forAN_noUpPt_noMt/eta_0p0_1p479/", 
			const string& inputFileName  = "test_plots.root",  // 
			const string& outputFilePath = "www/wmass/13TeV/test/rebinSingleDistribution/",
			const TString& processesList = "data,QCD,W,Z,Top,DiBosons",
			const TString& legendEntryMCList = "QCD,W (amc@NLO),Z (amc@NLO),Top,DiBosons",
			const vector<Int_t> colorMCList = {kGray, kRed+2, kAzure+2, kGreen+2, kViolet+2},
			const TString& varList       = "pfmt,ptl1,pfmet",
			const Double_t lumi          = 35.9, 
			const Int_t globalRebinFactor  = 1 
			) 
{

  TH1::SetDefaultSumw2(); //all the following histograms will automatically call TH1::Sumw2()                    

  string outDir = ((outputFilePath == "SAME") ? inputFilePath : outputFilePath);
  cout << "Will save plots in " << outDir << endl;
  createPlotDirAndCopyPhp(outDir);
  adjustSettings_CMS_lumi(outDir);

  vector<string> processes;
  cout << "Processes to plot: " << endl;
  getVectorCStringFromTStringList(processes,  processesList, ",", true);

  vector<string> vars;
  cout << "Variables to plot: " << endl;
  getVectorCStringFromTStringList(vars,  varList, ",", true);

  vector<string> legendEntriesMC;
  cout << "Legend entries: " << endl;
  getVectorCStringFromTStringList(legendEntriesMC,  legendEntryMCList, ",", true);


  vector<TH1*> hmcs;
  TH1* hdata;

  ///////////////////////////////////////
  // open file with inputs
  //
  TFile* inputFile = new TFile((inputFilePath+inputFileName).c_str(),"READ");
  if (!inputFile || inputFile->IsZombie()) {
    cout << "Error: file not opened. Exit" << endl;
    exit(EXIT_FAILURE);
  }
  inputFile->cd();

  for (UInt_t i = 0; i < vars.size(); ++i) {

    hdata = nullptr;
    hmcs.clear();

    for (UInt_t j = 0; j < processes.size(); ++j) {

      string histName = Form("%s_%s",vars[i].c_str(),processes[j].c_str());
      if (processes[j] == "data") {
	hdata = (TH1*) getHistCloneFromFile(inputFile, histName);
	checkNotNullPtr(hdata, histName);
	hdata->SetDirectory(0);
      } else {
	hmcs.push_back( (TH1*) getHistCloneFromFile(inputFile, histName) );
	checkNotNullPtr(hmcs.back(), histName);
	hmcs.back()->SetDirectory(0);
	if (processes[j] == "QCD") smoothAveragingNbins(hmcs.back(),4);
      }

    }

    drawTH1dataMCstack(hdata,hmcs,
		       hdata->GetXaxis()->GetTitle(),hdata->GetYaxis()->GetTitle(),vars[i],
		       outDir,"Data",legendEntriesMC,"Data/pred.",lumi,globalRebinFactor,false,1,0.01,colorMCList,1001);

  }

  inputFile->Close();
  delete inputFile;

}


