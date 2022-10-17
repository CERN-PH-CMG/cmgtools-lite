import os 
import logging 

from PhysicsTools.HeppyCore.utils.deltar import deltaR
from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.HeppyCore.framework.event import Event
from PhysicsTools.HeppyCore.statistics.counter import Counter, Counters
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle

class isoTrackFastSkimmer( Analyzer ):
    def __init__(self, cfg_ana, cfg_comp, looperName ):
        super(isoTrackFastSkimmer,self).__init__(cfg_ana,cfg_comp,looperName)
        self.cut = cfg_ana.cut

    def declareHandles(self):
        super(isoTrackFastSkimmer, self).declareHandles()
        self.handles['src'] = AutoHandle("isolatedTracks","std::vector<pat::IsolatedTrack>")            

    def beginLoop(self,setup):
        super(isoTrackFastSkimmer,self).beginLoop(setup)
        self.counters.addCounter('events')
        count = self.counters.counter('events')
        count.register('all events')
        count.register('accepted events')


    def process(self, event):
        self.readCollections( event.input )
        self.counters.counter('events').inc('all events')

        objects = []
        for i,obj in enumerate(self.handles['src'].product()):
            if self.cut(obj):
                obj.index = i # needed to retrieve dE/dX later
                objects.append(obj)
        if not objects:
            return False

        self.counters.counter('events').inc('accepted events')
        event.preselIsoTracks = objects
        return True
