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


# principal output dir (tags will be added)
D = "2016-07-05_ewk80X_scan_4fb_C1N2LL"
I = "/mnt/t3nfs01/data01/shome/cheidegg/o/"
O = "/afs/cern.ch/user/c/cheidegg/www/heppy/"

# tree input dir
T    = "/mnt/t3nfs01/data01/shome/cheidegg/o/2016-06-09_ewktrees80X_2LL_mix/"
jlr  = "leptonJetReCleanerSusyEWK3L"
lch  = "leptonBuilderEWK"
sys  = "systs_dummy.txt"
#flags = "--asimov"
flagsD = "--plotgroup _fakeappl_data+=_promptsub" # this one and flagsS on BKG cmd
flagsS = "-p data -W 'puw2016_nInt_4fb(nTrueInt)' -X blinding" # only this one on SIG cmd

# lumi in /fb
lumi = 4

# templating
W       = "susy-ewkino/3l/"
mcafile = "mca_ewkino_scanTest.txt"

# batch
batch   = True # masspoints (NOT bkg!) are run on batch
queue   = "all.q"
points  = 5 # masspoints per job if running on batch

# name, filepath (masspoints) and filepath (xsec) of the model
model  =  [
           ["TChiNeu_SlepSneu_FD", "susy-ewkino/3l/list_C1N2_LL_FD.txt", "susy-ewkino/3l/xsec_C1N2_LL_FD.txt"],
          ]


## ----------- this is the script beyond this point ------------------

DI = I.rstrip("/") + "/" + D
DO = O.rstrip("/") + "/" + D

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

def getBkgs(sig = False):
	if not sig:
		return ["_fakeappl_data", "_promptsub", "_standard_prompt_.*"]
	return ["_fakeappl_data", "_standard_prompt_.*"]
	return ["_matched_fakes_.*", "_standard_prompt_.*"]

def getBinning(categs):
	nb = sum(getNBins(categ) for categ in categs)
	return str(nb) + ",0.5,"+str(nb)+".5"	

def getCategs(model):
	if model == "TChiNeu_WZ"         : return ["A"]
	if model == "TChiNeu_WH"         : return ["A"]
	if model == "TChiNeu_SlepSneu_FD": return ["A"]
	if model == "TChiNeu_SlepSneu_TE": return ["C"]
	if model == "TChiNeu_SlepSneu_TD": return ["B", "C", "D", "E", "F"]
	if model == "TNeuNeu_ZZ"         : return ["G", "H", "I"]
	if model == "TNeuNeu_HZ"         : return ["G", "H", "I"]
	if model == "TNeuNeu_HH"         : return ["G", "H", "I"]
	return []	

def getCategNum(categ):
	categs = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
	return categs.index(categ)+1

def getCut1(categs):
	return "-A alwaystrue goodCateg '" + " || ".join("BR == " + str(getCategNum(c)) for c in categs) + "'"

def getCut2(categs):
	offset = getOffset(categs[0]) 
	nbin   = sum(getNBins(categ) for categ in categs)
	return "-A alwaystrue inSR 'SR > " + str(offset) + " && SR <= " + str(offset + nbin) + "'"

def getExpr(categ):
	offset = getOffset(categ)
	if offset > 0: return "SR-" + str(offset)
	return "SR"

def getNBins(categ):
	if categ == "A": return 36
	if categ == "B": return 6
	if categ == "C": return 14
	if categ == "D": return 14
	if categ == "E": return 11
	if categ == "F": return 10
	if categ == "G": return 4
	if categ == "H": return 4
	if categ == "I": return 4
	return 0

def getOffset(categ):
	categs = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
	idx = categs.index(categ)
	offset = 0
	for i in range(idx):
		offset += getNBins(categs[i])
	return offset

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
		script = W + "/run/run_job_" + str(job) + ".sh"
		if int(num) % int(points) == 0:
			cp(W + "/batch_runner.sh", script)
			replaceInFile(script, "WORK=$1; shift", "WORK=\"" + os.getcwd() + "\"")
			replaceInFile(script, "SRC=$1; shift" , "SRC=\"" + os.getcwd().replace("/CMGTools/TTHAnalysis/python/plotter", "") + "\"")
		f = open(script, "a")
		f.write(base.replace("-j 8", "") + "\n")
		f.close()
	else:
		cmd(base)

