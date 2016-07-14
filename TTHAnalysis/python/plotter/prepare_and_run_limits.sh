#!/bin/bash

#-- How to by R.C. -----------------------------
# Set here output dirs and types of limits 
type="_ddbkg" ## type of limits you want to extract
## can be: '_unblind' (observed), '_ddbkg' (expected data-driven bkg), '' (expected pure MC)
DIR=SR_ddbkg_test/  # local dir where all the temorary cards and histograms will be saved
version=result_v0  # if you want a different versioning inside the $DIR
WWWDIR=/afs/cern.ch/user/c/castello/www/susy-sos/ichep/pre_approval/limits/ ## Directory where you want to save the final results (combined final limits)
# ----------------------------------------------

########## EWKino #####################################
## SR EWKino 10 GeV
python susy-sos/sos_plots.py $DIR 2los_SR_bins_notriggers_ewk10_met125_mm$type | sh
python susy-sos/sos_plots.py $DIR 2los_SR_bins_notriggers_ewk10_met200$type | sh


## SR EWKino 20 GeV
python susy-sos/sos_plots.py $DIR 2los_SR_bins_notriggers_ewk20_met125_mm$type | sh
python susy-sos/sos_plots.py $DIR 2los_SR_bins_notriggers_ewk20_met200$type    | sh


############## STOP #####################################
## SR Stop 20 GeV
python susy-sos/sos_plots.py $DIR 2los_SR_bins_notriggers_stop20_met125_mm$type | sh
python susy-sos/sos_plots.py $DIR 2los_SR_bins_notriggers_stop20_met200$type | sh


## SR Stop 35 GeV
python susy-sos/sos_plots.py $DIR 2los_SR_bins_notriggers_stop35_met125_mm$type | sh
python susy-sos/sos_plots.py $DIR 2los_SR_bins_notriggers_stop35_met200$type | sh

############## CR #####################################
#python susy-sos/sos_plots.py $DIR 2los_CR_DY_vars_notrigger_met125 
#python susy-sos/sos_plots.py $DIR 2los_CR_DY_vars_notrigger_met200 
#python susy-sos/sos_plots.py $DIR 2los_CR_TT_vars_notrigger_met125 
#python susy-sos/sos_plots.py $DIR 2los_CR_TT_vars_notrigger_met200 

cd $DIR
cd ~/WorkArea/physics/limits/CMSSW_7_4_7/src/
eval `scramv1 runtime -sh`
cd -
echo "Creating $WWWDIR/$DIR_combined_limits directory"
mkdir $WWWDIR/$DIR
mkdir $version

#separate
echo "Running on separate datacards..."

if [ $type != "_unblind" ]  
then
    combine -M Asymptotic --run=blind -t -1 --datacard=TChiNeuWZ_80/2los_SR_bins_notriggers_ewk20_met125_mm$type.card.txt > $version/Asymp_2los_SR_bins_notriggers_ewk20_met125_mm.txt
    combine -M Asymptotic --run=blind -t -1 --datacard=TChiNeuWZ_80/2los_SR_bins_notriggers_ewk20_met200$type.card.txt > $version/Asymp_2los_SR_bins_notriggers_ewk20_met200.txt

    combine -M Asymptotic --run=blind -t -1 --datacard=TChiNeuWZ_90/2los_SR_bins_notriggers_ewk10_met125_mm$type.card.txt > $version/Asymp_2los_SR_bins_notriggers_ewk10_met125_mm.txt
    combine -M Asymptotic --run=blind -t -1 --datacard=TChiNeuWZ_90/2los_SR_bins_notriggers_ewk10_met200$type.card.txt > $version/Asymp_2los_SR_bins_notriggers_ewk10_met200.txt

    combine -M Asymptotic --run=blind -t -1 --datacard=T2ttDeg_330/2los_SR_bins_notriggers_stop20_met125_mm$type.card.txt > $version/Asymp_2los_SR_bins_notriggers_stop20_met125_mm.txt
    combine -M Asymptotic --run=blind -t -1 --datacard=T2ttDeg_330/2los_SR_bins_notriggers_stop20_met200$type.card.txt > $version/Asymp_2los_SR_bins_notriggers_stop20_met200.txt

    combine -M Asymptotic --run=blind -t -1 --datacard=T2ttDeg_315/2los_SR_bins_notriggers_stop35_met125_mm$type.card.txt > $version/Asymp_2los_SR_bins_notriggers_stop35_met125_mm.txt
    combine -M Asymptotic --run=blind -t -1 --datacard=T2ttDeg_315/2los_SR_bins_notriggers_stop35_met200$type.card.txt > $version/Asymp_2los_SR_bins_notriggers_stop35_met200.txt
    
