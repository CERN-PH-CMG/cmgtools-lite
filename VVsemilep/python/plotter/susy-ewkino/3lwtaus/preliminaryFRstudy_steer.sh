#!/bin/bash

ANALYZER=../../mcAnalysis.py
PLOTTER=../../mcPlots.py

TREESPATH=/afs/cern.ch/user/i/igsuarez/work/public/trees80X_809June9/
TREE=treeProducerSusyMultilepton

FT_LJCLEANER=leptonJetReCleanerSusyRA7mva
FT_LJCLEANER=leptonJetReCleanerSusySSDL_M

FT_LCHOICE=leptonChoiceEWK

LCHOICE="--Fs ${TREESPATH}${FT_LCHOICE}"
LCHOICE=""

MCA=preliminaryFRstudy_mca.txt
CUTS=preliminaryFRstudy_cuts.txt
MCC=mcc_susy_2lssinc_triggerdefs.txt

PLOTS=preliminaryFRstudy_plots.txt

PLOTSDIR=~/www/susyRA7/

NPROC=8

LUMI=10.0


if [ "${1}" = "anal" ]; then

    python ${ANALYZER} ${MCA} ${CUTS} --path ${TREESPATH} --tree ${TREE}  --lumi ${LUMI} --s2v -j ${NPROC} --Fs ${TREESPATH}${FT_LJCLEANER} ${LCHOICE} --mcc ${MCC} -f -G

elif [ "${1}" = "plot" ]; then

    rm -r ${PLOTSDIR}TT/
    rm -r ${PLOTSDIR}DY/
    rm -r ${PLOTSDIR}data/
    
    mkdir -p ${PLOTSDIR}TT/
    mkdir -p ${PLOTSDIR}DY/
    mkdir -p ${PLOTSDIR}data/

    cp ${PLOTSDIR}index.php ${PLOTSDIR}
    cp ${PLOTSDIR}index.php ${PLOTSDIR}TT/
    cp ${PLOTSDIR}index.php ${PLOTSDIR}DY/
    cp ${PLOTSDIR}index.php ${PLOTSDIR}data/
    
    # TT
    python ${PLOTTER} --exclude-process data --exclude-process DY ${MCA} ${CUTS} ${PLOTS} --path ${TREESPATH} --tree ${TREE} --lumi ${LUMI} --s2v -j ${NPROC} --Fs ${TREESPATH}${FT_LJCLEANER} ${LCHOICE} --mcc ${MCC} --rspam "%(lumi) (13 TeV)" --lspam "#bf{CMS} #it{Preliminary}" --legendBorder=0 --legendFontSize 0.055 --legendWidth=0.30 --showMCError --pdir ${PLOTSDIR}TT/ &

    # DY
    python ${PLOTTER} --exclude-process data --exclude-process TT ${MCA} ${CUTS} ${PLOTS} --path ${TREESPATH} --tree ${TREE} --lumi ${LUMI} --s2v -j ${NPROC} --Fs ${TREESPATH}${FT_LJCLEANER} ${LCHOICE} --mcc ${MCC} --rspam "%(lumi) (13 TeV)" --lspam "#bf{CMS} #it{Preliminary}" --legendBorder=0 --legendFontSize 0.055 --legendWidth=0.30 --showMCError --pdir ${PLOTSDIR}DY/ &

    # Data
    python ${PLOTTER} --exclude-process TT --exclude-process DY ${MCA} ${CUTS} ${PLOTS} --path ${TREESPATH} --tree ${TREE} --lumi ${LUMI} --s2v -j ${NPROC} --Fs ${TREESPATH}${FT_LJCLEANER} ${LCHOICE} --mcc ${MCC} --rspam "%(lumi) (13 TeV)" --lspam "#bf{CMS} #it{Preliminary}" --legendBorder=0 --legendFontSize 0.055 --legendWidth=0.30 --showMCError --pdir ${PLOTSDIR}data/ &


fi


exit 0