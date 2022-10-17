
int tauIdx1(int lep1pdg, int lep2pdg, int lep3pdg, int lep4pdg = 0){
    if(abs(lep1pdg)==15) return 0;
    if(abs(lep2pdg)==15) return 1;
    if(abs(lep3pdg)==15) return 2;
    if(abs(lep4pdg)==15) return 3;
    return -1;
}

int tauIdx2(int lep1pdg, int lep2pdg, int lep3pdg, int lep4pdg = 0){
    int firstTau = tauIdx1(lep1pdg, lep2pdg, lep3pdg, lep4pdg);
    if(firstTau == -1) return -1;
    if(abs(lep2pdg)==15 && firstTau<1) return 1;
    if(abs(lep3pdg)==15 && firstTau<2) return 2;
    if(abs(lep4pdg)==15 && firstTau<3) return 3;
    return -1;
}

int isConv(int nLep, int lep1mcUCSX, int lep2mcUCSX, int lep3mcUCSX, int lep4mcUCSX = 0) {
    if(nLep == 3) return (lep1mcUCSX==4 || lep2mcUCSX==4 || lep3mcUCSX==4);
    return (lep1mcUCSX==4 || lep2mcUCSX==4 || lep3mcUCSX==4 || lep4mcUCSX==4);
}

int isFake(int nLep, int lep1mcUCSX, int lep2mcUCSX, int lep3mcUCSX, int lep4mcUCSX = 0) {
    if(nLep == 3) return ((lep1mcUCSX==2 || lep1mcUCSX==3) || (lep2mcUCSX==2 || lep2mcUCSX==3) || (lep3mcUCSX==2 || lep3mcUCSX==3));
    return ((lep1mcUCSX==2 || lep1mcUCSX==3) || (lep2mcUCSX==2 || lep2mcUCSX==3) || (lep3mcUCSX==2 || lep3mcUCSX==3) || (lep4mcUCSX==2 || lep4mcUCSX==3));
}

int isFakeHF(int nLep, int lep1mcUCSX, int lep2mcUCSX, int lep3mcUCSX, int lep4mcUCSX = 0) {
    if(nLep == 3) return (lep1mcUCSX==3 || lep2mcUCSX==3 || lep3mcUCSX==3);
    return (lep1mcUCSX==3 || lep2mcUCSX==3 || lep3mcUCSX==3 || lep4mcUCSX==3);
}

int isFakeLF(int nLep, int lep1mcUCSX, int lep2mcUCSX, int lep3mcUCSX, int lep4mcUCSX = 0) {
    if(nLep == 3) return (lep1mcUCSX==2 || lep2mcUCSX==2 || lep3mcUCSX==2);
    return (lep1mcUCSX==2 || lep2mcUCSX==2 || lep3mcUCSX==2 || lep4mcUCSX==2);
}

int isPrompt(int nLep, int lep1mcUCSX, int lep2mcUCSX, int lep3mcUCSX, int lep4mcUCSX = 0) {
    if(nLep == 3) return ((lep1mcUCSX==0 || lep1mcUCSX==1) && (lep2mcUCSX==0 || lep2mcUCSX==1) && (lep3mcUCSX==0 || lep3mcUCSX==1));
    return ((lep1mcUCSX==0 || lep1mcUCSX==1) && (lep2mcUCSX==0 || lep2mcUCSX==1) && (lep3mcUCSX==0 || lep3mcUCSX==1) && (lep4mcUCSX==0 || lep4mcUCSX==1));
}

int isGoodFake(float pt, int isTight) {
    if(pt == 0) return 0;
    if(isTight) return 0;
    return 1;
}

int allTight(int nLep, int l1isTight, int l2isTight, int l3isTight, int l4isTight = 0){
    if(nLep == 3) return ((l1isTight+l2isTight+l3isTight)==3);
    return ((l1isTight+l2isTight+l3isTight+l4isTight)==4);
}

int countTaus(int nLep, int l1pdgId, int l2pdgId, int l3pdgId, int l4pdgId = 0){
    if(nLep == 3) return (abs(l1pdgId)==15)+(abs(l2pdgId)==15)+(abs(l3pdgId)==15);
    return (abs(l1pdgId)==15)+(abs(l2pdgId)==15)+(abs(l3pdgId)==15)+(abs(l4pdgId)==15);
}

