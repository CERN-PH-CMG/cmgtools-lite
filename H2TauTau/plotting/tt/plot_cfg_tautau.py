from collections import namedtuple
from operator import itemgetter

from CMGTools.H2TauTau.proto.samples.summer16.htt_common import lumi
from CMGTools.H2TauTau.proto.plotter.PlotConfigs import SampleCfg, HistogramCfg, VariableCfg
from CMGTools.H2TauTau.proto.plotter.categories_TauTau import inc_sig_tau1_iso, inc_sig_tau2_iso, inc_sig_no_iso
from CMGTools.H2TauTau.proto.plotter.categories_common import cat_J1, cat_VBF
from CMGTools.H2TauTau.proto.plotter.HistCreator import createHistograms, createTrees
from CMGTools.H2TauTau.proto.plotter.HistDrawer import HistDrawer
from CMGTools.H2TauTau.proto.plotter.Variables import tautau_vars, getVars
from CMGTools.H2TauTau.proto.plotter.Samples import createSampleLists
from CMGTools.H2TauTau.proto.plotter.qcdEstimation import qcd_estimation
from CMGTools.H2TauTau.proto.plotter.cut import Cut
from CMGTools.H2TauTau.proto.plotter.metrics import ams_hists_rebin

MyCut = namedtuple('MyCut', ['name', 'cut'])

inc_sig_no_iso = inc_sig_no_iso & Cut('Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_goodVertices && Flag_eeBadScFilter && Flag_globalTightHalo2016Filter && passBadMuonFilter && passBadChargedHadronFilter && badMuonMoriond2017 && badCloneMuonMoriond2017')

