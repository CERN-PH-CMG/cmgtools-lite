################################
#  use mcEfficiencies.py to make plots of the fake rate
################################
T="/afs/cern.ch/user/g/gpetrucc/w/TREES_TTH_260116_76X_1L"
if hostname | grep -q cmsco01; then
    T="/data1/gpetrucc/TREES_TTH_260116_76X_1L"
fi
BCORE=" --s2v --tree treeProducerSusyMultilepton ttH-multilepton/mca-qcd1l.txt ttH-multilepton/qcd1l.txt -P $T -l 2.26 --AP  "

BG=" -j 6 "; if [[ "$1" == "-b" ]]; then BG=" & "; shift; fi

lepton=$1; if [[ "$1" == "" ]]; then exit 1; fi
case $lepton in
mu) BCORE="${BCORE} -E ${lepton} --xf 'DoubleEG.*'  "; QCD=QCDMu; ;;
el) BCORE="${BCORE} -E ${lepton} --xf 'DoubleMu.*'  "; QCD=QCDEl; ;;
esac;

trigger=$2; if [[ "$2" == "" ]]; then exit 1; fi
BCORE="${BCORE} -A veto trigger HLT_FR_${trigger} --mcc ttH-multilepton/mcc-eleIdEmu2.txt  "; 
PUW=" -L ttH-multilepton/frPuReweight.cc -W 'puw$trigger(nVert)' "

what=$3;
more=$4
PBASE="plots/76X/ttH/fr-meas/v1.0/$lepton/HLT_$trigger/$what/$more"

EWKONE="-p ${QCD}_red,EWK,data"
EWKSPLIT="-p ${QCD}_red,WJets,DYJets,data"
FITEWK=" $EWKSPLIT --peg-process DYJets WJets --flp WJets,DYJets,${QCD}_red "

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
    fitmtW1)
        echo "python mcPlots.py -f -j 6 $BCORE $PUW ttH-multilepton/qcd1l_plots.txt --pdir $PBASE -E $what --fitData $FITEWK --sP ${what/fit/} --showRatio --maxRatioRange 0.0 1.99 " 
        ;;
    num-fitmtW1)
        echo "python mcPlots.py -f -j 6 $BCORE $PUW ttH-multilepton/qcd1l_plots.txt --pdir $PBASE -E $what --fitData $FITEWK --sP ${what/num-fit/} --showRatio --maxRatioRange 0.0 1.99 -E num" 
        ;;
    num|den)
        echo "python mcPlots.py -f -j 6 $BCORE $PUW ttH-multilepton/qcd1l_plots.txt --pdir $PBASE -E $what $FITEWK --preFitData mtW1  --showRatio --maxRatioRange 0.0 1.99 " 
        ;;
    cuts-num)
        echo "python mcPlots.py -f -j 6 $BCORE $PUW ttH-multilepton/qcd1l_plots.txt --pdir $PBASE -E num $EWKONE --scale-process EWK $SC_EWK --scale-process ${QCD}_red $SC_QCD  --showRatio --maxRatioRange 0.0 1.99  -A veto mt25 'mt_2(met_pt,met_phi,LepGood_pt,LepGood_phi) < 15'  " 
        ;;
    num45)
        echo "python mcPlots.py -f -j 6 $BCORE $PUW ttH-multilepton/qcd1l_plots.txt --pdir $PBASE -E num $EWKONE --scale-process EWK $SC_EWK --scale-process ${QCD}_red $SC_QCD  --showRatio --maxRatioRange 0.0 1.99  -A veto pt45 'LepGood_pt > 45'  " 
        ;;
    cuts-num45)
        echo "python mcPlots.py -f -j 6 $BCORE $PUW ttH-multilepton/qcd1l_plots.txt --pdir $PBASE -E num $EWKONE --scale-process EWK $SC_EWK --scale-process ${QCD}_red $SC_QCD  --showRatio --maxRatioRange 0.0 1.99  -A veto mt25 'mt_2(met_pt,met_phi,LepGood_pt,LepGood_phi) < 15'  -A veto pt45 'LepGood_pt > 45' " 
        ;;
    fakerates-*)
        fitVar=${what/fakerates-/}
        BCORE="${BCORE/mca-qcd1l.txt/mca-qcd1l-fit.txt}"
        MCEFF="  python ttH-multilepton/dataFakeRate.py -f  $BCORE $PUW $EWKONE  --groupBy cut ttH-multilepton/make_fake_rates_sels.txt ttH-multilepton/make_fake_rates_xvars.txt  "
        MCEFF="$MCEFF --sp ${QCD}_red  "
        MCEFF="$MCEFF --sP mvaPt_075i --sP ptJI85_mvaPt075_coarse  --sP $fitVar $fitVar  --ytitle 'Fake rate' "
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
        PATT="mvaPt_075i_vs_ptJI85_mvaPt075_coarse_mtW1R_%s"
        for E in ${BARREL} ${ENDCAP}; do
            echo "( $STACK -o $PBASE/fr_sub_eta_${E}_comp.root    $PBASE/fr_sub_eta_${E}_globalFit.root:$PATT:${QCD}_red_prefit,data_sub_syst_prefit  $PBASE/fr_sub_eta_${E}_fQCD.root:$PATT:${QCD}_red_prefit,data_fqcd   $PBASE/fr_sub_eta_${E}_fitSimND.root:$PATT:data_fit   )";
        done
       ;;

esac;
