#!/usr/bin/env python
#Script to read data cards and turn them either into a table that can be copied to Excel/OpenOffice
#1;2cor print out in latex format.

import shutil
import subprocess
import os
import sys
import glob
from multiprocessing import Pool
from ROOT import *
import math
from readYields import getYield, getScanYieldDict
from searchBins import *
######################GLOBAL VARIABLES PUT IN OPTIONS############
ignoreEmptySignal = True


def getYieldDict(cardFnames, region, sig = "", lep = "lep"):
    print "getting dict", sig
    yields = {}
    for cardFname in cardFnames:
        binname = os.path.basename(cardFname)
        binname = binname.replace('.merge.root','')
        tfile = TFile(cardFname,"READ")
        if 'Scan' in sig:
            yields[binname] = getScanYieldDict(tfile, sig ,region, lep)
            
        else:
            tfile.cd(region)
            dirList = gDirectory.GetListOfKeys()
            sourceYield = {}

            for k1 in dirList:
                print k1, k1.ReadObj().GetName()
                if 'Name' in k1.ReadObj().GetName() or 'name' in k1.ReadObj().GetName(): continue
                h1 = k1.ReadObj().GetName()
                
                (yd, yerr)  = getYield(tfile, h1, region, (lep,'sele'))
                if 'dummy' in sig:
                    sourceYield[h1] = (0.3, 0)
                else:
                    sourceYield[h1] = (yd, yerr)
                yields[binname] = sourceYield
    return yields


def getPredDict(cardFnames, lep = 'lep'):
    yields = {}
    for cardFname in cardFnames:
        binname = os.path.basename(cardFname)
        binname = binname.replace('.merge.root','')
        tfile = TFile(cardFname,"READ")
        h1 = "background"
 
        (ySR_MB, ySR_MBerr) = getYield(tfile, h1, "SR_MB", (lep,'sele'))

        (yCR_MB, yCR_MBerr) = getYield(tfile, h1, "CR_MB", ('lep','sele'))

        (yCR_SB, yCR_SBerr) = getYield(tfile, h1, "CR_SB", ('lep','sele'))
        (ySR_SB, ySR_SBerr) = getYield(tfile, h1, "SR_SB", ('lep','sele'))
        (Rcs_SB, Rcs_SBerr) = getYield(tfile, h1, "Rcs_SB", ('lep','sele'))
        (kappa, kappaerr) = getYield(tfile, h1, "Kappa", ('lep','sele'))
        
#        print  binname, "CR_SB", (yCR_SB, yCR_SBerr), "SR_SB", (ySR_SB, ySR_SBerr),"RCS_SB",(Rcs_SB, Rcs_SBerr), "Kappa", (kappa, kappaerr)

        #predSR_MB = yCR_MB * Rcs_SB * kappa
        predSR_MB = yCR_MB * Rcs_SB
        if  yCR_MB > 0.01  and kappa > 0.01 and Rcs_SB > 0.01:
#            predSR_MBerr = predSR_MB * math.sqrt( (yCR_MBerr/yCR_MB)**2 + (kappaerr/kappa)**2 + (Rcs_SBerr/Rcs_SB)**2)
            predSR_MBerr = predSR_MB * math.sqrt( (yCR_MBerr/yCR_MB)**2 + (kappaerr/kappa)**2 + (Rcs_SBerr/Rcs_SB)**2)
        else: predSR_MBerr =  1.0 * predSR_MB
        if predSR_MB < 0.001 :
            predSR_MB = 0.01
            predSR_MBerr = 0.01
            #        print  binname, predSR_MB, ySR_MB, yCR_MB, Rcs_SB, kappa
        sourceYield = {}
        sourceYield['data'] = getYield(tfile, 'data', "SR_MB", (lep,'sele'))
        sourceYield['RcsPred'] = (predSR_MB, predSR_MBerr)

        yields[binname] = sourceYield

    return yields

