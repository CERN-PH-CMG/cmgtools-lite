#!/usr/bin/env python                                                                                                             
import os, sys
import ROOT
eospath = '/eos/user/m/mdunser/dps-13TeV-combination/TREES_fr_2016/'
outputdir='JetCleaning_1lskim_DblMu_friendsMay30_v1'
batchQ='8nh'
logdir='1lskim_JC_friends_log_May30'

samplelist=['DoubleMuon_2016B','DoubleMuon_2016D','DoubleMuon_2016F','DoubleMuon_2016H_ds1','DoubleMuon_2016C','DoubleMuon_2016E','DoubleMuon_2016G','DoubleMuon_2016H_ds2']#'WJetsToLNu_LO','QCD_Mu15','DYJetsToLL_M50_LO_ext','DoubleEG_2016B_reMiniAOD','DoubleEG_2016C_reMiniAOD','DoubleEG_2016D_reMiniAOD','DoubleEG_2016E_reMiniAOD','DoubleEG_2016F_reMiniAOD','DoubleEG_2016G_reMiniAOD','DoubleEG_2016H_ds1_reMiniAOD','DoubleEG_2016H_ds2_reMiniAOD']
#SingleElectron_2016H_ds2_reMiniAOD','SingleElectron_2016H_ds1_reMiniAOD', 'SingleElectron_2016G_reMiniAOD','SingleElectron_2016F_reMiniAOD','SingleElectron_2016E_reMiniAOD','SingleElectron_2016D_reMiniAOD','SingleElectron_2016C_reMiniAOD','SingleElectron_2016B_reMiniAOD','MuonEG_2016B_reMiniAOD','MuonEG_2016D_reMiniAOD','MuonEG_2016F_reMiniAOD','MuonEG_2016H_ds1_reMiniAOD','MuonEG_2016C_reMiniAOD','MuonEG_2016E_reMiniAOD','MuonEG_2016G_reMiniAOD','MuonEG_2016H_ds2_reMiniAOD']

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

