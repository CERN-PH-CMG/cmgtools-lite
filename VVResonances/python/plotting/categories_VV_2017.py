"""define cuts in here and combine them."""
import itertools
# make sure you put brackets around all your statements
# since they will be multiplied intead of using logical AND
# to allow for multiplication of scale factors

# cuts already applied in selection:
# mu: etmiss > 40, e: etmiss > 80
# leptonic W pT > 200
# angular cuts:
# - DeltaR(lepton, jet) > pi/2
# - DeltaPhi(W_l, jet) > 2
# - DeltaPhi(etmiss, jet) > 2

# define a few cuts here
cut_massWlow = 65
cut_massWhigh = 85
cut_massZlow = cut_massWhigh
cut_massZhigh = 105
cut_massVlow = cut_massWlow
cut_massVhigh = cut_massZhigh
cut_massHlow = cut_massZhigh
cut_massHhigh = 135
cut_tau21HP_jj = 0.4
cut_tau21HP_lnujj = 0.55
cut_tau21LP = 0.75
cut_mjj = 1200
cut_mlnujj = 600
cut_HbbLoose = 0.3
cut_HbbMedium1 = 0.6
cut_HbbMedium2 = 0.8
cut_HbbTight = 0.9
cut_vbfDEta = 4.0
cut_vbfMass = 400

cat_lnujj_trigOrSF = "((HLT_MU||HLT_ELE||HLT_ISOMU||HLT_ISOELE||HLT_MET120)&&((run>2000*Flag_eeBadScFilter)+((run<2000)*lnujj_sf)))"
cat_metFilters = "(((run>2000*Flag_eeBadScFilter)+(run<2000))&&Flag_goodVertices&&Flag_globalTightHalo2016Filter&&Flag_HBHENoiseFilter&&Flag_HBHENoiseIsoFilter&&Flag_eeBadScFilter&&Flag_EcalDeadCellTriggerPrimitiveFilter&&Flag_BadPFMuonFilter&&Flag_BadChargedCandidateFilter&&Flag_ecalBadCalibFilter)"
cat_lnujj_basic = "(lnujj_nOtherLeptons==0&&lnujj_l2_softDrop_mass>0&&lnujj_LV_mass>{cut_mlnujj}&&((abs(lnujj_l1_l_pdgId)==11||(abs(lnujj_l1_l_pdgId)==13))))".format(cut_mlnujj=cut_mlnujj)
cat_jj_basic = 'jj_nOtherLeptons==0&&((HLT_JJ*run>2000)+(run<2000))&&(jj_LV_mass>{cut_mjj}&&jj_l1_softDrop_mass>0&&jj_l2_softDrop_mass>0)'.format(cut_mjj=cut_mjj)

cat_lnujj_mu = '(abs(lnujj_l1_l_pdgId)==13)'
cat_lnujj_e = '(abs(lnujj_l1_l_pdgId)==11)'

# tau21 cuts for VV
cat_jj_l2_NP = '(jj_l2_tau2/jj_l2_tau1>{cut_tau21LP})'.format(cut_tau21LP=cut_tau21LP)
cat_jj_l1_NP = '(jj_l1_tau2/jj_l1_tau1>{cut_tau21LP})'.format(cut_tau21LP=cut_tau21LP)
cat_jj_l2_SP = '(jj_l2_tau2/jj_l2_tau1<{cut_tau21LP})'.format(cut_tau21LP=cut_tau21LP)
cat_jj_l1_SP = '(jj_l1_tau2/jj_l1_tau1<{cut_tau21LP})'.format(cut_tau21LP=cut_tau21LP)
cat_jj_l2_HP = '(jj_l2_tau2/jj_l2_tau1<{cut_tau21HP_jj})'.format(cut_tau21HP_jj=cut_tau21HP_jj)
cat_jj_l2_LP = '(jj_l2_tau2/jj_l2_tau1>{cut_tau21HP_jj}&&jj_l2_tau2/jj_l2_tau1<{cut_tau21LP})'.format(cut_tau21HP_jj=cut_tau21HP_jj, cut_tau21LP=cut_tau21LP)
cat_jj_l1_HP = '(jj_l1_tau2/jj_l1_tau1<{cut_tau21HP_jj})'.format(cut_tau21HP_jj=cut_tau21HP_jj)
cat_jj_l1_LP = '(jj_l1_tau2/jj_l1_tau1>{cut_tau21HP_jj}&&jj_l1_tau2/jj_l1_tau1<{cut_tau21LP})'.format(cut_tau21HP_jj=cut_tau21HP_jj, cut_tau21LP=cut_tau21LP)

