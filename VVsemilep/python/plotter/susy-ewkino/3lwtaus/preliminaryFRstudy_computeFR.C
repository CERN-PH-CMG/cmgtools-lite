


void doRatioInt(TH1* h1, TH1* h2, TString sample)
{
  TH1* h = (TH1*) h1->Clone("ratioplot");
  
  h->Divide(h2);



  TCanvas* c = new TCanvas("c", "c", 800, 800);
  c->cd();
  h1->SetLineColor(kRed);
  h2->SetLineColor(kBlue);
  h1->SetMarkerColor(kRed);
  h2->SetMarkerColor(kBlue);
  h1->SetMarkerStyle(21);
  h2->SetMarkerStyle(21);

  h1->Draw();
  h2->Draw("same");
  c->Print(TString("~/www/susyRA7/met_")+sample+TString(".png"));
  c->Print(TString("~/www/susyRA7/met_")+sample+TString(".pdf"));
  c->Clear(); 

  h->Draw();

  h->Fit("pol2");

  c->Print(TString("~/www/susyRA7/ratio_")+sample+TString(".png"));
  c->Print(TString("~/www/susyRA7/ratio_")+sample+TString(".pdf"));

  
}


void preliminaryFRstudy_computeFR()
{

  TString num("met_");
  TString den("cut_00_1_tau_noid/met_");

  TFile* fTT   = TFile::Open("~/www/susyRA7/TT/preliminaryFRstudy_plots.root"  , "READ");
  TFile* fDY   = TFile::Open("~/www/susyRA7/DY/preliminaryFRstudy_plots.root"  , "READ");
  TFile* fData = TFile::Open("~/www/susyRA7/data/preliminaryFRstudy_plots.root", "READ");

  TH1* h1 = NULL;
  TH1* h2 = NULL;

  h1 = (TH1*) fTT->Get(num+TString("TT"));
  h2 = (TH1*) fTT->Get(den+TString("TT"));
  doRatioInt(h1, h2, "TT");

  h1 = (TH1*) fDY->Get(num+TString("DY"));
  h2 = (TH1*) fDY->Get(den+TString("DY"));
  doRatioInt(h1, h2, "DY");
  return;
  h1 = (TH1*) fData->Get(num+TString("data"));
  h2 = (TH1*) fData->Get(den+TString("data"));
  doRatioInt(h1, h2, "Data");

}
