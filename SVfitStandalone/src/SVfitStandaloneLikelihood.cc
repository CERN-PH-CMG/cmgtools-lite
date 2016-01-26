#include "CMGTools/SVfitStandalone/interface/SVfitStandaloneLikelihood.h"

#include "CMGTools/SVfitStandalone/interface/svFitStandaloneAuxFunctions.h"
#include "CMGTools/SVfitStandalone/interface/LikelihoodFunctions.h"

// !!! ONLY FOR TESTING
//#include "CMGTools/SVfitMEM/interface/svFitAuxFunctions.h"
//     FOR TESTING ONLY !!!

using namespace svFitStandalone;

/// global function pointer for minuit or VEGAS
const SVfitStandaloneLikelihood* SVfitStandaloneLikelihood::gSVfitStandaloneLikelihood = 0;
/// indicate first iteration for integration or fit cycle for debugging
static bool FIRST = true;

SVfitStandaloneLikelihood::SVfitStandaloneLikelihood(const std::vector<MeasuredTauLepton>& measuredTauLeptons, const Vector& measuredMET, const TMatrixD& covMET, bool verbosity) 
  : metPower_(1.0), 
    addLogM_(false), 
    powerLogM_(1.),
    addDelta_(true),
    addSinTheta_(false),
    addPhiPenalty_(true),
    verbosity_(verbosity), 
    idxObjFunctionCall_(0), 
    invCovMET_(2,2),
    errorCode_(0),
    requirePhysicalSolution_(false),
    marginalizeVisMass_(false),
    l1lutVisMass_(0),
    l2lutVisMass_(0),
    shiftVisMass_(false),
    l1lutVisMassRes_(0),
    l2lutVisMassRes_(0),
    shiftVisPt_(false),
    l1lutVisPtRes_(0),
    l2lutVisPtRes_(0)
{
  //if ( verbosity_ ) {
  //  std::cout << "<SVfitStandaloneLikelihood::SVfitStandaloneLikelihood>:" << std::endl;
  //}
  measuredMET_ = measuredMET;
  measuredTauLeptons_= measuredTauLeptons;
  if ( measuredTauLeptons_.size() != 2 ) {
    std::cout << " >> ERROR : the number of measured leptons must be 2 but is found to be: " << measuredTauLeptons_.size() << std::endl;
    errorCode_ |= LeptonNumber;
  }
  // determine transfer matrix for MET
  invCovMET_= covMET;
  covDet_ = invCovMET_.Determinant();
  if ( covDet_ != 0 ) { 
    invCovMET_.Invert(); 
  } else{
    std::cout << " >> ERROR: cannot invert MET covariance Matrix (det=0)." << std::endl;
    errorCode_ |= MatrixInversion;
  }
  // set global function pointer to this
  gSVfitStandaloneLikelihood = this;
}

void 
SVfitStandaloneLikelihood::marginalizeVisMass(bool value, const TH1* l1lutVisMass, const TH1* l2lutVisMass)
{
  marginalizeVisMass_ = value;
  if ( marginalizeVisMass_ ) {
    l1lutVisMass_ = l1lutVisMass;
    l2lutVisMass_ = l2lutVisMass;
  }
}

void 
SVfitStandaloneLikelihood::shiftVisMass(bool value, const TH1* l1lutVisMassRes, const TH1* l2lutVisMassRes)
{
  shiftVisMass_ = value;
  if ( shiftVisMass_ ) {
    l1lutVisMassRes_ = l1lutVisMassRes;
    l2lutVisMassRes_ = l2lutVisMassRes;
  }
}

void 
SVfitStandaloneLikelihood::shiftVisPt(bool value, const TH1* l1lutVisPtRes, const TH1* l2lutVisPtRes)
{
  shiftVisPt_ = value;
  if ( shiftVisPt_ ) {
    l1lutVisPtRes_ = l1lutVisPtRes;
    l2lutVisPtRes_ = l2lutVisPtRes;
  }
}

