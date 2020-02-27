import os
from ROOT import TCanvas, TROOT, TH1D, TH1F, TH2F, TFile, TTree, gROOT, kRed, kGreen, kBlack, kMagenta, TLegend, gStyle

gROOT.SetBatch(True)
    ## open files 
#f1  = TFile("./skimmedTrees_16_mm/testing/TTHnobb_fxfx_Friend.root")
f1  = TFile("/nfs/user/elfaham/104X/v6/2016/2lss_diff_Top-tagged/TTHnobb_fxfx_Friend.root")
if not f1:
    raise ValueError('File not opened')
tr = f1.Get("Friends")
if not tr:
    raise ValueError('Tree not loaded')
comparisonplotlist1 = [
    [   "Hreco_pTHvis"          , "Hreco_pTHvis > 0 "           , 
        "Hreco_pTHgen"          , "Hreco_pTHgen > 0"            , 
        "Hreco_pTVisPlusNu"     , "Hreco_pTVisPlusNu > 0"       , 
        "Hreco_pTTrueGenplusNu" , "Hreco_pTTrueGenplusNu > 0"   ,
        "Hreco_pTTrueGen"       , "Hreco_pTTrueGen > 0"         , 
        "pTH"                   ,
         200, 0., 600.   ],
]
comparisonplotlist2 = [
    [   "Hreco_pTHvis"          , "Hreco_pTHvis > 0             && Hreco_pTHvis < 60"               ,
        "Hreco_pTHgen"          , "Hreco_pTHgen > 0             && Hreco_pTHgen < 60"               ,
        "Hreco_pTVisPlusNu"     , "Hreco_pTVisPlusNu > 0        && Hreco_pTVisPlusNu < 60"          ,
        "Hreco_pTTrueGenplusNu" , "Hreco_pTTrueGenplusNu > 0    && Hreco_pTTrueGenplusNu < 60"      ,
        "Hreco_pTTrueGen"       , "Hreco_pTTrueGen > 0          && Hreco_pTTrueGen < 60"            ,
        "pTH_0_60"              ,
         40, 0., 60. ], 
]

comparisonplotlist3 = [
    [   "Hreco_pTHvis"          , "Hreco_pTHvis >= 60           && Hreco_pTHvis < 120"              ,
        "Hreco_pTHgen"          , "Hreco_pTHgen >= 60           && Hreco_pTHgen < 120"              ,
        "Hreco_pTVisPlusNu"     , "Hreco_pTVisPlusNu >= 60      && Hreco_pTVisPlusNu < 120"         ,
        "Hreco_pTTrueGenplusNu" , "Hreco_pTTrueGenplusNu >= 60  && Hreco_pTTrueGenplusNu < 120"     ,
        "Hreco_pTTrueGen"       , "Hreco_pTTrueGen >= 60        && Hreco_pTTrueGen < 120"           ,
        "pTH_60_120"            ,
         40, 60., 120. ],
]

comparisonplotlist4 = [
    [   "Hreco_pTHvis"          , "Hreco_pTHvis >= 120          && Hreco_pTHvis < 200"              ,
        "Hreco_pTHgen"          , "Hreco_pTHgen >= 120          && Hreco_pTHgen < 200"              ,
        "Hreco_pTVisPlusNu"     , "Hreco_pTVisPlusNu  >= 120    && Hreco_pTVisPlusNu < 200"         ,
        "Hreco_pTTrueGenplusNu" , "Hreco_pTTrueGenplusNu >= 120 && Hreco_pTTrueGenplusNu < 200"     ,
        "Hreco_pTTrueGen"       , "Hreco_pTTrueGen >= 120       && Hreco_pTTrueGen < 200"           ,
        "pTH_120_200"           ,
         40, 120., 200. ],
]

comparisonplotlist5 = [
    [   "Hreco_pTHvis"          , "Hreco_pTHvis >= 200          && Hreco_pTHvis < 300"              ,
        "Hreco_pTHgen"          , "Hreco_pTHgen >= 200          && Hreco_pTHgen < 300"              ,
        "Hreco_pTVisPlusNu"     , "Hreco_pTVisPlusNu  >= 200    && Hreco_pTVisPlusNu < 300"         ,
        "Hreco_pTTrueGenplusNu" , "Hreco_pTTrueGenplusNu >= 200  && Hreco_pTTrueGenplusNu < 300"    ,
        "Hreco_pTTrueGen"       , "Hreco_pTTrueGen >= 200        && Hreco_pTTrueGen < 300"          ,   
        "pTH_200_300"           ,
         40, 200., 300. ],
]

