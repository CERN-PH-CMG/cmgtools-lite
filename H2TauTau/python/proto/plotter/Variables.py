from CMGTools.H2TauTau.proto.plotter.PlotConfigs import VariableCfg as VCfg

from CMGTools.H2TauTau.proto.plotter.binning import binning_svfitMass_finer

generic_vars = [
    VCfg(name='_norm_', drawname='1.', binning={'nbinsx':5, 'xmin':-1.5, 'xmax':3.5}, unit='', xtitle='Normalisation'),
    VCfg(name='svfit_mass', binning=binning_svfitMass_finer, unit='GeV', xtitle='m_{#tau#tau}'),
    VCfg(name='svfit_transverse_mass', binning={'nbinsx':40, 'xmin':0., 'xmax':300.}, unit='GeV', xtitle='M_{T}^{SVFit}'),
    VCfg(name='mvis', binning=binning_svfitMass_finer, unit='GeV', xtitle='m_{vis}'),
    VCfg(name='mvis_fine', drawname='mvis', binning={'nbinsx':200, 'xmin':0., 'xmax':200.}, unit='GeV', xtitle='m_{vis}'),
    VCfg(name='mvis_extended', drawname='mvis', binning={'nbinsx':50, 'xmin':0., 'xmax':1000.}, unit='GeV', xtitle='m_{vis}'),
    VCfg(name='mt', binning={'nbinsx':50, 'xmin':0., 'xmax':200.}, unit='GeV', xtitle='m_{T}'),
    VCfg(name='n_vertices', binning={'nbinsx':51, 'xmin':-0.5, 'xmax':50.5}, unit=None, xtitle='N_{vertices}'),
    VCfg(name='n_jets', binning={'nbinsx':12, 'xmin':-0.5, 'xmax':11.5}, unit=None, xtitle='N_{jets}'),
    VCfg(name='n_jets_20', binning={'nbinsx':12, 'xmin':-0.5, 'xmax':11.5}, unit=None, xtitle='N_{jets} (20 GeV)'),
    VCfg(name='n_bjets', binning={'nbinsx':12, 'xmin':-0.5, 'xmax':11.5}, unit=None, xtitle='N_{b jets}'),
    VCfg(name='met_phi', binning={'nbinsx':40, 'xmin':-3.141593, 'xmax':3.141593}, unit=None, xtitle='E_{T}^{miss} #Phi'),
    VCfg(name='pthiggs', binning={'nbinsx':40, 'xmin':0., 'xmax':200.}, unit='GeV', xtitle='Higgs boson p_{T}'),
    VCfg(name='met_pt', binning={'nbinsx':40, 'xmin':0., 'xmax':150.}, unit='GeV', xtitle='E_{T}^{miss}'),
    VCfg(name='vbf_mjj', binning={'nbinsx':40, 'xmin':0, 'xmax':1000.}, unit='GeV', xtitle='m_{jj}'),
    VCfg(name='vbf_deta', binning={'nbinsx':40, 'xmin':-7., 'xmax':7.}, unit=None, xtitle='#Delta#eta (VBF)'),
    VCfg(name='vbf_n_central', binning={'nbinsx':4, 'xmin':-0.5, 'xmax':3.5}, unit=None, xtitle='N_{central jets}'),
    VCfg(name='jet1_pt', binning={'nbinsx':40, 'xmin':0., 'xmax':200.}, unit='GeV', xtitle='jet 1 p_{T}'),
    VCfg(name='jet2_pt', binning={'nbinsx':40, 'xmin':0., 'xmax':200.}, unit='GeV', xtitle='jet 2 p_{T}'),
    VCfg(name='jet1_eta', binning={'nbinsx':40, 'xmin':-5., 'xmax':5.}, unit=None, xtitle='jet 1 #eta'),
    VCfg(name='jet2_eta', binning={'nbinsx':40, 'xmin':-5., 'xmax':5.}, unit=None, xtitle='jet 2 #eta'),
    VCfg(name='pzeta_vis', binning={'nbinsx':40, 'xmin':0., 'xmax':200.}, unit=None, xtitle='p^{#zeta}_{vis} (GeV)'),
    VCfg(name='pzeta_met', binning={'nbinsx':40, 'xmin':-150., 'xmax':150.}, unit=None, xtitle='p^{#zeta}_{MET} (GeV)'),
    VCfg(name='pzeta_disc', binning={'nbinsx':40, 'xmin':-200., 'xmax':200.}, unit=None, xtitle='p^{#zeta}_{disc} (GeV)'),
    VCfg(name='delta_phi_l1_l2', binning={'nbinsx':40, 'xmin':-3.141593, 'xmax':3.141593}, unit=None, xtitle='#Delta #phi (l1, l2)'),
    # VCfg(name='jet1_chargedHadronMultiplicity', binning={'nbinsx':40, 'xmin':-0.5, 'xmax':39.5}, unit=None, xtitle='jet 1 N_{CH}'),
    # VCfg(name='jet1_chargedMultiplicity', binning={'nbinsx':40, 'xmin':-0.5, 'xmax':39.5}, unit='', xtitle='jet 1 N_{charged}'),
    # VCfg(name='jet1_neutralMultiplicity', binning={'nbinsx':40, 'xmin':-0.5, 'xmax':39.5}, unit='', xtitle='jet 1 N_{neutral}'),
]