# mass cuts for VV
cat_jj_l2_mLowSB = '(jj_l2_softDrop_mass<{cut_massWlow})'.format(cut_massWlow=cut_massWlow)
cat_jj_l2_mW = '((jj_l2_softDrop_mass>{cut_massWlow})&&(jj_l2_softDrop_mass<{cut_massWhigh}))'.format(cut_massWlow=cut_massWlow, cut_massWhigh=cut_massWhigh)
cat_jj_l2_mZ = '((jj_l2_softDrop_mass>{cut_massZlow})&&(jj_l2_softDrop_mass<{cut_massZhigh}))'.format(cut_massZlow=cut_massZlow, cut_massZhigh=cut_massZhigh)
cat_jj_l2_mV = '((jj_l2_softDrop_mass>{cut_massVlow})&&(jj_l2_softDrop_mass<{cut_massVhigh}))'.format(cut_massVlow=cut_massVlow, cut_massVhigh=cut_massVhigh)
cat_jj_l2_mH = '((jj_l2_softDrop_mass>{cut_massHlow})&&(jj_l2_softDrop_mass<{cut_massHhigh}))'.format(cut_massHlow=cut_massHlow, cut_massHhigh=cut_massHhigh)
cat_jj_l2_mHighSB = '(jj_l2_softDrop_mass>{cut_massHhigh})'.format(cut_massHhigh=cut_massHhigh)
cat_jj_l2_veto_mV = '((jj_l2_softDrop_mass<{cut_massVlow})||(jj_l2_softDrop_mass>{cut_massVhigh}))'.format(cut_massVlow=cut_massVlow, cut_massVhigh=cut_massVhigh)
cat_jj_l1_mLowSB = '(jj_l1_softDrop_mass<{cut_massWlow})'.format(cut_massWlow=cut_massWlow)
cat_jj_l1_mW = '((jj_l1_softDrop_mass>{cut_massWlow})&&(jj_l1_softDrop_mass<{cut_massWhigh}))'.format(cut_massWlow=cut_massWlow, cut_massWhigh=cut_massWhigh)
cat_jj_l1_mZ = '((jj_l1_softDrop_mass>{cut_massZlow})&&(jj_l1_softDrop_mass<{cut_massZhigh}))'.format(cut_massZlow=cut_massZlow, cut_massZhigh=cut_massZhigh)
cat_jj_l1_mV = '((jj_l1_softDrop_mass>{cut_massVlow})&&(jj_l1_softDrop_mass<{cut_massVhigh}))'.format(cut_massVlow=cut_massVlow, cut_massVhigh=cut_massVhigh)
cat_jj_l1_mH = '((jj_l1_softDrop_mass>{cut_massHlow})&&(jj_l1_softDrop_mass<{cut_massHhigh}))'.format(cut_massHlow=cut_massHlow, cut_massHhigh=cut_massHhigh)
cat_jj_l1_mHighSB = '(jj_l1_softDrop_mass>{cut_massHhigh})'.format(cut_massHhigh=cut_massHhigh)
cat_jj_l1_veto_mV = '((jj_l1_softDrop_mass<{cut_massVlow})||(jj_l1_softDrop_mass>{cut_massVhigh}))'.format(cut_massVlow=cut_massVlow, cut_massVhigh=cut_massVhigh)

