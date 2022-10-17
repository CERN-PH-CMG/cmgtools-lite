#!/bin/bash

T="/mnt/t3nfs01/data01/shome/cheidegg/o/2016-07-13_ewkskims80X"
O="/afs/cern.ch/user/c/cheidegg/www/heppy/2016-11-07_ewk80X_sr4lopt"
base="python mcPlots.py susy-ewkino/4l/mca_ewkino.txt susy-ewkino/4l/cuts_ewkino.txt susy-ewkino/3l/plots_ewkino.txt -P $T --neg --s2v --tree treeProducerSusyMultilepton -f --cmsprel 'Preliminary' --legendWidth 0.20 --legendFontSize 0.035 --mcc susy-ewkino/4l/mcc_ewkino.txt --load-macro susy-ewkino/3l/functionsEWK.cc --showRatio -l 35 -F sf/t {P}/leptonJetReCleanerSusyEWK3L/evVarFriend_{cname}.root -F sf/t {P}/leptonBuilderEWK/evVarFriend_{cname}.root -p fakes_matched_.* -p promptsub -p prompt_.* -p rares_.* -p convs -X blinding --perBin --ratioOffset 0.03 --print C,png,pdf,txt --plotgroup rares_ttX+=rares_ttW --plotgroup rares_ttX+=rares_ttZ --showMCError --plotgroup fakes_matched_DY+=fakes_matched_WW --plotgroup fakes_matched_DY+=fakes_matched_WJ --plotgroup fakes_matched_DY+=fakes_matched_TT --plotgroup fakes_matched_DY+=fakes_matched_ST --showIndivSigs --noStackSig"
baseOpt="python mcPlots.py susy-ewkino/4l/mca_ewkino.txt susy-ewkino/4l/cuts_ewkino.txt susy-ewkino/3l/plots_ewkino_opt.txt -P $T --neg --s2v --tree treeProducerSusyMultilepton -f --cmsprel 'Preliminary' --legendWidth 0.20 --legendFontSize 0.035 --mcc susy-ewkino/4l/mcc_ewkino.txt --load-macro susy-ewkino/3l/functionsEWKopt.cc --showRatio -l 35 -F sf/t {P}/leptonJetReCleanerSusyEWK3L/evVarFriend_{cname}.root -F sf/t {P}/leptonBuilderEWK/evVarFriend_{cname}.root -p fakes_matched_.* -p prompt_.* -p rares_.* -p convs -X blinding --perBin --ratioOffset 0.03 --print C,png,pdf,txt --plotgroup rares_ttX+=rares_ttW --plotgroup rares_ttX+=rares_ttZ --showMCError --plotgroup fakes_matched_DY+=fakes_matched_WW --plotgroup fakes_matched_DY+=fakes_matched_WJ --plotgroup fakes_matched_DY+=fakes_matched_TT --plotgroup fakes_matched_DY+=fakes_matched_ST --showIndivSigs --noStackSig"

