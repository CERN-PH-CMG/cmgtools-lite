double FastSimTriggerEfficiency(double HT, double l1_Pt, int l1_pdgId, double l2_Pt, int l2_pdgId) {
  double pt1, pt2, pdgid1, pdgid2; 
  //Sort leptons: electrons first, then muons
  //Amongst the same flavor, sort by pt

  if(abs(l1_pdgId) == abs(l2_pdgId)){
    pt1 = (l1_Pt>l2_Pt)? l1_Pt: l2_Pt ; 
    pt2 = (l1_Pt>l2_Pt)? l2_Pt: l1_Pt ; 
  }
  else{
    pt1= (abs(l1_pdgId)< abs(l2_pdgId))? l1_Pt:l2_Pt; 
    pt2= (abs(l1_pdgId)< abs(l2_pdgId))? l2_Pt:l1_Pt; 
  } 



  if(HT>80 && HT<=150){
    if(abs(l1_pdgId)+abs(l2_pdgId) ==22){
      if(pt1>25. && pt1<=35. && pt2>15. && pt2<=20.) return 0.901454;
      if(pt1>25. && pt1<=35. && pt2>20. && pt2<=25.) return 0.942286;
      if(pt1>25. && pt1<=35. && pt2>25. && pt2<=35.) return 0.957884;
      if(pt1>35. && pt1<=45. && pt2>15. && pt2<=20.) return 0.915385;
      if(pt1>35. && pt1<=45. && pt2>20. && pt2<=25.) return 0.934807;
      if(pt1>35. && pt1<=45. && pt2>25. && pt2<=35.) return 0.95;
      if(pt1>35. && pt1<=45. && pt2>35. && pt2<=45.) return 0.957918;
      if(pt1>45. && pt1<=100. && pt2>15. && pt2<=20.) return 0.9128;
      if(pt1>45. && pt1<=100. && pt2>20. && pt2<=25.) return 0.955773;
      if(pt1>45. && pt1<=100. && pt2>25. && pt2<=35.) return 0.96567;
      if(pt1>45. && pt1<=100. && pt2>35. && pt2<=45.) return 0.969886;
      if(pt1>45. && pt1<=100. && pt2>45. && pt2<=100.) return 0.976102;
      if(pt1>100. && pt2>15. && pt2<=20.) return 0.915323;
      if(pt1>100. && pt2>20. && pt2<=25.) return 0.94704;
      if(pt1>100. && pt2>25. && pt2<=35.) return 0.963359;
      if(pt1>100. && pt2>35. && pt2<=45.) return 0.967742;
      if(pt1>100. && pt2>45. && pt2<=100.) return 0.983276;
      if(pt1>100. && pt2>100.) return 0.986301;
    }
    else if(abs(l1_pdgId)+abs(l2_pdgId) ==24){
      if(pt1>15. && pt1<=20. && pt2>25. && pt2<=35.) return 0.873717;
      if(pt1>15. && pt1<=20. && pt2>35. && pt2<=45.) return 0.870614;
      if(pt1>15. && pt1<=20. && pt2>45. && pt2<=100.) return 0.896967;
      if(pt1>15. && pt1<=20. && pt2>100.) return 0.895973;
      if(pt1>20. && pt1<=25. && pt2>25. && pt2<=35.) return 0.923441;
      if(pt1>20. && pt1<=25. && pt2>35. && pt2<=45.) return 0.934142;
      if(pt1>20. && pt1<=25. && pt2>45. && pt2<=100.) return 0.928716;
      if(pt1>20. && pt1<=25. && pt2>100.) return 0.93617;
      if(pt1>25. && pt1<=35. && pt2>10. && pt2<=15.) return 0.921466;
      if(pt1>25. && pt1<=35. && pt2>15. && pt2<=20.) return 0.934702;
      if(pt1>25. && pt1<=35. && pt2>20. && pt2<=25.) return 0.93576;
      if(pt1>25. && pt1<=35. && pt2>25. && pt2<=35.) return 0.936442;
      if(pt1>25. && pt1<=35. && pt2>35. && pt2<=45.) return 0.942179;
      if(pt1>25. && pt1<=35. && pt2>45. && pt2<=100.) return 0.942545;
      if(pt1>25. && pt1<=35. && pt2>100.) return 0.941558;
      if(pt1>35. && pt1<=45. && pt2>10. && pt2<=15.) return 0.928756;
      if(pt1>35. && pt1<=45. && pt2>15. && pt2<=20.) return 0.943327;
      if(pt1>35. && pt1<=45. && pt2>20. && pt2<=25.) return 0.952617;
      if(pt1>35. && pt1<=45. && pt2>25. && pt2<=35.) return 0.951613;
      if(pt1>35. && pt1<=45. && pt2>35. && pt2<=45.) return 0.955859;
      if(pt1>35. && pt1<=45. && pt2>45. && pt2<=100.) return 0.954449;
      if(pt1>35. && pt1<=45. && pt2>100.) return 0.960159;
      if(pt1>45. && pt1<=100. && pt2>10. && pt2<=15.) return 0.942029;
      if(pt1>45. && pt1<=100. && pt2>15. && pt2<=20.) return 0.957756;
      if(pt1>45. && pt1<=100. && pt2>20. && pt2<=25.) return 0.949438;
      if(pt1>45. && pt1<=100. && pt2>25. && pt2<=35.) return 0.95452;
      if(pt1>45. && pt1<=100. && pt2>35. && pt2<=45.) return 0.952258;
      if(pt1>45. && pt1<=100. && pt2>45. && pt2<=100.) return 0.95515;
      if(pt1>45. && pt1<=100. && pt2>100.) return 0.949413;
      if(pt1>100. && pt2>10. && pt2<=15.) return 0.959654;
      if(pt1>100. && pt2>15. && pt2<=20.) return 0.937931;
      if(pt1>100. && pt2>20. && pt2<=25.) return 0.962076;
      if(pt1>100. && pt2>25. && pt2<=35.) return 0.969893;
      if(pt1>100. && pt2>35. && pt2<=45.) return 0.961538;
      if(pt1>100. && pt2>45. && pt2<=100.) return 0.950055;
      if(pt1>100. && pt2>100.) return 0.968534;
    }
    else if(abs(l1_pdgId)+abs(l2_pdgId) ==26){
      if(pt1>25. && pt1<=35. && pt2>10. && pt2<=15.) return 0.945614;
      if(pt1>25. && pt1<=35. && pt2>15. && pt2<=20.) return 0.950939;
      if(pt1>25. && pt1<=35. && pt2>20. && pt2<=25.) return 0.951076;
      if(pt1>25. && pt1<=35. && pt2>25. && pt2<=35.) return 0.960113;
      if(pt1>35. && pt1<=45. && pt2>10. && pt2<=15.) return 0.928707;
      if(pt1>35. && pt1<=45. && pt2>15. && pt2<=20.) return 0.958694;
      if(pt1>35. && pt1<=45. && pt2>20. && pt2<=25.) return 0.957458;
      if(pt1>35. && pt1<=45. && pt2>25. && pt2<=35.) return 0.956865;
      if(pt1>35. && pt1<=45. && pt2>35. && pt2<=45.) return 0.958692;
      if(pt1>45. && pt1<=100. && pt2>10. && pt2<=15.) return 0.945736;
      if(pt1>45. && pt1<=100. && pt2>15. && pt2<=20.) return 0.953125;
      if(pt1>45. && pt1<=100. && pt2>20. && pt2<=25.) return 0.960789;
      if(pt1>45. && pt1<=100. && pt2>25. && pt2<=35.) return 0.958855;
      if(pt1>45. && pt1<=100. && pt2>35. && pt2<=45.) return 0.955881;
      if(pt1>45. && pt1<=100. && pt2>45. && pt2<=100.) return 0.955658;
      if(pt1>100. && pt2>10. && pt2<=15.) return 0.940191;
      if(pt1>100. && pt2>15. && pt2<=20.) return 0.946869;
      if(pt1>100. && pt2>20. && pt2<=25.) return 0.957447;
      if(pt1>100. && pt2>25. && pt2<=35.) return 0.961307;
      if(pt1>100. && pt2>35. && pt2<=45.) return 0.958892;
      if(pt1>100. && pt2>45. && pt2<=100.) return 0.950298;
      if(pt1>100. && pt2>100.) return 0.935943;
    }
    else return 0;
  }
  if(HT>150 && HT<=300){
    if(abs(l1_pdgId)+abs(l2_pdgId) ==22){
      if(pt1>25. && pt1<=35. && pt2>15. && pt2<=20.) return 0.902316;
      if(pt1>25. && pt1<=35. && pt2>20. && pt2<=25.) return 0.935867;
      if(pt1>25. && pt1<=35. && pt2>25. && pt2<=35.) return 0.952381;
      if(pt1>35. && pt1<=45. && pt2>15. && pt2<=20.) return 0.896133;
      if(pt1>35. && pt1<=45. && pt2>20. && pt2<=25.) return 0.940891;
      if(pt1>35. && pt1<=45. && pt2>25. && pt2<=35.) return 0.954545;
      if(pt1>35. && pt1<=45. && pt2>35. && pt2<=45.) return 0.960618;
      if(pt1>45. && pt1<=100. && pt2>15. && pt2<=20.) return 0.919115;
      if(pt1>45. && pt1<=100. && pt2>20. && pt2<=25.) return 0.94696;
      if(pt1>45. && pt1<=100. && pt2>25. && pt2<=35.) return 0.957937;
      if(pt1>45. && pt1<=100. && pt2>35. && pt2<=45.) return 0.969733;
      if(pt1>45. && pt1<=100. && pt2>45. && pt2<=100.) return 0.975612;
      if(pt1>100. && pt2>15. && pt2<=20.) return 0.910321;
      if(pt1>100. && pt2>20. && pt2<=25.) return 0.949509;
      if(pt1>100. && pt2>25. && pt2<=35.) return 0.966376;
      if(pt1>100. && pt2>35. && pt2<=45.) return 0.97209;
      if(pt1>100. && pt2>45. && pt2<=100.) return 0.97965;
      if(pt1>100. && pt2>100.) return 0.983429;
    }
    else if(abs(l1_pdgId)+abs(l2_pdgId) ==24){
      if(pt1>15. && pt1<=20. && pt2>25. && pt2<=35.) return 0.868211;
      if(pt1>15. && pt1<=20. && pt2>35. && pt2<=45.) return 0.882721;
      if(pt1>15. && pt1<=20. && pt2>45. && pt2<=100.) return 0.883999;
      if(pt1>15. && pt1<=20. && pt2>100.) return 0.870219;
      if(pt1>20. && pt1<=25. && pt2>25. && pt2<=35.) return 0.926146;
      if(pt1>20. && pt1<=25. && pt2>35. && pt2<=45.) return 0.912413;
      if(pt1>20. && pt1<=25. && pt2>45. && pt2<=100.) return 0.926985;
      if(pt1>20. && pt1<=25. && pt2>100.) return 0.914962;
      if(pt1>25. && pt1<=35. && pt2>10. && pt2<=15.) return 0.927951;
      if(pt1>25. && pt1<=35. && pt2>15. && pt2<=20.) return 0.934032;
      if(pt1>25. && pt1<=35. && pt2>20. && pt2<=25.) return 0.940945;
      if(pt1>25. && pt1<=35. && pt2>25. && pt2<=35.) return 0.933834;
      if(pt1>25. && pt1<=35. && pt2>35. && pt2<=45.) return 0.93512;
      if(pt1>25. && pt1<=35. && pt2>45. && pt2<=100.) return 0.941769;
      if(pt1>25. && pt1<=35. && pt2>100.) return 0.940374;
      if(pt1>35. && pt1<=45. && pt2>10. && pt2<=15.) return 0.933817;
      if(pt1>35. && pt1<=45. && pt2>15. && pt2<=20.) return 0.946082;
      if(pt1>35. && pt1<=45. && pt2>20. && pt2<=25.) return 0.950611;
      if(pt1>35. && pt1<=45. && pt2>25. && pt2<=35.) return 0.946244;
      if(pt1>35. && pt1<=45. && pt2>35. && pt2<=45.) return 0.947135;
      if(pt1>35. && pt1<=45. && pt2>45. && pt2<=100.) return 0.948951;
      if(pt1>35. && pt1<=45. && pt2>100.) return 0.947566;
      if(pt1>45. && pt1<=100. && pt2>10. && pt2<=15.) return 0.939487;
      if(pt1>45. && pt1<=100. && pt2>15. && pt2<=20.) return 0.949677;
      if(pt1>45. && pt1<=100. && pt2>20. && pt2<=25.) return 0.947852;
      if(pt1>45. && pt1<=100. && pt2>25. && pt2<=35.) return 0.955468;
      if(pt1>45. && pt1<=100. && pt2>35. && pt2<=45.) return 0.952626;
      if(pt1>45. && pt1<=100. && pt2>45. && pt2<=100.) return 0.953233;
      if(pt1>45. && pt1<=100. && pt2>100.) return 0.952798;
      if(pt1>100. && pt2>10. && pt2<=15.) return 0.938119;
      if(pt1>100. && pt2>15. && pt2<=20.) return 0.951521;
      if(pt1>100. && pt2>20. && pt2<=25.) return 0.955197;
      if(pt1>100. && pt2>25. && pt2<=35.) return 0.94905;
      if(pt1>100. && pt2>35. && pt2<=45.) return 0.953109;
      if(pt1>100. && pt2>45. && pt2<=100.) return 0.949548;
      if(pt1>100. && pt2>100.) return 0.944965;
    }
    else if(abs(l1_pdgId)+abs(l2_pdgId) ==26){
      if(pt1>25. && pt1<=35. && pt2>10. && pt2<=15.) return 0.944513;
      if(pt1>25. && pt1<=35. && pt2>15. && pt2<=20.) return 0.952299;
      if(pt1>25. && pt1<=35. && pt2>20. && pt2<=25.) return 0.956522;
      if(pt1>25. && pt1<=35. && pt2>25. && pt2<=35.) return 0.95232;
      if(pt1>35. && pt1<=45. && pt2>10. && pt2<=15.) return 0.944979;
      if(pt1>35. && pt1<=45. && pt2>15. && pt2<=20.) return 0.955279;
      if(pt1>35. && pt1<=45. && pt2>20. && pt2<=25.) return 0.957053;
      if(pt1>35. && pt1<=45. && pt2>25. && pt2<=35.) return 0.956792;
      if(pt1>35. && pt1<=45. && pt2>35. && pt2<=45.) return 0.953535;
      if(pt1>45. && pt1<=100. && pt2>10. && pt2<=15.) return 0.94373;
      if(pt1>45. && pt1<=100. && pt2>15. && pt2<=20.) return 0.951135;
      if(pt1>45. && pt1<=100. && pt2>20. && pt2<=25.) return 0.955552;
      if(pt1>45. && pt1<=100. && pt2>25. && pt2<=35.) return 0.956778;
      if(pt1>45. && pt1<=100. && pt2>35. && pt2<=45.) return 0.956169;
      if(pt1>45. && pt1<=100. && pt2>45. && pt2<=100.) return 0.952121;
      if(pt1>100. && pt2>10. && pt2<=15.) return 0.946903;
      if(pt1>100. && pt2>15. && pt2<=20.) return 0.959514;
      if(pt1>100. && pt2>20. && pt2<=25.) return 0.95028;
      if(pt1>100. && pt2>25. && pt2<=35.) return 0.951219;
      if(pt1>100. && pt2>35. && pt2<=45.) return 0.947489;
      if(pt1>100. && pt2>45. && pt2<=100.) return 0.942206;
      if(pt1>100. && pt2>100.) return 0.943656;
    }
    else return 0;
  }
  if(HT>300 && HT<=350){
    if(abs(l1_pdgId)+abs(l2_pdgId) ==22){
      if(pt1>15. && pt1<=20. && pt2>15. && pt2<=20.) return 0.6;
      if(pt1>20. && pt1<=25. && pt2>15. && pt2<=20.) return 0.722222;
      if(pt1>20. && pt1<=25. && pt2>20. && pt2<=25.) return 0.657143;
      if(pt1>25. && pt1<=35. && pt2>15. && pt2<=20.) return 0.817518;
      if(pt1>25. && pt1<=35. && pt2>20. && pt2<=25.) return 0.825503;
      if(pt1>25. && pt1<=35. && pt2>25. && pt2<=35.) return 0.892655;
      if(pt1>35. && pt1<=45. && pt2>15. && pt2<=20.) return 0.927083;
      if(pt1>35. && pt1<=45. && pt2>20. && pt2<=25.) return 0.906475;
      if(pt1>35. && pt1<=45. && pt2>25. && pt2<=35.) return 0.929825;
      if(pt1>35. && pt1<=45. && pt2>35. && pt2<=45.) return 0.980519;
      if(pt1>45. && pt1<=100. && pt2>15. && pt2<=20.) return 0.888889;
      if(pt1>45. && pt1<=100. && pt2>20. && pt2<=25.) return 0.945137;
      if(pt1>45. && pt1<=100. && pt2>25. && pt2<=35.) return 0.966245;
      if(pt1>45. && pt1<=100. && pt2>35. && pt2<=45.) return 0.976082;
      if(pt1>45. && pt1<=100. && pt2>45. && pt2<=100.) return 0.978176;
      if(pt1>100. && pt2>15. && pt2<=20.) return 0.918699;
      if(pt1>100. && pt2>20. && pt2<=25.) return 0.951049;
      if(pt1>100. && pt2>25. && pt2<=35.) return 0.973422;
      if(pt1>100. && pt2>35. && pt2<=45.) return 0.989583;
      if(pt1>100. && pt2>45. && pt2<=100.) return 0.984314;
      if(pt1>100. && pt2>100.) return 0.989761;
    }
    else if(abs(l1_pdgId)+abs(l2_pdgId) ==24){
      if(pt1>15. && pt1<=20. && pt2>10. && pt2<=15.) return 0.641509;
      if(pt1>15. && pt1<=20. && pt2>15. && pt2<=20.) return 0.741379;
      if(pt1>15. && pt1<=20. && pt2>20. && pt2<=25.) return 0.662162;
      if(pt1>15. && pt1<=20. && pt2>25. && pt2<=35.) return 0.735714;
      if(pt1>15. && pt1<=20. && pt2>35. && pt2<=45.) return 0.844444;
      if(pt1>15. && pt1<=20. && pt2>45. && pt2<=100.) return 0.905063;
      if(pt1>15. && pt1<=20. && pt2>100.) return 0.860759;
      if(pt1>20. && pt1<=25. && pt2>10. && pt2<=15.) return 0.793651;
      if(pt1>20. && pt1<=25. && pt2>15. && pt2<=20.) return 0.71;
      if(pt1>20. && pt1<=25. && pt2>20. && pt2<=25.) return 0.681818;
      if(pt1>20. && pt1<=25. && pt2>25. && pt2<=35.) return 0.73516;
      if(pt1>20. && pt1<=25. && pt2>35. && pt2<=45.) return 0.838889;
      if(pt1>20. && pt1<=25. && pt2>45. && pt2<=100.) return 0.917782;
      if(pt1>20. && pt1<=25. && pt2>100.) return 0.875598;
      if(pt1>25. && pt1<=35. && pt2>10. && pt2<=15.) return 0.847826;
      if(pt1>25. && pt1<=35. && pt2>15. && pt2<=20.) return 0.811111;
      if(pt1>25. && pt1<=35. && pt2>20. && pt2<=25.) return 0.854545;
      if(pt1>25. && pt1<=35. && pt2>25. && pt2<=35.) return 0.886076;
      if(pt1>25. && pt1<=35. && pt2>35. && pt2<=45.) return 0.933649;
      if(pt1>25. && pt1<=35. && pt2>45. && pt2<=100.) return 0.928333;
      if(pt1>25. && pt1<=35. && pt2>100.) return 0.923754;
      if(pt1>35. && pt1<=45. && pt2>10. && pt2<=15.) return 0.894737;
      if(pt1>35. && pt1<=45. && pt2>15. && pt2<=20.) return 0.940476;
      if(pt1>35. && pt1<=45. && pt2>20. && pt2<=25.) return 0.943878;
      if(pt1>35. && pt1<=45. && pt2>25. && pt2<=35.) return 0.913333;
      if(pt1>35. && pt1<=45. && pt2>35. && pt2<=45.) return 0.94837;
      if(pt1>35. && pt1<=45. && pt2>45. && pt2<=100.) return 0.944198;
      if(pt1>35. && pt1<=45. && pt2>100.) return 0.954023;
      if(pt1>45. && pt1<=100. && pt2>10. && pt2<=15.) return 0.951654;
      if(pt1>45. && pt1<=100. && pt2>15. && pt2<=20.) return 0.957895;
      if(pt1>45. && pt1<=100. && pt2>20. && pt2<=25.) return 0.96118;
      if(pt1>45. && pt1<=100. && pt2>25. && pt2<=35.) return 0.961295;
      if(pt1>45. && pt1<=100. && pt2>35. && pt2<=45.) return 0.959322;
      if(pt1>45. && pt1<=100. && pt2>45. && pt2<=100.) return 0.959381;
      if(pt1>45. && pt1<=100. && pt2>100.) return 0.957878;
      if(pt1>100. && pt2>10. && pt2<=15.) return 0.958042;
      if(pt1>100. && pt2>15. && pt2<=20.) return 0.956989;
      if(pt1>100. && pt2>20. && pt2<=25.) return 0.960591;
      if(pt1>100. && pt2>25. && pt2<=35.) return 0.972665;
      if(pt1>100. && pt2>35. && pt2<=45.) return 0.970976;
      if(pt1>100. && pt2>45. && pt2<=100.) return 0.971081;
      if(pt1>100. && pt2>100.) return 0.969887;
    }
    else if(abs(l1_pdgId)+abs(l2_pdgId) ==26){
      if(pt1>10. && pt1<=15. && pt2>10. && pt2<=15.) return 0.866667;
      if(pt1>15. && pt1<=20. && pt2>10. && pt2<=15.) return 0.684783;
      if(pt1>15. && pt1<=20. && pt2>15. && pt2<=20.) return 0.678571;
      if(pt1>20. && pt1<=25. && pt2>10. && pt2<=15.) return 0.740741;
      if(pt1>20. && pt1<=25. && pt2>15. && pt2<=20.) return 0.722222;
      if(pt1>20. && pt1<=25. && pt2>20. && pt2<=25.) return 0.62963;
      if(pt1>25. && pt1<=35. && pt2>10. && pt2<=15.) return 0.70283;
      if(pt1>25. && pt1<=35. && pt2>15. && pt2<=20.) return 0.710037;
      if(pt1>25. && pt1<=35. && pt2>20. && pt2<=25.) return 0.790323;
      if(pt1>25. && pt1<=35. && pt2>25. && pt2<=35.) return 0.672131;
      if(pt1>35. && pt1<=45. && pt2>10. && pt2<=15.) return 0.862637;
      if(pt1>35. && pt1<=45. && pt2>15. && pt2<=20.) return 0.82716;
      if(pt1>35. && pt1<=45. && pt2>20. && pt2<=25.) return 0.87619;
      if(pt1>35. && pt1<=45. && pt2>25. && pt2<=35.) return 0.837174;
      if(pt1>35. && pt1<=45. && pt2>35. && pt2<=45.) return 0.886447;
      if(pt1>45. && pt1<=100. && pt2>10. && pt2<=15.) return 0.915663;
      if(pt1>45. && pt1<=100. && pt2>15. && pt2<=20.) return 0.921283;
      if(pt1>45. && pt1<=100. && pt2>20. && pt2<=25.) return 0.919075;
      if(pt1>45. && pt1<=100. && pt2>25. && pt2<=35.) return 0.912069;
      if(pt1>45. && pt1<=100. && pt2>35. && pt2<=45.) return 0.919419;
      if(pt1>45. && pt1<=100. && pt2>45. && pt2<=100.) return 0.921429;
      if(pt1>100. && pt2>10. && pt2<=15.) return 0.903955;
      if(pt1>100. && pt2>15. && pt2<=20.) return 0.925197;
      if(pt1>100. && pt2>20. && pt2<=25.) return 0.937984;
      if(pt1>100. && pt2>25. && pt2<=35.) return 0.927711;
      if(pt1>100. && pt2>35. && pt2<=45.) return 0.913858;
      if(pt1>100. && pt2>45. && pt2<=100.) return 0.93019;
      if(pt1>100. && pt2>100.) return 0.939806;
    }
    else return 0;
  }
  if(HT>350 && HT<=400){
    if(abs(l1_pdgId)+abs(l2_pdgId) ==22){
      if(pt1>15. && pt1<=20. && pt2>15. && pt2<=20.) return 1;
      if(pt1>20. && pt1<=25. && pt2>15. && pt2<=20.) return 0.945946;
      if(pt1>20. && pt1<=25. && pt2>20. && pt2<=25.) return 1;
      if(pt1>25. && pt1<=35. && pt2>15. && pt2<=20.) return 0.830769;
      if(pt1>25. && pt1<=35. && pt2>20. && pt2<=25.) return 0.943182;
      if(pt1>25. && pt1<=35. && pt2>25. && pt2<=35.) return 0.961538;
      if(pt1>35. && pt1<=45. && pt2>15. && pt2<=20.) return 0.855072;
      if(pt1>35. && pt1<=45. && pt2>20. && pt2<=25.) return 0.910448;
      if(pt1>35. && pt1<=45. && pt2>25. && pt2<=35.) return 0.953488;
      if(pt1>35. && pt1<=45. && pt2>35. && pt2<=45.) return 0.961039;
      if(pt1>45. && pt1<=100. && pt2>15. && pt2<=20.) return 0.856481;
      if(pt1>45. && pt1<=100. && pt2>20. && pt2<=25.) return 0.950758;
      if(pt1>45. && pt1<=100. && pt2>25. && pt2<=35.) return 0.965577;
      if(pt1>45. && pt1<=100. && pt2>35. && pt2<=45.) return 0.971483;
      if(pt1>45. && pt1<=100. && pt2>45. && pt2<=100.) return 0.975381;
      if(pt1>100. && pt2>15. && pt2<=20.) return 0.945205;
      if(pt1>100. && pt2>20. && pt2<=25.) return 0.92233;
      if(pt1>100. && pt2>25. && pt2<=35.) return 0.959276;
      if(pt1>100. && pt2>35. && pt2<=45.) return 0.979675;
      if(pt1>100. && pt2>45. && pt2<=100.) return 0.979167;
      if(pt1>100. && pt2>100.) return 0.983806;
    }
    else if(abs(l1_pdgId)+abs(l2_pdgId) ==24){
      if(pt1>15. && pt1<=20. && pt2>10. && pt2<=15.) return 0.96875;
      if(pt1>15. && pt1<=20. && pt2>15. && pt2<=20.) return 0.95;
      if(pt1>15. && pt1<=20. && pt2>20. && pt2<=25.) return 0.846154;
      if(pt1>15. && pt1<=20. && pt2>25. && pt2<=35.) return 0.829787;
      if(pt1>15. && pt1<=20. && pt2>35. && pt2<=45.) return 0.901099;
      if(pt1>15. && pt1<=20. && pt2>45. && pt2<=100.) return 0.902778;
      if(pt1>15. && pt1<=20. && pt2>100.) return 0.85;
      if(pt1>20. && pt1<=25. && pt2>10. && pt2<=15.) return 1;
      if(pt1>20. && pt1<=25. && pt2>15. && pt2<=20.) return 0.916667;
      if(pt1>20. && pt1<=25. && pt2>20. && pt2<=25.) return 0.966102;
      if(pt1>20. && pt1<=25. && pt2>25. && pt2<=35.) return 0.858156;
      if(pt1>20. && pt1<=25. && pt2>35. && pt2<=45.) return 0.921875;
      if(pt1>20. && pt1<=25. && pt2>45. && pt2<=100.) return 0.934579;
      if(pt1>20. && pt1<=25. && pt2>100.) return 0.93985;
      if(pt1>25. && pt1<=35. && pt2>10. && pt2<=15.) return 0.915663;
      if(pt1>25. && pt1<=35. && pt2>15. && pt2<=20.) return 0.95935;
      if(pt1>25. && pt1<=35. && pt2>20. && pt2<=25.) return 0.924242;
      if(pt1>25. && pt1<=35. && pt2>25. && pt2<=35.) return 0.942373;
      if(pt1>25. && pt1<=35. && pt2>35. && pt2<=45.) return 0.955466;
      if(pt1>25. && pt1<=35. && pt2>45. && pt2<=100.) return 0.933896;
      if(pt1>25. && pt1<=35. && pt2>100.) return 0.92053;
      if(pt1>35. && pt1<=45. && pt2>10. && pt2<=15.) return 0.894118;
      if(pt1>35. && pt1<=45. && pt2>15. && pt2<=20.) return 0.959677;
      if(pt1>35. && pt1<=45. && pt2>20. && pt2<=25.) return 0.957143;
      if(pt1>35. && pt1<=45. && pt2>25. && pt2<=35.) return 0.94386;
      if(pt1>35. && pt1<=45. && pt2>35. && pt2<=45.) return 0.946154;
      if(pt1>35. && pt1<=45. && pt2>45. && pt2<=100.) return 0.962079;
      if(pt1>35. && pt1<=45. && pt2>100.) return 0.964912;
      if(pt1>45. && pt1<=100. && pt2>10. && pt2<=15.) return 0.955479;
      if(pt1>45. && pt1<=100. && pt2>15. && pt2<=20.) return 0.959302;
      if(pt1>45. && pt1<=100. && pt2>20. && pt2<=25.) return 0.960494;
      if(pt1>45. && pt1<=100. && pt2>25. && pt2<=35.) return 0.96792;
      if(pt1>45. && pt1<=100. && pt2>35. && pt2<=45.) return 0.962169;
      if(pt1>45. && pt1<=100. && pt2>45. && pt2<=100.) return 0.959751;
      if(pt1>45. && pt1<=100. && pt2>100.) return 0.944964;
      if(pt1>100. && pt2>10. && pt2<=15.) return 0.971429;
      if(pt1>100. && pt2>15. && pt2<=20.) return 0.95092;
      if(pt1>100. && pt2>20. && pt2<=25.) return 0.961783;
      if(pt1>100. && pt2>25. && pt2<=35.) return 0.961957;
      if(pt1>100. && pt2>35. && pt2<=45.) return 0.9701;
      if(pt1>100. && pt2>45. && pt2<=100.) return 0.971144;
      if(pt1>100. && pt2>100.) return 0.963893;
    }
    else if(abs(l1_pdgId)+abs(l2_pdgId) ==26){
      if(pt1>10. && pt1<=15. && pt2>10. && pt2<=15.) return 0.944444;
      if(pt1>15. && pt1<=20. && pt2>10. && pt2<=15.) return 0.928571;
      if(pt1>15. && pt1<=20. && pt2>15. && pt2<=20.) return 0.794118;
      if(pt1>20. && pt1<=25. && pt2>10. && pt2<=15.) return 0.935484;
      if(pt1>20. && pt1<=25. && pt2>15. && pt2<=20.) return 0.915663;
      if(pt1>20. && pt1<=25. && pt2>20. && pt2<=25.) return 0.911765;
      if(pt1>25. && pt1<=35. && pt2>10. && pt2<=15.) return 0.91453;
      if(pt1>25. && pt1<=35. && pt2>15. && pt2<=20.) return 0.908537;
      if(pt1>25. && pt1<=35. && pt2>20. && pt2<=25.) return 0.909091;
      if(pt1>25. && pt1<=35. && pt2>25. && pt2<=35.) return 0.925134;
      if(pt1>35. && pt1<=45. && pt2>10. && pt2<=15.) return 0.946565;
      if(pt1>35. && pt1<=45. && pt2>15. && pt2<=20.) return 0.921212;
      if(pt1>35. && pt1<=45. && pt2>20. && pt2<=25.) return 0.940887;
      if(pt1>35. && pt1<=45. && pt2>25. && pt2<=35.) return 0.941691;
      if(pt1>35. && pt1<=45. && pt2>35. && pt2<=45.) return 0.936047;
      if(pt1>45. && pt1<=100. && pt2>10. && pt2<=15.) return 0.95679;
      if(pt1>45. && pt1<=100. && pt2>15. && pt2<=20.) return 0.940803;
      if(pt1>45. && pt1<=100. && pt2>20. && pt2<=25.) return 0.926554;
      if(pt1>45. && pt1<=100. && pt2>25. && pt2<=35.) return 0.940257;
      if(pt1>45. && pt1<=100. && pt2>35. && pt2<=45.) return 0.944498;
      if(pt1>45. && pt1<=100. && pt2>45. && pt2<=100.) return 0.948026;
      if(pt1>100. && pt2>10. && pt2<=15.) return 0.954248;
      if(pt1>100. && pt2>15. && pt2<=20.) return 0.978378;
      if(pt1>100. && pt2>20. && pt2<=25.) return 0.932642;
      if(pt1>100. && pt2>25. && pt2<=35.) return 0.948546;
      if(pt1>100. && pt2>35. && pt2<=45.) return 0.951157;
      if(pt1>100. && pt2>45. && pt2<=100.) return 0.937548;
      if(pt1>100. && pt2>100.) return 0.936061;
    }
    else return 0;
  }
  if(HT>400 && HT<=800){
    if(abs(l1_pdgId)+abs(l2_pdgId) ==22){
      if(pt1>15. && pt1<=20. && pt2>15. && pt2<=20.) return 0.888889;
      if(pt1>20. && pt1<=25. && pt2>15. && pt2<=20.) return 0.886792;
      if(pt1>20. && pt1<=25. && pt2>20. && pt2<=25.) return 0.943662;
      if(pt1>25. && pt1<=35. && pt2>15. && pt2<=20.) return 0.864198;
      if(pt1>25. && pt1<=35. && pt2>20. && pt2<=25.) return 0.915541;
      if(pt1>25. && pt1<=35. && pt2>25. && pt2<=35.) return 0.941748;
      if(pt1>35. && pt1<=45. && pt2>15. && pt2<=20.) return 0.891667;
      if(pt1>35. && pt1<=45. && pt2>20. && pt2<=25.) return 0.968198;
      if(pt1>35. && pt1<=45. && pt2>25. && pt2<=35.) return 0.953285;
      if(pt1>35. && pt1<=45. && pt2>35. && pt2<=45.) return 0.966049;
      if(pt1>45. && pt1<=100. && pt2>15. && pt2<=20.) return 0.911622;
      if(pt1>45. && pt1<=100. && pt2>20. && pt2<=25.) return 0.929006;
      if(pt1>45. && pt1<=100. && pt2>25. && pt2<=35.) return 0.959006;
      if(pt1>45. && pt1<=100. && pt2>35. && pt2<=45.) return 0.967981;
      if(pt1>45. && pt1<=100. && pt2>45. && pt2<=100.) return 0.975743;
      if(pt1>100. && pt2>15. && pt2<=20.) return 0.894928;
      if(pt1>100. && pt2>20. && pt2<=25.) return 0.945865;
      if(pt1>100. && pt2>25. && pt2<=35.) return 0.961408;
      if(pt1>100. && pt2>35. && pt2<=45.) return 0.974609;
      if(pt1>100. && pt2>45. && pt2<=100.) return 0.983743;
      if(pt1>100. && pt2>100.) return 0.986499;
    }
    else if(abs(l1_pdgId)+abs(l2_pdgId) ==24){
      if(pt1>15. && pt1<=20. && pt2>10. && pt2<=15.) return 0.918919;
      if(pt1>15. && pt1<=20. && pt2>15. && pt2<=20.) return 0.902098;
      if(pt1>15. && pt1<=20. && pt2>20. && pt2<=25.) return 0.884848;
      if(pt1>15. && pt1<=20. && pt2>25. && pt2<=35.) return 0.860947;
      if(pt1>15. && pt1<=20. && pt2>35. && pt2<=45.) return 0.894558;
      if(pt1>15. && pt1<=20. && pt2>45. && pt2<=100.) return 0.892045;
      if(pt1>15. && pt1<=20. && pt2>100.) return 0.873303;
      if(pt1>20. && pt1<=25. && pt2>10. && pt2<=15.) return 0.92;
      if(pt1>20. && pt1<=25. && pt2>15. && pt2<=20.) return 0.916201;
      if(pt1>20. && pt1<=25. && pt2>20. && pt2<=25.) return 0.912621;
      if(pt1>20. && pt1<=25. && pt2>25. && pt2<=35.) return 0.921801;
      if(pt1>20. && pt1<=25. && pt2>35. && pt2<=45.) return 0.917738;
      if(pt1>20. && pt1<=25. && pt2>45. && pt2<=100.) return 0.935759;
      if(pt1>20. && pt1<=25. && pt2>100.) return 0.928398;
      if(pt1>25. && pt1<=35. && pt2>10. && pt2<=15.) return 0.93949;
      if(pt1>25. && pt1<=35. && pt2>15. && pt2<=20.) return 0.949029;
      if(pt1>25. && pt1<=35. && pt2>20. && pt2<=25.) return 0.958057;
      if(pt1>25. && pt1<=35. && pt2>25. && pt2<=35.) return 0.947429;
      if(pt1>25. && pt1<=35. && pt2>35. && pt2<=45.) return 0.942286;
      if(pt1>25. && pt1<=35. && pt2>45. && pt2<=100.) return 0.948181;
      if(pt1>25. && pt1<=35. && pt2>100.) return 0.947034;
      if(pt1>35. && pt1<=45. && pt2>10. && pt2<=15.) return 0.962121;
      if(pt1>35. && pt1<=45. && pt2>15. && pt2<=20.) return 0.944297;
      if(pt1>35. && pt1<=45. && pt2>20. && pt2<=25.) return 0.953684;
      if(pt1>35. && pt1<=45. && pt2>25. && pt2<=35.) return 0.970954;
      if(pt1>35. && pt1<=45. && pt2>35. && pt2<=45.) return 0.95526;
      if(pt1>35. && pt1<=45. && pt2>45. && pt2<=100.) return 0.958278;
      if(pt1>35. && pt1<=45. && pt2>100.) return 0.956614;
      if(pt1>45. && pt1<=100. && pt2>10. && pt2<=15.) return 0.960707;
      if(pt1>45. && pt1<=100. && pt2>15. && pt2<=20.) return 0.965243;
      if(pt1>45. && pt1<=100. && pt2>20. && pt2<=25.) return 0.959032;
      if(pt1>45. && pt1<=100. && pt2>25. && pt2<=35.) return 0.956389;
      if(pt1>45. && pt1<=100. && pt2>35. && pt2<=45.) return 0.96952;
      if(pt1>45. && pt1<=100. && pt2>45. && pt2<=100.) return 0.961897;
      if(pt1>45. && pt1<=100. && pt2>100.) return 0.955745;
      if(pt1>100. && pt2>10. && pt2<=15.) return 0.956522;
      if(pt1>100. && pt2>15. && pt2<=20.) return 0.966025;
      if(pt1>100. && pt2>20. && pt2<=25.) return 0.969052;
      if(pt1>100. && pt2>25. && pt2<=35.) return 0.966071;
      if(pt1>100. && pt2>35. && pt2<=45.) return 0.965698;
      if(pt1>100. && pt2>45. && pt2<=100.) return 0.966688;
      if(pt1>100. && pt2>100.) return 0.964623;
    }
    else if(abs(l1_pdgId)+abs(l2_pdgId) ==26){
      if(pt1>10. && pt1<=15. && pt2>10. && pt2<=15.) return 0.971429;
      if(pt1>15. && pt1<=20. && pt2>10. && pt2<=15.) return 0.949495;
      if(pt1>15. && pt1<=20. && pt2>15. && pt2<=20.) return 0.908257;
      if(pt1>20. && pt1<=25. && pt2>10. && pt2<=15.) return 0.94086;
      if(pt1>20. && pt1<=25. && pt2>15. && pt2<=20.) return 0.897638;
      if(pt1>20. && pt1<=25. && pt2>20. && pt2<=25.) return 0.9375;
      if(pt1>25. && pt1<=35. && pt2>10. && pt2<=15.) return 0.947846;
      if(pt1>25. && pt1<=35. && pt2>15. && pt2<=20.) return 0.94188;
      if(pt1>25. && pt1<=35. && pt2>20. && pt2<=25.) return 0.936202;
      if(pt1>25. && pt1<=35. && pt2>25. && pt2<=35.) return 0.938897;
      if(pt1>35. && pt1<=45. && pt2>10. && pt2<=15.) return 0.920635;
      if(pt1>35. && pt1<=45. && pt2>15. && pt2<=20.) return 0.922481;
      if(pt1>35. && pt1<=45. && pt2>20. && pt2<=25.) return 0.944805;
      if(pt1>35. && pt1<=45. && pt2>25. && pt2<=35.) return 0.944674;
      if(pt1>35. && pt1<=45. && pt2>35. && pt2<=45.) return 0.946087;
      if(pt1>45. && pt1<=100. && pt2>10. && pt2<=15.) return 0.95036;
      if(pt1>45. && pt1<=100. && pt2>15. && pt2<=20.) return 0.941913;
      if(pt1>45. && pt1<=100. && pt2>20. && pt2<=25.) return 0.940397;
      if(pt1>45. && pt1<=100. && pt2>25. && pt2<=35.) return 0.949603;
      if(pt1>45. && pt1<=100. && pt2>35. && pt2<=45.) return 0.947381;
      if(pt1>45. && pt1<=100. && pt2>45. && pt2<=100.) return 0.945082;
      if(pt1>100. && pt2>10. && pt2<=15.) return 0.942308;
      if(pt1>100. && pt2>15. && pt2<=20.) return 0.94385;
      if(pt1>100. && pt2>20. && pt2<=25.) return 0.943507;
      if(pt1>100. && pt2>25. && pt2<=35.) return 0.940537;
      if(pt1>100. && pt2>35. && pt2<=45.) return 0.946047;
      if(pt1>100. && pt2>45. && pt2<=100.) return 0.942713;
      if(pt1>100. && pt2>100.) return 0.937208;
    }
    else return 0;
  }
  if(HT>800 && HT<=1600){
    if(abs(l1_pdgId)+abs(l2_pdgId) ==22){
      if(pt1>15. && pt1<=20. && pt2>15. && pt2<=20.) return 0.777778;
      if(pt1>20. && pt1<=25. && pt2>15. && pt2<=20.) return 0.846774;
      if(pt1>20. && pt1<=25. && pt2>20. && pt2<=25.) return 0.882353;
      if(pt1>25. && pt1<=35. && pt2>15. && pt2<=20.) return 0.869732;
      if(pt1>25. && pt1<=35. && pt2>20. && pt2<=25.) return 0.924471;
      if(pt1>25. && pt1<=35. && pt2>25. && pt2<=35.) return 0.942675;
      if(pt1>35. && pt1<=45. && pt2>15. && pt2<=20.) return 0.904382;
      if(pt1>35. && pt1<=45. && pt2>20. && pt2<=25.) return 0.917763;
      if(pt1>35. && pt1<=45. && pt2>25. && pt2<=35.) return 0.937591;
      if(pt1>35. && pt1<=45. && pt2>35. && pt2<=45.) return 0.962644;
      if(pt1>45. && pt1<=100. && pt2>15. && pt2<=20.) return 0.857143;
      if(pt1>45. && pt1<=100. && pt2>20. && pt2<=25.) return 0.899065;
      if(pt1>45. && pt1<=100. && pt2>25. && pt2<=35.) return 0.947368;
      if(pt1>45. && pt1<=100. && pt2>35. && pt2<=45.) return 0.943478;
      if(pt1>45. && pt1<=100. && pt2>45. && pt2<=100.) return 0.963075;
      if(pt1>100. && pt2>15. && pt2<=20.) return 0.863839;
      if(pt1>100. && pt2>20. && pt2<=25.) return 0.898723;
      if(pt1>100. && pt2>25. && pt2<=35.) return 0.941104;
      if(pt1>100. && pt2>35. && pt2<=45.) return 0.953275;
      if(pt1>100. && pt2>45. && pt2<=100.) return 0.968577;
      if(pt1>100. && pt2>100.) return 0.977384;
    }
    else if(abs(l1_pdgId)+abs(l2_pdgId) ==24){
      if(pt1>15. && pt1<=20. && pt2>10. && pt2<=15.) return 0.861314;
      if(pt1>15. && pt1<=20. && pt2>15. && pt2<=20.) return 0.896341;
      if(pt1>15. && pt1<=20. && pt2>20. && pt2<=25.) return 0.873494;
      if(pt1>15. && pt1<=20. && pt2>25. && pt2<=35.) return 0.87106;
      if(pt1>15. && pt1<=20. && pt2>35. && pt2<=45.) return 0.863372;
      if(pt1>15. && pt1<=20. && pt2>45. && pt2<=100.) return 0.885152;
      if(pt1>15. && pt1<=20. && pt2>100.) return 0.881298;
      if(pt1>20. && pt1<=25. && pt2>10. && pt2<=15.) return 0.901786;
      if(pt1>20. && pt1<=25. && pt2>15. && pt2<=20.) return 0.92;
      if(pt1>20. && pt1<=25. && pt2>20. && pt2<=25.) return 0.939252;
      if(pt1>20. && pt1<=25. && pt2>25. && pt2<=35.) return 0.940397;
      if(pt1>20. && pt1<=25. && pt2>35. && pt2<=45.) return 0.917275;
      if(pt1>20. && pt1<=25. && pt2>45. && pt2<=100.) return 0.923379;
      if(pt1>20. && pt1<=25. && pt2>100.) return 0.918803;
      if(pt1>25. && pt1<=35. && pt2>10. && pt2<=15.) return 0.925816;
      if(pt1>25. && pt1<=35. && pt2>15. && pt2<=20.) return 0.949109;
      if(pt1>25. && pt1<=35. && pt2>20. && pt2<=25.) return 0.956;
      if(pt1>25. && pt1<=35. && pt2>25. && pt2<=35.) return 0.944328;
      if(pt1>25. && pt1<=35. && pt2>35. && pt2<=45.) return 0.941514;
      if(pt1>25. && pt1<=35. && pt2>45. && pt2<=100.) return 0.939907;
      if(pt1>25. && pt1<=35. && pt2>100.) return 0.940453;
      if(pt1>35. && pt1<=45. && pt2>10. && pt2<=15.) return 0.961538;
      if(pt1>35. && pt1<=45. && pt2>15. && pt2<=20.) return 0.934896;
      if(pt1>35. && pt1<=45. && pt2>20. && pt2<=25.) return 0.951945;
      if(pt1>35. && pt1<=45. && pt2>25. && pt2<=35.) return 0.945175;
      if(pt1>35. && pt1<=45. && pt2>35. && pt2<=45.) return 0.946953;
      if(pt1>35. && pt1<=45. && pt2>45. && pt2<=100.) return 0.956379;
      if(pt1>35. && pt1<=45. && pt2>100.) return 0.953683;
      if(pt1>45. && pt1<=100. && pt2>10. && pt2<=15.) return 0.9583;
      if(pt1>45. && pt1<=100. && pt2>15. && pt2<=20.) return 0.960645;
      if(pt1>45. && pt1<=100. && pt2>20. && pt2<=25.) return 0.961644;
      if(pt1>45. && pt1<=100. && pt2>25. && pt2<=35.) return 0.964843;
      if(pt1>45. && pt1<=100. && pt2>35. && pt2<=45.) return 0.959388;
      if(pt1>45. && pt1<=100. && pt2>45. && pt2<=100.) return 0.96071;
      if(pt1>45. && pt1<=100. && pt2>100.) return 0.955142;
      if(pt1>100. && pt2>10. && pt2<=15.) return 0.954833;
      if(pt1>100. && pt2>15. && pt2<=20.) return 0.957529;
      if(pt1>100. && pt2>20. && pt2<=25.) return 0.970267;
      if(pt1>100. && pt2>25. && pt2<=35.) return 0.970022;
      if(pt1>100. && pt2>35. && pt2<=45.) return 0.968966;
      if(pt1>100. && pt2>45. && pt2<=100.) return 0.966912;
      if(pt1>100. && pt2>100.) return 0.961464;
    }
    else if(abs(l1_pdgId)+abs(l2_pdgId) ==26){
      if(pt1>10. && pt1<=15. && pt2>10. && pt2<=15.) return 0.961039;
      if(pt1>15. && pt1<=20. && pt2>10. && pt2<=15.) return 0.954128;
      if(pt1>15. && pt1<=20. && pt2>15. && pt2<=20.) return 0.930233;
      if(pt1>20. && pt1<=25. && pt2>10. && pt2<=15.) return 0.931818;
      if(pt1>20. && pt1<=25. && pt2>15. && pt2<=20.) return 0.943333;
      if(pt1>20. && pt1<=25. && pt2>20. && pt2<=25.) return 0.971098;
      if(pt1>25. && pt1<=35. && pt2>10. && pt2<=15.) return 0.940206;
      if(pt1>25. && pt1<=35. && pt2>15. && pt2<=20.) return 0.939935;
      if(pt1>25. && pt1<=35. && pt2>20. && pt2<=25.) return 0.957516;
      if(pt1>25. && pt1<=35. && pt2>25. && pt2<=35.) return 0.952646;
      if(pt1>35. && pt1<=45. && pt2>10. && pt2<=15.) return 0.93819;
      if(pt1>35. && pt1<=45. && pt2>15. && pt2<=20.) return 0.954098;
      if(pt1>35. && pt1<=45. && pt2>20. && pt2<=25.) return 0.945545;
      if(pt1>35. && pt1<=45. && pt2>25. && pt2<=35.) return 0.95264;
      if(pt1>35. && pt1<=45. && pt2>35. && pt2<=45.) return 0.94462;
      if(pt1>45. && pt1<=100. && pt2>10. && pt2<=15.) return 0.937914;
      if(pt1>45. && pt1<=100. && pt2>15. && pt2<=20.) return 0.953266;
      if(pt1>45. && pt1<=100. && pt2>20. && pt2<=25.) return 0.948914;
      if(pt1>45. && pt1<=100. && pt2>25. && pt2<=35.) return 0.946694;
      if(pt1>45. && pt1<=100. && pt2>35. && pt2<=45.) return 0.948549;
      if(pt1>45. && pt1<=100. && pt2>45. && pt2<=100.) return 0.947672;
      if(pt1>100. && pt2>10. && pt2<=15.) return 0.939743;
      if(pt1>100. && pt2>15. && pt2<=20.) return 0.946653;
      if(pt1>100. && pt2>20. && pt2<=25.) return 0.948159;
      if(pt1>100. && pt2>25. && pt2<=35.) return 0.949451;
      if(pt1>100. && pt2>35. && pt2<=45.) return 0.941121;
      if(pt1>100. && pt2>45. && pt2<=100.) return 0.940587;
      if(pt1>100. && pt2>100.) return 0.934288;
    }
    else return 0;
  }
  if(HT>1600 && HT<=2500){
    if(abs(l1_pdgId)+abs(l2_pdgId) ==22){
      if(pt1>20. && pt1<=25. && pt2>15. && pt2<=20.) return 0.25;
      if(pt1>20. && pt1<=25. && pt2>20. && pt2<=25.) return 0.833333;
      if(pt1>25. && pt1<=35. && pt2>15. && pt2<=20.) return 0.714286;
      if(pt1>25. && pt1<=35. && pt2>20. && pt2<=25.) return 0.8125;
      if(pt1>25. && pt1<=35. && pt2>25. && pt2<=35.) return 0.884615;
      if(pt1>35. && pt1<=45. && pt2>15. && pt2<=20.) return 0.740741;
      if(pt1>35. && pt1<=45. && pt2>20. && pt2<=25.) return 0.842105;
      if(pt1>35. && pt1<=45. && pt2>25. && pt2<=35.) return 0.862069;
      if(pt1>35. && pt1<=45. && pt2>35. && pt2<=45.) return 1;
      if(pt1>45. && pt1<=100. && pt2>15. && pt2<=20.) return 0.6375;
      if(pt1>45. && pt1<=100. && pt2>20. && pt2<=25.) return 0.75;
      if(pt1>45. && pt1<=100. && pt2>25. && pt2<=35.) return 0.812183;
      if(pt1>45. && pt1<=100. && pt2>35. && pt2<=45.) return 0.82439;
      if(pt1>45. && pt1<=100. && pt2>45. && pt2<=100.) return 0.835784;
      if(pt1>100. && pt2>15. && pt2<=20.) return 0.69697;
      if(pt1>100. && pt2>20. && pt2<=25.) return 0.764706;
      if(pt1>100. && pt2>25. && pt2<=35.) return 0.8;
      if(pt1>100. && pt2>35. && pt2<=45.) return 0.815;
      if(pt1>100. && pt2>45. && pt2<=100.) return 0.876033;
      if(pt1>100. && pt2>100.) return 0.921606;
    }
    else if(abs(l1_pdgId)+abs(l2_pdgId) ==24){
      if(pt1>15. && pt1<=20. && pt2>10. && pt2<=15.) return 0.916667;
      if(pt1>15. && pt1<=20. && pt2>15. && pt2<=20.) return 0.818182;
      if(pt1>15. && pt1<=20. && pt2>20. && pt2<=25.) return 0.8;
      if(pt1>15. && pt1<=20. && pt2>25. && pt2<=35.) return 0.894737;
      if(pt1>15. && pt1<=20. && pt2>35. && pt2<=45.) return 0.9;
      if(pt1>15. && pt1<=20. && pt2>45. && pt2<=100.) return 0.806818;
      if(pt1>15. && pt1<=20. && pt2>100.) return 0.79798;
      if(pt1>20. && pt1<=25. && pt2>10. && pt2<=15.) return 0.733333;
      if(pt1>20. && pt1<=25. && pt2>15. && pt2<=20.) return 0.761905;
      if(pt1>20. && pt1<=25. && pt2>20. && pt2<=25.) return 0.9375;
      if(pt1>20. && pt1<=25. && pt2>25. && pt2<=35.) return 0.74359;
      if(pt1>20. && pt1<=25. && pt2>35. && pt2<=45.) return 0.892857;
      if(pt1>20. && pt1<=25. && pt2>45. && pt2<=100.) return 0.842105;
      if(pt1>20. && pt1<=25. && pt2>100.) return 0.871795;
      if(pt1>25. && pt1<=35. && pt2>10. && pt2<=15.) return 0.903226;
      if(pt1>25. && pt1<=35. && pt2>15. && pt2<=20.) return 0.805556;
      if(pt1>25. && pt1<=35. && pt2>20. && pt2<=25.) return 0.931035;
      if(pt1>25. && pt1<=35. && pt2>25. && pt2<=35.) return 0.922222;
      if(pt1>25. && pt1<=35. && pt2>35. && pt2<=45.) return 0.951613;
      if(pt1>25. && pt1<=35. && pt2>45. && pt2<=100.) return 0.892193;
      if(pt1>25. && pt1<=35. && pt2>100.) return 0.913208;
      if(pt1>35. && pt1<=45. && pt2>10. && pt2<=15.) return 0.961538;
      if(pt1>35. && pt1<=45. && pt2>15. && pt2<=20.) return 0.965517;
      if(pt1>35. && pt1<=45. && pt2>20. && pt2<=25.) return 0.938776;
      if(pt1>35. && pt1<=45. && pt2>25. && pt2<=35.) return 0.924242;
      if(pt1>35. && pt1<=45. && pt2>35. && pt2<=45.) return 0.967213;
      if(pt1>35. && pt1<=45. && pt2>45. && pt2<=100.) return 0.937255;
      if(pt1>35. && pt1<=45. && pt2>100.) return 0.933086;
      if(pt1>45. && pt1<=100. && pt2>10. && pt2<=15.) return 0.915789;
      if(pt1>45. && pt1<=100. && pt2>15. && pt2<=20.) return 0.985816;
      if(pt1>45. && pt1<=100. && pt2>20. && pt2<=25.) return 0.96748;
      if(pt1>45. && pt1<=100. && pt2>25. && pt2<=35.) return 0.937086;
      if(pt1>45. && pt1<=100. && pt2>35. && pt2<=45.) return 0.956364;
      if(pt1>45. && pt1<=100. && pt2>45. && pt2<=100.) return 0.946429;
      if(pt1>45. && pt1<=100. && pt2>100.) return 0.939227;
      if(pt1>100. && pt2>10. && pt2<=15.) return 0.961165;
      if(pt1>100. && pt2>15. && pt2<=20.) return 0.974576;
      if(pt1>100. && pt2>20. && pt2<=25.) return 0.954887;
      if(pt1>100. && pt2>25. && pt2<=35.) return 0.958477;
      if(pt1>100. && pt2>35. && pt2<=45.) return 0.95189;
      if(pt1>100. && pt2>45. && pt2<=100.) return 0.959932;
      if(pt1>100. && pt2>100.) return 0.964207;
    }
    else if(abs(l1_pdgId)+abs(l2_pdgId) ==26){
      if(pt1>10. && pt1<=15. && pt2>10. && pt2<=15.) return 0.857143;
      if(pt1>15. && pt1<=20. && pt2>10. && pt2<=15.) return 0.95;
      if(pt1>15. && pt1<=20. && pt2>15. && pt2<=20.) return 0.857143;
      if(pt1>20. && pt1<=25. && pt2>10. && pt2<=15.) return 1;
      if(pt1>20. && pt1<=25. && pt2>15. && pt2<=20.) return 0.818182;
      if(pt1>20. && pt1<=25. && pt2>20. && pt2<=25.) return 0.916667;
      if(pt1>25. && pt1<=35. && pt2>10. && pt2<=15.) return 0.941176;
      if(pt1>25. && pt1<=35. && pt2>15. && pt2<=20.) return 0.957447;
      if(pt1>25. && pt1<=35. && pt2>20. && pt2<=25.) return 0.947368;
      if(pt1>25. && pt1<=35. && pt2>25. && pt2<=35.) return 0.980769;
      if(pt1>35. && pt1<=45. && pt2>10. && pt2<=15.) return 1;
      if(pt1>35. && pt1<=45. && pt2>15. && pt2<=20.) return 0.93617;
      if(pt1>35. && pt1<=45. && pt2>20. && pt2<=25.) return 0.959184;
      if(pt1>35. && pt1<=45. && pt2>25. && pt2<=35.) return 0.97;
      if(pt1>35. && pt1<=45. && pt2>35. && pt2<=45.) return 0.963636;
      if(pt1>45. && pt1<=100. && pt2>10. && pt2<=15.) return 0.943925;
      if(pt1>45. && pt1<=100. && pt2>15. && pt2<=20.) return 0.958333;
      if(pt1>45. && pt1<=100. && pt2>20. && pt2<=25.) return 0.934426;
      if(pt1>45. && pt1<=100. && pt2>25. && pt2<=35.) return 0.960212;
      if(pt1>45. && pt1<=100. && pt2>35. && pt2<=45.) return 0.968661;
      if(pt1>45. && pt1<=100. && pt2>45. && pt2<=100.) return 0.957143;
      if(pt1>100. && pt2>10. && pt2<=15.) return 0.953846;
      if(pt1>100. && pt2>15. && pt2<=20.) return 0.953488;
      if(pt1>100. && pt2>20. && pt2<=25.) return 0.955056;
      if(pt1>100. && pt2>25. && pt2<=35.) return 0.949853;
      if(pt1>100. && pt2>35. && pt2<=45.) return 0.948586;
      if(pt1>100. && pt2>45. && pt2<=100.) return 0.945442;
      if(pt1>100. && pt2>100.) return 0.938983;
    }
    else return 0;
  }
  if(HT>2500){
    if(abs(l1_pdgId)+abs(l2_pdgId) ==22){
      if(pt1>15. && pt1<=20. && pt2>15. && pt2<=20.) return 0.5;
      if(pt1>20. && pt1<=25. && pt2>20. && pt2<=25.) return 0.75;
      if(pt1>25. && pt1<=35. && pt2>15. && pt2<=20.) return 0.555556;
      if(pt1>25. && pt1<=35. && pt2>20. && pt2<=25.) return 0.411765;
      if(pt1>25. && pt1<=35. && pt2>25. && pt2<=35.) return 0.75;
      if(pt1>35. && pt1<=45. && pt2>15. && pt2<=20.) return 0.5;
      if(pt1>35. && pt1<=45. && pt2>20. && pt2<=25.) return 0.875;
      if(pt1>35. && pt1<=45. && pt2>25. && pt2<=35.) return 0.73913;
      if(pt1>35. && pt1<=45. && pt2>35. && pt2<=45.) return 0.833333;
      if(pt1>45. && pt1<=100. && pt2>15. && pt2<=20.) return 0.454545;
      if(pt1>45. && pt1<=100. && pt2>20. && pt2<=25.) return 0.5;
      if(pt1>45. && pt1<=100. && pt2>25. && pt2<=35.) return 0.66129;
      if(pt1>45. && pt1<=100. && pt2>35. && pt2<=45.) return 0.698413;
      if(pt1>45. && pt1<=100. && pt2>45. && pt2<=100.) return 0.736625;
      if(pt1>100. && pt2>15. && pt2<=20.) return 0.352941;
      if(pt1>100. && pt2>20. && pt2<=25.) return 0.537313;
      if(pt1>100. && pt2>25. && pt2<=35.) return 0.566929;
      if(pt1>100. && pt2>35. && pt2<=45.) return 0.721311;
      if(pt1>100. && pt2>45. && pt2<=100.) return 0.77027;
      if(pt1>100. && pt2>100.) return 0.808362;
    }
    else if(abs(l1_pdgId)+abs(l2_pdgId) ==24){
      if(pt1>15. && pt1<=20. && pt2>10. && pt2<=15.) return 0.8;
      if(pt1>15. && pt1<=20. && pt2>15. && pt2<=20.) return 0.8;
      if(pt1>15. && pt1<=20. && pt2>20. && pt2<=25.) return 0.5;
      if(pt1>15. && pt1<=20. && pt2>25. && pt2<=35.) return 0.727273;
      if(pt1>15. && pt1<=20. && pt2>35. && pt2<=45.) return 0.666667;
      if(pt1>15. && pt1<=20. && pt2>45. && pt2<=100.) return 0.781818;
      if(pt1>15. && pt1<=20. && pt2>100.) return 0.676056;
      if(pt1>20. && pt1<=25. && pt2>10. && pt2<=15.) return 0.833333;
      if(pt1>20. && pt1<=25. && pt2>15. && pt2<=20.) return 0.888889;
      if(pt1>20. && pt1<=25. && pt2>20. && pt2<=25.) return 1;
      if(pt1>20. && pt1<=25. && pt2>25. && pt2<=35.) return 0.777778;
      if(pt1>20. && pt1<=25. && pt2>35. && pt2<=45.) return 0.894737;
      if(pt1>20. && pt1<=25. && pt2>45. && pt2<=100.) return 0.8;
      if(pt1>20. && pt1<=25. && pt2>100.) return 0.746835;
      if(pt1>25. && pt1<=35. && pt2>10. && pt2<=15.) return 0.933333;
      if(pt1>25. && pt1<=35. && pt2>15. && pt2<=20.) return 0.777778;
      if(pt1>25. && pt1<=35. && pt2>20. && pt2<=25.) return 0.894737;
      if(pt1>25. && pt1<=35. && pt2>25. && pt2<=35.) return 0.875;
      if(pt1>25. && pt1<=35. && pt2>35. && pt2<=45.) return 0.866667;
      if(pt1>25. && pt1<=35. && pt2>45. && pt2<=100.) return 0.842424;
      if(pt1>25. && pt1<=35. && pt2>100.) return 0.803922;
      if(pt1>35. && pt1<=45. && pt2>10. && pt2<=15.) return 0.888889;
      if(pt1>35. && pt1<=45. && pt2>15. && pt2<=20.) return 1;
      if(pt1>35. && pt1<=45. && pt2>20. && pt2<=25.) return 0.833333;
      if(pt1>35. && pt1<=45. && pt2>25. && pt2<=35.) return 0.822222;
      if(pt1>35. && pt1<=45. && pt2>35. && pt2<=45.) return 0.925;
      if(pt1>35. && pt1<=45. && pt2>45. && pt2<=100.) return 0.865497;
      if(pt1>35. && pt1<=45. && pt2>100.) return 0.861446;
      if(pt1>45. && pt1<=100. && pt2>10. && pt2<=15.) return 0.877551;
      if(pt1>45. && pt1<=100. && pt2>15. && pt2<=20.) return 0.854839;
      if(pt1>45. && pt1<=100. && pt2>20. && pt2<=25.) return 0.939759;
      if(pt1>45. && pt1<=100. && pt2>25. && pt2<=35.) return 0.935294;
      if(pt1>45. && pt1<=100. && pt2>35. && pt2<=45.) return 0.913979;
      if(pt1>45. && pt1<=100. && pt2>45. && pt2<=100.) return 0.927419;
      if(pt1>45. && pt1<=100. && pt2>100.) return 0.903614;
      if(pt1>100. && pt2>10. && pt2<=15.) return 0.984375;
      if(pt1>100. && pt2>15. && pt2<=20.) return 0.934211;
      if(pt1>100. && pt2>20. && pt2<=25.) return 0.986842;
      if(pt1>100. && pt2>25. && pt2<=35.) return 0.976331;
      if(pt1>100. && pt2>35. && pt2<=45.) return 0.927273;
      if(pt1>100. && pt2>45. && pt2<=100.) return 0.94825;
      if(pt1>100. && pt2>100.) return 0.944633;
    }
    else if(abs(l1_pdgId)+abs(l2_pdgId) ==26){
      if(pt1>10. && pt1<=15. && pt2>10. && pt2<=15.) return 1;
      if(pt1>15. && pt1<=20. && pt2>10. && pt2<=15.) return 0.9;
      if(pt1>15. && pt1<=20. && pt2>15. && pt2<=20.) return 1;
      if(pt1>20. && pt1<=25. && pt2>10. && pt2<=15.) return 0.888889;
      if(pt1>20. && pt1<=25. && pt2>15. && pt2<=20.) return 1;
      if(pt1>20. && pt1<=25. && pt2>20. && pt2<=25.) return 1;
      if(pt1>25. && pt1<=35. && pt2>10. && pt2<=15.) return 0.888889;
      if(pt1>25. && pt1<=35. && pt2>15. && pt2<=20.) return 0.9;
      if(pt1>25. && pt1<=35. && pt2>20. && pt2<=25.) return 0.96;
      if(pt1>25. && pt1<=35. && pt2>25. && pt2<=35.) return 0.970588;
      if(pt1>35. && pt1<=45. && pt2>10. && pt2<=15.) return 1;
      if(pt1>35. && pt1<=45. && pt2>15. && pt2<=20.) return 0.958333;
      if(pt1>35. && pt1<=45. && pt2>20. && pt2<=25.) return 1;
      if(pt1>35. && pt1<=45. && pt2>25. && pt2<=35.) return 0.9375;
      if(pt1>35. && pt1<=45. && pt2>35. && pt2<=45.) return 1;
      if(pt1>45. && pt1<=100. && pt2>10. && pt2<=15.) return 0.94186;
      if(pt1>45. && pt1<=100. && pt2>15. && pt2<=20.) return 0.968085;
      if(pt1>45. && pt1<=100. && pt2>20. && pt2<=25.) return 0.941176;
      if(pt1>45. && pt1<=100. && pt2>25. && pt2<=35.) return 0.930736;
      if(pt1>45. && pt1<=100. && pt2>35. && pt2<=45.) return 0.957547;
      if(pt1>45. && pt1<=100. && pt2>45. && pt2<=100.) return 0.936118;
      if(pt1>100. && pt2>10. && pt2<=15.) return 0.979381;
      if(pt1>100. && pt2>15. && pt2<=20.) return 0.93578;
      if(pt1>100. && pt2>20. && pt2<=25.) return 0.942623;
      if(pt1>100. && pt2>25. && pt2<=35.) return 0.927126;
      if(pt1>100. && pt2>35. && pt2<=45.) return 0.926087;
      if(pt1>100. && pt2>45. && pt2<=100.) return 0.952656;
      if(pt1>100. && pt2>100.) return 0.932476;
    }
    else return 0;
  }

  return 0;
}

