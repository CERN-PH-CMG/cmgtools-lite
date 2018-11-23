import os
import ROOT
from PhysicsTools.HeppyCore.utils.deltar import deltaR
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.Heppy.physicsobjects.PhysicsObjects import Tau, Muon
from PhysicsTools.Heppy.physicsobjects.Electron import Electron

from CMGTools.H2TauTau.proto.analyzers.DiLeptonAnalyzer import DiLeptonAnalyzer
from CMGTools.H2TauTau.proto.physicsobjects.DiObject import TauTau, DirectTauTau
from CMGTools.H2TauTau.proto.analyzers.HTTGenAnalyzer import HTTGenAnalyzer


class TauTauAnalyzer(DiLeptonAnalyzer):

    DiObjectClass = TauTau
    LeptonClass = Electron
    OtherLeptonClass = Muon
  
    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(TauTauAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)

    def declareHandles(self):
        super(TauTauAnalyzer, self).declareHandles()
        if hasattr(self.cfg_ana, 'from_single_objects') and self.cfg_ana.from_single_objects:
            self.handles['taus'] = AutoHandle('slimmedTaus', 'std::vector<pat::Tau>')
        else:
            self.handles['diLeptons'] = AutoHandle('cmgDiTauCorSVFitFullSel', 'std::vector<pat::CompositeCandidate>')

        self.handles['leptons'] = AutoHandle(
            'slimmedElectrons', 
            'std::vector<pat::Electron>'
        )
        
        self.handles['otherLeptons'] = AutoHandle(
            'slimmedMuons', 
            'std::vector<pat::Muon>'
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

        self.handles['l1IsoTau'] = AutoHandle( 
            ('l1extraParticles', 'IsoTau'), 
            'std::vector<l1extra::L1JetParticle>'   
        )

    def process(self, event):

        # method inherited from parent class DiLeptonAnalyzer
        # asks for at least on di-tau pair
        # applies the third lepton veto
        # tests leg1 and leg2
        # cleans by dR the two signal leptons
        # applies the trigger matching to the two signal leptons
        # choses the best di-tau pair, with the bestDiLepton method
        # as implemented here
        event.goodVertices = event.vertices

        result = super(TauTauAnalyzer, self).process(event)

        event.isSignal = False
        if result:
            event.isSignal = True
        # trying to get a dilepton from the control region.
        # it must have well id'ed and trig matched legs,
        # di-lepton and tri-lepton veto must pass
        result = self.selectionSequence(event,
                                        fillCounter=True,
                                        leg1IsoCut=self.cfg_ana.looseiso1,
                                        leg2IsoCut=self.cfg_ana.looseiso2)

        if result is False:
            # really no way to find a suitable di-lepton,
            # even in the control region
            return False
        
        if not (hasattr(event, 'leg1') and hasattr(event, 'leg2')):
            return False

        if hasattr(event, 'calibratedPfMet'):
            event.pfmet = event.calibratedPfMet
        else:
            event.pfmet = self.handles['pfMET'].product()[0]

        if hasattr(event, 'calibratedPuppiMet'):
            event.puppimet = event.calibratedPuppiMet
        else:
            event.puppimet = self.handles['puppiMET'].product()[0]

        if getattr(self.cfg_ana, 'scaleTaus', False):
            self.scaleMet(event, event.diLepton)

        return True

    def buildDiLeptons(self, cmgDiLeptons, event):
        '''Build di-leptons, associate best vertex to both legs.'''
        diLeptons = []
        for index, dil in enumerate(cmgDiLeptons):
            pydil = TauTau(dil, iso=self.cfg_ana.isolation)
            pydil.leg1().associatedVertex = event.goodVertices[0]
            pydil.leg2().associatedVertex = event.goodVertices[0]
            pydil.leg1().event = event.input.object()
            pydil.leg2().event = event.input.object()
            diLeptons.append(pydil)
            pydil.mvaMetSig = pydil.met().getSignificanceMatrix()
            if getattr(self.cfg_ana, 'scaleTaus', False):
                for leg in [pydil.leg1(), pydil.leg2()]:
                    HTTGenAnalyzer.genMatch(event, leg, event.ptSelGentauleps, event.ptSelGenleps, event.ptSelGenSummary)
                    HTTGenAnalyzer.attachGenStatusFlag(leg)
                    self.scaleP4(leg, self.cfg_ana.tes_scale)

        return diLeptons

    def buildDiLeptonsSingle(self, leptons, event):
        '''
        '''
        di_objects = []
        
        if hasattr(event, 'calibratedTaus'):
            taus = event.calibratedTaus
        else:
            taus = self.handles['taus'].product()
        
        if hasattr(event, 'calibratedPfMet'):
            met = event.calibratedPfMet
        else:
            met = self.handles['pfMET'].product()[0]
        
        taus = [Tau(tau) for tau in taus]

        if getattr(self.cfg_ana, 'scaleTaus', False):
            for tau in taus:
                HTTGenAnalyzer.genMatch(event, tau, event.ptSelGentauleps, event.ptSelGenleps, event.ptSelGenSummary)
                HTTGenAnalyzer.attachGenStatusFlag(tau)
                self.scaleP4(tau, self.cfg_ana.tes_scale)

        for leg1 in taus:
            for leg2 in taus:
                if leg1 != leg2:
                    di_tau = DirectTauTau(leg1, leg2, met)
                    di_tau.leg2().associatedVertex = event.goodVertices[0]
                    di_tau.leg1().associatedVertex = event.goodVertices[0]
                    di_tau.leg1().event = event.input.object()
                    di_tau.leg2().event = event.input.object()
                    di_tau.mvaMetSig = None
                    di_objects.append(di_tau)
        return di_objects

    def buildOtherLeptons(self, cmgLeptons, event):
        '''Build muons for veto, associate best vertex, select loose ID muons.
        The loose ID selection is done to ensure that the muon has an inner track.'''
        leptons = []
        for index, lep in enumerate(cmgLeptons):
            pyl = Muon(lep)
            pyl.associatedVertex = event.goodVertices[0]
            pyl.event = event.input.object()
            if not pyl.muonIDMoriond17():
                continue
            if not pyl.relIso(0.4, dbeta_factor=0.5, all_charged=0) < 0.3:
                continue
            if not self.testLegKine(pyl, ptcut=10, etacut=2.4):
                continue
            leptons.append(pyl)
        return leptons

    def buildLeptons(self, cmgOtherLeptons, event):
        '''Build electrons for third lepton veto, associate best vertex.'''
        otherLeptons = []
        for index, lep in enumerate(cmgOtherLeptons):
            pyl = Electron(lep)
            pyl.associatedVertex = event.goodVertices[0]
            pyl.rho = event.rho
            pyl.event = event.input.object()
            if not pyl.mvaIDRun2('Spring16', 'POG90'):
                continue
            if not pyl.relIso(0.3, dbeta_factor=0.5, all_charged=0) < 0.3:
                continue
            if not self.testLegKine(pyl, ptcut=10, etacut=2.5):
                continue
            otherLeptons.append(pyl)
        return otherLeptons

    def testLeg(self, leg, leg_pt, leg_eta, iso, isocut):
        '''requires loose isolation, pt, eta and minimal tauID cuts'''
        # RIC: relaxed
        return (abs(leg.charge()) == 1 and  # RIC: ensure that taus have abs(charge) == 1
                self.testTauVertex(leg) and
                leg.tauID(iso) < isocut and
                leg.pt() > leg_pt and
                abs(leg.eta()) < leg_eta and
                leg.tauID('decayModeFinding') > 0.5)

    def testLeg1(self, leg, isocut):
        leg_pt = self.cfg_ana.pt1
        leg_eta = self.cfg_ana.eta1
        iso = self.cfg_ana.isolation
        return self.testLeg(leg, leg_pt, leg_eta, iso, isocut)

    def testLeg2(self, leg, isocut):
        leg_pt = self.cfg_ana.pt2
        leg_eta = self.cfg_ana.eta2
        iso = self.cfg_ana.isolation
        return self.testLeg(leg, leg_pt, leg_eta, iso, isocut)

    def testTauVertex(self, tau):
        '''Tests vertex constraints, for tau'''
        # Just checks if the primary vertex the tau was reconstructed with
        # corresponds to the one used in the analysis
        # isPV = abs(tau.vertex().z() - tau.associatedVertex.z()) < 0.2
        isPV = abs(tau.leadChargedHadrCand().dz()) < 0.2
        return isPV

    def testVertex(self, lepton, dxy=0.045, dz=0.2):
        '''Tests vertex constraints, for mu, e and tau'''
        return abs(lepton.dxy()) < dxy and \
            abs(lepton.dz()) < dz

    def otherLeptonVeto(self, electrons, muons, isocut=None):
        '''Second electron veto '''
        return len(electrons) == 0

    def thirdLeptonVeto(self, electrons, muons, isocut=None):
        '''Second muon veto'''
        return len(muons) == 0

    def trigMatched(self, event, diL, requireAllMatched=False):
        matched = super(TauTauAnalyzer, self).trigMatched(event, diL, requireAllMatched=requireAllMatched)

        # Not needed in 2016, for the moment
        
        # if not self.l1Matched(event, diL):
        #     matched = False

        return matched

    def l1Matched(self, event, diL):
        '''Additional L1 matching for 2015 trigger bug.'''
        allMatched = True

        l1objs = self.handles['l1IsoTau'].product()

        for leg in [diL.leg1(), diL.leg2()]:
            legMatched = False
            bestDR = 0.5
            for l1 in l1objs:
                if l1.pt() < 28.:
                    continue
                dR = deltaR(l1.eta(), l1.phi(), leg.eta(), leg.phi())
                if dR < bestDR:
                    legMatched = True
                    bestDR = dR
                    leg.L1 = l1
            if not legMatched:
                allMatched = False
                break

        if allMatched and diL.leg1().L1 == diL.leg2().L1:
            allMatched = False

        return allMatched

    def bestDiLepton(self, diLeptons):
        '''Returns the best diLepton (1st precedence highest pT,
        2nd precedence most isolated).'''
        # osDiLeptons = [dl for dl in diLeptons if dl.leg1().charge() != dl.leg2().charge()]
        # least_iso_highest_pt = lambda dl : min((dl.leg1().tauID(self.cfg_ana.isolation), -dl.leg1().pt()), (dl.leg2().tauID(self.cfg_ana.isolation), -dl.leg2().pt()))

        # least_iso_highest_pt = lambda dl: (-dl.leg1().tauID(self.cfg_ana.isolation), -dl.leg1().pt(), -dl.leg2().tauID(self.cfg_ana.isolation), -dl.leg2().pt())

        least_iso_highest_pt = lambda dl: (-dl.leg1().tauID(self.cfg_ana.isolation) - dl.leg2().tauID(self.cfg_ana.isolation), -dl.leg1().pt() - dl.leg2().pt())

        # def id3(tau,X):
        #     """Create an integer equal to 1-2-3 for (loose,medium,tight)"""
        #     return tau.tauID(X%"Loose") + tau.tauID(X%"Medium") + tau.tauID(X%"Tight")
        # def id5(tau,X):
        #     """Create an integer equal to 1-2-3-4-5 for (very loose, 
        #         loose, medium, tight, very tight)"""
        #     return id3(tau, X) + tau.tauID(X%"VLoose") + tau.tauID(X%"VTight")
        # def id6(tau,X):
        #     """Create an integer equal to 1-2-3-4-5-6 for (very loose, 
        #         loose, medium, tight, very tight, very very tight)"""
        #     return id5(tau, X) + tau.tauID(X%"VVTight")

        # iso_string = self.cfg_ana.isolation.replace('raw', '').replace('byIso', 'by%sIso')

        # least_iso_highest_pt = lambda dl: (-id6(dl.leg1(), iso_string) - id6(dl.leg2(), iso_string), -dl.leg1().pt(), -dl.leg2().pt())

        # highest_pt_least_iso = lambda dl: (-dl.leg1().pt(), -dl.leg1().tauID(self.cfg_ana.isolation), -dl.leg2().pt(), -dl.leg2().tauID(self.cfg_ana.isolation))


        # set reverse = True in case the isolation changes to MVA
        # in that case the least isolated is the one with the lowest MVAscore
        # if osDiLeptons : return sorted(osDiLeptons, key=lambda dl : least_iso(dl), reverse=False)[0]
        # else           :

        return sorted(diLeptons, key=lambda dl: least_iso_highest_pt(dl), reverse=False)[0]

    def scaleP4(self, tau, scale):
        if tau.gen_match != 5:
            return

        deltaMet = ROOT.LorentzVector(tau.p4())
        modifiedP4 = ROOT.TLorentzVector()

        modifiedP4.SetPtEtaPhiM(
            tau.pt() * scale,
            tau.eta(),
            tau.phi(),
            tau.mass() # do not scale mass
        )
        
        # I love ROOT
        modifiedP4LV = ROOT.LorentzVector(
            modifiedP4.Px(),
            modifiedP4.Py(),
            modifiedP4.Pz(),
            modifiedP4.E(),
        )
        
        tau.setP4(modifiedP4LV)
        deltaMet -= tau.p4()
        tau.deltaMet = deltaMet

    def scaleMet(self, event, diLep):
       
        pfmet = event.pfmet
        puppimet = event.pfmet
        met = diLep.met()

        taus =[diLep.leg1(), diLep.leg2()]

        for tau in taus:
            if not hasattr(tau, 'deltaMet'):
                # tau wasn't scaled
                continue
            pfmetP4    = pfmet.p4()
            puppimetP4 = puppimet.p4()
            metP4      = met.p4()
            # remove pre-calibrated tau from met computation
            pfmetP4    += tau.deltaMet
            puppimetP4 += tau.deltaMet
            metP4      += tau.deltaMet
        
            pfmet.setP4(pfmetP4)
            puppimet.setP4(puppimetP4)
            met.setP4(metP4)
                    
        return True
