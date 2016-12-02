from copy import deepcopy

from CMGTools.H2TauTau.proto.plotter.PlotConfigs import HistogramCfg, VariableCfg
from CMGTools.H2TauTau.proto.plotter.HistCreator import createHistogram
from CMGTools.H2TauTau.proto.plotter.defaultGroups import createDefaultGroups

def createQCDWHistograms(samples, hist_dict, int_lumi, weight, r_qcd_os_ss=1.17):
    w_names = ['W', 'W1Jets', 'W2Jets', 'W3Jets', 'W4Jets']
    samples_non_w = [s for s in samples if s.name != 'QCD' and s.name not in w_names and not s.is_signal]
    samples_non_w_ss = deepcopy(samples_non_w)
    
    samples_signal = [s for s in samples if s.is_signal]

    samples_w = deepcopy([s for s in samples if s.name in w_names])
    samples_w_ss = deepcopy(samples_w)
    
    # To calculate OS/SS ratio in inclusive W selection
    samples_w_incl_os = deepcopy(samples_w)
    samples_w_incl_ss = deepcopy(samples_w)

    # To calculate W scale factor
    samples_w_highmt_os = deepcopy(samples_w)

    # Build a high MT region: OS - non-W/QCD OS - (SS - non-W/QCD SS)
    samples_non_w_highmt_os = deepcopy(samples_non_w)
    samples_non_w_highmt_ss = deepcopy(samples_non_w)


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

    hist_dict['stacknow_highmt_os'] = HistogramCfg(name='HighMTOS', var=var_norm, cfgs=samples_non_w_highmt_os, cut=None, lumi=int_lumi, weight=weight)
    hist_dict['stacknow_highmt_ss'] = HistogramCfg(name='HighMTSS', var=var_norm, cfgs=samples_non_w_highmt_ss, cut=None, lumi=int_lumi, weight=weight)

    hist_dict['wjets_incl_os'] = HistogramCfg(name='WInclOS', var=var_norm, cfgs=samples_w_incl_os, cut=None, lumi=int_lumi, weight=weight)
    hist_dict['wjets_incl_ss'] = HistogramCfg(name='WInclSS', var=var_norm, cfgs=samples_w_incl_ss, cut=None, lumi=int_lumi, weight=weight)

    hist_dict['wjets_highmt_os'] = HistogramCfg(name='WHighMTOS', var=var_norm, cfgs=samples_w_highmt_os, cut=None, lumi=int_lumi, weight=weight)

    hist_dict['wjets'] = HistogramCfg(name='W', var=None, cfgs=samples_w, cut=None, lumi=int_lumi, weight=weight)
    hist_dict['wjets_ss'] = HistogramCfg(name='WSS', var=None, cfgs=samples_w_ss, cut=None, lumi=int_lumi, weight=weight)

    hist_dict['qcd'] = HistogramCfg(name='QCD', var=None, cfgs=samples_non_w_ss + [hist_dict['wjets_ss']], cut=None, total_scale=r_qcd_os_ss, lumi=int_lumi, weight=weight)

    return samples_non_w + [hist_dict['wjets'], hist_dict['qcd']] + samples_signal

def estimateQCDWMSSM(hist_dict, cut, mt_cut, high_mt_cut='mt>70', friend_func=None, r_qcd_os_ss=1.17):
    hist_dict['stacknow_highmt_os'].name = 'HighMTOS'+cut.name
    hist_dict['stacknow_highmt_ss'].name = 'HighMTSS'+cut.name
    hist_dict['wjets_incl_os'].name = 'WInclOS'+cut.name
    hist_dict['wjets_incl_ss'].name = 'WInclSS'+cut.name
    hist_dict['wjets_highmt_os'].name = 'WHighMTOS'+cut.name
    hist_dict['wjets_ss'].name = 'WJetsSS'+cut.name

    hist_dict['qcd'].cut = cut.cut.replace('l1_charge != l2_charge', 'l1_charge == l2_charge')
    hist_dict['wjets_ss'].cut = cut.cut.replace('l1_charge != l2_charge', 'l1_charge == l2_charge')

    hist_dict['stacknow_highmt_os'].cut = cut.cut.replace(mt_cut, high_mt_cut) + '&& ' + high_mt_cut
    hist_dict['stacknow_highmt_ss'].cut = cut.cut.replace('l1_charge != l2_charge', 'l1_charge == l2_charge').replace(mt_cut, high_mt_cut) + '&& ' + high_mt_cut

    hist_dict['wjets_incl_os'].cut = cut.cut.replace(mt_cut, '1.')
    hist_dict['wjets_incl_ss'].cut = cut.cut.replace('l1_charge != l2_charge', 'l1_charge == l2_charge').replace(mt_cut, '1.')

    hist_dict['wjets_highmt_os'].cut = cut.cut.replace(mt_cut, high_mt_cut) + '&& ' + high_mt_cut

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

    print plot_w_highmt_os
    print plot_highmt_os
    print 'Having used cut', hist_dict['stacknow_highmt_os'].cut
    print plot_highmt_ss

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

    if w_sf <= 0.25:
        print 'Warning: W+jets scale factor very small or negative', w_sf, 'setting to 1.'
        w_sf = 1.

    if w_sf > 2.5 and yield_w_highmt_os and yield_w_highmt_os < 10.:
        print 'Warning: W+jets scale factor very large', w_sf, ' but low stats, setting to 1.'
        w_sf = 1.

    # if cut.name in ['vbf_highmva0', '0jet_highmva0']:
    #     print 'Very tight category, fixing W+jets SF to 1'
    #     w_sf = 1.
    hist_dict['wjets'].total_scale = w_sf
    hist_dict['wjets_ss'].total_scale = -w_sf
