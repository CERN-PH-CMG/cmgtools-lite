#!/bin/bash
# Mostly based on @vischia's implementation at https://github.com/vischia/stopLimits/blob/master/estimateImpact.sh

# Usage: sh estimateImpact.sh [DATACARD NAME] [What to use as data: d (data), t0 (background only Asimov), t1 (s+b Asimov)] [Number of parallel jobs]  [OUTPUT shortname] [Extra commands to be feeded to combineToools]

# Prerequisite: installing the combineTool.py tool.
#       Method 1 (install only the script):
#                  bash <(curl -s https://raw.githubusercontent.com/cms-analysis/CombineHarvester/master/CombineTools/scripts/sparse-checkout-ssh.sh)
#       Method 2 (install the whole CombineHarvester):
#                  cd $CMSSW_BASE/src
#                  git clone https://github.com/cms-analysis/CombineHarvester.git CombineHarvester
#                  scram b -j 4


DATACARD=$1
ASIMOV=$2
JOBS=$3
OUTPUT=$4
EXTRA=$5
HERE="$PWD/"

 
if [ "$DATACARD" = "" ]; then
   echo "You need to provide a datacard!!"
   exit
fi

if [ "$ASIMOV" = "" ]; then
   echo "Defaulting to data"
fi

if [ "$ASIMOV" = "d" ]; then
   echo "Using data"
   ASIMOV=""
   PREFIX="d"
fi

if [ "$ASIMOV" = "t0" ]; then
   echo "Using background-only Asimov dataset"
   ASIMOV=" -t -1 --expectSignal 0 --rMin -10"
   PREFIX="t0"
fi

if [ "$ASIMOV" = "t1" ]; then
   echo "Using signal + background Asimov dataset"
   ASIMOV=" -t -1 --setParameters r_ttH=1,r_ttZ=1,r_ttW=1,r_tH=1 "
   PREFIX="t1"
fi

if [  "$JOBS" = ""  ]; then
    JOBS=4
    echo "Defaulting to 4 parallel jobs"
fi

if [ "$OUTPUT" = "" ]; then
   OUTPUT="impacts"   
fi

cd $OUTPUT


echo "---------------------------------"
echo "---------------------------------"

echo "You are about to run impacts for datacard $DATACARD with $JOBS parallel jobs. Additional toy options are set to $ASIMOV. Extra parameters to be passed to combine are: $EXTRA" 

echo "---------------------------------"
echo "---------------------------------"


if [[ "$DATACARD" != *"root"* ]]; then
   echo "Preliminary: convert to rootspace"
   echo "---------------------------------"
   text2workspace.py $HERE/${DATACARD}
   DATACARD="${DATACARD//.txt/.root}"
   echo "Card is $DATACARD"
fi



echo "First Stage: fit for each POI"
echo "-----------------------------"

#combineTool.py -M Impacts -d $HERE/${DATACARD} --doInitialFit --robustFit 1 $ASIMOV $EXTRA -m 1 -n $PREFIX --redefineSignalPOIs r_ttH,r_ttW,r_ttZ --floatOtherPOIs 1 


echo "Second Stage: fit scan for each nuisance parameter"
echo "--------------------------------------------------"

#combineTool.py -M Impacts -d $HERE/${DATACARD} --robustFit 1 --doFits --parallel $JOBS $ASIMOV $EXTRA -m 1 -n $PREFIX  --redefineSignalPOIs r_ttH,r_ttW,r_ttZ --job-mode SGE

echo "Third Stage: collect outputs"
echo "----------------------------"

combineTool.py -M Impacts -d $HERE/${DATACARD} -o impacts$PREFIX.json $ASIMOV $EXTRA -m 1 -n $PREFIX --redefineSignalPOIs r_ttH,r_ttW,r_ttZ 

echo "Fourth Stage: plot pulls and impacts"
echo "------------------------------------"

python plotImpacts_multiSignal.py -i impacts$PREFIX.json -o impacts$PREFIX --left-margin 0.2

cp $HERE/$DATACARD ./
cd $HERE