float srMll(int nLep, float mllAllFlavors, float mllOnlyLight, float mllOnlyTaus) {
    if(nLep==3) return mllOnlyLight;
    return mllAllFlavors;
}

float srMt(int nLep, float mtAllFlavors, float mtOnlyLight, float mtOnlyTaus) {
    if(nLep==3) return mtOnlyLight;
    return mtAllFlavors;
}

int nLepFlavor(int nTau, int is4l, int is5l){

    if(!is4l && !is5l) return 0;
    if(is5l          ) return 6;
    if(nTau == 0     ) return 1;
    if(nTau == 1     ) return 2;
    if(nTau == 2     ) return 3;
    if(nTau == 3     ) return 4; 
    if(nTau == 4     ) return 5; 

    return 0;
}

int BR(int nLep, int nTau, int nOSSF, int nOSLF, int nOSTF){

    if(nLep == 3 && nTau == 0 && nOSSF >= 1              ) return  1;
    if(nLep == 3 && nTau == 0 && nOSSF <  1              ) return  2;
    if(nLep == 3 && nTau == 1 && nOSSF >= 1              ) return  3;
    if(nLep == 3 && nTau == 1 && nOSSF <  1 && nOSLF >= 1) return  4;
    if(nLep == 3 && nTau == 1 && nOSLF <  1              ) return  5;
    if(nLep == 3 && nTau == 2                            ) return  6;
    if(nLep == 4 && nTau == 0 && nOSSF >= 2              ) return  7;
    if(nLep == 4 && nTau == 0 && nOSSF <= 1              ) return  8;
    if(nLep == 4 && nTau == 1                            ) return  9;
    if(nLep == 4 && nTau == 2 && nOSSF >= 2              ) return 10;
    if(nLep == 4 && nTau == 2 && nOSSF <= 1              ) return 11;

    return 0;
}

int SR3lA(float mT2L, float mT2T, float mll, float mT, float met, int offset = 0) {

    if(mll >= 0 && mll < 75) {
        if (mT >=   0 && mT < 100 && met >=  50 && met < 100) return offset +  1;
        if (mT >=   0 && mT < 100 && met >= 100 && met < 150) return offset +  2;
        if (mT >=   0 && mT < 100 && met >= 150 && met < 200) return offset +  3;
        if (mT >=   0 && mT < 100 && met >= 200 && met < 250) return offset +  4;
        if (mT >=   0 && mT < 100 && met >= 250             ) return offset +  5;
        if (mT >= 100 && mT < 160 && met >=  50 && met < 100) return offset +  6;
        if (mT >= 100 && mT < 160 && met >= 100 && met < 150) return offset +  7;
        if (mT >= 100 && mT < 160 && met >= 150 && met < 200) return offset +  8;
        if (mT >= 100 && mT < 160 && met >= 200             ) return offset +  9;
        if (mT >= 160 &&             met >=  50 && met < 100) return offset + 10;
        if (mT >= 160 &&             met >= 100 && met < 150) return offset + 11;
        if (mT >= 160 &&             met >= 150 && met < 200) return offset + 12;
        if (mT >= 160 &&             met >= 200 && met < 250) return offset + 13;
        if (mT >= 160 &&             met >= 250             ) return offset + 14;
    }
    if(mll >= 75 && mll < 105) {
        if (mT >=   0 && mT < 100 && met >=  50 && met < 100) return offset + 15;
        if (mT >=   0 && mT < 100 && met >= 100 && met < 150) return offset + 16;
        if (mT >=   0 && mT < 100 && met >= 150 && met < 200) return offset + 17;
        if (mT >=   0 && mT < 100 && met >= 200 && met < 250) return offset + 18;
        if (mT >=   0 && mT < 100 && met >= 250 && met < 400) return offset + 19;
        if (mT >=   0 && mT < 100 && met >= 400 && met < 550) return offset + 20;
        if (mT >=   0 && mT < 100 && met >= 550             ) return offset + 21;
        if (mT >= 100 && mT < 160 && met >=  50 && met < 100) return offset + 22;
        if (mT >= 100 && mT < 160 && met >= 100 && met < 150) return offset + 23;
        if (mT >= 100 && mT < 160 && met >= 150 && met < 200) return offset + 24;
        if (mT >= 100 && mT < 160 && met >= 200             ) return offset + 25;
        if (mT >= 160 &&             met >=  50 && met < 100) return offset + 26;
        if (mT >= 160 &&             met >= 100 && met < 150) return offset + 27;
        if (mT >= 160 &&             met >= 150 && met < 200) return offset + 28;
        if (mT >= 160 &&             met >= 200 && met < 250) return offset + 29;
        if (mT >= 160 &&             met >= 250 && met < 400) return offset + 30;
        if (mT >= 160 &&             met >= 400             ) return offset + 31;
    }
    if(mll >= 105) {
        if (mT >=   0 && mT < 100 && met >=  50 && met < 100) return offset + 32;
        if (mT >=   0 && mT < 100 && met >= 100 && met < 150) return offset + 33;
        if (mT >=   0 && mT < 100 && met >= 150 && met < 200) return offset + 34;
        if (mT >=   0 && mT < 100 && met >= 200 && met < 250) return offset + 35;
        if (mT >=   0 && mT < 100 && met >= 250             ) return offset + 36;
        if (mT >= 100 && mT < 160 && met >=  50 && met < 100) return offset + 37;
        if (mT >= 100 && mT < 160 && met >= 100 && met < 150) return offset + 38;
        if (mT >= 100 && mT < 160 && met >= 150 && met < 200) return offset + 39;
        if (mT >= 100 && mT < 160 && met >= 200             ) return offset + 40;
        if (mT >= 160 &&             met >=  50 && met < 100) return offset + 41;
        if (mT >= 160 &&             met >= 100 && met < 150) return offset + 42;
        if (mT >= 160 &&             met >= 150 && met < 200) return offset + 43;
        if (mT >= 160 &&             met >= 200             ) return offset + 44;
    }
    return 0;
}

