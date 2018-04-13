#include "../interface/utility.h"

#include <TDirectory.h>
#include <TKey.h>
#include <TList.h>

using namespace std;

// this macro handles the histograms in *_shapes.root file used by combine
// it copies signal W templates with a given charge from a file for a W with opposite charge
// Basically, it leaves names and global normalization of signal templates unchanged, but takes the shape of the opposite charge


//======================================================================

void checkElementInMap(const std::map<string,TH1D*>& m, const string& name = "") {

  std::map<string,TH1D*>::const_iterator it = m.find(name);
  if (it != m.end()) {
    cout << "Warning: copying an existing element with name " << name << ". Exit!" << endl;
    exit(EXIT_FAILURE);
  }

}

//======================================================================

void createShapeFile_scaleYields(const string& inputFilePath = "/afs/cern.ch/work/m/mciprian/w_mass_analysis/heppy/CMSSW_8_0_25/src/CMGTools/WMass/python/plotter/cards/helicity_2018_03_05_baseSel_WLO/", 
				 const string& outFilesuffix = "test_scaleWcharge",
				 const string& chargeToScale = "plus",  // minus, plus
				 const string& outputFilePath = "SAME",
				 const Bool_t  isMuon = false
				 ) 
{

  if (isMuon) {
    cout << "Warning: at the moment this macro has hardcoded parts for electrons. Usage with muons must be implemented! Exit." << endl;
    exit(EXIT_FAILURE);
  }

  TH1::SetDefaultSumw2(); //all the following histograms will automatically call TH1::Sumw2()                    

  string outDir = ((outputFilePath == "SAME") ? inputFilePath : outputFilePath);
  createPlotDirAndCopyPhp(outDir);

  string otherCharge = (chargeToScale == "minus") ? "plus" : "minus";

  string shapeFile_thisCharge  = Form("Wel_%s_shapes.root",   chargeToScale.c_str());
  string shapeFile_otherCharge = Form("Wel_%s_shapes.root",   otherCharge.c_str());
  string shapeFileOut          = Form("Wel_%s_shapes_%s.root",chargeToScale.c_str(), outFilesuffix.c_str());

  cout << endl;
  cout << "-------------------------------" << endl;
  cout << "Charge to scale: " << chargeToScale << endl;
  cout << "-------------------------------" << endl;

  TH1D* htmp = nullptr;
  map<string,TH1D*> histToCopy;
  TDirectory *dir = nullptr;
  Int_t total = 0;
  Int_t totalCopied = 0;
  TKey *key;

  ///////////////////////////////////////
  // open file with selected charge to be scaled
  //
  TFile* shapeFile = new TFile((inputFilePath+shapeFile_thisCharge).c_str(),"READ");
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
  // loop on keys inheriting from TH1D and copy these objects in a map (key is the name of the TH1D)
  //
  TIter next((TList *) dir->GetListOfKeys());

  while ((key = (TKey *)next())) {

    TClass *cl = gROOT->GetClass(key->GetClassName());

    if (cl->InheritsFrom("TH1D")) {

      TH1D *h = (TH1D *) key->ReadObj();
      string hname(h->GetName());
      cout << "######### " << hname << endl;      
      checkElementInMap(histToCopy,hname);
      histToCopy[hname] = (TH1D*) shapeFile->Get(hname.c_str());
      checkNotNullPtr(histToCopy[hname],"histToCopy:"+hname);
      histToCopy[hname]->SetDirectory(0);	
      total++;

    }

  }

  cout << "-----------------------------------" << endl;
  cout << "Found " << total << " histograms" << endl;
  cout << endl;

  shapeFile->Close();
  delete shapeFile;

  ///////////////////////////////////////////////
  // open file again (this time for the opposite charge)
  //
  shapeFile = new TFile((inputFilePath+shapeFile_otherCharge).c_str(),"READ");
  if (!shapeFile || shapeFile->IsZombie()) {
    cout << "Error: file not opened. Exit" << endl;
    exit(EXIT_FAILURE);
  }
  shapeFile->cd();
  cout << "#########" << endl;
  dir = shapeFile;

  next = TIter((TList *) dir->GetListOfKeys());

  while ((key = (TKey *)next())) {

    TClass *cl = gROOT->GetClass(key->GetClassName());

    if (cl->InheritsFrom("TH1D")) {

      TH1D *h = (TH1D *) key->ReadObj();
      string hname(h->GetName());
      // cout << "######### " << hname << endl;      
      string hname_chargeInMap = hname;
      replaceSubstringFromCString(hname_chargeInMap,otherCharge,chargeToScale,true); // map has keys named with chargeToScale
      Int_t lastbin = h->GetNbinsX() + 1;
      Double_t scaleFactor = (h->Integral(0,lastbin) + histToCopy[hname_chargeInMap]->Integral(0,lastbin)) / histToCopy[hname_chargeInMap]->Integral(0,lastbin); 
      histToCopy[hname_chargeInMap]->Scale(scaleFactor);

    }

  }

  shapeFile->Close();
  delete shapeFile;

  ///////////////////////////////////////////////
  // Finally, open new file and save scaled histograms
  //
  shapeFile = new TFile((outDir+shapeFileOut).c_str(),"RECREATE");
  if (!shapeFile || shapeFile->IsZombie()) {
    cout << "Error: file not opened. Exit" << endl;
    exit(EXIT_FAILURE);
  }
  shapeFile->cd();
  cout << "#########" << endl;
  cout << "######### Writing following samples" << endl;
  cout << "-----------------------------------" << endl;

  std::map<string, TH1D*>::iterator it;
  for (it = histToCopy.begin(); it != histToCopy.end(); it++) {
    cout << "######### " << it->first << endl;
    it->second->Write();
    totalCopied++;
  }

  cout << "-----------------------------------" << endl;
  cout << "Copied " << totalCopied << " histograms" << endl;
  cout << "Output: " << outDir + shapeFileOut << endl;
  cout << endl;

  histToCopy.clear();


}

