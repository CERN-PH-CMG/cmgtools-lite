from CMGTools.H2TauTau.proto.plotter.categories_common import categories_common
from CMGTools.H2TauTau.proto.plotter.cut import Cut

pt1 = 23
pt2 = 23

# NEW one - to be implemented as soon as trees are there
inc_sig = Cut('!veto_dilepton && !veto_thirdlepton && !veto_otherlepton')

inc_sig_mu1 = Cut('l1_reliso05<0.15 && l1_muonid_medium>0.5 && l1_pt>{pt1}'.format(pt1=pt1))
inc_sig_mu2 = Cut('l2_reliso05<0.15 && l2_muonid_medium>0.5 && l2_pt>{pt2}'.format(pt2=pt2))

inc_sig = inc_sig & inc_sig_mu1 & inc_sig_mu2

cat_Inc = str(inc_sig)

categories = {
    'Xcat_IncX': cat_Inc,
}

categories.update(categories_common)
