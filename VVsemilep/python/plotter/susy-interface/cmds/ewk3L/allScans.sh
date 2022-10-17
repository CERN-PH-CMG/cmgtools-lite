#!/bin/bash

## IMPORTANT REMARK: In principle, one could run all models per config/region all together,
## but this will generate a lot of jobs which are all accessing the same background ROOT file.
## This kills memory and performance. Keep in mind to split as good and effective as possible
## to optimize performance.

T="/mnt/t3nfs01/data01/shome/cheidegg/o/2016-07-13_ewkskims80X"
#O="/mnt/t3nfs01/data01/shome/cheidegg/o/2016-10-14_ewk80X_allCardsNoTauSF"
O="/mnt/t3nfs01/data01/shome/cheidegg/o/2016-10-14_ewk80X_allCardsWithTauSFwithFS"
#QUEUE="--pretend" #"-q all.q"
QUEUE="-q all.q" #"-q all.q"
#QUEUE="-q all.q@t3wn20.psi.ch all.q@t3wn22.psi.ch all.q@t3wn26.psi.ch all.q@t3wn21.psi.ch all.q@t3wn10.psi.ch"
#QUEUE="-q all.q@t3wn20.psi.ch all.q@t3wn22.psi.ch all.q@t3wn26.psi.ch all.q@t3wn21.psi.ch all.q@t3wn10.psi.ch all.q@t3wn16.psi.ch all.q@t3wn17.psi.ch all.q@t3wn29.psi.ch all.q@t3wn11.psi.ch all.q@t3wn36.psi.ch all.q@t3wn13.psi.ch all.q@t3wn14.psi.ch all.q@t3wn25.psi.ch all.q@t3wn37.psi.ch all.q@t3wn40.psi.ch all.q@t3wn35.psi.ch all.q@t3wn27.psi.ch all.q@t3wn38.psi.ch all.q@t3wn33.psi.ch all.q@t3wn31.psi.ch all.q@t3wn39.psi.ch all.q@t3wn32.psi.ch"

#QUEUE="--pretend"

## background only first
#python susy-interface/scanmaker.py crwz crwz $T $O -l 12.9 -o SR --models TChiNeuWZ --bkgOnly --redoBkg --flags '-X blinding' $QUEUE 
#python susy-interface/scanmaker.py 3l "3lA1;3lA2;3lB;3lC;3lD;3lE;3lF" $T $O -l 12.9 -o SR --models TChiNeuWZ --bkgOnly --redoBkg --flags '-X blinding' --mca susy-ewkino/3l/mca_ewkino_forScan.txt $QUEUE 

## TChiNeuWH
#python susy-interface/scanmaker.py crwz crwz $T $O -l 12.9 -o SR --models TChiNeuWH --flags '-X blinding' --sigOnly $QUEUE
#python susy-interface/scanmaker.py 3l "3lA1;3lA2;3lB" $T $O -l 12.9 -o SR --models TChiNeuWH --mca susy-ewkino/3l/mca_ewkino_forScan.txt --flags '-X blinding' --sigOnly $QUEUE
#python susy-interface/scanmaker.py 3l "3lC;3lD;3lE;3lF" $T $O -l 12.9 -o SR --models TChiNeuWH --mca susy-ewkino/3l/mca_ewkino_forScan.txt --flags '-X blinding' --sigOnly $QUEUE

## TChiNeuWZ
#python susy-interface/scanmaker.py crwz crwz $T $O -l 12.9 -o SR --models TChiNeuWZ --flags '-X blinding' --sigOnly $QUEUE
#python susy-interface/scanmaker.py 3l "3lA1;3lA2" $T $O -l 12.9 -o SR --models TChiNeuWZ --mca susy-ewkino/3l/mca_ewkino_forScan.txt --flags '-X blinding' --sigOnly $QUEUE

## TChiNeuSlepSneu_FD
#python susy-interface/scanmaker.py crwz crwz $T $O -l 12.9 -o SR --models TChiNeuSlepSneu_FD --flags '-X blinding' --sigOnly $QUEUE
#python susy-interface/scanmaker.py 3l "3lA1;3lA2" $T $O -l 12.9 -o SR --models TChiNeuSlepSneu_FD --mca susy-ewkino/3l/mca_ewkino_forScan.txt --flags '-X blinding' --sigOnly $QUEUE

## TChiNeuSlepSneu_05
#python susy-interface/scanmaker.py crwz crwz $T $O -l 12.9 -o SR --models TChiNeuSlepSneu_05 --flags '-X blinding' --sigOnly $QUEUE
#python susy-interface/scanmaker.py 3l "3lA1;3lA2" $T $O -l 12.9 -o SR --models TChiNeuSlepSneu_05 --mca susy-ewkino/3l/mca_ewkino_forScan.txt --flags '-X blinding' --sigOnly $QUEUE

## TChiNeuSlepSneu_TD
python susy-interface/scanmaker.py crwz crwz $T $O -l 12.9 -o SR --models TChiNeuSlepSneu_TD --flags '-X blinding' --sigOnly $QUEUE
python susy-interface/scanmaker.py 3l "3lB;3lD;3lE;3lF" $T $O -l 12.9 -o SR --models TChiNeuSlepSneu_TD --mca susy-ewkino/3l/mca_ewkino_forScan.txt --flags '-X blinding' --sigOnly $QUEUE