int SR3lB(float mT2L, float mT2T, float mll, float mT, float met, int offset = 0) {

    if(mll < 100){
        if(mT <  120 && met >=  50 && met < 100) return offset + 1;
        if(mT <  120 && met >= 100             ) return offset + 2;
        if(mT >= 120 && met >=  50             ) return offset + 3;
    }
    if(mll >= 100) {
        if(mT <  120 && met >=  50 && met < 100) return offset + 4;
        if(mT <  120 && met >= 100             ) return offset + 5;
        if(mT >= 120 && met >=  50             ) return offset + 6;
    }

    return 0;
}

int SR3lC(float mT2L, float mT2T, float mll, float mT, float met, int offset = 0) {

    if(mT2L < 100  && mll >=   0 && mll <  75 && met >=  50 && met < 100) return offset +  1;
    if(mT2L < 100  && mll >=   0 && mll <  75 && met >= 100 && met < 150) return offset +  2;
    if(mT2L < 100  && mll >=   0 && mll <  75 && met >= 150 && met < 200) return offset +  3;
    if(mT2L < 100  && mll >=   0 && mll <  75 && met >= 200 && met < 250) return offset +  4;
    if(mT2L < 100  && mll >=   0 && mll <  75 && met >= 250             ) return offset +  5;
    if(               mll >=  75 && mll < 105 && met >=  50 && met < 100) return offset +  6;
    if(               mll >=  75 && mll < 105 && met >= 100 && met < 150) return offset +  7;
    if(               mll >=  75 && mll < 105 && met >= 150 && met < 200) return offset +  8;
    if(               mll >=  75 && mll < 105 && met >= 200 && met < 300) return offset +  9;
    if(               mll >=  75 && mll < 105 && met >= 300 && met < 400) return offset + 10;
    if(               mll >=  75 && mll < 105 && met >= 400             ) return offset + 11;
    if(mT2L < 100  && mll >= 105 &&              met >=  50 && met < 100) return offset + 12;
    if(mT2L < 100  && mll >= 105 &&              met >= 100 && met < 150) return offset + 13;
    if(mT2L < 100  && mll >= 105 &&              met >= 150 && met < 200) return offset + 14;
    if(mT2L < 100  && mll >= 105 &&              met >= 200 && met < 250) return offset + 15;
    if(mT2L < 100  && mll >= 105 &&              met >= 250             ) return offset + 16;
    if(mT2L >= 100 && (mll < 75 || mll >= 105) && met >= 50 && met < 200) return offset + 17;
    if(mT2L >= 100 && (mll < 75 || mll >= 105) && met >= 200            ) return offset + 18;
    return 0;
}

