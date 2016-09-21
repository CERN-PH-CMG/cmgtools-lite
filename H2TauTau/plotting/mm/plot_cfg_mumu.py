import copy

from CMGTools.H2TauTau.proto.samples.spring16.htt_common import lumi, lumi_2016G

from CMGTools.H2TauTau.proto.plotter.PlotConfigs import HistogramCfg
from CMGTools.H2TauTau.proto.plotter.categories_MuMu import cat_Inc
from CMGTools.H2TauTau.proto.plotter.HistCreator import createHistograms
from CMGTools.H2TauTau.proto.plotter.HistDrawer import HistDrawer
from CMGTools.H2TauTau.proto.plotter.Variables import getVars, mumu_vars
from CMGTools.H2TauTau.proto.plotter.Samples import createSampleLists
from CMGTools.H2TauTau.proto.plotter.helper_methods import plotDataOverMCEff, getPUWeight, getVertexWeight


# total_weight = 'weight/l1_weight_eff_data_trigger * ( (l2_pt>22.) * (1 - (1-l1_weight_eff_data_trigger)**2) + (l2_pt<22.) * l1_weight_eff_data_trigger ) '

total_weight = 'weight/l1_weight_eff_data_trigger * (1. - (1.-l1_weight_eff_data_trigger)*(1.-l1_weight_eff_data_trigger))'
# total_weight = 'weight/l1_weight_eff_data_trigger'# * (1. - (1.-l1_weight_eff_data_trigger)**2)'

print 'Total weight', total_weight

# -> Command line
analysis_dir = '/data1/steggema/mm/220716/MuMuMC'
qcd_from_same_sign = True
data2016G = True

int_lumi = lumi

if data2016G:
    int_lumi = lumi_2016G
    total_weight = '(' + total_weight + '*' + getVertexWeight(True) + ')'

cuts = {}

inc_cut = '&&'.join([cat_Inc])

# cuts['OS_PU_m50'] = inc_cut + '&& l1_charge != l2_charge && abs(l1_eta) < 2.1 && abs(l2_eta) < 2.1  && mvis>50'
# # cuts['OS_PU_m20'] = inc_cut + '&& l1_charge != l2_charge && abs(l1_eta) < 2.1 && abs(l2_eta) < 2.1  && mvis>20'
# cuts['OS_PU_1bjet'] = inc_cut + '&& l1_charge != l2_charge && abs(l1_eta) < 2.1 && abs(l2_eta) < 2.1  && mvis>50 && n_bjets==1'
# cuts['OS_PU_2bjet'] = inc_cut + '&& l1_charge != l2_charge && abs(l1_eta) < 2.1 && abs(l2_eta) < 2.1  && mvis>50 && n_bjets>=2'
# cuts['OS_PU_mZ'] = inc_cut + '&& l1_charge != l2_charge && abs(l1_eta) < 2.1 && abs(l2_eta) < 2.1 && mvis>70 && mvis<100'
# cuts['OS_PU_mZ_lowPU'] = inc_cut + '&& l1_charge != l2_charge && abs(l1_eta) < 2.1 && abs(l2_eta) < 2.1 && mvis>70 && mvis<100 && n_vertices<12'
# cuts['OS_PU_mZ_highPU'] = inc_cut + '&& l1_charge != l2_charge && abs(l1_eta) < 2.1 && abs(l2_eta) < 2.1 && mvis>70 && mvis<100 && n_vertices>20'
# # cuts['OS_PU_mZ_0jet'] = inc_cut + '&& l1_charge != l2_charge && abs(l1_eta) < 2.1 && abs(l2_eta) < 2.1 && mvis>70 && mvis<100 && n_jets==0'

# cuts['OS_PU_mZ_gr1jet'] = inc_cut + '&& l1_charge != l2_charge && abs(l1_eta) < 2.1 && abs(l2_eta) < 2.1 && mvis>70 && mvis<100 && n_jets>=1'

