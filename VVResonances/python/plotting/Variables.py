from CMGTools.H2TauTau.proto.plotter.PlotConfigs import VariableCfg as VCfg
from CMGTools.VVResonances.plotting.binning import eta_binning, phi_binning, pt_binning
from math import pi

generic_vars = [
    VCfg(name='_norm_', drawname='1.', binning={'nbinsx':5, 'xmin':-1.5, 'xmax':3.5}, unit='', xtitle='Normalisation'),
    VCfg(name='Flag_goodVertices', binning={'nbinsx':5, 'xmin':-1.5, 'xmax':3.5}, unit='', xtitle='Flag_goodVertices'),
    VCfg(name='nVert', binning={'nbinsx':60, 'xmin':0, 'xmax':60}, unit='', xtitle='N primary vertices'),
    VCfg(name='met_pt', binning=pt_binning, unit='GeV', xtitle='MET'),
    VCfg(name='met_phi', binning=phi_binning, unit='', xtitle='MET #phi'),
]

jj_generic_vars = [
    VCfg(name='jj_LV_mass', binning={'nbinsx':100, 'xmin':600., 'xmax':5000.}, unit='GeV', xtitle='m_{VV}'),
    VCfg(name='jj_Delta_eta', drawname='abs(jj_l1_eta-jj_l2_eta)', binning={'nbinsx':50, 'xmin':0, 'xmax':5}, unit='', xtitle='#Delta #eta'),
]

jj_l1_vars = [
    VCfg(name='jj_l1_pt', binning=pt_binning, unit='GeV', xtitle='jet1 p_{T}'),
    VCfg(name='jj_l1_eta', binning=eta_binning, unit=None, xtitle='jet1 #eta'),
    VCfg(name='jj_l1_phi', binning=phi_binning, unit=None, xtitle='jet1 #phi'),
    # VCfg(name='jj_l1_tau1', binning={'nbinsx':40, 'xmin':0., 'xmax':1.}, unit=None, xtitle='jet1 #tau_{1}'),
    # VCfg(name='jj_l1_tau2', binning={'nbinsx':40, 'xmin':0., 'xmax':1.}, unit=None, xtitle='jet1 #tau_{2}'),
    VCfg(name='jj_l1_tau21', drawname='jj_l1_tau2/jj_l1_tau1', binning={'nbinsx':40, 'xmin':0., 'xmax':1.}, unit='', xtitle='jet1 #tau_{21}'),
    VCfg(name='jj_l1_tau21_DDT', binning={'nbinsx':40, 'xmin':0., 'xmax':1.}, unit='', xtitle='jet1 #tau_{21}^{DDT}'),
    # VCfg(name='jj_l1_btagBOOSTED_recalc', binning={'nbinsx':40, 'xmin':-1., 'xmax':1.}, unit='', xtitle='boosted b-tag'),
    VCfg(name='jj_l1_softDrop_mass', drawname='jj_l1_softDrop_massCorr*jj_l1_softDrop_massBare', binning={'nbinsx':100, 'xmin':0., 'xmax':250.}, unit='GeV', xtitle='jet1 SD mass'),
    VCfg(name='jj_l1_softDrop_mass_m55', drawname='jj_l1_softDrop_massCorr*jj_l1_softDrop_massBare', binning={'nbinsx':33, 'xmin':55., 'xmax':220.}, unit='GeV', xtitle='jet1 SD mass'),
    # VCfg(name='jj_l1_s1BTag', binning={'nbinsx':40, 'xmin':-1., 'xmax':1.}, unit=None, xtitle='jet1 subjet1 CSV'),
    # VCfg(name='jj_l1_s2BTag', binning={'nbinsx':40, 'xmin':-1., 'xmax':1.}, unit=None, xtitle='jet1 subjet2 CSV'),
]

