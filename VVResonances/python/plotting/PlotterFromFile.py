from CMGTools.VVResonances.plotting.TreePlotter import TreePlotter
from CMGTools.VVResonances.plotting.MergedPlotter import MergedPlotter
import os, sys,shutil

class PlotterFromFile:
    def __init__(self,directory, filenames,isData):
        self.dataPlotters=[]
        sampleTypes=filenames.split(',')
        for filename in os.listdir(directory):
            for sampleType in sampleTypes:
                if filename.find(sampleType)!=-1:
                    fnameParts=filename.split('.')
                    fname=fnameParts[0]
                    ext=fnameParts[1]
                    if ext.find("root") ==-1:
                        continue
                    self.dataPlotters.append(TreePlotter(directory+'/'+fname+'.root','tree'))
                    if not isData:
                        self.dataPlotters[-1].setupFromFile(directory+'/'+fname+'.pck')
                        self.dataPlotters[-1].addCorrectionFactor('xsec','tree')
                        self.dataPlotters[-1].addCorrectionFactor('genWeight','tree')
                        self.dataPlotters[-1].addCorrectionFactor('puWeight','tree')
        self.plotter=MergedPlotter(self.dataPlotters)               
        
    def __call__(self):
        return self.plotter
    
    
