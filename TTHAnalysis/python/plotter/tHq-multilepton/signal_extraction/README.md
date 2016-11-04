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
-F sf/t tHq_eventvars_Oct24_skim/evVarFriend_{cname}.root \
--Fs {P}/2_recleaner_v4_b1E2 \
--mcc ttH-multilepton/lepchoice-ttH-FO.txt \
--neg \
-o 3l \
--od tHq-multilepton/signal_extraction/cards \
-L tHq-multilepton/functionsTHQ.cc \
--2d-binning-function "12:tHq_MVAto1D_3l_12"
```

- Change from `--savefile activate` to `--infile activate` to rerun quickly with a different binning.
- Binning function in `tHq-multilepton/functionsTHQ.cc`. This turns the 2d histogram of mva1 vs mva2 into a 1d histogram for shape fitting in combine.
- Keep track of reporting of empty bins and adjust binning function accordingly.
- Systematics are mostly copied from ttH so far. Needs to be checked.
- Will want to script this in case of several categories/tests, or to combine with same-sign channel.
- Need to fix pileup weight.

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

or use `make_limit.sh cards/ttH_3l.card.txt` to do everything in one go.

In case of several datacards, combine them first with `combineCards.py *card.txt > combined.txt`.

Then the "Expected 50.0%" is the number to be quoted.
