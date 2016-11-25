from numpy import array

from CMGTools.H2TauTau.proto.samples.spring16.htt_common import lumi, lumi_2016G

from CMGTools.H2TauTau.proto.plotter.PlotConfigs import HistogramCfg, VariableCfg
from CMGTools.H2TauTau.proto.plotter.categories_eMu import cat_Inc
from CMGTools.H2TauTau.proto.plotter.HistCreator import createHistograms
from CMGTools.H2TauTau.proto.plotter.HistDrawer import HistDrawer
from CMGTools.H2TauTau.proto.plotter.Variables import all_vars, emu_vars, getVars
from CMGTools.H2TauTau.proto.plotter.helper_methods import getPUWeight
from CMGTools.H2TauTau.proto.plotter.helper_methods import plotDataOverMCEff

from CMGTools.H2TauTau.proto.plotter.Samples import createSampleLists

from ROOT import gROOT

gROOT.SetBatch(True)

# total_weight = 'weight * ' + getPUWeight()
total_weight = 'weight'
data2016G = False

print total_weight

cuts = {}

inc_cut = '&&'.join([cat_Inc])


# cuts['inclusive'] = inc_cut + '&& l1_charge != l2_charge'
# cuts['inclusive_SS'] = inc_cut + '&& l1_charge == l2_charge'

# # # ttbar selections
# # cuts['1bjet'] = inc_cut + '&& l1_charge != l2_charge && n_bjets==1'
# cuts['1bjet_taudm'] = inc_cut + '&& l1_charge != l2_charge && n_bjets==1 && tau1_decayModeFinding>0.5'
# cuts['1bjet_taudm_mvaiso'] = inc_cut + '&& l1_charge != l2_charge && n_bjets==1 && tau1_decayModeFinding>0.5 && tau1_byIsolationMVArun2v1DBoldDMwLT>3.5'
# cuts['1bjet_taudm_dbiso'] = inc_cut + '&& l1_charge != l2_charge && n_bjets==1 && tau1_decayModeFinding>0.5 && tau1_byCombinedIsolationDeltaBetaCorr3Hits>2.5'

# cuts['1bjet_ljcentral_mvaiso'] = (
#     inc_cut + '&& l1_charge != l2_charge && n_bjets==1 && abs(jet1_eta)<2.4',
#     inc_cut + '&& l1_charge != l2_charge && n_bjets==1 && tau1_decayModeFinding>0.5 && tau1_byIsolationMVArun2v1DBoldDMwLT>2.5 && abs(jet1_eta)<2.4 && abs(TVector2::Phi_mpi_pi(jet1_phi - tau1_phi))<0.4 && abs(jet1_eta - tau1_eta)<0.4'
# )

# cuts['1bjet_ljcentral_dmtomvaiso'] = (
#     inc_cut + '&& l1_charge != l2_charge && n_bjets==1 && tau1_decayModeFinding>0.5 && abs(jet1_eta)<2.4',
#     inc_cut + '&& l1_charge != l2_charge && n_bjets==1 && tau1_decayModeFinding>0.5 && tau1_byIsolationMVArun2v1DBoldDMwLT>2.5 && abs(jet1_eta)<2.4 && abs(TVector2::Phi_mpi_pi(jet1_phi - tau1_phi))<0.4 && abs(jet1_eta - tau1_eta)<0.4'
# )


# cuts['1bjet_ljcentral_dbiso'] = (
#     inc_cut + '&& l1_charge != l2_charge && n_bjets==1  && abs(jet1_eta)<2.4',
#     inc_cut + '&& l1_charge != l2_charge && n_bjets==1 && tau1_decayModeFinding>0.5 && tau1_byCombinedIsolationDeltaBetaCorr3Hits>2.5 && abs(jet1_eta)<2.4 && abs(TVector2::Phi_mpi_pi(jet1_phi - tau1_phi))<0.4 && abs(jet1_eta - tau1_eta)<0.4'
# )

