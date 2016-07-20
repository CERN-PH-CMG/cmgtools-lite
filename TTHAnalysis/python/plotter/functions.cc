#include <cmath>
#include "Math/GenVector/LorentzVector.h"
#include "Math/GenVector/PtEtaPhiM4D.h"
#include "Math/GenVector/PxPyPzM4D.h"
#include "Math/GenVector/Boost.h"
#include "TLorentzVector.h"
#include "TH2Poly.h"
#include "PhysicsTools/Heppy/interface/Davismt2.h"

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


// for 74X
//float _puw_true[50] = {3.652322599922302, 3.652322599922302, 3.652322599922302, 3.652322599922302, 3.652322599922302, 3.652322599922302, 2.1737862420968868, 2.7116925849897364, 3.352556070095877, 3.083015137131128, 2.8824218072960823, 2.6791975503716743, 2.212434153800565, 1.5297063638539434, 0.8762698648562287, 0.41326633649647065, 0.17496252648670657, 0.07484562496757297, 0.038507396968229766, 0.021849761893692053, 0.01140425609526747, 0.005063578526248854, 0.001881351382104846, 0.0006306639125313864, 0.00021708627575927402, 9.42187694469501e-05, 5.146591433045169e-05, 3.326854405002371e-05, 2.426063215708668e-05, 1.8575279862433386e-05, 1.281054551977887e-05, 8.01819566777096e-06, 3.6521122159066883e-06, 1.574921039309069e-06, 5.770182058345157e-07, 2.0862027190449754e-07, 6.946502045299735e-08, 2.032077576113469e-08, 6.417943581326451e-09, 1.5934414668326278e-09, 4.311337237072122e-10, 1.1138367777447038e-10, 2.6925919137965106e-11, 8.08827951069873e-12, 1.3708268591386723e-12, 4.065021195897016e-13, 1.770006195676463e-13, 5.689967214903059e-14, 6.224880123134382e-14, 0.0};
//
//float _puw_Mu8[60] = { 1.0, 2.2753238054533287, 2.5087852081376565, 2.547534409862272, 2.5453856677292626, 2.3957671901210302, 2.329888347258754, 2.132632821246379, 1.9294351293836975, 1.6869299027848321, 1.410414475296686, 1.18061883859625, 0.9505511419155187, 0.7455821522790507, 0.5917331920192597, 0.4497875190879285, 0.3529109417225823, 0.26485881058611677, 0.208008048447543, 0.1582531319686015, 0.12944461423876671, 0.10248826819473823, 0.07759715482270031, 0.05888999109148935, 0.059779044174240605, 0.041874820142546565, 0.03324024895102297, 0.039028818938047924, 0.02179308514266076, 0.01197215401539325, 0.009421343447104134, 0.013861014595193729, 0.0, 0.06539755302753723, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0 };
//float _puw_Mu17[60] = { 1.0, 2.6025657030947866, 2.8330872498461876, 2.477197375267561, 2.552415607786326, 2.4047951682107627, 2.3024376807492737, 2.1540414886183843, 1.9518423032680638, 1.699049184347834, 1.4639137707975747, 1.2067661580794682, 0.966660952828535, 0.766250445622546, 0.5938409557059098, 0.4557404537508868, 0.3447511898010737, 0.26427563682379623, 0.2033725709370245, 0.15418157724654288, 0.12117494844707002, 0.09683984946855388, 0.08058574696446474, 0.06008103415479263, 0.049369064099306637, 0.043438226650837304, 0.032177902255824065, 0.029449084226433955, 0.02071379137395143, 0.01793424569381745, 0.013294248051062496, 0.012108360448835863, 0.009083026618738383, 0.0091627022908326, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0 };
//

