#!/usr/bin/env python

import sys, glob, os
from ROOT import *

f1_ele = TFile.Open('GsfElectronToTight.root', 'read') 
f2_ele = TFile.Open('MVAVLooseElectronToMini.root', 'read')
f3_ele = TFile.Open('egammaEffi.txt_SF2D.root', 'read')

f1_mu = TFile.Open('TnP_MuonID_NUM_MediumID_DENOM_generalTracks_VAR_map_pt_eta.root', 'read')
f2_mu = TFile.Open('TnP_MuonID_NUM_MiniIsoTight_DENOM_MediumID_VAR_map_pt_eta.root', 'read')
f3_mu = TFile.Open('TnP_MuonID_NUM_TightIP3D_DENOM_MediumID_VAR_map_pt_eta.root', 'read')
f4_mu = TFile.Open('general_tracks_and_early_general_tracks_corr_ratio.root', 'read')


h1_ele = f1_ele.Get('h2_scaleFactorsEGamma')
h2_ele = f2_ele.Get('h2_scaleFactorsEGamma')
h3_ele = f3_ele.Get('EGamma_SF2D')

h12_ele = h1_ele.Clone()
h12_ele.Multiply(h2_ele)
h12_ele.SetName('CBtight_miniIso0p1_ICHEP')
h12_ele.SetTitle('CBtight_miniIso0p1_ICHEP')
h12_ele.SaveAs('CBtight_miniIso0p1_ICHEP.root')


h123_ele = h12_ele.Clone()
etabins = h12_ele.GetNbinsY()
ptbins = h12_ele.GetNbinsX()

##########################
####MUONS##############
h1_mu = f1_mu.Get('pt_abseta_PLOT_pair_probeMultiplicity_bin0')
h2_mu = f2_mu.Get('pt_abseta_PLOT_pair_probeMultiplicity_bin0_&_Medium2016_pass')
h3_mu = f3_mu.Get('pt_abseta_PLOT_pair_probeMultiplicity_bin0_&_Medium2016_pass')

h4_mu = f4_mu.Get('mutrksfptg10')

h123_mu = h1_mu.Clone()
h123_mu.Multiply(h2_mu)
h123_mu.Multiply(h3_mu)
h123_mu.SetName("MediumMuon_miniIso0p2_SIP3D_ICHEP")
h123_mu.SetTitle("MediumMuon_miniIso0p2_SIP3D_ICHEP")
h123_mu.SaveAs("MediumMuon_miniIso0p2_SIP3D_ICHEP.root")

        
