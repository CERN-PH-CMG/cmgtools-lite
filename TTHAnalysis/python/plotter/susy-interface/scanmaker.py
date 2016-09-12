import sys, os, subprocess
from optparse import OptionParser
from lib import maker
from lib import functions as func

collectFlags("flagsScans")

def addOptions(base, options):
	if options.doS2V                 : base += " --s2v"
	if options.allowNegative         : base += " --neg"
	if options.hardZero              : base += " --hardZero"
	if len(options.negAllowed)    > 0: base += " " + " ".join(["--neglist " + m          for m in options.negAllowed    ])
	if options.jobs               > 0: base += " -j " + str(options.jobs)
	if options.lumi               > 0: base += " -l " + str(options.lumi)
	if len(options.friendTrees)   > 0: base += " " + " ".join(["-F " + f[0] + " " + f[1] for f in options.friendTrees   ])
	if len(options.mcCorrs)       > 0: base += " " + " ".join(["--mcc " + m              for m in options.mcCorrs       ])
	if len(options.loadMacro)     > 0: base += " " + " ".join(["-L "    + m              for m in options.loadMacro     ])
	if len(options.plotmergemap)  > 0: base += " " + " ".join(["--plotgroup " + p        for p in options.plotmergemap  ])
	if options.startCut              : base += " " + " -S " + options.startCut
	if options.upToCut               : base += " " + " -U " + options.upToCut 
	if len(options.cutsToExclude) > 0: base += " " + " ".join(["-X " + c                 for c in options.cutsToExclude ])
	if len(options.cutsToEnable)  > 0: base += " " + " ".join(["-E " + c                 for c in options.cutsToEnable  ])
	if len(options.cutsToInvert)  > 0: base += " " + " ".join(["-I " + c                 for c in options.cutsToInvert  ])
	if len(options.cutsToReplace) > 0: base += " " + " ".join(["-R " +c[0]+" "+c[1]+" '"+c[2]+"' " for c in options.cutsToReplace ])
	if len(options.cutsToAdd)     > 0: base += " " + " ".join(["-A " +c[0]+" "+c[1]+" '"+c[2]+"' " for c in options.cutsToAdd     ])
	if options.tree                  : base += " --tree " + options.tree
	if options.path                  : base += " --path " + options.path
	if options.noNegVar              : base += " --noNegVar"
	return base

def addOptionsSig(base, options):
	if len(options.ignore) > 0: base += " " + " ".join(["--ignore " + p for p in options.ignore ]) 
	return base

def addWeight(base, options, fastSim = False):
	weight = "1.0"
	if options.weightString              : weight += "*" + options.weightString
	if fastSim and options.weightStringFS: weight += "*" + options.weightStringFS
	if weight != "1.0": return base + " -W '" + weight + "'"
	return base

def getXS(xs, mass, factor):
	themass = [p[0] for p in xs]
	thexs   = [p[1] for p in xs]
	return str(thexs[themass.index(float(mass))]) + "*" + str(factor)

def prepareJob(name, thecmd, mp, model, config, b):
	global pypath, mcapath, outpath, xslist, options

	m1 = mp[0].strip()
	m2 = mp[1].strip()
	xs = getXS(xslist, float(m1), model.corr)
	print xs
	sig = model.name + "_" + m1 + "_" + m2

	source=open("susy-interface/scripts/job_scanmaker.py", "r").readlines()

	tmpfile = open(pypath + "/submitJob_" + name + ".py", "w")
	for line in source:
		line = line.replace("THESCRIPT"    , options.script                                                       )
		line = line.replace("THENAME"      , name                                                                 )
		line = line.replace("THESIGNAL"    , sig                                                                  )
		line = line.replace("THEMASS1"     , m1                                                                   )
		line = line.replace("THEMASS2"     , m2                                                                   )
		line = line.replace("THEOFFSET"    , getOffset(config.expr, b)                                            )
		line = line.replace("THEFILE"      , mp[2]                                                                )
		line = line.replace("THEXS"        , xs                                                                   ) 
		line = line.replace("THEQ2FILE"    , model.q2acc.split(",")[0] if model.q2acc.find(",")>-1 else ""        )
		line = line.replace("THEQ2SYNTAX"  , model.q2acc.split(",")[1] if model.q2acc.find(",")>-1 else ""        )
		line = line.replace("THEWEIGHTSTR" , config.weightString                                                  )
		line = line.replace("THEFRFILES"   , "["+",".join(["\""+f+"\"" for f in config.frFilesSignal   .split(",")])+"]")
		line = line.replace("THEJEC"       , config.jec                                                           )
		line = line.replace("THEMET"       , config.met                                                           )
		line = line.replace("THEQ2ACC"     , config.q2acc                                                         )
		line = line.replace("THEFRJEC"     , "["+",".join(["\""+f+"\"" for f in config.frFilesJec.split(",")])+"]")
		line = line.replace("THEWVJEC"     , "["+",".join(["\""+f+"\"" for f in config.wVarsJec  .split(",")])+"]")
		line = line.replace("THEFRMET"     , "["+",".join(["\""+f+"\"" for f in config.frFilesMet.split(",")])+"]")
		line = line.replace("THEWVMET"     , "["+",".join(["\""+f+"\"" for f in config.wVarsMet  .split(",")])+"]")
		line = line.replace("THEWEIGHTVARS", "{"+",".join(["\""+k+"\":[" + ",".join("\""+v+"\"" for v in vals) + "]" for k,vals in config.wVars.iteritems()])+"}")
		line = line.replace("THEMCADIR"    , mcapath                                                              )
		line = line.replace("THEOUTDIR"    , outpath                                                              )
		line = line.replace("THEMCA"       , config.mca                                                           )
		line = line.replace("THESYST"      , config.syst                                                          )
		line = line.replace("THECMDFIRST"  , "{CUTS} \\\"{EXPR}\\\" \\\"{BINS}\\\"".format(CUTS=config.cuts, EXPR=config.expr, BINS=b))
		line = line.replace("THECMDSECOND" , thecmd.split("[SYSTS]")[1])
		tmpfile.write(line)
	tmpfile.close()
	return "python " + pypath + "/submitJob_" + name + ".py"