def getSystDict(cardFnames, region, sig = "", lep = "lep", uncert = "default"):
    yields = {}
    for cardFname in cardFnames:
        binname = os.path.basename(cardFname)
        binname = binname.replace('.merge.root','')
        tfile = TFile(cardFname,"READ")
        if 'Scan' in sig:
            sampleDict = getScanYieldDict(tfile, sig ,region, lep)

            if type(uncert) == float:
                sampleDict.update({key: ( uncert, 0)  for key in sampleDict.keys() } )
            
            yields[binname] = sampleDict


        else:
            tfile.cd(region)
            dirList = gDirectory.GetListOfKeys()
            sourceYield = {}

            for k1 in dirList:
                h1 = k1.ReadObj().GetName()
                
                (yd, yerr)  = getYield(tfile, h1, region, (lep,'sele'))
                if type(uncert) == float:
                    sourceYield[h1] = (uncert , 0)

                yields[binname] = sourceYield
    return yields

def divideTwoYieldDicts(yieldDict1, yieldDict2, correlated=False ):
    #return dict = yieldDict1/yieldDict2
    if not correlated:
        print "implemented"
        assert len(yieldDict1)==len(yieldDict2), "dictionaries have different size"

        dividedDict = {}
        for bin, v1 in yieldDict1.iteritems():
            v2 = yieldDict2[bin]
            perProcessDict = {}
            for process, yieldtupel1 in v1.iteritems():
                yieldtupel2 = v2[process]
                print process, yieldtupel1, yieldtupel2
                if yieldtupel2[0] !=0:
                    perProcessDict[process] = (yieldtupel1[0]/yieldtupel2[0], pow(yieldtupel1[1]/yieldtupel2[0],2) +pow(yieldtupel1[0]/pow(yieldtupel2[0],2) *yieldtupel2[1] ,2))
                else:
                    perProcessDict[process] = (-999,0)
                print process, yieldtupel1, yieldtupel2, perProcessDict[process]
            dividedDict[bin] = perProcessDict
#        (yieldsSig[bin][source][0] *  factor[source], yieldsSig[bin][source][1]        
        
        return dividedDict
    else:
        print "not implemented yet, no return defined"

def printBinnedTable(yieldsList, yieldsSig, printSource, name):
    benchmark = (1200,750)
    benchmark2 = (1500,0)
    factor = {benchmark2 : 145296.0/45886.0*0.0141903,benchmark:145296.0/99410.0*0.0856418}
    precision = 2
    f = open(name + '.tex','w')
    f.write('\\begin{table}[ht] \n ')
    binNames = sorted(yieldsList[0].keys())
    singleSourceNames = []
    regions = []
    region = ['MB', 'SB', '$\kappa$']
    for i,yields in enumerate(yieldsList):
        singleSourceNames.append(sorted( x for x in yields[binNames[0]].keys() if not('EWK' in x) and (x != 'TT' and x != 'TTincl')))
            #singleSourceNames.append(sorted( x for x in yields[binNames[0]].keys() if ('TT' in x and not 'TTV' in x and not 'TTd' in x and not 'TTs' in x)  ))

    singleSourceNames = sum(singleSourceNames, [])
    
    singleSourceNames.append(benchmark)    
    singleSourceNames.append(benchmark2)    
    SourceNames = singleSourceNames
    
    print type(benchmark)
    print SourceNames, singleSourceNames
    nSource = len(singleSourceNames) 
    nCol = nSource + 4
    f.write('\\tiny \n')
    f.write('\\caption{'+name.replace('_',' ')+'} \n')
    f.write('\\begin{tabular}{|' + (nCol *'%(align)s | ') % dict(align = 'c') + '} \n')

    f.write('\\hline \n')
    f.write('$L_T$ & $H_T$ & nB & binName &' +  ' %s ' % ' & '.join(map(str, singleSourceNames)) + ' \\\ \n')
    f.write(' $[$ GeV $]$  &   $[$GeV$]$ & &  '  + (nSource *'%(tab)s  ') % dict(tab = '&') + ' \\\ \\hline \n')
    #write out all the counts
    for i,bin in enumerate(binNames):
        (LTbin, HTbin, Bbin ) = bin.split("_")[0:3]        
        (LT, HT, B) = (binsLT[LTbin][1],binsHT[HTbin][1],binsNB[Bbin][1])           
        (LT0, HT0, B0 ) = ("","","") 
        if i > 0 :
            (LT0bin, HT0bin, B0bin ) = binNames[i-1].split("_")[0:3]
            (LT0, HT0, B0) = (binsLT[LT0bin][1],binsHT[HT0bin][1],binsNB[B0bin][1])           
        if LT != LT0:
            f.write(('\\cline{1-%s} ' + LT + ' & ' + HT + ' & ' + B + '&' + LTbin +', ' + HTbin + ', ' + Bbin) % (nCol))
        if LT == LT0 and HT != HT0:
            f.write(('\\cline{2-%s}  & ' + HT + ' & ' + B + '&' + LTbin +', ' + HTbin + ', ' + Bbin) % (nCol))
        elif LT == LT0 and HT == HT0:
            f.write('  &  & ' + B + '&' + LTbin +', ' + HTbin + ', ' + Bbin)
