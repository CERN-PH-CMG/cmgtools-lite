#include <cmath>
#include <map>
#include "Math/GenVector/LorentzVector.h"
#include "Math/GenVector/PtEtaPhiM4D.h"
#include "Math/GenVector/PxPyPzM4D.h"
#include "Math/GenVector/Boost.h"
#include "TLorentzVector.h"
#include "TH2Poly.h"
#include "TGraphAsymmErrors.h"
#include "TH1F.h"
#include "TFile.h"
#include "PhysicsTools/Heppy/interface/Davismt2.h"
#include "TSystem.h"

TString CMSSW_BASE = gSystem->ExpandPathName("${CMSSW_BASE}");

//// UTILITY FUNCTIONS NOT IN TFORMULA ALREADY

float myratio(float num, float denom) {
  if(denom==0) return 0;
  return num/denom;
}

float deltaPhi(float phi1, float phi2) {
    float result = phi1 - phi2;
    while (result > float(M_PI)) result -= float(2*M_PI);
    while (result <= -float(M_PI)) result += float(2*M_PI);
    return result;
}

float if3(bool cond, float iftrue, float iffalse) {
    return cond ? iftrue : iffalse;
}

float deltaR2(float eta1, float phi1, float eta2, float phi2) {
    float deta = std::abs(eta1-eta2);
    float dphi = deltaPhi(phi1,phi2);
    return deta*deta + dphi*dphi;
}
float deltaR(float eta1, float phi1, float eta2, float phi2) {
    return std::sqrt(deltaR2(eta1,phi1,eta2,phi2));
}

float pt_2(float pt1, float phi1, float pt2, float phi2) {
    phi2 -= phi1;
    return hypot(pt1 + pt2 * std::cos(phi2), pt2*std::sin(phi2));
}

float mt_2(float pt1, float phi1, float pt2, float phi2) {
    return std::sqrt(2*pt1*pt2*(1-std::cos(phi1-phi2)));
}

float mass_2(float pt1, float eta1, float phi1, float m1, float pt2, float eta2, float phi2, float m2) {
    typedef ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double> > PtEtaPhiMVector;
    PtEtaPhiMVector p41(pt1,eta1,phi1,m1);
    PtEtaPhiMVector p42(pt2,eta2,phi2,m2);
    return (p41+p42).M();
}

float mt2davis(float pt1, float eta1, float phi1, float pt2, float eta2, float phi2, float met, float metphi){
    // NOTE THAT THIS FUNCTION ASSUMES MASSLESS OBJECTS. NOT ADVISED TO USE WITH HEMISPHERES ETC.
    typedef ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double> > PtEtaPhiMVector;
    PtEtaPhiMVector p1(pt1,eta1,phi1,0.);
    PtEtaPhiMVector p2(pt2,eta2,phi2,0.);
    PtEtaPhiMVector mv(met,0.,metphi,0.);
    double a[] = {p1.M(), p1.Px(), p1.Py()};
    double b[] = {p2.M(), p2.Px(), p2.Py()};
    double c[] = {mv.M(), mv.Px(), mv.Py()};

    heppy::Davismt2 mt2obj;
    mt2obj.set_momenta( a, b, c );
    mt2obj.set_mn( 0. );

    float result = (float) mt2obj.get_mt2();
    return result;
}

float phi_2(float pt1, float phi1, float pt2, float phi2) {
    float px1 = pt1 * std::cos(phi1);
    float py1 = pt1 * std::sin(phi1);
    float px2 = pt2 * std::cos(phi2);
    float py2 = pt2 * std::sin(phi2);
    return std::atan2(py1+py2,px1+px2);
}

float pt_3(float pt1, float phi1, float pt2, float phi2, float pt3, float phi3) {
    phi2 -= phi1;
    phi3 -= phi1;
    return hypot(pt1 + pt2 * std::cos(phi2) + pt3 * std::cos(phi3), pt2*std::sin(phi2) + pt3*std::sin(phi3));
}


float mass_3(float pt1, float eta1, float phi1, float m1, float pt2, float eta2, float phi2, float m2, float pt3, float eta3, float phi3, float m3) {
    typedef ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double> > PtEtaPhiMVector;
    PtEtaPhiMVector p41(pt1,eta1,phi1,m1);
    PtEtaPhiMVector p42(pt2,eta2,phi2,m2);
    PtEtaPhiMVector p43(pt3,eta3,phi3,m3);
    return (p41+p42+p43).M();
}


float pt_4(float pt1, float phi1, float pt2, float phi2, float pt3, float phi3, float pt4, float phi4) {
    phi2 -= phi1;
    phi3 -= phi1;
    phi4 -= phi1;
    return hypot(pt1 + pt2 * std::cos(phi2) + pt3 * std::cos(phi3) + pt4 * std::cos(phi4), pt2*std::sin(phi2) + pt3*std::sin(phi3) + pt4*std::sin(phi4));
}
 
float mass_4(float pt1, float eta1, float phi1, float m1, float pt2, float eta2, float phi2, float m2, float pt3, float eta3, float phi3, float m3, float pt4, float eta4, float phi4, float m4) {
    typedef ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double> > PtEtaPhiMVector;
    PtEtaPhiMVector p41(pt1,eta1,phi1,m1);
    PtEtaPhiMVector p42(pt2,eta2,phi2,m2);
    PtEtaPhiMVector p43(pt3,eta3,phi3,m3);
    PtEtaPhiMVector p44(pt4,eta4,phi4,m4);
    return (p41+p42+p43+p44).M();
}

