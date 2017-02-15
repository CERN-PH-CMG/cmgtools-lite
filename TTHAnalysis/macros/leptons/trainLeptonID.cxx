#include <assert.h>

void trainLeptonID(TString name, TString sig1file, TString sig2file, TString bkg1file, TString bkg2file, bool doMultiClass = false, TString file_for_sigW_1="", TString file_for_sigW_2="", TString file_for_bkgW_1="", TString file_for_bkgW_2="", double int1s=0, double int2s=0, double int1b=0, double int2b=0) {
    TFile *_f_s1 = TFile::Open(sig1file.Data(),"read");
    TFile *_f_s2 =  (sig2file=="") ? NULL : TFile::Open(sig2file.Data(),"read");
    TFile *_f_b1 = TFile::Open(bkg1file.Data(),"read");
    TFile *_f_b2 =  (bkg2file=="") ? NULL : TFile::Open(bkg2file.Data(),"read");
    TTree *dSig1 = (TTree*) _f_s1->Get("tree");
    TTree *dSig2 = (_f_s2) ? ((TTree*) _f_s2->Get("tree")) : NULL;
    if (file_for_sigW_1!="") dSig1->AddFriend("wtree",file_for_sigW_1.Data());
    if (file_for_sigW_2!="") dSig2->AddFriend("wtree",file_for_sigW_2.Data());
    TTree *dBg1 = (TTree*) _f_b1->Get("tree");
    TTree *dBg2 = (_f_b2) ? ((TTree*) _f_b2->Get("tree")) : NULL;
    if (file_for_bkgW_1!="") dBg1->AddFriend("wtree",file_for_bkgW_1.Data());
    if (file_for_bkgW_2!="") dBg2->AddFriend("wtree",file_for_bkgW_2.Data());
    TFile *fOut = new TFile(name+".root","RECREATE");
    TString factory_conf = (!doMultiClass) ? "!V:!Color:Transformations=I" : "!V:!Color:Transformations=I:AnalysisType=Multiclass";
    TMVA::Factory *factory = new TMVA::Factory(name, fOut, factory_conf.Data());

    TCut lepton = "1";
    
    if (name.Contains("forMoriond")) {
        factory->AddVariable("LepGood_pt", 'D');
        factory->AddVariable("LepGood_eta", 'D');
	factory->AddVariable("LepGood_jetNDauChargedMVASel", 'D');
	factory->AddVariable("LepGood_miniRelIsoCharged", 'D');
	factory->AddVariable("LepGood_miniRelIsoNeutral", 'D');
	factory->AddVariable("LepGood_jetPtRelv2", 'D');
	factory->AddVariable("LepGood_jetPtRatio := min(LepGood_jetPtRatiov2,1.5)", 'D');
	factory->AddVariable("LepGood_jetBTagCSV := max(LepGood_jetBTagCSV,0)", 'D');
        factory->AddVariable("LepGood_sip3d", 'D'); 
        factory->AddVariable("LepGood_dxy := log(abs(LepGood_dxy))", 'D');
        factory->AddVariable("LepGood_dz  := log(abs(LepGood_dz))",  'D');
	lepton += "LepGood_miniRelIso<0.4 && LepGood_sip3d < 8";
	if (name.Contains("_mu")) {
	  factory->AddVariable("LepGood_segmentCompatibility",'D');
	} else if (name.Contains("_el")) {
	  if (name.Contains("_eleHZZ")) factory->AddVariable("LepGood_mvaIdSpring16HZZ",'D');
	  else if (name.Contains("_eleGP")) factory->AddVariable("LepGood_mvaIdSpring16GP",'D');
	  else if (name.Contains("_eleOLD")) factory->AddVariable("LepGood_mvaIdSpring15",'D');
	  else assert(0);
	}
	else { std::cerr << "ERROR: must either be electron or muon." << std::endl; return; }
	
    }
    else if (name.Contains("asMultiIso")){
	factory->AddVariable("LepGood_miniRelIso", 'D');
	factory->AddVariable("LepGood_jetPtRelv2", 'D');
	factory->AddVariable("LepGood_jetPtRatio := min(LepGood_jetPtRatiov2,1.5)", 'D');
	lepton += "LepGood_miniRelIso<0.4 && LepGood_sip3d < 8";
    }

    else if (name.Contains("SoftJetLess")){
      factory->AddSpectator("LepGood_mcMatchAny", 'D');
      factory->AddVariable("LepGood_pt", 'D');
      factory->AddVariable("LepGood_eta", 'D');
      factory->AddVariable("LepGood_miniRelIsoCharged := min(LepGood_miniRelIsoCharged,4)", 'D');
      factory->AddVariable("LepGood_miniRelIsoNeutral := min(LepGood_miniRelIsoNeutral,4)", 'D');
      if (!(name.Contains("NO04ISO"))){
	factory->AddVariable("LepGood_isoRelH04", 'D');
	factory->AddVariable("LepGood_RelIsoChargedFix04 := min(LepGood_RelIsoChargedFix04,4)", 'D');
	factory->AddVariable("LepGood_RelIsoNeutralFix04 := min(LepGood_RelIsoNeutralFix04,4)", 'D');
      }

      if (name.Contains("IVF")){
	factory->AddVariable("LepGood_hasSV", 'D');
	factory->AddVariable("LepGood_svSip3d := max(LepGood_svSip3d,0)", 'D');
	factory->AddVariable("LepGood_svRedPt := max(LepGood_svRedPt,0)", 'D');
	factory->AddVariable("LepGood_svMass := max(LepGood_svMass,0)", 'D');
	factory->AddVariable("LepGood_svNTracks := max(LepGood_svNTracks,0)", 'D');
      }
      else if (name.Contains("SVSafe")){
	factory->AddVariable("LepGood_hasSV := (LepGood_hasSV>1)*(LepGood_hasSV)", 'D');
	factory->AddVariable("LepGood_svSip3d := (LepGood_hasSV>1)*(max(LepGood_svSip3d,0))", 'D');
	factory->AddVariable("LepGood_svRedPt := (LepGood_hasSV>1)*(max(LepGood_svRedPt,0))", 'D');
	factory->AddVariable("LepGood_svMass := (LepGood_hasSV>1)*(max(LepGood_svMass,0))", 'D');
	factory->AddVariable("LepGood_svNTracks := (LepGood_hasSV>1)*(max(LepGood_svNTracks,0))", 'D');	
      }
      else if (name.Contains("NOBTAG")){
      }
      else {
	factory->AddVariable("LepGood_jetBTagCSV := max(LepGood_jetBTagCSV,0)", 'D');
      }

      factory->AddVariable("LepGood_sip3d", 'D');
      factory->AddVariable("LepGood_dxy := log(abs(LepGood_dxy))", 'D');
      factory->AddVariable("LepGood_dz  := log(abs(LepGood_dz))",  'D');

      lepton += "LepGood_pt<30 && LepGood_pt>3.5 && (abs(LepGood_pdgId)==11 || LepGood_pt>5) && LepGood_RelIsoFix04*LepGood_pt<10 && LepGood_sip3d<8 && (abs(LepGood_pdgId)!=11 || (abs(LepGood_etaSc)<0.8 && LepGood_mvaIdSpring15 > -0.70) || (abs(LepGood_etaSc)>=0.8 && abs(LepGood_etaSc)<1.479 && LepGood_mvaIdSpring15 > -0.83) || (abs(LepGood_etaSc)>=1.479 && LepGood_mvaIdSpring15 > -0.92))";
      if (name.Contains("NOTAU")) lepton += "LepGood_mcMatchId==0 || LepGood_mcMatchTau!=1";

	if (name.Contains("_mu")) {
	  if (name.Contains("MuMVAID")){
	    factory->AddVariable("LepGood_trackerLayers",'D');
	    factory->AddVariable("LepGood_pixelLayers",'D');
	    factory->AddVariable("LepGood_innerTrackValidHitFraction",'D');
	    factory->AddVariable("LepGood_trkKink := min(LepGood_trkKink,400)",'D');
	    factory->AddVariable("LepGood_chi2LocalPosition",'D');
	  }
	  if (name.Contains("MuCBID")){
	    factory->AddVariable("LepGood_mediumMuonId",'D');
	  }
	  factory->AddVariable("LepGood_segmentCompatibility",'D');
	} else if (name.Contains("_el")) {
	  factory->AddVariable("LepGood_mvaIdSpring15",'D');
	}

    }
    else if (name.Contains("SoftALaMoriond16")) {
      factory->AddSpectator("LepGood_mcMatchAny", 'D');
        factory->AddVariable("LepGood_pt", 'D');
        factory->AddVariable("LepGood_eta", 'D');
	factory->AddVariable("LepGood_jetNDauChargedMVASel", 'D');
	factory->AddVariable("LepGood_miniRelIsoCharged", 'D');
	factory->AddVariable("LepGood_miniRelIsoNeutral", 'D');
	factory->AddVariable("LepGood_jetPtRelv2", 'D');
	factory->AddVariable("LepGood_jetPtRatio := min(LepGood_jetPtRatiov2,1.5)", 'D');
	factory->AddVariable("LepGood_jetBTagCSV := max(LepGood_jetBTagCSV,0)", 'D');
        factory->AddVariable("LepGood_sip3d", 'D'); 
        factory->AddVariable("LepGood_dxy := log(abs(LepGood_dxy))", 'D');
        factory->AddVariable("LepGood_dz  := log(abs(LepGood_dz))",  'D');

	lepton += "LepGood_pt<20 && LepGood_pt>3.5 && LepGood_miniRelIso<0.4 && LepGood_sip3d<8";

	if (name.Contains("_mu")) {
	  factory->AddVariable("LepGood_segmentCompatibility",'D');

	} else if (name.Contains("_el")) {
	  factory->AddVariable("LepGood_mvaIdSpring15",'D');
	}
	
    }


    if (name.Contains("mu")) {
      lepton += "abs(LepGood_pdgId) == 13";
    } else if (name.Contains("el")) {
      lepton += "abs(LepGood_pdgId) == 11";
    }

    double wSig = 1.0, wBkg = 1.0;
    if (!doMultiClass){
      if (!dSig2) factory->AddSignalTree(dSig1, wSig);
      else {
	std::cout << "Adding signal tree 1 and 2 with respective weights: " << wSig/int1s/2. << " " << wSig/int2s/2. << std::endl;
	factory->AddSignalTree(dSig1, wSig/int1s/2.);
	factory->AddSignalTree(dSig2, wSig/int2s/2.);
      }
      if (!dBg2) factory->AddBackgroundTree(dBg1, wBkg);
      else {
	std::cout << "Adding background tree 1 and 2 with respective weights: " << wBkg/int1b/2. << " " << wBkg/int2b/2. << std::endl;
	factory->AddBackgroundTree(dBg1, wBkg/int1b/2.);
	factory->AddBackgroundTree(dBg2, wBkg/int2b/2.);
      }
    }
    else {
      if (!dSig2) factory->AddTree(dSig1,"signal",wSig, "LepGood_mcMatchId!=0");
      else {
	factory->AddTree(dSig1, "signal", wSig/int1s/2., "LepGood_mcMatchId!=0");
	factory->AddTree(dSig2, "signal", wSig/int2s/2., "LepGood_mcMatchId!=0");
      }
      if (!dBg2) {
	factory->AddTree(dBg1, "bfake", wBkg, "LepGood_mcMatchId==0 && (abs(LepGood_mcMatchAny)==4 || abs(LepGood_mcMatchAny)==5)");
	factory->AddTree(dBg1, "light", wBkg, "LepGood_mcMatchId==0 && (abs(LepGood_mcMatchAny)<4 || abs(LepGood_mcMatchAny)>5)");
      }
      else {
	factory->AddTree(dBg1, "bfake", wBkg/int1b/2., "LepGood_mcMatchId==0 && (abs(LepGood_mcMatchAny)==4 || abs(LepGood_mcMatchAny)==5)");
	factory->AddTree(dBg1, "light", wBkg/int1b/2., "LepGood_mcMatchId==0 && (abs(LepGood_mcMatchAny)<4 || abs(LepGood_mcMatchAny)>5)");
	factory->AddTree(dBg2, "bfake", wBkg/int2b/2., "LepGood_mcMatchId==0 && (abs(LepGood_mcMatchAny)==4 || abs(LepGood_mcMatchAny)==5)");
	factory->AddTree(dBg2, "light", wBkg/int2b/2., "LepGood_mcMatchId==0 && (abs(LepGood_mcMatchAny)<4 || abs(LepGood_mcMatchAny)>5)");
      }
    }

    if (file_for_sigW_1!="" || file_for_sigW_2!="") factory->SetSignalWeightExpression("addW*xsec*genWeight");
    else factory->SetSignalWeightExpression("xsec*genWeight");
    if (file_for_bkgW_1!="" || file_for_bkgW_2!="") factory->SetBackgroundWeightExpression("addW*xsec*genWeight");
    else factory->SetBackgroundWeightExpression("xsec*genWeight");

    if (!doMultiClass) factory->PrepareTrainingAndTestTree( lepton+" LepGood_mcMatchId != 0", lepton+" LepGood_mcMatchId == 0", "" );
    else factory->PrepareTrainingAndTestTree(lepton,"SplitMode=Random:NormMode=NumEvents:!V");

    //    if (!doMultiClass) factory->BookMethod( TMVA::Types::kLD, "LD", "!H:!V:VarTransform=None" );
    
    // Boosted Decision Trees with gradient boosting
    TString BDTGopt = "!H:!V:NTrees=500:BoostType=Grad:Shrinkage=0.10:!UseBaggedGrad:nCuts=2000:nEventsMin=100:NNodesMax=9:UseNvars=9:MaxDepth=8";

    // alternative options
    //TString BDTGopt = "!H:!V:NTrees=1000:BoostType=Grad:Shrinkage=0.10:!UseBaggedGrad:nCuts=2000:nEventsMin=100:MaxDepth=3";
    //TString BDTGopt = "!H:!V:NTrees=1000:BoostType=Grad:Shrinkage=0.10:!UseBaggedGrad:nCuts=2000";

    if (!doMultiClass) BDTGopt += ":CreateMVAPdfs"; // Create Rarity distribution
    factory->BookMethod( TMVA::Types::kBDT, "BDTG", BDTGopt);

    factory->TrainAllMethods();
    factory->TestAllMethods();
    factory->EvaluateAllMethods();

    fOut->Close();
}
