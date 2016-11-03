#include "CMGTools/SVfitStandalone/interface/SVfitStandaloneAlgorithm.h"

#include "Math/Factory.h"
#include "Math/Functor.h"
#include "Math/GSLMCIntegrator.h"
#include "Math/LorentzVector.h"
#include "Math/PtEtaPhiM4D.h"

#include <TGraphErrors.h>
#include <TMatrixD.h>
#include <TMatrixDSym.h>
#include <TMatrixDSymEigen.h>
#include <TVectorD.h>

namespace svFitStandalone
{
  TH1* makeHistogram(const std::string& histogramName, double xMin, double xMax, double logBinWidth)
  {
    if(xMin <= 0)
      xMin = 0.1;
    int numBins = 1 + TMath::Log(xMax/xMin)/TMath::Log(logBinWidth);
    TArrayF binning(numBins + 1);
    binning[0] = 0.;
    double x = xMin;  
    for ( int iBin = 1; iBin <= numBins; ++iBin ) {
      binning[iBin] = x;
      x *= logBinWidth;
    }  
    TH1* histogram = new TH1D(histogramName.data(), histogramName.data(), numBins, binning.GetArray());
    return histogram;
  }
  void compHistogramDensity(const TH1* histogram, TH1* histogram_density) 
  {
    for ( int iBin = 1; iBin <= histogram->GetNbinsX(); ++iBin ) {
      double binContent = histogram->GetBinContent(iBin);
      double binError = histogram->GetBinError(iBin);
      double binWidth = histogram->GetBinWidth(iBin);
      //if ( histogram == histogramMass_ ) {
      //  TAxis* xAxis = histogram->GetXaxis();
      //  std::cout << "bin #" << iBin << " (x = " << xAxis->GetBinLowEdge(iBin) << ".." << xAxis->GetBinUpEdge(iBin) << ", width = " << binWidth << "):"
      //        << " " << binContent << " +/- " << binError << std::endl;
      //}
      assert(binWidth > 0.);
      histogram_density->SetBinContent(iBin, binContent/binWidth);
      histogram_density->SetBinError(iBin, binError/binWidth);
    }
  }
  double extractValue(const TH1* histogram, TH1* histogram_density) 
  {
    double maximum, maximum_interpol, mean, quantile016, quantile050, quantile084, mean3sigmaWithinMax, mean5sigmaWithinMax;
    compHistogramDensity(histogram, histogram_density);
    svFitStandalone::extractHistogramProperties(histogram, histogram_density, maximum, maximum_interpol, mean, quantile016, quantile050, quantile084, mean3sigmaWithinMax, mean5sigmaWithinMax);
    //double value = maximum_interpol;
    double value = maximum;
    return value;
  }
  double extractUncertainty(const TH1* histogram, TH1* histogram_density)
  {
    double maximum, maximum_interpol, mean, quantile016, quantile050, quantile084, mean3sigmaWithinMax, mean5sigmaWithinMax;
    compHistogramDensity(histogram, histogram_density);
    svFitStandalone::extractHistogramProperties(histogram, histogram_density, maximum, maximum_interpol, mean, quantile016, quantile050, quantile084, mean3sigmaWithinMax, mean5sigmaWithinMax);
    //double uncertainty = TMath::Sqrt(0.5*(TMath::Power(quantile084 - maximum_interpol, 2.) + TMath::Power(maximum_interpol - quantile016, 2.)));
    double uncertainty = TMath::Sqrt(0.5*(TMath::Power(quantile084 - maximum, 2.) + TMath::Power(maximum - quantile016, 2.)));
    return uncertainty;  
  }
  double extractLmax(const TH1* histogram, TH1* histogram_density)
  {
    compHistogramDensity(histogram, histogram_density);
    double Lmax = histogram_density->GetMaximum();
    return Lmax;
  }

  void map_xVEGAS(const double* x, bool l1isLep, bool l2isLep, bool marginalizeVisMass, bool shiftVisMass, bool shiftVisPt, double mvis, double mtest, double* x_mapped)
  {
    int offset1 = 0;
    if ( l1isLep ) {
      x_mapped[kXFrac]                 = x[0];
      x_mapped[kMNuNu]                 = x[1];
      x_mapped[kPhi]                   = x[2];
      x_mapped[kVisMassShifted]        = 0.;
      x_mapped[kRecTauPtDivGenTauPt]   = 0.;
      offset1 = 3;
    } else {
      x_mapped[kXFrac]                 = x[0];
      x_mapped[kMNuNu]                 = 0.;
      x_mapped[kPhi]                   = x[1];
      offset1 = 2;
      if ( marginalizeVisMass || shiftVisMass ) {
  x_mapped[kVisMassShifted]      = x[offset1];
  ++offset1;
      } else {
  x_mapped[kVisMassShifted]      = 0.;
      }
      if ( shiftVisPt ) {
  x_mapped[kRecTauPtDivGenTauPt] = x[offset1];
  ++offset1;
      } else {
  x_mapped[kRecTauPtDivGenTauPt] = 0.;
      }
    }    
    double x2 = ( x[0] > 0. ) ? TMath::Power(mvis/mtest, 2.)/x[0] : 1.e+3;
    int offset2 = 0;
    if ( l2isLep ) {
      x_mapped[kMaxFitParams + kXFrac]                 = x2;
      x_mapped[kMaxFitParams + kMNuNu]                 = x[offset1 + 0];
      x_mapped[kMaxFitParams + kPhi]                   = x[offset1 + 1];
      x_mapped[kMaxFitParams + kVisMassShifted]        = 0.;
      x_mapped[kMaxFitParams + kRecTauPtDivGenTauPt]   = 0.;
      offset2 = 2;
    } else {
      x_mapped[kMaxFitParams + kXFrac]                 = x2;
      x_mapped[kMaxFitParams + kMNuNu]                 = 0.;
      x_mapped[kMaxFitParams + kPhi]                   = x[offset1 + 0];
      offset2 = 1;
      if ( marginalizeVisMass || shiftVisMass ) {
  x_mapped[kMaxFitParams + kVisMassShifted]      = x[offset1 + offset2];
  ++offset2;
      } else {
  x_mapped[kMaxFitParams + kVisMassShifted]      = 0.;
      }
      if ( shiftVisPt ) {
  x_mapped[kMaxFitParams + kRecTauPtDivGenTauPt] = x[offset1 + offset2];
  ++offset2;
      } else {
  x_mapped[kMaxFitParams + kRecTauPtDivGenTauPt] = 0.;
      }
    }
  }