# cuts['1bjet_ljcentral_dm'] = (
#     inc_cut + '&& l1_charge != l2_charge && n_bjets==1 && abs(jet1_eta)<2.4',
#     inc_cut + '&& l1_charge != l2_charge && n_bjets==1 && tau1_decayModeFinding>0.5  && abs(jet1_eta)<2.4 && abs(TVector2::Phi_mpi_pi(jet1_phi - tau1_phi))<0.4 && abs(jet1_eta - tau1_eta)<0.4'
# )


not_the_tau = '&& ( (bjet1_pt>0 && (abs(TVector2::Phi_mpi_pi(bjet1_phi - tau1_phi))>0.4 || abs(bjet1_eta - tau1_eta) > 0.4) ) || (bjet2_pt>0 && (abs(TVector2::Phi_mpi_pi(bjet2_phi - tau1_phi))>0.4 || abs(bjet2_eta - tau1_eta) > 0.4) ))'

cuts['gr1bjet_notthetau_ljcentral_dmtomvaiso'] = (
    inc_cut + not_the_tau + '&& l1_charge != l2_charge && n_bjets>=1 && tau1_decayModeFinding>0.5 && abs(jet1_eta)<2.4',
    inc_cut + not_the_tau + '&& l1_charge != l2_charge && n_bjets>=1 && tau1_decayModeFinding>0.5 && tau1_byIsolationMVArun2v1DBoldDMwLT>2.5 && abs(jet1_eta)<2.4 && abs(TVector2::Phi_mpi_pi(jet1_phi - tau1_phi))<0.4 && abs(jet1_eta - tau1_eta)<0.4'
)

cuts['gr1bjet_notthetau_ljcentral_dmtodbiso'] = (
    inc_cut + not_the_tau + '&& l1_charge != l2_charge && n_bjets>=1 && tau1_decayModeFinding>0.5 && abs(jet1_eta)<2.4',
    inc_cut + not_the_tau + '&& l1_charge != l2_charge && n_bjets>=1 && tau1_decayModeFinding>0.5 && tau1_byCombinedIsolationDeltaBetaCorr3Hits>2.5 && abs(jet1_eta)<2.4 && abs(TVector2::Phi_mpi_pi(jet1_phi - tau1_phi))<0.4 && abs(jet1_eta - tau1_eta)<0.4'
)

cuts['gr1bjet_notthetau_ljcentral_dm'] = (
    inc_cut + '&& l1_charge != l2_charge && n_bjets>=1 && abs(jet1_eta)<2.4',
    inc_cut + not_the_tau + '&& l1_charge != l2_charge && n_bjets>=1 && tau1_decayModeFinding>0.5  && abs(jet1_eta)<2.4 && abs(TVector2::Phi_mpi_pi(jet1_phi - tau1_phi))<0.4 && abs(jet1_eta - tau1_eta)<0.4'
)

cuts['gr1bjet_notthetau_ljcentral_dmtomvaiso_2jets'] = (
    inc_cut + not_the_tau + '&& l1_charge != l2_charge && n_bjets>=1 && tau1_decayModeFinding>0.5 && abs(jet1_eta)<2.4 && n_jets<=2',
    inc_cut + not_the_tau + '&& l1_charge != l2_charge && n_bjets>=1 && tau1_decayModeFinding>0.5 && tau1_byIsolationMVArun2v1DBoldDMwLT>2.5 && abs(jet1_eta)<2.4 && abs(TVector2::Phi_mpi_pi(jet1_phi - tau1_phi))<0.4 && abs(jet1_eta - tau1_eta)<0.4 && n_jets<=2'
)

cuts['gr1bjet_notthetau_ljcentral_dmtodbiso_2jets'] = (
    inc_cut + not_the_tau + '&& l1_charge != l2_charge && n_bjets>=1 && tau1_decayModeFinding>0.5 && abs(jet1_eta)<2.4 && n_jets<=2',
    inc_cut + not_the_tau + '&& l1_charge != l2_charge && n_bjets>=1 && tau1_decayModeFinding>0.5 && tau1_byCombinedIsolationDeltaBetaCorr3Hits>2.5 && abs(jet1_eta)<2.4 && abs(TVector2::Phi_mpi_pi(jet1_phi - tau1_phi))<0.4 && abs(jet1_eta - tau1_eta)<0.4 && n_jets<=2'
)