# Hbb cuts for VV
# still need to add Hbbtagger SFs
cat_jj_l2_HbbLoose = '(jj_l2_btagBOOSTED_recalc>{cut_HbbLoose})'.format(cut_HbbLoose=cut_HbbLoose)
cat_jj_l2_HbbMedium1 = '(jj_l2_btagBOOSTED_recalc>{cut_HbbMedium1})'.format(cut_HbbMedium1=cut_HbbMedium1)
cat_jj_l2_HbbMedium2 = '(jj_l2_btagBOOSTED_recalc>{cut_HbbMedium2})'.format(cut_HbbMedium2=cut_HbbMedium2)
cat_jj_l2_HbbTight = '(jj_l2_btagBOOSTED_recalc>{cut_HbbTight})'.format(cut_HbbTight=cut_HbbTight)
cat_jj_l1_HbbLoose = '(jj_l1_btagBOOSTED_recalc>{cut_HbbLoose})'.format(cut_HbbLoose=cut_HbbLoose)
cat_jj_l1_HbbMedium1 = '(jj_l1_btagBOOSTED_recalc>{cut_HbbMedium1})'.format(cut_HbbMedium1=cut_HbbMedium1)
cat_jj_l1_HbbMedium2 = '(jj_l1_btagBOOSTED_recalc>{cut_HbbMedium2})'.format(cut_HbbMedium2=cut_HbbMedium2)
cat_jj_l1_HbbTight = '(jj_l1_btagBOOSTED_recalc>{cut_HbbTight})'.format(cut_HbbTight=cut_HbbTight)
cat_jj_l1_HbbAntiLoose = '(jj_l1_btagBOOSTED_recalc<{cut_HbbLoose})'.format(cut_HbbLoose=cut_HbbLoose)
cat_jj_l1_HbbAntiMedium1 = '(jj_l1_btagBOOSTED_recalc<{cut_HbbMedium1})'.format(cut_HbbMedium1=cut_HbbMedium1)
cat_jj_l1_HbbAntiMedium2 = '(jj_l1_btagBOOSTED_recalc<{cut_HbbMedium2})'.format(cut_HbbMedium2=cut_HbbMedium2)
cat_jj_l1_HbbAntiTight = '(jj_l1_btagBOOSTED_recalc<{cut_HbbTight})'.format(cut_HbbTight=cut_HbbTight)
cat_jj_l2_HbbAntiLoose = '(jj_l2_btagBOOSTED_recalc<{cut_HbbLoose})'.format(cut_HbbLoose=cut_HbbLoose)
cat_jj_l2_HbbAntiMedium1 = '(jj_l2_btagBOOSTED_recalc<{cut_HbbMedium1})'.format(cut_HbbMedium1=cut_HbbMedium1)
cat_jj_l2_HbbAntiMedium2 = '(jj_l2_btagBOOSTED_recalc<{cut_HbbMedium2})'.format(cut_HbbMedium2=cut_HbbMedium2)
cat_jj_l2_HbbAntiTight = '(jj_l2_btagBOOSTED_recalc<{cut_HbbTight})'.format(cut_HbbTight=cut_HbbTight)


# tau21 and mass cuts for WV
cat_lnujj_NP = cat_jj_l2_NP.replace("jj_", "lnujj_")
cat_lnujj_SP = cat_jj_l2_SP.replace("jj_", "lnujj_")
cat_lnujj_HP = '(lnujj_l2_tau2/lnujj_l2_tau1<{cut_tau21HP_lnujj})'.format(cut_tau21HP_lnujj=cut_tau21HP_lnujj)
cat_lnujj_LP = '(lnujj_l2_tau2/lnujj_l2_tau1>{cut_tau21HP_lnujj}&&lnujj_l2_tau2/lnujj_l2_tau1<{cut_tau21LP})'.format(cut_tau21HP_lnujj=cut_tau21HP_lnujj, cut_tau21LP=cut_tau21LP)
cat_lnujj_mLowSB = cat_jj_l2_mLowSB.replace("jj_", "lnujj_")
cat_lnujj_mW = cat_jj_l2_mW.replace("jj_", "lnujj_")
cat_lnujj_mZ = cat_jj_l2_mZ.replace("jj_", "lnujj_")
cat_lnujj_mV = cat_jj_l2_mV.replace("jj_", "lnujj_")
cat_lnujj_mH = cat_jj_l2_mH.replace("jj_", "lnujj_")
cat_lnujj_mHighSB = cat_jj_l2_mHighSB.replace("jj_", "lnujj_")
cat_lnujj_veto_mV = cat_jj_l2_veto_mV.replace("jj_", "lnujj_")

