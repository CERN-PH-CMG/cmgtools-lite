#!/usr/bin/env python

from CMGTools.WMass.plotter.mcPlots import *

## safe batch mode
## safe batch mode
import sys
args = sys.argv[:]
sys.argv = ['-b']
import ROOT
sys.argv = args
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True

def doStandaloneRatioHists(wplot,zplot,options,maxRange,fixRange=False,fitRatio=None,errorsOnRef=True,ratioNums="signal",ratioDen="background"):
    # do this first
    wplot.GetXaxis().SetLabelOffset(999) ## send them away
    wplot.GetXaxis().SetTitleOffset(999) ## in outer space
    wplot.GetYaxis().SetLabelSize(0.05)
    ratio = wplot.Clone("_".join(wplot.GetName().split("_")[:-1])+"Z_ratio")
    ratio.Divide(zplot)
    unity  = zplot.Clone("z_div");
    rmin, rmax =  1,1
    for b in xrange(1,unity.GetNbinsX()+1):
        e,n = unity.GetBinError(b), unity.GetBinContent(b)
        unity.SetBinContent(b, 1 if n > 0 else 0)
        if errorsOnRef:
            unity.SetBinError(b, e/n if n > 0 else 0)
        else:
            unity.SetBinError(b, 0)
        rmin = min([ rmin, 1-2*e/n if n > 0 else 1])
        rmax = max([ rmax, 1+2*e/n if n > 0 else 1])
    if ratio.ClassName() != "TGraphAsymmErrors":
        for b in xrange(1,unity.GetNbinsX()+1):
            if ratio.GetBinContent(b) == 0: continue
            rmin = min([ rmin, ratio.GetBinContent(b) - 2*ratio.GetBinError(b) ]) 
            rmax = max([ rmax, ratio.GetBinContent(b) + 2*ratio.GetBinError(b) ])  
    else:
        for i in xrange(ratio.GetN()):
            rmin = min([ rmin, ratio.GetY()[i] - 2*ratio.GetErrorYlow(i)  ]) 
            rmax = max([ rmax, ratio.GetY()[i] + 2*ratio.GetErrorYhigh(i) ])  
    if rmin < maxRange[0] or fixRange: rmin = maxRange[0]; 
    if rmax > maxRange[1] or fixRange: rmax = maxRange[1];
    if (rmax > 3 and rmax <= 3.4): rmax = 3.4
    if (rmax > 2 and rmax <= 2.4): rmax = 2.4
    unity.SetFillStyle(1001);
    unity.SetFillColor(ROOT.kCyan);
    unity.SetMarkerStyle(1);
    unity.SetMarkerColor(ROOT.kCyan);
    ROOT.gStyle.SetErrorX(0.5);
    if errorsOnRef:
        unity.Draw("E2");
    else:
        unity.Draw("AXIS");
    if fitRatio != None:
        from CMGTools.TTHAnalysis.tools.plotDecorations import fitTGraph
        fitTGraph(ratio,order=fitRatio)
        unity.SetFillStyle(3013);
        if errorsOnRef:
            unity.Draw("AXIS SAME");
    unity.GetYaxis().SetRangeUser(rmin,rmax);
    unity.GetXaxis().SetTitleSize(0.14)
    unity.GetYaxis().SetTitleSize(0.14)
    unity.GetXaxis().SetLabelSize(0.11)
    unity.GetYaxis().SetLabelSize(0.11)
    unity.GetYaxis().SetNdivisions(505)
    unity.GetYaxis().SetDecimals(True)
    unity.GetYaxis().SetTitle("W/Z")
    unity.GetYaxis().SetTitleOffset(0.52);
    zplot.GetXaxis().SetLabelOffset(999) ## send them away
    zplot.GetXaxis().SetTitleOffset(999) ## in outer space
    zplot.GetYaxis().SetLabelSize(0.05)
    #ratio.SetMarkerSize(0.7*ratio.GetMarkerSize()) # no it is confusing
    #$ROOT.gStyle.SetErrorX(0.0);
    line = ROOT.TLine(unity.GetXaxis().GetXmin(),1,unity.GetXaxis().GetXmax(),1)
    line.SetLineWidth(2);
    line.SetLineColor(58);
    line.Draw("L")
    ratio.Draw("E SAME" if ratio.ClassName() != "TGraphAsymmErrors" else "PZ SAME");
    return (ratio, unity, line)

