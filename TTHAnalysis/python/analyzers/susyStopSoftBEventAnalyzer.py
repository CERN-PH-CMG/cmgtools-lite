from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.HeppyCore.utils.deltar import deltaPhi
from math import sqrt, cos

        
class susyStopSoftBEventAnalyzer( Analyzer ):
    def __init__(self, cfg_ana, cfg_comp, looperName ):
        super(susyStopSoftBEventAnalyzer,self).__init__(cfg_ana,cfg_comp,looperName)

    def declareHandles(self):
        super(susyStopSoftBEventAnalyzer, self).declareHandles()

    def beginLoop(self, setup):
        super(susyStopSoftBEventAnalyzer,self).beginLoop(setup)
        self.counters.addCounter('events')
        count = self.counters.counter('events')
        count.register('all events')
        count.register('one jet')
        count.register('accepted events')
        self.nfail = 0


    def process(self, event):
        self.readCollections( event.input )
        self.counters.counter('events').inc('all events')

        if len(event.cleanJets) >= 0:
            self.counters.counter('events').inc('one jet')

        event.lightJets = [ j for j in event.cleanJets if not j.btagWP("CSVv2IVFL") ]
        event.lightJets.sort( key = lambda j : j.pt(), reverse = True )
        event.ISRJet = event.lightJets[0] if len(event.lightJets) else None

        event.iBs = [ i for (i,j) in enumerate(event.cleanJets) ]
        event.iBs.sort(key = lambda i : event.cleanJets[i].btag('pfCombinedInclusiveSecondaryVertexV2BJetTags'), reverse = True)

        def mT(b, m): 
            return sqrt(2*b.pt()*m.pt()*(1-cos(b.phi()-m.phi())))
        event.mtB1 = mT(event.cleanJets[event.iBs[0]], event.met) if len(event.iBs) >= 1 else -99.0
        event.mtB2 = mT(event.cleanJets[event.iBs[1]], event.met) if len(event.iBs) >= 2 else -99.0

        for i in xrange(6):
            setattr(event, 'dphiJet%dMet' % (i+1), abs(deltaPhi(event.cleanJets[i].phi(), event.met.phi())) if len(event.cleanJets) > i else -99)

        self.counters.counter('events').inc('accepted events')
        return True
