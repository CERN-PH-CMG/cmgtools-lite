#include "../interface/utility.h"

#include <TDirectory.h>
#include <TKey.h>
#include <TList.h>

using namespace std;

// this macro makes ratio of templates (prefit) from two different files (made with different conditions)
// templates can be obtained using the script w-helicity-13TeV/testRolling.py, which creates 2 root files with the 2D templates (1 for each charge)
// These input root files created by w-helicity-13TeV/testRolling.py have their names ending with "XXX.root", where XXX = "plus" or "minus"
// and this convention is used here to determine the charge
// For signal templates, we take the sum of all rapidity bins (separating only left and right polarization)


//======================================================================

void checkElementInMap(const std::map<string,TH2*>& m, const string& name = "") {

  std::map<string,TH2*>::const_iterator it = m.find(name);
  if (it != m.end()) {
    cout << "Warning: copying an existing element with name " << name << ". Exit!" << endl;
    exit(EXIT_FAILURE);
  }

}

//======================================================================

void realMakeTemplatesRatio(const string& inputFilePath  = "www/wmass/13TeV/test/rollingTemplates/fromEmanuele/",
			    const string& inputFilePath2 = "www/wmass/13TeV/test/rollingTemplates/helicity_2018_04_17_smearPFMET0p2/", 
			    const string& inputFileName  = "templates_2D_minus.root",  // 
			    const string& inputFileName2 = "templates_2D_minus.root",  // 
			    const string& outputFilePath = "www/wmass/13TeV/test/rollingTemplates/ratio/fromEmanuele_OVER_helicity_2018_04_17_smearPFMET0p2/",
			    const string& zAxisName      = "nominal / smeared PF E_{T}^{miss} (20%)::0.95,1.05",
			    const bool smoothPlot = true,
			    const bool drawProfileX = true,
			    const bool scaleToUnitArea = true
			    ) 
{

  TH1::SetDefaultSumw2(); //all the following histograms will automatically call TH1::Sumw2()                    

  string charge = (inputFileName.find("plus.root") != string::npos) ? "plus" : "minus";

  string outDir = ((outputFilePath == "SAME") ? inputFilePath : outputFilePath);
  outDir += (charge + "/");
  cout << "Will save plots in " << outDir << endl;
  createPlotDirAndCopyPhp(outDir);
  adjustSettings_CMS_lumi(outDir);

  map<string,TH2*> histToCopy;
  map<string,TH2*> histToCopy2;
  TDirectory *dir = nullptr;
  Int_t total = 0;
  Int_t totalCopied = 0;
  TKey *key;

  ///////////////////////////////////////
  // open file with shapes (first one)
  //
  TFile* shapeFile = new TFile((inputFilePath+inputFileName).c_str(),"READ");
  if (!shapeFile || shapeFile->IsZombie()) {
    cout << "Error: file not opened. Exit" << endl;
    exit(EXIT_FAILURE);
  }
  shapeFile->cd();
  cout << "#########" << endl;
  cout << "######### reading following samples" << endl;
  cout << "-----------------------------------" << endl;
  dir = shapeFile;

  ////////////////////////////////
  // loop on keys inheriting from TH2 and copy these objects in a map (key is the name of the TH2)
  //
  TIter next((TList *) dir->GetListOfKeys());

  while ((key = (TKey *)next())) {

    TClass *cl = gROOT->GetClass(key->GetClassName());

    if (cl->InheritsFrom("TH2")) {

      Bool_t isSignalTemplate = false;
      TH2 *h = (TH2 *) key->ReadObj();
      string hname(h->GetName());
      cout << "######### " << hname << endl;      
      string hnameSignal = "";
      if (hname.find("_Ybin_") != string::npos) {
	isSignalTemplate = true;
	// string lepton = "";
	string polarization = "";
	// if (hname.find("_el_") != string::npos) lepton = "el";
	// else                                    lepton = "mu";
	if (hname.find("right") != string::npos) polarization = "right"; 
	else                                     polarization = "left";  
	//hnameSignal = Form("W%s_%s_%s",charge.c_str(),polarization.c_str(),lepton.c_str());
	hnameSignal = Form("W%s_%s",charge.c_str(),polarization.c_str());
      }
      if (isSignalTemplate) {
	if (histToCopy.find(hnameSignal) != histToCopy.end()) {
	  histToCopy[hnameSignal]->Add( (TH2*) shapeFile->Get(hname.c_str()) );
	} else { 
	  histToCopy[hnameSignal] = (TH2*) ((TH2*) shapeFile->Get(hname.c_str()))->Clone(hnameSignal.c_str());
	  checkNotNullPtr(histToCopy[hnameSignal],"histToCopy:"+hnameSignal);
	  histToCopy[hnameSignal]->SetDirectory(0);	
	}
      } else {
	checkElementInMap(histToCopy,hname);
	histToCopy[hname] = (TH2*) shapeFile->Get(hname.c_str());
	checkNotNullPtr(histToCopy[hname],"histToCopy:"+hname);
	histToCopy[hname]->SetDirectory(0);	
      }
      total++;

    }

  }

  cout << "-----------------------------------" << endl;
  cout << "Found " << total << " histograms" << endl;
  cout << endl;

  shapeFile->Close();
  delete shapeFile;

  ///////////////////////////////////////////////
  // open other file again and get objects based on name
  //
  shapeFile = new TFile((inputFilePath2+inputFileName2).c_str(),"READ");
  if (!shapeFile || shapeFile->IsZombie()) {
    cout << "Error: file not opened. Exit" << endl;
    exit(EXIT_FAILURE);
  }
  shapeFile->cd();
  dir = shapeFile;

  next = TIter((TList *) dir->GetListOfKeys());

  while ((key = (TKey *)next())) {

    TClass *cl = gROOT->GetClass(key->GetClassName());

    if (cl->InheritsFrom("TH2")) {

      Bool_t isSignalTemplate = false;
      TH2 *h = (TH2 *) key->ReadObj();
      string hname(h->GetName());
      string hnameSignal = "";
      if (hname.find("_Ybin_") != string::npos) {
	isSignalTemplate = true;
	// string lepton = "";
	string polarization = "";
	// if (hname.find("_el_") != string::npos) lepton = "el";
	// else                                    lepton = "mu";
	if (hname.find("right") != string::npos) polarization = "right"; 
	else                                     polarization = "left";  
	//hnameSignal = Form("W%s_%s_%s",charge.c_str(),polarization.c_str(),lepton.c_str());
	hnameSignal = Form("W%s_%s",charge.c_str(),polarization.c_str());
      }
      if (isSignalTemplate) {
	if (histToCopy2.find(hnameSignal) != histToCopy2.end()) {
	  histToCopy2[hnameSignal]->Add( (TH2*) shapeFile->Get(hname.c_str()) );
	} else { 
	  histToCopy2[hnameSignal] = (TH2*) ((TH2*) shapeFile->Get(hname.c_str()))->Clone(hnameSignal.c_str());
	  checkNotNullPtr(histToCopy2[hnameSignal],"histToCopy2:"+hnameSignal);
	  histToCopy2[hnameSignal]->SetDirectory(0);	
	}
      } else {
	checkElementInMap(histToCopy2,hname);
	histToCopy2[hname] = (TH2*) shapeFile->Get(hname.c_str());
	checkNotNullPtr(histToCopy2[hname],"histToCopy2:"+hname);
	histToCopy2[hname]->SetDirectory(0);	
      }
      total++;

    }

  }

  //////////////////////////////////
  // loop on maps, make ratios and plot

  for (std::map<string,TH2*>::const_iterator it = histToCopy.begin(); it != histToCopy.end(); ++it) {

    string templateName = it->first;
    TH2* hratio = (TH2*) histToCopy[templateName]->Clone(Form("%s_ratio_%s",templateName.c_str(),charge.c_str()));
    hratio->Divide(histToCopy2[templateName]);

    // get binning from zAxisName, if given
    Double_t zmin = 0.9;
    Double_t zmax = 1.1;
    string zAxisName_dummy = "";
    getAxisRangeFromUser(zAxisName_dummy,zmin,zmax,zAxisName);
    setContentBelowScaleToZmin(hratio,zmin);

    drawCorrelationPlot(hratio, hratio->GetXaxis()->GetTitle(), hratio->GetYaxis()->GetTitle(), zAxisName,
			hratio->GetName(), "", outDir, 1, 1, smoothPlot, drawProfileX, scaleToUnitArea, 1);


  }

  histToCopy.clear();
  histToCopy2.clear();


}