float mt_llv(float ptl1, float phil1, float ptl2, float phil2, float ptv, float phiv) {
    float px = ptl1*std::cos(phil1) + ptl2*std::cos(phil2) + ptv*std::cos(phiv);
    float py = ptl1*std::sin(phil1) + ptl2*std::sin(phil2) + ptv*std::sin(phiv);
    float ht = ptl1+ptl2+ptv;
    return std::sqrt(std::max(0.f, ht*ht - px*px - py*py));
}

float mt_lllv(float ptl1, float phil1, float ptl2, float phil2, float ptl3, float phil3, float ptv, float phiv) {
    float px = ptl1*std::cos(phil1) + ptl2*std::cos(phil2) + ptl3*std::cos(phil3) + ptv*std::cos(phiv);
    float py = ptl1*std::sin(phil1) + ptl2*std::sin(phil2) + ptl3*std::sin(phil3) + ptv*std::sin(phiv);
    float ht = ptl1+ptl2+ptl3+ptv;
    return std::sqrt(std::max(0.f, ht*ht - px*px - py*py));
}


float mtw_wz3l(float pt1, float eta1, float phi1, float m1, float pt2, float eta2, float phi2, float m2, float pt3, float eta3, float phi3, float m3, float mZ1, float met, float metphi) 
{
    if (abs(mZ1 - mass_2(pt1,eta1,phi1,m1,pt2,eta2,phi2,m2)) < 0.01) return mt_2(pt3,phi3,met,metphi);
    if (abs(mZ1 - mass_2(pt1,eta1,phi1,m1,pt3,eta3,phi3,m3)) < 0.01) return mt_2(pt2,phi2,met,metphi);
    if (abs(mZ1 - mass_2(pt2,eta2,phi2,m2,pt3,eta3,phi3,m3)) < 0.01) return mt_2(pt1,phi1,met,metphi);
    return 0;
}

float u1_2(float met_pt, float met_phi, float ref_pt, float ref_phi) 
{
    float met_px = met_pt*std::cos(met_phi), met_py = met_pt*std::sin(met_phi);
    float ref_px = ref_pt*std::cos(ref_phi), ref_py = ref_pt*std::sin(ref_phi);
    float ux = - met_px + ref_px, uy = - met_px + ref_px;
    return (ux*ref_px + uy*ref_py)/ref_pt;
}
float u2_2(float met_pt, float met_phi, float ref_pt, float ref_phi)
{
    float met_px = met_pt*std::cos(met_phi), met_py = met_pt*std::sin(met_phi);
    float ref_px = ref_pt*std::cos(ref_phi), ref_py = ref_pt*std::sin(ref_phi);
    float ux = - met_px + ref_px, uy = - met_px + ref_px;
    return (ux*ref_py - uy*ref_px)/ref_pt;
}

// reconstructs a top from lepton, met, b-jet, applying the W mass constraint and taking the smallest neutrino pZ
float mtop_lvb(float ptl, float etal, float phil, float ml, float met, float metphi, float ptb, float etab, float phib, float mb) 
{
    typedef ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double> > PtEtaPhiMVector;
    typedef ROOT::Math::LorentzVector<ROOT::Math::PxPyPzM4D<double> > PxPyPzMVector;
    PtEtaPhiMVector p4l(ptl,etal,phil,ml);
    PtEtaPhiMVector p4b(ptb,etab,phib,mb);
    double MW=80.4;
    double a = (1 - std::pow(p4l.Z()/p4l.E(), 2));
    double ppe    = met * ptl * std::cos(phil - metphi)/p4l.E();
    double brk    = MW*MW / (2*p4l.E()) + ppe;
    double b      = (p4l.Z()/p4l.E()) * brk;
    double c      = met*met - brk*brk;
    double delta   = b*b - a*c;
    double sqdelta = delta > 0 ? std::sqrt(delta) : 0;
    double pz1 = (b + sqdelta)/a, pz2 = (b - sqdelta)/a;
    double pznu = (abs(pz1) <= abs(pz2) ? pz1 : pz2);
    PxPyPzMVector p4v(met*std::cos(metphi),met*std::sin(metphi),pznu,0);
    return (p4l+p4b+p4v).M();
}

float DPhi_CMLep_Zboost(float l_pt, float l_eta, float l_phi, float l_M, float l_other_pt, float l_other_eta, float l_other_phi, float l_other_M){
  typedef ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double> > PtEtaPhiMVector;
  PtEtaPhiMVector l1(l_pt,l_eta,l_phi,l_M);
  PtEtaPhiMVector l2(l_other_pt,l_other_eta,l_other_phi,l_other_M);
  PtEtaPhiMVector Z = l1+l2;
  ROOT::Math::Boost boost(Z.BoostToCM());
  l1 = boost*l1;
  return deltaPhi(l1.Phi(),Z.Phi());
}

float relax_cut_in_eta_bins(float val, float eta, float eta1, float eta2, float eta3, float val1, float val2, float val3, float val1t, float val2t, float val3t){

// Return a new value of val (variable on which a cut is applied), in such a way that the thresholds (val1,val2,val3)
// initially valid in regions of abs(eta)<(eta1,eta2,eta3) become effectively (val1t,val2t,val3t).
// The cut must be of the form val>=valN, and the condition valNt>valN must hold.

  if (abs(eta)<eta1){
    if (val>=val1) return val1t;
  }
  else if (abs(eta)<eta2){
    if (val>=val2) return val2t;
  }
  else if (abs(eta)<eta3){
    if (val>=val3) return val3t;
  }
  return val;

}



