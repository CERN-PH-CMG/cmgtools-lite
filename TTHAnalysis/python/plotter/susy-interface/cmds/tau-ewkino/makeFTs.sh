#!/bin/bash


if [ "$1" == "btag" ]; then
    #python susy-interface/friendmaker.py 3l 3lA /pool/ciencias/HeppyTrees/RA7/estructura/trees_8011_July5_allscans/ /pool/ciencias/HeppyTrees/RA7/estructura/trees_8011_July5_allscans/ --modules eventBTagWeight -q batch 
    # python susy-interface/friendmaker.py 3l 3lA /pool/ciencias/HeppyTrees/RA7/estructura/trees_8011_July5_allscans/ /pool/ciencias/HeppyTrees/RA7/estructura/testbtag/ --modules eventBTagWeight --accept WZZ -q batch --direct

    python susy-interface/friendmaker.py 3l 3lA /pool/ciencias/HeppyTrees/RA7/estructura/trees_8011_July5_allscans/ /pool/ciencias/HeppyTrees/RA7/estructura/testbtag/ --modules eventBTagWeight --accept WZZ -q local --direct --pretend

elif [ "$1" == "taus" ]; then
    # python susy-interface/friendmaker.py 3l 3lA /pool/ciencias/HeppyTrees/RA7/estructura/trees_8011_July5_allscans/ /pool/ciencias/HeppyTrees/RA7/estructura/testbtag/ --modules leptonJetReCleanerNoCleanTausSusyEWK3L --accept WZZ -q local --direct --pretend
    python susy-interface/friendmaker.py 3l 3lA /pool/ciencias/HeppyTrees/RA7/estructura/trees_8011_July5_allscans/ /pool/ciencias/HeppyTrees/RA7/estructura/testbtag/ --modules tauFakesBuilderEWKMini --accept WZZ -q local --direct --pretend
    # python susy-interface/friendmaker.py 3l 3lA /pool/ciencias/HeppyTrees/RA7/estructura/trees_8011_July5_allscans/ /pool/ciencias/HeppyTrees/RA7/estructura/testbtag/ --modules tauFakesBuilderEWKRecl   --accept WZZ -q local --direct --pretend

fi

exit 0