cuts['gr1bjet_notthetau_ljcentral_dm_2jets'] = (
    inc_cut + '&& l1_charge != l2_charge && n_bjets>=1 && abs(jet1_eta)<2.4 && n_jets<=2',
    inc_cut + not_the_tau + '&& l1_charge != l2_charge && n_bjets>=1 && tau1_decayModeFinding>0.5  && abs(jet1_eta)<2.4 && abs(TVector2::Phi_mpi_pi(jet1_phi - tau1_phi))<0.4 && abs(jet1_eta - tau1_eta)<0.4 && n_jets<=2'
)

cuts['gr1bjet_notthetau_ljcentral_dmtomvaiso_gr3jets'] = (
    inc_cut + not_the_tau + '&& l1_charge != l2_charge && n_bjets>=1 && tau1_decayModeFinding>0.5 && abs(jet1_eta)<2.4 && n_jets>2',
    inc_cut + not_the_tau + '&& l1_charge != l2_charge && n_bjets>=1 && tau1_decayModeFinding>0.5 && tau1_byIsolationMVArun2v1DBoldDMwLT>2.5 && abs(jet1_eta)<2.4 && abs(TVector2::Phi_mpi_pi(jet1_phi - tau1_phi))<0.4 && abs(jet1_eta - tau1_eta)<0.4 && n_jets>2'
)

cuts['gr1bjet_notthetau_ljcentral_dmtodbiso_gr3jets'] = (
    inc_cut + not_the_tau + '&& l1_charge != l2_charge && n_bjets>=1 && tau1_decayModeFinding>0.5 && abs(jet1_eta)<2.4 && n_jets>2',
    inc_cut + not_the_tau + '&& l1_charge != l2_charge && n_bjets>=1 && tau1_decayModeFinding>0.5 && tau1_byCombinedIsolationDeltaBetaCorr3Hits>2.5 && abs(jet1_eta)<2.4 && abs(TVector2::Phi_mpi_pi(jet1_phi - tau1_phi))<0.4 && abs(jet1_eta - tau1_eta)<0.4 && n_jets>2'
)

cuts['gr1bjet_notthetau_ljcentral_dm_gr3jets'] = (
    inc_cut + '&& l1_charge != l2_charge && n_bjets>=1 && abs(jet1_eta)<2.4 && n_jets>2',
    inc_cut + not_the_tau + '&& l1_charge != l2_charge && n_bjets>=1 && tau1_decayModeFinding>0.5  && abs(jet1_eta)<2.4 && abs(TVector2::Phi_mpi_pi(jet1_phi - tau1_phi))<0.4 && abs(jet1_eta - tau1_eta)<0.4 && n_jets>2'
)

# cuts['1bjet_notthetau_mvaiso'] = (
#     inc_cut + '&& l1_charge != l2_charge && n_bjets==1 && tau1_decayModeFinding>0.5 && (abs(TVector2::Phi_mpi_pi(bjet1_phi - tau1_phi))>0.4 || abs(bjet1_eta - tau1_eta)>0.4)',
#     inc_cut + '&& l1_charge != l2_charge && n_bjets==1 && tau1_decayModeFinding>0.5 && (abs(TVector2::Phi_mpi_pi(bjet1_phi - tau1_phi))>0.4 || abs(bjet1_eta - tau1_eta)>0.4) && tau1_byIsolationMVArun2v1DBoldDMwLT>2.5',
# )
# cuts['1bjet_notthetau_dm'] = inc_cut + '&& l1_charge != l2_charge && n_bjets==1 && (abs(TVector2::Phi_mpi_pi(bjet1_phi - tau1_phi))>0.4 || abs(bjet1_eta - tau1_eta)>0.4) && tau1_decayModeFinding'
# cuts['1bjet_notthetau_dm_mvaiso'] = inc_cut + '&& l1_charge != l2_charge && n_bjets==1 && (abs(TVector2::Phi_mpi_pi(bjet1_phi - tau1_phi))>0.4 || abs(bjet1_eta - tau1_eta)>0.4) && tau1_decayModeFinding>0.5 && tau1_byIsolationMVArun2v1DBoldDMwLT>3.5'
# cuts['1bjet_notthetau_dm_dbiso'] = inc_cut + '&& l1_charge != l2_charge && n_bjets==1 && (abs(TVector2::Phi_mpi_pi(bjet1_phi - tau1_phi))>0.4 || abs(bjet1_eta - tau1_eta)>0.4) && tau1_decayModeFinding>0.5 && tau1_byCombinedIsolationDeltaBetaCorr3Hits>2.5'

