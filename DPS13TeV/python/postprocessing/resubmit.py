#!/usr/bin/env python                                                                                                                           
import os, sys
import ROOT
eospath = '/eos/user/m/mdunser/w-helicity-13TeV/trees/trees_all_skims/'
logdir ='friends_log_v1'
outputdir='Full_Singlemu_friends_v1'
batchQ='8nh'
logdir='friends_log_v1'

#list1=( list( i for i in os.listdir("friends_log_v1") if i.endswith(".err") and  os.path.getsize("friends_log_v1/"+i) > 8000000) )
list1=[
'SingleMuon_Run2016D_part3_11.err'
]
for name in list1:
    dataset = '_'.join(name.split('_')[:-1])
    chunk = name.split('_')[-1].replace('.err','')
    cmd='bsub -q 8nh /afs/cern.ch/work/a/anmehta/work/TestingWW2/CMSSW_8_0_25/src/CMGTools/DPS13TeV/python/postprocessing/lxbatch_runner.sh /afs/cern.ch/work/a/anmehta/work/TestingWW2/CMSSW_8_0_25/src/CMGTools/DPS13TeV/python/postprocessing /afs/cern.ch/work/a/anmehta/work/TestingWW2/CMSSW_8_0_25 python postproc_batch.py -N 270000 -t treeProducerWMass --moduleList DEFAULT_MODULES /eos/user/m/mdunser/w-helicity-13TeV/trees/trees_all_skims/ Full_Singlemu_friends_v1 -d {Sample} -c {CHUNK} --friend'.format(Sample=dataset,CHUNK=chunk)
        #cmd='python postproc_batch.py -N 250000 -t treeProducerWMass --moduleList DEFAULT_MODULES {treePath} {outdir} -d {Sample} -c {CHUNK} --friend &'.format(treePath=eospath,outdir=outputdir,Sample=dataset,CHUNK=chunk)
    print cmd
    os.system(cmd)
    
