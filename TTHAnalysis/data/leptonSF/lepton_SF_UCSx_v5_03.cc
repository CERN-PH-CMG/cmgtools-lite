float electronScaleFactorHighHT_UCSx(float pt, float eta) {
   if (pt>=10 && pt<20 && fabs(eta)>=0 && fabs(eta)<0.8 ) return 0.800833;
   if (pt>=10 && pt<20 && fabs(eta)>=0.8 && fabs(eta)<1.442 ) return 1.09259;
   if (pt>=10 && pt<20 && fabs(eta)>=1.442 && fabs(eta)<1.566 ) return 1.38004;
   if (pt>=10 && pt<20 && fabs(eta)>=1.566 && fabs(eta)<2 ) return 1.06353;
   if (pt>=10 && pt<20 && fabs(eta)>=2 && fabs(eta)<2.5 ) return 1.01303;
   if (pt>=20 && pt<30 && fabs(eta)>=0 && fabs(eta)<0.8 ) return 0.951939;
   if (pt>=20 && pt<30 && fabs(eta)>=0.8 && fabs(eta)<1.442 ) return 0.978131;
   if (pt>=20 && pt<30 && fabs(eta)>=1.442 && fabs(eta)<1.566 ) return 1.00001;
   if (pt>=20 && pt<30 && fabs(eta)>=1.566 && fabs(eta)<2 ) return 0.944541;
   if (pt>=20 && pt<30 && fabs(eta)>=2 && fabs(eta)<2.5 ) return 0.958243;
   if (pt>=30 && pt<40 && fabs(eta)>=0 && fabs(eta)<0.8 ) return 0.974265;
   if (pt>=30 && pt<40 && fabs(eta)>=0.8 && fabs(eta)<1.442 ) return 0.979292;
   if (pt>=30 && pt<40 && fabs(eta)>=1.442 && fabs(eta)<1.566 ) return 0.978247;
   if (pt>=30 && pt<40 && fabs(eta)>=1.566 && fabs(eta)<2 ) return 0.973954;
   if (pt>=30 && pt<40 && fabs(eta)>=2 && fabs(eta)<2.5 ) return 0.982194;
   if (pt>=40 && pt<50 && fabs(eta)>=0 && fabs(eta)<0.8 ) return 0.979367;
   if (pt>=40 && pt<50 && fabs(eta)>=0.8 && fabs(eta)<1.442 ) return 0.984915;
   if (pt>=40 && pt<50 && fabs(eta)>=1.442 && fabs(eta)<1.566 ) return 0.989583;
   if (pt>=40 && pt<50 && fabs(eta)>=1.566 && fabs(eta)<2 ) return 1.00021;
   if (pt>=40 && pt<50 && fabs(eta)>=2 && fabs(eta)<2.5 ) return 0.995648;
   if (pt>=50 && fabs(eta)>=0 && fabs(eta)<0.8 ) return 0.980086;
   if (pt>=50 && fabs(eta)>=0.8 && fabs(eta)<1.442 ) return 0.980024;
   if (pt>=50 && fabs(eta)>=1.442 && fabs(eta)<1.566 ) return 0.986589;
   if (pt>=50 && fabs(eta)>=1.566 && fabs(eta)<2 ) return 0.984587;
   if (pt>=50 && fabs(eta)>=2 && fabs(eta)<2.5 ) return 0.995184;
   return 0.;
}
float electronScaleFactorLowHT_UCSx(float pt, float eta) {
   if (pt>=10 && pt<20 && fabs(eta)>=0 && fabs(eta)<0.8 ) return 0.81309;
   if (pt>=10 && pt<20 && fabs(eta)>=0.8 && fabs(eta)<1.442 ) return 1.09402;
   if (pt>=10 && pt<20 && fabs(eta)>=1.442 && fabs(eta)<1.566 ) return 1.38969;
   if (pt>=10 && pt<20 && fabs(eta)>=1.566 && fabs(eta)<2 ) return 1.05715;
   if (pt>=10 && pt<20 && fabs(eta)>=2 && fabs(eta)<2.5 ) return 1.01151;
   if (pt>=20 && pt<30 && fabs(eta)>=0 && fabs(eta)<0.8 ) return 0.952485;
   if (pt>=20 && pt<30 && fabs(eta)>=0.8 && fabs(eta)<1.442 ) return 0.978021;
   if (pt>=20 && pt<30 && fabs(eta)>=1.442 && fabs(eta)<1.566 ) return 0.999009;
   if (pt>=20 && pt<30 && fabs(eta)>=1.566 && fabs(eta)<2 ) return 0.947156;
   if (pt>=20 && pt<30 && fabs(eta)>=2 && fabs(eta)<2.5 ) return 0.957892;
   if (pt>=30 && pt<40 && fabs(eta)>=0 && fabs(eta)<0.8 ) return 0.974451;
   if (pt>=30 && pt<40 && fabs(eta)>=0.8 && fabs(eta)<1.442 ) return 0.978913;
   if (pt>=30 && pt<40 && fabs(eta)>=1.442 && fabs(eta)<1.566 ) return 0.979384;
   if (pt>=30 && pt<40 && fabs(eta)>=1.566 && fabs(eta)<2 ) return 0.973866;
   if (pt>=30 && pt<40 && fabs(eta)>=2 && fabs(eta)<2.5 ) return 0.981911;
   if (pt>=40 && pt<50 && fabs(eta)>=0 && fabs(eta)<0.8 ) return 0.979478;
   if (pt>=40 && pt<50 && fabs(eta)>=0.8 && fabs(eta)<1.442 ) return 0.984782;
   if (pt>=40 && pt<50 && fabs(eta)>=1.442 && fabs(eta)<1.566 ) return 0.990569;
   if (pt>=40 && pt<50 && fabs(eta)>=1.566 && fabs(eta)<2 ) return 1.00085;
   if (pt>=40 && pt<50 && fabs(eta)>=2 && fabs(eta)<2.5 ) return 0.996501;
   if (pt>=50 && fabs(eta)>=0 && fabs(eta)<0.8 ) return 0.980182;
   if (pt>=50 && fabs(eta)>=0.8 && fabs(eta)<1.442 ) return 0.979994;
   if (pt>=50 && fabs(eta)>=1.442 && fabs(eta)<1.566 ) return 0.988436;
   if (pt>=50 && fabs(eta)>=1.566 && fabs(eta)<2 ) return 0.984572;
   if (pt>=50 && fabs(eta)>=2 && fabs(eta)<2.5 ) return 0.995253;
   return 0.;
}
float muonScaleFactor_UCSx(float pt, float eta) {
   if (pt>=10 && pt<20 && fabs(eta)>=0 && fabs(eta)<0.9 ) return 0.950673;
   if (pt>=10 && pt<20 && fabs(eta)>=0.9 && fabs(eta)<1.2 ) return 0.959971;
   if (pt>=10 && pt<20 && fabs(eta)>=1.2 && fabs(eta)<2.1 ) return 0.96344;
   if (pt>=10 && pt<20 && fabs(eta)>=2.1 && fabs(eta)<2.4 ) return 0.97954;
   if (pt>=20 && pt<25 && fabs(eta)>=0 && fabs(eta)<0.9 ) return 0.968778;
   if (pt>=20 && pt<25 && fabs(eta)>=0.9 && fabs(eta)<1.2 ) return 0.985696;
   if (pt>=20 && pt<25 && fabs(eta)>=1.2 && fabs(eta)<2.1 ) return 0.986646;
   if (pt>=20 && pt<25 && fabs(eta)>=2.1 && fabs(eta)<2.4 ) return 0.961432;
   if (pt>=25 && pt<30 && fabs(eta)>=0 && fabs(eta)<0.9 ) return 0.986112;
   if (pt>=25 && pt<30 && fabs(eta)>=0.9 && fabs(eta)<1.2 ) return 0.982328;
   if (pt>=25 && pt<30 && fabs(eta)>=1.2 && fabs(eta)<2.1 ) return 0.981606;
   if (pt>=25 && pt<30 && fabs(eta)>=2.1 && fabs(eta)<2.4 ) return 0.964637;
   if (pt>=30 && pt<40 && fabs(eta)>=0 && fabs(eta)<0.9 ) return 0.989584;
   if (pt>=30 && pt<40 && fabs(eta)>=0.9 && fabs(eta)<1.2 ) return 0.990363;
   if (pt>=30 && pt<40 && fabs(eta)>=1.2 && fabs(eta)<2.1 ) return 0.989629;
   if (pt>=30 && pt<40 && fabs(eta)>=2.1 && fabs(eta)<2.4 ) return 0.954459;
   if (pt>=40 && pt<50 && fabs(eta)>=0 && fabs(eta)<0.9 ) return 0.990997;
   if (pt>=40 && pt<50 && fabs(eta)>=0.9 && fabs(eta)<1.2 ) return 0.990606;
   if (pt>=40 && pt<50 && fabs(eta)>=1.2 && fabs(eta)<2.1 ) return 0.991023;
   if (pt>=40 && pt<50 && fabs(eta)>=2.1 && fabs(eta)<2.4 ) return 0.951617;
   if (pt>=50 && pt<60 && fabs(eta)>=0 && fabs(eta)<0.9 ) return 0.987545;
   if (pt>=50 && pt<60 && fabs(eta)>=0.9 && fabs(eta)<1.2 ) return 0.989335;
   if (pt>=50 && pt<60 && fabs(eta)>=1.2 && fabs(eta)<2.1 ) return 0.99151;
   if (pt>=50 && pt<60 && fabs(eta)>=2.1 && fabs(eta)<2.4 ) return 0.94982;
   if (pt>=60 && fabs(eta)>=0 && fabs(eta)<0.9 ) return 0.992751;
   if (pt>=60 && fabs(eta)>=0.9 && fabs(eta)<1.2 ) return 0.9878;
   if (pt>=60 && fabs(eta)>=1.2 && fabs(eta)<2.1 ) return 0.988131;
   if (pt>=60 && fabs(eta)>=2.1 && fabs(eta)<2.4 ) return 0.958638;
   return 0.;
}

float leptonScaleFactor_UCSx(int pdgId, float pt, float eta, float ht) {
  if (abs(pdgId)==13) return muonScaleFactor_UCSx(pt, eta);
  else if (abs(pdgId)==11){
    if (ht>300) return electronScaleFactorHighHT_UCSx(pt, eta);
      else return electronScaleFactorLowHT_UCSx(pt, eta);
  }
  return 0.;
}