// for 76X
float _puw_true[50] = {0.5269234785559587, 0.6926695654592266, 1.080004829553802, 1.379105403255213, 1.819531519703243, 2.212948765398841, 1.591693852037577, 1.3246151544739415, 1.332963823519763, 1.252466214103506, 1.1890944076884082, 1.1546479191424708, 1.0968414518989904, 0.9606172752657895, 0.7612068106342116, 0.5447695822686637, 0.373924851932163, 0.27930793003309273, 0.24795243534715622, 0.2166027139283378, 0.1428710628614267, 0.06602338110497821, 0.021980743935920363, 0.006398279132023322, 0.0017936194597459384, 0.0006009500899246867, 0.00024768297660153493, 0.00011533171910677974, 5.940474255383892e-05, 3.0175857564910636e-05, 1.6223458431650605e-05, 8.845524938467253e-06, 4.8328429446258596e-06, 2.435353948121383e-06, 1.1669731534545345e-06, 5.843672017481929e-07, 2.975267432326348e-07, 1.3319634853069228e-07, 4.880943490079542e-08, 1.8002534751187506e-08, 1.2438479691035926e-08, 5.881024897175279e-09, 1.559130111354315e-09, 4.399999147793046e-10, 5.222167998741082e-11, 2.6387645368250217e-11, 1.0, 1.0, 1.0, 1.0};

float puw(int nTrueInt) { if (nTrueInt<50) return _puw_true[nTrueInt]; else return 0; }


// CAREFUL to the bin alignment: check which bin is nVert==0
// for 80X miniAOD v2, golden up to run 274443 (2.6/fb, Jun16 JSON)
float _puw2016_vtx[60] = {1.0, 0.05279044032209489, 0.11898234374437847, 0.24839403240247732, 0.4414409758143405, 0.6800191525008986, 0.911238430838953, 1.1249250544346439, 1.3083391445128427, 1.4527031750771802, 1.5156438062395463, 1.5389169972670533, 1.5035916926401598, 1.4373269045147126, 1.333092377737066, 1.2248748489799457, 1.0918319339782905, 0.9636778613250641, 0.8410627330851944, 0.7261267863768212, 0.6235739762642099, 0.5315059034719868, 0.44970258176095207, 0.3828912199699739, 0.32480952469934127, 0.27387410135800994, 0.23077463619648667, 0.1962917069010862, 0.16875803152705662, 0.14725031730832552, 0.13147828517394833, 0.11963481956991436, 0.1055294146473766, 0.09910459281290813, 0.08749009279742694, 0.07566616130096912, 0.07414888388958515, 0.07427197742439709, 0.07831177286837666, 0.07210793417378795, 0.14541998285529517, 0.05653406075048574, 0.053526929859502484, 0.2147604868753209, 0.1006306281358646, 0.2515765703396614, 0.0, 1.2578828516983072, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0};
float puw2016_vtx(int nVtx) { if (nVtx<60) return _puw2016_vtx[nVtx]; else return 0; }

// for up to 275125
float _puw2016_vtx_4fb[60] = {1.0, 0.05100939489406209, 0.10753683801507614, 0.22479210497504293, 0.4061194548857097, 0.6424861757674111, 0.8699208198466813, 1.0886008554762319, 1.276892560891215, 1.4184863274330797, 1.4865216108423305, 1.5122068499515893, 1.4790079191970888, 1.4196901839857483, 1.3216638995044172, 1.2217703342251016, 1.0976458888260794, 0.9796814642869479, 0.8639064021650553, 0.7535695441176858, 0.6555461235682296, 0.5641253790572658, 0.4834647260351342, 0.4164426860491679, 0.35606001606142423, 0.30497669791734305, 0.2592054182625056, 0.22335323942907434, 0.19192071849647147, 0.1672517813653499, 0.14683806760557278, 0.13614259650259863, 0.11857021273678048, 0.11205636298564389, 0.10212521715621654, 0.08684353771752344, 0.08864604848027625, 0.09804676288437263, 0.09235565349796869, 0.07943403772193891, 0.14417507424675546, 0.08136302667712911, 0.05135680407279777, 0.1569931571656257, 0.12873438887581296, 0.3218359721895326, 0.1609179860947663, 0.8045899304738313, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0 };
float puw2016_vtx_4fb(int nVtx) { if (nVtx<60) return _puw2016_vtx_4fb[nVtx]; else return 0; }

