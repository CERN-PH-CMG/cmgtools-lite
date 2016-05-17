################################
#  use mcEfficiencies.py to make plots of the fake rate
################################
T="NON_ESISTE"
if hostname | grep -q cmsco01; then
    T="/data1/peruzzi/TREES_76X_200216_jecV1M2/"
fi

BCORE=" --s2v --tree treeProducerSusyMultilepton ttH-multilepton/mca-fr-z3l.txt ttH-multilepton/fr-z3l.txt -P $T -l 2.32 --AP  "
BCORE="$BCORE --mcc ttH-multilepton/ttH_2lss3l_triggerdefs.txt "

BG=" -j 6 "; if [[ "$1" == "-b" ]]; then BG=" & "; shift; fi

lepton=$1; if [[ "$1" == "" ]]; then exit 1; fi
case $lepton in
mu) BCORE="${BCORE} -E ${lepton} -E tightZ1 "; ;;
el) BCORE="${BCORE} -E ${lepton} "; ;;
esac;

what=$2; shift; shift;
PBASE="plots/76X/ttH/fr-meas/z3l/v1.2/$lepton/$what"


case $lepton in
    el) BARREL="00_15"; ENDCAP="15_25"; ETA="1.479"; SC_EWK=1.58;  SC_DY=0.86;;
    mu) BARREL="00_12"; ENDCAP="12_24"; ETA="1.2";   SC_EWK=1.57;  SC_DY=0.84;;
esac;

FITEWK=" -p ZZ,WZ,DY,TT,data --peg-process ZZ WZ --flp ZZ,WZ,DY "
FITDY=" --flp DY $SCALEWK "
PUW=" -L ttH-multilepton/frPuReweight.cc -W 'puwZ3l(nVert)' "

