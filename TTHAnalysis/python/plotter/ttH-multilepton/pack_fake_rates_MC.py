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

def fillSliceY(th2,plot1d,yvalue):
    ybin = th2.GetYaxis().FindBin(yvalue)
    for xbin in xrange(1,th2.GetNbinsX()+1):
        xval = th2.GetXaxis().GetBinCenter(xbin)
        for i in xrange(plot1d.GetN()):
            x,xp,xm = plot1d.GetX()[i], plot1d.GetErrorXhigh(i), plot1d.GetErrorYlow(i)
            if x-xm <= xval and xval <= x+xp:
                th2.SetBinContent(xbin,ybin,plot1d.GetY()[i])
                th2.SetBinError(xbin,ybin,max(plot1d.GetErrorYlow(i),plot1d.GetErrorYhigh(i)))
def readSliceY(th2,filename,plotname,yvalue):
    slicefile = ROOT.TFile.Open(filename)
    if not slicefile: raise RuntimeError, "Cannot open "+filename
    plot = slicefile.Get(plotname)
    if not plot: 
        slicefile.ls()
        raise RuntimeError, "Cannot find "+plotname+" in "+filename
    fillSliceY(th2,plot,yvalue)
    slicefile.Close()
def assemble2D(out,name,xedges,yedges,filepattern,plotname,yslices):
    out.cd()
    th2 = makeH2D(name,xedges,yedges)
    for yvalue,yname in yslices:
        readSliceY(th2,filepattern%yname,plotname,yvalue)
    out.WriteTObject(th2)
    return th2
    
if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser(usage="%prog [options] what path out")
    parser.add_option("-s", "--sel", dest="sel", default=None, help="Select");
    (options, args) = parser.parse_args()
    (what,path,outname) = args
    outfile = ROOT.TFile.Open(outname,"RECREATE")
    if what == "mvaTTH":
       ptbins_c = [ 10,15,20,30,45,65,100 ]
       etabins_c_el = [0, 1.479, 2.5]
       etabins_c_mu = [0, 1.2,   2.4]
       etaslices_c_el = [ (0.4,"00_15"), (1.8,"15_24") ]
       etaslices_c_mu = [ (0.4,"00_12"), (1.8,"12_24") ]
       for WP in "075ibf30E",: #,"060ib":
           WP0 = re.sub(r"^(\d+).*",r"\1",WP)   # for binning
           WP1 = re.sub(r"^(\d+i?).*",r"\1",WP) # for numerator
           num = "mvaPt_"+WP1
           ptj = "ptJI_mvaPt%s_coarse" % WP0
           ptj2 = "ptJI85_mvaPt%s_coarse" % WP0
           for ptBin in "",:
               for src in "QCDMu", "TT": 
                    assemble2D(outfile,"FR_wp%s_mu_%s_%s%s" % (WP,src,ptj,ptBin), ptbins_c, etabins_c_mu, path+"/mu_wp"+WP+"_rec30_bAny_eta_%s"+ptBin+".root", num+"_"+ptj2+"_"+src+"_red", etaslices_c_mu)
           for ptBin in "",:
               for src in "QCDEl", "TT": 
                    assemble2D(outfile,"FR_wp%s_el_%s_%s%s" % (WP,src,ptj,ptBin), ptbins_c, etabins_c_el, path+"/el_wp"+WP+"_rec30_bMedium_eta_%s"+ptBin+".root", num+"_"+ptj2+"_"+src+"_red", etaslices_c_el)
    outfile.ls()
