from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.HeppyCore.statistics.average import Average

from CMGTools.H2TauTau.proto.weights.ScaleFactor import ScaleFactor


class LeptonWeighter(Analyzer):

    '''Gets lepton efficiency weight and puts it in the event'''

    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(LeptonWeighter, self).__init__(cfg_ana, cfg_comp, looperName)

        self.leptonName = self.cfg_ana.lepton
        
        self.scaleFactors = {}
        for sf_name, sf_file in self.cfg_ana.scaleFactorFiles.items():
            self.scaleFactors[sf_name] = ScaleFactor(sf_file)
        if hasattr(self.cfg_ana, 'otherScaleFactorFiles'):
            for sf_name, sf_file in self.cfg_ana.otherScaleFactorFiles.items():
                self.scaleFactors[sf_name] = ScaleFactor(sf_file)

    def beginLoop(self, setup):
        print self, self.__class__
        super(LeptonWeighter, self).beginLoop(setup)
        self.averages.add('weight', Average('weight'))

        for sf_name in self.scaleFactors:
            self.averages.add('weight_'+sf_name, Average('weight_'+sf_name))
            self.averages.add('eff_data_'+sf_name, Average('eff_data_'+sf_name))
            self.averages.add('eff_MC_'+sf_name, Average('eff_MC_'+sf_name))

    def process(self, event):
        self.readCollections(event.input)
        lep = getattr(event, self.leptonName)
        lep.weight = 1.

        for sf_name in self.scaleFactors:
            setattr(lep, 'weight_'+sf_name, 1.)
            setattr(lep, 'eff_data_'+sf_name, 1.)
            setattr(lep, 'eff_MC_'+sf_name, 1.)

        if (self.cfg_comp.isMC or self.cfg_comp.isEmbed) and \
           not (hasattr(self.cfg_ana, 'disable') and self.cfg_ana.disable is True) and lep.pt() < 9999.:
            # Get scale factors
            for sf_name, sf in self.scaleFactors.items():
                pt = lep.pt()
                eta = lep.eta()
                setattr(lep, 'weight_'+sf_name, sf.getScaleFactor(pt, eta))
                setattr(lep, 'eff_data_'+sf_name, sf.getEfficiencyData(pt, eta))
                setattr(lep, 'eff_mc_'+sf_name, sf.getEfficiencyMC(pt, eta))

                if sf_name in self.cfg_ana.scaleFactorFiles:
                    lep.weight *= getattr(lep, 'weight_'+sf_name)

        if not hasattr(event, "triggerWeight"):
            event.triggerWeight = 1.0
        if 'trigger' in self.scaleFactors:
            event.triggerWeight *= lep.weight_trigger

        event.eventWeight *= lep.weight

        self.averages['weight'].add(lep.weight)
        for sf_name in self.scaleFactors:
            self.averages['weight_'+sf_name].add(getattr(lep, 'weight_'+sf_name))
            self.averages['eff_data_'+sf_name].add(getattr(lep, 'eff_data_'+sf_name))
            self.averages['eff_MC_'+sf_name].add(getattr(lep, 'eff_MC_'+sf_name))
