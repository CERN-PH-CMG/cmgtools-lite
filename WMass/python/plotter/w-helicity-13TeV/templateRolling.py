#!/usr/bin/env python

# USAGE: python w-helicity-13TeV/templateRolling.py testMergeW_goodSyst/ -o plots/diffXsec/templates/fromEmanuele/  -c el -p _addInclW -b [-2.5,-2.3,-2.1,-1.9,-1.7,-1.566,-1.4442,-1.3,-1.2,-1.1,-1.0,-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.1,1.2,1.3,1.4442,1.566,1.7,1.9,2.1,2.3,2.5]*[30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45]

# will implement taking 2D template binning from a file


import ROOT, os
from array import array
from make_diff_xsec_cards import getArrayParsingString

import sys
sys.path.append(os.environ['CMSSW_BASE']+"/src/CMGTools/WMass/python/plotter/")
from plotUtils.utility import *

# def getbinning(splitline):
#     bins = splitline[5]
#     if '*' in bins:
#         etabins = list( float(i) for i in bins.replace(' ','').split('*')[0].replace('\'[','').replace(']','').split(',') )
#         ptbins  = list( float(i) for i in bins.replace(' ','').split('*')[1].replace('[','').replace(']\'','').split(',') )
#         nbinseta = len(etabins)-1
#         nbinspt  = len( ptbins)-1
#         binning = [nbinseta, etabins, nbinspt, ptbins]
#     else:
#         bins = bins.replace('\'','')
#         nbinseta = int( bins.split(',')[0] )
#         nbinspt  = int( bins.split(',')[3] )
#         etamin   = float( bins.split(',')[1] )
#         etamax   = float( bins.split(',')[2] )
#         ptmin    = float( bins.split(',')[4] )
#         ptmax    = float( bins.split(',')[5] )
#         binning = [nbinseta, etamin, etamax, nbinspt, ptmin, ptmax]
#     return binning

ROOT.gStyle.SetOptStat(0)
#ROOT.gStyle.SetPadRightMargin(0.13)
ROOT.gROOT.SetBatch()

def roll1Dto2D(h1d, histo):
    for i in xrange(1,h1d.GetNbinsX()+1):
        # histogram bin is numbered starting from 1, so add 1
        xbin = (i - 1) % histo.GetNbinsX() + 1  
        ybin = (i - 1) / histo.GetNbinsX() + 1
        histo.SetBinContent(xbin,ybin,h1d.GetBinContent(i))
    return histo

def dressed2D(h1d,binning,name,title=''):
    if len(binning) == 4:
        n1 = binning[0]; bins1 = array('d', binning[1])
        n2 = binning[2]; bins2 = array('d', binning[3])
        h2_1 = ROOT.TH2F(name, title, n1, bins1, n2, bins2 )
    else:
        n1 = binning[0]; min1 = binning[1]; max1 = binning[2]
        n2 = binning[3]; min2 = binning[4]; max2 = binning[5]
        h2_1 = ROOT.TH2F(name, title, n1, min1, max1, n2, min2, max2)
    h2_backrolled_1 = roll1Dto2D(h1d, h2_1 )
    return h2_backrolled_1


