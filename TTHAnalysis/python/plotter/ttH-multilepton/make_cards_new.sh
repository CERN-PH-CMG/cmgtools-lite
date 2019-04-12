#!/bin/bash

TREES_ZERO=TREES_TTH_190418_Fall17_skim2lss3l
case $HOSTNAME in
    cmsco01.cern.ch) ORIGIN=/data/peruzzi; J=8 ;;
    cmsphys10) ORIGIN=/data1/g/gpetrucc; J=8 ;;
    gpetrucc-vm2.cern.ch) ORIGIN=/data/gpetrucc; J=4 ;;
    *)
        ORIGIN=/afs/cern.ch/work/p/peruzzi; J=4
        test -d /tmp/$USER/TREES_TTH_190418_Fall17_skim2lss3l && ORIGIN=/tmp/$USER;;
esac;

T2L=" -P $ORIGIN/TREES_TTH_190418_Fall17_skim2lss3l --Fs {P}/1_recleaner_180518_v2 --Fs {P}/5_triggerDecision_230418_v1 --Fs {P}/7_tauTightSel_v2 --FMCs {P}/8_vtxWeight2017_v1 --FMCs {P}/6_bTagSF_v2 --Fs {P}/2_eventVars_230418_v2 --Fs {P}/3_kinMVA_noMEM_200618_v5"
T3L=" -P $ORIGIN/TREES_TTH_190418_Fall17_skim2lss3l --Fs {P}/1_recleaner_180518_v2 --Fs {P}/5_triggerDecision_230418_v1 --Fs {P}/7_tauTightSel_v2 --FMCs {P}/8_vtxWeight2017_v1 --FMCs {P}/6_bTagSF_v2 --Fs {P}/2_eventVars_230418_v2 --Fs {P}/3_kinMVA_withMEM_200618_v5"
T4L=${T2L}
#if test -d $ORIGIN/TREES_TTH_190418_Fall17_skim4l ; then
#    T4L=${T4L/TREES_TTH_190418_Fall17_skim2lss3l/TREES_TTH_190418_Fall17_skim4l};
#fi

if [[ "X$1" == "X" ]]; then echo "Provide output directory name!"; exit; fi
OUTNAME=$1; shift;
if [[ "X$1" == "X" ]]; then echo "Provide luminosity!"; exit; fi
LUMI="$1"; shift
echo "Normalizing to ${LUMI}/fb";
OPTIONS=" --tree treeProducerSusyMultilepton --s2v -j $J -l ${LUMI} -f --WA prescaleFromSkim"
test -d cards/$OUTNAME || mkdir -p cards/$OUTNAME
OPTIONS="${OPTIONS} --od cards/$OUTNAME ";

SYSTS="--unc ttH-multilepton/systsUnc.txt --amc"
case $1 in
--bbb)
    shift;
    SYSTS="--unc ttH-multilepton/systsUnc.txt --bbb CMS_ttHl17_templstat";;
esac;
BLoose=" -E ^BLoose "
BTight=" -E ^BTight "

#SPLITDECAYS=""
SPLITDECAYS="-splitdecays"

PROMPTSUB="--plotgroup data_fakes+=.*_promptsub"
OPTIONS="${OPTIONS} -L ttH-multilepton/functionsTTH.cc --mcc ttH-multilepton/lepchoice-ttH-FO.txt ${PROMPTSUB} --neg" # neg necessary for subsequent rebin
CATPOSTFIX=""

FUNCTION_2L="OurBin2l(kinMVA_2lss_ttbar_withBDTrTT,kinMVA_2lss_ttV_withHj_rTT) [0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5,10.5,11.5]"
#FUNCTION_3L="OurBin3l(kinMVA_3l_ttbar,kinMVA_3l_ttV) [0.5,1.5,2.5,3.5,4.5,5.5,6.5]"
FUNCTION_3L="OurBin3l(kinMVA_3l_ttbar_withMEM,kinMVA_3l_ttV_withMEM) [0.5,1.5,2.5,3.5,4.5,5.5,6.5]"
FUNCTION_SVA_2L="mass_2(LepGood1_conePt,LepGood1_eta,LepGood1_phi,LepGood1_mass,LepGood2_conePt,LepGood2_eta,LepGood2_phi,LepGood2_mass) [10.0,50.0,70.0,80.0,90.0,110.0,140.0,190.0,400.0]"
FUNCTION_SVA_3L="mass_3_cheap(LepGood1_pt,LepGood1_eta,LepGood2_pt,LepGood2_eta,LepGood2_phi-LepGood1_phi,LepGood3_pt,LepGood3_eta,LepGood3_phi-LepGood1_phi) [26.0,107.0,146.0,193.0,261.0,400.0]"
ONEBIN="1 1,0.5,1.5"

