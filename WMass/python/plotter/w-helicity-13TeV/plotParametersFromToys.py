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
def effSigma(histo):
    xaxis = histo.GetXaxis()
    nb = xaxis.GetNbins()
    xmin = xaxis.GetXmin()
    ave = histo.GetMean()
    rms = histo.GetRMS()
    total=histo.Integral()
    if total < 100: 
        print "effsigma: Too few entries to compute it: ", total
        return 0.
    ierr=0
    ismin=999
    rlim=0.683*total
    bwid = xaxis.GetBinWidth(1)
    nrms=int(rms/bwid)
    if nrms > nb/10: nrms=int(nb/10) # Could be tuned...
    widmin=9999999.
    for iscan in xrange(-nrms,nrms+1): # // Scan window centre 
        ibm=int((ave-xmin)/bwid)+1+iscan
        x=(ibm-0.5)*bwid+xmin
        xj=x; xk=x;
        jbm=ibm; kbm=ibm;
        bin=histo.GetBinContent(ibm)
        total=bin
        for j in xrange(1,nb):
            if jbm < nb:
                jbm += 1
                xj += bwid
                bin=histo.GetBinContent(jbm)
                total += bin
                if total > rlim: break
            else: ierr=1
            if kbm > 0:
                kbm -= 1
                xk -= bwid
                bin=histo.GetBinContent(kbm)
                total+=bin
            if total > rlim: break
            else: ierr=1
        dxf=(total-rlim)*bwid/bin
        wid=(xj-xk+bwid-dxf)*0.5
        if wid < widmin:
            widmin=wid
            ismin=iscan
    if ismin == nrms or ismin == -nrms: ierr=3
    if ierr != 0: print "effsigma: Error of type ", ierr
    return widmin

