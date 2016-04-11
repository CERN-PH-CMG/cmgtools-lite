import pickle

from CMGTools.H2TauTau.proto.plotter.PlotConfigs import HistogramCfg
from CMGTools.H2TauTau.proto.plotter.DataMCPlot import DataMCPlot

from CMGTools.RootTools.DataMC.Histogram import Histogram

from ROOT import TH1F

def initHist(hist, vcfg):
    hist.Sumw2()
    xtitle = vcfg.xtitle
    if vcfg.unit:
        xtitle += ' ({})'.format(vcfg.unit)
    hist.GetXaxis().SetTitle(xtitle)
    hist.SetStats(False)

def createHistogram(hist_cfg, all_stack=False, verbose=False):
    '''Method to create actual histogram (DataMCPlot) instance from histogram 
    config.
    '''
    plot = DataMCPlot(hist_cfg.var.name)
    plot.lumi = hist_cfg.lumi
    vcfg = hist_cfg.var
    for cfg in hist_cfg.cfgs:
        # First check whether it's a sub-histo or not
        if isinstance(cfg, HistogramCfg):
            hist = createHistogram(cfg, all_stack=True)
            hist._BuildStack(hist._SortedHistograms(), ytitle='Events')

            total_hist = plot.AddHistogram(cfg.name, hist.stack.totalHist.weighted, stack=True)

            if cfg.norm_cfg is not None:
                norm_hist = createHistogram(cfg.norm_cfg, all_stack=True)
                norm_hist._BuildStack(norm_hist._SortedHistograms(), ytitle='Events')
                total_hist.Scale(hist.stack.integral/total_hist.Yield())

            if cfg.total_scale is not None:
                total_hist.Scale(cfg.total_scale)
        else:
            # It's a sample cfg
            hname = '_'.join([hist_cfg.name, cfg.name, vcfg.name, cfg.dir_name])
            if 'xmin' in vcfg.binning:
                hist = TH1F(hname, '', vcfg.binning['nbinsx'], 
                    vcfg.binning['xmin'], vcfg.binning['xmax'])
            else:
                hist = TH1F(hname, '', len(vcfg.binning)-1, vcfg.binning)

            initHist(hist, vcfg)

            file_name = '/'.join([cfg.ana_dir, cfg.dir_name, cfg.tree_prod_name, 'tree.root'])

            ttree = plot.readTree(file_name, cfg.tree_name, verbose=verbose)

            norm_cut = hist_cfg.cut
            shape_cut = hist_cfg.cut

            if cfg.norm_cut:
                norm_cut = cfg.norm_cut

            if cfg.shape_cut:
                shape_cut = cfg.shape_cut

            weight = hist_cfg.weight
            if cfg.weight_expr:
                weight = '*'.join([weight, cfg.weight_expr])

            if hist_cfg.weight:
                norm_cut = '({c}) * {we}'.format(c=norm_cut, we=weight)
                shape_cut = '({c}) * {we}'.format(c=shape_cut, we=weight)


            ttree.Project(hname, vcfg.drawname, norm_cut)

            if shape_cut != norm_cut:
                scale = hist.Integral()
                ttree.Project(hname, vcfg.drawname, shape_cut)
                hist.Scale(scale/hist.Integral())

            stack = all_stack or (not cfg.is_data and not cfg.is_signal)

            hist.Scale(cfg.scale)

            if cfg.name in plot:
                plot[cfg.name].Add(Histogram(cfg.name, hist))
            else:
                plot_hist = plot.AddHistogram(cfg.name, hist, stack=stack)

            if not cfg.is_data:
                plot_hist.SetWeight(hist_cfg.lumi*cfg.xsec/cfg.sumweights)

    plot._ApplyPrefs()
    return plot

def setSumWeights(sample, weight_dir='MCWeighter'):
    if isinstance(sample, HistogramCfg) or sample.is_data:
        return

    pckfile = '/'.join([sample.ana_dir, sample.dir_name, weight_dir, 'SkimReport.pck'])
    try:
        pckobj  = pickle.load(open(pckfile,'r'))
        counters = dict(pckobj)
        if 'Sum Weights' in counters:
            sample.sumweights = counters['Sum Weights']
    except IOError:
        print 'Warning: could not find sum weights information for sample', sample.name
        pass
        

