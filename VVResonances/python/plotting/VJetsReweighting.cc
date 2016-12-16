#include <TROOT.h>
#include <TFile.h>
#include <TTree.h>
#include <TF1.h>
#include <iostream>

class HistProvider {
public:
    static HistProvider& instance() {
        static HistProvider instance;
        return instance;
    }

    const TF1& zpt_func() const {
        return *h_zpt;
    }

    const TF1& wpt_func() const {
        return *h_wpt;
    }

private:
    HistProvider() {
        f_in = new TFile("/afs/cern.ch/work/z/zucchett/public/EWK/scalefactors_v4.root");
        std::cout << "Creating HistProvider instance in VJetsReweighting" << std::endl;
        h_zpt = dynamic_cast<TF1*>(f_in->Get("z_ewkcorr/z_ewkcorr_func"));
        h_wpt = dynamic_cast<TF1*>(f_in->Get("w_ewkcorr/w_ewkcorr_func"));
        if (!h_zpt || !h_wpt)
            std::cerr << "ERROR: Not getting histogram out of file in VJetsReweighting" << std::endl;
    }

    ~HistProvider() {
        delete f_in;
    }

    TFile* f_in;
    TF1* h_zpt;
    TF1* h_wpt;
};


double getDYWeight(double genpT) {
    const TF1& h_zpt = HistProvider::instance().zpt_func();
    double weight = h_zpt.Eval(genpT);
    if (weight == 0.) {
        std::cout << "WARNING: Zero weight in DY reweighting: " << std::endl;
        std::cout << "   DY weight " << weight << std::endl;
        std::cout << "   genpT " << genpT << std::endl;
    }
    return weight;
}

double getWWeight(double genpT) {
    const TF1& h_wpt = HistProvider::instance().wpt_func();
    double weight = h_wpt.Eval(genpT);
    if (weight == 0.) {
        std::cout << "WARNING: Zero weight in W reweighting: " << std::endl;
        std::cout << "   W weight " << weight << std::endl;
        std::cout << "   genpT " << genpT << std::endl;
    }
    return weight;
}
