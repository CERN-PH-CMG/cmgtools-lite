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
parser.add_option("-m","--minMVV",dest="min",type=float,help="mVV variable",default=1)
parser.add_option("-M","--maxMVV",dest="max",type=float, help="mVV variable",default=1)
parser.add_option("-f","--function",dest="function",help="interpolating function",default='')
parser.add_option("-b","--BR",dest="BR",type=float, help="branching ratio",default=1)
parser.add_option("-x","--minMass",dest="minMass",type=float, help="minimumMass",default=0.0)

(options,args) = parser.parse_args()
#define output dictionary
samples={}

yieldgraph=ROOT.TGraphErrors()

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

    if mass<options.minMass:
        continue


    samples[mass] = fname

    print 'found',filename,'mass',str(mass) 


#Now we have the samples: Sort the masses and run the fits
N=0
for mass in sorted(samples.keys()):

    print 'fitting',str(mass) 
    plotter=TreePlotter(args[0]+'/'+samples[mass]+'.root','tree')
    plotter.setupFromFile(args[0]+'/'+samples[mass]+'.pck')
    plotter.addCorrectionFactor('genWeight','tree')
    plotter.addCorrectionFactor('xsec','tree')
    plotter.addCorrectionFactor('puWeight','tree')
    histo = plotter.drawTH1(options.mvv,options.cut,"1",500,options.min,options.max)
    err=ROOT.Double(0)
    integral=histo.IntegralAndError(1,histo.GetNbinsX(),err) 

    yieldgraph.SetPoint(N,mass,integral*options.BR)
    yieldgraph.SetPointError(N,0.0,err*options.BR)
    N=N+1





func = ROOT.TF1("func",options.function,0,13000)
yieldgraph.Fit(func)


parameterization={'yield':returnString(func)}
f=open(options.output+".json","w")
json.dump(parameterization,f)
f.close()

c=ROOT.TCanvas("c")
c.cd()
yieldgraph.Draw("AP")
c.SaveAs("debug_"+options.output+".png")

#F=ROOT.TFile(options.output+".root",'RECREATE')
#F.cd()
#yieldgraph.Write("yield")
#F.Close()

