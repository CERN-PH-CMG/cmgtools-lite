#include <cmath>
#include "Math/GenVector/LorentzVector.h"
#include "Math/GenVector/PtEtaPhiM4D.h"
#include "Math/GenVector/PxPyPzM4D.h"
#include "Math/GenVector/Boost.h"
#include "TLorentzVector.h"

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


// May 2016: This is func which takes the 4vectors of MET, L1,L2 and reconstructs 2 taus and returns the effective Z(-->tautau) mass.                                                                                        // To be investigated: do not allow to insert more than 9 parameter; Skipped the lepton types/masses...                                                                                                         

float mass_tautau( float Met_Pt, float Met_Phi, float l1_Pt, float l1_Eta, float l1_Phi, float l2_Pt, float l2_Eta, float l2_Phi ) {
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
  
  if (nj==0 && met<100)        return -1;  //validation region 0-jet
  else if (nj==1 && met<100)   return -2;  //validation region 1-jet
  else if (nj==0 && mtw<40 && met>100 && met<200)             return 1;
  else if (nj==0 && mtw<40 && met>200)                        return 2;
  else if (nj==0 && mtw>40 && mtw<120 && met>100 && met<200)  return 3;
  else if (nj==0 && mtw>40 && mtw<120 && met>200)             return 4;
  else if (nj==0 && mtw>120 && mtw<120 && met>100 && met<200) return 5;
  else if (nj==0 && mtw>120 && mtw<120 &&  met>200)           return 6;
  else if (nj==1 && mtw<40 && met>100 && met<200)             return 11;
  else if (nj==1 && mtw<40 && met>200)                        return 12;
  else if (nj==1 && mtw>40 && mtw<120 && met>100 && met<200)  return 13;
  else if (nj==1 && mtw>40 && mtw<120 && met>200)             return 14;
  else if (nj==1 && mtw>120 && mtw<120 && met>100 && met<200) return 15;
  else if (nj==1 && mtw>120 && mtw<120 &&  met>200)           return 16;
  
  return -99;
  
}
//float MVAto1D_6_sorted_ee(float kinMVA_2lss_ttbar, float kinMVA_2lss_ttV) {
//    
//    float MVA_binned_6 = 0; 		
//
//    if ((kinMVA_2lss_ttbar > 0.2 && kinMVA_2lss_ttbar <=  1.0) && (kinMVA_2lss_ttV > -1.0 && kinMVA_2lss_ttV <= 0.1)) MVA_binned_6 += 1;
//
//    if ((kinMVA_2lss_ttbar > 0.2 && kinMVA_2lss_ttbar <=  1.0) && (kinMVA_2lss_ttV > 0.1 && kinMVA_2lss_ttV <=  0.3)) MVA_binned_6 += 2;
//
//    if ((kinMVA_2lss_ttbar > 0.2 && kinMVA_2lss_ttbar <=  1.0) && (kinMVA_2lss_ttV > 0.3 && kinMVA_2lss_ttV <=  1.0)) MVA_binned_6 += 3;
//
//    if ((kinMVA_2lss_ttbar > -1.0 && kinMVA_2lss_ttbar <= 0.2) && (kinMVA_2lss_ttV > -1.0 && kinMVA_2lss_ttV <=  0.3)) MVA_binned_6 += 5;
//
//    if ((kinMVA_2lss_ttbar > 0.1 && kinMVA_2lss_ttbar <= 0.2) && (kinMVA_2lss_ttV > 0.3 && kinMVA_2lss_ttV <=  1.0)) MVA_binned_6 += 4;
//
//    if ((kinMVA_2lss_ttbar > -1.0 && kinMVA_2lss_ttbar <= 0.1) && (kinMVA_2lss_ttV > 0.3 && kinMVA_2lss_ttV <=  1.0)) MVA_binned_6 += 4;
//
////    if ((kinMVA_2lss_ttbar > -1.0 && kinMVA_2lss_ttbar <= 0.2) && (kinMVA_2lss_ttV > -1.0 && kinMVA_2lss_ttV <=  0.3)) MVA_binned_6 += 6;
////
////    if ((kinMVA_2lss_ttbar > 0.1 && kinMVA_2lss_ttbar <= 0.2) && (kinMVA_2lss_ttV > 0.3 && kinMVA_2lss_ttV <=  1.0)) MVA_binned_6 += 5;
////
////    if ((kinMVA_2lss_ttbar > -1.0 && kinMVA_2lss_ttbar <= 0.1) && (kinMVA_2lss_ttV > 0.3 && kinMVA_2lss_ttV <=  1.0)) MVA_binned_6 += 4;
//
//	
//    return MVA_binned_6;
//
//}
//
//float MVAto1D_6_sorted_em(float kinMVA_2lss_ttbar, float kinMVA_2lss_ttV) {
//    
//    float MVA_binned_6 = 0; 		
//
//    if ((kinMVA_2lss_ttbar > 0.4 && kinMVA_2lss_ttbar <=  1.0) && (kinMVA_2lss_ttV > -1.0 && kinMVA_2lss_ttV <= 0.1)) MVA_binned_6 += 1;
//
//    if ((kinMVA_2lss_ttbar > 0.4 && kinMVA_2lss_ttbar <=  1.0) && (kinMVA_2lss_ttV > 0.1 && kinMVA_2lss_ttV <=  0.3)) MVA_binned_6 += 2;
//
//    if ((kinMVA_2lss_ttbar > 0.4 && kinMVA_2lss_ttbar <=  1.0) && (kinMVA_2lss_ttV > 0.3 && kinMVA_2lss_ttV <=  1.0)) MVA_binned_6 += 3;
//
//    if ((kinMVA_2lss_ttbar > -1.0 && kinMVA_2lss_ttbar <= 0.4) && (kinMVA_2lss_ttV > -1.0 && kinMVA_2lss_ttV <=  0.2)) MVA_binned_6 += 6;
//
//    if ((kinMVA_2lss_ttbar > 0.3 && kinMVA_2lss_ttbar <= 0.4) && (kinMVA_2lss_ttV > 0.2 && kinMVA_2lss_ttV <=  1.0)) MVA_binned_6 += 5;
//
//    if ((kinMVA_2lss_ttbar > -1.0 && kinMVA_2lss_ttbar <= 0.3) && (kinMVA_2lss_ttV > 0.2 && kinMVA_2lss_ttV <=  1.0)) MVA_binned_6 += 4;
//        
//    return MVA_binned_6;
//
//}
//
//float MVAto1D_6_sorted_mumu(float kinMVA_2lss_ttbar, float kinMVA_2lss_ttV) {
//    
//    float MVA_binned_6 = 0; 		
//
//    if ((kinMVA_2lss_ttbar > 0.35 && kinMVA_2lss_ttbar <=  1.0) && (kinMVA_2lss_ttV > -1.0 && kinMVA_2lss_ttV <= 0.1)) MVA_binned_6 += 1;
//
//    if ((kinMVA_2lss_ttbar > 0.35 && kinMVA_2lss_ttbar <=  1.0) && (kinMVA_2lss_ttV > 0.1 && kinMVA_2lss_ttV <=  0.25)) MVA_binned_6 += 2;
//
//    if ((kinMVA_2lss_ttbar > 0.35 && kinMVA_2lss_ttbar <=  1.0) && (kinMVA_2lss_ttV > 0.25 && kinMVA_2lss_ttV <=  1.0)) MVA_binned_6 += 3;
//
//    if ((kinMVA_2lss_ttbar > -1.0 && kinMVA_2lss_ttbar <= 0.35) && (kinMVA_2lss_ttV > -1.0 && kinMVA_2lss_ttV <=  0.15)) MVA_binned_6 += 6;
//
//    if ((kinMVA_2lss_ttbar > 0.1 && kinMVA_2lss_ttbar <= 0.35) && (kinMVA_2lss_ttV > 0.15 && kinMVA_2lss_ttV <=  1.0)) MVA_binned_6 += 5;
//
//    if ((kinMVA_2lss_ttbar > -1.0 && kinMVA_2lss_ttbar <= 0.1) && (kinMVA_2lss_ttV > 0.15 && kinMVA_2lss_ttV <=  1.0)) MVA_binned_6 += 4;
//	
//    return MVA_binned_6;
//
//}
//
//float MVAto1D_6_sorted_3l(float kinMVA_3l_ttbar, float kinMVA_3l_ttV) {
//    
//    float MVA_binned_6_3l = 0; 		
//
//    if ((kinMVA_3l_ttbar > 0.2 && kinMVA_3l_ttbar <=  1.0) && (kinMVA_3l_ttV > -1.0 && kinMVA_3l_ttV <= 0.0)) MVA_binned_6_3l += 1;
//
//    if ((kinMVA_3l_ttbar > 0.2 && kinMVA_3l_ttbar <=  1.0) && (kinMVA_3l_ttV > 0.0 && kinMVA_3l_ttV <=  0.25)) MVA_binned_6_3l += 2;
//
//    if ((kinMVA_3l_ttbar > 0.2 && kinMVA_3l_ttbar <=  1.0) && (kinMVA_3l_ttV > 0.25 && kinMVA_3l_ttV <=  1.0)) MVA_binned_6_3l += 3;
//
//    if ((kinMVA_3l_ttbar > -1.0 && kinMVA_3l_ttbar <= 0.2) && (kinMVA_3l_ttV > -1.0 && kinMVA_3l_ttV <=  0.25)) MVA_binned_6_3l += 6;
//
//    if ((kinMVA_3l_ttbar > 0.1 && kinMVA_3l_ttbar <= 0.2) && (kinMVA_3l_ttV > 0.25 && kinMVA_3l_ttV <=  1.0)) MVA_binned_6_3l += 5;
//
//    if ((kinMVA_3l_ttbar > -1.0 && kinMVA_3l_ttbar <= 0.1) && (kinMVA_3l_ttV > 0.25 && kinMVA_3l_ttV <=  1.0)) MVA_binned_6_3l += 4;
//	
//    return MVA_binned_6_3l;
//
//}

