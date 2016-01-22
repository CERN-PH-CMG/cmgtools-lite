from CMGTools.H2TauTau.proto.analyzers.H2TauTauTreeProducer import H2TauTauTreeProducer

class H2TauTauTreeProducerTauEle(H2TauTauTreeProducer):
    '''Tree producer for the H->tau tau analysis.'''

    def declareVariables(self, setup):

        super(H2TauTauTreeProducerTauEle, self).declareVariables(setup)

        self.bookTau(self.tree, 'l2')
        self.bookEle(self.tree, 'l1')

        self.bookGenParticle(self.tree, 'l1_gen')
        self.var(self.tree, 'l1_gen_lepfromtau', int)

        self.var(self.tree, 'l1_ntriggerobjects')
        self.bookGenParticle(self.tree, 'l1_triggerobject1')
        self.bookGenParticle(self.tree, 'l1_triggerobject2')

        self.bookGenParticle(self.tree, 'l2_gen')
        self.var(self.tree, 'l2_gen_lepfromtau', int)

        self.bookParticle(self.tree, 'l2_gen_vis')

        self.var(self.tree, 'l2_weight_fakerate')
        self.var(self.tree, 'l2_weight_fakerate_up')
        self.var(self.tree, 'l2_weight_fakerate_down')

        self.var( self.tree, 'weight_zll')

    def process(self, event):

        super(H2TauTauTreeProducerTauEle, self).process(event)

        tau = event.diLepton.leg2()
        ele = event.diLepton.leg1()

        self.fillTau(self.tree, 'l2', tau)
        self.fillEle(self.tree, 'l1', ele)

        if hasattr(tau, 'genp') and tau.genp:
            self.fillGenParticle(self.tree, 'l2_gen', tau.genp)
            self.fill(self.tree, 'l2_gen_lepfromtau', tau.isTauLep)
        if hasattr(ele, 'genp') and ele.genp:
            self.fillGenParticle(self.tree, 'l1_gen', ele.genp)
            self.fill(self.tree, 'l1_gen_lepfromtau', ele.isTauLep)

        if hasattr(ele, 'triggerobjects'):
            n_triggerobjects = len(ele.triggerobjects)
            self.fill(self.tree, 'l1_ntriggerobjects', n_triggerobjects)
            if n_triggerobjects >= 1:
                self.fillParticle(self.tree, 'l1_triggerobject1', ele.triggerobjects[0])
            if n_triggerobjects >= 2:
                self.fillParticle(self.tree, 'l1_triggerobject2', ele.triggerobjects[1])
        
        # save the p4 of the visible tau products at the generator level
        if tau.genJet() and hasattr(tau, 'genp') and tau.genp and abs(tau.genp.pdgId()) == 15:
            self.fillParticle(self.tree, 'l2_gen_vis', tau.physObj.genJet())

        self.fill(self.tree, 'l2_weight_fakerate', event.tauFakeRateWeightUp)
        self.fill(self.tree, 'l2_weight_fakerate_up', event.tauFakeRateWeightDown)
        self.fill(self.tree, 'l2_weight_fakerate_down', event.tauFakeRateWeight)

        self.fill(self.tree, 'weight_zll', event.zllWeight)

        self.fillTree(event)
