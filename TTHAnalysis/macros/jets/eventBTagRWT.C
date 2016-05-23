#include "TTree.h"
#include "TFile.h"
#include <iostream>
#include <assert.h>

TFile *newfile = 0;
TTree *newtree = 0;

Float_t eventBTagSF;
Float_t eventBTagSF_LFUp;
Float_t eventBTagSF_LFDown;
Float_t eventBTagSF_HFUp;
Float_t eventBTagSF_HFDown;
Float_t eventBTagSF_HFStats1Up;
Float_t eventBTagSF_HFStats1Down;
Float_t eventBTagSF_HFStats2Up;
Float_t eventBTagSF_HFStats2Down;
Float_t eventBTagSF_LFStats1Up;
Float_t eventBTagSF_LFStats1Down;
Float_t eventBTagSF_LFStats2Up;
Float_t eventBTagSF_LFStats2Down;
Float_t eventBTagSF_cErr1Up;
Float_t eventBTagSF_cErr1Down;
Float_t eventBTagSF_cErr2Up;
Float_t eventBTagSF_cErr2Down;
Float_t eventBTagSF_jecUp;
Float_t eventBTagSF_jecDown;

void eventBTagRWT_Begin(TTree *tree){

  TString fname = GetOption();
  if (fname==TString("")) assert(0);

  newfile = new TFile(fname.Data(),"recreate");
  newfile->cd();
  newfile->mkdir("sf");
  newfile->cd("sf");

  newtree = new TTree("t","t");

  newtree->Branch("eventBTagSF", &eventBTagSF, "eventBTagSF/F");
  newtree->Branch("eventBTagSF_LFUp", &eventBTagSF_LFUp, "eventBTagSF_LFUp/F");
  newtree->Branch("eventBTagSF_LFDown", &eventBTagSF_LFDown, "eventBTagSF_LFDown/F");
  newtree->Branch("eventBTagSF_HFUp", &eventBTagSF_HFUp, "eventBTagSF_HFUp/F");
  newtree->Branch("eventBTagSF_HFDown", &eventBTagSF_HFDown, "eventBTagSF_HFDown/F");
  newtree->Branch("eventBTagSF_HFStats1Up", &eventBTagSF_HFStats1Up, "eventBTagSF_HFStats1Up/F");
  newtree->Branch("eventBTagSF_HFStats1Down", &eventBTagSF_HFStats1Down, "eventBTagSF_HFStats1Down/F");
  newtree->Branch("eventBTagSF_HFStats2Up", &eventBTagSF_HFStats2Up, "eventBTagSF_HFStats2Up/F");
  newtree->Branch("eventBTagSF_HFStats2Down", &eventBTagSF_HFStats2Down, "eventBTagSF_HFStats2Down/F");
  newtree->Branch("eventBTagSF_LFStats1Up", &eventBTagSF_LFStats1Up, "eventBTagSF_LFStats1Up/F");
  newtree->Branch("eventBTagSF_LFStats1Down", &eventBTagSF_LFStats1Down, "eventBTagSF_LFStats1Down/F");
  newtree->Branch("eventBTagSF_LFStats2Up", &eventBTagSF_LFStats2Up, "eventBTagSF_LFStats2Up/F");
  newtree->Branch("eventBTagSF_LFStats2Down", &eventBTagSF_LFStats2Down, "eventBTagSF_LFStats2Down/F");
  newtree->Branch("eventBTagSF_cErr1Up", &eventBTagSF_cErr1Up, "eventBTagSF_cErr1Up/F");
  newtree->Branch("eventBTagSF_cErr1Down", &eventBTagSF_cErr1Down, "eventBTagSF_cErr1Down/F");
  newtree->Branch("eventBTagSF_cErr2Up", &eventBTagSF_cErr2Up, "eventBTagSF_cErr2Up/F");
  newtree->Branch("eventBTagSF_cErr2Down", &eventBTagSF_cErr2Down, "eventBTagSF_cErr2Down/F");
  newtree->Branch("eventBTagSF_jecUp", &eventBTagSF_jecUp, "eventBTagSF_jecUp/F");
  newtree->Branch("eventBTagSF_jecDown", &eventBTagSF_jecDown, "eventBTagSF_jecDown/F");

};

Double_t makeRWT(TIntProxy* nj, TArrayIntProxy *ijl, TArrayFloatProxy *jcw, TArrayFloatProxy *jdw){
  Float_t res = 1;
  for (int i=0; i<(*nj); i++) {
    int ij = (*ijl)[i];
    if (ij>=0) res *= (*jcw)[ij];
    else res *= (*jdw)[-ij-1];
  }
  return res;
}

