import copy
from collections import namedtuple

from CMGTools.H2TauTau.proto.plotter.PlotConfigs import HistogramCfg, VariableCfg
from CMGTools.H2TauTau.proto.plotter.categories_TauMu import cat_Inc
from CMGTools.H2TauTau.proto.plotter.HistCreator import createHistogram
from CMGTools.H2TauTau.proto.plotter.HistDrawer import HistDrawer
from CMGTools.H2TauTau.proto.plotter.Variables import all_vars, getVars
# from CMGTools.H2TauTau.proto.plotter.helper_methods import getPUWeight

from CMGTools.H2TauTau.proto.plotter.Samples import createSampleLists

int_lumi = 2240. # from Alexei's email
qcd_from_same_sign = True
analysis_dir = '/afs/cern.ch/user/s/steggema/work/public/mt/180216/'

total_weight = 'weight'
total_weight = 'weight/l1_weight'
# total_weight = 'geninfo_mcweight'
# total_weight = 'weight/l1_weight/weight_njet'
# total_weight = 'weight/l1_weight/weight_njet/weight_vertex'

print total_weight

Cut = namedtuple('Cut', ['name', 'cut'])

cuts = []

inc_cut = '&&'.join([cat_Inc])
# inc_cut += '&& l2_decayModeFinding'


cuts.append(Cut('inclusive', inc_cut + '&& l1_charge != l2_charge'))
cuts.append(Cut('inclusivemt40', inc_cut + '&& l1_charge != l2_charge && mt<40'))

# cuts.append(Cut('inclusivehighmt40', inc_cut + '&& l1_charge != l2_charge && mt>40'))

# cuts.append(Cut('SS', inc_cut + '&& l1_charge == l2_charge'))
# cuts.append(Cut('SSmt40', inc_cut + '&& l1_charge == l2_charge && mt<40'))
# cuts.append(Cut('SShighmt40', inc_cut + '&& l1_charge == l2_charge && mt>40'))

samples_mc, samples_data, samples, all_samples, sampleDict = createSampleLists(analysis_dir=analysis_dir)

if qcd_from_same_sign:
    samples_qcdfromss = [s for s in all_samples if s.name != 'QCD']
    samples_ss = copy.deepcopy(samples_qcdfromss)

    samples_ss = [s for s in samples_ss if not s.is_signal]

    scale = 1.06

    for sample in samples_ss:
        sample.scale = scale
        if sample.name != 'data_obs':
            # Subtract background from data
            sample.scale = -scale

    qcd = HistogramCfg(name='QCD', var=None, cfgs=samples_ss, cut=inc_cut, lumi=int_lumi, weight=total_weight)

    samples_qcdfromss.append(qcd)

# Taken from Variables.py, can get subset with e.g. getVars(['mt', 'mvis'])
variables = all_vars
# variables = getVars(['_norm_', 'mt', 'mvis', 'l1_pt', 'l2_pt', 'l1_eta', 'l2_eta', 'n_vertices', 'n_jets', 'n_bjets'])

# variables = getVars(['_norm_', 'mt', 'mvis', 'n_vertices'])

# variables = getVars(['_norm_', 'met_pt', 'met_phi'])

# variables = getVars(['_norm_'])
variables = [
    VariableCfg(name='mvis', binning={'nbinsx':35, 'xmin':0, 'xmax':350}, unit='GeV', xtitle='m_{vis}')
]

for cut in cuts:
    if qcd_from_same_sign and not 'SS' in cut.name:
        cfg_example = HistogramCfg(name=cut.name, var=None, cfgs=samples_qcdfromss, cut=inc_cut, lumi=int_lumi, weight=total_weight)
    else:
        cfg_example = HistogramCfg(name=cut.name, var=None, cfgs=all_samples, cut=inc_cut, lumi=int_lumi, weight=total_weight)
        

    cfg_example.cut = cut.cut
    if qcd_from_same_sign and not 'SS' in cut.name:
        qcd.cut = cut.cut.replace('l1_charge != l2_charge', 'l1_charge == l2_charge')

    for variable in variables:
        cfg_example.var = variable
        if qcd_from_same_sign:
            qcd.var = variable # Can put into function but we will not want it by default if we take normalisations from e.g. high MT
        
        plot = createHistogram(cfg_example, verbose=False)
        plot.Group('VV', ['ZZTo2L2Q', 'WWTo1L1Nu2Q', 'WZTo1L3Nu', 'ZZTo4L', 'WZTo3L', 'WZTo2L2Q', 'WZTo1L1Nu2Q', 'T_tWch', 'TBar_tWch', 'TToLeptons_tch_powheg', 'TBarToLeptons_tch_powheg'])
        plot.Group('ZTT', ['ZTT', 'ZTT1Jets', 'ZTT2Jets', 'ZTT3Jets', 'ZTT4Jets'])
        plot.Group('ZJ', ['ZJ', 'ZJ1Jets', 'ZJ2Jets', 'ZJ3Jets', 'ZJ4Jets'])
        plot.Group('ZL', ['ZL', 'ZL1Jets', 'ZL2Jets', 'ZL3Jets', 'ZL4Jets'])
        # plot.Group('Single t', ['T_tWch', 'TBar_tWch', 'TToLeptons_sch', 'TToLeptons_tch'])
        # plot.Group('ZLL', ['Ztt_ZL', 'Ztt_ZJ'], style=plot.Hist('Ztt_ZL').style)
        HistDrawer.draw(plot, plot_dir='plots/'+cut.name)
        if variable.name == 'mvis':
            plot.WriteDataCard(filename='datacard_mvis.root', dir='mt_' + cut.name, mode='UPDATE')