#        for sources, yields in zip(SourceNames, yieldsList):
        for yields in yieldsList:
            for source in SourceNames:
                print source
                if type(source) == str:
                    f.write((' & %.'+str(precision)+'f $\pm$ %.'+str(precision)+'f') % yields[bin][source])                

                elif type(source) == tuple:
                    print yieldsSig[bin][source], factor[source]
                    f.write((' & %.'+str(precision)+'f $\pm$ %.'+str(precision)+'f') % (yieldsSig[bin][source][0] *  factor[source], yieldsSig[bin][source][1] *  factor[source]))
        #print '--'
        f.write(' \\\ \n')

    f.write('\\hline \n')
    f.write('\\end{tabular} \n')
    f.write('\\end{table} \n')   
    return

def printBinnedRcsKappaTable(yieldsList, printSource, name, signedPercentage=False):
    precision = 4
    f = open(name + '.tex','w')
    f.write('\\begin{table}[ht] \n ')
    binNames = sorted(yieldsList[0].keys())
    singleSourceNames = []
    regions = []
    region = ['MB', 'SB', '$\kappa$']
    #for i,yields in enumerate(yieldsList):
    #    singleSourceNames.append(sorted( x for x in yields[binNames[0]].keys() if (x in printSource)))
    singleSourceNames.append(sorted( x for x in yieldsList[0][binNames[0]].keys() if (x in printSource)))
    singleSourceNames = sum(singleSourceNames, [])
    SourceNames = singleSourceNames

    nSource = len(singleSourceNames)*len(yieldsList)
    print nSource, SourceNames
    nCol = nSource + 4
    f.write('\\tiny \n')
    f.write('\\caption{'+name.replace('_',' ')+'} \n')
    f.write('\\begin{tabular}{|' + (nCol *'%(align)s | ') % dict(align = 'c') + '} \n')

    f.write('\\hline \n')
    f.write('$L_T$ & $H_T$ & nB & binName &' +  ' %s ' % ' & '.join(map(str, singleSourceNames)) + ' \\\ \n')
    f.write(' $[$ GeV $]$  &   $[$GeV$]$ & &  '  + (nSource *'%(tab)s  ') % dict(tab = '&') + ' \\\ \\hline \n')
    #write out all the counts
    for i,bin in enumerate(binNames):
        (LTbin, HTbin, Bbin ) = bin.split("_")[0:3]        
        (LT, HT, B) = (binsLT[LTbin][1],binsHT[HTbin][1],binsNB[Bbin][1])           
        (LT0, HT0, B0 ) = ("","","") 
        if i > 0 :
            (LT0bin, HT0bin, B0bin ) = binNames[i-1].split("_")[0:3]
            (LT0, HT0, B0) = (binsLT[LT0bin][1],binsHT[HT0bin][1],binsNB[B0bin][1])           
        if LT != LT0:
            f.write(('\\cline{1-%s} ' + LT + ' & ' + HT + ' & ' + B + '&' + LTbin +', ' + HTbin + ', ' + Bbin) % (nCol))
        if LT == LT0 and HT != HT0:
            f.write(('\\cline{2-%s}  & ' + HT + ' & ' + B + ' & ' + LTbin +', ' + HTbin + ', ' + Bbin) % (nCol))
        elif LT == LT0 and HT == HT0:
            f.write('  &  & ' + B + ' & ' + LTbin +', ' + HTbin + ', ' + Bbin)
        for yields in yieldsList:
            for source in SourceNames:
                if signedPercentage:
                    markRed = False
                    if abs((yields[bin][source][0]-1)*100.) >20: markRed = True
                    f.write((' & \\textcolor{red}{%+.2f\%%} ' if markRed else ' & %+.2f\%% ') % ((yields[bin][source][0]-1)*100.) )                
                else:
                    f.write((' & %.'+str(precision)+'f $\pm$ %.'+str(precision)+'f') % yields[bin][source])                
        f.write(' \\\ \n')

    f.write('\\hline \n')
    f.write('\\end{tabular} \n')
    f.write('\\end{table} \n')   
    return



