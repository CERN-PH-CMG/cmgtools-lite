#!/usr/bin/env python
import sys
from math import *
from ROOT import *

def getPUratio(fdata, fmc, hname = "puRatio"):

    hData = fdata.Get("pileup")
    hMC = fmc.Get("pileup")

    # normalise if not already
    if hData.Integral() != 1:
        print "##Normalising data histo!"
        hData.Scale(1/hData.Integral())
    if hMC.Integral() != 1:
        print "##Normalising MC histo!"
        hMC.Scale(1/hMC.Integral())

    # choose maximum NbinsX
    nXdata = hData.GetNbinsX()
    nXmc = hMC.GetNbinsX()

    maxX = nXdata if nXdata > nXmc else nXmc

    #hRatio = TH1F(hname,"PU Data/MC ratio",maxX,-0.5,maxX+0.5)
    hRatio = TH1F(hname,"PU Data/MC ratio",nXdata,-0.5,nXdata+0.5)

    for i in range(1,nXdata):
        # ratio
        nData = hData.GetBinContent(i)
        nDataErr = 0#hData.GetBinError(i)

        nMC = hMC.GetBinContent(i) if i <= nXmc else 0
        nMCerr = 0#hMC.GetBinError(i) if i <= nXmc else 0

        if nMC > 0:
            rat = nData/nMC
            err = 0#rat*hypot(nDataErr/nData,nMCerr/nMC)
        else:
            rat = 0
            err = 0

        hRatio.SetBinContent(i,rat)
        hRatio.SetBinError(i,err)

    return hRatio

if __name__ == "__main__":

    '''
    if '-b' in sys.argv:
        sys.argv.remove('-b')
        _batchMode = True
    '''

    if len(sys.argv) > 2:
        dataFname = sys.argv[1]
        mcFname = sys.argv[2]

        print '## data file:', dataFname
        print '## mc   file:', mcFname

    else:
        print "## Usage:"
        print "./makePUweightHisto.py dataPUfile.root mcPUfile.root"
        exit(0)

    fdata  = TFile(dataFname, "READ")
    fmc  = TFile(mcFname, "READ")
    fout  = TFile("pu_ratio.root", "RECREATE")

    if not fdata or not fmc:
        print "Couldn't open the file(s)"
        exit(0)

    hRatio = getPUratio(fdata,fmc)
    hRatio.Write()

    fdata.Close()
    fmc.Close()
    fout.Close()

    print 'Finished'
