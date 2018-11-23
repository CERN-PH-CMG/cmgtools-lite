from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.Heppy.physicsobjects.Muon import Muon
from PhysicsTools.Heppy.physicsobjects.Electron import Electron
from PhysicsTools.Heppy.physicsobjects.Tau import Tau

from CMGTools.H2TauTau.proto.analyzers.DiLeptonAnalyzer import DiLeptonAnalyzer
from CMGTools.H2TauTau.proto.physicsobjects.DiObject import TauElectron, DirectDiTau
import ROOT


class TauEleAnalyzer(DiLeptonAnalyzer):

    DiObjectClass = TauElectron
    LeptonClass = Electron
    OtherLeptonClass = Muon

    def declareHandles(self):
        super(TauEleAnalyzer, self).declareHandles()

        if hasattr(self.cfg_ana, 'from_single_objects') and self.cfg_ana.from_single_objects:
            self.handles['taus'] = AutoHandle(
                'slimmedTaus',
                'std::vector<pat::Tau>'
            )
        else:
            self.handles['diLeptons'] = AutoHandle(
                'cmgTauEleCorSVFitFullSel',
                'std::vector<pat::CompositeCandidate>'
            )

        self.handles['otherLeptons'] = AutoHandle(
            'slimmedMuons',
            'std::vector<pat::Muon>'
        )

        self.handles['leptons'] = AutoHandle(
            'slimmedElectrons',
            'std::vector<pat::Electron>'
        )

        self.mchandles['genParticles'] = AutoHandle('prunedGenParticles',
                                                    'std::vector<reco::GenParticle>')

        self.handles['puppiMET'] = AutoHandle(
            'slimmedMETsPuppi',
            'std::vector<pat::MET>'
        )

        self.handles['pfMET'] = AutoHandle(
            'slimmedMETs',
            'std::vector<pat::MET>'
        )

    def buildDiLeptons(self, cmgDiLeptons, event):
        '''Build di-leptons, associate best vertex to both legs,
        select di-leptons with a tight ID electron.
        The electron ID selection is done so that dxy and dz can be computed
        '''
        diLeptons = []
        for index, dil in enumerate(cmgDiLeptons):
            pydil = self.__class__.DiObjectClass(dil)
            pydil.leg2().associatedVertex = event.goodVertices[0]
            pydil.leg1().associatedVertex = event.goodVertices[0]
            pydil.leg1().rho = event.rho
            pydil.leg1().event = event.input.object()
            pydil.leg2().event = event.input.object()
            pydil.mvaMetSig = pydil.met().getSignificanceMatrix()
            diLeptons.append(pydil)
        return diLeptons

    def buildDiLeptonsSingle(self, leptons, event):
        di_leptons = []
        met = self.handles['pfMET'].product()[0]
        for pat_ele in leptons:
            ele = self.__class__.LeptonClass(pat_ele)
            for pat_tau in self.handles['taus'].product():
                tau = Tau(pat_tau)
                di_tau = DirectDiTau(ele, tau, met)
                di_tau.leg2().associatedVertex = event.goodVertices[0]
                di_tau.leg1().associatedVertex = event.goodVertices[0]
                di_tau.leg1().event = event.input.object()
                di_tau.leg2().event = event.input.object()
                di_tau.leg1().rho = event.rho

                di_tau.mvaMetSig = None
                di_leptons.append(di_tau)
        return di_leptons

    def buildLeptons(self, cms_leptons, event):
        '''Build electrons for veto, associate best vertex, select loose ID electrons.
        Since the electrons are used for veto, the 0.3 default isolation cut is left there,
        as well as the pt 15 gev cut'''
        leptons = []
        for index, lep in enumerate(cms_leptons):
            pyl = self.__class__.LeptonClass(lep)
            pyl.associatedVertex = event.goodVertices[0]
            pyl.rho = event.rho
            pyl.event = event.input.object()

            if pyl.relIso(0.3, dbeta_factor=0.5, all_charged=0) > 0.3:
                continue

            leptons.append(pyl)
        return leptons

    def testMuonIDLoose(self, muon):
        '''Loose muon ID and kine, no isolation requirement, for lepton veto'''
        return muon.pt() > 15 and \
            abs(muon.eta()) < 2.4 and \
            muon.isGlobalMuon() and \
            muon.isTrackerMuon() and \
            muon.sourcePtr().userFloat('isPFMuon') and \
            abs(muon.dz()) < 0.2
        # self.testVertex( muon )

    def buildOtherLeptons(self, cmgOtherLeptons, event):
        '''Build muons for third lepton veto, associate best vertex.
        '''
        otherLeptons = []
        for index, lep in enumerate(cmgOtherLeptons):
            pyl = self.__class__.OtherLeptonClass(lep)
            pyl.associatedVertex = event.goodVertices[0]
            pyl.event = event.input.object()
            # if not self.testMuonIDLoose(pyl):
            #     continue
            otherLeptons.append(pyl)
        return otherLeptons

    def process(self, event):
        # FIXME - JAN - for current 2015 sync, but shall we really discard
        # the vertex cuts?
        event.goodVertices = event.vertices

        result = super(TauEleAnalyzer, self).process(event)

        event.isSignal = False
        if result:
            event.isSignal = True

        # trying to get a dilepton from the control region.
        # it must have well id'ed and trig matched legs,
        # and di-lepton veto must pass
        # i.e. only the iso requirement is relaxed
        result = self.selectionSequence(event, fillCounter=True,
                                        leg2IsoCut=self.cfg_ana.looseiso1,
                                        leg1IsoCut=self.cfg_ana.looseiso2)
        if result is False:
            # really no way to find a suitable di-lepton,
            # even in the control region
            return False

        event.isSignal = event.isSignal and event.leptonAccept and event.thirdLeptonVeto

        event.pfmet = self.handles['pfMET'].product()[0]
        event.puppimet = self.handles['puppiMET'].product()[0]

        return True

    def testTauVertex(self, tau):
        '''Tests vertex constraints, for tau'''
        # Just checks if the primary vertex the tau was reconstructed with
        # corresponds to the one used in the analysis
        # isPV = tau.vertex().z() == lepton.associatedVertex.z()
        isPV = abs(tau.leadChargedHadrCand().dz()) < 0.2
        return isPV

    def testVertex(self, lepton):
        '''Tests vertex constraints, for mu'''
        return abs(lepton.dxy()) < 0.045 and abs(lepton.dz()) < 0.2

    def testLeg2ID(self, tau):
        # Don't apply anti-e discriminator for relaxed tau ID
        # RIC: 9 March 2015
        return  (tau.tauID('decayModeFinding') > 0.5 and 
                abs(tau.charge()) == 1 and
                # tau.tauID('againstElectronTightMVA5')  > 0.5  and
                # tau.tauID('againstMuonLoose3')         > 0.5  and
                # (tau.zImpact() > 0.5 or tau.zImpact() < -1.5) and
                self.testTauVertex(tau))

    def testLeg2Iso(self, tau, isocut):
        '''if isocut is None, returns true if three-hit iso cut is passed.
        Otherwise, returns true if iso MVA > isocut.'''
        if isocut is None:
            return tau.tauID('byLooseCombinedIsolationDeltaBetaCorr3Hits') > 0.5
        else:
            # JAN FIXME - placeholder, as of now only used to define passing cuts
            # return tau.tauID("byIsolationMVA3newDMwLTraw") > isocut
            # RIC: 9 March 2015
            return tau.tauID("byCombinedIsolationDeltaBetaCorrRaw3Hits") < isocut

    def testTightElectronID(self, electron):
        '''Selection for electron from tau decay'''
        return electron.mvaIDRun2('Spring16', 'POG80')

    def testElectronID(self, electron):
        '''Loose selection for generic electrons'''
        return electron.mvaIDRun2('Spring16', 'POG90')

    def testVetoElectronID(self, electron):
        return electron.mvaIDRun2('Spring16', 'POG90')

    def testLeg1ID(self, electron):
        '''Tight electron selection, no isolation requirement.
        '''

        cVeto = electron.passConversionVeto()
        mHits = electron.gsfTrack().hitPattern().numberOfHits(ROOT.reco.HitPattern.MISSING_INNER_HITS) <= 1

        return self.testTightElectronID(electron) and self.testVertex(electron) and (cVeto and mHits)

    def testLeg1Iso(self, leg, isocut):  # electron
        if isocut is None:
            isocut = self.cfg_ana.iso2
        return leg.relIso(0.3, dbeta_factor=0.5, all_charged=0) < isocut

    def testLooseleg1(self, leg):  # electrons
        ''' pt, eta and isolation selection for electrons
            used in the di-electron veto.
            pt 15, eta 2.5, dB relIso 0.3
        '''
        if (leg.relIso(0.3, dbeta_factor=0.5, all_charged=0) > 0.3 or
                abs(leg.eta()) > 2.5 or
                leg.pt() < 15 or
                not self.testVetoElectronID(leg) or
                not self.testVertex(leg)):
            return False
        return True

    def testTightOtherLepton(self, muon):
        '''Tight muon selection, no isolation requirement'''
        return muon.muonIDMoriond17() and \
            self.testVertex(muon) and \
            abs(muon.eta()) < 2.4 and \
            muon.pt() > 10. and \
            muon.relIso(0.4, dbeta_factor=0.5, all_charged=0) < 0.3

    def otherLeptonVeto(self, leptons, otherLeptons, isoCut=0.3):
        # count veto muons
        vOtherLeptons = [muon for muon in otherLeptons if
                         muon.muonIDMoriond17() and
                         self.testVertex(muon) and
                         self.testLegKine(muon, ptcut=10, etacut=2.4) and
                         muon.relIso(0.4, dbeta_factor=0.5, all_charged=0) < 0.3]

        if len(vOtherLeptons) > 0:
            return False

        return True

    def thirdLeptonVeto(self, leptons, otherLeptons, isoCut=0.3):
        # count electrons
        vLeptons = [electron for electron in leptons if
                    self.testLegKine(electron, ptcut=10, etacut=2.5) and
                    self.testVertex(electron) and
                    self.testElectronID(electron) and
                    electron.relIso(0.3, dbeta_factor=0.5, all_charged=0) < 0.3]

        if len(vLeptons) > 1:
            return False

        return True

    def leptonAccept(self, leptons, event):
        '''Returns True if the additional lepton veto is successful'''
        looseLeptons = [l for l in leptons if self.testLooseleg1(l)]
        nLeptons = len(looseLeptons)

        if event.leg1 not in looseLeptons:
            looseLeptons.append(event.leg1)

        if nLeptons < 2:
            return True

        # Reject if OS
        if any(l.charge() > 0 for l in looseLeptons) and \
           any(l.charge() < 0 for l in looseLeptons):
            return False

        return True

    def bestDiLepton(self, diLeptons):
        '''Returns the best diLepton according to Andrew's prescription.'''

        if len(diLeptons) == 1:
            return diLeptons[0]

        least_iso_highest_pt = lambda dl: (dl.leg1().relIso(0.3, dbeta_factor=0.5, all_charged=0), -dl.leg1().pt(), -dl.leg2().tauID("byIsolationMVArun2v1DBoldDMwLTraw"), -dl.leg2().pt())

        return sorted(diLeptons, key=lambda dil : least_iso_highest_pt(dil))[0]

    def trigMatched(self, event, diL, requireAllMatched=False):

        matched = super(TauEleAnalyzer, self).trigMatched(event, diL, requireAllMatched=requireAllMatched, ptMin=23., relaxIds=[11])

        if matched and len(diL.matchedPaths) == 1 and diL.leg1().pt() <= 33. and 'Ele32' in list(diL.matchedPaths)[0]:
            matched = False

        return matched
