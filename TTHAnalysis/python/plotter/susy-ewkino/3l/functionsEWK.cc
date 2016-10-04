
int isConv(int nLep, int lep1mcUCSX, int lep2mcUCSX, int lep3mcUCSX, int lep4mcUCSX = 0) {
    if(nLep == 3) return (lep1mcUCSX==4 || lep2mcUCSX==4 || lep3mcUCSX==4);
    return (lep1mcUCSX==4 || lep2mcUCSX==4 || lep3mcUCSX==4 || lep4mcUCSX==4);
}

int isFake(int nLep, int lep1mcUCSX, int lep2mcUCSX, int lep3mcUCSX, int lep4mcUCSX = 0) {
    if(nLep == 3) return ((lep1mcUCSX==2 || lep1mcUCSX==3) || (lep2mcUCSX==2 || lep2mcUCSX==3) || (lep3mcUCSX==2 || lep3mcUCSX==3));
    return ((lep1mcUCSX==2 || lep1mcUCSX==3) || (lep2mcUCSX==2 || lep2mcUCSX==3) || (lep3mcUCSX==2 || lep3mcUCSX==3) || (lep4mcUCSX==2 || lep4mcUCSX==3));
}

int isFakeHF(int nLep, int lep1mcUCSX, int lep2mcUCSX, int lep3mcUCSX, int lep4mcUCSX = 0) {
    if(nLep == 3) return (lep1mcUCSX==3 || lep2mcUCSX==3 || lep3mcUCSX==3);
    return (lep1mcUCSX==3 || lep2mcUCSX==3 || lep3mcUCSX==3 || lep4mcUCSX==3);
}

int isFakeLF(int nLep, int lep1mcUCSX, int lep2mcUCSX, int lep3mcUCSX, int lep4mcUCSX = 0) {
    if(nLep == 3) return (lep1mcUCSX==2 || lep2mcUCSX==2 || lep3mcUCSX==2);
    return (lep1mcUCSX==2 || lep2mcUCSX==2 || lep3mcUCSX==2 || lep4mcUCSX==2);
}

int isPrompt(int nLep, int lep1mcUCSX, int lep2mcUCSX, int lep3mcUCSX, int lep4mcUCSX = 0) {
    if(nLep == 3) return ((lep1mcUCSX==0 || lep1mcUCSX==1) && (lep2mcUCSX==0 || lep2mcUCSX==1) && (lep3mcUCSX==0 || lep3mcUCSX==1));
    return ((lep1mcUCSX==0 || lep1mcUCSX==1) && (lep2mcUCSX==0 || lep2mcUCSX==1) && (lep3mcUCSX==0 || lep3mcUCSX==1) && (lep4mcUCSX==0 || lep4mcUCSX==1));
}

int isGoodFake(float pt, int isTight) {
    if(pt == 0) return 0;
    if(isTight) return 0;
    return 1;
}

int allTight(int nLep, int l1isTight, int l2isTight, int l3isTight, int l4isTight = 0){
    if(nLep == 3) return ((l1isTight+l2isTight+l3isTight)==3);
    return ((l1isTight+l2isTight+l3isTight+l4isTight)==4);
}

int countTaus(int nLep, int l1pdgId, int l2pdgId, int l3pdgId, int l4pdgId = 0){
    if(nLep == 3) return (abs(l1pdgId)==15)+(abs(l2pdgId)==15)+(abs(l3pdgId)==15);
    return (abs(l1pdgId)==15)+(abs(l2pdgId)==15)+(abs(l3pdgId)==15)+(abs(l4pdgId)==15);
}

int BR(int nLep, int nTau, int nOSSF, int nOSLF, int nOSTF){

    if(nLep == 3 && nTau == 0 && nOSSF >= 1              ) return 1;
    if(nLep == 3 && nTau == 0 && nOSSF <  1              ) return 2;
    if(nLep == 3 && nTau == 1 && nOSSF >= 1              ) return 3;
    if(nLep == 3 && nTau == 1 && nOSSF <  1 && nOSLF >= 1) return 4;
    if(nLep == 3 && nTau == 1 && nOSLF <  1              ) return 5;
    if(nLep == 3 && nTau == 2                            ) return 6;
    if(nLep == 4 && nTau == 0 && nOSSF >= 2              ) return 7;
    if(nLep == 4 && nTau == 0 && nOSSF <= 1              ) return 8;
    if(nLep == 4 && nTau == 1                            ) return 9;

    return 0;
}

