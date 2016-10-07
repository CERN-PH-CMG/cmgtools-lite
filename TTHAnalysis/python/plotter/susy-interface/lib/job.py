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
		self.template   = "lxbatch_runner.sh"
		if self.options.queue in ["short.q", "all.q", "long.q"]:
			self.template = "psibatch_runner.sh"
		elif self.options.queue in ["batch"] and os.path.isdir('/pool/ciencias/'):
			self.template = "oviedobatch_runner.sh"
		self.script     = self.master.srcpath +"/submitJob_"+name+".sh"
		self.prepare()
	def batchRuns(self):
		if self.batchId==-1: return False
		if self.options.queue in ["all.q", "long.q", "short.q"]:
			jobLine = bash("qstat -j "+str(self.batchId))
			return not(jobLine=="" or "Following jobs do not exist" in jobLine)
		elif self.options.queue in ["batch"] and os.path.isdir('/pool/ciencias/'):
			jobLine = bash("qstat "+str(self.batchId))
			return not(jobLine=="" or "Unknown Job Id Error" in jobLine)
		else:
			jobLine = bash("bjobs "+str(self.batchId))
			return not(jobLine=="" or "Job <"+str(self.batchId)+"> is not found" in jobLine)
		return False
	def isDone(self):
		return os.path.exists(self.master.jobpath+"/"+self.id)
	def isError(self):
		stillRunning = self.batchRuns() # will be False for local job
		if stillRunning: return False
		if not os.path.exists(self.master.jobpath+"/"+self.id): return True
		return os.path.exists(self.master.jobpath+"/err_"+self.id)
	def prepare(self):
		template = [l.strip("\n") for l in open("susy-interface/scripts/"+self.template).readlines()]
		f = open(self.script, "w")
		for line in template:
			line = line.replace("[WORK]"       , self.master.workdir                  )
			line = line.replace("[SRC]"        , self.master.cmssw+"/src"             )
			line = line.replace("[INST]"       , self.master.instance                 )
			line = line.replace("[PLACEHOLDER]", "\n".join([b for b in self.commands]))
			line = line.replace("[JOBDIR]"     , self.master.jobpath                  )
			line = line.replace("[JOBID]"      , self.id                              )
			f.write(line+"\n")
		f.close()
		cmd("chmod 755 "+self.script)
	def run(self):
		if self.options.queue and not self.forceLocal:
			super = "bsub -q {queue} -J SPM_{name} "
			if self.options.queue in ["all.q", "long.q", "short.q"]:
				super = "qsub -q {queue} -N SPM_{name} "
			elif self.options.queue in ["batch"] and os.path.isdir('/pool/ciencias/'):
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
		if   self.options.queue in ["all.q", "long.q", "short.q"]                : theId=int(jobLine.split()[2])
		elif self.options.queue in ["batch"] and os.path.isdir('/pool/ciencias/'): theId=int(jobLine.split('.')[0])
		else: theId   = int(jobLine.split()[1].strip("<").strip(">"))
		return theId
		cmd(super + self.script) 




