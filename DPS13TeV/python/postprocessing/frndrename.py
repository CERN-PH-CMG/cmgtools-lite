#!/usr/bin/env python                                                                                                                           
import os, sys
import ROOT
eospath = 'JetCleaning_ElEl_friendsMay21/'
outputdir='JetCleaning_ElEl_friendsMay21_renamed/'
list1=( list( i for i in os.listdir(eospath) ) ) 

for name in list1:
    name1=name.split('_treeProducerSusyMultilepton_')[-1] 
    cmd='cp {indir}{infile} {outdir}{outfile}'.format(indir=eospath,outdir=outputdir,infile=name,outfile=name1)
    print cmd
    os.system(cmd)
    