// for runs 274954-275125
float _puw2016_vtx_postTS_1p4fb[60] = {1.0, 0.0436628547984852, 0.0842489361361326, 0.17821945962362193, 0.3359458176736438, 0.5602926533570876, 0.7949986470183944, 1.009956832499392, 1.2171719031951709, 1.3352425499300327, 1.440211942752969, 1.461874846281358, 1.442598177264856, 1.3933114880260349, 1.303895089233208, 1.2175329549318987, 1.1119038703640942, 1.0164455216655062, 0.9118520665638973, 0.8059572090329304, 0.7155624000589931, 0.6289173123131537, 0.551810715512236, 0.4833237093643216, 0.4192621566956886, 0.3644494058922173, 0.30458903411821625, 0.2707118142127595, 0.2278811064155144, 0.20083759822187328, 0.17416091877224055, 0.16340944020160908, 0.14995476800202442, 0.12504239103683595, 0.12132829462778992, 0.09634514689836478, 0.1269739863549877, 0.1477893939541658, 0.12321393664515852, 0.03694734848854124, 0.10072796682909534, 0.06010102020802678, 0.11268941289005037, 0.0, 0.20488984161827345, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0};
float puw2016_vtx_postTS_1p4fb(int nVtx) { if (nVtx<60) return _puw2016_vtx_postTS_1p4fb[nVtx]; else return 0; }

// for json up to 276384 (9.235/fb)
float _puw2016_vtx_9fb[60] = {1.0, 0.04935539210063196, 0.10330050968638685, 0.2147911101772578, 0.39265726267153417, 0.6154543185021981, 0.8307112462687154, 1.0234405172528802, 1.1925131512920364, 1.2992751918824221, 1.3675693415474597, 1.383571620896604, 1.370751371914269, 1.3312898916887232, 1.260970719202342, 1.1934158915388204, 1.1079581139187757, 1.0207671452254607, 0.9330680851961782, 0.8459974039502247, 0.7660997972524449, 0.6853105592363634, 0.619098569695837, 0.5548227688124637, 0.498590328109847, 0.43969852956854144, 0.39485106899051653, 0.3546221583391258, 0.32414310290951415, 0.29492937650181855, 0.26816973928662186, 0.26026228952267894, 0.25438200170624503, 0.24305609489401844, 0.2402861143189915, 0.22410752071130485, 0.2329521554125791, 0.27204322650384044, 0.2187522991708468, 0.2697045149716429, 0.26325149847967466, 0.20939084706659114, 0.41327140868406215, 0.45300904413445264, 0.15704313529994357, 1.0, 0.3926078382498588, 1.963039191249294, 0.39260783824985873, 1.1778235147495764, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0};
float puw2016_vtx_9fb(int nVtx) { if (nVtx<60) return _puw2016_vtx_9fb[nVtx]; else return 0; }

// for json up to 276811 (12.9/fb)
float _puw2016_vtx_13fb[60] = {1.0, 0.046904649804193066, 0.09278031810949669, 0.18880389403907694, 0.3514757265099305, 0.557758357976481, 0.7693577917575528, 0.9666548740765918, 1.145319485841941, 1.2648398335691222, 1.3414360633779425, 1.3679594451533137, 1.362759399034107, 1.327376308549365, 1.2613315166803767, 1.196440614259811, 1.1139701579261285, 1.029953473266092, 0.9499371225384508, 0.8650456207995321, 0.7851579627730857, 0.7104602883630896, 0.6454503663312138, 0.5827160708961265, 0.527376483837914, 0.4700331217669938, 0.4271753119677936, 0.3869926520067443, 0.35986269245880403, 0.3280226115374019, 0.2995626735821264, 0.29695297220375283, 0.2904602474734967, 0.27797348557821827, 0.27285575884404983, 0.2696769830193652, 0.2834280746705423, 0.3079991295527812, 0.2958183730167929, 0.3281547943587132, 0.34428579006474574, 0.34709355767303973, 0.5916367460335905, 0.4991935044658422, 0.2689257936516321, 1.0, 0.690242870372522, 2.0707286111175662, 0.2958183730167952, 0.8874551190503855, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0};
float puw2016_vtx_13fb(int nVtx) { if (nVtx<60) return _puw2016_vtx_13fb[nVtx]; else return 0; }

