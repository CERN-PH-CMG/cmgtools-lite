#!/usr/bin/env python

import ROOT
from array import array
from CMGTools.VVResonances.plotting.PlotterFromFile  import PlotterFromFile
from math import log
import os, sys, re, optparse,pickle,shutil,json


parser = optparse.OptionParser()
parser.add_option("-s","--samplesNum",dest="samplesNum",default='',help="Type of sample")
parser.add_option("-S","--samplesDenom",dest="samplesDenom",default='',help="Type of sample")
parser.add_option("-c","--cutNum",dest="cutNum",help="Cut to apply for yield",default='')
parser.add_option("-C","--cutDenom",dest="cutDenom",help="Cut to apply for yield",default='')
parser.add_option("-v","--vars",dest="vars",help="variables seprataed by comma",default='')
parser.add_option("-b","--bins",dest="bins",help="bins per dimension separated by comma and by : for the different dimensions",default='')
parser.add_option("-o","--output",dest="output",help="Output ROOT",default='')
parser.add_option("-d","--isData",dest="data",type=int,help="isData",default=1)
parser.add_option("-n","--name",dest="name",help="name",default="histo")




(options,args) = parser.parse_args()
#define output dictionary

samples={}




dataNP=PlotterFromFile(args[0],options.samplesNum,options.data)
dataN=dataNP()

dataDP=PlotterFromFile(args[0],options.samplesDenom,options.data)
dataD=dataDP()


pvars=options.vars.split(',')

binsPerDim=options.bins.split(':')


bins={}
for i,v in enumerate(pvars):
    bins[v]=map(float,binsPerDim[i].split(','))

#import pdb;pdb.set_trace()

if len(pvars)==1:
    efficiency=dataN.drawTH1Binned(pvars[0],options.cutNum,"1",bins[pvars[0]])
    denom=dataD.drawTH1Binned(pvars[0],options.cutDenom,"1",bins[pvars[0]])
    graph=ROOT.TGraphAsymmErrors()
    graph.BayesDivide(efficiency,denom)
    graph.SetName(options.name+"_graph")

    efficiency.Divide(efficiency,denom,1,1,"B")

if len(pvars)==2:
    efficiency=dataN.drawTH2Binned(pvars[1]+":"+pvars[0],options.cutNum,"1",bins[pvars[0]],bins[pvars[1]])
    denom=dataN.drawTH2Binned(pvars[1]+":"+pvars[0],options.cutDenom,"1",bins[pvars[0]],bins[pvars[1]])
    efficiency.Divide(efficiency,denom,1,1,"B")
    graph=None
F=ROOT.TFile(options.output,"UPDATE")
F.cd()
efficiency.Write(options.name)
if graph!=None:
    graph.Write()
F.Close()