muon_l1_vars = [
    VCfg(name='l1_pt', binning={'nbinsx':40, 'xmin':0., 'xmax':100.}, unit='GeV', xtitle='muon p_{T}'),
    VCfg(name='l1_eta', binning={'nbinsx':20, 'xmin':-2.5, 'xmax':2.5}, unit=None, xtitle='muon #eta'),
    VCfg(name='l1_phi', binning={'nbinsx':40, 'xmin':-3.141593, 'xmax':3.141593}, unit=None, xtitle='muon #phi'),
    VCfg(name='l1_reliso05_04', drawname='log(abs(l1_reliso05_04)+0.004)', binning={'nbinsx':40, 'xmin':-6., 'xmax':0.}, unit='', xtitle='log(muon relative isolation cone 0.4)'),
    VCfg(name='l1_reliso05', drawname='log(abs(l1_reliso05)+0.004)', binning={'nbinsx':40, 'xmin':-6., 'xmax':0.}, unit='', xtitle='log(muon relative isolation cone 0.3)'),
    VCfg(name='l1_gen_pdgId', binning={'nbinsx':40, 'xmin':-17.5, 'xmax':22.5}, unit=None, xtitle='muon gen match PDG ID'),
    VCfg(name='l1_log_dxy', drawname='log(abs(l1_dxy))', binning={'nbinsx':40, 'xmin':-18., 'xmax':-2.}, unit='log(cm)', xtitle='log(muon d_{xy})'),
    VCfg(name='l1_dxy_sig', drawname='log(abs(l1_dxy/l1_dxy_error))', binning={'nbinsx':100, 'xmin':-20., 'xmax':20.}, unit=None, xtitle='muon log(d_{xy}/#sigma(d_{xy}))'),
    VCfg(name='l1_log_dz', drawname='log(abs(l1_dz))', binning={'nbinsx':40, 'xmin':-18., 'xmax':-2.}, unit='log(cm)', xtitle='log(muon d_{z})'),
    VCfg(name='l1_dz_sig', drawname='log(abs(l1_dz/l1_dz_error))', binning={'nbinsx':100, 'xmin':-20., 'xmax':20.}, unit=None, xtitle='muon log(d_{z}/#sigma(d_{z}))'),
    VCfg(name='delta_phi_l1_met', binning={'nbinsx':40, 'xmin':-3.141593, 'xmax':3.141593}, unit=None, xtitle='#Delta #phi (muon, MET)'),
]

