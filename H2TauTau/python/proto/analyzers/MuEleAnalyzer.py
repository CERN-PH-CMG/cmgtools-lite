from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.Heppy.physicsobjects.PhysicsObjects import Muon
from PhysicsTools.Heppy.physicsobjects.Electron import Electron
from PhysicsTools.Heppy.physicsobjects.Tau import Tau
from PhysicsTools.HeppyCore.utils.deltar import deltaR2

from CMGTools.H2TauTau.proto.analyzers.DiLeptonAnalyzer import DiLeptonAnalyzer
from CMGTools.H2TauTau.proto.physicsobjects.DiObject import MuonElectron, DirectDiTau
import ROOT


class MuEleAnalyzer(DiLeptonAnalyzer):

    DiObjectClass = MuonElectron
    LeptonClass = Electron
    OtherLeptonClass = Muon

    def declareHandles(self):
        super(MuEleAnalyzer, self).declareHandles()

        if hasattr(self.cfg_ana, 'from_single_objects') and self.cfg_ana.from_single_objects:
            self.handles['met'] = AutoHandle(
                'slimmedMETs',
                'std::vector<pat::MET>'
            )
        else:
            self.handles['diLeptons'] = AutoHandle(
                'cmgMuEleCorSVFitFullSel',
                'std::vector<pat::CompositeCandidate>'
            )

        self.handles['leptons'] = AutoHandle(
            'slimmedElectrons',
            'std::vector<pat::Electron>'
        )

        self.handles['taus'] = AutoHandle(
                'slimmedTaus',
                'std::vector<pat::Tau>'
            )

        self.handles['otherLeptons'] = AutoHandle(
            'slimmedMuons',
            'std::vector<pat::Muon>'
        )

        self.mchandles['genParticles'] = AutoHandle(
            'prunedGenParticles',
            'std::vector<reco::GenParticle>'
        )

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
        select di-leptons with a tight ID muon.
        The tight ID selection is done so that dxy and dz can be computed
        (the muon must not be standalone).
        '''
        diLeptons = []
        for index, dil in enumerate(cmgDiLeptons):
            pydil = self.__class__.DiObjectClass(dil)
            pydil.leg1().associatedVertex = event.goodVertices[0]
            pydil.leg2().associatedVertex = event.goodVertices[0]
            pydil.leg1().event = event.input.object()
            pydil.leg2().event = event.input.object()
#            pydil.leg2().rho = event.rho
            pydil.leg1().rho = event.rho
            pydil.leg1().event = event
#            if not self.testLeg2( pydil.leg2(), 999999 ):
            if not self.testLeg1(pydil.leg1(), 999999):
                continue
            # pydil.mvaMetSig = pydil.met().getSignificanceMatrix()
            diLeptons.append(pydil)
            pydil.mvaMetSig = pydil.met().getSignificanceMatrix()
        return diLeptons

    def buildDiLeptonsSingle(self, leptons, event):
        di_leptons = []
        met = self.handles['pfMET'].product()[0]

#        import pdb; pdb.set_trace()
        for pat_e in leptons:
            electron = self.__class__.LeptonClass(pat_e)
            for pat_mu in self.handles['otherLeptons'].product():
                muon = self.__class__.OtherLeptonClass(pat_mu)
                di_tau = DirectDiTau(electron, muon, met)
                di_tau.leg1().associatedVertex = event.goodVertices[0]
                di_tau.leg2().associatedVertex = event.goodVertices[0]
                di_tau.leg1().event = event.input.object()
                di_tau.leg2().event = event.input.object()
                di_tau.leg1().rho = event.rho

                if not self.testLeg1(di_tau.leg1(), 99999):
                    continue

                di_tau.mvaMetSig = None
                di_leptons.append(di_tau)
        return di_leptons

    def buildOtherLeptons(self, otherLeptons, event):
        '''Build muons for veto, associate best vertex, select loose ID muons.
        The loose ID selection is done to ensure that the muon has an inner track.'''
        muons = []
        for index, lep in enumerate(otherLeptons):
            pyl = self.__class__.OtherLeptonClass(lep)
            #pyl = Muon(lep)
            pyl.associatedVertex = event.goodVertices[0]
            pyl.event = event.input.object()
            muons.append(pyl)
        return muons

    def buildLeptons(self, leptons, event):
        '''Build electrons for third lepton veto, associate best vertex.
        '''
        electrons = []
        for index, lep in enumerate(leptons):
            pyl = self.__class__.LeptonClass(lep)
            #import pdb ; pdb.set_trace()
            #pyl = Electron(lep)
            pyl.associatedVertex = event.goodVertices[0]
            pyl.rho = event.rho
            pyl.event = event.input.object()
            electrons.append(pyl)
        return electrons

    def process(self, event):

        event.goodVertices = event.vertices

        result = super(MuEleAnalyzer, self).process(event)
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
        
      
        event.selectedTaus = [Tau(tau) for tau in self.handles['taus'].product() 
                              if tau.pt() > 18. 
                              and deltaR2(tau, event.leg1) > 0.25
                              and deltaR2(tau, event.leg2) > 0.25]

        for tau in event.selectedTaus:
            tau.associatedVertex = event.goodVertices[0]

        event.otherLeptons = event.selectedTaus[:]

        event.pfmet = self.handles['pfMET'].product()[0]
        event.puppimet = self.handles['puppiMET'].product()[0]

        return True

    def crossKinematicSelection(self, diL, event):
        return diL.leg1().pt() > self.cfg_ana.pt1_leading or diL.leg2().pt() > self.cfg_ana.pt2_leading

    def testLeg2ID(self, muon):
        '''Tight muon selection, no isolation requirement'''
        return muon.muonIDMoriond17() and self.testVertex(muon)

    def testLeg2Iso(self, muon, isocut):
        '''Muon isolation to be implemented'''
        if isocut is None:
            isocut = self.cfg_ana.iso2
        return muon.relIsoR(R=0.4, dBetaFactor=0.5, allCharged=0) < isocut

    def testVertex(self, lepton):
        '''Tests vertex constraints, for mu and electron'''
        return abs(lepton.dxy()) < 0.045 and abs(lepton.dz()) < 0.2

    def testLeg1ID(self, electron):
        '''Electron ID. To be implemented'''

        cVeto = electron.passConversionVeto()
        mHits = electron.gsfTrack().hitPattern().numberOfHits(ROOT.reco.HitPattern.MISSING_INNER_HITS) <= 1

        return self.testElectronID(electron) and self.testVertex(electron) and (cVeto and mHits)

    def testLeg1Iso(self, electron, isocut):
        '''Electron Isolation. Relative isolation, dB correction factor 0.5
        '''
        if isocut is None:
            isocut = self.cfg_ana.iso2
        return electron.relIsoR(R=0.3, dBetaFactor=0.5, allCharged=0) < isocut

    def otherLeptonVeto(self, leptons, otherLeptons, isocut=None):
        '''Second electron veto '''
        vOtherLeptons = [electron for electron in leptons if
                         self.testLegKine(electron, ptcut=10, etacut=2.5) and
                         self.testVertex(electron) and
                         electron.passConversionVeto() and 
                         electron.gsfTrack().hitPattern().numberOfHits(ROOT.reco.HitPattern.MISSING_INNER_HITS) <= 1 and
                         electron.mvaIDRun2('NonTrigSpring15MiniAOD', 'POG90') and
                         electron.relIsoR(R=0.3, dBetaFactor=0.5, allCharged=0) < 0.3]

        if len(vOtherLeptons) > 1:
            return False

        return True

    def thirdLeptonVeto(self, leptons, otherLeptons, isocut=None):
        '''Second muon veto'''
        # count tight muons
        vLeptons = [muon for muon in otherLeptons if
                    muon.muonIDMoriond17() and
                    self.testVertex(muon) and
                    self.testLegKine(muon, ptcut=10, etacut=2.4) and
                    muon.relIsoR(R=0.4, dBetaFactor=0.5, allCharged=False) < 0.3]

        if len(vLeptons) > 1:
            return False

        return True

    def testElectronID(self, electron):
        return electron.mvaIDRun2('Spring16', 'POG80')

    def leptonAccept(self, leptons, event):
        '''Loose e/mu veto to reject DY; passes for e-mu'''
        return True

    def bestDiLepton(self, diLeptons):
        '''Returns the best diLepton (1st precedence opposite-sign, 2nd precedence
        highest pt1 + pt2).'''

        if len(diLeptons) == 1:
            return diLeptons[0]

        minRelIso = min(d.leg2().relIsoR(R=0.4, dBetaFactor=0.5, allCharged=0) for d in diLeptons)

        diLeps = [dil for dil in diLeptons if dil.leg2().relIsoR(R=0.4, dBetaFactor=0.5, allCharged=0) == minRelIso]

        if len(diLeps) == 1:
            return diLeps[0]

        maxPt = max(d.leg2().pt() for d in diLeps)

        diLeps = [dil for dil in diLeps if dil.leg2().pt() == maxPt]

        if len(diLeps) == 1:
            return diLeps[0]

        minIso = min(d.leg1().relIsoR(R=0.3, dBetaFactor=0.5, allCharged=0) for d in diLeps)

        diLeps = [dil for dil in diLeps if dil.leg1().relIsoR(R=0.3, dBetaFactor=0.5, allCharged=0) == minIso]

        if len(diLeps) == 1:
            return diLeps[0]

        maxPt = max(d.leg1().pt() for d in diLeps)

        diLeps = [dil for dil in diLeps if dil.leg1().pt() == maxPt]

        if len(diLeps) != 1:
            print 'ERROR in finding best dilepton', diLeps
            import pdb
            pdb.set_trace()

        return diLeps[0]

    def trigMatched(self, event, diL, requireAllMatched=False):
        '''Check that at least one trigger object per pgdId from a given trigger 
        has a matched leg with the same pdg ID. If requireAllMatched is True, 
        requires that each single trigger object has a match.'''
        matched = False
        legs = [diL.leg1(), diL.leg2()]
        event.matchedPaths = set()

#        import pdb; pdb.set_trace()

        for info in event.trigger_infos:
            if not info.fired:
                continue

            if self.cfg_ana.verbose:
                print '[DBG] HLT_path = ', info.name

            matchedIds = set()
            allMatched = True
            for to in info.objects:

                if self.cfg_ana.verbose:
                    print '[DBG] \t match =', self.trigObjMatched(to, legs)

                    for ipath in to.pathNames(True, True):
                        print '[DBG] \t\t pathNames(True, True) = ', ipath

                    for ipath in to.pathNames(True, False):
                        print '[DBG] \t\t pathNames(True, False) = ', ipath

                    for ipath in to.pathNames(False, True):
                        print '[DBG] \t\t pathNames(False, True) = ', ipath

                    for ipath in to.pathNames(False, False):
                        print '[DBG] \t\t pathNames(False, False) = ', ipath

                    for ipath in to.filterLabels():
                        print '[DBG] \t\t filter name = ', ipath

                if self.trigObjMatched(to, legs)[0]:
                    matchedIds.add(abs(to.pdgId()))
                else:
                    allMatched = False

            if matchedIds == info.objIds:
                if requireAllMatched and not allMatched:
                    matched = False
                else:
                    matched = True
                    event.matchedPaths.add(info.name)

        Mu17_flag = any([mp.find('Mu17') != -1 for mp in event.matchedPaths])
        Ele17_flag = any([mp.find('Ele17') != -1 for mp in event.matchedPaths])

        if all([Mu17_flag, Ele17_flag]):
            return matched and (diL.leg1().pt() > 18 or diL.leg2().pt() > 18)
        elif Ele17_flag and not Mu17_flag:
            return matched and diL.leg1().pt() > 18
        elif Mu17_flag and not Ele17_flag:
            return matched and diL.leg2().pt() > 18
        else:
            print 'Found no trigger match'
            return matched