comparisonplotlist6 = [
    [   "Hreco_pTHvis"          , "Hreco_pTHvis >= 300          && Hreco_pTHvis < 450"              , 
        "Hreco_pTHgen"          , "Hreco_pTHgen >= 300          && Hreco_pTHgen < 450"              , 
        "Hreco_pTVisPlusNu"     , "Hreco_pTVisPlusNu  >= 300    && Hreco_pTVisPlusNu < 450"         , 
        "Hreco_pTTrueGenplusNu" , "Hreco_pTTrueGenplusNu >= 300 && Hreco_pTTrueGenplusNu < 450"     , 
        "Hreco_pTTrueGen"       , "Hreco_pTTrueGen >= 300       && Hreco_pTTrueGen < 450"           , 
        "pTH_300_450"           ,
         40, 300., 450. ],
]
def draw_comparison(var1, cut1, var2, cut2, var3, cut3, var4, cut4, var5, cut5, fname, nbins, lowbin, highbin):
    gStyle.SetOptTitle(0)
    gStyle.SetOptStat(0) 
    c   = TCanvas()
    leg = TLegend(0.6,0.7,0.89,0.89)
    c.cd()
    theplot_1 = TH1F(var1,var1, nbins, lowbin, highbin)
    tr.Draw("%s>>%s"%(var1,var1),cut1)
    theplot_2 = TH1F("%s_2"%var2,var2, nbins, lowbin, highbin) # Avoid issues with same names
    tr.Draw("%s>>%s_2"%(var2,var2),cut2)
    theplot_3 = TH1F("%s_3"%var3,var3, nbins, lowbin, highbin) # Avoid issues with same name
    tr.Draw("%s>>%s_3"%(var3,var3),cut3)
    theplot_4 = TH1F("%s_4"%var4,var4, nbins, lowbin, highbin) # Avoid issues with same name
    tr.Draw("%s>>%s_4"%(var4,var4),cut4)
    theplot_5 = TH1F("%s_5"%var5,var5, nbins, lowbin, highbin) # Avoid issues with same name
    tr.Draw("%s>>%s_5"%(var5,var5),cut5)
    theplot_2.SetLineColor(kRed)
    theplot_3.SetLineColor(kGreen)
    theplot_4.SetLineColor(kBlack)
    theplot_5.SetLineColor(kMagenta)
    theplot_1.GetXaxis().SetTitle("pTH(GeV)")
    theplot_1.GetYaxis().SetTitle("a.u.")
    theplot_1.Draw("HIST")
    theplot_1.Scale(1./theplot_1.Integral()) if theplot_1.Integral() != 0 else -99
    theplot_2.Draw("HIST SAME")
    theplot_2.Scale(1./theplot_2.Integral()) if theplot_2.Integral() != 0 else -99
    theplot_3.Draw("HIST SAME")
    theplot_3.Scale(1./theplot_3.Integral()) if theplot_3.Integral() != 0 else -99
    theplot_4.Draw("HIST SAME")
    theplot_4.Scale(1./theplot_4.Integral()) if theplot_4.Integral() != 0 else -99
    theplot_5.Draw("HIST SAME")
    theplot_5.Scale(1./theplot_5.Integral()) if theplot_5.Integral() != 0 else -99
    leg.AddEntry(theplot_1,"reco")
    leg.AddEntry(theplot_2,"gen")
    leg.AddEntry(theplot_3,"reco+gen(nu)")
    leg.AddEntry(theplot_4,"gen(q1)+gen(q2)+gen(l)+gen(nu)")
    leg.AddEntry(theplot_5,"gen(q1)+gen(q2)+gen(l)")
    leg.Draw()
    c.Print("%s/%s_comp.png"%("./test_compare_stxs/",fname)) # Avoid overwriting single var plots

for var1, cut1, var2, cut2, var3, cut3, var4, cut4, var5, cut5, fname, nbins, lowbin, highbin in comparisonplotlist1:
    draw_comparison(var1, cut1, var2, cut2, var3, cut3, var4, cut4, var5, cut5, fname, nbins, lowbin, highbin )

for var1, cut1, var2, cut2, var3, cut3, var4, cut4, var5, cut5, fname, nbins, lowbin, highbin  in comparisonplotlist2:
    draw_comparison(var1, cut1, var2, cut2, var3, cut3, var4, cut4, var5, cut5, fname, nbins, lowbin, highbin )

for var1, cut1, var2, cut2, var3, cut3, var4, cut4, var5, cut5, fname, nbins, lowbin, highbin  in comparisonplotlist3:
    draw_comparison(var1, cut1, var2, cut2, var3, cut3, var4, cut4, var5, cut5, fname, nbins, lowbin, highbin )

for var1, cut1, var2, cut2, var3, cut3, var4, cut4, var5, cut5, fname, nbins, lowbin, highbin  in comparisonplotlist4:
    draw_comparison(var1, cut1, var2, cut2, var3, cut3, var4, cut4, var5, cut5, fname, nbins, lowbin, highbin )

for var1, cut1, var2, cut2, var3, cut3, var4, cut4, var5, cut5, fname, nbins, lowbin, highbin  in comparisonplotlist5:
    draw_comparison(var1, cut1, var2, cut2, var3, cut3, var4, cut4, var5, cut5, fname, nbins, lowbin, highbin )

for var1, cut1, var2, cut2, var3, cut3, var4, cut4, var5, cut5, fname, nbins, lowbin, highbin  in comparisonplotlist6:
    draw_comparison(var1, cut1, var2, cut2, var3, cut3, var4, cut4, var5, cut5, fname, nbins, lowbin, highbin )
