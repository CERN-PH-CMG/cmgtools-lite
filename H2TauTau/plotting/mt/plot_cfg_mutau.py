import copy
from numpy import array
from collections import namedtuple

from CMGTools.H2TauTau.proto.plotter.PlotConfigs import HistogramCfg, VariableCfg
from CMGTools.H2TauTau.proto.plotter.categories_TauMu import cat_Inc
from CMGTools.H2TauTau.proto.plotter.HistCreator import createHistograms, createHistogram
from CMGTools.H2TauTau.proto.plotter.HistDrawer import HistDrawer
from CMGTools.H2TauTau.proto.plotter.Variables import taumu_vars, getVars
# from CMGTools.H2TauTau.proto.plotter.helper_methods import getPUWeight

from CMGTools.H2TauTau.proto.plotter.Samples import createSampleLists

mode = 'sm'
# mode = 'mssm_signal' 
# mode = 'mssm_control'

int_lumi = 2301. # from Alexei's email
qcd_from_same_sign = True
w_qcd_mssm_method = True
r_qcd_os_ss = 1.17

analysis_dir = '/data1/steggema/mt/070416/TauMuSVFitMC/'
# analysis_dir = '/data1/steggema/mt/070416/TauMuSVFitMVA/'

total_weight = 'weight'#*weight_njet'

print total_weight

Cut = namedtuple('Cut', ['name', 'cut'])

cuts = []

inc_cut = '&&'.join([cat_Inc])
# inc_cut += '&& l2_decayModeFinding'

mt_cut = 'mt<30'
if mode == 'sm':
    mt_cut = 'mt<40'

binning_mssm = array([0.,10.,20.,30.,40.,50.,60.,70.,80.,90.,100.,110.,120.,130.,140.,150.,160.,170.,180.,190.,200.,225.,250.,275.,300.,325.,350.,400.,500.,700.,900.,1100.,1300.,1500.,1700.,1900.,2100.,2300.,2500.,2700.,2900.,3100.,3300.,3500.,3700.,3900.])

binning_mssm_btag = array([0.,20.,40.,60.,80.,100.,120.,140.,160.,180.,200.,250.,300.,350.,400.,500.,700.,900.,1100.,1300.,1500.,1700.,1900.,2100.,2300.,2500.,2700.,2900.,3100.,3300.,3500.,3700.,3900.])

cuts.append(Cut('inclusive', inc_cut + '&& l1_charge != l2_charge'))
# cuts.append(Cut('inclusive_tauisosideband', inc_cut.replace('l2_byIsolationMVArun2v1DBoldDMwLT>3.5', 'l2_byIsolationMVArun2v1DBoldDMwLT<3.5&&l2_byIsolationMVArun2v1DBoldDMwLT>0.5') + '&& l1_charge != l2_charge'))
cuts.append(Cut('inclusivemt40', inc_cut + '&& l1_charge != l2_charge && mt<40'))

# MSSM Categories

if 'mssm' in mode:
    cuts.append(Cut('nobtag', inc_cut + '&& l1_charge != l2_charge && n_bjets==0 && mt<30'))
    cuts.append(Cut('btag', inc_cut + '&& l1_charge != l2_charge && n_bjets>=1 && n_jets<=1 && mt<30'))
if mode == 'mssm_signal':
    cuts.append(Cut('nobtag_highmtos', inc_cut + '&& l1_charge != l2_charge && n_bjets==0 && mt>70'))
    cuts.append(Cut('nobtag_highmtss', inc_cut + '&& l1_charge == l2_charge && n_bjets==0 && mt>70'))
    cuts.append(Cut('nobtag_lowmtss', inc_cut + '&& l1_charge == l2_charge && n_bjets==0 && mt<30'))

if mode == 'mssm_signal':
    cuts.append(Cut('btag_highmtos', inc_cut + '&& l1_charge != l2_charge && n_bjets>=1 && n_jets<=1 && mt>70'))
    cuts.append(Cut('btag_highmtss', inc_cut + '&& l1_charge == l2_charge && n_bjets>=1 && n_jets<=1 && mt>70'))
    cuts.append(Cut('btag_lowmtss', inc_cut + '&& l1_charge == l2_charge && n_bjets>=1 && n_jets<=1 && mt<30'))

