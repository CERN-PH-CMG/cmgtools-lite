import os
from ROOT import gROOT, TTree, TFile, TCanvas, TH1F, kBlack, kRed, kBlue, TLegend


class Validation_HiggsDiffCompTTH():
    def __init__(self, fname='', tname='Friends', label='Hreco_', outdir='test', doSystJEC=True, altfname=None):
        gROOT.SetBatch()
        self.f = TFile.Open(fname, 'read')
        if not self.f:
            print('Cannot open file %s. Exiting'%fname)
            return
        self.t = self.f.Get(tname)
        if not self.t:
            print('Cannot open tree %s for file %s. Exiting'%(tname,fname))
            return
        self.altf = TFile.Open(altfname, 'read') if altfname else None
        #self.altt = self.altf.Get(tname) if self.altf else None
        #if altfname and not self.altt:
        #    print('File for Wmass constraint comparison specified but either file or tree not opened: %s'%altfname)
        #    return
        self.altfname=altfname
        if self.t and self.altfname:
            self.t.AddFriend('alttree = %s'%tname, altfname)
        self.label=label
        self.outdir=outdir
        if not os.path.isdir(self.outdir):
            os.makedirs(self.outdir)
        self.p=[]
        self.systsJEC = {0:"", 1:"_jesTotalCorrUp", -1:"_jesTotalCorrDown"} if doSystJEC else {0:""}

    def printPlotList(self):
        for plot in self.p:
            print('Plotting:', plot)

    def plotList(self):
        for plot in self.p:
            if len(plot)==4:
                name, nbins, xlow, xhigh = plot
                c = TCanvas('c%s'%name,name)
                c.cd()
                h = TH1F('h%s'%name, name, nbins, xlow, xhigh)
                self.t.Draw('%s>>h%s'%(name,name))
                h.Draw('hist')
                h.SetLineWidth(2)
                h.SetLineColor(kBlack)
                c.Print('%s/%s.png'%(self.outdir,name))
                del c
            elif len(plot)==5:
                name, plotname, nbins, xlow, xhigh = plot
                c = TCanvas('c%s'%plotname, plotname)
                c.cd()
                h = TH1F('h%s'%plotname, plotname, nbins, xlow, xhigh)
                drawname='%s[0]'%name if '0' in plotname else ('%s[1]'%name if '1' in plotname else '')
                self.t.Draw('%s>>h%s'%(drawname,plotname))
                h.Draw('hist')
                h.SetLineWidth(2)
                h.SetLineColor(kBlack)
                c.Print('%s/%s.png'%(self.outdir,plotname))
                del c
            elif len(plot)==10 and self.altfname:
                # Comparison plot
                name, nbinsd, xlowd, xhighd, nbins, xlow, xhigh, nbinsz, xlowz, xhighz = plot
                c = TCanvas('c%scomp'%name, name)
                c.cd()
                h = TH1F('h%s'%name, name, nbinsd, xlowd, xhighd)
                self.t.Draw('(%s-alttree.%s)>>h%s'%(name,name, name ))
                #self.t.Draw('%s>>h%s'%(name,name))
                h.Draw('hist')
                #hnoconstr = TH1F('h%snoconstr'%name, name, nbins, xlow, xhigh)
                #self.altt.Draw('%s>>h%snoconstr'%(name,name))
                #hnoconstr.Draw('histsame')
                h.SetMaximum(1.3*h.GetMaximum())
                h.SetLineWidth(2)
                h.SetLineColor(kBlack)
                h.SetTitle('%s(Wconstr) - %s(noWconstr)'%(name,name))
                #hnoconstr.SetLineWidth(2)
                #hnoconstr.SetLineColor(kRed)
                #leg = TLegend(0.7, 0.8, 0.9, 0.9)
                #leg.AddEntry(h, 'Constrained dijet mass', 'l')
                #leg.AddEntry(hnoconstr, 'Unconstrained dijet mass', 'l')
                #leg.Draw()
                c.Print('%s/%s_constraintDifference.png'%(self.outdir,name))
                hn   = TH1F('hn%s'%name, name, nbins, xlow, xhigh)
                hnno = TH1F('hnno%s'%name, name, nbins, xlow, xhigh)
                self.t.Draw('%s>>hn%s'%(name,name ))
                self.t.Draw('alttree.%s>>hnno%s'%(name,name ))
                hn.Draw('hist')
                hnno.Draw('hist same')
                hn.SetLineColor(kBlue)
                hnno.SetLineColor(kRed)
                hn.SetLineWidth(2)
                hnno.SetLineWidth(2)
                leg = TLegend(0.7, 0.8, 0.9, 0.9)
                leg.AddEntry(hn, 'Constrained dijet mass', 'l')
                leg.AddEntry(hnno, 'Unconstrained dijet mass', 'l')
                leg.Draw()
                c.Print('%s/%s_constraintComparison.png'%(self.outdir,name))
                hn   = TH1F('hn%s'%name, name,   nbinsz, xlowz, xhighz)
                hnno = TH1F('hnno%s'%name, name, nbinsz, xlowz, xhighz)
                self.t.Draw('%s>>hn%s'%(name,name ))
                self.t.Draw('alttree.%s>>hnno%s'%(name,name ))
                hn.SetLineColor(kBlue)
                hnno.SetLineColor(kRed)
                hn.SetLineWidth(2)
                hnno.SetLineWidth(2)
                leg = TLegend(0.7, 0.8, 0.9, 0.9)
                leg.AddEntry(hn, 'Constrained dijet mass', 'l')
                leg.AddEntry(hnno, 'Unconstrained dijet mass', 'l')
                hn.Draw('hist')
                hnno.Draw('hist same')
                leg.Draw()
                c.Print('%s/%s_constraintZoomedComparison.png'%(self.outdir,name))
                del c
                

    def buildPlotListFromBranches(self):

        # Independent on JES
        
        # Somehow dependent on JES
        for jesLabel in self.systsJEC.values():
            self.p.append(['%spTVisCrossCheck%s'%(self.label,jesLabel)                      , 200, -100., 100.])
            self.p.append(['%spTVisPlusNu%s'%(self.label,jesLabel)                          , 200, -100., 100.])
            self.p.append(['%spTVis_jets_match%s'%(self.label,jesLabel)                     , 200, -100., 100.])
            self.p.append(['%spTVis_jets_match_plusNu%s'%(self.label,jesLabel)              , 200, -100., 100.])
            self.p.append(['%spTVis_jets_match_plusNu_plus_gen_lep%s'%(self.label,jesLabel) , 200, -100., 100.])
            self.p.append(['%spTVis_jets_match_with_gen_lep%s'%(self.label,jesLabel)        , 200, -100., 100.])
            self.p.append(['%sclosestJet_pt_ToQ1FromWFromH%s'%(self.label,jesLabel)         , 200, -100., 100.])
            self.p.append(['%sclosestJet_pt_ToQ2FromWFromH%s'%(self.label,jesLabel)         , 200, -100., 100.])

            # Comparison
            self.p.append(['%spTVisCrossCheck%s'%(self.label,jesLabel)                      , 200, -5., 5., 200, -100., 100., 200, -100., 100.])
            self.p.append(['%spTVisPlusNu%s'%(self.label,jesLabel)                          , 200, -5., 5., 200, -100., 100., 200, -100., 100.])
            self.p.append(['%spTVis_jets_match%s'%(self.label,jesLabel)                     , 200, -5., 5., 200, -100., 100., 200, -100., 100.])
            self.p.append(['%spTVis_jets_match_plusNu%s'%(self.label,jesLabel)              , 200, -5., 5., 200, -100., 100., 200, -100., 100.])
            self.p.append(['%spTVis_jets_match_plusNu_plus_gen_lep%s'%(self.label,jesLabel) , 200, -5., 5., 200, -100., 100., 200, -100., 100.])
            self.p.append(['%spTVis_jets_match_with_gen_lep%s'%(self.label,jesLabel)        , 200, -5., 5., 200, -100., 100., 200, -100., 100.])
            self.p.append(['%sclosestJet_pt_ToQ1FromWFromH%s'%(self.label,jesLabel)         , 200, -5., 5., 200, -100., 100., 200, -100., 100.])
            self.p.append(['%sclosestJet_pt_ToQ2FromWFromH%s'%(self.label,jesLabel)         , 200, -5., 5., 200, -100., 100., 200, -100., 100.])

            self.p.append(['%snmatchedpartons%s'%(self.label,jesLabel)                      , 7, -2., 5.])

            self.p.append(['%sinv_mass_jm1jm2%s'%(self.label,jesLabel)                      , 600, -100., 500.])
            self.p.append(['%sinv_mass_H_jets_match_plusNu%s'%(self.label,jesLabel)         , 600, -100., 500.])
            self.p.append(['%sinv_mass_H_jets_match%s'%(self.label,jesLabel)                , 600, -100., 500.])

            self.p.append(['%sclosestJet_ptres_ToQ1FromWFromH%s'%(self.label,jesLabel)      , 500, -5., 5.])
            self.p.append(['%sclosestJet_ptres_ToQ2FromWFromH%s'%(self.label,jesLabel)      , 500, -5., 5.])

            self.p.append(['%sdelR_lep_jm1%s'%(self.label,jesLabel)                         , 60, -1., 5.])
            self.p.append(['%sdelR_lep_jm2%s'%(self.label,jesLabel)                         , 60, -1., 5.])
            self.p.append(['%sdelR_jm1_jm2%s'%(self.label,jesLabel)                         , 60, -1., 5.])
            self.p.append(['%sclosestJet_delR_ToQ1FromWFromH%s'%(self.label,jesLabel)       , 60, -1., 5.])
            self.p.append(['%sclosestJet_delR_ToQ2FromWFromH%s'%(self.label,jesLabel)       , 60, -1., 5.])
            self.p.append(['%sdelR_lep_jm_closest%s'%(self.label,jesLabel)                  , 60, -1., 5.])
            self.p.append(['%sdelR_lep_jm_farthest%s'%(self.label,jesLabel)                 , 60, -1., 5.])
            self.p.append(['%sdelR_jm_closest_jm_farthest%s'%(self.label,jesLabel)          , 60, -1., 5.])
            self.p.append(['%sdelR_lep_closest_wrongjet%s'%(self.label,jesLabel)            , 60, -1., 5.])


        

for year in [2016, 2017, 2018]:
    print('With windows, year %s'%year)
    validator = None
    #if year == 2016:
    validator = Validation_HiggsDiffCompTTH('/nfs/user/pvischia/tth/v6/NanoTrees_TTH_091019_v6pre_skim2lss_tight/%s/6_higgsDiffCompTTH/TTHnobb_fxfx_Friend.root'%year, outdir='validationPlots_higgsDiffCompTTH/%s'%year, altfname='/nfs/user/pvischia/tth/v6/NanoTrees_TTH_091019_v6pre_skim2lss_tight/%s/6_higgsDiffCompTTH_noWmassConstraint/TTHnobb_fxfx_Friend.root'%year)
    #else:
    #    validator = Validation_HiggsDiffCompTTH('/nfs/user/pvischia/tth/v6/NanoTrees_TTH_091019_v6pre_skim2lss_tight/%s/6_higgsDiffCompTTH/TTHnobb_fxfx_Friend.root'%year, outdir='validationPlots_higgsDiffCompTTH/%s'%year)
    validator.buildPlotListFromBranches()
    validator.printPlotList()
    validator.plotList()
    