def printAnyBinnedTable(yieldsList, name, precision=4):
    print "starting test"
    f = open(name + '.tex','w')
    f.write('\\begin{table}[ht] \n ')
    binNames = sorted(yieldsList[0][0].keys())
    singleSourceNames = []
    regions = []
    region = ['MB', 'SB', '$\kappa$']

    for dicts in yieldsList:
        printSource = dicts[1]
        for source in printSource:
            singleSourceNames.append(source[1])


#    singleSourceNames = sum(singleSourceNames, [])
    SourceNames = singleSourceNames

    nSource = len(singleSourceNames)#*len(yieldsList)
    print nSource, SourceNames
    nCol = nSource + 4
    f.write('\\tiny \n')
    f.write('\\caption{'+name.replace('_',' ')+'} \n')
    f.write('\\begin{tabular}{|' + (nCol *'%(align)s | ') % dict(align = 'c') + '} \n')

    f.write('\\hline \n')
    f.write('$L_T$ & $H_T$ & nB & binName &' +  ' %s ' % ' & '.join(map(str, singleSourceNames)) + ' \\\ \n')
    f.write(' $[$ GeV $]$  &   $[$GeV$]$ & &  '  + (nSource *'%(tab)s  ') % dict(tab = '&') + ' \\\ \\hline \n')
    #write out all the counts
    for i,bin in enumerate(binNames):
        (LTbin, HTbin, Bbin ) = bin.split("_")[0:3]        
        (LT, HT, B) = (binsLT[LTbin][1],binsHT[HTbin][1],binsNB[Bbin][1])           
        (LT0, HT0, B0 ) = ("","","") 
        if i > 0 :
            (LT0bin, HT0bin, B0bin ) = binNames[i-1].split("_")[0:3]
            (LT0, HT0, B0) = (binsLT[LT0bin][1],binsHT[HT0bin][1],binsNB[B0bin][1])           
        if LT != LT0:
            f.write(('\\cline{1-%s} ' + LT + ' & ' + HT + ' & ' + B + '&' + LTbin +', ' + HTbin + ', ' + Bbin) % (nCol))
        if LT == LT0 and HT != HT0:
            f.write(('\\cline{2-%s}  & ' + HT + ' & ' + B + '&' + LTbin +', ' + HTbin + ', ' + Bbin) % (nCol))
        elif LT == LT0 and HT == HT0:
            f.write('  &  & ' + B + '&' + LTbin +', ' + HTbin + ', ' + Bbin)
        for dicts in yieldsList:
            for source in dicts[1]:
                f.write((' & %.'+str(precision)+'f $\pm$ %.'+str(precision)+'f') % dicts[0][bin][source[0]])                

        f.write(' \\\ \n')

    f.write('\\hline \n')
    f.write('\\end{tabular} \n')
    f.write('\\end{table} \n')   
    return


