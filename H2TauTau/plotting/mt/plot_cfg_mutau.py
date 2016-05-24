import copy
from numpy import array
from collections import namedtuple

from CMGTools.H2TauTau.proto.plotter.PlotConfigs import HistogramCfg, VariableCfg
from CMGTools.H2TauTau.proto.plotter.categories_TauMu import cat_Inc
from CMGTools.H2TauTau.proto.plotter.HistCreator import createHistograms, createHistogram
from CMGTools.H2TauTau.proto.plotter.HistDrawer import HistDrawer
from CMGTools.H2TauTau.proto.plotter.Variables import taumu_vars, getVars
# from CMGTools.H2TauTau.proto.plotter.helper_methods import getPUWeight

from CMGTools.H2TauTau.proto.plotter.Samples import createSampleLists

Cut = namedtuple('Cut', ['name', 'cut'])

binning_mssm = array([0.,10.,20.,30.,40.,50.,60.,70.,80.,90.,100.,110.,120.,130.,140.,150.,160.,170.,180.,190.,200.,225.,250.,275.,300.,325.,350.,400.,500.,700.,900.,1100.,1300.,1500.,1700.,1900.,2100.,2300.,2500.,2700.,2900.,3100.,3300.,3500.,3700.,3900.])

binning_mssm_btag = array([0.,20.,40.,60.,80.,100.,120.,140.,160.,180.,200.,250.,300.,350.,400.,500.,700.,900.,1100.,1300.,1500.,1700.,1900.,2100.,2300.,2500.,2700.,2900.,3100.,3300.,3500.,3700.,3900.])

binning_mva = array([0., 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.85, 0.9, 0.925, 0.95, 0.975, 0.985, 0.9925, 1.001])
binning_mva2 = array([0., 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.85, 0.9, 0.925, 0.95, 0.975, 1.001])