int SR3lA(float mT2L, float mT2T, float mll, float mT, float met, int offset = 0) {

    if(mll >= 0 && mll < 75) {
        if (mT >=   0 && mT < 120 && met >=  50 && met < 100) return offset +  1;
        if (mT >=   0 && mT < 120 && met >= 100 && met < 150) return offset +  2;
        if (mT >=   0 && mT < 120 && met >= 150 && met < 200) return offset +  3;
        if (mT >=   0 && mT < 120 && met >= 200             ) return offset +  4;
        if (mT >= 120 && mT < 160 && met >=  50 && met < 100) return offset +  5;
        if (mT >= 120 && mT < 160 && met >= 100 && met < 150) return offset +  6;
        if (mT >= 120 && mT < 160 && met >= 150 && met < 200) return offset +  7;
        if (mT >= 120 && mT < 160 && met >= 200             ) return offset +  8;
        if (mT >= 160 &&             met >=  50 && met < 100) return offset +  9;
        if (mT >= 160 &&             met >= 100 && met < 150) return offset + 10;
        if (mT >= 160 &&             met >= 150 && met < 200) return offset + 11;
        if (mT >= 160 &&             met >= 200             ) return offset + 12;
    }
    if(mll >= 75 && mll < 105) {
        if (mT >=   0 && mT < 120 && met >=  50 && met < 100) return offset + 13;
        if (mT >=   0 && mT < 120 && met >= 100 && met < 150) return offset + 14;
        if (mT >=   0 && mT < 120 && met >= 150 && met < 200) return offset + 15;
        if (mT >=   0 && mT < 120 && met >= 200             ) return offset + 16;
        if (mT >= 120 && mT < 160 && met >=  50 && met < 100) return offset + 17;
        if (mT >= 120 && mT < 160 && met >= 100 && met < 150) return offset + 18;
        if (mT >= 120 && mT < 160 && met >= 150 && met < 200) return offset + 19;
        if (mT >= 120 && mT < 160 && met >= 200             ) return offset + 20;
        if (mT >= 160 &&             met >=  50 && met < 100) return offset + 21;
        if (mT >= 160 &&             met >= 100 && met < 150) return offset + 22;
        if (mT >= 160 &&             met >= 150 && met < 200) return offset + 23;
        if (mT >= 160 &&             met >= 200             ) return offset + 24;
    }
    if(mll >= 105) {
        if (mT >=   0 && mT < 120 && met >=  50 && met < 100) return offset + 25;
        if (mT >=   0 && mT < 120 && met >= 100 && met < 150) return offset + 26;
        if (mT >=   0 && mT < 120 && met >= 150 && met < 200) return offset + 27;
        if (mT >=   0 && mT < 120 && met >= 200             ) return offset + 28;
        if (mT >= 120 && mT < 160 && met >=  50 && met < 100) return offset + 29;
        if (mT >= 120 && mT < 160 && met >= 100 && met < 150) return offset + 30;
        if (mT >= 120 && mT < 160 && met >= 150 && met < 200) return offset + 31;
        if (mT >= 120 && mT < 160 && met >= 200             ) return offset + 32;
        if (mT >= 160 &&             met >=  50 && met < 100) return offset + 33;
        if (mT >= 160 &&             met >= 100 && met < 150) return offset + 34;
        if (mT >= 160 &&             met >= 150 && met < 200) return offset + 35;
        if (mT >= 160 &&             met >= 200             ) return offset + 36;
    }
    return 0;
}

int SR3lB(float mT2L, float mT2T, float mll, float mT, float met, int offset = 0) {

    if(mll < 100){
        if(mT <  120 && met >=  50 && met < 100) return offset + 1;
        if(mT <  120 && met >= 100             ) return offset + 2;
        if(mT >= 120 && met >=  50             ) return offset + 3;
    }
    if(mll >= 100) {
        if(mT <  120 && met >=  50 && met < 100) return offset + 4;
        if(mT <  120 && met >= 100             ) return offset + 5;
        if(mT >= 120 && met >=  50             ) return offset + 6;
    }

    return 0;
}

