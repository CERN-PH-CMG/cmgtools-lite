#!/usr/bin/env python

import ROOT
from array import array
from CMGTools.VVResonances.statistics.Fitter import Fitter
from math import log
import os, sys, re, optparse,pickle,shutil,json
import json

parser = optparse.OptionParser()
parser.add_option("-o","--output",dest="output",help="Output JSON",default='')
parser.add_option("-i","--histo",dest="histo",help="name",default="histo")
parser.add_option("-f","--function",dest="function",help="name",default="bernstein")
parser.add_option("-j","--json",dest="json",help="name",default="test.json")

(options,args) = parser.parse_args()


parameterization={}

f=ROOT.TFile(args[0])
histo=f.Get(options.histo)

fitter=Fitter(['x','y'])
fitter.importBinnedData(histo,['x','y'],'data')

if options.function=='erfexpW2D':
    fitter.mjjParamErfExp('model',options.json)

fitter.fit('model','data',[ROOT.RooFit.SumW2Error(1),ROOT.RooFit.ConditionalObservables(ROOT.RooArgSet(fitter.w.var("x")))])
fitter.fit('model','data',[ROOT.RooFit.SumW2Error(1),ROOT.RooFit.ConditionalObservables(ROOT.RooArgSet(fitter.w.var("x")))])
fitter.projectionCond("model","data","y","x","debug"+options.output+".png")


for i in range(0,4):
    var='c_'+str(i)
    val,err=fitter.fetch(var)
    parameterization[var]=val
    parameterization[var+'Err']=err

f=open(options.output+".json","w")
json.dump(parameterization,f)
f.close()




