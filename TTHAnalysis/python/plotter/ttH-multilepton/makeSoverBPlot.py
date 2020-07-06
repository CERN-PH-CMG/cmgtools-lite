#!/usr/bin/env python                                                                                                                                                                                              
import sys, os
import numpy as np
import ROOT  as r
import pickle
from array import array
from math import log10, sqrt
from tabulate import tabulate
sys.path.append(os.environ['CMSSW_BASE']+ '/CMGTools/python/plotter/ttH-modules/')
from signalExtractionHarvestingConfigs import catsStackYears
from signalExtractionHarvesting        import readNominalAndToys, stackByMapping, tableToNumbers, buildRms, getSoverB
r.gROOT.SetBatch(True)

def doSpam(text,x1,y1,x2,y2,align=12,fill=False,textSize=0.033,_noDelete={}):
    cmsprel = r.TPaveText(x1,y1,x2,y2,"NDC");
    cmsprel.SetTextSize(textSize);
    cmsprel.SetFillColor(0);
    cmsprel.SetFillStyle(1001 if fill else 0);
    cmsprel.SetLineStyle(2);
    cmsprel.SetLineColor(0);
    cmsprel.SetTextAlign(align);
    cmsprel.SetTextFont(42);
    cmsprel.AddText(text);
    cmsprel.Draw("same");
    _noDelete[text] = cmsprel; ## so it doesn't get deleted by PyROOT
    return cmsprel


from optparse import OptionParser
parser = OptionParser()

parser.add_option('--reloadToys', dest='reloadToys',action='store_true',default=False)
parser.add_option('--redoStack', dest='redoStack',action='store_true',default=False)
parser.add_option('--fittype', dest='fittype',type="string",default="fit_s")
parser.add_option('--fitdiagnostics', dest='fitdiagnostics',type="string",default="/nfs/fanae/user/sscruz/Combine/CMSSW_10_2_13/src/postfit_tests/fitDiagnostics_shapes_combine_combo_ttHmultilep_cminDefaultMinimizerStrategy0robustHesse_MINIMIZER_analytic_fixXtrg.root")
parser.add_option('--toys', dest='toys',type="string",default="/nfs/fanae/user/sscruz/Combine/CMSSW_10_2_13/src/postfit_tests/toys/toys_{fit}{toy}.root")

(options, args) = parser.parse_args()

if options.redoStack:
    results,data=readNominalAndToys(options.fitdiagnostics, options.toys,fit=options.fittype,readFromPickle=(not options.reloadToys))
else:
    results=None; data=None

results, data=stackByMapping( results, data, catsStackYears, 'stack_soverb', readFromPickle=(not options.redoStack))
#print results
points=getSoverB(results,data, [x for x in catsStackYears],['ttH','tH'])
print 'hola'
bins=[-5,-3,-2.5,-2,-1.5,-1.,-0.5,0.5]

hData=r.TH1F('data','',len(bins)-1, array('d',bins))
hBkg =r.TH1F('hbkg','',len(bins)-1, array('d',bins))
htth =r.TH1F('htth','',len(bins)-1, array('d',bins))
hth =r.TH1F('hth'  ,'',len(bins)-1, array('d',bins))

binlist={} # we dont plug migrations (they would depend on signal uncertainties also)
for cat, bin, data,bkg,sigs in points['nom']:
    if not bkg: continue
    sig=0; 
    for s in sigs:
        sig+=sigs[s]
    
    histbin = hData.FindBin( log10(sig/bkg))
    binlist[(cat,bin)]=histbin
    hData.AddBinContent(histbin, data)
    hBkg.AddBinContent(histbin, bkg)
    htth.AddBinContent(histbin, sigs.get('ttH',0))
    hth.AddBinContent(histbin, sigs.get('tH',0))

toylist=[]
print binlist
for toy in range(100):
    hbkg =r.TH1F('hbkg_toy%d'%toy,'',len(bins)-1, array('d',bins))
    for cat, bin, data,bkg,sigs in points['toy_%d'%toy]:
        if not bkg: continue
        hbkg.AddBinContent(binlist[(cat,bin)], bkg)
    toylist.append( hbkg)

