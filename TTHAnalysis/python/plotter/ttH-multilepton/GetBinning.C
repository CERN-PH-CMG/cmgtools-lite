#include <iostream>
#include "TH2.h"
#include "TROOT.h"
#include "TFile.h"

using namespace std;

class GetBinning
{
public:
  GetBinning();
  Int_t GetCluster2l(Double_t, Double_t);
  Int_t GetCluster3l(Double_t, Double_t);
  Int_t GetCluster3lMEM(Double_t, Double_t);
protected:
  TFile* file2l;
  TFile* file3l;
  TFile* file3lMEM;
  TH2F* hBinning2l;
  TH2F* hBinning3l;
  TH2F* hBinning3lMEM;
};


GetBinning::GetBinning()
{
  TString fileName2l = "ttH-multilepton/binning_2l.root";
  TString fileName3l = "ttH-multilepton/binning_3l.root";
  TString fileName3lMEM = "ttH-multilepton/binning_3l_MEM.root";
  file2l = (TFile*) gROOT->GetListOfFiles()->FindObject(fileName2l);
  file3l = (TFile*) gROOT->GetListOfFiles()->FindObject(fileName3l);
  file3lMEM = (TFile*) gROOT->GetListOfFiles()->FindObject(fileName3lMEM);
  if (!file2l || !file2l->IsOpen()) file2l = TFile::Open(fileName2l);
  if (!file3l || !file3l->IsOpen()) file3l = TFile::Open(fileName3l);
  if (!file3lMEM || !file3lMEM->IsOpen()) file3lMEM = TFile::Open(fileName3lMEM);
  hBinning2l = (TH2F*) file2l->Get("hTargetBinning");
  hBinning3l = (TH2F*) file3l->Get("hTargetBinning");
  hBinning3lMEM = (TH2F*) file3lMEM->Get("hTargetBinning");
}


Int_t GetBinning::GetCluster2l( Double_t x, Double_t y)
{
  return hBinning2l->GetBinContent( hBinning2l->FindBin(x,y) );
}
Int_t GetBinning::GetCluster3l( Double_t x, Double_t y)
{
  return hBinning3l->GetBinContent( hBinning3l->FindBin(x,y) );
}
Int_t GetBinning::GetCluster3lMEM( Double_t x, Double_t y)
{
  return hBinning3lMEM->GetBinContent( hBinning3lMEM->FindBin(x,y) );
}

GetBinning ClusteringSuite;

Int_t OurBin2l(Double_t x, Double_t y)
{
  return ClusteringSuite.GetCluster2l(x,y)+1;

}
Int_t OurBin3l(Double_t x, Double_t y)
{
  return ClusteringSuite.GetCluster3l(x,y)+1;

}
Int_t OurBin3lMEM(Double_t x, Double_t y)
{
  return ClusteringSuite.GetCluster3lMEM(x,y)+1;

}


