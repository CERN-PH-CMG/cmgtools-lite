#!/bin/bash

T="/mnt/t3nfs01/data01/shome/cheidegg/o/2016-07-13_ewkskims80X"
O="/afs/cern.ch/user/c/cheidegg/www/heppy/2016-11-07_ewk80X_sr3lopt_ICHEP"
base="python mcPlots.py susy-ewkino/3l/mca_ewkino.txt susy-ewkino/3l/cuts_ewkino.txt susy-ewkino/3l/plots_ewkino.txt -P $T --neg --s2v --tree treeProducerSusyMultilepton -f --cmsprel 'Preliminary' --legendWidth 0.20 --legendFontSize 0.035 --mcc susy-ewkino/3l/mcc_ewkino.txt --load-macro susy-ewkino/3l/functionsEWK.cc --showRatio -l 35 -F sf/t {P}/leptonJetReCleanerSusyEWK3L/evVarFriend_{cname}.root -F sf/t {P}/leptonBuilderEWK/evVarFriend_{cname}.root -F sf/t {P}/eventBTagWeight/evVarFriend_{cname}.root -p fakes_matched_.* -p prompt_.* -p rares_.* -p convs -X blinding --perBin --ratioOffset 0.03 --print C,png,pdf,txt --plotgroup rares_ttX+=rares_ttW --plotgroup rares_ttX+=rares_ttZ --showMCError --plotgroup fakes_matched_DY+=fakes_matched_WW --plotgroup fakes_matched_DY+=fakes_matched_WJ --plotgroup fakes_matched_DY+=fakes_matched_TT --plotgroup fakes_matched_DY+=fakes_matched_ST --showIndivSigs --noStackSig"
baseOpt="python mcPlots.py susy-ewkino/3l/mca_ewkino.txt susy-ewkino/3l/cuts_ewkino.txt susy-ewkino/3l/plots_ewkino_opt.txt -P $T --neg --s2v --tree treeProducerSusyMultilepton -f --cmsprel 'Preliminary' --legendWidth 0.20 --legendFontSize 0.035 --mcc susy-ewkino/3l/mcc_ewkino.txt --load-macro susy-ewkino/3l/functionsEWKopt.cc --showRatio -l 35 -F sf/t {P}/leptonJetReCleanerSusyEWK3L/evVarFriend_{cname}.root -F sf/t {P}/leptonBuilderEWK/evVarFriend_{cname}.root -F sf/t {P}/eventBTagWeight/evVarFriend_{cname}.root -p fakes_matched_.* -p prompt_.* -p rares_.* -p convs -X blinding --perBin --ratioOffset 0.03 --print C,png,pdf,txt --plotgroup rares_ttX+=rares_ttW --plotgroup rares_ttX+=rares_ttZ --showMCError --plotgroup fakes_matched_DY+=fakes_matched_WW --plotgroup fakes_matched_DY+=fakes_matched_WJ --plotgroup fakes_matched_DY+=fakes_matched_TT --plotgroup fakes_matched_DY+=fakes_matched_ST --showIndivSigs --noStackSig"

