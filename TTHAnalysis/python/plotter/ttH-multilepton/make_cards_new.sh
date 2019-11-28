#!/bin/bash

TREES_ZERO=NanoTrees_TTH_300519_v5pre_skim2LSS

case $HOSTNAME in
    cmsco01.cern.ch) ORIGIN=/data/peruzzi; J=8 ;;
    cmsphys10) ORIGIN=/data1/g/gpetrucc; J=8 ;;
    gpetrucc-vm2.cern.ch) ORIGIN=/data/gpetrucc; J=4 ;;
    fanae*) ORIGIN=/pool/cienciasrw/userstorage/sscruz/NanoAOD/; J=64;;
    gae*) ORIGIN=/pool/cienciasrw/userstorage/sscruz/NanoAOD/; J=64;;
    *)
        ORIGIN=/afs/cern.ch/work/p/peruzzi; J=1
        test -d /tmp/$USER/TREES_TTH_190418_Fall17_skim2lss3l && ORIGIN=/tmp/$USER;;
esac;
#if test -d $ORIGIN/TREES_TTH_190418_Fall17_skim4l ; then
#    T4L=${T4L/TREES_TTH_190418_Fall17_skim2lss3l/TREES_TTH_190418_Fall17_skim4l};
#fi

if [[ "X$1" == "X" ]]; then echo "Provide output directory name!"; exit; fi
OUTNAME=$1; shift;
if [[ "X$1" == "X" ]]; then echo "Provide year!"; exit; fi
YEAR="$1"; shift
case $YEAR in
    2016) LUMI="35.9";;
    2017) LUMI="41.4";;
    2018) LUMI="59.7";;
    *) echo "Wrong year" $YEAR;;
esac
echo "Normalizing to ${LUMI}/fb";
OPTIONS=" --tree NanoAOD --s2v -j $J -l ${LUMI} -f --WA prescaleFromSkim --split-factor=-1 "
test -d cards/$OUTNAME || mkdir -p cards/$OUTNAME
OPTIONS="${OPTIONS} --od cards/$OUTNAME ";

T2L="-P $ORIGIN/NanoTrees_TTH_091019_v6pre_skim2lss/${YEAR} --FMCs {P}/0_jmeUnc_v1  --Fs  {P}/1_recl/ --FMCs {P}/2_scalefactors --Fs {P}/3_tauCount --Fs {P}/6_mva3l_new --Fs {P}/6_mva2lss_new --xf TTTW --xf TTWH"
T3L=${T2L}
T4L=${T2L}


SYSTS="--unc ttH-multilepton/systsUnc.txt --amc"
case $1 in
--bbb)
    shift;
    SYSTS="--unc ttH-multilepton/systsUnc.txt --bbb CMS_ttHl17_templstat";;
esac;
BLoose=" -E ^BLoose "
BTight=" -E ^BTight "

SPLITDECAYS=""
SPLITDECAYS="-splitdecays"

PROMPTSUB="--plotgroup data_fakes+=.*_promptsub"
echo "We are using the asimov dataset"
OPTIONS="${OPTIONS} -L ttH-multilepton/functionsTTH.cc --mcc ttH-multilepton/lepchoice-ttH-FO.txt --mcc ttH-multilepton/mcc-METFixEE2017.txt ${PROMPTSUB} --neg --asimov signal" # neg necessary for subsequent rebin
CATPOSTFIX=""

