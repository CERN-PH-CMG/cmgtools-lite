import os
import ROOT
from ROOT import gSystem, gROOT

from CMGTools.H2TauTau.proto.plotter.PlotConfigs import SampleCfg
from CMGTools.VVResonances.plotting.HistCreator import setSumWeights


from CMGTools.RootTools.samples.samples_13TeV_RunIIFall15MiniAODv2 import TTJets, WJetsToLNuHT, QCDHT, DYJetsM50HT, GJetsHT
# from CMGTools.RootTools.samples.samples_13TeV_RunIIFall15MiniAODv2 import TT_pow_ext3 as TT_pow_ext
from CMGTools.RootTools.samples.samples_13TeV_DATA2015 import JetHT_Run2015C_25ns_16Dec, JetHT_Run2015D_16Dec, SingleElectron_Run2015C_25ns_16Dec, SingleElectron_Run2015D_16Dec, SingleMuon_Run2015C_25ns_16Dec, SingleMuon_Run2015D_16Dec
# from CMGTools.VVAnalysis.samples.signal_13TeV_80X import signalSamples

def createSampleLists(analysis_dir='/data/clange/ntuples/2015_76X_Pruning/',
                      channel='VV', weight=''):
    # -> Possibly from cfg like in the past, but may also make sense to enter directly

    tree_prod_name = ''

    samples_essential = []
    for qcdSample in QCDHT:
        if not ((qcdSample.name.find("_ext") >= 0) or (qcdSample.name.find("100to200") >= 0)):
            print qcdSample.name
            samples_essential.append(
            SampleCfg(name=qcdSample.name, dir_name=qcdSample.name, ana_dir=analysis_dir, tree_prod_name=tree_prod_name,
                  xsec=qcdSample.xSection, sumweights=qcdSample.nGenEvents, weight_expr=weight))
    samples_essential.append(
    SampleCfg(name=TTJets.name, dir_name=TTJets.name, ana_dir=analysis_dir, tree_prod_name=tree_prod_name,
          xsec=TTJets.xSection, sumweights=TTJets.nGenEvents, weight_expr=weight))

    samples_data = []
    # if channel in ['VV']:
    samples_data = [
        # SampleCfg(name='data_obs', dir_name='JetHT_Run2015C_25ns_16Dec', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, is_data=True),
        SampleCfg(name='data_obs', dir_name='JetHT_Run2015D_16Dec', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, is_data=True),
    ]

    # samples_WH = []
    # mssm_names = ['HiggsSUSYBB80', 'HiggsSUSYBB90', 'HiggsSUSYBB100', 'HiggsSUSYBB110', 'HiggsSUSYBB120', 'HiggsSUSYBB130', 'HiggsSUSYBB140', 'HiggsSUSYBB160', 'HiggsSUSYBB180', 'HiggsSUSYBB200', 'HiggsSUSYBB250', 'HiggsSUSYBB300', 'HiggsSUSYBB350', 'HiggsSUSYBB400', 'HiggsSUSYBB450', 'HiggsSUSYBB500', 'HiggsSUSYBB600', 'HiggsSUSYBB700', 'HiggsSUSYBB900', 'HiggsSUSYBB1000', 'HiggsSUSYBB1200', 'HiggsSUSYBB1500', 'HiggsSUSYBB1600', 'HiggsSUSYBB1800', 'HiggsSUSYBB2000', 'HiggsSUSYBB2300', 'HiggsSUSYBB2600', 'HiggsSUSYBB2900', 'HiggsSUSYBB3200', 'HiggsSUSYGG80', 'HiggsSUSYGG90',
    #               'HiggsSUSYGG100', 'HiggsSUSYGG110', 'HiggsSUSYGG120', 'HiggsSUSYGG130', 'HiggsSUSYGG140', 'HiggsSUSYGG160', 'HiggsSUSYGG180', 'HiggsSUSYGG200', 'HiggsSUSYGG250', 'HiggsSUSYGG300', 'HiggsSUSYGG400', 'HiggsSUSYGG450', 'HiggsSUSYGG500', 'HiggsSUSYGG600', 'HiggsSUSYGG700', 'HiggsSUSYGG800', 'HiggsSUSYGG900', 'HiggsSUSYGG1000', 'HiggsSUSYGG1200', 'HiggsSUSYGG1400', 'HiggsSUSYGG1500', 'HiggsSUSYGG1600', 'HiggsSUSYGG1800', 'HiggsSUSYGG2000', 'HiggsSUSYGG2300', 'HiggsSUSYGG2600', 'HiggsSUSYGG2900', 'HiggsSUSYGG3200']  # HiggsSUSYBB800, HiggsSUSYBB1400, HiggsSUSYGG350
    # for name in mssm_names:
    #     samples_WH.append(SampleCfg(name=name.replace('HiggsSUSYBB', 'bbH').replace('HiggsSUSYGG', 'ggH'), dir_name=name,
    #                                   ana_dir=analysis_dir, tree_prod_name=tree_prod_name, xsec=1., sumweights=1., is_signal=True),)


    samples_mc = samples_essential # + samples_WH
    samples = samples_essential + samples_data
    all_samples = samples_mc + samples_data

    # -> Can add cross sections for samples either explicitly, or from file, or from cfg
    #    (currently taken from htt_common)

    weighted_list = ['W', 'W1Jets', 'W2Jets', 'W3Jets', 'W4Jets']

    for sample in samples_mc:
        if sample.name not in weighted_list:
            setSumWeights(sample)

    # sampleDict = {s.name: s for s in all_samples}
    sampleDict = {}
    for s in all_samples:
        sampleDict[s.name] = s

    return samples_mc, samples_data, samples, all_samples, sampleDict

samples_mc, samples_data, samples, all_samples, sampleDict = createSampleLists()
