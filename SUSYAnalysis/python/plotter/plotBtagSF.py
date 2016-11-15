#!/usr/bin/python

import sys
import os
#sys.argv.append( '-b' )

from ROOT import *
## STYLE
gStyle.SetOptTitle(0)
gStyle.SetOptStat(0)
'''
gStyle.SetPadTopMargin(0.05)
gStyle.SetPadBottomMargin(0.125)
gStyle.SetPadRightMargin(0.075)
gStyle.SetPadLeftMargin(0.125)
'''

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
        exit()

    '''
    tfile  = TFile(infile, "READ")
    tree = tfile.Get("sf/t")
    '''
    tree = TChain("sf/t")
    tree.Add(infile)

    # get sample name
    samp = infile[infile.find("evVarFriend_"):]
    #samp = samp[infile.find("d_")+1:]
    samp = samp.replace(".root","")
    samp = samp.replace("evVarFriend_","")
    if "*" in samp: samp = samp[:samp.find("*")]
    print "Sample", samp

    print tree.GetEntries()

    # settings for hists
    #names = ["central","b-Up","b-Down","l-Up","l-Down"]
    names = ["central","HF-Up","HF-Down","LF-Up","LF-Down"]
    weights = ["btagSF","btagSF_b_up","btagSF_b_down","btagSF_l_up","btagSF_l_down"]
    cols = [kBlack,kRed,kRed,kBlue,kBlue]
    lsty = [1,2,3,2,3]

    var = "nBJets30"
    #var = "nJets30Clean"
    #var = "HT"

    # create hists
    hists = []
    for i,name in enumerate(names):
        hist = TH1F(name,name,5,-0.5,4.5)
        #hist = TH1F(name,name,15,-0.5,14.5)
        #hist = TH1F(name,name,100,500,2500)

        tree.Draw(var + " >>" + name,weights[i],"goff")

        hist.SetLineWidth(2)
        hist.SetLineColor(cols[i])
        hist.SetLineStyle(lsty[i])

        hists.append(hist)

    # set up hist
    hists[0].GetXaxis().SetTitle("N_{b-tag}")
    hists[0].GetXaxis().SetNdivisions(505)

    # show relative variations
    doRel = False

    if doRel:
        for hist in reversed(hists): hist.Divide(hists[0])
        #hists[0].GetYaxis().SetRangeUser(0.81,1.19)
        hists[0].GetYaxis().SetRangeUser(0.51,1.49)
        hists[0].GetYaxis().SetTitle("Variation")
        hists[0].GetYaxis().SetTitleOffset(1.2)
    else:
        for hist in reversed(hists): hist.Scale(1/hists[0].Integral())
        hists[0].GetYaxis().SetTitle("Normalised events [a.u.]")
        hists[0].GetYaxis().SetTitleOffset(1.2)
        hists[0].GetYaxis().SetLabelSize(0.025)

    canv = TCanvas("cNBjetsSF","NBjets with SF",800,800)
    for i,hist in enumerate(hists):

        if i == 0: hist.Draw("histe1")
        else: hist.Draw("histsame")

    leg = canv.BuildLegend()
    leg.SetHeader(samp)

    if not batchMode:
        raw_input("Exit")

    if doRel:
        cname = "plots/btagVar_relative_" + samp
    else:
        cname = "plots/btagVar_norm_" + samp

    for ext in [".pdf",".png"]:
        canv.SaveAs(cname+ext)

    #tfile.Close()