int SR3lC(float mT2L, float mT2T, float mll, float mT, float met, int offset = 0) {

    if(mT2L < 100  && mll >=   0 && mll <  75 && met >=  50 && met < 100) return offset +  1;
    if(mT2L < 100  && mll >=   0 && mll <  75 && met >= 100 && met < 150) return offset +  2;
    if(mT2L < 100  && mll >=   0 && mll <  75 && met >= 150 && met < 200) return offset +  3;
    if(mT2L < 100  && mll >=   0 && mll <  75 && met >= 200             ) return offset +  4;
    if(               mll >=  75 && mll < 105 && met >=  50 && met < 100) return offset +  5;
    if(               mll >=  75 && mll < 105 && met >= 100 && met < 150) return offset +  6;
    if(               mll >=  75 && mll < 105 && met >= 150 && met < 200) return offset +  7;
    if(               mll >=  75 && mll < 105 && met >= 200             ) return offset +  8;
    if(mT2L < 100  && mll >= 105 &&              met >=  50 && met < 100) return offset +  9;
    if(mT2L < 100  && mll >= 105 &&              met >= 100 && met < 150) return offset + 10;
    if(mT2L < 100  && mll >= 105 &&              met >= 150 && met < 200) return offset + 11;
    if(mT2L < 100  && mll >= 105 &&              met >= 200             ) return offset + 12;
    if(mT2L >= 100 && (mll < 75 || mll >= 105) && met >= 50 && met < 200) return offset + 13;
    if(mT2L >= 100 && (mll < 75 || mll >= 105) && met >= 200            ) return offset + 14;
    return 0;
}


int SR3lD(float mT2L, float mT2T, float mll, float mT, float met, int offset = 0) {

    if(mT2L >= 0 && mT2L < 100){
        if(mll >=   0 && mll <  60 && met >=  50 && met < 100) return offset +  1;
        if(mll >=   0 && mll <  60 && met >= 100 && met < 150) return offset +  2;
        if(mll >=   0 && mll <  60 && met >= 150 && met < 200) return offset +  3;
        if(mll >=   0 && mll <  60 && met >= 200             ) return offset +  4;
        if(mll >=  60 && mll < 100 && met >=  50 && met < 100) return offset +  5;
        if(mll >=  60 && mll < 100 && met >= 100 && met < 150) return offset +  6;
        if(mll >=  60 && mll < 100 && met >= 150 && met < 200) return offset +  7;
        if(mll >=  60 && mll < 100 && met >= 200             ) return offset +  8;
        if(mll >= 100 &&              met >=  50 && met < 100) return offset +  9;
        if(mll >= 100 &&              met >= 100 && met < 150) return offset + 10;
        if(mll >= 100 &&              met >= 150 && met < 200) return offset + 11;
        if(mll >= 100 &&              met >= 200             ) return offset + 12;
    }
    if(mT2L >= 100) {
        if(met >= 50 && met < 200                            ) return offset + 13;
        if(met >= 200                                        ) return offset + 14;
    }

    return 0;
}


int SR3lE(float mT2L, float mT2T, float mll, float mT, float met, int offset = 0) {

    if(mT2T >= 0 && mT2T < 100){
        if(mll >=   0 && mll <  60 && met >=  50 && met < 100) return offset +  1;
        if(mll >=   0 && mll <  60 && met >= 100 && met < 150) return offset +  2;
        if(mll >=   0 && mll <  60 && met >= 150 && met < 200) return offset +  3;
        if(mll >=   0 && mll <  60 && met >= 200             ) return offset +  4;
        if(mll >=  60 && mll < 100 && met >=  50 && met < 100) return offset +  5;
        if(mll >=  60 && mll < 100 && met >= 100 && met < 150) return offset +  6;
        if(mll >=  60 && mll < 100 && met >= 150 && met < 200) return offset +  7;
        if(mll >=  60 && mll < 100 && met >= 200             ) return offset +  8;
        if(mll >= 100 &&              met >=  50             ) return offset +  9;
    }
    if(mT2T >= 100) {
        if(met >= 50                                         ) return offset + 10;
    }

    return 0;
}