float ttH_MVAto1D_6_2lss_Marco (float kinMVA_2lss_ttbar, float kinMVA_2lss_ttV){

  return 2*((kinMVA_2lss_ttbar>=-0.2)+(kinMVA_2lss_ttbar>=0.3))+(kinMVA_2lss_ttV>=-0.1)+1;

}

float ttH_MVAto1D_3_3l_Marco (float kinMVA_3l_ttbar, float kinMVA_3l_ttV){

  if (kinMVA_3l_ttbar<0.3 && kinMVA_3l_ttV<-0.1) return 1;
  else if (kinMVA_3l_ttbar>=0.3 && kinMVA_3l_ttV>=-0.1) return 3;
  else return 2;

}

float ttH_MVAto1D_6_flex (float kinMVA_2lss_ttbar, float kinMVA_2lss_ttV, int pdg1, int pdg2, float ttVcut, float ttcut1, float ttcut2){

  return 2*((kinMVA_2lss_ttbar>=ttcut1)+(kinMVA_2lss_ttbar>=ttcut2)) + (kinMVA_2lss_ttV>=ttVcut)+1;

}

//float ttH_MVAto1D_6_2lss_Milos (float kinMVA_2lss_ttbar, float kinMVA_2lss_ttV, int pdg1, int pdg2){
//
//  if (abs(pdg1)==11 && abs(pdg2)==11) return MVAto1D_6_sorted_ee(kinMVA_2lss_ttbar,kinMVA_2lss_ttV);
//  else if (abs(pdg1)==13 && abs(pdg2)==13) return MVAto1D_6_sorted_mumu(kinMVA_2lss_ttbar,kinMVA_2lss_ttV);
//  else return MVAto1D_6_sorted_em(kinMVA_2lss_ttbar,kinMVA_2lss_ttV);
//}
//
//float ttH_MVAto1D_6_3l_Milos (float kinMVA_3l_ttbar, float kinMVA_3l_ttV){
//
//  return MVAto1D_6_sorted_3l(kinMVA_3l_ttbar,kinMVA_3l_ttV);
//}

