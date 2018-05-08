# VVResonances

## General setup

This is very similar to the normal heppy setup, for now just pointing at the latest branch.

```
cmsrel 9_4_2
cd CMSSW_9_4_2/src
cmsenv
git cms-init
git remote add clelange git@github.com:clelange/cmg-cmssw.git -f -t jetID2017
cp /afs/cern.ch/user/c/cmgtools/public/sparse-checkout_80X_heppy .git/info/sparse-checkout
git checkout -b jetID2017 clelange/jetID2017
git remote add origin git@github.com:`git config user.github`/cmg-cmssw.git
git push -u origin jetID2017
git clone -o clelange git@github.com:clelange/cmgtools-lite.git -b Diboson_2017 CMGTools
cd CMGTools
git remote add origin git@github.com:`git config user.github`/cmgtools-lite.git
git push -u origin Diboson_2017
cd $CMSSW_BASE/src
scram b -j 8
```

## Running locally

`heppy` should be executed from the `$CMSSW_BASE/CMGTools/VVResonances/cfg` directory.
To test if its working, edit the `runVV_JJ_cfg.py` file, setting `test = 0` and execute:
```
heppy test runVV_JJ_cfg.py -N 200
```
The output will end up in `test`.

To see on which samples the code would run, just execute:
```
python runVV_JJ_cfg.py
```

## Running on the batch

There are two (three) options for running from lxplus.
For `bsub` system:
```
heppy_batch.py -r /store/cmst3/group/exovv/clange/HeppyProduction/trees_VV_20180220_data -o VV_20180220_data runVV_JJ_cfg.py -b 'bsub -q 1nd -u clange -o std_output.txt -J VV_20180220_data  < batchScript.sh'
```
where
- `/store/cmst3/group/exovv/clange/HeppyProduction/trees_VV_20180220_data` is the output directory for the ROOT trees (without prepending `/eos/cms`)
- the `-o` option defines the output directory for logs etc.
- the `-J` option defines the job name

For submission to condor using AFS (e.g. 8 hrs wall clock):
```
heppy_batch.py -r /store/cmst3/group/exovv/clange/HeppyProduction/trees_VV_20180220_data -o VV_20180220_data runVV_JJ_cfg.py -b 'run_condor_simple.sh -t 480 < batchScript.sh'
```

## Job resubmission

For `lxbatch/bsub` system:
```
cmgListChunksToResub -q 2nd trees_VV_20180220_data/
```
which will print out the commands to execute for resubmission.

For `condor`:
```
cmgListChunksToResub -q HTCondor trees_VV_20180220_data/
```
for which the command needs to be extended by -t XXX for the desired wall clock time in minutes.

Running a chunk locally:
```
cmgRunChunkLocally $chunkname
```

## Downloading output

Download files from EOS (after deleting failed chunks):
```
downloadTreesFromEOS.py -t vvTreeProducer VV_20170118
```
merge in Batch dir (use -r to remove existing dirs):
```
haddChunks.py -c .
```
when this finishes:
```
rm -rf *Chunk*
```
then merge `_ext` samples (currently not needed):
```
vvMergedExtended.py .
```
and again:
```
rm -rf *_Chunk*
```
then the VVpacking:
```
vvPack.py .
```
and then you just copy the root and the pck files to a computer with disk (or EOS):
```
scp *.* ...
```
delete remaining directories (careful here):
```
find . -name "??*" -type d -exec rm -r "{}" \;
```
