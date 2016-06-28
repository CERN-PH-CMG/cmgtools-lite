from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer

class ZTagAndProbeAnalyzer( Analyzer ):
    def __init__(self, cfg_ana, cfg_comp, looperName ):
        super(ZTagAndProbeAnalyzer,self).__init__(cfg_ana,cfg_comp,looperName)
        if self.cfg_comp.isMC:
            self.tagSelection = getattr(cfg_ana, 'tagSelectionMC', getattr(cfg_ana, 'tagSelection', None))
        else:
            self.tagSelection = getattr(cfg_ana, 'tagSelectionData', getattr(cfg_ana, 'tagSelection', None))
        if not self.tagSelection: raise RuntimeError, "Need to specify tagSelection(MC|Data) or tagSelection"
        self.probeSelection = cfg_ana.probeSelection
        self.probeCollection = cfg_ana.probeCollection
        self.massRange = cfg_ana.massRange
        self.filter = getattr(cfg_ana, 'filter', False)

    def beginLoop(self, setup):
        super(ZTagAndProbeAnalyzer,self).beginLoop(setup)
        self.counters.addCounter('ZTagAndProbe')
        count = self.counters.counter('ZTagAndProbe')
        count.register('all events')
        count.register('passing events')
        count.register('all pairs')

    def process(self, event):
        self.readCollections( event.input )

        self.counters.counter('ZTagAndProbe').inc('all events')
        probeCollection = getattr(event, self.probeCollection)
        # count tight leptons
        tags   = [ lep for lep in event.selectedLeptons if self.tagSelection(lep)   ]
        probes = [ lep for lep in probeCollection       if self.probeSelection(lep) ]

        event.TnP = []
        for tag in tags:
            for probe in probes:
                if tag.pdgId() != - probe.pdgId(): continue
                pair = tag.p4() + probe.p4()
                if pair.mass() < self.massRange[0] or pair.mass() > self.massRange[1]: continue
                pair.tag = tag
                pair.probe = probe
                event.TnP.append(pair)
        #event.TnP.sort(key = lambda dilep : abs(dilep.M() - 91.1876))
        for p in event.TnP: 
            self.counters.counter('ZTagAndProbe').inc('all pairs')

        if self.filter and len(event.TnP) == 0:
            return False
        self.counters.counter('ZTagAndProbe').inc('passing events')
        return True
