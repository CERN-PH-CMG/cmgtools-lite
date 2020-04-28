import os, sys
nCores=16
submit = '''sbatch -c %d -p short  --wrap '{command}' '''%nCores
#submit = '{command}' 


if   'cmsco01.cern.ch' in os.environ['HOSTNAME']: ORIGIN="/data/peruzzi";
elif 'cmsphys10' in os.environ['HOSTNAME']:       ORIGIN="/data1/g/gpetrucc"; 
elif 'gpetrucc-vm2.cern.ch' in os.environ['HOSTNAME']:       ORIGIN="/data/gpetrucc"; 
elif 'fanae' in os.environ['HOSTNAME']:       ORIGIN="/pool/ciencias/HeppyTrees/EdgeZ/TTH/"; 
elif 'gae' in os.environ['HOSTNAME']:       ORIGIN="/pool/ciencias/HeppyTrees/EdgeZ/TTH/"; 
else: ORIGIN="/afs/cern.ch/work/p/peruzzi"; 

if len(sys.argv) < 4: 
    print 'Sytaxis is %s [outputdir] [year] [region] [other]'%sys.argv[0]
    raise RuntimeError 
OUTNAME=sys.argv[1]
YEAR=sys.argv[2]
REGION=sys.argv[3]
OTHER=sys.argv[4:] if len(sys.argv) > 4 else ''

if   YEAR in '2016': LUMI="35.9"
elif YEAR in '2017': LUMI="41.4"
elif YEAR in '2018': LUMI="59.7"
else:
    raise RuntimeError("Wrong year %s"%YEAR)


#print "Normalizing to {LUMI}/fb".format(LUMI=LUMI);
OPTIONS=" --tree NanoAOD --s2v -j {J} -l {LUMI} -f --WA prescaleFromSkim --split-factor=-1 ".format(LUMI=LUMI,J=nCores)
os.system("test -d cards/{OUTNAME} || mkdir -p cards/{OUTNAME}".format(OUTNAME=OUTNAME))
OPTIONS="{OPTIONS} --od cards/{OUTNAME} ".format(OPTIONS=OPTIONS, OUTNAME=OUTNAME)
#T2L="-P {ORIGIN}/NanoTrees_TTH_091019_v6pre_skim2lss/{YEAR} --FMCs {{P}}/0_jmeUnc_v1  --Fs  {{P}}/1_recl/ --FMCs {{P}}/2_scalefactors --Fs {{P}}/3_tauCount --Fs {{P}}/6_mva3l --Fs {{P}}/6_mva2lss_new/  --Fs {{P}}/6_mva4l --xf TTTW --xf TTWH".format(ORIGIN=ORIGIN, YEAR=YEAR)
T2L="-P {ORIGIN}/NanoTrees_TTH_090120_091019_v6_skim2lss/{YEAR} --FMCs {{P}}/0_jmeUnc_v1 --FDs {{P}}/1_recl --FMCs {{P}}/1_recl_allvars --FMCs {{P}}/2_btag_SFs --FMCs {{P}}/2_scalefactors_lep_fixed --Fs {{P}}/3_tauCount --Fs {{P}}/4_evtVars --Fs {{P}}/5_BDThtt_reco_new_blah --Fs {{P}}/6_mva2lss --Fs {{P}}/6_mva3l --Fs {{P}}/6_mva4l  --xf TTTW --xf TTWH".format(ORIGIN=ORIGIN, YEAR=YEAR)
T3L=T2L
T4L=T2L

