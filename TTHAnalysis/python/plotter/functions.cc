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

// May 2016: This is func which takes the 4vectors of MET, L1,L2 and reconstructs 2 taus and returns the effective Z(-->tautau) mass.                                                                                       

float mass_tautau( float Met_Pt, float Met_Phi,  float l1_Pt, float l1_Eta, float l1_Phi, float l2_Pt, float l2_Eta, float l2_Phi ) {
  typedef ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double> > PtEtaPhiMVector;
  typedef ROOT::Math::LorentzVector<ROOT::Math::PxPyPzM4D<double>   > PxPyPzMVector;
  PtEtaPhiMVector Met( Met_Pt, 0.     , Met_Phi , 0.   );
  PtEtaPhiMVector L1(  l1_Pt , l1_Eta , l1_Phi  , 0.106 );
  PtEtaPhiMVector L2(  l2_Pt , l2_Eta , l2_Phi  , 0.106 );   // 0.106 mu mass                                                                                                                                                 
  float A00,A01,A10,A11,  C0,C1,  X0,X1,  inv_det;     // Define A:2x2 matrix, C,X 2x1 vectors & det[A]^-1                                                                                                                    
  inv_det = 1./( L1.Px()*L2.Py() - L2.Px()*L1.Py() );
  A00 = inv_det*L2.Py();     A01 =-inv_det*L2.Px();
  A10 =-inv_det*L1.Py();     A11 = inv_det*L1.Px();
  C0  = (Met+L1+L2).Px();    C1  = (Met+L1+L2).Py();
  X0  = A00*C0 + A01*C1;     X1  = A10*C0 + A11*C1;
  PxPyPzMVector T1( L1.Px()*X0 , L1.Py()*X0 , L1.Pz()*X0 , 1.777 );    // 1.777 tau mass                                                                                                                                      
  PxPyPzMVector T2( L2.Px()*X1 , L2.Py()*X1 , L2.Pz()*X1 , 1.777 );
  if(X0>0.&&X1>0.)return  (T1+T2).M();
  else            return -(T1+T2).M();
}

// SOS stuff

int SR_bins_EWKino(float Mll){
  if     (4.<Mll && Mll<9.5) return 1;
  else if(10.5<Mll && Mll<=20.) return 2;
  else if(20.<Mll && Mll<=30.) return 3;
  else if(30.<Mll) return 4;
  else return -99;
}

int SR_bins_stop(float ptlep1){
  if     (ptlep1 <=12.) return 1;
  else if(ptlep1 >12. && ptlep1 <=20.) return 2;
  else if(ptlep1 >20.) return 3; 
  else return -99;
}


float metmm_pt(int pdg1, float pt1, float phi1, int pdg2, float pt2, float phi2, float metpt, float metphi) {
  if (abs(pdg1)==13 && abs(pdg2)==13) return pt_3(pt1,phi1,pt2,phi2,metpt,metphi);
  else if (abs(pdg1)==13 && !(abs(pdg2)==13)) return pt_2(pt1,phi1,metpt,metphi);
  else if (!(abs(pdg1)==13) && abs(pdg2)==13) return pt_2(pt2,phi2,metpt,metphi);
  else if (!(abs(pdg1)==13) && !(abs(pdg2)==13)) return metpt;
  else return -99;
}



float eleWPVVL(float pt, float etaSc, float mva){
  if (pt<=10 && ((abs(etaSc)<0.8 && mva>-0.265) || (abs(etaSc)>=0.8 && abs(etaSc)<1.479 && mva > -0.556) || (abs(etaSc)>=1.479 && mva>-0.6))) return 1;
  else if (pt>10 && ((abs(etaSc)<0.8 && mva > 0.87) || (abs(etaSc)>=0.8 && abs(etaSc)<1.479 && mva > 0.30) || (abs(etaSc)>=1.479 && mva >-0.30))) return 1;
  else return 0;
}


