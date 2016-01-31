//////////////////////////////////////////////////////////
// This class has been automatically generated on
// Fri Jan 29 15:23:07 2016 by ROOT version 6.02/05
// from TChain tree/
//////////////////////////////////////////////////////////

#ifndef lepTnPFriendTreeMaker_h
#define lepTnPFriendTreeMaker_h

#include <iostream>

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>
#include <TLorentzVector.h>

// Header file for the classes stored in the TTree if any.

class lepTnPFriendTreeMaker {
public :
   TTree          *fChain;   //!pointer to the analyzed TTree or TChain
   Int_t           fCurrent; //!current Tree number in a TChain

// Fixed size dimensions of array or collections stored in the TTree if any.

   // Declaration of leaf types
   UInt_t          run;
   UInt_t          lumi;
   ULong64_t       evt;
   Int_t           isData;
   Float_t         rho;
   Float_t         rhoCN;
   Int_t           nVert;
   Float_t         met_pt;

   Float_t         mZ1;
   Float_t         mZ1SFSS;
   Float_t         minMllSFOS;
   Float_t         maxMllSFOS;
   Float_t         minMllAFOS;
   Float_t         maxMllAFOS;
   Float_t         minMllAFSS;
   Float_t         maxMllAFSS;
   Float_t         minMllAFAS;
   Float_t         maxMllAFAS;

   Int_t           nBJetLoose30;
   Int_t           nBJetMedium30;

   Float_t         HLT_DoubleElHT;
   Float_t         HLT_TripleEl;
   Float_t         HLT_SingleMu;
   Float_t         HLT_DoubleMuEl;
   Float_t         HLT_TripleMu;
   Float_t         HLT_DoubleElMu;
   Float_t         HLT_DoubleMuNoIso;
   Float_t         HLT_DoubleMuSS;
   Float_t         HLT_SingleEl;
   Float_t         HLT_TripleMuA;
   Float_t         HLT_MuEG;
   Float_t         HLT_DoubleMuHT;
   Float_t         HLT_DoubleEl;
   Float_t         HLT_DoubleMu;
   Float_t         Flag_HBHENoiseIsoFilter;
   Float_t         Flag_EcalDeadCellTriggerPrimitiveFilter;
   Float_t         Flag_trkPOG_manystripclus53X;
   Float_t         Flag_ecalLaserCorrFilter;
   Float_t         Flag_trkPOG_toomanystripclus53X;
   Float_t         Flag_hcalLaserEventFilter;
   Float_t         Flag_trkPOG_logErrorTooManyClusters;
   Float_t         Flag_trkPOGFilters;
   Float_t         Flag_trackingFailureFilter;
   Float_t         Flag_CSCTightHaloFilter;
   Float_t         Flag_HBHENoiseFilter;
   Float_t         Flag_goodVertices;
   Float_t         Flag_METFilters;
   Float_t         Flag_eeBadScFilter;

   Int_t           nLepGood;
   Float_t         LepGood_mvaIdPhys14[4];   //[nLepGood]
   Float_t         LepGood_mvaIdSpring15[4];   //[nLepGood]
   Float_t         LepGood_mvaTTH[4];   //[nLepGood]
   Float_t         LepGood_jetPtRatiov2[4];   //[nLepGood]
   Float_t         LepGood_jetPtRelv2[4];   //[nLepGood]
   Float_t         LepGood_jetBTagCSV[4];   //[nLepGood]
   Int_t           LepGood_tightId[4];   //[nLepGood]
   Float_t         LepGood_dxy[4];   //[nLepGood]
   Float_t         LepGood_dz[4];   //[nLepGood]
   Float_t         LepGood_ip3d[4];   //[nLepGood]
   Float_t         LepGood_sip3d[4];   //[nLepGood]
   Int_t           LepGood_convVeto[4];   //[nLepGood]
   Int_t           LepGood_lostHits[4];   //[nLepGood]
   Float_t         LepGood_relIso03[4];   //[nLepGood]
   Float_t         LepGood_relIso04[4];   //[nLepGood]
   Float_t         LepGood_miniRelIso[4];   //[nLepGood]
   Float_t         LepGood_relIsoAn04[4];   //[nLepGood]
   Int_t           LepGood_tightCharge[4];   //[nLepGood]
   Int_t           LepGood_mcMatchId[4];   //[nLepGood]
   Int_t           LepGood_mediumMuonId[4];   //[nLepGood]
   Int_t           LepGood_pdgId[4];   //[nLepGood]
   Float_t         LepGood_pt[4];   //[nLepGood]
   Float_t         LepGood_eta[4];   //[nLepGood]
   Float_t         LepGood_phi[4];   //[nLepGood]
   Float_t         LepGood_mass[4];   //[nLepGood]
   Float_t         LepGood_idEmu[4];   //[nLepGood]

   // List of branches
   TBranch *b_run;
   TBranch *b_lumi;
   TBranch *b_evt;
   TBranch *b_isData;
   TBranch *b_rho;
   TBranch *b_rhoCN;
   TBranch *b_nVert;
   TBranch *b_met_pt;