def runAll():
	global batch, queue, W
	if not batch: return
	ls = os.listdir(W + "/run")
	mkdir(W + "/log", False)
	super = "qsub -q " + queue + " -N scanner -o {W}/log/job_{J}.out -e {W}/log/job_{J}.err "
	for f in ls:
		if f.find("run_job") == -1: continue
		job = f.replace("run_job_","").replace(".sh","")
		cmd(super.format(W=os.getcwd() + "/" + W, J=job) + os.getcwd() + "/" + W + "/run/" + f)

def getXS(xs, mass):
	themass = [p[0].strip() for p in xs]
	thexs   = [p[1].strip() for p in xs]
	return thexs[themass.index(mass)] + "/2000."
 
def upload():
	global DI, DO
	cmd("mv " + DI + " "  + DO)


base = "python makeShapeCardsSusy.py "+W+"/{{{{MCA}}}} "+W+"/cuts_ewkino.txt \"{EXPR}\" \"{BINS}\" susy-ewkino/{SYSTS} -o SR -P {T} --mcc susy-ewkino/mcc_triggerdefs.txt --mcc "+W+"/mcc_ewkino.txt --neg --s2v --tree treeProducerSusyMultilepton -F sf/t {JLR} -F sf/t {LCH} -f -j 8 --od {{O}} -l {L} {{BKG}} {CUTS} {{FLAGS}} --load-macro "+W+"/functionsEWK.cc"

for mod in model:
	m = mod[0]
	output = DI + "/" + str(lumi) + "fb/" + m
	mkdir(output)
	categs = getCategs(m) ## assume categories are consecutive for every model
	expr = getExpr(categs[0]) ## first one because of offset
	bins = getBinning(categs)	
	bkgD = " ".join(["-p " + b for b in getBkgs()])
	bkgS = " ".join(["-p " + b for b in getBkgs(True)])
	cut1 = getCut1(categs)
	cut2 = getCut2(categs)

	myBase=base.format(T=T, L=lumi, JLR="{{{{P}}}}/"+jlr+"/evVarFriend_{{{{cname}}}}.root", LCH="{{{{P}}}}/"+lch+"/evVarFriend_{{{{cname}}}}.root", EXPR=expr, BINS=bins, SYSTS=sys, CUTS=cut1+" "+cut2)

	## run once for bkg
	mkdir(output + "/bkg")
	cmd(myBase.format(O=output + "/bkg", BKG=bkgD, FLAGS=flagsS + " " + flagsD).format(MCA=mcafile))	

	## now run for every masspoint separately adding bkg and data via infile option
	mkdir(W + "/tmp", False)
	mkdir(W + "/run", False)
	cleandir(W + "/tmp")
	cleandir(W + "/run")
	mkdir(output + "/mps")
	#myBase = myBase.format(O=output + "/mps") ## NO! put it into a separate directory because of the ROOT file!

	ff = open(mod[2], "r")
	xs = [l.rstrip("\n").split(":") for l in ff.readlines()]
	ff.close()

	f = open(mod[1], "r")
	ll = f.readlines()
	f.close()

	for i, l in enumerate(ll):
		mp = [x.strip("\n").strip() for x in l.split(":")]
		sig = m + "_" + mp[0] + "_" + mp[1]

		cp(W + "/" + mcafile, W + "/tmp/mca_" + sig + ".txt")		
		f = open(W + "/tmp/mca_" + sig + ".txt", "a")
		for fr in ["central"]:
		#for fr in ["central", "jecUp", "jecDown"]:
			f.write("_sig_" + sig + "+ : " + mp[2] + " : " + getXS(xs, mp[0]) + " ; Label=\"" + mp[0] + "/" + mp[1] + "\", LineStyle=1, FillColor=ROOT.kRed, FakeRate=\"" + W + "/fakerate_standard_" + fr + ".txt\," + W + "/fakerate_load_isprompt.txt\,"+W+"/fakerate_filters_mc.txt\"\n")
		f.close()

		submit(myBase.format(O=output + "/mps/" + mp[0] + "_" + mp[1], BKG=bkgS, FLAGS=flagsS).format(MCA="tmp/mca_" + sig + ".txt") + " --infile " + output + "/bkg/common/SR.input.root --ip x -p _sig_" + sig, sig, i)

	runAll()


