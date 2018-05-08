#!/usr/bin/env python
# USAGE: 
# PDFs: python systRatios.py -o plots -s 'pdf' cards_el el
# OTHER SYSTEMATICS: python systRatios.py -o plots -s 'muR,muF,muRmuF,alphaS,wptSlope' cards_el el

import ROOT, os, copy, re
from array import array
from testRolling import getbinning,roll1Dto2D,unroll2Dto1D,dressed2D

ROOT.gROOT.SetBatch()
ROOT.gStyle.SetPalette(55)
ROOT.gErrorIgnoreLevel = 100

canv = ROOT.TCanvas()

if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser(usage="%prog [options] shapesdir channel")
    parser.add_option('-o','--outdir', dest='outdir', default='.', type='string', help='outdput directory to save the matrix')
    parser.add_option('-s','--syst', dest='systematics', default=None, type='string', help='systematics of which drawing the ratio (comma-separated list of)')
    (options, args) = parser.parse_args()
    channel = args[1]

    systs = [] if not options.systematics else options.systematics.split(',')
    print "Will consider these possible systematics: ",systs

    outname = options.outdir
    if not os.path.exists(outname):
        os.system("mkdir -p "+outname)
        if os.path.exists("/afs/cern.ch"): os.system("cp /afs/cern.ch/user/g/gpetrucc/php/index.php "+outname)

    nY = {}
    errors = []
    for charge in ['minus','plus']:
        print "===> RUNNING CHARGE = ",charge
        chs = '+' if charge == 'plus' else '-'
        shapesfile = "{indir}/W{flav}_{ch}_shapes.root".format(indir=args[0],flav=channel,ch=charge)
        infile = ROOT.TFile(shapesfile, 'read')
        keylist = infile.GetListOfKeys()
        siglist = list( i.GetName() for i in keylist if 'Ybin_' in i.GetName() )
        fulllist = list(i.GetName() for i in keylist)
        nY[charge+'_left']  = max( int(i.split('_')[-2]) for i in siglist if 'pdf' in i and 'left'  in i)
        nY[charge+'_right'] = max( int(i.split('_')[-2]) for i in siglist if 'pdf' in i and 'right' in i)
        nPDF = max( int(i.split('_')[-1].replace('pdf','').replace('Down','').replace('Up','')) for i in siglist if 'pdf' in i)

        bkgs = ['data_fakes','Flips','DiBosons','Top','TauDecaysW','Z','W%s_long'%charge] # other than W_{L,R}
        wlr = ['W{ch}_{p}_W{ch}_{p}_{flav}_Ybin_{i}'.format(ch=charge,p=pol,flav=channel,i=iy) for pol in ['left','right'] for iy in xrange(nY[charge+'_'+pol]+1)]
        procs=wlr+bkgs

        jobsdir = args[0]+'/jobs/'
        jobfile_name = 'W{ch}_left_{flav}_Ybin_0.sh'.format(ch=charge,flav=channel)
        tmp_jobfile = open(jobsdir+jobfile_name, 'r')
        tmp_line = tmp_jobfile.readlines()[-1].replace(', ',',').split()
        binning = getbinning(tmp_line)

        ratios={}
        for proc in procs:
            print "Making syst plots for process : ",proc," ..."
            # central template
            if 'W{ch}'.format(ch=charge) in proc:
                for pol in ['right', 'left']:
                    cp = charge+'_'+pol
                    histo_central = infile.Get('x_W{ch}_{pol}_W{ch}_{pol}_{flav}_Ybin_0'.format(ch=charge,pol=pol,flav=channel))
                    for iy in xrange(1,nY[cp]+1):
                        histo_central.Add(infile.Get('x_W{ch}_{pol}_W{ch}_{pol}_{flav}_Ybin_{i}'.format(ch=charge,pol=pol,flav=channel,i=iy)))
            else:
                histo_central = infile.Get('x_%s'%proc)
            # systematic templates
            for syst in systs:
                if 'pdf' in syst: # generic pdf means looping over all 60 Hessian variations
                    if not re.match('W{ch}|Z'.format(ch=charge),proc): continue # only W and Z have PDF variations
                    for ip in xrange(1,nPDF+1):
                        if 'W{ch}'.format(ch=charge) in proc:
                            for pol in ['right', 'left']:
                                cp = charge+'_'+pol
                                histo_pdfi = infile.Get('x_W{ch}_{pol}_W{ch}_{pol}_{flav}_Ybin_0_pdf{ip}Up'.format(ch=charge,pol=pol,flav=channel,ip=ip))
                                for iy in xrange(1,nY[cp]+1):
                                    histo_pdfi_iy = infile.Get('x_W{ch}_{pol}_W{ch}_{pol}_{flav}_Ybin_{iy}_pdf{ip}Up'.format(ch=charge,pol=pol,flav=channel,iy=iy,ip=ip))
                                    if histo_pdfi_iy: histo_pdfi.Add(histo_pdfi_iy)
                                title2D = 'W{ch} {pol} : pdf {ip}'.format(ip=ip,pol=pol,ch=chs)
                                key = 'syst_W{ch}_{pol}_W{ch}_{pol}_{flav}_pdf{ip}'.format(ch=charge,pol=pol,flav=channel,ip=ip)
                        else:
                            histo_pdfi = infile.Get('x_{proc}_pdf{ip}Up'.format(proc=proc,ip=ip))
                            title2D = 'Z : pdf {ip}'.format(ip=ip)
                            key = 'syst_{proc}_{ch}_{flav}_pdf{ip}'.format(proc=proc,ch=charge,flav=channel,ip=ip)
                        if not histo_central.GetEntries() == histo_pdfi.GetEntries():
                            print 'WARNING/ERROR: THE CENTRAL HISTO AND PDF HISTO DO NOT HAVE THE SAME NUMBER OF ENTRIES'
                            print 'this just happened for {ch} and {pol} and pdf {syst}'.format(ch=charge, pol=pol, syst=ip)
                            errors.append('{ch}_{pol}_pdf{syst}'.format(ch=charge, pol=pol, syst=ip))
                        ratio_pdfi = copy.deepcopy(histo_pdfi)
                        ratio_pdfi.Divide(histo_central)
                        for ib in xrange(1, ratio_pdfi.GetNbinsX()+1):
                            ##ratio_pdfi.SetBinContent(ib, abs(1.-ratio_pdfi.GetBinContent(ib) if histo_central.GetBinContent(ib)>0 else 0))
                            ratio_pdfi.SetBinContent(ib, 1.-ratio_pdfi.GetBinContent(ib) if histo_central.GetBinContent(ib)>0 else 0)
                        h2_backrolled_1 = dressed2D(ratio_pdfi,binning,title2D)
                        h2_backrolled_1.GetZaxis().SetRangeUser(-0.02,0.02)
                        ratios[key] = h2_backrolled_1
                else:
                    histo_syst = None
                    fullsyst = syst if any(sfx in syst for sfx in ['Up','Down']) else syst+"Up"
                    if 'W{ch}'.format(ch=charge) in proc:
                        for pol in ['right', 'left']:
                            cp = charge+'_'+pol
                            hname = 'x_W{ch}_{pol}_W{ch}_{pol}_{flav}_Ybin_0_{syst}'.format(ch=charge,pol=pol,flav=channel,syst=fullsyst)
                            histo_syst = infile.Get(hname) if hname in keylist else None
                            for iy in xrange(1,nY[cp]+1):
                                hname_iy = 'x_W{ch}_{pol}_W{ch}_{pol}_{flav}_Ybin_{iy}_{syst}'.format(ch=charge,pol=pol,flav=channel,iy=iy,syst=fullsyst)
                                histo_syst_iy = infile.Get(hname_iy) if hname in keylist else None
                                if histo_syst_iy: histo_syst.Add(histo_syst_iy)
                            title2D = 'W{ch} {pol} : variation={syst}'.format(pol=pol,ch=chs,syst=syst)
                            key = 'syst_W{ch}_{pol}_W{ch}_{pol}_{flav}_{syst}'.format(ch=charge,pol=pol,flav=channel,syst=syst)
                    else:
                        hname = 'x_{proc}_{syst}'.format(proc=proc,syst=fullsyst)
                        if hname in fulllist:
                            histo_syst = infile.Get(hname)
                        title2D = '{proc} : variation={syst}'.format(proc=proc,syst=syst)
                        key = 'syst_{proc}_{ch}_{flav}_{syst}'.format(proc=proc,ch=charge,flav=channel,syst=syst)
                    if histo_syst:
                        ratio = copy.deepcopy(histo_syst)
                        ratio.Divide(histo_central)
                        for ib in xrange(1, ratio.GetNbinsX()+1):
                            ratio.SetBinContent(ib, abs(1.-ratio.GetBinContent(ib) if histo_central.GetBinContent(ib)>0 else 0))
                        h2_backrolled_1 = dressed2D(ratio,binning,title2D)
                        hmax = 0.05 if 'muF' in syst else 0.02
                        h2_backrolled_1.GetZaxis().SetRangeUser(0.,hmax)
                        ratios[key] = h2_backrolled_1

        print ratios
        canv = ROOT.TCanvas()
        for k,r in ratios.iteritems():
            r.Draw('colz')
            for ext in ['pdf', 'png']:
                canv.SaveAs('{odir}/{name}.{ext}'.format(odir=outname,name=k,ext=ext))

    print 'ERRORS FOUND IN THESE SYSTEAMTICS'
    for err in errors:
        print err
