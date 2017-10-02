import hashlib

from array import array

# Adds MultiDraw method to ROOT.TTree
import CMGTools.H2TauTau.proto.plotter.MultiDraw

from CMGTools.H2TauTau.proto.plotter.PlotConfigs import HistogramCfg
from CMGTools.H2TauTau.proto.plotter.DataMCPlot import DataMCPlot


from CMGTools.RootTools.DataMC.Histogram import Histogram

from ROOT import TH1F, TFile, TTree, TTreeFormula


def initHist(hist, vcfg):
    hist.Sumw2()
    xtitle = vcfg.xtitle
    if vcfg.unit:
        xtitle += ' ({})'.format(vcfg.unit)
    hist.GetXaxis().SetTitle(xtitle)
    hist.SetStats(False)


def createHistograms(hist_cfg, all_stack=False, verbose=False, friend_func=None, vcfgs=None):
    '''Method to create actual histogram (DataMCPlot) instances from histogram 
    config; this version handles multiple variables via MultiDraw.
    '''
    if hist_cfg.vars:
        vcfgs = hist_cfg.vars

    if not vcfgs:
        print 'ERROR in createHistograms: No variable configs passed', hist_cfg.name

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
            hists = createHistograms(cfg, all_stack=True, vcfgs=vcfgs)
            for vcfg in vcfgs:
                hist = hists[vcfg.name]
                plot = plots[vcfg.name]
                hist._BuildStack(hist._SortedHistograms(), ytitle='Events')

                total_hist = plot.AddHistogram(cfg.name, hist.stack.totalHist.weighted, stack=True)

                if cfg.norm_cfg is not None:
                    norm_hist = createHistogram(cfg.norm_cfg, all_stack=True)
                    norm_hist._BuildStack(norm_hist._SortedHistograms(), ytitle='Events')
                    total_hist.Scale(hist.stack.integral/total_hist.Yield())

                if cfg.total_scale is not None:
                    total_hist.Scale(cfg.total_scale)
                    # print 'Scaling total', hist_cfg.name, 'by', cfg.total_scale
        else:
            # It's a sample cfg

            # Now read the tree
            file_name = '/'.join([cfg.ana_dir, cfg.dir_name, cfg.tree_prod_name, 'tree.root'])

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

            if cfg.cut_replace_func:
                norm_cut = cfg.cut_replace_func(norm_cut)
                shape_cut = cfg.cut_replace_func(norm_cut)

            if hist_cfg.weight:
                norm_cut = '({c}) * {we}'.format(c=norm_cut, we=weight)
                shape_cut = '({c}) * {we}'.format(c=shape_cut, we=weight)

            # print '#### FULL CUT ####', norm_cut

            # Initialise all hists before the multidraw
            hists = {}

            for vcfg in vcfgs:
                # plot = plots[vcfg.name]

                hname = '_'.join([hist_cfg.name, hashlib.md5(hist_cfg.cut).hexdigest(), cfg.name, vcfg.name, cfg.dir_name])
                if any(str(b) == 'xmin' for b in vcfg.binning):
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
                    print 'Histogram', cfg.name, 'already exists; adding...', cfg.dir_name
                    hist_to_add = Histogram(cfg.name, hist)
                    if not cfg.is_data:
                        hist_to_add.SetWeight(hist_cfg.lumi*cfg.xsec/cfg.sumweights)
                    plot[cfg.name].Add(hist_to_add)
                else:
                    plot_hist = plot.AddHistogram(cfg.name, hist, stack=stack)

                    if not cfg.is_data:
                        plot_hist.SetWeight(hist_cfg.lumi*cfg.xsec/cfg.sumweights)

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
            hname = '_'.join([hist_cfg.name, hashlib.md5(hist_cfg.cut).hexdigest(), cfg.name, vcfg.name, cfg.dir_name])
            if any(str(b) == 'xmin' for b in vcfg.binning):
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

            if cfg.cut_replace_func:
                norm_cut = cfg.cut_replace_func(norm_cut)
                shape_cut = cfg.cut_replace_func(norm_cut)

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
                print 'Histogram', cfg.name, 'already exists; adding...', cfg.dir_name
                hist_to_add = Histogram(cfg.name, hist)
                if not cfg.is_data:
                    hist_to_add.SetWeight(hist_cfg.lumi*cfg.xsec/cfg.sumweights)
                plot[cfg.name].Add(hist_to_add)
            else:
                plot_hist = plot.AddHistogram(cfg.name, hist, stack=stack)

                if not cfg.is_data:
                    plot_hist.SetWeight(hist_cfg.lumi*cfg.xsec/cfg.sumweights)

    plot._ApplyPrefs()
    return plot


