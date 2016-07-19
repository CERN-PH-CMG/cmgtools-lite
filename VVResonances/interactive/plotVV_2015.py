import copy

print "importing HistogramCfg"
from CMGTools.H2TauTau.proto.plotter.PlotConfigs import HistogramCfg
print "importing cat_Inc"
from CMGTools.VVResonances.plotting.categories_VV_2015 import cat_Inc
print "importing createHistograms"
from CMGTools.VVResonances.plotting.HistCreator import createHistograms
print "importing HistDrawer"
from CMGTools.VVResonances.plotting.HistDrawer import HistDrawer
print "importing Variables"
from CMGTools.VVResonances.plotting.Variables import getVars, VV_vars
print "importing createSampleLists"
from CMGTools.VVResonances.plotting.Samples import createSampleLists
print "importing plotDataOverMCEff"
from CMGTools.H2TauTau.proto.plotter.helper_methods import plotDataOverMCEff

print "Done importing"

total_weight = ''

print 'Total weight', total_weight

weight_MC = "genWeight * puWeight"

int_lumi = 2630

cuts = {}

inc_cut = '&&'.join([cat_Inc])

cuts['NoSubstructure'] = inc_cut #+ '&& l1_charge != l2_charge && abs(l1_eta) < 2.1 && mvis>50'

# -> Command line
analysis_dir = '/data/clange/ntuples/2015_76X_Pruning_20160708/'
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
        plot.Group('QCD', ['QCD_HT2000toInf', 'QCD_HT1500to2000', 'QCD_HT1000to1500', 'QCD_HT700to1000', 'QCD_HT500to700', 'QCD_HT300to500', 'QCD_HT200to300'])
        plot.Group('TT', ['TTJets'])
        # plot.Group('ZLL', ['ZL', 'ZJ'], style=plot.Hist('ZL').style)
        # plot.Group('Electroweak', ['W', 'VV'])
        HistDrawer.draw(plot, plot_dir='plots/'+cut_name, channel='VV')

        # plot.WriteDataCard(filename='datacard_mm.root', dir='mm_' + cut_name)
