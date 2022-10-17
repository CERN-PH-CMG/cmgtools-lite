float flipRate_UCSx(float pt, float eta) {
   float scale = 1.35;
   if (pt>=15 && pt<40 && fabs(eta)>=0 && fabs(eta)<0.8 ) return scale*7.36646e-06;
   if (pt>=15 && pt<40 && fabs(eta)>=0.8 && fabs(eta)<1.479 ) return scale*0.000108283;
   if (pt>=15 && pt<40 && fabs(eta)>=1.479 && fabs(eta)<2.5 ) return scale*0.00108401;
   if (pt>=40 && pt<60 && fabs(eta)>=0 && fabs(eta)<0.8 ) return scale*2.34739e-05;
   if (pt>=40 && pt<60 && fabs(eta)>=0.8 && fabs(eta)<1.479 ) return scale*0.000198413;
   if (pt>=40 && pt<60 && fabs(eta)>=1.479 && fabs(eta)<2.5 ) return scale*0.00141664;
   if (pt>=60 && fabs(eta)>=0 && fabs(eta)<0.8 ) return scale*0.00011247;
   if (pt>=60 && pt<80 && fabs(eta)>=0.8 && fabs(eta)<1.479 ) return scale*0.000301189;
   if (pt>=60 && pt<80 && fabs(eta)>=1.479 && fabs(eta)<2.5 ) return scale*0.0020123;
   if (pt>=80 && pt<100 && fabs(eta)>=0.8 && fabs(eta)<1.479 ) return scale*0.000560358;
   if (pt>=80 && pt<100 && fabs(eta)>=1.479 && fabs(eta)<2.5 ) return scale*0.00233948;
   if (pt>=100 && pt<200 && fabs(eta)>=0.8 && fabs(eta)<1.479 ) return scale*0.000295415;
   if (pt>=100 && pt<200 && fabs(eta)>=1.479 && fabs(eta)<2.5 ) return scale*0.00395713;
   if (pt>=200 && fabs(eta)>=0.8 && fabs(eta)<1.479 ) return scale*0.00282565;
   if (pt>=200 && fabs(eta)>=1.479 && fabs(eta)<2.5 ) return scale*0.0127978;
   return 0.;
}
float flipRate_UCSx_Error(float pt, float eta) {
   float scale = 1.35;
   if (pt>=15 && pt<40 && fabs(eta)>=0 && fabs(eta)<0.8 ) return scale*3.6401e-06;
   if (pt>=15 && pt<40 && fabs(eta)>=0.8 && fabs(eta)<1.479 ) return scale*2.89577e-05;
   if (pt>=15 && pt<40 && fabs(eta)>=1.479 && fabs(eta)<2.5 ) return scale*9.84959e-05;
   if (pt>=40 && pt<60 && fabs(eta)>=0 && fabs(eta)<0.8 ) return scale*1.09368e-05;
   if (pt>=40 && pt<60 && fabs(eta)>=0.8 && fabs(eta)<1.479 ) return scale*3.71107e-05;
   if (pt>=40 && pt<60 && fabs(eta)>=1.479 && fabs(eta)<2.5 ) return scale*0.000119599;
   if (pt>=60 && fabs(eta)>=0 && fabs(eta)<0.8 ) return scale*5.90675e-05;
   if (pt>=60 && pt<80 && fabs(eta)>=0.8 && fabs(eta)<1.479 ) return scale*0.000120319;
   if (pt>=60 && pt<80 && fabs(eta)>=1.479 && fabs(eta)<2.5 ) return scale*0.00039592;
   if (pt>=80 && pt<100 && fabs(eta)>=0.8 && fabs(eta)<1.479 ) return scale*0.000285579;
   if (pt>=80 && pt<100 && fabs(eta)>=1.479 && fabs(eta)<2.5 ) return scale*0.000686392;
   if (pt>=100 && pt<200 && fabs(eta)>=0.8 && fabs(eta)<1.479 ) return scale*0.000180937;
   if (pt>=100 && pt<200 && fabs(eta)>=1.479 && fabs(eta)<2.5 ) return scale*0.000965423;
   if (pt>=200 && fabs(eta)>=0.8 && fabs(eta)<1.479 ) return scale*0.00207696;
   if (pt>=200 && fabs(eta)>=1.479 && fabs(eta)<2.5 ) return scale*0.00742097;
   return 0.;
}
