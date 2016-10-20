cat_VBF = 'n_jets>=2 && vbf_n_central==0 && vbf_mjj > 500 && abs(vbf_deta) > 3.5'
cat_VBF_Rel_30 = 'n_jets>=2 && n_bjets==0 && vbf_n_central==0 && vbf_mjj>200 && abs(vbf_deta) > 2.'
cat_VBF_Rel_20 = 'n_jets_20>=2 && n_bjets==0 && vbf_n_central==0 && vbf_mjj>200 && abs(vbf_deta) > 2.'

cat_J2 = 'n_jets>=2'
# cat_VH  = 'n_jets>=2 && VBF_mjj>60 && VBF_mjj<120 && VBF_dijetpt>150 && VBF_mva<0.5 && nBJets==0'
cat_J1  = 'n_jets>=1 && !({VBF}) && n_bjets==0'.format(VBF=cat_VBF)
#cat_J1  = 'n_jets>=1 && nBJets==0' #Jose
cat_J1B = 'nBJets>=1 && n_jets<2'
cat_J0 = 'n_jets==0 && n_bjets==0' # Jose
#cat_J0  = '!({VBF}) && !({J1}) && !({J1B}) && n_jets==0'.format(VBF=cat_VBF,
#                                                               J1=cat_J1,
#                                                               J1B=cat_J1B)

cat_J1B_Rel_CSVL = 'nCSVLJets>=1 && n_jets<2'

cat_1BInclusive = 'nBJets>=1'
cat_0B = 'nBJets==0'

cat_J0_high = cat_J0 + ' && l1_pt>45.'
cat_J0_medium = cat_J0 + ' && l1_pt>30. && l1_pt<=45.'
cat_J0_low = cat_J0 + ' && l1_pt>20. && l1_pt<=30.'

cat_J1_high_mediumhiggs = cat_J1 + ' && l1_pt>45. && pthiggs>100.'
cat_J1_high_lowhiggs = cat_J1 + ' && l1_pt>45. && pthiggs<100.'
cat_J1_medium = cat_J1 + ' && l1_pt>30. && l1_pt<=45.'

cat_J1_oldlow = cat_J1 + ' && l1_pt<=40.'
cat_J1_oldhigh = cat_J1 + ' && l1_pt>40.'

cat_J0_oldlow = cat_J0 + ' && l1_pt<=40.'
cat_J0_oldhigh = cat_J0 + ' && l1_pt>40.'

cat_VBF_tight = 'n_jets>=2 && l1_pt>30. && nBJets==0 && VBF_nCentral==0 && VBF_mjj>700 && abs(VBF_deta)>4. && pthiggs>100.'
cat_VBF_loose = cat_VBF + ' && l1_pt>30. && nBJets==0 && !({VBF_tight})'.format(VBF_tight=cat_VBF_tight)
cat_J2B0 = 'n_jets>=2 && l1_pt>30. && nBJets==0'

def replaceCategories(cutstr, categories):
    for catname, cat in categories.iteritems():
        cutstr = cutstr.replace( catname, cat )
    return cutstr

categories_common = {
    'Xcat_VBFX':cat_VBF,
    'Xcat_VBF_Rel_30X':cat_VBF_Rel_30,
    'Xcat_VBF_Rel_20X':cat_VBF_Rel_20,
    'Xcat_J2X':cat_J2,
    'Xcat_J2B0X':cat_J2B0,
    'Xcat_J1X':cat_J1,
    'Xcat_J1BX':cat_J1B,
    'Xcat_J0X':cat_J0,
    # The following are the Summer 13 categories
    'Xcat_J0_highX':cat_J0_high,
    'Xcat_J0_mediumX':cat_J0_medium,
    'Xcat_J0_lowX':cat_J0_low,
    'Xcat_J1_high_mediumhiggsX':cat_J1_high_mediumhiggs,
    'Xcat_J1_high_lowhiggsX':cat_J1_high_lowhiggs,
    'Xcat_J1_mediumX':cat_J1_medium,
    'Xcat_VBF_tightX':cat_VBF_tight,
    'Xcat_VBF_looseX':cat_VBF_loose,
    'Xcat_J0_oldlowX':cat_J0_oldlow,
    'Xcat_J0_oldhighX':cat_J0_oldhigh,
    'Xcat_J1_oldlowX':cat_J1_oldlow,
    'Xcat_J1_oldhighX':cat_J1_oldhigh,
    'Xcat_1BInclusiveX':cat_1BInclusive,
    'Xcat_0BX':cat_0B,
    'Xcat_J1B_Rel_CSVLX':cat_J1B_Rel_CSVL
    }
