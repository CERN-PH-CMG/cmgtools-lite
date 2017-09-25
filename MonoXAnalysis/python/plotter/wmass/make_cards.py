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
masses = range(mass_id_down, mass_id_down + n_mass_id)
#masses = [19]
T='/data1/emanuele/wmass/TREES_1LEP_53X_V3_WSKIM_V7/'
if 'pccmsrm29' in os.environ['HOSTNAME']: T = T.replace('/data1/emanuele/wmass','/u2/emanuele')
elif 'lxplus' in os.environ['HOSTNAME']: T = T.replace('/data1/emanuele/wmass','/afs/cern.ch/work/e/emanuele/TREES/')
elif 'cmsrm-an' in os.environ['HOSTNAME']: T = T.replace('/data1/emanuele/wmass','/t3/users/dimarcoe/')
print "used trees from: ",T
J=4
BASECONFIG="wmass_e"
#BASECONFIG=""
MCA=BASECONFIG+'/mca-53X-wenu.txt'
CUTFILE=BASECONFIG+'/wenu.txt'
SYSTFILE=BASECONFIG+'/systsEnv.txt'
# moved below option parser to allow their setting with options
#VAR="mt_lu_cart(LepCorr1_pt,LepGood1_phi,w_ux,w_uy) 90,30,120"
#VAR="LepCorr1_pt 28,36,50"
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
parser.add_option("--etaBins", dest="etaBins", action="append", default=['0','0.45','0.8','1.15','1.479','2.0','2.5'], help="Give a list of lepton eta bins to make fit categories")
parser.add_option("--fitVar", dest="fitVar", type="string", default="pt", help="Pass the name of variable to fit (pt or mt, default is pt)")
parser.add_option("--fitRange", dest="fitRange", type="string", default="", help="Pass the number of bins and range to be used for the fit, e.g '40,30,50'. Arguments are separated by commas with no spaces (use only integer numbers please")
parser.add_option("-q", "--queue",    dest="queue",     type="string", default=None, help="Run jobs on lxbatch instead of locally");
parser.add_option("--dry-run", dest="dryRun",    action="store_true", default=False, help="Do not run the job, only print the command");
(options, args) = parser.parse_args()

if options.fitVar == "mt":
    if len(options.fitRange)>0:
        VAR="mt_lu_cart(LepCorr1_pt,LepGood1_phi,w_ux,w_uy) " + options.fitRange
    else:
        VAR="mt_lu_cart(LepCorr1_pt,LepGood1_phi,w_ux,w_uy) 90,30,120"
elif options.fitVar == "pt":
    if len(options.fitRange)>0:
        VAR="LepCorr1_pt " + options.fitRange
    else:
        VAR="LepCorr1_pt 40,30,50"
else:
    print "options.fitVar = '%s': not a valid option (use pt or mt)" % options.fitVar
print str(VAR)

if not os.path.exists("cards/"):
    os.makedirs("cards/")
outdir="cards/"+args[0]

# write systematic variations to be considered in the MCA file
MCASYSTS=('.').join(MCA.split('.')[:-1])+"-systs.txt"
copyfile(MCA,MCASYSTS)
writePdfSystsToMCA("W","pdf","WJets",37509.0,"pdfWeight_CT10",MCASYSTS)

# write the complete systematics file
SYSTFILEALL=('.').join(SYSTFILE.split('.')[:-1])+"-all.txt"
copyfile(SYSTFILE,SYSTFILEALL)
writePdfSystsToSystFile("W","pdf","CMS_We",SYSTFILEALL)

fitvar = VAR.split()[0]
x_range = (VAR.split()[1]).split(",")[-2:]
ARGS=" ".join([MCASYSTS,CUTFILE,"'"+fitvar+"' "+VAR.split()[1],SYSTFILEALL])
if options.queue:
    ARGS = ARGS.replace(BASECONFIG,os.getcwd()+"/"+BASECONFIG)
