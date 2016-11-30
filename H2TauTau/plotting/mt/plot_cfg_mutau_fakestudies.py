import fnmatch
from numpy import array

from CMGTools.H2TauTau.proto.plotter.PlotConfigs import HistogramCfg, VariableCfg
from CMGTools.H2TauTau.proto.plotter.categories_TauMu import cat_Inc
from CMGTools.H2TauTau.proto.plotter.HistCreator import createHistogram
# from CMGTools.H2TauTau.proto.plotter.HistDrawer import HistDrawer
from CMGTools.H2TauTau.proto.plotter.Variables import getVars, all_vars
from CMGTools.H2TauTau.proto.plotter.Samples import createSampleLists
from CMGTools.H2TauTau.proto.samples.spring16.htt_common import lumi as int_lumi

from CMGTools.H2TauTau.proto.plotter.helper_methods import plotDataOverMCEff, getPUWeight


# total_weight = 'weight * ' + getPUWeight()

total_weight = 'weight'

cuts = {}

cat_Inc = cat_Inc.replace('l2_byIsolationMVArun2v1DBoldDMwLT>3.5', '1.')

inc_cut = '&&'.join([cat_Inc])
inc_cut += '&& n_jets==0 && l2_decayModeFinding && l2_byIsolationMVArun2v1DBoldDMwLT>2.5'

cuts['d_samecharge'] = '&& abs(l2_gen_pdgId) == 1 && l2_gen_pdgId * l2_charge > 0.'
cuts['d_oppcharge'] = '&& abs(l2_gen_pdgId) == 1 && l2_gen_pdgId * l2_charge < 0.'
cuts['s_samecharge'] = '&& abs(l2_gen_pdgId) == 3 && l2_gen_pdgId * l2_charge > 0.'
cuts['s_oppcharge'] = '&& abs(l2_gen_pdgId) == 3 && l2_gen_pdgId * l2_charge < 0.'
cuts['b_samecharge'] = '&& abs(l2_gen_pdgId) == 5 && l2_gen_pdgId * l2_charge > 0.'
cuts['b_oppcharge'] = '&& abs(l2_gen_pdgId) == 5 && l2_gen_pdgId * l2_charge < 0.'
cuts['u_samecharge'] = '&& abs(l2_gen_pdgId) == 2 && l2_gen_pdgId * l2_charge < 0.'
cuts['u_oppcharge'] = '&& abs(l2_gen_pdgId) == 2 && l2_gen_pdgId * l2_charge > 0.'
cuts['c_samecharge'] = '&& abs(l2_gen_pdgId) == 4 && l2_gen_pdgId * l2_charge < 0.'
cuts['c_oppcharge'] = '&& abs(l2_gen_pdgId) == 4 && l2_gen_pdgId * l2_charge > 0.'
cuts['gluon'] = '&& abs(l2_gen_pdgId) == 21'

# cuts['tau_jet_80_100'] = '&& l2_jet_pt>80 && l2_jet_pt<100 && l2_jet_pt>jet1_pt'
cuts['tau_jet_80_100'] = '&& l2_jet_pt>80 && l2_jet_pt<100 && n_jets==0'

# cuts['Update_OS'] = inc_cut + '&& l1_charge != l2_charge'
# cuts['Update_OSlowMT'] = inc_cut + '&& l1_charge != l2_charge && mt<40'
# cuts['Update_SSlowMT'] = inc_cut + '&& l1_charge == l2_charge && mt<40'

# cuts['Update_OShighMT'] = inc_cut + '&& l1_charge != l2_charge && mt>40'
# cuts['Update_SShighMT'] = inc_cut + '&& l1_charge == l2_charge && mt>40'

# cut_names = [cut for cut in cuts]
# for cut in cut_names:
#     cuts[cut+'_plus'] = cuts[cut] + ' && l1_charge==1'
#     cuts[cut+'_minus'] = cuts[cut] + ' && l1_charge==-1'

# cut_names = [cut for cut in cuts]
# for cut in cut_names:
#     # cuts[cut+'invmu'] = cuts[cut].replace('l1_reliso05<0.1', 'l1_reliso05>0.1')
#     cuts[cut+'invtau'] = cuts[cut].replace('l2_byCombinedIsolationDeltaBetaCorrRaw3Hits<1.5', 'l2_byCombinedIsolationDeltaBetaCorrRaw3Hits>1.5')

