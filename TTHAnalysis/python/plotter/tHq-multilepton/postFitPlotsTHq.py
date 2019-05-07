#!/usr/bin/env python
import ROOT
ROOT.gROOT.SetBatch(True)

from math import sqrt
from os.path import dirname,basename
import os
import CMGTools.TTHAnalysis.plotter.mcPlots as mcP
from CMGTools.TTHAnalysis.plotter.mcAnalysis import MCAnalysis
from CMGTools.TTHAnalysis.plotter.tree2yield import PlotSpec

from CMGTools.TTHAnalysis.plotter.histoWithNuisances import HistoWithNuisances

# RARES = ["ZZTo4L","WWW","WWZ","WZZ","ZZZ","TTTT",
#          "tZq_ll_ext_highstat","tWll",
#          "DYJetsToLL_M10to50_LO",
#          "DYJetsToLL_M50_LO_ext_part1",
#          "DYJetsToLL_M50_LO_ext_part2",
#          "DYJetsToLL_M50_LO_ext_part3",
#          "WpWpJJ", "WWDouble"]
RARES = [ "Rares", "WWss", "Gstar" ]

mergeMap = {
    "ttH_hww" : "ttH",
    "ttH_htt" : "ttH",
    "ttH_hzz" : "ttH",
    "tHq_hww" : "tHq",
    "tHq_htt" : "tHq",
    "tHq_hzz" : "tHq",
    "tHW_hww" : "tHW",
    "tHW_htt" : "tHW",
    "tHW_hzz" : "tHW",
}
mergeMap.update({k:'ZZ' for k in RARES})

PROC_TO_PLOTHIST = {
# processes defined for the fit, but not in the plot should take the
# colors etc. from these other processes
    'Rares'   : 'ZZ',
    'WWss'    : 'ZZ',
    'tHq_hww' : 'tHq',
    'tHq_htt' : 'tHq',
    'tHq_hzz' : 'tHq',
    'tHW_hww' : 'tHW',
    'tHW_htt' : 'tHW',
    'tHW_hzz' : 'tHW',
    'ttH_hww' : 'ttH',
    'ttH_htt' : 'ttH',
    'ttH_hzz' : 'ttH',
}

rank = {
    'WWqq'       : 0,
    'VV'         : 0,
    'WZ'         : 1,
    'Others'     : 1,
    'ttGStar'    : 2,
    'ttG'        : 3,
    'ttZ'        : 4,
    'ttW'        : 5,
    'ttH'        : 6,
    'RareSM'     : 7,
    'QF_data'    : 8,
    'FR_data'    : 9,
    'Fakes'      : 9,
    'tHW_htt'    : 100,
    'tHW_hww'    : 101,
    'tHW_hzz'    : 102,
    'tHq_htt'    : 200,
    'tHq_hww'    : 201,
    'tHq_hzz'    : 202,
    'background' : 1001,
    'signal'     : 1002,
    'data'       : 1003
}

YAXIS_RANGE = { # For log plots
    'tHq_3l_13TeV'      : (0.05,200),
    'tHq_2lss_mm_13TeV' : (0.6, 200),
    'tHq_2lss_em_13TeV' : (0.8, 400),
    'tHq_2lss_ee_13TeV' : (0.5, 70),
}

CHANNEL_LABELS = {
    'tHq_3l_13TeV'      : "3 leptons",
    'tHq_2lss_mm_13TeV' : "#mu^{#pm}#mu^{#pm}",
    'tHq_2lss_em_13TeV' : "e^{#pm}#mu^{#pm}",
    'tHq_2lss_ee_13TeV' : "e^{#pm}e^{#pm}"
}

REBINMAP_3l = {7:9, 2:5, 9:7, 5:2}
REBINMAP_2l = {3:2, 2:4, 5:3, 4:8, 6:5, 9:6, 8:10, 10:9}

from plotTHQ import LABELS

AXISLABEL = 'Combined BDT bin'

