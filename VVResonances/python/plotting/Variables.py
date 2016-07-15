from CMGTools.H2TauTau.proto.plotter.PlotConfigs import VariableCfg as VCfg

from CMGTools.VVResonances.plotting.binning import test_binning

generic_vars = [
    VCfg(name='_norm_', drawname='1.', binning={'nbinsx':5, 'xmin':-1.5, 'xmax':3.5}, unit='', xtitle='Normalisation'),
    VCfg(name='jj_LV_mass', binning={'nbinsx':100, 'xmin':600., 'xmax':5000.}, unit='GeV', xtitle='m_{VV}'),
]

jj_l1_vars = [
    # VCfg(name='l1_pt', binning={'nbinsx':40, 'xmin':0., 'xmax':100.}, unit='GeV', xtitle='muon p_{T}'),
    # VCfg(name='l1_eta', binning={'nbinsx':20, 'xmin':-2.5, 'xmax':2.5}, unit=None, xtitle='muon #eta'),
    # VCfg(name='l1_phi', binning={'nbinsx':40, 'xmin':-3.141593, 'xmax':3.141593}, unit=None, xtitle='muon #phi'),
    # VCfg(name='l1_reliso05_04', drawname='log(abs(l1_reliso05_04)+0.004)', binning={'nbinsx':40, 'xmin':-6., 'xmax':0.}, unit='', xtitle='log(muon relative isolation cone 0.4)'),
    # VCfg(name='l1_reliso05', drawname='log(abs(l1_reliso05)+0.004)', binning={'nbinsx':40, 'xmin':-6., 'xmax':0.}, unit='', xtitle='log(muon relative isolation cone 0.3)'),
    # VCfg(name='l1_gen_pdgId', binning={'nbinsx':40, 'xmin':-17.5, 'xmax':22.5}, unit=None, xtitle='muon gen match PDG ID'),
    # VCfg(name='l1_log_dxy', drawname='log(abs(l1_dxy))', binning={'nbinsx':40, 'xmin':-18., 'xmax':-2.}, unit='log(cm)', xtitle='log(muon d_{xy})'),
    # VCfg(name='l1_dxy_sig', drawname='log(abs(l1_dxy/l1_dxy_error))', binning={'nbinsx':100, 'xmin':-20., 'xmax':20.}, unit=None, xtitle='muon log(d_{xy}/#sigma(d_{xy}))'),
    # VCfg(name='l1_log_dz', drawname='log(abs(l1_dz))', binning={'nbinsx':40, 'xmin':-18., 'xmax':-2.}, unit='log(cm)', xtitle='log(muon d_{z})'),
    # VCfg(name='l1_dz_sig', drawname='log(abs(l1_dz/l1_dz_error))', binning={'nbinsx':100, 'xmin':-20., 'xmax':20.}, unit=None, xtitle='muon log(d_{z}/#sigma(d_{z}))'),
    # VCfg(name='delta_phi_l1_met', binning={'nbinsx':40, 'xmin':-3.141593, 'xmax':3.141593}, unit=None, xtitle='#Delta #phi (muon, MET)'),
]

jj_l2_vars = [

]


VV_vars = generic_vars #+ jj_l1_vars + + jj_l2_vars

all_vars = generic_vars #+ jj_l1_vars + + jj_l2_vars

dict_all_vars = {}
for v in all_vars:
    dict_all_vars[v.name] = v

def getVars(names):
    return [dict_all_vars[n] for n in names]