//=====================================

void makeTemplatesRatio(const string& inputFilePath  = "www/wmass/13TeV/test/rollingTemplates/helicity_2018_04_19_noSmearPFMET/",
			const string& inputFilePath2 = "www/wmass/13TeV/test/rollingTemplates/helicity_2018_04_17_smearPFMET0p2/", 
			const string& inputFileName  = "templates_2D_CHARGE.root",  // 
			const string& inputFileName2 = "templates_2D_CHARGE.root",  // 
			const string& outputFilePath = "www/wmass/13TeV/test/rollingTemplates/ratio/helicity_2018_04_19_noSmearPFMET_OVER_helicity_2018_04_17_smearPFMET0p2/",
			const string& zAxisName      = "nominal / smeared PF E_{T}^{miss} (20%)::0.95,1.05",
                        const bool smoothPlot = false,
			const bool drawProfileX = false,
			const bool scaleToUnitArea = false
			) 
{

  string matchToBeReplaced = "CHARGE";
  if (inputFileName.find(matchToBeReplaced) != string::npos) {

    vector<string> charges = {"plus", "minus"};

    for (UInt_t i = 0; i < charges.size(); ++i) {
      string name1 = inputFileName;
      size_t pos = inputFileName.find(matchToBeReplaced);
      name1.replace(pos, matchToBeReplaced.size(), charges[i]);
      string name2 = inputFileName2;
      pos = inputFileName2.find(matchToBeReplaced);
      name2.replace(pos, matchToBeReplaced.size(), charges[i]);
      realMakeTemplatesRatio(inputFilePath, inputFilePath2, name1, name2, outputFilePath, zAxisName, smoothPlot, drawProfileX, scaleToUnitArea);
    }    

  } else {
    realMakeTemplatesRatio(inputFilePath, inputFilePath2, inputFileName, inputFileName, outputFilePath, zAxisName, smoothPlot, drawProfileX, scaleToUnitArea);
  }    

}
