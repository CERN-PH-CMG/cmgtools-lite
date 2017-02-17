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
protected:
  TFile* file2l;
  TFile* file3l;
  TH2F* hBinning2l;
  TH2F* hBinning3l;
};


GetBinning::GetBinning()
{
  //TString fileName2l = "/nfs/fanae/user/sscruz/TTH/CMSSW_8_0_19/src/CMGTools/TTHAnalysis/python/plotter/ttH-multilepton/binning2l.root";
  //TString fileName3l = "/nfs/fanae/user/vischia/workarea/cmssw/tthMultilepton/Clusterization/binning539.root";
  TString fileName2l = "ttH-multilepton/binning_2l.root";
  TString fileName3l = "ttH-multilepton/binning_3l.root";
  file2l = (TFile*) gROOT->GetListOfFiles()->FindObject(fileName2l);
  file3l = (TFile*) gROOT->GetListOfFiles()->FindObject(fileName3l);
  if (!file2l || !file2l->IsOpen()) file2l = TFile::Open(fileName2l);
  if (!file3l || !file3l->IsOpen()) file3l = TFile::Open(fileName3l);
  hBinning2l = (TH2F*) file2l->Get("hBinning");
  hBinning3l = (TH2F*) file3l->Get("hBinning");
}


Int_t GetBinning::GetCluster2l( Double_t x, Double_t y)
{
  return hBinning2l->GetBinContent( hBinning2l->FindBin(x,y) );
}
Int_t GetBinning::GetCluster3l( Double_t x, Double_t y)
{
  return hBinning3l->GetBinContent( hBinning3l->FindBin(x,y) );
}

GetBinning ClusteringSuite;

Int_t OurBin2l(Double_t x, Double_t y)
{
  return ClusteringSuite.GetCluster2l(y,x)+1;

}
Int_t OurBin3l(Double_t x, Double_t y)
{
  return ClusteringSuite.GetCluster3l(y,x)+1;

}


Int_t classicalBinning2l(Double_t y, Double_t x){
  if      ((-1. < y ) && ( y <= 1)   && (-1.0 < y) && (y <= -0.2))  return 0+1;
  else if ((-1. < x ) && ( x <= 1)   && (-0.2 < y) && ( y  <=  0.1))  return 1+1;
  else if ((-1. < x ) && ( x <= 0.3) && (0.1  < y) && ( y  <=  0.4))  return 2+1;
  else if ((0.3 < x ) && ( x <= 1.)  && (0.1  < y) && ( y  <=  0.4))  return 3+1;
  else if ((-1. < x ) && ( x <= 0.1) && (0.4  < y) && ( y  <=  1.0))  return 4+1;
  else if ((0.1 < x ) && ( x <= 0.4) && (0.4  < y) && ( y  <=  1.0))  return 5+1;
  else if ((0.4 < x ) && ( x <= 1.)  && (0.4  < y) && ( y  <=  1.0))  return 6+1;
  else {
    cout <<  "one bin is missing " << x << " " << y << endl;
    return -1;
  }
}


Int_t classicalBinning3l(Double_t y, Double_t x){
  if      ((-1. < x)  && ( x <= 1   ) && (-1.0 < y)  && (y <= -0.3))    return 0+1;
  else if ((-1. < x ) && ( x <= 0.25) && (-0.3 < y)  && ( y  <=  0.3))  return 1+1;
  else if ((0.25 < x )&& ( x <= 1.  ) && (-0.3  < y) && ( y  <=  0.3))  return 2+1;
  else if ((-1. < x ) && ( x <= 0.25) && (0.3  < y)  && ( y  <=  1.0))  return 3+1;
  else if ((0.25 < x )&& ( x <= 1.  ) && (0.3  < y)  && ( y  <=  1.0))  return 4+1;
  else {
    cout <<  "one bin is missing " << x << " " << y << endl;
    return -1;
  }
}
