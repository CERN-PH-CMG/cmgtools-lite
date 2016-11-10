import os
## this script requires an MCA file that contains BKG and DATA including all
## variations; and a list of signal masspoints of the format: 
## MASS1 : MASS2 : FILENAME
## also, give the xsec for every mass of C1N2 in the format:
## MASS : XSEC
## in particular, the mass points need to be splitted
## -> a separate directory with treeProducerSusyMultilepton, skimAnalyzerCount, etc. for every mass point

## this script will loop over all mass points, run the bkg and data once (!)
## and add the signal in every iteration and create the data cards for every mass point


# principal output dir (tags will be added)  --- DATA-CARDS 
OUT   = "/afs/cern.ch/user/f/folguera/workdir/SUS/EWKino/CMSSW_8_0_11/src/CMGTools/TTHAnalysis/python/plotter/susy-ewkino/cards"

# tree input dir
T    = "/afs/cern.ch/user/f/folguera/workdir/trees/ewkino/8011_July5_skimmed/"

# lumi in /fb
lumi = 9.2

# templating
sys     = "susy-ewkino/systs_ewkino.txt"
mccs    = ["susy-ewkino/mcc_triggerdefs.txt", "susy-ewkino/2lss/lepchoice-2lss-FO.txt"]  #HERE !!! 
macros  = []   
friends = ["sf/t {{P}}/2_recleaner_wpsViX4mrE2_ptJIMIX3/evVarFriend_{{cname}}.root"]
W       = "susy-ewkino/2lss/"
mcafile = "mca-2lss-mcdata-frdata.txt" # within directory W
cutfile = "cuts_2lss.txt"        # within directory W

# batch
batch   = True # masspoints (NOT bkg!) are run on batch
queue   = "8nh -W 70"
points  = 5 # masspoints per job if running on batch

# name, filepath (masspoints) and filepath (xsec) of the model
modelname  = "TChiNeu_SlepSneu_FD"
modelfiles = "susy-ewkino/list_C1N2_LL_FD.txt"
modelxs    = "susy-ewkino/xsec_C1N2_LL_FD.txt" # in fb and with BR corrections applied

# flags
flagsD = "--plotgroup fakes_data+=promptsub --plotgroup fakes_appldata_ewk_Up+=promptsub_ewk_Up --plotgroup fakes_appldata_ewk_Dn+=promptsub_ewk_Dn" # this one and flagsS on BKG cmd
flagsS = "--ignore promptsub --ignore promptsub_ewk_Up --ignore promptsub_ewk_Dn -W 'puw2016_nInt_9p2fb(nTrueInt)*triggerSF_2lss_ewk(LepGood1_pt,LepGood2_pt,LepGood2_pdgId)'" # only this one on SIG cmd  
## MODIFY PUWEIGHT and ADD TRIGGER SF 

# signal region expression
expr   = "SR_ewk_ss2l(nJet40,LepGood1_conePt,LepGood1_phi, LepGood2_conePt,LepGood2_phi, met_pt,met_phi)"
bins   = "18,0.5,18.5"

# some labelling
channel  = "2lss" # Santi: 2lss, Jesus: wzcr


## ----------- this is the script beyond this point ------------------

W = W.rstrip("/")
T = T.rstrip("/")

def cmd(cmd):
	print cmd
	os.system(cmd)

def cp(location, destination):
	cmd("cp " + location + " " + destination)

def mkdir(path, cpIdx = True):
	if os.path.isdir(path) and os.path.exists(path.rstrip("/") + "/index.php"): return
	cmd("mkdir -p " + path)
	if cpIdx:
		cmd("cp /afs/cern.ch/user/g/gpetrucc/php/index.php " + path)

def cleandir(path):
	if not os.path.isdir(path): return
	path = path.rstrip("/")
	cmd("rm -rf " + path + "/*")

def replaceInFile(path, search, replace):
	f = open(path, "r")
	lines = "".join(f.readlines())
	f.close()
	lines = lines.replace(search, replace)
	cmd("rm " + path)
	f = open(path, "w")
	f.write(lines)
	f.close()

