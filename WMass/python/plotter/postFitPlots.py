#!/usr/bin/env python
# usage: python postFitPlots.py localplots/templates cards/helicity_2018_01_25_eta48pt20/Wel_plus_shapes.root x ~/w/wmass/fit/CMSSW_8_1_0/src/fitDiagnostics.root Wel w-helicity-13TeV/wmass_e/wenu_plots.txt --rollback2D etaPt

import ROOT
ROOT.gROOT.SetBatch(True)

from math import *
from os.path import dirname,basename
from CMGTools.TTHAnalysis.tools.plotDecorations import *
from CMGTools.WMass.plotter.mcPlots import *

mergeMap = { 
#    "ttH_hww" : "ttH",
#    "ttH_hzz" : "ttH",
#    "ttH_htt" : "ttH",
#    "TTWW" : "RARE",
#    "TBZ" : "RARE",
#    "WWqq" : "RARE",
#    "WWDPI" : "RARE",
#    "VVV" : "RARE",
#    "TTGStar" : "TTZ",
}

def roll1Dto2D(h1d,h2dname,plotfile,options):
    pfile = PlotFile(plotfile,options)
    pspecs = pfile.plots()
    matchspec = [ p for p in pspecs if p.name == h2dname ]
    if not matchspec: raise RuntimeError, "Error: plot %s not found" % h2dname
    if len(matchspec)>1: print "WARNING! more than one plot matching %s. Taking the specifics from the first occurence in plotfile %s" % (h2dname,plotfile)
    p2d = matchspec[0]
    histo = makeHistFromBinsAndSpec("%s_%s" % (h2dname,h1d.GetName()),p2d.expr,p2d.bins,None)
    histo.GetYaxis().SetTitle(p2d.getOption('YTitle'))
    histo.GetXaxis().SetTitle(p2d.getOption('XTitle'))
    histo.SetContour(100)
    ROOT.gStyle.SetPaintTextFormat(p2d.getOption("PaintTextFormat","g"))
    histo.SetMarkerSize(p2d.getOption("MarkerSize",1))
    if p2d.hasOption('ZMin') and p2d.hasOption('ZMax'):
        histo.GetZaxis().SetRangeUser(p2d.getOption('ZMin',1.0), p2d.getOption('ZMax',1.0))
    if 'TH2' not in histo.ClassName(): raise RuntimeError, "Trying to roll the 1D histo on something that is not TH2"
    for i in xrange(1,h1d.GetNbinsX()+1):
        xbin = i % histo.GetNbinsX()
        if not xbin: xbin = xbin+histo.GetNbinsX()
        ybin = i / histo.GetNbinsX() + (1 if i%histo.GetNbinsX() else 0)
        val = h1d.GetBinContent(i)
        if val>1.0: histo.SetBinContent(xbin,ybin,h1d.GetBinContent(i))
    return histo

options = None
if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser(usage="%prog [options] plotdir shapesfile varname mlfile channel plots.txt [onlyNorm]")
    addPlotMakerOptions(parser)
    parser.add_option("--do-stack", dest="doStack", action="store_true", default=False, help="do the stack plot of all the processes and compare with data")
    parser.add_option("--rollback2D", dest="rollBackTo2D", type='string', default=None, help="roll back to 2D. It uses the option variable, which has to be in plots.txt")
    (options, args) = parser.parse_args()
    #options.path = ["/data1/emanuele/wmass/TREES_1LEP_80X_V3_WENUSKIM_V3/"]
    options.lumi = 35.9
    basedir = args[0]
    infile = ROOT.TFile(args[1]);
    var    = args[2];
    mlfile = ROOT.TFile(args[3]);
    channel = args[4];
    plotfile = args[5];
    onlynorm = (len(args)>6 and args[6]=='onlyNorm')
    ROOT.gROOT.ProcessLine(".x /afs/cern.ch/user/g/gpetrucc/cpp/tdrstyle.cc(0)")
    ROOT.gROOT.ForceStyle(False)
    ROOT.gStyle.SetErrorX(0.5)
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetPaperSize(20.,25.)
    for O,MLD in ("prefit","prefit"), ("postfit_s","fit_s"):
      print "NOW PLOTTING ",O," ..."
      normset = mlfile.Get("norm_"+MLD)
      mldir  = mlfile.GetDirectory("shapes_"+MLD);
      if not mldir: raise RuntimeError, mlfile
      outfile = ROOT.TFile(basedir + "/"+O+".root", "RECREATE")
      processes = ['_'.join(p.GetName().split('_')[1:]) for p in infile.GetListOfKeys()]
      #print "prima ",processes,"\n"
      processes = filter(lambda x: not re.match('(.*Up|.*Down|data\_obs)',x),processes)
      #print "dopo: ",processes
      hdata = infile.Get(var+"_data_obs")
      htot = hdata.Clone(var+"_total")
      htot.Reset()
      stack = ROOT.THStack(var+"_stack","")
      plots = {'data':hdata}
      if options.poisson:
            pdata = getDataPoissonErrors(hdata, False, True)
            hdata.poissonGraph = pdata ## attach it so it doesn't get deleted
      for p in processes:
        pout = mergeMap[p] if p in mergeMap else p
        h = infile.Get(var+"_"+pout)
        if not h: 
            print "Missing %s_%s for %s" % (var,pout, p)
            continue
        h = h.Clone(var+"_"+p)
        h.SetDirectory(0)
        hpf = mldir.Get("%s/%s" % (channel,p))
        hpn = normset.find("%s/%s" % (channel,p))
        if not hpf: 
            if h.Integral() > 0 and p not in mergeMap: raise RuntimeError, "Could not find post-fit shape for %s" % p
            continue
        if not hpn:
            if h.Integral() > 0 and p not in mergeMap: raise RuntimeError, "Could not find post-fit normalization for %s" % p
        if onlynorm:
            prev_integral = h.Integral()
            scale_content = hpn.getVal()/prev_integral
            for b in xrange(1, h.GetNbinsX()+1):
                h.SetBinContent(b, h.GetBinContent(b)*scale_content)
                h.SetBinError(b, h.GetBinError(b)*scale_content)
        else:
            for b in xrange(1, h.GetNbinsX()+1):
                h.SetBinContent(b, hpf.GetBinContent(b))
                h.SetBinError(b, hpf.GetBinError(b))
        print 'adding',p,'with norm',h.Integral()
        if pout in plots:
            plots[pout].Add(h)
            htot.Add(h)
        else: 
            plots[pout] = h
            htot.Add(h)
            h.SetName(var+"_"+pout)
            stack.Add(h)
      htotpf = mldir.Get(channel+"/total")
