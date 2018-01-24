import ROOT, math, datetime, os
from array import array
ROOT.gROOT.SetBatch(True)

# import some parameters from wmass_parameters.py, they are also used by other scripts                                                                                      
from wmass_parameters import *

colorArray = [1, 2, 3, 4, 6, 7, 8, 9, 45, 38, 28, 29, 13, 41, 30, 40, ROOT.kOrange, ROOT.kPink, ROOT.kCyan+1, ROOT.kSpring, ROOT.kYellow-3, ROOT.kRed-3, ROOT.kBlue-3, ROOT.kOrange-3, ROOT.kMagenta-3, ROOT.kGreen-8]

date = datetime.date.today().isoformat()
date+='-manyPoints'

mcentral = mass_id_central # from wmass_parameters

def getMW(massid):
    #wmass_steps = [x for x in range(0,24,2)] + [x for x in range(24,54,10)] + [x for x in range(54,141,20)]
    wmass_steps = wmass_steps_MeV  # from wmass_parameters
    wmass_central = 80.398
    wmass_steps_full = [-1e-3*x + wmass_central for x in wmass_steps[1:]]
    wmass_steps_full += [1e-3*x + wmass_central for x in wmass_steps]
    wmass_steps_full.sort()
    return wmass_steps_full[int(round(massid,0))]

class likelihood:
    def __init__(self, infile, name, title, color, style):
        self.color = color
        self.markerstyle = style
        self.infile_name = infile
        self.infile = ROOT.TFile(self.infile_name, 'READ')
        self.tree   = self.infile.Get('limit'); 
        self.lims   = {}
        self.mwns = []
        self.mws  = []
        for evt in self.tree: 
            self.mwns.append(evt.mw)
            self.mws.append(getMW(int(evt.mw)))
        self.name  = name
        self.title = title
        self.hist = ROOT.TH1F('hist_{name}'.format(name=self.name), 'likelihood scan', len(self.mws), min(self.mws), max(self.mws))
        self.fillHisto()
        self.getGraph()
        self.getVariationGraphs()

    def fillHisto(self):
        for evt in self.tree: 
            self.hist. SetBinContent(self.hist.FindBin(getMW(int(evt.mw))), 2*evt.deltaNLL)
        self.histStyle()

    def histStyle(self):
        self.hist.SetMarkerStyle(self.markerstyle)
        self.hist.SetMarkerColor(self.color)
        self.hist.SetMarkerSize(1.1)
        self.hist.GetXaxis().SetTitle('m_{W} (GeV)')
        self.hist.GetYaxis().SetTitle('-2 #Delta ln L')
        self.hist.GetYaxis().SetRangeUser(-0.01, 4.0)

    def getGraph(self):
        self.vals = []
        for ev in self.tree:
            self.vals.append( [(getMW(ev.mw)-getMW(mcentral))*1000, (2.*ev.deltaNLL)] )
        self.vals = sorted(self.vals)
        self.graph = ROOT.TGraph(len(self.vals), array('d', [x[0] for x in self.vals]), array('d', [y[1] for y in self.vals]) )
        self.graphStyle()
        self.graph_alt = ROOT.TGraph(len(self.vals), array('d', [y[1] for y in self.vals]), array('d', [x[0] for x in self.vals]) )
        self.err = self.graph_alt.Eval(1.)
        self.line = ROOT.TLine(self.err, -0.01, self.err, 1.)
        self.line.SetLineColor(self.color)
        self.line.SetLineWidth(2)
        self.line.SetLineStyle(2)

    def getVariationGraphs(self):
        self.vargraphs = []
        self.varsmg = ROOT.TMultiGraph()
        self.varsmg.SetName(self.name); self.varsmg.SetTitle(self.name)
        self.hasVars = False
        for ev in self.tree:
            if hasattr(ev, 'v1'): self.hasVars = True
            continue
        if self.hasVars:
            for var in range(1,27):
                vals = []
                for ev in self.tree:
                    vi = 'v{var}'.format(var=var)
                    vals.append( [((ev.mw-20)*2.000), (0+getattr(ev, vi) ) ] )
                vals = sorted(vals)
                vargraph = ROOT.TGraph(len(vals), array('d', [x[0] for x in vals]), array('d', [y[1] for y in vals]) )
                vargraph.SetName('v%i'%var); vargraph.SetTitle('v%i'%var)
                vargraph.SetLineColor(colorArray[var-1] )#var if var <5 else var+1)
                vargraph.SetLineWidth(2)
                self.vargraphs.append(vargraph)
                
        if self.hasVars:
            for g in self.vargraphs:
                self.varsmg.Add(g)

    def graphStyle(self):
        self.graph.SetMarkerStyle(self.markerstyle)
        self.graph.SetMarkerColor(self.color)
        self.graph.SetLineColor  (self.color)
        self.graph.SetLineWidth  (2)
        self.graph.SetMarkerSize(1.0)
        self.graph.GetXaxis().SetTitle('m_{fit} - m_{true} (MeV)')
        self.graph.GetYaxis().SetTitle('-2 #Delta ln L')
        self.graph.GetYaxis().SetRangeUser(-0.01, 4.0)

