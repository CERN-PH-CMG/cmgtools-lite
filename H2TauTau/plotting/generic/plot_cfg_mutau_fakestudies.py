from numpy import array
import copy

from CMGTools.H2TauTau.proto.plotter.PlotConfigs import HistogramCfg, VariableCfg
from CMGTools.H2TauTau.proto.plotter.HistCreator import createHistogram
from CMGTools.H2TauTau.proto.plotter.HistDrawer import HistDrawer
from CMGTools.H2TauTau.proto.plotter.Variables import getVars, all_vars
from CMGTools.H2TauTau.proto.plotter.Samples import createSampleLists

from CMGTools.H2TauTau.proto.plotter.HistCreator import setSumWeights

from CMGTools.H2TauTau.proto.plotter.helper_methods import plotDataOverMCEff


# total_weight = 'weight * ' + getPUWeight()

only_stack = False

total_weight = 'weight/weight_njet/weight_vertex'
analysis_dir = '/data1/steggema/TauFRMuWeights/'
int_lumi = 2301.

samples_mc, samples_data, samples, all_samples, sampleDict = createSampleLists(analysis_dir=analysis_dir, channel='tau_fr', ztt_cut='(tau_gen_match == 5)', zl_cut='(tau_gen_match>=0 && tau_gen_match < 5)',
                      zj_cut='(tau_gen_match == 6 || tau_gen_match<0)')

cuts = {}

inc_cut = '!veto_dilepton && !veto_thirdlepton && !veto_otherlepton && muon_reliso05<0.1 && muon_muonid_medium>0.5 && muon_pt>19. && abs(jet_eta)<2.3'

samples = [s for s in all_samples if s.name != 'TBar_tWch' and not 'SUSY' in s.name]

samples_mc = [s for s in samples if s.name != 'data_obs']


for s in samples:
    if s.name not in ['ZTT1Jets', 'ZTT2Jets', 'ZTT3Jets', 'ZTT4Jets',
                               'ZJ1Jets', 'ZJ2Jets', 'ZJ3Jets', 'ZJ4Jets',
                               'ZL1Jets', 'ZL2Jets', 'ZL3Jets', 'ZL4Jets',]:
        ana_dir = s.ana_dir
        s.ana_dir = '/afs/cern.ch/user/s/steggema/work/public/mt/180216/'
        setSumWeights(s)
        s.ana_dir = ana_dir

# cuts['inclusive'] = inc_cut + ' && jet_pt > 20.'
# cuts['MTgr40_mupt30_metpt20'] = inc_cut + ' && puppimet_mt1>40 && jet_pt > 20. && muon_pt>30 && met_pt>20'

# cuts['MTgr40_mupt30_metpt20_jetup20'] = inc_cut + ' && puppimet_mt1>40 && jet_pt*(is_data + (1. - is_data)*jet_corrJECUp) > 20. && muon_pt>30 && met_pt>20'
cuts['MTgr40_mupt30_metpt20_nob'] = inc_cut + ' && puppimet_mt1>40 && jet_pt>20. && muon_pt>30 && met_pt>20 && nbjets20<0.5'
cuts['MTgr40_mupt30_metpt20_nob_noemu'] = inc_cut + ' && puppimet_mt1>40 && jet_pt>20. && muon_pt>30 && met_pt>20 && nbjets20<0.5 && jet_nooverlap'
# cuts['MTgr40_mupt30_metpt20_jetdown20'] = inc_cut + ' && puppimet_mt1>40 && jet_pt*(is_data + (1. - is_data)*jet_corrJECDown) > 20. && muon_pt>30 && met_pt>20'

# cuts['MTgr40_mupt30_metpt20_jet60'] = inc_cut + ' && puppimet_mt1>40 && jet_pt > 60. && muon_pt>30 && met_pt>20'
# cuts['MTgr40_mupt30_metpt20_jetup60'] = inc_cut + ' && puppimet_mt1>40 && jet_pt*(is_data + (1. - is_data)*jet_corrJECUp) > 60. && muon_pt>30 && met_pt>20'
# cuts['MTgr40_mupt30_metpt20_jetdown60'] = inc_cut + ' && puppimet_mt1>40 && jet_pt*(is_data + (1. - is_data)*jet_corrJECDown) > 60. && muon_pt>30 && met_pt>20'