# cuts['OS_PU_mZ_gr1jet_tau1'] = inc_cut + '&& l1_charge != l2_charge && abs(l1_eta) < 2.1 && abs(l2_eta) < 2.1 && mvis>70 && mvis<100 && n_jets>=1 && tau1_pt>0.'

# cuts['OS_PU_mZ_eq1jet_tau1dm_30'] = inc_cut + '&& l1_charge != l2_charge && abs(l1_eta) < 2.1 && abs(l2_eta) < 2.1 && mvis>70 && mvis<100 && n_jets==1 && tau1_decayModeFinding>0. && abs(tau1_dz)<0.2 && tau1_pt>30.'
# cuts['OS_PU_mZ_eq1jet_tau1dm_50'] = inc_cut + '&& l1_charge != l2_charge && abs(l1_eta) < 2.1 && abs(l2_eta) < 2.1 && mvis>70 && mvis<100 && n_jets==1 && tau1_decayModeFinding>0. && abs(tau1_dz)<0.2 && tau1_pt>50.'
# cuts['OS_PU_mZ_eq1jet_tau1dm_80'] = inc_cut + '&& l1_charge != l2_charge && abs(l1_eta) < 2.1 && abs(l2_eta) < 2.1 && mvis>70 && mvis<100 && n_jets==1 && tau1_decayModeFinding>0. && abs(tau1_dz)<0.2 && tau1_pt>80.'

# cuts['OS_PU_mZ_gr1jet_tau1dm'] = inc_cut + '&& l1_charge != l2_charge && abs(l1_eta) < 2.1 && abs(l2_eta) < 2.1 && mvis>70 && mvis<100 && n_jets>=1 && tau1_decayModeFinding>0. && abs(tau1_dz)<0.2'

cuts['OS_PU_mZ_eq1jet_tau1dm_30_pos'] = inc_cut + '&& l1_charge != l2_charge && abs(l1_eta) < 2.1 && abs(l2_eta) < 2.1 && mvis>70 && mvis<100 && n_jets==1 && tau1_decayModeFinding>0. && abs(tau1_dz)<0.2 && tau1_pt>30. && tau1_charge>0'

cuts['OS_PU_mZ_eq1jet_tau1dm_30_neg'] = inc_cut + '&& l1_charge != l2_charge && abs(l1_eta) < 2.1 && abs(l2_eta) < 2.1 && mvis>70 && mvis<100 && n_jets==1 && tau1_decayModeFinding>0. && abs(tau1_dz)<0.2 && tau1_pt>30. && tau1_charge<0'

# cuts['OS_PU_mZ_gr1jet_tau1dm0'] = inc_cut + '&& l1_charge != l2_charge && abs(l1_eta) < 2.1 && abs(l2_eta) < 2.1 && mvis>70 && mvis<100 && n_jets>=1 && tau1_decayModeFinding>0. && tau1_decayMode==0'
# cuts['OS_PU_mZ_gr1jet_tau1dm1'] = inc_cut + '&& l1_charge != l2_charge && abs(l1_eta) < 2.1 && abs(l2_eta) < 2.1 && mvis>70 && mvis<100 && n_jets>=1 && tau1_decayModeFinding>0. && tau1_decayMode==1'
# cuts['OS_PU_mZ_gr1jet_tau1dm10'] = inc_cut + '&& l1_charge != l2_charge && abs(l1_eta) < 2.1 && abs(l2_eta) < 2.1 && mvis>70 && mvis<100 && n_jets>=1 && tau1_decayModeFinding>0. && tau1_decayMode==10'

# cuts['OS_PU_mZ_gr1jet_tau1_dbmedium'] = inc_cut + '&& l1_charge != l2_charge && abs(l1_eta) < 2.1 && abs(l2_eta) < 2.1 && mvis>70 && mvis<100 && n_jets>=1 && tau1_decayModeFinding>0. && tau1_byCombinedIsolationDeltaBetaCorr3Hits>1.5'
# cuts['OS_PU_mZ_gr1jet_tau1_mvamedium'] = inc_cut + '&& l1_charge != l2_charge && abs(l1_eta) < 2.1 && abs(l2_eta) < 2.1 && mvis>70 && mvis<100 && n_jets>=1 && tau1_decayModeFinding>0. && tau1_byIsolationMVArun2v1DBoldDMwLT>3.5'