def prepareCuts(mode):
    cuts = []

    # categories, do not include charge and iso cuts
    inc_cut = inc_sig_no_iso
    jet1_cut = inc_sig_no_iso & Cut(cat_J1)
    vbf_cut = inc_sig_no_iso & Cut(cat_VBF)

    # append categories to plot
    if mode == 'control':
        # cuts.append(MyCut('inclusive', inc_cut & Cut('n_bjets==0')))
        # cuts.append(MyCut('dilpt50', inc_cut & Cut('n_bjets==0 && dil_pt>50')))

        cuts.append(MyCut('2bjet', inc_cut & Cut('n_bjets>=2')))
        cuts.append(MyCut('gr1bjet', inc_cut & Cut('n_bjets>=1')))

        # cuts.append(MyCut('sm_dysel_new_mz', inc_cut & Cut('n_bjets==0 && n_jets>=1 && l1_pt>50 && l2_pt>40 && abs(l1_eta - l2_eta)<1. && pzeta_vis>60. && mvis<100')))
        # cuts.append(MyCut('sm_dysel_ptgr100_mz', inc_cut & Cut('n_bjets==0 && n_jets>=1 && l1_pt>100 && l2_pt>40 && abs(l1_eta - l2_eta)<1. && pzeta_vis>60. && mvis<100')))

        # cuts.append(MyCut('sm_dysel_new', inc_cut & Cut('n_bjets==0 && n_jets>=1 && l1_pt>50 && l2_pt>40 && abs(l1_eta - l2_eta)<1. && pzeta_vis>60.')))
        # cuts.append(MyCut('sm_dysel_ptgr100', inc_cut & Cut('n_bjets==0 && n_jets>=1 && l1_pt>100 && l2_pt>40 && abs(l1_eta - l2_eta)<1. && pzeta_vis>60.')))
        # cuts.append(MyCut('sm_dysel_ptgr200', inc_cut & Cut('n_bjets==0 && n_jets>=1 && l1_pt>200 && l2_pt>40 && abs(l1_eta - l2_eta)<1. && pzeta_vis>60.')))
        # cuts.append(MyCut('sm_dysel_pt150_200', inc_cut & Cut('n_bjets==0 && n_jets>=1 && l1_pt>150 && l1_pt<200 && l2_pt>40 && abs(l1_eta - l2_eta)<1. && pzeta_vis>60.')))
        # cuts.append(MyCut('sm_dysel_pt100_150', inc_cut & Cut('n_bjets==0 && n_jets>=1 && l1_pt>100 && l1_pt<150 && l2_pt>40 && abs(l1_eta - l2_eta)<1. && pzeta_vis>60.')))
        # cuts.append(MyCut('sm_dysel_pt80_100', inc_cut & Cut('n_bjets==0 && n_jets>=1 && l1_pt>80 && l1_pt<100 && l2_pt>40 && abs(l1_eta - l2_eta)<1. && pzeta_vis>60.')))
        # cuts.append(MyCut('sm_dysel_pt50_80', inc_cut & Cut('n_bjets==0 && n_jets>=1 && l1_pt>50 && l1_pt<80 && l2_pt>40 && abs(l1_eta - l2_eta)<1. && pzeta_vis>60.')))

        # cuts.append(MyCut('inclusive_SS', inc_cut))
        # cuts.append(MyCut('mZ', inc_cut & Cut('mvis < 110.')))
        # cuts.append(MyCut('low_deta', inc_cut & Cut('delta_eta_l1_l2 < 1.5')))
        # cuts.append(MyCut('high_deta', inc_cut & Cut('delta_eta_l1_l2 > 1.5')))

        # cuts.append(MyCut('mZ_0jet', inc_cut & Cut('mvis < 110. && n_jets==0')))
        # cuts.append(MyCut('mZ_1jet', inc_cut & Cut('mvis < 110. && n_jets>=1')))
        # Next is a failed attempt to get a W+jets-enriched control region
        # cuts.append(MyCut('mva_met_sig_1_low_deta', inc_cut & Cut('met_pt/sqrt(met_cov00 + met_cov11) > 1. && delta_eta_l1_l2 < 2.')))

    if mode == 'mssm':
        cuts.append(MyCut('nobtag', inc_cut & Cut('n_bjets==0')))
        cuts.append(MyCut('inclusive', inc_cut & Cut('1')))
        cuts.append(MyCut('btag', inc_cut & Cut('n_bjets==1 && n_jets<=1')))
        # cuts.append(MyCut('1bjet', inc_cut & Cut('n_bjets==1')))
        # # cuts.append(MyCut('0jet', inc_cut & Cut('n_bjets==1 && n_jets==0')))

        # # cuts.append(MyCut('inclusive_largedphi', inc_cut & Cut('n_bjets==0 && abs(TVector2::Phi_mpi_pi(l1_phi - l2_phi))>1.5')))
        # cuts.append(MyCut('inclusive_tau1pt60', inc_cut & Cut('n_bjets==0 && l1_pt>60')))
        # cuts.append(MyCut('inclusive_tau1ptl60', inc_cut & Cut('n_bjets==0 && l1_pt<60')))
        # cuts.append(MyCut('inclusive_tau1pt75', inc_cut & Cut('n_bjets==0 && l1_pt>75')))
        # cuts.append(MyCut('inclusive_tau1ptl75', inc_cut & Cut('n_bjets==0 && l1_pt<75')))
        # cuts.append(MyCut('inclusive_tau1pt100', inc_cut & Cut('n_bjets==0 && l1_pt>100')))
        # cuts.append(MyCut('inclusive_tau1ptl100', inc_cut & Cut('n_bjets==0 && l1_pt<100')))
        # cuts.append(MyCut('inclusive_tau1pt150', inc_cut & Cut('n_bjets==0 && l1_pt>150')))
        # cuts.append(MyCut('inclusive_tau1ptl150', inc_cut & Cut('n_bjets==0 && l1_pt<150')))
        # cuts.append(MyCut('inclusive_lowdphimetl2', inc_cut & Cut('n_bjets==0 && abs(TVector2::Phi_mpi_pi(l2_phi-met_phi))<0.5')))
        # cuts.append(MyCut('inclusive_lowdphimetl2_highdphimetl1', inc_cut & Cut('n_bjets==0 && abs(TVector2::Phi_mpi_pi(l2_phi-met_phi))<0.5 && abs(TVector2::Phi_mpi_pi(l1_phi-met_phi))>2')))
        
        # cuts.append(MyCut('inclusive_mttotal300', inc_cut & Cut('n_bjets==0 && mt_total>300')))


    if mode == 'sm':
        cuts.append(MyCut('sm_1jet', inc_cut & Cut('n_bjets==0 && n_jets>=1 && l1_pt>50 && l2_pt>40')))
        cuts.append(MyCut('sm_0jet', inc_cut & Cut('n_bjets==0 && n_jets==0 && l1_pt>50 && l2_pt>40')))
        cuts.append(MyCut('1jet', jet1_cut)) # with VBF veto
        cuts.append(MyCut('vbf', vbf_cut))


    if mode == 'susy':
        # cuts.append(MyCut('mva_met_sig_3', inc_cut & Cut('met_pt/sqrt(met_cov00 + met_cov11) > 3.')))

        # cuts.append(MyCut('met200', inc_cut & Cut('met_pt > 200.')))


        # cuts.append(MyCut('susy_loose_met', inc_cut & Cut('mvis>100 && n_bjets==0 && met_pt>100.')))
        # cuts.append(MyCut('susy_loose', inc_cut & Cut('mvis>100 && n_bjets==0 && pzeta_disc < -40.')))

        # cuts.append(MyCut('susy_mtsum200', inc_cut & Cut('n_bjets==0 && mt + mt_leg2>200.')))
        # cuts.append(MyCut('susy_highmva', inc_cut & Cut('n_bjets==0 && mva1>0.75')))

        # cuts.append(MyCut('susy_mva_mtsum200_mt2_20', inc_cut & Cut('n_bjets==0 && mt2>20 && mt + mt_leg2>200. && mva1>0.85')))
        # cuts.append(MyCut('susy_mva2_mtsum200_mt2_20', inc_cut & Cut('n_bjets==0 && mt2>20 && mt + mt_leg2>200. && mva1>0.90')))
        # cuts.append(MyCut('susy_mva3_mtsum200_mt2_20', inc_cut & Cut('n_bjets==0 && mt2>20 && mt + mt_leg2>200. && mva1>0.95')))
        # cuts.append(MyCut('susy_mtsum200_mt2_20', inc_cut & Cut('n_bjets==0 && mt2>20 && mt + mt_leg2>200.')))

        # cuts.append(MyCut('pieter_1', inc_cut & Cut('n_bjets==0 && mt2>90. && abs(TVector2::Phi_mpi_pi(l1_phi - l2_phi))>1.5')))
        # cuts.append(MyCut('pieter_2', inc_cut & Cut('n_bjets==0 && mt2>40. && mt2<90. && mt2>40. && abs(TVector2::Phi_mpi_pi(l1_phi - l2_phi))>1.5 && mt + mt_leg2>300. && mt + mt_leg2<300. ')))
        # cuts.append(MyCut('pieter_3', inc_cut & Cut('n_bjets==0 && mt2>40. && mt2<90. && mt2>40. && abs(TVector2::Phi_mpi_pi(l1_phi - l2_phi))>1.5 && mt + mt_leg2>350.')))

        # cuts.append(MyCut('maryam_incl', inc_cut & Cut('n_bjets==0 && mt2>20. && mvis>85. && pfmet_pt>30.')))
        
        # cuts.append(MyCut('maryam_1', inc_cut & Cut('n_bjets==0 && mt2>90. && mvis>85. && pfmet_pt>30.')))
        # cuts.append(MyCut('maryam_1_0jet', inc_cut & Cut('n_bjets==0 && mt2>90. && mvis>85. && pfmet_pt>30. && n_jets==0')))
        # cuts.append(MyCut('maryam_1_1jet', inc_cut & Cut('n_bjets==0 && mt2>90. && mvis>85. && pfmet_pt>30. && n_jets>=1')))

        # cuts.append(MyCut('maryam_1_SS', inc_cut & Cut('n_bjets==0 && mt2>90. && mvis>85. && pfmet_pt>30.')))
        # cuts.append(MyCut('maryam_1_0jet_SS', inc_cut & Cut('n_bjets==0 && mt2>90. && mvis>85. && pfmet_pt>30. && n_jets==0')))
        # cuts.append(MyCut('maryam_1_1jet_SS', inc_cut & Cut('n_bjets==0 && mt2>90. && mvis>85. && pfmet_pt>30. && n_jets>=1')))


        cuts.append(MyCut('maryam_1_mt2sideband_1jet', inc_cut & Cut('n_bjets==0 && mt2>75. && mt2<90. && mvis>85. && pfmet_pt>30. && n_jets>=1')))
        cuts.append(MyCut('maryam_1_mt2sideband_1jet_SS', inc_cut & Cut('n_bjets==0 && mt2>75. && mt2<90. && mvis>85. && pfmet_pt>30. && n_jets>=1')))

        # cuts.append(MyCut('maryam_1_tight', inc_cut & Cut('n_bjets==0 && mt2>90. && mvis>85. && pfmet_pt>30. && l1_pt>100.')))
        # cuts.append(MyCut('maryam_1_tight_1jet', inc_cut & Cut('n_bjets==0 && mt2>90. && mvis>85. && pfmet_pt>30. && l1_pt>100. && n_jets>=1')))
        # cuts.append(MyCut('maryam_1_tight_0jet', inc_cut & Cut('n_bjets==0 && mt2>90. && mvis>85. && pfmet_pt>30. && l1_pt>100. && n_jets==0')))
        # cuts.append(MyCut('maryam_2', inc_cut & Cut('n_bjets==0 && mt2<90. && mvis>85. && pfmet_pt>30. && mt + mt_leg2 > 250. && l1_pt>100.')))

        # cuts.append(MyCut('susy_onlytaupt', inc_cut & Cut('mvis>100 && n_bjets==0 && l1_pt>60 && met_pt>20.')))
        # cuts.append(MyCut('susy_taupt', inc_cut & Cut('mvis>100 && n_bjets==0 && l1_pt>60 && met_pt>20. && mt>50.')))
        # cuts.append(MyCut('susy_taupt_pzetamet', inc_cut & Cut(
        #     'mvis>100 && n_bjets==0 && l1_pt>60 && met_pt>20. && mt>50. && pzeta_met<-50. && delta_eta_l1_l2<3. && (min(abs(TVector2::Phi_mpi_pi(met_phi - jet2_phi)) + 20*(jet2_phi<-50), abs(TVector2::Phi_mpi_pi(met_phi - jet1_phi))+ 20*(jet1_phi<-50)) > 0.8 || jet1_pt<30.)')))
        # cuts.append(MyCut('susy_jan_opt', inc_cut & Cut('met_pt/sqrt(met_cov00 + met_cov11) > 2. && mvis>100 && mt + mt_leg2 > 200. && n_bjets==0 && pzeta_disc < -40.')))
        # cuts.append(MyCut('susy_jan_tight', inc_cut & Cut(
        #     'met_pt/sqrt(met_cov00 + met_cov11) > 1. && mvis>100 && mt + mt_leg2 > 150. && n_bjets==0 && pzeta_disc < -40. && abs(abs(TVector2::Phi_mpi_pi(l1_phi - l2_phi))) > 1. && mt_total>300.')))

        # cuts.append(MyCut('susy_onlytaupt_0jet', inc_cut & Cut('mvis>100 && n_bjets==0 && l1_pt>60 && met_pt>20. && n_jets==0')))
        # cuts.append(MyCut('susy_taupt_0jet', inc_cut & Cut('mvis>100 && n_bjets==0 && l1_pt>60 && met_pt>20. && mt>50. && n_jets==0')))
        # cuts.append(MyCut('susy_taupt_pzetamet_0jet', inc_cut & Cut(
        #     'mvis>100 && n_bjets==0 && l1_pt>60 && met_pt>20. && mt>50. && pzeta_met<-50. && delta_eta_l1_l2<3. && (min(abs(TVector2::Phi_mpi_pi(met_phi - jet2_phi)) + 20*(jet2_phi<-50), abs(TVector2::Phi_mpi_pi(met_phi - jet1_phi))+ 20*(jet1_phi<-50)) > 0.8 || jet1_pt<30.) && n_jets==0')))
        # cuts.append(MyCut('susy_jan_opt_0jet', inc_cut & Cut('met_pt/sqrt(met_cov00 + met_cov11) > 2. && mvis>100 && mt + mt_leg2 > 200. && n_bjets==0 && pzeta_disc < -40. && n_jets==0')))
        # cuts.append(MyCut('susy_jan_tight_0jet', inc_cut & Cut(
        #     'met_pt/sqrt(met_cov00 + met_cov11) > 1. && mvis>100 && mt + mt_leg2 > 150. && n_bjets==0 && pzeta_disc < -40. && abs(abs(TVector2::Phi_mpi_pi(l1_phi - l2_phi))) > 1. && mt_total>300. && n_jets==0')))


        # cuts.append(MyCut('susy_onlytaupt_gr1jet', inc_cut & Cut('mvis>100 && n_bjets==0 && l1_pt>60 && met_pt>20. && n_jets>0')))
        # cuts.append(MyCut('susy_taupt_gr1jet', inc_cut & Cut('mvis>100 && n_bjets==0 && l1_pt>60 && met_pt>20. && mt>50. && n_jets>0')))
        # cuts.append(MyCut('susy_taupt_pzetamet_gr1jet', inc_cut & Cut(
        #     'mvis>100 && n_bjets==0 && l1_pt>60 && met_pt>20. && mt>50. && pzeta_met<-50. && delta_eta_l1_l2<3. && (min(abs(TVector2::Phi_mpi_pi(met_phi - jet2_phi)) + 20*(jet2_phi<-50), abs(TVector2::Phi_mpi_pi(met_phi - jet1_phi))+ 20*(jet1_phi<-50)) > 0.8 || jet1_pt<30.) && n_jets>0')))
        # cuts.append(MyCut('susy_jan_opt_gr1jet', inc_cut & Cut(
        #     'met_pt/sqrt(met_cov00 + met_cov11) > 2. && mvis>100 && mt + mt_leg2 > 200. && n_bjets==0 && pzeta_disc < -40. && n_jets>0')))
        # cuts.append(MyCut('susy_jan_tight_gr1jet', inc_cut & Cut(
        #     'met_pt/sqrt(met_cov00 + met_cov11) > 1. && mvis>100 && mt + mt_leg2 > 150. && n_bjets==0 && pzeta_disc < -40. && abs(abs(TVector2::Phi_mpi_pi(l1_phi - l2_phi))) > 1. && mt_total>300. && n_jets>0')))

        # cuts.append(MyCut('susy_jan_nomet', inc_cut & Cut('mvis>100 && n_bjets==0 && mt + mt_leg2 > 150.')))

    return cuts

    # if optimisation:
    #     cuts = []
    #     met_sig_cuts = [2, 3]
    #     # met_sig_cuts = [1]
    #     sum_mt_cuts = [0, 50, 100, 150, 200, 250]
    #     # pzeta_disc_cuts = [-40, 0, 1000]
    #     pzeta_disc_cuts = [-40, 1000]

    #     for met_sig_cut in met_sig_cuts:
    #         for sum_mt_cut in sum_mt_cuts:
    #             for pzeta_cut in pzeta_disc_cuts:
    #                 cut_name = 'susy_jan_{c1}_{c2}_{c3}'.format(c1=met_sig_cut, c2=sum_mt_cut, c3=pzeta_cut)
    #                 cut = 'met_pt/sqrt(met_cov00 + met_cov11) > {met_sig_cut} && mvis>100 && mt + mt_leg2 > {sum_mt_cut} && n_bjets==0 && pzeta_disc < {pzeta_disc_cut}'.format(met_sig_cut=met_sig_cut, sum_mt_cut=sum_mt_cut, pzeta_disc_cut=pzeta_cut)
    #                 cuts.append(MyCut(cut_name, inc_cut & cut))


    # cuts.append(MyCut('susy_jan_SS', inc_cut & Cut('met_pt/sqrt(met_cov00 + met_cov11) > 1. && mvis>100 && mt + mt_leg2 > 150. && n_bjets==0 && pzeta_disc < -40.')))

    

