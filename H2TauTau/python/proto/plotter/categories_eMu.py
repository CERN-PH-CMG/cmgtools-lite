from CMGTools.H2TauTau.proto.plotter.categories_common import categories_common
from CMGTools.H2TauTau.proto.plotter.cut import Cut

# NEW one - to be implemented as soon as trees are there

inc_sig_e = Cut('!veto_thirdlepton && !veto_otherlepton && l1_reliso05<0.15')
inc_sig_mu = Cut('l2_reliso05<0.2')
inc_pt = Cut('(l2_pt>24 && l1_pt>13) || (l2_pt>9 && l1_pt>24')

inc_sig = inc_sig_mu & inc_sig_e

cat_Inc = str(inc_sig)

categories = {
    'Xcat_IncX': cat_Inc,
}

categories.update(categories_common)