# cuts['2bjets_notthetau_mvaiso'] = (
#     inc_cut + '&& l1_charge != l2_charge && n_bjets==2 && tau1_decayModeFinding>0.5&& (abs(TVector2::Phi_mpi_pi(bjet1_phi - tau1_phi))>0.4 || abs(bjet1_eta - tau1_eta)>0.4) && (abs(TVector2::Phi_mpi_pi(bjet2_phi - tau1_phi))>0.4 || abs(bjet2_eta - tau1_eta)>0.4)',
#     inc_cut + '&& l1_charge != l2_charge && n_bjets==2 && tau1_decayModeFinding>0.5&& (abs(TVector2::Phi_mpi_pi(bjet1_phi - tau1_phi))>0.4 || abs(bjet1_eta - tau1_eta)>0.4) && (abs(TVector2::Phi_mpi_pi(bjet2_phi - tau1_phi))>0.4 || abs(bjet2_eta - tau1_eta)>0.4)&& tau1_byIsolationMVArun2v1DBoldDMwLT>2.5'
# )


# cuts['inclusive_ljcentral_dm'] = (
#     inc_cut + '&& l1_charge != l2_charge && abs(jet1_eta)<2.4',
#     inc_cut + '&& l1_charge != l2_charge && tau1_decayModeFinding>0.5 && abs(jet1_eta)<2.4 && abs(TVector2::Phi_mpi_pi(jet1_phi - tau1_phi))<0.4 && abs(jet1_eta - tau1_eta)<0.4'
# )

# cuts['inclusive_ljcentral_mvaiso'] = (
#     inc_cut + '&& l1_charge != l2_charge && abs(jet1_eta)<2.4',
#     inc_cut + '&& l1_charge != l2_charge && tau1_decayModeFinding>0.5 && tau1_byIsolationMVArun2v1DBoldDMwLT>2.5 && abs(jet1_eta)<2.4 && abs(TVector2::Phi_mpi_pi(jet1_phi - tau1_phi))<0.4 && abs(jet1_eta - tau1_eta)<0.4'
# )

# cuts['inclusive_ljcentral_dmtomvaiso'] = (
#     inc_cut + '&& l1_charge != l2_charge && tau1_decayModeFinding>0.5 && abs(jet1_eta)<2.4',
#     inc_cut + '&& l1_charge != l2_charge && tau1_decayModeFinding>0.5 && tau1_byIsolationMVArun2v1DBoldDMwLT>2.5 && abs(jet1_eta)<2.4 && abs(TVector2::Phi_mpi_pi(jet1_phi - tau1_phi))<0.4 && abs(jet1_eta - tau1_eta)<0.4'
# )

cuts = cuts.copy()

for cut in cuts:
    print cut
    print cuts[cut]

analysis_dir = '/data1/steggema/em/06092016/MuEleRealMCPlusTau'

samples_mc, samples_data, samples, all_samples, sampleDict = createSampleLists(analysis_dir, channel='em',  ztt_cut='(l1_gen_match>2 && l2_gen_match>3)', zl_cut='l2_gen_match==99',zj_cut='l2_gen_match==99', data2016G=data2016G)


