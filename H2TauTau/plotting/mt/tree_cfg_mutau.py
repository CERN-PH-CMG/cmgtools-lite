import copy
from array import array
from collections import namedtuple
from ROOT import TFile, TTreeFormula

from CMGTools.H2TauTau.proto.plotter.PlotConfigs import HistogramCfg, VariableCfg
from CMGTools.H2TauTau.proto.plotter.categories_TauMu import cat_Inc
from CMGTools.H2TauTau.proto.plotter.HistCreator import createHistograms, createHistogram
from CMGTools.H2TauTau.proto.plotter.HistDrawer import HistDrawer
from CMGTools.H2TauTau.proto.plotter.Variables import taumu_vars, getVars
# from CMGTools.H2TauTau.proto.plotter.helper_methods import getPUWeight

from CMGTools.H2TauTau.proto.plotter.Samples import createSampleLists

# mode = 'mssm_signal' 
mode = 'mssm_control'

int_lumi = 2301. # from Alexei's email
qcd_from_same_sign = False
w_qcd_mssm_method = False
r_qcd_os_ss = 1.17

analysis_dir = '/data1/steggema/mt/070416/TauMuSVFitMC/'

total_weight = 'weight'#*weight_njet'

print total_weight

Cut = namedtuple('Cut', ['name', 'cut'])

cuts = []

inc_cut = '&&'.join([cat_Inc])
# inc_cut += '&& l2_decayModeFinding'

cuts.append(Cut('inclusive', inc_cut + '&& l1_charge != l2_charge && n_bjets==0'))
# cuts.append(Cut('inclusive_tauisosideband', inc_cut.replace('l2_byIsolationMVArun2v1DBoldDMwLT>3.5', 'l2_byIsolationMVArun2v1DBoldDMwLT<3.5&&l2_byIsolationMVArun2v1DBoldDMwLT>0.5') + '&& l1_charge != l2_charge'))
# cuts.append(Cut('inclusivemt40', inc_cut + '&& l1_charge != l2_charge && mt<40'))

samples_mc, samples_data, samples, all_samples, sampleDict = createSampleLists(analysis_dir=analysis_dir)

if mode == 'mssm_control' or not 'mssm' in mode:
    all_samples = [s for s in all_samples if not 'ggH' in s.name and not 'bbH' in s.name]


def createDefaultGroups(plot):
    plot.Group('VV', ['VVTo2L2Nu', 'ZZTo2L2Q', 'WWTo1L1Nu2Q', 'WZTo1L3Nu', 'ZZTo4L', 'WZTo3L', 'WZTo2L2Q', 'WZTo1L1Nu2Q', 'T_tWch', 'TBar_tWch', 'TToLeptons_tch_powheg', 'TBarToLeptons_tch_powheg'])
    plot.Group('ZTT', ['ZTT', 'ZTT1Jets', 'ZTT2Jets', 'ZTT3Jets', 'ZTT4Jets', 'ZTTM150', 'ZTTM10'])
    plot.Group('ZJ', ['ZJ', 'ZJ1Jets', 'ZJ2Jets', 'ZJ3Jets', 'ZJ4Jets', 'ZJM150', 'ZJM10'])
    plot.Group('ZL', ['ZL', 'ZL1Jets', 'ZL2Jets', 'ZL3Jets', 'ZL4Jets', 'ZLM150', 'ZLM10'])

