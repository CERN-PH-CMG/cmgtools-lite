import os

# principal output dir (tags will be added)
O    = "/afs/cern.ch/user/c/cheidegg/www/heppy/2016-07-05_ewk80X_plots_preapproval/"

# tree input dir
T    = "/mnt/t3nfs01/data01/shome/cheidegg/o/2016-06-09_ewktrees80X_2LL_mix/"
jlr  = "leptonJetReCleanerSusyEWK3L"
lch  = "leptonBuilderEWK"
#flags = "-W 'puw2016_nInt_4fb(nTrueInt)' --perBin --ratioOffset 0.03"
flags = "--plotgroup _fakeappl_data+=_promptsub -W 'puw2016_nInt_4fb(nTrueInt)' --perBin --ratioOffset 0.03"

# lumi in /fb
#lumi = 0.8042 # blinding
lumi = 4
lspam = "#bf{CMS} #it{Preliminary}" 
#lspam = "#bf{CMS} #it{Simulation}" 

# do
what  = "data" # data, bkg, sig, both (=bkg+sig separately), mix (=bkg+sig together)

# category
categ = [
         "A", # 3l light nOSSF = 1
         "B", # 3l light nOSSF = 0
         #"C", # 3l 1tau  nOSSF = 1
         #"D", # 3l 1tau  nOSSF = 0 nOSLF = 1
         #"E", # 3l 1tau  nOSLF = 0
         #"F", # 3l 2tau ## CURRENTLY MISSING
         #"G", # 4l light nOSSF >= 2
         #"H", # 4l light nOSSF <= 1
         #"I", # 4l 1tau  nOSSF >= 0
        ]

# plot binning
plots = [
         #"all"     , # everything
         #"br"      , # wide plots for all BR
         "perCateg", # one plot per principal category
         #"perMll"  , # one plot per mll bin
         #"perMt"   , # one plot per mT bin
         #"lep"     , # lepton quantities in BR
         #"evt"     , # event quantities in BR
        ]

scenario = [
            #["SR"     , ""                      ], # signal region
            ["SR"     , "-X blinding"           ], # signal region
            #["SBfakes", "-X blinding -I SRevent"], # sideband 
           ]


## ----------- this is the script beyond this point ------------------

O = O.rstrip("/")
T = T.rstrip("/")

def cmd(cmd):
	print cmd
	##os.system(cmd)

def mkdir(path):
	if os.path.isdir(path) and os.path.exists(path.rstrip("/") + "/index.php"): return
	cmd("mkdir -p " + path)
	cmd("cp /afs/cern.ch/user/g/gpetrucc/php/index.php " + path)

def getBkgs(categ):
	return ["fakes_appldata", "promptsub", "prompt_.*"]
	#return ["fakes_matched_.*", "prompt_.*"]
	#return ["fakes_matchedB", "fakes_matchedC", "fakes_matchedUDSG", "prompt_.*"]

def getNum(categ):
	return ["A", "B", "C", "D", "E", "F", "G", "H", "I"].index(categ) + 1

def getBR(categ):
	if categ in ["A", "B", "C", "D", "E", "F", "G", "H", "I"]: 
		return "-A alwaystrue BRcut 'BR == " + str(getNum(categ)) + "'"
	return ""

def getCuts(categ):
	cuts = getBR(categ)
	if categ in ["G", "H", "I"]: cuts += " -R met met0 'met_pt > 0'"
	if categ in ["C", "D", "E"]: cuts += " -X trigger"
	if categ in ["F"]: cuts += " -R trigger trigger2T 'Triggers_2tau' -A sanity tigherpteta 'abs(LepSel1_eta)<2.1 && abs(LepSel2_eta)<2.1 && abs(LepSel3_eta)<2.1'"
	return cuts

