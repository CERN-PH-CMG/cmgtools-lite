#include "../interface/utility.h"
#include "../../functions.cc"
#include "../../w-helicity-13TeV/functionsWMass.cc"

#define CHECK_EVERY_N 50000
#define N_MAX_ENTRIES_PER_SAMPLE 0 // for tests, use number <= 0 to use all events in each sample

using namespace std;

//static float intLumi = 30.9 // 35.9 for muons, 30.9 for electrons, measured in 1/fb
//static vector<Double_t> eleEtaBinEdges_double = {0.0, 1.0, 1.479, 2.1, 2.5};
static vector<Double_t> etaBinEdgesTemplate = {-2.5,-2.3,-2.1,-1.9,-1.7,-1.566,-1.4442,-1.3,-1.2,-1.1,-1.0,-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.1,1.2,1.3,1.4442,1.566,1.7,1.9,2.1,2.3,2.5};
static vector<Double_t> ptBinEdgesTemplate = {30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45};
static Int_t nPDFweight = 60;

//=============================================================

void fillHistograms(const string& treedir = "./", 
		    const string& outdir = "./", 
		    const Sample& sample = Sample::wjets, 
		    TFile* outputFile = NULL
		    ) 
{

  gROOT->SetBatch(kTRUE);
  TH1::SetDefaultSumw2(); //all the following histograms will automatically call TH1::Sumw2()  

  cout << endl;
  cout << "================================================" << endl;
  cout << endl;

  if (outputFile == NULL) {
    cout << "Error: file is NULL. please check. Exit ..." << endl;
    exit(EXIT_FAILURE);
  }

  outputFile->cd();

  TDirectory *dirSample = NULL;
  string sampleDir = getStringFromEnumSample(sample).c_str();
  cout << "Sample --> " << sampleDir << endl;
  if (outputFile->GetKey(sampleDir.c_str())) dirSample = outputFile->GetDirectory(sampleDir.c_str());
  else dirSample = outputFile->mkdir(sampleDir.c_str());
  dirSample->cd();

  cout << endl;

  Int_t netaBins = etaBinEdgesTemplate.size() -1;
  Int_t nptBins = ptBinEdgesTemplate.size() -1;
  Int_t nBinsTemplate = netaBins * netaBins;

  TChain* chain = new TChain("tree");
  // INFO: the new friend trees at 13 TeV are inside a "tree_Friend_<sampleName>.root" file, and the tree's name is "Friends"
  // friend trees are still located in a directory called "friends" with respect to base trees
  TChain* friendChain = new TChain("Friends");      
  //TChain* friendChain = NULL;  // leave as NULL if you don't use friend trees
  TChain* SfFriendChain = NULL;
  //if (sampleDir.find("data") == string::npos && sampleDir.find("fake") == string::npos) SfFriendChain = new TChain("sf/t");  
  // leave as NULL if you don't use friend trees

  vector<Double_t> sumGenWeightVector;
  buildChain(chain, sumGenWeightVector, use8TeVSample, treedir, sample, friendChain, SfFriendChain); 

  // change directory again, when building chain something was messed up
  dirSample->cd();
  //  cout << "check" << endl;

  Bool_t isWsignal = false;
  if (sampleDir.find("wenujets") != string::npos or sampleDir.find("wmunujets") != string::npos) isWsignal = true;

  TTreeReader reader (chain);

  TTreeReaderValue<Int_t> isData(reader,"isData");
  TTreeReaderValue<UInt_t> run   (reader,"run");
  TTreeReaderValue<UInt_t> lumi  (reader,"lumi");
  //TTreeReaderValue<Int_t> nVert  (reader,"nVert");
  //TTreeReaderValue<Float_t> rho  (reader,"rho");

  // trigger
  TTreeReaderValue<Int_t> HLT_SingleElectron(reader,"HLT_BIT_HLT_Ele27_WPTight_Gsf_v");

  // reco met
  // TTreeReaderValue<Float_t> tkmet    (reader,"met_trkPt");
  // TTreeReaderValue<Float_t> tkmet_phi(reader,"met_trkPhi");
  TTreeReaderValue<Float_t> pfmet    (reader,"met_pt");
  TTreeReaderValue<Float_t> pfmet_phi(reader,"met_phi");


  // LepGood branch
  TTreeReaderValue<Int_t> nlep      (reader,"nLepGood");
  TTreeReaderArray<Int_t> lep_pdgId (reader,"LepGood_pdgId");
  TTreeReaderArray<Int_t> lep_charge(reader,"LepGood_charge");  
  TTreeReaderArray<Float_t> lep_calPt(reader,"LepGood_calPt");
  TTreeReaderArray<Float_t> lep_pt  (reader,"LepGood_pt");
  TTreeReaderArray<Float_t> lep_eta (reader,"LepGood_eta");
  TTreeReaderArray<Float_t> lep_phi (reader,"LepGood_phi");

  // for electronID
  TTreeReaderArray<Int_t> lep_hltId (reader,"LepGood_hltId");  
  TTreeReaderArray<Int_t> lep_Id (reader,"LepGood_customId");  
  TTreeReaderArray<Int_t> lep_tightChargeFix (reader,"LepGood_tightChargeFix");  

  // gen quantities
  TTreeReaderValue<Float_t> nTrueInt(reader,"nTrueInt");
  TTreeReaderValue<Float_t> xsec(reader,"xsec");
  TTreeReaderValue<Float_t> genWeight(reader,"genWeight");
  TTreeReaderArray<Int_t>   lep_mcMatchId(reader,"LepGood_mcMatchId");

  // W MC specific branches
  TTreeReaderArray<Float_t> GenLepDressed_pt(reader,"GenLepDressed_pt");
  TTreeReaderArray<Float_t> GenLepDressed_eta(reader,"GenLepDressed_eta");
  TTreeReaderValue<Float_t> genw_charge(reader,"genw_charge");
  TTreeReaderValue<Float_t> genw_decayId(reader,"genw_decayId");
  TTreeReaderValue<Float_t> genw_pt(reader,"genw_pt");
  // syst weights for W
  TTreeReaderValue<Float_t> qcd_muRUp(reader,"qcd_muRUp");
  TTreeReaderValue<Float_t> qcd_muRDn(reader,"qcd_muRDn");
  TTreeReaderValue<Float_t> qcd_muFUp(reader,"qcd_muFUp");
  TTreeReaderValue<Float_t> qcd_muFDn(reader,"qcd_muFDn");
  TTreeReaderValue<Float_t> qcd_muRmuFUp(reader,"qcd_muRmuFUp");
  TTreeReaderValue<Float_t> qcd_muRmuFDn(reader,"qcd_muRmuFDn");
  TTreeReaderValue<Float_t> qcd_alphaSUp(reader,"qcd_alphaSUp");
  TTreeReaderValue<Float_t> qcd_alphaSDn(reader,"qcd_alphaSDn");
  // pdf
  vector< TTreeReaderValue<Float_t>* > pdfwgt;
  for (Int_t i = 1; i <= nPDFweight; ++i) {
    pdfwgt.push_back( new TTreeReaderValue<Float_t>(reader,Form("hessWgt%d",i)) );
  }

  //////////////////////////////
  // Following is the same as before, in case I decide to use all the samples 
  // If I only run on W, then I don't need to use pointers to create objects depending on the sample

  // // gen quantities
  // TTreeReaderValue<Float_t>* nTrueInt = nullptr;
  // TTreeReaderValue<Float_t>* xsec = nullptr;
  // TTreeReaderArray<Int_t>* lep_mcMatchId = nullptr;
  // TTreeReaderValue<Float_t>* genWeight = nullptr;

  // // W MC specific branches
  // TTreeReaderArray<Float_t>* GenLepDressed_pt = nullptr;
  // TTreeReaderArray<Float_t>* GenLepDressed_eta = nullptr;
  // TTreeReaderValue<Float_t>* genw_charge = nullptr;
  // TTreeReaderValue<Float_t>* genw_decayId = nullptr;
  // // syst weights for W
  // vector<TTreeReaderValue<Float_t> *> pdfwgt;
  // TTreeReaderValue<Float_t>* qcd_muRUp = nullptr;
  // TTreeReaderValue<Float_t>* qcd_muRDn = nullptr;
  // TTreeReaderValue<Float_t>* qcd_muFUp = nullptr;
  // TTreeReaderValue<Float_t>* qcd_muFDn = nullptr;
  // TTreeReaderValue<Float_t>* qcd_muRmuFUp = nullptr;
  // TTreeReaderValue<Float_t>* qcd_muRmuFDn = nullptr;
  // TTreeReaderValue<Float_t>* qcd_alphaSUp = nullptr;
  // TTreeReaderValue<Float_t>* qcd_alphaSDn = nullptr;
  
  // if (sampleDir.find("data") == string::npos && sampleDir.find("fake") == string::npos) {

  //   nTrueInt      = new TTreeReaderValue<Float_t>(reader,"nTrueInt");
  //   xsec          = new TTreeReaderValue<Float_t>(reader,"xsec");
  //   genWeight     = new TTreeReaderValue<Float_t>(reader,"genWeight");
  //   lep_mcMatchId = new TTreeReaderArray<Int_t>(reader,"LepGood_mcMatchId");  

  //   if (isWsignal) {
  //     GenLepDressed_pt  = new TTreeReaderArray<Float_t>(reader,"GenLepDressed_pt");
  //     GenLepDressed_eta = new TTreeReaderArray<Float_t>(reader,"GenLepDressed_eta");
  //     genw_charge       = new TTreeReaderValue<Float_t>(reader,"genw_charge");
  //     genw_decayId      = new TTreeReaderValue<Float_t>(reader,"genw_decayId");
  //     // weights
  //     qcd_muRUp = new TTreeReaderValue<Float_t>(reader,"qcd_muRUp");
  //     qcd_muRDn = new TTreeReaderValue<Float_t>(reader,"qcd_muRDn");
  //     qcd_muFUp = new TTreeReaderValue<Float_t>(reader,"qcd_muFUp");
  //     qcd_muFDn = new TTreeReaderValue<Float_t>(reader,"qcd_muFDn");
  //     qcd_muRmuFUp = new TTreeReaderValue<Float_t>(reader,"qcd_muRmuFUp");
  //     qcd_muRmuFDn = new TTreeReaderValue<Float_t>(reader,"qcd_muRmuFDn");
  //     qcd_alphaSUp = new TTreeReaderValue<Float_t>(reader,"qcd_alphaSUp");
  //     qcd_alphaSDn = new TTreeReaderValue<Float_t>(reader,"qcd_alphaSDn");

  //     for (Int_t i = 1; i <= nPDFweight; ++i) {
  // 	pdfwgt.push_back( new TTreeReaderValue<Float_t>(reader,Form("hessWgt%d",i)) );
  //     }

  //   }

  // }  


  //////////////////////////
  // NOTE
  // values of TTreeReaderValue objects are read with * before the variable name, as if they were pointers
  // Pointers to TTreeReaderValue are used with double * (one to access the pointer's content and the other for the TTreeReaderValue convention)
  // TTreeReaderArray variables are used as normal array variables (if they are pointers to TTreeReaderArray.then you still need a * to access the array)
  //////////////////////////

  /////////////////////////////////////
  // dummy histogram to easily retrieve information on eta-pt bins
  TH2F* h2_etaPt = new TH2F("h2_etaPt","",netaBins,etaBinEdgesTemplate.data(),nptBins,ptBinEdgesTemplate.data());
  h2_etaPt->SetDirectory(0); // I don't want to save this histogram in the output file

  // 1 histogram for each bin of the template and for each charge, hence a double vector of histograms
  vector<string> charges = {"plus","minus"}; // 0 for positive, 1 for negative
  vector<string> chargeSigns = {"+","-"}; // 0 for positive, 1 for negative

  vector<TH1F*> h1_charge_eta;
  vector<TH1F*> h1_charge_pt;
  vector<TH2F*> h2_charge_eta_pt_inclusive;

  vector<TH3F*> h3_charge_eta_pt_globalBin;
  vector< vector<TH3F*> > h3_charge_eta_pt_globalBin_pdf(charges.size());  // will have 60 replicas of pairs of TH3 (the pair is for charge + and -)
  vector<TH3F*> h3_charge_eta_pt_globalBin_alphaSUp;
  vector<TH3F*> h3_charge_eta_pt_globalBin_wptSlopeUp;
  vector<TH3F*> h3_charge_eta_pt_globalBin_muRUp;
  vector<TH3F*> h3_charge_eta_pt_globalBin_muFUp;
  vector<TH3F*> h3_charge_eta_pt_globalBin_muRmuFUp;
  vector<TH3F*> h3_charge_eta_pt_globalBin_alphaSDn;
  vector<TH3F*> h3_charge_eta_pt_globalBin_wptSlopeDn;
  vector<TH3F*> h3_charge_eta_pt_globalBin_muRDn;
  vector<TH3F*> h3_charge_eta_pt_globalBin_muFDn;
  vector<TH3F*> h3_charge_eta_pt_globalBin_muRmuFDn;

  for (UInt_t ch = 0; ch < charges.size(); ++ch) {  
    // for (Int_t bin = 0; bin  < nBinsTemplate; ++bin) {
    //   Int_t ieta = 0;
    //   Int_t ipt = 0;
    //   h2_etaPt->GetBinXYZ(bin+1,ieta,ipt)
    vector<Double_t> globalBin_binning; // temporary vector to be used in TH3 constructor
    for (Int_t bin = 0; bin  <= nBinsTemplate; ++bin) 
      globalBin_binning.push_back(0.5+(Double_t)bin); // note that loop goes from 0 to 600 included

    h1_charge_pt.push_back(new TH1F(Form("h1_%s_pt",charges[ch].c_str()),"",35,30,65));
    h1_charge_eta.push_back(new TH1F(Form("h1_%s_eta",charges[ch].c_str()),"",50,-2.5,2.5));

    h2_charge_eta_pt_inclusive.push_back(new TH2F(Form("h2_%s_eta_pt_inclusive",charges[ch].c_str()),"",
						  netaBins,etaBinEdgesTemplate.data(),
						  nptBins,ptBinEdgesTemplate.data())	  
					 );

    h3_charge_eta_pt_globalBin.push_back(new TH3F(Form("h3_%s_eta_pt_globalBin",charges[ch].c_str()),"",
						  netaBins,etaBinEdgesTemplate.data(),
						  nptBins,ptBinEdgesTemplate.data(),
						  nBinsTemplate,globalBin_binning.data())
					 );
    h3_charge_eta_pt_globalBin_alphaSUp.push_back(new TH3F(Form("h3_%s_eta_pt_globalBin_alphaSUp",charges[ch].c_str()),"",
							   netaBins,etaBinEdgesTemplate.data(),
							   nptBins,ptBinEdgesTemplate.data(),
							   nBinsTemplate,globalBin_binning.data())
					 );
    h3_charge_eta_pt_globalBin_alphaSDn.push_back(new TH3F(Form("h3_%s_eta_pt_globalBin_alphaSDn",charges[ch].c_str()),"",
							   netaBins,etaBinEdgesTemplate.data(),
							   nptBins,ptBinEdgesTemplate.data(),
							   nBinsTemplate,globalBin_binning.data())
					 );
    h3_charge_eta_pt_globalBin_muRUp.push_back(new TH3F(Form("h3_%s_eta_pt_globalBin_muRUp",charges[ch].c_str()),"",
							   netaBins,etaBinEdgesTemplate.data(),
							   nptBins,ptBinEdgesTemplate.data(),
							   nBinsTemplate,globalBin_binning.data())
					 );
    h3_charge_eta_pt_globalBin_muRDn.push_back(new TH3F(Form("h3_%s_eta_pt_globalBin_muRDn",charges[ch].c_str()),"",
							   netaBins,etaBinEdgesTemplate.data(),
							   nptBins,ptBinEdgesTemplate.data(),
							   nBinsTemplate,globalBin_binning.data())
					 );
    h3_charge_eta_pt_globalBin_muFUp.push_back(new TH3F(Form("h3_%s_eta_pt_globalBin_muFUp",charges[ch].c_str()),"",
							   netaBins,etaBinEdgesTemplate.data(),
							   nptBins,ptBinEdgesTemplate.data(),
							   nBinsTemplate,globalBin_binning.data())
					 );
    h3_charge_eta_pt_globalBin_muFDn.push_back(new TH3F(Form("h3_%s_eta_pt_globalBin_muFDn",charges[ch].c_str()),"",
							   netaBins,etaBinEdgesTemplate.data(),
							   nptBins,ptBinEdgesTemplate.data(),
							   nBinsTemplate,globalBin_binning.data())
					 );
    h3_charge_eta_pt_globalBin_muRmuFUp.push_back(new TH3F(Form("h3_%s_eta_pt_globalBin_muRmuFUp",charges[ch].c_str()),"",
							   netaBins,etaBinEdgesTemplate.data(),
							   nptBins,ptBinEdgesTemplate.data(),
							   nBinsTemplate,globalBin_binning.data())
					 );
    h3_charge_eta_pt_globalBin_muRmuFDn.push_back(new TH3F(Form("h3_%s_eta_pt_globalBin_muRmuFDn",charges[ch].c_str()),"",
							   netaBins,etaBinEdgesTemplate.data(),
							   nptBins,ptBinEdgesTemplate.data(),
							   nBinsTemplate,globalBin_binning.data())
					 );
    h3_charge_eta_pt_globalBin_wptSlopeUp.push_back(new TH3F(Form("h3_%s_eta_pt_globalBin_wptSlopeUp",charges[ch].c_str()),"",
							   netaBins,etaBinEdgesTemplate.data(),
							   nptBins,ptBinEdgesTemplate.data(),
							   nBinsTemplate,globalBin_binning.data())
					 );
    h3_charge_eta_pt_globalBin_wptSlopeDn.push_back(new TH3F(Form("h3_%s_eta_pt_globalBin_wptSlopeDn",charges[ch].c_str()),"",
							   netaBins,etaBinEdgesTemplate.data(),
							   nptBins,ptBinEdgesTemplate.data(),
							   nBinsTemplate,globalBin_binning.data())
					 );

    for (Int_t ipdf = 1; ipdf <= nPDFweight; ++ipdf) {
      h3_charge_eta_pt_globalBin_pdf[ch].push_back(new TH3F(Form("h3_%s_eta_pt_globalBin_pdf%d",charges[ch].c_str(),ipdf),"",
							    netaBins,etaBinEdgesTemplate.data(),
							    nptBins,ptBinEdgesTemplate.data(),
							    nBinsTemplate,globalBin_binning.data())
						   );
    }

  }
  ////////////////////
  ////////////////////

  // start event loop                                                                                                                     
                    
  long int nTotal = chain->GetEntries();
  long int nEvents = 0;
  long int nEventsInSample = 0; // events processed for each sample

  Int_t EB0orEE1 = -1;

  Bool_t negativeLeptonHasPassedSelection = false;
  Bool_t positiveLeptonHasPassedSelection = false;

  Double_t wgt = 1.0;
  Double_t lep1pt = 0.0;
  ////////////////////////////////////////////
  // to get correct weight depending on sample in chain
  string currentFile = "";
  Int_t ifile = 0;
  ////////////////////

  Double_t intLumiPb = 1000.0 * intLumi;
  Double_t intLumiPbXsecZ = intLumiPb * 1921.8 * 3.; // for Z the xsec in the ntuples is no more valid, it changed
  Double_t wjets_NLO_wgt_partial = intLumiPb * (3. * 20508.9) / 3.54324749853e+13;  // WJetsToLNu_NLO, just to speed up
 
  while (reader.Next()) {
  
    cout.flush();
    if (nEvents % CHECK_EVERY_N == 0) cout << "\r" << "Analyzing events " << ((Double_t) nEvents)/nTotal*100.0 << " % ";
    //cout << "entry : " << nEvents << endl;
    nEvents++;
    nEventsInSample++;

    if (dynamic_cast<TChain*>(reader.GetTree())->GetFile()->GetName() != currentFile and currentFile != "") { 
      currentFile = dynamic_cast<TChain*>(reader.GetTree())->GetFile()->GetName();                   
      ifile ++;                                                                                      
      nEventsInSample = 1; // reset nEvents when sub sample is changed (useful with N_MAX_ENTRIES_PER_SAMPLE for debugging)
    } else if (dynamic_cast<TChain*>(reader.GetTree())->GetFile()->GetName() != currentFile and currentFile == "") {
      currentFile = dynamic_cast<TChain*>(reader.GetTree())->GetFile()->GetName();                         
    }      
    if (N_MAX_ENTRIES_PER_SAMPLE > 0 && nEventsInSample > N_MAX_ENTRIES_PER_SAMPLE) continue; // this does not skip the tree, but still loop on all events doing nothing

    //if (nEvents > 100) break;  // temporary line for tests
    //checkPoint(currentFile,200,nEvents);

    negativeLeptonHasPassedSelection = false;
    positiveLeptonHasPassedSelection = false;
  
    Double_t lep1calPt = ptElFull(lep_calPt[0],lep_eta[0]);
    Double_t absLep1eta = fabs(lep_eta[0]);  

    // selection
    if (lep_hltId[0] < 1) continue;
    if (*HLT_SingleElectron != 1) continue;
    if (*nlep != 1) continue;
    if (fabs(lep_pdgId[0]) != 11) continue;
    if (not isFloatEqual(*genw_decayId, 12.0)) continue;
    if (lep_mcMatchId[0]*lep_charge[0] == -24) continue;
    if (absLep1eta > 2.5) continue;
    if (absLep1eta > 1.4442 and absLep1eta < 1.566) continue;
    if (lep1calPt < 30 or lep1calPt > 45) continue;
    if (lep_Id[0] != 1 or lep_tightChargeFix[0] != 2) continue;
    if (mt_2(*pfmet,*pfmet_phi,lep1calPt,lep_phi[0]) < 40) continue;

    // if (fabs(lep_etaSc[0]) < 1.479) {
    // } else {
    // }	

    // if (lep_tightId[0]  < tightID->cutBasedId() || 
    // 	lep_lostHits[0] > tightID->maxMissingHits() || 
    // 	fabs(lep_dz[0]) > tightID->dz() || 
    // 	fabs(lep_dxy[0]) > tightID->dxy() || 
    // 	lep_convVeto[0] != tightID->convVeto()
    // 	) 
    //   { 
    // 	passLooseAndNotTightSeleForFR_noIso = true;
    //   }
    // if (lep_relIso04[0] < tightID->relIso04()) passIsoSel = true;
    // if (passLooseAndNotTightSeleForFR_noIso || not passIsoSel) passLooseAndNotTightSeleForFR = true;
    // if (not useFakeRateForElectron and passLooseAndNotTightSeleForFR_noIso) continue; // if not using fake rate, require tight selection (without isolation here)

    // if (fabs(lep_eta[0]) < 1.479) EB0orEE1 = 0;
    // else EB0orEE1 = 1;

    // // hardcoded value for Z cross-section, because it was updated wrt our ntuple content                     
    // if (*isData == 1)                                 wgt = 1.0;
    // else {
    //   // for some processes, like top, the sum of weights depends on subprocess, so we have sumGenWeightVector[ifile] which stores 1./Sum(gen weights)
    //   if (isWsignal)                                    wgt = wjets_NLO_wgt_partial *  *genWeight; // done like this to speed it up
    //   else if (sampleDir.find("zjets") != string::npos) wgt = intLumiPbXsecZ *  *genWeight * sumGenWeightVector[ifile];    
    //   else                                              wgt = intLumiPb *  *genWeight * *xsec * sumGenWeightVector[ifile]; 
    // }

    wgt = wjets_NLO_wgt_partial * *genWeight; // done like this to speed it up
    // PU reweigthing, trigger scale factors, lepton efficiency scale factors
    wgt *= (puw2016_nTrueInt_36fb(*nTrueInt) * 
	    trgSF_We(lep_pdgId[0],lep_pt[0],lep_eta[0],2) *// * 
	    leptonSF_We(lep_pdgId[0],lep_pt[0],lep_eta[0])
	    );    
    
    // Get charge index: 0 for positive, 1 for negative
    Int_t chargeIndex = 0; 
    if (lep_pdgId[0] > 0) {
      negativeLeptonHasPassedSelection = true;
      chargeIndex = 1;
    } else {
      positiveLeptonHasPassedSelection = true;
      chargeIndex = 0;
    }

    // Now start filling histograms
    h1_charge_pt[chargeIndex]->Fill(lep1calPt, wgt);
    h1_charge_eta[chargeIndex]->Fill(lep_eta[0], wgt);
    h2_charge_eta_pt_inclusive[chargeIndex]->Fill(lep_eta[0],lep1calPt, wgt);
    Int_t globalBinEtaPt = h2_etaPt->FindFixBin(GenLepDressed_eta[0], GenLepDressed_pt[0]);
    // fill with reco quantities the bin corresponding to the gen level quantities (it is equivalent to cutting on gen level variables)
    h3_charge_eta_pt_globalBin[chargeIndex]->Fill(lep_eta[0],lep1calPt, globalBinEtaPt, wgt);
    // wpt syst
    h3_charge_eta_pt_globalBin_wptSlopeUp[chargeIndex]->Fill(lep_eta[0],lep1calPt, globalBinEtaPt, wpt_slope_weight(*genw_pt,0.95,0.005) * wgt);
    h3_charge_eta_pt_globalBin_wptSlopeDn[chargeIndex]->Fill(lep_eta[0],lep1calPt, globalBinEtaPt, wpt_slope_weight(*genw_pt,1.05,-0005) * wgt);
    // qcd syst
    h3_charge_eta_pt_globalBin_muRUp[chargeIndex]->Fill(lep_eta[0],lep1calPt, globalBinEtaPt, *qcd_muRUp * wgt);
    h3_charge_eta_pt_globalBin_muRDn[chargeIndex]->Fill(lep_eta[0],lep1calPt, globalBinEtaPt, *qcd_muRDn * wgt);
    h3_charge_eta_pt_globalBin_muFUp[chargeIndex]->Fill(lep_eta[0],lep1calPt, globalBinEtaPt, *qcd_muFUp * wgt);
    h3_charge_eta_pt_globalBin_muFDn[chargeIndex]->Fill(lep_eta[0],lep1calPt, globalBinEtaPt, *qcd_muFDn * wgt);
    h3_charge_eta_pt_globalBin_muRmuFUp[chargeIndex]->Fill(lep_eta[0],lep1calPt, globalBinEtaPt, *qcd_muRmuFUp * wgt);
    h3_charge_eta_pt_globalBin_muRmuFDn[chargeIndex]->Fill(lep_eta[0],lep1calPt, globalBinEtaPt, *qcd_muRmuFDn * wgt);
    h3_charge_eta_pt_globalBin_alphaSUp[chargeIndex]->Fill(lep_eta[0],lep1calPt, globalBinEtaPt, *qcd_alphaSUp * wgt);
    h3_charge_eta_pt_globalBin_alphaSDn[chargeIndex]->Fill(lep_eta[0],lep1calPt, globalBinEtaPt, *qcd_alphaSDn * wgt);
    // pdf syst
    for (Int_t ipdf = 0; ipdf < nPDFweight; ++ipdf) {
      h3_charge_eta_pt_globalBin_pdf[chargeIndex][ipdf]->Fill(lep_eta[0],lep1calPt, globalBinEtaPt, **(pdfwgt[ipdf]) * wgt);
    }

  }

  delete h2_etaPt;  // no need to save this as well
  cout << endl;
  cout << "Writing on output file" << endl;

  // if the file is opened in UPDATE mode, the following should overwrite an object if its key inside the file already exists
  outputFile->Write(0,TObject::kOverwrite);

  cout << "End of fillHistograms for " << sampleDir << endl;
  cout << endl;

}


