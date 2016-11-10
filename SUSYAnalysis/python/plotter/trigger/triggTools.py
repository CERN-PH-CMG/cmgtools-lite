#!/usr/bin/python

import os
import math
from ROOT import *

#import tdrstyle
#set the tdr style
#tdrstyle.setTDRStyle()

import CMS_lumi
CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "Preliminary"
iPos = 0
if( iPos==0 ): CMS_lumi.relPosX = 0.12

gStyle.SetOptTitle(0)
gStyle.SetOptStat(0)
gStyle.SetPadTopMargin(0.05)
#gStyle.SetOptFit()

gStyle.SetLabelFont(62)
gStyle.SetTitleFont(62)

#gStyle.SetPalette(53)
#gStyle.SetCanvasPreferGL(True)

_colorList = [2,4,8,9,7,3,6] + range(10,50)

eta_bins = []#-2.5,-2.25,-2.,-1.75,]
for ieta in range(-10,11):
    eta_bins += [ieta*2.4/10]

eta_bins_2d = [-2.4,-2,-1.5,-1.,-0.5,0,0.5,1.,1.5,2.,2.4]

#pt_bins = range(0,30,2) + range(30,70,5) + range(70,150,10) + range (150,250,25) + range(250,350,50)
pt_bins = range(0,30,2) + range(30,70,5) + range(70,150,10) + range (150,350,50)
#pt_bins = range(0,30,2) + range(30,70,5) + range(70,100,10)
pt_bins_2d = range(0,80,10) + range(80,150,20) + range (150,350,50)

lt_bins = range(0,100,10) + range(100,200,25) + range(200,400,50) + range(400,900,100) # high stat
#lt_bins = range(0,200,25) + range(200,300,50) + range(300,700,150) # low stat

met_bins = range(0,200,20) + range(200,400,50) + range(400,700,100) # high stat
#met_bins = range(0,200,40) + range(200,400,100) + range(400,700,300) # low stat
#met_bins_2d = range(0,200,25) + range(200,400,100) + range(400,700,200) # high stat
met_bins_2d = range(0,200,25) + range(200,400,100)

#ht_bins = range(0,200,10) + range(200,400,50) + range(400,1000,100) + range(1000,1750,250) # high stat
ht_bins = range(200,400,50) + range(400,1000,100) + range(1000,1750,250) # high stat
#ht_bins = range(0,200,40) + range(200,400,100) + range(400,1000,300) + range(1000,1750,250) # low stat
ht_bins_2d = range(0,200,10) + range(200,400,50) + range(400,1000,100) + range(1000,1750,250) # high stat

def getLogBins(nbinsx,xmin,xmax):
    logxmin = math.log10(xmin)
    logxmax = math.log10(xmax)
    binwidth = (logxmax-logxmin)/nbinsx
    xbins = [ xmin + math.pow(10,logxmin+x*binwidth) for x in range(1,nbinsx+1)]
    xbins.sort(key=int)
    #binc = array('d', xbins)

    return xbins

'''
#pt_bins = getLogBins(30,0.9,1000)
pt_bins = getLogBins(33,0.9,1500)
#lt_bins = getLogBins(20,9,1000)
lt_bins = getLogBins(22,9,3000)
ht_bins = getLogBins(30,30,2000)
'''
#pt_bins_2d = getLogBins(30,0.9,1000)
#met_bins_2d = getLogBins(20,9,1000)

#print ht_bins

def cleanName(line):

    cline = line

    if line == 'JetHT!':
        cline = 'hadronic triggers'

    return cline

def varToLabel(var):

    label = var

    if 'pt' in var:
        label = 'p_{T}(lep)'
    elif 'METNoHF' in var:
        label = 'E_{T}^{miss} (NoHF)'
    elif 'LTNoHF' in var:
        label = 'L_{T}'# (NoHF)'
    elif 'MET' in var:
        label = 'E_{T}^{miss}'
        #label = '#slashE_{T}'
    elif 'T' in var:
        label = var.replace('T','_{T}')
    if 'eta' in var:
        label = '#eta(lep)'

    return label

