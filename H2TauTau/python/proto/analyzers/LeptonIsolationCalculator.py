from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer

from PhysicsTools.HeppyCore.utils.deltar import deltaR

from ROOT import heppy


class LeptonIsolationCalculator(Analyzer):

    '''Calculates different muon isolation values'''

    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(LeptonIsolationCalculator, self).__init__(cfg_ana, cfg_comp, looperName)

    def attachPuppiIso(self, muon, puppi, weight_func='puppiWeight', name='puppi'):
        puppi_iso_pt = []
        puppi_iso_pt_04 = []
        puppi_iso_pt_03 = []
        muon_eta = muon.eta()
        muon_phi = muon.phi()

        for c_p in puppi:
            pdgId = c_p.pdgId()

            if abs(pdgId) not in [22, 130, 211]:
                continue

            pt = c_p.pt() * getattr(c_p, weight_func)()
            eta = c_p.eta()
            phi = c_p.phi()
            # Neutral hadrons or photons
            inner_cone = 0.01
            if abs(pdgId) in [211]:
                inner_cone = 0.0001
            elif pt < 0.5:
                continue

            if abs(muon_eta - eta) < 0.5:
                dr = deltaR(eta, phi, muon_eta, muon_phi)
                if inner_cone < dr:
                    if dr < 0.5:
                        puppi_iso_pt.append(pt)
                    if dr < 0.4:
                        puppi_iso_pt_04.append(pt)
                    if dr < 0.3:
                        puppi_iso_pt_03.append(pt)


        setattr(muon, name+'_iso_pt', sum(puppi_iso_pt))
        setattr(muon, name+'_iso04_pt', sum(puppi_iso_pt_04))
        setattr(muon, name+'_iso03_pt', sum(puppi_iso_pt_03))

    def attachEffectiveArea(self, lep, name):

        if name in ['muon', 'Muon']:
            aeta = abs(lep.eta())
            if   aeta < 0.800: lep.EffectiveArea03 = 0.0735
            elif aeta < 1.300: lep.EffectiveArea03 = 0.0619
            elif aeta < 2.000: lep.EffectiveArea03 = 0.0465
            elif aeta < 2.200: lep.EffectiveArea03 = 0.0433
            else:              lep.EffectiveArea03 = 0.0577

        elif name in ['electron', 'Electron']:
            sceta = abs(lep.superCluster().eta())

            if   sceta < 1.000: lep.EffectiveArea03 = 0.1752
            elif sceta < 1.479: lep.EffectiveArea03 = 0.1862
            elif sceta < 2.000: lep.EffectiveArea03 = 0.1411
            elif sceta < 2.200: lep.EffectiveArea03 = 0.1534
            elif sceta < 2.300: lep.EffectiveArea03 = 0.1903
            elif sceta < 2.400: lep.EffectiveArea03 = 0.2243
            else:              lep.EffectiveArea03 = 0.2687
            lep.EffectiveArea04 = 0.0

        else:
            print 'not supportive lepton type. please choose [muon, electron]'


            

    def attachMiniIsolation(self, mu):
        mu.miniIsoR = 10.0/min(max(mu.pt(), 50), 200)
        # -- version with increasing cone at low pT, gives slightly better performance for tight cuts and low pt leptons
        # mu.miniIsoR = 10.0/min(max(mu.pt(), 50),200) if mu.pt() > 20 else 4.0/min(max(mu.pt(),10),20)
        what = "mu" if (abs(mu.pdgId()) == 13) else ("eleB" if mu.isEB() else "eleE")
        if what == "mu":
            mu.miniAbsIsoCharged = self.IsolationComputer.chargedAbsIso(mu.physObj, mu.miniIsoR, {"mu": 0.0001, "eleB": 0, "eleE": 0.015}[what], 0.0)
        else:
            mu.miniAbsIsoCharged = self.IsolationComputer.chargedAbsIso(
                mu.physObj, mu.miniIsoR, {"mu": 0.0001, "eleB": 0, "eleE": 0.015}[what], 0.0, self.IsolationComputer.selfVetoNone)
        if what == "mu":
            mu.miniAbsIsoNeutral = self.IsolationComputer.neutralAbsIsoRaw(mu.physObj, mu.miniIsoR, 0.01, 0.5)
        else:
            mu.miniAbsIsoPho = self.IsolationComputer.photonAbsIsoRaw(mu.physObj, mu.miniIsoR, 0.08 if what == "eleE" else 0.0, 0.0, self.IsolationComputer.selfVetoNone)
            mu.miniAbsIsoNHad = self.IsolationComputer.neutralHadAbsIsoRaw(mu.physObj, mu.miniIsoR, 0.0, 0.0, self.IsolationComputer.selfVetoNone)
            mu.miniAbsIsoNeutral = mu.miniAbsIsoPho + mu.miniAbsIsoNHad

        if self.miniIsolationPUCorr == "rhoArea":
            mu.miniAbsIsoNeutral = max(0.0, mu.miniAbsIsoNeutral - mu.rho * mu.EffectiveArea03 * (mu.miniIsoR/0.3)**2)
        elif self.miniIsolationPUCorr != 'raw':
            raise RuntimeError, "Unsupported miniIsolationCorr name '" + \
                str(self.cfg_ana.miniIsolationCorr) + "'! For now only 'rhoArea', 'deltaBeta', 'raw', 'weights' are supported (and 'weights' is not tested)."

        mu.miniAbsIso = mu.miniAbsIsoCharged + mu.miniAbsIsoNeutral
        mu.miniRelIso = mu.miniAbsIso/mu.pt()

    def declareHandles(self):

        super(LeptonIsolationCalculator, self).declareHandles()
        self.handles['pf'] = AutoHandle('packedPFCandidates', 'std::vector<pat::PackedCandidate>')

        self.getter = self.cfg_ana.getter if hasattr(self.cfg_ana, 'getter') else lambda event: event.selectedTaus
        self.lepton = self.cfg_ana.lepton if hasattr(self.cfg_ana, 'lepton') else 'muon'

        self.IsolationComputer = heppy.IsolationComputer()
        self.miniIsolationPUCorr = 'rhoArea'

    def beginLoop(self, setup):
        print self, self.__class__
        super(LeptonIsolationCalculator, self).beginLoop(setup)

    def process(self, event):
        self.readCollections(event.input)

        pf_cands = self.handles['pf'].product()
        self.IsolationComputer.setPackedCandidates(pf_cands)
        for lep in [event.diLepton.leg1(), event.diLepton.leg2()]:
            self.IsolationComputer.addVetos(lep.physObj)

        for lepton in self.getter(event):
            lepton.rho = event.rho
            self.attachEffectiveArea(lepton, self.lepton)
            self.attachMiniIsolation(lepton)
            self.attachPuppiIso(lepton, pf_cands, 'puppiWeight')
            self.attachPuppiIso(lepton, pf_cands, 'puppiWeightNoLep', 'puppi_no_lepton')

        return True
