################################
#  use mcEfficiencies.py to make plots of the fake rate
################################
T_SUSY="/data1/peruzzi/TREES_80X_011216_Spring16MVA_1lepFR --FDs /data1/peruzzi/frQCDVars_skimdata"
T_TTH=/afs/cern.ch/work/g/gpetrucc/TREES_80X_ttH_300117_1L
if hostname | grep -q cmsco01; then
    T_TTH=/data1/gpetrucc/TREES_80X_ttH_300117_1L
elif hostname | grep -q cmsphys10; then
    T_TTH=/data1/g/gpetrucc/TREES_80X_ttH_300117_1L
fi
ANALYSIS=$1; if [[ "$1" == "" ]]; then exit 1; fi; shift;
case $ANALYSIS in
ttH) T="${T_TTH}"; CUTFILE="ttH-multilepton/qcd1l.txt"; XVAR="ptJI90_mvaPt090_coarselongbin"; NUM="mvaPt_090i";;
susy_wpM) T="${T_SUSY}"; CUTFILE="susy-ewkino/qcd1l_wpM.txt"; XVAR="ptJIMIX4_mvaSusy_sMi_coarselongbin"; NUM="mvaSusy_sMi";;
susy_wpV) T="${T_SUSY}"; CUTFILE="susy-ewkino/qcd1l_wpV.txt"; XVAR="ptJIMIX3_mvaSusy_sVi_coarselongbin"; NUM="mvaSusy_sVi";;
susy_RA7) T="${T_SUSY}"; CUTFILE="susy-ewkino/qcd1l_RA7.txt"; XVAR="conePt_RA7_coarselongbin"; NUM="ra7_tight";;
*) echo "You did not specify the analysis"; exit 1;;
esac;
BCORE=" --s2v --tree treeProducerSusyMultilepton ttH-multilepton/mca-qcd1l.txt ${CUTFILE} -P $T -l 36.5 --AP  "
BCORE="${BCORE} --Fs {P}/1_extraVars_v1  "
BCORE="${BCORE} --mcc ttH-multilepton/mcc-eleIdEmu2.txt  "; 
BCORE="${BCORE} --mcc ttH-multilepton/mcc-noHLTinMC-some.txt  "; 

BG=" -j 8 "; if [[ "$1" == "-b" ]]; then BG=" & "; shift; fi

lepton=$1; if [[ "$1" == "" ]]; then exit 1; fi
case $lepton in
mu) BCORE="${BCORE} -E ^${lepton} --xf 'DoubleEG.*,JetHT.*'  "; QCD=QCDMu; ;;
el) BCORE="${BCORE} -E ^${lepton} --xf 'DoubleMu.*,JetHT.*,SingleMu.*' "; QCD=QCDEl; ;;
#mu_jet) lepton="mu"; BCORE="${BCORE} -E ${lepton} --xf 'Double.*' -X idEmuCut -R minimal ptj40 ' LepGood_awayJet_pt > 40'  "; QCD=QCDMu; ;;
#mu_jet6) lepton="mu"; BCORE="${BCORE} -E ${lepton} --xf 'Double.*,JetHT_.*' -X idEmuCut -R minimal ptj40 ' LepGood_awayJet_pt > 60'  "; QCD=QCDMu; ;;
#mu_ht)  lepton="mu"; BCORE="${BCORE} -E ${lepton} --xf 'Double.*' -X idEmuCut -R minimal ptj40 ' LepGood_awayJet_pt > 40'  "; QCD=QCDMu; ;;
#mu_any)  lepton="mu"; BCORE="${BCORE} -E ${lepton} --xf 'DoubleEG.*' -X idEmuCut  "; QCD=QCDMu; ;;
esac;

trigger=$2; if [[ "$2" == "" ]]; then exit 1; fi
case $trigger in
#PFJet6)
#    BCORE="${BCORE} -E HLT_PFJet6   "; 
#    PUW=" -L ttH-multilepton/frPuReweight.cc -W 'puw$lepton$trigger(nVert)' "
#    ;;
Mu3_PFJet40)
    BCORE="${BCORE} -A veto trigger 'HLT_FR_${trigger}' -A veto recoptfortrigger 'LepGood_pt>4.0' --xf 'SingleMu.*'  "; 
    PUW=" -L ttH-multilepton/frPuReweight.cc -W 'puw$trigger(nVert)' "
    ;;
