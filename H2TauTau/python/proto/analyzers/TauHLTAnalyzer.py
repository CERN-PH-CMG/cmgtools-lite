from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.physicsobjects.Tau import Tau

from PhysicsTools.HeppyCore.utils.deltar import deltaR
from CMGTools.H2TauTau.proto.analyzers.HTTGenAnalyzer import HTTGenAnalyzer

class TauHLTAnalyzer(Analyzer):

    '''Gets tau decay mode efficiency weight and puts it in the event'''

    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(TauHLTAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)

    def declareHandles(self):

        super(TauHLTAnalyzer, self).declareHandles()
        self.handles['rho'] = AutoHandle(
            ('fixedGridRhoFastjetAll', '', 'RECO'),
            'double'
            )

        self.handles['taus'] = AutoHandle(
            ('hpsPFTauProducer', '', 'RECO'),
            'std::vector<reco::PFTau>'
        )

        self.handles['DM'] = AutoHandle(
            ('hpsPFTauDiscriminationByDecayModeFindingNewDMs', '', 'RECO'),
            'reco::PFTauDiscriminator'
        )

        self.handles['looseDBIso'] = AutoHandle(
            ('hpsPFTauDiscriminationByLooseCombinedIsolationDBSumPtCorr3Hits', '', 'RECO'),
            'reco::PFTauDiscriminator'
        )

        self.handles['genParticles'] = AutoHandle(
            'genParticles',
            'std::vector<reco::GenParticle>')

        self.handles['hlt_taus'] = AutoHandle(
            ('hltHpsPFTauProducer', '', 'TEST'),
            'std::vector<reco::PFTau>',
            lazy=False,
            mayFail=True,
            disableAtFirstFail=False
        )

        self.handles['hltDM'] = AutoHandle(
            ('hltHpsPFTauDiscriminationByDecayModeFindingNewDMs', '', 'TEST'),
            'reco::PFTauDiscriminator',
            lazy=False,
            mayFail=True,
            disableAtFirstFail=False
        )

        self.handles['hltLooseDB'] = AutoHandle(
            ('hltHpsPFTauDiscriminationByLooseCombinedIsolationDBSumPtCorr3Hits', '', 'TEST'),
            'reco::PFTauDiscriminator',
            lazy=False,
            mayFail=True,
            disableAtFirstFail=False
        )

        self.handles['hltSingle_taus'] = AutoHandle(
            ('hltHpsPFTauProducerSingleTau', '', 'TEST'),
            'std::vector<reco::PFTau>',
            lazy=False,
            mayFail=True,
            disableAtFirstFail=False
        )

        self.handles['hltSingleDM'] = AutoHandle(
            ('hltHpsPFTauDiscriminationByDecayModeFindingNewDMsSingleTau', '', 'TEST'),
            'reco::PFTauDiscriminator',
            lazy=False,
            mayFail=True,
            disableAtFirstFail=False
        )

        self.handles['hltSingleLooseDB'] = AutoHandle(
            ('hltHpsPFTauDiscriminationByLooseCombinedIsolationDBSumPtCorr3HitsSingleTau', '', 'TEST'),
            'reco::PFTauDiscriminator',
            lazy=False,
            mayFail=True,
            disableAtFirstFail=False
        )

        self.handles['pfCandidates'] = AutoHandle(
            ('particleFlow', '', 'RECO'),
            'std::vector<reco::PFCandidate>'
        )

        self.handles['hltPfCandidates'] = AutoHandle(
            ('hltParticleFlowReg', '', 'TEST'),
            'std::vector<reco::PFCandidate>',
            lazy=False,
            mayFail=True,
            disableAtFirstFail=False
        )

        self.handles['hltSinglePfCandidates'] = AutoHandle(
            ('hltParticleFlowForTaus', '', 'TEST'),
            'std::vector<reco::PFCandidate>',
            lazy=False,
            mayFail=True,
            disableAtFirstFail=False
        )

    def beginLoop(self, setup):
        print self, self.__class__
        super(TauHLTAnalyzer, self).beginLoop(setup)

    def process(self, event):
        self.readCollections(event.input)

        event.rho = self.handles['rho'].product()[0]

        event.taus = [Tau(tau) for tau in self.handles['taus'].product()]
        dms = self.handles['DM'].product() 
        loose_db_isos = self.handles['looseDBIso'].product()

        if len(event.taus) != len(dms) or len(event.taus) != len(loose_db_isos):
            import pdb; pdb.set_trace()

        for i_tau, tau in enumerate(event.taus):
            tau.dm = dms.value(i_tau)
            tau.loose_db_iso = loose_db_isos.value(i_tau)
            if tau.dm > 1:
                import pdb; pdb.set_trace()

        event.hlt_taus = []
        if self.handles['hlt_taus'].isValid():
            event.hlt_taus = [Tau(tau) for tau in self.handles['hlt_taus'].product()]

        if event.hlt_taus:
            hlt_dms = self.handles['hltDM'].product() 
            hlt_loose_db_isos = self.handles['hltLooseDB'].product()
            for i_tau, tau in enumerate(event.hlt_taus):
                tau.dm = hlt_dms.value(i_tau)
                tau.loose_db_iso = hlt_loose_db_isos.value(i_tau)
        else:
            # print self.handles['hlt_taus']._exception
            if self.handles['hlt_taus']._exception is None:
                import pdb; pdb.set_trace()


        event.hlt_single_taus = []
        if self.handles['hltSingle_taus'].isValid():
            event.hlt_single_taus = [Tau(tau) for tau in self.handles['hltSingle_taus'].product()]

        if event.hlt_single_taus:
            hlt_dms = self.handles['hltSingleDM'].product() 
            hlt_loose_db_isos = self.handles['hltSingleLooseDB'].product()
            for i_tau, tau in enumerate(event.hlt_single_taus):
                tau.dm = hlt_dms.value(i_tau)
                tau.loose_db_iso = hlt_loose_db_isos.value(i_tau)
        else:
            # print self.handles['hlt_taus']._exception
            if self.handles['hltSingle_taus']._exception is None:
                import pdb; pdb.set_trace()


        event.genParticles = self.handles['genParticles'].product()

        event.genleps = [p for p in event.genParticles if abs(p.pdgId()) in [11, 13] and p.statusFlags().isPrompt()]
        event.gentauleps = [p for p in event.genParticles if abs(p.pdgId()) in [11, 13] and p.statusFlags().isDirectPromptTauDecayProduct()]
        event.gentaus = [p for p in event.genParticles if abs(p.pdgId()) == 15 and p.statusFlags().isPrompt() and not any(abs(HTTGenAnalyzer.getFinalTau(p).daughter(i_d).pdgId()) in [11, 13] for i_d in xrange(HTTGenAnalyzer.getFinalTau(p).numberOfDaughters()))]

        def addInfo(tau, cands=None, maxDeltaR=None):
            HTTGenAnalyzer.genMatch(event, tau, event.gentauleps, event.genleps, [], 
                 dR=0.2, matchAll=True)
            self.tauIsoBreakdown(tau, cands, maxDeltaR=maxDeltaR)
            tau.nphotons = sum(1 for cand in TauHLTAnalyzer.tauFilteredPhotons(tau))

        pfCandidates = self.handles['pfCandidates'].product()
        hltPfCandidates = self.handles['hltPfCandidates'].product() if self.handles['hltPfCandidates'].isValid() else None
        hltSinglePfCandidates = self.handles['hltSinglePfCandidates'].product() if self.handles['hltSinglePfCandidates'].isValid() else None

        for tau in event.taus:
            addInfo(tau, [c for c in pfCandidates if abs(c.pdgId()) == 211], maxDeltaR=0.8)

        for tau in event.hlt_taus :
            addInfo(tau, [c for c in hltPfCandidates if abs(c.pdgId()) == 211], maxDeltaR=0.5)

        for tau in event.hlt_single_taus:
            addInfo(tau, [c for c in hltSinglePfCandidates if abs(c.pdgId()) == 211], maxDeltaR=0.5)

        return True


    @staticmethod
    def tauChargedFilteredIso(tau, minDeltaZ=-1., maxDeltaZ=0.2, maxTrackChi2=100., maxTransverseImpactParameter=0.03, minTrackHits=3, minTrackPt=0.5, cands=None, maxDeltaR=None):
        
        if not cands:
            cands = [cand.get() for cand in tau.isolationPFChargedHadrCands()]
        pv = tau.vertex()
        filteredCands = []
        for cand in cands:
            if maxDeltaR:
                # Speed up
                if abs(cand.eta() - tau.eta()) > maxDeltaR or abs(cand.phi() - tau.phi()) > maxDeltaR:
                    continue
                if deltaR(tau, cand) > maxDeltaR:
                    continue

            # print 'deltaR:', deltaR(tau, cand)


            if not cand.trackRef().isAvailable():
                print 'Track not avaialble for PF candidate with ID', cand.pdgId()
                continue
            track = cand.trackRef().get()

            if TauHLTAnalyzer.filterTrack(track, pv, minDeltaZ, maxDeltaZ, maxTrackChi2, maxTransverseImpactParameter, minTrackHits, minTrackPt):
                continue

            filteredCands.append(cand)
        return filteredCands

    @staticmethod
    def filterTrack(track, pv, minDeltaZ=-1., maxDeltaZ=0.2, maxTrackChi2=100., maxTransverseImpactParameter=0.03, minTrackHits=3, minTrackPt=0.5,):
        return (track.pt() < minTrackPt
                or track.normalizedChi2() > maxTrackChi2
                or track.hitPattern().numberOfValidHits() < minTrackHits
                or abs(track.dz(pv)) > maxDeltaZ
                or abs(track.dz(pv)) < minDeltaZ
                or abs(track.dxy(pv)) > maxTransverseImpactParameter)

    @staticmethod
    def tauPhotonsOutsideSignalCone(tau):
        filteredCands = []
        signalConeSize = tau.signalConeSize()
        for c in tau.signalPFGammaCands():
            if deltaR(tau, c) > signalConeSize:
                filteredCands.append(c)
        return filteredCands

    @staticmethod
    def tauFilteredPhotons(tau, minPt=0.5, maxDR=0.5):
        filteredCands = []
        for cand in tau.isolationPFGammaCands():
            # if abs(cand.pdgId()) == 11:
            #     track = None
            #     if cand.trackRef().isAvailable():
            #         track = cand.trackRef().get()
            #     elif cand.gsfTrackRef().isAvailable():
            #         track = cand.gsfTrackRef().get()
            #     else:
            #         print 'No electron track found'
            #         import pdb; pdb.set_trace()
            #     if TauHLTAnalyzer.filterTrack(track, tau.vertex()):
            #         continue
            # el
            if (cand.pt() < minPt
                or deltaR(cand, tau) > maxDR):
                continue
            filteredCands.append(cand)
        return filteredCands

    @staticmethod
    def tauIsoBreakdown(tau, pfCandidates=None, maxDeltaR=None):
        # calculate photon pT outside signal cone
        variables = {
            'ptSumIso': tau.isolationPFCands(),
            'chargedPtSumIso': TauHLTAnalyzer.tauChargedFilteredIso(tau),
            'chargedPUPtSumIso': TauHLTAnalyzer.tauChargedFilteredIso(tau, minDeltaZ=0.2, maxDeltaZ=99999., cands=pfCandidates, maxDeltaR=maxDeltaR),
            'gammaPtSumIso': TauHLTAnalyzer.tauFilteredPhotons(tau),
            'gammaPtSumOutsideSignalCone': TauHLTAnalyzer.tauPhotonsOutsideSignalCone(tau),
            'neutralPtSumIso': tau.isolationPFNeutrHadrCands(),
            'ptSumSignal': tau.signalPFCands(),
            'chargedCandsPtSumSignal': tau.signalPFChargedHadrCands(),
            'gammaCandsPtSumSignal': tau.signalPFGammaCands(),
            'neutralCandsPtSumSignal': tau.signalPFNeutrHadrCands(),
        }

        for k, v in variables.items():
            ptsum = 0.
            for i in v:
                ptsum += i.pt()
            setattr(tau, k, ptsum)
