import math
import ROOT
from ROOT import TGraphAsymmErrors, TLine, TLegend

from CMGTools.H2TauTau.proto.plotter.HistDrawer import HistDrawer

def getVertexWeight(verbose=False):
    '''Gets a string to reweight according to PU while doing ROOT plotting'''
    f_data = ROOT.TFile('$CMSSW_BASE/src/CMGTools/H2TauTau/plotting/mm/data.root')
    h_data = f_data.Get('example_data_obs_n_vertices_SingleMuon_Run2016G_PromptReco_v1;1')
    f_mc = ROOT.TFile('$CMSSW_BASE/src/CMGTools/H2TauTau/plotting/mm/mc.root')
    h_mc = f_mc.Get('example_W1Jets_n_vertices_W1JetsToLNu_LO')


    # Should ideally be normalised but better make sure
    h_data.Scale(1./h_data.Integral())
    h_mc.Scale(1./h_mc.Integral())

    pattern = '((n_vertices >= {npu} && n_vertices < {npu_up}) * {weight})'
    patterns = []
    for i in xrange(min(h_mc.GetNbinsX(), h_data.GetNbinsX())):
        if h_data.GetBinContent(i+1) == 0.:
            continue
        elif h_mc.GetBinContent(i+1) == 0.:
            print 'WARNING - data PU weight filled but MC zero:'
            print 'nPU =', i, 'w_data =', h_data.GetBinContent(i+1)
        else:
            ratio = h_data.GetBinContent(i+1)/h_mc.GetBinContent(i+1)
            patterns.append(pattern.format(npu=i, npu_up=i+1, weight=ratio))

    weight = '+'.join(patterns)
    weight = '(({0})*(is_data<0.5) + (is_data>0.5))'.format(weight)
    if verbose:
        print 'PU weight:', weight
    return weight

def getPUWeight(verbose=False):
    '''Gets a string to reweight according to PU while doing ROOT plotting'''
    f_data = ROOT.TFile('$CMSSW_BASE/src/CMGTools/H2TauTau/data/2016G.root')
    h_data = f_data.Get('pileup')
    f_mc = ROOT.TFile('$CMSSW_BASE/src/CMGTools/H2TauTau/data/MC_Spring16_PU25_Startup.root')
    h_mc = f_mc.Get('pileup')

    h_data.Rebin(10)
    h_mc.Rebin(10)

    # Should ideally be normalised but better make sure
    h_data.Scale(1./h_data.Integral())
    h_mc.Scale(1./h_mc.Integral())

    pattern = '((nPU >= {npu} && nPU < {npu_up}) * {weight})'
    patterns = []
    for i in xrange(min(h_mc.GetNbinsX(), h_data.GetNbinsX())):
        if h_data.GetBinContent(i+1) == 0.:
            continue
        elif h_mc.GetBinContent(i+1) == 0.:
            print 'WARNING - data PU weight filled but MC zero:'
            print 'nPU =', i, 'w_data =', h_data.GetBinContent(i+1)
        else:
            ratio = h_data.GetBinContent(i+1)/h_mc.GetBinContent(i+1)
            patterns.append(pattern.format(npu=i, npu_up=i+1, weight=ratio))

    weight = '+'.join(patterns)
    weight = '({0} + (is_data>0.5))'.format(weight)
    if verbose:
        print 'PU weight:', weight
    return weight


def drawRatioLines(hist, frac=0., y0=1.):
    '''Draw a line at y = 1, at 1+frac, and at 1-frac.
    hist is used to get the x axis range.'''
    xmin = hist.GetXaxis().GetXmin()
    xmax = hist.GetXaxis().GetXmax()
    line = TLine()
    line.DrawLine(xmin, y0, xmax, y0)
    if frac > 0.:
        line.DrawLine(xmin, y0+frac, xmax, y0+frac)
        line.DrawLine(xmin, y0-frac, xmax, y0-frac)


