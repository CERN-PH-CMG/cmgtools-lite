#!/usr/bin/env python
import sys

ODIR="~/www/data_postICHEP2016_validation_oct12"
MYTREEDIR="/data1/peruzzi/TREES_80X_280916_dataEFG -P /data1/peruzzi/mixture_jecv6prompt_datafull_jul20"

EXE="python mcPlots.py"
WDIR="lepton-validation"
COMMOPT0='--s2v --tree treeProducerSusyMultilepton --cms --legendBorder=0 --legendFontSize 0.055 --legendWidth=0.30  -j 8 -f --sp ".*" --showMCError -A filters sip8 "LepGood_sip3d[iChosen]<8" --mcc ttH-multilepton/mcc-ichepMediumMuonId.txt --showRatio --fixRatioRange --maxRatioRange 0 2 '+(' '.join(sys.argv[1:]))

COMMOPT1='-W "puw2016_nTrueInt_13fb(nTrueInt)" -l 12.9 --xf ".*Run2016E.*,.*Run2016F.*,.*Run2016G.*"'
COMMOPT2='-W "puw2016_nTrueInt_EF(nTrueInt)" -l 7.3 --xf ".*Run2016B.*,.*Run2016C.*,.*Run2016D.*,.*Run2016G.*"'
COMMOPT3='-W "puw2016_nTrueInt_G_upto279931(nTrueInt)" -l 4.3 --xf ".*Run2016B.*,.*Run2016C.*,.*Run2016D.*,.*Run2016E.*,.*Run2016F.*"'
commopts=[(y,COMMOPT0+' '+x) for x,y in [(COMMOPT1,'BCD'),(COMMOPT2,'EF'),(COMMOPT3,'G')]][2:3]

#SELECTIONS=["ZtoEE","ZtoMuMu","ttbar","Wl","Zl","ttbar_semiLeptonic"]
#SELECTIONS=["ttbar","ttbar_semiLeptonic"][:1]
#SELECTIONS=["ZtoEE","ttbar","Wl"]
SELECTIONS=["ZtoMuMu","ZtoEE","ttbar","ttbar_semiLeptonic","Zl"]

for period,COMMOPT in commopts:
    for SEL in SELECTIONS:
        print '#'+SEL
        MCA = 'mca_13tev_%s.txt'%SEL if SEL in ["ttbar",'Wl','Zl','ttbar_semiLeptonic'] else 'mca_13tev.txt'
        MYMCC = '--mcc %s/mcc_%s.txt'%(WDIR,SEL)
        COARSE = '_coarse' if SEL in ['Wl','Zl','ttbar_semiLeptonic'] else ''
        print '%s %s/%s %s/cuts_%s.txt %s/plots_lepquantities%s.txt %s -P %s %s --scaleSigToData --pdir %s/%s/ScaleToData/%s'%(EXE,WDIR,MCA,WDIR,SEL,WDIR,COARSE,COMMOPT,MYTREEDIR,MYMCC,ODIR,SEL,period)
        #    print '%s %s/%s %s/cuts_%s.txt %s/plots_lepquantities%s.txt %s -P %s  %s --pdir %s/%s/ScaleToLumi/%s'%(EXE,WDIR,MCA,WDIR,SEL,WDIR,COARSE,COMMOPT,MYTREEDIR,MYMCC,ODIR,SEL,period)
        print '%s %s/%s %s/cuts_%s.txt %s/plots_eventquantities.txt %s -P %s  %s --scaleSigToData --pdir %s/%s/ScaleToData/%s'%(EXE,WDIR,MCA,WDIR,SEL,WDIR,COMMOPT,MYTREEDIR,MYMCC,ODIR,SEL,period)
        #    print '%s %s/%s %s/cuts_%s.txt %s/plots_eventquantities.txt %s -P %s  %s --pdir %s/%s/ScaleToLumi/%s'%(EXE,WDIR,MCA,WDIR,SEL,WDIR,COMMOPT,MYTREEDIR,MYMCC,ODIR,SEL,period)


#SELECTIONS=["ttbar_application"]
#for SEL in SELECTIONS:
#    print '#'+SEL
#    MCA = 'mca_13tev.txt'
#    print '%s %s/%s %s/cuts_%s.txt %s/plots_eventquantities.txt %s -P %s  --pdir %s/%s/ScaleToLumi'%(EXE,WDIR,MCA,WDIR,SEL,WDIR,COMMOPT,MYTREEDIR,ODIR,SEL)
