import ROOT
from array import array
import copy,re,os
import os, re

cardRegex = "higgsCombinekt_(?P<kt>.*)_kv_(?P<kv>.*)_zero.MultiDimFit.mH125.root"
scanName  = "dnn_ktkv"
cardDirectory="."
outputDirectory="dnn_ktkv"

os.system('mkdir -p ' + outputDirectory ) 

point_kv='1p0'
csvfname = 'nll_scan%s.csv' % point_kv
csvfile = open(csvfname, 'w')

cards = {}
pattern = re.compile( cardRegex ) 


csvfile.write("fname,cv,cf,ratio,nllr1,nllr0\n")

for card in os.listdir(cardDirectory + '/'): 
    match = pattern.search( card )
    if not match: continue
    xi = match.group('kt')
    yi = match.group('kv')
    if yi != point_kv: continue
    point = (xi.replace('p','.'), yi.replace('p','.'))
    quot=float(xi.replace('p','.').replace('m','-'))/float(yi.replace('p','.'))
    
    f1 = ROOT.TFile.Open('higgsCombinekt_'+xi+'_kv_'+yi+'_one.MultiDimFit.mH125.root', "read")
    f2 = ROOT.TFile.Open('higgsCombinekt_'+xi+'_kv_'+yi+'_zero.MultiDimFit.mH125.root', "read")

    k  = [event.deltaNLL for event in f1.limit]
    k2 = [event.deltaNLL for event in f2.limit]

    #write
    csvfile.write(','.join(map(str, [card.replace('zero',''), point[1], point[0], quot, k[1] ,k2[1]])) + '\n')