int SR3lD(float mT2L, float mT2T, float mll, float mT, float met, int offset = 0) {

    if(mT2L >= 0 && mT2L < 100){
        if(mll >=   0 && mll <  60 && met >=  50 && met < 100) return offset +  1;
        if(mll >=   0 && mll <  60 && met >= 100 && met < 150) return offset +  2;
        if(mll >=   0 && mll <  60 && met >= 150 && met < 200) return offset +  3;
        if(mll >=   0 && mll <  60 && met >= 200 && met < 250) return offset +  4;
        if(mll >=   0 && mll <  60 && met >= 250             ) return offset +  5;
        if(mll >=  60 && mll < 100 && met >=  50 && met < 100) return offset +  6;
        if(mll >=  60 && mll < 100 && met >= 100 && met < 150) return offset +  7;
        if(mll >=  60 && mll < 100 && met >= 150 && met < 200) return offset +  8;
        if(mll >=  60 && mll < 100 && met >= 200 && met < 250) return offset +  9;
        if(mll >=  60 && mll < 100 && met >= 250             ) return offset + 10;
        if(mll >= 100 &&              met >=  50 && met < 100) return offset + 11;
        if(mll >= 100 &&              met >= 100 && met < 150) return offset + 12;
        if(mll >= 100 &&              met >= 150 && met < 200) return offset + 13;
        if(mll >= 100 &&              met >= 200             ) return offset + 14;
    }
    if(mT2L >= 100) {
        if(met >= 50 && met < 200                            ) return offset + 15;
        if(met >= 200                                        ) return offset + 16;
    }

    return 0;
}

int SR3lE(float mT2L, float mT2T, float mll, float mT, float met, int offset = 0) {

    if(mT2T >= 0 && mT2T < 100){
        if(mll >=   0 && mll <  60 && met >=  50 && met < 100) return offset +  1;
        if(mll >=   0 && mll <  60 && met >= 100 && met < 150) return offset +  2;
        if(mll >=   0 && mll <  60 && met >= 150 && met < 200) return offset +  3;
        if(mll >=   0 && mll <  60 && met >= 200 && met < 250) return offset +  4;
        if(mll >=   0 && mll <  60 && met >= 250             ) return offset +  5;
        if(mll >=  60 && mll < 100 && met >=  50 && met < 100) return offset +  6;
        if(mll >=  60 && mll < 100 && met >= 100 && met < 150) return offset +  7;
        if(mll >=  60 && mll < 100 && met >= 150 && met < 200) return offset +  8;
        if(mll >=  60 && mll < 100 && met >= 200 && met < 250) return offset +  9;
        if(mll >=  60 && mll < 100 && met >= 250             ) return offset + 10;
        if(mll >= 100 &&              met >=  50             ) return offset + 11;
    }
    if(mT2T >= 100) {
        if(met >= 50                                         ) return offset + 12;
    }

    return 0;
}

int SR3lF(float mT2L, float mT2T, float mll, float mT, float met, int offset = 0) {

    if(mT2T >= 0 && mT2T < 100){
        if(mll >=   0 && mll < 100 && met >=  50 && met < 100) return offset +  1;
        if(mll >=   0 && mll < 100 && met >= 100 && met < 150) return offset +  2;
        if(mll >=   0 && mll < 100 && met >= 150 && met < 200) return offset +  3;
        if(mll >=   0 && mll < 100 && met >= 200 && met < 250) return offset +  4;
        if(mll >=   0 && mll < 100 && met >= 250 && met < 300) return offset +  5;
        if(mll >=   0 && mll < 100 && met >= 300             ) return offset +  6;
        if(mll >= 100 &&              met >=  50 && met < 100) return offset +  7;
        if(mll >= 100 &&              met >= 100 && met < 150) return offset +  8;
        if(mll >= 100 &&              met >= 150 && met < 200) return offset +  9;
        if(mll >= 100 &&              met >= 200             ) return offset + 10;
    }
    if(mT2T >= 100) {
        if(met >= 50 && met < 200                            ) return offset + 11;
        if(met >= 200                                        ) return offset + 12;
    }

    return 0;
}

