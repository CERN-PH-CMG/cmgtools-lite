import sys, re

allcats={
"b2lss_1tau" : "b2lss_1tau=ttH_2lss_1tau.card.txt",
"b2lss_ee_0tau_neg" : "b2lss_ee_0tau_neg=ttH_2lss_ee_0tau_neg.card.txt",
"b2lss_ee_0tau_pos" : "b2lss_ee_0tau_pos=ttH_2lss_ee_0tau_pos.card.txt",
"b2lss_em_0tau_bl_neg" : "b2lss_em_0tau_bl_neg=ttH_2lss_em_0tau_bl_neg.card.txt",
"b2lss_em_0tau_bl_pos" : "b2lss_em_0tau_bl_pos=ttH_2lss_em_0tau_bl_pos.card.txt",
"b2lss_em_0tau_bt_neg" : "b2lss_em_0tau_bt_neg=ttH_2lss_em_0tau_bt_neg.card.txt",
"b2lss_em_0tau_bt_pos" : "b2lss_em_0tau_bt_pos=ttH_2lss_em_0tau_bt_pos.card.txt",
"b2lss_mm_0tau_bl_neg" : "b2lss_mm_0tau_bl_neg=ttH_2lss_mm_0tau_bl_neg.card.txt",
"b2lss_mm_0tau_bl_pos" : "b2lss_mm_0tau_bl_pos=ttH_2lss_mm_0tau_bl_pos.card.txt",
"b2lss_mm_0tau_bt_neg" : "b2lss_mm_0tau_bt_neg=ttH_2lss_mm_0tau_bt_neg.card.txt",
"b2lss_mm_0tau_bt_pos" : "b2lss_mm_0tau_bt_pos=ttH_2lss_mm_0tau_bt_pos.card.txt",
"b3l_bl_neg" : "b3l_bl_neg=ttH_3l_bl_neg.card.txt",
"b3l_bl_pos" : "b3l_bl_pos=ttH_3l_bl_pos.card.txt",
"b3l_bt_neg" : "b3l_bt_neg=ttH_3l_bt_neg.card.txt",
"b3l_bt_pos" : "b3l_bt_pos=ttH_3l_bt_pos.card.txt",
}

torun={}
for reg in sys.argv[2:]:
    for cat in allcats:
        if re.match(reg,cat): torun[cat]=allcats[cat]

print 'echo Will join to %s these cards:'%(sys.argv[1],), torun

print 'combineCards.py %s > %s.txt'%( ' '.join([torun[x] for x in torun]), sys.argv[1] )
print 'text2workspace.py -o %s.root %s.txt'%(sys.argv[1],sys.argv[1])
