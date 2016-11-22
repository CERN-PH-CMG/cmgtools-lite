import ROOT, os, copy, sys, time
from string import Formatter
from functions import *
from custom import *
from job import *
from init import *

def addMakerOptions(parser):
	parser.add_option("-j"       , "--jobs"       , dest="jobs"   , type="int"   , default=0     , help="Number of jobs in multi-processing")
	parser.add_option("-l"       , "--lumi"       , dest="lumi"   , type="string", default="12.9", help="Luminosity in /fb")
	parser.add_option("-o"       , "--out"        , dest="outname", type="string", default=None, help="Name of the production, default is name of config.") 
	parser.add_option("-q"       , "--queue"      , dest="queue"  , type="string", default=None, help="Submit jobs to batch system queue")
	parser.add_option("--flags"  , dest="flags"   , type="string" , action="append", default=[], help="Give additional strings to be added to the final command")
	parser.add_option("--mca"    , dest="mcafile" , type="string" , default=None, help="Overwrite the mca file from the config");
	parser.add_option("--cuts"   , dest="cutfile" , type="string" , default=None, help="Overwrite the cuts file from the config");
	parser.add_option("--plot"   , dest="plotfile", type="string" , default=None, help="Overwrite the plots file from the config");
	parser.add_option("--sys"    , dest="sysfile" , type="string" , default=None, help="Overwrite the syst file from the config");
	parser.add_option("--expr"   , dest="expr"    , type="string" , default=None, help="Overwrite the expr from the config");
	parser.add_option("--bins"   , dest="bins"    , type="string" , default=None, help="Overwrite the bins from the config");
	parser.add_option("--fmt"    , dest="fmt"     , type="string" , default=None, help="Overwrite the fmt from the config");
	parser.add_option("--mccs"   , dest="mccs"    , type="string" , action="append", default=[], help="Overwrite MCC from the config");
	parser.add_option("--macros" , dest="macros"  , type="string" , action="append", default=[], help="Overwrite macros from the config");
	parser.add_option("--pretend", dest="pretend" , action="store_true", default=False, help="Only write the commands");
	parser.add_option("--tree"   , dest="treename", type="string", default="treeProducerSusyMultilepton", help="Give name of tree producer")
	parser.add_option("--bkgs"   , dest="bkgs"    , type="string" , action="append", default=[], help="Overwrite the bkgs from the region")
	parser.add_option("--sigs"   , dest="sigs"    , type="string" , action="append", default=[], help="Overwrite the sigs from the region")
	parser.add_option("-p", "--procs" , dest="procs" , type="string" , action="append", default=[], help="Overwrite both bkgs and sigs from the region")
	parser.add_option("-W", "--weight", dest="weight", type="string" , default=None, help="Overwrite the weight expression")
	return parser

def splitLists(options):
	options.flags  = splitList(options.flags )
	options.mccs   = splitList(options.mccs  )
	options.macros = splitList(options.macros)
	options.bkgs   = splitList(options.bkgs  )
	options.sigs   = splitList(options.sigs  )
	options.procs  = splitList(options.procs )
	return options

