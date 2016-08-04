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
#include <TH1I.h>

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
   Float_t         nTrueInt;
   Float_t         met_pt;
   Float_t         puWeight;

   Int_t           nJet25;
   Int_t           nBJetLoose25;
   Int_t           nBJetMedium25;

   Int_t           HLT_DoubleElHT;
   Int_t           HLT_TripleEl;
   Int_t           HLT_SingleMu;
   Int_t           HLT_DoubleMuEl;
   Int_t           HLT_TripleMu;
   Int_t           HLT_DoubleElMu;
   Int_t           HLT_DoubleMuNoIso;
   Int_t           HLT_DoubleMuSS;
   Int_t           HLT_SingleEl;
   Int_t           HLT_TripleMuA;
   Int_t           HLT_MuEG;
   Int_t           HLT_DoubleMuHT;
   Int_t           HLT_DoubleEl;
   Int_t           HLT_DoubleMu;

   Int_t           nLepGood;
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
   Float_t         LepGood_innerTrackValidHitFraction[4];   //[nLepGood]
   Float_t         LepGood_segmentCompatibility[4];   //[nLepGood]
   Float_t         LepGood_globalTrackChi2[4];   //[nLepGood]
   Float_t         LepGood_chi2LocalPosition[4];   //[nLepGood]
   Float_t         LepGood_trkKink[4];   //[nLepGood]
   Int_t           LepGood_isGlobalMuon[4];   //[nLepGood]
   Int_t           LepGood_pdgId[4];   //[nLepGood]
   Float_t         LepGood_pt[4];   //[nLepGood]
   Float_t         LepGood_eta[4];   //[nLepGood]
   Float_t         LepGood_phi[4];   //[nLepGood]
   Float_t         LepGood_mass[4];   //[nLepGood]

   Float_t         LepGood_hadronicOverEm[4];   //[nLepGood]
   Float_t         LepGood_dEtaScTrkIn[4];   //[nLepGood]
   Float_t         LepGood_dPhiScTrkIn[4];   //[nLepGood]
   Float_t         LepGood_etaSc[4];   //[nLepGood]
   Float_t         LepGood_eInvMinusPInv[4]; //[nLepGood]
   Float_t         LepGood_sigmaIEtaIEta[4]; //[nLepGood]

   // List of branches
   TBranch *b_run;
   TBranch *b_lumi;
   TBranch *b_evt;
   TBranch *b_isData;
   TBranch *b_rho;
   TBranch *b_rhoCN;
   TBranch *b_nVert;
   TBranch *b_nTrueInt;
   TBranch *b_met_pt;
   TBranch *b_puWeight;

   TBranch *b_nJet25;
   TBranch *b_nBJetLoose25;
   TBranch *b_nBJetMedium25;
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
   TBranch *b_nLepGood;
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
   TBranch *b_LepGood_innerTrackValidHitFraction;
   TBranch *b_LepGood_segmentCompatibility;
   TBranch *b_LepGood_globalTrackChi2;
   TBranch *b_LepGood_chi2LocalPosition;
   TBranch *b_LepGood_trkKink;
   TBranch *b_LepGood_isGlobalMuon;
   TBranch *b_LepGood_pdgId;
   TBranch *b_LepGood_pt;
   TBranch *b_LepGood_eta;
   TBranch *b_LepGood_phi;
   TBranch *b_LepGood_mass;
   TBranch *b_LepGood_hadronicOverEm;
   TBranch *b_LepGood_dEtaScTrkIn;
   TBranch *b_LepGood_dPhiScTrkIn;
   TBranch *b_LepGood_etaSc;
   TBranch *b_LepGood_eInvMinusPInv;
   TBranch *b_LepGood_sigmaIEtaIEta;



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
   virtual bool     PassICHEPMediumMuonID(int);
   virtual float    ConePt(int);
   virtual float    PuWeight();

   virtual bool     _ttH_idEmu_cuts_E2(int);

   virtual int      SelectPair(int,int,float);


   bool fIsData;
   Long64_t fMaxEvents;
   virtual inline void setMaxEvents(int maxevents){fMaxEvents = maxevents;};

   Float_t fPUw2016_vtx_13fb[60] = { 1.0,
                                   0.046904649804193066,
                                   0.09278031810949669,
                                   0.18880389403907694,
                                   0.3514757265099305,
                                   0.557758357976481,
                                   0.7693577917575528,
                                   0.9666548740765918,
                                   1.145319485841941,
                                   1.2648398335691222,
                                   1.3414360633779425,
                                   1.3679594451533137,
                                   1.362759399034107,
                                   1.327376308549365,
                                   1.2613315166803767,
                                   1.196440614259811,
                                   1.1139701579261285,
                                   1.029953473266092,
                                   0.9499371225384508,
                                   0.8650456207995321,
                                   0.7851579627730857,
                                   0.7104602883630896,
                                   0.6454503663312138,
                                   0.5827160708961265,
                                   0.527376483837914,
                                   0.4700331217669938,
                                   0.4271753119677936,
                                   0.3869926520067443,
                                   0.35986269245880403,
                                   0.3280226115374019,
                                   0.2995626735821264,
                                   0.29695297220375283,
                                   0.2904602474734967,
                                   0.27797348557821827,
                                   0.27285575884404983,
                                   0.2696769830193652,
                                   0.2834280746705423,
                                   0.3079991295527812,
                                   0.2958183730167929,
                                   0.3281547943587132,
                                   0.34428579006474574,
                                   0.34709355767303973,
                                   0.5916367460335905,
                                   0.4991935044658422,
                                   0.2689257936516321,
                                   1.0,
                                   0.690242870372522,
                                   2.0707286111175662,
                                   0.2958183730167952,
                                   0.8874551190503855,
                                   1.0,
                                   1.0,
                                   1.0,
                                   1.0,
                                   1.0,
                                   1.0,
                                   1.0,
                                   0.0,
                                   1.0,
                                   1.0};

   TH1I *fHCutFlow;

   TTree *fTnPTree;

   Int_t   fT_evSel;
   Int_t   fT_passSingle;
   Int_t   fT_passDouble;

   Float_t fT_mass;
   Int_t   fT_pair_probeMultiplicity;
   Int_t   fT_nVert;
   Int_t   fT_run;
   Int_t   fT_isdata;

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
   Int_t   fT_ICHEPmediumMuonId;
   Float_t fT_mvaIdPhys14;
   Float_t fT_mvaIdSpring15;
   Int_t   fT_mcMatchId;
   Float_t fT_idEmu;
   Int_t   fT_nJet25;
   Int_t   fT_nBJetLoose25;
   Int_t   fT_nBJetMedium25;
   Float_t fT_met_pt;
   Float_t fT_puWeight;

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
   fHCutFlow = new TH1I("CutFlow", "CutFlow", 12, 0, 12);
   fHCutFlow->GetXaxis()->SetBinLabel(1, "All events");
   fHCutFlow->GetXaxis()->SetBinLabel(2, "Two loose leptons");
   fHCutFlow->GetXaxis()->SetBinLabel(3, "ee, e#mu, #mu#mu channels");
   fHCutFlow->GetXaxis()->SetBinLabel(4, "Pass triggers");
   fHCutFlow->GetXaxis()->SetBinLabel(5, "Found a tag electron");
   fHCutFlow->GetXaxis()->SetBinLabel(6, "Found a probe electron");
   fHCutFlow->GetXaxis()->SetBinLabel(7, "Probe electron passes loose");
   fHCutFlow->GetXaxis()->SetBinLabel(8, "Probe electron passes tight");
   fHCutFlow->GetXaxis()->SetBinLabel(9, "Found a tag muon");
   fHCutFlow->GetXaxis()->SetBinLabel(10, "Found a probe muon");
   fHCutFlow->GetXaxis()->SetBinLabel(11, "Probe muon passes loose");
   fHCutFlow->GetXaxis()->SetBinLabel(12, "Probe muon passes tight");
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

   fChain->SetBranchStatus("*", 0);

   fChain->SetBranchStatus("run"                    , 1);
   fChain->SetBranchStatus("lumi"                   , 1);
   fChain->SetBranchStatus("evt"                    , 1);
   fChain->SetBranchStatus("isData"                 , 1);
   fChain->SetBranchStatus("rho"                    , 1);
   fChain->SetBranchStatus("rhoCN"                  , 1);
   fChain->SetBranchStatus("nVert"                  , 1);
   fChain->SetBranchStatus("nTrueInt"               , 1);
   fChain->SetBranchStatus("met_pt"                 , 1);
   fChain->SetBranchStatus("puWeight"               , 1);
   fChain->SetBranchStatus("nJet25"                 , 1);
   fChain->SetBranchStatus("nBJetLoose25"           , 1);
   fChain->SetBranchStatus("nBJetMedium25"          , 1);
   fChain->SetBranchStatus("HLT_DoubleElHT"         , 1);
   fChain->SetBranchStatus("HLT_TripleEl"           , 1);
   fChain->SetBranchStatus("HLT_SingleMu"           , 1);
   fChain->SetBranchStatus("HLT_DoubleMuEl"         , 1);
   fChain->SetBranchStatus("HLT_TripleMu"           , 1);
   fChain->SetBranchStatus("HLT_DoubleElMu"         , 1);
   fChain->SetBranchStatus("HLT_DoubleMuNoIso"      , 1);
   fChain->SetBranchStatus("HLT_DoubleMuSS"         , 1);
   fChain->SetBranchStatus("HLT_SingleEl"           , 1);
   fChain->SetBranchStatus("HLT_TripleMuA"          , 1);
   fChain->SetBranchStatus("HLT_MuEG"               , 1);
   fChain->SetBranchStatus("HLT_DoubleMuHT"         , 1);
   fChain->SetBranchStatus("HLT_DoubleEl"           , 1);
   fChain->SetBranchStatus("HLT_DoubleMu"           , 1);
   fChain->SetBranchStatus("nLepGood"               , 1);
   fChain->SetBranchStatus("LepGood_mvaIdSpring15"  , 1);
   fChain->SetBranchStatus("LepGood_mvaTTH"         , 1);
   fChain->SetBranchStatus("LepGood_jetPtRatiov2"   , 1);
   fChain->SetBranchStatus("LepGood_jetPtRelv2"     , 1);
   fChain->SetBranchStatus("LepGood_jetBTagCSV"     , 1);
   fChain->SetBranchStatus("LepGood_tightId"        , 1);
   fChain->SetBranchStatus("LepGood_dxy"            , 1);
   fChain->SetBranchStatus("LepGood_dz"             , 1);
   fChain->SetBranchStatus("LepGood_ip3d"           , 1);
   fChain->SetBranchStatus("LepGood_sip3d"          , 1);
   fChain->SetBranchStatus("LepGood_convVeto"       , 1);
   fChain->SetBranchStatus("LepGood_lostHits"       , 1);
   fChain->SetBranchStatus("LepGood_relIso03"       , 1);
   fChain->SetBranchStatus("LepGood_relIso04"       , 1);
   fChain->SetBranchStatus("LepGood_miniRelIso"     , 1);
   fChain->SetBranchStatus("LepGood_relIsoAn04"     , 1);
   fChain->SetBranchStatus("LepGood_tightCharge"    , 1);
   fChain->SetBranchStatus("LepGood_mcMatchId"      , 1);
   fChain->SetBranchStatus("LepGood_mediumMuonId"   , 1);
   fChain->SetBranchStatus("LepGood_innerTrackValidHitFraction" , 1);
   fChain->SetBranchStatus("LepGood_segmentCompatibility"       , 1);
   fChain->SetBranchStatus("LepGood_globalTrackChi2"            , 1);
   fChain->SetBranchStatus("LepGood_chi2LocalPosition"          , 1);
   fChain->SetBranchStatus("LepGood_trkKink"                    , 1);
   fChain->SetBranchStatus("LepGood_isGlobalMuon"   , 1);
   fChain->SetBranchStatus("LepGood_pdgId"          , 1);
   fChain->SetBranchStatus("LepGood_pt"             , 1);
   fChain->SetBranchStatus("LepGood_eta"            , 1);
   fChain->SetBranchStatus("LepGood_phi"            , 1);
   fChain->SetBranchStatus("LepGood_mass"           , 1);
   fChain->SetBranchStatus("LepGood_hadronicOverEm" , 1);
   fChain->SetBranchStatus("LepGood_dEtaScTrkIn"    , 1);
   fChain->SetBranchStatus("LepGood_dPhiScTrkIn"    , 1);
   fChain->SetBranchStatus("LepGood_etaSc"          , 1);
   fChain->SetBranchStatus("LepGood_eInvMinusPInv"  , 1);
   fChain->SetBranchStatus("LepGood_sigmaIEtaIEta"  , 1);

   fChain->SetBranchAddress("run"                    , &run                   , &b_run);
   fChain->SetBranchAddress("lumi"                   , &lumi                  , &b_lumi);
   fChain->SetBranchAddress("evt"                    , &evt                   , &b_evt);
   fChain->SetBranchAddress("isData"                 , &isData                , &b_isData);
   fChain->SetBranchAddress("rho"                    , &rho                   , &b_rho);
   fChain->SetBranchAddress("rhoCN"                  , &rhoCN                 , &b_rhoCN);
   fChain->SetBranchAddress("nVert"                  , &nVert                 , &b_nVert);
   fChain->SetBranchAddress("nTrueInt"               , &nTrueInt              , &b_nTrueInt);
   fChain->SetBranchAddress("met_pt"                 , &met_pt                , &b_met_pt);
   fChain->SetBranchAddress("puWeight"               , &puWeight              , &b_puWeight);
   fChain->SetBranchAddress("nJet25"                 , &nJet25                , &b_nJet25);
   fChain->SetBranchAddress("nBJetLoose25"           , &nBJetLoose25          , &b_nBJetLoose25);
   fChain->SetBranchAddress("nBJetMedium25"          , &nBJetMedium25         , &b_nBJetMedium25);
   fChain->SetBranchAddress("HLT_DoubleElHT"         , &HLT_DoubleElHT        , &b_HLT_DoubleElHT);
   fChain->SetBranchAddress("HLT_TripleEl"           , &HLT_TripleEl          , &b_HLT_TripleEl);
   fChain->SetBranchAddress("HLT_SingleMu"           , &HLT_SingleMu          , &b_HLT_SingleMu);
   fChain->SetBranchAddress("HLT_DoubleMuEl"         , &HLT_DoubleMuEl        , &b_HLT_DoubleMuEl);
   fChain->SetBranchAddress("HLT_TripleMu"           , &HLT_TripleMu          , &b_HLT_TripleMu);
   fChain->SetBranchAddress("HLT_DoubleElMu"         , &HLT_DoubleElMu        , &b_HLT_DoubleElMu);
   fChain->SetBranchAddress("HLT_DoubleMuNoIso"      , &HLT_DoubleMuNoIso     , &b_HLT_DoubleMuNoIso);
   fChain->SetBranchAddress("HLT_DoubleMuSS"         , &HLT_DoubleMuSS        , &b_HLT_DoubleMuSS);
   fChain->SetBranchAddress("HLT_SingleEl"           , &HLT_SingleEl          , &b_HLT_SingleEl);
   fChain->SetBranchAddress("HLT_TripleMuA"          , &HLT_TripleMuA         , &b_HLT_TripleMuA);
   fChain->SetBranchAddress("HLT_MuEG"               , &HLT_MuEG              , &b_HLT_MuEG);
   fChain->SetBranchAddress("HLT_DoubleMuHT"         , &HLT_DoubleMuHT        , &b_HLT_DoubleMuHT);
   fChain->SetBranchAddress("HLT_DoubleEl"           , &HLT_DoubleEl          , &b_HLT_DoubleEl);
   fChain->SetBranchAddress("HLT_DoubleMu"           , &HLT_DoubleMu          , &b_HLT_DoubleMu);
   fChain->SetBranchAddress("nLepGood"               , &nLepGood              , &b_nLepGood);
   fChain->SetBranchAddress("LepGood_mvaIdSpring15"  , LepGood_mvaIdSpring15  , &b_LepGood_mvaIdSpring15);
   fChain->SetBranchAddress("LepGood_mvaTTH"         , LepGood_mvaTTH         , &b_LepGood_mvaTTH);
   fChain->SetBranchAddress("LepGood_jetPtRatiov2"   , LepGood_jetPtRatiov2   , &b_LepGood_jetPtRatiov2);
   fChain->SetBranchAddress("LepGood_jetPtRelv2"     , LepGood_jetPtRelv2     , &b_LepGood_jetPtRelv2);
   fChain->SetBranchAddress("LepGood_jetBTagCSV"     , LepGood_jetBTagCSV     , &b_LepGood_jetBTagCSV);
   fChain->SetBranchAddress("LepGood_tightId"        , LepGood_tightId        , &b_LepGood_tightId);
   fChain->SetBranchAddress("LepGood_dxy"            , LepGood_dxy            , &b_LepGood_dxy);
   fChain->SetBranchAddress("LepGood_dz"             , LepGood_dz             , &b_LepGood_dz);
   fChain->SetBranchAddress("LepGood_ip3d"           , LepGood_ip3d           , &b_LepGood_ip3d);
   fChain->SetBranchAddress("LepGood_sip3d"          , LepGood_sip3d          , &b_LepGood_sip3d);
   fChain->SetBranchAddress("LepGood_convVeto"       , LepGood_convVeto       , &b_LepGood_convVeto);
   fChain->SetBranchAddress("LepGood_lostHits"       , LepGood_lostHits       , &b_LepGood_lostHits);
   fChain->SetBranchAddress("LepGood_relIso03"       , LepGood_relIso03       , &b_LepGood_relIso03);
   fChain->SetBranchAddress("LepGood_relIso04"       , LepGood_relIso04       , &b_LepGood_relIso04);
   fChain->SetBranchAddress("LepGood_miniRelIso"     , LepGood_miniRelIso     , &b_LepGood_miniRelIso);
   fChain->SetBranchAddress("LepGood_relIsoAn04"     , LepGood_relIsoAn04     , &b_LepGood_relIsoAn04);
   fChain->SetBranchAddress("LepGood_tightCharge"    , LepGood_tightCharge    , &b_LepGood_tightCharge);
   fChain->SetBranchAddress("LepGood_mcMatchId"      , LepGood_mcMatchId      , &b_LepGood_mcMatchId);
   fChain->SetBranchAddress("LepGood_mediumMuonId"   , LepGood_mediumMuonId   , &b_LepGood_mediumMuonId);
   fChain->SetBranchAddress("LepGood_innerTrackValidHitFraction" , LepGood_innerTrackValidHitFraction , &b_LepGood_innerTrackValidHitFraction);
   fChain->SetBranchAddress("LepGood_segmentCompatibility"       , LepGood_segmentCompatibility       , &b_LepGood_segmentCompatibility);
   fChain->SetBranchAddress("LepGood_globalTrackChi2"            , LepGood_globalTrackChi2            , &b_LepGood_globalTrackChi2);
   fChain->SetBranchAddress("LepGood_chi2LocalPosition"          , LepGood_chi2LocalPosition          , &b_LepGood_chi2LocalPosition);
   fChain->SetBranchAddress("LepGood_trkKink"                    , LepGood_trkKink                    , &b_LepGood_trkKink);
   fChain->SetBranchAddress("LepGood_isGlobalMuon"               , LepGood_isGlobalMuon               , &b_LepGood_isGlobalMuon);
   fChain->SetBranchAddress("LepGood_pdgId"          , LepGood_pdgId          , &b_LepGood_pdgId);
   fChain->SetBranchAddress("LepGood_pt"             , LepGood_pt             , &b_LepGood_pt);
   fChain->SetBranchAddress("LepGood_eta"            , LepGood_eta            , &b_LepGood_eta);
   fChain->SetBranchAddress("LepGood_phi"            , LepGood_phi            , &b_LepGood_phi);
   fChain->SetBranchAddress("LepGood_mass"           , LepGood_mass           , &b_LepGood_mass);
   fChain->SetBranchAddress("LepGood_hadronicOverEm" , LepGood_hadronicOverEm , &b_LepGood_hadronicOverEm);
   fChain->SetBranchAddress("LepGood_dEtaScTrkIn"    , LepGood_dEtaScTrkIn    , &b_LepGood_dEtaScTrkIn);
   fChain->SetBranchAddress("LepGood_dPhiScTrkIn"    , LepGood_dPhiScTrkIn    , &b_LepGood_dPhiScTrkIn);
   fChain->SetBranchAddress("LepGood_etaSc"          , LepGood_etaSc          , &b_LepGood_etaSc);
   fChain->SetBranchAddress("LepGood_eInvMinusPInv"  , LepGood_eInvMinusPInv  , &b_LepGood_eInvMinusPInv);
   fChain->SetBranchAddress("LepGood_sigmaIEtaIEta"  , LepGood_sigmaIEtaIEta  , &b_LepGood_sigmaIEtaIEta);

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
   fTnPTree->Branch("isdata"                 ,&fT_isdata                 ,"isdata/I");

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
   fTnPTree->Branch("ICHEPmediumMuonId"  ,&fT_ICHEPmediumMuonId  ,"ICHEPmediumMuonId/I");
   fTnPTree->Branch("mvaIdPhys14"   ,&fT_mvaIdPhys14   ,"mvaIdPhys14/F");
   fTnPTree->Branch("mvaIdSpring15" ,&fT_mvaIdSpring15 ,"mvaIdSpring15/F");
   fTnPTree->Branch("mcMatchId"     ,&fT_mcMatchId     ,"mcMatchId/I");
   fTnPTree->Branch("idEmu"         ,&fT_idEmu         ,"idEmu/F");
   fTnPTree->Branch("nJet25"        ,&fT_nJet25        ,"nJet25/I");
   fTnPTree->Branch("nBJetLoose25"  ,&fT_nBJetLoose25  ,"nBJetLoose25/I");
   fTnPTree->Branch("nBJetMedium25" ,&fT_nBJetMedium25 ,"nBJetMedium25/I");
   fTnPTree->Branch("met_pt"        ,&fT_met_pt        ,"met_pt/F");
   fTnPTree->Branch("puWeight"      ,&fT_puWeight      ,"puWeight/F");

   fTnPTree->Branch("tag_pt"        ,&fT_tag_pt        ,"tag_pt/F");
   fTnPTree->Branch("tag_eta"       ,&fT_tag_eta       ,"tag_eta/F");
   fTnPTree->Branch("tag_pdgId"     ,&fT_tag_pdgId     ,"tag_pdgId/I");
   fTnPTree->Branch("tag_relIso03"  ,&fT_tag_relIso03  ,"tag_relIso03/F");
   fTnPTree->Branch("tag_mcMatchId" ,&fT_tag_mcMatchId ,"tag_mcMatchId/I");

}

