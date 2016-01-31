################################
#  use mcEfficiencies.py to make plots of the fake rate
################################
T="/afs/cern.ch/work/p/peruzzi/tthtrees/TREES_74X_140116_MiniIso_tauClean_Mor16lepMVA/"
if hostname | grep -q cmsphys10; then
    T="/data/p/peruzzi/TREES_74X_140116_MiniIso_tauClean_Mor16lepMVA"
fi

BCORE=" --s2v --tree treeProducerSusyMultilepton ttH-multilepton/mca-fr-z3l.txt ttH-multilepton/fr-z3l.txt -P $T -l 2.26 --AP  "
BCORE="$BCORE --mcc ttH-multilepton/ttH_2lss3l_triggerdefs.txt "

BG=" -j 6 "; if [[ "$1" == "-b" ]]; then BG=" & "; shift; fi

lepton=$1; if [[ "$1" == "" ]]; then exit 1; fi
case $lepton in
mu) BCORE="${BCORE} -E ${lepton} "; ;;
el) BCORE="${BCORE} -E ${lepton} "; ;;
esac;

what=$2;
PBASE="plots/74X/ttH/fr-meas/z3l/v1.1/$lepton/$what"


case $lepton in
    el) BARREL="00_15"; ENDCAP="15_25"; ETA="1.479"; SC_EWK=1.54;  SC_DY=0.82;;
    mu) BARREL="00_12"; ENDCAP="12_24"; ETA="1.2";   SC_EWK=1.55;  SC_DY=0.96;;
esac;

SCALEWK=" --scale-process [WZ]Z $SC_EWK --scale-process DY $SC_DY  "
FITEWK=" --peg-process ZZ WZ --flp ZZ,WZ,DY "
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
        echo "python mcPlots.py -f -j 6 $BCORE $PUW ttH-multilepton/fr-z3l_plots.txt --pdir $PBASE --sP nvtx $EWKONE  --showRatio --maxRatioRange 0.9 1.1 " 
        ;;
    fitmtW1)
        echo "python mcPlots.py -f -j 6 $BCORE $PUW ttH-multilepton/fr-z3l_plots.txt --pdir $PBASE -E $what --fitData $FITEWK --sP ${what/fit/} --showRatio --maxRatioRange 0.0 1.99 " 
        ;;
    num-fitmtW3)
        echo "python mcPlots.py -f -j 6 $BCORE $PUW ttH-multilepton/fr-z3l_plots.txt --pdir $PBASE -E $what --fitData $FITEWK --sP ${what/num-fit/} --showRatio --maxRatioRange 0.0 1.99 -E num" 
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
    fakerates)
        MCEFF="  python mcEfficiencies.py -f  $BCORE $PUW $SCALEWK --groupBy cut ttH-multilepton/fr-z3l_pass.txt  ttH-multilepton/fr-z3l_plots.txt  "
        MCEFF="$MCEFF  --sp DY --sP mva06 "
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
esac;
