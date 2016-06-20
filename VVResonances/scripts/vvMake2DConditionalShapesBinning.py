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
parser.add_option("-b","--binningx",dest="binningx",help="binning  in x",default="")
parser.add_option("-B","--binningy",dest="binningy",help="binning in y",default="")
parser.add_option("-n","--name",dest="name",help="name",default="histo")
parser.add_option("-N","--systName",dest="systName",help="name",default="histo variation name")



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

binningx=map(float,options.binningx.split(','))
binningy=map(float,options.binningy.split(','))



#STandard histogramming
histo=data.drawTH2Binned(options.vary+":"+options.varx,options.cut,"1",binningx,binningy)
histoSUP=data.drawTH2Binned(options.vary+"Up:"+options.varx,options.cut,"1",binningx,binningy)
histoSDWN=data.drawTH2Binned(options.vary+"Down:"+options.varx,options.cut,"1",binningx,binningy)
histoRUP=data.drawTH2Binned(options.vary+"Smear:"+options.varx,options.cut,"1",binningx,binningy)
histoRDWN = mirror(histo,histoRUP)
    


    
renormalizeHisto(histo)
renormalizeHisto(histoSUP)
renormalizeHisto(histoSDWN)
renormalizeHisto(histoRUP)
renormalizeHisto(histoRDWN)
  




F=ROOT.TFile(options.output,"UPDATE")
F.cd()
histo.Write(options.name)
histoSUP.Write(options.name+"_"+options.systName+"ScaleUp")
histoSDWN.Write(options.name+"_"+options.systName+"ScaleDown")
histoRUP.Write(options.name+"_"+options.systName+"ResUp")
histoSDWN.Write(options.name+"_"+options.systName+"ResDown")
F.Close()