//PU weights

#include <assert.h>
#include "TH2F.h"
#include "TH1F.h"
#include "TFile.h"

// for json up to 276811 (12.9/fb), pu true reweighting
float _puw2016_nTrueInt_13fb[60] = {0.0004627598152210959, 0.014334910915287028, 0.01754727657726197, 0.03181477917631854, 0.046128282569231016, 0.03929080994013006, 0.057066019809589925, 0.19570744862221007, 0.3720256062526554, 0.6440076202772811, 0.9218024454406528, 1.246743510634073, 1.5292543296414058, 1.6670061646418215, 1.7390553377117133, 1.6114721876895595, 1.4177294439817985, 1.420132866045718, 1.3157656415540477, 1.3365188060918483, 1.1191478126677334, 0.9731079434848392, 0.9219564145009487, 0.8811793391804676, 0.7627315352977334, 0.7265186492688713, 0.558602385324645, 0.4805954159733825, 0.34125298049234554, 0.2584848657646724, 0.1819638766151892, 0.12529545619337035, 0.11065705912071645, 0.08587356267495487, 0.09146322371620583, 0.11885517671051576, 0.1952483711863489, 0.23589115679998116, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0};
float puw2016_nTrueInt_13fb(int nTrueInt) { if (nTrueInt<60) return _puw2016_nTrueInt_13fb[nTrueInt]; else return 0; }

// Run2016 E+F+G up to 279931
float _puw2016_nTrueInt_EF[60] = {0.0002476692378524667, 0.014821369430223724, 0.01908474123097549, 0.018774416942744378, 0.027731029726566526, 0.022766323438142735, 0.02112794605705192, 0.015627067131392624, 0.013027012984949482, 0.02664421891070537, 0.105951322567897, 0.2282219493320249, 0.3198539045796174, 0.4472658025206919, 0.6588805154724832, 0.7954191125076755, 0.7971828693076433, 0.8476493223752923, 0.828823661825391, 0.9020575899440882, 0.8251811240056177, 0.8088819151700594, 0.898945222693826, 1.0499718952630142, 1.1569874762934436, 1.4559615822558385, 1.5258279117119538, 1.8409115119643453, 1.8896981359803084, 2.140209911977273, 2.3304811410048387, 2.558753854290941, 3.6974162747530404, 4.798085511876458, 5.7327747190694405, 5.7327747190694405, 5.7327747190694405, 5.7327747190694405, 1.0318994494324993, 1.0318994494324993, 1.0318994494324993, 1.0318994494324993, 1.0318994494324993, 1.0318994494324993, 1.0318994494324993, 1.0318994494324993, 1.0318994494324993, 1.0318994494324993, 1.0318994494324993, 1.0318994494324993, 1.0318994494324993, 1.0318994494324993, 1.0318994494324993, 1.0318994494324993, 1.0318994494324993, 1.0318994494324993, 1.0318994494324993, 1.0318994494324993, 1.0318994494324993, 1.0318994494324993};
float _puw2016_nTrueInt_G_upto279931[60] = {0.0030664708563046326, 0.01123794331581895, 0.016465056588825536, 0.024602832177926543, 0.026107749406095258, 0.019050503081821886, 0.02110161688725923, 0.017694605650846847, 0.016290999589588673, 0.03017245306638949, 0.062201175397462435, 0.21783085244166905, 0.5552753191757233, 0.7214955162768668, 0.7324485837208575, 0.7293440437992165, 0.7146681538266634, 0.7527382158346893, 0.7180480259007131, 0.7910622869835229, 0.7597422022206722, 0.7786794509943739, 0.8873764384591624, 1.0499884204081869, 1.1665585452761693, 1.482186697601494, 1.579761549660652, 1.9529819332323881, 2.053483793295554, 2.356853951860021, 2.5540748462771266, 2.7323308232944745, 3.76828118550158, 4.585241234971839, 5.680781421298886, 5.680781421298886, 5.680781421298886, 5.680781421298886, 1.0225406558337995, 1.0225406558337995, 1.0225406558337995, 1.0225406558337995, 1.0225406558337995, 1.0225406558337995, 1.0225406558337995, 1.0225406558337995, 1.0225406558337995, 1.0225406558337995, 1.0225406558337995, 1.0225406558337995, 1.0225406558337995, 1.0225406558337995, 1.0225406558337995, 1.0225406558337995, 1.0225406558337995, 1.0225406558337995, 1.0225406558337995, 1.0225406558337995, 1.0225406558337995, 1.0225406558337995};
float _puw2016_nTrueInt_EFG_upto279931[60] = {0.0012466094493921048, 0.013160935994534766, 0.01768708902983447, 0.021285749046576714, 0.02682365314703701, 0.020855099389744048, 0.020605061123741098, 0.016225941568981307, 0.014048132697170798, 0.02723810756281671, 0.08766748594327597, 0.2188586889136281, 0.3959226446275465, 0.53375637601322, 0.668298874408685, 0.7522202102811592, 0.7512257707056236, 0.8045384529297095, 0.790321346838139, 0.8694715549669896, 0.80985012101077, 0.8077764909536846, 0.9071025263393598, 1.0638089303658826, 1.17351814974311, 1.478754892106334, 1.5559650574410981, 1.8900984223481412, 1.9531327854179075, 2.2173732038373344, 2.402868150348858, 2.6038209490463284, 3.685234828496249, 4.657038942103952, 5.7091311002033045, 5.7091311002033045, 5.7091311002033045, 5.7091311002033045, 1.0276435980365948, 1.0276435980365948, 1.0276435980365948, 1.0276435980365948, 1.0276435980365948, 1.0276435980365948, 1.0276435980365948, 1.0276435980365948, 1.0276435980365948, 1.0276435980365948, 1.0276435980365948, 1.0276435980365948, 1.0276435980365948, 1.0276435980365948, 1.0276435980365948, 1.0276435980365948, 1.0276435980365948, 1.0276435980365948, 1.0276435980365948, 1.0276435980365948, 1.0276435980365948, 1.0276435980365948};
float puw2016_nTrueInt_EF(int nTrueInt) { if (nTrueInt<60) return _puw2016_nTrueInt_EF[nTrueInt]; else return 0; }
float puw2016_nTrueInt_G_upto279931(int nTrueInt) { if (nTrueInt<60) return _puw2016_nTrueInt_G_upto279931[nTrueInt]; else return 0; }
float puw2016_nTrueInt_EFG_upto279931(int nTrueInt) { if (nTrueInt<60) return _puw2016_nTrueInt_EFG_upto279931[nTrueInt]; else return 0; }

