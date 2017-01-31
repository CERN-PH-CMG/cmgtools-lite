import os
from optparse import OptionParser
from lib import maker
from lib import functions as func

def getXS(xs, mass, factor):
	themass = [p[0] for p in xs]
	thexs   = [p[1] for p in xs]
	return str(thexs[themass.index(float(mass))]) + "*" + str(factor)

def prepareJob(mm, name, mp, baseSig, binning, bkgpath, outpath, xslist, options):

	mp = [m.strip() for m in mp]
	#name = "mp_"+mm.model.name+"_"+mp[0]+"_"+mp[1]
	sig  = mm.model.name +"_"+ mp[0] +"_"+ mp[1]
	xs = getXS(xslist, float(mp[0]), mm.model.brcorr)

	source  = open("susy-interface/scripts/job_scanmaker.py", "r").readlines()

	tmpfile = open(mm.srcpath +"/submitJob_"+ name +".py", "w")
	for line in source:
		line = line.replace("THENAME"      , name                                              )
		line = line.replace("THESIGNAL"    , sig                                               )
		line = line.replace("THEMASS1"     , mp[0]                                             )
		line = line.replace("THEMASS2"     , mp[1]                                             )
		line = line.replace("THEOFFSET"    , func.getOffset(mm.getVariable("expr",""), binning))
		line = line.replace("THEFILE"      , mp[2]                                             )
		line = line.replace("THEXS"        , xs                                                ) 
		line = line.replace("THEQ2FILE"    , mm.getVariable("q2accfile","")                    )
		line = line.replace("THEQ2SYNTAX"  , mm.getVariable("q2accformat","")                  )
		line = line.replace("THEWEIGHTSTR" , mm.getVariable("mcaWeightFS","1.0")               )
		line = line.replace("THEFRFILES"   , "["+",".join(["\""+f+"\"" for f in mm.getVariable("frFilesFS","").split(";")])+"]")
		line = line.replace("THEJEC"       , mm.getVariable("jec","")                          )
		line = line.replace("THEMET"       , mm.getVariable("met","")                          )
		line = line.replace("THEQ2ACC"     , mm.getVariable("q2acc","")                        )
		line = line.replace("THEFRJEC"     , "["+",".join(["\""+f+"\"" for f in mm.getVariable("frFilesFSJec","").split(";")])+"]")
		line = line.replace("THEWVJEC"     , "["+",".join(["\""+f+"\"" for f in mm.getVariable("wVarsFSJec"  ,"").split(";")])+"]")
		line = line.replace("THEFRMET"     , "["+",".join(["\""+f+"\"" for f in mm.getVariable("frFilesFSMet","").split(";")])+"]")
		line = line.replace("THEWVMET"     , "["+",".join(["\""+f+"\"" for f in mm.getVariable("wVarsFSMet"  ,"").split(";")])+"]")
		line = line.replace("THEWEIGHTVARS", "{"+",".join(["\""+k+"\":[" + ",".join("\""+v+"\"" for v in vals) + "]" for k,vals in mm.getVariable("wVarsFS",{}).iteritems()])+"}")
		line = line.replace("THEMCADIR"    , mm.tmppath                                        )
		line = line.replace("THEBKGDIR"    , bkgpath                                           )
		line = line.replace("THEOUTDIR"    , outpath                                           )
		line = line.replace("THEMCA"       , mm.getVariable("mcafile","")                      )
		line = line.replace("THESYST"      , mm.getVariable("sysfile","")                      )
		line = line.replace("THEBASE"      , baseSig                                           )
		tmpfile.write(line)
	tmpfile.close()
	return "python "+ mm.srcpath +"/submitJob_"+ name +".py"

	
parser = OptionParser(usage="%prog cfg regions treedir outdir [options]")
parser = maker.addMakerOptions(parser)
parser.add_option("--WFS"         , dest="weightFS"   , type="string"      , default=None , help="Overwrite the weightFS expression");
parser.add_option("--q2accfile"   , dest="q2accfile"  , type="string"      , default=None , help="Overwrite the q2accfile expression");
parser.add_option("--q2accformat" , dest="q2accformat", type="string"      , default=None , help="Overwrite the q2accfile expression");
parser.add_option("--bkgOnly"     , dest="bkgOnly"    , action="store_true", default=False, help="Only run the bkg only");
parser.add_option("--sigOnly"     , dest="sigOnly"    , action="store_true", default=False, help="Only run the signal (if bkg already is present)");
parser.add_option("--perBin"      , dest="perBin"     , action="store_true", default=False, help="Make datacards for every bin in 'expr' separately.");
parser.add_option("-m", "--models", dest="models"     , action="append"    , default=[]   , help="Fastsim signal models to loop upon.");
parser.add_option("--redoBkg"     , dest="redoBkg"    , action="store_true", default=False, help="Redo bkg if it already exists.");

