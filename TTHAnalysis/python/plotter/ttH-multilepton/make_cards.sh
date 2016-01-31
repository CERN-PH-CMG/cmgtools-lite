#!/bin/bash

if [[ "$HOSTNAME" == "cmsphys10" ]]; then
#    T="/data1/p/peruzzi/TREES_74X_140116_MiniIso_tauClean_Mor16lepMVA";
    T="/data/p/peruzzi/skim_2lss_3l_TREES_74X_140116_MiniIso_tauClean_Mor16lepMVA";
    J=8;
else
    T="/afs/cern.ch/work/p/peruzzi/tthtrees/TREES_74X_140116_MiniIso_tauClean_Mor16lepMVA";
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
SYSTS="ttH-multilepton/systsEnv.txt ../../macros/systematics/btagSysts2.txt"
BLoose=" -E BLoose "
BTight=" -E BTight "
ZeroTau=" -E 0tau "
OneTau=" -E 1tau "

OPTIONS="${OPTIONS} --Fs {P}/2_recleaner_v6_vetoCSVM_eleIdEmuPt30_PtRatio030orMVA --Fs {P}/4_kinMVA_trainMilosJan31_v3_reclv6"
OPTIONS="${OPTIONS} --mcc ttH-multilepton/lepchoice-ttH-FO.txt --mcc ttH-multilepton/ttH_2lss3l_triggerdefs.txt -W puw(nTrueInt)"
OPTIONS="${OPTIONS} --asimov --xp data --xp '.*data.*'" # safety!



#OPTIONS="${OPTIONS} -X exclusive " ; echo "!!!!!! TESTING !!!!!!"
#OPTIONS="${OPTIONS} -E tightMVA080 " ; echo "!!!!!! TESTING !!!!!!"
#OPTIONS="${OPTIONS} -E tightMVA075 " ; echo "!!!!!! TEMPORARY !!!!!!"   


FUNCTION_2L="ttH_MVAto1D_6_2lss_Marco(kinMVA_2lss_ttbar,kinMVA_2lss_ttV,LepGood1_pdgId,LepGood2_pdgId) 6,0.5,6.5"
FUNCTION_3L="ttH_MVAto1D_3_3l_Marco(kinMVA_3l_ttbar,kinMVA_3l_ttV) 3,0.5,3.5"
# for testing different binnings "ttH_MVAto1D_6_flex(kinMVA_3l_ttbar,kinMVA_3l_ttV,LepGood1_pdgId,LepGood2_pdgId,$2,$3,$4) 4,0.5,4.5"

if [[ "$1" == "" || "$1" == "2lss" ]]; then
    OPT_2L="${OPTIONS} "

    POS=" -A alwaystrue positive LepGood1_charge>0 "
    NEG=" -A alwaystrue negative LepGood1_charge<0 "

    for X in mm ee em; do 
        echo "2lss_${X}";
	FLAV=" -E ${X} "
	if [[ "${X}" == "mm" ]]; then Y="mumu"; else Y=${X}; fi
	if [[ "${X}" == "ee" ]]; then
	    python makeShapeCards.py ttH-multilepton/mca-2lss-mc.txt ttH-multilepton/2lss_tight.txt ${FUNCTION_2L} $SYSTS $OPT_2L -o 2lss_${Y}_0tau_BCat_MVA_pos $POS $FLAV $ZeroTau;
            python makeShapeCards.py ttH-multilepton/mca-2lss-mc.txt ttH-multilepton/2lss_tight.txt ${FUNCTION_2L} $SYSTS $OPT_2L -o 2lss_${Y}_0tau_BCat_MVA_neg $NEG $FLAV $ZeroTau;
	else
	    python makeShapeCards.py ttH-multilepton/mca-2lss-mc.txt ttH-multilepton/2lss_tight.txt ${FUNCTION_2L} $SYSTS $OPT_2L -o 2lss_${Y}_0tau_bl_BCat_MVA_pos $POS $BLoose $FLAV $ZeroTau;
            python makeShapeCards.py ttH-multilepton/mca-2lss-mc.txt ttH-multilepton/2lss_tight.txt ${FUNCTION_2L} $SYSTS $OPT_2L -o 2lss_${Y}_0tau_bl_BCat_MVA_neg $NEG $BLoose $FLAV $ZeroTau;
            python makeShapeCards.py ttH-multilepton/mca-2lss-mc.txt ttH-multilepton/2lss_tight.txt ${FUNCTION_2L} $SYSTS $OPT_2L -o 2lss_${Y}_0tau_bt_BCat_MVA_pos $POS $BTight $FLAV $ZeroTau;
            python makeShapeCards.py ttH-multilepton/mca-2lss-mc.txt ttH-multilepton/2lss_tight.txt ${FUNCTION_2L} $SYSTS $OPT_2L -o 2lss_${Y}_0tau_bt_BCat_MVA_neg $NEG $BTight $FLAV $ZeroTau;
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
    python makeShapeCards.py ttH-multilepton/mca-3l-mc.txt ttH-multilepton/3l_tight.txt ${FUNCTION_3L} $SYSTS $OPT_3L -o 3lBCat_bl_MVA_pos $POS $BLoose;
    python makeShapeCards.py ttH-multilepton/mca-3l-mc.txt ttH-multilepton/3l_tight.txt ${FUNCTION_3L} $SYSTS $OPT_3L -o 3lBCat_bl_MVA_neg $NEG $BLoose;
    python makeShapeCards.py ttH-multilepton/mca-3l-mc.txt ttH-multilepton/3l_tight.txt ${FUNCTION_3L} $SYSTS $OPT_3L -o 3lBCat_bt_MVA_pos $POS $BTight;
    python makeShapeCards.py ttH-multilepton/mca-3l-mc.txt ttH-multilepton/3l_tight.txt ${FUNCTION_3L} $SYSTS $OPT_3L -o 3lBCat_bt_MVA_neg $NEG $BTight;

   echo "Done at $(date)"
fi

