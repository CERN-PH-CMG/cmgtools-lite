from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from CMGTools.VVResonances.tools.Pair import Pair
from CMGTools.VVResonances.tools.Singlet import Singlet
from PhysicsTools.HeppyCore.utils.deltar import *
from CMGTools.VVResonances.tools.BTagEventWeights import *
from CMGTools.VVResonances.tools.VectorBosonToolBox import VectorBosonToolBox

# import itertools
import ROOT
import os
import math


class Substructure(object):

    def __init__(self):
        pass


class Truth(object):

    def __init__(self):
        pass


class VVBuilder(Analyzer):

    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(VVBuilder, self).__init__(cfg_ana, cfg_comp, looperName)
        self.vbTool = VectorBosonToolBox()
        self.smearing = ROOT.TRandom(10101982)
        # btag reweighting
        self.btagSF = BTagEventWeights(
            'btagsf', os.path.expandvars(self.cfg_ana.btagCSVFile))
        self.subjetBtagSF0 = BTagEventWeights(
            'btagsf', os.path.expandvars(self.cfg_ana.subjetBtagCSVFile),0,[0,1,2],'incl')
        self.subjetBtagSF1 = BTagEventWeights(
            'btagsf', os.path.expandvars(self.cfg_ana.subjetBtagCSVFile),1,[0,1,2],'incl')


        puppiJecCorrWeightFile = os.path.expandvars(
            self.cfg_ana.puppiJecCorrFile)
        self.puppiJecCorr = ROOT.TFile.Open(puppiJecCorrWeightFile)
        self.puppisd_corrGEN = self.puppiJecCorr.Get("puppiJECcorr_gen")
        self.puppisd_corrRECO_cen = self.puppiJecCorr.Get(
            "puppiJECcorr_reco_0eta1v3")
        self.puppisd_corrRECO_for = self.puppiJecCorr.Get(
            "puppiJECcorr_reco_1v3eta2v5")

    def declareHandles(self):
        super(VVBuilder, self).declareHandles()
        self.handles['packed'] = AutoHandle(
            'packedPFCandidates', 'std::vector<pat::PackedCandidate>')

        if self.cfg_comp.isMC:
            self.handles['packedGen'] = AutoHandle(
                'packedGenParticles', 'std::vector<pat::PackedGenParticle>')
    def copyLV(self, LV):
        out = []
        for i in LV:
            out.append(ROOT.math.XYZTLorentzVector(
                i.px(), i.py(), i.pz(), i.energy()))
        return out


    def cleanOverlap(self, collection, toRemove):
        after = list(set(collection) - set(toRemove))
        return after


    def substructure(self, jet):
        if hasattr(jet,'softDropMassCor'):
            return

        jet.softDropMassCor = self.getPUPPIMassWeight(jet)*jet.userFloat('ak8PFJetsPuppiSoftDropMass')
        jet.softDropMassBare =jet.userFloat('ak8PFJetsPuppiSoftDropMass')

        

        jet.subJetTags = [-99.0] * 2
        jet.subJetCTagL = [-99.0] * 2
        jet.subJetCTagB = [-99.0] * 2
        jet.subJet_hadronFlavour = [-99.0] * 2
        jet.subJet_partonFlavour = [-99.0] * 2
        jet.subJet_btagWeights0 = [1.0] * 2
        jet.subJet_btagWeights1 = [1.0] * 2


        for i,o in enumerate(jet.subjets("SoftDropPuppi")):
            bTag = o.bDiscriminator(self.cfg_ana.fDiscriminatorB)+o.bDiscriminator(self.cfg_ana.fDiscriminatorBB)
            ##BTAG subject weights
            if self.cfg_comp.isMC:
                jet.subJet_btagWeights0[i]= self.subjetBtagSF0.getSF(o.pt(),
                                                o.eta(), o.hadronFlavour(), bTag)
                jet.subJet_btagWeights1[i]= self.subjetBtagSF1.getSF(o.pt(),
                                                o.eta(), o.hadronFlavour(), bTag)
            cTag = o.bDiscriminator(self.cfg_ana.fDiscriminatorC)
            lTag = o.bDiscriminator(self.cfg_ana.fDiscriminatorL)
            jet.subJetTags[i] = bTag
            jet.subJetCTagL[i] = cTag/(cTag+lTag)
            jet.subJetCTagB[i] = cTag/(cTag+bTag)
            jet.subJet_partonFlavour[i] = o.partonFlavour()
            jet.subJet_hadronFlavour[i] = o.hadronFlavour()

    def softDropRECO(self, jet,event):
        # if we already filled it exit
        if hasattr(jet, 'softDrop_low'):
            return          
        # constituents = []
        LVs = ROOT.std.vector("math::XYZTLorentzVector")()

        # we take LVs around the jets and recluster
        for p in event.packed:
            if deltaR(p.eta(), p.phi(), jet.eta(), jet.phi()) < 1.2:
                if p.puppiWeight() > 0:
                    LVs.push_back(p.p4() * p.puppiWeight())

        interface = ROOT.cmg.FastJetInterface(
            LVs, -1.0, 0.8, 1, 0.01, 5.0, 4.4)
        # make jets
        interface.makeInclusiveJets(50.0)
        outputJets = interface.get(True)
        if len(outputJets) == 0:
            return
        interface.softDrop(True, 0, 0.0, 0.15, 0.8)
        jet.softDrop_high = self.getPUPPIMassWeight(jet)*self.copyLV(interface.get(False))[0].mass()
        interface = ROOT.cmg.FastJetInterface(
            LVs, -1.0, 0.8, 1, 0.01, 5.0, 4.4)
        interface.makeInclusiveJets(50.0)
        outputJets = interface.get(True)
        interface.softDrop(True, 0, 0.0, 0.05, 0.8)
        jet.softDrop_low = self.getPUPPIMassWeight(jet)*self.copyLV(interface.get(False))[0].mass()



    def softDropGen(self, jet,event):
        # if we already filled it exit
        if hasattr(jet, 'genSoftDrop') or not self.cfg_comp.isMC:
            return          
        # constituents = []
        LVs = ROOT.std.vector("math::XYZTLorentzVector")()

        # we take LVs around the jets and recluster
        for p in event.genPacked:
            if p.status() == 1 and p.pt() > 0.05 and not (abs(p.pdgId()) in [12, 14, 16]):
                if deltaR(p.eta(), p.phi(), jet.eta(), jet.phi()) < 1.2:
                    LVs.push_back(p.p4())
        interface = ROOT.cmg.FastJetInterface(
            LVs, -1.0, 0.8, 1, 0.01, 5.0, 4.4)
        # make jets
        interface.makeInclusiveJets(50.0)
        outputJets = interface.get(True)
        if len(outputJets) == 0:
            return

        jet.genJetP4 = ROOT.Candidate.LorentzVector(outputJets[0].px(),outputJets[0].py(),outputJets[0].pz(),outputJets[0].energy())

        # OK!Now save the area
        interface.softDrop(True, 0, 0.0, 0.1, 0.8)
        jet.genSoftDrop = self.copyLV(interface.get(False))[0]




    def topology(self, VV, jets, leptons):
        VV.otherLeptons = leptons
        VV.satteliteJets = jets
        # VBF Tag
        if len(jets) > 1:
            VV.vbfDEta = abs(jets[0].eta() - jets[1].eta())
            VV.vbfMass = (jets[0].p4() + jets[1].p4()).M()
        else:
            VV.vbfDEta = -999
            VV.vbfMass = -999

        # Btags
        jetsCentral = filter(lambda x: abs(x.eta()) < 2.4, jets)

        VV.satteliteCentralJets = jetsCentral
        # cuts are taken from
        # https://twiki.cern.ch/twiki/bin/view/CMS/BtagRecommendation94X
        # (20.06.2016)
        VV.nLooseBTags = len(filter(lambda x: x.bDiscriminator(self.cfg_ana.fDiscriminatorB)+
                                    x.bDiscriminator(self.cfg_ana.fDiscriminatorBB)> 0.1522, jetsCentral))
        VV.nMediumBTags =len(filter(lambda x: x.bDiscriminator(self.cfg_ana.fDiscriminatorB)+
                                    x.bDiscriminator(self.cfg_ana.fDiscriminatorBB)> 0.4941, jetsCentral)) 
        VV.nTightBTags = len(filter(lambda x: x.bDiscriminator(self.cfg_ana.fDiscriminatorB)+
                                    x.bDiscriminator(self.cfg_ana.fDiscriminatorBB)> 0.8001, jetsCentral)) 
        VV.nOtherLeptons = len(leptons)

        maxbtag = -100.0

        VV.btagWeight = 1.0
        for j in jetsCentral:
            btag = j.bDiscriminator(self.cfg_ana.fDiscriminatorB)+j.bDiscriminator(self.cfg_ana.fDiscriminatorBB)
            flavor = j.hadronFlavour()

            # btag event weight
            if self.cfg_comp.isMC:
                VV.btagWeight *= self.btagSF.getSF(j.pt(),
                                                   j.eta(), flavor, btag)

            # and systematics
            if btag > maxbtag:
                maxbtag = btag
        VV.highestEventBTag = maxbtag

    def selectJets(self, jets, func, otherObjects, DR, otherObjects2=None, DR2=0.0):
        output = []
        for j in jets:
            if not func(j):
                continue
            overlap = False
            for o in otherObjects:
                dr = deltaR(j.eta(), j.phi(), o.eta(), o.phi())
                if dr < DR:
                    overlap = True
                    break
            if otherObjects2 is not None:
                for o in otherObjects2:
                    dr = deltaR(j.eta(), j.phi(), o.eta(), o.phi())
                    if dr < DR2:
                        overlap = True
                        break
            if not overlap:
                output.append(j)
        return output

    def makeWV(self, event):
        output = []

        # loop on the leptons
        looseLeptonsForW = filter(lambda x: (abs(x.pdgId()) == 11 and x.heepID) or (
            abs(x.pdgId()) == 13 and x.highPtIDIso), event.selectedLeptons)
        tightLeptonsForW = filter(lambda x: (abs(x.pdgId()) == 11 and x.heepID and x.pt() > 55) or (
            abs(x.pdgId()) == 13 and x.highPtIDIso and x.pt() > 55), event.selectedLeptons)

        if len(tightLeptonsForW) == 0:
            return output

        # make leptonic W
        W = self.vbTool.makeW(tightLeptonsForW, event.met)
        if len(W) == 0:
            return output

        bestW = max(W, key=lambda x: x.leg1.pt())
        # now the jets, use lower pT cut since we'll recluster
        fatJets = self.selectJets(event.jetsAK8, lambda x: x.pt() > 200.0 and abs(
            x.eta()) < 2.4 and x.jetID('POG_PFID_Tight'), tightLeptonsForW, 1.0)
        if len(fatJets) == 0:
            return output
        bestJet = max(fatJets, key=lambda x: x.pt())
        self.substructure(bestJet)
        self.softDropRECO(bestJet,event)
        VV = Pair(bestW, bestJet)
        if deltaR(bestW.leg1.eta(), bestW.leg1.phi(), bestJet.eta(), bestJet.phi()) < ROOT.TMath.Pi() / 2.0:
            return output
        if VV.deltaPhi() < 2.0:
            return output
        if abs(deltaPhi(bestW.leg2.phi(), bestJet.phi())) < 2.0:
            return output


        if self.cfg_comp.isMC:
            self.softDropGen(bestJet,event)

            if not hasattr(bestJet,'genJetP4'):
                VV.genPartialMass = -1
            else:
                newMET = event.met.p4() + VV.leg2.p4() - VV.leg2.genJetP4
                newMET.SetPz(0.0)
                newW = Pair(VV.leg1.leg1, Singlet(newMET))
                self.vbTool.defaultWKinematicFit(newW)
                VV.genPartialMass = ( VV.leg1.p4() + VV.leg2.genJetP4 ).M()
        else:
            VV.genPartialMass = -1

        # topology
        satteliteJets = self.selectJets(event.jets, lambda x: x.pt() > 30.0 and x.jetID(
            'POG_PFID_Tight'), tightLeptonsForW, 0.4, [bestJet], 0.8)
        otherLeptons = self.cleanOverlap(looseLeptonsForW, [bestW.leg1])
        self.topology(VV, satteliteJets, otherLeptons)

        output.append(VV)
        return output

    def makeZV(self, event):
        output = []

        # loop on the leptons
        leptonsForZ = filter(lambda x: (abs(x.pdgId()) == 11 and x.heepIDNoIso) or (
            abs(x.pdgId()) == 13 and (x.highPtID or x.highPtTrackID)), event.selectedLeptons)

        if len(leptonsForZ) < 2:
            return output

        # make leptonic Z
        Z = self.vbTool.makeZ(leptonsForZ)
        if len(Z) == 0:
            return output
        bestZ = max(Z, key=lambda x: x.pt())

        # other higbn pt isolated letpons in the event
        otherGoodLeptons = self.cleanOverlap(
            leptonsForZ, [bestZ.leg1, bestZ.leg2])
        otherTightLeptons = filter(lambda x: (abs(x.pdgId()) == 11 and x.heepID) or (
            abs(x.pdgId()) == 13 and (x.highPtIDIso)), otherGoodLeptons)
        # now the jets
        fatJets = self.selectJets(event.jetsAK8, lambda x: x.pt() > 200.0 and abs(
            x.eta()) < 2.4 and x.jetID('POG_PFID_Tight'), [bestZ.leg1, bestZ.leg2], 1.0)
        if len(fatJets) == 0:
            return output
        bestJet = max(fatJets, key=lambda x: x.pt())
        self.substructure(bestJet)
        self.softDropRECO(bestJet,event)
        VV = Pair(bestZ, bestJet)

        if self.cfg_comp.isMC:
            self.softDropGen(bestJet,event)
            VV.genPartialMass = (VV.leg1.p4() + VV.leg2.genJet().p4()).M()
        else:
            VV.genPartialMass = -1

        satteliteJets = self.selectJets(event.jets, lambda x: x.pt() > 30.0 and x.jetID(
            'POG_PFID_Tight'), otherTightLeptons, 0.4, [bestJet], 0.8)
        self.topology(VV, satteliteJets, otherTightLeptons)
        output.append(VV)
        return output

    def makeMETV(self, event):
        output = []

        # loop on the leptons
        leptons = filter(lambda x: (abs(x.pdgId()) == 11 and x.heepID) or (
            abs(x.pdgId()) == 13 and x.highPtIDIso), event.selectedLeptons)
        fatJets = self.selectJets(event.jetsAK8, lambda x: x.pt() > 200.0 and abs(
            x.eta()) < 2.4 and x.jetID('POG_PFID_Tight'), leptons, 1.0)

        if len(fatJets) < 1:
            return output

        self.substructure(fatJets[0])
        self.softDropRECO(fatJets[0],event)

        VV = Pair(event.met, fatJets[0])

        # kinematics
        if VV.deltaPhi() < 2.0 or VV.leg1.pt() < 200:
            return output

        if self.cfg_comp.isMC:
            self.softDropGen(fatJets[0],event)
            VVGEN = Pair(event.met,Singlet(VV.leg2.genJet().p4()))
            VV.genPartialMass = VVGEN.mt()
        else:
            VV.genPartialMass = -1
            
        # topology
        satteliteJets = self.selectJets(event.jets, lambda x: x.pt() > 30.0 and x.jetID(
            'POG_PFID_Tight'), leptons, 0.3, [VV.leg2], 0.8)
        self.topology(VV, satteliteJets, leptons)
        output.append(VV)
        return output

    def getPUPPIMassWeight(self, puppijet):
        # mass correction for PUPPI following
        # https://github.com/thaarres/PuppiSoftdropMassCorr

        genCorr = 1.
        recoCorr = 1.
        # corrections only valid up to |eta| < 2.5, use 1. beyond
        if (abs(puppijet.eta()) < 2.5):
            genCorr = self.puppisd_corrGEN.Eval(puppijet.pt())
            if (abs(puppijet.eta()) <= 1.3):
                recoCorr = self.puppisd_corrRECO_cen.Eval(puppijet.pt())
            else:
                recoCorr = self.puppisd_corrRECO_for.Eval(puppijet.pt())
        totalWeight = genCorr * recoCorr
        return totalWeight

    def fillTopPtReweighting(self, event, truth):
        """Top pT reweighting."""
        if not self.cfg_comp.isMC:
            truth.genTop_weight = 1.
            return truth

        ttbar = [p for p in event.genParticles if abs(p.pdgId()) == 6 and p.statusFlags(
        ).isLastCopy() and p.statusFlags().fromHardProcess()]

        if self.cfg_comp.name.find('TT') != -1 and self.cfg_comp.name.find('TTH') == -1 and len(ttbar) == 2:
            # store also individual pTs for later correction
            truth.genTop_1_pt = ttbar[0].pt()
            truth.genTop_2_pt = ttbar[1].pt()
            top_1_pt = truth.genTop_1_pt
            top_2_pt = truth.genTop_2_pt
            # only valid up to 400 GeV, assume constant afterwards
            if top_1_pt > 400:
                top_1_pt = 400.
            if top_2_pt > 400:
                top_2_pt = 400.
            # see
            # https://twiki.cern.ch/twiki/bin/view/CMS/TopSystematics#pt_top_Reweighting
            truth.genTop_weight = math.sqrt(
                math.exp(0.0615 - 0.0005 * top_1_pt) * math.exp(0.0615 - 0.0005 * top_2_pt))
        else:
            truth.genTop_weight = 1.
        return truth

    @staticmethod
    def p4sum(ps):
        '''Returns four-vector sum of objects in passed list. Returns None
        if empty. Note that python sum doesn't work since p4() + 0/None fails,
        but will be possible in future python'''
        if not ps:
            return None
        p4 = ps[0].p4()
        for i in xrange(len(ps) - 1):
            p4 += ps[i + 1].p4()
        return p4

    def getParentBoson(self, event):
        """Get generator level boson (last in chain) for correct kinematics."""
        # if we already filled it exit
        if hasattr(event, 'genBoson') or not self.cfg_comp.isMC:
            return
        leptons_prompt = [p for p in event.genParticles if abs(
            p.pdgId()) in [11, 12, 13, 14] and p.fromHardProcessFinalState()]
        taus_prompt = [p for p in event.genParticles if p.statusFlags(
        ).isDirectHardProcessTauDecayProduct()]
        all = leptons_prompt + taus_prompt
        genBoson = VVBuilder.p4sum(all)
        return genBoson

    def makeTruthType(self, event):
        """create truth collection."""
        truth = Truth()
        genBoson = self.getParentBoson(event)
        truth = self.fillTopPtReweighting(event, truth)
        if genBoson:
            truth.genBoson = genBoson
        return [truth]

    def process(self, event):
        self.readCollections(event.input)

        # if MC create the stable particles for Gen Jet reco and substructure
        event.genParticleLVs = ROOT.std.vector("math::XYZTLorentzVector")()

        if self.cfg_comp.isMC:
            event.genPacked = self.handles['packedGen'].product()
        event.packed = self.handles['packed'].product()


        LNuJJ = self.makeWV(event)
        LLJJ = [] #self.makeZV(event)
        JJNuNu = [] #self.makeMETV(event)
        TruthType = self.makeTruthType(event)

        setattr(event, 'LNuJJ' + self.cfg_ana.suffix, LNuJJ)
        setattr(event, 'LLJJ' + self.cfg_ana.suffix, LLJJ)
        setattr(event, 'JJNuNu' + self.cfg_ana.suffix, JJNuNu)
        setattr(event, 'TruthType' + self.cfg_ana.suffix, TruthType)