jj_l2_vars = [
    VCfg(name='jj_l2_pt', binning=pt_binning, unit='GeV', xtitle='jet2 p_{T}'),
    VCfg(name='jj_l2_eta', binning=eta_binning, unit=None, xtitle='jet2 #eta'),
    VCfg(name='jj_l2_phi', binning=phi_binning, unit=None, xtitle='jet2 #phi'),
    # VCfg(name='jj_l2_tau1', binning={'nbinsx':40, 'xmin':0., 'xmax':1.}, unit=None, xtitle='jet2 #tau_{1}'),
    # VCfg(name='jj_l2_tau2', binning={'nbinsx':40, 'xmin':0., 'xmax':1.}, unit=None, xtitle='jet2 #tau_{2}'),
    VCfg(name='jj_l2_tau21', drawname='jj_l2_tau2/jj_l2_tau1', binning={'nbinsx':40, 'xmin':0., 'xmax':1.}, unit='', xtitle='jet2 #tau_{21}'),
    VCfg(name='jj_l2_tau21_DDT', binning={'nbinsx':40, 'xmin':0., 'xmax':1.}, unit='', xtitle='jet2 #tau_{21}^{DDT}'),
    # VCfg(name='jj_l2_btagBOOSTED_recalc', binning={'nbinsx':40, 'xmin':-1., 'xmax':1.}, unit='', xtitle='boosted b-tag'),
    VCfg(name='jj_l2_softDrop_mass', drawname='jj_l2_softDrop_massCorr*jj_l2_softDrop_massBare', binning={'nbinsx':100, 'xmin':0., 'xmax':250.}, unit='GeV', xtitle='jet2 SD mass'),
    VCfg(name='jj_l2_softDrop_mass_m55', drawname='jj_l2_softDrop_massCorr*jj_l2_softDrop_massBare', binning={'nbinsx':33, 'xmin':55., 'xmax':220.}, unit='GeV', xtitle='jet2 SD mass'),
    # VCfg(name='jj_l2_s1BTag', binning={'nbinsx':40, 'xmin':-1., 'xmax':1.}, unit=None, xtitle='jet2 subjet2 CSV'),
    # VCfg(name='jj_l2_s2BTag', binning={'nbinsx':40, 'xmin':-1., 'xmax':1.}, unit=None, xtitle='jet2 subjet2 CSV'),
]

jj_l1_jetid = [
    VCfg(name='jj_l1_chf', binning={'nbinsx':50, 'xmin':0., 'xmax':1.}, unit='', xtitle='jet1 charged hadron fraction'),
    VCfg(name='jj_l1_nhf', binning={'nbinsx':50, 'xmin':0., 'xmax':1.}, unit='', xtitle='jet1 neutral hadron fraction'),
    VCfg(name='jj_l1_phf', binning={'nbinsx':50, 'xmin':0., 'xmax':1.}, unit='', xtitle='jet1 neutral EM fraction'),
    VCfg(name='jj_l1_muf', binning={'nbinsx':50, 'xmin':0., 'xmax':1.}, unit='', xtitle='jet1 muon fraction'),
    VCfg(name='jj_l1_elf', binning={'nbinsx':50, 'xmin':0., 'xmax':1.}, unit='', xtitle='jet1 charged EM fraction'),
    VCfg(name='jj_l1_chm', binning={'nbinsx':50, 'xmin':0., 'xmax':200}, unit='', xtitle='jet1 charged hadron multiplicity'),
    VCfg(name='jj_l1_npr', binning={'nbinsx':50, 'xmin':0., 'xmax':200}, unit='', xtitle='jet1 number of constituents'),
    VCfg(name='jj_l1_npn', binning={'nbinsx':50, 'xmin':0., 'xmax':200}, unit='', xtitle='jet1 neutral hadron multiplicity'),

]

