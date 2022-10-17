#include <cmath>
#include <TTreeReaderValue.h>
#include <TTreeReaderArray.h>
#include <DataFormats/Math/interface/deltaR.h>

class JetReCleanerExampleHelper2 {
    public:
        typedef TTreeReaderValue<int>   rint;
        typedef TTreeReaderArray<float> rfloats;
        typedef TTreeReaderArray<int> rints;

        JetReCleanerExampleHelper2() {}

        void setLeptons(rint *nLep, rfloats *lepEta, rfloats *lepPhi) {
            nLepGood_ = nLep; LepGood_eta_ = lepEta; LepGood_phi_ = lepPhi;
        }
        void setJets(rint *nJet, rfloats *jetEta, rfloats *jetPhi) {
            nJet_ = nJet; Jet_eta_ = jetEta; Jet_phi_ = jetPhi;
        }
        const std::vector<int> & run() {
            ret_.clear();
            for (int iJ = 0, nJ = **nJet_; iJ < nJ; ++iJ) {
                bool ok = true;
                for (int iL = 0, nL = **nLepGood_; iL < nL; ++iL) {
                    if (deltaR2((*LepGood_eta_)[iL], (*LepGood_phi_)[iL], (*Jet_eta_)[iJ], (*Jet_phi_)[iJ]) < 0.16) {
                        ok = false;
                        break;
                    }
                }
                if (ok) {
                    ret_.push_back(iJ);
                }
            }
            return ret_;
        }
    private:
        std::vector<int> ret_;
        rint *nLepGood_, *nJet_;
        rfloats *LepGood_eta_, *LepGood_phi_;
        rfloats *Jet_phi_, *Jet_eta_;
};