int SR4lG(float mT2L, float mT2T, float mll, float mT, float met, int offset = 0) {

    if(met >=   0 && met <  50) return offset + 1;
    if(met >=  50 && met < 100) return offset + 2;
    if(met >= 100 && met < 150) return offset + 3;
    if(met >= 150 && met < 200) return offset + 4;
    if(met >= 200             ) return offset + 5;

    return 0;
}

int SR4lH(float mT2L, float mT2T, float mll, float mT, float met, int offset = 0) {

    if(met >=   0 && met <  50) return offset + 1;
    if(met >=  50 && met < 100) return offset + 2;
    if(met >= 100 && met < 150) return offset + 3;
    if(met >= 150             ) return offset + 4;

    return 0;
}

int SR4lK(float mT2L, float mT2T, float mll, float mT, float met, int offset = 0) {

    if(met >=   0 && met < 100) return offset + 1;
    if(met >= 100 && met < 150) return offset + 2;
    if(met >= 150             ) return offset + 3;

    return 0;
}

int SR3l(int nTau, int nOSSF, int nOSLF, float mT2L, float mT2T, float mll, float mT, float met){

    // 3 light
    if(nTau == 0 && nOSSF >= 1              ) return SR3lA(mT2L, mT2T, mll, mT, met,  0);
    if(nTau == 0 && nOSSF <  1              ) return SR3lB(mT2L, mT2T, mll, mT, met, 44);
    // 2 light + 1 tau
    if(nTau == 1 && nOSSF >= 1              ) return SR3lC(mT2L, mT2T, mll, mT, met, 50);
    if(nTau == 1 && nOSSF <  1 && nOSLF >= 1) return SR3lD(mT2L, mT2T, mll, mT, met, 68);
    if(nTau == 1 && nOSLF <  1              ) return SR3lE(mT2L, mT2T, mll, mT, met, 84);
    // 1 light + 2 tau
    if(nTau == 2                            ) return SR3lF(mT2L, mT2T, mll, mT, met, 96);
    return 0;
}

int SR4l(int nTau, int nOSSF, int nOSLF, float mT2L, float mT2T, float mll, float mT, float met){

    // 4 light
    if(nTau == 0 && nOSSF >= 2              ) return SR4lG(mT2L, mT2T, mll, mT, met, 109);
    if(nTau == 0 && nOSSF <= 1              ) return SR4lH(mT2L, mT2T, mll, mT, met, 113);
    // 3light + 1tau
    if(nTau == 1                            ) return SR4lH(mT2L, mT2T, mll, mT, met, 117);
    // 2light + 2tau
    if(nTau == 2 && nOSSF >= 2              ) return SR4lH(mT2L, mT2T, mll, mT, met, 121);
    if(nTau == 2 && nOSSF <= 1              ) return SR4lK(mT2L, mT2T, mll, mT, met, 125);
    return 0;
}

int SR(int nLep, int nTau, int nOSSF, int nOSLF, float mT2L, float mT2T, float mll, float mT, float met) {

    if(nLep == 3)
        return SR3l(nTau, nOSSF, nOSLF, mT2L, mT2T, mll, mT, met);
    if(nLep == 4)
        return SR4l(nTau, nOSSF, nOSLF, mT2L, mT2T, mll, mT, met);
    return 0;
}

int SuperSig(int nLep, int nTau, int nOSSF, int nOSLF, float mT2L, float mT2T, float mll, float mT, float met) {

    if(nLep == 3){
        if(nTau==0 && (mT   >= 120 && met >= 200)) return 1;
        if(nTau==1 && (mT2L >=  50 && met >= 200)) return 2;
        if(nTau==2 && (mT2T >=  50 && met >= 200)) return 3;
        if(nTau==2 &&                 met >=  75 ) return 4;
    }
    if(nLep == 4){
        if(met >= 200                            ) return 5;
    }
    return 0;
}

void functionsEWK() {}
