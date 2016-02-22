# Produce the mee histograms in lepton categories

```
./chargeFlips/makeMEECatHistos.py -P treeDir/ chargeFlips/mca-chargeflip-control.txt chargeFlips/cuts-chargeflip-control.txt
```

# Compile the chargeMisIdProb.cc code:

```
g++ -o chMidProb chargeMisIdProb.cc `root-config --glibs --cflags` -lMinuit -lMinuit2 -lRooFit -lRooFitCore
```

# Run fits from the root file, for MC (D=0), and data (D=1):

```
./chMidProb -f meecathistos.root -D 0
./chMidProb -f meecathistos.root -D 1
```

# Make the 1D plots:

```
./make1DPlots.py meecathistos_data.root meecathistos_MC.root
```
