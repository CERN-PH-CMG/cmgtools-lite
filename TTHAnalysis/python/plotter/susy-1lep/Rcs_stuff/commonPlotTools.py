#!/usr/bin/python

import sys
import os
#sys.argv.append( '-b' )

from ROOT import *
from array import array

_histListSR = []
_histListCR = []
_histListRcs = []

_canvStore = []
_histStore = []

def setColors(histList):

    colorList = [1,2,4,7,3,6,8,9] + range(10,50)

    histNj45 = [hist for hist in histList if 'NJ45' in hist.GetName()]

    for ind,hist in enumerate(histNj45):

        hist.SetLineColor(colorList[ind])
        hist.SetMarkerColor(colorList[ind])

    histRest = [hist for hist in histList if 'NJ45' not in hist.GetName()]

    for ind,hist in enumerate(histRest):

        hist.SetLineColor(colorList[ind])
        hist.SetMarkerColor(colorList[ind])
        hist.SetLineStyle(2)

def custHists():
    ## loop over all saved hists
    for hist in _histListCR+_histListSR:

        hname = hist.GetName()
        ## common settings
        hist.SetStats(0)
        hist.SetFillColor(0)
        hist.SetLineWidth(2)
        hist.SetMarkerStyle(0)

        ## rebin
        #hist.Rebin(2)

        htitle = ''
        ## NJ bins
        if 'NJ45'in hname:
            htitle = 'Nj #in [4,5] '
        elif 'NJ6i'in hname:
            htitle = 'Nj #geq 6 '
        elif 'NJ68'in hname:
            htitle = 'Nj #in [6,8] '
        elif 'NJ9i'in hname:
            htitle = 'Nj #geq 9 '

        #if 'NJ' in hname and 'HT' in hname: htitle += '; '

        ## HT bins
        if 'HT500750'in hname:
            htitle += '500 < HT < 750'
        elif 'HT7501000'in hname:
            htitle += '750 < HT < 1000'
        elif 'HT5001000'in hname:
            htitle += '500 < HT < 1000'
        elif 'HT7501250'in hname:
            htitle += '750 < HT < 1250'
        elif 'HT1250'in hname:
            htitle += 'HT > 1250'
        elif 'HT1000'in hname:
            htitle += 'HT > 1000'
        elif 'HT500'in hname:
            htitle += 'HT > 500'
        elif 'HT750'in hname:
            htitle += 'HT > 750'

        hist.SetTitle(htitle)

        print hname, htitle

        setColors(_histListSR)
        setColors(_histListCR)

    return 1

def saveCanvases(tfile, pdir, canvList):

    extList = ['.pdf','.png']
    for canv in _canvStore:

        for ext in extList:
            cname = '/'+samp+'_'+ canv.GetName()+ext
            canv.SaveAs(pdir+cname)

    canv.Write()
