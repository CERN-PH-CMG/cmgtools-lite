#!/bin/bash

ANALYZER=../../mcAnalysis.py
PLOTTER=../../mcPlots.py

#TREESPATH=/afs/cern.ch/user/i/igsuarez/work/public/trees80X_809June9/
TREESPATH=/pool/ciencias/HeppyTrees/RA7/pietro/friendTrees/trees80X_809June9/
TREE=treeProducerSusyMultilepton

FT_LJCLEANER=leptonJetReCleanerSusyRA7mva
FT_LJCLEANER=leptonJetReCleanerSusySSDL_M

FT_LCHOICE=leptonChoiceEWK

LCHOICE="--Fs ${TREESPATH}${FT_LCHOICE}"
LCHOICE=""

MCA=regions_mca.txt
CUTS=regions_cuts.txt
MCCTRIGDEF=mcc_susy_2lssinc_triggerdefs.txt
MCCCUTSDEF=regions_cutsdef.txt

PLOTS=regions_plots.txt

PLOTSDIR=~/www/susyRA7/

NPROC=8

LUMI=4.0

if [ "${1}" = "anal" ]; then

    # final only -f
    python ${ANALYZER} ${MCA} ${CUTS} -G --path ${TREESPATH} --tree ${TREE}  --lumi ${LUMI} --s2v -j ${NPROC} --Fs ${TREESPATH}${FT_LJCLEANER} ${LCHOICE} --mcc ${MCCTRIGDEF} --mcc ${MCCCUTSDEF}  

elif [ "${1}" = "plot" ]; then                                                                                                                          
    rm -r ${PLOTSDIR}baseline/
    mkdir -p ${PLOTSDIR}baseline/

    cp ${PLOTSDIR}index.php ${PLOTSDIR}
    cp ${PLOTSDIR}index.php ${PLOTSDIR}baseline/
    #--exclude-process data
    python ${PLOTTER}  ${MCA} ${CUTS} ${PLOTS} --path ${TREESPATH} --AP --tree ${TREE} --lumi ${LUMI} --s2v -j ${NPROC} --Fs ${TREESPATH}${FT_LJCLEANER} ${LCHOICE} --mcc ${MCCTRIGDEF} --mcc ${MCCCUTSDEF} --rspam "%(lumi) (13 TeV)" --lspam "#bf{CMS} #it{Preliminary}" --legendBorder=0 --legendFontSize 0.055 --legendWidth=0.30 --showMCError --pdir ${PLOTSDIR}baseline/



fi


exit 0