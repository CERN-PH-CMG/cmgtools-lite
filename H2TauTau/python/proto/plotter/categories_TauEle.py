from CMGTools.H2TauTau.proto.plotter.categories_common import categories_common
from CMGTools.H2TauTau.proto.plotter.cut import Cut

pt1 = 24
pt2 = 20

inc_sig_tau = Cut(
    '!veto_dilepton && !veto_thirdlepton && !veto_otherlepton && l2_byIsolationMVArun2v1DBoldDMwLT>3.5 && l2_againstMuon3>1.5 && l2_againstElectronMVA6>0.5 && l2_pt>{pt2}'.format(pt2=pt2))

inc_sig_ele = Cut('l1_reliso05<0.1 && l1_eid_nontrigmva_tight>0.5 && l1_pt>{pt1}'.format(pt1=pt1))

inc_sig = inc_sig_ele & inc_sig_tau
cat_Inc = str(inc_sig)

categories = {
    'Xcat_IncX': cat_Inc,
}

categories.update(categories_common)
