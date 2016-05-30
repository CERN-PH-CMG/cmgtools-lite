################################
#  use mcEfficiencies.py to make plots of the fake rate
################################
T="/afs/cern.ch/user/g/gpetrucc/w/TREES_TTH_260116_76X_1L"
if hostname | grep -q cmsco01; then
    T="/data1/gpetrucc/TREES_TTH_260116_76X_1L"
elif hostname | grep -q vinavx; then
    T="/home/gpetrucc/TREES_TTH_260116_76X_1L"
fi
BCORE=" --s2v --tree treeProducerSusyMultilepton ttH-multilepton/mca-qcd1l.txt ttH-multilepton/qcd1l.txt -P $T -l 2.32 --AP  "
BCORE="${BCORE} --mcc ttH-multilepton/mcc-eleIdEmu2.txt  "; 

BG=" -j 6 "; if [[ "$1" == "-b" ]]; then BG=" & "; shift; fi

lepton=$1; if [[ "$1" == "" ]]; then exit 1; fi
case $lepton in
mu) BCORE="${BCORE} -E ${lepton} --xf 'DoubleEG.*,JetHT.*'  "; QCD=QCDMu; ;;
el) BCORE="${BCORE} -E ${lepton} --xf 'DoubleMu.*,JetHT.*'  "; QCD=QCDEl; ;;
mu_jet) lepton="mu"; BCORE="${BCORE} -E ${lepton} --xf 'Double.*' -X idEmuCut -R minimal ptj40 ' LepGood_awayJet_pt > 40'  "; QCD=QCDMu; ;;
mu_jet6) lepton="mu"; BCORE="${BCORE} -E ${lepton} --xf 'Double.*,JetHT_.*' -X idEmuCut -R minimal ptj40 ' LepGood_awayJet_pt > 60'  "; QCD=QCDMu; ;;
mu_ht)  lepton="mu"; BCORE="${BCORE} -E ${lepton} --xf 'Double.*' -X idEmuCut -R minimal ptj40 ' LepGood_awayJet_pt > 40'  "; QCD=QCDMu; ;;
mu_any)  lepton="mu"; BCORE="${BCORE} -E ${lepton} --xf 'DoubleEG.*' -X idEmuCut  "; QCD=QCDMu; ;;
esac;

trigger=$2; if [[ "$2" == "" ]]; then exit 1; fi
case $trigger in
PFJet40)
    BCORE="${BCORE} -E HLT_FR_PFJet40   "; 
    PUW=" -L ttH-multilepton/frPuReweight.cc -W 'puw$lepton$trigger(nVert)' "
    ;;
PFJet)
    BCORE="${BCORE} -E HLT_PFJet   "; 
    PUW=" -L ttH-multilepton/frPuReweight.cc -W 'puw$lepton$trigger(nVert)' "
    ;;
PFJet6)
    BCORE="${BCORE} -E HLT_PFJet6   "; 
    PUW=" -L ttH-multilepton/frPuReweight.cc -W 'puw$lepton$trigger(nVert)' "
    ;;
PFHT*)
    BCORE="${BCORE} -E HLT_FR_$trigger   "; 
    PUW=" -L ttH-multilepton/frPuReweight.cc -W 'puw$lepton$trigger(nVert)' "
    ;;
JHT)
    BCORE="${BCORE} -E HLT_JHT   "; 
    PUW=" -L ttH-multilepton/frPuReweight.cc -W 'puw$lepton$trigger(nVert)' "
    ;;
AnyM)
    BCORE="${BCORE} -A veto trigger HLT_AnyM  ";
    PUW=" -L ttH-multilepton/frPuReweight.cc -W 'puw$trigger(nVert)' "
    ;;
*)
    BCORE="${BCORE} -A veto trigger HLT_FR_${trigger}  "; 
    PUW=" -L ttH-multilepton/frPuReweight.cc -W 'puw$trigger(nVert)' "
    ;;
esac;


