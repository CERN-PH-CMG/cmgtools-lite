#include "TCanvas.h"
#include "TROOT.h"
#include "TH1F.h"
#include "TFile.h"
#include "TTree.h"
#include "TImage.h"

void delR_q1_l(){
TCanvas *c = new TCanvas;
TFile *f  = new TFile("/nfs/user/elfaham/104X/v6/2016/2lss_diff_Top-tagged/TTHnobb_fxfx_Friend.root");
//TFile *f  = new TFile("./TTHnobb_fxfx_Friend.root");
TTree *tr = (TTree*)f->Get("Friends");
TH1F *delR_q1_l = new TH1F("delR_q1_l","delR_q1_l", 11, 0, 10);
tr->Draw("Hreco_delR_H_q1l>>delR_q1_l","Hreco_delR_H_q1l>=0");
delR_q1_l->Draw();
TImage *img0 = TImage::Create();
img0->FromPad(c);
img0->WriteImage("./rootplots/delR_q1l.png");
delete delR_q1_l;
delete c;
delete img0;
}

void delR_q2_l(){
TCanvas *c1 = new TCanvas;
TFile *f  = new TFile("/nfs/user/elfaham/104X/v6/2016/2lss_diff_Top-tagged/TTHnobb_fxfx_Friend.root");
//TFile *f  = new TFile("./TTHnobb_fxfx_Friend.root");
TTree *tr = (TTree*)f->Get("Friends");
TH1F *delR_q2_l = new TH1F("delR_q2_l","delR_q2_l", 11, 0, 10);
tr->Draw("Hreco_delR_H_q2l>>delR_q2_l","Hreco_delR_H_q2l>=0");
delR_q2_l->Draw();
TImage *img1 = TImage::Create();
img1->FromPad(c1);
img1->WriteImage("./rootplots/delR_q2l.png");
delete delR_q2_l;
delete c1;
delete img1;
}

void delR_partons(){
TCanvas *c2 = new TCanvas;
TFile *f  = new TFile("/nfs/user/elfaham/104X/v6/2016/2lss_diff_Top-tagged/TTHnobb_fxfx_Friend.root");
//TFile *f  = new TFile("./TTHnobb_fxfx_Friend.root");
TTree *tr = (TTree*)f->Get("Friends");
TH1F *delR_partons = new TH1F("delR_partons","delR_partons", 11, 0, 10);
tr->Draw("Hreco_delR_H_partons>>delR_partons","Hreco_delR_H_partons>=0");
delR_partons->Draw();
TImage *img2 = TImage::Create();
img2->FromPad(c2);
img2->WriteImage("./rootplots/delR_partons.png");
delete delR_partons;
delete c2;
delete img2;
}

void delR_j1j2(){
TCanvas *c3 = new TCanvas;
TFile *f  = new TFile("/nfs/user/elfaham/104X/v6/2016/2lss_diff_Top-tagged/TTHnobb_fxfx_Friend.root");
//TFile *f  = new TFile("./TTHnobb_fxfx_Friend.root");
TTree *tr = (TTree*)f->Get("Friends");
TH1F *delR_j1j2 = new TH1F("delR_j1j2","delR_j1j2", 11, 0, 10);
tr->Draw("Hreco_delR_H_j1j2>>delR_j1j2","Hreco_delR_H_j1j2>=0 && Hreco_matchedpartons ==1");
TH1F *delR_j1j2_2 = new TH1F("delR_j1j2_2","delR_j1j2_2", 11, 0, 10);
tr->Draw("Hreco_delR_H_j1j2>>delR_j1j2_2","Hreco_delR_H_j1j2>=0 && Hreco_matchedpartons ==2");
delR_j1j2->Scale(1/delR_j1j2->Integral());
delR_j1j2_2->Scale(1/delR_j1j2_2->Integral());
delR_j1j2->SetLineColor(kRed);
delR_j1j2->Draw("Hist");
delR_j1j2_2->Draw("Hist SAME");
TImage *img3 = TImage::Create();
img3->FromPad(c3);
img3->WriteImage("./rootplots/delR_j1j2.png");
delete delR_j1j2;
delete c3;
delete img3;
}