//
//float puwMu8(int nVert) { return _puw_Mu8[nVert] * 0.001; }
//float puwMu17(int nVert) { return _puw_Mu17[nVert] * (2305428/29339.)*0.002/2.26; }

TFile* puw2016_ICHEP = NULL;
TFile* puw2016_ICHEP_Up = NULL;
TFile* puw2016_ICHEP_Dn = NULL;
TH1F* _puw2016_nInt_ICHEP = NULL;
TH1F* _puw2016_nInt_ICHEP_Up = NULL;
TH1F* _puw2016_nInt_ICHEP_Dn = NULL;
float puw2016_nInt_ICHEP(float nInt, int var=0) { 
  
  if (var==0) { 
    if (!_puw2016_nInt_ICHEP){ 
      puw2016_ICHEP = new TFile(CMSSW_BASE+"/src/CMGTools/TTHAnalysis/data/pileup/puWeights_12fb_63mb.root", "read");
      _puw2016_nInt_ICHEP = (TH1F*) (puw2016_ICHEP->Get("puw"));
    }
    return _puw2016_nInt_ICHEP->GetBinContent(_puw2016_nInt_ICHEP->FindBin(nInt));
  }
  else if (var==1) { 
    if (!puw2016_ICHEP_Up) {
      puw2016_ICHEP_Up = new TFile(CMSSW_BASE+"/src/CMGTools/TTHAnalysis/data/pileup/puWeights_12fb_63mb_Up.root", "read");
      _puw2016_nInt_ICHEP_Up = (TH1F*) (puw2016_ICHEP_Up->Get("puw"));
    }
    return _puw2016_nInt_ICHEP_Up->GetBinContent(_puw2016_nInt_ICHEP_Up->FindBin(nInt));
  }
  else if (var==-1) {
    if (!puw2016_ICHEP_Dn) {
      puw2016_ICHEP_Dn = new TFile(CMSSW_BASE+"/src/CMGTools/TTHAnalysis/data/pileup/puWeights_12fb_63mb_Down.root", "read");
      _puw2016_nInt_ICHEP_Dn = (TH1F*) (puw2016_ICHEP_Dn->Get("puw"));
    }
    return _puw2016_nInt_ICHEP_Dn->GetBinContent(_puw2016_nInt_ICHEP_Dn->FindBin(nInt));
  }
  cout <<"[WARNING!!!]  don't know what to do with PUweight, please check!! ";
  return -9999.;
}

TFile *_file_recoToLoose_leptonSF_mu1_b = NULL;
TFile *_file_recoToLoose_leptonSF_mu1_e = NULL;
TFile *_file_recoToLoose_leptonSF_mu2 = NULL;
TFile *_file_recoToLoose_leptonSF_mu3 = NULL;
TGraphAsymmErrors *_histo_recoToLoose_leptonSF_mu1_b = NULL;
TGraphAsymmErrors *_histo_recoToLoose_leptonSF_mu1_e = NULL;
TH2F *_histo_recoToLoose_leptonSF_mu2 = NULL;
TGraphAsymmErrors *_histo_recoToLoose_leptonSF_mu3 = NULL;
TFile *_file_recoToLoose_leptonSF_el = NULL;
TH2F *_histo_recoToLoose_leptonSF_el1 = NULL;
TH2F *_histo_recoToLoose_leptonSF_el2 = NULL;
TH2F *_histo_recoToLoose_leptonSF_el3 = NULL;
TFile *_file_recoToLoose_leptonSF_gsf = NULL;
TH2F *_histo_recoToLoose_leptonSF_gsf = NULL;

