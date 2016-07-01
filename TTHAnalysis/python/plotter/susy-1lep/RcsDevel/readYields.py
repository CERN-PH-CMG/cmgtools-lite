#!/usr/bin/env python
#import re, sys, os, os.path

import glob, os, sys
from math import hypot,sqrt
from ROOT import *

#########################
### For yieldClass
#########################

# round up masses to base (5)
base = 5

def getLepYield(hist,leptype = ('lep','sele')):
    if hist.GetNbinsX() == 1:
        return (hist.GetBinContent(1),hist.GetBinError(1))

#    elif hist.GetNbinsX() == 4 and hist.GetNbinsY() == 2:
    
    elif hist.GetNbinsX() <= 5 and hist.GetNbinsY() <= 3:

        if leptype == ('mu','anti'):
            return (hist.GetBinContent(1,1),hist.GetBinError(1,1))
        elif leptype == ('mu','sele'):
            return (hist.GetBinContent(1,2),hist.GetBinError(1,2))
        elif leptype == ('ele','anti'):
            return (hist.GetBinContent(3,1),hist.GetBinError(3,1))
        elif leptype == ('ele','sele'):
            return (hist.GetBinContent(3,2),hist.GetBinError(3,2))
        elif leptype == ('lep','anti'):
            return (hist.GetBinContent(2,1),hist.GetBinError(2,1))
        elif leptype == ('lep','sele'):
            return (hist.GetBinContent(2,2),hist.GetBinError(2,2))
    else:
        print "WARNING: Integrating over all yields... Check getLepYield definition! "
        return (hist.Integral(),sqrt(hist.Integral()))

def getScanYields(hist,leptype = ('lep','sele')):

    ydict = {}

    for xbin in range(1,hist.GetNbinsX()+1):
        for ybin in range(1,hist.GetNbinsY()+1):

            ycnt = hist.GetBinContent(xbin,ybin)

            # skip empty bins for now
            if ycnt == 0: continue

            yerr = hist.GetBinError(xbin,ybin)
            xpar = hist.GetXaxis().GetBinCenter(xbin); #xpar = int(xpar)
            ypar = hist.GetYaxis().GetBinCenter(ybin); #ypar = int(ypar)

            # round up to base (5)
            base = 5
            xpar = int(base * round(xpar/base))
            ypar = int(base * round(ypar/base))

            ydict[(xpar,ypar)] = (ycnt,yerr)

    # filter out lepton yields
    ret = {}

    if leptype[0] == 'lep':
        for point in ydict:
            if point[0] > 0: # sum ele + mu yield
                mupoint = (-point[0],point[1])
                if mupoint in ydict:
                    ycnt = (ydict[point][0] + ydict[mupoint][0], hypot(ydict[point][1], ydict[mupoint][1]))
                else:
                    ycnt = ydict[point]
                if 'syst' in hist.GetName():
                    ycnt = (ycnt[0] / 2.0, ycnt[1] / 2.0)
                ret[point] = ycnt

    elif leptype[0] == 'ele':
        for point in ydict:
            if point[0] > 0: # ele + mu yield
                ycnt = ydict[point]
                ret[point] = ycnt

    elif leptype[0] == 'mu':
        for point in ydict:
            if point[0] < 0: # ele + mu yield
                ycnt = ydict[point]
                ret[(-point[0],point[1])] = ycnt

    #print 'done', ret
    return ret

#########################
### For Old yield disctionaries
#########################

