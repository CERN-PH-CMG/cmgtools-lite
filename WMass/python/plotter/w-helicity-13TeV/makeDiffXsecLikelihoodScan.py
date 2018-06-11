#!/usr/bin/env python

# python makeDiffXsecLikelihoodScan.py ../diffXsecFit_testScalLikelihood_freezeShapeNuis/ [-2.5,-2.25,-2.0,-1.8,-1.566,-1.4442,-1.3,-1.2,-1.1,-1.0,-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.1,1.2,1.3,1.4442,1.566,1.8,2.0,2.25,2.5]*[30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45] -o ../plots/diffXsec/likelihoodScan/ -f el -c plus -n 50


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

# def getXfromSpline(spline,yval,x0,dx,tolerance=0.001):
#     # return first x for which y=yval (in case you expect more, choose x0 accodingly
#     # pass a ROOT.TSpline3, the y value you are looking for, the starting x value x0, the step dx and the tolerance to claim to have found x(yval)

#     # y0 = spline.Eval(x0)
#     # if y0 > yval:
#     #     x0isUp = True
#     # elif y0 < yval:
#     #     x0isUp = False
#     # else:
#     #     retun x0
        
#     x = x0
#     found = False

#     while not found:
#         # sample the spline looking for x for which [y0,y(x)] contains yval (this is meant to avoid situations with non monotonic curves)
#         y1tmp = spline.Eval(x)
#         y2mp = spline.Eval(x + dx)
#         ymax = max(y1tmp,y2tmp)
#         ymin = min(y1tmp,y2tmp)
#         if ymax > yval and ymin < yval:
#             xlow = x
#             xup = x + 0.5 * dx
#             ycenter = spline.Eval(xup)
#             if ycenter > yval:
#                 ymin = min(ycenter,ymax)
#                 ymax = max(ycenter,ymax)
                
#         else:
#             x = x + dx

def filterBadScanPoints(gr, dnll_r, fdef, nTrial=3, maxDNLL=10.0, verbose=False):

    # dnll_r is a dictionary, key=r, value=2*deltaNLL (gr was built with this dictionary, so I could pass just on of them (to be implemented))

    hDistFitGraph = ROOT.TH1D("hDistFitGraph","",100,0, maxDNLL)
    colors = [ROOT.kRed, ROOT.kGreen+2, ROOT.kAzure+2, ROOT.kViolet, ROOT.kPink, ROOT.kBlue, ROOT.kOrange+1]  # make it with at least nTrial colors
    newdnll_r = dict(dnll_r) # copy dictionary of 2*dnll versus r, will start removing points
    newgr = 0
    for i in range(nTrial):
        newgr = ROOT.TGraph()
        hDistFitGraph.Reset()
        print "trial",str(i)
        for r in sorted(newdnll_r):
            #print "x, y = %.3f, %.3f" % (r,newdnll_r[r]) 
            hDistFitGraph.Fill(abs(fdef.Eval(r)-dnll_r[r]))
        mean = hDistFitGraph.GetMean()
        stddev = hDistFitGraph.GetStdDev()
        if verbose: print "mean dist: %.3f, rms: %.3f " % (mean,stddev)
        for r in newdnll_r.keys():
            if abs(fdef.Eval(r)-newdnll_r[r]) > (mean+stddev): del newdnll_r[r]
        keys = newdnll_r.keys()
        for point,r in enumerate(sorted(keys)):
            newgr.SetPoint(point,r,newdnll_r[r])            
        rmin = min(keys)
        rmax = max(keys)
        newgr.SetMarkerColor(colors[i])
        newgr.SetMarkerStyle(20)
        newgr.Fit(fdef,"0QMFS+","",rmin,rmax)  # do not use original range of the function (no "R" option to Fit), but use [rmin,rmax]

    del hDistFitGraph

    # return dictionary with filtered key and values and final graph
    return newdnll_r,newgr  # pass both (it looks like I cannot reset the number of points in a graph, I have to recreate TGraph, so return also the points, even though I could get them from the graph itself)


