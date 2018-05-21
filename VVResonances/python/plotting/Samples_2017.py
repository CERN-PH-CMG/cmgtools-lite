import os
import ROOT
from ROOT import gSystem

from CMGTools.H2TauTau.proto.plotter.PlotConfigs import SampleCfg
from CMGTools.VVResonances.plotting.HistCreator import setSumWeights


from CMGTools.RootTools.samples.samples_13TeV_RunIIFall17MiniAOD import QCDHT, QCDPt, VJetsQQHT, TTHad_pow
from CMGTools.RootTools.samples.samples_13TeV_DATA2017 import *
from CMGTools.VVResonances.samples.signal_13TeV_94X_Fall17 import signalSamples
from CMGTools.VVResonances.samples.signal_13TeV_94X_Fall17_private import signalSamples_private


def createSampleLists(analysis_dir='samples/',
                      channel='VV', weight='', signalSample='',
                      vJetsKFac=1., qcdKFac=1.,
                      useQCDPt=False):

    # settings and code to reweight V+jets samples (EW and QCD NLO corrections)
    # the following two k-factors are from samples_13TeV_RunIISpring16MiniAODv2.py
    # if reweightVJets and reweightVJets2015:
    #     raise AssertionError
    # wJetsKFac = 1.21
    # dyJetsKFac = 1.23
    # wJetsQCDCorrections2015 = {}
    # dyJetsQCDCorrections2015 = {}
    # wJetsQCDCorrections = {}
    # dyJetsQCDCorrections = {}
    # # taken from http://cms.cern.ch/iCMS/jsp/db_notes/noteInfo.jsp?cmsnoteid=CMS%20AN-2015/186 (Table 4)
    # wJetsQCDCorrections2015["WJetsToLNu_HT100to200"] = 1.459/wJetsKFac
    # wJetsQCDCorrections2015["WJetsToLNu_HT200to400"] = 1.434/wJetsKFac
    # wJetsQCDCorrections2015["WJetsToLNu_HT400to600"] = 1.532/wJetsKFac
    # wJetsQCDCorrections2015["WJetsToLNu_HT600to800"] = 1.004/wJetsKFac
    # wJetsQCDCorrections2015["WJetsToLNu_HT800to1200"] = 1.004/wJetsKFac
    # wJetsQCDCorrections2015["WJetsToLNu_HT1200to2500"] = 1.004/wJetsKFac
    # wJetsQCDCorrections2015["WJetsToLNu_HT2500toInf"] = 1.004/wJetsKFac
    # dyJetsQCDCorrections2015["DYJetsToLL_M50_HT100to200"] = 1.588/dyJetsKFac
    # dyJetsQCDCorrections2015["DYJetsToLL_M50_HT200to400"] = 1.438/dyJetsKFac
    # dyJetsQCDCorrections2015["DYJetsToLL_M50_HT400to600"] = 1.494/dyJetsKFac
    # dyJetsQCDCorrections2015["DYJetsToLL_M50_HT600to800"] = 1.139/dyJetsKFac
    # dyJetsQCDCorrections2015["DYJetsToLL_M50_HT800to1200"] = 1.139/dyJetsKFac
    # dyJetsQCDCorrections2015["DYJetsToLL_M50_HT1200to2500"] = 1.139/dyJetsKFac
    # dyJetsQCDCorrections2015["DYJetsToLL_M50_HT2500toInf"] = 1.139/dyJetsKFac
    # # new for Summer16 W+jets (see https://github.com/jmhogan/GenHTweight)
    # wJetsQCDCorrections["WJetsToLNu_HT100to200"] = 0.998056
    # wJetsQCDCorrections["WJetsToLNu_HT200to400"] = 0.978569
    # wJetsQCDCorrections["WJetsToLNu_HT400to600"] = 0.928054
    # wJetsQCDCorrections["WJetsToLNu_HT600to800"] = 0.856705
    # wJetsQCDCorrections["WJetsToLNu_HT800to1200"] = 0.757463
    # wJetsQCDCorrections["WJetsToLNu_HT1200to2500"] = 0.608292
    # wJetsQCDCorrections["WJetsToLNu_HT2500toInf"] = 0.454246
    # dyJetsQCDCorrections["DYJetsToLL_M50_HT100to200"] = 1.007516
    # dyJetsQCDCorrections["DYJetsToLL_M50_HT200to400"] = 0.992853
    # dyJetsQCDCorrections["DYJetsToLL_M50_HT400to600"] = 0.974071
    # dyJetsQCDCorrections["DYJetsToLL_M50_HT600to800"] = 0.948367
    # dyJetsQCDCorrections["DYJetsToLL_M50_HT800to1200"] = 0.883340
    # dyJetsQCDCorrections["DYJetsToLL_M50_HT1200to2500"] = 0.749894
    # dyJetsQCDCorrections["DYJetsToLL_M50_HT2500toInf"] = 0.617254

    # explicit list of samples:
    wjetsSampleNames = ["WJetsToQQ_HT800toInf"]
    dyjetsSampleNames = ['ZJetsToQQ_HT800toInf']
    ttjetsSampleNames = ["TTHad_pow"]
    qcdSampleNames = ['QCD_HT100to200', 'QCD_HT200to300', 'QCD_HT300to500', 'QCD_HT500to700', 'QCD_HT700to1000', 'QCD_HT1000to1500', 'QCD_HT1500to2000', 'QCD_HT2000toInf']
    # vvSampleNames = ['WWTo1L1Nu2Q', 'WWTo1L1Nu2Q', 'WZTo1L1Nu2Q']
    # singleTopSampleNames = ['Ttch_powheg', 'TBar_tch_powheg', 'TToLeptons_sch', 'TBar_tWch', 'T_tWch']
    # topSamples = [TT_pow]
    # if useTopMcatnlo:
    #     topSamples = [TTJets]
    #     ttjetsSampleNames = ["TTJets"]
    # if useWJetsPt:
    #     wjetsSampleNames = ["WJetsToLNu_Pt_100To250", "WJetsToLNu_Pt_250To400", "WJetsToLNu_Pt_400To600", "WJetsToLNu_Pt_600ToInf"]

    jj_SampleNames = qcdSampleNames + wjetsSampleNames + dyjetsSampleNames + ttjetsSampleNames
    # cuts to split ttbar sample according to W decay
    # ttjetsWCut = '(lnujj_l2_mergedVTruth==1&&lnujj_l2_nearestBDRTruth>0.8)'
    # ttjetsNonWCut = '(!(lnujj_l2_mergedVTruth==1&&lnujj_l2_nearestBDRTruth>0.8))'
    # add ttbar pT reweighting
    # if reweightTop:
    #     ttjetsWCut += '*truth_genTop_weight'
    #     ttjetsNonWCut += '*truth_genTop_weight'

    tree_prod_name = ''

    # if (channel == "WV"):
    #     channelSampleNames = lnujj_SampleNames
    # else:
    channelSampleNames = jj_SampleNames
    samples_essential = []

    # if "/sVJetsReweighting_cc.so" not in gSystem.GetLibraries():
    #     ROOT.gROOT.ProcessLine(".L %s/src/CMGTools/VVResonances/python/plotting/VJetsReweighting.cc+" % os.environ['CMSSW_BASE'])
    # from ROOT import getDYWeight, getWWeight

    # add samples
    for sample in QCDHT + QCDPt + VJetsQQHT + [TTHad_pow]:
        vJetsWeight = "1."  # str(vJetsKFac)
        if sample.name in channelSampleNames:
            if sample.name in qcdSampleNames:
                vJetsWeight = str(qcdKFac)
            if sample.name in (wjetsSampleNames + dyjetsSampleNames):
                vJetsWeight = str(0.3)
            # if (sample in DYJetsM50HT) and reweightVJets:
            #     vJetsWeight = '{} * {}'.format(vJetsKFac, dyJetsQCDCorrections[sample.name])
            # elif (sample in WJetsToLNuHT) and reweightVJets:
            #     vJetsWeight = '{} * {}'.format(vJetsKFac, wJetsQCDCorrections[sample.name])
            # if (sample in DYJetsM50HT) and reweightVJets2015:
            #     vJetsWeight = 'getDYWeight(truth_genBoson_pt) * {} * {}'.format(vJetsKFac, dyJetsQCDCorrections2015[sample.name])
            # elif (sample in WJetsToLNuHT) and reweightVJets2015:
            #     vJetsWeight = 'getWWeight(truth_genBoson_pt) * {} * {}'.format(vJetsKFac, wJetsQCDCorrections2015[sample.name])
            samples_essential.append(
                SampleCfg(name=sample.name, dir_name=sample.name, ana_dir=analysis_dir, tree_prod_name=tree_prod_name,
                    xsec=sample.xSection, sumweights=sample.nGenEvents, weight_expr=('*'.join([weight, vJetsWeight]))))

    # # TTJets sample
    # for sample in topSamples:
    #     if sample.name in channelSampleNames:
    #         # print "Adding", sample.name, sample.xSection, sample.nGenEvents, weight
    #         samples_essential.append(
    #             SampleCfg(name=sample.name+'_W', dir_name=sample.name, ana_dir=analysis_dir, tree_prod_name=tree_prod_name,
    #                 xsec=sample.xSection, sumweights=sample.nGenEvents, weight_expr=('*'.join([weight, ttjetsWCut]))))
    #         samples_essential.append(
    #             SampleCfg(name=sample.name+'_nonW', dir_name=sample.name, ana_dir=analysis_dir, tree_prod_name=tree_prod_name,
    #                 xsec=sample.xSection, sumweights=sample.nGenEvents, weight_expr=('*'.join([weight, ttjetsNonWCut]))))

    # signal sample (set signal xsec to 5 pb)
    samples_signal = []
    if (signalSample):
        for sample in signalSamples:
            if sample.name == signalSample:
                samples_signal.append(
                    SampleCfg(name=sample.name, dir_name=sample.name, ana_dir=analysis_dir, tree_prod_name=tree_prod_name,
                        xsec=5., sumweights=sample.nGenEvents, weight_expr=('*'.join([weight])), is_signal=True))

    samples_data = []
    if channel == 'WV':
        samples_data = [
            SampleCfg(name='data_SingleMuon', dir_name='SingleMuon_Run2016B_17Nov2017', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, is_data=True),
            SampleCfg(name='data_SingleMuon', dir_name='SingleMuon_Run2016C_17Nov2017', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, is_data=True),
            SampleCfg(name='data_SingleMuon', dir_name='SingleMuon_Run2016D_17Nov2017', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, is_data=True),
            SampleCfg(name='data_SingleMuon', dir_name='SingleMuon_Run2016E_17Nov2017', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, is_data=True),
            SampleCfg(name='data_SingleMuon', dir_name='SingleMuon_Run2016F_17Nov2017', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, is_data=True),
            SampleCfg(name='data_SingleMuon', dir_name='SingleMuon_Run2016G_17Nov2017', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, is_data=True),
            SampleCfg(name='data_SingleMuon', dir_name='SingleMuon_Run2016H_17Nov2017', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, is_data=True),
            SampleCfg(name='data_SingleMuon', dir_name='SingleMuon_Run2016H_17Nov2017', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, is_data=True),
            SampleCfg(name='data_SingleElectron', dir_name='SingleElectron_Run2016B_17Nov2017', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, is_data=True),
            SampleCfg(name='data_SingleElectron', dir_name='SingleElectron_Run2016C_17Nov2017', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, is_data=True),
            SampleCfg(name='data_SingleElectron', dir_name='SingleElectron_Run2016D_17Nov2017', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, is_data=True),
            SampleCfg(name='data_SingleElectron', dir_name='SingleElectron_Run2016E_17Nov2017', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, is_data=True),
            SampleCfg(name='data_SingleElectron', dir_name='SingleElectron_Run2016F_17Nov2017', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, is_data=True),
            SampleCfg(name='data_SingleElectron', dir_name='SingleElectron_Run2016G_17Nov2017', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, is_data=True),
            SampleCfg(name='data_SingleElectron', dir_name='SingleElectron_Run2016H_17Nov2017', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, is_data=True),
            SampleCfg(name='data_SingleElectron', dir_name='SingleElectron_Run2016H_17Nov2017', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, is_data=True),
            SampleCfg(name='data_MET', dir_name='MET_Run2016B_17Nov2017', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, is_data=True),
            SampleCfg(name='data_MET', dir_name='MET_Run2016C_17Nov2017', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, is_data=True),
            SampleCfg(name='data_MET', dir_name='MET_Run2016D_17Nov2017', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, is_data=True),
            SampleCfg(name='data_MET', dir_name='MET_Run2016E_17Nov2017', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, is_data=True),
            SampleCfg(name='data_MET', dir_name='MET_Run2016F_17Nov2017', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, is_data=True),
            SampleCfg(name='data_MET', dir_name='MET_Run2016G_17Nov2017', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, is_data=True),
            SampleCfg(name='data_MET', dir_name='MET_Run2016H_17Nov2017', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, is_data=True),
            SampleCfg(name='data_MET', dir_name='MET_Run2016H_17Nov2017', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, is_data=True),
        ]
    else:
        samples_data = [
            SampleCfg(name='data_JetHT', dir_name='JetHT_Run2017B_17Nov2017', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, is_data=True),
            SampleCfg(name='data_JetHT', dir_name='JetHT_Run2017C_17Nov2017', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, is_data=True),
            SampleCfg(name='data_JetHT', dir_name='JetHT_Run2017D_17Nov2017', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, is_data=True),
            SampleCfg(name='data_JetHT', dir_name='JetHT_Run2017E_17Nov2017', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, is_data=True),
            SampleCfg(name='data_JetHT', dir_name='JetHT_Run2017F_17Nov2017', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, is_data=True),
        ]

    # samples_WH = []
    # mssm_names = ['HiggsSUSYBB80', 'HiggsSUSYBB90', 'HiggsSUSYBB100', 'HiggsSUSYBB110', 'HiggsSUSYBB120', 'HiggsSUSYBB130', 'HiggsSUSYBB140', 'HiggsSUSYBB160', 'HiggsSUSYBB180', 'HiggsSUSYBB200', 'HiggsSUSYBB250', 'HiggsSUSYBB300', 'HiggsSUSYBB350', 'HiggsSUSYBB400', 'HiggsSUSYBB450', 'HiggsSUSYBB500', 'HiggsSUSYBB600', 'HiggsSUSYBB700', 'HiggsSUSYBB900', 'HiggsSUSYBB1000', 'HiggsSUSYBB1200', 'HiggsSUSYBB1500', 'HiggsSUSYBB1600', 'HiggsSUSYBB1800', 'HiggsSUSYBB2000', 'HiggsSUSYBB2300', 'HiggsSUSYBB2600', 'HiggsSUSYBB2900', 'HiggsSUSYBB3200', 'HiggsSUSYGG80', 'HiggsSUSYGG90',
    #               'HiggsSUSYGG100', 'HiggsSUSYGG110', 'HiggsSUSYGG120', 'HiggsSUSYGG130', 'HiggsSUSYGG140', 'HiggsSUSYGG160', 'HiggsSUSYGG180', 'HiggsSUSYGG200', 'HiggsSUSYGG250', 'HiggsSUSYGG300', 'HiggsSUSYGG400', 'HiggsSUSYGG450', 'HiggsSUSYGG500', 'HiggsSUSYGG600', 'HiggsSUSYGG700', 'HiggsSUSYGG800', 'HiggsSUSYGG900', 'HiggsSUSYGG1000', 'HiggsSUSYGG1200', 'HiggsSUSYGG1400', 'HiggsSUSYGG1500', 'HiggsSUSYGG1600', 'HiggsSUSYGG1800', 'HiggsSUSYGG2000', 'HiggsSUSYGG2300', 'HiggsSUSYGG2600', 'HiggsSUSYGG2900', 'HiggsSUSYGG3200']  # HiggsSUSYBB800, HiggsSUSYBB1400, HiggsSUSYGG350
    # for name in mssm_names:
    #     samples_WH.append(SampleCfg(name=name.replace('HiggsSUSYBB', 'bbH').replace('HiggsSUSYGG', 'ggH'), dir_name=name,
    #                                   ana_dir=analysis_dir, tree_prod_name=tree_prod_name, xsec=1., sumweights=1., is_signal=True),)

    samples_mc = samples_essential + samples_signal
    samples = samples_essential + samples_data + samples_signal
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