cat_lnujj_HbbLoose = cat_jj_l2_HbbLoose.replace("jj_", "lnujj_")
cat_lnujj_HbbMedium1 = cat_jj_l2_HbbMedium1.replace("jj_", "lnujj_")
cat_lnujj_HbbMedium2 = cat_jj_l2_HbbMedium2.replace("jj_", "lnujj_")
cat_lnujj_HbbTight = cat_jj_l2_HbbTight.replace("jj_", "lnujj_")
cat_lnujj_HbbAntiLoose = cat_jj_l2_HbbAntiLoose.replace("jj_", "lnujj_")
cat_lnujj_HbbAntiMedium1 = cat_jj_l2_HbbAntiMedium1.replace("jj_", "lnujj_")
cat_lnujj_HbbAntiMedium2 = cat_jj_l2_HbbAntiMedium2.replace("jj_", "lnujj_")
cat_lnujj_HbbAntiTight = cat_jj_l2_HbbAntiTight.replace("jj_", "lnujj_")

cat_nob = '(lnujj_nMediumBTags==0)*lnujj_btagWeight'
cat_b = '(lnujj_nMediumBTags>0)*lnujj_btagWeight'

lnujj_inc_basic = '*'.join([cat_lnujj_trigOrSF, cat_lnujj_basic, cat_metFilters])
# lnujj_mu = '*'.join([lnujj_inc, cat_lnujj_mu])
# lnujj_e = '*'.join([lnujj_inc, cat_lnujj_e])
# lnujj_inc_HP = '*'.join([lnujj_inc, cat_lnujj_HP])
# lnujj_inc_LP = '*'.join([lnujj_inc, cat_lnujj_LP])
# lnujj_mu_HP = '*'.join([lnujj_inc, cat_lnujj_mu, cat_lnujj_HP])
# lnujj_mu_LP = '*'.join([lnujj_inc, cat_lnujj_mu, cat_lnujj_LP])
# lnujj_e_HP = '*'.join([lnujj_inc, cat_lnujj_e, cat_lnujj_HP])
# lnujj_e_LP = '*'.join([lnujj_inc, cat_lnujj_e, cat_lnujj_LP])

lnujj_inc = {}

lnujj_inc["lep_all"] = '1.'
lnujj_inc["lep_e"] = cat_lnujj_e
lnujj_inc["lep_mu"] = cat_lnujj_mu
lnujj_inc["reg_all"] = '1.'
lnujj_inc["reg_b"] = cat_b
lnujj_inc["reg_nob"] = cat_nob

lnujj_inc["tau21_all"] = '1'
lnujj_inc["tau21_LP"] = cat_lnujj_NP
lnujj_inc["tau21_SP"] = cat_lnujj_SP
lnujj_inc["tau21_HP"] = cat_lnujj_HP
lnujj_inc["tau21_LP"] = cat_lnujj_LP

lnujj_inc["mJJ_all"] = '1'
lnujj_inc["mJ_LowSB"] = cat_lnujj_mLowSB
lnujj_inc["mJ_V"] = cat_lnujj_mV
lnujj_inc["mJ_W"] = cat_lnujj_mW
lnujj_inc["mJ_Z"] = cat_lnujj_mZ
lnujj_inc["mJ_H"] = cat_lnujj_mH
lnujj_inc["mJ_HighSB"] = cat_lnujj_mHighSB
lnujj_inc["mJ_VetoV"] = cat_lnujj_veto_mV