float _get_recoToLoose_leptonSF_ttH(int pdgid, float pt, float eta, int nlep, float var){

  if (var!=0 && abs(pdgid)!=11) assert(0); // NOT IMPLEMENTED

  if (!_histo_recoToLoose_leptonSF_mu1_b) {
    _file_recoToLoose_leptonSF_mu1_b = new TFile("../../data/leptonSF/mu_ttH_presel_barrel.root","read");
    _file_recoToLoose_leptonSF_mu1_e = new TFile("../../data/leptonSF/mu_ttH_presel_endcap.root","read");
    _file_recoToLoose_leptonSF_mu2 = new TFile("../../data/leptonSF/MuonID_Z_RunBCD_prompt80X_7p65_looseID.root","read");
    _file_recoToLoose_leptonSF_mu3 = new TFile("../../data/leptonSF/ratios_HIP_trkEff.root","read");
    _histo_recoToLoose_leptonSF_mu1_b = (TGraphAsymmErrors*)(_file_recoToLoose_leptonSF_mu1_b->Get("ratio"));
    _histo_recoToLoose_leptonSF_mu1_e = (TGraphAsymmErrors*)(_file_recoToLoose_leptonSF_mu1_e->Get("ratio"));
    _histo_recoToLoose_leptonSF_mu2 = (TH2F*)(_file_recoToLoose_leptonSF_mu2->Get("pt_abseta_ratio_MC_NUM_LooseID_DEN_genTracks_PAR_pt_spliteta_bin1"));
    _histo_recoToLoose_leptonSF_mu3 = (TGraphAsymmErrors*)(_file_recoToLoose_leptonSF_mu3->Get("ratio_eta"));
  }
  if (!_histo_recoToLoose_leptonSF_el1) {
    _file_recoToLoose_leptonSF_el = new TFile("../../data/leptonSF/el_scaleFactors_20160724.root","read");
    _histo_recoToLoose_leptonSF_el1 = (TH2F*)(_file_recoToLoose_leptonSF_el->Get("GsfElectronToFOID2D"));
    _histo_recoToLoose_leptonSF_el2 = (TH2F*)(_file_recoToLoose_leptonSF_el->Get("MVAVLooseElectronToMini4"));
    _histo_recoToLoose_leptonSF_el3 = (TH2F*)(_file_recoToLoose_leptonSF_el->Get("MVAVLooseElectronToConvIHit1"));
  }
  if (!_histo_recoToLoose_leptonSF_gsf) {
    _file_recoToLoose_leptonSF_gsf = new TFile("../../data/leptonSF/el_scaleFactors_gsf.root","read");
    _histo_recoToLoose_leptonSF_gsf = (TH2F*)(_file_recoToLoose_leptonSF_gsf->Get("EGamma_SF2D"));
  }

  if (abs(pdgid)==13){

    TGraphAsymmErrors *hist1 = (fabs(eta)<1.2) ? _histo_recoToLoose_leptonSF_mu1_b : _histo_recoToLoose_leptonSF_mu1_e;
    float pt1 = std::max(float(hist1->GetXaxis()->GetXmin()+1e-5), std::min(float(hist1->GetXaxis()->GetXmax()-1e-5), pt));
    float out = hist1->Eval(pt1);

    TH2F *hist = _histo_recoToLoose_leptonSF_mu2;
    int ptbin  = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(pt)));
    int etabin = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(fabs(eta))));
    out *= hist->GetBinContent(ptbin,etabin);

    hist1 = _histo_recoToLoose_leptonSF_mu3;
    float eta1 = std::max(float(hist1->GetXaxis()->GetXmin()+1e-5), std::min(float(hist1->GetXaxis()->GetXmax()-1e-5), eta));
    out *= hist1->Eval(eta1);

    return out;

  }
  if (abs(pdgid)==11){
    TH2F *hist = _histo_recoToLoose_leptonSF_el1;
    int ptbin  = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(pt)));
    int etabin = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(fabs(eta))));
    float out = hist->GetBinContent(ptbin,etabin)+var*hist->GetBinError(ptbin,etabin);
    hist = _histo_recoToLoose_leptonSF_el2;
    ptbin  = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(pt)));
    etabin = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(fabs(eta))));
    out *= hist->GetBinContent(ptbin,etabin)+var*hist->GetBinError(ptbin,etabin);
    hist = _histo_recoToLoose_leptonSF_el3;
    ptbin  = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(pt)));
    etabin = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(fabs(eta))));
    out *= hist->GetBinContent(ptbin,etabin)+var*hist->GetBinError(ptbin,etabin);

    hist = _histo_recoToLoose_leptonSF_gsf;
    etabin = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(eta))); // careful, different convention
    ptbin  = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(pt)));
    out *= hist->GetBinContent(etabin,ptbin);

    return out;
  }

  assert(0);
  return -999;

}

TFile *_file_looseToTight_leptonSF_mu_2lss = NULL;
TH2F *_histo_looseToTight_leptonSF_mu_2lss = NULL;
TFile *_file_looseToTight_leptonSF_el_2lss = NULL;
TH2F *_histo_looseToTight_leptonSF_el_2lss = NULL;
TFile *_file_looseToTight_leptonSF_mu_3l = NULL;
TH2F *_histo_looseToTight_leptonSF_mu_3l = NULL;
TFile *_file_looseToTight_leptonSF_el_3l = NULL;
TH2F *_histo_looseToTight_leptonSF_el_3l = NULL;

