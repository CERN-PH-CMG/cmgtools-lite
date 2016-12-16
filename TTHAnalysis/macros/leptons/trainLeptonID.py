# wrapper around trainLeptonID.cxx cause I cannot remember all the commands
import ROOT, os
from optparse import OptionParser

def getTreePath(treedir, samplename):
	if not samplename: return ""
	if os.path.exists(treedir+"/"+samplename+"/treeProducerSusyMultilepton/tree.root"):
		return treedir+"/"+samplename+"/treeProducerSusyMultilepton/tree.root"
	elif os.path.exists(treedir+"/"+samplename+"/treeProducerSusyMultilepton/tree.root.url"):
		return open(treedir+"/"+samplename+"/treeProducerSusyMultilepton/tree.root.url").readlines()[0].rstrip("\n")
	else:
		return ""

def getTreeNEvt(treedir, samplename = None):
	if not samplename: return "0"
	path = treedir+"/"+samplename+"/skimAnalyzerCount/SkimReport.txt"
	if not os.path.exists(path): return "0"
	lines = [l.rstrip("\n") for l in open(path,"r").readlines()]
	for line in lines:
		if line.find("All Events")==-1: continue
		sl = line.split()
		return sl[2]
	return "0"

def cmd(base):
	print base
	os.system(base)

def submit(base, name, queue):
	if not queue: 
		cmd(base)
		return
	super = "bsub"
	if queue in ["all.q", "long.q", "short.q"]: super = "qsub"
	full = super +" -q {Q} -N {N} -o {W}/{N}.out -e {W}/{N}.err {W}/{N}.sh".format(Q=queue, N=name, W=os.getcwd())
	f = open(name+".sh","w")
	f.write("#!/bin/bash\n")
	f.write("source /mnt/t3nfs01/data01/swshare/psit3/etc/profile.d/cms_ui_env.sh\n")
	f.write("source $VO_CMS_SW_DIR/cmsset_default.sh\n")
	f.write("cd "+os.getcwd()+"\n")
	f.write("eval $(scramv1 runtime -sh);\n")
	f.write(base+"\n")
	cmd(full)

parser = OptionParser(usage="%prog treedir [options]")
parser.add_option("--model", dest="model", type="string"      , default="forMoriond16"               , help="The MVA name"        )
parser.add_option("--sig1" , dest="sig1" , type="string"      , default="TTZ_LO"                     , help="Signal process 1"    )
parser.add_option("--sig2" , dest="sig2" , type="string"      , default=None                         , help="Signal process 2"    )
parser.add_option("--bkg1" , dest="bkg1" , type="string"      , default="TTJets_SingleLeptonFromT"   , help="Background process 1")
parser.add_option("--bkg2" , dest="bkg2" , type="string"      , default="TTJets_SingleLeptonFromTbar", help="Background process 2")
parser.add_option("--multi", dest="multi", action="store_true", default=False                        , help="Do multi class"      )
parser.add_option("-q"     , dest="queue", type="string"      , default=None                         , help="Queue for batch submission")
(options, args) = parser.parse_args()
treedir = args[0].rstrip("/")

base = "root.exe -b -l -q 'trainLeptonID.cxx(\"{MODEL}\", \"{SIG1}\", \"{SIG2}\", \"{BKG1}\", \"{BKG2}\", {MULTI}, \"\", \"\", \"\", \"\", {NS1}, {NS2}, {NB1}, {NB2})'"

for flavor in ["el", "mu"]:
	name    = options.model+"_"+flavor
	submit(base.format(MODEL=name, SIG1 =getTreePath(treedir, options.sig1), \
	                               SIG2 =getTreePath(treedir, options.sig2), \
	                               BKG1 =getTreePath(treedir, options.bkg1), \
	                               BKG2 =getTreePath(treedir, options.bkg2), \
	                               MULTI="true" if options.multi else "false", \
	                               NS1  =getTreeNEvt(treedir, options.sig1), \
	                               NS2  =getTreeNEvt(treedir, options.sig2), \
	                               NB1  =getTreeNEvt(treedir, options.bkg1), \
	                               NB2  =getTreeNEvt(treedir, options.bkg2)), name, options.queue)
