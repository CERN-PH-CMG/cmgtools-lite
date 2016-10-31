
IN="/mnt/t3nfs01/data01/shome/cheidegg/o/2016-07-13_ewkskims80X"
OUT="/mnt/t3nfs01/data01/shome/cheidegg/o/2016-07-13_ewkskims80X_fancyPancySkimsy"
SAMPLES="--allSamples" ## or add them with --samples, or put --procs data

python susy-interface/skimmaker.py 3l 3lA $T $O $SAMPLES -X blinding -X filters -X trigger -X SRevent -X veto -X convveto -X met 