// for 74X
//float _puw_true[50] = {3.652322599922302, 3.652322599922302, 3.652322599922302, 3.652322599922302, 3.652322599922302, 3.652322599922302, 2.1737862420968868, 2.7116925849897364, 3.352556070095877, 3.083015137131128, 2.8824218072960823, 2.6791975503716743, 2.212434153800565, 1.5297063638539434, 0.8762698648562287, 0.41326633649647065, 0.17496252648670657, 0.07484562496757297, 0.038507396968229766, 0.021849761893692053, 0.01140425609526747, 0.005063578526248854, 0.001881351382104846, 0.0006306639125313864, 0.00021708627575927402, 9.42187694469501e-05, 5.146591433045169e-05, 3.326854405002371e-05, 2.426063215708668e-05, 1.8575279862433386e-05, 1.281054551977887e-05, 8.01819566777096e-06, 3.6521122159066883e-06, 1.574921039309069e-06, 5.770182058345157e-07, 2.0862027190449754e-07, 6.946502045299735e-08, 2.032077576113469e-08, 6.417943581326451e-09, 1.5934414668326278e-09, 4.311337237072122e-10, 1.1138367777447038e-10, 2.6925919137965106e-11, 8.08827951069873e-12, 1.3708268591386723e-12, 4.065021195897016e-13, 1.770006195676463e-13, 5.689967214903059e-14, 6.224880123134382e-14, 0.0};
//
//float _puw_Mu8[60] = { 1.0, 2.2753238054533287, 2.5087852081376565, 2.547534409862272, 2.5453856677292626, 2.3957671901210302, 2.329888347258754, 2.132632821246379, 1.9294351293836975, 1.6869299027848321, 1.410414475296686, 1.18061883859625, 0.9505511419155187, 0.7455821522790507, 0.5917331920192597, 0.4497875190879285, 0.3529109417225823, 0.26485881058611677, 0.208008048447543, 0.1582531319686015, 0.12944461423876671, 0.10248826819473823, 0.07759715482270031, 0.05888999109148935, 0.059779044174240605, 0.041874820142546565, 0.03324024895102297, 0.039028818938047924, 0.02179308514266076, 0.01197215401539325, 0.009421343447104134, 0.013861014595193729, 0.0, 0.06539755302753723, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0 };
//float _puw_Mu17[60] = { 1.0, 2.6025657030947866, 2.8330872498461876, 2.477197375267561, 2.552415607786326, 2.4047951682107627, 2.3024376807492737, 2.1540414886183843, 1.9518423032680638, 1.699049184347834, 1.4639137707975747, 1.2067661580794682, 0.966660952828535, 0.766250445622546, 0.5938409557059098, 0.4557404537508868, 0.3447511898010737, 0.26427563682379623, 0.2033725709370245, 0.15418157724654288, 0.12117494844707002, 0.09683984946855388, 0.08058574696446474, 0.06008103415479263, 0.049369064099306637, 0.043438226650837304, 0.032177902255824065, 0.029449084226433955, 0.02071379137395143, 0.01793424569381745, 0.013294248051062496, 0.012108360448835863, 0.009083026618738383, 0.0091627022908326, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0 };
//