int SR3lF(float mT2L, float mT2T, float mll, float mT, float met, int offset = 0) {

    if(mT2T >= 0 && mT2T < 100){
        if(mll >=   0 && mll < 100 && met >=  50 && met < 100) return offset +  1;
        if(mll >=   0 && mll < 100 && met >= 100 && met < 150) return offset +  2;
        if(mll >=   0 && mll < 100 && met >= 150             ) return offset +  3;
        if(mll >= 100 &&              met >=  50 && met < 100) return offset +  4;
        if(mll >= 100 &&              met >= 100 && met < 150) return offset +  5;
        if(mll >= 100 &&              met >= 150             ) return offset +  6;
    }
    if(mT2T >= 100) {
        if(met >= 50 && met < 200                            ) return offset +  7;
        if(met >= 200                                        ) return offset +  8;
    }

    return 0;
}


int SR4lG(float mT2L, float mT2T, float mll, float mT, float met, int offset = 0) {

    if(met >=   0 && met <  30) return offset + 1;
    if(met >=  30 && met <  50) return offset + 2;
    if(met >=  50 && met < 100) return offset + 3;
    if(met >= 100             ) return offset + 4;

    return 0;
}

int SR3l(int nTau, int nOSSF, int nOSLF, float mT2L, float mT2T, float mll, float mT, float met){

    // 3 light
    if(nTau == 0 && nOSSF >= 1              ) return SR3lA(mT2L, mT2T, mll, mT, met,  0);
    if(nTau == 0 && nOSSF <  1              ) return SR3lB(mT2L, mT2T, mll, mT, met, 36);
    // 2 light + 1 tau
    if(nTau == 1 && nOSSF >= 1              ) return SR3lC(mT2L, mT2T, mll, mT, met, 42);
    if(nTau == 1 && nOSSF <  1 && nOSLF >= 1) return SR3lD(mT2L, mT2T, mll, mT, met, 56);
    if(nTau == 1 && nOSLF <  1              ) return SR3lE(mT2L, mT2T, mll, mT, met, 70);
    // 1 light + 2 tau
    if(nTau == 2                            ) return SR3lF(mT2L, mT2T, mll, mT, met, 80);
    return 0;
}

int SR4l(int nTau, int nOSSF, int nOSLF, float mT2L, float mT2T, float mll, float mT, float met){

    // 4 light
    if(nTau == 0 && nOSSF >= 2              ) return SR4lG(mT2L, mT2T, mll, mT, met, 88);
    if(nTau == 0 && nOSSF <= 1              ) return SR4lG(mT2L, mT2T, mll, mT, met, 92);
    // 3light + 1 tau
    if(nTau == 1                            ) return SR4lG(mT2L, mT2T, mll, mT, met, 96);
    return 0;
}

int SR(int nLep, int nTau, int nOSSF, int nOSLF, float mT2L, float mT2T, float mll, float mT, float met) {

    if(nLep == 3)
        return SR3l(nTau, nOSSF, nOSLF, mT2L, mT2T, mll, mT, met);
    if(nLep == 4)
        return SR4l(nTau, nOSSF, nOSLF, mT2L, mT2T, mll, mT, met);
    return 0;
}

#include "TH2F.h"
#include "TMath.h"
#include "TGraphAsymmErrors.h"
#include "TFile.h"
#include "TSystem.h"

TString CMSSW_BASE_EWK = gSystem->ExpandPathName("${CMSSW_BASE}");

TFile* trigSF = new TFile(CMSSW_BASE_EWK+"/src/CMGTools/TTHAnalysis/data/triggerSF/EWKino_9p2_triggerSF.root", "read");
TFile* trigSFele27 = new TFile(CMSSW_BASE_EWK+"/src/CMGTools/TTHAnalysis/data/triggerSF/EWKino_12p9_triggerSF_ele27.root", "read");
TH2F* _trigSF_3l_m = (TH2F*) trigSF->Get("eff_3l_mu" );
TH2F* _trigSF_3l_e = (TH2F*) trigSF->Get("eff_3l_ele");
TH2F* _trigSF_2l_m = (TH2F*) trigSF->Get("eff_2l_mu" );
TH2F* _trigSF_2l_e = (TH2F*) trigSF->Get("eff_2l_ele");
TH2F* _trigSF_ele27 = (TH2F*) trigSFele27->Get("hist2dnum_Ele27_WPLoose_Gsf__HLT_Ele27_WPLoose_Gsf");


