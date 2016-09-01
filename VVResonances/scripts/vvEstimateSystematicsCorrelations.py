#!/usr/bin/env python

import ROOT
from array import array
from CMGTools.VVResonances.plotting.TreePlotter import TreePlotter
from CMGTools.VVResonances.plotting.MergedPlotter import MergedPlotter
from math import log
import os, sys, re, optparse,pickle,shutil,json


parser = optparse.OptionParser()
parser.add_option("-s","--samples",dest="samples",default='',help="Type of sample")
parser.add_option("-d","--cutDenominator",dest="cutDenominator",help="Cut to apply for yield denominator",default='')
parser.add_option("-n","--cutNumerator",dest="cutNumerator",help="Cut to apply for yield numerator",default='')
parser.add_option("-v","--var",dest="var",help="variable seprataed by comma",default='')
parser.add_option("-f","--factor",dest="factor",type=float,help="factor to scale the variable",default=1.0)

(options,args) = parser.parse_args()
#define output dictionary

samples={}



sampleTypes=options.samples.split(',')

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


denominator = data.drawTH1("0.5",options.cutDenominator,"1",1,0,1)

cut=options.cutNumerator
nominal = data.drawTH1("0.5",'&&'.join([options.cutDenominator,cut]),"1",1,0,1)

cut=options.cutNumerator.replace(options.var,"("+str(options.factor)+"*"+options.var+")")
up = data.drawTH1("0.5",'&&'.join([options.cutDenominator,cut]),"1",1,0,1)

cut=options.cutNumerator.replace(options.var,"("+str(1.0/options.factor)+"*"+options.var+")")
down = data.drawTH1("0.5",'&&'.join([options.cutDenominator,cut]),"1",1,0,1)


effUp = abs(up.Integral()/nominal.Integral())
effDown = abs(down.Integral()/nominal.Integral())

print sampleTypes,'Uncertainty =',(effUp-effDown)/2.0