bkg_err=hBkg.Clone('bkg_err')
for bin in range(1,hData.GetNbinsX()+1):
    mean=sum([ x.GetBinContent(bin) for x in toylist ])/100.
    toyvalues=[x.GetBinContent(bin)-mean for x in toylist]
    dn = abs(np.percentile(np.array(toyvalues), 16))
    up = np.percentile(np.array(toyvalues), 84)
    bkg_err.SetBinError(bin, (up+dn)/2 ) 

r.gROOT.ProcessLine(".x tdrstyle.cc")
r.gStyle.SetOptStat(0)
r.gStyle.SetOptTitle(0)
r.gStyle.SetErrorX(0.5)

htth.SetFillColor(2)
hth.SetFillColor(r.kBlue)
htth.SetLineColor(2)
hth.SetLineColor(r.kBlue)
hBkg.SetLineColor(r.kBlack)
hBkg.SetFillColorAlpha(r.kWhite, 0)
bkg_err.SetMarkerSize(0)
bkg_err.SetMarkerColorAlpha(r.kWhite, 0);
bkg_err.SetFillColorAlpha(12, 0.40)

plotformat = (600,600)
sf = 20./plotformat[0]
height = plotformat[1]+150
c1 = r.TCanvas("canvas", 'canvas', plotformat[0], height)

hData.GetXaxis().SetTitleFont(42)
hData.GetXaxis().SetTitleSize(0.05)
hData.GetXaxis().SetTitleOffset(1.1)
hData.GetXaxis().SetLabelFont(42)
hData.GetXaxis().SetLabelSize(0.05)
hData.GetXaxis().SetLabelOffset(0.007)
hData.GetYaxis().SetTitleFont(42)
hData.GetYaxis().SetTitleSize(0.06)
hData.GetYaxis().SetTitleOffset(0.9)
hData.GetYaxis().SetLabelFont(42)
hData.GetYaxis().SetLabelSize(0.05)
hData.GetYaxis().SetLabelOffset(0.007)
hData.GetYaxis().SetTitle('Events')
hData.GetXaxis().SetTitle('log_{10}(S/B)')
hData.GetXaxis().SetNdivisions(510)

grData = r.TGraphAsymmErrors(hData.GetNbinsX())
for i in range(hData.GetNbinsX()):
    grData.SetPoint(i, hData.GetXaxis().GetBinCenter(i+1), hData.GetBinContent(i+1))
    grData.SetPointEXhigh(i, hData.GetXaxis().GetBinWidth(i+1)/2)
    grData.SetPointEXlow(i, hData.GetXaxis().GetBinWidth(i+1)/2)
    grData.SetPointEYhigh(i, hData.GetBinError(i+1))
    grData.SetPointEYlow(i, hData.GetBinError(i+1))
grData.SetMarkerStyle(r.kFullCircle)
topsize = 0.12*600./height

c1.SetWindowSize(plotformat[0] + (plotformat[0] - c1.GetWw()), (plotformat[1]+150 + (plotformat[1]+150 - c1.GetWh())));
p1 = r.TPad("pad1","pad1",0,0.30,1,1);
p1.SetTopMargin(p1.GetTopMargin()*1.1);
p1.SetBottomMargin(0.0);
p1.Draw();
p2 = r.TPad("pad2","pad2",0,0,1,0.30);
p2.SetTopMargin(0.0);
p2.SetBottomMargin(0.32);
p2.SetFillStyle(0);
p2.Draw();
p1.cd();


stack = r.THStack('stack','stack')
stack.Add(hBkg)
stack.Add(hth)
stack.Add(htth)
hData.SetMarkerStyle(r.kFullCircle)

hData.Draw('P,e')
stack.Draw('hist,same')
bkg_err.Draw('e2,same')
bkg_err.SetLineColorAlpha(r.kWhite,1)
hData.Draw('P,e,same')
grData.Draw("P,e,same")
p1.SetLogy()

leg=r.TLegend(0.3,0.15,0.55,0.45)
leg.AddEntry(grData,'Data','pel')
leg.AddEntry(htth,'ttH (#mu=#hat{#mu})','f')
leg.AddEntry(hth,'tH (#mu=#hat{#mu})','f')
leg.AddEntry(hBkg,'Background','f')
leg.AddEntry(bkg_err,'Background unc.','f')
leg.SetFillColor(0)
leg.SetShadowColor(0)
leg.SetLineColor(0)
leg.SetTextFont(42)
leg.SetTextSize(0.045)

