import os

# principal output dir (tags will be added)
O    = "/afs/cern.ch/user/c/cheidegg/www/heppy/2016-06-26_ewk80X_limits_test"

# tree input dir
T    = "/mnt/t3nfs01/data01/shome/cheidegg/o/2016-06-09_ewktrees80X_2LL_mix/"
jlr  = "leptonJetReCleanerSusyEWK3L"
lch  = "leptonBuilderEWK"
sys  = "systs_dummy.txt"
flags = "--asimov"

# lumi in /fb
lumi = 4

# model
model = [
         "TChiNeu_WZ",
         "TChiNeu_SlepSneu_FD", 
         #"TChiNeu_WH", 
         #"TChiNeu_SlepSneu_TE", 
         #"TChiNeu_SlepSneu_TD", 
         #"TNeuNeu_ZZ", 
         #"TNeuNeu_HZ", 
         #"TNeuNeu_HH", 
        ] 


## ----------- this is the script beyond this point ------------------

O = O.rstrip("/")
T = T.rstrip("/")

def cmd(cmd):
	print cmd
	os.system(cmd)

def mkdir(path):
	if os.path.isdir(path) and os.path.exists(path.rstrip("/") + "/index.php"): return
	cmd("mkdir -p " + path)
	cmd("cp /afs/cern.ch/user/g/gpetrucc/php/index.php " + path)

def getBkgs():
	return ["_matched_fakes_.*", "_standard_prompt_.*"]

def getBinning(categs):
	nb = sum(getNBins(categ) for categ in categs)
	return str(nb) + ",0.5,"+str(nb)+".5"	

def getCategs(model):
	return ["B"]
	if model == "TChiNeu_WZ"         : return ["A"]
	if model == "TChiNeu_WH"         : return ["A"]
	if model == "TChiNeu_SlepSneu_FD": return ["A"]
	if model == "TChiNeu_SlepSneu_TE": return ["C"]
	if model == "TChiNeu_SlepSneu_TD": return ["B", "D", "E", "F"]
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

def getSigs(model):
	return ["_sig_" + model + "_.*"]

base = "python makeShapeCardsSusy.py susy-ewkino/3l/mca_ewkino.txt susy-ewkino/3l/cuts_ewkino.txt \"{EXPR}\" \"{BINS}\" susy-ewkino/{SYSTS} -o SR -P {T} --mcc susy-ewkino/mcc_triggerdefs.txt --mcc susy-ewkino/3l/mcc_ewkino.txt --neg --s2v --tree treeProducerSusyMultilepton -F sf/t {JLR} -F sf/t {LCH} -f -j 8 --od {O} -l {L} {BKG} {SIG} {CUTS} {FLAGS} --load-macro susy-ewkino/3l/functionsEWK.cc"

for m in model:
	output = O + "/" + str(lumi) + "fb/" + m
	mkdir(output)
	categs = getCategs(m) ## assume categories are consecutive for every model
	expr = getExpr(categs[0]) ## first one because of offset
	bins = getBinning(categs)	
	bkg = " ".join(["-p " + b for b in getBkgs()])
	sig = "-p " + getSigs(m)[0]
	cut1 = getCut1(categs)
	cut2 = getCut2(categs)

	cmd(base.format(O=output, T=T, L=lumi, JLR="{P}/"+jlr+"/evVarFriend_{cname}.root", LCH="{P}/"+lch+"/evVarFriend_{cname}.root", EXPR=expr, BINS=bins, SYSTS=sys, CUTS=cut1+" "+cut2, BKG=bkg, SIG=sig, FLAGS=flags))