## all yields
## ------------------------------------------
#python susy-interface/plotmaker.py 3l "3lA;3lB;3lC;3lD;3lE;3lF" $T $O -l 35 --make bkgs --plots perCateg -o SR --flags '-X blinding --perBin --plotgroup rares_ttX+=rares_ttW --plotgroup rares_ttX+=rares_ttZ --showMCError --plotgroup fakes_matched_DY+=fakes_matched_WW --plotgroup fakes_matched_DY+=fakes_matched_WJ --plotgroup fakes_matched_DY+=fakes_matched_TT --plotgroup fakes_matched_DY+=fakes_matched_ST' --bkgs "fakes_matched_.*;prompt_.*;rares_.*;convs"
#python susy-interface/plotmaker.py 3l 3lA $T $O -l 35 --make mix --plots perCateg -o SR --flags '-X blinding --perBin --plotgroup rares_ttX+=rares_ttW --plotgroup rares_ttX+=rares_ttZ --showMCError --plotgroup fakes_matched_DY+=fakes_matched_WW --plotgroup fakes_matched_DY+=fakes_matched_WJ --plotgroup fakes_matched_DY+=fakes_matched_TT --plotgroup fakes_matched_DY+=fakes_matched_ST' --bkgs "fakes_matched_.*;prompt_.*;rares_.*;convs" --sigs "TChiNeuSlepSneuFD_1000_1;TChiNeuSlepSneuFD_500_475" --pretend
#python susy-interface/plotmaker.py 3l "3lB;3lC;3lD;3lE;3lF" $T $O -l 35 --make mix --plots perCateg -o SR --flags '-X blinding --perBin --plotgroup rares_ttX+=rares_ttW --plotgroup rares_ttX+=rares_ttZ --showMCError --plotgroup fakes_matched_DY+=fakes_matched_WW --plotgroup fakes_matched_DY+=fakes_matched_WJ --plotgroup fakes_matched_DY+=fakes_matched_TT --plotgroup fakes_matched_DY+=fakes_matched_ST' --bkgs "fakes_matched_.*;prompt_.*;rares_.*;convs" --sigs "TChiNeuSlepSneuTD_500_1;TChiNeuSlepSneuTD_200_150"
#O="/afs/cern.ch/user/c/cheidegg/www/heppy/2016-10-25_ewk80X_sr3lopt_tauMETsplit"
#python susy-interface/plotmaker.py 3l "3lD" $T $O -l 35 --make mix --plots perCateg -o SR --flags '-X blinding --perBin --plotgroup rares_ttX+=rares_ttW --plotgroup rares_ttX+=rares_ttZ --showMCError --plotgroup fakes_matched_DY+=fakes_matched_WW --plotgroup fakes_matched_DY+=fakes_matched_WJ --plotgroup fakes_matched_DY+=fakes_matched_TT --plotgroup fakes_matched_DY+=fakes_matched_ST' --bkgs "fakes_matched_.*;prompt_.*;rares_.*;convs" --sigs "TChiNeuSlepSneuTD_500_1;TChiNeuSlepSneuTD_200_150" --macros susy-ewkino/3l/functionsEWKopt.cc --plot susy-ewkino/3l/plots_ewkino_opt.txt
#python susy-interface/plotmaker.py 3l "3lC;3lD;3lE;3lF" $T $O -l 35 --make mix --plots perCateg -o SR --flags '-X blinding --perBin --plotgroup rares_ttX+=rares_ttW --plotgroup rares_ttX+=rares_ttZ --showMCError --plotgroup fakes_matched_DY+=fakes_matched_WW --plotgroup fakes_matched_DY+=fakes_matched_WJ --plotgroup fakes_matched_DY+=fakes_matched_TT --plotgroup fakes_matched_DY+=fakes_matched_ST' --bkgs "fakes_matched_.*;prompt_.*;rares_.*;convs" --sigs "TChiNeuSlepSneuTD_500_1;TChiNeuSlepSneuTD_200_150" --macros susy-ewkino/3l/functionsEWKopt.cc --plot susy-ewkino/3l/plots_ewkino_opt.txt


