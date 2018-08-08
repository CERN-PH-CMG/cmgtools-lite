#!/usr/bin/env python
import sys
import re
import os

ODIR=sys.argv[1]

dowhat = "plots" 
#dowhat = "dumps" 
#dowhat = "yields" 
#dowhat = "ntuple" # syntax: python ttH-multilepton/ttH_plots.py no 2lss_SR_extr outfile_{cname}.root --sP var1,var2,...

P0="/afs/cern.ch/work/p/peruzzi/tthtrees"
if 'cmsco01'   in os.environ['HOSTNAME']: P0="/data/peruzzi"
if 'cmsphys10' in os.environ['HOSTNAME']: P0="/data1/g/gpetrucc"
TREES = "--Fs {P}/5_triggerDecision_230418_v1 --Fs {P}/7_tauTightSel_v2 --FMCs {P}/8_vtxWeight2017_v1 --FMCs {P}/6_bTagSF_v2"
TREESONLYSKIM = "-P "+P0+"/TREES_TTH_190418_Fall17_skim2lss3l --Fs {P}/1_recleaner_180518_v2 --Fs {P}/2_eventVars_230418_v2 --Fs {P}/3_kinMVA_noMEM_200618_v5 --Fs {P}/4_BDTv8_Hj_200618_v1 --Fs {P}/4_BDTrTT_Hj_200618_v1 --Fs {P}/4_BDThttTT_Hj_200618_v4"
TREESONLYFULL = "-P "+P0+"/TREES_TTH_190418_Fall17 --Fs {P}/1_recleaner_230418_v2"
TREESONLYMEMZVETO = "-P "+P0+"/TREES_TTH_190418_Fall17_skim_3l_2j_2b1B_Zveto_presc --Fs {P}/1_recleaner_180518_v2 --Fs {P}/2_eventVars_230418_v2 --Fs {P}/3_kinMVA_withMEM_200618_v5 --Fs {P}/4_BDTv8_Hj_200618_v1 --Fs {P}/4_BDTrTT_Hj_200618_v1 --Fs {P}/4_BDThttTT_Hj_200618_v4 --Fs {P}/4_MEM_v4 --FMCs {P}/4_MEM_JECs_v1"
TREESONLYMEMZPEAK = "-P "+P0+"/TREES_TTH_190418_Fall17_skim_3l_2j_2b1B_Zpeak_presc --Fs {P}/1_recleaner_180518_v2 --Fs {P}/2_eventVars_230418_v2 --Fs {P}/3_kinMVA_withMEM_200618_v5 --Fs {P}/4_BDTv8_Hj_200618_v1 --Fs {P}/4_BDTrTT_Hj_200618_v1 --Fs {P}/4_BDThttTT_Hj_200618_v4 --Fs {P}/4_MEM_v4 --FMCs {P}/4_MEM_JECs_v1"

