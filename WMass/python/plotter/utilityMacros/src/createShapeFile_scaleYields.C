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
				 const Bool_t  isMuon = false
				 ) 
{

  if (isMuon) {
    cout << "Warning: at the moment this macro has hardcoded parts for electrons. Usage with muons must be implemented! Exit." << endl;
    exit(EXIT_FAILURE);
  }

  TH1::SetDefaultSumw2(); //all the following histograms will automatically call TH1::Sumw2()                    

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
  shapeFile = new TFile((inputFilePath+shapeFileOut).c_str(),"RECREATE");
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
  cout << "Output: " << inputFilePath + shapeFileOut << endl;
  cout << endl;

  histToCopy.clear();


}





  // for (UInt_t i = 0; i < processDiffSelToAdd.size(); i++) {

  //   cout << "#########  i = " << i << ": " << processDiffSelToAdd[i] << endl;
  //   htmp = (TH1D*) shapeFile->Get(processDiffSelToAdd[i].c_str());
  //   checkNotNullPtr(htmp,"htmp:"+processDiffSelToAdd[i]);
  //   htmp->SetDirectory(0);

  //   if (i == 0) {
  //     hSumProcesses = (TH1D*) htmp->Clone("hSumProcesses"); 
  //     checkNotNullPtr(hSumProcesses,"hSumProcesses:"+processDiffSelToAdd[i]);
  //     hSumProcesses->SetDirectory(0);
  //   } else {
  //     hSumProcesses->Add((TH1D*) htmp->Clone());
  //   }

  // }
  // cout << "######### done" << endl;

  // //shapeFile->Close();  // keep openend, it is used again below

  // //////////////////////////////////////////////////////////////////
  // // now we loop on input file to copy objects to rewrite on output
  // //////////////////////////////////////////////////////////////////
  // TFile* shapeFile_original = new TFile(fileName.c_str(),"READ");
  // if (!shapeFile_original || shapeFile_original->IsZombie()) {
  //   cout << "Error: file not opened. Exit" << endl;
  //   exit(EXIT_FAILURE);
  // }

  // shapeFile_original->cd();

  // cout << "#########" << endl;
  // cout << "######### adding following samples with original selection" << endl;
  // cout << "######### must add " << processOrigSelToAdd.size() << " elements" << endl;

  // for (UInt_t i = 0; i < processOrigSelToAdd.size(); i++) {

  //   cout << "#########  i = " << i << ": " << processOrigSelToAdd[i] << endl;
  //   htmp = (TH1D*) shapeFile_original->Get(processOrigSelToAdd[i].c_str());
  //   checkNotNullPtr(htmp,"htmp:"+processOrigSelToAdd[i]);
  //   htmp->SetDirectory(0);
  //   if (i == 0 && processDiffSelToAdd.size() == 0) {
  //     hSumProcesses = (TH1D*) htmp->Clone("hSumProcesses"); 
  //     checkNotNullPtr(hSumProcesses,"hSumProcesses:"+processOrigSelToAdd[i]);
  //     hSumProcesses->SetDirectory(0);
  //   } else {
  //     hSumProcesses->Add((TH1D*) htmp->Clone());
  //   }

  // }

  // cout << "######### done" << endl;


  // if (copyProcessDiffSel_sig0_bkg1_all2_none3 != 2) {

  //   dir = shapeFile_original;
  //   total = dir->GetNkeys();
  //   totalCopied = 0;
  //   TIter next((TList *) dir->GetListOfKeys());

  //   cout << "#########" << endl;
  //   cout << "######### copying following samples with original selection" << endl;

  //   while ((key = (TKey *)next())) {

  //     TClass *cl = gROOT->GetClass(key->GetClassName());
  //     if (cl->InheritsFrom("TH1")) {

  // 	// the following line is not needed if you only want                                                                 
  // 	// to count the histograms                                                           
  // 	TH1 *h = (TH1 *)key->ReadObj();
  // 	string hname(h->GetName());
  // 	if (hname.find("x_data_obs") != string::npos) continue;

  // 	if (copyProcessDiffSel_sig0_bkg1_all2_none3 == 0) {
  // 	  if (hname.find("left") != string::npos || hname.find("right") != string::npos) continue;	
  // 	} else if (copyProcessDiffSel_sig0_bkg1_all2_none3 == 1) {
  // 	  if (hname.find("left") == string::npos && hname.find("right") == string::npos) continue;
  // 	}

  // 	cout << "######### " << hname << endl;      
  // 	checkElementInMap(histToCopy,hname);
  // 	histToCopy[hname] = (TH1D*) shapeFile_original->Get(hname.c_str());
  // 	checkNotNullPtr(histToCopy[hname],"histToCopy:"+hname);
  // 	histToCopy[hname]->SetDirectory(0);	
  // 	totalCopied++;
      
  
  //     }

  //   }
  //   cout << "Copied " << totalCopied << " histograms with original selection (there were " << total << " histograms including data)" << endl;
  //   cout << "######### done" << endl;

  // }

  // shapeFile_original->Close();

  // //////////////////////////////////////
  // // change again to file with different selection to copy the remaining histograms (if any)

  // if (copyProcessDiffSel_sig0_bkg1_all2_none3 != 3) {

  //   shapeFile->cd();

  //   dir = shapeFile;
  //   total = dir->GetNkeys();
  //   totalCopied = 0;
  //   TIter next((TList *) dir->GetListOfKeys());

  //   cout << "#########" << endl;
  //   cout << "######### copying following samples with different selection" << endl;

  //   while ((key = (TKey *)next())) {

  //     TClass *cl = gROOT->GetClass(key->GetClassName());
  //     if (cl->InheritsFrom("TH1")) {

  // 	// the following line is not needed if you only want                                                                 
  // 	// to count the histograms                                                           
  // 	TH1 *h = (TH1 *)key->ReadObj();
  // 	string hname(h->GetName());
  // 	if (hname.find("x_data_obs") != string::npos) continue;

  // 	if (copyProcessDiffSel_sig0_bkg1_all2_none3 == 0) {
  // 	  if (hname.find("left") == string::npos && hname.find("right") == string::npos) continue;	
  // 	} else if (copyProcessDiffSel_sig0_bkg1_all2_none3 == 1) {
  // 	  if (hname.find("left") != string::npos || hname.find("right") != string::npos) continue;
  // 	}

  // 	cout << "######### " << hname << endl;      
  // 	checkElementInMap(histToCopy,hname);
  // 	histToCopy[hname] = (TH1D*) shapeFile->Get(hname.c_str());
  // 	checkNotNullPtr(histToCopy[hname],"histToCopy:"+hname);
  // 	histToCopy[hname]->SetDirectory(0);	
  // 	totalCopied++;
      
  
  //     }

  //   }
  //   cout << "Copied " << totalCopied << " histograms with different selection (there were " << total << " histograms including data)" << endl;
  //   cout << "######### done" << endl;

  // }

  // shapeFile->Close();

  // //////////////////////////////////////
  // // opening new output file
  // //////////////////////////////////////

  // TFile* shapeFileOut = new TFile(fileNameOut.c_str(),"RECREATE");
  // if (!shapeFileOut || shapeFileOut->IsZombie()) {
  //   cout << "Error: file not opened. Exit" << endl;
  //   exit(EXIT_FAILURE);
  // }

  // shapeFileOut->cd();

  // std::map<string, TH1D*>::iterator it;
  // for (it = histToCopy.begin(); it != histToCopy.end(); it++) {
  //   it->second->Write();
  // }
  // hSumProcesses->Write("x_data_obs");  

  // cout << endl;
  // cout << endl;
  // cout << "Created file " << fileNameOut << endl;
  // cout << endl;
  // shapeFileOut->Close();