# cuts['OS_PU_mZ_gr1jet_tau1_dbmedium_lowPU'] = inc_cut + '&& l1_charge != l2_charge && abs(l1_eta) < 2.1 && abs(l2_eta) < 2.1 && mvis>70 && mvis<100  && n_jets>=1 && tau1_decayModeFinding>0. && tau1_byIsolationMVArun2v1DBoldDMwLT>3.5&& n_vertices<12'
# cuts['OS_PU_mZ_gr1jet_tau1_dbmedium_highPU'] = inc_cut + '&& l1_charge != l2_charge && abs(l1_eta) < 2.1 && abs(l2_eta) < 2.1 && mvis>70 && mvis<100  && n_jets>=1 && tau1_decayModeFinding>0. && tau1_byIsolationMVArun2v1DBoldDMwLT>3.5&& n_vertices>20'


####

# cuts['OS_PU_mZ_gr2jet'] = inc_cut + '&& l1_charge != l2_charge && abs(l1_eta) < 2.1 && abs(l2_eta) < 2.1 && mvis>70 && mvis<100 && n_jets>=2'

# cuts['OS_PU_mZ_VBF'] = inc_cut + '&& l1_charge != l2_charge && abs(l1_eta) < 2.1 && abs(l2_eta) < 2.1 && mvis>70 && mvis<100 && vbf_mjj>500. && abs(vbf_deta)>3.5 && jet2_pt>30.'

# cuts['OS_PU_mZ_VBF_puid'] = inc_cut + '&& l1_charge != l2_charge && abs(l1_eta) < 2.1 && abs(l2_eta) < 2.1 && mvis>70 && mvis<100 && vbf_mjj>500. && abs(vbf_deta)>3.5 && jet1_id_pu>0.5 && jet2_id_pu>0.5 && jet2_pt>30.'

# cuts['OS_PU_mZ_VBF_puid_tight'] = inc_cut + '&& l1_charge != l2_charge && abs(l1_eta) < 2.1 && abs(l2_eta) < 2.1 && mvis>70 && mvis<100 && vbf_mjj>500. && abs(vbf_deta)>3.5 && jet1_id_pu>2.5 && jet2_id_pu>2.5 && jet2_pt>30.'

# cuts['OS_PU_mZ_1jet_PUenriched'] = inc_cut + '&& l1_charge != l2_charge && abs(l1_eta) < 2.1 && abs(l2_eta) < 2.1 && mvis>70 && mvis<100 && jet1_pt>20 && n_jets<=1 && pthiggs<20 && met_pt<20'

# cuts['OS_PU_mZ_VBF_highPU'] = inc_cut + '&& l1_charge != l2_charge && abs(l1_eta) < 2.1 && abs(l2_eta) < 2.1 && mvis>70 && mvis<100 && vbf_mjj>500. && abs(vbf_deta)>3.5 && jet2_pt>30. && n_vertices>25'
# cuts['OS_PU_mZ_VBF_lowPU'] = inc_cut + '&& l1_charge != l2_charge && abs(l1_eta) < 2.1 && abs(l2_eta) < 2.1 && mvis>70 && mvis<100 && vbf_mjj>500. && abs(vbf_deta)>3.5 && jet2_pt>30. && n_vertices<15'

# cuts['OS_PU_mZ_relaxl1iso'] = inc_cut.replace('l1_reliso05<0.1', 'l1_reliso05<1.') + '&& l1_charge != l2_charge && abs(l1_eta) < 2.1 && mvis>80 && mvis<100'
# cuts['OS_PU_mZ_relaxl2iso'] = inc_cut.replace('l2_reliso05<0.1', 'l2_reliso05<1.') + '&& l1_charge != l2_charge && abs(l1_eta) < 2.1 && mvis>80 && mvis<100'