if mode == 'sm':
    cuts.append(Cut('mva_high', inc_cut + '&& l1_charge != l2_charge && mt<40 && mva>0.2'))
    cuts.append(Cut('mva_vhigh', inc_cut + '&& l1_charge != l2_charge && mt<40 && mva>0.5'))
    cuts.append(Cut('mva_low', inc_cut + '&& l1_charge != l2_charge && mt<40 && mva<0.2'))
    cuts.append(Cut('mva_high_vbf', inc_cut + '&& l1_charge != l2_charge && mt<40 && mva>0.4 && vbf_mjj>300 && abs(vbf_deta)>3.5'))
    cuts.append(Cut('mva_low_vbf', inc_cut + '&& l1_charge != l2_charge && mt<40 && mva<0.4 && vbf_mjj>300 && abs(vbf_deta)>3.5'))
    cuts.append(Cut('mva_high_1jet', inc_cut + '&& l1_charge != l2_charge && mt<40 && mva>0.2 && !(vbf_mjj>300 && abs(vbf_deta)>3.5) && n_jets>0.5'))
    cuts.append(Cut('mva_low_1jet', inc_cut + '&& l1_charge != l2_charge && mt<40 && mva<0.2 && !(vbf_mjj>300 && abs(vbf_deta)>3.5) && n_jets>0.5'))
    cuts.append(Cut('mva_high_0jet', inc_cut + '&& l1_charge != l2_charge && mt<40 && mva>0.2 && !(vbf_mjj>300 && abs(vbf_deta)>3.5) && n_jets<0.5'))
    cuts.append(Cut('mva_low_0jet', inc_cut + '&& l1_charge != l2_charge && mt<40 && mva<0.2 && !(vbf_mjj>300 && abs(vbf_deta)>3.5) && n_jets<0.5'))
    cuts.append(Cut('0jet', inc_cut + '&& l1_charge != l2_charge && mt<40 && mva>0.2 && n_jets<0.5'))

# cuts.append(Cut('inclusivemtgr40', inc_cut + '&& l1_charge != l2_charge && mt>40'))

# cuts.append(Cut('SS', inc_cut + '&& l1_charge == l2_charge'))
# cuts.append(Cut('SS_muantiiso', inc_cut.replace('l1_reliso05<0.1', 'l1_reliso05>0.2') + '&& l1_charge == l2_charge'))
# cuts.append(Cut('SSmt40', inc_cut + '&& l1_charge == l2_charge && mt<40'))
# cuts.append(Cut('SShighmt40', inc_cut + '&& l1_charge == l2_charge && mt>40'))

samples_mc, samples_data, samples, all_samples, sampleDict = createSampleLists(analysis_dir=analysis_dir)

if mode == 'mssm_control' or not 'mssm' in mode:
    all_samples = [s for s in all_samples if not 'ggH' in s.name and not 'bbH' in s.name]


def createDefaultGroups(plot):
    plot.Group('VV', ['VVTo2L2Nu', 'ZZTo2L2Q', 'WWTo1L1Nu2Q', 'WZTo1L3Nu', 'ZZTo4L', 'WZTo3L', 'WZTo2L2Q', 'WZTo1L1Nu2Q', 'T_tWch', 'TBar_tWch', 'TToLeptons_tch_powheg', 'TBarToLeptons_tch_powheg'])
    # plot.Group('ZTT', ['ZTT', 'ZTT1Jets', 'ZTT2Jets', 'ZTT3Jets', 'ZTT4Jets', 'ZTTM150', 'ZTTM10'])
    # plot.Group('ZJ', ['ZJ', 'ZJ1Jets', 'ZJ2Jets', 'ZJ3Jets', 'ZJ4Jets', 'ZJM150', 'ZJM10'])
    # plot.Group('ZL', ['ZL', 'ZL1Jets', 'ZL2Jets', 'ZL3Jets', 'ZL4Jets', 'ZLM150', 'ZLM10'])

