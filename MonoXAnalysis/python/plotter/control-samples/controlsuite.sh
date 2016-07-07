#!/bin/bash

DATAvsDATA=0
if [[ "$1" == "-d" ]]; then
    echo "# will do data vs data comparison "
    DATAvsDATA=1; shift;
fi;

WHAT=$1; if [[ "$1" == "" ]]; then echo "controlsuite.sh <what>"; exit 1; fi


BASEDIR="TREES_2LEPSKIM_80X"
WORKDIR="control-samples"

if [[ "$HOSTNAME" == "cmsphys06" ]]; then
    T="/data1/emanuele/monox/${BASEDIR}";
    J=8;
else
    T="/cmshome/dimarcoe/${BASEDIR}";
    J=3;
fi

MCA=""
SP="DYJets"
if [[ "$WHAT" == *"zee"* ]] ; then
    MCA="${WORKDIR}/mca-80X-Ve.txt "
    if [ "$DATAvsDATA" != "0" ] ; then
        MCA="${WORKDIR}/dta-80X-Ve.txt "
        SP="dataref"
    fi
elif [ "$WHAT" == "zmm" ] ; then
    MCA="${WORKDIR}/mca-80X-Vm.txt "
fi


ROOTPREF="plots"
ROOT="${ROOTPREF}/${WHAT}"
COREOPT="-P $T --s2v -j $J -l 0.650 "
COREY="mcAnalysis.py ${MCA} ${COREOPT}  "
COREP="mcPlots.py ${MCA} ${COREOPT} -f --poisson --showRatio --maxRatioRange 0.8 1.2 --scaleSigToData "
#FEV=" -F mjvars/t \"$T/friends/evVarFriend_{cname}.root\" "
#SF=" --FM sf/t \"$T/friends/sfFriend_{cname}.root\" "
#FULLOPT=" $FEV $SF -W 'vtxWeight*SF_trig1lep*SF_LepTightLoose' "
FEV=""
SF=""
FULLOPT=" $FEV $SF "

RUNY2M="${COREY} ${WORKDIR}/zmumu_twiki.txt "
RUNY2E="${COREY} ${WORKDIR}/zeeincl.txt "

PLOT2M="${COREP} ${WORKDIR}/zmumu_twiki.txt ${WORKDIR}/zmumu_plots.txt "
PLOT2E="${COREP} ${WORKDIR}/zeeincl.txt ${WORKDIR}/zee_incl_plots.txt "

case $WHAT in
zmumu)
        echo "python ${RUNY2MU} $FEV --sp ${SP} "
        echo "python ${PLOT2MU} $FEV --sp ${SP} --pdir plots/Z_datamc_mm "
;;
zee)
        echo "python ${RUNY2E} ${FULLOPT} --sp ${SP} "
        echo "python ${PLOT2E} ${FULLOPT} --sp ${SP} --pdir plots/Zel_inclusive "
;;
zee_bb)
        echo "python ${RUNY2E} ${FULLOPT} --sp ${SP} -A mass ebeb 'abs(LepGood1_eta) < 1.479 && abs(LepGood2_eta) < 1.479' "
        echo "python ${PLOT2E} ${FULLOPT} --sp ${SP} -A mass ebeb 'abs(LepGood1_eta) < 1.479 && abs(LepGood2_eta) < 1.479' --pdir plots/Zel_datamc_EBEB --print=pdf,png,C,root "
;;                                                                                                                                      
zee_ee)                                                                                                                                 
        echo "python ${RUNY2E} ${FULLOPT} --sp ${SP} -A mass eeee 'abs(LepGood1_eta) > 1.479 && abs(LepGood2_eta) > 1.479' "            
        echo "python ${PLOT2E} ${FULLOPT} --sp ${SP} -A mass eeee 'abs(LepGood1_eta) > 1.479 && abs(LepGood2_eta) > 1.479' --pdir plots/Zel_datamc_EEEE --print=pdf,png,C,root --rebin 2 "
;;                                                                                                                                      
zee_notebeb)                                                                                                                            
        echo "python ${RUNY2E} ${FULLOPT} --sp ${SP} -A mass notebeb '(abs(LepGood1_eta)>1.566 || abs(LepGood2_eta)>1.566)' "           
        echo "python ${PLOT2E} ${FULLOPT} --sp ${SP} -A mass notebeb '(abs(LepGood1_eta)>1.566 || abs(LepGood2_eta)>1.566)' --pdir plots/Zel_datamc_notEBEB --print=pdf,png,C,root "
;;
esac;