if qcd_from_same_sign and not w_qcd_mssm_method:
    samples_qcdfromss = [s for s in all_samples if s.name != 'QCD']
    samples_ss = copy.deepcopy(samples_qcdfromss)

    samples_ss = [s for s in samples_ss if not s.is_signal]

    for sample in samples_ss:
        if sample.name != 'data_obs':
            # Subtract background from data
            sample.scale = -1.

    qcd = HistogramCfg(name='QCD', var=None, cfgs=samples_ss, cut=inc_cut, total_scale=r_qcd_os_ss, lumi=int_lumi, weight=total_weight)

    samples_qcdfromss.append(qcd)

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

    stacknow_highmt_os = HistogramCfg(name='HighMTOS', var=var_norm, cfgs=samples_non_w_highmt_os, cut=inc_cut, lumi=int_lumi, weight=total_weight)
    stacknow_highmt_ss = HistogramCfg(name='HighMTSS', var=var_norm, cfgs=samples_non_w_highmt_ss, cut=inc_cut, lumi=int_lumi, weight=total_weight)

    wjets_incl_os = HistogramCfg(name='WInclOS', var=var_norm, cfgs=samples_w_incl_os, cut=inc_cut, lumi=int_lumi, weight=total_weight)
    wjets_incl_ss = HistogramCfg(name='WInclSS', var=var_norm, cfgs=samples_w_incl_ss, cut=inc_cut, lumi=int_lumi, weight=total_weight)

    wjets_highmt_os = HistogramCfg(name='WHighMTOS', var=var_norm, cfgs=samples_w_highmt_os, cut=inc_cut, lumi=int_lumi, weight=total_weight)

    wjets = HistogramCfg(name='W', var=None, cfgs=samples_w, cut=inc_cut,lumi=int_lumi, weight=total_weight)
    wjets_ss = HistogramCfg(name='WSS', var=None, cfgs=samples_w_ss, cut=inc_cut,lumi=int_lumi, weight=total_weight)

    qcd = HistogramCfg(name='QCD', var=None, cfgs=samples_non_w_ss + [wjets_ss], cut=inc_cut, total_scale=r_qcd_os_ss, lumi=int_lumi, weight=total_weight)

    samples_mssm_method = samples_non_w + [wjets, qcd] + samples_signal


# for cut in cuts:
#     if qcd_from_same_sign and not 'SS' in cut.name and not w_qcd_mssm_method:
#         cfg_main = HistogramCfg(name=cut.name, var=None, cfgs=samples_qcdfromss, cut=cut.cut, lumi=int_lumi, weight=total_weight)
#     elif w_qcd_mssm_method:
#         cfg_main = HistogramCfg(name=cut.name, var=None, cfgs=samples_mssm_method, cut=cut.cut, lumi=int_lumi, weight=total_weight)
#         wjets.cut = cut.cut # since wjets is a sub-HistogramCfg
#     else:
#         cfg_main = HistogramCfg(name=cut.name, var=None, cfgs=all_samples, cut=cut.cut, lumi=int_lumi, weight=total_weight)
    
#     if qcd_from_same_sign and not 'SS' in cut.name:
#         qcd.cut = cut.cut.replace('l1_charge != l2_charge', 'l1_charge == l2_charge')

#     if w_qcd_mssm_method:
#         stacknow_highmt_os.name = 'HighMTOS'+cut.name
#         stacknow_highmt_ss.name = 'HighMTSS'+cut.name
#         wjets_incl_os.name = 'WInclOS'+cut.name
#         wjets_incl_ss.name = 'WInclSS'+cut.name
#         wjets_highmt_os.name = 'WHighMTOS'+cut.name
#         wjets_ss.name = 'WJetsSS'+cut.name

#         qcd.cut = cut.cut.replace('l1_charge != l2_charge', 'l1_charge == l2_charge')
#         wjets_ss.cut = cut.cut.replace('l1_charge != l2_charge', 'l1_charge == l2_charge')

#         stacknow_highmt_os.cut = cut.cut.replace('mt<30', 'mt>70') + '&& mt>70'
#         stacknow_highmt_ss.cut = cut.cut.replace('l1_charge != l2_charge', 'l1_charge == l2_charge').replace('mt<30', 'mt>70') + '&& mt>70'

#         wjets_incl_os.cut = cut.cut.replace('mt<30', '1.')
#         wjets_incl_ss.cut = cut.cut.replace('l1_charge != l2_charge', 'l1_charge == l2_charge').replace('mt<30', '1.')

#         wjets_highmt_os.cut = cut.cut.replace('mt<30', 'mt>70') + '&& mt>70'

#         plot_w_os = createHistogram(wjets_incl_os, verbose=False)
#         plot_w_ss = createHistogram(wjets_incl_ss, verbose=False)

#         r_w_os_ss = plot_w_os.GetStack().totalHist.Yield()/plot_w_ss.GetStack().totalHist.Yield()
#         print 'Inclusive W OS/SS ratio:', r_w_os_ss

