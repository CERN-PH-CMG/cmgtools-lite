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
            msg = "trying to fill %s bin %2d x %5.1f from %s: " % (th2.GetName(), xbin, xval, plot1d.GetName())
            found = "Not found!!"
            if "TGraph" in plot1d.ClassName():
                for i in xrange(plot1d.GetN()):
                    x,xp,xm = plot1d.GetX()[i], plot1d.GetErrorXhigh(i), plot1d.GetErrorYlow(i)
                    if x-xm <= xval and xval <= x+xp:
                        th2.SetBinContent(xbin,ybin,plot1d.GetY()[i])
                        th2.SetBinError(xbin,ybin,max(plot1d.GetErrorYlow(i),plot1d.GetErrorYhigh(i)))
                        found = "bin %d x %5.1f endpoints [%5.1f, %5.1f], fr = %.3f +- %.3f" % (i, x, x-xm,x+xp, th2.GetBinContent(xbin,ybin), th2.GetBinError(xbin,ybin))
            elif "TH1" in plot1d.ClassName():
                for i in xrange(1,plot1d.GetNbinsX()+1):
                    x,xh,xl = plot1d.GetXaxis().GetBinCenter(i), plot1d.GetXaxis().GetBinUpEdge(i), plot1d.GetXaxis().GetBinLowEdge(i)
                    if xl <= xval and xval <= xh:
                        th2.SetBinContent(xbin,ybin,plot1d.GetBinContent(i))
                        th2.SetBinError(xbin,ybin,plot1d.GetBinError(i))
                        found = "bin %d x %5.1f endpoints [%5.1f, %5.1f], fr = %.3f +- %.3f" % (i, x, xl, xh, th2.GetBinContent(xbin,ybin), th2.GetBinError(xbin,ybin))
            else: raise RuntimeError()
            if "Not" in found:
                print msg, found
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

