################################
#  use mcEfficiencies.py to make plots of the fake rate
################################
T="NON_ESISTE"
if hostname | grep -q cmsco01; then
    T="/data1/peruzzi/TREES_TTH_250117_Summer16_JECV3_noClean_qgV2"
fi

BG=" -j 6 "; if [[ "$1" == "-b" ]]; then BG=" & "; shift; fi

ANALYSIS=$1; if [[ "$1" == "" ]]; then exit 1; fi; shift;
case $ANALYSIS in
ttH) CUTFILE="ttH-multilepton/lepton-fr/fr-z3l.txt"; XVAR="l3CPt"; NUM="mva090";;
susy_wpM) CUTFILE="susy-ewkino/fr-z3l-wpM.txt"; XVAR="ptJIMIX4"; NUM="mvaSusy_sMi";;
susy_wpV) CUTFILE="susy-ewkino/fr-z3l-wpV.txt"; XVAR="ptJIMIX3"; NUM="mvaSusy_sVi";;
*) echo "unknown analysis $ANALYSIS"; exit 1; ;;
esac;

BCORE=" --s2v --tree treeProducerSusyMultilepton ttH-multilepton/lepton-fr/mca-fr-z3l.txt ${CUTFILE} -P $T -l  36.5 --AP --mcc ttH-multilepton/mcc-eleIdEmu2.txt "
BCORE="$BCORE --mcc ttH-multilepton/ttH_2lss3l_triggerdefs.txt -X ^Trig -A Z1 ptcuts 'LepGood_pt[0]>25 && LepGood_pt[1]>15' " # no trigger selection

lepton=$1; if [[ "$1" == "" ]]; then exit 1; fi
case $lepton in
mu) BCORE="${BCORE} -E ^${lepton} -E tightZ1 ";; #;--mcc ttH-multilepton/mcc-ichepMediumMuonId.txt "; ;;
el) BCORE="${BCORE} -E ^${lepton} -E tight70";; #--mcc ttH-multilepton/mcc-ichepMediumMuonId-fake.txt"; ;;
*) echo "unknown lepton $lepton"; exit 1; ;;
esac;

what=$2; shift; shift;
#PBASE="~/www/plots_FR/80X/lepMVA_${ANALYSIS}/v1.4_250616/fr-meas/$lepton/z3l/$what"
PBASE="plots/80X/${ANALYSIS}_Moriond17/lepMVA/v2.1-dev/fr-meas/z3l/$lepton/$what"

case $lepton in
    el) BARREL="00_15"; ENDCAP="15_25"; ETA="1.479"; SC_EWK=1.58;  SC_DY=0.86;;
    mu) BARREL="00_12"; ENDCAP="12_24"; ETA="1.2";   SC_EWK=1.57;  SC_DY=0.84;;
esac;

FITEWK=" -p ZZ,WZ,DY,TT,data --peg-process ZZ WZ --flp ZZ,WZ,DY "
FITDY=" --flp DY $SCALEWK "
PUW=" -L ttH-multilepton/lepton-fr/frPuReweight.cc -W 'puwZ3l(nVert)' "

