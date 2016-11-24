#!/bin/bash

if [[ "$HOSTNAME" == "cmsphys06" ]]; then
    TBASE="/data1/emanuele/monox/";
    J=6;
elif [[ "$HOSTNAME" == "pccmsrm29.cern.ch" ]]; then
    TBASE="/u2/emanuele/";
    J=4;
else
    TBASE="/afs/cern.ch/work/e/emanuele/TREES/";
    J=4;
fi

METSKIM="TREES_MET_80X_V4"
LEPSKIM="TREES_1LEP_80X_V4"

TREEMET="${TBASE}/$METSKIM"
TREELEP="${TBASE}/$LEPSKIM"

if [[ "X$1" == "X" ]]; then echo "Provide output directory name!"; exit; fi
OUTNAME=$1; shift;
echo "output will go into ${OUTNAME} "
if [[ "X$1" == "X" ]]; then echo "Provide luminosity!"; exit; fi
LUMI="$1"; shift
echo "Normalizing to ${LUMI}/fb";
if [[ "X$1" == "X" ]]; then echo "Provide selection step!"; exit; fi
PRESEL="$1"; shift
echo "Using inputs for preselection ${PRESEL}";

OPTIONS=" --s2v -j $J -l ${LUMI} -f -X trigger -U ${PRESEL} "

SYST="vbfdm/systsEnv.txt"

OPTIONS_TFSR="--P_SR \"$TREEMET\" --F_SR mjvars/t \"$TREEMET/friends_SR/evVarFriend_{cname}.root\" --FMC_SR sf/t \"$TREEMET/friends/sfFriend_{cname}.root\" --W_SR 'puw*SF_trigmetnomu*SF_BTag*SF_NLO_QCD*SF_NLO_EWK' "
if [[ "$1" == "alltf" || "$1" == "ZMtf" ]] ; then
    OPTIONS_TFCR="--P_CR \"$TREEMET\" --F_CR mjvars/t \"$TREEMET/friends_VM/evVarFriend_{cname}.root\" --FMC_CR sf/t \"$TREEMET/friends/sfFriend_{cname}.root\" --W_CR 'puw*SF_trigmetnomu*SF_LepTightLoose*SF_BTag*SF_NLO_QCD*SF_NLO_EWK' "
    command="python countingTransferFactor.py vbfdm/mca-80X-sync.txt vbfdm/vbfdm.txt vbfdm/mca-80X-muonCR.txt vbfdm/zmumu.txt $OPTIONS $OPTIONS_TFSR $OPTIONS_TFCR 'ZNuNu' 'ZLL' 'ZM' -w 'countingTFs.txt' -o w "
    echo "===> EXECUTING " $command
    eval $command
    echo "Done at $(date)"
fi;

if [[ "$1" == "alltf" || "$1" == "WMtf" ]] ; then
    OPTIONS_TFCR="--P_CR \"$TREEMET\" --F_CR mjvars/t \"$TREEMET/friends_VM/evVarFriend_{cname}.root\" --FMC_CR sf/t \"$TREEMET/friends/sfFriend_{cname}.root\" --W_CR 'puw*SF_trigmetnomu*SF_LepTight*SF_BTag*SF_NLO_QCD*SF_NLO_EWK' "
    command="python countingTransferFactor.py vbfdm/mca-80X-sync.txt vbfdm/vbfdm.txt vbfdm/mca-80X-muonCR.txt vbfdm/wmunu.txt $OPTIONS $OPTIONS_TFSR $OPTIONS_TFCR 'W' 'W' 'WM' -w 'countingTFs.txt' -o a "
    echo "===> EXECUTING " $command
    eval $command
    echo "Done at $(date)"
fi;

if [[ "$1" == "alltf" || "$1" == "ZEtf" ]] ; then
    OPTIONS_TFCR="--P_CR \"$TREELEP\" --F_CR mjvars/t \"$TREELEP/friends_VE/evVarFriend_{cname}.root\" --FMC_CR sf/t \"$TREELEP/friends/sfFriend_{cname}.root\" --W_CR 'puw*SF_LepTightLoose*SF_BTag*SF_NLO_QCD*SF_NLO_EWK' "
    command="python countingTransferFactor.py vbfdm/mca-80X-sync.txt vbfdm/vbfdm.txt vbfdm/mca-80X-electronCR.txt vbfdm/zee.txt $OPTIONS $OPTIONS_TFSR $OPTIONS_TFCR 'ZNuNu' 'ZLL' 'ZE' -w 'countingTFs.txt' -o a "
    echo "===> EXECUTING " $command
    eval $command
    echo "Done at $(date)"
fi;

