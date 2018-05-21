import copy
import socket
from CMGTools.H2TauTau.proto.plotter.PlotConfigs import HistogramCfg
from CMGTools.VVResonances.plotting.categories_VV_2017 import *
from CMGTools.VVResonances.plotting.HistCreator import createHistograms
from CMGTools.VVResonances.plotting.HistDrawer import HistDrawer
from CMGTools.VVResonances.plotting.Variables import *
from CMGTools.VVResonances.plotting.Samples_2017 import createSampleLists
# from CMGTools.H2TauTau.proto.plotter.helper_methods import plotDataOverMCEff

# always cut on category, otherwise normalisation is off!
total_weight = '(njj>0)'

print 'Total weight:', total_weight

weight_MC = "genWeight * puWeight"

int_lumi = 13500

cuts = {}

# if adding additional cuts, join with * and not &&, e.g.
# inc_cut = '*'.join([lnujj_inc])
# cuts['lnujj_Inclusive'] = categories["lnujj_Inclusive"]

# (HLT_JJ>0&&njj>0&&Flag_goodVertices&&Flag_HBHENoiseFilter&&Flag_HBHENoiseIsoFilter&&Flag_eeBadScFilter&&jj_LV_mass>1000&&abs(jj_l1_eta-jj_l2_eta)<1.3&&jj_l1_softDrop_mass>0.&&jj_l2_softDrop_mass>0.)

qcdKFac = 0.7
cutDDT = 0.57
cutDDT_LP = 0.98

cuts['jj'] = jj_inc + "&&(abs(jj_l1_eta-jj_l2_eta)<1.3)"
# cuts['jj_l1_V'] = cuts['jj'] + "&&(jj_l1_softDrop_mass>55&&jj_l1_softDrop_mass<105)"
# cuts['jj_l2_V'] = cuts['jj'] + "&&(jj_l2_softDrop_mass>55&&jj_l2_softDrop_mass<105)"
# cuts['jj_l1_V_HP'] = cuts['jj'] + "&&(jj_l1_softDrop_mass>55&&jj_l1_softDrop_mass<105&&jj_l1_tau21_DDT<{})".format(cutDDT)
# cuts['jj_l2_V_HP'] = copy.deepcopy(cuts['jj']) + "&&(jj_l2_softDrop_mass>55&&jj_l2_softDrop_mass<105&&jj_l2_tau21_DDT<{})".format(cutDDT)
l1_LP = "&&(jj_l1_tau21_DDT>{}&&jj_l1_tau21_DDT<{})".format(cutDDT, cutDDT_LP)
l2_LP = "&&(jj_l2_tau21_DDT>{}&&jj_l2_tau21_DDT<{})".format(cutDDT, cutDDT_LP)
l1_NP = "&&(jj_l1_tau21_DDT>{})".format(cutDDT_LP)
l2_NP = "&&(jj_l2_tau21_DDT>{})".format(cutDDT_LP)
cuts['jj_l1_LP'] = cuts['jj'] + l1_LP
cuts['jj_l2_LP'] = cuts['jj'] + l2_LP
cuts['jj_l1_NP'] = cuts['jj'] + l1_NP
cuts['jj_l2_NP'] = cuts['jj'] + l2_NP
cuts['jj_LP'] = cuts['jj'] + l1_LP + l2_LP
cuts['jj_NP'] = cuts['jj'] + l1_NP + l2_NP

# del cuts['jj']

# cuts['lnujj_mu'] = findCut(categories, cat="lnujj", lep="mu")
# cuts['lnujj_e'] = findCut(categories, cat="lnujj", lep="e")
# cuts['lnujj_ttbar_mu_b'] = findCut(categories, cat="lnujj", lep="mu", reg="b")
# cuts['lnujj_ttbar_e_b'] = findCut(categories, cat="lnujj", lep="e", reg="b")
# cuts['lnujj_mu_nob'] = findCut(categories, cat="lnujj", lep="mu", reg="nob")
# cuts['lnujj_e_nob'] = findCut(categories, cat="lnujj", lep="e", reg="nob")
# cuts['lnujj_e_veto_mV_nob'] = findCut(categories, cat="lnujj", lep="e", mJ="VetoV", reg="nob")
# cuts['lnujj_mu_veto_mV_nob'] = findCut(categories, cat="lnujj", lep="mu", mJ="VetoV", reg="nob")
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


# -> Command line
analysis_dir = '/eos/cms/store/cmst3/group/exovv/VVtuple/VV3Dproduction/2017_JEC_V6/'
if socket.gethostname().find("uzhcms1") >= 0:
    analysis_dir = '/data/clange/ntuples/2017_JEC_V6/'
print "Analysis dir:", analysis_dir
tree_prod_name = ''

samples_mc, samples_data, samples, all_samples, sampleDict = createSampleLists(analysis_dir, channel='VV', weight=weight_MC, qcdKFac=qcdKFac)
samples = samples_mc + [samples_data[4]]

# Taken from Variables.py, can get subset with e.g. getVars(['mt', 'mvis'])
variables = generic_vars + jj_vars + jj_l1_jetid + jj_l2_jetid
# variables = [lnujj_vars[0]]
# variables = getVars(['l1_reliso05', 'l2_reliso05'])
# variables = [
#     VariableCfg(name='mvis', binning={'nbinsx':35, 'xmin':0, 'xmax':350}, unit='GeV', xtitle='m_{vis}')
# ]

for cut_name in cuts:

    cfg_example = HistogramCfg(name='example', var=None, cfgs=samples, cut='', lumi=int_lumi, weight=total_weight)

    cfg_example.cut = cuts[cut_name]
    print cfg_example.cut
    cfg_example.vars = variables

    channel = ""
    # channel = "jj"
    # if cut_name.find("HP") >= 0:
    #     channel += " HP"
    # elif cut_name.find("LP") >= 0:
    #     channel += " LP"

    plots = createHistograms(cfg_example, verbose=False)
    for variable in variables:
        plot = plots[variable.name]
        # plot.Group('Diboson', ['WWTo1L1Nu2Q', 'WWTo1L1Nu2Q', 'WZTo1L1Nu2Q'])
        plot.Group('Top', ['TTHad_pow'])
        plot.Group('WJets', ['WJetsToQQ_HT800toInf'])
        plot.Group('ZJets', ['ZJetsToQQ_HT800toInf'])
        plot.Group('QCD', ['QCD_HT100to200', 'QCD_HT200to300', 'QCD_HT300to500', 'QCD_HT500to700', 'QCD_HT700to1000', 'QCD_HT1000to1500', 'QCD_HT1500to2000', 'QCD_HT2000toInf'])
        plot.Group('data_obs', ['data_JetHT_Run2017F'])
        HistDrawer.draw(plot, plot_dir='plots_jj_Run2017F/'+cut_name, channel=channel)
        # plot.WriteDataCard(filename='datacard_mm.root', dir='mm_' + cut_name)
