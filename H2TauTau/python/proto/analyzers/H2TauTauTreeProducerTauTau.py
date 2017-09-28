from CMGTools.H2TauTau.proto.analyzers.H2TauTauTreeProducer import H2TauTauTreeProducer
from PhysicsTools.Heppy.physicsutils.TauDecayModes import tauDecayModes

from CMGTools.H2TauTau.proto.analyzers.HTTGenAnalyzer import HTTGenAnalyzer

class H2TauTauTreeProducerTauTau(H2TauTauTreeProducer):

    '''Tree producer for the H->tau tau analysis'''

    def declareVariables(self, setup):

        super(H2TauTauTreeProducerTauTau, self).declareVariables(setup)

        self.bookTau(self.tree, 'l1')
        self.bookTau(self.tree, 'l2')

        self.bookGenParticle(self.tree, 'l1_gen')
        self.bookGenParticle(self.tree, 'l2_gen')

        self.bookParticle(self.tree, 'l1_gen_vis')
        self.bookParticle(self.tree, 'l2_gen_vis')

        self.var(self.tree, 'l1_gen_decaymode', int)
        self.var(self.tree, 'l2_gen_decaymode', int)

        self.var(self.tree, 'l1_trigger_weight')
        self.var(self.tree, 'l1_trigger_weight_up')
        self.var(self.tree, 'l1_trigger_weight_down')

        self.var(self.tree, 'l2_trigger_weight')
        self.var(self.tree, 'l2_trigger_weight_up')
        self.var(self.tree, 'l2_trigger_weight_down')

        self.var(self.tree, 'mt2')
        self.var(self.tree, 'mt2_lep')
        self.var(self.tree, 'mt2_mvamet')
        self.var(self.tree, 'mt2_rawpfmet')

        self.var(self.tree, 'minDphiMETJets')
        
        self.var(self.tree, 'trigger_ditau35')
        self.var(self.tree, 'trigger_ditau35_combiso')
        self.var(self.tree, 'trigger_singletau140')
        self.var(self.tree, 'trigger_singletau120')

        self.var(self.tree, 'trigger_matched_ditau35')
        self.var(self.tree, 'trigger_matched_ditau35_combiso')
        self.var(self.tree, 'trigger_matched_singletau140')
        self.var(self.tree, 'trigger_matched_singletau120')

        if self.cfg_comp.isMC and getattr(self.cfg_ana, 'isSUSY', False):
            self.var(self.tree, 'GenSusyMScan1')
            self.var(self.tree, 'GenSusyMScan2')
            self.var(self.tree, 'GenSusyMScan3')
            self.var(self.tree, 'GenSusyMScan4')
            self.var(self.tree, 'GenSusyMNeutralino')
            self.var(self.tree, 'GenSusyMChargino')
            self.var(self.tree, 'GenSusyMStau')
            self.var(self.tree, 'GenSusyMStau2')
            self.bookLHEWeights(self.tree)
            self.var(self.tree, 'gen_dichargino_pt')

    def process(self, event):

        super(H2TauTauTreeProducerTauTau, self).process(event)

        isSUSY = getattr(self.cfg_ana, 'isSUSY', False)

        tau1 = event.diLepton.leg1()
        tau2 = event.diLepton.leg2()

        self.fillTau(self.tree, 'l1', tau1)
        self.fillTau(self.tree, 'l2', tau2)

        if hasattr(tau1, 'genp'):
            if tau1.genp:
                self.fillGenParticle(self.tree, 'l1_gen', tau1.genp)
        if hasattr(tau2, 'genp'):
            if tau2.genp:
                self.fillGenParticle(self.tree, 'l2_gen', tau2.genp)

        # save the p4 of the visible tau products at the generator level
        # make sure that the reco tau matches with a gen tau that decays into hadrons

        if tau1.genJet() and hasattr(tau1, 'genp') and tau1.genp and abs(tau1.genp.pdgId()) == 15:
            self.fillParticle(self.tree, 'l1_gen_vis', tau1.physObj.genJet())
            tau_gen_dm = tauDecayModes.translateGenModeToInt(tauDecayModes.genDecayModeFromGenJet(tau1.physObj.genJet()))
            self.fill(self.tree, 'l1_gen_decaymode', tau_gen_dm)

        if tau2.genJet() and hasattr(tau2, 'genp') and tau2.genp and abs(tau2.genp.pdgId()) == 15:
            self.fillParticle(self.tree, 'l2_gen_vis', tau2.physObj.genJet())
            tau_gen_dm = tauDecayModes.translateGenModeToInt(tauDecayModes.genDecayModeFromGenJet(tau2.physObj.genJet()))
            self.fill(self.tree, 'l2_gen_decaymode', tau_gen_dm)

        if hasattr(tau1, 'weight_trigger'):
            self.fill(self.tree, 'l1_trigger_weight', tau1.weight_trigger)
            self.fill(self.tree, 'l1_trigger_weight_up', getattr(tau1, 'weight_trigger_up', 1.))
            self.fill(self.tree, 'l1_trigger_weight_down', getattr(tau1, 'weight_trigger_down', 1.))

            self.fill(self.tree, 'l2_trigger_weight', tau2.weight_trigger)
            self.fill(self.tree, 'l2_trigger_weight_up', getattr(tau2, 'weight_trigger_up', 1.))
            self.fill(self.tree, 'l2_trigger_weight_down', getattr(tau2, 'weight_trigger_down', 1.))

        self.fill(self.tree, 'mt2',  event.mt2)
        self.fill(self.tree, 'mt2_lep',  event.mt2_lep)
        self.fill(self.tree, 'mt2_mvamet',  event.mt2_mvamet)
        self.fill(self.tree, 'mt2_rawpfmet',  event.mt2_rawpfmet)
        
        self.fill(self.tree, 'minDphiMETJets', event.minDphiMETJets)


        fired_triggers = [info.name for info in getattr(event, 'trigger_infos', []) if info.fired]

        self.fill(self.tree, 'trigger_ditau35', any('HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg_v' in name for name in fired_triggers) or isSUSY)
        self.fill(self.tree, 'trigger_ditau35_combiso', any('HLT_DoubleMediumCombinedIsoPFTau35_Trk1_eta2p1_Reg_' in name for name in fired_triggers) or isSUSY)
        self.fill(self.tree, 'trigger_singletau140', any('HLT_VLooseIsoPFTau140_Trk50_eta2p1_v' in name for name in fired_triggers) or isSUSY)
        self.fill(self.tree, 'trigger_singletau120', any('HLT_VLooseIsoPFTau120_Trk50_eta2p1_v' in name for name in fired_triggers) or isSUSY)

        matched_paths = getattr(event.diLepton, 'matchedPaths', [])
        self.fill(self.tree, 'trigger_matched_ditau35', any('HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg_v' in name for name in matched_paths) or isSUSY)
        self.fill(self.tree, 'trigger_matched_ditau35_combiso', any('HLT_DoubleMediumCombinedIsoPFTau35_Trk1_eta2p1_Reg_' in name for name in matched_paths) or isSUSY)
        self.fill(self.tree, 'trigger_matched_singletau140', any('HLT_VLooseIsoPFTau140_Trk50_eta2p1_v' in name for name in matched_paths) or isSUSY)
        self.fill(self.tree, 'trigger_matched_singletau120', any('HLT_VLooseIsoPFTau120_Trk50_eta2p1_v' in name for name in matched_paths) or isSUSY)

        if self.cfg_comp.isMC and isSUSY:
            self.fill(self.tree, 'GenSusyMScan1',  getattr(event, 'genSusyMScan1', -999.))
            self.fill(self.tree, 'GenSusyMScan2',  getattr(event, 'genSusyMScan2', -999.))
            self.fill(self.tree, 'GenSusyMScan3',  getattr(event, 'genSusyMScan3', -999.))
            self.fill(self.tree, 'GenSusyMScan4',  getattr(event, 'genSusyMScan4', -999.))
            self.fill(self.tree, 'GenSusyMNeutralino',  getattr(event, 'genSusyMNeutralino', -999.))
            self.fill(self.tree, 'GenSusyMChargino',  getattr(event, 'genSusyMChargino', -999.))
            self.fill(self.tree, 'GenSusyMStau',  getattr(event, 'genSusyMStau', -999.))
            self.fill(self.tree, 'GenSusyMStau2',  getattr(event, 'genSusyMStau2', -999.))

        
            self.fillLHEWeights(self.tree, event)

            self.fill(self.tree, 'gen_dichargino_pt', HTTGenAnalyzer.getSusySystem(event).pt())

        self.fillTree(event)