qcd_from_same_sign = False

# -> Command line
analysis_dir = '/data1/steggema/mt/051016/MuTauMC/'
tree_prod_name = 'H2TauTauTreeProducerTauMu'
data_dir = analysis_dir

samples_mc, samples_data, samples, all_samples, sampleDict = createSampleLists(analysis_dir=analysis_dir)

samples_mc_w = [s for s in samples_mc if fnmatch.fnmatch(s.name, 'W*Jet*')]
samples_mc_tt = [s for s in samples_mc if fnmatch.fnmatch(s.name, 'TT*')]

# Taken from Variables.py, can get subset with e.g. getVars(['mt', 'mvis'])
variables = getVars(['l1_pt', 'l2_pt', 'l2_eta', 'l2_jet_pt'])

variables += [
    VariableCfg(name='l2_jet_pt', binning=array([20., 30., 40., 50., 60., 70., 80., 90., 100., 150., 200.]), unit='GeV', xtitle='tau jet p_{T}'),
    VariableCfg(name='l2_pt', binning=array([20., 25., 30., 35., 40., 50., 60., 80., 120., 200.]), unit='GeV', xtitle='tau p_{T}'),
]

# variables += [v for v in all_vars if 'dxy' in v.name or 'dz' in v.name]

# variables = getVars(['_norm_', 'l2_pt', 'l2_eta', 'l2_mass', 'l2_decayMode', 'mvis', 'mt', 'delta_r_l1_l2', 'l2_gen_pdgId', 'l2_mt'])
# variables = all_vars

for cut_name in cuts:
    cfg_tight = HistogramCfg(name='tight', var=None, cfgs=samples_mc_w, cut=inc_cut, lumi=int_lumi, weight=total_weight + ' * ((l2_gen_match == 6))')
    cfg_loose = HistogramCfg(name='loose', var=None, cfgs=samples_mc_w, cut=inc_cut, lumi=int_lumi, weight=total_weight + ' * ((l2_gen_match == 6))')

    cfg_data_tight = HistogramCfg(name='tight_data', var=None, cfgs=samples_mc_tt, cut=inc_cut, lumi=int_lumi, weight=total_weight + ' * ((l2_gen_match == 6))')
    cfg_data_loose = HistogramCfg(name='loose_data', var=None, cfgs=samples_mc_tt, cut=inc_cut, lumi=int_lumi, weight=total_weight  + ' * ((l2_gen_match == 6))')


    tight_cut = inc_cut + cuts[cut_name]
    loose_cut = tight_cut.replace('l2_byIsolationMVArun2v1DBoldDMwLT>2.5', '1.')

    print 'Tight cut:', tight_cut
    print 'Loose cut:', loose_cut

    cfg_tight.cut = tight_cut
    cfg_loose.cut = loose_cut
    cfg_data_tight.cut = tight_cut
    cfg_data_loose.cut = loose_cut



    for variable in variables:
        cfg_tight.var = variable
        cfg_loose.var = variable
        cfg_data_tight.var = variable
        cfg_data_loose.var = variable
        
        plot_tight = createHistogram(cfg_tight, verbose=False)
        plot_loose = createHistogram(cfg_loose, verbose=False)
        plot_data_tight = createHistogram(cfg_data_tight, verbose=False, all_stack=True)
        plot_data_loose = createHistogram(cfg_data_loose, verbose=False, all_stack=True)
        # for plot in [plot_tight, plot_loose, plot_data_tight, plot_data_loose]:
        #     # plot.Group('VV', ['ZZ', 'WZ', 'WW', 'T_tWch', 'TBar_tWch'])
        #     out_dir = 'fakeplots/'+cut_name if plot is plot_tight else 'fakeplots/loose'+cut_name
        #     # HistDrawer.draw(plot, plot_dir='fakeplots/'+cut_name)

        plotDataOverMCEff(plot_tight.GetStack().totalHist.weighted, 
                          plot_loose.GetStack().totalHist.weighted, 
                          plot_data_tight.GetStack().totalHist.weighted, 
                          plot_data_loose.GetStack().totalHist.weighted,
                          'fakeplots/fakerate_' + variable.name + cut_name + '.pdf',
                          mc_leg='W+jets', obs_leg='t#bar{t}',
                          ratio_leg='W/t#bar{t}')

