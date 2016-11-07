T="/mnt/t3nfs01/data01/shome/cheidegg/o/2016-07-13_ewkskims80X"
F="--accept TChiNeuSlepSneu_TD -q all.q --direct --nosplit" #"-F" 

#python susy-interface/friendmaker.py 3l 3lA $T $T --bk --log $F --modules leptonJetReCleanerSusyEWK3L --pretend
#python susy-interface/friendmaker.py 3l 3lA $T $T --bk --log $F --modules leptonBuilderEWK
#python susy-interface/friendmaker.py 3l 3lA $T $T --bk --log $F --modules eventBTagWeight             --pretend


T="/mnt/t3nfs01/data01/shome/cheidegg/o/2016-10-04_leptonMVAtraining/trees_80X/"
F="-q all.q --direct" #"-F" 
python susy-interface/friendmaker.py 3l 3lA $T $T --bk --log $F --modules mvaSUSY_80X_TTH_simple 