def doTinyCmsPrelim(textLeft="_default_",
                    textRight="_default_",
                    hasExpo=False,
                    textSize=0.033,
                    lumi=None,
                    xoffs=0,
                    options=None,
                    doWide=False,
                    ypos=0.955):
    if textLeft  == "_default_": textLeft  = options.lspam
    if textRight == "_default_": textRight = options.rspam
    if lumi      == None       : lumi      = options.lumi
    if   lumi > 3.54e+1: lumitext = "%.0f fb^{-1}" % lumi
    elif lumi > 3.54e+0: lumitext = "%.1f fb^{-1}" % lumi
    elif lumi > 3.54e-1: lumitext = "%.2f fb^{-1}" % lumi
    elif lumi > 3.54e-2: lumitext = "%.0f pb^{-1}" % (lumi*1000)
    elif lumi > 3.54e-3: lumitext = "%.1f pb^{-1}" % (lumi*1000)
    else               : lumitext = "%.2f pb^{-1}" % (lumi*1000)
    lumitext = "%.1f fb^{-1}" % lumi
    textLeft = textLeft.replace("%(lumi)",lumitext)
    textRight = textRight.replace("%(lumi)",lumitext)
    if textLeft not in ['', None]:
        mcP.doSpam(textLeft, (.28 if hasExpo else 0.07 if doWide else .17)+xoffs,
                   ypos, .60+xoffs, ypos+0.04, align=12, textSize=textSize)
    if textRight not in ['', None]:
        mcP.doSpam(textRight, (0.6 if doWide else .68)+xoffs,
                   ypos, .99+xoffs, ypos+0.04, align=32, textSize=textSize)

legend_ = None
def doLegend(pmap, mca,
             corner="TR",
             textSize=0.035,
             cutoff=1e-2,
             cutoffSignals=True,
             mcStyle="F",
             legWidth=0.18,
             legBorder=True,
             signalPlotScale=None,
             totalError=None,
             header="",
             doWide=False,
             nColumns=1,
             xy=None):
        if (corner == None): return
        total = sum([x.Integral() for x in pmap.itervalues()])
        sigEntries = []; bgEntries = []
        for p in mca.listSignals(allProcs=True):
            if mca.getProcessOption(p,'HideInLegend',False): continue
            if p in pmap and pmap[p].Integral() > (cutoff*total if cutoffSignals else 0): 
                lbl = mca.getProcessOption(p,'Label',p)
                if signalPlotScale and signalPlotScale!=1: 
                    lbl=lbl+" x "+("%d"%signalPlotScale if floor(signalPlotScale)==signalPlotScale else "%.2f"%signalPlotScale)
                myStyle = mcStyle if type(mcStyle) == str else mcStyle[0]
                sigEntries.append( (pmap[p],lbl,myStyle) )
        backgrounds = mca.listBackgrounds(allProcs=True)
        for p in backgrounds:
            if mca.getProcessOption(p,'HideInLegend',False): continue
            if p in pmap and pmap[p].Integral() >= cutoff*total: 
                lbl = mca.getProcessOption(p,'Label',p)
                myStyle = mcStyle if type(mcStyle) == str else mcStyle[1]
                bgEntries.append( (pmap[p],lbl,myStyle) )
        nentries = len(sigEntries) + len(bgEntries) + ('data' in pmap)

        nentries = nentries/nColumns

        if xy:
            (x1, y1, x2, y2) = xy
        else:
            (x1, y1, x2, y2) = (0.97-legWidth if doWide else .90-legWidth,
                                  .7-textSize*max(nentries-3,0), .90, .91)
            if corner == "TR":
                (x1,y1,x2,y2) = (0.97-legWidth if doWide else .90-legWidth, .7 - textSize*max(nentries-3,0), .90, .91)
            elif corner == "TC":
                (x1,y1,x2,y2) = (.5, .70 - textSize*max(nentries-3,0), .5+legWidth, .91)
            elif corner == "TL":
                (x1,y1,x2,y2) = (.2, .70 - textSize*max(nentries-3,0), .2+legWidth, .91)
            elif corner == "BR":
                (x1,y1,x2,y2) = (.85-legWidth, .33 + textSize*max(nentries-3,0), .90, .15)
            elif corner == "BC":
                (x1,y1,x2,y2) = (.5, .33 + textSize*max(nentries-3,0), .5+legWidth, .15)
            elif corner == "BL":
                (x1,y1,x2,y2) = (.2, .27 + textSize*max(nentries-3,0), .2+legWidth, .09)

        leg = ROOT.TLegend(x1,y1,x2,y2)
        leg.SetNColumns(nColumns)
        if header: leg.SetHeader(header.replace("\#", "#"))
        leg.SetFillColor(0)
        leg.SetShadowColor(0)
        if header: leg.SetHeader(header.replace("\#", "#"))       
        if not legBorder:
            leg.SetLineColor(0)
        leg.SetTextFont(43)
        leg.SetTextSize(18)
        if 'data' in pmap: 
            leg.AddEntry(pmap['data'], mca.getProcessOption('data','Label','Data', noThrow=True), 'LPE')
        total = sum([x.Integral() for x in pmap.itervalues()])
        for (plot,label,style) in sigEntries: leg.AddEntry(plot,label,style)
        for (plot,label,style) in  bgEntries: leg.AddEntry(plot,label,style)
        if totalError: leg.AddEntry(totalError,"total bkg. unc.","F") 
        leg.Draw()
        ## assign it to a global variable so it's not deleted
        global legend_
        legend_ = leg 
        return leg

