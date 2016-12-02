import os
import ROOT
from ROOT import gSystem, gROOT

from CMGTools.H2TauTau.proto.plotter.PlotConfigs import SampleCfg
from CMGTools.VVResonances.plotting.HistCreator import setSumWeights


from CMGTools.RootTools.samples.samples_13TeV_RunIISpring16MiniAODv2 import TTJets, SingleTop, WJetsToLNuHT, QCDHT, DYJetsM50HT, DiBosons, GJetsHT
# from CMGTools.RootTools.samples.samples_13TeV_RunIISpring16MiniAODv2 import TT_pow_ext3 as TT_pow_ext
from CMGTools.RootTools.samples.samples_13TeV_DATA2016 import *
# from CMGTools.VVAnalysis.samples.signal_13TeV_80X import signalSamples

def createSampleLists(analysis_dir='samples/',
                      channel='VV', weight=''):
    # explicit list of samples:
    wjetsSampleNames = ["WJetsToLNu_HT1200to2500", "WJetsToLNu_HT2500toInf", "WJetsToLNu_HT400to600", "WJetsToLNu_HT600to800", "WJetsToLNu_HT800to1200", 'WJetsToLNu_HT100to200', 'WJetsToLNu_HT200to400']
    ttjetsSampleNames = ["TTJets"]
    qcdSampleNames = ["QCD_HT1000to1500", "QCD_HT1500to2000", "QCD_HT2000toInf", "QCD_HT500to700", "QCD_HT700to1000"]
    vvSampleNames = ['WWTo1L1Nu2Q', 'WZTo1L1Nu2Q']
    singleTopSamplesNames = ['TToLeptons_tch_powheg', 'TBarToLeptons_tch_powheg', 'TToLeptons_sch', 'TBar_tWch', 'T_tWch']
    ttjetsWCut = '(lnujj_l2_mergedVTruth==1&&lnujj_l2_nearestBDRTruth>0.8)'
    ttjetsNonWCut = '(!(lnujj_l2_mergedVTruth==1&&lnujj_l2_nearestBDRTruth>0.8))'

    tree_prod_name = ''

    samples_essential = []
    # add QCD samples, but not those with _ext, since they are merged with the others
    for sample in QCDHT:
        continue
        # if not (sample.name.find("_ext") >= 0):
        if sample.name in qcdSampleNames:
            # print "Adding", sample.name, sample.xSection, sample.nGenEvents, weight
            samples_essential.append(
            SampleCfg(name=sample.name, dir_name=sample.name, ana_dir=analysis_dir, tree_prod_name=tree_prod_name,
                  xsec=sample.xSection, sumweights=sample.nGenEvents, weight_expr=weight))

    # TTJets sample
    sample = TTJets
    if sample.name in ttjetsSampleNames:
        # print "Adding", sample.name, sample.xSection, sample.nGenEvents, weight
        samples_essential.append(
            SampleCfg(name=sample.name+'_W', dir_name=sample.name, ana_dir=analysis_dir, tree_prod_name=tree_prod_name,
              xsec=sample.xSection, sumweights=sample.nGenEvents, weight_expr=('*'.join([weight, ttjetsWCut]))))
        samples_essential.append(
            SampleCfg(name=sample.name+'_nonW', dir_name=sample.name, ana_dir=analysis_dir, tree_prod_name=tree_prod_name,
                xsec=sample.xSection, sumweights=sample.nGenEvents, weight_expr=('*'.join([weight, ttjetsNonWCut]))))

    # DY+jets samples, but not those with _ext, since they are merged with the others
    for sample in DYJetsM50HT:
        continue
        if not (sample.name.find("_ext") >= 0):
            samples_essential.append(
            SampleCfg(name=sample.name, dir_name=sample.name, ana_dir=analysis_dir, tree_prod_name=tree_prod_name,
                  xsec=sample.xSection, sumweights=sample.nGenEvents, weight_expr=weight))

    # W+jets samples, but not those with _ext, since they are merged with the others
    for sample in WJetsToLNuHT:
        # if not (sample.name.find("_ext") >= 0):
        if sample.name in wjetsSampleNames:
            # print "Adding", sample.name, sample.xSection, sample.nGenEvents, weight
            samples_essential.append(
                SampleCfg(name=sample.name, dir_name=sample.name, ana_dir=analysis_dir, tree_prod_name=tree_prod_name,
                    xsec=sample.xSection, sumweights=sample.nGenEvents, weight_expr=weight))

    # DiBosons samples
    for sample in DiBosons:
        # if not ((sample.name.find("NuNu") >= 0) or (sample.name.find('WWToLNuQQ_ext') >= 0)):
        if sample.name in vvSampleNames:
            # print "Adding", sample.name
            samples_essential.append(
                SampleCfg(name=sample.name, dir_name=sample.name, ana_dir=analysis_dir, tree_prod_name=tree_prod_name,
                    xsec=sample.xSection, sumweights=sample.nGenEvents, weight_expr=weight))

    # SingleTop samples
    for sample.name in singleTopSamplesNames:
        continue
        # print "Adding", sample.name
        samples_essential.append(
        SampleCfg(name=sample.name, dir_name=sample.name, ana_dir=analysis_dir, tree_prod_name=tree_prod_name,
              xsec=sample.xSection, sumweights=sample.nGenEvents, weight_expr=weight))



    samples_data = []
    # if channel in ['VV']:
    samples_data = [
        # SampleCfg(name='data_JetHT', dir_name='JetHT_Run2016B_PromptReco_v2', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, is_data=True),
        # SampleCfg(name='data_JetHT', dir_name='JetHT_Run2016C_PromptReco_v2', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, is_data=True),
        # SampleCfg(name='data_JetHT', dir_name='JetHT_Run2016D_PromptReco_v2', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, is_data=True),
        SampleCfg(name='data_SingleMuon', dir_name='SingleMuon_Run2016B_PromptReco_v2', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, is_data=True),
        SampleCfg(name='data_SingleMuon', dir_name='SingleMuon_Run2016C_PromptReco_v2', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, is_data=True),
        SampleCfg(name='data_SingleMuon', dir_name='SingleMuon_Run2016D_PromptReco_v2', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, is_data=True),
        SampleCfg(name='data_SingleElectron', dir_name='SingleElectron_Run2016B_PromptReco_v2', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, is_data=True),
        SampleCfg(name='data_SingleElectron', dir_name='SingleElectron_Run2016C_PromptReco_v2', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, is_data=True),
        SampleCfg(name='data_SingleElectron', dir_name='SingleElectron_Run2016D_PromptReco_v2', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, is_data=True),
        SampleCfg(name='data_MET', dir_name='MET_Run2016B_PromptReco_v2', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, is_data=True),
        SampleCfg(name='data_MET', dir_name='MET_Run2016C_PromptReco_v2', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, is_data=True),
        SampleCfg(name='data_MET', dir_name='MET_Run2016D_PromptReco_v2', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, is_data=True),
    ]

    # samples_WH = []
    # mssm_names = ['HiggsSUSYBB80', 'HiggsSUSYBB90', 'HiggsSUSYBB100', 'HiggsSUSYBB110', 'HiggsSUSYBB120', 'HiggsSUSYBB130', 'HiggsSUSYBB140', 'HiggsSUSYBB160', 'HiggsSUSYBB180', 'HiggsSUSYBB200', 'HiggsSUSYBB250', 'HiggsSUSYBB300', 'HiggsSUSYBB350', 'HiggsSUSYBB400', 'HiggsSUSYBB450', 'HiggsSUSYBB500', 'HiggsSUSYBB600', 'HiggsSUSYBB700', 'HiggsSUSYBB900', 'HiggsSUSYBB1000', 'HiggsSUSYBB1200', 'HiggsSUSYBB1500', 'HiggsSUSYBB1600', 'HiggsSUSYBB1800', 'HiggsSUSYBB2000', 'HiggsSUSYBB2300', 'HiggsSUSYBB2600', 'HiggsSUSYBB2900', 'HiggsSUSYBB3200', 'HiggsSUSYGG80', 'HiggsSUSYGG90',
    #               'HiggsSUSYGG100', 'HiggsSUSYGG110', 'HiggsSUSYGG120', 'HiggsSUSYGG130', 'HiggsSUSYGG140', 'HiggsSUSYGG160', 'HiggsSUSYGG180', 'HiggsSUSYGG200', 'HiggsSUSYGG250', 'HiggsSUSYGG300', 'HiggsSUSYGG400', 'HiggsSUSYGG450', 'HiggsSUSYGG500', 'HiggsSUSYGG600', 'HiggsSUSYGG700', 'HiggsSUSYGG800', 'HiggsSUSYGG900', 'HiggsSUSYGG1000', 'HiggsSUSYGG1200', 'HiggsSUSYGG1400', 'HiggsSUSYGG1500', 'HiggsSUSYGG1600', 'HiggsSUSYGG1800', 'HiggsSUSYGG2000', 'HiggsSUSYGG2300', 'HiggsSUSYGG2600', 'HiggsSUSYGG2900', 'HiggsSUSYGG3200']  # HiggsSUSYBB800, HiggsSUSYBB1400, HiggsSUSYGG350
    # for name in mssm_names:
    #     samples_WH.append(SampleCfg(name=name.replace('HiggsSUSYBB', 'bbH').replace('HiggsSUSYGG', 'ggH'), dir_name=name,
    #                                   ana_dir=analysis_dir, tree_prod_name=tree_prod_name, xsec=1., sumweights=1., is_signal=True),)

    samples_mc = samples_essential  # + samples_WH
    samples = samples_essential + samples_data
    all_samples = samples_mc + samples_data

    # -> Can add cross sections for samples either explicitly, or from file, or from cfg
    #    (currently taken from htt_common)

    weighted_list = []

    for sample in samples_mc:
        if sample.name not in weighted_list:
            setSumWeights(sample)

    # sampleDict = {s.name: s for s in all_samples}
    sampleDict = {}
    for s in all_samples:
        sampleDict[s.name] = s

    return samples_mc, samples_data, samples, all_samples, sampleDict

samples_mc, samples_data, samples, all_samples, sampleDict = createSampleLists()
