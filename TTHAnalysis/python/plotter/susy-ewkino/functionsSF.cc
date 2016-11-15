#include "TH2F.h"
#include "TMath.h"
#include "TGraphAsymmErrors.h"
#include "TFile.h"
#include "TSystem.h"

TString CMSSW_BASE_SF = gSystem->ExpandPathName("${CMSSW_BASE}");
TString DATA_SF = CMSSW_BASE_SF+"/src/CMGTools/TTHAnalysis/data";

float getSF(TH2F* hist, float pt, float eta){
    int xbin = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(pt)));
    int ybin = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(eta)));
    return hist->GetBinContent(xbin,ybin);
}

float getUnc(TH2F* hist, float pt, float eta){
    int xbin = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(pt)));
    int ybin = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(eta)));
    return hist->GetBinError(xbin,ybin);
}


// TRIGGER SCALE FACTORS FULLSIM
// -------------------------------------------------------------

TFile* f_trigSF       = new TFile(DATA_SF+"/triggerSF/triggerSF_EWKino_fullsim_ICHEP2016_9p2fb.root"       , "read");
TFile* f_trigSF_ele27 = new TFile(DATA_SF+"/triggerSF/triggerSF_Ele27_EWKino_fullsim_ICHEP2016_12p9fb.root", "read");

TH2F* h_trigSF_3l_mu = (TH2F*) f_trigSF      ->Get("eff_3l_mu" );
TH2F* h_trigSF_3l_el = (TH2F*) f_trigSF      ->Get("eff_3l_ele");
TH2F* h_trigSF_2l_mu = (TH2F*) f_trigSF      ->Get("eff_2l_mu" );
TH2F* h_trigSF_2l_el = (TH2F*) f_trigSF      ->Get("eff_2l_ele");
TH2F* h_trigSF_ele27 = (TH2F*) f_trigSF_ele27->Get("hist2dnum_Ele27_WPLoose_Gsf__HLT_Ele27_WPLoose_Gsf");

float triggerSFBR6(float pt1, float eta1, int pdg1,
                   float pt2, float eta2, int pdg2,
                   float pt3, float eta3, int pdg3) {

        if(abs(pdg1)+abs(pdg2)+abs(pdg3)==43) return 0.86;

        float pt = pt1; float eta = eta1;
        if(abs(pdg2)==11) {pt = pt2; eta=eta2; }
        if(abs(pdg3)==11) {pt = pt3; eta=eta3; }
        TH2F* hist = h_trigSF_ele27;
        int xbin = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(pt)));
        int ybin = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(abs(eta))));
        return hist->GetBinContent(xbin,ybin);
}


float triggerSF(int BR, float pt1, int pdg1, 
                        float pt2, int pdg2, 
                        float pt3 = 0, int pdg3 = 0, 
                        float pt4 = 0, int pdg4 = 0){
    // Lesya's mail:
    // - split for trailing ele or trailing mu
    // - 3l: subleading vs trailing lepton pt (1l + 2l triggers)
    // - 2l: leading light lepton vs subleading light lepton ==> good for both 2l+tau and 2lSS cases (1l + 2l triggers)
    // - l+tautau: use flat 86% everywhere; pt_e > 35 GeV; pt_mu > 25 GeV (1l + l/tau triggers)

    // 3l: 2tau (flat 86% in dedicated function)
    if(BR == 6) return 1.0;

    // 3l: 3light
    if(BR <= 2) {
        TH2F* hist = (abs(pdg3) == 13)?h_trigSF_3l_mu:h_trigSF_3l_el;
        int xbin = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(pt2)));
        int ybin = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(pt3)));
        return hist->GetBinContent(xbin,ybin);
    } 

    // 3l: 2light + 1tau
    if(BR >= 3 && BR <= 5){
        vector<int> pdgs; vector<float> pts;
        if(abs(pdg1)!=15) { pdgs.push_back(abs(pdg1)); pts.push_back(pt1); }
        if(abs(pdg2)!=15) { pdgs.push_back(abs(pdg2)); pts.push_back(pt2); }
        if(abs(pdg3)!=15) { pdgs.push_back(abs(pdg3)); pts.push_back(pt3); }
        TH2F* hist = (pdgs[1] == 13)?h_trigSF_2l_mu:h_trigSF_2l_el;
        int xbin = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(pts[0])));
        int ybin = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(pts[1])));
        return hist->GetBinContent(xbin,ybin);
    }

    // 2lss 
    if(BR == -1){
        TH2F* hist = (pdg2 == 13)?h_trigSF_2l_mu:h_trigSF_2l_el;
        int xbin = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(pt1)));
        int ybin = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(pt2)));
        return hist->GetBinContent(xbin,ybin);
    }

    // others: (4l, crwz) 
    return 1;
}