   TBranch *b_mZ1;
   TBranch *b_mZ1SFSS;
   TBranch *b_minMllSFOS;
   TBranch *b_maxMllSFOS;
   TBranch *b_minMllAFOS;
   TBranch *b_maxMllAFOS;
   TBranch *b_minMllAFSS;
   TBranch *b_maxMllAFSS;
   TBranch *b_minMllAFAS;
   TBranch *b_maxMllAFAS;
   TBranch *b_nBJetLoose30;
   TBranch *b_nBJetMedium30;
   TBranch *b_HLT_DoubleElHT;
   TBranch *b_HLT_TripleEl;
   TBranch *b_HLT_SingleMu;
   TBranch *b_HLT_DoubleMuEl;
   TBranch *b_HLT_TripleMu;
   TBranch *b_HLT_DoubleElMu;
   TBranch *b_HLT_DoubleMuNoIso;
   TBranch *b_HLT_DoubleMuSS;
   TBranch *b_HLT_SingleEl;
   TBranch *b_HLT_TripleMuA;
   TBranch *b_HLT_MuEG;
   TBranch *b_HLT_DoubleMuHT;
   TBranch *b_HLT_DoubleEl;
   TBranch *b_HLT_DoubleMu;
   TBranch *b_Flag_HBHENoiseIsoFilter;
   TBranch *b_Flag_EcalDeadCellTriggerPrimitiveFilter;
   TBranch *b_Flag_trkPOG_manystripclus53X;
   TBranch *b_Flag_ecalLaserCorrFilter;
   TBranch *b_Flag_trkPOG_toomanystripclus53X;
   TBranch *b_Flag_hcalLaserEventFilter;
   TBranch *b_Flag_trkPOG_logErrorTooManyClusters;
   TBranch *b_Flag_trkPOGFilters;
   TBranch *b_Flag_trackingFailureFilter;
   TBranch *b_Flag_CSCTightHaloFilter;
   TBranch *b_Flag_HBHENoiseFilter;
   TBranch *b_Flag_goodVertices;
   TBranch *b_Flag_METFilters;
   TBranch *b_Flag_eeBadScFilter;
   TBranch *b_nLepGood;
   TBranch *b_LepGood_mvaIdPhys14;
   TBranch *b_LepGood_mvaIdSpring15;
   TBranch *b_LepGood_mvaTTH;
   TBranch *b_LepGood_jetPtRatiov2;
   TBranch *b_LepGood_jetPtRelv2;
   TBranch *b_LepGood_jetBTagCSV;
   TBranch *b_LepGood_tightId;
   TBranch *b_LepGood_dxy;
   TBranch *b_LepGood_dz;
   TBranch *b_LepGood_ip3d;
   TBranch *b_LepGood_sip3d;
   TBranch *b_LepGood_convVeto;
   TBranch *b_LepGood_lostHits;
   TBranch *b_LepGood_relIso03;
   TBranch *b_LepGood_relIso04;
   TBranch *b_LepGood_miniRelIso;
   TBranch *b_LepGood_relIsoAn04;
   TBranch *b_LepGood_tightCharge;
   TBranch *b_LepGood_mcMatchId;
   TBranch *b_LepGood_mediumMuonId;
   TBranch *b_LepGood_pdgId;
   TBranch *b_LepGood_pt;
   TBranch *b_LepGood_eta;
   TBranch *b_LepGood_phi;
   TBranch *b_LepGood_mass;
   TBranch *b_LepGood_idEmu;

   lepTnPFriendTreeMaker(TTree *tree=0);
   virtual ~lepTnPFriendTreeMaker();
   virtual Int_t    GetEntry(Long64_t entry);
   virtual Long64_t LoadTree(Long64_t entry);
   virtual void     Init(TTree *tree);
   virtual void     Loop();
   virtual Bool_t   Notify();

   virtual void     RunJob(TString, bool);
   virtual void     Begin(TFile*);
   virtual void     End(TFile*);
   virtual void     ResetTnPTree();
   virtual bool     PassSingleTriggers();
   virtual bool     PassDoubleTriggers();
   virtual bool     SelectEvent();
   virtual int      PassTTBarSelection();
   virtual bool     SelectTagElectron(int);
   virtual bool     SelectTagMuon(int);

   virtual bool     PassLooseLepton(int);
   virtual bool     PassTightLepton(int);
   virtual bool     PassConvRejection(int);
   virtual bool     PassTightCharge(int);
   virtual float    ConePt(int);

   virtual int      SelectPair(int,int,float);


   bool fIsData;
   Long64_t fMaxEvents;
   virtual inline void setMaxEvents(int maxevents){fMaxEvents = maxevents;};

   TTree *fTnPTree;

   Int_t   fT_evSel;
   Int_t   fT_passSingle;
   Int_t   fT_passDouble;

   Float_t fT_mass;
   Int_t   fT_pair_probeMultiplicity;
   Int_t   fT_nVert;
   Int_t   fT_run;

