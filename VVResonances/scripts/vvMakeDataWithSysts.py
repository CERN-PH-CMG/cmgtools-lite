#!/usr/bin/env python

import ROOT
from array import array
from CMGTools.VVResonances.plotting.TreePlotter import TreePlotter
from CMGTools.VVResonances.plotting.MergedPlotter import MergedPlotter
from math import log
import os, sys, re, optparse,pickle,shutil,json


parser = optparse.OptionParser()
parser.add_option("-s","--samples",dest="samples",default='',help="Type of sample")
parser.add_option("-c","--cut",dest="cut",help="Cut to apply for yield",default='')
parser.add_option("-o","--output",dest="output",help="Output ROOT",default='')
parser.add_option("-v","--var",dest="var",help="variables seprataed by comma",default='')
parser.add_option("-b","--bins",dest="bins",type=int,help="bins")
parser.add_option("-m","--min",dest="min",type=float, help="minimum ",default=40)
parser.add_option("-M","--max",dest="max",type=float,help="maximum",default=160)
parser.add_option("-n","--name",dest="name",help="name",default="histo")
parser.add_option("-N","--systName",dest="systName",help="name",default="jetMass")


def mirror(histo,histoRUp):
    histoRDwn=histoRUp.Clone()
    for bin in range(1,histo.GetNbinsX()+1):
            if histoRUp.GetBinContent(bin)>0:
                histoRDwn.SetBinContent(bin,histo.GetBinContent(bin)/histoRUp.GetBinContent(bin))
            else:   
                histoRDwn.SetBinContent(bin,histo.GetBinContent(bin))
    return histoRDwn        


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

histo=data.drawTH1(options.var,options.cut,"1",options.bins,options.min,options.max)
histoUp=data.drawTH1(options.var+"Up",options.cut,"1",options.bins,options.min,options.max)
histoDown=data.drawTH1(options.var+"Down",options.cut,"1",options.bins,options.min,options.max)
histoRUp=data.drawTH1(options.var+"Smear",options.cut,"1",options.bins,options.min,options.max)
histoRDown=mirror(histo,histoRUp)



F=ROOT.TFile(options.output,"UPDATE")
F.cd()

histo.Write(options.name)
histoUp.Write(options.name+"_"+options.systName+"ScaleUp")
histoDown.Write(options.name+"_"+options.systName+"ScaleDown")
histoRUp.Write(options.name+"_"+options.systName+"ResUp")
histoRDown.Write(options.name+"_"+options.systName+"ResDown")

F.Close()



