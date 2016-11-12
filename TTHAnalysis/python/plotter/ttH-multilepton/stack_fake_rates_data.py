from math import *
from os.path import basename
import re

import sys
sys.argv.append('-b-')
import ROOT
ROOT.gROOT.SetBatch(True)
sys.argv.remove('-b-')
from array import *

def readGraphs(filename,pattern,keys):
    ret = {}
    slicefile = ROOT.TFile.Open(filename)
    if not slicefile: raise RuntimeError, "Cannot open "+filename
    for key in keys:
        plotname = pattern % key
        plot = slicefile.Get(plotname)
        if not plot: 
            slicefile.ls()
            raise RuntimeError, "Cannot find "+plotname+" in "+filename
        ret[key] = plot.Clone()
    slicefile.Close()
    return ret

def combine(graphs):
    xvals = []
    for g in graphs:
        for i in xrange(g.GetN()):
            xi = g.GetX()[i]
            if len(xvals) == 0 or (min([abs(x[0]-xi) for x in xvals]) > 0.01):
                xvals.append((xi,g.GetErrorXlow(i),g.GetErrorXhigh(i)))
    xvals.sort()
    ret = ROOT.TGraphAsymmErrors(len(xvals))
    for j,(x,xl,xh) in enumerate(xvals):
        yhli = [ (g.GetY()[i], g.GetErrorYhigh(i), g.GetErrorYlow(i)) for g in graphs for i in xrange(g.GetN()) if abs(g.GetX()[i]-x) <= 0.01 ]
        yavg = sum((y/(h**2+l**2)) for (y,h,l) in yhli)/sum(1.0/(h**2+l**2) for (y,h,l) in yhli)
        ymax = max(y+h for (y,h,l) in yhli)
        ymin = min(y-l for (y,h,l) in yhli)
        ret.SetPoint(j, x, yavg);
        ret.SetPointError(j, xl, xh, yavg-ymin, ymax-yavg);
    return ret

        

def attrs(filename,process):
    if "globalFit"  in filename:
        if "QCD"      in process: return { 'Label':'QCD MC, cut',     'Color':ROOT.kPink-5,  '#':1, 'key':'QCD_cut'  }
        if "DY"       in process: return { 'Label':'DY MC, cut',      'Color':ROOT.kPink-5,  '#':1, 'key':'DY_cut'  }
        if "data_sub" in process: return { 'Label':'Data, cut & sub', 'Color':ROOT.kAzure+1, '#':2, 'key':'data_sub' }
    elif "fitSimND" in filename:
        if "QCD"      in process: return { 'Label':'QCD MC',         'Color':ROOT.kPink-2,  '#':0, 'key':'QCD'       }
        if "DY"       in process: return { 'Label':'DY MC',          'Color':ROOT.kPink-2,    '#':0, 'key':'DY'       }
        if "data_fit" in process: return { 'Label':'Data, sim. fit', 'Color':ROOT.kGreen+2, '#':3, 'key':'data_fit'  }
    elif "fQCD" in filename:
        if "QCD"       in process: return { 'Label':'QCD MC',         'Color':ROOT.kPink-2, '#':0, 'key':'QCD'       }
        if "DY"        in process: return { 'Label':'DY MC',          'Color':ROOT.kPink-2,   '#':0, 'key':'DY'       }
        if "data_fqcd" in process: return { 'Label':'Data, unfolded', 'Color':ROOT.kGray+2, '#':4, 'key':'data_fqcd' }
    else: raise RuntimeError, "No idea of the file"
    raise RuntimeError, "No idea of the process"

def setattrs(graph, opts, xtitle):
    graph.SetLineColor(opts['Color'])
    graph.SetMarkerColor(opts['Color'])
    graph.SetLineWidth(3)
    graph.GetXaxis().SetTitle(xtitle)
    graph.SetName(opts['key'])
    graph.SetTitle(opts['Label'])


if __name__ == "__main__":
    from CMGTools.TTHAnalysis.plotter.mcEfficiencies import stackEffs
    import os.path
    from optparse import OptionParser
    parser = OptionParser(usage="%prog [options] what path out")
    parser.add_option("-o", "--out", dest="out", default=None, help="Output file name. by default equal to plots -'.txt' +'.root'");
    parser.add_option("--xcut", dest="xcut", default=None, nargs=2, type='float', help="X axis cut");
    parser.add_option("--xline", dest="xlines", default=[], action="append", type='float', help="Lines to draw at given X axis values");
    parser.add_option("--xtitle", dest="xtitle", default="lepton p_{T}^{corr} (GeV)", type='string', help="X axis title");
    parser.add_option("--xrange", dest="xrange", default=None, nargs=2, type='float', help="X axis range");
    parser.add_option("--yrange", dest="yrange", default=None, nargs=2, type='float', help="Y axis range");
    parser.add_option("--logy", dest="logy", default=False, action='store_true', help="Do y axis in log scale");
    parser.add_option("--ytitle", dest="ytitle", default="Fake rate", type='string', help="Y axis title");
    parser.add_option("--fontsize", dest="fontsize", default=0.04, type='float', help="Legend font size");
    parser.add_option("--grid", dest="showGrid", action="store_true", default=False, help="Show grid lines")
    parser.add_option("--legend",  dest="legend",  default="TL",  type="string", help="Legend position (BR, TR)")
    parser.add_option("--legendWidth", dest="legendWidth", type="float", default=0.35, help="Width of the legend")
    parser.add_option("--compare", dest="compare", default="", help="Samples to compare (by default, all except the totals)")
    parser.add_option("--showRatio", dest="showRatio", action="store_true", default=False, help="Add a data/sim ratio plot at the bottom")
    parser.add_option("--rr", "--ratioRange", dest="ratioRange", type="float", nargs=2, default=(-1,-1), help="Min and max for the ratio")
    parser.add_option("--normEffUncToLumi", dest="normEffUncToLumi", action="store_true", default=False, help="Normalize the dataset to the given lumi for the uncertainties on the calculated efficiency")
    (options, args) = parser.parse_args()
    if not options.out: raise RuntimeError
    outdir = os.path.basename(options.out)
    if outdir:
        if not os.path.exists(outdir):
            os.system("mkdir -p "+outdir)
            if os.path.exists("/afs/cern.ch"): os.system("cp /afs/cern.ch/user/g/gpetrucc/php/index.php "+outdir)
    outfile = ROOT.TFile(options.out, "RECREATE")
    ROOT.gROOT.ProcessLine(".x tdrstyle.cc")
    ROOT.gStyle.SetOptStat(0)
    
    alleffs = []
    for i,arg in enumerate(args):
        filename,pattern,processes = arg.split(":")
        processes = processes.split(",")
        graphs = readGraphs(filename, pattern, processes)
        for p in processes:
            opts = attrs(filename, p)
            setattrs(graphs[p], opts, options.xtitle)
            alleffs.append( ( opts['Label'], graphs[p] ) )
            graphs[p].order = opts['#']
            outfile.WriteTObject(graphs[p], opts['key'])
    alleffs.sort(key = lambda (l,g) : g.order)
    stackEffs(options.out,None,alleffs,options)
    shortEffs = [ (l,g) for (l,g) in alleffs if g.order == 0 ]
    cdata = combine([ g for (l,g) in alleffs if 'data' in g.GetName() ])
    setattrs(cdata, { 'Color':ROOT.kBlack, 'key':'data_comb', 'Label':'Data, comb.' }, options.xtitle)
    outfile.WriteTObject(cdata)
    shortEffs.append( ( 'Data, comb.', cdata) )
    stackEffs(options.out.replace(".root","_one.root"),None,shortEffs,options)
    
