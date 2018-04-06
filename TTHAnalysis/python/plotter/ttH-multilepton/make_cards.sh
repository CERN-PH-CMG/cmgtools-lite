#!/bin/bash

if [[ "$HOSTNAME" == "cmsco01.cern.ch" ]]; then
    T2L=" -P /data1/peruzzi/TREES_TTH_250117_Summer16_JECV3_noClean_qgV2_skimOnlyMC_v6 --Fs {P}/1_recleaner_230217_v6 --Fs {P}/2_eventVars_230217_v6 --Fs {P}/3_kinMVA_BDTv8_230217_v6 --Fs {P}/4_BDTv8_Hj_230217_v6 --Fs {P}/5_triggerDecision_230217_v6 --Fs {P}/6_bTagSF_v6 --Fs {P}/7_tauTightSel_v6"
    T3L=" -P /data1/peruzzi/TREES_TTH_250117_Summer16_JECV3_noClean_qgV2_skim3l2j2b1B_v6 --Fs {P}/1_recleaner_230217_v6 --Fs {P}/2_eventVars_230217_v6 --Fs {P}/3_kinMVA_BDTv8_withMEM_230217_v6 --Fs {P}/4_BDTv8_Hj_230217_v6 --Fs {P}/5_triggerDecision_230217_v6 --Fs {P}/6_bTagSF_v6 --Fs {P}/7_tauTightSel_v6 --Fs {P}/8_MEM_v6"
    T4L=${T2L}
    J=8;
else
    T2L=" -P /afs/cern.ch/work/p/peruzzi/tthtrees/TREES_TTH_250117_Summer16_JECV3_noClean_qgV2_skimOnlyMC_v6 --Fs {P}/1_recleaner_230217_v6 --Fs {P}/2_eventVars_230217_v6 --Fs {P}/3_kinMVA_BDTv8_230217_v6 --Fs {P}/4_BDTv8_Hj_230217_v6 --Fs {P}/5_triggerDecision_230217_v6 --Fs {P}/6_bTagSF_v6 --Fs {P}/7_tauTightSel_v6"
    T3L=" -P /afs/cern.ch/work/p/peruzzi/tthtrees/TREES_TTH_250117_Summer16_JECV3_noClean_qgV2_skim3l2j2b1B_v6 --Fs {P}/1_recleaner_230217_v6 --Fs {P}/2_eventVars_230217_v6 --Fs {P}/3_kinMVA_BDTv8_withMEM_230217_v6 --Fs {P}/4_BDTv8_Hj_230217_v6 --Fs {P}/5_triggerDecision_230217_v6 --Fs {P}/6_bTagSF_v6 --Fs {P}/7_tauTightSel_v6 --Fs {P}/8_MEM_v6"
    T4L=${T2L}
    J=8;
fi

if [[ "X$1" == "X" ]]; then echo "Provide output directory name!"; exit; fi
OUTNAME=$1; shift;
if [[ "X$1" == "X" ]]; then echo "Provide luminosity!"; exit; fi
LUMI="$1"; shift
if [[ "${LUMI}" == "ICHEP" ]]; then LUMI="12.9 --xf .*_2016E.*,.*_2016F.*,.*_2016G.*,.*_2016H.*"; fi
if [[ "${LUMI}" == "POSTICHEP" ]]; then LUMI="23.0 --xf .*_2016B.*,.*_2016C.*,.*_2016D.*"; fi
echo "Normalizing to ${LUMI}/fb";
OPTIONS=" --tree treeProducerSusyMultilepton --s2v -j $J -l ${LUMI} -f "
test -d cards/$OUTNAME || mkdir -p cards/$OUTNAME
OPTIONS="${OPTIONS} --od cards/$OUTNAME ";

SYSTS="ttH-multilepton/systsEnv.txt"
BLoose=" -E ^BLoose "
BTight=" -E ^BTight "

#SPLITDECAYS=""
SPLITDECAYS="-splitdecays"

