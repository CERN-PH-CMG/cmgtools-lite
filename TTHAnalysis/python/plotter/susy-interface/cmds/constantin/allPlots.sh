#!/bin/bash

T="/mnt/t3nfs01/data01/shome/cheidegg/o/2016-07-13_ewkskims80X"
O="/mnt/t3nfs01/data01/shome/cheidegg/o/2016-10-19_ewk80X_plotsForDominick"
#O="$ODIR/2016-10-14_ewk80X_allPlotsWithTauSF"
PLOTS="perCateg"
QUEUE="--pretend" #"-q all.q"

#python susy-interface/plotmaker.py 3l "3lA;3lB;3lC;3lD;3lE;3lF" $T $O -l 12.9 --make data --plots $PLOTS -o SR --flags '-X blinding --perBin' $QUEUE
#python susy-interface/plotmaker.py 3l "4lG;4lH;4lI" $T $O -l 12.9 --make data --plots $PLOTS -o SR --flags '-X blinding --perBin' $QUEUE --mccs susy-ewkino/4l/mcc_ewkino.txt
#python susy-interface/plotmaker.py 3l "4lI" $T $O -l 12.9 --make data --plots $PLOTS -o SR --flags '-X blinding --perBin --cmsprel ""' $QUEUE --mccs susy-ewkino/4l/mcc_ewkino.txt

#python susy-interface/plotmaker.py 3l 3lA $T $O -l 12.9 --make mix --plots dominick -o SR --flags '-X blinding --perBin' $QUEUE --bkgs "fakes_matched_.*;prompt_.*;rares_.*;convs"  --sigs "TChiNeuWZ_200_100;TChiNeuWZ_150_120;TChiNeuWZ_400_1" --flags '--plotgroup fakes_matched_DY+=fakes_matched_WW --plotgroup fakes_matched_DY+=fakes_matched_WJ --plotgroup fakes_matched_DY+=fakes_matched_TT --plotgroup fakes_matched_DY+=fakes_matched_ST'
python susy-interface/plotmaker.py 3l 3lF $T $O -l 12.9 --make mix --plots dominick -o SR --flags '-X blinding --perBin' $QUEUE --bkgs "fakes_matched_.*;prompt_.*;rares_.*;convs"  --sigs "TChiNeuSlepSneuTD_200_100;TChiNeuSlepSneuTD_400_1" --flags '--plotgroup fakes_matched_DY+=fakes_matched_WW --plotgroup fakes_matched_DY+=fakes_matched_WJ --plotgroup fakes_matched_DY+=fakes_matched_TT --plotgroup fakes_matched_DY+=fakes_matched_ST'
