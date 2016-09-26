#!/usr/bin/env python
import sys

ODIR="~/www/data13fb_validation_aug03"
MYTREEDIR="/data1/peruzzi/mixture_jecv6prompt_datafull_jul20"
MYLUMI="12.9"

EXE="python mcPlots.py"
WDIR="lepton-validation"
COMMOPT='--s2v --tree treeProducerSusyMultilepton --rspam "%(lumi) (13 TeV)  " --lspam "#bf{CMS} #it{Preliminary}" --legendBorder=0 --legendFontSize 0.055 --legendWidth=0.30  -j 8 -f --sp ".*" --showMCError -W "puw2016_nTrueInt_13fb(nTrueInt)" -A filters sip8 "LepGood_sip3d[iChosen]<8" --mcc ttH-multilepton/mcc-ichepMediumMuonId.txt '+(' '.join(sys.argv[1:]))

#SELECTIONS=["ZtoEE","ZtoMuMu","ttbar","Wl","Zl","ttbar_semiLeptonic"]
SELECTIONS=["ttbar","ttbar_semiLeptonic"]
#SELECTIONS=["ZtoEE","ttbar","Wl"]

for SEL in SELECTIONS:
    print '#'+SEL
    MCA = 'mca_13tev_%s.txt'%SEL if SEL in ["ttbar",'Wl','Zl','ttbar_semiLeptonic'] else 'mca_13tev.txt'
    MYMCC = '--mcc %s/mcc_%s.txt'%(WDIR,SEL)
    COARSE = '_coarse' if SEL in ['Wl','Zl','ttbar_semiLeptonic'] else ''
    print '%s %s/%s %s/cuts_%s.txt %s/plots_lepquantities%s.txt %s -P %s -l %s %s --scaleSigToData --pdir %s/%s/ScaleToData --sP lep_mvaTTH_log'%(EXE,WDIR,MCA,WDIR,SEL,WDIR,COARSE,COMMOPT,MYTREEDIR,MYLUMI,MYMCC,ODIR,SEL)
#    print '%s %s/%s %s/cuts_%s.txt %s/plots_lepquantities%s.txt %s -P %s -l %s %s --pdir %s/%s/ScaleToLumi'%(EXE,WDIR,MCA,WDIR,SEL,WDIR,COARSE,COMMOPT,MYTREEDIR,MYLUMI,MYMCC,ODIR,SEL)
#    print '%s %s/%s %s/cuts_%s.txt %s/plots_eventquantities.txt %s -P %s -l %s %s --scaleSigToData --pdir %s/%s/ScaleToData'%(EXE,WDIR,MCA,WDIR,SEL,WDIR,COMMOPT,MYTREEDIR,MYLUMI,MYMCC,ODIR,SEL)
#    print '%s %s/%s %s/cuts_%s.txt %s/plots_eventquantities.txt %s -P %s -l %s %s --pdir %s/%s/ScaleToLumi'%(EXE,WDIR,MCA,WDIR,SEL,WDIR,COMMOPT,MYTREEDIR,MYLUMI,MYMCC,ODIR,SEL)


#SELECTIONS=["ttbar_application"]
#for SEL in SELECTIONS:
#    print '#'+SEL
#    MCA = 'mca_13tev.txt'
#    print '%s %s/%s %s/cuts_%s.txt %s/plots_eventquantities.txt %s -P %s -l %s --pdir %s/%s/ScaleToLumi'%(EXE,WDIR,MCA,WDIR,SEL,WDIR,COMMOPT,MYTREEDIR,MYLUMI,ODIR,SEL)