FUNCTION_2L="ttH_catIndex_2lss_MVA(LepGood1_pdgId,LepGood2_pdgId,DNN_2lss_predictions_ttH,DNN_2lss_predictions_ttW,DNN_2lss_predictions_tHQ,DNN_2lss_predictions_Rest)"
FUNCTION_3L="ttH_catIndex_3l_MVA(DNN_3l_predictions_ttH,DNN_3l_predictions_tH,DNN_3l_predictions_rest,LepGood1_pdgId,LepGood2_pdgId,LepGood3_pdgId,nBJetMedium25)"
FUNCTION_CR_3L='ttH_3l_clasifier(nJet25,nBJetMedium25) [0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5,10.5,11.5,12.5] '
FUNCTION_CR_4L="ttH_4l_clasifier(nJet25,nBJetMedium25,mZ2) [0.5,1.5,2.5,3.5,4.5] "
FUNCTION_SVA_2L="mass_2(LepGood1_conePt,LepGood1_eta,LepGood1_phi,LepGood1_mass,LepGood2_conePt,LepGood2_eta,LepGood2_phi,LepGood2_mass) [10.0,50.0,70.0,80.0,90.0,110.0,140.0,190.0,400.0]"
FUNCTION_SVA_3L="mass_3_cheap(LepGood1_pt,LepGood1_eta,LepGood2_pt,LepGood2_eta,LepGood2_phi-LepGood1_phi,LepGood3_pt,LepGood3_eta,LepGood3_phi-LepGood1_phi) [26.0,107.0,146.0,193.0,261.0,400.0]"
ONEBIN="1 1,0.5,1.5"
echo "${FUNCTION_CR_3L}"
MCASUFFIX="mcdata-frdata"
SVA="true"
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
    OPT_2L="${T2L} ${OPTIONS} -W puWeight*btagSF_shape*leptonSF_2lss*triggerSF_2lss"
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

    for ch in ee em mm; do 
	for node in Rest tHQ ttH ttW; do 
	    CATNAME=${ch}_${node}node
	    if [[ "$CATNAME" == "ee_ttHnode" ]]; then
		CATBINS="[0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5]"
		CUT="${FUNCTION_2L} > 0 && ${FUNCTION_2L} < 9"
	    elif [[ "$CATNAME" == "ee_Restnode" ]]; then
		CATBINS="[8.5,9.5,10.5,11.5,12.5,13.5,14.5,15.5,16.5,17.5,18.5,19.5,20.5,21.5]"
		CUT="${FUNCTION_2L} > 8 && ${FUNCTION_2L} < 22"
	    elif [[ "$CATNAME" == "ee_ttWnode" ]]; then
		CATBINS="[21.5,22.5,23.5,24.5,25.5,26.5,27.5,28.5,29.5,30.5,31.5,32.5]"
		CUT="${FUNCTION_2L} > 21 && ${FUNCTION_2L} < 33"
	    elif [[ "$CATNAME" == "ee_tHQnode" ]]; then
		CATBINS="[32.5,33.5,34.5,35.5,36.5,37.5,38.5,39.5,40.5]"
		CUT="${FUNCTION_2L} > 32 && ${FUNCTION_2L} < 41"
	    elif [[ "$CATNAME" == "em_ttHnode" ]]; then
		CATBINS="[40.5,41.5,42.5,43.5,44.5,45.5]"
		CUT="${FUNCTION_2L} > 40 && ${FUNCTION_2L} < 46"
	    elif [[ "$CATNAME" == "em_Restnode" ]]; then
		CATBINS="[45.5,46.5,47.5,48.5,49.5,50.5,51.5,52.5,53.5,54.5,55.5,56.5]"
		CUT="${FUNCTION_2L} > 45 && ${FUNCTION_2L} < 57"
	    elif [[ "$CATNAME" == "em_ttWnode" ]]; then
		CATBINS="[56.5,57.5,58.5,59.5,60.5,61.5,62.5,63.5,64.5,65.5,66.5,67.5]"
		CUT="${FUNCTION_2L} > 56 && ${FUNCTION_2L} < 68"
	    elif [[ "$CATNAME" == "em_tHQnode" ]]; then
		CATBINS="[67.5,68.5,69.5,70.5,71.5,72.5,73.5,74.5]"
		CUT="${FUNCTION_2L} > 67&& ${FUNCTION_2L} < 75"
	    elif [[ "$CATNAME" == "mm_ttHnode" ]]; then
		CATBINS="[74.5,75.5,76.5,77.5,78.5,79.5,80.5,81.5,82.5,83.5,84.5]"
		CUT="${FUNCTION_2L} > 74 && ${FUNCTION_2L} < 85"
	    elif [[ "$CATNAME" == "mm_Restnode" ]]; then
		CATBINS="[84.5,85.5,86.5,87.5,88.5,89.5,90.5,91.5,92.5,93.5,94.5]"
		CUT="${FUNCTION_2L} > 84 && ${FUNCTION_2L} < 95"
	    elif [[ "$CATNAME" == "mm_ttWnode" ]]; then
		CATBINS="[94.5,95.5,96.5,97.5,98.5,99.5,100.5,101.5,102.5,103.5,104.5,105.5,106.5,107.5]"
		CUT="${FUNCTION_2L} > 94 && ${FUNCTION_2L} < 108"
	    elif [[ "$CATNAME" == "mm_tHQnode" ]]; then
		CATBINS="[107.5,108.5,109.5,110.5,111.5]"
		CUT="${FUNCTION_2L} > 107 && ${FUNCTION_2L} < 112"
	    else
		echo Unknown category $CATNAME
	    fi
	    
	    python makeShapeCardsNew.py ${DOFILE} ttH-multilepton/mca-2lss-${MCASUFFIX}${SPLITDECAYS}.txt ttH-multilepton/2lss_tight_legacy.txt ${FUNCTION_2L} "$CATBINS" $SYSTS $OPT_2L --binname ttH_2lss_0tau_${ch}_${node}node_${YEAR} --year ${YEAR} -A ^alwaystrue regcut "${CUT}";
	done 
    done

    echo "Done at $(date)"

