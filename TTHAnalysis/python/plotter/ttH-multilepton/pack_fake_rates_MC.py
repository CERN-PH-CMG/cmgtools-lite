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
        print th2
        print filepattern
        print yname
        print plotname
        print yvalue
        readSliceY(th2,filepattern%yname,plotname,yvalue)
    out.WriteTObject(th2)
    return th2
    
if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser(usage="%prog [options] path out")
    parser.add_option("-s", "--sel", dest="sel", default=None, help="Select");
    (options, args) = parser.parse_args()
    (path,outname) = args
    outfile = ROOT.TFile.Open(outname,"RECREATE")
    if True:

       ptbins_c = [ 10,15,20,30,45,100 ]
       etabins_c_el = [0, 1.479, 2.5]
       etabins_c_mu = [0, 1.2,   2.4]
       etaslices_c_el = [ (0.4,"00_15"), (1.8,"15_25") ]
       etaslices_c_mu = [ (0.4,"00_12"), (1.8,"12_24") ]
       torun = []
#       torun += [("sViX4E2","ptJIMIX_mvaSusy_sVi","mvaSusy_sVi","30"),("sMiX4E2","ptJIMIX2_mvaSusy_sMi","mvaSusy_sMi","30")]
       torun += [("RA7E2","conePt_RA7","ra7_tight","40")]
#       torun += [("sViX4vE2","ptJIMIX_mvaSusy_sVi","mvaSusy_sVi","30"),("sMiX4vE2","ptJIMIX2_mvaSusy_sMi","mvaSusy_sMi","30")]
#       torun += [("sViX0E2","ptJI85_mvaSusy_sVi","mvaSusy_sVi","30"),("sMiX0E2","ptJI85_mvaSusy_sMi","mvaSusy_sMi","30")]
       torun += [("sViX4mrE2","ptJIMIX3_mvaSusy_sVi","mvaSusy_sVi","30"),("sMiX4mrE2","ptJIMIX4_mvaSusy_sMi","mvaSusy_sMi","30")]

       for WP,ptj,num,rec in torun:
           assemble2D(outfile,"FR_wp%s_mu_%s_%s" % (WP,'QCDMu',ptj), ptbins_c, etabins_c_mu, path+"/mu_lbin_wp"+WP+"_rec"+rec+"_bAny_eta_%s.root", num+"_"+ptj+"_coarselongbin_QCDMu_red", etaslices_c_mu)
           assemble2D(outfile,"FR_wp%s_el_%s_%s" % (WP,'QCDEl',ptj), ptbins_c, etabins_c_el, path+"/el_lbin_wp"+WP+"_rec"+rec+"_bAny_eta_%s.root", num+"_"+ptj+"_coarselongbin_QCDEl_red", etaslices_c_el)
           assemble2D(outfile,"FR_wp%s_mu_%s_%s" % (WP,'TT',ptj), ptbins_c, etabins_c_mu, path+"/mu_lbin_wp"+WP+"_rec"+rec+"_bAny_eta_%s.root", num+"_"+ptj+"_coarselongbin_TT_red", etaslices_c_mu)
           assemble2D(outfile,"FR_wp%s_el_%s_%s" % (WP,'TT',ptj), ptbins_c, etabins_c_el, path+"/el_lbin_wp"+WP+"_rec"+rec+"_bAny_eta_%s.root", num+"_"+ptj+"_coarselongbin_TT_red", etaslices_c_el)

    outfile.ls()

