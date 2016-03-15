from array import array
import re, sys
sys.argv.append('-b-')
import ROOT
ROOT.gROOT.SetBatch(True)
sys.argv.remove('-b-')

def makeH2D(name,graphs):
    etaRanges = graphs.keys()
    etaVals = [ r[0] for r in etaRanges ] + [ max(r[1] for r in etaRanges) ]
    etaVals.sort()
    oneGraph = graphs.values()[0]
    ptVals = [ oneGraph.GetX()[i] + oneGraph.GetErrorXhigh(i) for i in xrange(oneGraph.GetN()) ]
    ptVals.insert(0, oneGraph.GetX()[0] - oneGraph.GetErrorXlow(0))
    th2 = ROOT.TH2F(name,name,len(ptVals)-1,array('f',ptVals),len(etaVals)-1,array('f',etaVals))
    for etabin in xrange(1,th2.GetNbinsY()+1):
        etaval = th2.GetYaxis().GetBinCenter(etabin)
        for etaRange, graph in graphs.iteritems():
            if etaRange[0] <= etaval and etaval < etaRange[1]:
                break
        for ptbin in xrange(1,th2.GetNbinsX()+1):
            th2.SetBinContent(ptbin,etabin,graph.GetY()[ptbin-1])
            th2.SetBinError(ptbin,etabin,max(graph.GetErrorYlow(ptbin-1),graph.GetErrorYhigh(ptbin-1)))
    return th2

def readGraph(filename,plotname):
    slicefile = ROOT.TFile.Open(filename)
    if not slicefile: raise RuntimeError, "Cannot open "+filename
    plot = slicefile.Get(plotname)
    if not plot: 
        slicefile.ls()
        raise RuntimeError, "Cannot find "+plotname+" in "+filename
    ret = plot.Clone()
    slicefile.Close()
    return ret

def assemble2D(out,name,filepattern,slices,plotname):
    graphs = dict([(r, readGraph(filepattern % n,plotname)) for (n,r) in slices.iteritems()])
    out.cd()
    th2 = makeH2D(name,graphs)
    out.WriteTObject(th2)
    return th2
    
if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser(usage="%prog [options] what path out")
    parser.add_option("-s", "--sel", dest="sel", default=None, help="Select");
    (options, args) = parser.parse_args()
    (what,path,outname) = args
    outfile = ROOT.TFile.Open(outname,"RECREATE")
    muSlices = { 'barrel':(0,1.2),   'endcap':(1.2,2.4) }
    elSlices = { 'barrel':(0,1.479), 'endcap':(1.479,2.5) }
    for p in "data", "DY":
        for l,slices in [('mu',muSlices),('el',elSlices)]:
            assemble2D(outfile,"_".join([what,l,p]),path+"/%s_%%s.root"%l,slices,"pass_l3pt_coarse_"+p)
    outfile.ls()
