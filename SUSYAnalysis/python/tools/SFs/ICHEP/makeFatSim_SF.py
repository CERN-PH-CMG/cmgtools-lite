#!/usr/bin/env python

import sys, glob, os
from ROOT import *


f1_ele = TFile.Open('sf_el_mini01_FastSim.root', 'read') 
f2_ele = TFile.Open('sf_el_tightCB_FastSim.root', 'read')


f1_mu = TFile.Open('sf_mu_mediumID_mini02_FastSim.root', 'read')
f2_mu = TFile.Open('sf_mu_medium_FastSim.root', 'read')
f3_mu = TFile.Open('sf_mu_tightIP3D_FastSim.root', 'read')



h1_ele = f1_ele.Get('histo2D')
h2_ele = f2_ele.Get('histo2D')

h12_ele = h1_ele.Clone()
h12_ele.Multiply(h2_ele)

h12_ele.SetName('CBtight_miniIso0p1_FastSim_ICHEP')
h12_ele.SetTitle('CBtight_miniIso0p1_FastSim_ICHEP')
h12_ele.SaveAs('CBtight_miniIso0p1_FastSim_ICHEP.root')


##########################
####MUONS##############
h1_mu = f1_mu.Get('histo2D')
h2_mu = f2_mu.Get('histo2D')
h3_mu = f3_mu.Get('histo2D')

h123_mu = h1_mu.Clone()
h123_mu.Multiply(h2_mu)
h123_mu.Multiply(h3_mu)
h123_mu.SetName("MediumMuon_miniIso0p2_SIP3D_FastSim_ICHEP")
h123_mu.SetTitle("MediumMuon_miniIso0p2_SIP3D_FastSim_ICHEP")
h123_mu.SaveAs("MediumMuon_miniIso0p2_SIP3D_FastSim_ICHEP.root")

        
