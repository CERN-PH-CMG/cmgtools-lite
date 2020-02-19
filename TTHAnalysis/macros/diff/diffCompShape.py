import os
from ROOT import TCanvas, TROOT, TH1D, TH1F, TH2F, TFile, TTree, gROOT, kRed, kGreen, TLegend, gStyle

gROOT.SetBatch(True)
    ## open files 
f1  = TFile("./TTHnobb_fxfx_Friend.root")
if not f1:
    raise ValueError('File not opened')
tr = f1.Get("Friends")
if not tr:
    raise ValueError('Tree not loaded')

comparisonplotlist1 = [
    ["Hreco_pTHvis"     , "0 <= Hreco_pTHvis < 120"     , "Hreco_pTHgen" , "0 <= Hreco_pTHgen < 120"    , "pTH_0_120"       ,20, 0., 120.   ],
]

comparisonplotlist2 = [
    ["Hreco_pTHvis"     , "120 <= Hreco_pTHvis < 200"   , "Hreco_pTHgen" , "120 <= Hreco_pTHgen < 200"  , "pTH_120_200"     ,20, 120., 200. ],
]

comparisonplotlist3 = [
    ["Hreco_pTHvis"     , "200 <= Hreco_pTHvis < 350"   , "Hreco_pTHgen" , "200 <= Hreco_pTHgen < 350"  , "pTH_200_350"     ,20, 200., 350. ],
]

def draw_comparison(var1, cut1, var2, cut2, fname, nbins, lowbin, highbin):
    gStyle.SetOptTitle(0)
    gStyle.SetOptStat("e") 
    c   = TCanvas()
    leg = TLegend(0.6,0.7,0.89,0.89)
    c.cd()
    theplot_1 = TH1F(var1,var1, nbins, lowbin, highbin)
    tr.Draw("%s>>%s"%(var1,var1),cut1)
    theplot_2 = TH1F("%s_2"%var2,var2, nbins, lowbin, highbin) # Avoid issues with same names
    tr.Draw("%s>>%s_2"%(var2,var2),cut2)
    theplot_2.SetLineColor(kRed)
    theplot_1.GetXaxis().SetTitle("pTH(GeV)")
    theplot_1.GetYaxis().SetTitle("a.u.")
    theplot_1.Draw("HIST")
    theplot_1.Scale(1/theplot_1.Integral())
    theplot_2.Draw("HIST SAME")
    theplot_2.Scale(1/theplot_2.Integral())
    leg.AddEntry(theplot_1,"reco_STXS1.1_bin_%s"%(fname))
    leg.AddEntry(theplot_2,"gen_STXS1.1_bin_%s"%(fname))
    leg.Draw()
    c.Print("%s/%s_comp.png"%("./test_compare_stxs/",fname)) # Avoid overwriting single var plots

for var1, cut1, var2, cut2, fname, nbins, lowbin, highbin  in comparisonplotlist1:
    draw_comparison(var1, cut1, var2, cut2, fname, nbins, lowbin, highbin )

for var1, cut1, var2, cut2, fname, nbins, lowbin, highbin  in comparisonplotlist2:
    draw_comparison(var1, cut1, var2, cut2, fname, nbins, lowbin, highbin )

for var1, cut1, var2, cut2, fname, nbins, lowbin, highbin  in comparisonplotlist3:
    draw_comparison(var1, cut1, var2, cut2, fname, nbins, lowbin, highbin )
