import os,sys

## to be executed in CMGTools/TTHAnalysis/python/plotter

publdir = sys.argv[1] ### "/afs/cern.ch/user/p/peruzzi/www/plots_softId_250516_forWP" #do NOT give a trailing /

do = sys.argv[2:]

if 'soft' not in do:
	treedir = "/data/peruzzi/soft_lep_training_forDirIso_76X/mix_for_rocs_nosoft/ "
	friends = " --Fs {P}/0_lepMVAfriends_v5 "
	#friends = " --Fs {P}/0_lepMVAfriends_v2 --Fs {P}/0_lepMVAfriends_v4 --Fs {P}/0_lepMVAfriends_v5 "
else:
	treedir = "/data/peruzzi/soft_lep_training_forDirIso_76X/mix_for_rocs/ "
	friends = ""

base = "lepton-efficiency/mca_ewkino_nopresel.txt lepton-efficiency/presel_cuts.txt lepton-efficiency/numerators_ewkino.txt lepton-efficiency/xvars_ewkino.txt -P " + treedir+friends + " --s2v --tree treeProducerSusyMultilepton --mcc lepton-efficiency/mcc-defs.txt "
rocs = "python rocCurves.py " + base + " --splitSig 1 -j 8 --logx --grid  --max-entries 250000"
effs = "python mcEfficiencies.py " + base + " --groupBy process --max-entries 250000"
plots = "python mcPlots.py -f lepton-efficiency/mca_ewkino_nopresel.txt lepton-efficiency/presel_cuts.txt lepton-efficiency/plots_lepquantities.txt -P " + treedir + " --s2v --tree treeProducerSusyMultilepton -j 8 --max-entries 250000 --plotmode=norm"


## ----------------- do not touch beyond this line --------------------

debug = ('debug' in do)

def cmd(cmd):
	print cmd
	if not debug:
		os.system(cmd)


## make rocs
## ---------------------------------------------------------------------
if "rocs" in do: 

	cmd("mkdir -p " + publdir + "/rocs 2> /dev/null && cp /afs/cern.ch/user/g/gpetrucc/php/index.php " + publdir + "/rocs")

	processes = [
		["TT_red,TT_true",""],
		["TT_red,T1_1500_100",""],
		["TT_red,WZ_true",""],
		["TT_red,TChiNeuWZ_mCh150_mChi120",""],
		["TT_red,WZ_350_20",""],
		["TT_red,WZ_350_100",""],
		["TT_red,WZ_200_100",""],
		["TT_red,WZTo2L2Q",""],
		["TT_red,WZ_350_20_OS",""],
		["TT_red,WZ_350_100_OS",""],
		["TT_red,WZ_200_100_OS",""],
		]

	ptbins = [(10,25),(25,999)]
	flav = ["mu","el"]
	plots = [
#		["compMVAs" , "'.*forMoriond.*,RA7t,RA5t,OSt,NROSt'"],
		["standardIDs" , "'.*forMoriond.*TTZ.*,RA7t.*,RA5t,OSt,NROSt'"],
	        ]
	rangestring = "--yrange 0.5 1.0"

	processes_soft = [["TT_red,TChiNeuWZ_mCh150_mChi120",""]]
	ptbins_soft = [(3.5,10),(5,10),(10,20)]
	plots_soft = [
	        ["softIDs" , "'.*SoftJetLessDY.*,SoftMoriondDY,sosID,SLsoft,RA7t,RA5t,OSt,NROSt' --Fs {P}/0_lepMVAfriends_v1"],
		]
	if 'soft' in do:
		processes = processes_soft
		ptbins = ptbins_soft
		plots = plots_soft
		rangestring = "--yrange 0 1 -X ^ptcut_5_7 -E ^ptcut_3p5_5"

	torun=[]
	for f in flav:
		flavstring = "-I ^mu" if f=="el" else ""
		for b in ptbins:
			torun.append([ "%s_pt_%s_%s"%(f,str(b[0]),str(b[1])), " --legend BR --xrange 0.001 10. %s -A alwaystrue pt 'LepGood_pt>%f && LepGood_pt<%f' %s "%(rangestring,b[0],b[1],flavstring) ])

	## production
	for p in processes:
		pn = p[0].replace(",", "_")
		cmd("mkdir -p " + publdir + "/rocs/" + pn + " 2> /dev/null && cp /afs/cern.ch/user/g/gpetrucc/php/index.php " + publdir + "/rocs/" + pn)
		for s in plots:
			for b in torun:
				cmd(rocs + " -p " + p[0] + " -o " + publdir + "/rocs/" + pn + "/" + b[0] + "_" + s[0] + ".root " + b[1] + " --sP " + s[1])


