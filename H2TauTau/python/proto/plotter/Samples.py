import os
import pickle

import ROOT
from ROOT import gSystem, gROOT

from CMGTools.H2TauTau.proto.plotter.PlotConfigs import SampleCfg, HistogramCfg
from CMGTools.H2TauTau.proto.samples.spring16.sms_xsec import get_xsec

from CMGTools.H2TauTau.proto.samples.summer16.htt_common import TT_pow, DYJetsToLL_M50_LO, DYJetsToLL_M50_LO_ext2, DYNJets, WJetsToLNu,  WNJets, WWTo2L2Nu, T_tWch, TBar_tWch, VVTo2L2Nu, ZZTo4L, WZTo1L3Nu, WWTo1L1Nu2Q, ZZTo2L2Q, WZTo2L2Q, WZTo1L1Nu2Q, TBar_tch_powheg, T_tch_powheg, HiggsGGH125, HiggsVBF125, mssm_signals, dy_weight_dict, w_weight_dict, data_tau

# WJetsToLNu_LO, TToLeptons_tch_amcatnlo, WZTo3LNu_amcatnlo, , WJetsToLNu_HT100to200, WJetsToLNu_HT200to400, WJetsToLNu_HT400to600, WJetsToLNu_HT600toInf, QCD_Mu15, DYJetsToTauTau_M150_LO, DYJetsToLL_M10to50_ext1

if "/sDYReweighting_cc.so" not in gSystem.GetLibraries(): 
    gROOT.ProcessLine(".L %s/src/CMGTools/H2TauTau/python/proto/plotter/DYReweighting.cc+" % os.environ['CMSSW_BASE']);
    from ROOT import getDYWeight

splitDY = True
useDYWeight = True
# data2016G = True

if useDYWeight or splitDY:
    dy_exps = []
    if splitDY:
        for njet in xrange(0, 5):
            weight = dy_weight_dict[njet]
            dy_exps.append('(geninfo_nup == {njet})*{weight}'.format(njet=njet, weight=weight))
            # dy_exps.append('(geninfo_nup == {njet} && (geninfo_invmass<150. || !(l2_gen_match==5 || l1_gen_lepfromtau)))*{weight}'.format(njet=njet, weight=weight))
            # weight = dy_weight_dict[(njet, 150)]
            # dy_exps.append('(geninfo_nup == {njet} && (geninfo_invmass>=150. && (l2_gen_match==5 || l1_gen_lepfromtau)))*{weight}'.format(njet=njet, weight=weight))
    # if useDYWeight:
    #     dy_exps.append('')
    dy_exp = '*({})'.format(' + '.join(dy_exps))
    if useDYWeight:
        dy_exp += '*getDYWeight(genboson_mass, genboson_pt)'
    print 'Using DY expression', dy_exp

w_exps = []
for njet in xrange(0, 5):
    weight = w_weight_dict[njet]
    w_exps.append('(geninfo_nup == {njet})*{weight}'.format(njet=njet, weight=weight))

w_exp = '({w})'.format(w=' + '.join(w_exps))


