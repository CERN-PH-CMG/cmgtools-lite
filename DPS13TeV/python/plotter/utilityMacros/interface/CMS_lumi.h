#ifndef CMS_lumi_h
#define CMS_lumi_h

#include "./centerOfMassEnergy.h"

#include "TPad.h"
#include "TLatex.h"
#include "TLine.h"
#include "TBox.h"
#include "TASImage.h"
#include "TStyle.h"
#include <iostream>
#include <sstream>

void setTDRStyle (){

  gStyle->SetCanvasBorderMode(0);
  gStyle->SetCanvasColor(0);
  gStyle->SetCanvasDefH(600);
  gStyle->SetCanvasDefW(600);
  gStyle->SetCanvasDefX(0);
  gStyle->SetCanvasDefY(0);

  gStyle->SetPadBorderMode(0);
  gStyle->SetPadColor(0); 
  gStyle->SetPadGridX(0);
  gStyle->SetPadGridY(0);
  gStyle->SetGridColor(0);
  gStyle->SetGridStyle(3);
  gStyle->SetGridWidth(1);

  gStyle->SetFrameBorderMode(0);
  gStyle->SetFrameBorderSize(1);
  gStyle->SetFrameFillColor(0);
  gStyle->SetFrameFillStyle(0);
  gStyle->SetFrameLineColor(1);
  gStyle->SetFrameLineStyle(1);
  gStyle->SetFrameLineWidth(1);
  gStyle->SetHistLineColor(1);
  gStyle->SetHistLineStyle(0);
  gStyle->SetHistLineWidth(1);

  gStyle->SetEndErrorSize(2);
  gStyle->SetFuncColor(2);
  gStyle->SetFuncStyle(1);
  gStyle->SetFuncWidth(1);
  gStyle->SetOptDate(0);
  
  gStyle->SetOptFile(0);
  gStyle->SetOptStat(0);
  gStyle->SetStatColor(0);
  gStyle->SetStatFont(42);
  gStyle->SetStatFontSize(0.04);
  gStyle->SetStatTextColor(1);
  gStyle->SetStatFormat("6.4g");
  gStyle->SetStatBorderSize(0);
  gStyle->SetStatH(0.19);
  gStyle->SetStatW(0.24);
  gStyle->SetStatX(0.9);
  gStyle->SetStatY(0.9);

  gStyle->SetPadTopMargin(0.07);
  gStyle->SetPadBottomMargin(0.13);
  gStyle->SetPadLeftMargin(0.12);
  gStyle->SetPadRightMargin(0.05);

  gStyle->SetOptTitle(0);
  gStyle->SetTitleFont(42);
  gStyle->SetTitleColor(1);
  gStyle->SetTitleTextColor(1);
  gStyle->SetTitleFillColor(10);
  gStyle->SetTitleFontSize(0.05);

  gStyle->SetTitleColor(1, "XYZ");
  gStyle->SetTitleFont(42, "XYZ");
  gStyle->SetTitleSize(0.05, "XYZ");
  gStyle->SetTitleXOffset(0.9);
  gStyle->SetTitleYOffset(1.05);
 
  gStyle->SetLabelColor(1, "XYZ");
  gStyle->SetLabelFont(42, "XYZ");
  gStyle->SetLabelOffset(0.007, "XYZ");
  gStyle->SetLabelSize(0.04, "XYZ");

  gStyle->SetAxisColor(1, "XYZ");
  gStyle->SetStripDecimals(1); 
  gStyle->SetTickLength(0.025, "XYZ");
  gStyle->SetNdivisions(510, "XYZ");
  gStyle->SetPadTickX(1); 
  gStyle->SetPadTickY(1);

  gStyle->SetOptLogx(0);
  gStyle->SetOptLogy(0);
  gStyle->SetOptLogz(0);

  gStyle->SetPaperSize(20.,20.);
  gStyle->SetPaintTextFormat(".2f");

}