def prepareCuts(mode):
    cuts = []
    inc_cut = '&&'.join([cat_Inc])
    # inc_cut += '&& l2_decayModeFinding'

    mt_cut = 'mt<30'
    if mode in ['sm', 'iso', 'cp']:
        mt_cut = 'mt<40'
        inc_cut += '&& n_bjets==0'

    
    # cuts.append(Cut('inclusive_tauisosideband', inc_cut.replace('l2_byIsolationMVArun2v1DBoldDMwLT>3.5', 'l2_byIsolationMVArun2v1DBoldDMwLT<3.5&&l2_byIsolationMVArun2v1DBoldDMwLT>0.5') + '&& l1_charge != l2_charge'))

    # cuts.append(Cut('inclusive', inc_cut + '&& l1_charge != l2_charge'))
    # cuts.append(Cut('inclusivemt40', inc_cut + '&& l1_charge != l2_charge && mt<40'))

    # MSSM Categories

    if 'mssm' in mode:
        cuts.append(Cut('nobtag', inc_cut + '&& l1_charge != l2_charge && n_bjets==0 && mt<30'))
        cuts.append(Cut('btag', inc_cut + '&& l1_charge != l2_charge && n_bjets>=1 && n_jets<=1 && mt<30'))
    if mode == 'mssm_signal':
        cuts.append(Cut('nobtag_highmtos', inc_cut + '&& l1_charge != l2_charge && n_bjets==0 && mt>70'))
        cuts.append(Cut('nobtag_highmtss', inc_cut + '&& l1_charge == l2_charge && n_bjets==0 && mt>70'))
        cuts.append(Cut('nobtag_lowmtss', inc_cut + '&& l1_charge == l2_charge && n_bjets==0 && mt<30'))

    if mode == 'mssm_signal':
        cuts.append(Cut('btag_highmtos', inc_cut + '&& l1_charge != l2_charge && n_bjets>=1 && n_jets<=1 && mt>70'))
        cuts.append(Cut('btag_highmtss', inc_cut + '&& l1_charge == l2_charge && n_bjets>=1 && n_jets<=1 && mt>70'))
        cuts.append(Cut('btag_lowmtss', inc_cut + '&& l1_charge == l2_charge && n_bjets>=1 && n_jets<=1 && mt<30'))

    if mode == 'sm':
        # cuts.append(Cut('mva_high', inc_cut + '&& l1_charge != l2_charge && mt<40 && mva>0.2'))
        # cuts.append(Cut('mva_vhigh', inc_cut + '&& l1_charge != l2_charge && mt<40 && mva>0.5'))
        # cuts.append(Cut('mva_low', inc_cut + '&& l1_charge != l2_charge && mt<40 && mva<0.2'))

        # for mva_cut in ['0.5', '0.6', '0.7']:
        #     cuts.append(Cut('mva_gr{cut}_vbf'.format(cut=mva_cut).replace('.', ''), inc_cut + '&& l1_charge != l2_charge && mt<40 && mva>{cut} && vbf_mjj>300 && abs(vbf_deta)>3.5'.format(cut=mva_cut)))
        #     cuts.append(Cut('mva_l{cut}_vbf'.format(cut=mva_cut).replace('.', ''), inc_cut + '&& l1_charge != l2_charge && mt<40 && mva<{cut} && vbf_mjj>300 && abs(vbf_deta)>3.5'.format(cut=mva_cut)))
        #     cuts.append(Cut('mva_gr{cut}_1jet'.format(cut=mva_cut).replace('.', ''), inc_cut + '&& l1_charge != l2_charge && mt<40 && mva>{cut} && !(vbf_mjj>300 && abs(vbf_deta)>3.5) && n_jets>0.5'.format(cut=mva_cut)))
        #     cuts.append(Cut('mva_l{cut}_1jet'.format(cut=mva_cut).replace('.', ''), inc_cut + '&& l1_charge != l2_charge && mt<40 && mva<{cut} && !(vbf_mjj>300 && abs(vbf_deta)>3.5) && n_jets>0.5'.format(cut=mva_cut)))

        #     cuts.append(Cut('mva_gr{cut}_0jet'.format(cut=mva_cut).replace('.', ''), inc_cut + '&& l1_charge != l2_charge && mt<40 && mva>{cut} && !(vbf_mjj>300 && abs(vbf_deta)>3.5) && n_jets<0.5'.format(cut=mva_cut)))
        #     cuts.append(Cut('mva_l{cut}_0jet'.format(cut=mva_cut).replace('.', ''), inc_cut + '&& l1_charge != l2_charge && mt<40 && mva<{cut} && !(vbf_mjj>300 && abs(vbf_deta)>3.5) && n_jets<0.5'.format(cut=mva_cut)))

        cuts.append(Cut('0jet_medium', inc_cut + '&& l1_charge != l2_charge && mt<40 && n_jets<0.5 && l2_pt>30. && l2_pt<45.'))
        cuts.append(Cut('0jet_high', inc_cut + '&& l1_charge != l2_charge && mt<40 && n_jets<0.5 && l2_pt>45.'))

        cut_vbf = '(vbf_mjj>500. && abs(vbf_deta)>3.5 && vbf_n_central==0.)'
        cut_vbf_tight = '(vbf_mjj>700. && abs(vbf_deta)>4.0 && vbf_n_central==0. && pthiggs>100.)'
        cut_vbf_loose = '({cut_vbf} && !({cut_vbf_tight}))'.format(cut_vbf=cut_vbf, cut_vbf_tight=cut_vbf_tight)

        cuts.append(Cut('1jet_medium', inc_cut + '&& l1_charge != l2_charge && mt<40 && n_jets>0.5 && l2_pt>30. && l2_pt<45. && !{vbf}'.format(vbf=cut_vbf)))
        cuts.append(Cut('1jet_high_lowhiggspt', inc_cut + '&& l1_charge != l2_charge && mt<40 && n_jets>0.5 && l2_pt>45. && pthiggs<100. && !{vbf}'.format(vbf=cut_vbf)))
        cuts.append(Cut('1jet_high_highhiggspt', inc_cut + '&& l1_charge != l2_charge && mt<40 && n_jets>0.5 && l2_pt>45. && pthiggs>100. && !{vbf}'.format(vbf=cut_vbf)))

        # cuts.append(Cut('0jet', inc_cut + '&& l1_charge != l2_charge && mt<40 && n_jets<0.5'))
        cuts.append(Cut('vbf', inc_cut + '&& l1_charge != l2_charge && mt<40 && {vbf}'.format(vbf=cut_vbf)))
        # cuts.append(Cut('1jet_novbf', inc_cut + '&& l1_charge != l2_charge && mt<40 && n_jets>0.5 && !{vbf}'.format(vbf=cut_vbf)))

        cuts.append(Cut('0jet_lowmva0', inc_cut + '&& l1_charge != l2_charge && mt<40 && n_jets<0.5 && mva0<0.1'))
        cuts.append(Cut('0jet_highmva0', inc_cut + '&& l1_charge != l2_charge && mt<40 && n_jets<0.5 && mva0>0.1'))
        cuts.append(Cut('vbf_lowmva0', inc_cut + '&& l1_charge != l2_charge && mt<40 && {vbf} && mva0<0.2'.format(vbf=cut_vbf)))
        cuts.append(Cut('vbf_highmva0', inc_cut + '&& l1_charge != l2_charge && mt<40 && {vbf} && mva0>0.2'.format(vbf=cut_vbf)))
        cuts.append(Cut('1jet_novbf_lowmva0', inc_cut + '&& l1_charge != l2_charge && mt<40 && n_jets>0.5 && !{vbf} && mva0<0.3'.format(vbf=cut_vbf)))
        cuts.append(Cut('1jet_novbf_highmva0', inc_cut + '&& l1_charge != l2_charge && mt<40 && n_jets>0.5 && !{vbf} && mva0>0.3'.format(vbf=cut_vbf)))

        cuts.append(Cut('vbf_loose', inc_cut + '&& l1_charge != l2_charge && l2_pt>30. && mt<40 && {vbf}'.format(vbf=cut_vbf_loose)))
        cuts.append(Cut('vbf_tight', inc_cut + '&& l1_charge != l2_charge && l2_pt>30. && mt<40 && {vbf}'.format(vbf=cut_vbf_tight)))

    if mode == 'cp':
        cuts.append(Cut('inclusivemt40', inc_cut + '&&  l1_charge != l2_charge && mt<40 && mvis>40 && mvis<90 && l2_nc_ratio>-99'))

    if mode == 'iso':
        cuts = []
        cuts.append(Cut('inclusivemtgr60', inc_cut + '&& l1_charge != l2_charge && mt>70 && n_jets<0.5'))
        # cuts.append(Cut('inclusivemtgr40antiiso', inc_cut.replace('l1_reliso05<0.1', 'l1_reliso05>0.2') + '&& l1_charge != l2_charge && mt>40'))
        cuts.append(Cut('inclusivemtgr60antiiso', inc_cut.replace('l2_byIsolationMVArun2v1DBoldDMwLT>3.5', 'l2_byIsolationMVArun2v1DBoldDMwLT<3.5') + '&& l1_charge != l2_charge && mt>70 && n_jets<0.5'))

    # cuts.append(Cut('SS', inc_cut + '&& l1_charge == l2_charge'))
    # cuts.append(Cut('SS_muantiiso', inc_cut.replace('l1_reliso05<0.1', 'l1_reliso05>0.2') + '&& l1_charge == l2_charge'))
    # cuts.append(Cut('SSmt40', inc_cut + '&& l1_charge == l2_charge && mt<40'))
    # cuts.append(Cut('SShighmt40', inc_cut + '&& l1_charge == l2_charge && mt>40'))

    return cuts, mt_cut

