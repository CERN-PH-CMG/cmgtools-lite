#!/bin/bash

RUNIT="echo "
if [[ "$1" == "-e" ]]; then
    echo "# will execute the program "
    RUNIT="eval "; shift;
fi;

SAVEYIELD=0
if [[ "$1" == "-y" ]]; then
    echo "# save the yields in a text file"
    SAVEYIELD=1; shift;
fi;

DOPLOTS=0
if [[ "$1" == "-p" ]]; then
    echo "# will do the plots"
    DOPLOTS=1; shift;
fi;

RINPUTS=0
if [[ "$1" == "-r" ]]; then
    echo "# will print the command to write the inputs for the R factors"
    RINPUTS=1; shift;
fi;

CATEGORY="inclusive"
if [[ "$1" == "-c" ]]; then
    CATEGORY=$2; shift; shift;
    echo "# ${RUNIT} command for the category " $CATEGORY
fi;

WHAT=$1; if [[ "$1" == "" ]]; then echo "monojet.sh <what>"; exit 1; fi

BASEDIR=""
if [ "$WHAT" == "zee" ] || [ "$WHAT" == "zeeI" ] || [ "$WHAT" == "wenI" ] || [ "$WHAT" == "wen" ] ; then
    BASEDIR="TREES_25ns_1TLEP1JETSKIM_76X"
elif [ "$WHAT" == "gj" ] ; then
    BASEDIR="TREES_25ns_1GSKIM_76X"
else 
    BASEDIR="TREES_25ns_MET200SKIM_76X"
fi

WORKDIR="monojet"

if [[ "$HOSTNAME" == "cmsphys06" ]]; then
    T="/data1/emanuele/monox/${BASEDIR}";
    #T="/afs/cern.ch/work/e/emanuele/Trees/"
    J=8;
else
    T="/cmshome/dimarcoe/${BASEDIR}";
    J=3;
fi

MCA=""
if [ "$WHAT" == "wen" ] || [ "$WHAT" == "zee" ] ; then
    MCA="${WORKDIR}/mca-76X-Ve.txt "
elif [ "$WHAT" == "wmn" ] || [ "$WHAT" == "zmm" ] ; then
    MCA="${WORKDIR}/mca-76X-Vm.txt "
elif [ "$WHAT" == "gj" ] ; then
    MCA="${WORKDIR}/mca-76X-Gj.txt "
else
    MCA="${WORKDIR}/mca-76X-sr.txt "
fi

ROOTPREF="plots/${CATEGORY}"
ROOT="${ROOTPREF}/${WHAT}"
YIELDFILE="${ROOTPREF}/${WHAT}/${WHAT}_yields.txt"
ROOTR="${ROOTPREF}/transfer_factors"
COREOPT="-P $T --s2v -j $J -l 2.32 "
COREY="mcAnalysis.py ${MCA} ${COREOPT} -G  "
COREP="mcPlots.py ${MCA} ${COREOPT} -f --poisson --pdir ${ROOT} --showRatio --maxRatioRange 0.5 1.5 "
CORER="mcSystematics.py ${MCA} ${COREOPT} -f --select-plot \"recoil\" "
FEV=" -F mjvars/t \"$T/friends/evVarFriend_{cname}.root\" "
SF=" --FM sf/t \"$T/friends/sfFriend_{cname}.root\" "

if [ "$CATEGORY" == "monov" ] ; then COREP="${COREP} --rebin 2 " ; fi
if [ "$RINPUTS" != "0" ] ; then mkdir -p $ROOTR ; fi

RUNYSR="${COREY} ${WORKDIR}/monojet_twiki.txt "
RUNY2M="${COREY} ${WORKDIR}/zmumu_twiki.txt "
RUNY2E="${COREY} ${WORKDIR}/zee_twiki.txt "
RUNY1M="${COREY} ${WORKDIR}/wmunu_twiki.txt "
RUNY1E="${COREY} ${WORKDIR}/wenu_twiki.txt "
RUNY1G="${COREY} ${WORKDIR}/gjets_twiki.txt "

PLOTSR="${COREP} ${WORKDIR}/monojet_twiki.txt ${WORKDIR}/monojet_plots.txt "
PLOT2M="${COREP} ${WORKDIR}/zmumu_twiki.txt ${WORKDIR}/zmumu_plots.txt "
PLOT2E="${COREP} ${WORKDIR}/zee_twiki.txt ${WORKDIR}/zee_plots.txt "
PLOT1M="${COREP} ${WORKDIR}/wmunu_twiki.txt ${WORKDIR}/wmunu_plots.txt "
PLOT1E="${COREP} ${WORKDIR}/wenu_twiki.txt ${WORKDIR}/wenu_plots.txt "
PLOT1G="${COREP} ${WORKDIR}/gjets_twiki.txt ${WORKDIR}/gjets_plots.txt "