float eleWPT(float pt, float etaSc, float mva){
  if (pt<=10 && ((abs(etaSc)<0.8 && mva>-0.265) || (abs(etaSc)>=0.8 && abs(etaSc)<1.479 && mva > -0.556) || (abs(etaSc)>=1.479 && mva>-0.551))) return 1;
  else if (pt>10 && ((abs(etaSc)<0.8 && mva > 0.87) || (abs(etaSc)>=0.8 && abs(etaSc)<1.479 && mva > 0.60) || (abs(etaSc)>=1.479 && mva >0.17))) return 1;
  else return 0;
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

int regroupSignalRegions_RA5(int SR){

  int rgr[66+1];
  rgr[0]=0; //unused
  if (SR<1 || SR>66) return 0;

  // HH
  rgr[1]=1;
  rgr[2]=2;
  rgr[3]=3;
  rgr[4]=4;
  rgr[5]=5;
  rgr[6]=5;
  rgr[7]=5;
  rgr[8]=5;
  rgr[9]=6;
  rgr[10]=7;
  rgr[11]=8;
  rgr[12]=9;
  rgr[13]=10;
  rgr[14]=10;
  rgr[15]=10;
  rgr[16]=10;
  rgr[17]=11;
  rgr[18]=12;
  rgr[19]=13;
  rgr[20]=14;
  rgr[21]=15;
  rgr[22]=15;
  rgr[23]=15;
  rgr[24]=15;
  rgr[25]=16;
  rgr[26]=16;
  rgr[27]=16;
  rgr[28]=16;
  rgr[29]=16;
  rgr[30]=16;
  rgr[31]=17;
  rgr[32]=18;

  // HL
  rgr[32+1]=18+1;
  rgr[32+2]=18+2;
  rgr[32+3]=18+3;
  rgr[32+4]=18+4;
  rgr[32+5]=18+4;
  rgr[32+6]=18+4;
  rgr[32+7]=18+5;
  rgr[32+8]=18+6;
  rgr[32+9]=18+7;
  rgr[32+10]=18+8;
  rgr[32+11]=18+8;
  rgr[32+12]=18+8;
  rgr[32+13]=18+9;
  rgr[32+14]=18+10;
  rgr[32+15]=18+11;
  rgr[32+16]=18+12;
  rgr[32+17]=18+12;
  rgr[32+18]=18+12;
  rgr[32+19]=18+13;
  rgr[32+20]=18+13;
  rgr[32+21]=18+13;
  rgr[32+22]=18+13;
  rgr[32+23]=18+14;
  rgr[32+24]=18+14;
  rgr[32+25]=18+14;
  rgr[32+26]=18+15;

  // LL (UCSx proposal)
  rgr[58+1]=18+15+1;
  rgr[58+2]=18+15+2;
  rgr[58+3]=18+15+1;
  rgr[58+4]=18+15+2;
  rgr[58+5]=18+15+3;
  rgr[58+6]=18+15+3;
  rgr[58+7]=18+15+3;
  rgr[58+8]=18+15+3;

  return rgr[SR]; // between 1 and 36

}

int SR_ewk_ss2l(int nj, float ptl1, float phil1, float ptl2, float phil2, float met, float metphi){
  
  float mtw1 = mt_2(ptl1,phil1, met, metphi);
  float mtw2 = mt_2(ptl2,phil2, met, metphi);
  float mtw  = std::min(mtw1,mtw2);
  float ptdil = pt_2(ptl1,phil1,ptl2,phil2);

  // V0 --- LPC version
//V0-LPC  if      (nj==0 && mtw<40 && met>100 && met<200)             return 1;
//V0-LPC  else if (nj==0 && mtw<40 && met>200)                        return 2;
//V0-LPC  else if (nj==0 && mtw>40 && mtw<120 && met>100 && met<200)  return 3;
//V0-LPC  else if (nj==0 && mtw>40 && mtw<120 && met>200)             return 4;
//V0-LPC  else if (nj==0 && mtw>120 && met>100 && met<200)            return 5;
//V0-LPC  else if (nj==0 && mtw>120 && met>200)                       return 6;
//V0-LPC  else if (nj==1 && mtw<40 && met>100 && met<200)             return 7;
//V0-LPC  else if (nj==1 && mtw<40 && met>200)                        return 8;
//V0-LPC  else if (nj==1 && mtw>40 && mtw<120 && met>100 && met<200)  return 9;
//V0-LPC  else if (nj==1 && mtw>40 && mtw<120 && met>200)             return 10;
//V0-LPC  else if (nj==1 && mtw>120 && met>100 && met<200)            return 11;
//V0-LPC  else if (nj==1 && mtw>120 && met>200)                       return 12;

  if      (nj==0 && ptdil<50 && mtw<100 && met<100)            return 1;  //VR
  else if (nj==0 && ptdil<50 && mtw<100 && met>100 && met<150) return 2;
  else if (nj==0 && ptdil<50 && mtw<100 && met>150)            return 3;
  else if (nj==0 && ptdil>50 && mtw<100 && met<100)            return 4; //VR
  else if (nj==0 && ptdil>50 && mtw<100 && met>100 && met<150) return 5;
  else if (nj==0 && ptdil>50 && mtw<100 && met>150)            return 6;
  else if (nj==0 && mtw>100 && met<100)                        return 7;  //VR
  else if (nj==0 && mtw>100 && met>100 && met<150)             return 8;
  else if (nj==0 && mtw>100 && met>150)                        return 9;
  else if (nj==1 && ptdil<50 && mtw<100 && met<100)            return 10;  //VR
  else if (nj==1 && ptdil<50 && mtw<100 && met>100 && met<150) return 11;
  else if (nj==1 && ptdil<50 && mtw<100 && met>150)            return 12;
  else if (nj==1 && ptdil>50 && mtw<100 && met<100)            return 13; //VR
  else if (nj==1 && ptdil>50 && mtw<100 && met>100 && met<150) return 14;
  else if (nj==1 && ptdil>50 && mtw<100 && met>150)            return 15;
  else if (nj==1 && mtw>100 && met<100)                        return 16;  //VR
  else if (nj==1 && mtw>100 && met>100 && met<150)             return 17;
  else if (nj==1 && mtw>100 && met>150)                        return 18;

  return -99;  
  
}


float ttH_MVAto1D_6_2lss_Marco (float kinMVA_2lss_ttbar, float kinMVA_2lss_ttV){

  return 2*((kinMVA_2lss_ttbar>=-0.2)+(kinMVA_2lss_ttbar>=0.3))+(kinMVA_2lss_ttV>=-0.1)+1;

}
float ttH_MVAto1D_3_3l_Marco (float kinMVA_3l_ttbar, float kinMVA_3l_ttV){

  if (kinMVA_3l_ttbar<0.3 && kinMVA_3l_ttV<-0.1) return 1;
  else if (kinMVA_3l_ttbar>=0.3 && kinMVA_3l_ttV>=-0.1) return 3;
  else return 2;

}

#include "ttH-multilepton/binning_2d_thresholds.h"
float ttH_MVAto1D_7_2lss_Marco (float kinMVA_2lss_ttbar, float kinMVA_2lss_ttV){

//________________
//|   |   |   | 7 |
//|   |   | 4 |___|
//| 1 | 2 |___| 6 |
//|   |   |   |___|
//|   |   | 3 | 5 |
//|___|___|___|___|
//

  if (kinMVA_2lss_ttbar<cuts_2lss_ttbar0) return 1;
  else if (kinMVA_2lss_ttbar<cuts_2lss_ttbar1) return 2;
  else if (kinMVA_2lss_ttbar<cuts_2lss_ttbar2) return 3+(kinMVA_2lss_ttV>=cuts_2lss_ttV0);
  else return 5+(kinMVA_2lss_ttV>=cuts_2lss_ttV1)+(kinMVA_2lss_ttV>=cuts_2lss_ttV2);

}
float ttH_MVAto1D_5_3l_Marco (float kinMVA_3l_ttbar, float kinMVA_3l_ttV){

  int reg = 2*((kinMVA_3l_ttbar>=cuts_3l_ttbar1)+(kinMVA_3l_ttbar>=cuts_3l_ttbar2))+(kinMVA_3l_ttV>=cuts_3l_ttV1)+1;
  if (reg==2) reg=1;
  if (reg>2) reg = reg-1;
  return reg;

}



float ttH_MVAto1D_6_flex (float kinMVA_2lss_ttbar, float kinMVA_2lss_ttV, int pdg1, int pdg2, float ttVcut, float ttcut1, float ttcut2){

  return 2*((kinMVA_2lss_ttbar>=ttcut1)+(kinMVA_2lss_ttbar>=ttcut2)) + (kinMVA_2lss_ttV>=ttVcut)+1;

}


int ttH_catIndex_2lss(int nTauTight, int LepGood1_pdgId, int LepGood2_pdgId, int LepGood1_charge, int nBJetMedium25){

//2lss_1tau
//2lss_ee_0tau_neg
//2lss_ee_0tau_pos
//2lss_em_0tau_bl_neg
//2lss_em_0tau_bl_pos
//2lss_em_0tau_bt_neg
//2lss_em_0tau_bt_pos
//2lss_mm_0tau_bl_neg
//2lss_mm_0tau_bl_pos
//2lss_mm_0tau_bt_neg
//2lss_mm_0tau_bt_pos
   
  if (nTauTight>=1) return 1;
  if (nTauTight==0 && abs(LepGood1_pdgId)==11 && abs(LepGood2_pdgId)==11 && LepGood1_charge<0) return 2;
  if (nTauTight==0 && abs(LepGood1_pdgId)==11 && abs(LepGood2_pdgId)==11 && LepGood1_charge>0) return 3;
  if (nTauTight==0 && (abs(LepGood1_pdgId) != abs(LepGood2_pdgId)) && LepGood1_charge<0 && nBJetMedium25 < 2) return 4;
  if (nTauTight==0 && (abs(LepGood1_pdgId) != abs(LepGood2_pdgId)) && LepGood1_charge>0 && nBJetMedium25 < 2) return 5;
  if (nTauTight==0 && (abs(LepGood1_pdgId) != abs(LepGood2_pdgId)) && LepGood1_charge<0 && nBJetMedium25 >= 2) return 6;
  if (nTauTight==0 && (abs(LepGood1_pdgId) != abs(LepGood2_pdgId)) && LepGood1_charge>0 && nBJetMedium25 >= 2) return 7;
  if (nTauTight==0 && abs(LepGood1_pdgId)==13 && abs(LepGood2_pdgId)==13 && LepGood1_charge<0 && nBJetMedium25 < 2) return 8;
  if (nTauTight==0 && abs(LepGood1_pdgId)==13 && abs(LepGood2_pdgId)==13 && LepGood1_charge>0 && nBJetMedium25 < 2) return 9;
  if (nTauTight==0 && abs(LepGood1_pdgId)==13 && abs(LepGood2_pdgId)==13 && LepGood1_charge<0 && nBJetMedium25 >= 2) return 10;
  if (nTauTight==0 && abs(LepGood1_pdgId)==13 && abs(LepGood2_pdgId)==13 && LepGood1_charge>0 && nBJetMedium25 >= 2) return 11;

 return -1;

}

int ttH_catIndex_3l(int LepGood1_charge, int LepGood2_charge, int LepGood3_charge, int nBJetMedium25){

//3l_bl_neg
//3l_bl_pos
//3l_bt_neg
//3l_bt_pos

  if ((LepGood1_charge+LepGood2_charge+LepGood3_charge)<0 && nBJetMedium25 < 2) return 12;
  if ((LepGood1_charge+LepGood2_charge+LepGood3_charge)>0 && nBJetMedium25 < 2) return 13;
  if ((LepGood1_charge+LepGood2_charge+LepGood3_charge)<0 && nBJetMedium25 >= 2) return 14;
  if ((LepGood1_charge+LepGood2_charge+LepGood3_charge)>0 && nBJetMedium25 >= 2) return 15;

 return -1;

}



#include <assert.h>
#include "TH2F.h"
#include "TH1F.h"
#include "TFile.h"



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





