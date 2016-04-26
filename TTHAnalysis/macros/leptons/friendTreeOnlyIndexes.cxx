#define friendTreeOnlyIndexes_cxx
#include "friendTreeOnlyIndexes.h"
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <assert.h>
#include <iostream>

void friendTreeOnlyIndexes::Loop()
{
//   In a ROOT session, you can do:
//      root> .L friendTreeOnlyIndexes.C
//      root> friendTreeOnlyIndexes t
//      root> t.GetEntry(12); // Fill t data members with entry number 12
//      root> t.Show();       // Show values of entry 12
//      root> t.Show(16);     // Read and show values of entry 16
//      root> t.Loop();       // Loop on all entries
//

//     This is the loop skeleton where:
//    jentry is the global entry number in the chain
//    ientry is the entry number in the current Tree
//  Note that the argument to GetEntry must be:
//    jentry for TChain::GetEntry
//    ientry for TTree::GetEntry and TBranch::GetEntry
//
//       To read only selected branches, Insert statements like:
// METHOD1:
//    fChain->SetBranchStatus("*",0);  // disable all branches
//    fChain->SetBranchStatus("branchname",1);  // activate branchname
// METHOD2: replace line
//    fChain->GetEntry(jentry);       //read all branches
//by  b_branchname->GetEntry(ientry); //read only this branch
   if (fChain == 0) return;

   Long64_t nentries = fChain->GetEntriesFast();

   TFile *newfile = new TFile(_fname.Prepend("../friendTreeOnlyIndexes/").Data(),"recreate");
   std::cout << newfile->GetName() << std::endl;
   assert(newfile && !(newfile->IsZombie()));
   newfile->cd();
   newfile->mkdir("sf");
   newfile->cd("sf");
   TTree *t = new TTree("t","t");
   int i0;
   int i1;
   int i2;
   TBranch *br0 = t->Branch("iF_Recl_0",&i0,"iF_Recl_0/I");
   TBranch *br1 = t->Branch("iF_Recl_1",&i1,"iF_Recl_1/I");
   TBranch *br2 = t->Branch("iF_Recl_2",&i2,"iF_Recl_2/I");

   Long64_t nbytes = 0, nb = 0;
   for (Long64_t jentry=0; jentry<nentries;jentry++) {
      Long64_t ientry = LoadTree(jentry);
      if (ientry < 0) break;
      nb = fChain->GetEntry(jentry);   nbytes += nb;
      // if (Cut(ientry) < 0) continue;

      i0 = iF_Recl[0];
      i1 = iF_Recl[1];
      i2 = iF_Recl[2];
      t->Fill();

   }

   t->Write();
   newfile->Close();

}
