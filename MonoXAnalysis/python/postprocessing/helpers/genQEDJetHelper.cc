#ifndef CMGTools_MonoXAnalysisTools_genQEDJetHelperHelper_h
#define CMGTools_MonoXAnalysisTools_genQEDJetHelperHelper_h

#include <iostream>
#include <vector>
#include <TTreeReaderValue.h>
#include <TTreeReaderArray.h>
#include <TLorentzVector.h>
#include <DataFormats/Math/interface/deltaR.h>

class GenQEDJetHelper {
 public:
  typedef TTreeReaderValue<int>   rint;
  typedef TTreeReaderArray<float> rfloats;
  typedef TTreeReaderArray<int> rints;
  typedef TLorentzVector genparticle;
  typedef std::vector<genparticle> genparticles;

  GenQEDJetHelper(float dR=0.1) { deltaR_=dR; }
  ~GenQEDJetHelper() {}
  
  void setGenParticles(rint *nGp, rfloats *gpPt, rfloats *gpEta, rfloats *gpPhi, rfloats *gpMass, rints *gpPdgId, rints *gpPromptHard) {
    nGp_ = nGp; Gp_pt_ = gpPt; Gp_eta_ = gpEta; Gp_phi_ = gpPhi; Gp_mass_ = gpMass; Gp_pdgId_ = gpPdgId; Gp_prompt_ = gpPromptHard;
  }
  void run() {
    dressedLeptons_.clear();
    neutrinos_.clear();
    lepPdgIds_.clear();
    nuPdgIds_.clear();

    // fill the prmpt hard particles and leptons / neutrinos
    genparticles promptgp;
    std::vector<int> pdgIds;
    for(int iP = 0, nP = **nGp_; iP < nP; ++iP) {
      int pdgId = (*Gp_pdgId_)[iP];
      bool isChLep = abs(pdgId)==11 || abs(pdgId)==13 || abs(pdgId)==15;
      genparticle gp = TLorentzVector();
      gp.SetPtEtaPhiM((*Gp_pt_)[iP],(*Gp_eta_)[iP],(*Gp_phi_)[iP],(*Gp_mass_)[iP]);
      if( (*Gp_prompt_)[iP] && (*Gp_pt_)[iP]>0 && (isChLep || abs(pdgId)==22) ) {
        promptgp.push_back(gp);
        pdgIds.push_back(pdgId);
      } else if ( (*Gp_prompt_)[iP] && (*Gp_pt_)[iP]>0 && (abs(pdgId)==12 || abs(pdgId)==14 || abs(pdgId)==16) ) {
        neutrinos_.push_back(gp);
        nuPdgIds_.push_back(pdgId);
      }
    }

    std::vector<bool> usedPart;
    for(int iP=0;iP<(int)promptgp.size(); ++iP) usedPart.push_back(false);
    for(int iL=0; iL<(int)promptgp.size(); ++iL) {
      for(int iP=iL+1; iP<(int)promptgp.size(); ++iP) {
        if(!usedPart[iP] && promptgp[iL].DeltaR(promptgp[iP]) < deltaR_) {
          // std::cout << "Dressing a lepton with a particle of pt = " << promptgp[iP].Pt() << " and within dR = " << leps[iL].DeltaR(promptgp[iP]) << std::endl;
          promptgp[iL] += promptgp[iP];
          usedPart[iP] = true;
        }
      }
      bool isChLep = abs(pdgIds[iL])==11 || abs(pdgIds[iL])==13 || abs(pdgIds[iL])==15;
      if(!usedPart[iL] && isChLep) {
        dressedLeptons_.push_back(promptgp[iL]);
        lepPdgIds_.push_back(pdgIds[iL]);
      }
    }
  }

  const genparticles & dressedLeptons() { return dressedLeptons_; }
  const genparticles & promptNeutrinos() { return neutrinos_; }
  const std::vector<int> & dressedLeptonsPdgId() { return lepPdgIds_; }
  const std::vector<int> & promptNeutrinosPdgId() { return nuPdgIds_; }

private:
  genparticles dressedLeptons_, neutrinos_;
  std::vector<int> lepPdgIds_,nuPdgIds_;
  float deltaR_;
  rint *nGp_ = nullptr;
  rfloats *Gp_pt_ = nullptr;
  rfloats *Gp_eta_ = nullptr;
  rfloats *Gp_phi_ = nullptr;
  rfloats *Gp_mass_ = nullptr;
  rints *Gp_pdgId_ = nullptr;
  rints *Gp_prompt_ = nullptr;
};

#endif