## 3l region A
## ------------------------------------------
## plots
#eval "$base --pdir $O/plots/3lOpt/0taus/mix --sP mll3l -A alwaystrue underflow 'BR==1' -p TChiNeuSlepSneuFD_1100_1 -p TChiNeuSlepSneuFD_500_475" 
#eval "$base --pdir $O/plots/3lOpt/0taus/mix --sP mtW3l -A alwaystrue underflow 'BR==1' -p TChiNeuSlepSneuFD_1100_1 -p TChiNeuSlepSneuFD_500_475" 
#eval "$base --pdir $O/plots/3lOpt/0taus/mix --sP met   -A alwaystrue underflow 'BR==1' -p TChiNeuSlepSneuFD_1100_1 -p TChiNeuSlepSneuFD_500_475" 
#eval "$base --pdir $O/plots/3lOpt/0taus/mix --sP mTmll -A alwaystrue underflow 'BR==1' -p TChiNeuSlepSneuFD_1100_1 -p TChiNeuSlepSneuFD_500_475"
#eval "$base --pdir $O/plots/3lOpt/0taus/mix --sP mTmet -A alwaystrue underflow 'BR==1' -p TChiNeuSlepSneuFD_1100_1 -p TChiNeuSlepSneuFD_500_475"
#O="/afs/cern.ch/user/c/cheidegg/www/heppy/2016-11-07_ewk80X_sr3lopt_ICHEP"
#eval "$base --pdir $O/plots/3lOpt/0taus/mix --sP SR_A -A alwaystrue underflow 'BR==1' -p TChiNeuSlepSneuFD_1100_1 -p TChiNeuSlepSneuFD_500_475"
#O="/afs/cern.ch/user/c/cheidegg/www/heppy/2016-11-07_ewk80X_sr3lopt_moreMET"
#O="/afs/cern.ch/user/c/cheidegg/www/heppy/2016-11-07_ewk80X_sr3lopt_mergedMET"
#O="/afs/cern.ch/user/c/cheidegg/www/heppy/2016-11-07_ewk80X_sr3lopt_option1"
#O="/afs/cern.ch/user/c/cheidegg/www/heppy/2016-11-07_ewk80X_sr3lopt_option2"
#eval "$baseOpt --pdir $O/plots/3lOpt/0taus/mix --sP SR_A -A alwaystrue underflow 'BR==1' -p TChiNeuSlepSneuFD_1100_1 -p TChiNeuSlepSneuFD_500_475"
## limits
#O="/afs/cern.ch/user/c/cheidegg/www/heppy/2016-11-07_ewk80X_sr3lopt_ICHEP"
#python susy-interface/limitmaker.py 3l 3lA $T $O -l 35 -o SR --flags '-X blinding --asimov' --sigs "TChiNeuSlepSneuFD_.*;TChiNeuWZ_.*" --bkgs "fakes_matched_.*;prompt_.*;rares_.*;convs" --sys susy-ewkino/systs_dummy.txt --finalize
#O="/afs/cern.ch/user/c/cheidegg/www/heppy/2016-11-07_ewk80X_sr3lopt_moreMET"
#python susy-interface/limitmaker.py 3l 3lA $T $O -l 35 -o SR --flags '-X blinding --asimov' --sigs "TChiNeuSlepSneuFD_.*;TChiNeuWZ_.*" --bkgs "fakes_matched_.*;prompt_.*;rares_.*;convs" --sys susy-ewkino/systs_dummy.txt --finalize --macros susy-ewkino/3l/functionsEWKopt.cc --bins "47,0.5,47.5"
#O="/afs/cern.ch/user/c/cheidegg/www/heppy/2016-11-07_ewk80X_sr3lopt_mergedMET"
#O="/afs/cern.ch/user/c/cheidegg/www/heppy/2016-11-07_ewk80X_sr3lopt_option1"
#python susy-interface/limitmaker.py 3l 3lA $T $O -l 35 -o SR --flags '-X blinding --asimov' --sigs "TChiNeuSlepSneuFD_.*;TChiNeuWZ_.*" --bkgs "fakes_matched_.*;prompt_.*;rares_.*;convs" --sys susy-ewkino/systs_dummy.txt --finalize --macros susy-ewkino/3l/functionsEWKopt.cc --bins "43,0.5,43.5"
#O="/afs/cern.ch/user/c/cheidegg/www/heppy/2016-11-07_ewk80X_sr3lopt_option2"
#python susy-interface/limitmaker.py 3l 3lA $T $O -l 35 -o SR --flags '-X blinding --asimov' --sigs "TChiNeuSlepSneuFD_.*;TChiNeuWZ_.*" --bkgs "fakes_matched_.*;prompt_.*;rares_.*;convs" --sys susy-ewkino/systs_dummy.txt --finalize --macros susy-ewkino/3l/functionsEWKopt.cc --bins "31,0.5,31.5"

