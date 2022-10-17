from math import *
import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gROOT.ProcessLine(".x tdrstyle.cc")
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetErrorX(0.5)

txtdata="""
		sf	stat	bkg	mc_stat
MG_NLO	IVF	0.821	0.044	0.14	0.04
MG_NLO	softMu	0.954	0.108	0.169	0.086
MG_NLO	Ratio	0.86	0.108	0.211	0.088
Powh	IVF	0.883	0.048	0.155	0.016
Powh	softMu	0.911	0.101	0.137	0.033
Powh	Ratio	0.969	0.119	0.224	0.039
Powh_New	IVF	0.887	0.048	0.151	0.016
Powh_New	softMu	0.922	0.103	0.147	0.034
Powh_New	Ratio	0.962	0.119	0.225	0.04
MG_LO	IVF	0.906	0.049	0.162	0.03
MG_LO	softMu	0.909	0.103	0.161	0.064
MG_LO	Ratio	0.997	0.125	0.251	0.078
MG_LO_Fast	Ratio	0.752	0.089	0.156	0.052
MG_LO_Fast	IVF	0.731	0.04	0.135	0.025
MG_LO_Fast	softMu	0.971	0.102	0.089	0.058
"""

data = {}
for line in txtdata.split("\n"):
    fields = line.strip().split()
    if len(fields) != 6: continue
    (gen,kind) = fields[:2]
    (sf,stat,bkg,mcst) = map(float,fields[2:])
    if kind not in data: data[kind] = []
    data[kind].append( (gen, (sf,stat,bkg,mcst)) )


c1 = ROOT.TCanvas("c1","c1")
c1.SetBottomMargin(0.25)
for kind,gens in data.iteritems():
    ngens = len(gens)
    hist   = ROOT.TH1F("none", "all",ngens,0,ngens);
    hist_a = ROOT.TH1F("all",  "all",ngens,0,ngens);
    hist_u = ROOT.TH1F("all_u","all",ngens,0,ngens);
    hist_c = ROOT.TH1F("all_c","all",ngens,0,ngens);
    hist_a.GetXaxis().SetBit(hist_a.GetXaxis().kLabelsVert)
    for b,(gen,(sf,stat,bkg,mcst)) in enumerate(gens):
        hist_a.GetXaxis().SetBinLabel(b+1,gen.replace("_"," "))
        for h in hist, hist_a, hist_u, hist_c:
            h.SetBinContent(b+1, sf)
        hist.SetBinError(b+1,0)
        hist_a.SetBinError(b+1,sqrt(stat**2+bkg**2+mcst**2))
        hist_u.SetBinError(b+1,mcst)
        hist_c.SetBinError(b+1,sqrt(stat**2+bkg**2))
    hist_a.SetFillColor(ROOT.kGreen)
    hist_c.SetFillColor(ROOT.kOrange-2)
    hist_u.SetFillColor(ROOT.kRed-4)
    hist_a.Draw("E2")
    hist_c.Draw("E2 SAME")
    hist_u.Draw("E2 SAME")
    hist.Draw("HIST SAME")
    hist_a.Draw("AXIS SAME")
    hist_a.GetYaxis().SetDecimals(True)
    line = ROOT.TLine()
    line.SetLineWidth(3)
    line.SetLineStyle(7)
    line.DrawLine(0,1,ngens,1)
    mcnorm = sum( 1/mcst**2 for (gen,(sf,stat,bkg,mcst)) in gens if "Fast" not in gen)
    mcavg  = sum(sf/mcst**2 for (gen,(sf,stat,bkg,mcst)) in gens if "Fast" not in gen)/mcnorm
    mcerr  = sqrt(1.0/mcnorm)
    line.SetLineColor(ROOT.kViolet+1)
    line.SetLineStyle(1)
    line.SetLineWidth(3)
    line.DrawLine(0,mcavg,ngens-1,mcavg)
    c1.Print(kind+".png")
    
