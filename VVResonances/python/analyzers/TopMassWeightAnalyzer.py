from math import *
from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle

from PhysicsTools.HeppyCore.framework.event import Event
from PhysicsTools.HeppyCore.utils.deltar import *
import os
import itertools
import ROOT

        
class TopMassWeightAnalyzer( Analyzer ):
    def __init__(self, cfg_ana, cfg_comp, looperName ):
        super(TopMassWeightAnalyzer,self).__init__(cfg_ana,cfg_comp,looperName)
        self.doHists=False
        if (hasattr(self.cfg_ana,'makeHists')) and self.cfg_ana.makeHists:
            self.doHists=True
            self.file = ROOT.TFile('/'.join([self.dirName,'mttspectrum.root']),'RECREATE')
            self.histo = ROOT.TH1D("spectrum","spectrum",400,0,8000)
    def declareHandles(self):
        super(TopMassWeightAnalyzer, self).declareHandles()
        self.mchandles['GenInfo'] = AutoHandle( ('generator','',''), 'GenEventInfoProduct' )

    def beginLoop(self, setup):
        super(TopMassWeightAnalyzer,self).beginLoop(setup)

    def process(self, event):
        self.readCollections( event.input )
        event.topMassWeight=1.0
        event.genMTT=-1.0
        if self.cfg_comp.isData:
            return
        #look only at semileptonic    
        if len(event.genlepsFromTop)==0 or len(event.gentopquarks)!=2:
            return
        event.genMTT = (event.gentopquarks[0].p4()+event.gentopquarks[1].p4()).mass()



        if self.doHists:
            weight= self.mchandles['GenInfo'].product().weight()
            self.histo.Fill(event.genMTT*weight)


    def write(self, setup):
        super(TopMassWeightAnalyzer,self).write(setup)
        if self.doHists:
            self.file.cd()
            self.histo.Write()
            self.file.Close()


                


        
        

            




                
        


        



