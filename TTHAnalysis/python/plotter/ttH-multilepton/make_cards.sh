#!/bin/bash

if [[ "$HOSTNAME" == "cmsco01.cern.ch" ]]; then
    T="/data1/peruzzi/TREES_76X_150216_noLHE_jecV1_noJecUnc_skim_reclv8"; echo "NOT OK for flips in data";
    J=8;
else
    T="/afs/cern.ch/work/p/peruzzi/tthtrees/TREES_76X_150216_noLHE_jecV1_noJecUnc";
    J=4;
fi

SCENARIO=""
if echo "X$1" | grep -q "scenario"; then SCENARIO="$1"; shift; fi
if [[ "X$1" == "X" ]]; then echo "Provide luminosity!"; exit; fi
LUMI="$1"; shift
echo "Normalizing to ${LUMI}/fb";
OPTIONS=" -P $T --tree treeProducerSusyMultilepton --s2v -j $J -l ${LUMI} -f --asimov "
#OPTIONS="${OPTIONS} --neg " # to be checked!!!
echo 'WARNING: check usage of --neg!!!'
if [[ "$SCENARIO" != "" ]]; then
    test -d cards/$SCENARIO || mkdir -p cards/$SCENARIO
    OPTIONS="${OPTIONS} --od cards/$SCENARIO --project $SCENARIO ";
else
    OPTIONS="${OPTIONS} --od cards/new ";
fi
SYSTS="ttH-multilepton/systsEnv_dummy.txt"
echo "DUMMY SYSTEMATICS!!!"
#SYSTS="ttH-multilepton/systsEnv.txt ../../macros/systematics/btagSysts2.txt"
BLoose=" -E BLoose "
BTight=" -E BTight "
ZeroTau=" -E 0tau "
OneTau=" -E 1tau "

OPTIONS="${OPTIONS} --Fs {P}/2_recleaner_v8_b1E2_approx --Fs {P}/4_kinMVA_74XtrainingMilosJan31_v3_reclv8"
OPTIONS="${OPTIONS} --mcc ttH-multilepton/lepchoice-ttH-FO.txt --mcc ttH-multilepton/ttH_2lss3l_triggerdefs.txt -W puw(nTrueInt)"
OPTIONS="${OPTIONS} --asimov --xp data --xp '.*data.*'" # safety!


FUNCTION_2L="kinMVA_2lss_ttV:kinMVA_2lss_ttbar 20,-1,1,20,-1,1"
FUNCTION_3L="kinMVA_3l_ttV:kinMVA_3l_ttbar 20,-1,1,20,-1,1"

if [[ "$1" == "" || "$1" == "2lss" ]]; then
    OPT_2L="${OPTIONS} "

    POS=" -A alwaystrue positive LepGood1_charge>0 "
    NEG=" -A alwaystrue negative LepGood1_charge<0 "

    for X in mm ee em; do 
        echo "2lss_${X}";
	FLAV=" -E ${X} "
	if [[ "${X}" == "mm" ]]; then Y="mumu"; else Y=${X}; fi
	if [[ "${X}" == "ee" ]]; then
	    python makeShapeCards.py --2d-binning-function 6:ttH_MVAto1D_6_2lss_Marco ttH-multilepton/mca-2lss-mc.txt ttH-multilepton/2lss_tight.txt ${FUNCTION_2L} $SYSTS $OPT_2L -o 2lss_${Y}_0tau_BCat_MVA_pos $POS $FLAV $ZeroTau;
            python makeShapeCards.py --2d-binning-function 6:ttH_MVAto1D_6_2lss_Marco ttH-multilepton/mca-2lss-mc.txt ttH-multilepton/2lss_tight.txt ${FUNCTION_2L} $SYSTS $OPT_2L -o 2lss_${Y}_0tau_BCat_MVA_neg $NEG $FLAV $ZeroTau;
	else
	    python makeShapeCards.py --2d-binning-function 6:ttH_MVAto1D_6_2lss_Marco ttH-multilepton/mca-2lss-mc.txt ttH-multilepton/2lss_tight.txt ${FUNCTION_2L} $SYSTS $OPT_2L -o 2lss_${Y}_0tau_bl_BCat_MVA_pos $POS $BLoose $FLAV $ZeroTau;
            python makeShapeCards.py --2d-binning-function 6:ttH_MVAto1D_6_2lss_Marco ttH-multilepton/mca-2lss-mc.txt ttH-multilepton/2lss_tight.txt ${FUNCTION_2L} $SYSTS $OPT_2L -o 2lss_${Y}_0tau_bl_BCat_MVA_neg $NEG $BLoose $FLAV $ZeroTau;
            python makeShapeCards.py --2d-binning-function 6:ttH_MVAto1D_6_2lss_Marco ttH-multilepton/mca-2lss-mc.txt ttH-multilepton/2lss_tight.txt ${FUNCTION_2L} $SYSTS $OPT_2L -o 2lss_${Y}_0tau_bt_BCat_MVA_pos $POS $BTight $FLAV $ZeroTau;
            python makeShapeCards.py --2d-binning-function 6:ttH_MVAto1D_6_2lss_Marco ttH-multilepton/mca-2lss-mc.txt ttH-multilepton/2lss_tight.txt ${FUNCTION_2L} $SYSTS $OPT_2L -o 2lss_${Y}_0tau_bt_BCat_MVA_neg $NEG $BTight $FLAV $ZeroTau;
	fi
    done

    python makeShapeCards.py ttH-multilepton/mca-2lss-mc.txt ttH-multilepton/2lss_tight.txt ${FUNCTION_2L} $SYSTS $OPT_2L -o 2lss_1tau_BCat_MVA $OneTau;

    echo "Done at $(date)"

fi

if [[ "$1" == "" || "$1" == "3l" ]]; then
    OPT_3L="${OPTIONS} "
    POS=" -A alwaystrue positive (LepGood1_charge+LepGood2_charge+LepGood3_charge)>0 "
    NEG=" -A alwaystrue negative (LepGood1_charge+LepGood2_charge+LepGood3_charge)<0 "
    echo "3l";
    python makeShapeCards.py --2d-binning-function 3:ttH_MVAto1D_3_3l_Marco ttH-multilepton/mca-3l-mc.txt ttH-multilepton/3l_tight.txt ${FUNCTION_3L} $SYSTS $OPT_3L -o 3lBCat_bl_MVA_pos $POS $BLoose;
    python makeShapeCards.py --2d-binning-function 3:ttH_MVAto1D_3_3l_Marco ttH-multilepton/mca-3l-mc.txt ttH-multilepton/3l_tight.txt ${FUNCTION_3L} $SYSTS $OPT_3L -o 3lBCat_bl_MVA_neg $NEG $BLoose;
    python makeShapeCards.py --2d-binning-function 3:ttH_MVAto1D_3_3l_Marco ttH-multilepton/mca-3l-mc.txt ttH-multilepton/3l_tight.txt ${FUNCTION_3L} $SYSTS $OPT_3L -o 3lBCat_bt_MVA_pos $POS $BTight;
    python makeShapeCards.py --2d-binning-function 3:ttH_MVAto1D_3_3l_Marco ttH-multilepton/mca-3l-mc.txt ttH-multilepton/3l_tight.txt ${FUNCTION_3L} $SYSTS $OPT_3L -o 3lBCat_bt_MVA_neg $NEG $BTight;

   echo "Done at $(date)"
fi

