#!/bin/bash
## ------------------------------------------- ##
## !!!THIS WORKS FOR 2LSS ONLY!!!              ##
## $1  is out dir = no                         ##
## $2  is year    = 6, 7 or 8                  ##
## $3  is either  = Top-tagged or NoTop-tagged ##
## ------------------------------------------- ##
if [ "$2" == "6" ]; then
#python ttH-multilepton/ttH_plots.py $1 201$2 2lss_$3 -p ttH,TTWW,TTW,TTZ,EWK,Rares,TT,DY,WJets,SingleTop,WW,Flips,Convs
python ttH-multilepton/ttH_plots.py $1 201$2 2lss_$3 -p ttH
fi
if [ "$2" == "7" ]; then
#python ttH-multilepton/ttH_plots.py $1 201$2 2lss_$3 -p ttH,tHW,TTWW,TTW,TTZ,WZ,ZZ,Rares,tttt,tZq,TT,DY,WJets,SingleTop,WW,Flips,Convs
python ttH-multilepton/ttH_plots.py $1 201$2 2lss_$3 -p ttH
fi
if [ "$2" == "8" ]; then
#python ttH-multilepton/ttH_plots.py $1 201$2 2lss_$3 -p ttH,TTWW,TTW,TTZ,WZ,ZZ,Rares,tttt,tZq,TT,DY,WJets,SingleTop,WW,Flips,Convs
python ttH-multilepton/ttH_plots.py $1 201$2 2lss_$3 -p ttH
fi
