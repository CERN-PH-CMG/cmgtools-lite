import os

# principal output dir (tags will be added)
O    = "/afs/cern.ch/user/c/cheidegg/www/heppy/2016-06-13_ewk76X_effsMVAtest"

# tree input dir
T    = "/mnt/t3nfs01/data01/shome/cheidegg/o/2016-06-01_ewktrees76X_2LL"
#T    = "/scratch/cheidegg/2016-05-03_ewktrees76X"
jlr  = "THEGREATESTBESTEVERFRIENDTREES/leptonJetReCleanerSusyRA7mva"
lch  = "THEGREATESTBESTEVERFRIENDTREES/leptonChoiceEWK"
#jlr  = "SyncWithIlliaWZ/leptonJetReCleanerSusyRA7mva_sync"
#lch  = "SyncWithIlliaWZ/leptonChoiceEWK_sync"

# lumi in /fb
lumi = 6

# process
procs = [
         ["WZ"      , "_standard_prompt_WZ"       ],
         #["TT"      , "_matched_fakes_TT"         ],
         #["ZG"      , "_standard_prompt_ZG"       ],
         #["fakes"   , "_matched_fakes_.*"         ], 
         #["prompt"  , "_standard_prompt_.*"       ],
         #["prompt"  , "_standard3l_prompt_.*"       ],
         #["C1N2WZ"  , "_sig_TChiNeu_WZ_.*"        ],
         #["C1N2WH"  , "_sig_TChiNeu_WH_.*"        ],
         #["C1N2LLFD", "_sig_TChiNeu_SlepSneuFD_.*"],
         #["C1N2LLTE", "_sig_TChiNeu_SlepSneuTE_.*"],
         #["C1N2LLTD", "_sig_TChiNeu_SlepSneuTD_.*"],
         #["N2N3ZZ"  , "_sig_TNeuNeu_ZZ_.*"        ],
         #["N2N3HZ"  , "_sig_TNeuNeu_HZ_.*"        ],
         #["N2N3HH"  , "_sig_TNeuNeu_HH_.*"        ],
        ]

# cuts on top of baseline
effs = {
        "baseline": [""]          , # baseline selection
        #"categA"  : ["categ == 1"], # 3l light nOSSF = 1 
        #"categB"  : ["categ == 2"], # 3l light nOSSF = 0
        #"categC"  : ["categ == 3"], # 3l light nOSSF = 1
        #"categD"  : ["categ == 4"], # 3l light nOSSF = 0 nOSLF = 1
        #"categE"  : ["categ == 5"], # 3l light nOSLF = 0
        #"categF"  : ["categ == 6"], # 3l 2tau ## CURRENTLY MISSING
        #"categG"  : ["categ == 7"], # 4l light nOSSF = 2
        #"categH"  : ["categ == 8"], # 4l light nOSSF = 1
        #"categI"  : ["categ == 9"], # 4l 1tau  nOSSF = 1
       }

# bins
bins = {
        "br"    : ""                     , # baseline region, no SR binning
        "test": "'SR_Loop' '3,0.5,3.5'", # 3l light nOSSF = 1
        #"categA": "'SR_Loop' '36,0.5,36.5'", # 3l light nOSSF = 1
       }


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

def recursiveCutting(cutstring, it, after, cuts):
	if len(cuts) == 0 or cuts[0] == "": return cutstring
	cutstring += " -A " + after + " recursive" + str(it) + " '" + cuts[0] + "'"
	return recursiveCutting(cutstring, it+1, "recursive" + str(it), cuts[1:])


base = "python mcAnalysis.py susy-ewkino/3l/mca_ewkino.txt susy-ewkino/3l/cuts_effs.txt -P {T} --neg --s2v --tree treeProducerSusyMultilepton -j 8 --mcc susy-ewkino/mcc_triggerdefs.txt -l {L} -F sf/t {JLR} -F sf/t {LCH} {CUTS} {PROC} {BINS} -u >> {O}"

for c,v in effs.iteritems():
	output = O + "/" + c
	mkdir(output)
	cuts = recursiveCutting("", 0, "met", v)

	for b,k in bins.iteritems():
		binning = ""
		if k != "": binning = "--yieldPerBin " + k
		for p in procs:
			cmd(base.format(O=output+"/"+c+"_"+b+"_"+p[0]+".txt", T=T, L=lumi, JLR="{P}/"+jlr+"/evVarFriend_{cname}.root", LCH="{P}/"+lch+"/evVarFriend_{cname}.root", CUTS=cuts, PROC="-p " + p[1], BINS=binning))




	