if __name__ == "__main__":

    from optparse import OptionParser
    parser = OptionParser(usage="%prog [options] higgsCombineFolder binning")
    parser.add_option('-o','--outdir', dest='outdir', default='./', type='string', help='output directory')
    parser.add_option('-n','--n-points', dest='npoints', default=0, type='int', help='Number of points used for the scan')
    parser.add_option('-g','--min-good-points', dest='minGoodPoints', default=0, type='int', help='Number of minimum points not to skip scan (useful with --maxDNLL)')
    parser.add_option('-r','--range-scan', dest='rangescan', default="0.9,1.1", type='string', help='Range used for scan of r (two value separated by comma)')
    parser.add_option(     '--min-bin', dest='minbin', default=1, type='int', help='minimum bin number when selecting bin range for the scans')
    parser.add_option(     '--max-bin', dest='maxbin', default=0, type='int', help='max bin number when selecting bin range for the scans (0 for up to the last one)')
    parser.add_option("-f", "--flavour", dest="flavour", type="string", default='el', help="Channel: either 'el' or 'mu'");
    parser.add_option("-c", "--charge", dest="charge", type="string", default='plus', help="Charge: either 'plus' or 'minus'");
    parser.add_option(      "--scan-fit-opt", dest="scanFitOpt", type="string", default='QMFS+', help="Options passed to TGraph::Fit for the scan fit");
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
    etabinning = getArrayParsingString(etabinning, makeFloat=True)
    ptbinning = getArrayParsingString(ptbinning, makeFloat=True)
    # tmpbinning = [float(x) for x in etabinning]  ## needed for constructor of TH2 below
    #etabinning = tmpbinning
    # tmpbinning = [float(x) for x in ptbinning]
    #ptbinning = tmpbinning 
    nptbins = len(ptbinning)-1
    netabins = len(etabinning)-1
    nBinsInTemplate = (netabins)*(nptbins)
    print "eta binning " + str(etabinning)
    print "pt  binning " + str(ptbinning)
    print "%d eta bins and %d pt bins (%d in total)" % (netabins, nptbins, nBinsInTemplate)

    files = [ f for f in os.listdir(inputdir) if f.endswith('.root') and f.startswith('higgsCombine')]
    files = list( [os.path.join(inputdir, f) for f in files] ) 
    #files = [inputdir + "higgsCombine_Wplus_bin365.MultiDimFit.mH120.root"]

    h2_npoints = ROOT.TH2D("h2_npoints","",netabins, array('d',etabinning), nptbins, array('d',ptbinning))
    h2_nPointsBelowMaxDNLL = ROOT.TH2D("h2_nPointsBelowMaxDNLL","",netabins, array('d',etabinning), nptbins, array('d',ptbinning))
    h2_rMinFit = ROOT.TH2D("h2_rMinFit","",netabins, array('d',etabinning), nptbins, array('d',ptbinning))
    h2_r1sigmaDn = ROOT.TH2D("h2_r1sigmaDn","",netabins, array('d',etabinning), nptbins, array('d',ptbinning))
    h2_r1sigmaUp = ROOT.TH2D("h2_r1sigmaUp","",netabins, array('d',etabinning), nptbins, array('d',ptbinning))
    h2_r1sigmaUpDnMean = ROOT.TH2D("h2_r1sigmaUpDnMean","",netabins, array('d',etabinning), nptbins, array('d',ptbinning))  #(Up+Dn)/2 - 1 (0 if symmetric)
    h2_r1sigmaUpDnDiff = ROOT.TH2D("h2_r1sigmaUpDnDiff","",netabins, array('d',etabinning), nptbins, array('d',ptbinning))  #(Up-Dn)  (0 if symmetric)

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
        # match bin number (expected to be the first integer in the name (a second one will be the mass passed to -m n combine)
        globalbin = re.findall(r'\d+', rootfile)
        # print globalbin
        globalbin = int(globalbin[0])
        # get eta.pt bin 
        etabin,ptbin = getXYBinsFromGlobalBin(globalbin,netabins,False) ## indices from 1 in both input and output, usable for TH2::GetBinContent
        etal = h2_npoints.GetXaxis().GetBinLowEdge(etabin)
        etah = h2_npoints.GetXaxis().GetBinLowEdge(etabin+1)
        ptl  = h2_npoints.GetYaxis().GetBinLowEdge(ptbin)
        pth  = h2_npoints.GetYaxis().GetBinLowEdge(ptbin+1)
        print "Global bin = %d    eta,pt bin= %d,%d (indices from 1)"  % (globalbin,etabin,ptbin)
        print "Eta in [%.3g, %.3g] --- Pt in [%.0f, %.0f]"  % (etal,etah,ptl,pth)


        # Open root file and get limit tree
        dnll_r = {}
        tf = ROOT.TFile(f, 'READ')
        tree = tf.Get("limit")
        if not tree:
            print "Warning: tree named 'limit' not found in file",rootfile
            print "Skipping and continuing"
            nMissingTree += 1
            continue
        # build dictionary with r and 2*deltaNLL, exclude some points
        nVarPoints = tree.GetEntries() - 1
        for entry in tree:
            r = tree.r
            dnll = 2. * tree.deltaNLL
            #print "r=%.3f   2*dNLL=%.3f" % (r, dnll)
            if ((dnll <= options.maxDNLL and dnll >= options.minDNLL) or r == 1.0): 
                dnll_r[r] = dnll
        tf.Close()

        keys = dnll_r.keys()
        firstPointFound = False
        tmpPoints = [x for x in sorted(keys)]
        nPointsBelowMaxDNLL = len(tmpPoints)
        gr_xmin = tmpPoints[0]
        gr_xmax = tmpPoints[-1]
        # xminfit = float(options.rangescan.split(',')[0])
        # xmaxfit = float(options.rangescan.split(',')[1])
        xminfit = gr_xmin
        xmaxfit = gr_xmax

        c = ROOT.TCanvas("c","",700,600)
        c.cd()
        c.SetTickx(1)
        c.SetTicky(1)
        c.cd()
        c.SetFillColor(0)
        c.SetGrid()
        c.SetLeftMargin(0.14)

        gr = ROOT.TGraph()
        for i,r in enumerate(sorted(keys)):
            #print "Adding point %f   %f to graph" % (r,dnll_r[r])
            gr.SetPoint(i, r, dnll_r[r])
            # save x of first value with ordinate < options.maxDNLL, also used for fit below
            if (not firstPointFound and dnll_r[r] <= options.maxDNLL and dnll_r[r] >= options.minDNLL): 
                xminfit = 0.99 * gr_xmin
                xmaxfit = 1.01 * gr_xmax
                firstPointFound = True

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
        maxStoredValDNLL = max(dnll_r[r] for r in dnll_r)
        gr.GetYaxis().SetRangeUser(-0.1,1.2*min(options.maxDNLL,maxStoredValDNLL))

        # very first fit with pol9 (random, just need something that follows the points, to create the spline)
        f1 = ROOT.TF1("f1","pol9") # symmetric range in r
        gr.Fit(f1,"0"+options.scanFitOpt,"",xminfit,xmaxfit)  # option 0 not to draw fitted function 
        fit = gr.GetFunction("f1")
        # fit.SetLineWidth(3)
        # fit.SetLineColor(ROOT.kOrange+2)
        # fit.SetFillColor(ROOT.kOrange+2)
        # fit.SetMarkerColor(ROOT.kOrange+2)

        spl = ROOT.TSpline3("spline3",gr,"b1e1",fit.Derivative(gr_xmin),fit.Derivative(gr_xmax))   # "b1e1" gives first derivative at beginning and end point
        spl.SetLineWidth(3)
        spl.SetLineColor(ROOT.kOrange+2)
        #spl.SetFillColor(ROOT.kOrange+2)
        spl.SetMarkerColor(ROOT.kOrange+2)
        spl.Draw("pclsame")

        mypol2 = ROOT.TF1("mypol2","[0]*(x-1)**2");  # a*(x-1)^2 is a parabola centered at x = 1, with minimum at 0
        mypol2.SetParameter(0,300)  # we would expect that for x = 0.9 it is roughly 2*deltaNLL=3
        mypol2.SetParLimits(0,0.1,600) 
        gr.Fit("mypol2","0"+options.scanFitOpt,"",xminfit,xmaxfit) 
        mypol2 = gr.GetFunction("mypol2") # .Clone("mypol2_init")
        mypol2.SetLineWidth(3)
        mypol2.SetLineColor(ROOT.kBlack)        
        mypol2.SetFillColor(ROOT.kBlack)        
        mypol2.SetMarkerColor(ROOT.kBlack)        
        mypol2.DrawCopy("CSAME")   # use DrawCopy because we are going to use mypol2 again for fit later, with less points (otherwise the previously plotted fits are modified)

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
        
        hDistFitGraph = ROOT.TH1D("hDistFitGraph","",100,0,options.maxDNLL)
        nTrial = 3
        colors = [ROOT.kRed, ROOT.kGreen+2, ROOT.kAzure+2]  #  , ROOT.kViolet,ROOT.kOrange+1]  # make it with at least nTrial colors
        newdnll_r = dict(dnll_r)
        graphs = {}
        flist = []
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
            rmin = min(keys)
            rmax = max(keys)
            graphs[name].SetMarkerColor(colors[i])
            graphs[name].SetMarkerStyle(20)
            graphs[name].Draw("P SAME")
            graphs[name].Fit(mypol2,"0"+options.scanFitOpt,"",rmin,rmax)         
            func = graphs[name].GetFunction("mypol2")         
            func.SetLineColor(colors[i])
            func.SetFillColor(colors[i])
            func.SetMarkerColor(colors[i])
            flist.append(func.DrawCopy("CSAME"))
            
        del hDistFitGraph

        #newdnll_r,flist = filterBadScanPoints(gr, dnll_r, mypol2, canvas=c, nTrial=3, options=options)
        #func = flist[-1]

        # newdnll_r = {}
        # newgr = 0
        # newdnll_r,newgr = filterBadScanPoints(gr, dnll_r, mypol2, nTrial=3, maxDNLL=10.0, verbose=False)
        # newgr.Draw("PSAME")
        # newgr.SetMarkerColor(ROOT.kGreen+2)
        # newgr.SetLineColor(ROOT.kGreen+2)
        # newgr.SetFillColor(ROOT.kGreen+2)
        # func = mypol2

        finalkeys = sorted(newdnll_r.keys())
        finalxmin = finalkeys[0]
        finalxmax = finalkeys[-1]
        # takes some interesting parameters from pol9 fit (could use the spline)
        # generally, for good scans, which are the majority, there is no need to filter points away, because they already behave sensibly
        r1sigmaDn = fit.GetX(1.0, 0.5, 1)  # last two arguments are the x range where to look for
        r1sigmaUp = fit.GetX(1.0, 1, 1.5)
        rMinFit = fit.GetMinimumX(0.95, 1.05)  # 1 by definition if we use mypol2 because we forced mypol2 to pass through (1,0), otherwise can be any value around 1
        print "Bin %d --> Fit: rmin = %.3f    +/- 1 sigma range = [%.3f, %.3f]" % (globalbin, rMinFit, r1sigmaDn, r1sigmaUp)

        leg = ROOT.TLegend(0.30, 0.48, 0.7, 0.87)
        leg.SetFillColor(0)
        leg.SetFillStyle(0)
        leg.SetBorderSize(0)
        chLeg = 'W^{+}' if charge == "plus" else 'W^{-}'
        flLeg = 'e' if flavour == "el" else "#mu"
        leg.SetHeader("Channel: {ch} #rightarrow {fl}#nu".format(ch=chLeg, fl=flLeg) )
        leg.AddEntry(gr , "scan: 1 + %d/%d points" % (nVarPoints,options.npoints), 'P')
        #leg.AddEntry(fit, "fit with pol9", 'LF')
        leg.AddEntry(spl, "TSpline3", 'LF')
        leg.AddEntry(mypol2, "first fit: y = a#dot(x-1)^{2}", "LF")
        for i in range(len(flist)):
            leg.AddEntry(flist[i], "trial %d: y = a#dot(x-1)^{2}" % (i+1), "LF")
        leg.AddEntry(0, "r(min) = %.3f" % rMinFit, '')
        leg.AddEntry(0, "r(-1#sigma) = %.3f" % r1sigmaDn, '')
        leg.AddEntry(0, "r(+1#sigma) = %.3f" % r1sigmaUp, '')
        leg.Draw('same')    

        c.RedrawAxis("sameaxis")
        if not options.nosavescan:
            for ext in ['png', 'pdf']:
                c.SaveAs('{od}/deltaNll_bin{bin}_{ch}.{ext}'.format(od=outdir, bin=globalbin, ch=charge, ext=ext))

        
        sigmaUp = r1sigmaUp - rMinFit
        sigmaDn = rMinFit - r1sigmaDn
        if options.minGoodPoints and nPointsBelowMaxDNLL >= options.minGoodPoints:
            h2_npoints.SetBinContent(etabin,ptbin,nVarPoints)
            h2_nPointsBelowMaxDNLL.SetBinContent(etabin,ptbin,nPointsBelowMaxDNLL)
            h2_rMinFit.SetBinContent(etabin,ptbin,rMinFit)
            h2_r1sigmaDn.SetBinContent(etabin,ptbin,sigmaDn)
            h2_r1sigmaUp.SetBinContent(etabin,ptbin,sigmaUp)
            h2_r1sigmaUpDnMean.SetBinContent(etabin,ptbin,((r1sigmaUp+r1sigmaDn)/2. -rMinFit))
            h2_r1sigmaUpDnDiff.SetBinContent(etabin,ptbin,sigmaUp - sigmaDn) 

        ### end of loop on bins
        #newdnll_r.clear()
        #del flist
        #del graphs  # don't delete, trhows seg.fault
        #del gr      # don't delete, trhows seg.fault
        #del leg
        #del c

        print "============================================"
        print "Done with file", rootfile
        print "============================================"
        print ""

    h2list = []
    
    h2list.append(h2_npoints)
    h2list.append(h2_nPointsBelowMaxDNLL)
    h2list.append(h2_rMinFit)
    h2list.append(h2_r1sigmaDn)
    h2list.append(h2_r1sigmaUp)
    h2list.append(h2_r1sigmaUpDnMean)
    h2list.append(h2_r1sigmaUpDnDiff)

    h2_npoints.GetZaxis().SetTitle("Successful scans::0.5,%f" % (0.5+float(options.npoints)))
    h2_nPointsBelowMaxDNLL.GetZaxis().SetTitle("scans with 2*#DeltaNLL < %.1f::0.5,%f" % (options.maxDNLL,0.5+float(options.npoints)))
    h2_rMinFit.GetZaxis().SetTitle("r minimum from fit::0.98,1.02")
    h2_r1sigmaDn.GetZaxis().SetTitle("r(-1#sigma)::0.0,0.15")
    h2_r1sigmaUp.GetZaxis().SetTitle("r(+1#sigma)::0.0,0.15")
    h2_r1sigmaUpDnMean.GetZaxis().SetTitle("[r(+1#sigma) + r(-1#sigma)] / 2 - r(min)::-0.15,0.15")
    h2_r1sigmaUpDnDiff.GetZaxis().SetTitle("#sigma(Up) - #sigma(Down)::-0.1,0.1")
    adjustSettings_CMS_lumi()

    lepton = "electron" if flavour == "el" else "muon"
    for h in h2list:
        h.SetStats(0)
        xname = "%s #eta" % lepton
        yname = "%s p_{T}" % lepton
        zname = h.GetZaxis().GetTitle()

        # following function will make some warnings appear
        # TCanvas::Constructor:0: RuntimeWarning: Deleting canvas with same name: canvas
        # see also https://root-forum.cern.ch/t/segfault-in-batch-mode-root-groot-setbatch-true/24180/8

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