def getYield(tfile, hname = "background",bindir = "", leptype = ('lep','sele')):

    if bindir != '': bindir += "/"

    hist = tfile.Get(bindir+hname)

    if hist.GetNbinsX() == 1:
        return (hist.GetBinContent(1),hist.GetBinError(1))

    elif hist.GetNbinsX() == 5 and hist.GetNbinsY() == 2:

        if leptype == ('mu','anti'):
            return (hist.GetBinContent(1,1),hist.GetBinError(1,1))
        elif leptype == ('mu','sele'):
            return (hist.GetBinContent(1,2),hist.GetBinError(1,2))
        elif leptype == ('ele','anti'):
            return (hist.GetBinContent(3,1),hist.GetBinError(3,1))
        elif leptype == ('ele','sele'):
            return (hist.GetBinContent(3,2),hist.GetBinError(3,2))
        elif leptype == ('lep','anti'):
            return (hist.GetBinContent(2,1),hist.GetBinError(2,1))
        elif leptype == ('lep','sele'):
            return (hist.GetBinContent(2,2),hist.GetBinError(2,2))
    else:
        print "WARNING: Integrating over all yields... Check getYield definition! "
        return (hist.Integral(),TMath.Sqrt(hist.Integral()))

def getScanYieldDict(tfile, hname = "T1tttt_HM_1200_800",bindir = "", leptype = 'lep'):

    ydict = {}

#    print "Cd into", bindir
    #tfile.cd(bindir)
    #print gDirectory.ls()

    if bindir != '': bindir += "/"
#    print bindir+hname
    hist = tfile.Get(bindir+hname)

    #print hist
    #if not hist: return ydict

    for xbin in range(1,hist.GetNbinsX()+1):
        for ybin in range(1,hist.GetNbinsY()+1):

            xpar = hist.GetXaxis().GetBinLowEdge(xbin); xpar = int(xpar)
            ypar = hist.GetYaxis().GetBinLowEdge(ybin); ypar = int(ypar)
            ycnt = hist.GetBinContent(xbin,ybin)
            yerr = hist.GetBinError(xbin,ybin)

            ydict[(xpar,ypar)] = (ycnt,yerr)

    # filter out electron yields
    ret = {}

    if leptype == 'lep':
        for point in ydict:
            if point[0] > 0: # summ ele + mu yield
                mupoint = (-point[0],point[1])
                if mupoint in ydict:
                    #ycnt = ydict[point] + ydict[mupoint] # wrong: it appends tuples
                    ycnt = (ydict[point][0] + ydict[mupoint][0], hypot(ydict[point][1], ydict[mupoint][1]))
                else:
                    ycnt = ydict[point]
                ret[point] = ycnt

    elif leptype == 'ele':
        for point in ydict:
            if point[0] > 0: # ele + mu yield
                ycnt = ydict[point]
                ret[point] = ycnt

    elif leptype == 'mu':
        for point in ydict:
            if point[0] < 0: # ele + mu yield
                ycnt = ydict[point]
                ret[(-point[0],point[1])] = ycnt

    return ret

#########################
### For QCD estimation
#########################


#########################
### Old stuff for testing
#########################

def makeBinHisto(ydict, hname = "hYields"):

    nbins = len(ydict)

    hist = TH1F(hname,"bin yields for "+hname,nbins,-0.5,nbins+0.5)

    binList = [name for (name,yd,yerr) in ydict]

    for idx,bin in enumerate(sorted(binList)):

        #(yd,yerr) = ydict[bin]
        (name,yd,yerr) = ydict[idx]

        hist.SetBinContent(idx+1,yd)
        hist.SetBinError(idx+1,yerr)

        binlabel = bin.replace('_SR','')
        binlabel = binlabel.replace('_CR','')
        binlabel = binlabel.replace('_CR','')
        binlabel = binlabel.replace('_NJ45','')
        binlabel = binlabel.replace('_NJ68','')

        hist.GetXaxis().SetBinLabel(idx+1,binlabel)

    return hist

def getYHisto(fileList, hname, hyname = "background", hdir = "", leptype = ("lep","sele")):

    binDict = {}
    binList = []

    for fname in fileList:
        binname = os.path.basename(fname)
        #binname = binname.replace('.yields.root','')
        binname = binname[:binname.find('.')]

        #makeRCS(binname)

        print 'Bin', binname, #'in file', fname

        tfile = TFile(fname,"READ")
        (yd,yerr) = getYield(tfile,hyname,hdir, leptype)

        print "yield:", yd, "+/-", yerr
        tfile.Close()

        binDict[binname] = (yd,yerr)
        binList.append((binname, yd, yerr))

    return makeBinHisto(binList, hname)