SYSTS="--unc ttH-multilepton/systsUnc.txt --amc --xu CMS_ttHl_TTZ_lnU,CMS_ttHl_TTW_lnU"
MCAOPTION=""
MCAOPTION="-splitdecays"
ASIMOV="--asimov signal"
#ASIMOV="" 
SCRIPT= "makeShapeCardsNew.py"
PROMPTSUB="--plotgroup data_fakes+=.*_promptsub"
if "scan" in OTHER:         
    ASIMOV="--asimov tHq_ct_1p0_cv_1p0_hww,tHq_ct_1p0_cv_1p0_htt,tHq_ct_1p0_cv_1p0_hzz,ttH_ct_1p0_cv_1p0_hww,ttH_ct_1p0_cv_1p0_hzz,ttH_ct_1p0_cv_1p0_htt,ttH_ct_1p0_cv_1p0_hmm,ttH_ct_1p0_cv_1p0_hzg,tHW_ct_1p0_cv_1p0_hww,tHW_ct_1p0_cv_1p0_hzz,tHW_ct_1p0_cv_1p0_htt,ZH_hww,ZH_htt,ZH_hzz,WH_hww,WH_htt,WH_hzz" 
    SCRIPT = "makeShapeCardsNewScan.py"
    MCAOPTION="-ctcv"
    SYSTS="--unc ttH-multilepton/systsUnc.txt --amc"

if 'unblind' in OTHER:
    ASIMOV=""

print "We are using the asimov dataset"
OPTIONS="{OPTIONS} -L ttH-multilepton/functionsTTH.cc --mcc ttH-multilepton/lepchoice-ttH-FO.txt --mcc ttH-multilepton/mcc-METFixEE2017.txt {PROMPTSUB} --neg   --threshold 0.01 {ASIMOV} --filter ttH-multilepton/filter-processes.txt ".format(OPTIONS=OPTIONS,PROMPTSUB=PROMPTSUB,ASIMOV=ASIMOV) # neg necessary for subsequent rebin #  
CATPOSTFIX=""

FUNCTION_2L="ttH_catIndex_2lss_MVA(LepGood1_pdgId,LepGood2_pdgId,DNN_2lss_predictions_ttH,DNN_2lss_predictions_ttW,DNN_2lss_predictions_tHQ,DNN_2lss_predictions_Rest)"
FUNCTION_3L="ttH_catIndex_3l_MVA(DNN_3l_predictions_ttH,DNN_3l_predictions_tH,DNN_3l_predictions_rest,LepGood1_pdgId,LepGood2_pdgId,LepGood3_pdgId,nBJetMedium25)"
FUNCTION_4L=''' "ttH_catIndex_4l(FinalMVA_4L_BDTG)" [0.5,1.5,2.5] '''
FUNCTION_CR_3L='''"ttH_3l_clasifier(nJet25,nBJetMedium25)" [0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5,10.5,11.5,12.5] '''
FUNCTION_CR_4L='''"ttH_4l_clasifier(nJet25,nBJetMedium25,mZ2)" [0.5,1.5,2.5,3.5,4.5] '''
FUNCTION_SVA_2L='''"mass_2(LepGood1_conePt,LepGood1_eta,LepGood1_phi,LepGood1_mass,LepGood2_conePt,LepGood2_eta,LepGood2_phi,LepGood2_mass)" [10.,40.0,55.0,70.0,80.0,95.0,110.0,140.0,180.,800.0]'''
FUNCTION_SVA_2L_scan='''"deltaPhi(LepGood1_phi, LepGood2_phi)" 30,-3.14,3.14 '''
FUNCTION_SVA_3L='''"mass_3_cheap(LepGood1_pt,LepGood1_eta,LepGood2_pt,LepGood2_eta,LepGood2_phi-LepGood1_phi,LepGood3_pt,LepGood3_eta,LepGood3_phi-LepGood1_phi)" [20.,100.,140.,190.,250.,1000.]'''
FUNCTION_SVA_4L="m4l [70.,200.0,300.0,1000.]"
ONEBIN="1 1,0.5,1.5"
MCASUFFIX="mcdata-frdata"

DOFILE = ""

