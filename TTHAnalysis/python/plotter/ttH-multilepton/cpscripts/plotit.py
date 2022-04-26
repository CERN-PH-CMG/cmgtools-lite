import ROOT as r 
from array import array
from copy import deepcopy
_noDelete=[]
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


r.gROOT.SetBatch(True)
r.gStyle.SetOptStat(0)
r.gStyle.SetOptTitle(0)

inputs = [ 
    ("Multilepton",'scans/scan_multilepton.root',r.kRed),
    ("H#rightarrow#gamma#gamma",'scans/scan_gambagamba.root', r.kBlue),
    ("Multilepton + H#rightarrow#gamma#gamma",'scans/scan_multilepton_gambagamba.root',r.kMagenta),
    ("Full combination",'scans/scan_fullcombination.root',r.kBlack),
]



plotformat = (600,600)
height =  plotformat[1]
topSpamSize=1.1
c1 = r.TCanvas("canvas", "", plotformat[0], height)
c1.SetTopMargin(c1.GetTopMargin()*topSpamSize);
c1.SetWindowSize(plotformat[0] + (plotformat[0] - c1.GetWw()), plotformat[1] + (plotformat[1] - c1.GetWh()));




frame = r.TH2F("frame", "", 1, -1.2,1.7,1,-1.5,1.5)
frame.GetXaxis().SetTitle("#kappa_{t}")
frame.GetYaxis().SetTitle("#tilde{#kappa_{t}}")
frame.Draw()

c=r.TCanvas("dummy","")
tokeep=[]

leg1=r.TLegend(0.2, 0.2, 0.5, 0.4)
leg1.SetTextSize(0.035)
leg1.SetLineColor(0)

storeGraph=True
for proc, fil, color in inputs:
    c.cd()
    tf=r.TFile.Open(fil)
    limit=tf.Get('limit')
    if 'Meng' in proc: 
        limit.Draw("2*deltaNLL:kappa_t:kappa")
    else:
        limit.Draw("2*deltaNLL:kappa_ttilde:kappa_t")

    graph = r.TGraph2D(limit.GetEntries(), limit.GetV3(), limit.GetV2(), limit.GetV1())
    graph.SetNpy(500); graph.SetNpx(500)
    if storeGraph: 
        outf=r.TFile.Open(fil.replace('.root','_graph.root'),"recreate")
        outf.WriteTObject(graph, 'graph')
        outf.Close()
    hist = deepcopy(graph.GetHistogram())
    hist.SetName(proc)
    hist.SetDirectory(0)
    hist.SetLineColor(color)
    hist.SetLineWidth(2)
    cont=array('d',[2.3])
    hist.SetContour(1, cont)
    c1.cd()
    hist.Draw('cont3,same')
    leg1.AddEntry(hist, proc, 'l')
    tokeep.append(hist)
    tokeep.append(graph)
print tokeep
doSpam('#bf{CMS} #it{Preliminary}', .09, .92, .6, .92, align=12, textSize=0.05)
doSpam('137 fb^{-1} (13 TeV)', .56, .92, .75, .92, align=12, textSize=0.05)
leg1.Draw("same")

c1.SaveAs('plot.pdf')

