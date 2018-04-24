#include "../interface/utility.h"

using namespace std;

// this macro compares efficiency due to a cut on some variables.
// pass comma separated list of variables to be compared in varList (these names are the prefix of histograms in root file made wth mcPlots.py)
//
// pass signal and backgrounds in signalBackgroundList: this macro compares one signal with one background, but if you pass more of any, they are 
// summed up in one component
// use ":" to separate signals and backgrounds, and "," to separate the single signals and the single backgrounds
//
// efficiency_XtoInf is true if you define cut efficiency as integral from X to infinity over full integral, false to define numerator as integral from 0 to X
// if outDir_tmp == "SAME", it is considered as inputFilePath_tmp

void realMakeVariableEfficiencyAndROC(const string& inputFilePath_tmp = "/afs/cern.ch/user/m/mciprian/www/wmass/13TeV/distribution/TREES_1LEP_80X_V3_WENUSKIM_V5/whelicity_signal_region/full2016dataBH_puAndTrgSf_ptResScale_09_04_2018_restrictPt_HLT27_forAN_noUpPt_noMt/eta_0p0_1p479/",
				  const string& fileName = "test_plots.root",
				  const TString& varList = "trkmt_trkmetEleCorr_dy,pfmt", 
				  const TString& legendList = "Trk M_{T},PF M_{T}",
				  const TString& signalBackgroundList = "W:data_fakes", // S and B separated by ":", multiple signals or backgrounds separated by ","
				  const TString& signalBackgroundLegendList = "W+jets,QCD (FR)",
				  const Bool_t efficiency_XtoInf = true, 
				  const string& outDir_tmp = "SAME" 
				  ) 
{
  
  string outDir = ((outDir_tmp == "SAME") ? inputFilePath_tmp : (outDir_tmp));
  string inputFileName = inputFilePath_tmp + fileName;

  createPlotDirAndCopyPhp(outDir);
  adjustSettings_CMS_lumi(outDir);

  vector<string> vars;
  cout << "Variables to plot: " << endl;
  getVectorCStringFromTStringList(vars, varList, ",", true);

  vector<TString> signalBackground;
  //cout << "Signals and backgrounds: " << endl;
  getVectorTStringFromTStringList(signalBackground, signalBackgroundList, ":", false);

  vector<string> signals;
  cout << "Signals: " << endl;
  getVectorCStringFromTStringList(signals, signalBackground[0], ",", true);
  vector<string> backgrounds;
  cout << "Backgrounds: " << endl;
  getVectorCStringFromTStringList(backgrounds, signalBackground[1], ",", true);

  gROOT->SetBatch(kTRUE);
  TH1::SetDefaultSumw2(); //all the following histograms will automatically call TH1::Sumw2()                  
  cout << endl;

  TFile* inputFile = new TFile(inputFileName.c_str(),"READ");
  if (!inputFile || inputFile->IsZombie()) {
    cout << "Error: file not opened. Exit" << endl;
    exit(EXIT_FAILURE);
  }

  inputFile->cd();

  // vector<plotManager> myPlot;
  // myPlot.push_back(plotManager("trkmt_trkmetEleCorr_dy","W Trk m_{T}","trkmt_trkmetEleCorr_dy",1));
  // myPlot.push_back(plotManager("pfmt","W PF m_{T} (pfmt)","pfmt",1));
  
  vector<TGraph*> gr_roc_S_B;
  vector<string> leg_roc;
  if (legendList == "") getVectorCStringFromTStringList(leg_roc,  varList, ",", false);
  else                  getVectorCStringFromTStringList(leg_roc,  legendList, ",", false);

  vector<string> sigBkgLegendEntry;
  getVectorCStringFromTStringList(sigBkgLegendEntry, signalBackgroundLegendList, ",", false);

  TH1D* hbackground = NULL;
  TH1D* hsignal = NULL;
  TH1D* htmp = NULL;

  for (UInt_t i = 0; i < vars.size(); i++) {

    //if ( i > 0 ) break;  for tests with only first entry

    // hsignal = (TH1D*) getHistCloneFromFile(inputFile, Form("%s_W",vars[i].c_str()), "");
    // hbackground = (TH1D*) getHistCloneFromFile(inputFile, Form("%s_data_fakes_fakes",vars[i].c_str()), "");

    // checkNotNullPtr(hsignal,"hsignal");
    // checkNotNullPtr(hbackground,"hbackground");
     
    for (UInt_t isig = 0; isig < signals.size(); ++isig) {
      htmp = (TH1D*) getHistCloneFromFile(inputFile, Form("%s_%s",vars[i].c_str(),signals[isig].c_str()), "");
      checkNotNullPtr(htmp,Form("hsignal:%s",signals[isig].c_str()));
      if (isig == 0) hsignal = (TH1D*) htmp->Clone("hsignal");
      else           hsignal->Add(htmp);
    }

    for (UInt_t ibkg = 0; ibkg < backgrounds.size(); ++ibkg) {
      htmp = (TH1D*) getHistCloneFromFile(inputFile, Form("%s_%s",vars[i].c_str(),backgrounds[ibkg].c_str()), "");
      checkNotNullPtr(htmp,Form("hbackground:%s",backgrounds[ibkg].c_str()));
      if (ibkg == 0) hbackground = (TH1D*) htmp->Clone("hbackground");
      else           hbackground->Add(htmp);
    }

    addOutliersInHistoRange(hsignal);
    addOutliersInHistoRange(hbackground);

    ///////////////////////////////////
    // efficiencies
    ///////////////////////////////////

    // 21 points for efficiency (from 0 to 1 , step of 5%)
    TGraph* gr_wjets = new TGraph(21);
    TGraph* gr_qcd = new TGraph(gr_wjets->GetN());

    quantiles(gr_wjets,hsignal, efficiency_XtoInf);
    quantiles(gr_qcd,hbackground, efficiency_XtoInf);

    gr_roc_S_B.push_back(new TGraph(gr_wjets->GetN())); // efficiency from 0 to 100 % included
    makeROC(gr_roc_S_B.back(), hsignal, hbackground, efficiency_XtoInf);

    TGraph* gr_sob = new TGraph(gr_wjets->GetN());
    Double_t max_sob = doSoverB(gr_sob, hsignal, hbackground, efficiency_XtoInf);

    TCanvas* canvas = new TCanvas("canvas","",600,600);
    canvas->SetRightMargin(0.06);
    canvas->cd();
    TPad *pad = new TPad("pad","",0,0,1,1);
    pad->SetFillColor(0);
    pad->SetGrid();
    pad->SetRightMargin(0.09);
    pad->Draw();
    pad->cd();
    gr_wjets->SetMarkerStyle(21);
    gr_wjets->SetMarkerColor(kRed);
    gr_wjets->SetLineColor(kRed);
    gr_wjets->SetFillColor(kRed);
    gr_wjets->SetTitle(Form("quantiles;%s;efficiency",hsignal->GetXaxis()->GetTitle()));

    gr_wjets->Draw("alp");

    gr_qcd->SetMarkerStyle(21);
    gr_qcd->SetMarkerColor(kBlue);
    gr_qcd->SetLineColor(kBlue);
    gr_qcd->SetFillColor(kBlue);
    gr_qcd->Draw("lp same");
    canvas->Update();

    TLegend leg (0.15,0.15,0.55,0.3);
    leg.SetFillColor(0);
    leg.SetFillStyle(0);
    leg.SetBorderSize(0);
    leg.AddEntry(gr_wjets,sigBkgLegendEntry[0].c_str(),"LF");
    leg.AddEntry(gr_qcd,sigBkgLegendEntry[1].c_str(),"LF");
    leg.Draw("same");
    //    canvas->RedrawAxis("sameaxis");

    canvas->cd();
    TPad *overlay = new TPad("overlay","",0,0,1,1);
    overlay->SetFillStyle(4000);
    overlay->SetFillColor(0);
    overlay->SetFrameFillStyle(4000);
    overlay->SetRightMargin(0.09);
    overlay->Draw("same");
    overlay->cd();
    gr_sob->SetMarkerStyle(20);
    gr_sob->SetMarkerColor(kGreen+2);
    gr_sob->SetLineColor(kGreen+2);
    gr_sob->SetFillColor(kGreen+2);
    leg.AddEntry(gr_sob,"S/B","LF");
    leg.Draw("same");

    vector<Double_t> goodYmax = {1.1, 5.5, 11, 27.5, 55};
    Double_t xmin = gr_wjets->GetXaxis()->GetXmin();
    Double_t ymin = gr_wjets->GetYaxis()->GetXmin();
    Double_t xmax = gr_wjets->GetXaxis()->GetXmax();
    Double_t ymax = goodYmax.back();; //(Int_t) max_sob * 1.5;  // 27.5
    // cout << "xmin,xmax = " << xmin << "," << xmax << endl;
    // the max should be a multiple of 5.5, the lowest larger than max_sob (not all multiples are good)
    // in order to have ticks on the right vertical axis match those on the left
    // good numbers for ymax are: 5.5 11 27.5 55
    for (UInt_t im = 0; im < goodYmax.size(); im++) {
      if (goodYmax[im] > max_sob) {
	ymax = goodYmax[im]; 
	break;
      }
    }

    TH1F *hframe = overlay->DrawFrame(xmin,ymin,xmax,ymax);
    //hframe->SetNdivisions(hr->GetNdivisions(),"+LNI");
    // hframe->SetTickLength(0, "Y");
    // hframe->SetTickLength(0, "X");
    hframe->GetXaxis()->SetLabelOffset(99);
    hframe->GetYaxis()->SetLabelOffset(99);
    gr_sob->Draw("LP same");
    gr_sob->GetXaxis()->SetRangeUser(xmin,xmax);

    //cout << "sob xmax, max_xi: " << gr_sob->GetXaxis()->GetXmax() << ", " << gr_sob->GetX()[gr_sob->GetN()-1] << endl;
    // 7th argument to be tuned by hand, it is the number of divisions for the y axis ticks
    TGaxis *axis = new TGaxis(xmax,ymin,xmax, ymax,ymin,ymax,1006,"+LNI");
    axis->SetLineColor(kBlack);
    axis->SetTitle("S/B");
    axis->SetLabelColor(kBlack);
    axis->Draw("same");  

    canvas->SaveAs((outDir+vars[i].c_str()+"_quantile.png").c_str());  
    canvas->SaveAs((outDir+vars[i].c_str()+"_quantile.pdf").c_str());

  }

  vector<Double_t> legCoord = {0.5, 0.15, 0.9, 0.35};
  drawGraph(gr_roc_S_B, Form("background efficiency: %s",sigBkgLegendEntry[1].c_str()),Form("signal efficiency: %s",sigBkgLegendEntry[0].c_str()), "roc", outDir, leg_roc, legCoord);

  inputFile->Close();

  cout << endl;

}

