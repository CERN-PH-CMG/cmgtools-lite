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
    ybin = th2.GetYaxis().FindFixBin(yvalue)
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

def makeVariants(h,altsrc=None):
    lptmin = log(h.GetXaxis().GetBinCenter(1))
    lptmax = log(h.GetXaxis().GetBinCenter(h.GetNbinsX()))
    lptc     = 0.5*(lptmax+lptmin)
    lptslope = 1.0/(lptmax-lptc)
    shifters = [
        ("up"  ,  lambda pt,eta,fr,err : min(fr+err, 1.0) ),
        ("down",  lambda pt,eta,fr,err : max(fr-err, 0.05*fr) ),
        ("pt1" ,  lambda pt,eta,fr,err : min(max( fr + err * lptslope*(log(pt)-lptc),  0.05*fr),1.0) ),
        ("pt2" ,  lambda pt,eta,fr,err : min(max( fr - err * lptslope*(log(pt)-lptc),  0.05*fr),1.0) ),
    ]
    ret = []
    for s,func in shifters:
        hsyst = h.Clone(h.GetName()+"_"+s)
        for bx in xrange(1,h.GetNbinsX()+1):
            x = h.GetXaxis().GetBinCenter(bx) 
            for by in xrange(1,h.GetNbinsY()+1):
                y = h.GetYaxis().GetBinCenter(by) 
                fr0 = h.GetBinContent(bx,by)
                if altsrc == None:
                    err = h.GetBinError(bx,by)
                else:
                    err = fr0 * altsrc.GetBinError(bx,by)/altsrc.GetBinContent(bx,by)
                fr = func(x,y,fr0,err)
                print "Variation %-15s: pt %4.1f, eta %3.1f: nominal %.3f +- %.3f --> shifted %.3f "  % (hsyst.GetName(), x, y, fr0, err, fr)
                hsyst.SetBinContent(bx, by, fr)
                hsyst.SetBinError(bx, by, 0)
        ret.append(hsyst)
    return ret

def styles(hs):
    colors = [ ('Data',ROOT.kBlack), ('MC tt',ROOT.kRed+1), ('QCD',ROOT.kAzure+1 ),
               ('QCD, #gamma corr',ROOT.kGreen+2), ('Data, #gamma corr',ROOT.kGray+2),
               ('nominal',ROOT.kBlack), ('up',ROOT.kGray+1), ('down',ROOT.kGray+1), 
                ('pt1',ROOT.kRed+1), ('pt2',ROOT.kBlue+2),
                ('be1',ROOT.kViolet+1), ('be2',ROOT.kGreen+2)]
    for label,h in hs:
        for n,c in colors:
            if n in label:
                h.SetLineColor(c)
                h.SetMarkerColor(c)
        h.SetLineWidth(3)
        h.GetXaxis().SetTitle("lepton p_{T}^{corr} (GeV)")