  void map_xMarkovChain(const double* x, bool l1isLep, bool l2isLep, bool marginalizeVisMass, bool shiftVisMass, bool shiftVisPt, double* x_mapped)
  {
    int offset1 = 0;
    if ( l1isLep ) {
      x_mapped[kXFrac]                 = x[0];
      x_mapped[kMNuNu]                 = x[1];
      x_mapped[kPhi]                   = x[2];
      x_mapped[kVisMassShifted]        = 0.;
      x_mapped[kRecTauPtDivGenTauPt]   = 0.;
      offset1 = 3;
    } else {
      x_mapped[kXFrac]                 = x[0];
      x_mapped[kMNuNu]                 = 0.;
      x_mapped[kPhi]                   = x[1];
      offset1 = 2;
      if ( marginalizeVisMass || shiftVisMass ) {
  x_mapped[kVisMassShifted]      = x[offset1];
  ++offset1;
      } else {
  x_mapped[kVisMassShifted]      = 0.;
      }
      if ( shiftVisPt ) {
  x_mapped[kRecTauPtDivGenTauPt] = x[offset1];
  ++offset1;
      } else {
  x_mapped[kRecTauPtDivGenTauPt] = 0.;
      }
    }
    int offset2 = 0;
    if ( l2isLep ) {
      x_mapped[kMaxFitParams + kXFrac]                 = x[offset1 + 0];
      x_mapped[kMaxFitParams + kMNuNu]                 = x[offset1 + 1];
      x_mapped[kMaxFitParams + kPhi]                   = x[offset1 + 2];
      x_mapped[kMaxFitParams + kVisMassShifted]        = 0.;
      x_mapped[kMaxFitParams + kRecTauPtDivGenTauPt]   = 0.;
      offset2 = 3;
    } else {
      x_mapped[kMaxFitParams + kXFrac]                 = x[offset1 + 0];
      x_mapped[kMaxFitParams + kMNuNu]                 = 0.;
      x_mapped[kMaxFitParams + kPhi]                   = x[offset1 + 1];
      offset2 = 2;
      if ( marginalizeVisMass || shiftVisMass ) {
  x_mapped[kMaxFitParams + kVisMassShifted]      = x[offset1 + offset2];
  ++offset2;
      } else {
  x_mapped[kMaxFitParams + kVisMassShifted]      = 0.;
      }
      if ( shiftVisPt ) { 
  x_mapped[kMaxFitParams + kRecTauPtDivGenTauPt] = x[offset1 + offset2];
  ++offset2;
      } else {
  x_mapped[kMaxFitParams + kRecTauPtDivGenTauPt] = 0.;
      }
    }
    //std::cout << "<map_xMarkovChain>:" << std::endl;
    //for ( int i = 0; i < 6; ++i ) {
    //  std::cout << " x_mapped[" << i << "] = " << x_mapped[i] << std::endl;
    //}
  }

  struct sortMeasuredTauLeptons 
  {
    bool operator() (const svFitStandalone::MeasuredTauLepton& measuredTauLepton1, const svFitStandalone::MeasuredTauLepton& measuredTauLepton2)
    {
      if ( (measuredTauLepton1.type() == svFitStandalone::kTauToElecDecay || measuredTauLepton1.type() == svFitStandalone::kTauToMuDecay) && 
     measuredTauLepton2.type() == svFitStandalone::kTauToHadDecay  ) return true;
      if ( (measuredTauLepton2.type() == svFitStandalone::kTauToElecDecay || measuredTauLepton2.type() == svFitStandalone::kTauToMuDecay) && 
     measuredTauLepton1.type() == svFitStandalone::kTauToHadDecay ) return false;
      return ( measuredTauLepton1.pt() > measuredTauLepton2.pt() );
    }
  };
}

SVfitStandaloneAlgorithm::SVfitStandaloneAlgorithm(const std::vector<svFitStandalone::MeasuredTauLepton>& measuredTauLeptons, double measuredMETx, double measuredMETy, const TMatrixD& covMET, 
               unsigned int verbosity) 
  : fitStatus_(-1), 
    verbosity_(verbosity), 
    maxObjFunctionCalls_(10000),
    standaloneObjectiveFunctionAdapterVEGAS_(0),
    mcObjectiveFunctionAdapter_(0),
    mcPtEtaPhiMassAdapter_(0),
    integrator2_(0),
    integrator2_nDim_(0),
    isInitialized2_(false),
    maxObjFunctionCalls2_(100000),
    marginalizeVisMass_(false),
    lutVisMassAllDMs_(0),
    shiftVisMass_(false),
    lutVisMassResDM0_(0),
    lutVisMassResDM1_(0),
    lutVisMassResDM10_(0),
    shiftVisPt_(false),
    lutVisPtResDM0_(0),
    lutVisPtResDM1_(0),
    lutVisPtResDM10_(0)
{ 
  // instantiate minuit, the arguments might turn into configurables once
  minimizer_ = ROOT::Math::Factory::CreateMinimizer("Minuit2", "Migrad");

  std::vector<svFitStandalone::MeasuredTauLepton> measuredTauLeptons_rounded;
  for ( std::vector<svFitStandalone::MeasuredTauLepton>::const_iterator measuredTauLepton = measuredTauLeptons.begin();
  measuredTauLepton != measuredTauLeptons.end(); ++measuredTauLepton ) {
    svFitStandalone::MeasuredTauLepton measuredTauLepton_rounded(
      measuredTauLepton->type(), 
      svFitStandalone::roundToNdigits(measuredTauLepton->pt()), 
      svFitStandalone::roundToNdigits(measuredTauLepton->eta()), 
      svFitStandalone::roundToNdigits(measuredTauLepton->phi()), 
      svFitStandalone::roundToNdigits(measuredTauLepton->mass()), 
      measuredTauLepton->decayMode());
    measuredTauLeptons_rounded.push_back(measuredTauLepton_rounded);
  }
  // for the VEGAS integration the order of MeasuredTauLeptons matters,
  // due to the choice of order in which the integration boundaries are defined.
  // The leptonic tau decay should go before the hadronic tau decays.
  // In case both taus decay to leptons or both taus decay hadronically,
  // the higher pT tau should go before the lower pT tau.
  std::sort(measuredTauLeptons_rounded.begin(), measuredTauLeptons_rounded.end(), svFitStandalone::sortMeasuredTauLeptons());
  if ( verbosity_ >= 1 ) {
    for ( size_t idx = 0; idx < measuredTauLeptons_rounded.size(); ++idx ) {
      const svFitStandalone::MeasuredTauLepton& measuredTauLepton = measuredTauLeptons_rounded[idx];
      std::cout << "measuredTauLepton #" << idx << " (type = " << measuredTauLepton.type() << "): Pt = " << measuredTauLepton.pt() << "," 
    << " eta = " << measuredTauLepton.eta() << " (theta = " << measuredTauLepton.p4().theta() << ")" << ", phi = " << measuredTauLepton.phi() << "," 
    << " mass = " << measuredTauLepton.mass() << std::endl;
    }
  }
  double measuredMETx_rounded = svFitStandalone::roundToNdigits(measuredMETx);
  double measuredMETy_rounded = svFitStandalone::roundToNdigits(measuredMETy);
  svFitStandalone::Vector measuredMET_rounded(measuredMETx_rounded, measuredMETy_rounded, 0.);
  TMatrixD covMET_rounded(2,2);
  covMET_rounded[0][0] = svFitStandalone::roundToNdigits(covMET[0][0]);
  covMET_rounded[1][0] = svFitStandalone::roundToNdigits(covMET[1][0]);
  covMET_rounded[0][1] = svFitStandalone::roundToNdigits(covMET[0][1]);
  covMET_rounded[1][1] = svFitStandalone::roundToNdigits(covMET[1][1]);
  if ( verbosity_ >= 1 ) {
    std::cout << "MET: Px = " << measuredMETx_rounded << ", Py = " << measuredMETy_rounded << std::endl;
    std::cout << "covMET:" << std::endl;
    covMET_rounded.Print();
    TMatrixDSym covMET_sym(2);
    covMET_sym(0,0) = covMET_rounded[0][0];
    covMET_sym(0,1) = covMET_rounded[0][1];
    covMET_sym(1,0) = covMET_rounded[1][0];
    covMET_sym(1,1) = covMET_rounded[1][1];
    TMatrixD EigenVectors(2,2);
    EigenVectors = TMatrixDSymEigen(covMET_sym).GetEigenVectors();
    std::cout << "Eigenvectors =  { " << EigenVectors(0,0) << ", " << EigenVectors(1,0) << " (phi = " << TMath::ATan2(EigenVectors(1,0), EigenVectors(0,0)) << ") },"
        << " { " << EigenVectors(0,1) << ", " << EigenVectors(1,1) << " (phi = " << TMath::ATan2(EigenVectors(1,1), EigenVectors(0,1)) << ") }" << std::endl;
    TVectorD EigenValues(2);  
    EigenValues = TMatrixDSymEigen(covMET_sym).GetEigenValues();
    EigenValues(0) = TMath::Sqrt(EigenValues(0));
    EigenValues(1) = TMath::Sqrt(EigenValues(1));
    std::cout << "Eigenvalues = " << EigenValues(0) << ", " << EigenValues(1) << std::endl;
  }
  
  // instantiate the combined likelihood
  nll_ = new svFitStandalone::SVfitStandaloneLikelihood(measuredTauLeptons_rounded, measuredMET_rounded, covMET_rounded, (verbosity_ >= 2));
  nllStatus_ = nll_->error();

  standaloneObjectiveFunctionAdapterVEGAS_ = new svFitStandalone::ObjectiveFunctionAdapterVEGAS();
  
  clock_ = new TBenchmark();
}

