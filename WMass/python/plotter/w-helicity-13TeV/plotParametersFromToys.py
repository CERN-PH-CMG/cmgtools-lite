#!/usr/bin/env python

## USAGE
## python plotParametersFromToys.py higgsLimit.root multidimfit.root

import re
from sys import argv, stdout, stderr, exit
import datetime
argv.append( '-b-' )
import ROOT
ROOT.gROOT.SetBatch(True)
argv.remove( '-b-' )

lat = ROOT.TLatex(); lat.SetNDC()

def plotPars(inputFile, mdFit, doPull=True, pois=None, selectString=''):
    
    fitFile = ROOT.TFile(mdFit)
    if fitFile == None: raise RuntimeError, "Cannot open file %s" % mdFit
    fit_s  = fitFile.Get("fit_mdf")
    if fit_s == None or fit_s.ClassName()   != "RooFitResult": raise RuntimeError, "File %s does not contain the output of the signal fit 'fit_mdf'"     % mdFit

    # get the initial parameters (from one multidim fit)
    fpi_s = fit_s.floatParsInit()
    # get the ones to be plotted
    pars = list(fpi_s.at(i).GetName() for i in xrange(len(fpi_s))) 

    if pois:
        poi_patts = pois.split(",")
        for ppatt in poi_patts:
            pars = filter(lambda x: re.match(ppatt,x),pars)

    if any(re.match('pdf.*',x) for x in pars):
        pars = sorted(pars, key = lambda x: int(x.split('pdf')[-1]), reverse=False)

    treeFile = ROOT.TFile(inputFile)
    tree = treeFile.Get("limit")
    treename = tree.GetName()

    nPulls = 0
    pullLabelSize = 0.028
    maxPullsPerPlot = 30
    pullSummaryMap = {}

    c = ROOT.TCanvas("c","",960,800)

    for name in pars:

        print "Making pull for parameter ",name
        nuis_p = fpi_s.find(name)
        nToysInTree = tree.GetEntries()
     
        # get best-fit value and uncertainty at prefit for this 
        # nuisance parameter
        if nuis_p.getErrorLo()==0 : nuis_p.setErrorLo(nuis_p.getErrorHi())
        mean_p, sigma_p, sigma_pu,sigma_pd = (nuis_p.getVal(), nuis_p.getError(),nuis_p.getErrorHi(),nuis_p.getErrorLo())
     
        if not sigma_p > 0: sigma_p = (nuis_p.getMax()-nuis_p.getMin())/2
        nuisIsSymm = abs(abs(nuis_p.getErrorLo())-abs(nuis_p.getErrorHi()))<0.01 or nuis_p.getErrorLo() == 0

        if doPull:
            tree.Draw( "(trackedParam_%s-%f)/%f>>%s" % (name,mean_p,sigma_p,name) )
        else:
            tree.Draw( "trackedParam_%s>>%s" % (name,name) )
     
        histo = ROOT.gROOT.FindObject("%s" % name).Clone()
        histo.GetXaxis().SetTitle(histo.GetTitle())
        histo.GetYaxis().SetTitle("no toys (%d total)" % nToysInTree)
        histo.GetYaxis().SetTitleOffset(1.05)
        histo.GetXaxis().SetTitleOffset(0.9)
        histo.GetYaxis().SetTitleSize(0.05)
        histo.GetXaxis().SetTitleSize(0.05)
        histo.GetXaxis().SetTitle("(%s-#theta_{0})/#sigma_{#theta}" % name)
        
        histo.SetTitle("")
     
        fitPull = histo.Integral()>0
        if fitPull:
            histo.Fit("gaus")
            fit = histo.GetFunction("gaus")
            fit.SetLineColor(4)
            lat.DrawLatex(0.12, 0.8, 'mean:     {me:.2f}'.format(me=fit.GetParameter(1)))
            lat.DrawLatex(0.12, 0.7, 'err :     {er:.2f}'.format(er=fit.GetParameter(2)))
            lat.DrawLatex(0.12, 0.6, 'chi2/ndf: {cn:.2f}'.format(cn=fit.GetChisquare()/fit.GetNDF()))
        
        for ext in ['png', 'pdf']:
            c.SaveAs("%s_%s.%s" % (name,'pull' if doPull else 'val',ext))

        if fitPull:
            tlatex = ROOT.TLatex(); tlatex.SetNDC(); 
            tlatex.SetTextSize(0.11)
            tlatex.SetTextColor(4);
            tlatex.DrawLatex(0.65,0.80,"Mean    : %.3f #pm %.3f" % (histo.GetFunction("gaus").GetParameter(1),histo.GetFunction("gaus").GetParError(1)))
            tlatex.DrawLatex(0.65,0.66,"Sigma   : %.3f #pm %.3f" % (histo.GetFunction("gaus").GetParameter(2),histo.GetFunction("gaus").GetParError(2)))
            
            tlatex.SetTextSize(0.11);
            tlatex.SetTextColor(1);
            tlatex.DrawLatex(0.65,0.33,"Pre-fit #pm #sigma_{#theta}: %.3f #pm %.3f" % (mean_p, sigma_p))

            pullSummaryMap[name]=(histo.GetFunction("gaus").GetParameter(1),histo.GetFunction("gaus").GetParameter(2))
            nPulls += 1
            
    if doPull and nPulls>0:
        print "Generating Pull Summaries...\n"
        nRemainingPulls = nPulls
        hc = ROOT.TCanvas("hc","",3000,2000); hc.SetGrid(0);
        pullPlots = 1;
        while nRemainingPulls > 0:
            nThisPulls = min(maxPullsPerPlot,nRemainingPulls)

            pullSummaryHist = ROOT.TH1F("pullSummary","",nThisPulls,0,nThisPulls);
            pi=1
            for name,pull in sorted(pullSummaryMap.iteritems(), key=lambda(k,v): int(k.split('pdf')[-1])):
                if pi>nThisPulls: break
                pullSummaryHist.GetXaxis().SetBinLabel(pi,name);
                pullSummaryHist.SetBinContent(pi,pull[0]);
                pullSummaryHist.SetBinError(pi,pull[1]);
                del pullSummaryMap[name]
                pi += 1
                nRemainingPulls -= 1
            pullSummaryHist.SetMarkerStyle(20);
            pullSummaryHist.SetMarkerSize(1.);
            pullSummaryHist.SetMarkerColor(ROOT.kRed);
            pullSummaryHist.SetLineColor(ROOT.kRed);
            pullSummaryHist.SetLineWidth(2);
            pullSummaryHist.SetLabelSize(pullLabelSize);
            pullSummaryHist.LabelsOption("v");
            pullSummaryHist.GetYaxis().SetRangeUser(-1,1);
            pullSummaryHist.GetYaxis().SetTitle("pull summary (n#sigma)");
            pullSummaryHist.Draw("E1");
            for ext in ['png', 'pdf']:
                hc.SaveAs("pullSummaryToys_%d.%s" % (pullPlots,ext));
            pullPlots += 1


if __name__ == "__main__":

    ROOT.gROOT.SetBatch()
    ROOT.gStyle.SetOptStat(0)

    date = datetime.date.today().isoformat()

    from optparse import OptionParser
    parser = OptionParser(usage='%prog limitsFile mdfitfile [options] ')
    (options, args) = parser.parse_args()

    if len(args)<2: 
        print "need at least limitsFile and mdfitfile. Exit."
        exit(0)

    limitsFile = args[0]
    mdfitfile = args[1]

    plotPars(limitsFile,mdfitfile,pois='pdf.*')

