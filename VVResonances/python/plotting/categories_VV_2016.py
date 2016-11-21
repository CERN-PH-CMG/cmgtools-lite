# define cuts in here and combine them

# make sure you put brackets around all your statements
# since they will be multiplied intead of using logical AND
# to allow for multiplication of scale factors

cat_lnujj_trigOrSF = "(((HLT2_MU||HLT2_ELE||HLT2_ISOMU||HLT2_ISOELE||HLT2_MET120)&&run>2000)+((run<2000)*lnujj_sf))"
cat_metFilters = "(Flag_goodVertices&&Flag_CSCTightHaloFilter&&Flag_HBHENoiseFilter&&Flag_HBHENoiseIsoFilter&&Flag_eeBadScFilter&&Flag_badChargedHadronFilter&&Flag_badMuonFilter)"
cat_lnujj_basic = "(lnujj_nOtherLeptons==0&&lnujj_l2_pruned_mass>0&&lnujj_LV_mass>600&&(abs(lnujj_l1_l_pdgId)==11||(abs(lnujj_l1_l_pdgId)==13&&lnujj_l1_l_relIso04<0.1)))"
cat_jj_basic = 'lnujj_nOtherLeptons==0&&((HLT2_HT800||HLT2_HT900)&&run>2000)+(run<2000)*jj_sf&&jj_LV_mass>1000'

cat_lnujj_mu = '(abs(lnujj_l1_l_pdgId)==13)'
cat_lnujj_e = '(abs(lnujj_l1_l_pdgId)==11)'

cat_jj_HP = '(jj_l2_tau2/jj_l2_tau1<0.6)'
cat_jj_LP = '(jj_l2_tau2/jj_l2_tau1>0.6&&jj_l2_tau2/jj_l2_tau1<0.75)'
cat_lnujj_HP = '(lnujj_l2_tau2/lnujj_l2_tau1<0.4)'
cat_lnujj_LP = '(lnujj_l2_tau2/lnujj_l2_tau1>0.4&&lnujj_l2_tau2/lnujj_l2_tau1<0.75)'

cat_nob = '(lnujj_nMediumBTags==0)*lnujj_btagWeight'
cat_b = '(lnujj_nMediumBTags>0)*lnujj_btagWeight'

lnujj_inc = '*'.join([cat_lnujj_trigOrSF, cat_lnujj_basic, cat_metFilters])
lnujj_mu = '*'.join([lnujj_inc, cat_lnujj_mu])
lnujj_e = '*'.join([lnujj_inc, cat_lnujj_e])
lnujj_inc_HP = '*'.join([lnujj_inc, cat_lnujj_HP])
lnujj_inc_LP = '*'.join([lnujj_inc, cat_lnujj_LP])
lnujj_mu_HP = '*'.join([lnujj_inc, cat_lnujj_mu, cat_lnujj_HP])
lnujj_mu_LP = '*'.join([lnujj_inc, cat_lnujj_mu, cat_lnujj_LP])
lnujj_e_HP = '*'.join([lnujj_inc, cat_lnujj_e, cat_lnujj_HP])
lnujj_e_LP = '*'.join([lnujj_inc, cat_lnujj_e, cat_lnujj_LP])

jj_inc_basic = cat_jj_basic
jj_inc = '*'.join([jj_inc_basic, cat_metFilters])
jj_inc_HP = '*'.join([jj_inc, cat_jj_HP])
jj_inc_LP = '*'.join([jj_inc, cat_jj_LP])

categories = {
    'lnujj_Inclusive': lnujj_inc,
    'lnujj_mu': lnujj_mu,
    'lnujj_e': lnujj_e,
    'lnujj_Inclusive_HP': lnujj_inc_HP,
    'lnujj_mu_HP': lnujj_mu_HP,
    'lnujj_e_HP': lnujj_e_HP,
    'lnujj_Inclusive_LP': lnujj_inc_LP,
    'lnujj_mu_LP': lnujj_mu_LP,
    'lnujj_e_LP': lnujj_e_LP,

    'jj_Inclusive': jj_inc,
    'jj_Inclusive_HP': jj_inc_HP,
    'jj_Inclusive_LP': jj_inc_LP,
}

# categories.update(categories_common)
