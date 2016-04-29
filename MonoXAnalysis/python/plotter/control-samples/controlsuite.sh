#!/bin/bash

WHAT=$1; if [[ "$1" == "" ]]; then echo "monojet.sh <what>"; exit 1; fi

WHAT=$1; if [[ "$1" == "" ]]; then echo "monojet.sh <what>"; exit 1; fi


BASEDIR="TREES_25ns_2LEPSKIM_76X"

WORKDIR="control-samples"

if [[ "$HOSTNAME" == "cmsphys06" ]]; then
    T="/data1/emanuele/monox/${BASEDIR}";
    J=8;
else
    T="/cmshome/dimarcoe/${BASEDIR}";
    J=3;
fi

MCA=""
if [ "$WHAT" == "zee" ] ; then
    MCA="${WORKDIR}/mca-76X-Ve.txt "
elif [ "$WHAT" == "zmm" ] ; then
    MCA="${WORKDIR}/mca-76X-Vm.txt "
fi

ROOTPREF="plots/Fall15-Inclusive/v1"
ROOT="${ROOTPREF}/${WHAT}"
COREOPT="-P $T --s2v -j $J -l 2.32 "
COREY="mcAnalysis.py ${MCA} ${COREOPT} -G  "
COREP="mcPlots.py ${MCA} ${COREOPT} -f --poisson --pdir ${ROOT} --showRatio --maxRatioRange 0.5 1.5 "
FEV=" -F mjvars/t \"$T/friends/evVarFriend_{cname}.root\" "
SF=" --FM sf/t \"$T/friends/sfFriend_{cname}.root\" "
FULLOPT=" $FEV $SF -W 'vtxWeight*SF_trig1lep*SF_LepTightLoose' "

RUNY2M="${COREY} ${WORKDIR}/zmumu_twiki.txt "
RUNY2E="${COREY} ${WORKDIR}/zeeincl.txt "

PLOT2M="${COREP} ${WORKDIR}/zmumu_twiki.txt ${WORKDIR}/zmumu_plots.txt "
PLOT2E="${COREP} ${WORKDIR}/zeeincl.txt ${WORKDIR}/zee_incl_plots.txt "

case $WHAT in
zmumu)
        echo "python ${RUNY2MU} $FEV --sp DYJets "
        echo "python ${PLOT2MU} $FEV --sp DYJets --pdir plots/Z_Inclusive_mm "
;;
zee)
        echo "python ${RUNY2E} ${FULLOPT} --sp DYJets "
        echo "python ${PLOT2E} ${FULLOPT} --sp DYJets --pdir plots/Z_inclusive_ee "
;;
zee_bb)
        echo "python ${RUNY2E} ${FULLOPT} --sp DYJets -A btagveto ebeb 'abs(LepGood1_eta) < 1.479 && abs(LepGood2_eta) < 1.479' "
        echo "python ${PLOT2E} ${FULLOPT} --sp DYJets -A btagveto ebeb 'abs(LepGood1_eta) < 1.479 && abs(LepGood2_eta) < 1.479' --pdir plots/Z_Inclusive_ee_EBEB --print=pdf,png,C,root "
;;                                                                                                                                      
zee_ee)                                                                                                                                 
        echo "python ${RUNY2E} ${FULLOPT} --sp DYJets -A btagveto ebeb 'abs(LepGood1_eta) > 1.479 && abs(LepGood2_eta) > 1.479' "            
        echo "python ${PLOT2E} ${FULLOPT} --sp DYJets -A btagveto ebeb 'abs(LepGood1_eta) > 1.479 && abs(LepGood2_eta) > 1.479' --pdir plots/Z_Inclusive_ee_EEEE --print=pdf,png,C,root "
;;                                                                                                                                      
zee_notebeb)                                                                                                                            
        echo "python ${RUNY2E} ${FULLOPT} --sp DYJets -A btagveto notebeb '(abs(LepGood1_eta)>1.566 || abs(LepGood2_eta)>1.566)' "           
        echo "python ${PLOT2E} ${FULLOPT} --sp DYJets -A btagveto notebeb '(abs(LepGood1_eta)>1.566 || abs(LepGood2_eta)>1.566)' --pdir plotsZ_Inclusive_ee_notEBEB --print=pdf,png,C,root "
;;
esac;
