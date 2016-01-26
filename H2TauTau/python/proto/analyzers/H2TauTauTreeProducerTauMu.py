from CMGTools.H2TauTau.proto.analyzers.H2TauTauTreeProducer import H2TauTauTreeProducer
from PhysicsTools.Heppy.physicsutils.TauDecayModes import tauDecayModes

class H2TauTauTreeProducerTauMu(H2TauTauTreeProducer):

    '''Tree producer for the H->tau tau analysis.'''

    def declareVariables(self, setup):

        super(H2TauTauTreeProducerTauMu, self).declareVariables(setup)

        self.bookTau(self.tree, 'l2')
        self.bookMuon(self.tree, 'l1')

        self.bookGenParticle(self.tree, 'l2_gen')
        self.var(self.tree, 'l2_gen_lepfromtau', int)
        self.bookGenParticle(self.tree, 'l1_gen')
        self.var(self.tree, 'l1_gen_lepfromtau', int)

        self.bookParticle(self.tree, 'l2_gen_vis')
        self.var(self.tree, 'l2_gen_decaymode', int)

        self.var(self.tree, 'l2_gen_nc_ratio')
        self.var(self.tree, 'l2_nc_ratio')

        self.var(self.tree, 'l2_weight_fakerate')
        self.var(self.tree, 'l2_weight_fakerate_up')
        self.var(self.tree, 'l2_weight_fakerate_down')

        if hasattr(self.cfg_ana, 'addIsoInfo') and self.cfg_ana.addIsoInfo:
            self.var(self.tree, 'l1_puppi_iso_pt')
            self.var(self.tree, 'l1_puppi_iso04_pt')
            self.var(self.tree, 'l1_puppi_iso03_pt')

            self.var(self.tree, 'l1_puppi_no_muon_iso_pt')
            self.var(self.tree, 'l1_puppi_no_muon_iso04_pt')
            self.var(self.tree, 'l1_puppi_no_muon_iso03_pt')

            self.var(self.tree, 'l2_puppi_iso_pt')
            self.var(self.tree, 'l2_puppi_iso04_pt')
            self.var(self.tree, 'l2_puppi_iso03_pt')

            self.var(self.tree, 'l1_mini_iso')
            self.var(self.tree, 'l1_mini_reliso')

        if hasattr(self.cfg_ana, 'addTnPInfo') and self.cfg_ana.addTnPInfo:
            self.var(self.tree, 'tag')
            self.var(self.tree, 'probe')
            self.bookParticle(self.tree, 'l1_trig_obj')
            self.bookParticle(self.tree, 'l2_trig_obj')
            self.bookParticle(self.tree, 'l1_L1')
            self.bookParticle(self.tree, 'l2_L1')
            self.var(self.tree, 'l1_L1_type')
            self.var(self.tree, 'l2_L1_type')
            # RM add further branches related to the HLT filter matching by hand.
            #    I cannot find a better solution for the moment 14/10/2015
            self.bookParticle(self.tree, 'l2_hltL2Tau30eta2p2')


    def process(self, event):

        super(H2TauTauTreeProducerTauMu, self).process(event)

        tau = event.diLepton.leg2()
        muon = event.diLepton.leg1()