def printDataCardsFromMC(mc, sig, mcSys, sigSys, signal, lep):
    
   # print sigSys.keys()
    signalPoint =  {'m1': ('mGlu',signal[0]) , 'm2': ('mLSP',signal[1]) }
    signalName = ('%s_%s') % signalPoint['m1'] + ('_%s_%s') % signalPoint['m2']
    dataCardDir = 'datacards_' + signalName
    try:
        os.stat(inDirSig + '/' + dataCardDir)
    except:
        os.mkdir(inDirSig + '/' + dataCardDir)


    binNames = sorted(mc.keys())
    for binName in binNames:
        sigp = {signalName: sig[binName][signal]}
        singleBkgNames = sorted([ x for x in mc[binName].keys() if not('EWK' in x or 'background' in x or 'data' in x)])
        myyields = mc[binName]
        myyields.update(sigp)
        #print myyields

        singleSourceNames = sorted([ x for x in myyields.keys() if not('EWK' in x or 'background' in x or 'data' in x)])

        allSys = {}

        #make sure we get all systematics together
        for syst in mcSys.keys():
            allSys.update( { syst : { p: 1 + mcSys[syst][binName][p][0]  for p in singleBkgNames } })
            if syst in sigSys:
                allSys[syst].update( { signalName: 1 + sigSys[syst][binName][signal][0] }  )
            elif not syst in sigSys:
                allSys[syst].update( { signalName: '-' } ) 

        for syst in sigSys.keys():
            allSys.update( { syst : { signalName: 1 + sigSys[syst][binName][signal][0] } } )
            if syst in mcSys:
                allSys[syst].update( { p: 1 + mcSys[syst][binName][p][0]  for p in singleBkgNames } )
            else:
                allSys[syst].update({ p : '-'  for p in singleSourceNames if p in singleBkgNames } )
        
        
            


        iproc = { key: i for (i,key) in enumerate(reversed(singleSourceNames))}
        #print 'print ' + binName +'_.card.txt'

        if ignoreEmptySignal and myyields[signalName][0] > 0.01:
            datacard = open(inDirSig + '/' + dataCardDir + '/' + binName +'_'+lep+'.card.txt', 'w'); 
            datacard.write("## Datacard for cut file %s (signal %s)\n"%(binName,signalName))
            
            #datacard.write("shapes *        * ../common/%s.input.root x_$PROCESS x_$PROCESS_$SYSTEMATIC\n" % binName)
            datacard.write('##----------------------------------\n')
            datacard.write('bin         %s\n' % binName)
            datacard.write('observation %s\n' % myyields['background'][0])
            datacard.write('##----------------------------------\n')
            klen = len(singleSourceNames)
            kpatt = " %%%ds "  % klen
            fpatt = " %%%d.%df " % (klen,3)
            datacard.write('##----------------------------------\n')
            datacard.write('bin             '+(" ".join([kpatt % binName     for p in singleSourceNames]))+"\n")
            datacard.write('process         '+(" ".join([kpatt % p           for p in singleSourceNames]))+"\n")
            datacard.write('process         '+(" ".join([kpatt % iproc[p]    for p in singleSourceNames]))+"\n")
            datacard.write('rate            '+(" ".join([fpatt % myyields[p][0] for p in singleSourceNames]))+"\n")
            datacard.write('##----------------------------------\n')
            
            for syst in allSys:
                name = syst
                if 'uBin' in name:
                    name = name.replace('uBin', binName)
                if 'uLep' in name:
                    name = name.replace('uLep', lep) 
                datacard.write(('%-12s lnN' % name) + " ".join([kpatt % numToBar(allSys[syst][p])  for p in singleSourceNames]) +"\n")             

            datacard.close()
        
    return

def numToBar(num):
    r = num
    if type(num) == float and abs(num - 1.0) < 0.001:
        r = '-'
    return r