case $what in
    nvtx)
        echo "python mcPlots.py -f -j 6 $BCORE ttH-multilepton/lepton-fr/fr-z3l_plots.txt --pdir $PBASE --sP nvtx $EWKONE " 
        echo "echo; echo; ";
        echo "python ../tools/vertexWeightFriend.py no $PBASE/fr-z3l_plots.root ";
        echo "echo; echo ' ---- Now you should put the normalization and weight into frPuReweight.cc defining puwZ3l ----- ' ";
        ;;
    nvtx-closure)
        echo "python mcPlots.py -f -j 6 $BCORE $PUW ttH-multilepton/lepton-fr/fr-z3l_plots.txt --pdir $PBASE --sP nvtx $EWKONE  --showRatio --maxRatioRange 0.8 1.2 " 
        ;;
    fit*)
        echo "python mcPlots.py -f -j 6 $BCORE $PUW ttH-multilepton/lepton-fr/fr-z3l_plots.txt --pdir $PBASE -E $what $FITEWK --preFitData ${what/fit/} --sP ${what/fit/} --showRatio --maxRatioRange 0.0 1.99 $* " 
        ;;
    num-fit*)
        echo "python mcPlots.py -f -j 6 $BCORE $PUW ttH-multilepton/lepton-fr/fr-z3l_plots.txt --pdir $PBASE -E $what $FITEWK --preFitData ${what/num-fit/} --sP ${what/num-fit/} --showRatio --maxRatioRange 0.0 1.99 -E num $* " 
        ;;
    prefit-num|prefit-den)
        echo "python mcPlots.py -f -j 6 $BCORE $PUW ttH-multilepton/lepton-fr/fr-z3l_plots.txt --pdir $PBASE -E ${what/prefit-/} --showRatio --maxRatioRange 0.0 1.99 --sP mZ1,mtW3,met_log,l3.* " 
        ;;
    scaled-num|scaled-den)
        echo "python mcPlots.py -f -j 6 $BCORE $PUW ttH-multilepton/lepton-fr/fr-z3l_plots.txt --pdir $PBASE $FITDY -E ${what/scaled-/} --showRatio --maxRatioRange 0.0 1.99 --sP mZ1,mtW3,met_log,l3.* --preFitData mtW3 " 
        ;;
    cuts-num|cuts-den)
        CUTS="  -A 3l mt25 'met_pt < 25' "
        echo "python mcPlots.py -f -j 6 $BCORE $PUW ttH-multilepton/lepton-fr/fr-z3l_plots.txt --pdir $PBASE $FITDY -E ${what/cuts-/} --showRatio --maxRatioRange 0.0 1.99 --sP mtW3,met_log,l3CPt_c --preFitData mtW3 $CUTS " 
        ;;
    fakerates-old)
        MCEFF="  python mcEfficiencies.py -f  $BCORE $PUW $SCALEWK --groupBy cut ttH-multilepton/lepton-fr/fr-z3l_pass.txt  ttH-multilepton/lepton-fr/fr-z3l_plots.txt  "
        MCEFF="$MCEFF  --sp DY --sP ${NUM} "
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
        MCEFF="  python ttH-multilepton/dataFakeRate.py -f  $BCORE $PUW -p DY,VZ,data --groupBy cut ttH-multilepton/lepton-fr/fr-z3l_pass.txt  ttH-multilepton/lepton-fr/fr-z3l_plots.txt  "
        MCEFF="$MCEFF --sp DY --sP ${NUM}  "
        MCEFF="$MCEFF --sP $fitVar $fitVar  --ytitle 'Fake rate' "
        case $lepton in
        el) XVAR="${XVAR}_2"; MCEFF="$MCEFF --sP $XVAR " ;;
        mu) XVAR="${XVAR}_1"; MCEFF="$MCEFF --sP $XVAR " ;;
        esac;
        MCEFF="$MCEFF  " # ratio for fake rates
        MCEFF="$MCEFF --fixRatioRange --maxRatioRange 0.5 1.79 " # ratio for other plots
        LEGEND=" --legend=TL --fontsize 0.05 --legendWidth 0.4"
        RANGES=" --showRatio  --ratioRange 0.00 2.99 "
        STACK="python ttH-multilepton/lepton-fr/stack_fake_rates_data.py "
        case $lepton in  
           el) RANGES="$RANGES  --yrange 0 0.10 --xline 30 "; MCEFF="$MCEFF --fqcd-ranges 0 40 40 140" ;;
           mu) RANGES="$RANGES  --yrange 0 0.10 --xline 20 "; MCEFF="$MCEFF --fqcd-ranges 0 40 40 140" ;;
        esac;
        MCEFF="$MCEFF $LEGEND $RANGES"
        echo " ( $MCEFF -o $PBASE/fr_sub_eta_${BARREL}.root --bare -A cleanup eta 'abs(LepGood_eta[2])<$ETA' $BG )"
        echo " ( $MCEFF -o $PBASE/fr_sub_eta_${ENDCAP}.root --bare -A cleanup eta 'abs(LepGood_eta[2])>$ETA' $BG )"
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
        STACK="python ttH-multilepton/lepton-fr/stack_fake_rates_data.py $RANGES $LEGEND "
        PATT="${NUM}_vs_${XVAR}_${fitVar}_%s"
        for E in ${BARREL} ${ENDCAP}; do
            echo "( $STACK -o $PBASE/fr_sub_eta_${E}_comp.root    $PBASE/fr_sub_eta_${E}_globalFit.root:$PATT:DY_prefit,data_sub_syst_prefit  $PBASE/fr_sub_eta_${E}_fQCD.root:$PATT:DY_prefit,data_fqcd   $PBASE/fr_sub_eta_${E}_fitSimND.root:$PATT:data_fit   )";
        done
       ;;


esac;
