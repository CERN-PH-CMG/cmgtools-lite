#!/bin/bash
eval `scramv1 runtime -sh`

## ==> COPY this script into /python/plotter folder <==

# Set here output dirs and types of limits 
type="_unblind" ## type of limits you want to extract
## can be: '_unblind' (observed), '_unblind_exp' 
DIR=SR_unblind_12invfb/  # local dir where all the temporary cards and histograms will be saved
version=result_v0  # if you want a different versioning inside the $DIR
WWWDIR=/afs/cern.ch/user/c/castello/www/susy-sos/ichep/approval/limits ## Directory where you want to save the final results (combined final limits)

echo "Producing cards from sos_plot.py"

########## EWKino ################################ 
python susy-sos/sos_plots.py $DIR 2los_SR_bins_notriggers_ewk10_met125_mm$type
python susy-sos/sos_plots.py $DIR 2los_SR_bins_notriggers_ewk10_met125_mm$type | sh                                                                            
#python susy-sos/sos_plots.py $DIR 2los_SR_bins_notriggers_ewk10_met200$type
#python susy-sos/sos_plots.py $DIR 2los_SR_bins_notriggers_ewk10_met200$type | sh  

## CR EWKino 10 GeV                                                                                                                                                                                              
#python susy-sos/sos_plots.py $DIR 2los_CR_DY_vars_data_met125_ewk10$type
#python susy-sos/sos_plots.py $DIR 2los_CR_DY_vars_data_met125_ewk10$type  | sh      
#python susy-sos/sos_plots.py $DIR 2los_CR_SS_bins_notriggers_ewk10_met200$type
#python susy-sos/sos_plots.py $DIR 2los_CR_SS_bins_notriggers_ewk10_met200$type  | sh     
#python susy-sos/sos_plots.py $DIR 2los_CR_TT_vars_dataMET_met125_ewk10$type
#python susy-sos/sos_plots.py $DIR 2los_CR_TT_vars_dataMET_met125_ewk10$type  | sh                                                
#python susy-sos/sos_plots.py $DIR 2los_CR_DY_vars_data_met200_ewk10$type
#python susy-sos/sos_plots.py $DIR 2los_CR_DY_vars_data_met200_ewk10$type    | sh
#python susy-sos/sos_plots.py $DIR 2los_CR_TT_vars_dataMET_met200_ewk10$type 
#python susy-sos/sos_plots.py $DIR 2los_CR_TT_vars_dataMET_met200_ewk10$type   | sh # (run separately due to the SF problem)       


########## Stop ################################ 
#python susy-sos/sos_plots.py $DIR 2los_SR_bins_notriggers_stop20_met125_mm$type                                                                                                                   
#python susy-sos/sos_plots.py $DIR 2los_SR_bins_notriggers_stop20_met125_mm$type | sh     
#python susy-sos/sos_plots.py $DIR 2los_SR_bins_notriggers_stop20_met200$type 
#python susy-sos/sos_plots.py $DIR 2los_SR_bins_notriggers_stop20_met200$type | sh

#python susy-sos/sos_plots.py $DIR 2los_CR_DY_vars_data_met125_stop20$type  
#python susy-sos/sos_plots.py $DIR 2los_CR_DY_vars_data_met125_stop20$type   | sh
#python susy-sos/sos_plots.py $DIR 2los_CR_SS_bins_notriggers_stop20_met200$type  
#python susy-sos/sos_plots.py $DIR 2los_CR_SS_bins_notriggers_stop20_met200$type  | sh 
#python susy-sos/sos_plots.py $DIR 2los_CR_TT_vars_dataMET_met125_stop20$type      
#python susy-sos/sos_plots.py $DIR 2los_CR_TT_vars_dataMET_met125_stop20$type  | sh      
#python susy-sos/sos_plots.py $DIR 2los_CR_DY_vars_data_met200_stop20$type                    
#python susy-sos/sos_plots.py $DIR 2los_CR_DY_vars_data_met200_stop20$type    | sh    
#python susy-sos/sos_plots.py $DIR 2los_CR_TT_vars_dataMET_met200_stop20$type 
#python susy-sos/sos_plots.py $DIR 2los_CR_TT_vars_dataMET_met200_stop20$type   | sh # (run separately due to the SF problem)    


exit 0

################## RUNNING COMBINE #############################################

cd $DIR
cd ~/WorkArea/physics/limits/CMSSW_7_4_7/src/
eval `scramv1 runtime -sh`
cd -
echo "Creating $WWWDIR/$DIR_combined_limits directory"
mkdir $WWWDIR/$DIR
mkdir $version

