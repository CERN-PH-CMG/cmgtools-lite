import os
from ROOT import TCanvas, TROOT, TH1D, TH1F, TH2F, TFile, TTree, gROOT, kRed, kGreen, kBlack, kMagenta, kBlue, TLegend, gStyle
from copy import deepcopy

gROOT.SetBatch(True)
odir="./test_compare_stxs"

if not os.path.isdir(odir):
    os.mkdir(odir)
    print('Output directory %s did not exist. I now created it.')

f1  = TFile("./skimmedTrees_16/2lss_diff_Top-tagged/TTHnobb_fxfx_Friend.root")
if not f1:
    raise ValueError('File not opened')
tr = f1.Get("Friends")
if not tr:
    raise ValueError('Tree not loaded')
colours = {
    "Hreco_pTHvis"                          : kRed, 
    "Hreco_pTHgen"                          : kGreen, 
    "Hreco_pTVisPlusNu"                     : kBlack, 
    "Hreco_pTTrueGenPlusNu"                 : kMagenta, 
    "Hreco_pTTrueGen"                       : kBlue, 
    "Hreco_pTVis_jets_match"                : kRed-5,
    "Hreco_pTVis_jets_match_plusNu"         : kRed+5,
} # :add more if needed

comparisonplotlists = [
#first list is an attempt to plot all variables under the same condition
#TODO why these plots blow up when the cut is >= 0?
    {
        'vars' : {
            "Hreco_pTHvis"                  :  [ "Hreco_pTHvis > 0           && Hreco_nQFromWFromH==2"  ,"reco if best and cond. len(QFromWFromH)==2"                                                 ], 
            "Hreco_pTHgen"                  :  [ "Hreco_pTHgen > 0           && Hreco_nQFromWFromH==2"  ,"gen if best and cond. len(QFromWFromH)==2"                                                  ],
            "Hreco_pTVisPlusNu"             :  [ "Hreco_pTVisPlusNu > 0      && Hreco_nQFromWFromH==2"  ,"reco+gen(nu) if best and cond. len(QFromWFromH)==2"                                         ], 
            "Hreco_pTTrueGenPlusNu"         :  [ "Hreco_pTTrueGenPlusNu > 0  && Hreco_nQFromWFromH==2"  ,"gen(q1)+gen(q2)+gen(l)+gen(nu) if best and cond. len(QFromWFromH)==2"                       ],
            "Hreco_pTTrueGen"               :  [ "Hreco_pTTrueGen > 0        && Hreco_nQFromWFromH==2"  ,"gen(q1)+gen(q2)+gen(l) if best and cond. len(QFromWFromH)==2"                               ],
            "Hreco_pTVis_jets_match"        :  [ "Hreco_pTVis_jets_match > 0                         "  ,"jm1+jm2+best_lep if best and cond. len(QFromWFromH)==2 and if -1 not in jet_match_quarks"   ],
            "Hreco_pTVis_jets_match_plusNu" :  [ "Hreco_pTVis_jets_match_plusNu > 0                   " ,"jm1+jm2+best_lep+gen(nu) if best and cond. len(QFromWFromH)==2 and if -1 not in jet_match_quarks"   ],
    },
        'pars' : {"pTH"                   :        [50, 0., 400.]}
    },
    #{
        #'vars' : {
            #"Hreco_pTHvis"                  : [ "Hreco_pTHvis > 0                                                 " ,  "reco"                           ], 
            #"Hreco_pTHgen"                  : [ "Hreco_pTHgen > 0             && Hreco_pTHvis             >= 0    " ,  "gen"                            ],
            #"Hreco_pTVisPlusNu"             : [ "Hreco_pTVisPlusNu > 0                                            " ,  "reco+gen(nu)"                   ], 
            #"Hreco_pTTrueGenPlusNu"         : [ "Hreco_pTTrueGenPlusNu > 0    && Hreco_pTHvis             >= 0    " ,  "gen(q1)+gen(q2)+gen(l)+gen(nu)" ],
            #"Hreco_pTTrueGen"               : [ "Hreco_pTTrueGen > 0          && Hreco_pTHvis             >= 0    " ,  "gen(q1)+gen(q2)+gen(l)"         ],
            #"Hreco_pTVis_jets_match"        : [ "Hreco_pTVis_jets_match > 0   && Hreco_pTVis_jets_match   >= 0    " ,  "jm1+jm2+best_lep"               ],
        #},
        #'pars' : {"pTH"                   :        [200, 0., 400.]}
    #},
    {
        'vars' : {
            "Hreco_pTHvis"          : ["Hreco_pTHvis > 0             && Hreco_pTHvis < 60"                                , "reco"                          ],
            "Hreco_pTHgen"          : ["Hreco_pTHgen > 0             && Hreco_pTHgen < 60            && Hreco_pTHvis >= 0", "gen"                           ],
            "Hreco_pTVisPlusNu"     : ["Hreco_pTVisPlusNu > 0        && Hreco_pTVisPlusNu < 60"                           , "reco+gen(nu)"                  ],
            "Hreco_pTTrueGenPlusNu" : ["Hreco_pTTrueGenPlusNu > 0    && Hreco_pTTrueGenPlusNu < 60   && Hreco_pTHvis >= 0", "gen(q1)+gen(q2)+gen(l)+gen(nu)"],
            "Hreco_pTTrueGen"       : ["Hreco_pTTrueGen > 0          && Hreco_pTTrueGen < 60         && Hreco_pTHvis >= 0", "gen(q1)+gen(q2)+gen(l)"        ],
        },
        'pars' : {"pTH_0_60" : [40, 0., 60.] } 
    },
    {
        'vars' : {
        "Hreco_pTHvis"          : ["Hreco_pTHvis >= 60           && Hreco_pTHvis < 120"                                ,  "reco"                          ],
            "Hreco_pTHgen"          : ["Hreco_pTHgen >= 60           && Hreco_pTHgen < 120            && Hreco_pTHvis >= 0",  "gen"                           ],
            "Hreco_pTVisPlusNu"     : ["Hreco_pTVisPlusNu >= 60      && Hreco_pTVisPlusNu < 120"                           ,  "reco+gen(nu)"                  ],
            "Hreco_pTTrueGenPlusNu" : ["Hreco_pTTrueGenPlusNu >= 60  && Hreco_pTTrueGenPlusNu < 120   && Hreco_pTHvis >= 0",  "gen(q1)+gen(q2)+gen(l)+gen(nu)"],
            "Hreco_pTTrueGen"       : ["Hreco_pTTrueGen >= 60        && Hreco_pTTrueGen < 120         && Hreco_pTHvis >= 0",  "gen(q1)+gen(q2)+gen(l)"        ],
        },
    'pars' : {"pTH_60_120" : [40, 60., 120. ] },
    },
    {
        'vars' : {
            "Hreco_pTHvis"          : [ "Hreco_pTHvis >= 120          && Hreco_pTHvis < 200"                                 , "reco"                          ],
            "Hreco_pTHgen"          : [ "Hreco_pTHgen >= 120          && Hreco_pTHgen < 200            && Hreco_pTHvis >= 0" , "gen"                           ],
            "Hreco_pTVisPlusNu"     : [ "Hreco_pTVisPlusNu  >= 120    && Hreco_pTVisPlusNu < 200"                            , "reco+gen(nu)"                  ],
        "Hreco_pTTrueGenPlusNu" : [ "Hreco_pTTrueGenPlusNu >= 120 && Hreco_pTTrueGenPlusNu < 200   && Hreco_pTHvis >= 0" , "gen(q1)+gen(q2)+gen(l)+gen(nu)"],
            "Hreco_pTTrueGen"       : [ "Hreco_pTTrueGen >= 120       && Hreco_pTTrueGen < 200         && Hreco_pTHvis >= 0" , "gen(q1)+gen(q2)+gen(l)"        ],
        },
        'pars' : {"pTH_120_200" : [40, 120., 200.] },
    },
    {
        'vars' : {
            "Hreco_pTHvis"          : [ "Hreco_pTHvis >= 200          && Hreco_pTHvis < 300"                                 , "reco"                          ],
            "Hreco_pTHgen"          : [ "Hreco_pTHgen >= 200          && Hreco_pTHgen < 300            && Hreco_pTHvis >= 0" , "gen"                           ],
            "Hreco_pTVisPlusNu"     : [ "Hreco_pTVisPlusNu  >= 200    && Hreco_pTVisPlusNu < 300"                            , "reco+gen(nu)"                  ],
            "Hreco_pTTrueGenPlusNu" : [ "Hreco_pTTrueGenPlusNu >= 200 && Hreco_pTTrueGenPlusNu < 300   && Hreco_pTHvis >= 0" , "gen(q1)+gen(q2)+gen(l)+gen(nu)"],
            "Hreco_pTTrueGen"       : [ "Hreco_pTTrueGen >= 200       && Hreco_pTTrueGen < 300         && Hreco_pTHvis >= 0" , "gen(q1)+gen(q2)+gen(l)"        ],
        },
        'pars' : { "pTH_200_300" : [40, 200., 300.]},
    },
    {
        'vars' : {
            "Hreco_pTHvis"          : ["Hreco_pTHvis >= 300          && Hreco_pTHvis < 450"                                 , "reco"                          ], 
            "Hreco_pTHgen"          : ["Hreco_pTHgen >= 300          && Hreco_pTHgen < 450            && Hreco_pTHvis >= 0" , "gen"                           ],
            "Hreco_pTVisPlusNu"     : ["Hreco_pTVisPlusNu  >= 300    && Hreco_pTVisPlusNu < 450"                            , "reco+gen(nu)"                  ],
            "Hreco_pTTrueGenPlusNu" : ["Hreco_pTTrueGenPlusNu >= 300 && Hreco_pTTrueGenPlusNu < 450   && Hreco_pTHvis >= 0" , "gen(q1)+gen(q2)+gen(l)+gen(nu)"],
            "Hreco_pTTrueGen"       : ["Hreco_pTTrueGen >= 300       && Hreco_pTTrueGen < 450         && Hreco_pTHvis >= 0" , "gen(q1)+gen(q2)+gen(l)"        ],
        },
        'pars' : { "pTH_300_450" : [40, 300., 450. ]},
    }
]

