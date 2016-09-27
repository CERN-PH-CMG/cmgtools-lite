from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
import itertools

class GammaSkimmer( Analyzer ):
    def __init__(self, cfg_ana, cfg_comp, looperName ):
        super(GammaSkimmer,self).__init__(cfg_ana,cfg_comp,looperName)

    def declareHandles(self):
        super(GammaSkimmer, self).declareHandles()

    def beginLoop(self, setup):
        super(GammaSkimmer,self).beginLoop(setup)
        self.counters.addCounter('events')
        count = self.counters.counter('events')
        count.register('all events')
        count.register('vetoed events')
        count.register('accepted events')


    def process(self, event):
        self.readCollections( event.input )
        self.counters.counter('events').inc('all events')

        gammaSkim = ( len(event.selectedPhotons) > 0 )
        ret = ( gammaSkim )

        if ret: self.counters.counter('events').inc('accepted events')
        return ret
