from CMGTools.H2TauTau.proto.plotter.cut import Cut

# pt1 = 200
# pt2 = 200

cat_lnujj_trigOrSF = "(((HLT2_MU||HLT2_ELE||HLT2_ISOMU||HLT2_ISOELE||HLT2_MET120)&&run>2000)+(run<2000)*lnujj_sf)"
cat_metFilters = "(Flag_goodVertices&&Flag_CSCTightHaloFilter&&Flag_HBHENoiseFilter&&Flag_HBHENoiseIsoFilter&&Flag_eeBadScFilter&&Flag_badChargedHadronFilter&&Flag_badMuonFilter)"
cat_lnujj_basic = "(lnujj_nOtherLeptons==0&&lnujj_l2_pruned_mass>0&&lnujj_LV_mass>600&&(abs(lnujj_l1_l_pdgId)==11||(abs(lnujj_l1_l_pdgId)==13&&lnujj_l1_l_relIso04<0.1)))"
cat_jj_basic = '(njj>0)&&lnujj_nOtherLeptons==0&&((HLT2_HT800||HLT2_HT900)&&run>2000)+(run<2000)*jj_sf&&jj_LV_mass>1000'

cat_lnujj_mu = 'abs(lnujj_l1_l_pdgId)==13'
cat_lnujj_e = 'abs(lnujj_l1_l_pdgId)==11'

cat_jj_HP = 'jj_l2_tau2/jj_l2_tau1<0.6'
cat_jj_LP = 'jj_l2_tau2/jj_l2_tau1>0.6&&jj_l2_tau2/jj_l2_tau1<0.75'
cat_lnujj_HP = 'lnujj_l2_tau2/lnujj_l2_tau1<0.45'
cat_lnujj_LP = 'lnujj_l2_tau2/lnujj_l2_tau1>0.45&&lnujj_l2_tau2/lnujj_l2_tau1<0.75'

cat_nob = 'lnujj_nMediumBTags==0'
cat_b = 'lnujj_nMediumBTags>0'

inc_metFilters = Cut(cat_metFilters)
inc_lnujj_trigOrSF = Cut(cat_lnujj_trigOrSF)
inc_lnujj_basic = Cut(cat_lnujj_basic)
inc_lnujj = inc_lnujj_trigOrSF & inc_lnujj_basic & inc_metFilters
mu_lnujj = inc_lnujj & Cut(cat_lnujj_mu)
e_lnujj = inc_lnujj & Cut(cat_lnujj_e)
inc_lnujj_HP = inc_lnujj & Cut(cat_lnujj_HP)
inc_lnujj_LP = inc_lnujj & Cut(cat_lnujj_LP)
mu_lnujj_HP = mu_lnujj & Cut(cat_lnujj_HP)
e_lnujj_HP = e_lnujj & Cut(cat_lnujj_HP)
mu_lnujj_LP = mu_lnujj & Cut(cat_lnujj_LP)
e_lnujj_LP = e_lnujj & Cut(cat_lnujj_LP)


inc_jj_basic = Cut(cat_jj_basic)
inc_jj = inc_jj_basic & inc_metFilters
inc_jj_HP = inc_jj & Cut(cat_jj_HP)
inc_jj_LP = inc_jj & Cut(cat_jj_LP)


# inc_sig_mu1 = Cut('l1_reliso05<0.1 && l1_muonid_medium>0.5 && l1_pt>{pt1}'.format(pt1=pt1))
# inc_sig_mu2 = Cut('l2_reliso05<0.1 && l2_muonid_medium>0.5 && l2_pt>{pt2}'.format(pt2=pt2))

# inc_sig = inc_sig & inc_sig_mu1 & inc_sig_mu2

cat_lnujj_inc = str(inc_lnujj)
cat_lnujj_mu = str(mu_lnujj)
cat_lnujj_e = str(e_lnujj)
cat_lnujj_inc_HP = str(inc_lnujj_HP)
cat_lnujj_mu_HP = str(mu_lnujj_HP)
cat_lnujj_e_HP = str(e_lnujj_HP)
cat_lnujj_inc_LP = str(inc_lnujj_LP)
cat_lnujj_mu_LP = str(mu_lnujj_LP)
cat_lnujj_e_LP = str(e_lnujj_LP)

cat_jj_inc = str(inc_jj)
cat_jj_inc_HP = str(inc_jj_HP)
cat_jj_inc_LP = str(inc_jj_LP)

categories = {
    'lnujj_Inclusive': cat_lnujj_inc,
    'lnujj_mu': cat_lnujj_mu,
    'lnujj_e': cat_lnujj_e,
    'lnujj_Inclusive_HP': cat_lnujj_inc_HP,
    'lnujj_mu_HP': cat_lnujj_mu_HP,
    'lnujj_e_HP': cat_lnujj_e_HP,
    'lnujj_Inclusive_LP': cat_lnujj_inc_LP,
    'lnujj_mu_LP': cat_lnujj_mu_LP,
    'lnujj_e_LP': cat_lnujj_e_LP,

    'jj_Inclusive': cat_jj_inc,
    'jj_Inclusive_HP': cat_jj_inc_HP,
    'jj_Inclusive_LP': cat_jj_inc_LP,
}

# categories.update(categories_common)