class Maker():
	def __init__(self, module, base, args, options):
		self.module   = module
		self.base     = base
		self.args     = args
		self.options  = options
		self.cmssw    = os.environ["CMSSW_BASE"]
		self.workdir  = self.cmssw   +"/src/CMGTools/TTHAnalysis/python/plotter"
		self.dir      = self.workdir +"/susy-interface"
		self.tmpdir   = self.dir     +"/tmp"
		mkdir(self.tmpdir, False)
		self.instance = self.findInstance()
		mkcleandir(self.tmpdir+"/"+self.instance, False)
		self.init.write()
		self.jobpath  = self.tmpdir+"/"+self.instance+"/job"
		self.logpath  = self.tmpdir+"/"+self.instance+"/log"
		self.srcpath  = self.tmpdir+"/"+self.instance+"/src"
		self.tmppath  = self.tmpdir+"/"+self.instance+"/tmp"
		mkdir(self.jobpath, False)
		mkdir(self.logpath, False)
		mkdir(self.srcpath, False)
		mkdir(self.tmppath, False)
		self.use = {}
		self.parseBase()
		configsC = Collection(self.dir+"/env/configs")
		self.config  = configsC.get(self.args[0])
		self.loadRegions()
		self.treedir = self.args[2].rstrip("/")
		self.outdir  = self.args[3].rstrip("/")
	def addToTalk(self, message):
		print message # placeholder for now
	def clearJobs(self):
		self.talk("Checking job status")
		if hasattr(self, "jobs") and len(self.jobs)>0:
			njobs = [j.isDone() or j.isError() for j in self.jobs].count(False)
			while njobs > 0:
				nerr = [j.isError() for j in self.jobs].count(True)
				self.talk(str(njobs)+"/"+str(len(self.jobs))+" jobs are running. Checking back in 5 seconds...")
				time.sleep(5)
				njobs = [j.isDone() or j.isError() for j in self.jobs].count(False)
			jerr = [j for j in self.jobs if j.isError()]
			if len(jerr)>0:
				errorJobs = [j.name+": "+j.script for j in jerr]
				self.error(str(len(jerr))+"/"+str(len(self.jobs))+" jobs have finished in error state.\n"+"\n".join(errorJobs))
		self.jobs = []
		cleandir(self.jobpath, False)
		return True
	def collectFlags(self, additionals = "", useWeight = True, isFastSim = False, forceRedo = False):
		theflags = copy.deepcopy(getattr(self.config , "flags", []))
		theflags.extend(getattr(self.region , "flags", []))
		theflags.extend(self.getOption("flags", []))
		theflags.extend(getattr(self.config , additionals, []))
		theflags.extend(getattr(self.region , additionals, []))
		theflags.extend(self.getOption(additionals, []))
		weight   = self.getWeight(isFastSim)
		if useWeight and weight: theflags.append("-W '"+weight+"'")
		theflags = filter(lambda x: x, theflags)
		return " ".join(theflags)
		#self.flags = theFlags
		#if not hasattr(self, "flags") or forceRedo: 
		#	theFlags = copy.deepcopy(getattr(self.config , "flags", []))
		#	theFlags.extend(getattr(self.region , "flags", []))
		#	theFlags.extend(getattr(self.options, "flags", []))
		#	theFlags.extend(getattr(self.config , additionals, []))
		#	theFlags.extend(getattr(self.region , additionals, []))
		#	theFlags.extend(getattr(self.options, additionals, []))
		#	self.flags = theFlags
		#theflags = copy.deepcopy(self.flags)
		#weight   = self.getWeight(isFastSim)
		#if useWeight and weight: theflags.append("-W '"+weight+"'")
		#theflags = filter(lambda x: x, theflags)
		#return " ".join(theflags)
	def collectFriends(self):
		return " ".join(self.getFriends())
	def collectMacros(self):
		use = getattr(self.config, "macros", [])
		if len(self.getOption("macros",[]))>0: use = self.getOption("macros",[])
		return " ".join(["--load-macro "+m for m in use])
	def collectMCCs(self):
		use = getattr(self.config, "mccs", [])
		if len(self.getOption("mccs", []))>0: use = self.getOption("mccs", [])
		return " ".join(["--mcc "+m for m in use])
	def collectProcs(self):
		return " ".join(["-p "+p for p in self.getProcs()])
	def error(self, message):
		self.talk(message, True)	
	def findInstance(self):
		init = None
		for inst in os.listdir(self.tmpdir):
			del init
			init = Init(self.tmpdir+"/"+inst+"/init")
			if init.identify(self.module, self.args, self.options):
				self.init = init
				return inst
		del init
		number = timestamp(False)
		self.init = Init(self.tmpdir+"/"+number+"/init")
		self.init.set(self.module, self.args, self.options)
		return number
	def getAllProcs(self):
		#regprocs  = ["data"] + getattr(self.region, "bkgs", []) + getattr(self.region, "sigs", [])
		regprocs  = ["data"] + self.getBkgs() + self.getSigs()
		pfull, s  = self.getStuffFromMCA()
		procs = []
		for pname in pfull:
			for p in regprocs:
				if re.match(p+"$", pname):
					procs.append(pname)
		return procs
	def getAllSamples(self, allSamples = False):
		pfull, s  = self.getStuffFromMCA()
		puse = pfull if allSamples else self.getAllProcs()
		samples   = []
		for p in puse:
			samples.extend(s[p])
		return samples
	def getBkgs(self):
		toReturn = splitList(getattr(self.region, "bkgs", []))
		if len(self.getOption("bkgs", []))>0: toReturn = splitList(self.getOption("bkgs", []))
		return toReturn
	def getExprCut(self):
		return getCut(getattr(self.config, "firstCut", "alwaystrue"), self.getVariable("expr"), self.getVariable("bins"))
	def getFriends(self):
		friends = []
		friends += ["-F sf/t {P}/"+f+"/evVarFriend_{cname}.root"    for f in getattr(self.config,"sfriends"  ,[])]
		friends += getattr(self.config, "friends" , [])
		friends += ["--FD sf/t {P}/"+f+"/evVarFriend_{cname}.root"  for f in getattr(self.config,"sdfriends" ,[])]
		friends += getattr(self.config, "dfriends" , [])
		friends += ["--FMC sf/t {P}/"+f+"/evVarFriend_{cname}.root" for f in getattr(self.config,"smcfriends",[])]
		friends += getattr(self.config, "mcfriends", [])
		return friends
	def getFriendLocations(self):
		fs = []
		fm = []
		for f in self.getFriends():
			if not f.strip(): continue
			ffm = f  .split()[2]
			ffm = ffm.replace("{P}/", "")
			ffm = ffm[0:ffm.rfind("/")]
			fm.append(ffm)
			fs.append(self.treedir +"/"+ ffm)
		return fs, fm	
	def getFriendModules(self):
		if len(self.options.modules)>0: return self.options.modules
		friendConn = self.getVariable("friendConn", {})
		return [k for k,v in friendConn.iteritems()]
	def getNEvtSample(self, sample):	
		samples = [l[0] for l in self.nevts]
		if sample in samples:
			return self.nevts[samples.index(sample)][1]
		filtered = filter(lambda x: x[0].find(sample)>-1, self.nevts)
		if len(filtered)>0:
			return str(max([int(l[1]) for l in filtered]))
		return "50000"
	def getOption(self, key, default = None):
		raw = getattr(self.options, key, default)
		if not raw or raw=="''" or raw=='""': raw = default
		return raw
	def getProcs(self):
		procs = self.getBkgs() + self.getSigs()
		if len(self.getOption("procs", []))>0: procs = splitList(self.getOption("procs", []))
		return procs
	def getSigs(self):
		toReturn = splitList(getattr(self.region, "sigs", []))
		if len(self.getOption("sigs", []))>0: toReturn = splitList(self.getOption("sigs", []))
		return toReturn
	def getStuffFromMCA(self):
		procs   = []
		samples = {}
		path = self.getVariable("mca")
		if not path: return
		for line in open(path, "r"):
			if re.match("\s*#.*", line): continue 
			line = re.sub(r"(?<!\\)#.*","",line)
			line = line.replace(r"\#","#")
			if ";" in line:
				(line,more) = line.split(";")[:2]
				for setting in [f.replace(';',',').strip() for f in more.replace('\\,',';').split(',')]:
					if "=" in setting:
						(key,val) = [f.strip() for f in setting.split("=")]
						extra[key] = eval(val)
					else: extra[setting] = True
			field = [f.strip() for f in line.split(':')]
			if len(field) <= 1: continue
			if "SkipMe" in extra and extra["SkipMe"] == True: continue
			pname = field[0]
			if pname[-1] == "+": pname = pname[:-1]
			if not pname in procs: procs.append(pname)
			samples[pname].append(field[1])
		return procs, samples
	def getScenario(self, perRegion=False):
		if perRegion and hasattr(self, "region"): return self.getScenario(False)+"/"+self.region.name
		return self.options.outname if self.options.outname else self.config.name
	def getTFilePath(self, samplename):
		thedir = self.treedir+"/"+samplename
		if not os.path.isdir(thedir): 
			return None
		if os.path.exists(thedir+"/"+self.options.treename+"/tree.root"): 
			return thedir+"/"+self.options.treename+"/tree.root"
		if os.path.exists(thedir+"/"+self.options.treename+"/tree.root.url"):
			return open(thedir+"/"+self.options.treename+"/tree.root.url","r").readlines()[0].rstrip("\n")
		return None
	def getVariable(self, var, default = None):
		if var in self.use.keys(): return self.use[var]
		if                             hasattr(self.options, var) and self.getOption(var, default): return self.getOption(var, default)
		if hasattr(self, "model" ) and hasattr(self.model  , var) and getattr(self.model  , var): return getattr(self.model  , var)
		if hasattr(self, "region") and hasattr(self.region , var) and getattr(self.region , var): return getattr(self.region , var)
		if                             hasattr(self.config , var) and getattr(self.config , var): return getattr(self.config , var)
		return default
	def getWeight(self, isFastSim = False):
		weight = None
		if               self.getVariable("weight"  ): weight = self.getVariable("weight")
		if isFastSim and self.getVariable("weightFS"): 
			if weight: weight = "("+weight+")*("+self.getVariable("weightFS")+")"
			else     : weight = self.getVariable("weightFS")
		return weight
	def iterateModel(self):
		if not hasattr(self, "modelIdx"): self.modelIdx = -1
		self.modelIdx += 1
		self.model = self.models[self.modelIdx]
	def iterateRegion(self):
		if not hasattr(self, "regionIdx"): self.regionIdx = -1
		self.regionIdx += 1
		self.region = self.regions[self.regionIdx]
	def loadNEvtSample(self):
		nevts      = [l.rstrip("\n").strip() for l in open(self.dir+"/env/nevtsamples", "r").readlines()]		
		nevts      = filter(lambda x: x, nevts)
		self.nevts = [[ll.strip() for ll in l.split(":")] for l in nevts]
	def loadModels(self):
		allmodels = Collection(self.dir+"/env/models")
		if len(self.options.models)==0: self.options.models = allmodels.getAllNames()
		self.models = [allmodels.get(m) for m in self.options.models]
	def loadRegions(self):
		allregions = Collection(self.dir+"/env/regions")
		self.regions = [allregions.get(a) for a in self.args[1].split(";")]
	def makeCmd(self, args):
		if len(args) != len(self.keys): 
			print "error, not all arguments given"
			return -1
		dict = {}
		for i,k in enumerate(self.keys):
			dict[k] = args[i]
		multi = " -j %d"%(self.options.jobs) if self.options.jobs>0 else ""
		return self.base.format(**dict) + multi
	def parseBase(self):
		self.keys = filter(lambda x: x, [i[1] for i in Formatter().parse(self.base)])
	def prepareSplit(self, samplename):
		nevt = int(self.getNEvtSample(samplename))
		path = self.getTFilePath(samplename)
		if not path: return
		file = ROOT.TFile.Open(path,"read")
		if not file: return
		all  = file.Get("tree").GetEntries()
		file.Close()
		chunks = int(all)/nevt + 1
		#self.bunches = [nevt for i in range(chunks-1)] + [int(all)%nevt]
		self.bunches = [nevt for i in range(chunks)]
	def registerCmd(self, cmd, name = "maker", forceLocal = False, collect = 0):
		if self.options.pretend:
			print cmd
			return
		self.registerJob(name, [cmd], forceLocal, collect)
	def registerJob(self, name, commands, forceLocal = False, collect = 0):
		if not hasattr(self, "jobs"    ): self.jobs = []
		if not hasattr(self, "jobcount"): self.jobcount = -1
		self.jobcount += 1
		if collect>0 and self.jobcount%collect != 0:
			self.jobs[-1].addCommands(commands)
			return
		self.jobs.append(Job(self, name, commands, self.options, forceLocal))
	def reloadBase(self, newbase):
		self.base = newbase
		self.parseBase()
	def resetModel(self):
		self.modelIdx = -1
	def resetRegion(self):
		self.regionIdx = -1
	def runCmd(self, cmd, name = "maker", forceLocal = False):
		if self.options.pretend: 
			print cmd
			return -1
		return self.runJob(name, [cmd], forceLocal)
	def runJob(self, name, commands, forceLocal = False):
		self.talk("Submitting job '"+name+"'")
		theJob = Job(self, name, commands, self.options, forceLocal)
		theJob.run()
		while not (theJob.isDone() or theJob.isError()):
			self.talk("Job '"+name+"' still running. Checking back in 5 seconds...")
			time.sleep(5)
		if theJob.isError():
			self.error("Job '"+name+"' ("+theJob.script+") has finished in error state.")
		del theJob
	def runJobs(self):
		self.talk("Submitting "+str(len(getattr(self,"jobs",[])))+" jobs")
		for job in getattr(self,"jobs",[]):
			job.run()
	def submit(self, args, name = "maker", run = True, forceLocal = False):
		self.talk("Preparing job '"+name+"'")
		cmd = self.makeCmd(args)
		if run: self.runCmd     (cmd, name, forceLocal)
		else  : self.registerCmd(cmd, name, forceLocal)
	def splittedSubmit(self, args, name = "maker", run = True, forceLocal = False, cFlag="-c", nFlag="-N"):
		self.talk("Preparing splitted job '"+name+"'")
		if not hasattr(self, "bunches") or self.bunches == [] or self.bunches == [0]:
			self.submit(args, name, run, forceLocal)
			return
		base = self.makeCmd(args)
		for b,n in enumerate(self.bunches):
			theCmd = base
			if n>0: theCmd +=" {C} {B} {N} {M}".format(C=cFlag, B=b, N=nFlag, M=n)
			if run: self.runCmd     (theCmd, name+"_"+str(b), forceLocal, )
			else  : self.registerCmd(theCmd, name+"_"+str(b), forceLocal)
	def talk(self, message, isError=False):
	    if isError:
	        print "ERROR: "+message
	        print "Aborting..."
	        sys.exit()
	    print timestamp()+": "+message
	def useVar(self, key, value):
		self.use[key] = value
