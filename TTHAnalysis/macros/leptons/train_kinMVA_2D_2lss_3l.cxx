//
// call this as trainMVA("2lss_ttV"), trainMVA("2lss_ttbar"), trainMVA("3l_ttV"), trainMVA("3l_ttbar")
//

#include "TString.h"

//TString Path = "/afs/cern.ch/work/p/peruzzi/tthtrees/TREES_74X_140116_MiniIso_tauClean_Mor16lepMVA/";
//TString Path = "root://eoscms.cern.ch//eos/cms/store/cmst3/user/peruzzi/tthtrees/TREES_74X_140116_MiniIso_tauClean_Mor16lepMVA/TTHnobb_pow_treeProducerSusyMultilepton_tree.root";
TString Path = "root://eoscms.cern.ch//eos/cms/store/cmst3/user/mdjordje/TTH/TREES_74X_140116_MiniIso_tauClean_Mor16lepMVA";
//TString Path = "/data1/p/peruzzi/TREES_74X_140116_MiniIso_tauClean_Mor16lepMVA/";
TString friends[3] = {TString("/2_recleaner_v4_vetoCSVM"), TString("/4_kinMVA_trainMarcoJan27_v1_fix_reliso_conept"), TString("/3_BDT2var_v0")};

#include "TFile.h"
#include "TTree.h"
#include "TMVA/Factory.h"