def updateModel(model, options):
	model.q2acc = options.q2acc if not options.q2acc=="palimpalim" else model.q2acc
	return model

def updateConfig(config, options):
	config.expr     = options.expr if options.expr else config.expr
	config.bins     = options.bins if options.bins else config.bins
	config.mca      = options.mca  if options.mca  else config.mca
	config.cuts     = options.cuts if options.cuts else config.cuts
	config.syst     = options.syst if options.syst else config.syst
	config.firstCut = options.firstCut if options.firstCut else config.firstCut
	return config

parser = OptionParser(usage="%prog cfg model outdir [options]")
parser = maker.addMakerOptions(parser)
## tree2yield,mcAnalysis options
parser.add_option("-t", "--tree"        , dest="tree"         , default='ttHLepTreeProducerTTH', help="Pattern for tree name");
parser.add_option("-P", "--path"        , dest="path"         , type="string", default="./", help="path to directory with input trees and pickle files (./)") 
parser.add_option("-l", "--lumi"        , dest="lumi"         , type="float", default="19.7", help="Luminosity (in 1/fb)");
parser.add_option("-W", "--weightString", dest="weightString" , type="string", default="1", help="Use weight (in MC events)");
parser.add_option("-f", "--final"       , dest="final"        , action="store_true", help="Just compute final yield after all cuts");
parser.add_option("-S", "--start-at-cut", dest="startCut"     , type="string", help="Run selection starting at the cut matched by this regexp, included.") 
parser.add_option("-U", "--up-to-cut"   , dest="upToCut"      , type="string", help="Run selection only up to the cut matched by this regexp, included.") 
parser.add_option("-X", "--exclude-cut" , dest="cutsToExclude", action="append", default=[], help="Cuts to exclude (regexp matching cut name), can specify multiple times.") 
parser.add_option("-E", "--enable-cut"  , dest="cutsToEnable" , action="append", default=[], help="Cuts to enable if they were disabled in the cut file (regexp matching cut name), can specify multiple times.") 
parser.add_option("-I", "--invert-cut"  , dest="cutsToInvert" , action="append", default=[], help="Cuts to invert (regexp matching cut name), can specify multiple times.") 
parser.add_option("-R", "--replace-cut" , dest="cutsToReplace", action="append", default=[], nargs=3, help="Cuts to invert (regexp of old cut name, new name, new cut); can specify multiple times.") 
parser.add_option("-A", "--add-cut"     , dest="cutsToAdd"    , action="append", default=[], nargs=3, help="Cuts to insert (regexp of cut name after which this cut should go, new name, new cut); can specify multiple times.") 
parser.add_option("-F", "--add-friend",    dest="friendTrees",  action="append", default=[], nargs=2, help="Add a friend tree (treename, filename). Can use {name}, {cname} patterns in the treename") 
parser.add_option("--mcc", "--mc-corrections",    dest="mcCorrs",  action="append", default=[], nargs=1, help="Load the following file of mc to data corrections") 
parser.add_option("--s2v", "--scalar2vector",     dest="doS2V",    action="store_true", default=False, help="Do scalar to vector conversion") 
parser.add_option("--neg", "--allow-negative-results",     dest="allowNegative",    action="store_true", default=False, help="If the total yield is negative, keep it so rather than truncating it to zero") 
parser.add_option("-L", "--load-macro",  dest="loadMacro",   type="string", action="append", default=[], help="Load the following macro, with .L <file>+");
parser.add_option("-j", "--jobs",           dest="jobs", type="int", default=0, help="Use N threads");
parser.add_option("--plotgroup", dest="plotmergemap", type="string", default=[], action="append", help="Group plots into one. Syntax is '<newname> := (comma-separated list of regexp)', can specify multiple times. Note it is applied after plotting.")
parser.add_option("--neglist", dest="negAllowed", action="append", default=[], help="Give process names where negative values are allowed")
## makeShapeCards options
parser.add_option("--ignore",dest="ignore", type="string", default=[], action="append", help="Ignore processes when loading infile")
parser.add_option("--noNegVar",dest="noNegVar", action="store_true", default=False, help="Replace negative variations per bin by 0.1% of central value")
parser.add_option("--hardZero",dest="hardZero", action="store_true", default=False, help="Hard cutoff")
## scanmaker options
parser.add_option("-o"    , "--out"     , dest="outname", type="string", default=None, help="output name") 
parser.add_option("-q"    , "--queue"   , dest="queue"  , type="string", default=None, help="Submit jobs to batch system queue")
parser.add_option("--WFS" , "--weightStringFS", dest="weightStringFS" , type="string", default="1", help="Additional weight (in MC events) for FastSim");
parser.add_option("--expr",  dest="expr",   type="string", default=None, help="Overwrite the expression from the config");
parser.add_option("--bins",  dest="bins",   type="string", default=None, help="Overwrite the binning from the config");
parser.add_option("--mca" ,  dest="mca" ,   type="string", default=None, help="Overwrite the mca file from the config");
parser.add_option("--cuts",  dest="cuts",   type="string", default=None, help="Overwrite the cuts file from the config");
parser.add_option("--syst",  dest="syst",   type="string", default=None, help="Overwrite the systs file from the config");
parser.add_option("--firstCut",  dest="firstCut", type="string", default=None, help="Overwrite the firstcut from the config");
parser.add_option("--q2acc",  dest="q2acc",   type="string", default="palimpalim", help="Overwrite the q2acc file from the model");
parser.add_option("--script",  dest="script", type="string", default="makeShapeCardsSusy.py", help="Use a different makeShapeCardsSusy.py file. USE AT YOUR OWN RISK!");
parser.add_option("--bkgOnly",  dest="bkgOnly", action="store_true", default=False, help="Only run the bkg only");
parser.add_option("--sigOnly",  dest="sigOnly", action="store_true", default=False, help="Only run the signal (if bkg already is present)");
parser.add_option("--perBin",  dest="perBin", action="store_true", default=False, help="Run every value of the bin separately.");