## flavors
#eval "$base --pdir $O/SR/4lOpt/all/bkg --sP BRnew -A alwaystrue underflow 'BRnew>6'" 
#eval "$base --pdir $O/SR/4lOpt/all/mix --sP nLepFlavor -p TChiNeuZZ4L_400_1 -p TChiNeuHZ_400_1 -p TChiNeuHH_400_1"
#
### 0taus
#eval "$base --pdir $O/SR/4lOpt/0taus/mix --sP nOSSF -A alwaystrue BR0taus 'nLepFlavor==1||nLepFlavor==6' -p TChiNeuZZ4L_400_1 -p TChiNeuHZ_400_1 -p TChiNeuHH_400_1" 
#eval "$base --pdir $O/SR/4lOpt/0taus2OSSF/mix --sP met       -A alwaystrue BR0taus '(nLepFlavor==1||nLepFlavor==6)&&nOSSF_4l==2' -p TChiNeuZZ4L_400_1 -p TChiNeuHZ_400_1 -p TChiNeuHH_400_1" 
#eval "$base --pdir $O/SR/4lOpt/0taus2OSSF/mix --sP mll4l     -A alwaystrue BR0taus '(nLepFlavor==1||nLepFlavor==6)&&nOSSF_4l==2' -p TChiNeuZZ4L_400_1 -p TChiNeuHZ_400_1 -p TChiNeuHH_400_1" 
#eval "$base --pdir $O/SR/4lOpt/0taus2OSSF/mix --sP mllFirst  -A alwaystrue BR0taus '(nLepFlavor==1||nLepFlavor==6)&&nOSSF_4l==2' -p TChiNeuZZ4L_400_1 -p TChiNeuHZ_400_1 -p TChiNeuHH_400_1" 
#eval "$base --pdir $O/SR/4lOpt/0taus2OSSF/mix --sP mllSecond -A alwaystrue BR0taus '(nLepFlavor==1||nLepFlavor==6)&&nOSSF_4l==2' -p TChiNeuZZ4L_400_1 -p TChiNeuHZ_400_1 -p TChiNeuHH_400_1" 
#eval "$base --pdir $O/SR/4lOpt/0taus1OSSF/mix --sP met       -A alwaystrue BR0taus '(nLepFlavor==1||nLepFlavor==6)&&nOSSF_4l<2' -p TChiNeuZZ4L_400_1 -p TChiNeuHZ_400_1 -p TChiNeuHH_400_1 --yrange 0.001 10000" 
#eval "$base --pdir $O/SR/4lOpt/0taus1OSSF/mix --sP mll4l     -A alwaystrue BR0taus '(nLepFlavor==1||nLepFlavor==6)&&nOSSF_4l<2' -p TChiNeuZZ4L_400_1 -p TChiNeuHZ_400_1 -p TChiNeuHH_400_1 --yrange 0.001 1000" 
#
### 1taus
#eval "$base --pdir $O/SR/4lOpt/1taus/mix --sP nOSSF -A alwaystrue BR0taus 'nLepFlavor==2||nLepFlavor==6' -p TChiNeuZZ4L_400_1 -p TChiNeuHZ_400_1 -p TChiNeuHH_400_1" 
#eval "$base --pdir $O/SR/4lOpt/1taus1OSSF/mix --sP met       -A alwaystrue BR0taus '(nLepFlavor==2||nLepFlavor==6)&&nOSSF_4l>=1' -p TChiNeuZZ4L_400_1 -p TChiNeuHZ_400_1 -p TChiNeuHH_400_1 --yrange 0.001 10000" 
#eval "$base --pdir $O/SR/4lOpt/1taus0OSSF/mix --sP met       -A alwaystrue BR0taus '(nLepFlavor==2||nLepFlavor==6)&&nOSSF_4l==0' -p TChiNeuZZ4L_400_1 -p TChiNeuHZ_400_1 -p TChiNeuHH_400_1 --yrange 0.001 10000" 
#eval "$base --pdir $O/SR/4lOpt/1taus/mix --sP met   -A alwaystrue BR0taus '(nLepFlavor==2||nLepFlavor==6)' -p TChiNeuZZ4L_400_1 -p TChiNeuHZ_400_1 -p TChiNeuHH_400_1 --yrange 0.001 10000" 
### 2taus
#eval "$base --pdir $O/SR/4lOpt/2taus/mix --sP nOSSF -A alwaystrue BR0taus '(nLepFlavor==3||nLepFlavor==6)' -p TChiNeuZZ4L_400_1 -p TChiNeuHZ_400_1 -p TChiNeuHH_400_1" 
#eval "$base --pdir $O/SR/4lOpt/2taus2OSSF/mix --sP met -A alwaystrue BR0taus '(nLepFlavor==3||nLepFlavor==6)&&nOSSF_4l==2' -p TChiNeuZZ4L_400_1 -p TChiNeuHZ_400_1 -p TChiNeuHH_400_1 --yrange 0.001 10000" 
#eval "$base --pdir $O/SR/4lOpt/2taus2OSSF/mix --sP mllFirst  -A alwaystrue BR0taus '(nLepFlavor==3||nLepFlavor==6)&&nOSSF_4l==2' -p TChiNeuZZ4L_400_1 -p TChiNeuHZ_400_1 -p TChiNeuHH_400_1 --yrange 0.001 1000" 
#eval "$base --pdir $O/SR/4lOpt/2taus2OSSF/mix --sP mllSecond -A alwaystrue BR0taus '(nLepFlavor==3||nLepFlavor==6)&&nOSSF_4l==2' -p TChiNeuZZ4L_400_1 -p TChiNeuHZ_400_1 -p TChiNeuHH_400_1 --yrange 0.001 1000" 
#eval "$base --pdir $O/SR/4lOpt/2taus1OSSF/mix --sP met -A alwaystrue BR0taus '(nLepFlavor==3||nLepFlavor==6)&&nOSSF_4l<2' -p TChiNeuZZ4L_400_1 -p TChiNeuHZ_400_1 -p TChiNeuHH_400_1 --yrange 0.001 10000" 
#eval "$base --pdir $O/SR/4lOpt/2taus1OSSF/mix --sP mll4l     -A alwaystrue BR0taus '(nLepFlavor==3||nLepFlavor==6)&&nOSSF_4l<2' -p TChiNeuZZ4L_400_1 -p TChiNeuHZ_400_1 -p TChiNeuHH_400_1 --yrange 0.001 1000" 
### 3taus
#eval "$base --pdir $O/SR/4lOpt/3taus/mix --sP nOSSF -A alwaystrue BR0taus '(nLepFlavor==4||nLepFlavor==6)' -p TChiNeuZZ4L_400_1 -p TChiNeuHZ_400_1 -p TChiNeuHH_400_1" 
#eval "$base --pdir $O/SR/4lOpt/3taus/mix --sP met -A alwaystrue BR0taus '(nLepFlavor==4||nLepFlavor==6)' -p TChiNeuZZ4L_400_1 -p TChiNeuHZ_400_1 -p TChiNeuHH_400_1" 
##eval "$base --pdir $O/SR/4lOpt/3taus0OSSF/mix --sP met -A alwaystrue BR0taus '(nLepFlavor==4||nLepFlavor==6)&&nOSSF_4l==0' -p TChiNeuZZ4L_400_1 -p TChiNeuHZ_400_1 -p TChiNeuHH_400_1 --yrange 0.001 10000" 
##eval "$base --pdir $O/SR/4lOpt/3taus1OSSF/mix --sP met -A alwaystrue BR0taus '(nLepFlavor==4||nLepFlavor==6)&&nOSSF_4l>=1' -p TChiNeuZZ4L_400_1 -p TChiNeuHZ_400_1 -p TChiNeuHH_400_1 --yrange 0.001 10000" 
##eval "$base --pdir $O/SR/4lOpt/3taus1OSSF/mix --sP mll4l     -A alwaystrue BR0taus '(nLepFlavor==4||nLepFlavor==6)&&nOSSF_4l>=1' -p TChiNeuZZ4L_400_1 -p TChiNeuHZ_400_1 -p TChiNeuHH_400_1 --yrange 0.001 1000" 
## >4lep
#eval "$base --pdir $O/SR/4lOpt/5lep/mix --sP met -A alwaystrue BR0taus 'is_5l' -p TChiNeuZZ4L_400_1 -p TChiNeuHZ_400_1 -p TChiNeuHH_400_1" 

