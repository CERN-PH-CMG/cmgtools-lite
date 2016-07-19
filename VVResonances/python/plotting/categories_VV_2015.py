from CMGTools.H2TauTau.proto.plotter.cut import Cut

# pt1 = 200
# pt2 = 200

cat_VV = '(njj>0)'
cat_common = '(HLT_HT800||HLT_HT900)&&Flag_goodVertices&&Flag_CSCTightHaloFilter&&Flag_HBHENoiseFilter&&Flag_HBHENoiseIsoFilter&&Flag_eeBadScFilter&&jj_nOtherLeptons==0'
cat_mu = '(HLT_MU||HLT_ELE)&&abs(lnujj_l1_l_pdgId)==13'
cat_e = '(HLT_MU||HLT_ELE)&&abs(lnujj_l1_l_pdgId)==11'
cat_HP = 'lnujj_l2_tau2/lnujj_l2_tau1<0.6'
cat_LP = 'lnujj_l2_tau2/lnujj_l2_tau1>0.6&&lnujj_l2_tau2/lnujj_l2_tau1<0.75'
cat_nob = 'lnujj_nMediumBTags==0'
cat_b = 'lnujj_nMediumBTags>0'


inc_common = Cut(cat_common)
inc_VV = Cut(cat_VV)
inc_sig = inc_common & inc_VV

# inc_sig_mu1 = Cut('l1_reliso05<0.1 && l1_muonid_medium>0.5 && l1_pt>{pt1}'.format(pt1=pt1))
# inc_sig_mu2 = Cut('l2_reliso05<0.1 && l2_muonid_medium>0.5 && l2_pt>{pt2}'.format(pt2=pt2))

# inc_sig = inc_sig & inc_sig_mu1 & inc_sig_mu2

cat_Inc = str(inc_sig)

categories = {
    'Inclusive': cat_Inc,
}

# categories.update(categories_common)