PROMPTSUB="--plotgroup data_fakes+=.*_promptsub --plotgroup data_fakes_FRe_norm_Up+=.*_promptsub_FRe_norm_Up --plotgroup data_fakes_FRe_norm_Dn+=.*_promptsub_FRe_norm_Dn --plotgroup data_fakes_FRe_pt_Up+=.*_promptsub_FRe_pt_Up --plotgroup data_fakes_FRe_pt_Dn+=.*_promptsub_FRe_pt_Dn --plotgroup data_fakes_FRe_be_Up+=.*_promptsub_FRe_be_Up --plotgroup data_fakes_FRe_be_Dn+=.*_promptsub_FRe_be_Dn --plotgroup data_fakes_FRm_norm_Up+=.*_promptsub_FRm_norm_Up --plotgroup data_fakes_FRm_norm_Dn+=.*_promptsub_FRm_norm_Dn --plotgroup data_fakes_FRm_pt_Up+=.*_promptsub_FRm_pt_Up --plotgroup data_fakes_FRm_pt_Dn+=.*_promptsub_FRm_pt_Dn --plotgroup data_fakes_FRm_be_Up+=.*_promptsub_FRm_be_Up --plotgroup data_fakes_FRm_be_Dn+=.*_promptsub_FRm_be_Dn"
OPTIONS="${OPTIONS} -L ttH-multilepton/functionsTTH.cc --mcc ttH-multilepton/lepchoice-ttH-FO.txt --mcc ttH-multilepton/ttH_2lss3l_triggerdefs.txt ${PROMPTSUB} --neg" # neg necessary for subsequent rebin
CATPOSTFIX=""

#FUNCTION_2L="kinMVA_2lss_ttV:kinMVA_2lss_ttbar 40,-1,1,40,-1,1"
#FUNCTION_3L="kinMVA_3l_ttV:kinMVA_3l_ttbar 40,-1,1,40,-1,1"
FUNCTION_2L="kinMVA_2lss_ttV_withHj:kinMVA_2lss_ttbar_withBDTv8 40,-1,1,40,-1,1"
FUNCTION_3L="kinMVA_3l_ttV_withMEM:kinMVA_3l_ttbar 40,-1,1,40,-1,1"

BINFUNCTION_2L="8:OurBin2l"
BINFUNCTION_3L="5:OurBin3lMEM"

MCASUFFIX="mcdata-frdata"

if [[ "$2" == "save" ]]; then
DOFILE="--savefile activate"
fi
if [[ "$2" == "read" ]]; then
DOFILE="--infile activate"
fi

if [[ "$1" == "all" || "$1" == "2lss" || "$1" == "2lss_3j" ]]; then
    OPT_2L="${T2L} ${OPTIONS} -W puw2016_nTrueInt_36fb(nTrueInt)*leptonSF_ttH(LepGood_pdgId[iLepFO_Recl[0]],LepGood_pt[iLepFO_Recl[0]],LepGood_eta[iLepFO_Recl[0]],2)*leptonSF_ttH(LepGood_pdgId[iLepFO_Recl[1]],LepGood_pt[iLepFO_Recl[1]],LepGood_eta[iLepFO_Recl[1]],2)*triggerSF_ttH(LepGood_pdgId[iLepFO_Recl[0]],LepGood_pdgId[iLepFO_Recl[1]],2)*eventBTagSF"
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
	    python makeShapeCards.py ${DOFILE} --2d-binning-function ${BINFUNCTION_2L} ttH-multilepton/mca-2lss-${MCASUFFIX}${SPLITDECAYS}.txt ttH-multilepton/2lss_tight.txt ${FUNCTION_2L} $SYSTS $OPT_2L -o 2lss_${X}_pos${CATPOSTFIX} $POS $FLAV;
            python makeShapeCards.py ${DOFILE} --2d-binning-function ${BINFUNCTION_2L} ttH-multilepton/mca-2lss-${MCASUFFIX}${SPLITDECAYS}.txt ttH-multilepton/2lss_tight.txt ${FUNCTION_2L} $SYSTS $OPT_2L -o 2lss_${X}_neg${CATPOSTFIX} $NEG $FLAV;
	else
	    python makeShapeCards.py ${DOFILE} --2d-binning-function ${BINFUNCTION_2L} ttH-multilepton/mca-2lss-${MCASUFFIX}${SPLITDECAYS}.txt ttH-multilepton/2lss_tight.txt ${FUNCTION_2L} $SYSTS $OPT_2L -o 2lss_${X}_bl_pos${CATPOSTFIX} $POS $BLoose $FLAV;
            python makeShapeCards.py ${DOFILE} --2d-binning-function ${BINFUNCTION_2L} ttH-multilepton/mca-2lss-${MCASUFFIX}${SPLITDECAYS}.txt ttH-multilepton/2lss_tight.txt ${FUNCTION_2L} $SYSTS $OPT_2L -o 2lss_${X}_bl_neg${CATPOSTFIX} $NEG $BLoose $FLAV;
            python makeShapeCards.py ${DOFILE} --2d-binning-function ${BINFUNCTION_2L} ttH-multilepton/mca-2lss-${MCASUFFIX}${SPLITDECAYS}.txt ttH-multilepton/2lss_tight.txt ${FUNCTION_2L} $SYSTS $OPT_2L -o 2lss_${X}_bt_pos${CATPOSTFIX} $POS $BTight $FLAV;
            python makeShapeCards.py ${DOFILE} --2d-binning-function ${BINFUNCTION_2L} ttH-multilepton/mca-2lss-${MCASUFFIX}${SPLITDECAYS}.txt ttH-multilepton/2lss_tight.txt ${FUNCTION_2L} $SYSTS $OPT_2L -o 2lss_${X}_bt_neg${CATPOSTFIX} $NEG $BTight $FLAV;
	fi
    done

    echo "Done at $(date)"