def readGrid(fileList, hyname = "background", hdir = "", leptype = ("lep","sele")):

    for fname in fileList:
        binname = os.path.basename(fname)
        binname = binname[:binname.find('.')]

        print 'Bin', binname, #'in file', fname

        tfile = TFile(fname,"READ")
        (yd,yerr) = getYield(tfile,hyname,hdir, leptype)

        print "yield:", yd, "+/-", yerr
        tfile.Close()

    return 1


def readScan(fileList, hyname = "T1tttt_HM_1200_800", hdir = "", leptype = "lep"):

    for fname in fileList:
        binname = os.path.basename(fname)
        binname = binname[:binname.find('.')]

        print 'Bin', binname, #'in file', fname

        tfile = TFile(fname,"READ")
        ydict =  getScanYieldDict(tfile,hyname,hdir)#, leptype)

        tfile.Close()

        print ydict
        '''
        for point,yd in ydict.iteritems():
            if yd[0] > 0:
                print point, yd

        #binDict[binname] = (yd,yerr)
        #binList.append((binname, yd, yerr))
        '''

    return 1


def makeRCShist(fileList, hname):

    # sort SR/CR files
    srList = [fname for fname in fileList if 'SR' in fname]
    crList = [fname for fname in fileList if 'CR' in fname]

    #print 'SR files:', srList
    #print 'CR files:', crList
    print 'Found %i SR files and %i CR files matching pattern' %(len(srList), len(crList))

    hSR = getYHisto(srList,"hSR"+hname)
    hCR = getYHisto(crList,"hCR"+hname)

    print hSR.GetNbinsX(), hCR.GetNbinsX()

    hRcs = hSR.Clone("hRcs")
    hRcs.Divide(hCR)

    hRcs.Draw("histe")
    a = raw_input("wait")

    return hRcs

def rename(nameList):

    newList = []

    for name in nameList:

        name = name.replace('NJ68','NJ45')
        name = name.replace('NB2_','NB2i_')
        name = name.replace('NB3i_','NB2i_')

        newList.append(name)

    return newList

def makeKappaHists_old(fileList):

    # filter
    #fileList = [fname for fname in fileList if 'NB3' not in fname]

    # split lists
    #nj45List = [fname for fname in fileList if 'NJ45' in fname]
    nj68List = [fname for fname in fileList if 'NJ68' in fname]
    nj45List = rename(nj68List)

    #print len(nj68List)
    #print rename(nj68List)
    #print len(nj45List)
    #print len(nj45List)

    hRcsNj68 = makeRCShist(nj68List,"_Nj68")
    hRcsNj68.SetLineColor(kBlue)
    hRcsNj68.SetMarkerStyle(22)
    hRcsNj68.SetMarkerColor(kBlue)

    hRcsNj45 = makeRCShist(nj45List,"_Nj45")
    hRcsNj45.SetLineColor(kRed)
    hRcsNj45.SetMarkerStyle(22)
    hRcsNj45.SetMarkerColor(kRed)

    hRcsNj68.Draw("histe1")
    hRcsNj45.Draw("histe1same")

    b = raw_input("cont")

    hKappa = hRcsNj68.Clone("hKappa")
    hKappa.Divide(hRcsNj45)
    hKappa.GetYaxis().SetRangeUser(0,2)

    hKappa.Draw("histe1")
    b = raw_input("cont")

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
    fileList = glob.glob(pattern+"*.root")

    #makeKappaHists_old(fileList)

    #hKappa = getYHisto(fileList,"hKappa", "Kappa_background",  "Kappa", ("mu","sele"))
    #hKappa.Draw("histe1")

    # read scan
    #readScan(fileList,"T1tttt_HM_1200_800","SR_MB")
    readGrid(fileList)

    raw_input("cont")

    print 'Finished'