Mu8)
    BCORE="${BCORE} -A veto trigger 'HLT_FR_${trigger}' -A veto recoptfortrigger 'LepGood_pt>8' --xf 'SingleMu.*'  "; 
    PUW=" -L ttH-multilepton/frPuReweight.cc -W 'puw$trigger(nVert)' "
    ;;
Mu17)
    BCORE="${BCORE} -A veto trigger 'HLT_FR_${trigger}' -A veto recoptfortrigger 'LepGood_pt>17' --xf 'SingleMu.*' "; 
    PUW=" -L ttH-multilepton/frPuReweight.cc -W 'puw$trigger(nVert)' "
    ;;
Mu27)
    BCORE="${BCORE} -A veto trigger 'HLT_FR_${trigger}' -A veto recoptfortrigger 'LepGood_pt>27' --xf 'DoubleMu.*' "; 
    PUW=" -L ttH-multilepton/frPuReweight.cc -W 'puw$trigger(nVert)' "
    ;;
Mu50)
    BCORE="${BCORE} -A veto trigger 'HLT_FR_${trigger}' -A veto recoptfortrigger 'LepGood_pt>50' --xf 'DoubleMu.*' "; 
    PUW=" -L ttH-multilepton/frPuReweight.cc -W 'puw$trigger(nVert)' "
    ;;
MuX_Combined)
    BCORE="${BCORE} -A veto trigger 'HLT_FR_${trigger}' -A veto recoptfortrigger 'LepGood_pt>8.5' --xf 'SingleMu.*'  "; 
    PUW=" "
    ;;
Ele8_CaloIdM_TrackIdM_PFJet30)
    BCORE="${BCORE} -A veto trigger 'HLT_FR_${trigger}' -A veto recoptfortrigger 'LepGood_pt>8'  "; 
    PUW=" -L ttH-multilepton/frPuReweight.cc -W 'puw$trigger(nVert)' "
    ;;
Ele12_CaloIdM_TrackIdM_PFJet30)
    BCORE="${BCORE} -A veto trigger 'HLT_FR_${trigger}' -A veto recoptfortrigger 'LepGood_pt>12'  "; 
    PUW=" -L ttH-multilepton/frPuReweight.cc -W 'puw$trigger(nVert)' "
    ;;
Ele17_CaloIdM_TrackIdM_PFJet30)
    BCORE="${BCORE} -A veto trigger 'HLT_FR_${trigger}' -A veto recoptfortrigger 'LepGood_pt>15'  "; 
    PUW=" -L ttH-multilepton/frPuReweight.cc -W 'puw$trigger(nVert)' "
    ;;
*)
    BCORE="${BCORE} -A veto trigger 'HLT_FR_${trigger}'  "; 
    PUW=" -L ttH-multilepton/frPuReweight.cc -W 'puw$trigger(nVert)' "
    ;;
esac;


what=$3;
more=$4
#PBASE="~/www/plots_FR/80X/lepMVA_$ANALYSIS/v2.0_041216/fr-meas/$lepton/HLT_$trigger/$what/$more"
PBASE="plots/80X/${ANALYSIS}_Moriond17/lepMVA/v3.0/fr-meas/qcd1l/$lepton/HLT_$trigger/$what/$more"

EWKONE="-p ${QCD}_red,EWK,data"
EWKSPLIT="-p ${QCD}_red,WJets,DYJets,data"
QCDEWKSPLIT="-p ${QCD}_[bclg]jets,WJets,DYJets,data"
FITEWK=" $EWKSPLIT --flp WJets,DYJets,${QCD}_red --peg-process DYJets WJets "
QCDNORM=" $QCDEWKSPLIT --sp WJets,DYJets,${QCD}_.jets --scaleSigToData  "
QCDFITEWK=" $QCDEWKSPLIT --flp WJets,DYJets,${QCD}_.jets --peg-process DYJets WJets --peg-process ${QCD}_[clg]jets ${QCD}_bjets "
QCDFITQCD=" $QCDEWKSPLIT --flp WJets,DYJets,${QCD}_.jets --peg-process DYJets WJets --peg-process ${QCD}_[gl]jets WJets --peg-process ${QCD}_cjets ${QCD}_bjets "
QCDFITALL=" $QCDEWKSPLIT --flp WJets,DYJets,${QCD}_.jets --peg-process DYJets WJets --peg-process ${QCD}_gjets WJets --peg-process ${QCD}_cjets ${QCD}_bjets "

