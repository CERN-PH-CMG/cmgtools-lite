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

VARIABLE=""

# VARNAME="detajj_fullsel"
# if [[ "$PRESEL" == "full_sel" ]]; then 
#     VARIABLE="'abs(JetClean1_eta-JetClean2_eta)' '[1,1.5,2,2.5,3,3.5,4,4.5,5,6,10]'"
# else
#     VARIABLE="'abs(JetClean1_eta-JetClean2_eta)' '[0,0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,6,10]'"
# fi;

# VARNAME="mjj_fullsel"
# if [[ "$PRESEL" == "full_sel" ]]; then
#     VARIABLE="'mass_2(JetClean1_pt,JetClean1_eta,JetClean1_phi,0.,JetClean2_pt,JetClean2_eta,JetClean2_phi,0.)' '[300,400,500,600,700,800,900,1000,1100,1200,1300,1400,1500,1600,1700,1800,1900,2000,2250,2500,2750,3000,3500,4000]'"
# else
#     VARIABLE="'mass_2(JetClean1_pt,JetClean1_eta,JetClean1_phi,0.,JetClean2_pt,JetClean2_eta,JetClean2_phi,0.)' '[0,300,400,500,600,700,800,900,1000,1100,1200,1300,1400,1500,1600,1700,1800,1900,2000,2250,2500,2750,3000,3500,4000]'"
# fi

VARNAME="detajj_mjj_binned"
if [[ "$PRESEL" == "full_sel" ]]; then
    VARIABLE="NOTIMPL"
else
    VARIABLE="'abs(JetClean1_eta-JetClean2_eta):mass_2(JetClean1_pt,JetClean1_eta,JetClean1_phi,0.,JetClean2_pt,JetClean2_eta,JetClean2_phi,0.)' '30,0,4000,30,0,10'"
fi

test -d $OUTNAME/$PRESEL/$VARNAME || mkdir -p $OUTNAME/$PRESEL/$VARNAME

if [[ "$2" == "save" ]]; then
DOFILE="--savefile activate"
fi
if [[ "$2" == "read" ]]; then
DOFILE="--infile activate"
fi
if [[ "$2" == "twodim" ]]; then
OPTIONS="${OPTIONS} --2d-binning-function 10:vbfdm_2Dto1D"
fi

if [[ "$1" == "all" || "$1" == "SR" ]] ; then
    OPTIONS_SR="${OPTIONS} -P \"$TREEMET\" -F mjvars/t \"$TREEMET/friends/evVarFriend_{cname}.root\" --FMC sf/t \"$TREEMET/friends/sfFriend_{cname}.root\" -W 'puw*SF_trigmetnomu*SF_BTag*SF_NLO_QCD*SF_NLO_EWK' "
    command="python makeShapeCards.py ${DOFILE} vbfdm/mca-80X-sync.txt vbfdm/vbfdm.txt ${VARIABLE} $SYST $OPTIONS_SR --od ${OUTNAME}/${PRESEL}/$VARNAME --processesFromCR ZNuNu,W --region SR --unbinned"
    echo "===> EXECUTING " $command
    eval $command
    echo "Done at $(date)"
fi;

if [[ "$1" == "all" || "$1" == "ZM" ]] ; then
    OPTIONS_ZM="${OPTIONS} -P \"$TREEMET\" -F mjvars/t \"$TREEMET/friends/evVarFriend_{cname}.root\" --FMC sf/t \"$TREEMET/friends/sfFriend_{cname}.root\" -W 'puw*SF_trigmetnomu*SF_LepTightLoose*SF_BTag*SF_NLO_QCD*SF_NLO_EWK' "
    command="python makeShapeCards.py ${DOFILE} vbfdm/mca-80X-muonCR.txt vbfdm/zmumu.txt ${VARIABLE} $SYST $OPTIONS_ZM --od ${OUTNAME}/${PRESEL}/$VARNAME --correlateProcessCR 'ZNuNu,SR,rfac_ZLL_full,templates/${PRESEL}/rfactors_${VARNAME}_ZNuNuSR_Over_ZMCR.root' --region ZM --unbinned --xp ZLL,EWKZLL --appendWorkspace vbfdm.input.root"
    echo "===> EXECUTING " $command
    eval $command    
    echo "Done at $(date)"
fi;


if [[ "$1" == "all" || "$1" == "ZE" ]] ; then
    OPTIONS_ZE="${OPTIONS} -P \"$TREELEP\" -F mjvars/t \"$TREELEP/friends/evVarFriend_{cname}.root\" --FMC sf/t \"$TREELEP/friends/sfFriend_{cname}.root\" -W 'puw*SF_LepTightLoose*SF_BTag*SF_NLO_QCD*SF_NLO_EWK' "
    command="python makeShapeCards.py ${DOFILE} vbfdm/mca-80X-electronCR.txt vbfdm/zee.txt ${VARIABLE} $SYST $OPTIONS_ZE --od ${OUTNAME}/${PRESEL}/$VARNAME --correlateProcessCR 'ZNuNu,SR,rfac_ZLL_full,templates/${PRESEL}/rfactors_${VARNAME}_ZNuNuSR_Over_ZECR.root' --region ZE --unbinned --xp ZLL,EWKZLL --appendWorkspace vbfdm.input.root"
    echo "===> EXECUTING " $command
    eval $command    
    echo "Done at $(date)"
fi;

if [[ "$1" == "all" || "$1" == "WM" ]] ; then
    OPTIONS_WM="${OPTIONS} -P \"$TREEMET\" -F mjvars/t \"$TREEMET/friends/evVarFriend_{cname}.root\" --FMC sf/t \"$TREEMET/friends/sfFriend_{cname}.root\" -W 'puw*SF_trigmetnomu*SF_LepTight*SF_BTag*SF_NLO_QCD*SF_NLO_EWK' "
    command="python makeShapeCards.py ${DOFILE} vbfdm/mca-80X-muonCR.txt vbfdm/wmunu.txt ${VARIABLE} $SYST $OPTIONS_WM --od ${OUTNAME}/${PRESEL}/$VARNAME --correlateProcessCR 'W,SR,rfac_W_full,templates/${PRESEL}/rfactors_${VARNAME}_WSR_Over_WMCR.root' --region WM --unbinned --xp W,EWKW --appendWorkspace vbfdm.input.root"
    echo "===> EXECUTING " $command
    eval $command
    echo "Done at $(date)"
fi;

if [[ "$1" == "all" || "$1" == "WE" ]] ; then
    OPTIONS_WE="${OPTIONS} -P \"$TREELEP\" -F mjvars/t \"$TREELEP/friends/evVarFriend_{cname}.root\" --FMC sf/t \"$TREELEP/friends/sfFriend_{cname}.root\" -W 'puw*SF_LepTight*SF_BTag*SF_NLO_QCD*SF_NLO_EWK' "
    command="python makeShapeCards.py ${DOFILE} vbfdm/mca-80X-electronCR.txt vbfdm/wenu.txt ${VARIABLE} $SYST $OPTIONS_WE --od ${OUTNAME}/${PRESEL}/$VARNAME --correlateProcessCR 'W,SR,rfac_W_full,templates/${PRESEL}/rfactors_${VARNAME}_WSR_Over_WECR.root' --region WE --unbinned --xp W,EWKW --appendWorkspace vbfdm.input.root"
    echo "===> EXECUTING " $command
    eval $command
    echo "Done at $(date)"
fi;

