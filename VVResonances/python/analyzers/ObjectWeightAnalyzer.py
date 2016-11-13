import ROOT
import random
import math
from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
import PhysicsTools.HeppyCore.framework.config as cfg
import os

class ObjectWeightAnalyzer( Analyzer ):
    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(ObjectWeightAnalyzer,self).__init__(cfg_ana, cfg_comp, looperName)
        
        path = os.path.expandvars(self.cfg_ana.path) #"%s/src/CMGTools/RootTools/data/jec" % os.environ['CMSSW_BASE'];


        for weight in self.cfg_ana.weights:
            if weight['filename']=='None':
                continue
            weight['rootFile'] = ROOT.TFile(path+"/"+weight['filename'])
            weight['histo'] = weight['rootFile'].Get(weight["histoname"]) 


    def beginLoop(self, setup):
        super(ObjectWeightAnalyzer,self).beginLoop(setup)

        
    def process(self, event):
        self.readCollections( event.input )
        objects  = getattr(event,self.cfg_ana.collection)
        
        for obj in objects:
            for weight in self.cfg_ana.weights:
                if not weight['cut'](obj):
                    continue
                if weight['filename']=="None": #flat scale factor
                    if hasattr(obj,weight['tag']):
                        current = getattr(obj,weight['tag'])
                    else:
                        current = 1.0
                    setattr(obj,weight['tag'],current*weight['f'](obj))
                    

                elif weight['dimensions']==1:
                    x=weight['x'](obj)
                    bin =weight['histo'].GetXaxis().FindBin(x)
                    if bin==0:
                        bin=1
                    if bin==weight['histo'].GetXaxis().GetNbins()+1:
                        bin=weight['histo'].GetXaxis().GetNbins()
                    scaleFactor = weight['histo'].GetBinContent(bin)
                    if hasattr(obj,weight['tag']):
                        current = getattr(obj,weight['tag'])
                    else:
                        current = 1.0
                    setattr(obj,weight['tag'],current*scaleFactor)

                elif weight['dimensions']==2:
                    x=weight['x'](obj)
                    y=weight['y'](obj)
                    binx =weight['histo'].GetXaxis().FindBin(x)
                    if binx==0:
                        binx=1
                    if binx==weight['histo'].GetXaxis().GetNbins()+1:
                        binx=weight['histo'].GetXaxis().GetNbins()
                    biny =weight['histo'].GetYaxis().FindBin(y)
                    if biny==0:
                        biny=1
                    if biny==weight['histo'].GetYaxis().GetNbins()+1:
                        biny=weight['histo'].GetYaxis().GetNbins()
                    bin=weight['histo'].GetBin(binx,biny)
                    scaleFactor = weight['histo'].GetBinContent(bin)
                    if hasattr(obj,weight['tag']):
                        current = getattr(obj,weight['tag'])
                    else:
                        current = 1.0
                    setattr(obj,weight['tag'],current*scaleFactor)
                elif weight['dimensions']==3:
                    x=weight['x'](obj)
                    y=weight['y'](obj)
                    z=weight['z'](obj)
                    binx =weight['histo'].GetXaxis().FindBin(x)
                    if binx==0:
                        binx=1
                    if binx==weight['histo'].GetXaxis().GetNbins()+1:
                        binx=weight['histo'].GetXaxis().GetNbins()
                    biny =weight['histo'].GetYaxis().FindBin(y)
                    if biny==0:
                        biny=1
                    if biny==weight['histo'].GetYaxis().GetNbins()+1:
                        biny=weight['histo'].GetYaxis().GetNbins()

                    binz =weight['histo'].GetZaxis().FindBin(z)
                    if binz==0:
                        binz=1
                    if binz==weight['histo'].GetZaxis().GetNbins()+1:
                        binz=weight['histo'].GetZaxis().GetNbins()

                    bin=weight['histo'].GetBin(binx,biny,binz)
                    scaleFactor = weight['histo'].GetBinContent(bin)
                    if hasattr(obj,weight['tag']):
                        current = getattr(obj,weight['tag'])
                    else:
                        current = 1.0
                    setattr(obj,weight['tag'],current*scaleFactor)




        
            

        


                
                
