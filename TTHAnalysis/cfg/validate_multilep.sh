RUN=/bin/false;
if [[ "$1" == "-run" ]]; then RUN=/bin/true; shift; fi;

if [[ "$1" == "" ]]; then echo "Usage: validate_multilep.sh [ -run ] <what> [dir = 'Trash' + <what> ]"; exit 1; fi;  
WHAT=$1; shift;
DIR=$1; if [[ "$1" == "" ]]; then DIR="Trash$WHAT"; fi;
DIR=$PWD/$DIR; ## make absolute

function do_run {
    CFG=$1; shift
    name=$1; [[ "$name" == "" ]] && return; shift;
    echo "Will run as $name";
    rm -r $name 2> /dev/null
    echo "heppy $name $CFG -p 0 -o nofetch $*"
    heppy $name $CFG -p 0 -o nofetch $*
    if ls -1 $name/ | grep -q _Chunk0; then (cd $name; rm *_Chunk*/cmsswPreProcessing.root 2> /dev/null; haddChunks.py -c .); fi; 
    echo "Run done. press enter to continue (ctrl-c to break)";
    read DUMMY;
}
function do_plot {
    PROC=$1; PROCR=$2; LABEL=$3; RVER=$4
    if [[ "${PROCR}" == "" ]]; then return; fi;
    if test \! -d ${DIR}/${PROC}; then echo "Did not find ${PROC} in ${DIR}"; exit 1; fi
    if [[ "${RVER}" == "" ]]; then RVER=94X; fi;
    if [[ "${LABEL}" != "MANUAL" ]]; then 
        test -L ${DIR}/Ref && rm ${DIR}/Ref    
        test -L ${DIR}/New && rm ${DIR}/New    
        if test -d ~/Reference_${RVER}_${PROCR}${LABEL}; then
             ln -sd ~/Reference_${RVER}_${PROCR}${LABEL} ${DIR}/Ref;
        else
             ln -sd $PWD/Reference_${RVER}_${PROCR}${LABEL} ${DIR}/Ref;
        fi
    else
        test -L ${DIR}/Ref && rm ${DIR}/Ref    
        test -L ${DIR}/New && rm ${DIR}/New    
        if test -d ${DIR}/${PROCR}; then
            ln -sd ${DIR}/${PROCR} ${DIR}/Ref
        elif test -d ${PROCR}; then
            ln -sd ${PROCR}  ${DIR}/Ref
            PROCR=$(basename ${PROCR})
        fi;
    fi
    ln -sd ${DIR}/${PROC} ${DIR}/New;
    OUTNAME=${WHAT}-${PROCR}${LABEL}
    ( cd ../python/plotter;
      # ---- MCA ---
      MCA=susy-multilepton/validation_mca.txt
      # ---- CUT FILE ---
      CUTS=susy-multilepton/validation.txt;
      if [ -f susy-multilepton/validation-${PROC}.txt ]; then 
        CUTS=susy-multilepton/validation-${PROC}.txt
      elif echo $PROC | grep -q Run201[67]; then
        if echo $PROC | grep -q Single; then
             CUTS=susy-multilepton/validation-data-single.txt
        elif echo $PROC | grep -q 'MET\|2017'; then
             CUTS=susy-multilepton/validation.txt
        else
             CUTS=susy-multilepton/validation-data.txt
        fi;
      fi
      python mcPlots.py -f --s2v --tree treeProducerSusyMultilepton  -P ${DIR} $MCA $CUTS ${CUTS/.txt/_plots.txt} \
              --pdir plots/94X/validation/${OUTNAME} -p new,ref -u -e \
              --plotmode=nostack --showRatio --maxRatioRange 0.65 1.35 --flagDifferences
    );
}
function do_size {
    PROC=$1; SUB=$2; 
    perl /afs/cern.ch/user/g/gpetrucc/pl/treeSize.pl $DIR/$PROC/treeProducerSusyMultilepton/tree.root > ../python/plotter/plots/94X/validation/treeSize/${PROC}${SUB}.html
}


case $WHAT in
    ttHData)
        $RUN && do_run run_ttH_cfg.py $DIR -o test=94X-Data  -N 10000 -o runData;
        do_plot DoubleMuon_Run2017C DoubleMuon_Run2017C
        do_plot DoubleEG_Run2017E DoubleEG_Run2017E
        ;;
    ttHMC)
        $RUN && do_run run_ttH_cfg.py $DIR -o test=94X-MC -o sample=TTLep -N 2000;
        do_plot TTLep_pow TTLep_pow
        ;;
    ttHSpeed)
        $RUN && do_run run_ttH_cfg.py $DIR -o test=94X-MC -o sample=TTSemi -N 10000 -t -o fast -o single;
        do_plot TTSemi TTSemi
        ;;
    ttHMCSize)
        $RUN && do_run run_ttH_cfg.py $DIR -o test=94X-MC -o sample=TTLep -o fast;
        do_size TTLep_pow
        do_plot TTLep_pow TTLep_pow big
        ;;
    ttHDataSize)
        $RUN && do_run run_ttH_cfg.py $DIR -o test=94X-Data  -N 100000 -o runData -o fast;
        do_size DoubleMuon_Run2017C 
        do_size DoubleEG_Run2017E
        do_plot DoubleMuon_Run2017C DoubleMuon_Run2017C big
        do_plot DoubleEG_Run2017E DoubleEG_Run2017E big
        ;;
    ttHData80X)
        $RUN && do_run run_ttH_cfg.py $DIR -o test=80X-Data  -N 10000 -o runData -o run80X;
        do_plot DoubleMuon_Run2016H_run283885 DoubleMuon_Run2016H_run283885 "" 80X
        do_plot DoubleEG_Run2016H_run283885 DoubleEG_Run2016H_run283885 "" 80X
        ;;
    ttHMC80X)
        $RUN && do_run run_ttH_cfg.py $DIR -o test=80X-MC -o sample=TTLep  -o run80X -N 2000;
        do_plot TTLep_pow TTLep_pow "" 80X
        ;;
    SOSData)
        $RUN && do_run run_susyMultilepton_cfg.py $DIR -o test=94X-Data  -N 40000 -o runData -o sample=DoubleMuon  -o analysis=SOS;
        do_plot DoubleMuon_Run2017C_run299649 DoubleMuon_Run2017C_run299649 _SOS
        ;;
    SOSData80X)
        $RUN && do_run run_susyMultilepton_cfg.py $DIR -o test=80X-Data  -N 100000 -o runData -o sample=MET  -o analysis=SOS;
        do_plot MET_Run2016H_run283885 MET_Run2016H_run283885 _SOS 80X
        ;;
    SOSMC)
        $RUN && do_run run_susyMultilepton_cfg.py $DIR -o test=94X-MC -o sample=TTLep -N 2000 -o analysis=SOS;
        do_plot TTLep_pow TTLep_pow _SOS
        ;;
    SOSMC80X)
        $RUN && do_run run_susyMultilepton_cfg.py $DIR -o test=80X-MC -o sample=TTLep -N 2000 -o analysis=SOS;
        do_plot TTLep_pow TTLep_pow _SOS 80X
        ;;

    -manual)
        O=$3; if [[ "$4" != "" ]]; then O=$4; fi
        do_plot $2 $3 MANUAL $O
        ;;
    *)
        echo "Test for $WHAT not implemented";
        ;;
esac;
