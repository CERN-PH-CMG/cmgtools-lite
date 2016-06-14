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
        st=st+"+("+str(func.GetParameter(i))+")"+("*(MVV/13000)"*i)
    return st    


parser = optparse.OptionParser()
parser.add_option("-s","--sample",dest="sample",default='',help="Type of sample")
parser.add_option("-c","--cut",dest="cut",help="Cut to apply for shape",default='')
parser.add_option("-o","--output",dest="output",help="Output JSON",default='')
parser.add_option("-b","--bins",dest="bins",type=int,help="bins",default=88)
parser.add_option("-V","--MVV",dest="mvv",help="mVV variable",default='')
parser.add_option("-m","--minMVV",dest="min",type=float,help="mVV variable",default=1)
parser.add_option("-M","--maxMVV",dest="max",type=float, help="mVV variable",default=1)
parser.add_option("-f","--function",dest="function",help="interpolating function",default='')
parser.add_option("-q","--quarkCut",dest="quarkCut",help="quark Selection cut",default='')

(options,args) = parser.parse_args()

sampleTypes=options.sample.split(',')
dataPlotters=[]

for filename in os.listdir(args[0]):
    for sampleType in sampleTypes:
        if filename.find(sampleType)!=-1:
            fnameParts=filename.split('.')
            fname=fnameParts[0]
            ext=fnameParts[1]
            if ext.find("root") ==-1:
                continue
            dataPlotters.append(TreePlotter(args[0]+'/'+fname+'.root','tree'))
            dataPlotters[-1].setupFromFile(args[0]+'/'+fname+'.pck')
            dataPlotters[-1].addCorrectionFactor('xsec','tree')
            dataPlotters[-1].addCorrectionFactor('genWeight','tree')
            dataPlotters[-1].addCorrectionFactor('puWeight','tree')

data=MergedPlotter(dataPlotters)



histoQ=data.drawTH1(options.mvv+"/13000.0",options.cut+"&&"+options.quarkCut,"1",options.bins,options.min/13000.0,options.max/13000.0)
histoA=data.drawTH1(options.mvv+"/13000.0",options.cut,"1",options.bins,options.min/13000.0,options.max/13000.0)
histoQ.Divide(histoA)

func=ROOT.TF1("func",options.function,options.min/13000.0,options.max/13000.0)
histoQ.Fit(func)

parameterization={'quarkFraction':returnString(func)}
f=open(options.output+".json","w")
json.dump(parameterization,f)
f.close()

F=ROOT.TFile(options.output+".root",'RECREATE')
F.cd()
histoQ.Write("fraction")
F.Close()

