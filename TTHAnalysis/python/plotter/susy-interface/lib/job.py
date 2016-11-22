import os
from functions import *

class Job():
	def __init__(self, master, name, commands, options, forceLocal = False):
		self.master     = master
		self.id         = "job"+timestamp(False)
		self.name       = name
		self.commands   = commands
		self.options    = options
		self.forceLocal = forceLocal
		testqueue       = ["8nm", "1nh", "8nh", "1nd", "2nd", "1nw", "2nw"]
		self.template   = "lxbatch_runner.sh"
		if "t3ui" in os.environ["HOSTNAME"]:
			testqueue = ["short.q", "all.q", "long.q"]
			self.template = "psibatch_runner.sh"
		elif "uniovi" in os.environ["HOSTNAME"]:
			testqueue = ["batch"]
			self.template = "oviedobatch_runner.sh"
		self.script     = self.master.srcpath +"/submitJob_"+name+".sh"
		if self.options.queue and not any([t in self.options.queue for t in testqueue]):
		#if self.options.queue and not self.options.queue in testqueue:
			self.master.error("Cannot find queue '"+self.options.queue+"' on this system.")
		self.prepare()
	def addCommands(self, commands):
		self.commands += commands
	def batchRuns(self):
		if hasattr(self, "batchDone"): return self.batchDone
		if self.batchId==-1 or not self.options.queue: return False
		if any([t in self.options.queue for t in ["all.q", "long.q", "short.q"]]):
		#if self.options.queue in ["all.q", "long.q", "short.q", "all.q@t3wn59.psi.ch"]:
			jobLine = bash("qstat -j "+str(self.batchId))
			toReturn = not(jobLine=="" or "Following jobs do not exist" in jobLine)
		elif any([t in self.options.queue for t in ["batch"]]):
		#elif self.options.queue in ["batch"]:
			jobLine = bash("qstat "+str(self.batchId))
			toReturn = not(jobLine=="" or "Unknown Job Id Error" in jobLine)
		else:
			jobLine = bash("bjobs "+str(self.batchId))
			toReturn = not(jobLine=="" or "Job <"+str(self.batchId)+"> is not found" in jobLine)
		if toReturn: self.batchDone = True
		return toReturn
	def isDone(self):
		return os.path.exists(self.master.jobpath+"/"+self.id)
	def isError(self):
		stillRunning = self.batchRuns() # will be False for local job
		if stillRunning: return False
		if not os.path.exists(self.master.jobpath+"/"+self.id): return True
		return os.path.exists(self.master.jobpath+"/err_"+self.id)
	def prepare(self):
		## PLACEHOLDER is replaced later
		template = [l.strip("\n") for l in open("susy-interface/scripts/"+self.template).readlines()]
		f = open(self.script, "w")
		for line in template:
			line = line.replace("[WORK]"       , self.master.workdir                  )
			line = line.replace("[SRC]"        , self.master.cmssw+"/src"             )
			line = line.replace("[INST]"       , self.master.instance                 )
			line = line.replace("[JOBDIR]"     , self.master.jobpath                  )
			line = line.replace("[JOBID]"      , self.id                              )
			f.write(line+"\n")
		f.close()
		cmd("chmod 755 "+self.script)
		cmd("chmod 755 "+self.master.jobpath)
	def prepareCommands(self):
		replaceInFile(self.script, "[PLACEHOLDER]", "\n".join([b for b in self.commands]))
	def run(self):
		self.prepareCommands() # here, because of the add commands method
		if self.options.queue and not self.forceLocal:
			super = "bsub -q {queue} -J SPM_{name} "
			if any([t in self.options.queue for t in ["all.q", "long.q", "short.q"]]):
			#if self.options.queue in ["all.q", "long.q", "short.q", "all.q@t3wn59.psi.ch"]:
				super = "qsub -q {queue} -N SPM_{name} "
			elif any([t in self.options.queue for t in ["batch"]]):
			#elif self.options.queue in ["batch"] and os.path.isdir('/pool/ciencias/'):
				super = "qsub -q {queue} -N SPM_{name} "
			super += "-o {dir}/submitJob_{name}.out -e {dir}/submitJob_{name}.err "
			super = super.format(queue=self.options.queue, name=self.name, dir=self.master.logpath)
		else:
			super = "source "
		self.batchId = self.runCmd(super + self.script)
	def runCmd(self, theCmd):
		jobLine = bash(theCmd)
		theId   = -1
		if not self.options.queue or self.forceLocal: return theId
		if   any([t in self.options.queue for t in ["all.q", "long.q", "short.q"]]): theId=int(jobLine.split()[2])
		elif any([t in self.options.queue for t in ["batch"]                     ]): theId=int(jobLine.split('.')[0])
		#if   self.options.queue in ["all.q", "long.q", "short.q"]                : theId=int(jobLine.split()[2])
		#elif self.options.queue in ["batch"] and os.path.isdir('/pool/ciencias/'): theId=int(jobLine.split('.')[0])
		else: theId = int(jobLine.split()[1].strip("<").strip(">"))
		return theId




