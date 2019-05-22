#!/bin/bash
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
    if test -f $name; then
        echo "ERROR: $name is a file.";
        return;
    fi
    rm -r $name 2> /dev/null
    echo "heppy $name $CFG -p 0 -o nofetch $*"
    heppy $name $CFG -p 0 -o nofetch $*
    if ls -1 $name/ | grep -q _Chunk0; then (cd $name; rm *_Chunk*/cmsswPreProcessing.root 2> /dev/null; haddChunks.py -c .); fi; 
    echo "Run done. press enter to continue (ctrl-c to break)";
    read DUMMY;
}

function do_nano {
    CFG=$1; shift
    name=$1; [[ "$name" == "" ]] && return; shift;
    echo "Will run as $name";
    if test -f $name; then
        echo "ERROR: $name is a file.";
        return;
    fi
    rm -r $name 2> /dev/null
    echo "nanopy.py $name $CFG $*"
    nanopy.py $name $CFG $*
    if ls -1 $name/ | grep -q _Chunk0; then (cd $name; rm *_Chunk*/cmsswPreProcessing.root 2> /dev/null; haddChunks.py -n -c .); fi; 
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
    echo "Run done. press enter to continue (ctrl-c to break)";
    read DUMMY;
}
function do_plot {
    PROC=$1; PROCR=$2; LABEL=$3; RVER=$4; shift; shift; shift; shift;
    if [[ "${PROCR}" == "" ]]; then return; fi;
    if test  -d ${DIR}/${PROC} || test -d ${DIR}/New; then 
        NANOAOD=false; TESTARG="-d"; LNARG="-sd"; POST="";
    elif test  -f ${DIR}/${PROC}.root || test -f ${DIR}/New.root; then 
        NANOAOD=true; TESTARG="-f"; LNARG="-s"; POST=".root";
    else
        echo "Did not find ${PROC} or New in ${DIR}"; exit 1; 
    fi
    if [[ "${RVER}" == "" ]]; then RVER=94X; fi;
    if [[ "${KEEP_REF}" == "1" ]]; then
        if test \! -d ${DIR}/Ref && test \! -f ${DIR}/Ref.root; then
            echo "KEEP_REF set to 1 but I can't find a reference"; exit 1;
        fi
    elif [[ "${LABEL}" != "MANUAL" ]]; then 
        for X in Ref Ref.root New New.root; do test -L ${DIR}/$X && rm ${DIR}/$X; done
        if test ${TESTARG} ~/Reference_${RVER}_${PROCR}${LABEL}${POST}; then
             ln $LNARG ~/Reference_${RVER}_${PROCR}${LABEL}${POST} ${DIR}/Ref${POST};
        elif test ${TESTARG} $PWD/Reference_${RVER}_${PROCR}${LABEL}${POST}; then
             ln $LNARG $PWD/Reference_${RVER}_${PROCR}${LABEL}${POST} ${DIR}/Ref${POST};
        else
             echo "No idea where to take the reference from"; exit 1; 
        fi
    else
        for X in Ref Ref.root New New.root; do test -L ${DIR}/$X && rm ${DIR}/$X; done
        if test ${TESTARG} ${DIR}/${PROCR}${POST}; then
            ln $LNARG ${DIR}/${PROCR}${POST} ${DIR}/Ref${POST}
        elif test ${TESTARG} ${PROCR}${POST}; then
            ln $LNARG ${PROCR}${POST}  ${DIR}/Ref${POST}
            PROCR=$(basename ${PROCR} ${POST})
        fi;
    fi
    test ${TESTARG} ${DIR}/New${POST} || ln $LNARG ${DIR}/${PROC}${POST} ${DIR}/New${POST};
    OUTNAME=${WHAT}-${PROCR}${LABEL}
    ( cd ../python/plotter;
      # ---- MCA, CUT & PLOT FILE ---
      [[ "${MCA}" == "" ]] && MCA=susy-multilepton/validation_mca.txt
      [[ "${CUTS}" == "" ]] && CUTS=susy-multilepton/validation.txt
      [[ "${PLOTS}" == "" ]] && PLOTS=${CUTS/.txt/_plots.txt}
      if $NANOAOD; then
          TREE=NanoAOD
      else
          [[ "${TREE}" == "" ]] && TREE=treeProducerSusyMultilepton
      fi;
      echo "python mcPlots.py -f --s2v --tree $TREE  -P ${DIR} $MCA $CUTS ${PLOTS} \
              --pdir plots/104X/validation/${OUTNAME}  -u -e $* \
              --plotmode=nostack --showRatio --maxRatioRange 0.65 1.35 --flagDifferences"
      python mcPlots.py -f --s2v --tree $TREE  -P ${DIR} $MCA $CUTS ${PLOTS} \
              --pdir plots/104X/validation/${OUTNAME}  -u -e $* \
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
        CUTS=susy-multilepton/validation-data.txt
        do_plot DoubleMuon_Run2017C DoubleMuon_Run2017C
        do_plot DoubleEG_Run2017E DoubleEG_Run2017E
        ;;
    ttHMC)
        $RUN && do_run run_ttH_cfg.py $DIR -o test=94X-MC -o sample=TTLep -N 2000;
        do_plot TTLep_pow TTLep_pow
        ;;
    ttHMC-recl)
        if test -d ${DIR/-recl/}; then
            if $RUN; then
                test -d $DIR || mkdir $DIR || exit 1;
                test -d $DIR/New || cp -a ${DIR/-recl/}/{Ref,New,TTLep_pow} $DIR || exit 1;
                test -d $DIR/1_recleaner_v0 || cp -r ~/Reference_94X_TTLep_pow_friends/[0-9]_* $DIR || exit 1;
                do_friends_heppy $DIR ttHMC New;
            fi;
            PLOTS=ttH-multilepton/validation/recl_plots.txt
            KEEP_REF=1
            do_plot TTLep_pow TTLep_pow "" "" --Fs {P}/1_recleaner_v0 --Fs {P}/2_eventVars_v0 -L ttH-multilepton/functionsTTH.cc --mcc ttH-multilepton/lepchoice-ttH-FO.txt
        else
            echo "first run ttHMC";
        fi
        ;;
    nano_ttHMC)
        $RUN && do_nano run_ttH_fromNanoAOD_cfg.py $DIR -o test=94X-MC
        PLOTS=ttH-multilepton/validation/nanoaod_plots.txt
        do_plot TTLep_pow TTLep_pow
        ;;
    nano_ttHMC-vs_cmg)
        BASE=${DIR/nano_ttHMC-vs_cmg/}
        if test -d ${BASE}ttHMC && test -d ${BASE}nano_ttHMC; then
            test -d $DIR || mkdir $DIR || exit 1;
            test -L $DIR/New.root || ln -s  ${BASE}nano_ttHMC/New.root $DIR/New.root 
            test -L $DIR/Ref      || ln -sd ${BASE}ttHMC/New           $DIR/Ref
            MCA=ttH-multilepton/validation/nanoaod-vs-cmg_mca.txt
            PLOTS=ttH-multilepton/validation/nanoaod_plots.txt
            KEEP_REF=1
            do_plot TTLep_pow TTLep_pow
        else
            echo "first run ttHMC and nano_ttHMC";
        fi
        ;;
    nano_ttHMC-recl)
        if test -d ${DIR/-recl/}; then
            if $RUN; then
                test -d $DIR || mkdir $DIR || exit 1;
                test -d $DIR/New.root || cp -a ${DIR/-recl/}/{Ref.root,New.root} $DIR || exit 1;
                test -d $DIR/1_recleaner_v0 || cp -r ~/Reference_94X_TTLep_pow_nanoaod_friends/[0-9]_* $DIR || exit 1;
                MODS=CMGTools.TTHAnalysis.tools.nanoAOD.ttH_modules
                nano_postproc.py -I $MODS recleaner_step1,recleaner_step2_mc --friend ${DIR}/1_recleaner_v0 ${DIR}/New.root
                nano_postproc.py -I $MODS eventVars                          --friend ${DIR}/2_eventVars_v0 ${DIR}/New.root,${DIR}/1_recleaner_v0/New_Friend.root
                echo "Run done. press enter to continue (ctrl-c to break)";
                read DUMMY;
            fi;
            PLOTS=ttH-multilepton/validation/nanoaod-recl_plots.txt
            KEEP_REF=1
            do_plot TTLep_pow TTLep_pow "" "" --Fs {P}/1_recleaner_v0 --Fs {P}/2_eventVars_v0 -L ttH-multilepton/functionsTTH.cc --mcc ttH-multilepton/lepchoice-ttH-FO.txt
        else
            echo "first run nano_ttHMC";
        fi
        ;;
    nano_ttHMC-recl-vs_cmg)
        BASE=${DIR/nano_ttHMC-recl-vs_cmg/}
        if test -d ${BASE}ttHMC-recl && test -d ${BASE}nano_ttHMC-recl; then
            test -d $DIR || mkdir $DIR || exit 1;
            test -L $DIR/New.root || ln -s  ${BASE}nano_ttHMC-recl/New.root $DIR/New.root 
            test -L $DIR/Ref      || ln -sd ${BASE}ttHMC-recl/New           $DIR/Ref
            for F in 1_recleaner_v0 2_eventVars_v0; do
                test -d $DIR/$F || mkdir $DIR/$F || exit 1;
                test -L $DIR/$F/New_Friend.root      || ln -s ${BASE}nano_ttHMC-recl/$F/New_Friend.root  $DIR/$F/
                test -L $DIR/$F/evVarFriend_Ref.root || ln -s ${BASE}ttHMC-recl/$F/evVarFriend_Ref.root $DIR/$F/
            done
            MCA=ttH-multilepton/validation/nanoaod-vs-cmg_mca.txt
            PLOTS=ttH-multilepton/validation/nanoaod-recl_plots.txt
            KEEP_REF=1
            do_plot TTLep_pow TTLep_pow "" "" --Fs {P}/1_recleaner_v0 --Fs {P}/2_eventVars_v0 -L ttH-multilepton/functionsTTH.cc --mcc ttH-multilepton/lepchoice-ttH-FO.txt
        else
            echo "first run ttHMC-recl and nano_ttHMC-recl";
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
        CUTS=susy-multilepton/validation-data.txt
        do_size DoubleMuon_Run2017C 
        do_size DoubleEG_Run2017E
        do_plot DoubleMuon_Run2017C DoubleMuon_Run2017C _big
        do_plot DoubleEG_Run2017E DoubleEG_Run2017E _big
        ;;
    ttHDataPresc)
        $RUN && do_run run_ttH_cfg.py $DIR -o test=94X-Data  -N 100000 -o runData -o fast -o prescaleskim;
        CUTS=susy-multilepton/validation-data.txt
        do_plot DoubleMuon_Run2017C DoubleMuon_Run2017C _big 94X --WA prescaleFromSkim
        do_plot DoubleEG_Run2017E DoubleEG_Run2017E _big 94X --WA prescaleFromSkim
        ;;
    ttHData80X)
        $RUN && do_run run_ttH_cfg.py $DIR -o test=80X-Data  -N 10000 -o runData -o run80X;
        CUTS=susy-multilepton/validation-data.txt
        do_plot DoubleMuon_Run2016H_run283885 DoubleMuon_Run2016H_run283885 "" 80X
        do_plot DoubleEG_Run2016H_run283885 DoubleEG_Run2016H_run283885 "" 80X
        ;;
    ttHMC80X)
        $RUN && do_run run_ttH_cfg.py $DIR -o test=80X-MC -o sample=TTLep  -o run80X -N 2000;
        CUTS=susy-multilepton/validation-data.txt
        do_plot TTLep_pow TTLep_pow "" 80X
        ;;
    SOSData)
        $RUN && do_run run_susyMultilepton_cfg.py $DIR -o test=94X-Data  -N 40000 -o runData -o sample=DoubleMuon  -o analysis=SOS;
        CUTS=susy-multilepton/validation-data.txt
        do_plot DoubleMuon_Run2017C_run299649 DoubleMuon_Run2017C_run299649 _SOS
        ;;
    SOSData80X)
        $RUN && do_run run_susyMultilepton_cfg.py $DIR -o test=80X-Data  -N 100000 -o runData -o sample=MET  -o analysis=SOS;
        CUTS=susy-multilepton/validation.txt
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