lnujj_inc["Hbb_all"] = '1'
lnujj_inc["Hbb_Loose"] = cat_lnujj_HbbLoose
lnujj_inc["Hbb_Medium1"] = cat_lnujj_HbbMedium1
lnujj_inc["Hbb_Medium2"] = cat_lnujj_HbbMedium2
lnujj_inc["Hbb_Tight"] = cat_lnujj_HbbTight
lnujj_inc["Hbb_AntiLoose"] = cat_lnujj_HbbAntiLoose
lnujj_inc["Hbb_AntiMedium1"] = cat_lnujj_HbbAntiMedium1
lnujj_inc["Hbb_AntiMedium2"] = cat_lnujj_HbbAntiMedium2
lnujj_inc["Hbb_AntiTight"] = cat_lnujj_HbbAntiTight

# jj categories
jj_inc_basic = cat_jj_basic
jj_inc = '*'.join([jj_inc_basic, cat_metFilters])

jj_inc_l1 = {}
jj_inc_l2 = {}

jj_inc_l1["tau21_all"] = '1'
jj_inc_l1["tau21_NP"] = cat_jj_l1_NP
jj_inc_l1["tau21_SP"] = cat_jj_l1_SP
jj_inc_l1["tau21_HP"] = cat_jj_l1_HP
jj_inc_l1["tau21_LP"] = cat_jj_l1_LP
jj_inc_l2["tau21_all"] = '1'
jj_inc_l2["tau21_NP"] = cat_jj_l2_NP
jj_inc_l2["tau21_SP"] = cat_jj_l2_SP
jj_inc_l2["tau21_HP"] = cat_jj_l2_HP
jj_inc_l2["tau21_LP"] = cat_jj_l2_LP

jj_inc_l1["mJJ_all"] = '1'
jj_inc_l1["mJ_LowSB"] = cat_jj_l1_mLowSB
jj_inc_l1["mJ_V"] = cat_jj_l1_mV
jj_inc_l1["mJ_W"] = cat_jj_l1_mW
jj_inc_l1["mJ_Z"] = cat_jj_l1_mZ
jj_inc_l1["mJ_H"] = cat_jj_l1_mH
jj_inc_l1["mJ_HighSB"] = cat_jj_l1_mHighSB
jj_inc_l1["mJ_VetoV"] = cat_jj_l1_veto_mV
jj_inc_l2["mJJ_all"] = '1'
jj_inc_l2["mJ_LowSB"] = cat_jj_l2_mLowSB
jj_inc_l2["mJ_V"] = cat_jj_l2_mV
jj_inc_l2["mJ_W"] = cat_jj_l2_mW
jj_inc_l2["mJ_Z"] = cat_jj_l2_mZ
jj_inc_l2["mJ_H"] = cat_jj_l2_mH
jj_inc_l2["mJ_HighSB"] = cat_jj_l2_mHighSB
jj_inc_l2["mJ_VetoV"] = cat_jj_l2_veto_mV

jj_inc_l1["Hbb_all"] = '1'
jj_inc_l1["Hbb_Loose"] = cat_jj_l1_HbbLoose
jj_inc_l1["Hbb_Medium1"] = cat_jj_l1_HbbMedium1
jj_inc_l1["Hbb_Medium2"] = cat_jj_l1_HbbMedium2
jj_inc_l1["Hbb_Tight"] = cat_jj_l1_HbbTight
jj_inc_l1["Hbb_AntiLoose"] = cat_jj_l1_HbbAntiLoose
jj_inc_l1["Hbb_AntiMedium1"] = cat_jj_l1_HbbAntiMedium1
jj_inc_l1["Hbb_AntiMedium2"] = cat_jj_l1_HbbAntiMedium2
jj_inc_l1["Hbb_AntiTight"] = cat_jj_l1_HbbAntiTight
jj_inc_l2["Hbb_all"] = '1'
jj_inc_l2["Hbb_Loose"] = cat_jj_l2_HbbLoose
jj_inc_l2["Hbb_Medium1"] = cat_jj_l2_HbbMedium1
jj_inc_l2["Hbb_Medium2"] = cat_jj_l2_HbbMedium2
jj_inc_l2["Hbb_Tight"] = cat_jj_l2_HbbTight
jj_inc_l2["Hbb_AntiLoose"] = cat_jj_l2_HbbAntiLoose
jj_inc_l2["Hbb_AntiMedium1"] = cat_jj_l2_HbbAntiMedium1
jj_inc_l2["Hbb_AntiMedium2"] = cat_jj_l2_HbbAntiMedium2
jj_inc_l2["Hbb_AntiTight"] = cat_jj_l2_HbbAntiTight