def base(selection):

    CORE=' '.join([TREES,TREESONLYSKIM])
    CORE+=" -f -j 8 -l 41.4 --s2v -L ttH-multilepton/functionsTTH.cc --tree treeProducerSusyMultilepton --mcc ttH-multilepton/lepchoice-ttH-FO.txt --split-factor=-1 --WA prescaleFromSkim "# --neg"
    RATIO= " --maxRatioRange 0.0  1.99 --ratioYNDiv 505 "
    RATIO2=" --showRatio --attachRatioPanel --fixRatioRange "
    LEGEND=" --legendColumns 2 --legendWidth 0.25 "
    LEGEND2=" --legendFontSize 0.042 "
    SPAM=" --noCms --topSpamSize 1.1 --lspam '#scale[1.1]{#bf{CMS}} #scale[0.9]{#it{Preliminary}}' "
    if dowhat == "plots": CORE+=RATIO+RATIO2+LEGEND+LEGEND2+SPAM+"  --showMCError --rebin 4 --xP 'nT_.*' --xP 'debug_.*'"

    if selection=='2lss':
        GO="%s ttH-multilepton/mca-2lss-mc.txt ttH-multilepton/2lss_tight.txt "%CORE
        GO="%s -W 'vtxWeight2017*eventBTagSF*leptonSF_ttH(LepGood_pdgId[iLepFO_Recl[0]],LepGood_pt[iLepFO_Recl[0]],LepGood_eta[iLepFO_Recl[0]],2)*leptonSF_ttH(LepGood_pdgId[iLepFO_Recl[1]],LepGood_pt[iLepFO_Recl[1]],LepGood_eta[iLepFO_Recl[1]],2)*triggerSF_ttH(LepGood_pdgId[iLepFO_Recl[0]],LepGood_pt[iLepFO_Recl[0]],LepGood_pdgId[iLepFO_Recl[1]],LepGood_pt[iLepFO_Recl[1]],nLepTight_Recl,0)'"%GO
        if dowhat in ["plots","ntuple"]: GO+=" ttH-multilepton/2lss_3l_plots.txt --xP '^lep(3|4)_.*' --xP '^(3|4)lep_.*' --xP 'kinMVA_3l_.*' "
        if dowhat == "plots": GO=GO.replace(LEGEND, " --legendColumns 3 --legendWidth 0.52 ")
        if dowhat == "plots": GO=GO.replace(RATIO,  " --maxRatioRange 0.6  1.99 --ratioYNDiv 210 ")
        GO += " --binname 2lss "
    elif selection=='3l':
        GO="%s ttH-multilepton/mca-3l-mc.txt ttH-multilepton/3l_tight.txt "%CORE
        GO="%s -W 'vtxWeight2017*eventBTagSF*leptonSF_ttH(LepGood_pdgId[iLepFO_Recl[0]],LepGood_pt[iLepFO_Recl[0]],LepGood_eta[iLepFO_Recl[0]],3)*leptonSF_ttH(LepGood_pdgId[iLepFO_Recl[1]],LepGood_pt[iLepFO_Recl[1]],LepGood_eta[iLepFO_Recl[1]],3)*leptonSF_ttH(LepGood_pdgId[iLepFO_Recl[2]],LepGood_pt[iLepFO_Recl[2]],LepGood_eta[iLepFO_Recl[2]],3)*triggerSF_ttH(LepGood_pdgId[iLepFO_Recl[0]],LepGood_pt[iLepFO_Recl[0]],LepGood_pdgId[iLepFO_Recl[1]],LepGood_pt[iLepFO_Recl[1]],nLepTight_Recl,0)'"%GO
        if dowhat in ["plots","ntuple"]: GO+=" ttH-multilepton/2lss_3l_plots.txt --xP '^(2|4)lep_.*' --xP '^lep4_.*' --xP 'kinMVA_2lss_.*' "
        if dowhat == "plots": GO=GO.replace(LEGEND, " --legendColumns 3 --legendWidth 0.42 ")
        GO += " --binname 3l "
    elif selection=='4l':
        GO="%s ttH-multilepton/mca-4l-mc.txt ttH-multilepton/4l_tight.txt "%CORE
        GO="%s -W 'vtxWeight2017*eventBTagSF*leptonSF_ttH(LepGood_pdgId[iLepFO_Recl[0]],LepGood_pt[iLepFO_Recl[0]],LepGood_eta[iLepFO_Recl[0]],3)*leptonSF_ttH(LepGood_pdgId[iLepFO_Recl[1]],LepGood_pt[iLepFO_Recl[1]],LepGood_eta[iLepFO_Recl[1]],3)*leptonSF_ttH(LepGood_pdgId[iLepFO_Recl[2]],LepGood_pt[iLepFO_Recl[2]],LepGood_eta[iLepFO_Recl[2]],3)*leptonSF_ttH(LepGood_pdgId[iLepFO_Recl[3]],LepGood_pt[iLepFO_Recl[3]],LepGood_eta[iLepFO_Recl[3]],3)*triggerSF_ttH(LepGood_pdgId[iLepFO_Recl[0]],LepGood_pt[iLepFO_Recl[0]],LepGood_pdgId[iLepFO_Recl[1]],LepGood_pt[iLepFO_Recl[1]],nLepTight_Recl,0)'"%GO
        if dowhat in ["plots","ntuple"]: GO+=" ttH-multilepton/2lss_3l_plots.txt --xP '^(2|3)lep_.*' --xP '^lep(1|2|3|4)_.*' --xP 'kinMVA_.*' "
        if dowhat == "plots": GO=GO.replace(LEGEND, " --legendColumns 2 --legendWidth 0.3 ")
        if dowhat == "plots": GO=GO.replace(RATIO,  " --maxRatioRange 0.0  2.99 --ratioYNDiv 505 ")
        GO += " --binname 4l "
    else:
        raise RuntimeError, 'Unknown selection'

    if '_prescale' in torun:
        GO = doprescale3l(GO,torun)

    return GO

