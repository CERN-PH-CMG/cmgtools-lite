import os
from ROOT import TCanvas, TROOT, TH1F, TH2F, TFile, TTree, gROOT, kBlack, kRed, TLegend

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
#TODO overwrites variables
'''
plotdict = {
    "Hreco_delR_H_partons_no_cond"                  : [ "","Hreco_delR_H_partons_no_cond>=0"                                ,"delR_partons_no_cond"                                       , 100, 0., 10.  ],
    "Hreco_delR_H_j1j2"                             : [ "","Hreco_delR_H_j1j2>=0"                                           ,"delR_H_j1j2"                                                , 100, 0., 10.  ],
    "Hreco_delR_H_partons_no_cond"                  : [ "cut","Hreco_delR_H_partons_no_cond>=0 && Hreco_nmatchedpartons ==1","delR_partons_no_cond"                                       , 100, 0., 10.  ],
    "Hreco_delR_H_j1j2"                             : [ "","Hreco_delR_H_j1j2>=0      && Hreco_nmatchedpartons ==1"         ,"delR_H_j1j2_cut"                                            , 100, 0., 10.  ],
    "Hreco_nmatchedpartons"                         : [ "","Hreco_nmatchedpartons==1"                                       ,"hnum_top_1"                                                 , 100, 0., 10.  ],
    "Hreco_pTHvis"                                  : [ "","Hreco_pTHvis>=0"                                                ,"pTHvis"                                                     , 100, 0., 400. ],
    "Hreco_pTHgen"                                  : [ "","Hreco_pTHgen>=0"                                                ,"pTHgen"                                                     , 100, 0., 400. ],
    "Hreco_quark1pT_no_cond"                        : [ "","Hreco_quark1pT_no_cond>=0"                                      ,"Hreco_quark1pT_no_cond"                                     , 100, 0., 400. ],
    "Hreco_quark2pT_no_cond"                        : [ "","Hreco_quark2pT_no_cond>=0"                                      ,"Hreco_quark2pT_no_cond"                                     , 100, 0., 400. ],
    "Hreco_closestJet_pt_ToQ1FromWFromH_no_cond"    : [ "","Hreco_closestJet_pt_ToQ1FromWFromH_no_cond>=0"                  ,"Hreco_closestJet_pt_ToQ1FromWFromH_no_cond"                 , 100, 0., 400. ],
    "Hreco_closestJet_pt_ToQ2FromWFromH_no_cond"    : [ "","Hreco_closestJet_pt_ToQ2FromWFromH_no_cond>=0"                  ,"Hreco_closestJet_pt_ToQ2FromWFromH_no_cond"                 , 100, 0., 400. ],
    "Hreco_closestJet_ptres_ToQ1FromWFromH_no_cond" : [ "",""                                                               ,"Hreco_closestJet_ptres_ToQ1FromWFromH_no_cond"              , 100, -10, 10. ],
    "Hreco_closestJet_ptres_ToQ2FromWFromH_no_cond" : [ "",""                                                               ,"Hreco_closestJet_ptres_ToQ2FromWFromH_no_cond"              , 100, -10, 10. ],
    "Hreco_closestJet_delR_ToQ1FromWFromH_no_cond"  : [ "","Hreco_closestJet_delR_ToQ1FromWFromH_no_cond>=0"                ,"Hreco_closestJet_delR_ToQ1FromWFromH_no_cond"               , 100, -1., 10. ],
    "Hreco_closestJet_delR_ToQ2FromWFromH_no_cond"  : [ "","Hreco_closestJet_delR_ToQ2FromWFromH_no_cond>=0"                ,"Hreco_closestJet_delR_ToQ2FromWFromH_no_cond"               , 100, -1., 10. ],
    "Hreco_closestJet_delR_ToQ1FromWFromH_no_cond"  : [ "","Hreco_closestJet_delR_ToQ1FromWFromH_no_cond>=0.05"             ,"Hreco_closestJet_delR_ToQ1FromWFromH_no_cond_cut_0.05"      , 100, -1., 10. ],
    "Hreco_closestJet_delR_ToQ2FromWFromH_no_cond"  : [ "","Hreco_closestJet_delR_ToQ2FromWFromH_no_cond>=0.05"             ,"Hreco_closestJet_delR_ToQ2FromWFromH_no_cond_cut_0.05"      , 100, -1., 10. ],
    "Hreco_closestJet_delR_ToQ1FromWFromH_no_cond"  : [ "",""                                                               ,"Hreco_closestJet_delR_ToQ1FromWFromH_no_cond_no_cut_at_zero", 100, -1., 10. ],
    "Hreco_closestJet_delR_ToQ2FromWFromH_no_cond"  : [ "",""                                                               ,"Hreco_closestJet_delR_ToQ2FromWFromH_no_cond_no_cut_at_zero", 100, -1., 10. ],
    "Hreco_jet_matches_quark1_two_cond"             : [ "","Hreco_jet_matches_quark1_two_cond>=0"                           ,"Hreco_jet_matches_quark1"                                   , 100, -1., 10. ],
    "Hreco_jet_matches_quark2_two_cond"             : [ "","Hreco_jet_matches_quark2_two_cond>=0"                           ,"Hreco_jet_matches_quark2"                                   , 100, -1., 10. ],
    "Hreco_j1Idx"                                   : [ "","Hreco_j1Idx>=0"                                                 ,"Hreco_j1Idx"                                                , 100, -1., 10. ],
    "Hreco_j2Idx"                                   : [ "","Hreco_j2Idx>=0"                                                 ,"Hreco_j2Idx"                                                , 100, -1., 10. ],
    "Hreco_delR_lep_jm1"                            : [ "","Hreco_delR_lep_jm1>=0"                                          ,"Hreco_delR_lep_jm1"                                         , 100, 0., 10.  ],
    "Hreco_delR_lep_jm2"                            : [ "","Hreco_delR_lep_jm2>=0"                                          ,"Hreco_delR_lep_jm2"                                         , 100, 0., 10.  ],
    "Hreco_delR_lep_jm_closest"                     : [ "","Hreco_delR_lep_jm_closest>=0"                                   ,"Hreco_delR_lep_jm_closest"                                  , 100, 0., 10.  ],
    "Hreco_delR_lep_jm_farthest"                    : [ "","Hreco_delR_lep_jm_farthest>=0"                                  ,"Hreco_delR_lep_jm_farthest"                                 , 100, 0., 10.  ],
    "Hreco_delR_jm_closest_jm_farthest"             : [ "","Hreco_delR_jm_closest_jm_farthest>=0"                           ,"Hreco_delR_jm_closest_jm_farthest"                          , 100, 0., 10.  ],
    "Hreco_inv_mass_jm1jm2"                         : [ "","Hreco_inv_mass_jm1jm2>=0"                                       ,"Hreco_inv_mass_jm1jm2"                                      , 100, 0., 150. ],
    "Hreco_inv_mass_jm1jm2_no_cond"                 : [ "","Hreco_inv_mass_jm1jm2_no_cond>=0"                               ,"Hreco_inv_mass_jm1jm2_no_cond"                              , 100, 0., 150. ],
}
'''


