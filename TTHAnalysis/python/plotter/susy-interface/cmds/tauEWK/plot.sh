#python mcPlots.py susy-ewkino/3l/mca_ewkino.txt susy-ewkino/3l/cuts_ewkino.txt susy-ewkino/3l/plots_ewkino.txt -P /pool/ciencias/HeppyTrees/RA7/8011_July22/ --neg --s2v --tree treeProducerSusyMultilepton -f -j 4 --legendWidth 0.20 --legendFontSize 0.035 --mcc susy-ewkino/3l/mcc_ewkino.txt --load-macro susy-ewkino/3l/functionsEWK.cc --showRatio -l 12.9 --pdir   ~/www/susyRA7/ -F sf/t {P}/leptonJetReCleanerSusyEWK3L/evVarFriend_{cname}.root -F sf/t {P}/leptonBuilderEWK/evVarFriend_{cname}.root -F sf/t {P}/eventBTagWeight/evVarFriend_{cname}.root -p data -p fakes_appldata -p promptsub -p prompt_.* -p rares_.* -p convs --sP lep.*._pt --sP *._eta --sP flavor3l --sP charge3l -A alwaystrue BRcut 'BR==1' -X blinding --perBin --ratioOffset 0.03 --print C,png,pdf,txt --plotgroup rares_ttX+=rares_ttW --plotgroup rares_ttX+=rares_ttZ --plotgroup fakes_appldata+=promptsub --cms --legendHeader 'A: OSSF' -W 'puw2016_nInt_12p9fb(nTrueInt)*triggerSF()*leptonSF()*eventBTagSF'



#python susy-interface/plotmaker.py 3l 3lA /pool/ciencias/HeppyTrees/RA7/8011_June29/  ~/www/susyRA7/ -l 12.9 --make data --plots lep -o SR

python susy-interface/plotmaker.py 3l 3lA /pool/ciencias/HeppyTrees/RA7/estructura/trees_8011_July5_allscans/  ~/www/susyRA7/ -l 12.9 --make data --plots lep -o SR


