from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.HeppyCore.statistics.average import Average

from CMGTools.H2TauTau.proto.weights.ScaleFactor import ScaleFactor


class DiLeptonWeighter(Analyzer):

    '''
    Gets lepton efficiency weight and puts it in the event
    Dedicated to e-mu channel only
    
    '''

    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(DiLeptonWeighter, self).__init__(cfg_ana, cfg_comp, looperName)

        self.muonName = self.cfg_ana.lepton_mu
        self.electronName = self.cfg_ana.lepton_e
        
        self.scaleFactors = {}
        for sf_name, sf_file in self.cfg_ana.scaleFactorFiles.items():
            self.scaleFactors[sf_name] = ScaleFactor(sf_file)

    def beginLoop(self, setup):
        print self, self.__class__
        super(DiLeptonWeighter, self).beginLoop(setup)


    def process(self, event):
        self.readCollections(event.input)
        muon = getattr(event, self.muonName)
        electron = getattr(event, self.electronName)
        muon.weight = 1.
        electron.weight = 1.

        for sf_name in ['trigger', 'idiso']:
            setattr(electron, 'weight_' + sf_name, 1.)
            setattr(muon, 'weight_' + sf_name, 1.)
#            setattr(event, 'eff_data_'+sf_name, 1.)
#            setattr(event, 'eff_MC_'+sf_name, 1.)

        if (self.cfg_comp.isMC or self.cfg_comp.isEmbed) and \
           not (hasattr(self.cfg_ana, 'disable') and self.cfg_ana.disable is True) and muon.pt() < 9999. and electron.pt() < 9999.:
            # Get scale factors

            mu_pt = muon.pt()
            mu_eta = muon.eta()
            e_pt = electron.pt()
            e_eta = electron.eta()

#            print 'muon pt,eta, e pt, eta =', mu_pt, mu_eta, e_pt, e_eta

            idiso_weight = self.scaleFactors['idiso_mu'].getScaleFactor(mu_pt, mu_eta)*self.scaleFactors['idiso_e'].getScaleFactor(e_pt, e_eta)
            idiso_eff_data = self.scaleFactors['idiso_mu'].getEfficiencyData(mu_pt, mu_eta)*self.scaleFactors['idiso_e'].getEfficiencyData(e_pt, e_eta)
            idiso_eff_mc = self.scaleFactors['idiso_mu'].getEfficiencyMC(mu_pt, mu_eta)*self.scaleFactors['idiso_e'].getEfficiencyMC(e_pt, e_eta)


            setattr(electron, 'weight_idiso', idiso_weight)
            setattr(muon, 'weight_idiso', 1.)
#            setattr(event, 'eff_data_idiso', idiso_eff_data)
#            setattr(event, 'eff_mc_idiso', idiso_eff_mc)

#            import pdb; pdb.set_trace()
            event.eventWeight *= getattr(electron, 'weight_idiso')


            # trigger SF 
            eff_data_mu_high = self.scaleFactors['trigger_mu_high'].getEfficiencyData(mu_pt, mu_eta) 
            eff_data_mu_low = self.scaleFactors['trigger_mu_low'].getEfficiencyData(mu_pt, mu_eta) 
            eff_data_e_high = self.scaleFactors['trigger_e_high'].getEfficiencyData(e_pt, e_eta) 
            eff_data_e_low = self.scaleFactors['trigger_e_low'].getEfficiencyData(e_pt, e_eta) 

            # eff_mc_mu_high = self.scaleFactors['trigger_mu_high'].getEfficiencyMC(mu_pt, mu_eta) 
            # eff_mc_mu_low = self.scaleFactors['trigger_mu_low'].getEfficiencyMC(mu_pt, mu_eta) 
            # eff_mc_e_high = self.scaleFactors['trigger_e_high'].getEfficiencyMC(e_pt, e_eta) 
            # eff_mc_e_low = self.scaleFactors['trigger_e_low'].getEfficiencyMC(e_pt, e_eta) 
            
            eff_data = eff_data_mu_high*eff_data_e_low + eff_data_mu_low*eff_data_e_high - eff_data_mu_high*eff_data_e_high
            # eff_mc = eff_mc_mu_high*eff_mc_e_low + eff_mc_mu_low*eff_mc_e_high - eff_mc_mu_high*eff_mc_e_high
            eff_mc = 1.


            setattr(electron, 'weight_trigger', eff_data/eff_mc)
            setattr(muon, 'weight_trigger', 1.)
#            setattr(event, 'eff_data_trigger', eff_data)
#            setattr(event, 'eff_mc_trigger', eff_mc)

            event.eventWeight *= getattr(electron, 'weight_trigger')
            
            # set variables into electron leg



            

#        if not hasattr(event, "triggerWeight"):
#            event.trigweight_1 = 1.0
#        if 'trigger' in self.scaleFactors:
#            event.trigweight_1 *= event.trigweight_1