SYSTSR="${CORER} ${WORKDIR}/monojet_twiki.txt ${WORKDIR}/monojet_plots.txt monojet/syst_2l.txt "
SYST2M="${CORER} ${WORKDIR}/zmumu_twiki.txt ${WORKDIR}/zmumu_plots.txt monojet/syst_2l.txt "
SYST2E="${CORER} ${WORKDIR}/zee_twiki.txt ${WORKDIR}/zee_plots.txt monojet/syst_2l.txt "
SYST1M="${CORER} ${WORKDIR}/wmunu_twiki.txt ${WORKDIR}/wmunu_plots.txt monojet/syst_1l.txt "
SYST1E="${CORER} ${WORKDIR}/wenu_twiki.txt ${WORKDIR}/wenu_plots.txt monojet/syst_1l.txt "
SYST1G="${CORER} ${WORKDIR}/gjets_twiki.txt ${WORKDIR}/gjets_plots.txt monojet/syst_1g.txt "

MONOV_CUT="-A dphijm monoV 'nFatJetClean>0 && FatJetClean1_pt>250 && abs(FatJetClean1_eta)<2.4 && abs(FatJetClean1_prunedMass-85)<20 && FatJetClean1_tau2/FatJetClean1_tau1<0.6"
MONOJ_CUT="-A dphijm monoJ '!(nFatJetClean>0 && FatJetClean1_pt>250 && abs(FatJetClean1_eta)<2.4 && abs(FatJetClean1_prunedMass-85)<20 && FatJetClean1_tau2/FatJetClean1_tau1<0.6)"
if [ "$WHAT" == "zmm" ] || [ "$WHAT" == "wmn" ] ; then
    MONOV_CUT="${MONOV_CUT} && metNoMu_pt>250' "
    MONOJ_CUT="${MONOJ_CUT} || metNoMu_pt<=250' "
elif [ "$WHAT" == "zee" ] ; then
    MONOV_CUT="${MONOV_CUT} && pt_3(met_pt,met_phi,LepGood1_pt,LepGood1_phi,LepGood2_pt,LepGood2_phi)>250' "
    MONOJ_CUT="${MONOJ_CUT} || pt_3(met_pt,met_phi,LepGood1_pt,LepGood1_phi,LepGood2_pt,LepGood2_phi)<=250' "
elif [ "$WHAT" == "wen" ] ; then
    MONOV_CUT="${MONOV_CUT} && pt_2(met_pt,met_phi,LepGood1_pt,LepGood1_phi)>250' "
    MONOJ_CUT="${MONOJ_CUT} || pt_2(met_pt,met_phi,LepGood1_pt,LepGood1_phi)<=250' "
elif [ "$WHAT" == "gj" ] ; then
    MONOV_CUT="${MONOV_CUT} && pt_2(met_pt,met_phi,GammaGood1_pt,GammaGood1_phi)>250' "
    MONOJ_CUT="${MONOJ_CUT} || pt_2(met_pt,met_phi,GammaGood1_pt,GammaGood1_phi)<=250' "
else
    MONOV_CUT="${MONOV_CUT}' "
    MONOJ_CUT="${MONOJ_CUT}' "
fi

CAT_CUT=""
case $CATEGORY in
monov) CAT_CUT=$MONOV_CUT ;;
monoj) CAT_CUT=$MONOJ_CUT ;;
esac

REDIRECTYIELD=""
if [[ "$SAVEYIELD" != "0" ]]; then
    mkdir -p "${ROOT}";
    echo "# will save the yields in the file: $YIELDFILE"
    REDIRECTYIELD=" > ${YIELDFILE} "
fi

case $WHAT in
sr)
        FULLOPT=" $FEV $SF -W 'vtxWeight*SF_trigmetnomu*SF_BTag*SF_NLO_QCD*SF_NLO_EWK' $CAT_CUT "
        if [[ "$RINPUTS" != "0" ]]; then
            comm="python ${SYSTSR} ${FULLOPT} -p 'ZNuNuHT,WJetsHT' -o ${ROOTR}/rinputs_SR.root "
            $RUNIT $comm
        else
            if [[ "$DOPLOTS" != "0" ]]; then
                comm="python ${PLOTSR} ${FULLOPT} "
                $RUNIT $comm
            else
                comm="python ${RUNYSR} ${FULLOPT} ${REDIRECTYIELD}"
                $RUNIT $comm
            fi
        fi;
