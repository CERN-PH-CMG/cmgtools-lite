#include "../interface/utility.h"

#include <TDirectory.h>
#include <TKey.h>
#include <TList.h>

using namespace std;

// this macro handles the histograms in *_shapes.root file used by combine
// it copies a given input file but changing x_data_obs
// x_data_obs is obtained from some histograms in another *_shapes.root file produced with a different selection
// through options 'addProcessDiffSel_sig0_bkg1_all2_none3' and 'copyProcessDiffSel_sig0_bkg1_all2_none3' it is possible to select 
// which components should be added and/or copied from the file with different selection

//======================================================================

void checkElementInMap(const std::map<string,TH1D*>& m, const string& name = "") {

  std::map<string,TH1D*>::const_iterator it = m.find(name);
  if (it != m.end()) {
    cout << "Warning: copying an existing element with name " << name << ". Exit!" << endl;
    exit(EXIT_FAILURE);
  }

}

//======================================================================


void realCreateShapeFile(const string& fileName = "", 
			 const string& fileName_diffSelection = "",
			 const string& fileNameOut = "", 
			 const string& charge = "",
			 const Int_t nBinsYw = 13,  // histogram named x_Wplus_right_Wplus_el_Ybin_NN, NN goes to 0 to nBinsYw - 1 
			 const Int_t addProcessDiffSel_sig0_bkg1_all2_none3 = 2, // make data using signal or background or both with different selection
			 const Int_t copyProcessDiffSel_sig0_bkg1_all2_none3 = 3, // copy signal or background or both or none from file with different selection   	 
			 const Bool_t isMuon = false) {

  cout << endl;
  cout << "-------------------------------" << endl;
  cout << "Charge: " << charge << endl;
  cout << "-------------------------------" << endl;

  vector<string> backgroundProcesses;  
  // backgrounds
  backgroundProcesses.push_back("x_TauDecaysW");
  backgroundProcesses.push_back("x_Top");
  backgroundProcesses.push_back("x_DiBosons");
  backgroundProcesses.push_back("x_Z");
  backgroundProcesses.push_back(Form("x_W%s_long",charge.c_str()));
  backgroundProcesses.push_back("x_data_fakes");

  // signals
  vector<string> signalProcesses;
  for (Int_t i = 0; i < nBinsYw; i++) {
    signalProcesses.push_back(Form("x_W%s_left_W%s_el_Ybin_%d", charge.c_str(),charge.c_str(),i));
    signalProcesses.push_back(Form("x_W%s_right_W%s_el_Ybin_%d",charge.c_str(),charge.c_str(),i));
  }

  vector<string> processDiffSelToAdd;
  vector<string> processOrigSelToAdd;
  if (addProcessDiffSel_sig0_bkg1_all2_none3 == 0) {
    processDiffSelToAdd = signalProcesses;
    processOrigSelToAdd = backgroundProcesses;
  } else if (addProcessDiffSel_sig0_bkg1_all2_none3 == 1) {
    processDiffSelToAdd = backgroundProcesses;
    processOrigSelToAdd = signalProcesses;
  } else if (addProcessDiffSel_sig0_bkg1_all2_none3 == 2) {
    processDiffSelToAdd = backgroundProcesses;
    processDiffSelToAdd.insert(processDiffSelToAdd.end(), signalProcesses.begin(), signalProcesses.end());
  } else {
    processOrigSelToAdd = backgroundProcesses;
    processOrigSelToAdd.insert(processOrigSelToAdd.end(), signalProcesses.begin(), signalProcesses.end());
  }

  TH1D* htmp = nullptr;
  TH1D* hSumProcesses = nullptr;

  map<string,TH1D*> histToCopy;
  TKey *key;
  TDirectory *dir = nullptr;
  Int_t total = 0;
  Int_t totalCopied = 0;


  TFile* shapeFile = new TFile(fileName_diffSelection.c_str(),"READ");
  if (!shapeFile || shapeFile->IsZombie()) {
    cout << "Error: file not opened. Exit" << endl;
    exit(EXIT_FAILURE);
  }

  shapeFile->cd();
  cout << "#########" << endl;
  cout << "######### adding following samples with different selection" << endl;
  cout << "######### must add " << processDiffSelToAdd.size() << " elements" << endl;

  for (UInt_t i = 0; i < processDiffSelToAdd.size(); i++) {

    cout << "#########  i = " << i << ": " << processDiffSelToAdd[i] << endl;
    htmp = (TH1D*) shapeFile->Get(processDiffSelToAdd[i].c_str());
    checkNotNullPtr(htmp,"htmp:"+processDiffSelToAdd[i]);
    htmp->SetDirectory(0);

    if (i == 0) {
      hSumProcesses = (TH1D*) htmp->Clone("hSumProcesses"); 
      checkNotNullPtr(hSumProcesses,"hSumProcesses:"+processDiffSelToAdd[i]);
      hSumProcesses->SetDirectory(0);
    } else {
      hSumProcesses->Add((TH1D*) htmp->Clone());
    }

  }
  cout << "######### done" << endl;

  //shapeFile->Close();  // keep openend, it is used again below

  //////////////////////////////////////////////////////////////////
  // now we loop on input file to copy objects to rewrite on output
  //////////////////////////////////////////////////////////////////
  TFile* shapeFile_original = new TFile(fileName.c_str(),"READ");
  if (!shapeFile_original || shapeFile_original->IsZombie()) {
    cout << "Error: file not opened. Exit" << endl;
    exit(EXIT_FAILURE);
  }

  shapeFile_original->cd();

  cout << "#########" << endl;
  cout << "######### adding following samples with original selection" << endl;
  cout << "######### must add " << processOrigSelToAdd.size() << " elements" << endl;

  for (UInt_t i = 0; i < processOrigSelToAdd.size(); i++) {

    cout << "#########  i = " << i << ": " << processOrigSelToAdd[i] << endl;
    htmp = (TH1D*) shapeFile_original->Get(processOrigSelToAdd[i].c_str());
    checkNotNullPtr(htmp,"htmp:"+processOrigSelToAdd[i]);
    htmp->SetDirectory(0);
    if (i == 0 && processDiffSelToAdd.size() == 0) {
      hSumProcesses = (TH1D*) htmp->Clone("hSumProcesses"); 
      checkNotNullPtr(hSumProcesses,"hSumProcesses:"+processOrigSelToAdd[i]);
      hSumProcesses->SetDirectory(0);
    } else {
      hSumProcesses->Add((TH1D*) htmp->Clone());
    }

  }

  cout << "######### done" << endl;


  if (copyProcessDiffSel_sig0_bkg1_all2_none3 != 2) {

    dir = shapeFile_original;
    total = dir->GetNkeys();
    totalCopied = 0;
    TIter next((TList *) dir->GetListOfKeys());

    cout << "#########" << endl;
    cout << "######### copying following samples with original selection" << endl;

    while ((key = (TKey *)next())) {

      TClass *cl = gROOT->GetClass(key->GetClassName());
      if (cl->InheritsFrom("TH1")) {

	// the following line is not needed if you only want                                                                 
	// to count the histograms                                                           
	TH1 *h = (TH1 *)key->ReadObj();
	string hname(h->GetName());
	if (hname.find("x_data_obs") != string::npos) continue;

	if (copyProcessDiffSel_sig0_bkg1_all2_none3 == 0) {
	  if (hname.find("left") != string::npos || hname.find("right") != string::npos) continue;	
	} else if (copyProcessDiffSel_sig0_bkg1_all2_none3 == 1) {
	  if (hname.find("left") == string::npos && hname.find("right") == string::npos) continue;
	}

	cout << "######### " << hname << endl;      
	checkElementInMap(histToCopy,hname);
	histToCopy[hname] = (TH1D*) shapeFile_original->Get(hname.c_str());
	checkNotNullPtr(histToCopy[hname],"histToCopy:"+hname);
	histToCopy[hname]->SetDirectory(0);	
	totalCopied++;
      
  
      }

    }
    cout << "Copied " << totalCopied << " histograms with original selection (there were " << total << " histograms including data)" << endl;
    cout << "######### done" << endl;

  }

  shapeFile_original->Close();

  //////////////////////////////////////
  // change again to file with different selection to copy the remaining histograms (if any)

  if (copyProcessDiffSel_sig0_bkg1_all2_none3 != 3) {

    shapeFile->cd();

    dir = shapeFile;
    total = dir->GetNkeys();
    totalCopied = 0;
    TIter next((TList *) dir->GetListOfKeys());

    cout << "#########" << endl;
    cout << "######### copying following samples with different selection" << endl;

    while ((key = (TKey *)next())) {

      TClass *cl = gROOT->GetClass(key->GetClassName());
      if (cl->InheritsFrom("TH1")) {

	// the following line is not needed if you only want                                                                 
	// to count the histograms                                                           
	TH1 *h = (TH1 *)key->ReadObj();
	string hname(h->GetName());
	if (hname.find("x_data_obs") != string::npos) continue;

	if (copyProcessDiffSel_sig0_bkg1_all2_none3 == 0) {
	  if (hname.find("left") == string::npos && hname.find("right") == string::npos) continue;	
	} else if (copyProcessDiffSel_sig0_bkg1_all2_none3 == 1) {
	  if (hname.find("left") != string::npos || hname.find("right") != string::npos) continue;
	}

	cout << "######### " << hname << endl;      
	checkElementInMap(histToCopy,hname);
	histToCopy[hname] = (TH1D*) shapeFile->Get(hname.c_str());
	checkNotNullPtr(histToCopy[hname],"histToCopy:"+hname);
	histToCopy[hname]->SetDirectory(0);	
	totalCopied++;
      
  
      }

    }
    cout << "Copied " << totalCopied << " histograms with different selection (there were " << total << " histograms including data)" << endl;
    cout << "######### done" << endl;

  }

  shapeFile->Close();

  //////////////////////////////////////
  // opening new output file
  //////////////////////////////////////

  TFile* shapeFileOut = new TFile(fileNameOut.c_str(),"RECREATE");
  if (!shapeFileOut || shapeFileOut->IsZombie()) {
    cout << "Error: file not opened. Exit" << endl;
    exit(EXIT_FAILURE);
  }

  shapeFileOut->cd();

  std::map<string, TH1D*>::iterator it;
  for (it = histToCopy.begin(); it != histToCopy.end(); it++) {
    it->second->Write();
  }
  hSumProcesses->Write("x_data_obs");  

  cout << endl;
  cout << endl;
  cout << "Created file " << fileNameOut << endl;
  cout << endl;
  shapeFileOut->Close();

  histToCopy.clear();
  delete shapeFile;
  delete shapeFile_original;
  delete shapeFileOut;

}

