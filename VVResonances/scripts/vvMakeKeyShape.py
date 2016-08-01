#!/usr/bin/env python

import ROOT
from array import array
from CMGTools.VVResonances.plotting.TreePlotter import TreePlotter
from CMGTools.VVResonances.plotting.MergedPlotter import MergedPlotter
from math import log
import os, sys, re, optparse,pickle,shutil,json



def mirror(histo,histoRUp):
    histoRDwn=histoRUp.Clone()
    for i in range(1,histo.GetNbinsX()+1):
        for j in range(1,histo.GetNbinsY()+1):
            bin=histo.GetBin(i,j)
            if histoRUp.GetBinContent(bin)>0:
                histoRDwn.SetBinContent(bin,histo.GetBinContent(bin)/histoRUp.GetBinContent(bin))
            else:   
                histoRDwn.SetBinContent(bin,histo.GetBinContent(bin))
    return histoRDwn        



def renormalizeHisto(histo):
    for i in range(1,histo.GetNbinsX()+1):
        integral=0.0
        for j in range(1,histo.GetNbinsY()+1):
            bin=histo.GetBin(i,j)
            integral=integral+histo.GetBinContent(bin)
        if integral==0.0:
            continue
        
        for j in range(1,histo.GetNbinsY()+1):
            bin=histo.GetBin(i,j)
            c=histo.GetBinContent(bin)
            e=histo.GetBinError(bin)
            histo.SetBinContent(bin,c/integral)
            histo.SetBinError(bin,e/integral)
         





parser = optparse.OptionParser()
parser.add_option("-s","--samples",dest="samples",default='',help="Type of sample")
parser.add_option("-c","--cut",dest="cut",help="Cut to apply for yield",default='')
parser.add_option("-o","--output",dest="output",help="Output ROOT",default='')
parser.add_option("-v","--varx",dest="varx",help="variablex",default='')
parser.add_option("-V","--vary",dest="vary",help="variablex",default='')
parser.add_option("-b","--binsx",dest="binsx",type=int,help="bins in x",default=20)
parser.add_option("-B","--binsy",dest="binsy",type=int,help="bins in x",default=20)
parser.add_option("-x","--minx",dest="minx",type=float,help="minimum x",default=0)
parser.add_option("-X","--maxx",dest="maxx",type=float, help="maximum x",default=160)
parser.add_option("-y","--miny",dest="miny",type=float,help="minimum y",default=0)
parser.add_option("-Y","--maxy",dest="maxy",type=float, help="maximum y",default=160)
parser.add_option("-n","--name",dest="name",help="name",default="histo")




(options,args) = parser.parse_args()



#Initialize plotters


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


#STandard histogramming
histo=data.drawTH2Keys(options.varx+","+options.vary,options.cut,options.binsx,options.minx,options.maxx,options.binsy,options.miny,options.maxy)
if histo.Integral()>0:
    histoNorm=data.drawTH2(options.vary+":"+options.varx,options.cut,"1",options.binsx,options.minx,options.maxx,options.binsy,options.miny,options.maxy)
    histo.Scale(1.0/histo.Integral())
    histo.Scale(histoNorm.Integral())
    F=ROOT.TFile(options.output,"UPDATE")
    F.cd()
    histo.Write(options.name)
    F.Close()
else: 
    print 'No events to make keys with after cut!'



