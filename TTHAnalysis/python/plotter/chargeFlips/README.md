#### Produce the mee histograms in lepton categories

```
./chargeFlips/makeMEECatHistos.py -P treedir/ chargeFlips/mca-chargeflip-control.txt chargeFlips/cuts-chargeflip-control.txt --mcc ttH-multilepton/ttH_2lss3l_triggerdefs.txt
```

#### Run fits from the root file, for MC (D=0), and data (D=1):

First compile the `chargeMisIdProb.cc`:

```
LIBRARY_PATH=$LD_LIBRARY_PATH g++ -o chMidProb chargeMisIdProb.cc `root-config --glibs --cflags` -lMinuit -lMinuit2 -lRooFit -lRooFitCore -I$CMSSW_RELEASE_BASE/src/ -lPhysicsToolsTagAndProbe
```

Run the combined fits:

```
./chMidProb -f meecathistos.root -D 0
./chMidProb -f meecathistos.root -D 1
```

Then copy the resulting rootfiles to the `data/fakerate/` directory:

```
cp meecathistos_data.root $CMSSW_BASE/src/CMGTools/TTHAnalysis/data/fakerate/QF_data_el.root
cp meecathistos_MC.root $CMSSW_BASE/src/CMGTools/TTHAnalysis/data/fakerate/QF_DY_el.root
```

#### Make the 1D plots:

```
./make1DPlots.py meecathistos_data.root meecathistos_MC.root
```


#### Run the closure test plots:

DY control region:

```
python mcPlots.py chargeFlips/mca-chargeflip-closure.txt chargeFlips/cuts-chargeflip-closure-DY.txt chargeFlips/plots-chargeflip.txt --s2v --tree treeProducerSusyMultilepton --legendBorder=0 --legendFontSize 0.055 --legendWidth=0.35 --showRatio --maxRatioRange 0.2 3.2 --poisson -j 8 -f -P treedir/ -l 3.99 --pdir plotDir/ --neg --mcc ttH-multilepton/ttH_2lss3l_triggerdefs.txt
```

ttbar control region:

```
python mcPlots.py chargeFlips/mca-chargeflip-closure.txt chargeFlips/cuts-chargeflip-closure-tt.txt chargeFlips/plots-chargeflip.txt --s2v --tree treeProducerSusyMultilepton --legendBorder=0 --legendFontSize 0.055 --legendWidth=0.35 --showRatio --maxRatioRange 0.2 3.2 --poisson -j 8 -f -P treedir/ -l 3.99 --pdir plotDir/ --neg --mcc ttH-multilepton/ttH_2lss3l_triggerdefs.txt
```




