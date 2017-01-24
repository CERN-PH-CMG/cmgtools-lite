#T="/mnt/t3nfs01/data01/shome/cheidegg/o/2016-11-06_ewk80X_signalssplit/DONE"
T="/mnt/t3nfs01/data01/shome/cheidegg/o/2016-07-13_ewkskims80X"
F="--accept TChiNeuH -q all.q --direct --nosplit" #"-F" 

#python susy-interface/friendmaker.py 3l 3lA $T $T --bk --log $F --modules leptonJetReCleanerSusyEWK3L
python susy-interface/friendmaker.py 3l 3lA $T $T --bk --log $F --modules leptonBuilderEWK
#python susy-interface/friendmaker.py 3l 3lA $T $T --bk --log $F --modules eventBTagWeight             --pretend


#T="/mnt/t3nfs01/data01/shome/cheidegg/o/2016-10-04_leptonMVAtraining/trees_80X/"
#F="-q all.q --direct" #"-F" 
#python susy-interface/friendmaker.py 3l 3lA $T $T --bk --log $F --modules mvaSUSY_80X_TTZ_decoupleAndBTagCut
