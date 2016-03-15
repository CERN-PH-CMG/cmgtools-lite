T=/afs/cern.ch/work/g/gpetrucc/TREES_HZZ4L_231115/3L 
PDIR=plots/251115/cr_zl

BASE=" -l 2.47 -P $T cr_zl/mca.txt cr_zl/cuts.txt --s2v " 
PLOTBASE="python mcPlots.py $BASE -j 8 -f --showRatio --maxRatioRange 0 2.48 cr_zl/plots.txt "

function doPlots {
    SUBDIR=$1; shift;
    echo "$PLOTBASE  --pdir $PDIR/$SUBDIR/mu/den -X num -A nWZ mu 'abs(WZ_lep3_pdgId)==13' $*"
    echo "$PLOTBASE  --pdir $PDIR/$SUBDIR/mu/num        -A nWZ mu 'abs(WZ_lep3_pdgId)==13' $*"
    echo "$PLOTBASE  --pdir $PDIR/$SUBDIR/el/den -X num -A nWZ el 'abs(WZ_lep3_pdgId)==11' $*"
    echo "$PLOTBASE  --pdir $PDIR/$SUBDIR/el/num        -A nWZ el 'abs(WZ_lep3_pdgId)==11' $*"
}
function doScaledPlots {
    SUBDIR=$1; shift;
    PLOT="${PLOTBASE/--showRatio/} --sp '.*' --scaleSigToData"
    echo "$PLOT  --pdir $PDIR/$SUBDIR/mu/den -X num -A nWZ mu 'abs(WZ_lep3_pdgId)==13' $*"
    echo "$PLOT  --pdir $PDIR/$SUBDIR/mu/num        -A nWZ mu 'abs(WZ_lep3_pdgId)==13' $*"
    echo "$PLOT  --pdir $PDIR/$SUBDIR/el/den -X num -A nWZ el 'abs(WZ_lep3_pdgId)==11' $*"
    echo "$PLOT  --pdir $PDIR/$SUBDIR/el/num        -A nWZ el 'abs(WZ_lep3_pdgId)==11' $*"
}
function doPromptFit {
    SUBDIR=$1; shift;
    CHANGE="-A nWZ met 'met_pt > 20' --fitData --flp WZ,Top,DY --peg-process Top WZ "
    J0="-A nWZ 0j 'nJet30 == 0' "
    J1="-A nWZ 1j 'Jet1_pt > 40'  --rebin 2"
    B1="-A nWZ 1b 'Jet1_pt > 40 && Jet1_btagCSV > 0.89' --rebin 2"

    echo "$PLOTBASE  --pdir $PDIR/$SUBDIR/mu/     -A nWZ mu 'abs(WZ_lep3_pdgId)==13' $CHANGE     --sP WZ  --sP 'mtW,met,mZ1_wide'   "
    echo "$PLOTBASE  --pdir $PDIR/$SUBDIR/mu/0j   -A nWZ mu 'abs(WZ_lep3_pdgId)==13' $CHANGE $J0 --sP WZ  --sP 'mtW,met,mZ1_wide'   "
    echo "$PLOTBASE  --pdir $PDIR/$SUBDIR/mu/1j40 -A nWZ mu 'abs(WZ_lep3_pdgId)==13' $CHANGE $J1 --sP Top --sP 'mtW,met,j1_.*,mZ1_wide' "
    echo "$PLOTBASE  --pdir $PDIR/$SUBDIR/mu/bj40 -A nWZ mu 'abs(WZ_lep3_pdgId)==13' $CHANGE $B1 --sP Top --sP 'mtW,met,j1_.*,mZ1_wide'  "

    echo "$PLOTBASE  --pdir $PDIR/$SUBDIR/el/     -A nWZ el 'abs(WZ_lep3_pdgId)==11' $CHANGE     --sP WZ  --sP 'mtW,met,mZ1_wide'   "
    echo "$PLOTBASE  --pdir $PDIR/$SUBDIR/el/0j   -A nWZ el 'abs(WZ_lep3_pdgId)==11' $CHANGE $J0 --sP WZ  --sP 'mtW,met,mZ1_wide'   "
    echo "$PLOTBASE  --pdir $PDIR/$SUBDIR/el/1j40 -A nWZ el 'abs(WZ_lep3_pdgId)==11' $CHANGE $J1 --sP Top --sP 'mtW,met,j1_.*,mZ1_wide' "
    echo "$PLOTBASE  --pdir $PDIR/$SUBDIR/el/bj40 -A nWZ el 'abs(WZ_lep3_pdgId)==11' $CHANGE $B1 --sP Top --sP 'mtW,met,j1_.*,mZ1_wide'  "
}

#doPlots prefit-nomet " $* ";
doPlots prefit  " -A nWZ met 'met_pt < 20' $* " ;
doScaledPlots prefit-scaled  " -A nWZ met 'met_pt < 20' $* " ;
doPlots postfit-mtW  " -A nWZ met 'met_pt < 20' --preFitData mtW  --flp DY --peg-process Top WZ $*" ;
doPlots postfit-l3pt " -A nWZ met 'met_pt < 20' --preFitData l3pt --flp DY --peg-process Top WZ $*" ;
doPromptFit prompt-fit " $*";
