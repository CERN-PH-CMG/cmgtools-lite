import os
import ROOT
from ROOT import gSystem, gROOT

from CMGTools.H2TauTau.proto.plotter.PlotConfigs import SampleCfg
from CMGTools.H2TauTau.proto.plotter.HistCreator import setSumWeights
from CMGTools.H2TauTau.proto.samples.spring16.sms_xsec import get_xsec

from CMGTools.H2TauTau.proto.samples.spring16.htt_common import TT_pow_ext, DYJetsToLL_M50_LO, DYNJets, WJetsToLNu,  WNJets, WWTo2L2Nu, T_tWch, TBar_tWch, VVTo2L2Nu, ZZTo4L, WZTo1L3Nu, WWTo1L1Nu2Q, ZZTo2L2Q, WZTo2L2Q, WZTo1L1Nu2Q, TBarToLeptons_tch_powheg, TToLeptons_tch_powheg, mssm_signals, dy_weight_dict, w_weight_dict

# WJetsToLNu_LO, TToLeptons_tch_amcatnlo, WZTo3LNu_amcatnlo, , WJetsToLNu_HT100to200, WJetsToLNu_HT200to400, WJetsToLNu_HT400to600, WJetsToLNu_HT600toInf, QCD_Mu15, DYJetsToTauTau_M150_LO, DYJetsToLL_M10to50_ext1

if "/sDYReweighting_cc.so" not in gSystem.GetLibraries(): 
    gROOT.ProcessLine(".L %s/src/CMGTools/H2TauTau/python/proto/plotter/DYReweighting.cc+" % os.environ['CMSSW_BASE']);
    from ROOT import getDYWeight

splitDY = False
useDYWeight = False
# data2016G = True

if useDYWeight:
    dy_exps = []
    for njet in xrange(0, 5):
        weight = dy_weight_dict[(njet, 0)]
        dy_exps.append('(geninfo_nup == {njet})*{weight}'.format(njet=njet, weight=weight))
        # dy_exps.append('(geninfo_nup == {njet} && (geninfo_invmass<150. || !(l2_gen_match==5 || l1_gen_lepfromtau)))*{weight}'.format(njet=njet, weight=weight))
        # weight = dy_weight_dict[(njet, 150)]
        # dy_exps.append('(geninfo_nup == {njet} && (geninfo_invmass>=150. && (l2_gen_match==5 || l1_gen_lepfromtau)))*{weight}'.format(njet=njet, weight=weight))

    dy_exp = '*({})'.format(' + '.join(dy_exps))

w_exps = []
for njet in xrange(0, 5):
    weight = w_weight_dict[njet]
    w_exps.append('(geninfo_nup == {njet})*{weight}'.format(njet=njet, weight=weight))

w_exp = '({w})'.format(w=' + '.join(w_exps))


