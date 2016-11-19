#!/bin/bash

T="/afs/cern.ch/user/f/folguera/workdir/trees/ewkino/TREES_76X_160526/"
J=12;

if [[ "X$1" == "X" ]]; then echo "Provide output directory name!"; exit; fi
OUTNAME=$1; shift;
if [[ "X$1" == "X" ]]; then echo "Provide luminosity!"; exit; fi
LUMI="$1"; shift
echo "Normalizing to ${LUMI}/fb";
OPTIONS=" --asimov -P $T --tree treeProducerSusyMultilepton --s2v -j $J -l ${LUMI} -f "
test -d cards/$OUTNAME || mkdir -p cards/$OUTNAME
OPTIONS="${OPTIONS} --od cards/160606/$OUTNAME ";

SYSTS="susy-ewkino/syst_dummy.txt"
SPLITDECAYS=""
#SPLITDECAYS="-splitdecays"

#OPTIONS="${OPTIONS} --Fs  {P}/3_recleaner_cbId "
OPTIONS="${OPTIONS} --Fs  {P}/3_recleaner_MVAT_FO "
OPTIONS="${OPTIONS} --mcc susy-ewkino/2lss/lepchoice-ss2l-FO.txt --mcc susy-ewkino/mcc_triggerdefs.txt --neg" # neg necessary for subsequent rebin
CATPOSTFIX=""

FUNCTION_2L="SR_ewk_ss2l(nJet40,LepGood1_pt,LepGood1_phi,LepGood2_pt,LepGood2_phi,met_pt,met_phi) 18,0.5,18.5"
#FUNCTION_2L="SR_ewk_ss2l(nJet40,LepGood1_pt,LepGood1_phi,LepGood2_pt,LepGood2_phi,met_pt,met_phi) 12,0.5,12.5"

if [[ "$1" == "ss2l" ]]; then
    OPT_2L="${OPTIONS} -E sr -E tightMVAVT"
#    OPT_2L="${OPTIONS} -E sr"
    
    echo "making cards for ss2l with following command: "
    echo python makeShapeCardsSusy.py susy-ewkino/2lss/mca-ss2l-mc${SPLITDECAYS}.txt susy-ewkino/2lss/susy_ss2l_cuts.txt $FUNCTION_2L $SYSTS $OPT_2L -o ss2l ; 
    python makeShapeCardsSusy.py susy-ewkino/2lss/mca-ss2l-mc${SPLITDECAYS}.txt susy-ewkino/2lss/susy_ss2l_cuts.txt $FUNCTION_2L $SYSTS $OPT_2L -o ss2l ; 
    echo "Done at $(date)"
fi