tau_l2_vars = [
    VCfg(name='l2_pt', binning={'nbinsx':40, 'xmin':0., 'xmax':100.}, unit='GeV', xtitle='tau p_{T}'),
    VCfg(name='l2_eta', binning={'nbinsx':20, 'xmin':-2.5, 'xmax':2.5}, unit=None, xtitle='tau #eta'),
    VCfg(name='l2_phi', binning={'nbinsx':40, 'xmin':-3.141593, 'xmax':3.141593}, unit=None, xtitle='tau #phi'),
    VCfg(name='l2_mt', drawname='mt_leg2', binning={'nbinsx':50, 'xmin':0., 'xmax':200.}, unit='GeV', xtitle='m_{T} #tau'),
    VCfg(name='l2_decayMode', binning={'nbinsx':12, 'xmin':-0.5, 'xmax':11.5}, unit=None, xtitle='tau decay mode'),
    VCfg(name='l2_mass', binning={'nbinsx':40, 'xmin':0., 'xmax':3.}, unit='GeV', xtitle='tau mass'),
    VCfg(name='l2_gen_pdgId', binning={'nbinsx':40, 'xmin':-17.5, 'xmax':22.5}, unit=None, xtitle='tau gen match PDG ID'),
    VCfg(name='l2_log_dxy', drawname='log(abs(l2_dxy)+0.00001)', binning={'nbinsx':40, 'xmin':-18., 'xmax':0.5}, unit='log(cm)', xtitle='log(tau d_{xy})'),
    VCfg(name='l2_dxy_sig', drawname='log(abs(l2_dxy/l2_dxy_error))', binning={'nbinsx':100, 'xmin':-20., 'xmax':20.}, unit=None, xtitle='tau log(d_{xy}/#sigma(d_{xy}))'),
    VCfg(name='l2_log_dz', drawname='log(abs(l2_dz)+0.00001)', binning={'nbinsx':40, 'xmin':-18., 'xmax':0.5}, unit='log(cm)', xtitle='log(tau d_{z})'),
    VCfg(name='l2_dz_sig', drawname='log(abs(l2_dz/l2_dz_error))', binning={'nbinsx':100, 'xmin':-20., 'xmax':20.}, unit=None, xtitle='tau log(d_{z}/#sigma(d_{z}))'),
    VCfg(name='l2_byCombinedIsolationDeltaBetaCorrRaw3Hits', binning={'nbinsx':100, 'xmin':0., 'xmax':100.}, unit='GeV', xtitle='tau delta-beta corr. 3-hit isolation'),
    VCfg(name='l2_byIsolationMVArun2v1DBoldDMwLTraw', binning={'nbinsx':100, 'xmin':-1., 'xmax':1.}, unit='', xtitle='tau isolation MVA (old DM w/LT)'),
    VCfg(name='l2_byIsolationMVArun2v1DBdR03oldDMwLTraw', binning={'nbinsx':100, 'xmin':0., 'xmax':1.}, unit='', xtitle='tau isolation MVA (old DM w/LT cone 0.3)'),
    VCfg(name='l2_nc_ratio', binning={'nbinsx':20, 'xmin':-1., 'xmax':1.}, unit='GeV', xtitle='tau neutral-charged asymmetry'),
    VCfg(name='l2_gen_nc_ratio', binning={'nbinsx':20, 'xmin':-1., 'xmax':1.}, unit='GeV', xtitle='tau gen neutral-charged asymmetry'),
    VCfg(name='delta_phi_l2_met', binning={'nbinsx':40, 'xmin':-3.141593, 'xmax':3.141593}, unit=None, xtitle='#Delta #phi (tau, MET)'),
]