def doRatioHistsCustom(pspec, pmap, total, maxRange,
                       fixRange=False,
                       fitRatio=None,
                       errorsOnRef=True,
                       ratioNums="signal",
                       ratioDen="background",
                       ylabel="Data/pred.",
                       doWide=False,
                       showStatTotLegend=False):
    numkeys = [ "data" ]
    if "data" not in pmap: 
        if len(pmap) >= 4 and ratioDen in pmap:
            numkeys = []
            for p in pmap.iterkeys():
                for s in ratioNums.split(","):
                    if re.match(s,p): 
                        numkeys.append(p)
                        break
            if len(numkeys) == 0:
                return (None,None,None,None)
            # do this first
            total.GetXaxis().SetLabelOffset(999) ## send them away
            total.GetXaxis().SetTitleOffset(999) ## in outer space
            total.GetYaxis().SetTitleSize(26)
            total.GetYaxis().SetTitleOffset(0.75 if doWide else 1.0) # was 1.48
            total.GetYaxis().SetLabelSize(0.05)
            total.GetYaxis().SetLabelOffset(0.007)
            # then we can overwrite total with background
            numkey = 'signal'
            total     = pmap[ratioDen]
        else:    
            return (None,None,None,None)
    ratios = [] #None
    for numkey in numkeys:
        if hasattr(pmap[numkey], 'poissonGraph'):
            ratio = pmap[numkey].poissonGraph.Clone("data_div"); 
            for i in xrange(ratio.GetN()):
                x    = ratio.GetX()[i]
                div  = total.GetBinContent(total.GetXaxis().FindBin(x))
                ratio.SetPoint(i, x, ratio.GetY()[i]/div if div > 0 else 0)
                ratio.SetPointError(i, ratio.GetErrorXlow(i), ratio.GetErrorXhigh(i), 
                                       ratio.GetErrorYlow(i)/div  if div > 0 else 0, 
                                       ratio.GetErrorYhigh(i)/div if div > 0 else 0) 
        else:
            ratio = pmap[numkey].Clone("data_div"); 
            ratio.Divide(total.raw())
        ratios.append(ratio)
    unity  = total.raw().Clone("sim_div");
    unityErr  = total.graphAsymmTotalErrors(relative=True)
    unityErr0 = total.graphAsymmTotalErrors(toadd=[],relative=True)
    rmin, rmax =  1,1
    for b in xrange(1,unity.GetNbinsX()+1):
        e,n = unity.GetBinError(b), unity.GetBinContent(b)
        unity.SetBinContent(b, 1 if n > 0 else 0)
        unity.SetBinError(b, 0)
        if not errorsOnRef:
            raise RuntimeError("Not implemented yet with histoWithNuisances")
    rmin = min(1-2*unityErr.GetErrorYlow(b)  for b in xrange(unityErr.GetN())) if unityErr.GetN() else 1
    rmax = max(1+2*unityErr.GetErrorYhigh(b) for b in xrange(unityErr.GetN())) if unityErr.GetN() else 1
    for ratio in ratios:
        if ratio.ClassName() != "TGraphAsymmErrors":
            for b in xrange(1,unity.GetNbinsX()+1):
                if ratio.GetBinContent(b) == 0: continue
                rmin = min( rmin, ratio.GetBinContent(b) - 2*ratio.GetBinError(b) )
                rmax = max( rmax, ratio.GetBinContent(b) + 2*ratio.GetBinError(b) )
        else:
            for i in xrange(ratio.GetN()):
                rmin = min( rmin, ratio.GetY()[i] - 2*ratio.GetErrorYlow(i)  )
                rmax = max( rmax, ratio.GetY()[i] + 2*ratio.GetErrorYhigh(i) )
    if rmin < maxRange[0] or fixRange: rmin = maxRange[0]; 
    if rmax > maxRange[1] or fixRange: rmax = maxRange[1];
    if (rmax > 3 and rmax <= 3.4): rmax = 3.4
    if (rmax > 2 and rmax <= 2.4): rmax = 2.4
    unity.SetFillStyle(3244);
    unity.SetFillColor(ROOT.kGray+2)
    unity.SetMarkerStyle(0)
    unityErr.SetFillStyle(1001);
    unityErr.SetFillColor(ROOT.kCyan);
    unityErr.SetMarkerStyle(1);
    unityErr.SetMarkerColor(ROOT.kCyan);
    unityErr0.SetFillStyle(1001);
    unityErr0.SetFillColor(ROOT.kBlue-7);
    unityErr0.SetMarkerStyle(1);
    unityErr0.SetMarkerColor(ROOT.kBlue-7);
    ROOT.gStyle.SetErrorX(0.5);
    unity.Draw("AXIS");
    if errorsOnRef:
        unityErr.Draw("E2");
    if fitRatio != None and len(ratios) == 1:
        from CMGTools.TTHAnalysis.tools.plotDecorations import fitTGraph
        fitTGraph(ratio,order=fitRatio)
        unityErr.SetFillStyle(3013);
        unityErr0.SetFillStyle(3013);
        if errorsOnRef:
            unityErr0.Draw("E2 SAME");
    else:
        if errorsOnRef:
            unityErr0.Draw("E2 SAME");
    unity.Draw("AXIS SAME");
    rmin = float(pspec.getOption("RMin",rmin))
    rmax = float(pspec.getOption("RMax",rmax))
    unity.GetYaxis().SetRangeUser(rmin,rmax);
    unity.GetXaxis().SetTitleFont(43)
    unity.GetXaxis().SetTitleSize(26)
    unity.GetXaxis().SetTitleOffset(2.9)
    unity.GetXaxis().SetLabelFont(43)
    unity.GetXaxis().SetLabelSize(22)
    unity.GetXaxis().SetLabelOffset(0.007)
    unity.GetYaxis().SetNdivisions(505)
    unity.GetYaxis().SetTitleFont(43)
    unity.GetYaxis().SetTitleSize(26)
    unity.GetYaxis().SetTitleOffset(1.8)
    unity.GetYaxis().SetLabelFont(43)
    unity.GetYaxis().SetLabelSize(22)
    unity.GetYaxis().SetLabelOffset(0.007)
    unity.GetYaxis().SetDecimals(True) 
    unity.GetYaxis().SetTitle(ylabel)
    total.GetXaxis().SetLabelOffset(999) ## send them away
    total.GetXaxis().SetTitleOffset(999) ## in outer space
    total.GetYaxis().SetTitleFont(43)
    total.GetYaxis().SetTitleSize(26)
    total.GetYaxis().SetTitleOffset(1.8)
    total.GetYaxis().SetLabelFont(43)
    total.GetYaxis().SetLabelSize(22)
    total.GetYaxis().SetLabelOffset(0.007)
    binlabels = pspec.getOption("xBinLabels","")
    if binlabels != "" and len(binlabels.split(",")) == unity.GetNbinsX():
        blist = binlabels.split(",")
        for i in range(1,unity.GetNbinsX()+1): 
            unity.GetXaxis().SetBinLabel(i,blist[i-1]) 
        unity.GetXaxis().SetLabelSize(0.15)
    #ratio.SetMarkerSize(0.7*ratio.GetMarkerSize()) # no it is confusing
    binlabels = pspec.getOption("xBinLabels","")
    if binlabels != "" and len(binlabels.split(",")) == unity.GetNbinsX():
        blist = binlabels.split(",")
        for i in range(1,unity.GetNbinsX()+1): 
            unity.GetXaxis().SetBinLabel(i,blist[i-1]) 
    #$ROOT.gStyle.SetErrorX(0.0);
    line = ROOT.TLine(unity.GetXaxis().GetXmin(),1,unity.GetXaxis().GetXmax(),1)
    line.SetLineWidth(1);
    line.SetLineColor(1);
    line.Draw("L")
    for ratio in ratios:
        ratio.Draw("E SAME" if ratio.ClassName() != "TGraphAsymmErrors" else "PZ SAME");
    leg0 = ROOT.TLegend(0.12 if doWide else 0.2, 0.8, 0.25 if doWide else 0.45, 0.9)
    leg0.SetFillColor(0)
    leg0.SetShadowColor(0)
    leg0.SetLineColor(0)
    leg0.SetTextFont(43)
    leg0.SetTextSize(18)
    leg0.AddEntry(unityErr0, "stat. unc.", "F")
    # if showStatTotLegend: leg0.Draw()
    leg1 = ROOT.TLegend(0.2, 0.8, 0.5, 0.9)
    leg1.SetFillColor(0)
    leg1.SetShadowColor(0)
    leg1.SetLineColor(0)
    leg1.SetTextFont(43)
    leg1.SetTextSize(18)
    leg1.AddEntry(unityErr, "Total uncertainty", "F")
    if showStatTotLegend: leg1.Draw()
    global legendratio0_, legendratio1_
    legendratio0_ = leg0
    legendratio1_ = leg1
    return (ratios, unity,(unityErr,unityErr0), line)

