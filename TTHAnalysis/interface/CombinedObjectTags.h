#ifndef CMGTools_TTHAnalysis_CombinedObjectTags_h
#define CMGTools_TTHAnalysis_CombinedObjectTags_h
#include <cmath>
#include <vector>
#include <algorithm>
#include <memory>

class CombinedObjectTags {
 public:
  
  CombinedObjectTags(uint nLep, uint nTau, uint nJet);
  
  void setLepFlags(uint i, bool isL, bool isC, bool isF, bool isT, float conept);
  void setTauFlags(uint i, bool isF, bool isT);
  void setJetFlags(uint i, bool isS);
    
  std::vector<int> getLepsF_byConePt();
    
  std::unique_ptr<bool[]> lepsL;
  std::unique_ptr<bool[]> lepsC;
  std::unique_ptr<bool[]> lepsF;
  std::unique_ptr<bool[]> lepsT;
  std::unique_ptr<bool[]> tausF;
  std::unique_ptr<bool[]> tausT;
  std::unique_ptr<bool[]> jetsS;
  std::unique_ptr<float[]> leps_conept;

private:
  uint nLep_;

};
#endif