SVfitStandaloneAlgorithm::~SVfitStandaloneAlgorithm() 
{
  delete nll_;
  delete minimizer_;
  delete standaloneObjectiveFunctionAdapterVEGAS_;
  delete mcObjectiveFunctionAdapter_;
  delete mcPtEtaPhiMassAdapter_;
  delete integrator2_;
  //delete lutVisMassAllDMs_;
  //delete lutVisMassResDM0_;
  //delete lutVisMassResDM1_;
  //delete lutVisMassResDM10_;
  //delete lutVisPtResDM0_;
  //delete lutVisPtResDM1_;
  //delete lutVisPtResDM10_;

  delete clock_;
}

namespace
{
  TH1* readHistogram(TFile* inputFile, const std::string& histogramName)
  {
    TH1* histogram = dynamic_cast<TH1*>(inputFile->Get(histogramName.data()));
    if ( !histogram ) {
      std::cerr << "<readHistogram>: Failed to load histogram = " << histogramName << " from file = " << inputFile->GetName() << " !!" << std::endl;
      assert(0);
    }
    return histogram;
  }
}

void 
SVfitStandaloneAlgorithm::marginalizeVisMass(bool value, TFile* inputFile)
{
  marginalizeVisMass_ = value;
  if ( marginalizeVisMass_ ) {
    delete lutVisMassAllDMs_;
    TH1* lutVisMassAllDMs_tmp = readHistogram(inputFile, "DQMData/genTauMassAnalyzer/genTauJetMass");
    if ( lutVisMassAllDMs_tmp->GetNbinsX() >= 1000 ) lutVisMassAllDMs_tmp->Rebin(100);
    lutVisMassAllDMs_ = lutVisMassAllDMs_tmp;
  }
}

void 
SVfitStandaloneAlgorithm::marginalizeVisMass(bool value, const TH1* lut)
{
  marginalizeVisMass_ = value;
  if ( marginalizeVisMass_ ) {
    lutVisMassAllDMs_ = lut;
  }
}

void 
SVfitStandaloneAlgorithm::shiftVisMass(bool value, TFile* inputFile)
{
  shiftVisMass_ = value;
  if ( shiftVisMass_ ) {
    delete lutVisMassResDM0_;
    lutVisMassResDM0_ = readHistogram(inputFile, "recMinusGenTauMass_recDecayModeEq0");
    delete lutVisMassResDM1_;
    lutVisMassResDM1_ = readHistogram(inputFile, "recMinusGenTauMass_recDecayModeEq1");
    delete lutVisMassResDM10_;
    lutVisMassResDM10_ = readHistogram(inputFile, "recMinusGenTauMass_recDecayModeEq10");
  }
}

void 
SVfitStandaloneAlgorithm::shiftVisPt(bool value, TFile* inputFile)
{
  shiftVisPt_ = value;
  if ( shiftVisPt_ ) {
    delete lutVisPtResDM0_;
    lutVisPtResDM0_ = readHistogram(inputFile, "recTauPtDivGenTauPt_recDecayModeEq0");
    delete lutVisPtResDM1_;
    lutVisPtResDM1_ = readHistogram(inputFile, "recTauPtDivGenTauPt_recDecayModeEq1");
    delete lutVisPtResDM10_;
    lutVisPtResDM10_ = readHistogram(inputFile, "recTauPtDivGenTauPt_recDecayModeEq10");
  }
}

void
SVfitStandaloneAlgorithm::setup()
{
  using namespace svFitStandalone;

  //if ( verbosity_ >= 1 ) {
  //  std::cout << "<SVfitStandaloneAlgorithm::setup()>:" << std::endl;
  //}
  for ( size_t idx = 0; idx < nll_->measuredTauLeptons().size(); ++idx ) {
    const MeasuredTauLepton& measuredTauLepton = nll_->measuredTauLeptons()[idx];
    //if ( verbosity_ >= 1 ) {
    //  std::cout << " --> upper limit of leg1::mNuNu will be set to "; 
    //  if ( measuredTauLepton.type() == kTauToHadDecay ) { 
    //    std::cout << "0";
    //  } else {
    //    std::cout << (svFitStandalone::tauLeptonMass - TMath::Min(measuredTauLepton.mass(), 1.5));
    //  } 
    //  std::cout << std::endl;
    //}
    // start values for xFrac
    minimizer_->SetLimitedVariable(
      idx*kMaxFitParams + kXFrac, 
      std::string(TString::Format("leg%i::xFrac", (int)idx + 1)).c_str(), 
      0.5, 0.1, 0., 1.);
    // start values for nunuMass (leptonic tau decays only)
    if ( measuredTauLepton.type() == kTauToHadDecay ) { 
      minimizer_->SetFixedVariable(
        idx*kMaxFitParams + kMNuNu, 
  std::string(TString::Format("leg%i::mNuNu", (int)idx + 1)).c_str(), 
  0.); 
    } else { 
      minimizer_->SetLimitedVariable(
        idx*kMaxFitParams + kMNuNu, 
  std::string(TString::Format("leg%i::mNuNu", (int)idx + 1)).c_str(), 
  0.8, 0.10, 0., svFitStandalone::tauLeptonMass - TMath::Min(measuredTauLepton.mass(), 1.5)); 
    }
    // start values for phi
    minimizer_->SetVariable(
      idx*kMaxFitParams + kPhi, 
      std::string(TString::Format("leg%i::phi", (int)idx + 1)).c_str(), 
      0.0, 0.25);
    // start values for Pt and mass of visible tau decay products (hadronic tau decays only)
    if ( measuredTauLepton.type() == kTauToHadDecay && (marginalizeVisMass_ || shiftVisMass_) ) {
      minimizer_->SetLimitedVariable(
        idx*kMaxFitParams + kVisMassShifted, 
        std::string(TString::Format("leg%i::mVisShift", (int)idx + 1)).c_str(), 
        0.8, 0.10, svFitStandalone::chargedPionMass, svFitStandalone::tauLeptonMass);
    } else {
      minimizer_->SetFixedVariable(
        idx*kMaxFitParams + kVisMassShifted, 
        std::string(TString::Format("leg%i::mVisShift", (int)idx + 1)).c_str(), 
        measuredTauLepton.mass());
    }
    if ( measuredTauLepton.type() == kTauToHadDecay && shiftVisPt_ ) {
      minimizer_->SetLimitedVariable(
        idx*kMaxFitParams + kRecTauPtDivGenTauPt, 
        std::string(TString::Format("leg%i::tauPtDivGenVisPt", (int)idx + 1)).c_str(), 
        0., 0.10, -1., +1.5);
    } else {     
      minimizer_->SetFixedVariable(
        idx*kMaxFitParams + kRecTauPtDivGenTauPt, 
        std::string(TString::Format("leg%i::tauPtDivGenVisPt", (int)idx + 1)).c_str(), 
        0.);
    }
  }
}