# cuts['MTgr40_mupt30_metpt20_jetpt120'] = inc_cut + ' && puppimet_mt1>40 && jet_pt > 120. && muon_pt>30 && met_pt>20'
# cuts['MTgr40_mupt30_metpt20_leadingjet'] = inc_cut + ' && puppimet_mt1>40 && jet_pt > 20. && muon_pt>30 && met_pt>20 && jet_nth==0'

# cuts['MTgr40'] = inc_cut + ' && puppimet_mt1>40 && jet_pt > 20.'
# cuts['MTgr60'] = inc_cut + ' && puppimet_mt1>60 && jet_pt > 20.'
# cuts['MTgr40_noemu'] = inc_cut + ' && puppimet_mt1>40 && jet_pt > 20. && jet_nooverlap'

# cuts['MTgr40jetpt120'] = inc_cut + ' && puppimet_mt1>40 && jet_pt > 120.'

# cuts['MTgr40nobless2jets'] = inc_cut + ' && puppimet_mt1>40 && nbjets20==0 && njets30<2 && jet_pt > 20.'

# cuts['MTgr40_mupt30_metpt20_nobless2jets'] = inc_cut + ' && puppimet_mt1>40 && jet_pt >20. && muon_pt>30 && met_pt>20 && nbjets20==0 && n_jets<2'

# cuts['MTgr40gr1b'] = inc_cut + ' && puppimet_mt1>40 && nbjets20>=1 && jet_pt > 20.'
# cuts['MTgr40gr1b_noemu'] = inc_cut + ' && puppimet_mt1>40 && nbjets20>=1 && jet_pt > 20. && jet_nooverlap'

# cuts['MTgr40nobless2jetspt120'] = inc_cut + ' && puppimet_mt1>40 && nbjets20==0 && n_jets<2 && jet_pt > 120.'
# cuts['MTgr40nobless1jet'] = inc_cut + ' && puppimet_mt1>40 && nbjets20==0 && n_jets<1'


cut_names = [cut for cut in cuts]
# for cut in cut_names:
#     cuts[cut+'_plus'] = cuts[cut] + ' && muon_charge==1'
#     cuts[cut+'_minus'] = cuts[cut] + ' && muon_charge==-1'

qcd_from_same_sign = False

# Taken from Variables.py, can get subset with e.g. getVars(['mt', 'mvis'])
# variables = getVars(['jet_pt'])