baseBkg = "python makeShapeCardsSusy.py {MCA} {CUTS} \"{EXPR}\" \"{BINS}\" -o SR --bin {TAG} -P {T} --tree {TREENAME} {MCCS} {MACROS} --s2v -f -l {LUMI} --od {O} {FRIENDS} {FLAGS} {OVERFLOWCUTS}"
baseSig = "python makeShapeCardsSusy.py [[[MCA]]] {CUTS} \\\"{EXPR}\\\" \\\"{BINS}\\\" [[[SYS]]] -o SR --bin {TAG} -P {T} --tree {TREENAME} {MCCS} {MACROS} --s2v -f -l {LUMI} --od [[[O]]] {FRIENDS} {FLAGS} {OVERFLOWCUTS}"
(options, args) = parser.parse_args()
options         = maker.splitLists(options)
options.models  = func.splitList(options.models)
mm              = maker.Maker("scanmaker", baseBkg, args, options)
mm.loadModels()

friends = mm.collectFriends()	
mccs    = mm.collectMCCs   ()
macros  = mm.collectMacros ()	
sl      = str(options.lumi).replace(".","p")


## first do bkg
if not options.sigOnly:

	mm.reloadBase(baseBkg)
	mm.resetRegion()

	## looping over regions
	for r in range(len(mm.regions)):
		mm.iterateRegion()
		
		sc    = mm.getScenario(True)
		flags = mm.collectFlags("flagsScans", True, False, True)
	
		## looping over binnings
		binnings = [mm.getVariable("bins","")] if not options.perBin else getAllBins(mm.getVariable("bins",""))
		for ib,b in enumerate(binnings):
			
			## change scenario if looping over all bins
			if options.perBin: 
				min, max = getMinMax(b)
				sc += "_" + min.replace(".","p")
		
			## background first
			output = mm.outdir +"/"+ sc +"/"+ sl +"fb" 
			bkgDir = output +"/bkg"
			if not options.redoBkg and os.path.exists(bkgDir+"/common/SR.input.root"): continue
			func.mkdir(bkgDir)
		
			mm.submit([mm.getVariable("mcafile",""), mm.getVariable("cutfile",""), mm.getVariable("expr",""), mm.getVariable("bins",""), sc.replace("/","_"), mm.treedir, options.treename, mccs, macros, options.lumi, bkgDir, friends, flags, func.getCut(mm.getVariable("firstCut","alwaystrue"), mm.getVariable("expr",""), mm.getVariable("bins",""))],sc.replace("/", "_")+"_bkg",False)
	mm.runJobs()
	mm.clearJobs()
		


## second do models
if not options.bkgOnly:
	
	mm.reloadBase(baseSig)
	mm.resetRegion()

	## looping over regions
	for r in range(len(mm.regions)):
		mm.iterateRegion()
	
		sc    = mm.getScenario(True)
		flags = mm.collectFlags("flagsScans", True, False, True)
	
		## looping over binnings
		binnings = [mm.getVariable("bins","")] if not options.perBin else getAllBins(mm.getVariable("bins",""))
		for ib,b in enumerate(binnings):
			
			## change scenario if looping over all bins
			if options.perBin: 
				min, max = getMinMax(b)
				sc += "_" + min.replace(".","p")
		
			## background first
			output = mm.outdir +"/"+ sc +"/"+ sl +"fb" 
	
			## looping over models
			mm.resetModel()

			for m in range(len(mm.models)):
				mm.iterateModel()
	
				myDir  = output +"/"+ mm.model.name 
				bkgDir = output +"/bkg"
				func.mkdir(myDir +"/acc")
				func.mkdir(myDir +"/mps")
	
				## prepare jobs for masspoints
				xslist = [l.rstrip("\n").split(":") for l in open(mm.model.xsecfile  , "r").readlines()]
				xslist = [[float(m.strip()),float(xs.strip())] for [m,xs,err] in xslist ]
				mps    = [l.rstrip("\n").split(":") for l in open(mm.model.masspoints, "r").readlines()]
				mps    = [[m[0].strip(), m[1].strip(), m[2].strip()] for m in mps]

				## looping over masspoints
				for iiii,mp in enumerate(mps):
					flags   = mm.collectFlags("flagsScans", True, True)
					thebase = mm.makeCmd([mm.getVariable("cutfile",""), mm.getVariable("expr",""), b, sc.replace("/","_"), mm.treedir, options.treename, mccs, macros, options.lumi, friends, flags, func.getCut(mm.getVariable("firstCut","alwaystrue"), mm.getVariable("expr",""), mm.getVariable("bins",""))])
					thecmd = prepareJob(mm, sc.replace("/", "_")+"_mp_"+mp[2], mp, thebase, b, bkgDir, myDir, xslist, options)
					mm.registerCmd(thecmd, sc.replace("/", "_")+"_mp_"+mp[2],False,10)
	mm.runJobs()
	mm.clearJobs()


	