def getPlots(plot, categ):
	lop = []
	if plot in ["all", "lep"     ]                                 : lop.extend(["lep1_pt", "lep2_pt", "lep3_pt", "flavor"])
	if plot in ["all", "evt"     ]                                 : lop.extend(["mll", "met", "mtW","htJet30j","nJet30","nBJet25", "m3l"])
	if plot in ["all", "br"      ]                                 : lop.extend(["BR", "SR_3l_light", "SR_3l_1tau", "SR_3l_2tau", "SR_4l"])
	if plot in ["all", "perCateg"]                                 : lop.extend(["SR_" + categ])
	if plot in ["all", "perMll"  ] and not categ in ["G", "H", "I"]: lop.extend(["SR_" + categ])
	if plot in ["all", "perMll"  ] and     categ in ["G", "H", "I"]: lop.extend(["SR_GHI"])
	if plot in ["all", "perMll"  ] and     categ in ["A"]          : lop.extend(["SR_A_i.*"])
	if plot in ["all", "perMt"   ] and     categ in ["G", "H", "I"]: lop.extend(["SR_" + categ])
	if plot in ["all", "perMt"   ] and not categ in ["G", "H", "I"]: lop.extend(["SR_" + categ + "_p.*"])
	return lop

def getFlags(plot, categ):
	if not plot in ["lep", "evt"]: return ""
	if categ == "A": return "--legendHeader 'A: OSSF'"
	if categ == "B": return "--legendHeader 'B: noOSSF'"
	if categ == "C": return "--legendHeader 'C: OSSF+\#tau'"
	if categ == "D": return "--legendHeader 'D: e^{\#pm}\#mu^{\#mp}\#tau'"
	if categ == "E": return "--legendHeader 'E: SS+\#tau'"
	if categ == "F": return "--legendHeader 'F: e/\#mu+\#tau\#tau'"
	if categ == "G": return "--legendHeader 'G: 2OSSF'"
	if categ == "H": return "--legendHeader 'H: <2 OSSF'"
	if categ == "I": return "--legendHeader 'I: 3l+\#tau'"
	return ""

def getSigs(categ):
	if categ == "A": return ["_sig_TChiNeu_WZ_.*", "_sig_TChiNeu_WH_.*", "_sig_TChiNeu_SlepSneu_FD_.*"]
	if categ == "B": return ["_sig_TChiNeu_WH_.*", "_sig_TChiNeu_SlepSneu_TE_.*", "_sig_TChiNeu_SlepSneu_TD_.*"]
	if categ == "C": return ["_sig_TChiNeu_WH_.*", "_sig_TChiNeu_SlepSneu_TE_.*", "_sig_TChiNeu_SlepSneu_TD_.*"]
	if categ == "D": return ["_sig_TChiNeu_WH_.*", "_sig_TChiNeu_SlepSneu_TE_.*", "_sig_TChiNeu_SlepSneu_TD_.*"]
	if categ == "E": return ["_sig_TChiNeu_WH_.*", "_sig_TChiNeu_SlepSneu_TE_.*", "_sig_TChiNeu_SlepSneu_TD_.*"]
	if categ == "F": return ["_sig_TChiNeu_SlepSneu_TD_.*"]
	if categ == "G": return ["_sig_TNeuNeu_ZZ_.*", "_sig_TNeuNeu_HZ_.*", "_sig_TNeuNeu_HH_.*"]
	if categ == "H": return ["_sig_TNeuNeu_ZZ_.*", "_sig_TNeuNeu_HZ_.*", "_sig_TNeuNeu_HH_.*"]
	if categ == "I": return ["_sig_TNeuNeu_ZZ_.*", "_sig_TNeuNeu_HZ_.*", "_sig_TNeuNeu_HH_.*"]
	return []

