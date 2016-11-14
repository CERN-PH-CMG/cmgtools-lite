#! /usr/bin/env python

import os
import re
import ROOT as rt
rt.gROOT.SetBatch(True)

# PU profile for Spring16 MC: $CMSSW_RELEASE_BASE/src/SimGeneral/MixingModule/python/mix_2016_25ns_SpringMC_PUScenarioV1_PoissonOOTPU_cfi.py

mixingfile = 'mix_2016_25ns_SpringMC_PUScenarioV1_PoissonOOTPU_cfi.py'
pufile=os.environ['CMSSW_RELEASE_BASE']+'/src/SimGeneral/MixingModule/python/'+mixingfile

OutputFile=rt.TFile.Open('MCPUProfile.root','recreate')
pu_mc=rt.TH1F('pu_mc','pu_mc',49,0,49)

startHisto=False
b=0
for line in open(pufile):
    lines=line.rstrip('\n')
    if 'probValue' in lines: startHisto=True
    matchObj = re.match( r'\s+(\d.\S+),',lines)
    matchLastBin = re.match( r'\s+(\d.\d+)\s\),',lines)
    if startHisto and matchObj:
        val = matchObj.group(1)
        print 'Filling PU bin ',b,' with weight ',float(val)
        pu_mc.Fill(b,float(val))
        b += 1
    if startHisto and matchLastBin:
        val = matchLastBin.group(1)
        print 'Filling last PU bin ',b,' with weight ',float(val)
        pu_mc.Fill(b,float(val))
        startHisto = False

pu_mc.Write()
OutputFile.Close()
