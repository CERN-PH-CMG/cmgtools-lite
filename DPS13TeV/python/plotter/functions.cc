// #ifndef FUNCTIONS_H
// #define FUNCTIONS_H

// #include <stdio.h>
// #include <stdlib.h>
#include <iostream>
#include <cstdlib> //as stdlib.h                 
#include <cstdio>
#include <map>
#include <string>
#include <cmath>
#include "TH2F.h"
#include "TVector2.h"
#include "Math/GenVector/LorentzVector.h"
#include "Math/GenVector/PtEtaPhiM4D.h"
#include "PhysicsTools/Heppy/interface/Davismt2.h"

using namespace std;

//// UTILITY FUNCTIONS NOT IN TFORMULA ALREADY

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

float Hypot(float x, float y) {
  return hypot(x,y);
}

float pt_2(float pt1, float phi1, float pt2, float phi2) {
    phi2 -= phi1;
    return hypot(pt1 + pt2 * std::cos(phi2), pt2*std::sin(phi2));
}

float mt_2(float pt1, float phi1, float pt2, float phi2) {
    return std::sqrt(2*pt1*pt2*(1-std::cos(phi1-phi2)));
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

float mass_2_ene(float ene1, float eta1, float phi1, float m1, float ene2, float eta2, float phi2, float m2) {
    typedef ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double> > PtEtaPhiMVector;
    PtEtaPhiMVector unitp41(1.0,eta1,phi1,m1);
    PtEtaPhiMVector unitp42(1.0,eta2,phi2,m2);
    double theta1 = unitp41.Theta();
    double theta2 = unitp42.Theta();
    double pt1 = ene1*fabs(sin(theta1));
    double pt2 = ene2*fabs(sin(theta2));
    PtEtaPhiMVector p41(pt1,eta1,phi1,m1);
    PtEtaPhiMVector p42(pt2,eta2,phi2,m2);
    return (p41+p42).M();
}

float mass_2(float pt1, float eta1, float phi1, float m1, float pt2, float eta2, float phi2, float m2) {
    typedef ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double> > PtEtaPhiMVector;
    PtEtaPhiMVector p41(pt1,eta1,phi1,m1);
    PtEtaPhiMVector p42(pt2,eta2,phi2,m2);
    return (p41+p42).M();
}

float eta_2(float pt1, float eta1, float phi1, float m1, float pt2, float eta2, float phi2, float m2) {
    typedef ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double> > PtEtaPhiMVector;
    PtEtaPhiMVector p41(pt1,eta1,phi1,m1);
    PtEtaPhiMVector p42(pt2,eta2,phi2,m2);
    return (p41+p42).Eta();
}

float phi_2(float pt1, float eta1, float phi1, float m1, float pt2, float eta2, float phi2, float m2){
    typedef ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double> > PtEtaPhiMVector; 
    PtEtaPhiMVector l1(pt1, eta1, phi1, m1); 
    PtEtaPhiMVector l2(pt2, eta2, phi2, m2);
    return (l1+l2).Phi();
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

float mt_lu_cart(float lep_pt, float lep_phi, float u_x, float u_y)
{
    float lep_px = lep_pt*std::cos(lep_phi), lep_py = lep_pt*std::sin(lep_phi);
    float u = hypot(u_x,u_y);
    float uDotLep = u_x*lep_px + u_y*lep_py;
    return sqrt(2*lep_pt*sqrt(u*u+lep_pt*lep_pt+2*uDotLep) + 2*uDotLep + 2*lep_pt*lep_pt);
}

float u1_2(float met_pt, float met_phi, float ref_pt, float ref_phi) 
{
    float met_px = met_pt*std::cos(met_phi), met_py = met_pt*std::sin(met_phi);
    float ref_px = ref_pt*std::cos(ref_phi), ref_py = ref_pt*std::sin(ref_phi);
    float ux = - met_px + ref_px, uy = - met_py + ref_py;
    return (ux*ref_px + uy*ref_py)/ref_pt;
}
float u2_2(float met_pt, float met_phi, float ref_pt, float ref_phi)
{
    float met_px = met_pt*std::cos(met_phi), met_py = met_pt*std::sin(met_phi);
    float ref_px = ref_pt*std::cos(ref_phi), ref_py = ref_pt*std::sin(ref_phi);
    float ux = - met_px + ref_px, uy = - met_py + ref_py;
    return (ux*ref_py - uy*ref_px)/ref_pt;
}

float met_cal(float met_pt, float met_phi, float lep_pt, float lep_phi, float u_coeff, float u_syst)
{
    float met_px = met_pt*std::cos(met_phi), met_py = met_pt*std::sin(met_phi);
    float lep_px = lep_pt*std::cos(lep_phi), lep_py = lep_pt*std::sin(lep_phi);
    float ux = met_px + lep_px, uy = met_py + lep_py;
    float metcal_px = - u_coeff*ux*(1+u_syst) - lep_px, metcal_py = - u_coeff*uy*(1+u_syst) - lep_py;
    return hypot(metcal_px,metcal_py);
}
/*
float puw2017_herwigg[80] = {0,0,0,2.27008,3.74564,2.25339,2.82139,2.97948,2.47187,2.77325,2.53951,2.33365,2.03668,1.88443,1.77833,1.67443,1.56289,1.3917,1.25253,1.06277,0.976758,0.870936,0.790535,0.713799,0.643822,0.551428,0.516994,0.465398,0.38879,0.349138,0.327546,0.30658,0.240941,0.251968,0.200709,0.181512,0.183967,0.157223,0.151671,0.106266,0.104634,0.0948796,0.0902638,0.0717555,0.0832775,0.0625131,0.0606511,0.0446805,0.036115,0.0295584,0.0344268,0.0403625,0.0211761,0.0270248,0.00522258,0.0136205,0.0214609,0.0390496,0.0286949,0.0197972,0.0425641,0,0.0236467,0.0257964,0,0,0,0.0405372,0,0,0,0,0,0,0,0,0,0,0,0};
float puw2017_CP5[80] = {0,0,0,0.0720495,0.396272,0.368435,1.04472,1.10326,1.26087,2.03283,2.41803,1.9437,1.61881,1.51869,1.59003,1.60409,1.48697,1.55307,1.42429,1.04643,0.977148,0.925688,0.89919,0.696008,0.652616,0.619487,0.529287,0.476657,0.363019,0.380386,0.38475,0.295426,0.227875,0.243373,0.189566,0.184144,0.194828,0.150433,0.177622,0.0854195,0.0947405,0.109906,0.0900619,0.104282,0.0827099,0.0577756,0.068155,0.0438763,0.0360248,0.0237005,0.0300206,0.0309588,0.0250172,0.0200138,0.00428866,0.0180124,0.0150103,0.0204686,0.0142203,0.0225155,0.0600413,0,0.0150103,0.0300206,0,0,0,0.0900619,0,0,0,0,0,0,0,0,0,0,0,0};

float puw_2017( int nVert, bool herwMC){
  if(herwMC == true) return puw2017_herwigg[nVert];
  else if (nVert > 80) return 0;
  else if(herwMC == false) return puw2017_CP5[nVert];
  else return 0;
}
*/
float _puw2016_nTrueInt_BF[60] = {0.0004627598152210959, 0.014334910915287028, 0.01754727657726197, 0.03181477917631854, 0.046128282569231016, 0.03929080994013006, 0.057066019809589925, 0.19570744862221007, 0.3720256062526554, 0.6440076202772811, 0.9218024454406528, 1.246743510634073, 1.5292543296414058, 1.6670061646418215, 1.7390553377117133, 1.6114721876895595, 1.4177294439817985, 1.420132866045718, 1.3157656415540477, 1.3365188060918483, 1.1191478126677334, 0.9731079434848392, 0.9219564145009487, 0.8811793391804676, 0.7627315352977334, 0.7265186492688713, 0.558602385324645, 0.4805954159733825, 0.34125298049234554, 0.2584848657646724, 0.1819638766151892, 0.12529545619337035, 0.11065705912071645, 0.08587356267495487, 0.09146322371620583, 0.11885517671051576, 0.1952483711863489, 0.23589115679998116, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0};
float puw2016_nTrueInt_BF(int nTrueInt) { if (nTrueInt<60) return _puw2016_nTrueInt_BF[nTrueInt]; else return 0; }

float _puw2016_nTrueInt_36fb[100] = {0.3505407355600995, 0.8996968628890968, 1.100322319466069, 0.9562526765089195, 1.0366251229154624, 1.0713954619016586, 0.7593488199769544, 0.47490309461978414, 0.7059895997695581, 0.8447022252423783, 0.9169159386164522, 1.0248924033173097, 1.0848877947714115, 1.1350984224561655, 1.1589888429954602, 1.169048420382294, 1.1650383018054549, 1.1507200023444994, 1.1152571438041776, 1.0739529436969637, 1.0458014000030829, 1.032500407707141, 1.0391236062781293, 1.041283620738903, 1.0412963370894526, 1.0558823002770783, 1.073481674823461, 1.0887053272606795, 1.1041701696801014, 1.123218903738397, 1.1157169321377927, 1.1052520327174429, 1.0697489590429388, 1.0144652740600584, 0.9402657069968621, 0.857142825520793, 0.7527112615290031, 0.6420618248685722, 0.5324755829715156, 0.4306470627563325, 0.33289171600176093, 0.24686361729094983, 0.17781595237914027, 0.12404411884835284, 0.08487088505600057, 0.056447805688061216, 0.03540829360547507, 0.022412461576677457, 0.013970541270658443, 0.008587896629717911, 0.004986410514292661, 0.00305102303701641, 0.001832072556146534, 0.0011570757619737708, 0.0008992999249003301, 0.0008241241729452477, 0.0008825716073180279, 0.001187003960081393, 0.0016454104270429153, 0.0022514113879764414, 0.003683196037880878, 0.005456695951503178, 0.006165248770884191, 0.007552675218762607, 0.008525338219226993, 0.008654690499815343, 0.006289068906974821, 0.00652551838513972, 0.005139581024893171, 0.005115751962934923, 0.004182527768384693, 0.004317593022028565, 0.0035749335962533355, 0.003773660372937113, 0.002618732319396435, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0};
float puw2016_nTrueInt_36fb(int nTrueInt) { if (nTrueInt<100) return _puw2016_nTrueInt_36fb[nTrueInt]; else return 0; }

// functions to assess if events pass given ID cuts
// isEB can be defined as (LepGood1_etaSc)<1.479 
// note that 2016 cut-based ID defines thesholds for EB and EE using SuperCluster eta
// the real ID WP part is in LepGood1_tightId, LepGood1_lostHits and LepGood1_convVeto
// dxy and dz are not part of the official ID WP, but we use the suggested thresholds anyway
// https://twiki.cern.ch/twiki/bin/viewauth/CMS/CutBasedElectronIdentificationRun2
// 
// list of functions to manage IDs
// those marked with ** are work in progress (problems with string, format is n tcompatible with TTree::Draw() used by mcPlots.py)
// -------------------------------
// pass_dxy_dz
// pass_lostHits_conVe
// pass_looseIDnoIso_2016
// pass_mediumIDnoIso_2016
// pass_tightIDnoIso_2016
// pass_workingPointIDnoIso_2016 **
// pass_isolation_2016 **
// passFakerateNumerator2016 **
// isInFakerateApplicationRegion2016 **
// pass_isolation_WP
// pass_FakerateNumerator2016
// pass_FakerateApplicationRegion2016
//
//
// -------------------------------


// pass dxy and dz
bool pass_dxy_dz(const bool isEB = true, 
		 const float LepGood1_dxy = -999, 
		 const float LepGood1_dz = -999
		 ) 
{
  
  if (isEB) return (abs(LepGood1_dxy) < 0.05 && abs(LepGood1_dz) < 0.1);
  else      return (abs(LepGood1_dxy) < 0.1  && abs(LepGood1_dz) < 0.2);

}

// missing hits and conversion veto
bool pass_lostHits_conVeto(const int LepGood1_lostHits = -999, 
			   const int LepGood1_convVeto = -999
			   ) 
{
  return (LepGood1_lostHits <= 1 && LepGood1_convVeto == 1);
}


// loose ID no isolation
bool pass_looseIDnoIso_2016(const bool  isEB = true, 
			    const int   LepGood1_tightId = -1, 
			    const float LepGood1_dxy = -999, 
			    const float LepGood1_dz = -999,
			    const int   LepGood1_lostHits = -1,
			    const int   LepGood1_convVeto = -999
			    ) 
{

  return (LepGood1_tightId >= 1 && pass_dxy_dz(isEB,LepGood1_dxy,LepGood1_dz) && pass_lostHits_conVeto(LepGood1_lostHits,LepGood1_convVeto) );

}

// medium ID no isolation
bool pass_mediumIDnoIso_2016(const bool  isEB = true, 
			     const int   LepGood1_tightId = -1, 
			     const float LepGood1_dxy = -999, 
			     const float LepGood1_dz = -999,
			     const int   LepGood1_lostHits = -1,
			     const int   LepGood1_convVeto = -999
			     ) 
{

  return (LepGood1_tightId >= 2 && pass_dxy_dz(isEB,LepGood1_dxy,LepGood1_dz) && pass_lostHits_conVeto(LepGood1_lostHits,LepGood1_convVeto) );

}

// tight ID no isolation
bool pass_tightIDnoIso_2016(const bool  isEB = true, 
			    const int   LepGood1_tightId = -1, 
			    const float LepGood1_dxy = -999, 
			    const float LepGood1_dz = -999,
			    const int   LepGood1_lostHits = -1,
			    const int   LepGood1_convVeto = -999
			    ) 
{

  return (LepGood1_tightId >= 3 && pass_dxy_dz(isEB,LepGood1_dxy,LepGood1_dz) && pass_lostHits_conVeto(LepGood1_lostHits,LepGood1_convVeto) );

}

/////////////////////////////////////////////////////
//
// Following commented functions are work in progress
// Problems in using string
//
/////////////////////////////////////////////////////

// bool pass_workingPointIDnoIso_2016(const string workingPoint = "loose", // loose, medium, tight
// 				   const bool  isEB = true, 
// 				   const int   LepGood1_tightId = -1, 
// 				   const float LepGood1_dxy = -999, 
// 				   const float LepGood1_dz = -999,
// 				   const int   LepGood1_lostHits = -1,
// 				   const int   LepGood1_convVeto = -999
// 				   ) 
// {

//   if      (workingPoint == "loose" ) return pass_looseIDnoIso_2016(  isEB,LepGood1_tightId,LepGood1_dxy,LepGood1_dz,LepGood1_lostHits,LepGood1_convVeto);
//   else if (workingPoint == "medium") return pass_mediumIDnoIso_2016( isEB,LepGood1_tightId,LepGood1_dxy,LepGood1_dz,LepGood1_lostHits,LepGood1_convVeto);
//   else if (workingPoint == "tight" ) return pass_tightIDnoIso_2016(  isEB,LepGood1_tightId,LepGood1_dxy,LepGood1_dz,LepGood1_lostHits,LepGood1_convVeto);
//   else {
//     cout << "Error in function pass_workingPointIDnoIso_2016(): undefined working point "<< workingPoint << ", please check. Exiting ..." <<endl;
//     exit(EXIT_FAILURE);
//   }

// }


// bool pass_isolation_2016(const string workingPoint = "loose", // loose, medium, tight, custom
// 			 const bool   isEB = true,
// 			 const float  LepGood1_relIso04EA = -1,
// 			 )
// {

//   // WARNING: test that strings are accepted by mc*.py, currently they are not
//   // function format should be compatible with TTre::Draw()
//   std::map<string,float> workingPointIsolation_EB;
//   workingPointIsolation_EB["veto"  ] = 0.175; 
//   workingPointIsolation_EB["loose" ] = 0.0994; 
//   workingPointIsolation_EB["medium"] = 0.0695; 
//   workingPointIsolation_EB["tight" ] = 0.0588; 
//   workingPointIsolation_EB["custom"] = 0.2; 
//   std::map<std::string,float> workingPointIsolation_EE;
//   workingPointIsolation_EE["veto"  ] = 0.159; 
//   workingPointIsolation_EE["loose" ] = 0.107; 
//   workingPointIsolation_EE["medium"] = 0.0821; 
//   workingPointIsolation_EE["tight" ] = 0.0571; 
//   workingPointIsolation_EE["custom"] = 0.0821;

//   if (isEB) return LepGood1_relIso04EA < workingPointIsolation_EB[workingPoint];
//   else      return LepGood1_relIso04EA < workingPointIsolation_EE[workingPoint];

// }

// bool passFakerateNumerator2016(const string workingPoint = "loose", // loose, medium, tight
// 			       const bool   isEB = true, 
// 			       const int    LepGood1_tightId = -1, 
// 			       const float  LepGood1_dxy = -999, 
// 			       const float  LepGood1_dz = -999,
// 			       const int    LepGood1_lostHits = -1,
// 			       const int    LepGood1_convVeto = -999,
// 			       const float  LepGood1_relIso04EA = -1,
// 			       const bool   useCustomRelIso04EA = true // use user defined isolation threshold, not the E/gamma value
// 			       ) 
// {

//   return (pass_workingPointIDnoIso_2016(workingPoint,isEB,LepGood1_tightId,LepGood1_dxy,LepGood1_dz,LepGood1_lostHits,LepGood1_convVeto) 
// 	  && 
// 	  pass_isolation_2016(workingPoint,isEB,LepGood1_relIso04EA,useCustomRelIso04EA)
// 	  );

// }


// bool isInFakerateApplicationRegion2016(const string workingPoint = "loose", // loose, medium, tight
// 				       const bool   isEB = true, 
// 				       const int    LepGood1_tightId = -1, 
// 				       const float  LepGood1_dxy = -999, 
// 				       const float  LepGood1_dz = -999,
// 				       const int    LepGood1_lostHits = -1,
// 				       const int    LepGood1_convVeto = -999,
// 				       const float  LepGood1_relIso04EA = -1,
// 				       const bool   useCustomRelIso04EA = true // use user defined isolation threshold, not the E/gamma value
// 				       ) 
// {

//   return (not passFakerateNumerator2016(workingPoint,isEB,
// 					LepGood1_tightId,LepGood1_dxy,LepGood1_dz,LepGood1_lostHits,LepGood1_convVeto,
// 					LepGood1_relIso04EA,useCustomRelIso04EA
// 					)
// 	  );

// }

//==========================

bool pass_isolation_WP(const bool isEB = true, const float  LepGood1_relIso04EA = -1)
{
  // custom WP for 2016 data (before final Legacy ReReco, it could be changed for the new last one)
  return (LepGood1_relIso04EA < (isEB ? 0.2 : 0.0821)); // custom value for EB, medium WP for EE
}

//==========================

bool pass_looseIsolation_2016(const bool   isEB = true,
			      const float  LepGood1_relIso04EA = -1
			      )
{

  if (isEB) return LepGood1_relIso04EA < 0.0994;
  else      return LepGood1_relIso04EA < 0.107;

}

//==========================


bool pass_mediumIsolation_2016(const bool   isEB = true,
			       const float  LepGood1_relIso04EA = -1
			       )
{

  if (isEB) return LepGood1_relIso04EA < 0.0695;
  else      return LepGood1_relIso04EA < 0.0821;

}

//==========================


bool pass_tightIsolation_2016(const bool   isEB = true,
			      const float  LepGood1_relIso04EA = -1
			      )
{

  if (isEB) return LepGood1_relIso04EA < 0.0588;
  else      return LepGood1_relIso04EA < 0.0571;

}

//==========================

bool pass_FakerateNumerator_loose2016(const bool   isEB = true, 
				      const int    LepGood1_tightId = -1, 
				      const float  LepGood1_dxy = -999, 
				      const float  LepGood1_dz = -999,
				      const int    LepGood1_lostHits = -1,
				      const int    LepGood1_convVeto = -999,
				      const float  LepGood1_relIso04EA = -1
				      ) 
{
  
    return (pass_looseIDnoIso_2016(isEB,LepGood1_tightId,LepGood1_dxy,LepGood1_dz,LepGood1_lostHits,LepGood1_convVeto)
	    && 
	    pass_looseIsolation_2016(isEB,LepGood1_relIso04EA)
	    );

}

//============================================

bool pass_FakerateNumerator_medium2016(const bool   isEB = true, 
				       const int    LepGood1_tightId = -1, 
				       const float  LepGood1_dxy = -999, 
				       const float  LepGood1_dz = -999,
				       const int    LepGood1_lostHits = -1,
				       const int    LepGood1_convVeto = -999,
				       const float  LepGood1_relIso04EA = -1
				       ) 
{
  
    return (pass_mediumIDnoIso_2016(isEB,LepGood1_tightId,LepGood1_dxy,LepGood1_dz,LepGood1_lostHits,LepGood1_convVeto)
	    && 
	    pass_mediumIsolation_2016(isEB,LepGood1_relIso04EA)
	    );

}

//============================================

bool pass_FakerateNumerator2016(const bool   isEB = true, 
				const int    LepGood1_tightId = -1, 
				const float  LepGood1_dxy = -999, 
				const float  LepGood1_dz = -999,
				const int    LepGood1_lostHits = -1,
				const int    LepGood1_convVeto = -999,
				const float  LepGood1_relIso04EA = -1
				) 
{

  // EB, loose ID + iso < 0.2
  // EE full medium ID + iso

  if (isEB) {
    return (pass_looseIDnoIso_2016(isEB,LepGood1_tightId,LepGood1_dxy,LepGood1_dz,LepGood1_lostHits,LepGood1_convVeto)
	    && 
	    pass_isolation_WP(isEB,LepGood1_relIso04EA)
	    );
  } else {
    return (pass_mediumIDnoIso_2016(isEB,LepGood1_tightId,LepGood1_dxy,LepGood1_dz,LepGood1_lostHits,LepGood1_convVeto)
	    &&
	    pass_isolation_WP(isEB,LepGood1_relIso04EA)
	    );
  }

}

//==========================


bool pass_FakerateApplicationRegion2016(const bool   isEB = true, 
					const int    LepGood1_tightId = -1, 
					const float  LepGood1_dxy = -999, 
					const float  LepGood1_dz = -999,
					const int    LepGood1_lostHits = -1,
					const int    LepGood1_convVeto = -999,
					const float  LepGood1_relIso04EA = -1
					) 
{

  return (not pass_FakerateNumerator2016(isEB,LepGood1_tightId,LepGood1_dxy,LepGood1_dz,LepGood1_lostHits,LepGood1_convVeto,LepGood1_relIso04EA));

}


//==================================================

bool pass_FakerateNum_debug(const bool  isEB = true, 
			    const int   LepGood1_tightId = -1, 
			    const float LepGood1_dxy = -999, 
			    const float LepGood1_dz = -999,
			    const int   LepGood1_lostHits = -1,
			    const int   LepGood1_convVeto = -999,
			    const float LepGood1_relIso04EA = -1
			    ) 
{

  // EB, loose ID + iso < 0.2
  // EE full medium ID + iso

  if (isEB) {
    return (LepGood1_tightId >= 1 && abs(LepGood1_dxy) <= 0.05 && abs(LepGood1_dxy) <= 0.1 && LepGood1_lostHits <= 1 && LepGood1_convVeto == 1 && LepGood1_relIso04EA <= 0.2);
  } else {
    return (LepGood1_tightId >= 2 && abs(LepGood1_dxy) <= 0.1 && abs(LepGood1_dxy) <= 0.2 && LepGood1_lostHits <= 1 && LepGood1_convVeto == 1 && LepGood1_relIso04EA <= 0.0821);
  }

}
//==================================================


// call like 
// tkmt_tkmetEleCorr(met_trkPt,
// 		     met_trkPhi,
// 		     ptElFull(LepGood1_calPt,LepGood1_eta),
// 		     LepGood_phi, 
// 		     pass_dxy_dz(abs(LepGood1_eta)<1.479, LepGood1_dxy, LepGood1_dz) && pass_lostHits_conVeto(LepGood1_lostHits, LepGood1_convVeto))


float tkmt_tkmetEleCorr(float tkmet_pt, float tkmet_phi, float lep_pt, float lep_phi, bool eleTrackIsVertexCompatible) {

  if (eleTrackIsVertexCompatible) {

    return mt_2(tkmet_pt, tkmet_phi, lep_pt, lep_phi);

  } else {

    // when the electron is not compatible with the primary vertex, its track is not used to compute tkMet (it is a bug in our ntuples)
    // in that case, add the electron back
    // We have the following (assuming vectorial object in the equation)
    // TkMEt_corr = -Sum(pT_tracks_noBadEle) - pT_badEle
    // in the ntuples we have TkMEt = -Sum(pT_tracks_noBadEle)

    // here we define the tkMet as the wrong one and will correct later (we avoid declaring 2 TVector2) 
    TVector2 trkmet_corr; trkmet_corr.SetMagPhi(tkmet_pt, tkmet_phi);  
    TVector2 badEle;      badEle.SetMagPhi(lep_pt,lep_phi);
    trkmet_corr -= badEle;

    return mt_2(trkmet_corr.Mod(),trkmet_corr.Phi(),lep_pt,lep_phi);

  }

}

//==================================================

int Binnumberset1D(float BDTx,float BDTy){
  /*
    //v3
  if(BDTx <=0.25 && BDTy > 0.2)return 1;
  if(BDTx > 0.25 && BDTx <= 0.7 && BDTy >= 0.65) return 2;
  if(BDTx > 0.5 && BDTx <= 0.7 && BDTy > 0.25 && BDTy <=0.65) return 3;
  if(BDTx > 0.7 && BDTy > 0.25 && BDTy <=0.65 ) return 4;
  if(BDTx > 0.95 && BDTy > 0.65 && BDTy <=0.95) return 5;
  if(BDTx >0.25 && BDTx <=0.5 && BDTy > 0.2  && BDTy <= 0.45)return 6;
  if(BDTx <=0.5 && BDTy <= 0.2)return 7;
  if(BDTx > 0.8 && BDTx <= 0.9 && BDTy > 0.65 && BDTy <=0.85) return 8;
  if(BDTx > 0.95 && BDTy > 0.95 ) return 9;
  if(BDTx >0.8 &&  BDTx <= 0.9 && BDTy > 0.85 ) return 10;
  if(BDTx >0.25 && BDTx <=0.5 && BDTy > 0.45  && BDTy <= 0.65)return 11;
  if(BDTx >0.9 &&  BDTx <= 0.95 && BDTy > 0.65 && BDTy <=0.9) return 12;
  if(BDTx >0.7 &&  BDTx <= 0.8 && BDTy > 0.65 ) return 13;
  if(BDTx >0.9 && BDTx <= 0.95 && BDTy > 0.9)return 14;
  if(BDTx >0.5 && BDTy <= 0.25)return 15;
  
  //v2
  float a=0.35; float b=0.4; float c=0.6; float d=0.75; float e=0.8; float f =0.95;
  if(BDTx <= 0.15 && BDTy <=b) return 4;
  if(BDTx > 0.15 &&  BDTx <= 0.4 && BDTy <=0.4) return 2;
  if(BDTx > 0.4  && BDTy <=b) return 5;
  if(BDTx <=0.35 && BDTy > b && BDTy <=e) return 11;
  if(BDTx >0.35 && BDTx <=0.6 && BDTy > b && BDTy <=0.6) return 12;
  if(BDTx >0.35 && BDTx <=0.6 && BDTy > 0.6 && BDTy <=e) return 10;

  if(BDTx > 0.6  && BDTx <=e  && BDTy > b && BDTy <=c) return 6;
  if(BDTx > 0.6  && BDTx <=e  && BDTy > c && BDTy <=e) return 3;
  if(BDTx > e && BDTx <=f && BDTy > b && BDTy <=0.85) return 1;
  if(BDTx > f   && BDTy > b && BDTy <=0.9) return 9;
  if(BDTx > f   && BDTy > 0.9 && BDTy <=f) return 14;
  if(BDTx > f   && BDTy > f ) return 7;
  if(BDTx > e && BDTx <=f  && BDTy > 0.85 && BDTy <=0.9 ) return 8;
  if(BDTx > e && BDTx <=f  && BDTy >0.9 ) return 15;
  if(BDTx <=0.8  && BDTy >e ) return 13;

  //v4
  if(BDTx <=0.25 && BDTy > 0.2)return 1;
  if(BDTx > 0.25 && BDTx <= 0.7 && BDTy >= 0.65) return 2;
  if(BDTx > 0.5 && BDTx <= 0.7 && BDTy <=0.65) return 3;
  if(BDTx > 0.95 && BDTy > 0.65 && BDTy <=0.95) return 4;
  if(BDTx >0.25 && BDTx <=0.5 && BDTy > 0.2  && BDTy <= 0.45)return 5;
  if(BDTx <=0.5 && BDTy <= 0.2)return 6;
  if(BDTx > 0.8 && BDTx <= 0.9 && BDTy > 0.65 && BDTy <=0.85) return 7;
  if(BDTx > 0.7 && BDTy >0.5  && BDTy <=0.65) return 8;
  if(BDTx >0.8 &&  BDTx <= 0.9 && BDTy > 0.85 ) return 9;
  if(BDTx > 0.95 && BDTy > 0.95 ) return 10;
  if(BDTx >0.25 && BDTx <=0.5 && BDTy > 0.45  && BDTy <= 0.65)return 11;
  if(BDTx >0.9 &&  BDTx <= 0.95 && BDTy > 0.65 && BDTy <=0.9) return 12;
  if(BDTx > 0.7 && BDTy <=0.5 ) return 13;
  if(BDTx >0.7 &&  BDTx <= 0.8 && BDTy > 0.65 ) return 14;
  if(BDTx >0.9 && BDTx <= 0.95 && BDTy > 0.9)return 15;

  //v5
  if(BDTx <=0.25 && BDTy > 0.2)return 1;
  if(BDTx > 0.25 && BDTx <= 0.7 && BDTy >= 0.65) return 2;
  if(BDTx > 0.5 && BDTx <= 0.7 && BDTy <=0.65) return 3;
  if(BDTx > 0.95 && BDTy > 0.65 && BDTy <=0.9) return 10;
  if(BDTx >0.25 && BDTx <=0.5 && BDTy > 0.2  && BDTy <= 0.45)return 5;
  if(BDTx <=0.5 && BDTy <= 0.2)return 6;
  if(BDTx > 0.8 && BDTx <= 0.9 && BDTy > 0.65 && BDTy <=0.85) return 7;
  if(BDTx > 0.7 && BDTy >0.5  && BDTy <=0.65) return 8;
  if(BDTx >0.8 &&  BDTx <= 0.9 && BDTy > 0.85 ) return 9;
  if(BDTx > 0.95 && BDTy > 0.9 ) return 4;
  if(BDTx >0.25 && BDTx <=0.5 && BDTy > 0.45  && BDTy <= 0.65)return 11;
  if(BDTx >0.9 &&  BDTx <= 0.95 && BDTy > 0.65 && BDTy <=0.9) return 12;
  if(BDTx > 0.7 && BDTy <=0.5 ) return 13;
  if(BDTx >0.7 &&  BDTx <= 0.8 && BDTy > 0.65 ) return 14;
  if(BDTx >0.9 && BDTx <= 0.95 && BDTy > 0.9)return 15;
  */
  //v6
  if(BDTx <=0.25 && BDTy > 0.2)return 1;
  if(BDTx > 0.25 && BDTx <= 0.7 && BDTy >= 0.65) return 2;
  if(BDTx > 0.5 && BDTx <= 0.7 && BDTy <=0.65) return 3;
  if(BDTx > 0.95 && BDTy > 0.65 && BDTy <=0.95) return 4;
  if(BDTx >0.25 && BDTx <=0.5 && BDTy > 0.2  && BDTy <= 0.45)return 5;
  if(BDTx <=0.5 && BDTy <= 0.2)return 6;
  if(BDTx > 0.8 && BDTx <= 0.9 && BDTy > 0.65 && BDTy <=0.85) return 7;
  if(BDTx > 0.7 && BDTy >0.5  && BDTy <=0.65) return 8;
  if(BDTx >0.8 &&  BDTx <= 0.9 && BDTy > 0.85 ) return 9;
  if(BDTx > 0.95 && BDTx <= 0.975 && BDTy > 0.95 &&  BDTy <= 0.975) return 10;
  if(BDTx >0.25 && BDTx <=0.5 && BDTy > 0.45  && BDTy <= 0.65)return 11;
  if(BDTx >0.9 &&  BDTx <= 0.95 && BDTy > 0.65) return 12;
  if(BDTx > 0.7 && BDTy <=0.5 ) return 13;
  if(BDTx >0.7 &&  BDTx <= 0.8 && BDTy > 0.65 ) return 14;
  if(BDTx > 0.975 && BDTy > 0.975 ) return 15;


}




void functions() {}

//#endif
