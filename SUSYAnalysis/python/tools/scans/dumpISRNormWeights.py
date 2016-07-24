#!/usr/bin/env python
import sys,os

from math import *
from ROOT import *

SMS = "T1tttt"

def dumpCounts(fname,cname = "counts.txt"):

    cname = "ISRnormWeights"+SMS+".txt"
    tfile = TFile(fname,"READ")

    # Content should be
    '''
    KEY: TH1DCount;1Count -- total counts in file
    KEY: TH3DCountSMS;1CountSMS -- counts per mass point
    KEY: TH1DCountLHE;1CountLHE -- some LHE info (weights?)
    KEY: TH1DSumGenWeights;1SumGenWeights -- total gen weight sum per file
    KEY: TH3DSumGenWeightsSMS;1SumGenWeightsSMS -- gen weight sum per mass point
    '''
    #should be 2D
    hCountSMS = tfile.Get("SMSscan_"+SMS+"_Scan")
    hISRweight = tfile.Get("SMSscan_"+SMS+"_Scan_nISRweight")
    hISRweight_up = tfile.Get("SMSscan_"+SMS+"_Scan_nISRweight_up")
    hISRweight_down = tfile.Get("SMSscan_"+SMS+"_Scan_nISRweight_down")
    print "Total entries %i" % hCountSMS.GetEntries()
    #print hCountSMS.GetEntries()


    cntDict = {}

    # round up to 5
    base = 5

    for xbin in range(1,hCountSMS.GetNbinsX()+1):
        for ybin in range(1,hCountSMS.GetNbinsY()+1):

            cnt = hCountSMS.GetBinContent(xbin,ybin)
            if cnt < 1: continue



            mGo = hCountSMS.GetXaxis().GetBinCenter(xbin)
            #mGo = hCountSMS.GetXaxis().GetBinLowEdge(xbin)
            mLSP = hCountSMS.GetYaxis().GetBinCenter(ybin)
            #mLSP = hCountSMS.GetYaxis().GetBinLowEdge(ybin)

            # round up to base (5)
            mGo = int(base * round(mGo/base))
            mLSP = int(base * round(mLSP/base))
            
            ISRweight = cnt/hISRweight.GetBinContent(xbin,ybin)
            ISRweight_up = cnt/hISRweight_up.GetBinContent(xbin,ybin)
            ISRweight_down = cnt/hISRweight_down.GetBinContent(xbin,ybin)
            print "Found %f %f %f weights and %i  counts for mass point %i,%i" %(ISRweight, ISRweight_up, ISRweight_down,cnt, mGo,mLSP)
            cntDict[(mGo,mLSP)] = (cnt, ISRweight, ISRweight_up, ISRweight_down)

    #print cntDict
    #exit(0)

    # write file
    with open(cname,"a") as cfile:

        cfile.write("#mGo\tmLSP\ISRweight\ISRweight_up\ISRweight_down\n")

        for point in cntDict:

            #write only count for each point
            #line = "%i\t%i\t%i\n" %(point[0],point[1],cntDict[point])

            # write count, weight and total for each point
            #line = "%i\t%i\t%i\t%i\t%.3f\n" %(point[0],point[1],totalEvts,cntDict[point][0],cntDict[point][1])
            line = "%i\t%i\t%f\t%f\t%f\n" %(point[0],point[1],cntDict[point][1],cntDict[point][2],cntDict[point][3])

            cfile.write(line)

    #raw_input("exit")

    tfile.Close()

def dumpFiles(fileList):

    cname = "ISRnormWeights"+SMS+".txt"

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