MCASUFFIX="mcdata-frdata"

SVA="false"
if [[ "$1" == "SVA" ]]; then
FUNCTION_2L=${FUNCTION_SVA_2L}
FUNCTION_3L=${FUNCTION_SVA_3L}
SVA="true"
shift
fi
if [[ "$2" == "save" ]]; then
DOFILE="--savefile"
fi
if [[ "$2" == "read" ]]; then
DOFILE="--infile"
fi
if [[ "$2" == "regularize" ]]; then
DOFILE="--regularize"
fi

if [[ "$1" == "all" || "$1" == "2lss" || "$1" == "2lss_3j" ]]; then
#    test -d $ORIGIN/TREES_TTH_190418_Fall17_skim2lss_3j_2b1B && T2L="${T2L/TREES_TTH_190418_Fall17_skim2lss3l/TREES_TTH_190418_Fall17_skim2lss_3j_2b1B}";
    OPT_2L="${T2L} ${OPTIONS} -W vtxWeight2017*eventBTagSF*leptonSF_ttH(LepGood_pdgId[iLepFO_Recl[0]],LepGood_pt[iLepFO_Recl[0]],LepGood_eta[iLepFO_Recl[0]],2)*leptonSF_ttH(LepGood_pdgId[iLepFO_Recl[1]],LepGood_pt[iLepFO_Recl[1]],LepGood_eta[iLepFO_Recl[1]],2)*triggerSF_ttH(LepGood_pdgId[iLepFO_Recl[0]],LepGood_pt[iLepFO_Recl[0]],LepGood_pdgId[iLepFO_Recl[1]],LepGood_pt[iLepFO_Recl[1]],nLepTight_Recl,0)"
    CATPOSTFIX=""

    if [[ "$1" == "2lss_3j" ]]; then
	OPT_2L="${OPT_2L} -X ^4j -E ^x3j"
	CATPOSTFIX="_3j"
    fi

    if [[ "$SVA" == "false" ]]; then
	CATFUNC="ttH_catIndex_2lss(LepGood1_pdgId,LepGood2_pdgId,LepGood1_charge,nBJetMedium25)"
	CATBINS="[0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5,10.5]"
	CATNAMES="$(echo ee_{neg,pos}${CATPOSTFIX} {em,mm}_{bl,bt}_{neg,pos}${CATPOSTFIX} | sed 's/ /,/g')"
    else
	CATFUNC="ttH_catIndex_2lss_SVA(LepGood1_pdgId,LepGood2_pdgId,LepGood1_charge,nJet25)"
	if [[ "$1" == "2lss_3j" ]]; then
	    CATBINS="[0.5,2.5,4.5,6.5,8.5,10.5]" # no high-jet category when requiring x3j
	    CATNAMES="$(echo ee${CATPOSTFIX} {em,mm}_{neg,pos}${CATPOSTFIX} | sed 's/ /,/g')"
	else
	    CATBINS="[0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5,10.5]"
	    CATNAMES="$(echo ee_{lj,hj}${CATPOSTFIX} {em,mm}_{neg,pos}_{lj,hj}${CATPOSTFIX} | sed 's/ /,/g')"
	fi
    fi

    python makeShapeCardsNew.py ${DOFILE} ttH-multilepton/mca-2lss-${MCASUFFIX}${SPLITDECAYS}.txt ttH-multilepton/2lss_tight.txt ${FUNCTION_2L} $SYSTS $OPT_2L --binname ttH_2lss --categorize $CATFUNC $CATBINS $CATNAMES;

    echo "Done at $(date)"

fi

