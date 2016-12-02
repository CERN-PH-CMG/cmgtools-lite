import fnmatch
from numpy import array

from CMGTools.H2TauTau.proto.plotter.PlotConfigs import HistogramCfg, VariableCfg
from CMGTools.H2TauTau.proto.plotter.categories_TauMu import cat_Inc
from CMGTools.H2TauTau.proto.plotter.HistCreator import createHistogram
# from CMGTools.H2TauTau.proto.plotter.HistDrawer import HistDrawer
from CMGTools.H2TauTau.proto.plotter.Variables import getVars, all_vars
from CMGTools.H2TauTau.proto.plotter.Samples import createSampleLists
from CMGTools.H2TauTau.proto.samples.spring16.htt_common import lumi as int_lumi

from CMGTools.H2TauTau.proto.plotter.helper_methods import plotMCEffs


total_weight = 'weight'

cuts = {}

cat_Inc = cat_Inc.replace('l2_byIsolationMVArun2v1DBoldDMwLT>3.5', '1.')

inc_cut = '&&'.join([cat_Inc])
inc_cut += '&& l2_decayModeFinding && l2_byIsolationMVArun2v1DBoldDMwLT>2.5 && n_jets==0'

# cuts['d_samecharge'] = '&& abs(l2_gen_pdgId) == 1 && l2_gen_pdgId * l2_charge > 0.'
# cuts['d_oppcharge'] = '&& abs(l2_gen_pdgId) == 1 && l2_gen_pdgId * l2_charge < 0.'
# cuts['s_samecharge'] = '&& abs(l2_gen_pdgId) == 3 && l2_gen_pdgId * l2_charge > 0.'
# cuts['s_oppcharge'] = '&& abs(l2_gen_pdgId) == 3 && l2_gen_pdgId * l2_charge < 0.'
# cuts['b_samecharge'] = '&& abs(l2_gen_pdgId) == 5 && l2_gen_pdgId * l2_charge > 0.'
# cuts['b_oppcharge'] = '&& abs(l2_gen_pdgId) == 5 && l2_gen_pdgId * l2_charge < 0.'
# cuts['u_samecharge'] = '&& abs(l2_gen_pdgId) == 2 && l2_gen_pdgId * l2_charge < 0.'
# cuts['u_oppcharge'] = '&& abs(l2_gen_pdgId) == 2 && l2_gen_pdgId * l2_charge > 0.'
# cuts['c_samecharge'] = '&& abs(l2_gen_pdgId) == 4 && l2_gen_pdgId * l2_charge < 0.'
# cuts['c_oppcharge'] = '&& abs(l2_gen_pdgId) == 4 && l2_gen_pdgId * l2_charge > 0.'

cuts['Inclusive'] = ''
cuts['taupt30'] = '&& l2_pt>30'

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

samples = samples_mc_w + samples_mc_tt

# Taken from Variables.py, can get subset with e.g. getVars(['mt', 'mvis'])
variables = getVars(['l1_pt', 'l2_eta'])

variables += [
    VariableCfg(name='l2_jet_pt', binning=array([20., 30., 40., 50., 60., 70., 80., 90., 100., 150., 200.]), unit='GeV', xtitle='tau jet p_{T}'),
    VariableCfg(name='l2_pt', binning=array([20., 25., 30., 35., 40., 50., 60., 80., 120., 200.]), unit='GeV', xtitle='tau p_{T}'),
    VariableCfg(name='l2_jet_pt_div_l2_pt', drawname='l2_jet_pt/l2_pt', binning=array([0., 0.5, 0.8, 1.0, 1.1, 1.2, 1.5, 2.0, 3.0, 4.0]), unit=None, xtitle='tau p_{T}'),
]

# variables += [v for v in all_vars if 'dxy' in v.name or 'dz' in v.name]

# variables = getVars(['_norm_', 'l2_pt', 'l2_eta', 'l2_mass', 'l2_decayMode', 'mvis', 'mt', 'delta_r_l1_l2', 'l2_gen_pdgId', 'l2_mt'])
# variables = all_vars