fi

if [[ "$1" == "all" || "$1" == "3l" ]]; then
    OPT_3L="${T3L} ${OPTIONS} -W puw2016_nTrueInt_36fb(nTrueInt)*leptonSF_ttH(LepGood_pdgId[iLepFO_Recl[0]],LepGood_pt[iLepFO_Recl[0]],LepGood_eta[iLepFO_Recl[0]],3)*leptonSF_ttH(LepGood_pdgId[iLepFO_Recl[1]],LepGood_pt[iLepFO_Recl[1]],LepGood_eta[iLepFO_Recl[1]],3)*leptonSF_ttH(LepGood_pdgId[iLepFO_Recl[2]],LepGood_pt[iLepFO_Recl[2]],LepGood_eta[iLepFO_Recl[2]],3)*triggerSF_ttH(LepGood_pdgId[iLepFO_Recl[0]],LepGood_pdgId[iLepFO_Recl[1]],3)*eventBTagSF"
    POS=" -A alwaystrue positive (LepGood1_charge+LepGood2_charge+LepGood3_charge)>0 "
    NEG=" -A alwaystrue negative (LepGood1_charge+LepGood2_charge+LepGood3_charge)<0 "

    echo "3l";
    python makeShapeCards.py ${DOFILE} --2d-binning-function ${BINFUNCTION_3L} ttH-multilepton/mca-3l-${MCASUFFIX}${SPLITDECAYS}.txt ttH-multilepton/3l_tight.txt ${FUNCTION_3L} $SYSTS $OPT_3L -o 3l_bl_pos${CATPOSTFIX} $POS $BLoose;
    python makeShapeCards.py ${DOFILE} --2d-binning-function ${BINFUNCTION_3L} ttH-multilepton/mca-3l-${MCASUFFIX}${SPLITDECAYS}.txt ttH-multilepton/3l_tight.txt ${FUNCTION_3L} $SYSTS $OPT_3L -o 3l_bl_neg${CATPOSTFIX} $NEG $BLoose;
    python makeShapeCards.py ${DOFILE} --2d-binning-function ${BINFUNCTION_3L} ttH-multilepton/mca-3l-${MCASUFFIX}${SPLITDECAYS}.txt ttH-multilepton/3l_tight.txt ${FUNCTION_3L} $SYSTS $OPT_3L -o 3l_bt_pos${CATPOSTFIX} $POS $BTight;
    python makeShapeCards.py ${DOFILE} --2d-binning-function ${BINFUNCTION_3L} ttH-multilepton/mca-3l-${MCASUFFIX}${SPLITDECAYS}.txt ttH-multilepton/3l_tight.txt ${FUNCTION_3L} $SYSTS $OPT_3L -o 3l_bt_neg${CATPOSTFIX} $NEG $BTight;

   echo "Done at $(date)"
fi