def makeVariants(h,altsrc=None,norm=None):
    lptmin = log(h.GetXaxis().GetBinCenter(1))
    lptmax = log(h.GetXaxis().GetBinCenter(h.GetNbinsX()))
    lptc     = 0.5*(lptmax+lptmin)
    lptslope = 1.0/(lptmax-lptc)
    shifters = [
        ("up"  ,  lambda pt,eta,fr,err : min(fr+err, 1.0) ),
        ("down",  lambda pt,eta,fr,err : max(fr-err, 0.05*fr) ),
        ("pt1" ,  lambda pt,eta,fr,err : min(max( fr + err * lptslope*(log(pt)-lptc),  0.05*fr),1.0) ),
        ("pt2" ,  lambda pt,eta,fr,err : min(max( fr - err * lptslope*(log(pt)-lptc),  0.05*fr),1.0) ),
        ("be1" ,  lambda pt,eta,fr,err : min(max( fr + err*0.707 if eta < 1.3 else fr-err*0.707, 0.05*fr),1.0) ), 
        ("be2" ,  lambda pt,eta,fr,err : min(max( fr - err*0.707 if eta < 1.3 else fr+err*0.707, 0.05*fr),1.0) ),
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
                    if altsrc.GetBinContent(bx,by) <= 0:
                        print "Warning: in %s, pt %4.1f, eta %3.1f: nominal %.4f +- %.4f , alternate %.4f +- %.4f  "  % (hsyst.GetName(), x, y, fr0, err, altsrc.GetBinContent(bx,by), altsrc.GetBinError(bx,by))
                    else:
                        err = fr0 * altsrc.GetBinError(bx,by)/altsrc.GetBinContent(bx,by)
                fr = func(x,y,fr0,err)
                #print "Variation %-15s: pt %4.1f, eta %3.1f: nominal %.3f +- %.3f --> shifted %.3f "  % (hsyst.GetName(), x, y, fr0, err, fr)
                hsyst.SetBinContent(bx, by, fr)
                hsyst.SetBinError(bx, by, 0)
        if norm and s not in ("up","down"):
            sum0, sums = 0, 0
            for bx in xrange(1,h.GetNbinsX()+1):
                x = h.GetXaxis().GetBinCenter(bx) 
                binw = h.GetXaxis().GetBinWidth(bx)
                #if x <= 15: continue
                for by in xrange(1,h.GetNbinsY()+1):
                    f0, f = h.GetBinContent(bx,by), hsyst.GetBinContent(bx,by)
                    sum0 += norm.GetBinContent(bx,by) * binw * f0/(1-f0)
                    sums += norm.GetBinContent(bx,by) * binw * f /(1-f) 
                    #print "     at bx %2d by %2d pt %5.1f abseta %5.2f    N = %9.2f  fr0 = %.3f   fr = %.3f" % (bx,by,x,h.GetYaxis().GetBinCenter(by), norm.GetBinContent(bx,by), f0, f)
            print "   pre-normalization for %s: sum0 %9.2f   sum %9.2f    ratio %.3f " % (hsyst.GetName(), sums, sum0, sums/sum0)
            hsyst.Scale(sum0/sums)
        ret.append(hsyst)
     
    return ret

def fixLastBin(ibin, hdata, hmc=None, blowup=2.0):
    isrc = hdata.GetNbinsX()+ibin
    idst = isrc+1
    for iy in xrange(1,hdata.GetNbinsY()+1):
        fr0 = hdata.GetBinContent(isrc, iy)
        er0 = hdata.GetBinError(isrc, iy)
        if hmc:
            sf = hmc.GetBinContent(idst, iy)/hmc.GetBinContent(isrc, iy)
            print "extrapolate %s from pt %.1f to pt %.1f with SF %.3f from %s" % (hdata.GetName(), hdata.GetXaxis().GetBinCenter(isrc), hdata.GetXaxis().GetBinCenter(idst), sf, hmc.GetName())
            fr0 *= sf; er0 *= sf
        else:
            print "extrapolate %s from pt %.1f to pt %.1f" % (hdata.GetName(), hdata.GetXaxis().GetBinCenter(isrc))
        hdata.SetBinContent(idst, iy, fr0)
        hdata.SetBinError(idst, iy, er0 * blowup)

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
    from CMGTools.TTHAnalysis.plotter.mcEfficiencies import stackEffs, graphFromXSlice
    import os.path
    from optparse import OptionParser
    parser = OptionParser(usage="%prog [options] path out")
    parser.add_option("--pdir", dest="outdir", default="plots/104X/ttH/lepMVA/", help="Output base directory for plots");
    parser.add_option("--xcut", dest="xcut", default=None, nargs=2, type='float', help="X axis cut");
    parser.add_option("--xrange", dest="xrange", default=None, nargs=2, type='float', help="X axis range");
    parser.add_option("--yrange", dest="yrange", default=(0,0.45), nargs=2, type='float', help="Y axis range");
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
    parser.add_option("--shiftPoints", dest="shiftPoints", type="float", default=0.3, help="Shift x coordinates of points by this fraction of the error bar in thew plot to make them more visible when stacking.")

    parser.add_option("--fix-last-bin", dest="fixLastBin", action="store_true", default=False, help="Fudge last bin")
    parser.add_option("--norm", dest="norm", action="store_true", default=False, help="Normalize variations")
    parser.add_option("--mva-version",  dest="mvaVersion",  default="v1.0",  type="string", help="MVA version (common)")
    parser.add_option("--mva-version-mc",   dest="mvaVersionMC",  default=None,  type="string", help="MC MVA version (fr-mc), defaults to common")
    parser.add_option("--mva-version-data", dest="mvaVersionData",  default=None,  type="string", help="Data MVA version (fr-meas), defaults to common")
    parser.add_option("--mva-version-comb", dest="mvaVersionComb",  default=None,  type="string", help="Comb MVA version (fr-comb), defaults to common")
    parser.add_option("-y", "--years", dest="years",  default="2016,2017,2018",  type="string", help="Year: one or more, comma separated, default is 2016,2017,2018")
    (options, args) = parser.parse_args()
    if options.mvaVersionMC is None: options.mvaVersionMC = options.mvaVersion
    if options.mvaVersionData is None: options.mvaVersionData = options.mvaVersion
    if options.mvaVersionComb is None: options.mvaVersionComb = options.mvaVersion

    years = options.years.split(",")

    PlotOut="%s/%s/fr-comb" % ( options.outdir, options.mvaVersionComb)

    if not os.path.exists(PlotOut):
        os.system("mkdir -p "+PlotOut)
        if os.path.exists("/afs/cern.ch"): os.system("cp /afs/cern.ch/user/g/gpetrucc/php/index.php "+PlotOut)
    ROOT.gROOT.ProcessLine(".x tdrstyle.cc")
    ROOT.gStyle.SetOptStat(0)
        

    ptbins_el = [ 15,25,35,45,65,100 ]
    ptbins_mu = [ 10,15,20,32,45,65,100 ]
    etabins_el = [0, 1.479, 2.5]
    etabins_mu = [0, 1.2,   2.4]
    etaslices_el = [ (0.4,"00_15"), (1.8,"15_25") ]
    etaslices_mu = [ (0.4,"00_12"), (1.8,"12_24") ]
    XsQ    = [ "QCD", "data_comb" ]
    Xnices = [ "MC QCD", "Data, comb." ]

    mva_el = "080"
    mva_mu = "085"

    for year in years:
        outname = PlotOut + "/fr_%s.root" % year
        outfile = ROOT.TFile.Open(outname,"RECREATE")

        h2d_el = [ make2D(outfile,"FR_mva"+mva_el+"_el_"+X, ptbins_el, etabins_el) for X in XsQ ]
        h2d_mu = [ make2D(outfile,"FR_mva"+mva_mu+"_mu_"+X, ptbins_mu, etabins_mu) for X in XsQ ]
        h2d_el_tt = [ make2D(outfile,"FR_mva"+mva_el+"_el_TT", ptbins_el, etabins_el) ]
        h2d_mu_tt = [ make2D(outfile,"FR_mva"+mva_mu+"_mu_TT", ptbins_mu, etabins_mu) ]
        h2d_el_tt_norm = [ make2D(outfile,"norm_el_TT", ptbins_el, etabins_el) ]
        h2d_mu_tt_norm = [ make2D(outfile,"norm_mu_TT", ptbins_mu, etabins_mu) ]

        Plots = "%s/%s/fr-meas/qcd1l/" % ( options.outdir, options.mvaVersionData)
        readMany2D(XsQ, h2d_mu, "/".join([Plots, "mu", year,  "HLT_MuX_OR/fakerates-mtW1R/fr_sub_eta_%s_compG.root"]), "%s", etaslices_mu, (10,999) )
        readMany2D(XsQ, h2d_el, "/".join([Plots, "el", year, "HLT_EleX_OR/fakerates-mtW1R/fr_sub_eta_%s_compG.root"]), "%s", etaslices_el, (15,999) )

        if options.fixLastBin:
            fixLastBin(-1, h2d_el[1], h2d_el[0])
            fixLastBin(-1, h2d_mu[1], h2d_mu[0])

        #### TT MC-truth
        MCPlots = "%s/%s/fr-mc/%s" % ( options.outdir, options.mvaVersionMC, year)
        ID="iRun2v1.0";
        XVarBins_mu = "ptJI90_mvaPt"+mva_mu+"_coarsecomb_%s"
        XVarBins_el = "ptJI90_mvaPt"+mva_el+"_coarseelcomb_%s"
        NumXVarBins_mu = "mvaPt_"+mva_mu+"i_"+XVarBins_mu
        NumXVarBins_el = "mvaPt_"+mva_el+"i_"+XVarBins_el
        TT_mu, TT_el = "TT_SS_red", "TT_SS_redNC_pink"
        readMany2D([TT_mu], h2d_mu_tt, "/".join([MCPlots,  "mu_sum_wp"+mva_mu+ID+"_recJet30_eta_%s.root"]),      NumXVarBins_mu, etaslices_mu, (10,999) )
        readMany2D([TT_el], h2d_el_tt, "/".join([MCPlots, "el_sum8_wp"+mva_el+ID+"_recJet30_eta_%s.root"]),      NumXVarBins_el, etaslices_el, (15,999) )
        readMany2D([TT_mu], h2d_mu_tt_norm, "/".join([MCPlots, "mu_ttnorm_wp"+mva_mu+ID+"_recJet30_eta_%s.root"]), XVarBins_mu, etaslices_mu, (15,999) ) #NOTA BENE: we skip the 10-15 bin when normalizing
        readMany2D([TT_el], h2d_el_tt_norm, "/".join([MCPlots, "el_ttnorm_wp"+mva_el+ID+"_recJet30_eta_%s.root"]), XVarBins_el, etaslices_el, (15,999) )

        h2d_el_mc4cc = [ make2D(outfile,"FR_mva"+mva_el+"_el_MC"+X, ptbins_el, etabins_el) for X in ("QCD","QCDNC") ]
        readMany2D(["QCDEl_red_El8", "QCDEl_redNC_El8"],  h2d_el_mc4cc, "/".join([MCPlots, "el_sum8_wp"+ mva_el+ID+"_recJet30_eta_%s.root"]), NumXVarBins_el, etaslices_el, (15,32) )
        readMany2D(["QCDEl_red_El17","QCDEl_redNC_El17"], h2d_el_mc4cc, "/".join([MCPlots, "el_sum17_wp"+mva_el+ID+"_recJet30_eta_%s.root"]), NumXVarBins_el, etaslices_el, (32,999) )
        h2d_el_cc = [ make2D(outfile,"FR_mva"+mva_el+"_el_"+X+"_NC", ptbins_el, etabins_el) for X in XsQ ]
        for hu,hc in zip(h2d_el,h2d_el_cc):
           for ie in xrange(1,len(etabins_el)):
             for ip in xrange(1,len(ptbins_el)):
                 mcratio = h2d_el_mc4cc[1].GetBinContent(ip,ie)/h2d_el_mc4cc[0].GetBinContent(ip,ie)
                 hc.SetBinContent(ip,ie, hu.GetBinContent(ip,ie)*mcratio)
                 hc.SetBinError(ip,ie, hu.GetBinError(ip,ie)*mcratio)
        h2d_el += h2d_el_cc
        Xnices += [ "QCD, #gamma corr", "Data, #gamma corr" ]

        # Serialize
        for h in h2d_el    + h2d_mu:    outfile.WriteTObject(h)
        for h in h2d_el_tt + h2d_mu_tt: outfile.WriteTObject(h)
        for h in h2d_el_tt_norm + h2d_mu_tt_norm: outfile.WriteTObject(h)

        # Plot
        for lep,h2d,h2dtt,h2tt_norm,xcuts in (("el",h2d_el,h2d_el_tt,h2d_el_tt_norm,[30]),("mu",h2d_mu,h2d_mu_tt,h2d_mu_tt_norm,[20,45])):
           for ieta,eta in enumerate(["barrel","endcap"]):
               effs = [ (n,graphFromXSlice(h,ieta+1)) for (n,h) in zip(["MC ttbar"],h2dtt) ]
               effs += [ (n,graphFromXSlice(h,ieta+1)) for (n,h) in zip(Xnices,h2d) ]
               styles(effs)
               options.xlines = xcuts
               savErrorLevel = ROOT.gErrorIgnoreLevel; ROOT.gErrorIgnoreLevel = ROOT.kWarning;
               stackEffs(PlotOut+"/fr_%s_%s_%s.root"%(lep,eta,year), None,effs,options, legHeader = "%s %s, %s" % (lep,eta,year))
               ROOT.gErrorIgnoreLevel = savErrorLevel;
           variants = makeVariants(h2d[-1],norm=(h2tt_norm[0] if options.norm else None))
           for v in variants: outfile.WriteTObject(v, v.GetName())
           for ieta,eta in enumerate(["barrel","endcap"]):
               effs = [ ('nominal', graphFromXSlice(h2d[-1],ieta+1)) ]
               for v in variants: 
                 label = v.GetName().rsplit("_",1)[1]
                 effs.append( (label, graphFromXSlice(v,ieta+1) ) )
               styles(effs)
               options.xlines = xcuts
               savErrorLevel = ROOT.gErrorIgnoreLevel; ROOT.gErrorIgnoreLevel = ROOT.kWarning;
               stackEffs(PlotOut+"/variants_fr_%s_%s_%s.root"%(lep,eta,year), None,effs,options, legHeader = "%s %s, %s" % (lep,eta,year))
               ROOT.gErrorIgnoreLevel = savErrorLevel;
           mcttvariants = makeVariants(h2dtt[0],h2d[-1],norm=(h2tt_norm[0] if options.norm else None))
           for v in mcttvariants: outfile.WriteTObject(v, v.GetName())
           mcvariants = makeVariants(h2d[-2],h2d[-1],norm=(h2tt_norm[0] if options.norm else None))
           for v in mcvariants: outfile.WriteTObject(v, v.GetName())

        outfile.Close()
        print "Saved FR for year %s in %s" % (year, outname)