def fillIntoTree(out_tree, branches, cfg, hist_cfg, vcfgs, total_scale, plot, verbose, friend_func):

    if isinstance(cfg, HistogramCfg):
        # Loop over sub-cfgs and fill them
        total_scale *= cfg.total_scale if cfg.total_scale else 1.
        for sub_cfg in cfg.cfgs:
            fillIntoTree(out_tree, branches, sub_cfg, cfg, vcfgs, total_scale, plot, verbose, friend_func)
        return

    file_name = '/'.join([cfg.ana_dir, cfg.dir_name, cfg.tree_prod_name, 'tree.root'])

    # Attaches tree to plot
    ttree = plot.readTree(file_name, cfg.tree_name, verbose=verbose, friend_func=friend_func)

    norm_cut = hist_cfg.cut
    shape_cut = hist_cfg.cut

    if cfg.norm_cut:
        norm_cut = cfg.norm_cut

    if cfg.shape_cut:
        shape_cut = cfg.shape_cut

    full_weight = branches[-1]

    weight = hist_cfg.weight
    if cfg.weight_expr:
        weight = '*'.join([weight, cfg.weight_expr])

    if hist_cfg.weight:
        norm_cut = '({c}) * {we}'.format(c=norm_cut, we=weight)
        shape_cut = '({c}) * {we}'.format(c=shape_cut, we=weight)

    # and this one too
    sample_weight = cfg.scale * total_scale
    if not cfg.is_data:
        sample_weight *= hist_cfg.lumi*cfg.xsec/cfg.sumweights

    formula = TTreeFormula('weight_formula', norm_cut, ttree)
    formula.GetNdata()

    # Add weight as tree variable
    # Then loop over ttree
    # And save this to the other tree
    # 

    # Create TTreeFormulas for all vars
    for var in vcfgs:
        if var.drawname != var.name:
            var.formula = TTreeFormula('formula'+var.name, var.drawname, ttree)
            var.formula.GetNdata()

    for i in xrange(ttree.GetEntries()):
        ttree.GetEntry(i)
        w = formula.EvalInstance()
        if w == 0.:
            continue
        full_weight[0] = w * sample_weight
        if abs(full_weight[0]) > 1000.:
            print "WARNING, unusually large weight", w, sample_weight
            import pdb; pdb.set_trace()
            print '\nWeight:', full_weight[0]
            print cfg.name
            print norm_cut
        for branch, var in zip(branches, vcfgs):
            branch[0] = var.formula.EvalInstance() if hasattr(var, 'formula') else getattr(ttree, var.name)
        out_tree.Fill()


    if shape_cut != norm_cut:
        print 'WARNING: different norm and shape cuts currently not supported in HistCreator.createTrees'


def createTrees(hist_cfg, out_dir, verbose=False, friend_func=None):
    '''Writes out TTrees from histogram configuration for each contribution. 
    Takes list of variables attached to histogram config (hist_cfg.vars) to 
    create branches.
    '''
    plot = DataMCPlot(hist_cfg.name) # Used to cache TTrees
    vcfgs = hist_cfg.vars
    for cfg in hist_cfg.cfgs:
        
        out_file = TFile('/'.join([out_dir, hist_cfg.name + '_' + cfg.name + '.root']), 'RECREATE')
        out_tree = TTree('tree', '')

        # Create branches for all variables
        branches = [array('f', [0.]) for i in xrange(len(vcfgs))]
        for branch_name, branch in zip([v.name for v in vcfgs], branches):
            out_tree.Branch(branch_name, branch, branch_name+'/F')

        # Create branch with full weight including lumi x cross section
        full_weight = array('f', [0.])
        out_tree.Branch('full_weight', full_weight, 'full_weight/F')
        branches.append(full_weight)

        total_scale = hist_cfg.total_scale if hist_cfg.total_scale else 1.
        fillIntoTree(out_tree, branches, cfg, hist_cfg, vcfgs, total_scale, plot, verbose, friend_func)

        out_file.cd()
        out_tree.Write()
        out_file.Write()
        out_file.Close()
    return plot