   Float_t fT_pt;
   Float_t fT_phi;
   Int_t   fT_pdgId;
   Int_t   fT_passLoose;
   Int_t   fT_passConvRej;
   Int_t   fT_passTight;
   Int_t   fT_passTCharge;
   Float_t fT_conePt;
   Float_t fT_abseta;
   Float_t fT_dxy;
   Float_t fT_dz;
   Float_t fT_ip3d;
   Float_t fT_sip3d;
   Float_t fT_jetPtRelv2;
   Float_t fT_jetPtRatiov2;
   Float_t fT_jetBTagCSV;
   Float_t fT_miniRelIso;
   Float_t fT_relIso03;
   Float_t fT_relIsoAn04;
   Float_t fT_mvaTTH;
   Int_t   fT_tightId;
   Int_t   fT_convVeto;
   Int_t   fT_lostHits;
   Int_t   fT_tightCharge;
   Int_t   fT_mediumMuonId;
   Float_t fT_mvaIdPhys14;
   Float_t fT_mvaIdSpring15;
   Int_t   fT_mcMatchId;
   Float_t fT_idEmu;

   Float_t fT_tag_pt;
   Float_t fT_tag_eta;
   Int_t   fT_tag_pdgId;
   Float_t fT_tag_relIso03;
   Int_t   fT_tag_mcMatchId;
};

lepTnPFriendTreeMaker::lepTnPFriendTreeMaker(TTree *tree) : fChain(0){
   Init(tree);
   fTnPTree = 0;
   fMaxEvents = -1;
}

lepTnPFriendTreeMaker::~lepTnPFriendTreeMaker(){
   if (!fChain) return;
   delete fChain->GetCurrentFile();
}

Int_t lepTnPFriendTreeMaker::GetEntry(Long64_t entry){
   if (!fChain) return 0;
   return fChain->GetEntry(entry);
}

Long64_t lepTnPFriendTreeMaker::LoadTree(Long64_t entry){
// Set the environment to read one entry
   if (!fChain) return -5;
   Long64_t centry = fChain->LoadTree(entry);
   if (centry < 0) return centry;
   if (fChain->GetTreeNumber() != fCurrent) {
      fCurrent = fChain->GetTreeNumber();
      Notify();
   }
   return centry;
}

