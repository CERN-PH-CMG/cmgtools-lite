#include "TCanvas.h"
#include "TROOT.h"
#include "TH1F.h"
#include "TFile.h"
#include "TTree.h"
#include "TImage.h"


//TFile *f  = new TFile("TTHnobb_pow_Friend.root");
//TTree *tr = (TTree*)f->Get("Friends");
//hden->Draw();
//hnum->Draw();
//Float_t eff = hnum->Integral()/hden->Integral();
//cout << eff;


void drawnum(){

TCanvas *c = new TCanvas;
TFile *f  = new TFile("/nfs/user/elfaham/104X/2016/2lss_NoTop-tagged/TTHnobb_pow_Friend.root");
TTree *tr = (TTree*)f->Get("Friends");
TH1F *hnum = new TH1F("hnum","hnum", 21, 0, 20);
tr->Draw("Hreco_matchedpartons>>hnum","Hreco_matchedpartons>=1");
hnum->Draw();
TImage *img1 = TImage::Create();
//img1->FromPad(c,10,10,300,200);
img1->FromPad(c);
img1->WriteImage("hnum_no_top.png");
delete hnum;
delete c;
delete img1;
}


void drawden(){

TCanvas *c1 = new TCanvas;
TFile *f  = new TFile("/nfs/user/elfaham/104X/2016/2lss_NoTop-tagged/TTHnobb_pow_Friend.root");
TTree *tr = (TTree*)f->Get("Friends");
TH1F *hden = new TH1F("hden","hden", 21, 0, 20);
tr->Draw("Hreco_matchedpartons>>hden","Hreco_matchedpartons>=0");
hden->Draw();
TImage *img2 = TImage::Create();
//img1->FromPad(c,10,10,300,200);
img2->FromPad(c1);
img2->WriteImage("hden_no_top.png");
delete hden;
delete c1;
delete img2;
}

void draw(){
drawnum();
drawden();
}