//=============================================================

void loopNtuplesSkeleton(const string& treedir = "/eos/cms/store/group/dpg_ecal/comm_ecal/localreco/TREES_1LEP_80X_V3_WENUSKIM_V5_TINY/", 
			 const string& outdir = "./", 
			 const string& outfileName = "wmass_varhists.root"
			 ) {

  createPlotDirAndCopyPhp(outdir);

  gROOT->SetBatch(kTRUE);
  TH1::SetDefaultSumw2(); //all the following histograms will automatically call TH1::Sumw2()  
  cout << endl;


  string cmssw_base = getEnvVariable("CMSSW_BASE");
  cout << "CMSSW_BASE = " << cmssw_base << endl;
  // //compile some stuff to get functions used in heppy for some reweightings
  // string rootLibraries = string(gSystem->GetLibraries());                                                                                       
  // //cout << "gSystem->GetLibraries():" << endl;
  // //cout << gSystem->GetLibraries() << endl;
  // if (rootLibraries.find("/w-helicity-13TeV/functionsWMass_cc.so") == string::npos) 
  //   compileMacro("src/CMGTools/WMass/python/plotter/w-helicity-13TeV/functionsWMass.cc");
  // if (rootLibraries.find("/functions_cc.so") == string::npos)
  //   compileMacro("src/CMGTools/WMass/python/plotter/functions.cc");                               

  // gROOT->ProcessLine(Form(".L %s/src/CMGTools/WMass/python/plotter/functions.cc+",cmssw_base.c_str()));
  // gROOT->ProcessLine(Form(".L %s/src/CMGTools/WMass/python/plotter/w-helicity-13TeV/functionsWMass.cc+",cmssw_base.c_str()));

  // cout << "PU(0) = " << puw2016_nTrueInt_36fb(0) << endl;
  // cout << "PU(1) = " << puw2016_nTrueInt_36fb(1) << endl;
  // cout << "PU(5) = " << puw2016_nTrueInt_36fb(5) << endl;
  // cout << "PU(30) = " << puw2016_nTrueInt_36fb(30) << endl;
  // cout << "PU(99) = " << puw2016_nTrueInt_36fb(99) << endl;
  // cout << "PU(100) = " << puw2016_nTrueInt_36fb(100) << endl;
  // cout << "TEST SUCCESSFUL" << endl;
  // return;

  //TFile* outputFile = new TFile((outdir + outfileName).c_str(),"RECREATE");
  TFile* outputFile = new TFile((outdir + outfileName).c_str(),"UPDATE");
  if (!outputFile || outputFile->IsZombie()) {
    cout << "Error: file not opened. Exit" << endl;
    exit(EXIT_FAILURE);
  }

  outputFile->cd();

  fillHistograms(treedir, outdir, Sample::wenujets, outputFile);
  // fillHistograms(treedir, outdir, Sample::data_singleEG, outputFile);
  // if (useFakeRateForElectron) 
  //   fillHistograms(treedir, outdir, Sample::qcd_ele_fake, outputFile); // use fake rate only in SR
  // fillHistograms(treedir, outdir, Sample::qcd_ele, outputFile);
  //  fillHistograms(treedir, outdir, Sample::wenujets, outputFile);
  // fillHistograms(treedir, outdir, Sample::wmunujets, outputFile);
  // fillHistograms(treedir, outdir, Sample::wtaunujets, outputFile);
  // fillHistograms(treedir, outdir, Sample::zjets, outputFile);
  // fillHistograms(treedir, outdir, Sample::top, outputFile);
  // fillHistograms(treedir, outdir, Sample::diboson, outputFile);
  
  outputFile->Close();
  delete outputFile;

  if (outdir != "./") {
    cout << "Going to copy this code for future reference in " << outdir << endl;     
    system(Form("cp %s/src/CMGTools/WMass/python/plotter/utilityMacros/src/loopNtuplesSkeleton.C %s",cmssw_base.c_str(),outdir.c_str()));
  }  

}
