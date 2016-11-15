#!/usr/bin/env python
import sys
import numpy as np
import random as rd
out = ''
SMS = 'T1tttt'

from yieldClass import *
from ROOT import *
def printDataCard(yds, ydsObs):
    folder = 'datacards_'+ out +'/'
    if not os.path.exists(folder): os.makedirs(folder) 
    bins = sorted(yds.keys())

    sampNames = [x.name for x in yds[bins[0]]]
    nSamps = len(sampNames)
    for x in sampNames:
        if "Scan_m" in x: signalName = x

    precision = 4
    
    try:                                                                                                                     
        os.stat(folder + signalName )                                                                                
    except:                                                                                                                  
        os.mkdir(folder + signalName )
    iproc = { key: i+1 for (i,key) in enumerate(sorted(reversed(sampNames)))}
    iproc.update({signalName: 0})
    
    for i,bin in enumerate(bins):
        datacard = open(folder + signalName + '/' +bin + '.card.txt', 'w'); 
        datacard.write("## Datacard for binfile %s (signal %s)\n"%(bin,signalName))
        
        datacard.write('##----------------------------------\n')
        datacard.write('bin         %s\n' % bin)
        obs = sum(yd.val for yd in ydsObs[bin])
        datacard.write('observation %s\n' % obs)
        datacard.write('##----------------------------------\n')
        klen = len(sampNames)
        kpatt = " %%%ds "  % klen
        fpatt = " %%%d.%df " % (klen,3)
        datacard.write('##----------------------------------\n')
        datacard.write('bin'+ ( ' ' * 32) +(" ".join([kpatt % bin     for p in sampNames]))+"\n")
        datacard.write('process'+ ( ' ' * 30)  +(" ".join([kpatt % p          for p in sampNames]))+"\n")
        datacard.write('process'+ ( ' ' * 30)  +(" ".join([kpatt % iproc[p]    for p in sampNames]))+"\n")
        datacard.write('rate'+ ( ' ' * 35)  +(" ".join([fpatt % yd.val for yd in yds[bin]]))+"\n")
        datacard.write('##----------------------------------\n')
        
        #bkg uncertainty define what you like, right now correlated accross bins and bkg samples, change if needed
        bkguncert =  0.1
        datacard.write('bkguncert lnN' + (' ' * 33) +  " ".join([kpatt % numToBar(1.0+bkguncert) if "can" not in yd.name else "-" for yd in yds[bin]]) + ' \n')
        



        
        #this includes the MC statistical uncertainty on the bkg and signal, uncorrelated accros bkgs and bins
        for i,yd in enumerate(yds[bin]):
            before = '       -  ' * i
            after = '       -  ' * (nSamps - i - 1)
            datacard.write('MCstats' + yd.name + '_SR_MB'+bin+' lnN  ' + (' ' * (28-len(yd.name)))  + before + " ".join([kpatt % numToBar(1.0+(yd.err/(yd.val+0.01))) ]) +  after +"\n")        
        #signal uncertainty, right now 20% correlated accross all bins (before gets the last value from previous loop, i.e. correct position)
        datacard.write('sigSyst lnN  ' + (' ' * (28))  + before + " 1.2 " + after + "\n")

    return 1


def numToBar(num):
    r = num
    if type(num) == float and abs(num - 1.0) < 0.001:
        r = '   -  '
    else: r = '%1.3f' % num
    return r

def valToBar(num):
    r = '%1.3f' % num
    return r

if __name__ == "__main__":

    ## remove '-b' option
    if '-b' in sys.argv:
        sys.argv.remove('-b')
        _batchMode = True

    if len(sys.argv) > 1:
        out = sys.argv[1]
        print '# out is', out
    else:
        print "No output folder name given!!"
        exit(0)

    ## Create Yield Storage
    ydsSys = YieldStore("lepYields") 
    storeDict = True

    #Define Signal pickle file
    pckname = "pickles/"+SMS+"_sigSysts_2016_all.pckz"
    if storeDict == True and os.path.exists(pckname):

        print "#Loading saved yields from pickle!"

        import cPickle as pickle
        import gzip

        ydsSys = pickle.load( gzip.open( pckname, "rb" ) )
#        print [name for name in ydsSys.samples if ("syst" in name and "mGo1500_mLSP1000" in name)]
 
    yds6 = YieldStore("lepYields")
    yds9 = YieldStore("lepYields")
    pattern = "lumi12p88/*/merged/LT*NJ68*"
    yds6.addFromFiles(pattern,("lep","sele")) 
    pattern = "lumi12p88/*/merged/LT*NJ9i.*"
    yds9.addFromFiles(pattern,("lep","sele"))


    
#    yds6.showStats()
#    yds9.showStats()

    ####SELECT DATA OR MC### (turn into options for the commandline at some point)
    useMC = True
    prefix =  'data'
    if useMC:
        prefix = 'background'

    readSystFile()
#    for mGo in range(600, 2000, 25):
#       for mLSP in range(0,1200,25):

    for mGo in range(1600, 2100, 100):
        for mLSP in range(50,150,50):
            for ydIn in (yds6, yds9):
                print "making datacards for "+str(mGo)+ ' '+str(mLSP)
                signal = SMS+'_Scan_mGo'+str(mGo)+'_mLSP'+str(mLSP)
                cat = 'SR_MB'
                sampsObs = [('background',cat),]
                ydsObs = ydIn.getMixDict(sampsObs)
                sampsBkg = [('TTsemiLep',cat),('TTdiLep',cat),('TTV',cat), ('SingleT',cat), ('WJets',cat), ('DY',cat), ('QCD',cat),]
                sampsSig = [(signal ,cat),]
                samps = sampsBkg + sampsSig

                ydsSig = ydIn.getMixDict(sampsSig)
                print ydsSig
                if type(ydsSig.values()[0][0]) == int:
                    print "signal not available will skip"
                    continue
                
                yds = ydIn.getMixDict(samps)

                printDataCard(yds, ydsObs)

                
