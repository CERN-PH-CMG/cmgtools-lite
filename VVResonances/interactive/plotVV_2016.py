# import copy
from CMGTools.H2TauTau.proto.plotter.PlotConfigs import HistogramCfg
from CMGTools.VVResonances.plotting.categories_VV_2016 import *
from CMGTools.VVResonances.plotting.HistCreator import createHistograms
from CMGTools.VVResonances.plotting.HistDrawer import HistDrawer
from CMGTools.VVResonances.plotting.Variables import *
from CMGTools.VVResonances.plotting.Samples_2016 import createSampleLists
from CMGTools.H2TauTau.proto.plotter.helper_methods import plotDataOverMCEff

# always cut on category, otherwise normalisation is off!
total_weight = '(njj>0)'

print 'Total weight:', total_weight

weight_MC = "genWeight * puWeight"

int_lumi = 12900

cuts = {}

# if adding additional cuts, join with * and not &&, e.g.
# inc_cut = '*'.join([jj_inc])
cuts['jj_inc_l1_tau21_all_l2_tau21_all'] = categories["jj_inc_l1_tau21_all_l2_tau21_all"]
cuts['jj_inc_l1_tau21_HP_mJ_W_l2_tau21_HP_mJ_W'] = categories["jj_inc_l1_tau21_HP_mJ_W_l2_tau21_HP_mJ_W"]
cuts['jj_inc_l1_tau21_HP_l2_tau21_all'] = categories["jj_inc_l1_tau21_HP_l2_tau21_all"]
cuts['jj_inc_l1_tau21_HP_l2_tau21_HP_mJ_W'] = categories["jj_inc_l1_tau21_HP_l2_tau21_HP_mJ_W"]


# -> Command line
analysis_dir = '/data/clange/ntuples/VV_20161117/'
tree_prod_name = ''

samples_mc, samples_data, samples, all_samples, sampleDict = createSampleLists(analysis_dir, channel='VV', weight=weight_MC)

# Taken from Variables.py, can get subset with e.g. getVars(['mt', 'mvis'])
variables = jj_l1_vars + jj_l2_vars + generic_vars
# variables = [jj_l1_vars[0]]
# variables = getVars(['l1_reliso05', 'l2_reliso05'])
# variables = [
#     VariableCfg(name='mvis', binning={'nbinsx':35, 'xmin':0, 'xmax':350}, unit='GeV', xtitle='m_{vis}')
# ]

for cut_name in cuts:

    cfg_example = HistogramCfg(name='example', var=None, cfgs=samples, cut='', lumi=int_lumi, weight=total_weight)

    cfg_example.cut = cuts[cut_name]
    cfg_example.vars = variables

    plots = createHistograms(cfg_example, verbose=False)
    for variable in variables:
        plot = plots[variable.name]
        # plot.Group('Diboson', ['WWTo1L1Nu2Q', 'WZTo1L1Nu2Q'])
        # plot.Group('TT_W', ['TTJets_W'])
        # plot.Group('W', ['WJetsToLNu_HT100to200', 'WJetsToLNu_HT200to400', 'WJetsToLNu_HT400to600', 'WJetsToLNu_HT600to800', 'WJetsToLNu_HT800to1200', 'WJetsToLNu_HT1200to2500', 'WJetsToLNu_HT2500toInf'])
        plot.Group('QCD', ['QCD_HT2000toInf', 'QCD_HT1500to2000', 'QCD_HT1000to1500', 'QCD_HT700to1000', 'QCD_HT500to700', 'QCD_HT300to500'])
        # plot.Group('TT_nonW', ['TTJets_nonW'])
        # plot.Group('Single t', ['TToLeptons_tch_powheg', 'TBarToLeptons_tch_powheg', 'TToLeptons_sch', 'TBar_tWch', 'T_tWch'])
        # plot.Group('ZLL', ['DYJetsToLL_M50_HT100to200', 'DYJetsToLL_M50_HT200to400', 'DYJetsToLL_M50_HT400to600', 'DYJetsToLL_M50_HT600toInf'])
        plot.Group('data_obs', ['data_JetHT']) #, 'data_JetHT'
        #['WpWpJJ', 'ZGTo2LG', 'ZGJets', 'WGToLNuG', 'WGJets', 'WW', 'WWDouble', 'WWTo1L1Nu2Q', 'WWToLNuQQ_ext', 'WWToLNuQQ', 'WWTo2L2Nu', 'WZ', 'WZTo3LNu_amcatnlo', 'WZTo3LNu', 'WZTo2L2Q', 'WZTo1L1Nu2Q', 'WZTo1L3Nu', 'ZZ', 'VVTo2L2Nu', 'ZZTo4L', 'ZZTo2Q2Nu', 'ZZTo2L2Q', 'ZZTo2L2Nu'])
        HistDrawer.draw(plot, plot_dir='plots/'+cut_name, channel='VV #rightarrow jj')

        # plot.WriteDataCard(filename='datacard_mm.root', dir='mm_' + cut_name)
