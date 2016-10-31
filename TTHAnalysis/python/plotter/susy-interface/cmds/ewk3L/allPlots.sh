#!/bin/bash

T="/mnt/t3nfs01/data01/shome/cheidegg/o/2016-07-13_ewkskims80X"
O="$ODIR/2016-09-07_fullTest/plots"
PLOTS="perCateg"
QUEUE="--pretend" #"-q all.q"

python susy-interface/plotmaker.py 3l 3lA $T $O -l 12.9 --make data --plots $PLOTS -o SR --flags '-X blinding --perBin' $QUEUE
#python susy-interface/plotmaker.py 3l 3lB $T $O -l 12.9 --make data --plots $PLOTS -o SR --flags '-X blinding --perBin' $QUEUE
#python susy-interface/plotmaker.py 3l 3lC $T $O -l 12.9 --make data --plots $PLOTS -o SR --flags '-X blinding --perBin' $QUEUE
#python susy-interface/plotmaker.py 3l 3lD $T $O -l 12.9 --make data --plots $PLOTS -o SR --flags '-X blinding --perBin' $QUEUE
#python susy-interface/plotmaker.py 3l 3lE $T $O -l 12.9 --make data --plots $PLOTS -o SR --flags '-X blinding --perBin' $QUEUE
#python susy-interface/plotmaker.py 3l 3lF $T $O -l 12.9 --make data --plots $PLOTS -o SR --flags '-X blinding --perBin' $QUEUE
#python susy-interface/plotmaker.py 3l 4lG $T $O -l 12.9 --make data --plots $PLOTS -o SR --flags '-X blinding --perBin' $QUEUE --mccs susy-ewkino/4l/mcc_ewkino.txt
#python susy-interface/plotmaker.py 3l 4lH $T $O -l 12.9 --make data --plots $PLOTS -o SR --flags '-X blinding --perBin' $QUEUE --mccs susy-ewkino/4l/mcc_ewkino.txt
#python susy-interface/plotmaker.py 3l 4lI $T $O -l 12.9 --make data --plots $PLOTS -o SR --flags '-X blinding --perBin' $QUEUE --mccs susy-ewkino/4l/mcc_ewkino.txt