if [[ "$1" == "all" || "$1" == "3l" ]]; then
    test -d $ORIGIN/TREES_TTH_190418_Fall17_skim_3l_2j_2b1B_Zveto_presc && T3L="${T3L/TREES_TTH_190418_Fall17_skim2lss3l/TREES_TTH_190418_Fall17_skim_3l_2j_2b1B_Zveto_presc}";
    OPT_3L="${T3L} ${OPTIONS} -W vtxWeight2017*eventBTagSF*leptonSF_ttH(LepGood_pdgId[iLepFO_Recl[0]],LepGood_pt[iLepFO_Recl[0]],LepGood_eta[iLepFO_Recl[0]],3)*leptonSF_ttH(LepGood_pdgId[iLepFO_Recl[1]],LepGood_pt[iLepFO_Recl[1]],LepGood_eta[iLepFO_Recl[1]],3)*leptonSF_ttH(LepGood_pdgId[iLepFO_Recl[2]],LepGood_pt[iLepFO_Recl[2]],LepGood_eta[iLepFO_Recl[2]],3)*triggerSF_ttH(LepGood_pdgId[iLepFO_Recl[0]],LepGood_pt[iLepFO_Recl[0]],LepGood_pdgId[iLepFO_Recl[1]],LepGood_pt[iLepFO_Recl[1]],nLepTight_Recl,0)"
    CATPOSTFIX=""

    echo "3l";
    if [[ "$SVA" == "false" ]]; then
    CATFUNC="ttH_catIndex_3l(LepGood1_charge,LepGood2_charge,LepGood3_charge,nBJetMedium25)"
    CATBINS="[10.5,11.5,12.5,13.5,14.5]"
    CATNAMES="$(echo {bl,bt}_{neg,pos}${CATPOSTFIX} | sed 's/ /,/g')"
    else
    CATFUNC="ttH_catIndex_3l_SVA(LepGood1_charge,LepGood2_charge,LepGood3_charge,nJet25)"
    CATBINS="[10.5,11.5,12.5,13.5,14.5]"
    CATNAMES="$(echo {lj,hj}_{neg,pos}${CATPOSTFIX} | sed 's/ /,/g')"
    fi

    python makeShapeCardsNew.py ${DOFILE} ttH-multilepton/mca-3l-${MCASUFFIX}${SPLITDECAYS}.txt ttH-multilepton/3l_tight.txt ${FUNCTION_3L} $SYSTS $OPT_3L --binname ttH_3l --categorize $CATFUNC $CATBINS $CATNAMES;

    echo "Done at $(date)"
fi

if [[ "$1" == "3l_zpeak" || "$1" == "3l_zpeak_btight" ]]; then
    test -d $ORIGIN/TREES_TTH_190418_Fall17_skim_3l_2j_2b1B_Zpeak_presc && T3L="${T3L/TREES_TTH_190418_Fall17_skim2lss3l/TREES_TTH_190418_Fall17_skim_3l_2j_2b1B_Zpeak_presc}";

    OPT_3L="${T3L} ${OPTIONS} -W vtxWeight2017*eventBTagSF*leptonSF_ttH(LepGood_pdgId[iLepFO_Recl[0]],LepGood_pt[iLepFO_Recl[0]],LepGood_eta[iLepFO_Recl[0]],3)*leptonSF_ttH(LepGood_pdgId[iLepFO_Recl[1]],LepGood_pt[iLepFO_Recl[1]],LepGood_eta[iLepFO_Recl[1]],3)*leptonSF_ttH(LepGood_pdgId[iLepFO_Recl[2]],LepGood_pt[iLepFO_Recl[2]],LepGood_eta[iLepFO_Recl[2]],3)*leptonSF_ttH(LepGood_pdgId[iLepFO_Recl[3]],LepGood_pt[iLepFO_Recl[3]],LepGood_eta[iLepFO_Recl[3]],3)*triggerSF_ttH(LepGood_pdgId[iLepFO_Recl[0]],LepGood_pt[iLepFO_Recl[0]],LepGood_pdgId[iLepFO_Recl[1]],LepGood_pt[iLepFO_Recl[1]],nLepTight_Recl,0)"
    OPT_3L="${OPT_3L} -I ^Zveto"
    CATPOSTFIX="_zpeak"
    echo "3l on-Z";

    if [[ "$1" == "3l_zpeak_btight" ]]; then
	OPT_3L="${OPT_3L} -X ^2b1B -E ^gt2b -E ^1B"
	CATPOSTFIX="${CATPOSTFIX}_btight"
	echo "asking tighter b requirements"
    fi

    if [[ "$SVA" == "false" ]]; then
    CATFUNC="ttH_catIndex_3l(LepGood1_charge,LepGood2_charge,LepGood3_charge,nBJetMedium25)"
    CATBINS="[10.5,11.5,12.5,13.5,14.5]"
    CATNAMES="$(echo {bl,bt}_{neg,pos}${CATPOSTFIX} | sed 's/ /,/g')"
    else
    CATFUNC="ttH_catIndex_3l_SVA(LepGood1_charge,LepGood2_charge,LepGood3_charge,nJet25)"
    CATBINS="[10.5,11.5,12.5,13.5,14.5]"
    CATNAMES="$(echo {lj,hj}_{neg,pos}${CATPOSTFIX} | sed 's/ /,/g')"
    fi
    python makeShapeCardsNew.py ${DOFILE} ttH-multilepton/mca-3l-${MCASUFFIX}${SPLITDECAYS}.txt ttH-multilepton/3l_tight.txt ${FUNCTION_3L} $SYSTS $OPT_3L --binname ttH_3l --categorize $CATFUNC $CATBINS $CATNAMES;

    echo "Done at $(date)"
