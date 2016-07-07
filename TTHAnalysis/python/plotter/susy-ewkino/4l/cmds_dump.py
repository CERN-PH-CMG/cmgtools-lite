import os

# principal output dir (tags will be added)
O    = "/afs/cern.ch/user/c/cheidegg/www/heppy/2016-06-30_ewk80X_plots_final/"

# tree input dir
T    = "/mnt/t3nfs01/data01/shome/cheidegg/o/2016-06-09_ewktrees80X_2LL_mix/"
jlr  = "leptonJetReCleanerSusyEWK3L"
lch  = "leptonBuilderEWK"
flags = ""
flags = "--plotgroup _fakeappl_data+=_promptsub  --perBin"

# lumi in /fb
#lumi = 0.8042 # blinding
lumi = 4
lspam = "#bf{CMS} #it{Preliminary}" 
#lspam = "#bf{CMS} #it{Simulation}" 

# do
process = "data"

# category
categ = [
         #"A", # 3l light nOSSF = 1
         #"B", # 3l light nOSSF = 0
         #"C", # 3l 1tau  nOSSF = 1
         #"D", # 3l 1tau  nOSSF = 0 nOSLF = 1
         #"E", # 3l 1tau  nOSLF = 0
         #"F", # 3l 2tau ## CURRENTLY MISSING
         #"G", # 4l light nOSSF >= 2
         "H", # 4l light nOSSF <= 1
         #"I", # 4l 1tau  nOSSF >= 0
        ]

scenario = [
            #["SR"     , ""                      ], # signal region
            #["SR"     , "-X blinding"           ], # signal region
            ["SBfakes", "-X blinding -I SRevent"], # sideband 
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

def getNum(categ):
	return ["A", "B", "C", "D", "E", "F", "G", "H", "I"].index(categ) + 1

def getBR(categ):
	if categ in ["A", "B", "C", "D", "E", "F", "G", "H", "I"]: 
		return "-A alwaystrue BRcut 'BR == " + str(getNum(categ)) + "'"
	return ""

def getCuts(categ):
	cuts = getBR(categ)
	if categ in ["C", "D", "E", "F"]: cuts += " -X trigger"
	return cuts

def getFMT(categ):
	return "'{run:1d} {lumi:9d} {evt:12d}'"
	add = ""
	mT2 = "mT2L_3l"
	mll = "mll_3l"
	mT  = "mT_3l"
	if categ == "F": mT2 = "mT2T_3l"
	if categ in ["G", "H", "I"]: 
		add = "\\t{LepSel4_pdgId:+2d} {LepSel4_pt:5.1f} {LepSel4_mcMatchId:2d}"
		mT2 = "mT2L_4l"
		mll = "mll_4l"
		mT  = "mT_4l"
	return "'{run:1d} {lumi:9d} {evt:12d}\\t{LepSel1_pdgId:+2d} {LepSel1_pt:5.1f} {LepSel1_mcMatchId:2d}\\t{LepSel2_pdgId:+2d} {LepSel2_pt:5.1f} {LepSel2_mcMatchId:2d}\\t{LepSel3_pdgId:+2d} {LepSel3_pt:5.1f} {LepSel3_mcMatchId:2d}" + add + "\\t{nJet30:d}\\t{nBJetMedium25:2d}\\t{met_pt:5.1f}\\t{htJet30j:6.1f}\\t{" + mll + ":6.1f}\\t{" + mt + ":6.1f}\\t{" + mT2 + ":6.1f}'"

base = "python mcDump.py --dumpFile .fdump.txt susy-ewkino/4l/mca_ewkino.txt susy-ewkino/4l/cuts_ewkino.txt {FMT} -P {T} --s2v --tree treeProducerSusyMultilepton --mcc susy-ewkino/mcc_triggerdefs.txt --mcc susy-ewkino/4l/mcc_ewkino.txt -F sf/t {JLR} -F sf/t {LCH} --load-macro susy-ewkino/4l/functionsEWK.cc -p {PROC} {CUTS} {SC} &&  sort -n -k1 -k2 -k3 .fdump.txt > {O}/fdump_{PROC}.txt && rm .fdump.txt"

for sc in scenario:
	for c in categ:
		fmt = getFMT(c)
		output = O + "/" + sc[0] + "/dumps/" + c
		mkdir(output)

		cmd(base.format(O=output, T=T, JLR="{P}/"+jlr+"/evVarFriend_{cname}.root", LCH="{P}/"+lch+"/evVarFriend_{cname}.root", FMT=fmt, PROC=process, CUTS=getCuts(c), SC=sc[1]))
