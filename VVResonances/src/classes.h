#include "CMGTools/VVResonances/interface/FastJetInterface.h"
#include "CMGTools/VVResonances/interface/CandidateBoostedDoubleSecondaryVertexComputerLight.h"
#include "CMGTools/VVResonances/interface/IPProducerLight.h"
#include "CMGTools/VVResonances/interface/SecondaryVertexProducerLight.h"

namespace cmg{

  struct cmg_vvresonances_dictionary {
    cmg::FastJetInterface fastjetInterface;
    cmg::CandidateBoostedDoubleSecondaryVertexComputerLight candidateBoostedDoubleSecondaryVertexComputerLight;
    cmg::IPProducerLight ipProducerLight;
    cmg::IPProducerLight secondaryVertexProducerLight;
  };
}
