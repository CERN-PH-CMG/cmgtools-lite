import os

# principal output dir (tags will be added)
O    = "/afs/cern.ch/user/c/cheidegg/www/heppy/2016-06-10_ewk76X_limitsFinalMVA"

# tree input dir
T    = "/mnt/t3nfs01/data01/shome/cheidegg/o/2016-06-01_ewktrees76X_2LL"
jlr  = "THEGREATESTBESTEVERFRIENDTREES/leptonJetReCleanerSusyRA7mva"
lch  = "THEGREATESTBESTEVERFRIENDTREES/leptonChoiceEWK"
sys  = "systs_dummy.txt"

# lumi in /fb
lumi = 3

# model
model = [
         "TChiNeu_WZ",
         "TChiNeu_WH", 
         "TChiNeu_SlepSneu_FD", 
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
	return ["_matched_fakes_.*", "_standard_prompt_.*", "_standard3l_prompt_.*"]

def getBinning(categs):
	nb = sum(getNBins(categ) for categ in categs)
	return str(nb) + ",0.5,"+str(nb)+".5"	

def getCategs(model):
	if model == "TChiNeu_WZ"         : return ["A"]
	if model == "TChiNeu_WH"         : return ["A"]
	if model == "TChiNeu_SlepSneu_FD": return ["A"]
	if model == "TChiNeu_SlepSneu_TE": return ["C"]
	if model == "TChiNeu_SlepSneu_TD": return ["C", "D", "E"]
	if model == "TNeuNeu_ZZ"         : return ["G"]
	if model == "TNeuNeu_HZ"         : return ["H", "I"]
	if model == "TNeuNeu_HH"         : return ["H", "I"]
	return []	

def getCategNum(categ):
	categs = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"]
	return categs.index(categ)+1

def getCut1(categs):
	return "-A alwaystrue goodCateg '" + " || ".join("categ == " + str(getCategNum(c)) for c in categs) + "'"

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
	if categ == "B": return 24
	if categ == "C": return 36
	if categ == "D": return 24
	if categ == "E": return 24
	if categ == "F": return 1
	if categ == "G": return 4
	if categ == "H": return 4
	if categ == "I": return 4
	if categ == "J": return 4
	if categ == "K": return 4
	return 0

def getOffset(categ):
	categs = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"]
	idx = categs.index(categ)
	offset = 0
	for i in range(idx):
		offset += getNBins(categs[i])
	return offset

def getSigs(model):
	return ["_sig_" + model + "_.*"]

base = "python makeShapeCardsSusy.py susy-ewkino/3l/mca_ewkino.txt susy-ewkino/3l/cuts_ewkino.txt \"{EXPR}\" \"{BINS}\" susy-ewkino/{SYSTS} -o SR --asimov -P {T} --mcc susy-ewkino/3l/mcc_triggerdefs.txt --neg --s2v --tree treeProducerSusyMultilepton -F sf/t {JLR} -F sf/t {LCH} -f -j 8 --od {O} -l {L} {BKG} {SIG} {CUTS}"
#base = "python makeShapeCardsSusy.py susy-ewkino/3l/mca_ewkino.txt susy-ewkino/3l/cuts_ewkino.txt \"{EXPR}\" \"{BINS}\" susy-ewkino/{SYSTS} -o SR --asimov -P {T} --mcc susy-ewkino/3l/mcc_triggerdefs.txt --neg --s2v --tree treeProducerSusyMultilepton -F sf/t {JLR} -F sf/t {LCH} -f -j 8 --od {O} -l {L} {BKG} {SIG} {CUTS} -A haspair categA 'nTriples == 1' -A haspair tightMVAT '(LepGood1_mvaSUSY>0.15+(-0.15+0.65)*(abs(LepGood1_pdgId)==11)) && (LepGood2_mvaSUSY>0.15+(-0.15+0.65)*(abs(LepGood2_pdgId)==11)) && (LepGood3_mvaSUSY>0.15+(-0.15+0.65)*(abs(LepGood3_pdgId)==11))'"

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

	cmd(base.format(O=output, T=T, L=lumi, JLR="{P}/"+jlr+"/evVarFriend_{cname}.root", LCH="{P}/"+lch+"/evVarFriend_{cname}.root", EXPR=expr, BINS=bins, SYSTS=sys, CUTS=cut1+" "+cut2, BKG=bkg, SIG=sig))