leg.Draw('same')


offset=0.09
doSpam('#scale[1.1]{#bf{CMS}} #scale[0.9]{#it{Preliminary}}',0.07+offset,.975,.6+offset,.975,align=12,textSize=0.045)
offset=0.60
doSpam('137 fb^{-1} (13 TeV)',0.07+offset,.975,.6+offset,.975,align=12, textSize=0.045)


p1.RedrawAxis('G')
p1.RedrawAxis()

p2.cd()

data_ratio=hData.Clone('ratio')


bkg_noerr=bkg_err.Clone('bkg_noerr')
bkg_ratio=bkg_err.Clone('bkg_ratio')
for i in range(1,bkg_noerr.GetNbinsX()+1):
    bkg_noerr.SetBinError(i,0)
    cont=bkg_ratio.GetBinContent(i); err=bkg_ratio.GetBinError(i)
    bkg_ratio.SetBinContent(i,0); bkg_ratio.SetBinError(i, err/cont)
data_ratio.Add(bkg_noerr,-1)
data_ratio.Divide(bkg_noerr)
ratio_hth = hth .Clone('ratio_hth')
ratio_htth = htth.Clone('ratio_htth')
grDataRatio = r.TGraphAsymmErrors(hData.GetNbinsX())
for i in range(hData.GetNbinsX()):
    grDataRatio.SetPoint(i, data_ratio.GetXaxis().GetBinCenter(i+1), data_ratio.GetBinContent(i+1))
    grDataRatio.SetPointEXhigh(i, data_ratio.GetXaxis().GetBinWidth(i+1)/2)
    grDataRatio.SetPointEXlow(i, data_ratio.GetXaxis().GetBinWidth(i+1)/2)
    grDataRatio.SetPointEYhigh(i, data_ratio.GetBinError(i+1))
    grDataRatio.SetPointEYlow(i, data_ratio.GetBinError(i+1))
grDataRatio.SetMarkerStyle(r.kFullCircle)

ratio_htth.Divide(bkg_noerr)
ratio_hth .Divide(bkg_noerr)
ratio_stack = r.THStack('ratio_stack','ratio_stack')
ratio_stack.Add(ratio_hth)
ratio_stack.Add(ratio_htth)




data_ratio.GetXaxis().SetTitleFont(42)
data_ratio.GetXaxis().SetTitleSize(0.14)
data_ratio.GetXaxis().SetTitleOffset(1.0)
data_ratio.GetXaxis().SetLabelFont(42)
data_ratio.GetXaxis().SetLabelSize(0.1)
data_ratio.GetXaxis().SetLabelOffset(0.015)
data_ratio.GetYaxis().SetNdivisions(505)
data_ratio.GetYaxis().SetTitleFont(42)
data_ratio.GetYaxis().SetTitleSize(0.14)

data_ratio.GetYaxis().SetTitleOffset(0.55)
data_ratio.GetYaxis().CenterTitle()
data_ratio.GetYaxis().SetLabelFont(42)
data_ratio.GetYaxis().SetLabelSize(0.11)
data_ratio.GetYaxis().SetLabelOffset(0.01)
data_ratio.GetYaxis().SetDecimals(True) 
data_ratio.GetYaxis().SetTitle('#frac{Data-Bkg.}{Bkg.}')
data_ratio.GetXaxis().SetTitle('log_{10}(S/B)')
data_ratio.GetYaxis().SetRangeUser(-1.2,1.2)
r.gStyle.SetErrorX(0.5)

data_ratio.Draw('p')
ratio_stack.Draw('hist,same')
bkg_ratio.SetLineColor(r.kBlack)
bkg_ratio.Draw('l,same')

bkg_ratio.Draw('e2,same')
data_ratio.Draw('a,p,same')
grDataRatio.Draw("P,E,same")


p2.RedrawAxis('G')
p2.RedrawAxis()

c1.SaveAs('test.pdf')
c1.SaveAs('test.png')