## yields
#eval "$baseOpt --pdir $O/plots/4lOpt/yields/mix --sP SR_G -A alwaystrue underflow 'BR==7' -p TChiNeuZZ4L_400_1 -p TChiNeuHZ_400_1 -p TChiNeuHH_400_1"
#eval "$baseOpt --pdir $O/plots/4lOpt/yields/mix --sP SR_H -A alwaystrue underflow 'BR==8' -p TChiNeuZZ4L_400_1 -p TChiNeuHZ_400_1 -p TChiNeuHH_400_1"
#eval "$baseOpt --pdir $O/plots/4lOpt/yields/mix --sP SR_I -A alwaystrue underflow 'BR==9' -p TChiNeuZZ4L_400_1 -p TChiNeuHZ_400_1 -p TChiNeuHH_400_1"
#eval "$baseOpt --pdir $O/plots/4lOpt/yields/mix --sP SR_J -A alwaystrue underflow 'BR==10' -p TChiNeuZZ4L_400_1 -p TChiNeuHZ_400_1 -p TChiNeuHH_400_1"
#eval "$baseOpt --pdir $O/plots/4lOpt/yields/mix --sP SR_K -A alwaystrue underflow 'BR==11' -p TChiNeuZZ4L_400_1 -p TChiNeuHZ_400_1 -p TChiNeuHH_400_1"
#eval "$baseOpt --pdir $O/plots/4lOpt/yields/mix --sP SR_L -A alwaystrue underflow 'BR==12' -p TChiNeuZZ4L_400_1 -p TChiNeuHZ_400_1 -p TChiNeuHH_400_1"

