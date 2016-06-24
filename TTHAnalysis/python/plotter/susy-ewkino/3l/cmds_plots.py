import os

# principal output dir (tags will be added)
O    = "/afs/cern.ch/user/c/cheidegg/www/heppy/2016-06-10_ewk76X_plotsFinalMVA"

# tree input dir
T    = "/mnt/t3nfs01/data01/shome/cheidegg/o/2016-06-01_ewktrees76X_2LL"
#T    = "/scratch/cheidegg/2016-05-03_ewktrees76X"
jlr  = "THEGREATESTBESTEVERFRIENDTREES/leptonJetReCleanerSusyRA7mva"
lch  = "THEGREATESTBESTEVERFRIENDTREES/leptonChoiceEWK"

# lumi in /fb
lumi = 6
lspam = "#bf{CMS} #it{Simulation}" 

# do
what = "both" # bkg, sig, both (=bkg+sig)

# category
categ = [
         "A", # 3l light nOSSF = 1
         #"B", # 3l light nOSSF = 0
         #"C", # 3l light nOSSF = 1
         #"D", # 3l light nOSSF = 0 nOSLF = 1
         #"E", # 3l light nOSLF = 0
         ##"F", # 3l 2tau ## CURRENTLY MISSING
         #"G", # 4l light nOSSF = 2
         #"H", # 4l light nOSSF = 1
         #"I", # 4l light nOSSF = 0
         #"J", # 4l 1tau  nOSSF = 1
         #"K", # 4l 1tau  nOSSF = 0
        ]

# plot binning
plots = [
         #"br"   , 
         #"perCateg", # one plot per principal category
         #"perMll"  , # one plot per mll bin
         "perMt"   , # one plot per mT bin
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

def getBkgs(categ):
	if categ in ["G", "H", "I", "J", "K"]:
		return ["_matched_fakes_.*", "_standard_prompt_.*", "_standard4l_prompt_.*"]
	return ["_matched_fakes_.*", "_standard_prompt_.*", "_standard3l_prompt_.*"]

def getCuts(categ):
	if categ in ["G", "H", "I", "J", "K"]: return "-R met met0 'met_pt > 0'"
	if categ in ["C", "D", "E", "F"]: return "-X trigger"
	return ""

def getPlots(plot, categ):
	if plot == "br"      : return ["SR_3l_light"]#["BR", "SR_3l_light", "SR_3l_1tau", "SR_3l_2tau", "SR_4l"]
	if plot == "perCateg": return []
	if plot == "perMll"  : 
		if categ in ["G", "H", "I", "J", "K"]:
			return ["SR_" + categ]
		return ["SR_" + categ + "_i.*"]
	if plot == "perMt"   :
		if categ in ["G", "H", "I", "J", "K"]:
			return ["SR_" + categ]
		return ["SR_" + categ + "_p6"]
	return []	

def getSigs(categ):
	return ["_sig_TChiNeu_WZ_350_20"]
	#return ["_sig_TChiNeu_WZ_.*", "_sig_TChiNeu_WH_.*", "_sig_TChiNeu_SlepSneu_FD_.*"]
	if categ == "A": return ["_sig_TChiNeu_WZ_.*", "_sig_TChiNeu_WH_.*", "_sig_TChiNeu_SlepSneu_FD_.*"]
	if categ == "B": return ["_sig_TChiNeu_WH_.*", "_sig_TChiNeu_SlepSneu_TE_.*", "_sig_TChiNeu_SlepSneu_TD_.*"]
	if categ == "C": return ["_sig_TChiNeu_WH_.*", "_sig_TChiNeu_SlepSneu_TE_.*", "_sig_TChiNeu_SlepSneu_TD_.*"]
	if categ == "D": return ["_sig_TChiNeu_WH_.*", "_sig_TChiNeu_SlepSneu_TE_.*", "_sig_TChiNeu_SlepSneu_TD_.*"]
	if categ == "E": return ["_sig_TChiNeu_WH_.*", "_sig_TChiNeu_SlepSneu_TE_.*", "_sig_TChiNeu_SlepSneu_TD_.*"]
	if categ == "F": return ["_sig_TChiNeu_SlepSneu_TD_.*"]
	if categ == "G": return ["_sig_TNeuNeu_ZZ_.*"]
	if categ == "H": return ["_sig_TNeuNeu_ZZ_.*", "_sig_TNeuNeu_HZ_.*", "_sig_TNeuNeu_HH_.*"]
	if categ == "I": return ["_sig_TNeuNeu_ZZ_.*", "_sig_TNeuNeu_HZ_.*", "_sig_TNeuNeu_HH_.*"]
	if categ == "J": return ["_sig_TNeuNeu_ZZ_.*", "_sig_TNeuNeu_HZ_.*", "_sig_TNeuNeu_HH_.*"]
	if categ == "K": return ["_sig_TNeuNeu_ZZ_.*", "_sig_TNeuNeu_HZ_.*", "_sig_TNeuNeu_HH_.*"]
	return []

base = "python mcPlots.py susy-ewkino/3l/mca_ewkino.txt susy-ewkino/3l/cuts_ewkino.txt susy-ewkino/3l/plots_ewkino.txt -P {T} --neg --s2v --tree treeProducerSusyMultilepton -f -j 8 --lspam '{LSPAM}' --legendWidth 0.20 --legendFontSize 0.035 --mcc susy-ewkino/3l/mcc_triggerdefs.txt --showMCError -l {L} --pdir {O} -F sf/t {JLR} -F sf/t {LCH} {PROC} --sP {PLOT} {CUTS}"

for p in plots:
	if p == "br": # these plots are inclusive in categ
		saved = categ
		categ = [""]

	for c in categ:
		plots = getPlots(p, c)
		output = O + "/" + p + "/" + c
		mkdir(output + "/bkg")
		mkdir(output + "/sig")

		## both
		if what == "both":
			bkgs = getBkgs(c)
			sigs = getSigs(c)
			if len(bkgs) + len(sigs) > 0:
				bkg = " --showIndivSigs --noStackSig " + " ".join(["-p " + b for b in bkgs]) + " " + " ".join(["-p " + b for b in sigs])
				for plot in plots:
					cmd(base.format(O=output+"/bkg", T=T, LSPAM=lspam, L=lumi, JLR="{P}/"+jlr+"/evVarFriend_{cname}.root", LCH="{P}/"+lch+"/evVarFriend_{cname}.root", PLOT=plot, PROC=bkg, CUTS=getCuts(c)))

		## bkgs
		if what == "bkg":
			bkgs = getBkgs(c)
			if len(bkgs) > 0:
				bkg = " ".join(["-p " + b for b in bkgs])
				for plot in plots:
					cmd(base.format(O=output+"/bkg", T=T, LSPAM=lspam, L=lumi, JLR="{P}/"+jlr+"/evVarFriend_{cname}.root", LCH="{P}/"+lch+"/evVarFriend_{cname}.root", PLOT=plot, PROC=bkg, CUTS=getCuts(c)))
		
		## sigs
		if what == "sig":
			sigs = getSigs(c)
			if len(sigs) > 0:
				sig = "--emptyStack -p dummy --showIndivSigs --noStackSig " + " ".join(["-p " + s for s in sigs])
				for plot in plots:
					cmd(base.format(O=output+"/sig", T=T, LSPAM=lspam, L=lumi, JLR="{P}/"+jlr+"/evVarFriend_{cname}.root", LCH="{P}/"+lch+"/evVarFriend_{cname}.root", PLOT=plot, PROC=sig, CUTS=getCuts(c)))

	if "saved" in locals(): 
		categ = saved
		del saved


	
