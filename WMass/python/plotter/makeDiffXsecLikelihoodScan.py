#!/usr/bin/env python

# python makeDiffXsecLikelihoodScan.py diffXsecFit_testScalLikelihood_freezeShapeNuis/ [-2.5,-2.25,-2.0,-1.8,-1.566,-1.4442,-1.3,-1.2,-1.1,-1.0,-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.1,1.2,1.3,1.4442,1.566,1.8,2.0,2.25,2.5]*[30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45] -o plots/diffXsec/likelihoodScan/ -f el -c plus


from shutil import copyfile
import re, sys, os, os.path, subprocess, json, ROOT
import numpy as np
from array import array

from w_helicity_13TeV.make_diff_xsec_cards import getXYBinsFromGlobalBin
from w_helicity_13TeV.make_diff_xsec_cards import getGlobalBin
from w_helicity_13TeV.make_diff_xsec_cards import getArrayParsingString

from utility import *

if __name__ == "__main__":

    from optparse import OptionParser
    parser = OptionParser(usage="%prog [options] higgsCombineFolder binning")
    parser.add_option('-o','--outdir', dest='outdir', default='./', type='string', help='output directory')
    parser.add_option('-n','--n-points', dest='npoints', default=0, type='int', help='Number of points used for the scan')
    parser.add_option("-f", "--flavour", dest="flavour", type="string", default='el', help="Channel: either 'el' or 'mu'");
    parser.add_option("-c", "--charge", dest="charge", type="string", default='plus', help="Charge: either 'plus' or 'minus'");
    parser.add_option(      "--no-save-scan", dest="nosavescan", action="store_true", default=False, help="Do not save the scans, just the 2D maps with the summary")
    (options, args) = parser.parse_args()

    if len(args) < 2:
        parser.print_usage()
        quit()

    ROOT.gROOT.SetBatch()
 
    charge = options.charge
    flavour = options.flavour
    outdir = options.outdir
    if not outdir.endswith('/'): outdir += "/"    
    if outdir != "./":
        if not os.path.exists(outdir):
            print "Creating folder", outdir
            os.system("mkdir -p " + outdir)
        os.system('cp {pf} {od}'.format(pf='/afs/cern.ch/user/g/gpetrucc/php/index.php',od=outdir))

    inputdir = args[0]
    if not inputdir.endswith('/'): inputdir += "/"    

    binning = args[1]
    etabinning=binning.split('*')[0]    # this is like [a,b,c,...], and is of type string. We nedd to get an array    
    ptbinning=binning.split('*')[1]
    etabinning = getArrayParsingString(etabinning)
    ptbinning = getArrayParsingString(ptbinning)
    tmpbinning = [float(x) for x in etabinning]  ## needed for constructor of TH2 below
    etabinning = tmpbinning
    tmpbinning = [float(x) for x in ptbinning]
    ptbinning = tmpbinning 
    print "eta binning " + str(etabinning)
    print "pt  binning " + str(ptbinning)
    nptbins = len(ptbinning)-1
    netabins = len(etabinning)-1
    nBinsInTemplate = (netabins)*(nptbins)

    files = [ f for f in os.listdir(inputdir) if f.endswith('.root') and f.startswith('higgsCombine')]
    files = list( [os.path.join(inputdir, f) for f in files] ) 
    #files = [inputdir + "higgsCombine_Wplus_bin365.MultiDimFit.mH120.root"]

    h2_npoints = ROOT.TH2D("h2_npoints","",netabins, array('d',etabinning), nptbins, array('d',ptbinning))
    h2_rMinFit = ROOT.TH2D("h2_rMinFit","",netabins, array('d',etabinning), nptbins, array('d',ptbinning))
    h2_r1sigmaDn = ROOT.TH2D("h2_r1sigmaDn","",netabins, array('d',etabinning), nptbins, array('d',ptbinning))
    h2_r1sigmaUp = ROOT.TH2D("h2_r1sigmaUp","",netabins, array('d',etabinning), nptbins, array('d',ptbinning))
    h2_r1sigmaUpDnMean = ROOT.TH2D("h2_r1sigmaUpDnMean","",netabins, array('d',etabinning), nptbins, array('d',ptbinning))  #(Up+Dn)/2 - 1 (0 if symmetric)

    for f in files:

        rootfile = f.split('/')[-1]
        print "========================"
        print "Scanning file",rootfile
        # one way to match bin number
        # nameBeforeBinNum = "higgsCombine_W{ch}_bin".format(ch=charge)
        # regex = re.compile(nameBeforeBinNum+'([0-9]*)')  # get whatever number after nameBeforeBinNum
        # globalbin = regex.findall(rootfile)
        ## another possibility is the following
        globalbin = re.findall(r'\d+', rootfile)
        # print globalbin
        globalbin = int(globalbin[0])
        etabin,ptbin = getXYBinsFromGlobalBin(globalbin,netabins,False) ## indices from 1 in both input and output, usable for TH2::GetBinContent
        etal = h2_npoints.GetXaxis().GetBinLowEdge(etabin)
        etah = h2_npoints.GetXaxis().GetBinLowEdge(etabin+1)
        ptl  = h2_npoints.GetYaxis().GetBinLowEdge(ptbin)
        pth  = h2_npoints.GetYaxis().GetBinLowEdge(ptbin+1)
        #etabin,ptbin = getXYBinsFromGlobalBin(globalbin-1,netabins)  ## array-like indices in both input and output
        print "Global bin = %d    eta,pt bin= %d,%d (indices from 1)"  % (globalbin,etabin,ptbin)
        print "Eta in [%.3g, %.3g] --- Pt in [%.0f, %.0f]"  % (etal,etah,ptl,pth)
        tf = ROOT.TFile(f, 'READ')
        tree = tf.Get("limit")
        if not tree:
            print "Warning: tree named 'limit' not found in file",rootfile
            print "Skipping and continuing"
            continue

        dnll_r = {}
        nVarPoints = tree.GetEntries() - 1
        for entry in tree:
            r = tree.r
            dnll = 2. * tree.deltaNLL
            #print "r=%.3f   2*dNLL=%.3f" % (r, dnll)
            if (dnll > 0 or r == 1.0): 
                dnll_r[r] = dnll

        gr = ROOT.TGraph(len(dnll_r))
        keys = dnll_r.keys()
        i = 0
        # find first point with y value < 10 (but not 0)
        pointFound = False
        xminfit = 0.9
        xmaxfit = 1.1
        for key in sorted(keys):
            #print "Adding point %f   %f to graph" % (key,dnll_r[key])
            gr.SetPoint(i, key, dnll_r[key])
            i += 1
            # save x of first value with ordinate < 2, used for fit below
            if (not pointFound and dnll_r[key] <= 10 and dnll_r[key] > 0.0): 
                xfitmin = key
                xfitmax = 2.0 - xfitmin
                pointfound = True

        c = ROOT.TCanvas("c","",700,600)
        c.cd();
        c.SetTickx(1);
        c.SetTicky(1);
        c.cd();
        c.SetFillColor(0);
        c.SetGrid();
        c.SetLeftMargin(0.14)

        gr.SetMarkerStyle(20);
        gr.SetMarkerColor(ROOT.kBlack);
        gr.SetLineColor(ROOT.kBlack);
        gr.SetLineWidth(2);
        gr.SetFillColor(ROOT.kBlack);
        gr.Draw("ap");
        
        gr.SetTitle("Bin %d: #eta #in [%.3g, %.3g], p_{T} #in [%.0f, %.0f]" % (globalbin,etal,etah,ptl,pth));
        gr.GetXaxis().SetTitleSize(0.05);
        gr.GetXaxis().SetLabelSize(0.04);
        gr.GetYaxis().SetTitleOffset(1.3);
        gr.GetYaxis().SetTitleSize(0.05);
        gr.GetYaxis().SetLabelSize(0.04);
        gr.GetXaxis().SetTitle("r");
        gr.GetYaxis().SetTitle("2 #times #Delta NLL");
        gr.GetXaxis().SetRangeUser(xfitmin,xfitmax);

        # fit
        f1 = ROOT.TF1("f1","pol9",xfitmin,xfitmax); # symmetric range in r
        #f1 = ROOT.TF1("f1","pol9",0.9,1.1); 
        fitres = gr.Fit("f1","EMFRS+"); 
        fit = gr.GetFunction("f1");
        fit.SetLineWidth(3);
        #for x in [0.9, 0.95, 0.99,1.05, 1.1]:
        #    print "f(%f) = %f " % (x, f1.Eval(x))
        r1sigmaDn = f1.GetX(1.0, 0.5, 1)
        r1sigmaUp = f1.GetX(1.0, 1, 1.5)
        rMinFit = f1.GetMinimumX(0.95, 1.05)
        print "Bin %d --> Fit: rmin = %.3f    +/- 1 sigma range = [%.3f, %.3f]" % (globalbin, rMinFit, r1sigmaDn, r1sigmaUp)

        leg = ROOT.TLegend(0.30, 0.50, 0.7, 0.85)
        leg.SetFillColor(0);
        leg.SetFillStyle(0);
        leg.SetBorderSize(0);
        chLeg = 'W^{+}' if charge == "plus" else 'W^{-}'
        flLeg = 'e' if flavour == "el" else "#mu"
        leg.SetHeader("Channel: {ch} #rightarrow {fl}#nu".format(ch=chLeg, fl=flLeg) )
        leg.AddEntry(gr , "scan: 1 + %d/%d points" % (nVarPoints,options.npoints), 'PL')
        leg.AddEntry(fit, "fit with pol9", 'lf')
        leg.AddEntry(0, "r(min) = %.3f" % rMinFit, '')
        leg.AddEntry(0, "r(-1#sigma) = %.3f" % r1sigmaDn, '')
        leg.AddEntry(0, "r(+1#sigma) = %.3f" % r1sigmaUp, '')
        leg.Draw('same')    
 
        c.RedrawAxis("sameaxis");
        if not options.nosavescan:
            for ext in ['png', 'pdf']:
                c.SaveAs('{od}/deltaNll_bin{bin}_{ch}.{ext}'.format(od=outdir, bin=globalbin, ch=charge, ext=ext))
            c = 0


        h2_npoints.SetBinContent(etabin,ptbin,nVarPoints)
        h2_rMinFit.SetBinContent(etabin,ptbin,rMinFit)
        h2_r1sigmaDn.SetBinContent(etabin,ptbin,1.-r1sigmaDn)
        h2_r1sigmaUp.SetBinContent(etabin,ptbin,r1sigmaUp-1.)
        h2_r1sigmaUpDnMean.SetBinContent(etabin,ptbin,((r1sigmaUp+r1sigmaDn)/2. -1))

        ### end of loop on bins

    h2list = []
    
    h2list.append(h2_npoints)
    h2list.append(h2_rMinFit)
    h2list.append(h2_r1sigmaDn)
    h2list.append(h2_r1sigmaUp)
    h2list.append(h2_r1sigmaUpDnMean)

    h2_npoints.GetZaxis().SetTitle("Successful scans::0.5,%f" % (0.5+float(options.npoints)))
    h2_rMinFit.GetZaxis().SetTitle("r minimum from fit::0.98,1.02")
    h2_r1sigmaDn.GetZaxis().SetTitle("r(-1#sigma)::0.0,0.1")
    h2_r1sigmaUp.GetZaxis().SetTitle("r(+1#sigma)::0.0,0.1")
    h2_r1sigmaUpDnMean.GetZaxis().SetTitle("(r(+1#sigma)+r(-1#sigma))/2 - 1")

    lepton = "electron" if flavour == "el" else "muon"
    for h in h2list:
        h.SetStats(0)
        xname = "%s #eta" % lepton
        yname = "%s p_{T}" % lepton
        zname = h.GetZaxis().GetTitle()

        drawCorrelationPlot(h, labelXtmp=xname, labelYtmp=yname, labelZtmp=zname,
                            canvasName=(h.GetName()+"_{ch}_{fl}".format(ch=charge,fl=flavour)), 
                            outdir=outdir,
                            smoothPlot=False,
                            drawProfileX=False,
                            scaleToUnitArea=False,
                            draw_both0_noLog1_onlyLog2=1,
                            leftMargin=0.16,
                            rightMargin=0.20,
                            nContours=(20 if h.GetName() == "h2_npoints" else 100),
                            palette=55
                            )
