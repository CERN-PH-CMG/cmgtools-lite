from CMGTools.H2TauTau.proto.plotter.PlotConfigs import VariableCfg as VCfg

from CMGTools.VVResonances.plotting.binning import test_binning

generic_vars = [
    VCfg(name='_norm_', drawname='1.', binning={'nbinsx':5, 'xmin':-1.5, 'xmax':3.5}, unit='', xtitle='Normalisation'),
    VCfg(name='jj_LV_mass', binning={'nbinsx':100, 'xmin':600., 'xmax':5000.}, unit='GeV', xtitle='m_{VV}'),
    VCfg(name='Flag_goodVertices', binning={'nbinsx':5, 'xmin':-1.5, 'xmax':3.5}, unit='', xtitle='Flag_goodVertices'),
]

jj_l1_vars = [
    VCfg(name='jj_l1_pt', binning={'nbinsx':100, 'xmin':0., 'xmax':1000.}, unit='GeV', xtitle='jet1 p_{T}'),
    VCfg(name='jj_l1_eta', binning={'nbinsx':20, 'xmin':-2.5, 'xmax':2.5}, unit=None, xtitle='jet1 #eta'),
    VCfg(name='jj_l1_phi', binning={'nbinsx':40, 'xmin':-3.141593, 'xmax':3.141593}, unit=None, xtitle='jet1 #phi'),
    # VCfg(name='jj_l1_tau1', binning={'nbinsx':40, 'xmin':0., 'xmax':1.}, unit=None, xtitle='jet1 #tau_{1}'),
    # VCfg(name='jj_l1_tau2', binning={'nbinsx':40, 'xmin':0., 'xmax':1.}, unit=None, xtitle='jet1 #tau_{2}'),
    VCfg(name='jj_l1_tau21', drawname='jj_l1_tau2/jj_l1_tau1', binning={'nbinsx':40, 'xmin':0., 'xmax':1.}, unit='', xtitle='jet1 #tau_{21}'),
    VCfg(name='jj_l1_btagBOOSTED_recalc', binning={'nbinsx':40, 'xmin':-1., 'xmax':1.}, unit='', xtitle='boosted b-tag'),
    VCfg(name='jj_l1_softDrop_mass', drawname='jj_l1_softDrop_massCorr*jj_l1_softDrop_massBare', binning={'nbinsx':100, 'xmin':0., 'xmax':250.}, unit='GeV', xtitle='jet1 SD mass'),
    VCfg(name='jj_l1_s1BTag', binning={'nbinsx':40, 'xmin':-1., 'xmax':1.}, unit=None, xtitle='jet1 subjet1 CSV'),
    VCfg(name='jj_l1_s2BTag', binning={'nbinsx':40, 'xmin':-1., 'xmax':1.}, unit=None, xtitle='jet1 subjet2 CSV'),
]

jj_l2_vars = [
    VCfg(name='jj_l2_pt', binning={'nbinsx':100, 'xmin':0., 'xmax':1000.}, unit='GeV', xtitle='jet2 p_{T}'),
    VCfg(name='jj_l2_eta', binning={'nbinsx':20, 'xmin':-2.5, 'xmax':2.5}, unit=None, xtitle='jet2 #eta'),
    VCfg(name='jj_l2_phi', binning={'nbinsx':40, 'xmin':-3.141593, 'xmax':3.141593}, unit=None, xtitle='jet2 #phi'),
    # VCfg(name='jj_l2_tau1', binning={'nbinsx':40, 'xmin':0., 'xmax':1.}, unit=None, xtitle='jet2 #tau_{1}'),
    # VCfg(name='jj_l2_tau2', binning={'nbinsx':40, 'xmin':0., 'xmax':1.}, unit=None, xtitle='jet2 #tau_{2}'),
    VCfg(name='jj_l2_tau21', drawname='jj_l2_tau2/jj_l2_tau1', binning={'nbinsx':40, 'xmin':0., 'xmax':1.}, unit='', xtitle='jet2 #tau_{21}'),
    VCfg(name='jj_l2_btagBOOSTED_recalc', binning={'nbinsx':40, 'xmin':-1., 'xmax':1.}, unit='', xtitle='boosted b-tag'),
    VCfg(name='jj_l2_softDrop_mass', drawname='jj_l2_softDrop_massCorr*jj_l2_softDrop_massBare', binning={'nbinsx':100, 'xmin':0., 'xmax':250.}, unit='GeV', xtitle='jet2 SD mass'),
    VCfg(name='jj_l2_s1BTag', binning={'nbinsx':40, 'xmin':-1., 'xmax':1.}, unit=None, xtitle='jet2 subjet2 CSV'),
    VCfg(name='jj_l2_s2BTag', binning={'nbinsx':40, 'xmin':-1., 'xmax':1.}, unit=None, xtitle='jet2 subjet2 CSV'),
]

