#!/bin/bash
# run from /plotter, one dir up
## ------------------------------------------- ##
## !!!THIS WORKS FOR 2LSS ONLY!!!              ##
## $1  is year    = 6, 7 or 8                  ##
## $2  is either  = Top-tagged or NoTop-tagged ##
## e.g --> ./diff_plot.sh 6 Top-tagged         ## 
## ------------------------------------------- ##
if [ "$1" == "6" ]; then
python ttH-multilepton/ttH_plots.py ../../macros/diff/diff_2lss_v6_plots 201$1 2lss_diff_$2 -p ttH,TTWW,TTW,TTZ,EWK,Rares,TT,DY,WJets,SingleTop,WW,Flips,Convs
fi
if [ "$1" == "7" ]; then
python ttH-multilepton/ttH_plots.py ../../macros/diff/diff_2lss_v6_plots 201$1 2lss_diff_$2 -p ttH,tHW,TTWW,TTW,TTZ,WZ,ZZ,Rares,tttt,tZq,TT,DY,WJets,SingleTop,WW,Flips,Convs
fi
if [ "$1" == "8" ]; then
python ttH-multilepton/ttH_plots.py ../../macros/diff/diff_2lss_v6_plots 201$1 2lss_diff_$2 -p ttH,TTWW,TTW,TTZ,WZ,ZZ,Rares,tttt,tZq,TT,DY,WJets,SingleTop,WW,Flips,Convs
fi