//
//float puwMu8(int nVert) { return _puw_Mu8[nVert] * 0.001; }
//float puwMu17(int nVert) { return _puw_Mu17[nVert] * (2305428/29339.)*0.002/2.26; }

#include <assert.h>
#include "TH2F.h"
#include "TFile.h"

TFile *_file_recoToLoose_leptonSF_mu = NULL;
TH2F *_histo_recoToLoose_leptonSF_mu = NULL;
TFile *_file_recoToLoose_leptonSF_el = NULL;
TH2F *_histo_recoToLoose_leptonSF_el1 = NULL;
TH2F *_histo_recoToLoose_leptonSF_el2 = NULL;

float _get_recoToLoose_leptonSF_ttH(int pdgid, float pt, float eta, int nlep, float var){

  if (var!=0) assert(0); // NOT IMPLEMENTED

  if (!_histo_recoToLoose_leptonSF_mu) {
    _file_recoToLoose_leptonSF_mu = new TFile("","read");
    _histo_recoToLoose_leptonSF_mu = (TH2F*)(_file_recoToLoose_leptonSF_mu->Get("FINAL"));
  }
  if (!_histo_recoToLoose_leptonSF_el1) {
    _file_recoToLoose_leptonSF_el = new TFile("","read");
    _histo_recoToLoose_leptonSF_el1 = (TH2F*)(_file_recoToLoose_leptonSF_el->Get("MVAVLooseFO_and_IDEmu_and_TightIP2D"));
    _histo_recoToLoose_leptonSF_el2 = (TH2F*)(_file_recoToLoose_leptonSF_el->Get("MiniIso0p4_vs_AbsEta"));
  }

  if (abs(pdgid)==13){
    TH2F *hist = _histo_recoToLoose_leptonSF_mu;
    int etabin = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(eta)));
    int ptbin  = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(pt)));
    return hist->GetBinContent(etabin,ptbin);
  }
  if (abs(pdgid)==11){
    TH2F *hist = _histo_recoToLoose_leptonSF_el1;
    int ptbin  = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(pt)));
    int etabin = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(fabs(eta))));
    float out = hist->GetBinContent(ptbin,etabin);
    hist = _histo_recoToLoose_leptonSF_el2;
    ptbin  = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(pt)));
    etabin = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(fabs(eta))));
    out *= hist->GetBinContent(ptbin,etabin);
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

float _get_looseToTight_leptonSF_ttH(int pdgid, float _pt, float eta, int nlep, float var){

  float pt = std::min(float(79.9),_pt);

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

  float recoToLoose = 1; //_get_recoToLoose_leptonSF_ttH(pdgid,pt,eta,nlep,var);
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
    t2poly_triggerSF_ttH_ee = (TH2Poly*)(file_triggerSF_ttH->Get("SSee2DPt_effic"));
    t2poly_triggerSF_ttH_em = (TH2Poly*)(file_triggerSF_ttH->Get("SSeu2DPt_effic"));
    t2poly_triggerSF_ttH_3l = (TH2Poly*)(file_triggerSF_ttH->Get("__3l2DPt_effic"));
  }
  TH2Poly* hist = NULL;
  if (nlep==2){
    if (abs(pdgid1)==13 && abs(pdgid2)==13) hist = t2poly_triggerSF_ttH_mm;
    else if (abs(pdgid1)==11 && abs(pdgid2)==11) hist = t2poly_triggerSF_ttH_ee;
    else hist = t2poly_triggerSF_ttH_em;
  }
  else if (nlep==3) hist = t2poly_triggerSF_ttH_3l;
  int xbin  = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(pt1)));
  int ybin = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(pt2)));
  float eff = hist->GetBinContent(xbin,ybin) + var * hist->GetBinError(xbin,ybin);

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


void functions() {}
