#!/usr/bin/env python

import ROOT
from array import array
import os, sys, re, optparse,pickle,shutil,json

parser = optparse.OptionParser()
parser.add_option("-o","--output",dest="output",help="output JSON file",default='hvt_sigma.json')
(options,args) = parser.parse_args()


info={}

f=open(args[0])

for line in f:
    obj=line.split(',')
    if obj[0]=='M0':
        continue
    
    data =map(float,obj)

    lineinfo={ 'g':data[2],'gv':data[3],'ch':data[4],'cq':data[5],'cl':data[6],'c3':data[7],'cvvw':data[8],'cvvhh':data[9],'cvvv':data[10],'width0':data[11],'BRWW':data[12],'BRZH':data[13],'BRuu':data[14],'BRdd':data[15],'BRll':data[16],'BRnunu':data[17],'BRbb':data[18],'BRtt':data[19],\
                   'width+':data[20],'BRWZ':data[21],'BRWgamma':data[22],'BRWh':data[23],'BRud':data[24],'BRus':data[25],'BRlnu':data[26],'BRtb':data[27],'sigma+':data[28],'sigma0':data[29],'sigma-':data[30]}

    info[int(data[0])]=lineinfo


f.close()

f=open(options.output,'w')
json.dump(info,f)
f.close()







