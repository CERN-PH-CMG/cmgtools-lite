from CMGTools.H2TauTau.proto.analyzers.H2TauTauTreeProducer import H2TauTauTreeProducer

class H2TauTauTreeProducerMuEle(H2TauTauTreeProducer):
    '''Tree producer for the H->tau tau analysis'''
  
    def declareVariables(self, setup):
        super(H2TauTauTreeProducerMuEle, self).declareVariables(setup)

        self.bookEle (self.tree, 'l1')
        self.bookMuon(self.tree, 'l2')

        self.bookGenParticle(self.tree, 'l1_gen')
        self.var(self.tree, 'l1_gen_lepfromtau', int)
        self.bookGenParticle(self.tree, 'l2_gen')
        self.var(self.tree, 'l2_gen_lepfromtau', int)

        self.bookTau(self.tree, 'tau1')
        self.bookGenParticle(self.tree, 'tau1_gen')

        if hasattr(self.cfg_ana, 'addIsoInfo') and self.cfg_ana.addIsoInfo:
            self.var(self.tree, 'l1_puppi_iso_pt')
            self.var(self.tree, 'l1_puppi_iso04_pt')
            self.var(self.tree, 'l1_puppi_iso03_pt')

            self.var(self.tree, 'l1_puppi_no_lepton_iso_pt')
            self.var(self.tree, 'l1_puppi_no_lepton_iso04_pt')
            self.var(self.tree, 'l1_puppi_no_lepton_iso03_pt')

            self.var(self.tree, 'l1_mini_iso')
            self.var(self.tree, 'l1_mini_reliso')

            self.var(self.tree, 'l2_puppi_iso_pt')
            self.var(self.tree, 'l2_puppi_iso04_pt')
            self.var(self.tree, 'l2_puppi_iso03_pt')

            self.var(self.tree, 'l2_puppi_no_lepton_iso_pt')
            self.var(self.tree, 'l2_puppi_no_lepton_iso04_pt')
            self.var(self.tree, 'l2_puppi_no_lepton_iso03_pt')

            self.var(self.tree, 'l2_mini_iso')
            self.var(self.tree, 'l2_mini_reliso')

  
    def process(self, event):
         
        super(H2TauTauTreeProducerMuEle, self).process(event)

        ele = event.diLepton.leg1() 
        muon = event.diLepton.leg2()

        self.fillEle(self.tree, 'l1', ele)
        self.fillMuon(self.tree, 'l2', muon)

        if getattr(muon, 'genp', False):
            self.fillGenParticle(self.tree, 'l2_gen', muon.genp)
            self.fill(self.tree, 'l2_gen_lepfromtau', muon.isTauLep)

        if getattr(ele, 'genp', False):
            self.fillGenParticle(self.tree, 'l1_gen', ele.genp)
            self.fill(self.tree, 'l1_gen_lepfromtau', ele.isTauLep)


        if getattr(self.cfg_ana, 'addIsoInfo', False):
            self.fill(self.tree, 'l1_puppi_iso_pt', ele.puppi_iso_pt)
            self.fill(self.tree, 'l1_puppi_iso04_pt', ele.puppi_iso04_pt)
            self.fill(self.tree, 'l1_puppi_iso03_pt', ele.puppi_iso03_pt)
            self.fill(self.tree, 'l1_puppi_no_lepton_iso_pt', ele.puppi_no_lepton_iso_pt)
            self.fill(self.tree, 'l1_puppi_no_lepton_iso04_pt', ele.puppi_no_lepton_iso04_pt)
            self.fill(self.tree, 'l1_puppi_no_lepton_iso03_pt', ele.puppi_no_lepton_iso03_pt)
            self.fill(self.tree, 'l1_mini_iso', ele.miniAbsIso)
            self.fill(self.tree, 'l1_mini_reliso', ele.miniRelIso)

            self.fill(self.tree, 'l2_puppi_iso_pt', muon.puppi_iso_pt)
            self.fill(self.tree, 'l2_puppi_iso04_pt', muon.puppi_iso04_pt)
            self.fill(self.tree, 'l2_puppi_iso03_pt', muon.puppi_iso03_pt)
            self.fill(self.tree, 'l2_puppi_no_lepton_iso_pt', muon.puppi_no_lepton_iso_pt)
            self.fill(self.tree, 'l2_puppi_no_lepton_iso04_pt', muon.puppi_no_lepton_iso04_pt)
            self.fill(self.tree, 'l2_puppi_no_lepton_iso03_pt', muon.puppi_no_lepton_iso03_pt)
            self.fill(self.tree, 'l2_mini_iso', muon.miniAbsIso)
            self.fill(self.tree, 'l2_mini_reliso', muon.miniRelIso)


        if event.selectedTaus:
            tau1 = event.selectedTaus[0]
            self.fillTau(self.tree, 'tau1', tau1)
            if hasattr(tau1, 'genp') and tau1.genp:
                self.fillGenParticle(self.tree, 'tau1_gen', tau1.genp)

        self.fillTree(event)