if qcd_from_same_sign and not w_qcd_mssm_method:
    samples_qcdfromss = [s for s in all_samples if s.name != 'QCD']
    samples_ss = copy.deepcopy(samples_qcdfromss)

    samples_ss = [s for s in samples_ss if not s.is_signal]

    for sample in samples_ss:
        if sample.name != 'data_obs':
            # Subtract background from data
            sample.scale = -1.

    qcd = HistogramCfg(name='QCD', var=None, cfgs=samples_ss, cut=inc_cut, total_scale=r_qcd_os_ss, lumi=int_lumi, weight=total_weight)

    samples_qcdfromss.append(qcd)

if w_qcd_mssm_method:
    w_names = ['W', 'W1Jets', 'W2Jets', 'W3Jets', 'W4Jets']
    samples_non_w = [s for s in all_samples if s.name != 'QCD' and s.name not in w_names and not s.is_signal]
    samples_non_w_ss = copy.deepcopy(samples_non_w)
    
    samples_signal = [s for s in all_samples if s.is_signal]

    samples_w = copy.deepcopy([s for s in all_samples if s.name in w_names])
    samples_w_ss = copy.deepcopy(samples_w)
    
    # To calculate OS/SS ratio in inclusive W selection
    samples_w_incl_os = copy.deepcopy(samples_w)
    samples_w_incl_ss = copy.deepcopy(samples_w)

    # To calculate W scale factor
    samples_w_highmt_os = copy.deepcopy(samples_w)

    # Build a high MT region: OS - non-W/QCD OS - (SS - non-W/QCD SS)
    samples_non_w_highmt_os = copy.deepcopy(samples_non_w)
    samples_non_w_highmt_ss = copy.deepcopy(samples_non_w)


    for sample in samples_non_w_highmt_os:
        if sample.name != 'data_obs':
            # Subtract background from data
            sample.scale = -1.

    for sample in samples_non_w_highmt_ss:
        if sample.name != 'data_obs':
            sample.scale = -1.

    for sample in samples_non_w_ss:
        if sample.name != 'data_obs':
            sample.scale = -1.

    var_norm = VariableCfg(name='_norm_', drawname='1.', binning={'nbinsx':5, 'xmin':-1.5, 'xmax':3.5}, unit='', xtitle='Normalisation')

    stacknow_highmt_os = HistogramCfg(name='HighMTOS', var=var_norm, cfgs=samples_non_w_highmt_os, cut=inc_cut, lumi=int_lumi, weight=total_weight)
    stacknow_highmt_ss = HistogramCfg(name='HighMTSS', var=var_norm, cfgs=samples_non_w_highmt_ss, cut=inc_cut, lumi=int_lumi, weight=total_weight)

    wjets_incl_os = HistogramCfg(name='WInclOS', var=var_norm, cfgs=samples_w_incl_os, cut=inc_cut, lumi=int_lumi, weight=total_weight)
    wjets_incl_ss = HistogramCfg(name='WInclSS', var=var_norm, cfgs=samples_w_incl_ss, cut=inc_cut, lumi=int_lumi, weight=total_weight)

    wjets_highmt_os = HistogramCfg(name='WHighMTOS', var=var_norm, cfgs=samples_w_highmt_os, cut=inc_cut, lumi=int_lumi, weight=total_weight)

    wjets = HistogramCfg(name='W', var=None, cfgs=samples_w, cut=inc_cut,lumi=int_lumi, weight=total_weight)
    wjets_ss = HistogramCfg(name='WSS', var=None, cfgs=samples_w_ss, cut=inc_cut,lumi=int_lumi, weight=total_weight)

    qcd = HistogramCfg(name='QCD', var=None, cfgs=samples_non_w_ss + [wjets_ss], cut=inc_cut, total_scale=r_qcd_os_ss, lumi=int_lumi, weight=total_weight)

    samples_mssm_method = samples_non_w + [wjets, qcd] + samples_signal