what=$3;
more=$4
PBASE="plots/76X/ttH/fr-meas/v1.0/$lepton/HLT_$trigger/$what/$more"

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
        echo "python ../tools/vertexWeightFriend.py no $PBASE/qcd1l_plots.root ";
        echo "echo; echo ' ---- Now you should put the normalization and weight into frPuReweight.cc defining a puw$trigger ----- ' ";
        ;;
    nvtx-closure)
        echo "python mcPlots.py -f -j 6 $BCORE $PUW ttH-multilepton/qcd1l_plots.txt --pdir $PBASE --sP nvtx $EWKONE  --showRatio --maxRatioRange 0.9 1.1 " 
        ;;
    fit*)
        echo "python mcPlots.py -f -j 6 $BCORE $PUW ttH-multilepton/qcd1l_plots.txt --pdir $PBASE -E $what $FITEWK --preFitData ${what/fit/} --showRatio --maxRatioRange 0.0 1.99 " 
        ;;
    num-fit*)
        echo "python mcPlots.py -f -j 6 $BCORE $PUW ttH-multilepton/qcd1l_plots.txt --pdir $PBASE -E $what $FITEWK --preFitData ${what/num-fit/} --showRatio --maxRatioRange 0.0 1.99 -E num" 
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
        XVAR="mvaPt075_coarse"
        MCEFF="  python ttH-multilepton/dataFakeRate.py -f  $BCORE $PUW $EWKONE  --groupBy cut ttH-multilepton/make_fake_rates_sels.txt ttH-multilepton/make_fake_rates_xvars.txt  "
        MCEFF="$MCEFF --sp ${QCD}_red  "
        MCEFF="$MCEFF --sP mvaPt_075i --sP ptJI85_${XVAR}  --sP $fitVar $fitVar  --ytitle 'Fake rate' "
        MCEFF="$MCEFF  " # ratio for fake rates
        MCEFF="$MCEFF --fixRatioRange --maxRatioRange 0.7 1.29 " # ratio for other plots
        LEGEND=" --legend=TL --fontsize 0.05 --legendWidth 0.4"
        RANGES=" --showRatio  --ratioRange 0.00 2.99 "
        STACK="python ttH-multilepton/stack_fake_rates_data.py "
        case $lepton in  # 0,5,10,15,20,30,45,65,100
           el) RANGES="$RANGES  --yrange 0 0.25  --xcut 20 100 --xline 30 " ;;
           mu)
                 RANGES="$RANGES  --yrange 0 0.25  --xcut 15 100 --xline 20 --xline 45" ;
                 if [[ "$trigger" == "Mu17" ]]; then 
                     RANGES=${RANGES/--xcut 15 100/--xcut 30 100}; 
                     RANGES=${RANGES/--xline 20 --xline 45/--xline 45}; 
                 elif [[ "$trigger" == "PFJet40" ]]; then
                     MCEFF="${MCEFF/mvaPt075_coarse/mvaPt075_vcoarse}"
                     RANGES=${RANGES/--xcut 15 100/--xcut 5 30};
                     RANGES=${RANGES/--xline 20 --xline 45/--xline 10 --xline 20};
                 elif [[ "$trigger" == "PFJet" ]]; then
                     XVAR="mvaPt075_low"
                     MCEFF="${MCEFF/mvaPt075_coarse/$XVAR}"
                     RANGES=${RANGES/--xcut 15 100/--xcut 10 30};
                     RANGES=${RANGES/--xline 20 --xline 45/--xline 10 --xline 20};
                     RANGES=${RANGES/--yrange 0 0.??/--yrange 0 0.12};
                 elif [[ "$trigger" == "PFJet6" ]]; then
                     XVAR="mvaPt075_low"
                     MCEFF="${MCEFF/mvaPt075_coarse/$XVAR}"
                     RANGES=${RANGES/--xcut 15 100/--xcut 10 30};
                     RANGES=${RANGES/--xline 20 --xline 45/--xline 10 --xline 20};
                     RANGES=${RANGES/--yrange 0 0.??/--yrange 0 0.12};
                 fi;
            ;;
        esac;
        MCEFF="$MCEFF $LEGEND $RANGES"
        echo " ( $MCEFF -o $PBASE/fr_sub_eta_${BARREL}.root --bare -A veto eta 'abs(LepGood_eta)<$ETA' $BG )"
        echo " ( $MCEFF -o $PBASE/fr_sub_eta_${ENDCAP}.root --bare -A veto eta 'abs(LepGood_eta)>$ETA' $BG )"
        MCGO="$MCEFF --compare ${QCD}_red_prefit,data_sub_syst_prefit,data_sub_prefit --algo=globalFit "
        echo " ( $MCGO -i $PBASE/fr_sub_eta_${BARREL}.root -o $PBASE/fr_sub_eta_${BARREL}_globalFit.root --algo=globalFit --fcut 0 20 --subSyst 0.1 $BG )"
        echo " ( $MCGO -i $PBASE/fr_sub_eta_${ENDCAP}.root -o $PBASE/fr_sub_eta_${ENDCAP}_globalFit.root --algo=globalFit --fcut 0 20 --subSyst 0.1 $BG )"
        MCGO="$MCEFF --compare ${QCD}_red_prefit,data_prefit,total_prefit,data_sub_syst_prefit,data_sub_prefit --algo=globalFit "
        MCGO="${MCGO/--yrange 0 0.??/--yrange 0 0.5}"
        echo " ( $MCGO -i $PBASE/fr_sub_eta_${BARREL}.root -o $PBASE/fr_sub_eta_${BARREL}_globalFit_full.root --algo=globalFit --fcut 0 20 --subSyst 0.1 $BG )"
        echo " ( $MCGO -i $PBASE/fr_sub_eta_${ENDCAP}.root -o $PBASE/fr_sub_eta_${ENDCAP}_globalFit_full.root --algo=globalFit --fcut 0 20 --subSyst 0.1 $BG )"
        #MCGO="$MCEFF --compare ${QCD}_red_prefit,${QCD}_red --algo=fitND "
        #echo " ( $MCGO -i $PBASE/fr_sub_eta_${BARREL}.root -o $PBASE/fr_sub_eta_${BARREL}_full.root   $BG )"
        #echo " ( $MCGO -i $PBASE/fr_sub_eta_${ENDCAP}.root -o $PBASE/fr_sub_eta_${ENDCAP}_full.root   $BG )"
        MCGO="$MCEFF --compare ${QCD}_red_prefit,data_fit --algo=fitSimND --shapeSystSignal=l:0.2,s:0.1,b:0.01 --shapeSystBackground=l:0.1,s:0.05,b:0.01 "
        echo " ( $MCGO -i $PBASE/fr_sub_eta_${BARREL}.root -o $PBASE/fr_sub_eta_${BARREL}_fitSimND.root  $BG )"
        echo " ( $MCGO -i $PBASE/fr_sub_eta_${ENDCAP}.root -o $PBASE/fr_sub_eta_${ENDCAP}_fitSimND.root  $BG )"
        MCGO="$MCEFF --compare ${QCD}_red_prefit,data_fqcd --algo=fQCD "
        echo " ( $MCGO -i $PBASE/fr_sub_eta_${BARREL}.root -o $PBASE/fr_sub_eta_${BARREL}_fQCD.root --algo=fQCD  $BG )"
        echo " ( $MCGO -i $PBASE/fr_sub_eta_${ENDCAP}.root -o $PBASE/fr_sub_eta_${ENDCAP}_fQCD.root --algo=fQCD  $BG )"
        STACK="python ttH-multilepton/stack_fake_rates_data.py $RANGES $LEGEND "
        PATT="mvaPt_075i_vs_ptJI85_${XVAR}_${fitVar}_%s"
        for E in ${BARREL} ${ENDCAP}; do
            echo "( $STACK -o $PBASE/fr_sub_eta_${E}_comp.root    $PBASE/fr_sub_eta_${E}_globalFit.root:$PATT:${QCD}_red_prefit,data_sub_syst_prefit  $PBASE/fr_sub_eta_${E}_fQCD.root:$PATT:${QCD}_red_prefit,data_fqcd   $PBASE/fr_sub_eta_${E}_fitSimND.root:$PATT:data_fit   )";
        done
       ;;

esac;
