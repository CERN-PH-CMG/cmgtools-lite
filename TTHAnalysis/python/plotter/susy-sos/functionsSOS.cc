// we need headers
#include <cmath>
#include "Math/GenVector/LorentzVector.h"
#include "Math/GenVector/PtEtaPhiM4D.h"
#include "Math/GenVector/PxPyPzM4D.h"
// we need to declare the functions we use from functions.cc
float pt_2(float,float,float,float) ;
float pt_3(float,float,float,float,float,float) ;
// and we need an empty function
void functionsSOS() {}
// and we can check that everything compiles fine with
// $ root.exe -b -l -q functions.cc+ susy-sos/functionsSOS.cc+

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
  if (std::abs(pdg1)==13 && std::abs(pdg2)==13) return pt_3(pt1,phi1,pt2,phi2,metpt,metphi);
  else if (std::abs(pdg1)==13 && !(std::abs(pdg2)==13)) return pt_2(pt1,phi1,metpt,metphi);
  else if (!(std::abs(pdg1)==13) && std::abs(pdg2)==13) return pt_2(pt2,phi2,metpt,metphi);
  else if (!(std::abs(pdg1)==13) && !(std::abs(pdg2)==13)) return metpt;
  else return -99;
}



float eleWPVVL(float pt, float etaSc, float mva){
  if (pt<=10 && ((std::abs(etaSc)<0.8 && mva>-0.265) || (std::abs(etaSc)>=0.8 && std::abs(etaSc)<1.479 && mva > -0.556) || (std::abs(etaSc)>=1.479 && mva>-0.6))) return 1;
  else if (pt>10 && ((std::abs(etaSc)<0.8 && mva > 0.87) || (std::abs(etaSc)>=0.8 && std::abs(etaSc)<1.479 && mva > 0.30) || (std::abs(etaSc)>=1.479 && mva >-0.30))) return 1;
  else return 0;
}


float eleWPT(float pt, float etaSc, float mva){
  if (pt<=10 && ((std::abs(etaSc)<0.8 && mva>-0.265) || (std::abs(etaSc)>=0.8 && std::abs(etaSc)<1.479 && mva > -0.556) || (std::abs(etaSc)>=1.479 && mva>-0.551))) return 1;
  else if (pt>10 && ((std::abs(etaSc)<0.8 && mva > 0.87) || (std::abs(etaSc)>=0.8 && std::abs(etaSc)<1.479 && mva > 0.60) || (std::abs(etaSc)>=1.479 && mva >0.17))) return 1;
  else return 0;
}

