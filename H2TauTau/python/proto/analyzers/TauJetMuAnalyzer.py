import ROOT

from PhysicsTools.HeppyCore.utils.deltar import deltaR, deltaR2

from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.Heppy.physicsobjects.Muon import Muon
from PhysicsTools.Heppy.physicsobjects.Electron import Electron
from PhysicsTools.Heppy.physicsobjects.Tau import Tau

from CMGTools.H2TauTau.proto.analyzers.DiLeptonAnalyzer import DiLeptonAnalyzer
from CMGTools.H2TauTau.proto.physicsobjects.DiObject import DirectDiTau



class TauJetMuAnalyzer(DiLeptonAnalyzer):

    # DiObjectClass = TauMuon
    LeptonClass = Muon
    OtherLeptonClass = Electron

    def declareHandles(self):
        super(TauJetMuAnalyzer, self).declareHandles()

        self.handles['taus'] = AutoHandle(
            'slimmedTaus',
            'std::vector<pat::Tau>'
        )

        self.handles['otherLeptons'] = AutoHandle(
            'slimmedElectrons',
            'std::vector<pat::Electron>'
        )

        self.handles['leptons'] = AutoHandle(
            'slimmedMuons',
            'std::vector<pat::Muon>'
        )

        self.mchandles['genParticles'] = AutoHandle(
            'prunedGenParticles',
            'std::vector<reco::GenParticle>'
        )

        self.handles['jets'] = AutoHandle(
            'slimmedJets',
            'std::vector<pat::Jet>'
            )

        self.handles['puppiMET'] = AutoHandle(
            'slimmedMETsPuppi',
            'std::vector<pat::MET>'
        )

        self.handles['pfMET'] = AutoHandle(
            'slimmedMETs',
            'std::vector<pat::MET>'
        )


    def buildDiLeptonsSingle(self, leptons, event):
        di_leptons = []
        met = self.handles['pfMET'].product()[0]
        for pat_mu in leptons:
            muon = self.__class__.LeptonClass(pat_mu)
            for i_jet, pat_jet in enumerate(self.handles['jets'].product()):
                for pat_tau in self.handles['taus'].product():
                    # Get highest-pt tau in jet cone, if any
                    if deltaR2(pat_jet.eta(), pat_jet.phi(), pat_tau.eta(), pat_tau.phi()) < 0.25:
                        pat_jet.tau = Tau(pat_tau)
                        pat_jet.tau.associatedVertex = event.goodVertices[0]
                        break

                di_tau = DirectDiTau(muon, pat_jet, met)
                di_tau.leg2().associatedVertex = event.goodVertices[0]
                di_tau.leg2().nth_jet = i_jet
                di_tau.leg1().associatedVertex = event.goodVertices[0]
                di_tau.leg1().event = event.input.object()
                di_tau.leg2().event = event.input.object()
                if not self.testLeg1(di_tau.leg1(), 99999):
                    continue

                di_tau.mvaMetSig = None
                di_leptons.append(di_tau)
        return di_leptons

    def buildLeptons(self, patLeptons, event):
        '''Build muons for veto, associate best vertex, select loose ID muons.
        The loose ID selection is done to ensure that the muon has an inner track.'''
        leptons = []
        for index, lep in enumerate(patLeptons):
            pyl = self.__class__.LeptonClass(lep)
            pyl.associatedVertex = event.goodVertices[0]
            pyl.event = event.input.object()
            leptons.append(pyl)
        return leptons

    def buildOtherLeptons(self, patOtherLeptons, event):
        '''Build electrons for third lepton veto, associate best vertex.
        '''
        otherLeptons = []
        for index, lep in enumerate(patOtherLeptons):
            pyl = self.__class__.OtherLeptonClass(lep)
            pyl.associatedVertex = event.goodVertices[0]
            pyl.rho = event.rho
            pyl.event = event.input.object()
            otherLeptons.append(pyl)
        return otherLeptons

    def process(self, event):
        # FIXME - JAN - for current 2015 sync, but shall we really discard
        # the vertex cuts?
        event.goodVertices = event.vertices

        result = super(TauJetMuAnalyzer, self).process(event)

        event.isSignal = False
        if result:
            event.isSignal = True
        
        # trying to get a dilepton from the control region.
        # it must have well id'ed and trig matched legs,
        # di-lepton and tri-lepton veto must pass
        result = self.selectionSequence(event, fillCounter=True,
                                        leg1IsoCut=self.cfg_ana.looseiso1,
                                        leg2IsoCut=self.cfg_ana.looseiso2)
        if result is False:
            # really no way to find a suitable di-lepton,
            # even in the control region
            return False

        event.pfmet = self.handles['pfMET'].product()[0]
        event.puppimet = self.handles['puppiMET'].product()[0]

        return True

    def testLeg2ID(self, tau):
        return True

    def testLeg2Iso(self, tau, isocut):
        '''if isocut is None, returns true if three-hit iso cut is passed.
        Otherwise, returns true if iso MVA > isocut.'''
        return True

    def testTauVertex(self, tau):
        '''Tests vertex constraints, for tau'''
        # Just checks if the primary vertex the tau was reconstructed with
        # corresponds to the one used in the analysis
        # isPV = abs(tau.vertex().z() - tau.associatedVertex.z()) < 0.2
        isPV = abs(tau.leadChargedHadrCand().dz()) < 0.2
        return isPV

    def testVertex(self, lepton):
        '''Tests vertex constraints, for mu'''
        return abs(lepton.dxy()) < 0.045 and abs(lepton.dz()) < 0.2

    def testLeg1ID(self, muon):
        '''Tight muon selection, no isolation requirement'''
        return muon.muonIDMoriond17() and self.testVertex(muon)

    def testLeg1Iso(self, muon, isocut):
        '''Tight muon selection, with isolation requirement'''
        if isocut is None:
            isocut = self.cfg_ana.iso2

        return muon.relIsoR(R=0.3, dBetaFactor=0.5, allCharged=False) < isocut

    def thirdLeptonVeto(self, leptons, otherLeptons, isoCut=0.3):
        # count tight muons
        vLeptons = [muon for muon in leptons if
                    muon.muonIDMoriond17() and
                    self.testVertex(muon) and
                    self.testLegKine(muon, ptcut=10, etacut=2.4) and
                    muon.relIsoR(R=0.3, dBetaFactor=0.5, allCharged=False) < 0.3]

        if len(vLeptons) > 1:
            return False

        return True


    def testElectronID(self, electron):
        return electron.mvaIDRun2('Spring16', 'POG90')

    def otherLeptonVeto(self, leptons, otherLeptons, isoCut=0.3):
        # count electrons
        vOtherLeptons = [electron for electron in otherLeptons if
                         self.testLegKine(electron, ptcut=10, etacut=2.5) and
                         self.testVertex(electron) and
                         self.testElectronID(electron) and
                         electron.passConversionVeto() and
                         electron.physObj.gsfTrack().hitPattern().numberOfHits(ROOT.reco.HitPattern.MISSING_INNER_HITS) <= 1 and
                         electron.relIsoR(R=0.3, dBetaFactor=0.5, allCharged=0) < 0.3]

        if len(vOtherLeptons) > 0:
            return False

        return True

    def leptonAccept(self, leptons, event):
        '''Di-lepton veto: returns false if >= 1 OS same flavour lepton pair,
        e.g. >= 1 OS mu pair in the mu tau channel'''
        looseLeptons = [muon for muon in leptons if
                        self.testLegKine(muon, ptcut=15, etacut=2.4) and
                        muon.isGlobalMuon() and
                        muon.isTrackerMuon() and
                        muon.isPFMuon() and
                        abs(muon.dz()) < 0.2 and
                        self.testLeg1Iso(muon, 0.3)
                        ]

        if event.leg1 not in looseLeptons:
            looseLeptons.append(event.leg1)

        if any(l.charge() > 0 for l in looseLeptons) and \
           any(l.charge() < 0 for l in looseLeptons):
            return False

        return True

    def trigMatched(self, event, diL, requireAllMatched=False):
        
        matched = super(TauJetMuAnalyzer, self).trigMatched(event, diL, requireAllMatched=requireAllMatched, ptMin=18.)

        if matched and len(diL.matchedPaths) == 1 and diL.leg1().pt() < 25. and 'IsoMu24' in list(diL.matchedPaths)[0]:
            matched = False

        return matched

    def bestDiLepton(self, diLeptons):
        '''Returns the best diLepton (1st precedence opposite-sign, 2nd precedence
        highest pt1 + pt2).'''

        if len(diLeptons) == 1:
            return diLeptons[0]

        least_iso_highest_pt = lambda dl: (dl.leg1().relIsoR(R=0.3, dBetaFactor=0.5, allCharged=0), -dl.leg1().pt(), -dl.leg2().pt())

        return sorted(diLeptons, key=lambda dil : least_iso_highest_pt(dil))[0]

