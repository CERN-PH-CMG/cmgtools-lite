from CMGTools.ObjectStudies.scripts.leptonTnP.tnpHarvest import *

def loadFile(name,options):
    tfile = ROOT.TFile.Open(options.inDir+"/"+name+".root")
    if not tfile: print "Can't find file "+name
    ret = dict([(ko,tfile.Get(ki)) for (ko,ki) in (("data",name),("ref",name+"_ref"))])
    for (k,v) in ret.iteritems(): 
        if not v: print "Null %s in %s" % (k, options.inDir+"/"+name+".root")
    return ret

def check(graphs):
    for k in  ("data","ref"):
        g0 = graphs[0][k]
        for i in xrange(1,len(graphs)):
            g1 = graphs[i][k]
            if g0.GetN() != g1.GetN():
                raise RuntimeError, "Number of points mismatch between graph %s/%s and %s/%s: %d vs %d" % (e0,k,ei,k,g0.GetN(),g1.GetN())
            for i in xrange(g0.GetN()):
                if abs(g0.GetX()[i]-g1.GetX()[i]) > 1e-4:
                    raise RuntimeError, "Coordinate mismatch between graph %s/%s and %s/%s: x[%d] = %.8g vs %.8g" % (e0,k,ei,k,i,g0.GetX()[i],g1.GetX()[i])
    return True



def fakeMatchingCorr(graphs):
    check(graphs)
    if len(graphs) != 2: raise RuntimeError, "For the moment, only two graphs are supported"
    ret = {}
    for k in  ("data","ref"):
        gfit  = graphs[0][k]
        gfake = graphs[1][k] 
        n = gfit.GetN()
        if gfake.GetN() != n: raise RuntimeError, "Mismatching N points for "+k
        g = ROOT.TGraphAsymmErrors(n)
        for i in xrange(n):
            y = gfit.GetY()[i]   
            eyh = gfit.GetErrorYhigh(i) 
            eyl = gfit.GetErrorYlow(i)
            yf  = gfake.GetY()[i] 
            eyhf = gfake.GetErrorYhigh(i) 
            eylf = gfake.GetErrorYlow(i)
            ycorr =    (   y   -    yf   )/(1-    yf   );
            ycorr_hi = ((y+eyh)-(yf-eylf))/(1-(yf-eylf));
            ycorr_lo = ((y-eyl)-(yf+eyhf))/(1-(yf+eyhf));
            if abs(gfit.GetX()[i] - gfake.GetX()[i]) > 0.001: raise RuntimeError, "Mismatching points %d for %s" % (i,k)
            g.SetPoint(i, gfit.GetX()[i], ycorr);
            g.SetPointError(i, gfit.GetErrorXlow(i), gfit.GetErrorXhigh(i), ycorr - ycorr_lo, ycorr_hi - ycorr);
        ret[k] = g
    makeRatios(ret)
    return ret

def addTnPCombineOptions(parser):
    parser.add_option("-N", "--name",    dest="name", type="string", help="name", default="eff")
    parser.add_option("--postfix",    dest="postfix", type="string", help="Postfix for the output", default="")
    parser.add_option("--xtitle",   dest="xtitle", type="string", default=None, help="X title")
    parser.add_option("--ytitle",   dest="ytitle", type="string", default="Efficiency", help="Y title")
    #parser.add_option("--pdir", "--print-dir", dest="printDir", type="string", default="plots", help="print out plots in this directory");
    parser.add_option("--idir", "--in-dir", dest="inDir", type="string", default="plots", help="print out plots in this directory");
    parser.add_option("--refcol", "--refcol", dest="inDir", type="string", default="ROOT.kAzure+10", help="print out plots in this directory");
    parser.add_option("--xrange", dest="xrange", type="float", nargs=2, default=None);
    parser.add_option("--yrange", dest="yrange", type="float", nargs=2, default=(0.9,1.0));
    parser.add_option("--rrange", dest="rrange", type="float", nargs=2, default=None);
    parser.add_option("--doRatio", dest="doRatio", action="store_true", default=False, help="Add a ratio plot at the bottom")


if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser(usage="%prog [options] tree reftree")
    addTnPCombineOptions(parser)
    (options, args) = parser.parse_args()
    options.printDir = options.inDir
    ROOT.gROOT.SetBatch(True)
    ROOT.gROOT.ProcessLine(".x tdrstyle.cc")
    ROOT.gStyle.SetOptStat(0)
    if not os.path.exists(options.printDir):
        os.system("mkdir -p %s" % options.printDir)
        os.system("cp /afs/cern.ch/user/g/gpetrucc/php/index.php  %s/" % options.printDir)
    if not os.path.exists(options.inDir):
        raise RuntimeError, "Input directory missing"
    factors = [ loadFile(options.name.replace(args[0],f),options) for f in args[1:] ]
    product = fakeMatchingCorr(factors)

    for k in "data","ref","ratio","ratioErr":
        if k in ("data","ref"): 
            capErrors(product[k])
    plotEffs(options.name+options.postfix, [ product['data'], product['ref'] ], product['ratioErr'], options, withSyst=False)
    fout = ROOT.TFile.Open(options.printDir+"/"+options.name+options.postfix+".root", "RECREATE")
    for k in "data","ref","ratio","ratioErr":
        fout.WriteTObject(product[k], k)
        #fout.WriteTObject(product[k].syst, k+"_syst")
    fout.Close()
    

