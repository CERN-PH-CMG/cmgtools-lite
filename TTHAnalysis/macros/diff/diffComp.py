import os
from ROOT import TCanvas, TROOT, TH1F, TH2F, TFile, TTree, gROOT, kRed, kGreen, TLegend

gROOT.SetBatch(True)
    ## open files 
f1  = TFile("./skimmedTrees_16/2lss_diff_NoTop-tagged/TTHnobb_fxfx_Friend.root")
if not f1:
    raise ValueError('File not opened')
tr1 = f1.Get("Friends")
if not tr1:
    raise ValueError('Tree not loaded')
f2  = TFile("./skimmedTrees_v5_16/2lss_diff_NoTop-tagged/TTHnobb_pow_Friend.root")
if not f2:
    raise ValueError('File not opened')
tr2 = f2.Get("Friends")
if not tr2:
    raise ValueError('Tree not loaded')
f3  = TFile("./skimmedTrees_v4_16/2016/evVarFriend_TTHnobb_2016.root")
if not f3:
    raise ValueError('File not opened')
tr3 = f3.Get("sf/t")
if not tr3:
    raise ValueError('Tree not loaded')
plotlist = [
    ["Hreco_delR_H_q1l"                         ,"Hreco_delR_H_q1l>=0"                   ,"delR_q1l"      , 100, 0., 10. ],
    ["Hreco_delR_H_q2l"                         ,"Hreco_delR_H_q2l>=0"                   ,"delR_q2l"      , 100, 0., 10. ],
    ["Hreco_delR_H_partons"                     ,"Hreco_delR_H_partons>=0"               ,"delR_partons"  , 100, 0., 10. ],
    ["Hreco_delR_H_j1l"                         ,"Hreco_delR_H_j1l>=0"                   ,"delR_j1l"      , 100, 0., 10. ],
    ["Hreco_delR_H_j2l"                         ,"Hreco_delR_H_j2l>=0"                   ,"delR_j2l"      , 100, 0., 10. ],
    ["Hreco_BDThttTT_eventReco_mvaValue"        ,"Hreco_BDThttTT_eventReco_mvaValue>=0"  ,"all_score_test", 100, 0., 10. ],
    ["Hreco_nmatchedpartons"                    ,"Hreco_nmatchedpartons==1"              ,"hnum_top_1"    , 100, 0., 10. ],
    ["Hreco_nmatchedpartons"                    ,"Hreco_nmatchedpartons==2"              ,"hnum_top_2"    , 100, 0., 10. ],
    ["Hreco_nmatchedpartons"                    ,"Hreco_nmatchedpartons>=0"              ,"hden_no_top"   , 100, 0., 10. ],
    ["Hreco_pTHgen"                             ,"Hreco_pTHgen>=0"                       ,"pTHgen"        , 100, 0., 400.],
    ["Hreco_pTHvis"                             ,"Hreco_pTHvis>=0"                       ,"pTHvis"        , 100, 0., 400.],
 ]
 
    ## compare the same var from different ntuples versions
comparisonplotlist1 = [
    ["Hreco_pTHgen"     , "Hreco_pTHgen>=0"     ,"pTHgen"   ,100, 0., 400.],
]
comparisonplotlist2 = [
    ["Hreco_pTHvis"     , "Hreco_pTHvis>=0"     ,"pTHvis"   ,100, 0., 400.],
]
comparisonplotlist3 = [
    ["Hreco_delR_H_j1l" , "Hreco_delR_H_j1l>=0" ,"delR_j1l" , 100, 0., 10.],
]
comparisonplotlist4 = [
    ["Hreco_delR_H_j2l" , "Hreco_delR_H_j2l>=0" ,"delR_j2l" , 100, 0., 10.],
]
comparisonplotlist5 = [
    ["Hreco_delR_H_q1l" , "Hreco_delR_H_q1l>=0" ,"delR_q1l" , 100, 0., 10.],
]

comparisonplotlist6 = [
    ["Hreco_delR_H_q2l" , "Hreco_delR_H_q2l>=0" ,"delR_q2l" , 100, 0., 10.],
]

def draw_plot(var,cut,fname,nbins,lowbin, highbin):
    c = TCanvas()
    c.cd()
    theplot = TH1F(var,var, nbins, lowbin, highbin)
    tr1.Draw("%s>>%s"%(var,var),cut)
    theplot.Draw()
    c.Print("%s/%s.png"%("./test_compare/",fname)) 

def draw_comparison(var,cut, fname, nbins, lowbin, highbin):
    c   = TCanvas()
    leg = TLegend(0.5,0.6,0.9,0.9)
    c.cd()
    theplot_1 = TH1F(var,var, nbins, lowbin, highbin)
    tr1.Draw("%s>>%s"%(var,var),cut)
    theplot_2 = TH1F("%s_2"%var,var, nbins, lowbin, highbin) # Avoid issues with same names
    tr2.Draw("%s>>%s_2"%(var,var),cut)
    theplot_3 = TH1F("%s_3"%var,var, nbins, lowbin, highbin) # Avoid issues with same names
    tr3.Draw("%s>>%s_3"%(var,var),cut)
    theplot_1.Scale(1/theplot_1.Integral())
    theplot_2.Scale(1/theplot_2.Integral())
    theplot_3.Scale(1/theplot_3.Integral())
    theplot_2.SetLineColor(kRed)
    theplot_3.SetLineColor(kGreen)
    theplot_1.Draw("HIST")
    theplot_2.Draw("HIST SAME")
    theplot_3.Draw("HIST SAME")
    leg.AddEntry(theplot_1,"v6")
    leg.AddEntry(theplot_2,"v5")
    leg.AddEntry(theplot_3,"v4")
    leg.Draw()
    c.Print("%s/%s_comp.png"%("./test_compare/",fname)) # Avoid overwriting single var plots

#for var, cut, fname, nbins, lowbin, highbin in plotlist:
    #draw_plot(var, cut, fname, nbins, lowbin, highbin )
for var, cut, fname, nbins, lowbin, highbin  in comparisonplotlist1:
    draw_comparison(var, cut, fname, nbins, lowbin, highbin )

for var, cut, fname, nbins, lowbin, highbin  in comparisonplotlist2:
    draw_comparison(var, cut, fname, nbins, lowbin, highbin )

#for var, cut, fname, nbins, lowbin, highbin  in comparisonplotlist3:
    #draw_comparison(var, cut, fname, nbins, lowbin, highbin )

#for var, cut, fname, nbins, lowbin, highbin  in comparisonplotlist4:
    #draw_comparison(var, cut, fname, nbins, lowbin, highbin )

#for var, cut, fname, nbins, lowbin, highbin  in comparisonplotlist5:
    #draw_comparison(var, cut, fname, nbins, lowbin, highbin )

#for var, cut, fname, nbins, lowbin, highbin  in comparisonplotlist6:
    #draw_comparison(var, cut, fname, nbins, lowbin, highbin )
