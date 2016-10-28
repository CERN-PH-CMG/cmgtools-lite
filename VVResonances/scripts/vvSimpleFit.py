#!/usr/bin/env python

import ROOT
from array import array
from CMGTools.VVResonances.statistics.Fitter import Fitter
from math import log
import os, sys, re, optparse,pickle,shutil,json
import json
from CMGTools.VVResonances.plotting.tdrstyle import *
setTDRStyle()

parser = optparse.OptionParser()
parser.add_option("-o","--output",dest="output",help="Output JSON",default='')
parser.add_option("-i","--histo",dest="histo",help="name",default="histo")
parser.add_option("-f","--function",dest="function",help="name",default="bernstein")
parser.add_option("-t","--title",dest="title",help="name",default="x")

(options,args) = parser.parse_args()


parameterization={}

f=ROOT.TFile(args[0])
histo=f.Get(options.histo)

fitter=Fitter(['x'])
fitter.importBinnedData(histo,['x'],'data')

if options.function=='expo':
    fitter.expo('model','x')
    parameterization['type']='expo'

if options.function=='erfpow':
    fitter.erfpow('model','x')
    parameterization['type']='erfpow'


if options.function=='erfexp':
    fitter.erfexp('model','x')
    parameterization['type']='erfexp'

if options.function=='erfexpCB':
    fitter.erfexpCB('model','x')
    parameterization['type']='erfexpCB'

if options.function=='erfexpTimesCB':
    fitter.erfexpTimesCB('model','x')
    parameterization['type']='erfexpTimesCB'


if options.function.find('bernstein')!=-1:
    order=int(options.function.split('_')[1])
    fitter.bernstein('model','x',order)
    parameterization['type']='bernstein'
    parameterization['order']=order

fitter.fit('model','data',[ROOT.RooFit.SumW2Error(1)])
fitter.fit('model','data',[ROOT.RooFit.SumW2Error(1)])

fitter.projection("model","data","x","debug"+options.output+".root",options.title)
fitter.projection("model","data","x","debug"+options.output+".png",options.title)



if parameterization['type']=='expo':
    val,err=fitter.fetch('c_0')
    parameterization['c_0']=val
    parameterization['c_0Err']=err


if parameterization['type']=='erfexp':
    for i in range(0,3):
        var='c_'+str(i)
        val,err=fitter.fetch(var)
        parameterization[var]=val
        parameterization[var+'Err']=err


if parameterization['type']=='erfpow':
    for i in range(0,3):
        var='c_'+str(i)
        val,err=fitter.fetch(var)
        parameterization['p'+str(i)]=val
        parameterization['p'+str(i)+'Err']=err


if parameterization['type']=='erfexpCB':
    for i in range(0,3):
        var='c_'+str(i)
        val,err=fitter.fetch(var)
        parameterization[var]=val
        parameterization[var+'Err']=err
    for var in ['mean','sigma','alpha1','n1','alpha2','n2','fR']:
        val,err=fitter.fetch(var)
        parameterization[var]=val
        parameterization[var+'Err']=err

if parameterization['type']=='erfexpTimesCB':
    for i in range(0,3):
        var='c_'+str(i)
        val,err=fitter.fetch(var)
        parameterization[var]=val
        parameterization[var+'Err']=err
    for var in ['mean','sigma','alpha1','n1','alpha2','n2']:
        val,err=fitter.fetch(var)
        parameterization[var]=val
        parameterization[var+'Err']=err


if parameterization['type']=='bernstein':
    for i in range(0,parameterization['order']):
        var='c_'+str(i)
        val,err=fitter.fetch(var)
        parameterization[var]=val
        parameterization[var+'Err']=err


f=open(options.output+".json","w")
json.dump(parameterization,f)
f.close()




