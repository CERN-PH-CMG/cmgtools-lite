import copy

from CMGTools.H2TauTau.proto.plotter.PlotConfigs import HistogramCfg, VariableCfg
from CMGTools.H2TauTau.proto.plotter.categories_TauMu import cat_Inc
from CMGTools.H2TauTau.proto.plotter.HistCreator import createHistogram
from CMGTools.H2TauTau.proto.plotter.HistDrawer import HistDrawer
from CMGTools.H2TauTau.proto.plotter.Variables import all_vars, getVars
from CMGTools.H2TauTau.proto.plotter.helper_methods import getPUWeight

from CMGTools.H2TauTau.proto.plotter.Samples import createSampleLists

int_lumi = 2094.2 # from Alexei's email

total_weight = 'weight * ' + getPUWeight()
# total_weight = 'weight'

print total_weight

cuts = {}

inc_cut = '&&'.join([cat_Inc])
inc_cut += '&& l2_decayModeFinding'

cuts['inclusive'] = inc_cut + '&& l1_charge != l2_charge && !(met_pt < 0.15 && met_phi > 0. && met_phi < 1.8)'

# cuts['lowMT'] = cuts['inclusive'] + '&& mt < 20'
# cuts['verylowMT'] = cuts['inclusive'] + '&& mt < 5'

# cuts['inclusive_taumva_mupuppi'] = cuts['inclusive'].replace('l2_byCombinedIsolationDeltaBetaCorr3Hits>1.5', 'l2_byIsolationMVA3oldDMwLT>4.5').replace('l1_reliso05<0.1', '(l1_puppi_iso04_pt + l1_puppi_no_muon_iso04_pt)/l1_pt<0.284')

# cuts['lowMT'] = cuts['inclusive'] + '&& mt < 40'
# cuts['highMT'] = cuts['inclusive'] + '&& mt > 40'

# cuts['inclusive_mupuppi'] = cuts['inclusive'].replace('l1_reliso05<0.1', '(l1_puppi_iso04_pt + l1_puppi_no_muon_iso04_pt)/l1_pt<0.284')
# cuts['inclusive_taupuppi'] = cuts['inclusive'].replace('l2_byCombinedIsolationDeltaBetaCorr3Hits>1.5', 'l2_puppi_iso_pt<1.8')

# cuts['inclusive_taumva'] = cuts['inclusive'].replace('l2_byCombinedIsolationDeltaBetaCorr3Hits>1.5', 'l2_byIsolationMVA3oldDMwLT>4.5')

# cuts['inclusive_taumva_mupuppi'] = cuts['inclusive'].replace('l2_byCombinedIsolationDeltaBetaCorrRaw3Hits<1.5', 'l2_byIsolationMVA3oldDMwLTraw>0.848').replace('l1_reliso05<0.1', '(l1_puppi_iso04_pt + l1_puppi_no_muon_iso04_pt)/l1_pt<0.284')

# cuts['highMT_taumva_mupuppi'] = cuts['inclusive_taumva_mupuppi'] + '&& mt > 40'
# cuts['lowMT_taumva_mupuppi'] = cuts['inclusive_taumva_mupuppi'] + '&& mt < 40'

# cuts['inclusive_taupuweighted'] = cuts['inclusive'].replace('l2_byCombinedIsolationDeltaBetaCorrRaw3Hits<1.5', 'l2_byPileupWeightedIsolationRaw3Hits<1.')

# del cuts['inclusive']
# del cuts['inclusive_taumva_mupuppi']

# cuts['OSlowMT'] = inc_cut + '&& l1_charge != l2_charge && mt<40'
# cuts['SSlowMT'] = inc_cut + '&& l1_charge == l2_charge && mt<40'

# cuts['OShighMT'] = inc_cut + '&& l1_charge != l2_charge && mt>40'
# cuts['SShighMT'] = inc_cut + '&& l1_charge == l2_charge && mt>40'

# new_cuts = {}

# for cut in cuts:
#     new_cuts[cut.replace('inclusive', 'SS')] = cuts[cut].replace('l1_charge != l2_charge', 'l1_charge == l2_charge')

# inv_cuts = {}
# for cut in cuts:
#     new_cuts[cut+'invmu'] = cuts[cut].replace('l1_reliso05<0.1', 'l1_reliso05>0.1')
#     new_cuts[cut+'invtau'] = cuts[cut].replace('l2_byCombinedIsolationDeltaBetaCorr3Hits>1.5', 'l2_byCombinedIsolationDeltaBetaCorr3Hits<1.5')

# # cuts = inv_cuts

# cuts = cuts.copy()
# cuts.update(inv_cuts)
# cuts.update(new_cuts)

qcd_from_same_sign = True

analysis_dir = '/data/steggema/mt/18112015'
samples_mc, samples_data, samples, all_samples, sampleDict = createSampleLists(analysis_dir=analysis_dir)

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
variables = all_vars
# variables = getVars(['_norm_', 'mt', 'mvis', 'l1_pt', 'l2_pt', 'l1_eta', 'l2_eta', 'n_vertices', 'n_jets', 'n_bjets'])

variables = getVars(['_norm_', 'mt', 'mvis', 'n_vertices'])

# variables = getVars(['_norm_', 'met_pt', 'met_phi'])

# variables = getVars(['_norm_'])
# variables = [
#     VariableCfg(name='mvis', binning={'nbinsx':35, 'xmin':0, 'xmax':350}, unit='GeV', xtitle='m_{vis}')
# ]

for cut_name in cuts:
    if qcd_from_same_sign and not 'SS' in cut_name :
        cfg_example = HistogramCfg(name='example', var=None, cfgs=samples_qcdfromss, cut=inc_cut, lumi=int_lumi, weight=total_weight)
    else:
        cfg_example = HistogramCfg(name='example', var=None, cfgs=samples, cut=inc_cut, lumi=int_lumi, weight=total_weight)
        

    cfg_example.cut = cuts[cut_name]
    if qcd_from_same_sign and not 'SS' in cut_name:
        qcd.cut = cuts[cut_name].replace('l1_charge != l2_charge', 'l1_charge == l2_charge')

    for variable in variables:
        cfg_example.var = variable
        if qcd_from_same_sign:
            qcd.var = variable # Can put into function but we will not want it by default if we take normalisations from e.g. high MT
        
        plot = createHistogram(cfg_example, verbose=True)
        plot.Group('VV', ['ZZ', 'WZ', 'WW', 'T_tWch', 'TBar_tWch'])
        # plot.Group('Single t', ['T_tWch', 'TBar_tWch', 'TToLeptons_sch', 'TToLeptons_tch'])
        # plot.Group('ZLL', ['Ztt_ZL', 'Ztt_ZJ'], style=plot.Hist('Ztt_ZL').style)
        HistDrawer.draw(plot, plot_dir='plots/RemoveLowMET_'+cut_name)

        plot.WriteDataCard(filename='datacard_mvis.root', dir='mt_' + cut_name)
