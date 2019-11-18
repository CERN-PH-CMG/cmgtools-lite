#!/bin/bash
#run from /plotter, one dir up
#TODO 
#when skimming trees consider pietro's comment on MM that you have to add a year parameter
echo "output files will be written to ../../macros/diff/skimmedTrees_1<Y>; Y --> Year = 6, 7 or 8"
if [ "$1" == "2016" ]; then
python skimTreesNew.py -P /nfs/user/pvischia/tth/v6/NanoTrees_TTH_091019_v6pre_skim2lss/2016 --skim-friends --Fs {P}/0_jmeUnc_v1 --Fs {P}/2_scalefactors --Fs {P}/3_tauCount --Fs {P}/1_recl --Fs {P}/5_BDThtt_reco --Fs {P}/2lss_diff_Top-tagged --Fs {P}/2lss_diff_NoTop-tagged --mcc ttH-multilepton/lepchoice-ttH-FO.txt -L ttH-multilepton/functionsTTH.cc --mcc ttH-multilepton/mcc-METFixEE2017.txt -p ttH --tree NanoAOD --elist skimwork ttH-multilepton/mca-2lss-mc.txt ttH-multilepton/2lss_tight.txt ../../macros/diff/skimmedTrees_16

elif [ "$1" == "2017" ]; then
python skimTreesNew.py -P /nfs/user/pvischia/tth/v6/NanoTrees_TTH_091019_v6pre_skim2lss/2017 --skim-friends --Fs {P}/0_jmeUnc_v1 --Fs {P}/2_scalefactors --Fs {P}/3_tauCount --Fs {P}/1_recl --Fs {P}/5_BDThtt_reco --Fs {P}/2lss_diff_Top-tagged --Fs {P}/2lss_diff_NoTop-tagged --mcc ttH-multilepton/lepchoice-ttH-FO.txt -L ttH-multilepton/functionsTTH.cc --mcc ttH-multilepton/mcc-METFixEE2017.txt -p ttH --tree NanoAOD --elist skimwork ttH-multilepton/mca-2lss-mc.txt ttH-multilepton/2lss_tight.txt ../../macros/diff/skimmedTrees_17

elif [ "$1" == "2018" ]; then
python skimTreesNew.py -P /nfs/user/pvischia/tth/v6/NanoTrees_TTH_091019_v6pre_skim2lss/2018 --skim-friends --Fs {P}/0_jmeUnc_v1 --Fs {P}/2_scalefactors --Fs {P}/3_tauCount --Fs {P}/1_recl --Fs {P}/5_BDThtt_reco --Fs {P}/2lss_diff_Top-tagged --Fs {P}/2lss_diff_NoTop-tagged --mcc ttH-multilepton/lepchoice-ttH-FO.txt -L ttH-multilepton/functionsTTH.cc --mcc ttH-multilepton/mcc-METFixEE2017.txt -p ttH --tree NanoAOD --elist skimwork ttH-multilepton/mca-2lss-mc.txt ttH-multilepton/2lss_tight.txt ../../macros/diff/skimmedTrees_18
else
echo "ERROR: enter a correct year; either 2016, 2017 or 2018"
fi