variables = [
    VariableCfg(name='jet_pt', binning=array([20., 30., 40., 50., 60., 80., 100., 120., 140., 160., 180., 200., 250., 300., 350.]), unit='GeV', xtitle='jet p_{T}'),
    VariableCfg(name='tau_pt', binning=array([20., 30., 40., 50., 60., 80., 100., 120., 140., 160., 180., 200., 250., 300., 350.]), unit='GeV', xtitle='tau p_{T}'),
    VariableCfg(name='jet_eta', binning={'nbinsx':25, 'xmin':-2.5, 'xmax':2.5}, unit='', xtitle='jet #eta'),
    # VariableCfg(name='njets30', binning={'nbinsx':10, 'xmin':0.5, 'xmax':10.5}, unit='', xtitle='n_{jets}'),
    # VariableCfg(name='tau_chargedIsoPtSum', binning={'nbinsx':50, 'xmin':0., 'xmax':50.}, unit='', xtitle='charged isolation (GeV)'),
    # VariableCfg(name='tau_neutralIsoPtSum', binning={'nbinsx':50, 'xmin':0., 'xmax':50.}, unit='', xtitle='neutral isolation (GeV)'),
    # VariableCfg(name='tau_photonPtSumOutsideSignalCone', binning={'nbinsx':50, 'xmin':0., 'xmax':30.}, unit='', xtitle='tau photon p_{T} outer (GeV)'),
    VariableCfg(name='jet_pt_up', drawname='jet_pt*(is_data + (1. - is_data)*jet_corrJECUp)', binning=array([20., 30., 40., 50., 60., 80., 100., 120., 140., 160., 180., 200., 250., 300., 350.]), unit='GeV', xtitle='jet p_{T} up'),
    VariableCfg(name='jet_pt_down', drawname='jet_pt*(is_data + (1. - is_data)*jet_corrJECDown)', binning=array([20., 30., 40., 50., 60., 80., 100., 120., 140., 160., 180., 200., 250., 300., 350.]), unit='GeV', xtitle='jet p_{T} down'),    
    # # VariableCfg(name='n_jets', binning={'nbinsx':10, 'xmin':-0.5, 'xmax':9.5}, unit='', xtitle='n_{jets} (30 GeV, overlap removal)'),
    # VariableCfg(name='nbjets20', binning={'nbinsx':5, 'xmin':-0.5, 'xmax':4.5}, unit='', xtitle='n_{b jets} (20 GeV, no overlap removal)'),
    # VariableCfg(name='tau_gen_pdgId', binning={'nbinsx':40, 'xmin':-17.5, 'xmax':22.5}, unit=None, xtitle='tau gen match PDG ID'),
    # VariableCfg(name='tau_byIsolationMVA3oldDMwLT', binning={'nbinsx':10, 'xmin':-0.5, 'xmax':9.5}, unit=None, xtitle='MVA isolation'),
    
    # VariableCfg(name='tau_gen_match', binning={'nbinsx':7, 'xmin':-0.5, 'xmax':6.5}, unit=None, xtitle='tau gen match flag'),
]

# variables = [
#     VariableCfg(name='geninfo_htgen', binning={'nbinsx':400, 'xmin':0, 'xmax':800.}, unit='GeV', xtitle='HT gen'),
# ]

variables = [
    VariableCfg(name='jet_pt', binning=array([20., 30., 40., 50., 60., 80., 100., 120., 140., 160., 180., 200., 250., 300., 350.]), unit='GeV', xtitle='jet p_{T}'),
    VariableCfg(name='tau_dz', drawname='log(abs(tau_dz))', binning={'nbinsx':28, 'xmin':-10, 'xmax':4}, unit='log(cm)', xtitle='log(#Delta z tau)'),
    VariableCfg(name='tau_chargedIsoPtSum', binning={'nbinsx':50, 'xmin':0., 'xmax':50.}, unit='', xtitle='charged isolation (GeV)'),
    # VariableCfg(name='jet_eta', binning={'nbinsx':25, 'xmin':-2.5, 'xmax':2.5}, unit='', xtitle='jet #eta'),
    # VariableCfg(name='njets30', binning={'nbinsx':10, 'xmin':0.5, 'xmax':10.5}, unit='', xtitle='n_{jets}'),
    # VariableCfg(name='muon_pt', binning={'nbinsx':40, 'xmin':0., 'xmax':400.}, unit='GeV', xtitle='muon p_{T}'),
    # VariableCfg(name='muon_eta', binning={'nbinsx':25, 'xmin':-2.5, 'xmax':2.5}, unit='', xtitle='muon #eta'),
    # VariableCfg(name='muon_charge', binning={'nbinsx':3, 'xmin':-1.5, 'xmax':1.5}, unit='', xtitle='muon charge'),
    # VariableCfg(name='tau_puCorrPtSum', binning={'nbinsx':70, 'xmin':0., 'xmax':70.}, unit='GeV', xtitle='tau PU p_{T}'),
    # VariableCfg(name='tau_footprintCorrection', binning={'nbinsx':70, 'xmin':0., 'xmax':70.}, unit='GeV', xtitle='tau footprint correction p_{T}'),
    # VariableCfg(name='puppimet_mt1', binning={'nbinsx':40, 'xmin':0., 'xmax':300.}, unit='GeV', xtitle='m_{T} muon'),
    # VariableCfg(name='puppimet_mt2', binning={'nbinsx':40, 'xmin':0., 'xmax':300.}, unit='GeV', xtitle='m_{T} tau'),
    # VariableCfg(name='met_pt', binning={'nbinsx':40, 'xmin':0., 'xmax':300.}, unit='GeV', xtitle='PF MET p_{T}'),
    # VariableCfg(name='mvis', binning={'nbinsx':40, 'xmin':0., 'xmax':300.}, unit='GeV', xtitle='m(jet, muon)'),
    VariableCfg(name='n_vertices', binning={'nbinsx':40, 'xmin':-0.5, 'xmax':39.5}, unit=None, xtitle='N_{vertices}'),
]

