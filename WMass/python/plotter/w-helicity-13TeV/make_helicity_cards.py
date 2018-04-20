#!/usr/bin/env python
from shutil import copyfile
import re, sys, os, os.path, subprocess, json, ROOT
import numpy as np
# import some parameters from wmass_parameters.py, they are also used by other scripts
from wmass_parameters import *

## infile should be the reco/gen efficiency file of the electrons
def makeYWBinning(infile, cutoff=10000):
    
    histo_file = ROOT.TFile(infile, 'READ')
    
    yw_binning = {}
    
    for ch in ['plus', 'minus']:
        for pol in ['left', 'right']:
            yw_binning['{ch}_{pol}'.format(ch=ch,pol=pol)] = [i*0.15 for i in range(11)]
            hname = 'w{ch}_wy_reco_W{ch}_{pol}'.format(ch=ch,pol=pol)
            histo = histo_file.Get(hname)
            nlast = 0.
            for ibin in reversed(range(1,histo.GetNbinsX()+1)):
                nlast += histo.GetBinContent(ibin)
                if nlast > cutoff: 
                    ilast = ibin
                    ylast = histo.GetXaxis().GetBinUpEdge(ilast)
                    yw_binning['{ch}_{pol}'.format(ch=ch,pol=pol)] += [ 1.5+i*0.25 for i in range(1,int((ylast-1.5)/0.25)+1)]
                    yw_binning['{ch}_{pol}'.format(ch=ch,pol=pol)] += [histo.GetXaxis().GetXmax()]
                    break
    
    return yw_binning


NPDFSYSTS=60 # Hessian variations of NNPDF 3.0
pdfsysts=[''] # array containing the signal variations

def writePdfSystsToMCA(mcafile,odir,vec_weight="hessWgt",syst="pdf",incl_mca='incl_sig'):
    open("%s/systEnv-dummy.txt" % odir, 'a').close()
    incl_file=''
    mcaf = open(mcafile,'r')
    for l in mcaf.readlines():
        if re.match("\s*#.*", l): continue
        tokens = [t.strip() for t in l.split(':')]
        if len(tokens)<2: continue
        if tokens[0]==incl_mca and "+" in tokens[1]:
            options_str = [t.strip() for t in (l.split(';')[1]).split(',')]
            for o in options_str:
                if "IncludeMca" in o: 
                    incl_file = o.split('=')[1]
            break
    if len(incl_file)==0: 
        print "Warning! '%s' include directive not found. Not adding pdf systematics samples to MCA file %s" %(incl_mca,MCASYSTS)
        return

    for i in range(1,NPDFSYSTS+1):
        postfix = "_%s%d" % (syst,i) # this is the change needed to make all alternative variations to be symmetrized
        mcafile_syst = open("%s/mca%s.txt" % (odir,postfix), "w")
        mcafile_syst.write(incl_mca+postfix+'   : + ; IncludeMca='+incl_file+', AddWeight="'+vec_weight+str(i)+'", PostFix="'+postfix+'" \n')
        pdfsysts.append(postfix)
    print "written ",vec_weight," systematics into ",MCASYSTS
    return MCASYSTS

def writePdfSystsToSystFile(filename,sample="W.*",syst="CMS_W_pdf"):
    SYSTFILEALL=('.').join(filename.split('.')[:-1])+"-all.txt"
    copyfile(filename,SYSTFILEALL)
    systfile=open(SYSTFILEALL,"a")
    for i in range(NPDFSYSTS/2):
        systfile.write(syst+str(i+1)+"  : "+sample+" : .* : pdf"+str(i+1)+" : templates\n")
    print "written pdf syst configuration to ",SYSTFILEALL
    return SYSTFILEALL

        
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