def createDefaultGroups(plot):
    plot.Group('VV', ['VVTo2L2Nu', 'ZZTo2L2Q', 'WWTo1L1Nu2Q', 'WZTo1L3Nu', 'ZZTo4L', 'WZTo3L', 'WZTo2L2Q', 'WZTo1L1Nu2Q', 'T_tWch', 'TBar_tWch', 'TToLeptons_tch_powheg', 'TBarToLeptons_tch_powheg'], silent=True)
    plot.Group('ZTT', ['ZTT', 'ZTT1Jets', 'ZTT2Jets', 'ZTT3Jets', 'ZTT4Jets', 'ZTTM150', 'ZTTM10'], silent=True)
    plot.Group('ZJ', ['ZJ', 'ZJ1Jets', 'ZJ2Jets', 'ZJ3Jets', 'ZJ4Jets', 'ZJM150', 'ZJM10'], silent=True)
    plot.Group('ZL', ['ZL', 'ZL1Jets', 'ZL2Jets', 'ZL3Jets', 'ZL4Jets', 'ZLM150', 'ZLM10'], silent=True)


def createSamples(mode, analysis_dir, total_weight, qcd_from_same_sign, w_qcd_mssm_method, r_qcd_os_ss):
    hist_dict = {}
    sample_dict = {}

    samples_mc, samples_data, samples, all_samples, sampleDict = createSampleLists(analysis_dir=analysis_dir)

    if mode == 'mssm_control' or not 'mssm' in mode:
        all_samples = [s for s in all_samples if not 'ggH' in s.name and not 'bbH' in s.name]

    sample_dict['all_samples'] = all_samples

    if qcd_from_same_sign and not w_qcd_mssm_method:
        samples_qcdfromss = [s for s in all_samples if s.name != 'QCD']
        samples_ss = copy.deepcopy(samples_qcdfromss)

        samples_ss = [s for s in samples_ss if not s.is_signal]

        for sample in samples_ss:
            if sample.name != 'data_obs':
                # Subtract background from data
                sample.scale = -1.

        qcd = HistogramCfg(name='QCD', var=None, cfgs=samples_ss, cut=None, total_scale=r_qcd_os_ss, lumi=int_lumi, weight=total_weight)

        samples_qcdfromss.append(qcd)
        sample_dict['samples_qcdfromss'] = samples_qcdfromss

    if w_qcd_mssm_method:
        w_names = ['W', 'W1Jets', 'W2Jets', 'W3Jets', 'W4Jets']
        samples_non_w = [s for s in all_samples if s.name != 'QCD' and s.name not in w_names and not s.is_signal]
        samples_non_w_ss = copy.deepcopy(samples_non_w)
        
        samples_signal = [s for s in all_samples if s.is_signal]

        samples_w = copy.deepcopy([s for s in all_samples if s.name in w_names])
        samples_w_ss = copy.deepcopy(samples_w)
        
        # To calculate OS/SS ratio in inclusive W selection
        samples_w_incl_os = copy.deepcopy(samples_w)
        samples_w_incl_ss = copy.deepcopy(samples_w)

        # To calculate W scale factor
        samples_w_highmt_os = copy.deepcopy(samples_w)

        # Build a high MT region: OS - non-W/QCD OS - (SS - non-W/QCD SS)
        samples_non_w_highmt_os = copy.deepcopy(samples_non_w)
        samples_non_w_highmt_ss = copy.deepcopy(samples_non_w)


        for sample in samples_non_w_highmt_os:
            if sample.name != 'data_obs':
                # Subtract background from data
                sample.scale = -1.

        for sample in samples_non_w_highmt_ss:
            if sample.name != 'data_obs':
                sample.scale = -1.

        for sample in samples_non_w_ss:
            if sample.name != 'data_obs':
                sample.scale = -1.

        var_norm = VariableCfg(name='_norm_', drawname='1.', binning={'nbinsx':5, 'xmin':-1.5, 'xmax':3.5}, unit='', xtitle='Normalisation')

        hist_dict['stacknow_highmt_os'] = HistogramCfg(name='HighMTOS', var=var_norm, cfgs=samples_non_w_highmt_os, cut=None, lumi=int_lumi, weight=total_weight)
        hist_dict['stacknow_highmt_ss'] = HistogramCfg(name='HighMTSS', var=var_norm, cfgs=samples_non_w_highmt_ss, cut=None, lumi=int_lumi, weight=total_weight)

        hist_dict['wjets_incl_os'] = HistogramCfg(name='WInclOS', var=var_norm, cfgs=samples_w_incl_os, cut=None, lumi=int_lumi, weight=total_weight)
        hist_dict['wjets_incl_ss'] = HistogramCfg(name='WInclSS', var=var_norm, cfgs=samples_w_incl_ss, cut=None, lumi=int_lumi, weight=total_weight)

        hist_dict['wjets_highmt_os'] = HistogramCfg(name='WHighMTOS', var=var_norm, cfgs=samples_w_highmt_os, cut=None, lumi=int_lumi, weight=total_weight)

        hist_dict['wjets'] = HistogramCfg(name='W', var=None, cfgs=samples_w, cut=None, lumi=int_lumi, weight=total_weight)
        hist_dict['wjets_ss'] = HistogramCfg(name='WSS', var=None, cfgs=samples_w_ss, cut=None, lumi=int_lumi, weight=total_weight)

        hist_dict['qcd'] = HistogramCfg(name='QCD', var=None, cfgs=samples_non_w_ss + [hist_dict['wjets_ss']], cut=None, total_scale=r_qcd_os_ss, lumi=int_lumi, weight=total_weight)

        sample_dict['samples_mssm_method'] = samples_non_w + [hist_dict['wjets'], hist_dict['qcd']] + samples_signal

    return sample_dict, hist_dict

