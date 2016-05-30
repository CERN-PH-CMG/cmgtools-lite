#!/usr/bin/env python
#import re, sys, os, os.path

import glob, os, sys
from math import hypot, sqrt
from ROOT import *

from readYields import getYield

def getSamples(fname,tdir):

    tfile = TFile(fname,"READ")
    tfile.cd(tdir)

    samples = []

    for key in gDirectory.GetListOfKeys():

        obj = key.ReadObj()
        if "TH" in obj.ClassName():
            samples.append(obj.GetName())

    tfile.Close()

    return samples

def getRcsHist(tfile, hname, band = "SB", merge = True):

    hSR = tfile.Get("SR_"+band+"/"+hname)
    hCR = tfile.Get("CR_"+band+"/"+hname)

    hRcs = hSR.Clone(hSR.GetName().replace('x_','Rcs_'))
    hRcs.Divide(hCR)

    hRcs.GetYaxis().SetTitle("Rcs")

    # merge means ele/mu values are overwritten by the combined Rcs
    if 'data' in hname: merge = True

    if merge:
        rcs = hRcs.GetBinContent(2,2); err = hRcs.GetBinError(2,2) # lep sele

        hRcs.SetBinContent(1,2,rcs); hRcs.SetBinError(1,2,err) # mu sele
        hRcs.SetBinContent(3,2,rcs); hRcs.SetBinError(3,2,err) # ele sele

    return hRcs

def getPredHist(tfile, hname):

    hRcsMB = tfile.Get("Rcs_SB/"+hname)

    if ('data' in hname) or ("background" in hname) or ("poisson" in hname):
        # use EWK template
        hKappa = tfile.Get("Kappa/EWK")
        if not hKappa: hKappa = tfile.Get("Kappa/"+hname)
    else:
        hKappa = tfile.Get("Kappa/"+hname)

    # get yield from CR of MB
    hCR_MB = tfile.Get("CR_MB/"+hname)

    hPred = hCR_MB.Clone(hCR_MB.GetName())#+"_pred")
    #hPred.SetTitle("Predicted yield")

    hPred.Multiply(hRcsMB)
    hPred.Multiply(hKappa)

    return hPred

def readQCDratios(fname = "lp_LTbins_NJ34_f-ratios_MC.txt"):

    fDict = {}

    with open(fname) as ftxt:
        lines = ftxt.readlines()

        for line in lines:
            if line[0] != '#':
                (bin,rat,err) = line.split()
                bin = bin.replace("_NJ34","")
                if 'LT' in bin:
                    fDict[bin] = (float(rat),float(err))

    #print 'Loaded f-ratios from file', fname
    #print fDict

    return fDict

def getPoissonHist(tfile, sample = "background", band = "CR_MB"):
    # sets all bin errors to sqrt(N)

    hist = tfile.Get(band+"/"+sample).Clone(sample+"_poisson")

    if "TH" not in hist.ClassName(): return 0

    for ix in range(1,hist.GetNbinsX()+1):
        for iy in range(1,hist.GetNbinsY()+1):
            hist.SetBinError(ix,iy,sqrt(hist.GetBinContent(ix,iy)))

    return hist


# Systematic error on F-ratio
qcdSysts = {
    ('NJ45','HT0') : 0.25,
    ('NJ45','HT1') : 0.25,
    ('NJ45','HT2i') : 0.5,
    ('NJ68','HT0') : 0.25,
    ('NJ68','HT1') : 0.25,
    ('NJ68','HT2i') : 0.5,
    ('NJ9','HT01') : 0.75,
    ('NJ9','HT2i') : 0.75,
    #    ('NB2','NB2') : 1.0,
    #    ('NB3','NB3') : 1.0,
    }

def getQCDsystError(binname):

    # Set 100% syst if NB >= 2
    for nbbin in ['NB2','NB3']:
        if nbbin in binname:
            return 1.00

    for njbin,htbin in qcdSysts.keys():
        if njbin in binname and htbin in binname:
            #print binname, njbin, htbin, qcdSysts[(njbin,htbin)]
            return qcdSysts[(njbin,htbin)]
    return 0