def createSampleLists(analysis_dir='/afs/cern.ch/user/s/steggema/work/public/mt/NewProd',
                      channel='mt',
                      mode='sm',
                      ztt_cut='(l2_gen_match == 5)', zl_cut='(l2_gen_match < 5)',
                      zj_cut='(l2_gen_match == 6)',
                      data2016G=False,
                      signal_scale=1.,
                      no_data=False):
    # -> Possibly from cfg like in the past, but may also make sense to enter directly
    if channel == 'mt':
        tree_prod_name = 'H2TauTauTreeProducerTauMu'
    elif channel == 'et':
        tree_prod_name = 'H2TauTauTreeProducerTauEle'
    elif channel == 'mm':
        tree_prod_name = 'H2TauTauTreeProducerMuMu'
    elif channel == 'tt':
        tree_prod_name = 'H2TauTauTreeProducerTauTau'
    elif channel == 'em':
        tree_prod_name = 'H2TauTauTreeProducerMuEle'
    elif channel == 'tau_fr':
        tree_prod_name = 'TauFRTreeProducer'

    samples_essential = [
        # SampleCfg(name='ZTTM10', dir_name='DYJetsToLL_M10to50', ana_dir=analysis_dir, tree_prod_name=tree_prod_name,
                      # xsec=DYJetsToLL_M10to50_ext1.xSection, sumweights=DYJetsToLL_M10to50_ext1.nGenEvents, weight_expr=ztt_cut),
        # SampleCfg(name='ZLM10', dir_name='DYJetsToLL_M10to50', ana_dir=analysis_dir, tree_prod_name=tree_prod_name,
                  # xsec=DYJetsToLL_M10to50_ext1.xSection, sumweights=DYJetsToLL_M10to50_ext1.nGenEvents, weight_expr=zl_cut),
        # SampleCfg(name='ZJM10', dir_name='DYJetsToLL_M10to50', ana_dir=analysis_dir, tree_prod_name=tree_prod_name,
                      # xsec=DYJetsToLL_M10to50_ext1.xSection, sumweights=DYJetsToLL_M10to50_ext1.nGenEvents, weight_expr=zj_cut),
    ]
    if splitDY:
        for sample in [DYJetsToLL_M50_LO_ext2, DYJetsToLL_M50_LO]:
            samples_essential += [
                SampleCfg(name='ZTT', dir_name=sample.name, ana_dir=analysis_dir, tree_prod_name=tree_prod_name, xsec=1., sumweights=1., weight_expr=ztt_cut+dy_exp),
                SampleCfg(name='ZL', dir_name=sample.name, ana_dir=analysis_dir, tree_prod_name=tree_prod_name,
                      xsec=1., sumweights=1., weight_expr=zl_cut+dy_exp),
                SampleCfg(name='ZJ', dir_name=sample.name, ana_dir=analysis_dir, tree_prod_name=tree_prod_name,
                          xsec=1., sumweights=1., weight_expr=zj_cut+dy_exp),
            ]
        
    else:
        samples_essential += [
            SampleCfg(name='ZTT', dir_name=DYJetsToLL_M50_LO_ext2.name, ana_dir=analysis_dir, tree_prod_name=tree_prod_name,
                      xsec=DYJetsToLL_M50_LO_ext2.xSection, sumweights=DYJetsToLL_M50_LO_ext2.nGenEvents, weight_expr=ztt_cut),
            SampleCfg(name='ZL', dir_name=DYJetsToLL_M50_LO_ext2.name, ana_dir=analysis_dir, tree_prod_name=tree_prod_name,
                      xsec=DYJetsToLL_M50_LO_ext2.xSection, sumweights=DYJetsToLL_M50_LO_ext2.nGenEvents, weight_expr=zl_cut),
            SampleCfg(name='ZJ', dir_name=DYJetsToLL_M50_LO_ext2.name, ana_dir=analysis_dir, tree_prod_name=tree_prod_name,
                      xsec=DYJetsToLL_M50_LO_ext2.xSection, sumweights=DYJetsToLL_M50_LO_ext2.nGenEvents, weight_expr=zj_cut),
            ]

    if channel == 'tt':
        samples_essential += [
            # SampleCfg(name='TTT', dir_name='TT_pow', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, xsec=TT_pow.xSection, sumweights=TT_pow.nGenEvents, weight_expr='l1_gen_match==5 && l2_gen_match==5'),
            # SampleCfg(name='TTJ', dir_name='TT_pow', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, xsec=TT_pow.xSection, sumweights=TT_pow.nGenEvents, weight_expr='!(l1_gen_match==5 && l2_gen_match==5)'),
            SampleCfg(name='TT', dir_name='TT_pow', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, xsec=TT_pow.xSection, sumweights=TT_pow.nGenEvents),
        ]
    else:
        samples_essential += [
            SampleCfg(name='TT', dir_name='TT_pow', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, xsec=TT_pow.xSection, sumweights=TT_pow.nGenEvents),
        ]

    samples_essential += [
            SampleCfg(name='T_tWch', dir_name='T_tWch_ext', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, xsec=T_tWch.xSection, sumweights=T_tWch.nGenEvents),
            SampleCfg(name='TBar_tWch', dir_name='TBar_tWch_ext', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, xsec=TBar_tWch.xSection, sumweights=TBar_tWch.nGenEvents),
            # SampleCfg(name='HiggsGGH125', dir_name='HiggsGGH125', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, xsec=HiggsGGH125.xSection, sumweights=HiggsGGH125.nGenEvents),
            # SampleCfg(name='HiggsVBF125', dir_name='HiggsVBF125', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, xsec=HiggsVBF125.xSection, sumweights=HiggsVBF125.nGenEvents),
            # SampleCfg(name='QCD', dir_name='QCD_Mu15', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, xsec=QCD_Mu15.xSection)
        ]

    if splitDY and channel not in ['mm', 'tau_fr']:
        for sample in DYNJets:
            n_jet_name = str(sample.name[sample.name.find('Jets')-1])+'Jets'
            samples_essential += [
                SampleCfg(name='ZTT'+n_jet_name, dir_name=sample.name, ana_dir=analysis_dir, tree_prod_name=tree_prod_name, xsec=1., sumweights=1., weight_expr=ztt_cut+dy_exp),
                SampleCfg(name='ZL'+n_jet_name, dir_name=sample.name, ana_dir=analysis_dir, tree_prod_name=tree_prod_name, xsec=1., sumweights=1., weight_expr=zl_cut+dy_exp),
                SampleCfg(name='ZJ'+n_jet_name, dir_name=sample.name, ana_dir=analysis_dir, tree_prod_name=tree_prod_name, xsec=1., sumweights=1., weight_expr=zj_cut+dy_exp),
            ]
    for sample in WNJets:
        n_jet_name = str(sample.name[sample.name.find('Jets')-1])+'Jets'
        # print 'WARNING - W - using n(gen events)', WJetsToLNu_LO.nevents[0], 'for W n(jets)', n_jet_name, 'xsec', sample.xSection
        samples_essential += [
            SampleCfg(name='W'+n_jet_name, dir_name=sample.name, ana_dir=analysis_dir, tree_prod_name=tree_prod_name, xsec=sample.xSection) #, sumweights=WJetsToLNu_LO.nevents[0]) #, weight_expr=w_exp)
            ]

    samples_data = []
    if data2016G and channel in ['mt', 'mm', 'tau_fr']:
         samples_data = [
            SampleCfg(name='data_obs', dir_name='SingleMuon_Run2016G_PromptReco_v1', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, is_data=True)
        ]
    elif channel in ['mt', 'mm', 'tau_fr']:
        samples_data = [
            SampleCfg(name='data_obs', dir_name='SingleMuon_Run2016B_PromptReco_v2', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, is_data=True),
            SampleCfg(name='data_obs', dir_name='SingleMuon_Run2016C_PromptReco_v2', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, is_data=True),
            SampleCfg(name='data_obs', dir_name='SingleMuon_Run2016D_PromptReco_v2', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, is_data=True),
        ]
    elif channel in ['et']:
        samples_data = [
            SampleCfg(name='data_obs', dir_name='SingleElectron_Run2016B_PromptReco_v2', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, is_data=True),
        ]
    elif channel in ['tt']:
        samples_data = [
            SampleCfg(name='data_obs', dir_name=mc_comp.name, ana_dir=analysis_dir, tree_prod_name=tree_prod_name, is_data=True) for mc_comp in data_tau
        ]
    elif channel in ['em']:
        samples_data = [
            SampleCfg(name='data_obs', dir_name='MuonEG_Run2016B_PromptReco_v2', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, is_data=True),
            SampleCfg(name='data_obs', dir_name='MuonEG_Run2016C_PromptReco_v2', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, is_data=True),
            SampleCfg(name='data_obs', dir_name='MuonEG_Run2016D_PromptReco_v2', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, is_data=True),
        ]

    if no_data:
        samples_data = []

    samples_additional = [
        SampleCfg(name='TToLeptons_tch_powheg', dir_name=T_tch_powheg.name, ana_dir=analysis_dir, tree_prod_name=tree_prod_name, xsec=T_tch_powheg.xSection, sumweights=T_tch_powheg.nGenEvents),
        SampleCfg(name='TBarToLeptons_tch_powheg', dir_name=TBar_tch_powheg.name, ana_dir=analysis_dir, tree_prod_name=tree_prod_name, xsec=TBar_tch_powheg.xSection, sumweights=TBar_tch_powheg.nGenEvents),
    ]

    samples_additional += [
        SampleCfg(name='ZZTo4L', dir_name='ZZTo4L', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, xsec=ZZTo4L.xSection, sumweights=ZZTo4L.nGenEvents),
        SampleCfg(name='ZZTo2L2Q', dir_name='ZZTo2L2Q', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, xsec=ZZTo2L2Q.xSection, sumweights=ZZTo2L2Q.nGenEvents),
        # SampleCfg(name='WZTo3L', dir_name='WZTo3LNu_amcatnlo', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, xsec=WZTo3LNu_amcatnlo.xSection, sumweights=WZTo3LNu_amcatnlo.nGenEvents),
        SampleCfg(name='WZTo2L2Q', dir_name='WZTo2L2Q', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, xsec=WZTo2L2Q.xSection, sumweights=WZTo2L2Q.nGenEvents),
        SampleCfg(name='WZTo1L3Nu', dir_name='WZTo1L3Nu', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, xsec=WZTo1L3Nu.xSection, sumweights=WZTo1L3Nu.nGenEvents),
        SampleCfg(name='WZTo1L1Nu2Q', dir_name='WZTo1L1Nu2Q', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, xsec=WZTo1L1Nu2Q.xSection, sumweights=WZTo1L1Nu2Q.nGenEvents),
        SampleCfg(name='VVTo2L2Nu', dir_name='VVTo2L2Nu', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, xsec=VVTo2L2Nu.xSection, sumweights=VVTo2L2Nu.nGenEvents),
        SampleCfg(name='WWTo1L1Nu2Q', dir_name='WWTo1L1Nu2Q', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, xsec=WWTo1L1Nu2Q.xSection, sumweights=WWTo1L1Nu2Q.nGenEvents),
    ]

    samples_sm = [
        SampleCfg(name='HiggsGGH125', dir_name='HiggsGGH125', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, xsec=HiggsGGH125.xSection, sumweights=HiggsGGH125.nGenEvents, is_signal=True),
        SampleCfg(name='HiggsVBF125', dir_name='HiggsVBF125', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, xsec=HiggsVBF125.xSection, sumweights=HiggsVBF125.nGenEvents, is_signal=True),
    ]

    samples_mssm = []
    # '80', '90',
    masses_bbh = [ '100', '110', '120', '130', '140', '160', '180', '200', '250',  '350', '400', '450',  '500', '600', '700', '800', '900', '1000',  '1400', '1600', '1800', '2000', '2300', '2900', '3200']
    # '80', '90',
    masses_ggh = ['100', '110', '120', '130', '160', '180', '200', '250', '350', '400', '450', '500', '600', '700', '800',  '1000', '1200', '1400', '1800', '2000', '2300', '2600', '2900', '3200']

    # mssm_names = ['HiggsSUSYBB80', 'HiggsSUSYBB90', 'HiggsSUSYBB100', 'HiggsSUSYBB110', 'HiggsSUSYBB120', 'HiggsSUSYBB130', 'HiggsSUSYBB140', 'HiggsSUSYBB160', 'HiggsSUSYBB180', 'HiggsSUSYBB200', 'HiggsSUSYBB250',  'HiggsSUSYBB350', 'HiggsSUSYBB400', 'HiggsSUSYBB450', 'HiggsSUSYBB500', 'HiggsSUSYBB600', 'HiggsSUSYBB700', 'HiggsSUSYBB800', 'HiggsSUSYBB900', 'HiggsSUSYBB1000',  'HiggsSUSYBB1400', 'HiggsSUSYBB1500', 'HiggsSUSYBB1600', 'HiggsSUSYBB1800', 'HiggsSUSYBB2000', 'HiggsSUSYBB2300', 'HiggsSUSYBB2900', 'HiggsSUSYBB3200', 'HiggsSUSYGG80', 'HiggsSUSYGG90',
    #               'HiggsSUSYGG100', 'HiggsSUSYGG110', 'HiggsSUSYGG120', 'HiggsSUSYGG130', 'HiggsSUSYGG160', 'HiggsSUSYGG180', 'HiggsSUSYGG200', 'HiggsSUSYGG250', 'HiggsSUSYGG300', 'HiggsSUSYGG350', 'HiggsSUSYGG400', 'HiggsSUSYGG450', 'HiggsSUSYGG500', 'HiggsSUSYGG600', 'HiggsSUSYGG700', 'HiggsSUSYGG800',  'HiggsSUSYGG1000', 'HiggsSUSYGG1200', 'HiggsSUSYGG1400', 'HiggsSUSYGG1500',  'HiggsSUSYGG1800', 'HiggsSUSYGG2000', 'HiggsSUSYGG2300', 'HiggsSUSYGG2600', 'HiggsSUSYGG2900', 'HiggsSUSYGG3200']  # 'HiggsSUSYBB300','HiggsSUSYBB1200', 'HiggsSUSYBB2600', 'HiggsSUSYGG140', 'HiggsSUSYGG900','HiggsSUSYGG1600',
    # # mssm_names = ['HiggsSUSYGG160', 'HiggsSUSYGG500', 'HiggsSUSYGG1000',
    # #               'HiggsSUSYBB160', 'HiggsSUSYBB500', 'HiggsSUSYBB1000',]

    limits_ichep_ggh = {'2900': 0.0064239501953125, '450': 0.12127685546875, '700': 0.0381317138671875, '130': 10.5439453125, '110': 21.0205078125, '250': 0.79638671875, '2300': 0.007214355282485485, '180': 2.4345703125, '400': 0.17047119140625, '1400': 0.010340881533920765, '500': 0.089935302734375, '200': 1.708984375, '140': 7.3095703125, '120': 15.7705078125, '100': 24.57275390625, '160': 3.9550781249999996, '900': 0.02440795861184597, '1800': 0.008679199032485485, '1600': 0.009762573055922985, '3200': 0.0063995360396802425, '2000': 0.008056640625, '350': 0.2442626953125, '800': 0.0279693603515625, '1000': 0.01924438402056694, '1200':0.013682556338608265, '2600':0.0067382813431322575}

    limits_ichep_ggh['300'] = 0.5
    limits_ichep_ggh['600'] = 0.06
    limits_ichep_ggh['1500'] = 0.01

    limits_ichep_bbh = {'2900': 0.005267334170639515, '450': 0.069732666015625, '700': 0.030960083007812497, '130': 4.880859375, '110': 10.3125, '250': 0.3885498046875, '2300': 0.0059265135787427425, '180': 1.17919921875, '400': 0.095672607421875, '1400': 0.01087188720703125, '500': 0.0551605224609375, '200': 0.80517578125, '140': 3.818359375, '120': 6.77490234375, '100': 15.25390625, '160': 1.8818359375, '900': 0.02145080640912056, '1800': 0.007534789852797985, '1600': 0.00846252404153347, '3200': 0.0050369263626635075, '2000': 0.0066925049759447575, '350': 0.13861083984375, '800': 0.025848388671875, '1000': 0.01756439171731472}

    limits_ichep_bbh['600'] = 0.045
    limits_ichep_bbh['1500'] = 0.0095


    for mass in masses_bbh:
        samples_mssm.append(SampleCfg(name='bbH'+mass, dir_name='HiggsSUSYBB'+mass, ana_dir=analysis_dir, tree_prod_name=tree_prod_name, xsec=limits_ichep_bbh[mass], sumweights=1., is_signal=True))

    for mass in masses_ggh:
        if mass not in limits_ichep_ggh: import pdb; pdb.set_trace()
        samples_mssm.append(SampleCfg(name='ggH'+mass, dir_name='HiggsSUSYGG'+mass, ana_dir=analysis_dir, tree_prod_name=tree_prod_name, xsec=limits_ichep_ggh[mass], sumweights=1., is_signal=True))

    # for name in mssm_names:
    #     samples_mssm.append(SampleCfg(name=name.replace('HiggsSUSYBB', 'bbH').replace('HiggsSUSYGG', 'ggH'), dir_name=name,
    #                                   ana_dir=analysis_dir, tree_prod_name=tree_prod_name, xsec=1., sumweights=1., is_signal=True),)
        
        # SampleCfg(name='HiggsSUSYGG200', dir_name='HiggsSUSYGG200', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, xsec=100., sumweights=1., is_signal=True),
        # SampleCfg(name='HiggsSUSYGG500', dir_name='HiggsSUSYGG500', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, xsec=100., sumweights=1., is_signal=True),
        # SampleCfg(name='HiggsSUSYGG1000', dir_name='HiggsSUSYGG1000', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, xsec=100., sumweights=1., is_signal=True),
        # SampleCfg(name='HiggsSUSYGG1500', dir_name='HiggsSUSYGG1500', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, xsec=100., sumweights=1., is_signal=True),
    # ]

    samples_susy = []
    if mode == 'susy':
        
        # normfile = ROOT.TFile(' /afs/cern.ch/work/s/steggema/public/tt/100417/SMS_TChipmStauSnu/ttHhistoCounterAnalyzer/sumhist.root')
        normfile = ROOT.TFile(' /afs/cern.ch/work/s/steggema/public/tt/270617/sms_sys/SMS_TChipmStauSnu//H2TauTauTreeProducerTauTau/tree.root')
        normhist = normfile.Get('SumGenWeightsSMS')

        from CMGTools.H2TauTau.proto.plotter.categories_TauTau import inc_trigger
        def createSusySampleCfg(m_stau=150, m_chi0=1):

            sname = 'SMS_TChipmStauSnu'
            print "setting sum of weights to", normhist.GetBinContent(m_stau+1, m_chi0+1, 1), 'for', sname+'MStau{m_stau}MChi{m_chi0}'.format(m_stau=m_stau, m_chi0=m_chi0)
            return SampleCfg(name=sname+'MStau{m_stau}MChi{m_chi0}'.format(m_stau=m_stau, m_chi0=m_chi0), dir_name=sname, ana_dir=analysis_dir, tree_prod_name=tree_prod_name, xsec=get_xsec(m_stau), sumweights=normhist.GetBinContent(m_stau+1, m_chi0+1, 1), is_signal=True, weight_expr='(GenSusyMChargino=={m_stau}. && GenSusyMNeutralino=={m_chi0})'.format(m_stau=m_stau, m_chi0=m_chi0),
                cut_replace_func=lambda s : s.replace(inc_trigger.cutstr, '1.'))

        # # the following is good for staus
        # samples_susy.append(createSusySampleCfg(100, 1))
        # samples_susy.append(createSusySampleCfg(200, 1))
        # samples_susy.append(createSusySampleCfg(150, 1))
        # samples_susy.append(createSusySampleCfg(150, 10))
        # samples_susy.append(createSusySampleCfg(150, 20))
        # samples_susy.append(createSusySampleCfg(150, 50))
        # samples_susy.append(createSusySampleCfg(150, 100))

        # samples_susy.append(createSusySampleCfg(100, 1))
        # samples_susy.append(createSusySampleCfg(200, 1))
        # samples_susy.append(createSusySampleCfg(150, 1))
        samples_susy.append(createSusySampleCfg(150, 25))
        samples_susy.append(createSusySampleCfg(300, 100))
        samples_susy.append(createSusySampleCfg(500, 1))
        samples_susy.append(createSusySampleCfg(600, 1))

    if mode in ['sm', 'mva']:
        samples_additional += samples_sm
    if mode == 'mssm':
        samples_additional += samples_mssm
    if mode == 'susy':
        samples_additional += samples_susy

    samples_mc = samples_essential + samples_additional 

    samples = samples_essential + samples_additional + samples_data
    all_samples = samples_mc + samples_data

    # -> Can add cross sections for samples either explicitly, or from file, or from cfg
    #    (currently taken from htt_common)

    # weighted_list = ['W', 'W1Jets', 'W2Jets', 'W3Jets', 'W4Jets']
    weighted_list = []
    weighted_list += [s.name for s in samples_susy]
    if splitDY:
        weighted_list += ['ZTT', 'ZTT1Jets', 'ZTT2Jets', 'ZTT3Jets', 'ZTT4Jets',
                          'ZJ', 'ZJ1Jets', 'ZJ2Jets', 'ZJ3Jets', 'ZJ4Jets',
                          'ZL', 'ZL1Jets', 'ZL2Jets', 'ZL3Jets', 'ZL4Jets',
                          'ZTTM150', 'ZJM150', 'ZLM150']

    for sample in samples_mc:
        if sample.name not in weighted_list:
            setSumWeights(sample, 'MCWeighter' if channel not in ['tau_fr'] else 'SkimAnalyzerCount')
            print 'Set sum weights for sample', sample.name, 'to', sample.sumweights

    # sampleDict = {s.name: s for s in all_samples}
    sampleDict = {}
    for s in all_samples:
        sampleDict[s.name] = s

    for sample in all_samples:
        if sample.is_signal:
            sample.scale = sample.scale * signal_scale

    return samples_mc, samples_data, samples, all_samples, sampleDict


def setSumWeights(sample, weight_dir='MCWeighter'):
    if isinstance(sample, HistogramCfg) or sample.is_data:
        return

    pckfile = '/'.join([sample.ana_dir, sample.dir_name, weight_dir, 'SkimReport.pck'])
    try:
        pckobj = pickle.load(open(pckfile, 'r'))
        counters = dict(pckobj)
        if 'Sum Weights' in counters:
            sample.sumweights = counters['Sum Weights']
    except IOError:
        # print 'Warning: could not find sum weights information for sample', sample.name
        pass
