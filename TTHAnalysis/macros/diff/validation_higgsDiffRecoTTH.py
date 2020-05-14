import os
from ROOT import gROOT, TTree, TFile, TCanvas, TH1F, kBlack, kRed, TLegend


class Validation_HiggsDiffGenTTH():
    def __init__(self, fname='', tname='Friends', label='Hreco_', outdir='test', doSystJEC=True, altfname=None):
        gROOT.SetBatch()
        self.f = TFile.Open(fname, 'read')
        if not self.f:
            print('Cannot open file %s. Exiting'%fname)
            return
        self.t = self.f.Get(tname)
        if not self.t:
            print('Cannot open tree %s. Exiting'%tname)
            return
        self.altf = TFile.Open(altfname, 'read') if altfname else None
        #self.altt = self.altf.Get(tname) if self.altf else None
        #if altfname and not self.altt:
        #    print('File for Wmass constraint comparison specified but either file or tree not opened: %s'%altfname)
        #    return
        if self.t and altfname:
            self.t.AddFriend('alttree = %s'%tname, altfname)
        self.label=label
        self.outdir=outdir
        self.systsJEC = {0:"", 1:"_jesTotalCorrUp", -1:"_jesTotalCorrDown"} if doSystJEC else {0:""}
        if not os.path.isdir(self.outdir):
            os.mkdir(self.outdir)
        self.p=[]

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
            elif len(plot)==6:
                # Comparison plot
                name, nbins, xlow, xhigh, _, _ = plot
                c = TCanvas('c%scomp'%name, name)
                c.cd()
                h = TH1F('h%s'%name, name, nbins, xlow, xhigh)
                self.t.Draw('(%s-%s.varname)>>h%s'%(name,name, name ))
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
                c.Print('%s/%s_constraintComparison.png'%(self.outdir,name))
                del c
                

    def buildPlotListFromBranches(self):

        self.p.append(['%sGenHiggsDecayMode'%(self.label), 20, -10, 10])

        # Somehow dependent on JES
        for jesLabel in self.systsJEC.values(): 

            # Some quantities
            self.p.append(['%svisHmass%s'%(self.label,jesLabel)                   , 200, -100, 100])
            self.p.append(['%sWmass%s'%(self.label,jesLabel)                      , 200, -100, 100])
            self.p.append(['%spTHvis%s'%(self.label,jesLabel)                     , 200, -100, 100])
            
            # The comparison (I add two dummy variables to match the array size later)
            self.p.append(['%svisHmass%s'%(self.label,jesLabel)                   , 200, -5., 5., 0, 0])
            self.p.append(['%sWmass%s'%(self.label,jesLabel)                      , 200, -5., 5., 0, 0])
            self.p.append(['%spTHvis%s'%(self.label,jesLabel)                     , 200, -5., 5., 0, 0])

            self.p.append(['%slepIdx%s'%(self.label,jesLabel)           ,5, -0.5, 4.5])
            self.p.append(['%sj1Idx%s'%(self.label,jesLabel)            ,5, -0.5, 4.5])
            self.p.append(['%sj2Idx%s'%(self.label,jesLabel)            ,5, -0.5, 4.5])
            self.p.append(['%snJetsFromHiggs%s'%(self.label,jesLabel)   ,5, -0.5, 4.5])    

            self.p.append(['%sminDRlj%s'%(self.label,jesLabel)          , 60, -1., 5.])
            self.p.append(['%sDRj1j2%s'%(self.label,jesLabel)           , 60, -1., 5.])
            self.p.append(['%sDRj1l%s'%(self.label,jesLabel)            , 60, -1., 5.])
            self.p.append(['%sDRj2l%s'%(self.label,jesLabel)            , 60, -1., 5.])
            
            self.p.append(['%sBDThttTT_eventReco_mvaValue%s'%(self.label,jesLabel), 20, -1., 1.])




            # Useful quadrimomenta
            for suffix in ["_Pt", "_Eta", "_Phi", "_M"]:

                if ('Pt' in suffix) or ('M' in suffix):
                    self.p.append(['%sleptonFromHiggs%s%s'%(self.label,suffix,jesLabel), 400, -100, 300])
                    for obj in [0, 1]:
                        self.p.append(['%sjetFromHiggs%s%s'%(self.label,suffix,jesLabel), '%sjetFromHiggs%s%s%s'%(self.label,obj,suffix,jesLabel) , 400, -100., 300.])
                    # not needed now, will add later self.out.branch('%sfatJetsNearLeptonFromHiggs%s%s'%(self.label,suffix,jesLabel)        , 'F', 2, '%snFatJetsNearLeptonFromHiggs%s'%(self.label,jesLabel))
                if 'Eta' in suffix:
                    self.p.append(['%sleptonFromHiggs%s%s'%(self.label,suffix,jesLabel), 200, -6, 6])
                    for obj in [0, 1]:
                        self.p.append(['%sjetFromHiggs%s%s'%(self.label,suffix,jesLabel), '%sjetFromHiggs%s%s%s'%(self.label,obj,suffix,jesLabel) , 200, -6., 6.])
                    # not needed now, will add later self.out.branch('%sfatJetsNearLeptonFromHiggs%s%s'%(self.label,suffix,jesLabel)        , 'F', 2, '%snFatJetsNearLeptonFromHiggs%s'%(self.label,jesLabel))
                if 'Phi' in suffix:
                    self.p.append(['%sleptonFromHiggs%s%s'%(self.label,suffix,jesLabel), 200, -6.28, 6.28])
                    for obj in [0, 1]:
                        self.p.append(['%sjetFromHiggs%s%s'%(self.label,suffix,jesLabel), '%sjetFromHiggs%s%s%s'%(self.label,obj,suffix,jesLabel) , 200, -6.28, 6.28])
                    # not needed now, will add later self.out.branch('%sfatJetsNearLeptonFromHiggs%s%s'%(self.label,suffix,jesLabel)        , 'F', 2, '%snFatJetsNearLeptonFromHiggs%s'%(self.label,jesLabel))
                
            # not needed now, will add later self.out.branch('%sfatJetsNearLeptonFromHiggs_deltaR%s'%(self.label,jesLabel)    , 'F', 2, '%snFatJetsNearLeptonFromHiggs%s'%(self.label,jesLabel))
            # not needed now, will add later self.out.branch('%sfatJetsNearLeptonFromHiggs_lepIsFromH%s'%(self.label,jesLabel), 'F', 2, '%snFatJetsNearLeptonFromHiggs%s'%(self.label,jesLabel))
            # not needed now, will add later self.out.branch('%sfatJetsNearLeptonFromHiggs_msoftdrop%s'%(self.label,jesLabel) , 'F', 2, '%snFatJetsNearLeptonFromHiggs%s'%(self.label,jesLabel))
            # not needed now, will add later self.out.branch('%sfatJetsNearLeptonFromHiggs_tau1%s'%(self.label,jesLabel)      , 'F', 2, '%snFatJetsNearLeptonFromHiggs%s'%(self.label,jesLabel))
            # not needed now, will add later self.out.branch('%sfatJetsNearLeptonFromHiggs_tau2%s'%(self.label,jesLabel)      , 'F', 2, '%snFatJetsNearLeptonFromHiggs%s'%(self.label,jesLabel))
            # not needed now, will add later self.out.branch('%sfatJetsNearLeptonFromHiggs_tau3%s'%(self.label,jesLabel)      , 'F', 2, '%snFatJetsNearLeptonFromHiggs%s'%(self.label,jesLabel))
            # not needed now, will add later self.out.branch('%sfatJetsNearLeptonFromHiggs_tau4%s'%(self.label,jesLabel)      , 'F', 2, '%snFatJetsNearLeptonFromHiggs%s'%(self.label,jesLabel))

        # The comparison
        

validator = Validation_HiggsDiffGenTTH('/nfs/user/pvischia/tth/v6/NanoTrees_TTH_091019_v6pre_skim2lss/2016/6_higgsDiffRecoTTH/TTHnobb_fxfx_Friend.root', outdir='validationPlots_higgsDiffRecoTTH', altfname='/nfs/user/pvischia/tth/v6/NanoTrees_TTH_091019_v6pre_skim2lss/2016/6_higgsDiffRecoTTH_noWmassConstraint/TTHnobb_fxfx_Friend.root')
validator.buildPlotListFromBranches()
validator.printPlotList()
validator.plotList()
