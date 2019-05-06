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
function do_friends_heppy {
    pushd ../macros
    SRC=$1; shift;
    case $1 in
        ttHMC)
            echo "python prepareEventVariablesFriendTree.py --tra2 $SRC {P}/1_recleaner_v0 --tree treeProducerSusyMultilepton -I CMGTools.TTHAnalysis.tools.functionsTTH -m jetPtRatiov3 -m leptonJetFastReCleanerTTH_step1 -m leptonJetFastReCleanerTTH_step2_mc -d $2 -j 0"
            python prepareEventVariablesFriendTree.py --tra2 $SRC {P}/1_recleaner_v0 --tree treeProducerSusyMultilepton -I CMGTools.TTHAnalysis.tools.functionsTTH -m jetPtRatiov3 -m leptonJetFastReCleanerTTH_step1 -m leptonJetFastReCleanerTTH_step2_mc -d $2 -j 0
            python prepareEventVariablesFriendTree.py --tra2 $SRC {P}/2_eventVars_v0 --tree treeProducerSusyMultilepton -I CMGTools.TTHAnalysis.tools.functionsTTH -m eventVars -F sf/t {P}/1_recleaner_v0/evVarFriend_{cname}.root -d $2 -j 0
            ;;
        ttHData)
            python prepareEventVariablesFriendTree.py --tra2 $SRC {P}/1_recleaner_v0 --tree treeProducerSusyMultilepton -I CMGTools.TTHAnalysis.tools.functionsTTH -m jetPtRatiov3 -m leptonJetFastReCleanerTTH_step1 -m leptonJetFastReCleanerTTH_step2_data -d $2 -j 0
            python prepareEventVariablesFriendTree.py --tra2 $SRC {P}/2_eventVars_v0 --tree treeProducerSusyMultilepton -I CMGTools.TTHAnalysis.tools.functionsTTH -m eventVars -F sf/t {P}/1_recleaner_v0/evVarFriend_{cname}.root -d $2 -j 0
            ;;
    esac;
    popd
}
function do_plot {
    PROC=$1; PROCR=$2; LABEL=$3; RVER=$4; shift; shift; shift; shift;
    if [[ "${PROCR}" == "" ]]; then return; fi;
    if test \! -d ${DIR}/${PROC} && test \! -d ${DIR}/New; then echo "Did not find ${PROC} or New in ${DIR}"; exit 1; fi
    if [[ "${RVER}" == "" ]]; then RVER=94X; fi;
    if [[ "${PROCR}" == "Ref" ]]; then
        test -d ${DIR}/Ref && echo "Using existing Ref"
    elif [[ "${LABEL}" != "MANUAL" ]]; then 
        test -L ${DIR}/Ref && rm ${DIR}/Ref    
        test -L ${DIR}/New && rm ${DIR}/New    
        if test -d ~/Reference_${RVER}_${PROCR}${LABEL}; then
             ln -sd ~/Reference_${RVER}_${PROCR}${LABEL} ${DIR}/Ref;
        else
             ln -sd $PWD/Reference_${RVER}_${PROCR}${LABEL} ${DIR}/Ref;
        fi
        ln -sd ${DIR}/${PROC} ${DIR}/New;
    else
        test -L ${DIR}/Ref && rm ${DIR}/Ref    
        test -L ${DIR}/New && rm ${DIR}/New    
        if test -d ${DIR}/${PROCR}; then
            ln -sd ${DIR}/${PROCR} ${DIR}/Ref
        elif test -d ${PROCR}; then
            ln -sd ${PROCR}  ${DIR}/Ref
            PROCR=$(basename ${PROCR})
        fi;
        ln -sd ${DIR}/${PROC} ${DIR}/New;
    fi
    test -d ${DIR}/New || ln -sd ${DIR}/${PROC} ${DIR}/New;
    OUTNAME=${WHAT}-${PROCR}${LABEL}
    ( cd ../python/plotter;
      # ---- MCA ---
      MCA=susy-multilepton/validation_mca.txt
      if echo $PROC | grep -q Run201[2567]; then MCA=susy-multilepton/validation-data_mca.txt; fi;
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
      elif echo "X$LABEL" | grep -q [Rr]ecl; then
        CUTS=ttH-multilepton/validation-recl.txt
      fi
      WA=1; if echo $WHAT | grep -q Presc; then WA=prescaleFromSkim; fi;
      echo "python mcPlots.py -f --s2v --tree treeProducerSusyMultilepton  -P ${DIR} $MCA $CUTS ${CUTS/.txt/_plots.txt} \
              --pdir plots/104X/validation/${OUTNAME}  -u -e --WA $WA $* \
              --plotmode=nostack --showRatio --maxRatioRange 0.65 1.35 --flagDifferences"
      python mcPlots.py -f --s2v --tree treeProducerSusyMultilepton  -P ${DIR} $MCA $CUTS ${CUTS/.txt/_plots.txt} \
              --pdir plots/104X/validation/${OUTNAME}  -u -e --WA $WA $* \
              --plotmode=nostack --showRatio --maxRatioRange 0.65 1.35 --flagDifferences
    );
}
function do_size {
    PROC=$1; SUB=$2; 
    perl /afs/cern.ch/user/g/gpetrucc/pl/treeSize.pl $DIR/$PROC/treeProducerSusyMultilepton/tree.root > ../python/plotter/plots/104X/validation/treeSize/${PROC}${SUB}.html
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
    ttHMC_Recl)
        if test -d ${DIR/_Recl/}; then
            if $RUN; then
                test -d $DIR || mkdir $DIR || exit 1;
                test -d $DIR/New || cp -av ${DIR/_Recl/}/{Ref,New,TTLep_pow} $DIR || exit 1;
                test -d $DIR/1_recleaner_v0 || cp -rv ~/Reference_94X_TTLep_pow_friends/[0-9]_* $DIR || exit 1;
                do_friends_heppy $DIR ttHMC New;
            fi;
            do_plot TTLep_pow Ref -recl 94X --Fs {P}/1_recleaner_v0 --Fs {P}/2_eventVars_v0  -L ttH-multilepton/functionsTTH.cc --mcc ttH-multilepton/lepchoice-ttH-FO.txt
        else
            echo "first run ttHMC to create $DIR";
        fi
        ;;
    ttHSpeed)
        $RUN && do_run run_ttH_cfg.py $DIR -o test=94X-MC -o sample=TTSemi -N 10000 -t -o fast -o single;
        do_plot TTSemi TTSemi
        ;;
    ttHMCSize)
        $RUN && do_run run_ttH_cfg.py $DIR -o test=94X-MC -o sample=TTLep -o fast;
        do_size TTLep_pow
        do_plot TTLep_pow TTLep_pow _big
        ;;
    ttHDataSize)
        $RUN && do_run run_ttH_cfg.py $DIR -o test=94X-Data  -N 100000 -o runData -o fast;
        do_size DoubleMuon_Run2017C 
        do_size DoubleEG_Run2017E
        do_plot DoubleMuon_Run2017C DoubleMuon_Run2017C _big
        do_plot DoubleEG_Run2017E DoubleEG_Run2017E _big
        ;;
    ttHDataPresc)
        $RUN && do_run run_ttH_cfg.py $DIR -o test=94X-Data  -N 100000 -o runData -o fast -o prescaleskim;
        do_plot DoubleMuon_Run2017C DoubleMuon_Run2017C _big
        do_plot DoubleEG_Run2017E DoubleEG_Run2017E _big
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