#         plot_highmt_os = createHistogram(stacknow_highmt_os, all_stack=True, verbose=False)
#         plot_highmt_ss = createHistogram(stacknow_highmt_ss, all_stack=True, verbose=False)
#         createDefaultGroups(plot_highmt_os)
#         createDefaultGroups(plot_highmt_ss)

#         yield_highmt_os = plot_highmt_os.GetStack().totalHist.Yield()
#         yield_highmt_ss = plot_highmt_ss.GetStack().totalHist.Yield()

#         plot_w_highmt_os = createHistogram(wjets_highmt_os, verbose=False)

#         yield_w_highmt_os = plot_w_highmt_os.GetStack().totalHist.Yield()

#         if r_w_os_ss < r_qcd_os_ss:
#             print 'WARNING, OS/SS ratio larger for QCD than for W+jets!', r_w_os_ss, r_qcd_os_ss

#         yield_estimation = r_w_os_ss*(yield_highmt_os - r_qcd_os_ss*yield_highmt_ss)/(r_w_os_ss - r_qcd_os_ss)

#         print 'High MT W+jets estimated yield', yield_estimation
#         print 'High MT W+jets MC yield', yield_w_highmt_os

#         w_sf = yield_estimation/yield_w_highmt_os

#         print 'W+jets scale factor:', w_sf, '\n'

#         wjets.total_scale = w_sf
#         wjets_ss.total_scale = -w_sf


keep_vars = ['n_jets', 'weight', 'met_pt', 'mt', 'pthiggs', 'delta_phi_l1_l2', 'delta_eta_l1_l2', 'vbf_deta', 'vbf_mjj', 'vbf_dphidijethiggs', 'vbf_jdphi', 'vbf_n_central', 'svfit_transverse_mass', 'svfit_mass', 'l1_pt', 'l2_pt']

