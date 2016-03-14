from CMGTools.H2TauTau.proto.plotter.categories_common import categories_common
from CMGTools.H2TauTau.proto.plotter.cut import Cut

pt1 = 40
pt2 = 40

inc_sig_tau1 = Cut(
    '!veto_dilepton && !veto_thirdlepton && !veto_otherlepton && l1_byIsolationMVArun2v1DBoldDMwLT>3.5 && l1_againstMuon3>1.5 && l1_againstElectronMVA6>0.5 && l1_pt>{pt1}'.format(pt1=pt1))

inc_sig_tau2 = Cut(
    'l2_byIsolationMVArun2v1DBoldDMwLT>3.5 && l2_againstMuon3>1.5 && l2_againstElectronMVA6>0.5 && l2_pt>{pt2}'.format(pt2=pt2))


inc_sig = inc_sig_tau1 & inc_sig_tau2

cat_Inc = str(inc_sig)

categories = {
    'Xcat_IncX': cat_Inc,
}

categories.update(categories_common)