fi

if [[ "$1" == "3l_crwz" ]]; then
    #test -d $ORIGIN/TREES_TTH_190418_Fall17_skim3l_2j_no2b1B_Zpeak_presc && T3L="${T3L/TREES_TTH_190418_Fall17_skim2lss3l/TREES_TTH_190418_Fall17_skim3l_2j_no2b1B_Zpeak_presc}";
    T3L="${T3L/3_kinMVA_withMEM_200618_v5/3_kinMVA_noMEM_200618_v5}" # MEM not needed here
    OPT_3L="${T3L} ${OPTIONS} -W vtxWeight2017*eventBTagSF*leptonSF_ttH(LepGood_pdgId[iLepFO_Recl[0]],LepGood_pt[iLepFO_Recl[0]],LepGood_eta[iLepFO_Recl[0]],3)*leptonSF_ttH(LepGood_pdgId[iLepFO_Recl[1]],LepGood_pt[iLepFO_Recl[1]],LepGood_eta[iLepFO_Recl[1]],3)*leptonSF_ttH(LepGood_pdgId[iLepFO_Recl[2]],LepGood_pt[iLepFO_Recl[2]],LepGood_eta[iLepFO_Recl[2]],3)*leptonSF_ttH(LepGood_pdgId[iLepFO_Recl[3]],LepGood_pt[iLepFO_Recl[3]],LepGood_eta[iLepFO_Recl[3]],3)*triggerSF_ttH(LepGood_pdgId[iLepFO_Recl[0]],LepGood_pt[iLepFO_Recl[0]],LepGood_pdgId[iLepFO_Recl[1]],LepGood_pt[iLepFO_Recl[1]],nLepTight_Recl,0)"
    OPT_3L="${OPT_3L} -I ^Zveto -I ^2b1B"
    echo "3l WZ";

    python makeShapeCardsNew.py ${DOFILE} ttH-multilepton/mca-3l-${MCASUFFIX}${SPLITDECAYS}.txt ttH-multilepton/3l_tight.txt ${ONEBIN} $SYSTS $OPT_3L --binname ttH_3l_crwz;

    echo "Done at $(date)"
fi

if [[ "$1" == "all" || "$1" == "4l" || "$1" == "4l_crzz"  ]]; then
    OPT_4L="${T4L} ${OPTIONS} -W vtxWeight2017*leptonSF_ttH(LepGood_pdgId[iLepFO_Recl[0]],LepGood_pt[iLepFO_Recl[0]],LepGood_eta[iLepFO_Recl[0]],3)*leptonSF_ttH(LepGood_pdgId[iLepFO_Recl[1]],LepGood_pt[iLepFO_Recl[1]],LepGood_eta[iLepFO_Recl[1]],3)*leptonSF_ttH(LepGood_pdgId[iLepFO_Recl[2]],LepGood_pt[iLepFO_Recl[2]],LepGood_eta[iLepFO_Recl[2]],3)*leptonSF_ttH(LepGood_pdgId[iLepFO_Recl[3]],LepGood_pt[iLepFO_Recl[3]],LepGood_eta[iLepFO_Recl[3]],3)*triggerSF_ttH(LepGood_pdgId[iLepFO_Recl[0]],LepGood_pt[iLepFO_Recl[0]],LepGood_pdgId[iLepFO_Recl[1]],LepGood_pt[iLepFO_Recl[1]],nLepTight_Recl,0)*eventBTagSF"
    CATPOSTFIX=""

    if [[ "$1" == "4l_crzz" ]]; then
        OPT_4L="${OPT_4L} -I ^Zveto -I ^2b1B"
        CATPOSTFIX="_crzz";
    fi;

    echo "4l${CATPOSTFIX}";
    python makeShapeCardsNew.py ${DOFILE} ttH-multilepton/mca-4l-${MCASUFFIX}${SPLITDECAYS}.txt ttH-multilepton/4l_tight.txt ${ONEBIN} $SYSTS $OPT_4L --binname ttH_4l${CATPOSTFIX};

   echo "Done at $(date)"
fi