const double*
SVfitStandaloneLikelihood::transform(double* xPrime, const double* x, bool fixToMtest, double mtest) const
{
  //if ( verbosity_ ) {
  //  std::cout << "<SVfitStandaloneLikelihood::transform(double*, const double*)>:" << std::endl;
  //}
  LorentzVector fittedDiTauSystem;
  for ( size_t idx = 0; idx < measuredTauLeptons_.size(); ++idx ) {
    const MeasuredTauLepton& measuredTauLepton = measuredTauLeptons_[idx];

    // map to local variables to be more clear on the meaning of the individual parameters. The fit parameters are ayered 
    // for each tau decay
    double nunuMass, labframeXFrac, labframePhi;
    double visMass_unshifted = measuredTauLepton.mass();
    double visMass = visMass_unshifted; // visible momentum in lab-frame
    double labframeVisMom_unshifted = measuredTauLepton.momentum(); 
    double labframeVisMom = labframeVisMom_unshifted; // visible momentum in lab-frame
    double labframeVisEn  = measuredTauLepton.energy(); // visible energy in lab-frame    
    if ( measuredTauLepton.type() == kTauToElecDecay || measuredTauLepton.type() == kTauToMuDecay ) {
      labframeXFrac = x[idx*kMaxFitParams + kXFrac];
      nunuMass = x[idx*kMaxFitParams + kMNuNu];
      labframePhi = x[idx*kMaxFitParams + kPhi];
    } else {
      labframeXFrac = x[idx*kMaxFitParams + kXFrac];
      nunuMass = 0.;
      labframePhi = x[idx*kMaxFitParams + kPhi];
      if ( marginalizeVisMass_ || shiftVisMass_ ) {
  visMass = x[idx*kMaxFitParams + kVisMassShifted];
      } 
      if ( shiftVisPt_ ) {
  double shiftInv = 1. + x[idx*kMaxFitParams + kRecTauPtDivGenTauPt];
  double shift = ( shiftInv > 1.e-1 ) ?
    (1./shiftInv) : 1.e+1;
  labframeVisMom *= shift;
  //visMass *= shift; // CV: take mass and momentum to be correlated
  //labframeVisEn = TMath::Sqrt(labframeVisMom*labframeVisMom + visMass*visMass);
  labframeVisEn *= shift;
      }
    }
    bool isValidSolution = true;
    // add protection against unphysical mass of visible tau decay products
    if ( visMass < electronMass || visMass > tauLeptonMass ) { 
      isValidSolution = false;
    }  
    // add protection against unphysical visible energy fractions
    if ( !(labframeXFrac >= 0. && labframeXFrac <= 1.) ) {
      isValidSolution = false;
    }
    // CV: do not spend time on unphysical solutions: returning 0 pointer will lead to 0 evaluation of prob
    if ( !isValidSolution ) {
      return 0;
    }
    double gjAngle_lab = gjAngleLabFrameFromX(labframeXFrac, visMass, nunuMass, labframeVisMom, labframeVisEn, tauLeptonMass, isValidSolution);
    double enTau_lab = labframeVisEn/labframeXFrac;
    if ( (enTau_lab*enTau_lab) < tauLeptonMass2 ) {
      enTau_lab = tauLeptonMass;
      isValidSolution = false;
    }  
    double pTau_lab = TMath::Sqrt(square(enTau_lab) - tauLeptonMass2);
    double gamma = enTau_lab/tauLeptonMass;
    double beta = TMath::Sqrt(1. - 1./(gamma*gamma));
    double pVis_parl_rf = -beta*gamma*labframeVisEn + gamma*TMath::Cos(gjAngle_lab)*labframeVisMom;
    double pVis_perp = labframeVisMom*TMath::Sin(gjAngle_lab);
    double gjAngle_rf = TMath::ATan2(pVis_perp, pVis_parl_rf);
    Vector p3Tau_unit = motherDirection(measuredTauLepton.direction(), gjAngle_lab, labframePhi);
    LorentzVector p4Tau_lab = motherP4(p3Tau_unit, pTau_lab, enTau_lab);
    //if ( verbosity_ ) {
    //  std::cout << "tau #" << idx << ": Pt = " << p4Tau_lab.pt() << ", eta = " << p4Tau_lab.eta() << ", phi = " << p4Tau_lab.phi() << ", mass = " << p4Tau_lab.mass() << std::endl;
    //  LorentzVector p4Vis_lab = measuredTauLeptons_[idx].p4();
    //  std::cout << "vis #" << idx << ": Pt = " << p4Vis_lab.pt() << ", eta = " << p4Vis_lab.eta() << ", phi = " << p4Vis_lab.phi() << ", mass = " << p4Vis_lab.mass() << std::endl;
    //  LorentzVector p4Nu_lab = p4Tau_lab - p4Vis_lab;
    //  std::cout << "nu #" << idx << ": Pt = " << p4Nu_lab.pt() << ", eta = " << p4Nu_lab.eta() << ", phi = " << p4Nu_lab.phi() << ", mass = " << p4Nu_lab.mass() << std::endl;
    //  double angle = (p4Vis_lab.px()*p4Nu_lab.px() + p4Vis_lab.py()*p4Nu_lab.py() + p4Vis_lab.pz()*p4Nu_lab.pz())/(p4Vis_lab.P()*p4Nu_lab.P());
    //  std::cout << "angle(vis, nu) = " << angle << std::endl;
    //  svFitMEM::Vector beamAxis(0., 0., 1.);
    //  svFitMEM::Vector p3Vis_lab(p4Vis_lab.px(), p4Vis_lab.py(), p4Vis_lab.pz());
    //  svFitMEM::Vector eZ = svFitMEM::normalize(p3Vis_lab);
    //  svFitMEM::Vector eY = svFitMEM::normalize(svFitMEM::compCrossProduct(eZ, beamAxis));
    //  svFitMEM::Vector eX = svFitMEM::normalize(svFitMEM::compCrossProduct(eY, eZ));
    //  svFitMEM::Vector p3Nu_lab(p4Nu_lab.px(), p4Nu_lab.py(), p4Nu_lab.pz());
    //  double pxInvis = svFitMEM::compScalarProduct(p3Nu_lab, eX);
    //  double pyInvis = svFitMEM::compScalarProduct(p3Nu_lab, eY);
    //  double phiInvis = TMath::ATan2(pyInvis, pxInvis);
    //  std::cout << "phiInvis = " << phiInvis << std::endl;
    //}
    fittedDiTauSystem += p4Tau_lab;
    // fill branch-wise nll parameters
    xPrime[ idx == 0 ? kNuNuMass1            : kNuNuMass2            ] = nunuMass;
    xPrime[ idx == 0 ? kVisMass1             : kVisMass2             ] = visMass;
    xPrime[ idx == 0 ? kDecayAngle1          : kDecayAngle2          ] = gjAngle_rf;
    xPrime[ idx == 0 ? kDeltaVisMass1        : kDeltaVisMass2        ] = ( marginalizeVisMass_ ) ? visMass : (visMass_unshifted - visMass);
    xPrime[ idx == 0 ? kRecTauPtDivGenTauPt1 : kRecTauPtDivGenTauPt2 ] = ( labframeVisMom > 0. ) ? (labframeVisMom_unshifted/labframeVisMom) : 1.e+3;
    xPrime[ idx == 0 ? kMaxNLLParams         : (kMaxNLLParams + 1)   ] = labframeXFrac;
    xPrime[ idx == 0 ? (kMaxNLLParams + 2)   : (kMaxNLLParams + 3)   ] = isValidSolution;
  }
 
  Vector fittedMET = fittedDiTauSystem.Vect() - (measuredTauLeptons_[0].p() + measuredTauLeptons_[1].p()); 
  //if ( verbosity_ >= 2 ) {
  //  std::cout << "fittedMET: Px = " << fittedMET.x() << ", Py = " << fittedMET.y() << std::endl;
  //}
  // fill event-wise nll parameters
  xPrime[ kDMETx   ] = measuredMET_.x() - fittedMET.x(); 
  xPrime[ kDMETy   ] = measuredMET_.y() - fittedMET.y();
  if ( fixToMtest ) xPrime[ kMTauTau ] = mtest;       // CV: evaluate delta-function derrivate in case of VEGAS integration for nominal test mass,
  else xPrime[ kMTauTau ] = fittedDiTauSystem.mass(); //     not for fitted mass, to improve numerical stability of integration (this is what the SVfit plugin version does)

  //if ( verbosity_ && FIRST ) {
  //  std::cout << " >> input values for transformed variables: " << std::endl;
  //  std::cout << "    MET[x] = " <<  fittedMET.x() << " (fitted)  " << measuredMET_.x() << " (measured) " << std::endl; 
  //  std::cout << "    MET[y] = " <<  fittedMET.y() << " (fitted)  " << measuredMET_.y() << " (measured) " << std::endl; 
  //  std::cout << "    fittedDiTauSystem: [" 
  //          << " px = " << fittedDiTauSystem.px() 
  //          << " py = " << fittedDiTauSystem.py() 
  //          << " pz = " << fittedDiTauSystem.pz() 
  //          << " En = " << fittedDiTauSystem.energy() 
  //          << " ]" << std::endl; 
  //  std::cout << " >> nll parameters after transformation: " << std::endl;
  //  std::cout << "    x[kNuNuMass1  ] = " << xPrime[kNuNuMass1  ] << std::endl;
  //  std::cout << "    x[kVisMass1   ] = " << xPrime[kVisMass1   ] << std::endl;
  //  std::cout << "    x[kDecayAngle1] = " << xPrime[kDecayAngle1] << std::endl;
  //  std::cout << "    x[kNuNuMass2  ] = " << xPrime[kNuNuMass2  ] << std::endl;
  //  std::cout << "    x[kVisMass2   ] = " << xPrime[kVisMass2   ] << std::endl;
  //  std::cout << "    x[kDecayAngle2] = " << xPrime[kDecayAngle2] << std::endl;
  //  std::cout << "    x[kDMETx      ] = " << xPrime[kDMETx      ] << std::endl;
  //  std::cout << "    x[kDMETy      ] = " << xPrime[kDMETy      ] << std::endl;
  //  std::cout << "    x[kMTauTau    ] = " << xPrime[kMTauTau    ] << std::endl;
  //}
  return xPrime;
}

