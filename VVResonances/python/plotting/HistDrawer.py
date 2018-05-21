import re
import os
import copy

from math import log10, floor, pow

from ROOT import TCanvas, TPaveText, TBox, gStyle
from CMGTools.RootTools.DataMC.Stack import Stack

from CMGTools.H2TauTau.proto.plotter.CMS_lumi import CMS_lumi

from CMGTools.H2TauTau.proto.plotter.officialStyle import officialStyle
officialStyle(gStyle)
gStyle.SetLegendBorderSize(0)

def ensureDir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

class HistDrawer:
    ocan = None
    can = None
    pad = None
    padr = None

    @classmethod
    def buildCanvas(cls):
        can = cls.can
        pad = cls.pad
        padr = cls.padr
        if not can:
            can = cls.can = TCanvas('can', '', 800, 800)

            can.Divide(1, 2, 0.0, 0.0)

            pad = cls.pad = can.GetPad(1)
            padr = cls.padr = can.GetPad(2)

            # Set Pad sizes
            # pad.SetPad(0.0, 0.32, 1., 1.0)
            # padr.SetPad(0.0, 0.00, 1., 0.34)
            pad.SetPad(0.0, 0.2, 1.0, 1.0)
            padr.SetPad(0.0, 0.0, 1.0, 0.2)

            pad.SetTopMargin(0.08)
            pad.SetLeftMargin(0.16)
            pad.SetBottomMargin(0.03)
            pad.SetRightMargin(0.05)

            # padr.SetBottomMargin(0.35)
            padr.SetBottomMargin(0.4)
            padr.SetLeftMargin(0.16)
            padr.SetRightMargin(0.05)

        can.cd()
        can.Draw()
        pad.Draw()
        padr.Draw()

        return can, pad, padr

    @classmethod
    def buildCanvasSingle(cls):
        ocan = TCanvas('ocan', '', 600, 600)
        ocan.cd()
        ocan.Draw()
        return ocan

    @staticmethod
    def datasetInfo(plot):
        year = ''
        year = '2016'
        lumi = plot.lumi/1000. if hasattr(plot, 'lumi') else 0.
        unit = plot.lumi_unit if hasattr(plot, 'lumi_unit') else 'fb'
        energy = plot.com_energy if hasattr(plot, 'com_energy') else 13
        return year, lumi, energy, unit

    @staticmethod
    def CMSPrelim(plot, pad, channel, legend='right', writeExtraText=True, extraText='Preliminary'):
        pad.cd()
        year, lumi, energy, unit = HistDrawer.datasetInfo(plot)
        theStr = '{lumi:3.3} {unit}^{{-1}} ({energy:d} TeV)'.format(year=year, unit=unit, lumi=lumi, energy=energy)
        # CMS_lumi(pad, theStr, iPosX=0, writeExtraText=writeExtraText, extraText=extraText)  # CMS outside canvas
        if legend == 'right':
            CMS_lumi(pad, theStr, iPosX=10, writeExtraText=writeExtraText, extraText=extraText)
        else:
            CMS_lumi(pad, theStr, iPosX=13, writeExtraText=writeExtraText, extraText=extraText)


        lowY = 0.68
        if writeExtraText:
            lowY = 0.74

        r = pad.GetRightMargin()
        l = pad.GetLeftMargin()
        posX = l + 0.045*(1-l-r)
        posXhigh = 0.25
        if writeExtraText:
            r = pad.GetRightMargin()+.3
            l = pad.GetLeftMargin()+.15
            posXhigh = 0.75

        if legend == 'left':
            posX = 1. - r - 0.16 - 0.21
            posXhigh = 1. - r - 0.02 - 0.21
            if writeExtraText:
                posX = 1. - r - 0.16 -.2
                posXhigh = 1. - r - 0.02 -.2

        plot.chan = TPaveText(posX, lowY, posXhigh, lowY+0.18, "NDC")
        if writeExtraText:
            plot.chan = TPaveText(posX, lowY, posXhigh, lowY+0.22, "NDC")

        plot.chan.SetBorderSize(0)
        plot.chan.SetFillStyle(0)
        plot.chan.SetTextAlign(12)
        # plot.chan.SetTextSize(0.6*pad.GetTopMargin()) # To have it the same size as CMS_lumi
        plot.chan.SetTextSize(0.7*pad.GetTopMargin()) # make larger than CMS_lumi
        plot.chan.SetTextFont(42)
        plot.chan.AddText(channel)
        plot.chan.Draw('same')


    unitpat = re.compile('.*\((.*)\)\s*$')

    keeper = []

    @staticmethod
    def draw(plot, do_ratio=True, channel='#mu#tau_{h}', plot_dir='plots',
             plot_name=None, SetLogy=0,
             blindxmin=None, blindxmax=None, unit=None,
             writeExtraText=True, extraText='Preliminary',
             do_pull=False):
        print plot
        assert(do_ratio != do_pull)
        Stack.STAT_ERRORS = True

        can = pad = padr = None

        if do_ratio or do_pull:
            can, pad, padr = HistDrawer.buildCanvas()
        else:
            can = HistDrawer.buildCanvasSingle()

        pad.cd()
        pad.SetLogy(SetLogy)
        # print "about to DrawStack"
        # plot.DrawNormalized()
        # plot.DrawNormalizedRatioStack('HIST', ymin=0.1)
        # , dataAsPoisson=True
        plot.statErrors = False
        plot.DrawStack('HIST', print_norm=plot.name=='_norm_', ymin=0.1, scale_signal='') # magic word to print integrals in legend

        h = plot.supportHist
        h.GetXaxis().SetLabelColor(1)
        # h.GetXaxis().SetLabelSize(1)

        unitsperbin = h.GetXaxis().GetBinWidth(1)
        ytitle = 'Events'
        if unit:
            round_to_n = lambda x, n: round(x, -int(floor(log10(abs(x)))) + (n - 1))
            ytitle += " / {} {}".format(round_to_n(unitsperbin, 3), unit)
        else:
            round_to_n = lambda x, n: round(x, -int(floor(log10(abs(x)))) + (n - 1))
            ytitle += " / {}".format(round_to_n(unitsperbin, 3))

        h.GetYaxis().SetTitle(ytitle)
        # if axis labels and title overlap, change offset here
        h.GetYaxis().SetTitleOffset(1.3)
        h.GetXaxis().SetTitleOffset(2.0)

        if do_ratio or do_pull:
            padr.cd()
            ratio = copy.deepcopy(plot)
            ratio.legendOn = False

        if blindxmin or blindxmax:
            if not blindxmin:
                blindxmin = 0
            if not blindxmax:
                blindxmax = plot.GetXaxis().GetXmax()
            if do_ratio:
                ratio.Blind(blindxmin, blindxmax, True)
            plot.Blind(blindxmin, blindxmax, False)

        if do_ratio:
            ratio.DrawDataOverMCMinus1(-0.5, 0.5)
            hr = ratio.dataOverMCHist

        if do_pull:
            ratio.DrawDataMinusMCOverData(-0.5, 0.5)
            print "DrawDataMinusMCOverData"
            hr = ratio.dataOverMCHist

        if do_ratio or do_pull:

            # Gymnastics to get same label sizes etc in ratio and main plot
            ytp_ratio = 3.5
            xtp_ratio = 3.5

            # hr.GetYaxis().SetNdivisions(4)

            hr.GetYaxis().SetTitleSize(h.GetYaxis().GetTitleSize() * xtp_ratio)
            hr.GetXaxis().SetTitleSize(h.GetXaxis().GetTitleSize() * ytp_ratio)

            hr.GetYaxis().SetTitleOffset(h.GetYaxis().GetTitleOffset() / xtp_ratio)
            hr.GetXaxis().SetTitleOffset(h.GetXaxis().GetTitleOffset() / ytp_ratio+.35)

            hr.GetYaxis().SetLabelSize(h.GetYaxis().GetLabelSize() * xtp_ratio*.9)
            hr.GetXaxis().SetLabelSize(h.GetXaxis().GetLabelSize() * ytp_ratio)

            h.GetXaxis().SetLabelColor(0)
            h.GetXaxis().SetLabelSize(0)
            padr.Update()

        # blinding
        if blindxmin or blindxmax:
            pad.cd()
            max = plot.stack.totalHist.GetMaximum()
            box = TBox(blindxmin, 0,  blindxmax, max)
            box.SetFillColor(1)
            box.SetFillStyle(3004)
            box.Draw()
            HistDrawer.keeper.append(box)

        HistDrawer.CMSPrelim(plot, pad, channel, legend=plot.legendPos, writeExtraText=writeExtraText, extraText=extraText)
        can.cd()

        plotname = plot_dir + '/'
        ensureDir(plot_dir)
        plotname += plot_name if plot_name else plot.name
        can.SaveAs(plotname + '.png')
        can.SaveAs(plotname + '.pdf')

        # Also save with log y
        if plot.legendPos == 'right':
            h.GetYaxis().SetRangeUser(0.1001, pad.GetUymax() * 5.)
        else:
            # minimum is set to 2 orders of magnitude lower than maximum
            minRange = pow(10, floor(log10(pad.GetUymax()/100.)))
            h.GetYaxis().SetRangeUser(minRange + minRange*1e-4, pad.GetUymax() * 5.e3)
        pad.SetLogy(True)
        can.SaveAs(plotname + '_log.png')
        can.SaveAs(plotname + '_log.pdf')
        pad.SetLogy(0)
        return ratio

    drawRatio = draw
