import copy

from CMGTools.H2TauTau.proto.plotter.PlotConfigs import HistogramCfg, VariableCfg
from CMGTools.H2TauTau.proto.plotter.categories_eMu import cat_Inc
from CMGTools.H2TauTau.proto.plotter.HistCreator import createHistogram
from CMGTools.H2TauTau.proto.plotter.HistDrawer import HistDrawer
from CMGTools.H2TauTau.proto.plotter.Variables import all_vars, emu_vars, getVars
from CMGTools.H2TauTau.proto.plotter.helper_methods import getPUWeight

from CMGTools.H2TauTau.proto.plotter.Samples import createSampleLists

from ROOT import gROOT

gROOT.SetBatch(True)

int_lumi = 2094.2

total_weight = 'weight * ' + getPUWeight()
#total_weight = 'weight'

print total_weight

cuts = {}

inc_cut = '&&'.join([cat_Inc])


cuts['inclusive'] = inc_cut + '&& l1_charge != l2_charge'
#cuts['inclusive'] = inc_cut + '&& l1_charge != l2_charge && mvis <= 40 && n_bjets >= 1'

new_cuts = {}

for cut in cuts:
    print 'check', cut
    new_cuts[cut.replace('inclusive', 'SS')] = cuts[cut].replace('l1_charge != l2_charge', 'l1_charge == l2_charge')

inv_cuts = {}
for cut in cuts:
    new_cuts[cut+'invmu'] = cuts[cut].replace('l2_reliso05<0.15', 'l2_reliso05>0.15')
    new_cuts[cut+'inve'] = cuts[cut].replace('l1_reliso05<0.15', 'l1_reliso05>0.15')

cuts = cuts.copy()
#cuts.update(new_cuts)

print cuts

qcd_from_same_sign = True

analysis_dir = '/afs/cern.ch/user/y/ytakahas/work/public/forHTT/em'

samples_mc, samples_data, samples, all_samples, sampleDict = createSampleLists(analysis_dir=analysis_dir, tree_prod_name='H2TauTauTreeProducerMuEle', ztt_cut='(l1_gen_match>2 && l2_gen_match>3)', zl_cut='l2_gen_match==99',zj_cut='l2_gen_match==99')

if qcd_from_same_sign:
    samples_qcdfromss = [s for s in samples if s.name != 'QCD']
    samples_ss = copy.deepcopy(samples_qcdfromss)

#    import pdb; pdb.set_trace()

    scale = 1.06

    for sample in samples_ss:
        sample.scale = scale
        if sample.name != 'data_obs':
            # Subtract background from data
            sample.scale = -scale

    qcd = HistogramCfg(name='QCD', var=None, cfgs=samples_ss, cut=inc_cut, lumi=int_lumi)

    samples_qcdfromss.append(qcd)

# Taken from Variables.py, can get subset with e.g. getVars(['mt', 'mvis'])
#variables = all_vars
variables = emu_vars
# variables = getVars(['_norm_', 'mt', 'mvis', 'l1_pt', 'l2_pt', 'l1_eta', 'l2_eta', 'n_vertices', 'n_jets', 'n_bjets'])
#variables = getVars(['mvis', '_norm_', 'n_vertices'])
#    VariableCfg(name='mvis', binning={'nbinsx':35, 'xmin':0, 'xmax':350}, unit='GeV', xtitle='m_{vis}')
#    ]

for cut_name in cuts:
    if qcd_from_same_sign and not 'SS' in cut_name :
        cfg_example = HistogramCfg(name='example', var=None, cfgs=samples_qcdfromss, cut=inc_cut, lumi=int_lumi, weight=total_weight)
    else:
        cfg_example = HistogramCfg(name='example', var=None, cfgs=samples, cut=inc_cut, lumi=int_lumi, weight=total_weight)
        

    cfg_example.cut = cuts[cut_name]
    if qcd_from_same_sign and not 'SS' in cut_name:
        qcd.cut = cuts[cut_name].replace('l1_charge != l2_charge', 'l1_charge == l2_charge')

    for variable in variables:

        print 'variable = ', variable
        
        cfg_example.var = variable
        if qcd_from_same_sign:
            qcd.var = variable # Can put into function but we will not want it by default if we take normalisations from e.g. high MT
        
#        import pdb; pdb.set_trace()
        plot = createHistogram(cfg_example, verbose=True)
        plot.Group('VV', ['VVTo2L2Nu', 'ZZTo2L2Q', 'ZZTo4L', 'WWTo1L1Nu2Q', 'WZTo2L2Q', 'WZTo3L', 'WZTo1L3Nu', 'WZTo1L1Nu2Q', 'T_tWch', 'TBar_tWch', 'TToLeptons_tch', 'TBarToLeptons_tch_powheg'])
        # plot.Group('Single t', ['T_tWch', 'TBar_tWch', 'TToLeptons_sch', 'TToLeptons_tch'])
#        plot.Group('ZLL', ['Ztt_ZL', 'Ztt_ZJ'], style=plot.Hist('Ztt_ZL').style)
        HistDrawer.draw(plot, plot_dir='plots/'+cut_name)

        if cut_name == 'inclusive' and variable.name == 'mvis':
            plot.WriteDataCard(filename='htt_em.inputs-sm-13TeV-mvis.root', dir='em_' + cut_name)
