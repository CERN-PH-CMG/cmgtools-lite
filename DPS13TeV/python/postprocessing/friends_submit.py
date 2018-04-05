#!/usr/bin/env python                                                                                                             
import os, sys
import ROOT
eospath = '/eos/user/m/mdunser/w-helicity-13TeV/trees/trees_all_skims/'
outputdir='DPS_HWPP_friends_v1'
batchQ='8nh'
logdir='friends_log_v1'

samplelist=['WW_DPS_herwig']#'WZTo3LNu_fxfx_part2','WZTo3LNu_fxfx_part1','SingleMuon_Run2016','SingleMuon_Run2016C','SingleMuon_Run2016D','SingleMuon_Run2016E','SingleMuon_Run2016F','SingleMuon_Run2016G','SingleMuon_Run2016H']

dirs = os.listdir(eospath)
list1 = [] 
for sample in samplelist: 
    list1.extend( list( i for i in dirs if sample in i) )
#for sample in samplelist:
  #  list1.extend( list( i for i in os.listdir(eospath) if sample in i) )
cmd='python postproc_batch.py -N 270000 -q {bqueue} {treePath} {outdir} --log {logDir} --friend '.format(bqueue=batchQ, treePath=eospath,outdir=outputdir,logDir=logdir)
cmd +=' -d '+' -d '.join(list1) 

print cmd
os.system(cmd)
