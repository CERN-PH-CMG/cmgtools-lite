from collections import namedtuple

from CMGTools.H2TauTau.proto.plotter.PlotConfigs import HistogramCfg, VariableCfg
from CMGTools.H2TauTau.proto.plotter.HistCreator import createHistogram

from CMGTools.H2TauTau.proto.plotter.ROCPlotter import histsToRoc, makeROCPlot

from CMGTools.H2TauTau.proto.plotter.Samples import createSampleLists

analysis_dir = '/data/steggema/mt/18112015'
samples_mc, samples_data, samples, all_samples, sampleDict = createSampleLists(analysis_dir=analysis_dir)

int_lumi = 2110.
pt1 = 19
# pt1 = 40
pt2 = 20

inc_cut = '!veto_dilepton && !veto_thirdlepton && !veto_otherlepton && l2_againstMuon3>1.5 && l2_againstElectronMVA5>0.5 && l2_pt>{pt2} && l2_decayModeFinding && l1_pt>{pt1}'.format(pt1=pt1, pt2=pt2)

vars_tau = [
    VariableCfg(name='l2_byCombinedIsolationDeltaBetaCorrRaw3Hits', drawname='l2_byCombinedIsolationDeltaBetaCorrRaw3Hits + 100 * (l2_photonPtSumOutsideSignalCone/l2_pt>0.1)', binning={'nbinsx': 10000, 'xmin': 0., 'xmax': 150.}, unit='GeV', xtitle='db corr. 3-hit iso'),
    VariableCfg(name='l2_byPileupWeightedIsolationRaw3Hits', drawname='l2_byPileupWeightedIsolationRaw3Hits + 100 * (l2_photonPtSumOutsideSignalCone/l2_pt>0.1)', binning={'nbinsx': 10000, 'xmin': 0., 'xmax': 150.}, unit='GeV', xtitle='PU corr. 3-hit iso'),
    VariableCfg(name='l2_puppi_iso_pt', drawname='l2_puppi_iso_pt + 100 * (l2_photonPtSumOutsideSignalCone/l2_pt>0.1)', binning={'nbinsx': 10000, 'xmin': 0., 'xmax': 150.}, unit='GeV', xtitle='PUPPI cone 0.5'),
    # VariableCfg(name='l2_puppi_iso04_pt', binning={'nbinsx': 10000, 'xmin': 0., 'xmax': 150.}, unit='GeV', xtitle='PUPPI cone 0.4'),
    # VariableCfg(name='l2_puppi_iso03_pt', binning={'nbinsx': 10000, 'xmin': 0., 'xmax': 150.}, unit='GeV', xtitle='PUPPI cone 0.3'),
    # VariableCfg(name='l2_byIsolationMVA3newDMwLTraw', binning={'nbinsx': 10000, 'xmin': -1., 'xmax': 1.001}, unit='GeV', xtitle='MVA new DM'),
    VariableCfg(name='l2_byIsolationMVA3oldDMwLTraw', binning={'nbinsx': 10000, 'xmin': -1., 'xmax': 1.001}, unit='GeV', xtitle='MVA old DM'),
    VariableCfg(name='l2_byPileupWeightedIsolation3Hits', binning={'nbinsx': 4, 'xmin': -0.5, 'xmax': 3.5}, unit='', xtitle='PU corr iso WPs'),
    VariableCfg(name='l2_byIsolationMVA3oldDMwLT', binning={'nbinsx': 7, 'xmin': -0.5, 'xmax': 6.5}, unit='', xtitle='MVA WPs'),
    VariableCfg(name='l2_byCombinedIsolationDeltaBetaCorr3Hits', binning={'nbinsx': 4, 'xmin': -0.5, 'xmax': 3.5}, unit='', xtitle='3-hit WPs')
]