void CMS_lumi(TPad* pad = NULL, string lumi = "", bool up = false, bool skipPreliminary = true, int reduceSize = false, float offset = 0,float offsetLumi = 0){

  TLatex* latex2 = new TLatex();
  latex2->SetNDC();
  latex2->SetTextSize(0.6*pad->GetTopMargin());
  latex2->SetTextFont(42);
  latex2->SetTextAlign(31);
  if(reduceSize)
    latex2->SetTextSize(0.5*pad->GetTopMargin());
  
  if(lumi != "")
    latex2->DrawLatex(0.94+offsetLumi, 0.95,Form("%s fb^{-1} (%d TeV)",lumi.c_str(),centerOfMassEnergy));
  else
    latex2->DrawLatex(0.88+offsetLumi, 0.95,Form("(%d TeV)",centerOfMassEnergy));

  if(up){
    latex2->SetTextSize(0.65*pad->GetTopMargin());
    if(reduceSize)
      latex2->SetTextSize(0.5*pad->GetTopMargin());
    latex2->SetTextFont(62);
    latex2->SetTextAlign(11);    
    latex2->DrawLatex(0.15+offset, 0.95, "CMS");
  }
  else{
    latex2->SetTextSize(0.6*pad->GetTopMargin());
    if(reduceSize)
      latex2->SetTextSize(0.45*pad->GetTopMargin());
    else if(reduceSize == 2)
      latex2->SetTextSize(0.40*pad->GetTopMargin());

    latex2->SetTextFont(62);
    latex2->SetTextAlign(11);    
    latex2->DrawLatex(0.175+offset, 0.85, "CMS");
  }

  if(not skipPreliminary){
    
    if(up){
      latex2->SetTextSize(0.65*pad->GetTopMargin());
      latex2->SetTextFont(52);
      latex2->SetTextAlign(11);
      latex2->DrawLatex(0.25+offset, 0.95, "Preliminary");
    }
    else{
      latex2->SetTextSize(0.6*pad->GetTopMargin());
      if(reduceSize)
	latex2->SetTextSize(0.45*pad->GetTopMargin());
      latex2->SetTextFont(52);
      latex2->SetTextAlign(11);    
      if(reduceSize)
	latex2->DrawLatex(0.235+offset, 0.85, "Preliminary");
      else
	latex2->DrawLatex(0.28+offset, 0.85, "Preliminary");
    }
  }
}


void changeInLatexName(string & variable){

  if(variable == "met")
    variable = "Recoil [GeV]";
  else if(variable == "ht")
    variable = "H_{T} [GeV]";
  else if(variable == "mT")
    variable = "m_{T} [GeV]";
  else if(variable == "njet")
    variable = "N_{jet}";
  else if(variable == "nbjet")
    variable = "N_{bjet}";
  else if(variable == "dphiJJ")
    variable = "#Delta#phi_{jj}";
  else if(variable == "minDphiJJ")
    variable = "min(#Delta#phi_{jj})";
  else if(variable == "minDphiJ1J")
    variable = "min(#Delta#phi_{j_{1}j})";
  else if(variable == "mpruned")
    variable = "m_{pruned} [GeV]";
  else if(variable == "tau2tau1")
    variable = "#tau_{2}/#tau_{1}";
  else if(variable == "bosonPt")
    variable = "p_{T}^{V} [GeV]";
  else if(variable == "jetPt")
    variable = "p_{T}^{jet} [GeV]";
  else if(variable == "boostedJetPt")
    variable = "p_{T}^{jet} [GeV]";

}

pair<string,string> observableName (string name, bool alongX = false){

  stringstream name_tmp(name.c_str());
  string segment;
  vector<string> seglist;
  while(getline(name_tmp, segment,'_')){
    seglist.push_back(segment);
  }

  string variableX;
  string variableY;

  if(seglist.size() == 2){
    variableX = seglist.back();
    variableY = seglist.front();
    changeInLatexName(variableX);
    changeInLatexName(variableY);
  }
  else{
    variableX = seglist.at(1);
    variableY = seglist.front();
    changeInLatexName(variableX);
    changeInLatexName(variableY);
  }

  if(alongX)
    return make_pair(variableX,variableY);
  else
    return make_pair(variableY,variableX);
}


#endif
