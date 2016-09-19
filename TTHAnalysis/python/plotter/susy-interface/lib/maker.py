import os
from string import Formatter
from functions import *
from custom import *

def addMakerOptions(parser):
	parser.add_option("-l"       , "--lumi"       , dest="lumi"   , type="string", default="12.9", help="Luminosity in /fb")
	parser.add_option("-o"       , "--out"        , dest="outname", type="string", default=None, help="Name of the production, default is name of config.") 
	parser.add_option("-q"       , "--queue"      , dest="queue"  , type="string", default=None, help="Submit jobs to batch system queue")
	parser.add_option("--flags"  , dest="flags"   , type="string" , action="append", default=[], help="Give additional strings to be added to the final command")
	parser.add_option("--flagsDumps" , dest="flagsDumps" , type="string" , action="append", default=[], help="Give additional strings to be added to the final command (only dumpmaker)")
	parser.add_option("--flagsEffs"  , dest="flagsEffs"  , type="string" , action="append", default=[], help="Give additional strings to be added to the final command (only effmaker)")
	parser.add_option("--flagsLimits", dest="flagsLimits", type="string" , action="append", default=[], help="Give additional strings to be added to the final command (only limitmaker)")
	parser.add_option("--flagsPlots" , dest="flagsPlots" , type="string" , action="append", default=[], help="Give additional strings to be added to the final command (only plotmaker)")
	parser.add_option("--flagsScans" , dest="flagsScans" , type="string" , action="append", default=[], help="Give additional strings to be added to the final command (only scanmaker)")
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

class Maker():
	def __init__(self, base, args, options):
		self.cmssw   = os.environ["CMSSW_BASE"]
		self.plotter = self.cmssw   +"/src/CMGTools/TTHAnalysis/python/plotter"
		self.dir     = self.plotter +"/susy-interface"
		self.tmpdir  = self.dir     +"/tmp"
		self.instance = timestamp(False)
		self.logpath  = self.tmpdir+"/"+self.instance+"/log"
		self.srcpath  = self.tmpdir+"/"+self.instance+"/src"
		self.tmppath  = self.tmpdir+"/"+self.instance+"/tmp"
		mkdir(self.tmpdir , False)
		mkdir(self.logpath, False)
		mkdir(self.srcpath, False)
		mkdir(self.tmppath, False)
		self.use = {}
		self.base = base
		self.parseBase()
		configs = Collection(self.dir+"/env/configs")
		regions = Collection(self.dir+"/env/regions")
		self.config  = configs.get(args[0])
		self.region  = regions.get(args[1])
		self.treedir = args[2].rstrip("/")
		self.outdir  = args[3].rstrip("/")
		self.options = options
		self.updateConfig()
		self.updateRegion()
	def collectFlags(self, additionals = "", useWeight = True):
		if not hasattr(self, "flags"): 
			self.flags = self.config.flags
			self.flags.extend(self.region.flags)
			self.flags.extend(self.options.flags)
			self.flags.extend(getattr(self.config , additionals, []))
			self.flags.extend(getattr(self.region , additionals, []))
			self.flags.extend(getattr(self.options, additionals, []))
			if useWeight and self.getVariable("weight"): self.flags.append("-W '"+self.getVariable("weight")+"'")
			self.flags = filter(lambda x: x, self.flags)
		return " ".join(self.flags)
	def collectFriends(self):
		return " ".join(self.getFriends())
	def collectMacros(self):
		use = self.config.macros
		if len(self.options.macros)>0: use = self.options.macros
		return " ".join(["--load-macro "+m for m in use])
	def collectMCCs(self):
		use = self.config.mccs
		if len(self.options.mccs)>0: use = self.options.mccs
		return " ".join(["--mcc "+m for m in use])
	def getAllProcs(self):
		regprocs  = ["data"] + m.region.bkgs + m.region.sigs
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
	def getExprCut(self):
		return getCut(self.config.firstCut, self.getVariable("expr"), self.getVariable("bins"))
	def getFriends(self):
		friends = []
		friends += ["-F sf/t {P}/"+f+"/evVarFriend_{cname}.root" for f in self.config.sfriends]
		friends += self.config.friends
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
	def getStuffFromMCA(self):
		procs   = []
		samples = {}
		path = self.getVariable("mca")
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
	def getScenario(self):
		return self.options.outname if self.options.outname else self.config.name
	def getVariable(self, var):
		if var in self.use.keys(): return self.use[var]
		if hasattr(self.options, var) and getattr(self.options, var): return getattr(self.options, var)
		if hasattr(self.region , var) and getattr(self.region , var): return getattr(self.region , var)
		if hasattr(self.config , var) and getattr(self.config , var): return getattr(self.config , var)
		return None
	def parseBase(self):
		self.keys = filter(lambda x: x, [i[1] for i in Formatter().parse(self.base)])
	def reloadBase(self, newbase):
		self.base = newbase
		self.parseBase()
	def submit(self, args):
		if len(args) != len(self.keys): 
			print "error, not all arguments given"
			return
		dict = {}
		for i,k in enumerate(self.keys):
			dict[k] = args[i]
		cmd = self.base.format(**dict)
		if self.options.pretend: 
			print cmd
			return
		self.submitJob("maker", [cmd], self.options.queue)
	def submitJob(self, name, commands, queue, setHold = -1, needHold = False):
		script = self.srcpath + "/submitJob_" + name + ".sh"
		runner = "lxbatch_runner.sh"
		if queue in ["short.q", "all.q", "long.q"]:
			runner = "psibatch_runner.sh"
		cp("susy-interface/scripts/" + runner, script)
		replaceInFile(script, "WORK=$1; shift", "WORK=\"" + os.getcwd() + "\"")
		replaceInFile(script, "SRC=$1; shift" , "SRC=\"" + os.getcwd().replace("/CMGTools/TTHAnalysis/python/plotter", "") + "\"")
		replaceInFile(script, "INST=$1; shift" , "INST=\"" + self.instance + "\"")
		replaceInFile(script, "[PLACEHOLDER]" , "\n".join([b for b in commands])+"\n")
		cant = needHold and not queue in ["short.q", "all.q", "long.q"]
		if queue and not cant:
			return self.submitOnBatch(name, script, queue, setHold)
		else:
			cmd("source " + script)
			return -1
	def submitOnBatch(self, name, script, queue, setHold = -1):
		super = "bsub -q {queue} -J SUSY_{name} "
		if queue in ["all.q", "long.q", "short.q"]:
			super = "qsub -q {queue} -N SUSY_{name} "
		super += "-o {dir}/submitJob_{name}.out -e {dir}/submitJob_{name}.err "
		super = super.format(queue=queue, name=name, dir=self.logpath)
		if setHold > -1 and queue in ["all.q", "long.q", "short.q"]:
			super += " -hold_jid " + str(setHold) + " " 
		jobLine = bash(super + script) 
		if queue in ["all.q", "long.q", "short.q"]:
			jobId = int(jobLine.split()[2])
		else:
			jobId = int(jobLine.split()[1].strip("<").strip(">"))
		return jobId
	def updateConfig(self):
		return self.config
	def updateRegion(self):
		if len(self.options.procs)>0: self.region.procs = self.options.procs
		if len(self.options.bkgs )>0: self.region.bkgs  = self.options.bkgs
		if len(self.options.sigs )>0: self.region.sigs  = self.options.sigs
		return self.region
	def useVar(self, key, value):
		self.use[key] = value
	

