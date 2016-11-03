#!/usr/bin/env python

import ROOT
from array import array
import os, sys, re, optparse,pickle,shutil,json

def returnHisto(name,w,binsx,minx,maxx):
    histo=ROOT.TH1D(name,name,binsx,minx,maxx)
    for i in range(1,histo.GetNbinsX()+1):
        bin=i
        x=histo.GetXaxis().GetBinCenter(i)
        w.var("MVV").setVal(x)
        val=w.pdf("pdf").getVal()
        histo.SetBinContent(bin,val)
#        sumi=sumi+val
#        if sumi>0: #renormalize    
#            for j in range(1,histo.GetNbinsY()+1):
#                bin=histo.GetBin(i,j)
#                histo.SetBinContent(bin,histo.GetBinContent(bin)/sumi)
    histo.Scale(1.0/histo.Integral())        
    return histo


parser = optparse.OptionParser()
parser.add_option("-s","--systSlope",dest="systSlope",default='',help="Comma   separated and semicolon separated systs for p0 ")
parser.add_option("-m","--systMean",dest="systMean",default='',help="Comma   separated and semicolon separated systs for p1 ")
parser.add_option("-w","--systWidth",dest="systWidth",default='',help="Comma   separated and semicolon separated systs for p2")
parser.add_option("-o","--output",dest="output",help="Output ROOT File",default='')
parser.add_option("-b","--binsx",dest="binsx",type=int, help="bins x",default=0)
parser.add_option("-x","--minx",dest="minx",type=float, help="min x",default=0.0)
parser.add_option("-X","--maxx",dest="maxx",type=float, help="maximum x",default=0.0)
parser.add_option("-n","--name",dest="name",help="histoName",default="test")

(options,args) = parser.parse_args()
#define output dictionary




ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")

jsonFile=open(args[0])
dataInfo=json.load(jsonFile)
jsonFile.close()

w=ROOT.RooWorkspace("w","w")

w.factory("MVV[0,100000]")

syst0Str='0'
syst1Str='0'
syst2Str='0'


systsV0=[]
systsV1=[]
systsV2=[]


systs0={}
for s in options.systSlope.split(','):
    if len(s)==0:
        continue
    tmp=s.split(':')
    systs0[tmp[0]] ={'factor':tmp[1],'unc':float(tmp[2])}

systs1={}
for s in options.systMean.split(','):
    if len(s)==0:
        continue
    tmp=s.split(':')
    systs1[tmp[0]] ={'factor':tmp[1],'unc':float(tmp[2])}

systs2={}
for s in options.systWidth.split(','):
    if len(s)==0:
        continue
    tmp=s.split(':')
    systs2[tmp[0]] ={'factor':tmp[1],'unc':float(tmp[2])}




systUnc={}

for syst,info in systs0.iteritems():
    systUnc[syst]=info['unc']
    factor = info['factor']
    w.factory(syst+"[0,-0.5,0.5]")
    syst0Str+="+{factor}*{syst}".format(factor=factor,syst=syst)
    systsV0.append(syst)

for syst,info in systs1.iteritems():
    systUnc[syst]=info['unc']
    factor = info['factor']
    w.factory(syst+"[0,-0.5,0.5]")
    syst1Str+="+{factor}*{syst}".format(factor=factor,syst=syst)
    systsV1.append(syst)

for syst,info in systs2.iteritems():
    systUnc[syst]=info['unc']
    factor = info['factor']
    w.factory(syst+"[0,-0.5,0.5]")
    syst2Str+="+{factor}*{syst}".format(factor=factor,syst=syst)
    systsV2.append(syst)


w.factory("expr::p0('({param})*(1+{syst})',{systs})".format(param=str(dataInfo['p0']),syst=syst0Str,systs=','.join(systsV0)))
w.factory("expr::p1('({param})*(1+{syst})',{systs})".format(param=str(dataInfo['p1']),syst=syst1Str,systs=','.join(systsV1)))
w.factory("expr::p2('({param})*(1+{syst})',{systs})".format(param=str(dataInfo['p2']),syst=syst2Str,systs=','.join(systsV2)))
pdf = ROOT.RooErfPowPdf("pdf","pdf",w.var("MVV"),w.function("p0"),w.function("p1"),w.function("p2"))
getattr(w,'import')(pdf,ROOT.RooFit.Rename('pdf'))
f=ROOT.TFile(options.output,"RECREATE")
f.cd()

#create nominal:
nominal=returnHisto(options.name,w,options.binsx,options.minx,options.maxx)
nominal.Write()

for syst,unc in systUnc.iteritems():
    w.var(syst).setVal(0+3*unc)
    h=returnHisto(options.name+"_"+syst+"Up",w,options.binsx,options.minx,options.maxx)
    h.Write()
    w.var(syst).setVal(0-3*unc)
    h=returnHisto(options.name+"_"+syst+"Down",w,options.binsx,options.minx,options.maxx)
    h.Write()
    w.var(syst).setVal(0)

f.Close()