sample_def_sets = {}
sample_def_sets['all_flavours_charges'] = [
    {'name':'u', 'samples':samples, 'cut':'&& abs(l2_gen_pdgId) == 2 && l2_gen_pdgId * l2_charge > 0.', 'colour':3, 'style':1},
    {'name':'u opp', 'samples':samples, 'cut':'&& abs(l2_gen_pdgId) == 2 && l2_gen_pdgId * l2_charge < 0.', 'colour':3, 'style':2},
    {'name':'d', 'samples':samples, 'cut':'&& abs(l2_gen_pdgId) == 1 && l2_gen_pdgId * l2_charge < 0.', 'colour':2, 'style':1},
    {'name':'d opp', 'samples':samples, 'cut':'&& abs(l2_gen_pdgId) == 1 && l2_gen_pdgId * l2_charge > 0.', 'colour':2, 'style':2},
    
    {'name':'b', 'samples':samples, 'cut':'&& abs(l2_gen_pdgId) == 5 && l2_gen_pdgId * l2_charge < 0.', 'colour':6, 'style':1},
    {'name':'b opp', 'samples':samples, 'cut':'&& abs(l2_gen_pdgId) == 5 && l2_gen_pdgId * l2_charge > 0.', 'colour':6, 'style':2},
    {'name':'c', 'samples':samples, 'cut':'&& abs(l2_gen_pdgId) == 4 && l2_gen_pdgId * l2_charge > 0.', 'colour':4, 'style':1},
    {'name':'c opp', 'samples':samples, 'cut':'&& abs(l2_gen_pdgId) == 4 && l2_gen_pdgId * l2_charge < 0.', 'colour':4, 'style':1},
    {'name':'s', 'samples':samples, 'cut':'&& abs(l2_gen_pdgId) == 3 && l2_gen_pdgId * l2_charge < 0.', 'colour':7, 'style':1},
    {'name':'s opp', 'samples':samples, 'cut':'&& abs(l2_gen_pdgId) == 3 && l2_gen_pdgId * l2_charge > 0.', 'colour':7, 'style':2},

    {'name':'g', 'samples':samples, 'cut':'&& abs(l2_gen_pdgId) == 21 ', 'colour':1, 'style':1},
]

sample_def_sets['all_flavours'] = [
    {'name':'u', 'samples':samples, 'cut':'&& abs(l2_gen_pdgId) == 2', 'colour':3, 'style':1},
    {'name':'d', 'samples':samples, 'cut':'&& abs(l2_gen_pdgId) == 1', 'colour':2, 'style':1},
    {'name':'b', 'samples':samples, 'cut':'&& abs(l2_gen_pdgId) == 5', 'colour':6, 'style':1},
    {'name':'c', 'samples':samples, 'cut':'&& abs(l2_gen_pdgId) == 4', 'colour':4, 'style':1},
    {'name':'s', 'samples':samples, 'cut':'&& abs(l2_gen_pdgId) == 3', 'colour':7, 'style':1},
    {'name':'g', 'samples':samples, 'cut':'&& abs(l2_gen_pdgId) == 21 ', 'colour':1, 'style':1},
]


for set_name, sample_defs in sample_def_sets.items():
    for cut_name in cuts:
        for variable in variables:
            plot_inputs = []
            for sample_def in sample_defs:
                cut_extra = sample_def['cut']
                cfg_tight = HistogramCfg(name='tight', var=None, cfgs=samples_mc_w, cut=inc_cut, lumi=int_lumi, weight=total_weight + ' * ((l2_gen_match == 6))')
                cfg_loose = HistogramCfg(name='loose', var=None, cfgs=samples_mc_w, cut=inc_cut, lumi=int_lumi, weight=total_weight + ' * ((l2_gen_match == 6))')

                tight_cut = inc_cut + cuts[cut_name] + cut_extra
                loose_cut = tight_cut.replace('l2_byIsolationMVArun2v1DBoldDMwLT>2.5', '1.')
                loose_cut = tight_cut.replace('l2_byIsolationMVArun2v1DBoldDMwLT>2.5', 'l2_byIsolationMVArun2v1DBoldDMwLT>0.5')

                print 'Tight cut:', tight_cut
                print 'Loose cut:', loose_cut

                cfg_tight.cut = tight_cut
                cfg_loose.cut = loose_cut
            
                cfg_tight.var = variable
                cfg_loose.var = variable
                
                plot_tight = createHistogram(cfg_tight, verbose=False)
                plot_loose = createHistogram(cfg_loose, verbose=False)

                tight_hist = plot_tight.GetStack().totalHist.weighted
                loose_hist = plot_loose.GetStack().totalHist.weighted

                plot_inputs.append((tight_hist, loose_hist, sample_def['name'], sample_def['colour'], sample_def['style']))

            plotMCEffs(plot_inputs, 'mcfakeplots/tight_to_loose'+set_name + '_' + variable.name + cut_name + '.pdf')