## OLD STUFF
#eval "$baseOpt --pdir $O/plots/3lOpt/0taus/mix --sP SR_A_opt2 -A alwaystrue underflow 'BR==1' -p TChiNeuSlepSneuFD_1100_1 -p TChiNeuSlepSneuFD_500_475"
#eval "$baseOpt --pdir $O/plots/3lOpt/0taus/mix --sP SR_A_opt2MET -A alwaystrue underflow 'BR==1' -p TChiNeuSlepSneuFD_1100_1 -p TChiNeuSlepSneuFD_500_475"
## scans
#O="/mnt/t3nfs01/data01/shome/cheidegg/o/2016-10-25_ewk80X_sr3lopt_try2"
#python susy-interface/scanmaker.py 3l 3lA $T $O -l 35 -o SR --models "TChiNeuSlepSneu_FD;TChiNeuWZ" --mca susy-ewkino/3l/mca_ewkino_forOpt.txt --sys susy-ewkino/systs_dummy.txt --flags '-X blinding' --sigOnly -q all.q --bins "24,0.5,24.5"
## limits
#O="/mnt/t3nfs01/data01/shome/cheidegg/o/2016-10-25_ewk80X_sr3lopt_try2new"
#python susy-interface/limitmaker.py 3l 3lA $T $O -l 35 -o SR --flags '-X blinding --asimov' --sigs "TChiNeuSlepSneuFD_.*;TChiNeuWZ_.*" --bkgs "fakes_matched_.*;prompt_.*;rares_.*;convs" --sys susy-ewkino/systs_dummy.txt --finalize --macros susy-ewkino/3l/functionsEWKopt.cc --bins "24,0.5,24.5"
#O="/mnt/t3nfs01/data01/shome/cheidegg/o/2016-10-25_ewk80X_sr3lopt_try2MET"
#python susy-interface/limitmaker.py 3l 3lA $T $O -l 35 -o SR --flags '-X blinding --asimov' --sigs "TChiNeuSlepSneuFD_.*;TChiNeuWZ_.*" --bkgs "fakes_matched_.*;prompt_.*;rares_.*;convs" --sys susy-ewkino/systs_dummy.txt --finalize --macros susy-ewkino/3l/functionsEWKopt.cc --bins "30,0.5,30.5" --pretend
#O="/mnt/t3nfs01/data01/shome/cheidegg/o/2016-10-25_ewk80X_sr3lopt_tauMETsplit"
#python susy-interface/limitmaker.py 3l "3lC;3lD;3lE;3lF" $T $O -l 35 -o SR --flags '-X blinding --asimov' --sigs "TChiNeuSlepSneuTD_.*;TChiNeuWH_.*" --bkgs "fakes_matched_.*;prompt_.*;rares_.*;convs" --sys susy-ewkino/systs_dummy.txt --macros susy-ewkino/3l/functionsEWKopt.cc --finalize

