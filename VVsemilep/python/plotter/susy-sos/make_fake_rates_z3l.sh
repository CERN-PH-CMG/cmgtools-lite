################################
#  use mcEfficiencies.py to make plots of the fake rate
################################
T="/afs/cern.ch/user/g/gpetrucc/w/TREES_80X_SOS_130716_3L"
if hostname | grep -q cmsco01; then
    T="/data1/gpetrucc/TREES_80X_SOS_130716_3L"
fi
BCORE=" --s2v --tree treeProducerSusyMultilepton susy-sos/mca-fr-z3l.txt susy-sos/fr-z3l.txt -P $T -l 12.9 --AP  "

BG=" -j 6 "; if [[ "$1" == "-b" ]]; then BG=" & "; shift; fi

lepton=$1; if [[ "$1" == "" ]]; then exit 1; fi
case $lepton in
mu) BCORE="${BCORE} -E ^${lepton} "; ;;
el) BCORE="${BCORE} -E ^${lepton} "; ;;
esac;

what=$2; shift; shift;
PBASE="plots/80X/sos/fr-meas/z3l/v2.1.1/$lepton/$what"


case $lepton in
    el) BARREL="00_15"; ENDCAP="15_25"; ETA="1.479" ;;
    mu) BARREL="00_12"; ENDCAP="12_24"; ETA="1.2"   ;;
esac;

FITEWK=" -p ZZ,WZ,DY,TT,data --peg-process ZZ WZ --flp ZZ,WZ,DY "
FITDY=" --flp DY $SCALEWK "
PUW=" -L susy-sos/frPuReweight.cc -W 'puwZ3l(nVert)' "

case $what in
    nvtx)
        echo "python mcPlots.py -f -j 6 $BCORE susy-sos/make_fake_rates_xvars.txt --pdir $PBASE --sP nvtx $EWKONE " 
        echo "echo; echo; ";
        echo "python ../tools/vertexWeightFriend.py no $PBASE/make_fake_rates_xvars.root ";
        echo "echo; echo ' ---- Now you should put the normalization and weight into susy-sos/frPuReweight.cc defining puwZ3l ----- ' ";
        ;;
    nvtx-closure)
        echo "python mcPlots.py -f -j 6 $BCORE $PUW susy-sos/make_fake_rates_xvars.txt --pdir $PBASE --sP nvtx $EWKONE  --showRatio --maxRatioRange 0.8 1.2 " 
        ;;
#    fit*)
#        echo "python mcPlots.py -f -j 6 $BCORE $PUW susy-sos/make_fake_rates_xvars.txt --pdir $PBASE -E $what $FITEWK --preFitData ${what/fit/} --sP ${what/fit/} --showRatio --maxRatioRange 0.0 1.99 $* " 
#        ;;
#    num-fit*)
#        echo "python mcPlots.py -f -j 6 $BCORE $PUW susy-sos/make_fake_rates_xvars.txt --pdir $PBASE -E $what $FITEWK --preFitData ${what/num-fit/} --sP ${what/num-fit/} --showRatio --maxRatioRange 0.0 1.99 -E num $* " 
#        ;;
#    prefit-num|prefit-den)
#        echo "python mcPlots.py -f -j 6 $BCORE $PUW susy-sos/make_fake_rates_xvars.txt --pdir $PBASE -E ${what/prefit-/} --showRatio --maxRatioRange 0.0 1.99 --sP mZ1,mtW3,met_log,l3.* " 
#        ;;
    scaled-num|scaled-den)
        echo "python mcPlots.py -f -j 6 $BCORE $PUW susy-sos/make_fake_rates_xvars.txt --pdir $PBASE $FITEWK -E ${what/scaled-/} --showRatio --maxRatioRange 0.0 1.99 --sP ev_.*,nvtx,pt_fine,lep_.*,mtW3.* --preFitData mtW3 " 
        ;;