## limits
#O="/afs/cern.ch/user/c/cheidegg/www/heppy/2016-11-07_ewk80X_sr3lopt_ICHEP"
#python susy-interface/limitmaker.py 3l 4lG $T $O -l 35 -o SR --flags '-X blinding --asimov' --sigs "TChiNeuZZ4L_.*;TChiNeuZZ2L_.*;TChiNeuHZ_.*;TChiNeuHH_.*" --bkgs "fakes_matched_.*;prompt_.*;rares_.*;convs" --sys susy-ewkino/systs_dummy.txt --macros susy-ewkino/3l/functionsEWKopt.cc --mccs susy-ewkino/4l/mcc_ewkino.txt --finalize
#python susy-interface/limitmaker.py 3l 4lH $T $O -l 35 -o SR --flags '-X blinding --asimov' --sigs "TChiNeuZZ4L_.*;TChiNeuZZ2L_.*;TChiNeuHZ_.*;TChiNeuHH_.*" --bkgs "fakes_matched_.*;prompt_.*;rares_.*;convs" --sys susy-ewkino/systs_dummy.txt --macros susy-ewkino/3l/functionsEWKopt.cc --mccs susy-ewkino/4l/mcc_ewkino.txt --finalize
#python susy-interface/limitmaker.py 3l 4lI $T $O -l 35 -o SR --flags '-X blinding --asimov' --sigs "TChiNeuZZ4L_.*;TChiNeuZZ2L_.*;TChiNeuHZ_.*;TChiNeuHH_.*" --bkgs "fakes_matched_.*;prompt_.*;rares_.*;convs" --sys susy-ewkino/systs_dummy.txt --macros susy-ewkino/3l/functionsEWKopt.cc --mccs susy-ewkino/4l/mcc_ewkino.txt --finalize
#python susy-interface/limitmaker.py 3l 4lJ $T $O -l 35 -o SR --flags '-X blinding --asimov' --sigs "TChiNeuZZ4L_.*;TChiNeuZZ2L_.*;TChiNeuHZ_.*;TChiNeuHH_.*" --bkgs "fakes_matched_.*;prompt_.*;rares_.*;convs" --sys susy-ewkino/systs_dummy.txt --macros susy-ewkino/3l/functionsEWKopt.cc --mccs susy-ewkino/4l/mcc_ewkino.txt --finalize
#python susy-interface/limitmaker.py 3l 4lK $T $O -l 35 -o SR --flags '-X blinding --asimov' --sigs "TChiNeuZZ4L_.*;TChiNeuZZ2L_.*;TChiNeuHZ_.*;TChiNeuHH_.*" --bkgs "fakes_matched_.*;prompt_.*;rares_.*;convs" --sys susy-ewkino/systs_dummy.txt --macros susy-ewkino/3l/functionsEWKopt.cc --mccs susy-ewkino/4l/mcc_ewkino.txt --finalize

O="/afs/cern.ch/user/c/cheidegg/www/heppy/2016-11-07_ewk80X_sr4lopt_ALLBINS"
python susy-interface/limitmaker.py 3l 4lG $T $O -l 35 -o SR --flags '-X blinding --asimov' --sigs "TChiNeuZZ4L_.*;TChiNeuZZ2L_.*;TChiNeuHZ_.*;TChiNeuHH_.*" --bkgs "fakes_matched_.*;prompt_.*;rares_.*;convs" --sys susy-ewkino/systs_dummy.txt --macros susy-ewkino/3l/functionsEWKopt.cc --mccs susy-ewkino/4l/mcc_ewkino.txt --finalize










#eval "$base --pdir $O/SR/4lOpt/1taus/mix --sP nOSSF -A alwaystrue BR0taus 'BRnew==8'" 
#eval "$base --pdir $O/SR/4lOpt/2taus/mix --sP nOSSF -A alwaystrue BR0taus 'BRnew==9'" 
#eval "$base --pdir $O/SR/4lOpt/3taus/mix --sP nOSSF -A alwaystrue BR0taus 'BRnew==10'" 

## nOSLF
#eval "$base --pdir $O/SR/4lOpt/0taus/mix --sP nOSLF -A alwaystrue BR0taus 'BRnew==7'" 
#eval "$base --pdir $O/SR/4lOpt/1taus/mix --sP nOSLF -A alwaystrue BR0taus 'BRnew==8'" 
#eval "$base --pdir $O/SR/4lOpt/2taus/mix --sP nOSLF -A alwaystrue BR0taus 'BRnew==9'" 
#eval "$base --pdir $O/SR/4lOpt/3taus/mix --sP nOSLF -A alwaystrue BR0taus 'BRnew==10'" 
