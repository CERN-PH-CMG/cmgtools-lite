#!/usr/bin/env python
import ROOT
ROOT.gROOT.SetBatch(True)

from math import *
from os.path import dirname,basename
from CMGTools.TTHAnalysis.tools.plotDecorations import *
from CMGTools.TTHAnalysis.plotter.mcPlots import *

options = None
if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser(usage="%prog [options] mca.txt cuts.txt plots.txt varname mlfile channel")
    addPlotMakerOptions(parser)
    (options, args) = parser.parse_args()
    mca = MCAnalysis(args[0],options)
    plots = PlotFile(args[2],options)
    basedir = options.printDir
    infile = ROOT.TFile(basedir+"/"+basename(args[2]).replace(".txt","")+".root");
    var    = args[3];
    pspec = [p for p in plots.plots() if p.name == var ][0]
    mlfile = ROOT.TFile(args[4]);
    channel = args[5];
    for O,MLD in ("prefit","prefit"), ("postfit_b","fit_b"), ("postfit_s","fit_s"):
        normset = mlfile.Get("norm_"+MLD)
        mldir  = mlfile.GetDirectory("shapes_"+MLD);
        if not mldir: raise RuntimeError, mlfile
        outfile = ROOT.TFile(basedir + "/"+O+"_" + basename(args[2]), "RECREATE")
        pspec.name = O+"_"+var
        processes = [p for p in reversed(mca.listBackgrounds())] + mca.listSignals()
        hdata = infile.Get(var+"_data")
        plots = {'data':HistoWithNuisances(hdata)}
        if options.poisson:
              pdata = getDataPoissonErrors(hdata, False, True)
              hdata.poissonGraph = pdata ## attach it so it doesn't get deleted
        if channel == "2lss":
            allchannels = [ f+"_"+c for f in ("ee","em_bl","em_bt","mm_bl","mm_bt") for c in ("pos","neg") ]
            subbins = 8
        elif channel == "3l":
            allchannels = [ f+"_"+c for f in ("bl","bt") for c in ("neg","pos") ]
            subbins = 5
        else: raise RuntimeError
        for p in processes:
            h = infile.Get(var+"_"+p)
            if not h: 
                print "Missing %s_%s for %s" % (var,p, p)
                continue
            h = h.Clone(var+"_"+p)
            h.Reset()
            h.SetDirectory(0)
            for isub,subch in enumerate(allchannels):
                hpf = mldir.Get("ttH_%s_%s/%s" % (channel,subch,p))
                if not hpf: 
                    print "Could not find post-fit shape for %s in %s_%s" % (p,channel,subch)
                    continue
                for b in xrange(1, subbins+1):
                    h.SetBinContent(b+isub*subbins, hpf.GetBinContent(b))
                    h.SetBinError(b+isub*subbins, hpf.GetBinError(b))
                #print 'for',subch,'adding',p,'with norm',hpf.Integral()
            plots[p] = HistoWithNuisances(h)
        htot = hdata.Clone(var+"_total")
        htot.Reset()
        for isub,subch in enumerate(allchannels):
            htotpf = mldir.Get("ttH_%s_%s/total"% (channel,subch) )
            for b in xrange(1, subbins+1):
                 htot.SetBinContent(b+isub*subbins, htotpf.GetBinContent(b))
                 htot.SetBinError(b+isub*subbins, htotpf.GetBinError(b))
        htot = HistoWithNuisances(htot)
        plotter = PlotMaker(outfile,options)
        if channel == "2lss":
            options.legendHeader = "l^{#pm}l^{#pm}"
        elif channel == "3l":
            options.legendHeader = "3l"
        if O == "prefit": options.legendHeader += ", pre-fit"
        if O == "postfit_b": options.legendHeader += ", post-fit (SM prediction)"
        if O == "postfit_s": options.legendHeader += ", post-fit (#hat{#mu} = 1.5)"
        plotter.printOnePlot(mca,pspec,plots,mytotal=htot,printDir=basedir)
