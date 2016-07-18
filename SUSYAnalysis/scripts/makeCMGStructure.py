#!/usr/bin/env python
import sys, glob, os
import numpy as np
import random as rd

inDir = sys.argv[1]
dirList = glob.glob(inDir+'/cmg*')
print dirList
execute = False

print "Run with python makeCMGStructure.py FOLDER_WITH_CRAB_NTUPLES"
print "Default is to not really do the change of filestructure, change execute to true, if you are happy with the pritout"
print "execute ", execute
print "Some folder don't really work, but the important stuff does"

names = ['JetHT',
         'SingleElectron',
         'SingleMuon',
         'DYJetsToLL_M-50_HT-100to200',
         'DYJetsToLL_M-50_HT-200to400',
         'DYJetsToLL_M-50_HT-400to600',
         'DYJetsToLL_M-50_HT-600toInf',
         'QCD_HT100to200',
         'QCD_HT300to500',
         'QCD_HT500to700',
         'QCD_HT700to1000',
         'QCD_HT1000to1500',
         'QCD_HT1500to2000',
         'QCD_HT2000toInf',
         'WJetsToLNu_HT-100To200',
         'WJetsToLNu_HT-200To400',
         'WJetsToLNu_HT-400To600',
         'WJetsToLNu_HT-600To800',
         'WJetsToLNu_HT-800To1200',
         'WJetsToLNu_HT-1200To2500',
         'WJetsToLNu_HT-2500ToInf',
         'TTJets_DiLept',
         'TTJets_SingleLeptFromTbar',
         'TTJets_SingleLeptFromT',
         'TTJets_HT-600to800',
         'TTJets_HT-800to1200',
         'TTJets_HT-1200to2500',
         'TTJets_HT-2500toInf',
         'TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX',
         'ST_t-channel_antitop_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8',
         'ST_t-channel_antitop_4f_leptonDecays_13TeV-powheg-pythia8',
         'ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8',
         'ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8',
         'ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8',
         'TTWJetsToLNu',
         'TTWJetsToQQ',
         'TTZToLLNuNu',
         'TTZToQQ',
         'WW',
         'WZ',
         'ZZ']


for d in dirList:
    newName = ''
    newName = [name for name in names if '_'+name in d]
    cmd = './makeDirStruct.sh ' + d
    print cmd
    if execute:
        os.popen(cmd)
    try:
        cmd = 'mv ' + d + ' ' + inDir+'/'+newName[0]
    except IndexError:
        raise NameError('Unknown folder: {0}'.format(d))
    print cmd
    print
    if execute:
        os.popen(cmd)