//======================================================================

void createShapeFile_MCasDataObs(const string& inputFilePath = "/afs/cern.ch/work/m/mciprian/w_mass_analysis/heppy/CMSSW_8_0_25/src/CMGTools/WMass/python/plotter/cards/helicity_2018_03_05_baseSel_WLO/", 
				 const string& inputFilePath_diffSelection = "/afs/cern.ch/work/m/mciprian/w_mass_analysis/heppy/CMSSW_8_0_25/src/CMGTools/WMass/python/plotter/cards/helicity_2018_03_06_pfmt30_WLO/",
				 const string& outFilesuffix = "test_MCasData",
				 const Int_t nBinsYw = 13,  // histogram named x_Wplus_right_Wplus_el_Ybin_NN, NN goes to 0 to nBinsYw - 1 
				 const Int_t addProcessDiffSel_sig0_bkg1_all2_none3 = 3, // make data using signal or background or both with different selection
				 const Int_t copyProcessDiffSel_sig0_bkg1_all2_none3 = 3, // copy signal or background or both or none from file with different selection
				 const Bool_t isMuon = false
				 ) 
{

  if (isMuon) {
    cout << "Warning: at the moment this macro has hardcoded parts for electrons. Usage with muons must be implemented! Exit." << endl;
    exit(EXIT_FAILURE);
  }

 
  string shapePlusFile = "Wel_plus_shapes.root";
  string shapeMinusFile = "Wel_minus_shapes.root";
  string shapePlusFileOut = Form("Wel_plus_shapes_%s.root",outFilesuffix.c_str());
  string shapeMinusFileOut = Form("Wel_minus_shapes_%s.root",outFilesuffix.c_str());

  realCreateShapeFile(inputFilePath+shapePlusFile,  inputFilePath_diffSelection+shapePlusFile,  inputFilePath+shapePlusFileOut, "plus",   nBinsYw, addProcessDiffSel_sig0_bkg1_all2_none3, copyProcessDiffSel_sig0_bkg1_all2_none3, isMuon);
  realCreateShapeFile(inputFilePath+shapeMinusFile, inputFilePath_diffSelection+shapeMinusFile, inputFilePath+shapeMinusFileOut, "minus", nBinsYw, addProcessDiffSel_sig0_bkg1_all2_none3, copyProcessDiffSel_sig0_bkg1_all2_none3, isMuon);

}