if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser(usage="%prog [options] shapesdir")
    parser.add_option('-o','--outdir', dest='outdir', default='.', type='string', help='output directory to save things')
    parser.add_option('-c','--channel', dest='channel', default='el', type='string', help='Channel (el, mu)')
    parser.add_option('-p','--postfix', dest='postfix', default='', type='string', help='Postfix for input file with shapes (e.g: "_addInclW" in "Wel_plus_shapes_addInclW.root"). Default is ""')
    parser.add_option('-b','--etaPtbinning', dest='etaPtbinning', default='[-2.5,-1.566,-1.4442,0,1.4442,1.566,2.5]*[30,35,40,45]', type='string', help='eta-pt binning for templates (will have to implement reading it from file)')
    parser.add_option(     '--noplot', dest="noplot", default=False, action='store_true', help="Do not plot templates (but you can still save them in a root file with option -s)");
    parser.add_option('-s','--save', dest='outfile_templates', default='templates_2D', type='string', help='pass name of output file to save 2D histograms (charge is automatically appended before extension). No need to specify extension, .root is automatically added')
    (options, args) = parser.parse_args()

    if len(args) < 1:
        parser.print_usage()
        quit()

    channel = options.channel
    if channel not in ["el","mu"]:
        print "Error: unknown channel %s (select 'el' or 'mu')" % channel
        quit()
        
    outname = options.outdir
    addStringToEnd(outname,"/",notAddIfEndswithMatch=True)
    createPlotDirAndCopyPhp(outname)

    etabinning = options.etaPtbinning.split('*')[0]    # this is like [a,b,c,...], and is of type string. We nedd to get an array  
    ptbinning  = options.etaPtbinning.split('*')[1]
    etabinning = getArrayParsingString(etabinning,makeFloat=True)
    ptbinning  = getArrayParsingString(ptbinning,makeFloat=True)
    binning = [len(etabinning)-1, etabinning, len(ptbinning)-1, ptbinning] 

    for charge in ['plus','minus']:
        shapesfile = "{indir}/W{flav}_{ch}_shapes{pf}.root".format(indir=args[0],flav=channel,ch=charge,pf=options.postfix)
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

        chs = '+' if charge == 'plus' else '-' 

        # doing signal
        # for pol in ['right', 'left']:
        #     print "\tPOLARIZATION ",pol
        #     for ybin in range(13): 

        #         jobsdir = args[0]+'/jobs/'
        #         jobfile_name = 'W{ch}_{flav}_Ybin_{b}.sh'.format(ch=charge,flav=channel,b=ybin)
        #         tmp_jobfile = open(jobsdir+jobfile_name, 'r')
        #         tmp_line = tmp_jobfile.readlines()[-1].split()
        #         ymin = list(i for i in tmp_line if '(genw_y)>' in i)[0].replace('\'','').split('>')[-1]
        #         ymax = list(i for i in tmp_line if '(genw_y)<' in i)[0].replace('\'','').split('<')[-1]
                
        #         binning = getbinning(tmp_line)

        #         h1_1 = infile.Get('x_W{ch}_{pol}_W{ch}_{flav}_Ybin_{ybin}'.format(ch=charge,pol=pol,flav=channel,ybin=ybin))
        #         name2D = 'W{ch}_{pol}_W{ch}_{flav}_Ybin_{ybin}'.format(ch=charge,pol=pol,flav=channel,ybin=ybin)
        #         title2D = 'W{ch} {pol} : |Y_{{W}}| #in [{ymin},{ymax}]'.format(ymin=ymin,ymax=ymax,pol=pol,ybin=ybin,ch=chs)
        #         h2_backrolled_1 = dressed2D(h1_1,binning,name2D,title2D)
        #         canv = ROOT.TCanvas()
        #         h2_backrolled_1.Draw('colz')
        #         h2_backrolled_1.Write(name2D)
        #         if not options.noplot:
        #             for ext in ['pdf', 'png']:
        #                 canv.SaveAs('{odir}/W{ch}_{pol}_W{ch}_{flav}_Ybin_{ybin}_PFMT40_absY.{ext}'.format(odir=outname,ch=charge,flav=channel,pol=pol,ybin=ybin,ext=ext))

        # do backgrounds and inclusive signal
        signalTitle = "W^{%s}#rightarrow%s#nu" % (chs, "e" if channel == "el" else "#mu")
        procs=["Flips","Z","Top","DiBosons","TauDecaysW","data_fakes","W{ch}_{flav}".format(ch=charge,flav=channel)]
        titles=["charge flips","DY","Top","di-bosons","W#rightarrow#tau#nu","QCD", signalTitle]
        lepton = "electron" if channel == "el" else " muon"
        adjustSettings_CMS_lumi()

        for i,p in enumerate(procs):
            h1_1 = infile.Get('x_{p}'.format(p=p))
            if not h1_1: continue # muons don't have Flips components
            h2_backrolled_1 = dressed2D(h1_1,binning,p,titles[i])
            h2_backrolled_1.Write(str(p))
            
            xaxisTitle = '%s #eta' % lepton
            yaxisTitle = '%s p_{T} [GeV]' % lepton
            zaxisTitle = "Events::0,%.1f" % h2_backrolled_1.GetMaximum()

            if not options.noplot:
                drawCorrelationPlot(h2_backrolled_1, 
                                    xaxisTitle, yaxisTitle, zaxisTitle, 
                                    '{proc}_{ch}_{flav}'.format(proc=p,ch=charge,flav=channel),
                                    "",outname,1,1,False,False,False,1)

            # canv = ROOT.TCanvas()
            # h2_backrolled_1.Draw('colz')
            # if not options.noplot:
            #     for ext in ['pdf', 'png']:
            #         canv.SaveAs('{odir}/{proc}_{ch}_{flav}.{ext}'.format(odir=outname,proc=p,ch=charge,flav=channel,ext=ext))
            
        outfile.Close()

    ## canv.Divide(1,2)
    ## canv.cd(1)
    ## h2.Draw('colz')
    ## canv.cd(2)
    ## h2backrolled.Draw('colz')