muon_l2_vars = [
    VCfg(name='l2_pt', binning={'nbinsx':40, 'xmin':0., 'xmax':100.}, unit='GeV', xtitle='2nd muon p_{T}'),
    VCfg(name='l2_eta', binning={'nbinsx':20, 'xmin':-2.5, 'xmax':2.5}, unit=None, xtitle='2nd muon #eta'),
    VCfg(name='l2_phi', binning={'nbinsx':40, 'xmin':-3.141593, 'xmax':3.141593}, unit=None, xtitle='2nd muon #phi'),
    VCfg(name='l2_reliso05_04', drawname='log(abs(l2_reliso05_04)+0.004)', binning={'nbinsx':40, 'xmin':-6., 'xmax':0.}, unit='', xtitle='log(2nd muon relative isolation cone 0.4)'),
    VCfg(name='l2_reliso05', drawname='log(abs(l2_reliso05)+0.004)', binning={'nbinsx':40, 'xmin':-6., 'xmax':0.}, unit='', xtitle='log(2nd muon relative isolation cone 0.3)'),
    VCfg(name='l2_gen_pdgId', binning={'nbinsx':40, 'xmin':-17.5, 'xmax':22.5}, unit=None, xtitle='muon gen match PDG ID'),
    VCfg(name='l2_log_dxy', drawname='log(abs(l2_dxy))', binning={'nbinsx':40, 'xmin':-18., 'xmax':-2.}, unit='log(cm)', xtitle='log(2nd muon d_{xy})'),
    VCfg(name='l2_dxy_sig', drawname='log(abs(l2_dxy/l1_dxy_error))', binning={'nbinsx':100, 'xmin':-20., 'xmax':20.}, unit=None, xtitle='2nd muon log(d_{xy}/#sigma(d_{xy}))'),
    VCfg(name='l2_log_dz', drawname='log(abs(l2_dz))', binning={'nbinsx':40, 'xmin':-18., 'xmax':-2.}, unit='log(cm)', xtitle='log(2nd muon d_{z})'),
    VCfg(name='l2_dz_sig', drawname='log(abs(l2_dz/l2_dz_error))', binning={'nbinsx':100, 'xmin':-20., 'xmax':20.}, unit=None, xtitle='2nd muon log(d_{z}/#sigma(d_{z}))'),
    VCfg(name='delta_phi_l2_met', binning={'nbinsx':40, 'xmin':-3.141593, 'xmax':3.141593}, unit=None, xtitle='#Delta #phi (2nd muon, MET'),
]

tau_mu_special_vars = [
    VCfg(name='delta_eta_l1_l2', binning={'nbinsx':40, 'xmin':0, 'xmax':4.5}, unit=None, xtitle='#Delta#eta(#tau, #mu)'),
    VCfg(name='delta_r_l1_l2', binning={'nbinsx':40, 'xmin':0, 'xmax':4.5}, unit=None, xtitle='#Delta R(#tau, #mu)'),
]

mu_mu_special_vars = [
    VCfg(name='delta_eta_l1_l2', binning={'nbinsx':40, 'xmin':0, 'xmax':4.5}, unit=None, xtitle='#Delta#eta(#mu, #mu)'),
    VCfg(name='delta_r_l1_l2', binning={'nbinsx':40, 'xmin':0, 'xmax':4.5}, unit=None, xtitle='#Delta R(#mu, #mu)'),
]


