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
parser.add_option("-i","--input",dest="input",help="inputJSON")

(options,args) = parser.parse_args()

def returnString(func,options):
    varName="MH"
    if func.GetName().find("pol")!=-1:
        st='0'
        for i in range(0,func.GetNpar()):
            st=st+"+("+str(func.GetParameter(i))+")"+(("*"+varName)*i)
        return st    
    elif func.GetName().find("log")!=-1:
        return "("+str(func.GetParameter(0))+")+("+str(func.GetParameter(1))+")*log("+varName+")"
    else:
        return ""



def runFits(data,options,info):
    axis=ROOT.TAxis(8,array('d',[600,650,700,750,800,850,1000,1200,1400]))

   #first pass     
    graphs={'mean':ROOT.TGraphErrors(),'alpha2':ROOT.TGraphErrors(),'n2':ROOT.TGraphErrors()}

    for i in range(1,axis.GetNbins()+1):
    
        center=axis.GetBinCenter(i)
        h = data.drawTH1(options.varx,options.cut+"&&({vary}>{mini}&&{vary}<{maxi})".format(vary=options.vary,mini=axis.GetBinLowEdge(i),maxi=axis.GetBinUpEdge(i)),str(options.lumi),options.binsx,options.minx,options.maxx) 

        histo=copy.deepcopy(h)
        fitter=Fitter(['M'])
        fitter.w.var("M").setVal((options.maxx-options.minx)/2.0)
        fitter.w.var("M").setMax(options.maxx)
        fitter.w.var("M").setMin(options.minx)


        func=ROOT.TF1("func",info['mean'].replace("MH","x"),0,6000)       
#        fitter.w.factory("mean["+str(func.Eval(center))+"]")
        fitter.w.factory("mean[1,-20,20]")        
        fitter.w.factory("expr::mean2('{val}+mean',mean)".format(val=func.Eval(center)))

        func=ROOT.TF1("func",info['sigma'].replace("MH","x"),0,6000)       
        fitter.w.factory("sigma["+str(func.Eval(center))+"]")

        func=ROOT.TF1("func",info['alpha'].replace("MH","x"),0,6000)       
        fitter.w.factory("alpha["+str(func.Eval(center))+"]")

        func=ROOT.TF1("func",info['n'].replace("MH","x"),0,6000)       
        fitter.w.factory("n["+str(func.Eval(center))+"]")

        func=ROOT.TF1("func",info['slope'].replace("MH","x"),0,6000)       
        fitter.w.factory("slope["+str(func.Eval(center))+"]")

        func=ROOT.TF1("func",info['f'].replace("MH","x"),0,6000)       
        fitter.w.factory("f["+str(func.Eval(center))+"]")
        
        fitter.w.factory("alpha2[3,0.5,6]")
        fitter.w.factory("n2[6]")

        name='model'
        peak = ROOT.RooDoubleCB(name,'modelS',fitter.w.var("M"),fitter.w.function('mean2'),fitter.w.var('sigma'),fitter.w.var('alpha'),fitter.w.var('n'),fitter.w.var("alpha2"),fitter.w.var("n2"))
        getattr(fitter.w,'import')(peak,ROOT.RooFit.Rename(name+'S'))
#        fitter.w.factory("RooExponential::"+name+"B(M,slope)")       
#        fitter.w.factory("SUM::"+name+"(f*"+name+"S,"+name+"B)")
       
#        fitter.signalMJJCB('model','M')
        fitter.importBinnedData(histo,['M'],'data')   
        fitter.fit('model','data',[ROOT.RooFit.SumW2Error(1)])
        fitter.fit('model','data',[ROOT.RooFit.SumW2Error(1),ROOT.RooFit.Minos(1)])
        chi=fitter.projection("model","data","M","debugfitMJJTop_"+options.output+"_"+str(i)+".png")
    
        c,cerr=fitter.fetch('mean')
        graphs['mean'].SetPoint(i-1,center,c)
        graphs['mean'].SetPointError(i-1,0.0,c)

        c,cerr=fitter.fetch('alpha2')
        graphs['alpha2'].SetPoint(i-1,center,c)
        graphs['alpha2'].SetPointError(i-1,0.0,c)

        c,cerr=fitter.fetch('n2')
        graphs['n2'].SetPoint(i-1,center,c)
        graphs['n2'].SetPointError(i-1,0.0,c)


    data={}
    pol4=ROOT.TF1("pol4","pol4",options.minx,options.maxx)
    pol3=ROOT.TF1("pol3","pol3",options.minx,options.maxx)
    pol2=ROOT.TF1("pol2","pol2",options.minx,options.maxx)
    pol1=ROOT.TF1("pol1","pol1",options.minx,options.maxx)
    pol0=ROOT.TF1("pol0","pol0",options.minx,options.maxx)
    log=ROOT.TF1("log0","[0]+[1]*log(x)",options.minx,options.maxx)



    graphs['mean'].Fit(log)
    data['mean']=info['mean']+"+"+returnString(log,options)

    graphs['alpha2'].Fit(log)
    data['alpha2']=returnString(log,options)

    graphs['n2'].Fit(pol0)
    data['n2']=returnString(pol0,options)


#    data['mean']=info['mean']
    data['sigma']=info['sigma']
    data['alpha1']=info['alpha']
    data['n1']=info['n']

    
    #create json
    f=open(options.output+".json","w")
    json.dump(data,f)
    f.close()
    return graphs

#Initialize plotters


samples={}



f=open(options.input)
info=json.load(f)



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






graphs=runFits(data,options,info)

f=ROOT.TFile(options.output+".root","RECREATE")
f.cd()
for name,g in graphs.iteritems():
    g.Write(name)
f.Close()

    
    
    



