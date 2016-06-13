#!/usr/bin/env python

import ROOT
from array import array
from CMGTools.VVResonances.plotting.TreePlotter import TreePlotter
from CMGTools.VVResonances.plotting.MergedPlotter import MergedPlotter
from CMGTools.VVResonances.statistics.Fitter import Fitter
from math import log
import os, sys, re, optparse,pickle,shutil,json
ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")
import copy



parser = optparse.OptionParser()
parser.add_option("-s","--samples",dest="samples",default='',help="Type of sample")
parser.add_option("-c","--cut",dest="cut",help="Cut to apply for yield",default='')
parser.add_option("-o","--output",dest="output",help="Output ROOT",default='')
parser.add_option("-v","--varx",dest="varx",help="variablex",default='lnujj_LV_mass')
parser.add_option("-b","--binsx",dest="binsx",type=int,help="bins in x",default=1000)
parser.add_option("-x","--minx",dest="minx",type=float,help="minimum x",default=600)
parser.add_option("-X","--maxx",dest="maxx",type=float, help="maximum x",default=5000)
parser.add_option("-V","--vary",dest="vary",help="variablex",default='lnujj_l2_pruned_mass')
parser.add_option("-B","--binsy",dest="binsy",type=int,help="bins in x",default=20)
parser.add_option("-y","--miny",dest="miny",type=float,help="minimum y",default=0)
parser.add_option("-Y","--maxy",dest="maxy",type=float, help="maximum y",default=160)
parser.add_option("-l","--lumi",dest="lumi",type=float, help="lumi",default=7700)

(options,args) = parser.parse_args()

def returnString(variable,w):
    if variable =='c1':
        return "(({x0})+({x1})*mjj+({x2})*mjj*mjj+({x3})*mjj*mjj*mjj)".format(x0=w.var(variable+"_0").getVal(),x1=w.var(variable+"_1").getVal(),x2=w.var(variable+"_2").getVal(),x3=w.var(variable+'_3').getVal())
    if variable =='c2':
        return "(({x0})+({x1})*mjj+({x2})*mjj*mjj)".format(x0=w.var(variable+"_0").getVal(),x1=w.var(variable+"_1").getVal(),x2=w.var(variable+"_2").getVal())
    if variable=='c0':
        return "({x0})".format(x0=w.var("c0").getVal())


    


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
histo = data.drawTH2(options.vary+":"+options.varx,options.cut,str(options.lumi),options.binsx,options.minx,options.maxx,options.binsy,options.miny,options.maxy) 
histo=copy.deepcopy(histo)
fitter=Fitter(['M','m'])
fitter.w.var("M").setVal((options.maxx-options.minx)/2.0)
fitter.w.var("M").setMax(options.maxx)
fitter.w.var("M").setMin(options.minx)
fitter.w.var("m").setVal((options.maxy-options.miny)/2.0)
fitter.w.var("m").setMax(options.maxy)
fitter.w.var("m").setMin(options.miny)
fitter.erfpowParam('model',['M','m'])
fitter.importBinnedData(histo,['M','m'],'data')   
fitter.fit('model','data',[ROOT.RooFit.SumW2Error(0),ROOT.RooFit.ConditionalObservables(ROOT.RooArgSet(fitter.w.var('m')))])
fitter.fit('model','data',[ROOT.RooFit.SumW2Error(0),ROOT.RooFit.ConditionalObservables(ROOT.RooArgSet(fitter.w.var('m')))])
fitter.projectionCond("model","data","M","m",'debug'+options.output+".png")




data={}

data['p0']=returnString('c0',fitter.w)
data['p1']=returnString('c1',fitter.w)
data['p2']=returnString('c2',fitter.w)
f=open(options.output+".json","w")
json.dump(data,f)
f.close()


    
    
    



