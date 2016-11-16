import copy

from CMGTools.H2TauTau.proto.plotter.Variables import dict_all_vars
from CMGTools.H2TauTau.proto.plotter.HistCreator import createHistogram
from CMGTools.H2TauTau.proto.plotter.PlotConfigs import HistogramCfg

def qcd_estimation(B_cut, C_cut, D_cut, all_samples, int_lumi, total_weight, scale=1., verbose=True, friend_func=None):
    '''ABCD method.
    
     A | B
    -------
     C | D
     
    A is the signal region
    B is where the shape is taken from
    C/D gives the scale factor to be applied to the shape in B
    
    Returns an updated list of samples that includes the QCD HistgramCfg.
    '''
    
    norm_var = dict_all_vars['_norm_']

    QCD_C_region_cut = C_cut
    QCD_D_region_cut = D_cut
    QCD_B_region_cut = B_cut
        
    samples_qcd_copy = copy.deepcopy( [s for s in all_samples if s.name != 'QCD' and not s.is_signal] )
    samples_qcd_copy = [s for s in samples_qcd_copy if not s.is_signal]
    
    for sample in samples_qcd_copy:
        sample.scale = scale if sample.name == 'data_obs' else -scale
    
    qcd_c_region = HistogramCfg(name='QCD_C_region', var=norm_var, cfgs=samples_qcd_copy, cut=str(QCD_C_region_cut), lumi=int_lumi, weight=total_weight)
    qcd_d_region = HistogramCfg(name='QCD_D_region', var=norm_var, cfgs=samples_qcd_copy, cut=str(QCD_D_region_cut), lumi=int_lumi, weight=total_weight)

    # samples_qcd = [qcd_c_region, qcd_d_region] 

    # cfg_qcd = HistogramCfg(name='QCD_aux', var=None, cfgs=samples_qcd, cut=None, lumi=int_lumi, weight=total_weight)
    
    plot_qcd_c = createHistogram(qcd_c_region, all_stack=True, friend_func=friend_func)
    plot_qcd_d = createHistogram(qcd_d_region, all_stack=True, friend_func=friend_func)

    if verbose:
        print 'Histogram C region'
        print plot_qcd_c
        print 'Histogram D region'
        print plot_qcd_d

    yield_c = plot_qcd_c.GetStack().totalHist.Yield()
    yield_d = plot_qcd_d.GetStack().totalHist.Yield()

    if yield_d == 0.:
        print 'WARNING: no events left for the QCD estimation. Set to 0'
        qcd_scale = 0.
    else:
        qcd_scale = yield_c / yield_d

    if qcd_scale < 0.:
        print 'WARNING: negative QCD scaling; set it to zero'
        qcd_scale = 0.
        verbose = True

    if verbose:
        print 'QCD estimation: '
        print '  Yield C:', yield_c, ' yield D:', yield_d
        print '  Ratio C/D', qcd_scale

    qcd_b_region_hist = HistogramCfg(name='QCD', var=None, cfgs=samples_qcd_copy, cut=str(QCD_B_region_cut), lumi=int_lumi, weight=total_weight, total_scale=qcd_scale)
    
    all_samples_qcd = copy.deepcopy(all_samples)
    all_samples_qcd = [qcd_b_region_hist] + all_samples_qcd
    
    return all_samples_qcd

