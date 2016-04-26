from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle

class ttHFastJetSkimmer( Analyzer ):
    def __init__(self, cfg_ana, cfg_comp, looperName ):
        super(ttHFastJetSkimmer,self).__init__(cfg_ana,cfg_comp,looperName)
        self.jetCut = self.cfg_ana.jetCut

    def declareHandles(self):
        super(ttHFastJetSkimmer, self).declareHandles()
        self.handles['jets'] = AutoHandle(self.cfg_ana.jets,"std::vector<pat::Jet>")            

    def beginLoop(self, setup):
        super(ttHFastJetSkimmer,self).beginLoop(setup)
        self.counters.addCounter('events')
        self.count = self.counters.counter('events')
        self.count.register('all events')
        self.count.register('accepted events')


    def process(self, event):
        self.readCollections( event.input )
        self.count.inc('all events')
        
        jets = 0

        for jet in self.handles['jets'].product():
            if self.jetCut(jet): jets += 1

        if jets >= self.cfg_ana.minJets:
             self.count.inc('accepted events')
             return True

        return False