def createVariables(mode):
    # Taken from Variables.py; can get subset with e.g. getVars(['mt', 'mvis'])
    # variables = taumu_vars
    # variables = getVars(['_norm_', 'mt', 'mvis', 'l1_pt', 'l2_pt', 'l1_eta', 'l2_eta', 'n_vertices', 'n_jets', 'n_bjets'])

    variables = []
    if mode == 'sm':
        variables = [
            # VariableCfg(name='mva', binning={'nbinsx':20, 'xmin':0., 'xmax':1.}, unit='', xtitle='s_{BDT}'),
            VariableCfg(name='svfit_mass', binning={'nbinsx':20, 'xmin':50., 'xmax':250}, unit='GeV', xtitle='m_{SVFit}'),
            VariableCfg(name='mva0', binning={'nbinsx':20, 'xmin':0., 'xmax':1.0001}, unit='', xtitle='s_{BDT} (BG)'),
            VariableCfg(name='mva1', binning={'nbinsx':20, 'xmin':0., 'xmax':1.0001}, unit='', xtitle='s_{BDT} (ZTT)'),
            VariableCfg(name='mva2', binning=binning_mva2, unit='', xtitle='s_{BDT} (Higgs)'),
            # VariableCfg(name='mva2div1', drawname='mva2/(mva1+mva2)', binning={'nbinsx':20, 'xmin':0., 'xmax':1.0001}, unit='', xtitle='s_{BDT}^{Higgs}/s_{BDT}^{ZTT}'),
            VariableCfg(name='mva2div1', drawname='mva2/(mva1+mva2)', binning=binning_mva, unit='', xtitle='s_{BDT}^{Higgs}/s_{BDT}^{ZTT}'),
        ]

        # MVA training variables
        variables += getVars(['mt', 'n_jets', 'met_pt', 'pthiggs', 'vbf_mjj', 'vbf_deta', 'vbf_n_central', 'l2_pt', 'l1_pt', 'svfit_transverse_mass', 'delta_phi_l1_l2', 'delta_eta_l1_l2', 'mvis'])

    if mode == 'cp':
        variables = getVars(['l2_nc_ratio'])

    if mode == 'mssm_signal':
        variables = [
            VariableCfg(name='svfit_transverse_mass', binning=binning_mssm, unit='GeV', xtitle='m_{T,SVFit}'),
            VariableCfg(name='svfit_mass', binning=binning_mssm, unit='GeV', xtitle='m_{SVFit}'),
            VariableCfg(name='mvis', binning=binning_mssm, unit='GeV', xtitle='m_{vis}'),
        ]

    if mode == 'iso':
        variables = getVars(['mt', 'l1_pt', 'l2_pt', 'l1_eta', 'l2_eta'])

    return variables

