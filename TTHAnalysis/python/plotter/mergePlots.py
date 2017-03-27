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
    parser = OptionParser(usage="%prog [options] mca.txt dir file")
    parser.add_option("--channels", dest="channels", type="string", default="ee,em,mumu", help="channels to merge")
    parser.add_option("--useTotal", dest="useTotal", action="store_true", default=False, help="Use total from input")
    parser.add_option("--postFit_s", dest="postFit_s", action="store_true", default=False, help="Use total from input, s+b fit")
    parser.add_option("--postFit_b", dest="postFit_b", action="store_true", default=False, help="Use total from input, b-only fit")
    parser.add_option("--addErrorsLinearlyForTotal", dest="addErrorsLinearlyForTotal", action="store_true", default=False, help="Add errors linearly for the total histogram")
    addPlotMakerOptions(parser)
    (options, args) = parser.parse_args()
    options.path = ["/data1/peruzzi/TREES_TTH_250117_Summer16_JECV3_noClean_qgV2_skimOnlyMC_v6"]
#    options.path = ["/data1/peruzzi/TREES_TTH_250117_Summer16_JECV3_noClean_qgV2_skim3l2j2b1B_v6"]
    options.lumi = 35.9
    if options.postFit_s or options.postFit_b: options.useTotal = True
    mca  = MCAnalysis(args[0],options)
    FS = options.channels.split(",")
    basedir = args[1];
    plots   = PlotFile(args[2],options)
    filename = basename(args[2]).replace(".txt",".root");
    if options.postFit_s: filename = "postfit_s_"+filename
    if options.postFit_b: filename = "postfit_b_"+filename
    files = dict([ (f,ROOT.TFile("%s/%s/%s" % (basedir,f,filename))) for f in FS])
    outdir = 'merged_linearAddErrors' if options.addErrorsLinearlyForTotal else 'merged'
    ROOT.gSystem.Exec("mkdir -p %s/%s/" % (basedir,outdir))
    ROOT.gSystem.Exec("cp /afs/cern.ch/user/g/gpetrucc/php/index.php %s/%s/" % (basedir,outdir))
    ROOT.gROOT.ProcessLine(".x /afs/cern.ch/user/g/gpetrucc/cpp/tdrstyle.cc(0)")
    ROOT.gROOT.ForceStyle(False)
    ROOT.gStyle.SetErrorX(0.5)
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetPaperSize(20.,25.)
    itemlist = files[FS[0]].GetListOfKeys()
    processes = ['data'] + [p for p in reversed(mca.listBackgrounds())] + mca.listSignals()
    if options.useTotal: processes += [ 'total' ] 
    for pspec in plots.plots():
        P = pspec.name
        plots = {}
        for f in FS:
            for p in processes:
                h = files[f].Get(P+"_"+p)
                if not h: continue
                if p in plots:
                    if options.addErrorsLinearlyForTotal and p=='total':
                        for b in xrange(1, plots[p].GetNbinsX()+1):
                            plots[p].SetBinContent(b, plots[p].GetBinContent(b)+h.GetBinContent(b))
                            plots[p].SetBinError(b, plots[p].GetBinError(b)+h.GetBinError(b))
                    else:
                        plots[p].Add(h)
                else:
                    hc = h.Clone()
                    hc.SetDirectory(None)
                    plots[p] = hc
#        print plots.keys()
        stack = ROOT.THStack()
        if len(plots) == 0: continue
        tot = plots['data'].Clone(); tot.Reset() 
        totSyst = plots['data'].Clone(); totSyst.Reset() 
        data = plots['data']
        if options.useTotal:
            tot     = plots['total']
            totSyst = plots['total']
        doRatio = True
        for p in [_p for _p in reversed(mca.listBackgrounds())] + mca.listSignals():
            if p not in plots: continue
            h = plots[p]
            stack.Add(h)
            if not options.useTotal:
                tot.Add(h)
                totSyst.Add(h)
                if mca.getProcessOption(p,'NormSystematic',0.0) > 0:
                    syst = mca.getProcessOption(p,'NormSystematic',0.0)
                    if "TH1" in h.ClassName():
                        for b in xrange(1,h.GetNbinsX()+1):
                            totSyst.SetBinError(b, hypot(totSyst.GetBinError(b), syst*h.GetBinContent(b)))
        tot.GetYaxis().SetRangeUser(0, 1.0*pspec.getOption('MoreY',2.0)*max(tot.GetMaximum(), data.GetMaximum()))
        ## Prepare split screen
        c1 = ROOT.TCanvas("c1", "c1", 600, 750); c1.Draw()
        c1.SetWindowSize(600 + (600 - c1.GetWw()), (750 + (750 - c1.GetWh())));