def getVariables(mode):
    # Taken from Variables.py, can get subset with e.g. getVars(['mt', 'mvis'])
    # variables = tautau_vars
    if mode == 'control':
        variables = getVars(['_norm_', 'mvis', 'mt2', 'l1_pt', 'l2_pt', 'delta_phi_l1_l2', 'delta_eta_l1_l2', 'met_pt', 'mt_total', 'mt_total_mssm', 'mt_sum', 'pzeta_met', 'l2_mt', 'mt', 'pzeta_vis', 'pzeta_disc', 'pthiggs', 'jet1_pt', 'n_jets', 'dil_pt', 'l1_byCombinedIsolationDeltaBetaCorrRaw3Hits', 'l1_byIsolationMVArun2v1DBoldDMwLTraw', 'l1_dz_sig', 'l1_log_dz', 'l1_dxy_sig', 'l1_log_dxy', 'l1_decayMode', 'l1_chargedIsoPtSum', 'l1_neutralIsoPtSum', 'l1_puCorrPtSum', 'l1_photonPtSumOutsideSignalCone', 'l1_zImpact', 'l1_jet_charge', 'l1_jet_pt_div_l1_pt'], channel='tautau')
    if mode == 'mssm':
        variables = getVars(['mt_total', 'mt_total_mssm', 'mt_total_mssm_fine', 'mvis_extended', 'l1_pt', 'dil_pt'], channel='tautau')
    # variables += [
    #     VariableCfg(name='mt2', binning={'nbinsx':15, 'xmin':0., 'xmax':150.}, unit='GeV', xtitle='m_{T2}')
    # ]
    if mode == 'mva':
        variables += getVars(['_norm_'])
        variables += [
            VariableCfg(name='mva1', binning={'nbinsx':10, 'xmin':0., 'xmax':1.}, unit='', xtitle='Stau MVA')
        ]

    if mode == 'susy':
        variables = getVars(['l1_pt', '_norm_', 'l2_pt', 'mt2', 'mt', 'mt_leg2', 'mt_total_mssm', 'min_delta_phi_tau1tau2_met'], channel='tautau')

    return variables



