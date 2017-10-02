from CMGTools.H2TauTau.proto.plotter.categories_common import categories_common
from CMGTools.H2TauTau.proto.plotter.cut import Cut

pt1 = 40
pt2 = 40

inc_event = Cut(
    '!veto_dilepton && !veto_thirdlepton && !veto_otherlepton'
)

inc_trigger = Cut(
    '(trigger_ditau35 && trigger_matched_ditau35) || (trigger_ditau35_combiso && trigger_matched_ditau35_combiso)'
)

inc_sig_tau1_iso = Cut(
    # 'l1_byIsolationMVArun2v1DBoldDMwLT>3.5'  # Tight WP
    'l1_byIsolationMVArun2v1DBoldDMwLT>4.5' # VTight WP
)

inc_sig_tau2_iso = Cut(
    # 'l2_byIsolationMVArun2v1DBoldDMwLT>3.5'  # Tight WP
    'l2_byIsolationMVArun2v1DBoldDMwLT>4.5'  # VTight WP
)

inc_sig_tau1_other = Cut(
    'l1_againstMuon3>0.5 && l1_againstElectronMVA6>0.5 && l1_pt>{pt1} && abs(l1_eta)<2.1'.format(pt1=pt1)
)

inc_sig_tau2_other = Cut(
    'l2_againstMuon3>0.5 && l2_againstElectronMVA6>0.5 && l2_pt>{pt2} && abs(l2_eta)<2.1'.format(pt2=pt2)
)

inc_sig = inc_event & inc_trigger & inc_sig_tau1_iso & inc_sig_tau1_other & inc_sig_tau2_iso & inc_sig_tau2_other
inc_sig_no_iso = inc_event & inc_trigger & inc_sig_tau1_other & inc_sig_tau2_other
inc_anti_iso = (~inc_sig_tau1_iso | ~inc_sig_tau2_iso) & inc_event & inc_trigger & inc_sig_tau1_other & inc_sig_tau2_other 

cat_Inc = str(inc_sig)
cat_Inc_NoIso = str(inc_sig_no_iso)
cat_Inc_AntiIso = str(inc_anti_iso)

categories = {
    'Xcat_IncX': cat_Inc,
    'Xcat_Inc_NoIsoX': cat_Inc_NoIso,
    'Xcat_Inc_AntiIsoX': cat_Inc_AntiIso,
}

categories.update(categories_common)


if __name__ == '__main__':
    
    print inc_event
    print inc_sig_tau1_iso
    print inc_sig_tau2_iso
    print inc_sig_tau1_other
    print inc_sig_tau2_other
    print ~inc_sig_tau1_iso
    print ~inc_sig_tau1_iso
    
    
    
    #for k, v in categories.items():
    #    print k, v
