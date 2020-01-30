import os
from ROOT import TCanvas, TROOT, TH1F, TH2F, TFile, TTree, gROOT, kRed, TLegend

gROOT.SetBatch(True)

from optparse import OptionParser
parser = OptionParser(usage="%prog [options]")
# common options, independent of the flavour chosen
parser.add_option("-i", "--inputFile", dest="inputFile",  type="string", default="./skimmedTrees_16/2lss_diff_Top-tagged/TTHnobb_fxfx_Friend.root", help="Friend tree with the needed information");
parser.add_option("-o", "--outputDir", dest="outputDir",  type="string", default="./rootplots", help="Friend tree with the needed information");
(options, args) = parser.parse_args()

if not os.path.isdir(options.outputDir):
    os.mkdir(options.outputDir)
    
f  = TFile(options.inputFile)
if not f:
    raise ValueError('File not opened')
tr = f.Get("Friends")
if not tr:
    raise ValueError('Tree not loaded')

plotlist = [
    ["Hreco_delR_H_q1l"                         ,"Hreco_delR_H_q1l>=0"                   ,"delR_q1l"      , 100, 0., 10. ],
    ["Hreco_delR_H_q2l"                         ,"Hreco_delR_H_q2l>=0"                   ,"delR_q2l"      , 100, 0., 10. ],
    ["Hreco_delR_H_partons"                     ,"Hreco_delR_H_partons>=0"               ,"delR_partons"  , 100, 0., 10. ],
    ["Hreco_delR_H_j1l"                         ,"Hreco_delR_H_j1l>=0"                   ,"delR_j1l"      , 100, 0., 10. ],
    ["Hreco_delR_H_j2l"                         ,"Hreco_delR_H_j2l>=0"                   ,"delR_j2l"      , 100, 0., 10. ],
    ["Hreco_BDThttTT_eventReco_mvaValue"        ,"Hreco_BDThttTT_eventReco_mvaValue>=0"  ,"all_score_test", 100, 0., 10. ],
    #["HTXS_Higgs_pt"                            ,"HTXS_Higgs_pt>=0"                      ,"gen_STXS_pTH"  , 100, 0., 400.],
    ["Hreco_nmatchedpartons"                    ,"Hreco_nmatchedpartons==1"              ,"hnum_top_1"    , 100, 0., 10. ],
    ["Hreco_nmatchedpartons"                    ,"Hreco_nmatchedpartons==2"              ,"hnum_top_2"    , 100, 0., 10. ],
    ["Hreco_nmatchedpartons"                    ,"Hreco_nmatchedpartons>=0"              ,"hden_no_top"   , 100, 0., 10. ],
 ]

comparisonplotlist1 = [
    ["Hreco_delR_H_j1j2", "Hreco_delR_H_j1j2>=0 && Hreco_nmatchedpartons ==1", "Hreco_delR_H_j1j2","Hreco_delR_H_j1j2>=0 && Hreco_nmatchedpartons ==2","delR_j1j2", 100, 0., 10.],
]
comparisonplotlist2 = [
    ["Hreco_delR_H_j1l" , "Hreco_delR_H_j1l>=0 && Hreco_nmatchedpartons ==1" , "Hreco_delR_H_j1l" ,"Hreco_delR_H_j1l>=0 && Hreco_nmatchedpartons ==2" ,"delR_j1l" , 100, 0., 10.],
]
comparisonplotlist3 = [
    ["Hreco_delR_H_j2l" , "Hreco_delR_H_j2l>=0 && Hreco_nmatchedpartons ==1" , "Hreco_delR_H_j2l" ,"Hreco_delR_H_j2l>=0 && Hreco_nmatchedpartons ==2" ,"delR_j2l" , 100, 0., 10.],
]
comparisonplotlist4 = [
    ["Hreco_delR_H_q1l" , "Hreco_delR_H_q1l>=0" , "Hreco_delR_H_j1l" ,"Hreco_delR_H_j1l>=0 && Hreco_nmatchedpartons==2 " ,"delR_q1j1l" , 100, 0., 10.],
]
comparisonplotlist5 = [
    ["Hreco_delR_H_q2l" , "Hreco_delR_H_q2l>=0" , "Hreco_delR_H_j2l" ,"Hreco_delR_H_j2l>=0 && Hreco_nmatchedpartons==2 " ,"delR_q2j2l" , 100, 0., 10.],
]
## another lists for scatter
scatterplotlist1 = [
    ["Hreco_delR_H_j1j2", "Hreco_delR_H_j1j2>=0 && Hreco_nmatchedpartons ==1", "Hreco_delR_H_j1j2","Hreco_delR_H_j1j2>=0 && Hreco_nmatchedpartons ==2","delR_j1j2_diff_cuts", 100, 0., 10.],
]
scatterplotlist2 = [
    ["Hreco_delR_H_j1l" , "Hreco_delR_H_j1l>=0 && Hreco_nmatchedpartons ==1" , "Hreco_delR_H_j1l" ,"Hreco_delR_H_j1l>=0 && Hreco_nmatchedpartons ==2" ,"delR_j1l_diff_cuts" , 100, 0., 10.],
]
scatterplotlist3 = [
    ["Hreco_delR_H_j2l" , "Hreco_delR_H_j2l>=0 && Hreco_nmatchedpartons ==1" , "Hreco_delR_H_j2l" ,"Hreco_delR_H_j2l>=0 && Hreco_nmatchedpartons ==2" ,"delR_j2l_diff_cuts" , 100, 0., 10.],
]
scatterplotlist4 = [
    ["Hreco_delR_H_q1l" , "Hreco_delR_H_q1l>=0" , "Hreco_delR_H_j1l" ,"Hreco_delR_H_j1l>=0 && Hreco_nmatchedpartons==2 " ,"delR_q1j1l" , 100, 0., 10.],
]
scatterplotlist5 = [
    ["Hreco_delR_H_q2l" , "Hreco_delR_H_q2l>=0" , "Hreco_delR_H_j2l" ,"Hreco_delR_H_j2l>=0 && Hreco_nmatchedpartons==2 " ,"delR_q2j2l" , 100, 0., 10.],
]

