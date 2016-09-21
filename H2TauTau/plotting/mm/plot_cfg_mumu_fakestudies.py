from numpy import array

from CMGTools.H2TauTau.proto.samples.spring16.htt_common import lumi, lumi_2016G

from CMGTools.H2TauTau.proto.plotter.PlotConfigs import HistogramCfg, VariableCfg
from CMGTools.H2TauTau.proto.plotter.categories_MuMu import cat_Inc
from CMGTools.H2TauTau.proto.plotter.HistCreator import createHistograms
from CMGTools.H2TauTau.proto.plotter.HistDrawer import HistDrawer
from CMGTools.H2TauTau.proto.plotter.Variables import getVars, mumu_vars
from CMGTools.H2TauTau.proto.plotter.Samples import createSampleLists
from CMGTools.H2TauTau.proto.plotter.helper_methods import plotDataOverMCEff


# total_weight = 'weight/l1_weight_eff_data_trigger * ( (l2_pt>22.) * (1 - (1-l1_weight_eff_data_trigger)**2) + (l2_pt<22.) * l1_weight_eff_data_trigger ) '

total_weight = 'weight/l1_weight_eff_data_trigger * (1. - (1.-l1_weight_eff_data_trigger)*(1.-l1_weight_eff_data_trigger))'
# total_weight = 'weight/l1_weight_eff_data_trigger'# * (1. - (1.-l1_weight_eff_data_trigger)**2)'

print 'Total weight', total_weight

# -> Command line
analysis_dir = '/data1/steggema/mm/220716/MuMuMC'
data2016G = False

int_lumi = lumi

if data2016G:
    int_lumi = lumi_2016G

cuts = {}

inc_cut = '&&'.join([cat_Inc])
inc_cut += '&& tau1_pt>30'
# cuts['OS_PU_mZ'] = inc_cut + '&& l1_charge != l2_charge && abs(l1_eta) < 2.1 && abs(l2_eta) < 2.1 && mvis>70 && mvis<100'
# cuts['OS_PU_mZ_lowPU'] = inc_cut + '&& l1_charge != l2_charge && abs(l1_eta) < 2.1 && abs(l2_eta) < 2.1 && mvis>70 && mvis<100 && n_vertices<12'
# cuts['OS_PU_mZ_highPU'] = inc_cut + '&& l1_charge != l2_charge && abs(l1_eta) < 2.1 && abs(l2_eta) < 2.1 && mvis>70 && mvis<100 && n_vertices>20'

# cuts['OS_PU_mZ_eq1jet'] = inc_cut + '&& l1_charge != l2_charge && abs(l1_eta) < 2.1 && abs(l2_eta) < 2.1 && mvis>70 && mvis<100 && n_jets==1'

# cuts['OS_PU_mZ_eq1jet_tau1'] = inc_cut + '&& l1_charge != l2_charge && abs(l1_eta) < 2.1 && abs(l2_eta) < 2.1 && mvis>70 && mvis<100 && n_jets==1 && tau1_pt>0.'
cuts['OS_PU_mZ_eq1jet_tau1_dm'] = (
    inc_cut + '&& l1_charge != l2_charge && abs(l1_eta) < 2.1 && abs(l2_eta) < 2.1 && mvis>70 && mvis<100 && n_jets==1 && tau1_decayModeFinding>0.',
    inc_cut + '&& l1_charge != l2_charge && abs(l1_eta) < 2.1 && abs(l2_eta) < 2.1 && mvis>70 && mvis<100 && n_jets==1')

cuts['OS_PU_mZ_eq1jet_tau1_dbiso'] = (
    inc_cut + '&& l1_charge != l2_charge && abs(l1_eta) < 2.1 && abs(l2_eta) < 2.1 && mvis>70 && mvis<100 && n_jets==1 && tau1_decayModeFinding>0. && tau1_byCombinedIsolationDeltaBetaCorr3Hits>1.5',
    inc_cut + '&& l1_charge != l2_charge && abs(l1_eta) < 2.1 && abs(l2_eta) < 2.1 && mvis>70 && mvis<100 && n_jets==1 && tau1_decayModeFinding>0.')

cuts['OS_PU_mZ_eq1jet_tau1_dmplusdbiso'] = (
    inc_cut + '&& l1_charge != l2_charge && abs(l1_eta) < 2.1 && abs(l2_eta) < 2.1 && mvis>70 && mvis<100 && n_jets==1 && tau1_decayModeFinding>0. && tau1_byCombinedIsolationDeltaBetaCorr3Hits>1.5',
    inc_cut + '&& l1_charge != l2_charge && abs(l1_eta) < 2.1 && abs(l2_eta) < 2.1 && mvis>70 && mvis<100 && n_jets==1')

cuts['OS_PU_mZ_eq1jet_tau1_mvaiso'] = (
    inc_cut + '&& l1_charge != l2_charge && abs(l1_eta) < 2.1 && abs(l2_eta) < 2.1 && mvis>70 && mvis<100 && n_jets==1 && tau1_decayModeFinding>0. && tau1_byIsolationMVArun2v1DBoldDMwLT>3.5',
    inc_cut + '&& l1_charge != l2_charge && abs(l1_eta) < 2.1 && abs(l2_eta) < 2.1 && mvis>70 && mvis<100 && n_jets==1 && tau1_decayModeFinding>0.')


cuts['OS_PU_mZ_eq1jet_tau1_ptouter'] = (
    inc_cut + '&& l1_charge != l2_charge && abs(l1_eta) < 2.1 && abs(l2_eta) < 2.1 && mvis>70 && mvis<100 && n_jets==1 && tau1_decayModeFinding>0. && tau1_byCombinedIsolationDeltaBetaCorrRaw3Hits<1.5 && tau1_photonPtSumOutsideSignalCone/tau1_pt<0.1',
    inc_cut + '&& l1_charge != l2_charge && abs(l1_eta) < 2.1 && abs(l2_eta) < 2.1 && mvis>70 && mvis<100 && n_jets==1 && tau1_decayModeFinding>0. && tau1_byCombinedIsolationDeltaBetaCorrRaw3Hits<1.5')