#        c1 = ROOT.TCanvas("c1", "c1", 1200, 750); c1.Draw()
#        c1.SetWindowSize(1200 + (1200 - c1.GetWw()), (750 + (750 - c1.GetWh())));

        p1 = ROOT.TPad("pad1","pad1",0,0.30,1,1);
        p1.SetTopMargin(p1.GetTopMargin()*options.topSpamSize);
        p1.SetBottomMargin(0.025)
        p1.Draw();
        p2 = ROOT.TPad("pad2","pad2",0,0,1,0.30);
        p2.SetTopMargin(0.06);
        p2.SetBottomMargin(0.3);
        p2.SetFillStyle(0);
        p2.Draw();
        p1.cd();

        ## Draw absolute prediction in top frame
        tot.Draw("HIST")
        stack.Draw("HIST F SAME")
        if options.showMCError:
            totalError = doShadedUncertainty(totSyst)
        data.Draw("E SAME")
        tot.Draw("AXIS SAME")
        legendCutoff = pspec.getOption('LegendCutoff', 1e-5 if c1.GetLogy() else 1e-2)
        doLegend(plots,mca,corner=pspec.getOption('Legend','TR'),
                 cutoff=legendCutoff, mcStyle="F",
                 cutoffSignals=not(options.showSigShape or options.showIndivSigShapes or options.showSFitShape), 
                 textSize=( (0.045 if doRatio else 0.035) if options.legendFontSize <= 0 else options.legendFontSize ),
                 legWidth=options.legendWidth, legBorder=options.legendBorder, signalPlotScale=options.signalPlotScale,
                 header=options.legendHeader if options.legendHeader else pspec.getOption("LegendHeader", ""))
#        doLegend(plots,mca,corner=pspec.getOption('Legend','TR'))
        doTinyCmsPrelim(hasExpo = tot.GetMaximum() > 9e4 and not c1.GetLogy(),textSize=(0.045 if doRatio else 0.033)*options.topSpamSize,
                        options=options)
        ## Draw relaive prediction in the bottom frame
        p2.cd() 
        rdata,rnorm,rnorm2,rline = doRatioHists(pspec,plots,tot,totSyst, maxRange=options.maxRatioRange, fitRatio=options.fitRatio)
        #rframe = ROOT.TH1F("rframe","rframe",1,xmin,xmax)
        #rframe.GetXaxis().SetTitle(bandN.GetXaxis().GetTitle())
        #rframe.GetYaxis().SetRangeUser(0,1.95);
        #rframe.GetXaxis().SetTitleSize(0.14)
        #rframe.GetYaxis().SetTitleSize(0.14)
        #rframe.GetXaxis().SetLabelSize(0.11)
        #rframe.GetYaxis().SetLabelSize(0.11)
        #rframe.GetXaxis().SetNdivisions(505 if var == "nJet25" else 510)
        #rframe.GetYaxis().SetNdivisions(505)
        #rframe.GetYaxis().SetDecimals(True)
        #rframe.GetYaxis().SetTitle("Ratio")
        #rframe.GetYaxis().SetTitleOffset(0.52);
        #rframe.Draw()
        #bands[ "norm_ratio"].Draw("E2 SAME")
        #bands["shape_ratio"].Draw("E2 SAME")
        #line = ROOT.TLine(xmin,1,xmax,1)
        #line.SetLineWidth(2);
        #line.SetLineStyle(7);
        #line.SetLineColor(1);
        #line.Draw("L")
        #rframe.Draw("AXIS SAME")
        #p1.cd()
        #leg = doLegend(.67,.75,.92,.91, textSize=0.05)
        #leg.AddEntry(bandN, "Norm.",  "F")
        #leg.AddEntry(bandS, "Shape",  "F")
        #leg.Draw()
        #c1.cd()
        #doCMSSpam("CMS Preliminary",textSize=0.035)
        c1.Print("%s/%s/%s.png" % (basedir,outdir,P))
        c1.Print("%s/%s/%s.pdf" % (basedir,outdir,P))
        #del leg
        #del frame
        #del rframe
        del c1