def draw_comparison(args):
    fname = args['pars'].keys()[0]
    nbins, lowbin, highbin = args['pars'].values()[0]

    gStyle.SetOptTitle(0)
    gStyle.SetOptStat(0) 

    c   = TCanvas('c', 'c', 800, 800)
    leg = TLegend(0.4,0.6,0.89,0.89)
    #leg = TLegend(0.6,0.7,0.89,0.89)
    c.cd()
    ps = [] # This is needed because ROOT is a mess
    h=TH1F('h', '', nbins, lowbin, highbin)
    h.Draw("ICE")
    ip=0
    ymax=0
    for var, vals in args['vars'].items():
        ps.append(TH1F(var, var, nbins, lowbin, highbin))
        tr.Draw("%s>>%s"%(var,var),vals[0])
        ps[ip].GetXaxis().SetTitle("%s [GeV]"%fname)
        ps[ip].GetYaxis().SetTitle("a.u.")
        ps[ip].SetLineColor(colours[var])
        ps[ip].Scale(1./ps[ip].Integral()) if ps[ip].Integral() != 0 else -99
        if ps[ip].GetMaximum() > ymax:
            ymax=ps[ip].GetMaximum()
        leg.AddEntry(ps[ip],vals[1])
        ip+=1
    # Find the maximum dynamically
    for p in ps:
        p.GetYaxis().SetRangeUser(0, 1.1*ymax)
        p.Draw("HIST SAME")

    leg.Draw()
    #c.SetLogy()
    c.Modified()
    c.Update()
    c.Print("%s/%s_comp.png"%(odir,fname)) # Avoid overwriting single var plots


#draw_comparison(comparisonplotlists[0])

for l in comparisonplotlists:
    draw_comparison(l)