def createSampleLists(analysis_dir='/afs/cern.ch/user/s/steggema/work/public/mt/NewProd',
                      channel='mt',
                      mode='sm',
                      ztt_cut='(l2_gen_match == 5)*getDYWeight(genboson_mass, genboson_pt)', zl_cut='(l2_gen_match < 5)*getDYWeight(genboson_mass, genboson_pt)',
                      zj_cut='(l2_gen_match == 6)*getDYWeight(genboson_mass, genboson_pt)',
                      data2016G=False,
                      signal_scale=1.):
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

    DYJetsToLL_M50_LO.nGenEvents = 1000.
    # WJetsToLNu_LO.nGenEvents = 1000.

    samples_essential = [
        # SampleCfg(name='ZTTM10', dir_name='DYJetsToLL_M10to50', ana_dir=analysis_dir, tree_prod_name=tree_prod_name,
                      # xsec=DYJetsToLL_M10to50_ext1.xSection, sumweights=DYJetsToLL_M10to50_ext1.nGenEvents, weight_expr=ztt_cut),
        # SampleCfg(name='ZLM10', dir_name='DYJetsToLL_M10to50', ana_dir=analysis_dir, tree_prod_name=tree_prod_name,
                  # xsec=DYJetsToLL_M10to50_ext1.xSection, sumweights=DYJetsToLL_M10to50_ext1.nGenEvents, weight_expr=zl_cut),
        # SampleCfg(name='ZJM10', dir_name='DYJetsToLL_M10to50', ana_dir=analysis_dir, tree_prod_name=tree_prod_name,
                      # xsec=DYJetsToLL_M10to50_ext1.xSection, sumweights=DYJetsToLL_M10to50_ext1.nGenEvents, weight_expr=zj_cut),
    ]
    if useDYWeight:
        samples_essential += [
            SampleCfg(name='ZTT', dir_name='DYJetsToLL_M50_LO', ana_dir=analysis_dir, tree_prod_name=tree_prod_name,
                      xsec=DYJetsToLL_M50_LO.xSection, sumweights=DYJetsToLL_M50_LO.nGenEvents, weight_expr=ztt_cut+dy_exp),
            SampleCfg(name='ZL', dir_name='DYJetsToLL_M50_LO', ana_dir=analysis_dir, tree_prod_name=tree_prod_name,
                      xsec=DYJetsToLL_M50_LO.xSection, sumweights=DYJetsToLL_M50_LO.nGenEvents, weight_expr=zl_cut+dy_exp),
            SampleCfg(name='ZJ', dir_name='DYJetsToLL_M50_LO', ana_dir=analysis_dir, tree_prod_name=tree_prod_name,
                      xsec=DYJetsToLL_M50_LO.xSection, sumweights=DYJetsToLL_M50_LO.nGenEvents, weight_expr=zj_cut+dy_exp),
            
        ]
    else:
        if not splitDY:
            samples_essential += [
                SampleCfg(name='ZTT', dir_name='DYJetsToLL_M50_LO', ana_dir=analysis_dir, tree_prod_name=tree_prod_name,
                          xsec=DYJetsToLL_M50_LO.xSection, sumweights=DYJetsToLL_M50_LO.nGenEvents, weight_expr=ztt_cut),
                SampleCfg(name='ZL', dir_name='DYJetsToLL_M50_LO', ana_dir=analysis_dir, tree_prod_name=tree_prod_name,
                          xsec=DYJetsToLL_M50_LO.xSection, sumweights=DYJetsToLL_M50_LO.nGenEvents, weight_expr=zl_cut),
                SampleCfg(name='ZJ', dir_name='DYJetsToLL_M50_LO', ana_dir=analysis_dir, tree_prod_name=tree_prod_name,
                          xsec=DYJetsToLL_M50_LO.xSection, sumweights=DYJetsToLL_M50_LO.nGenEvents, weight_expr=zj_cut),
            ]
        else:
            samples_essential += [
                SampleCfg(name='ZTT', dir_name='DYJetsToLL_M50_LO', ana_dir=analysis_dir, tree_prod_name=tree_prod_name,
                          xsec=DYJetsToLL_M50_LO.xSection, sumweights=DYJetsToLL_M50_LO.nGenEvents, weight_expr=ztt_cut),
                SampleCfg(name='Zl0jet', dir_name='DYJetsToLL_M50_LO', ana_dir=analysis_dir, tree_prod_name=tree_prod_name,
                          xsec=DYJetsToLL_M50_LO.xSection, sumweights=DYJetsToLL_M50_LO.nGenEvents, weight_expr='('+zl_cut+'*(jet1_genjet_pt<8.))'),
                SampleCfg(name='Zl1jet', dir_name='DYJetsToLL_M50_LO', ana_dir=analysis_dir, tree_prod_name=tree_prod_name,
                          xsec=DYJetsToLL_M50_LO.xSection, sumweights=DYJetsToLL_M50_LO.nGenEvents, weight_expr='('+zl_cut+'*(jet1_genjet_pt>8. && jet2_genjet_pt<8.))'),
                SampleCfg(name='Zl2jet', dir_name='DYJetsToLL_M50_LO', ana_dir=analysis_dir, tree_prod_name=tree_prod_name,
                          xsec=DYJetsToLL_M50_LO.xSection, sumweights=DYJetsToLL_M50_LO.nGenEvents, weight_expr='('+zl_cut+'*(jet1_genjet_pt>8. && jet2_genjet_pt>8.))'),
                SampleCfg(name='ZJ', dir_name='DYJetsToLL_M50_LO', ana_dir=analysis_dir, tree_prod_name=tree_prod_name,
                          xsec=DYJetsToLL_M50_LO.xSection, sumweights=DYJetsToLL_M50_LO.nGenEvents, weight_expr=zj_cut),
            ]
        # SampleCfg(name='ZTTM150', dir_name='DYJetsToTauTau_M150_LO', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, xsec=DYJetsToLL_M50_LO.xSection, sumweights=DYJetsToLL_M50_LO.nGenEvents, weight_expr=ztt_cut+dy_exp),
        # SampleCfg(name='ZLM150', dir_name='DYJetsToTauTau_M150_LO', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, xsec=DYJetsToLL_M50_LO.xSection, sumweights=DYJetsToLL_M50_LO.nGenEvents, weight_expr=zl_cut+dy_exp),
        # SampleCfg(name='ZJM150', dir_name='DYJetsToTauTau_M150_LO', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, xsec=DYJetsToLL_M50_LO.xSection, sumweights=DYJetsToLL_M50_LO.nGenEvents, weight_expr=zj_cut+dy_exp),
    samples_essential += [
        # SampleCfg(name='W', dir_name='WJetsToLNu_LO' if channel != 'mm' else 'WJetsToLNu', ana_dir=analysis_dir, tree_prod_name=tree_prod_name,
        #           xsec=WJetsToLNu_LO.xSection, sumweights=WJetsToLNu_LO.nGenEvents, weight_expr=w_exp if channel != 'tau_fr' else '(geninfo_htgen<100.)'),
        SampleCfg(name='TT', dir_name='TT_pow_ext3', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, xsec=TT_pow_ext.xSection, sumweights=TT_pow_ext.nGenEvents),
        SampleCfg(name='T_tWch', dir_name='T_tWch', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, xsec=T_tWch.xSection, sumweights=T_tWch.nGenEvents),
        SampleCfg(name='TBar_tWch', dir_name='TBar_tWch', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, xsec=TBar_tWch.xSection, sumweights=TBar_tWch.nGenEvents),
        # SampleCfg(name='HiggsGGH125', dir_name='HiggsGGH125', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, xsec=HiggsGGH125.xSection, sumweights=HiggsGGH125.nGenEvents),
        # SampleCfg(name='HiggsVBF125', dir_name='HiggsVBF125', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, xsec=HiggsVBF125.xSection, sumweights=HiggsVBF125.nGenEvents),
        # SampleCfg(name='QCD', dir_name='QCD_Mu15', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, xsec=QCD_Mu15.xSection)
    ]

    if channel in ['tau_fr']:
        k_factor = '1.'
        samples_essential += [
            # SampleCfg(name='WJetsToLNu_HT100to200', dir_name='WJetsToLNu_HT100to200', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, xsec=WJetsToLNu_HT100to200.xSection, sumweights=WJetsToLNu_HT100to200.nGenEvents, weight_expr=k_factor),
            # SampleCfg(name='WJetsToLNu_HT200to400', dir_name='WJetsToLNu_HT200to400', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, xsec=WJetsToLNu_HT200to400.xSection, sumweights=WJetsToLNu_HT200to400.nGenEvents, weight_expr=k_factor),
            # SampleCfg(name='WJetsToLNu_HT400to600', dir_name='WJetsToLNu_HT400to600', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, xsec=WJetsToLNu_HT400to600.xSection, sumweights=WJetsToLNu_HT400to600.nGenEvents, weight_expr=k_factor),
            # SampleCfg(name='WJetsToLNu_HT600toInf', dir_name='WJetsToLNu_HT600toInf', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, xsec=WJetsToLNu_HT600toInf.xSection, sumweights=WJetsToLNu_HT600toInf.nGenEvents, weight_expr=k_factor),
        ]

    if useDYWeight and channel not in ['mm', 'tau_fr']:
        for sample in DYNJets:
            n_jet_name = str(sample.name[sample.name.find('Jets')-1])+'Jets'
            print 'WARNING - DY - using n(gen events)', DYJetsToLL_M50_LO.nevents[0], 'for DY', n_jet_name
            samples_essential += [
                SampleCfg(name='ZTT'+n_jet_name, dir_name=sample.name, ana_dir=analysis_dir, tree_prod_name=tree_prod_name, xsec=sample.xSection, sumweights=DYJetsToLL_M50_LO.nevents[0], weight_expr=ztt_cut+dy_exp),
                SampleCfg(name='ZL'+n_jet_name, dir_name=sample.name, ana_dir=analysis_dir, tree_prod_name=tree_prod_name, xsec=sample.xSection, sumweights=DYJetsToLL_M50_LO.nevents[0], weight_expr=zl_cut+dy_exp),
                SampleCfg(name='ZJ'+n_jet_name, dir_name=sample.name, ana_dir=analysis_dir, tree_prod_name=tree_prod_name, xsec=sample.xSection, sumweights=DYJetsToLL_M50_LO.nevents[0], weight_expr=zj_cut+dy_exp),
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
            SampleCfg(name='data_obs', dir_name='Tau_Run2016B_PromptReco_v2', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, is_data=True),
            SampleCfg(name='data_obs', dir_name='Tau_Run2016C_PromptReco_v2', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, is_data=True),
            SampleCfg(name='data_obs', dir_name='Tau_Run2016D_PromptReco_v2', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, is_data=True),
        ]
    elif channel in ['em']:
        samples_data = [
            SampleCfg(name='data_obs', dir_name='MuonEG_Run2016B_PromptReco_v2', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, is_data=True),
            SampleCfg(name='data_obs', dir_name='MuonEG_Run2016C_PromptReco_v2', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, is_data=True),
            SampleCfg(name='data_obs', dir_name='MuonEG_Run2016D_PromptReco_v2', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, is_data=True),
        ]

    samples_additional = [
        # SampleCfg(name='TToLeptons_tch', dir_name='TToLeptons_tch_amcatnlo', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, xsec=TToLeptons_tch_amcatnlo.xSection, sumweights=TToLeptons_tch_amcatnlo.nGenEvents),
        SampleCfg(name='TToLeptons_tch_powheg', dir_name='TToLeptons_tch_powheg', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, xsec=TToLeptons_tch_powheg.xSection, sumweights=TToLeptons_tch_powheg.nGenEvents),
        SampleCfg(name='TBarToLeptons_tch_powheg', dir_name='TBarToLeptons_tch_powheg', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, xsec=TBarToLeptons_tch_powheg.xSection, sumweights=TBarToLeptons_tch_powheg.nGenEvents),
        # SampleCfg(name='TToLeptons_tch_powheg', dir_name='TToLeptons_tch_powheg', ana_dir=analysis_dir,
        #           tree_prod_name=tree_prod_name, xsec=TToLeptons_tch_powheg.xSection, sumweights=TToLeptons_tch_powheg.nGenEvents),
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

    samples_mssm = []
    # mssm_names = ['HiggsSUSYBB80', 'HiggsSUSYBB90', 'HiggsSUSYBB100', 'HiggsSUSYBB110', 'HiggsSUSYBB120', 'HiggsSUSYBB130', 'HiggsSUSYBB140', 'HiggsSUSYBB160', 'HiggsSUSYBB180', 'HiggsSUSYBB200', 'HiggsSUSYBB250', 'HiggsSUSYBB300', 'HiggsSUSYBB350', 'HiggsSUSYBB400', 'HiggsSUSYBB450', 'HiggsSUSYBB500', 'HiggsSUSYBB600', 'HiggsSUSYBB700', 'HiggsSUSYBB900', 'HiggsSUSYBB1000', 'HiggsSUSYBB1200', 'HiggsSUSYBB1500', 'HiggsSUSYBB1600', 'HiggsSUSYBB1800', 'HiggsSUSYBB2000', 'HiggsSUSYBB2300', 'HiggsSUSYBB2600', 'HiggsSUSYBB2900', 'HiggsSUSYBB3200', 'HiggsSUSYGG80', 'HiggsSUSYGG90',
                  # 'HiggsSUSYGG100', 'HiggsSUSYGG110', 'HiggsSUSYGG120', 'HiggsSUSYGG130', 'HiggsSUSYGG140', 'HiggsSUSYGG160', 'HiggsSUSYGG180', 'HiggsSUSYGG200', 'HiggsSUSYGG250', 'HiggsSUSYGG300', 'HiggsSUSYGG400', 'HiggsSUSYGG450', 'HiggsSUSYGG500', 'HiggsSUSYGG600', 'HiggsSUSYGG700', 'HiggsSUSYGG800', 'HiggsSUSYGG900', 'HiggsSUSYGG1000', 'HiggsSUSYGG1200', 'HiggsSUSYGG1400', 'HiggsSUSYGG1500', 'HiggsSUSYGG1600', 'HiggsSUSYGG1800', 'HiggsSUSYGG2000', 'HiggsSUSYGG2300', 'HiggsSUSYGG2600', 'HiggsSUSYGG2900', 'HiggsSUSYGG3200']  # HiggsSUSYBB800, HiggsSUSYBB1400, HiggsSUSYGG350
    mssm_names = ['HiggsSUSYGG160', 'HiggsSUSYBB500', 'HiggsSUSYBB1000',]
    for name in mssm_names:
        samples_mssm.append(SampleCfg(name=name.replace('HiggsSUSYBB', 'bbH').replace('HiggsSUSYGG', 'ggH'), dir_name=name,
                                      ana_dir=analysis_dir, tree_prod_name=tree_prod_name, xsec=1., sumweights=1., is_signal=True),)
        # SampleCfg(name='HiggsSUSYGG200', dir_name='HiggsSUSYGG200', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, xsec=100., sumweights=1., is_signal=True),
        # SampleCfg(name='HiggsSUSYGG500', dir_name='HiggsSUSYGG500', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, xsec=100., sumweights=1., is_signal=True),
        # SampleCfg(name='HiggsSUSYGG1000', dir_name='HiggsSUSYGG1000', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, xsec=100., sumweights=1., is_signal=True),
        # SampleCfg(name='HiggsSUSYGG1500', dir_name='HiggsSUSYGG1500', ana_dir=analysis_dir, tree_prod_name=tree_prod_name, xsec=100., sumweights=1., is_signal=True),
    # ]

    samples_susy = []
    if mode == 'susy':
        
        normfile = ROOT.TFile('/data1/steggema/tt/230816/DiTauNewMC/SMS_TStauStau/ttHhistoCounterAnalyzer/sumhist.root')
        normhist = normfile.Get('SumGenWeightsSMS')

        def createSusySampleCfg(m_stau=150, m_chi0=1):
            sname = 'SMS_TStauStau'
            return SampleCfg(name=sname+'MStau{m_stau}MChi{m_chi0}'.format(m_stau=m_stau, m_chi0=m_chi0), dir_name=sname, ana_dir=analysis_dir, tree_prod_name=tree_prod_name, xsec=get_xsec(m_stau), sumweights=normhist.GetBinContent(m_stau+1, m_chi0+1, 1), is_signal=True, weight_expr='(GenSusyMStau=={m_stau}. && GenSusyMNeutralino=={m_chi0})'.format(m_stau=m_stau, m_chi0=m_chi0))

        samples_susy.append(createSusySampleCfg(100, 1))
        samples_susy.append(createSusySampleCfg(200, 1))
        samples_susy.append(createSusySampleCfg(150, 1))
        samples_susy.append(createSusySampleCfg(150, 10))
        samples_susy.append(createSusySampleCfg(150, 20))
        samples_susy.append(createSusySampleCfg(150, 50))
        samples_susy.append(createSusySampleCfg(150, 100))


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
    if useDYWeight:
        weighted_list += ['ZTT', 'ZTT1Jets', 'ZTT2Jets', 'ZTT3Jets', 'ZTT4Jets',
                          'ZJ', 'ZJ1Jets', 'ZJ2Jets', 'ZJ3Jets', 'ZJ4Jets',
                          'ZL', 'ZL1Jets', 'ZL2Jets', 'ZL3Jets', 'ZL4Jets',
                          'ZTTM150', 'ZJM150', 'ZLM150']

    for sample in samples_mc:
        if sample.name not in weighted_list:
            setSumWeights(sample, 'MCWeighter' if channel not in ['tau_fr'] else 'SkimAnalyzerCount')

    # sampleDict = {s.name: s for s in all_samples}
    sampleDict = {}
    for s in all_samples:
        sampleDict[s.name] = s

    for sample in all_samples:
        if sample.is_signal:
            sample.scale = sample.scale * signal_scale

    return samples_mc, samples_data, samples, all_samples, sampleDict

samples_mc, samples_data, samples, all_samples, sampleDict = createSampleLists()
