//////////////////////////////////////////////////////////
// This class has been automatically generated on
// Fri Feb 19 14:02:48 2016 by ROOT version 6.02/13
// from TTree t/t
// found on file: evVarFriend_TTJets_SingleLeptonFromT_ext.root
//////////////////////////////////////////////////////////

#ifndef friendTreeOnlyIndexes_h
#define friendTreeOnlyIndexes_h

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>

// Header file for the classes stored in the TTree if any.

class friendTreeOnlyIndexes {
public :
   TTree          *fChain;   //!pointer to the analyzed TTree or TChain
   Int_t           fCurrent; //!current Tree number in a TChain
   TString _fname;

// Fixed size dimensions of array or collections stored in the TTree if any.

   // Declaration of leaf types
   Int_t           iF_Recl[20];

   // List of branches
   TBranch        *b_iF_Recl;   //!

   friendTreeOnlyIndexes(TString fname);
   virtual ~friendTreeOnlyIndexes();
   virtual Int_t    Cut(Long64_t entry);
   virtual Int_t    GetEntry(Long64_t entry);
   virtual Long64_t LoadTree(Long64_t entry);
   virtual void     Init(TTree *tree);
   virtual void     Loop();
   virtual Bool_t   Notify();
   virtual void     Show(Long64_t entry = -1);
};

#endif

#ifdef friendTreeOnlyIndexes_cxx
friendTreeOnlyIndexes::friendTreeOnlyIndexes(TString fname) : fChain(0) 
{
// if parameter tree is not specified (or zero), connect the file
// used to generate this class and read the Tree.
  TFile *f = new TFile(fname.Data(),"read");
  _fname = fname;
  TTree *tree = 0;
  f->GetObject("sf/t",tree);
  Init(tree);
  Loop();
}

friendTreeOnlyIndexes::~friendTreeOnlyIndexes()
{
   if (!fChain) return;
   delete fChain->GetCurrentFile();
}

Int_t friendTreeOnlyIndexes::GetEntry(Long64_t entry)
{
// Read contents of entry.
   if (!fChain) return 0;
   return fChain->GetEntry(entry);
}
Long64_t friendTreeOnlyIndexes::LoadTree(Long64_t entry)
{
// Set the environment to read one entry
   if (!fChain) return -5;
   Long64_t centry = fChain->LoadTree(entry);
   if (centry < 0) return centry;
   if (fChain->GetTreeNumber() != fCurrent) {
      fCurrent = fChain->GetTreeNumber();
      Notify();
   }
   return centry;
}

void friendTreeOnlyIndexes::Init(TTree *tree)
{
   // The Init() function is called when the selector needs to initialize
   // a new tree or chain. Typically here the branch addresses and branch
   // pointers of the tree will be set.
   // It is normally not necessary to make changes to the generated
   // code, but the routine can be extended by the user if needed.
   // Init() will be called many times when running on PROOF
   // (once per file to be processed).

   // Set branch addresses and branch pointers
   if (!tree) return;
   fChain = tree;
   fCurrent = -1;
   fChain->SetMakeClass(1);

   fChain->SetBranchAddress("iF_Recl", iF_Recl, &b_iF_Recl);
   Notify();
}

Bool_t friendTreeOnlyIndexes::Notify()
{
   // The Notify() function is called when a new file is opened. This
   // can be either for a new TTree in a TChain or when when a new TTree
   // is started when using PROOF. It is normally not necessary to make changes
   // to the generated code, but the routine can be extended by the
   // user if needed. The return value is currently not used.

   return kTRUE;
}

void friendTreeOnlyIndexes::Show(Long64_t entry)
{
// Print contents of entry.
// If entry is not specified, print current entry
   if (!fChain) return;
   fChain->Show(entry);
}
Int_t friendTreeOnlyIndexes::Cut(Long64_t entry)
{
// This function may be called from Loop.
// returns  1 if entry is accepted.
// returns -1 otherwise.
   return 1;
}
#endif // #ifdef friendTreeOnlyIndexes_cxx