plotlist = [
    ["Hreco_delR_H_partons_no_cond"                 ,""           ,"Hreco_delR_H_partons_no_cond>=0"                             ,"delR_partons_no_cond"                         , 100, 0., 10.  ],
    ["Hreco_delR_H_j1j2"                            ,""           ,"Hreco_delR_H_j1j2>=0"                                        ,"delR_H_j1j2"                                  , 100, 0., 10.  ],
    ["Hreco_delR_H_partons_no_cond"                 ,"_cut"       ,"Hreco_delR_H_partons_no_cond>=0 && Hreco_nmatchedpartons ==1","delR_partons_no_cond"                         , 100, 0., 10.  ],
    ["Hreco_delR_H_j1j2"                            ,"_cut"       ,"Hreco_delR_H_j1j2>=0 && Hreco_nmatchedpartons ==1"           ,"delR_H_j1j2"                                  , 100, 0., 10.  ],
    ["Hreco_nmatchedpartons"                        ,""           ,"Hreco_nmatchedpartons==1"                                    ,"hnum_top_1"                                   , 100, 0., 10.  ],
    ["Hreco_pTHvis"                                 ,""           ,"Hreco_pTHvis>=0"                                             ,"pTHvis"                                       , 100, 0., 400. ],
    ["Hreco_pTHgen"                                 ,""           ,"Hreco_pTHgen>=0"                                             ,"pTHgen"                                       , 100, 0., 400. ],
    ["Hreco_quark1pT_no_cond"                       ,""           ,"Hreco_quark1pT_no_cond>=0"                                   ,"Hreco_quark1pT_no_cond"                       , 100, 0., 400. ],
    ["Hreco_quark2pT_no_cond"                       ,""           ,"Hreco_quark2pT_no_cond>=0"                                   ,"Hreco_quark2pT_no_cond"                       , 100, 0., 400. ],
    ["Hreco_closestJet_pt_ToQ1FromWFromH_no_cond"   ,""           ,"Hreco_closestJet_pt_ToQ1FromWFromH_no_cond>=0"               ,"Hreco_closestJet_pt_ToQ1FromWFromH_no_cond"   , 100, 0., 400. ],
    ["Hreco_closestJet_pt_ToQ2FromWFromH_no_cond"   ,""           ,"Hreco_closestJet_pt_ToQ2FromWFromH_no_cond>=0"               ,"Hreco_closestJet_pt_ToQ2FromWFromH_no_cond"   , 100, 0., 400. ],
    ["Hreco_closestJet_ptres_ToQ1FromWFromH_no_cond",""           ,""                                                            ,"Hreco_closestJet_ptres_ToQ1FromWFromH_no_cond", 100, -10, 10. ],
    ["Hreco_closestJet_ptres_ToQ2FromWFromH_no_cond",""           ,""                                                            ,"Hreco_closestJet_ptres_ToQ2FromWFromH_no_cond", 100, -10, 10. ],
    ["Hreco_closestJet_delR_ToQ1FromWFromH_no_cond" ,""           ,"Hreco_closestJet_delR_ToQ1FromWFromH_no_cond>=0"             ,"Hreco_closestJet_delR_ToQ1FromWFromH_no_cond" , 100, -1., 10. ],
    ["Hreco_closestJet_delR_ToQ2FromWFromH_no_cond" ,""           ,"Hreco_closestJet_delR_ToQ2FromWFromH_no_cond>=0"             ,"Hreco_closestJet_delR_ToQ2FromWFromH_no_cond" , 100, -1., 10. ],
    ["Hreco_closestJet_delR_ToQ1FromWFromH_no_cond" ,"cut_0.05"   ,"Hreco_closestJet_delR_ToQ1FromWFromH_no_cond>=0.05"          ,"Hreco_closestJet_delR_ToQ1FromWFromH_no_cond" , 100, -1., 10. ],
    ["Hreco_closestJet_delR_ToQ2FromWFromH_no_cond" ,"cut_0.05"   ,"Hreco_closestJet_delR_ToQ2FromWFromH_no_cond>=0.05"          ,"Hreco_closestJet_delR_ToQ2FromWFromH_no_cond" , 100, -1., 10. ],
    ["Hreco_closestJet_delR_ToQ1FromWFromH_no_cond" ,"no_cut_zero",""                                                            ,"Hreco_closestJet_delR_ToQ1FromWFromH_no_cond" , 100, -1., 10. ],
    ["Hreco_closestJet_delR_ToQ2FromWFromH_no_cond" ,"no_cut_zero",""                                                            ,"Hreco_closestJet_delR_ToQ2FromWFromH_no_cond" , 100, -1., 10. ],
    ["Hreco_jet_matches_quark1_two_cond"            ,""           ,"Hreco_jet_matches_quark1_two_cond>=0"                        ,"Hreco_jet_matches_quark1"                     , 100, -1., 10. ],
    ["Hreco_jet_matches_quark2_two_cond"            ,""           ,"Hreco_jet_matches_quark2_two_cond>=0"                        ,"Hreco_jet_matches_quark2"                     , 100, -1., 10. ],
    ["Hreco_j1Idx"                                  ,""           ,"Hreco_j1Idx>=0"                                              ,"Hreco_j1Idx"                                  , 100, -1., 10. ],
    ["Hreco_j2Idx"                                  ,""           ,"Hreco_j2Idx>=0"                                              ,"Hreco_j2Idx"                                  , 100, -1., 10. ],
    ["Hreco_delR_lep_jm1"                           ,""           ,"Hreco_delR_lep_jm1>=0"                                       ,"Hreco_delR_lep_jm1"                           , 100, 0., 10.  ],
    ["Hreco_delR_lep_jm2"                           ,""           ,"Hreco_delR_lep_jm2>=0"                                       ,"Hreco_delR_lep_jm2"                           , 100, 0., 10.  ],
    ["Hreco_delR_lep_jm_closest"                    ,""           ,"Hreco_delR_lep_jm_closest>=0"                                ,"Hreco_delR_lep_jm_closest"                    , 100, 0., 10.  ],
    ["Hreco_delR_lep_jm_farthest"                   ,""           ,"Hreco_delR_lep_jm_farthest>=0"                               ,"Hreco_delR_lep_jm_farthest"                   , 100, 0., 10.  ],
    ["Hreco_delR_jm_closest_jm_farthest"            ,""           ,"Hreco_delR_jm_closest_jm_farthest>=0"                        ,"Hreco_delR_jm_closest_jm_farthest"            , 100, 0., 10.  ],
    ["Hreco_inv_mass_jm1jm2"                        ,""           ,"Hreco_inv_mass_jm1jm2>=0"                                    ,"Hreco_inv_mass_jm1jm2"                        , 100, 0., 150. ],
    ["Hreco_inv_mass_jm1jm2_no_cond"                ,""           ,"Hreco_inv_mass_jm1jm2_no_cond>=0"                            ,"Hreco_inv_mass_jm1jm2_no_cond"                , 100, 0., 150. ],
]

