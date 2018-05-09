#!/usr/bin/env python
from shutil import copyfile
import re, sys, os, os.path, subprocess, json, ROOT
import numpy as np
# import some parameters from wmass_parameters.py, they are also used by other scripts
from wmass_parameters import *

from make_helicity_cards.py import intermediateBinning, makeYWBinning, getMcaIncl, writePdfSystsToMCA, writeQCDScaleSystsToMCA, writePdfSystsToSystFile, submitBatch

NPDFSYSTS=60 # Hessian variations of NNPDF 3.0
pdfsysts=[] # array containing the PDFs signal variations
qcdsysts=[] # array containing the QCD scale signal variations

from optparse import OptionParser
parser = OptionParser(usage="%prog [options] mc.txt cuts.txt var bins systs.txt outdir ")
parser.add_option("-q", "--queue",    dest="queue",     type="string", default=None, help="Run jobs on lxbatch instead of locally");
parser.add_option("--dry-run", dest="dryRun",    action="store_true", default=False, help="Do not run the job, only print the command");
parser.add_option("--long-bkg", dest="longBkg",    action="store_true", default=False, help="Treat the longitudinal polarization as one background template.");
parser.add_option("-s", "--signal-cards",  dest="signalCards",  action="store_true", default=False, help="Make the signal part of the datacards");
parser.add_option("-b", "--bkgdata-cards", dest="bkgdataCards", action="store_true", default=False, help="Make the background and data part of the datacards");
parser.add_option("-W", "--weight", dest="weightExpr", default="-W 1", help="Event weight expression (default 1)");
parser.add_option("-P", "--path", dest="path", type="string",default=None, help="Path to directory with input trees and pickle files");
parser.add_option("-C", "--channel", dest="channel", type="string", default='el', help="Channel. either 'el' or 'mu'");
parser.add_option("--not-unroll2D", dest="notUnroll2D", action="store_true", default=False, help="Do not unroll the TH2Ds in TH1Ds needed for combine (to make 2D plots)");
parser.add_option("--pdf-syst", dest="addPdfSyst", action="store_true", default=False, help="Add PDF systematics to the signal (need incl_sig directive in the MCA file)");
parser.add_option("--qcd-syst", dest="addQCDSyst", action="store_true", default=False, help="Add QCD scale systematics to the signal (need incl_sig directive in the MCA file)");
(options, args) = parser.parse_args()

if len(sys.argv) < 6:
    parser.print_usage()
    quit()


FASTTEST=''
#FASTTEST='--max-entries 1000 '
T=options.path
print "used trees from: ",T
J=2
MCA = args[0]
CUTFILE = args[1]
fitvar = args[2]
binning = args[3]
SYSTFILE = args[4]

if not os.path.exists("cards/"):
    os.makedirs("cards/")
outdir="cards/"+args[5]

if not os.path.exists(outdir): os.mkdir(outdir)
if options.queue and not os.path.exists(outdir+"/jobs"): 
    os.mkdir(outdir+"/jobs")
    os.mkdir(outdir+"/mca")

# copy some cfg for bookkeeping
os.system("cp %s %s" % (CUTFILE, outdir))
os.system("cp %s %s" % (MCA, outdir))

if options.addPdfSyst:
    # write the additional systematic samples in the MCA file
    writePdfSystsToMCA(MCA,outdir+"/mca") # on W + jets 
    writePdfSystsToMCA(MCA,outdir+"/mca",incl_mca='incl_dy') # on DY + jets
    # write the complete systematics file (this was needed when trying to run all systs in one job)
    # SYSTFILEALL = writePdfSystsToSystFile(SYSTFILE)
if options.addQCDSyst:
    scales = ['muR','muF',"muRmuF", "alphaS"]
    writeQCDScaleSystsToMCA(MCA,outdir+"/mca",scales=scales+["wptSlope"])
    writeQCDScaleSystsToMCA(MCA,outdir+"/mca",scales=scales,incl_mca='incl_dy')

ARGS=" ".join([MCA,CUTFILE,"'"+fitvar+"' "+"'"+binning+"'",SYSTFILE])
BASECONFIG=os.path.dirname(MCA)
if options.queue:
    ARGS = ARGS.replace(BASECONFIG,os.getcwd()+"/"+BASECONFIG)
OPTIONS=" -P "+T+" --s2v -j "+str(J)+" -l "+str(luminosity)+" -f --obj tree "+FASTTEST
if not os.path.exists(outdir): os.makedirs(outdir)
OPTIONS+=" -F Friends '{P}/friends/tree_Friend_{cname}.root' "
if not options.notUnroll2D:
    OPTIONS+=" --2d-binning-function unroll2Dto1D "

if options.queue:
    import os, sys
    basecmd = "bsub -q {queue} {dir}/lxbatch_runner.sh {dir} {cmssw} python {self}".format(
                queue = options.queue, dir = os.getcwd(), cmssw = os.environ['CMSSW_BASE'], self=sys.argv[0]
            )