// LEPTON SCALE FACTORS FULLSIM
// -------------------------------------------------------------

// electrons
TFile* f_elSF_id   = new TFile(DATA_SF+"/leptonSF/electronSF_id_EWKino_fullsim_ICHEP2016_12p9fb.root"    , "read");
TFile* f_elSF_eff  = new TFile(DATA_SF+"/leptonSF/electronSF_trkEff_EWKino_fullsim_ICHEP2016_12p9fb.root", "read");
TH2F* h_elSF_mvaVT = (TH2F*) f_elSF_id ->Get("GsfElectronToLeptonMvaVTIDEmuTightIP2DSIP3D8miniIso04");
TH2F* h_elSF_mvaM  = (TH2F*) f_elSF_id ->Get("GsfElectronToLeptonMvaMIDEmuTightIP2DSIP3D8miniIso04");
TH2F* h_elSF_id    = (TH2F*) f_elSF_id ->Get("GsfElectronToLoose2D");
TH2F* h_elSF_trk   = (TH2F*) f_elSF_eff->Get("EGamma_SF2D");

// muons
TFile* f_muSF_mvaVT = new TFile(DATA_SF+"/leptonSF/muonSF_mvaVT_EWKino_fullsim_ICHEP2016_12p9fb.root", "read");
TFile* f_muSF_mvaM  = new TFile(DATA_SF+"/leptonSF/muonSF_mvaM_EWKino_fullsim_ICHEP2016_12p9fb.root" , "read");
TFile* f_muSF_id    = new TFile(DATA_SF+"/leptonSF/muonSF_id_EWKino_fullsim_ICHEP2016_12p9fb.root"   , "read");
TFile* f_muSF_eff   = new TFile(DATA_SF+"/leptonSF/muonSF_trk_EWKino_fullsim_ICHEP2016_12p9fb.root"  , "read"); 
TH2F* h_muSF_mvaVT = (TH2F*) f_muSF_mvaVT->Get("pt_abseta_PLOT_pair_probeMultiplicity_bin0_&_tag_combRelIsoPF04dBeta_bin0_&_tag_pt_bin0_&_mvaPreSel_pass" );
TH2F* h_muSF_mvaM  = (TH2F*) f_muSF_mvaM ->Get("pt_abseta_PLOT_pair_probeMultiplicity_bin0_&_tag_combRelIsoPF04dBeta_bin0_&_tag_pt_bin0_&_mvaPreSel_pass" );
TH2F* h_muSF_id    = (TH2F*) f_muSF_id   ->Get("pt_abseta_PLOT_pair_probeMultiplicity_bin0" );
TGraphAsymmErrors* h_muSF_trk = (TGraphAsymmErrors*) f_muSF_eff->Get("ratio_eta");

float getElectronSF(float pt, float eta, int wp = 0){
    TH2F* hist = (wp == 1)?h_elSF_mvaVT:h_elSF_mvaM;
    return getSF(hist, pt, abs(eta))*getSF(h_elSF_id, pt, abs(eta))*getSF(h_elSF_trk, eta, pt);
}

float getElectronUnc(float pt, float eta, int wp = 0, int var = 0){
    TH2F* hist = (wp == 1)?h_elSF_mvaVT:h_elSF_mvaM;
    float error1 = getUnc(hist      , pt , abs(eta));
    float error2 = getUnc(h_elSF_id , pt , abs(eta));
    float error3 = getUnc(h_elSF_trk, eta, pt);
    return var*TMath::Sqrt(error1*error1 + error2*error2 + error3*error3);
}

float getMuonSF(float pt, float eta, int wp = 0){
    TH2F* hist = (wp == 1)?h_muSF_mvaVT:h_muSF_mvaM;
    return h_muSF_trk->Eval(eta)*getSF(hist, pt, abs(eta))*getSF(h_muSF_id, pt, abs(eta)); 
}

float getMuonUnc(float pt, int var = 0) {
    if (pt<20) 
         return var*TMath::Sqrt(0.03*0.03+0.01*0.01+0.01*0.01);
    return var*TMath::Sqrt(0.02*0.02+0.01*0.01);  
}

float getLepSF(float pt, float eta, int pdgId, int wp = 0, int var = 0){
    if(abs(pdgId) == 13) return (var==0)?getMuonSF    (pt, eta, wp):(1+getMuonUnc    (pt, var));
    if(abs(pdgId) == 11) return (var==0)?getElectronSF(pt, eta, wp):(1+getElectronUnc(pt, eta, wp, var));
    if(abs(pdgId) == 15) return 0.83;
    return 1.0;
}