fi

if [[ "$1" == "all" || "$1" == "3l" ]]; then
    test -d $ORIGIN/TREES_TTH_190418_Fall17_skim_3l_2j_2b1B_Zveto_presc && T3L="${T3L/TREES_TTH_190418_Fall17_skim2lss3l/TREES_TTH_190418_Fall17_skim_3l_2j_2b1B_Zveto_presc}";
    OPT_3L="${T3L} ${OPTIONS} -W puWeight*btagSF_shape*triggerSF_3l*leptonSF_3l"
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
    
    
    for CATNAME in ttH_bl ttH_bt tH_bl tH_bt rest_eee rest_eem_bl rest_eem_bt rest_emm_bl rest_emm_bt rest_mmm_bl rest_mmm_bt; do 
	if [[ "$CATNAME" == "ttH_bl" ]]; then
	    CATBINS="[0.5,1.5,2.5,3.5,4.5,5.5]"
	    CUT="${FUNCTION_3L} > 0 && ${FUNCTION_3L} < 6"
	elif [[ "$CATNAME" == "ttH_bt" ]]; then
	    CATBINS="[5.5,6.5,7.5,8.5,9.5]"
	    CUT="${FUNCTION_3L} > 5 && ${FUNCTION_3L} < 10"
	elif [[ "$CATNAME" == "tH_bl" ]]; then
	    CATBINS="[9.5,10.5,11.5,12.5,13.5,14.5,15.5,16.5]"
	    CUT="${FUNCTION_3L} > 9 && ${FUNCTION_3L} < 17"
	elif [[ "$CATNAME" == "tH_bt" ]]; then
	    CATBINS="[16.5,17.5,18.5,19.5]"
	    CUT="${FUNCTION_3L} > 16 && ${FUNCTION_3L} < 20"
	elif [[ "$CATNAME" == "rest_eee" ]]; then
	    CATBINS="[19.5,20.5]"
	    CUT="${FUNCTION_3L} > 19 && ${FUNCTION_3L} < 21"
	elif [[ "$CATNAME" == "rest_eem_bl" ]]; then
	    CATBINS="[20.5,21.5,22.5,23.5,24.5]"
	    CUT="${FUNCTION_3L} > 20 && ${FUNCTION_3L} < 25"
	elif [[ "$CATNAME" == "rest_eem_bt" ]]; then
	    CATBINS="[24.5,25.5]"
	    CUT="${FUNCTION_3L} > 24 && ${FUNCTION_3L} < 26"
	elif [[ "$CATNAME" == "rest_emm_bl" ]]; then
	    CATBINS="[25.5,26.5,27.5,28.5,29.5]"
	    CUT="${FUNCTION_3L} > 25 && ${FUNCTION_3L} < 30"
	elif [[ "$CATNAME" == "rest_emm_bt" ]]; then
	    CATBINS="[29.5,30.5]"
	    CUT="${FUNCTION_3L} > 29 && ${FUNCTION_3L} < 31"
	elif [[ "$CATNAME" == "rest_mmm_bl" ]]; then
	    CATBINS="[30.5,31.5,32.5,33.5]"
	    CUT="${FUNCTION_3L} > 30 && ${FUNCTION_3L} < 34"
	elif [[ "$CATNAME" == "rest_mmm_bt" ]]; then
	    CATBINS="[30.5,34.5]"
	    CUT="${FUNCTION_3L} > 33 && ${FUNCTION_3L} < 35"
	else
	    echo "Unkown sr" $CATNAME
	fi
	# sbatch -c 8 --wrap '
	python makeShapeCardsNew.py ${DOFILE} ttH-multilepton/mca-3l-${MCASUFFIX}${SPLITDECAYS}.txt ttH-multilepton/3l_tight_legacy.txt ${FUNCTION_3L} "$CATBINS" $SYSTS $OPT_3L --binname ttH_3l_0tau_${CATNAME}_${YEAR} --year ${YEAR}  -A ^alwaystrue regcut "${CUT}"
    done

    echo "Done at $(date)"
fi