float triggerSFBR6(float pt1, float eta1, int pdg1,
                   float pt2, float eta2, int pdg2,
                   float pt3, float eta3, int pdg3) {

        if(abs(pdg1)+abs(pdg2)+abs(pdg3)==43) return 0.86;

        float pt = pt1; float eta = eta1;
        if(abs(pdg2)==11) {pt = pt2; eta=eta2; }
        if(abs(pdg3)==11) {pt = pt3; eta=eta3; }
        TH2F* hist = _trigSF_ele27;
        int xbin = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(pt)));
        int ybin = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(abs(eta))));
        return hist->GetBinContent(xbin,ybin);
}


float triggerSF(int BR, float pt1, int pdg1, 
                        float pt2, int pdg2, 
                        float pt3, int pdg3, 
                        float pt4 = 0, int pdg4 = 0){
    // Lesya's mail:
    // - split for trailing ele or trailing mu
    // - 3l: subleading vs trailing lepton pt (1l + 2l triggers)
    // - 2l: leading light lepton vs subleading light lepton ==> good for both 2l+tau and 2lSS cases (1l + 2l triggers)
    // - l+tautau: use flat 86% everywhere; pt_e > 35 GeV; pt_mu > 25 GeV (1l + l/tau triggers)

    // flat 86% 
    if(BR == 6) return 1.0;

    // 3l
    if(BR <= 2) {
        TH2F* hist = (abs(pdg3) == 13)?_trigSF_3l_m:_trigSF_3l_e;
        int xbin = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(pt2)));
        int ybin = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(pt3)));
        return hist->GetBinContent(xbin,ybin);
    } 

    // 2l
    if(BR >= 3 && BR <= 5){
        vector<int> pdgs; vector<float> pts;
        if(abs(pdg1)!=15) { pdgs.push_back(abs(pdg1)); pts.push_back(pt1); }
        if(abs(pdg2)!=15) { pdgs.push_back(abs(pdg2)); pts.push_back(pt2); }
        if(abs(pdg3)!=15) { pdgs.push_back(abs(pdg3)); pts.push_back(pt3); }
        TH2F* hist = (pdgs[1] == 13)?_trigSF_2l_m:_trigSF_2l_e;
        int xbin = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(pts[0])));
        int ybin = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(pts[1])));
        return hist->GetBinContent(xbin,ybin);
    } 
    return 1;
}


// electrons
TFile* elSFmva = new TFile(CMSSW_BASE_EWK+"/src/CMGTools/TTHAnalysis/data/leptonSF/SF2016_electron_lepMVAmedium.root", "read");
TFile* elSFeff = new TFile(CMSSW_BASE_EWK+"/src/CMGTools/TTHAnalysis/data/leptonSF/SF2016_electron_trackingEff.root", "read");
TH2F* _lepSF_eMVA = (TH2F*) elSFmva->Get("GsfElectronToLeptonMvaMIDEmuTightIP2DSIP3D8miniIso04");
TH2F* _lepSF_eID  = (TH2F*) elSFmva->Get("GsfElectronToLoose2D");
TH2F* _lepSF_eTRK = (TH2F*) elSFeff->Get("EGamma_SF2D");

// muons
TFile* muSFmva = new TFile(CMSSW_BASE_EWK+"/src/CMGTools/TTHAnalysis/data/leptonSF/SF2016_muon_lepMVAmedium.root", "read");
TFile* muSFid  = new TFile(CMSSW_BASE_EWK+"/src/CMGTools/TTHAnalysis/data/leptonSF/SF2016_muon_mediumId.root"   , "read");
TFile* muSFeff = new TFile(CMSSW_BASE_EWK+"/src/CMGTools/TTHAnalysis/data/leptonSF/SF2016_muon_trackingEff.root", "read"); 
TH2F* _lepSF_mMVA = (TH2F*) muSFmva->Get("pt_abseta_PLOT_pair_probeMultiplicity_bin0_&_tag_combRelIsoPF04dBeta_bin0_&_tag_pt_bin0_&_mvaPreSel_pass" );
TH2F* _lepSF_mID  = (TH2F*) muSFid->Get("pt_abseta_PLOT_pair_probeMultiplicity_bin0" );
TGraphAsymmErrors* _lepSF_mTRK = (TGraphAsymmErrors*) muSFeff->Get("ratio_eta");

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

