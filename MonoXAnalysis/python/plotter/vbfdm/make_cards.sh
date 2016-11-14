#!/bin/bash

if [[ "$HOSTNAME" == "cmsphys06" ]]; then
    TBASE="/data1/emanuele/monox/";
    J=6;
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

OPTIONS=" --s2v -j $J -l ${LUMI} -f -X trigger "
test -d $OUTNAME || mkdir -p $OUTNAME
OPTIONS="${OPTIONS} --od cards/$OUTNAME ";

SYST="vbfdm/systsEnv.txt"

VARIABLE="'abs(JetClean1_eta-JetClean2_eta)' '[0,0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,6,10]'"

if [[ "$2" == "save" ]]; then
DOFILE="--savefile activate"
fi
if [[ "$2" == "read" ]]; then
DOFILE="--infile activate"
fi

if [[ "$1" == "all" || "$1" == "SR" ]] ; then
    OPTIONS_SR="${OPTIONS} -P \"$TREEMET\" -F mjvars/t \"$TREEMET/friends/evVarFriend_{cname}.root\" --FMC sf/t \"$TREEMET/friends/sfFriend_{cname}.root\" -W 'puw*SF_trigmetnomu*SF_BTag*SF_NLO_QCD*SF_NLO_EWK' "
    command="python makeShapeCards.py ${DOFILE} vbfdm/mca-80X-sync.txt vbfdm/vbfdm.txt ${VARIABLE} $SYST $OPTIONS_SR --od ${OUTNAME} --processesFromCR ZNuNu,W --region SR --unbinned"
    echo "===> EXECUTING " $command
    eval $command
    echo "Done at $(date)"
fi;

if [[ "$1" == "all" || "$1" == "ZM" ]] ; then
    OPTIONS_ZM="${OPTIONS} -P \"$TREEMET\" -F mjvars/t \"$TREEMET/friends/evVarFriend_{cname}.root\" --FMC sf/t \"$TREEMET/friends/sfFriend_{cname}.root\" -W 'puw*SF_trigmetnomu*SF_LepTightLoose*SF_BTag*SF_NLO_QCD*SF_NLO_EWK' "
    command="python makeShapeCards.py ${DOFILE} vbfdm/mca-80X-muonCR.txt vbfdm/zmumu.txt ${VARIABLE} $SYST $OPTIONS_ZM --od ${OUTNAME} --correlateProcessCR 'ZNuNu,SR,rfac_ZLL_full,templates/rfactors_ZNuNuSR_Over_zmumuCR.root' --region ZM --unbinned --xp ZLL,EWKZLL --appendWorkspace vbfdm.input.root"
    echo "===> EXECUTING " $command
    eval $command    
    echo "Done at $(date)"
fi;


if [[ "$1" == "all" || "$1" == "ZE" ]] ; then
    OPTIONS_ZE="${OPTIONS} -P \"$TREELEP\" -F mjvars/t \"$TREELEP/friends/evVarFriend_{cname}.root\" --FMC sf/t \"$TREELEP/friends/sfFriend_{cname}.root\" -W 'puw*SF_LepTightLoose*SF_BTag*SF_NLO_QCD*SF_NLO_EWK' "
    command="python makeShapeCards.py ${DOFILE} vbfdm/mca-80X-electronCR.txt vbfdm/zee.txt ${VARIABLE} $SYST $OPTIONS_ZE --od ${OUTNAME} --correlateProcessCR 'ZNuNu,SR,rfac_ZLL_full,templates/rfactors_ZNuNuSR_Over_zeeCR.root' --region ZE --unbinned --xp ZLL,EWKZLL --appendWorkspace vbfdm.input.root"
    echo "===> EXECUTING " $command
    eval $command    
    echo "Done at $(date)"
fi;

if [[ "$1" == "all" || "$1" == "WM" ]] ; then
    OPTIONS_WM="${OPTIONS} -P \"$TREEMET\" -F mjvars/t \"$TREEMET/friends/evVarFriend_{cname}.root\" --FMC sf/t \"$TREEMET/friends/sfFriend_{cname}.root\" -W 'puw*SF_trigmetnomu*SF_LepTight*SF_BTag*SF_NLO_QCD*SF_NLO_EWK' "
    command="python makeShapeCards.py ${DOFILE} vbfdm/mca-80X-muonCR.txt vbfdm/wmunu.txt ${VARIABLE} $SYST $OPTIONS_WM --od ${OUTNAME} --correlateProcessCR 'W,SR,rfac_W_full,templates/rfactors_WSR_Over_wmunuCR.root' --region WM --unbinned --xp W,EWKW --appendWorkspace vbfdm.input.root"
    echo "===> EXECUTING " $command
    eval $command
    echo "Done at $(date)"
fi;

if [[ "$1" == "all" || "$1" == "WE" ]] ; then
    OPTIONS_WE="${OPTIONS} -P \"$TREELEP\" -F mjvars/t \"$TREELEP/friends/evVarFriend_{cname}.root\" --FMC sf/t \"$TREELEP/friends/sfFriend_{cname}.root\" -W 'puw*SF_LepTight*SF_BTag*SF_NLO_QCD*SF_NLO_EWK' "
    command="python makeShapeCards.py ${DOFILE} vbfdm/mca-80X-electronCR.txt vbfdm/wenu.txt ${VARIABLE} $SYST $OPTIONS_WE --od ${OUTNAME} --correlateProcessCR 'W,SR,rfac_W_full,templates/rfactors_WSR_Over_wenuCR.root' --region WE --unbinned --xp W,EWKW --appendWorkspace vbfdm.input.root"
    echo "===> EXECUTING " $command
    eval $command
    echo "Done at $(date)"
fi;
