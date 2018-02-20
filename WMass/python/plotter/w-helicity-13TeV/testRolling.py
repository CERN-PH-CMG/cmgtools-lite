import ROOT, os
from array import array


def getbinning(splitline):
    bins = splitline[5]
    if '*' in bins:
        etabins = list( float(i) for i in bins.split('*')[0].replace('\'[','').replace(']','').split(',') )
        ptbins  = list( float(i) for i in bins.split('*')[1].replace('[','').replace(']\'','').split(',') )
        nbinseta = len(etabins)-1
        nbinspt  = len( ptbins)-1
        binning = [nbinseta, etabins, nbinspt, ptbins]
    else:
        bins = bins.replace('\'','')
        nbinseta = int( bins.split(',')[0] )
        nbinspt  = int( bins.split(',')[3] )
        etamin   = float( bins.split(',')[1] )
        etamax   = float( bins.split(',')[2] )
        ptmin    = float( bins.split(',')[4] )
        ptmax    = float( bins.split(',')[5] )
    return binning

ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetPadRightMargin(0.13)

def roll1Dto2D(h1d, histo):#,h2dname):#,plotfile,options):
    ## pfile = PlotFile(plotfile,options)
    ## pspecs = pfile.plots()
    ## matchspec = [ p for p in pspecs if p.name == h2dname ]
    ## if not matchspec: raise RuntimeError, "Error: plot %s not found" % h2dname
    ## if len(matchspec)>1: print "WARNING! more than one plot matching %s. Taking the specifics from the first occurence in plotfile %s" % (h2dname,plotfile)
    ## p2d = matchspec[0]
    ## histo = makeHistFromBinsAndSpec("%s_%s" % (h2dname,h1d.GetName()),p2d.expr,p2d.bins,None)
    #histo = ROOT.TH2F('backrolledh2', 'backrolledh2', 10, 0, 10., 20, 0., 10.)
    ## histo.GetYaxis().SetTitle(p2d.getOption('YTitle'))
    ## histo.GetXaxis().SetTitle(p2d.getOption('XTitle'))
    ## histo.SetContour(100)
    ## ROOT.gStyle.SetPaintTextFormat(p2d.getOption("PaintTextFormat","g"))
    ## histo.SetMarkerSize(p2d.getOption("MarkerSize",1))
    ## if p2d.hasOption('ZMin') and p2d.hasOption('ZMax'):
    ##     histo.GetZaxis().SetRangeUser(p2d.getOption('ZMin',1.0), p2d.getOption('ZMax',1.0))
    ## if 'TH2' not in histo.ClassName(): raise RuntimeError, "Trying to roll the 1D histo on something that is not TH2"
    for i in xrange(1,h1d.GetNbinsX()+1):
        xbin = i % histo.GetNbinsX()
        if not xbin: xbin = xbin+histo.GetNbinsX()
        ybin = i / histo.GetNbinsX() + (1 if i%histo.GetNbinsX() else 0)
        val = h1d.GetBinContent(i)
        histo.SetBinContent(xbin,ybin,h1d.GetBinContent(i))
    return histo

def unroll2Dto1D(h):
    nbins = h.GetNbinsX() * h.GetNbinsY()
    goodname = h.GetName()
    h.SetName(goodname+"_oldbinning")
    newh = ROOT.TH1D(goodname,h.GetTitle(),nbins,0.5,nbins+0.5)
    if 'TH2' not in h.ClassName(): raise RuntimeError, "Calling rebin2Dto1D on something that is not TH2"
    for i in xrange(h.GetNbinsX()):
        for j in xrange(h.GetNbinsY()):
            bin = 1 + i + j*h.GetNbinsX()
            newh.SetBinContent(bin,h.GetBinContent(i+1,j+1))
            newh.SetBinError(bin,h.GetBinError(i+1,j+1))
    for bin in range(1,nbins+1):
        if newh.GetBinContent(bin)<0:
            print 'Warning: cropping to zero bin %d in %s (was %f)'%(bin,newh.GetName(),newh.GetBinContent(bin))
            newh.SetBinContent(bin,0)
    newh.SetLineWidth(h.GetLineWidth())
    newh.SetLineStyle(h.GetLineStyle())
    newh.SetLineColor(h.GetLineColor())
    return newh

