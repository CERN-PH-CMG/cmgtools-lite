#!/usr/bin/env python
# usage: python parsetable.py A*_8TeV_atlas.txt
import os,re,sys
from array import array
from math import *

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True

def parseOneTable(filename,tfile):
    inputfile = open(filename)
    lines = inputfile.readlines()
    for i,line in enumerate(lines):
        l=line.rstrip()
        p = re.compile('(-?0\.\d+\spm\s0\.\d+\spm\s0\.\d+)')
        vals = p.findall(l)
        etastr = "eta%s_%s" % (etaBins[i],etaBins[i+1])
        histoname = basename+"_"+etastr
        histo = ROOT.TH1F(histoname,"",len(ptBins)-1,array('f',ptBins))
        for b,ptb in enumerate(vals):
            ai = [float(f) for f in ptb.split(" pm ")]
            #print "pt bin: [",ptBins[b],",",ptBins[b+1],"] = ",ai
            histo.SetBinContent(b+1,ai[0])
            histo.SetBinError(b+1,hypot(ai[1],ai[2]))
        tfile.WriteTObject(histo)

def makeAiPlot(filename,i):
    ROOT.gROOT.ProcessLine(".x %s/src/CMGTools/WMass/python/plotter/tdrstyle.cc" %  os.environ['CMSSW_BASE'])
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetOptTitle(0)
    ROOT.gStyle.SetErrorX(0.5);

    etaBins = ["00", "10", "20", "35"]
    labels = ["|#eta|<1","1<|#eta|<2","2<|#eta|<3.5"]
    colors = [ROOT.kBlack, ROOT.kOrange+1, ROOT.kGreen+3]
    tf = ROOT.TFile(filename)
    leg = ROOT.TLegend(.70, .15, .90, .35)
    leg.SetFillColor(0)
    leg.SetShadowColor(0)
    leg.SetLineColor(0)
    leg.SetTextFont(42)
    leg.SetTextSize(0.035)
    c1 = ROOT.TCanvas("canvas","",600,600)
    c1.SetLogx()
    ymin=1; ymax=-1
    histos = []
    for eb in range(len(etaBins)-1):
        histo = tf.Get("A%d_8TeV_atlas_eta%s_%s" % (i,etaBins[eb],etaBins[eb+1]))
        histo.SetMarkerColor(colors[eb])
        histo.SetLineColor(colors[eb])
        histo.SetMarkerStyle(ROOT.kFullSquare)
        histo.SetMarkerSize(0.9)
        histo.GetXaxis().SetTitle("p_{T}^{Z} [GeV]")
        histo.GetYaxis().SetTitle("A_{%d}" % i)
        ymax = max(ymax,histo.GetBinContent(histo.GetMaximumBin())+histo.GetBinError(histo.GetMaximumBin()))
        ymin = min(ymin,histo.GetBinContent(histo.GetMinimumBin())+histo.GetBinError(histo.GetMinimumBin()))
        histos.append(histo)
        leg.AddEntry(histo,labels[eb],"pe")

    for eb,h in enumerate(histos):
        h.GetYaxis().SetRangeUser(ymin,ymax)
        h.GetYaxis().SetLimits(ymin,ymax)
        h.Draw("pe" if eb==0 else "same pe")

    leg.Draw()
    [c1.SaveAs("A%d_ATLAS.%s" % (i,ext)) for ext in ["pdf","png"]]

if __name__ == '__main__':

    from optparse import OptionParser
    parser = OptionParser(usage="%prog testname ")
    parser.add_option("-p", "--plotOnly", dest="plotOnly", action="store_true", default=False, help="Do not redo the root file, only plot the Ais from root file");
    (options, args) = parser.parse_args()

    if not options.plotOnly:
        if len(args) == 0:
            print "You must provide at least one file to parse"
            exit(0)
     
        ptBins = [0.0 , 2.5 , 5.0 , 8.0 , 11.4 , 14.9 , 18.5 , 22.0 , 25.5 , 29.0 , 32.6 , 36.4 , 40.4 , 44.9 , 50.2 , 56.4 , 63.9 , 73.4 , 85.4 , 105 , 132 , 173 , 253 , 600 ]
        etaBins = ["00", "10", "20", "35"]
     
        tfile = ROOT.TFile.Open("Ai_8TeV_atlas.root","recreate")
        for fname in args[1:]:
            print "fname = ", fname
            basename = os.path.basename(fname).split('.')[0]
            print "Creating histograms for ", basename
            parseOneTable(fname,tfile)
        tfile.Close()

    for i in range(5):
        makeAiPlot("Ai_8TeV_atlas.root",i)

    print "DONE."