if REGION == "2lss":
    OPT_2L='{T2L} {OPTIONS} -W "L1PreFiringWeight_Nom*puWeight*btagSF_shape*leptonSF_2lss*triggerSF_ttH(LepGood1_pdgId, LepGood1_conePt, LepGood2_pdgId, LepGood2_conePt, 2, year)"'.format(T2L=T2L, OPTIONS=OPTIONS)
    CATPOSTFIX=""

    CATBINS="[0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5,10.5,11.5,12.5,13.5,14.5,15.5,16.5,17.5,18.5,19.5,20.5,21.5,22.5,23.5,24.5,25.5,26.5,27.5,28.5,29.5,30.5,31.5,32.5,33.5,34.5,35.5,36.5,37.5,38.5,39.5,40.5,41.5,42.5,43.5,44.5,45.5,46.5,47.5,48.5,49.5,50.5,51.5,52.5,53.5,54.5,55.5,56.5,57.5,58.5,59.5,60.5,61.5,62.5,63.5,64.5,65.5,66.5,67.5,68.5,69.5,70.5,71.5,72.5,73.5,74.5,75.5,76.5,77.5,78.5,79.5,80.5,81.5,82.5,83.5,84.5,85.5,86.5,87.5,88.5,89.5,90.5,91.5,92.5,93.5,94.5,95.5,96.5,97.5,98.5,99.5,100.5,101.5,102.5,103.5,104.5,105.5,106.5,107.5,108.5,109.5,110.5,111.5,112.5,113.5,114.5,115.5,116.5,117.5,118.5,119.5,120.5]"
    RANGES = '[1,6,14,20,24,37,45,64,75,88,99,114,121]'
    NAMES  = ','.join( '%s_%s'%(x,YEAR) for x in 'ee_ttHnode,ee_Restnode,ee_ttWnode,ee_tHQnode,em_ttHnode,em_Restnode,em_ttWnode,em_tHQnode,mm_ttHnode,mm_Restnode,mm_ttWnode,mm_tHQnode'.split(','))
            
    TORUN='''python {SCRIPT} {DOFILE} ttH-multilepton/mca-2lss-{MCASUFFIX}{MCAOPTION}.txt ttH-multilepton/2lss_tight_legacy.txt "{FUNCTION_2L}" "{CATBINS}" {SYSTS} {OPT_2L} --binname ttH_2lss_0tau --year {YEAR} --categorize-by-ranges {RANGES} {NAMES} '''.format(SCRIPT=SCRIPT, DOFILE=DOFILE, MCASUFFIX=MCASUFFIX, MCAOPTION=MCAOPTION, FUNCTION_2L=FUNCTION_2L, CATBINS=CATBINS, SYSTS=SYSTS, OPT_2L=OPT_2L,YEAR=YEAR,RANGES=RANGES,NAMES=NAMES)
    print submit.format(command=TORUN)
            

if REGION == "2lss_SVA":
    CATFUNC='''"ttH_catIndex_2lss_SVA(LepGood1_pdgId,LepGood2_pdgId,LepGood1_charge,nJet25)"'''
    CATBINS="[0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5,10.5]"
    CATNAMES="ee_lj,ee_hj,em_neg_lj,em_neg_hj,em_pos_lj,em_pos_hj,mm_neg_lj,mm_neg_hj,mm_pos_lj,mm_pos_hj"
    OPT_2L='{T2L} {OPTIONS} -W "L1PreFiringWeight_Nom*puWeight*btagSF_shape*leptonSF_2lss*triggerSF_ttH(LepGood1_pdgId, LepGood1_conePt, LepGood2_pdgId, LepGood2_conePt, 2, year)"'.format(T2L=T2L, OPTIONS=OPTIONS)
    CATPOSTFIX=""
    TORUN='''python {SCRIPT} {DOFILE} ttH-multilepton/mca-2lss-{MCASUFFIX}{MCAOPTION}.txt ttH-multilepton/2lss_tight.txt {FUNCTION_SVA_2L} {SYSTS} {OPT_2L} --binname ttH_2lss_{YEAR} --categorize {CATFUNC} {CATBINS} {CATNAMES}  --year {YEAR};'''.format(SCRIPT=SCRIPT, DOFILE=DOFILE, MCASUFFIX=MCASUFFIX, MCAOPTION=MCAOPTION, FUNCTION_SVA_2L=FUNCTION_SVA_2L, SYSTS=SYSTS, OPT_2L=OPT_2L, CATFUNC=CATFUNC,CATNAMES=CATNAMES, CATBINS=CATBINS,YEAR=YEAR)
    print submit.format(command=TORUN)