def draw_plot(var,cut,fname,nbins,lowbin, highbin):
    c = TCanvas()
    c.cd()
    theplot = TH1F(var,var, nbins, lowbin, highbin)
    tr.Draw("%s>>%s"%(var,var),cut)
    theplot.Draw()
    c.Print("%s/%s.png"%(options.outputDir,fname)) 

def draw_comparison(var1, cut1, var2, cut2, fname, nbins, lowbin, highbin): #TODO the hist title is always the first var--> confusing when comparing two different vars
    c   = TCanvas()
    leg = TLegend(0.5,0.6,0.9,0.9)
    c.cd()
    theplot_1 = TH1F(var1,var1, nbins, lowbin, highbin)
    tr.Draw("%s>>%s"%(var1,var1),cut1)
    theplot_2 = TH1F("%s_2"%var2,var2, nbins, lowbin, highbin) # Avoid issues with same names
    tr.Draw("%s>>%s_2"%(var2,var2),cut2)
    theplot_1.Scale(1/theplot_1.Integral())
    theplot_2.Scale(1/theplot_2.Integral())
    theplot_1.SetLineColor(kRed)
    theplot_1.Draw("HIST")
    theplot_2.Draw("HIST SAME")
    leg.AddEntry(theplot_1,"%s"%(cut1))
    leg.AddEntry(theplot_2,"%s"%(cut2))
    leg.Draw()
    c.Print("%s/%s_comp.png"%(options.outputDir,fname)) # Avoid overwriting single var plots

def draw_scatter(var1, cut1, var2, cut2, fname, nbins, lowbin, highbin):
    c   = TCanvas()
    c.cd()
    theplot_scat = TH2F(var2,var2, nbins, lowbin, highbin, nbins, lowbin, highbin)
    theplot_scat.GetXaxis().SetTitle("%s"%var1)
    theplot_scat.GetYaxis().SetTitle("%s"%var2)
    tr.Draw("%s:%s>>%s"%(var1,var2,var2),cut1)
    theplot_scat.Draw("COL")
    theplot_scat.SetTitle("%s_Vs_%s"%(var1,var2))
    c.Print("%s/%s_2D.png"%(options.outputDir,fname))


for var, cut, fname, nbins, lowbin, highbin in plotlist:
    draw_plot(var, cut, fname, nbins, lowbin, highbin )

    for var1, cut1, var2, cut2, fname, nbins, lowbin, highbin  in comparisonplotlist1:
        draw_comparison(var1, cut1, var2, cut2, fname, nbins, lowbin, highbin )

    for var1, cut1, var2, cut2, fname, nbins, lowbin, highbin  in comparisonplotlist2:
        draw_comparison(var1, cut1, var2, cut2, fname, nbins, lowbin, highbin )
    
    for var1, cut1, var2, cut2, fname, nbins, lowbin, highbin  in comparisonplotlist3:
        draw_comparison(var1, cut1, var2, cut2, fname, nbins, lowbin, highbin )
    
    for var1, cut1, var2, cut2, fname, nbins, lowbin, highbin  in comparisonplotlist4:
        draw_comparison(var1, cut1, var2, cut2, fname, nbins, lowbin, highbin )
    
    for var1, cut1, var2, cut2, fname, nbins, lowbin, highbin  in comparisonplotlist5:
        draw_comparison(var1, cut1, var2, cut2, fname, nbins, lowbin, highbin )

        for var1, cut1, var2, cut2, fname, nbins, lowbin, highbin  in scatterplotlist1:
            draw_scatter(var1, cut1, var2, cut2, fname, nbins, lowbin, highbin)

        for var1, cut1, var2, cut2, fname, nbins, lowbin, highbin  in scatterplotlist2:
            draw_scatter(var1, cut1, var2, cut2, fname, nbins, lowbin, highbin)
        
        for var1, cut1, var2, cut2, fname, nbins, lowbin, highbin  in scatterplotlist3:
            draw_scatter(var1, cut1, var2, cut2, fname, nbins, lowbin, highbin)
        
        for var1, cut1, var2, cut2, fname, nbins, lowbin, highbin  in scatterplotlist4:
            draw_scatter(var1, cut1, var2, cut2, fname, nbins, lowbin, highbin)
        
        for var1, cut1, var2, cut2, fname, nbins, lowbin, highbin  in scatterplotlist5:
            draw_scatter(var1, cut1, var2, cut2, fname, nbins, lowbin, highbin)
