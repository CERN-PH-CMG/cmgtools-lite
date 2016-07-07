import os

# principal output dir (tags will be added)
O      = "/afs/cern.ch/user/c/cheidegg/www/heppy/2016-06-29_ewk80X_plots_effs/4fb/"

# tree input dir
T      = "/mnt/t3nfs01/data01/shome/cheidegg/o/2016-06-09_ewktrees80X_2LL_mix/"
jlr    = "leptonJetReCleanerSusyEWK3L"
lch    = "leptonBuilderEWK"
perBin = False
flags  = ""

# lumi in /fb
lumi = 4

# process
procs = [
         #["WZ"       , "_standard_prompt_WZ"       ],
         #["TT"       , "_matched_fakes_TT"         ],
         #["ZG"       , "_standard_prompt_ZG"       ],
         #["data"     , "_standard_prompt_WZ"       ],
         #["fakesmc"  , "_matched_fakes_.*"         ], 
         #["fakesapp" , "_fakeappl_data_.*"         ], 
         ["ZZbkg"     , "_standard_prompt_ZZ -p _standard_prompt_HZZ"    ],
         #["C1N2WZ"   , "_sig_TChiNeu_WZ_.*"        ],
         #["C1N2WH"   , "_sig_TChiNeu_WH_.*"        ],
         #["C1N2LLFD" , "_sig_TChiNeu_SlepSneuFD_.*"],
         #["C1N2LLTE" , "_sig_TChiNeu_SlepSneuTE_.*"],
         #["C1N2LLTD" , "_sig_TChiNeu_SlepSneuTD_.*"],
         #["N2N3ZZ"   , "_sig_TNeuNeu_ZZ_.*"        ],
         #["N2N3HZ"   , "_sig_TNeuNeu_HZ_.*"        ],
         #["N2N3HH"   , "_sig_TNeuNeu_HH_.*"        ],
        ]

# cuts on top of baseline
effs = {
        #"baseline": [""]          , # baseline selection
        "SRG01": ["met<30", "nOSSF_4l>=2", "SR == 86"]          , # SR G01
        #"categA"  : ["BR == 1"], # 3l light nOSSF = 1 
        #"categB"  : ["BR == 2"], # 3l light nOSSF = 0
        #"categC"  : ["BR == 3"], # 3l light nOSSF = 1
        #"categD"  : ["BR == 4"], # 3l light nOSSF = 0 nOSLF = 1
        #"categE"  : ["BR == 5"], # 3l light nOSLF = 0
        #"categF"  : ["BR == 6"], # 3l 2tau
        #"categG"  : ["BR == 7"], # 4l light nOSSF = 2
        #"categH"  : ["BR == 8"], # 4l light nOSSF = 1
        #"categI"  : ["BR == 9"], # 4l 1tau  nOSSF = 1
       }

# bins (if perBin = True)
bins = {
        "br"    : ""     , # baseline region, no SR binning
        #"categA": "SR_A", # 3l light nOSSF = 1
       }


## ----------- this is the script beyond this point ------------------

O = O.rstrip("/")
T = T.rstrip("/")

def cmd(cmd):
	print cmd
	#os.system(cmd)

def mkdir(path):
	if os.path.isdir(path) and os.path.exists(path.rstrip("/") + "/index.php"): return
	cmd("mkdir -p " + path)
	cmd("cp /afs/cern.ch/user/g/gpetrucc/php/index.php " + path)

#def recursiveCutting(cutstring, it, after, cuts):
#	if len(cuts) == 0 or cuts[0] == "": return cutstring
#	cutstring += " -A " + after + " recursive" + str(it) + " '" + cuts[0] + "'"
#	return recursiveCutting(cutstring, it+1, "recursive" + str(it), cuts[1:])

def recursiveCutting(cutstring, it, after, cuts):
	for i, cut in enumerate(cuts):
		cutstring += " -A " + after + " recursive" + str(i) + " '" + cut + "'"
	return cutstring

baseAll = "python mcAnalysis.py susy-ewkino/4l/mca_ewkino.txt susy-ewkino/4l/cuts_ewkino.txt -P {T} --neg --s2v --tree treeProducerSusyMultilepton -j 8 --mcc susy-ewkino/mcc_triggerdefs.txt --mcc susy-ewkino/4l/mcc_ewkino.txt -l {L} -F sf/t {JLR} -F sf/t {LCH} {CUTS} {PROC} {FLAGS} --load-macro susy-ewkino/4l/functionsEWK.cc >> {O}"
baseBin = "python mcPlots.py susy-ewkino/4l/mca_ewkino.txt susy-ewkino/4l/cuts_ewkino.txt susy-ewkino/4l/plots_ewkino.txt -P {T} --neg --s2v --tree treeProducerSusyMultilepton -j 8 --mcc susy-ewkino/mcc_triggerdefs.txt --mcc susy-ewkino/4l/mcc_ewkino.txt -l {L} -F sf/t {JLR} -F sf/t {LCH} {CUTS} {PROC} {BINS} {FLAGS} --perBin --load-macro susy-ewkino/4l/functionsEWK.cc"

for c,v in effs.iteritems():
	output = O + "/" + c
	mkdir(output)
	cuts = recursiveCutting("", 0, "met", v)
	
	for p in procs:
		cmd(baseAll.format(O=output+"/"+c+"_"+p[0]+".txt", T=T, L=lumi, JLR="{P}/"+jlr+"/evVarFriend_{cname}.root", LCH="{P}/"+lch+"/evVarFriend_{cname}.root", CUTS=cuts, PROC="-p " + p[1], FLAGS=flags))

	if perBin:
		for b,k in bins.iteritems():
			for p in procs:
				cmd(baseBin.format(O=output+"/"+c+"_"+b+"_"+p[0]+".txt", T=T, L=lumi, JLR="{P}/"+jlr+"/evVarFriend_{cname}.root", LCH="{P}/"+lch+"/evVarFriend_{cname}.root", CUTS=cuts, PROC="-p " + p[1], BINS="--sP " + k, FLAGS=flags))