else
    echo " Running UNBLINDED..."
    combine -M Asymptotic --datacard=TChiNeuWZ_80/2los_SR_bins_notriggers_ewk20_met125_mm$type.card.txt > $version/Asymp_2los_SR_bins_notriggers_ewk20_met125_mm.txt
    combine -M Asymptotic --datacard=TChiNeuWZ_80/2los_SR_bins_notriggers_ewk20_met200$type.card.txt > $version/Asymp_2los_SR_bins_notriggers_ewk20_met200.txt
    
    combine -M Asymptotic --datacard=TChiNeuWZ_90/2los_SR_bins_notriggers_ewk10_met125_mm$type.card.txt > $version/Asymp_2los_SR_bins_notriggers_ewk10_met125_mm.txt
    combine -M Asymptotic --datacard=TChiNeuWZ_90/2los_SR_bins_notriggers_ewk10_met200$type.card.txt > $version/Asymp_2los_SR_bins_notriggers_ewk10_met200.txt
    
    combine -M Asymptotic --datacard=T2ttDeg_330/2los_SR_bins_notriggers_stop20_met125_mm$type.card.txt > $version/Asymp_2los_SR_bins_notriggers_stop20_met125_mm.txt
    combine -M Asymptotic --datacard=T2ttDeg_330/2los_SR_bins_notriggers_stop20_met200$type.card.txt > $version/Asymp_2los_SR_bins_notriggers_stop20_met200.txt
    
    combine -M Asymptotic --datacard=T2ttDeg_315/2los_SR_bins_notriggers_stop35_met125_mm$type.card.txt > $version/Asymp_2los_SR_bins_notriggers_stop35_met125_mm.txt
    combine -M Asymptotic --datacard=T2ttDeg_315/2los_SR_bins_notriggers_stop35_met200$type.card.txt > $version/Asymp_2los_SR_bins_notriggers_stop35_met200.txt

fi

## combining
echo "Combining datacards..."
combineCards.py TChiNeuWZ_80/2los_SR_bins_notriggers_ewk20_met125_mm$type.card.txt TChiNeuWZ_80/2los_SR_bins_notriggers_ewk20_met200$type.card.txt  > TChiNeuWZ_80/2los_SR_bins_notriggers_ewk20_comb.card.txt
combineCards.py TChiNeuWZ_90/2los_SR_bins_notriggers_ewk10_met125_mm$type.card.txt TChiNeuWZ_90/2los_SR_bins_notriggers_ewk10_met200$type.card.txt  > TChiNeuWZ_90/2los_SR_bins_notriggers_ewk10_comb.card.txt

combineCards.py T2ttDeg_330/2los_SR_bins_notriggers_stop20_met125_mm$type.card.txt T2ttDeg_330/2los_SR_bins_notriggers_stop20_met200$type.card.txt  > T2ttDeg_330/2los_SR_bins_notriggers_stop20_comb.card.txt
combineCards.py T2ttDeg_315/2los_SR_bins_notriggers_stop35_met125_mm$type.card.txt T2ttDeg_315/2los_SR_bins_notriggers_stop35_met200$type.card.txt  > T2ttDeg_315/2los_SR_bins_notriggers_stop35_comb.card.txt


echo "Running on combined datacards..."

if [ $type != "_unblind" ]  
then
    combine -M Asymptotic --run=blind -t -1 --datacard=TChiNeuWZ_80/2los_SR_bins_notriggers_ewk20_comb.card.txt > $WWWDIR/$DIR/Asymp_2los_SR_bins_notriggers_ewk20_combined.txt
    combine -M Asymptotic --run=blind -t -1 --datacard=TChiNeuWZ_90/2los_SR_bins_notriggers_ewk10_comb.card.txt > $WWWDIR/$DIR/Asymp_2los_SR_bins_notriggers_ewk10_combined.txt
    combine -M Asymptotic --run=blind -t -1 --datacard=T2ttDeg_330/2los_SR_bins_notriggers_stop20_comb.card.txt > $WWWDIR/$DIR/Asymp_2los_SR_bins_notriggers_stop20_combined.txt
    combine -M Asymptotic --run=blind -t -1 --datacard=T2ttDeg_315/2los_SR_bins_notriggers_stop35_comb.card.txt > $WWWDIR/$DIR/Asymp_2los_SR_bins_notriggers_stop35_combined.txt
else
    echo " Running UNBLINDED..."
    combine -M Asymptotic --datacard=TChiNeuWZ_80/2los_SR_bins_notriggers_ewk20_comb.card.txt > $WWWDIR/$DIR/Asymp_2los_SR_bins_notriggers_ewk20_combined.txt
    combine -M Asymptotic --datacard=TChiNeuWZ_90/2los_SR_bins_notriggers_ewk10_comb.card.txt > $WWWDIR/$DIR/Asymp_2los_SR_bins_notriggers_ewk10_combined.txt
    combine -M Asymptotic --datacard=T2ttDeg_330/2los_SR_bins_notriggers_stop20_comb.card.txt > $WWWDIR/$DIR/Asymp_2los_SR_bins_notriggers_stop20_combined.txt
    combine -M Asymptotic --datacard=T2ttDeg_315/2los_SR_bins_notriggers_stop35_comb.card.txt > $WWWDIR/$DIR/Asymp_2los_SR_bins_notriggers_stop35_combined.txt
fi