def getQCDsubtrHistos(tfile, sample = "background", band = "CR_MB/", isMC = True, applySyst = True, lep = "ele"):
    ## returns two histograms:
    ## 1. QCD prediction from anti-leptons
    ## 2. Original histo - QCD from prediction

    ## Get fRatios for electrons
    fRatio = 0.3 # default
    fRatioErr = 0.01 # default

    fRatios = {}

    if isMC: fRatios = readQCDratios("fRatios_MC_lumi2p1.txt")
    else: fRatios = readQCDratios("fRatios_Data_lumi2p1.txt")

    # read bin name
    binString = tfile.Get(band+"BinName")
    if binString: binName = binString.GetTitle()
    else: binName = tfile.GetName()

    # get bin from filename
    for key in fRatios:
        if key in binName:
            (fRatio,fRatioErr) = fRatios[key]
            #print "Found matching ratios for key" , key
            break
        #else: print "No corresp fRatio found! Using default."

    # get QCD syst error pn F
    if applySyst == True:
        systErr = getQCDsystError(binName)

        #print "Fratio\t%f, old error\t%f, new error\t%f" %(fRatio,fRatioErr,hypot(fRatioErr,systErr*fRatio))
        fRatioErr = hypot(fRatioErr,systErr*fRatio)
        # make sure error not bigger than value itself
        fRatioErr = min(fRatioErr,fRatio)

    ## fRatios for muons
    fRatioMu = 0.1; fRatioMuErr = 1.00 * fRatioMu

    ############################
    # Get original histo
    hOrig = tfile.Get(band+sample) # original histogram
    if not hOrig: return 0

    ## 1. QCD prediction
    hQCDpred = hOrig.Clone(sample+"_QCDpred")
    hQCDpred.Reset() # reset counts/errors

    if lep == "ele" :
        # take anti-selected ele yields
        yAnti = hOrig.GetBinContent(3,1); yAntiErr = hOrig.GetBinError(3,1);

        # apply f-ratio
        yQCDFromAnti = fRatio*yAnti
        yQCDFromAntiErr = hypot(yAntiErr*fRatio,yAnti*fRatioErr)
        # make sure error is not bigger than value
        yQCDFromAntiErr = min(yQCDFromAntiErr, yQCDFromAnti)

        # set bin content for ele
        hQCDpred.SetBinContent(3,2,yQCDFromAnti)
        hQCDpred.SetBinError(3,2,yQCDFromAntiErr)

        # set bin content for lep (=ele)
        hQCDpred.SetBinContent(2,2,yQCDFromAnti)
        hQCDpred.SetBinError(2,2,yQCDFromAntiErr)
    elif lep == "lep":

        ## Electrons
        # take anti-selected ele yields
        yAntiEle = hOrig.GetBinContent(3,1); yAntiEleErr = hOrig.GetBinError(3,1);

        # apply f-ratio
        yQCDFromAntiEle = fRatio*yAntiEle
        yQCDFromAntiEleErr = hypot(yAntiEleErr*fRatio,yAntiEle*fRatioErr)
        # make sure error is not bigger than value
        yQCDFromAntiEleErr = min(yQCDFromAntiEleErr, yQCDFromAntiEle)

        # set bin content for ele
        hQCDpred.SetBinContent(3,2,yQCDFromAntiEle)
        hQCDpred.SetBinError(3,2,yQCDFromAntiEleErr)

        ## Muons
        # take anti-selected mu yields
        yAntiMu = hOrig.GetBinContent(1,1); yAntiMuErr = hOrig.GetBinError(1,1);

        # apply f-ratio
        yQCDFromAntiMu = fRatioMu*yAntiMu
        yQCDFromAntiMuErr = hypot(yAntiMuErr*fRatioMu,yAntiMu*fRatioMuErr)
        # make sure error is not bigger than value
        yQCDFromAntiMuErr = min(yQCDFromAntiMuErr, yQCDFromAntiMu)

        # set bin content for mu
        hQCDpred.SetBinContent(1,2,yQCDFromAntiMu)
        hQCDpred.SetBinError(1,2,yQCDFromAntiMuErr)

        # set bin content for lep (=mu+ele)
        yQCDFromAntiLep = yQCDFromAntiEle + yQCDFromAntiMu
        yQCDFromAntiLepErr = hypot(yQCDFromAntiEleErr,yQCDFromAntiMuErr)
        yQCDFromAntiLepErr = min(yQCDFromAntiLepErr,yQCDFromAntiLep)

        hQCDpred.SetBinContent(2,2,yQCDFromAntiLep)
        hQCDpred.SetBinError(2,2,yQCDFromAntiLepErr)
    elif lep == "mu":
        ## Muons
        # take anti-selected mu yields
        yAntiMu = hOrig.GetBinContent(1,1); yAntiMuErr = hOrig.GetBinError(1,1);

        # apply f-ratio
        yQCDFromAntiMu = fRatioMu*yAntiMu
        yQCDFromAntiMuErr = hypot(yAntiMuErr*fRatioMu,yAntiMu*fRatioMuErr)
        # make sure error is not bigger than value
        yQCDFromAntiMuErr = min(yQCDFromAntiMuErr, yQCDFromAntiMu)

        # set bin content for mu
        hQCDpred.SetBinContent(1,2,yQCDFromAntiMu)
        hQCDpred.SetBinError(1,2,yQCDFromAntiMuErr)

        # set bin content for lep (=ele)
        hQCDpred.SetBinContent(2,2,yQCDFromAntiMu)
        hQCDpred.SetBinError(2,2,yQCDFromAntiMuErr)
    else:
        print "QCD estimate not yet implemented for", lep
        return 0

    ############################
    ## 2. histo with QCD subtracted
    hQCDsubtr = hOrig.Clone(sample+"_QCDsubtr")

    # do QCD subtraction only in Control Region
    if 'CR' in band:
        # subtract prediction from histo
        hQCDsubtr.Add(hQCDpred,-1)

    return (hQCDpred,hQCDsubtr)

