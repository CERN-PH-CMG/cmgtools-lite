#include "TVector2.h"
float pt_o1_o2(float o1_pt, float o1_phi, float o2_pt, float o2_phi)
{
  TVector2 o1; o1.SetMagPhi(o1_pt, o1_phi);
  TVector2 o2; o2.SetMagPhi(o2_pt, o2_phi);
  return (o1+o2).Mod();

}

int categories3l(float mZ, int nbjets, int charge_sum){

  if (abs(mZ-91.2) > 10){
    if (nbjets == 1){
      if (charge_sum < 0) return 1;
      else              return 2;
    }
    else{
      if (charge_sum < 0) return 3;
      else              return 4;
    }
  }
  else{
    if (nbjets == 1) return 5;
    else return 6;
  }


}

float categories2l( int charge1, int nbjets){
  
  if (charge1 < 0 && nbjets > 2){
    return 1;
  }
  else if (charge1 > 0 && nbjets > 2){
    return 2;
  }
  else if (charge1 < 0 && nbjets <= 2){
    return 3;
  }
  else if (charge1 > 0 && nbjets <= 2){
    return 4;
  }
  else return 0;

}

float njet_rewighting_TTZ( float njet30 ){
  if (njet30 == 0) return 0.999109;
  else if (njet30 == 1) return 0.991581;
  else if (njet30 == 2) return 0.975370;
  else if (njet30 == 3) return 0.963591;
  else if (njet30 == 4) return 0.949661;
  else if (njet30 == 5) return 0.924440;
  else if (njet30 == 6) return 0.904931;
  else if (njet30 == 7) return 0.826180;
  else return 0.826180;
}
float njet_rewighting_ZZ( float njet30 ){
  if (njet30 == 0) return 0.995479;
  else if (njet30 == 1) return 0.919387;
  else if (njet30 == 2) return 0.888784;
  else if (njet30 == 3) return 0.861565;
  else if (njet30 == 4) return 0.822855;
  else if (njet30 == 5) return 0.808218;
  else if (njet30 == 6) return 0.900529;
  else if (njet30 == 7) return 0.745352;
  else return 0.745352;
}
float njet_rewighting_WZ( float njet30 ){
  if (njet30 == 0) return 0.999539;
  else if (njet30 == 1) return 0.994151;
  else if (njet30 == 2) return 0.971694;
  else if (njet30 == 3) return 0.939267;
  else if (njet30 == 4) return 0.888235;
  else if (njet30 == 5) return 0.870577;
  else if (njet30 == 6) return 0.805650;
  else if (njet30 == 7) return 0.742035;
  else return 0.742035;
}
