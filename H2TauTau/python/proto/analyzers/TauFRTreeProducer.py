import ROOT

from PhysicsTools.Heppy.physicsutils.TauDecayModes import tauDecayModes
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.Heppy.physicsobjects.PhysicsObjects import Jet

from CMGTools.H2TauTau.proto.analyzers.H2TauTauTreeProducerBase import H2TauTauTreeProducerBase

from CMGTools.H2TauTau.proto.analyzers.HTTGenAnalyzer import HTTGenAnalyzer

from PhysicsTools.HeppyCore.utils.deltar import deltaR2

class TauFRTreeProducer(H2TauTauTreeProducerBase):
    ''' Tree producer for tau POG study.
    '''

    def __init__(self, *args):
        super(TauFRTreeProducer, self).__init__(*args)

    def declareHandles(self):
        super(TauFRTreeProducer, self).declareHandles()

        if self.cfg_comp.isMC:
            self.mchandles['genJets'] = AutoHandle('slimmedGenJets', 'std::vector<reco::GenJet>')
        # self.handles['puppi_met'] = AutoHandle('slimmedMETsPuppi', 'std::vector<pat::MET>')
        self.handles['pfmet'] = AutoHandle('slimmedMETs', 'std::vector<pat::MET>')

    def declareVariables(self, setup):
        self.bookEvent(self.tree)
        self.bookDiLepton(self.tree, fill_svfit=False)
        self.bookExtraMetInfo(self.tree)

        self.bookJet(self.tree, 'oriJet')
        self.var(self.tree, 'jet_nth', int)
        self.var(self.tree, 'jet_nooverlap', int)
        self.var(self.tree, 'jet_corrJECUp')
        self.var(self.tree, 'jet_corrJECDown')
        self.var(self.tree, 'jet_corr')
        self.bookJet(self.tree, 'jet')
        self.bookTau(self.tree, 'tau')
        self.bookMuon(self.tree, 'muon')
        self.bookGenParticle(self.tree, 'tau_gen')
        self.bookGenParticle(self.tree, 'tau_gen_vis')
        self.var(self.tree, 'tau_gen_decayMode')

        self.bookGenInfo(self.tree)
        
        self.declareJetMETVars()


    def declareJetMETVars(self):
        self.var(self.tree, 'genmet_pt')
        self.var(self.tree, 'genmet_phi')

        self.var(self.tree, 'pfmet_pt')
        self.var(self.tree, 'pfmet_phi')

        # self.var(self.tree, 'puppimet_pt')
        # self.var(self.tree, 'puppimet_phi')

        self.var(self.tree, 'nbjets20')
        self.var(self.tree, 'nbjets20up')
        self.var(self.tree, 'nbjets20down')

        self.var(self.tree, 'njets30')
        self.var(self.tree, 'njets30up')
        self.var(self.tree, 'njets30down')        

        self.var(self.tree, 'njets30clean')
        self.var(self.tree, 'njets30cleanup')
        self.var(self.tree, 'njets30cleandown')

    def fillJetMETVars(self, event):
        genmet = ROOT.math.XYZTLorentzVectorD()
        if self.cfg_comp.isMC:
            neutrinos = [
                p for p in event.genParticles if abs(p.pdgId()) in (12, 14, 16)]
            
            for nu in neutrinos:
                genmet += nu.p4()

        self.fill(self.tree, 'genmet_pt', genmet.pt())
        self.fill(self.tree, 'genmet_phi', genmet.phi())

        met = self.handles['pfmet'].product()[0]
        self.fill(self.tree, 'pfmet_pt', met.pt())
        self.fill(self.tree, 'pfmet_phi', met.phi())

        # puppimet = self.handles['puppi_met'].product()[0]
        # self.fill(self.tree, 'puppimet_pt', puppimet.pt())
        # self.fill(self.tree, 'puppimet_phi', puppimet.phi())

        self.fill(self.tree, 'nbjets20', len([j for j in event.bJets if j.pt() > 20.]))
        self.fill(self.tree, 'nbjets20up', len([j for j in event.bJets if j.pt()*j.corrJECUp/j.corr > 20.]))
        self.fill(self.tree, 'nbjets20down', len([j for j in event.bJets if j.pt()*j.corrJECDown/j.corr > 20.]))

        self.fill(self.tree, 'njets30', len([j for j in event.jets if j.pt() > 30.]))
        self.fill(self.tree, 'njets30up', len([j for j in event.jets if j.pt()*j.corrJECUp/j.corr > 30.]))
        self.fill(self.tree, 'njets30down', len([j for j in event.jets if j.pt()*j.corrJECDown/j.corr > 30.]))

        self.fill(self.tree, 'njets30clean', len([j for j in event.cleanJets if j.pt() > 30.]))
        self.fill(self.tree, 'njets30cleanup', len([j for j in event.cleanJets if j.pt()*j.corrJECUp/j.corr > 30.]))
        self.fill(self.tree, 'njets30cleandown', len([j for j in event.cleanJets if j.pt()*j.corrJECDown/j.corr > 30.]))

    def process(self, event):
        # needed when doing handle.product(), goes back to
        # PhysicsTools.Heppy.analyzers.core.Analyzer
        self.readCollections(event.input)

        if not eval(self.skimFunction):
            return False


        ptSelGentauleps = []
        ptSelGenleps = []
        ptSelGenSummary = []


        if self.cfg_comp.isMC:
            event.genJets = self.mchandles['genJets'].product()

            ptcut = 8.
            ptSelGentauleps = [lep for lep in event.gentauleps if lep.pt() > ptcut]
            ptSelGenleps = [lep for lep in event.genleps if lep.pt() > ptcut]
            ptSelGenSummary = [p for p in event.generatorSummary if p.pt() > ptcut and abs(p.pdgId()) not in [6, 23, 24, 25, 35, 36, 37]]


        for i_dil, dil in enumerate(event.selDiLeptons):
            
            muon = dil.leg1()
            jet = dil.leg2()
            found = False
            for corr_jet in event.jets:
                if deltaR2(jet.eta(), jet.phi(), corr_jet.eta(), corr_jet.phi()) < 0.01:
                    pt = max(corr_jet.pt(), corr_jet.pt() * corr_jet.corrJECUp/corr_jet.corr, corr_jet.pt() * corr_jet.corrJECDown/corr_jet.corr)
                    if pt < 20.:
                        continue
                    found = True

            if not found:
                continue



            tau = jet.tau if hasattr(jet, 'tau') else None
            if self.cfg_comp.isMC:
                if tau:
                    HTTGenAnalyzer.genMatch(event, tau, ptSelGentauleps,
                                                ptSelGenleps, ptSelGenSummary)
                    HTTGenAnalyzer.attachGenStatusFlag(tau)
                HTTGenAnalyzer.genMatch(event, muon, ptSelGentauleps,
                                            ptSelGenleps, ptSelGenSummary)
                HTTGenAnalyzer.attachGenStatusFlag(muon)

            self.tree.reset()
            self.fillEvent(self.tree, event)
            self.fillDiLepton(self.tree, event.diLepton, fill_svfit=False)
            self.fillExtraMetInfo(self.tree, event)
            self.fillGenInfo(self.tree, event)

            self.fillJetMETVars(event)
            self.fillMuon(self.tree, 'muon', muon)
            jet = Jet(jet)
            jet.btagMVA = jet.btag('pfCombinedInclusiveSecondaryVertexV2BJetTags')
            jet.btagFlag = jet.btagMVA > 0.8
            self.fillJet(self.tree, 'oriJet', jet)
            self.fill(self.tree, 'jet_nth', i_dil)

            for corr_jet in event.jets:
                if deltaR2(jet.eta(), jet.phi(), corr_jet.eta(), corr_jet.phi()) < 0.01:
                    self.fillJet(self.tree, 'jet', corr_jet)
                    self.fill(self.tree, 'jet_nooverlap', True if corr_jet in event.cleanJets else False)
                    self.fill(self.tree, 'jet_corrJECUp', corr_jet.corrJECUp/corr_jet.corr)
                    self.fill(self.tree, 'jet_corrJECDown', corr_jet.corrJECDown/corr_jet.corr)
                    self.fill(self.tree, 'jet_corr', corr_jet.corr)

            if tau:
                self.fillTau(self.tree, 'tau', tau)

                if hasattr(tau, 'genp') and tau.genp:
                    self.fillGenParticle(self.tree, 'tau_gen', tau.genp)
                    if tau.genJet():
                        self.fillGenParticle(self.tree, 'tau_gen_vis', tau.genJet())
                        self.fill(self.tree, 'tau_gen_decayMode', tauDecayModes.genDecayModeInt(tau.genJet()))

            self.fillTree(event)
