import copy
from collections import namedtuple

from CMGTools.H2TauTau.proto.plotter.PlotConfigs       import SampleCfg, HistogramCfg, VariableCfg
from CMGTools.H2TauTau.proto.plotter.categories_TauTau import cat_Inc, cat_Inc_AntiIso
from CMGTools.H2TauTau.proto.plotter.HistCreator       import createHistogram, setSumWeights
from CMGTools.H2TauTau.proto.plotter.HistDrawer        import HistDrawer
from CMGTools.H2TauTau.proto.plotter.Variables         import all_vars, getVars
from CMGTools.H2TauTau.proto.plotter.Samples           import createSampleLists

int_lumi = 2240. # from Alexei's email
tree_prod_name = 'H2TauTauTreeProducerTauTau'
analysis_dir   = '/afs/cern.ch/work/m/manzoni/diTau2015/CMSSW_7_6_3/src/CMGTools/H2TauTau/cfgPython/tt/tt_14march2016'

total_weight = 'weight'

samples_mc, samples_data, samples, all_samples, sampleDict = createSampleLists(analysis_dir=analysis_dir, channel='tt')

Cut = namedtuple('Cut', ['name', 'cut'])
cuts = []
inc_cut          = '&&'.join([cat_Inc])
inc_anti_iso_cut = '&&'.join([cat_Inc_AntiIso])

cuts.append(Cut('inclusive', inc_cut + '&& l1_charge != l2_charge'))

# Taken from Variables.py, can get subset with e.g. getVars(['mt', 'mvis'])
variables = all_vars
variables = getVars(['mvis', 'l1_pt', 'l2_pt'])

# QCD estimation
def qcd_estimation(cut, sideband_cut, all_samples, scale = 1.):
    '''ABCD method.
    Shape from opposite sign events in an isolation sideband.
    Scale factor from same sign regions, isolated and sideband.
    returns an updated list of samples that includes the QCD HIstgramCfg.
    '''
    regions = {}
    
    regions['QCD_ss_tight'] = Cut('QCD_ss_tight', cut          + '&& l1_charge == l2_charge && l1_byIsolationMVArun2v1DBoldDMwLT > 1.5 && l2_byIsolationMVArun2v1DBoldDMwLT > 1.5')
    regions['QCD_ss_loose'] = Cut('QCD_ss_loose', sideband_cut + '&& l1_charge == l2_charge && l1_byIsolationMVArun2v1DBoldDMwLT > 1.5 && l2_byIsolationMVArun2v1DBoldDMwLT > 1.5')
    regions['QCD_os_loose'] = Cut('QCD_os_loose', sideband_cut + '&& l1_charge != l2_charge && l1_byIsolationMVArun2v1DBoldDMwLT > 1.5 && l2_byIsolationMVArun2v1DBoldDMwLT > 1.5')
        
    samples_qcd_copy = copy.deepcopy( [s for s in all_samples if s.name != 'QCD' and not s.is_signal] )
    samples_qcd_copy = [s for s in samples_qcd_copy if not s.is_signal]
    
    for sample in samples_qcd_copy:
        sample.scale = scale if sample.name == 'data_obs' else -scale
    
    qcd_ss_tight = HistogramCfg(name=regions['QCD_ss_tight'].name, var=None, cfgs=samples_qcd_copy, cut=regions['QCD_ss_tight'].cut, lumi=int_lumi, weight=total_weight)
    qcd_ss_loose = HistogramCfg(name=regions['QCD_ss_loose'].name, var=None, cfgs=samples_qcd_copy, cut=regions['QCD_ss_loose'].cut, lumi=int_lumi, weight=total_weight)

    samples_qcd = [qcd_ss_tight, qcd_ss_loose] 

    cfg_qcd = HistogramCfg(name='QCD_aux', var=None, cfgs=samples_qcd, cut=None, lumi=int_lumi, weight=total_weight)
    
    plotQCD = createHistogram(cfg_qcd)

    qcd_ss_tight_hist = [hist for hist in plotQCD.histos if hist.name == 'QCD_ss_tight'][0]
    qcd_ss_loose_hist = [hist for hist in plotQCD.histos if hist.name == 'QCD_ss_loose'][0]
    
    qcd_scale = qcd_ss_tight_hist.Integral() / max(1.e-9, qcd_ss_loose_hist.Integral())

    qcd_os_loose = HistogramCfg(name='QCD', var=None, cfgs=samples_qcd_copy, cut=regions['QCD_os_loose'].cut, lumi=int_lumi, weight=total_weight+'* %f' %qcd_scale)
    
    all_samples_qcd = copy.deepcopy(all_samples)
    all_samples_qcd.append(qcd_os_loose)
    
    return all_samples_qcd

for cut in cuts:

    # RIC: FIXME! - cuts are ~hard coded now
    all_samples_qcd = qcd_estimation(inc_cut, inc_anti_iso_cut, all_samples)
    
    for variable in variables:
        cfg_total = HistogramCfg(name=cut.name, var=variable, cfgs=all_samples_qcd, cut=cut.cut, lumi=int_lumi, weight=total_weight)
        all_samples_qcd[-1].var = variable
        plot = createHistogram(cfg_total)
        plot.Group('VV', ['ZZTo2L2Q', 'WWTo1L1Nu2Q', 'WZTo1L3Nu', 'ZZTo4L', 'WZTo3L', 'WZTo2L2Q', 'WZTo1L1Nu2Q', 'T_tWch', 'TBar_tWch', 'TToLeptons_tch_powheg', 'TBarToLeptons_tch_powheg'])
        plot.Group('ZTT', ['ZTT', 'ZTT1Jets', 'ZTT2Jets', 'ZTT3Jets', 'ZTT4Jets'])
        plot.Group('ZJ', ['ZJ', 'ZJ1Jets', 'ZJ2Jets', 'ZJ3Jets', 'ZJ4Jets'])
        plot.Group('ZL', ['ZL', 'ZL1Jets', 'ZL2Jets', 'ZL3Jets', 'ZL4Jets'])
        plot.Group('WJets'  , ['WJetsToLNu', 'W1JetsToLNu', 'W4JetsToLNu'])
        plot.Group('Single t', ['T_tWch', 'TBar_tWch', 'TToLeptons_sch', 'TToLeptons_tch'])
        if variable.name == 'mvis':
            plot.WriteDataCard(filename='datacard_mvis.root', dir='tt_' + cut.name, mode='UPDATE')

        HistDrawer.draw(plot, channel='#tau_{h}#tau_{h}')
        # HistDrawer.drawRatio(plot, channel='#tau_{h}#tau_{h}')
    
    