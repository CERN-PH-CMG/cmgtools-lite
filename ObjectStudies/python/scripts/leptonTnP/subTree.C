void subTree(TString newFile="subTree.root", TString dir="tpTree", TString cut="tag_IsoMu22 && tag_chargedHadIso04/tag_pt < 0.2 && tag_SIP < 2.5 && (pt > 20 || TM || Glb) && (65 <= mass && mass <= 125)") {
    TTree *in  = (TTree *)gFile->Get(dir+"/fitter_tree");
    TFile *fout = new TFile(newFile, "RECREATE");
    TDirectory *dout = fout->mkdir(dir); dout->cd();

    TTree *out = in->CopyTree(cut);
    std::cout << "INPUT TREE (" << in->GetEntries() << " ENTRIES)" << std::endl;
    //in->Print();
    std::cout << "OUTPUT TREE (" << out->GetEntries() << " ENTRIES)" << std::endl;
    //out->Print();
    dout->WriteTObject(out, "fitter_tree");
    fout->Close();
}
