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

            maxDR=0;            
            for quark in event.genwzquarks:
                dR=deltaR(quark.eta(),quark.phi(),jet.eta(),jet.phi())


                if dR<0.8:
                    associatedQuarks.append(quark)
                if dR<1.5:
                    if dR>maxDR:
                        maxDR=dR


#            print 'associated quarks',len(associatedQuarks)        
            jet.genqq = associatedQuarks 
            if len(associatedQuarks)==2:
                jet.mergedTrue=1
            else:
                jet.mergedTrue=0
                jet.quark1 = None
                jet.quark2 = None
            
            #nearest b quark
            jet.genb=[]
            jet.maxQuarkDistance = maxDR
            if len(event.genbquarksFromTop)==0:
                jet.nearestBDR=-1.0
            else:
                nearest=min(event.genbquarksFromTop,key=lambda x: deltaR(jet.eta(),jet.phi(),x.eta(),x.phi()))
                jet.nearestBDR=deltaR(jet.eta(),jet.phi(),nearest.eta(),nearest.phi())
                jet.genb.append(nearest)


                
        


        