#         import pdb ; pdb.set_trace()
        
        self.fillTau(self.tree, 'l2', tau)
        self.fillMuon(self.tree, 'l1', muon)

        if hasattr(tau, 'genp') and tau.genp:
            self.fillGenParticle(self.tree, 'l2_gen', tau.genp)
            self.fill(self.tree, 'l2_gen_lepfromtau', tau.isTauLep)

        if hasattr(muon, 'genp') and muon.genp:
            self.fillGenParticle(self.tree, 'l1_gen', muon.genp)
            self.fill(self.tree, 'l1_gen_lepfromtau', muon.isTauLep)

        # save the p4 of the visible tau products at the generator level
        if tau.genJet() and hasattr(tau, 'genp') and tau.genp and abs(tau.genp.pdgId()) == 15:
            self.fillParticle(self.tree, 'l2_gen_vis', tau.physObj.genJet())
            tau_gen_dm = tauDecayModes.translateGenModeToInt(tauDecayModes.genDecayModeFromGenJet(tau.physObj.genJet()))
            self.fill(self.tree, 'l2_gen_decaymode', tau_gen_dm)
            if tau_gen_dm in [1, 2, 3, 4]:
                pt_neutral = 0.
                pt_charged = 0.
                for daughter in tau.genJet().daughterPtrVector():
                    id = abs(daughter.pdgId())
                    if id in [22, 11]:
                        pt_neutral += daughter.pt()
                    elif id not in [11, 13, 22] and daughter.charge():
                        if daughter.pt() > pt_charged:
                            pt_charged = daughter.pt()
                if pt_charged > 0.:
                    self.fill(self.tree, 'l2_gen_nc_ratio', (pt_charged - pt_neutral)/(pt_charged + pt_neutral))

        if tau.decayMode() in [1, 2, 3, 4]:
            pt_neutral = 0.
            pt_charged = 0.
            # for cand_ptr in tau.signalCands(): # THIS CRASHES
            for i_cand in xrange(len(tau.signalCands())):
                cand = tau.signalCands()[i_cand]
                id = abs(cand.pdgId())
                if id in [11, 22, 130]:
                    pt_neutral += cand.pt()
                elif id in [211]:
                    if cand.pt() > pt_charged:
                        pt_charged = cand.pt()
            if pt_charged > 0.:
                self.fill(self.tree, 'l2_nc_ratio', (pt_charged - pt_neutral)/(pt_charged + pt_neutral))


        self.fill(self.tree, 'l2_weight_fakerate', event.tauFakeRateWeightUp)
        self.fill(self.tree, 'l2_weight_fakerate_up', event.tauFakeRateWeightDown)
        self.fill(self.tree, 'l2_weight_fakerate_down', event.tauFakeRateWeight)

        if hasattr(self.cfg_ana, 'addIsoInfo') and self.cfg_ana.addIsoInfo:
            self.fill(self.tree, 'l1_puppi_iso_pt', muon.puppi_iso_pt)
            self.fill(self.tree, 'l1_puppi_iso04_pt', muon.puppi_iso04_pt)
            self.fill(self.tree, 'l1_puppi_iso03_pt', muon.puppi_iso03_pt)
            self.fill(self.tree, 'l1_puppi_no_muon_iso_pt', muon.puppi_no_muon_iso_pt)
            self.fill(self.tree, 'l1_puppi_no_muon_iso04_pt', muon.puppi_no_muon_iso04_pt)
            self.fill(self.tree, 'l1_puppi_no_muon_iso03_pt', muon.puppi_no_muon_iso03_pt)
            self.fill(self.tree, 'l2_puppi_iso_pt', tau.puppi_iso_pt)
            self.fill(self.tree, 'l2_puppi_iso04_pt', tau.puppi_iso04_pt)
            self.fill(self.tree, 'l2_puppi_iso03_pt', tau.puppi_iso03_pt)
            self.fill(self.tree, 'l1_mini_iso', muon.miniAbsIso)
            self.fill(self.tree, 'l1_mini_reliso', muon.miniRelIso)

        if hasattr(self.cfg_ana, 'addTnPInfo') and self.cfg_ana.addTnPInfo:
            self.fill(self.tree, 'tag', event.tag)
            self.fill(self.tree, 'probe', event.probe)
            if hasattr(muon, 'to'):
                self.fillParticle(self.tree, 'l1_trig_obj', muon.to)
            if hasattr(tau, 'to'):            
                self.fillParticle(self.tree, 'l2_trig_obj', tau.to)
            if hasattr(muon, 'L1'):
                self.fillParticle(self.tree, 'l1_L1', muon.L1)
                self.fill(self.tree, 'l1_L1_type', muon.L1flavour)
            if hasattr(tau, 'L1'):
                self.fillParticle(self.tree, 'l2_L1', tau.L1)
                self.fill(self.tree, 'l2_L1_type', tau.L1flavour)
            # RM add further branches related to the HLT filter matching by hand.
            #    I cannot find a better solution for the moment 14/10/2015
            if hasattr(tau, 'hltL2Tau30eta2p2'):
                self.fillParticle(self.tree, 'l2_hltL2Tau30eta2p2', tau.hltL2Tau30eta2p2)

        self.fillTree(event)
