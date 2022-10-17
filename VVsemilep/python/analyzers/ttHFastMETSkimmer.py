from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle

class ttHFastMETSkimmer( Analyzer ):
    def __init__(self, cfg_ana, cfg_comp, looperName ):
        super(ttHFastMETSkimmer,self).__init__(cfg_ana,cfg_comp,looperName)
        self.metCut = self.cfg_ana.metCut

    def declareHandles(self):
        super(ttHFastMETSkimmer, self).declareHandles()
        self.handles['met'] = AutoHandle(self.cfg_ana.met,"std::vector<pat::MET>")            

    def beginLoop(self, setup):
        super(ttHFastMETSkimmer,self).beginLoop(setup)
        self.counters.addCounter('events')
        self.count = self.counters.counter('events')
        self.count.register('all events')
        self.count.register('accepted events')


    def process(self, event):
        self.readCollections( event.input )
        self.count.inc('all events')
       
        if self.handles['met'].product().front().pt() > self.metCut :
             self.count.inc('accepted events')
             return True
        return False