def submit(base, sig, num):
	global batch, points
	if batch:
		job = int(num)/int(points)
		script = W + "/tmp/run/run_job_" + str(job) + ".sh"
		if int(num) % int(points) == 0:
			cp(W + "/batch_runner.sh", script)
			replaceInFile(script, "WORK=$1; shift", "WORK=\"" + os.getcwd() + "\"")
			replaceInFile(script, "SRC=$1; shift" , "SRC=\"" + os.getcwd().replace("/CMGTools/TTHAnalysis/python/plotter", "") + "\"")
			cmd("chmod 777 "+script) 
		f = open(script, "a")
		f.write(base.replace("-j 8", "") + "\n")
		f.close()
	else:
		cmd(base)

def runAll():
	global batch, queue, W
	if not batch: return
	ls = os.listdir(W + "/tmp/run")
	mkdir(W + "/log", False)
	ss = "bsub -q " + queue + " -J scanner"
	if queue in ["all.q", "long.q", "short.q"]:
		ss = "qsub -q " + queue + " -N scanner"
	super = ss + " -o {W}/log/job_{J}.out -e {W}/log/job_{J}.err "
	for f in ls:
		if f.find("run_job") == -1: continue
		job = f.replace("run_job_","").replace(".sh","")
#		cmd("chmod  777 "+ f)
		cmd(super.format(W=os.getcwd() + "/" + W, J=job) + os.getcwd() + "/" + W + "/tmp/run/" + f)

def getXS(xs, mass):
	themass = [p[0].strip() for p in xs]
	thexs   = [p[1].strip() for p in xs]
	return thexs[themass.index(mass)] + "/2000."


base = "python makeShapeCardsSusy.py "+W+"/{{MCA}} "+W+"/{CUTS} \"{EXPR}\" \"{BINS}\" {{SYSTS}} -o SR -P {T} {MCCS} {MACROS} {FRIENDS} --neg --s2v --tree treeProducerSusyMultilepton -f -j 8 --od {{O}} -l {L} --out {CH} {{FLAGS}}"

min = bins.split(",")[1]
max = bins.split(",")[2]

output = OUT + "/" + channel + "/" + str(lumi) + "fb/" + modelname
mkdir(output)

myBase = base.format(CUTS=cutfile, EXPR=expr, BINS=bins, T=T, MCCS=" ".join("--mcc " + m for m in mccs), MACROS=" ".join("--load-macro " + m for m in macros), FRIENDS=" ".join("-F " + f for f in friends), L=lumi, MIN=min, MAX=max, CH=channel)

## run once for bkg
mkdir(output + "/bkg")
cmd(myBase.format(MCA=mcafile, SYSTS="", FLAGS=flagsD+" "+flagsS, O=output + "/bkg"))

## now run for every masspoint separately adding bkg and data via infile option
mkdir(W + "/tmp", False)
mkdir(W + "/tmp/mca", False)
mkdir(W + "/tmp/run", False)
cleandir(W + "/tmp/mca")
cleandir(W + "/tmp/run")
mkdir(output + "/mps")

ff = open(modelxs, "r")
xs = [l.rstrip("\n").split(":") for l in ff.readlines()]
ff.close()

f = open(modelfiles, "r")
ll = f.readlines()
f.close()

for i, l in enumerate(ll):
	mp = [x.strip("\n").strip() for x in l.split(":")]
	sig = modelname + "_" + mp[0] + "_" + mp[1]
	cp(W + "/" + mcafile, W + "/tmp/mca/mca_" + sig + ".txt")		
	f = open(W + "/tmp/mca/mca_" + sig + ".txt", "a")
	for fr in [("", ""), ("_jec_Up", ", FakeRate=\"susy-ewkino/2lss/fr-jecUp.txt\", SkipMe=True"), ("_jec_Dn", ", FakeRate=\"susy-ewkino/2lss/fr-jecDn.txt\", SkipMe=True")]:
		f.write("sig_" + sig + fr[0] + "+ : " + mp[2] + " : " + getXS(xs, mp[0]) + " : LepGood1_isMatchRightCharge && LepGood2_isMatchRightCharge ; Label=\"" + mp[0] + "/" + mp[1] + "\", LineStyle=1, FillColor=ROOT.kRed "+fr[1]+"\n")
	f.close()

	submit(myBase.format(MCA="tmp/mca/mca_" + sig + ".txt", SYSTS="", FLAGS=flagsS, O=output + "/mps/" + mp[0] + "_" + mp[1]) + " --infile " + output + "/bkg/common/SR.input.root --ip x", sig, i)

runAll()