def createSamples(mode, analysis_dir, optimisation=False):
    samples_mc, samples_data, samples, all_samples, sampleDict = createSampleLists(analysis_dir=analysis_dir, channel='tt', mode=mode, ztt_cut='(l2_gen_match == 5 && l1_gen_match == 5)', zl_cut='(l1_gen_match < 6 && l2_gen_match < 6 && !(l1_gen_match == 5 && l2_gen_match == 5))',
                                                                                   zj_cut='(l2_gen_match == 6 || l1_gen_match == 6)', signal_scale=1. if optimisation else 20.)
    return all_samples, samples


def makePlots(variables, cuts, total_weight, all_samples, samples, friend_func, mode='control', dc_postfix='', make_plots=True, optimisation=False):
    sample_names = set()
    ams_dict = {}

    from CMGTools.H2TauTau.proto.plotter.cut import Cut

    # def_iso_cut = inc_sig_tau1_iso & inc_sig_tau2_iso
    iso_cuts = {
        # 'vvtight':(Cut('l1_byIsolationMVArun2v1DBoldDMwLT>5.5') & Cut('l2_byIsolationMVArun2v1DBoldDMwLT>5.5'), Cut('l1_byIsolationMVArun2v1DBoldDMwLT>3.5') & Cut('l2_byIsolationMVArun2v1DBoldDMwLT>3.5')),
        'vtight_relax2nd':(Cut('l1_byIsolationMVArun2v1DBoldDMwLT>4.5') & Cut('l2_byIsolationMVArun2v1DBoldDMwLT>4.5'), Cut('l1_byIsolationMVArun2v1DBoldDMwLT>4.5') & Cut('l2_byIsolationMVArun2v1DBoldDMwLT>2.5')),
        'loose_not_vtight':(Cut('l1_byIsolationMVArun2v1DBoldDMwLT>1.5 && l1_byIsolationMVArun2v1DBoldDMwLT<4.5') & Cut('l2_byIsolationMVArun2v1DBoldDMwLT>1.5&&l2_byIsolationMVArun2v1DBoldDMwLT<4.5'), Cut('l1_byIsolationMVArun2v1DBoldDMwLT<1.5 && l1_byIsolationMVArun2v1DBoldDMwLT>0.5') & Cut('l2_byIsolationMVArun2v1DBoldDMwLT<1.5 && l2_byIsolationMVArun2v1DBoldDMwLT>0.5')),
        'one_loose_other_vtight':(Cut('(l1_byIsolationMVArun2v1DBoldDMwLT>4.5 && (l2_byIsolationMVArun2v1DBoldDMwLT>1.5&&l2_byIsolationMVArun2v1DBoldDMwLT<4.5)) || (l2_byIsolationMVArun2v1DBoldDMwLT>4.5 && (l1_byIsolationMVArun2v1DBoldDMwLT>1.5&&l1_byIsolationMVArun2v1DBoldDMwLT<4.5)) '), Cut('l1_byIsolationMVArun2v1DBoldDMwLT<1.5 && l1_byIsolationMVArun2v1DBoldDMwLT>0.5') & Cut('l2_byIsolationMVArun2v1DBoldDMwLT<1.5 && l2_byIsolationMVArun2v1DBoldDMwLT>0.5')),
        # 'vtight':(Cut('l1_byIsolationMVArun2v1DBoldDMwLT>4.5') & Cut('l2_byIsolationMVArun2v1DBoldDMwLT>4.5'), Cut('l1_byIsolationMVArun2v1DBoldDMwLT>2.5') & Cut('l2_byIsolationMVArun2v1DBoldDMwLT>2.5')),
        # 'tight':(Cut('l1_byIsolationMVArun2v1DBoldDMwLT>3.5') & Cut('l2_byIsolationMVArun2v1DBoldDMwLT>3.5'), Cut('l1_byIsolationMVArun2v1DBoldDMwLT>3.5') & Cut('l2_byIsolationMVArun2v1DBoldDMwLT>1.5')),
        # 'medium':(Cut('l1_byIsolationMVArun2v1DBoldDMwLT>2.5') & Cut('l2_byIsolationMVArun2v1DBoldDMwLT>2.5'), Cut('l1_byIsolationMVArun2v1DBoldDMwLT>0.5') & Cut('l2_byIsolationMVArun2v1DBoldDMwLT>0.5')),
        # 'loose':(Cut('l1_byIsolationMVArun2v1DBoldDMwLT>1.5') & Cut('l2_byIsolationMVArun2v1DBoldDMwLT>1.5'), Cut('1')),
        # 'vloose':(Cut('l1_byIsolationMVArun2v1DBoldDMwLT>0.5') & Cut('l2_byIsolationMVArun2v1DBoldDMwLT>0.5'), Cut('1')),
    }

    # iso_cuts = {
    #     'l1_vvtight':(Cut('l1_byIsolationMVArun2v1DBoldDMwLT>5.5') & Cut('l2_byIsolationMVArun2v1DBoldDMwLT>4.5'), Cut('l1_byIsolationMVArun2v1DBoldDMwLT>5.5') & Cut('l2_byIsolationMVArun2v1DBoldDMwLT>3.5')),
    #     'l1_vtight':(Cut('l1_byIsolationMVArun2v1DBoldDMwLT>4.5') & Cut('l2_byIsolationMVArun2v1DBoldDMwLT>4.5'), Cut('l1_byIsolationMVArun2v1DBoldDMwLT>4.5') & Cut('l2_byIsolationMVArun2v1DBoldDMwLT>2.5')),
    #     'l1_tight':(Cut('l1_byIsolationMVArun2v1DBoldDMwLT>3.5') & Cut('l2_byIsolationMVArun2v1DBoldDMwLT>4.5'), Cut('l1_byIsolationMVArun2v1DBoldDMwLT>3.5') & Cut('l2_byIsolationMVArun2v1DBoldDMwLT>1.5')),
    #     'l1_medium':(Cut('l1_byIsolationMVArun2v1DBoldDMwLT>2.5') & Cut('l2_byIsolationMVArun2v1DBoldDMwLT>4.5'), Cut('l1_byIsolationMVArun2v1DBoldDMwLT>2.5') & Cut('l2_byIsolationMVArun2v1DBoldDMwLT>0.5')),
    #     'l1_loose':(Cut('l1_byIsolationMVArun2v1DBoldDMwLT>1.5') & Cut('l2_byIsolationMVArun2v1DBoldDMwLT>4.5'), Cut('l1_byIsolationMVArun2v1DBoldDMwLT>1.5') & Cut('l2_byIsolationMVArun2v1DBoldDMwLT>0.5')),
    #     'l1_vloose':(Cut('l1_byIsolationMVArun2v1DBoldDMwLT>0.5') & Cut('l2_byIsolationMVArun2v1DBoldDMwLT>4.5'),Cut('l1_byIsolationMVArun2v1DBoldDMwLT>0.5') & Cut('1')),
    # }

    for cut in cuts:
        for iso_cut_name, (iso_cut, max_iso_cut) in iso_cuts.items():
            
            # iso and charge cuts, need to have them explicitly for the QCD estimation
            # max_iso_cut = Cut('l1_byIsolationMVArun2v1DBoldDMwLT > 2.5 && l2_byIsolationMVArun2v1DBoldDMwLT > 2.5')
            iso_sideband_cut = (~iso_cut) & max_iso_cut
            charge_cut = Cut('l1_charge != l2_charge')
            isSS = 'SS' in cut.name
            all_samples_qcd = qcd_estimation(
                cut.cut & iso_sideband_cut & (charge_cut if not isSS else ~charge_cut),  # shape sideband
                cut.cut & iso_cut & (~charge_cut),  # norm sideband 1
                cut.cut & iso_sideband_cut & (~charge_cut),  # norm sideband 2
                all_samples if mode in ['mssm'] else samples,
                int_lumi,
                total_weight,
                verbose=verbose,
                friend_func=friend_func
            )

            # now include charge and isolation too
            the_cut = MyCut(cut.name+iso_cut_name, cut.cut & iso_cut & (charge_cut if not isSS else ~charge_cut))

            # for variable in variables:
            cfg_total = HistogramCfg(name=the_cut.name, vars=variables, cfgs=all_samples_qcd, cut=str(the_cut.cut), lumi=int_lumi, weight=total_weight)
            # all_samples_qcd[-1].vars = variables

            if mode == 'mva_train':
                createTrees(cfg_total, '/data1/steggema/tt/MVATrees', verbose=True)
                continue

            plots = createHistograms(cfg_total, verbose=True, friend_func=friend_func)


            for variable in variables:
                plot = plots[variable.name]
                plot.Group('Single t', ['T_tWch', 'TBar_tWch', 'TToLeptons_tch_powheg', 'TBarToLeptons_tch_powheg'])  # 'TToLeptons_sch',
                plot.Group('VV', ['VVTo2L2Nu', 'ZZTo2L2Q', 'WWTo1L1Nu2Q', 'WZTo1L3Nu', 'ZZTo4L',  'WZTo2L2Q', 'WZTo1L1Nu2Q', 'Single t'])  # 'WZTo3L',
                plot.Group('ZTT', ['ZTT', 'ZTT1Jets', 'ZTT2Jets', 'ZTT3Jets', 'ZTT4Jets'])
                plot.Group('ZJ', ['ZJ', 'ZJ1Jets', 'ZJ2Jets', 'ZJ3Jets', 'ZJ4Jets'])
                plot.Group('ZL', ['ZL', 'ZL1Jets', 'ZL2Jets', 'ZL3Jets', 'ZL4Jets'])
                plot.Group('W', ['WJetsToLNu', 'W1Jets', 'W2Jets', 'W3Jets', 'W4Jets'])
                plot.Group('Electroweak', ['W', 'VV', 'Single t', 'ZJ'])

                if optimisation:
                    plot.DrawStack('HIST')
                    print plot
                    for signal_hist in plot.SignalHists():
                        sample_names.add(signal_hist.name)
                        ams = ams_hists_rebin(signal_hist.weighted, plot.BGHist().weighted)
                        if variable.name == 'mt_total_mssm' and signal_hist.name == 'ggH1800':
                            print ams_hists_rebin(signal_hist.weighted, plot.BGHist().weighted, debug=True)
                            # import pdb; pdb.set_trace()
                        ams_dict[variable.name + '__' + the_cut.name + '__' + signal_hist.name + '_'] = ams
                
                if not make_plots:
                    continue

                blindxmin = 0.7 if 'mva' in variable.name else None
                blindxmax = 1.00001 if 'mva' in variable.name else None

                if variable.name == 'mt2':
                    blindxmin = 60.
                    blindxmax = variable.binning['xmax']

                if variable.name == 'mt_sum':
                    blindxmin = 250.
                    blindxmax = variable.binning['xmax']

                if variable.name == 'mt_total':
                    blindxmin = 200.
                    blindxmax = variable.binning['xmax']

                plot_dir = 'plot_' + the_cut.name
                HistDrawer.draw(plot, channel='#tau_{h}#tau_{h}', plot_dir=plot_dir, blindxmin=blindxmin, blindxmax=blindxmax)
                # HistDrawer.drawRatio(plot, channel='#tau_{h}#tau_{h}')

                plot.UnGroup('Electroweak')#, ['W', 'VV', 'Single t', 'ZJ'])
                plot.Group('VV', ['VV', 'Single t'])
                if variable.name in ['mt_total', 'svfit_mass', 'mt_total_mssm', 'mt_total_mssm_fine']:
                    plot.WriteDataCard(filename=plot_dir+'/htt_tt.inputs-sm-13TeV_{var}{postfix}.root'.format(var=variable.name, postfix=dc_postfix), dir='tt_' + cut.name, mode='UPDATE')

            # Save AMS dict
            import pickle
            pickle.dump(ams_dict, open('opt.pkl', 'wb'))
            

    if optimisation:
        print '\nOptimisation results:'
        all_vals = ams_dict.items()
        for sample_name in sample_names:
            vals = [v for v in all_vals if sample_name + '_' in v[0]]
            vals.sort(key=itemgetter(1))
            for key, item in vals:
                print item, key

            print '\nBy variable'
            for variable in variables:
                name = variable.name
                print '\nResults for variable', name
                for key, item in vals:
                    if key.startswith(name + '__'):
                        print item, key


