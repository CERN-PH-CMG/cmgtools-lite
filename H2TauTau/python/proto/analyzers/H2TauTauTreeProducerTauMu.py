import ROOT

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

        self.var(self.tree, 'trigger_isomu22')
        self.var(self.tree, 'trigger_isotkmu22')
        self.var(self.tree, 'trigger_isomu19tau20')

        self.var(self.tree, 'trigger_matched_isomu22')
        self.var(self.tree, 'trigger_matched_isotkmu22')
        self.var(self.tree, 'trigger_matched_isomu19tau20')

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

        if hasattr(self.cfg_ana, 'addTauTrackInfo') and self.cfg_ana.addTauTrackInfo:
            self.var(self.tree, 'tau_iso_n_ch')
            self.var(self.tree, 'tau_iso_n_gamma')
            self.bookTrackInfo('tau_lead_ch')
            self.bookTrackInfo('tau_leadiso_ch')

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


    def bookTrackInfo(self, name):
        self.var(self.tree, name + '_pt')
        self.var(self.tree, name + '_dxy')
        self.var(self.tree, name + '_dz')
        self.var(self.tree, name + '_ndof')
        self.var(self.tree, name + '_chi2')
        self.var(self.tree, name + '_normchi2')
        self.var(self.tree, name + '_n_layers_pixel')
        self.var(self.tree, name + '_n_hits_pixel')
        self.var(self.tree, name + '_n_layers_tracker')
        self.var(self.tree, name + '_n_hits')
        self.var(self.tree, name + '_n_missing_inner')
        self.var(self.tree, name + '_high_purity')

    def fillTrackInfo(self, track, name='tau_track'):
        pt = track.pt()
        ndof = track.pseudoTrack().ndof()
        dxy = track.dxy()
        dz = track.dz()
        chi2 = track.pseudoTrack().chi2()
        norm_chi2 = track.pseudoTrack().normalizedChi2()

        n_layers_pixel = track.pseudoTrack().hitPattern().pixelLayersWithMeasurement()
        n_hits_pixel = track.pseudoTrack().hitPattern().numberOfValidPixelHits()
        n_layers_tracker = track.pseudoTrack().hitPattern().trackerLayersWithMeasurement()
        n_hits = track.pseudoTrack().hitPattern().numberOfValidHits()
        n_missing_inner = track.pseudoTrack().hitPattern().numberOfHits(ROOT.reco.HitPattern.MISSING_INNER_HITS)
        high_purity = track.pseudoTrack().quality(ROOT.reco.TrackBase.highPurity)

        self.fill(self.tree, name + '_pt', pt)
        self.fill(self.tree, name + '_dxy', dxy)
        self.fill(self.tree, name + '_dz', dz)
        self.fill(self.tree, name + '_ndof', ndof)
        self.fill(self.tree, name + '_chi2', chi2)
        self.fill(self.tree, name + '_normchi2', norm_chi2)
        self.fill(self.tree, name + '_n_layers_pixel', n_layers_pixel)
        self.fill(self.tree, name + '_n_hits_pixel', n_hits_pixel)
        self.fill(self.tree, name + '_n_layers_tracker', n_layers_tracker)
        self.fill(self.tree, name + '_n_hits', n_hits)
        self.fill(self.tree, name + '_n_missing_inner', n_missing_inner)
        self.fill(self.tree, name + '_high_purity', high_purity)

    def process(self, event):

        super(H2TauTauTreeProducerTauMu, self).process(event)

        tau = event.diLepton.leg2()
        muon = event.diLepton.leg1()
       
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

        fired_triggers = [info.name for info in getattr(event, 'trigger_infos', []) if info.fired]

        self.fill(self.tree, 'trigger_isomu22', any('IsoMu22_v' in name for name in fired_triggers))
        self.fill(self.tree, 'trigger_isotkmu22', any('IsoTkMu22_v' in name for name in fired_triggers))
        self.fill(self.tree, 'trigger_isomu19tau20', any('IsoMu19_eta2p1_LooseIsoPFTau20_v' in name for name in fired_triggers))

        matched_paths = getattr(event.diLepton, 'matchedPaths', [])
        self.fill(self.tree, 'trigger_matched_isomu22', any('IsoMu22_v' in name for name in matched_paths))
        self.fill(self.tree, 'trigger_matched_isotkmu22', any('IsoTkMu22_v' in name for name in matched_paths))
        self.fill(self.tree, 'trigger_matched_isomu19tau20', any('IsoMu19_eta2p1_LooseIsoPFTau20_v' in name for name in matched_paths))

        if hasattr(self.cfg_ana, 'addTauTrackInfo') and self.cfg_ana.addTauTrackInfo:
            # Leading CH part
            if tau.signalChargedHadrCands().size() == 0:
                print 'Uh, tau w/o charged hadron???'
            
            leading_ch = tau.signalChargedHadrCands()[0].get()
            self.fillTrackInfo(leading_ch, 'tau_lead_ch')

            # Iso part
            i_lead_ch = -1
            n_ch = len(tau.isolationChargedHadrCands())
            n_gamma = len(tau.isolationGammaCands())

            self.fill(self.tree, 'tau_iso_n_ch', n_ch)
            self.fill(self.tree, 'tau_iso_n_gamma', n_gamma)

            for i_cand in xrange(n_ch):
                if i_lead_ch >= 0:
                    if tau.isolationChargedHadrCands()[i_cand].get().pt() > tau.isolationChargedHadrCands()[i_lead_ch].get().pt():
                        i_lead_ch = i_cand
                else:
                    i_lead_ch = i_cand

            if i_lead_ch >= 0 and tau.isolationChargedHadrCands()[i_lead_ch].get().pt() > 0.95:
                track = tau.isolationChargedHadrCands()[i_lead_ch].get()
                self.fillTrackInfo(track, 'tau_leadiso_ch')


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
