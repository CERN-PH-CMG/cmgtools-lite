#!/usr/bin/env python

import ROOT
from array import array
from CMGTools.VVResonances.plotting.TreePlotter import TreePlotter
from CMGTools.VVResonances.plotting.MergedPlotter import MergedPlotter
from CMGTools.VVResonances.plotting.StackPlotter import StackPlotter
from CMGTools.VVResonances.statistics.Fitter import Fitter
from math import log
import os, sys, re, optparse,pickle,shutil,json

def returnString(func):
    st='0'
    for i in range(0,func.GetNpar()):
        st=st+"+("+str(func.GetParameter(i))+")"+("*MH"*i)
    return st    


parser = optparse.OptionParser()
parser.add_option("-s","--sample",dest="sample",default='',help="Type of sample")
parser.add_option("-c","--cut",dest="cut",help="Cut to apply for shape",default='')
parser.add_option("-o","--output",dest="output",help="Output JSON",default='')
parser.add_option("-V","--MVV",dest="mvv",help="mVV variable",default='')
parser.add_option("-v","--mjj",dest="mjj",help="mJJ variable",default='')
parser.add_option("-m","--minMJJ",dest="minMJJ",type=float,help="minMJJ",default=20)
parser.add_option("-M","--maxMJJ",dest="maxMJJ",type=float,help="maxMJJ",default=160)
(options,args) = parser.parse_args()
#define output dictionary

samples={}
graphs={'MEAN':ROOT.TGraphErrors(),'SIGMA':ROOT.TGraphErrors(),'ALPHA1':ROOT.TGraphErrors(),'N1':ROOT.TGraphErrors(),'ALPHA2':ROOT.TGraphErrors(),'N2':ROOT.TGraphErrors(),\
'mean':ROOT.TGraphErrors(),'sigma':ROOT.TGraphErrors(),'alpha':ROOT.TGraphErrors(),'n':ROOT.TGraphErrors(),'slope':ROOT.TGraphErrors(),'f':ROOT.TGraphErrors()}

for filename in os.listdir(args[0]):
    if not (filename.find(options.sample)!=-1):
        continue

#found sample. get the mass
    fnameParts=filename.split('.')
    fname=fnameParts[0]
    ext=fnameParts[1]
    if ext.find("root") ==-1:
        continue
        

    mass = float(fname.split('_')[-1])

        

    samples[mass] = fname

    print 'found',filename,'mass',str(mass) 


#Now we have the samples: Sort the masses and run the fits
N=0
for mass in sorted(samples.keys()):

    print 'fitting',str(mass) 
    plotter=TreePlotter(args[0]+'/'+samples[mass]+'.root','tree')
#    plotter.setupFromFile(args[0]+'/'+samples[mass]+'.pck')
    plotter.addCorrectionFactor('genWeight','tree')
#    plotter.addCorrectionFactor('xsec','tree')
    plotter.addCorrectionFactor('puWeight','tree')
       
        
    fitter=Fitter(['MVV','MJJ'])
    fitter.signal2D('model',['MVV','MJJ'])
    fitter.w.var("MH").setVal(mass)
    histo = plotter.drawTH2(options.mjj+':'+options.mvv,options.cut,"1",500,0,6000,100,options.minMJJ,options.maxMJJ)

    fitter.importBinnedData(histo,['MVV','MJJ'],'data')
    fitter.fit('model','data',[ROOT.RooFit.SumW2Error(0)])
    fitter.fit('model','data',[ROOT.RooFit.SumW2Error(0),ROOT.RooFit.Minos(1)])
    fitter.projection("model","data","MVV","debugMVV_"+str(mass)+"_"+options.output+".png")
    fitter.projection("model","data","MJJ","debugMJJ_"+str(mass)+"_"+options.output+".png")

    for var,graph in graphs.iteritems():
        value,error=fitter.fetch(var)
        graph.SetPoint(N,mass,value)
        graph.SetPointError(N,0.0,error)
                
    N=N+1
        
F=ROOT.TFile(options.output,"RECREATE")
F.cd()
for name,graph in graphs.iteritems():
    graph.Write(name)
F.Close()
            
