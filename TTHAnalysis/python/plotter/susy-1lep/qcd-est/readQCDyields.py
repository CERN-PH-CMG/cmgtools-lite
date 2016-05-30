#!/usr/bin/env python

import shutil
import subprocess
import os
import sys
import glob
from multiprocessing import Pool
from ROOT import *

def readRatios(fname = "f_ratios_NJ34_Nb0.txt"):

    ratioDict = {}

    rfile = open(fname)

    for line in rfile.readlines():

        if 'ST' in line:
            (name,ratio,err) = line.split()

            # filter STX
            stbin = name[name.find('ST'):name.find('ST')+3]

            ratioDict[stbin] = (float(ratio),float(err))

    print 'Read ratios from', fname
    for bin in ratioDict:
        print "%s:\t%f +/- %f" %(bin, ratioDict[bin][0], ratioDict[bin][1])

    rfile.close()

    return ratioDict

def applyRatio(binname, nAnti):
    # scale yield with ratio and get correct yield

    return (nPred, nPredErr)

def _getYieldsFromInput(inargs):

    (sample, cardDir, binName, ratDict) = inargs

    if len(inargs) < 1:
        return (binName,[0,0])

    cardName = cardDir+"/common/QCDyield_"+binName+".input.root"

    #print "# Starting Bin:", binName

    cardf = TFile(cardName,"READ")

    # get anti-selected histo
    hAnti = cardf.Get("x_QCDanti")
    nAnti = hAnti.Integral()
    nAntiErr = hAnti.GetBinError(1)

    # get selected histo
    hSel = cardf.Get("x_QCDsel")
    nSel = hSel.Integral()
    nSelErr = hSel.GetBinError(1)

    nPred = 0
    nPredErr = 0

    cardf.Close()

    # Apply f-ratios for prediction
    if ratDict != {} and nAnti != 0:
        # filter STX from binname
        stbin = binName[binName.find('ST'):binName.find('ST')+3]

        #print 'Going to apply ratios in ST bin:', stbin

        fRatio = ratDict[stbin][0]
        fRatioErr = ratDict[stbin][1]

        nPred = nAnti * fRatio

        nPredErr = nPred * sqrt(nAntiErr/nAnti*nAntiErr/nAnti +  fRatioErr/fRatio*fRatioErr/fRatio)
        #print nAnti, fRatio, nPred , nSel

        return (binName,[nAnti, nAntiErr,nSel, nSelErr, nPred, nPredErr])
    else:
        #print 'No ratios given'
        return (binName,[nAnti, nAntiErr,nSel, nSelErr, nPred, nPredErr])