if [[ "$1" == "3l_zpeak" || "$1" == "3l_zpeak_btight" ]]; then

    POS=" -A alwaystrue positive (LepGood1_charge+LepGood2_charge+LepGood3_charge)>0 "
    NEG=" -A alwaystrue negative (LepGood1_charge+LepGood2_charge+LepGood3_charge)<0 "
    OPT_3L="${T3L} ${OPTIONS} -W puw2016_nTrueInt_36fb(nTrueInt)*leptonSF_ttH(LepGood_pdgId[iLepFO_Recl[0]],LepGood_pt[iLepFO_Recl[0]],LepGood_eta[iLepFO_Recl[0]],3)*leptonSF_ttH(LepGood_pdgId[iLepFO_Recl[1]],LepGood_pt[iLepFO_Recl[1]],LepGood_eta[iLepFO_Recl[1]],3)*leptonSF_ttH(LepGood_pdgId[iLepFO_Recl[2]],LepGood_pt[iLepFO_Recl[2]],LepGood_eta[iLepFO_Recl[2]],3)*triggerSF_ttH(LepGood_pdgId[iLepFO_Recl[0]],LepGood_pdgId[iLepFO_Recl[1]],3)*eventBTagSF"
    OPT_3L="${OPT_3L} -I ^Zveto"
    CATPOSTFIX="_zpeak"
    echo "3l on-Z";

    if [[ "$1" == "3l_zpeak_btight" ]]; then
	OPT_3L="${OPT_3L} -X ^2b1B -E ^gt2b -E ^1B"
	CATPOSTFIX="${CATPOSTFIX}_btight"
	echo "asking tighter b requirements"
    fi

    python makeShapeCards.py ${DOFILE} --2d-binning-function ${BINFUNCTION_3L} ttH-multilepton/mca-3l-${MCASUFFIX}${SPLITDECAYS}.txt ttH-multilepton/3l_tight.txt ${FUNCTION_3L} $SYSTS $OPT_3L -o 3l_bl_pos${CATPOSTFIX} $POS $BLoose;
    python makeShapeCards.py ${DOFILE} --2d-binning-function ${BINFUNCTION_3L} ttH-multilepton/mca-3l-${MCASUFFIX}${SPLITDECAYS}.txt ttH-multilepton/3l_tight.txt ${FUNCTION_3L} $SYSTS $OPT_3L -o 3l_bl_neg${CATPOSTFIX} $NEG $BLoose;
    python makeShapeCards.py ${DOFILE} --2d-binning-function ${BINFUNCTION_3L} ttH-multilepton/mca-3l-${MCASUFFIX}${SPLITDECAYS}.txt ttH-multilepton/3l_tight.txt ${FUNCTION_3L} $SYSTS $OPT_3L -o 3l_bt_pos${CATPOSTFIX} $POS $BTight;
    python makeShapeCards.py ${DOFILE} --2d-binning-function ${BINFUNCTION_3L} ttH-multilepton/mca-3l-${MCASUFFIX}${SPLITDECAYS}.txt ttH-multilepton/3l_tight.txt ${FUNCTION_3L} $SYSTS $OPT_3L -o 3l_bt_neg${CATPOSTFIX} $NEG $BTight;

   echo "Done at $(date)"
fi

if [[ "$1" == "all" || "$1" == "4l" ]]; then
    OPT_4L="${T4L} ${OPTIONS} -W puw2016_nTrueInt_36fb(nTrueInt)*leptonSF_ttH(LepGood_pdgId[iLepFO_Recl[0]],LepGood_pt[iLepFO_Recl[0]],LepGood_eta[iLepFO_Recl[0]],3)*leptonSF_ttH(LepGood_pdgId[iLepFO_Recl[1]],LepGood_pt[iLepFO_Recl[1]],LepGood_eta[iLepFO_Recl[1]],3)*leptonSF_ttH(LepGood_pdgId[iLepFO_Recl[2]],LepGood_pt[iLepFO_Recl[2]],LepGood_eta[iLepFO_Recl[2]],3)*leptonSF_ttH(LepGood_pdgId[iLepFO_Recl[3]],LepGood_pt[iLepFO_Recl[3]],LepGood_eta[iLepFO_Recl[3]],3)*triggerSF_ttH(LepGood_pdgId[iLepFO_Recl[0]],LepGood_pdgId[iLepFO_Recl[1]],3)*eventBTagSF"

    ONEBIN_4L="1 1,0.5,1.5"

    echo "4l";
    python makeShapeCards.py ${DOFILE} ttH-multilepton/mca-4l-${MCASUFFIX}${SPLITDECAYS}.txt ttH-multilepton/4l_tight.txt ${ONEBIN_4L} $SYSTS $OPT_4L -o 4l${CATPOSTFIX};

   echo "Done at $(date)"
fi