void delR_j1l(){
TCanvas *c4 = new TCanvas;
TFile *f  = new TFile("/nfs/user/elfaham/104X/v6/2016/2lss_diff_Top-tagged/TTHnobb_fxfx_Friend.root");
//TFile *f  = new TFile("./TTHnobb_fxfx_Friend.root");
TTree *tr = (TTree*)f->Get("Friends");
TH1F *delR_j1l = new TH1F("delR_j1l","delR_j1l", 11, 0, 10);
tr->Draw("Hreco_delR_H_j1l>>delR_j1l","Hreco_delR_H_j1l>=0");
delR_j1l->Draw();
TImage *img4 = TImage::Create();
img4->FromPad(c4);
img4->WriteImage("./rootplots/delR_j1l.png");
delete delR_j1l;
delete c4;
delete img4;
}

void delR_j2l(){
TCanvas *c5 = new TCanvas;
TFile *f  = new TFile("/nfs/user/elfaham/104X/v6/2016/2lss_diff_Top-tagged/TTHnobb_fxfx_Friend.root");
//TFile *f  = new TFile("./TTHnobb_fxfx_Friend.root");
TTree *tr = (TTree*)f->Get("Friends");
TH1F *delR_j2l = new TH1F("delR_j2l","delR_j2l", 11, 0, 10);
tr->Draw("Hreco_delR_H_j2l>>delR_j2l","Hreco_delR_H_j2l>=0");
delR_j2l->Draw();
TImage *img5 = TImage::Create();
img5->FromPad(c5);
img5->WriteImage("./rootplots/delR_j2l.png");
delete delR_j2l;
delete c5;
delete img5;
}

void drawscore(){
TCanvas *c6 = new TCanvas;
TFile *f  = new TFile("/nfs/user/elfaham/104X/v6/2016/2lss_diff_Top-tagged/TTHnobb_fxfx_Friend.root");
//TFile *f  = new TFile("./TTHnobb_fxfx_Friend.root");
TTree *tr = (TTree*)f->Get("Friends");
TH1F *score = new TH1F("score","score", 11, 0, 1);
tr->Draw("Hreco_BDThttTT_eventReco_mvaValue>>score","Hreco_BDThttTT_eventReco_mvaValue>=0");
score->Draw();
TImage *img5 = TImage::Create();
img5->FromPad(c6);
img5->WriteImage("./rootplots/all_score_test.png");
delete score;
delete c6;
delete img5;
}

void drawnum_1(){
TCanvas *c7 = new TCanvas;
TFile *f  = new TFile("/nfs/user/elfaham/104X/v6/2016/2lss_diff_Top-tagged/TTHnobb_fxfx_Friend.root");
//TFile *f  = new TFile("./TTHnobb_fxfx_Friend.root");
TTree *tr = (TTree*)f->Get("Friends");
TH1F *hnum = new TH1F("hnum","hnum", 21, 0, 20);
tr->Draw("Hreco_matchedpartons>>hnum","Hreco_matchedpartons==1");
hnum->Draw();
TImage *img6 = TImage::Create();
img6->FromPad(c7);
img6->WriteImage("./rootplots/hnum_top_1.png");
delete hnum;
delete c7;
delete img6;
}

void drawnum_2(){
TCanvas *c8 = new TCanvas;
TFile *f  = new TFile("/nfs/user/elfaham/104X/v6/2016/2lss_diff_Top-tagged/TTHnobb_fxfx_Friend.root");
//TFile *f  = new TFile("./TTHnobb_fxfx_Friend.root");
TTree *tr = (TTree*)f->Get("Friends");
TH1F *hnum = new TH1F("hnum","hnum", 21, 0, 20);
tr->Draw("Hreco_matchedpartons>>hnum","Hreco_matchedpartons==2");
hnum->Draw();
TImage *img7 = TImage::Create();
img7->FromPad(c8);
img7->WriteImage("./rootplots/hnum_top_2.png");
delete hnum;
delete c8;
delete img7;
}

void drawden(){
TCanvas *c9 = new TCanvas;
TFile *f  = new TFile("/nfs/user/elfaham/104X/v6/2016/2lss_diff_Top-tagged/TTHnobb_fxfx_Friend.root");
//TFile *f  = new TFile("./TTHnobb_fxfx_Friend.root");
TTree *tr = (TTree*)f->Get("Friends");
TH1F *hden = new TH1F("hden","hden", 21, 0, 20);
tr->Draw("Hreco_matchedpartons>>hden","Hreco_matchedpartons>=0");
hden->Draw();
TImage *img8 = TImage::Create();
img8->FromPad(c9);
img8->WriteImage("./rootplots/hden_no_top.png");
delete hden;
delete c9;
delete img8;
}

void draw(){
drawnum_1();
drawnum_2();
drawnum();
drawden();
drawscore();
delR_q1_l();
delR_q2_l();
delR_partons();
delR_j1l();
delR_j2l();
delR_j1j2();
}
