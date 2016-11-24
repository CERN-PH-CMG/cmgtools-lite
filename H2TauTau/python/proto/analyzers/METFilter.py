from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle

from CMGTools.H2TauTau.proto.analyzers.met_filter_implementations import passBadMuonFilter, passBadChargedHadronFilter

class METFilter(Analyzer):

    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(METFilter, self).__init__(cfg_ana, cfg_comp, looperName)
        self.processName = getattr(self.cfg_ana, "processName", "HLT")
        self.triggers = cfg_ana.triggers
        self.autoAccept = True if len(self.triggers) == 0 else False

    def declareHandles(self):
        super(METFilter, self).declareHandles()
        self.handles['TriggerResults'] = AutoHandle(('TriggerResults', '', self.processName), 'edm::TriggerResults', fallbackLabel=('TriggerResults', '', 'PAT')) # fallback for FastSim
        self.handles['packedCandidates'] = AutoHandle('packedPFCandidates', 'std::vector<pat::PackedCandidate>')
        self.handles['muons'] = AutoHandle('slimmedMuons', 'std::vector<pat::Muon>')

    def beginLoop(self, setup):
        super(METFilter, self).beginLoop(setup)
        self.counters.addCounter('events')
        self.count = self.counters.counter('events')
        self.count.register('all events')
        for trigger in self.triggers:
            self.count.register('pass {t}'.format(t=trigger))

        self.count.register('pass bad muon')
        self.count.register('pass bad charged hadron')

    def process(self, event):
        if self.autoAccept:
            return True

        self.readCollections(event.input)
        self.count.inc('all events')

        triggerBits = self.handles['TriggerResults'].product()
        names = event.input.object().triggerNames(triggerBits)

        for trigger_name in self.triggers:
            index = names.triggerIndex(trigger_name)
            if index == len(triggerBits):
                setattr(event, trigger_name, False)
                continue

            fired = triggerBits.accept(index)
            if fired:
                setattr(event, trigger_name, True)
                self.count.inc('pass {t}'.format(t=trigger_name))
            else:
                setattr(event, trigger_name, False)

        packedCandidates = self.handles['packedCandidates'].product()
        muons = self.handles['muons'].product()

        event.passBadMuonFilter = passBadMuonFilter(muons, packedCandidates)
        event.passBadChargedHadronFilter = passBadChargedHadronFilter(muons, packedCandidates)

        if event.passBadMuonFilter:
            self.count.inc('pass bad muon')
        if event.passBadChargedHadronFilter:
            self.count.inc('pass bad charged hadron')

        return True
