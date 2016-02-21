from math import *
from os.path import basename
import re

import sys
sys.argv.append('-b-')
import ROOT
ROOT.gROOT.SetBatch(True)
sys.argv.remove('-b-')
from array import *

def makeH2D(name,xedges,yedges):
    return ROOT.TH2F(name,name,len(xedges)-1,array('f',xedges),len(yedges)-1,array('f',yedges))

def fillSliceY(th2,plot1d,yvalue,xslice):
    ybin = th2.GetYaxis().FindBin(yvalue)
    for xbin in xrange(1,th2.GetNbinsX()+1):
        xval = th2.GetXaxis().GetBinCenter(xbin)
        if xslice[0] <= xval and xval <= xslice[1]:
            for i in xrange(plot1d.GetN()):
                x,xp,xm = plot1d.GetX()[i], plot1d.GetErrorXhigh(i), plot1d.GetErrorYlow(i)
                if x-xm <= xval and xval <= x+xp:
                    th2.SetBinContent(xbin,ybin,plot1d.GetY()[i])
                    th2.SetBinError(xbin,ybin,max(plot1d.GetErrorYlow(i),plot1d.GetErrorYhigh(i)))
def readSliceY(th2,filename,plotname,yvalue,xslice):
    slicefile = ROOT.TFile.Open(filename)
    if not slicefile: raise RuntimeError, "Cannot open "+filename
    plot = slicefile.Get(plotname)
    if not plot: 
        slicefile.ls()
        raise RuntimeError, "Cannot find "+plotname+" in "+filename
    fillSliceY(th2,plot,yvalue,xslice)
    slicefile.Close()
def read2D(th2,filepattern,plotname,yslices,xslice):
    for yvalue,yname in yslices:
        readSliceY(th2,filepattern%yname,plotname,yvalue,xslice)
def readMany2D(processes,th2s,filepattern,plotname,yslices,xslice):
    for (th2,proc) in zip(th2s,processes):
        read2D(th2, filepattern, plotname%proc, yslices, xslice)
def make2D(out,name,xedges,yedges):
    out.cd()
    th2 = makeH2D(name,xedges,yedges)
    return th2

def styles(hs):
    colors = { 'Data':ROOT.kBlack, 'MC':ROOT.kAzure+1 }
    for label,h in hs:
        for n,c in colors.iteritems():
            if n in label:
                h.SetLineColor(c)
                h.SetMarkerColor(c)
        h.SetLineWidth(3)
        h.GetXaxis().SetTitle("lepton p_{T}^{corr} (GeV)")

