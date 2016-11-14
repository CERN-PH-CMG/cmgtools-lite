import copy

from CMGTools.H2TauTau.proto.samples.spring16.htt_common import lumi, lumi_2016G

from CMGTools.H2TauTau.proto.plotter.PlotConfigs import HistogramCfg, VariableCfg
from CMGTools.H2TauTau.proto.plotter.categories_eMu import cat_Inc
from CMGTools.H2TauTau.proto.plotter.HistCreator import createHistograms
from CMGTools.H2TauTau.proto.plotter.HistDrawer import HistDrawer
from CMGTools.H2TauTau.proto.plotter.Variables import all_vars, emu_vars, getVars
from CMGTools.H2TauTau.proto.plotter.helper_methods import getPUWeight

from CMGTools.H2TauTau.proto.plotter.Samples import createSampleLists

from ROOT import gROOT

gROOT.SetBatch(True)

# total_weight = 'weight * ' + getPUWeight()
total_weight = 'weight'
data2016G = False

print total_weight

cuts = {}

inc_cut = '&&'.join([cat_Inc])


cuts['inclusive'] = inc_cut + '&& l1_charge != l2_charge'
cuts['inclusive_SS'] = inc_cut + '&& l1_charge == l2_charge'

# # ttbar selections
# cuts['1bjet'] = inc_cut + '&& l1_charge != l2_charge && n_bjets==1'
# cuts['1bjetmax2jets'] = inc_cut + '&& l1_charge != l2_charge && n_bjets==1 && n_jets<=2'
# cuts['inclusive_jet1pt70'] = inc_cut + '&& l1_charge != l2_charge && jet1_pt>70'
# cuts['inclusive_maxMT100'] = inc_cut + '&& l1_charge != l2_charge && max(mt, mt_leg2)>100'
# cuts['inclusive_MET70'] = inc_cut + '&& l1_charge != l2_charge && met_pt>70'
# cuts['inclusive_mvis100'] = inc_cut + '&& l1_charge != l2_charge && mvis>100'

# ZTT selections
cuts['bveto'] = inc_cut + '&& l1_charge != l2_charge && n_bjets==0'
cuts['bveto_less1jet'] = inc_cut + '&& l1_charge != l2_charge && n_bjets==0 && n_jets<=1'
cuts['bveto_jet1ptless100'] = inc_cut + '&& l1_charge != l2_charge && n_bjets==0&& jet1_pt<100.'
cuts['bveto_maxMTless100'] = inc_cut + '&& l1_charge != l2_charge && n_bjets==0 && max(mt, mt_leg2)<100'

cuts['bveto_lowdeta'] = inc_cut + '&& l1_charge != l2_charge && n_bjets==0 && delta_eta_l1_l2<2.5'


#cuts['inclusive'] = inc_cut + '&& l1_charge != l2_charge && mvis <= 40 && n_bjets >= 1'


cuts = cuts.copy()

print cuts

qcd_from_same_sign = True

analysis_dir = '/data1/steggema/em/06092016/MuEleRealMCPlusTau'

samples_mc, samples_data, samples, all_samples, sampleDict = createSampleLists(analysis_dir, channel='em',  ztt_cut='(l1_gen_match>2 && l2_gen_match>3)', zl_cut='l2_gen_match==99',zj_cut='l2_gen_match==99', data2016G=data2016G)

if qcd_from_same_sign:
    samples_qcdfromss = [s for s in samples if s.name != 'QCD']
    samples_ss = copy.deepcopy(samples_qcdfromss)

    scale = 2.0

    for sample in samples_ss:
        sample.scale = scale
        if sample.name != 'data_obs':
            # Subtract background from data
            sample.scale = -scale

    qcd = HistogramCfg(name='QCD', var=None, cfgs=samples_ss, cut=inc_cut, lumi=lumi)

    samples_qcdfromss.append(qcd)

# Taken from Variables.py, can get subset with e.g. getVars(['mt', 'mvis'])
variables = emu_vars
# variables = getVars(['n_vertices'])
# variables = getVars(['l1_reliso05', 'l2_reliso05'])
# variables = [
#     VariableCfg(name='mvis', binning={'nbinsx':35, 'xmin':0, 'xmax':350}, unit='GeV', xtitle='m_{vis}')
# ]

for cut_name in cuts:
    if  qcd_from_same_sign and not 'SS' in cut_name :
        cfg_example = HistogramCfg(name='example', var=None, cfgs=samples_qcdfromss, cut=inc_cut, lumi=lumi, weight=total_weight)
    else:
        cfg_example = HistogramCfg(name='example', var=None, cfgs=samples, cut=inc_cut, lumi=lumi, weight=total_weight)
        

    cfg_example.cut = cuts[cut_name]
    if qcd_from_same_sign and not 'SS' in cut_name:
        qcd.cut = cuts[cut_name].replace('l1_charge != l2_charge', 'l1_charge == l2_charge')

    
    cfg_example.vars = variables
    if qcd_from_same_sign:
        qcd.vars = variables # Can put into function but we will not want it by default if we take normalisations from e.g. high MT

    plots = createHistograms(cfg_example, verbose=True)
    for variable in variables:    
        plot = plots[variable.name]
        plot.Group('VV', ['WWTo1L1Nu2Q', 'WZTo1L1Nu2Q', 'WZTo1L3Nu', 'WZTo2L2Q', 'VVTo2L2Nu', 'ZZTo2L2Q', 'ZZTo4L'])
        plot.Group('Single t', ['T_tWch', 'TBar_tWch', 'TBarToLeptons_tch_powheg', 'TToLeptons_tch_powheg'])
        plot.Group('ZLL', ['ZL', 'ZJ'], style=plot.Hist('ZL').style)
        plot.Group('W', ['W1Jets', 'W2Jets', 'W3Jets', 'W4Jets'])
        plot.Group('Electroweak', ['W', 'VV', 'Single t'])
        base_dir = 'plotsG/' if data2016G else 'plots/'
        HistDrawer.draw(plot, plot_dir=base_dir+cut_name, channel='e#mu')