float getElectronSF(float pt, float eta){
    return getSF(_lepSF_eMVA, pt, abs(eta))*getSF(_lepSF_eID, pt, abs(eta))*getSF(_lepSF_eTRK, eta, pt);
}

float getElectronUnc(float pt, float eta, int var = 0){
    float error1 = getUnc(_lepSF_eMVA, pt , abs(eta));
    float error2 = getUnc(_lepSF_eID , pt , abs(eta));
    float error3 = getUnc(_lepSF_eTRK, eta, pt);
    return var*TMath::Sqrt(error1*error1 + error2*error2 + error3*error3);
}

float getMuonSF(float pt, float eta){
    return _lepSF_mTRK->Eval(eta)*getSF(_lepSF_mMVA, pt, abs(eta))*getSF(_lepSF_mID, pt, abs(eta)); 
}

float getMuonUnc(float pt, int var = 0) {
    if (pt<20) 
         return var*TMath::Sqrt(0.03*0.03+0.01*0.01+0.01*0.01);
    return var*TMath::Sqrt(0.02*0.02+0.01*0.01);  
}

float getLeptonSF(float pt, float eta, int pdgId, int var = 0){
    if(abs(pdgId) == 13) return (var==0)?getMuonSF(pt, eta):(1+getMuonUnc(pt, var));
    if(abs(pdgId) == 11) return (var==0)?getElectronSF(pt, eta):(1+getElectronUnc(pt,eta,var));
    return 1.0;
}

float leptonSF(float lepSF1, float lepSF2, float lepSF3, float lepSF4 = 1){
    return lepSF1*lepSF2*lepSF3*lepSF4;
}


// FASTSIM TO FULLSIM

// electrons
TFile* elSFmvaFS = new TFile(CMSSW_BASE_EWK+"/src/CMGTools/TTHAnalysis/data/leptonSF/SF2016_electron_lepMVAmedium_FS.root", "read");
TFile* elSFidFS  = new TFile(CMSSW_BASE_EWK+"/src/CMGTools/TTHAnalysis/data/leptonSF/SF2016_electron_mvaID_FS.root", "read");
TH2F* _lepSF_eMVA_FS = (TH2F*) elSFmvaFS->Get("histo2D");
TH2F* _lepSF_eID_FS  = (TH2F*) elSFidFS ->Get("histo2D");

// muons
TFile* muSFmvaFS = new TFile(CMSSW_BASE_EWK+"/src/CMGTools/TTHAnalysis/data/leptonSF/SF2016_muon_lepMVAmedium_FS.root", "read");
TFile* muSFidFS  = new TFile(CMSSW_BASE_EWK+"/src/CMGTools/TTHAnalysis/data/leptonSF/SF2016_muon_mediumId_FS.root"   , "read");
TH2F* _lepSF_mMVA_FS = (TH2F*) muSFmvaFS->Get("histo2D" );
TH2F* _lepSF_mID_FS  = (TH2F*) muSFidFS->Get("histo2D" );


float getElectronSFFS(float pt, float eta){
    return getSF(_lepSF_eMVA_FS, pt, abs(eta))*getSF(_lepSF_eID_FS, pt, abs(eta));
}

float getElectronUncFS(int var = 0){
	return var*0.02;
}

float getMuonSFFS(float pt, float eta){
    return getSF(_lepSF_mMVA_FS, pt, abs(eta))*getSF(_lepSF_mID_FS, pt, abs(eta)); 
}

float getMuonUncFS(float pt, int var = 0) {
	return var*0.02;
}

float getLeptonSFFS(float pt, float eta, int pdgId, int var = 0){
    if(abs(pdgId) == 13) return (var==0)?getMuonSFFS(pt, eta):(1+getMuonUncFS(var));
    if(abs(pdgId) == 11) return (var==0)?getElectronSFFS(pt, eta):(1+getElectronUncFS(var));
    return 1.0;
}

float leptonSFFS(float lepSF1, float lepSF2, float lepSF3, float lepSF4 = 1.0){
    return lepSF1*lepSF2*lepSF3*lepSF4;
}


void functionsEWK() {}