def promptsub(x):
    procs = [ '' ]
    if dowhat == "cards": procs += ['_FRe_norm_Up','_FRe_norm_Dn','_FRe_pt_Up','_FRe_pt_Dn','_FRe_be_Up','_FRe_be_Dn','_FRm_norm_Up','_FRm_norm_Dn','_FRm_pt_Up','_FRm_pt_Dn','_FRm_be_Up','_FRm_be_Dn']
    return x + ' '.join(["--plotgroup data_fakes%s+='.*_promptsub%s'"%(x,x) for x in procs])+" --neglist '.*_promptsub.*' "
def procs(GO,mylist):
    return GO+' '+" ".join([ '-p %s'%l for l in mylist ])
def sigprocs(GO,mylist):
    return procs(GO,mylist)+' --showIndivSigs --noStackSig'
def runIt(GO,name,plots=[],noplots=[]):
    if '_74vs76' in name: GO = prep74vs76(GO)
    if dowhat == "plots":  
        if not ('forcePlotChoice' in sys.argv[3:]): print 'python mcPlots.py',"--pdir %s/%s"%(ODIR,name),GO,' '.join(['--sP %s'%p for p in plots]),' '.join(['--xP %s'%p for p in noplots]),' '.join(sys.argv[3:])
        else: print 'python mcPlots.py',"--pdir %s/%s"%(ODIR,name),GO,' '.join([x for x in sys.argv[3:] if x!='forcePlotChoice'])
    elif dowhat == "yields": print 'echo %s; python mcAnalysis.py'%name,GO,' '.join(sys.argv[3:])
    elif dowhat == "dumps":  print 'echo %s; python mcDump.py'%name,GO,' '.join(sys.argv[3:])
    elif dowhat == "ntuple": print 'echo %s; python mcNtuple.py'%name,GO,' '.join(sys.argv[3:])
def add(GO,opt):
    return '%s %s'%(GO,opt)
def setwide(x):
    x2 = add(x,'--wide')
    x2 = x2.replace('--legendWidth 0.35','--legendWidth 0.20')
    return x2
def fulltrees(x):
    return x.replace(TREESONLYSKIM,TREESONLYFULL)
def doprescale3l(x,torun):
    return x.replace(TREESONLYSKIM,TREESONLYMEMZPEAK if any([(_y in torun) for _y in ['cr_wz','cr_ttz','cr_fourlep_onZ','_Zpeak']]) else TREESONLYMEMZVETO)

allow_unblinding = True

