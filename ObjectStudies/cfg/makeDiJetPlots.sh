#!/bin/bash

##workingDir="$PWD"
workingDir="/afs/cern.ch/work/d/dalfonso/CMSSW_8_0_5_LPCp/src/CMGTools/ObjectStudies/cfg/"
echo $workingDir

weightPU=" -L $workingDir/../python/plotter/vtxReweight.cc -W puDiJet(nVert) "
BCORE="--s2v --tree METtree $workingDir/plotDiJet/plots_listMC_mca.txt $workingDir/plotDiJet/plots_list_cuts.txt"

cd ../../TTHAnalysis/python/plotter

##===> this make DATA overlayed STACK
python mcPlots.py --s2v --tree METtree $workingDir/plotDiJet/plots_list_mca.txt $workingDir/plotDiJet/plots_list_cuts.txt $workingDir/plotDiJet/plots_list_plots.txt -P $workingDir --pdir $workingDir/plotDiJet/plots/ -l 0.8 --rebin=1 --plotmode=nostack

##===> this make MC STACK
#python mcPlots.py $BCORE $weightPU $workingDir/plotDiJet/plots_list_plots.txt -P $workingDir --pdir $workingDir/plotDiJet/plots/ -l 0.8 --rebin=1 --showRatio --maxRatioRange 0. 2.
#-j 8

exit

PBASE=$workingDir"plotDiJet/plots/VTX"

python mcPlots.py $BCORE $workingDir/plotDiJet/nvtx_plots.txt -P $workingDir -l 0.8 --rebin=1 --pdir $PBASE --sP nvtx
#"echo; echo; ";
python ../tools/vertexWeightFriend.py no $PBASE/nvtx_plots.root;
#echo ' ---- Now you should put the normalization and weight into vtxReweight.cc defining a puDiJet ----- ';