void lepTnPFriendTreeMaker::End(TFile *file){
   file->cd();
   fTnPTree->Write(fTnPTree->GetName());
   fHCutFlow->Write(fHCutFlow->GetName());
   file->Write();
   file->Close();
}

void lepTnPFriendTreeMaker::ResetTnPTree(){
   fT_evSel                  = -1;
   fT_passSingle             = -1;
   fT_passDouble             = -1;
   fT_run                    = run;
   fT_isdata                 = fIsData;
   fT_nVert                  = nVert;
   fT_pair_probeMultiplicity = 0;
   fT_mass                   = -999.99;

   fT_puWeight      = PuWeight();

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
   fT_ICHEPmediumMuonId  = -999;
   fT_mvaIdPhys14   = -999.99;
   fT_mvaIdSpring15 = -999.99;
   fT_idEmu         = -999.99;
   fT_nJet25        = -999;
   fT_nBJetLoose25  = -999;
   fT_nBJetMedium25 = -999;
   fT_met_pt        = -999.99;
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
   fHCutFlow->Fill(1);

   // Force e or mu (no taus)
   if( abs(LepGood_pdgId[0]) != 13 && abs(LepGood_pdgId[0]) != 11)
      return false;
   if( abs(LepGood_pdgId[1]) != 13 && abs(LepGood_pdgId[1]) != 11)
      return false;

   fHCutFlow->Fill(2);

   // Trigger selection (for data only)
   if( !PassDoubleTriggers() && !PassSingleTriggers() && fIsData ) return false;

   return true;
}

