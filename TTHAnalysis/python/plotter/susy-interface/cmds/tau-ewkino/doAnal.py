#!/bin/bash


if [ "$1" == "btag" ]; then
    #python susy-interface/friendmaker.py 3l 3lA /pool/ciencias/HeppyTrees/RA7/estructura/trees_8011_July5_allscans/ /pool/ciencias/HeppyTrees/RA7/estructura/trees_8011_July5_allscans/ --modules eventBTagWeight -q batch 
    # python susy-interface/friendmaker.py 3l 3lA /pool/ciencias/HeppyTrees/RA7/estructura/trees_8011_July5_allscans/ /pool/ciencias/HeppyTrees/RA7/estructura/testbtag/ --modules eventBTagWeight --accept WZZ -q batch --direct

    python susy-interface/friendmaker.py 3l 3lA /pool/ciencias/HeppyTrees/RA7/estructura/trees_8011_July5_allscans/ /pool/ciencias/HeppyTrees/RA7/estructura/testbtag/ --modules eventBTagWeight --accept WZZ -q local --direct --pretend

elif [ "$1" == "taus" ]; then
    MODULE=""
    if [ "$2" == "" ]; then 
        MODULE="leptonJetReCleanerNoCleanTausSusyEWK3L"
    elif [ "$2" == "tauMini" ]; then
        MODULE="tauFakesBuilderEWKMini"
    elif [ "$2" == "tauRecl" ]; then
        MODULE="tauFakesBuilderEWKRecl"
    fi
    PRETEND=" -q local --direct --pretend"
    PRETEND=" -q batch --direct "
    ONLY=" --accept WZZ "
    ONLY="" 
    python susy-interface/friendmaker.py taustudies 3lA /pool/ciencias/HeppyTrees/RA7/estructura/trees_8011_July5_allscans/ /pool/ciencias/HeppyTrees/RA7/estructura/testbtag/ --modules ${MODULE} ${ONLY} ${PRETEND}

fi

exit 0