case $lepton in
    el) BARREL="00_15"; ENDCAP="15_25"; ETA="1.479";;
    mu) BARREL="00_12"; ENDCAP="12_24"; ETA="1.2";;
esac;

if [[ "$more" != "" ]]; then
    shift 4; BCORE="$BCORE $*";
    echo "Adding the following options for $more: $*" 1>&2 
fi;

case $what in
    nvtx)
        echo "python mcPlots.py -f -j 6 $BCORE ttH-multilepton/qcd1l_plots.txt --pdir $PBASE --sP nvtx $EWKONE " 
        echo "echo; echo; ";
        echo "python ../tools/vertexWeightFriend.py _puw$trigger $PBASE/qcd1l_plots.root ";
        echo "echo; echo ' ---- Now you should put the normalization and weight into frPuReweight.cc defining a puw$trigger ----- ' ";
        ;;
    nvtx-closure)
        echo "python mcPlots.py -f -j 6 $BCORE $PUW ttH-multilepton/qcd1l_plots.txt --pdir $PBASE --sP nvtx $EWKONE  --showRatio --maxRatioRange 0.9 1.1 " 
        ;;
    mc-yields)
        echo "python mcAnalysis.py -f -j 6 $BCORE $PUW ${EWKSPLIT} --sp 'QCD.*' --fom S/B --fom S/errSB -G " 
        ;;
    fit-*)
        echo "python mcPlots.py -f -j 6 $BCORE $PUW ttH-multilepton/qcd1l_plots.txt --pdir $PBASE -E $what $FITEWK --preFitData ${what/fit-/} --showRatio --maxRatioRange 0.0 1.99 " 
        ;;
    num-fit-*)
        echo "python mcPlots.py -f -j 6 $BCORE $PUW ttH-multilepton/qcd1l_plots.txt --pdir $PBASE -E $what $FITEWK --preFitData ${what/num-fit-/} --showRatio --maxRatioRange 0.0 1.99 -E num" 
        ;;
    qcdflav-norm)
        echo "python mcPlots.py -f -j 6 $BCORE $PUW ttH-multilepton/qcd1l_plots.txt --pdir $PBASE -E $what $QCDNORM --showRatio --maxRatioRange 0.0 1.99 " 
        ;;
    qcdflav-fit)
        echo "python mcPlots.py -f -j 6 $BCORE $PUW ttH-multilepton/qcd1l_plots.txt --pdir $PBASE -E $what $QCDFITEWK --preFitData ${what/flav-fit/} --showRatio --maxRatioRange 0.0 1.99 " 
        ;;
    flav-fit*)
        echo "python mcPlots.py -f -j 6 $BCORE $PUW ttH-multilepton/qcd1l_plots.txt --pdir $PBASE -E $what $QCDFITQCD --preFitData ${what/flav-fit/} --showRatio --maxRatioRange 0.0 1.99 " 
        ;;
    flav3-fit*)
        echo "python mcPlots.py -f -j 6 $BCORE $PUW ttH-multilepton/qcd1l_plots.txt --pdir $PBASE -E $what $QCDFITALL --preFitData ${what/flav3-fit/} --showRatio --maxRatioRange 0.0 1.99 " 
        ;;
    fakerates-*)
        fitVar=${what/fakerates-/}

        MCEFF="  python ttH-multilepton/dataFakeRate.py -f  $BCORE $PUW $EWKONE  --groupBy cut ttH-multilepton/make_fake_rates_sels.txt ttH-multilepton/make_fake_rates_xvars.txt  "
        MCEFF="$MCEFF --sp ${QCD}_red  "
        MCEFF="$MCEFF --sP ${NUM} --sP ${XVAR}  --sP $fitVar $fitVar  --ytitle 'Fake rate' "
        MCEFF="$MCEFF  " # ratio for fake rates
        MCEFF="$MCEFF --fixRatioRange --maxRatioRange 0.7 1.29 " # ratio for other plots
        LEGEND=" --legend=TL --fontsize 0.05 --legendWidth 0.4"
        RANGES=" --showRatio  --ratioRange 0.00 2.99 "
        STACK="python ttH-multilepton/stack_fake_rates_data.py "
        ISCOMB=false
        case $lepton in  # 0,5,10,15,20,30,45,65,100
           el) 
                case $trigger in
                Ele8_CaloIdM_TrackIdM_PFJet30)
        		RANGES="$RANGES  --yrange 0 0.25  --xcut 15 45 --xline 20 " ;;
                Ele12_CaloIdM_TrackIdM_PFJet30)
        		RANGES="$RANGES  --yrange 0 0.25  --xcut 20 100 --xline 20 --xline 30 " ;;
                Ele17_CaloIdM_TrackIdM_PFJet30)
                        MCEFF="${MCEFF/_coarselongbin/_coarse}"
                        XVAR="${XVAR/_coarselongbin/_coarse}"
        		RANGES="$RANGES  --yrange 0 0.25  --xcut 30 100  " ;;
                esac;
		;;
           mu)
                 RANGES="$RANGES  --yrange 0 0.25 " ;
                 if [[ "$trigger" == "Mu17" ]]; then 
                     MCEFF="${MCEFF/_coarselongbin/_finemu17bin}"
                     XVAR="${XVAR/_coarselongbin/_finemu17bin}"
                     RANGES="${RANGES} --xcut 25 100 --xline 30 "; 
                elif [[ "$trigger" == "Mu8" ]]; then
                     MCEFF="${MCEFF/_coarselongbin/_coarsemu8bin}"
                     XVAR="${XVAR/_coarselongbin/_coarsemu8bin}"
                     RANGES="${RANGES} --xcut 13 45 --xline 15 --xline 30"; 
                 elif [[ "$trigger" == "Mu27" ]]; then
                     MCEFF="${MCEFF/_coarselongbin/_finemu27bin}"
                     XVAR="${XVAR/_coarselongbin/_finemu27bin}"
                     RANGES="${RANGES} --xcut 40 100 --xline 45 "; 
                 elif [[ "$trigger" == "Mu50" ]]; then
                     MCEFF="${MCEFF/_coarselongbin/_coarsemu50bin}"
                     XVAR="${XVAR/_coarselongbin/_coarsemu50bin}"
                     RANGES="${RANGES} --xcut 81 100 "; 
                 elif [[ "$trigger" == "Mu3_PFJet40" ]]; then
                     RANGES="${RANGES} --xcut 10 30 --xline 10 --xline 15"; 
                 elif [[ "$trigger" == "MuX_Combined" ]]; then
                     ISCOMB=true
                     MCEFF="${MCEFF/_coarselongbin/_coarsecomb}"
                     XVAR="${XVAR/_coarselongbin/_coarsecomb}"
                     RANGES="${RANGES} --xcut 10 100 --xline 10 --xline 15 --xline 30 --xline 45 "; 
                     for E in ${BARREL} ${ENDCAP}; do
                        STACK=""
                        STACK="${STACK}  ${PBASE/MuX_Combined/Mu3_PFJet40}/fr_sub_eta_${E}.root:5-30"
                        STACK="${STACK}  ${PBASE/MuX_Combined/Mu8}/fr_sub_eta_${E}.root:15-45"
                        STACK="${STACK}  ${PBASE/MuX_Combined/Mu17}/fr_sub_eta_${E}.root:30-100"
                        STACK="${STACK}  ${PBASE/MuX_Combined/Mu27}/fr_sub_eta_${E}.root:45-100"
                        #STACK="${STACK}  ${PBASE/MuX_Combined/Mu50}/fr_sub_eta_${E}.root:81-100"
                        echo "python ttH-multilepton/combine-fr-bins-prefit.py ${STACK} $PBASE/fr_sub_eta_${E}.root --oprefix ${NUM}_vs_${fitVar}_${XVAR}";
                     done;
                 elif [[ "$trigger" == "MuX_CombLow" ]]; then
                     ISCOMB=true
                     MCEFF="${MCEFF/_coarselongbin/_coarsecomblo}"
                     XVAR="${XVAR/_coarselongbin/_coarsecomblo}"
                     RANGES="${RANGES} --xcut 10 45 --xline 15 --xline 30"; 
                     for E in ${BARREL} ${ENDCAP}; do
                        STACK=""
                        STACK="${STACK}  ${PBASE/MuX_CombLow/Mu3_PFJet40}/fr_sub_eta_${E}.root:5-30"
                        STACK="${STACK}  ${PBASE/MuX_CombLow/Mu8}/fr_sub_eta_${E}.root:15-45"
                        #STACK="${STACK}  ${PBASE/MuX_CombLow/Mu50}/fr_sub_eta_${E}.root:81-100"
                        echo "python ttH-multilepton/combine-fr-bins-prefit.py ${STACK} $PBASE/fr_sub_eta_${E}.root --oprefix ${NUM}_vs_${fitVar}_${XVAR}";
                     done;
                  elif [[ "$trigger" == "MuX_CombHigh" ]]; then
                     ISCOMB=true
                     if [[ "$more" == "splitbin" ]]; then
                         MCEFF="${MCEFF/_coarselongbin/_finecombhi}"
                         XVAR="${XVAR/_coarselongbin/_finecombhi}"
                     else
                         MCEFF="${MCEFF/_coarselongbin/_coarsecombhi}"
                         XVAR="${XVAR/_coarselongbin/_coarsecombhi}"
                     fi
                     RANGES="${RANGES} --xcut 20 100 --xline 30 --xline 45 "; 
                     for E in ${BARREL} ${ENDCAP}; do
                        STACK=""
                        STACK="${STACK}  ${PBASE/MuX_CombHigh/Mu8}/fr_sub_eta_${E}.root:20-45"
                        STACK="${STACK}  ${PBASE/MuX_CombHigh/Mu17}/fr_sub_eta_${E}.root:30-100"
                        STACK="${STACK}  ${PBASE/MuX_CombHigh/Mu27}/fr_sub_eta_${E}.root:45-100"
                        #STACK="${STACK}  ${PBASE/MuX_CombHigh/Mu50}/fr_sub_eta_${E}.root:81-100"
                        echo "python ttH-multilepton/combine-fr-bins-prefit.py ${STACK} $PBASE/fr_sub_eta_${E}.root --oprefix ${NUM}_vs_${fitVar}_${XVAR}";
                     done;
                 fi
            ;;
        esac;
	if [[ "$ANALYSIS" == "susy_wpM" ]]; then RANGES=${RANGES/--yrange 0 0.??/--yrange 0 0.50}; fi
        MCEFF="$MCEFF $LEGEND $RANGES"
        if ! $ISCOMB; then
        echo " ( $MCEFF -o $PBASE/fr_sub_eta_${BARREL}.root --bare -A veto eta 'abs(LepGood_eta)<$ETA' $BG )"
        echo " ( $MCEFF -o $PBASE/fr_sub_eta_${ENDCAP}.root --bare -A veto eta 'abs(LepGood_eta)>$ETA' $BG )"
        fi;
        MCGO="$MCEFF --compare ${QCD}_red_prefit,data_sub_syst_prefit,data_sub_prefit --algo=globalFit "
        echo " ( $MCGO -i $PBASE/fr_sub_eta_${BARREL}.root -o $PBASE/fr_sub_eta_${BARREL}_globalFit.root --algo=globalFit --fcut 0 20 --subSyst 0.05 $BG )"
        echo " ( $MCGO -i $PBASE/fr_sub_eta_${ENDCAP}.root -o $PBASE/fr_sub_eta_${ENDCAP}_globalFit.root --algo=globalFit --fcut 0 20 --subSyst 0.05 $BG )"
        MCGO="$MCEFF --compare ${QCD}_red_prefit,data_prefit,total_prefit,data_sub_syst_prefit,data_sub_prefit --algo=globalFit "
        MCGO="${MCGO/--yrange 0 0.??/--yrange 0 0.5}"
        echo " ( $MCGO -i $PBASE/fr_sub_eta_${BARREL}.root -o $PBASE/fr_sub_eta_${BARREL}_globalFit_full.root --algo=globalFit --fcut 0 20 --subSyst 0.05 $BG )"
        echo " ( $MCGO -i $PBASE/fr_sub_eta_${ENDCAP}.root -o $PBASE/fr_sub_eta_${ENDCAP}_globalFit_full.root --algo=globalFit --fcut 0 20 --subSyst 0.05 $BG )"
        #MCGO="$MCEFF --compare ${QCD}_red_prefit,${QCD}_red --algo=fitND "
        #echo " ( $MCGO -i $PBASE/fr_sub_eta_${BARREL}.root -o $PBASE/fr_sub_eta_${BARREL}_full.root   $BG )"
        #echo " ( $MCGO -i $PBASE/fr_sub_eta_${ENDCAP}.root -o $PBASE/fr_sub_eta_${ENDCAP}_full.root   $BG )"
        MCGO="$MCEFF --compare ${QCD}_red_prefit,data_fit --algo=fitSimND --shapeSystSignal=l:0.2,s:0.1,b:0.01 --shapeSystBackground=l:0.1,s:0.05,b:0.01 "
        echo " ( $MCGO -i $PBASE/fr_sub_eta_${BARREL}.root -o $PBASE/fr_sub_eta_${BARREL}_fitSimND.root  $BG )"
        echo " ( $MCGO -i $PBASE/fr_sub_eta_${ENDCAP}.root -o $PBASE/fr_sub_eta_${ENDCAP}_fitSimND.root  $BG )"
        #if $ISCOMB; then
        #MCGO="$MCEFF --compare ${QCD}_red_prefit,data_fit --algo=fitAllSimND --shapeSystSignal=l:0.25,s:0.05,b:0.01 --shapeSystBackground=l:0.05,s:0.03,b:0.01 "
        #echo " ( ${MCGO/dataFakeRate.py/dataFakeRate2.py} -i $PBASE/fr_sub_eta_${BARREL}.root -o $PBASE/fr_sub_eta_${BARREL}_fitAllSimND.root  $BG )"
        #echo " ( ${MCGO/dataFakeRate.py/dataFakeRate2.py} -i $PBASE/fr_sub_eta_${ENDCAP}.root -o $PBASE/fr_sub_eta_${ENDCAP}_fitAllSimND.root  $BG )"
        #fi;
        #if ! $ISCOMB; then
        MCGO="$MCEFF --compare ${QCD}_red_prefit,data_fqcd --algo=fQCD "
        echo " ( $MCGO -i $PBASE/fr_sub_eta_${BARREL}.root -o $PBASE/fr_sub_eta_${BARREL}_fQCD.root  $BG )"
        echo " ( $MCGO -i $PBASE/fr_sub_eta_${ENDCAP}.root -o $PBASE/fr_sub_eta_${ENDCAP}_fQCD.root  $BG )"
        MCGO="$MCEFF --compare ${QCD}_red_prefit,data_fqcd --algo=ifQCD "
        echo " ( $MCGO -i $PBASE/fr_sub_eta_${BARREL}.root -o $PBASE/fr_sub_eta_${BARREL}_ifQCD.root --subSyst 1.0 $BG )"
        echo " ( $MCGO -i $PBASE/fr_sub_eta_${ENDCAP}.root -o $PBASE/fr_sub_eta_${ENDCAP}_ifQCD.root --subSyst 1.0 $BG )"
        STACK="python ttH-multilepton/stack_fake_rates_data.py $RANGES $LEGEND --comb-mode=midpoint" # :_fit
        PATT="${NUM}_vs_${XVAR}_${fitVar}_%s"
        for E in ${BARREL} ${ENDCAP}; do
            echo "( $STACK -o $PBASE/fr_sub_eta_${E}_comp.root    $PBASE/fr_sub_eta_${E}_globalFit.root:$PATT:${QCD}_red_prefit,data_sub_syst_prefit  $PBASE/fr_sub_eta_${E}_ifQCD.root:$PATT:${QCD}_red_prefit,data_fqcd   $PBASE/fr_sub_eta_${E}_fitSimND.root:$PATT:data_fit   )";
        done
        #fi
       ;;

esac;
