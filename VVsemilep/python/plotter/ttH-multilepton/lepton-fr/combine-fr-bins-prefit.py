import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True
from array import array
from collections import defaultdict
from math import hypot

import os.path
from optparse import OptionParser
parser = OptionParser(usage="%prog [options] ins out")
parser.add_option("--oprefix", dest="oprefix", default=None, help="Output prefix");
(options, args) = parser.parse_args()
if len(args) < 2: raise RuntimeError

def binEdges(axis,nbins):
    r0 = [ axis.GetBinLowEdge(1) ] + [ axis.GetBinUpEdge(i) for i in xrange(1,nbins+1) ]
    return array('f',r0)
def yzslice(h,ix):
    ny,nz = h.GetNbinsY(), h.GetNbinsZ()
    ys = binEdges(h.GetYaxis(), ny)
    zs = binEdges(h.GetZaxis(), nz)
    hslice = ROOT.TH2D("%s_ix%d" % (h.GetName(), ix), "", ny,ys,nz,zs)
    hslice.SetDirectory(None)
    #if str(h.GetName()).endswith("_data"):
    #    print "Input %s: %.3f events at ix=%d,iz=1, %.3f events at ix=%d,iz=2, x=[%.0f,%.0f]" % (h.GetName(), sum(h.GetBinContent(ix,iy,1) for iy in xrange(1,ny+1)), ix,sum(h.GetBinContent(ix,iy,2) for iy in xrange(1,ny+1)),ix,h.GetXaxis().GetBinLowEdge(ix),h.GetXaxis().GetBinUpEdge(ix))
    for iy in xrange(1,ny+1):
        for iz in xrange(1,nz+1):
            hslice.SetBinContent(iy,iz, h.GetBinContent(ix,iy,iz))
            hslice.SetBinError(iy,iz, h.GetBinError(ix,iy,iz))
    #print "Histo %s: %.3f events at iz=1, %.3f events at iz=2" % (hslice.GetName(), sum(hslice.GetBinContent(iy,1) for iy in xrange(1,ny+1)), sum(hslice.GetBinContent(iy,2) for iy in xrange(1,ny+1)))
    return hslice

def copyAdd(h2d, ix, h3d, linear):
    ny,nz = h3d.GetNbinsY(), h3d.GetNbinsZ()
    #print "Histo %s: %.3f events at iz=1, %.3f events at iz=2" % (h2d.GetName(), sum(h2d.GetBinContent(iy,1) for iy in xrange(1,ny+1)), sum(h2d.GetBinContent(iy,2) for iy in xrange(1,ny+1)))
    #print "Before %s: %.3f events at ix=%d,iz=1, %.3f events at ix=%d,iz=2, x=[%.0f,%.0f]" % (h3d.GetName(),sum(h3d.GetBinContent(ix,iy,1) for iy in xrange(1,ny+1)), ix,sum(h3d.GetBinContent(ix,iy,2) for iy in xrange(1,ny+1)), ix, h3d.GetXaxis().GetBinLowEdge(ix),h3d.GetXaxis().GetBinUpEdge(ix))
    for iy in xrange(1,ny+1):
        for iz in xrange(1,nz+1):
            h3d.SetBinContent(ix,iy,iz, h2d.GetBinContent(iy,iz) + h3d.GetBinContent(ix,iy,iz))
            if linear:
                h3d.SetBinError(ix,iy,iz, h2d.GetBinError(iy,iz) + h3d.GetBinError(ix,iy,iz))
            else:
                h3d.SetBinError(ix,iy,iz, hypot(h2d.GetBinError(iy,iz), h3d.GetBinError(ix,iy,iz)))
    #if str(h3d.GetName()).endswith("_data"):
    #    print "After  %s: %.3f events at ix=%d,iz=1, %.3f events at ix=%d,iz=2, x=[%.0f,%.0f]" % (h3d.GetName(),sum(h3d.GetBinContent(ix,iy,1) for iy in xrange(1,ny+1)), ix,sum(h3d.GetBinContent(ix,iy,2) for iy in xrange(1,ny+1)), ix, h3d.GetXaxis().GetBinLowEdge(ix),h3d.GetXaxis().GetBinUpEdge(ix))

allprocs = None
ptbins = defaultdict(list)
yedges, zedges = None, None
for ispec in args[:-1]:
    (fname,conePtRange) = ispec.split(":")
    ptMin,ptMax = map(float,conePtRange.split("-"))
    tfin = ROOT.TFile(fname)
    allkeys = [ k.GetName() for k in tfin.GetListOfKeys() ]
    prefix  = [ k for k in allkeys if k.endswith("_data") ][0].replace("_data","")
    allprocs = [ k.replace(prefix+"_","") for k in allkeys if prefix in k ]
    hdata = tfin.Get(prefix+"_data")
    allh  = dict([(p,tfin.Get("%s_%s"%(prefix,p))) for p in allprocs])
    nx = hdata.GetNbinsX()
    xedges = binEdges(hdata.GetXaxis(),nx)
    for ix in xrange(1,nx+1): 
        xmin,xmax = xedges[ix-1], xedges[ix]
        if (ptMin <= xmin and xmax <= ptMax):
            ptbins[(xmin,xmax)].append( dict((p,yzslice(h,ix)) for (p,h) in allh.iteritems()) )
    if yedges == None:
        yedges = binEdges(hdata.GetYaxis(), hdata.GetNbinsY())
        zedges = binEdges(hdata.GetZaxis(), hdata.GetNbinsZ())
    tfin.Close()
allbins = list(sorted(ptbins.iterkeys()))
for ibin in xrange(len(allbins)-1):
    if allbins[ibin][1] != allbins[ibin+1][0]: raise RuntimeError("BAD BINS: %s" % allbins)
xedges = array('f',[allbins[0][0]]+[x[1] for x in allbins])
print "Output bin edges: %s" % list(xedges)
out = args[-1]
outdir = os.path.dirname(out)
if outdir:
    if not os.path.exists(outdir):
        os.system("mkdir -p "+outdir)
        if os.path.exists("/afs/cern.ch"): os.system("cp /afs/cern.ch/user/g/gpetrucc/php/index.php "+outdir)
outfile = ROOT.TFile(out, "RECREATE")
if options.oprefix: prefix = options.oprefix
for p in allprocs:
    h3d = ROOT.TH3D("%s_%s"%(prefix,p), "", len(xedges)-1,xedges, len(yedges)-1,yedges, len(zedges)-1,zedges)
    for ibin,xbin in enumerate(allbins):
        for srcmap in ptbins[xbin]:
            copyAdd(srcmap[p], ibin+1, h3d, (p != "data"))
    outfile.WriteTObject(h3d)
outfile.ls()
outfile.Close()
