int eleIdMVAWP_Tight(float _idmva, float _pt, float _eta){
  float eta = fabs(_eta);
  float A = 0.77+(0.56-0.77)*(eta>0.8)+(0.48-0.56)*(eta>1.479);
  float B = 0.52+(0.11-0.52)*(eta>0.8)+(-0.01-0.11)*(eta>1.479);    
  return (_idmva > std::min(A , std::max( B , A+(B-A)/10*(_pt-15) ) ) );
}

void functionsID() {}