# Taken from Variables.py; can get subset with e.g. getVars(['mt', 'mvis'])
# variables = taumu_vars
# variables = getVars(['_norm_', 'mt', 'mvis', 'l1_pt', 'l2_pt', 'l1_eta', 'l2_eta', 'n_vertices', 'n_jets', 'n_bjets'])
# variables = getVars(['_norm_', 'mt', 'mvis', 'n_vertices', 'met_pt', 'l1_pt', 'l2_pt'])
# variables = getVars(['delta_phi_l2_met', 'met_pt', 'met_phi'])
# variables = getVars(['_norm_'])
# variables = getVars(['mvis'])
# variables = [
#     VariableCfg(name='mvis', binning={'nbinsx':35, 'xmin':0., 'xmax':350}, unit='GeV', xtitle='m_{vis}')
# ]
variables = [
    VariableCfg(name='mva', binning={'nbinsx':20, 'xmin':0., 'xmax':1.}, unit='', xtitle='s_{BDT}'),
    VariableCfg(name='svfit_mass', binning={'nbinsx':20, 'xmin':50., 'xmax':250}, unit='GeV', xtitle='m_{SVFit}'),
]

variables += getVars(['mt', 'n_jets', 'met_pt', 'pthiggs', 'vbf_mjj', 'vbf_deta', 'vbf_n_central', 'l2_pt', 'l1_pt', 'svfit_transverse_mass', 'delta_phi_l1_l2', 'delta_eta_l1_l2'])

if mode == 'mssm_signal':
    variables = [
        VariableCfg(name='svfit_transverse_mass', binning=binning_mssm, unit='GeV', xtitle='m_{T,SVFit}'),
        VariableCfg(name='svfit_mass', binning=binning_mssm, unit='GeV', xtitle='m_{SVFit}'),
        VariableCfg(name='mvis', binning=binning_mssm, unit='GeV', xtitle='m_{vis}'),
    ]


