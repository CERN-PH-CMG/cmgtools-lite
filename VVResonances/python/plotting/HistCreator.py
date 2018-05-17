import pickle

# Adds MultiDraw method to ROOT.TTree
import CMGTools.H2TauTau.proto.plotter.MultiDraw

from CMGTools.H2TauTau.proto.plotter.PlotConfigs import HistogramCfg
from CMGTools.VVResonances.plotting.DataMCPlot import DataMCPlot


from CMGTools.RootTools.DataMC.Histogram import Histogram

from ROOT import TH1F, TGraphAsymmErrors, Math, kBlack


def initHist(hist, vcfg):
    hist.Sumw2()
    xtitle = vcfg.xtitle
    if vcfg.unit:
        xtitle += ' ({})'.format(vcfg.unit)
    hist.GetXaxis().SetTitle(xtitle)
    hist.SetStats(False)


def createHistograms(hist_cfg, all_stack=False, verbose=False, friend_func=None):
    '''Method to create actual histogram (DataMCPlot) instances from histogram
    config; this version handles multiple variables via MultiDraw.
    '''
    vcfgs = hist_cfg.vars
    plots = {}

    for vcfg in vcfgs:
        plot = DataMCPlot(vcfg.name)
        plot.lumi = hist_cfg.lumi
        if vcfg.name in plots:
            print 'Adding variable with same name twice', vcfg.name, 'not yet foreseen; taking the last'
        plots[vcfg.name] = plot

    for cfg in hist_cfg.cfgs:
        # First check whether it's a sub-histo or not
        if isinstance(cfg, HistogramCfg):
            hists = createHistograms(cfg, all_stack=True)
            for vcfg in vcfgs:
                hist = hists[vcfg.name]
                plot = plots[vcfg.name]
                hist._BuildStack(hist._SortedHistograms(), ytitle=cfg.ytitle)

                total_hist = plot.AddHistogram(cfg.name, hist.stack.totalHist.weighted, stack=True)

                if cfg.norm_cfg is not None:
                    norm_hist = createHistogram(cfg.norm_cfg, all_stack=True)
                    norm_hist._BuildStack(norm_hist._SortedHistograms(), ytitle=cfg.ytitle)
                    total_hist.Scale(hist.stack.integral/total_hist.Yield())

                if cfg.total_scale is not None:
                    total_hist.Scale(cfg.total_scale)
                    # print 'Scaling total', hist_cfg.name, 'by', cfg.total_scale
        else:
            # It's a sample cfg

            # Now read the tree
            file_name = cfg.ana_dir+"/"+cfg.dir_name+".root"

            # attach the trees to the first DataMCPlot
            plot = plots[vcfgs[0].name]
            ttree = plot.readTree(file_name, cfg.tree_name, verbose=verbose, friend_func=friend_func)

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

            # Initialise all hists before the multidraw
            hists = {}

            for vcfg in vcfgs:
                # plot = plots[vcfg.name]

                hname = '_'.join([hist_cfg.name, cfg.name, vcfg.name, cfg.dir_name])
                if 'xmin' in vcfg.binning:
                    hist = TH1F(hname, '', vcfg.binning['nbinsx'],
                                vcfg.binning['xmin'], vcfg.binning['xmax'])
                else:
                    hist = TH1F(hname, '', len(vcfg.binning)-1, vcfg.binning)

                initHist(hist, vcfg)
                hists[vcfg.name] = hist

            var_hist_tuples = []

            for vcfg in vcfgs:
                # var_hist_tuples.append(('{var} >> {hist}'.format(var=vcfg.drawname, hist=hists[vcfg.name].GetName()), '1.'))
                var_hist_tuples.append('{var} >> {hist}'.format(var=vcfg.drawname, hist=hists[vcfg.name].GetName()))

            # Implement the multidraw.
            ttree.MultiDraw(var_hist_tuples, norm_cut)

            # Do another multidraw here, if needed, and reset the scales in a separate loop
            if shape_cut != norm_cut:
                scale = hist.Integral()
                ttree.Project(hname, vcfg.drawname, shape_cut)
                hist.Scale(scale/hist.Integral())

            stack = all_stack or (not cfg.is_data and not cfg.is_signal)

            # Loop again over the variables and add histograms to plots one by one
            for vcfg in vcfgs:
                hist = hists[vcfg.name]
                plot = plots[vcfg.name]

                hist.Scale(cfg.scale)

                if cfg.name in plot:
                    print 'Histogram', cfg.name, 'already exists; adding...'
                    plot[cfg.name].Add(Histogram(cfg.name, hist))
                else:
                    plot_hist = plot.AddHistogram(cfg.name, hist, stack=stack)

                if not cfg.is_data:
                    plot_hist.SetWeight(hist_cfg.lumi*cfg.xsec/cfg.sumweights)
                else:
                    convertToPoisson(hist)

    for plot in plots.itervalues():
        plot._ApplyPrefs()
    return plots


def createHistogram(hist_cfg, all_stack=False, verbose=False, friend_func=None):
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

            ttree = plot.readTree(file_name, cfg.tree_name, verbose=verbose, friend_func=friend_func)

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
            else:
                convertToPoisson(hist)

    plot._ApplyPrefs()
    return plot


def setSumWeights(sample):
    if isinstance(sample, HistogramCfg) or sample.is_data:
        return

    pckfile = '/'.join([sample.ana_dir, sample.dir_name])+'.pck'
    try:
        pckobj = pickle.load(open(pckfile, 'r'))
        weightinv = float(pckobj['events'])
        sample.sumweights = weightinv
    except IOError:
        print 'Warning: could not find sum weights information for sample', sample.name
        pass


def convertToPoisson(h):
    graph = TGraphAsymmErrors()
    q = (1-0.6827)/2.

    for i in range(1,h.GetNbinsX()+1):
        x=h.GetXaxis().GetBinCenter(i)
        xLow =h.GetXaxis().GetBinLowEdge(i)
        xHigh =h.GetXaxis().GetBinUpEdge(i)
        y=h.GetBinContent(i)
        yLow=0
        yHigh=0
        if y !=0.0:
            yLow = y-Math.chisquared_quantile_c(1-q,2*y)/2.
            yHigh = Math.chisquared_quantile_c(q,2*(y+1))/2.-y
            graph.SetPoint(i-1,x,y)
            graph.SetPointEYlow(i-1,yLow)
            graph.SetPointEYhigh(i-1,yHigh)
            graph.SetPointEXlow(i-1,0.0)
            graph.SetPointEXhigh(i-1,0.0)


    graph.SetMarkerStyle(20)
    graph.SetLineWidth(2)
    graph.SetMarkerSize(1.)
    graph.SetMarkerColor(kBlack)


    return graph