if __name__ == "__main__":
    from CMGTools.WMass.plotter.mcEfficiencies import stackEffs, graphFromXSlice
    import os.path
    from optparse import OptionParser
    parser = OptionParser(usage="%prog [options] path out")
    parser.add_option("--pdir", dest="outdir", default=None, help="Output directory for plots");
    parser.add_option("--xcut", dest="xcut", default=None, nargs=2, type='float', help="X axis cut");
    parser.add_option("--xrange", dest="xrange", default=None, nargs=2, type='float', help="X axis range");
    parser.add_option("--yrange", dest="yrange", default=(0,0.15), nargs=2, type='float', help="Y axis range");
    parser.add_option("--logy", dest="logy", default=False, action='store_true', help="Do y axis in log scale");
    parser.add_option("--ytitle", dest="ytitle", default="Fake rate", type='string', help="Y axis title");
    parser.add_option("--fontsize", dest="fontsize", default=0.05, type='float', help="Legend font size");
    parser.add_option("--legendWidth", dest="legendWidth", type="float", default=0.35, help="Width of the legend")
    parser.add_option("--grid", dest="showGrid", action="store_true", default=False, help="Show grid lines")
    parser.add_option("--legend",  dest="legend",  default="TL",  type="string", help="Legend position (BR, TR)")
    parser.add_option("--compare", dest="compare", default="", help="Samples to compare (by default, all except the totals)")
    parser.add_option("--showRatio", dest="showRatio", action="store_true", default=True, help="Add a data/sim ratio plot at the bottom")
    parser.add_option("--rr", "--ratioRange", dest="ratioRange", type="float", nargs=2, default=(0,2.9), help="Min and max for the ratio")
    parser.add_option("--normEffUncToLumi", dest="normEffUncToLumi", action="store_true", default=False, help="Normalize the dataset to the given lumi for the uncertainties on the calculated efficiency")
    parser.add_option("--etaBinEdges", dest="etaBinEdges", type="string", default="", help="Give a comma separated list of lepton eta bin edges to make fit categories. Be consistent with binning used to compute fake rate")
    parser.add_option("--ptBinEdges", dest="ptBinEdges", type="string", default="", help="Give a comma separated list of lepton pt bin edges to make fit categories. Be consistent with binning used to compute fake rate")
    parser.add_option("--charge", dest="charge", default="", type='string', help="Select charge: p for positive, n for negative");
    parser.add_option("--wfake", dest="useWfake", action="store_true", default=False, help="Use W_fake MC instead of QCD sample")
    parser.add_option("--lep-flavour", dest="lepFlavour", type="string", default="", help="Specify lepton flavour (el,mu). This option is mandatory (default is \"\" because you have to be consistent with output file name in args[0])")
    parser.add_option("--input-path", dest="input_path", default="", type='string', help="provide path where to find fake-rate files (if empty, 'fake-rate' will use");
    (options, args) = parser.parse_args()
    (outname) = args[0]

    lep = options.lepFlavour
    if lep == "":
        raise RuntimeError, "What analysis (el, mu)?? Specify as --lep-flavour <arg>"

    print outname
    outfile = ROOT.TFile.Open(outname,"RECREATE")
    if options.outdir:
        if not os.path.exists(options.outdir):
            os.system("mkdir -p "+options.outdir)
            if os.path.exists("/afs/cern.ch"): os.system("cp /afs/cern.ch/user/g/gpetrucc/php/index.php "+options.outdir)
        ROOT.gROOT.ProcessLine(".x tdrstyle.cc")
        ROOT.gStyle.SetOptStat(0)
    if True:
        # ptbins_el = [ 25,30,32,34,36,38,40,42,44,46,50,60 ]
        # ptbins_mu = [ 25,27,30,35,45,100 ]
        # etabins_el = [0, 1.479, 2.5]
        # etabins_mu = [0, 1.2,   2.4]
        # if lep=='el':
        #     ptbins = ptbins_el
        #     etabins = etabins_el
        # elif lep=='mu':
        #     ptbins = ptbins_mu
        #     etabins = etabins_mu
        # else: 
        #     raise RuntimeError, "What analysis (el, mu)?? Specify as --lep-flavour <arg>)"

        if len(options.etaBinEdges):
            etabins = [float(binEdge) for binEdge in options.etaBinEdges.split(",")]
            etabins_str = [str(binEdge).replace(".","p") for binEdge in options.etaBinEdges.split(",")]
        if len(options.ptBinEdges):
            ptbins = [float(binEdge) for binEdge in options.ptBinEdges.split(",")]

        print "################################"
        print "### WARNING : READ CAREFULLY ###"
        print "################################"
        print "Using pt bins  --> %s" % ptbins
        print "Using eta bins --> %s" % etabins
        print "################################"

        #etaslices_el = [ (0.4,"00_15"), (1.8,"15_25") ]   # first value in pair can be any value in the range defined by the string argument, used to look for the bin
        #etaslices_mu = [ (0.4,"00_12"), (1.8,"12_24") ]
        #etaslices_mu = [ (1.8,"00_24") ]

        etaslices = []
        for bin in range(0,len(etabins)-1):
            bincenter = (etabins[bin]+etabins[bin+1])/2.0
            binrange_str = etabins_str[bin] + "_" + etabins_str[bin+1]
            etaslices.append( ( bincenter, binrange_str ) )
            
        XsQ    = [ "QCD", "data_comb" ]
        Xnices = [ "MC fakes", "Data, EWK-sub." ]
        if options.useWfake:
            XsQ    = [ "W_fake", "data_comb" ]
        
        if options.input_path == "":
            Plots = "plots/fake-rate/" + str(lep) +"/"  
            if options.charge == "p":
                Plots=Plots +"pos"
            elif options.charge == "n":
                Plots=Plots +"neg"
            else:
                Plots=Plots +"comb"
        else :
            Plots = options.input_path 
            if Plots.endswith("/"):
                Plots = Plots[:-1]


        if lep=='el':
            # TTH

            h2d_el = [ make2D(outfile,"FR_FullSel_el_"+X, ptbins, etabins) for X in XsQ ]

            #### Electrons: 
            readMany2D(XsQ, h2d_el, Plots+"/fr_sub_eta_%s_comp.root", "%s", etaslices, (25,100) )
            # Serialize
            for h in h2d_el:    outfile.WriteTObject(h)

        elif lep=='mu':

            h2d_mu = [ make2D(outfile,"FR_FullSel_mu_"+X, ptbins, etabins) for X in XsQ ]

            #### Muons: 
            readMany2D(XsQ, h2d_mu, "plots/fake-rate/mu/fr_sub_eta_%s_comp.root", "%s", etaslices, (25,100) )
            # Serialize
            for h in h2d_mu:    outfile.WriteTObject(h)

        else: 
             raise RuntimeError, "What analysis (el, mu)??"


        # Plot
        if options.outdir:
            for lep,h2d,xcuts in (("el",h2d_el,[25])),(("mu",h2d_mu,[15])):
               if len(h2d)==0: continue # protection for muons FR, empty for the time being
               for ieta,eta in enumerate(["barrel","endcap"]):
                   effs = [ (n,graphFromXSlice(h,ieta+1)) for (n,h) in zip(Xnices,h2d) ]
                   styles(effs)
                   options.xlines = xcuts
                   print effs
                   stackEffs(options.outdir+"/fr_%s_%s.root"%(lep,eta), None,effs,options)
               variants = makeVariants(h2d[-1])
               for v in variants: outfile.WriteTObject(v, v.GetName())
               for ieta,eta in enumerate(["barrel","endcap"]):
                   effs = [ ('nominal', graphFromXSlice(h2d[-1],ieta+1)) ]
                   for v in variants: 
                     label = v.GetName().rsplit("_",1)[1]
                     effs.append( (label, graphFromXSlice(v,ieta+1) ) )
                   styles(effs)
                   options.xlines = xcuts
                   stackEffs(options.outdir+"/variants_fr_%s_%s.root"%(lep,eta), None,effs,options)
               mcvariants = makeVariants(h2d[-2],h2d[-1])
               for v in mcvariants: outfile.WriteTObject(v, v.GetName())
    outfile.ls()