float _get_looseToTight_leptonSF_ttH(int pdgid, float pt, float eta, int nlep, float var){

  if (var!=0) assert(0); // NOT IMPLEMENTED

  if (!_histo_looseToTight_leptonSF_mu_2lss) {
    _file_looseToTight_leptonSF_mu_2lss = new TFile("../../data/lepMVAEffSF_m_2lss.root","read");
    _histo_looseToTight_leptonSF_mu_2lss = (TH2F*)(_file_looseToTight_leptonSF_mu_2lss->Get("sf"));
  }
  if (!_histo_looseToTight_leptonSF_el_2lss) {
    _file_looseToTight_leptonSF_el_2lss = new TFile("../../data/lepMVAEffSF_e_2lss.root","read");
    _histo_looseToTight_leptonSF_el_2lss = (TH2F*)(_file_looseToTight_leptonSF_el_2lss->Get("sf"));
  }
  if (!_histo_looseToTight_leptonSF_mu_3l) {
    _file_looseToTight_leptonSF_mu_3l = new TFile("../../data/lepMVAEffSF_m_3l.root","read");
    _histo_looseToTight_leptonSF_mu_3l = (TH2F*)(_file_looseToTight_leptonSF_mu_3l->Get("sf"));
  }
  if (!_histo_looseToTight_leptonSF_el_3l) {
    _file_looseToTight_leptonSF_el_3l = new TFile("../../data/lepMVAEffSF_e_3l.root","read");
    _histo_looseToTight_leptonSF_el_3l = (TH2F*)(_file_looseToTight_leptonSF_el_3l->Get("sf"));
  }

  TH2F *hist = 0;
  if (abs(pdgid)==13) hist = (nlep>2) ? _histo_looseToTight_leptonSF_mu_3l : _histo_looseToTight_leptonSF_mu_2lss;
  else if (abs(pdgid)==11) hist = (nlep>2) ? _histo_looseToTight_leptonSF_el_3l : _histo_looseToTight_leptonSF_el_2lss;
  assert(hist);
  int ptbin  = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(pt)));
  int etabin = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(fabs(eta))));
  return hist->GetBinContent(ptbin,etabin);

}

float leptonSF_ttH(int pdgid, float pt, float eta, int nlep, float var=0){

  float recoToLoose = _get_recoToLoose_leptonSF_ttH(pdgid,pt,eta,nlep,var);
  float looseToTight = _get_looseToTight_leptonSF_ttH(pdgid,pt,eta,nlep,var);
  float res = recoToLoose*looseToTight;
  assert (res>0);
  return res;

}

TFile *file_triggerSF_ttH = NULL;
TH2Poly* t2poly_triggerSF_ttH_mm = NULL;
TH2Poly* t2poly_triggerSF_ttH_ee = NULL;
TH2Poly* t2poly_triggerSF_ttH_em = NULL;
TH2Poly* t2poly_triggerSF_ttH_3l = NULL;

float triggerSF_ttH(int pdgid1, float pt1, int pdgid2, float pt2, int nlep, float var=0){
  if (!file_triggerSF_ttH) {
    file_triggerSF_ttH = new TFile("../../data/triggerSF/trig_eff_map_v4.root");
    t2poly_triggerSF_ttH_mm = (TH2Poly*)(file_triggerSF_ttH->Get("SSuu2DPt_effic"));
    t2poly_triggerSF_ttH_ee = (TH2Poly*)(file_triggerSF_ttH->Get("SSee2DPt__effic"));
    t2poly_triggerSF_ttH_em = (TH2Poly*)(file_triggerSF_ttH->Get("SSeu2DPt_effic"));
    t2poly_triggerSF_ttH_3l = (TH2Poly*)(file_triggerSF_ttH->Get("__3l2DPt_effic"));
    if (!(t2poly_triggerSF_ttH_mm && t2poly_triggerSF_ttH_ee && t2poly_triggerSF_ttH_em && t2poly_triggerSF_ttH_3l)) {
	std::cout << "Impossible to load trigger scale factors!" << std::endl;
	file_triggerSF_ttH->ls();
	file_triggerSF_ttH = NULL;
      }
  }
  TH2Poly* hist = NULL;
  if (nlep==2){
    if (abs(pdgid1)==13 && abs(pdgid2)==13) hist = t2poly_triggerSF_ttH_mm;
    else if (abs(pdgid1)==11 && abs(pdgid2)==11) hist = t2poly_triggerSF_ttH_ee;
    else hist = t2poly_triggerSF_ttH_em;
  }
  else if (nlep==3) hist = t2poly_triggerSF_ttH_3l;
  else std::cout << "Wrong options to trigger scale factors" << std::endl;
  pt1 = std::max(float(hist->GetXaxis()->GetXmin()+1e-5), std::min(float(hist->GetXaxis()->GetXmax()-1e-5), pt1));
  pt2 = std::max(float(hist->GetYaxis()->GetXmin()+1e-5), std::min(float(hist->GetYaxis()->GetXmax()-1e-5), pt2));
  int bin = hist->FindBin(pt1,pt2);
  float eff = hist->GetBinContent(bin) + var * hist->GetBinError(bin);

  if (nlep>2) return eff;
  int cat = (abs(pdgid1)==11) + (abs(pdgid2)==11);
  if (cat==2) return eff*1.02;
  else if (cat==1) return eff*1.02;
  else return eff*1.01;


}

float mass_3_cheap(float pt1, float eta1, float pt2, float eta2, float phi2, float pt3, float eta3, float phi3) {
    typedef ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double> > PtEtaPhiMVector;
    PtEtaPhiMVector p41(pt1,eta1,0,   0.0);
    PtEtaPhiMVector p42(pt2,eta2,phi2,0.0);
    PtEtaPhiMVector p43(pt3,eta3,phi3,0.0);
    return (p41+p42+p43).M();
}




