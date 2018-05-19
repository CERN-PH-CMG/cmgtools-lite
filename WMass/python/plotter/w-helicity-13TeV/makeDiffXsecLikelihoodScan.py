#!/usr/bin/env python

# python makeDiffXsecLikelihoodScan.py ../diffXsecFit_testScalLikelihood_freezeShapeNuis/ [-2.5,-2.25,-2.0,-1.8,-1.566,-1.4442,-1.3,-1.2,-1.1,-1.0,-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.1,1.2,1.3,1.4442,1.566,1.8,2.0,2.25,2.5]*[30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45] -o ../plots/diffXsec/likelihoodScan/ -f el -c plus


from shutil import copyfile
import re, sys, os, os.path, subprocess, json, ROOT
import numpy as np
from math import hypot
from array import array

from make_diff_xsec_cards import getXYBinsFromGlobalBin
from make_diff_xsec_cards import getGlobalBin
from make_diff_xsec_cards import getArrayParsingString

sys.path.append(os.environ['CMSSW_BASE']+"/src/CMGTools/WMass/python/plotter/")
from plotUtils.utility import *

if __name__ == "__main__":

    from optparse import OptionParser
    parser = OptionParser(usage="%prog [options] higgsCombineFolder binning")
    parser.add_option('-o','--outdir', dest='outdir', default='./', type='string', help='output directory')
    parser.add_option('-n','--n-points', dest='npoints', default=0, type='int', help='Number of points used for the scan')
    parser.add_option(     '--min-bin', dest='minbin', default=1, type='int', help='minimum bin number when selecting bin range for the scans')
    parser.add_option(     '--max-bin', dest='maxbin', default=0, type='int', help='max bin number when selecting bin range for the scans (0 for up to the last one)')
    parser.add_option("-f", "--flavour", dest="flavour", type="string", default='el', help="Channel: either 'el' or 'mu'");
    parser.add_option("-c", "--charge", dest="charge", type="string", default='plus', help="Charge: either 'plus' or 'minus'");
    parser.add_option(      "--scan-fit-opt", dest="scanFitOpt", type="string", default='QMRFS+', help="Options passed to TGraph::Fit for the scan fit");
    parser.add_option(      "--maxDNLL", dest="maxDNLL", type="float", default='1000000.0', help="Maximum deltaNLL to add point in graph");
    parser.add_option(      "--minDNLL", dest="minDNLL", type="float", default='0.05', help="Minimum deltaNLL to add point in graph");
    parser.add_option(      "--no-save-scan", dest="nosavescan", action="store_true", default=False, help="Do not save the scans, just the 2D maps with the summary")
    parser.add_option(      "--no-save-summary", dest="nosavesummary", action="store_true", default=False, help="Do not save the summary (mainly for tests, not to overwrite the 2D maps that need to be done running on all bins")
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

    filteredfiles = []    
    if options.minbin > 1 or options.maxbin > 0:
        maxFileIndex = min(options.maxbin,len(files)) if options.maxbin > 0 else len(files)
        for f in files:
            rootfile = f.split('/')[-1]
            globalbin = re.findall(r'\d+', rootfile)
            globalbin = int(globalbin[0])
            if globalbin >= options.minbin and globalbin <= maxFileIndex:
                filteredfiles.append(f)            
    else:
        filteredfiles = files
    
    print "I will run the scans for %d files from %d to %d out of %d" % (len(filteredfiles),options.minbin,options.maxbin if options.maxbin else len(files), len(files))

    nMissingTree = 0

    for f in filteredfiles:

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
            nMissingTree += 1
            continue

        dnll_r = {}
        nVarPoints = tree.GetEntries() - 1
        for entry in tree:
            r = tree.r
            dnll = 2. * tree.deltaNLL
            #print "r=%.3f   2*dNLL=%.3f" % (r, dnll)
            if ((dnll <= options.maxDNLL and dnll >= options.minDNLL) or r == 1.0): 
                dnll_r[r] = dnll

        gr = ROOT.TGraph()
        keys = dnll_r.keys()
        # find first point with y value < options.maxDLL and > options.minDLL
        firstPointFound = False
        xminfit = 0.9
        xmaxfit = 1.1
        for i,key in enumerate(sorted(keys)):
            #print "Adding point %f   %f to graph" % (key,dnll_r[key])
            gr.SetPoint(i, key, dnll_r[key])
            # save x of first value with ordinate < options.maxDNLL, also used for fit below
            if (not firstPointFound and dnll_r[key] <= options.maxDNLL and dnll_r[key] >= options.minDNLL): 
                xminfit = 0.99 * key
                xmaxfit = 2.0 - xminfit
                firstPointFound = True

        c = ROOT.TCanvas("c","",700,600)
        c.cd()
        c.SetTickx(1)
        c.SetTicky(1)
        c.cd()
        c.SetFillColor(0)
        c.SetGrid()
        c.SetLeftMargin(0.14)

        gr.SetMarkerStyle(20)
        gr.SetMarkerColor(ROOT.kBlack)
        gr.SetLineColor(ROOT.kBlack)
        gr.SetLineWidth(2)
        gr.SetFillColor(ROOT.kBlack)
        gr.Draw("ap")
        
        gr.SetTitle("Bin %d: #eta #in [%.3g, %.3g], p_{T} #in [%.0f, %.0f]" % (globalbin,etal,etah,ptl,pth))
        gr.GetXaxis().SetTitleSize(0.05)
        gr.GetXaxis().SetLabelSize(0.04)
        gr.GetYaxis().SetTitleOffset(1.3)
        gr.GetYaxis().SetTitleSize(0.05)
        gr.GetYaxis().SetLabelSize(0.04)
        gr.GetXaxis().SetTitle("r")
        gr.GetYaxis().SetTitle("2 #times #Delta NLL")
        gr.GetXaxis().SetRangeUser(xminfit,xmaxfit)
        maxStoredValDNLL = max(dnll_r[key] for key in dnll_r)
        gr.GetYaxis().SetRangeUser(-0.1,1.2*min(options.maxDNLL,maxStoredValDNLL))

        # very first fit with pol9 (random, just need something that follows the points
        f1 = ROOT.TF1("f1","pol9",xminfit,xmaxfit) # symmetric range in r
        gr.Fit(f1,options.scanFitOpt) 
        fit = gr.GetFunction("f1")
        fit.SetLineWidth(3)
        fit.SetLineColor(ROOT.kOrange+2)
        #f2 = ROOT.TF1("f2","pol2",xminfit,xmaxfit)
        #gr.Fit(f2,options.scanFitOpt) 
        #parabola = gr.GetFunction("f2")
        #parabola.SetLineWidth(3)
        #parabola.SetLineColor(ROOT.kBlue)

        mypol2 = ROOT.TF1("mypol2","[0]*(x-1)**2",xminfit,xmaxfit);  # a*(x-1)^2 is a parabola centered at x = 1, with minimum at 0
        mypol2.SetParameter(0,300)  # we would expect that for x = 0.9 it is roughly 2*deltaNLL=3
        mypol2.SetParLimits(0,10,600) 
        gr.Fit("mypol2",options.scanFitOpt) 
        mypol2 = gr.GetFunction("mypol2")
        mypol2.SetLineWidth(3)
        mypol2.SetLineColor(ROOT.kGreen+3)        


        # ## algo to remove points too far from the expected position 
        # # let's assume r in [0.9, 1.1], dnll(max)~5
        # arr_rleft = [r for r in dnll_r.keys() if r <= 1.0] 
        # arr_rleft = sorted(arr_rleft,reverse=True)
        # arr_rright = [r for r in dnll_r.keys() if r >= 1.0] 
        # arr_rright = sorted(arr_rright)
        # # roughly, the distance between close points is sqrt(dr^2 + dy^2), where dr= r_i -r_(i+1)
        # # dy can be defined as (Ymax-Ymin)/n(r) where Ymin=0 and n(r) is the number of points in each side before rejection (i.e. number of scans divided by2)
        # # it can be estmated evaluating a preliminary fit with parabola
        # # goodPoints = dict(dnll_r)
        # # for i in range(len(arr_rleft)):
        # #     dr = arr_rleft[i]-arr_rleft[i+1]
        # #     dy = dnll_r[arr_rleft[i]] - dnll_r[arr_rleft[i+1]]
        # #     dist = hypot(dr, dy)
        # #     # now we expect the distance to be close to that obtained from same dr and dy from parabola
        # #     # we could approximate the distance as sqrt(2)*dr (diagonal of square built on dr)
        # #     # but this would not take into account the non constant derivative of the parabola.
        # #     expdy = mypol2.Eval(arr_rleft[i]) - mypol2.Eval(arr_rleft[i+1])
        # #     expdist = hypot(dr, expdy) 
        # #     if (expdist > 1.5 * expdy): del goodPoints[arr_rleft[i+1]]

        hDistFitGraph = ROOT.TH1D("hDistFitGraph","",500,0,25)
        nTrial = 3
        colors = [ROOT.kRed, ROOT.kGreen+2, ROOT.kAzure+2, ROOT.kViolet,ROOT.kOrange+1]  # make it with at least nTrial colors
        newdnll_r = dict(dnll_r)
        graphs = {}
        for i in range(nTrial):
            name = "nTrial%d" % i
            graphs[name] = ROOT.TGraph()
            hDistFitGraph.Reset()
            print "trial",str(i)
            for r in sorted(newdnll_r):
                #print "x, y = %.3f, %.3f" % (r,newdnll_r[r]) 
                hDistFitGraph.Fill(abs(mypol2.Eval(r)-dnll_r[r]))
            mean = hDistFitGraph.GetMean()
            stddev = hDistFitGraph.GetStdDev()
            print "mean dist: %.3f, rms: %.3f " % (mean,stddev)
            for r in newdnll_r.keys():
                if abs(mypol2.Eval(r)-newdnll_r[r]) > (mean+stddev): del newdnll_r[r]
            keys = newdnll_r.keys()
            for point,r in enumerate(sorted(keys)):
                graphs[name].SetPoint(point,r,newdnll_r[r])            
            graphs[name].SetMarkerColor(colors[i])
            graphs[name].SetMarkerStyle(20)
            graphs[name].Draw("P SAME")
            graphs[name].Fit(mypol2,options.scanFitOpt)         
            func = graphs[name].GetFunction("mypol2")         
            func.SetLineColor(colors[i])
            #func.DrawCopy("SAME")
            
        finalkeys = sorted(newdnll_r.keys())
        finalxmin = finalkeys[0]
        finalxmax = finalkeys[len(finalkeys)-1]
        # f1 = ROOT.TF1("f1","pol9",finalxmin,finalxmax) # symmetric range in r
        # graphs[name].Fit(f1,"0"+options.scanFitOpt) 
        # fit = graphs[name].GetFunction("f1")
        # fit.SetLineWidth(3)
        r1sigmaDn = func.GetX(1.0, 0.5, 1)
        r1sigmaUp = func.GetX(1.0, 1, 1.5)
        rMinFit = func.GetMinimumX(0.95, 1.05)  # 1 by definition because we forced mypol2 to pass through (1,0)
        print "Bin %d --> Fit: rmin = %.3f    +/- 1 sigma range = [%.3f, %.3f]" % (globalbin, rMinFit, r1sigmaDn, r1sigmaUp)


        leg = ROOT.TLegend(0.30, 0.50, 0.7, 0.85)
        leg.SetFillColor(0)
        leg.SetFillStyle(0)
        leg.SetBorderSize(0)
        chLeg = 'W^{+}' if charge == "plus" else 'W^{-}'
        flLeg = 'e' if flavour == "el" else "#mu"
        leg.SetHeader("Channel: {ch} #rightarrow {fl}#nu".format(ch=chLeg, fl=flLeg) )
        leg.AddEntry(gr , "scan: 1 + %d/%d points" % (nVarPoints,options.npoints), 'PL')
        leg.AddEntry(fit, "fit with pol9", 'lf')
        #leg.AddEntry(parabola, "fit with pol2", 'lf')
        leg.AddEntry(mypol2, "first fit: y = a#dot(x-1)^{2}", 'lf')
        leg.AddEntry(func, "last fit: y = a#dot(x-1)^{2}", 'lf')
        leg.AddEntry(0, "r(min) = %.3f" % rMinFit, '')
        leg.AddEntry(0, "r(-1#sigma) = %.3f" % r1sigmaDn, '')
        leg.AddEntry(0, "r(+1#sigma) = %.3f" % r1sigmaUp, '')
        leg.Draw('same')    
 
        c.RedrawAxis("sameaxis")
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
    adjustSettings_CMS_lumi()

    lepton = "electron" if flavour == "el" else "muon"
    for h in h2list:
        h.SetStats(0)
        xname = "%s #eta" % lepton
        yname = "%s p_{T}" % lepton
        zname = h.GetZaxis().GetTitle()

        if not options.nosavesummary:
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


    print "#################################"
    print "Summary"
    print "---------------------------------"
    print "Made %d scans " % len(filteredfiles)
    print "Occurrences of missing tree %d" % nMissingTree
