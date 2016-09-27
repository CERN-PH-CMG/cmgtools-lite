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
parser.add_option("-l","--lumi",dest="lumi",type=float, help="lumi",default=7700)

(options,args) = parser.parse_args()

def returnString(func,options):
    varName="MH"
    if func.GetName().find("pol")!=-1:
        st='0'
        for i in range(0,func.GetNpar()):
            st=st+"+("+str(func.GetParameter(i))+")"+(("*"+varName)*i)
        return st    
    elif func.GetName().find("log")!=-1:
        return str(func.GetParameter(0))+"+("+str(func.GetParameter(1))+")*log("+varName+")"
    else:
        return ""



def runFits(data,options):
    axis=ROOT.TAxis(5,array('d',[600,700,800,900,1000,2000]))

   #first pass     
    graphs=[]
    for i in range(0,12):
        graphs.append(ROOT.TGraphErrors())

    for i in range(1,axis.GetNbins()+1):
    
        center=axis.GetBinCenter(i)
        h = data.drawTH1(options.varx,options.cut+"&&({vary}>{mini}&&{vary}<{maxi})".format(vary=options.vary,mini=axis.GetBinLowEdge(i),maxi=axis.GetBinUpEdge(i)),str(options.lumi),options.binsx,options.minx,options.maxx) 

        histo=copy.deepcopy(h)
        fitter=Fitter(['M'])
        fitter.w.var("M").setVal((options.maxx-options.minx)/2.0)
        fitter.w.var("M").setMax(options.maxx)
        fitter.w.var("M").setMin(options.minx)


        fitter.signalMJJCBBoth('model','M')
        fitter.importBinnedData(histo,['M'],'data')   
        fitter.fit('model','data',[ROOT.RooFit.SumW2Error(0)])
        chi=fitter.projection("model","data","M","debugfitMJJTop_"+options.output+"_"+str(i)+".png")
    
        for j,g in enumerate(graphs):
            c,cerr=fitter.fetch("c_"+str(j))
            g.SetPoint(i-1,center,c)
            g.SetPointError(i-1,0.0,cerr)



    data={}
    pol4=ROOT.TF1("pol4","pol4",options.minx,options.maxx)
    pol3=ROOT.TF1("pol3","pol3",options.minx,options.maxx)
    pol2=ROOT.TF1("pol2","pol2",options.minx,options.maxx)
    pol1=ROOT.TF1("pol1","pol1",options.minx,options.maxx)
    pol0=ROOT.TF1("pol0","pol0",options.minx,options.maxx)



    graphs[0].Fit(pol1)
    data['mean']=returnString(pol1,options)

    graphs[1].Fit(pol1)
    data['sigma']=returnString(pol1,options)

    graphs[2].Fit(pol0)
    data['alpha1']=returnString(pol0,options)

    graphs[3].Fit(pol0)
    data['n1']=returnString(pol0,options)

    graphs[4].Fit(pol1)
    data['alpha2']=returnString(pol1,options)

    graphs[5].Fit(pol0)
    data['n2']=returnString(pol0,options)

    #create json
    f=open(options.output+"_W.json","w")
    json.dump(data,f)
    f.close()

    data={}

    graphs[6].Fit(pol1)
    data['mean']=returnString(pol1,options)

    graphs[7].Fit(pol1)
    data['sigma']=returnString(pol1,options)

    graphs[8].Fit(pol0)
    data['alpha1']=returnString(pol0,options)

    graphs[9].Fit(pol0)
    data['n1']=returnString(pol0,options)

    graphs[10].Fit(pol1)
    data['alpha2']=returnString(pol1,options)

    graphs[11].Fit(pol0)
    data['n2']=returnString(pol0,options)
    f=open(options.output+"_top.json","w")
    json.dump(data,f)
    f.close()
    return graphs



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






graphs=runFits(data,options)

f=ROOT.TFile(options.output+".root","RECREATE")
f.cd()
for i,g in enumerate(graphs):
    g.Write("p"+str(i))
f.Close()

    
    
    