def makeTable(yieldDict, format = "text"):

    # sort by bin name
    ykeys = sorted(yieldDict.keys())
    #print 'KEYS', sorted(ykeys)

    if format == "text":

        # Print yields
        print 80*'#'
        print "Yields with zero selected"
        print "Bin:\t\tNanti\t\t\t\t\tNpredict\t\t\t\tNselect\t\t\t\t\tDifference(%)"

        for bin in ykeys:#yieldDict:

            (nAnti, nAntiErr,nSel, nSelErr, nPred, nPredErr) = yieldDict[bin]

            if nSel != 0:
                diff = abs(nSel-nPred)/(nSel)*100
            else:
                diff = 0

            if diff == 0:
                print "%s:\t%f\t+/-\t%f\t%f\t+/-\t%f\t%f\t+/-\t%f\t%f" % ( bin, nAnti, nAntiErr, nPred, nPredErr, nSel, nSelErr, diff)

        print 80*'#'
        print "Yields with non-zero selected"
        print "Bin:\t\tNanti\t\t\t\t\tNpredict\t\t\t\tNselect\t\t\t\t\tDifference(%)"
        for bin in ykeys:#yieldDict:

            (nAnti, nAntiErr,nSel, nSelErr, nPred, nPredErr) = yieldDict[bin]

            if nSel != 0:
                diff = abs(nSel-nPred)/(nSel)*100
            else:
                diff = 0

            if diff != 0:
                print "%s:\t%f\t+/-\t%f\t%f\t+/-\t%f\t%f\t+/-\t%f\t%f" % ( bin, nAnti, nAntiErr, nPred, nPredErr, nSel, nSelErr, diff)

    elif format == "latex":

        print 80*'#'
        print 'Going to print out LaTeX tables'
        print 80*'#'

        nColumns = 7

        begtab = "\\begin{table}[!hbtp]"
        begcent = "\\begin{center}"
        endtab = "\\label{tab:qcdYieldsHTbin}\n\\end{table}"
        endcent = "\\end{center}"

        header = "\\begin{tabular}{|"+nColumns*'c|'+"}"
        hline = "\\hline"
        #header = "\\begin{tabular}{|c||c|c||c|c||c|c|}"
        footer = "\end{tabular}"

        caption = "\\caption{HTbin}"
        njheader = "\multicolumn{7}{|c|}{NJ}\\\\ "+hline
        nbheader = " & \multicolumn{2}{|c|}{\\nbtag = 1} & \multicolumn{2}{|c|}{\\nbtag = 2} & \multicolumn{2}{|c|}{\\nbtag $\\geq$ 3}\\\\ "+hline
        binheader = "\\ST & Predicted & $N_\\textrm{QCD}^\\textrm{selected}$ & Predicted & $N_\\textrm{QCD}^\\textrm{selected}$ & Predicted & $N_\\textrm{QCD}^\\textrm{selected}$ \\\\ "+hline

        for htbin in ['HT0','HT1','HT2']:

            print '%', 10*'-', htbin, 10*'-'

            print begtab
            print caption.replace('HTbin',htbin)
            print begcent
            print header
            print hline, hline
            # filter keys
            ykHT = [key for key in ykeys if htbin in key]

            for njbin in ['45j', '68j']:
                ykNJ = [key for key in ykHT if njbin in key]

                print '%', 10*'-', njbin, 10*'-'
                print njheader.replace('NJ',njbin)
                print nbheader
                print binheader

                for stbin in ['ST1','ST2','ST3','ST4']:
                    ykST = [key for key in ykNJ if stbin in key]

                    print stbin,

                    for nbbin in ['1B','2B','3p']:
                        ykNB = [key for key in ykST if nbbin in key]
                        for bin in ykNB:
                            (nAnti, nAntiErr,nSel, nSelErr, nPred, nPredErr) = yieldDict[bin]


                            print "& %5.1f$\pm$%5.1f & %5.1f$\pm$%5.1f" % ( nPred, nPredErr, nSel, nSelErr),
                    print " \\\\"
                print hline
            print footer
            print endcent
            print endtab.replace('HTbin',htbin)
            print
    else:
        print 'Unknown print format!'

    return 1

# MAIN
if __name__ == "__main__":

    nJobs = 12

    # read f-ratios
    ratDict = {}
    ratDict = readRatios()

    ## usage: python read.py cardDir textformat

    if len(sys.argv) > 1:
        cardDirectory = sys.argv[1]
    else:
        cardDirectory="yields/QCD_yields_3fb_test3"

    if len(sys.argv) > 2:
        pfmt = sys.argv[2]
    else:
        pfmt = "text"


    cardDirectory = os.path.abspath(cardDirectory)
    cardDirName = os.path.basename(cardDirectory)

    print 'Using cards from', cardDirName

    QCDdir = 'common'
    cardPattern = 'QCDyield'

    limitdict = {}
    sigdict = {}


    #print 80*'#'
    #print "Yields for", QCDdir

    # get card file list
    inDir = cardDirectory+'/'+QCDdir
    cardFnames = glob.glob(inDir+'/'+ cardPattern + '_*.root')
    cardNames = [os.path.basename(name) for name in cardFnames]
    cardNames = [(name.replace(cardPattern+'_','')).replace('.input.root','') for name in cardNames]

    #print 'Card list', cardNames
    argTuple = [(QCDdir, cardDirectory,name, ratDict) for name in cardNames]
    #print 'Card list', argTuple

    yieldDict = {}

    # single jobs
    #for args in argTuple:
    #    _getYieldsFromInput(args)
    #    yieldDict[args[0]] = (val,err)

    # multi thread
    pool = Pool(nJobs)
    yieldDict = dict(pool.map(_getYieldsFromInput, argTuple))

    # Output yields
    makeTable(yieldDict,pfmt)
