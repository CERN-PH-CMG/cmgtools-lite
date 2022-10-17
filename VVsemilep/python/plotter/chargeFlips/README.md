#### Produce the mee histograms in lepton categories

```
./chargeFlips/makeMEECatHistos.py -P treedir/ chargeFlips/mca-chargeflip-control.txt chargeFlips/cuts-chargeflip-control.txt --mcc ttH-multilepton/ttH_2lss3l_triggerdefs.txt --mcc ttH-multilepton/lepchoice-ttH-FO.txt
```

#### Run fits from the root file:

```
python fitMassHistos.py meecathistos.root
```

This will fit all the mass peaks and write out two files with sets of equations to solve, one for data, one for MC.


Then, compile the `chargeMisIdProb.cc`:

```
LIBRARY_PATH=$LD_LIBRARY_PATH g++ -o chMidProb chargeMisIdProb.cc `root-config --glibs --cflags` -lMinuit -lMinuit2 -lRooFit -lRooFitCore -I$CMSSW_RELEASE_BASE/src/ -lPhysicsToolsTagAndProbe
```

Run the combined fit on the equations files:

```
./chMidProb -f equations_data.dat && ./chMidProb -f equations_DY.dat
```

The resulting root files, called `chMidProb_data.root` and `chMidProb_DY.root` contain the histograms with charge misid probability maps. Copy them to the common area.

```
cp chMidIdProb_data.root $CMSSW_BASE/src/CMGTools/TTHAnalysis/data/fakerate/QF_data_el.root
cp chMidIdProb_DY.root $CMSSW_BASE/src/CMGTools/TTHAnalysis/data/fakerate/QF_DY_el.root
```

#### Make the 1D plots:

```
./make1DPlots.py chMidProb_data.root chMidProb_DY.root
```


#### Run the closure test plots:

DY control region:

```
python mcPlots.py \
chargeFlips/mca-chargeflip-closure.txt \
chargeFlips/cuts-chargeflip-closure-DY.txt \
chargeFlips/plots-chargeflip.txt \
--s2v --tree treeProducerSusyMultilepton --neg \
--legendBorder=0 --legendFontSize 0.055 --legendWidth=0.35 \
--showRatio --maxRatioRange 0.2 3.2 \
--poisson -j 8 -f -P treedir/ -l 36.8 \
--pdir plotDir/\
--mcc ttH-multilepton/ttH_2lss3l_triggerdefs.txt
--mcc ttH-multilepton/lepchoice-ttH-FO.txt
 --Fs {P}/1_recleaner_250117_v1
```

ttbar control region:

```
python mcPlots.py \
chargeFlips/mca-chargeflip-closure.txt \
chargeFlips/cuts-chargeflip-closure-tt.txt \
chargeFlips/plots-chargeflip.txt \
--s2v --tree treeProducerSusyMultilepton --neg \
--legendBorder=0 --legendFontSize 0.055 --legendWidth=0.35 \
--showRatio --maxRatioRange 0.2 3.2 \
--poisson -j 8 -f -P treedir/ -l 36.8 \
--pdir plotDir/\
--mcc ttH-multilepton/ttH_2lss3l_triggerdefs.txt
--mcc ttH-multilepton/lepchoice-ttH-FO.txt
 --Fs {P}/1_recleaner_250117_v1
```

