#include "../interface/utility.h"

using namespace std;


void makeVariableEfficiencyAndROC(const string& inputFilePath_tmp = "/afs/cern.ch/user/m/mciprian/www/wmass/13TeV/distribution/TREES_1LEP_80X_V3_WENUSKIM_V5/whelicity_signal_region/full2016dataBH_puAndTrgSf_ptResScale_25_03_2018_restrictPt_HLT27_mtPlots/eta_0p0_1p479/",
				  const string& fileName = "test_plots.root",
				  const TString& varList = "trkmt_trkmetEleCorr_dy,pfmt", 
				  const TString& legendList = "Trk M_{T},PF M_{T}", 
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

  TH1D* hqcd = NULL;
  TH1D* hwjets = NULL;

  for (UInt_t i = 0; i < vars.size(); i++) {

    //if ( i > 0 ) break;  for tests with only first entry

    //////////////////////////
    // add suffix about the region in canvas title

    vector<TH1*> stackElementMC;  // first element is the one on top of the stack
    vector<string> stackLegendMC;

    hwjets = (TH1D*) getHistCloneFromFile(inputFile, Form("%s_W",vars[i].c_str()), "");
    hqcd = (TH1D*) getHistCloneFromFile(inputFile, Form("%s_data_fakes_fakes",vars[i].c_str()), "");

    checkNotNullPtr(hwjets,"hwjets");
    checkNotNullPtr(hqcd,"hqcd");
     
    addOutliersInHistoRange(hwjets);
    addOutliersInHistoRange(hqcd);

    stackElementMC.push_back(hwjets);
    stackElementMC.push_back(hqcd);
     
    stackLegendMC.push_back("W+jets");
    stackLegendMC.push_back("QCD (FR)");

    ///////////////////////////////////
    // efficiencies
    ///////////////////////////////////

    // 21 points for efficiency (from 0 to 1 , step of 5%)
    TGraph* gr_wjets = new TGraph(21);
    TGraph* gr_qcd = new TGraph(gr_wjets->GetN());
    Bool_t efficiency_XtoInf = true;   

    quantiles(gr_wjets,hwjets, efficiency_XtoInf);
    quantiles(gr_qcd,hqcd, efficiency_XtoInf);

    gr_roc_S_B.push_back(new TGraph(gr_wjets->GetN())); // efficiency from 0 to 100 % included
    makeROC(gr_roc_S_B.back(), hwjets, hqcd, efficiency_XtoInf);

    TGraph* gr_sob = new TGraph(gr_wjets->GetN());
    Double_t max_sob = doSoverB(gr_sob, hwjets, hqcd, efficiency_XtoInf);

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
    gr_wjets->SetTitle(Form("quantiles;%s;efficiency",hwjets->GetXaxis()->GetTitle()));

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
    leg.AddEntry(gr_wjets,"W","LF");
    leg.AddEntry(gr_qcd,"QCD (FR)","LF");
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

  vector<Double_t> legCoord = {0.15, 0.6, 0.55, 0.8};
  drawGraph(gr_roc_S_B, "background efficiency (QCD)","signal efficiency (W)", "roc_MT", outDir, leg_roc, legCoord);

  inputFile->Close();

  cout << endl;

}
