import ROOT, os, copy
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

ROOT.gROOT.SetBatch()




canv = ROOT.TCanvas()

for charge in ['minus']: #, 'plus']:
    shapesfile = '/afs/cern.ch/user/e/emanuele/w/wmass/heppy/CMSSW_8_0_25/src/CMGTools/WMass/python/plotter/cards/helicity_2018_03_09_testpdfsymm/Wel_{ch}_shapes.root'.format(ch=charge)
    infile = ROOT.TFile(shapesfile, 'read')
    keylist = infile.GetListOfKeys()
    siglist = list( i.GetName() for i in keylist if 'Ybin_' in i.GetName() )
    nY = max( int(i.split('_')[-2]) for i in siglist if 'pdf' in i)
    nPDF = max( int(i.split('_')[-1].replace('pdf','').replace('Down','').replace('Up','')) for i in siglist if 'pdf' in i)

    for pol in ['right', 'left']:
        jobsdir = os.path.dirname(shapesfile)+'/jobs/'
        jobfile_name = 'W{ch}_el_Ybin_0.sh'.format(ch=charge)
        tmp_jobfile = open(jobsdir+jobfile_name, 'r')
        tmp_line = tmp_jobfile.readlines()[-1].replace(', ',',').split()

        binning = getbinning(tmp_line)

        histo_central = infile.Get('x_W{ch}_{pol}_W{ch}_el_Ybin_0'.format(ch=charge,pol=pol))
        for iy in range(1,nY+1):
            histo_central.Add(infile.Get('x_W{ch}_{pol}_W{ch}_el_Ybin_{i}'.format(ch=charge,pol=pol,i=iy)))
        #for ybin in range(1):nY+1): 
        ratios = {}
        for ip in range(1,nPDF+1):
            histo_pdfi = infile.Get('x_W{ch}_{pol}_W{ch}_el_Ybin_0_pdf{ip}Up'.format(ch=charge,pol=pol,ip=ip))
            for iy in range(1,nY+1):
                histo_pdfi.Add(infile.Get('x_W{ch}_{pol}_W{ch}_el_Ybin_{iy}_pdf{ip}Up'.format(ch=charge,pol=pol,iy=iy,ip=ip)))
            ratio_pdfi = copy.deepcopy(histo_pdfi)
            ratio_pdfi.Divide(histo_central)

            for ib in range(1, ratio_pdfi.GetNbinsX()+1):
                ratio_pdfi.SetBinContent(ib, abs(1.-ratio_pdfi.GetBinContent(ib)))

            chs = '+' if charge == 'plus' else '-'

            if len(binning) == 4:
                n1 = binning[0]; bins1 = array('d', binning[1])
                n2 = binning[2]; bins2 = array('d', binning[3])
                h2_1 = ROOT.TH2F('h2_1', 'W{ch} {pol} : pdf {ip}'.format(ip=ip,pol=pol,ch=chs) , n1, bins1, n2, bins2 )
            else:
                n1 = binning[0]; min1 = binning[1]; max1 = binning[2]
                n2 = binning[3]; min2 = binning[4]; max2 = binning[5]
                h2_1 = ROOT.TH2F('h2_1', 'W{ch} {pol} : pdf {ip}'.format(ip=ip,pol=pol,ch=chs) , n1, min1, max1, n2, min2, max2)

            h2_backrolled_1 = roll1Dto2D(ratio_pdfi, h2_1 )
            h2_backrolled_1 .GetXaxis().SetTitle('lepton #eta')
            h2_backrolled_1 .GetYaxis().SetTitle('lepton p_{T} (GeV)')
            h2_backrolled_1 .GetZaxis().SetRangeUser(0.1*h2_backrolled_1.GetMaximum(),1.1*h2_backrolled_1.GetMaximum())

            h2_backrolled_1.GetZaxis().SetRangeUser(0.,0.02)
            h2_backrolled_1.Draw('colz')
            for ext in ['pdf', 'png']:
                canv.SaveAs('~/www/private/w-helicity-13TeV/pdfRatios/W{ch}_{pol}_W{ch}_el_pdfVariation{ip}.{ext}'.format(ch=charge,pol=pol,ip=ip,ext=ext))
            
## canv.Divide(1,2)
## canv.cd(1)
## h2.Draw('colz')
## canv.cd(2)
## h2backrolled.Draw('colz')
