#!/bin/bash

if [[ "$HOSTNAME" == "cmsco01.cern.ch" ]]; then
    T2L=" -P /data1/peruzzi/TREES_TTH_250117_Summer16_JECV3_noClean_qgV2_skimOnlyMC_v1 --Fs {P}/1_recleaner_250117_v1 --Fs {P}/2_eventVars_250117_v1 --Fs {P}/3_kinMVA_250117_v2_withBDTv8Hjv2 --Fs {P}/5_triggerDecision_250117_v1"
    T3L=${T2L}
    J=8;
else
    T2L=" -P /afs/cern.ch/work/p/peruzzi/tthtrees/TREES_TTH_250117_Summer16_JECV3_noClean_qgV2_skimOnlyMC_v1 --Fs {P}/1_recleaner_250117_v1 --Fs {P}/2_eventVars_250117_v1 --Fs {P}/3_kinMVA_250117_v2_withBDTv8Hjv2 --Fs {P}/5_triggerDecision_250117_v1"
    T3L=${T2L}
    J=4;
fi

if [[ "X$1" == "X" ]]; then echo "Provide output directory name!"; exit; fi
OUTNAME=$1; shift;
if [[ "X$1" == "X" ]]; then echo "Provide luminosity!"; exit; fi
LUMI="$1"; shift
echo "Normalizing to ${LUMI}/fb";
OPTIONS=" --tree treeProducerSusyMultilepton --s2v -j $J -l ${LUMI} -f "
test -d cards/$OUTNAME || mkdir -p cards/$OUTNAME
OPTIONS="${OPTIONS} --od cards/$OUTNAME ";

SYSTS="ttH-multilepton/systsEnv.txt"
#SYSTS="ttH-multilepton/systsEnv_pureMC_dummy.txt"
BLoose=" -E ^BLoose "
BTight=" -E ^BTight "

#SPLITDECAYS=""
SPLITDECAYS="-splitdecays"

### # ADDED ASIMOV HERE (temporary)
OPTIONS="${OPTIONS} --asimov -L ttH-multilepton/functionsTTH.cc --mcc ttH-multilepton/lepchoice-ttH-FO.txt --mcc ttH-multilepton/ttH_2lss3l_triggerdefs.txt --neg" # neg necessary for subsequent rebin
CATPOSTFIX=""

### #FUNCTION_2L="kinMVA_2lss_ttV:kinMVA_2lss_ttbar 40,-1,1,40,-1,1"
### #FUNCTION_3L="kinMVA_3l_ttV_withMEM:kinMVA_3l_ttbar 40,-1,1,40,-1,1"
#FUNCTION_2L="kinMVA_2lss_ttV:kinMVA_2lss_ttbar 40,-1,1,40,-1,1"
FUNCTION_2L="kinMVA_2lss_ttV_withHj:kinMVA_2lss_ttbar_withBDTv8 40,-1,1,40,-1,1"
FUNCTION_3L="kinMVA_3l_ttV:kinMVA_3l_ttbar 40,-1,1,40,-1,1"
#BINFUNCTION_2L="7:ttH_MVAto1D_7_2lss_Marco"
#BINFUNCTION_3L="5:ttH_MVAto1D_5_3l_Marco"
BINFUNCTION_2L="7:OurBin2l"
BINFUNCTION_3L="4:OurBin3l"

if [[ "$2" == "save" ]]; then
DOFILE="--savefile activate"
fi
if [[ "$2" == "read" ]]; then
DOFILE="--infile activate"
fi

### # REPLACED MCA NAME NO DATA AND NO PRESCALE

