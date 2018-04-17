#include "../interface/utility.h"

using namespace std;


//================================================================

TH1* getEfficiency(const string& inputFile = "", 
		   const Bool_t isMuon = false,
		   const string& nameGen = "", 
		   const string& nameReco = ""
		   ) 
{

  if (isMuon) {
    cout << "Warning: at the moment this macro has hardcoded parts for electrons. Usage with muons must be implemented! Exit." << endl;
    exit(EXIT_FAILURE);
  }

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

void plotEfficiency(const string& inputFilePath = "/afs/cern.ch/work/m/mciprian/w_mass_analysis/heppy/CMSSW_8_0_25/src/CMGTools/WMass/data/efficiency/", 
		    const TString& inputFileNameList = "mc_reco_eff.root,mc_reco_pfmt30_eff.root,mc_reco_pfmt40_eff.root,mc_reco_pfmt50_eff.root",	
		    const TString& legendEntryList = "no PF M_{T},PF M_{T} > 30,PF M_{T} > 40,PF M_{T} > 50",
		    const string& outDir = "www/wmass/13TeV/efficiency_NLO_tightCharge/",
		    const Bool_t compareWithLO = true,
		    const Bool_t isMuon = false 
		    ) 
{


  createPlotDirAndCopyPhp(outDir);
  adjustSettings_CMS_lumi(outDir);

  vector<TString> inputFileNames;
  cout << "Input file names: " << endl;
  getVectorTStringFromTStringList(inputFileNames, inputFileNameList, ",", true);

  vector<string> heffsLegEntry;
  cout << "Legend entries: " << endl;
  getVectorCStringFromTStringList(heffsLegEntry, legendEntryList, ",", true);

  vector<string> names;
  names.push_back("wminus_wy_Wminus_left");
  names.push_back("wminus_wy_Wminus_long");
  names.push_back("wminus_wy_Wminus_right");
  names.push_back("wplus_wy_Wplus_left");
  names.push_back("wplus_wy_Wplus_long");
  names.push_back("wplus_wy_Wplus_right");

  string nameReco = "";

  for (UInt_t i = 0; i < names.size(); ++i) {
    
    nameReco = names[i];
    nameReco.insert(nameReco.find("_wy_")+4,"reco_");  

    vector<TH1*> heffs;
    vector<TH1*> heffs_LO;

    string canvasName = "reco_gen_efficiency_" + names[i].substr(names[i].find("wy_W"));

    for (UInt_t iname = 0; iname < inputFileNames.size(); ++iname) {
      
      string efficiencyFileName = string(inputFileNames[iname].Data());
      // remove extension 
      string extension = ".root";
      string outDirTagName = efficiencyFileName.substr(0,efficiencyFileName.size()-extension.size());
      outDirTagName += "/";

      heffs.push_back( new TH1D( *((TH1D*) getEfficiency(inputFilePath+efficiencyFileName, isMuon, names[i], nameReco)) ) );
      if (compareWithLO) {
	heffs_LO.push_back( new TH1D( *((TH1D*) getEfficiency(inputFilePath+efficiencyFileName, isMuon, names[i]+"_LO", nameReco+"_LO")) ) );   	
	createPlotDirAndCopyPhp(outDir+outDirTagName);
	adjustSettings_CMS_lumi(outDir+outDirTagName);
	drawTH1pair((TH1*)heffs.back()->Clone(),heffs_LO.back(),"y_{W}", "Reco/gen efficiency",canvasName,outDir+outDirTagName,"NLO","LO","NLO/LO::0.9,1.1",-1.0,1,false);
      }

    }
    
    draw_nTH1(heffs, "y_{W} (NLO)", "Reco/gen efficiency", canvasName, outDir, heffsLegEntry, "x / first::0.80,1.05", -1, 1, false, true);
    if (compareWithLO) draw_nTH1(heffs_LO, "y_{W} (LO)", "Reco/gen efficiency", canvasName+"_LO", outDir, heffsLegEntry, "x / first::0.80,1.05", -1, 1, false, true);

    for (UInt_t ieff = 0; ieff < heffs.size(); ++ieff) delete heffs[ieff];
    heffs.clear(); 
    if (compareWithLO) {
      for (UInt_t ieff = 0; ieff < heffs_LO.size(); ++ieff) delete heffs_LO[ieff];
    heffs_LO.clear();
    }

  }    


}