# Taken from Variables.py, can get subset with e.g. getVars(['mt', 'mvis'])
variables = emu_vars
variables = getVars(['tau1_eta', 'n_jets']) #'tau1_pt',
variables += [
    VariableCfg(name='jet1_pt', binning=array([30., 40., 50., 60., 80., 100., 120., 160.,  200., 350.]), unit='GeV', xtitle='jet p_{T}'),
    VariableCfg(name='tau1_pt', binning=array([30., 35., 40., 45., 50., 60., 80., 100., 140., 200.]), unit='GeV', xtitle='tau p_{T}'),
    VariableCfg(name='jet1_eta', binning={'nbinsx':10, 'xmin':-2.5, 'xmax':2.5}, unit='', xtitle='jet #eta'),
    VariableCfg(name='HT_jets', binning=array([0., 100., 200., 300., 500., 1000.]), unit='GeV', xtitle='#Sigma jet p_{T}')
]

for cut_name in cuts:
    cfg_tight = HistogramCfg(name='tight', var=None, cfgs=samples, cut=inc_cut, lumi=lumi, weight=total_weight+'*( (abs(tau1_gen_pdgId)!=15) - (abs(tau1_gen_pdgId)==15))')
    cfg_loose = HistogramCfg(name='loose', var=None, cfgs=samples, cut=inc_cut, lumi=lumi, weight=total_weight+'*( (abs(tau1_gen_pdgId)!=15) - (abs(tau1_gen_pdgId)==15))')
    cfg_tight_data = HistogramCfg(name='tight_data', var=None, cfgs=samples, cut=inc_cut, lumi=lumi, weight=total_weight+'*( (is_data>0.5) - (abs(tau1_gen_pdgId)==15))')
    cfg_loose_data = HistogramCfg(name='loose_data', var=None, cfgs=samples, cut=inc_cut, lumi=lumi, weight=total_weight+'*( (is_data>0.5) - (abs(tau1_gen_pdgId)==15))')
        
    
    cfg_tight.cut = cuts[cut_name][1]
    cfg_loose.cut = cuts[cut_name][0]
    cfg_tight_data.cut = cuts[cut_name][1]
    cfg_loose_data.cut = cuts[cut_name][0]


    for cfg in [cfg_tight, cfg_loose, cfg_tight_data, cfg_loose_data]:
        cfg.vars = variables

    plots_tight = createHistograms(cfg_tight, verbose=True)
    plots_loose = createHistograms(cfg_loose, verbose=True)
    plots_tight_data = createHistograms(cfg_tight_data, verbose=True, all_stack=True)
    plots_loose_data = createHistograms(cfg_loose_data, verbose=True, all_stack=True)
    for variable in variables:    
        plot_tight = plots_tight[variable.name]
        plot_loose = plots_loose[variable.name]
        plot_tight_data = plots_tight_data[variable.name]
        plot_loose_data = plots_loose_data[variable.name]
        for plot in [plot_tight, plot_loose, plot_tight_data, plot_loose_data]:
            plot.Group('VV', ['WWTo1L1Nu2Q', 'WZTo1L1Nu2Q', 'WZTo1L3Nu', 'WZTo2L2Q', 'VVTo2L2Nu', 'ZZTo2L2Q', 'ZZTo4L'])
            plot.Group('Single t', ['T_tWch', 'TBar_tWch', 'TBarToLeptons_tch_powheg', 'TToLeptons_tch_powheg'])
            plot.Group('ZLL', ['ZL', 'ZJ'], style=plot.Hist('ZL').style)
            plot.Group('W', ['W1Jets', 'W2Jets', 'W3Jets', 'W4Jets'])
            plot.Group('Electroweak', ['W', 'VV', 'Single t'])
            # HistDrawer.draw(plot, plot_dir='plotsG/'+cut_name, channel='#mu#mu')
        
        base_dir = 'fakeplotsG' if data2016G else 'fakeplots'
        plotDataOverMCEff(plot_tight.GetStack().totalHist.weighted, 
                          plot_loose.GetStack().totalHist.weighted, 
                          plot_tight_data.GetStack().totalHist.weighted, 
                          plot_loose_data.GetStack().totalHist.weighted,
                          base_dir+'_dm/fakerate_' + variable.name + cut_name + '.pdf')