void lepTnPFriendTreeMaker::Init(TTree *tree){
   // Set branch addresses and branch pointers
   if (!tree) return;
   fChain = tree;
   fCurrent = -1;
   fChain->SetMakeClass(1);

   fChain->SetBranchAddress("run"                                     , &run                                     , &b_run);
   fChain->SetBranchAddress("lumi"                                    , &lumi                                    , &b_lumi);
   fChain->SetBranchAddress("evt"                                     , &evt                                     , &b_evt);
   fChain->SetBranchAddress("isData"                                  , &isData                                  , &b_isData);
   fChain->SetBranchAddress("rho"                                     , &rho                                     , &b_rho);
   fChain->SetBranchAddress("rhoCN"                                   , &rhoCN                                   , &b_rhoCN);
   fChain->SetBranchAddress("nVert"                                   , &nVert                                   , &b_nVert);
   fChain->SetBranchAddress("met_pt", &met_pt, &b_met_pt);
   fChain->SetBranchAddress("mZ1"                                     , &mZ1                                     , &b_mZ1);
   fChain->SetBranchAddress("mZ1SFSS"                                 , &mZ1SFSS                                 , &b_mZ1SFSS);
   fChain->SetBranchAddress("minMllSFOS"                              , &minMllSFOS                              , &b_minMllSFOS);
   fChain->SetBranchAddress("maxMllSFOS"                              , &maxMllSFOS                              , &b_maxMllSFOS);
   fChain->SetBranchAddress("minMllAFOS"                              , &minMllAFOS                              , &b_minMllAFOS);
   fChain->SetBranchAddress("maxMllAFOS"                              , &maxMllAFOS                              , &b_maxMllAFOS);
   fChain->SetBranchAddress("minMllAFSS"                              , &minMllAFSS                              , &b_minMllAFSS);
   fChain->SetBranchAddress("maxMllAFSS"                              , &maxMllAFSS                              , &b_maxMllAFSS);
   fChain->SetBranchAddress("minMllAFAS"                              , &minMllAFAS                              , &b_minMllAFAS);
   fChain->SetBranchAddress("maxMllAFAS"                              , &maxMllAFAS                              , &b_maxMllAFAS);
   fChain->SetBranchAddress("nBJetLoose30", &nBJetLoose30, &b_nBJetLoose30);
   fChain->SetBranchAddress("nBJetMedium30", &nBJetMedium30, &b_nBJetMedium30);
   fChain->SetBranchAddress("HLT_DoubleElHT"                          , &HLT_DoubleElHT                          , &b_HLT_DoubleElHT);
   fChain->SetBranchAddress("HLT_TripleEl"                            , &HLT_TripleEl                            , &b_HLT_TripleEl);
   fChain->SetBranchAddress("HLT_SingleMu"                            , &HLT_SingleMu                            , &b_HLT_SingleMu);
   fChain->SetBranchAddress("HLT_DoubleMuEl"                          , &HLT_DoubleMuEl                          , &b_HLT_DoubleMuEl);
   fChain->SetBranchAddress("HLT_TripleMu"                            , &HLT_TripleMu                            , &b_HLT_TripleMu);
   fChain->SetBranchAddress("HLT_DoubleElMu"                          , &HLT_DoubleElMu                          , &b_HLT_DoubleElMu);
   fChain->SetBranchAddress("HLT_DoubleMuNoIso"                       , &HLT_DoubleMuNoIso                       , &b_HLT_DoubleMuNoIso);
   fChain->SetBranchAddress("HLT_DoubleMuSS"                          , &HLT_DoubleMuSS                          , &b_HLT_DoubleMuSS);
   fChain->SetBranchAddress("HLT_SingleEl"                            , &HLT_SingleEl                            , &b_HLT_SingleEl);
   fChain->SetBranchAddress("HLT_TripleMuA"                           , &HLT_TripleMuA                           , &b_HLT_TripleMuA);
   fChain->SetBranchAddress("HLT_MuEG"                                , &HLT_MuEG                                , &b_HLT_MuEG);
   fChain->SetBranchAddress("HLT_DoubleMuHT"                          , &HLT_DoubleMuHT                          , &b_HLT_DoubleMuHT);
   fChain->SetBranchAddress("HLT_DoubleEl"                            , &HLT_DoubleEl                            , &b_HLT_DoubleEl);
   fChain->SetBranchAddress("HLT_DoubleMu"                            , &HLT_DoubleMu                            , &b_HLT_DoubleMu);
   fChain->SetBranchAddress("Flag_HBHENoiseIsoFilter"                 , &Flag_HBHENoiseIsoFilter                 , &b_Flag_HBHENoiseIsoFilter);
   fChain->SetBranchAddress("Flag_EcalDeadCellTriggerPrimitiveFilter" , &Flag_EcalDeadCellTriggerPrimitiveFilter , &b_Flag_EcalDeadCellTriggerPrimitiveFilter);
   fChain->SetBranchAddress("Flag_trkPOG_manystripclus53X"            , &Flag_trkPOG_manystripclus53X            , &b_Flag_trkPOG_manystripclus53X);
   fChain->SetBranchAddress("Flag_ecalLaserCorrFilter"                , &Flag_ecalLaserCorrFilter                , &b_Flag_ecalLaserCorrFilter);
   fChain->SetBranchAddress("Flag_trkPOG_toomanystripclus53X"         , &Flag_trkPOG_toomanystripclus53X         , &b_Flag_trkPOG_toomanystripclus53X);
   fChain->SetBranchAddress("Flag_hcalLaserEventFilter"               , &Flag_hcalLaserEventFilter               , &b_Flag_hcalLaserEventFilter);
   fChain->SetBranchAddress("Flag_trkPOG_logErrorTooManyClusters"     , &Flag_trkPOG_logErrorTooManyClusters     , &b_Flag_trkPOG_logErrorTooManyClusters);
   fChain->SetBranchAddress("Flag_trkPOGFilters"                      , &Flag_trkPOGFilters                      , &b_Flag_trkPOGFilters);
   fChain->SetBranchAddress("Flag_trackingFailureFilter"              , &Flag_trackingFailureFilter              , &b_Flag_trackingFailureFilter);
   fChain->SetBranchAddress("Flag_CSCTightHaloFilter"                 , &Flag_CSCTightHaloFilter                 , &b_Flag_CSCTightHaloFilter);
   fChain->SetBranchAddress("Flag_HBHENoiseFilter"                    , &Flag_HBHENoiseFilter                    , &b_Flag_HBHENoiseFilter);
   fChain->SetBranchAddress("Flag_goodVertices"                       , &Flag_goodVertices                       , &b_Flag_goodVertices);
   fChain->SetBranchAddress("Flag_METFilters"                         , &Flag_METFilters                         , &b_Flag_METFilters);
   fChain->SetBranchAddress("Flag_eeBadScFilter"                      , &Flag_eeBadScFilter                      , &b_Flag_eeBadScFilter);
   fChain->SetBranchAddress("nLepGood"                     , &nLepGood                    , &b_nLepGood);
   fChain->SetBranchAddress("LepGood_mvaIdPhys14"          , LepGood_mvaIdPhys14          , &b_LepGood_mvaIdPhys14);
   fChain->SetBranchAddress("LepGood_mvaIdSpring15"        , LepGood_mvaIdSpring15        , &b_LepGood_mvaIdSpring15);
   fChain->SetBranchAddress("LepGood_mvaTTH"               , LepGood_mvaTTH               , &b_LepGood_mvaTTH);
   fChain->SetBranchAddress("LepGood_jetPtRatiov2"         , LepGood_jetPtRatiov2         , &b_LepGood_jetPtRatiov2);
   fChain->SetBranchAddress("LepGood_jetPtRelv2"           , LepGood_jetPtRelv2           , &b_LepGood_jetPtRelv2);
   fChain->SetBranchAddress("LepGood_jetBTagCSV"           , LepGood_jetBTagCSV           , &b_LepGood_jetBTagCSV);
   fChain->SetBranchAddress("LepGood_tightId"              , LepGood_tightId              , &b_LepGood_tightId);
   fChain->SetBranchAddress("LepGood_dxy"                  , LepGood_dxy                  , &b_LepGood_dxy);
   fChain->SetBranchAddress("LepGood_dz"                   , LepGood_dz                   , &b_LepGood_dz);
   fChain->SetBranchAddress("LepGood_ip3d"                 , LepGood_ip3d                 , &b_LepGood_ip3d);
   fChain->SetBranchAddress("LepGood_sip3d"                , LepGood_sip3d                , &b_LepGood_sip3d);
   fChain->SetBranchAddress("LepGood_convVeto"             , LepGood_convVeto             , &b_LepGood_convVeto);
   fChain->SetBranchAddress("LepGood_lostHits"             , LepGood_lostHits             , &b_LepGood_lostHits);
   fChain->SetBranchAddress("LepGood_relIso03"             , LepGood_relIso03             , &b_LepGood_relIso03);
   fChain->SetBranchAddress("LepGood_relIso04"             , LepGood_relIso04             , &b_LepGood_relIso04);
   fChain->SetBranchAddress("LepGood_miniRelIso"           , LepGood_miniRelIso           , &b_LepGood_miniRelIso);
   fChain->SetBranchAddress("LepGood_relIsoAn04"           , LepGood_relIsoAn04           , &b_LepGood_relIsoAn04);
   fChain->SetBranchAddress("LepGood_tightCharge"          , LepGood_tightCharge          , &b_LepGood_tightCharge);
   fChain->SetBranchAddress("LepGood_mcMatchId"            , LepGood_mcMatchId            , &b_LepGood_mcMatchId);
   fChain->SetBranchAddress("LepGood_mediumMuonId"         , LepGood_mediumMuonId         , &b_LepGood_mediumMuonId);
   fChain->SetBranchAddress("LepGood_pdgId"                , LepGood_pdgId                , &b_LepGood_pdgId);
   fChain->SetBranchAddress("LepGood_pt"                   , LepGood_pt                   , &b_LepGood_pt);
   fChain->SetBranchAddress("LepGood_eta"                  , LepGood_eta                  , &b_LepGood_eta);
   fChain->SetBranchAddress("LepGood_phi"                  , LepGood_phi                  , &b_LepGood_phi);
   fChain->SetBranchAddress("LepGood_mass"                 , LepGood_mass                 , &b_LepGood_mass);
   fChain->SetBranchAddress("LepGood_idEmu"                , LepGood_idEmu,  &b_LepGood_idEmu);

   Notify();
}