void
SVfitStandaloneAlgorithm::fit()
{
  if ( verbosity_ >= 1 ) {
    std::cout << "<SVfitStandaloneAlgorithm::fit>:" << std::endl;
  }

  // clear minimizer
  minimizer_->Clear();

  // set verbosity level of minimizer
  minimizer_->SetPrintLevel(-1);

  // setup the function to be called and the dimension of the fit
  ROOT::Math::Functor toMinimize(standaloneObjectiveFunctionAdapterMINUIT_, nll_->measuredTauLeptons().size()*svFitStandalone::kMaxFitParams);
  minimizer_->SetFunction(toMinimize); 
  setup();
  minimizer_->SetMaxFunctionCalls(maxObjFunctionCalls_);

  // set Minuit strategy = 2, in order to get reliable error estimates:
  // http://www-cdf.fnal.gov/physics/statistics/recommendations/minuit.html
  minimizer_->SetStrategy(2);

  // compute uncertainties for increase of objective function by 0.5 wrt. 
  // minimum (objective function is log-likelihood function)
  minimizer_->SetErrorDef(0.5);

  // do the minimization
  nll_->addDelta(false);
  nll_->addSinTheta(true);
  nll_->requirePhysicalSolution(false);
  minimizer_->Minimize();

  /* get Minimizer status code, check if solution is valid:
    
     0: Valid solution
     1: Covariance matrix was made positive definite
     2: Hesse matrix is invalid
     3: Estimated distance to minimum (EDM) is above maximum
     4: Reached maximum number of function calls before reaching convergence
     5: Any other failure
  */
  fitStatus_ = minimizer_->Status();
  
  // and write out the result
  using svFitStandalone::kXFrac;
  using svFitStandalone::kMNuNu;
  using svFitStandalone::kPhi;
  using svFitStandalone::kMaxFitParams;
  // update di-tau system with final fit results
  nll_->results(fittedTauLeptons_, minimizer_->X());
  // determine uncertainty of the fitted di-tau mass
  double x1RelErr = minimizer_->Errors()[kXFrac]/minimizer_->X()[kXFrac];
  double x2RelErr = minimizer_->Errors()[kMaxFitParams + kXFrac]/minimizer_->X()[kMaxFitParams + kXFrac];
  // this gives a unified treatment for retrieving the result for integration mode and fit mode
  fittedDiTauSystem_ = fittedTauLeptons_[0] + fittedTauLeptons_[1];
  mass_ = fittedDiTauSystem().mass();
  massUncert_ = TMath::Sqrt(0.25*x1RelErr*x1RelErr + 0.25*x2RelErr*x2RelErr)*fittedDiTauSystem().mass();
}