for cut in cuts:
    if qcd_from_same_sign and not 'SS' in cut.name and not w_qcd_mssm_method:
        cfg_main = HistogramCfg(name=cut.name, var=None, cfgs=samples_qcdfromss, cut=cut.cut, lumi=int_lumi, weight=total_weight)
    elif w_qcd_mssm_method:
        cfg_main = HistogramCfg(name=cut.name, var=None, cfgs=samples_mssm_method, cut=cut.cut, lumi=int_lumi, weight=total_weight)
        wjets.cut = cut.cut # since wjets is a sub-HistogramCfg
    else:
        cfg_main = HistogramCfg(name=cut.name, var=None, cfgs=all_samples, cut=cut.cut, lumi=int_lumi, weight=total_weight)
    
    if qcd_from_same_sign and not 'SS' in cut.name:
        qcd.cut = cut.cut.replace('l1_charge != l2_charge', 'l1_charge == l2_charge')

    if w_qcd_mssm_method:
        stacknow_highmt_os.name = 'HighMTOS'+cut.name
        stacknow_highmt_ss.name = 'HighMTSS'+cut.name
        wjets_incl_os.name = 'WInclOS'+cut.name
        wjets_incl_ss.name = 'WInclSS'+cut.name
        wjets_highmt_os.name = 'WHighMTOS'+cut.name
        wjets_ss.name = 'WJetsSS'+cut.name

        qcd.cut = cut.cut.replace('l1_charge != l2_charge', 'l1_charge == l2_charge')
        wjets_ss.cut = cut.cut.replace('l1_charge != l2_charge', 'l1_charge == l2_charge')

        stacknow_highmt_os.cut = cut.cut.replace(mt_cut, 'mt>70') + '&& mt>70'
        stacknow_highmt_ss.cut = cut.cut.replace('l1_charge != l2_charge', 'l1_charge == l2_charge').replace(mt_cut, 'mt>70') + '&& mt>70'

        wjets_incl_os.cut = cut.cut.replace(mt_cut, '1.')
        wjets_incl_ss.cut = cut.cut.replace('l1_charge != l2_charge', 'l1_charge == l2_charge').replace(mt_cut, '1.')

        wjets_highmt_os.cut = cut.cut.replace(mt_cut, 'mt>70') + '&& mt>70'

        plot_w_os = createHistogram(wjets_incl_os, verbose=False, friend_func=lambda f: f.replace('MC', 'MVA'))
        plot_w_ss = createHistogram(wjets_incl_ss, verbose=False, friend_func=lambda f: f.replace('MC', 'MVA'))

        r_w_os_ss = plot_w_os.GetStack().totalHist.Yield()/plot_w_ss.GetStack().totalHist.Yield()
        print 'Inclusive W OS/SS ratio:', r_w_os_ss

        plot_highmt_os = createHistogram(stacknow_highmt_os, all_stack=True, verbose=False, friend_func=lambda f: f.replace('MC', 'MVA'))
        plot_highmt_ss = createHistogram(stacknow_highmt_ss, all_stack=True, verbose=False, friend_func=lambda f: f.replace('MC', 'MVA'))
        createDefaultGroups(plot_highmt_os)
        createDefaultGroups(plot_highmt_ss)

        yield_highmt_os = plot_highmt_os.GetStack().totalHist.Yield()
        yield_highmt_ss = plot_highmt_ss.GetStack().totalHist.Yield()

        plot_w_highmt_os = createHistogram(wjets_highmt_os, verbose=False, friend_func=lambda f: f.replace('MC', 'MVA'))

        yield_w_highmt_os = plot_w_highmt_os.GetStack().totalHist.Yield()

        if r_w_os_ss < r_qcd_os_ss:
            print 'WARNING, OS/SS ratio larger for QCD than for W+jets!', r_w_os_ss, r_qcd_os_ss

        yield_estimation = r_w_os_ss*(yield_highmt_os - r_qcd_os_ss*yield_highmt_ss)/(r_w_os_ss - r_qcd_os_ss)

        print 'High MT W+jets estimated yield', yield_estimation
        print 'High MT W+jets MC yield', yield_w_highmt_os

        w_sf = 0.
        if yield_w_highmt_os:
            w_sf = yield_estimation/yield_w_highmt_os
        else:
            print 'Warning: no MC events in high MT W+jets'

        print 'W+jets scale factor:', w_sf, '\n'

        wjets.total_scale = w_sf
        wjets_ss.total_scale = -w_sf

    cfg_main.vars = variables
    if qcd_from_same_sign:
        qcd.vars = variables # Can put into function but we will not want it by default if we take normalisations from e.g. high MT
    if w_qcd_mssm_method:
        wjets.vars = variables # Can put into function but we will not want it by default if we take normalisations from e.g. high MT
        qcd.vars = variables
        wjets_ss.vars = variables

    for variable in variables:
        if variable.name in ['svfit_mass', 'svfit_transverse_mass', 'mvis'] and 'mssm' in mode:
            if cut.name in ['inclusive', 'nobtag']:
                variable.binning = binning_mssm
            elif cut.name in ['btag']:
                variable.binning = binning_mssm_btag

    plots = createHistograms(cfg_main, verbose=False, friend_func=lambda f: f.replace('MC', 'MVA'))
    for variable in variables:
    # for plot in plots.itervalues():
        plot = plots[variable.name]
        createDefaultGroups(plot)
        if not w_qcd_mssm_method:
            plot.Group('W', ['W', 'W1Jets', 'W2Jets', 'W3Jets', 'W4Jets'])
        # plot.Group('Electroweak', ['Diboson', 'W'])
        # plot.Group('Single t', ['T_tWch', 'TBar_tWch', 'TToLeptons_sch', 'TToLeptons_tch'])
        # plot.Group('ZLL', ['Ztt_ZL', 'Ztt_ZJ'], style=plot.Hist('Ztt_ZL').style)
        HistDrawer.draw(plot, plot_dir='plots/'+cut.name)
        if variable.name in ['mvis', 'svfit_transverse_mass', 'svfit_mass', 'mva']:
            plot.WriteDataCard(filename='datacard_{mode}_{var}.root'.format(mode=mode, var=variable.name), dir='mt_' + cut.name, mode='UPDATE') #mt = mu-tau
