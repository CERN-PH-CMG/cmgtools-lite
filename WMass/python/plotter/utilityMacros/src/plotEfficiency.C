#include "../interface/utility.h"

using namespace std;


//================================================================

TH1* getEfficiency(const string& inputFile = "", 
		   const Bool_t isMuon = false,
		   const string& nameGen = "", 
		   const string& nameReco = ""
		   ) 
{

  // if (isMuon) {
  //   cout << "Warning: at the moment this macro has hardcoded parts for electrons. Usage with muons must be implemented! Exit." << endl;
  //   exit(EXIT_FAILURE);
  // }

  //cout << Form("Getting histograms %s and %s from file %s", nameGen.c_str(), nameReco.c_str(), inputFile.c_str()) << endl;

  TH1D* hgen = nullptr;
  TH1D* hreco = nullptr;
  TH1D* hreco_over_gen = nullptr;

  TFile* file = new TFile(inputFile.c_str(),"READ");
  if (!file || file->IsZombie()) {
    cout << "Error: file " << inputFile << " not opened. Exit" << endl;
    exit(EXIT_FAILURE);
  }

  file->cd();
  hgen  = (TH1D*) getHistCloneFromFile(file, nameGen);
  hreco = (TH1D*) getHistCloneFromFile(file, nameReco);
  checkNotNullPtr(hgen, nameGen);
  checkNotNullPtr(hreco, nameReco);
  hgen->SetDirectory(0);
  hreco->SetDirectory(0);

  hreco_over_gen = (TH1D*) hreco->Clone();
  hreco_over_gen->Divide(hgen);
  hreco_over_gen->SetDirectory(0);

  file->Close();

  delete file;
  return hreco_over_gen;

}

//==================================================================

// each file might have the LO histograms: their names end with '_LO'
// if you pass compareWithLO, an additional folder is created for each file, and inside the NLO and LO samples are compared

void plotEfficiency(const string& inputFilePath = "/afs/cern.ch/work/m/mciprian/w_mass_analysis/heppy/CMSSW_8_0_25/src/CMGTools/WMass/python/plotter/eff_tightCharge_chargeMatch_absY/", 
		    const TString& inputFileNameList = "mc_reco_eff.root",	
		    const TString& legendEntryList = "PF M_{T} > 40",
		    const string& outDir = "www/wmass/13TeV/efficiency_NLO_tightCharge_chargeMatch_absY/",
		    const string& xvar = "abswy",
		    const Bool_t compareWithLO = true,
		    const Bool_t compareWithSmear = true,
		    const TString& inputFileNameWithSmearList= "mc_reco_eff.root",
		    const Bool_t isMuon = false 
		    ) 