Bool_t lepTnPFriendTreeMaker::Notify(){
   return kTRUE;
}

void lepTnPFriendTreeMaker::RunJob(TString filename, bool isData){
   fIsData = isData;

   TFile *file = TFile::Open(filename, "recreate");
   //do the analysis
   Begin(file);
   Loop();
   End(file);
}

void lepTnPFriendTreeMaker::Begin(TFile *file){
   file->cd();
   fTnPTree = new TTree("fitter_tree", "TagnProbeTree");

   fTnPTree->Branch("evSel"                  ,&fT_evSel                  ,"evSel/I");
   fTnPTree->Branch("passSingle"             ,&fT_passSingle             ,"passSingle/I");
   fTnPTree->Branch("passDouble"             ,&fT_passDouble             ,"passDouble/I");
   fTnPTree->Branch("mass"                   ,&fT_mass                   ,"mass/F");
   fTnPTree->Branch("pair_probeMultiplicity" ,&fT_pair_probeMultiplicity ,"pair_probeMultiplicity/I");
   fTnPTree->Branch("nVert"                  ,&fT_nVert                  ,"nVert/I");
   fTnPTree->Branch("run"                    ,&fT_run                    ,"run/I");

   fTnPTree->Branch("pt"            ,&fT_pt            ,"pt/F");
   fTnPTree->Branch("abseta"        ,&fT_abseta        ,"abseta/F");
   fTnPTree->Branch("phi"           ,&fT_phi           ,"phi/F");
   fTnPTree->Branch("pdgId"         ,&fT_pdgId         ,"pdgId/I");
   fTnPTree->Branch("passLoose"     ,&fT_passLoose     ,"passLoose/I");
   fTnPTree->Branch("passConvRej"   ,&fT_passConvRej   ,"passConvRej/I");
   fTnPTree->Branch("passTight"     ,&fT_passTight     ,"passTight/I");
   fTnPTree->Branch("passTCharge"   ,&fT_passTCharge   ,"passTCharge/I");
   fTnPTree->Branch("conePt"        ,&fT_conePt        ,"conePt/F");
   fTnPTree->Branch("dxy"           ,&fT_dxy           ,"dxy/F");
   fTnPTree->Branch("dz"            ,&fT_dz            ,"dz/F");
   fTnPTree->Branch("ip3d"          ,&fT_ip3d          ,"ip3d/F");
   fTnPTree->Branch("sip3d"         ,&fT_sip3d         ,"sip3d/F");
   fTnPTree->Branch("jetPtRelv2"    ,&fT_jetPtRelv2    ,"jetPtRelv2/F");
   fTnPTree->Branch("jetPtRatiov2"  ,&fT_jetPtRatiov2  ,"jetPtRatiov2/F");
   fTnPTree->Branch("jetBTagCSV"    ,&fT_jetBTagCSV    ,"jetBTagCSV/F");
   fTnPTree->Branch("miniRelIso"    ,&fT_miniRelIso    ,"miniRelIso/F");
   fTnPTree->Branch("relIso03"      ,&fT_relIso03      ,"relIso03/F");
   fTnPTree->Branch("relIsoAn04"    ,&fT_relIsoAn04    ,"relIsoAn04/F");
   fTnPTree->Branch("mvaTTH"        ,&fT_mvaTTH        ,"mvaTTH/F");
   fTnPTree->Branch("tightId"       ,&fT_tightId       ,"tightId/I");
   fTnPTree->Branch("convVeto"      ,&fT_convVeto      ,"convVeto/I");
   fTnPTree->Branch("lostHits"      ,&fT_lostHits      ,"lostHits/I");
   fTnPTree->Branch("tightCharge"   ,&fT_tightCharge   ,"tightCharge/I");
   fTnPTree->Branch("mediumMuonId"  ,&fT_mediumMuonId  ,"mediumMuonId/I");
   fTnPTree->Branch("mvaIdPhys14"   ,&fT_mvaIdPhys14   ,"mvaIdPhys14/F");
   fTnPTree->Branch("mvaIdSpring15" ,&fT_mvaIdSpring15 ,"mvaIdSpring15/F");
   fTnPTree->Branch("mcMatchId"     ,&fT_mcMatchId     ,"mcMatchId/I");
   fTnPTree->Branch("idEmu"         ,&fT_idEmu         ,"idEmu/F");
   fTnPTree->Branch("tag_pt"        ,&fT_tag_pt        ,"tag_pt/F");
   fTnPTree->Branch("tag_eta"       ,&fT_tag_eta       ,"tag_eta/F");
   fTnPTree->Branch("tag_pdgId"     ,&fT_tag_pdgId     ,"tag_pdgId/I");
   fTnPTree->Branch("tag_relIso03"  ,&fT_tag_relIso03  ,"tag_relIso03/F");
   fTnPTree->Branch("tag_mcMatchId" ,&fT_tag_mcMatchId ,"tag_mcMatchId/I");

}

