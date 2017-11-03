#ifndef RecoEgamma_EgammaTools_EffectiveAreas_H
#define RecoEgamma_EgammaTools_EffectiveAreas_H

#include <cmath>
#include <fstream>
#include <string>
#include <sstream>
#include <vector>

class EffectiveAreas {

public:
  // Constructor, destructor
  EffectiveAreas(const std::string& filename);
  ~EffectiveAreas();

  // Accessors
  float getEffectiveArea(float eta);

  // Utility functions
  void printEffectiveAreas() const;
  void checkConsistency() const;

private:
  // Data members
  const std::string  filename_;  // effective areas source file name
  std::vector<float> absEtaMin_; // low limit of the eta range
  std::vector<float> absEtaMax_; // upper limit of the eta range
  std::vector<float> effectiveAreaValues_; // effective area for this eta range

};

EffectiveAreas::EffectiveAreas(const std::string& filename):
  filename_(filename)
{

  // Open the file with the effective area constants
  std::ifstream inputFile;
  inputFile.open(filename_.c_str());
  if( !inputFile.is_open() )
    throw "EffectiveAreas config failure";
  
  // Read file line by line
  std::string line;
  const float undef = -999;
  while( getline(inputFile, line) ){
    if(line[0]=='#') continue; // skip the comments lines
    float etaMin = undef, etaMax = undef, effArea = undef;
    std::stringstream ss(line);
    ss >>  etaMin >> etaMax >> effArea;
    // In case if the format is messed up, there are letters
    // instead of numbers, or not exactly three numbers in the line,
    // it is likely that one or more of these vars never changed
    // the original "undef" value:
    if( etaMin==undef || etaMax==undef || effArea==undef )
      throw "wrong file format, file name ";
    
    absEtaMin_          .push_back( etaMin );
    absEtaMax_          .push_back( etaMax );
    effectiveAreaValues_.push_back( effArea );
  }

  // Extra consistency checks are in the function below.
  // If any of them fail, an exception is thrown.
  checkConsistency();
}

EffectiveAreas::~EffectiveAreas(){
}

// Return effective area for given eta
float EffectiveAreas::getEffectiveArea(float eta){

  float effArea = 0;
  uint nEtaBins = absEtaMin_.size();
  for(uint iEta = 0; iEta<nEtaBins; iEta++){
    if( std::abs(eta) >= absEtaMin_[iEta]
	&& std::abs(eta) < absEtaMax_[iEta] ){
      effArea = effectiveAreaValues_[iEta];
      break;
    }
  }

  return effArea;
}

void EffectiveAreas::printEffectiveAreas() const {

  printf("EffectiveAreas: source file %s\n", filename_.c_str());
  printf("  eta_min   eta_max    effective area\n");
  uint nEtaBins = absEtaMin_.size();
  for(uint iEta = 0; iEta<nEtaBins; iEta++){
    printf("  %8.4f    %8.4f   %8.5f\n",
	   absEtaMin_[iEta], absEtaMax_[iEta],
	   effectiveAreaValues_[iEta]);
  }

}

// Basic common sense checks
void EffectiveAreas::checkConsistency() const {

  // There should be at least one eta range with one constant
  if( effectiveAreaValues_.size() == 0 )
    throw "found no effective area constans in the file " ;

  uint nEtaBins = absEtaMin_.size();
  for(uint iEta = 0; iEta<nEtaBins; iEta++){

    // The low limit should be lower than the upper limit
    if( !( absEtaMin_[iEta] < absEtaMax_[iEta] ) )
      throw "eta ranges improperly defined (min>max) in the file" ;

    // The low limit of the next range should be (near) equal to the
    // upper limit of the previous range
    if( iEta != nEtaBins-1 ) // don't do the check for the last bin
      if( !( absEtaMin_[iEta+1] - absEtaMax_[iEta] < 0.0001 ) )
	throw "eta ranges improperly defined (disjointed) in the file " ;

    // The effective area should be non-negative number,
    // and should be less than the whole calorimeter area 
    // eta range -2.5 to 2.5, phi 0 to 2pi => Amax = 5*2*pi ~= 31.4
    if( !( effectiveAreaValues_[iEta] >= 0
	   && effectiveAreaValues_[iEta] < 31.4 ) )
      throw "effective area values are too large or negative in the file";
  }

}

#endif
