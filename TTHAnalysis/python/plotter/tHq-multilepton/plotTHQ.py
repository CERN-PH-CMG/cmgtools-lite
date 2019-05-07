#!/usr/bin/env python
import sys
import os
import re
from os.path import dirname,basename

from CMGTools.TTHAnalysis.plotter.tree2yield import PlotSpec
from CMGTools.TTHAnalysis.plotter.mcAnalysis import MCAnalysis
from CMGTools.TTHAnalysis.plotter.mcPlots import PlotMaker
from CMGTools.TTHAnalysis.plotter.mcPlots import PlotFile

import CMGTools.TTHAnalysis.plotter.mcPlots as mcP

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gROOT.ProcessLine(".x /afs/cern.ch/user/g/gpetrucc/cpp/tdrstyle.cc(0)")
ROOT.gROOT.ForceStyle(False)
ROOT.gStyle.SetErrorX(0.5)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetPaperSize(20.,25.)

PLOTRANGES = {
    ('dPhiHighestPtSSPair', 'em') : (0., 75.),
    ('finalBins_log_40', '3l')    : (0.1, 500.),
    ('finalBins_log_mm_40', 'mm') : (0.1, 200.),
    ('finalBins_log_em_40', 'em') : (1.5, 500.),
    ('maxEtaJet25_40', '3l')      : (0.0, 28.),
    ('maxEtaJet25_40', 'em')      : (0.0, 110.),
    ('nJet25', '3l')              : (0.0, 95.),
    ('nJet25', 'em')              : (0.0, 260.),
    ('nJet25', 'mm')              : (0.0, 130.),
    ('thqMVA_tt_3l_40', '3l')     : (0.0, 41.),
    ('thqMVA_tt_2lss_40', 'em')   : (0.0, 120.),
    ('thqMVA_tt_2lss_40', 'mm')   : (0.0, 56.),
    ('thqMVA_ttv_2lss_40', 'em')  : (0.0, 91.),
    ('thqMVA_ttv_2lss_40', 'mm')  : (0.0, 61.),
    ('thqMVA_ttv_3l_40', '3l')    : (0.0, 41.),
}

RATIORANGES = {
    'dPhiHighestPtSSPair' : (-0.4, 3.2),
    'maxEtaJet25_40'      : (-0.4, 4.2),
    'nJet25'              : (-0.4, 2.8),
}

XAXISLABELS = {
    'dPhiHighestPtSSPair' : "#Delta#phi of highest p_{T} same-sign lepton pair",
    'maxEtaJet25_40' : "Max. |#eta| of any untagged jet",
    'nJet25' : "N(jets, p_{T} > 25 GeV, |#eta| < 2.4)",
    'thqMVA_tt_2lss_40' : "BDT (tHq vs t#bar{t}+jets)",
    'thqMVA_ttv_2lss_40' : "BDT (tHq vs t#bar{t}V)",
    'thqMVA_tt_3l_40' : "BDT (tHq vs t#bar{t}+jets)",
    'thqMVA_ttv_3l_40' : "BDT (tHq vs t#bar{t}V)",
}

YAXISLABELS = {
    'nJet25' : "Events",
    'finalBins_40' : "Events",
}

YAXISUNIT = {
    'dPhiHighestPtSSPair' : " rad.",
}

MERGEMAP = {
    "tZq"   : 'tZq',
    "tZW"   : 'tZq',
    "WWDPS" : 'tZq',
    "WWss"  : 'tZq',
    "Gstar" : 'tZq',
    "tttt"  : 'tZq',
    "VVV"   : 'tZq',
    "ZZ"    : 'tZq',
}

LABELS = {
    'tZq' : 'tZ, W^{#pm}W^{#pm}, t#bar{t}t#bar{t}, VVV',
    'ZZ'  : 'tZ, W^{#pm}W^{#pm}, t#bar{t}t#bar{t}, VVV',
    'data_fakes' : 'Nonprompt',
    'data_flips' : 'Charge misid.'
}

CHANNEL_LABELS = {
    '3l' : "3 lep.",
    'mm' : "#mu^{#pm}#mu^{#pm}",
    'em' : "e^{#pm}#mu^{#pm}",
    'ee' : "e^{#pm}e^{#pm}"
}