vars_mu = [
    VariableCfg(name='l1_reliso05', binning={'nbinsx': 10000, 'xmin': 0., 'xmax': 150.}, unit='GeV', xtitle='dB iso cone 0.3'),
    VariableCfg(name='l1_reliso05_04', binning={'nbinsx': 10000, 'xmin': 0., 'xmax': 150.}, unit='GeV', xtitle='dB iso cone 0.4'),
    VariableCfg(name='l1_mini_reliso', binning={'nbinsx': 10000, 'xmin': 0., 'xmax': 150.}, unit='GeV', xtitle='Mini iso'),
    VariableCfg(name='l1_puppi_iso_pt', drawname='l1_puppi_iso_pt/l1_pt',  binning={'nbinsx': 10000, 'xmin': 0., 'xmax': 150.}, unit='GeV', xtitle='PUPPI cone 0.5'),
    VariableCfg(name='l1_puppi_iso04_pt', drawname='l1_puppi_iso04_pt/l1_pt',  binning={'nbinsx': 10000, 'xmin': 0., 'xmax': 150.}, unit='GeV', xtitle='PUPPI cone 0.4'),
    VariableCfg(name='l1_puppi_iso03_pt', drawname='l1_puppi_iso03_pt/l1_pt',  binning={'nbinsx': 10000, 'xmin': 0., 'xmax': 150.}, unit='GeV', xtitle='PUPPI cone 0.3'),
    VariableCfg(name='l1_puppi_no_muon_iso_pt', drawname='l1_puppi_no_muon_iso_pt/l1_pt', binning={'nbinsx': 10000, 'xmin': 0., 'xmax': 150.}, unit='GeV', xtitle='PUPPI n/l cone 0.5'),
    VariableCfg(name='l1_puppi_no_muon_iso04_pt', drawname='l1_puppi_no_muon_iso04_pt/l1_pt',  binning={'nbinsx': 10000, 'xmin': 0., 'xmax': 150.}, unit='GeV', xtitle='PUPPI n/l cone 0.4'),
    VariableCfg(name='l1_puppi_no_muon_iso03_pt', drawname='l1_puppi_no_muon_iso03_pt/l1_pt',  binning={'nbinsx': 10000, 'xmin': 0., 'xmax': 150.}, unit='GeV', xtitle='PUPPI n/l cone 0.3'),
    VariableCfg(name='l1_puppi_ave_iso_pt', drawname='(l1_puppi_iso_pt + l1_puppi_no_muon_iso_pt)/l1_pt', binning={'nbinsx': 10000, 'xmin': 0., 'xmax': 150.}, unit='GeV', xtitle='PUPPI ave cone 0.5'),
    VariableCfg(name='l1_puppi_ave_iso04_pt', drawname='(l1_puppi_iso04_pt + l1_puppi_no_muon_iso04_pt)/l1_pt', binning={'nbinsx': 10000, 'xmin': 0., 'xmax': 150.}, unit='GeV', xtitle='PUPPI ave cone 0.4'),
    VariableCfg(name='l1_puppi_ave_iso03_pt', drawname='(l1_puppi_iso03_pt + l1_puppi_no_muon_iso03_pt)/l1_pt', binning={'nbinsx': 10000, 'xmin': 0., 'xmax': 150.}, unit='GeV', xtitle='PUPPI ave cone 0.3'),

]

VarSet = namedtuple('VariableSet', ['name', 'vars', 'cut_s', 'cut_b'])

var_sets = [
    VarSet('tau_iso', vars_tau, '&& l2_gen_match == 5', '&& l2_gen_match == 6'),
    # VarSet('muon_iso', vars_mu, '&& (l2_gen_match == 2 || l2_gen_match == 4)', '&& l2_gen_match == 6')
]

# samples = [sampleDict['TTJets']]#, sampleDict['QCD']]

cfg_signal = HistogramCfg(name='signal', var=None, cfgs=samples, cut=inc_cut, lumi=int_lumi, weight='1.')
cfg_bg = HistogramCfg(name='bg', var=None, cfgs=samples, cut=inc_cut, lumi=int_lumi, weight='1.')


for var_set in var_sets:
    print 'Variable set', var_set.name

    cfg_signal.cut += var_set.cut_s
    cfg_bg.cut += var_set.cut_b

    rocs = []
    sig_eff = None
    bg_eff = None
    for i_var, var in enumerate(var_set.vars):
        print '  variable:', var
        cfg_signal.var = var
        cfg_bg.var = var

        plot_signal = createHistogram(cfg_signal, verbose=False)
        plot_bg = createHistogram(cfg_bg, verbose=False)

        h_signal = plot_signal.GetStack().totalHist.weighted
        h_bg = plot_bg.GetStack().totalHist.weighted

        print 'Working point at cut 1.5:'

        if not sig_eff and not bg_eff:
            sig_eff = h_signal.Integral(0, h_signal.FindBin(1.5))/h_signal.Integral(0, h_signal.GetNbinsX()+1)
            bg_eff = h_bg.Integral(0, h_bg.FindBin(1.5))/h_bg.Integral(0, h_bg.GetNbinsX()+1)
            print 'Eff sig', sig_eff
            print 'Eff bg', bg_eff
        else:
            print 'Finding cut at sig_eff =', sig_eff
            if h_signal.GetMean() > h_bg.GetMean():
                for i in reversed(range(h_signal.GetNbinsX()+1)):
                    if h_signal.Integral(i, h_signal.GetNbinsX()+1)/h_signal.Integral(0, h_signal.GetNbinsX()+1) > sig_eff:
                        print 'Found cut at eff', h_signal.Integral(i, h_signal.GetNbinsX()+1)/h_signal.Integral(0, h_signal.GetNbinsX()+1)
                        print 'Bg eff', h_bg.Integral(i, h_bg.GetNbinsX()+1)/h_bg.Integral(0, h_bg.GetNbinsX()+1)
                        print 'Cut:', h_signal.GetBinLowEdge(i)
                        break
            else:
                for i in range(h_signal.GetNbinsX()+1):
                    if h_signal.Integral(0, i)/h_signal.Integral(0, h_signal.GetNbinsX()+1) > sig_eff:
                        print 'Found cut at eff',h_signal.Integral(0, i)/h_signal.Integral(0, h_signal.GetNbinsX()+1)
                        print 'Bg eff', h_bg.Integral(0, i)/h_bg.Integral(0, h_bg.GetNbinsX()+1)
                        print 'Cut:', h_signal.GetBinLowEdge(i)
                        break


        roc = histsToRoc(h_signal, h_bg)
        roc.title = var.xtitle
        roc.name = var.name

        rocs.append(roc)

    allrocs = makeROCPlot(rocs, var_set.name, xmin=0.3, ymin=0.002, logy=True)
    # allrocs = makeROCPlot(rocs, var_set.name, xmin=0.9, ymin=0.5, logy=False)