double
SVfitStandaloneLikelihood::prob(const double* x, bool fixToMtest, double mtest) const 
{
  // in case of initialization errors don't start to do anything
  if ( error() ) { 
    return 0.;
  }
  //if ( verbosity_ ) {
  //  std::cout << "<SVfitStandaloneLikelihood::prob(const double*)>:" << std::endl;
  //}
  ++idxObjFunctionCall_;
  //if ( verbosity_ && FIRST ) {
  //  std::cout << " >> ixdObjFunctionCall : " << idxObjFunctionCall_ << std::endl;  
  //}
  // prevent kPhi in the fit parameters (kFitParams) from trespassing the 
  // +/-pi boundaries
  double phiPenalty = 0.;
  if ( addPhiPenalty_ ) {
    for ( size_t idx = 0; idx < measuredTauLeptons_.size(); ++idx ) {
      if ( TMath::Abs(idx*kMaxFitParams + x[kPhi]) > TMath::Pi() ) {
  phiPenalty += (TMath::Abs(x[kPhi]) - TMath::Pi())*(TMath::Abs(x[kPhi]) - TMath::Pi());
      }
    }
  }
  // xPrime are the transformed variables from which to construct the nll
  // transform performs the transformation from the fit parameters x to the 
  // nll parameters xPrime. prob is the actual combined likelihood. The
  // phiPenalty prevents the fit to converge to unphysical values beyond
  // +/-pi 
  double xPrime[kMaxNLLParams + 4];
  const double* xPrime_ptr = transform(xPrime, x, fixToMtest, mtest);
  if ( xPrime_ptr ) {
    return prob(xPrime_ptr, phiPenalty);
  } else {
    return 0.;
  }
}