OPTIONS=" -P "+T+" --s2v -j "+str(J)+" -l 19.7 -f --obj tree "+FASTTEST
if not os.path.exists(outdir): os.makedirs(outdir)
OPTIONS+=" -F mjvars/t '{P}/friends/evVarFriend_{cname}.root' --FMC sf/t '{P}/friends/sfFriend_{cname}.root' --FMC kinvars/t '{P}/friends/kinVarFriend_{cname}.root' "

print "Mass IDs that will be done: ",masses," (",mass_id_central," is the central one)"
mass_offs = 0

FITRANGE=" -A alwaystrue fitrange '%s>%s && %s<%s' " % (fitvar,x_range[0],fitvar,x_range[1])
OPTIONS += FITRANGE

if options.queue:
    import os, sys
    basecmd = "bsub -q {queue} {dir}/lxbatch_runner.sh {dir} {cmssw} python {self}".format(
                queue = options.queue, dir = os.getcwd(), cmssw = os.environ['CMSSW_BASE'], self=sys.argv[0]
            )

etaBins=[]
isEtaIncl = True
if len(options.etaBins):
    etaBins = [binEdge for binEdge in options.etaBins.split(",")]
    isEtaIncl = False
else: 
    etaBins=['0','5']
print "Categories in lepton eta = ",etaBins

for ieta in range(len(etaBins)-1):
    subdir = ("eta_%.1f_%.1f" % (float(etaBins[ieta]),float(etaBins[ieta+1]))).replace(".","p") if not isEtaIncl else 'etaIncl'
    etacut=" -A alwaystrue eta%d 'abs(LepGood1_eta)>%s && abs(LepGood1_eta)<%s' " % (ieta,etaBins[ieta],etaBins[ieta+1])
    myout = outdir + "/" + subdir
    if not os.path.exists(myout): os.mkdir(myout)
    if options.queue and not os.path.exists(outdir+"/jobs"): os.mkdir(outdir+"/jobs")
    for mass in masses:
        smass=str(mass-mass_offs)
        W=" -W 'puWeight*SF_LepTight_1l*zpt_w*aipi_w*mwWeight["+str(mass)+"]' "
        POS=" -A alwaystrue positive 'LepGood1_charge>0' "
        NEG=" -A alwaystrue negative 'LepGood1_charge<0' "
        charges=[POS,NEG]
        for c in charges: 
            dcname="wenu_mass"+smass+("_pos_" if "positive" in c else "_neg_")+subdir
            BIN_OPTS=OPTIONS+W+" -o "+dcname+" --od "+myout+" --floatProcesses W --groupSystematics pdfUncertainties pdf"
            if options.queue:
                srcfile=outdir+"/jobs/"+dcname+".sh"
                logfile=outdir+"/jobs/"+dcname+".log"
                srcfile_op = open(srcfile,"w")
                srcfile_op.write("#! /bin/sh\n")
                srcfile_op.write("cd {cmssw};\neval $(scramv1 runtime -sh);\ncd {dir};\n".format( 
                        dir = os.getcwd(), cmssw = os.environ['CMSSW_BASE']))
                srcfile_op.write("python {dir}/makeShapeCards.py {args} \n".format(
                        dir = os.getcwd(), args = ARGS+" "+BIN_OPTS+c+etacut))
                os.system("chmod a+x "+srcfile)
                cmd = "bsub -q {queue} -o {dir}/{logfile} {dir}/{srcfile}\n".format(
                    queue=options.queue, dir=os.getcwd(), logfile=logfile, srcfile=srcfile)
                if options.dryRun: print cmd
                else: os.system(cmd)
            else:
                cmd = "python makeShapeCards.py "+ARGS+" "+BIN_OPTS+c+etacut
                if options.dryRun: print cmd
                else:
                    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
                    out, err = p.communicate() 
                    result = out.split('\n')
                    for lin in result:
                        if not lin.startswith('#'):
                            print(lin)
