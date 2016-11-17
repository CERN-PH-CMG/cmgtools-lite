import array
import ROOT

from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.HeppyCore.utils.deltar import deltaPhi

import PhysicsTools.HeppyCore.framework.config as cfg

from ROOT.heppy import Hemisphere
from ROOT.heppy import ReclusterJets

from ROOT.heppy import Davismt2
davismt2 = Davismt2()

from ROOT.heppy import mt2w_bisect
mt2wSNT = mt2w_bisect.mt2w()


class MT2Analyzer(Analyzer):

    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(MT2Analyzer, self).__init__(cfg_ana, cfg_comp, looperName)
        self.jetPt = cfg_ana.jetPt

    def declareHandles(self):
        super(MT2Analyzer, self).declareHandles()
       # genJets
        self.handles['genJets'] = AutoHandle('slimmedGenJets', 'std::vector<reco::GenJet>')
        self.handles['met'] = AutoHandle(self.cfg_ana.metCollection, 'std::vector<pat::MET>')

    def beginLoop(self, setup):
        super(MT2Analyzer, self).beginLoop(setup)
        self.counters.addCounter('pairs')
        count = self.counters.counter('pairs')
        count.register('all events')

    def computeMT2(self, visaVec, visbVec, metVec):

        metVector = array.array('d', [0., metVec.px(), metVec.py()])
        visaVector = array.array('d', [0., visaVec.px(), visaVec.py()])
        visbVector = array.array('d', [0., visbVec.px(), visbVec.py()])

        davismt2.set_momenta(visaVector, visbVector, metVector)
        davismt2.set_mn(0)

        return davismt2.get_mt2()

    def getMT2AKT(self, event, TMPobjects40jc, met, collectionPostFix, postFix):
        '''get hemispheres via AntiKT -1 antikt, 1 kt, 0 CA'''
        if len(TMPobjects40jc) >= 2:

            objects = ROOT.std.vector(ROOT.reco.Particle.LorentzVector)()
            for jet in TMPobjects40jc:
                objects.push_back(jet.p4())

            hemisphereViaKt = ReclusterJets(objects, 1., 50.0)
            groupingViaKt = hemisphereViaKt.getGroupingExclusive(2)

            if len(groupingViaKt) >= 2:
                setattr(event, "pseudoViaKtJet1"+collectionPostFix+postFix, ROOT.reco.Particle.LorentzVector(groupingViaKt[0]))
                setattr(event, "pseudoViaKtJet2"+collectionPostFix+postFix, ROOT.reco.Particle.LorentzVector(groupingViaKt[1]))
                setattr(event, "mt2ViaAKt"+collectionPostFix+postFix,
                        self.computeMT2(getattr(event, 'pseudoViaKtJet1'+collectionPostFix+postFix), getattr(event, 'pseudoViaKtJet2'+collectionPostFix+postFix), met))
                return self.computeMT2(getattr(event, 'pseudoViaKtJet1'+collectionPostFix+postFix), getattr(event, 'pseudoViaKtJet2'+collectionPostFix+postFix), met)

            if not self.cfg_ana.doOnlyDefault:
                hemisphereViaAKt = ReclusterJets(objects, -1., 50.0)
                groupingViaAKt = hemisphereViaAKt.getGroupingExclusive(2)

                if len(groupingViaAKt) >= 2:
                    setattr(event, "pseudoViaAKtJet1"+collectionPostFix+postFix, ROOT.reco.Particle.LorentzVector(groupingViaAKt[0]))
                    setattr(event, "pseudoViaAKtJet2"+collectionPostFix+postFix, ROOT.reco.Particle.LorentzVector(groupingViaAKt[1]))
                    setattr(event, "mt2ViaAKt"+collectionPostFix+postFix,
                            self.computeMT2(getattr(event, 'pseudoViaAKtJet1'+collectionPostFix+postFix), getattr(event, 'pseudoViaAKtJet2'+collectionPostFix+postFix), met))
                    return self.computeMT2(getattr(event, 'pseudoViaAKtJet1'+collectionPostFix+postFix), getattr(event, 'pseudoViaAKtJet2'+collectionPostFix+postFix), met)

    def getMT2Hemi(self, event, TMPobjects40jc, met, collectionPostFix, postFix):

        if len(TMPobjects40jc) >= 2:

            pxvec = ROOT.std.vector(float)()
            pyvec = ROOT.std.vector(float)()
            pzvec = ROOT.std.vector(float)()
            Evec = ROOT.std.vector(float)()
            grouping = ROOT.std.vector(int)()

            for jet in TMPobjects40jc:
                pxvec.push_back(jet.px())
                pyvec.push_back(jet.py())
                pzvec.push_back(jet.pz())
                Evec.push_back(jet.energy())

            hemisphere = Hemisphere(pxvec, pyvec, pzvec, Evec, 2, 3)
            grouping = hemisphere.getGrouping()

            pseudoJet1px = 0
            pseudoJet1py = 0
            pseudoJet1pz = 0
            pseudoJet1energy = 0
            multPSJ1 = 0

            pseudoJet2px = 0
            pseudoJet2py = 0
            pseudoJet2pz = 0
            pseudoJet2energy = 0
            multPSJ2 = 0

            for index in range(0, len(pxvec)):
                if(grouping[index] == 1):
                    pseudoJet1px += pxvec[index]
                    pseudoJet1py += pyvec[index]
                    pseudoJet1pz += pzvec[index]
                    pseudoJet1energy += Evec[index]
                    multPSJ1 += 1
                if(grouping[index] == 2):
                    pseudoJet2px += pxvec[index]
                    pseudoJet2py += pyvec[index]
                    pseudoJet2pz += pzvec[index]
                    pseudoJet2energy += Evec[index]
                    multPSJ2 += 1

            pseudoJet1pt2 = pseudoJet1px*pseudoJet1px + pseudoJet1py*pseudoJet1py
            pseudoJet2pt2 = pseudoJet2px*pseudoJet2px + pseudoJet2py*pseudoJet2py

            if pseudoJet1pt2 >= pseudoJet2pt2:
                setattr(event, "pseudoJet1"+collectionPostFix+postFix, ROOT.reco.Particle.LorentzVector(pseudoJet1px, pseudoJet1py, pseudoJet1pz, pseudoJet1energy))
                setattr(event, "pseudoJet2"+collectionPostFix+postFix, ROOT.reco.Particle.LorentzVector(pseudoJet2px, pseudoJet2py, pseudoJet2pz, pseudoJet2energy))
                setattr(event, "multPseudoJet1"+collectionPostFix+postFix, multPSJ1)
                setattr(event, "multPseudoJet2"+collectionPostFix+postFix, multPSJ2)
            else:
                setattr(event, "pseudoJet2"+collectionPostFix+postFix, ROOT.reco.Particle.LorentzVector(pseudoJet1px, pseudoJet1py, pseudoJet1pz, pseudoJet1energy))
                setattr(event, "pseudoJet1"+collectionPostFix+postFix, ROOT.reco.Particle.LorentzVector(pseudoJet2px, pseudoJet2py, pseudoJet2pz, pseudoJet2energy))
                setattr(event, "multPseudoJet1"+collectionPostFix+postFix, multPSJ2)
                setattr(event, "multPseudoJet2"+collectionPostFix+postFix, multPSJ1)
            
            mt2 = self.computeMT2(getattr(event, 'pseudoJet1'+collectionPostFix+postFix), getattr(event, 'pseudoJet2'+collectionPostFix+postFix), met)
            setattr(event, "mt2"+collectionPostFix+postFix, mt2)
            return mt2

    def makeMT2(self, event):
        #        print '==> INSIDE THE PRINT MT2'
        #        print 'MET=',event.met.pt()

        met = ROOT.pat.MET(self.handles['met'].product()[0])

        setattr(event, "mt2"+self.cfg_ana.collectionPostFix+"_lep", -999)

        event.selectedLeptons = [event.leg1, event.leg2]
        self.mt2_lep = self.getMT2Hemi(event, event.selectedLeptons, met, self.cfg_ana.collectionPostFix, "_lep")

        mva_met = event.diLepton.met()

        self.mt2_lep = self.getMT2Hemi(event, event.selectedLeptons, mva_met, self.cfg_ana.collectionPostFix, "_lep_mvamet")

    def calculateSUSYVars(self, event):
        met = ROOT.pat.MET(self.handles['met'].product()[0])
        mva_met = event.diLepton.met()

        event.minDphiMETJets = min(deltaPhi(met.phi(), jet.phi()) for jet in event.cleanJets30) if event.cleanJets30 else -999.
        event.minDphiMVAMETJets = min(deltaPhi(mva_met.phi(), jet.phi()) for jet in event.cleanJets30)if event.cleanJets30 else -999.

        



    def process(self, event):
        self.readCollections(event.input)

        event.mt2bb = -999
        event.mt2bb_Xj = -999
        event.mt2lept = -999

        event.multPseudoJet1_had = 0
        event.multPseudoJet2_had = 0

        event.multPseudoJet1_Xj_had = 0
        event.multPseudoJet2_Xj_had = 0

        ###

        self.makeMT2(event)
        self.calculateSUSYVars(event)

        # print 'variables computed: MT=', event.mtw, 'MT2=', event.mt2, 'MT2W=', event.mt2w
        # print 'pseudoJet1 px=', event.pseudoJet1.px(), ' py=', event.pseudoJet1.py(), ' pz=', event.pseudoJet1.pz()
        # print 'pseudoJet2 px=', event.pseudoJet2.px(), ' py=', event.pseudoJet2.py(), ' pz=', event.pseudoJet2.pz()

        return True


setattr(MT2Analyzer, "defaultConfig", cfg.Analyzer(
    class_object=MT2Analyzer,
    metCollection="slimmedMETs",
    collectionPostFix="",
    doOnlyDefault=True,
)
)