//====================================================

void makeVariableEfficiencyAndROC(const string& inputFilePath_tmp = "/afs/cern.ch/user/m/mciprian/www/wmass/13TeV/distribution/TREES_1LEP_80X_V3_WENUSKIM_V5/whelicity_signal_region/full2016dataBH_puAndTrgSf_ptResScale_09_04_2018_restrictPt_HLT27_forAN_noUpPt_noMt/",
				  const TString& subfoldersList = "eta_0p0_1p479/,eta_1p479_2p1/,eta_2p1_2p5/",
				  const string& fileName = "test_plots.root",
				  const TString& varList = "trkmt_trkmetEleCorr_dy,pfmt", 
				  const TString& legendList = "Trk M_{T},PF M_{T}",
				  const TString& signalBackgroundList = "W:data_fakes", // S and B separated by ":", multiple signals or backgrounds separated by ","
				  const TString& signalBackgroundLegendList = "W+jets,QCD (FR)",
				  const Bool_t efficiency_XtoInf = true, 
				  const string& outDir_tmp = "SAME" 
				  ) 
{

  vector<string> subfolders;
  getVectorCStringFromTStringList(subfolders, subfoldersList, ",", false);

  if (subfolders.size() == 0) {
    realMakeVariableEfficiencyAndROC(inputFilePath_tmp,
				     fileName,
				     varList, 
				     legendList,
				     signalBackgroundList,
				     signalBackgroundLegendList,
				     efficiency_XtoInf, 
				     outDir_tmp);
  } else {
    
    for (UInt_t i = 0; i < subfolders.size(); ++i) {

      string outputFolder = (outDir_tmp == "SAME") ? outDir_tmp : (outDir_tmp + subfolders[i]);
      realMakeVariableEfficiencyAndROC(inputFilePath_tmp + subfolders[i],
				       fileName,
				       varList, 
				       legendList,
				       signalBackgroundList,
				       signalBackgroundLegendList,
				       efficiency_XtoInf, 
				       outDir_tmp);
      
    }

  }



}
