#!/usr/bin/env python
from shutil import copyfile
import re, sys, os, os.path, subprocess
import numpy as np
# import some parameters from wmass_parameters.py, they are also used by other scripts
from wmass_parameters import *

NPDFSYSTS=53 # for CT10

def writePdfSystsToMCA(sample,syst,dataset,xsec,vec_weight,filename):
    mcafile = open(filename, "a")
    for i in range(1,NPDFSYSTS):
        pdfvar=str((i-1)/2+1)
        direction="Up" if i%2 else "Dn"
        mcafile.write(sample+"_"+str(syst)+pdfvar+"_"+direction+"+   : "+dataset+" :  "+str(xsec)+" : "+vec_weight+"["+str(i)+"]/"+vec_weight+"[0]; SkipMe=True \n")
    print "written ",vec_weight," systematics into ",filename

def writePdfSystsToSystFile(sample,syst,channel,filename):
    systfile=open(filename,"a")
    for i in range(NPDFSYSTS/2):
        systfile.write(channel+"_pdf"+str(i+1)+"  : "+sample+" : .* : pdf"+str(i+1)+" : templates\n")
    print "written pdf syst configuration to ",filename
        
from optparse import OptionParser
parser = OptionParser(usage="%prog [options] mc.txt cuts.txt var bins systs.txt outdir ")
parser.add_option("-q", "--queue",    dest="queue",     type="string", default=None, help="Run jobs on lxbatch instead of locally");
parser.add_option("--dry-run", dest="dryRun",    action="store_true", default=False, help="Do not run the job, only print the command");
parser.add_option("-s", "--signal-cards",  dest="signalCards",  action="store_true", default=False, help="Make the signal part of the datacards");
parser.add_option("-b", "--bkgdata-cards", dest="bkgdataCards", action="store_true", default=False, help="Make the background and data part of the datacards");
parser.add_option("-W", "--weight", dest="weightExpr", default="-W 1", help="Event weight expression (default 1)");
parser.add_option("-P", "--path", dest="path", type="string",default=None, help="Path to directory with input trees and pickle files");
parser.add_option("--not-unroll2D", dest="notUnroll2D", action="store_true", default=False, help="Do not unroll the TH2Ds in TH1Ds needed for combine (to make 2D plots)");
(options, args) = parser.parse_args()

if len(sys.argv) < 6:
    parser.print_usage()
    quit()


FASTTEST=''
#FASTTEST='--max-entries 1000 '
T=options.path
print "used trees from: ",T
J=4
MCA = args[0]
CUTFILE = args[1]
fitvar = args[2]
binning = args[3]
SYSTFILE = args[4]

if not os.path.exists("cards/"):
    os.makedirs("cards/")
outdir="cards/"+args[5]

#FIXME: for the moment avoid this part, need to understand which weight to use
# write systematic variations to be considered in the MCA file
MCASYSTS=('.').join(MCA.split('.')[:-1])+"-systs.txt"
copyfile(MCA,MCASYSTS)
#writePdfSystsToMCA("W","pdf","WJets",61526.7,"LHEweight_wgt",MCASYSTS)

# write the complete systematics file
SYSTFILEALL=('.').join(SYSTFILE.split('.')[:-1])+"-all.txt"
copyfile(SYSTFILE,SYSTFILEALL)
#writePdfSystsToSystFile("W","pdf","CMS_We",SYSTFILEALL)

ARGS=" ".join([MCASYSTS,CUTFILE,"'"+fitvar+"' "+"'"+binning+"'",SYSTFILEALL])
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

if not os.path.exists(outdir): os.mkdir(outdir)
if options.queue and not os.path.exists(outdir+"/jobs"): os.mkdir(outdir+"/jobs")

POSCUT=" -A alwaystrue positive 'LepGood1_charge>0' "
NEGCUT=" -A alwaystrue negative 'LepGood1_charge<0' "
if options.signalCards:
    WYBins=(16,-6,6)
    bWidth=(WYBins[2]-WYBins[1])/float(WYBins[0])
    WYBinsEdges=np.arange(WYBins[1],WYBins[2]+0.001,bWidth)
    print "MAKING SIGNAL PART: WYBinsEdges = ",WYBinsEdges
    for charge in ['p','m']:
        for iy in xrange(len(WYBinsEdges)-1):
            print "Making card for %s<genw_y<%s and signal process with charge %s " % (WYBinsEdges[iy],WYBinsEdges[iy+1],charge)
            ycut=" -A alwaystrue YW%d 'genw_y>%s && genw_y<%s' " % (iy,WYBinsEdges[iy],WYBinsEdges[iy+1])
            ycut += POSCUT if charge=='p' else NEGCUT
            xpsel=' --xp "W%s.*,Z,Top,DiBosons,TauDecaysW,data.*" --asimov ' % ('p' if charge=='m' else 'm')
            if not os.path.exists(outdir): os.mkdir(outdir)
            if options.queue and not os.path.exists(outdir+"/jobs"): os.mkdir(outdir+"/jobs")
            dcname = "W%s_el_Ybin_%d" % (charge,iy)
            BIN_OPTS=OPTIONS + " -W '" + options.weightExpr + "'" + " -o "+dcname+" --od "+outdir + xpsel + ycut
            if options.queue:
                srcfile=outdir+"/jobs/"+dcname+".sh"
                logfile=outdir+"/jobs/"+dcname+".log"
                srcfile_op = open(srcfile,"w")
                srcfile_op.write("#! /bin/sh\n")
                srcfile_op.write("cd {cmssw};\neval $(scramv1 runtime -sh);\ncd {dir};\n".format( 
                        dir = os.getcwd(), cmssw = os.environ['CMSSW_BASE']))
                srcfile_op.write("python {dir}/makeShapeCards.py {args} \n".format(
                        dir = os.getcwd(), args = ARGS+" "+BIN_OPTS))
                os.system("chmod a+x "+srcfile)
                cmd = "bsub -q {queue} -o {dir}/{logfile} {dir}/{srcfile}\n".format(
                    queue=options.queue, dir=os.getcwd(), logfile=logfile, srcfile=srcfile)
                if options.dryRun: print cmd
                else: os.system(cmd)
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

if options.bkgdataCards:
    print "MAKING BKG and DATA PART:\n"
    for charge in ['p','m']:
        xpsel=' --xp "W.*" '
        chargecut = POSCUT if charge=='p' else NEGCUT
        dcname = "bkg_plus_data_el_%s" % charge
        BIN_OPTS=OPTIONS + " -W '" + options.weightExpr + "'" + " -o "+dcname+" --od "+outdir + xpsel + chargecut
        if options.queue:
            srcfile=outdir+"/jobs/"+dcname+".sh"
            logfile=outdir+"/jobs/"+dcname+".log"
            srcfile_op = open(srcfile,"w")
            srcfile_op.write("#! /bin/sh\n")
            srcfile_op.write("cd {cmssw};\neval $(scramv1 runtime -sh);\ncd {dir};\n".format( 
                    dir = os.getcwd(), cmssw = os.environ['CMSSW_BASE']))
            srcfile_op.write("python {dir}/makeShapeCards.py {args} \n".format(
                    dir = os.getcwd(), args = ARGS+" "+BIN_OPTS))
            os.system("chmod a+x "+srcfile)
            cmd = "bsub -q {queue} -o {dir}/{logfile} {dir}/{srcfile}\n".format(
                queue=options.queue, dir=os.getcwd(), logfile=logfile, srcfile=srcfile)
            if options.dryRun: print cmd
            else: os.system(cmd)
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
