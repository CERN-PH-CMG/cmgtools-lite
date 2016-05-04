void trainLeptonID(TString name, TString sig1file, TString sig2file, TString bkg1file, TString bkg2file, bool doMultiClass = false) {
    TFile *_f_s1 = new TFile(sig1file.Data(),"read");
    TFile *_f_s2 =  (sig2file=="") ? NULL : new TFile(sig2file.Data(),"read");
    TFile *_f_b1 = new TFile(bkg1file.Data(),"read");
    TFile *_f_b2 =  (bkg2file=="") ? NULL : new TFile(bkg2file.Data(),"read");
    TTree *dSig1 = (TTree*) _f_s1->Get("tree");
    TTree *dSig2 = (_f_s2) ? ((TTree*) _f_s2->Get("tree")) : NULL;
    TTree *dBg1 = (TTree*) _f_b1->Get("tree");
    TTree *dBg2 = (_f_b2) ? ((TTree*) _f_b2->Get("tree")) : NULL;
    TFile *fOut = new TFile(name+".root","RECREATE");
    TString factory_conf = (!doMultiClass) ? "!V:!Color:Transformations=I" : "!V:!Color:Transformations=I:AnalysisType=Multiclass";
    TMVA::Factory *factory = new TMVA::Factory(name, fOut, factory_conf.Data());

    TCut lepton = "1";
    
    if (name.Contains("forMoriond16")) {
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
	  factory->AddVariable("LepGood_mvaIdSpring15",'D');
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
      factory->AddVariable("LepGood_isoRelH04", 'D');
      factory->AddVariable("LepGood_RelIsoChargedFix04 := min(LepGood_RelIsoChargedFix04,4)", 'D');
      factory->AddVariable("LepGood_RelIsoNeutralFix04 := min(LepGood_RelIsoNeutralFix04,4)", 'D');

      if (name.Contains("IVF")){
	factory->AddVariable("LepGood_hasSV", 'D');
	factory->AddVariable("LepGood_svSip3d := max(LepGood_svSip3d,0)", 'D');
	factory->AddVariable("LepGood_svRedPt := max(LepGood_svRedPt,0)", 'D');
	factory->AddVariable("LepGood_svMass := max(LepGood_svMass,0)", 'D');
	factory->AddVariable("LepGood_svNTracks := max(LepGood_svNTracks,0)", 'D');
      }
      else {
	factory->AddVariable("LepGood_jetBTagCSV := max(LepGood_jetBTagCSV,0)", 'D');
      }

      factory->AddVariable("LepGood_sip3d", 'D');
      factory->AddVariable("LepGood_dxy := log(abs(LepGood_dxy))", 'D');
      factory->AddVariable("LepGood_dz  := log(abs(LepGood_dz))",  'D');

      lepton += "LepGood_pt<20 && LepGood_pt>3.5 && LepGood_miniRelIso<0.4 && LepGood_sip3d<8";

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
	double int1 = dSig1->GetEntries();
	double int2 = dSig2->GetEntries();
	factory->AddSignalTree(dSig1, wSig/int1/2.);
	factory->AddSignalTree(dSig2, wSig/int2/2.);
      }
      if (!dBg2) factory->AddBackgroundTree(dBg1, wBkg);
      else {
	double int1 = dBg1->GetEntries();
	double int2 = dBg2->GetEntries();
	factory->AddBackgroundTree(dBg1, wBkg/int1/2.);
	factory->AddBackgroundTree(dBg2, wBkg/int2/2.);
      }
    }
    else {
      if (!dSig2) factory->AddTree(dSig1,"signal",wSig, "LepGood_mcMatchId!=0");
      else {
	double int1 = dSig1->GetEntries();
	double int2 = dSig2->GetEntries();
	factory->AddTree(dSig1, "signal", wSig/int1/2., "LepGood_mcMatchId!=0");
	factory->AddTree(dSig2, "signal", wSig/int2/2., "LepGood_mcMatchId!=0");
      }
      if (!dBg2) {
	factory->AddTree(dBg1, "bfake", wBkg, "LepGood_mcMatchId==0 && (abs(LepGood_mcMatchAny)==4 || abs(LepGood_mcMatchAny)==5)");
	factory->AddTree(dBg1, "light", wBkg, "LepGood_mcMatchId==0 && (abs(LepGood_mcMatchAny)<4 || abs(LepGood_mcMatchAny)>5)");
      }
      else {
	double int1 = dBg1->GetEntries();
	double int2 = dBg2->GetEntries();
	factory->AddTree(dBg1, "bfake", wBkg/int1/2., "LepGood_mcMatchId==0 && (abs(LepGood_mcMatchAny)==4 || abs(LepGood_mcMatchAny)==5)");
	factory->AddTree(dBg1, "light", wBkg/int1/2., "LepGood_mcMatchId==0 && (abs(LepGood_mcMatchAny)<4 || abs(LepGood_mcMatchAny)>5)");
	factory->AddTree(dBg2, "bfake", wBkg/int2/2., "LepGood_mcMatchId==0 && (abs(LepGood_mcMatchAny)==4 || abs(LepGood_mcMatchAny)==5)");
	factory->AddTree(dBg2, "light", wBkg/int2/2., "LepGood_mcMatchId==0 && (abs(LepGood_mcMatchAny)<4 || abs(LepGood_mcMatchAny)>5)");
      }
    }

    if (!doMultiClass) factory->PrepareTrainingAndTestTree( lepton+" LepGood_mcMatchId != 0", lepton+" LepGood_mcMatchId == 0", "" );
    else factory->PrepareTrainingAndTestTree(lepton,"SplitMode=Random:NormMode=NumEvents:!V");

    //    if (!doMultiClass) factory->BookMethod( TMVA::Types::kLD, "LD", "!H:!V:VarTransform=None" );
    
    // Boosted Decision Trees with gradient boosting
    TString BDTGopt = "!H:!V:NTrees=500:BoostType=Grad:Shrinkage=0.10:!UseBaggedGrad:nCuts=2000:nEventsMin=100:NNodesMax=9:UseNvars=9:MaxDepth=8";

    if (!doMultiClass) BDTGopt += ":CreateMVAPdfs"; // Create Rarity distribution
    factory->BookMethod( TMVA::Types::kBDT, "BDTG", BDTGopt);

    factory->TrainAllMethods();
    factory->TestAllMethods();
    factory->EvaluateAllMethods();

    fOut->Close();
}