categories_lnujj_inc = lnujj_inc
categories_jj_inc_l1 = {}
categories_jj_inc_l2 = {}
uniqueStrings = ["lep", "reg", "tau21", "mJ", "Hbb"]

# for lnujj allow up to five combinations
categories_lnujj_inc_2 = {'%s_%s' % (x1, x2): '*'.join([lnujj_inc[x1], lnujj_inc[x2]]) for x1, x2 in itertools.combinations(lnujj_inc, 2)}
categories_lnujj_inc_3 = {'%s_%s_%s' % (x1, x2, x3): '*'.join([lnujj_inc[x1], lnujj_inc[x2], lnujj_inc[x3]]) for x1, x2, x3 in itertools.combinations(lnujj_inc, 3)}
categories_lnujj_inc_4 = {'%s_%s_%s_%s' % (x1, x2, x3, x4): '*'.join([lnujj_inc[x1], lnujj_inc[x2], lnujj_inc[x3], lnujj_inc[x4]]) for x1, x2, x3, x4 in itertools.combinations(lnujj_inc, 4)}
categories_lnujj_inc_5 = {'%s_%s_%s_%s_%s' % (x1, x2, x3, x4, x5): '*'.join([lnujj_inc[x1], lnujj_inc[x2], lnujj_inc[x3], lnujj_inc[x4], lnujj_inc[x5]]) for x1, x2, x3, x4, x5 in itertools.combinations(lnujj_inc, 5)}
categories_lnujj_inc_2.update(categories_lnujj_inc_3)
categories_lnujj_inc_2.update(categories_lnujj_inc_4)
categories_lnujj_inc_2.update(categories_lnujj_inc_5)
for key, item in categories_lnujj_inc_2.iteritems():
    add = True
    for uniqStr in uniqueStrings:
        if key.count(uniqStr) > 1:
            add = False
            continue
    if add:
        categories_lnujj_inc[key] = item

categories_lnujj = {}
# now merge l1 and l2
for key, cut in categories_lnujj_inc.iteritems():
    categories_lnujj['lnujj_%s' % (key)] = '*'.join([cut, lnujj_inc_basic])
    # print 'lnujj_%s' % (key)

categories_jj_inc_l1 = {'l1_%s' % key: value for key, value in jj_inc_l1.iteritems()}
categories_jj_inc_l1_2 = {'l1_%s_%s' % (x1, x2): '*'.join([jj_inc_l1[x1], jj_inc_l1[x2]]) for x1, x2 in itertools.combinations(jj_inc_l1, 2)}
categories_jj_inc_l1_3 = {'l1_%s_%s_%s' % (x1, x2, x3): '*'.join([jj_inc_l1[x1], jj_inc_l1[x2], jj_inc_l1[x3]]) for x1, x2, x3 in itertools.combinations(jj_inc_l1, 3)}
categories_jj_inc_l1_2.update(categories_jj_inc_l1_3)
for key, item in categories_jj_inc_l1_2.iteritems():
    add = True
    for uniqStr in uniqueStrings:
        if key.count(uniqStr) > 1:
            add = False
            continue
    if add:
        categories_jj_inc_l1[key] = item

categories_jj_inc_l2 = {'l2_%s' % key: value for key, value in jj_inc_l2.iteritems()}
categories_jj_inc_l2_2 = {'l2_%s_%s' % (x1, x2): '*'.join([jj_inc_l2[x1], jj_inc_l2[x2]]) for x1, x2 in itertools.combinations(jj_inc_l2, 2)}
categories_jj_inc_l2_3 = {'l2_%s_%s_%s' % (x1, x2, x3): '*'.join([jj_inc_l2[x1], jj_inc_l2[x2], jj_inc_l2[x3]]) for x1, x2, x3 in itertools.combinations(jj_inc_l2, 3)}
categories_jj_inc_l2_2.update(categories_jj_inc_l2_3)
for key, item in categories_jj_inc_l2_2.iteritems():
    add = True
    for uniqStr in uniqueStrings:
        if key.count(uniqStr) > 1:
            add = False
            continue
    if add:
        categories_jj_inc_l2[key] = item

