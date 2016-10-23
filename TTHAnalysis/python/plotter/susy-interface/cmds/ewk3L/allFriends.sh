T="/mnt/t3nfs01/data01/shome/cheidegg/o/2016-07-13_ewkskims80X"
F="" #"-F" 

python susy-interface/friendmaker.py 3l 3lA $T $T --bk --log $F --modules leptonJetReCleanerSusyEWK3L --pretend
python susy-interface/friendmaker.py 3l 3lA $T $T --bk --log $F --modules leptonBuilderEWK            --pretend
python susy-interface/friendmaker.py 3l 3lA $T $T --bk --log $F --modules eventBTagWeight             --pretend



