#!/usr/bin/python

import sys
import os
#sys.argv.append( '-b' )

from ROOT import *
## STYLE
gStyle.SetOptTitle(0)
gStyle.SetOptStat(0)
gStyle.SetPadTopMargin(0.05)
gStyle.SetPadBottomMargin(0.125)
gStyle.SetPadRightMargin(0.075)
gStyle.SetPadLeftMargin(0.125)

## CMS Lumi
import CMS_lumi

CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "Simulation"
CMS_lumi.lumi_13TeV = "MC"

iPos = 11
if( iPos==0 ): CMS_lumi.relPosX = 0.1

colorList = [1,2,4,7,9,8,3,6] + range(10,50)

_histStore = {}
_canvStore = {}

# do transparent fill?
doTransp = True

def doLegend():

    leg = TLegend(0.65,0.7,0.85,0.9) # right
    #leg = TLegend(0.45,0.7,0.7,0.9) # middle
    #leg = TLegend(0.25,0.2,0.45,0.4) # BL

    leg.SetBorderSize(1)
    leg.SetTextFont(62)
    leg.SetTextSize(0.04)
    leg.SetLineColor(1)
    leg.SetLineStyle(1)
    leg.SetLineWidth(1)
    leg.SetFillStyle(1001)

    if doTransp: leg.SetFillColorAlpha(0,0.8)
    else:leg.SetFillColor(0)

    return leg

def getBinLabel(binname):

    # NB
    binname = binname.replace("NB3i","N_{b} #geq 3")
    binname = binname.replace("NB2i","N_{b} #geq 2")
    binname = binname.replace("NB1i","N_{b} #geq 1")
    binname = binname.replace("NB0i","N_{b} #geq 0")

    binname = binname.replace("NB2","N_{b} = 2")
    binname = binname.replace("NB1","N_{b} = 1")
    binname = binname.replace("NB0","N_{b} = 0")

    # NJ
    binname = binname.replace("NJ34","N_{j} #in [3,4]")
    binname = binname.replace("NJ45","N_{j} #in [4,5]")
    binname = binname.replace("NJ6i","N_{j} #geq 6")

    return binname

def getRatiosPlot(tfile):

    histList = []

    # Get ratio hists from file
    for key in tfile.GetListOfKeys():
        hist = key.ReadObj()

        if 'TH1' in str(type(hist)):
            if '_ratio' in hist.GetName():

                binName = hist.GetName().replace('_ratio','')
                binName = binName[binName.find("_")+1:]

                # filter:
                if binName in ['NB3i','NB1i','NB0i']:
                    continue

                print 'Found', binName

                histList.append((binName,hist))
                #histDict[binName] = hist
                #_histStore[hist.GetName()] = hist

                #hist.Draw(plotOpt)
                #if "same" not in plotOpt: plotOpt += "same"
    # Plot hists
    #_canvStore[canv.GetName()] = canv

    return histList

if __name__ == "__main__":

    if "-b" in sys.argv:
        sys.argv.remove("-b")
        batchMode = True
    else:
        batchMode = False

    if len(sys.argv) > 1:
        infile = sys.argv[1]
        print 'Infile is', infile
    else:
        print 'No file name is given'

    tfile  = TFile(infile, "READ")

    if len(sys.argv) > 2:
        outName = sys.argv[2]
    else:
        print 'No out file name is given'
        outName = os.path.basename(infile).replace(".root","_ratios.root")
        print 'Out file name is', outName

    outdir = os.path.dirname(infile)

    if not os.path.isdir(outdir+"/fRatios"): os.makedirs(outdir+"/fRatios")

    outfile = TFile(outdir+"/fRatios/"+outName, "RECREATE")

    if not tfile:
        print "Couldn't open the file"
        exit(0)

    hList = getRatiosPlot(tfile)

    pname = os.path.basename(tfile.GetName()).replace(".root","")
    canv=TCanvas(pname,"F-ratios for " + pname.replace("_"," "),800,800)

    if doTransp: plotOpt = "e5"
    else:        plotOpt = "pe1"

    leg = doLegend()

    # if you want extra text:
    if 'NJ34' in infile:
        leg.SetHeader("N_{j} #in [3,4]")
    elif 'NJ6i' in infile:
        leg.SetHeader("N_{j} #geq 6")

    for i,(bin,hist) in enumerate(hList):

        print hist
        for ibin in range(1,hist.GetNbinsX()+1):
            print ibin, hist.GetBinContent(ibin), hist.GetBinError(ibin)
            if hist.GetBinContent(ibin) == 0:
                hist.SetBinError(ibin,0)

        if i == 0:
            #hist.GetYaxis().SetNdivisions(505)
            #hist.GetYaxis().SetRangeUser(0,1.45)
            hist.GetYaxis().SetRangeUser(0,0.49)
            #hist.GetYaxis().SetRangeUser(0,0.12)
            hist.GetYaxis().SetTitleOffset(1.4)
            hist.GetYaxis().SetTitleSize(0.04)
            hist.GetYaxis().SetLabelSize(0.03)
            hist.GetYaxis().SetTitle("F_{sel-to-anti}")
            #hist.GetYaxis().SetTitle("R_{CS}")
            #hist.GetYaxis().SetTitle("#frac{QCD}{QCD+EWK}")

        # make up hist
        hist.SetStats(0)
        hist.SetMarkerColor(colorList[i])
        hist.SetLineColor(colorList[i])
        if doTransp: hist.SetFillColorAlpha(colorList[i],0.35)
        else:  hist.SetFillColor(colorList[i])
        #hist.SetFillStyle(3002)

        hist.Draw(plotOpt)
        if "same" not in plotOpt: plotOpt += "same"

        leg.AddEntry(hist,getBinLabel(bin),"pl")

    leg.Draw()

    CMS_lumi.CMS_lumi(canv, 4, iPos)

    if not batchMode:
        raw_input("Press 'Enter' to continue")

    exts = [".pdf",".png"]
    for ext in exts:
        canv.SaveAs(outfile.GetName().replace(".root",ext))

    tfile.Close()
    outfile.Close()