void addBkgAndVarsToFactory(TString name, TMVA::Factory *factory){
    if (name.Contains("ttV")) {
        TFile *fBkgW = TFile::Open(Path+"/TTWToLNu_treeProducerSusyMultilepton_tree.root");
        TTree *tBkgW = (TTree *) fBkgW->Get("tree");
	for (int i=0; i<2; i++) tBkgW->AddFriend("sf/t", Path + friends[i].Data() +"/evVarFriend_TTWToLNu.root");
        factory->AddBackgroundTree(tBkgW, 0.2043/85407.061152);
	TFile *fBkgZ = TFile::Open(Path+"/TTZToLLNuNu_treeProducerSusyMultilepton_tree.root");
        TTree *tBkgZ = (TTree *) fBkgZ->Get("tree");
	for (int i=0; i<2; i++) tBkgZ->AddFriend("sf/t", Path + friends[i].Data() +"/evVarFriend_TTZToLLNuNu.root");
        factory->AddBackgroundTree(tBkgZ, 0.2529/100112.251834);		

	if (name.Contains("2lss")){
	
	factory->AddVariable("max_Lep_eta := max(abs(LepGood_eta[iF_Recl_0]),abs(LepGood_eta[iF_Recl_1]))", 'F');
	factory->AddVariable("MT_met_lep1 := MT_met_lep1", 'F');
	factory->AddVariable("numJets_float := nJet25_Recl", 'F');
	factory->AddVariable("mindr_lep1_jet := mindr_lep1_jet", 'F');
	factory->AddVariable("mindr_lep2_jet := mindr_lep2_jet", 'F'); 
	factory->AddVariable("LepGood_conePt[iF_Recl_0] := LepGood_conePt[iF_Recl_0]", 'F');  
	factory->AddVariable("LepGood_conePt[iF_Recl_1] := LepGood_conePt[iF_Recl_1]", 'F'); 
	 
//	factory->AddVariable("BDT2 := BDT2", 'F'); 

	}
	else if (name.Contains("3l")) {

	factory->AddVariable("max_Lep_eta := max(abs(LepGood_eta[iF_Recl_0]),abs(LepGood_eta[iF_Recl_1]))", 'F');
	factory->AddVariable("MT_met_lep1 := MT_met_lep1", 'F');
	factory->AddVariable("numJets_float := nJet25_Recl", 'F');
	factory->AddVariable("mindr_lep1_jet := mindr_lep1_jet", 'F');
	factory->AddVariable("mindr_lep2_jet := mindr_lep2_jet", 'F'); 
	factory->AddVariable("LepGood_conePt[iF_Recl_0] := LepGood_conePt[iF_Recl_0]", 'F');  
	factory->AddVariable("LepGood_conePt[iF_Recl_2] := LepGood_conePt[iF_Recl_2]", 'F'); 
	
//	factory->AddVariable("BDT2 := BDT2", 'F');   

	}
	else {
	  assert(0);
	}
		
    }
    
    else if (name.Contains("ttW")) {
      TFile *fBkgW = TFile::Open(Path+"/TTWToLNu_treeProducerSusyMultilepton_tree.root");
      TTree *tBkgW = (TTree *) fBkgW->Get("tree");
      for (int i=0; i<2; i++) tBkgW->AddFriend("sf/t", Path + friends[i].Data() +"/evVarFriend_TTWToLNu.root");
      factory->AddBackgroundTree(tBkgW, 0.2043/85407.061152);          

	if (name.Contains("2lss")){
	
	factory->AddVariable("max_Lep_eta := max(abs(LepGood_eta[iF_Recl_0]),abs(LepGood_eta[iF_Recl_1]))", 'F');
	factory->AddVariable("MT_met_lep1 := MT_met_lep1", 'F');
	factory->AddVariable("numJets_float := nJet25_Recl", 'F');
	factory->AddVariable("LepGood_conePt[iF_Recl_1] := LepGood_conePt[iF_Recl_1]", 'F');
	factory->AddVariable("mindr_lep1_jet := mindr_lep1_jet", 'F');
	factory->AddVariable("mindr_lep2_jet := mindr_lep2_jet", 'F');
	
//	factory->AddVariable("BDT2 := BDT2", 'F');    
	
	}
	else if (name.Contains("3l")) {
	
	factory->AddVariable("max_Lep_eta := max(abs(LepGood_eta[iF_Recl_0]),abs(LepGood_eta[iF_Recl_1]))", 'F');
	factory->AddVariable("MT_met_lep1 := MT_met_lep1", 'F');
	factory->AddVariable("numJets_float := nJet25_Recl", 'F');
	factory->AddVariable("LepGood_conePt[iF_Recl_2] := LepGood_conePt[iF_Recl_2]", 'F');
	factory->AddVariable("mindr_lep1_jet := mindr_lep1_jet", 'F');
	factory->AddVariable("mindr_lep2_jet := mindr_lep2_jet", 'F');  
	
//	factory->AddVariable("BDT2 := BDT2", 'F');  
	  
	}
	else {
	  assert(0);
	}

    }
    
    else if (name.Contains("ttbar")) {
      TFile *fBkgTT2 = TFile::Open(Path+"/TTJets_DiLepton_treeProducerSusyMultilepton_tree.root");
      TTree *tBkgTT2 = (TTree *) fBkgTT2->Get("tree");
      for (int i=0; i<2; i++) tBkgTT2->AddFriend("sf/t", Path + friends[i].Data() +"/evVarFriend_TTJets_DiLepton.root");
      factory->AddBackgroundTree(tBkgTT2, 831.76*((3*0.108)*(3*0.108))/5927992.0);	
      TFile *fBkgTT1 = TFile::Open(Path+"/TTJets_SingleLeptonFromT_treeProducerSusyMultilepton_tree.root");
      TTree *tBkgTT1 = (TTree *) fBkgTT1->Get("tree");
      for (int i=0; i<2; i++) tBkgTT1->AddFriend("sf/t", Path + friends[i].Data() +"/evVarFriend_TTJets_SingleLeptonFromT.root");
      factory->AddBackgroundTree(tBkgTT1, 831.76*(3*0.108)*(1-3*0.108)/11564279.0);	
      TFile *fBkgTT1bar = TFile::Open(Path+"/TTJets_SingleLeptonFromTbar_treeProducerSusyMultilepton_tree.root");
      TTree *tBkgTT1bar = (TTree *) fBkgTT1bar->Get("tree");
      for (int i=0; i<2; i++) tBkgTT1bar->AddFriend("sf/t", Path + friends[i].Data() +"/evVarFriend_TTJets_SingleLeptonFromTbar.root");
      factory->AddBackgroundTree(tBkgTT1bar, 831.76*(3*0.108)*(1-3*0.108)/11723390.0);	
 
      if (name.Contains("2lss")){
      
	factory->AddVariable("max_Lep_eta := max(abs(LepGood_eta[iF_Recl_0]),abs(LepGood_eta[iF_Recl_1]))", 'F');
	factory->AddVariable("numJets_float := nJet25_Recl", 'F');
	factory->AddVariable("mindr_lep1_jet := mindr_lep1_jet", 'F');
	factory->AddVariable("mindr_lep2_jet := mindr_lep2_jet", 'F');   
	factory->AddVariable("met := min(met_pt, 400)", 'F');
        factory->AddVariable("avg_dr_jet : = avg_dr_jet", 'F');
	factory->AddVariable("MT_met_lep1 := MT_met_lep1", 'F');
	
//	factory->AddVariable("BDT2 := BDT2", 'F'); 

      }
      else if (name.Contains("3l")) {
      
	factory->AddVariable("max_Lep_eta := max(abs(LepGood_eta[iF_Recl_0]),abs(LepGood_eta[iF_Recl_1]))", 'F');
	factory->AddVariable("MT_met_lep1 := MT_met_lep1", 'F');
	factory->AddVariable("numJets_float := nJet25_Recl", 'F');
	factory->AddVariable("mhtJet25 := mhtJet25_Recl", 'F'); 
        factory->AddVariable("avg_dr_jet : = avg_dr_jet", 'F');
	factory->AddVariable("mindr_lep1_jet := mindr_lep1_jet", 'F');
	factory->AddVariable("mindr_lep2_jet := mindr_lep2_jet", 'F');  
	
//	factory->AddVariable("BDT2 := BDT2", 'F');  
	
      }
      else {
	assert(0);
      }
      
    }

    factory->AddSpectator("iF0 := iF_Recl_0","F"); // do not remove this!
    factory->AddSpectator("iF1 := iF_Recl_1","F"); // do not remove this!
    factory->AddSpectator("iF2 := iF_Recl_2","F"); // do not remove this!

};