case $what in
    nvtx)
        echo "python mcPlots.py -f -j 6 $BCORE ttH-multilepton/fr-z3l_plots.txt --pdir $PBASE --sP nvtx $EWKONE " 
        echo "echo; echo; ";
        echo "python ../tools/vertexWeightFriend.py no $PBASE/fr-z3l_plots.root ";
        echo "echo; echo ' ---- Now you should put the normalization and weight into frPuReweight.cc defining puwZ3l ----- ' ";
        ;;
    nvtx-closure)
        echo "python mcPlots.py -f -j 6 $BCORE $PUW ttH-multilepton/fr-z3l_plots.txt --pdir $PBASE --sP nvtx $EWKONE  --showRatio --maxRatioRange 0.8 1.2 " 
        ;;
    fit*)
        echo "python mcPlots.py -f -j 6 $BCORE $PUW ttH-multilepton/fr-z3l_plots.txt --pdir $PBASE -E $what $FITEWK --preFitData ${what/fit/} --sP ${what/fit/} --showRatio --maxRatioRange 0.0 1.99 $* " 
        ;;
    num-fit*)
        echo "python mcPlots.py -f -j 6 $BCORE $PUW ttH-multilepton/fr-z3l_plots.txt --pdir $PBASE -E $what $FITEWK --preFitData ${what/num-fit/} --sP ${what/num-fit/} --showRatio --maxRatioRange 0.0 1.99 -E num $* " 
        ;;
    prefit-num|prefit-den)
        echo "python mcPlots.py -f -j 6 $BCORE $PUW ttH-multilepton/fr-z3l_plots.txt --pdir $PBASE -E ${what/prefit-/} --showRatio --maxRatioRange 0.0 1.99 --sP mZ1,mtW3,met_log,l3.* " 
        ;;
    scaled-num|scaled-den)
        echo "python mcPlots.py -f -j 6 $BCORE $PUW ttH-multilepton/fr-z3l_plots.txt --pdir $PBASE $FITDY -E ${what/scaled-/} --showRatio --maxRatioRange 0.0 1.99 --sP mZ1,mtW3,met_log,l3.* --preFitData mtW3 " 
        ;;
    cuts-num|cuts-den)
        CUTS="  -A 3l mt25 'met_pt < 25' "
        echo "python mcPlots.py -f -j 6 $BCORE $PUW ttH-multilepton/fr-z3l_plots.txt --pdir $PBASE $FITDY -E ${what/cuts-/} --showRatio --maxRatioRange 0.0 1.99 --sP mtW3,met_log,l3CPt_c --preFitData mtW3 $CUTS " 
        ;;
    fakerates-old)
        MCEFF="  python mcEfficiencies.py -f  $BCORE $PUW $SCALEWK --groupBy cut ttH-multilepton/fr-z3l_pass.txt  ttH-multilepton/fr-z3l_plots.txt  "
        MCEFF="$MCEFF  --sp DY --sP mva075 "
        case $lepton in
        el) MCEFF="$MCEFF --sP l3CPt_[c1]  " ;;
        mu) MCEFF="$MCEFF --sP l3CPt_1     " ;;
        esac;
        MCEFF="$MCEFF   --compare DY,data_sub,data,total,background --showRatio --ratioRange 0.0 1.99 "
        MCEFF="$MCEFF  --yrange 0 0.3  --ytitle 'Fake rate' --xcut 10 100 "
        MCEFF="$MCEFF  -A 3l mt25 'met_pt < 25' "
        #MCEFF="$MCEFF  -A veto mt25 'mt_2(met_pt,met_phi,LepGood_pt[2],LepGood_phi[2]) < 15' "
        echo " ( $MCEFF -o $PBASE/fr_sub_eta_${BARREL}.root  -A 3l eta 'abs(LepGood_eta[2])<$ETA' $BG )"
        echo " ( $MCEFF -o $PBASE/fr_sub_eta_${ENDCAP}.root  -A 3l eta 'abs(LepGood_eta[2])>$ETA' $BG )"
        ;;
    fakerates-*)
        fitVar=${what/fakerates-/}
        MCEFF="  python ttH-multilepton/dataFakeRate.py -f  $BCORE $PUW -p DY,VZ,data --groupBy cut ttH-multilepton/fr-z3l_pass.txt  ttH-multilepton/fr-z3l_plots.txt  "
        MCEFF="$MCEFF --sp DY --sP mva075  "
        MCEFF="$MCEFF --sP $fitVar $fitVar  --ytitle 'Fake rate' "
        case $lepton in
        el) XVAR="l3CPt_2"; MCEFF="$MCEFF --sP $XVAR " ;;
        mu) XVAR="l3CPt_1"; MCEFF="$MCEFF --sP $XVAR " ;;
        esac;
        MCEFF="$MCEFF  " # ratio for fake rates
        MCEFF="$MCEFF --fixRatioRange --maxRatioRange 0.5 1.79 " # ratio for other plots
        LEGEND=" --legend=TL --fontsize 0.05 --legendWidth 0.4"
        RANGES=" --showRatio  --ratioRange 0.00 2.99 "
        STACK="python ttH-multilepton/stack_fake_rates_data.py "
        case $lepton in  
           el) RANGES="$RANGES  --yrange 0 0.10 --xline 30 "; MCEFF="$MCEFF --fqcd-ranges 0 40 40 140" ;;
           mu) RANGES="$RANGES  --yrange 0 0.10 --xline 20 "; MCEFF="$MCEFF --fqcd-ranges 0 40 40 140" ;;
        esac;
        MCEFF="$MCEFF $LEGEND $RANGES"
        echo " ( $MCEFF -o $PBASE/fr_sub_eta_${BARREL}.root --bare -A cleanup eta 'abs(LepGood_eta)<$ETA' $BG )"
        echo " ( $MCEFF -o $PBASE/fr_sub_eta_${ENDCAP}.root --bare -A cleanup eta 'abs(LepGood_eta)>$ETA' $BG )"
        MCGO="$MCEFF --compare DY_prefit,data_sub_syst_prefit,data_sub_prefit --algo=globalFit "
        echo " ( $MCGO -i $PBASE/fr_sub_eta_${BARREL}.root -o $PBASE/fr_sub_eta_${BARREL}_globalFit.root --algo=globalFit --rebin 2 --fcut 0 40 --subSyst 0.1 $BG )"
        echo " ( $MCGO -i $PBASE/fr_sub_eta_${ENDCAP}.root -o $PBASE/fr_sub_eta_${ENDCAP}_globalFit.root --algo=globalFit --rebin 2 --fcut 0 40 --subSyst 0.1 $BG )"
        MCGO="$MCEFF --compare DY_prefit,data_prefit,total_prefit,data_sub_syst_prefit,data_sub_prefit --algo=globalFit "
        MCGO="${MCGO/--yrange 0 0.??/--yrange 0 0.2}"
        echo " ( $MCGO -i $PBASE/fr_sub_eta_${BARREL}.root -o $PBASE/fr_sub_eta_${BARREL}_globalFit_full.root --algo=globalFit --rebin 2 --fcut 0 40 --subSyst 0.1 $BG )"
        echo " ( $MCGO -i $PBASE/fr_sub_eta_${ENDCAP}.root -o $PBASE/fr_sub_eta_${ENDCAP}_globalFit_full.root --algo=globalFit --rebin 2 --fcut 0 40 --subSyst 0.1 $BG )"
        MCGO="$MCEFF --compare DY_prefit,data_fit --algo=fitSimND --shapeSystSignal=l:0.2,s:0.1,b:0.01 --shapeSystBackground=l:0.1,s:0.05,b:0.01 "
        echo " ( $MCGO -i $PBASE/fr_sub_eta_${BARREL}.root -o $PBASE/fr_sub_eta_${BARREL}_fitSimND.root --same-nd-templates --rebin 2 $BG )"
        echo " ( $MCGO -i $PBASE/fr_sub_eta_${ENDCAP}.root -o $PBASE/fr_sub_eta_${ENDCAP}_fitSimND.root --same-nd-templates --rebin 2 $BG )"
        MCGO="$MCEFF --compare DY_prefit,data_fqcd --algo=fQCD "
        echo " ( $MCGO -i $PBASE/fr_sub_eta_${BARREL}.root -o $PBASE/fr_sub_eta_${BARREL}_fQCD.root --algo=fQCD  $BG )"
        echo " ( $MCGO -i $PBASE/fr_sub_eta_${ENDCAP}.root -o $PBASE/fr_sub_eta_${ENDCAP}_fQCD.root --algo=fQCD  $BG )"
        STACK="python ttH-multilepton/stack_fake_rates_data.py $RANGES $LEGEND "
        PATT="mva075_vs_${XVAR}_${fitVar}_%s"
        for E in ${BARREL} ${ENDCAP}; do
            echo "( $STACK -o $PBASE/fr_sub_eta_${E}_comp.root    $PBASE/fr_sub_eta_${E}_globalFit.root:$PATT:DY_prefit,data_sub_syst_prefit  $PBASE/fr_sub_eta_${E}_fQCD.root:$PATT:DY_prefit,data_fqcd   $PBASE/fr_sub_eta_${E}_fitSimND.root:$PATT:data_fit   )";
        done
       ;;


esac;