def printOnePlot(plots,varname,xtitle,options,outputDir=None,printDir=None):
    ROOT.gROOT.ProcessLine(".x tdrstyle.cc")
    ROOT.gROOT.ProcessLine(".L smearer.cc+")
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetOptTitle(0)

    if printDir == None: printDir=options.printDir
    maximum=-1

    for i,plot in enumerate(plots):
        plot.GetYaxis().SetTitle(plot.GetYaxis().GetTitle()+" (normalized)")
        plot.GetYaxis().SetDecimals(True)
        for b in xrange(1,plot.GetNbinsX()+1):
            if plot.GetBinContent(b)<0: print 'Warning: histo %s has bin %d with negative content (%f), the stack plot will probably be incorrect.'%(p,b,plot.GetBinContent(b))
        plot.Sumw2()
        plot.Scale(1./plot.Integral())
        plot.SetFillColor(SAFE_COLOR_LIST[i])
        plot.SetLineColor(SAFE_COLOR_LIST[i])
        plot.SetLineWidth(3)
        plot.SetFillStyle(0)
        plot.SetMaximum(max(maximum,1.3*plot.GetMaximum()))
        plot.GetXaxis().SetTitle(xtitle)

        if outputDir: outputDir.WriteTObject(plot)

    # define aspect ratio
    plotformat = (1200,600) if options.wideplot else (600,600)
    sf = 20./plotformat[0]
    ROOT.gStyle.SetPadLeftMargin(600.*0.18/plotformat[0])

    doRatio = options.showRatio
    islog = options.Logy; 
    if doRatio: ROOT.gStyle.SetPaperSize(20.,sf*(plotformat[1]+150))
    else:       ROOT.gStyle.SetPaperSize(20.,sf*plotformat[1])
    # create canvas
    c1 = ROOT.TCanvas(varname+"_canvas", varname, plotformat[0], (plotformat[1]+150 if doRatio else plotformat[1]))
    c1.SetTopMargin(c1.GetTopMargin()*options.topSpamSize);
    c1.Draw()
    p1, p2 = c1, None # high and low panes
    # set borders, if necessary create subpads
    if doRatio:
        c1.SetWindowSize(plotformat[0] + (plotformat[0] - c1.GetWw()), (plotformat[1]+150 + (plotformat[1]+150 - c1.GetWh())));
        p1 = ROOT.TPad("pad1","pad1",0,0.31,1,1);
        p1.SetTopMargin(p1.GetTopMargin()*options.topSpamSize);
        p1.SetBottomMargin(0);
        p1.Draw();
        p2 = ROOT.TPad("pad2","pad2",0,0,1,0.31);
        p2.SetTopMargin(0);
        p2.SetBottomMargin(0.3);
        p2.SetFillStyle(0);
        p2.Draw();
        p1.cd();
    else:
        c1.SetWindowSize(plotformat[0] + (plotformat[0] - c1.GetWw()), plotformat[1] + (plotformat[1] - c1.GetWh()));
    p1.SetLogy(islog)
    if options.Logx:
        p1.SetLogx(True)
        if p2: p2.SetLogx(True)
        plots[0].GetXaxis().SetNoExponent(True)
        plots[0].GetXaxis().SetMoreLogLabels(True)
    if islog: plots[0].SetMaximum(2*plots[0].GetMaximum())
    if not islog: plots[0].SetMinimum(0)
    plots[0].Draw("HIST")
    ROOT.gStyle.SetErrorX(0.5)
    [p.Draw("SAME E") for p in plots[1:]]
    if doRatio:
        p2.cd()
        ratio,rnorm,rline = doStandaloneRatioHists(plots[0],plots[1],options,maxRange=options.maxRatioRange, fixRange=options.fixRatioRange,
                                                            fitRatio=options.fitRatio, errorsOnRef=options.errorBandOnRatio, 
                                                            ratioNums=options.ratioNums, ratioDen=options.ratioDen)
        if outputDir: outputDir.WriteTObject(ratio)
    if outputDir: outputDir.WriteTObject(c1)
    if options.printPlots:
        for ext in options.printPlots.split(","):
            fdir = printDir;
            if not os.path.exists(fdir): 
                os.makedirs(fdir); 
                if os.path.exists("/afs/cern.ch"): os.system("cp /afs/cern.ch/user/g/gpetrucc/php/index.php "+fdir)
            c1.Print("%s/%s.%s" % (fdir, varname+"_woverz", ext))


if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser(usage="%prog [options] zplots.root wplots.root plots.txt")
    addPlotMakerOptions(parser)
    parser.add_option("--logy", dest="Logy", action="store_true", default=False, help="make logy plot")
    parser.add_option("--logx", dest="Logx", action="store_true", default=False, help="make logx plot")
    (options, args) = parser.parse_args()

    if len(args)<3:
        print "ERROR, must give at least: zplots.root wplots.root plots.txt"
        exit(1)

    zfile = ROOT.TFile.Open(args[0])
    wfile = ROOT.TFile.Open(args[1])
    outfile = ROOT.TFile.Open(options.printDir+"/"+os.path.basename(args[2]).split('.')[0]+".root","recreate")

    plotfile = PlotFile(args[2],options)
    
    for plot in plotfile.plots():
        name = plot.name
        xtitle = plot.getOption('XTitle',name)
        print "Making ratio plot of: ",name
        wplot = wfile.Get(name+"_W").Clone(name+"_W_numerator")
        zplot = zfile.Get(name+"_Z").Clone(name+"_Z_denominator")
        printOnePlot([wplot,zplot],name,xtitle,options,printDir=options.printDir,outputDir=outfile)

    outfile.Close()