(options, args) = parser.parse_args()
configs = Collection("susy-interface/env/scansetups")
models  = Collection("susy-interface/env/scanmodels" )
config  = configs.get(args[0])
model   = models .get(args[1])
outdir  = args[2]

config = updateConfig(config, options)
model  = updateModel (model , options)

binnings = [config.bins] if not options.perBin else getAllBins(config.bins)


## run binnings
for ib,b in enumerate(binnings):
	
	## change tag if looping over all bins
	tag = options.outname if options.outname else config.name
	if options.perBin: 
		min, max = getMinMax(b)
		tag += "_" + min.replace(".","p")


	## setup all directories
	#prod = datetime.datetime.now().strftime("%Y%m%d%H%M%S")+"_"+str(ib) 
	#prod = datetime.datetime.now().strftime("%Y%m%d%H%M%S")+"_"+tag+"_"+model.name 
	prod = model.name+"_"+tag
	tmppath = os.getcwd() + "/" + config.workdir + "/tmp/" + prod
	mcapath = tmppath        + "/mca"
	pypath  = tmppath        + "/py"
	shpath  = tmppath        + "/sh"
	logpath = tmppath        + "/log"
	mkdir(tmppath, False)
	mkdir(mcapath, False)
	mkdir(pypath , False)
	mkdir(shpath , False)
	mkdir(logpath, False)

	## create output directories
	outpath = outdir + "/" + tag + "/" + str(options.lumi) + "fb/" + model.name
	mkdir(outpath)
	mkdir(outpath + "/acc")
	mkdir(outpath + "/bkg")
	mkdir(outpath + "/mps")
	
	## prepare the command
	base = "python {sc} {MCA} {CUTS} \"{EXPR}\" \"{BINS}\" [SYSTS] -o SR {OVERFLOWCUTS} "
	base = base.format(sc=options.script, MCA=config.mca, CUTS=config.cuts, EXPR=config.expr, BINS=b, OVERFLOWCUTS=getCut(config.firstCut, config.expr, b))
	base = addOptions(base, options) + " --out SR --bin " + tag
	
	## run first on Data+Bkg
	myBase = addWeight(base.replace("[SYSTS]", ""), options, False) + " --od " + outpath + "/bkg" 
	bkgId  = -1
	if not options.sigOnly:
		bkgId  = submitJob("bkg", [myBase], options.queue, -1, True)

	if options.bkgOnly: continue
	
	## prepare jobs for masspoints
	xslist = [l.rstrip("\n").split(":") for l in open(model.xsec    , "r").readlines()]
	xslist = [[float(m.strip()),float(xs.strip())] for [m,xs] in xslist ]
	mps    = [l.rstrip("\n").split(":") for l in open(model.filelist, "r").readlines()]

	for mp in mps:
		mp = [m.strip() for m in mp]
		jobName="mp_"+mp[0]+"_"+mp[1]
		thecmd = prepareJob(jobName, addWeight(addOptionsSig(base, options), options, True), mp, model, config, b)
		submitJob(jobName, [thecmd], options.queue, bkgId)
	
