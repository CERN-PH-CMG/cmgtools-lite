from CMGTools.H2TauTau.proto.plotter.PlotConfigs import VariableCfg as VCfg

from CMGTools.H2TauTau.proto.plotter.binning import binning_svfitMass_finer

generic_vars = [
    VCfg(name='_norm_', drawname='1.', binning={'nbinsx':5, 'xmin':-1.5, 'xmax':3.5}, unit='', xtitle='Normalisation'),
    VCfg(name='mvis', binning=binning_svfitMass_finer, unit='GeV', xtitle='m_{vis}'),
    VCfg(name='mvis_fine', drawname='mvis', binning={'nbinsx':200, 'xmin':0., 'xmax':200.}, unit='GeV', xtitle='m_{vis}'),
    VCfg(name='mt', binning={'nbinsx':50, 'xmin':0., 'xmax':200.}, unit='GeV', xtitle='m_{T}'),
    VCfg(name='n_vertices', binning={'nbinsx':51, 'xmin':-0.5, 'xmax':50.5}, unit=None, xtitle='N_{vertices}'),
    VCfg(name='n_jets', binning={'nbinsx':12, 'xmin':-0.5, 'xmax':11.5}, unit=None, xtitle='N_{jets}'),
    VCfg(name='n_jets_20', binning={'nbinsx':12, 'xmin':-0.5, 'xmax':11.5}, unit=None, xtitle='N_{jets} (20 GeV)'),
    VCfg(name='n_bjets', binning={'nbinsx':12, 'xmin':-0.5, 'xmax':11.5}, unit=None, xtitle='N_{b jets}'),
    VCfg(name='met_phi', binning={'nbinsx':40, 'xmin':-3.141593, 'xmax':3.141593}, unit=None, xtitle='E_{T}^{miss} #Phi'),
    VCfg(name='met_pt', binning={'nbinsx':40, 'xmin':0., 'xmax':150.}, unit='GeV', xtitle='E_{T}^{miss}'),
    VCfg(name='vbf_mjj', binning={'nbinsx':40, 'xmin':0, 'xmax':1000.}, unit='GeV', xtitle='m_{jj}'),
    VCfg(name='vbf_deta', binning={'nbinsx':40, 'xmin':-7., 'xmax':7.}, unit=None, xtitle='#Delta#eta (VBF)'),
    VCfg(name='jet1_pt', binning={'nbinsx':40, 'xmin':0., 'xmax':200.}, unit='GeV', xtitle='jet 1 p_{T}'),
    VCfg(name='jet2_pt', binning={'nbinsx':40, 'xmin':0., 'xmax':200.}, unit='GeV', xtitle='jet 2 p_{T}'),
    VCfg(name='jet1_eta', binning={'nbinsx':40, 'xmin':-5., 'xmax':5.}, unit=None, xtitle='jet 1 #eta'),
    VCfg(name='jet2_eta', binning={'nbinsx':40, 'xmin':-5., 'xmax':5.}, unit=None, xtitle='jet 2 #eta'),
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
    VCfg(name='l2_nc_ratio', binning={'nbinsx':20, 'xmin':-1., 'xmax':1.}, unit='GeV', xtitle='tau neutral-charged asymmetry'),
    VCfg(name='l2_gen_nc_ratio', binning={'nbinsx':20, 'xmin':-1., 'xmax':1.}, unit='GeV', xtitle='tau gen neutral-charged asymmetry'),
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
]

taumu_vars = generic_vars + muon_l1_vars + tau_l2_vars + tau_mu_special_vars

mumu_vars = generic_vars + muon_l1_vars + muon_l2_vars + additional_tau_vars

all_vars = generic_vars + muon_l1_vars + tau_l2_vars + additional_tau_vars + tau_mu_special_vars

dict_all_vars = {}
for v in all_vars:
    dict_all_vars[v.name] = v

def getVars(names):
    return [dict_all_vars[n] for n in names]
    
