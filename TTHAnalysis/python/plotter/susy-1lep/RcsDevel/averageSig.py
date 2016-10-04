#!/usr/bin/env python
#import re, sys, os, os.path

from numpy import *
import glob, os, sys, math
from math import hypot
from ROOT import *

from readYields import getYield

def getDirNames(fname):

    tfile = TFile(fname,"READ")

    dirList = [dirKey.ReadObj().GetName() for dirKey in gDirectory.GetListOfKeys() if dirKey.IsFolder() == 1]

    tfile.Close()

    return dirList

def makeSystHists(fileList1, fileList2):

    hnames = ["T1tttt_Scan"] # process name
    bindirs =  ['SR_MB','CR_MB','SR_SB','CR_SB']

    print "Found those dirs:", bindirs
    bindirs = [bin for bin in bindirs if "DL" not in bin]
    print bindirs

    for fname1,fname2 in zip(sort(fileList1),sort(fileList2)):
        tfile1 = TFile(fname1,"UPDATE")
        tfile2 = TFile(fname2,"UPDATE")
        for bindir in bindirs:
            for hname in hnames:
                print bindir+'/'+ hname
                hMet = tfile1.Get(bindir+'/'+ hname)
                hGenMet = tfile2.Get(bindir+'/'+ hname)
                print tfile1.GetName(),tfile2.GetName()
                print hMet, hGenMet
                print hMet.GetName(),hMet.GetTitle()
                hAverage = hMet.Clone()
                hAverage.Add(hGenMet)
                hAverage.Scale(0.5)
                hAverage.SetName("T1tttt_Scan")
                
               
                
                #print hMet.GetBinContent(119,15),hGenMet.GetBinContent(119,15), hAverage.GetBinContent(119,15)

                hSyst = hMet.Clone()
                for binx in range(1,hSyst.GetNbinsX()+1):
                    for biny in range(1,hSyst.GetNbinsY()+1):
                        if hAverage.GetBinContent(binx, biny) > 0: 
                            sys = abs(hMet.GetBinContent(binx, biny) - hAverage.GetBinContent(binx, biny)) / 2.0 / hAverage.GetBinContent(binx, biny)
                        else: sys = 0
                   #     print hAverage.GetBinContent(binx, biny), sys
                        hSyst.SetBinContent(binx,biny,sys)
                hSyst.SetName("T1tttt_Scan_MET_syst")
                tfile1.cd(bindir)
                hSyst.Write("",TObject.kOverwrite)
                tfile1.cd(bindir)
                hAverage.Write("",TObject.kOverwrite)

        tfile1.Close()
        tfile2.Close()


    return 1


if __name__ == "__main__":

    ## remove '-b' option
    _batchMode = False

    if '-b' in sys.argv:
        sys.argv.remove('-b')
        _batchMode = True

    if len(sys.argv) > 1:
        pattern = sys.argv[1]
        print '# pattern is', pattern
    else:
        print "No pattern given!"
        exit(0)

    # find files matching pattern
    fileList1 = glob.glob("Test/NormMet/scan*/merged/*.root")
    fileList2 = glob.glob("Test/NormGenMet/scan*/merged/*.root")

    makeSystHists(fileList1, fileList2)

    print 'Finished'