# MAIN
if __name__ == "__main__":
    if len(sys.argv) > 2:
        cardDirectory = sys.argv[1]
        cardDirectorySig = sys.argv[2]
    else:
        print "Will stop, give input Dir"
        quit()

    doKappaChangeTables = False
    if len(sys.argv) > 3 and "KappaChange" in sys.argv[3]:
        doKappaChangeTables=True
        print "Will print out kappa change tables as well" 

    cardDirectory = os.path.abspath(cardDirectory)
    cardDirName = os.path.basename(cardDirectory)

    print 'Using cards from', cardDirName
    inDir = cardDirectory
    cardFnames = glob.glob(inDir+'/*/*68*.root')
    cardDnames = glob.glob(inDir+'/*/')
    strippedDirNames = [os.path.basename(name.rstrip('/')) for name in cardDnames]
    strippedDirNames.remove("merged") #this is the default and does not need to be printed for kappa-change table
    print strippedDirNames
    print [os.path.basename(name) for name in cardFnames]
    cardFnames9 = glob.glob(inDir+'/*/*9i*.root')
    inDirSig = cardDirectorySig
    cardFnamesSig = glob.glob(inDirSig+'/*/*.root')

    if 1==1:

        SR_MBDict = getYieldDict(cardFnames,  "SR_MB","","lep")
        CR_MBDict = getYieldDict(cardFnames,  "CR_MB","","lep")
        DLCR_MBDict = getYieldDict(cardFnames,  "DLCR_MB","","lep")
        CRSR_MBDict = divideTwoYieldDicts(CR_MBDict, SR_MBDict, correlated=False )
        DLCRSR_MBDict = divideTwoYieldDicts(DLCR_MBDict, SR_MBDict, correlated=False )

        SR_MBYields   = [ SR_MBDict,   [('EWK','EWK')] ]
        SRDiLep_MBYields   = [ SR_MBDict,   [('TTdiLep','TTdiLep')] ]
        CR_MBYields   = [ CR_MBDict,   [('EWK','EWK')] ]
        DLCR_MBYields = [ DLCR_MBDict, [('EWK','EWK')] ]
        DLCRDiLep_MBYields = [ DLCR_MBDict, [('TTdiLep','TTdiLep')] ]
        CRSR_MBYields     = [ CRSR_MBDict,     [('EWK','EWK')] ]
        DLCRSR_MBYields   = [ DLCRSR_MBDict,   [('EWK','EWK')] ]
        DLCRSRDiLep_MBYields   = [ DLCRSR_MBDict,   [('TTdiLep','TTdiLep')] ]

        printAnyBinnedTable((SR_MBYields, SRDiLep_MBYields, CR_MBYields, DLCR_MBYields, DLCRDiLep_MBYields, CRSR_MBYields, DLCRSR_MBYields, DLCRSRDiLep_MBYields),'CRSize', precision=1)




