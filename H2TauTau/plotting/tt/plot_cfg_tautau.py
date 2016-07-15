from collections import namedtuple

from CMGTools.H2TauTau.proto.samples.spring16.htt_common import lumi_tt as lumi
from CMGTools.H2TauTau.proto.plotter.PlotConfigs       import SampleCfg, HistogramCfg, VariableCfg
from CMGTools.H2TauTau.proto.plotter.categories_TauTau import inc_sig_tau1_iso, inc_sig_tau2_iso, inc_sig_no_iso
from CMGTools.H2TauTau.proto.plotter.categories_common import cat_J1, cat_VBF
from CMGTools.H2TauTau.proto.plotter.HistCreator       import createHistograms
from CMGTools.H2TauTau.proto.plotter.HistDrawer        import HistDrawer
from CMGTools.H2TauTau.proto.plotter.Variables         import tautau_vars, getVars
from CMGTools.H2TauTau.proto.plotter.Samples           import createSampleLists
from CMGTools.H2TauTau.proto.plotter.qcdEstimation     import qcd_estimation
from CMGTools.H2TauTau.proto.plotter.cut               import Cut

int_lumi = lumi
analysis_dir = '/data1/steggema/tt/140716/DiTauMC'
verbose = True
total_weight = 'weight'

samples_mc, samples_data, samples, all_samples, sampleDict = createSampleLists(analysis_dir=analysis_dir, channel='tt', ztt_cut='(l2_gen_match == 5 && l1_gen_match == 5)', zl_cut='(l1_gen_match < 6 && l2_gen_match < 6 && !(l1_gen_match == 5 && l2_gen_match == 5))',
                      zj_cut='(l2_gen_match == 6 || l1_gen_match == 6)')

myCut = namedtuple('myCut', ['name', 'cut'])
cuts = []

# categories, do not include charge and iso cuts
inc_cut  = inc_sig_no_iso
jet1_cut = inc_sig_no_iso & Cut(cat_J1)
vbf_cut  = inc_sig_no_iso & Cut(cat_VBF)

# iso and charge cuts, need to have them explicitly for the QCD estimation
iso_cut          = inc_sig_tau1_iso & inc_sig_tau2_iso
max_iso_cut      = Cut('l1_byIsolationMVArun2v1DBoldDMwLT > 1.5 && l2_byIsolationMVArun2v1DBoldDMwLT > 1.5')
iso_sideband_cut = (~iso_cut) & max_iso_cut
charge_cut       = Cut('l1_charge != l2_charge')

# append categories to plot
cuts.append(myCut('inclusive', inc_cut ))
# cuts.append(myCut('1jet'     , jet1_cut))
# cuts.append(myCut('vbf'      , vbf_cut ))

# Taken from Variables.py, can get subset with e.g. getVars(['mt', 'mvis'])
variables = tautau_vars
# variables = getVars(['mvis', 'l1_pt', 'l2_pt']) #, 'l1_pt', 'l2_pt'])

for cut in cuts:
    all_samples_qcd = qcd_estimation(
        cut.cut & iso_sideband_cut &   charge_cut , # shape sideband
        cut.cut & iso_cut          & (~charge_cut), # norm sideband 1
        cut.cut & iso_sideband_cut & (~charge_cut), # norm sideband 2
        samples,
        int_lumi, 
        total_weight,
        verbose=verbose
    )
    
    # now include charge and isolation too
    cut = myCut(cut.name, cut.cut & iso_cut & charge_cut)
    
    # for variable in variables:
    cfg_total = HistogramCfg(name=cut.name, vars=variables, cfgs=all_samples_qcd, cut=str(cut.cut), lumi=int_lumi, weight=total_weight)
    all_samples_qcd[-1].vars = variables
    plots = createHistograms(cfg_total, verbose=True)
    for variable in variables:
        plot = plots[variable.name]
        plot.Group('VV', ['ZZTo2L2Q', 'WWTo1L1Nu2Q', 'WZTo1L3Nu', 'ZZTo4L', 'WZTo3L', 'WZTo2L2Q', 'WZTo1L1Nu2Q', 'T_tWch', 'TBar_tWch', 'TToLeptons_tch_powheg', 'TBarToLeptons_tch_powheg'])
        # plot.Group('ZTT', ['ZTT', 'ZTT1Jets', 'ZTT2Jets', 'ZTT3Jets', 'ZTT4Jets'])
        # plot.Group('ZJ', ['ZJ', 'ZJ1Jets', 'ZJ2Jets', 'ZJ3Jets', 'ZJ4Jets'])
        # plot.Group('ZL', ['ZL', 'ZL1Jets', 'ZL2Jets', 'ZL3Jets', 'ZL4Jets'])
        plot.Group('WJets'  , ['WJetsToLNu', 'W1JetsToLNu', 'W4JetsToLNu'])
        plot.Group('Single t', ['T_tWch', 'TBar_tWch', 'TToLeptons_sch', 'TToLeptons_tch'])

        HistDrawer.draw(plot, channel='#tau_{h}#tau_{h}', plot_dir='plot_%s' %cut.name)
        # HistDrawer.drawRatio(plot, channel='#tau_{h}#tau_{h}')

        if variable.name == 'mvis':
            plot.WriteDataCard(filename='plot_%s/htt_tt.inputs-sm-13TeV.root' %cut.name, dir='tt_' + cut.name, mode='UPDATE')
        if variable.name == 'svfit_mass':
            plot.WriteDataCard(filename='plot_%s/htt_tt.inputs-sm-13TeV_svFit.root' %cut.name, dir='tt_' + cut.name, mode='UPDATE')
    
