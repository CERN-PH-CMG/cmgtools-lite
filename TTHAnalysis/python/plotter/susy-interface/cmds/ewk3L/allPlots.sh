#!/bin/bash

T="/mnt/t3nfs01/data01/shome/cheidegg/o/2016-07-13_ewkskims80X"
O="/afs/cern.ch/user/c/cheidegg/www/heppy/2016-11-14_ewk80X_35fb_expectedYields"
PLOTS="perCateg"
QUEUE="" #"-q all.q"

## data plots
#python susy-interface/plotmaker.py 3l "3lA;3lB;3lC;3lD;3lE;3lF" $T $O -l 12.9 --make data --plots $PLOTS -o SR --flags '-X blinding --perBin' $QUEUE
#python susy-interface/plotmaker.py 3l "4lG;4lH;4lI;4lJ;4lK" $T $O -l 12.9 --make data --plots $PLOTS -o SR --flags '-X blinding --perBin' $QUEUE --mccs susy-ewkino/4l/mcc_ewkino.txt

## expected yields
python susy-interface/plotmaker.py 3l 3lA $T $O -l 35 --make mix --plots $PLOTS -o SR --flags '-X blinding --perBin --plotgroup fakes_matched_DY+=fakes_matched_WW --plotgroup fakes_matched_DY+=fakes_matched_WJ --plotgroup fakes_matched_DY+=fakes_matched_TT --plotgroup fakes_matched_DY+=fakes_matched_ST' -p "fakes_matched_.*;prompt_.*;rares_.*;convs" -p "sig_TChiNeuSlepSneuFD_1100_1;sig_TChiNeuSlepSneuFD_500_475" $QUEUE
#python susy-interface/plotmaker.py 3l "3lB;3lC;3lD;3lE;3lF" $T $O -l 35 --make mix --plots $PLOTS -o SR --flags '-X blinding --perBin --plotgroup fakes_matched_DY+=fakes_matched_WW --plotgroup fakes_matched_DY+=fakes_matched_WJ --plotgroup fakes_matched_DY+=fakes_matched_TT --plotgroup fakes_matched_DY+=fakes_matched_ST' -p "fakes_matched_.*;prompt_.*;rares_.*;convs" -p "sig_TChiNeuSlepSneuTD_500_1;sig_TChiNeuSlepSneuTD_200_150" $QUEUE
#python susy-interface/plotmaker.py 3l "4lG;4lH;4lI;4lJ;4lK" $T $O -l 35 --make mix --plots $PLOTS -o SR --flags '-X blinding --perBin --plotgroup fakes_matched_DY+=fakes_matched_WW --plotgroup fakes_matched_DY+=fakes_matched_WJ --plotgroup fakes_matched_DY+=fakes_matched_TT --plotgroup fakes_matched_DY+=fakes_matched_ST' -p "fakes_matched_.*;prompt_.*;rares_.*;convs" -p "sig_TChiNeuZZ4L_400_1;sig_TChiNeuHZ_400_1;sig_TChiNeuHH_400_1" --mccs susy-ewkino/4l/mcc_ewkino.txt $QUEUE

