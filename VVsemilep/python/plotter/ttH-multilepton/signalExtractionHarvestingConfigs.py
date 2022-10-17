processes = {
    'Fakes' : ['data_fakes', 'fakes_mc'],
    'Flips' : ['data_flips'],
    'Conv'  : ['Conv'],
    'TT+jets' : ['TT'],
    'Rares' : ['Rares'],
    'ZZ'    : ['ZZ'],
    'WZ'    : ['WZ'],
    'TTW TTWW' : ['TTW','TTWW'],
    'Other Higgs'    : ['HH', 'VH', 'TTWH',"TTWH", "TTZH", "qqH", "VH", "WH", "ZH", "ggH"],
    'tH' : ['tHq','tHW'],
    'ttH' : ['ttH'],
    'ttZ' : ['TTZ'],
    'DY'  : ['DY'],

}
signals='ttH,tHW,tHq'.split(',')

regionMappingFortables = {
    '0l 2tau'   : ['ttH_0l_2tau_2016','ttH_0l_2tau_2017','ttH_0l_2tau_2018'],
    '1l 1tau'   : ['ttH_1l_1tau_2016','ttH_1l_1tau_2017','ttH_1l_1tau_2018'],
    '1l 2tau'   : ['ttH_1l_2tau_2016','ttH_1l_2tau_2017','ttH_1l_2tau_2018'],
    '2l 2tau'   : ['ttH_2l_2tau_2016','ttH_2l_2tau_2017','ttH_2l_2tau_2018'],
    '2los 1tau' : ['ttH_2los_1tau_2016','ttH_2los_1tau_2017','ttH_2los_1tau_2018'],
    '3l 1tau'   : ['ttH_3l_1tau_2016','ttH_3l_1tau_2017','ttH_3l_1tau_2018'],
    '4l'        : ['ttH_4l_2017','ttH_4l_2016','ttH_4l_2018'],
    'cr 4l'     : ['ttH_cr_4l_2016','ttH_cr_4l_2017','ttH_cr_4l_2018'],
    'cr 3l'     : ['ttH_cr_3l_2016_eee_cr','ttH_cr_3l_2016_eem_cr','ttH_cr_3l_2016_emm_cr','ttH_cr_3l_2016_mmm_cr','ttH_cr_3l_2017_eee_cr','ttH_cr_3l_2017_eem_cr','ttH_cr_3l_2017_emm_cr','ttH_cr_3l_2017_mmm_cr','ttH_cr_3l_2018_eee_cr','ttH_cr_3l_2018_eem_cr','ttH_cr_3l_2018_emm_cr','ttH_cr_3l_2018_mmm_cr'],

    # separated regions for AN                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
    '3l 0tau rest' : ['ttH_3l_0tau_rest_eem_bl_2016','ttH_3l_0tau_rest_eem_bl_2017','ttH_3l_0tau_rest_eem_bl_2018','ttH_3l_0tau_rest_emm_bl_2016','ttH_3l_0tau_rest_emm_bl_2017','ttH_3l_0tau_rest_emm_bl_2018','ttH_3l_0tau_rest_mmm_bl_2016','ttH_3l_0tau_rest_mmm_bl_2018','ttH_3l_0tau_rest_eee_2016','ttH_3l_0tau_rest_eee_2017','ttH_3l_0tau_rest_eee_2018','ttH_3l_0tau_rest_eem_bt_2016','ttH_3l_0tau_rest_eem_bt_2017','ttH_3l_0tau_rest_eem_bt_2018','ttH_3l_0tau_rest_emm_bt_2016','ttH_3l_0tau_rest_emm_bt_2017','ttH_3l_0tau_rest_emm_bt_2018','ttH_3l_0tau_rest_mmm_bl_2017','ttH_3l_0tau_rest_mmm_bt_2016','ttH_3l_0tau_rest_mmm_bt_2017','\
ttH_3l_0tau_rest_mmm_bt_2018'],
    'ttH 3l 0tau_tH' : ['ttH_3l_0tau_tH_bl_2016','ttH_3l_0tau_tH_bl_2017','ttH_3l_0tau_tH_bl_2018','ttH_3l_0tau_tH_bt_2016','ttH_3l_0tau_tH_bt_2017','ttH_3l_0tau_tH_bt_2018'],
    'ttH 3l 0tau_ttH': ['ttH_3l_0tau_ttH_bl_2018','ttH_3l_0tau_ttH_bt_2016','ttH_3l_0tau_ttH_bt_2017','ttH_3l_0tau_ttH_bt_2018','ttH_3l_0tau_ttH_bl_2016','ttH_3l_0tau_ttH_bl_2017'],

    '2lss 0tau Rest'   : ['ttH_2lss_0tau_mm_Restnode_2016','ttH_2lss_0tau_ee_Restnode_2016','ttH_2lss_0tau_ee_Restnode_2017','ttH_2lss_0tau_ee_Restnode_2018','ttH_2lss_0tau_em_Restnode_2016','ttH_2lss_0tau_em_Restnode_2017','ttH_2lss_0tau_em_Restnode_2018','ttH_2lss_0tau_mm_Restnode_2017','ttH_2lss_0tau_mm_Restnode_2018'],
    '2lss 0tau tHQnode': ['ttH_2lss_0tau_mm_tHQnode_2016','ttH_2lss_0tau_ee_tHQnode_2016','ttH_2lss_0tau_ee_tHQnode_2017','ttH_2lss_0tau_ee_tHQnode_2018','ttH_2lss_0tau_em_tHQnode_2016','ttH_2lss_0tau_em_tHQnode_2017','ttH_2lss_0tau_em_tHQnode_2018','ttH_2lss_0tau_mm_tHQnode_2017','ttH_2lss_0tau_mm_tHQnode_2018'],
    '2lss 0tau ttWnode': ['ttH_2lss_0tau_mm_ttWnode_2016','ttH_2lss_0tau_mm_ttWnode_2018','ttH_2lss_0tau_ee_ttWnode_2016','ttH_2lss_0tau_ee_ttWnode_2017','ttH_2lss_0tau_ee_ttWnode_2018','ttH_2lss_0tau_em_ttWnode_2016','ttH_2lss_0tau_em_ttWnode_2017','ttH_2lss_0tau_em_ttWnode_2018','ttH_2lss_0tau_mm_ttWnode_2017'],
    '2lss 0tau ttHnode': ['ttH_2lss_0tau_mm_ttHnode_2016','ttH_2lss_0tau_mm_ttHnode_2018','ttH_2lss_0tau_ee_ttHnode_2016','ttH_2lss_0tau_ee_ttHnode_2017','ttH_2lss_0tau_ee_ttHnode_2018','ttH_2lss_0tau_em_ttHnode_2016','ttH_2lss_0tau_em_ttHnode_2017','ttH_2lss_0tau_em_ttHnode_2018','ttH_2lss_0tau_mm_ttHnode_2017'],

    '2lss 1tau rest'  : ['ttH_2lss_1tau_rest_2016','ttH_2lss_1tau_rest_2017','ttH_2lss_1tau_rest_2018'],
    '2lss 1tau tH'    : ['ttH_2lss_1tau_tH_2016','ttH_2lss_1tau_tH_2017','ttH_2lss_1tau_tH_2018'],
    '2lss 1tau ttH'   : ['ttH_2lss_1tau_ttH_2016','ttH_2lss_1tau_ttH_2017','ttH_2lss_1tau_ttH_2018'],

    # merged regions for paper                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
    '2lss 0tau'   : ['ttH_2lss_0tau_mm_Restnode_2016','ttH_2lss_0tau_ee_Restnode_2016','ttH_2lss_0tau_ee_Restnode_2017','ttH_2lss_0tau_ee_Restnode_2018','ttH_2lss_0tau_em_Restnode_2016','ttH_2lss_0tau_em_Restnode_2017','ttH_2lss_0tau_em_Restnode_2018','ttH_2lss_0tau_mm_Restnode_2017','ttH_2lss_0tau_mm_Restnode_2018', 'ttH_2lss_0tau_mm_tHQnode_2016','ttH_2lss_0tau_ee_tHQnode_2016','ttH_2lss_0tau_ee_tHQnode_2017','ttH_2lss_0tau_ee_tHQnode_2018','ttH_2lss_0tau_em_tHQnode_2016','ttH_2lss_0tau_em_tHQnode_2017','ttH_2lss_0tau_em_tHQnode_2018','ttH_2lss_0tau_mm_tHQnode_2017','ttH_2lss_0tau_mm_tHQnode_2018','ttH_2lss_0tau_mm_ttWnode_2\
016','ttH_2lss_0tau_mm_ttWnode_2018','ttH_2lss_0tau_ee_ttWnode_2016','ttH_2lss_0tau_ee_ttWnode_2017','ttH_2lss_0tau_ee_ttWnode_2018','ttH_2lss_0tau_em_ttWnode_2016','ttH_2lss_0tau_em_ttWnode_2017','ttH_2lss_0tau_em_ttWnode_2018','ttH_2lss_0tau_mm_ttWnode_2017','ttH_2lss_0tau_mm_ttHnode_2016','ttH_2lss_0tau_mm_ttHnode_2018','ttH_2lss_0tau_ee_ttHnode_2016','ttH_2lss_0tau_ee_ttHnode_2017','ttH_2lss_0tau_ee_ttHnode_2018','ttH_2lss_0tau_em_ttHnode_2016','ttH_2lss_0tau_em_ttHnode_2017','ttH_2lss_0tau_em_ttHnode_2018','ttH_2lss_0tau_mm_ttHnode_2017'],
    '3l 0tau'     : ['ttH_3l_0tau_rest_eem_bl_2016','ttH_3l_0tau_rest_eem_bl_2017','ttH_3l_0tau_rest_eem_bl_2018','ttH_3l_0tau_rest_emm_bl_2016','ttH_3l_0tau_rest_emm_bl_2017','ttH_3l_0tau_rest_emm_bl_2018','ttH_3l_0tau_rest_mmm_bl_2016','ttH_3l_0tau_rest_mmm_bl_2018','ttH_3l_0tau_rest_eee_2016','ttH_3l_0tau_rest_eee_2017','ttH_3l_0tau_rest_eee_2018','ttH_3l_0tau_rest_eem_bt_2016','ttH_3l_0tau_rest_eem_bt_2017','ttH_3l_0tau_rest_eem_bt_2018','ttH_3l_0tau_rest_emm_bt_2016','ttH_3l_0tau_rest_emm_bt_2017','ttH_3l_0tau_rest_emm_bt_2018','ttH_3l_0tau_rest_mmm_bl_2017','ttH_3l_0tau_rest_mmm_bt_2016','ttH_3l_0tau_rest_mmm_bt_2017','t\
tH_3l_0tau_rest_mmm_bt_2018', 'ttH_3l_0tau_tH_bl_2016','ttH_3l_0tau_tH_bl_2017','ttH_3l_0tau_tH_bl_2018','ttH_3l_0tau_tH_bt_2016','ttH_3l_0tau_tH_bt_2017','ttH_3l_0tau_tH_bt_2018','ttH_3l_0tau_ttH_bl_2018','ttH_3l_0tau_ttH_bt_2016','ttH_3l_0tau_ttH_bt_2017','ttH_3l_0tau_ttH_bt_2018','ttH_3l_0tau_ttH_bl_2016','ttH_3l_0tau_ttH_bl_2017'],
    '2lss 1tau' : ['ttH_2lss_1tau_rest_2016','ttH_2lss_1tau_rest_2017','ttH_2lss_1tau_rest_2018','ttH_2lss_1tau_tH_2016','ttH_2lss_1tau_tH_2017','ttH_2lss_1tau_tH_2018','ttH_2lss_1tau_ttH_2016','ttH_2lss_1tau_ttH_2017','ttH_2lss_1tau_ttH_2018'],

}
procswithdecays=['ttH','VH', 'TTWH',"TTWH", "TTZH", "qqH", "VH", "WH", "ZH", "ggH",'tHq','tHW']


