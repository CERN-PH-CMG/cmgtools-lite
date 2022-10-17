#include "CMGTools/TTHAnalysis/interface/CombinedObjectTags.h"

CombinedObjectTags::CombinedObjectTags(uint nLep, uint nTau, uint nJet){
  nLep_ = nLep;
  lepsL.reset(new bool[nLep]); std::fill_n(lepsL.get(),nLep,false);
  lepsC.reset(new bool[nLep]); std::fill_n(lepsC.get(),nLep,false);
  lepsF.reset(new bool[nLep]); std::fill_n(lepsF.get(),nLep,false);
  lepsT.reset(new bool[nLep]); std::fill_n(lepsT.get(),nLep,false);
  tausF.reset(new bool[nTau]); std::fill_n(tausF.get(),nTau,false);
  tausT.reset(new bool[nTau]); std::fill_n(tausT.get(),nTau,false);
  jetsS.reset(new bool[nJet]); std::fill_n(jetsS.get(),nJet,false);
  leps_conept.reset(new float[nLep]); std::fill_n(leps_conept.get(),nLep,0);
}

void CombinedObjectTags::setLepFlags(uint i, bool isL, bool isC, bool isF, bool isT, float conept){
  lepsL[i] = isL; lepsC[i] = isC; lepsF[i] = isF; lepsT[i] = isT; leps_conept[i] = conept;
}
void CombinedObjectTags::setTauFlags(uint i, bool isF, bool isT){
  tausF[i] = isF; tausT[i] = isT;
}
void CombinedObjectTags::setJetFlags(uint i, bool isS){
  jetsS[i] = isS;
}

std::vector<int> CombinedObjectTags::getLepsF_byConePt(){
  std::vector<int> out;
  std::vector<std::pair<uint,float> > leps;
  for (uint i=0; i<nLep_; i++) if (lepsF[i]) leps.push_back(std::make_pair(i,leps_conept[i]));
  std::stable_sort(leps.begin(),leps.end(),[](std::pair<uint,float> a, std::pair<uint,float> b){return (a.second>b.second);});
  for (auto x : leps) out.push_back(x.first);
  return out;
}
