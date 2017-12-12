#!/usr/bin/env python
from shutil import copyfile
import re, sys, os, os.path, subprocess
# import some parameters from wmass_parameters.py, they are also used by other scripts
from wmass_parameters import *

if len(sys.argv) < 2:
    print "----- WARNING -----"
    print "Too few arguments: need at list output folder name."
    print "-------------------"
    quit()


FASTTEST=''
#FASTTEST='--max-entries 1000 '
T='/eos/cms/store/group/dpg_ecal/comm_ecal/localreco/TREES_1LEP_80X_V3_WENUSKIM_V3'
# if 'pccmsrm29' in os.environ['HOSTNAME']: T = T.replace('/data1/emanuele/wmass','/u2/emanuele')
# elif 'lxplus' in os.environ['HOSTNAME']: T = T.replace('/data1/emanuele/wmass','/afs/cern.ch/work/e/emanuele/TREES/')
# elif 'cmsrm-an' in os.environ['HOSTNAME']: T = T.replace('/data1/emanuele/wmass','/t3/users/dimarcoe/')
print "used trees from: ",T
J=4
BASECONFIG="wmass/wmass_e"
#BASECONFIG=""
MCA=BASECONFIG+'/mca-80X-wenu-helicity.txt'
CUTFILE=BASECONFIG+'/wenu.txt'
SYSTFILE=BASECONFIG+'/systsEnv.txt'
# moved below option parser to allow their setting with options
#VAR="mt_lu_cart(LepCorr1_pt,LepGood1_phi,w_ux,w_uy) 90,30,120"
#VAR="LepCorr1_pt 28,36,50"
# FIMXE: NPDFSYSTS to be made consistent with 13 TeV setup (CT10 was for 8 TeV)
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
parser = OptionParser(usage="%prog testname ")

parser.add_option("--fitVar", dest="fitVar", type="string", default="etapt", help="Pass the name of variable to fit (default is 2d etapt of the lepton)")
parser.add_option("-q", "--queue",    dest="queue",     type="string", default=None, help="Run jobs on lxbatch instead of locally");
parser.add_option("--dry-run", dest="dryRun",    action="store_true", default=False, help="Do not run the job, only print the command");
(options, args) = parser.parse_args()

if options.fitVar == "etapt":
    VAR="LepGood1_pt:LepGood1_eta 48,-2.1,2.1,20,30.,50."
else:
    print "options.fitVar = '%s': not a valid option " % options.fitVar
print str(VAR)

if not os.path.exists("cards/"):
    os.makedirs("cards/")
outdir="cards/"+args[0]

#FIXME: for the moment avoid this part, need to understand which weight to use
# write systematic variations to be considered in the MCA file
MCASYSTS=('.').join(MCA.split('.')[:-1])+"-systs.txt"
copyfile(MCA,MCASYSTS)
#writePdfSystsToMCA("W","pdf","WJets",61526.7,"LHEweight_wgt",MCASYSTS)

# write the complete systematics file
SYSTFILEALL=('.').join(SYSTFILE.split('.')[:-1])+"-all.txt"
copyfile(SYSTFILE,SYSTFILEALL)
#writePdfSystsToSystFile("W","pdf","CMS_We",SYSTFILEALL)

fitvar = VAR.split()[0]
x_range = (VAR.split()[1]).split(",")[-2:]
ARGS=" ".join([MCASYSTS,CUTFILE,"'"+fitvar+"' "+VAR.split()[1],SYSTFILEALL])
if options.queue:
    ARGS = ARGS.replace(BASECONFIG,os.getcwd()+"/"+BASECONFIG)
OPTIONS=" -P "+T+" --s2v -j "+str(J)+" -l "+str(luminosity)+" -f --obj tree "+FASTTEST
if not os.path.exists(outdir): os.makedirs(outdir)
OPTIONS+=" -F Friends '{P}/friends/tree_Friend_{cname}.root' "

if options.queue:
    import os, sys
    basecmd = "bsub -q {queue} {dir}/lxbatch_runner.sh {dir} {cmssw} python {self}".format(
                queue = options.queue, dir = os.getcwd(), cmssw = os.environ['CMSSW_BASE'], self=sys.argv[0]
            )

if not os.path.exists(outdir): os.mkdir(outdir)
if options.queue and not os.path.exists(outdir+"/jobs"): os.mkdir(outdir+"/jobs")

W=" -W 'puw2016_nTrueInt_36fb(nTrueInt)*trgSF_We(LepGood1_pdgId,LepGood1_pt,LepGood1_eta,2)*leptonSF_We(LepGood1_pdgId,LepGood1_pt,LepGood1_eta)' "
WYBins=list(xrange(-6,7))
#WYBins=[-1,0,1]
SignalProcesses=['Wp_long','Wp_left','Wp_right','Wm_long','Wm_left','Wm_right']
for sp in SignalProcesses:
    for iy in xrange(len(WYBins)-1):
        print "Making card for %s<genw_y<%s and signal process %s" (WYBins[iy],WYBins[iy+1],sp)
        ycut=" -A alwaystrue YW%d 'genw_y>%s && genw_y<%s' " % (iy,WYBins[iy],WYBins[iy+1])
        spsel=' -p %s --asimov ' % sp
        if not os.path.exists(outdir): os.mkdir(outdir)
        if options.queue and not os.path.exists(outdir+"/jobs"): os.mkdir(outdir+"/jobs")
        dcname = "%s_el_Ybin_%d" % (sp,iy)
        BIN_OPTS=OPTIONS+W+" -o "+dcname+" --od "+outdir + spsel + ycut
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