options = None
if __name__ == "__main__":
    from optparse import OptionParser
    usage="%prog [options] mcaplot.txt mcafit.txt infile.root mlfile.root channel"
    parser = OptionParser(usage=usage)
    mcP.addPlotMakerOptions(parser)
    parser.add_option("--outDir", dest="outDir", type="string",
                      default="postFitPlots/",
                      help="Output directory for postfit plots");
    parser.add_option("--doLog", dest="doLog", action="store_true",
                      help="Do logarithmic scale plots");
    parser.add_option("--bkgSub", dest="bkgSub", action="store_true",
                      help="Subtract backgrounds");
    parser.add_option("--doRebinning", dest="doRebinning", action="store_true",
                      help="Remap the bins according to PR#18");
    (options, args) = parser.parse_args()
    #options.path = ["thqtrees/TREES_TTH_250117_Summer16_JECV3_noClean_qgV2_tHqsoup_v2/"]
    options.path = ["skimtrees/"]
    options.lumi = 41.5
    options.poisson = True

    # options.lspam = 'CMS'

    try: os.makedirs(options.outDir)
    except OSError: pass

    os.system("cp /afs/cern.ch/work/p/pdas/www/index.php "+options.outDir)

    mca_merged = MCAnalysis(args[0], options) # for the merged processes (plots)
    mca_indivi = MCAnalysis(args[1], options) # for the individual processes (fit)
    print args[1]
    channel = {'3l': 'tHq_3l_13TeV', 
               '2lss_mm':'tHq_2lss_mm_13TeV',
               '2lss_em':'tHq_2lss_em_13TeV',
               '2lss_ee':'tHq_2lss_ee_13TeV'}[args[4]]
    rebinmap = REBINMAP_3l if '3l' in channel else REBINMAP_2l

    var = "finalBins_60"

    if args[4].rsplit('_',1)[0] not in args[2]: # channel not in filename is suspicious
        print "WARNING"

    infile = ROOT.TFile(args[2])
    datahistname = "_data"
    hdata  = infile.Get(var+datahistname)
    try:
        hdata.GetName()
    except ReferenceError:
        raise RuntimeError("Histo %s not found in %s" % (var+datahistname, args[2]))

    hdata_rebinned = hdata.Clone("%s_rebinned"%hdata.GetName())
    hdata_rebinned.Reset("ICE")
    for b in xrange(1, hdata.GetNbinsX()+1):
        hdata_rebinned.SetBinContent(rebinmap.get(b,b), hdata.GetBinContent(b))
        hdata_rebinned.SetBinError(  rebinmap.get(b,b), hdata.GetBinError(b))
    hdata = hdata_rebinned

    ## Cosmetics
    hdata.SetMarkerSize(1.3)

    mlfile  = ROOT.TFile(args[3])

    ROOT.gROOT.ProcessLine(".x /afs/cern.ch/user/g/gpetrucc/cpp/tdrstyle.cc(0)")
    ROOT.gROOT.ForceStyle(False)
    ROOT.gStyle.SetErrorX(0.5)
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetPaperSize(20.,25.)

    # Adjust label of merged processes
    for process,newlabel in LABELS.iteritems():
        try: mca_merged.setProcessOption(process, 'Label', newlabel)
        except RuntimeError: pass

    ymax = -1
    for MLD in ["prefit", "fit_b", "fit_s"]:
        if not MLD == 'fit_s': continue ## PAS plots only
        if options.bkgSub and MLD == "fit_b": continue
        plots  = {'data' : hdata}
        mldir  = mlfile.GetDirectory("shapes_"+MLD);
        try:
            mldirname = mldir.GetName()
        except ReferenceError:
            print "Could not find directory shapes_%s in %s" %(MLD, args[3])
            exit(-1)

        outfile = ROOT.TFile(os.path.join(options.outDir, "%s_%s.root" % (MLD, channel)), "RECREATE")

        # `processes` should be all the ones defined in the fit (i.e. the second mca)
        processes = list(reversed(mca_indivi.listBackgrounds()))
        thqsigs = ['tHq_hww', 'tHq_htt', 'tHq_hzz']
        thwsigs = ['tHW_hww', 'tHW_htt', 'tHW_hzz']
        tthsigs = ['ttH_hww', 'ttH_htt', 'ttH_hzz']
        processes += tthsigs
        processes += thwsigs
        processes += thqsigs

        # Remove the _promptsub processes
        processes = [p for p in processes if not p.endswith('_promptsub')]

        #for proc in processes:
        #    print proc
        ## HACK
        if '2lss_mm' in channel:
            for removeme in ['Convs','Conversions','data_flips']:
                try: processes.remove(removeme)
                except ValueError: pass

        stack = ROOT.THStack("%s_stack_%s"%(var,MLD),"")

        print infile
        for process in processes:
            print process
            # Get the pre-fit histogram (just for the color etc.)
            hist = infile.Get("%s_%s" % (var, PROC_TO_PLOTHIST.get(process, process)))
            if not hist:
                raise RuntimeError("Missing %s_%s for %s" % (var, process, process))

            hist = hist.Clone(var+"_"+process)
            hist.Reset("ICE")
            hist.SetDirectory(0)

            # Get the post-fit shape
            channel = "thq_3l_13TeV"
            chdir = mldir.GetDirectory("%s" % channel)
            h_postfit = chdir.Get("%s" % process)
            #h_postfit = mldir.Get("%s/%s" % (channel, process))
            print h_postfit.GetName()
            print h_postfit.GetNbinsX()
            if not h_postfit:
                # if process not in mergeMap:
                raise RuntimeError("Could not find shape for %s/%s in dir %s of file %s" % (channel, process, mldir.GetName(), args[3]))

            # Set the bin-content and error from the post-fit
            for b in xrange(1, hist.GetNbinsX()+1):
                hist.SetBinContent(rebinmap.get(b,b), h_postfit.GetBinContent(b))
                hist.SetBinError(rebinmap.get(b,b), h_postfit.GetBinError(b))

            # Add them up to reflect the plotting mca
            if options.bkgSub and process not in thqsigs+thwsigs+tthsigs:
                continue
            pout = mergeMap.get(process, process)
            if pout in plots:
                plots[pout].Add(hist)
            else:
                plots[pout] = hist
                hist.SetName(var+"_"+pout)
                stack.Add(hist) # only add them once to the stack

        htot         = hdata.Clone(var+"_total")
        htot_postfit = mldir.Get(channel+"/total")
        hbkg         = hdata.Clone(var+"_total_background")
        hbkg_postfit = mldir.Get(channel+"/total_background")
        hsig         = hdata.Clone(var+"_total_signal")
        hsig_postfit = mldir.Get(channel+"/total_signal")

        for b in xrange(1, hdata.GetNbinsX()+1):
            htot.SetBinContent(rebinmap.get(b,b), htot_postfit.GetBinContent(b))
            htot.SetBinError(  rebinmap.get(b,b), htot_postfit.GetBinError(b))
            hbkg.SetBinContent(rebinmap.get(b,b), hbkg_postfit.GetBinContent(b))
            hbkg.SetBinError(  rebinmap.get(b,b), hbkg_postfit.GetBinError(b))
            hsig.SetBinContent(rebinmap.get(b,b), hsig_postfit.GetBinContent(b))
            hsig.SetBinError(  rebinmap.get(b,b), hsig_postfit.GetBinError(b))

        if options.bkgSub:
            hdata_bgsub = hdata.Clone("%s_bgsub" % hdata.GetName()) # subtract backgrounds
            hdata_bgsub.Add(hbkg, -1.0)
            hdata_bgsub.SetDirectory(0)
            plots['data'] = hdata_bgsub
        if options.poisson:
            pdata = mcP.getDataPoissonErrors(hdata, True, True)
            hdata.poissonGraph = pdata ## attach it so it doesn't get deleted

        for hist in plots.values() + [htot]:
            outfile.WriteTObject(hist)

        ## Prepare split screen
        c1 = ROOT.TCanvas("c1%s"%MLD, "c1", 600, 750)
        c1.Draw()
        c1.SetWindowSize(600 + (600 - c1.GetWw()), (750 + (750 - c1.GetWh())))
        p1 = ROOT.TPad("pad1","pad1",0,0.29,1,0.99)
        p1.SetTopMargin(0.08)
        p1.SetBottomMargin(0.06)
        p1.Draw()
        p2 = ROOT.TPad("pad2","pad2",0,0,1,0.32)
        p2.SetTopMargin(0.01)
        p2.SetBottomMargin(0.3)
        p2.SetFillStyle(0)
        p2.Draw()
        p1.cd()

        ## Cosmetics (note that these are affected by doRatioHistsCustom below)
        if not options.doLog:
            if ymax < 0: #MLD == 'prefit':
                ymax = 1.2*max(htot.GetMaximum(), hdata.GetMaximum())
            htot.GetYaxis().SetRangeUser(0, ymax)
        else:
            htot.GetYaxis().SetRangeUser(YAXIS_RANGE.get(channel, (0.5, 100))[0],
                                         YAXIS_RANGE.get(channel, (0.5, 100))[1])
        if options.bkgSub:
            if not options.doLog:
                if ymax < 0: #MLD == 'prefit':
                    ymax = max([hdata_bgsub.GetBinContent(b)+hdata_bgsub.GetBinErrorUp(b)  for b in xrange(1,hdata.GetNbinsX())])
                    ymin = min([hdata_bgsub.GetBinContent(b)-hdata_bgsub.GetBinErrorLow(b) for b in xrange(1,hdata.GetNbinsX())])
                    ymax = max(20, 1.2*ymax)
                    ymin = min(-3, 1.5*ymin)
                hsig.GetYaxis().SetRangeUser(ymin, ymax)
            else:
                hsig.GetYaxis().SetRangeUser(0.1, 20)

        htot.GetXaxis().SetTitle(AXISLABEL)
        # htot.GetXaxis().SetNdivisions(510)
        # htot.GetYaxis().SetNdivisions(510)
        htot.GetYaxis().SetTitle('Events/Bin')
        htot.GetYaxis().SetTitleFont(43)
        htot.GetYaxis().SetTitleSize(26)
        htot.GetYaxis().SetTitleOffset(1.8)
        htot.GetYaxis().SetLabelFont(43)
        htot.GetYaxis().SetLabelSize(22)
        htot.GetYaxis().SetLabelOffset(0.007)

        ## Draw absolute prediction in top frame
        if not options.bkgSub:
            htot.Draw("HIST")
            stack.Draw("HIST F SAME")
            htot = HistoWithNuisances(htot)
            totalError = mcP.doShadedUncertainty(htot)
            hdata.poissonGraph.Draw("PZ")
            htot.Draw("AXIS SAME")
        else:
            mca_merged.setProcessOption('data', 'Label', 'Data-Backgr.')
            hsig.Draw("HIST")
            stack.Draw("HIST F SAME")
            hsig = HistoWithNuisances(hsig)
            totalError = mcP.doShadedUncertainty(hsig)
            hdata_bgsub.Draw("PE SAME")
            hsig.Draw("AXIS SAME")

            line = ROOT.TLine(hsig.GetXaxis().GetXmin(),0,hsig.GetXaxis().GetXmax(),0)
            line.SetLineWidth(1)
            line.SetLineColor(1)
            line.Draw("L")

        ## Add prefit signal shape
        thqprefit = infile.Get("%s_tHq" % var).Clone("%s_tHq_prefit"%var)
        thwprefit = infile.Get("%s_tHW" % var).Clone("%s_tHW_prefit"%var)
        thwprefit.Add(thwprefit)
        thqprefit.SetLineWidth(3)
        thqprefit.SetFillStyle(0)
        thqprefit.SetMarkerSize(0)
        thqprefit.SetLineColor(thqprefit.GetFillColor())

        ## Adjust scale
        sigscalefactor = 10
        thqprefit.Scale(float(sigscalefactor))
        thqprefit.Draw("HIST SAME")

        ## Do the legend
        leg = None
        if options.doLog:
            leg = doLegend(plots, mca_merged,
                           textSize=0.042,
                           totalError=None,
                           cutoff=0.01,
                           cutoffSignals=True,
                           legWidth=0.58,
                           legBorder=False,
                           corner='TR',
                           nColumns=2,
                           xy=(.41, .658, .955, .91))
        else:
            leg = doLegend(plots, mca_merged,
                           textSize=0.042,
                           totalError=None,
                           cutoff=0.01 if not options.bkgSub else 0.0,
                           cutoffSignals=not options.bkgSub,
                           legBorder=False,
                           legWidth=0.28)
        leg.AddEntry(totalError, "Total uncertainty","F") 
        leg.AddEntry(thqprefit, "%d#times tH (expected)" % sigscalefactor,"L") 
        
        lspam = options.lspam
        if channel == 'em':
            lspam += r"e^{#pm}#mu^{#pm} channel"
        if channel == 'mm':
            lspam += r"#mu^{#pm}#mu^{#pm} channel"
        if channel == '3l':
            lspam += "3-lepton channel"

        doTinyCmsPrelim(hasExpo = False,
                        textSize=(0.055), xoffs=-0.03,
                        textLeft = lspam, textRight = options.rspam,
                        lumi = options.lumi,
                        ypos=0.935)

        if options.doLog:
            p1.SetLogy(True)

        ## Add labels for each channel
        tlat = ROOT.TLatex()
        tlat.SetNDC(True)
        tlat.SetTextFont(43); tlat.SetTextSize(28);
        tlat.DrawLatex(0.28, 0.82, CHANNEL_LABELS.get(channel, "Undef."))

        ## Do the ratio plot
        ## Draw relative prediction in the bottom frame
        p2.cd()
        rdata,rnorm,(rnorm2,rnorm0),rline = doRatioHistsCustom(PlotSpec(var,var,"",{}),
                                                             plots,
                                                             htot if not options.bkgSub else hsig,
                                                             maxRange=options.maxRatioRange,
                                                             fixRange=options.fixRatioRange,
                                                             fitRatio=options.fitRatio,
                                                             errorsOnRef=options.errorBandOnRatio,
                                                             ratioNums=options.ratioNums,
                                                             ratioDen=options.ratioDen,
                                                             ylabel="Data/Pred." if not options.bkgSub else "(Data-Bkg)/Sig",
                                                             doWide=options.wideplot,
                                                             showStatTotLegend=True)
        rnorm2.Delete()
        rnorm0.Delete()

        # ## Legend for uncertainties
        # leg2 = ROOT.TLegend(x1,y1,x2,y2)
        # leg2.SetFillColor(0)
        # leg2.SetShadowColor(0)
        # leg2.SetLineColor(0)
        # leg2.SetTextFont(43)
        # leg2.SetTextSize(18)
        # leg2.AddEntry(, mca.getProcessOption('data','Label','Data', noThrow=True), 'LPE')

        ## Save the plots
        c1.cd()
        for ext in ['.pdf', '.png', '.C']:
            outname = '%s_%s%s' % (channel,MLD,ext)
            if options.doLog:
                outname = '%s_%s_log%s' % (channel,MLD,ext)
            c1.Print(os.path.join(options.outDir, outname))
        del c1

        outfile.Close()
        ## PLOTTING DONE
        ################

        ## Save the postfit yields also
        dump = open("%s/%s_%s.txt" % (options.outDir,channel,MLD), "w")
        pyields = {
            "background" : [0,0],
            "signal"     : [0,0],
            "data"       : [plots["data"].Integral(), plots["data"].Integral()]
        }
        argset =  mlfile.Get("norm_"+MLD)

        for proc in processes:
            pout = mergeMap.get(proc, proc)
            if pout not in pyields:
                pyields[pout] = (0,0)
            rvar = argset.find("%s/%s" % (channel,proc))
            if not rvar:
                print 'Did not find rvar for %s/%s' % (channel, proc)
                continue
            pyields[pout] = ( pyields[pout][0] + rvar.getVal(),
                              pyields[pout][1] + rvar.getError()**2 ) 
            if pout.startswith('tHq') or pout.startswith('tHW') or pout.startswith('ttH'):
                pyields["signal"] = ( pyields[pout][0] + rvar.getVal(),
                                      pyields[pout][1] + rvar.getError()**2 ) 
            else:
                pyields["background"] = ( pyields[pout][0] + rvar.getVal(),
                                          pyields[pout][1] + rvar.getError()**2 ) 

        for p in pyields.iterkeys():
            pyields[p] = (pyields[p][0], sqrt(pyields[p][1]))

        maxlen = max([len(mca_indivi.getProcessOption(p,'Label',p))
                      for p in mca_indivi.listSignals(allProcs=True) +
                               mca_indivi.listBackgrounds(allProcs=True)]+[7])
        fmt    = "%%-%ds %%6.2f \pm %%5.2f\n" % (maxlen+1)

        all_processes =  mca_indivi.listSignals(allProcs=True)
        all_processes += mca_indivi.listBackgrounds(allProcs=True)
        all_processes += ["background","signal","data"]

        for p in sorted(all_processes+list(set(mergeMap.values())), key=lambda x:rank.get(x,-1)):
            if p not in pyields: continue
            if p in ["background", "data"]:
                dump.write(("-"*(maxlen+45))+"\n");
            label = p.upper()
            try:
                label = mca_indivi.getProcessOption(p,'Label',p)
            except RuntimeError: pass
            dump.write(fmt % ( label, pyields[p][0], pyields[p][1]))

        dump.close()



