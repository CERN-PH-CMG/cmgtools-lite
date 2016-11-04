# tHq signal extraction procedure

### Produce datacards:

```
python makeShapeCards.py \
--savefile activate \
tHq-multilepton/mca-thq-3l-mcdata-frdata_limits.txt \
tHq-multilepton/cuts-thq-3l.txt \
thqMVA_ttv:thqMVA_tt 40,-1,1,40,-1,1 \
tHq-multilepton/signal_extraction/systsEnv.txt \
-P 809_June9_ttH_skimOnlyMC_3ltight_relax_prescale/ \
-P treedir/tHq_production_Sep2/ \
--tree treeProducerSusyMultilepton \
--s2v -j 8 -l 12.9 -f \
--xp data --asimov \
-W 'puw2016_vtx_4fb(nVert)' \
-F sf/t tHq_eventvars_Oct24_skim/evVarFriend_{cname}.root \
--Fs {P}/2_recleaner_v4_b1E2 \
--mcc ttH-multilepton/lepchoice-ttH-FO.txt \
--neg \
-o 3l \
--od tHq-multilepton/signal_extraction/cards \
--2d-binning-function "5:ttH_MVAto1D_5_3l_Marco"
```

- Needs a hack of makeShapeCards.py for the hardcoded path to a combine area. I.e. change the YRpath around line 53 to `/afs/cern.ch/user/s/stiegerb/combine/HiggsAnalysis/CombinedLimit/data/lhc-hxswg/sm/` or another one that's readable.
- Change from `--savefile activate` to `--infile activate` to rerun quickly with a different binning.
- Still need to use an optimized binning function. Something like: '--2d-binning-function "5:ttH_MVAto1D_5_3l_Marco"', where ttH_MVAto1D_5_3l_Marco is a function defined in `functions.cc`. This converts the 2D histogram into a 1D histogram to be fed to combine.
- (Might need to run twice to create all output.)
- Systematics are copied from ttH so far. Several are missing.
- Will want to script this in case of several categories/tests, or to combine with same-sign channel.

This produces three files: `..input.root`, `..card.txt`, `..bare.root`

### Run the limit calculation:

Note that you'll need to set your environment to a release area with `combine` available:

```
cd ~stiegerb/combine/; eval `scramv1 runtime -sh`; cd -;
```

Run on a single datacard:

```
combine -M Asymptotic --run blind --rAbsAcc 0.0005 --rRelAcc 0.0005 ttH_3l.card.txt
```

In case of several datacards, combine them first with `combineCards.py *card.txt > combined.txt`.

Then the "Expected 50.0%" is the number to be quoted.