def plotPars(inputFile, mdFit, doPull=True, pois=None, selectString=''):
    
    fitFile = ROOT.TFile(mdFit)
    if fitFile == None: raise RuntimeError, "Cannot open file %s" % mdFit
    fit_s  = fitFile.Get("fit_mdf")
    if fit_s == None or fit_s.ClassName()   != "RooFitResult": raise RuntimeError, "File %s does not contain the output of the signal fit 'fit_mdf'"     % mdFit

    # get the initial parameters (from one multidim fit)
    fpi_s = fit_s.floatParsInit()
    # get the ones to be plotted
    pars = list(fpi_s.at(i).GetName() for i in xrange(len(fpi_s))) 

    channel=''
    if any(re.match('.*_el_.*',x) for x in pars): channel += 'el'
    if any(re.match('.*_mu_.*',x) for x in pars): channel += 'mu'
    if len(channel): print "UNDERSTOOD FROM PARAMETERS THAT YOU ARE RUNNING ON CHANNEL: ", channel

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
            error = ROOT.TH1F("error","",100,0,1e+7)
            tree.Draw( "trackedParamErr_{par}>>error".format(par=name))
            mean_err = error.GetMean()
            histo = ROOT.TH1F("pull","",100,-5,5)
            tree.Draw( "(trackedParam_{par}-{prefit})/{meanerr}>>pull".format(par=name,prefit=mean_p,meanerr=mean_err) )
            #tree.Draw( "(trackedParam_{par}-{prefit})/trackedParamErr_{par}>>pull".format(par=name,prefit=mean_p) )
        else:
            residual = ROOT.TH1F("residual","",100,-1.,1.)
            varname = "(trackedParam_{par}-{prefit})/{prefit}".format(par=name,prefit=mean_p)
            tree.Draw( "{var}>>residual".format(var=varname))
            rms = residual.GetRMS()
            histo = ROOT.TH1F("pull","",100,-5*rms,5*rms)
            tree.Draw( "{var}>>pull".format(var=varname) )
        histo.GetXaxis().SetTitle(histo.GetTitle())
        histo.GetYaxis().SetTitle("no toys (%d total)" % nToysInTree)
        histo.GetYaxis().SetTitleOffset(1.05)
        histo.GetXaxis().SetTitleOffset(0.9)
        histo.GetYaxis().SetTitleSize(0.05)
        histo.GetXaxis().SetTitleSize(0.05)
        if doPull:
            histo.GetXaxis().SetTitle("(%s-#theta_{0})/#sigma_{#theta}" % name)
        else:
            histo.GetXaxis().SetTitle("(%s-#theta_{0})/#theta_{0}" % name)

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
            c.SaveAs("%s_%s_%s.%s" % (name,'pull' if doPull else 'val',channel,ext))

        if fitPull:
            tlatex = ROOT.TLatex(); tlatex.SetNDC(); 
            tlatex.SetTextSize(0.11)
            tlatex.SetTextColor(4);
            tlatex.DrawLatex(0.65,0.80,"Mean    : %.3f #pm %.3f" % (histo.GetFunction("gaus").GetParameter(1),histo.GetFunction("gaus").GetParError(1)))
            tlatex.DrawLatex(0.65,0.66,"Sigma   : %.3f #pm %.3f" % (histo.GetFunction("gaus").GetParameter(2),histo.GetFunction("gaus").GetParError(2)))
            
            tlatex.SetTextSize(0.11);
            tlatex.SetTextColor(1);
            tlatex.DrawLatex(0.65,0.33,"Pre-fit #pm #sigma_{#theta}: %.3f #pm %.3f" % (mean_p, sigma_p))

            pullSummaryMap[name]=(histo.GetFunction("gaus").GetParameter(1),histo.GetFunction("gaus").GetParameter(2),
                                  histo.GetMean(),effSigma(histo))
            nPulls += 1
            
    if nPulls>0:
        print "Generating Pull Summaries...\n"
        nRemainingPulls = nPulls
        hc = ROOT.TCanvas("hc","",3000,2000); hc.SetGrid(0);
        pullPlots = 1;
        while nRemainingPulls > 0:
            nThisPulls = min(maxPullsPerPlot,nRemainingPulls)

            pullSummaryHist = ROOT.TH1F("pullSummary","",nThisPulls,0,nThisPulls);
            pullSummaryHist2 = ROOT.TH1F("pullSummary2","",nThisPulls,0,nThisPulls);
            pi=1
            sortedpulls = []
            if 'pdf' in pois:
                sortedpulls = sorted(pullSummaryMap.keys(), key=lambda k: int(k.split('pdf')[-1]))
            elif 'norm' in pois:
                keys = pullSummaryMap.keys()
                keys_l = list(k for k in keys if 'left' in k)
                keys_r = list(k for k in keys if 'right' in k)
                norms_l = sorted(keys_l, key=lambda k: int(k.split('_')[-1]), reverse=False)
                norms_r = sorted(keys_r, key=lambda k: int(k.split('_')[-1]), reverse=True)
                sortedpulls = norms_r + norms_l
            if len(sortedpulls)==0: break

            for name in sortedpulls:
                if pi>nThisPulls: break
                pull = pullSummaryMap[name]
                pullSummaryHist.GetXaxis().SetBinLabel(pi,name)
                pullSummaryHist.SetBinContent(pi,pull[0]);  pullSummaryHist.SetBinError(pi,pull[1])
                pullSummaryHist2.SetBinContent(pi,pull[2]);  pullSummaryHist2.SetBinError(pi,pull[3])
                del pullSummaryMap[name]
                pi += 1
                nRemainingPulls -= 1
            pullSummaryHist.SetMarkerStyle(20)
            pullSummaryHist.SetMarkerSize(1.)
            #pullSummaryHist.SetMarkerColor(ROOT.kBlack)
            #pullSummaryHist.SetLineColor(ROOT.kBlack)
            pullSummaryHist.SetFillColor(ROOT.kRed+1)
            pullSummaryHist.SetLineWidth(2)

            pullSummaryHist2.SetMarkerStyle(20)
            pullSummaryHist2.SetMarkerSize(1.)
            pullSummaryHist2.SetMarkerColor(ROOT.kBlack)
            pullSummaryHist2.SetLineColor(ROOT.kBlack)
            pullSummaryHist2.SetLineWidth(4)

            pullSummaryHist.SetLabelSize(pullLabelSize)
            pullSummaryHist.LabelsOption("v")
            pullSummaryHist.GetYaxis().SetRangeUser(-1.,1.)
            if doPull: pullSummaryHist.GetYaxis().SetTitle("pull summary (n#sigma)")
            else: pullSummaryHist.GetYaxis().SetTitle("residual summary (relative)")
            pullSummaryHist.Draw("E2")
            pullSummaryHist2.Draw("E1 SAME")

            leg = ROOT.TLegend(0.60, 0.60, 0.85, 0.80)
            leg.SetFillStyle(0)
            leg.SetBorderSize(0)
            leg.AddEntry(pullSummaryHist,"Gassian #sigma")
            leg.AddEntry(pullSummaryHist2,"Effective #sigma")
            leg.Draw("same")
            suffix=pois.replace('.*','')
            for ext in ['png', 'pdf']:
                hc.SaveAs("pullSummaryToys_{sfx}_{igroup}_{c}.{ext}".format(sfx=suffix,igroup=pullPlots,c=channel,ext=ext))
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

    plotPars(limitsFile,mdfitfile,doPull=True,pois='pdf.*')
    plotPars(limitsFile,mdfitfile,doPull=False,pois='norm_Wplus.*')
    plotPars(limitsFile,mdfitfile,doPull=False,pois='norm_Wminus.*')
