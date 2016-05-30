from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer

class ttHHTSkimmer( Analyzer ):
    def __init__(self, cfg_ana, cfg_comp, looperName ):
        super(ttHHTSkimmer,self).__init__(cfg_ana,cfg_comp,looperName)
        self.minHT = cfg_ana.minHT if hasattr(cfg_ana, 'minHT') else 0.

    def declareHandles(self):
        super(ttHHTSkimmer, self).declareHandles()

    def beginLoop(self, setup):
        super(ttHHTSkimmer,self).beginLoop(setup)
        self.counters.addCounter('events')
        count = self.counters.counter('events')
        count.register('all events')
        count.register('accepted events')


    def process(self, event):
        self.readCollections( event.input )
        self.counters.counter('events').inc('all events')

        htJet30j = sum([j.pt() for j in event.cleanJetsAll if (j.pt() > 30 and abs(j.eta())<2.4) ]) #only consider central jets with pt>30 GeV for ht-calculation
        if(htJet30j<self.minHT): 
            return False
        self.counters.counter('events').inc('accepted events')
        return True
