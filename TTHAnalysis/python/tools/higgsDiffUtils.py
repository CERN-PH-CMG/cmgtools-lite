# General centralized definitions for differential ttH


statusFlagsMap = {
          # Comments taken from:
          # DataFormats/HepMCCandidate/interface/GenParticle.h
          # PhysicsTools/HepMCCandAlgos/interface/MCTruthHelper.h
          #
          # Nomenclature taken from:
          # PhysicsTools/NanoAOD/python/genparticles_cff.py
          #
          #TODO: use this map in other gen-lvl particle selectors as well:
          # GenLepFromTauFromTop -> isDirectPromptTauDecayProduct &&
          #                         isDirectHardProcessTauDecayProduct &&
          #                         isLastCopy &&
          #                         ! isDirectHadronDecayProduct
          # GenLepFromTau -> isDirectTauDecayProduct (or isDirectPromptTauDecayProduct?) &&
          #                  isLastCopy &&
          #                  ! isDirectHadronDecayProduct
          #                  (&& maybe isHardProcessTauDecayProduct?)
          # GenLepFromTop -> isPrompt &&
          #                  isHardProcess &&
          #                  (isLastCopy || isLastCopyBeforeFSR) &&
          #                  ! isDirectHadronDecayProduct
          #
          # Not sure whether to choose (isLastCopy or isLastCopyBeforeFSR) or just isFirstCopy:
          # GenWZQuark, GenHiggsDaughters, GenVbosons
          #
          # Not sure what to require from GenTau
          'isPrompt'                           : 0,  # any decay product NOT coming from hadron, muon or tau decay
          'isDecayedLeptonHadron'              : 1,  # a particle coming from hadron, muon, or tau decay
                                                     # (does not include resonance decays like W,Z,Higgs,top,etc)
                                                     # equivalent to status 2 in the current HepMC standard
          'isTauDecayProduct'                  : 2,  # a direct or indirect tau decay product
          'isPromptTauDecayProduct'            : 3,  # a direct or indirect decay product of a prompt tau
          'isDirectTauDecayProduct'            : 4,  # a direct tau decay product
          'isDirectPromptTauDecayProduct'      : 5,  # a direct decay product from a prompt tau
          'isDirectHadronDecayProduct'         : 6,  # a direct decay product from a hadron
          'isHardProcess'                      : 7,  # part of the hard process
          'fromHardProcess'                    : 8,  # the direct descendant of a hard process particle of the same pdg id
          'isHardProcessTauDecayProduct'       : 9,  # a direct or indirect decay product of a tau from the hard process
          'isDirectHardProcessTauDecayProduct' : 10, # a direct decay product of a tau from the hard process
          'fromHardProcessBeforeFSR'           : 11, # the direct descendant of a hard process particle of the same pdg id
                                                     # for outgoing particles the kinematics are those before QCD or QED FSR
          'isFirstCopy'                        : 12, # the first copy of the particle in the chain with the same pdg id
          'isLastCopy'                         : 13, # the last copy of the particle in the chain with the same pdg id
                                                     # (and therefore is more likely, but not guaranteed,
                                                     # to carry the final physical momentum)
          'isLastCopyBeforeFSR'                : 14, # the last copy of the particle in the chain with the same pdg id
                                                     # before QED or QCD FSR (and therefore is more likely,
                                                     # but not guaranteed, to carry the momentum after ISR;
                                                     # only really makes sense for outgoing particles
        }
