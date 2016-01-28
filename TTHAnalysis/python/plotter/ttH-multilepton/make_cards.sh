#!/bin/bash

if [[ "$HOSTNAME" == "cmsphys10" ]]; then
    T="/data1/p/peruzzi/TREES_74X_140116_MiniIso_tauClean_Mor16lepMVA";
    J=8;
else
    T="/afs/cern.ch/work/p/peruzzi/tthtrees/TREES_74X_140116_MiniIso_tauClean_Mor16lepMVA";
    J=4;
fi

SCENARIO=""
if echo "X$1" | grep -q "scenario"; then SCENARIO="$1"; shift; fi
if [[ "X$1" == "X" ]]; then echo "Provide luminosity!"; exit; fi
LUMI="$1"; shift
OPTIONS=" -P $T -j $J -l ${LUMI} -f  --od cards/new --asimov "
if [[ "$SCENARIO" != "" ]]; then
    test -d cards/$SCENARIO || mkdir -p cards/$SCENARIO
    OPTIONS=" -P $T -j $J -l ${LUMI} -f  --od cards/$SCENARIO --project $SCENARIO --asimov ";
fi
SYSTS="ttH-multilepton/systsEnv.txt"
BLoose=" -E BLoose "
BTight=" -E BTight "
ZeroTau=" -E 0tau "
OneTau=" -E 1tau "

OPTIONS="${OPTIONS} --Fs {P}/2_recleaner_v4_vetoCSVM --Fs {P}/2_recleaner_v4_vetoCSVM "
OPTIONS="${OPTIONS} --asimov --xp data --xp '.*data.*'" # safety!

if [[ "$1" == "" || "$1" == "2lss" ]]; then
    OPT_2L="${OPTIONS} "

    POS=" -A alwaystrue positive LepGood1_charge>0 "
    NEG=" -A alwaystrue negative LepGood1_charge<0 "
    for X in 2lss_{mm,ee,em}; do 
        echo $X;
	FLAV=" -E ${X} "
	python makeShapeCards.py ttH-multilepton/mca-2lss-mc.txt ttH-multilepton/2lss_tight.txt 'ttH_MVAto1D_6_2lss(kinMVA_2lss_ttbar,kinMVA_2lss_ttV)' '6,0.5,6.5' $SYSTS $OPT_2L -o ${X}_BLoose_pos $POS $BLoose $FLAV $ZeroTau;
        python makeShapeCards.py ttH-multilepton/mca-2lss-mc.txt ttH-multilepton/2lss_tight.txt 'ttH_MVAto1D_6_2lss(kinMVA_2lss_ttbar,kinMVA_2lss_ttV)' '6,0.5,6.5' $SYSTS $OPT_2L -o ${X}_BLoose_neg $NEG $BLoose $FLAV $ZeroTau;
        python makeShapeCards.py ttH-multilepton/mca-2lss-mc.txt ttH-multilepton/2lss_tight.txt 'ttH_MVAto1D_6_2lss(kinMVA_2lss_ttbar,kinMVA_2lss_ttV)' '6,0.5,6.5' $SYSTS $OPT_2L -o ${X}_BTight_pos $POS $BTight $FLAV $ZeroTau;
        python makeShapeCards.py ttH-multilepton/mca-2lss-mc.txt ttH-multilepton/2lss_tight.txt 'ttH_MVAto1D_6_2lss(kinMVA_2lss_ttbar,kinMVA_2lss_ttV)' '6,0.5,6.5' $SYSTS $OPT_2L -o ${X}_BTight_neg $NEG $BTight $FLAV $ZeroTau;
    done

    python makeShapeCards.py ttH-multilepton/mca-2lss-mc.txt ttH-multilepton/2lss_tight.txt 'ttH_MVAto1D_6_2lss(kinMVA_2lss_ttbar,kinMVA_2lss_ttV)' '6,0.5,6.5' $SYSTS $OPT_2L -o ${X}_Tau $OneTau;

    echo "Done at $(date)"

fi

if [[ "$1" == "" || "$1" == "3l" ]]; then
    OPT_3L="${OPTIONS} "
    POS=" -A alwaystrue positive LepGood1_charge+LepGood2_charge+LepGood3_charge>0 "
    NEG=" -A alwaystrue negative LepGood1_charge+LepGood2_charge+LepGood3_charge<0 "

    python makeShapeCards.py ttH-multilepton/mca-3l-mc.txt ttH-multilepton/3l_tight.txt 'ttH_MVAto1D_6_3l(kinMVA_3l_ttbar,kinMVA_3l_ttV)' '6,0.5,6.5' $SYSTS $OPT_3L -o ${X}_BLoose_pos $POS $BLoose $ZeroTau;
    python makeShapeCards.py ttH-multilepton/mca-3l-mc.txt ttH-multilepton/3l_tight.txt 'ttH_MVAto1D_6_3l(kinMVA_3l_ttbar,kinMVA_3l_ttV)' '6,0.5,6.5' $SYSTS $OPT_3L -o ${X}_BLoose_neg $NEG $BLoose $ZeroTau;
    python makeShapeCards.py ttH-multilepton/mca-3l-mc.txt ttH-multilepton/3l_tight.txt 'ttH_MVAto1D_6_3l(kinMVA_3l_ttbar,kinMVA_3l_ttV)' '6,0.5,6.5' $SYSTS $OPT_3L -o ${X}_BTight_pos $POS $BTight $ZeroTau;
    python makeShapeCards.py ttH-multilepton/mca-3l-mc.txt ttH-multilepton/3l_tight.txt 'ttH_MVAto1D_6_3l(kinMVA_3l_ttbar,kinMVA_3l_ttV)' '6,0.5,6.5' $SYSTS $OPT_3L -o ${X}_BTight_neg $NEG $BTight $ZeroTau;
    python makeShapeCards.py ttH-multilepton/mca-3l-mc.txt ttH-multilepton/3l_tight.txt 'ttH_MVAto1D_6_3l(kinMVA_3l_ttbar,kinMVA_3l_ttV)' '6,0.5,6.5' $SYSTS $OPT_3L -o ${X}_Tau $OneTau;

   echo "Done at $(date)"
fi