// void plotEfficiency(const string& inputFilePath = "/afs/cern.ch/work/m/mdunser/public/cmssw/w-helicity-13TeV/CMSSW_8_0_25/src/CMGTools/WMass/python/plotter/cards/helicity_2018_03_29_PFMT40_pdfSyst_GRANDECOMBINAZIONE/", 
// 		    const TString& inputFileNameList = "scalefile_PFMT40_LONLO.root",	
// 		    const TString& legendEntryList = "PF M_{T} > 40",
// 		    const string& outDir = "www/wmass/13TeV/efficiency_muon/",
//		    const string& xvar = "abswy",
// 		    const Bool_t compareWithLO = true,
// 		    const Bool_t compareWithSmear = false,
// 		    const TString& inputFileNameWithSmearList= "",
// 		    const Bool_t isMuon = true 
// 		    ) 
// void plotEfficiency(const string& inputFilePath = "/afs/cern.ch/work/m/mciprian/w_mass_analysis/heppy/CMSSW_8_0_25/src/CMGTools/WMass/python/plotter/eff_tightCharge_chargeMatch/", 
// 		    const TString& inputFileNameList = "mc_reco_eff.root,mc_reco_pfmt30_eff.root,mc_reco_pfmt40_eff.root,mc_reco_pfmt50_eff.root",	
// 		    const TString& legendEntryList = "no PF M_{T},PF M_{T} > 30,PF M_{T} > 40,PF M_{T} > 50",
// 		    const string& outDir = "www/wmass/13TeV/efficiency_NLO_tightCharge_chargeMatch/",
//		    const string& xvar = "abswy",
// 		    const Bool_t compareWithLO = true,
// 		    const Bool_t compareWithSmear = true,
// 		    const TString& inputFileNameWithSmearList= "mc_reco_pfmt30_eff.root,mc_reco_pfmt40_eff.root,mc_reco_pfmt50_eff.root",
// 		    const Bool_t isMuon = false 
// 		    ) 
{


  createPlotDirAndCopyPhp(outDir);
  adjustSettings_CMS_lumi(outDir);

  vector<TString> inputFileNames;
  cout << "Input file names: " << endl;
  getVectorTStringFromTStringList(inputFileNames, inputFileNameList, ",", true);

  vector<TString> inputFileNamesWithSmear;
  //cout << "Input file names: " << endl;
  getVectorTStringFromTStringList(inputFileNamesWithSmear, inputFileNameWithSmearList, ",", false);

  vector<string> heffsLegEntry;
  cout << "Legend entries: " << endl;
  getVectorCStringFromTStringList(heffsLegEntry, legendEntryList, ",", true);

  vector<string> names;
  names.push_back(Form("wminus_%s_Wminus_left",xvar.c_str()));
  names.push_back(Form("wminus_%s_Wminus_long",xvar.c_str()));
  names.push_back(Form("wminus_%s_Wminus_right",xvar.c_str()));
  names.push_back(Form("wplus_%s_Wplus_left",xvar.c_str()));
  names.push_back(Form("wplus_%s_Wplus_long",xvar.c_str()));
  names.push_back(Form("wplus_%s_Wplus_right",xvar.c_str()));

  string nameReco = "";
  Int_t xvarMatchLength = xvar.size() + 2; // we take into account _ before and after xvar. e.g.: xvar = wy --> 2 +2; xvar = abswy --> 5 + 2

  for (UInt_t i = 0; i < names.size(); ++i) {
    
    nameReco = names[i];
    nameReco.insert(nameReco.find(Form("_%s_",xvar.c_str()))+xvarMatchLength,"reco_");  

    vector<TH1*> heffs;
    vector<TH1*> heffs_LO;
    vector<TH1*> heffs_Smear;

    string canvasName = "reco_gen_efficiency_" + names[i].substr(names[i].find(Form("%s_W",xvar.c_str())));

    for (UInt_t iname = 0; iname < inputFileNames.size(); ++iname) {
      
      string efficiencyFileName = string(inputFileNames[iname].Data());
      // remove extension 
      string extension = ".root";
      string outDirTagName = efficiencyFileName.substr(0,efficiencyFileName.size()-extension.size());
      outDirTagName += "/";

      heffs.push_back( new TH1D( *((TH1D*) getEfficiency(inputFilePath+efficiencyFileName, isMuon, names[i], nameReco)) ) );
      if (compareWithLO) {
	if (isMuon) {
	  string nameGen = names[i];
	  nameGen.insert(nameGen.find(Form("_%s_",xvar.c_str())) +xvarMatchLength,"LO_");  
	  nameReco.insert(nameReco.find("_reco_")+6,"LO_");  
	  heffs_LO.push_back( new TH1D( *((TH1D*) getEfficiency(inputFilePath+efficiencyFileName, isMuon, nameGen, nameReco)) ) );   
	} else {
	  heffs_LO.push_back( new TH1D( *((TH1D*) getEfficiency(inputFilePath+efficiencyFileName, isMuon, names[i]+"_LO", nameReco+"_LO")) ) );   	
	}
	createPlotDirAndCopyPhp(outDir+outDirTagName);
	adjustSettings_CMS_lumi(outDir+outDirTagName);
	drawTH1pair((TH1*)heffs.back()->Clone(),heffs_LO.back(),"y_{W}", "Reco/gen efficiency",canvasName,outDir+outDirTagName,"NLO","LO","NLO/LO::0.9,1.1",-1.0,1,false);
      }
      if (compareWithSmear) {
	Bool_t fileHasSmear = false;
	for (UInt_t j = 0; j < inputFileNamesWithSmear.size(); ++j) {
	  if (efficiencyFileName == inputFileNamesWithSmear[j]) {
	    fileHasSmear = true;
	    break;
	  }
	}
	if (fileHasSmear) {
	  heffs_Smear.push_back( new TH1D( *((TH1D*) getEfficiency(inputFilePath+efficiencyFileName, isMuon, names[i], nameReco+"_SmearPFMET")) ) );   	
	  createPlotDirAndCopyPhp(outDir+outDirTagName);
	  adjustSettings_CMS_lumi(outDir+outDirTagName);
	  drawTH1pair((TH1*)heffs.back()->Clone(),heffs_Smear.back(),"y_{W}", "Reco/gen efficiency",canvasName+"_Smear",outDir+outDirTagName,"No smear","Smear","NLO/Smear::0.98,1.02",-1.0,1,false); 
	}
      }
    }
    
    if (heffs.size() > 1) 
      draw_nTH1(heffs, "y_{W} (NLO)", "Reco/gen efficiency", canvasName, outDir, heffsLegEntry, "x / first::0.80,1.05", -1, 1, false, true);
    if (compareWithLO and heffs_LO.size() > 1) 
      draw_nTH1(heffs_LO, "y_{W} (LO)", "Reco/gen efficiency", canvasName+"_LO", outDir, heffsLegEntry, "x / first::0.80,1.05", -1, 1, false, true);

    for (UInt_t ieff = 0; ieff < heffs.size(); ++ieff) delete heffs[ieff];
    heffs.clear(); 

    if (compareWithLO) {
      for (UInt_t ieff = 0; ieff < heffs_LO.size(); ++ieff) delete heffs_LO[ieff];
      heffs_LO.clear();
    }

    if (compareWithSmear) {
      for (UInt_t ieff = 0; ieff < heffs_Smear.size(); ++ieff) delete heffs_Smear[ieff];
      heffs_Smear.clear();
    }
  }    


}