// for 76X
float _puw_true[50] = {0.5269234785559587, 0.6926695654592266, 1.080004829553802, 1.379105403255213, 1.819531519703243, 2.212948765398841, 1.591693852037577, 1.3246151544739415, 1.332963823519763, 1.252466214103506, 1.1890944076884082, 1.1546479191424708, 1.0968414518989904, 0.9606172752657895, 0.7612068106342116, 0.5447695822686637, 0.373924851932163, 0.27930793003309273, 0.24795243534715622, 0.2166027139283378, 0.1428710628614267, 0.06602338110497821, 0.021980743935920363, 0.006398279132023322, 0.0017936194597459384, 0.0006009500899246867, 0.00024768297660153493, 0.00011533171910677974, 5.940474255383892e-05, 3.0175857564910636e-05, 1.6223458431650605e-05, 8.845524938467253e-06, 4.8328429446258596e-06, 2.435353948121383e-06, 1.1669731534545345e-06, 5.843672017481929e-07, 2.975267432326348e-07, 1.3319634853069228e-07, 4.880943490079542e-08, 1.8002534751187506e-08, 1.2438479691035926e-08, 5.881024897175279e-09, 1.559130111354315e-09, 4.399999147793046e-10, 5.222167998741082e-11, 2.6387645368250217e-11, 1.0, 1.0, 1.0, 1.0};

float puw(int nTrueInt) { if (nTrueInt<50) return _puw_true[nTrueInt]; else return 0; }

