#include <TROOT.h>
#include <TFile.h>
#include <TTree.h>
#include <TH2D.h>

TH2D* getHist() {
    TH2D* h_zptmass;
    TFile* f_in = gROOT->GetFile("/afs/cern.ch/user/r/rlane/public/HIG16006/Zweights/zpt_weights.root");
    if (!f_in) {
        f_in = new TFile("/afs/cern.ch/user/r/rlane/public/HIG16006/Zweights/zpt_weights.root");
        h_zptmass = dynamic_cast<TH2D*>(f_in->Get("zptmass_histo"));
    }
    h_zptmass = dynamic_cast<TH2D*>(f_in->Get("zptmass_histo"));
    return h_zptmass;
  }


double getDYWeight(double genMass, double genpT) {
    TH2D* h_zptmass = getHist();
    return h_zptmass->GetBinContent(h_zptmass->GetXaxis()->FindBin(genMass), h_zptmass->GetYaxis()->FindBin(genpT));
}
