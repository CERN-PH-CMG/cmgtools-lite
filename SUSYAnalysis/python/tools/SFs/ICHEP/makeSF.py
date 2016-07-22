#!/usr/bin/env python

import sys, glob, os
from ROOT import *

f1_ele = TFile.Open('GsfElectronToTight.root', 'read') 
f2_ele = TFile.Open('MVAVLooseElectronToMini.root', 'read')

f1_mu = TFile.Open('TnP_MuonID_NUM_MediumID_DENOM_generalTracks_VAR_map_pt_eta.root', 'read')
f2_mu = TFile.Open('TnP_MuonID_NUM_MiniIsoTight_DENOM_MediumID_VAR_map_pt_eta.root', 'read')
f3_mu = TFile.Open('TnP_MuonID_NUM_TightIP3D_DENOM_MediumID_VAR_map_pt_eta.root', 'read')
f4_mu = TFile.Open('general_tracks_and_early_general_tracks_corr_ratio.root', 'read')


h1_ele = f1_ele.Get('probe_Ele_pt_probe_sc_abseta_PLOT')
h2_ele = f2_ele.Get('probe_Ele_pt_probe_sc_abseta_PLOT')

h12_ele = h1_ele.Clone()
h12_ele.Multiply(h2_ele)
h12_ele.SetName('CBtight_miniIso0p2_ICHEP')
h12_ele.SetTitle('CBtight_miniIso0p2_ICHEP')
h12_ele.SaveAs('CBtight_miniIso0p2_ICHEP.root')


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

h1234_mu = h123_mu.Clone()
etabins = h123_mu.GetNbinsY()
ptbins = h123_mu.GetNbinsX()

for eta in range(1,etabins+1):
    HIPfactor = h4_mu.GetBinContent(eta)
    for pt in range(1,ptbins+1):
        before = h123_mu.GetBinContent(pt, eta)
        after = before * HIPfactor
        print before, after, HIPfactor
        h1234_mu.SetBinContent(pt, eta, after)

h1234_mu.SetName("MediumMuon_miniIso0p2_SIP3D_HIP_ICHEP")
h1234_mu.SetTitle("MediumMuon_miniIso0p2_SIP3D_HIP_ICHEP")
h1234_mu.SaveAs("MediumMuon_miniIso0p2_SIP3D_HIP_ICHEP.root")
        