;;
zmm)
        FULLOPT=" $FEV $SF -W 'vtxWeight*SF_trigmetnomu*SF_LepTightLoose*SF_BTag*SF_NLO_QCD*SF_NLO_EWK' $CAT_CUT "
        if [[ "$RINPUTS" != "0" ]]; then
            comm="python ${SYST2M} ${FULLOPT} -p DYJetsHT -o ${ROOTR}/rinputs_DYJetsHT_CR2MU.root "
            $RUNIT $comm
        else
            if [[ "$DOPLOTS" != "0" ]]; then
                comm="python ${PLOT2M} ${FULLOPT} --sp DYJetsHT "
                $RUNIT $comm
            else
                comm="python ${RUNY2M} ${FULLOPT} --sp DYJetsHT ${REDIRECTYIELD}"
                $RUNIT $comm
            fi
        fi;
;;
wmn)
        FULLOPT=" $FEV $SF -W 'vtxWeight*SF_trigmetnomu*SF_LepTight*SF_BTag*SF_NLO_QCD*SF_NLO_EWK' $CAT_CUT "
        if [[ "$RINPUTS" != "0" ]]; then
            comm="python ${SYST1M} ${FULLOPT} -p WJetsHT -o ${ROOTR}/rinputs_WJetsHT_CR1MU.root "
            $RUNIT $comm
        else
            if [[ "$DOPLOTS" != "0" ]]; then
                comm="python ${PLOT1M} ${FULLOPT} --sp WJetsHT "
                $RUNIT $comm
            else
                comm="python ${RUNY1M} ${FULLOPT} --sp WJetsHT ${REDIRECTYIELD}"
                $RUNIT $comm
            fi
        fi;
;;
zee)
        FULLOPT=" $FEV $SF -W 'vtxWeight*SF_trig1lep*SF_LepTightLoose*SF_BTag*SF_NLO_QCD*SF_NLO_EWK' $CAT_CUT "
        if [[ "$RINPUTS" != "0" ]]; then
            comm="python ${SYST2E} ${FULLOPT} -p DYJetsHT -o ${ROOTR}/rinputs_DYJetsHT_CR2E.root "
            $RUNIT $comm
        else
            if [[ "$DOPLOTS" != "0" ]]; then
                comm="python ${PLOT2E} ${FULLOPT} --sp DYJetsHT "
                $RUNIT $comm
            else
                comm="python ${RUNY2E} ${FULLOPT} --sp DYJetsHT ${REDIRECTYIELD}"
                $RUNIT $comm
            fi
        fi;
;;
wen)
        FULLOPT=" $FEV $SF -W 'vtxWeight*SF_trig1lep*SF_LepTight*SF_BTag*SF_NLO_QCD*SF_NLO_EWK' $CAT_CUT "
        if [[ "$RINPUTS" != "0" ]]; then
            comm="python ${SYST1E} ${FULLOPT} -p WJetsHT -o ${ROOTR}/rinputs_WJetsHT_CR1E.root "
            $RUNIT $comm
        else
            if [[ "$DOPLOTS" != "0" ]]; then
                comm="python ${PLOT1E} ${FULLOPT} --sp WJetsHT "
                $RUNIT $comm
            else
                comm="python ${RUNY1E} ${FULLOPT} --sp WJetsHT ${REDIRECTYIELD}"
                $RUNIT $comm
            fi
        fi;
;;
gj)
        FULLOPT=" $FEV $SF -W 'vtxWeight*SF_BTag*SF_NLO_QCD*SF_NLO_EWK' $CAT_CUT "
        if [[ "$RINPUTS" != "0" ]]; then
            comm="python ${SYST1G} ${FULLOPT} -p GJetsHT -o ${ROOTR}/rinputs_GJetsHT_CR1G.root "
            $RUNIT $comm
        else
            if [[ "$DOPLOTS" != "0" ]]; then
                comm="python ${PLOT1G} ${FULLOPT} --sp GJetsHT "
                $RUNIT $comm
            else
                comm="python ${RUNY1G} ${FULLOPT} --sp GJetsHT ${REDIRECTYIELD}"
                $RUNIT $comm
            fi
        fi;
;;
TF)
        echo "python monojet/prepareRFactors.py ZNuNuHT DYJetsHT ${ROOTR}/rinputs_SR.root ${ROOTR}/rinputs_DYJetsHT_CR2MU.root SR CR --pdir ${ROOTR}"
        echo "python monojet/prepareRFactors.py WJetsHT WJetsHT ${ROOTR}/rinputs_SR.root ${ROOTR}/rinputs_WJetsHT_CR1MU.root SR CR --pdir ${ROOTR}"
        echo "python monojet/prepareRFactors.py ZNuNuHT WJetsHT ${ROOTR}/rinputs_SR.root ${ROOTR}/rinputs_SR.root SR SR --pdir ${ROOTR}"
esac;
