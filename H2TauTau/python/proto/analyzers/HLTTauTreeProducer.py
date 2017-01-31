from PhysicsTools.HeppyCore.utils.deltar import deltaR
from PhysicsTools.Heppy.physicsutils.TauDecayModes import tauDecayModes
from CMGTools.H2TauTau.proto.analyzers.TauGenTreeProducer import TauGenTreeProducer
from CMGTools.H2TauTau.proto.analyzers.H2TauTauTreeProducerBase import H2TauTauTreeProducerBase

class HLTTauTreeProducer(H2TauTauTreeProducerBase):
    ''' Tree producer for tau POG study.
    '''

    def __init__(self, *args):
        super(HLTTauTreeProducer, self).__init__(*args)

    def declareHandles(self):
        super(HLTTauTreeProducer, self).declareHandles()


    def bookTau(self, tau_name):
        self.bookParticle(self.tree, tau_name)
        self.bookGenParticle(self.tree, tau_name+'_gen')
        self.var(self.tree, 'tau_gen_decayMode')

        for var in ['ptSumIso', 'chargedPtSumIso', 'chargedPUPtSumIso', 'gammaPtSumIso', 'neutralPtSumIso', 'ptSumSignal', 'chargedCandsPtSumSignal', 'gammaCandsPtSumSignal', 'neutralCandsPtSumSignal', 'dm', 'loose_db_iso', 'nphotons', 'decayMode']:
            self.var(self.tree, '_'.join([tau_name, var]))

    def fillTau(self, tau, tau_name):
        self.fillParticle(self.tree, tau_name, tau)
        if tau.genp:
            self.fillGenParticle(self.tree, tau_name+'_gen', tau.genp)
            if abs(tau.genp.pdgId()) == 15:
                self.fill(self.tree, 'tau_gen_decayMode', tauDecayModes.genDecayModeInt(tau.genp.daughters))

                print 'From final daughters', tauDecayModes.genDecayModeInt(tau.genp.daughters)

            
        for var in ['ptSumIso', 'chargedPtSumIso', 'chargedPUPtSumIso', 'gammaPtSumIso', 'neutralPtSumIso', 'ptSumSignal', 'chargedCandsPtSumSignal', 'gammaCandsPtSumSignal', 'neutralCandsPtSumSignal', 'dm', 'loose_db_iso', 'nphotons']:
            try:
                self.fill(self.tree, '_'.join([tau_name, var]), getattr(tau, var))
            except TypeError:
                import pdb; pdb.set_trace()
        for var in ['decayMode']:
            try:
                self.fill(self.tree, '_'.join([tau_name, var]), getattr(tau, var)())
            except TypeError:
                import pdb; pdb.set_trace()

    def declareVariables(self, setup):
        self.bookTau('tau')
        self.bookTau('hlt_tau')
        self.bookTau('hlt_single_tau')
        self.var(self.tree, 'rho')

    def process(self, event):
        # needed when doing handle.product(), goes back to
        # PhysicsTools.Heppy.analyzers.core.Analyzer
        self.readCollections(event.input)

        if not eval(self.skimFunction):
            return False


        hlt_taus = [tau for tau in event.hlt_taus] # it's a vector
        hlt_single_taus = [tau for tau in event.hlt_single_taus] # it's a vector
        for tau in event.taus:
            self.tree.reset()

            self.fill(self.tree, 'rho', event.rho)

            if tau.pt() < 20.:
                continue
            self.fillTau(tau, 'tau')

            for hlt_tau in hlt_taus:
                if deltaR(tau, hlt_tau) < 0.3:
                    self.fillTau(hlt_tau, 'hlt_tau')
                    hlt_taus.remove(hlt_tau)
                    break

            for hlt_tau in hlt_single_taus:
                if deltaR(tau, hlt_tau) < 0.3:
                    self.fillTau(hlt_tau, 'hlt_single_tau')
                    hlt_single_taus.remove(hlt_tau)
                    break
            

            self.fillTree(event)

        for hlt_tau in hlt_taus:
            self.tree.reset()
            self.fill(self.tree, 'rho', event.rho)

            if hlt_tau.pt() < 20.:
                continue
            self.fillTau(hlt_tau, 'hlt_tau')
            for single_tau in hlt_single_taus:
                if deltaR(single_tau, hlt_tau) < 0.3:
                    self.fillTau(single_tau, 'hlt_single_tau')
                    hlt_single_taus.remove(single_tau)
                    break
            self.fillTree(event)

        for hlt_tau in hlt_single_taus:
            self.tree.reset()
            self.fill(self.tree, 'rho', event.rho)
            
            if hlt_tau.pt() < 20.:
                continue
            self.fillTau(hlt_tau, 'hlt_single_tau')
            self.fillTree(event)