if [[ "$1" == "all" || "$1" == "2lss" || "$1" == "2lss_3j" ]]; then
### #    OPT_2L="${T2L} ${OPTIONS} -W puw2016_nTrueInt_36fb(nTrueInt)*leptonSF_ttH(LepGood_pdgId[iLepFO_Recl[0]],LepGood_pt[iLepFO_Recl[0]],LepGood_eta[iLepFO_Recl[0]],2)*leptonSF_ttH(LepGood_pdgId[iLepFO_Recl[1]],LepGood_pt[iLepFO_Recl[1]],LepGood_eta[iLepFO_Recl[1]],2)*triggerSF_ttH(LepGood_pdgId[iLepFO_Recl[0]],LepGood_pt[iLepFO_Recl[0]],LepGood_pdgId[iLepFO_Recl[1]],LepGood_pt[iLepFO_Recl[1]],2)*eventBTagSF"
    OPT_2L="${T2L} ${OPTIONS} -W puw2016_nTrueInt_36fb(nTrueInt)*leptonSF_ttH(LepGood_pdgId[iLepFO_Recl[0]],LepGood_pt[iLepFO_Recl[0]],LepGood_eta[iLepFO_Recl[0]],2)*leptonSF_ttH(LepGood_pdgId[iLepFO_Recl[1]],LepGood_pt[iLepFO_Recl[1]],LepGood_eta[iLepFO_Recl[1]],2)"
    POS=" -A alwaystrue positive LepGood1_charge>0 "
    NEG=" -A alwaystrue negative LepGood1_charge<0 "

    if [[ "$1" == "2lss_3j" ]]; then
	OPT_2L="${OPT_2L} -X ^4j -E ^x3j"
	CATPOSTFIX="_3j"
    fi

    for X in mm ee em; do 
        echo "2lss_${X}";
	FLAV=" -E ^${X} "
	if [[ "${X}" == "ee" ]]; then
	    python makeShapeCards.py ${DOFILE} --2d-binning-function ${BINFUNCTION_2L} ttH-multilepton/mca-2lss-mcdata-frdata${SPLITDECAYS}.txt ttH-multilepton/2lss_tight.txt ${FUNCTION_2L} $SYSTS $OPT_2L -o 2lss_${X}_pos${CATPOSTFIX} $POS $FLAV;
            python makeShapeCards.py ${DOFILE} --2d-binning-function ${BINFUNCTION_2L} ttH-multilepton/mca-2lss-mcdata-frdata${SPLITDECAYS}.txt ttH-multilepton/2lss_tight.txt ${FUNCTION_2L} $SYSTS $OPT_2L -o 2lss_${X}_neg${CATPOSTFIX} $NEG $FLAV;
	else
	    python makeShapeCards.py ${DOFILE} --2d-binning-function ${BINFUNCTION_2L} ttH-multilepton/mca-2lss-mcdata-frdata${SPLITDECAYS}.txt ttH-multilepton/2lss_tight.txt ${FUNCTION_2L} $SYSTS $OPT_2L -o 2lss_${X}_bl_pos${CATPOSTFIX} $POS $BLoose $FLAV;
            python makeShapeCards.py ${DOFILE} --2d-binning-function ${BINFUNCTION_2L} ttH-multilepton/mca-2lss-mcdata-frdata${SPLITDECAYS}.txt ttH-multilepton/2lss_tight.txt ${FUNCTION_2L} $SYSTS $OPT_2L -o 2lss_${X}_bl_neg${CATPOSTFIX} $NEG $BLoose $FLAV;
            python makeShapeCards.py ${DOFILE} --2d-binning-function ${BINFUNCTION_2L} ttH-multilepton/mca-2lss-mcdata-frdata${SPLITDECAYS}.txt ttH-multilepton/2lss_tight.txt ${FUNCTION_2L} $SYSTS $OPT_2L -o 2lss_${X}_bt_pos${CATPOSTFIX} $POS $BTight $FLAV;
            python makeShapeCards.py ${DOFILE} --2d-binning-function ${BINFUNCTION_2L} ttH-multilepton/mca-2lss-mcdata-frdata${SPLITDECAYS}.txt ttH-multilepton/2lss_tight.txt ${FUNCTION_2L} $SYSTS $OPT_2L -o 2lss_${X}_bt_neg${CATPOSTFIX} $NEG $BTight $FLAV;
	fi
    done

    echo "Done at $(date)"

fi

if [[ "$1" == "all" || "$1" == "3l" ]]; then
### #    OPT_3L="${T3L} ${OPTIONS} -W puw2016_nTrueInt_36fb(nTrueInt)*leptonSF_ttH(LepGood_pdgId[iLepFO_Recl[0]],LepGood_pt[iLepFO_Recl[0]],LepGood_eta[iLepFO_Recl[0]],3)*leptonSF_ttH(LepGood_pdgId[iLepFO_Recl[1]],LepGood_pt[iLepFO_Recl[1]],LepGood_eta[iLepFO_Recl[1]],3)*leptonSF_ttH(LepGood_pdgId[iLepFO_Recl[2]],LepGood_pt[iLepFO_Recl[2]],LepGood_eta[iLepFO_Recl[2]],3)*triggerSF_ttH(LepGood_pdgId[iLepFO_Recl[0]],LepGood_pt[iLepFO_Recl[0]],LepGood_pdgId[iLepFO_Recl[1]],LepGood_pt[iLepFO_Recl[1]],3)*eventBTagSF"
    OPT_3L="${T3L} ${OPTIONS} -W puw2016_nTrueInt_36fb(nTrueInt)*leptonSF_ttH(LepGood_pdgId[iLepFO_Recl[0]],LepGood_pt[iLepFO_Recl[0]],LepGood_eta[iLepFO_Recl[0]],3)*leptonSF_ttH(LepGood_pdgId[iLepFO_Recl[1]],LepGood_pt[iLepFO_Recl[1]],LepGood_eta[iLepFO_Recl[1]],3)*leptonSF_ttH(LepGood_pdgId[iLepFO_Recl[2]],LepGood_pt[iLepFO_Recl[2]],LepGood_eta[iLepFO_Recl[2]],3)*leptonSF_ttH(LepGood_pdgId[iLepFO_Recl[3]],LepGood_pt[iLepFO_Recl[3]],LepGood_eta[iLepFO_Recl[3]],3)"
    POS=" -A alwaystrue positive (LepGood1_charge+LepGood2_charge+LepGood3_charge)>0 "
    NEG=" -A alwaystrue negative (LepGood1_charge+LepGood2_charge+LepGood3_charge)<0 "

    echo "3l";
    python makeShapeCards.py ${DOFILE} --2d-binning-function ${BINFUNCTION_3L} ttH-multilepton/mca-3l-mcdata-frdata${SPLITDECAYS}.txt ttH-multilepton/3l_tight.txt ${FUNCTION_3L} $SYSTS $OPT_3L -o 3l_bl_pos${CATPOSTFIX} $POS $BLoose;
    python makeShapeCards.py ${DOFILE} --2d-binning-function ${BINFUNCTION_3L} ttH-multilepton/mca-3l-mcdata-frdata${SPLITDECAYS}.txt ttH-multilepton/3l_tight.txt ${FUNCTION_3L} $SYSTS $OPT_3L -o 3l_bl_neg${CATPOSTFIX} $NEG $BLoose;
    python makeShapeCards.py ${DOFILE} --2d-binning-function ${BINFUNCTION_3L} ttH-multilepton/mca-3l-mcdata-frdata${SPLITDECAYS}.txt ttH-multilepton/3l_tight.txt ${FUNCTION_3L} $SYSTS $OPT_3L -o 3l_bt_pos${CATPOSTFIX} $POS $BTight;
    python makeShapeCards.py ${DOFILE} --2d-binning-function ${BINFUNCTION_3L} ttH-multilepton/mca-3l-mcdata-frdata${SPLITDECAYS}.txt ttH-multilepton/3l_tight.txt ${FUNCTION_3L} $SYSTS $OPT_3L -o 3l_bt_neg${CATPOSTFIX} $NEG $BTight;

   echo "Done at $(date)"
