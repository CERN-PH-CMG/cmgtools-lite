T=/afs/cern.ch/work/g/gpetrucc/TREES_HZZ4L_231115/4L
BASE="python mcPlots.py --s2v -f -j 8 -P $T cr_zll/mca.txt -l 2.47 "
PDIR=plots/251115/cr_zll

WHAT=$1; shift;
POST=""; if [[ $1 != "" ]]; then POST=$1; shift; fi;
case $WHAT in
ss|2p2f|3p1f)
    BASE="$BASE --mcc cr_zll/mcc-$WHAT.txt cr_zll/cuts.txt cr_zll/plots.txt --showRatio --maxRatioRange 0 2.48"
    REBIN="1"; [[ "$WHAT" == "3p1f" ]] && REBIN=2;
    for ll in all 2x2e 2x2mu; do
        case $ll in
            all)   RUN="$BASE "; SUB="" ;;
            2x2e)  RUN="$BASE -A hlt 2x2e 'abs(zz1_z2_l1_pdgId)==11' "; SUB="$ll" ;;
            2x2mu) RUN="$BASE -A hlt 2x2mu 'abs(zz1_z2_l1_pdgId)==13' "; SUB="$ll"; REBIN=$(( $REBIN * 2 ));;
        esac;
        echo "( $RUN --pdir=$PDIR/$WHAT/$POST/$SUB --rebin $REBIN $* )";
        echo "( $RUN --pdir=$PDIR/$WHAT/$POST/$SUB/fits    --sP mZ1_wide,met --fitData --flp DY,Top --rebin $(( $REBIN * 2 )) $* )";
        echo "( ${RUN/--showRatio/} --pdir=$PDIR/$WHAT/$POST/$SUB/zscaled --scaleSigToData --sp DY --rebin $(( $REBIN * 2 )) $* )";
    done
    ;;
all)
    for W in ss 2p2f 3p1f; do
        bash $0 $W;
    done
esac