CHANNEL_LABEL_POS = {
    ('dPhiHighestPtSSPair', 'mm') : (0.82, 0.82),
    ('dPhiHighestPtSSPair', 'em') : (0.82, 0.82),
    ('dPhiHighestPtSSPair', '3l') : (0.82, 0.82),
}

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


def getRatioTGraph(graph, tothist):
    """Calculate graph/tot"""
    ratio = graph.Clone("%s_%s"%(graph.GetName(), tothist.GetName()))
    for i in xrange(ratio.GetN()):
        x    = ratio.GetX()[i]
        div  = tothist.GetBinContent(tothist.GetXaxis().FindBin(x))
        ratio.SetPoint(i, x, ratio.GetY()[i]/div if div > 0 else 0)
        ratio.SetPointError(i, ratio.GetErrorXlow(i), ratio.GetErrorXhigh(i), 
                               ratio.GetErrorYlow(i)/div  if div > 0 else 0, 
                               ratio.GetErrorYhigh(i)/div if div > 0 else 0) 
    return ratio

def getRatioTGraph2(graph, tothist):
    """Calculate (graph-tot)/tot"""
    ratio = graph.Clone("%s_%s"%(graph.GetName(), tothist.GetName()))
    for i in xrange(ratio.GetN()):
        x    = ratio.GetX()[i]
        div  = tothist.GetBinContent(tothist.GetXaxis().FindBin(x))
        ratio.SetPoint(i, x,   (ratio.GetY()[i]-div)/div if div > 0 else 0)
        ratio.SetPointError(i, ratio.GetErrorXlow(i), ratio.GetErrorXhigh(i), 
                               ratio.GetErrorYlow(i)/div  if div > 0 else 0, 
                               ratio.GetErrorYhigh(i)/div if div > 0 else 0) 
    return ratio

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
             nColumns=1):
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

        (x1,y1,x2,y2) = (0.97-legWidth if doWide else .90-legWidth, .7 - textSize*max(nentries-3,0), .90, .91)
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
            (x1,y1,x2,y2) = (.2, .33 + textSize*max(nentries-3,0), .2+legWidth, .15)

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

