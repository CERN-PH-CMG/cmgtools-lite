import math
import pickle

import ROOT

from CMGTools.H2TauTau.proto.plotter.ROCPlotter import makeLegend
from CMGTools.H2TauTau.proto.plotter.officialStyle import setTDRStyle
setTDRStyle()

#'80', '90', 
masses_bbh = ['100', '110', '120', '130', '140', '160', '180', '250',  '350', '400', '450',  '500', '600', '700', '800', '900', '1000',  '1400', '1500', '1600', '1800', '2000', '2900', '3200']
# '80', '90',
# '100', '110', '120', '130', '160', '180', 
masses_ggh = ['200', '350', '450', '500', '600', '700', '800',  '1000', '1200', '1400', '1500',  '1800', '2000', '2300', '2600', '2900', '3200']

var_name = 'mt_total_mssm'

bbh_name = 'HiggsSUSYBB'
ggh_name = 'HiggsSUSYGG'

isos = ['vvtight', 'vtight', 'tight', 'medium', 'loose']
isos_titles = ['VVTight', 'VTight', 'Tight', 'Medium', 'Loose']

groups = {
    'inclusive':['inclusive'],
    'btag':['btag'],
    'nobtag':['nobtag'],
    # 'taupt60split':['inclusive_tau1pt60', 'inclusive_tau1ptl60'],
    # 'taupt75split':['inclusive_tau1pt75', 'inclusive_tau1ptl75'],
    # 'taupt100split':['inclusive_tau1pt100', 'inclusive_tau1ptl100'],
    # 'taupt60':['inclusive_tau1pt60'],
    # 'taupt75':['inclusive_tau1pt75'],
    # 'taupt100':['inclusive_tau1pt100']
}

ams_dict = pickle.load(open('opt.pkl'))

process = 'ggH'
masses = masses_ggh

process = 'bbH'
masses = masses_bbh

graphs = {}

for group, cats in groups.items():
    for iso in isos:
        ams_vals = {}
        g = ROOT.TGraph(len(masses))
        for i_mass, mass in enumerate(masses):

            ams = math.sqrt(sum(ams_dict['__'.join([var_name, cat+iso, process+mass])+'_']**2 for cat in cats))

            ams_vals[int(mass)] = ams
            g.SetPoint(i_mass, float(mass), ams)
        
        graphs[group+iso] = g

colours = [1, 2, 3, 4, 6, 7, 8, 9, 47, 46, 44, 43, 42, 41, 40]
# markers = [20, 21, 22, 23, 24, 25, 26, 27]

cats_pt = ['inclusive']#, 'taupt60split', 'taupt75split', 'taupt100split']
cats_pt_titles = ['Inclusive']#, 'p_{T} > 60 GeV', 'p_{T} > 75 GeV', 'p_{T} > 100 GeV', ]
cats_jets = ['inclusive', 'nobtag', 'btag']
cats_jets_titles = ['Inclusive', 'No b-tag', 'b-tag']#, 'p_{T} > 60 GeV', 'p_{T} > 75 GeV', 'p_{T} > 100 GeV', ]

plots = {
    # 'cats_pt_loose':([c+'loose' for c in cats_pt], [t for t in cats_pt_titles]),
    # 'cats_pt_medium':([c+'medium' for c in cats_pt], [t for t in cats_pt_titles]),
    # 'cats_pt_tight':([c+'tight' for c in cats_pt], [t for t in cats_pt_titles]),
    # 'cats_pt_vtight':([c+'vtight' for c in cats_pt], [t for t in cats_pt_titles]),
    # 'cats_pt_vvtight':([c+'vvtight' for c in cats_pt], [t for t in cats_pt_titles]),
    'cats_jets_loose':([c+'loose' for c in cats_jets], [t for t in cats_jets_titles]),
    'cats_jets_medium':([c+'medium' for c in cats_jets], [t for t in cats_jets_titles]),
    'cats_jets_tight':([c+'tight' for c in cats_jets], [t for t in cats_jets_titles]),
    'cats_jets_vtight':([c+'vtight' for c in cats_jets], [t for t in cats_jets_titles]),
    'cats_jets_vvtight':([c+'vvtight' for c in cats_jets], [t for t in cats_jets_titles]),
    'cats_iso_inclusive':(['inclusive'+c for c in isos], [iso for iso in isos_titles]),
    'cats_iso_btag':(['btag'+c for c in isos], [iso for iso in isos_titles]),
    'cats_iso_nobtag':(['nobtag'+c for c in isos], [iso for iso in isos_titles]),
    # 'cats_iso_taupt60split':(['taupt60split'+c for c in isos], [iso for iso in isos_titles]),
    # 'cats_iso_taupt75split':(['taupt75split'+c for c in isos], [iso for iso in isos_titles]),
    # 'cats_iso_taupt100split':(['taupt100split'+c for c in isos], [iso for iso in isos_titles]),
}

c = ROOT.TCanvas()
for plot_name, (cats, titles) in plots.items():
    print 'Plot name:', plot_name
    g_multi = ROOT.TMultiGraph(plot_name, '')
    c_graphs = []
    for i_col, cat in enumerate(cats):
        graph = graphs[cat].Clone()
        c_graphs.append(graph)
        col = colours[i_col]
        graph.SetLineColor(col)
        graph.SetMarkerColor(col)
        graph.SetLineWidth(3)
        graph.SetMarkerStyle(0)
        g_multi.Add(graph)

    g_multi.Draw('APL')

    g_multi.GetXaxis().SetTitle('M (GeV)')
    g_multi.GetYaxis().SetTitle('AMS')
    g_multi.GetYaxis().SetDecimals(True)

    g_multi.leg = makeLegend(zip(titles, c_graphs), left=False)

    c.Print('amsplots/bbh'+plot_name+'.pdf')