jj_l2_jetid = [
    VCfg(name='jj_l2_chf', binning={'nbinsx':50, 'xmin':0., 'xmax':1.}, unit='', xtitle='jet2 charged hadron fraction'),
    VCfg(name='jj_l2_nhf', binning={'nbinsx':50, 'xmin':0., 'xmax':1.}, unit='', xtitle='jet2 neutral hadron fraction'),
    VCfg(name='jj_l2_phf', binning={'nbinsx':50, 'xmin':0., 'xmax':1.}, unit='', xtitle='jet2 neutral EM fraction'),
    VCfg(name='jj_l2_muf', binning={'nbinsx':50, 'xmin':0., 'xmax':1.}, unit='', xtitle='jet2 muon fraction'),
    VCfg(name='jj_l2_elf', binning={'nbinsx':50, 'xmin':0., 'xmax':1.}, unit='', xtitle='jet2 charged EM fraction'),
    VCfg(name='jj_l2_chm', binning={'nbinsx':50, 'xmin':0., 'xmax':200}, unit='', xtitle='jet2 charged hadron multiplicity'),
    VCfg(name='jj_l2_npr', binning={'nbinsx':50, 'xmin':0., 'xmax':200}, unit='', xtitle='jet2 number of constituents'),
    VCfg(name='jj_l2_npn', binning={'nbinsx':50, 'xmin':0., 'xmax':200}, unit='', xtitle='jet2 neutral hadron multiplicity'),

]

lnujj_generic_vars = [
    VCfg(name='lnujj_LV_mass', binning={'nbinsx':100, 'xmin':600., 'xmax':5000.}, unit='GeV', xtitle='m_{VV}'),
    VCfg(name='lnujj_sf', binning={'nbinsx':1000, 'xmin':0.75, 'xmax':1.25}, unit=None, xtitle='SF weight'),
    VCfg(name='lnujj_deltaR_lep_jet', drawname='sqrt(pow(lnujj_l1_l_eta-lnujj_l2_eta, 2) + pow(lnujj_l1_l_phi-lnujj_l2_phi, 2))', binning={'nbinsx':50, 'xmin':0, 'xmax':5}, unit=None, xtitle='#Delta R(lepton, jet)'),
    VCfg(name='lnujj_deltaPhi_Wlep_jet', drawname='TVector2::Phi_0_2pi(lnujj_l1_phi-lnujj_l2_phi)', binning={'nbinsx': 40, 'xmin': 0, 'xmax': 2*pi}, unit=None, xtitle='#Delta #phi(W_l, jet)'),
    VCfg(name='lnujj_deltaPhi_met_jet', drawname='TVector2::Phi_0_2pi(met_phi-lnujj_l2_phi)', binning={'nbinsx': 40, 'xmin': 0, 'xmax': 2*pi}, unit=None, xtitle='#Delta #phi(MET, jet)'),
    VCfg(name='lnujj_highestOtherBTag', binning={'nbinsx':40, 'xmin':-1., 'xmax':1.}, unit=None, xtitle='spectator jets highest CSV'),
]

lnujj_l1_vars = [
    VCfg(name='lnujj_l1_l_pt', binning=pt_binning, unit='GeV', xtitle='lepton p_{T}'),
    VCfg(name='lnujj_l1_l_eta', binning=eta_binning, unit=None, xtitle='lepton #eta'),
    VCfg(name='lnujj_l1_l_phi', binning=phi_binning, unit=None, xtitle='lepton #phi'),
    VCfg(name='lnujj_l1_mt', binning={'nbinsx':50, 'xmin':0., 'xmax':150.}, unit='GeV', xtitle='W m_{T}'),
    VCfg(name='lnujj_l1_pt', binning=pt_binning, unit='GeV', xtitle='W p_{T}'),
    VCfg(name='lnujj_l1_eta', binning=eta_binning, unit=None, xtitle='W #eta'),
    VCfg(name='lnujj_l1_phi', binning=phi_binning, unit=None, xtitle='W #phi'),
]

