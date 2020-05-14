import os
from ROOT import gROOT, TTree, TFile, TCanvas, TH1F, kBlack, kRed


class Validation_HiggsDiffGenTTH():
    def __init__(self, fname='', tname='Friends', label='Hreco_', outdir='test'):
        gROOT.SetBatch()
        self.f = TFile.Open(fname, 'read')
        if not self.f:
            print('Cannot open file %s. Exiting'%fname)
            return
        self.t = self.f.Get(tname)
        if not self.t:
            print('Cannot open tree %s. Exiting'%tname)
            return
        self.label=label
        self.outdir=outdir
        if not os.path.isdir(self.outdir):
            os.makedirs(self.outdir)
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
                

    def buildPlotListFromBranches(self):
        # Particle counters
        self.p.append(['%snHiggses'%self.label         , 5, -0.5, 4.5])
        self.p.append(['%snTfromhardprocess'%self.label, 5, -0.5, 4.5])
        self.p.append(['%snWFromH'%self.label          , 5, -0.5, 4.5])
        self.p.append(['%snWFromT'%self.label          , 5, -0.5, 4.5])
        self.p.append(['%snQFromW'%self.label          , 5, -0.5, 4.5])
        self.p.append(['%snGenLep'%self.label          , 5, -0.5, 4.5])
        self.p.append(['%snLFromW'%self.label          , 5, -0.5, 4.5])
        self.p.append(['%snNuFromWFromH'%self.label    , 5, -0.5, 4.5])
        self.p.append(['%snNuFromWFromT'%self.label    , 5, -0.5, 4.5])
        self.p.append(['%snQFromWFromH'%self.label     , 5, -0.5, 4.5])
        self.p.append(['%snQFromWFromT'%self.label     , 5, -0.5, 4.5])
        self.p.append(['%snLFromWFromH'%self.label     , 5, -0.5, 4.5])
        self.p.append(['%snLFromWFromT'%self.label     , 5, -0.5, 4.5])


        for obj in [0, 1]:

            self.p.append(['%spTtgen'%self.label, '%spTtgen%s'%(self.label, obj), 401, -1., 400.])

            for suffix in ['_Pt', '_Eta', '_Phi', '_M']:

                # These should be guaranteed to be only 1
                if ('Pt' in suffix) or ('M' in suffix):
                    if obj==0:
                        self.p.append(['%sHiggses%s'%(self.label,suffix),'%sHiggses%s%s'%(self.label,obj,suffix), 401, -1., 400.])
                        self.p.append(['%sWFromH%s'%(self.label,suffix) ,'%sWFromH%s%s'%(self.label,obj,suffix) , 401, -1., 400.])
                        self.p.append(['%sWFromT%s'%(self.label,suffix) ,'%sWFromT%s%s'%(self.label,obj,suffix) , 401, -1., 400.])
                        self.p.append(['%sLFromW%s'%(self.label,suffix) ,'%sLFromW%s%s'%(self.label,obj,suffix) , 401, -1., 400.])
                        
                    self.p.append(['%sTfromhardprocess%s'%(self.label,suffix) ,'%sTfromhardprocess%s%s'%(self.label,obj,suffix) , 401, -1., 400. ])
                    self.p.append(['%sQFromW%s'%(self.label,suffix)           ,'%sQFromW%s%s'%(self.label,obj,suffix)           , 401, -1., 400. ])
                    self.p.append(['%sGenLep%s'%(self.label,suffix)           ,'%sGenLep%s%s'%(self.label,obj,suffix)           , 401, -1., 400. ])
                    self.p.append(['%sQFromWFromH%s'%(self.label,suffix)      ,'%sQFromWFromH%s%s'%(self.label,obj,suffix)      , 401, -1., 400. ])
                    self.p.append(['%sQFromWFromT%s'%(self.label,suffix)      ,'%sQFromWFromT%s%s'%(self.label,obj,suffix)      , 401, -1., 400. ])
                    self.p.append(['%sLFromWFromH%s'%(self.label,suffix)      ,'%sLFromWFromH%s%s'%(self.label,obj,suffix)      , 401, -1., 400. ])
                    self.p.append(['%sLFromWFromT%s'%(self.label,suffix)      ,'%sLFromWFromT%s%s'%(self.label,obj,suffix)      , 401, -1., 400. ])
                    self.p.append(['%sNuFromWFromH%s'%(self.label,suffix)     ,'%sNuFromWFromH%s%s'%(self.label,obj,suffix)     , 401, -1., 400. ])
                    self.p.append(['%sNuFromWFromT%s'%(self.label,suffix)     ,'%sNuFromWFromT%s%s'%(self.label,obj,suffix)     , 401, -1., 400. ])

                if 'Eta' in suffix:
                    if obj==0:    
                        self.p.append(['%sHiggses%s'%(self.label,suffix),'%sHiggses%s%s'%(self.label,obj,suffix), 200, -6., 6.])
                        self.p.append(['%sWFromH%s'%(self.label,suffix) ,'%sWFromH%s%s'%(self.label,obj,suffix) , 200, -6., 6.])
                        self.p.append(['%sWFromT%s'%(self.label,suffix) ,'%sWFromT%s%s'%(self.label,obj,suffix) , 200, -6., 6.])
                        self.p.append(['%sLFromW%s'%(self.label,suffix) ,'%sLFromW%s%s'%(self.label,obj,suffix) , 200, -6., 6.])
                        
                    self.p.append(['%sTfromhardprocess%s'%(self.label,suffix) ,'%sTfromhardprocess%s%s'%(self.label,obj,suffix) ,200, -6., 6. ])
                    self.p.append(['%sQFromW%s'%(self.label,suffix)           ,'%sQFromW%s%s'%(self.label,obj,suffix)           ,200, -6., 6. ])
                    self.p.append(['%sGenLep%s'%(self.label,suffix)           ,'%sGenLep%s%s'%(self.label,obj,suffix)           ,200, -6., 6. ])
                    self.p.append(['%sQFromWFromH%s'%(self.label,suffix)      ,'%sQFromWFromH%s%s'%(self.label,obj,suffix)      ,200, -6., 6. ])
                    self.p.append(['%sQFromWFromT%s'%(self.label,suffix)      ,'%sQFromWFromT%s%s'%(self.label,obj,suffix)      ,200, -6., 6. ])
                    self.p.append(['%sLFromWFromH%s'%(self.label,suffix)      ,'%sLFromWFromH%s%s'%(self.label,obj,suffix)      ,200, -6., 6. ])
                    self.p.append(['%sLFromWFromT%s'%(self.label,suffix)      ,'%sLFromWFromT%s%s'%(self.label,obj,suffix)      ,200, -6., 6. ])
                    self.p.append(['%sNuFromWFromH%s'%(self.label,suffix)     ,'%sNuFromWFromH%s%s'%(self.label,obj,suffix)     ,200, -6., 6. ])
                    self.p.append(['%sNuFromWFromT%s'%(self.label,suffix)     ,'%sNuFromWFromT%s%s'%(self.label,obj,suffix)     ,200, -6., 6. ])

                if 'Phi' in suffix:
                    if obj==0:
                        self.p.append(['%sHiggses%s'%(self.label,suffix),'%sHiggses%s%s'%(self.label,obj,suffix), 200, -6.28, 6.28])
                        self.p.append(['%sWFromH%s'%(self.label,suffix) ,'%sWFromH%s%s'%(self.label,obj,suffix) , 200, -6.28, 6.28])
                        self.p.append(['%sWFromT%s'%(self.label,suffix) ,'%sWFromT%s%s'%(self.label,obj,suffix) , 200, -6.28, 6.28])
                        self.p.append(['%sLFromW%s'%(self.label,suffix) ,'%sLFromW%s%s'%(self.label,obj,suffix) , 200, -6.28, 6.28])
                    self.p.append(['%sTfromhardprocess%s'%(self.label,suffix) ,'%sTfromhardprocess%s%s'%(self.label,obj,suffix) , 200, -6.28, 6.28 ])
                    self.p.append(['%sQFromW%s'%(self.label,suffix)           ,'%sQFromW%s%s'%(self.label,obj,suffix)           , 200, -6.28, 6.28 ])
                    self.p.append(['%sGenLep%s'%(self.label,suffix)           ,'%sGenLep%s%s'%(self.label,obj,suffix)           , 200, -6.28, 6.28 ])
                    self.p.append(['%sQFromWFromH%s'%(self.label,suffix)      ,'%sQFromWFromH%s%s'%(self.label,obj,suffix)      , 200, -6.28, 6.28 ])
                    self.p.append(['%sQFromWFromT%s'%(self.label,suffix)      ,'%sQFromWFromT%s%s'%(self.label,obj,suffix)      , 200, -6.28, 6.28 ])
                    self.p.append(['%sLFromWFromH%s'%(self.label,suffix)      ,'%sLFromWFromH%s%s'%(self.label,obj,suffix)      , 200, -6.28, 6.28 ])
                    self.p.append(['%sLFromWFromT%s'%(self.label,suffix)      ,'%sLFromWFromT%s%s'%(self.label,obj,suffix)      , 200, -6.28, 6.28 ])
                    self.p.append(['%sNuFromWFromH%s'%(self.label,suffix)     ,'%sNuFromWFromH%s%s'%(self.label,obj,suffix)     , 200, -6.28, 6.28 ])
                    self.p.append(['%sNuFromWFromT%s'%(self.label,suffix)     ,'%sNuFromWFromT%s%s'%(self.label,obj,suffix)     , 200, -6.28, 6.28 ])
                        
        # Some precomputed quantities of interest
        self.p.append(['%spTHgen'%self.label            , 101, -1., 100.])
        self.p.append(['%sinv_mass_q1_q2'%self.label    , 101, -1., 100.])
        self.p.append(['%sdelR_partonsFromH'%self.label , 110, -1., 10.])
        self.p.append(['%squark1pT'%self.label          , 101, -1, 100.])
        self.p.append(['%squark2pT'%self.label          , 101, -1, 100.])
        self.p.append(['%sdelR_H_q1l'%self.label        , 110, -1., 10.])
        self.p.append(['%sdelR_H_q2l'%self.label        , 110, -1., 10.])
        self.p.append(['%spTTrueGen'%self.label         , 101, -1., 100.])
        self.p.append(['%spTTrueGenPlusNu'%self.label   , 101, -1., 100.])
        
        
for year in [2016, 2017, 2018]:
    validator = Validation_HiggsDiffGenTTH('/nfs/user/pvischia/tth/v6/NanoTrees_TTH_091019_v6pre_skim2lss_tight/%s/6_higgsDiffGenTTH/TTHnobb_fxfx_Friend.root'%year, outdir='validationPlots_higgsDiffGenTTH/%s'%year)
    validator.buildPlotListFromBranches()
    validator.printPlotList()
    validator.plotList()
    del validator