def plotDataOverMCEff(hist_mc_tight, hist_mc_loose, hist_data_tight, hist_data_loose, plot_name='fakerate.pdf', mc_leg='MC', obs_leg='Observed', ratio_leg='Obs/MC'):

    g = TGraphAsymmErrors(hist_mc_tight)
    g.Divide(hist_mc_tight, hist_mc_loose)
    g.GetYaxis().SetTitle('Misidentification rate')
    g.GetXaxis().SetTitle(hist_mc_tight.GetXaxis().GetTitle())
    g.GetYaxis().SetTitleOffset(1.2)
    g.GetYaxis().SetTitleOffset(1.3)

    g.SetLineColor(2)
    g.SetMarkerColor(2)

    g_data = TGraphAsymmErrors(hist_data_tight)
    g_data.Divide(hist_data_tight, hist_data_loose)

    # if g_data.GetN() != hist_data_tight.GetNbinsX():
    #     import pdb; pdb.set_trace()

    g_data.GetYaxis().SetTitle('Misidentification rate')
    g_data.GetXaxis().SetTitle(hist_data_tight.GetXaxis().GetTitle())
    g_data.GetYaxis().SetTitleOffset(1.2)
    g_data.GetYaxis().SetTitleOffset(1.3)
    g_data.SetMarkerColor(1)

    g_vals = g.GetY()
    g_data_vals = g_data.GetY()

    g_ratio = g_data.Clone('ratio')

    for i in xrange(g_data.GetN()):
        ratio = g_data_vals[i]/g_vals[i] if g_vals[i] else 0.
        g_ratio.SetPoint(i, g.GetX()[i], ratio)

        rel_y_low = math.sqrt((g_data.GetErrorYlow(i)/g_data_vals[i])**2 + (g.GetErrorYlow(i)/g_vals[i])**2) if g_data_vals[i] > 0. and g_vals[i] > 0. else 0.

        g_ratio.SetPointEYlow(i, rel_y_low * ratio)

        rel_y_high = math.sqrt((g_data.GetErrorYhigh(i)/g_data_vals[i])**2 + (g.GetErrorYhigh(i)/g_vals[i])**2) if g_data_vals[i] > 0. and g_vals[i] > 0. else 0.

        g_ratio.SetPointEYhigh(i, rel_y_high * ratio)

    # Gymnastics to get same label sizes etc in ratio and main plot
    ytp_ratio = 2.
    xtp_ratio = 2.

    # hr.GetYaxis().SetNdivisions(4)

    g_ratio.GetYaxis().SetTitleSize(g.GetYaxis().GetTitleSize() * xtp_ratio)
    g_ratio.GetXaxis().SetTitleSize(g.GetXaxis().GetTitleSize() * ytp_ratio)

    g_ratio.GetYaxis().SetTitleOffset(g.GetYaxis().GetTitleOffset() / xtp_ratio)
    g_ratio.GetXaxis().SetTitleOffset(g.GetXaxis().GetTitleOffset())  # / ytp_ratio)

    g_ratio.GetYaxis().SetLabelSize(g.GetYaxis().GetLabelSize() * xtp_ratio)
    g_ratio.GetXaxis().SetLabelSize(g.GetXaxis().GetLabelSize() * ytp_ratio)

    g_data.GetXaxis().SetLabelColor(0)
    g_data.GetXaxis().SetLabelSize(0)
    g.GetXaxis().SetLabelColor(0)
    g.GetXaxis().SetLabelSize(0)

    g_ratio.GetXaxis().SetTitle(g.GetXaxis().GetTitle())

    maxy = 1.3 * max(g.GetMaximum(), g_data.GetMaximum(), 0.05)
    g.GetYaxis().SetRangeUser(0.0011, maxy)

    cv, pad, padr = HistDrawer.buildCanvas()

    pad.cd()

    g.Draw('AP')
    g_data.Draw('P')

    legend = TLegend(0.23, 0.73, 0.43, 0.91)
    legend.SetFillColor(0)
    legend.SetFillStyle(0)
    legend.SetLineColor(0)
    legend.SetLineWidth(0)

    legend.AddEntry(g.GetName(), mc_leg, 'lep')
    legend.AddEntry(g_data.GetName(), obs_leg, 'lep')

    legend.Draw()

    padr.cd()
    g_ratio.GetYaxis().SetRangeUser(0.01, 1.99)
    g_ratio.GetYaxis().SetTitle(ratio_leg)
    g_ratio.Draw('AP')

    drawRatioLines(g_ratio)

    cv.Print(plot_name)

    g.GetYaxis().SetRangeUser(0.0001, 1)
    pad.SetLogy(True)
    cv.Print(plot_name.replace('.', '_log.'))
    f = ROOT.TFile(plot_name.replace('.', '_log.').replace('.pdf', '.root'), 'RECREATE')
    g.Write()
    g_data.Write()
    cv.Write()
    f.Close()
    

