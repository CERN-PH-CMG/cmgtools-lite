T=/afs/cern.ch/work/g/gpetrucc/TREES_HZZ4L_231115/3L 
PDIR=plots/251115/cr_zl/effs

BASE=" -l 2.47 -P $T cr_zl/mca.txt cr_zl/cuts.txt --s2v " 
EFFBASE="python mcEfficiencies.py $BASE -X num -j 8 -f --showRatio cr_zl/nums.txt cr_zl/plots.txt --groupBy cut "

function doFRs {
    SUBDIR=$1; shift;
    EFF="$EFFBASE --AP -p DY,data,WZ,Top --sp WZ --compare DY,total,data "
    EFF="$EFF     --sP pass --sP l3pt_coarse --yrange 0 0.2 --ratioRange 0 2.8 --legend=TL"
    echo "$EFF -o $PDIR/$SUBDIR/mu_barrel.root -A nWZ mu 'abs(WZ_lep3_pdgId)==13 && abs(WZ_lep3_eta)<1.2  '  $*"
    echo "$EFF -o $PDIR/$SUBDIR/mu_endcap.root -A nWZ mu 'abs(WZ_lep3_pdgId)==13 && abs(WZ_lep3_eta)>1.2  '  $*"
    echo "$EFF -o $PDIR/$SUBDIR/el_barrel.root -A nWZ el 'abs(WZ_lep3_pdgId)==11 && abs(WZ_lep3_eta)<1.479'  $*"
    echo "$EFF -o $PDIR/$SUBDIR/el_endcap.root -A nWZ el 'abs(WZ_lep3_pdgId)==11 && abs(WZ_lep3_eta)>1.479'  $*"
}

doFRs prefit  " -A nWZ met 'met_pt < 25' $* " ;
doFRs prefit-mZ_10GeV  " -A nWZ met 'met_pt < 25 && abs(WZ_z_mass-91.1876)<10 ' $* " ;
doFRs prefit-mZ_7GeV   " -A nWZ met 'met_pt < 25 && abs(WZ_z_mass-91.1876)<7  ' $* " ;