cuts['OS_PU_mZ_eq1jet_tau1_noptouter'] = (
    inc_cut + '&& l1_charge != l2_charge && abs(l1_eta) < 2.1 && abs(l2_eta) < 2.1 && mvis>70 && mvis<100 && n_jets==1 && tau1_decayModeFinding>0. && tau1_byCombinedIsolationDeltaBetaCorrRaw3Hits<1.5',
    inc_cut + '&& l1_charge != l2_charge && abs(l1_eta) < 2.1 && abs(l2_eta) < 2.1 && mvis>70 && mvis<100 && n_jets==1 && tau1_decayModeFinding>0.')

samples_mc, samples_data, samples, all_samples, sampleDict = createSampleLists(analysis_dir, channel='mm', ztt_cut='(l1_gen_match == 4 && l2_gen_match == 4)', zl_cut='(l1_gen_match == 2 && l2_gen_match == 2)', zj_cut='(l1_gen_match != l2_gen_match || (l1_gen_match != 4 && l1_gen_match != 2))', data2016G=data2016G)


# Taken from Variables.py, can get subset with e.g. getVars(['mt', 'mvis'])
# variables = mumu_vars
variables = getVars(['tau1_eta']) #'tau1_pt',
variables += [
    VariableCfg(name='jet1_pt', binning=array([30., 40., 50., 60., 80., 100., 120., 160.,  200., 350.]), unit='GeV', xtitle='jet p_{T}'),
    VariableCfg(name='tau1_pt', binning=array([30., 40., 50., 60., 80., 100., 150., 200.]), unit='GeV', xtitle='tau p_{T}'),
    VariableCfg(name='jet1_eta', binning={'nbinsx':25, 'xmin':-2.5, 'xmax':2.5}, unit='', xtitle='jet #eta'),
]
# variables = [
#     VariableCfg(name='mvis', binning={'nbinsx':35, 'xmin':0, 'xmax':350}, unit='GeV', xtitle='m_{vis}')
# ]

for cut_name in cuts:
    cfg_tight = HistogramCfg(name='tight', var=None, cfgs=samples, cut=inc_cut, lumi=int_lumi, weight=total_weight+'*( (abs(tau1_gen_pdgId)!=15) - (abs(tau1_gen_pdgId)==15))')
    cfg_loose = HistogramCfg(name='loose', var=None, cfgs=samples, cut=inc_cut, lumi=int_lumi, weight=total_weight+'*( (abs(tau1_gen_pdgId)!=15) - (abs(tau1_gen_pdgId)==15))')
    cfg_tight_data = HistogramCfg(name='tight_data', var=None, cfgs=samples, cut=inc_cut, lumi=int_lumi, weight=total_weight+'*( (is_data>0.5) - (abs(tau1_gen_pdgId)==15))')
    cfg_loose_data = HistogramCfg(name='loose_data', var=None, cfgs=samples, cut=inc_cut, lumi=int_lumi, weight=total_weight+'*( (is_data>0.5) - (abs(tau1_gen_pdgId)==15))')
        

    cfg_tight.cut = cuts[cut_name][0]
    cfg_loose.cut = cuts[cut_name][1]
    cfg_tight_data.cut = cuts[cut_name][0]
    cfg_loose_data.cut = cuts[cut_name][1]

    
    for cfg in [cfg_tight, cfg_loose, cfg_tight_data, cfg_loose_data]:
        cfg.vars = variables

    plots_tight = createHistograms(cfg_tight, verbose=True)
    plots_loose = createHistograms(cfg_loose, verbose=True)
    plots_tight_data = createHistograms(cfg_tight_data, verbose=True, all_stack=True)
    plots_loose_data = createHistograms(cfg_loose_data, verbose=True, all_stack=True)
    for variable in variables:    
        plot_tight = plots_tight[variable.name]
        plot_loose = plots_loose[variable.name]
        plot_tight_data = plots_tight_data[variable.name]
        plot_loose_data = plots_loose_data[variable.name]
        for plot in [plot_tight, plot_loose, plot_tight_data, plot_loose_data]:
            plot.Group('VV', ['WWTo1L1Nu2Q', 'WZTo1L1Nu2Q', 'WZTo1L3Nu', 'WZTo2L2Q', 'VVTo2L2Nu', 'ZZTo2L2Q', 'ZZTo4L'])
            plot.Group('Single t', ['T_tWch', 'TBar_tWch', 'TBarToLeptons_tch_powheg', 'TToLeptons_tch_powheg'])
            plot.Group('ZLL', ['ZL', 'ZJ'], style=plot.Hist('ZL').style)
            plot.Group('W', ['W1Jets', 'W2Jets', 'W3Jets', 'W4Jets'])
            plot.Group('Electroweak', ['W', 'VV', 'Single t'])
            # HistDrawer.draw(plot, plot_dir='plotsG/'+cut_name, channel='#mu#mu')
        
        base_dir = 'fakeplotsG' if data2016G else 'fakeplots'
        plotDataOverMCEff(plot_tight.GetStack().totalHist.weighted, 
                          plot_loose.GetStack().totalHist.weighted, 
                          plot_tight_data.GetStack().totalHist.weighted, 
                          plot_loose_data.GetStack().totalHist.weighted,
                          base_dir+'_dm/fakerate_' + variable.name + cut_name + '.pdf')
        # plot.WriteDataCard(filename='datacard_mm.root', dir='mm_' + cut_name)
