from math import *
from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.HeppyCore.framework.event import Event
from PhysicsTools.HeppyCore.utils.deltar import *
import os

        
class TopMergingAnalyzer( Analyzer ):
    def __init__(self, cfg_ana, cfg_comp, looperName ):
        super(TopMergingAnalyzer,self).__init__(cfg_ana,cfg_comp,looperName)

    def declareHandles(self):
        super(TopMergingAnalyzer, self).declareHandles()

    def beginLoop(self, setup):
        super(TopMergingAnalyzer,self).beginLoop(setup)

    def process(self, event):
        self.readCollections( event.input )
        if self.cfg_comp.isData:
            return

        for jet in event.jetsAK8:
            associatedQuarks=[]

            for quark in event.genwzquarks:
                if deltaR(quark.eta(),quark.phi(),jet.eta(),jet.phi())<0.8:
                    associatedQuarks.append(quark)

#            print 'associated quarks',len(associatedQuarks)        
            if len(associatedQuarks)==2:
                jet.mergedTrue=1
            else:
                jet.mergedTrue=0
            
            #nearest b quark
            if len(event.genbquarksFromTop)==0:
                jet.nearestBDR=-99.0
            else:
                nearest=min(event.genbquarksFromTop,key=lambda x: deltaR(jet.eta(),jet.phi(),x.eta(),x.phi()))
                jet.nearestBDR=deltaR(jet.eta(),jet.phi(),nearest.eta(),nearest.phi())


                
        


        