all_vars = ['run', 'lumi', 'event', 'bx', 'orbit_number', 'is_data', 'nPU', 'pass_leptons', 'veto_dilepton', 'veto_thirdlepton', 'veto_otherlepton', 'n_jets', 'n_jets_puid', 'n_jets_20', 'n_jets_20_puid', 'n_bjets', 'n_jets_csvl', 'n_vertices', 'rho', 'weight', 'weight_vertex', 'weight_embed', 'weight_njet', 'weight_hqt', 'weight_hqt_up', 'weight_hqt_down', 'mvis', 'mt_total', 'pzeta_met', 'pzeta_vis', 'pzeta_disc', 'mt', 'mt_leg2', 'met_cov00', 'met_cov01', 'met_cov10', 'met_cov11', 'met_phi', 'met_px', 'met_py', 'met_pt', 'pthiggs', 'delta_phi_l1_l2', 'delta_eta_l1_l2', 'delta_r_l1_l2', 'delta_phi_l1_met', 'delta_phi_l2_met', 'svfit_mass', 'svfit_transverse_mass', 'svfit_mass_error', 'svfit_pt', 'svfit_pt_error', 'svfit_eta', 'svfit_phi', 'svfit_met_pt', 'svfit_met_e', 'svfit_met_phi', 'svfit_met_eta', 'svfit_l1_pt', 'svfit_l1_eta', 'svfit_l1_phi', 'svfit_l1_charge', 'svfit_l1_mass', 'svfit_l2_pt', 'svfit_l2_eta', 'svfit_l2_phi', 'svfit_l2_charge', 'svfit_l2_mass', 'geninfo_mcweight', 'geninfo_nup', 'geninfo_htgen', 'geninfo_invmass', 'geninfo_has_w', 'geninfo_has_z', 'geninfo_mass', 'weight_gen', 'genmet_pt', 'genmet_px', 'genmet_py', 'genmet_phi', 'vbf_mjj', 'vbf_deta', 'vbf_n_central20', 'vbf_n_central', 'vbf_jdphi', 'vbf_dijetpt', 'vbf_dijetphi', 'vbf_dphidijethiggs', 'vbf_mindetajetvis', 'jet1_pt', 'jet1_eta', 'jet1_phi', 'jet1_charge', 'jet1_mass', 'jet1_mva_pu', 'jet1_id_loose', 'jet1_id_pu', 'jet1_mva_btag', 'jet1_area', 'jet1_flavour_parton', 'jet1_csv', 'jet1_rawfactor', 'jet1_genjet_pt', 'jet2_pt', 'jet2_eta', 'jet2_phi', 'jet2_charge', 'jet2_mass', 'jet2_mva_pu', 'jet2_id_loose', 'jet2_id_pu', 'jet2_mva_btag', 'jet2_area', 'jet2_flavour_parton', 'jet2_csv', 'jet2_rawfactor', 'jet2_genjet_pt', 'bjet1_pt', 'bjet1_eta', 'bjet1_phi', 'bjet1_charge', 'bjet1_mass', 'bjet1_mva_pu', 'bjet1_id_loose', 'bjet1_id_pu', 'bjet1_mva_btag', 'bjet1_area', 'bjet1_flavour_parton', 'bjet1_csv', 'bjet1_rawfactor', 'bjet1_genjet_pt', 'bjet2_pt', 'bjet2_eta', 'bjet2_phi', 'bjet2_charge', 'bjet2_mass', 'bjet2_mva_pu', 'bjet2_id_loose', 'bjet2_id_pu', 'bjet2_mva_btag', 'bjet2_area', 'bjet2_flavour_parton', 'bjet2_csv', 'bjet2_rawfactor', 'bjet2_genjet_pt', 'HT_allJets', 'HT_jets', 'HT_bJets', 'HT_cleanJets', 'HT_jets30', 'HT_cleanJets30', 'genboson_pt', 'genboson_eta', 'genboson_phi', 'genboson_charge', 'genboson_mass', 'genboson_pdgId', 'puppimet_pt', 'puppimet_phi', 'puppimet_mt1', 'puppimet_mt2', 'pfmet_pt', 'pfmet_phi', 'pfmet_mt1', 'pfmet_mt2', 'l2_pt', 'l2_eta', 'l2_phi', 'l2_charge', 'l2_mass', 'l2_jet_pt', 'l2_jet_eta', 'l2_jet_phi', 'l2_jet_charge', 'l2_jet_mass', 'l2_reliso05', 'l2_reliso05_04', 'l2_dxy', 'l2_dxy_error', 'l2_dz', 'l2_dz_error', 'l2_weight', 'l2_weight_trigger', 'l2_eff_trigger_data', 'l2_eff_trigger_mc', 'l2_weight_idiso', 'l2_eff_idiso_data', 'l2_eff_idiso_mc', 'l2_gen_match', 'l2_decayMode', 'l2_zImpact', 'l2_dz_selfvertex', 'l2_ptScale', 'l2_againstElectronMVA6', 'l2_againstElectronMVA6category', 'l2_againstElectronMVA6raw', 'l2_againstMuon3', 'l2_byCombinedIsolationDeltaBetaCorrRaw3Hits', 'l2_byIsolationMVA3newDMwLTraw', 'l2_byIsolationMVA3oldDMwLTraw', 'l2_byIsolationMVArun2v1DBoldDMwLTraw', 'l2_byIsolationMVArun2v1DBnewDMwLTraw', 'l2_byIsolationMVArun2v1DBdR03oldDMwLTraw', 'l2_byCombinedIsolationDeltaBetaCorr3Hits', 'l2_byIsolationMVA3newDMwLT', 'l2_byIsolationMVA3oldDMwLT', 'l2_byIsolationMVArun2v1DBoldDMwLT', 'l2_byIsolationMVArun2v1DBnewDMwLT', 'l2_byIsolationMVArun2v1DBdR03oldDMwLT', 'l2_chargedIsoPtSum', 'l2_chargedIsoPtSumdR03', 'l2_decayModeFinding', 'l2_decayModeFindingNewDMs', 'l2_neutralIsoPtSum', 'l2_neutralIsoPtSumdR03', 'l2_puCorrPtSum', 'l2_puCorrPtSumdR03', 'l2_byPileupWeightedIsolation3Hits', 'l2_byPileupWeightedIsolationRaw3Hits', 'l2_neutralIsoPtSumWeight', 'l2_footprintCorrection', 'l2_footprintCorrectiondR03', 'l2_photonPtSumOutsideSignalCone', 'l2_photonPtSumOutsideSignalConedR03', 'l1_pt', 'l1_eta', 'l1_phi', 'l1_charge', 'l1_mass', 'l1_jet_pt', 'l1_jet_eta', 'l1_jet_phi', 'l1_jet_charge', 'l1_jet_mass', 'l1_reliso05', 'l1_reliso05_04', 'l1_dxy', 'l1_dxy_error', 'l1_dz', 'l1_dz_error', 'l1_weight', 'l1_weight_trigger', 'l1_eff_trigger_data', 'l1_eff_trigger_mc', 'l1_weight_idiso', 'l1_eff_idiso_data', 'l1_eff_idiso_mc', 'l1_gen_match', 'l1_muonid_loose', 'l1_muonid_medium', 'l1_muonid_tight', 'l1_muonid_tightnovtx', 'l1_muonid_highpt', 'l1_dxy_innertrack', 'l1_dz_innertrack', 'l2_gen_pt', 'l2_gen_eta', 'l2_gen_phi', 'l2_gen_charge', 'l2_gen_mass', 'l2_gen_pdgId', 'l2_gen_lepfromtau', 'l1_gen_pt', 'l1_gen_eta', 'l1_gen_phi', 'l1_gen_charge', 'l1_gen_mass', 'l1_gen_pdgId', 'l1_gen_lepfromtau', 'l2_gen_vis_pt', 'l2_gen_vis_eta', 'l2_gen_vis_phi', 'l2_gen_vis_charge', 'l2_gen_vis_mass', 'l2_gen_decaymode', 'l2_gen_nc_ratio', 'l2_nc_ratio', 'l2_weight_fakerate', 'l2_weight_fakerate_up', 'l2_weight_fakerate_down']

