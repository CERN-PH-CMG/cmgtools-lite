import ROOT

from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.Heppy.physicsobjects.PhysicsObjects import Muon
from PhysicsTools.Heppy.physicsobjects.Electron import Electron
from PhysicsTools.Heppy.physicsobjects.Tau import Tau
from PhysicsTools.HeppyCore.utils.deltar import deltaR2

from CMGTools.H2TauTau.proto.analyzers.DiLeptonAnalyzer import DiLeptonAnalyzer
from CMGTools.H2TauTau.proto.physicsobjects.DiObject import DiMuon, DirectDiTau

class MuMuAnalyzer(DiLeptonAnalyzer):

    DiObjectClass = DiMuon
    LeptonClass = Muon
    OtherLeptonClass = Electron

    def declareHandles(self):
        super(MuMuAnalyzer, self).declareHandles()
        if hasattr(self.cfg_ana, 'from_single_objects') and self.cfg_ana.from_single_objects:
            self.handles['met'] = AutoHandle(
                'slimmedMETs',
                'std::vector<pat::MET>'
            )
        else:
            self.handles['diLeptons'] = AutoHandle(
                'cmgDiMuCorSVFitFullSel',
                'std::vector<pat::CompositeCandidate>'
                )

        self.handles['otherLeptons'] = AutoHandle(
            'slimmedElectrons',
            'std::vector<pat::Electron>'
            )
        
        self.handles['leptons'] = AutoHandle(
            'slimmedMuons',
            'std::vector<pat::Muon>'
            )
        
        self.handles['taus'] = AutoHandle(
                'slimmedTaus',
                'std::vector<pat::Tau>'
            )

        self.handles['puppiMET'] = AutoHandle(
            'slimmedMETsPuppi',
            'std::vector<pat::MET>'
        )

        self.handles['pfMET'] = AutoHandle(
            'slimmedMETs',
            'std::vector<pat::MET>'
        )

        self.mchandles['genParticles'] = AutoHandle(
            'prunedGenParticles',
            'std::vector<reco::GenParticle>'
            )

    def buildDiLeptons(self, patDiLeptons, event):
        '''Build di-leptons, associate best vertex to both legs,
        select di-leptons with a tight ID muon.
        The tight ID selection is done so that dxy and dz can be computed
        (the muon must not be standalone).
        '''
        diLeptons = []
        for index, dil in enumerate(patDiLeptons):
            pydil = self.__class__.DiObjectClass(dil)
            pydil.leg1().associatedVertex = event.goodVertices[0]
            pydil.leg2().associatedVertex = event.goodVertices[0]
            pydil.leg1().event = event.input.object()
            pydil.leg2().event = event.input.object()
            if not self.testLeg2(pydil.leg2(), 99999):
                continue

            pydil.mvaMetSig = pydil.met().getSignificanceMatrix()
            diLeptons.append(pydil)
        return diLeptons

    def buildDiLeptonsSingle(self, leptons, event):
        di_leptons = []
        met = self.handles['met'].product()[0]
        for i_1, pat_muon1 in enumerate(leptons):
            muon1 = self.__class__.LeptonClass(pat_muon1)
            for i_2, pat_muon2 in enumerate(leptons):
                # Keep only pairs with pT(muon1) > pT(muon2)
                if i_2 <= i_1:
                    continue

                muon2 = self.__class__.LeptonClass(pat_muon2)
                di_tau = DirectDiTau(muon1, muon2, met)
                di_tau.leg2().associatedVertex = event.goodVertices[0]
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
        event.goodVertices = event.vertices

        result = super(MuMuAnalyzer, self).process(event, fillCounter=True)

        if result is False:
            # trying to get a dilepton from the control region.
            # it must have well id'ed and trig matched legs,
            # di-lepton and tri-lepton veto must pass
            # result = self.selectionSequence(event, fillCounter=False,
            #                                 leg1IsoCut=9999,
            #                                 leg2IsoCut=9999)
            if result is False:
                # really no way to find a suitable di-lepton,
                # even in the control region
                return False
            event.isSignal = False
        else:
            event.isSignal = True
      
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
        

    def testLeg1ID(self, muon):
        return self.testLeg2ID(muon)
        

    def testLeg1Iso(self, muon, isocut):
        return self.testLeg2Iso(muon, isocut)


    def testVertex(self, lepton):
        '''Tests vertex constraints, for mu'''
        return abs(lepton.dxy()) < 0.045 and abs(lepton.dz()) < 0.2 


    def testLeg2ID(self, muon):
        '''Tight muon selection, no isolation requirement'''
        return muon.muonIDMoriond17() and self.testVertex(muon)
               

    def testLeg2Iso(self, muon, isocut):
        '''Tight muon selection, with isolation requirement'''
        if isocut is None:
            isocut = self.cfg_ana.iso2

        return muon.relIso(0.4, dbeta_factor=0.5, all_charged=0) < isocut    

    def testElectronID(self, electron):
        return electron.mvaIDRun2('Spring16', 'POG90')

    def thirdLeptonVeto(self, leptons, otherLeptons, ptcut=10, isocut=0.3):
        '''Tri-lepton veto. Returns False if > 2 leptons (e or mu).'''
        vleptons = [lep for lep in leptons if
                    self.testLegKine(lep, ptcut=ptcut, etacut=2.4) and 
                    self.testLeg2ID(lep) and
                    self.testLeg2Iso(lep, isocut)
                   ]

        if len(vleptons)> 2:
            return False
        
        return True

    def otherLeptonVeto(self, leptons, otherLeptons, isoCut=0.3):
        # count electrons
        vOtherLeptons = [electron for electron in otherLeptons if
                         self.testLegKine(electron, ptcut=10, etacut=2.5) and
                         self.testVertex(electron) and
                         self.testElectronID(electron) and
                         electron.passConversionVeto() and
                         electron.physObj.gsfTrack().hitPattern().numberOfHits(ROOT.reco.HitPattern.MISSING_INNER_HITS) <= 1 and
                         electron.relIso(0.4, dbeta_factor=0.5, all_charged=0) < 0.3]

        if len(vOtherLeptons) > 0:
            return False

        return True

    def trigMatched(self, event, diL, requireAllMatched=False):
        
        matched = super(MuMuAnalyzer, self).trigMatched(event, diL, requireAllMatched=requireAllMatched, ptMin=18., etaMax=2.1, onlyLeg1=True)

        # if matched and len(diL.matchedPaths) == 1 and diL.leg1().pt() < 25. and 'IsoMu24' in list(diL.matchedPaths)[0]:
            # matched = False

        return matched

    def leptonAccept(self, leptons, event):
        '''Di-lepton veto: none applied for now'''
        return True

    def bestDiLepton(self, diLeptons):
        '''Returns the best diLepton (1st precedence least iso, 2nd
        precedence highest pT.'''

        if len(diLeptons) == 1:
            return diLeptons[0]

        least_iso_highest_pt = lambda dl: (dl.leg1().relIso(0.4, dbeta_factor=0.5, all_charged=0), -dl.leg1().pt(), dl.leg2().relIso(0.4, dbeta_factor=0.5, all_charged=0), -dl.leg2().pt())

        return sorted(diLeptons, key=lambda dil : least_iso_highest_pt(dil))[0]

