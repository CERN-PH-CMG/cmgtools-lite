from CMGTools.ObjectStudies.scripts.leptonTnP.tnpHarvest import *

def loadFile(name,options):
    tfile = ROOT.TFile.Open(options.inDir+"/"+name+".root")
    if not tfile: print "Can't find file "+name
    return dict([(k+p,tfile.Get(k+p)) for k in ("data","ref","ratio","ratioErr") for p in ("","_syst")])

def check(graphs):
    effs = graphs.keys()
    e0 = effs[0]
    for ei in effs[1:]:
        for k0 in  ("data","ref","ratio","ratioErr"):
            for k in k0, k0+"_syst":
                g0 = graphs[e0][k]
                g1 = graphs[ei][k]
                if g0.GetN() != g1.GetN():
                    raise RuntimeError, "Number of points mismatch between graph %s/%s and %s/%s: %d vs %d" % (e0,k,ei,k,g0.GetN(),g1.GetN())
                for i in xrange(g0.GetN()):
                    if abs(g0.GetX()[i]-g1.GetX()[i]) > 1e-4:
                        raise RuntimeError, "Coordinate mismatch between graph %s/%s and %s/%s: x[%d] = %.8g vs %.8g" % (e0,k,ei,k,i,g0.GetX()[i],g1.GetX()[i])
    return True

def multiply(graphs):
    check(graphs)
    effs = graphs.keys()
    e0 = effs[0]
    ret = {}
    for k0 in  ("data","ref","ratio","ratioErr"):
        for k in k0, k0+"_syst":
            g0 = graphs[e0][k]; n = g0.GetN()
            gi = [ graphs[ei][k] for ei in effs[1:] ]
            g = ROOT.TGraphAsymmErrors(n)
            for i in xrange(n):
                y = g0.GetY()[i]   
                yh2, yl2 = (g0.GetErrorYhigh(i)/(y if y else 1))**2, (g0.GetErrorYlow(i)/(y if y else 1))**2   
                for g1 in gi:
                    yi = g1.GetY()[i]   
                    yh2 += (g1.GetErrorYhigh(i)/(yi if yi else 1))**2;
                    yl2 += (g1.GetErrorYlow(i)/(yi if yi else 1))**2   
                    y *= yi
                g.SetPoint(i, g0.GetX()[i], y)
                g.SetPointError(i, g0.GetErrorXlow(i), g0.GetErrorXhigh(i),  sqrt(yl2)*(y if y else 1), sqrt(yh2)*(y if y else 1))
            ret[k] = g
        ret[k0].syst = ret[k0+"_syst"]
    return ret

def addTnPCombineOptions(parser):
    parser.add_option("-N", "--name",    dest="name", type="string", help="name", default="eff")
    parser.add_option("--postfix",    dest="postfix", type="string", help="Postfix for the output", default="")
    parser.add_option("--xtitle",   dest="xtitle", type="string", default=None, help="X title")
    parser.add_option("--ytitle",   dest="ytitle", type="string", default="Efficiency", help="Y title")
    parser.add_option("--pdir", "--print-dir", dest="printDir", type="string", default="plots", help="print out plots in this directory");
    parser.add_option("--idir", "--in-dir", dest="inDir", type="string", default="plots", help="print out plots in this directory");
    parser.add_option("--xrange", dest="xrange", type="float", nargs=2, default=None);
    parser.add_option("--yrange", dest="yrange", type="float", nargs=2, default=(0,1.025));
    parser.add_option("--rrange", dest="rrange", type="float", nargs=2, default=None);
    parser.add_option("--doRatio", dest="doRatio", action="store_true", default=False, help="Add a ratio plot at the bottom")


if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser(usage="%prog [options] tree reftree")
    addTnPCombineOptions(parser)
    (options, args) = parser.parse_args()
    ROOT.gROOT.SetBatch(True)
    ROOT.gROOT.ProcessLine(".x tdrstyle.cc")
    ROOT.gStyle.SetOptStat(0)
    if not os.path.exists(options.printDir):
        os.system("mkdir -p %s" % options.printDir)
        os.system("cp /afs/cern.ch/user/g/gpetrucc/php/index.php  %s/" % options.printDir)
    if not os.path.exists(options.inDir):
        raise RuntimeError, "Input directory missin"
    factors = dict([ (f, loadFile(options.name.replace(args[0],f),options)) for f in args[1:] ])
    product = multiply(factors)

    for k in "data","ref","ratio","ratioErr":
        product[k].systOnly = graphQSub(product[k].syst, product[k])
        if k in ("data","ref"): 
            capErrors(product[k])
            capErrors(product[k].syst)
            capErrors(product[k].systOnly)
    plotEffs(options.name+options.postfix, [ product['data'], product['ref'] ], product['ratioErr'], options)
    fout = ROOT.TFile.Open(options.printDir+"/"+options.name+options.postfix+".root", "RECREATE")
    for k in "data","ref","ratio","ratioErr":
        fout.WriteTObject(product[k], k)
        fout.WriteTObject(product[k].syst, k+"_syst")
    fout.Close()
    