## 3l taus
## ------------------------------------------
#O="/afs/cern.ch/user/c/cheidegg/www/heppy/2016-11-07_ewk80X_sr3lopt_expectedYields"
eval "$baseOpt --pdir $O/SR/3lC/35fb/mix --sP SR_C -A alwaystrue underflow 'BR==3' -p TChiNeuSlepSneuTD_500_1 -p TChiNeuSlepSneuTD_200_150"
eval "$baseOpt --pdir $O/plots/3lOpt/1taus/mix --sP SR_D -A alwaystrue underflow 'BR==4' -p TChiNeuSlepSneuTD_500_1 -p TChiNeuSlepSneuTD_200_150"
eval "$baseOpt --pdir $O/plots/3lOpt/2taus/mix --sP SR_F -A alwaystrue underflow 'BR==6' -p TChiNeuSlepSneuTD_500_1 -p TChiNeuSlepSneuTD_200_150"
eval "$baseOpt --pdir $O/plots/3lOpt/2taus/mix --sP SR_F -A alwaystrue underflow 'BR==6' -p TChiNeuSlepSneuTD_500_1 -p TChiNeuSlepSneuTD_200_150"
#O="/afs/cern.ch/user/c/cheidegg/www/heppy/2016-11-07_ewk80X_sr3lopt_mergedMET"
#python susy-interface/limitmaker.py 3l 3lC $T $O -l 35 -o SR --flags '-X blinding --asimov' --sigs "TChiNeuSlepSneuTD_.*;TChiNeuWH_.*" --bkgs "fakes_matched_.*;prompt_.*;rares_.*;convs" --sys susy-ewkino/systs_dummy.txt --finalize --macros susy-ewkino/3l/functionsEWKopt.cc --expr "SR-49" --bins "18,0.5,18.5"
#python susy-interface/limitmaker.py 3l 3lD $T $O -l 35 -o SR --flags '-X blinding --asimov' --sigs "TChiNeuSlepSneuTD_.*;TChiNeuWH_.*" --bkgs "fakes_matched_.*;prompt_.*;rares_.*;convs" --sys susy-ewkino/systs_dummy.txt --finalize --macros susy-ewkino/3l/functionsEWKopt.cc --expr "SR-67" --bins "16,0.5,16.5"
#python susy-interface/limitmaker.py 3l 3lF $T $O -l 35 -o SR --flags '-X blinding --asimov' --sigs "TChiNeuSlepSneuTD_.*;TChiNeuWH_.*" --bkgs "fakes_matched_.*;prompt_.*;rares_.*;convs" --sys susy-ewkino/systs_dummy.txt --finalize --macros susy-ewkino/3l/functionsEWKopt.cc --expr "SR-95" --bins "12,0.5,12.5"


#O="/mnt/t3nfs01/data01/shome/cheidegg/o/2016-10-25_ewk80X_sr3lopt_ICHEP"
#python susy-interface/limitmaker.py 3l "3lC;3lD;3lE;3lF" $T $O -l 35 -o SR --flags '-X blinding --asimov' --sigs "TChiNeuSlepSneuTD_.*;TChiNeuWH_.*" --bkgs "fakes_matched_.*;prompt_.*;rares_.*;convs" --sys susy-ewkino/systs_dummy.txt --finalize
#O="/mnt/t3nfs01/data01/shome/cheidegg/o/2016-10-25_ewk80X_sr3lopt_tauMETsplit"
#python susy-interface/limitmaker.py 3l "3lC;3lD;3lE;3lF" $T $O -l 35 -o SR --flags '-X blinding --asimov' --sigs "TChiNeuSlepSneuTD_.*;TChiNeuWH_.*" --bkgs "fakes_matched_.*;prompt_.*;rares_.*;convs" --sys susy-ewkino/systs_dummy.txt --macros susy-ewkino/3l/functionsEWKopt.cc --finalize



