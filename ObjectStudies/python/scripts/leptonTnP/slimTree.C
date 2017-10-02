void slimTree(TString out="slimTree.root", TString cut="(tag_IsoMu22 || tag_IsoMu24) && tag_combRelIsoPF03dBeta/tag_pt < 0.2 && tag_SIP < 2.5 && (pt > 20 || TM || Glb) && (65 <= mass && mass <= 125)", TString dir="tpTree") {
    TTree *in  = (TTree *)gFile->Get(dir+"/fitter_tree");
    TFile *fout = new TFile(out, "RECREATE");
    TDirectory *dout = fout->mkdir(dir); dout->cd();

    std::cout << "Selecting branches" << std::endl;
    // Switch off everything
    in->SetBranchStatus("*", 0);

    // Necessary
    in->SetBranchStatus("mass",1);
    in->SetBranchStatus("pt",1); in->SetBranchStatus("abseta",1); in->SetBranchStatus("eta",1); in->SetBranchStatus("phi",1);
    in->SetBranchStatus("mt",1);

    // A few more ID requirements 
    in->SetBranchStatus("PF",1);
    in->SetBranchStatus("Glb",1); 
    in->SetBranchStatus("Medium",1);
    in->SetBranchStatus("Medium2016",1);
    in->SetBranchStatus("TM",1); in->SetBranchStatus("TMA",1); 
    in->SetBranchStatus("combRelIsoPF04dBeta",1);
    in->SetBranchStatus("combRelIsoPF03dBeta",1);
    in->SetBranchStatus("numberOfMatchedStations",1);
    in->SetBranchStatus("tkPixelLay",1);
    in->SetBranchStatus("tkTrackerLay",1);
    in->SetBranchStatus("tkValidPixelHits",1);
    in->SetBranchStatus("TMOST",1);
    in->SetBranchStatus("Track_HP",1);
    in->SetBranchStatus("isoTrk03Rel",1);

    // Impact parameter
    in->SetBranchStatus("IP",1);
    in->SetBranchStatus("SIP",1);
    in->SetBranchStatus("dzPV",1);
    in->SetBranchStatus("dB",1);

    if (in->GetBranch("run"))    in->SetBranchStatus("run",1);
    if (in->GetBranch("mcTrue")) in->SetBranchStatus("mcTrue",1);

    in->SetBranchStatus("tag_nVertices",1);
    in->SetBranchStatus("tag_IsoMu22",1); 
    in->SetBranchStatus("tag_IsoMu24",1); 
    in->SetBranchStatus("tag_combRelIsoPF03dBeta",1); 
    in->SetBranchStatus("tag_pt",1);
    in->SetBranchStatus("tag_SIP",1);
    in->SetBranchStatus("tag_met",1);
    in->SetBranchStatus("tag_mt",1);
    in->SetBranchStatus("tag_instLumi",1);

    in->SetBranchStatus("pair_nJets30",1);
    in->SetBranchStatus("pair_probeMultiplicity_TMGM",1);
    in->SetBranchStatus("pair_probeMultiplicity_Pt10_M60140",1);
    in->SetBranchStatus("pair_BestZ",1);

    in->SetBranchStatus("miniIsoCharged",1);
    in->SetBranchStatus("miniIsoNeutrals",1);
    in->SetBranchStatus("miniIsoPhotons",1);
    //in->SetBranchStatus("activity_miniIsoCharged",1);
    //in->SetBranchStatus("activity_miniIsoPUCharged",1);
    //in->SetBranchStatus("activity_miniIsoNeutrals",1);
    //in->SetBranchStatus("activity_miniIsoPhotons",1);
    in->SetBranchStatus("fixedGridRhoFastjetCentralNeutral",1);


    std::cout << "Selecting entries" << std::endl;
    in->Draw(">>elist",cut);

    std::cout << "Applying selection" << std::endl;
    in->SetEventList((TEventList*)gDirectory->Get("elist"));

    std::cout << "Copying trees" << std::endl;
    TTree *tout = in->CopyTree("1");

    std::cout << "INPUT TREE (" << in->GetEntries() << " ENTRIES)" << std::endl;
    std::cout << "OUTPUT TREE (" << tout->GetEntries() << " ENTRIES)" << std::endl;

    std::cout << "Writing to file" << std::endl;
    dout->WriteTObject(tout, "fitter_tree");
    fout->Close();

    std::cout << "Done " << out << std::endl;
}
