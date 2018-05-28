#include "../interface/utility.h"

#include <TDirectory.h>
#include <TKey.h>
#include <TList.h>

using namespace std;

// this macro makes plots of 2D distributions from root files created by mcPlots.py 


//======================================================================

void realMake2DPlotsFromHeppy(const string& inputFilePath = "www/wmass/13TeV/correlation_pfmt_pfmet/", 
			      const string& outputFilePath = "SAME",
			      const string& inputFileName  = "test_plots.root",  // 
			      const TString& processesList = "W,Z,data_fakes,Top,DiBosons,TauDecaysW",
			      const TString& varList       = "pfmt_pfmet", // "pfmt,ptl1,pfmet",
			      const Double_t lumi          = 35.9 
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

  TH2* h = nullptr;

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

    for (UInt_t j = 0; j < processes.size(); ++j) {

      string histName = Form("%s_%s",vars[i].c_str(),processes[j].c_str());
      h = (TH2*) getHist2CloneFromFile(inputFile, histName);
      checkNotNullPtr(h, histName);
      h->SetDirectory(0);

      drawCorrelationPlot(h, h->GetXaxis()->GetTitle(), h->GetYaxis()->GetTitle(), "a.u.", 
			  h->GetName(), "", outDir, 1, 1, true, true, true, 1);
      
    }

  }

  inputFile->Close();
  delete inputFile;

}


//=======================================================

void make2DPlotsFromHeppy(const string& inputFilePath = "www/wmass/13TeV/correlation_pfmt_pfmet/", 
			  const string& outputFilePath = "www/wmass/13TeV/correlation_pfmt_pfmet/make2DPlotsFromHeppy/",
			  const TString& subfoldersList = "pos/",
			  const string& inputFileName  = "tmp_plots.root",  // 
			  const TString& processesList = "W,Z,data_fakes,Top,DiBosons,TauDecaysW",
			  const TString& varList       = "pfmt_pfmet", // "pfmt,ptl1,pfmet",
			  const Double_t lumi          = 35.9
			  )

{

  vector<string> subfolders;
  //cout << "subfolders to plot: " << endl;
  getVectorCStringFromTStringList(subfolders, subfoldersList, ",", false);

  if (subfolders.size() == 0) {
    realMake2DPlotsFromHeppy(inputFilePath,
			     outputFilePath,
			     inputFileName,
			     processesList,
			     varList,
			     lumi
			     );
  } else {
    for (UInt_t i = 0; i < subfolders.size(); ++i) {
      string outputFolder = (outputFilePath == "SAME") ? outputFilePath : (outputFilePath + subfolders[i]);
      realMake2DPlotsFromHeppy(inputFilePath + subfolders[i],
			       outputFolder,
			       inputFileName,
			       processesList,
			       varList,
			       lumi
			       );
    }
  }

}