lnujj_l1_vars = [
    VCfg(name='lnujj_l1_l_pt', binning={'nbinsx':100, 'xmin':0., 'xmax':1000.}, unit='GeV', xtitle='lepton p_{T}'),
    VCfg(name='lnujj_l1_l_eta', binning={'nbinsx':20, 'xmin':-2.5, 'xmax':2.5}, unit=None, xtitle='lepton #eta'),
    VCfg(name='lnujj_l1_l_phi', binning={'nbinsx':40, 'xmin':-3.141593, 'xmax':3.141593}, unit=None, xtitle='lepton #phi'),
]

lnujj_l2_vars = [
    VCfg(name='lnujj_l2_pt', binning={'nbinsx':100, 'xmin':0., 'xmax':1000.}, unit='GeV', xtitle='jet p_{T}'),
    VCfg(name='lnujj_l2_eta', binning={'nbinsx':20, 'xmin':-2.5, 'xmax':2.5}, unit=None, xtitle='jet #eta'),
    VCfg(name='lnujj_l2_phi', binning={'nbinsx':40, 'xmin':-3.141593, 'xmax':3.141593}, unit=None, xtitle='jet #phi'),
    VCfg(name='lnujj_l2_tau1', binning={'nbinsx':40, 'xmin':0., 'xmax':1.}, unit=None, xtitle='jet #tau_{1}'),
    VCfg(name='lnujj_l2_tau2', binning={'nbinsx':40, 'xmin':0., 'xmax':1.}, unit=None, xtitle='jet #tau_{2}'),
    VCfg(name='lnujj_l2_tau21', drawname='lnujj_l2_tau2/lnujj_l2_tau1', binning={'nbinsx':40, 'xmin':0., 'xmax':1.}, unit='', xtitle='jet #tau_{21}'),
    VCfg(name='lnujj_l2_btagBOOSTED_recalc', binning={'nbinsx':40, 'xmin':-1., 'xmax':1.}, unit='', xtitle='boosted b-tag'),
    VCfg(name='lnujj_l2_pruned_mass', binning={'nbinsx':100, 'xmin':0., 'xmax':250.}, unit='GeV', xtitle='jet pruned mass'),
    VCfg(name='lnujj_l2_softDrop_mass', binning={'nbinsx':100, 'xmin':0., 'xmax':250.}, unit='GeV', xtitle='jet soft-drop mass'),
    VCfg(name='lnujj_l2_s1BTag', binning={'nbinsx':40, 'xmin':-1., 'xmax':1.}, unit=None, xtitle='jet subjet1 CSV'),
    VCfg(name='lnujj_l2_s2BTag', binning={'nbinsx':40, 'xmin':-1., 'xmax':1.}, unit=None, xtitle='jet subjet2 CSV'),
    VCfg(name='lnujj_sf', binning={'nbinsx':1000, 'xmin':0.5, 'xmax':1.5}, unit=None, xtitle='SF weight'),
]

jj_vars = jj_l1_vars + jj_l2_vars
lnujj_vars = lnujj_l1_vars + lnujj_l2_vars

all_vars = generic_vars + jj_l1_vars + jj_l2_vars + lnujj_l1_vars + lnujj_l2_vars

dict_all_vars = {}
for v in all_vars:
    dict_all_vars[v.name] = v

def getVars(names):
    return [dict_all_vars[n] for n in names]