## make plots
## ---------------------------------------------------------------------
if "plots" in do: 

	cmd("mkdir -p " + publdir + "/plots 2> /dev/null && cp /afs/cern.ch/user/g/gpetrucc/php/index.php " + publdir + "/plots")

	processes = [
		["TT_true,T1_1500_100,WZ_true,WZ_200_100,WZTo2L2Q,TTHnobb_pow,TTZ,WZ_350_20,WZ_350_100,TT_red",""],
#		["T1_1500_100",""],
#		["WZ_true",""],
#		["TChiNeuWZ_mCh150_mChi120",""],
#		["WZ_350_20",""],
#		["WZ_350_100",""],
#		["WZ_200_100",""],
#		["WZTo2L2Q",""],
		]

	bins = [[],[]]
	ptbins = [(10,25),(25,999),(100,999)]
	flav = ["mu","el"]
	for f in flav:
		flavstring = "-I ^mu" if f=="el" else ""
		for b in ptbins:
			bins[0].append([ "%s_pt_%s_%s"%(f,str(b[0]),str(b[1])), "cuts_loose", " -X ^mom -A alwaystrue pt 'LepGood_pt>%f && LepGood_pt<%f' %s "%(b[0],b[1],flavstring) ])

	## production
	for p in processes:
		pn = p[0].replace(",", "_")
		cmd("mkdir -p " + publdir + "/plots/" + pn + " 2> /dev/null && cp /afs/cern.ch/user/g/gpetrucc/php/index.php " + publdir + "/plots/" + pn)
		for b in bins[0]:
			cmd(plots.replace("<DEN>", b[1]) + " -p " + p[0] + " --pdir " + publdir + "/plots/" + pn + "/" + b[0] + b[2])



## make effs
## ---------------------------------------------------------------------
if "effs" in do: 

	cmd("mkdir -p " + publdir + "/effs 2> /dev/null && cp /afs/cern.ch/user/g/gpetrucc/php/index.php " + publdir + "/effs")

	processes = [
		"TT_true",
#		"WZ_true",
#		"TT_true,T1_1500_100,WZTo2L2Q,WZ_200_100",
#		"TT_true,T1_1500_100,WZ_true,TChiNeuWZ_mCh150_mChi120,WZ_350_20",
#		"TT_red"
                ]

	bins = []

	ptbins = []#[(10,25),(25,999)]
	flav = ["mu","el"]
	
	for f in flav:
		etabins = [(0.0,1.479),(1.479,2.5)] if f=="el" else [(0.0,1.2),(1.2,2.5)]
		flavstring = "-I ^mu" if f=="el" else ""
		for b in ptbins:
			bins.append([ "%s_pt_%s_%s"%(f,str(b[0]),str(b[1])), "qcd1l-claudio", " --legend BR --yrange 0.5 1 -A alwaystrue pt 'LepGood_pt>%f && LepGood_pt<%f' %s --sP eta_fine"%(b[0],b[1],flavstring) ])
		for b in etabins:
			bins.append([ "%s_eta_%s_%s"%(f,str(b[0]),str(b[1])), "qcd1l-claudio", " --legend BR --yrange 0.5 1 -A alwaystrue eta 'abs(LepGood_eta)>%f && abs(LepGood_eta)<%f' %s --sP pt_cl"%(b[0],b[1],flavstring) ])
#	for f in flav:
#		flavstring = "-I ^mu" if f=="el" else ""
#		for b in ptbins:
#			bins.append([ "%s_pt_%s_%s"%(f,str(b[0]),str(b[1])), "cuts_loose", " --legend BR --yrange 0 1 -A alwaystrue pt 'LepGood_pt>%f && LepGood_pt<%f' %s --sP eta_fine"%(b[0],b[1],flavstring) ])
#		for b in etabins:
#			bins.append([ "%s_eta_%s_%s"%(f,str(b[0]),str(b[1])), "cuts_loose", " --legend BR --yrange 0 1 -A alwaystrue eta 'abs(LepGood_eta)>%f && abs(LepGood_eta)<%f' %s --sP pt_fine"%(b[0],b[1],flavstring) ])
			
	plots = [
#		["standardIDs" , " --sP 'CB_forMoriond.*,RA7t,RA5t,OSt,NROSt'"],
		["standardIDs" , " --sP 'CB_forMoriond16_sigTTZ_bkgTT_T,CB_forMoriond16_sigTTZ_bkgTT_VT,RA7t,RA5t'"],
		]
	

	for p in processes:
		pn = p.replace(",", "_")
		cmd("mkdir -p " + publdir + "/effs/" + pn + " 2> /dev/null && cp /afs/cern.ch/user/g/gpetrucc/php/index.php " + publdir + "/effs/" + pn)
		for s in plots:
			for b in bins:
				cmd(effs.replace("<DEN>", b[1]) + " -p " + p + " -o " + publdir + "/effs/" + pn + "/" + b[0] + "_" + s[0] + ".root " + b[2] + " " + s[1])