void lepTnPFriendTreeMaker::End(TFile *file){
   file->cd();
   fTnPTree->Write(fTnPTree->GetName());
   file->Write();
   file->Close();
}

void lepTnPFriendTreeMaker::ResetTnPTree(){
   fT_evSel                  = -1;
   fT_passSingle             = -1;
   fT_passDouble             = -1;
   fT_run                    = run;
   fT_nVert                  = nVert;
   fT_pair_probeMultiplicity = 0;
   fT_mass                   = -999.99;

   fT_pt            = -999.99;
   fT_phi           = -999.99;
   fT_pdgId         = -999;
   fT_passLoose     = -999;
   fT_passConvRej   = -999;
   fT_passTight     = -999;
   fT_passTCharge   = -999;
   fT_conePt        = -999.99;
   fT_abseta        = -999.99;
   fT_dxy           = -999.99;
   fT_dz            = -999.99;
   fT_ip3d          = -999.99;
   fT_sip3d         = -999.99;
   fT_jetPtRelv2    = -999.99;
   fT_jetPtRatiov2  = -999.99;
   fT_jetBTagCSV    = -999.99;
   fT_miniRelIso    = -999.99;
   fT_relIso03      = -999.99;
   fT_relIsoAn04    = -999.99;
   fT_mvaTTH        = -999.99;
   fT_tightId       = -999;
   fT_convVeto      = -999;
   fT_lostHits      = -999;
   fT_tightCharge   = -999;
   fT_mediumMuonId  = -999;
   fT_mvaIdPhys14   = -999.99;
   fT_mvaIdSpring15 = -999.99;
   fT_idEmu         = -999.99;
   fT_mcMatchId     = -999;
   fT_tag_pt        = -999.99;
   fT_tag_eta       = -999.99;
   fT_tag_pdgId     = -999;
   fT_tag_relIso03  = -999.99;
   fT_tag_mcMatchId = -999;
}

bool lepTnPFriendTreeMaker::PassSingleTriggers(){
   return (HLT_SingleMu || HLT_SingleEl);
}

