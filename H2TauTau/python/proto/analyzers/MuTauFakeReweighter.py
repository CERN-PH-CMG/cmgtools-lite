from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer

class MuTauFakeReweighter(Analyzer):
    '''Reweight muon->tauh fakes as derived here:
    https://twiki.cern.ch/twiki/bin/viewauth/CMS/TauIDRecommendation13TeV#Muon_to_tau_fake_rate
    '''

    @staticmethod
    def sfTight(eta):
        eta = abs(eta)
        if eta < 0.4:
            return 1.5
        if eta < 0.8:
            return 1.4
        if eta < 1.2:
            return 1.21
        if eta < 1.7:
            return 2.6
        if eta < 2.3:
            return 2.1

        print 'MuTauFakeReweighter: invalid eta', eta, 'returning SF of 1'
        return 1.

    @staticmethod
    def sfLoose(eta):
        eta = abs(eta)
        if eta < 0.4:
            return 1.15
        if eta < 0.8:
            return 1.15
        if eta < 1.2:
            return 1.18
        if eta < 1.7:
            return 1.2
        if eta < 2.3:
            return 1.3

        print 'MuTauFakeReweighter: invalid eta', eta, 'returning SF of 1'
        return 1.

    def process(self, event):
        event.zllWeight = 1
        if not self.cfg_comp.isMC:
            return True

        # Only apply corrections for leptons giving rise to fake hadronic taus
        if event.leg2.gen_match not in [2, 4]:
            return True

        tau = event.diLepton.leg2()
        
        if self.cfg_ana.wp == 'tight':
            event.zllWeight = self.sfTight(tau.eta())
        elif self.cfg_ana.wp == 'loose':
            event.zllWeight = self.sfLoose(tau.eta())
        else:
            print 'MuTauFakeReweighter: invalid working point', self.cfg_ana.wp
        
        if self.cfg_ana.verbose:    
            print 'MuTauFakeReweighter', tau.eta(), event.zllWeight
        
        event.eventWeight = event.eventWeight * event.zllWeight
        return True
