
T=/afs/cern.ch/work/g/gpetrucc/TREES_HZZ4L_231115/4L/EcalCorr_v2
BASE="python mcPlots.py --s2v -f -j 8 -P $T mca.txt -l 2.53 "
PDIR=plots/251115/4l/ecalCorr_v2/

WHAT=$1; shift;
POST=""; if [[ $2 != "" ]]; then POST=$2; shift; fi;
case $WHAT in
z4l)
    echo "( $BASE --pdir=$PDIR/$WHAT/$POST cuts.txt plots.txt -E z4l $*  --sp ZZ,ggZZ --sP '.*z4l.*' --xP mela_mass_2d_z4l )";
    echo "( $BASE --pdir=$PDIR/$WHAT/$POST cuts.txt plots.txt -E z4l $*  --sp ZZ,ggZZ --sP 'mela_mass_2d_z4l' -p ZZ,data )";
    ;;
high)
    echo "( $BASE --pdir=$PDIR/$WHAT/$POST cuts.txt plots.txt -E high $*  --sp ZZ,ggZZ --sP 'm4l_high,mZ1,mZ2_high,mela' )";
    echo "( $BASE --pdir=$PDIR/$WHAT/$POST cuts.txt plots.txt -E high $*  --sp ZZ,ggZZ --sP 'mela_mass_2d_high' -p ZZ,ggZZ,data )";
    ;;
full)
    echo "( $BASE --pdir=$PDIR/$WHAT/$POST cuts.txt plots.txt $*  --sP 'm4l_[acl].,mZ1,mZ2_high' )";
    ;;
all)
    for W in z4l high ; do
        bash $0 $W;
    done
esac