Bool_t eventBTagRWT_Process(Long64_t entry){

  fChain->GetTree()->GetEntry(entry);

  eventBTagSF = 1;
  eventBTagSF_LFUp = 1;
  eventBTagSF_LFDown = 1;
  eventBTagSF_HFUp = 1;
  eventBTagSF_HFDown = 1;
  eventBTagSF_HFStats1Up = 1;
  eventBTagSF_HFStats1Down = 1;
  eventBTagSF_HFStats2Up = 1;
  eventBTagSF_HFStats2Down = 1;
  eventBTagSF_LFStats1Up = 1;
  eventBTagSF_LFStats1Down = 1;
  eventBTagSF_LFStats2Up = 1;
  eventBTagSF_LFStats2Down = 1;
  eventBTagSF_cErr1Up = 1;
  eventBTagSF_cErr1Down = 1;
  eventBTagSF_cErr2Up = 1;
  eventBTagSF_cErr2Down = 1;
  eventBTagSF_jecUp = 1;
  eventBTagSF_jecDown = 1;

  eventBTagSF = makeRWT(&nJetSel_Recl,&iJ_Recl,&Jet_btagCSVWeight,&DiscJet_btagCSVWeight);
  eventBTagSF_LFUp = makeRWT(&nJetSel_Recl,&iJ_Recl,&Jet_btagCSVWeight_LFUp,&DiscJet_btagCSVWeight_LFUp);
  eventBTagSF_LFDown = makeRWT(&nJetSel_Recl,&iJ_Recl,&Jet_btagCSVWeight_LFDown,&DiscJet_btagCSVWeight_LFDown);
  eventBTagSF_HFUp = makeRWT(&nJetSel_Recl,&iJ_Recl,&Jet_btagCSVWeight_HFUp,&DiscJet_btagCSVWeight_HFUp);
  eventBTagSF_HFDown = makeRWT(&nJetSel_Recl,&iJ_Recl,&Jet_btagCSVWeight_HFDown,&DiscJet_btagCSVWeight_HFDown);
  eventBTagSF_HFStats1Up = makeRWT(&nJetSel_Recl,&iJ_Recl,&Jet_btagCSVWeight_HFStats1Up,&DiscJet_btagCSVWeight_HFStats1Up);
  eventBTagSF_HFStats1Down = makeRWT(&nJetSel_Recl,&iJ_Recl,&Jet_btagCSVWeight_HFStats1Down,&DiscJet_btagCSVWeight_HFStats1Down);
  eventBTagSF_HFStats2Up = makeRWT(&nJetSel_Recl,&iJ_Recl,&Jet_btagCSVWeight_HFStats2Up,&DiscJet_btagCSVWeight_HFStats2Up);
  eventBTagSF_HFStats2Down = makeRWT(&nJetSel_Recl,&iJ_Recl,&Jet_btagCSVWeight_HFStats2Down,&DiscJet_btagCSVWeight_HFStats2Down);
  eventBTagSF_LFStats1Up = makeRWT(&nJetSel_Recl,&iJ_Recl,&Jet_btagCSVWeight_LFStats1Up,&DiscJet_btagCSVWeight_LFStats1Up);
  eventBTagSF_LFStats1Down = makeRWT(&nJetSel_Recl,&iJ_Recl,&Jet_btagCSVWeight_LFStats1Down,&DiscJet_btagCSVWeight_LFStats1Down);
  eventBTagSF_LFStats2Up = makeRWT(&nJetSel_Recl,&iJ_Recl,&Jet_btagCSVWeight_LFStats2Up,&DiscJet_btagCSVWeight_LFStats2Up);
  eventBTagSF_LFStats2Down = makeRWT(&nJetSel_Recl,&iJ_Recl,&Jet_btagCSVWeight_LFStats2Down,&DiscJet_btagCSVWeight_LFStats2Down);
  eventBTagSF_cErr1Up = makeRWT(&nJetSel_Recl,&iJ_Recl,&Jet_btagCSVWeight_cErr1Up,&DiscJet_btagCSVWeight_cErr1Up);
  eventBTagSF_cErr1Down = makeRWT(&nJetSel_Recl,&iJ_Recl,&Jet_btagCSVWeight_cErr1Down,&DiscJet_btagCSVWeight_cErr1Down);
  eventBTagSF_cErr2Up = makeRWT(&nJetSel_Recl,&iJ_Recl,&Jet_btagCSVWeight_cErr2Up,&DiscJet_btagCSVWeight_cErr2Up);
  eventBTagSF_cErr2Down = makeRWT(&nJetSel_Recl,&iJ_Recl,&Jet_btagCSVWeight_cErr2Down,&DiscJet_btagCSVWeight_cErr2Down);
  eventBTagSF_jecUp = makeRWT(&nJetSel_Recl_jecUp,&iJ_Recl_jecUp,&Jet_btagCSVWeight_JESUp,&DiscJet_btagCSVWeight_JESUp);
  eventBTagSF_jecDown = makeRWT(&nJetSel_Recl_jecDown,&iJ_Recl_jecDown,&Jet_btagCSVWeight_JESDown,&DiscJet_btagCSVWeight_JESDown);

  newtree->Fill();

  if (entry%10000==0) std::cout << entry << " " << eventBTagSF << " " << eventBTagSF_jecUp << " " << eventBTagSF_jecDown << " " << eventBTagSF_HFUp << " " << eventBTagSF_LFUp << std::endl;

  return kTRUE;

};

Bool_t eventBTagRWT_Notify(){return kTRUE;};

Double_t eventBTagRWT(){return 0;};

void eventBTagRWT_SlaveTerminate(){};

void eventBTagRWT_Terminate(){

  newtree->Write();
  newfile->Close();

};

