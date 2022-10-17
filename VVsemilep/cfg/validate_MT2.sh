#!/bin/bash



if [[ "$#" -eq 0 ]]; then
echo "ERROR: the script needs at least one argument. Relunch it with one of the following options:"
echo "source validate_MT2.sh inputFolder"
echo "./validate_MT2.sh fileA.root fileB.root labelA labelB outputFolderName"
exit;
fi;

if [[ "$#" -eq 1 ]]; then
    X=$PWD/$1; 

# $1 is VALIDATEMT2
# copy files mt2_tree.root inside
# CMGTools/TTHAnalysis/cfg/VALIDATEMT2/SNT/mt2/mt2_tree.root
# CMGTools/TTHAnalysis/cfg/VALIDATEMT2/ETHCERN/mt2/mt2_tree.root
# to dun execute: source validate_MT2.sh VALIDATEMT2


    if test \! -d $X/ETHCERN; then echo "Did not find ETHCERN in $X"; exit 1; fi
    test -L $PWD/SNT || ln -sd $PWD/SNT $X/ -v;
    ( cd ../python/plotter; 
	python mcPlots.py -f --tree mt2  -P $X susy-mT2/validation_mca_MT2.txt susy-mT2/validation_MT2.txt susy-mT2/validation_plots_MT2.txt --pdir plots/70X/validation -p ref_ttHWWdata,ttHWWdata -u -e --plotmode=norm --showRatio --maxRatioRange 0.65 1.35 --flagDifferences
    )

## susy-mT2/validation_mca_MT2.txt --> this contains style
## susy-mT2/validation_MT2.txt --> contains selections
## susy-mT2/validation_plots_MT2.txt --> contains content, plot titles and binning



fi;

if [[ "$#" -eq 6 ]]; then
eval `scramv1 runtime -sh`
workingDir="$PWD"

fileA="$1"
fileB="$2"

labelA="$3"
labelB="$4"
outputFolder="$5"
isDataMC="$6"

if [ -d $outputFolder ]; then
    echo "output folder " $outputFolder " already exists. Exiting.."
    exit;
else
    mkdir $outputFolder;
    mkdir -p $outputFolder/$labelA/mt2;
    mkdir -p $outputFolder/$labelB/mt2;
    cp $fileA $outputFolder/$labelA/mt2/mt2_tree.root
    cp $fileB $outputFolder/$labelB/mt2/mt2_tree.root


# Here I create a dummy pickle file with the 'All Events' entry, so that the events can be rescaled in the standard way
    pythonTmpScript=$Rand.py
    cat <<EOF > $pythonTmpScript
#!/usr/bin/python
import pickle
file = open("dummyPickle.pck",'wb')
pck = [['All Events', 100], ['Sum Weights', 100.0]]
pickle.dump(pck,file)
file.close()
EOF
    chmod 755 $pythonTmpScript
    ./$pythonTmpScript
    rm $pythonTmpScript


    mkdir -p $outputFolder/$labelA/skimAnalyzerCount
    mkdir -p $outputFolder/$labelB/skimAnalyzerCount
    cp dummyPickle.pck $outputFolder/$labelA/skimAnalyzerCount/SkimReport.pck
    mv dummyPickle.pck $outputFolder/$labelB/skimAnalyzerCount/SkimReport.pck
fi 



### Here one should specify the weightes used to rescale the events in one or both samples ### 
cat <<EOF > $outputFolder/inputs.txt
ttHWW   : $labelB : 1.*puWeight*weight_btagsf*weight_lepsf*weight_isr ; FillColor=ROOT.kOrange+10 , Label="$labelB"
ref_ttHWW+ : $labelA : 1. ; FillColor=ROOT.kAzure+2, Label="$labelA"
EOF


cd ../python/plotter/

if [[ "$isDataMC" == "-data" ]]; then
    python mcPlots.py -f --tree mt2  -P $workingDir/$outputFolder  $workingDir/$outputFolder/inputs.txt susy-mT2/validation_MT2.txt susy-mT2/validation_plots_MT2.data.txt --pdir $workingDir/$outputFolder/plots -p ref_ttHWW,ttHWW  -u -e --plotmode=norm --showRatio --maxRatioRange 0.65 1.35 --flagDifferences --toleranceForDiff 0.005
elif [[ "$isDataMC" == "-mc" ]]; then
    python mcPlots.py -f --tree mt2  -P $workingDir/$outputFolder  $workingDir/$outputFolder/inputs.txt susy-mT2/validation_MT2.txt susy-mT2/validation_plots_MT2.txt --pdir $workingDir/$outputFolder/plots -p ref_ttHWW,ttHWW  -e --plotmode=norm --showRatio --maxRatioRange 0.65 1.35 --flagDifferences --toleranceForDiff 0.005
fi;

cd $OLDPWD

cp $outputFolder/$labelA/mt2/mt2_tree.root $outputFolder/plots/$labelA.root
cp $outputFolder/$labelB/mt2/mt2_tree.root $outputFolder/plots/$labelB.root

fi;