#    cuts-num|cuts-den)
#        CUTS="  -A 3l mt25 'met_pt < 25' "
#        echo "python mcPlots.py -f -j 6 $BCORE $PUW susy-sos/make_fake_rates_xvars.txt --pdir $PBASE $FITEWK -E ${what/cuts-/} --showRatio --maxRatioRange 0.0 1.99 --sP ev_.*,nvtx,pt_fine,lep_.* --preFitData mtW3 $CUTS " 
#        ;;
    fakerates-*)
        fitVar=${what/fakerates-/}
        Num=SOS_IdIsoDxyz;
        MCEFF="  python ttH-multilepton/dataFakeRate.py -f  $BCORE $PUW -p DY,VZ,data --groupBy cut susy-sos/make_fake_rates_sels.txt  susy-sos/make_fake_rates_xvars.txt  "
        MCEFF="$MCEFF --sp DY --sP ${Num}  "
        MCEFF="$MCEFF --sP $fitVar $fitVar  --ytitle 'Fake rate' "
        case $lepton in
        el) XVAR="pt_fine_ext"; MCEFF="$MCEFF --sP $XVAR " ;;
        mu) XVAR="pt_fine_ext"; MCEFF="$MCEFF --sP $XVAR " ;;
        esac;
        MCEFF="$MCEFF  " # ratio for fake rates
        MCEFF="$MCEFF --fixRatioRange --maxRatioRange 0.5 1.79 " # ratio for other plots
        LEGEND=" --legend=TL --fontsize 0.05 --legendWidth 0.4"
        RANGES=" --showRatio  --ratioRange 0.00 2.99 "
        case $lepton in  
           el) RANGES="$RANGES  --yrange 0 1.0 --xline 30 "; MCEFF="$MCEFF --fqcd-ranges 0 40 60 140" ;;
           mu) RANGES="$RANGES  --yrange 0 1.0 --xline 30 "; MCEFF="$MCEFF --fqcd-ranges 0 40 60 140" ;;
        esac;
        MCEFF="$MCEFF $LEGEND $RANGES"
        echo " ( $MCEFF -o $PBASE/fr_sub_eta_${BARREL}.root --bare -A cleanup eta 'abs(LepGood_eta)<$ETA' $BG )"
        echo " ( $MCEFF -o $PBASE/fr_sub_eta_${ENDCAP}.root --bare -A cleanup eta 'abs(LepGood_eta)>$ETA' $BG )"
        MCGO="$MCEFF --compare DY_prefit,data_sub_syst_prefit,data_sub_prefit --algo=globalFit "
        echo " ( $MCGO -i $PBASE/fr_sub_eta_${BARREL}.root -o $PBASE/fr_sub_eta_${BARREL}_globalFit.root --algo=globalFit --rebin 2 --fcut 0 40 --subSyst 0.1 $BG )"
        echo " ( $MCGO -i $PBASE/fr_sub_eta_${ENDCAP}.root -o $PBASE/fr_sub_eta_${ENDCAP}_globalFit.root --algo=globalFit --rebin 2 --fcut 0 40 --subSyst 0.1 $BG )"
        MCGO="$MCEFF --compare DY_prefit,data_prefit,total_prefit,data_sub_syst_prefit,data_sub_prefit --algo=globalFit "
        echo " ( $MCGO -i $PBASE/fr_sub_eta_${BARREL}.root -o $PBASE/fr_sub_eta_${BARREL}_globalFit_full.root --algo=globalFit --rebin 2 --fcut 0 40 --subSyst 0.1 $BG )"
        echo " ( $MCGO -i $PBASE/fr_sub_eta_${ENDCAP}.root -o $PBASE/fr_sub_eta_${ENDCAP}_globalFit_full.root --algo=globalFit --rebin 2 --fcut 0 40 --subSyst 0.1 $BG )"
        MCGO="$MCEFF --compare DY_prefit,data_fit --algo=fitSimND --shapeSystSignal=l:0.2,s:0.1,b:0.01 --shapeSystBackground=l:0.1,s:0.05,b:0.01 "
        echo " ( $MCGO -i $PBASE/fr_sub_eta_${BARREL}.root -o $PBASE/fr_sub_eta_${BARREL}_fitSimND.root --same-nd-templates --rebin 2 $BG )"
        echo " ( $MCGO -i $PBASE/fr_sub_eta_${ENDCAP}.root -o $PBASE/fr_sub_eta_${ENDCAP}_fitSimND.root --same-nd-templates --rebin 2 $BG )"
        MCGO="$MCEFF --compare DY_prefit,data_fqcd --algo=fQCD "
        echo " ( $MCGO -i $PBASE/fr_sub_eta_${BARREL}.root -o $PBASE/fr_sub_eta_${BARREL}_fQCD.root --algo=fQCD  $BG )"
        echo " ( $MCGO -i $PBASE/fr_sub_eta_${ENDCAP}.root -o $PBASE/fr_sub_eta_${ENDCAP}_fQCD.root --algo=fQCD  $BG )"
        STACK="python ttH-multilepton/stack_fake_rates_data.py $RANGES $LEGEND --xtitle 'lepton p_{T} (GeV)' "
        PATT="${Num}_vs_${XVAR}_${fitVar}_%s"
        for E in ${BARREL} ${ENDCAP}; do
            echo "( $STACK -o $PBASE/fr_sub_eta_${E}_comp.root    $PBASE/fr_sub_eta_${E}_globalFit.root:$PATT:DY_prefit,data_sub_syst_prefit  $PBASE/fr_sub_eta_${E}_fQCD.root:$PATT:DY_prefit,data_fqcd   $PBASE/fr_sub_eta_${E}_fitSimND.root:$PATT:data_fit   )";
        done
       ;;

esac;
