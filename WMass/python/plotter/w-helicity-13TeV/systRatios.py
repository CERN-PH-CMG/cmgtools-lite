import ROOT, os, copy
from array import array
from testRolling import getbinning,roll1Dto2D,unroll2Dto1D,dressed2D

ROOT.gROOT.SetBatch()

canv = ROOT.TCanvas()

if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser(usage="%prog [options] shapesdir channel")
    parser.add_option('-o','--outdir', dest='outdir', default='.', type='string', help='outdput directory to save the matrix')
    parser.add_option('-s','--syst', dest='systematics', default=None, type='string', help='systematics of which drawing the ratio (comma-separated list of regex')
    (options, args) = parser.parse_args()
    channel = args[1]

    systs = [] if not options.systematics else options.systematics.split(',')
    print "Will consider these possible systematics: ",systs

    outname = options.outdir
    if not os.path.exists(outname):
        os.system("mkdir -p "+outname)
        if os.path.exists("/afs/cern.ch"): os.system("cp /afs/cern.ch/user/g/gpetrucc/php/index.php "+outname)

    for charge in ['minus','plus']:
        print "===> RUNNING CHARGE = ",charge
        chs = '+' if charge == 'plus' else '-'
        shapesfile = "{indir}/W{flav}_{ch}_shapes.root".format(indir=args[0],flav=channel,ch=charge)
        infile = ROOT.TFile(shapesfile, 'read')
        keylist = infile.GetListOfKeys()
        siglist = list( i.GetName() for i in keylist if 'Ybin_' in i.GetName() )
        nY = max( int(i.split('_')[-2]) for i in siglist if 'pdf' in i)
        nPDF = max( int(i.split('_')[-1].replace('pdf','').replace('Down','').replace('Up','')) for i in siglist if 'pdf' in i)

        bkgs = ['data_fakes','Flips','DiBosons','Top','TauDecaysW','Z','W%s_long'%charge] # other than W_{L,R}
        wlr = ['W{ch}_{p}_W{ch}_{flav}_Ybin_{i}'.format(ch=charge,p=pol,flav=channel,i=iy) for pol in ['left','right'] for iy in xrange(nY+1)]
        procs=wlr+bkgs

        jobsdir = args[0]+'/jobs/'
        jobfile_name = 'W{ch}_{flav}_Ybin_0.sh'.format(ch=charge,flav=channel)
        tmp_jobfile = open(jobsdir+jobfile_name, 'r')
        tmp_line = tmp_jobfile.readlines()[-1].replace(', ',',').split()
        binning = getbinning(tmp_line)

        ratios={}
        if any('pdf' in syst for syst in systs):
            for pol in ['right', 'left']:
                print "\tPOLARIZATION ",pol
                histo_central = infile.Get('x_W{ch}_{pol}_W{ch}_{flav}_Ybin_0'.format(ch=charge,pol=pol,flav=channel))
                for iy in xrange(1,nY+1):
                    histo_central.Add(infile.Get('x_W{ch}_{pol}_W{ch}_{flav}_Ybin_{i}'.format(ch=charge,pol=pol,flav=channel,i=iy)))
                for ip in xrange(1,nPDF+1):
                    histo_pdfi = infile.Get('x_W{ch}_{pol}_W{ch}_{flav}_Ybin_0_pdf{ip}Up'.format(ch=charge,pol=pol,flav=channel,ip=ip))
                    for iy in xrange(1,nY+1):
                        histo_pdfi_iy = infile.Get('x_W{ch}_{pol}_W{ch}_{flav}_Ybin_{iy}_pdf{ip}Up'.format(ch=charge,pol=pol,flav=channel,iy=iy,ip=ip))
                        if histo_pdfi_iy: histo_pdfi.Add(histo_pdfi_iy)
                    ratio_pdfi = copy.deepcopy(histo_pdfi)
                    ratio_pdfi.Divide(histo_central)
             
                    for ib in xrange(1, ratio_pdfi.GetNbinsX()+1):
                        ratio_pdfi.SetBinContent(ib, abs(1.-ratio_pdfi.GetBinContent(ib) if histo_central.GetBinContent(ib)>0 else 0))
             
                    title2D = 'W{ch} {pol} : pdf {ip}'.format(ip=ip,pol=pol,ch=chs)
                    h2_backrolled_1 = dressed2D(ratio_pdfi,binning,title2D)
                    h2_backrolled_1.GetZaxis().SetRangeUser(0.,0.02)
                    ratios['syst_W{ch}_{pol}_W{ch}_{flav}_pdf{ip}'.format(ch=charge,pol=pol,flav=channel,ip=ip)] = h2_backrolled_1
        else:
            for proc in procs:
                histo_central = infile.Get('x_%s'%proc)
                for syst in systs:
                    # use just Up if you expect the syst ~symmetric
                    fullsyst = syst if any(sfx in syst for sfx in ['Up','Down']) else syst+"Up"
                    k_syst = 'x_{proc}_{syst}'.format(proc=proc,syst=fullsyst)
                    fulllist = list(i.GetName() for i in keylist)
                    if k_syst in fulllist:
                        print "Found ",k_syst, " in the histograms..."
                        h_syst = infile.Get(k_syst)
                        ratio = copy.deepcopy(h_syst)
                        ratio.Divide(histo_central)
                        for ib in xrange(1, ratio.GetNbinsX()+1):
                            ratio.SetBinContent(ib, abs(1.-ratio.GetBinContent(ib) if histo_central.GetBinContent(ib)>0 else 0))
                        title2D = '{proc} : variation={syst}'.format(proc=proc,syst=syst)
                        h2_backrolled_1 = dressed2D(ratio,binning,title2D)
                        h2_backrolled_1.GetZaxis().SetRangeUser(0.,0.50)
                        ratios['syst_{proc}_{ch}_{flav}_{syst}'.format(proc=proc,ch=charge,flav=channel,syst=syst)] = h2_backrolled_1
        print ratios
        canv = ROOT.TCanvas()
        for k,r in ratios.iteritems():
            r.Draw('colz')
            for ext in ['pdf', 'png']:
                canv.SaveAs('{odir}/{name}.{ext}'.format(odir=outname,name=k,ext=ext))