POSCUT=" -A alwaystrue positive 'LepGood1_charge>0' "
NEGCUT=" -A alwaystrue negative 'LepGood1_charge<0' "
if options.signalCards:
    WYBinsEdges = makeYWBinning(os.environ['CMSSW_BASE']+'/src/CMGTools/WMass/data/efficiency/eff_el_PFMT40.root')#, 5000)
    ybinfile = open(outdir+'/binningYW.txt','w')
    ybinfile.write(json.dumps(WYBinsEdges))
    #ybinfile.writelines(' '.join(str(i) for i in WYBinsEdges))
    ybinfile.close()
    print "MAKING SIGNAL PART: WYBinsEdges = ",WYBinsEdges
    wsyst = ['']+[x for x in pdfsysts+qcdsysts if 'sig' in x]
    for ivar,var in enumerate(wsyst):
        for helicity in ['right', 'left']:
            antihel = 'right' if helicity == 'left' else 'left'
            for charge in ['plus','minus']:
                antich = 'plus' if charge == 'minus' else 'minus'
                YWbinning = WYBinsEdges['{ch}_{hel}'.format(ch=charge,hel=helicity)]
                if ivar==0: 
                    IARGS = ARGS
                else: 
                    IARGS = ARGS.replace(MCA,"{outdir}/mca/mca{syst}.txt".format(outdir=outdir,syst=var))
                    IARGS = IARGS.replace(SYSTFILE,"{outdir}/mca/systEnv-dummy.txt".format(outdir=outdir))
                    print "Running the systematic: ",var
                for iy in xrange(len(YWbinning)-1):
                    print "Making card for %s<=abs(genw_y)<%s and signal process with charge %s " % (YWbinning[iy],YWbinning[iy+1],charge)
                    ycut=" -A alwaystrue YW%d 'abs(genw_y)>=%s && abs(genw_y)<%s' " % (iy,YWbinning[iy],YWbinning[iy+1])
                    ycut += POSCUT if charge=='plus' else NEGCUT
                    excl_long_signal  = '' if not options.longBkg else ',W{ch}_long.*'.format(ch=charge)
                    xpsel=' --xp "W{antich}.*,W{ch}_{antihel}.*,Flips,Z,Top,DiBosons,TauDecaysW{longbkg},data.*" --asimov '.format(antich=antich,ch=charge,antihel=antihel,longbkg = excl_long_signal)
                    if not os.path.exists(outdir): os.mkdir(outdir)
                    if options.queue and not os.path.exists(outdir+"/jobs"): os.mkdir(outdir+"/jobs")
                    syst = '' if ivar==0 else var
                    dcname = "W{charge}_{hel}_{channel}_Ybin_{iy}{syst}".format(charge=charge, hel=helicity, channel=options.channel,iy=iy,syst=syst)
                    BIN_OPTS=OPTIONS + " -W '" + options.weightExpr + "'" + " -o "+dcname+" --od "+outdir + xpsel + ycut
                    if options.queue:
                        mkShCardsCmd = "python {dir}/makeShapeCards.py {args} \n".format(dir = os.getcwd(), args = IARGS+" "+BIN_OPTS)
                        submitBatch(dcname,outdir,mkShCardsCmd,options)
                    else:
                        cmd = "python makeShapeCards.py "+IARGS+" "+BIN_OPTS
                        if options.dryRun: print cmd
                        else:
                            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
                            out, err = p.communicate() 
                            result = out.split('\n')
                            for lin in result:
                                if not lin.startswith('#'):
                                    print(lin)

if options.bkgdataCards:
    print "MAKING BKG and DATA PART:\n"
    for charge in ['plus','minus']:
        xpsel=' --xp "W.*" ' if not options.longBkg else ' --xp "W{ch}_left,W{ch}_right,W{ach}.*" '.format(ch=charge, ach='minus' if charge=='plus' else 'plus')
        if len(pdfsysts+qcdsysts)>1: # 1 is the nominal 
            xpsel+=' --xp "Z" '
        chargecut = POSCUT if charge=='plus' else NEGCUT
        dcname = "bkg_and_data_{channel}_{charge}".format(channel=options.channel, charge=charge)
        BIN_OPTS=OPTIONS + " -W '" + options.weightExpr + "'" + " -o "+dcname+" --od "+outdir + xpsel + chargecut
        if options.queue:
            mkShCardsCmd = "python {dir}/makeShapeCards.py {args} \n".format(dir = os.getcwd(), args = ARGS+" "+BIN_OPTS)
            submitBatch(dcname,outdir,mkShCardsCmd,options)
        else:
            cmd = "python makeShapeCards.py "+ARGS+" "+BIN_OPTS
            if options.dryRun: print cmd
            else:
                p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
                out, err = p.communicate() 
                result = out.split('\n')
                for lin in result:
                    if not lin.startswith('#'):
                        print(lin)

if options.bkgdataCards and len(pdfsysts+qcdsysts)>1:
    dysyst = ['']+[x for x in pdfsysts+qcdsysts if 'dy' in x]
    for ivar,var in enumerate(dysyst):
        for charge in ['plus','minus']:
            antich = 'plus' if charge == 'minus' else 'minus'
            if ivar==0: 
                IARGS = ARGS
            else: 
                IARGS = ARGS.replace(MCA,"{outdir}/mca/mca{syst}.txt".format(outdir=outdir,syst=var))
                IARGS = IARGS.replace(SYSTFILE,"{outdir}/mca/systEnv-dummy.txt".format(outdir=outdir))
                print "Running the DY with systematic: ",var
            print "Making card for DY process with charge ", charge
            chcut = POSCUT if charge=='plus' else NEGCUT
            xpsel=' --xp "[^Z]*" --asimov '
            syst = '' if ivar==0 else var
            dcname = "Z_{channel}_{charge}{syst}".format(channel=options.channel, charge=charge,syst=syst)
            BIN_OPTS=OPTIONS + " -W '" + options.weightExpr + "'" + " -o "+dcname+" --od "+outdir + xpsel + chcut
            if options.queue:
                mkShCardsCmd = "python {dir}/makeShapeCards.py {args} \n".format(dir = os.getcwd(), args = IARGS+" "+BIN_OPTS)
                submitBatch(dcname,outdir,mkShCardsCmd,options)
            else:
                cmd = "python makeShapeCards.py "+IARGS+" "+BIN_OPTS
                if options.dryRun: print cmd
                else:
                    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
                    out, err = p.communicate() 
                    result = out.split('\n')
                    for lin in result:
                        if not lin.startswith('#'):
                            print(lin)
