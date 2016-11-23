from optparse import OptionParser
from lib import maker
from lib import functions as func

def getXS(xs, mass, factor):
	themass = [p[0] for p in xs]
	thexs   = [p[1] for p in xs]
	return str(thexs[themass.index(float(mass))]) + "*" + str(factor)

def prepareJob(mm, mp, baseSig, binning, bkgpath, outpath, xslist, options):

	mp = [m.strip() for m in mp]
	name = "mp_"+mm.model.name+"_"+mp[0]+"_"+mp[1]
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
		line = line.replace("THEWEIGHTSTR" , mm.getVariable("mcaWeightFS","")                  )
		line = line.replace("THEFRFILES"   , "["+",".join(["\""+f+"\"" for f in mm.getVariable("frFilesFS","").split(";")])+"]")
		line = line.replace("THEJEC"       , mm.getVariable("jec","")                          )
		line = line.replace("THEMET"       , mm.getVariable("met","")                          )
		line = line.replace("THEQ2ACC"     , mm.getVariable("q2acc","")                        )
		line = line.replace("THEFRJEC"     , "["+",".join(["\""+f+"\"" for f in mm.getVariable("frFilesFSJec","").split(";")])+"]")
		line = line.replace("THEWVJEC"     , "["+",".join(["\""+f+"\"" for f in mm.getVariable("wVarsFSJec"  ,"").split(";")])+"]")
		line = line.replace("THEFRMET"     , "["+",".join(["\""+f+"\"" for f in mm.getVariable("frFilesFSMet","").split(";")])+"]")
		line = line.replace("THEWVMET"     , "["+",".join(["\""+f+"\"" for f in mm.getVariable("wVarsFSMet"  ,"").split(";")])+"]")
		line = line.replace("THEWEIGHTVARS", "{"+",".join(["\""+k+"\":[" + ",".join("\""+v+"\"" for v in vals) + "]" for k,vals in mm.getVariable("wVarsFS","").iteritems()])+"}")
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

baseBkg = "python makeShapeCardsSusy.py {MCA} {CUTS} \"{EXPR}\" \"{BINS}\" -o SR --bin {TAG} -P {T} --tree {TREENAME} {MCCS} {MACROS} --s2v -f -j 4 -l {LUMI} --od {O} {FRIENDS} {FLAGS} {OVERFLOWCUTS}"
baseSig = "python makeShapeCardsSusy.py [[[MCA]]] {CUTS} \\\"{EXPR}\\\" \\\"{BINS}\\\" [[[SYS]]] -o SR --bin {TAG} -P {T} --tree {TREENAME} {MCCS} {MACROS} --s2v -f -j 4 -l {LUMI} --od [[[O]]] {FRIENDS} {FLAGS} {OVERFLOWCUTS}"
(options, args) = parser.parse_args()
options         = maker.splitLists(options)
options.models  = func.splitList(options.models)
mm              = maker.Maker(baseBkg, args, options)
mm.loadModels()

sl = str(options.lumi).replace(".","p")


## looping over regions
for r in range(len(mm.regions)):
	mm.iterateRegion()
	
	friends = mm.collectFriends()	
	mccs    = mm.collectMCCs   ()
	macros  = mm.collectMacros ()	
	sc      = mm.getScenario(True)

	## looping over binnings
	binnings = [mm.getVariable("bins","")] if not options.perBin else getAllBins(mm.getVariable("bins",""))
	for ib,b in enumerate(binnings):
		
		## change scenario if looping over all bins
		if options.perBin: 
			min, max = getMinMax(b)
			sc += "_" + min.replace(".","p")
	
		## background first
		mm.reloadBase(baseBkg)
		flags  = mm.collectFlags("flagsScans")
		output = mm.outdir +"/"+ sc +"/"+ sl +"fb" 
		bkgDir = output +"/bkg"
		func.mkdir(bkgDir)
	
		bkgId  = -1
		if not options.sigOnly:
			bkgId = mm.submit([mm.getVariable("mcafile",""), mm.getVariable("cutfile",""), mm.getVariable("expr",""), mm.getVariable("bins",""), sc.replace("/","_"), mm.treedir, options.treename, mccs, macros, options.lumi, bkgDir, friends, flags, func.getCut(mm.getVariable("firstCut","alwaystrue"), mm.getVariable("expr",""), mm.getVariable("bins",""))],sc+"_"+mm.region.name+"_bkg",False)
			mm.clearJobs()
	
		if options.bkgOnly: continue
	
	
		## looping over models
		mm.reloadBase(baseSig)
		mm.resetModel()

		for m in range(len(mm.models)):
			mm.iterateModel()
	
			myDir = output +"/"+ mm.model.name 
			func.mkdir(myDir +"/acc")
			func.mkdir(myDir +"/mps")
	
	
			## prepare jobs for masspoints
			xslist = [l.rstrip("\n").split(":") for l in open(mm.model.xsecfile  , "r").readlines()]
			xslist = [[float(m.strip()),float(xs.strip())] for [m,xs] in xslist ]
			mps    = [l.rstrip("\n").split(":") for l in open(mm.model.masspoints, "r").readlines()]
	
			## looping over masspoints
			for mp in mps:
				flags   = mm.collectFlags("flagsScans", True, True)
				thebase = mm.makeCmd([mm.getVariable("cutfile",""), mm.getVariable("expr",""), b, sc.replace("/","_"), mm.treedir, options.treename, mccs, macros, options.lumi, friends, flags, func.getCut(mm.getVariable("firstCut","alwaystrue"), mm.getVariable("expr",""), mm.getVariable("bins",""))])
				thecmd = prepareJob(mm, mp, thebase, b, bkgDir, myDir, xslist, options)
				mm.registerCmd(thecmd,sc+"_"+mm.region.name+"_"+mp)
				break	
		mm.runJobs()
		mm.clearJobs()


	
