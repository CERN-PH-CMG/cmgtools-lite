
INPUTDIR="/pool/ciencias/HeppyTrees/RA7/estructura/trees_8011_July5_allscans/"
OUTPUTDIR="/pool/ciencias/HeppyTrees/RA7/estructura/testbtag/"

if [ "$1" == "ft" ]; then
    MODULE=""    
    PRETEND=" -q local --direct --pretend"
    PRETEND=" -q batch --direct "
    ONLY=" --accept WZZ "
    ONLY="" 
    if [ "$2" == "btag" ]; then
        MODULE="eventBTagWeight"
        #python susy-interface/friendmaker.py 3l 3lA ${INPUTDIR} ${INPUTDIR} --modules eventBTagWeight -q batch 
        # python susy-interface/friendmaker.py 3l 3lA ${INPUTDIR} ${OUTPUTDIR} --modules eventBTagWeight --accept WZZ -q batch --direct
        python susy-interface/friendmaker.py 3l 3lA ${INPUTDIR} ${OUTPUTDIR} --modules ${MODULE} ${ONLY} ${PRETEND}
    else
        if [ "$2" == "tauclean" ]; then
            MODULE="leptonJetReCleanerNoCleanTausSusyEWK3L"
        elif [ "$2" == "tauMini" ]; then
            MODULE="tauFakesBuilderEWKMini"
        elif [ "$2" == "tauRecl" ]; then
            MODULE="tauFakesBuilderEWKRecl"
        fi
        if [ "$MODULE" == "" ]; then
            print "No module specified"
            exit -1
        fi
        python susy-interface/friendmaker.py taustudies 3lA ${INPUTDIR} ${OUTPUTDIR} --modules ${MODULE} ${ONLY} ${PRETEND}
    fi
elif [ "$1" == "plot" ]; then
    
    ACTION=${2}
    # ACTION can be generalplots or tauopt
    SUBACTION=""
    if [ "$3" != "" ]; then
        SUBACTION=" -s ${3} "
    fi
    PRETEND=" --pretend "
    
  python susy-interface/cmds/tau-ewkino/plot.py -i ${INPUTDIR} -o ${OUTPUTDIR} ${SUBACTION} ${PRETEND}
    
fi

exit 0
