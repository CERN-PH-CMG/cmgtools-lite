from array import array
from collections import namedtuple
from ROOT import TFile, TTreeFormula

from CMGTools.H2TauTau.proto.plotter.categories_TauTau import inc_sig_tau1_iso, inc_sig_tau2_iso, inc_sig_no_iso
from CMGTools.H2TauTau.proto.plotter.cut import Cut
from CMGTools.H2TauTau.proto.plotter.qcdEstimation import qcd_estimation
# from CMGTools.H2TauTau.proto.plotter.helper_methods import getPUWeight
from CMGTools.H2TauTau.proto.samples.spring16.htt_common import lumi

from CMGTools.H2TauTau.proto.plotter.Samples import createSampleLists

int_lumi = lumi
qcd_from_same_sign = False
w_qcd_mssm_method = False
r_qcd_os_ss = 1.17
mssm = False

analysis_dir = '/data1/steggema/tt/230816/DiTauNewMC'
verbose = True
total_weight = 'weight'
myCut = namedtuple('myCut', ['name', 'cut'])
cuts = []

# categories, do not include charge and iso cuts
inc_cut = inc_sig_no_iso

# iso and charge cuts, need to have them explicitly for the QCD estimation
iso_cut = inc_sig_tau1_iso & inc_sig_tau2_iso
max_iso_cut = Cut('l1_byIsolationMVArun2v1DBoldDMwLT > 1.5 && l2_byIsolationMVArun2v1DBoldDMwLT > 1.5')
iso_sideband_cut = (~iso_cut) & max_iso_cut
charge_cut = Cut('l1_charge != l2_charge')

# append categories to plot

cuts.append(myCut('inclusive', inc_cut))

samples_mc, samples_data, samples, all_samples, sampleDict = createSampleLists(analysis_dir=analysis_dir, channel='tt', mode='mssm' if mssm else 'susy', ztt_cut='(l2_gen_match == 5 && l1_gen_match == 5)', zl_cut='(l1_gen_match < 6 && l2_gen_match < 6 && !(l1_gen_match == 5 && l2_gen_match == 5))',
                                                                               zj_cut='(l2_gen_match == 6 || l1_gen_match == 6)', signal_scale=1.)

def createDefaultGroups(plot):
    plot.Group('VV', ['VVTo2L2Nu', 'ZZTo2L2Q', 'WWTo1L1Nu2Q', 'WZTo1L3Nu', 'ZZTo4L', 'WZTo3L', 'WZTo2L2Q',
                      'WZTo1L1Nu2Q', 'T_tWch', 'TBar_tWch', 'TToLeptons_tch_powheg', 'TBarToLeptons_tch_powheg'])
    plot.Group('ZTT', ['ZTT', 'ZTT1Jets', 'ZTT2Jets', 'ZTT3Jets', 'ZTT4Jets', 'ZTTM150', 'ZTTM10'])
    plot.Group('ZJ', ['ZJ', 'ZJ1Jets', 'ZJ2Jets', 'ZJ3Jets', 'ZJ4Jets', 'ZJM150', 'ZJM10'])
    plot.Group('ZL', ['ZL', 'ZL1Jets', 'ZL2Jets', 'ZL3Jets', 'ZL4Jets', 'ZLM150', 'ZLM10'])



keep_vars = ['n_jets', 'weight', 'met_pt', 'mt', 'pthiggs', 'mt_total', 'l1_pt', 'l2_pt', 'mvis', 'delta_r_l1_l2', 'dil_eta', 'mt_leg2', 'delta_phi_l1_l2', 'delta_eta_l1_l2', 'delta_r_l1_l2', 'delta_phi_l1_met', 'l1_eta', 'l2_eta',  'jet1_pt', 'jet1_phi', 'jet2_pt'
             ]