bool lepTnPFriendTreeMaker::PassDoubleTriggers(){
   return ( HLT_DoubleElHT || HLT_TripleEl || HLT_DoubleMuEl ||
            HLT_TripleMu || HLT_DoubleElMu || HLT_DoubleMuNoIso ||
            HLT_DoubleMuSS || HLT_TripleMuA || HLT_MuEG || HLT_DoubleMuHT ||
            HLT_DoubleEl || HLT_DoubleMu );
}

bool lepTnPFriendTreeMaker::SelectEvent(){
   if( nLepGood < 2 ) return false;

   // Force e or mu (no taus)
   if( abs(LepGood_pdgId[0]) != 13 && abs(LepGood_pdgId[0]) != 11)
      return false;
   if( abs(LepGood_pdgId[1]) != 13 && abs(LepGood_pdgId[1]) != 11)
      return false;

   // DY selection
   if( !PassDoubleTriggers() && !PassSingleTriggers() ) return false;

   return true;
}

int lepTnPFriendTreeMaker::PassTTBarSelection(){
   if( !SelectEvent() ) return 0;
   if( nLepGood > 2 )      return 0;

   int evChan = LepGood_pdgId[0]*LepGood_pdgId[1];
   if( nBJetMedium30>0 && nBJetLoose30>1 ){
      // emu
      if( evChan == -143 ) return 1;

      // ee/mumu + met > 30:
      if( evChan == -121 || evChan == -169 ){
         if( met_pt > 30. ) return 2;
      }
   }
   return 0;
}

bool lepTnPFriendTreeMaker::SelectTagMuon(int i){
   if (LepGood_pt[i] < 25.) return false;
   if (fabs(LepGood_eta[i]) > 2.1) return false;
   if (LepGood_relIso03[i] > 0.2) return false;
   return true;
}

bool lepTnPFriendTreeMaker::SelectTagElectron(int i){
   if (LepGood_pt[i] < 25.) return false;
   if (fabs(LepGood_eta[i]) > 2.1) return false;
   if (LepGood_relIso03[i] > 0.2) return false;
   return true;
}

float lepTnPFriendTreeMaker::ConePt(int i){
   // =pt lep if tight, 0.85*pt lep-jet if loose)
   float conept = 0.85 * LepGood_pt[i] / LepGood_jetPtRatiov2[i];

   if( abs(LepGood_pdgId[i]) == 13 && !(LepGood_mediumMuonId[i]>0) )
      return conept;

   if( LepGood_mvaTTH[i] < 0.60 ) return conept;
   return LepGood_pt[i];
}

bool lepTnPFriendTreeMaker::PassLooseLepton(int i){
   if(LepGood_sip3d[i] > 8)         return false;
   if(ConePt(i) < 10.)              return false;

   // Electron specific
   if (abs(LepGood_pdgId[i]) == 11){
      if(ConePt(i) > 30. && LepGood_idEmu[i] < 1) return false;
      return true;
   }

   // Muon specific
   if (abs(LepGood_pdgId[i]) == 13){
      if(!(LepGood_mediumMuonId[i]>0)) return false;
      return true;
   }
   return false;
}

bool lepTnPFriendTreeMaker::PassConvRejection(int i){
   if( abs(LepGood_pdgId[i]) == 13) return true;
   if(!(LepGood_convVeto[i] > 0))   return false;
   if(!(LepGood_lostHits[i] == 0))  return false;
   return true;
}

bool lepTnPFriendTreeMaker::PassTightCharge(int i){
   if( LepGood_tightCharge[i] >= 2 ) return true;
   if( LepGood_tightCharge[i] >= 1 && abs(LepGood_pdgId[i])==13 ) return true;
   return false;
}

bool lepTnPFriendTreeMaker::PassTightLepton(int i){
   if( !PassLooseLepton(i) ) return false;
   if( LepGood_mvaTTH[i] < 0.60 ) return false;
   if( LepGood_jetBTagCSV[i] > 0.89 ) return false;
   if( LepGood_jetPtRatiov2[i] < 0.3 ) return false;

   // Tight electrons
   if (abs(LepGood_pdgId[i]) == 11){
      if(!PassConvRejection(i)) return false;
      return true;
   }

   // Tight muons
   if (abs(LepGood_pdgId[i]) == 13){
      return true;
   }
   return false;
}

int lepTnPFriendTreeMaker::SelectPair(int lep1, int lep2, float mass){
   int chan = LepGood_pdgId[lep1]*LepGood_pdgId[lep2];
   int ttbarsel = PassTTBarSelection();

   // Same flavor, opposite sign (DY selection)
   if( chan == -11*11 || chan == -13*13){
      if( mass > 60. && mass < 120. ) return 1;
   }

   // Same flavor, opposite sign (ttbar selection)
   if( (chan == -11*11 || chan == -13*13) && ttbarsel == 2 ){
      if( mass < 80. || mass > 100. ) return 2;
   }

   // Opposite flavor, opposite sign (ttbar selection)
   if( chan == -13*11 && ttbarsel == 1 ) return 3;

   return 0;
}