#      hbkg = hdata.Clone(var+"_total_background")
#      hbkgpf = mldir.Get(channel+"/total_background")
      print 'tot norm is ',htot.Integral()
      if onlynorm:
          hpn = normset.find("%s/total" % channel)
          rel_error = hpn.getError()/hpn.getVal()
          print rel_error
          for b in xrange(1, htot.GetNbinsX()+1):
              htot.SetBinError(b, hypot(htot.GetBinError(b),htot.GetBinContent(b)*rel_error))
      else:
          for b in xrange(1, h.GetNbinsX()+1):
              htot.SetBinContent(b, htotpf.GetBinContent(b))
              htot.SetBinError(b, htotpf.GetBinError(b))
#          hbkg.SetBinContent(b, hbkgpf.GetBinContent(b))
#          hbkg.SetBinError(b, hbkgpf.GetBinError(b))
      doRatio = True
      htot.GetYaxis().SetRangeUser(0, 1.8*max(htot.GetMaximum(), hdata.GetMaximum()))
      ## Prepare split screen
      plotformat = (600,600)
      c1 = ROOT.TCanvas("c1", "c1", plotformat[0], plotformat[1]); c1.Draw()
      c1.SetWindowSize(plotformat[0] + (plotformat[0] - c1.GetWw()), (plotformat[1] + (plotformat[1] - c1.GetWh())));
      p1 = ROOT.TPad("pad1","pad1",0,0.29,1,0.99);
      p1.SetBottomMargin(0.03);
      p1.Draw();
      if options.doStack:
          p2 = ROOT.TPad("pad2","pad2",0,0,1,0.31);
          p2.SetTopMargin(0);
          p2.SetBottomMargin(0.3);
          p2.SetFillStyle(0);
          p2.Draw();
          p1.cd();
          ## Draw absolute prediction in top frame
          htot.Draw("HIST")
          #htot.SetLabelOffset(9999.0);
          #htot.SetTitleOffset(9999.0);
          stack.Draw("HIST F SAME")
          if options.showMCError:
              totalError = doShadedUncertainty(htot)
          if options.poisson:
            hdata.poissonGraph.Draw("PZ SAME")
          else:
            hdata.Draw("E SAME")
          htot.Draw("AXIS SAME")
      else:
          for h in plots.values() + [htot]:
              if options.rollBackTo2D:
                  c1.SetRightMargin(0.20)
                  h2d = roll1Dto2D(h,options.rollBackTo2D,plotfile,options)
                  h2d.Draw("COLZ0")
                  outfile.WriteTObject(h2d)
              else:
                  h.GetXaxis().SetTitle("rolled bin number")
                  h.Draw("HIST")
                  if options.showMCError:
                      totalError = doShadedUncertainty(p)
                  outfile.WriteTObject(h)
              doTinyCmsPrelim(hasExpo = False,textSize=(0.045 if doRatio else 0.033), xoffs=-0.03,
                              textLeft = options.lspam, textRight = options.rspam, lumi = options.lumi)
              
              c1.cd()
              c1.Print("%s/%s_%s.png" % (basedir,O,h.GetName()))
              c1.Print("%s/%s_%s.pdf" % (basedir,O,h.GetName()))              
      ## Draw relaive prediction in the bottom frame
      if options.doStack:
          p2.cd() 
          rdata,rnorm,rnorm2,rline = doRatioHists(PlotSpec(var,var,"",{}), plots, htot, htot, maxRange=options.maxRatioRange, fixRange=options.fixRatioRange,
                                                  fitRatio=options.fitRatio, errorsOnRef=options.errorBandOnRatio,
                                                  ratioNums=options.ratioNums, ratioDen=options.ratioDen, ylabel="Data/pred.", doWide=options.wideplot, showStatTotLegend=False)
          c1.cd()
          c1.Print("%s/%s_%s.png" % (basedir,O,var))
          c1.Print("%s/%s_%s.pdf" % (basedir,O,var))
      del c1
      outfile.Close()
