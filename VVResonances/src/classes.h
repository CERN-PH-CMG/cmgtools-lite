#include "CMGTools/VVResonances/interface/FastJetInterface.h"
#include "CMGTools/VVResonances/interface/CandidateBoostedDoubleSecondaryVertexComputerLight.h"

namespace cmg{

  struct cmg_vvresonances_dictionary {
    cmg::FastJetInterface fastjetInterface;
    cmg::CandidateBoostedDoubleSecondaryVertexComputerLight candidateBoostedDoubleSecondaryVertexComputerLight;
  };
}
