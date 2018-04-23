#include "../interface/utility.h"

#include <TDirectory.h>
#include <TKey.h>
#include <TList.h>

using namespace std;

// this macro makes plots of 1D distributions from root files created by mcPlots.py 


//======================================================================

void realMakePlotsFromHeppy(const string& inputFilePath = "www/wmass/13TeV/distribution/TREES_1LEP_80X_V3_WENUSKIM_V5_TINY/FR_application_region/full2016data_14_04_2018_forAN_noUpPt_noMt/", 
			    const string& outputFilePath = "www/wmass/13TeV/test/rebinSingleDistribution/FR_application_region/full2016data_14_04_2018_forAN_noUpPt_noMt/",
			    const string& inputFileName  = "test_plots.root",  // 
			    const TString& processesList = "data,QCD,W,Z,Top,DiBosons",
			    const TString& legendEntryMCList = "QCD,W (amc@NLO),Z (amc@NLO),Top,DiBosons",
			    const vector<Int_t> colorMCList = {kGray, kRed+2, kAzure+2, kGreen+2, kViolet+2},
			    const TString& varList       = "trkmetEleCorr_dy,trkmt_trkmetEleCorr_dy", // "pfmt,ptl1,pfmet",
			    const Double_t lumi          = 35.9, 
			    const TString& globalRebinFactorList  = "1,1"
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

  vector<Int_t> globalRebinFactors;
  getVectorIntFromTStringList(globalRebinFactors, globalRebinFactorList,",",false);

  vector<TH1*> hmcs;
  TH1* hdata;

  TH1* hrebin = nullptr;

  ///////////////////////////////////////
  // open file with inputs
  //
  TFile* inputFile = new TFile((inputFilePath+inputFileName).c_str(),"READ");
  if (!inputFile || inputFile->IsZombie()) {
    cout << "Error: file not opened. Exit" << endl;
    exit(EXIT_FAILURE);
  }
  inputFile->cd();

  Int_t firstNonZeroBin = 1;

  for (UInt_t i = 0; i < vars.size(); ++i) {

    hdata = nullptr;
    hmcs.clear();
    

    for (UInt_t j = 0; j < processes.size(); ++j) {

      string histName = Form("%s_%s",vars[i].c_str(),processes[j].c_str());
      if (processes[j] == "data") {
	hdata = (TH1*) getHistCloneFromFile(inputFile, histName);
	checkNotNullPtr(hdata, histName);
	hdata->SetDirectory(0);
	firstNonZeroBin = hdata->FindFirstBinAbove(0.0);	
	///////////////
	hrebin = new TH1D("hrebin","",hdata->GetNbinsX()-firstNonZeroBin,hdata->GetBinLowEdge(firstNonZeroBin),hdata->GetBinLowEdge(1+hdata->GetNbinsX()));
	for (Int_t bin = 0; bin <= hrebin->GetNbinsX(); ++bin) {
	  hrebin->SetBinContent(bin,hdata->GetBinContent(hdata->FindBin(hrebin->GetBinCenter(bin))));
	  hrebin->SetBinError(bin,hdata->GetBinError(hdata->FindBin(hrebin->GetBinCenter(bin))));
	}
	hrebin->GetXaxis()->SetTitle(hdata->GetXaxis()->GetTitle());
	hdata = (TH1*) hrebin->Clone();
	delete hrebin;

	//if (globalRebinFactors[i] > 1) rebinByN(hdata,globalRebinFactors[i]);
      } else {
	hmcs.push_back( (TH1*) getHistCloneFromFile(inputFile, histName) );
	checkNotNullPtr(hmcs.back(), histName);
	hmcs.back()->SetDirectory(0);

	hrebin = new TH1D("hrebin","",hmcs.back()->GetNbinsX()-firstNonZeroBin,hmcs.back()->GetBinLowEdge(firstNonZeroBin),hmcs.back()->GetBinLowEdge(1+hmcs.back()->GetNbinsX()));
	for (Int_t bin = 0; bin <= hrebin->GetNbinsX(); ++bin) {
	  hrebin->SetBinContent(bin,hmcs.back()->GetBinContent(hmcs.back()->FindBin(hrebin->GetBinCenter(bin))));
	  hrebin->SetBinError(bin,hmcs.back()->GetBinError(hmcs.back()->FindBin(hrebin->GetBinCenter(bin))));
	}
	hmcs.back() = (TH1*) hrebin->Clone();
	delete hrebin;

	//if (globalRebinFactors[i] > 1) rebinByN(hmcs.back(),globalRebinFactors[i]);
      }

    }

    drawTH1dataMCstack(hdata,hmcs,
		       hdata->GetXaxis()->GetTitle(),hdata->GetYaxis()->GetTitle(),vars[i],
		       outDir,"Data",legendEntriesMC,"Data/pred.",lumi,globalRebinFactors[i],false,1,0.01,colorMCList,1001);

  }

  inputFile->Close();
  delete inputFile;

}


//=======================================================

void makePlotsFromHeppy(const string& inputFilePath = "www/wmass/13TeV/distribution/TREES_1LEP_80X_V3_FRELSKIM_V5/FR_computation_region/full2016dataBH_puAndTrgSf_ptResScale_08_04_2018_forAN/", 
			const string& outputFilePath = "www/wmass/13TeV/distribution/TREES_1LEP_80X_V3_FRELSKIM_V5/FR_computation_region/full2016dataBH_puAndTrgSf_ptResScale_08_04_2018_forAN/rebinned/",
			const TString& subfoldersList = "eta_0p0_1p479/,eta_1p479_2p1/,eta_2p1_2p5/",
			const string& inputFileName  = "test_plots.root",  // 
			const TString& processesList = "data,QCD,treeFR_W,Z,Top,DiBosons",
			const TString& legendEntryMCList = "QCD,W (amc@NLO),Z (amc@NLO),Top,DiBosons",
			const vector<Int_t> colorMCList = {kGray, kRed+2, kAzure+2, kGreen+2, kViolet+2},
			const TString& varList       = "ptl1", // "pfmt,ptl1,pfmet",
			const Double_t lumi          = 35.9, 
			const TString& globalRebinFactorList  = "2" 
			) 

{

  vector<string> subfolders;
  //cout << "subfolders to plot: " << endl;
  getVectorCStringFromTStringList(subfolders, subfoldersList, ",", false);

  if (subfolders.size() == 0) {
    realMakePlotsFromHeppy(inputFilePath,
			   outputFilePath,
			   inputFileName,
			   processesList,
			   legendEntryMCList,
			   colorMCList,
			   varList,
			   lumi,
			   globalRebinFactorList
			   );
  } else {
    for (UInt_t i = 0; i < subfolders.size(); ++i) {
      string outputFolder = (outputFilePath == "SAME") ? outputFilePath : (outputFilePath + subfolders[i]);
      realMakePlotsFromHeppy(inputFilePath + subfolders[i],
			     outputFolder,
			     inputFileName,
			     processesList,
			     legendEntryMCList,
			     colorMCList,
			     varList,
			     lumi,
			     globalRebinFactorList
			     );
    }
  }

}

