#!/usr/bin/env python
import sys,os

from math import *
from ROOT import *

def dumpCounts(fname,cname = "counts.txt"):

    tfile = TFile(fname,"READ")

    # Content should be
    '''
    KEY: TH1DCount;1Count -- total counts in file
    KEY: TH3DCountSMS;1CountSMS -- counts per mass point
    KEY: TH1DCountLHE;1CountLHE -- some LHE info (weights?)
    KEY: TH1DSumGenWeights;1SumGenWeights -- total gen weight sum per file
    KEY: TH3DSumGenWeightsSMS;1SumGenWeightsSMS -- gen weight sum per mass point
    '''

    hCount = tfile.Get("Count") # should be 1D
    hCountSMS = tfile.Get("CountSMS").Project3D("yx") # should be 2D

    print "Total entries %i" % hCount.GetEntries()
    #print hCountSMS.GetEntries()

    hWeight = tfile.Get("SumGenWeights") # should be 1D
    hWeightSMS = tfile.Get("SumGenWeightsSMS").Project3D("yx") # should be 1D

    totCnt = hCount.GetEntries()
    totW = hWeight.GetEntries()

    cntDict = {}

    # round up to 5
    base = 5

    for xbin in range(1,hCountSMS.GetNbinsX()+1):
        for ybin in range(1,hCountSMS.GetNbinsY()+1):

            cnt = hCountSMS.GetBinContent(xbin,ybin)
            if cnt < 1: continue

            wgt = hWeightSMS.GetBinContent(xbin,ybin)

            mGo = hCountSMS.GetXaxis().GetBinCenter(xbin)
            #mGo = hCountSMS.GetXaxis().GetBinLowEdge(xbin)
            mLSP = hCountSMS.GetYaxis().GetBinCenter(ybin)
            #mLSP = hCountSMS.GetYaxis().GetBinLowEdge(ybin)

            # round up to base (5)
            mGo = int(base * round(mGo/base))
            mLSP = int(base * round(mLSP/base))

            #print "Found %i entries for mass point %i,%i" %(cnt, mGo,mLSP)
            cntDict[(mGo,mLSP)] = (cnt,wgt)

    #print cntDict
    #exit(0)

    # write file
    with open(cname,"a") as cfile:

        #cfile.write("Total\t" + str(totalEvts) + "\n")
        cfile.write("#mGo\tmLSP\tTotal\tTotGenW\tCountsSMS\tGenWeightSMS\n")

        for point in cntDict:

            #write only count for each point
            #line = "%i\t%i\t%i\n" %(point[0],point[1],cntDict[point])

            # write count, weight and total for each point
            #line = "%i\t%i\t%i\t%i\t%.3f\n" %(point[0],point[1],totalEvts,cntDict[point][0],cntDict[point][1])
            line = "%i\t%i\t%i\t%.3f\t%i\t%.3f\n" %(point[0],point[1],totCnt,totW,cntDict[point][0],cntDict[point][1])

            cfile.write(line)

    #raw_input("exit")

    tfile.Close()

def dumpFiles(fileList):

    cname = "counts.txt"

    # overwrite file
    cf = open(cname,"w"); cf.close()

    for i,fname in enumerate(fileList):
        mass = fname

        parts = fname.split("/")
        for part in parts:
            if "mGo" in part and "mLSP" in part: mass = part

        #print "Counts for", os.path.basename(fname)
        print "Counts for", mass, "[%i/%i]" %(i+1,len(fileList))
        dumpCounts(fname,cname)
        print 80 *"-"

if __name__ == "__main__":

    if '-b' in sys.argv:
        sys.argv.remove('-b')

    if len(sys.argv) > 1:
        fileName = sys.argv[1:]
        #print '#fileName is', fileName
    else:
        print '#No file names given'
        exit(0)

    if len(fileName) == 1:
        dumpCounts(fileName[0])
    else:
        dumpFiles(fileName)

    print 'Finished'
