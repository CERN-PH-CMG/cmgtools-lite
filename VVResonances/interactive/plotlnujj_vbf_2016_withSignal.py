# import copy
from CMGTools.H2TauTau.proto.plotter.PlotConfigs import HistogramCfg
from CMGTools.VVResonances.plotting.categories_VV_2016 import *
from CMGTools.VVResonances.plotting.HistCreator import createHistograms
from CMGTools.VVResonances.plotting.HistDrawer import HistDrawer
from CMGTools.VVResonances.plotting.Variables import *
from CMGTools.VVResonances.plotting.Samples_2016 import createSampleLists
# from CMGTools.H2TauTau.proto.plotter.helper_methods import plotDataOverMCEff

# always cut on category, otherwise normalisation is off!
total_weight = '(nlnujj>0)'

print 'Total weight:', total_weight

weight_MC = "genWeight * puWeight"

int_lumi = 35867

cuts = {}

# if adding additional cuts, join with * and not &&, e.g.
# inc_cut = '*'.join([lnujj_inc])

cuts['lnujj_mu'] = findCut(categories, cat="lnujj", lep="mu")
cuts['lnujj_e'] = findCut(categories, cat="lnujj", lep="e")
cuts['lnujj_ttbar_mu_b'] = findCut(categories, cat="lnujj", lep="mu", reg="b")
cuts['lnujj_ttbar_e_b'] = findCut(categories, cat="lnujj", lep="e", reg="b")
# cuts['lnujj_mu_nob'] = findCut(categories, cat="lnujj", lep="mu", reg="nob")
# cuts['lnujj_e_nob'] = findCut(categories, cat="lnujj", lep="e", reg="nob")
cuts['lnujj_mu_nob_veto_mV'] = findCut(categories, cat="lnujj", lep="mu", mJ="VetoV", reg="nob")
cuts['lnujj_e_nob_veto_mV'] = findCut(categories, cat="lnujj", lep="e", mJ="VetoV", reg="nob")
# cuts['lnujj_ttbar_mu_SP_b'] = findCut(categories, cat="lnujj", lep="mu", tau21="SP", reg="b")
# cuts['lnujj_ttbar_e_SP_b'] = findCut(categories, cat="lnujj", lep="e", tau21="SP", reg="b")
# cuts['lnujj_ttbar_mu_mV_b'] = findCut(categories, cat="lnujj", lep="mu", mJ="V", reg="b")
# cuts['lnujj_ttbar_e_mV_b'] = findCut(categories, cat="lnujj", lep="e", mJ="V", reg="b")
# cuts['lnujj_mu_SP_veto_mV'] = findCut(categories, cat="lnujj", lep="mu", tau21="SP", mJ="VetoV")
# cuts['lnujj_e_SP_veto_mV'] = findCut(categories, cat="lnujj", lep="e", tau21="SP", mJ="VetoV")
# cuts['lnujj_e_HP_veto_mV_nob'] = findCut(categories, cat="lnujj", lep="e", tau21="HP", mJ="VetoV", reg="nob")
# cuts['lnujj_mu_HP_veto_mV_nob'] = findCut(categories, cat="lnujj", lep="mu", tau21="HP", mJ="VetoV", reg="nob")
# cuts['lnujj_e_HP_veto_mV'] = findCut(categories, cat="lnujj", lep="e", tau21="HP", mJ="VetoV")
# cuts['lnujj_mu_HP_veto_mV'] = findCut(categories, cat="lnujj", lep="mu", tau21="HP", mJ="VetoV")
# cuts['lnujj_ttbar_e_HP_b'] = findCut(categories, cat="lnujj", lep="e", tau21="HP", reg="b")
# cuts['lnujj_ttbar_mu_HP_b'] = findCut(categories, cat="lnujj", lep="mu", tau21="HP", reg="b")

# in order to be able to use standard categories, replace all cuts with vbf ones
vbfCuts = {}
for cutName, cut in cuts.iteritems():
    # vbfCuts[cutName+"_vbf_DEta"] = cut + "*(lnujj_vbfDEta>4.0)"
    # vbfCuts[cutName+"_vbf_Mass"] = cut + "*(lnujj_vbfMass>400)"
    vbfCuts[cutName+"_vbf_DEta_Mass"] = cut + "*(lnujj_vbfDEta>4.0&&lnujj_vbfMass>400)"
    # vbfCuts[cutName+"_novbf"] = cut + "*(lnujj_vbfDEta<=4.0||lnujj_vbfMass<=400)"
