# Specific instructions for the tHq analysis

#### Add the remotes for Benjamin's repository:

```
git remote add stiegerb https://github.com/stiegerb/cmgtools-lite.git -f -t tHq_80X_base
git push -u origin tHq_80X_base
```

#### [TODO]:

- Link to current set of minitrees at CERN
- Find out if we can put everything on the UNL T2 and run from there?
- Add example mca/cut/plot files


#### Producing friend trees

Friend trees are trees containing additional information to the original trees. Each entry (i.e. event) in the original trees has a corresponding entry in the friend tree. For the tHq analysis we create friend trees with additional event variables related to forward jets, e.g. the eta of the most forward jet in each event.

The main python class calculating this information for is in the file `python/tools/tHqEventVariables.py`. The `__call__` method of that class is called once per event and returns a dictionary associating each branch name to the value for that particular event. Currently, the class only calculates and stores the highest eta of any jet with pT greater than 25 GeV.

The class can be tested on a few events of a minitree by simply running `python tHqEventVariables.py tree.root`.

To produce the friend trees for many samples and events, a separate handler script is used, saved in `macros/prepareTHQEventVariableFriends.py`. It takes as first argument a directory with minitrees outputs, and as second argument a directory where it will store the output. To run it on a few events of a single sample, you can do this:
```
python prepareTHQEventVariableFriends.py -m tHqEventVariables -t treeProducerSusyMultilepton -N 10000 ra5trees/809_June9_ttH/ tHq_eventvars_Aug5 -d TTHnobb_mWCutfix_ext1 -c 1
```

You should use this to figure out how fast your producer is running, and adjust the chunk size (`-N` option) to have jobs of reasonable run times. Once this works, you can submit all the jobs for all samples to lxbatch, by running something like this:
```
python prepareTHQEventVariableFriends.py -m tHqEventVariables -t treeProducerSusyMultilepton -N 500000 ra5trees/809_June9_ttH/ tHq_eventvars_Aug11 -q 8nh
```

Note that the `-q` option specifies the queue to run on. The most common options would be `8nh` for jobs shorter than 8 hours, or `1nd` for jobs shorter than one day (24 hours). Keep an eye on the status of the jobs with the `bjobs` command, and look at the output of a running job with `bpeek <jobid>`. The STDOUT and STDERR log files of each job are stored in a directory named `LSFJOB_<jobid>`.

Once all the jobs have finished successfully, you can check the output files using the `friendChunkCheck.sh` script: cd to the output directory and run `friendChunkCheck.sh evVarFriend`. If there is no output from the script, all the chunks are present. To merge the junks, there is a similar script in `macros/leptons/friendChunkAdd.sh`. Run it with `. ../leptons/friendChunkAdd.sh evVarFriend`, inside the output directory.

If that went ok, you can remove all the chunk files and are left with only the friend tree files.

A first version of the trees is already produced and stored here: `/afs/cern.ch/user/s/stiegerb/work/TTHTrees/13TeV/tHq_eventvars_Aug11`.

*TODO*: add more variables like [these](https://github.com/stiegerb/cmg-cmssw/blob/thq_newjetid_for_518_samples/CMGTools/TTHAnalysis/macros/leptons/prepareTHQFriendTree.py)

#### Making basic plots using `mcPlots.py`

To be filled.

#### Some tips

-------

It's useful to have a symbolic link to the directory containing the minitree outputs in your working directory. E.g. like this:

```
ln -s /afs/cern.ch/work/p/peruzzi/ra5trees/809_June9_ttH
```

-------

Often we store the minitree files on eos, and save only a text file (`tree.root.url` in place of `tree.root`) with the location (something like `root://eoscms.cern.ch//eos/cms/store/...`). You can open them in one go like this:

```
root `cat /afs/cern.ch/user/p/peruzzi/work/ra5trees/809_June9_ttH/TTHnobb_mWCutfix_ext1/treeProducerSusyMultilepton/tree.root.url`
```

