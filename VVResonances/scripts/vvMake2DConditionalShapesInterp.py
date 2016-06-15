#!/usr/bin/env python

import ROOT
from array import array
from CMGTools.VVResonances.plotting.TreePlotter import TreePlotter
from CMGTools.VVResonances.plotting.MergedPlotter import MergedPlotter
from CMGTools.VVResonances.statistics.Fitter import Fitter

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
         


def interpolate(histos,axis,options):
    #create 2D histogram
    histo2D=ROOT.TH2D("histo2D","histo2D",options.binsx,options.minx,options.maxx,options.binsy,options.miny,options.maxy)

    if options.fitFunc =="bernstein3": 
        order=3
    if options.fitFunc =="bernstein4": 
        order=4
    if options.fitFunc =="bernstein5": 
        order=5
    if options.fitFunc =="bifur": 
        order=3

    graphs=[]    
    for i in range(0,order):
        graphs.append(ROOT.TGraphErrors())



    #run the fits
    for N,h in enumerate(histos):
        center=axis.GetBinCenter(N+1)
        fitter=Fitter(['mjj'])
        fitter.w.var("mjj").setVal(40)
        fitter.w.var("mjj").setMax(options.maxy)
        fitter.w.var("mjj").setMin(options.miny)
        if options.fitFunc =="bernstein3": 
            fitter.bernstein('model','mjj',3)
        if options.fitFunc =="bernstein4": 
            fitter.bernstein('model','mjj',4)
        if options.fitFunc =="bernstein5": 
            fitter.bernstein('model','mjj',5)
        if options.fitFunc =="bifur": 
            fitter.bifur('model','mjj')



        fitter.importBinnedData(h,['mjj'],'data')   
        fitter.fit('model','data')
        fitter.fit('model','data')
        fitter.projection("model","data","mjj","debugProjectionFit_"+str(N)+".png")
        for j,g in enumerate(graphs):
            c,cerr=fitter.fetch("c_"+str(j))
            g.SetPoint(N,center,c)
            g.SetPointError(N,0.0,cerr)

    ##OK now interpolate and make histograms!
    #first make the function
    fitter=Fitter(['mjj'])
    if options.fitFunc =="bernstein3": 
        fitter.bernstein('model','mjj',3)
        order=3

    if options.fitFunc =="bernstein4": 
        fitter.bernstein('model','mjj',4)
        order=4

    if options.fitFunc =="bernstein5": 
        fitter.bernstein('model','mjj',5)
        order=5

    if options.fitFunc =="bifur": 
        fitter.bifur('model','mjj')
        order=3


    fitter.w.var("mjj").setVal(80)
    fitter.w.var("mjj").setMax(options.maxy)
    fitter.w.var("mjj").setMin(options.miny)
    for i in range(1,histo2D.GetNbinsX()+1):
        x=histo2D.GetXaxis().GetBinCenter(i)
        print 'Bin:',i,'Evaluating function at x=',x
        for j,g in enumerate(graphs):
            print "c_"+str(j),"=",g.Eval(x)
            fitter.w.var("c_"+str(j)).setVal(g.Eval(x,0,"S"))
    
        histogram=fitter.w.pdf("model").createHistogram("mjj",options.binsy)
        for k in range(1,histo2D.GetNbinsY()+1):
            bin=histo2D.GetBin(i,k)
            histo2D.SetBinContent(bin,histogram.GetBinContent(k))

    return graphs,histo2D        
    



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
parser.add_option("-N","--systName",dest="systName",help="name",default="histo variation name")
parser.add_option("-f","--fitFunc",dest="fitFunc",help="name",default="bernstein4")



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


histos=[]
histosSUP=[]
histosSDWN=[]
histosRUP=[]
histosRDWN=[]


bins=[500,600,700,800,900,1000,1100,1200,1300,1500,1750,2000,2500,3000,3500,4000,4500,5000]
axis=ROOT.TAxis(len(bins)-1,array('d',bins))



for i in range(1,axis.GetNbins()+1):
    center = axis.GetBinCenter(i)
    histo=data.drawTH1(options.vary,options.cut+"&&{MVV}>{low}&&{MVV}<={high}".format(MVV=options.varx,low=axis.GetBinLowEdge(i),high=axis.GetBinUpEdge(i)),"1",options.binsy,options.miny,options.maxy)
    histos.append(histo)

    



graphs,histo2D=interpolate(histos,axis,options)  
renormalizeHisto(histo2D)
#renormalizeHisto(histoSUP)
#renormalizeHisto(histoSDWN)
#renormalizeHisto(histoRUP)
#renormalizeHisto(histoRDWN)
  




F=ROOT.TFile(options.output,"UPDATE")
F.cd()
histo2D.Write(options.name)
for bin,g in enumerate(graphs):
    g.Write(options.name+"_"+str(bin+1))
F.Close()