#base = "python mcPlots.py susy-ewkino/3l/mca_ewkino.txt susy-ewkino/3l/cuts_ewkino.txt susy-ewkino/3l/plots_ewkino.txt -P {T}  --s2v --tree treeProducerSusyMultilepton -f -j 8 --lspam '{LSPAM}' --legendWidth 0.20 --legendFontSize 0.035 --mcc susy-ewkino/mcc_triggerdefs.txt --mcc susy-ewkino/3l/mcc_ewkino.txt --showMCError -l {L} --pdir {O} -F sf/t {JLR} -F sf/t {LCH} --load-macro susy-ewkino/3l/functionsEWK.cc {PROC} --sP {PLOT} {CUTS} {SC} " + flags
base = "python mcPlots.py susy-ewkino/3l/mca_ewkino.txt susy-ewkino/3l/cuts_ewkino.txt susy-ewkino/3l/plots_ewkino.txt -P {T} --neg --s2v --tree treeProducerSusyMultilepton -f -j 8 --lspam '{LSPAM}' --legendWidth 0.20 --legendFontSize 0.035 --mcc susy-ewkino/mcc_triggerdefs.txt --mcc susy-ewkino/3l/mcc_ewkino.txt --showRatio --showMCError -l {L} --pdir {O} -F sf/t {JLR} -F sf/t {LCH} --load-macro susy-ewkino/3l/functionsEWK.cc {PROC} --sP {PLOT} {CUTS} {SC} " + flags + " {FLAGS}"

for sc in scenario:
	for p in plots:
		if p == "br": # these plots are inclusive in categ
			saved = categ
			categ = [""]
	
		for c in categ:
			plots = getPlots(p, c)
			output = O + "/" + sc[0] + "/" + p + "/" + c
	
			## bkgs
			if what == "data":
				mkdir(output + "/data")
				bkgs = getBkgs(c)
				if len(bkgs) > 0:
					bkg = " ".join(["-p " + b for b in bkgs]) + " -p data"
					for plot in plots:
						cmd(base.format(O=output+"/data", T=T, LSPAM=lspam, L=lumi, JLR="{P}/"+jlr+"/evVarFriend_{cname}.root", LCH="{P}/"+lch+"/evVarFriend_{cname}.root", PLOT=plot, PROC=bkg, CUTS=getCuts(c), SC=sc[1], FLAGS=getFlags(p,c)))

			## both
			if what == "mix":
				mkdir(output + "/mix")
				bkgs = getBkgs(c)
				sigs = getSigs(c)
				if len(bkgs) + len(sigs) > 0:
					bkg = " --showIndivSigs --noStackSig " + " ".join(["-p " + b for b in bkgs]) + " " + " ".join(["-p " + b for b in sigs])
					for plot in plots:
						cmd(base.format(O=output+"/both", T=T, LSPAM=lspam, L=lumi, JLR="{P}/"+jlr+"/evVarFriend_{cname}.root", LCH="{P}/"+lch+"/evVarFriend_{cname}.root", PLOT=plot, PROC=bkg, CUTS=getCuts(c), SC=sc[1], FLAGS=getFlags(p,c)))
	
			## bkgs
			if what == "bkg" or what == "both":
				mkdir(output + "/bkg")
				bkgs = getBkgs(c)
				if len(bkgs) > 0:
					bkg = " ".join(["-p " + b for b in bkgs])
					for plot in plots:
						cmd(base.format(O=output+"/bkg", T=T, LSPAM=lspam, L=lumi, JLR="{P}/"+jlr+"/evVarFriend_{cname}.root", LCH="{P}/"+lch+"/evVarFriend_{cname}.root", PLOT=plot, PROC=bkg, CUTS=getCuts(c), SC=sc[1], FLAGS=getFlags(p,c)))
			
			## sigs
			if what == "sig" or what == "both":
				mkdir(output + "/sig")
				sigs = getSigs(c)
				if len(sigs) > 0:
					sig = "--emptyStack -p dummy --showIndivSigs --noStackSig " + " ".join(["-p " + s for s in sigs])
					for plot in plots:
						cmd(base.format(O=output+"/sig", T=T, LSPAM=lspam, L=lumi, JLR="{P}/"+jlr+"/evVarFriend_{cname}.root", LCH="{P}/"+lch+"/evVarFriend_{cname}.root", PLOT=plot, PROC=sig, CUTS=getCuts(c), SC=sc[1], FLAGS=getFlags(p,c)))
	
		if "saved" in locals(): 
			categ = saved
			del saved


	