if [[ "$1" == "3l_zpeak" || "$1" == "3l_zpeak_btight" ]]; then
    test -d $ORIGIN/TREES_TTH_190418_Fall17_skim_3l_2j_2b1B_Zpeak_presc && T3L="${T3L/TREES_TTH_190418_Fall17_skim2lss3l/TREES_TTH_190418_Fall17_skim_3l_2j_2b1B_Zpeak_presc}";

    OPT_3L="${T3L} ${OPTIONS} -W puWeight*btagSF_shape*leptonSF_3l*triggerSF_3l"
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
    python makeShapeCardsNew.py ${DOFILE} ttH-multilepton/mca-3l-${MCASUFFIX}${SPLITDECAYS}.txt ttH-multilepton/3l_tight.txt ${FUNCTION_3L} $SYSTS $OPT_3L --binname ttH_3l_${YEAR} --categorize $CATFUNC $CATBINS $CATNAMES --year ${YEAR};

    echo "Done at $(date)"
fi

if [[ "$1" == "3l_crwz" ]]; then
    #test -d $ORIGIN/TREES_TTH_190418_Fall17_skim3l_2j_no2b1B_Zpeak_presc && T3L="${T3L/TREES_TTH_190418_Fall17_skim2lss3l/TREES_TTH_190418_Fall17_skim3l_2j_no2b1B_Zpeak_presc}";
    T3L="${T3L/3_kinMVA_withMEM_200618_v5/3_kinMVA_noMEM_200618_v5}" # MEM not needed here
    OPT_3L="${T3L} ${OPTIONS} -W puWeight*btagSF_shape*leptonSF_3l*triggerSF_3l"
    OPT_3L="${OPT_3L} -I ^Zveto -I ^2b1B"
    echo "3l WZ";

    python makeShapeCardsNew.py ${DOFILE} ttH-multilepton/mca-3l-${MCASUFFIX}${SPLITDECAYS}.txt ttH-multilepton/3l_tight.txt ${ONEBIN} $SYSTS $OPT_3L --binname ttH_3l_crwz_${YEAR} --year ${YEAR};

    echo "Done at $(date)"
fi

if [[ "$1" == "all" || "$1" == "4l" || "$1" == "4l_crzz"  ]]; then
    OPT_4L="${T4L} ${OPTIONS} -W puWeight*btagSF_shape*leptonSF_4l*triggerSF_3l"
    CATPOSTFIX=""

    if [[ "$1" == "4l_crzz" ]]; then
        OPT_4L="${OPT_4L} -I ^Zveto -I ^2b1B"
        CATPOSTFIX="_crzz";
    fi;

    echo "4l${CATPOSTFIX}";
    python makeShapeCardsNew.py ${DOFILE} ttH-multilepton/mca-4l-${MCASUFFIX}${SPLITDECAYS}.txt ttH-multilepton/4l_tight.txt ${ONEBIN} $SYSTS $OPT_4L --binname ttH_4l${CATPOSTFIX}_${YEAR} --year ${YEAR};

   echo "Done at $(date)"
fi

if [[ "$1" == "all" || "$1" == "cr_4l"  ]]; then
    OPT_4L="${T4L} ${OPTIONS} -W puWeight*btagSF_shape*leptonSF_4l*triggerSF_3l"
    CATPOSTFIX=""


    OPT_4L="${OPT_4L} -I ^Zveto -X ^2j -X ^2b1B -E ^underflowVeto4l" 
    CATPOSTFIX="_cr";


    echo "4l${CATPOSTFIX}";
    python makeShapeCardsNew.py ${DOFILE} ttH-multilepton/mca-4l-${MCASUFFIX}${SPLITDECAYS}.txt ttH-multilepton/4l_tight.txt ${FUNCTION_CR_4L} $SYSTS $OPT_4L --binname ttH${CATPOSTFIX}_${YEAR} --year ${YEAR};

   echo "Done at $(date)"
fi

if [[ "$1" == "all" || "$1" == "cr_3l" ]]; then
    OPT_3L="${T3L} ${OPTIONS} -W puWeight*btagSF_shape*triggerSF_3l*leptonSF_3l"
    CATPOSTFIX="_cr"
    OPT_3L="${OPT_3L} -I ^Zveto -X ^2j -X ^2b1B -E ^underflowVeto3l"
    CATFUNC="ttH_3l_ifflav(LepGood1_pdgId,LepGood2_pdgId,LepGood3_pdgId)"
    CATBINS="[0.5,1.5,2.5,3.5,4.5]"
    CATNAMES="$(echo {eee,eem,emm,mmm}${CATPOSTFIX} | sed 's/ /,/g')"
    python makeShapeCardsNew.py ${DOFILE} ttH-multilepton/mca-3l-${MCASUFFIX}${SPLITDECAYS}.txt ttH-multilepton/3l_tight.txt ${FUNCTION_CR_3L} $SYSTS $OPT_3L --binname ttH_cr_3l_${YEAR} --categorize $CATFUNC $CATBINS $CATNAMES --year ${YEAR};

    echo "Done at $(date)"
fi