colours = {
    "Hreco_delR_H_j1j2"    : kRed,
    "Hreco_delR_H_partons" : kBlack,
} # add more if needed

comparisonplotlist = [
    {
        'vars' : {
            "Hreco_delR_H_j1j2"     :   "Hreco_delR_H_j1j2>=0"                                 ,
            "Hreco_delR_H_partons"  :   "Hreco_delR_H_partons>=0 && Hreco_nmatchedpartons ==1" ,
        },
        'pars' : { "delR_j1j2_q1q2_cut" : [100, 0., 10.],}
    },
    {
        'vars' : {
            "Hreco_delR_H_j1j2"     :   "Hreco_delR_H_j1j2>=0 && Hreco_nmatchedpartons ==1"     , 
            "Hreco_delR_H_partons"  :   "Hreco_delR_H_partons>=0 && Hreco_nmatchedpartons ==1"  ,
        },
        'pars' : { "delR_j1j2_cut_q1q2_cut" : [ 100, 0., 10.],}
    }
]

scatterplotdict = {
    ("Hreco_closestJet_delR_ToQ1FromWFromH_no_cond" , "Hreco_closestJet_ptres_ToQ1FromWFromH_no_cond") : [ "","Hreco_closestJet_delR_ToQ1FromWFromH_no_cond>=0","","delR_vs_pTres_q1", 100, -2., 10.,100,0,10],
    ("Hreco_closestJet_delR_ToQ2FromWFromH_no_cond" , "Hreco_closestJet_ptres_ToQ2FromWFromH_no_cond") : [ "","Hreco_closestJet_delR_ToQ2FromWFromH_no_cond>=0","","delR_vs_pTres_q2", 100, -2., 10.,100,0,10],
    ("Hreco_closestJet_pt_ToQ1FromWFromH_no_cond"   , "Hreco_closestJet_ptres_ToQ1FromWFromH_no_cond") : [ "","Hreco_closestJet_pt_ToQ1FromWFromH_no_cond>=0"  ,"","jetpt_vs_pTres_q1", 100, -2., 10.,100,0,100],
    ("Hreco_closestJet_pt_ToQ2FromWFromH_no_cond"   , "Hreco_closestJet_ptres_ToQ2FromWFromH_no_cond") : [ "", "Hreco_closestJet_pt_ToQ2FromWFromH_no_cond>=0"  ,"","jetpt_vs_pTres_q2", 100, -2., 10.,100,0,100],
    ("Hreco_quark1pT_no_cond"                       , "Hreco_closestJet_ptres_ToQ1FromWFromH_no_cond") : [ "", "Hreco_quark1pT_no_cond>=0"                      ,"","quark1pt_vs_pTres_q1", 100, -2., 10.,100,0,100],
    ("Hreco_quark2pT_no_cond"                       , "Hreco_closestJet_ptres_ToQ2FromWFromH_no_cond") : [ "","Hreco_quark2pT_no_cond>=0"                      ,"","quark2pt_vs_pTres_q2", 100, -2., 10.,100,0,100],
    ("Hreco_jet_matches_quark1_two_cond"            , "Hreco_j1Idx"                                  ) : [ "","Hreco_jet_matches_quark1_two_cond>=0"           ,"Hreco_j1Idx>=0","jm1_j1", 10, -1., 10.,10,-1,10],
    ("Hreco_jet_matches_quark2_two_cond"            , "Hreco_j2Idx"                                  ) : [ "","Hreco_jet_matches_quark2_two_cond>=0"           ,"Hreco_j1Idx>=0","jm2_j2", 10, -1., 10.,10,-1,10],
    ("Hreco_delR_lep_jm_farthest"                   , "Hreco_delR_lep_jm_closest"                    ) : [ "","Hreco_delR_lep_jm_farthest>=0"                  ,"Hreco_delR_lep_jm_closest>=0","jm_close_jm_far_from_lepton", 100, 0., 10.,100,0.,10.],
}

