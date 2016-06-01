#!/bin/bash

##workingDir="$PWD"
workingDir="/afs/cern.ch/work/d/dalfonso/CMSSW_7_6_3_patch2_Maryam/src/CMGTools/ObjectStudies/cfg/"

echo $workingDir

cd ../../TTHAnalysis/python/plotter 
python mcPlots.py $workingDir/plotDiJet/plots_list_mca.txt $workingDir/plotDiJet/plots_list_cuts.txt $workingDir/plotDiJet/plots_list_plots.txt --s2v --tree METtree -P $workingDir --pdir $workingDir/plotDiJet/plots/ -l 1 --rebin=1 --plotmode=nostack
#-j 8