categories_jj_inc = {}
# now merge l1 and l2
for key_j1, cut_j1 in categories_jj_inc_l1.iteritems():
    for key_j2, cut_j2 in categories_jj_inc_l2.iteritems():
        categories_jj_inc['jj_inc_%s_%s' % (key_j1, key_j2)] = '*'.join([cut_j1, cut_j2, jj_inc])

categories = {
    # 'lnujj_Inclusive': lnujj_inc,
    # 'lnujj_mu': lnujj_mu,
    # 'lnujj_e': lnujj_e,
    # 'lnujj_Inclusive_HP': lnujj_inc_HP,
    # 'lnujj_mu_HP': lnujj_mu_HP,
    # 'lnujj_e_HP': lnujj_e_HP,
    # 'lnujj_Inclusive_LP': lnujj_inc_LP,
    # 'lnujj_mu_LP': lnujj_mu_LP,
    # 'lnujj_e_LP': lnujj_e_LP,

    # 'jj_Inclusive': jj_inc,
    # 'jj_Inclusive_HP': jj_inc_HP,
    # 'jj_Inclusive_LP': jj_inc_LP,
}

categories.update(categories_lnujj)
categories.update(categories_jj_inc)
# print categories


def findCategory(categories, cat="lnujj", lep=None, reg=None, tau21=None, mJ=None, Hbb=None):
    """Find cut category."""
    if lep is not None:
        if lep[0] != "_":
            lep = "_" + lep
    if reg is not None:
        if reg[0] != "_":
            reg = "_" + reg
    if tau21 is not None:
        if tau21[0] != "_":
            tau21 = "_" + tau21
    if mJ is not None:
        if mJ[0] != "_":
            mJ = "_" + mJ
    if Hbb is not None:
        if Hbb[0] != "_":
            Hbb = "_" + Hbb
    stringList = filter(None, [cat, lep, reg, tau21, mJ, Hbb])
    stringDict = {}
    stringDict["cat"] = cat
    stringDict["lep"] = lep
    stringDict["reg"] = reg
    stringDict["tau21"] = tau21
    stringDict["mJ"] = mJ
    stringDict["Hbb"] = Hbb
    vetoList = [k for k, v in stringDict.iteritems() if v is None]
    for key, item in categories.iteritems():
        if all(x in key for x in stringList) and not any(x in key for x in vetoList):
            return key
    return None


def findCut(categories, cat=None, lep=None, reg=None, tau21=None, mJ=None, Hbb=None):
    """Find cut for category."""
    return categories[findCategory(categories, cat=cat, lep=lep, reg=reg, tau21=tau21, mJ=mJ, Hbb=Hbb)]


# def findCategoryVV(categories, cat="jj", l1_tau21=None, l2_tau21=None, l1_mJ=None, l2_mJ=None, l1_Hbb=None, l2_Hbb=None):
#     """Find cut category."""
#     stringList = filter(None, [cat, l1_tau21, l2_tau21, l1_mJ, l2_mJ, l1_Hbb, l2_Hbb])
#     stringDict = {}
#     stringDict["cat"] = cat
#     stringDict["l1_tau21"] = l1_tau21
#     stringDict["l2_tau21"] = l2_tau21
#     stringDict["l1_mJ"] = l1_mJ
#     stringDict["l2_mJ"] = l2_mJ
#     stringDict["l1_Hbb"] = l1_Hbb
#     stringDict["l2_Hbb"] = l2_Hbb
#     vetoList = [k for k, v in stringDict.iteritems() if v is None]
#     for key, item in categories.iteritems():
#         if all(x in key for x in stringList) and not any(x in key for x in vetoList):
#             return key
#     return None