def replaceEmptyDataBinsWithMC(fileList):
    # hists to make QCD estimation
    bindirs =  ['CR_MB','SR_SB','CR_SB']
    print ''
    print "Replacing empty data bins with MC for CR_MB, SR_SB, CR_SB, 100% error"
    for fname in fileList:
        tfile = TFile(fname,"UPDATE")
        if 1==1:
            for bindir in bindirs:
                histData = tfile.Get(bindir+"/data").Clone()
                histBkg = tfile.Get(bindir+"/background").Clone()

                #if "TH" not in histData.ClassName() or 'TH' in histBkg.ClassName(): return 0

                ix = 2
                iy = 2
                if histData.GetBinContent(ix, iy) == 0:
                    print '!!! ATTENTION: replacing', fname, bindir, "bin number", ix, iy, "data", histData.GetBinContent(ix, iy), "with MC", histBkg.GetBinContent(ix,iy), 'alsp replacing sorrounding bins e, mu sel !!!'
                    histData.SetBinContent(ix, iy, histBkg.GetBinContent(ix,iy))
                    histData.SetBinError(ix, iy, histBkg.GetBinContent(ix,iy))
                    histData.SetBinContent(ix+1, iy, histBkg.GetBinContent(ix+1,iy))
                    histData.SetBinError(ix+1, iy, histBkg.GetBinContent(ix+1,iy))
                    histData.SetBinContent(ix-1, iy, histBkg.GetBinContent(ix-1,iy))
                    histData.SetBinError(ix-1, iy, histBkg.GetBinContent(ix-1,iy))

                if histData:
                    tfile.cd(bindir)
                    # overwrite old hist
                    histData.Write("",TObject.kOverwrite)
                tfile.cd()
        tfile.Close()
    print ''

def makeQCDsubtraction(fileList, samples):
    # hists to make QCD estimation
    bindirs =  ['SR_MB','CR_MB','SR_SB','CR_SB']

    print "Making QCD subtraction for", samples

    # Apply systematic error on F-ratio?
    applySyst = True

    for fname in fileList:
        tfile = TFile(fname,"UPDATE")

        for sample in samples:
            for bindir in bindirs:

                if 'data' in sample: isMC = False
                else: isMC = True

                #hNew = getQCDsubtrHisto(tfile,sample,bindir+"/",isMC)
                ret  = getQCDsubtrHistos(tfile,sample,bindir+"/",isMC, applySyst, "lep")

                if not ret:
                    print 'Could not create new histo for', sample, 'in bin', bindir
                else:
                    (hQCDpred,hQCDsubtr) = ret
                    tfile.cd(bindir)
                    #hNew.Write()
                    hQCDpred.Write()
                    hQCDsubtr.Write()
                tfile.cd()

        tfile.Close()

def makePoissonErrors(fileList, samples = ["background","QCD","EWK"]):
    # hists to make make poisson errors
    print "Making poisson hists for:", samples

    bindirs =  ['SR_MB','CR_MB','SR_SB','CR_SB']

    for fname in fileList:
        tfile = TFile(fname,"UPDATE")

        for sample in samples:
            for bindir in bindirs:

                hist = getPoissonHist(tfile,sample,bindir)

                if hist:
                    tfile.cd(bindir)
                    # overwrite old hist
                    hist.Write()#"",TObject.kOverwrite)
                tfile.cd()

        tfile.Close()