void lepTnPFriendTreeMaker::Loop(){
   if (fChain == 0) return;
   if (fTnPTree == 0) {
      std::cout << "Please call Begin() method first" << std::endl;
      return;
   }

   Long64_t nentries = fChain->GetEntriesFast();
   if( fMaxEvents > 0 ){
      printf(" Processing only %lld of %lld entries\n", fMaxEvents, nentries);
      nentries = min(fMaxEvents, nentries);
   }

   Long64_t nbytes = 0, nb = 0;
   for (Long64_t jentry=0; jentry<nentries;jentry++) {
      Long64_t ientry = LoadTree(jentry);
      if (ientry < 0) break;
      nb = fChain->GetEntry(jentry);   nbytes += nb;

      // Print progress
      if (jentry%500 == 0) {
         printf("\r [ %3d/100 ]", int(100*float(jentry)/float(nentries)));
         std::cout << std::flush;
      }

      if(!SelectEvent()) continue;
      ResetTnPTree();

      fT_passSingle = PassSingleTriggers();
      fT_passDouble = PassDoubleTriggers();

      // Find a tag lepton
      for (int lep1 = 0; lep1 < nLepGood; ++lep1){
         if (  (abs(LepGood_pdgId[lep1])==11 && SelectTagElectron(lep1))
            || (abs(LepGood_pdgId[lep1])==13 && SelectTagMuon(lep1)) ) {

            // Find a probe lepton
            for (int lep2 = lep1+1; lep2 < nLepGood; ++lep2){
               TLorentzVector p_lep1, p_lep2;
               p_lep1.SetPtEtaPhiM(LepGood_pt[lep1],
                                   LepGood_eta[lep1],
                                   LepGood_phi[lep1], 0.);
               p_lep2.SetPtEtaPhiM(LepGood_pt[lep2],
                                   LepGood_eta[lep2],
                                   LepGood_phi[lep2], 0.);
               float mass = (p_lep1+p_lep2).M();

               // Select pair
               int pairsel = SelectPair(lep1, lep2, mass);
               if( pairsel == 0 ) continue;

               // Found a pair!
               fT_evSel = pairsel; // 1 for DY, 2 for SF ttbar, 3 for OF ttbar
               fT_pair_probeMultiplicity++;
               fT_mass          = mass;

               // Save probe properties
               fT_pt            = LepGood_pt[lep2];
               fT_phi           = LepGood_phi[lep2];
               fT_abseta        = fabs(LepGood_eta[lep2]);
               fT_pdgId         = LepGood_pdgId[lep2];
               fT_passLoose     = PassLooseLepton(lep2);
               fT_passConvRej   = PassConvRejection(lep2);
               fT_passTight     = PassTightLepton(lep2);
               fT_passTCharge   = PassTightCharge(lep2);
               fT_conePt        = ConePt(lep2);
               fT_dxy           = LepGood_dxy[lep2];
               fT_dz            = LepGood_dz[lep2];
               fT_ip3d          = LepGood_ip3d[lep2];
               fT_sip3d         = LepGood_sip3d[lep2];
               fT_jetPtRelv2    = LepGood_jetPtRelv2[lep2];
               fT_jetPtRatiov2  = LepGood_jetPtRatiov2[lep2];
               fT_jetBTagCSV    = LepGood_jetBTagCSV[lep2];
               fT_miniRelIso    = LepGood_miniRelIso[lep2];
               fT_relIso03      = LepGood_relIso03[lep2];
               fT_relIsoAn04    = LepGood_relIsoAn04[lep2];
               fT_mvaTTH        = LepGood_mvaTTH[lep2];
               fT_tightId       = LepGood_tightId[lep2];
               fT_convVeto      = LepGood_convVeto[lep2];
               fT_lostHits      = LepGood_lostHits[lep2];
               fT_tightCharge   = LepGood_tightCharge[lep2];
               fT_mediumMuonId  = LepGood_mediumMuonId[lep2];
               fT_mvaIdPhys14   = LepGood_mvaIdPhys14[lep2];
               fT_mvaIdSpring15 = LepGood_mvaIdSpring15[lep2];
               fT_idEmu         = LepGood_idEmu[lep2];
               if( !fIsData ) fT_mcMatchId = LepGood_mcMatchId[lep2];

               // Save tag properties
               fT_tag_pt        = LepGood_pt[lep1];
               fT_tag_eta       = LepGood_eta[lep1];
               fT_tag_pdgId     = LepGood_pdgId[lep1];
               fT_tag_relIso03  = LepGood_relIso03[lep1];
               if( !fIsData ) fT_tag_mcMatchId = LepGood_mcMatchId[lep1];

               fTnPTree->Fill();
            }
         }
      } // end lepton loop 1
   } // end event loop
   std::cout << "\r [   done  ]" << std::endl;
}

#endif // #ifdef lepTnPFriendTreeMaker_cxx