if __name__ == '__main__':

    torun = sys.argv[2]

    if (not allow_unblinding) and '_data' in torun and (not any([re.match(x.strip()+'$',torun) for x in ['.*_appl.*','cr_.*','3l.*_Zpeak.*']])): raise RuntimeError, 'You are trying to unblind!'

    if '2lss_' in torun:
        x = base('2lss')
        if '_appl' in torun: x = add(x,'-I ^TT ')
        if '_1fo' in torun:
            x = add(x,"-A alwaystrue 1FO 'LepGood1_isLepTight+LepGood2_isLepTight==1'")
            x = x.replace("--xP 'nT_.*'","")
        if '_2fo' in torun: x = add(x,"-A alwaystrue 2FO 'LepGood1_isLepTight+LepGood2_isLepTight==0'")
        if '_relax' in torun: x = add(x,'-X ^TT ')
        if '_extr' in torun:
            x = x.replace('mca-2lss-mc.txt','mca-2lss-mc-sigextr.txt').replace('--showRatio --maxRatioRange 0 2','--showRatio --maxRatioRange 0 1 --ratioYLabel "S/B"')
        if '_data' in torun: x = x.replace('mca-2lss-mc.txt','mca-2lss-mcdata.txt')
        if '_table' in torun:
            x = x.replace('mca-2lss-mc.txt','mca-2lss-mc-table.txt')
        if '_frdata' in torun:
            x = promptsub(x)
            if '_blinddata' in torun:
                x = x.replace('mca-2lss-mc.txt','mca-2lss-mcdata.txt')
                x = add(x,'--xp data')
            elif not '_data' in torun: raise RuntimeError
            x = x.replace('mca-2lss-mcdata.txt','mca-2lss-mcdata-frdata.txt')
            if '_table' in torun:
                x = x.replace('mca-2lss-mcdata-frdata.txt','mca-2lss-mcdata-frdata-table.txt')

        if '_mll200' in torun:
            x = add(x,"-E ^mll200 ")

        if '_splitfakes' in torun:
            x = x.replace('mca-2lss-mc.txt','mca-2lss-mc-flavsplit.txt')
            
        if '_closuretest' in torun:
            x = x.replace('mca-2lss-mc.txt','mca-2lss-mc-closuretest.txt')
            x = x.replace("--maxRatioRange 0.6  1.99 --ratioYNDiv 210", "--maxRatioRange 0.0 1.99 --fixRatioRange ")
            x = x.replace("--legendColumns 3", "--legendColumns 2")
            x = add(x,"--AP --plotmode nostack --sP 2lep_catIndex_nosign --sP 2lep_catIndex --sP kinMVA_2lss_ttbar --sP kinMVA_2lss_ttV --sP nBJetMedium25 --sP 2lep_nJet25_from4")
            x = add(x,"-p TT_FR_QCD -p TT_FR_TT -p TT_fake --ratioDen TT_FR_QCD --ratioNums TT_fake,TT_FR_TT --errors ")
            if '_closuretest_norm' in torun:
                x = x.replace("--plotmode nostack","--plotmode norm")
                x = x.replace("--ratioNums TT_fake,TT_FR_TT","--ratioNums TT_fake")
                x = add(x,"--fitRatio 1")
                if '_unc' in torun:
                    x = add(x,"--su CMS_ttHl16_Clos_[em]_norm")
            else:
                if '_uncfull' in torun:
                    x = add(x,"--su 'CMS_ttHl16_FR.*' ")
                elif '_unc' in torun:
                    x = add(x,"--su 'CMS_ttHl16_Clos_[em].*_norm' ")
            if '_mufake' in torun: x = add(x,"-A alwaystrue mufake '(abs(LepGood1_pdgId)==13 && LepGood1_mcMatchId==0) || (abs(LepGood2_pdgId)==13 && LepGood2_mcMatchId==0)'")
            if '_elfake' in torun: x = add(x,"-A alwaystrue elfake '(abs(LepGood1_pdgId)==11 && LepGood1_mcMatchId==0) || (abs(LepGood2_pdgId)==11 && LepGood2_mcMatchId==0)'")
            if '_bloose' in torun: x = add(x,'-E ^BLoose ')
            if '_btight' in torun: x = add(x,'-E ^BTight ')
            if '_nobcut' in torun: x = add(x,'-X ^2b1B ')
            if '_notrigger' in torun: x = add(x,'-X ^trigger ' )

        if '_unc' in torun:
            x = add(x,"--unc ttH-multilepton/systsUnc.txt")

        if '_varsFR' in torun:
            x = x.replace('mca-2lss-mc.txt','mca-2lss-data-frdata-vars.txt')
            x = add(x,"--plotmode nostack --xP '.*Binning' --sP 'kinMVA_.*' --sP 2lep_catIndex")
            x = add(x,"--ratioDen data_fakes --ratioNums 'data_fakes_.*'")
            if '_norm' in torun:
                x = x.replace("--plotmode nostack","--plotmode norm")
            if '_fit' in torun:
                x = add(x,"--fitRatio 1")
            if '_varsFR_e' in torun: x = add(x,"--xp 'data_fakes_m_.*'")
            if '_varsFR_m' in torun: x = add(x,"--xp 'data_fakes_e_.*'")

        if '_Xh' in torun:
            x = x.replace('4_BDTv8_Hj_230217_v6','4_BDTv8_Hj_Xmass_bkg')
            x = x.replace('mca-2lss-mc.txt','mca-2lss-mc-sigextr-Xh.txt').replace('--showRatio','')
            x = x.replace('--legendColumns 3 --legendWidth 0.46','--legendWidth 0.30')
            x = x.replace('--showMCError','')
            x = add(x,'--plotmode norm')
            x = add(x,"--sP kinMVA_input_BDTv8_eventReco_X_mass --sP kinMVA_2lss_ttbar_withBDTv8 --sP kinMVA_input_BDTv8_eventReco_MT_HadLepTop_MET")

        runIt(x,'%s'%torun)
        if '_flav' in torun:
            for flav in ['mm','ee','em']: 
                runIt(add(x,'-E ^%s'%flav).replace("--binname 2lss","--binname 2lss_"+flav),'%s/%s'%(torun,flav))
        if '_catnosign' in torun:
            for flav in ['mm','ee','em']: 
                runIt(add(x,'-E ^%s'%flav).replace("--binname 2lss","--binname 2lss_"+flav),'%s/%s'%(torun,flav))
            for flav in ['mm_bt','mm_bl','em_bt','em_bl']: 
                runIt(add(x,'-E ^%s -E ^B%s'%(flav[:2], ("Tight" if "bt" in flav else "Loose"))).replace("--binname 2lss","--binname 2lss_"+flav),'%s/%s'%(torun,flav))
            for flav in ['btight','bloose']: 
                runIt(add(x,' -E ^B%s'%("Tight" if "bt" in flav else "Loose")),'%s/%s'%(torun,flav))
        if '_cats' in torun:
            for cat in ['b2lss_ee_neg','b2lss_ee_pos',\
                            'b2lss_em_bl_neg','b2lss_em_bl_pos','b2lss_em_bt_neg','b2lss_em_bt_pos',\
                            'b2lss_mm_bl_neg','b2lss_mm_bl_pos','b2lss_mm_bt_neg','b2lss_mm_bt_pos']:
                runIt(add(x,'-E ^%s'%cat).replace("--binname 2lss","--binname %s" % cat[1:-4]),'%s/%s'%(torun,cat))


    if '3l_' in torun:
        x = base('3l')
        if '_appl' in torun: x = add(x,'-I ^TTT ')
        if '_1fo' in torun:
            x = add(x,"-A alwaystrue 1FO 'LepGood1_isLepTight+LepGood2_isLepTight+LepGood3_isLepTight==2'")
            x = x.replace("--xP 'nT_.*'","")
        if '_relax' in torun: x = add(x,'-X ^TTT ')
        if '_extr' in torun:
            x = x.replace('mca-3l-mc.txt','mca-3l-mc-sigextr.txt').replace('--showRatio --maxRatioRange 0 2','--showRatio --maxRatioRange 0 1 --ratioYLabel "S/B"')
        if '_data' in torun: x = x.replace('mca-3l-mc.txt','mca-3l-mcdata.txt')
        if '_frdata' in torun:
            x = promptsub(x)
            if '_blinddata' in torun:
                x = x.replace('mca-3l-mc.txt','mca-3l-mcdata.txt')
                x = add(x,'--xp data')
            elif not '_data' in torun: raise RuntimeError
            x = x.replace('mca-3l-mcdata.txt','mca-3l-mcdata-frdata.txt')
            if '_table' in torun:
                x = x.replace('mca-3l-mcdata-frdata.txt','mca-3l-mcdata-frdata-table.txt')
        if '_table' in torun:
            x = x.replace('mca-3l-mc.txt','mca-3l-mc-table.txt')

        if '_closuretest' in torun:
            x = x.replace('mca-3l-mc.txt','mca-3l-mc-closuretest.txt')
            #x = x.replace("--maxRatioRange 0 3","--maxRatioRange 0.5 1.5")
            x = add(x,"--AP --plotmode nostack --sP kinMVA_3l_ttbar --sP kinMVA_3l_ttV --sP --sP 3lep_catIndex --sP nBJetMedium25 --sP 3lep_nJet25 --sP 3lep_n_ele")
            x = add(x,"-p TT_FR_QCD -p TT_FR_TT -p TT_fake --ratioDen TT_FR_QCD --ratioNums TT_fake,TT_FR_TT --errors ")
            x = x.replace('--showMCError','')
            x = x.replace('--legendWidth 0.42','--legendWidth 0.60')
            if '_closuretest_norm' in torun:
                x = x.replace("--plotmode nostack","--plotmode norm")
                x = x.replace("--ratioNums TT_fake,TT_FR_TT","--ratioNums TT_fake")
                x = add(x,"--fitRatio 1")
                if '_unc' in torun:
                    x = add(x,"--su CMS_ttHl16_Clos_[em]_norm")
            else:
                if '_uncfull' in torun:
                    x = add(x,"--su 'CMS_ttHl16_FR.*' ")
                elif '_unc' in torun:
                    x = add(x,"--su 'CMS_ttHl16_Clos_[em].*_norm' ")
            if '_mufake' in torun: x = add(x,"-A alwaystrue mufake '(abs(LepGood1_pdgId)==13 && LepGood1_mcMatchId==0) || (abs(LepGood2_pdgId)==13 && LepGood2_mcMatchId==0) || (abs(LepGood3_pdgId)==13 && LepGood3_mcMatchId==0)'")
            if '_elfake' in torun: x = add(x,"-A alwaystrue elfake '(abs(LepGood1_pdgId)==11 && LepGood1_mcMatchId==0) || (abs(LepGood2_pdgId)==11 && LepGood2_mcMatchId==0) || (abs(LepGood3_pdgId)==11 && LepGood3_mcMatchId==0)'")
            if '_bloose' in torun: x = add(x,'-E ^BLoose ')
            if '_btight' in torun: x = add(x,'-E ^BTight ')
            if '_nobcut' in torun: x = add(x,'-X ^2b1B ')
            if '_notrigger' in torun: x = add(x,'-X ^trigger ')

        if '_unc' in torun:
            x = add(x,"--unc ttH-multilepton/systsUnc.txt")

        if '_varsFR' in torun:
            torun += "_"+sys.argv[-1]
            x = x.replace('mca-3l-mc.txt','mca-3l-data-frdata-%s.txt'%sys.argv[-1])
            x = x.replace("--maxRatioRange 0 3","--maxRatioRange 0 2")
            x = add(x,"--plotmode nostack --sP kinMVA_3l_ttbar --sP kinMVA_3l_ttV_withMEM --sP kinMVA_3l_ttV")
            x = add(x,"--ratioDen fakes_data --ratioNums fakes_data_%s --errors"%sys.argv[-1])
            if '_varsFR_norm' in torun:
                x = x.replace("--plotmode nostack","--plotmode norm")
                x = add(x,"--fitRatio 1")
        if '_x2j' in torun:
            x = add(x,"-E ^x2j ")
        if '_Zpeak' in torun:
            x = add(x,'-I ^Zveto')
        runIt(x,'%s'%torun)
        if '_cats' in torun:
            for cat in ['b3l_bl_neg','b3l_bl_pos','b3l_bt_neg','b3l_bt_pos']:
                runIt(add(x,'-E ^%s'%cat).replace("--binname 3l","--binname %s" % cat[1:-4]),'%s/%s'%(torun,cat))
        if '_catnosign' in torun:
            for flav in ['btight','bloose']: 
                runIt(add(x,' -E ^B%s'%("Tight" if "bt" in flav else "Loose")).replace("--binname 3l","--binname 3l_%s" % flav[:2]),'%s/%s'%(torun,flav))


    if '4l_' in torun:
        x = base('4l')
        if '_appl' in torun: x = add(x,'-I ^TTTT ')
        if '_relax' in torun: x = add(x,'-X ^TTTT ')
        if '_data' in torun: x = x.replace('mca-4l-mc.txt','mca-4l-mcdata.txt')
        if '_frdata' in torun:
            x = promptsub(x)
            raise RuntimeError, 'Fakes estimation not implemented for 4l'
        if '_unc' in torun:
            x = add(x,"--unc ttH-multilepton/systsUnc.txt")
        runIt(x,'%s'%torun)

    if 'cr_3j' in torun:
        x = base('2lss')
        if '_data' in torun: x = x.replace('mca-2lss-mc.txt','mca-2lss-mcdata.txt')
        if '_frdata' in torun:
            x = promptsub(x)
            if not '_data' in torun: raise RuntimeError
            x = x.replace('mca-2lss-mcdata.txt','mca-2lss-mcdata-frdata.txt')
        x = add(x,"-R ^4j 3j 'nJet25==3'")
        if '_unc' in torun:
            x = add(x,"--unc ttH-multilepton/systsUnc.txt")

        plots = ['2lep_.*','nJet25','nBJetLoose25','nBJetMedium25','met','metLD','htJet25j','mhtJet25','mtWmin','htllv','kinMVA_2lss_ttbar.*','kinMVA_2lss_ttV.*','kinMVA_2lss_bins7','kinMVA_input.*','era']
        runIt(x,'%s'%torun,plots)
        if '_flav' in torun:
            for flav in ['mm','ee','em']:
                runIt(add(x,'-E ^%s'%flav).replace("--binname 2lss","--binname 2lss_"+flav),'%s/%s'%(torun,flav))

    if 'cr_ttbar' in torun:
        x = base('2lss')
        x = fulltrees(x) # for mc same-sign
        x = x.replace('mca-2lss-mc.txt','mca-2lss-mcdata-ttbar.txt')
        if '_data' not in torun: x = add(x,'--xp data')
        if '_appl' in torun: x = add(x,'-I ^TT ')
        if '_1fo' in torun: x = add(x,"-A alwaystrue 1FO 'LepGood1_isLepTight+LepGood2_isLepTight==1'")
        if '_leadmupt25' in torun: x = add(x,"-A 'entry point' leadmupt25 'abs(LepGood1_pdgId)==13 && LepGood1_pt>25'")
        if '_norm' in torun:
            x = add(x,"--sp '.*' --scaleSigToData")
        x = add(x,"-I same-sign -X ^4j -X ^2b1B -E ^2j -E ^em ")
        if '_highMetNoBCut' in torun: x = add(x,"-A 'entry point' highMET 'met_pt>60'")
        else: x = add(x,"-E ^1B ")
        if '_unc' in torun:
            x = add(x,"--unc ttH-multilepton/systsUnc.txt")
        plots = ['2lep_.*','met','metLD','nVert','nJet25','nBJetMedium25','nBJetLoose25','nBJetLoose40','nBJetMedium40','era']
        runIt(x,'%s'%torun)#,plots)

    if 'cr_zjets' in torun:
        x = base('2lss')
        x = x.replace('mca-2lss-mc.txt','mca-2lss-mcdata-ttbar.txt')
        x = x.replace('--maxRatioRange 0 3','--maxRatioRange 0.8 1.2')
        if '_ss' not in torun:
            x = fulltrees(x)
            x = add(x,"-I same-sign")
        else:
            x = add(x,"-X ^metLDee")
        if '_data' not in torun: x = add(x,'--xp data')
        x = add(x,"-X ^2b1B -X ^Zee_veto -A alwaystrue mllonZ 'mass_2(LepGood1_conePt,LepGood1_eta,LepGood1_phi,LepGood1_mass,LepGood2_conePt,LepGood2_eta,LepGood2_phi,LepGood2_mass)>60 && mass_2(LepGood1_conePt,LepGood1_eta,LepGood1_phi,LepGood1_mass,LepGood2_conePt,LepGood2_eta,LepGood2_phi,LepGood2_mass)<120'")
        if '_unc' in torun:
            x = add(x,"--unc ttH-multilepton/systsUnc.txt")
        for flav in ['mm','ee']:
            plots = ['2lep_.*','tot_weight','era']
            runIt(add(x,'-E ^%s -X ^4j'%flav),'%s/%s'%(torun,flav),plots)

    if 'cr_wz' in torun:
        x = base('3l')
        x = x.replace("--binname 3l","--binname 3l_crwz")
        x = add(x,"-I 'Zveto' -I ^2b1B ")
        x = add(x, " --Fs {P}/7_bestMTW3l_v1 ")
        if '_data' in torun: x = x.replace('mca-3l-mc.txt','mca-3l-mcdata.txt')
        if '_frdata' in torun:
            x = promptsub(x)
            if not '_data' in torun: raise RuntimeError
            x = x.replace('mca-3l-mcdata.txt','mca-3l-mcdata-frdata.txt')
        else: 
            print "ERROR: cr_wz with MC backgrounds does not work."
        if '_unc' in torun:
            x = add(x,"--unc ttH-multilepton/systsUnc.txt")
        if '_fit' in torun:
            if not '_data' in torun: raise RuntimeError
            x = add(x,"--sP tot_weight --preFitData tot_weight --sp WZ ")
            x = add(x,"--xu CMS_ttHl_ZZ_lnU ") # otherwise here we fit as ZZ
            if '_unc' not in torun:
                print "Will just float WZ freely"
                x = add(x,"--flp WZ")
        plots = ['3lep_mtW','3lep_nJet25','tot_weight','met','metLD','htJet25j','nBJetLoose25']
        if '_more' in torun:
            plots += ['lep3_pt','metLD','nBJetLoose25','3lep_worseIso','minMllAFAS','3lep_worseMVA','3lep_mtW','kinMVA.*','htJet25j','nJet25','era']
            plots += ['3lep_.*','nJet25','nBJetLoose25','nBJetMedium25','met','metLD','htJet25j','mhtJet25','mtWmin','htllv','kinMVA_3l_ttbar','kinMVA_3l_ttV','kinMVA_3l_ttV_withMEM']
        runIt(x,'%s'%torun,plots)

    if 'cr_ttz' in torun:
        x = base('3l')
        if '_data' in torun: x = x.replace('mca-3l-mc.txt','mca-3l-mcdata.txt')
        if '_frdata' in torun:
            x = promptsub(x)
            if not '_data' in torun: raise RuntimeError
            x = x.replace('mca-3l-mcdata.txt','mca-3l-mcdata-frdata.txt')
        plots = ['lep2_pt','met','nJet25','mZ1']
        plots += ['3lep_.*','nJet25','nBJetLoose25','nBJetMedium25','met','metLD','htJet25j','mhtJet25','mtWmin','htllv','kinMVA_3l_ttbar','kinMVA_3l_ttV','kinMVA_3l_ttV_withMEM','era']
        x = add(x,"-I 'Zveto' -X ^2b1B -E ^gt2b -E ^1B ")
        if '_unc' in torun:
            x = add(x,"--unc ttH-multilepton/systsUnc.txt")
        if '_4j' in torun:
            x = add(x,"-E ^4j ")
            runIt(x,'%s/4j'%torun,plots)
        else:
            runIt(x,'%s'%torun,plots)

    if 'cr_fourlep_onZ' in torun:
        x = base('4l').replace('mca-4l-mc.txt','mca-4l-mcdata.txt')
        if '_data' not in torun: x = add(x, "--xp data ")
        if '_frdata' in torun:
            x = promptsub(x)
            raise RuntimeError, 'Fakes estimation not implemented for 4l'
        if '_unc' in torun:
            x = add(x,"--unc ttH-multilepton/systsUnc.txt")
        x = add(x,"-I ^Zveto")
        plots = ['lep4_pt','met','mZ1','4lep_m4l_noRecl','4lep_mZ2_noRecl','minMllAFAS','tot_weight','4lep_nJet25','nBJetMedium25']
        runIt(x,'%s'%torun,plots)
    if 'cr_zz' in torun:
        x = base('4l')
        x = x.replace('mca-4l-mc.txt','mca-4l-mcdata.txt')
        x = x.replace("--binname 4l","--binname 4l_crzz")
        x = add(x,"-I ^Zveto -I ^2b1B")
        if '_data' not in torun: x = add(x, "--xp data ")
        if '_frdata' in torun:
            x = promptsub(x)
            raise RuntimeError, 'Fakes estimation not implemented for 4l'
        if '_unc' in torun:
            x = add(x,"--unc ttH-multilepton/systsUnc.txt")
        if '_fit' in torun:
            if not '_data' in torun: raise RuntimeError
            x = add(x,"--sP tot_weight --preFitData tot_weight --sp ZZ ")
            x = add(x,"--xu CMS_ttHl_WZ_lnU ") # otherwise here we fit as WZ
            if '_unc' not in torun:
                print "Will just float WZ freely"
                x = add(x,"--flp WZ")
        plots = ['lep4_pt','met','mZ1','4lep_m4l_noRecl','4lep_mZ2_noRecl','minMllAFAS','tot_weight','4lep_nJet25']
        runIt(x,'%s'%torun,plots)

        