double 
SVfitStandaloneLikelihood::prob(const double* xPrime, double phiPenalty) const
{
  //if ( verbosity_ && FIRST ) {
  //  std::cout << "<SVfitStandaloneLikelihood::prob(const double*, double)>:" << std::endl;
  //}
  if ( requirePhysicalSolution_ && (xPrime[ kMaxNLLParams + 2 ] < 0.5 || xPrime[ kMaxNLLParams + 3 ] < 0.5) ) return 0.;
  // add likelihoods for the decay branches
  double prob_PS_and_tauDecay = 1.;
  double prob_TF = 1.;
  for ( size_t idx = 0; idx < measuredTauLeptons_.size(); ++idx ) {
    switch ( measuredTauLeptons_[idx].type() ) {
    case kTauToHadDecay :
      prob_PS_and_tauDecay *= probTauToHadPhaseSpace(
                xPrime[idx == 0 ? kDecayAngle1 : kDecayAngle2], 
    xPrime[idx == 0 ? kNuNuMass1 : kNuNuMass2], 
    xPrime[idx == 0 ? kVisMass1 : kVisMass2], 
    xPrime[idx == 0 ? kMaxNLLParams : (kMaxNLLParams + 1)], 
    addSinTheta_, 
    (verbosity_ && FIRST));
      assert(!(marginalizeVisMass_ && shiftVisMass_));
      if ( marginalizeVisMass_ ) {
  prob_TF *= probVisMass(
                  xPrime[idx == 0 ? kDeltaVisMass1 : kDeltaVisMass2], 
      idx == 0 ? l1lutVisMass_ : l2lutVisMass_,
      (verbosity_ && FIRST));
      }
      if ( shiftVisMass_ ) {
  prob_TF *= probVisMassShift(
                  xPrime[idx == 0 ? kDeltaVisMass1 : kDeltaVisMass2], 
      idx == 0 ? l1lutVisMassRes_ : l2lutVisMassRes_,
      (verbosity_ && FIRST));
      }
      if ( shiftVisPt_ ) {
  prob_TF *= probVisPtShift(
      xPrime[idx == 0 ? kRecTauPtDivGenTauPt1 : kRecTauPtDivGenTauPt2], 
      idx == 0 ? l1lutVisPtRes_ : l2lutVisPtRes_, 
      (verbosity_ && FIRST));
      }
      break;
    case kTauToElecDecay :
    case kTauToMuDecay :
      prob_PS_and_tauDecay *= probTauToLepMatrixElement(
    xPrime[idx == 0 ? kDecayAngle1 : kDecayAngle2], 
    xPrime[idx == 0 ? kNuNuMass1 : kNuNuMass2], 
    xPrime[idx == 0 ? kVisMass1 : kVisMass2], 
    xPrime[idx == 0 ? kMaxNLLParams : (kMaxNLLParams + 1)], 
    addSinTheta_, 
    (verbosity_ && FIRST));
      break;
    default :
      break;
    }
  }
  prob_TF *= probMET(xPrime[kDMETx], xPrime[kDMETy], covDet_, invCovMET_, metPower_, (verbosity_&& FIRST));
  double jacobiFactor = 1.;
  if ( addDelta_ ) {
    jacobiFactor = (2.*xPrime[kMaxNLLParams + 1]/xPrime[kMTauTau]);
  }
  double prob = prob_PS_and_tauDecay*prob_TF*jacobiFactor;
  // add additional logM term if configured such 
  if ( addLogM_ && powerLogM_ > 0. ) {
    if ( xPrime[kMTauTau] > 0. ) {
      prob *= TMath::Power(1.0/xPrime[kMTauTau], powerLogM_);
    }
  }
  // add additional phiPenalty in case kPhi in the fit parameters 
  // (kFitParams) trespassed the physical boundaries from +/-pi 
  if ( phiPenalty > 0. ) {
    prob *= TMath::Exp(-phiPenalty);
  }
  //if ( verbosity_ >= 2 && FIRST ) {
  //  std::cout << "prob: PS+decay = " << prob_PS_and_tauDecay << "," 
  //          << " TF = " << prob_TF << ", Jacobi = " << jacobiFactor << " --> returning " << prob << std::endl;
  //}
  // set FIRST to false after the first complete evaluation of the likelihood 
  FIRST = false;
  return prob;
}

