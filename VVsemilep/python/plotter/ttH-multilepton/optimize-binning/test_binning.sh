#!/bin/bash
rm cards/scenarioTest/ttH* cards/scenarioTest/combined*
eval `scramv1 runtime -sh` 
bash ttH-multilepton/make_cards.sh scenarioTest 2.26 3l $1 $2 $3
cd cards/scenarioTest
cd /afs/cern.ch/work/p/peruzzi/cmgtools/combine/CMSSW_7_4_14
eval `scramv1 runtime -sh` 
cd -
combineCards.py ttH*3l*card.txt > combined.card.txt
text2workspace.py combined.card.txt -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel  --PO 'map=.*/ttH.*:r_ttH[1,-2,6]' --PO 'map=.*/TTW:r_ttV[1,0,6]' --PO 'map=.*/TTZ:r_ttV[1,0,6]'
combine -n `echo ${1}${2}${3} | sed "s/\-/m/g" | sed "s/\.//g"` -M MultiDimFit combined.card.root --algo=singles -P r_ttH --floatOtherPOIs=1
cd ../..
eval `scramv1 runtime -sh` 
