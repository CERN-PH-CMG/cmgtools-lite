#include "TFile.h"
#include "Math/Boost.h"
#include "TLorentzVector.h"
#include "TVector3.h"
#include "TH2D.h"
//typedef ROOT::Math::LorentzVector<ROOT::Math::PxPyPzE4D<float> > LorentzVector;
float ttbarPolarizationAngle(TLorentzVector p4top, TLorentzVector p4lepton){
  
  TVector3 boost_t = p4top.BoostVector();;
  p4lepton.Boost(-boost_t);
  float lepton_cos_theta =  cos(p4lepton.Vect().Angle(p4top.Vect()));
 
  return lepton_cos_theta;

}

float ttbarPolarizationreturnWeight(float t, float at){

  TFile* theFile = new TFile("../python/tools/TopSpinCorWeights.root");
  TH2D* hist = (TH2D*) theFile->Get("cos2D");
  int binX = hist->GetXaxis()->FindBin(t);
  int binY = hist->GetYaxis()->FindBin(at);
  float weight = hist->GetBinContent(binX,binY);
  delete theFile;
  return weight; 
}


float ResolutionWeight(float met_Pt, float met_Phi, TLorentzVector Z ){

  TFile* theFile = new TFile("../python/tools/ResolutionWeights.root");
  // TLorentzVector Z;
  //  Z.SetPtEtaPhiM(Z_Pt, Z_Phi,0,0);
  TLorentzVector MET;
  MET.SetPtEtaPhiM(met_Pt, met_Phi,0,0);
  float UT = sin(MET.DeltaPhi(Z))*MET.Pt();
  float UP = cos(MET.DeltaPhi(Z))*MET.Pt()-Z.Pt();
  float weight = 1 ;
  
  if( Z.Pt() >75 && Z.Pt()<150 )
    { 
      TH2D* hist = (TH2D*) theFile->Get("Resolution_Pt76");
      int binX = hist->GetXaxis()->FindBin(UT);
      int binY = hist->GetYaxis()->FindBin(UP);
      weight = hist->GetBinContent(binX,binY);
    }
  if( Z.Pt()>150 )
    { 
      TH2D* hist = (TH2D*) theFile->Get("Resolution_Pt150");
      int binX = hist->GetXaxis()->FindBin(UT);
      int binY = hist->GetYaxis()->FindBin(UP);
      weight = hist->GetBinContent(binX,binY);
    }
 
  /*
  if(Z_Pt>250 )
    { 
      TH2D* hist = (TH2D*) theFile->Get("blablaX250");
      int binX = hist->GetXaxis()->FindBin(UT);
      int binY = hist->GetYaxis()->FindBin(UP);
      weight = hist->GetBinContent(binX,binY);
    }
  */
  if (weight>2) weight=2;
  if (weight<0.5) weight=0.5;
  delete theFile;
  return weight; 

}
