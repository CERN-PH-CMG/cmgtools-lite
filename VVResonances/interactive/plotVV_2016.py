import copy

print "importing HistogramCfg"
from CMGTools.H2TauTau.proto.plotter.PlotConfigs import HistogramCfg
print "importing cat_Inc"
from CMGTools.VVResonances.plotting.categories_VV_2016 import cat_Inc
print "importing createHistograms"
from CMGTools.VVResonances.plotting.HistCreator import createHistograms
print "importing HistDrawer"
from CMGTools.VVResonances.plotting.HistDrawer import HistDrawer
print "importing Variables"
from CMGTools.VVResonances.plotting.Variables import getVars, VV_vars
print "importing createSampleLists"
from CMGTools.VVResonances.plotting.Samples_2016 import createSampleLists
print "importing plotDataOverMCEff"
from CMGTools.H2TauTau.proto.plotter.helper_methods import plotDataOverMCEff

print "Done importing"

total_weight = '1.'

print 'Total weight', total_weight

weight_MC = "genWeight * puWeight"

int_lumi = 7650

cuts = {}

inc_cut = '&&'.join([cat_Inc])

cuts['NoSubstructure'] = inc_cut #+ '&& l1_charge != l2_charge && abs(l1_eta) < 2.1 && mvis>50'

# -> Command line
analysis_dir = '/data/bachtis/VV/data/2016_80X_Pruning/'
tree_prod_name = ''

samples_mc, samples_data, samples, all_samples, sampleDict = createSampleLists(analysis_dir, channel='VV', weight=weight_MC)

# Taken from Variables.py, can get subset with e.g. getVars(['mt', 'mvis'])
variables = VV_vars
# variables = getVars(['l1_reliso05', 'l2_reliso05'])
# variables = [
#     VariableCfg(name='mvis', binning={'nbinsx':35, 'xmin':0, 'xmax':350}, unit='GeV', xtitle='m_{vis}')
# ]

for cut_name in cuts:

    cfg_example = HistogramCfg(name='example', var=None, cfgs=samples, cut=inc_cut, lumi=int_lumi, weight=total_weight)


    cfg_example.cut = cuts[cut_name]

    cfg_example.vars = variables

    plots = createHistograms(cfg_example, verbose=True)
    for variable in variables:
        plot = plots[variable.name]
        plot.Group('QCD', ['QCD_HT2000toInf', 'QCD_HT1500to2000', 'QCD_HT1000to1500', 'QCD_HT700to1000', 'QCD_HT300to500'])
        plot.Group('TT', ['TTJets'])
        plot.Group('Single t', ['TToLeptons_sch', 'TBarToLeptons_tch_powheg', 'TToLeptons_sch_amcatnlo', 'TBar_tWch', 'T_tWch', 'TGJets', 'TGJets_ext'])
        plot.Group('ZLL', ['DYJetsToLL_M50_HT100to200', 'DYJetsToLL_M50_HT200to400', 'DYJetsToLL_M50_HT400to600', 'DYJetsToLL_M50_HT600toInf'])
        plot.Group('W', ['WJetsToLNu_HT100to200', 'WJetsToLNu_HT200to400', 'WJetsToLNu_HT400to600', 'WJetsToLNu_HT600to800', 'WJetsToLNu_HT800to1200', 'WJetsToLNu_HT1200to2500', 'WJetsToLNu_HT2500toInf'])
        plot.Group('Electroweak', ['WpWpJJ', 'ZGTo2LG', 'ZGJets', 'WGToLNuG', 'WGJets', 'WW', 'WWDouble', 'WWTo1L1Nu2Q', 'WWToLNuQQ_ext', 'WWToLNuQQ', 'WWTo2L2Nu', 'WZ', 'WZTo3LNu_amcatnlo', 'WZTo3LNu', 'WZTo2L2Q', 'WZTo1L1Nu2Q', 'WZTo1L3Nu', 'ZZ', 'VVTo2L2Nu', 'ZZTo4L', 'ZZTo2Q2Nu', 'ZZTo2L2Q', 'ZZTo2L2Nu'])
        HistDrawer.draw(plot, plot_dir='plots/'+cut_name, channel='VV')

        # plot.WriteDataCard(filename='datacard_mm.root', dir='mm_' + cut_name)
