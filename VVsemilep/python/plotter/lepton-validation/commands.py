#!/usr/bin/env python
import sys

ODIR="~/www/data_validation_full2016_250117"
MYTREEDIR="/data1/peruzzi/TREES_TTH_250117_Summer16_JECV3_noClean_qgV2 --Fs {P}/1_recleaner_250117_v1 "

EXE="python mcPlots.py"
WDIR="lepton-validation"
COMMOPT=' -l 36.5 -W "puw2016_nTrueInt_36fb(nTrueInt)"'
COMMOPT+=' --s2v --tree treeProducerSusyMultilepton --lspam "#bf{CMS} #it{Preliminary}" --legendBorder=0 --legendFontSize 0.055 --legendWidth=0.30  -j 8 -f --sp ".*" --showMCError --showRatio --fixRatioRange --maxRatioRange 0 2 '+(' '.join(sys.argv[1:]))
COMMOPT+=' --mcc ttH-multilepton/ttH_2lss3l_triggerdefs.txt --mcc ttH-multilepton/lepchoice-ttH-FO.txt '

#SELECTIONS=["ZtoMuMu","ZtoEE","ttbar","ttbar_semiLeptonic","Wl","Zl"]
SELECTIONS=["ttbar_semiLeptonic","Wl","ttbar","Zl","ZtoMuMu","ZtoEE"]

for SEL in SELECTIONS:
    print '#'+SEL
    MCA = 'mca_13tev_%s.txt'%SEL if SEL in ["ttbar",'Wl','Zl','ttbar_semiLeptonic'] else 'mca_13tev.txt'
    MYMCC = '--mcc %s/mcc_%s.txt'%(WDIR,SEL)
    COARSE = '_coarse' if SEL in ['Wl','Zl','ttbar_semiLeptonic'] else ''
    #print '%s %s/%s %s/cuts_%s.txt %s/plots_lepquantities%s.txt %s -P %s %s --scaleSigToData --pdir %s/%s/ScaleToData'%(EXE,WDIR,MCA,WDIR,SEL,WDIR,COARSE,COMMOPT,MYTREEDIR,MYMCC,ODIR,SEL)
    print '%s %s/%s %s/cuts_%s.txt %s/plots_lepquantities%s.txt %s -P %s  %s --pdir %s/%s'%(EXE,WDIR,MCA,WDIR,SEL,WDIR,COARSE,COMMOPT,MYTREEDIR,MYMCC,ODIR,SEL)
    #print '%s %s/%s %s/cuts_%s.txt %s/plots_eventquantities.txt %s -P %s  %s --scaleSigToData --pdir %s/%s/ScaleToData'%(EXE,WDIR,MCA,WDIR,SEL,WDIR,COMMOPT,MYTREEDIR,MYMCC,ODIR,SEL)
    print '%s %s/%s %s/cuts_%s.txt %s/plots_eventquantities.txt %s -P %s  %s --pdir %s/%s'%(EXE,WDIR,MCA,WDIR,SEL,WDIR,COMMOPT,MYTREEDIR,MYMCC,ODIR,SEL)


#SELECTIONS=["ttbar_application"]
#for SEL in SELECTIONS:
#    print '#'+SEL
#    MCA = 'mca_13tev.txt'
#    print '%s %s/%s %s/cuts_%s.txt %s/plots_eventquantities.txt %s -P %s  --pdir %s/%s'%(EXE,WDIR,MCA,WDIR,SEL,WDIR,COMMOPT,MYTREEDIR,ODIR,SEL)
