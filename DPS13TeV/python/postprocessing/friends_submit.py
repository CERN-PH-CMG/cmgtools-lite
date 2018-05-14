#!/usr/bin/env python                                                                                                             
import os, sys
import ROOT
eospath = '/eos/user/m/mdunser/dps-13TeV-combination/TREES_latest/'
outputdir='JetClean_friendsMay11'
batchQ='8nh'
logdir='friends_log_May09'

samplelist=['SingleElectron_2016H_ds2_reMiniAOD','SingleElectron_2016H_ds1_reMiniAOD', 'SingleElectron_2016G_reMiniAOD','SingleElectron_2016F_reMiniAOD','SingleElectron_2016E_reMiniAOD','SingleElectron_2016D_reMiniAOD','SingleElectron_2016C_reMiniAOD','SingleElectron_2016B_reMiniAOD','MuonEG_2016B_reMiniAOD','MuonEG_2016D_reMiniAOD','MuonEG_2016F_reMiniAOD','MuonEG_2016H_ds1_reMiniAOD','MuonEG_2016C_reMiniAOD','MuonEG_2016E_reMiniAOD','MuonEG_2016G_reMiniAOD','MuonEG_2016H_ds2_reMiniAOD']

dirs = os.listdir(eospath)
list1 = [] 
for sample in samplelist: 
    list1.extend( list( i for i in dirs if sample in i) )
#for sample in samplelist:
#   list1.extend( list( i for i in os.listdir(eospath) if sample in i) )
    cmd='python postproc_batch.py -N 150000 -q {bqueue} --log {logDir} --friend {treePath} {outdir}'.format(bqueue=batchQ, treePath=eospath,outdir=outputdir,logDir=logdir)
    cmd +=' -d '+' -d '.join(list1) 

print cmd
os.system(cmd)