def makeKappaHists(fileList, samples = []):

    # get process names from file if not given
    if samples == []: samples = getSamples(fileList[0],'SR_MB')

    print "Making Rcs and Kappa hists for:", samples

    bindirs =  ['SR_MB','CR_MB','SR_SB','CR_SB']
    #print bindirs

    for fname in fileList:
        tfile = TFile(fname,"UPDATE")

        #getQCDpred(tfile, 'MB')

        # create Rcs/Kappa dir struct
        if not tfile.GetDirectory("Rcs_MB"):
            tfile.mkdir("Rcs_MB")
            tfile.mkdir("Rcs_SB")
            tfile.mkdir("Kappa")

            # store SB/MB names
            sbname = tfile.Get("SR_SB/BinName")
            if sbname:
                #print sbname
                sbname.SetName("SBname")
                tfile.cd("Kappa")
                sbname.Write()

            mbname = tfile.Get("SR_MB/BinName")
            if mbname:
                mbname.SetName("MBname")
                tfile.cd("Kappa")
                mbname.Write()

            for sample in samples:

                hRcsMB = getRcsHist(tfile, sample, 'MB')
                hRcsSB = getRcsHist(tfile, sample, 'SB')

                # make kappa
                hKappa = hRcsMB.Clone(hRcsMB.GetName().replace('Rcs','Kappa'))
                hKappa.Divide(hRcsSB)

                hKappa.GetYaxis().SetTitle("Kappa")

                tfile.cd("Rcs_MB")
                hRcsMB.Write()

                tfile.cd("Rcs_SB")
                hRcsSB.Write()

                tfile.cd("Kappa")
                hKappa.Write()

        else:
            pass
            #print 'Already found Rcs and Kappa'

        '''
        yList = []
        print 'Yields for', sample
        for bindir in bindirs:
        yList.append(getYield(tfile,sample,bindir))

        print yList
        '''

        tfile.Close()

    return 1

def makePredictHists(fileList, samples = []):

    # get process names from file
    if samples == []: samples = getSamples(fileList[0],'SR_MB')

    print "Making predictions for", samples

    for fname in fileList:
        tfile = TFile(fname,"UPDATE")

        # create Rcs/Kappa dir struct
        if not tfile.GetDirectory("SR_MB_predict"):
            tfile.mkdir("SR_MB_predict")
            binString = tfile.Get("SR_MB/BinName").Clone()
            if binString: binName = binString.GetTitle()
            else: binName = tfile.GetName()
            #print binString
            tfile.cd("SR_MB_predict")
            binString.Write()
            for sample in samples:

                hPredict = getPredHist(tfile,sample)

                if hPredict:
                    tfile.cd("SR_MB_predict")
                    hPredict.Write()
                    #print "Wrote prediction of", sample

                else:
                    print "Failed to make prediction for", sample
        else:
            pass

        tfile.Close()

    return 1

def makeClosureHists(fileList, samples = []):
    if samples == []: samples = getSamples(fileList[0],'SR_MB')

    print "Making closure hists for", samples

    bindirs =  ['SR_MB','CR_MB','SR_SB','CR_SB']

    for fname in fileList:
        tfile = TFile(fname,"UPDATE")

        # create Closure dir
        if not tfile.GetDirectory("Closure"):
            tfile.mkdir("Closure")

        for sample in samples:

            hPred = tfile.Get("SR_MB_predict/"+sample)#+"_pred")
            hObs = tfile.Get("SR_MB/"+sample)

            hDiff = hObs.Clone(hObs.GetName())#+"_diff")
            hDiff.Add(hPred,-1)

            #hDiff.GetYaxis().SetTitle("Observed - Predicted/Observed")
            hDiff.Divide(hObs)

            tfile.cd("Closure")
            hDiff.Write()

        tfile.Close()

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


    # append / if pattern is a dir
    if os.path.isdir(pattern): pattern += "/"

    # find files matching pattern
    fileList = glob.glob(pattern+"*merge.root")

    if len(fileList) < 1:
        print "Empty file list"
        exit(0)

    ##################
    # Sample names
    ##################
    # all sample names
    allSamps = getSamples(fileList[0],'SR_MB')
    print 'Found these samples:', allSamps

    # make poisson errors for
    poisSamps = []#"background","QCD","EWK"]
    poisSamps = [s for s in poisSamps if s in allSamps]
    # do qcd prediciton for:

    qcdPredSamps =  ["background","data","QCD","background_poisson","QCD_poisson"]
    #qcdPredSamps =  ["background","QCD","background_poisson","QCD_poisson"]
    qcdPredSamps = [s for s in qcdPredSamps if s in allSamps]
    # samples to make full prediciton
    predSamps = allSamps + ["background_poisson","QCD_poisson"]
    predSaps = [s for s in predSamps if s in allSamps]

    replaceEmptyDataBinsWithMC(fileList)

    makePoissonErrors(fileList, poisSamps)
    makeQCDsubtraction(fileList, qcdPredSamps)
    makeKappaHists(fileList)#, predSamps)
    makePredictHists(fileList)#, predSamps)
    #makeClosureHists(fileList, predSamps)

    print 'Finished'
