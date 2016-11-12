from CMGTools.H2TauTau.proto.plotter.PlotConfigs import HistogramCfg
from CMGTools.H2TauTau.proto.plotter.categories_TauMu import cat_Inc
from CMGTools.H2TauTau.proto.plotter.HistCreator import createHistogram
# from CMGTools.H2TauTau.proto.plotter.HistDrawer import HistDrawer
from CMGTools.H2TauTau.proto.plotter.Variables import getVars, all_vars
from CMGTools.H2TauTau.proto.plotter.Samples import samples

from CMGTools.H2TauTau.proto.plotter.helper_methods import plotDataOverMCEff, getPUWeight


# total_weight = 'weight * ' + getPUWeight()

total_weight = 'weight'

int_lumi = 1560.

cuts = {}

inc_cut = '&&'.join([cat_Inc])
inc_cut += '&& l2_decayModeFinding'

# cuts['Update_OS'] = inc_cut + '&& l1_charge != l2_charge'
# cuts['Update_OSlowMT'] = inc_cut + '&& l1_charge != l2_charge && mt<40'
cuts['Update_SSlowMT'] = inc_cut + '&& l1_charge == l2_charge && mt<40'

cuts['Update_OShighMT'] = inc_cut + '&& l1_charge != l2_charge && mt>40'
cuts['Update_SShighMT'] = inc_cut + '&& l1_charge == l2_charge && mt>40'

cut_names = [cut for cut in cuts]
for cut in cut_names:
    cuts[cut+'_plus'] = cuts[cut] + ' && l1_charge==1'
    cuts[cut+'_minus'] = cuts[cut] + ' && l1_charge==-1'

# cut_names = [cut for cut in cuts]
# for cut in cut_names:
#     # cuts[cut+'invmu'] = cuts[cut].replace('l1_reliso05<0.1', 'l1_reliso05>0.1')
#     cuts[cut+'invtau'] = cuts[cut].replace('l2_byCombinedIsolationDeltaBetaCorrRaw3Hits<1.5', 'l2_byCombinedIsolationDeltaBetaCorrRaw3Hits>1.5')

qcd_from_same_sign = False

# -> Command line
analysis_dir = '/afs/cern.ch/user/s/steggema/work/public/mt/NewProd'
tree_prod_name = 'H2TauTauTreeProducerTauMu'
data_dir = analysis_dir


# Taken from Variables.py, can get subset with e.g. getVars(['mt', 'mvis'])
variables = getVars(['l1_pt', 'l2_pt', 'l1_gen_pdgId', 'l2_gen_pdgId', 'l1_reliso05_04', 'l1_reliso05', 'l2_byCombinedIsolationDeltaBetaCorrRaw3Hits'])
variables += [v for v in all_vars if 'dxy' in v.name or 'dz' in v.name]

variables = getVars(['_norm_', 'l2_pt', 'l2_eta', 'l2_mass', 'l2_decayMode', 'mvis', 'mt', 'delta_r_l1_l2', 'l2_gen_pdgId', 'l2_mt'])
# variables = all_vars

for cut_name in cuts:
    cfg_tight = HistogramCfg(name='tight', var=None, cfgs=samples, cut=inc_cut, lumi=int_lumi, weight=total_weight + ' * ((l2_gen_match != 5) - (l2_gen_match == 5))')
    cfg_loose = HistogramCfg(name='loose', var=None, cfgs=samples, cut=inc_cut, lumi=int_lumi, weight=total_weight + ' * ((l2_gen_match != 5) - (l2_gen_match == 5))')

    cfg_data_tight = HistogramCfg(name='tight_data', var=None, cfgs=samples, cut=inc_cut, lumi=int_lumi, weight=total_weight + ' * ((genmet_pt < 0.) - (l2_gen_match == 5))')
    cfg_data_loose = HistogramCfg(name='loose_data', var=None, cfgs=samples, cut=inc_cut, lumi=int_lumi, weight=total_weight + ' * ((genmet_pt < 0.) - (l2_gen_match == 5))')


    cfg_tight.cut = cuts[cut_name]
    cfg_loose.cut = cuts[cut_name].replace('tau1_decayModeFinding>0.', '1.')
    cfg_data_tight.cut = cuts[cut_name]
    cfg_data_loose.cut = cuts[cut_name].replace('tau1_decayModeFinding>0.', '1.')

    for variable in variables:
        cfg_tight.var = variable
        cfg_loose.var = variable
        cfg_data_tight.var = variable
        cfg_data_loose.var = variable
        
        plot_tight = createHistogram(cfg_tight, verbose=False)
        plot_loose = createHistogram(cfg_loose, verbose=False)
        plot_data_tight = createHistogram(cfg_data_tight, verbose=False, all_stack=True)
        plot_data_loose = createHistogram(cfg_data_loose, verbose=False, all_stack=True)
        for plot in [plot_tight, plot_loose, plot_data_tight, plot_data_loose]:
            plot.Group('VV', ['ZZ', 'WZ', 'WW', 'T_tWch', 'TBar_tWch'])
            out_dir = 'fakeplots/'+cut_name if plot is plot_tight else 'fakeplots/loose'+cut_name
            # HistDrawer.draw(plot, plot_dir='fakeplots/'+cut_name)

        plotDataOverMCEff(plot_tight.GetStack().totalHist.weighted, 
                          plot_loose.GetStack().totalHist.weighted, 
                          plot_data_tight.GetStack().totalHist.weighted, 
                          plot_data_loose.GetStack().totalHist.weighted,
                          'fakeplots/fakerate_' + variable.name + cut_name + '.pdf')

