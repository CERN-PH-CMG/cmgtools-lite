import sys
import ROOT

if __name__ == '__main__':
    name, filename, xvar = sys.argv[1:]
    tfile = ROOT.TFile.Open(filename)
    if not tfile: raise RuntimeError("Can't find "+filename)
    hdata = tfile.Get(xvar+"_data")
    hmc = tfile.Get(xvar+"_background")
    if not hmc or not hdata: 
        tfile.ls()
        raise RuntimeError("Can't find histograms in "+filename)
    if xvar.endswith("_nvtx"):
        nbinsx = hdata.GetNbinsX()
        nbinsy = hdata.GetNbinsY()
        ptvals = []
        wvals = []
        xstep = hdata.GetXaxis().GetBinUpEdge(1)-hdata.GetXaxis().GetBinLowEdge(1)
        print "nvtx binning: %g" % xstep
        for iy in xrange(1,nbinsy+1):
            ptvals.append(hdata.GetYaxis().GetBinUpEdge(iy))
            print "working in pt bin %d [%g,%g]" % (iy, hdata.GetYaxis().GetBinLowEdge(iy), hdata.GetYaxis().GetBinUpEdge(iy))
            xmc, xdata = [], []
            for ix in xrange(1,nbinsx+1):
                xmc.append(hmc.GetBinContent(ix,iy))
                xdata.append(hdata.GetBinContent(ix,iy))
                wvals.append(xdata[-1]/xmc[-1] if xmc[-1] else 1.0)
            print "\t mc     = ", xmc
            print "\t data   = ", xmc
            print "\t weight = ", wvals[(iy-1)*nbinsx : (iy)*nbinsx]
        privname = "_"+name
        print ""
        print "float %s_ptvals[%d] = { %s };" % (privname, len(ptvals), ", ".join(map(str,ptvals)))
        print "float %s_wvals[%d] = { %s };" % (privname, len(wvals), ", ".join(map(str,wvals)))
        print ("""
float %(name)s(float conept, int nVert) { 
    int vtxbin = std::min(nVert/%(xstep)d, %(nbinsx)d-1);
    for (unsigned int i = 0; i < %(nbinsy)d; ++i) {
        if (conept < %(privname)s_ptvals[i]) return %(privname)s_wvals[i*%(nbinsx)d + vtxbin];
    }
    return 0.;
}""" % locals()).strip()
        print ""
    else:
        nbins = hdata.GetNbinsX()
        xvals = []
        yvals = []
        for i in xrange(1,nbins+1):
            xvals.append(hdata.GetXaxis().GetBinUpEdge(i))
            yvals.append(hdata.GetBinContent(i) / hmc.GetBinContent(i) if hmc.GetBinContent(i) else 1.0)
        privname = "_"+name
        print ""
        print "float %s_xvals[%d] = { %s };" % (privname, len(xvals), ", ".join(map(str,xvals)))
        print "float %s_yvals[%d] = { %s };" % (privname, len(xvals), ", ".join(map(str,yvals)))
        print ("""
float %(name)s(float conept) { 
    for (unsigned int i = 0; i < %(nbins)d; ++i) {
        if (conept < %(privname)s_xvals[i]) return %(privname)s_yvals[i];
    }
    return 0.;
}""" % locals()).strip()
        print ""
