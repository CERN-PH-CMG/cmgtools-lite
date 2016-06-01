#!/usr/bin/env python
from ROOT import *

# from $CMSSW_RELEASE_BASE/src/SimGeneral/MixingModule/python/mix_2015_25ns_Startup_PoissonOOTPU_cfi.py

nVtxlist = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52]
nProbslist = [
    4.8551E-07,
    1.74806E-06,
    3.30868E-06,
    1.62972E-05,
    4.95667E-05,
    0.000606966,
    0.003307249,
    0.010340741,
    0.022852296,
    0.041948781,
    0.058609363,
    0.067475755,
    0.072817826,
    0.075931405,
    0.076782504,
    0.076202319,
    0.074502547,
    0.072355135,
    0.069642102,
    0.064920999,
    0.05725576,
    0.047289348,
    0.036528446,
    0.026376131,
    0.017806872,
    0.011249422,
    0.006643385,
    0.003662904,
    0.001899681,
    0.00095614,
    0.00050028,
    0.000297353,
    0.000208717,
    0.000165856,
    0.000139974,
    0.000120481,
    0.000103826,
    8.88868E-05,
    7.53323E-05,
    6.30863E-05,
    5.21356E-05,
    4.24754E-05,
    3.40876E-05,
    2.69282E-05,
    2.09267E-05,
    1.5989E-05,
    4.8551E-06,
    2.42755E-06,
    4.8551E-07,
    2.42755E-07,
    1.21378E-07,
    4.8551E-08,
    0 # added by Artur -- missing 53th entry in cfi
    ]

print len(nVtxlist), len(nProbslist)

# write to file
fPUmc = TFile("mcSpring15_25ns_pu.root","RECREATE")
## define PU Histo
#hPUmc = TH1F("pileup","MC pileup for 25ns Spring15",len(nVtxlist),nVtxlist[0]-0.5,nVtxlist[-1]+0.5)
hPUmc = TH1F("pileup","MC pileup for 25ns Spring15",len(nVtxlist),nVtxlist[0],nVtxlist[-1]+1)
#hPUmc = TH1F("pileup","MC pileup for 25ns Spring15",53,-0.5,52.5)

for i in range(0,len(nVtxlist)):
    hPUmc.SetBinContent(i+1,nProbslist[i])

hPUmc.Write()
fPUmc.Close()