if REGION == "2lss_SVA_scan":
    CATFUNC='''"ttH_catIndex_2lss_SVA_soft(LepGood1_pdgId,LepGood2_pdgId,LepGood1_charge,nJet25)"'''
    CATBINS="[0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5,10.5]"
    CATNAMES="ee_lj,ee_hj,em_neg_lj,em_neg_hj,em_pos_lj,em_pos_hj,mm_neg_lj,mm_neg_hj,mm_pos_lj,mm_pos_hj"
    OPT_2L="{T2L} {OPTIONS} -W L1PreFiringWeight_Nom*puWeight*btagSF_shape*leptonSF_2lss*triggerSF_2lss".format(T2L=T2L, OPTIONS=OPTIONS)
    CATPOSTFIX=""
    TORUN1='''python {SCRIPT} {DOFILE} ttH-multilepton/mca-2lss-{MCASUFFIX}{MCAOPTION}.txt ttH-multilepton/2lss_tight_thq.txt {FUNCTION_SVA_2L} {SYSTS} {OPT_2L} --binname ttH_2lss_{YEAR} -E ^tthlike -X ^borthogonality -X ^FRWorthogonality --categorize {CATFUNC} {CATBINS} {CATNAMES}  --year {YEAR};'''.format(SCRIPT=SCRIPT, DOFILE=DOFILE, MCASUFFIX=MCASUFFIX, MCAOPTION=MCAOPTION, FUNCTION_SVA_2L=FUNCTION_SVA_2L_scan, SYSTS=SYSTS, OPT_2L=OPT_2L, CATFUNC=CATFUNC,CATNAMES=CATNAMES, CATBINS=CATBINS,YEAR=YEAR)
    TORUN2='''python {SCRIPT} {DOFILE} ttH-multilepton/mca-2lss-{MCASUFFIX}{MCAOPTION}.txt ttH-multilepton/2lss_tight_thq.txt {FUNCTION_SVA_2L} {SYSTS} {OPT_2L} --binname tHq_2lss_{YEAR} -E ^thqlike -X ^borthogonality -X ^FRWorthogonality --categorize {CATFUNC} {CATBINS} {CATNAMES}  --year {YEAR};'''.format(SCRIPT=SCRIPT, DOFILE=DOFILE, MCASUFFIX=MCASUFFIX, MCAOPTION=MCAOPTION, FUNCTION_SVA_2L=FUNCTION_SVA_2L_scan, SYSTS=SYSTS, OPT_2L=OPT_2L, CATFUNC=CATFUNC,CATNAMES=CATNAMES, CATBINS=CATBINS,YEAR=YEAR)
    print submit.format(command=TORUN1)
    print submit.format(command=TORUN2)

if REGION == "2lss_3j_SVA":
    CATFUNC='''"ttH_catIndex_2lss_SVA(LepGood1_pdgId,LepGood2_pdgId,LepGood1_charge,nJet25)"'''
    CATBINS="[0.5,2.5,4.5,6.5,8.5,10.5]"
    CATNAMES="ee,em_neg,em_pos,mm_neg,mm_pos"
    OPT_2L='{T2L} {OPTIONS} -W "L1PreFiringWeight_Nom*puWeight*btagSF_shape*leptonSF_2lss*triggerSF_ttH(LepGood1_pdgId, LepGood1_conePt, LepGood2_pdgId, LepGood2_conePt, 2, year)" -X ^4j -E ^x3j '.format(T2L=T2L, OPTIONS=OPTIONS)
    CATPOSTFIX=""
    TORUN='''python {SCRIPT} {DOFILE} ttH-multilepton/mca-2lss-{MCASUFFIX}{MCAOPTION}.txt ttH-multilepton/2lss_tight.txt {FUNCTION_SVA_2L} {SYSTS} {OPT_2L} --binname ttH_2lss_3j_{YEAR} --categorize {CATFUNC} {CATBINS} {CATNAMES}  --year {YEAR};'''.format(SCRIPT=SCRIPT, DOFILE=DOFILE, MCASUFFIX=MCASUFFIX, MCAOPTION=MCAOPTION, FUNCTION_SVA_2L=FUNCTION_SVA_2L, SYSTS=SYSTS, OPT_2L=OPT_2L, CATFUNC=CATFUNC,CATNAMES=CATNAMES, CATBINS=CATBINS,YEAR=YEAR)
    print submit.format(command=TORUN)
    