int lepTnPFriendTreeMaker::PassTTBarSelection(){
   if( !SelectEvent() ) return 0;
   if( nLepGood > 2 )   return 0;

   int evChan = LepGood_pdgId[0]*LepGood_pdgId[1];
   if( nBJetMedium25>0 && nBJetLoose25>1 ){
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

   if( LepGood_mvaTTH[i] < 0.75 ) return conept;
   return LepGood_pt[i];
}

float lepTnPFriendTreeMaker::PuWeight(){
   if( fIsData ) return 1.0;

   // For json up to 276811 (12.9/fb)
   int nTrueInt_int = int(nTrueInt);
   if( nTrueInt_int < 60 ) return fPUw2016_vtx_13fb[nTrueInt_int];
   else return 0;
}

bool lepTnPFriendTreeMaker::_ttH_idEmu_cuts_E2(int i){
    if (abs(LepGood_pdgId[i]) != 11) return true;
    if (LepGood_hadronicOverEm[i]    >= (0.10-0.03  *(fabs(LepGood_etaSc[i])>1.479))) return false;
    if (fabs(LepGood_dEtaScTrkIn[i]) >= (0.01-0.002 *(fabs(LepGood_etaSc[i])>1.479))) return false;
    if (fabs(LepGood_dPhiScTrkIn[i]) >= (0.04+0.03  *(fabs(LepGood_etaSc[i])>1.479))) return false;
    if (LepGood_eInvMinusPInv[i]     <= -0.05)                                        return false;
    if (LepGood_eInvMinusPInv[i]     >= (0.01-0.005 *(fabs(LepGood_etaSc[i])>1.479))) return false;
    if (LepGood_sigmaIEtaIEta[i]     >= (0.011+0.019*(fabs(LepGood_etaSc[i])>1.479))) return false;
    return true;
}

bool lepTnPFriendTreeMaker::PassLooseLepton(int i){
   if(LepGood_sip3d[i] > 8)         return false;

   return true;
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

bool lepTnPFriendTreeMaker::PassICHEPMediumMuonID(int i){
   if( abs(LepGood_pdgId[i]) != 13 ) return true;
   if( LepGood_innerTrackValidHitFraction[i] <= 0.49 ) return false;

   float segcomp_cut = 0.451;
   if( LepGood_isGlobalMuon[i] && LepGood_globalTrackChi2[i] < 3
                               && LepGood_chi2LocalPosition[i] < 12
                               && LepGood_trkKink[i] < 20) segcomp_cut = 0.303;

   if( LepGood_segmentCompatibility[i] > segcomp_cut) return true;
   return false;
}

bool lepTnPFriendTreeMaker::PassTightLepton(int i){
   if( !PassLooseLepton(i) ) return false;
   if( LepGood_mvaTTH[i] < 0.75 ) return false;
   if( LepGood_jetBTagCSV[i] > 0.80 ) return false;
   if( LepGood_jetPtRatiov2[i] < 0.3 ) return false;

   // Tight electrons
   if (abs(LepGood_pdgId[i]) == 11){
      if(LepGood_pt[i] > 30. && _ttH_idEmu_cuts_E2(i) < 1) return false;
      if(!PassConvRejection(i)) return false;
      return true;
   }

   // Tight Muons
   if( PassICHEPMediumMuonID(i) ) return true;
   return false;
}

int lepTnPFriendTreeMaker::SelectPair(int lep1, int lep2, float mass){
   // Disabled for now, want to keep all the pairs and apply the mass
   // selection later on.
   return 1;


   int chan = LepGood_pdgId[lep1]*LepGood_pdgId[lep2];
   int ttbarsel = PassTTBarSelection();

   // Same flavor, opposite sign (DY selection)
   if( chan == -11*11 || chan == -13*13){
      if( mass > 10. ) return 1;
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

      fHCutFlow->Fill(0);

      if(!SelectEvent()) continue;
      fHCutFlow->Fill(3);
      ResetTnPTree();

      fT_passSingle    = PassSingleTriggers();
      fT_passDouble    = PassDoubleTriggers();
      fT_nJet25        = nJet25;
      fT_nBJetLoose25  = nBJetLoose25;
      fT_nBJetMedium25 = nBJetMedium25;
      fT_met_pt        = met_pt;

      // Find a tag lepton
      for (int lep1 = 0; lep1 < nLepGood; ++lep1){
         if (  (abs(LepGood_pdgId[lep1])==11 && SelectTagElectron(lep1))
            || (abs(LepGood_pdgId[lep1])==13 && SelectTagMuon(lep1)) ) {

            if( abs(LepGood_pdgId[lep1])==11 ) fHCutFlow->Fill(4);
            if( abs(LepGood_pdgId[lep1])==13 ) fHCutFlow->Fill(8);

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
               if( abs(LepGood_pdgId[lep1])==11 ) fHCutFlow->Fill(5);
               if( abs(LepGood_pdgId[lep1])==13 ) fHCutFlow->Fill(9);
               fT_evSel = pairsel;
               fT_pair_probeMultiplicity++;
               fT_mass          = mass;

               // Save probe properties
               fT_pt            = LepGood_pt[lep2];
               fT_phi           = LepGood_phi[lep2];
               fT_abseta        = fabs(LepGood_eta[lep2]);
               fT_pdgId         = LepGood_pdgId[lep2];
               fT_passLoose     = PassLooseLepton(lep2);
               if( abs(LepGood_pdgId[lep1])==11 && PassLooseLepton(lep2)) fHCutFlow->Fill(6);
               if( abs(LepGood_pdgId[lep1])==13 && PassLooseLepton(lep2)) fHCutFlow->Fill(10);

               fT_passConvRej   = PassConvRejection(lep2);
               fT_passTight     = PassTightLepton(lep2);
               if( abs(LepGood_pdgId[lep1])==11 && PassTightLepton(lep2)) fHCutFlow->Fill(7);
               if( abs(LepGood_pdgId[lep1])==13 && PassTightLepton(lep2)) fHCutFlow->Fill(11);
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
               fT_ICHEPmediumMuonId = PassICHEPMediumMuonID(lep2);
               fT_mvaIdSpring15 = LepGood_mvaIdSpring15[lep2];
               fT_idEmu         = _ttH_idEmu_cuts_E2(lep2);
               if( !fIsData ) fT_mcMatchId = LepGood_mcMatchId[lep2];
               else           fT_mcMatchId = 1;

               // Save tag properties
               fT_tag_pt        = LepGood_pt[lep1];
               fT_tag_eta       = LepGood_eta[lep1];
               fT_tag_pdgId     = LepGood_pdgId[lep1];
               fT_tag_relIso03  = LepGood_relIso03[lep1];
               if( !fIsData ) fT_tag_mcMatchId = LepGood_mcMatchId[lep1];
               else           fT_tag_mcMatchId = 1;

               fTnPTree->Fill();
            }
         }
      } // end lepton loop 1
   } // end event loop
   std::cout << "\r [   done  ]" << std::endl;
}

#endif // #ifdef lepTnPFriendTreeMaker_cxx