if __name__ == "__main__":
    from optparse import OptionParser
    usage="%prog [options] mca.txt plots.txt infile.root"
    parser = OptionParser(usage=usage)
    mcP.addPlotMakerOptions(parser)

    parser.add_option("--outDir", dest="outDir", type="string",
                      default="postFitPlots/",
                      help="Output directory for postfit plots");
    parser.add_option("--doLog", dest="doLog", action="store_true",
                      help="Do logarithmic scale plots");
    parser.add_option("--paper", dest="paper", action="store_true",
                      help="Make paper version of plots");
    parser.add_option("--subPredInRatios", dest="subPredInRatios", action="store_true",
                      help="Subtract prediction in ratios");
    parser.add_option("--doRebinning", dest="doRebinning", action="store_true",
                      help="Remap the bins according to PR#18");
    (options, args) = parser.parse_args()
    # options.path = ["thqtrees/TREES_TTH_250117_Summer16_JECV3_noClean_qgV2_tHqsoup_v2/"]
    # options.lumi = 35.9
    # options.poisson = True

    try: os.makedirs(options.outDir)
    except OSError: pass

    os.system("cp /afs/cern.ch/user/s/stiegerb/www/index.php "+options.outDir)

    options.allProcesses = True # To include SkipMe=True ones

    mca = MCAnalysis(args[0], options)
    plots = PlotFile(args[1], options)
    infile = ROOT.TFile.Open(args[2], 'READ')
    print "Reading histograms from %s" % infile.GetName()

    channel = '3l'
    if '2lss_mm' in args[2] or '2lss-mm' in args[2]:
        channel = 'mm'
    if '2lss_em' in args[2] or '2lss-em' in args[2]:
        channel = 'em'

    # Adjust label of merged processes
    for process,newlabel in LABELS.iteritems():
        try: mca.setProcessOption(process, 'Label', newlabel)
        except RuntimeError: pass

    for pspec in plots.plots():
        hists = {} # pname -> histogram
        # Check that all histos are there
        for process in mca.listProcesses(allProcs=True):
            h = infile.Get("%s_%s"%(pspec.name, process))
            if not h and process in mca.listProcesses():
                print "ERROR: missing %s_%s in %s" % (pspec.name, process, infile.GetName())

            if not process in mca.listProcesses(): continue # skip 'SkipMe=True' ones

            # Explicit skip of flips for mm (somehow doesn't work otherwise?)
            if channel == 'mm' and process == 'data_flips': continue

            h.SetDirectory(0)
            pout = MERGEMAP.get(process, process)
            if pout in hists:
                hists[pout].Add(h)
            else:
                hists[pout] = h

        stack = ROOT.THStack("%s_stack_SM"%(pspec.name),"")
        for process in list(reversed(mca.listBackgrounds())) + list(reversed(mca.listSignals())):
            if process in hists:
                stack.Add(hists[process])

        hbkg = infile.Get("%s_background" % pspec.name)
        htot = hbkg.Clone("%s_htot" % pspec.name)
        if pspec.name in XAXISLABELS:
            htot.GetXaxis().SetTitle(XAXISLABELS[pspec.name])

        for process in mca.listSignals():
            hsig = infile.Get("%s_%s"%(pspec.name, process)).Clone('%s_%s_clone' % (pspec.name, process))
            htot.Add(hsig)

        hthq_itc = infile.Get("%s_%s"%(pspec.name, 'tHq_hww_ITC')).Clone('tHq_ITC')
        hthw_itc = infile.Get("%s_%s"%(pspec.name, 'tHW_hww_ITC')).Clone('tHW_ITC')
        htth     = infile.Get("%s_%s"%(pspec.name, 'ttH')).Clone('ttH_ITC')

        hthq_itc.SetLineWidth(3)
        hthq_itc.SetLineColor(hthq_itc.GetFillColor())
        hthq_itc.SetFillStyle(0)
        hthq_itc.SetMarkerSize(0)

        hthw_itc.SetLineWidth(3)
        hthw_itc.SetLineColor(hthw_itc.GetFillColor())
        hthw_itc.SetFillStyle(0)
        hthw_itc.SetMarkerSize(0)

        htot_itc = hthq_itc.Clone("%s_htot_itc" % pspec.name)
        htot_itc.Add(hthw_itc)
        htot_itc.Add(infile.Get("%s_%s"%(pspec.name, 'ttH')).Clone('ttH_forratio'))
        htot_itc.Add(hbkg)

        # Make canvas/pads
        c1 = ROOT.TCanvas("c1_%s"%pspec.name, "c1", 600, 750)
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

        # Draw histograms

        # Remove last bin in maxJetEta histos:
        if pspec.name == 'maxEtaJet25_40':
            htot.GetXaxis().SetRangeUser(0.0, 4.7)

        htot.Draw("HIST")
        stack.Draw("HIST F SAME")
        totalError = mcP.doShadedUncertainty(htot)

        hthq_itc.Draw("HIST SAME")
        hthw_itc.Draw("HIST SAME")

        if options.poisson:
            pdata = mcP.getDataPoissonErrors(hists['data'], True, True)
            pdata.SetMarkerSize(1.3)
            pdata.Draw("PZ SAME")
            hists['data'].poissonGraph = pdata ## attach it so it doesn't get deleted
        else:
            hists['data'].Draw("E SAME")

        # Re-adjust yaxis range
        mcP.reMax(htot, hists['data'],
                  islog=pspec.hasOption('Logy'),
                  factorLin=1.3,
                  factorLog=2.0,
                  doWide=False)

        if (pspec.name, channel) in PLOTRANGES:
            htot.GetYaxis().SetRangeUser(PLOTRANGES[(pspec.name, channel)][0],
                                         PLOTRANGES[(pspec.name, channel)][1])


        htot.Draw("AXIS SAME")

        # Do the legend
        leg = doLegend(hists, mca,
                       corner=pspec.getOption('Legend','TR'),
                       legBorder=options.legendBorder,
                       textSize=0.042,
                       totalError=None,
                       cutoff=0.01,
                       cutoffSignals=True,
                       legWidth=0.62,
                       nColumns=2)
        leg.AddEntry(totalError, "Total uncertainty","F") 
        leg.AddEntry(hthq_itc, "tHq (#kappa_{t}=-1.0)", "L") 
        leg.AddEntry(hthw_itc, "tHW (#kappa_{t}=-1.0)", "L") 

        # if channel == 'em':
        #     lspam += r"e^{#pm}#mu^{#pm} channel"
        # if channel == 'mm':
        #     lspam += r"#mu^{#pm}#mu^{#pm} channel"
        # if channel == '3l':
        #     lspam += "3-lepton channel"

        doTinyCmsPrelim(hasExpo = False,
                        textSize=(0.055), xoffs=-0.03,
                        textLeft = "#bf{CMS} #it{Preliminary}" if not options.paper else "#bf{CMS}",
                        textRight = "%(lumi) (13 TeV)",
                        lumi = options.lumi,
                        ypos=0.935)

        # mcP.doTinyCmsPrelim(hasExpo = False,
        #                     textSize=(0.055), xoffs=-0.03,
        #                     textLeft = "#bf{CMS} #it{Preliminary}",
        #                     textRight = "%(lumi) (13 TeV)",
        #                     lumi = options.lumi)

        if pspec.hasOption('Logy'):
            p1.SetLogy(True)

        ## Add labels for each channel
        tlat = ROOT.TLatex()
        tlat.SetNDC(True)
        tlat.SetTextFont(43); tlat.SetTextSize(28);
        tlat.DrawLatex(CHANNEL_LABEL_POS.get((pspec.name, channel), (0.82, 0.60))[0],
                       CHANNEL_LABEL_POS.get((pspec.name, channel), (0.82, 0.60))[1],
                       CHANNEL_LABELS.get(channel, "Undef."))

        # Make the ratios
        p2.cd()

        # if not options.subPredInRatios:
        nomratio = getRatioTGraph(hists['data'].poissonGraph, htot)
        # else:
        #     nomratio = getRatioTGraph2(hists['data'].poissonGraph, htot)

        thqratio = htot_itc.Clone("thqratio")
        # if options.subPredInRatios: thqratio.Add(htot_itc, -1.0)
        thqratio.Divide(htot)
        thqratio.SetLineWidth(2)
        thqratio.SetLineColor(htot_itc.GetLineColor())

        bgratio = hbkg.Clone("bgratio")
        # if options.subPredInRatios: bgratio.Add(hbkg, -1.0)
        bgratio.SetFillStyle(0)
        bgratio.Divide(htot)
        bgratio.SetLineWidth(2)
        bgratio.SetLineColor(ROOT.kBlack)
        bgratio.SetLineStyle(2)

        unity  = htot.Clone("sim_div")
        for ibin in xrange(1, unity.GetNbinsX()+1):
            cont = unity.GetBinContent(ibin)
            err  = unity.GetBinError(ibin)
            if not options.subPredInRatios:
                unity.SetBinContent(ibin, 1 if cont > 0 else 0)
            else:
                unity.SetBinContent(ibin, 0)
            if options.errorBandOnRatio:
                unity.SetBinError(ibin, err/cont if cont > 0 else 0)
            else:
                unity.SetBinError(ibin, 0)

        # unity.SetFillStyle(1001);
        # unity.SetFillColor(ROOT.kCyan);
        # unity.SetMarkerStyle(1);
        # unity.SetMarkerColor(ROOT.kCyan);
        unity.SetFillStyle(3244);
        unity.SetFillColor(ROOT.kGray+2)
        unity.SetMarkerStyle(0)
        ROOT.gStyle.SetErrorX(0.5);

        if options.errorBandOnRatio:
            unity.Draw("E2");
        else:
            unity.Draw("AXIS");

        if options.fitRatio != None:
            from CMGTools.TTHAnalysis.tools.plotDecorations import fitTGraph
            fitTGraph(nomratio, order=options.fitRatio)
            unity.SetFillStyle(3013);
            if options.errorBandOnRatio:
                unity.Draw("AXIS SAME");

        rmin = options.maxRatioRange[0]
        rmax = options.maxRatioRange[1]
        rmin = float(pspec.getOption("RMin", rmin))
        rmax = float(pspec.getOption("RMax", rmax))
        rmin, rmax = RATIORANGES.get(pspec.name, (rmin, rmax))

        unity.GetYaxis().SetRangeUser(rmin, rmax)
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
        if not options.subPredInRatios:
            unity.GetYaxis().SetTitle("Ratio to SM")
        else:
            unity.GetYaxis().SetTitle("#frac{Data-Pred}{Pred.}")

        htot.GetXaxis().SetLabelOffset(999) ## send them away
        htot.GetXaxis().SetTitleOffset(999) ## in outer space
        htot.GetYaxis().SetTitleFont(43)
        htot.GetYaxis().SetTitleSize(26)
        htot.GetYaxis().SetTitleOffset(1.8)
        htot.GetYaxis().SetLabelFont(43)
        htot.GetYaxis().SetLabelSize(22)
        htot.GetYaxis().SetLabelOffset(0.007)

        # Hack y axis title (assume fixed bin width!)
        yaxistitle = YAXISLABELS.get(pspec.name,
                                     "Events / %.2f" % htot.GetXaxis().GetBinWidth(1))
        yaxistitle += YAXISUNIT.get(pspec.name, "")
        htot.GetYaxis().SetTitle(yaxistitle)

        binlabels = pspec.getOption("xBinLabels","")
        if binlabels != "" and len(binlabels.split(",")) == unity.GetNbinsX():
            blist = binlabels.split(",")
            for i in range(1,unity.GetNbinsX()+1): 
                unity.GetXaxis().SetBinLabel(i,blist[i-1]) 
            unity.GetXaxis().SetLabelSize(0.18)
        #ratio.SetMarkerSize(0.7*ratio.GetMarkerSize()) # no it is confusing
        binlabels = pspec.getOption("xBinLabels","")
        if binlabels != "" and len(binlabels.split(",")) == unity.GetNbinsX():
            blist = binlabels.split(",")
            for i in range(1,unity.GetNbinsX()+1): 
                unity.GetXaxis().SetBinLabel(i,blist[i-1]) 
        #$ROOT.gStyle.SetErrorX(0.0);
        liney = 1 if not options.subPredInRatios else 0
        line = ROOT.TLine(unity.GetXaxis().GetXmin(),liney,unity.GetXaxis().GetXmax(),liney)
        line.SetLineWidth(2);
        line.SetLineColor(58);
        line.Draw("L")

        bgratio.Draw("HIST SAME")
        thqratio.Draw("HIST SAME")
        nomratio.Draw("PZ")
        # for ratio in ratios:
        #     if ratio == nomratio:
        #         ratio.Draw("PZ")
        #     elif ratio == thqratio:
        #         ratio.Draw("L")
        #     else:
        #         ratio.Draw("E SAME")

        xoffs = 0.03
        if pspec.name == 'dPhiHighestPtSSPair' and channel == 'mm':
            xoffs = 0.1
        leg0 = ROOT.TLegend(0.18+xoffs, 0.82, 0.35+xoffs, 0.9)
        leg0.AddEntry(nomratio, "Data/SM", "P")
        leg3 = ROOT.TLegend(0.35+xoffs, 0.82, 0.52+xoffs, 0.9)
        leg3.AddEntry(unity, "Total uncertainty", "F")
        leg1 = ROOT.TLegend(0.18+xoffs, 0.33, 0.40+xoffs, 0.41)
        leg1.AddEntry(thqratio, "(#kappa_{t}=-1.0)/SM", "L")
        leg2 = ROOT.TLegend(0.40+xoffs, 0.33, 0.60+xoffs, 0.41)
        leg2.AddEntry(bgratio, "Backg./SM", "L")
        # leg0 = ROOT.TLegend(0.18, 0.82, 0.35, 0.9)
        # leg0.AddEntry(nomratio, "SM", "P")
        # leg1 = ROOT.TLegend(0.28, 0.82, 0.52, 0.9)
        # leg1.AddEntry(thqratio, "SM (#kappa_{t}=-1.0)", "L")
        # leg2 = ROOT.TLegend(0.52, 0.82, 0.75, 0.9)
        # leg2.AddEntry(bgratio, "Backg.", "L")
        # leg3 = ROOT.TLegend(0.68, 0.82, 0.90, 0.9)
        # leg3.AddEntry(unity, "Tot. SM unc.", "F")
        for leg in [leg0, leg1, leg2, leg3]:
            leg.SetFillColor(0)
            leg.SetShadowColor(0)
            leg.SetLineColor(0)
            leg.SetTextFont(43)
            leg.SetTextSize(18)
            leg.Draw()

        # Save the plots
        c1.cd()
        for ext in ['.pdf', '.png']:#, '.C']:
            outname = '%s_%s' % (pspec.name, channel)
            if options.doLog: outname += '_log'
            c1.Print(os.path.join(options.outDir, outname+ext))
        del c1


