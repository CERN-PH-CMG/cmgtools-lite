from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer


        
class ttHLepQCDFakeRateAnalyzer( Analyzer ):
    def __init__(self, cfg_ana, cfg_comp, looperName ):
        super(ttHLepQCDFakeRateAnalyzer,self).__init__(cfg_ana,cfg_comp,looperName)
        self.leptonSel = getattr(cfg_ana, 'leptonSel', lambda lep : True)
        self.jetColl   = getattr(cfg_ana, 'jetColl', 'cleanJetsAll')
        self.jetSel    = getattr(cfg_ana, 'jetSel', lambda jet : True)
        self.pairSel   = getattr(cfg_ana, 'pairSel', lambda lep, jet : True)
        self.jetSort   = getattr(cfg_ana, 'jetSort', lambda jet : jet.pt())
        self.minPairs  = getattr(cfg_ana, 'minPairs', -1)

    def declareHandles(self):
        super(ttHLepQCDFakeRateAnalyzer, self).declareHandles()

    def beginLoop(self, setup):
        super(ttHLepQCDFakeRateAnalyzer,self).beginLoop(setup)
        self.counters.addCounter('events')
        count = self.counters.counter('events')
        count.register('all events')
        count.register('with leptons')
        count.register('with jets')
        count.register('accepted events')


    def process(self, event):
        npairs = 0;
        self.counters.counter('events').inc('all events')
        leps = filter(self.leptonSel, event.selectedLeptons)
        jets = filter(self.jetSel, getattr(event, self.jetColl))
        jets.sort(key = self.jetSort, reverse=True)
        if len(leps): self.counters.counter('events').inc('with leptons')
        if len(jets): self.counters.counter('events').inc('with jets')
        for lep in event.selectedLeptons: lep.awayJet = None
        for lep in leps:
            for jet in jets:
                if self.pairSel(lep,jet):
                    lep.awayJet = jet
                    npairs += 1
                    break
        if npairs < self.minPairs:
            return False
        self.counters.counter('events').inc('accepted events')
        return True