out_dict = {}
for cut in cuts:
    for sample in all_samples:

        name = sample.name

        file_name = '/'.join([sample.ana_dir, sample.dir_name, sample.tree_prod_name, 'tree.root'])
        file_in = TFile.Open(file_name)
        tree_in = file_in.Get(sample.tree_name)

        weight = total_weight
        if sample.weight_expr:
            weight = '*'.join([weight, sample.weight_expr])

        cut_str = '({c}) * {we}'.format(c=cut.cut, we=weight)


        # Extent scale by norm_cut/shape_cut if needed
        non_used_branches = [v for v in all_vars if v not in keep_vars and v not in cut_str]
        for branch in non_used_branches:
            tree_in.SetBranchStatus(branch, 0)
            # branch_to_del = tree_out.GetBranch("name of branch to delete")
            # tree_out.GetListOfBranches().Remove(branch_to_del)

        file_out_name = '/data1/steggema/ML2016/{sel}_{n}.root'.format(sel=cut.name, n=name)
        file_out = TFile(file_out_name, 'RECREATE')

        tree_out = tree_in.CopyTree(cut_str)

        tree_out.Write()
        # file_out.Close()

        new_file_out =  TFile(file_out_name.replace('.root', '_weight.root'), 'RECREATE')

        weight_tree = tree_out.CloneTree(0)

        scale = int_lumi*sample.xsec*sample.scale/sample.sumweights

        full_weight = array('f', [0.])
        new_b = weight_tree.Branch('full_weight', full_weight, 'full_weight/F')
        formula = TTreeFormula('weight_formula', weight, tree_out)
        formula.GetNdata()

        # ATTENTION THIS MAY NOT WORK!
        for i in xrange(tree_out.GetEntries()):
            tree_out.GetEntry(i)
            full_weight[0] = formula.EvalInstance() * scale
            # print full_weight[0]
            # new_b.Fill()
            weight_tree.Fill()
            # tree_out.Fill()

        new_file_out.Write()
        new_file_out.Close()
        file_out.Close()

        print 'Writing file', file_out_name

        out_dict[name] = {}
        out_dict[name]['weight'] = scale
        out_dict[name][cut.name] = cut_str


    import pickle
    pickle.dump(out_dict, open("/data1/steggema/ML2016/sample_dict_{sel}.pkl".format(sel=cut.name), "wb" ))