def plotMCEffs(input_list, plot_name='fakerate.pdf'):
    '''input_list expects tuples with structure:
       (hist tight, hist loose, legend line, colour)
    '''

    graphs = []

    for (hist_tight, hist_loose, legend, colour, style) in input_list:
        g = TGraphAsymmErrors(hist_tight)
        g.Divide(hist_tight, hist_loose)
        g.GetYaxis().SetTitle('Misidentification rate')
        g.GetXaxis().SetTitle(hist_tight.GetXaxis().GetTitle())
        g.GetYaxis().SetTitleOffset(1.2)
        g.GetYaxis().SetTitleOffset(1.3)

        g.SetLineColor(colour)
        g.SetLineStyle(style)
        g.SetMarkerColor(colour)
        g.SetMarkerStyle(19+style)

        g.legend = legend

        graphs.append(g)


    ratio_graphs = []

    base_graph = graphs[0]
    for graph in graphs[1:]:

        g_vals = base_graph.GetY()
        g_data_vals = graph.GetY()

        g_ratio = graph.Clone('ratio')

        for i in xrange(graph.GetN()):
            ratio = g_data_vals[i]/g_vals[i] if g_vals[i] else 0.
            g_ratio.SetPoint(i, base_graph.GetX()[i], ratio)

            rel_y_low = math.sqrt((graph.GetErrorYlow(i)/g_data_vals[i])**2 + (base_graph.GetErrorYlow(i)/g_vals[i])**2) if g_data_vals[i] > 0.0000001 and g_vals[i] > 0.0000001 else 0.

            g_ratio.SetPointEYlow(i, rel_y_low * ratio)

            rel_y_high = math.sqrt((graph.GetErrorYhigh(i)/g_data_vals[i])**2 + (base_graph.GetErrorYhigh(i)/g_vals[i])**2) if g_data_vals[i] > 0.0000001 and g_vals[i] > 0.0000001 else 0.

            g_ratio.SetPointEYhigh(i, rel_y_high * ratio)

        ratio_graphs.append(g_ratio)

    # Gymnastics to get same label sizes etc in ratio and main plot
    ytp_ratio = 2.
    xtp_ratio = 2.

    # hr.GetYaxis().SetNdivisions(4)
    for g_ratio in ratio_graphs:
        g_ratio.GetYaxis().SetTitleSize(g.GetYaxis().GetTitleSize() * xtp_ratio)
        g_ratio.GetXaxis().SetTitleSize(g.GetXaxis().GetTitleSize() * ytp_ratio)

        g_ratio.GetYaxis().SetTitleOffset(g.GetYaxis().GetTitleOffset() / xtp_ratio)
        g_ratio.GetXaxis().SetTitleOffset(g.GetXaxis().GetTitleOffset())  # / ytp_ratio)

        g_ratio.GetYaxis().SetLabelSize(g.GetYaxis().GetLabelSize() * xtp_ratio)
        g_ratio.GetXaxis().SetLabelSize(g.GetXaxis().GetLabelSize() * ytp_ratio)

        g_ratio.GetXaxis().SetTitle(base_graph.GetXaxis().GetTitle())


    for graph in graphs:
        graph.GetXaxis().SetLabelColor(0)
        graph.GetXaxis().SetLabelSize(0)


    maxy = 1.3 * max([gr.GetMaximum() for gr in graphs] + [1./1.25])
    for g in graphs:
        g.GetYaxis().SetRangeUser(0.0011, maxy)

    cv, pad, padr = HistDrawer.buildCanvas()

    pad.cd()

    base_graph.Draw('AP')
    for graph in graphs[1:]:
        graph.Draw('P')

    legend = TLegend(0.63, 0.63, 0.93, 0.91)
    legend.SetFillColor(0)
    legend.SetFillStyle(0)
    legend.SetLineColor(0)
    legend.SetLineWidth(0)

    legend2 = TLegend(0.78, 0.63, 0.93, 0.91)
    legend2.SetFillColor(0)
    legend2.SetFillStyle(0)
    legend2.SetLineColor(0)
    legend2.SetLineWidth(0)

    for graph in graphs:
        if 'opp' in graph.legend:
            legend2.AddEntry(graph.GetName(), graph.legend, 'lep')
        else:
            legend.AddEntry(graph.GetName(), graph.legend, 'lep')

    legend.Draw()
    legend2.Draw()

    padr.cd()

    for g_ratio in ratio_graphs:
        g_ratio.GetYaxis().SetRangeUser(0.01, 1.99)
        g_ratio.GetYaxis().SetTitle('Ratio to '+base_graph.legend)
        g_ratio.Draw('AP' if g_ratio == ratio_graphs[0] else 'P')

    drawRatioLines(g_ratio)

    cv.Print(plot_name)

    g.GetYaxis().SetRangeUser(0.0001, 1)
    pad.SetLogy(True)
    cv.Print(plot_name.replace('.', '_log.'))
    f = ROOT.TFile(plot_name.replace('.', '_log.').replace('.pdf', '.root'), 'RECREATE')
    g.Write()
    # g_data.Write()
    cv.Write()
    f.Close()