if [[ "$1" == "alltf" || "$1" == "WEtf" ]] ; then
    OPTIONS_TFCR="--P_CR \"$TREELEP\" --F_CR mjvars/t \"$TREELEP/friends_VE/evVarFriend_{cname}.root\" --FMC_CR sf/t \"$TREELEP/friends/sfFriend_{cname}.root\" --W_CR 'puw*SF_LepTight*SF_BTag*SF_NLO_QCD*SF_NLO_EWK' "
    command="python countingTransferFactor.py vbfdm/mca-80X-sync.txt vbfdm/vbfdm.txt vbfdm/mca-80X-electronCR.txt vbfdm/wenu.txt $OPTIONS $OPTIONS_TFSR $OPTIONS_TFCR 'W' 'W' 'WE' -w 'countingTFs.txt' -o a "
    echo "===> EXECUTING " $command
    eval $command
    echo "Done at $(date)"
fi;



# make cards
if [[ "$1" == "allcards" || "$1" == "ZM" ]] ; then
    OPTIONS_ZM="${OPTIONS} -P \"$TREEMET\" -F mjvars/t \"$TREEMET/friends_VM/evVarFriend_{cname}.root\" --FMC sf/t \"$TREEMET/friends/sfFriend_{cname}.root\" -W 'puw*SF_trigmetnomu*SF_LepTightLoose*SF_BTag*SF_NLO_QCD*SF_NLO_EWK' "
    command="python makeCountingCards.py ${DOFILE} vbfdm/mca-80X-muonCR.txt vbfdm/zmumu.txt $SYST $OPTIONS_ZM --od ${OUTNAME}/${PRESEL}/$VARNAME --correlateProcessCR 'ZNuNu,ZLL,ZM,countingTFs.txt'"
    echo "===> EXECUTING " $command
    eval $command
    echo "Done at $(date)"
fi;

if [[ "$1" == "allcards" || "$1" == "WM" ]] ; then
    OPTIONS_WM="${OPTIONS} -P \"$TREEMET\" -F mjvars/t \"$TREEMET/friends_VM/evVarFriend_{cname}.root\" --FMC sf/t \"$TREEMET/friends/sfFriend_{cname}.root\" -W 'puw*SF_trigmetnomu*SF_LepTight*SF_BTag*SF_NLO_QCD*SF_NLO_EWK' "
    command="python makeCountingCards.py ${DOFILE} vbfdm/mca-80X-muonCR.txt vbfdm/wmunu.txt $SYST $OPTIONS_WM --od ${OUTNAME}/${PRESEL}/$VARNAME --correlateProcessCR 'W,W,WM,countingTFs.txt'"
    echo "===> EXECUTING " $command
    eval $command
    echo "Done at $(date)"
fi;

if [[ "$1" == "allcards" || "$1" == "ZE" ]] ; then
    OPTIONS_ZE="${OPTIONS} -P \"$TREELEP\" -F mjvars/t \"$TREELEP/friends_VE/evVarFriend_{cname}.root\" --FMC sf/t \"$TREELEP/friends/sfFriend_{cname}.root\" -W 'puw*SF_LepTightLoose*SF_BTag*SF_NLO_QCD*SF_NLO_EWK' "
    command="python makeCountingCards.py ${DOFILE} vbfdm/mca-80X-electronCR.txt vbfdm/zee.txt $SYST $OPTIONS_ZE --od ${OUTNAME}/${PRESEL}/$VARNAME --correlateProcessCR 'ZNuNu,ZLL,ZE,countingTFs.txt'"
    echo "===> EXECUTING " $command
    eval $command
    echo "Done at $(date)"
fi;

if [[ "$1" == "allcards" || "$1" == "WE" ]] ; then
    OPTIONS_WE="${OPTIONS} -P \"$TREELEP\" -F mjvars/t \"$TREELEP/friends_VE/evVarFriend_{cname}.root\" --FMC sf/t \"$TREELEP/friends/sfFriend_{cname}.root\" -W 'puw*SF_LepTight*SF_BTag*SF_NLO_QCD*SF_NLO_EWK' "
    command="python makeCountingCards.py ${DOFILE} vbfdm/mca-80X-electronCR.txt vbfdm/wenu.txt $SYST $OPTIONS_WE --od ${OUTNAME}/${PRESEL}/$VARNAME --correlateProcessCR 'W,W,WE,countingTFs.txt'"
    echo "===> EXECUTING " $command
    eval $command
    echo "Done at $(date)"
fi;

if [[ "$1" == "allcards" || "$1" == "SR" ]] ; then
    OPTIONS_SR="${OPTIONS} -P \"$TREEMET\" -F mjvars/t \"$TREEMET/friends_VM/evVarFriend_{cname}.root\" --FMC sf/t \"$TREEMET/friends/sfFriend_{cname}.root\" -W 'puw*SF_trigmetnomu*SF_LepTight*SF_BTag*SF_NLO_QCD*SF_NLO_EWK' "
    command="python makeCountingCards.py ${DOFILE} vbfdm/mca-80X-sync.txt vbfdm/vbfdm.txt $SYST $OPTIONS_SR --od ${OUTNAME}/${PRESEL}/$VARNAME"
    echo "===> EXECUTING " $command
    eval $command
    echo "Done at $(date)"
fi;