additional_tau_vars = [
    VCfg(name='tau1_pt', binning={'nbinsx':40, 'xmin':0., 'xmax':100.}, unit='GeV', xtitle='tau p_{T}'),
    VCfg(name='tau1_eta', binning={'nbinsx':20, 'xmin':-2.5, 'xmax':2.5}, unit=None, xtitle='tau #eta'),
    VCfg(name='tau1_decayMode', binning={'nbinsx':12, 'xmin':-0.5, 'xmax':11.5}, unit=None, xtitle='tau decay mode'),
    VCfg(name='tau1_mass', binning={'nbinsx':40, 'xmin':0., 'xmax':3.}, unit='GeV', xtitle='tau mass'),
    VCfg(name='tau1_gen_pdgId', binning={'nbinsx':40, 'xmin':-17.5, 'xmax':22.5}, unit=None, xtitle='tau gen match PDG ID'),
    VCfg(name='tau1_log_dxy', drawname='log(abs(tau1_dxy)+0.00001)', binning={'nbinsx':40, 'xmin':-18., 'xmax':0.5}, unit='log(cm)', xtitle='log(tau d_{xy})'),
    VCfg(name='tau1_dxy_sig', drawname='log(abs(tau1_dxy/tau1_dxy_error))', binning={'nbinsx':100, 'xmin':-20., 'xmax':20.}, unit=None, xtitle='tau log(d_{xy}/#sigma(d_{xy}))'),
    VCfg(name='tau1_byCombinedIsolationDeltaBetaCorrRaw3Hits', binning={'nbinsx':100, 'xmin':0., 'xmax':100.}, unit='GeV', xtitle='tau delta-beta corr. 3-hit isolation'),
    VCfg(name='tau1_chargedIsoPtSum', binning={'nbinsx':50, 'xmin':0., 'xmax':50.}, unit='', xtitle='charged isolation (GeV)'),
    VCfg(name='tau1_neutralIsoPtSum', binning={'nbinsx':50, 'xmin':0., 'xmax':50.}, unit='', xtitle='neutral isolation (GeV)'),
    VCfg(name='tau1_photonPtSumOutsideSignalCone', binning={'nbinsx':50, 'xmin':0., 'xmax':30.}, unit='', xtitle='tau photon p_{T} outer (GeV)'),
]
additional_extra_tau_vars = [
    VCfg(name='tau1_iso_n_ch', binning={'nbinsx':41, 'xmin':-0.5, 'xmax':40.5}, unit='', xtitle='tau isolation N_{charged hadrons}'),
    VCfg(name='tau1_iso_n_gamma', binning={'nbinsx':41, 'xmin':-0.5, 'xmax':40.5}, unit='', xtitle='tau isolation N_{photons}'),
    VCfg(name='tau1_lead_ch_pt', drawname='log(abs(tau_lead_ch_pt)) - 999*(tau_lead_ch_pt<0)', binning={'nbinsx':40, 'xmin':-0.1, 'xmax':6.}, unit='GeV', xtitle='log(tau iso leading CH p_{T})'),
    VCfg(name='tau1_lead_ch_dxy', drawname='log(abs(tau_lead_ch_dxy))', binning={'nbinsx':40, 'xmin':-12., 'xmax':-2.}, unit='cm', xtitle='log(tau iso leading CH d_{xy})'),
    VCfg(name='tau1_lead_ch_dz', drawname='log(abs(tau_lead_ch_dz))', binning={'nbinsx':40, 'xmin':-12., 'xmax':3.}, unit='cm', xtitle='log(tau iso leading CH d_{z})'),
    VCfg(name='tau1_lead_ch_ndof', binning={'nbinsx':34, 'xmin':-0.5, 'xmax':33.5}, unit='', xtitle='tau iso leading CH ndof'),
    VCfg(name='tau1_lead_ch_normchi2', binning={'nbinsx':100, 'xmin':-0., 'xmax':49.5}, unit='', xtitle='tau iso leading CH normalized chi2'),
    VCfg(name='tau1_lead_ch_chi2', binning={'nbinsx':100, 'xmin':-0., 'xmax':49.5}, unit='', xtitle='tau iso leading CH  chi2'),
    VCfg(name='tau1_lead_ch_n_layers_pixel', binning={'nbinsx':6, 'xmin':-0.5, 'xmax':5.5}, unit='', xtitle='tau iso leading CH N_{pixel layers}'),
    VCfg(name='tau1_lead_ch_n_hits_pixel', binning={'nbinsx':9, 'xmin':-0.5, 'xmax':8.5}, unit='', xtitle='tau iso leading CH N_{pixel hits}'),
    VCfg(name='tau1_lead_ch_n_layers_tracker', binning={'nbinsx':6, 'xmin':-0.5, 'xmax':5.5}, unit='', xtitle='tau iso leading CH N_{tracker layers}'),
    VCfg(name='tau1_lead_ch_n_hits', binning={'nbinsx':32, 'xmin':-0.5, 'xmax':31.5}, unit='', xtitle='tau iso leading CH N_{hits}'),
    VCfg(name='tau1_lead_ch_n_missing_inner', binning={'nbinsx':4, 'xmin':-0.5, 'xmax':3.5}, unit='', xtitle='tau iso leading CH N_{missing inner hits}'),

    VCfg(name='tau1_leadiso_ch_pt', drawname='log(abs(tau_leadiso_ch_pt)) - 999*(tau_leadiso_ch_pt<0)', binning={'nbinsx':40, 'xmin':-0.1, 'xmax':6.}, unit='GeV', xtitle='log(tau iso leading CH p_{T})'),
    VCfg(name='tau1_leadiso_ch_dxy', drawname='log(abs(tau_leadiso_ch_dxy))', binning={'nbinsx':40, 'xmin':-12., 'xmax':-2.}, unit='cm', xtitle='log(tau iso leading CH d_{xy})'),
    VCfg(name='tau1_leadiso_ch_dz', drawname='log(abs(tau_leadiso_ch_dz))', binning={'nbinsx':40, 'xmin':-12., 'xmax':3.}, unit='cm', xtitle='log(tau iso leading CH d_{z})'),
    VCfg(name='tau1_leadiso_ch_ndof', binning={'nbinsx':34, 'xmin':-0.5, 'xmax':33.5}, unit='', xtitle='tau iso leading CH ndof'),
    VCfg(name='tau1_leadiso_ch_normchi2', binning={'nbinsx':100, 'xmin':-0., 'xmax':49.5}, unit='', xtitle='tau iso leading CH normalized chi2'),
    VCfg(name='tau1_leadiso_ch_chi2', binning={'nbinsx':100, 'xmin':-0., 'xmax':49.5}, unit='', xtitle='tau iso leading CH  chi2'),
    VCfg(name='tau1_leadiso_ch_n_layers_pixel', binning={'nbinsx':6, 'xmin':-0.5, 'xmax':5.5}, unit='', xtitle='tau iso leading CH N_{pixel layers}'),
    VCfg(name='tau1_leadiso_ch_n_hits_pixel', binning={'nbinsx':9, 'xmin':-0.5, 'xmax':8.5}, unit='', xtitle='tau iso leading CH N_{pixel hits}'),
    VCfg(name='tau1_leadiso_ch_n_layers_tracker', binning={'nbinsx':6, 'xmin':-0.5, 'xmax':5.5}, unit='', xtitle='tau iso leading CH N_{tracker layers}'),
    VCfg(name='tau1_leadiso_ch_n_hits', binning={'nbinsx':32, 'xmin':-0.5, 'xmax':31.5}, unit='', xtitle='tau iso leading CH N_{hits}'),
    VCfg(name='tau1_leadiso_ch_n_missing_inner', binning={'nbinsx':4, 'xmin':-0.5, 'xmax':3.5}, unit='', xtitle='tau iso leading CH N_{missing inner hits}'),

]

taumu_vars = generic_vars + muon_l1_vars + tau_l2_vars + tau_mu_special_vars

mumu_vars = generic_vars + muon_l1_vars + muon_l2_vars + additional_tau_vars

all_vars = generic_vars + muon_l1_vars + muon_l2_vars + tau_l2_vars + additional_tau_vars + tau_mu_special_vars

dict_all_vars = {}
for v in all_vars:
    dict_all_vars[v.name] = v

def getVars(names):
    return [dict_all_vars[n] for n in names]
    