// for 80X miniAOD v1, data up to run 273730
float _puw2016_vtx[40] = {0.19692137176564317, 0.5512893955944992, 0.9770490049006523, 1.5347221311033268, 1.9692615705153973, 2.1491195749572007, 2.1780114323780513, 2.1476769294879037, 2.034380632552017, 1.87588545290878, 1.706600023753648, 1.5343743090394626, 1.3432450969258811, 1.1510269674496358, 0.9801083154979298, 0.8092391449359286, 0.6641103531512786, 0.5447223215449378, 0.4295029198143936, 0.3338937564649758, 0.2631617941891352, 0.20079880107279335, 0.15986742978997262, 0.11445737335104854, 0.08137048173588282, 0.06446688279958453, 0.051602567961013174, 0.03886047839947285, 0.02639331456382827, 0.019479110921421926, 0.016802825802323017, 0.008207196793826336, 0.005048555458954462, 0.009915180991460402, 0.0032609928594136157, 0.009591155468863447, 0.0, 0.0, 0.0, 0.0};
float puw2016_vtx(int nVtx) { if (nVtx<40) return _puw2016_vtx[nVtx]; else return 0; }

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
    _file_recoToLoose_leptonSF_mu = new TFile("/afs/cern.ch/user/p/peruzzi/work/tthtrees/cms_utility_files/mu_eff_recoToLoose_ttH.root","read");
    _histo_recoToLoose_leptonSF_mu = (TH2F*)(_file_recoToLoose_leptonSF_mu->Get("FINAL"));
  }
  if (!_histo_recoToLoose_leptonSF_el1) {
    _file_recoToLoose_leptonSF_el = new TFile("/afs/cern.ch/user/p/peruzzi/work/tthtrees/cms_utility_files/kinematicBinSFele.root","read");
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
    _file_looseToTight_leptonSF_mu_2lss = new TFile("/afs/cern.ch/user/p/peruzzi/work/tthtrees/cms_utility_files/lepMVAEffSF_m_2lss.root","read");
    _histo_looseToTight_leptonSF_mu_2lss = (TH2F*)(_file_looseToTight_leptonSF_mu_2lss->Get("sf"));
  }
  if (!_histo_looseToTight_leptonSF_el_2lss) {
    _file_looseToTight_leptonSF_el_2lss = new TFile("/afs/cern.ch/user/p/peruzzi/work/tthtrees/cms_utility_files/lepMVAEffSF_e_2lss.root","read");
    _histo_looseToTight_leptonSF_el_2lss = (TH2F*)(_file_looseToTight_leptonSF_el_2lss->Get("sf"));
  }
  if (!_histo_looseToTight_leptonSF_mu_3l) {
    _file_looseToTight_leptonSF_mu_3l = new TFile("/afs/cern.ch/user/p/peruzzi/work/tthtrees/cms_utility_files/lepMVAEffSF_m_3l.root","read");
    _histo_looseToTight_leptonSF_mu_3l = (TH2F*)(_file_looseToTight_leptonSF_mu_3l->Get("sf"));
  }
  if (!_histo_looseToTight_leptonSF_el_3l) {
    _file_looseToTight_leptonSF_el_3l = new TFile("/afs/cern.ch/user/p/peruzzi/work/tthtrees/cms_utility_files/lepMVAEffSF_e_3l.root","read");
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

float triggerSF_ttH(int pdgid1, float pt1, int pdgid2, float pt2, int nlep, float var_ee=0){
  if (var_ee!=0) assert(0); // NOT IMPLEMENTED
  if (nlep>2) return 1;
  if (abs(pdgid1)==11 && abs(pdgid2)==11){
    if (std::max(pt1,pt2)<40) return 0.95;
    else return 0.99;
  }
  else if (abs(pdgid1)==13 && abs(pdgid2)==13) {
    return 1.;
  }
  else return 0.98;
}

float mass_3_cheap(float pt1, float eta1, float pt2, float eta2, float phi2, float pt3, float eta3, float phi3) {
    typedef ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double> > PtEtaPhiMVector;
    PtEtaPhiMVector p41(pt1,eta1,0,   0.0);
    PtEtaPhiMVector p42(pt2,eta2,phi2,0.0);
    PtEtaPhiMVector p43(pt3,eta3,phi3,0.0);
    return (p41+p42+p43).M();
}


void functions() {}
