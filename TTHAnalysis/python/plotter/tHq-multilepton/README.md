# Specific instructions for the tHq analysis

### Add the remotes for Benjamin's repository and get the `tHq_80X_base` branch:

```
git remote add stiegerb https://github.com/stiegerb/cmgtools-lite.git -f -t tHq_80X_base
git checkout -b tHq_80X_base stiegerb/tHq_80X_base
git push -u origin tHq_80X_base
```

A current set of minitree outputs is at:
```
/afs/cern.ch/work/p/peruzzi/ra5trees/809_June9_ttH_skimOnlyMC_3ltight_relax_prescale
```
You might have to ask Marco Peruzzi for access rights to it.

----------------

### Producing mini trees

It's advisable to put the version of the code used for a production on a separate branch on github. The branch used for the ICHEP samples is on the `80X_for2016basis_ttH` branch on [Marco's github](https://github.com/peruzzim/cmgtools-lite/tree/80X_for2016basis_ttH/TTHAnalysis/cfg).

Set it up like so:

```
cd $CMSSW_BASE/src
git remote add peruzzim https://github.com/peruzzim/cmg-cmssw.git -t heppy_80X_for2016basis  -f
git checkout -b heppy_80X_for2016basis peruzzim/heppy_80X_for2016basis
# Note that there is a hot fix for which you need this also: (c.f. PR [#661](https://github.com/CERN-PH-CMG/cmg-cmssw/pull/661))
git clone https://github.com/Werbellin/RecoEgamma_8X RecoEgamma
# Clean and recompile
scram b clean
scram b -j 9
```

The samples are defined in files in `CMGTools/RootTools/python/samples/`, e.g. in `samples_13TeV_RunIISpring16MiniAODv2.py`. So to add or update a sample, define it in the appropriate file there.

The configuration file used to run the production is:
```
TTHAnalysis/cfg/run_susyMultilepton_cfg.py
```

To run on specific samples, edit the code around [these lines](https://github.com/peruzzim/cmgtools-lite/blob/80X_for2016basis_ttH/TTHAnalysis/cfg/run_susyMultilepton_cfg.py#L369).

The command to test running on the first file of the first sample is then:
```
heppy myTest run_susyMultilepton_cfg.py -p 0 -o nofetch -j 1 -o test=1 -o analysis=susy
```

Note that the first time running will take a while, as it submits DAS queries for all the samples and caches the results (in `~/.cmgdatasets/`). Note also that you need a valid grid certificate for the DAS queries to work (`voms-proxy-init -voms cms -rfc` to get a valid token; check [this TWiki](https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookStartingGrid#ObtainingCert) on how to get a certificate).

Check that the output is ok before submitting jobs to the batch to run on the full samples. To submit to batch, you use these commands:

```
heppy_batch.py -r /store/user/stiegerb/remote_output -o local_directory --option analysis=susy run_susyMultilepton_cfg.py -b 'bsub -q 1nd -u stiegerb -o std_output.txt -J job_name < batchScript.sh'
```

The relevant options are: `-r remote_dir` to specify an output directory on eos (or don't specify to store locally); `-o dirname` for the local directory name; `--option analysis==susy` to give the HeppyOptions corresponding to the `-o` from before; `-J job_name` to specify the name of the jobs.

Once the jobs are completed, check that they are all there, i.e. that you have an output directory for each chunk. Then you can check if each of the output directories is ok by using `heppy_check.py outputdir/`, and finally merge the chunks by running `heppy_hadd.py outputdir/` -c.

----------------

### Producing friend trees

Friend trees are trees containing additional information to the original trees. Each entry (i.e. event) in the original trees has a corresponding entry in the friend tree. For the tHq analysis we create friend trees with additional event variables related to forward jets, e.g. the eta of the most forward jet in each event.

The main python class calculating this information for is in the file `python/tools/tHqEventVariables.py`. The `__call__` method of that class is called once per event and returns a dictionary associating each branch name to the value for that particular event. Currently, the class only calculates and stores the highest eta of any jet with pT greater than 25 GeV (stored in a branch named "maxEtaJet25").

The class can be tested on a few events of a minitree by simply running `python tHqEventVariables.py tree.root`.

To produce the friend trees for many samples and events, a separate handler script is used, saved in `macros/prepareTHQEventVariableFriends.py`. It takes as first argument a directory with minitrees outputs, and as second argument a directory where it will store the output. To run it on a few events of a single sample, you can do this:
```
python prepareTHQEventVariableFriends.py -m tHqEventVariables -t treeProducerSusyMultilepton -N 10000 ra5trees/809_June9_ttH/ tHq_eventvars_Aug5 -d TTHnobb_mWCutfix_ext1 -c 1
```

Or, with a friend tree included:
```
python prepareTHQEventVariableFriends.py -m tHqEventVariables -t treeProducerSusyMultilepton -N 10000 ra5trees/809_June9_ttH/ tHq_eventvars_Oct21 -d TTHnobb_mWCutfix_ext1 -c 1 -F sf/t ra5trees/809_June9_ttH/2_recleaner_v4_b1E2/evVarFriend_{cname}.root
```

You should use this to figure out how fast your producer is running, and adjust the chunk size (`-N` option) to have jobs of reasonable run times. Once this works, you can submit all the jobs for all samples to lxbatch, by running something like this:
```
python prepareTHQEventVariableFriends.py -m tHqEventVariables -t treeProducerSusyMultilepton -N 500000 ra5trees/809_June9_ttH/ tHq_eventvars_Aug11 -q 8nh
```

Note that the `-q` option specifies the queue to run on. The most common options would be `8nh` for jobs shorter than 8 hours, or `1nd` for jobs shorter than one day (24 hours). Keep an eye on the status of the jobs with the `bjobs` command, and look at the output of a running job with `bpeek <jobid>`. The STDOUT and STDERR log files of each job are stored in a directory named `LSFJOB_<jobid>`.

Once all the jobs have finished successfully, you can check the output files using the `friendChunkCheck.sh` script: cd to the output directory and run `friendChunkCheck.sh evVarFriend`. If there is no output from the script, all the chunks are present. To merge the junks, there is a similar script in `macros/leptons/friendChunkAdd.sh`. Run it with `. ../leptons/friendChunkAdd.sh evVarFriend`, inside the output directory.

If that went ok, you can remove all the chunk files and are left with only the friend tree files.

A first version of the trees is already produced and stored here: `/afs/cern.ch/user/s/stiegerb/work/TTHTrees/13TeV/tHq_eventvars_Aug12`.

*TODO*: add more variables like [these](https://github.com/stiegerb/cmg-cmssw/blob/thq_newjetid_for_518_samples/CMGTools/TTHAnalysis/macros/leptons/prepareTHQFriendTree.py)

----------------

### Making basic plots using `mcPlots.py`

The main script for making basic plots in the framework is in `python/plotter/mcPlots.py`, which uses the classes in `mcAnalysis.py` (for handling the samples) and `tree2yield.py` (for getting yields/histograms from the trees). It accepts three text files as inputs, one specifying the data and MC samples to be included, one listing the selection to be applied, and one configuring the variables to be plotted. Examples for these there files are in the `python/plotter/tHq-multilepton/` directory (where this README is also), with some explanation on their format in comments inside the files.

A full example for making plots with all corrections is the following:

```
python mcPlots.py \
tHq-multilepton/mca-thq-3l-mcdata-frdata.txt \
tHq-multilepton/cuts-thq-3l.txt \
tHq-multilepton/plots-thq.txt \
--s2v \
--tree treeProducerSusyMultilepton \
--showRatio --poisson \
-j 8 \
-f \
-P 809_June9_ttH_skimOnlyMC_3ltight_relax_prescale/ \
-P treedir/tHq_production_Sep2/ \
-l 12.9 \
--pdir tHq-multilepton/plots_Sep9/ \
-F sf/t tHq_eventvars_Aug12/evVarFriend_{cname}.root \
--Fs {P}/2_recleaner_v4_b1E2 \
--mcc ttH-multilepton/lepchoice-ttH-FO.txt \
-W 'puw2016_vtx_4fb(nVert)'
```

Note that this uses some symbolic links to the corresponding tree directories.

The important options are:

- `-P treedir/`: Input directory containing the minitree outputs. Can give multiple paths, the code will look through them in order.
- `--pdir plotdir/`: The output directory for the plots
- `-l 12.9`: Integrated luminosity to scale the MC to (in inverse femtobarn)
- `-j 8`: Number of processes to run in parallel
- `-f`: Only apply the full set of cuts at once. Without this, it will produce sequential plots for each line in the cut file.
- `-F sf/t directory/evVarFriend_{cname}.root`: Add the tree named `sf/t` in these files as a friend
- `--mcc textfile.txt`: Read this file defining new branches as shortcuts
- `-W 'weightexpression'`: Apply this event weight

If everything goes according to plan, this will produce an output directory with the plots in `.pdf` and `.png` format, a text file with the event yields, as well as a copy of the mca, cut, and plot files, the command string used, and a root file with the raw histograms.

----------------

### Some tips

- It's useful to have a symbolic link to the directory containing the minitree outputs in your working directory. E.g. like this:

```
ln -s /afs/cern.ch/work/p/peruzzi/ra5trees/809_June9_ttH
```

- Often we store the minitree files on eos, and save only a text file (`tree.root.url` in place of `tree.root`) with the location (something like `root://eoscms.cern.ch//eos/cms/store/...`). You can open them in one go like this:

```
root `cat /afs/cern.ch/user/p/peruzzi/work/ra5trees/809_June9_ttH/TTHnobb_mWCutfix_ext1/treeProducerSusyMultilepton/tree.root.url`
```

