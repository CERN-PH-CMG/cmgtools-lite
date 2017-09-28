import re
import os
import copy

from math import log10, floor

from ROOT import TCanvas, TPaveText, TBox, gStyle
from CMGTools.RootTools.DataMC.Stack import Stack

from CMGTools.H2TauTau.proto.plotter.CMS_lumi import CMS_lumi

from CMGTools.H2TauTau.proto.plotter.officialStyle import officialStyle
officialStyle(gStyle)

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
        if not all([can, pad, padr]):
            can = cls.can = TCanvas('can', '', 800, 800) if not can else can
            can.Divide(1, 2, 0.0, 0.0)

            pad = cls.pad = can.GetPad(1) if not pad else pad
            padr = cls.padr = can.GetPad(2) if not padr else padr

            # Set Pad sizes
            pad.SetPad(0.0, 0.32, 1., 1.0)
            padr.SetPad(0.0, 0.00, 1., 0.34)

            pad.SetTopMargin(0.08)
            pad.SetLeftMargin(0.16)
            pad.SetBottomMargin(0.03)
            pad.SetRightMargin(0.05)

            padr.SetBottomMargin(0.35)
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
        year = '2015'
        lumi = plot.lumi/1000. if hasattr(plot, 'lumi') else 0.
        unit = plot.lumi_unit if hasattr(plot, 'lumi_unit') else 'fb'
        energy = plot.com_energy if hasattr(plot, 'com_energy') else 13
        return year, lumi, energy, unit

    @staticmethod
    def CMSPrelim(plot, pad, channel, legend='right'):
        pad.cd()
        year, lumi, energy, unit = HistDrawer.datasetInfo(plot)
        theStr = '{lumi:3.3} {unit}^{{-1}} ({energy:d} TeV)'.format(year=year, unit=unit, lumi=lumi, energy=energy)
        CMS_lumi(pad, theStr, iPosX=0)

        lowY = 0.77

        r = pad.GetRightMargin()
        l = pad.GetLeftMargin()
        posX = l + 0.045*(1-l-r)
        posXhigh = 0.25

        if legend == 'left':
            posX = 1. - r - 0.08
            posXhigh = 1. - r - 0.02

        plot.chan = TPaveText(posX, lowY, posXhigh, lowY+0.18, "NDC")
        plot.chan.SetBorderSize(0)
        plot.chan.SetFillStyle(0)
        plot.chan.SetTextAlign(12)
        plot.chan.SetTextSize(0.6*pad.GetTopMargin()) # To have it the same size as CMS_lumi
        plot.chan.SetTextFont(42)
        plot.chan.AddText(channel)
        plot.chan.Draw('same')


    unitpat = re.compile('.*\((.*)\)\s*$')

    keeper = []

    @staticmethod
    def draw(plot, do_ratio=True, channel='#mu#tau_{h}', plot_dir='plots', 
             plot_name=None, SetLogy=0, 
             blindxmin=None, blindxmax=None, unit=None):
        print plot
        Stack.STAT_ERRORS = True

        can = pad = padr = None

        if do_ratio:
            can, pad, padr = HistDrawer.buildCanvas()
        else:
            can = HistDrawer.buildCanvasSingle()

        pad.cd()
        pad.SetLogy(SetLogy)

        plot.DrawStack('HIST', print_norm=plot.name=='_norm_', ymin=0.1) # magic word to print integrals in legend

        h = plot.supportHist
        h.GetXaxis().SetLabelColor(1)
        # h.GetXaxis().SetLabelSize(1)

        unitsperbin = h.GetXaxis().GetBinWidth(1)
        ytitle = 'Events'
        if unit:
            round_to_n = lambda x, n: round(x, -int(floor(log10(abs(x)))) + (n - 1))
            ytitle += round_to_n(unitsperbin, 3)

        h.GetYaxis().SetTitle('Events')
        h.GetYaxis().SetTitleOffset(1.0)
        h.GetXaxis().SetTitleOffset(2.0)

        if do_ratio:
            padr.cd()
            ratio = copy.deepcopy(plot)
            ratio.legendOn = False

        if blindxmin or blindxmax:
            if not blindxmin:
                blindxmin = 0
            if not blindxmax:
                blindxmax = plot.stack.totalHist.GetXaxis().GetXmax()
            if do_ratio:
                ratio.Blind(blindxmin, blindxmax, True)
            plot.Blind(blindxmin, blindxmax, False)

        if do_ratio:
            ratio.DrawDataOverMCMinus1(-0.5, 0.5)
            hr = ratio.dataOverMCHist

            # Gymnastics to get same label sizes etc in ratio and main plot
            ytp_ratio = 2.
            xtp_ratio = 2.

            # hr.GetYaxis().SetNdivisions(4)

            hr.GetYaxis().SetTitleSize(h.GetYaxis().GetTitleSize() * xtp_ratio)
            hr.GetXaxis().SetTitleSize(h.GetXaxis().GetTitleSize() * ytp_ratio)
            
            hr.GetYaxis().SetTitleOffset(h.GetYaxis().GetTitleOffset() / xtp_ratio)
            hr.GetXaxis().SetTitleOffset(h.GetXaxis().GetTitleOffset() / ytp_ratio)

            hr.GetYaxis().SetLabelSize(h.GetYaxis().GetLabelSize() * xtp_ratio)
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

        HistDrawer.CMSPrelim(plot, pad, channel, legend=plot.legendPos)
        can.cd()

        plotname = plot_dir + '/'
        ensureDir(plot_dir)
        plotname += plot_name if plot_name else plot.name
        can.SaveAs(plotname + '.png')
        can.SaveAs(plotname + '.pdf')
        can.SaveAs(plotname + '.root')

        # Also save with log y
        h.GetYaxis().SetRangeUser(pad.GetUymax() * 5./1000000., pad.GetUymax() * 5.)
        pad.SetLogy(True)
        can.SaveAs(plotname + '_log.png')
        can.SaveAs(plotname + '_log.pdf')
        pad.SetLogy(0)
        return ratio

    drawRatio = draw