if REGION == "3l":
    OPT_3L='{T3L} {OPTIONS} -W "L1PreFiringWeight_Nom*puWeight*btagSF_shape*triggerSF_ttH(LepGood1_pdgId, LepGood1_conePt, LepGood2_pdgId, LepGood2_conePt, 3, year)*leptonSF_3l"'.format(T3L=T3L, OPTIONS=OPTIONS)
    CATPOSTFIX=""
    CATBINS="[0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5,10.5,11.5,12.5,13.5,14.5,15.5,16.5,17.5,18.5,19.5,20.5,21.5,22.5,23.5,24.5,25.5,26.5,27.5,28.5,29.5,30.5,31.5,32.5,33.5,34.5]"
    RANGES = '[1,6,10,17,20,21,25,26,30,31,34,35]'
    NAMES  = ','.join( '%s_%s'%(x,YEAR) for x in ['ttH_bl','ttH_bt','tH_bl','tH_bt','rest_eee','rest_eem_bl','rest_eem_bt','rest_emm_bl','rest_emm_bt','rest_mmm_bl','rest_mmm_bt'])
    TORUN = 'python {SCRIPT} {DOFILE} ttH-multilepton/mca-3l-{MCASUFFIX}{MCAOPTION}.txt ttH-multilepton/3l_tight_legacy.txt "{FUNCTION_3L}" "{CATBINS}" {SYSTS} {OPT_3L} --binname ttH_3l_0tau --year {YEAR} --categorize-by-ranges {RANGES} {NAMES}'.format(SCRIPT=SCRIPT, DOFILE=DOFILE,MCASUFFIX=MCASUFFIX,MCAOPTION=MCAOPTION,FUNCTION_3L=FUNCTION_3L,CATBINS=CATBINS,YEAR=YEAR, SYSTS=SYSTS, OPT_3L=OPT_3L,RANGES=RANGES, NAMES=NAMES)
    print submit.format(command=TORUN)

if REGION == "3l_SVA":
    CATFUNC='''"ttH_catIndex_3l_SVA(LepGood1_charge,LepGood2_charge,LepGood3_charge,nJet25)"'''
    CATBINS="[10.5,11.5,12.5,13.5,14.5]"
    CATNAMES="lj_neg,lj_pos,hj_neg,hj_pos"
    OPT_3L='{T3L} {OPTIONS} -W "L1PreFiringWeight_Nom*puWeight*btagSF_shape*triggerSF_ttH(LepGood1_pdgId, LepGood1_conePt, LepGood2_pdgId, LepGood2_conePt, 3, year)*leptonSF_3l"'.format(T3L=T3L, OPTIONS=OPTIONS)
    TORUN="python {SCRIPT} {DOFILE} ttH-multilepton/mca-3l-{MCASUFFIX}{MCAOPTION}.txt ttH-multilepton/3l_tight.txt {FUNCTION_SVA_3L} {SYSTS} {OPT_3L} --binname ttH_3l_{YEAR} --categorize {CATFUNC} {CATBINS} {CATNAMES}  --year {YEAR} ;".format(SCRIPT=SCRIPT,DOFILE=DOFILE,MCASUFFIX=MCASUFFIX,MCAOPTION=MCAOPTION,FUNCTION_SVA_3L=FUNCTION_SVA_3L,SYSTS=SYSTS,OPT_3L=OPT_3L,CATFUNC=CATFUNC,CATBINS=CATBINS,CATNAMES=CATNAMES,YEAR=YEAR)
    print submit.format(command=TORUN)