#separate
#echo "Running on separate datacards..."
#if [ $type != "_unblind" ]  
#then
#    combine -M Asymptotic --run=blind -t -1 --datacard=TChiNeuWZ_80/2los_SR_bins_notriggers_ewk20_met125_mm$type.card.txt > $version/Asymp_2los_SR_bins_notriggers_ewk20_met125_mm.txt
#    combine -M Asymptotic --run=blind -t -1 --datacard=TChiNeuWZ_80/2los_SR_bins_notriggers_ewk20_met200$type.card.txt > $version/Asymp_2los_SR_bins_notriggers_ewk20_met200.txt
 ##   combine -M Asymptotic --run=blind -t -1 --datacard=TChiNeuWZ_90/2los_SR_bins_notriggers_ewk10_met125_mm$type.card.txt > $version/Asymp_2los_SR_bins_notriggers_ewk10_met125_mm.txt
 ##    combine -M Asymptotic --run=blind -t -1 --datacard=TChiNeuWZ_90/2los_SR_bins_notriggers_ewk10_met200$type.card.txt > $version/Asymp_2los_SR_bins_notriggers_ewk10_met200.txt
 ##   combine -M Asymptotic --run=blind -t -1 --datacard=T2ttDeg_330/2los_SR_bins_notriggers_stop20_met125_mm$type.card.txt > $version/Asymp_2los_SR_bins_notriggers_stop20_met125_mm.txt
 ##   combine -M Asymptotic --run=blind -t -1 --datacard=T2ttDeg_330/2los_SR_bins_notriggers_stop20_met200$type.card.txt > $version/Asymp_2los_SR_bins_notriggers_stop20_met200.txt
 ##   combine -M Asymptotic --run=blind -t -1 --datacard=T2ttDeg_315/2los_SR_bins_notriggers_stop35_met125_mm$type.card.txt > $version/Asymp_2los_SR_bins_notriggers_stop35_met125_mm.txt
 ##   combine -M Asymptotic --run=blind -t -1 --datacard=T2ttDeg_315/2los_SR_bins_notriggers_stop35_met200$type.card.txt > $version/Asymp_2los_SR_bins_notriggers_stop35_met200.txt
#else
#    echo " Running UNBLINDED..."
#    combine -M Asymptotic --datacard=TChiNeuWZ_80/2los_SR_bins_notriggers_ewk20_met125_mm$type.card.txt > $version/Asymp_2los_SR_bins_notriggers_ewk20_met125_mm.txt
#    combine -M Asymptotic --datacard=TChiNeuWZ_80/2los_SR_bins_notriggers_ewk20_met200$type.card.txt > $version/Asymp_2los_SR_bins_notriggers_ewk20_met200.txt    
   ## combine -M Asymptotic --datacard=TChiNeuWZ_90/2los_SR_bins_notriggers_ewk10_met125_mm$type.card.txt > $version/Asymp_2los_SR_bins_notriggers_ewk10_met125_mm.txt
    ##combine -M Asymptotic --datacard=TChiNeuWZ_90/2los_SR_bins_notriggers_ewk10_met200$type.card.txt > $version/Asymp_2los_SR_bins_notriggers_ewk10_met200.txt
   ## combine -M Asymptotic --datacard=T2ttDeg_330/2los_SR_bins_notriggers_stop20_met125_mm$type.card.txt > $version/Asymp_2los_SR_bins_notriggers_stop20_met125_mm.txt
    ##combine -M Asymptotic --datacard=T2ttDeg_330/2los_SR_bins_notriggers_stop20_met200$type.card.txt > $version/Asymp_2los_SR_bins_notriggers_stop20_met200.txt 
   ## combine -M Asymptotic --datacard=T2ttDeg_315/2los_SR_bins_notriggers_stop35_met125_mm$type.card.txt > $version/Asymp_2los_SR_bins_notriggers_stop35_met125_mm.txt
    ##combine -M Asymptotic --datacard=T2ttDeg_315/2los_SR_bins_notriggers_stop35_met200$type.card.txt > $version/Asymp_2los_SR_bins_notriggers_stop35_met200.txt
#fi

## combining
echo "Combining datacards..."

combineCards.py SR_MET125=TChiNeuWZ_90/2los_SR_bins_notriggers_ewk10_met125_mm$type.card.txt SR_MET200=TChiNeuWZ_90/2los_SR_bins_notriggers_ewk10_met200$type.card.txt DYCR_MET125=TChiNeuWZ_90/2los_CR_DY_vars_data_met125_ewk10$type.card.txt DYCR_MET200=TChiNeuWZ_90/2los_CR_DY_vars_data_met200_ewk10$type.card.txt TTCR_MET125=TChiNeuWZ_90/2los_CR_TT_vars_dataMET_met125_ewk10$type.card.txt  TTCR_MET200=TChiNeuWZ_90/2los_CR_TT_vars_dataMET_met200_ewk10$type.card.txt SSCR_MET200=TChiNeuWZ_90/2los_CR_SS_notriggers_ewk10_met200_unblind_exp.card.txt > TChiNeuWZ_90/2los_SR_bins_notriggers_ewk10_comb.card.txt