//#include "TGraphAsymmErrors.h"
//TFile *_file_reco_leptonSF_mu = NULL;
//TFile *_file_recoToMedium_leptonSF_mu = NULL;
//TFile *_file_MediumToMVA_leptonSF_mu = NULL;
//TFile *_file_recoToMVA_leptonSF_el = NULL;
//TFile *_file_reco_leptonSF_el = NULL;
//
//TGraphAsymmErrors *_histo_reco_leptonSF_mu = NULL;
//TH2F *_histo_recoToMedium_leptonSF_mu = NULL;
//TH2F *_histo_MediumToMVA_leptonSF_mu = NULL;
//TH2F *_histo_recoToMVA_leptonSF_el = NULL;
//TH2F *_histo_reco_leptonSF_el = NULL;
//
//float getLeptonSF_mu_Unc(float pt, int var) {
//  if (pt<20) 
//    return var*TMath::Sqrt(0.03*0.03+0.01*0.01+0.01*0.01);
//  else 
//    return var*TMath::Sqrt(0.02*0.02+0.01*0.01);  
//}
//float leptonSF_2lss_ewk(int pdgid, float pt, float eta, int var=0){
//  
//  if (!_histo_reco_leptonSF_mu) {
//     _file_reco_leptonSF_mu = new TFile(CMSSW_BASE+"/src/CMGTools/TTHAnalysis/data/leptonSF/SF2016_muon_trackingEff.root", "data");
//     _file_recoToMedium_leptonSF_mu = new TFile(CMSSW_BASE+"/src/CMGTools/TTHAnalysis/data/leptonSF/SF2016_muon_mediumId.root", "read");
//     _file_MediumToMVA_leptonSF_mu = new TFile(CMSSW_BASE+"/src/CMGTools/TTHAnalysis/data/leptonSF/SF2016_muon_lepMVAveryTight.root", "read");
//     _histo_reco_leptonSF_mu = (TGraphAsymmErrors*)(_file_reco_leptonSF_mu->Get("ratio_eta"));
//     _histo_recoToMedium_leptonSF_mu = (TH2F*)(_file_recoToMedium_leptonSF_mu->Get("pt_abseta_PLOT_pair_probeMultiplicity_bin0"));
//     _histo_MediumToMVA_leptonSF_mu = (TH2F*)(_file_MediumToMVA_leptonSF_mu->Get("pt_abseta_PLOT_pair_probeMultiplicity_bin0_&_tag_combRelIsoPF04dBeta_bin0_&_tag_pt_bin0_&_mvaPreSel_pass"));
//   }
//   if (!_histo_recoToMVA_leptonSF_el) {
//     _file_recoToMVA_leptonSF_el = new TFile(CMSSW_BASE+"/src/CMGTools/TTHAnalysis/data/leptonSF/SF2016_electron_full.root", "read");
//     _histo_recoToMVA_leptonSF_el = (TH2F*)(_file_recoToMVA_leptonSF_el->Get("GsfElectronToLeptonMvaVTIDEmuTightIP2DSIP3D8miniIso04"));
//     
//     _file_reco_leptonSF_el = new TFile(CMSSW_BASE+"/src/CMGTools/TTHAnalysis/data/leptonSF/SF2016_electron_trackingEff.root", "read");
//     _histo_reco_leptonSF_el = (TH2F*) (_file_reco_leptonSF_el->Get("EGamma_SF2D"));
//   }
//   float out = 0.;
//   if (abs(pdgid)==13){
//     out = _histo_reco_leptonSF_mu->Eval(eta);
//     TH2F *hist = _histo_recoToMedium_leptonSF_mu;
//     int ptbin  = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(pt)));
//     int etabin = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(fabs(eta))));
//     out *= hist->GetBinContent(ptbin,etabin);
//     hist = _histo_MediumToMVA_leptonSF_mu;
//     ptbin  = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(pt)));
//     etabin = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(fabs(eta))));
//     out *=hist->GetBinContent(ptbin,etabin);
//     return out + out*getLeptonSF_mu_Unc(pt,var);
//   }
//   float err = 0.;
//   if (abs(pdgid)==11){
//     TH2F *hist = _histo_recoToMVA_leptonSF_el;
//     int ptbin  = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(pt)));
//     int etabin = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(fabs(eta))));
//     out = hist->GetBinContent(ptbin,etabin);
//     err = hist->GetBinError(ptbin,etabin)*hist->GetBinError(ptbin,etabin);
//     hist = _histo_reco_leptonSF_el;
//     ptbin  = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(pt)));
//     etabin = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(eta)));
//     out *= hist->GetBinContent(etabin,ptbin);
//     err += hist->GetBinError(etabin,ptbin)*hist->GetBinError(etabin,ptbin);
//     err = TMath::Sqrt(err);
//     return out + out*err*var;
//   }
//   //cout << "[ERROR]!!!! SF UnKNOWN!!! PLEASE CHECK" << endl;
//   return 1.;
// }
//
//
//
//TFile* trigSF = NULL; 
//TH2F* _trigSF_2l_m = NULL;
//TH2F* _trigSF_2l_e = NULL;
//
//float triggerSF_2lss_ewk(float pt1, float pt2, int pdg2){
//  // Lesya's mail:
//  // - split for trailing ele or trailing mu
//  // - 3l: subleading vs trailing lepton pt (1l + 2l triggers)
//  // - 2l: leading light lepton vs subleading light lepton ==> good for both 2l+tau and 2lSS cases (1l + 2l triggers)
//  // - l+tautau: use flat 86% everywhere; pt_e > 35 GeV; pt_mu > 25 GeV (1l + l/tau triggers) 
//  if (!_trigSF_2l_m) { 
//    trigSF = new TFile(CMSSW_BASE+"/src/CMGTools/TTHAnalysis/data/triggerSF/EWKino_9p2_triggerSF.root", "read");
//    _trigSF_2l_m = (TH2F*) trigSF->Get("eff_2l_mu" );
//    _trigSF_2l_e = (TH2F*) trigSF->Get("eff_2l_ele");
//  }
//  // 2l
//  TH2F* hist = (pdg2 == 13)?_trigSF_2l_m:_trigSF_2l_e;
//  int xbin = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(pt1)));
//  int ybin = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(pt2)));
//  //  cout << pt1 << " " << pt2 << " " << xbin << " " << ybin << " " << hist->GetBinContent(xbin,ybin) << endl;
//  return hist->GetBinContent(xbin,ybin);
//}
//
//#include "TGraphAsymmErrors.h"
//TFile *_file_reco_leptonSF_mu = NULL;
//TFile *_file_recoToMedium_leptonSF_mu = NULL;
//TFile *_file_MediumToMVA_leptonSF_mu = NULL;
//TFile *_file_recoToMVA_leptonSF_el = NULL;
//TFile *_file_reco_leptonSF_el = NULL;
//
//TGraphAsymmErrors *_histo_reco_leptonSF_mu = NULL;
//TH2F *_histo_recoToMedium_leptonSF_mu = NULL;
//TH2F *_histo_MediumToMVA_leptonSF_mu = NULL;
//TH2F *_histo_recoToMVA_leptonSF_el = NULL;
//TH2F *_histo_reco_leptonSF_el = NULL;
//
//float getLeptonSF_mu_Unc(float pt, int var) {
//  if (pt<20) 
//    return var*TMath::Sqrt(0.03*0.03+0.01*0.01+0.01*0.01);
//  else 
//    return var*TMath::Sqrt(0.02*0.02+0.01*0.01);  
//}
//float leptonSF_2lss_ewk(int pdgid, float pt, float eta, int var=0){
//  
//  if (!_histo_reco_leptonSF_mu) {
//     _file_reco_leptonSF_mu = new TFile(CMSSW_BASE+"/src/CMGTools/TTHAnalysis/data/leptonSF/sf_mu_trk_susy_ICHEP.root","read");
//     _file_recoToMedium_leptonSF_mu = new TFile(CMSSW_BASE+"/src/CMGTools/TTHAnalysis/data/leptonSF/sf_mu_Medium_susy_ICHEP.root","read");
//     _file_MediumToMVA_leptonSF_mu = new TFile(CMSSW_BASE+"/src/CMGTools/TTHAnalysis/data/leptonSF/sf_mu_MVAVT_susy_ICHEP.root","read");
//     _histo_reco_leptonSF_mu = (TGraphAsymmErrors*)(_file_reco_leptonSF_mu->Get("ratio_eta"));
//     _histo_recoToMedium_leptonSF_mu = (TH2F*)(_file_recoToMedium_leptonSF_mu->Get("pt_abseta_PLOT_pair_probeMultiplicity_bin0"));
//     _histo_MediumToMVA_leptonSF_mu = (TH2F*)(_file_MediumToMVA_leptonSF_mu->Get("pt_abseta_PLOT_pair_probeMultiplicity_bin0_&_tag_combRelIsoPF04dBeta_bin0_&_tag_pt_bin0_&_mvaPreSel_pass"));
//   }
//   if (!_histo_recoToMVA_leptonSF_el) {
//     _file_recoToMVA_leptonSF_el = new TFile(CMSSW_BASE+"/src/CMGTools/TTHAnalysis/data/leptonSF/sf_el_susy_ICHEP.root","read");
//     _histo_recoToMVA_leptonSF_el = (TH2F*)(_file_recoToMVA_leptonSF_el->Get("GsfElectronToLeptonMvaVTIDEmuTightIP2DSIP3D8miniIso04"));
//     
//     _file_reco_leptonSF_el = new TFile(CMSSW_BASE+"/src/CMGTools/TTHAnalysis/data/leptonSF/sf_el_trk_susy_ICHEP.root","read");
//     _histo_reco_leptonSF_el = (TH2F*) (_file_reco_leptonSF_el->Get("EGamma_SF2D"));
//   }
//   float out = 0.;
//   if (abs(pdgid)==13){
//     out = _histo_reco_leptonSF_mu->Eval(eta);
//     TH2F *hist = _histo_recoToMedium_leptonSF_mu;
//     int ptbin  = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(pt)));
//     int etabin = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(fabs(eta))));
//     out *= hist->GetBinContent(ptbin,etabin);
//     hist = _histo_MediumToMVA_leptonSF_mu;
//     ptbin  = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(pt)));
//     etabin = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(fabs(eta))));
//     out *=hist->GetBinContent(ptbin,etabin);
//     return out + out*getLeptonSF_mu_Unc(pt,var);
//   }
//   float err = 0.;
//   if (abs(pdgid)==11){
//     TH2F *hist = _histo_recoToMVA_leptonSF_el;
//     int ptbin  = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(pt)));
//     int etabin = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(fabs(eta))));
//     out = hist->GetBinContent(ptbin,etabin);
//     err = hist->GetBinError(ptbin,etabin)*hist->GetBinError(ptbin,etabin);
//     hist = _histo_reco_leptonSF_el;
//     ptbin  = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(pt)));
//     etabin = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(eta)));
//     out *= hist->GetBinContent(etabin,ptbin);
//     err += hist->GetBinError(etabin,ptbin)*hist->GetBinError(etabin,ptbin);
//     err = TMath::Sqrt(err);
//     return out + out*err*var;
//   }
//   cout << "[ERROR]!!!! SF UnKNOWN!!! PLEASE CHECK" << endl;
//   return 1.;
// }



void functions() {}





