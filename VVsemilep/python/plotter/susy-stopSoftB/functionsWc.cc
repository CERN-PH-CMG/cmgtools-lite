#include <cmath>
#include "Math/GenVector/LorentzVector.h"
#include "Math/GenVector/PtEtaPhiM4D.h"
#include "Math/GenVector/PxPyPzM4D.h"

//// UTILITY FUNCTIONS NOT IN TFORMULA ALREADY

float m_D_Kpp(float qpt1, float eta1, float qpt2, float eta2, float phi12, float qpt3, float eta3, float phi13) {
    typedef ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double> > PtEtaPhiMVector;
    float m1 = 0.1396, m2 = 0.1396, m3 = 0.1396;
    float qtot = qpt1*qpt2*qpt3;
    if      (qtot*qpt1 > 0) m1 = 0.4937;
    else if (qtot*qpt2 > 0) m2 = 0.4937;
    else if (qtot*qpt3 > 0) m3 = 0.4937;
    PtEtaPhiMVector p41(std::abs(qpt1),eta1,0.0,  m1);
    PtEtaPhiMVector p42(std::abs(qpt2),eta2,phi12,m2);
    PtEtaPhiMVector p43(std::abs(qpt3),eta3,phi13,m3);
    return (p41+p42+p43).M();
}


void functionsWc() {}