if __name__ == '__main__':
    mode = 'susy' # 'control' 'mssm' 'mva_train' 'susy' 'sm'

    int_lumi = lumi
    analysis_dir = '/data1/steggema/Gael3/MC/'
    verbose = True
    total_weight = 'weight'

    import os
    from ROOT import gSystem, gROOT
    if "/sHTTEfficiencies_cc.so" not in gSystem.GetLibraries(): 
        gROOT.ProcessLine(".L %s/src/CMGTools/H2TauTau/python/proto/plotter/HTTEfficiencies.cc+" % os.environ['CMSSW_BASE']);
        from ROOT import getTauWeight

    total_weight = 'weight*getTauWeight(l1_gen_match, l1_pt, l1_eta, l1_decayMode)*getTauWeight(l2_gen_match, l2_pt, l2_eta, l2_decayMode)'

    optimisation = True
    make_plots = True

    # Check whether friend trees need to be added
    friend_func = None
    if mode == 'mva':
        # friend_func = lambda f: f.replace('MC', 'MCMVAmt200')
        friend_func = lambda f: f.replace('MC', 'MCMVAmt200_7Vars')

    cuts = prepareCuts(mode)
    all_samples, samples = createSamples(mode, analysis_dir, optimisation)
    variables = getVariables(mode)
    makePlots(variables, cuts, total_weight, all_samples, samples, friend_func, mode=mode, optimisation=optimisation)