if REGION == "3l_SVA_scan":
    CATFUNC='''"ttH_catIndex_3l_SVA_soft(LepGood1_charge,LepGood2_charge,LepGood3_charge,nJet25)"'''
    CATBINS="[10.5,11.5,12.5,13.5,14.5]"
    CATNAMES="lj_neg,lj_pos,hj_neg,hj_pos"
    OPT_3L="{T3L} {OPTIONS} -W L1PreFiringWeight_Nom*puWeight*btagSF_shape*triggerSF_3l*leptonSF_3l".format(T3L=T3L, OPTIONS=OPTIONS)
    TORUN1='''python {SCRIPT} {DOFILE} ttH-multilepton/mca-3l-{MCASUFFIX}{MCAOPTION}.txt ttH-multilepton/3l_tight_thq.txt {FUNCTION_SVA_3L} {SYSTS} {OPT_3L} --binname ttH_3l_{YEAR} -E ^tthlike -X ^borthogonality -X ^FRWorthogonality --categorize {CATFUNC} {CATBINS} {CATNAMES}  --year {YEAR};'''.format(SCRIPT=SCRIPT, DOFILE=DOFILE, MCASUFFIX=MCASUFFIX, MCAOPTION=MCAOPTION, FUNCTION_SVA_3L=FUNCTION_SVA_2L_scan, SYSTS=SYSTS, OPT_3L=OPT_3L, CATFUNC=CATFUNC,CATNAMES=CATNAMES, CATBINS=CATBINS,YEAR=YEAR)
    TORUN2='''python {SCRIPT} {DOFILE} ttH-multilepton/mca-3l-{MCASUFFIX}{MCAOPTION}.txt ttH-multilepton/3l_tight_thq.txt {FUNCTION_SVA_3L} {SYSTS} {OPT_3L} --binname tHq_3l_{YEAR} -E ^thqlike -X ^borthogonality -X ^FRWorthogonality --categorize {CATFUNC} {CATBINS} {CATNAMES}  --year {YEAR};'''.format(SCRIPT=SCRIPT, DOFILE=DOFILE, MCASUFFIX=MCASUFFIX, MCAOPTION=MCAOPTION, FUNCTION_SVA_3L=FUNCTION_SVA_2L_scan, SYSTS=SYSTS, OPT_3L=OPT_3L, CATFUNC=CATFUNC,CATNAMES=CATNAMES, CATBINS=CATBINS,YEAR=YEAR)
    print submit.format(command=TORUN1)
    print submit.format(command=TORUN2)

if  REGION == "cr_3l":
    OPT_3L='{T3L} {OPTIONS} -W "L1PreFiringWeight_Nom*puWeight*btagSF_shape*triggerSF_ttH(LepGood1_pdgId, LepGood1_conePt, LepGood2_pdgId, LepGood2_conePt, 3, year)*leptonSF_3l"'.format(T3L=T3L,OPTIONS=OPTIONS)
    CATPOSTFIX="_cr"
    OPT_3L="{OPT_3L} -I ^Zveto -X ^2j -X ^2b1B -E ^underflowVeto3l".format(OPT_3L=OPT_3L)
    CATFUNC="ttH_3l_ifflav(LepGood1_pdgId,LepGood2_pdgId,LepGood3_pdgId)"
    CATBINS="[0.5,1.5,2.5,3.5,4.5]"
    CATNAMES=",".join( map( lambda x : x+CATPOSTFIX, 'eee,eem,emm,mmm'.split(',')))
    TORUN = '''python {SCRIPT} {DOFILE} ttH-multilepton/mca-3l-{MCASUFFIX}{MCAOPTION}.txt ttH-multilepton/3l_tight.txt {FUNCTION_CR_3L} {SYSTS} {OPT_3L} --binname ttH_cr_3l_{YEAR} --categorize "{CATFUNC}" {CATBINS} {CATNAMES} --year {YEAR}'''.format( SCRIPT=SCRIPT, DOFILE=DOFILE, MCASUFFIX=MCASUFFIX,MCAOPTION=MCAOPTION,FUNCTION_CR_3L=FUNCTION_CR_3L,SYSTS=SYSTS,OPT_3L=OPT_3L,YEAR=YEAR,CATFUNC=CATFUNC,CATBINS=CATBINS,CATNAMES=CATNAMES)
    print submit.format(command=TORUN)