def makePlots(variables, cuts, total_weight, sample_dict, hist_dict, qcd_from_same_sign, w_qcd_mssm_method, mt_cut, friend_func, dc_postfix, make_plots=True):
    for cut in cuts:
        if qcd_from_same_sign and not 'SS' in cut.name and not w_qcd_mssm_method:
            cfg_main = HistogramCfg(name=cut.name, var=None, cfgs=sample_dict['samples_qcdfromss'], cut=cut.cut, lumi=int_lumi, weight=total_weight)
        elif w_qcd_mssm_method:
            cfg_main = HistogramCfg(name=cut.name, var=None, cfgs=sample_dict['samples_mssm_method'], cut=cut.cut, lumi=int_lumi, weight=total_weight)
            hist_dict['wjets'].cut = cut.cut # since wjets is a sub-HistogramCfg
        else:
            cfg_main = HistogramCfg(name=cut.name, var=None, cfgs=sample_dict['all_samples'], cut=cut.cut, lumi=int_lumi, weight=total_weight)
        
        if qcd_from_same_sign and not 'SS' in cut.name:
            hist_dict['qcd'].cut = cut.cut.replace('l1_charge != l2_charge', 'l1_charge == l2_charge')

        if w_qcd_mssm_method:
            hist_dict['stacknow_highmt_os'].name = 'HighMTOS'+cut.name
            hist_dict['stacknow_highmt_ss'].name = 'HighMTSS'+cut.name
            hist_dict['wjets_incl_os'].name = 'WInclOS'+cut.name
            hist_dict['wjets_incl_ss'].name = 'WInclSS'+cut.name
            hist_dict['wjets_highmt_os'].name = 'WHighMTOS'+cut.name
            hist_dict['wjets_ss'].name = 'WJetsSS'+cut.name

            hist_dict['qcd'].cut = cut.cut.replace('l1_charge != l2_charge', 'l1_charge == l2_charge')
            hist_dict['wjets_ss'].cut = cut.cut.replace('l1_charge != l2_charge', 'l1_charge == l2_charge')

            hist_dict['stacknow_highmt_os'].cut = cut.cut.replace(mt_cut, 'mt>70') + '&& mt>70'
            hist_dict['stacknow_highmt_ss'].cut = cut.cut.replace('l1_charge != l2_charge', 'l1_charge == l2_charge').replace(mt_cut, 'mt>70') + '&& mt>70'

            hist_dict['wjets_incl_os'].cut = cut.cut.replace(mt_cut, '1.')
            hist_dict['wjets_incl_ss'].cut = cut.cut.replace('l1_charge != l2_charge', 'l1_charge == l2_charge').replace(mt_cut, '1.')

            hist_dict['wjets_highmt_os'].cut = cut.cut.replace(mt_cut, 'mt>70') + '&& mt>70'

            plot_w_os = createHistogram(hist_dict['wjets_incl_os'], verbose=False, friend_func=friend_func)
            plot_w_ss = createHistogram(hist_dict['wjets_incl_ss'], verbose=False, friend_func=friend_func)

            r_w_os_ss = plot_w_os.GetStack().totalHist.Yield()/plot_w_ss.GetStack().totalHist.Yield()
            print 'Inclusive W OS/SS ratio:', r_w_os_ss

            plot_highmt_os = createHistogram(hist_dict['stacknow_highmt_os'], all_stack=True, verbose=False, friend_func=friend_func)
            plot_highmt_ss = createHistogram(hist_dict['stacknow_highmt_ss'], all_stack=True, verbose=False, friend_func=friend_func)
            createDefaultGroups(plot_highmt_os)
            createDefaultGroups(plot_highmt_ss)

            yield_highmt_os = plot_highmt_os.GetStack().totalHist.Yield()
            yield_highmt_ss = plot_highmt_ss.GetStack().totalHist.Yield()

            plot_w_highmt_os = createHistogram(hist_dict['wjets_highmt_os'], verbose=False, friend_func=friend_func)

            yield_w_highmt_os = plot_w_highmt_os.GetStack().totalHist.Yield()

            if r_w_os_ss < r_qcd_os_ss:
                print 'WARNING, OS/SS ratio larger for QCD than for W+jets!', r_w_os_ss, r_qcd_os_ss

            yield_estimation = r_w_os_ss*(yield_highmt_os - r_qcd_os_ss*yield_highmt_ss)/(r_w_os_ss - r_qcd_os_ss)

            print 'High MT W+jets estimated yield', yield_estimation
            print 'High MT W+jets MC yield', yield_w_highmt_os

            w_sf = 0.
            if yield_w_highmt_os:
                w_sf = yield_estimation/yield_w_highmt_os
            else:
                print 'Warning: no MC events in high MT W+jets'

            print 'W+jets scale factor:', w_sf, '\n'
            if cut.name == 'vbf_highmva0':
                print 'VBF very tight category, fixing W+jets SF to 1'
                w_sf = 1.
            hist_dict['wjets'].total_scale = w_sf
            hist_dict['wjets_ss'].total_scale = -w_sf

        cfg_main.vars = variables
        if qcd_from_same_sign:
            hist_dict['qcd'].vars = variables # Can put into function but we will not want it by default if we take normalisations from e.g. high MT
        if w_qcd_mssm_method:
            hist_dict['wjets'].vars = variables # Can put into function but we will not want it by default if we take normalisations from e.g. high MT
            hist_dict['qcd'].vars = variables
            hist_dict['wjets_ss'].vars = variables

        for variable in variables:
            if variable.name in ['svfit_mass', 'svfit_transverse_mass', 'mvis'] and 'mssm' in mode:
                if cut.name in ['inclusive', 'nobtag']:
                    variable.binning = binning_mssm
                elif cut.name in ['btag']:
                    variable.binning = binning_mssm_btag

        plots = createHistograms(cfg_main, verbose=False, friend_func=friend_func)
        for variable in variables:
        # for plot in plots.itervalues():
            plot = plots[variable.name]
            createDefaultGroups(plot)
            if not w_qcd_mssm_method:
                plot.Group('W', ['W', 'W1Jets', 'W2Jets', 'W3Jets', 'W4Jets'])
            # plot.Group('Electroweak', ['Diboson', 'W'])
            # plot.Group('Single t', ['T_tWch', 'TBar_tWch', 'TToLeptons_sch', 'TToLeptons_tch'])
            # plot.Group('ZLL', ['Ztt_ZL', 'Ztt_ZJ'], style=plot.Hist('Ztt_ZL').style)
            if make_plots:
                HistDrawer.draw(plot, plot_dir='plots/'+cut.name)
            if variable.name in ['mvis', 'svfit_transverse_mass', 'svfit_mass', 'mva', 'mva2div1', 'mva1', 'mva2', 'l2_nc_ratio']:
                plot.WriteDataCard(filename='datacard_{mode}_{var}.root'.format(mode=mode, var=variable.name), dir='mt_' + cut.name, mode='UPDATE', postfix=dc_postfix) #mt = mu-tau