combineCards.py SR_MET125=T2ttDeg_330/2los_SR_bins_notriggers_stop20_met125_mm$type.card.txt SR_MET200=T2ttDeg_330/2los_SR_bins_notriggers_stop20_met200$type.card.txt DYCR_MET125=T2ttDeg_330/2los_CR_DY_vars_data_met125_stop20$type.card.txt DYCR_MET200=T2ttDeg_330/2los_CR_DY_vars_data_met200_stop20$type.card.txt TTCR_MET125=T2ttDeg_330/2los_CR_TT_vars_dataMET_met125_stop20$type.card.txt  TTCR_MET200=T2ttDeg_330/2los_CR_TT_vars_dataMET_met200_stop20$type.card.txt SSCR_MET200=T2ttDeg_330/2los_CR_SS_notriggers_stop20_met200_unblind_exp.card.txt > T2ttDeg_330/2los_SR_bins_notriggers_stop20_comb.card.txt

#combineCards.py SR_MET125=TChiNeuWZ_80/2los_SR_bins_notriggers_ewk20_met125_mm$type.card.txt SR_MET200=TChiNeuWZ_80/2los_SR_bins_notriggers_ewk20_met200$type.card.txt DYCR_MET125=TChiNeuWZ_80/2los_CR_DY_vars_data_met125_ewk20$type.card.txt DYCR_MET200=TChiNeuWZ_80/2los_CR_DY_vars_data_met200_ewk20$type.card.txt TTCR_MET125=TChiNeuWZ_80/2los_CR_TT_vars_dataMET_met125_ewk20$type.card.txt  TTCR_MET200=TChiNeuWZ_80/2los_CR_TT_vars_dataMET_met200_ewk20$type.card.txt SSCR_MET200=TChiNeuWZ_80/2los_CR_SS_notriggers_ewk20_met200_unblind_exp.card.txt > TChiNeuWZ_80/2los_SR_bins_notriggers_ewk20_comb.card.txt

#combineCards.py SR_MET125=T2ttDeg_315/2los_SR_bins_notriggers_stop35_met125_mm$type.card.txt SR_MET200=T2ttDeg_315/2los_SR_bins_notriggers_stop35_met200$type.card.txt DYCR_MET125=T2ttDeg_315/2los_CR_DY_vars_data_met125_stop35$type.card.txt DYCR_MET200=T2ttDeg_315/2los_CR_DY_vars_data_met200_stop35$type.card.txt TTCR_MET125=T2ttDeg_315/2los_CR_TT_vars_dataMET_met125_stop35$type.card.txt  TTCR_MET200=T2ttDeg_315/2los_CR_TT_vars_dataMET_met200_stop35$type.card.txt SSCR_MET200=T2ttDeg_315/2los_CR_SS_notriggers_stop35_met200_unblind_exp.card.txt > T2ttDeg_315/2los_SR_bins_notriggers_stop35_comb.card.txt

echo "Linking the associated root file.."
text2workspace.py TChiNeuWZ_90/2los_SR_bins_notriggers_ewk10_comb.card.txt
text2workspace.py T2ttDeg_330/2los_SR_bins_notriggers_stop20_comb.card.txt
#text2workspace.py TChiNeuWZ_80/2los_SR_bins_notriggers_ewk20_comb.card.txt
#text2workspace.py T2ttDeg_315/2los_SR_bins_notriggers_stop35_comb.card.txt

## -- checking the cards 
echo "Checking the nuisance in the cards and printing on http://castello.web.cern.ch/castello/susy-sos/ichep/approval/limits/ "
python ~/WorkArea/physics/limits/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/test/systematicsAnalyzer.py TChiNeuWZ_90/2los_SR_bins_notriggers_ewk10_comb.card.txt --all -m 125 -f html > $WWWDIR/test_all_benchmarks/2los_SR_bins_notriggers_ewk10_comb.card.html
python ~/WorkArea/physics/limits/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/test/systematicsAnalyzer.py T2ttDeg_330/2los_SR_bins_notriggers_stop20_comb.card.txt --all -m 125 -f html > $WWWDIR/test_all_benchmarks/2los_SR_bins_notriggers_stop20_comb.card.html
#python ~/WorkArea/physics/limits/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/test/systematicsAnalyzer.py TChiNeuWZ_80/2los_SR_bins_notriggers_ewk20_comb.card.txt --all -m 125 -f html > $WWWDIR/test_all_benchmarks/2los_SR_bins_notriggers_ewk20_comb.card.html
#python ~/WorkArea/physics/limits/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/test/systematicsAnalyzer.py T2ttDeg_315/2los_SR_bins_notriggers_stop35_comb.card.txt --all -m 125 -f html > $WWWDIR/test_all_benchmarks/2los_SR_bins_notriggers_stop35_comb.card.html

