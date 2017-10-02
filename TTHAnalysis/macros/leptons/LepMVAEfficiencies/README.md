## Produce lepton MVA efficiency maps

#### Content

- `lepTnPFriendTreeMaker.cc`: TTree::MakeClass based macro that processes trees produced with the `treeProducerSusyMultiLepton` analyzer. Selects dilepton events (see `SelectEvent` method) consistent with DY, then looks for tag leptons passing a given selection (see `SelectTagElectron`, `SelectTagMuon` methods). For each found tag lepton, looks for a probe lepton such that the pair passes a given selection (see `SelectPair`). The tree is then filled with a few properties of the tag lepton and the pair, and all necessary properties of the probe lepton to be flexible enough to calculate efficiencies.

- `runLepTnPFriendMaker.py`: Python script to steer the `lepTnPFriendTreeMaker` class and run it on all input files in a given directory (locally or on eos). Note that for remote files it will copy them to a local temp directory first (`/tmp/username/` by default) to speed up the process. When running on data, some of the MC-only branches are not found in the tree, so errors like `<TTree::SetBranchAddress>: unknown branch` are expected.

- `makeLepTnPFriends.py`: Python script to do the mass fit for each bin in pt, eta, nvertices, etc. and produce the efficiency plots and maps. Note that by default it expects a merged file for the data trees.

- `makeXSecWeights.py`: Use the sample definition file (by `default samples_13TeV_RunIISpring16MiniAODv2.py`) to find cross sections and the `SkimReport.pck` pickle files to find number of processed events, and generate sample weights. These are used to weight MC samples when running `makeLepTnPFriends.py`.

------------

#### Instructions to run

First, compile the tree class: ```root -l -b -q -n lepTnPFriendTreeMaker.cc+```

Produce the tag and probe trees:

```
python runLepTnPFriendMaker.py /store/cmst3/group/tthlep/peruzzi/TREES_TTH_180117_Summer16_JEC_mc25nsV5_data23SepV2_noClean_lepMVAretr_qgV1/ -q 8nh
```

This will process all files in that directory containing `2016` or `DYJetsToLL_M50` strings. For debugging, you can use the `-f/--filter` option to restrict to individual samples and the `-m` option to process only a certain number of events. To run in parallel, use the `-j/--jobs` option. To submit to batch, use the `-q/--queue` option.

By default, the output is stored in a directory called `tnptrees/`. You can change this with the `-o/--outDir` option.

Note that samples are checked to be data or not depending on whether their name contains the string `2016`.

Merge the data trees:

```
hadd tnptrees/Run2016.root tnptrees/*2016*.root
```

Generate the cross section weights (stored in `.xsecweights.pck` by default):

```
python makeXSecWeights.py treeDir/
```

Finally, run the fits and make the plots using `makeLepTnPFriends.py`. Modify the global variables at the top of the script to configure the binnings, pair selections, event selections, probe selections, and input files. The script caches the passed and total histograms in a pickle file (`tnppassedtotal.pck` by default).

```
python makeLepTnPFriends.py tnptrees/ -j 8
```

Note: when running in parallel mode, a warning message (`*** Break *** write on a pipe with no one to read it`) is normal.






