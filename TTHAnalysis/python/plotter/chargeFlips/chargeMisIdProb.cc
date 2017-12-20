#include <vector>
#include <iostream>
#include <fstream>
#include <sstream>
#include <stdlib.h>
#include <string>

#include "TFile.h"
#include "TH2F.h"
#include <TMinuit.h>

#include <Math/Functor.h>
#include <Fit/Fitter.h>

using namespace std;

struct binSt{

    binSt() {};
    binSt(vector<float> pt, vector<float> eta) {
        binsPt = pt;
        binsEta = eta;

        nBPt = binsPt.size();
        nBEta = binsEta.size();
    }

    vector<float> binsPt;
    vector<float> binsEta;

    int nBPt;
    int nBEta;

    int getNProb() {return nBPt*nBEta;}
    int getNBPt() {return nBPt;}
    int getNBEta() {return nBEta;}

};

// function Object to be minimized
struct Chi2 {
    vector<std::pair<vector<float>, vector<int> > > _vals;

    void setPoint(float val, float eval, float p1, float p2) {
        vector<float> vals(2,0);
        vector<int> bins(2,0);

        vals[0] = val;
        vals[1] = eval;
        bins[0] = p1;
        bins[1] = p2;

        std::pair<vector<float>, vector<int> > p(vals,bins);
        _vals.push_back(p);
    }

    // implementation of the function to be minimized
    double operator() (const double * param) {
        double chi2 = 0;

        float val,eval;
        int p1,p2;
        for(unsigned int ip = 0;ip<_vals.size();ip++) {
            val = _vals[ip].first[0];
            eval = _vals[ip].first[1];
            p1 = _vals[ip].second[0];
            p2 = _vals[ip].second[1];

            if(eval == 0) eval = val;
            chi2 += pow( val-(param[p1]+param[p2]), 2)/pow(eval,2);
        }
        //cout << " chi2: " << chi2 << endl;
        return chi2;
    }
};

vector<float> parseEquation(string equation) {
    istringstream iss(equation);
    vector<string> tks;
    copy(istream_iterator<string>(iss),
             istream_iterator<string>(),
             back_inserter<vector<string> >(tks));

    int binpt1  = atoi( tks[0].c_str() );
    int bineta1 = atoi( tks[1].c_str() );
    int binpt2  = atoi( tks[2].c_str() );
    int bineta2 = atoi( tks[3].c_str() );
    float ratio    = atof( tks[4].c_str() );
    float ratioerr = atof( tks[5].c_str() );

    vector<float> parsedeq(6,0);
    parsedeq[0] = binpt1;
    parsedeq[1] = bineta1;
    parsedeq[2] = binpt2;
    parsedeq[3] = bineta2;
    parsedeq[4] = ratio;
    parsedeq[5] = ratioerr;

    return parsedeq;
}

binSt setPointsFromEquationsFile(string file, Chi2& chi2) {
    ifstream categs(file.c_str(), ios::in);
    string line;

    vector<float> parsedeq;

    int bPt1, bEta1, bPt2, bEta2;
    int p1, p2;
    float prob, eprob;

    while(getline(categs, line)){
        parsedeq = parseEquation(line);

        bPt1  = parsedeq[0];
        bEta1 = parsedeq[1];
        bPt2  = parsedeq[2];
        bEta2 = parsedeq[3];

        prob = parsedeq[4];
        eprob = parsedeq[5];

        p1 = bPt1*2 + bEta1;
        p2 = bPt2*2 + bEta2;

        chi2.setPoint( prob, eprob, p1, p2);
    }

    vector<float> binsPt;
    binsPt.push_back(10.);
    binsPt.push_back(25.);
    binsPt.push_back(50.);
    vector<float> binsEta;
    binsEta.push_back(0.0);
    binsEta.push_back(1.479);

    binSt binstruct(binsPt, binsEta);
    return binstruct;
}

int main(int argc, char* argv[]) {
    string file;

    char c;
    while( (c = getopt(argc, argv, "f:d:s:D:a:n:h")) != -1 ){
        switch (c) {
        case 'f': { file = string(optarg); break;}
        case 'h': {
            cout << "configuration options:\n "
                 << "-f : equations file to read (root or ASCII) \n "
                 <<"-h help \n" << endl;
            return 0; }
        default : {
            cout << "configuration options:\n "
                 << "-f : file to read (root or ASCII) \n "
                 <<"-h help \n" << endl;
            return 0; }
        }
    }

    //==============================================

    Chi2 chi2;
    binSt bins;
    bins = setPointsFromEquationsFile(file, chi2);


    // perform the final fit ====================
    int nvars = bins.getNProb();

    ROOT::Fit::Fitter  fitter;
    ROOT::Math::Functor fcn(chi2,nvars);

    // bloody ROOT and lack of vector handling
    double* vars = new double[nvars];
    fitter.SetFCN(fcn,vars);

    // set step sizes and limits
    for (int i=0; i<nvars; ++i) {
        fitter.Config().ParSettings(i).SetStepSize(0.000001);
        fitter.Config().ParSettings(i).SetLimits(0,0.2);
    }

    bool ok = fitter.FitFCN();
    if (!ok) {
        cout << "The final fit did not converged properly, "
             << "please check your data and the read/written database " << endl;
        return 1;
    }

    fitter.CalculateMinosErrors();
    fitter.CalculateHessErrors();
    const ROOT::Fit::FitResult & result = fitter.Result();
    result.Print(std::cout);

    const double * parFit = result.GetParams();
    const double * parErrs = result.GetErrors();
    cout << "probabilities (i/ptbin/etabin) and fit result" << endl;
    for(int i=0; i<nvars; i++)
        cout << i << "    "
             << i/bins.nBEta << "   "
             << i%bins.nBEta << " ==> "
             << parFit[i] << " +- " << parErrs[i] << endl;

    size_t start_pos = file.find("equations");
    if(start_pos != std::string::npos){
        file.replace(start_pos, 9, "chMidProb");
    }
    size_t dot = file.find(".dat");
    string tag = file.substr(0, dot);

    string fname = tag+".root";
    TFile* f = new TFile(fname.c_str(),"recreate");
    f->cd();

    // adding the last bin boundaries, bloody root...
    double* binsPt = new double[ bins.nBPt+1 ];
    double* binsEta = new double[ bins.nBEta+1 ];

    for(size_t ib = 0; ib<max( bins.nBPt, bins.nBEta ); ib++) {
        if(ib<bins.nBPt) binsPt[ib] = bins.binsPt[ib];
        if(ib<bins.nBEta) binsEta[ib] = bins.binsEta[ib];
    }
    binsPt[bins.nBPt] = 1000;
    binsEta[bins.nBEta] = 2.5;

    TH2F* h = new TH2F("chargeMisId","chargeMisId;p_{T}(e) [GeV];#eta(e)", bins.nBPt, binsPt, bins.nBEta, binsEta);
    for(int i=0; i<nvars; i++){
        h->SetBinContent((i/bins.nBEta)+1, (i%bins.nBEta)+1, parFit[i]);
        h->SetBinError((i/bins.nBEta)+1, (i%bins.nBEta)+1, parErrs[i]);
    }

    f->Write();
    f->Close();

    std::cout << "Wrote chMidProb histos to " << fname << std::endl;
}
