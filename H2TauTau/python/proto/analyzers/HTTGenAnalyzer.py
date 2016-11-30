import math
import os
import ROOT

from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.HeppyCore.utils.deltar import bestMatch

from PhysicsTools.Heppy.physicsobjects.PhysicsObject import PhysicsObject
from PhysicsTools.Heppy.physicsobjects.GenParticle import GenParticle

from CMGTools.H2TauTau.proto.analyzers.TauGenTreeProducer import TauGenTreeProducer

if "/sDYReweighting_cc.so" not in ROOT.gSystem.GetLibraries(): 
    ROOT.gROOT.ProcessLine(".L %s/src/CMGTools/H2TauTau/python/proto/plotter/DYReweighting.cc+" % os.environ['CMSSW_BASE']);
    from ROOT import getDYWeight


class HTTGenAnalyzer(Analyzer):

    '''Add generator information to hard leptons.
    '''
    def declareHandles(self):
        super(HTTGenAnalyzer, self).declareHandles()

        self.mchandles['genInfo'] = AutoHandle(('generator','',''), 'GenEventInfoProduct' )
        self.mchandles['genJets'] = AutoHandle('slimmedGenJets', 'std::vector<reco::GenJet>')
        self.mchandles['genParticles'] = AutoHandle('prunedGenParticles', 'std::vector<reco::GenParticle')

        self.handles['jets'] = AutoHandle(self.cfg_ana.jetCol, 'std::vector<pat::Jet>')

    def process(self, event):
        event.genmet_pt = -99.
        event.genmet_eta = -99.
        event.genmet_e = -99.
        event.genmet_px = -99.
        event.genmet_py = -99.
        event.genmet_phi = -99.
        event.weight_gen = 1.

        if self.cfg_comp.isData:
            return True

        self.readCollections(event.input)
        event.genJets = self.mchandles['genJets'].product()
        event.jets = self.handles['jets'].product()
        event.genParticles = self.mchandles['genParticles'].product()

        event.genleps = [p for p in event.genParticles if abs(p.pdgId()) in [11, 13] and p.statusFlags().isPrompt()]
        event.gentauleps = [p for p in event.genParticles if abs(p.pdgId()) in [11, 13] and p.statusFlags().isDirectPromptTauDecayProduct()]
        event.gentaus = [p for p in event.genParticles if abs(p.pdgId()) == 15 and p.statusFlags().isPrompt() and not any(abs(self.getFinalTau(p).daughter(i_d).pdgId()) in [11, 13] for i_d in xrange(self.getFinalTau(p).numberOfDaughters()))]
        self.getGenTauJets(event)

        event.weight_gen = self.mchandles['genInfo'].product().weight()
        event.eventWeight *= event.weight_gen

        # gen MET as sum of the neutrino 4-momenta
        neutrinos = [
            p for p in event.genParticles if abs(p.pdgId()) in (12, 14, 16) and p.status() == 1]

        genmet = ROOT.math.XYZTLorentzVectorD()
        for nu in neutrinos:
            genmet += nu.p4()

        event.genmet_pt = genmet.pt()
        event.genmet_eta = genmet.eta()
        event.genmet_e = genmet.e()
        event.genmet_px = genmet.px()
        event.genmet_py = genmet.py()
        event.genmet_phi = genmet.phi()

        ptcut = 0.
        # you can apply a pt cut on the gen leptons, electrons and muons
        # in HIG-13-004 it was 8 GeV
        if hasattr(self.cfg_ana, 'genPtCut'):
            ptcut = self.cfg_ana.genPtCut



        self.ptSelGentauleps = [lep for lep in event.gentauleps if lep.pt() > ptcut]
        self.ptSelGenleps = [lep for lep in event.genleps if lep.pt() > ptcut]
        self.ptSelGenSummary = []
        # self.ptSelGenSummary = [p for p in event.generatorSummary if p.pt() > ptcut and abs(p.pdgId()) not in [6, 11, 13, 15, 23, 24, 25, 35, 36, 37]]
        # self.ptSelGentaus    = [ lep for lep in event.gentaus    if lep.pt()
        # > ptcut ] # not needed

        self.l1 = event.diLepton.leg1()
        self.l2 = event.diLepton.leg2()

        self.genMatch(event, self.l1, self.ptSelGentauleps, self.ptSelGenleps, self.ptSelGenSummary)
        self.genMatch(event, self.l2, self.ptSelGentauleps, self.ptSelGenleps, self.ptSelGenSummary)

        self.attachGenStatusFlag(self.l1)
        self.attachGenStatusFlag(self.l2)

        if hasattr(event, 'selectedTaus'):
            for tau in event.selectedTaus:
                self.genMatch(event, tau, self.ptSelGentauleps, self.ptSelGenleps, self.ptSelGenSummary)

        if self.cfg_comp.name.find('TT') != -1 or self.cfg_comp.name.find('TTH') == -1:
            self.getTopPtWeight(event)

        if self.cfg_comp.name.find('DY') != -1:
            self.getDYMassPtWeight(event)

        return True

    @staticmethod
    def attachGenStatusFlag(lepton):        
        flag = 6

        gen_p = lepton.genp if hasattr(lepton, 'genp') else None
        # Check if we matched a generator particle and it's not a gen jet
        if gen_p and not hasattr(gen_p, 'detFlavour'):
            pdg_id = abs(gen_p.pdgId())
            if pdg_id == 15:
                if gen_p.pt() > 15.:
                    flag = 5
            elif gen_p.pt() > 8.:
                if pdg_id == 11:
                    flag = 1
                elif pdg_id == 13:
                    flag = 2
                # else:
                #     print 'Matched gen p with weird pdg ID', pdg_id

                if flag in [1, 2]:
                    if gen_p.statusFlags().isDirectPromptTauDecayProduct():
                        flag += 2
                    elif not gen_p.statusFlags().isPrompt():
                        flag = 6

        lepton.gen_match = flag


    @staticmethod
    def getFinalTau(tau):
        for i_d in xrange(tau.numberOfDaughters()):
            if tau.daughter(i_d).pdgId() == tau.pdgId():
                return HTTGenAnalyzer.getFinalTau(tau.daughter(i_d))
        return tau        

    @staticmethod
    def getGenTauJets(event):
        event.genTauJets = []
        event.genTauJetConstituents = []
        for gentau in event.gentaus:
            gentau = HTTGenAnalyzer.getFinalTau(gentau)

            c_genjet = TauGenTreeProducer.finalDaughters(gentau)
            c_genjet = [d for d in c_genjet if abs(d.pdgId()) not in [12, 14, 16]]
            p4_genjet = sum((d.p4() for d in c_genjet if abs(d.pdgId()) not in [12, 14, 16]), ROOT.math.XYZTLorentzVectorD())

            genjet = GenParticle(gentau)
            genjet.setP4(p4_genjet)

            if p4_genjet.pt() > 15.:
                event.genTauJets.append(genjet)
                event.genTauJetConstituents.append(c_genjet)


    @staticmethod
    def genMatch(event, leg, ptSelGentauleps, ptSelGenleps, ptSelGenSummary, 
                 dR=0.2, matchAll=True):

        dR2 = dR * dR

        leg.isTauHad = False
        leg.isTauLep = False
        leg.isPromptLep = False
        leg.genp = None

        best_dr2 = dR2

        # The following would work for pat::Taus, but we also want to flag a 
        # muon/electron as coming from a hadronic tau with the usual definition
        # if this happens

        # if hasattr(leg, 'genJet') and leg.genJet():
        #     if leg.genJet().pt() > 15.:
        #         dr2 = deltaR2(leg.eta(), leg.phi(), leg.genJet().eta(), leg.genJet().phi())
        #         if dr2 < best_dr2:
        #             best_dr2 = dr2
        #             leg.genp = leg.genJet()
        #             leg.genp.setPdgId(-15 * leg.genp.charge())
        #             leg.isTauHad = True
        
        # RM: needed to append genTauJets to the events,
        #     when genMatch is used as a static method
        if not hasattr(event, 'genTauJets'):
            HTTGenAnalyzer.getGenTauJets(event)

        l1match, dR2best = bestMatch(leg, event.genTauJets)
        if dR2best < best_dr2:
            best_dr2 = dR2best
            leg.genp = GenParticle(l1match)
            leg.genp.setPdgId(-15 * leg.genp.charge())
            leg.isTauHad = True
            # if not leg.genJet():
            #     print 'Warning, tau does not have matched gen tau'
            # elif leg.genJet().pt() < 15.:
            #     print 'Warning, tau has matched gen jet but with pt =', leg.genJet().pt()

        # to generated leptons from taus
        l1match, dR2best = bestMatch(leg, ptSelGentauleps)
        if dR2best < best_dr2:
            best_dr2 = dR2best
            leg.genp = l1match
            leg.isTauLep = True
            leg.isTauHad = False

        # to generated prompt leptons
        l1match, dR2best = bestMatch(leg, ptSelGenleps)
        if dR2best < best_dr2:
            best_dr2 = dR2best
            leg.genp = l1match
            leg.isPromptLep = True
            leg.isTauLep = False
            leg.isTauHad = False

        if best_dr2 < dR2:
            return

        # match with any other relevant gen particle
        if matchAll:
            l1match, dR2best = bestMatch(leg, ptSelGenSummary)
            if dR2best < best_dr2:
                leg.genp = l1match
                return

            # Ok do one more Pythia 8 trick...
            # This is to overcome that the GenAnalyzer doesn't like particles
            # that have daughters with same pdgId and status 71
            if not hasattr(event, 'pythiaQuarksGluons'):
                event.pythiaQuarksGluons = []
                for gen in event.genParticles:
                    pdg = abs(gen.pdgId())
                    status = gen.status()
                    if pdg in [1, 2, 3, 4, 5, 21] and status > 3:
                        if gen.isMostlyLikePythia6Status3():
                            event.pythiaQuarksGluons.append(gen)

            
            l1match, dR2best = bestMatch(leg, event.pythiaQuarksGluons)
            if dR2best < best_dr2:
                leg.genp = l1match
                return

            # Now this may be a pileup lepton, or one whose ancestor doesn't
            # appear in the gen summary because it's an unclear case in Pythia 8
            # To check the latter, match against jets as well...
            l1match, dR2best = bestMatch(leg, event.genJets)
            # Check if there's a gen jet with pT > 10 GeV (otherwise it's PU)
            if dR2best < dR2 and l1match.pt() > 10.:
                leg.genp = PhysicsObject(l1match)

                jet, dR2best = bestMatch(l1match, event.jets)

                if dR2best < dR2:
                    leg.genp.detFlavour = jet.partonFlavour()
                else:
                    print 'no match found', leg.pt(), leg.eta()

    @staticmethod
    def getTopPtWeight(event):
        ttbar = [p for p in event.genParticles if abs(p.pdgId()) == 6 and p.statusFlags().isLastCopy() and p.statusFlags().fromHardProcess()]

        if len(ttbar) == 2:
            top_1_pt = ttbar[0].pt()
            top_2_pt = ttbar[1].pt()

            if top_1_pt > 400:
                top_1_pt = 400.
            if top_2_pt > 400:
                top_2_pt = 400.

            topweight = math.sqrt(math.exp(0.156-0.00137*top_1_pt)*math.exp(0.156-0.00137*top_2_pt))

            event.top_1_pt = top_1_pt
            event.top_2_pt = top_2_pt
            event.topweight = topweight
            event.eventWeight *= topweight

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


    @staticmethod
    def getParentBoson(event):
        leptons_prompt = [p for p in event.genParticles if abs(p.pdgId()) in [11, 12, 13, 14] and p.fromHardProcessFinalState()]
        taus_prompt = [p for p in event.genParticles if p.statusFlags().isDirectHardProcessTauDecayProduct()]
        all = leptons_prompt + taus_prompt
        return HTTGenAnalyzer.p4sum(all)

    @staticmethod 
    def getDYMassPtWeight(event):
        if not hasattr(event, 'parentBoson'):
            event.parentBoson = HTTGenAnalyzer.getParentBoson(event)
        event.dy_weight = getDYWeight(event.parentBoson.mass(), event.parentBoson.pt())