if __name__ == "__main__":
    from CMGTools.TTHAnalysis.plotter.mcEfficiencies import stackEffs, graphFromXSlice
    import os.path
    from optparse import OptionParser
    parser = OptionParser(usage="%prog [options] path out")
    parser.add_option("--pdir", dest="outdir", default=None, help="Output directory for plots");
    parser.add_option("--xcut", dest="xcut", default=None, nargs=2, type='float', help="X axis cut");
    parser.add_option("--xrange", dest="xrange", default=None, nargs=2, type='float', help="X axis range");
    parser.add_option("--yrange", dest="yrange", default=None, nargs=2, type='float', help="Y axis range");
    parser.add_option("--logy", dest="logy", default=False, action='store_true', help="Do y axis in log scale");
    parser.add_option("--ytitle", dest="ytitle", default="Fake rate", type='string', help="Y axis title");
    parser.add_option("--fontsize", dest="fontsize", default=0.05, type='float', help="Legend font size");
    parser.add_option("--legendWidth", dest="legendWidth", type="float", default=0.35, help="Width of the legend")
    parser.add_option("--grid", dest="showGrid", action="store_true", default=False, help="Show grid lines")
    parser.add_option("--legend",  dest="legend",  default="TL",  type="string", help="Legend position (BR, TR)")
    parser.add_option("--compare", dest="compare", default="", help="Samples to compare (by default, all except the totals)")
    parser.add_option("--showRatio", dest="showRatio", action="store_true", default=False, help="Add a data/sim ratio plot at the bottom")
    parser.add_option("--rr", "--ratioRange", dest="ratioRange", type="float", nargs=2, default=(-1,-1), help="Min and max for the ratio")
    parser.add_option("--normEffUncToLumi", dest="normEffUncToLumi", action="store_true", default=False, help="Normalize the dataset to the given lumi for the uncertainties on the calculated efficiency")
    (options, args) = parser.parse_args()
    (outname) = args[0]
    print outname
    outfile = ROOT.TFile.Open(outname,"RECREATE")
    if options.outdir:
        if not os.path.exists(options.outdir):
            os.system("mkdir -p "+options.outdir)
            if os.path.exists("/afs/cern.ch"): os.system("cp /afs/cern.ch/user/g/gpetrucc/php/index.php "+options.outdir)
        ROOT.gROOT.ProcessLine(".x tdrstyle.cc")
        ROOT.gStyle.SetOptStat(0)
    if True:
       ptbins_el = [ 10,15,20,30,45,65,100 ]
       ptbins_mu = [ 10,   20,30,45,65,100 ]
       etabins_el = [0, 1.479, 2.5]
       etabins_mu = [0, 1.2,   2.4]
       etaslices_el = [ (0.4,"00_15"), (1.8,"15_25") ]
       etaslices_mu = [ (0.4,"00_12"), (1.8,"12_24") ]
       XsQ    = [ "QCD", "data_comb" ]
       XsD    = [ "DY",  "data_comb" ]
       Xnices = [ "MC non-pr.", "Data, comb." ]
       h2d_el = [ make2D(outfile,"FR_mva075_el_"+X, ptbins_el, etabins_el) for X in XsQ ]
       h2d_mu = [ make2D(outfile,"FR_mva075_mu_"+X, ptbins_mu, etabins_mu) for X in XsQ ]

       Plots="plots/76X/ttH/fr-meas"
       Z3l="z3l/v1.0"
       QCD="v1.0"
       #### Electrons: 
       # 10-30 from Z+l
       readMany2D(XsD, h2d_el, "/".join([Plots, Z3l, "el/fakerates-mtW3R/fr_sub_eta_%s_comp.root"]), "%s", etaslices_el, (10,30) )
       # 30-inf from Ele12 bMedium
       readMany2D(XsQ, h2d_el, "/".join([Plots, QCD, "el/HLT_Ele12_CaloIdM_TrackIdM_PFJet30/fakerates-mtW1R/fr_sub_eta_%s_comp.root"]), "%s", etaslices_el, (30,999) )

       #### Muons: 
       # 10-20 from Z+l
       readMany2D(XsD, h2d_mu, "/".join([Plots, Z3l, "mu/fakerates-mtW3R/fr_sub_eta_%s_comp.root"]), "%s", etaslices_mu, (10,20) )
       # 20-45 from Mu8
       readMany2D(XsQ, h2d_mu, "/".join([Plots, QCD, "mu/HLT_Mu8/fakerates-mtW1R/fr_sub_eta_%s_comp.root"]), "%s", etaslices_mu, (20,45) )
       # 45-inf from Mu17
       readMany2D(XsQ, h2d_mu, "/".join([Plots, QCD, "mu/HLT_Mu17/fakerates-mtW1R/fr_sub_eta_%s_comp.root"]), "%s", etaslices_mu, (45,999) )

       # Serialize
       for h in h2d_el + h2d_mu: outfile.WriteTObject(h)

       # Plot
       if options.outdir:
           for lep,h2d,xcuts in (("el",h2d_el,[30]),("mu",h2d_mu,[20,45])):
              for ieta,eta in enumerate(["barrel","endcap"]):
                  effs = [ (n,graphFromXSlice(h,ieta+1)) for (n,h) in zip(Xnices,h2d) ]
                  styles(effs)
                  options.xlines = xcuts
                  stackEffs(options.outdir+"/fr_%s_%s.root"%(lep,eta), None,effs,options)
    outfile.ls()