# lh_eta_0           = likelihood('higgsCombine2017-07-13_charges_00_04.MultiDimFit.mH120.root'                       , 'eta_00_04_withPDF'    , 'W^{#pm} w/ syst'    ,  1 , 20)
# lh_eta_0_noPDF     = likelihood('higgsCombine2017-07-13_charges_00_04_noPDFUncertainty.MultiDimFit.mH120.root'      , 'eta_00_04_noPDF'      , 'W^{#pm} no PDF'    ,  1 , 24)
# lh_eta_0_noPTW     = likelihood('higgsCombine2017-07-13_charges_00_04_noPTWUncertainty.MultiDimFit.mH120.root'      , 'eta_00_04_noPtW'      , 'W^{#pm} no p_{T}^{W}'  ,  1 , 21)
# lh_eta_0_noEScale  = likelihood('higgsCombine2017-07-13_charges_00_04_noEScaleUncertainty.MultiDimFit.mH120.root'   , 'eta_00_04_noEScale'   , 'W^{#pm} no e-scale'    ,  1 , 25)

lh_eta_0           = likelihood('higgsCombine2017-08-18_comb.MultiDimFit.mH120.root'                       , 'comb_withPDF'    , 'W^{#pm} w/ syst'    ,  1 , 20)
lh_eta_0_noPDF     = likelihood('higgsCombine2017-08-18_comb_noPDFUncertainty.MultiDimFit.mH120.root'      , 'comb_noPDF'      , 'W^{#pm} no PDF'    ,  1 , 24)
lh_eta_0_noPTW     = likelihood('higgsCombine2017-08-18_comb_noPtWUncertainty.MultiDimFit.mH120.root'      , 'comb_noPtW'      , 'W^{#pm} no p_{T}^{W}'  ,  1 , 21)
lh_eta_0_noEScale  = likelihood('higgsCombine2017-08-18_comb_noEScaleUncertainty.MultiDimFit.mH120.root'   , 'comb_noEScale'   , 'W^{#pm} no e-scale'    ,  1 , 25)

lhs = [
    lh_eta_0      ,
    lh_eta_0_noPDF ,
    lh_eta_0_noPTW ,
    lh_eta_0_noEScale
]

canv = ROOT.TCanvas('canv', 'canv', 800,600)
canv.cd()
ROOT.gStyle.SetOptStat(0)

leg = ROOT.TLegend(0.40, 0.72, 0.68, 0.85)
leg.SetLineColor(ROOT.kWhite)
leg.SetFillColorAlpha(ROOT.kWhite, 0.)
leg.SetTextSize(0.03)

for i,l in enumerate(lhs):
    leg.AddEntry(l.graph, l.title, 'pl')

mg = ROOT.TMultiGraph()
for i,l in enumerate(lhs):
    #l.graph.Draw('alp %s'%('same' if i else '') )
    mg.Add(l.graph)
mg.Draw('apl')
mg.GetYaxis().SetRangeUser(-0.01, 4.0)
mg.GetXaxis().SetTitle(lhs[0].graph.GetXaxis().GetTitle())
mg.GetYaxis().SetTitle(lhs[0].graph.GetYaxis().GetTitle())
mg.GetXaxis().SetRangeUser(-20., 20.)

leg.Draw('same')
line = ROOT.TLine(-20, 1., 20, 1.)
line.SetLineStyle(2)
line.SetLineWidth(2)
line.SetLineColor(ROOT.kGray+1)
line.Draw('same')

#for i,l in enumerate(lhs):
#    l.line.Draw()

outpath = '/afs/cern.ch/user/e/emanuele/www/Analysis/WMass/13TeV/we/fitTests/{date}/'.format(date=date)
if 'mciprian' in os.environ['USER']: 
    outpath = "{cmssw_base}/src/CMGTools/WMass/python/plotter/plots/Likelihood/{date}/".format(cmssw_base=os.environ['CMSSW_BASE'],date=date)
if not os.path.exists(outpath):
    os.makedirs(outpath)
    os.system('cp /afs/cern.ch/user/g/gpetrucc/php/index.php {op}'.format(op=outpath))
    
canv.SaveAs('{op}/syst_effects_comb.pdf'.format(op=outpath))
canv.SaveAs('{op}/syst_effects_comb.png'.format(op=outpath))

for i,l in enumerate(lhs):
    if l.hasVars:
        leg2 = ROOT.TLegend(0.12, 0.12, 0.45, 0.25)
        leg2.SetNColumns(4)
        for g in l.vargraphs:
            leg2.AddEntry(g, g.GetName(), 'pl')
        c2 = ROOT.TCanvas('c2', 'c2', 800,800)
        c2.cd()
        ROOT.gStyle.SetPadRightMargin(0.05)
        ROOT.gStyle.SetPadLeftMargin(0.12)
        l.varsmg.Draw('apl')
        l.varsmg.GetYaxis().SetRangeUser(-0.2,0.2)
        leg2.Draw('same')
        #l.varsmg.GetYaxis().SetRangeUser(-0.1, 26.1)
        l.varsmg.GetXaxis().SetRangeUser(-20., 20.)
        l.varsmg.GetXaxis().SetTitle(l.graph.GetXaxis().GetTitle())
        l.varsmg.GetYaxis().SetTitle('values of #theta_{i}')
        l.varsmg.GetYaxis().SetTitleOffset(1.60)
        c2.SaveAs('{op}/variations_effects_{name}.pdf'.format(op=outpath, name=l.name))
        c2.SaveAs('{op}/variations_effects_{name}.png'.format(op=outpath, name=l.name))
        del c2



for l in lhs:
    os.system('cp {filename} {target}'.format(filename=l.infile_name, target=outpath))