# variables = [
#     VariableCfg(name='tau_byIsolationMVA3oldDMwLT', binning={'nbinsx':10, 'xmin':-0.5, 'xmax':9.5}, unit=None, xtitle='MVA isolation'),
#     VariableCfg(name='delta_phi_l1_l2', binning={'nbinsx':40, 'xmin':-3.141593, 'xmax':3.141593}, unit=None, xtitle='#Delta#Phi(muon, jet)'),
#     VariableCfg(name='mt_total', binning={'nbinsx':40, 'xmin':0., 'xmax':600.}, unit='GeV', xtitle='#M_{T} total'),
    # VariableCfg(name='n_vertices', binning={'nbinsx':40, 'xmin':-0.5, 'xmax':39.5}, unit=None, xtitle='N_{vertices}'),
# ]

# variables = [
#     VariableCfg(name='tau_chargedIsoPtSum', binning={'nbinsx':50, 'xmin':0., 'xmax':50.}, unit='', xtitle='charged isolation (GeV)'),
#     VariableCfg(name='tau_neutralIsoPtSum', binning={'nbinsx':50, 'xmin':0., 'xmax':50.}, unit='', xtitle='neutral isolation (GeV)'),
#     VariableCfg(name='tau_photonPtSumOutsideSignalCone', binning={'nbinsx':50, 'xmin':0., 'xmax':30.}, unit='', xtitle='tau photon p_{T} outer (GeV)'),
# ]


# variables = all_vars

signal_cuts = {
    # 'dbetatight':'&& tau_byCombinedIsolationDeltaBetaCorr3Hits>0.5',
    # 'dbetamedium':'&& tau_byCombinedIsolationDeltaBetaCorr3Hits>1.5',
    # 'dbetaloose':'&& tau_byCombinedIsolationDeltaBetaCorr3Hits>0.5',

    # 'dmonly_antimuloose_20':'&& tau_decayModeFinding>0.5 && tau_againstMuon3>0.5 && tau_pt>20.',
    # 'charged2gev_antimuloose_20':'&& tau_decayModeFinding>0.5 && tau_againstMuon3>0.5 && tau_chargedIsoPtSum<2. && tau_pt>20.',
    # 'neutral2gev_antimuloose_20':'&& tau_decayModeFinding>0.5 && tau_againstMuon3>0.5 && tau_neutralIsoPtSum-0.2*tau_puCorrPtSum<2. && tau_pt>20.',
    # 'dbetatight_antimuloose':'&& tau_decayModeFinding>0.5&& tau_byCombinedIsolationDeltaBetaCorr3Hits>0.5 && tau_againstMuon3>0.5',
    'dbetamedium_antimuloose_20':'&& tau_decayModeFinding>0.5&& tau_byCombinedIsolationDeltaBetaCorr3Hits>1.5 && tau_againstMuon3>0.5 && tau_pt>20.',
    # 'dbetamedium_antimuloose_antietight_20':'&& tau_decayModeFinding>0.5&& tau_byCombinedIsolationDeltaBetaCorr3Hits>1.5 && tau_againstMuon3>0.5 && tau_pt>20. && tau_againstElectronMVA6>2.5',
    # 'dbetaloose_antimuloose':'&& tau_decayModeFinding>0.5&& tau_byCombinedIsolationDeltaBetaCorr3Hits>0.5 && tau_againstMuon3>0.5',
    # 'mvaolddmvloose_antimuloose':'&& tau_decayModeFinding>0.5&& tau_byIsolationMVA3oldDMwLT>0.5 && tau_againstMuon3>0.5',
    # 'mvaolddmloose_antimuloose':'&& tau_decayModeFinding>0.5&& tau_byIsolationMVA3oldDMwLT>1.5 && tau_againstMuon3>0.5',
    # 'mvaolddmmedium_antimuloose':'&& tau_decayModeFinding>0.5&& tau_byIsolationMVA3oldDMwLT>2.5 && tau_againstMuon3>0.5',
    # 'mvaolddmtight_antimuloose':'&& tau_decayModeFinding>0.5&& tau_byIsolationMVA3oldDMwLT>3.5 && tau_againstMuon3>0.5',
    # 'mvaolddmvtight_antimuloose':'&& tau_decayModeFinding>0.5&& tau_byIsolationMVA3oldDMwLT>4.5 && tau_againstMuon3>0.5',
}