float leptonSF(float lepSF1, float lepSF2, float lepSF3 = 1, float lepSF4 = 1){
    return lepSF1*lepSF2*lepSF3*lepSF4;
}



// LEPTON SCALE FACTORS FASTSIM
// -------------------------------------------------------------

// electrons
TFile* f_elSF_FS_mvaVT = new TFile(DATA_SF+"/leptonSF/electronSF_mvaVT_EWKino_fastsim_ICHEP2016_12p9fb.root", "read");
TFile* f_elSF_FS_mvaM  = new TFile(DATA_SF+"/leptonSF/electronSF_mvaM_EWKino_fastsim_ICHEP2016_12p9fb.root" , "read");
TFile* f_elSF_FS_id    = new TFile(DATA_SF+"/leptonSF/electronSF_id_EWKino_fastsim_ICHEP2016_12p9fb.root"   , "read");
TH2F* h_elSF_FS_mvaVT  = (TH2F*) f_elSF_FS_mvaVT->Get("histo2D");
TH2F* h_elSF_FS_mvaM   = (TH2F*) f_elSF_FS_mvaM ->Get("histo2D");
TH2F* h_elSF_FS_id     = (TH2F*) f_elSF_FS_id   ->Get("histo2D");

// muons
TFile* f_muSF_FS_mvaVT = new TFile(DATA_SF+"/leptonSF/muonSF_mvaVT_EWKino_fastsim_ICHEP2016_12p9fb.root", "read");
TFile* f_muSF_FS_mvaM  = new TFile(DATA_SF+"/leptonSF/muonSF_mvaM_EWKino_fastsim_ICHEP2016_12p9fb.root" , "read");
TFile* f_muSF_FS_id    = new TFile(DATA_SF+"/leptonSF/muonSF_id_EWKino_fastsim_ICHEP2016_12p9fb.root"   , "read");
TH2F* h_muSF_FS_mvaVT = (TH2F*) f_muSF_FS_mvaVT->Get("histo2D");
TH2F* h_muSF_FS_mvaM  = (TH2F*) f_muSF_FS_mvaM ->Get("histo2D");
TH2F* h_muSF_FS_id    = (TH2F*) f_muSF_FS_id   ->Get("histo2D");

// taus
TFile* f_tauSF_FS_id = new TFile(DATA_SF+"/leptonSF/tauSF_id_EWKino_fastsim_ICHEP2016_12p9fb.root", "read");
TH2F* h_tauSF_FS_id  = (TH2F*) f_tauSF_FS_id->Get("histo2D" );

float getElectronSFFS(float pt, float eta, int wp = 0){
    TH2F* hist = (wp == 1)?h_elSF_FS_mvaVT:h_elSF_FS_mvaM;
    return getSF(hist, pt, abs(eta))*getSF(h_elSF_FS_id, pt, abs(eta));
}

float getElectronUncFS(int var = 0){
	return var*0.02;
}

float getMuonSFFS(float pt, float eta, int wp = 0){
    TH2F* hist = (wp == 1)?h_muSF_FS_mvaVT:h_muSF_FS_mvaM;
    return getSF(hist, pt, abs(eta))*getSF(h_muSF_FS_id, pt, abs(eta)); 
}

float getMuonUncFS(float pt, int var = 0) {
	return var*0.02;
}

float getTauSFFS(float pt, float eta){
    return getSF(h_tauSF_FS_id, pt, abs(eta));
}

float getTauUncFS(float pt, float eta, int var = 0) {
	int fact = 1;
	if(var == 2) fact = -1;
	return fact * getUnc(h_tauSF_FS_id, pt, abs(eta));
}

float getLepSFFS(float pt, float eta, int pdgId, int wp, int var = 0){
    if(abs(pdgId) == 13) return (var==0)?getMuonSFFS    (pt, eta, wp):(1+getMuonUncFS(var));
    if(abs(pdgId) == 11) return (var==0)?getElectronSFFS(pt, eta, wp):(1+getElectronUncFS(var));
    if(abs(pdgId) == 15) return (var==0)?getTauSFFS     (pt, eta    ):(1+getTauUncFS(pt, eta, var));
    return 1.0;
}

float leptonSFFS(float lepSF1, float lepSF2, float lepSF3 = 1.0, float lepSF4 = 1.0){
    return lepSF1*lepSF2*lepSF3*lepSF4;
}


void functionsSF() {}