void
SVfitStandaloneAlgorithm::integrateVEGAS(const std::string& likelihoodFileName)
{
  using namespace svFitStandalone;
  
  if ( verbosity_ >= 1 ) {
    std::cout << "<SVfitStandaloneAlgorithm::integrateVEGAS>:" << std::endl;
    clock_->Start("<SVfitStandaloneAlgorithm::integrateVEGAS>");
  }

  // number of parameters for fit
  int nDim = 0;
  l1isLep_ = false;
  l2isLep_ = false;
  const TH1* l1lutVisMass = 0;
  const TH1* l1lutVisMassRes = 0;
  const TH1* l1lutVisPtRes = 0;
  const TH1* l2lutVisMass = 0;
  const TH1* l2lutVisMassRes = 0;
  const TH1* l2lutVisPtRes = 0;
  for ( size_t idx = 0; idx < nll_->measuredTauLeptons().size(); ++idx ) {
    const MeasuredTauLepton& measuredTauLepton = nll_->measuredTauLeptons()[idx];
    if ( idx == 0 ) {
      idxFitParLeg1_ = 0;
      if ( measuredTauLepton.type() == kTauToHadDecay ) { 
  if ( marginalizeVisMass_ ) {
    l1lutVisMass = lutVisMassAllDMs_;
  } 
  if ( shiftVisMass_ ) {
    if ( measuredTauLepton.decayMode() == 0 ) {
      l1lutVisMassRes = lutVisMassResDM0_;
    } else if ( measuredTauLepton.decayMode() == 1 || measuredTauLepton.decayMode() == 2 ) {
      l1lutVisMassRes = lutVisMassResDM1_;
    } else if ( measuredTauLepton.decayMode() == 10 ) {
      l1lutVisMassRes = lutVisMassResDM10_;
    //} else {
    //  std::cerr << "Warning: shiftVisMass is enabled, but leg1 decay mode = " << measuredTauLepton.decayMode() << " is not supported" 
    //          << " --> disabling shiftVisMass for this event !!" << std::endl;
    }
        }
  if ( shiftVisPt_ ) {
    if ( measuredTauLepton.decayMode() == 0 ) {
      l1lutVisPtRes = lutVisPtResDM0_;
    } else if ( measuredTauLepton.decayMode() == 1 || measuredTauLepton.decayMode() == 2 ) {
      l1lutVisPtRes = lutVisPtResDM1_;
    } else if ( measuredTauLepton.decayMode() == 10 ) {
      l1lutVisPtRes = lutVisPtResDM10_;
    //} else {
    //  std::cerr << "Warning: shiftVisPt is enabled, but leg1 decay mode = " << measuredTauLepton.decayMode() << " is not supported" 
    //          << " --> disabling shiftVisPt for this event !!" << std::endl;
    }
        }
  nDim += 2;
  if ( l1lutVisMass || l1lutVisMassRes ) {
    ++nDim;
  }
  if ( l1lutVisPtRes ) {
    ++nDim;
  }
      } else {
  l1isLep_ = true;
  nDim += 3;
      }
    }
    if ( idx == 1 ) {
      idxFitParLeg2_ = nDim;
      if ( measuredTauLepton.type() == kTauToHadDecay ) { 
  if ( marginalizeVisMass_ ) {
    l2lutVisMass = lutVisMassAllDMs_;
  } 
  if ( shiftVisMass_ ) {
    if ( measuredTauLepton.decayMode() == 0 ) {
      l2lutVisMassRes = lutVisMassResDM0_;
    } else if ( measuredTauLepton.decayMode() == 1 || measuredTauLepton.decayMode() == 2 ) {
      l2lutVisMassRes = lutVisMassResDM1_;
    } else if ( measuredTauLepton.decayMode() == 10 ) {
      l2lutVisMassRes = lutVisMassResDM10_;
    //} else {
    //  std::cerr << "Warning: shiftVisMass is enabled, but leg2 decay mode = " << measuredTauLepton.decayMode() << " is not supported" 
    //            << " --> disabling shiftVisMass for this event !!" << std::endl;
    }
  }
  if ( shiftVisPt_ ) {
    if ( measuredTauLepton.decayMode() == 0 ) {
      l2lutVisPtRes = lutVisPtResDM0_;
    } else if ( measuredTauLepton.decayMode() == 1 || measuredTauLepton.decayMode() == 2 ) {
      l2lutVisPtRes = lutVisPtResDM1_;
    } else if ( measuredTauLepton.decayMode() == 10 ) {
      l2lutVisPtRes = lutVisPtResDM10_;
    //} else {
    //  std::cerr << "Warning: shiftVisPt is enabled, but leg2 decay mode = " << measuredTauLepton.decayMode() << " is not supported" 
    //          << " --> disabling shiftVisPt for this event !!" << std::endl;
    }
  }
  nDim += 2;
  if ( l2lutVisMass || l2lutVisMassRes ) {
    ++nDim;
  }
  if ( l2lutVisPtRes ) {
    ++nDim;
  }
      } else {
  l2isLep_ = true;
  nDim += 3;
      }
    }
  }
  nDim -= 1; // xFrac for second tau is fixed by delta function for test mass

  /* --------------------------------------------------------------------------------------
     lower and upper bounds for integration. Boundaries are defined for each decay channel
     separately. The order is: 
     
     - fully hadronic {xFrac, phihad1, (masshad1, pthad1), phihad2, (masshad2, pthad2)}
     - semi  leptonic {xFrac, nunuMass, philep, phihad, (masshad, pthad)}
     - fully leptonic {xFrac, nunuMass1, philep1, nunuMass2, philep2}
     
     x0* defines the start value for the integration, xl* defines the lower integation bound, 
     xh* defines the upper integration bound in the following definitions. 
     ATTENTION: order matters here! In the semi-leptonic decay the lepton must go first in 
     the parametrization, as it is first in the definition of integral boundaries. This is
     the reason why the measuredLeptons are eventually re-ordered in the constructor of 
     this class before passing them on to SVfitStandaloneLikelihood.
  */
  double* x0 = new double[nDim];
  double* xl = new double[nDim];
  double* xh = new double[nDim];
  if ( l1isLep_ ) {
    x0[idxFitParLeg1_ + 0] = 0.5; 
    xl[idxFitParLeg1_ + 0] = 0.0; 
    xh[idxFitParLeg1_ + 0] = 1.0; 
    x0[idxFitParLeg1_ + 1] = 0.8; 
    xl[idxFitParLeg1_ + 1] = 0.0; 
    xh[idxFitParLeg1_ + 1] = svFitStandalone::tauLeptonMass; 
    x0[idxFitParLeg1_ + 2] = 0.0; 
    xl[idxFitParLeg1_ + 2] = -TMath::Pi(); 
    xh[idxFitParLeg1_ + 2] = +TMath::Pi();
  } else {
    x0[idxFitParLeg1_ + 0] = 0.5; 
    xl[idxFitParLeg1_ + 0] = 0.0; 
    xh[idxFitParLeg1_ + 0] = 1.0; 
    x0[idxFitParLeg1_ + 1] = 0.0; 
    xl[idxFitParLeg1_ + 1] = -TMath::Pi(); 
    xh[idxFitParLeg1_ + 1] = +TMath::Pi();
    int offset1 = 2;
    if ( (marginalizeVisMass_ && l1lutVisMass) || (shiftVisMass_ && l1lutVisMassRes) ) {
      x0[idxFitParLeg1_ + offset1] = nll_->measuredTauLeptons()[0].mass();
      xl[idxFitParLeg1_ + offset1] = svFitStandalone::chargedPionMass; 
      xh[idxFitParLeg1_ + offset1] = svFitStandalone::tauLeptonMass; 
      ++offset1;
    }
    if ( shiftVisPt_ && l1lutVisPtRes ) {
      x0[idxFitParLeg1_ + offset1] = 0.0; 
      xl[idxFitParLeg1_ + offset1] = -1.0; 
      xh[idxFitParLeg1_ + offset1] = +1.5;
      ++offset1;
    }
  }
  if ( l2isLep_ ) {
    x0[idxFitParLeg2_ + 0] = 0.8; 
    xl[idxFitParLeg2_ + 0] = 0.0; 
    xh[idxFitParLeg2_ + 0] = svFitStandalone::tauLeptonMass; 
    x0[idxFitParLeg2_ + 1] = 0.0; 
    xl[idxFitParLeg2_ + 1] = -TMath::Pi(); 
    xh[idxFitParLeg2_ + 1] = +TMath::Pi();
  } else {
    x0[idxFitParLeg2_ + 0] = 0.0; 
    xl[idxFitParLeg2_ + 0] = -TMath::Pi(); 
    xh[idxFitParLeg2_ + 0] = +TMath::Pi();
    int offset2 = 1;
    if ( (marginalizeVisMass_ && l2lutVisMass) || (shiftVisMass_ && l2lutVisMassRes) ) {
      x0[idxFitParLeg2_ + offset2] = nll_->measuredTauLeptons()[1].mass(); 
      xl[idxFitParLeg2_ + offset2] = svFitStandalone::chargedPionMass; 
      xh[idxFitParLeg2_ + offset2] = svFitStandalone::tauLeptonMass; 
      ++offset2;
    }
    if ( shiftVisPt_ && l2lutVisPtRes ) {
      x0[idxFitParLeg2_ + offset2] = 0.0; 
      xl[idxFitParLeg2_ + offset2] = -1.0; 
      xh[idxFitParLeg2_ + offset2] = +1.5;
      ++offset2;
    }
  }
  if ( verbosity_ >= 1 ) {
    for ( int iDim = 0; iDim < nDim; ++iDim ) {
      std::cout << "x0[" << iDim << "] = " << x0[iDim] << " (xl = " << xl[iDim] << ", xh = " << xh[iDim] << ")" << std::endl;
    }
  }

  double minMass = measuredDiTauSystem().mass()/1.0125;
  double maxMass = TMath::Max(1.e+4, 1.e+1*minMass);
  TH1* histogramMass = makeHistogram("SVfitStandaloneAlgorithmVEGAS_histogramMass", minMass, maxMass, 1.025);
  TH1* histogramMass_density = (TH1*)histogramMass->Clone(Form("%s_density", histogramMass->GetName()));

  std::vector<double> xGraph;
  std::vector<double> xErrGraph;
  std::vector<double> yGraph;
  std::vector<double> yErrGraph;

  // integrator instance
  ROOT::Math::GSLMCIntegrator ig2("vegas", 0., 1.e-6, 10000);
  //ROOT::Math::GSLMCIntegrator ig2("vegas", 0., 1.e-6, 2000);
  ROOT::Math::Functor toIntegrate(standaloneObjectiveFunctionAdapterVEGAS_, &ObjectiveFunctionAdapterVEGAS::Eval, nDim); 
  standaloneObjectiveFunctionAdapterVEGAS_->SetL1isLep(l1isLep_);
  standaloneObjectiveFunctionAdapterVEGAS_->SetL2isLep(l2isLep_);
  if ( marginalizeVisMass_ && shiftVisMass_ ) {
    std::cerr << "Error: marginalizeVisMass and shiftVisMass flags must not both be enabled !!" << std::endl;
    assert(0);
  }
  standaloneObjectiveFunctionAdapterVEGAS_->SetMarginalizeVisMass(marginalizeVisMass_ && (l1lutVisMass || l2lutVisMass));
  standaloneObjectiveFunctionAdapterVEGAS_->SetShiftVisMass(shiftVisMass_ && (l1lutVisMassRes || l2lutVisMassRes));
  standaloneObjectiveFunctionAdapterVEGAS_->SetShiftVisPt(shiftVisPt_ && (l1lutVisPtRes || l2lutVisPtRes));
  ig2.SetFunction(toIntegrate);
  nll_->addDelta(true);
  nll_->addSinTheta(false);
  nll_->addPhiPenalty(false);
  nll_->marginalizeVisMass(marginalizeVisMass_ && (l1lutVisMass || l2lutVisMass), l1lutVisMass, l2lutVisMass);
  nll_->shiftVisMass(shiftVisMass_ && (l1lutVisMassRes || l2lutVisMassRes), l1lutVisMassRes, l2lutVisMassRes);
  nll_->shiftVisPt(shiftVisPt_ && (l1lutVisPtRes || l2lutVisPtRes), l1lutVisPtRes, l2lutVisPtRes);
  nll_->requirePhysicalSolution(true);
  int count = 0;
  double pMax = 0.;
  double mvis = measuredDiTauSystem().mass();
  double mtest = mvis*1.0125;
  bool skiphighmasstail = false;
  for ( int i = 0; i < 100 && (!skiphighmasstail); ++i ) {
  //-----------------------------------------------------------------------------
  // !!! ONLY FOR TESTING
  //for ( int i = 0; i < 1 && (!skiphighmasstail); ++i ) {
  //  mtest = 3200.; 
  //     FOR TESTING ONLY !!!
  //-----------------------------------------------------------------------------
    standaloneObjectiveFunctionAdapterVEGAS_->SetMvis(mvis);
    standaloneObjectiveFunctionAdapterVEGAS_->SetMtest(mtest);
    double p = ig2.Integral(xl, xh);
    double pErr = ig2.Error();
    if ( verbosity_ >= 2 ) {
      std::cout << "--> scan idx = " << i << ": mtest = " << mtest << ", p = " << p << " +/- " << pErr << " (pMax = " << pMax << ")" << std::endl;
    }    
    if ( p > pMax ) {
      mass_ = mtest;
      pMax  = p;
      count = 0;
    } else {
      if ( p < (1.e-3*pMax) ) {
  ++count;
  if ( count>= 5 ) {
    skiphighmasstail = true;
  }
      } else {
  count = 0;
      }
    }
    double mtest_step = 0.025*mtest;
    int bin = histogramMass->FindBin(mtest);
    histogramMass->SetBinContent(bin, p*mtest_step);
    histogramMass->SetBinError(bin, pErr*mtest_step);
    xGraph.push_back(mtest);
    xErrGraph.push_back(0.5*mtest_step);
    yGraph.push_back(p);
    yErrGraph.push_back(pErr);
    mtest += mtest_step;
  }
  //mass_ = extractValue(histogramMass, histogramMass_density);
  massUncert_ = extractUncertainty(histogramMass, histogramMass_density);
  massLmax_ = extractLmax(histogramMass, histogramMass_density);
  fitStatus_ = ( massLmax_ > 0. ) ? 0 : 1;
  if ( verbosity_ >= 1 ) {
    std::cout << "--> mass  = " << mass_  << " +/- " << massUncert_ << std::endl;
    std::cout << "   (pMax = " << pMax << ", count = " << count << ")" << std::endl;
  }
  delete histogramMass;
  delete histogramMass_density;
  if ( likelihoodFileName != "" ) {
    size_t numPoints = xGraph.size();
    TGraphErrors* likelihoodGraph = new TGraphErrors(numPoints);
    likelihoodGraph->SetName("svFitLikelihoodGraph");
    for ( size_t iPoint = 0; iPoint < numPoints; ++iPoint ) {
      likelihoodGraph->SetPoint(iPoint, xGraph[iPoint], yGraph[iPoint]);
      likelihoodGraph->SetPointError(iPoint, xErrGraph[iPoint], yErrGraph[iPoint]);
    }
    TFile* likelihoodFile = new TFile(likelihoodFileName.data(), "RECREATE");
    likelihoodGraph->Write();
    delete likelihoodFile;
    delete likelihoodGraph;
  }

  delete[] x0;
  delete[] xl;
  delete[] xh;

  if ( verbosity_ >= 1 ) {
    clock_->Show("<SVfitStandaloneAlgorithm::integrateVEGAS>");
  }
}

