#!/usr/bin/env python                                                                                                             
import os, sys
import ROOT
eospath1 = '/eos/user/m/mdunser/dps-13TeV-combination/TREES_latest/'
eospath = '/eos/user/m/mdunser/dps-13TeV-combination/TREES_fr_2016/'
outputdir='test_friendsJune12'
batchQ='8nh'
logdir='test_log_jets_June12'

samplelist=['DoubleEG_2016B','DoubleEG_2016D','DoubleEG_2016F','DoubleEG_2016H_ds1','DoubleEG_2016C','DoubleEG_2016E','DoubleEG_2016G','DoubleEG_2016H_ds2']#TBar_tWch_noFullyHad','TTJets_DiLepton','TTJets_SingleLeptonFromTbar','T_tch_powheg','TBar_tch_powheg','TTJets_SingleLeptonFromT','T_tWch_noFullyHad','DYJetsToLL_M10to50_LO','QCD_Pt20to30_EMEnriched','QCD_Pt80to120_EMEnriched','QCD_Pt_30to80_bcToE','QCD_Pt120to170_EMEnriched','QCD_Pt30to50_EMEnriched','QCD_Pt_170to250_bcToE','QCD_Pt_80to170_bcToE','QCD_Pt170to300_EMEnriched','QCD_Pt50to80_EMEnriched','QCD_Pt_20to30_bcToE']#DoubleEG_2016B','DoubleEG_2016D','DoubleEG_2016F','DoubleEG_2016H_ds1','DoubleEG_2016C','DoubleEG_2016E','DoubleEG_2016G','DoubleEG_2016H_ds2']#'WJetsToLNu_LO','QCD_Mu15','DYJetsToLL_M50_LO_ext','DoubleEG_2016B_reMiniAOD','DoubleEG_2016C_reMiniAOD','DoubleEG_2016D_reMiniAOD','DoubleEG_2016E_reMiniAOD','DoubleEG_2016F_reMiniAOD','DoubleEG_2016G_reMiniAOD','DoubleEG_2016H_ds1_reMiniAOD','DoubleEG_2016H_ds2_reMiniAOD']#SingleElectron_2016H_ds2_reMiniAOD','SingleElectron_2016H_ds1_reMiniAOD', 'SingleElectron_2016G_reMiniAOD','SingleElectron_2016F_reMiniAOD','SingleElectron_2016E_reMiniAOD','SingleElectron_2016D_reMiniAOD','SingleElectron_2016C_reMiniAOD','SingleElectron_2016B_reMiniAOD','MuonEG_2016B_reMiniAOD','MuonEG_2016D_reMiniAOD','MuonEG_2016F_reMiniAOD','MuonEG_2016H_ds1_reMiniAOD','MuonEG_2016C_reMiniAOD','MuonEG_2016E_reMiniAOD','MuonEG_2016G_reMiniAOD','MuonEG_2016H_ds2_reMiniAOD']

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

