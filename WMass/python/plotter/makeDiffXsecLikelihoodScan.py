#!/usr/bin/env python

# python makeDiffXsecLikelihoodScan.py diffXsecFit_testScalLikelihood_freezeShapeNuis/ -o plots/diffXsec/likelihoodScan/ -f el -c plus


from shutil import copyfile
import re, sys, os, os.path, subprocess, json, ROOT
import numpy as np

from w_helicity_13TeV.make_diff_xsec_cards import getXYBinsFromGlobalBin
from w_helicity_13TeV.make_diff_xsec_cards import getGlobalBin

if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser(usage="%prog [options] higgsCombineFolder")
    parser.add_option('-o','--outdir', dest='outdir', default='./', type='string', help='output directory')
    parser.add_option("-f", "--flavour", dest="flavour", type="string", default='el', help="Channel: either 'el' or 'mu'");
    parser.add_option("-c", "--charge", dest="charge", type="string", default='plus', help="Charge: either 'plus' or 'minus'");
    (options, args) = parser.parse_args()

    if len(args) < 1:
        parser.print_usage()
        quit()
 
    charge = options.charge
    flavour = options.flavour
    outdir = options.outdir
    if not outdir.endswith('/'): outdir += "/"    
    if outdir != "./":
        if not os.path.exists(outdir):
            print "Creating folder", outdir
            os.system("mkdir -p " + outdir)

    inputdir = args[0]
    if not inputdir.endswith('/'): inputdir += "/"    



    #files = [ f for f in os.listdir(inputdir) if f.endswith('.root') and f.startswith('higgsCombine')]
    #files = list( [os.path.join(inputdir, f) for f in files] ) 
    files = inputdir + ""


    