void
SVfitStandaloneAlgorithm::integrateMarkovChain(const std::string& likelihoodFileName)
{
  using namespace svFitStandalone;
  
  if ( verbosity_ >= 1 ) {
    std::cout << "<SVfitStandaloneAlgorithm::integrateMarkovChain>:" << std::endl;
    clock_->Start("<SVfitStandaloneAlgorithm::integrateMarkovChain>");
  }
  if ( isInitialized2_ ) {
    mcPtEtaPhiMassAdapter_->Reset();
  } else {
    // initialize    
    std::string initMode = "none";
    unsigned numIterBurnin = TMath::Nint(0.10*maxObjFunctionCalls2_);
    unsigned numIterSampling = maxObjFunctionCalls2_;
    unsigned numIterSimAnnealingPhase1 = TMath::Nint(0.02*maxObjFunctionCalls2_);
    unsigned numIterSimAnnealingPhase2 = TMath::Nint(0.06*maxObjFunctionCalls2_);
    double T0 = 15.;
    double alpha = 1.0 - 1.e+2/maxObjFunctionCalls2_;
    unsigned numChains = 7;
    unsigned numBatches = 1;
    unsigned L = 1;
    double epsilon0 = 1.e-2;
    double nu = 0.71;
    int verbosity = -1;
    integrator2_ = new SVfitStandaloneMarkovChainIntegrator(
                         initMode, numIterBurnin, numIterSampling, numIterSimAnnealingPhase1, numIterSimAnnealingPhase2,
       T0, alpha, numChains, numBatches, L, epsilon0, nu,
       verbosity);
    mcObjectiveFunctionAdapter_ = new MCObjectiveFunctionAdapter();
    integrator2_->setIntegrand(*mcObjectiveFunctionAdapter_);
    integrator2_nDim_ = 0;
    mcPtEtaPhiMassAdapter_ = new MCPtEtaPhiMassAdapter();
    integrator2_->registerCallBackFunction(*mcPtEtaPhiMassAdapter_);
    isInitialized2_ = true;    
  }

  // number of parameters for fit
  int nDim = 0;
  l1isLep_ = false;
  l2isLep_ = false;
  const TH1* l1lutVisMass = 0;
  const TH1* l1lutVisMassRes = 0;
  const TH1* l1lutVisPtRes = 0;
  const TH1* l2lutVisMass = 0;
  const TH1* l2lutVisMassRes = 0;
  const TH1* l2lutVisPtRes = 0;
  for ( size_t idx = 0; idx < nll_->measuredTauLeptons().size(); ++idx ) {
    const MeasuredTauLepton& measuredTauLepton = nll_->measuredTauLeptons()[idx];
    if ( idx == 0 ) {
      idxFitParLeg1_ = 0;
      if ( measuredTauLepton.type() == kTauToHadDecay ) { 
  if ( marginalizeVisMass_ ) {
    l1lutVisMass = lutVisMassAllDMs_;
  }
  if ( shiftVisMass_ ) {
    if ( measuredTauLepton.decayMode() == 0 ) {
      l1lutVisMassRes = lutVisMassResDM0_;
    } else if ( measuredTauLepton.decayMode() == 1 || measuredTauLepton.decayMode() == 2 ) {
      l1lutVisMassRes = lutVisMassResDM1_;
    } else if ( measuredTauLepton.decayMode() == 10 ) {
      l1lutVisMassRes = lutVisMassResDM10_;
    //} else {
    //  std::cerr << "Warning: shiftVisMass is enabled, but leg1 decay mode = " << measuredTauLepton.decayMode() << " is not supported" 
    //          << " --> disabling shiftVisMass for this event !!" << std::endl;
    }
        }
  if ( shiftVisPt_ ) {
    if ( measuredTauLepton.decayMode() == 0 ) {
      l1lutVisPtRes = lutVisPtResDM0_;
    } else if ( measuredTauLepton.decayMode() == 1 || measuredTauLepton.decayMode() == 2 ) {
      l1lutVisPtRes = lutVisPtResDM1_;
    } else if ( measuredTauLepton.decayMode() == 10 ) {
      l1lutVisPtRes = lutVisPtResDM10_;
    //} else {
    //  std::cerr << "Warning: shiftVisPt is enabled, but leg1 decay mode = " << measuredTauLepton.decayMode() << " is not supported" 
    //          << " --> disabling shiftVisPt for this event !!" << std::endl;
    }
        }
  nDim += 2;
  if ( l1lutVisMass || l1lutVisMassRes ) {
    ++nDim;
  }
  if ( l1lutVisPtRes ) {
    ++nDim;
  }
      } else {
  l1isLep_ = true;
  nDim += 3;
      }
    }
    if ( idx == 1 ) {
      idxFitParLeg2_ = nDim;
      if ( measuredTauLepton.type() == kTauToHadDecay ) { 
  if ( marginalizeVisMass_ ) {
    l2lutVisMass = lutVisMassAllDMs_;
  }
  if ( shiftVisMass_ ) {
    if ( measuredTauLepton.decayMode() == 0 ) {
      l2lutVisMassRes = lutVisMassResDM0_;
    } else if ( measuredTauLepton.decayMode() == 1 || measuredTauLepton.decayMode() == 2 ) {
      l2lutVisMassRes = lutVisMassResDM1_;
    } else if ( measuredTauLepton.decayMode() == 10 ) {
      l2lutVisMassRes = lutVisMassResDM10_;
    //} else {
    //  std::cerr << "Warning: shiftVisMass is enabled, but leg2 decay mode = " << measuredTauLepton.decayMode() << " is not supported" 
    //          << " --> disabling shiftVisMass for this event !!" << std::endl;
    }
        }
  if ( shiftVisPt_ ) {
    if ( measuredTauLepton.decayMode() == 0 ) {
      l2lutVisPtRes = lutVisPtResDM0_;
    } else if ( measuredTauLepton.decayMode() == 1 || measuredTauLepton.decayMode() == 2 ) {
      l2lutVisPtRes = lutVisPtResDM1_;
    } else if ( measuredTauLepton.decayMode() == 10 ) {
      l2lutVisPtRes = lutVisPtResDM10_;
    //} else {
    //  std::cerr << "Warning: shiftVisPt is enabled, but leg2 decay mode = " << measuredTauLepton.decayMode() << " is not supported" 
    //          << " --> disabling shiftVisPt for this event !!" << std::endl;
    }
        }
  nDim += 2;
  if ( l2lutVisMass || l2lutVisMassRes ) {
    ++nDim;
  }
  if ( l2lutVisPtRes ) {
    ++nDim;
  }
      } else {
  l2isLep_ = true;
  nDim += 3;
      }
    }
  }

  if ( nDim != integrator2_nDim_ ) {
    mcObjectiveFunctionAdapter_->SetNDim(nDim);    
    integrator2_->setIntegrand(*mcObjectiveFunctionAdapter_);
    mcPtEtaPhiMassAdapter_->SetNDim(nDim);
    integrator2_nDim_ = nDim;
  }
  mcObjectiveFunctionAdapter_->SetL1isLep(l1isLep_);
  mcObjectiveFunctionAdapter_->SetL2isLep(l2isLep_);
  if ( marginalizeVisMass_ && shiftVisMass_ ) {
    std::cerr << "Error: marginalizeVisMass and shiftVisMass flags must not both be enabled !!" << std::endl;
    assert(0);
  }  
  mcObjectiveFunctionAdapter_->SetMarginalizeVisMass(marginalizeVisMass_ && (l1lutVisMass || l2lutVisMass));
  mcObjectiveFunctionAdapter_->SetShiftVisMass(shiftVisMass_ && (l1lutVisMassRes || l2lutVisMassRes));
  mcObjectiveFunctionAdapter_->SetShiftVisPt(shiftVisPt_ && (l1lutVisPtRes || l2lutVisPtRes));
  // CV: use same binning for Markov Chain and VEGAS integration.
  //     The binning relative to the visible mass avoids that SVfit mass is "quantizied" at the same discrete values for all events.
  double visMass = measuredDiTauSystem().mass();
  double minMass = visMass/1.0125;
  double maxMass = TMath::Max(1.e+4, 1.e+1*minMass);
  TH1* histogramMass = makeHistogram("SVfitStandaloneAlgorithmMarkovChain_histogramMass", minMass, maxMass, 1.025);
  TH1* histogramMass_density = (TH1*)histogramMass->Clone(Form("%s_density", histogramMass->GetName()));
  mcPtEtaPhiMassAdapter_->SetHistogramMass(histogramMass, histogramMass_density);
  double visTransverseMass2 = square(measuredTauLeptons()[0].Et() + measuredTauLeptons()[1].Et()) - (square(measuredDiTauSystem().px()) + square(measuredDiTauSystem().py()));
  double visTransverseMass = TMath::Sqrt(TMath::Max(1., visTransverseMass2));  
  //std::cout << "visMass = " << visMass << ", visTransverseMass = " << visTransverseMass << std::endl;
  double minTransverseMass = visTransverseMass/1.0125;
  double maxTransverseMass = TMath::Max(1.e+4, 1.e+1*minTransverseMass);
  TH1* histogramTransverseMass = makeHistogram("SVfitStandaloneAlgorithmMarkovChain_histogramTransverseMass", minTransverseMass, maxTransverseMass, 1.025);
  TH1* histogramTransverseMass_density = (TH1*)histogramTransverseMass->Clone(Form("%s_density", histogramTransverseMass->GetName()));
  mcPtEtaPhiMassAdapter_->SetHistogramTransverseMass(histogramTransverseMass, histogramTransverseMass_density);

  mcPtEtaPhiMassAdapter_->SetL1isLep(l1isLep_);
  mcPtEtaPhiMassAdapter_->SetL2isLep(l2isLep_);
  mcPtEtaPhiMassAdapter_->SetMarginalizeVisMass(marginalizeVisMass_ && (l1lutVisMass || l2lutVisMass));
  mcPtEtaPhiMassAdapter_->SetShiftVisMass(shiftVisMass_ && (l1lutVisMassRes || l2lutVisMassRes));
  mcPtEtaPhiMassAdapter_->SetShiftVisPt(shiftVisPt_ && (l1lutVisPtRes || l2lutVisPtRes));
  
  /* --------------------------------------------------------------------------------------
     lower and upper bounds for integration. Boundaries are defined for each decay channel
     separately. The order is: 
     
     - fully hadronic {xhad1, phihad1, (masshad1, pthad1), xhad2, phihad2, (masshad2, pthad2)}
     - semi  leptonic {xlep, nunuMass, philep, xhad, phihad, (masshad, pthad)}
     - fully leptonic {xlep1, nunuMass1, philep1, xlep2, nunuMass2, philep2}
     
     x0* defines the start value for the integration, xl* defines the lower integation bound, 
     xh* defines the upper integration bound in the following definitions. 
     ATTENTION: order matters here! In the semi-leptonic decay the lepton must go first in 
     the parametrization, as it is first in the definition of integral boundaries. This is
     the reason why the measuredLeptons are eventually re-ordered in the constructor of 
     this class before passing them on to SVfitStandaloneLikelihood.
  */
  std::vector<double> x0(nDim);
  std::vector<double> xl(nDim);
  std::vector<double> xh(nDim);
  if ( l1isLep_ ) {
    x0[idxFitParLeg1_ + 0] = 0.5; 
    xl[idxFitParLeg1_ + 0] = 0.0; 
    xh[idxFitParLeg1_ + 0] = 1.0; 
    x0[idxFitParLeg1_ + 1] = 0.8; 
    xl[idxFitParLeg1_ + 1] = 0.0; 
    xh[idxFitParLeg1_ + 1] = svFitStandalone::tauLeptonMass; 
    x0[idxFitParLeg1_ + 2] = 0.0; 
    xl[idxFitParLeg1_ + 2] = -TMath::Pi(); 
    xh[idxFitParLeg1_ + 2] = +TMath::Pi();
  } else {
    x0[idxFitParLeg1_ + 0] = 0.5; 
    xl[idxFitParLeg1_ + 0] = 0.0; 
    xh[idxFitParLeg1_ + 0] = 1.0; 
    x0[idxFitParLeg1_ + 1] = 0.0; 
    xl[idxFitParLeg1_ + 1] = -TMath::Pi(); 
    xh[idxFitParLeg1_ + 1] = +TMath::Pi();
    int offset1 = 2;
    if ( (marginalizeVisMass_ && l1lutVisMass) || (shiftVisMass_ && l1lutVisMassRes) ) {
      x0[idxFitParLeg1_ + offset1] = 0.8; 
      xl[idxFitParLeg1_ + offset1] = svFitStandalone::chargedPionMass; 
      xh[idxFitParLeg1_ + offset1] = svFitStandalone::tauLeptonMass; 
      ++offset1;
    }
    if ( shiftVisPt_ && l1lutVisPtRes ) {
      x0[idxFitParLeg1_ + offset1] = 0.0; 
      xl[idxFitParLeg1_ + offset1] = -1.0; 
      xh[idxFitParLeg1_ + offset1] = +1.5;
      ++offset1;
    }
  }
  if ( l2isLep_ ) {
    x0[idxFitParLeg2_ + 0] = 0.5; 
    xl[idxFitParLeg2_ + 0] = 0.0; 
    xh[idxFitParLeg2_ + 0] = 1.0; 
    x0[idxFitParLeg2_ + 1] = 0.8; 
    xl[idxFitParLeg2_ + 1] = 0.0; 
    xh[idxFitParLeg2_ + 1] = svFitStandalone::tauLeptonMass; 
    x0[idxFitParLeg2_ + 2] = 0.0; 
    xl[idxFitParLeg2_ + 2] = -TMath::Pi(); 
    xh[idxFitParLeg2_ + 2] = +TMath::Pi();
  } else {
    x0[idxFitParLeg2_ + 0] = 0.5; 
    xl[idxFitParLeg2_ + 0] = 0.0; 
    xh[idxFitParLeg2_ + 0] = 1.0; 
    x0[idxFitParLeg2_ + 1] = 0.0; 
    xl[idxFitParLeg2_ + 1] = -TMath::Pi(); 
    xh[idxFitParLeg2_ + 1] = +TMath::Pi();
    int offset2 = 2;
    if ( (marginalizeVisMass_ && l2lutVisMass) || (shiftVisMass_ && l2lutVisMassRes) ) {
      x0[idxFitParLeg2_ + offset2] = 0.8; 
      xl[idxFitParLeg2_ + offset2] = svFitStandalone::chargedPionMass; 
      xh[idxFitParLeg2_ + offset2] = svFitStandalone::tauLeptonMass; 
      ++offset2;
    }
    if ( shiftVisPt_ && l2lutVisPtRes ) {     
      x0[idxFitParLeg2_ + offset2] = 0.0; 
      xl[idxFitParLeg2_ + offset2] = -1.0; 
      xh[idxFitParLeg2_ + offset2] = +1.5;
      ++offset2;
    }
  }
  for ( int i = 0; i < nDim; ++i ) {
    // transform startPosition into interval ]0..1[
    // expected by MarkovChainIntegrator class
    x0[i] = (x0[i] - xl[i])/(xh[i] - xl[i]);
    //std::cout << "x0[" << i << "] = " << x0[i] << std::endl;
  }
  integrator2_->initializeStartPosition_and_Momentum(x0);
  nll_->addDelta(false);
  nll_->addSinTheta(false);
  nll_->addPhiPenalty(false);
  nll_->marginalizeVisMass(marginalizeVisMass_ && (l1lutVisMass || l2lutVisMass), l1lutVisMass, l2lutVisMass);
  nll_->shiftVisMass(shiftVisMass_ && (l1lutVisMassRes || l2lutVisMassRes), l1lutVisMassRes, l2lutVisMassRes);
  nll_->shiftVisPt(shiftVisPt_ && (l1lutVisPtRes || l2lutVisPtRes), l1lutVisPtRes, l2lutVisPtRes);
  nll_->requirePhysicalSolution(true);
  double integral = 0.;
  double integralErr = 0.;
  int errorFlag = 0;
  integrator2_->integrate(xl, xh, integral, integralErr, errorFlag);
  fitStatus_ = errorFlag;
  pt_ = mcPtEtaPhiMassAdapter_->getPt();
  ptUncert_ = mcPtEtaPhiMassAdapter_->getPtUncert();
  ptLmax_ = mcPtEtaPhiMassAdapter_->getPtLmax();
  eta_ = mcPtEtaPhiMassAdapter_->getEta();
  etaUncert_ = mcPtEtaPhiMassAdapter_->getEtaUncert();
  etaLmax_ = mcPtEtaPhiMassAdapter_->getEtaLmax();
  phi_ = mcPtEtaPhiMassAdapter_->getPhi();
  phiUncert_ = mcPtEtaPhiMassAdapter_->getPhiUncert();
  phiLmax_ = mcPtEtaPhiMassAdapter_->getPhiLmax();
  mass_ = mcPtEtaPhiMassAdapter_->getMass();
  massUncert_ = mcPtEtaPhiMassAdapter_->getMassUncert();
  massLmax_ = mcPtEtaPhiMassAdapter_->getMassLmax();
  if ( !(massLmax_ > 0.) ) fitStatus_ = 1;
  transverseMass_ = mcPtEtaPhiMassAdapter_->getTransverseMass();
  transverseMassUncert_ = mcPtEtaPhiMassAdapter_->getTransverseMassUncert();
  transverseMassLmax_ = mcPtEtaPhiMassAdapter_->getTransverseMassLmax();
  fittedDiTauSystem_ = ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double> >(pt_, eta_, phi_, mass_);
  if ( likelihoodFileName != "" ) {
    TFile* likelihoodFile = new TFile(likelihoodFileName.data(), "RECREATE");
    //mcPtEtaPhiMassAdapter_->histogramPt_->Write();
    //mcPtEtaPhiMassAdapter_->histogramPt_density_->Write();
    //mcPtEtaPhiMassAdapter_->histogramEta_->Write();
    //mcPtEtaPhiMassAdapter_->histogramEta_density_->Write();
    //mcPtEtaPhiMassAdapter_->histogramPhi_->Write();
    //mcPtEtaPhiMassAdapter_->histogramPhi_density_->Write();
    //mcPtEtaPhiMassAdapter_->histogramMass_->Write();
    //mcPtEtaPhiMassAdapter_->histogramMass_density_->Write();
    //mcPtEtaPhiMassAdapter_->histogramTransverseMass_->Write();
    //mcPtEtaPhiMassAdapter_->histogramTransverseMass_density_->Write();
    histogramMass->Write();
    histogramMass_density->Write();
    delete likelihoodFile;
  }

  delete histogramMass;
  delete histogramMass_density;
  mcPtEtaPhiMassAdapter_->SetHistogramMass(0, 0);

  if ( verbosity_ >= 1 ) {
    std::cout << "--> Pt = " << pt_ << ", eta = " << eta_ << ", phi = " << phi_ << ", mass  = " << mass_ << std::endl;
    clock_->Show("<SVfitStandaloneAlgorithm::integrateMarkovChain>");
  }
}