MCASYSTS=MCA
if options.addPdfSyst:
    # write the additional systematic samples in the MCA file
    MCASYSTS = writePdfSystsToMCA(MCA,outdir+"/mca")
    # write the complete systematics file (this was needed when trying to run all systs in one job)
    # SYSTFILEALL = writePdfSystsToSystFile(SYSTFILE)

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
    WYBinsEdges = makeYWBinning(os.environ['CMSSW_BASE']+'/src/CMGTools/WMass/data/efficiency/mc_reco_eff.root')#, 5000)
    ybinfile = open(outdir+'/binningYW.txt','w')
    ybinfile.write(json.dumps(WYBinsEdges))
    #ybinfile.writelines(' '.join(str(i) for i in WYBinsEdges))
    ybinfile.close()
    print "MAKING SIGNAL PART: WYBinsEdges = ",WYBinsEdges
    for ip,pdf in enumerate(pdfsysts):
        for helicity in ['right', 'left']:
            antihel = 'right' if helicity == 'left' else 'left'
            for charge in ['plus','minus']:
                antich = 'plus' if charge == 'minus' else 'minus'
                YWbinning = WYBinsEdges['{ch}_{hel}'.format(ch=charge,hel=helicity)]
                if ip==0: 
                    IARGS = ARGS
                else: 
                    IARGS = ARGS.replace(MCA,"{outdir}/mca/mca{syst}.txt".format(outdir=outdir,syst=pdf))
                    IARGS = IARGS.replace(SYSTFILE,"{outdir}/mca/systEnv-dummy.txt".format(outdir=outdir))
                    print "Running the systematic: ",pdf
                for iy in xrange(len(YWbinning)-1):
                    print "Making card for %s<=abs(genw_y)<%s and signal process with charge %s " % (YWbinning[iy],YWbinning[iy+1],charge)
                    ycut=" -A alwaystrue YW%d 'abs(genw_y)>=%s && abs(genw_y)<%s' " % (iy,YWbinning[iy],YWbinning[iy+1])
                    ycut += POSCUT if charge=='plus' else NEGCUT
                    excl_long_signal  = '' if not options.longBkg else ',W{ch}_long'.format(ch=charge)
                    xpsel=' --xp "W{antich}.*,W{ch}_{antihel},Flips,Z,Top,DiBosons,TauDecaysW{longbkg},data.*" --asimov '.format(antich=antich,ch=charge,antihel=antihel,longbkg = excl_long_signal)
                    if not os.path.exists(outdir): os.mkdir(outdir)
                    if options.queue and not os.path.exists(outdir+"/jobs"): os.mkdir(outdir+"/jobs")
                    syst = '' if ip==0 else pdf
                    dcname = "W{charge}_{hel}_{channel}_Ybin_{iy}{syst}".format(charge=charge, hel=helicity, channel=options.channel,iy=iy,syst=syst)
                    BIN_OPTS=OPTIONS + " -W '" + options.weightExpr + "'" + " -o "+dcname+" --od "+outdir + xpsel + ycut
                    if options.queue:
                        srcfile=outdir+"/jobs/"+dcname+".sh"
                        logfile=outdir+"/jobs/"+dcname+".log"
                        srcfile_op = open(srcfile,"w")
                        srcfile_op.write("#! /bin/sh\n")
                        srcfile_op.write("ulimit -c 0 -S\n")
                        srcfile_op.write("ulimit -c 0 -H\n")
                        srcfile_op.write("cd {cmssw};\neval $(scramv1 runtime -sh);\ncd {dir};\n".format( 
                                dir = os.getcwd(), cmssw = os.environ['CMSSW_BASE']))
                        srcfile_op.write("python {dir}/makeShapeCards.py {args} \n".format(
                                dir = os.getcwd(), args = IARGS+" "+BIN_OPTS))
                        os.system("chmod a+x "+srcfile)
                        cmd = "bsub -q {queue} -o {dir}/{logfile} {dir}/{srcfile}\n".format(
                            queue=options.queue, dir=os.getcwd(), logfile=logfile, srcfile=srcfile)
                        if options.dryRun: print cmd
                        else: os.system(cmd)
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
        chargecut = POSCUT if charge=='plus' else NEGCUT
        dcname = "bkg_and_data_{channel}_{charge}".format(channel=options.channel, charge=charge)
        BIN_OPTS=OPTIONS + " -W '" + options.weightExpr + "'" + " -o "+dcname+" --od "+outdir + xpsel + chargecut
        if options.queue:
            srcfile=outdir+"/jobs/"+dcname+".sh"
            logfile=outdir+"/jobs/"+dcname+".log"
            srcfile_op = open(srcfile,"w")
            srcfile_op.write("#! /bin/sh\n")
            srcfile_op.write("ulimit -c 0 -S\n")
            srcfile_op.write("ulimit -c 0 -H\n")
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