def draw_plot(var,suffix,cut,fname,nbins,lowbin, highbin):
        c = TCanvas()
        c.cd()
        theplot = TH1F(var,var, nbins, lowbin, highbin)
        tr.Draw("%s>>%s"%(var,var),cut)
        theplot.Draw()
        c.Print("%s/%s%s.png"%(options.outputDir,fname,suffix))

#TODO overwrites variables
'''
def draw_plot(args):
    for var,pars in args.items():
        suffix, cut,fname,nbins,lowbin, highbin = pars
        c = TCanvas()
        c.cd()
        theplot = TH1F("%s_%s"%(var,suffix),var, nbins, lowbin, highbin)
        #theplot = TH1F(var,var, nbins, lowbin, highbin)
        tr.Draw("%s>>%s_%s"%(var,var,suffix),cut)
        #tr.Draw("%s>>%s"%(var,var),cut)
        theplot.Draw()
        print (theplot.Integral())
        c.Print("%s/%s_%s.png"%(options.outputDir,fname, suffix)) 
'''
def draw_comparison(args): #TODO the hist title is always the first var--> confusing when comparing two different vars
    fname = args['pars'].keys()[0]
    nbins, lowbin, highbin = args['pars'].values()[0]
    c   = TCanvas('c', 'c', 800, 800)
    leg = TLegend(0.5,0.6,0.9,0.9)
    c.cd()
    ps = [] # This is needed because ROOT is a mess
    h=TH1F('h', '', nbins, lowbin, highbin)
    h.Draw("ICE")
    ip=0
    ymax=0
    for var, val in args['vars'].items():
        ps.append(TH1F(var, var, nbins, lowbin, highbin))
        tr.Draw("%s>>%s"%(var,var),val)
        ps[ip].GetXaxis().SetTitle("%s [GeV]"%fname)
        ps[ip].GetYaxis().SetTitle("a.u.")
        ps[ip].SetLineColor(colours[var])
        ps[ip].Scale(1./ps[ip].Integral()) if ps[ip].Integral() != 0 else -99
        if ps[ip].GetMaximum() > ymax:
            ymax=ps[ip].GetMaximum()
        leg.AddEntry(ps[ip],val)
        ip+=1
    # Find the maximum dynamically
    for p in ps:
        p.GetYaxis().SetRangeUser(0, 1.1*ymax)
        p.Draw("HIST SAME")

    leg.Draw()
    #c.SetLogy()
    c.Modified()
    c.Update()
    c.Print("%s/%s_comp.png"%(options.outputDir,fname)) # Avoid overwriting single var plots

def draw_scatter(args):
    for var, pars in args.items():
        var1, var2 = var
        suffix, cut1, cut2, fname, nbinsx, lowbinx, highbinx, nbinsy, lowbiny, highbiny = pars
        c   = TCanvas()
        c.cd()
        theplot_scat = TH2F(var2,var2, nbinsx, lowbinx, highbinx, nbinsy, lowbiny, highbiny)
        theplot_scat.GetXaxis().SetTitle("%s"%var2)
        theplot_scat.GetYaxis().SetTitle("%s"%var1)
        tr.Draw("%s:%s>>%s"%(var1,var2,var2),cut1)
        theplot_scat.Draw("COLZ")
        theplot_scat.SetTitle("%s_Vs_%s"%(var1,var2))
        c.Print("%s/%s_%s_2D.png"%(options.outputDir,fname,suffix))
        
for var, suffix,cut, fname, nbins, lowbin, highbin in plotlist:
        draw_plot(var, suffix,cut, fname, nbins, lowbin, highbin)
#TODO overwrites variables
#draw_plot(plotdict)
draw_scatter(scatterplotdict)
for cplot in comparisonplotlist:
    draw_comparison(cplot)

