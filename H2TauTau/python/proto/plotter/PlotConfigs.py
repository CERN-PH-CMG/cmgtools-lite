class VariableCfg(object):
    '''Configuration object for a variable.

    "binning" is a dict with either nbinsx, xmin, xmax for equidistant binning
    or nbinsx, bins=array([...]).
    '''
    def __init__(self, name='mvis', binning=None, xtitle=None, unit=None, drawname=None):
        self.name = name
        self.drawname = name if drawname is None else drawname
        self.binning = {'nbinsx':10, 'xmin':0., 'xmax':200.} if binning is None else binning
        self.unit = unit
        self.xtitle = name if xtitle is None else xtitle

    def __str__(self):
        out = 'Variable: name={name}, binning={binning}'.format(name=self.name, binning=self.binning)
        if self.drawname != self.name:
            out += ', drawname={drawname}'.format(drawname=self.drawname)
        if self.xtitle != self.name:
            out += ', xtitle={xtitle}'.format(xtitle=self.xtitle)
        if self.unit:
            out += ', unit={unit}'.format(unit=self.unit)
        return out


class SampleCfg(object):
    '''Configuration object for a sample contribution within a histogram.
    If specific properties are empty, overall defaults will be assumed.
    '''
    def __init__(self, name='Default', dir_name=None, ana_dir='', 
        tree_prod_name='H2TauTauTreeProducerTauMu', tree_name=None,
        scale=1., weight_expr=None, norm_cut=None, shape_cut=None, 
        xsec=1., sumweights=1., is_signal=False, is_data=False,
        cut_replace_func=None):
        self.name = name
        self.dir_name = name if dir_name is None else dir_name
        self.ana_dir = ana_dir
        self.tree_prod_name = tree_prod_name
        self.tree_name = 'tree' if tree_name is None else tree_name
        self.scale = scale # generic scale, e.g. scale signal by factor 5
        # a sample-specific weight expression (e.g. extra cut)),
        # multiplied with the overall histogram weight
        self.weight_expr = weight_expr 
        self.norm_cut = norm_cut
        self.shape_cut = shape_cut
        self.cut_replace_func = cut_replace_func

        self.xsec = xsec
        self.sumweights = sumweights

        self.is_signal = is_signal # To e.g. draw as separate curve (not stack)
        self.is_data = is_data # Will be drawn as data


class HistogramCfg(object):
    '''Configuration object for a histogram made up of several sub-contributions.

    A histogram can in turn have a sub-contribution from another histogram cfg. 
    '''
    def __init__(self, name='Default', var=None, vars=None, cfgs=None, cut='', lumi=1.,
                 weight='weight', norm_cfg=None, use_signal_for_stack=False,
                 total_scale=None):
        self.name = name # e.g. 'vbf tight'
        self.var = var # Single variable
        self.vars = [] if vars is None else vars # List of variable cfgs
        self.cfgs = [] if cfgs is None else cfgs # List of sample and/or histogram cfgs
        self.cut = cut
        self.lumi = lumi
        self.weight = weight
        self.use_signal_for_stack = use_signal_for_stack

        # The following two parameters are only used if this is used as a 
        # sub-contribution in a different histogram
        self.norm_cfg = norm_cfg # Different histogram cfg for normalisation
        self.total_scale = total_scale

