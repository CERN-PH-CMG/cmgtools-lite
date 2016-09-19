
## python susy-interface/plotmaker.py 3l 3lA /mnt/t3nfs01/data01/shome/cheidegg/o/2016-07-13_ewkskims80X /mnt/t3nfs01/data01/shome/cheidegg/o/2016-07-30_ewk80X_plots_12p9_final -l 12.9 -q all.q --make data --plots all -o SR --flags '-X blinding'

## python susy-interface/effmaker.py 3l 3lA /mnt/t3nfs01/data01/shome/cheidegg/o/2016-07-13_ewkskims80X /mnt/t3nfs01/data01/shome/cheidegg/o/interfaceTest/effs/new -l 12.9 -o SR --flags '-X blinding'

## python susy-interface/skimmaker.py 3l 3lA /mnt/t3nfs01/data01/shome/cheidegg/o/2016-07-13_ewkskims80X /mnt/t3nfs01/data01/shome/cheidegg/o/superTestSkim --samples MuonEG_Run2016C_PromptReco_v2_runs_271350_275783 -X blinding -X filters -X trigger -X SRevent -X veto -X convveto -X met 

#python susy-interface/limitmaker.py 3l 3lA /mnt/t3nfs01/data01/shome/cheidegg/o/2016-07-13_ewkskims80X /mnt/t3nfs01/data01/shome/cheidegg/o/interfaceTest/lims/new -l 12.9 -o SR --flags '-X blinding --asimov' --sigs TChiNeuWZ_mCh350_mChi20 --pretend

#python susy-interface/dumpmaker.py 3l 3lA /mnt/t3nfs01/data01/shome/cheidegg/o/2016-07-13_ewkskims80X /mnt/t3nfs01/data01/shome/cheidegg/o/interfaceTest/dumps/new -o SR --flags '-X blinding' --pretend 

#python susy-interface/effmaker.py 3l 3lA /mnt/t3nfs01/data01/shome/cheidegg/o/2016-07-13_ewkskims80X /mnt/t3nfs01/data01/shome/cheidegg/o/interfaceTest/effs/new -l 12.9 -o SR --flags '-X blinding' --pretend
#python susy-interface/effmaker.py 3l 3lA /mnt/t3nfs01/data01/shome/cheidegg/o/2016-07-13_ewkskims80X /mnt/t3nfs01/data01/shome/cheidegg/o/interfaceTest/effsPB/new -l 12.9 -o SR --flags '-X blinding' --perBin --pretend



