#!/usr/bin/env python
# USAGE: python w-helicity-13TeV/testRolling.py cards/XXX el -o plots/fit/templates2D
# el is for electrons, mu for muons

import ROOT, os
from array import array


def getbinning(splitline):
    bins = splitline[5]
    if '*' in bins:
        etabins = list( float(i) for i in bins.replace(' ','').split('*')[0].replace('\'[','').replace(']','').split(',') )
        ptbins  = list( float(i) for i in bins.replace(' ','').split('*')[1].replace('[','').replace(']\'','').split(',') )
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

def roll1Dto2D(h1d, histo):  #,h2dname):#,plotfile,options):
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

def dressed2D(h1d,binning,name,title=''):
    if len(binning) == 4:
        n1 = binning[0]; bins1 = array('d', binning[1])
        n2 = binning[2]; bins2 = array('d', binning[3])
        h2_1 = ROOT.TH2F(name, title, n1, bins1, n2, bins2 )
    else:
        n1 = binning[0]; min1 = binning[1]; max1 = binning[2]
        n2 = binning[3]; min2 = binning[4]; max2 = binning[5]
        h2_1 = ROOT.TH2F(name, title, n1, min1, max1, n2, min2, max2)
    h2_backrolled_1 = roll1Dto2D(h1_1, h2_1 )
    h2_backrolled_1 .GetXaxis().SetTitle('lepton #eta')
    h2_backrolled_1 .GetYaxis().SetTitle('lepton p_{T} (GeV)')
    h2_backrolled_1 .GetZaxis().SetRangeUser(0.01*h2_backrolled_1.GetMaximum(),1.1*h2_backrolled_1.GetMaximum())
    return h2_backrolled_1

ROOT.gROOT.SetBatch()

if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser(usage="%prog [options] shapesdir channel")
    parser.add_option('-o','--outdir', dest='outdir', default='.', type='string', help='output directory to save the matrix')
    parser.add_option(     '--noplot', dest="noplot", default=False, action='store_true', help="Do not plot templates (but you can still save them in a root file with option -s)");
    parser.add_option('-s','--save', dest='outfile_templates', default='templates_2D', type='string', help='pass name of output file to save 2D histograms (charge is automatically appended before extension). No need to specify extension, .root is automatically addedx')
    (options, args) = parser.parse_args()
    if len(args) < 2:
        parser.print_usage()
        quit()
    channel = args[1]
    
    outname = options.outdir
    if not os.path.exists(outname):
        os.system("mkdir -p "+outname)
        if os.path.exists("/afs/cern.ch"): os.system("cp /afs/cern.ch/user/g/gpetrucc/php/index.php "+outname)

    for charge in ['plus','minus']:
        shapesfile = "{indir}/W{flav}_{ch}_shapes.root".format(indir=args[0],flav=channel,ch=charge)
        infile = ROOT.TFile(shapesfile, 'read')
        print ""
        print "==> RUNNING FOR CHARGE ",charge

        outfile_templates = options.outfile_templates
        if outfile_templates.endswith(".root"):
            outfile_templates = outfile_templates.replace(".root","_%s.root" % str(charge))
        else:
            outfile_templates = outfile_templates + "_" + str(charge) + ".root"

        full_outfileName = outname + "/" + outfile_templates
        outfile = ROOT.TFile(full_outfileName, 'recreate')
        print "Will save 2D templates in file --> " + full_outfileName

        # doing signal
        for pol in ['right', 'left']:
            print "\tPOLARIZATION ",pol
            for ybin in range(13): 

                jobsdir = args[0]+'/jobs/'
                jobfile_name = 'W{ch}_{flav}_Ybin_{b}.sh'.format(ch=charge,flav=channel,b=ybin)
                tmp_jobfile = open(jobsdir+jobfile_name, 'r')
                tmp_line = tmp_jobfile.readlines()[-1].split()
                ymin = list(i for i in tmp_line if '(genw_y)>' in i)[0].replace('\'','').split('>')[-1]
                ymax = list(i for i in tmp_line if '(genw_y)<' in i)[0].replace('\'','').split('<')[-1]
                
                binning = getbinning(tmp_line)

                chs = '+' if charge == 'plus' else '-' 
                h1_1 = infile.Get('x_W{ch}_{pol}_W{ch}_{flav}_Ybin_{ybin}'.format(ch=charge,pol=pol,flav=channel,ybin=ybin))
                name2D = 'W{ch}_{pol}_W{ch}_{flav}_Ybin_{ybin}'.format(ch=charge,pol=pol,flav=channel,ybin=ybin)
                title2D = 'W{ch} {pol} : |Y_{{W}}| #in [{ymin},{ymax}]'.format(ymin=ymin,ymax=ymax,pol=pol,ybin=ybin,ch=chs)
                h2_backrolled_1 = dressed2D(h1_1,binning,name2D,title2D)
                canv = ROOT.TCanvas()
                h2_backrolled_1.Draw('colz')
                h2_backrolled_1.Write(name2D)
                if not options.noplot:
                    for ext in ['pdf', 'png']:
                        canv.SaveAs('{odir}/W{ch}_{pol}_W{ch}_{flav}_Ybin_{ybin}_PFMT40_absY.{ext}'.format(odir=outname,ch=charge,flav=channel,pol=pol,ybin=ybin,ext=ext))

        # do backgrounds now
        procs=["Flips","Z","Top","DiBosons","TauDecaysW","data_fakes","W{ch}_long".format(ch=charge)]
        titles=["charge flips","DY","Top","di-bosons","W#to#tau#nu","QCD","W{ch}_long".format(ch=charge)]
        for i,p in enumerate(procs):
            h1_1 = infile.Get('x_{p}'.format(p=p))
            if not h1_1: continue # muons don't have Flips components
            h2_backrolled_1 = dressed2D(h1_1,binning,p,titles[i])
            canv = ROOT.TCanvas()
            h2_backrolled_1.Draw('colz')
            h2_backrolled_1.Write(str(p))
            if not options.noplot:
                for ext in ['pdf', 'png']:
                    canv.SaveAs('{odir}/{proc}_{ch}_{flav}_PFMT40_absY.{ext}'.format(odir=outname,proc=p,ch=charge,flav=channel,ext=ext))
            
        outfile.Close()

    ## canv.Divide(1,2)
    ## canv.cd(1)
    ## h2.Draw('colz')
    ## canv.cd(2)
    ## h2backrolled.Draw('colz')
