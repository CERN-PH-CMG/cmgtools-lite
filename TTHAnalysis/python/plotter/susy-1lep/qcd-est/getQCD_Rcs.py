#!/usr/bin/env python

import shutil
import subprocess
import os
import sys
import glob
from multiprocessing import Pool
from ROOT import *

nameDict = {}

# ST bin names
nameDict['ST0'] = "[200,250]"
nameDict['ST1'] = "[250,350]"
nameDict['ST2'] = "[350,450]"
nameDict['ST3'] = "[450,600]"
nameDict['ST4'] = ">600"

'''
# HT bin names
nameDict['HT0'] = "500 < \\HT < 750"
nameDict['HT1'] = "750 < \\HT < 1250"
nameDict['HT2'] = "\\HT > 1250"

# Nj bins
nameDict['34'] = "\\njet = 3,5"
nameDict['45'] = "\\njet = 4,5"
nameDict['68'] = "\\njet = 6-8"
'''

_histStore = []

def makeRCSplots(rcsDict):

    canvList = []

    rkeys = sorted(rcsDict.keys())

    for njbin in ['68', '45']:
        rkNJ = [key for key in rkeys if njbin in key]

        cname = rkNJ[0]
        print 'creating canvas', cname
        canv=TCanvas(cname,cname,800,600)
        drawOpt = ''


        for nbbin in ['Nb1', 'Nb2','Nb3']:
            rkNB = [key for key in rkNJ if nbbin in key]

            ## make histo
            hname = rkNB[0]
            print 'creating hist', hname
            #hname = hname[:hname.find('_Nb')]
            #hname = hname.replace('ST','')

            STlist = ['ST1','ST2','ST3','ST4']
            nbins = len(STlist)

            hist = TH1F('h'+hname,'R_{CS} for '+hname,nbins,0.5,nbins+0.5)

            rkST = []
            for stbin in STlist:
                rkST += [key for key in rkNB if stbin in key]

            print rkST

            for i,bin in enumerate(rkST):

                print bin, i

                hist.SetBinContent(i+1, rcsDict[bin][0])
                hist.SetBinError(i+1, rcsDict[bin][1])

                for key in nameDict.keys():
                    if key in bin:
                        print 'Real name', nameDict[key]
                        hist.GetXaxis().SetBinLabel(i+1, nameDict[key])

                print rcsDict[bin]

            _histStore.append(hist)
            #hist.Draw('e1'+drawOpt)
            if drawOpt == '': drawOpt = 'same'

            #gPad.Update()
            #a = raw_input('aa')

        #exit(0)

    return canvList

def calcRcs(hd):

    rCSdict = {}

    for hname in sorted(hd.keys()):

        hist = hd[hname]

        binname = hname.replace('dPhi_','').replace('QCD','')

        if hist.GetNbinsX() == 2:
            nCR = hist.GetBinContent(1)
            nCRerr = hist.GetBinError(1)
            nSR = hist.GetBinContent(2)
            nSRerr = hist.GetBinError(2)
            rCS = 0
            rCSerr = 0

            if nCR != 0:
                rCS = nSR/nCR

                if nSR != 0:
                    rCSerr = rCS * sqrt(nCRerr/nCR*nCRerr/nCR +  nSRerr/nSR*nSRerr/nSR)

            if True:
                print "%s\t%6.2f\t%6.2f\t%6.2f\t%6.2f\t" %(binname, nCR, nSR, rCS, rCSerr)

            rCSdict[binname] = (rCS,rCSerr)

    return rCSdict

def getHistList(tfile):

    hd = {}
    ## make dict of histos
    for key in tfile.GetListOfKeys():
        obj = key.ReadObj()

        if 'TH1' in obj.ClassName():
            ## filter
            if 'background' in obj.GetName(): continue
            if 'incl' in obj.GetName(): continue

            hd[obj.GetName()] = obj.Clone()

    return hd

# MAIN
if __name__ == "__main__":

    if len(sys.argv) > 1:
        plotfName = sys.argv[1]
    else:
        plotfName = "../../www_plots/Lumi3fb/QCD/dPhi_Nb1p_Rcs/dphi_dynCut_STbin_Rcs.root"

    print "Going to calculate Rcs values from file", plotfName

    tfile = TFile(plotfName,"READ")

    histDict = getHistList(tfile)
    #print sorted(histDict.keys())
    rcsDict = calcRcs(histDict)
    makeRCSplots(rcsDict)

    plfile = TFile("rCSplots.root","RECREATE")

    for hist in _histStore:
        print hist
        hist.Write()

    plfile.Close()
    tfile.Close()
    print 'Done'