if __name__ == '__main__':
        
    # mode = 'iso'
    mode = 'sm'
    # mode = 'cp'
    # mode = 'mssm_signal' 
    # mode = 'mssm_control'

    # friend_func = lambda f: f.replace('MC', 'MVA')
    friend_func = lambda f: f.replace('MC', 'MultiMVA')
    

    int_lumi = 2301. # from Alexei's email
    qcd_from_same_sign = True
    w_qcd_mssm_method = True
    r_qcd_os_ss = 1.17

    if mode == 'iso':
        qcd_from_same_sign = False
        w_qcd_mssm_method = False
        friend_func = None

    run_central = True
    add_ttbar_sys = False
    add_tes_sys = True


    analysis_dir = '/data1/steggema/mt/070416/TauMuSVFitMC/'

    total_weight = 'weight'#*weight_njet'

    print total_weight

    cuts, mt_cut = prepareCuts(mode)

    variables = createVariables(mode)

    if run_central:
        sample_dict, hist_dict = createSamples(mode, analysis_dir, total_weight, qcd_from_same_sign, w_qcd_mssm_method, r_qcd_os_ss)
        makePlots(variables, cuts, total_weight, sample_dict, hist_dict, qcd_from_same_sign, w_qcd_mssm_method, mt_cut, friend_func, dc_postfix='')

    if add_ttbar_sys:

        weight_ttbar_up = 'weight * gen_top_weight'

        sample_dict, hist_dict = createSamples(mode, analysis_dir, weight_ttbar_up, qcd_from_same_sign=False, w_qcd_mssm_method=False, r_qcd_os_ss=None)

        sample_dict_ttbar = {'all_samples':[s for s in sample_dict['all_samples'] if s.name == 'TT']}

        makePlots(variables, cuts, weight_ttbar_up, sample_dict_ttbar, hist_dict={}, qcd_from_same_sign=False, w_qcd_mssm_method=False, mt_cut=mt_cut, friend_func=friend_func, dc_postfix='_CMS_htt_ttbarShape_13TeVUp', make_plots=False)

        weight_ttbar_down = 'weight / gen_top_weight'

        sample_dict, hist_dict = createSamples(mode, analysis_dir, weight_ttbar_up, qcd_from_same_sign=False, w_qcd_mssm_method=False, r_qcd_os_ss=None)

        sample_dict_ttbar = {'all_samples':[s for s in sample_dict['all_samples'] if s.name == 'TT']}


        makePlots(variables, cuts, weight_ttbar_down, sample_dict_ttbar, hist_dict={}, qcd_from_same_sign=False, w_qcd_mssm_method=False, mt_cut=mt_cut, friend_func=friend_func, dc_postfix='_CMS_htt_ttbarShape_13TeVDown', make_plots=False)

    if add_tes_sys:
        tes_samples = ['ZTT', 'ZTTM10', 'HiggsGGH125', 'HiggsVBF125']

        analysis_dir = '/data1/steggema/mt/070416/TauMuSVFitTESUp/'
        sample_dict, hist_dict = createSamples(mode, analysis_dir, total_weight, qcd_from_same_sign=False, w_qcd_mssm_method=False, r_qcd_os_ss=None)
        sample_dict_tes = {'all_samples':[s for s in sample_dict['all_samples'] if s.name in tes_samples]}
        makePlots(variables, cuts, total_weight, sample_dict_tes, hist_dict={}, qcd_from_same_sign=False, w_qcd_mssm_method=False, mt_cut=mt_cut, friend_func=lambda f: f.replace('TESUp', 'TESUpMultiMVA'), dc_postfix='_CMS_scale_t_mt_13TeVUp', make_plots=False)

        analysis_dir = '/data1/steggema/mt/070416/TauMuSVFitTESDown/'
        sample_dict, hist_dict = createSamples(mode, analysis_dir, total_weight, qcd_from_same_sign=False, w_qcd_mssm_method=False, r_qcd_os_ss=None)
        sample_dict_tes = {'all_samples':[s for s in sample_dict['all_samples'] if s.name in tes_samples]}

        makePlots(variables, cuts, total_weight, sample_dict_tes, hist_dict={}, qcd_from_same_sign=False, w_qcd_mssm_method=False, mt_cut=mt_cut, friend_func=lambda f: f.replace('TESDown', 'TESDownMultiMVA'), dc_postfix='_CMS_scale_t_mt_13TeVDown', make_plots=False)


