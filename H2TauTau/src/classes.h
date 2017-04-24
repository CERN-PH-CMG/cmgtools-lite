#define G__DICTIONARY

#include "DataFormats/Common/interface/Wrapper.h"
#include "CMGTools/H2TauTau/interface/TriggerEfficiency.h"
#include "CMGTools/H2TauTau/interface/METSignificance.h"
#include "CMGTools/H2TauTau/interface/HTTRecoilCorrector.h"

namespace {
  struct CMGTools_H2TauTau {

    TriggerEfficiency trigeff;
    cmg::METSignificance metsig_;
    edm::Wrapper<cmg::METSignificance> metsige_;
    std::vector<cmg::METSignificance> metsigv_;
    edm::Wrapper<std::vector<cmg::METSignificance> > metsigve_;
    HTTRecoilCorrector reccorr_;
  };
}