catsStackYears={}
for cat in ['ttH_2lss_0tau_ee_Restnode%s','ttH_2lss_0tau_ee_tHQnode%s','ttH_2lss_0tau_ee_ttHnode%s','ttH_2lss_0tau_ee_ttWnode%s','ttH_2lss_0tau_em_Restnode%s','ttH_2lss_0tau_em_tHQnode%s','ttH_2lss_0tau_em_ttHnode%s','ttH_2lss_0tau_em_ttWnode%s','ttH_2lss_1tau_rest%s','ttH_2lss_1tau_tH%s','ttH_2lss_1tau_ttH%s','ttH_3l_0tau_rest_eee%s','ttH_3l_0tau_rest_eem_bt%s','ttH_3l_0tau_rest_emm_bt%s','ttH_3l_0tau_rest_mmm_bt%s','ttH_3l_0tau_tH_bl%s','ttH_3l_0tau_ttH_bl%s','ttH_4l%s','ttH_cr_3l%s_eee_cr','ttH_cr_3l%s_eem_cr','ttH_cr_3l%s_emm_cr','ttH_cr_3l%s_mmm_cr','ttH_cr_4l%s','ttH_0l_2tau%s','ttH_1l_1tau%s','ttH_1l_2tau%s','ttH_2l_2tau%s','ttH_2los_1tau%s','ttH_2lss_0tau_mm_Restnode%s','ttH_2lss_0tau_mm_tHQnode%s','ttH_2lss_0tau_mm_ttHnode%s','ttH_2lss_0tau_mm_ttWnode%s','ttH_3l_0tau_rest_eem_bl%s','ttH_3l_0tau_rest_emm_bl%s','ttH_3l_0tau_rest_mmm_bl%s','ttH_3l_0tau_tH_bt%s','ttH_3l_0tau_ttH_bt%s','ttH_3l_1tau%s']:
    catsStackYears[cat%'']=[cat%x for x in '_2016,_2017,_2018'.split(',')]



processes_name = {
    'Fakes' : 'Non-prompt leptons',
    'Flips' : 'Flips',
    'Conv'  : 'Conversion',
    'TT+jets' : '$\ttbar$+jets',
    'Rares' : 'Rare backgrounds',
    'ZZ'    : '$\PZ\PZ$',
    'WZ'    : '$\PW\PZ$',
    'TTW TTWW' : '$\\ttW + \\ttWW$',
    'Other Higgs'    : '$\ggH + \qqH + \VH + \ttVH$',
    'tH'  : '$\\tH$',
    'ttH' : '$\\ttH$',
    'ttZ' : '$\\ttZ + \\ttbar\\Pggx$',
    'DY'  : 'DY',
    'total background' : 'Total expected background',
}

process_order = ['ttH','tH', 'ttZ', 'TTW TTWW','WZ','ZZ', 'DY', 'TT+jets', 'Fakes', 'Flips', 'Rares', 'Other Higgs', 'total background']