void trainMVA(TString name) {

    TFile *fOut = new TFile(name+".root","RECREATE");
    TMVA::Factory *factory = new TMVA::Factory(name, fOut, "!V:!Color");
    
    TCut all;
    if (name.Contains("2lss")) {
      all = "nLepFO_Recl>=2 && LepGood_conePt[iF_Recl_0]>20 && LepGood_conePt[iF_Recl_1]>10 && LepGood_charge[iF_Recl_0] == LepGood_charge[iF_Recl_1] && (nBJetLoose25_Recl >= 2 || nBJetMedium25_Recl >= 1) && nJet25_Recl >= 4";
    }
    else if (name.Contains("3l")) {
      all = "nLepFO_Recl>=3 && abs(mZ1_Recl-91.2)>10 && LepGood_conePt[iF_Recl_0]>20 && LepGood_conePt[iF_Recl_1]>10 && LepGood_conePt[iF_Recl_2]>10 && (nJet25_Recl >= 4 || (met_pt*0.00397 + mhtJet25_Recl*0.00265 - 0.184 > 0.0 + 0.1*(mZ1_Recl > 0))) && nBJetLoose25_Recl >= 2";
    }
    else {
      assert(0);
    }

    TFile *fSig = TFile::Open(Path+"/TTHnobb_pow_treeProducerSusyMultilepton_tree.root");
    TTree *tSig = (TTree *) fSig->Get("tree");
    for (int i=0; i<2; i++) tSig->AddFriend("sf/t", Path + friends[i].Data() +"/evVarFriend_TTHnobb_pow.root");
    factory->AddSignalTree(tSig, 0.5085*(1-0.577)/3824936.0);
    
    addBkgAndVarsToFactory(name,factory);

    factory->SetWeightExpression("genWeight");
    factory->PrepareTrainingAndTestTree( all, all, "SplitMode=Random" );

    ///   factory->BookMethod( TMVA::Types::kLD, "LD", "!H:!V:VarTransform=None:CreateMVAPdfs" );

    //    TString BDTGopt = "!H:!V:NTrees=200:BoostType=Grad:Shrinkage=0.10:!UseBaggedGrad:nCuts=200:nEventsMin=100:NNodesMax=5";  // use this only if all positive weights
    TString BDTGopt = "!H:!V:NTrees=200:BoostType=Grad:Shrinkage=0.10:!UseBaggedGrad:nCuts=200:nEventsMin=100:NNodesMax=5:NegWeightTreatment=PairNegWeightsGlobal";
        
    BDTGopt += ":CreateMVAPdfs"; // Create Rarity distribution
    factory->BookMethod( TMVA::Types::kBDT, "BDTG", BDTGopt);

    factory->TrainAllMethods();
    factory->TestAllMethods();
    factory->EvaluateAllMethods();

    fOut->Close();
}