class StitchingWeightForW(object):

    def __init__(self, Ninc=0, N1=0, N2=0, N3=0, N4=0):

        self.kFactor = 1.22125248
        self.SampleDict = {
            'WJetsToLNu_LO':{'LOxs':50380},
            'W1JetsToLNu_LO':{'LOxs':9644.5},
            'W2JetsToLNu_LO':{'LOxs':3144.5},
            'W3JetsToLNu_LO':{'LOxs':954.8},
            'W4JetsToLNu_LO':{'LOxs':485.6},
            }

        self.effL_inc   = Ninc/self.sampleDict['WJetsToLNu_LO']['LOxs']
        self.effL_1jet  = N1/self.sampleDict['W1JetsToLNu_LO']['LOxs']
        self.effL_2jet  = N2/self.sampleDict['W2JetsToLNu_LO']['LOxs']
        self.effL_3jet  = N3/self.sampleDict['W3JetsToLNu_LO']['LOxs']
        self.effL_4jet  = N4/self.sampleDict['W4JetsToLNu_LO']['LOxs']

        self.effL = [
                     self.effL_1jet, 
                     self.effL_2jet, 
                     self.effL_3jet, 
                     self.effL_4jet
                     ]

    def returnWeight(self, Nparton):
        
        if Nparton < 0 or Nparton > 4:
            print '[ERROR] Not correct Nparton'
        
        if Nparton==0: 
            return self.kFactor/self.effL_inc
        else:
            return self.kFactor/(self.effL_inc + self.effL[Nparton-1])
        


class StitchingWeightForDY(object):

    def __init__(self, Ninc=0, Ninc_ext=0, N1=0, N2=0, N3=0, N4=0, Nhigh=0):

        self.kFactor = 1.21622931

        self.SampleDict = {
            'DYJetsToLL_M50_LO':{'LOxs':4954},
            'DY1JetsToLL_M50_LO':{'LOxs':1012.5},
            'DY2JetsToLL_M50_LO':{'LOxs':332.8},
            'DY3JetsToLL_M50_LO':{'LOxs':101.8},
            'DY4JetsToLL_M50_LO':{'LOxs':54.8},
            'DYJetsToTauTau_M150_LO':{'LOxs':6.7}
        }

        
        self.effL_inc   = Ninc/self.sampleDict['DYJetsToLNu_LO']['LOxs']
        self.effL_inc_ext   = Ninc_ext/self.sampleDict['DYJetsToLNu_LO']['LOxs']
        self.effL_high = Nhigh/self.sampleDict['DYJetsToTauTau_M150_LO']['LOxs']
        self.effL_1jet  = N1/self.sampleDict['DY1JetsToLNu_LO']['LOxs']
        self.effL_2jet  = N2/self.sampleDict['DY2JetsToLNu_LO']['LOxs']
        self.effL_3jet  = N3/self.sampleDict['DY3JetsToLNu_LO']['LOxs']
        self.effL_4jet  = N4/self.sampleDict['DY4JetsToLNu_LO']['LOxs']

         self.effL = [
                      self.effL_1jet,
                      self.effL_2jet,
                      self.effL_3jet, 
                      self.effL_4jet, 
                      ]

    def returnWeight(self, Nparton, Mass, Decay):
        
        if Nparton < 0 or Nparton > 4:
            print '[ERROR] Not correct Nparton'

        if Decay=='TauTau':
            if Nparton==0: 
                if Mass < 150: 
                    return self.kFactor/(self.effL_inc + self.effL_inc_ext)
                else: 
                    return self.kFactor/(self.effL_inc + self.effL_inc_ext + self.effL_high)
            else:
                if Mass < 150: 
                    return self.kFactor/(self.effL_inc + self.effL_inc_ext + self.effL[Nparton-1])
                else: 
                    return self.kFactor/(self.effL_inc + self.effL_inc_ext + self.effL[Nparton-1] + self.effL_high)
                
        else:
            if Nparton==0: 
                if Mass < 150: 
                    return self.kFactor/(self.effL_inc + self.effL_inc_ext)
            else:
                if Mass < 150: 
                    return self.kFactor/(self.effL_inc + self.effL_inc_ext + self.effL[Nparton-1])

        