#echo "Running on combined datacards..."
#
if [ $type != "_unblind" ]  
then
    echo "== Asymptotic"
    combine -M Asymptotic --run=blind -t -1 --datacard=TChiNeuWZ_90/2los_SR_bins_notriggers_ewk10_comb.card.txt > $WWWDIR/$DIR/Asymp_2los_SR_bins_notriggers_ewk10_combined.txt   
    #combine -M Asymptotic --run=blind -t -1 --datacard=TChiNeuWZ_80/2los_SR_bins_notriggers_ewk20_comb.card.txt > $WWWDIR/$DIR/Asymp_2los_SR_bins_notriggers_ewk20_combined.txt
    combine -M Asymptotic --run=blind -t -1 --datacard=T2ttDeg_330/2los_SR_bins_notriggers_stop20_comb.card.txt > $WWWDIR/$DIR/Asymp_2los_SR_bins_notriggers_stop20_combined.txt
    #combine -M Asymptotic --run=blind -t -1 --datacard=T2ttDeg_315/2los_SR_bins_notriggers_stop35_comb.card.txt > $WWWDIR/$DIR/Asymp_2los_SR_bins_notriggers_stop35_combined.txt

#    echo "== Likelihood"
#    combine -M MaxLikelihoodFit --setPhysicsModelParameterRanges r=-0,10 --setPhysicsModelParameters r=1  --customStartingPoint TChiNeuWZ_80/2los_SR_bins_notriggers_ewk20_comb.card.root
# python diffNuisances.py mlfit.root -g diffnuisances.root   
 #   combine -M Asymptotic --run=blind -t -1 --datacard=TChiNeuWZ_90/2los_SR_bins_notriggers_ewk10_comb.card.txt > $WWWDIR/$DIR/Asymp_2los_SR_bins_notriggers_ewk10_combined.txt
 #   combine -M Asymptotic --run=blind -t -1 --datacard=T2ttDeg_330/2los_SR_bins_notriggers_stop20_comb.card.txt > $WWWDIR/$DIR/Asymp_2los_SR_bins_notriggers_stop20_combined.txt
 #   combine -M Asymptotic --run=blind -t -1 --datacard=T2ttDeg_315/2los_SR_bins_notriggers_stop35_comb.card.txt > $WWWDIR/$DIR/Asymp_2los_SR_bins_notriggers_stop35_combined.txt
else
    echo " Running UNBLINDED..."
    echo "== Asymptotic"
#    ##cd $asymptotic_dir

    combine -M Asymptotic --datacard=TChiNeuWZ_90/2los_SR_bins_notriggers_ewk10_comb.card.txt > $WWWDIR/$DIR/Asymp_2los_SR_bins_notriggers_ewk10_combined.txt
    #combine -M Asymptotic --datacard=TChiNeuWZ_80/2los_SR_bins_notriggers_ewk20_comb.card.txt > $WWWDIR/$DIR/Asymp_2los_SR_bins_notriggers_ewk20_combined.txt
    combine -M Asymptotic --datacard=T2ttDeg_330/2los_SR_bins_notriggers_stop20_comb.card.txt > $WWWDIR/$DIR/Asymp_2los_SR_bins_notriggers_stop20_combined.txt
    #combine -M Asymptotic --datacard=T2ttDeg_315/2los_SR_bins_notriggers_stop35_comb.card.txt > $WWWDIR/$DIR/Asymp_2los_SR_bins_notriggers_stop35_combined.txt

#    echo "== Likelihood"
#    combine -M MaxLikelihoodFit --setPhysicsModelParameterRanges r=-5,5 --setPhysicsModelParameters r=1 --customStartingPoint TChiNeuWZ_80/2los_SR_bins_notriggers_ewk20_comb.card.root -v 3 
#    python /afs/cern.ch/work/c/castello/physics/limits/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/test/diffNuisances.py mlfit.root -g diffnuisances.root

#   combine -M Asymptotic --datacard=TChiNeuWZ_90/2los_SR_bins_notriggers_ewk10_comb.card.txt > $WWWDIR/$DIR/Asymp_2los_SR_bins_notriggers_ewk10_combined.txt
#   combine -M Asymptotic --datacard=T2ttDeg_330/2los_SR_bins_notriggers_stop20_comb.card.txt > $WWWDIR/$DIR/Asymp_2los_SR_bins_notriggers_stop20_combined.txt
#   combine -M Asymptotic --datacard=T2ttDeg_315/2los_SR_bins_notriggers_stop35_comb.card.txt > $WWWDIR/$DIR/Asymp_2los_SR_bins_notriggers_stop35_combined.txt
fi

echo "I'm done. Bye."