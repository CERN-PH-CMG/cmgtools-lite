from CMGTools.H2TauTau.proto.analyzers.H2TauTauTreeProducer import H2TauTauTreeProducer


class H2TauTauTreeProducerMuMu(H2TauTauTreeProducer):

    '''Tree producer for the H->tau tau->mu mu analysis.'''

    def declareVariables(self, setup):

        super(H2TauTauTreeProducerMuMu, self).declareVariables(setup)

        self.bookMuon(self.tree, 'l1')
        self.bookMuon(self.tree, 'l2')

        self.bookGenParticle(self.tree, 'l1_gen')
        self.bookGenParticle(self.tree, 'l2_gen')

        self.bookTau(self.tree, 'tau1')
        self.bookGenParticle(self.tree, 'tau1_gen')

    def process(self, event):
        super(H2TauTauTreeProducerMuMu, self).process(event)

        mu1 = event.diLepton.leg1()
        mu2 = event.diLepton.leg2()

        self.fillMuon(self.tree, 'l1', mu1)
        self.fillMuon(self.tree, 'l2', mu2)

        if hasattr(mu1, 'genp') and mu1.genp:
            self.fillGenParticle(self.tree, 'l1_gen', mu1.genp)
        if hasattr(mu2, 'genp') and mu2.genp:
            self.fillGenParticle(self.tree, 'l2_gen', mu2.genp)

        if event.selectedTaus:
            tau1 = event.selectedTaus[0]
            self.fillTau(self.tree, 'tau1', tau1)
            if hasattr(tau1, 'genp') and tau1.genp:
                self.fillGenParticle(self.tree, 'tau1_gen', tau1.genp)

        self.fillTree(event)
        