##h2 = ROOT.TH2F('myh2', 'myh2', 10, 0, 10., 20, 0., 10.)
##
##
##rand1 = ROOT.TRandom3()
##
##
##for i in range(int(1e6)):
##    x = rand1.Gaus(5.,2.)
##    y = rand1.Gaus(6.,3.)
##    h2.Fill(x, y)

ROOT.gROOT.SetBatch()

#shapesfile = '/afs/cern.ch/work/m/mdunser/public/cmssw/w-helicity-13TeV/CMSSW_8_0_25/src/CMGTools/WMass/python/plotter/cards/helicity_2018_02_08_binsEta32_binsPt20_binsY26/Wmu_plus_shapes.root'
#shapesfile = '/afs/cern.ch/work/m/mdunser/public/cmssw/w-helicity-13TeV/CMSSW_8_0_25/src/CMGTools/WMass/python/plotter/cards/helicity_2018_02_09_variablebinningEta_binsPt20_longBkg/mu_minus_shapes.root'
#shapesfile = '/afs/cern.ch/work/m/mdunser/public/cmssw/w-helicity-13TeV/CMSSW_8_0_25/src/CMGTools/WMass/python/plotter/cards/helicity_2018_02_12_variableEta_ptBins20_longBkg_MTTK45/mu_minus_shapes.root'
shapesfile = '/afs/cern.ch/work/m/mdunser/public/cmssw/w-helicity-13TeV/CMSSW_8_0_25/src/CMGTools/WMass/python/plotter/cards/helicity_2018_02_12_variableEta_ptBins20_longBkg_MTTK45/mu_minus_shapes.root'


infile = ROOT.TFile(shapesfile, 'read')
for charge in ['minus']:#, 'minus']:
    for pol in ['right', 'left']:
        for ybin in range(26): 

            jobsdir = os.path.dirname(shapesfile)+'/jobs/'
            jobfile_name = 'W{ch}_mu_Ybin_{b}.sh'.format(ch=charge,b=ybin)
            tmp_jobfile = open(jobsdir+jobfile_name, 'r')
            tmp_line = tmp_jobfile.readlines()[-1].split()
            ymin = list(i for i in tmp_line if 'genw_y>' in i)[0].replace('\'','').split('>')[-1]
            ymax = list(i for i in tmp_line if 'genw_y<' in i)[0].replace('\'','').split('<')[-1]

            binning = getbinning(tmp_line)

            chs = '+' if charge == 'plus' else '-'

            h1_1 = infile.Get('x_W{ch}_{pol}_W{ch}_mu_Ybin_{ybin}'.format(ch=charge,pol=pol,ybin=ybin))
            if len(binning) == 4:
                n1 = binning[0]; bins1 = array('d', binning[1])
                n2 = binning[2]; bins2 = array('d', binning[3])
                h2_1 = ROOT.TH2F('h2_1', 'W{ch} {pol} : Y_{{W}} #in [{ymin},{ymax}]'.format(ymin=ymin,ymax=ymax,pol=pol,ybin=ybin,ch=chs) , n1, bins1, n2, bins2 )
            else:
                n1 = binning[0]; min1 = binning[1]; max1 = binning[2]
                n2 = binning[3]; min2 = binning[4]; max2 = binning[5]
                h2_1 = ROOT.TH2F('h2_1', 'W{ch} {pol} : Y_{{W}} #in [{ymin},{ymax}]'.format(ymin=ymin,ymax=ymax,pol=pol,ybin=ybin,ch=chs) , n1, min1, max1, n2, min2, max2)
            h2_backrolled_1 = roll1Dto2D(h1_1, h2_1 )
            h2_backrolled_1 .GetXaxis().SetTitle('lepton #eta')
            h2_backrolled_1 .GetYaxis().SetTitle('lepton p_{T} (GeV)')
            h2_backrolled_1 .GetZaxis().SetRangeUser(0.1*h2_backrolled_1.GetMaximum(),1.1*h2_backrolled_1.GetMaximum())
            
            
            canv = ROOT.TCanvas()
            h2_backrolled_1.Draw('colz')
            for ext in ['pdf', 'png']:
                canv.SaveAs('~/www/private/w-helicity-13TeV/helicityTemplates/backrolledTemplates/W{ch}_{pol}_W{ch}_mu_Ybin_{ybin}_MTTK45.{ext}'.format(ch=charge,pol=pol,ybin=ybin,ext=ext))
## canv.Divide(1,2)
## canv.cd(1)
## h2.Draw('colz')
## canv.cd(2)
## h2backrolled.Draw('colz')