# auto* iter =  tree->GetListOfBranches()->MakeIterator()
# TObject* obj = iter->Next();
# while (obj) {std::cout << obj->GetName() << std::endl; obj=iter->Next();}
all_vars = ['run', 'lumi', 'event', 'bx', 'orbit_number', 'is_data', 'nPU', 'pass_leptons', 'veto_dilepton', 'veto_thirdlepton', 'veto_otherlepton', 'n_jets', 'n_jets_puid', 'n_jets_20', 'n_jets_20_puid', 'n_bjets', 'n_jets_csvl', 'n_vertices', 'rho', 'weight', 'weight_vertex', 'weight_njet', 'mvis', 'mt_total', 'sum_lepton_mt', 'sqsum_lepton_mt', 'pzeta_met', 'pzeta_vis', 'pzeta_disc', 'mt', 'mt_leg2', 'met_cov00', 'met_cov10', 'met_cov11', 'met_phi', 'met_px', 'met_py', 'met_pt', 'pthiggs', 'delta_phi_l1_l2', 'delta_eta_l1_l2', 'delta_r_l1_l2', 'delta_phi_l1_met', 'delta_phi_l2_met', 'svfit_mass', 'svfit_transverse_mass', 'svfit_mass_error', 'svfit_pt', 'svfit_l1_pt', 'svfit_l1_eta', 'svfit_l1_phi', 'svfit_l1_charge', 'svfit_l1_mass', 'svfit_l2_pt', 'svfit_l2_eta', 'svfit_l2_phi', 'svfit_l2_charge', 'svfit_l2_mass', 'geninfo_mcweight', 'geninfo_nup', 'geninfo_htgen', 'geninfo_invmass', 'weight_gen', 'genmet_pt', 'genmet_px', 'genmet_py', 'genmet_phi', 'vbf_mjj', 'vbf_deta', 'vbf_n_central20', 'vbf_n_central', 'vbf_jdphi', 'vbf_dijetpt', 'vbf_dijetphi', 'vbf_dphidijethiggs', 'vbf_mindetajetvis', 'jet1_pt', 'jet1_eta', 'jet1_phi', 'jet1_charge', 'jet1_mass', 'jet1_mva_pu', 'jet1_id_pu', 'jet1_flavour_parton', 'jet1_csv', 'jet1_genjet_pt', 'jet2_pt', 'jet2_eta', 'jet2_phi', 'jet2_charge', 'jet2_mass', 'jet2_mva_pu', 'jet2_id_pu', 'jet2_flavour_parton', 'jet2_csv', 'jet2_genjet_pt', 'bjet1_pt', 'bjet1_eta', 'bjet1_phi', 'bjet1_charge', 'bjet1_mass', 'bjet1_mva_pu', 'bjet1_id_pu', 'bjet1_flavour_parton', 'bjet1_csv', 'bjet1_genjet_pt', 'bjet2_pt', 'bjet2_eta', 'bjet2_phi', 'bjet2_charge', 'bjet2_mass', 'bjet2_mva_pu', 'bjet2_id_pu', 'bjet2_flavour_parton', 'bjet2_csv', 'bjet2_genjet_pt', 'HT_allJets', 'HT_jets', 'HT_bJets', 'HT_cleanJets', 'HT_jets30', 'HT_cleanJets30', 'genboson_pt', 'genboson_eta', 'genboson_phi', 'genboson_charge', 'genboson_mass', 'genboson_pdgId', 'gen_top_1_pt', 'gen_top_2_pt', 'gen_top_weight', 'puppimet_pt', 'puppimet_phi', 'puppimet_mt1', 'puppimet_mt2', 'pfmet_pt', 'pfmet_phi', 'pfmet_mt1', 'pfmet_mt2', 'l1_pt', 'l1_eta', 'l1_phi', 'l1_charge', 'l1_mass', 'l1_jet_pt', 'l1_jet_eta', 'l1_jet_phi', 'l1_jet_charge', 'l1_jet_mass', 'l1_dxy', 'l1_dxy_error', 'l1_dz', 'l1_dz_error', 'l1_weight', 'l1_weight_trigger', 'l1_weight_eff_data_trigger', 'l1_eff_trigger_data', 'l1_eff_trigger_mc', 'l1_weight_idiso', 'l1_eff_idiso_data', 'l1_eff_idiso_mc', 'l1_gen_match', 'l1_decayMode', 'l1_zImpact', 'l1_dz_selfvertex', 'l1_ptScale', 'l1_againstElectronMVA6', 'l1_againstMuon3', 'l1_byCombinedIsolationDeltaBetaCorrRaw3Hits', 'l1_byIsolationMVArun2v1DBoldDMwLTraw', 'l1_byIsolationMVArun2v1DBnewDMwLTraw', 'l1_byIsolationMVArun2v1DBdR03oldDMwLTraw', 'l1_byCombinedIsolationDeltaBetaCorr3Hits', 'l1_byIsolationMVArun2v1DBoldDMwLT', 'l1_byIsolationMVArun2v1DBnewDMwLT', 'l1_byIsolationMVArun2v1DBdR03oldDMwLT', 'l1_chargedIsoPtSum', 'l1_decayModeFinding', 'l1_footprintCorrection', 'l1_neutralIsoPtSum', 'l1_puCorrPtSum', 'l1_photonPtSumOutsideSignalCone', 'l1_byTightIsolationMVArun2v1DBoldDMwLT', 'l2_pt', 'l2_eta', 'l2_phi', 'l2_charge', 'l2_mass', 'l2_jet_pt', 'l2_jet_eta', 'l2_jet_phi', 'l2_jet_charge', 'l2_jet_mass', 'l2_dxy', 'l2_dxy_error', 'l2_dz', 'l2_dz_error', 'l2_weight', 'l2_weight_trigger', 'l2_weight_eff_data_trigger', 'l2_eff_trigger_data', 'l2_eff_trigger_mc', 'l2_weight_idiso', 'l2_eff_idiso_data', 'l2_eff_idiso_mc', 'l2_gen_match', 'l2_decayMode', 'l2_zImpact', 'l2_dz_selfvertex', 'l2_ptScale', 'l2_againstElectronMVA6', 'l2_againstMuon3', 'l2_byCombinedIsolationDeltaBetaCorrRaw3Hits', 'l2_byIsolationMVArun2v1DBoldDMwLTraw', 'l2_byIsolationMVArun2v1DBnewDMwLTraw', 'l2_byIsolationMVArun2v1DBdR03oldDMwLTraw', 'l2_byCombinedIsolationDeltaBetaCorr3Hits', 'l2_byIsolationMVArun2v1DBoldDMwLT', 'l2_byIsolationMVArun2v1DBnewDMwLT', 'l2_byIsolationMVArun2v1DBdR03oldDMwLT', 'l2_chargedIsoPtSum', 'l2_decayModeFinding', 'l2_footprintCorrection', 'l2_neutralIsoPtSum', 'l2_puCorrPtSum', 'l2_photonPtSumOutsideSignalCone', 'l2_byTightIsolationMVArun2v1DBoldDMwLT', 'l1_gen_pt', 'l1_gen_eta', 'l1_gen_phi', 'l1_gen_charge', 'l1_gen_mass', 'l1_gen_pdgId', 'l2_gen_pt', 'l2_gen_eta', 'l2_gen_phi', 'l2_gen_charge', 'l2_gen_mass', 'l2_gen_pdgId', 'l1_gen_vis_pt', 'l1_gen_vis_eta', 'l1_gen_vis_phi', 'l1_gen_vis_charge', 'l1_gen_vis_mass', 'l2_gen_vis_pt', 'l2_gen_vis_eta', 'l2_gen_vis_phi', 'l2_gen_vis_charge', 'l2_gen_vis_mass', 'l1_gen_decaymode', 'l2_gen_decaymode', 'l1_trigger_weight', 'l1_trigger_weight_up', 'l1_trigger_weight_down', 'l2_trigger_weight', 'l2_trigger_weight_up', 'l2_trigger_weight_down', 'mt2', 'GenSusyMScan1', 'GenSusyMScan2', 'GenSusyMScan3', 'GenSusyMScan4', 'GenSusyMNeutralino', 'GenSusyMChargino', 'GenSusyMStau', 'GenSusyMStau2',]

out_dict = {}
for cut in cuts:

    isSS = 'SS' in cut.name
    all_samples_qcd = qcd_estimation(
        cut.cut & iso_sideband_cut &   (charge_cut if not isSS else ~charge_cut) , # shape sideband
        cut.cut & iso_cut          & (~charge_cut), # norm sideband 1
        cut.cut & iso_sideband_cut & (~charge_cut), # norm sideband 2
        all_samples if mssm else samples,
        int_lumi, 
        total_weight,
        verbose=verbose
    )
    
    # now include charge and isolation too
    cut = myCut(cut.name, cut.cut & iso_cut & (charge_cut if not isSS else ~charge_cut))
    


    for sample in all_samples_qcd:

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

        file_out_name = '/data1/steggema/MLSpring2016/{sel}_{n}.root'.format(sel=cut.name, n=name)
        file_out = TFile(file_out_name, 'RECREATE')

        tree_out = tree_in.CopyTree(cut_str)

        tree_out.Write()
        # file_out.Close()

        new_file_out = TFile(file_out_name.replace('.root', '_weight.root'), 'RECREATE')

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
    pickle.dump(out_dict, open("/data1/steggema/MLSpring2016/sample_dict_{sel}.pkl".format(sel=cut.name), "wb"))