fi

### #if [[ "$1" == "3l_zpeak" ]]; then
### #
### #    POS=" -A alwaystrue positive (LepGood1_charge+LepGood2_charge+LepGood3_charge)>0 "
### #    NEG=" -A alwaystrue negative (LepGood1_charge+LepGood2_charge+LepGood3_charge)<0 "
### #    OPT_3L="${T2L} ${OPTIONS} -W puw2016_nTrueInt_36fb(nTrueInt)*leptonSF_ttH(LepGood_pdgId[iLepFO_Recl[0]],LepGood_pt[iLepFO_Recl[0]],LepGood_eta[iLepFO_Recl[0]],3)*leptonSF_ttH(LepGood_pdgId[iLepFO_Recl[1]],LepGood_pt[iLepFO_Recl[1]],LepGood_eta[iLepFO_Recl[1]],3)*leptonSF_ttH(LepGood_pdgId[iLepFO_Recl[2]],LepGood_pt[iLepFO_Recl[2]],LepGood_eta[iLepFO_Recl[2]],3)*triggerSF_ttH(LepGood_pdgId[iLepFO_Recl[0]],LepGood_pt[iLepFO_Recl[0]],LepGood_pdgId[iLepFO_Recl[1]],LepGood_pt[iLepFO_Recl[1]],3)*eventBTagSF -I ^Zveto"
### #    FUNCTION_3L="kinMVA_3l_ttV:kinMVA_3l_ttbar 40,-1,1,40,-1,1" # use MVA without MEM on-peak
### #    CATPOSTFIX="_zpeak"
### #
### #    echo "3l on-Z";
### #    python makeShapeCards.py ${DOFILE} --2d-binning-function ${BINFUNCTION_3L} ttH-multilepton/mca-3l-mcdata-frdata${SPLITDECAYS}.txt ttH-multilepton/3l_tight.txt ${FUNCTION_3L} $SYSTS $OPT_3L -o 3l_bl_pos${CATPOSTFIX} $POS $BLoose;
### #    python makeShapeCards.py ${DOFILE} --2d-binning-function ${BINFUNCTION_3L} ttH-multilepton/mca-3l-mcdata-frdata${SPLITDECAYS}.txt ttH-multilepton/3l_tight.txt ${FUNCTION_3L} $SYSTS $OPT_3L -o 3l_bl_neg${CATPOSTFIX} $NEG $BLoose;
### #    python makeShapeCards.py ${DOFILE} --2d-binning-function ${BINFUNCTION_3L} ttH-multilepton/mca-3l-mcdata-frdata${SPLITDECAYS}.txt ttH-multilepton/3l_tight.txt ${FUNCTION_3L} $SYSTS $OPT_3L -o 3l_bt_pos${CATPOSTFIX} $POS $BTight;
### #    python makeShapeCards.py ${DOFILE} --2d-binning-function ${BINFUNCTION_3L} ttH-multilepton/mca-3l-mcdata-frdata${SPLITDECAYS}.txt ttH-multilepton/3l_tight.txt ${FUNCTION_3L} $SYSTS $OPT_3L -o 3l_bt_neg${CATPOSTFIX} $NEG $BTight;
### #
### #   echo "Done at $(date)"
### #fi

