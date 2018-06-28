#! /usr/bin/env python

import ROOT as rt
rt.gROOT.SetBatch(True)
from SimGeneral.MixingModule.mix_2016_25ns_Moriond17MC_PoissonOOTPU_cfi import mix

values=mix.input.nbPileupEvents.probValue

OutputFile=rt.TFile.Open('MCPUProfile.root','recreate')
pu_mc=rt.TH1F('pu_mc','pu_mc',74,0,74)

for i,val in enumerate(values):
    pu_mc.Fill(i+1,val)

pu_mc.Write()
OutputFile.Close()