if REGION == "cr_4l":
    OPT_4L='{T4L} {OPTIONS} -W "L1PreFiringWeight_Nom*puWeight*btagSF_shape*leptonSF_4l*triggerSF_ttH(LepGood1_pdgId, LepGood1_conePt, LepGood2_pdgId, LepGood2_conePt, 3, year)"'.format(T4L=T4L,OPTIONS=OPTIONS)
    OPT_4L="{OPT_4L} -I ^Zveto -X ^2j -X ^2b1B -E ^underflowVeto4l".format(OPT_4L=OPT_4L)
    CATPOSTFIX="_cr_4l";
    TORUN = 'python {SCRIPT} {DOFILE} ttH-multilepton/mca-4l-{MCASUFFIX}{MCAOPTION}.txt ttH-multilepton/4l_tight.txt {FUNCTION_CR_4L} {SYSTS} {OPT_4L} --binname ttH{CATPOSTFIX}_{YEAR} --year {YEAR}'.format(SCRIPT=SCRIPT, DOFILE=DOFILE,MCASUFFIX=MCASUFFIX,MCAOPTION=MCAOPTION, FUNCTION_CR_4L=FUNCTION_CR_4L,SYSTS=SYSTS,OPT_4L=OPT_4L,CATPOSTFIX=CATPOSTFIX,YEAR=YEAR)
    print submit.format(command=TORUN)
        
if REGION=="4l": 
    OPT_4L='{T4L} {OPTIONS} -W "L1PreFiringWeight_Nom*puWeight*btagSF_shape*leptonSF_4l*triggerSF_ttH(LepGood1_pdgId, LepGood1_conePt, LepGood2_pdgId, LepGood2_conePt, 3, year)"'.format(T4L=T4L,OPTIONS=OPTIONS)
    CATPOSTFIX=""
    TORUN="python {SCRIPT} {DOFILE} ttH-multilepton/mca-4l-{MCASUFFIX}{MCAOPTION}.txt ttH-multilepton/4l_tight.txt {FUNCTION_4L} {SYSTS} {OPT_4L} --binname ttH_4l{CATPOSTFIX}_{YEAR} --year {YEAR} ".format(SCRIPT=SCRIPT, DOFILE=DOFILE,MCASUFFIX=MCASUFFIX,MCAOPTION=MCAOPTION,FUNCTION_4L=FUNCTION_4L,SYSTS=SYSTS,OPT_4L=OPT_4L,CATPOSTFIX=CATPOSTFIX,YEAR=YEAR)
    
    print submit.format(command=TORUN)

if REGION=="4l_SVA": 
    OPT_4L='{T4L} {OPTIONS} -W "L1PreFiringWeight_Nom*puWeight*btagSF_shape*leptonSF_4l*triggerSF_ttH(LepGood1_pdgId, LepGood1_conePt, LepGood2_pdgId, LepGood2_conePt, 3, year)"'.format(T4L=T4L,OPTIONS=OPTIONS)
    CATPOSTFIX=""
    TORUN="python {SCRIPT} {DOFILE} ttH-multilepton/mca-4l-{MCASUFFIX}{MCAOPTION}.txt ttH-multilepton/4l_tight.txt {FUNCTION_SVA_4L} {SYSTS} {OPT_4L} --binname ttH_4l{CATPOSTFIX}_{YEAR} --year {YEAR}".format(SCRIPT=SCRIPT, DOFILE=DOFILE,MCASUFFIX=MCASUFFIX,MCAOPTION=MCAOPTION,FUNCTION_SVA_4L=FUNCTION_SVA_4L,SYSTS=SYSTS,OPT_4L=OPT_4L,CATPOSTFIX=CATPOSTFIX,YEAR=YEAR)
    print submit.format(command=TORUN)