void
SVfitStandaloneLikelihood::results(std::vector<LorentzVector>& fittedTauLeptons, const double* x) const
{
  //if ( verbosity_ ) {
  //  std::cout << "<SVfitStandaloneLikelihood::results(std::vector<LorentzVector>&, const double*)>:" << std::endl;
  //}
  for ( size_t idx = 0; idx < measuredTauLeptons_.size(); ++idx ) {
    const MeasuredTauLepton& measuredTauLepton = measuredTauLeptons_[idx];

    // map to local variables to be more clear on the meaning of the individual parameters. The fit parameters are ayered 
    // for each tau decay
    double nunuMass                 = x[ idx*kMaxFitParams + kMNuNu ];       // nunu inv mass (can be const 0 for had tau decays) 
    double labframeXFrac            = x[ idx*kMaxFitParams + kXFrac ];       // visible energy fraction x in labframe
    double labframePhi              = x[ idx*kMaxFitParams + kPhi   ];       // phi in labframe 
    double visMass                  = measuredTauLepton.mass(); 
    double labframeVisMom_unshifted = measuredTauLepton.momentum(); 
    double labframeVisMom           = labframeVisMom_unshifted; // visible momentum in lab-frame
    double labframeVisEn            = measuredTauLepton.energy(); // visible energy in lab-frame    
    if ( measuredTauLepton.type() == kTauToHadDecay ) {
      if ( marginalizeVisMass_ || shiftVisMass_ ) {
  visMass = x[idx*kMaxFitParams + kVisMassShifted];
      }
      if ( shiftVisPt_ ) {
  double shiftInv = 1. + x[idx*kMaxFitParams + kRecTauPtDivGenTauPt];
        double shift = ( shiftInv > 1.e-1 ) ?
    (1./shiftInv) : 1.e+1;
        labframeVisMom *= shift;
        //visMass *= shift; // CV: take mass and momentum to be correlated
        //labframeVisEn = TMath::Sqrt(labframeVisMom*labframeVisMom + visMass*visMass);
        labframeVisEn *= shift;
      }
    }
    if ( visMass < 5.1e-4 ) { 
      visMass = 5.1e-4; 
    } 
    bool isValidSolution = true;
    double gjAngle_lab = gjAngleLabFrameFromX(labframeXFrac, visMass, nunuMass, labframeVisMom, labframeVisEn, tauLeptonMass, isValidSolution);
    double enTau_lab = labframeVisEn/labframeXFrac;
    double pTau_lab = TMath::Sqrt(square(enTau_lab) - tauLeptonMass2);
    Vector p3Tau_unit = motherDirection(measuredTauLepton.direction(), gjAngle_lab, labframePhi);
    LorentzVector p4Tau_lab = motherP4(p3Tau_unit, pTau_lab, enTau_lab);
    // tau lepton four vector in labframe
    if ( idx < fittedTauLeptons.size() ) fittedTauLeptons[idx] = p4Tau_lab;
    else fittedTauLeptons.push_back(p4Tau_lab);
  }
}