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

total_weight = '1.'

cuts = {}

cat_Inc = cat_Inc.replace('tau_byIsolationMVArun2v1DBoldDMwLT>3.5', '1.')

inc_cut = '!veto_dilepton && !veto_thirdlepton && !veto_otherlepton && muon_reliso05<0.1 && muon_muonid_medium>0.5 && muon_pt>19. && abs(jet_eta)<2.3 && tau_decayModeFinding && tau_byIsolationMVArun2v1DBoldDMwLT>2.5'


cuts['d_samecharge'] = '&& abs(tau_gen_pdgId) == 1 && tau_gen_pdgId * tau_charge > 0.'
cuts['d_oppcharge'] = '&& abs(tau_gen_pdgId) == 1 && tau_gen_pdgId * tau_charge < 0.'
cuts['s_samecharge'] = '&& abs(tau_gen_pdgId) == 3 && tau_gen_pdgId * tau_charge > 0.'
cuts['s_oppcharge'] = '&& abs(tau_gen_pdgId) == 3 && tau_gen_pdgId * tau_charge < 0.'
cuts['b_samecharge'] = '&& abs(tau_gen_pdgId) == 5 && tau_gen_pdgId * tau_charge > 0.'
cuts['b_oppcharge'] = '&& abs(tau_gen_pdgId) == 5 && tau_gen_pdgId * tau_charge < 0.'
cuts['u_samecharge'] = '&& abs(tau_gen_pdgId) == 2 && tau_gen_pdgId * tau_charge < 0.'
cuts['u_oppcharge'] = '&& abs(tau_gen_pdgId) == 2 && tau_gen_pdgId * tau_charge > 0.'
cuts['c_samecharge'] = '&& abs(tau_gen_pdgId) == 4 && tau_gen_pdgId * tau_charge < 0.'
cuts['c_oppcharge'] = '&& abs(tau_gen_pdgId) == 4 && tau_gen_pdgId * tau_charge > 0.'
cuts['gluon'] = '&& abs(tau_gen_pdgId) == 21'

# cuts['tau_jet_80_100'] = '&& jet_pt>80 && jet_pt<100 && jet_pt>jet1_pt'
cuts['tau_jet_80_100'] = '&& jet_pt>80 && jet_pt<100 && n_jets==0'

# cuts['Update_OS'] = inc_cut + '&& l1_charge != tau_charge'
# cuts['Update_OSlowMT'] = inc_cut + '&& l1_charge != tau_charge && mt<40'
# cuts['Update_SSlowMT'] = inc_cut + '&& l1_charge == tau_charge && mt<40'

# cuts['Update_OShighMT'] = inc_cut + '&& l1_charge != tau_charge && mt>40'
# cuts['Update_SShighMT'] = inc_cut + '&& l1_charge == tau_charge && mt>40'

# cut_names = [cut for cut in cuts]
# for cut in cut_names:
#     cuts[cut+'_plus'] = cuts[cut] + ' && l1_charge==1'
#     cuts[cut+'_minus'] = cuts[cut] + ' && l1_charge==-1'

# cut_names = [cut for cut in cuts]
# for cut in cut_names:
#     # cuts[cut+'invmu'] = cuts[cut].replace('l1_reliso05<0.1', 'l1_reliso05>0.1')
#     cuts[cut+'invtau'] = cuts[cut].replace('tau_byCombinedIsolationDeltaBetaCorrRaw3Hits<1.5', 'tau_byCombinedIsolationDeltaBetaCorrRaw3Hits>1.5')

qcd_from_same_sign = False

# -> Command line
analysis_dir = '/data1/steggema/TauFRPU'
data_dir = analysis_dir

samples_mc, samples_data, samples, all_samples, sampleDict = createSampleLists(analysis_dir=analysis_dir, channel='tau_fr')

samples_mc_w = [s for s in samples_mc if fnmatch.fnmatch(s.name, 'W*Jet*')]
samples_mc_tt = [s for s in samples_mc if fnmatch.fnmatch(s.name, 'TT*')]

# Taken from Variables.py, can get subset with e.g. getVars(['mt', 'mvis'])
variables = getVars(['n_jets'])

variables += [
    VariableCfg(name='muon_pt', binning={'nbinsx':40, 'xmin':0., 'xmax':100.}, unit='GeV', xtitle='muon p_{T}'),
    VariableCfg(name='tau_pt', binning={'nbinsx':40, 'xmin':0., 'xmax':100.}, unit='GeV', xtitle='tau p_{T}'),
    VariableCfg(name='jet_pt', binning=array([20., 30., 40., 50., 60., 70., 80., 90., 100., 150., 200.]), unit='GeV', xtitle='tau jet p_{T}'),
    VariableCfg(name='tau_pt', binning=array([20., 25., 30., 35., 40., 50., 60., 80., 120., 200.]), unit='GeV', xtitle='tau p_{T}'),
]

# variables += [v for v in all_vars if 'dxy' in v.name or 'dz' in v.name]

# variables = getVars(['_norm_', 'tau_pt', 'tau_eta', 'tau_mass', 'tau_decayMode', 'mvis', 'mt', 'delta_r_l1_l2', 'tau_gen_pdgId', 'tau_mt'])
# variables = all_vars

for cut_name in cuts:
    cfg_tight = HistogramCfg(name='tight', var=None, cfgs=samples_mc_w, cut=inc_cut, lumi=int_lumi, weight=total_weight + ' * ((tau_gen_match == 6))')
    cfg_loose = HistogramCfg(name='loose', var=None, cfgs=samples_mc_w, cut=inc_cut, lumi=int_lumi, weight=total_weight + ' * ((tau_gen_match == 6))')

    cfg_data_tight = HistogramCfg(name='tight_data', var=None, cfgs=samples_mc_tt, cut=inc_cut, lumi=int_lumi, weight=total_weight + ' * ((tau_gen_match == 6))')
    cfg_data_loose = HistogramCfg(name='loose_data', var=None, cfgs=samples_mc_tt, cut=inc_cut, lumi=int_lumi, weight=total_weight  + ' * ((tau_gen_match == 6))')


    tight_cut = inc_cut + cuts[cut_name]
    loose_cut = tight_cut.replace('tau_byIsolationMVArun2v1DBoldDMwLT>2.5', '1.')

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
                          'taufrplots/fakerate_' + variable.name + cut_name + '.pdf',
                          mc_leg='W+jets', obs_leg='t#bar{t}',
                          ratio_leg='W/t#bar{t}')

