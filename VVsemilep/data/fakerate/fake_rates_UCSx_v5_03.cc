float electronFakeRate_UCSx(float pt, float eta) {
   if (pt>=10 && pt<15 && fabs(eta)>=0 && fabs(eta)<0.8 ) return 0.374124;
   if (pt>=10 && pt<15 && fabs(eta)>=0.8 && fabs(eta)<1.479 ) return 0.478443;
   if (pt>=10 && pt<15 && fabs(eta)>=1.479 && fabs(eta)<2.5 ) return 0.313999;
   if (pt>=15 && pt<25 && fabs(eta)>=0 && fabs(eta)<0.8 ) return 0.101303;
   if (pt>=15 && pt<25 && fabs(eta)>=0.8 && fabs(eta)<1.479 ) return 0.136487;
   if (pt>=15 && pt<25 && fabs(eta)>=1.479 && fabs(eta)<2.5 ) return 0.149813;
   if (pt>=25 && pt<35 && fabs(eta)>=0 && fabs(eta)<0.8 ) return 0.0534611;
   if (pt>=25 && pt<35 && fabs(eta)>=0.8 && fabs(eta)<1.479 ) return 0.080716;
   if (pt>=25 && pt<35 && fabs(eta)>=1.479 && fabs(eta)<2.5 ) return 0.0789684;
   if (pt>=35 && pt<50 && fabs(eta)>=0 && fabs(eta)<0.8 ) return 0.0758515;
   if (pt>=35 && pt<50 && fabs(eta)>=0.8 && fabs(eta)<1.479 ) return 0.0612818;
   if (pt>=35 && pt<50 && fabs(eta)>=1.479 && fabs(eta)<2.5 ) return 0.121294;
   if (pt>=50 && fabs(eta)>=0 && fabs(eta)<0.8 ) return 0.0996618;
   if (pt>=50 && fabs(eta)>=0.8 && fabs(eta)<1.479 ) return 0.13816;
   if (pt>=50 && fabs(eta)>=1.479 && fabs(eta)<2.5 ) return 0.20806;
   return 0.;
}
float electronFakeRate_UCSx_Error(float pt, float eta) {
   if (pt>=10 && pt<15 && fabs(eta)>=0 && fabs(eta)<0.8 ) return 0.102601;
   if (pt>=10 && pt<15 && fabs(eta)>=0.8 && fabs(eta)<1.479 ) return 0.064689;
   if (pt>=10 && pt<15 && fabs(eta)>=1.479 && fabs(eta)<2.5 ) return 0.0613725;
   if (pt>=15 && pt<25 && fabs(eta)>=0 && fabs(eta)<0.8 ) return 0.00865926;
   if (pt>=15 && pt<25 && fabs(eta)>=0.8 && fabs(eta)<1.479 ) return 0.014567;
   if (pt>=15 && pt<25 && fabs(eta)>=1.479 && fabs(eta)<2.5 ) return 0.012532;
   if (pt>=25 && pt<35 && fabs(eta)>=0 && fabs(eta)<0.8 ) return 0.00777352;
   if (pt>=25 && pt<35 && fabs(eta)>=0.8 && fabs(eta)<1.479 ) return 0.00904602;
   if (pt>=25 && pt<35 && fabs(eta)>=1.479 && fabs(eta)<2.5 ) return 0.00774862;
   if (pt>=35 && pt<50 && fabs(eta)>=0 && fabs(eta)<0.8 ) return 0.015786;
   if (pt>=35 && pt<50 && fabs(eta)>=0.8 && fabs(eta)<1.479 ) return 0.0113887;
   if (pt>=35 && pt<50 && fabs(eta)>=1.479 && fabs(eta)<2.5 ) return 0.0219291;
   if (pt>=50 && fabs(eta)>=0 && fabs(eta)<0.8 ) return 0.033801;
   if (pt>=50 && fabs(eta)>=0.8 && fabs(eta)<1.479 ) return 0.0399615;
   if (pt>=50 && fabs(eta)>=1.479 && fabs(eta)<2.5 ) return 0.0480033;
   return 0.;
}
float electronAlternativeFakeRate_UCSx(float pt, float eta) {
   if (pt>=10 && pt<15 && fabs(eta)>=0 && fabs(eta)<0.8 ) return 0.377743;
   if (pt>=10 && pt<15 && fabs(eta)>=0.8 && fabs(eta)<1.479 ) return 0.479465;
   if (pt>=10 && pt<15 && fabs(eta)>=1.479 && fabs(eta)<2.5 ) return 0.315083;
   if (pt>=15 && pt<25 && fabs(eta)>=0 && fabs(eta)<0.8 ) return 0.102743;
   if (pt>=15 && pt<25 && fabs(eta)>=0.8 && fabs(eta)<1.479 ) return 0.137483;
   if (pt>=15 && pt<25 && fabs(eta)>=1.479 && fabs(eta)<2.5 ) return 0.150551;
   if (pt>=25 && pt<35 && fabs(eta)>=0 && fabs(eta)<0.8 ) return 0.056454;
   if (pt>=25 && pt<35 && fabs(eta)>=0.8 && fabs(eta)<1.479 ) return 0.0827422;
   if (pt>=25 && pt<35 && fabs(eta)>=1.479 && fabs(eta)<2.5 ) return 0.0804462;
   if (pt>=35 && pt<50 && fabs(eta)>=0 && fabs(eta)<0.8 ) return 0.0874692;
   if (pt>=35 && pt<50 && fabs(eta)>=0.8 && fabs(eta)<1.479 ) return 0.0698315;
   if (pt>=35 && pt<50 && fabs(eta)>=1.479 && fabs(eta)<2.5 ) return 0.127891;
   if (pt>=50 && fabs(eta)>=0 && fabs(eta)<0.8 ) return 0.127156;
   if (pt>=50 && fabs(eta)>=0.8 && fabs(eta)<1.479 ) return 0.160474;
   if (pt>=50 && fabs(eta)>=1.479 && fabs(eta)<2.5 ) return 0.219421;
   return 0.;
}
float electronQCDMCFakeRate_UCSx(float pt, float eta) {
   if (pt>=10 && pt<15 && fabs(eta)>=0 && fabs(eta)<0.8 ) return 0.463469;
   if (pt>=10 && pt<15 && fabs(eta)>=0.8 && fabs(eta)<1.479 ) return 0.524263;
   if (pt>=10 && pt<15 && fabs(eta)>=1.479 && fabs(eta)<2.5 ) return 0.417145;
   if (pt>=15 && pt<25 && fabs(eta)>=0 && fabs(eta)<0.8 ) return 0.0910771;
   if (pt>=15 && pt<25 && fabs(eta)>=0.8 && fabs(eta)<1.479 ) return 0.154957;
   if (pt>=15 && pt<25 && fabs(eta)>=1.479 && fabs(eta)<2.5 ) return 0.173937;
   if (pt>=25 && pt<35 && fabs(eta)>=0 && fabs(eta)<0.8 ) return 0.0418556;
   if (pt>=25 && pt<35 && fabs(eta)>=0.8 && fabs(eta)<1.479 ) return 0.073533;
   if (pt>=25 && pt<35 && fabs(eta)>=1.479 && fabs(eta)<2.5 ) return 0.129059;
   if (pt>=35 && pt<50 && fabs(eta)>=0 && fabs(eta)<0.8 ) return 0.0428398;
   if (pt>=35 && pt<50 && fabs(eta)>=0.8 && fabs(eta)<1.479 ) return 0.111425;
   if (pt>=35 && pt<50 && fabs(eta)>=1.479 && fabs(eta)<2.5 ) return 0.0965191;
   if (pt>=50 && fabs(eta)>=0 && fabs(eta)<0.8 ) return 0.0758591;
   if (pt>=50 && fabs(eta)>=0.8 && fabs(eta)<1.479 ) return 0.268211;
   if (pt>=50 && fabs(eta)>=1.479 && fabs(eta)<2.5 ) return 0.151431;
   return 0.;
}
float muonFakeRate_UCSx(float pt, float eta) {
   if (pt>=10 && pt<15 && fabs(eta)>=0 && fabs(eta)<1.2 ) return 0.343609;
   if (pt>=10 && pt<15 && fabs(eta)>=1.2 && fabs(eta)<2.1 ) return 0.385942;
   if (pt>=10 && pt<15 && fabs(eta)>=2.1 && fabs(eta)<2.4 ) return 0.42431;
   if (pt>=15 && pt<25 && fabs(eta)>=0 && fabs(eta)<1.2 ) return 0.0890336;
   if (pt>=15 && pt<25 && fabs(eta)>=1.2 && fabs(eta)<2.1 ) return 0.087552;
   if (pt>=15 && pt<25 && fabs(eta)>=2.1 && fabs(eta)<2.4 ) return 0.143485;
   if (pt>=25 && pt<35 && fabs(eta)>=0 && fabs(eta)<1.2 ) return 0.0276982;
   if (pt>=25 && pt<35 && fabs(eta)>=1.2 && fabs(eta)<2.1 ) return 0.0298502;
   if (pt>=25 && pt<35 && fabs(eta)>=2.1 && fabs(eta)<2.4 ) return 0.0471047;
   if (pt>=35 && pt<50 && fabs(eta)>=0 && fabs(eta)<1.2 ) return 0.036255;
   if (pt>=35 && pt<50 && fabs(eta)>=1.2 && fabs(eta)<2.1 ) return 0.03729;
   if (pt>=35 && pt<50 && fabs(eta)>=2.1 && fabs(eta)<2.4 ) return 0.0476111;
   if (pt>=50 && fabs(eta)>=0 && fabs(eta)<1.2 ) return 0.0645243;
   if (pt>=50 && fabs(eta)>=1.2 && fabs(eta)<2.1 ) return 0.0576362;
   if (pt>=50 && fabs(eta)>=2.1 && fabs(eta)<2.4 ) return 0.0701183;
   return 0.;
}
float muonFakeRate_UCSx_Error(float pt, float eta) {
   if (pt>=10 && pt<15 && fabs(eta)>=0 && fabs(eta)<1.2 ) return 0.0167578;
   if (pt>=10 && pt<15 && fabs(eta)>=1.2 && fabs(eta)<2.1 ) return 0.0223931;
   if (pt>=10 && pt<15 && fabs(eta)>=2.1 && fabs(eta)<2.4 ) return 0.0432296;
   if (pt>=15 && pt<25 && fabs(eta)>=0 && fabs(eta)<1.2 ) return 0.00787709;
   if (pt>=15 && pt<25 && fabs(eta)>=1.2 && fabs(eta)<2.1 ) return 0.00931359;
   if (pt>=15 && pt<25 && fabs(eta)>=2.1 && fabs(eta)<2.4 ) return 0.025244;
   if (pt>=25 && pt<35 && fabs(eta)>=0 && fabs(eta)<1.2 ) return 0.00123477;
   if (pt>=25 && pt<35 && fabs(eta)>=1.2 && fabs(eta)<2.1 ) return 0.00166326;
   if (pt>=25 && pt<35 && fabs(eta)>=2.1 && fabs(eta)<2.4 ) return 0.00583996;
   if (pt>=35 && pt<50 && fabs(eta)>=0 && fabs(eta)<1.2 ) return 0.00284027;
   if (pt>=35 && pt<50 && fabs(eta)>=1.2 && fabs(eta)<2.1 ) return 0.00353169;
   if (pt>=35 && pt<50 && fabs(eta)>=2.1 && fabs(eta)<2.4 ) return 0.0109229;
   if (pt>=50 && fabs(eta)>=0 && fabs(eta)<1.2 ) return 0.00917269;
   if (pt>=50 && fabs(eta)>=1.2 && fabs(eta)<2.1 ) return 0.0109255;
   if (pt>=50 && fabs(eta)>=2.1 && fabs(eta)<2.4 ) return 0.0308188;
   return 0.;
}
float muonAlternativeFakeRate_UCSx(float pt, float eta) {
   if (pt>=10 && pt<15 && fabs(eta)>=0 && fabs(eta)<1.2 ) return 0.343743;
   if (pt>=10 && pt<15 && fabs(eta)>=1.2 && fabs(eta)<2.1 ) return 0.386068;
   if (pt>=10 && pt<15 && fabs(eta)>=2.1 && fabs(eta)<2.4 ) return 0.424402;
   if (pt>=15 && pt<25 && fabs(eta)>=0 && fabs(eta)<1.2 ) return 0.0892778;
   if (pt>=15 && pt<25 && fabs(eta)>=1.2 && fabs(eta)<2.1 ) return 0.0877863;
   if (pt>=15 && pt<25 && fabs(eta)>=2.1 && fabs(eta)<2.4 ) return 0.143819;
   if (pt>=25 && pt<35 && fabs(eta)>=0 && fabs(eta)<1.2 ) return 0.0284527;
   if (pt>=25 && pt<35 && fabs(eta)>=1.2 && fabs(eta)<2.1 ) return 0.0305254;
   if (pt>=25 && pt<35 && fabs(eta)>=2.1 && fabs(eta)<2.4 ) return 0.0482937;
   if (pt>=35 && pt<50 && fabs(eta)>=0 && fabs(eta)<1.2 ) return 0.0395472;
   if (pt>=35 && pt<50 && fabs(eta)>=1.2 && fabs(eta)<2.1 ) return 0.0403977;
   if (pt>=35 && pt<50 && fabs(eta)>=2.1 && fabs(eta)<2.4 ) return 0.0507116;
   if (pt>=50 && fabs(eta)>=0 && fabs(eta)<1.2 ) return 0.0851522;
   if (pt>=50 && fabs(eta)>=1.2 && fabs(eta)<2.1 ) return 0.0751169;
   if (pt>=50 && fabs(eta)>=2.1 && fabs(eta)<2.4 ) return 0.0961901;
   return 0.;
}
float muonQCDMCFakeRate_UCSx(float pt, float eta) {
   if (pt>=10 && pt<15 && fabs(eta)>=0 && fabs(eta)<1.2 ) return 0.354776;
   if (pt>=10 && pt<15 && fabs(eta)>=1.2 && fabs(eta)<2.1 ) return 0.408789;
   if (pt>=10 && pt<15 && fabs(eta)>=2.1 && fabs(eta)<2.4 ) return 0.470828;
   if (pt>=15 && pt<25 && fabs(eta)>=0 && fabs(eta)<1.2 ) return 0.0874476;
   if (pt>=15 && pt<25 && fabs(eta)>=1.2 && fabs(eta)<2.1 ) return 0.108587;
   if (pt>=15 && pt<25 && fabs(eta)>=2.1 && fabs(eta)<2.4 ) return 0.139358;
   if (pt>=25 && pt<35 && fabs(eta)>=0 && fabs(eta)<1.2 ) return 0.0571186;
   if (pt>=25 && pt<35 && fabs(eta)>=1.2 && fabs(eta)<2.1 ) return 0.0636855;
   if (pt>=25 && pt<35 && fabs(eta)>=2.1 && fabs(eta)<2.4 ) return 0.0836188;
   if (pt>=35 && pt<50 && fabs(eta)>=0 && fabs(eta)<1.2 ) return 0.0560387;
   if (pt>=35 && pt<50 && fabs(eta)>=1.2 && fabs(eta)<2.1 ) return 0.0593853;
   if (pt>=35 && pt<50 && fabs(eta)>=2.1 && fabs(eta)<2.4 ) return 0.0832994;
   if (pt>=50 && fabs(eta)>=0 && fabs(eta)<1.2 ) return 0.0587057;
   if (pt>=50 && fabs(eta)>=1.2 && fabs(eta)<2.1 ) return 0.0631318;
   if (pt>=50 && fabs(eta)>=2.1 && fabs(eta)<2.4 ) return 0.0637322;
   return 0.;
}
float electronFakeRate_UCSx_IsoTrigs(float pt, float eta) {
   if (pt>=10 && pt<15 && fabs(eta)>=0 && fabs(eta)<0.8 ) return 0.220798;
   if (pt>=10 && pt<15 && fabs(eta)>=0.8 && fabs(eta)<1.479 ) return 0.580497;
   if (pt>=10 && pt<15 && fabs(eta)>=1.479 && fabs(eta)<2.5 ) return 0.333126;
   if (pt>=15 && pt<25 && fabs(eta)>=0 && fabs(eta)<0.8 ) return 0.173966;
   if (pt>=15 && pt<25 && fabs(eta)>=0.8 && fabs(eta)<1.479 ) return 0.213694;
   if (pt>=15 && pt<25 && fabs(eta)>=1.479 && fabs(eta)<2.5 ) return 0.24967;
   if (pt>=25 && pt<35 && fabs(eta)>=0 && fabs(eta)<0.8 ) return 0.141592;
   if (pt>=25 && pt<35 && fabs(eta)>=0.8 && fabs(eta)<1.479 ) return 0.188489;
   if (pt>=25 && pt<35 && fabs(eta)>=1.479 && fabs(eta)<2.5 ) return 0.193299;
   if (pt>=35 && pt<50 && fabs(eta)>=0 && fabs(eta)<0.8 ) return 0.184865;
   if (pt>=35 && pt<50 && fabs(eta)>=0.8 && fabs(eta)<1.479 ) return 0.165801;
   if (pt>=35 && pt<50 && fabs(eta)>=1.479 && fabs(eta)<2.5 ) return 0.270511;
   if (pt>=50 && fabs(eta)>=0 && fabs(eta)<0.8 ) return 0.282862;
   if (pt>=50 && fabs(eta)>=0.8 && fabs(eta)<1.479 ) return 0.292214;
   if (pt>=50 && fabs(eta)>=1.479 && fabs(eta)<2.5 ) return 0.387291;
   return 0.;
}
float electronFakeRate_UCSx_Error_IsoTrigs(float pt, float eta) {
   if (pt>=10 && pt<15 && fabs(eta)>=0 && fabs(eta)<0.8 ) return 0.117379;
   if (pt>=10 && pt<15 && fabs(eta)>=0.8 && fabs(eta)<1.479 ) return 0.0565965;
   if (pt>=10 && pt<15 && fabs(eta)>=1.479 && fabs(eta)<2.5 ) return 0.0503559;
   if (pt>=15 && pt<25 && fabs(eta)>=0 && fabs(eta)<0.8 ) return 0.012186;
   if (pt>=15 && pt<25 && fabs(eta)>=0.8 && fabs(eta)<1.479 ) return 0.0120146;
   if (pt>=15 && pt<25 && fabs(eta)>=1.479 && fabs(eta)<2.5 ) return 0.01797;
   if (pt>=25 && pt<35 && fabs(eta)>=0 && fabs(eta)<0.8 ) return 0.0158084;
   if (pt>=25 && pt<35 && fabs(eta)>=0.8 && fabs(eta)<1.479 ) return 0.0169133;
   if (pt>=25 && pt<35 && fabs(eta)>=1.479 && fabs(eta)<2.5 ) return 0.0146922;
   if (pt>=35 && pt<50 && fabs(eta)>=0 && fabs(eta)<0.8 ) return 0.0309738;
   if (pt>=35 && pt<50 && fabs(eta)>=0.8 && fabs(eta)<1.479 ) return 0.0260184;
   if (pt>=35 && pt<50 && fabs(eta)>=1.479 && fabs(eta)<2.5 ) return 0.0471078;
   if (pt>=50 && fabs(eta)>=0 && fabs(eta)<0.8 ) return 0.0623712;
   if (pt>=50 && fabs(eta)>=0.8 && fabs(eta)<1.479 ) return 0.0598196;
   if (pt>=50 && fabs(eta)>=1.479 && fabs(eta)<2.5 ) return 0.0695031;
   return 0.;
}
float electronAlternativeFakeRate_UCSx_IsoTrigs(float pt, float eta) {
   if (pt>=10 && pt<15 && fabs(eta)>=0 && fabs(eta)<0.8 ) return 0.23204;
   if (pt>=10 && pt<15 && fabs(eta)>=0.8 && fabs(eta)<1.479 ) return 0.58167;
   if (pt>=10 && pt<15 && fabs(eta)>=1.479 && fabs(eta)<2.5 ) return 0.335363;
   if (pt>=15 && pt<25 && fabs(eta)>=0 && fabs(eta)<0.8 ) return 0.176761;
   if (pt>=15 && pt<25 && fabs(eta)>=0.8 && fabs(eta)<1.479 ) return 0.215574;
   if (pt>=15 && pt<25 && fabs(eta)>=1.479 && fabs(eta)<2.5 ) return 0.250951;
   if (pt>=25 && pt<35 && fabs(eta)>=0 && fabs(eta)<0.8 ) return 0.150197;
   if (pt>=25 && pt<35 && fabs(eta)>=0.8 && fabs(eta)<1.479 ) return 0.193336;
   if (pt>=25 && pt<35 && fabs(eta)>=1.479 && fabs(eta)<2.5 ) return 0.196746;
   if (pt>=35 && pt<50 && fabs(eta)>=0 && fabs(eta)<0.8 ) return 0.215181;
   if (pt>=35 && pt<50 && fabs(eta)>=0.8 && fabs(eta)<1.479 ) return 0.192155;
   if (pt>=35 && pt<50 && fabs(eta)>=1.479 && fabs(eta)<2.5 ) return 0.28705;
   if (pt>=50 && fabs(eta)>=0 && fabs(eta)<0.8 ) return 0.338096;
   if (pt>=50 && fabs(eta)>=0.8 && fabs(eta)<1.479 ) return 0.335431;
   if (pt>=50 && fabs(eta)>=1.479 && fabs(eta)<2.5 ) return 0.405235;
   return 0.;
}
float electronQCDMCFakeRate_UCSx_IsoTrigs(float pt, float eta) {
   if (pt>=10 && pt<15 && fabs(eta)>=0 && fabs(eta)<0.8 ) return 0.545757;
   if (pt>=10 && pt<15 && fabs(eta)>=0.8 && fabs(eta)<1.479 ) return 0.624208;
   if (pt>=10 && pt<15 && fabs(eta)>=1.479 && fabs(eta)<2.5 ) return 0.547046;
   if (pt>=15 && pt<25 && fabs(eta)>=0 && fabs(eta)<0.8 ) return 0.16516;
   if (pt>=15 && pt<25 && fabs(eta)>=0.8 && fabs(eta)<1.479 ) return 0.256338;
   if (pt>=15 && pt<25 && fabs(eta)>=1.479 && fabs(eta)<2.5 ) return 0.288052;
   if (pt>=25 && pt<35 && fabs(eta)>=0 && fabs(eta)<0.8 ) return 0.0990945;
   if (pt>=25 && pt<35 && fabs(eta)>=0.8 && fabs(eta)<1.479 ) return 0.184191;
   if (pt>=25 && pt<35 && fabs(eta)>=1.479 && fabs(eta)<2.5 ) return 0.226538;
   if (pt>=35 && pt<50 && fabs(eta)>=0 && fabs(eta)<0.8 ) return 0.111825;
   if (pt>=35 && pt<50 && fabs(eta)>=0.8 && fabs(eta)<1.479 ) return 0.235602;
   if (pt>=35 && pt<50 && fabs(eta)>=1.479 && fabs(eta)<2.5 ) return 0.177848;
   if (pt>=50 && fabs(eta)>=0 && fabs(eta)<0.8 ) return 0.153249;
   if (pt>=50 && fabs(eta)>=0.8 && fabs(eta)<1.479 ) return 0.459864;
   if (pt>=50 && fabs(eta)>=1.479 && fabs(eta)<2.5 ) return 0.251282;
   return 0.;
}
float muonFakeRate_UCSx_IsoTrigs(float pt, float eta) {
   if (pt>=10 && pt<15 && fabs(eta)>=0 && fabs(eta)<1.2 ) return 0.363634;
   if (pt>=10 && pt<15 && fabs(eta)>=1.2 && fabs(eta)<2.1 ) return 0.389502;
   if (pt>=10 && pt<15 && fabs(eta)>=2.1 && fabs(eta)<2.4 ) return 0.46614;
   if (pt>=15 && pt<25 && fabs(eta)>=0 && fabs(eta)<1.2 ) return 0.107164;
   if (pt>=15 && pt<25 && fabs(eta)>=1.2 && fabs(eta)<2.1 ) return 0.122401;
   if (pt>=15 && pt<25 && fabs(eta)>=2.1 && fabs(eta)<2.4 ) return 0.148046;
   if (pt>=25 && pt<35 && fabs(eta)>=0 && fabs(eta)<1.2 ) return 0.0434169;
   if (pt>=25 && pt<35 && fabs(eta)>=1.2 && fabs(eta)<2.1 ) return 0.0491015;
   if (pt>=25 && pt<35 && fabs(eta)>=2.1 && fabs(eta)<2.4 ) return 0.0538764;
   if (pt>=35 && pt<50 && fabs(eta)>=0 && fabs(eta)<1.2 ) return 0.0649291;
   if (pt>=35 && pt<50 && fabs(eta)>=1.2 && fabs(eta)<2.1 ) return 0.0760654;
   if (pt>=35 && pt<50 && fabs(eta)>=2.1 && fabs(eta)<2.4 ) return 0.092768;
   if (pt>=50 && fabs(eta)>=0 && fabs(eta)<1.2 ) return 0.11146;
   if (pt>=50 && fabs(eta)>=1.2 && fabs(eta)<2.1 ) return 0.0981935;
   if (pt>=50 && fabs(eta)>=2.1 && fabs(eta)<2.4 ) return 0.133383;
   return 0.;
}
float muonFakeRate_UCSx_Error_IsoTrigs(float pt, float eta) {
   if (pt>=10 && pt<15 && fabs(eta)>=0 && fabs(eta)<1.2 ) return 0.0132095;
   if (pt>=10 && pt<15 && fabs(eta)>=1.2 && fabs(eta)<2.1 ) return 0.0169688;
   if (pt>=10 && pt<15 && fabs(eta)>=2.1 && fabs(eta)<2.4 ) return 0.0344177;
   if (pt>=15 && pt<25 && fabs(eta)>=0 && fabs(eta)<1.2 ) return 0.00723521;
   if (pt>=15 && pt<25 && fabs(eta)>=1.2 && fabs(eta)<2.1 ) return 0.00949979;
   if (pt>=15 && pt<25 && fabs(eta)>=2.1 && fabs(eta)<2.4 ) return 0.019798;
   if (pt>=25 && pt<35 && fabs(eta)>=0 && fabs(eta)<1.2 ) return 0.00185232;
   if (pt>=25 && pt<35 && fabs(eta)>=1.2 && fabs(eta)<2.1 ) return 0.00252577;
   if (pt>=25 && pt<35 && fabs(eta)>=2.1 && fabs(eta)<2.4 ) return 0.0058389;
   if (pt>=35 && pt<50 && fabs(eta)>=0 && fabs(eta)<1.2 ) return 0.0045009;
   if (pt>=35 && pt<50 && fabs(eta)>=1.2 && fabs(eta)<2.1 ) return 0.00582292;
   if (pt>=35 && pt<50 && fabs(eta)>=2.1 && fabs(eta)<2.4 ) return 0.0134512;
   if (pt>=50 && fabs(eta)>=0 && fabs(eta)<1.2 ) return 0.01404;
   if (pt>=50 && fabs(eta)>=1.2 && fabs(eta)<2.1 ) return 0.0185428;
   if (pt>=50 && fabs(eta)>=2.1 && fabs(eta)<2.4 ) return 0.0513837;
   return 0.;
}
float muonAlternativeFakeRate_UCSx_IsoTrigs(float pt, float eta) {
   if (pt>=10 && pt<15 && fabs(eta)>=0 && fabs(eta)<1.2 ) return 0.363787;
   if (pt>=10 && pt<15 && fabs(eta)>=1.2 && fabs(eta)<2.1 ) return 0.389643;
   if (pt>=10 && pt<15 && fabs(eta)>=2.1 && fabs(eta)<2.4 ) return 0.466236;
   if (pt>=15 && pt<25 && fabs(eta)>=0 && fabs(eta)<1.2 ) return 0.107529;
   if (pt>=15 && pt<25 && fabs(eta)>=1.2 && fabs(eta)<2.1 ) return 0.122739;
   if (pt>=15 && pt<25 && fabs(eta)>=2.1 && fabs(eta)<2.4 ) return 0.148515;
   if (pt>=25 && pt<35 && fabs(eta)>=0 && fabs(eta)<1.2 ) return 0.0447441;
   if (pt>=25 && pt<35 && fabs(eta)>=1.2 && fabs(eta)<2.1 ) return 0.0503755;
   if (pt>=25 && pt<35 && fabs(eta)>=2.1 && fabs(eta)<2.4 ) return 0.0554084;
   if (pt>=35 && pt<50 && fabs(eta)>=0 && fabs(eta)<1.2 ) return 0.0714719;
   if (pt>=35 && pt<50 && fabs(eta)>=1.2 && fabs(eta)<2.1 ) return 0.0832446;
   if (pt>=35 && pt<50 && fabs(eta)>=2.1 && fabs(eta)<2.4 ) return 0.0995706;
   if (pt>=50 && fabs(eta)>=0 && fabs(eta)<1.2 ) return 0.152642;
   if (pt>=50 && fabs(eta)>=1.2 && fabs(eta)<2.1 ) return 0.131075;
   if (pt>=50 && fabs(eta)>=2.1 && fabs(eta)<2.4 ) return 0.191173;
   return 0.;
}
float muonQCDMCFakeRate_UCSx_IsoTrigs(float pt, float eta) {
   if (pt>=10 && pt<15 && fabs(eta)>=0 && fabs(eta)<1.2 ) return 0.37748;
   if (pt>=10 && pt<15 && fabs(eta)>=1.2 && fabs(eta)<2.1 ) return 0.422857;
   if (pt>=10 && pt<15 && fabs(eta)>=2.1 && fabs(eta)<2.4 ) return 0.485531;
   if (pt>=15 && pt<25 && fabs(eta)>=0 && fabs(eta)<1.2 ) return 0.115287;
   if (pt>=15 && pt<25 && fabs(eta)>=1.2 && fabs(eta)<2.1 ) return 0.137049;
   if (pt>=15 && pt<25 && fabs(eta)>=2.1 && fabs(eta)<2.4 ) return 0.167469;
   if (pt>=25 && pt<35 && fabs(eta)>=0 && fabs(eta)<1.2 ) return 0.0882726;
   if (pt>=25 && pt<35 && fabs(eta)>=1.2 && fabs(eta)<2.1 ) return 0.0980888;
   if (pt>=25 && pt<35 && fabs(eta)>=2.1 && fabs(eta)<2.4 ) return 0.113963;
   if (pt>=35 && pt<50 && fabs(eta)>=0 && fabs(eta)<1.2 ) return 0.0907067;
   if (pt>=35 && pt<50 && fabs(eta)>=1.2 && fabs(eta)<2.1 ) return 0.0919988;
   if (pt>=35 && pt<50 && fabs(eta)>=2.1 && fabs(eta)<2.4 ) return 0.117132;
   if (pt>=50 && fabs(eta)>=0 && fabs(eta)<1.2 ) return 0.0993451;
   if (pt>=50 && fabs(eta)>=1.2 && fabs(eta)<2.1 ) return 0.106613;
   if (pt>=50 && fabs(eta)>=2.1 && fabs(eta)<2.4 ) return 0.0941294;
   return 0.;
}
