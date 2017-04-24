#include <TROOT.h>
#include <TFile.h>
#include <TTree.h>
#include <TH2D.h>
#include <iostream>

class HistProvider {
public:
    static HistProvider& instance() {
        static HistProvider instance;
        return instance;
    }

    const TH2D& hist() const {
        return *h_zptmass;
    }

private:
    HistProvider() {
        f_in = new TFile("/afs/cern.ch/work/d/dwinterb/public/MSSM2016/zpt_weights_summer2016.root");
        std::cout << "Creating HistProvider instance in DYReweighting" << std::endl;
        h_zptmass = dynamic_cast<TH2D*>(f_in->Get("zptmass_histo"));
        if (!h_zptmass)
            std::cerr << "ERROR: Not getting histogram out of file in DYReweighting" << std::endl;
    }

    ~HistProvider() {
        delete f_in;
    }

    TFile* f_in;
    TH2D* h_zptmass;
};


double getDYWeight(double genMass, double genpT) {
    const TH2D& h_zptmass = HistProvider::instance().hist();
    double weight = h_zptmass.GetBinContent(h_zptmass.GetXaxis()->FindBin(genMass), h_zptmass.GetYaxis()->FindBin(genpT));
    if (weight == 0.) {
        std::cout << "WARNING: Zero weight in DY reweighting: " << std::endl;
        std::cout << "   DY weight " << weight << std::endl;
        std::cout << "   genMass " << genMass << std::endl;
        std::cout << "   genpT " << genpT << std::endl;
    }
    return weight;
}
