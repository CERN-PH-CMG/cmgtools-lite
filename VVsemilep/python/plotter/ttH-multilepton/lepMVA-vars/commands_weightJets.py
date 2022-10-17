#!/usr/bin/env python

ODIR="~/www/25ns_run2015cd_76X_24febNEW_weightJets"
MYTREEDIR="/data1/peruzzi/TREES_76X_200216_jecV1M2"
MYLUMI="2.26"

EXE="python mcPlots.py"
WDIR="ttH-multilepton/lepMVA-vars"
COMMOPT='--s2v --tree treeProducerSusyMultilepton -W "puw(nTrueInt)*eventBTagSF" -F sf/t {P}/2_recleaner_v8_b1E2/evVarFriend_{cname}.root -F sf/t {P}/5_eventBTagRWT_onlyJets_v1/evVarFriend_{cname}.root --mcc ttH-multilepton/ttH_2lss3l_triggerdefs.txt --rspam "%(lumi) (13 TeV)  " --lspam "#bf{CMS} #it{Preliminary}" --legendBorder=0 --legendFontSize 0.055 --legendWidth=0.35 --showRatio --maxRatioRange 0 2 --showRatio --poisson --showMCError -j 12 -f --sp ".*"'

SELECTIONS=["ttbar_MLM","ttbar_semiLeptonic","ZtoEE","ZtoMuMu","Wl","Zl"]#,"ttbar_Powheg","ttbar_MLM","ttbar_aMCatNLO","ttbar_Powheg_scaleUp","ttbar_aMCatNLO_scaleUp"]

for SEL in SELECTIONS:
    print '#'+SEL
    MCA = 'mca_13tev_%s.txt'%SEL if SEL in ["ttbar_Powheg","ttbar_aMCatNLO","ttbar_MLM","ttbar_Powheg_scaleUp","ttbar_aMCatNLO_scaleUp",'Wl','Zl','ttbar_semiLeptonic'] else 'mca_13tev.txt'
    MYMCC = '--mcc %s/mcc_%s.txt'%(WDIR,SEL)
    COARSE = '_coarse' if SEL in ['Wl','Zl','ttbar_semiLeptonic'] else ''
    print '%s %s/%s %s/cuts_%s.txt %s/plots_lepquantities%s.txt %s -P %s -l %s %s --scaleSigToData --fitRatio 1 --pdir %s/%s/ScaleToData'%(EXE,WDIR,MCA,WDIR,SEL,WDIR,COARSE,COMMOPT,MYTREEDIR,MYLUMI,MYMCC,ODIR,SEL)
    print '%s %s/%s %s/cuts_%s.txt %s/plots_lepquantities%s.txt %s -P %s -l %s %s --pdir %s/%s/ScaleToLumi'%(EXE,WDIR,MCA,WDIR,SEL,WDIR,COARSE,COMMOPT,MYTREEDIR,MYLUMI,MYMCC,ODIR,SEL)
    print '%s %s/%s %s/cuts_%s.txt %s/plots_eventquantities.txt %s -P %s -l %s %s --pdir %s/%s/ScaleToLumi'%(EXE,WDIR,MCA,WDIR,SEL,WDIR,COMMOPT,MYTREEDIR,MYLUMI,MYMCC,ODIR,SEL)


# to be adapted
#SELECTIONS=["ttbar_application"]
#for SEL in SELECTIONS:
#    print '#'+SEL
#    MCA = 'mca_13tev.txt'
#    print '%s %s/%s %s/cuts_%s.txt %s/plots_eventquantities.txt %s -P %s -l %s --pdir %s/%s/ScaleToLumi'%(EXE,WDIR,MCA,WDIR,SEL,WDIR,COMMOPT,MYTREEDIR,MYLUMI,ODIR,SEL)
