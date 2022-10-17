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
