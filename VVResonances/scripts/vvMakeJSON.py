#!/usr/bin/env python

import ROOT
from array import array
import os, sys, re, optparse,pickle,shutil,json

def returnString(func):
    if func.GetName().find("pol")!=-1:
        st='0'
        for i in range(0,func.GetNpar()):
            st=st+"+("+str(func.GetParameter(i))+")"+("*MH"*i)
        return st    
    elif func.GetName().find("llog")!=-1:
        return func.GetParameter(0)+"+"+func.GetParameter(1)+"*log(MH)"
    else:
        return ""

parser = optparse.OptionParser()
parser.add_option("-g","--graphs",dest="graphs",default='',help="Comma   separated graphs and functions to fit  like MEAN:pol3,SIGMA:pol2")
parser.add_option("-o","--output",dest="output",help="Output JSON",default='')
parser.add_option("-m","--min",dest="min",type=float, help="minimum x",default=0)
parser.add_option("-M","--max",dest="max",type=float, help="maximum x",default=0)


(options,args) = parser.parse_args()
#define output dictionary


rootFile=ROOT.TFile(args[0])


graphStr= options.graphs.split(',')
parameterization={}


for string in graphStr:
    comps =string.split(':')      
    graph=rootFile.Get(comps[0])
    if comps[1].find("pol")!=-1:
        func=ROOT.TF1(comps[1],comps[1],0,13000)
    elif  comps[1]=="llog":
        func=ROOT.TF1("llog","[0]+[1]*log(x)",1,13000)
        func.SetParameters(1,1)
    
    graph.Fit(func,"","",options.min,options.max)
    parameterization[comps[0]]=returnString(func)


f=open(options.output,"w")
json.dump(parameterization,f)
f.close()

