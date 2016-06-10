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


(options,args) = parser.parse_args()
#define output dictionary


f=open(args[0])
info=json.load(f)


mass = 600

while mass<5000:
    fitter=Fitter(['MVV'])
    fitter.signalResonance('model','MVV')
    fitter.w.factory("MH[0,20000]")
    for var in ['MEAN','SIGMA'
    



#Now we have the samples: Sort the masses and run the fits
N=0
for mass in sorted(samples.keys()):

    print 'fitting',str(mass) 
    plotter=TreePlotter(args[0]+'/'+samples[mass]+'.root','tree')
    plotter.setupFromFile(args[0]+'/'+samples[mass]+'.pck')
    plotter.addCorrectionFactor('genWeight','tree')
    plotter.addCorrectionFactor('xsec','tree')
    plotter.addCorrectionFactor('puWeight','tree')
       
        
    fitter.w.var("MH").setVal(mass)
    histo = plotter.drawTH1(options.mvv,options.cut,"1",500,0,13000)
    fitter.importBinnedData(histo,['MVV'],'data')
    fitter.fit('model','data',[ROOT.RooFit.SumW2Error(0)])
    events=histo.Integral()*options.BR
    graphs['yield'].SetPoint(N,mass,events)
    fitter.projection("model","data","MVV","debugVV_"+str(mass)+".root")

    

    for var,graph in graphs.iteritems():
        if var=='yield':
            continue
        value,error=fitter.fetch(var)
        graph.SetPoint(N,mass,value)
        graph.SetPointError(N,0.0,error)
                
    N=N+1

          

F=ROOT.TFile(options.output,"RECREATE")
F.cd()
for name,graph in graphs.iteritems():
    graph.Write(name)
F.Close()
            