## 3l region F
## ------------------------------------------
#eval "$base --pdir $O/plots/3lOpt/2taus/mix --sP mll3l  -A alwaystrue underflow 'BR==6' -p TChiNeuWH_200_1 -p TChiNeuWH_150_1" 
#eval "$base --pdir $O/plots/3lOpt/2taus/mix --sP mtautau -A alwaystrue underflow 'BR==6' -p TChiNeuWH_200_1 -p TChiNeuWH_150_1" 
#eval "$base --pdir $O/plots/3lOpt/2taus/mix --sP mll3l  -A alwaystrue underflow 'BR==6' -p TChiNeuSlepSneuTD_500_1 -p TChiNeuSlepSneuTD_200_150" 
#eval "$base --pdir $O/plots/3lOpt/2taus/mix --sP mtautau -A alwaystrue underflow 'BR==6' -p TChiNeuSlepSneuTD_500_1 -p TChiNeuSlepSneuTD_200_150" 
#eval "$base --pdir $O/plots/3lOpt/2taus/mix --sP mT2T3l  -A alwaystrue underflow 'BR==6' -p TChiNeuSlepSneuTD_500_1 -p TChiNeuSlepSneuTD_200_150" 
#eval "$base --pdir $O/plots/3lOpt/2taus/mix --sP met    -A alwaystrue underflow 'BR==6' -p TChiNeuSlepSneuTD_500_1 -p TChiNeuSlepSneuTD_200_150" 



## super signal regions
## ------------------------------------------
#O="/afs/cern.ch/user/c/cheidegg/www/heppy/2016-11-08_ewk80X_sr3lopt_SSR3light_opt3_2"
#python susy-interface/limitmaker.py 3l 3lA $T $O -l 35 -o SR --flags '-X blinding --hardZero --asimov -A alwaystrue BRcut "BR<=2"' --sigs "TChiNeuSlepSneuFD_.*;TChiNeuWZ_.*" --bkgs "fakes_matched_.*;prompt_.*;rares_.*;convs" --sys susy-ewkino/systs_dummy.txt --finalize --macros susy-ewkino/3l/functionsEWKopt.cc --expr "SuperSig" --bins "1,0.5,1.5"
#O="/afs/cern.ch/user/c/cheidegg/www/heppy/2016-11-08_ewk80X_sr3lopt_SSR2light1tau3"
#python susy-interface/limitmaker.py 3l 3lA $T $O -l 35 -o SR --flags '-X blinding --hardZero --asimov -A alwaystrue BRcut "BR>=3 && BR<=5"' --sigs "TChiNeuSlepSneuTD_.*;TChiNeuWH_.*" --bkgs "fakes_matched_.*;prompt_.*;rares_.*;convs" --sys susy-ewkino/systs_dummy.txt --finalize --macros susy-ewkino/3l/functionsEWKopt.cc --expr "SuperSig" --bins "1,0.5,1.5"
#O="/afs/cern.ch/user/c/cheidegg/www/heppy/2016-11-08_ewk80X_sr3lopt_SSR1light2tau2"
#python susy-interface/limitmaker.py 3l 3lA $T $O -l 35 -o SR --flags '-X blinding --hardZero --asimov -A alwaystrue BRcut "BR==6"' --sigs "TChiNeuSlepSneuTD_.*;TChiNeuWH_.*" --bkgs "fakes_matched_.*;prompt_.*;rares_.*;convs" --sys susy-ewkino/systs_dummy.txt --finalize --macros susy-ewkino/3l/functionsEWKopt.cc --expr "SuperSig" --bins "1,0.5,1.5"
#O="/afs/cern.ch/user/c/cheidegg/www/heppy/2016-11-08_ewk80X_sr3lopt_SSR4light"
#python susy-interface/limitmaker.py 3l 4lG $T $O -l 35 -o SR --flags '-X blinding --hardZero --asimov -A alwaystrue inSR "SuperSig>=0.5 && SuperSig<=1.5"' --sigs "TChiNeuZZ4L_.*;TChiNeuHZ_.*;TChiNeuHH_.*" --bkgs "fakes_matched_.*;prompt_.*;rares_.*;convs" --sys susy-ewkino/systs_dummy.txt --finalize --macros susy-ewkino/3l/functionsEWKopt.cc --mccs susy-ewkino/4l/mcc_ewkino.txt --expr "SuperSig" --bins "1,0.5,1.5"