def getLegend(pos = 'ne'):
    if pos == 'ne':
        leg = TLegend(0.4,0.7,0.9,0.9)
    elif pos == 'log':
        leg = TLegend(0.6,0.8,0.99,0.99)
    elif pos == 'roc':
        leg = TLegend(0.15,0.2,0.7,0.4)
    elif pos == 'fit':
        leg = TLegend(0.15,0.75,0.5,0.9)
    elif pos == 'fit2':
        leg = TLegend(0.15,0.7,0.8,0.9)
    elif pos == '2d':
        leg = TLegend(0.3,0.75,0.85,0.9)

    leg.SetBorderSize(1)
    leg.SetTextFont(62)
    leg.SetTextSize(0.03321678)
    leg.SetLineColor(0)
    leg.SetLineStyle(1)
    leg.SetLineWidth(1)
    leg.SetFillColor(0)
    leg.SetFillStyle(1001)

    return leg

def turnon_func(x, par):

    halfpoint = par[0]
    width = max(par[1],1)
    plateau = par[2]

    #offset = par[3]
    #plateau = 1.0
    offset = 0

    pt = TMath.Max(x[0],0.000001)

    arg = 0
    #print pt, halfpoint, width
    arg = (pt - halfpoint) / (width * TMath.Sqrt(2))

    fitval = offset + plateau * 0.5 * (1 + TMath.Erf(arg))
    #fitval = offset + plateau * TMath.Erfc(arg)

    return fitval

def cutsToString(cutList):

    cutstr = ''

    for i, cut in enumerate(cutList):
        cutstr += cut

        if i != len(cutList)-1: cutstr += ' && '

    return cutstr

def saveCanvases(canvList, pdir = '', extraName = '', _batchMode = True):

    ## save canvases to file
    #extList = ['.png','.pdf','.root','.C']
    extList = ['.png','.pdf']

    prefix = ''
    if extraName != '':
        suffix = '_' + extraName
    else:
        suffix = ''

    ## wait
    if not _batchMode:
        answ = raw_input("'Enter' to proceed (or 'q' to exit): ")
        if 'q' in answ: exit(0)


    cdir = os.path.dirname(pdir + prefix)
    print 'Canvas dir is', cdir

    if not os.path.exists(cdir):
        os.makedirs(cdir)

    cdir += '/'

    # make output file
    outName = cdir + 'plots_'+ extraName +'.root'
    ofile = TFile(outName,'RECREATE')

    for canv in canvList:
        for ext in extList:
            cname = canv.GetName().replace('Lep_pt','LepPt')

            # ignore var distributions for now
            if "Eff" not in cname: continue

            cname = cdir + cname+ suffix + ext
            # remove special symbols
            cname = cname.replace('||','or')
            canv.SaveAs(cname)
        canv.Write()

    '''
    # empty stores for further use
    del _canvStore[:]
    _histStore.clear()
    _hEffStore.clear()
    del _fitrStore[:]
    '''

    ofile.Close()

    return 1

def renameTrig(trigName):

    trigName = trigName.replace('SingleMu','IsoMu27')
    trigName = trigName.replace('Mu50NoIso','Mu50')
    trigName = trigName.replace('ElNoIso','El105')
    trigName = trigName.replace('SingleEl','El32')
    trigName = trigName.replace('HTMET','HT350MET120')

    if trigName == 'IsoMu27||IsoEle32':
        trigName = 'IsoMu27||Ele32'

    if trigName == 'MuHT350MET70||EleHT350MET70':
        trigName = 'Mu || Ele x HT350MET70'

    if trigName == 'Mu50||MuHT350MET70||Ele105||EleHT350MET70':
        trigName = 'Mu+Ele combined'

    if trigName == 'Mu50||MuHT350MET70':
        trigName = 'Mu50 OR MuHT350MET70'

    if trigName == 'Ele105||EleHT350MET70':
        trigName = 'Ele105 OR EleHT350MET70'

    return trigName