lnujj_l2_vars = [
    VCfg(name='lnujj_l2_pt', binning=pt_binning, unit='GeV', xtitle='jet p_{T}'),
    VCfg(name='lnujj_l2_eta', binning=eta_binning, unit=None, xtitle='jet #eta'),
    VCfg(name='lnujj_l2_phi', binning=phi_binning, unit=None, xtitle='jet #phi'),
    VCfg(name='lnujj_l2_tau1', binning={'nbinsx':40, 'xmin':0., 'xmax':1.}, unit=None, xtitle='jet #tau_{1}'),
    VCfg(name='lnujj_l2_tau2', binning={'nbinsx':40, 'xmin':0., 'xmax':1.}, unit=None, xtitle='jet #tau_{2}'),
    VCfg(name='lnujj_l2_tau21', drawname='lnujj_l2_tau2/lnujj_l2_tau1', binning={'nbinsx':40, 'xmin':0., 'xmax':1.}, unit='', xtitle='jet #tau_{21}'),
    VCfg(name='lnujj_l2_btagBOOSTED_recalc', binning={'nbinsx':40, 'xmin':-1., 'xmax':1.}, unit='', xtitle='boosted b-tag'),
    VCfg(name='lnujj_l2_pruned_mass', binning={'nbinsx':100, 'xmin':0., 'xmax':250.}, unit='GeV', xtitle='jet pruned mass'),
    VCfg(name='lnujj_l2_softDrop_mass', drawname='lnujj_l2_softDrop_massCorr*lnujj_l2_softDrop_massBare', binning={'nbinsx':100, 'xmin':0., 'xmax':250.}, unit='GeV', xtitle='jet soft-drop mass'),
    VCfg(name='lnujj_l2_s1BTag', binning={'nbinsx':40, 'xmin':-1., 'xmax':1.}, unit=None, xtitle='jet subjet1 CSV'),
    VCfg(name='lnujj_l2_s2BTag', binning={'nbinsx':40, 'xmin':-1., 'xmax':1.}, unit=None, xtitle='jet subjet2 CSV'),
    VCfg(name='lnujj_l2_btagCSV', binning={'nbinsx':40, 'xmin':-1., 'xmax':1.}, unit=None, xtitle='jet CSV'),
]

lnujj_vbf_vars = [
    VCfg(name='lnujj_vbfDEta', binning={'nbinsx':50, 'xmin':0, 'xmax':10.}, unit='', xtitle='VBF jets #Delta #eta'),
    VCfg(name='lnujj_vbfMass', binning={'nbinsx':100, 'xmin':0., 'xmax':2000.}, unit='GeV', xtitle='VBF jets mass'),
    VCfg(name='lnujj_vbf_j1_pt', binning=pt_binning, unit='GeV', xtitle='VBF jet1 p_{T}'),
    VCfg(name='lnujj_vbf_j1_eta', binning=eta_binning, unit=None, xtitle='VBF jet1 #eta'),
    VCfg(name='lnujj_vbf_j1_phi', binning=phi_binning, unit=None, xtitle='VBF jet1 #phi'),
    VCfg(name='lnujj_vbf_j1_btagCSV', binning={'nbinsx':40, 'xmin':-1., 'xmax':1.}, unit=None, xtitle='VBF jet1 CSV'),
    VCfg(name='lnujj_vbf_j2_pt', binning=pt_binning, unit='GeV', xtitle='VBF jet2 p_{T}'),
    VCfg(name='lnujj_vbf_j2_eta', binning=eta_binning, unit=None, xtitle='VBF jet2 #eta'),
    VCfg(name='lnujj_vbf_j2_phi', binning=phi_binning, unit=None, xtitle='VBF jet2 #phi'),
    VCfg(name='lnujj_vbf_j2_btagCSV', binning={'nbinsx':40, 'xmin':-1., 'xmax':1.}, unit=None, xtitle='VBF jet2 CSV'),
]


jj_vars = jj_generic_vars + jj_l1_vars + jj_l2_vars
lnujj_vars = lnujj_generic_vars + lnujj_l1_vars + lnujj_l2_vars

all_vars = generic_vars + jj_vars + lnujj_vars + lnujj_vbf_vars

dict_all_vars = {}
for v in all_vars:
    dict_all_vars[v.name] = v

def getVars(names):
    return [dict_all_vars[n] for n in names]
