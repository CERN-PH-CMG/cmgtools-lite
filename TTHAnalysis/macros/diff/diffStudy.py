import os
from ROOT import TCanvas, TROOT, TH1F, TFile, TTree, gROOT, kRed

gROOT.SetBatch(True)

from optparse import OptionParser
parser = OptionParser(usage="%prog [options]")
# common options, independent of the flavour chosen
parser.add_option("-i", "--inputFile", dest="inputFile",  type="string", default="./skimmedTrees_16/2lss_diff_Top-tagged/TTHnobb_fxfx_Friend.root", help="Friend tree with the needed information");
parser.add_option("-o", "--outputDir", dest="outputDir",  type="string", default="./rootplots/", help="Friend tree with the needed information");
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
    ["Hreco_delR_H_q1l"                         ,"Hreco_delR_H_q1l>=0"                  ,"delR_q1l"      , 100, 0., 10.],
    ["Hreco_delR_H_q2l"                         ,"Hreco_delR_H_q2l>=0"                  ,"delR_q2l"      , 100, 0., 10.],
    ["Hreco_delR_H_partons"                     ,"Hreco_delR_H_partons>=0"              ,"delR_partons"  , 100, 0., 10.],
    ["Hreco_delR_H_j1l"                         ,"Hreco_delR_H_j1l>=0"                  ,"delR_j1l"      , 100, 0., 10.],
    ["Hreco_delR_H_j2l"                         ,"Hreco_delR_H_j2l>=0"                  ,"delR_j2l"      , 100, 0., 10.],
    ["Hreco_BDThttTT_eventReco_mvaValue"        ,"Hreco_BDThttTT_eventReco_mvaValue>=0" ,"all_score_test", 100, 0., 10.],
    ["Hreco_nmatchedpartons"                     ,"Hreco_nmatchedpartons==1"              ,"hnum_top_1"    , 100, 0., 10.],
    ["Hreco_nmatchedpartons"                     ,"Hreco_nmatchedpartons==2"              ,"hnum_top_2"    , 100, 0., 10.],
    ["Hreco_nmatchedpartons"                     ,"Hreco_nmatchedpartons>=0"              ,"hden_no_top"   , 100, 0., 10.],
 ]

comparisonplotlist = [
    ["Hreco_delR_H_j1j2", "Hreco_delR_H_j1j2>=0 && Hreco_nmatchedpartons ==1", "Hreco_delR_H_j1j2","Hreco_delR_H_j1j2>=0 && Hreco_nmatchedpartons ==2","delR_j1j2", 100, 0., 10.],
]

def draw_plot(var,cut,fname,nbins,lowbin, highbin):
    c = TCanvas()
    c.cd()
    theplot = TH1F(var,var, nbins, lowbin, highbin)
    tr.Draw("%s>>%s"%(var,var),cut)
    theplot.Draw()
    c.Print("%s/%s.png"%(options.outputDir,fname))

def draw_comparison(var1, cut1, var2, cut2, fname, nbins, lowbin, highbin):
    c = TCanvas()
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
    c.Print("%s/%s.png"%(options.outputDir,fname))


for var, cut, fname, nbins, lowbin, highbin in plotlist:
    draw_plot(var, cut, fname, nbins, lowbin, highbin )

    for var1, cut1, var2, cut2, fname, nbins, lowbin, highbin  in comparisonplotlist:
        draw_comparison(var1, cut1, var2, cut2, fname, nbins, lowbin, highbin )
