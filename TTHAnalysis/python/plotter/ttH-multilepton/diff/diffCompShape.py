import os
from ROOT import TCanvas, TROOT, TH1D, TH1F, TH2F, TFile, TTree, gROOT, kRed, kGreen, kBlack, kMagenta, kBlue, kOrange, TLegend, gStyle
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
    "Hreco_pTHvis"                                          : kRed, 
    "Hreco_pTHgen"                                          : kGreen,
    "Hreco_pTHgen_no_cond"                                  : kGreen, 
    "Hreco_pTVisPlusNu"                                     : kBlack, 
    "Hreco_pTVis_jets_match"                                : kBlue,
    "Hreco_pTVis_jets_match_with_gen_lep_no_cond"           : kBlue,
    "Hreco_pTVis_jets_match_plusNu"                         : kMagenta,
    "Hreco_pTVis_jets_match_plusNu_plus_gen_lep_no_cond"    : kMagenta
} # :add more if needed

comparisonplotlists = [
#TODO why these plots blow up when the cut is >= 0?
    {
        'vars' : {
            "Hreco_pTHvis"                  :  [ "Hreco_pTHvis > 0           && Hreco_nQFromWFromH==2"  ,"reco-->best,cond_len(QWH)"                                                                    ], 
            "Hreco_pTHgen"                  :  [ "Hreco_pTHgen > 0           && Hreco_nQFromWFromH==2"  ,"gen-->best,cond_len(QWH)"                                                                     ],
            "Hreco_pTVisPlusNu"             :  [ "Hreco_pTVisPlusNu > 0      && Hreco_nQFromWFromH==2"  ,"reco+MET-->best,cond_len(QWH)"                                                                ], 
            "Hreco_pTVis_jets_match"        :  [ "Hreco_pTVis_jets_match > 0                         "  ,"jm1+jm2+best_lep-->best,cond_len(QWH),-1 not in j_m_q[]"                                      ],
            "Hreco_pTVis_jets_match_plusNu" :  [ "Hreco_pTVis_jets_match_plusNu > 0                   " ,"jm1+jm2+best_lep+MET-->best,cond_len(QWH),-1 not in j_m_q[]"                                  ],
    },
        'pars' : {"pTH"                     :        [40, 0., 400.]}
    },
    {
        'vars' : {
            "Hreco_pTHgen_no_cond"                               :  [ "Hreco_pTHgen_no_cond > 0  && Hreco_nQFromWFromH==2"          ,"gen,cond_len(QWH)"                                                 ],
            "Hreco_pTVis_jets_match_with_gen_lep_no_cond"        :  [ "Hreco_pTVis_jets_match_with_gen_lep_no_cond > 0"             ,"jm1+jm2+true_lep,cond_len(QWH),-1 not in j_m_q[]"                  ],
            "Hreco_pTVis_jets_match_plusNu_plus_gen_lep_no_cond" :  [ "Hreco_pTVis_jets_match_plusNu_plus_gen_lep_no_cond > 0"      ,"jm1+jm2+true_lep+MET,cond_len(QWH),-1 not in j_m_q[]"              ],
    },
        'pars' : {"pTH_no_cond"                                  :        [40, 0., 400.]}
    },
    {
        'vars' : {
            "Hreco_pTHvis"                  :  [ "Hreco_pTHvis > 0           && Hreco_nQFromWFromH==2"  ,"reco-->best,cond_len(QWH)"                                                                    ], 
            "Hreco_pTHgen"                  :  [ "Hreco_pTHgen > 0           && Hreco_nQFromWFromH==2"  ,"gen-->best,cond_len(QWH)"                                                                     ],
            "Hreco_pTVisPlusNu"             :  [ "Hreco_pTVisPlusNu > 0      && Hreco_nQFromWFromH==2"  ,"reco+MET-->best,cond_len(QWH)"                                                                ], 
            "Hreco_pTVis_jets_match"        :  [ "Hreco_pTVis_jets_match > 0                         "  ,"jm1+jm2+best_lep-->best,cond_len(QWH),-1 not in j_m_q[]"                                      ],
            "Hreco_pTVis_jets_match_plusNu" :  [ "Hreco_pTVis_jets_match_plusNu > 0                   " ,"jm1+jm2+best_lep+MET-->best,cond_len(QWH),-1 not in j_m_q[]"                                  ],
    },
        'pars' : {"pTH_4bins"               :        [4, 0., 400.]}
    },
    {
        'vars' : {
            "Hreco_pTHvis"                  :  [ "Hreco_pTHvis > 0           && Hreco_nQFromWFromH==2"  ,"reco-->best,cond_len(QWH)"                                                                    ], 
            "Hreco_pTHgen"                  :  [ "Hreco_pTHgen > 0           && Hreco_nQFromWFromH==2"  ,"gen-->best,cond_len(QWH)"                                                                     ],
            "Hreco_pTVisPlusNu"             :  [ "Hreco_pTVisPlusNu > 0      && Hreco_nQFromWFromH==2"  ,"reco+MET-->best,cond_len(QWH)"                                                                ], 
            "Hreco_pTVis_jets_match"        :  [ "Hreco_pTVis_jets_match > 0                         "  ,"jm1+jm2+best_lep-->best,cond_len(QWH),-1 not in j_m_q[]"                                      ],
            "Hreco_pTVis_jets_match_plusNu" :  [ "Hreco_pTVis_jets_match_plusNu > 0                   " ,"jm1+jm2+best_lep+MET-->best,cond_len(QWH),-1 not in j_m_q[]"                                  ],
    },
        'pars' : {"pTH_0_60"                :        [40, 0., 60.]}
    },
    {
        'vars' : {
            "Hreco_pTHvis"                  :  [ "Hreco_pTHvis > 0           && Hreco_nQFromWFromH==2"  ,"reco-->best,cond_len(QWH)"                                                                    ], 
            "Hreco_pTHgen"                  :  [ "Hreco_pTHgen > 0           && Hreco_nQFromWFromH==2"  ,"gen-->best,cond_len(QWH)"                                                                     ],
            "Hreco_pTVisPlusNu"             :  [ "Hreco_pTVisPlusNu > 0      && Hreco_nQFromWFromH==2"  ,"reco+MET-->best,cond_len(QWH)"                                                                ], 
            "Hreco_pTVis_jets_match"        :  [ "Hreco_pTVis_jets_match > 0                         "  ,"jm1+jm2+best_lep-->best,cond_len(QWH),-1 not in j_m_q[]"                                      ],
            "Hreco_pTVis_jets_match_plusNu" :  [ "Hreco_pTVis_jets_match_plusNu > 0                   " ,"jm1+jm2+best_lep+MET-->best,cond_len(QWH),-1 not in j_m_q[]"                                  ],
    },
        'pars' : {"pTH_0_120"               :        [40, 60., 120.]}
    },

    {
        'vars' : {
            "Hreco_pTHvis"                  :  [ "Hreco_pTHvis > 0           && Hreco_nQFromWFromH==2"  ,"reco-->best,cond_len(QWH)"                                                                    ], 
            "Hreco_pTHgen"                  :  [ "Hreco_pTHgen > 0           && Hreco_nQFromWFromH==2"  ,"gen-->best,cond_len(QWH)"                                                                     ],
            "Hreco_pTVisPlusNu"             :  [ "Hreco_pTVisPlusNu > 0      && Hreco_nQFromWFromH==2"  ,"reco+MET-->best,cond_len(QWH)"                                                                ], 
            "Hreco_pTVis_jets_match"        :  [ "Hreco_pTVis_jets_match > 0                         "  ,"jm1+jm2+best_lep-->best,cond_len(QWH),-1 not in j_m_q[]"                                      ],
            "Hreco_pTVis_jets_match_plusNu" :  [ "Hreco_pTVis_jets_match_plusNu > 0                   " ,"jm1+jm2+best_lep+MET-->best,cond_len(QWH),-1 not in j_m_q[]"                                  ],
    },
        'pars' : {"pTH_120_200"             :        [40, 120., 200.]}
    },

    {
        'vars' : {
            "Hreco_pTHvis"                  :  [ "Hreco_pTHvis > 0           && Hreco_nQFromWFromH==2"  ,"reco-->best,cond_len(QWH)"                                                                    ], 
            "Hreco_pTHgen"                  :  [ "Hreco_pTHgen > 0           && Hreco_nQFromWFromH==2"  ,"gen-->best,cond_len(QWH)"                                                                     ],
            "Hreco_pTVisPlusNu"             :  [ "Hreco_pTVisPlusNu > 0      && Hreco_nQFromWFromH==2"  ,"reco+MET-->best,cond_len(QWH)"                                                                ], 
            "Hreco_pTVis_jets_match"        :  [ "Hreco_pTVis_jets_match > 0                         "  ,"jm1+jm2+best_lep-->best,cond_len(QWH),-1 not in j_m_q[]"                                      ],
            "Hreco_pTVis_jets_match_plusNu" :  [ "Hreco_pTVis_jets_match_plusNu > 0                   " ,"jm1+jm2+best_lep+MET-->best,cond_len(QWH),-1 not in j_m_q[]"                                  ],
    },
        'pars' : {"pTH_200_300"             :        [40, 200., 300.]}
    },
    {
        'vars' : {
            "Hreco_pTHvis"                  :  [ "Hreco_pTHvis > 0           && Hreco_nQFromWFromH==2"  ,"reco-->best,cond_len(QWH)"                                                                    ], 
            "Hreco_pTHgen"                  :  [ "Hreco_pTHgen > 0           && Hreco_nQFromWFromH==2"  ,"gen-->best,cond_len(QWH)"                                                                     ],
            "Hreco_pTVisPlusNu"             :  [ "Hreco_pTVisPlusNu > 0      && Hreco_nQFromWFromH==2"  ,"reco+MET-->best,cond_len(QWH)"                                                                ], 
            "Hreco_pTVis_jets_match"        :  [ "Hreco_pTVis_jets_match > 0                         "  ,"jm1+jm2+best_lep-->best,cond_len(QWH),-1 not in j_m_q[]"                                      ],
            "Hreco_pTVis_jets_match_plusNu" :  [ "Hreco_pTVis_jets_match_plusNu > 0                   " ,"jm1+jm2+best_lep+MET-->best,cond_len(QWH),-1 not in j_m_q[]"                                  ],
    },
        'pars' : {"pTH_200_300"             :        [40, 300., 450.]}
    },
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