for cut_name in cuts:
    for signal_cut_name, signal_cut in signal_cuts.items():
        cfg_tight = HistogramCfg(name='tight'+cut_name+signal_cut_name, var=None, cfgs=samples_mc, cut=inc_cut, lumi=int_lumi, weight=total_weight + ' * ((tau_gen_match != 5) - (tau_gen_match == 5))')
        cfg_loose = HistogramCfg(name='loose'+cut_name+signal_cut_name, var=None, cfgs=samples_mc, cut=inc_cut, lumi=int_lumi, weight=total_weight + ' * ((tau_gen_match != 5) - (tau_gen_match == 5))')

        cfg_data_tight = HistogramCfg(name='tight_data'+cut_name+signal_cut_name, var=None, cfgs=samples, cut=inc_cut, lumi=int_lumi, weight=total_weight + ' * ((is_data) - (tau_gen_match == 5 || tau_gen_match ==1 || tau_gen_match == 2))')
        cfg_data_loose = HistogramCfg(name='loose_data'+cut_name+signal_cut_name, var=None, cfgs=samples, cut=inc_cut, lumi=int_lumi, weight=total_weight + ' * ((is_data) - (tau_gen_match == 5 || tau_gen_match ==1 || tau_gen_match == 2))')

        cfg_stack_tight = HistogramCfg(name='tight_stack'+cut_name+signal_cut_name, var=None, cfgs=samples, cut=inc_cut, lumi=int_lumi, weight=total_weight)
        cfg_stack_loose = HistogramCfg(name='loose_stack'+cut_name+signal_cut_name, var=None, cfgs=samples, cut=inc_cut, lumi=int_lumi, weight=total_weight)


        for variable in variables:
            cfg_tight.cut = cuts[cut_name] + signal_cut
            cfg_loose.cut = cuts[cut_name]
            cfg_data_tight.cut = cuts[cut_name] + signal_cut
            cfg_data_loose.cut = cuts[cut_name]
            cfg_stack_tight.cut = cuts[cut_name] + signal_cut
            cfg_stack_loose.cut = cuts[cut_name]

            if variable.name in ['jet_pt_up', 'jet_pt_down']:
                for cfg in [cfg_tight, cfg_loose, cfg_data_tight, cfg_data_loose, cfg_stack_tight, cfg_stack_loose]:
                    if variable.name == 'jet_pt_up':
                        cfg.cut = cfg.cut.replace('jet_pt', '(jet_pt*(is_data + (1. - is_data)*jet_corrJECUp))').replace('njets30', '(njets30*is_data + (1. - is_data)*njets30up)').replace('nbjets20', '(nbjets20*is_data + (1. - is_data)*nbjets20up)')
                    elif variable.name == 'jet_pt_down':
                        cfg.cut = cfg.cut.replace('jet_pt', '(jet_pt*(is_data + (1. - is_data)*jet_corrJECDown))').replace('njets30', '(njets30*is_data + (1. - is_data)*njets30down)').replace('nbjets20', '(nbjets20*is_data + (1. - is_data)*nbjets20down)')

            cfg_tight.var = variable
            cfg_loose.var = variable
            cfg_data_tight.var = variable
            cfg_data_loose.var = variable
            cfg_stack_tight.var = variable
            cfg_stack_loose.var = variable

            plot_stack_tight = createHistogram(cfg_stack_tight, verbose=True)
            plot_stack_loose = createHistogram(cfg_stack_loose, verbose=True)

            if not only_stack:
                       
                plot_tight = createHistogram(cfg_tight, verbose=True)
                plot_loose = createHistogram(cfg_loose, verbose=True)
                plot_data_tight = createHistogram(cfg_data_tight, verbose=True, all_stack=True)
                plot_data_loose = createHistogram(cfg_data_loose, verbose=True, all_stack=True)

            plots = [plot_stack_tight, plot_stack_loose] if only_stack else [plot_tight, plot_loose, plot_data_tight, plot_data_loose, plot_stack_tight, plot_stack_loose]

            for plot in plots:
                plot.Group('VV', ['VVTo2L2Nu', 'ZZTo2L2Q', 'WWTo1L1Nu2Q', 'WZTo1L3Nu', 'ZZTo4L', 'WZTo3L', 'WZTo2L2Q', 'WZTo1L1Nu2Q', 'T_tWch', 'TBar_tWch', 'TToLeptons_tch_powheg', 'TBarToLeptons_tch_powheg'])
                plot.Group('ZTT', ['ZTT', 'ZTT1Jets', 'ZTT2Jets', 'ZTT3Jets', 'ZTT4Jets'])
                plot.Group('ZJ', ['ZJ', 'ZJ1Jets', 'ZJ2Jets', 'ZJ3Jets', 'ZJ4Jets'])
                plot.Group('ZL', ['ZL', 'ZL1Jets', 'ZL2Jets', 'ZL3Jets', 'ZL4Jets'])

                plot.Group('W', ['W', 'WJetsToLNu_HT100to200', 'WJetsToLNu_HT200to400', 'WJetsToLNu_HT400to600', 'WJetsToLNu_HT600toInf'])

                # out_dir = 'fakeplots/'+cut_name if plot is plot_tight else 'fakeplots/loose'+cut_name
                # HistDrawer.draw(plot, plot_dir='fakeplots/'+cut_name)
        
            HistDrawer.draw(plot_stack_tight, plot_dir='fakeplots/stack_' + cut_name + signal_cut_name + '_tight')
            HistDrawer.draw(plot_stack_loose, plot_dir='fakeplots/stack_' + cut_name + signal_cut_name + '_loose')

            if only_stack:
                continue

            print '#### MC only tight'
            print plot_tight
            print '#### MC only loose'
            print plot_loose
            print '#### Data-MC only tight'
            print plot_data_tight
            print '#### Data-MC only loose'
            print plot_data_loose

            # import pdb; pdb.set_trace()
            def zeroOutNegBins(hist):
                for i_bin in xrange(0, hist.GetNbinsX()+2):
                    if hist.GetBinContent(i_bin) < 0.:
                        hist.SetBinContent(i_bin, 0.)

            for hist in [plot_tight.GetStack().totalHist.weighted, 
                         plot_loose.GetStack().totalHist.weighted, 
                         plot_data_tight.GetStack().totalHist.weighted, 
                         plot_data_loose.GetStack().totalHist.weighted]:
                zeroOutNegBins(hist)

            plotDataOverMCEff(plot_tight.GetStack().totalHist.weighted, 
                              plot_loose.GetStack().totalHist.weighted, 
                              plot_data_tight.GetStack().totalHist.weighted, 
                              plot_data_loose.GetStack().totalHist.weighted,
                              'fakeplots/fakerate_' + variable.name + cut_name + signal_cut_name + '.pdf')

