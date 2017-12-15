import ROOT

from CMGTools.H2TauTau.proto.plotter.officialStyle import setTDRStyle
setTDRStyle()

colours = [1, 2, 3, 4, 6, 7, 8, 9, 47, 46, 44, 43, 42, 41, 40]
markers = [20, 21, 22, 23, 24, 25, 26, 27]

def histsToRoc(hsig, hbg):
    '''Produce ROC curve from 2 input histograms.
    Partly adapted from Giovanni's ttH code.
    '''
    nbins = hsig.GetNbinsX()+2 # include under/overflow
    si = [hsig.GetBinContent(i) for i in xrange(nbins)]
    bi = [hbg.GetBinContent(i) for i in xrange(nbins)]

    if hsig.GetMean() > hbg.GetMean():
        si.reverse()
        bi.reverse()

    sums, sumb = sum(si), sum(bi)
    if sums == 0 or sumb == 0:
        print 'WARNING: Either signal or background histogram empty', sums, sumb
        return None

    for i in xrange(1, nbins):
        si[i] += si[i-1]
        bi[i] += bi[i-1]
    fullsi, fullbi = si[:], bi[:]
    si, bi = [], []
    for i in xrange(1, nbins):
        # skip negative weights
        if len(si) > 0 and (fullsi[i] < si[-1] or fullbi[i] < bi[-1]):
            continue
        # skip repetitions
        if fullsi[i] != fullsi[i-1] or fullbi[i] != fullbi[i-1]:
            si.append(fullsi[i])
            bi.append(fullbi[i])

    if len(si) == 2: 
        si = [si[0]]
        bi = [bi[0]]

    bins = len(si)
    roc = ROOT.TGraph(bins)
    for i in xrange(bins):
        roc.SetPoint(i, si[i]/sums, bi[i]/sumb)

    return roc


def makeLegend(rocs, textSize=0.035, left=True):
    (x1, y1, x2, y2) = (.18 if left else .68, .76 - textSize*max(len(rocs)-3, 0), .5 if left else .95, .88)
    leg = ROOT.TLegend(x1, y1, x2, y2)
    leg.SetFillColor(0)
    leg.SetShadowColor(0)
    leg.SetLineColor(0)
    leg.SetLineWidth(0)
    leg.SetTextFont(42)
    leg.SetTextSize(textSize)
    for key, roc in rocs:
        leg.AddEntry(roc, key, 'lp')
    leg.Draw()

    return leg

def makeROCPlot(rocs, set_name, ymin=0., ymax=1., xmin=0., xmax=1., logy=False):

    allrocs = ROOT.TMultiGraph(set_name, '')
    point_graphs = []
    i_marker = 0
    for i_col, (name, graph) in enumerate(zip([r.name for r in rocs], rocs)):
        col = colours[i_col]
        graph.SetLineColor(col)
        graph.SetMarkerColor(col)
        graph.SetLineWidth(3)
        graph.SetMarkerStyle(0)
        if graph.GetN() > 10:
            allrocs.Add(graph)
        else:
            graph.SetMarkerStyle(markers[i_marker])
            i_marker += 1
            graph.SetMarkerSize(1)
            point_graphs.append(graph)

    c = ROOT.TCanvas()

    allrocs.Draw('APL')

    allrocs.GetXaxis().SetTitle('#epsilon_{s}')
    allrocs.GetYaxis().SetTitle('#epsilon_{b}')
    allrocs.GetYaxis().SetDecimals(True)

    allrocs.GetYaxis().SetRangeUser(ymin, ymax)
    allrocs.GetXaxis().SetRangeUser(xmin, xmax)
    if ymin > 0. and logy:
        c.SetLogy()

    allrocs.Draw('APL')

    for graph in point_graphs:
        graph.Draw('P')

    allrocs.leg = makeLegend(zip([r.title for r in rocs], rocs))

    import pdb; pdb.set_trace()

    c.Print(set_name+'.pdf')

    return allrocs