# cuts['OS_PU_0bjet_mZ'] = inc_cut + '&& l1_charge != l2_charge && abs(l1_eta) < 2.1 && abs(l2_eta) < 2.1 && mvis>70 && mvis<100 && n_bjets==0'
# cuts['OS_PU_0bjet_vetoZ'] = inc_cut + '&& l1_charge != l2_charge && abs(l1_eta) < 2.1 && abs(l2_eta) < 2.1 && mvis>70 && (mvis>100 || mvis<80) && n_bjets==0'
# # cuts['OS_PU_2bjet'] = inc_cut + '&& l1_charge != l2_charge && abs(l1_eta) < 2.1 && n_bjets==2'
# cuts['OS_PU_2bjet_vetoZ'] = inc_cut + '&& l1_charge != l2_charge && abs(l1_eta) < 2.1 && n_bjets==2 && (mvis>100 || mvis<80)'


samples_mc, samples_data, samples, all_samples, sampleDict = createSampleLists(analysis_dir, channel='mm', ztt_cut='(l1_gen_match == 4 && l2_gen_match == 4)', zl_cut='(l1_gen_match == 2 && l2_gen_match == 2)', zj_cut='(l1_gen_match != l2_gen_match || (l1_gen_match != 4 && l1_gen_match != 2))', data2016G=data2016G)

if qcd_from_same_sign:
    samples_qcdfromss = [s for s in samples if s.name != 'QCD']
    samples_ss = copy.deepcopy(samples_qcdfromss)

    scale = 1.06

    for sample in samples_ss:
        sample.scale = scale
        if sample.name != 'data_obs':
            # Subtract background from data
            sample.scale = -scale

    qcd = HistogramCfg(name='QCD', var=None, cfgs=samples_ss, cut=inc_cut, lumi=int_lumi)

    samples_qcdfromss.append(qcd)

# Taken from Variables.py, can get subset with e.g. getVars(['mt', 'mvis'])
variables = mumu_vars
# variables = getVars(['n_vertices'])
# variables = getVars(['l1_reliso05', 'l2_reliso05'])
# variables = [
#     VariableCfg(name='mvis', binning={'nbinsx':35, 'xmin':0, 'xmax':350}, unit='GeV', xtitle='m_{vis}')
# ]

for cut_name in cuts:
    if  qcd_from_same_sign and not 'SS' in cut_name :
        cfg_example = HistogramCfg(name='example', var=None, cfgs=samples_qcdfromss, cut=inc_cut, lumi=int_lumi, weight=total_weight)
    else:
        cfg_example = HistogramCfg(name='example', var=None, cfgs=samples, cut=inc_cut, lumi=int_lumi, weight=total_weight)
        

    cfg_example.cut = cuts[cut_name]
    if qcd_from_same_sign and 'OS' in cut_name:
        qcd.cut = cuts[cut_name].replace('l1_charge != l2_charge', 'l1_charge == l2_charge')

    
    cfg_example.vars = variables
    if qcd_from_same_sign:
        qcd.vars = variables # Can put into function but we will not want it by default if we take normalisations from e.g. high MT

    plots = createHistograms(cfg_example, verbose=True)
    for variable in variables:    
        plot = plots[variable.name]
        plot.Group('VV', ['WWTo1L1Nu2Q', 'WZTo1L1Nu2Q', 'WZTo1L3Nu', 'WZTo2L2Q', 'VVTo2L2Nu', 'ZZTo2L2Q', 'ZZTo4L'])
        plot.Group('Single t', ['T_tWch', 'TBar_tWch', 'TBarToLeptons_tch_powheg', 'TToLeptons_tch_powheg'])
        plot.Group('ZLL', ['ZL', 'ZJ'], style=plot.Hist('ZL').style)
        plot.Group('W', ['W1Jets', 'W2Jets', 'W3Jets', 'W4Jets'])
        plot.Group('Electroweak', ['W', 'VV', 'Single t'])
        base_dir = 'plotsGRew/' if data2016G else 'plots/'
        HistDrawer.draw(plot, plot_dir=base_dir+cut_name, channel='#mu#mu')

        # plot.WriteDataCard(filename='datacard_mm.root', dir='mm_' + cut_name)
