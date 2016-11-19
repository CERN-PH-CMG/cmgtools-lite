#include <assert.h>
#include <iostream>
#include "TH2F.h"
#include "TH1F.h"
#include "TFile.h"
#include "TSystem.h"

TString CMSSW_BASE = gSystem->ExpandPathName("${CMSSW_BASE}");

TFile* f_puw2016_ICHEP = NULL;
TFile* f_puw2016_ICHEP_Up = NULL;
TFile* f_puw2016_ICHEP_Dn = NULL;
TH1F* h_puw2016_nInt_ICHEP = NULL;
TH1F* h_puw2016_nInt_ICHEP_Up = NULL;
TH1F* h_puw2016_nInt_ICHEP_Dn = NULL;
float puw2016_nInt_ICHEP(float nInt, int var=0) { 
  
  if (var==0) { 
    if (!h_puw2016_nInt_ICHEP){ 
      f_puw2016_ICHEP = new TFile(CMSSW_BASE+"/src/CMGTools/TTHAnalysis/data/pileup/puWeights_12fb_63mb.root", "read");
      h_puw2016_nInt_ICHEP = (TH1F*) (f_puw2016_ICHEP->Get("puw"));
    }
    return h_puw2016_nInt_ICHEP->GetBinContent(h_puw2016_nInt_ICHEP->FindBin(nInt));
  }
  else if (var==1) { 
    if (!h_puw2016_nInt_ICHEP_Up) {
      f_puw2016_ICHEP_Up = new TFile(CMSSW_BASE+"/src/CMGTools/TTHAnalysis/data/pileup/puWeights_12fb_63mb_Up.root", "read");
      h_puw2016_nInt_ICHEP_Up = (TH1F*) (f_puw2016_ICHEP_Up->Get("puw"));
    }
    return h_puw2016_nInt_ICHEP_Up->GetBinContent(h_puw2016_nInt_ICHEP_Up->FindBin(nInt));
  }
  else if (var==-1) {
    if (!h_puw2016_nInt_ICHEP_Dn) {
      f_puw2016_ICHEP_Dn = new TFile(CMSSW_BASE+"/src/CMGTools/TTHAnalysis/data/pileup/puWeights_12fb_63mb_Down.root", "read");
      h_puw2016_nInt_ICHEP_Dn = (TH1F*) (f_puw2016_ICHEP_Dn->Get("puw"));
    }
    return h_puw2016_nInt_ICHEP_Dn->GetBinContent(h_puw2016_nInt_ICHEP_Dn->FindBin(nInt));
  }
  cout <<"[WARNING!!!]  don't know what to do with PUweight, please check!! ";
  return -9999.;
}