##########
        SR_MBDict = getYieldDict(cardFnames9,  "SR_MB","","lep")
        CR_MBDict = getYieldDict(cardFnames9,  "CR_MB","","lep")
        DLCR_MBDict = getYieldDict(cardFnames9,  "DLCR_MB","","lep")
        CRSR_MBDict = divideTwoYieldDicts(CR_MBDict, SR_MBDict, correlated=False )
        DLCRSR_MBDict = divideTwoYieldDicts(DLCR_MBDict, SR_MBDict, correlated=False )

        SR_MBYields   = [ SR_MBDict,   [('EWK','EWK')] ]
        SRDiLep_MBYields   = [ SR_MBDict,   [('TTdiLep','TTdiLep')] ]
        CR_MBYields   = [ CR_MBDict,   [('EWK','EWK')] ]
        DLCR_MBYields = [ DLCR_MBDict, [('EWK','EWK')] ]
        DLCRDiLep_MBYields = [ DLCR_MBDict, [('TTdiLep','TTdiLep')] ]
        CRSR_MBYields     = [ CRSR_MBDict,     [('EWK','EWK')] ]
        DLCRSR_MBYields   = [ DLCRSR_MBDict,   [('EWK','EWK')] ]
        DLCRSRDiLep_MBYields   = [ DLCRSR_MBDict,   [('TTdiLep','TTdiLep')] ]

        printAnyBinnedTable((SR_MBYields, SRDiLep_MBYields, CR_MBYields, DLCR_MBYields, DLCRDiLep_MBYields, CRSR_MBYields, DLCRSR_MBYields, DLCRSRDiLep_MBYields),'CRSize9', precision=1)




        sigYields = getYieldDict(cardFnamesSig,"SR_MB", "T1tttt_Scan", "lep")
        sigYieldsCR = getYieldDict(cardFnamesSig,"CR_MB", "T1tttt_Scan", "lep")
        sigYieldsSB = getYieldDict(cardFnamesSig,"SR_SB", "T1tttt_Scan", "lep")
        sigYieldsCR_SB = getYieldDict(cardFnamesSig,"CR_SB", "T1tttt_Scan", "lep")
        mcYields = getYieldDict(cardFnames,"SR_MB","","lep")
        

        printBinnedTable((mcYields,),  sigYields, [],'SR_table')
        printBinnedTable((getYieldDict(cardFnames,"CR_MB","","lep") ,),  sigYieldsCR, [],'CR_table')
        printBinnedTable((getYieldDict(cardFnames,"CR_SB","","lep") ,),  sigYieldsCR_SB, [],'CR_SBtable')
        printBinnedTable((getYieldDict(cardFnames,"SR_SB","","lep") ,),  sigYieldsSB, [],'SR_SBtable')

        dictRcs_MB = getYieldDict(cardFnames,"Rcs_MB","","lep")
        dictRcs_SB = getYieldDict(cardFnames,"Rcs_SB","","lep")
        dictKappa = getYieldDict(cardFnames,"Kappa","","lep")
        tableList = ['EWK','TT','TTincl','TTdiLep','TTsemiLep','WJets','TTV','data']
        #tableList = ['TT','TTincl']
        for name in tableList:
            printBinnedRcsKappaTable((dictRcs_MB, dictRcs_SB, dictKappa),  [name],'Rcs_table_'+name)

        if doKappaChangeTables:        
            dictsKappaChange =[]
            for strippedDir in strippedDirNames:
                cardFnamesStripped = glob.glob(inDir+'/'+strippedDir+'/*68*.root')
                dictsKappaChange.append(getYieldDict(cardFnamesStripped,"KappaChange","","lep"))
            for name in tableList:
                printBinnedRcsKappaTable(dictsKappaChange,  [name],'KappaChange_table_'+name, True)

            dictsKappaChange =[]
            for strippedDir in strippedDirNames:
                cardFnamesStripped = glob.glob(inDir+'/'+strippedDir+'/*9i*.root')
                dictsKappaChange.append(getYieldDict(cardFnamesStripped,"KappaChange","","lep"))
            for name in tableList:
                printBinnedRcsKappaTable(dictsKappaChange,  [name],'KappaChange9_table_'+name, True)

        sigYields9 = getYieldDict(cardFnamesSig,"SR_MB", "T1tttt_Scan", "lep")
        sigYields9CR = getYieldDict(cardFnamesSig,"CR_MB", "T1tttt_Scan", "lep")
        sigYields9SB = getYieldDict(cardFnamesSig,"SR_SB", "T1tttt_Scan", "lep")
        sigYields9CR_SB = getYieldDict(cardFnamesSig,"CR_SB", "T1tttt_Scan", "lep")
        mcYields9 = getYieldDict(cardFnames9,"SR_MB","","lep")
        printBinnedTable((mcYields9,), sigYields9, [],'SR_table_9')
        printBinnedTable((getYieldDict(cardFnames9,"CR_MB","","lep") ,), sigYields9CR, [],'CR_table_9')
        printBinnedTable((getYieldDict(cardFnames9,"CR_SB","","lep") ,), sigYields9SB, [],'CR_SBtable_9')
        printBinnedTable((getYieldDict(cardFnames9,"SR_SB","","lep") ,), sigYields9CR_SB, [],'SR_SBtable_9')
        dictRcs_MB9 = getYieldDict(cardFnames9,"Rcs_MB","","lep")
        dictRcs_SB9 = getYieldDict(cardFnames9,"Rcs_SB","","lep")
        dictKappa9 = getYieldDict(cardFnames9,"Kappa","","lep")

        for name in tableList:
            printBinnedRcsKappaTable((dictRcs_MB9, dictRcs_SB9, dictKappa9), [name],'Rcs_table_9_'+name)
    if 1==2:
        for i,cards in enumerate((cardFnames, cardFnames9)):
            dictYieldCR_SB = getYieldDict(cards,"CR_SB","","lep")
            dictYieldCR_MB = getYieldDict(cards,"CR_MB","","lep")
            dictYieldSR_SB = getYieldDict(cards,"SR_SB","","lep")
            dictRcs_SB = getYieldDict(cards,"Rcs_SB","","lep")
            dictKappa = getYieldDict(cards,"Kappa","","lep")
            dictPredSR_MB = getYieldDict(cards,"SR_MB_predict","","lep")
            
            printBinnedRcsKappaTable((dictYieldCR_SB,  dictYieldSR_SB, dictYieldCR_MB), ['QCD','EWK','data'],'yields_data_45jets'+str(i))
            printBinnedRcsKappaTable((dictRcs_SB,  ), ['data_QCDsubtr','EWK'],'RCS_dataQCDsubtr_ewk_45jets'+str(i))
            printBinnedRcsKappaTable((dictKappa,  ), ['EWK'],'Kappa_EWK'+str(i))
            printBinnedRcsKappaTable((dictPredSR_MB,  ), ['data_pred','EWK_pred'],'RCS_datapred_SR68jets'+str(i))
    if 1==1:
        

        YieldCR_MB = [ getYieldDict(cardFnames,"CR_MB","","lep"), [('QCD','QCD'),('EWK','EWK'),('data','data')] ]

        YieldCR_SB = [ getYieldDict(cardFnames,"CR_SB","","lep"), [('data_QCDsubtr','data - QCD$^{pred}$')] ]
        YieldSR_SB = [ getYieldDict(cardFnames,"SR_SB","","lep"), [('data_QCDsubtr','data - QCD$^{pred}$')] ]
        Rcs_SB = [ getYieldDict(cardFnames,"Rcs_SB","","lep") , [('data_QCDsubtr','$R_{CS}(data - QCD$^{pred}$)'), ('EWK','$R_{CS}^{EWK}$')]]
        printAnyBinnedTable((YieldCR_SB,  YieldSR_SB, Rcs_SB),'test')
            
        '''for lep in ('ele','mu'):
        sig = getYieldDict(cardFnamesSig,"SR_MB", "T1tttt_Scan", lep)
        mc = getYieldDict(cardFnames,"SR_MB","", lep)
        mcSys = {"Flat_uBin_Lep": getSystDict(cardFnames,"SR_MB","dummy", lep, 0.3),
                 "FlatLumi_Bin_Lep": getSystDict(cardFnames,"SR_MB","dummy", lep, 0.1) }
        
        sigSys  = { "Xsec_Bin_Lep": getSystDict(cardFnamesSig,"SR_MB", "T1tttt_Scan_Xsec-Up",lep),
                    "FlatSig_Bin_Lep": getSystDict(cardFnamesSig,"SR_MB", "T1tttt_Scan_Xsec-Up",lep, 0.2),
                    "FlatLumi_Bin_Lep": getSystDict(cardFnamesSig,"SR_MB", "T1tttt_Scan_Xsec-Up",lep, 0.1) }
        
        printDataCardsFromMC(mc, sig, {},{},(1200,750), lep)
        '''
        
#    pred = getPredDict(cardFnames, 'lep')
#    printBinnedTable(pred, sigYields, 'PredTable')
    #loop stuff needs fixing
    #for sig in sigYields['LT1_HT0_NB1_NJ68_SR'].keys():
    #    print "processing datacards for ", sig
    #    printDataCardsFromMC(mcYields, sigYields, sig)