cuts.update(vbfCuts)

# -> Command line
analysis_dir = '/data/clange/ntuples/FixMass/'
tree_prod_name = ''

samples_mc, samples_data, samples, all_samples, sampleDict = createSampleLists(analysis_dir, channel='WV', weight=weight_MC, signalSample='VBF_RadionToWW_narrow_2500')

# Taken from Variables.py, can get subset with e.g. getVars(['mt', 'mvis'])
variables = generic_vars + lnujj_vars + lnujj_vbf_vars
# variables = [lnujj_vars[0]]
# variables = getVars(['l1_reliso05', 'l2_reliso05'])
# variables = [
#     VariableCfg(name='mvis', binning={'nbinsx':35, 'xmin':0, 'xmax':350}, unit='GeV', xtitle='m_{vis}')
# ]

for cut_name in cuts:

    cfg_example = HistogramCfg(name='example', var=None, cfgs=samples, cut='', lumi=int_lumi, weight=total_weight)

    cfg_example.cut = cuts[cut_name]
    cfg_example.vars = variables

    channel = "l#nujj"
    if cut_name.find("_mu") >= 0:
        channel = "#mu#nujj"
    elif cut_name.find("_e") >= 0:
        channel = "e#nujj"
    if cut_name.find("novbf") >= 0:
        channel += " noVBF"
    else:
        channel += " VBF"
    if cut_name.find("HP") >= 0:
        channel += " HP"
    elif cut_name.find("LP") >= 0:
        channel += " LP"

    plots = createHistograms(cfg_example, verbose=False)
    for variable in variables:
        plot = plots[variable.name]
        plot.Group('Diboson', ['WWTo1L1Nu2Q', 'WWTo1L1Nu2Q', 'WZTo1L1Nu2Q'])
        plot.Group('Top', ['TT_pow_W', 'TT_pow_nonW', 'TToLeptons_tch_powheg', 'TBarToLeptons_tch_powheg', 'TToLeptons_sch', 'TBar_tWch', 'T_tWch'])
        plot.Group('VJets', ['WJetsToLNu_HT100to200', 'WJetsToLNu_HT200to400', 'WJetsToLNu_HT400to600', 'WJetsToLNu_HT600to800', 'WJetsToLNu_HT800to1200', 'WJetsToLNu_HT1200to2500', 'WJetsToLNu_HT2500toInf', 'DYJetsToLL_M50_HT100to200', 'DYJetsToLL_M50_HT200to400', 'DYJetsToLL_M50_HT400to600', 'DYJetsToLL_M50_HT600to800', 'DYJetsToLL_M50_HT800to1200', 'DYJetsToLL_M50_HT1200to2500', 'DYJetsToLL_M50_HT2500toInf'])
        plot.Group('QCD', ['QCD_HT2000toInf', 'QCD_HT1500to2000', 'QCD_HT1000to1500', 'QCD_HT700to1000', 'QCD_HT500to700'])  # , 'QCD_HT300to500'
        plot.Group('data_obs', ['data_SingleMuon', 'data_SingleElectron', 'data_MET']) #, 'data_JetHT'
        #['WpWpJJ', 'ZGTo2LG', 'ZGJets', 'WGToLNuG', 'WGJets', 'WW', 'WWDouble', 'WWTo1L1Nu2Q', 'WWToLNuQQ_ext', 'WWToLNuQQ', 'WWTo2L2Nu', 'WZ', 'WZTo3LNu_amcatnlo', 'WZTo3LNu', 'WZTo2L2Q', 'WZTo1L1Nu2Q', 'WZTo1L3Nu', 'ZZ', 'VVTo2L2Nu', 'ZZTo4L', 'ZZTo2Q2Nu', 'ZZTo2L2Q', 'ZZTo2L2Nu'])
        HistDrawer.draw(plot, plot_dir='plots_lnujj_vbf_withSignal/'+cut_name, channel=channel)

        # plot.WriteDataCard(filename='datacard_mm.root', dir='mm_' + cut_name)
