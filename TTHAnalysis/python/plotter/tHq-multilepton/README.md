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
- Prepare a basic version of tHq event variable friends


#### Some tips

Often we store the minitree files on eos, and save only a text file (`tree.root.url` in place of `tree.root`) with the location (something like `root://eoscms.cern.ch//eos/cms/store/...`). You can open them in one go like this:

```
root `cat /afs/cern.ch/user/p/peruzzi/work/ra5trees/809_June9_ttH/TTHnobb_mWCutfix_ext1/treeProducerSusyMultilepton/tree.root.url`
```


