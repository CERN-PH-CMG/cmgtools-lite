import ROOT, os, copy, sys, time
from string import Formatter
from functions import *
from custom import *
from job import *

def addMakerOptions(parser):
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
	def __init__(self, base, args, options):
		self.cmssw   = os.environ["CMSSW_BASE"]
		self.workdir = self.cmssw   +"/src/CMGTools/TTHAnalysis/python/plotter"
		self.dir     = self.workdir +"/susy-interface"
		self.tmpdir  = self.dir     +"/tmp"
		self.instance = timestamp(False)
		self.jobpath  = self.tmpdir+"/"+self.instance+"/job"
		self.logpath  = self.tmpdir+"/"+self.instance+"/log"
		self.srcpath  = self.tmpdir+"/"+self.instance+"/src"
		self.tmppath  = self.tmpdir+"/"+self.instance+"/tmp"
		mkdir(self.tmpdir , False)
		mkdir(self.jobpath, False)
		mkdir(self.logpath, False)
		mkdir(self.srcpath, False)
		mkdir(self.tmppath, False)
		self.use = {}
		self.base = base
		self.parseBase()
		configsC = Collection(self.dir+"/env/configs")
		self.config  = configsC.get(args[0])
		self.loadRegions(args[1])
		self.treedir = args[2].rstrip("/")
		self.outdir  = args[3].rstrip("/")
		self.options = options
	def clearJobs(self):
		self.talk("Checking job status")
		if hasattr(self, "jobs") and len(self.jobs)>0:
			njobs = [j.isDone() or j.isError() for j in self.jobs].count(False)
			while njobs > 0:
				nerr = [j.isError() for j in self.jobs].count(True)
				self.talk(str(njobs)+"/"+str(len(self.jobs))+" jobs are running. Checking back in 5 seconds...")
				time.sleep(5)
				njobs = [j.isDone() or j.isError() for j in self.jobs].count(False)
			nerr = [j.isError() for j in self.jobs].count(True)
			if nerr>0:
				self.error(str(nerr)+"/"+str(len(self.jobs))+" jobs have finished in error state.")
		self.jobs = []
		cleandir(self.jobpath, False)
		return True
	def collectFlags(self, additionals = "", useWeight = True, isFastSim = False):
		if not hasattr(self, "flags"): 
			self.flags =      getattr(self.config , "flags", [])
			self.flags.extend(getattr(self.region , "flags", []))
			self.flags.extend(getattr(self.options, "flags", []))
			self.flags.extend(getattr(self.config , additionals, []))
			self.flags.extend(getattr(self.region , additionals, []))
			self.flags.extend(getattr(self.options, additionals, []))
		theflags = copy.deepcopy(self.flags)
		weight   = self.getWeight(isFastSim)
		if useWeight and weight: theflags.append("-W '"+weight+"'")
		theflags = filter(lambda x: x, theflags)
		return " ".join(theflags)
	def collectFriends(self):
		return " ".join(self.getFriends())
	def collectMacros(self):
		use = getattr(self.config, "macros", [])
		if len(self.options.macros)>0: use = self.options.macros
		return " ".join(["--load-macro "+m for m in use])
	def collectMCCs(self):
		use = getattr(self.config, "mccs", [])
		if len(self.options.mccs)>0: use = self.options.mccs
		return " ".join(["--mcc "+m for m in use])
	def collectProcs(self):
		return " ".join(["-p "+p for p in self.getProcs()])
	def error(self, message):
		self.talk(message, True)	
	def getAllProcs(self):
		regprocs  = ["data"] + getattr(self.region, "bkgs", []) + getattr(self.region, "sigs", [])
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
		procs = getattr(self.region, "bkgs", [])
		if len(self.options.bkgs)>0: procs = self.options.bkgs
		return procs
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
	def getProcs(self):
		procs = self.getBkgs() + self.getSigs()
		if len(self.options.procs)>0: procs = self.options.procs
		return self.options.procs
	def getSigs(self):
		procs = getattr(self.region, "sigs", [])
		if len(self.options.sigs)>0: procs = self.options.sigs
		return procs
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
		if                             hasattr(self.options, var) and getattr(self.options, var): return getattr(self.options, var)
		if hasattr(self, "model" ) and hasattr(self.model  , var) and getattr(self.model  , var): return getattr(self.model  , var)
		if hasattr(self, "region") and hasattr(self.region , var) and getattr(self.region , var): return getattr(self.region , var)
		if                             hasattr(self.config , var) and getattr(self.config , var): return getattr(self.config , var)
		return default
	def getWeight(self, isFastSim = False):
		weight = None
		if               self.getVariable("weight"  ): weight =  self.getVariable("weight")
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
	def loadRegions(self, arg):
		allregions = Collection(self.dir+"/env/regions")
		self.regions = [allregions.get(a) for a in arg.split(";")]
	def parseBase(self):
		self.keys = filter(lambda x: x, [i[1] for i in Formatter().parse(self.base)])
	def reloadBase(self, newbase):
		self.base = newbase
		self.parseBase()
	def makeCmd(self, args):
		if len(args) != len(self.keys): 
			print "error, not all arguments given"
			return -1
		dict = {}
		for i,k in enumerate(self.keys):
			dict[k] = args[i]
		return self.base.format(**dict)
	def prepareSplit(self, samplename):
		nevt = int(self.getNEvtSample(samplename))
		path = self.getTFilePath(samplename)
		if not path: return
		file = ROOT.TFile.Open(path,"read")
		if not file: return
		all  = file.Get("tree").GetEntries()
		file.Close()
		chunks = int(all)/nevt + 1
		self.bunches = [nevt for i in range(chunks-1)] + [int(all)%nevt]
	def resetModel(self):
		self.modelIdx = -1
	def runCmd(self, cmd, name = "maker", forceLocal = False):
		if self.options.pretend: 
			print cmd
			return -1
		return self.runJob(name, [cmd], forceLocal)
	def registerCmd(self, cmd, name = "maker", forceLocal = False):
		if self.options.pretend:
			print cmd
			return -1
		return self.registerJob(name, [cmd], forceLocal)
	def registerJob(self, name, commands, forceLocal = False):
		if not hasattr(self, "jobs"): self.jobs = []
		self.jobs.append(Job(self, name, commands, self.options, forceLocal))
	def runJob(self, name, commands, forceLocal = False):
		self.talk("Submitting job '"+name+"'")
		theJob = Job(self, name, commands, self.options, forceLocal)
		theJob.run()
		while not (theJob.isDone() or theJob.isError()):
			self.talk("Job '"+name+"' still running. Checking back in 5 seconds...")
			time.sleep(5)
		if theJob.isError():
			self.error("Job '"+name+"' has finished in error state.")
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
			if run: self.runCmd     (theCmd, name+"_"+str(b), forceLocal)
			else  : self.registerCmd(theCmd, name+"_"+str(b), forceLocal)
	def talk(self, message, isError=False):
	    if isError:
	        print "ERROR: "+message
	        print "Aborting..."
	        sys.exit()
	    print timestamp()+": "+message
	def useVar(self, key, value):
		self.use[key] = value

	##	script = self.srcpath + "/submitJob_" + name + ".sh"
	##	runner = "lxbatch_runner.sh"
	##	if queue in ["short.q", "all.q", "long.q"]:
	##		runner = "psibatch_runner.sh"
	##	elif queue in ["batch"] and os.path.isdir('/pool/ciencias/'):
	##		runner = "oviedobatch_runner.sh"
	##	cp("susy-interface/scripts/" + runner, script)
	##	replaceInFile(script, "WORK=$1; shift", "WORK=\"" + self.workdir + "\"")
	##	replaceInFile(script, "SRC=$1; shift" , "SRC=\"" + self.cmssw + "/src\"")
	##	replaceInFile(script, "INST=$1; shift" , "INST=\"" + self.instance + "\"")
	##	replaceInFile(script, "[PLACEHOLDER]" , "\n".join([b for b in commands])+"\n")
	##	cant = needHold and not queue in ["short.q", "all.q", "long.q"]
	##	if queue and not cant:
	##		return self.submitOnBatch(name, script, queue, setHold)
	##	else:
	##		cmd("source " + script)
	##		return -1
	##def submitOnBatch(self, name, script, queue, setHold = -1):
	##	super = "bsub -q {queue} -J SUSY_{name} "
	##	if queue in ["all.q", "long.q", "short.q"]:
	##		super = "qsub -q {queue} -N SUSY_{name} "
	##	elif queue in ["batch"] and os.path.isdir('/pool/ciencias/'):
	##		super = "qsub -q {queue} -N AWSMUniovi_{name} "
	##	super += "-o {dir}/submitJob_{name}.out -e {dir}/submitJob_{name}.err "
	##	super = super.format(queue=queue, name=name, dir=self.logpath)
	##	if setHold > -1 and queue in ["all.q", "long.q", "short.q"]:
	##		super += " -hold_jid " + str(setHold) + " " 
	##	jobLine = bash(super + script) 
	##	if queue in ["all.q", "long.q", "short.q"]:
	##		jobId = int(jobLine.split()[2])
	##	elif queue in ["batch"] and os.path.isdir('/pool/ciencias/'):
	##		jobId = int(jobLine.split('.')[0])
	##	else:
	##		jobId = int(jobLine.split()[1].strip("<").strip(">"))
	##	return jobId
	

