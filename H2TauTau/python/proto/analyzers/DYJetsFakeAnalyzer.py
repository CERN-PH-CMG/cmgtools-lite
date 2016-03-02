import ROOT

from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.HeppyCore.utils.deltar import bestMatch, deltaR2

from PhysicsTools.Heppy.physicsobjects.PhysicsObject import PhysicsObject
from PhysicsTools.Heppy.physicsobjects.GenParticle import GenParticle

from CMGTools.H2TauTau.proto.analyzers.TauGenTreeProducer import TauGenTreeProducer

class DYJetsFakeAnalyzer(Analyzer):

    '''Checks which kind of DYJet of Higgs event this is.
    isFake gets written to the event.
    - Z->tau tau : isFake = 0
    - Z->tau tau with matched rec hadr. tau->l: isFake = 3
    - Z->l l matched : isFake = 1
    - other : isFake = 2
    set the lepton type as leptonType in the configuration.
    In case of VH events, only the Higgs is considered.
    '''
    def declareHandles(self):
        super(DYJetsFakeAnalyzer, self).declareHandles()

        self.mchandles['genInfo'] = AutoHandle(('generator','',''), 'GenEventInfoProduct' )
        self.mchandles['genJets'] = AutoHandle('slimmedGenJets', 'std::vector<reco::GenJet>')

        self.handles['jets'] = AutoHandle(self.cfg_ana.jetCol, 'std::vector<pat::Jet>')

    def process(self, event):

        event.geninfo_tt = False
        event.geninfo_mt = False
        event.geninfo_et = False
        event.geninfo_ee = False
        event.geninfo_mm = False
        event.geninfo_em = False
        event.geninfo_EE = False
        event.geninfo_MM = False
        event.geninfo_TT = False
        event.geninfo_LL = False
        event.geninfo_mass = -99.
        event.genmet_pt = -99.
        event.genmet_eta = -99.
        event.genmet_e = -99.
        event.genmet_px = -99.
        event.genmet_py = -99.
        event.genmet_phi = -99.
        event.geninfo_has_z = False
        event.geninfo_has_w = False
        event.weight_gen = 1.

        if self.cfg_comp.isData:
            return True

        self.readCollections(event.input)
        event.genJets = self.mchandles['genJets'].product()
        event.jets = self.handles['jets'].product()

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
        self.ptSelGenSummary = [p for p in event.generatorSummary if p.pt() > ptcut and abs(p.pdgId()) not in [6, 11, 13, 15, 23, 24, 25, 35, 36, 37]]
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

        if 'Higgs' in self.cfg_comp.name:
            theZs = [bos for bos in event.generatorSummary if abs(bos.pdgId()) in (25, 35, 36, 37)]
        elif 'DY' in self.cfg_comp.name:
            theZs = [bos for bos in event.genVBosons if bos.pdgId() == 23]
        elif 'WJets' in self.cfg_comp.name:
            theZs = [bos for bos in event.genVBosons if abs(bos.pdgId()) == 24]
        else:
            return True

        # There isn't always a gen boson with Pythia 8, so gracefully return
        if len(theZs) != 1:
            # print 'WARNING: cannot find any H, W or Z in the sample'
            return True

        event.parentBoson = theZs[0]

        # check SM H associated production
        if event.parentBoson.pdgId() == 25:
            if any([bos.pdgId() == 23 for bos in event.genVBosons]):
                event.hasZ = True
            if any([abs(bos.pdgId()) == 24 for bos in event.genVBosons]):
                event.hasW = True

        # gen mass of the Higgs or Z boson
        event.geninfo_mass = event.parentBoson.mass()

        # move on if this is a W sample
        if abs(event.parentBoson.pdgId()) == 24:
            return True

        self.getGenType(event)

        return True

    def attachGenStatusFlag(self, lepton):        
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
                return DYJetsFakeAnalyzer.getFinalTau(tau.daughter(i_d))
        return tau        

    @staticmethod
    def getGenTauJets(event):
        event.genTauJets = []
        event.genTauJetConstituents = []
        for gentau in event.gentaus:
            gentau = DYJetsFakeAnalyzer.getFinalTau(gentau)

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
        # if hasattr(leg, 'genJet') and leg.genJet():
        #     if leg.genJet().pt() > 15.:
        #         dr2 = deltaR2(leg.eta(), leg.phi(), leg.genJet().eta(), leg.genJet().phi())
        #         if dr2 < best_dr2:
        #             best_dr2 = dr2
        #             leg.genp = leg.genJet()
        #             leg.genp.setPdgId(-15 * leg.genp.charge())
        #             leg.isTauHad = True

        l1match, dR2best = bestMatch(leg, event.genTauJets)
        if dR2best < best_dr2:
            best_dr2 = dR2best
            leg.genp = GenParticle(l1match)
            leg.genp.setPdgId(-15 * leg.genp.charge())
            leg.isTauHad = True

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


    def getGenType(self, event):
        '''Check the Z or H boson decay mode at gen level.
           Saves a bunch of flags in the event
           (capital e/m denotes prompt electron/muon).
           event.geninfo_tt : Z/H -> tautau -> tau_h tau_h
           event.geninfo_mt : Z/H -> tautau -> m tau_h
           event.geninfo_et : Z/H -> tautau -> e tau_h
           event.geninfo_ee : Z/H -> tautau -> ee
           event.geninfo_mm : Z/H -> tautau -> mm
           event.geninfo_em : Z/H -> tautau -> em
           event.geninfo_EE : Z/H -> ee
           event.geninfo_MM : Z/H -> mm
           event.geninfo_TT : Z/H -> tautau
           event.geninfo_LL : Z/H -> ll (ee or mm)
        '''
        # Z->TT

        h_taus = event.gentaus
        l_taus = event.gentauleps
        ls = event.genleps

        if len(l_taus) + len(h_taus) == 2:
            event.geninfo_TT = True

            # full hadronic first
            if len(h_taus) == 2:
                event.geninfo_tt = True

            # semi leptonic
            elif len(h_taus) == 1:
                if abs(l_taus[0].pdgId()) == 11:
                    event.geninfo_et = True
                if abs(l_taus[0].pdgId()) == 13:
                    event.geninfo_mt = True

            # fully leptonic
            elif len(h_taus) == 0:
                if abs(l_taus[0].pdgId()) == 11 and abs(l_taus[1].pdgId()) == 11:
                    event.geninfo_ee = True
                elif abs(l_taus[0].pdgId()) == 13 and abs(l_taus[1].pdgId()) == 13:
                    event.geninfo_mm = True
                else:
                    event.geninfo_em = True
        # Z->LL
        elif len(ls) == 2:
            event.geninfo_LL = True
            if abs(ls[0].pdgId()) == 11 and abs(ls[1].pdgId()) == 11:
                event.geninfo_EE = True
            elif abs(ls[0].pdgId()) == 13 and abs(ls[1].pdgId()) == 13:
                event.geninfo_MM = True


